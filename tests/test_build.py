"""Checks on `canon.py build` and the three files it writes."""
import html
import json
import os
import re
import unittest

from canon_testlib import (REPO, TempDirMixin, copy_real_root, edit_json, load_json, make_mini,
                           read, real_canon, real_rows, run)

OUTPUTS = ("canon.jsonl", "CANON.md", "index.html")
SUMMARY = "wrote 3 files: 89 rows, 52 benchmarks (48 caveat, 4 cut)\n"


class BuildOutputTest(TempDirMixin, unittest.TestCase):
    def build_into(self, name):
        out = os.path.join(self.make_tmp(), name)
        code, stdout, stderr = run(["build", "--out", out])
        self.assertEqual((code, stderr), (0, ""))
        return out, stdout

    def test_summary_line(self):
        _out, stdout = self.build_into("a")
        self.assertEqual(stdout, SUMMARY)

    def test_two_builds_are_byte_identical(self):
        first, _ = self.build_into("a")
        second, _ = self.build_into("b")
        for name in OUTPUTS:
            with open(os.path.join(first, name), "rb") as a, open(os.path.join(second, name), "rb") as b:
                self.assertEqual(a.read(), b.read(), name)

    def test_committed_files_match_a_fresh_build(self):
        fresh, _ = self.build_into("fresh")
        for name in OUTPUTS:
            with open(os.path.join(fresh, name), "rb") as a, open(os.path.join(REPO, name), "rb") as b:
                self.assertEqual(a.read(), b.read(), name + " is out of date; run python3 canon.py build")


class JsonlTest(unittest.TestCase):
    def setUp(self):
        text = read(os.path.join(REPO, "canon.jsonl"))
        self.assertTrue(text.endswith("\n"))
        self.lines = text.rstrip("\n").split("\n")
        self.rows = [json.loads(line) for line in self.lines]

    def test_row_counts(self):
        self.assertEqual(len(self.rows), 89)
        kinds = {}
        for row in self.rows:
            kinds[row["type"]] = kinds.get(row["type"], 0) + 1
        self.assertEqual(kinds, {"canon-meta": 1, "benchmark": 52, "primary": 11,
                                 "rule": 11, "void": 6, "curator": 8})

    def test_meta_row_first(self):
        meta = self.rows[0]
        self.assertEqual(meta["type"], "canon-meta")
        self.assertEqual(meta["id"], "canon-2026-07-17")
        self.assertEqual(meta["asof"], "2026-07-17")
        self.assertEqual(meta["note"], real_canon()["note"])
        self.assertEqual(meta["produced_by"], real_canon()["produced_by"])
        self.assertEqual(meta["counts"], {"benchmarks": 52, "canon": 0, "caveat": 48, "cut": 4})

    def test_keys_sorted_and_ids_unique(self):
        for line, row in zip(self.lines, self.rows):
            self.assertEqual(line, json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
        ids = [r["id"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_row_ids_and_fields(self):
        ids = [r["id"] for r in self.rows]
        for expected in ("primary-coding", "rule-01", "rule-11", "void-1", "void-6", "curator-1", "curator-8"):
            self.assertIn(expected, ids)
        bench = [r for r in self.rows if r["type"] == "benchmark"]
        self.assertEqual([b["id"] for b in bench], [r["id"] for r in real_rows()])
        by_id = dict((b["id"], b) for b in bench)
        self.assertEqual(by_id["terminal-bench"]["recheck_due"], "2026-10-17")
        self.assertEqual(by_id["livebench"]["recheck_due"], "2027-01-17")
        self.assertEqual(by_id["gaia"]["evidence"], "evidence/gaia.md")
        for key in ("id", "name", "cat", "url", "verdict", "caveat", "checked", "recheck_due",
                    "round", "aliases", "evidence"):
            self.assertIn(key, by_id["gaia"])


class MarkdownTest(unittest.TestCase):
    def setUp(self):
        self.md = read(os.path.join(REPO, "CANON.md"))

    def test_every_name_appears(self):
        for row in real_rows():
            self.assertIn(row["name"], self.md)

    def test_date_and_note_sit_above_the_first_table(self):
        lines = self.md.split("\n")
        self.assertEqual(lines[0], "# The Benchmark Canon")
        self.assertEqual(lines[2], "Checked 2026-07-17.")
        self.assertEqual(lines[3], real_canon()["note"])
        self.assertLess(self.md.index("Checked 2026-07-17."), self.md.index("| Category |"))
        self.assertLess(self.md.index(real_canon()["note"]), self.md.index("| Category |"))

    def test_sections_in_order(self):
        heads = [l for l in self.md.split("\n") if l.startswith("## ")]
        self.assertEqual(heads, ["## The eleven primaries", "## The ledger, by category",
                                 "## Voids nobody measures", "## Standing citation rules",
                                 "## Sources this canon leans on"])

    def test_key_lines(self):
        for word in ("canon: cite plain", "caveat: cite with the caveat", "cut: do not cite"):
            self.assertIn("- " + word, self.md)

    def test_one_ledger_table_per_category(self):
        self.assertEqual(self.md.count("\n### "), 11)
        self.assertEqual(len(re.findall(r"^\| \[", self.md, re.M)), 52)

    def test_angle_bracket_text_is_kept_visible(self):
        self.assertIn("\\<date>", self.md)


class HtmlTest(unittest.TestCase):
    def setUp(self):
        self.page = read(os.path.join(REPO, "index.html"))

    def test_every_name_appears_escaped(self):
        for row in real_rows():
            self.assertIn(html.escape(row["name"], quote=True), self.page)

    def test_no_script_or_remote_references(self):
        lowered = self.page.lower()
        for bad in ("<script", "src=", "<link", "@import", "url(", "http-equiv"):
            self.assertNotIn(bad, lowered)

    def test_self_contained_and_phone_ready(self):
        self.assertTrue(self.page.startswith("<!doctype html>"))
        self.assertIn('name="viewport"', self.page)
        self.assertIn("prefers-color-scheme:dark", self.page)
        self.assertEqual(self.page.count("<style>"), 1)
        hrefs = re.findall(r'href="([^"]*)"', self.page)
        for href in hrefs:
            self.assertTrue(href.startswith("https://") or href.startswith("evidence/"), href)

    def test_each_memo_is_a_closed_details_block(self):
        self.assertEqual(self.page.count("<details"), 11)
        self.assertEqual(self.page.count("</details>"), 11)
        for tag in re.findall(r"<details[^>]*>", self.page):
            self.assertNotIn("open", tag)
        self.assertIn("<summary>Judge memo: Coding + software agents</summary>", self.page)
        self.assertIn("PRIMARY: Terminal-Bench 2.x", self.page)

    def test_date_and_note_above_first_table(self):
        self.assertLess(self.page.index("Checked 2026-07-17."), self.page.index("<table>"))
        self.assertLess(self.page.index(html.escape(real_canon()["note"], quote=True)), self.page.index("<table>"))

    def test_angle_bracket_rule_text_is_escaped(self):
        self.assertIn("&lt;date&gt;", self.page)
        self.assertNotIn("<date>", self.page)

    def test_sections_in_order(self):
        order = ["The eleven primaries", "The ledger, by category", "Voids nobody measures",
                 "Standing citation rules", "Sources this canon leans on"]
        spots = [self.page.index("<h2>" + name + "</h2>") for name in order]
        self.assertEqual(spots, sorted(spots))


class EscapingTest(TempDirMixin, unittest.TestCase):
    NAME = '<b>X</b> & "Y"'

    def test_names_and_bars_are_escaped(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)

        def tweak(doc):
            doc["benchmarks"][0]["name"] = self.NAME
            doc["benchmarks"][0]["caveat"] = "left | right\nsecond line"
        edit_json(root, "data/verdicts.json", tweak)
        edit_json(root, "data/canon.json", lambda c: c["primaries"][0].update(pick=self.NAME))
        for name in ("one",):
            path = os.path.join(root, "evidence", name + ".md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("x\n\nVERDICT: caveat | n | c\n")
        with open(os.path.join(root, "memos", "alpha.md"), "w", encoding="utf-8") as fh:
            fh.write("A <b>memo</b> & more\n\nPRIMARY: %s\n" % self.NAME)
        out = os.path.join(tmp, "out")
        code, stdout, stderr = run(["build", "--out", out], root=root)
        self.assertEqual((code, stderr), (0, ""))
        page = read(os.path.join(out, "index.html"))
        self.assertIn("&lt;b&gt;X&lt;/b&gt; &amp; &quot;Y&quot;", page)
        self.assertNotIn("<b>X</b>", page)
        self.assertNotIn("<b>memo</b>", page)
        self.assertIn("A &lt;b&gt;memo&lt;/b&gt; &amp; more", page)
        self.assertIn("left | right\nsecond line", page)  # a newline is plain white space in HTML
        md = read(os.path.join(out, "CANON.md"))
        self.assertIn("left \\| right second line", md)
        for line in md.split("\n"):
            if line.startswith("| [") and "left" in line:
                cells = re.split(r"(?<!\\)\|", line.strip())
                self.assertEqual(len(cells), 7, line)  # empty edge cells plus five columns

    def test_build_counts_follow_the_data(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)
        out = os.path.join(tmp, "out")
        code, stdout, _ = run(["build", "--out", out], root=root)
        self.assertEqual(code, 0)
        self.assertEqual(stdout, "wrote 3 files: %d rows, 4 benchmarks (3 caveat, 1 cut)\n" % (1 + 4 + 2 + 2 + 1 + 1))


class RefusalTest(TempDirMixin, unittest.TestCase):
    def test_build_refuses_when_validate_fails(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)
        os.remove(os.path.join(root, "evidence", "one.md"))
        out = os.path.join(tmp, "out")
        code, stdout, stderr = run(["build", "--out", out], root=root)
        self.assertEqual(code, 1)
        self.assertIn("evidence/one.md is missing", stderr)
        self.assertEqual(stdout, "")
        self.assertFalse(os.path.exists(out) and os.listdir(out))
        self.assertEqual([n for n in OUTPUTS if os.path.exists(os.path.join(root, n))], [])

    def test_build_default_writes_into_the_root(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)
        code, _, _ = run(["build"], root=root)
        self.assertEqual(code, 0)
        for name in OUTPUTS:
            self.assertTrue(os.path.isfile(os.path.join(root, name)), name)


class RealRootCopyTest(TempDirMixin, unittest.TestCase):
    def test_a_copied_root_builds_the_same_bytes(self):
        tmp = self.make_tmp()
        root = copy_real_root(tmp)
        code, stdout, _ = run(["build"], root=root)
        self.assertEqual((code, stdout), (0, SUMMARY))
        for name in OUTPUTS:
            self.assertEqual(read(os.path.join(root, name)), read(os.path.join(REPO, name)), name)
        self.assertEqual(load_json(root, "data/canon.json")["asof"], "2026-07-17")


if __name__ == "__main__":
    unittest.main()
