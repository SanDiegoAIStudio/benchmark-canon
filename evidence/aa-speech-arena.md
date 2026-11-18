## Vendor capture / funding
AA took a seed round from Nat Friedman/Daniel Gross's AI Grant (confirmed by founders, [Latent Space podcast, Jan 2026](https://www.latent.space/p/artificialanalysis)). Revenue = subscriptions + private benchmarking; "no one pays for the public leaderboard" and "no compensation for favorable listing" are both self-declared, not audited ([methodology](https://artificialanalysis.ai/text-to-speech/methodology)). No confirmed overlap between AA's investors and ranked TTS vendors, but PitchBook's full investor list 403'd, not fully closed.

## Contamination / methodology
Human-blind-voted Elo, not LLM-judge (avoids that bias class). Provider-voice tests sample from each vendor's own published voice catalog; prompt-bank disclosure/rotation is unconfirmed either way ([methodology](https://artificialanalysis.ai/text-to-speech/methodology)). Pairwise-Elo arenas as a class are proven riggable at ~1,000 targeted votes via model-fingerprinting ([arXiv](https://arxiv.org/abs/2501.07493)): same mechanism AA uses; no confirmed exploit against AA's Speech Arena specifically.

## Saturation (incl. cross-arena consensus)
AA's own numbers show #1/#2 with overlapping confidence intervals: Qwen-Audio-3.0-TTS-Plus 1236±17 vs Simba 3.2 1234±17, statistically tied ([AA on X](https://x.com/ArtificialAnlys/status/2077140161335631957)). #1 churned across 4+ models within months on AA's own feed (Inworld→Qwen→Simba→Fun-Realtime-TTS). A separate rival, TTS-AGI's "TTS Arena," shows zero top-4 overlap with AA (Vocu V3.0/Inworld TTS MAX top there, [leaderboard](https://tts-agi-tts-arena-v2.hf.space/leaderboard)), plausibly different candidate pools not fraud, but it kills sole-authority claims. Mid/lower-tier gaps are real; the #1 slot is noise.

## Gaming history
No confirmed gaming of the Speech Arena itself. AA's broader Intelligence Index has swapped benchmark components before (dropped MMLU-Pro/AIME/LiveCodeBench): an org-level stability flag, not TTS-specific. Speechify has run multiple PR placements touting its Speech-Arena #1 ([PRWeb](https://www.prweb.com/releases/speechifys-simba-3-2-ranks-1-on-independent-artificial-analysis-tts-leaderboard-worlds-best-real-time-voice-model-above-elevenlabs-openai-google-deepmind--others-302819731.html)): motive for vendor influence exists, no rigging method confirmed.

## Staleness / liveness
"4x daily, random times" refresh is confirmed on AA's own methodology page; July 2026 numbers are live and current, matching the prior "multiple-daily refresh" claim.

## Case FOR
Genuinely human-judged (not self-graded), cost-normalized (price/1M chars), published methodology naming an outside academic advisor (Prof. Shinji Watanabe, CMU), real 4x/day refresh, and clean mid/bottom-tier separation. Trustworthy for "is vendor X roughly competitive at this price", not for crowning a definitive #1.

VERDICT: caveat | Artificial Analysis Speech Arena | Human-voted, cost-normalized, refreshes 4x/daily; but #1/#2 statistically tied, funding self-disclosed only, rival arena disagrees entirely.
