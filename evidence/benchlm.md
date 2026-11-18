## BenchLM.ai: Adversarial Verification

**(1) Vendor capture/funding.** Run by one person, with no institutional or lab backing found. Site sells paid placement: $1,500 "pilot," $2,500/mo "Category Partner," $4-6K "Research Partner" tiers on comparison/pricing pages (https://benchlm.ai/advertise). It self-declares "sponsors cannot buy a score, a rank, benchmark inclusion": an unaudited, self-policed claim with no outside check. Real conflict surface; no abuse documented.

**(2) Contamination/methodology.** Pure aggregator of vendor self-reported numbers (model cards, launch posts, OpenBench, public leaderboards): no independent re-running of evals, and the methodology page explicitly has nothing on train-on-test contamination or gaming checks (https://benchlm.ai/methodology, https://benchlm.ai/about). The composite score also folds in undisclosed-weight "bounded external consensus calibration" (arena-style signals) for coding/agentic/overall ordering: a second opaque layer atop vendor numbers. Mitigant: four-tier provenance tags (official/verified/reported/estimated) let users filter to verified-only.

**(3) Saturation.** Composite top-10 (7/17/26) spreads 83.93→72.84: real frontier separation, not saturated (https://benchlm.ai/). Site itself flags HumanEval/BBH "StaleSaturated" while versioning harder tests (FrontierMath v2, LiveCodeBench v5): self-aware curation, unverified for rigor site-wide.

**(4) Gaming history.** No documented case of BenchLM being gamed or manipulated found; only one SEO-directory review ("coverage of latest releases can lag slightly") and one GitHub list consuming its feed. Thin evidence either direction: unconfirmed, not clean.

**(5) Staleness/liveness.** Genuinely active: three independently fetched pages (home/benchmarks/data) all stamp 7/17/26 with a model roster matching the current frontier set. But /about contains a **within-page self-contradiction**: intro prose says "107 benchmarks," the footer counter on the *same page* says "316" (https://benchlm.ai/about): confirms the prior "stale sub-pages" signal is real, and worse than cross-page (it's uncorrected copy sitting next to live data).

**Case for:** Usable as a fast, provenance-tagged directional snapshot of frontier standings if filtered to "verified" rows, not as a primary or audited source.

VERDICT: caveat | BenchLM.ai | Solo aggregator, no independent recompute/contamination check, unaudited ad firewall, confirmed within-page stale copy; still discriminates at frontier.
