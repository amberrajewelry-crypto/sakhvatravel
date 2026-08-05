# Sitemap Audit — sakhva-travel.com
Date: 2026-08-05

> ⚠️ КОРРЕКЦИЯ ПОСЛЕ СТРОГОЙ ПЕРЕПРОВЕРКИ (оркестратор):
> - Sitemap-файлов **5** (sitemap-index + pages/blog/tours/landing), не «4».
> - Находка «17 orphan-экскурсий вне sitemap» — **ЛОЖНАЯ**. Прямая проверка: `ekskursiya-abanotubani`, `ekskursiya-ananuri-iz-tbilisi` и др. имеют собственный `<loc>` в sitemap-tours.xml для всех 3 языков (RU/GE/EN). Реальна только 1 битая запись — `rtveli-grape-harvest` (на диске `rtveli-sbor-vinograda`).

## Summary

| Check | Result |
|-------|--------|
| XML validity | PASS (all 4 child sitemaps well-formed) |
| Total URLs | 733 across 4 files — well under 50k limit |
| 404 in sitemap | 1 confirmed |
| Orphan pages (200, not in sitemap) | 15+ ekskursiya pages |
| hreflang consistency | 4 structural issues |
| lastmod staleness | sitemap-index entries stale vs content dates |
| Duplicate URLs cross-sitemap | 0 |
| Junk/scripts/noindex in sitemaps | 0 |
| Location page quality gate | WARNING — 28 geo-landing pages (RU only) |

---

## 1. 404 in Sitemap — CRITICAL (High)

| URL | Status | Sitemap |
|-----|--------|---------|
| `https://sakhva-travel.com/ekskursiya/rtveli-grape-harvest/` | 404 | sitemap-tours.xml |

**Note:** The slug `rtveli-sbor-vinograda` exists on disk and returns 200. The sitemap contains **both** the correct slug AND the English-slug alias `rtveli-grape-harvest` which does not exist. Remove `rtveli-grape-harvest` from sitemap-tours.xml.

---

## 2. Orphan Pages — High (200, not indexed via sitemap)

These pages exist on disk and return 200 but are absent from all sitemaps. Google can discover them only via internal links.

### ekskursiya/ orphans (sitemap-tours.xml missing these RU pages)

All confirmed 200:

| Path | Notes |
|------|-------|
| `/ekskursiya/ekskursiya-abanotubani/` | Abanotubani — high-intent Tbilisi page |
| `/ekskursiya/ekskursiya-ananuri-iz-tbilisi/` | Ananuri |
| `/ekskursiya/ekskursiya-bakuriani-iz-tbilisi/` | Bakuriani |
| `/ekskursiya/ekskursiya-dashbashi-iz-tbilisi/` | Dashbashi Canyon |
| `/ekskursiya/ekskursiya-gori-iz-tbilisi/` | Gori |
| `/ekskursiya/ekskursiya-gudauri-iz-tbilisi/` | Gudauri |
| `/ekskursiya/ekskursiya-hevsuretia-shatili/` | Khevsureti |
| `/ekskursiya/ekskursiya-jvari-iz-tbilisi/` | Jvari |
| `/ekskursiya/ekskursiya-kakheti-iz-tbilisi/` | Kakheti |
| `/ekskursiya/ekskursiya-kanyony-zapadnoy-gruzii/` | Western Georgia canyons |
| `/ekskursiya/ekskursiya-mtatsminda/` | Mtatsminda |
| `/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/` | Mtskheta |
| `/ekskursiya/ekskursiya-racha-iz-tbilisi/` | Racha |
| `/ekskursiya/ekskursiya-telavi-iz-tbilisi/` | Telavi |
| `/ekskursiya/ekskursiya-truso/` | Truso Valley |
| `/ekskursiya/ekskursiya-uplistsikhe-iz-tbilisi/` | Uplistsikhe |
| `/ekskursiya/ekskursiya-ureki-iz-tbilisi/` | Ureki |

These are real tour product pages with commercial intent. All need to be added to sitemap-tours.xml with RU/EN/GE hreflang blocks.

---

## 3. hreflang Issues — Medium

### 3a. `tury-v-tbilisi/` — no hreflang at all
`https://sakhva-travel.com/tury-v-tbilisi/` is in sitemap-pages.xml with zero `xhtml:link` entries. No EN, no GE, no x-default. Page returns 200. If EN/GE versions exist, add them. If not, add at minimum `hreflang="ru"` + `x-default`.

### 3b. `private-guide-tbilisi` — missing `hreflang="ru"`
Both `en/private-guide-tbilisi/` and `ge/private-guide-tbilisi/` entries in sitemap lack `hreflang="ru"`. There is no RU version of this page — intentional or oversight. If intentional, x-default should point to EN, which it correctly does. Acceptable if RU page doesn't exist, but verify.

### 3c. `privacy/` — missing EN hreflang
`/privacy/` entry has only `hreflang="ru"` + `ka` + `x-default`. But `/en/privacy/` exists (200) and is not referenced. Either add EN hreflang or check if the page is actually indexed.

### 3d. Multiple pages missing EN hreflang
Several RU-only pages (category pages: `mnogodnevnye-tury-gruzia/`, `gornye-tury-gruzia/`, `avtorskie-tury-gruzia/`, `ekskursionnye-tury-v-gruziyu/`, `tury-na-kazbek/`, `tury-v-svaneti/`, `tury-v-batumi/`, `tury-v-gruziyu-letom/`, `tury-v-gruziyu-zimoy/`, `grupovye-tury-v-gruziyu/`, `individualnyy-tur-v-gruziyu/`, `tury-v-gruziyu-s-detmi/`) have only `ru`+`ka` hreflang — no `en`. This is consistent across the file suggesting EN versions don't exist for these. Acceptable if true, but verify EN coverage gap.

---

## 4. sitemap-index lastmod Staleness — Low

| Child sitemap | sitemap-index lastmod | Actual newest content date |
|--------------|----------------------|---------------------------|
| sitemap-blog.xml | 2026-07-15 | 2026-07-26 |
| sitemap-tours.xml | 2026-07-17 | 2026-07-29 |
| sitemap-landing.xml | 2026-07-14 | 2026-07-24 |
| sitemap-pages.xml | 2026-07-16 | 2026-07-26 |

All sitemap-index `<lastmod>` values are 10–15 days behind the actual newest `<lastmod>` inside the child files. Google ignores sitemap-index lastmod in practice, but update for correctness.

---

## 5. Location Page Quality Gate — WARNING

**28 RU geo-landing pages** (`tury-v-gruziyu-iz-*`) in sitemap-landing.xml.

This is below the HARD STOP threshold of 50 but above the WARNING threshold of 30 only when counting all three language versions:
- RU: 28 pages × 3 languages (RU + EN + GE) = 84 total URLs in sitemap

The EN and GE versions exist in sitemap-landing.xml for all 28 cities, confirmed. Risk: if these pages swap only the city name with identical content body, Google's doorway page algorithm applies. Verify at least 60% unique content per city page (local transport details, flight times, crossing points specific to each city).

Additionally: **6 foreign-country landing pages** in sitemap-landing.xml (`/turkey/`, `/egypt/`, `/uae/`, `/thailand/`, `/maldives/`, `/vietnam/`, `/cyprus/`) — all return 200. These are off-topic for a Georgia tour guide. If they are thin placeholder pages, consider noindex or removal from sitemap.

---

## 6. en/tours-in-georgia Missing from sitemap-tours.xml `<loc>` — Info

`https://sakhva-travel.com/en/tours-in-georgia/` is referenced in hreflang alternates of `ekskursiya/` and `ge/ekskursiya/` entries, and it returns 200, but it has **no own `<loc>` entry** in sitemap-tours.xml. It appears only as an alternate target, never as a canonical URL. Add it as a `<loc>` entry.

---

## 7. Checks Passed

- No `/scripts/`, `/api/`, `.bak`, or admin URLs in any sitemap
- No noindex pages detected in sitemaps (spot-checked)
- No duplicate `<loc>` URLs across sitemaps
- All four child sitemaps referenced in sitemap-index
- All sampled blog RU/EN/GE URLs return 200 — no ghosts
- URL count 733 total — far below 50,000 limit
- Date format `YYYY-MM-DD` valid throughout
- No `<priority>` or `<changefreq>` tags present (correct)

---

## Action Priority

| Priority | Action |
|----------|--------|
| HIGH | Remove `ekskursiya/rtveli-grape-harvest/` from sitemap-tours.xml (404) |
| HIGH | Add 17 orphan ekskursiya pages to sitemap-tours.xml |
| HIGH | Add `en/tours-in-georgia/` as a `<loc>` entry in sitemap-tours.xml |
| MEDIUM | Fix `tury-v-tbilisi/` — add hreflang block |
| MEDIUM | Fix `privacy/` — add EN hreflang |
| MEDIUM | Audit 6 foreign-country pages (turkey/egypt/uae/etc) — noindex or remove from sitemap if thin |
| LOW | Update sitemap-index lastmod values to match child file dates |
| LOW | Verify 28 geo-landing pages have differentiated content (quality gate) |
