# Content Quality / E-E-A-T Audit — sakhva-travel.com
Date: 2026-09-18 | Score: 78/100

## Method
10 target pages read from local source (index.html main-content extraction, script/style stripped),
plus site-wide word-count scan of all `blog/*/index.html`, `en/blog/*/index.html`, `ge/blog/*/index.html` (355 articles).
4.9 rating / 90+ reviews / 98% claims treated as owner-confirmed per instruction, not flagged.

## Site-wide blog thin-content scan
- 0 of 355 blog articles fall under the 800-word floor.
- 10 thinnest (all still above 800, several below the 1,500-word blog QRG floor):
  1. `ge/blog/georgian-sweets-desserts/` — 845 words
  2. `ge/blog/tipping-in-georgia/` — 870
  3. `ge/blog/tbilisi-taxi-guide/` — 884
  4. `ge/blog/money-cards-georgia/` — 888
  5. `ge/blog/car-rental-georgia/` — 906
  6. `ge/blog/car-rental-tbilisi/` — 1,027
  7. `blog/gruzinskie-sladosti/` — 1,028
  8. `en/blog/car-rental-georgia/` — 1,031
  9. `blog/gamardzhoba/` — 1,055
  10. `ge/blog/hotels-tbilisi/` — 1,070
  - Pattern: GE-locale articles are systematically thinner than their RU/EN counterparts (likely translated/shortened, not independently written) — dilutes GE-locale expertise signal.

## 10 target pages — findings

### Critical
1. **Tour-count contradiction across pages**: homepage `index.html` states "460+ тур" (twitter/og description + on-page), while `about/index.html`, `en/about/index.html`, `ge/about/index.html` all state "**500+ туров**" (9 occurrences each). This is an internal factual inconsistency, not the exempted "460+" claim itself — the two numbers disagree site-wide across the about pages vs homepage.

### High
2. **AI-cliché phrasing in EN blog** (Sept 2025 QRG generic-AI-content marker): "hidden gem" / similar boilerplate travel-blog phrasing found verbatim in 10 EN posts incl. `en/blog/hidden-gems-tbilisi/`, `en/blog/free-things-tbilisi/`, `en/blog/kazbegi-day-trip-from-tbilisi/`, `en/blog/kakheti-wine-tour/`, `en/blog/georgian-food-guide/`, `en/blog/adjarian-khachapuri-guide/`, `en/blog/botanical-garden-tbilisi/`, `en/blog/georgia-with-pets/`, `en/blog/georgian-military-highway/`, `en/blog/georgia-visa-2026/` — undercuts "first-hand, specific" experience signal even though the site elsewhere has good local specifics (named cafes, streets).
3. **Missing datePublished/dateModified schema on key money pages**: `about/index.html` and `tury-v-gruziyu/index.html` have no `datePublished`/`dateModified` in schema (unlike homepage and all sampled blog/tour pages, which correctly carry `dateModified: 2026-09-17`). Freshness signal gap on the two highest-intent pages.

### Medium
4. **`ge/blog/tbilisoba/` under blog QRG floor**: 1,262 words vs 1,500 recommended minimum; GE about-page equivalent thinness pattern confirmed (see site-wide scan).
5. **Author schema present but only in blog/tour pages, absent from `about/`, `tury-v-gruziyu/`, homepage** — inconsistent expertise (E) signal placement; the person-level credential (license №8247109128, named guide Тимур Сахвадзе) lives only in visible text on `/about/`, not reinforced via schema on other pages.

### Low
6. Currency symbol inconsistency (stylistic, not factual): same tour price rendered as "175 лари", "₾175", "175 GEL" across index/RU-tour/EN-tour pages — not a price contradiction (value matches, 175 across RU+EN Kazbegi), but inconsistent formatting could confuse scrapers/AI citation extraction.

## Positive signals (no fix needed)
- Kazbegi tour price is consistent RU (175 лари/₾175) vs EN (₾175 per person) — no cross-page price contradiction found.
- `/about/` has strong first-hand experience signals: named guide, license number, founding year, specific unlisted places (Авлабари cafe, Коте Абхази courtyard), WhatsApp contact — solid Trust/Experience baseline.
- All 10 sampled pages exceed their page-type word minimum except `ge/blog/tbilisoba/` (medium finding above).

## Severity counts
- Critical: 1
- High: 2
- Medium: 2
- Low: 1
