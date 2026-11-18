**Vendor capture:** No sponsor, lab funding, or equity link found for Paul Gauthier/Aider (Apache-2.0, solo maintainer, ex-Groupon CTO). No smoking gun of capture (https://github.com/Aider-AI/aider, https://aider.chat/docs/leaderboards/).

**Methodology:** Grading is deterministic test-execution pass/fail, not LLM-judge, with a real 2-attempt edit loop (fail, error feedback, retry) across 225 Exercism exercises in 6 languages (https://aider.chat/docs/leaderboards/). Sound design, but Exercism solutions are public on GitHub and no decontamination statement exists in the docs: unaddressed train-on-test risk for any model trained after the set became known.

**Saturation:** Deliberately recalibrated Dec 2024 off an older benchmark saturating ~80%+ (https://aider.chat/2024/12/21/polyglot.html). Top score still climbed 72%→88% between May-Aug 2025 alone: trending toward re-saturation, but unverifiable further because no 2026 model has been added at all.

**Gaming history:** No documented gaming/manipulation incident found for this benchmark specifically: cleaner record than SWE-bench's.

**Staleness: the decisive finding:** the canonical data file's last real commit is 2025-10-03, confirmed by both commit log and raw file (https://github.com/Aider-AI/aider/commits/main/aider/website/_data/polyglot_leaderboard.yml, https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml). No blog post since May 2025 (https://aider.chat/blog/). GitHub issue #4584 (opened Oct 2025, no release since Aug 9) plus a 2026 Hacker News thread ("crickets… maintainer does not maintain") confirm the whole project stalled, spawning a community fork "Aider CE" (https://news.ycombinator.com/item?id=46067907). Zero GPT-5.1+, Opus 4.5+, Gemini 3+, or Grok 4.5 entries exist on the actual leaderboard. Any circulating "Aider polyglot" number for those models (e.g., Opus 4.5's 89.4%) traces to a vendor system card (https://www.anthropic.com/claude-opus-4-5-system-card), not Gauthier's harness: self-reported, not canon-verified.

**Strongest case FOR it:** sound, execution-graded (no LLM-judge), no capture evidence, independently tracked for years by Simon Willison (https://simonwillison.net/tags/paul-gauthier/). Trustworthy as a historical/methodology reference for pre-Oct-2025 models, not as a live current-frontier signal.

VERDICT: caveat | Aider Polyglot Leaderboard | Sound execution-graded methodology, no capture, but stale since Oct 2025: missing all 2026 frontier models
