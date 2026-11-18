## Coding: Benchmark Trust Canon

### KEEP (ranked by trust strength)

1. **Aider Polyglot Leaderboard**: trust it for clean, execution-graded coding-edit quality among pre-Oct-2025 models (no gaming found); don't use it to rank any 2026 model, it isn't in the dataset.
2. **Terminal-Bench 2.x**: trust it for relative agentic/terminal task-completion signal between current models; don't cite a bare score, real leaderboard cheating and an unpatched harness exploit were found, so always name your source (tbench.ai vs Artificial Analysis diverge).
3. **LiveCodeBench**: trust it as a historical snapshot through ~Apr 2025; don't use it for current comparisons, pool is frozen, scores are self-reported, top tier is saturated.

### Primary

**Terminal-Bench 2.x**, not the #1-ranked Aider. Aider is the cleaner benchmark but is blind to every 2026 frontier model, so it can't answer the question an SMB actually needs answered: does this current tool finish real coding work? Terminal-Bench still discriminates between today's models despite its integrity problems, and it tests the agentic/terminal task-completion shape that SMB coding tools actually sell. Cite it with the specific score source pinned: never a bare number.

### Cut

- **SWE-bench Verified**: CUT: funder's own audit found contamination + broken tests, 3 gaming incidents, saturated, successor also retracted. Still the name most people default to asking for: expect the question.
- **SWE-bench Pro**: CUT: Meta scores its own model live (49% COI), OpenAI retracted its endorsement over 30% broken tasks, reward-hacking exploit unpatched.

PRIMARY: Terminal-Bench 2.x
