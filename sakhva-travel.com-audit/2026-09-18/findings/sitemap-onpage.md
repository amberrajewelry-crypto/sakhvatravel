# Sitemap + On-Page Audit — sakhva-travel.com
Date: 2026-09-18 | Source: local repo (read-only) | Score: **71/100**

## Part A — Sitemap

### XML validity
All 7 files parse as valid XML: sitemap-index.xml, sitemap-blog.xml, sitemap-tours.xml,
sitemap-landing.xml, sitemap-pages.xml, sitemap-pogoda.xml, sitemap-images.xml. No `priority`/
`changefreq` tags present anywhere (already clean, matches Google's "ignored" guidance).

### Coverage
| Sitemap | URL count |
|---|---|
| sitemap-blog.xml | 358 |
| sitemap-tours.xml | 245 |
| sitemap-landing.xml | 68 |
| sitemap-pages.xml | 83 |
| sitemap-pogoda.xml | 66 |
| **Total unique URLs** | **820** |

- Duplicate URLs across child sitemaps: **0**
- Per-file limit (50,000): all files far under limit — PASS
- URLs in sitemap with no matching local file: **0** — PASS

### Local files not in any sitemap
Total local `index.html`: 899. Excluding payment-success/404/draft: **79 orphaned from sitemap**.
Breakdown of the 79:
- **56** = `en/tours-from-*` (28) + `ge/tours-from-*` (28) location/city-pair pages — RU equivalent
  (`tury-v-gruziyu-iz-*`, 28 cities) IS in sitemap-landing.xml (only 68 of 84 landing pages listed
  — see quality gate below), but EN/GE versions are silently excluded from all sitemaps.
- Remaining 23: utility/internal pages correctly excluded from sitemap by design —
  `dashboard/`, `gallery/` (ru/en/ge), `booking/` (en/ge), `links/` (en/ge), `pay/`/`gadakhda/`
  (payment aliases), `policy/`, `terms/` — these look intentional, not a bug.

### Lastmod
- Only 2 distinct dates across all 820 URLs: 2026-09-18 (480) and 2026-09-17 (340).
- No future dates. Not fully "identical" but suspiciously bulk-touched (Low severity per rubric —
  looks like a mass regenerate/deploy timestamp, not per-content-change tracking).

### Image sitemap
- 769 `<url>` entries, 1,414 `<image:image>` entries.
- **18 image:loc references point to files that don't exist locally** (5 distinct missing
  assets, referenced repeatedly): `og-avtorskie-tury.jpg`, `blog/og-old-tbilisi.webp`,
  `blog/kurs-lari-k-rublyu.jpg`, `stary-tbilisi-tour-600.jpg`, `og-ekskursii-gruzii.jpg`.
- No video sitemap exists (none needed unless video content is a priority).

### hreflang
hreflang/xhtml:link markup present inside sitemap entries for all 5 content sitemaps (blog 1418,
tours 972, landing 214, pages 300, pogoda 264 occurrences) — sitemap-level hreflang looks wired.
Did not cross-diff every alternate URL for reciprocity in this pass (would need a second script
pass matching sets of alternates per URL — flag as follow-up if needed).

### Quality Gate — Location Pages (HARD STOP triggered)
- Location/city-pair pages found: **28 RU** (`tury-v-gruziyu-iz-*`) + **28 EN**
  (`tours-from-*`) + **28 GE** (`tours-from-*`) = **84 total**, well over the 50-page hard-stop
  threshold.
- Content uniqueness sample (en/tours-from-moscow vs en/tours-from-sochi): **86.5% textual
  similarity → only ~13.5% unique content per page**, far below the required 60%+ unique-content
  threshold at 30+ pages.
- This is a textbook Google doorway-page pattern (city name swapped, rest boilerplate) — high
  risk of algorithmic demotion/penalty. **Explicit user justification required to keep as-is**,
  otherwise consolidate into fewer high-value pages or add real per-city unique content
  (flights, distances, local logistics) to clear 60%.

## Part B — On-Page (899 local index.html analyzed, excluding payment-success/404/draft)

### Titles
- Empty `<title>`: 2 pages (`yandex_59a834df.../index.html`, `yandex-verify/index.html` — verification stubs, not real pages, non-issue).
- <30 chars: 4 pages | >65 chars: 24 pages.
- Duplicate titles: **0 groups** — every page has a unique title. PASS.

### Meta descriptions
- Missing meta description: **7 pages** (after correcting for attribute-order variance in the
  `<meta>` tag — initial naive regex overcounted 635 due to `content` sometimes preceding `name`).
- Duplicate meta descriptions: **1 group, 2 pages** — homepage description duplicated onto
  `scripts/_xdefault_backup_20260704/index.html` (a backup/scratch page, not a live page — low
  real-world impact but should be removed from the crawlable tree regardless).

### H1
- Missing H1: 2 pages (same Yandex verification stubs as above — non-issue).
- Pages with >1 H1: **0** — PASS.
- Duplicate H1 groups: 2 groups / 6 pages — "Экскурсии по Грузии с гидом" (homepage +
  backup-scripts clone) and "Sakhva Travel" (dashboard/links pages ×4, generic branded H1 by
  design on utility pages).
- Title == H1 exact match: 45 pages (acceptable pattern for landing pages, not flagged as an
  issue on its own).

### Internal linking
- Blog posts (355 total, excl. blog index) with **no link to any `/ekskursiya/` tour page: 17**
  (9 EN + 8 GE informational posts — visa/legal/logistics topics: notary, company registration,
  residence permit, marriage, rafting, dental tourism, camping, best-time-to-visit — these
  legitimately may not need a tour CTA, but should still cross-sell somewhere).
- **Orphan pages (0 inbound internal links from any other local page): 6** —
  `dashboard/index.html`, `en/pay/index.html`, `ge/gadakhda/index.html`,
  `gid/_template/index.html`, `oplata/index.html`, `partner/index.html`. Payment/dashboard pages
  being orphaned is expected (accessed via direct link/QR, not nav), but `partner/` and the
  `gid/_template/` scaffold should be reviewed — template folder should likely not be a live
  crawlable page at all.
- Pages with >300 internal links: **0** — PASS.

## Severity Buckets
| Severity | Count | Items |
|---|---|---|
| Critical | 0 | — |
| High | 1 | Location-page doorway pattern: 84 pages, 86.5% content similarity, hard-stop threshold exceeded |
| Medium | 3 | 18 broken image-sitemap references (5 unique missing assets); 56 EN/GE location pages excluded from sitemap while RU version is included (inconsistent indexation signal); `scripts/_xdefault_backup_20260704/` and `gid/_template/` live/crawlable when they should not be |
| Low | 3 | 7 pages missing meta description; lastmod compressed into only 2 bulk dates (not real per-page change tracking); 17 blog posts with no internal link to a tour page |
| Info | 2 | No priority/changefreq tags present (good — nothing to remove); 24 titles >65 chars, 4 titles <30 chars |

## Score rationale
Base 100 − 20 (High: doorway-page hard-stop) − 3×4 (Medium items) − 3×2 (Low items) = 71/100.
