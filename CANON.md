# The Benchmark Canon

Checked 2026-07-17.
The refuter round checked 51 (47 with a caveat, 4 cut); Deep SWE was vetted separately and also carries a caveat

- canon: cite plain. No benchmark has earned it.
- caveat: cite with the caveat.
- cut: do not cite.

Produced by AI agents (Claude) with web access: one refuter per benchmark, one judge per category.

## The eleven primaries

| Category | Primary | Rule |
| --- | --- | --- |
| Composite indices | [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) | Cite with the funding-gap caveat attached, not hidden. |
| Chat / reasoning models | [LiveBench](https://livebench.ai/) | Cite livebench.ai directly: never mirrors (stale-aggregator artifacts documented). |
| Coding + software agents | [Terminal-Bench 2.x](https://www.tbench.ai/) | Always pin the score source (tbench.ai vs Artificial Analysis diverge); never a bare number. |
| Agentic / computer-use | [METR Time Horizon](https://metr.org/time-horizons/) | Cite the trend, never one point; 20-35% methodology swings are known-magnitude. |
| Search / research engines | [Deep Research Bench (FutureSearch)](https://futuresearch.ai/deep-research-bench/) | Disclose its Anthropic investor/client tie in the footnote; never bare-cite the name (collision with USTC's bench). |
| Aggregators | [Epoch AI Benchmarking Hub / ECI](https://epoch.ai/benchmarks) | Footnote out FrontierMath (COI history) and SWE-bench Verified (kept despite contamination) when citing. |
| Image generation | [Arena.ai Image/Video Arenas](https://arena.ai/leaderboard/text-to-image) | High-vote entries only; say 'human-voted, gameable', never 'verified' or 'independent'. |
| Video generation | [Artificial Analysis Video Arena](https://artificialanalysis.ai/video/arena) | Exclude anonymous entrants (HappyHorse-class); re-pull the live entrant list at each rebuild. |
| Voice (TTS / STT) | [Artificial Analysis Speech Arena](https://artificialanalysis.ai/text-to-speech/arena) | Directional only: top-2 statistically tied and the rival arena disagrees entirely; never a bare #1. |
| Documents / OCR | [OCRBench v2](https://99franklin.github.io/ocrbench_v2/) | Disclose the self-reported-score caveat; ByteDance co-authorship disclosed when citing ByteDance-adjacent tools. |
| Safety / red-teaming | [AgentHarm](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) | Stamp 'judge/content frozen 2024'; 2026 frontier discrimination unconfirmed. |

## The ledger, by category

### Composite indices

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) | caveat | Live, transparent, anti-gaming methodology; but funding/ownership stays off-site and payer/rated conflict undisclosed formally. | [evidence](evidence/aa-index.md) | [memo](memos/composite.md) |
| [GDPval / GDPval-AA v2](https://openai.com/index/gdpval/) | caveat | OpenAI owns/authors the task corpus and self-judges via GPT-5.5; ~30% grading noise; top-2 gap is statistical noise. | [evidence](evidence/gdpval.md) | [memo](memos/composite.md) |

### Chat / reasoning models

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [ARC-AGI-2](https://arcprize.org/leaderboard) | caveat | Well-governed but semi-private track admits overfitting risk; chat-model frontier already exceeds human baseline (92.5% vs ~60%). | [evidence](evidence/arc-agi-2.md) | [memo](memos/chat-model.md) |
| [ARC-AGI-3](https://arcprize.org/competitions/2026/arc-agi-3) | caveat | Live and unsaturated but founder-run for-profit is top funder; predecessor contamination history; tests agentic play not chat model output. | [evidence](evidence/arc-agi-3.md) | [memo](memos/chat-model.md) |
| [Arena (LMArena) Text Leaderboard](https://arena.ai/leaderboard/text) | caveat | Confirmed gaming precedent + VC conflicts + frontier saturation; live/current/largest-sample: use for broad tiering, not top-10 rank | [evidence](evidence/arena-text.md) | [memo](memos/chat-model.md) |
| [FACTS Benchmark Suite](https://www.kaggle.com/benchmarks/google/facts) | caveat | Google builds/hosts/self-judges via owned Kaggle; Gemini judges 2/4 legs; usable as relative signal only, not proof of superiority | [evidence](evidence/facts-suite.md) | [memo](memos/chat-model.md) |
| [FrontierMath](https://epoch.ai/frontiermath) | caveat | OpenAI funded+saw problems undisclosed till launch; 42% error rate fixed only June 2026; self-reported scores proven inflated 2.5x. | [evidence](evidence/frontiermath.md) | [memo](memos/chat-model.md) |
| [GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond) | caveat | Saturated at frontier (93-95%, cross-tracker noise ≈ model spread); creators' own group says top scores partly reflect predicting flawed answers. | [evidence](evidence/gpqa-diamond.md) | [memo](memos/chat-model.md) |
| [Humanity's Last Exam](https://agi.safe.ai/) | caveat | Meta owns 49% of Scale/HLE; Meta's model ranks on it; ~29% bio/chem error rate confirmed: still discriminates, disclose ties. | [evidence](evidence/hle.md) | [memo](memos/chat-model.md) |
| [LiveBench](https://livebench.ai/) | caveat | Live, objective, no-LLM-judge scoring at the source; single-vendor funder, no COI disclosure; cite livebench.ai directly, not stale mirrors. | [evidence](evidence/livebench.md) | [memo](memos/chat-model.md) |
| [MMLU-Pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) | caveat | Saturated at frontier (4 trackers, 4 different #1s, \<2pt spread); legit academic origin, static 2yr set, no gaming found. | [evidence](evidence/mmlu-pro.md) | [memo](memos/chat-model.md) |
| [Scale AI SEAL / SEAL Showdown](https://labs.scale.com/leaderboard) | caveat | Meta owns 49%+its Chief AI Officer sits on Scale's board scoring his own lab's models; sound stats, no confirmed rigging yet. | [evidence](evidence/seal-showdown.md) | [memo](memos/chat-model.md) |
| [SimpleBench (AI Explained)](https://simple-bench.com/) | caveat | Live, dual-mirrored, but near-saturated (81.9 vs 83.7 human), n=9 baseline, undisclosed grading method, prompting-sensitive. | [evidence](evidence/simplebench.md) | [memo](memos/chat-model.md) |
| [SimpleQA Verified](https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified) | caveat | Google creates, hosts, and currently tops its own leaderboard; treat as directional signal, not neutral ranking. | [evidence](evidence/simpleqa-verified.md) | [memo](memos/chat-model.md) |

### Coding + software agents

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Aider Polyglot Leaderboard](https://aider.chat/docs/leaderboards/) | caveat | Sound execution-graded methodology, no capture, but stale since Oct 2025: missing all 2026 frontier models | [evidence](evidence/aider-polyglot.md) | [memo](memos/coding.md) |
| [Deep SWE (Data Curve)](https://deepswe.datacurve.ai) | caveat | Real gains but self-graded flagship claim, confirmed cost bug, 4 broken golds, vendor-sales conflict, early re-saturation. | [evidence](evidence/deep-swe.md) | [memo](memos/coding.md) |
| [LiveCodeBench](https://livecodebench.github.io/leaderboard.html) | caveat | Problem pool frozen since Apr 2025, self-reported scores, near-saturated top tier; use as historical snapshot only. | [evidence](evidence/livecodebench.md) | [memo](memos/coding.md) |
| [Terminal-Bench 2.x](https://www.tbench.ai/) | caveat | Real leaderboard cheating + unpatched harness exploit found; still discriminates: must name score source (tbench.ai vs AA diverge). | [evidence](evidence/terminal-bench.md) | [memo](memos/coding.md) |
| [SWE-bench Pro](https://labs.scale.com/leaderboard/swe_bench_pro_public) | cut | Live Meta 49% COI scoring its own model, OpenAI retracted its endorsement over 30% broken tasks, unpatched reward-hacking exploit. | [evidence](evidence/swe-bench-pro.md) | [memo](memos/coding.md) |
| [SWE-bench Verified](https://www.swebench.com) | cut | Funder's own audit proved contamination+broken tests; 3 gaming incidents; frontier-saturated; successor also retracted. | [evidence](evidence/swe-bench-verified.md) | [memo](memos/coding.md) |

### Agentic / computer-use

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Cybench](https://cybench.github.io/) | caveat | Saturated at frontier (near-100%), documented flag-fetching cheats, self-reported leaderboard; still valid as sub-frontier floor gate. | [evidence](evidence/cybench.md) | [memo](memos/agentic.md) |
| [METR Time Horizon](https://metr.org/time-horizons/) | caveat | Self-admitted frontier saturation, on-suite reward-hacking, 20-35% methodology-driven swings; still best macro-trend reference. | [evidence](evidence/metr-time-horizon.md) | [memo](memos/agentic.md) |
| [OSWorld 2.0 / OSWorld-Verified](https://os-world.github.io/) | caveat | OSWorld 2.0 discriminates and is live; -Verified branch is saturated and its BenchJack-exploited gold files remain unpatched. | [evidence](evidence/osworld-2.md) | [memo](memos/agentic.md) |
| [tau2-bench](https://github.com/sierra-research/tau2-bench) | caveat | Owner's CEO chairs OpenAI's board, Google GV invests; open+pass^k discriminate, but pin version, skip aggregators. | [evidence](evidence/tau2-bench.md) | [memo](memos/agentic.md) |
| [Vending-Bench 2](https://andonlabs.com/evals/vending-bench-2) | caveat | Unsaturated, actively updated, but single-operator harness with real lab-funding COI and no independent replication. | [evidence](evidence/vending-bench-2.md) | [memo](memos/agentic.md) |
| [WebArena-Verified](https://webarena.dev/) | caveat | ServiceNow-run; BenchJack never retested it; raw gold-answer file still shipped; near-zero adoption; unverified since Mar 2026. | [evidence](evidence/webarena-verified.md) | [memo](memos/agentic.md) |
| [GAIA](https://huggingface.co/spaces/gaia-benchmark/leaderboard) | cut | Grader exploited to ~98% (Berkeley RDI, Apr 2026); HAL paused; creators shipped GAIA2 successor; no clean citable split. | [evidence](evidence/gaia.md) | [memo](memos/agentic.md) |

### Search / research engines

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Arena Search Arena](https://arena.ai/leaderboard/search) | caveat | Only live search arena found; but paid lab-optimization revenue + admitted org-bias + 9-way tie below #1. | [evidence](evidence/search-arena.md) | [memo](memos/search.md) |
| [BrowseComp](https://leaderboard.steel.dev/leaderboards/browsecomp/) | caveat | Self-reported scores dominate; Anthropic found a model decrypting the answer key; use only for coarse ranking. | [evidence](evidence/browsecomp.md) | [memo](memos/search.md) |
| [Deep Research Bench (FutureSearch)](https://futuresearch.ai/deep-research-bench/) | caveat | Frozen-corpus, non-saturated, no gaming found; but lead investor + clients include labs it ranks, esp. Anthropic. | [evidence](evidence/futuresearch-drb.md) | [memo](memos/search.md) |
| [DeepResearch Bench (USTC)](https://deepresearch-bench.github.io/) | caveat | Active & unsaturated, but judge=contestant self-preference (Gemini→now GPT-5.5) and rampant collision with FutureSearch's same-named bench | [evidence](evidence/deepresearch-bench-ustc.md) | [memo](memos/search.md) |
| [FreshQA](https://github.com/freshllms/freshqa) | cut | Cadence dead 11+ wks past self-set date; core search-vs-memorization signal empirically broken (74.3%); Google self-grades own model. | [evidence](evidence/freshqa.md) | [memo](memos/search.md) |

### Image generation

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Arena.ai Image/Video Arenas](https://arena.ai/leaderboard/text-to-image) | caveat | Live+discriminates at top, but pay-to-be-ranked conflict + proven deanonymization exploit; trust only high-vote entries. | [evidence](evidence/arena-media.md) | [memo](memos/image.md) |
| [Artificial Analysis Image Arena](https://artificialanalysis.ai/image/arena) | caveat | Live + published Elo methodology, but demonstrated de-anonymization exploit and paid private-benchmarking ties to ranked labs warrant caution. | [evidence](evidence/aa-image-arena.md) | [memo](memos/image.md) |

### Video generation

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Artificial Analysis Video Arena](https://artificialanalysis.ai/video/arena) | caveat | Real blind-vote methodology, no-pay-for-rank disclosure, but anonymous/unverified entrants (HappyHorse) rank top-5; re-verify live, exclude unverified models. | [evidence](evidence/aa-video-arena.md) | [memo](memos/video.md) |
| [VBench / VBench-2.0](https://vchitect.github.io/VBench-project/) | caveat | Academic, no vendor-pay found; v1 saturating, board stale since Apr 2026, circulating numbers often vendor self-reported. | [evidence](evidence/vbench-2.md) | [memo](memos/video.md) |

### Voice (TTS / STT)

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [Artificial Analysis Speech Arena](https://artificialanalysis.ai/text-to-speech/arena) | caveat | Human-voted, cost-normalized, refreshes 4x/daily; but #1/#2 statistically tied, funding self-disclosed only, rival arena disagrees entirely. | [evidence](evidence/aa-speech-arena.md) | [memo](memos/voice.md) |
| [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) | caveat | NVIDIA co-authors methodology its own models top; AMI gaming (Jul 2026) exceeds leading margin; private-eval fix is opt-in, not default. | [evidence](evidence/open-asr.md) | [memo](memos/voice.md) |
| [TTS Arena V2](https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2) | caveat | Live human-blind Elo, but a manipulated model held #1 undetected for months; top-10 is statistically noisy. | [evidence](evidence/tts-arena-v2.md) | [memo](memos/voice.md) |
| [Voice Arena (voicearena.com)](https://voicearena.com/) | caveat | Live, methodologically rigorous, vendor-independent (academic-funded); but ~4 months old, thin team, no disclosed vote-scale or audit. | [evidence](evidence/voice-arena.md) | [memo](memos/voice.md) |

### Documents / OCR

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [OCR Arena](https://www.ocrarena.ai/leaderboard) | caveat | Vendor-operated by Extend, YC-investor-amplified, undisclosed vote volumes, formatting-biased crowd votes; still discriminates, cross-checkable via idp-leaderboard. | [evidence](evidence/ocr-arena.md) | [memo](memos/docs.md) |
| [OCRBench v2](https://99franklin.github.io/ocrbench_v2/) | caveat | Self-reported/0-verified scores + ByteDance co-authorship; still unsaturated + peer-reviewed + genuinely refreshed, use with disclosure. | [evidence](evidence/ocrbench-v2.md) | [memo](memos/docs.md) |
| [OmniDocBench](https://github.com/opendatalab/OmniDocBench) | caveat | Self-reported-only leaderboard (0/16 verified), operator's own MinerU tops it, saturated top cluster; floor test only, not ranking. | [evidence](evidence/omnidocbench.md) | [memo](memos/docs.md) |

### Safety / red-teaming

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [AgentHarm](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) | caveat | Solid methodology/contamination controls, actively maintained infra, but frozen 2024 judge/content and unconfirmed 2026 frontier discrimination. | [evidence](evidence/agentharm.md) | [memo](memos/safety.md) |
| [HarmBench](https://arxiv.org/abs/2402.04249) | caveat | Frozen since Aug 2024; own judge tested near-random in 2026; single-turn ASR misses multi-turn jailbreak reality. | [evidence](evidence/harmbench.md) | [memo](memos/safety.md) |
| [Phare LLM Benchmark](https://phare.giskard.ai/) | caveat | Self-authored methodology + Anthropic-family judge seat + paid-audit vendor motive; still discriminates, govt-funded, actively updated. | [evidence](evidence/phare.md) | [memo](memos/safety.md) |

### Aggregators

| Benchmark | Verdict | Caveat | Evidence | Memo |
| --- | --- | --- | --- | --- |
| [BenchLM.ai](https://benchlm.ai/about) | caveat | Solo aggregator, no independent recompute/contamination check, unaudited ad firewall, confirmed within-page stale copy; still discriminates at frontier. | [evidence](evidence/benchlm.md) | [memo](memos/aggregator.md) |
| [Epoch AI Benchmarking Hub / ECI](https://epoch.ai/benchmarks) | caveat | OpenAI-funded FrontierMath COI (disclosed late) plus SWE-bench Verified kept in ECI after OpenAI called it contaminated. | [evidence](evidence/epoch-hub.md) | [memo](memos/aggregator.md) |
| [HAL (Holistic Agent Leaderboard)](https://hal.cs.princeton.edu/) | caveat | Independent, not vendor-captured, but frozen since Jul 2026 and published rankings shown statistically unreliable by outside analysis. | [evidence](evidence/hal-princeton.md) | [memo](memos/aggregator.md) |
| [llm-stats.com](https://llm-stats.com/) | caveat | Owner traceable (ZeroEval/YC S25); blended score sane but LiveBench subpage confirmed stale (o3-mini #1); undisclosed Google-backer conflict. | [evidence](evidence/llm-stats.md) | [memo](memos/aggregator.md) |
| [OpenRouter Rankings](https://openrouter.ai/rankings) | caveat | Token-volume telemetry, not quality; misleading copy, gameable via free-tier promos, Alphabet a material investor: label as adoption signal. | [evidence](evidence/openrouter-rankings.md) | [memo](memos/aggregator.md) |
| [Vellum LLM Leaderboard](https://www.vellum.ai/llm-leaderboard) | caveat | VC-funded, model-agnostic aggregator; real data but no published methodology, and still headlines contaminated/disavowed SWE-bench: treat as directory, not authority. | [evidence](evidence/vellum-board.md) | [memo](memos/aggregator.md) |

## Voids nobody measures

- SMB SaaS tools: NO independent capability benchmark exists (Salesforce grades itself; G2 bought Capterra + Software Advice + GetApp Feb 2026: one pay-to-play owner).
- Run-to-run reliability: nobody measures consistency across repeated runs: the thing an operator experiences as trustworthy. tau2-bench's pass^k is the lone partial exception.
- Human-oversight cost: capability-per-dollar exists; check-its-work time is measured nowhere. Princeton HAL's cost axis was closest and is now frozen.
- AI-search accuracy: no credible independent study since Columbia Tow Center (Mar 2025, all-eight-bad). Every circulating percentage is SEO/vendor content.
- Voice-cloning fidelity: no neutral benchmark isolates clone similarity; every '#1 at cloning' claim is vendor marketing.
- Safety currency: no continuously-updated public safety leaderboard exists the way capability ones do: 'is it safe' is structurally less visible to a buyer than 'is it smart'.

## Standing citation rules

1. Primary sources are the citation of record; SEO aggregators (benchlm / llm-stats / localaimaster class) are discovery-only.
2. Composites beat single benches, but know the components: a rotten ingredient (FrontierMath, SWE-bench Verified in ECI) taints the blend silently.
3. NAME THE HARNESS on any agent or coding score: on Terminal-Bench the same model scored 58% in one harness and 75 to 82% in others (Theo Browne, t3.gg, "Did Claude really get dumber again?", 2026-04-20, https://www.youtube.com/watch?v=KFisvc-AMII).
4. Adoption is not quality: OpenRouter volume is telemetry; AA's #1 ranks #7 by usage.
5. A vendor's own model leading the vendor's own benchmark is never evidence (Google/FACTS+SimpleQA-Verified, OpenAI/GDPval, MinerU/OmniDocBench, NVIDIA/Open-ASR).
6. Arenas: high-vote, named entrants only; call them 'human-voted, gameable', never 'independent'.
7. Stamp every citation 'as of \<date>'; frozen boards (Aider Oct 2025, LiveCodeBench Apr 2025, VBench Apr 2026, HAL Jul 2026) are archival, not current.
8. Never a bare #1: frontier gaps sit inside statistical noise on nearly every board (top-10 within ~20 Elo on Arena; 4 trackers, 4 different MMLU-Pro leaders).
9. Disclose the named caveat every time a canon benchmark is cited: the caveat IS the trust layer.
10. Saturated benchmarks demote to floor-gates (Cybench, MMLU-Pro, GPQA): 'passes the floor' is meaningful, ranking is not.
11. Re-vet cadence: coding quarterly at minimum (the succession pattern: Verified -> Pro -> Deep SWE each re-developed the same failure), everything else semi-annually, any benchmark on a funding/ownership change immediately.

## Sources this canon leans on

- **Artificial Analysis**: most cross-cited composite; funding undisclosed: caveat carried on every cite
- **Epoch AI**: most transparent tiering; FrontierMath COI history; slow to prune its own composite
- **METR**: predeployment access to 4 labs; funding undisclosed
- **ARC Prize Foundation**: discloses lab donors: the disclosure practice is the differentiator
- **Theo Browne (t3.gg)**: usage-grounded commentary; the name-the-harness rule follows his Terminal-Bench comparison
- **AI Explained / SimpleBench**: rigor-tier YouTuber; own bench near-saturated (n=9 baseline caveat)
- **Zvi Mowshowitz · Nathan Lambert · Simon Willison**: independent practitioner cross-checks; no lab affiliation
- **Vals AI**: cleanest independence profile among domain-specific evaluators (legal/tax/finance)
