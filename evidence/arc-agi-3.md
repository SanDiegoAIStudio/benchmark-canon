**Vendor capture.** ARC Prize Foundation co-founders Chollet & Knoop self-funded $1.1M, but the single largest donor is Ndea ($2M): their OWN for-profit AGI lab, whose research bet is explicitly informed by ARC-AGI results (https://arcprize.org/donate, https://www.startuphub.ai/ai-news/claudes-corner/2026/claudes-corner-ndea-yc-w2026). Additional funders whose own models get scored: xAI $1M, Google $100K, Y Combinator $500K (https://arcprize.org/donate). Mitigants: disclosed donor list, published no-influence policy, $10K/run eval cap, external academic panel (NYU/UCLA/Santa Fe/Columbia) (https://arcprize.org/policy): real, but self-administered.

**Methodology/contamination.** Predecessors ARC-AGI-1/2 both showed documented leakage: Gemini 3's unprompted chain-of-thought used correct ARC color-mappings, evidence the format was memorized (https://labs.adaline.ai/p/what-is-the-arc-agi-benchmark-and). V3's own preview self-reported real gaming: some games "brute-forced without reasoning," replay logs ballooning to tens of GB from exploit loops (https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings): transparent disclosure, but confirms the new format isn't gaming-proof either.

**Saturation.** Best official (no-harness) score ~7.8-13% (GPT-5.6 Sol Max) vs 100% human, aggregator-updated 2026-07-13 (https://benchlm.ai/benchmarks/arcAgi3), up from ~0.37-0.51% at March launch (https://arcprize.org/blog/arc-agi-3-launch). Nowhere near ceiling: still discriminates.

**Gaming/scaffold gap.** Official rules ban custom harnesses specifically to prevent gaming (https://arcprize.org/policy), yet a self-reported community board reaches 58% and a third-party harness claims ~99% on the 3 public games (https://schema-harness.github.io/): the <8% headline is largely a scaffolding ceiling, not a clean read of raw model capability.

**Category mismatch.** Its own paper calls ARC-AGI-3 "a fundamental shift away from traditional language model evaluation": POMDP agent exploration in game environments, not chat/dialogue (https://www.emergentmind.com/papers/2603.24621). Filing it as chat-model evidence misrepresents what it tests.

**Liveness.** Launched 2026-03-25 (https://arcprize.org/blog/arc-agi-3-launch), active competition through Sept 30 milestone, third-party leaderboard current as of 2026-07-13: fresh.

**Case FOR.** Real, live, transparent about its own flaws, adversarially redesigned after documented v1/v2 contamination, and still cleanly separates every frontier model from humans. Trustworthy as evidence of a long-horizon interactive-agent reasoning gap, NOT as chat-model evidence, and cite only the no-harness official score, never the community/harness-inflated numbers.

VERDICT: caveat | ARC-AGI-3 | Live and unsaturated but founder-run for-profit is top funder; predecessor contamination history; tests agentic play not chat model output.
