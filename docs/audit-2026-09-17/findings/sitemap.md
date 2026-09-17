# Sitemap audit — sakhva-travel.com — 2026-09-17

**Score: 78/100**

## Structure
- sitemap.xml → 301 → sitemap-index.xml (200, valid index, 5 sub-sitemaps).
- robots.txt declares `Sitemap: https://sakhva-travel.com/sitemap-index.xml` — correct, matches redirect target.
- Total URLs: 875 (blog 357 + tours 245 + landing 124 + pages 83 + pogoda 66) — matches GSC submitted counts exactly, 0 warnings/0 errors on all 6 GSC-registered sitemap entries.
- All 5 sub-sitemaps: valid XML, well under 50,000 URL limit, uncompressed (34–201 KB each, no gzip needed at this size).

## Checks
| Check | Result | Severity |
|---|---|---|
| XML validity | PASS — all 5 files parse clean | — |
| priority/changefreq | Absent (already removed) | Info — none |
| lastmod realism | FAIL — batched, not per-page: pogoda 66/66 same date; blog/tours/landing/pages cluster into 7–11 distinct dates (deploy-batch dates, not real edit dates) | Low |
| Duplicates across sub-sitemaps | 0 | — |
| Non-canonical URLs (query params/case/host) | 0 found | — |
| Sample 40 URLs status | 40/40 → 200 | — |
| hreflang (xhtml:link) | Present in sitemap for all urls; verified matches on-page `<link rel=alternate>` for sample (ru/en/ka + x-default) | — |
| RU/EN/GE coverage | RU 295, EN 283, GE 297 — near parity | — |
| image/video sitemap | Absent | Info — optional, not required |
| GSC submission | 6 entries (incl. legacy sitemap.xml + sitemap-index.xml both indexed), 0 errors/warnings | — |

## Quality gate — HARD STOP triggered
**84 "tours-from-city" location pages** (28 cities × ru `/tury-v-gruziyu-iz-*/` + en `/tours-from-*/` + ge `/tours-from-*/`), all inside sitemap-landing.xml (68% of that file's 124 URLs).

Diffed `/en/tours-from-moscow/` vs `/en/tours-from-sochi/`: only title/meta/price numbers differ — **~89% token overlap, ~11% unique content per page**. This is below the 60%-unique threshold and the page count (84) is well past the 50-page hard-stop line.

- **Action required**: either (a) get Владимир's explicit justification to keep as-is (doorway-page penalty risk per Google's algorithm), or (b) consolidate to fewer high-value city pages with real unique content (distances, transport options, prices, guide notes per city) to clear 60%+ uniqueness, or (c) noindex the thin tail and keep only top-traffic cities indexed.

## Fixes by priority
1. **High**: Resolve location-page quality gate on 84 tours-from-* pages (see above) — get sign-off or de-thin content.
2. **Low**: Replace batched lastmod with real per-page edit timestamps (currently misleading — Google mostly ignores lastmod anyway if untrustworthy, but worth fixing at next content-pipeline touch).
3. **Info**: Consider image sitemap for tour/blog hero images if the SEO agent wants faster image-search indexing — not urgent.

No critical XML/coverage/404 issues found.
