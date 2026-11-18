# Method

This file says how a row in the canon gets its verdict, and how to add a row or re-check one by hand. It is written for someone who wants to keep the canon current, or to judge whether to trust it.

One limit comes first. The verdicts here were produced by AI agents with web access: one agent per benchmark tried to refute it, then one agent per category wrote a memo and picked a primary. The prompts those agents were given and the record of the run are not in this repository. The round cannot be rerun from what is here. What you can do is read each evidence file, check its links, and redo any row by hand with the steps below.

## The five lenses

Every row was examined through the same five questions, in this order. Each evidence file in `evidence/` is organised around them. The sub-questions below are the ones the evidence files actually ask; the file named in brackets is a place to see the question answered.

### 1. Funding, ownership and conflicts

Who built the benchmark, who pays for it, and who benefits from the ranking?

- Does the operator sell products or services to the labs and vendors it ranks? An arena that also sells paid benchmarking to the ranked labs is a payer and rated overlap (`aa-index`, `aa-image-arena`, `agentharm`).
- Does an owner or funder of the benchmark also have a model on it? (`hle`, `swe-bench-verified`)
- Is there a conflict-of-interest statement on the benchmark's own site, or only in an interview? (`aa-index`, `livebench`)
- Is the board a true re-run, or are some rows team-reported? (`browsecomp`)
- Is the funder a single vendor, or do many labs and academics contribute? (`livebench`, `terminal-bench`)

### 2. Methodology and contamination

Can a score be earned without doing the task, and does the grading hold up?

- Are the answers or tests public, so a model or an agent can load them? (`gaia`, `browsecomp`)
- Who or what grades? If a model grades, is it from the same family as a model being scored, and is it an old model grading new ones? (`aa-index`, `hle`, `agentharm`)
- Has an outside audit found wrong answers or tests that reject correct fixes? (`hle`, `swe-bench-verified`)
- For a blind-vote arena, has anyone shown the model behind an answer can be identified, which breaks the blindness the ranking depends on? (`aa-image-arena`, `aa-speech-arena`)
- Does the same model swing a lot with the harness or retriever used, so the score belongs to the setup and not to the model? (`terminal-bench`, `gaia`, `browsecomp`)
- Are scores self-reported or independently measured?

### 3. Saturation

Does the benchmark still separate the models it is used to compare?

- How wide is the spread at the top, and do the error bars of the top entries overlap, so the order is a tie? (`arena-text`, `aa-speech-arena`)
- Do scores cluster near the ceiling? (`swe-bench-verified`)
- Has the maintainer said the suite is saturating, or that scores above some level are unreliable? (`metr-time-horizon`)
- Is there still headroom, with the frontier well below a human baseline? (`hle`)
- Does it still tell a weak model from a strong one even if it cannot order the top? (`arena-text`, `swe-bench-verified`)

### 4. Gaming history

Has anyone actually gamed it? Separate what is confirmed from what is alleged.

- A leaderboard entry removed after cheating was found (`terminal-bench`).
- A tuned variant that ranked far above the released model (`arena-text`).
- A model that reward-hacked the suite, or cracked an answer key it was never meant to see (`metr-time-horizon`, `browsecomp`).
- A rise on a usage chart explained by a free-promotion window (`openrouter-rankings`).
- A published exploit that scores near the maximum without doing the work (`gaia`, `swe-bench-verified`).
- A claim that an incident belongs to a different product with a similar name. Check that the incident is about this benchmark and not its namesake (`aa-image-arena`).
- No incident found is recorded as such, with how hard the search was. Absence is weak evidence and the file says so.

### 5. Staleness and liveness

Is it still maintained, and do the numbers people quote match the source?

- Is the primary source updated recently: commits, a changelog, new models added? (`livebench`, `aa-index`)
- Do different trackers give different numbers for the same model, or different winners? (`hle`, `terminal-bench`)
- Does a mirror show a fresh "last updated" date over old data? (`livebench`)
- Has the host paused updates, or the creators published a successor? (`gaia`)
- Is a figure in circulation traceable to a primary source at all? (`terminal-bench`)

After the five lenses, each evidence file states the best case for the benchmark: what it is still good for if it is cited carefully. The verdict line comes after that.

## The verdict scale

A verdict tells a person who wants to cite the benchmark what to do.

| Verdict | Instruction | Meaning here |
|---|---|---|
| canon | Cite plain. | The benchmark needs no qualification. No benchmark in this edition has earned it. |
| caveat | Cite with the caveat. | Usable, but only with the caveat text beside the number. The caveat names the one or two findings that matter most. |
| cut | Do not cite. | The findings on one or more lenses are bad enough that a number from it should not be quoted, even with a caveat. |

The edition has 52 rows: 48 caveat and 4 cut. The four cut rows are `freshqa`, `gaia`, `swe-bench-pro` and `swe-bench-verified`. A verdict is a judgment made from the evidence in the file next to it. Read the file before you rely on the verdict, and open the links in it.

## Categories, memos and primaries

Rows are grouped into 11 categories. After the refuters finished a category, one judge read that category's evidence and wrote a memo in `memos/<category>.md`: a ranked list of what to keep, what to cut, flags, and one primary, the single benchmark to cite first in that category. The primaries are listed in `data/canon.json` and shown at the top of `CANON.md` and `index.html`.

A primary is never a cut row, and it belongs to its own category. `python3 canon.py validate` checks both.

## Line formats

Two last lines are machine checked.

An evidence file ends with one line:

```
VERDICT: <verdict> | <benchmark name> | <caveat>
```

`<verdict>` is `canon`, `caveat` or `cut`. The caveat is the same text as the `caveat` field of the row in `data/verdicts.json`. Validation requires the last line to start with `VERDICT: ` and the row's verdict.

A memo ends with one line:

```
PRIMARY: <benchmark name>
```

The name must equal the `pick` of that category in `data/canon.json`.

## Add a row by hand

1. Pick an id: lowercase letters, digits and single hyphens, for example `my-bench`.
2. Work through the five lenses above. Write what you found, with the link for each claim, in `evidence/my-bench.md`. End the file with the case for the benchmark, then the `VERDICT:` line.
3. Add the row to `data/verdicts.json` under `benchmarks`, with `id`, `name`, `cat`, `url` (https), `verdict`, `caveat`, `round` and `aliases`. An alias is another way people write the name; `check` finds names and aliases. No name or alias may belong to two rows.
4. If the row is in a new category, add a label under `labels` in `data/canon.json`, a re-check interval if it should differ from the default under `revet_months`, a primary, and a memo.
5. Read the category memo again. If the new row changes which benchmark to cite first, change the memo, its last `PRIMARY:` line and the category's entry under `primaries` in `data/canon.json` together.
6. Update the `note` in `data/canon.json` if the counts in it are now wrong.
7. Run `python3 canon.py validate`. It prints every problem it finds, or `ok`.
8. Run `python3 canon.py build` to rewrite `canon.jsonl`, `CANON.md` and `index.html`.
9. Run `python3 -m unittest discover -s tests`. Some tests state the edition's exact counts (52 rows, 48 caveat, 4 cut), so a new row means updating those counts on purpose, in the same change.
10. Commit the data, the evidence file and the three rebuilt files together.

## Re-check a row by hand

1. Run `python3 canon.py stale` to see which rows are past their re-check date, or `python3 canon.py cite <name>` for one row.
2. Open the row's evidence file and go lens by lens. For each claim, open the link and see whether it still says that. Look for anything new: a funding announcement, an audit, an exploit, a successor, a pause.
3. Rewrite the evidence file where the findings changed. Keep its last line in the `VERDICT:` format, and change the verdict if the findings call for it.
4. In `data/verdicts.json`, update the row's `verdict` and `caveat` to match the new last line. To date the row on its own, add a `checked` field to it (`YYYY-MM-DD`); without one, the row takes the `checked` date at the top of the file. After a full pass, change that top date and `asof` in `data/canon.json` to the date of the pass.
5. If the verdict moved a benchmark in or out of cut, or changed the best choice in its category, update the memo and the primary as in step 5 of the previous list.
6. Validate, build, run the tests, and commit the data and the rebuilt files together.

The re-check interval is 3 months for the coding category and 6 months for every other category. The due date is the checked date plus that many months, on the same day of the month, or the last day of the month when that day does not exist (2026-08-31 plus 3 months is 2026-11-30).
