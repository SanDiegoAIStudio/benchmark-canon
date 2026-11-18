**Vendor capture**: TTS-AGI's HF org (233 followers, 36 members) is largely staffed by current/former Hugging Face employees: Clémentine Fourrier (leads HF's leaderboard team), Thomas Wolf (HF co-founder), Omar Sanseviero, Vaibhav Srivastav, Pedro Cuenca, Yoach Lacombe (https://huggingface.co/TTS-AGI). No paid-placement evidence found; models enter via public community/vendor requests (50+ open Discussions threads, e.g. #113 "Model Request Qwen-3-TTS," unresolved), so coverage is submission-gated, not comprehensive: Qwen isn't on the live board. Artificial Analysis runs a separate, unaffiliated Speech Arena (https://artificialanalysis.ai/text-to-speech/arena) that had Qwen-Audio-3.0-TTS-Plus at #1 while TTS-AGI's #1 was CastleFlow/Inworld: confirming disagreement, though partly a catalog-coverage artifact, not a clean same-models clash.

**Methodology**: Single ≤1000-char English-only blind human A/B, no LLM judge (https://docs.ttsarena.org/), avoids that bias vector, but short single-line voting rewards theatrical delivery: current #1 CastleFlow is described as sounding like "a movie trailer narrator" (theneuron.ai), a construct-validity gap versus real deployment fitness (audiobooks, IVR, etc.).

**Saturation**: Live pull today (https://tts-agi-tts-arena-v2.hf.space/api/leaderboard) shows the top ~10 models bunched within 30 Elo points with overlapping uncertainty bands (#1 CastleFlow 1562±19 vs #2 Inworld TTS MAX 1560±20): statistically noisy at the frontier, though clean separation from the bottom tier (Veena 1366, Wordcab 1363) persists.

**Gaming, confirmed, current**: That same live API shows Vocu V3.0 held Elo 1565 (would rank #1) on 1,448 votes, reportedly #1 since ~March 2026, before being suspended 2026-07-03 for "suspected vote manipulation", a flag visible only in raw API output, no public writeup found anywhere. Proves the vote-integrity layer is beatable and wasn't disclosed proactively.

**Liveness**: V2 is genuinely current (Space updated ~14 days ago per huggingface.co/TTS-AGI); V1/Legacy is explicitly frozen and read-only, so no stale-masquerading-as-live risk once pointed at the correct V2 URL.

**Case FOR**: Coarse tiering (good vs. mediocre vs. bad TTS, shortlist-building) remains trustworthy: bottom-tier separation holds, the manipulation was eventually caught and suspended, and no vendor pay-for-placement was found. Not trustworthy for fine #1-vs-#5 claims or as a complete model census.

VERDICT: caveat | TTS Arena V2 | Live human-blind Elo, but a manipulated model held #1 undetected for months; top-10 is statistically noisy.
