"""Mutation check for canon.py.

Each mutation is an exact text replacement in a copy of canon.py. For every one the
script copies the repository into a fresh temporary folder, writes the mutated
canon.py there, runs the whole test suite in the copy and prints "killed" when the
suite fails (or runs out of time) and "survived" when it still passes. The exit code
is 1 when any mutation survives and 0 when all are killed.

Run it from anywhere: python3 tests/mutate.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TIMEOUT = 60
SKIP = (".git", "__pycache__")

# (name, [(before, after), ...]); each "before" must occur exactly once in canon.py
MUTATIONS = [
    ("cite ignores aliases",
     [('+ [str(a) for a in row.get("aliases", [])]\n        folded', '\n        folded')]),
    ("cite compares case",
     [('key = query.strip().casefold()', 'key = query.strip()'),
      ('folded = [t.casefold() for t in terms]', 'folded = terms')]),
    ("cite prints a cite-as line for a cut row",
     [('    if cut:\n        print("do not cite', '    if False:\n        print("do not cite')]),
    ("check exits 0 on a cut hit",
     [('return 1 if cut else 0', 'return 0')]),
    ("check drops the whole-word rule",
     [('r"(?<!\\w)" + re.escape(term) + r"(?!\\w)"', 're.escape(term)')]),
    ("check takes the shorter match",
     [('(-(h[1] - h[0]), h[0])', '((h[1] - h[0]), h[0])')]),
    ("check is case sensitive",
     [('re.escape(term) + r"(?!\\w)", re.IGNORECASE)', 're.escape(term) + r"(?!\\w)")')]),
    ("stale uses six months for coding",
     [('months = revet.get(cat, revet.get("default", 6))', 'months = revet.get("default", 6)')]),
    ("stale uses before instead of on or before",
     [('if parse_date(due) <= today:', 'if parse_date(due) < today:')]),
    ("stale exits 0 when rows are due",
     [('return 1 if stale else 0', 'return 0')]),
    ("month sum breaks at year end",
     [('year, month = divmod(index, 12)', 'year, month = day.year, (day.month - 1 + months) % 12')]),
    ("day of month is not clamped",
     [('min(day.day, last)', 'day.day')]),
    ("list ignores the category filter",
     [('rows = [r for r in rows if r.get("cat") == args.cat]', 'rows = rows')]),
    ("build skips HTML escaping",
     [('return html.escape(str(text), quote=True)', 'return str(text)')]),
    ("build skips the bar escape",
     [('return text.replace("|", "\\\\|").replace("<", "\\\\<")', 'return text.replace("<", "\\\\<")')]),
    ("build drops the note from the Markdown",
     [('    out.append(md_text(canon["note"]))\n', '    pass\n')]),
    ("build drops the note from the page",
     [('''    o.append('<p class="lead">%s</p>' % h(canon["note"]))\n''', '    pass\n')]),
    ("build writes despite a validate failure",
     [('nothing written\\n" % len(problems))\n        return 1', 'nothing written\\n" % len(problems))')]),
    ("build writes keys unsorted",
     [('json.dumps(r, sort_keys=True', 'json.dumps(r, sort_keys=False')]),
    ("validate skips the duplicate id check",
     [('if rid in seen_ids:', 'if False:')]),
    ("validate skips the two-rows-one-alias check",
     [('if len(claims[term]) > 1:', 'if len(claims[term]) > 99:')]),
    ("validate skips the cut primary check",
     [('if target.get("verdict") == "cut":', 'if False:')]),
    ("validate skips the evidence verdict line check",
     [('if verdict in VERDICT_ORDER and not tail.startswith("VERDICT: " + verdict):', 'if False:')]),
    ("validate skips the missing evidence check",
     [('add("row %s: evidence file evidence/%s.md is missing" % (rid, rid))', 'pass')]),
    ("validate skips the memo PRIMARY line check",
     [('if prim and tail != "PRIMARY: " + str(prim.get("pick")):', 'if False:')]),
    ("validate accepts a non-https url",
     [('or not re.match(r"^https://[^/\\s]+", url):', ':')]),
]


def copy_repo(dest):
    def ignore(_folder, names):
        return [n for n in names if n in SKIP or n.endswith(".pyc")]
    shutil.copytree(REPO, dest, ignore=ignore)


def run_suite(folder):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        done = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=folder, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None
    return done.returncode


def main():
    with open(os.path.join(REPO, "canon.py"), encoding="utf-8", newline="") as fh:
        original = fh.read()
    work = tempfile.mkdtemp(prefix="canon-mutate-")
    survived = []
    try:
        base = os.path.join(work, "baseline")
        copy_repo(base)
        if run_suite(base) != 0:
            print("baseline: the unmodified suite does not pass; fix that first")
            return 1
        print("baseline: pass")
        for number, (name, edits) in enumerate(MUTATIONS, 1):
            text = original
            for before, after in edits:
                if text.count(before) != 1:
                    print("%-2d %s: ERROR, the text to replace occurs %d times" % (number, name, text.count(before)))
                    return 1
                text = text.replace(before, after)
            if text == original:
                print("%-2d %s: ERROR, the mutation changed nothing" % (number, name))
                return 1
            folder = os.path.join(work, "m%02d" % number)
            copy_repo(folder)
            with open(os.path.join(folder, "canon.py"), "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
            code = run_suite(folder)
            result = "killed" if code != 0 else "survived"
            if code == 0:
                survived.append(name)
            print("%-2d %s: %s%s" % (number, name, result, " (timeout)" if code is None else ""))
            shutil.rmtree(folder, True)
    finally:
        shutil.rmtree(work, True)
    print("%d mutations, %d killed, %d survived" % (len(MUTATIONS), len(MUTATIONS) - len(survived), len(survived)))
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
