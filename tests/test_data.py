"""Checks on the shipped data files, evidence files and memos."""
import os
import re
import tempfile
import unittest
from urllib.parse import urlsplit

from canon_testlib import REPO, read, real_canon, real_rows, run

EM = "\u2014"
EN = "\u2013"
NOTE = ("The refuter round checked 51 (47 with a caveat, 4 cut); "
        "Deep SWE was vetted separately and also carries a caveat")
PRODUCED_BY = ("AI agents (Claude) with web access: one refuter per benchmark, "
               "one judge per category")
CATS = ["composite", "chat-model", "coding", "agentic", "search", "image", "video",
        "voice", "docs", "safety", "aggregator"]


OS_FILES = re.compile(r"\.DS_Store|\._.*|Thumbs\.db|desktop\.ini")


def is_os_file(name):
    """A file the operating system leaves in a folder (Finder, Explorer); git never ships it."""
    return OS_FILES.fullmatch(name) is not None


def listed(*parts):
    """The sorted names in a folder of the repository, without operating system files."""
    return sorted(n for n in os.listdir(os.path.join(REPO, *parts)) if not is_os_file(n))


def published_text_files(root=REPO):
    """Every file the repository ships. Hidden folders (.git, .venv, tool caches), __pycache__
    and operating system files are not published, so they are left out."""
    found = []
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs
                   if not d.startswith(".") and d != "__pycache__"]
        for name in names:
            if name.endswith(".pyc") or is_os_file(name):
                continue
            found.append(os.path.join(base, name))
    return sorted(found)


class RowsTest(unittest.TestCase):
    def test_counts(self):
        rows = real_rows()
        self.assertEqual(len(rows), 52)
        self.assertEqual(len([r for r in rows if r["verdict"] == "caveat"]), 48)
        self.assertEqual(len([r for r in rows if r["verdict"] == "cut"]), 4)
        self.assertEqual(len([r for r in rows if r["verdict"] == "canon"]), 0)

    def test_cut_rows_are_the_four_named(self):
        cut = sorted(r["id"] for r in real_rows() if r["verdict"] == "cut")
        self.assertEqual(cut, ["freshqa", "gaia", "swe-bench-pro", "swe-bench-verified"])

    def test_rounds_and_order(self):
        rows = real_rows()
        self.assertEqual(rows[-1]["id"], "deep-swe")
        self.assertEqual(rows[-1]["round"], "standalone")
        self.assertEqual(len([r for r in rows if r["round"] == "main"]), 51)
        self.assertEqual(rows[0]["id"], "aa-index")

    def test_ids_unique_and_slugs(self):
        ids = [r["id"] for r in real_rows()]
        self.assertEqual(len(ids), len(set(ids)))
        for rid in ids:
            self.assertRegex(rid, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_urls_are_https(self):
        for row in real_rows():
            self.assertTrue(row["url"].startswith("https://"), row["id"])

    def test_no_row_cites_a_discovery_only_aggregator(self):
        """Rule 1 names the aggregators that are for discovery only, and `cite` prints a row's url,
        so a row outside the aggregator category must link to its primary source instead."""
        rule = real_canon()["rules"][0]
        names = re.search(r"\(([^)]*) class\)", rule).group(1).split(" / ")
        self.assertEqual(names, ["benchlm", "llm-stats", "localaimaster"])
        for row in real_rows():
            if row["cat"] == "aggregator":
                continue
            host = urlsplit(row["url"]).hostname
            for name in names:
                self.assertNotIn(name, host, row["id"])

    def test_fields_present(self):
        for row in real_rows():
            for key in ("id", "name", "cat", "url", "verdict", "caveat", "round", "aliases"):
                self.assertIn(key, row)
            self.assertTrue(row["caveat"].strip(), row["id"])
            self.assertIsInstance(row["aliases"], list)

    def test_categories(self):
        self.assertEqual(sorted(set(r["cat"] for r in real_rows())), sorted(CATS))

    def test_aliases_are_unique_across_rows(self):
        seen = {}
        names = set(r["name"].casefold() for r in real_rows())
        for row in real_rows():
            for alias in row["aliases"]:
                self.assertNotIn(alias.casefold(), seen, alias)
                self.assertNotIn(alias.casefold(), names, alias)
                seen[alias.casefold()] = row["id"]


class CanonTest(unittest.TestCase):
    def test_shape(self):
        canon = real_canon()
        self.assertEqual(canon["asof"], "2026-07-17")
        self.assertEqual(canon["note"], NOTE)
        self.assertEqual(canon["produced_by"], PRODUCED_BY)
        self.assertEqual(len(canon["primaries"]), 11)
        self.assertEqual(len(canon["rules"]), 11)
        self.assertEqual(len(canon["voids"]), 6)
        self.assertEqual(len(canon["curators"]), 8)
        self.assertEqual(len(canon["labels"]), 11)
        self.assertEqual(canon["revet_months"], {"coding": 3, "default": 6})
        for cur in canon["curators"]:
            self.assertTrue(cur["who"].strip())
            self.assertTrue(cur["note"].strip())

    def test_labels_cover_the_categories(self):
        self.assertEqual(sorted(real_canon()["labels"]), sorted(CATS))
        self.assertEqual(real_canon()["labels"]["coding"], "Coding + software agents")

    def test_primaries_point_at_good_rows(self):
        rows = dict((r["id"], r) for r in real_rows())
        cats = []
        for prim in real_canon()["primaries"]:
            cats.append(prim["cat"])
            row = rows[prim["pick_id"]]
            self.assertEqual(row["cat"], prim["cat"])
            self.assertNotEqual(row["verdict"], "cut")
            self.assertEqual(row["name"], prim["pick"])
            self.assertTrue(prim["rule"].strip())
        self.assertEqual(cats, ["composite", "chat-model", "coding", "agentic", "search",
                                "aggregator", "image", "video", "voice", "docs", "safety"])

    def test_the_harness_rule_and_its_curator(self):
        canon = real_canon()
        self.assertEqual(
            canon["rules"][2],
            "NAME THE HARNESS on any agent or coding score: on Terminal-Bench the same model "
            "scored 58% in one harness and 75 to 82% in others (Theo Browne, t3.gg, "
            "\"Did Claude really get dumber again?\", 2026-04-20, "
            "https://www.youtube.com/watch?v=KFisvc-AMII).")
        theo = [c for c in canon["curators"] if c["who"].startswith("Theo Browne")]
        self.assertEqual(len(theo), 1)
        self.assertEqual(
            theo[0]["note"],
            "usage-grounded commentary; the name-the-harness rule follows his Terminal-Bench comparison")


class EvidenceTest(unittest.TestCase):
    def test_every_row_has_evidence_ending_in_its_verdict(self):
        files = listed("evidence")
        self.assertEqual(len(files), 52)
        for row in real_rows():
            text = read(os.path.join(REPO, "evidence", row["id"] + ".md"))
            self.assertTrue(text.endswith("\n"), row["id"])
            self.assertFalse(text.endswith("\n\n"), row["id"])
            last = text.rstrip("\n").split("\n")[-1]
            self.assertTrue(last.startswith("VERDICT: " + row["verdict"]), row["id"])
            self.assertTrue(last.endswith(row["caveat"]), row["id"])

    def test_main_round_verdict_line_is_exact(self):
        for row in real_rows():
            if row["round"] != "main":
                continue
            text = read(os.path.join(REPO, "evidence", row["id"] + ".md"))
            want = "VERDICT: %s | %s | %s" % (row["verdict"], row["name"], row["caveat"])
            self.assertEqual(text.rstrip("\n").split("\n")[-1], want, row["id"])

    def test_evidence_wording(self):
        deep = read(os.path.join(REPO, "evidence", "deep-swe.md"))
        self.assertIn("same five-lens protocol as the main round", deep)
        self.assertIn("a Google address", read(os.path.join(REPO, "evidence", "freshqa.md")))
        aa = read(os.path.join(REPO, "evidence", "aa-index.md"))
        self.assertTrue(aa.startswith("**Funding/ownership"))
        self.assertIn("the URL this row cites", read(os.path.join(REPO, "evidence", "webarena-verified.md")))


class MemoTest(unittest.TestCase):
    def test_every_category_has_a_memo_ending_in_its_primary(self):
        files = listed("memos")
        self.assertEqual(files, sorted(c + ".md" for c in CATS))
        for prim in real_canon()["primaries"]:
            text = read(os.path.join(REPO, "memos", prim["cat"] + ".md"))
            self.assertTrue(text.endswith("\n") and not text.endswith("\n\n"), prim["cat"])
            self.assertEqual(text.rstrip("\n").split("\n")[-1], "PRIMARY: " + prim["pick"])

    def test_memo_headings(self):
        composite = read(os.path.join(REPO, "memos", "composite.md"))
        self.assertIn("LM Council defer to it", composite)
        self.assertTrue(composite.startswith("**1. Ranked KEEP list"))
        self.assertTrue(read(os.path.join(REPO, "memos", "agentic.md")).startswith("## KEEP list"))
        self.assertIn("### Cut\n", read(os.path.join(REPO, "memos", "coding.md")))
        self.assertIn("**3. Flags**", composite)


class PublishedTextTest(unittest.TestCase):
    def test_no_em_or_en_dash_anywhere(self):
        for path in published_text_files():
            text = read(path)
            self.assertNotIn(EM, text, path)
            self.assertNotIn(EN, text, path)

    def test_theo_appears_twice_as_theo_browne(self):
        total = 0
        for path in published_text_files():
            if path.startswith(os.path.join(REPO, "tests")):
                continue
            text = read(path)
            for match in re.finditer(r"Theo", text):
                total += 1
                self.assertEqual(text[match.start():match.start() + 11], "Theo Browne", path)
        # data/canon.json (rule and curator row) and the two builds that repeat them are
        # counted below; the data files alone hold exactly two
        data = read(os.path.join(REPO, "data", "canon.json"))
        self.assertEqual(len(re.findall(r"Theo", data)), 2)
        self.assertEqual(len(re.findall(r"Theo", read(os.path.join(REPO, "data", "verdicts.json")))), 0)
        for sub in ("evidence", "memos"):
            for name in listed(sub):
                self.assertNotIn("Theo", read(os.path.join(REPO, sub, name)), name)
        self.assertGreaterEqual(total, 2)

    def test_no_email_address_or_home_path(self):
        for path in published_text_files():
            text = read(path)
            if os.path.basename(path) == "LICENSE":
                continue
            self.assertIsNone(re.search(r"[\w.+-]+@[\w-]+\.[A-Za-z][\w.-]*", text), path)
            self.assertNotIn("/Us" + "ers/", text, path)


class PublishedFilesTest(unittest.TestCase):
    # source: a binary .DS_Store, which Finder writes into a folder it opens, made five tests
    # error or fail
    def test_operating_system_files_are_recognised(self):
        for name in (".DS_Store", "._a.md", "Thumbs.db", "desktop.ini"):
            self.assertTrue(is_os_file(name), name)
        for name in ("a.md", ".gitignore", "x.DS_Store.md", "LICENSE"):
            self.assertFalse(is_os_file(name), name)

    def test_finder_files_and_hidden_folders_are_left_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            for rel, data in (("a.md", b"text\n"), (".gitignore", b"*.pyc\n"),
                              (".DS_Store", b"\x00\x00\x00\x01Bud1\xff"),
                              ("._a.md", b"\x00\x05\x16\x07\xff"), ("sub/.DS_Store", b"\xff"),
                              ("sub/b.md", b"text\n"), (".venv/lib.txt", b"x\n")):
                path = os.path.join(tmp, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(data)
            got = [os.path.relpath(p, tmp) for p in published_text_files(tmp)]
            self.assertEqual(got, [".gitignore", "a.md", os.path.join("sub", "b.md")])


class ValidateRealTest(unittest.TestCase):
    def test_validate_passes(self):
        self.assertEqual(run(["validate"]), (0, "ok\n", ""))


if __name__ == "__main__":
    unittest.main()
