# Schema.org Audit — sakhva-travel.com — 2026-09-18

Score: 78/100

## Method
Local source at /Users/vladimir/sakhva-travel (read-only). JSON-LD extracted via regex + `json.loads` per block. Site-wide grep for cid, ratingValue, reviewCount, TouristTrip, HowTo across `*.html`.

## Pages checked
/, /en/, /ge/, /about/, /tury-v-gruziyu/, /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/, /en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/, /ekskursiya/transfer-tbilisi-batumi/, /blog/gruzinskie-frazy/, /en/blog/georgian-alphabet/, /ge/blog/tbilisoba/

## Critical (1)
1. **Invalid JSON-LD on live page** — `blog/gruzinskie-frazy/index.html`: FAQPage `Answer.text` contains an unescaped `<a href="/blog/gamardzhoba/">` with literal `"` inside a JSON string → `json.loads` fails (`Expecting ',' delimiter: line 1 column 3011`). Entire structured-data block is invalid for that page (Rich Results Test will reject it; AI crawlers parsing JSON-LD will also fail). Other 10 checked pages parsed clean.

## High (2)
2. **AggregateRating inconsistency on the same Product across locales** — RU Kazbegi page (`ekskursiya/ekskursiya-kazbegi-iz-tbilisi/index.html`) carries `AggregateRating {ratingValue: 5.0, reviewCount: 3}`; EN version of the identical page (`en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/index.html`) has the same Product/Offer but **no AggregateRating at all**. Both also diverge from the owner-confirmed site-wide real numbers (4.9 / 90+): sitewide grep found `reviewCount` values of 90 (154 occurrences, correct) vs an isolated `reviewCount: 3` only on this one RU page — an orphan/stale rating block, not the confirmed number.
3. **about/index.html TravelAgency entity missing telephone/sameAs at top level of the TravelAgency node** — telephone and sameAs (incl. Maps cid) exist elsewhere on the page in a *different* node's `sameAs` array, but were not directly re-verified as attached to the same `@id` as the TravelAgency block; recommend explicitly binding via `"@id":"https://sakhva-travel.com/#business"` reference on this page like homepage does, to avoid duplicate/conflicting business entities.

## Medium (1)
4. **12 duplicate inline `Organization {name, url}` stub nodes** on `tury-v-gruziyu/index.html` (one per Product’s `publisher`), each a bare 2-property object instead of an `@id` reference to the single canonical Organization node. Not invalid, but bloats payload and risks Google merging/deduping unpredictably.

## Info (2)
5. **FAQPage present on 924 local HTML files** — per owner rule this is Info-only (no SERP feature since 2026-05-07, still valid for AI/LLM citation). No action.
6. Tours correctly use `Product` + `Offer` sitewide (0 live `TouristTrip` occurrences — the 8 hits found are all in `scripts/_stars_backup_20260704/` backup folder, not served). No `HowTo` anywhere (0 hits). Confirms owner rules already respected in production.

## Validation checklist results (11 pages)
- @context `https://schema.org`: pass on all 11.
- JSON-LD valid: **10/11 pass, 1 fail** (see Critical #1).
- No deprecated types (HowTo/SpecialAnnouncement/CourseInfo/EstimatedSalary/LearningVideo): 0 found sitewide — pass.
- Product/Offer required fields (price, priceCurrency=GEL, availability, url): present and correct on both Kazbegi pages and transfer-tbilisi-batumi (`price`, `priceCurrency: GEL`, `availability: https://schema.org/InStock`, absolute `url`) — pass.
- Absolute URLs: pass (all offer/canonical URLs are `https://sakhva-travel.com/...`).
- LocalBusiness naming: site uses `TravelAgency`/`Organization`, not `LocalBusiness`/`TouristInformationCenter` — acceptable, no owner rule against it; name "Sakhva Travel" and telephone `+995511272623` consistent across all 4 top-level pages checked.
- sameAs Google Maps cid: correct cid `14112587239859278397` found on 153 files; dead cid `14070083063461040701` found on **0** files — pass, fully migrated.
- BreadcrumbList: present with `ListItem` on all 11 pages, positions look sequential (not exhaustively diffed item-by-item).
- BlogPosting (3 blog pages checked): all carry `Organization` publisher, `Person` author, `ImageObject`; did not confirm `datePublished`/`dateModified` presence in this pass — recommend follow-up spot-check if precise dates matter for Article rich results.
- VideoObject present on homepage and both Kazbegi pages and transfer-tbilisi-batumi — not schema-validated for `uploadDate`/`thumbnailUrl` in this pass.

## Severity counts
Critical: 1 | High: 2 | Medium: 1 | Info: 2 | Total flagged: 6
