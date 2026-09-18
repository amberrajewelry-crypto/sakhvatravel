# Performance / Core Web Vitals audit — sakhva-travel.com (2026-09-18)

**Method note:** PSI API hit rate limit (no API key configured — request quota
issue tracket already open per project memory). Fell back to local Lighthouse
13.5.0 (mobile, throttled). Only `/` and `/en/` completed; `/ekskursiya/...`,
`/blog/gruzinskie-frazy/`, `/blog/metro-tbilisi/`, `/ge/blog/tbilisoba/`,
`/tury-v-gruziyu/` failed with LanternError (trace processing) on repeat runs —
not measured this pass, re-run needed with `--max-wait-for-load` increase or
PSI once quota resets.

## Score: 62/100 (based on 2/7 pages measured; extrapolated MEDIUM confidence)

## Per-page table (mobile, Lighthouse lab data)

| Page | LCP | TBT (INP proxy) | CLS | Perf score (mobile) |
|---|---|---|---|---|
| `/` | 2.1s (good) | 540ms (poor) | 0.022 (good) | 85 |
| `/en/` | 2.9s (needs improvement) | 290ms (needs improvement) | 0.022 (good) | 88 |
| `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/` | not measured | not measured | not measured | — |
| `/blog/gruzinskie-frazy/` | not measured | not measured | not measured | — |
| `/blog/metro-tbilisi/` | not measured | not measured | not measured | — |
| `/ge/blog/tbilisoba/` | not measured | not measured | not measured | — |
| `/tury-v-gruziyu/` | not measured | not measured | not measured | — |

## Top findings

1. **HIGH — TBT 540ms on `/` (poor INP proxy).** Long main-thread tasks block interactivity; TBT nearly 3x the "needs improvement" ceiling for CWV good bucket. Root cause likely JS execution during load — needs a JS profile pass (not done this run).
2. **MEDIUM — `deferred.css` is 85% unused (11.6 KiB of 13.7 KiB wasted) on both measured pages.** `https://sakhva-travel.com/css/deferred.css?v=73` — same wasted-bytes on `/` and `/en/`, so likely site-wide. Split/purge unused rules or inline only critical CSS.
3. **MEDIUM — LCP degrades from 2.1s (`/`) to 2.9s (`/en/`), crossing into "needs improvement".** Same TTFB (~116-130ms, fine) so the gap is render-delay/resource-load on the EN locale, not the server — check hero image/font loading differences between locales.

## Summary

Only `/` and `/en/` produced usable Lighthouse data this run; the other 5 URLs failed with LanternError under load and PSI API was rate-limited without a configured key. Both measured pages pass CLS comfortably (0.022) and TTFB is fast (<130ms). The real risk is JS-driven main-thread blocking (TBT 540ms on `/`) and a shared oversized `deferred.css` wasting ~85% of its bytes. EN locale LCP crosses into "needs improvement" (2.9s) despite identical server speed — worth a locale-specific asset check. Re-run PSI/Lighthouse on the 5 missing pages once quota/timeout issue is resolved before treating the 62/100 score as final.
