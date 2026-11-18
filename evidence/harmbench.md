**HarmBench (arXiv:2402.04249): Adversarial Verification**

**1. Vendor capture/funding:** CAIS runs on EA-aligned philanthropy, Open Philanthropy ~$10.6M (2022-23), SFF ~$3.8M, Good Ventures $1.9M, Founders Pledge $0.9M (https://www.longtermwiki.com/wiki/E47), not AI-lab pay-to-play. But CAIS director and senior HarmBench author Dan Hendrycks holds a paid xAI safety-advisor role ($1 salary, no equity) and co-founded Gray Swan AI, a commercial red-team/compliance vendor: a reported structural COI (https://www.piratewires.com/p/sb-1047-dan-hendrycks-conflict-of-interest), not shown to bias scores but worth disclosing.

**2. Methodology integrity:** HarmBench's Llama-2-13B judge classifier scored only 78.3% human agreement and a 26.8% false-positive rate vs. >90% for GPT-4/Llama-3-70B judges (https://arxiv.org/pdf/2404.01318, JailbreakBench/NeurIPS 2024). A March 2026 paper tested it directly under adversarial distribution shift and found near-random performance (~50%, "coin flip"), with high inter-judge agreement masking wrong verdicts (https://arxiv.org/html/2603.06594). A dated, quantified flaw in the scoring pipeline itself.

**3. Saturation:** Confirmed for its dominant single-turn mode. Defenses showing single-digit ASR under single-turn attacks fall to 70%+ under multi-turn human jailbreaks; newer multi-turn methods hit 80%+ within four turns (https://arxiv.org/pdf/2605.08778, https://arxiv.org/html/2508.07646). Low single-turn ASR is no longer a trustworthy safety signal.

**4. Gaming history:** No documented case of a vendor manipulating its own reported score. The classifier is exploitable via feedback-manipulation during attack optimization (ΔASR +0.48): a methodology gap, not a scandal.

**5. Staleness/liveness:** GitHub API confirms last code push 2024-08-16, no releases, 38 stale open issues, not archived (https://github.com/centerforaisafety/HarmBench). No live leaderboard exists. No single successor: the field fragmented into JailbreakBench, StrongREJECT, and 2026 extensions (GT-HarmBench, PluriHarms) rather than one maintained standard.

**Case FOR:** ICML 2024 peer-reviewed, 12 authors across multiple universities plus CAIS (https://arxiv.org/abs/2402.04249); still embedded in actively-maintained meta-frameworks: Stanford HELM Safety v1.0 (https://crfm.stanford.edu/2024/11/08/helm-safety.html) and the Future of Life Institute AI Safety Index through 2025 (https://futureoflife.org/ai-safety-index-summer-2025/). Trustworthy narrowly as a frozen, well-documented behavior taxonomy for same-time, same-judge, single-turn refusal comparisons, not as a live score or evidence of real-world jailbreak resistance.

VERDICT: caveat | HarmBench | Frozen since Aug 2024; own judge tested near-random in 2026; single-turn ASR misses multi-turn jailbreak reality.
