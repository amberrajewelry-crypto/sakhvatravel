# Content Quality Audit — sakhva-travel.com
**Date:** 2026-08-05  
**Scope:** RU /blog/ (102 posts), EN /en/blog/ (104 posts), GE /ge/blog/ (106 posts), tour pages, category hubs

---

## Overall Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Content Quality | 68/100 | Strong long-form core, thin tail drags it down |
| E-E-A-T | 74/100 | Person schema solid, zero Review schema anywhere |
| AI Citation Readiness | 61/100 | FAQPage present, but no AggregateRating, prices inconsistent |

---

## E-E-A-T Breakdown

| Factor | Weight | Score | Finding |
|--------|--------|-------|---------|
| Experience | 20% | 72 | First-person signals in 102/102 RU posts (я/мы/лично) — good. No photo-of-guide in article body on thin posts. |
| Expertise | 25% | 78 | Person schema consistent: `Тимур Сахвадзе`, `jobTitle: Гид в Тбилиси`, `hasCredential` лицензия #8247109128 (Нац. администрация туризма Грузии). Credential identifier is machine-readable — strong signal. |
| Authoritativeness | 25% | 65 | Zero external citation or Review schema across all 102 RU posts. AggregateRating missing everywhere. About page has no review block (1192w, no reviews). |
| Trustworthiness | 30% | 72 | datePublished + dateModified present in all checked posts. OG article:published/modified confirmed. Price facts present in most commercial posts. Contact/WhatsApp visible. |

---

## 1. Thin Content [SEVERITY: HIGH]

### RU — Thin (<1000 words in main/article)

| URL | Words | Issue |
|-----|-------|-------|
| `/blog/gruzinskie-sladosti/` | 602 | 6 H2 headings but ~85w per section — list without depth |
| `/blog/karty-nalichnye-gruziya/` | 623 | Practical info page, no prices/ATM locations |
| `/blog/taksi-tbilisi/` | 657 | Missing: apps, price ranges, typical routes, safety tips |
| `/blog/chaevye-v-gruzii/` | 662 | Only 5 H2 sections, no FAQ schema despite being FAQ-type |
| `/blog/gruzinskie-frazy/` | 941 | Phrase list format — thin prose but acceptable format for the intent |

**None of the 5 have FAQPage schema** — the closest intent-fit for these utility pages is exactly FAQ, yet it's absent.

### RU — Borderline (1000–1499 words) — 22 posts

Top priority for expansion:

| URL | Words | Gap |
|-----|-------|-----|
| `/blog/mtskheta-iz-tbilisi/` | 1169 | Key long-tail — needs itinerary section, transport options |
| `/blog/istoriya-tbilisi/` | 1211 | Authority topic — needs timeline, key dates, rulers |
| `/blog/kanatnaya-doroga-tbilisi/` | 1230 | Missing: ticket prices, schedule, top/bottom views |
| `/blog/basseyny-tbilisi/` | 1248 | Missing: specific pool addresses, entry fees |
| `/blog/oteli-tbilisi-5-zvezd-v-centre/` | 1264 | No prices — fatal for commercial intent |
| `/blog/kanyon-martvili/` | 1282 | Missing: exact hours, entrance fee, how to get there |
| `/blog/david-gareji/` | 1291 | Pilgrimage site — needs border crossing note, visa |
| `/blog/tury-v-borzhomi-2026/` | 1358 | Commercial page — no price schema |
| `/blog/tury-v-tbilisi-2026/` | 1381 | Commercial page — no price schema |
| `/blog/tury-v-batumi-2026/` | 1383 | Commercial page — no price schema |

### EN — Thin (<1000 words)

| URL | Words |
|-----|-------|
| `/en/blog/car-rental-georgia/` | 818 |
| `/en/blog/georgian-sweets-desserts/` | 976 |
| `/en/blog/tbilisi-taxi-guide/` | 998 |

All three have Person schema and FAQPage — structure is correct, but content volume is below the 1500-word target for blog posts. The EN taxi/sweets pages mirror the same thin RU originals.

### GE — Thin (<1000 words) — 8 pages

| URL | Words |
|-----|-------|
| `/ge/blog/car-rental-georgia/` | 735 |
| `/ge/blog/georgian-sweets-desserts/` | 782 |
| `/ge/blog/tbilisi-taxi-guide/` | 787 |
| `/ge/blog/tipping-in-georgia/` | 788 |
| `/ge/blog/money-cards-georgia/` | 811 |
| `/ge/blog/hotels-tbilisi/` | 879 |
| `/ge/blog/car-rental-tbilisi/` | 895 |
| `/ge/blog/apartment-rental-tbilisi/` | 958 |

GE posts are systematically shorter than EN counterparts — likely translated with compression. 47 more GE posts are in the 1000–1499 borderline range (vs 18 EN).

---

## 2. E-E-A-T Gaps [SEVERITY: HIGH]

### No Review / AggregateRating schema anywhere

- **0 out of 102 RU posts** have `AggregateRating` or `reviewBody` schema.  
- Tour pages (`/ekskursionnye-tury-v-gruziyu/`, `/individualnyy-tur-v-gruziyu/`) show `review=True` in the DOM (visual blocks), but no structured Review schema in JSON-LD.  
- This is the single biggest AI citation readiness gap: Google's rich results for tour/local business need AggregateRating to surface star ratings.  
- **Fix:** Add `AggregateRating` to the main tour landing pages (`/ekskursiya/`, `/tury-v-gruziyu/`, `/individualnyy-tur-v-gruziyu/`) using existing Viator/Tripadvisor rating data if available, or collect and embed 5–10 reviews in JSON-LD.

### About page has no Review block

- `/about/` — 1192 words, Person schema with credential — good.  
- Missing: testimonial section, AggregateRating for the guide himself, no sameAs to any external profile (Google Business, Tripadvisor, Viator).  
- Fix: Add 3+ review quotes with `author`, `datePublished`, `reviewRating` in JSON-LD + visible HTML.

### dateModified stale on older posts

- 9 thin/borderline posts checked: dateModified = datePublished (never updated).  
- Example: `/blog/mtskheta-iz-tbilisi/` pub=mod=2026-04-05, `/blog/voskresene-v-tbilisi/` pub=mod=2026-06-13.  
- QRG 2025 weights freshness signals heavily for travel content. Posts that have been "published and forgotten" with identical pub/mod dates signal no editorial maintenance.

---

## 3. Cannibalisation [SEVERITY: MEDIUM]

Confirmed overlapping intent pairs:

| Pair | Risk | Note |
|------|------|------|
| `/blog/oteli-tbilisi/` vs `/blog/rayony-tbilisi-gde-ostanovitsya/` | HIGH | Both target "где остановиться Тбилиси" — titles overlap |
| `/blog/oteli-tbilisi/` vs `/blog/oteli-tbilisi-5-zvezd-v-centre/` | MEDIUM | Parent/child differentiation is clear but thin 5-star post competes |
| `/blog/arenda-avto-tbilisi/` vs `/blog/arenda-avto-gruziya/` | HIGH | "аренда авто" query set split across two pages |
| `/blog/gid-tbilisi-vs-gid-gruziya/` vs `/blog/russkoyazychny-gid-tbilisi/` vs `/blog/chastny-gid-ili-gruppa-tbilisi/` | MEDIUM | Three pages targeting guide-hire intent — consolidation candidate |
| `/blog/chto-posmotret-v-gruzii/` vs `/blog/chto-posmotret-v-tbilisi/` | LOW | Geographic scope is clearly different — acceptable |
| `/blog/gruzinskoe-vino-gid/` vs `/blog/degustatsiya-vina-gruziya/` | LOW | Guide vs tour — differentiated enough |
| Kazbegi cluster (3 posts) | LOW | Intent is clearly differentiated (what-to-see vs when-to-go vs solo-vs-guide) |

**Priority fix:** `/blog/oteli-tbilisi/` + `/blog/rayony-tbilisi-gde-ostanovitsya/` — merge or canonical redirect. `/blog/arenda-avto-tbilisi/` + `/blog/arenda-avto-gruziya/` — add explicit canonical, ensure each targets a distinct primary keyword.

---

## 4. Multilanguage Parity [SEVERITY: MEDIUM]

- All 19 recent RU posts (Jul 2026 batch) **have EN and GE mirrors** — parity is maintained.  
- EN (104) > RU (102) > GE (106) — count discrepancy suggests GE has some unique posts or different structure. Not necessarily a problem.  
- GE posts are systematically compressed (~15–25% fewer words than EN equivalents) — see thin content table above.  
- **Known risk (from metro article incident):** factual errors mirror across all 3 languages verbatim. No new instances detected in sampled posts, but the process risk remains. Recommend a fact-check pass on posts with specific factual claims (prices, distances, schedules) whenever RU is updated.

---

## 5. AI Citation Readiness [SEVERITY: MEDIUM]

| Signal | Status |
|--------|--------|
| FAQPage schema | Present in most posts (confirmed in 3/5 thin posts missing it) |
| Structured prices (₾/GEL/$) | Present in commercial posts, absent in utility posts |
| Clear H2/H3 hierarchy | Present — all thin posts have 5–7 H2s |
| AggregateRating | **ABSENT everywhere** |
| HowTo schema | Not used — missed opportunity for step-by-step posts (metro, taxi, baths) |
| Quotable expert facts | Moderate — posts cite facts but rarely with source attribution |

The FAQ structure is the strongest AI-citation asset. Missing AggregateRating is the biggest gap — AI overviews heavily cite rated local businesses and guides.

---

## 6. Readability [SEVERITY: LOW]

- Paragraph length: adequate in long-form posts (2–4 sentences).  
- Thin posts (600–660w): 5–6 H2 with ~85–100 words per section — each section is barely one paragraph. No depth, reads like a skeleton.  
- Lists used appropriately in phrase/food/culture posts.  
- No readability issues in posts above 1500w.

---

## Priority Action List

| Priority | Action | Affected URLs |
|----------|--------|---------------|
| P1 | Expand 5 thin RU posts to 1500w | `/blog/gruzinskie-sladosti/`, `/blog/karty-nalichnye-gruziya/`, `/blog/taksi-tbilisi/`, `/blog/chaevye-v-gruzii/`, `/blog/gruzinskie-frazy/` |
| P1 | Add AggregateRating JSON-LD to tour hubs | `/ekskursiya/`, `/tury-v-gruziyu/`, `/individualnyy-tur-v-gruziyu/` |
| P2 | Add Review block to `/about/` | `/about/` |
| P2 | Fix cannibalisation: hotels + car rental pairs | `/blog/oteli-tbilisi/` + `/blog/rayony-tbilisi-gde-ostanovitsya/`; `/blog/arenda-avto-tbilisi/` + `/blog/arenda-avto-gruziya/` |
| P2 | Update dateModified on borderline posts after any edit | All 22 borderline posts |
| P3 | Expand GE thin posts (8 pages) | See GE thin table above |
| P3 | Add FAQPage to 5 thin posts that lack it | `/blog/gruzinskie-sladosti/` etc. |
| P3 | Add HowTo schema to process posts | `/blog/taksi-tbilisi/`, `/blog/metro-tbilisi/`, `/blog/sernye-bani-tbilisi/` |
