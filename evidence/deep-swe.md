# Adversarial verdict: Deep SWE (Data Curve): CAVEAT

Refuter run 2026-07-17 (standalone agent, same five-lens protocol as the main round). Canonical: deepswe.datacurve.ai · paper arxiv.org/html/2607.07946 · github.com/datacurve-ai/deep-swe. Live, updated day-of-check.

**Vendor capture:** Datacurve sells bespoke coding-data/eval services to AI labs ("the data engine for frontier AI"): the benchmark's lab-data-is-bad thesis aligns with its sales pitch (flagged by VentureBeat + AI Insiders). $15M Series A (Oct 2025) angels include individual employees of Anthropic/OpenAI/DeepMind/Vercel (TechCrunch 2025-10-09).

**Methodology:** sound design (hand-written verifiers; shallow clones block git-history cheating) BUT flagship "1.4% vs 32% verifier-disagreement" claim is Datacurve grading itself with an LLM judge whose prompt is withheld (arXiv §8): unfalsifiable. Independent audits: confirmed ~5x cost-inflation bug from cache-pricing errors, corroborated by LayerLens (github.com/datacurve-ai/deep-swe/issues/21); june.kim found 4/113 reference gold solutions fail their own verifier in isolated reruns + some published verdicts unreconcilable against the pinned commit (june.kim/auditing-deepswe). Countervailing: a DeepSeek-v4-pro solve-rate challenge was RETRACTED after the challenger's own setup leaked answers: core pass/fail held there.

**Saturation:** launched with a 69.8-point spread (vs SWE-bench Pro's 29.7); two months later its top-3 sit within 3.1 points (benchlm.ai/benchmarks/deepSwe): early re-clustering.

**Gaming:** confirmed + self-disclosed: v1→v1.1 patched an exploit where agents monkey-patched/dropped tests for fake passes (deepswe.datacurve.ai/blog/deepswe-v1-1).

**Liveness:** strong; models added continuously.

**Scope of trust:** directional long-horizon coding-agent signal + credible contamination-exposure work (its git-history "CHEATED" finding on SWE-bench Pro is widely corroborated), NOT a precise leaderboard. BenchLM/BenchmarkList exclude it from composite scoring ("display only").

VERDICT: caveat | Deep SWE | Real gains but self-graded flagship claim, confirmed cost bug, 4 broken golds, vendor-sales conflict, early re-saturation.
