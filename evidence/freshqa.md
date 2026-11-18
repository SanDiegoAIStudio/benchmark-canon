## FreshQA (freshllms/freshqa): Adversarial Verification

**Vendor capture (1):** Author roster (Vu, Iyyer, Wang, Constant, J. Wei, J. Wei, Tar, Sung, Zhou, Le, Luong) is Google Research-led, with UMass Amherst co-authors Vu/Iyyer (ACL Findings 2024: https://aclanthology.org/2024.findings-acl.813/). Maintainer contact is a Google address; the GitHub org carries no independent verification (https://github.com/freshllms). Google builds, hosts, and grades this benchmark, and Gemini is among the models it scores: a disclosed but real structural conflict, not hidden pay-to-play. SerpApi donated 10K searches (minor, non-cash sponsorship).

**Methodology (2):** FreshEval's documented judge is GPT-4, specifically `gpt-4-1106-preview` (README). OpenAI retired that exact snapshot 2026-03-26 (https://developers.openai.com/api/docs/deprecations): the published eval pipeline can no longer be reproduced as specified. Separately, an independent paper (LiveNewsBench, arXiv:2602.13543, Feb 2026) found Gemini 3 Pro scores 74.3% on FreshQA with **zero** search access: fixed questions with a public, versioned answer history (Google Sheet, indexed since Feb 2024) leak into pretraining, so the "does search beat memorization" signal FreshQA exists to produce is measurably broken, not hypothetical.

**Saturation (3):** No maintained public leaderboard with current frontier scores was found. The same lineage (Tu Vu, a FreshQA author) shipped SealQA (arXiv:2506.01062, Jun 2025) explicitly to "raise the bar" because fixed-QA benchmarks including FreshQA plateau under memorization: an in-family admission the format needed replacing.

**Gaming history (4):** No documented cheating/scandal incident found: stated as a negative result. Only the structural memorization vulnerability above.

**Staleness (5), confirmed via commit history:** 196 total commits; HEAD of `main` is 2026-05-01, sha 7d2d368 (https://github.com/freshllms/freshqa/commits/main). README still reads "Current: April 21, 2026 / Next: May 11, 2026." That promised refresh never shipped: zero commits in 11+ weeks on a benchmark whose entire premise is "fresh."

**FOR:** Transparent, Apache-2.0, peer-reviewed methodology; still embedded as one probe inside composite harnesses (NVIDIA AI-Q Blueprint's FreshQA Evaluator, HalluLens paper). Its false-premise/debunking-question subset is a harder-to-memorize, still-useful qualitative check, distinct from the now-compromised recency-fact subset.

VERDICT: cut | FreshQA | Cadence dead 11+ wks past self-set date; core search-vs-memorization signal empirically broken (74.3%); Google self-grades own model.
