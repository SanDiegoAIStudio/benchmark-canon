## Arena (LMArena) Text Leaderboard: Adversarial Verification

**Vendor capture/funding**: $150M Series A confirmed: Jan 6 2026 close, $1.7B valuation, led by Felicis + UC Investments; a16z, Kleiner Perkins, Lightspeed, House Fund, LDVP, Laude also participated (prnewswire.com/news-releases/lmarena-raises-150-million-to-build-the-worlds-most-trusted-ai-evaluation-platform-302653012.html; cooley.com/news/coverage/2026/2026-01-06-lmarena-secures-$150-million-series-a). "Investors unconfirmed" was stale: they're named. a16z also led the 2025 seed (a16z.com/announcement/investing-in-lmarena-the-reliability-layer-for-ai) and holds stakes across labs LMArena ranks; a16z's own post names "neutrality under commercial pressure" as the live risk. LMArena's monetization path, selling eval/data access to labs it ranks, is an externally flagged structural conflict (research.contrary.com/company/lmarena).

**Contamination/methodology**: arXiv 2504.20879 (v2, 2025-05-12) documented Meta pre-testing 27 private Llama-4 variants plus closed-model sampling favoritism. LMArena's rebuttal (arena.ai/blog/our-response) disputes the open-weight-share stat and calls a pre-release-boost chart "a simulation": never denies the 27-variant testing. Live check today (arena.ai/leaderboard/text): #1 shows 8,819 votes vs #2-5's 48K-65K, matching the paper's under-sampled-new-entrant warning, live. A real fix landed 2026-05-12: direct-chat-to-battle conversion plus Bradley-Terry corrections for position/same-org bias (arena.ai/blog/leaderboard-changelog), but breaks pre/post-May comparability.

**Saturation**: Live top-10 spread = 21 Elo (1507→1486), matching the ~20-Elo prior. Adjacent CIs mostly overlap; #1 vs #10 barely doesn't. Frontier rank-order is near-noise; the full 376-model/7.3M-vote range still separates strong from weak broadly.

**Gaming history**: Confirmed, not alleged. Meta's chat-tuned "Llama-4-Maverick-03-26-Experimental" ranked #2; released weights hit #32 (theregister.com/2025/04/08/meta_llama4_cheating; dig.watch/updates/lmarena-tightens-rules-after-llama-4-incident). LeCun confirmed 2026-01-02 results were "fudged."

**Staleness**: Verified live: "Last Updated: July 16, 2026," 7,348,702 votes, 376 models (arena.ai/leaderboard/text). Current.

**FOR**: Largest live human-preference sample in the industry, published changelog, real 2026-05-12 bias fixes, rebuts criticism with data not silence. Trustworthy for broad market-position signal at scale, not for precise top-10 frontier ordering or any single vendor-submitted score at face value.

VERDICT: caveat | Arena (LMArena) Text Leaderboard | Confirmed gaming precedent + VC conflicts + frontier saturation; live/current/largest-sample: use for broad tiering, not top-10 rank
