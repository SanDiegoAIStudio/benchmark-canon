# OCR Arena: Adversarial Verification

**1. Vendor capture / funding / conflicts.** OCR Arena is built and operated by Extend (extend.ai), a document-processing-AI startup. Extend raised $17M seed+Series A led by Innovation Endeavors, with **Y Combinator as a participating investor** (extend.ai/resources/series-a). YC is also the amplifier that pushed the launch via its own X account and Hacker News Show HN (x.com/ycombinator/status/1991918332149399969; news.ycombinator.com/item?id=46006104): the amplifier has a financial stake in the operator. Extend sells a competing full-stack document platform and runs its own separate, non-crowdsourced benchmark (RealDocBench) where its own "Parse"/"Performance v2" product "leads" (extend.ai/resources/ocr-benchmarks-real-world-documents), a halo-effect risk, though I checked directly and **Extend's own product does not appear as a ranked competitor inside OCR Arena itself** (confirmed via the Product Hunt maker thread, producthunt.com/products/ocr-arena, no self-entry found). Models run "powered by our friends over at Baseten" (ocrarena.ai/about), an undisclosed-terms compute sponsorship.

**2. Methodology.** Standard ELO, 1500 start, K=20, on crowd votes (ocrarena.ai/about). HN commenters documented votes rewarding formatting polish over correctness, one case had a model's chemical viscosity value "off by 7 orders of magnitude" yet still scoring competitively, plus English-language and latency-perception bias (HN thread above). No total vote/battle count is disclosed anywhere on-site or in coverage.

**3. Saturation.** Full-field spread looks real (~1719 to ~1390 ELO across 21+ models per aggregated results: the live table is JS-rendered and didn't return via direct fetch, so this is third-party-reported, not independently confirmed). But cited pairwise samples are thin (144 to 171 matchups for specific pairs): too small for stable top-of-table ordering.

**4. Gaming history.** None documented in ~8 months live (launched Nov 2025). Can't rule out given zero public vote-volume disclosure.

**5. Staleness.** Genuinely live past launch: current #1 (Gemini 3 Flash) shipped Dec 17 2025 (blog.google/products/gemini/gemini-3-flash), after the Nov 2025 debut. No public changelog exists to confirm any 2026 update cadence (contrast: competitor arena.ai publishes one).

**Case for:** fills a real document-specific gap general arenas skip; a second, unaffiliated party (NanoNets' idp-leaderboard.org/arena) runs a comparable battle feature as a cross-check. Fine for a rough directional pulse, not for production model selection.

VERDICT: caveat | OCR Arena | Vendor-operated by Extend, YC-investor-amplified, undisclosed vote volumes, formatting-biased crowd votes; still discriminates, cross-checkable via idp-leaderboard.
