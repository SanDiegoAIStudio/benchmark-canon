# AgentHarm: Adversarial Verification

**Vendor capture (1):** Built by UK AISI (renamed AI Security Institute, Feb 2025) with Gray Swan AI [arxiv.org/abs/2410.09024]. Gray Swan is VC-backed ($40M Series A) and sells red-teaming-as-a-service (Cygnal/Shade) plus paid Arena competitions to the same frontier labs AgentHarm scores: the harm-benchmark's co-owner also sells harm-discovery/defense products to the graded labs [grayswan.ai/news/gray-swan-announces-series-a]. Structural conflict, not proven manipulation.

**Contamination/methodology (2):** Real safeguards: behaviors withheld from public release, canary GUID, a private set never exposed to public APIs [huggingface.co/datasets/ai-safety-institute/AgentHarm]. But grading isn't purely deterministic: I confirmed directly in the maintained scorer code that the default judge is hardcoded `openai/gpt-4o-2024-08-06`: a 2024 model grading 2026 frontier transcripts by default (overridable, but the repo default hasn't moved) [github.com/UKGovernmentBEIS/inspect_evals, src/inspect_evals/agentharm/scorer.py]. Self-documented limits: English-only, single-turn attacks only [arxiv.org/abs/2410.09024].

**Saturation (3):** 2024 launch showed real separation (GPT-4o/Claude 3.5 Sonnet 48-85% refusal, collapsing under simple jailbreaks). No 2026 GPT-5.x/Opus/Gemini-3 AgentHarm numbers surfaced in search or in Anthropic's Opus 4.8 card. 2026 successor benchmarks exist specifically because AgentHarm-class synthetic single-turn tool-call setups miss "Execution Hallucination": verbal refusal while the harmful action already ran [arxiv.org/abs/2605.10779, LITMUS, June 2026].

**Gaming (4):** No documented case of AgentHarm itself being gamed. Adjacent literature shows frontier models increasingly detect they're being evaluated: a class risk, not benchmark-specific evidence.

**Staleness (5):** Task content frozen since 2024 (partial release, "hope to release more" unfulfilled); HF namespace still reads `ai-safety-institute`, unchanged post-rebrand. Infra IS actively maintained, commits touching the AgentHarm scorer as recently as 2026-07-02 and 2026-07-08 [github.com/UKGovernmentBEIS/inspect_evals], content and judge model are frozen, plumbing is not.

**Strongest case FOR:** Sound benign/harmful task pairing, genuine held-out set, ICLR 2025 peer review, still the shared taxonomy 2026 successor papers build on: trustworthy as a comparative/historical research baseline, not as a live current-frontier safety leaderboard.

VERDICT: caveat | AgentHarm | Solid methodology/contamination controls, actively maintained infra, but frozen 2024 judge/content and unconfirmed 2026 frontier discrimination.
