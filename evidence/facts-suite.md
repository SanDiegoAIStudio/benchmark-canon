**Vendor capture: confirmed, severe.** Google DeepMind built the FACTS Suite; Google-owned Kaggle (acquired 2017, techcrunch.com/2017/03/08/google-confirms-its-acquisition-of-data-science-community-kaggle) hosts it, holds the private set, and "tests the leading LLMs." Google's own models occupy #1 (Gemini 3 Pro, 68.8%) and #2 (Gemini 2.5 Pro, 62.1%) on a leaderboard the company builds, hosts, and grades end-to-end: no independent third party involved. Sources: deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models, arxiv.org/abs/2512.10791 (Dec 2025, 65 authors, acknowledgments credit only "Gemini Team"/"Kaggle Team").

**Judge bias: regressed vs predecessor.** FACTS Grounding v1 (Jan 2025, arxiv.org/abs/2501.03200) used three cross-vendor judges (Gemini 1.5 Pro, GPT-4o, Claude 3.5 Sonnet) specifically to blunt self-preferencing. The Dec 2025 four-part Suite drops that for 2 of 4 legs: Parametric is judged by Gemini-2.5-Pro, Search by Gemini-2.0-Flash: Google's model grading Google's own answers. Only Grounding v2 keeps a second-vendor judge (GPT-5).

**Contamination.** Parametric is Wikipedia-grounded with no published train/test-leakage analysis: a "closed-book knowledge" test whose answers likely sit in every frontier model's pretraining data. The private held-out set (859/1,719 examples, v1) is the sole stated defense, and Google alone controls it; no external escrow/auditor named.

**Saturation, not saturated, real signal.** DeepMind's own conclusion: top score 68.8% ("considerable headroom"), spread down to ~51-53% (Claude Opus 4.5/4.8, Grok 4). Genuine discrimination at the frontier today.

**Gaming history.** No documented gaming/contamination scandal found in ~18 months live. Trade press (InfoQ, 2026-01-12) mostly repeats Google's framing uncritically; one outlet (hackshackers.com) explicitly flagged "when the referee is also a competitor, healthy skepticism is warranted."

**Staleness.** Suite launched 2025-12-09, ~7 months old, actively updated (Claude Opus 4.8 already listed at 53.7%). Caveat: an older, separately-scored standalone "FACTS Grounding" leaderboard (0-1 scale) still circulates via aggregators (llm-stats.com, marked "unverified/self-reported"): cite the Suite's FACTS Score explicitly, not a bare "FACTS Grounding %."

**FOR:** best-published cross-modal factuality benchmark available, real methodology paper, genuine spread, growing roster. Trustworthy as a RELATIVE hallucination-proneness ranking across frontier chat models, not as proof Gemini is factually superior, since the vendor builds, hosts, holds the answer key, and partly judges its own entry.

VERDICT: caveat | FACTS Benchmark Suite | Google builds/hosts/self-judges via owned Kaggle; Gemini judges 2/4 legs; usable as relative signal only, not proof of superiority
