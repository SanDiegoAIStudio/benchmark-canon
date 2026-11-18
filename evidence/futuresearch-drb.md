**Org & funding**: FutureSearch (founded 2023 by Dan Schwarz, ex-Metaculus/Google) raised a $5.7 to 5.79M seed in Nov 2024 led by **Metaplanet: an early Anthropic and DeepMind backer** (https://www.crunchbase.com/organization/varuna-ai, https://pitchbook.com/profiles/company/720755-65). FutureSearch also sells research directly to Anthropic, OpenAI, Google, and xAI (https://futuresearch.ai/company/). This is a material conflict: the org ranking these labs is investor- and client-linked to them, most directly Anthropic: whose Claude 4.6 Opus currently tops the DRB leaderboard (https://futuresearch.ai/docs/case-studies/deep-research-bench-pareto-analysis/).

**Methodology**: DRB uses "RetroSearch," a frozen offline scrape (up to ~189K pages/task) instead of live web, specifically to hold results stable and structurally block the live-search-leakage attack class (https://futuresearch.ai/deep-research-bench/). 89 tasks, 8 categories, human-derived reference answers, published with 8 named FutureSearch authors on arXiv (arxiv.org/abs/2506.06287). Whether final grading is fixed-answer matching or an LLM judge is not confirmable from public text: unconfirmed.

**Contamination**: A 2026 "Search-Time Contamination" paper (arxiv.org/html/2606.05241) surfaces adjacent to DRB in search results but actually tests six **medical** benchmarks (MedQA, MMLU-med, etc.); DRB/FutureSearch is not named in it. No confirmed contamination finding specific to DRB.

**Saturation**: Not saturated. Top score is 0.55/1.0 (Claude 4.6 Opus, high) across 26 agent configs with a real cost-accuracy Pareto spread, 7-model frontier: still discriminates (same URL as above).

**Gaming history**: None found in public record.

**Liveness**: Site reads "Updated June 25, 2026," and the current leaderboard cites frontier-era models (Claude 4.6 Opus, Gemini 3 Flash), consistent with active maintenance (https://futuresearch.ai/deep-research-bench/). Task count drifted 89→91 between paper and site: minor versioning noise, not disqualifying.

**Naming collision**: A separate, unrelated benchmark, "DeepResearch Bench / II" (Ayanami0730 et al., GPT-5.5 LLM-judge, arxiv.org/abs/2601.08536), shares a near-identical name. Do not let downstream citations conflate the two.

**Case for**: Best-in-class for relative cost/accuracy ranking of web-research agents: frozen corpus, named academic authorship, non-saturated at 55%. Not a neutral verdict on "which lab is best" given the Anthropic-adjacent funding and all-lab client roster.

VERDICT: caveat | Deep Research Bench (FutureSearch) | Frozen-corpus, non-saturated, no gaming found; but lead investor + clients include labs it ranks, esp. Anthropic.
