**Vendor capture:** Multi-university confirmed: OSWorld 2.0 authors span HKU XLANG Lab (lead), UC San Diego, Columbia, UC Santa Barbara, Mila (arxiv.org/abs/2606.29537), funded by the "Google Research gift fund" per the official site. OSWorld-Verified's 2025 redesign explicitly credits "feedback" from Anthropic, OpenAI, ByteDance Seed TARS, and MoonShot AI (xlang.ai/blog/osworld-verified), and on that same leaderboard, all top 3 spots are now Claude models (Fable 5 85.0%, Mythos 5 85%, Opus 4.8 83.4%, llm-stats.com/benchmarks/osworld-verified). Feedback isn't funding, but the vendor sweeping the podium helped shape the eval redesign that produced it.

**Methodology/contamination:** OSWorld 2.0 grading is 88.5% deterministic functional checks, 11.5% "objective binary" model-based checks, with reward-hacking audits built into task design (arxiv.org/abs/2606.29537). Tasks/gold data live in a gated HuggingFace dataset, not raw public files: tighter than the predecessor. Train-on-test risk is plausible but unconfirmed: tasks have lived in public GitHub/HF repos since 2024.

**Gaming history:** Berkeley RDI's BenchJack (April 2026) scored 73% on the 369-task OSWorld/-Verified via wget'd public gold files, eval()-on-agent-string code execution, and VM state manipulation: zero real tasks solved (rdi.berkeley.edu/blog/trustworthy-benchmarks-cont). The claimed "patched to unhackable" is BenchJack's own remediation demo, not a confirmed upstream fix: a live GitHub issue dated 2026-07-02 still shows predictably-named gold files (39_2_Gold.pptx) in the public repo (github.com/xlang-ai/OSWorld/issues/532), and the repo has zero published security advisories.

**Saturation:** OSWorld-Verified's top 3 models cluster within 1.6 points: saturated (benchlm.ai/benchmarks/osWorldVerified). OSWorld 2.0's best frontier system hits only 20.6% binary/54.8% partial at 500 steps: genuinely discriminating (snorkel.ai/leaderboard/os-world-2-0).

**Liveness:** Confirmed live via GitHub API: OSWorld pushed 2026-07-16, OSWorld-V2 pushed 2026-07-09, both with active recent PRs.

**Case for:** OSWorld 2.0 itself, fresh, majority-deterministic, wide headroom, real multi-university governance, disclosed-agent-code verification track, no confirmed break yet, is trustworthy for gauging long-horizon computer-use capability. The legacy -Verified 85% headline should not be cited without the unpatched-exploit caveat.

VERDICT: caveat | OSWorld 2.0 / OSWorld-Verified | OSWorld 2.0 discriminates and is live; -Verified branch is saturated and its BenchJack-exploited gold files remain unpatched.
