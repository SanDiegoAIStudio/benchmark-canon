# benchmark-canon

A dated ledger of 52 AI benchmarks. Each one carries a verdict (cite it with a caveat, or do not cite it), the caveat to print beside any score, and the evidence file behind it. All 52 rows were checked on 2026-07-17 and none came out clean. The repository ships the ledger as data, as a Markdown table and as one self-contained web page, with a small command line tool that looks up a benchmark and checks a draft for the benchmarks it names.

Checked 2026-07-17. The refuter round checked 51 benchmarks (47 with a caveat, 4 cut); Deep SWE was vetted separately and also carries a caveat.

## What you get

- `CANON.md`: the table to read. The eleven primaries (the benchmark to cite first in each category), the ledger by category, the gaps nobody measures, eleven standing citation rules, and the sources the canon leans on.
- `index.html`: the same content as one page with inline styles, no script and no outside requests. It works opened from disk and has a dark mode.
- `canon.jsonl`: the same content as one JSON object per line, 89 rows, for loading into other tools.
- `evidence/`: one file per benchmark, 52 files, each ending in its `VERDICT:` line.
- `memos/`: one file per category, 11 files, each ending in its `PRIMARY:` line.
- `data/`: the two JSON files the three outputs are built from.
- `canon.py`: the tool. Python 3.9 or later, standard library only, nothing to install.

Four benchmarks are cut. This is the output of `python3 canon.py list --verdict cut`:

```
swe-bench-pro          cut     coding      SWE-bench Pro
swe-bench-verified     cut     coding      SWE-bench Verified
gaia                   cut     agentic     GAIA
freshqa                cut     search      FreshQA
4 benchmarks (0 canon, 0 caveat, 4 cut)
```

The reason for each, taken from the `do not cite:` line of `python3 canon.py cite NAME` run for each of the four:

```
SWE-bench Pro       do not cite: Live Meta 49% COI scoring its own model, OpenAI retracted its endorsement over 30% broken tasks, unpatched reward-hacking exploit.
SWE-bench Verified  do not cite: Funder's own audit proved contamination+broken tests; 3 gaming incidents; frontier-saturated; successor also retracted.
GAIA                do not cite: Grader exploited to ~98% (Berkeley RDI, Apr 2026); HAL paused; creators shipped GAIA2 successor; no clean citable split.
FreshQA             do not cite: Cadence dead 11+ wks past self-set date; core search-vs-memorization signal empirically broken (74.3%); Google self-grades own model.
```

The other 48 are cited with a caveat. This is the full output of `python3 canon.py cite livebench`:

```
LiveBench
verdict: caveat
checked: 2026-07-17
re-check due: 2027-01-17
caveat: Live, objective, no-LLM-judge scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai directly, not stale mirrors.
source: https://livebench.ai/
evidence: evidence/livebench.md
cite as: LiveBench (as of 2026-07-17; caveat: Live, objective, no-LLM-judge scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai directly, not stale mirrors.) https://livebench.ai/
```

## Quick start

Clone or download the repository, then run these from its folder.

```
python3 canon.py cite livebench
```

Prints one benchmark: its verdict, the date it was checked, the date it is due for another look, the caveat, the source link, the evidence file, and a ready-to-paste `cite as:` line (or `do not cite:` for a cut row). Look up by id, name or a listed alias, in any letter case. When nothing matches exactly, any benchmark whose id, name or alias contains the query counts, so a unique part also works. A name that fits several benchmarks prints up to five candidates on stderr and exits 1, and a name that fits none prints `no benchmark matches` on stderr and exits 1.

```
python3 canon.py check your-draft.md
```

Scans a text for benchmark names and prints one line for each, with its verdict and caveat, then a count. See "Check a draft" below.

```
python3 canon.py stale
```

Lists the rows whose re-check date is today or earlier, then a count such as `6 of 52 past their re-check date`. It exits 1 when any row is listed.

Other commands: `list [--cat CATEGORY] [--verdict canon|caveat|cut]` shows the rows, `validate` checks the data files, and `build` rewrites `canon.jsonl`, `CANON.md` and `index.html`. `cite`, `list`, `check` and `stale` take `--json`. `--root DIR` points the tool at another copy of the data folders; it goes before the command, as in `python3 canon.py --root DIR list`.

## How to read a verdict

- `caveat`: the benchmark can be cited, with the caveat printed beside the number. 48 rows.
- `cut`: do not cite it. 4 rows.
- `canon`: cite it plain. No benchmark has earned it in this edition, so there are 0 rows.

The caveat is a one-line summary of the findings that matter most. The evidence file named in the `evidence:` line holds the full findings, with links, under headings for five questions: who funds it, how it is graded, whether it still separates models, whether anyone has gamed it, and whether it is still maintained. Some files answer two questions under one heading or leave one out: `evidence/swe-bench-pro.md` answers grading and gaming together under Integrity, and `evidence/tau2-bench.md` has no heading on gaming. Read it before you rely on a verdict. [METHOD.md](METHOD.md) lists the questions asked under each heading.

`re-check due` is the date after which the verdict should be looked at again; see "Re-check dates".

## Check a draft

`check` reads each line of a file and looks for benchmark names. A hit is a benchmark name or one of its listed aliases that appears as a whole word, in any letter case. A name inside a longer word is not a hit. When two names overlap, the longer one wins. It reads one line at a time, so a name broken across two lines is not found.

Exit codes: 0 when the text names no cut benchmark (including when it names none), 1 when it names at least one cut benchmark, 2 when a file cannot be read or the command is used wrongly (one line on stderr, nothing on stdout).

A three-line sample, saved as `draft.md`:

```
Our agent scores well on Terminal-Bench 2.x and LiveBench.
Earlier work reported GAIA results too.
Nothing else here is a benchmark.
```

The output of `python3 canon.py check draft.md`, which exited 1:

```
draft.md:1: Terminal-Bench 2.x [caveat] Real leaderboard cheating + unpatched harness exploit found; still discriminates: must name score source (tbench.ai vs AA diverge).
draft.md:1: LiveBench [caveat] Live, objective, no-LLM-judge scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai directly, not stale mirrors.
draft.md:2: GAIA [cut] Grader exploited to ~98% (Berkeley RDI, Apr 2026); HAL paused; creators shipped GAIA2 successor; no clean citable split.
3 citations, 1 cut
```

A file name of `-` reads standard input. The output of `cat draft.md | python3 canon.py check -`, which also exited 1, is the same with `-` in place of the file name:

```
-:1: Terminal-Bench 2.x [caveat] Real leaderboard cheating + unpatched harness exploit found; still discriminates: must name score source (tbench.ai vs AA diverge).
-:1: LiveBench [caveat] Live, objective, no-LLM-judge scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai directly, not stale mirrors.
-:2: GAIA [cut] Grader exploited to ~98% (Berkeley RDI, Apr 2026); HAL paused; creators shipped GAIA2 successor; no clean citable split.
3 citations, 1 cut
```

Several files can be given at once. Because the exit code is 1 only when a cut benchmark is named, `check` can gate a build or a review.

## Re-check dates

A row's re-check date is its checked date plus a number of months, on the same day of the month, or on the last day of the month when that day does not exist (2026-08-31 plus 3 months is 2026-11-30). The coding category is re-checked after 3 months and every other category after 6.

For the rows checked on 2026-07-17 that gives two dates: 2026-10-17 for the coding rows and 2027-01-17 for all the others. In plain words, the coding rows have been due since 2026-10-17. Run on 2026-11-17, `python3 canon.py stale` exited 1 and its output began:

```
Aider Polyglot Leaderboard  coding  checked 2026-07-17  due 2026-10-17
Deep SWE (Data Curve)  coding  checked 2026-07-17  due 2026-10-17
LiveCodeBench  coding  checked 2026-07-17  due 2026-10-17
Terminal-Bench 2.x  coding  checked 2026-07-17  due 2026-10-17
SWE-bench Pro  coding  checked 2026-07-17  due 2026-10-17
SWE-bench Verified  coding  checked 2026-07-17  due 2026-10-17
6 of 52 past their re-check date
```

`python3 canon.py stale --today 2026-10-16` prints `0 of 52 past their re-check date` and exits 0, so any day can be tested.

## Add or re-check a row

In short: write or update the row's evidence file, add or change its row in `data/verdicts.json`, update the category memo and primary if the best choice changed, run `python3 canon.py validate`, then `python3 canon.py build`, then the tests. The full steps, the two line formats the checks depend on, and the questions to ask under each of the five headings are in [METHOD.md](METHOD.md).

## Host the page

`index.html` is self-contained: inline styles, no script, and no request to any other host. It can be opened from disk, and GitHub Pages can serve it from the repository root (Settings, Pages, deploy from a branch, folder `/ (root)`). No hosted copy exists. The evidence and memo links on the page are relative links to the `.md` files in the repository, so a server may show them as plain text or offer them as a download.

## Tests

```
python3 -m unittest discover -s tests
python3 tests/mutate.py
```

The first runs the unit tests: the shipped data, the three built files (a fresh build must equal the committed ones), and the command line, including one test for each kind of problem `validate` reports. The second makes 26 deliberate breakages of `canon.py`, one at a time, in a temporary copy of the repository, runs the whole test suite against each, and prints `killed` when the suite fails and `survived` when it still passes. It exits 1 if any survives. After any change to `canon.py` or the data, run `python3 canon.py build` and commit the three rebuilt files, or the build test fails.

## Limits

- Every verdict dates from 2026-07-17. Nothing has been rechecked since.
- The verdicts, the writeups and the memos were written by AI agents (Claude) with web access. No person has rechecked every link, so links can be dead and a writeup can be wrong.
- The agents' prompts and the run are not in this repository, so the round cannot be rerun from it.
- A verdict is a judgment with cited reasons. Read the evidence file before you rely on one.
- The six entries under "Voids nobody measures" in `CANON.md` are the round's own observations. The `evidence/` folder holds a file for each benchmark row only, so claims inside a void, such as who owns which review site, carry no source link in this repository.
- `check` finds exact names and the listed aliases only. It does not find a benchmark described in other words, a misspelling, or a name split across two lines.
- Short aliases such as `HAL` and `ECI` are matched as whole words, so they also hit those letters when a draft uses them for something else. Read each hit before you act on it.
- The files `build --out DIR` writes link to `evidence/` and `memos/` inside DIR, so those links open only when DIR is the repository folder (the default) or holds copies of both folders.
- `stale` compares the re-check dates with the computer's date, so its list grows as time passes, and it exits 1 once any row is past due. Six of the 52 shipped rows fall due on 2026-10-17 and the other 46 on 2027-01-17. Give `--today YYYY-MM-DD` to check against another date.
- `list --cat` with a category name that does not exist prints `0 benchmarks` and exits 0, so a misspelled category looks like an empty one. `list` without `--cat` shows the category of every row.
- `check -` reads standard input in the encoding of your locale, while files are read as UTF-8. Under a locale that is not UTF-8, pass the file name instead.

## License

MIT. See [LICENSE](LICENSE).

## Built at San Diego AI Studio

This canon comes out of San Diego AI Studio, the builders' community in San Diego. More of what its members build is at https://sandiegoaistudio.com/projects.
