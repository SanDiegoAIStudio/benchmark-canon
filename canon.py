#!/usr/bin/env python3
"""Benchmark canon: look up, check and rebuild a ledger of AI benchmark verdicts.

Usage: python3 canon.py [--root DIR] COMMAND

  list      one line per benchmark, with --cat and --verdict filters
  cite      print one benchmark's verdict, caveat, source and a citation line
  check     find benchmark names in text files and report each one's verdict
  stale     list rows whose re-check date has arrived
  validate  check the data files for problems
  build     write canon.jsonl, CANON.md and index.html from the data files

The data lives in data/verdicts.json and data/canon.json, the per-benchmark
evidence in evidence/<id>.md and the per-category memos in memos/<cat>.md.
Standard library only; runs on Python 3.9 and later.
"""
import argparse
import calendar
import datetime
import difflib
import html
import json
import os
import re
import sys

DEFAULT_ROOT = os.path.dirname(os.path.abspath(__file__))
VERDICT_ORDER = ("canon", "caveat", "cut")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
    8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
    14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
    19: "nineteen", 20: "twenty",
}
CITE_LIMIT = 5


class CanonError(Exception):
    """A usage error or an unreadable file: one stderr line, exit code 2."""


# ---------------------------------------------------------------- loading

def read_text(path):
    """Return the UTF-8 text of a file or raise CanonError."""
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read()
    except UnicodeDecodeError:
        raise CanonError("cannot read %s: not UTF-8 text" % path)
    except OSError as exc:
        raise CanonError("cannot read %s: %s" % (path, exc.strerror or exc))


def read_json(path):
    text = read_text(path)
    try:
        return json.loads(text)
    except ValueError as exc:
        raise CanonError("cannot read %s: not valid JSON (%s)" % (path, exc))


def parse_date(text):
    """Parse YYYY-MM-DD or raise CanonError."""
    if not isinstance(text, str) or not DATE.match(text):
        raise CanonError("not a date (want YYYY-MM-DD): %r" % (text,))
    try:
        return datetime.date(int(text[0:4]), int(text[5:7]), int(text[8:10]))
    except ValueError:
        raise CanonError("not a date (want YYYY-MM-DD): %r" % (text,))


def add_months(day, months):
    """Add whole months to a date; the day of month is clamped to the month end."""
    index = day.year * 12 + (day.month - 1) + months
    year, month = divmod(index, 12)
    month += 1
    last = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, min(day.day, last))


class Data(object):
    """The two JSON documents plus the folder they came from."""

    def __init__(self, root, verdicts, canon):
        self.root = root
        self.verdicts = verdicts
        self.canon = canon
        self.rows = [r for r in verdicts.get("benchmarks", []) if isinstance(r, dict)]

    def labels(self):
        labels = self.canon.get("labels")
        return labels if isinstance(labels, dict) else {}

    def checked_of(self, row):
        return row.get("checked") or self.verdicts.get("checked")

    def months_for(self, cat):
        revet = self.canon.get("revet_months")
        revet = revet if isinstance(revet, dict) else {}
        months = revet.get(cat, revet.get("default", 6))
        return months if isinstance(months, int) else 6

    def due_of(self, row):
        checked = parse_date(self.checked_of(row))
        return add_months(checked, self.months_for(row.get("cat"))).isoformat()

    def evidence_of(self, row):
        return "evidence/%s.md" % row.get("id")

    def category_order(self):
        cats = list(self.labels().keys())
        for row in self.rows:
            if row.get("cat") not in cats:
                cats.append(row.get("cat"))
        return cats

    def ordered_rows(self):
        """Rows grouped by category in label order, then verdict, then name."""
        cats = self.category_order()

        def key(row):
            verdict = row.get("verdict")
            rank = VERDICT_ORDER.index(verdict) if verdict in VERDICT_ORDER else len(VERDICT_ORDER)
            return (cats.index(row.get("cat")), rank, str(row.get("name")).casefold(), str(row.get("name")))
        return sorted(self.rows, key=key)

    def counts(self):
        counts = {"benchmarks": len(self.rows)}
        for verdict in VERDICT_ORDER:
            counts[verdict] = len([r for r in self.rows if r.get("verdict") == verdict])
        return counts


def load(root):
    verdicts = read_json(os.path.join(root, "data", "verdicts.json"))
    canon = read_json(os.path.join(root, "data", "canon.json"))
    if not isinstance(verdicts, dict) or not isinstance(verdicts.get("benchmarks"), list):
        raise CanonError("data/verdicts.json must hold an object with a benchmarks list")
    if not isinstance(canon, dict):
        raise CanonError("data/canon.json must hold an object")
    return Data(root, verdicts, canon)


def dump_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


# ---------------------------------------------------------------- validate

def valid_date(text):
    try:
        parse_date(text)
        return True
    except CanonError:
        return False


def last_line(text):
    return text.rstrip("\n").split("\n")[-1]


def validate_data(data):
    """Return a list of problem lines; an empty list means the data is sound."""
    problems = []
    add = problems.append
    verdicts, canon, root = data.verdicts, data.canon, data.root

    if not valid_date(verdicts.get("checked")):
        add("verdicts.json: checked is not a YYYY-MM-DD date: %r" % (verdicts.get("checked"),))
    if not valid_date(canon.get("asof")):
        add("canon.json: asof is not a YYYY-MM-DD date: %r" % (canon.get("asof"),))
    for key in ("note", "produced_by"):
        if not isinstance(canon.get(key), str) or not canon.get(key).strip():
            add("canon.json: %s is missing or empty" % key)
    for key in ("primaries", "rules", "voids", "curators"):
        if not isinstance(canon.get(key), list):
            add("canon.json: %s must be a list" % key)
    if not isinstance(canon.get("labels"), dict):
        add("canon.json: labels must be an object")
    revet = canon.get("revet_months")
    if not isinstance(revet, dict) or not isinstance(revet.get("default"), int):
        add("canon.json: revet_months must be an object with an integer default")

    raw_rows = verdicts.get("benchmarks", [])
    for index, row in enumerate(raw_rows):
        if not isinstance(row, dict):
            add("verdicts.json: benchmark entry %d is not an object" % (index + 1))

    seen_ids = {}
    for row in data.rows:
        rid = row.get("id")
        where = "row %s" % (rid if isinstance(rid, str) else repr(rid))
        if not isinstance(rid, str) or not SLUG.match(rid):
            add("%s: id is not a lowercase slug" % where)
        if isinstance(rid, str):
            if rid in seen_ids:
                add("%s: duplicate id" % where)
            seen_ids[rid] = row
        for key in ("name", "cat"):
            if not isinstance(row.get(key), str) or not row.get(key).strip():
                add("%s: %s is missing or empty" % (where, key))
        if row.get("verdict") not in VERDICT_ORDER:
            add("%s: verdict %r is not canon, caveat or cut" % (where, row.get("verdict")))
        url = row.get("url")
        if not isinstance(url, str) or not re.match(r"^https://[^/\s]+", url):
            add("%s: url is missing or not an https URL" % where)
        if not isinstance(row.get("caveat"), str) or not row.get("caveat").strip():
            add("%s: caveat is empty" % where)
        if "checked" in row and not valid_date(row.get("checked")):
            add("%s: checked is not a YYYY-MM-DD date: %r" % (where, row.get("checked")))
        aliases = row.get("aliases", [])
        if not isinstance(aliases, list) or not all(isinstance(a, str) and a.strip() for a in aliases):
            add("%s: aliases must be a list of non-empty strings" % where)

    # a name or alias must point at one row only
    claims = {}
    for row in data.rows:
        terms = [row.get("name")]
        if isinstance(row.get("aliases"), list):
            terms += row.get("aliases")
        for term in terms:
            if isinstance(term, str) and term.strip():
                owners = claims.setdefault(term.casefold(), [])
                if row.get("id") not in owners:
                    owners.append(row.get("id"))
    for term in sorted(claims):
        if len(claims[term]) > 1:
            add("alias or name %r is claimed by two rows: %s" % (term, ", ".join(str(o) for o in claims[term])))

    # categories, primaries and memos
    cats = []
    for row in data.rows:
        if isinstance(row.get("cat"), str) and row.get("cat") not in cats:
            cats.append(row.get("cat"))
    labels = data.labels()
    for cat in cats:
        if cat not in labels:
            add("category %s has no label in canon.json" % cat)
    primaries = canon.get("primaries") if isinstance(canon.get("primaries"), list) else []
    by_cat = {}
    for prim in primaries:
        if not isinstance(prim, dict):
            add("canon.json: a primaries entry is not an object")
            continue
        cat = prim.get("cat")
        if cat in by_cat:
            add("category %s has two primaries" % cat)
        by_cat[cat] = prim
        for key in ("pick", "pick_id", "rule"):
            if not isinstance(prim.get(key), str) or not prim.get(key).strip():
                add("primary %s: %s is missing or empty" % (cat, key))
        target = seen_ids.get(prim.get("pick_id"))
        if target is None:
            add("primary %s: pick_id %r is not a row" % (cat, prim.get("pick_id")))
        else:
            if target.get("cat") != cat:
                add("primary %s: pick_id %s belongs to category %s" % (cat, prim.get("pick_id"), target.get("cat")))
            if target.get("verdict") == "cut":
                add("primary %s: pick_id %s is a cut row" % (cat, prim.get("pick_id")))
            if target.get("name") != prim.get("pick"):
                add("primary %s: pick does not match the name of %s" % (cat, prim.get("pick_id")))
    for cat in cats:
        if cat not in by_cat:
            add("category %s has no primary" % cat)

    for row in data.rows:
        rid, verdict = row.get("id"), row.get("verdict")
        if not isinstance(rid, str) or not SLUG.match(rid):
            continue
        path = os.path.join(root, "evidence", rid + ".md")
        if not os.path.isfile(path):
            add("row %s: evidence file evidence/%s.md is missing" % (rid, rid))
            continue
        try:
            tail = last_line(read_text(path))
        except CanonError:
            add("row %s: evidence file evidence/%s.md cannot be read" % (rid, rid))
            continue
        if verdict in VERDICT_ORDER and not tail.startswith("VERDICT: " + verdict):
            add("row %s: evidence/%s.md does not end with a VERDICT: %s line" % (rid, rid, verdict))
    for cat in cats:
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", cat):
            add("category %r is not a lowercase slug" % cat)
            continue
        path = os.path.join(root, "memos", cat + ".md")
        if not os.path.isfile(path):
            add("category %s: memo memos/%s.md is missing" % (cat, cat))
            continue
        prim = by_cat.get(cat)
        try:
            tail = last_line(read_text(path))
        except CanonError:
            add("category %s: memo memos/%s.md cannot be read" % (cat, cat))
            continue
        if prim and tail != "PRIMARY: " + str(prim.get("pick")):
            add("category %s: memos/%s.md does not end with PRIMARY: %s" % (cat, cat, prim.get("pick")))
    return problems


# ---------------------------------------------------------------- lookup

def find_rows(data, query):
    """Return (rows, mode) for a cite query: exact match first, then substring."""
    key = query.strip().casefold()
    exact, partial = [], []
    for row in data.ordered_rows():
        terms = [str(row.get("id")), str(row.get("name"))] + [str(a) for a in row.get("aliases", [])]
        folded = [t.casefold() for t in terms]
        if key in folded:
            exact.append(row)
        elif key and any(key in t for t in folded):
            partial.append(row)
    if exact:
        return exact, "exact"
    return partial, "partial"


def cite_line(data, row):
    return "%s (as of %s; caveat: %s) %s" % (row["name"], data.checked_of(row), row["caveat"], row["url"])


def row_view(data, row):
    view = dict(row)
    view["checked"] = data.checked_of(row)
    view["recheck_due"] = data.due_of(row)
    view["evidence"] = data.evidence_of(row)
    return view


def cmd_cite(data, args):
    rows, _mode = find_rows(data, args.name)
    if len(rows) != 1:
        if rows:
            sys.stderr.write("%r matches %d benchmarks; name one of:\n" % (args.name, len(rows)))
            names = [r["name"] for r in rows]
        else:
            sys.stderr.write("no benchmark matches %r\n" % args.name)
            pool = {}
            for row in data.rows:
                for term in [row["name"]] + list(row.get("aliases", [])):
                    pool[term.casefold()] = row["name"]
            close = difflib.get_close_matches(args.name.strip().casefold(), sorted(pool), n=CITE_LIMIT, cutoff=0.4)
            names = []
            for term in close:
                if pool[term] not in names:
                    names.append(pool[term])
            if names:
                sys.stderr.write("closest names:\n")
        for name in names[:CITE_LIMIT]:
            sys.stderr.write("  %s\n" % name)
        return 1
    row = rows[0]
    view = row_view(data, row)
    cut = row["verdict"] == "cut"
    if args.json:
        view["cite_as"] = None if cut else cite_line(data, row)
        view["do_not_cite"] = cut
        print(dump_json(view))
        return 0
    print(row["name"])
    print("verdict: %s" % row["verdict"])
    print("checked: %s" % view["checked"])
    print("re-check due: %s" % view["recheck_due"])
    print("caveat: %s" % row["caveat"])
    print("source: %s" % row["url"])
    print("evidence: %s" % view["evidence"])
    if cut:
        print("do not cite: %s" % row["caveat"])
    else:
        print("cite as: %s" % cite_line(data, row))
    return 0


# ---------------------------------------------------------------- list

def cmd_list(data, args):
    rows = data.ordered_rows()
    if args.cat:
        rows = [r for r in rows if r.get("cat") == args.cat]
    if args.verdict:
        rows = [r for r in rows if r.get("verdict") == args.verdict]
    tally = dict((v, len([r for r in rows if r.get("verdict") == v])) for v in VERDICT_ORDER)
    if args.json:
        print(dump_json({"count": len(rows), "benchmarks": [row_view(data, r) for r in rows]}))
        return 0
    for row in rows:
        print("%-22s %-7s %-11s %s" % (row["id"], row["verdict"], row["cat"], row["name"]))
    print("%d benchmarks (%d canon, %d caveat, %d cut)" % (
        len(rows), tally["canon"], tally["caveat"], tally["cut"]))
    return 0


# ---------------------------------------------------------------- check

def build_matchers(rows):
    """One whole-word, case-ignored pattern per name and alias."""
    matchers = []
    for row in rows:
        seen = set()
        for term in [row["name"]] + list(row.get("aliases", [])):
            if not term.strip() or term.casefold() in seen:
                continue
            seen.add(term.casefold())
            pattern = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)
            matchers.append((pattern, row))
    return matchers


def find_hits(line, matchers):
    """Longest match first, no overlaps; returned in left to right order."""
    found = []
    for pattern, row in matchers:
        for m in pattern.finditer(line):
            found.append((m.start(), m.end(), row))
    found.sort(key=lambda h: (-(h[1] - h[0]), h[0]))
    taken = []
    for start, end, row in found:
        if any(start < t_end and t_start < end for t_start, t_end, _ in taken):
            continue
        taken.append((start, end, row))
    taken.sort(key=lambda h: h[0])
    return [(s, e, r) for s, e, r in taken]


def cmd_check(data, args):
    texts = []
    stdin_text = None
    for name in args.files:
        if name == "-":
            if stdin_text is None:
                try:
                    stdin_text = sys.stdin.read()
                except (OSError, UnicodeDecodeError) as exc:
                    raise CanonError("cannot read standard input: %s" % exc)
            texts.append((name, stdin_text))
        else:
            texts.append((name, read_text(name)))
    matchers = build_matchers(data.rows)
    hits = []
    for name, text in texts:
        for number, line in enumerate(text.split("\n"), 1):
            for start, end, row in find_hits(line, matchers):
                hits.append({
                    "file": name, "line": number, "matched": line[start:end],
                    "id": row["id"], "name": row["name"], "verdict": row["verdict"],
                    "caveat": row["caveat"],
                })
    cut = len([h for h in hits if h["verdict"] == "cut"])
    if args.json:
        print(dump_json({"citations": len(hits), "cut": cut, "hits": hits}))
    else:
        for h in hits:
            print("%s:%d: %s [%s] %s" % (h["file"], h["line"], h["name"], h["verdict"], h["caveat"]))
        print("%d citations, %d cut" % (len(hits), cut))
    return 1 if cut else 0


# ---------------------------------------------------------------- stale

def cmd_stale(data, args):
    today = parse_date(args.today) if args.today else datetime.date.today()
    stale = []
    for row in data.ordered_rows():
        due = data.due_of(row)
        if parse_date(due) <= today:
            stale.append(row)
    total = len(data.rows)
    if args.json:
        print(dump_json({
            "today": today.isoformat(), "total": total, "count": len(stale),
            "stale": [row_view(data, r) for r in stale],
        }))
    else:
        for row in stale:
            print("%s  %s  checked %s  due %s" % (row["name"], row["cat"], data.checked_of(row), data.due_of(row)))
        print("%d of %d past their re-check date" % (len(stale), total))
    return 1 if stale else 0


# ---------------------------------------------------------------- validate

def cmd_validate(data, args):
    problems = validate_data(data)
    if problems:
        for line in problems:
            print(line)
        return 1
    print("ok")
    return 0


# ---------------------------------------------------------------- build: jsonl

def jsonl_rows(data):
    canon = data.canon
    counts = data.counts()
    rows = [{
        "type": "canon-meta",
        "id": "canon-" + canon["asof"],
        "asof": canon["asof"],
        "note": canon["note"],
        "produced_by": canon["produced_by"],
        "counts": counts,
    }]
    for row in data.rows:
        item = {
            "type": "benchmark",
            "id": row["id"], "name": row["name"], "cat": row["cat"], "url": row["url"],
            "verdict": row["verdict"], "caveat": row["caveat"],
            "checked": data.checked_of(row), "recheck_due": data.due_of(row),
            "round": row.get("round"), "aliases": list(row.get("aliases", [])),
            "evidence": data.evidence_of(row),
        }
        rows.append(item)
    for prim in canon["primaries"]:
        rows.append({
            "type": "primary", "id": "primary-" + prim["cat"], "cat": prim["cat"],
            "pick": prim["pick"], "pick_id": prim["pick_id"], "rule": prim["rule"],
        })
    for number, text in enumerate(canon["rules"], 1):
        rows.append({"type": "rule", "id": "rule-%02d" % number, "text": text})
    for number, text in enumerate(canon["voids"], 1):
        rows.append({"type": "void", "id": "void-%d" % number, "text": text})
    for number, cur in enumerate(canon["curators"], 1):
        rows.append({"type": "curator", "id": "curator-%d" % number, "who": cur["who"], "note": cur["note"]})
    return rows


def render_jsonl(data):
    lines = [json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) for r in jsonl_rows(data)]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- build: markdown

def md_text(text):
    """Make data text safe for one Markdown table cell or list item."""
    text = re.sub(r"\s*\n\s*", " ", str(text))
    return text.replace("|", "\\|").replace("<", "\\<")


def md_link(text, url):
    safe = url.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
    return "[%s](%s)" % (md_text(text).replace("[", "\\[").replace("]", "\\]"), safe)


def count_word(n):
    return NUMBER_WORDS.get(n, str(n))


def key_lines(data):
    canon_note = "cite plain. No benchmark has earned it." if data.counts()["canon"] == 0 else "cite plain."
    return [
        "canon: " + canon_note,
        "caveat: cite with the caveat.",
        "cut: do not cite.",
    ]


def render_md(data):
    canon = data.canon
    rows_by_id = dict((r["id"], r) for r in data.rows)
    out = []
    out.append("# The Benchmark Canon")
    out.append("")
    out.append("Checked %s." % canon["asof"])
    out.append(md_text(canon["note"]))
    out.append("")
    for line in key_lines(data):
        out.append("- " + line)
    out.append("")
    out.append("Produced by %s." % md_text(canon["produced_by"]))
    out.append("")
    prims = canon["primaries"]
    out.append("## The %s primaries" % count_word(len(prims)))
    out.append("")
    out.append("| Category | Primary | Rule |")
    out.append("| --- | --- | --- |")
    for prim in prims:
        pick = rows_by_id[prim["pick_id"]]
        out.append("| %s | %s | %s |" % (
            md_text(data.labels()[prim["cat"]]), md_link(prim["pick"], pick["url"]), md_text(prim["rule"])))
    out.append("")
    out.append("## The ledger, by category")
    out.append("")
    ordered = data.ordered_rows()
    for cat in data.category_order():
        group = [r for r in ordered if r.get("cat") == cat]
        if not group:
            continue
        out.append("### " + md_text(data.labels()[cat]))
        out.append("")
        out.append("| Benchmark | Verdict | Caveat | Evidence | Memo |")
        out.append("| --- | --- | --- | --- | --- |")
        for row in group:
            out.append("| %s | %s | %s | [evidence](%s) | [memo](memos/%s.md) |" % (
                md_link(row["name"], row["url"]), row["verdict"], md_text(row["caveat"]),
                data.evidence_of(row), cat))
        out.append("")
    out.append("## Voids nobody measures")
    out.append("")
    for text in canon["voids"]:
        out.append("- " + md_text(text))
    out.append("")
    out.append("## Standing citation rules")
    out.append("")
    for number, text in enumerate(canon["rules"], 1):
        out.append("%d. %s" % (number, md_text(text)))
    out.append("")
    out.append("## Sources this canon leans on")
    out.append("")
    for cur in canon["curators"]:
        out.append("- **%s**: %s" % (md_text(cur["who"]), md_text(cur["note"])))
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- build: html

CSS = """
:root{color-scheme:light dark;--bg:#fbfaf7;--fg:#1d1c1a;--muted:#5c5a55;--rule:#d9d5cc;--card:#f2efe8;--link:#0b5cad;--canon:#1b6b3a;--caveat:#8a5a00;--cut:#a3261b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141412;--fg:#ece9e2;--muted:#a8a49b;--rule:#37352f;--card:#1e1d1a;--link:#7db4f0;--canon:#6fcf8e;--caveat:#e8b04a;--cut:#f08a80}}
:root[data-theme="dark"]{--bg:#141412;--fg:#ece9e2;--muted:#a8a49b;--rule:#37352f;--card:#1e1d1a;--link:#7db4f0;--canon:#6fcf8e;--caveat:#e8b04a;--cut:#f08a80}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:72rem;margin:0 auto;padding:24px 16px 56px}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 .4rem}
h2{font-size:1.35rem;margin:2.4rem 0 .6rem;padding-top:.6rem;border-top:1px solid var(--rule)}
h3{font-size:1.1rem;margin:1.6rem 0 .5rem}
h4,h5{font-size:1rem;margin:1rem 0 .3rem}
a{color:var(--link)}
p,li{overflow-wrap:anywhere}
.lead{color:var(--muted);margin:.2rem 0}
.key{list-style:none;padding:0;margin:1rem 0}
.key li{margin:.2rem 0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:34rem;font-size:.92rem}
th,td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--rule)}
th{background:var(--card);font-weight:600}
.v{font-weight:600}
.v-canon{color:var(--canon)}
.v-caveat{color:var(--caveat)}
.v-cut{color:var(--cut)}
details{margin:.8rem 0;border:1px solid var(--rule);border-radius:6px;background:var(--card)}
summary{cursor:pointer;padding:.55rem .8rem;font-weight:600}
details .memo{padding:0 .9rem .8rem}
ol,ul{padding-left:1.3rem}
@media (max-width:40rem){main{padding:16px}h1{font-size:1.5rem}}
""".strip()


def h(text):
    return html.escape(str(text), quote=True)


def inline_html(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h(text))


def memo_html(text):
    """Convert a category memo (headings, lists, bold, paragraphs) to simple HTML."""
    out = []
    para = []
    items = []
    kind = [None]

    def flush():
        if para:
            out.append("<p>%s</p>" % inline_html(" ".join(para)))
            del para[:]
        if items:
            tag = kind[0]
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline_html(i) for i in items), tag))
            del items[:]
            kind[0] = None

    for line in text.rstrip("\n").split("\n"):
        stripped = line.strip()
        head = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        number = re.match(r"^[0-9]+\.\s+(.*)$", stripped)
        if not stripped:
            flush()
        elif head:
            flush()
            level = min(6, max(4, len(head.group(1)) + 2))
            out.append("<h%d>%s</h%d>" % (level, inline_html(head.group(2)), level))
        elif bullet or number:
            want = "ul" if bullet else "ol"
            if para or kind[0] != want:
                flush()
            kind[0] = want
            items.append((bullet or number).group(1))
        else:
            if items:
                flush()
            para.append(stripped)
    flush()
    return "\n".join(out)


def render_html(data, memos):
    canon = data.canon
    rows_by_id = dict((r["id"], r) for r in data.rows)
    o = []
    o.append("<!doctype html>")
    o.append('<html lang="en">')
    o.append("<head>")
    o.append('<meta charset="utf-8">')
    o.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    o.append('<meta name="color-scheme" content="light dark">')
    o.append("<title>The Benchmark Canon</title>")
    o.append("<style>")
    o.append(CSS)
    o.append("</style>")
    o.append("</head>")
    o.append("<body>")
    o.append("<main>")
    o.append("<h1>The Benchmark Canon</h1>")
    o.append('<p class="lead">Checked %s.</p>' % h(canon["asof"]))
    o.append('<p class="lead">%s</p>' % h(canon["note"]))
    o.append('<ul class="key">')
    for line in key_lines(data):
        word, rest = line.split(": ", 1)
        o.append('<li><span class="v v-%s">%s</span>: %s</li>' % (h(word), h(word), h(rest)))
    o.append("</ul>")
    o.append('<p class="lead">Produced by %s.</p>' % h(canon["produced_by"]))
    prims = canon["primaries"]
    o.append("<h2>The %s primaries</h2>" % h(count_word(len(prims))))
    o.append('<div class="scroll"><table>')
    o.append("<thead><tr><th>Category</th><th>Primary</th><th>Rule</th></tr></thead>")
    o.append("<tbody>")
    for prim in prims:
        pick = rows_by_id[prim["pick_id"]]
        o.append('<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (
            h(data.labels()[prim["cat"]]), h(pick["url"]), h(prim["pick"]), h(prim["rule"])))
    o.append("</tbody></table></div>")
    o.append("<h2>The ledger, by category</h2>")
    ordered = data.ordered_rows()
    for cat in data.category_order():
        group = [r for r in ordered if r.get("cat") == cat]
        if not group:
            continue
        label = data.labels()[cat]
        o.append('<h3 id="cat-%s">%s</h3>' % (h(cat), h(label)))
        o.append('<div class="scroll"><table>')
        o.append("<thead><tr><th>Benchmark</th><th>Verdict</th><th>Caveat</th><th>Evidence</th></tr></thead>")
        o.append("<tbody>")
        for row in group:
            o.append(
                '<tr id="row-%s"><td><a href="%s">%s</a></td><td><span class="v v-%s">%s</span></td>'
                '<td>%s</td><td><a href="%s">evidence</a></td></tr>' % (
                    h(row["id"]), h(row["url"]), h(row["name"]), h(row["verdict"]), h(row["verdict"]),
                    h(row["caveat"]), h(data.evidence_of(row))))
        o.append("</tbody></table></div>")
        o.append('<details class="memo-box"><summary>Judge memo: %s</summary>' % h(label))
        o.append('<div class="memo">')
        o.append(memo_html(memos[cat]))
        o.append("</div></details>")
    o.append("<h2>Voids nobody measures</h2>")
    o.append("<ul>")
    for text in canon["voids"]:
        o.append("<li>%s</li>" % h(text))
    o.append("</ul>")
    o.append("<h2>Standing citation rules</h2>")
    o.append("<ol>")
    for text in canon["rules"]:
        o.append("<li>%s</li>" % h(text))
    o.append("</ol>")
    o.append("<h2>Sources this canon leans on</h2>")
    o.append("<ul>")
    for cur in canon["curators"]:
        o.append("<li><strong>%s</strong>: %s</li>" % (h(cur["who"]), h(cur["note"])))
    o.append("</ul>")
    o.append("</main>")
    o.append("</body>")
    o.append("</html>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- build

def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def cmd_build(data, args):
    problems = validate_data(data)
    if problems:
        for line in problems:
            sys.stderr.write(line + "\n")
        sys.stderr.write("build refused: %d problems, nothing written\n" % len(problems))
        return 1
    memos = {}
    for cat in data.category_order():
        if any(r.get("cat") == cat for r in data.rows):
            memos[cat] = read_text(os.path.join(data.root, "memos", cat + ".md"))
    out_dir = args.out or data.root
    jsonl = render_jsonl(data)
    markdown = render_md(data)
    page = render_html(data, memos)
    try:
        os.makedirs(out_dir, exist_ok=True)
        write_text(os.path.join(out_dir, "canon.jsonl"), jsonl)
        write_text(os.path.join(out_dir, "CANON.md"), markdown)
        write_text(os.path.join(out_dir, "index.html"), page)
    except OSError as exc:
        raise CanonError("cannot write to %s: %s" % (out_dir, exc.strerror or exc))
    counts = data.counts()
    print("wrote 3 files: %d rows, %d benchmarks (%d caveat, %d cut)" % (
        len(jsonl.splitlines()), counts["benchmarks"], counts["caveat"], counts["cut"]))
    return 0


# ---------------------------------------------------------------- command line

class OneLineParser(argparse.ArgumentParser):
    """An argument parser whose usage errors are one stderr line with exit code 2."""

    def error(self, message):
        sys.stderr.write("canon.py: error: %s\n" % message)
        raise SystemExit(2)


def make_parser():
    parser = OneLineParser(prog="canon.py", description="Look up, check and rebuild the benchmark canon.")
    parser.add_argument("--root", help="folder that holds data/, evidence/ and memos/ (default: this file's folder)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    p = sub.add_parser("list", help="one line per benchmark")
    p.add_argument("--cat", help="only this category id")
    p.add_argument("--verdict", choices=VERDICT_ORDER, help="only this verdict")
    p.add_argument("--json", action="store_true", help="print JSON")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("cite", help="print one benchmark's verdict and a citation line")
    p.add_argument("name", help="id, name or alias (case ignored; a unique part also works)")
    p.add_argument("--json", action="store_true", help="print JSON")
    p.set_defaults(func=cmd_cite)

    p = sub.add_parser("check", help="find benchmark names in text files")
    p.add_argument("files", nargs="+", metavar="FILE", help="a file to read; - reads standard input")
    p.add_argument("--json", action="store_true", help="print JSON")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("stale", help="list rows whose re-check date has arrived")
    p.add_argument("--today", help="the day to compare against, YYYY-MM-DD (default: today)")
    p.add_argument("--json", action="store_true", help="print JSON")
    p.set_defaults(func=cmd_stale)

    p = sub.add_parser("validate", help="check the data files for problems")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("build", help="write canon.jsonl, CANON.md and index.html")
    p.add_argument("--out", help="folder to write into (default: the root)")
    p.set_defaults(func=cmd_build)
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root) if args.root else DEFAULT_ROOT
    try:
        data = load(root)
        return args.func(data, args)
    except CanonError as exc:
        sys.stderr.write("canon.py: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
