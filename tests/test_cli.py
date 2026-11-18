"""Checks on the command line: cite, list, check, stale and validate."""
import json
import os
import subprocess
import sys
import unittest

from canon_testlib import (REPO, TempDirMixin, edit_json, load_json, make_mini, read, real_rows,
                           run, write)

CODING = [r for r in real_rows() if r["cat"] == "coding"]


class CiteTest(TempDirMixin, unittest.TestCase):
    def test_by_id_name_alias_and_other_case(self):
        outputs = []
        for query in ("livebench", "LiveBench", "LIVEBENCH", "  livebench "):
            code, out, err = run(["cite", query])
            self.assertEqual((code, err), (0, ""), query)
            outputs.append(out)
        self.assertEqual(len(set(outputs)), 1)
        code, out, _ = run(["cite", "hal"])
        self.assertEqual(code, 0)
        self.assertEqual(out.split("\n")[0], "HAL (Holistic Agent Leaderboard)")
        code, out2, _ = run(["cite", "Holistic Agent Leaderboard"])
        self.assertEqual((code, out2), (0, out))

    def test_alias_that_is_not_part_of_the_name(self):
        root = make_mini(self.make_tmp())
        for query in ("A1", "a1"):
            code, out, err = run(["cite", query], root=root)
            self.assertEqual((code, err), (0, ""))
            self.assertEqual(out.split("\n")[0], "Alpha One")

    def test_caveat_row_output(self):
        code, out, err = run(["cite", "livebench"])
        lines = out.split("\n")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(lines[:7], [
            "LiveBench", "verdict: caveat", "checked: 2026-07-17", "re-check due: 2027-01-17",
            "caveat: Live, objective, no-LLM-judge scoring at the source; single-vendor funder, "
            "no COI disclosure; cite livebench.ai directly, not stale mirrors.",
            "source: https://livebench.ai/", "evidence: evidence/livebench.md"])
        self.assertEqual(lines[7],
                         "cite as: LiveBench (as of 2026-07-17; caveat: Live, objective, no-LLM-judge "
                         "scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai "
                         "directly, not stale mirrors.) https://livebench.ai/")
        self.assertEqual(lines[8:], [""])

    def test_cut_row_output(self):
        code, out, _ = run(["cite", "gaia"])
        self.assertEqual(code, 0)
        self.assertIn("verdict: cut\n", out)
        self.assertIn("do not cite: Grader exploited", out)
        self.assertNotIn("cite as:", out)

    def test_several_substring_matches_are_refused(self):
        code, out, err = run(["cite", "Verified"])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("matches", err)

    def test_single_substring_hit(self):
        code, out, err = run(["cite", "terminal"])
        self.assertEqual(code, 0)
        self.assertEqual(out.split("\n")[0], "Terminal-Bench 2.x")

    def test_many_matches_list_names_on_stderr(self):
        code, out, err = run(["cite", "bench"])
        self.assertEqual((code, out), (1, ""))
        self.assertTrue(err.startswith("'bench' matches "))
        self.assertIn("benchmarks; name one of:\n  ", err)
        self.assertLessEqual(len(err.strip().split("\n")), 1 + 5)

    def test_unknown_name(self):
        code, out, err = run(["cite", "zzzzqq"])
        self.assertEqual((code, out), (1, ""))
        self.assertEqual(err, "no benchmark matches 'zzzzqq'\n")

    def test_close_names_are_offered(self):
        code, out, err = run(["cite", "livebnch"])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("closest names:\n  LiveBench\n", err)

    def test_json_parses(self):
        code, out, _ = run(["cite", "livebench", "--json"])
        doc = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(doc["id"], "livebench")
        self.assertEqual(doc["recheck_due"], "2027-01-17")
        self.assertFalse(doc["do_not_cite"])
        self.assertTrue(doc["cite_as"].startswith("LiveBench (as of 2026-07-17; caveat: "))
        code, out, _ = run(["cite", "gaia", "--json"])
        doc = json.loads(out)
        self.assertEqual((code, doc["cite_as"], doc["do_not_cite"]), (0, None, True))

    def test_recheck_dates(self):
        _c, out, _e = run(["cite", "terminal-bench"])
        self.assertIn("re-check due: 2026-10-17\n", out)
        _c, out, _e = run(["cite", "livebench"])
        self.assertIn("re-check due: 2027-01-17\n", out)


class ListTest(unittest.TestCase):
    def test_all(self):
        code, out, _ = run(["list"])
        lines = out.rstrip("\n").split("\n")
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 53)
        self.assertEqual(lines[-1], "52 benchmarks (0 canon, 48 caveat, 4 cut)")

    def test_filters(self):
        code, out, _ = run(["list", "--verdict", "cut"])
        lines = out.rstrip("\n").split("\n")
        self.assertEqual(lines[-1], "4 benchmarks (0 canon, 0 caveat, 4 cut)")
        self.assertEqual(len(lines), 5)
        code, out, _ = run(["list", "--cat", "coding"])
        self.assertEqual(out.rstrip("\n").split("\n")[-1].split(" (")[0], "%d benchmarks" % len(CODING))
        code, out, _ = run(["list", "--cat", "coding", "--verdict", "cut"])
        self.assertEqual(out.rstrip("\n").split("\n")[-1], "2 benchmarks (0 canon, 0 caveat, 2 cut)")
        code, out, _ = run(["list", "--cat", "nothing"])
        self.assertEqual((code, out), (0, "0 benchmarks (0 canon, 0 caveat, 0 cut)\n"))

    def test_json(self):
        code, out, _ = run(["list", "--verdict", "cut", "--json"])
        doc = json.loads(out)
        self.assertEqual((code, doc["count"], len(doc["benchmarks"])), (0, 4, 4))
        self.assertTrue(all(b["verdict"] == "cut" for b in doc["benchmarks"]))

    def test_bad_verdict_is_a_usage_error(self):
        code, out, err = run(["list", "--verdict", "maybe"])
        self.assertEqual(code, 2)
        self.assertEqual(len(err.strip().split("\n")), 1)


class CheckTest(TempDirMixin, unittest.TestCase):
    def check(self, text, *extra):
        tmp = self.make_tmp()
        path = os.path.join(tmp, "draft.md")
        write(path, text)
        return run(["check", path] + list(extra)), path

    def test_two_hits_one_cut_exits_one(self):
        (code, out, err), path = self.check("We use LiveBench here.\nAnd GAIA too.\n")
        lines = out.rstrip("\n").split("\n")
        self.assertEqual((code, err), (1, ""))
        self.assertEqual(lines[0], "%s:1: LiveBench [caveat] %s" % (path, real_by_id("livebench")["caveat"]))
        self.assertEqual(lines[1], "%s:2: GAIA [cut] %s" % (path, real_by_id("gaia")["caveat"]))
        self.assertEqual(lines[2], "2 citations, 1 cut")

    def test_caveat_only_exits_zero(self):
        (code, out, _), _p = self.check("Only LiveBench is named.\n")
        self.assertEqual(code, 0)
        self.assertTrue(out.endswith("1 citations, 0 cut\n"))

    def test_no_hits(self):
        (code, out, _), _p = self.check("Nothing relevant here.\n")
        self.assertEqual((code, out), (0, "0 citations, 0 cut\n"))

    def test_a_name_inside_a_longer_word_is_not_a_hit(self):
        (code, out, _), _p = self.check("Sometimes the gaiany or livebenchmarks or xLiveBench show up.\n")
        self.assertEqual((code, out), (0, "0 citations, 0 cut\n"))

    def test_case_is_ignored_and_aliases_count(self):
        (code, out, _), _p = self.check("see livebench and also hal for agents\n")
        self.assertEqual(code, 0)
        self.assertIn("LiveBench [caveat]", out)
        self.assertIn("HAL (Holistic Agent Leaderboard) [", out)

    def test_punctuation_next_to_a_name_still_hits(self):
        (code, out, _), _p = self.check("(LiveBench), and \"GAIA\".\n")
        self.assertEqual(out.rstrip("\n").split("\n")[-1], "2 citations, 1 cut")

    def test_longer_overlapping_name_wins(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)
        path = os.path.join(tmp, "d.md")
        write(path, "Alpha Two beats Alpha and Alpha One.\n")
        code, out, _ = run(["check", path], root=root)
        lines = out.rstrip("\n").split("\n")
        self.assertEqual(code, 1)
        self.assertEqual([l.split(": ", 1)[1].split(" [")[0] for l in lines[:-1]],
                         ["Alpha Two", "Alpha", "Alpha One"])
        self.assertEqual(lines[-1], "3 citations, 1 cut")

    def test_alias_of_the_longer_row(self):
        tmp = self.make_tmp()
        root = make_mini(tmp)
        path = os.path.join(tmp, "d.md")
        write(path, "The A1 score.\n")
        code, out, _ = run(["check", path], root=root)
        self.assertEqual((code, out.rstrip("\n").split("\n")[0].split(": ", 1)[1].split(" [")[0]), (0, "Alpha One"))

    def test_stdin(self):
        code, out, err = run(["check", "-"], stdin="LiveBench\nGAIA\n")
        self.assertEqual((code, err), (1, ""))
        lines = out.rstrip("\n").split("\n")
        self.assertTrue(lines[0].startswith("-:1: LiveBench [caveat]"))
        self.assertTrue(lines[1].startswith("-:2: GAIA [cut]"))
        self.assertEqual(lines[2], "2 citations, 1 cut")

    def test_several_files(self):
        tmp = self.make_tmp()
        first, second = os.path.join(tmp, "a.md"), os.path.join(tmp, "b.md")
        write(first, "LiveBench\n")
        write(second, "\n\nGAIA\n")
        code, out, _ = run(["check", first, second])
        lines = out.rstrip("\n").split("\n")
        self.assertEqual(code, 1)
        self.assertTrue(lines[0].startswith(first + ":1:"))
        self.assertTrue(lines[1].startswith(second + ":3:"))

    def test_missing_file_exits_two_with_no_partial_output(self):
        tmp = self.make_tmp()
        good = os.path.join(tmp, "a.md")
        write(good, "LiveBench\n")
        code, out, err = run(["check", good, os.path.join(tmp, "nope.md")])
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(len(err.strip().split("\n")), 1)
        self.assertTrue(err.startswith("canon.py: "))

    def test_json(self):
        (code, out, _), path = self.check("LiveBench and GAIA\n", "--json")
        doc = json.loads(out)
        self.assertEqual((code, doc["citations"], doc["cut"]), (1, 2, 1))
        first = doc["hits"][0]
        self.assertEqual((first["file"], first["line"], first["matched"], first["id"]),
                         (path, 1, "LiveBench", "livebench"))
        self.assertEqual(sorted(first), ["caveat", "file", "id", "line", "matched", "name", "verdict"])


def real_by_id(rid):
    return [r for r in real_rows() if r["id"] == rid][0]


class StaleTest(TempDirMixin, unittest.TestCase):
    def test_before_the_first_date_nothing_is_stale(self):
        code, out, _ = run(["stale", "--today", "2026-10-16"])
        self.assertEqual((code, out), (0, "0 of 52 past their re-check date\n"))

    def test_coding_rows_on_their_due_date(self):
        code, out, _ = run(["stale", "--today", "2026-10-17"])
        lines = out.rstrip("\n").split("\n")
        self.assertEqual(code, 1)
        self.assertEqual(lines[-1], "%d of 52 past their re-check date" % len(CODING))
        listed = sorted(l.split("  ")[0] for l in lines[:-1])
        self.assertEqual(listed, sorted(r["name"] for r in CODING))
        for line in lines[:-1]:
            self.assertTrue(line.endswith("checked 2026-07-17  due 2026-10-17"), line)

    def test_everything_on_the_second_date(self):
        code, out, _ = run(["stale", "--today", "2027-01-17"])
        self.assertEqual(code, 1)
        self.assertEqual(out.rstrip("\n").split("\n")[-1], "52 of 52 past their re-check date")

    def test_day_between_the_dates(self):
        code, out, _ = run(["stale", "--today", "2027-01-16"])
        self.assertEqual(out.rstrip("\n").split("\n")[-1], "%d of 52 past their re-check date" % len(CODING))

    def test_json(self):
        code, out, _ = run(["stale", "--today", "2026-10-17", "--json"])
        doc = json.loads(out)
        self.assertEqual((code, doc["today"], doc["total"], doc["count"]), (1, "2026-10-17", 52, len(CODING)))
        self.assertEqual(len(doc["stale"]), len(CODING))

    def test_month_end_is_clamped(self):
        root = make_mini(self.make_tmp())
        code, out, _ = run(["cite", "Alpha One"], root=root)
        self.assertIn("checked: 2026-08-31\nre-check due: 2026-11-30\n", out)
        code, out, _ = run(["cite", "Beta Three"], root=root)
        self.assertIn("re-check due: 2027-02-28\n", out)

    def test_clamped_boundary_in_stale(self):
        root = make_mini(self.make_tmp())
        code, out, _ = run(["stale", "--today", "2026-11-29"], root=root)
        self.assertEqual((code, out), (0, "0 of 4 past their re-check date\n"))
        code, out, _ = run(["stale", "--today", "2026-11-30"], root=root)
        self.assertEqual(code, 1)
        self.assertEqual(out.rstrip("\n").split("\n")[-1], "3 of 4 past their re-check date")

    def test_year_end_rollover(self):
        root = make_mini(self.make_tmp(), checked="2026-10-15")
        code, out, _ = run(["cite", "Beta Three"], root=root)
        self.assertIn("re-check due: 2027-04-15\n", out)
        code, out, _ = run(["cite", "Alpha One"], root=root)
        self.assertIn("re-check due: 2027-01-15\n", out)

    def test_bad_today_is_a_usage_error(self):
        code, out, err = run(["stale", "--today", "17/10/2026"])
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(len(err.strip().split("\n")), 1)


class ValidateProblemTest(TempDirMixin, unittest.TestCase):
    """One test per kind of problem, each on a small temp root."""

    def problems(self, root):
        code, out, err = run(["validate"], root=root)
        return code, out

    def setUp(self):
        self.tmp = self.make_tmp()
        self.root = make_mini(self.tmp)

    def assert_problem(self, fragment):
        code, out = self.problems(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(fragment, out)

    def edit_rows(self, fn):
        edit_json(self.root, "data/verdicts.json", lambda d: fn(d["benchmarks"]))

    def test_mini_root_is_valid(self):
        self.assertEqual(self.problems(self.root), (0, "ok\n"))

    def test_duplicate_id(self):
        self.edit_rows(lambda rows: rows[1].update(id="one"))
        self.assert_problem("duplicate id")

    def test_bad_id(self):
        self.edit_rows(lambda rows: rows[0].update(id="Bad Id"))
        self.assert_problem("id is not a lowercase slug")

    def test_bad_verdict(self):
        self.edit_rows(lambda rows: rows[0].update(verdict="maybe"))
        self.assert_problem("verdict 'maybe' is not canon, caveat or cut")

    def test_url_not_https(self):
        self.edit_rows(lambda rows: rows[0].update(url="http://example.org/one"))
        self.assert_problem("url is missing or not an https URL")

    def test_empty_caveat(self):
        self.edit_rows(lambda rows: rows[0].update(caveat="  "))
        self.assert_problem("caveat is empty")

    def test_bad_checked_date(self):
        edit_json(self.root, "data/verdicts.json", lambda d: d.update(checked="2026-13-40"))
        self.assert_problem("checked is not a YYYY-MM-DD date")

    def test_bad_row_checked_date(self):
        self.edit_rows(lambda rows: rows[0].update(checked="yesterday"))
        self.assert_problem("checked is not a YYYY-MM-DD date: 'yesterday'")

    def test_alias_claimed_twice(self):
        self.edit_rows(lambda rows: rows[3].update(aliases=["a1"]))
        self.assert_problem("claimed by two rows")

    def test_alias_equal_to_another_name(self):
        self.edit_rows(lambda rows: rows[3].update(aliases=["ALPHA TWO"]))
        self.assert_problem("claimed by two rows")

    def test_missing_evidence(self):
        os.remove(os.path.join(self.root, "evidence", "three.md"))
        self.assert_problem("evidence file evidence/three.md is missing")

    def test_evidence_with_the_wrong_verdict_line(self):
        write(os.path.join(self.root, "evidence", "three.md"), "x\n\nVERDICT: cut | n | c\n")
        self.assert_problem("evidence/three.md does not end with a VERDICT: caveat line")

    def test_evidence_with_no_verdict_line(self):
        write(os.path.join(self.root, "evidence", "three.md"), "x\n\nNothing here\n")
        self.assert_problem("does not end with a VERDICT: caveat line")

    def test_missing_memo(self):
        os.remove(os.path.join(self.root, "memos", "beta.md"))
        self.assert_problem("memo memos/beta.md is missing")

    def test_memo_with_the_wrong_primary_line(self):
        write(os.path.join(self.root, "memos", "beta.md"), "x\n\nPRIMARY: Somebody Else\n")
        self.assert_problem("memos/beta.md does not end with PRIMARY: Beta Three")

    def test_category_without_primary(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"].pop())
        self.assert_problem("category beta has no primary")

    def test_two_primaries_for_one_category(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"].append(dict(c["primaries"][0])))
        self.assert_problem("category alpha has two primaries")

    def test_primary_pick_id_not_a_row(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"][0].update(pick_id="nope"))
        self.assert_problem("pick_id 'nope' is not a row")

    def test_primary_in_another_category(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"][0].update(pick_id="three", pick="Beta Three"))
        self.assert_problem("belongs to category beta")

    def test_primary_is_a_cut_row(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"][0].update(pick_id="two", pick="Alpha Two"))
        self.assert_problem("primary alpha: pick_id two is a cut row")

    def test_primary_name_does_not_match(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"][0].update(pick="Wrong Name"))
        self.assert_problem("pick does not match the name of one")

    def test_category_without_label(self):
        edit_json(self.root, "data/canon.json", lambda c: c["labels"].pop("beta"))
        self.assert_problem("category beta has no label in canon.json")

    def test_empty_note(self):
        edit_json(self.root, "data/canon.json", lambda c: c.update(note=""))
        self.assert_problem("canon.json: note is missing or empty")

    def test_bad_asof(self):
        edit_json(self.root, "data/canon.json", lambda c: c.update(asof="soon"))
        self.assert_problem("asof is not a YYYY-MM-DD date")

    def test_revet_default_must_be_an_integer(self):
        edit_json(self.root, "data/canon.json", lambda c: c["revet_months"].update(default="six"))
        self.assert_problem("revet_months must be an object with an integer default")

    def test_rules_must_be_a_list(self):
        edit_json(self.root, "data/canon.json", lambda c: c.update(rules="none"))
        self.assert_problem("canon.json: rules must be a list")

    def test_labels_must_be_an_object(self):
        edit_json(self.root, "data/canon.json", lambda c: c.update(labels=["alpha", "beta"]))
        self.assert_problem("canon.json: labels must be an object")

    def test_benchmark_entry_not_an_object(self):
        self.edit_rows(lambda rows: rows.append("five"))
        self.assert_problem("verdicts.json: benchmark entry 5 is not an object")

    def test_empty_name(self):
        self.edit_rows(lambda rows: rows[0].update(name=" "))
        self.assert_problem("row one: name is missing or empty")

    def test_aliases_must_be_strings(self):
        self.edit_rows(lambda rows: rows[0].update(aliases=["a1", ""]))
        self.assert_problem("row one: aliases must be a list of non-empty strings")

    def test_category_not_a_slug(self):
        self.edit_rows(lambda rows: rows[0].update(cat="Alpha Group"))
        self.assert_problem("category 'Alpha Group' is not a lowercase slug")

    def test_primaries_entry_not_an_object(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"].append("alpha"))
        self.assert_problem("canon.json: a primaries entry is not an object")

    def test_primary_rule_empty(self):
        edit_json(self.root, "data/canon.json", lambda c: c["primaries"][0].update(rule=""))
        self.assert_problem("rule is missing or empty")

    def test_evidence_not_utf8(self):
        with open(os.path.join(self.root, "evidence", "three.md"), "wb") as fh:
            fh.write(b"\xff\xfe not text\n")
        self.assert_problem("row three: evidence file evidence/three.md cannot be read")

    def test_memo_not_utf8(self):
        with open(os.path.join(self.root, "memos", "beta.md"), "wb") as fh:
            fh.write(b"\xff\xfe not text\n")
        self.assert_problem("category beta: memo memos/beta.md cannot be read")

    def test_validate_prints_every_problem(self):
        os.remove(os.path.join(self.root, "evidence", "three.md"))
        os.remove(os.path.join(self.root, "memos", "beta.md"))
        code, out = self.problems(self.root)
        self.assertEqual(code, 1)
        self.assertEqual(len(out.rstrip("\n").split("\n")), 2)


class UsageErrorTest(TempDirMixin, unittest.TestCase):
    def test_unreadable_root(self):
        code, out, err = run(["list"], root=os.path.join(self.make_tmp(), "missing"))
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(len(err.strip().split("\n")), 1)
        self.assertTrue(err.startswith("canon.py: "))

    def test_broken_json(self):
        root = make_mini(self.make_tmp())
        write(os.path.join(root, "data", "verdicts.json"), "{not json")
        code, out, err = run(["list"], root=root)
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(len(err.strip().split("\n")), 1)

    def test_unknown_command(self):
        code, out, err = run(["frobnicate"])
        self.assertEqual(code, 2)
        self.assertEqual(len(err.strip().split("\n")), 1)

    def test_no_command(self):
        code, out, err = run([])
        self.assertEqual(code, 2)


class SubprocessTest(unittest.TestCase):
    """The real program, as a user starts it."""

    def run_cli(self, *args, **kw):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run([sys.executable, os.path.join(REPO, "canon.py")] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, env=env, cwd=REPO, **kw)

    def test_cite_runs_as_a_script(self):
        done = self.run_cli("cite", "livebench")
        self.assertEqual(done.returncode, 0)
        self.assertEqual(done.stdout.split("\n")[0], "LiveBench")

    def test_check_exit_code_reaches_the_shell(self):
        done = self.run_cli("check", "-", input="GAIA\n")
        self.assertEqual(done.returncode, 1)
        self.assertTrue(done.stdout.endswith("1 citations, 1 cut\n"))

    def test_stale_exit_code_reaches_the_shell(self):
        self.assertEqual(self.run_cli("stale", "--today", "2026-10-16").returncode, 0)
        self.assertEqual(self.run_cli("stale", "--today", "2026-10-17").returncode, 1)

    def test_usage_error_exit_code_and_one_line(self):
        done = self.run_cli("check", "no-such-file.md")
        self.assertEqual(done.returncode, 2)
        self.assertEqual(done.stdout, "")
        self.assertEqual(len(done.stderr.strip().split("\n")), 1)

    def test_validate_exit_code(self):
        done = self.run_cli("validate")
        self.assertEqual((done.returncode, done.stdout), (0, "ok\n"))

    def test_root_flag(self):
        done = self.run_cli("--root", REPO, "list", "--verdict", "cut")
        self.assertEqual(done.returncode, 0)


if __name__ == "__main__":
    unittest.main()
