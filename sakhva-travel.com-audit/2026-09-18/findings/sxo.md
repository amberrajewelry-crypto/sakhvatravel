# SXO Gap Analysis — sakhva-travel.com (2026-09-18)

Scope: 3 keyword/page pairs, RU SERP for RU queries, EN SERP for EN query.
Fetched via `render_page.py --mode auto` + `parse_html.py`. Owner constraints applied:
no fake ratings, tours use Product+Offer schema, prepayment 10%, aggregator (Tripster/
Sputnik8) structure is NOT to be copied.

---

## Pair 1 — "экскурсии из тбилиси" → /tury-v-gruziyu/ (GSC pos ~29)

**Target page:** Title "Туры в Грузию 2026...", H1×1, 2338 words, schema:
TravelAgency+Product+Offer+AggregateOffer+ItemList+FAQPage+BreadcrumbList (5 blocks).

**Top-10 SERP:** sputnik8.com/category (marketplace listing, 186 excursions, from $17),
aviasales.ru/ekskursii (marketplace), tripadvisor (aggregator list), getyourguide
(marketplace), tezeks.com, coolgeorgia.com, allgeotrip.ru, tbilisi-tours.ru — **8/9
are multi-operator marketplace/aggregator listing pages** for day-trip excursions.

**SERP features:** no featured snippet observed, no local pack, no AI Overview surfaced
in results text; results dominated by category/listing pages with price filters.

**Dominant type:** Aggregator listing (day-trip catalog), confidence ~89%.
**Target type:** Single-vendor "Tours to Georgia" hub (broader multi-day country tours,
not a Tbilisi day-trip catalog) — **topical + format drift**, not just a display issue.

**Mismatch severity: HIGH.** Query intent = compare many operators' one-day Tbilisi
excursions; page answers "our Georgia tour catalog" one level up in scope.

**Gap score (100 pts):**
| Dim | Score | Evidence |
|---|---|---|
| Page Type | 6/15 | Country-tours hub ≠ Tbilisi-day-trip catalog query intent |
| Content Depth | 12/15 | 2338 words, 17 H2 — deep enough |
| UX Signals | 10/15 | 152 internal links (good), but no filter/sort UI marketplaces offer |
| Schema | 13/15 | Product/Offer/ItemList/FAQ present — strong |
| Media | 8/15 | 16 images, no video, no interactive map like getyourguide |
| Authority | 6/15 | Single-operator; GSC pos ~29 signals weak relevance vs marketplace scale |
| Freshness | 7/10 | "2026" in title, no visible last-updated date |
| **Total** | **62/100** | |

**3 user stories:**
1. "I want to compare several one-day excursions from Tbilisi by price and duration"
   (from sputnik8/aviasales filter UX) — page has no day-trip-only filtered view.
2. "I want to see Kazbegi/Mtskheta/Signagi as separate bookable day trips" (SERP
   subtopics) — page groups them inside multi-day itineraries, not a day-trip index.
3. "I want price transparency before I click" (marketplace snippets show "от $17")
   — page's Offer schema exists but isn't surfaced as a scannable price list.

**Most impactful change:** Build/promote a dedicated "Экскурсии из Тбилиси" day-trip
index page (ItemList of 1-day tours only, price/duration sortable) separate from the
country-tours hub — matches the marketplace-listing intent directly instead of
competing with an off-topic broader page. (Do not restructure as a Tripster/Sputnik8
clone — keep it single-operator Product+Offer, just narrow the topical scope.)

---

## Pair 2 — "казбеги из тбилиси экскурсия" → /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ (GSC ~51)

**Target page:** Title "Экскурсия Казбеги из Тбилиси за 1 день — от ₾175 с гидом",
1624 words, 3 images, schema: Product+Offer+AggregateRating+VideoObject+FAQPage+
BreadcrumbList+Person (5 blocks).

**Top-10 SERP:** sputnik8, booking.com/attractions, getyourguide, tripster.ru,
extraguide.ru, delicatours.ge (single-tour page), excursio.com, ge.engineer-history.com
(single-tour page), allgeotrip.ru — **6/9 marketplace/aggregator listings, 3/9
single-operator tour pages** (delicatours, engineer-history, target's own format).

**SERP features:** none of the notable SERP features (PAA/local pack/AIO) surfaced in
result set; pricing shown in titles ("от €9", "от 12 евро") across most results.

**Dominant type:** Aggregator/marketplace listing, confidence ~67%.
**Target type:** Single-operator Product page — a legitimate minority format in this
SERP, so **format itself isn't wrong**, but it's outgunned on scale signals.

**Mismatch severity: MEDIUM–HIGH.** Not a structural mismatch (single-tour pages do
rank), but competing against marketplaces' review volume and gallery depth without
the owner-approved workaround of adding fake reviews or copying marketplace layout.

**Gap score (100 pts):**
| Dim | Score | Evidence |
|---|---|---|
| Page Type | 7/15 | Single-product format is a real but minority SERP pattern |
| Content Depth | 12/15 | 1624 words, 13 H2 — adequate for a single tour |
| UX Signals | 11/15 | 49 internal links; single primary CTA/booking path present |
| Schema | 14/15 | Product+Offer+AggregateRating+VideoObject+FAQ — best of the 3 pairs |
| Media | 5/15 | Only 3 images vs marketplace listings' multi-photo galleries |
| Authority | 5/15 | No large review volume; GSC pos ~51 confirms weak relevance signal |
| Freshness | 7/10 | No visible updated date |
| **Total** | **61/100** | |

**3 user stories:**
1. "Show me real photos of the route/views before I book" (marketplaces lead with
   galleries) — page has only 3 images against 1624 words of text.
2. "I want to see this operator's real rating, not just a badge" (booking.com/
   getyourguide show aggregate review counts prominently) — AggregateRating schema
   exists but is not owner-inflatable; needs genuine review volume growth instead.
3. "I want price + group size clarity at a glance" ("до 7 человек", "от ₾175" already
   in title/meta — good match to SERP pattern, keep this).

**Most impactful change:** Expand the photo gallery (3 → 10+ real trip photos) and
surface the video higher on the page; this is the single biggest visible gap vs
marketplace competitors and doesn't require any schema/rating manipulation. Pair with
internal links from the (fixed) day-trip index in Pair 1.

---

## Pair 3 — "tbilisi to kazbegi" → /en/blog/transfer-tbilisi-to-kazbegi/ (GSC pos ~7.6, CTR 1%)

**Target page:** Title "Tbilisi to Kazbegi 2026: Bus ₾15, Shared Taxi ₾25, Private
Driver — Times & Tips", 2405 words, 4 images, schema: BlogPosting+FAQPage+Place+
Person+Organization+EducationalOccupationalCredential+BreadcrumbList (3 blocks).

**Top-10 SERP:** rome2rio (route/transport-options tool) ×2, wander-lush.org (blog
guide), gotrip.ge (blog guide), viator (transfer product/booking), theworldwasherefirst
(blog guide), travelersanddreamers.com (blog guide), awaywiththesteiners.com (blog
guide), **target page itself at position 9**.

**SERP features:** rome2rio-style route/price/duration comparison boxes dominate
above blog results; no local pack/AI Overview text surfaced.

**Dominant type:** Travel blog "how to get there" guide, confidence ~56%; secondary
cluster = route-comparison tool (rome2rio, ~22%).

**Mismatch severity: ALIGNED.** Page IS a transport blog guide matching the dominant
type, and it already ranks on page 1 (~7.6). The problem is not page type — it's
**post-click CTR (1% vs ~3-5% expected at that position)**.

**Gap score (100 pts):**
| Dim | Score | Evidence |
|---|---|---|
| Page Type | 14/15 | Matches dominant blog-guide format |
| Content Depth | 13/15 | 2405 words, 13 H2 — most comprehensive of the 3 pages |
| UX Signals | 10/15 | 50 internal links; no scannable comparison table/route map |
| Schema | 12/15 | BlogPosting+FAQ+Place solid; no Trip/Transfer Offer schema like viator |
| Media | 6/15 | 4 images only; rome2rio wins snippet space with an interactive map |
| Authority | 8/15 | Ranking position 7.6 itself is decent authority evidence |
| Freshness | 8/10 | "2026" in title |
| **Total** | **71/100** | |

**3 user stories:**
1. "Give me the fastest way to compare bus/taxi/private options by price and time in
   one glance" (rome2rio's dominant comparison-box format) — page has the data in
   prose/H2s but no compact comparison table for a rich snippet.
2. "I clicked expecting today's schedule, not a generic guide" — low CTR at pos ~7.6
   suggests title reads as one-of-many guides rather than the most current/specific
   answer; competitors' titles are terser ("How to Travel... 4 Options").
3. "I want to book a private transfer right from this page" (viator ranks with a
   bookable product) — page is informational only, no transfer-booking CTA/Offer.

**Most impactful change:** This is a CTR problem, not a page-type problem — add a
compact comparison table (bus/shared taxi/private, price, duration) near the top to
win the featured-snippet space rome2rio currently owns, and tighten the title/meta to
lead with the single most decision-relevant fact (e.g. exact departure times) to lift
CTR from 1% toward the ~3-5% expected at position ~7.6.

---

## Cross-cutting conclusions

1. **RU pages fail on topical/scale mismatch against marketplaces the site cannot
   structurally clone (owner constraint)**: Pair 1 needs a narrower, intent-matched
   page (day-trip index, not country hub); Pair 2 needs deeper media/trust signals,
   not marketplace-style layout. The fix path is content scope + real photos/reviews,
   never fake ratings or aggregator copy.
2. **EN page (Pair 3) proves page-type alignment isn't enough**: it ranks page-1 with
   the right format but starves on CTR (1%) — the SXO lever there is
   snippet-capture (comparison table) and title specificity, distinct from the RU
   pages' architecture-level fixes.

## Limitations

- SERP data from WebSearch text summaries, not live rendered SERP screenshots — PAA/
  local pack/AI Overview presence could not be visually confirmed, only inferred from
  absence in returned snippets.
- No rank-tracking tool used; GSC position figures were supplied by the user, not
  independently re-verified.
- Domain Authority/backlink data not pulled (no Ahrefs/GSC API call in this run).
