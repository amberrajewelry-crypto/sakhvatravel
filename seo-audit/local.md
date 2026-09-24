# Local SEO Audit: sakhva-travel.com

**Date:** 2026-05-04
**Auditor:** Claude Opus 4.6 (automated)
**Business:** Sakhva Travel (private tour guide, Tbilisi, Georgia)

---

## Local SEO Score: 74 / 100

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| GBP Signals | 25% | 78 | 19.5 |
| Reviews & Reputation | 20% | 82 | 16.4 |
| Local On-Page SEO | 20% | 80 | 16.0 |
| NAP Consistency & Citations | 15% | 65 | 9.8 |
| Local Schema Markup | 10% | 75 | 7.5 |
| Local Link & Authority Signals | 10% | 48 | 4.8 |
| **TOTAL** | | | **74.0** |

---

## Business Type Detection

**Detected: Service Area Business (SAB) / Hybrid**

Signals:
- No visible street address (only "Tbilisi, Georgia, 0105")
- Service area declared in schema: Tbilisi, Kazbegi, Kakheti, Georgia
- Guide comes to tourists (meeting point model)
- Google Maps embed present with CID (hybrid signal)
- GBP CID: 14070083063461040701 -- verified on site

**Industry vertical: Tour / Travel (tour guide services)**

Signals: TouristTrip schema, tour pricing, guide bio, booking flow, TripAdvisor badge, multilingual (RU/EN)

---

## NAP Consistency Audit

### Source Comparison

| Field | HTML visible | JSON-LD schema | Meta tags | WhatsApp links |
|-------|-------------|----------------|-----------|----------------|
| Name | Sakhva Travel | Sakhva Travel | Sakhva Travel | -- |
| Address | Tbilisi, Georgia | Tbilisi, 0105, GE | -- | -- |
| Phone | +995 511 272 623 | +995511272623 | -- | wa.me/995511272623 |
| Email | help@sakhva-travel.com | help@sakhva-travel.com | -- | -- |

### Issues Found

- **MINOR**: Phone format inconsistency -- visible text uses `+995 511 272 623` (with spaces), schema uses `+995511272623` (no spaces). Both are valid E.164, but Google prefers consistent formatting. Recommend: use `+995 511 272 623` everywhere for readability, `+995511272623` in schema tel: links.
- **OK**: Name, email are consistent across all sources.
- **OK**: RU and EN versions share identical NAP data.

---

## GBP Signals on Website

| Signal | Status | Details |
|--------|--------|---------|
| Google Maps embed | YES | iframe with pb= parameter, coordinates 41.7250505, 44.7789235 |
| Google Maps CID link | YES | cid=14070083063461040701, used in schema hasMap and footer |
| Google Maps place link | YES | Full place URL with @coordinates and place_id |
| Review widget | PARTIAL | Custom review section with 3 reviews, not live Google widget |
| GBP photos referenced | NO | No Google Places photo API integration |
| GBP posts indicators | NO | No GBP post embeds on site |
| Directions link | NO | No "Get Directions" button found |
| "Write a review" CTA | NO | No link encouraging Google reviews |

**Score: 78/100** -- strong Maps integration, missing review CTA and live widget

---

## Review Health Snapshot

| Metric | Value | Assessment |
|--------|-------|------------|
| Platform | Google (via schema) | Primary |
| Rating | 4.9 / 5.0 | Excellent |
| Review count | 87 | Good for niche SAB |
| Reviews in schema | 3 individual + AggregateRating | OK |
| TripAdvisor | Travellers' Choice badge linked | Strong signal |
| Review velocity | Unknown (no dates visible) | Cannot assess 18-day rule |
| Response rate | Unknown from site | Need GBP panel to verify |
| Review diversity | RU names visible (Tigran, Giorgi, Nugo) | Matches target audience |

**Recommendations:**
1. Add `datePublished` to Review objects in schema
2. Add "Leave a review" CTA linking to Google review URL
3. Rotate displayed reviews periodically (freshness signal)
4. Add EN reviews for the English version
5. Display review count from multiple platforms (Google + TripAdvisor combined)

---

## Local Schema Validation

### Main Page (index.html)

| Property | Status | Value |
|----------|--------|-------|
| @type | TravelAgency | CORRECT for tour agency |
| name | YES | "Sakhva Travel" |
| address | YES | PostalAddress with locality, region, postalCode, country |
| geo | YES | 41.7250505, 44.7789235 (7 decimal precision) |
| telephone | YES | +995511272623 |
| email | YES | help@sakhva-travel.com |
| url | YES | https://sakhva-travel.com/ |
| openingHoursSpecification | YES | Mon-Sun 08:00-22:00 |
| aggregateRating | YES | 4.9, 87 reviews |
| areaServed | YES | Tbilisi, Kazbegi, Kakheti, Georgia |
| sameAs | YES | Instagram, Telegram, YouTube, TripAdvisor, Google Maps |
| hasMap | YES | Google Maps CID URL |
| priceRange | YES | GEL 77-595 |
| image/logo | YES | logo-schema.webp |
| Person (guide) | YES | Timur, jobTitle, worksFor, knowsLanguage |
| TouristTrip (x12) | YES | All tours with Offer, duration |
| FAQPage | YES | 9 Q&A pairs |
| VideoObject | YES | Promo video |
| BreadcrumbList | YES | Present |
| ItemList | YES | 12 tours catalogued |

### Issues

1. **MEDIUM**: `@type` is `TravelAgency` -- consider adding `["TravelAgency", "TourProvider"]` as array type for better specificity. Google supports multi-type.
2. **MEDIUM**: `areaServed` on main page has 2 variants (4 items vs 2 items in Person schema) -- consolidate.
3. **LOW**: `addressRegion` = "Tbilisi" -- should be region name or omit for city-states.

### Tour Pages

| Page | JSON-LD | TouristTrip | TravelAgency | FAQPage | Reviews | areaServed |
|------|---------|-------------|--------------|---------|---------|------------|
| kazbegi | YES | YES | Inline | NO | NO | NO |
| kakheti | YES | YES | Inline | NO | NO | NO |
| kutaisi | YES | YES | Inline | NO | NO | NO |
| batumi | YES | YES | YES | YES | YES | NO |
| mtskheta | YES | YES | Inline | NO | NO | NO |
| old-tbilisi | YES | YES | YES | YES | NO | NO |
| night-tbilisi | YES | YES | YES | YES | YES | NO |
| dinner | YES | YES | YES | YES | YES | NO |
| digital-nomad | YES | YES | YES | YES | YES | NO |
| emigrant | YES | YES | YES | YES | YES | NO |
| slow-travel | YES | YES | YES | YES | YES | NO |
| soviet | YES | YES | YES | YES | YES | NO |

**Critical finding**: 5 of 12 tour pages (kazbegi, kakheti, kutaisi, mtskheta, old-tbilisi) have significantly less rich schema than the other 7. They lack FAQPage, standalone TravelAgency, and Review data. These are the most popular tours.

---

## Citation Presence (Tier 1 Directories)

| Directory | Status | Notes |
|-----------|--------|-------|
| Google Business Profile | YES | CID 14070083063461040701, verified |
| TripAdvisor | YES | Travellers' Choice, linked in sameAs |
| Instagram | YES | @sakhvatravel, linked in sameAs |
| YouTube | YES | @SakhvaTravel, linked in sameAs |
| Telegram | YES | @SakhvaGuideBot |
| Yelp | NOT FOUND | No Yelp link or mention on site |
| BBB | N/A | Not applicable (Georgia, not US) |
| Yandex Maps | UNKNOWN | Not linked, relevant for RU audience |
| 2GIS | UNKNOWN | Popular in CIS, relevant for target audience |
| Booking.com | UNKNOWN | Not found on site |
| Viator/GetYourGuide | UNKNOWN | Not found on site |
| TourRadar | UNKNOWN | Not found on site |

**Score: 65/100** -- core platforms present, missing tour-specific directories

---

## Location Page Quality

This is a single-location SAB, so multi-location assessment is N/A.

### Service (Tour) Page Quality

| Metric | Assessment |
|--------|------------|
| Total tour pages | 12 RU + 12 EN = 24 |
| Category pages | 3 RU + 3 EN (day-trips, walking, wine) |
| Unique content | HIGH -- each page has unique itinerary, photos, FAQ |
| Word count range | 2,200 - 3,100 words per tour page |
| Doorway page risk | LOW -- pages have genuinely different content |
| Internal linking | GOOD -- ItemList in schema, nav links, breadcrumbs |
| hreflang | YES -- ru/en on all pages |
| Canonical | Needs verification per page |

### Blog

- 42 RU articles, 10 EN articles
- 207 URLs in sitemap
- Content supports local topical authority

---

## Service Area Optimization

| Factor | Status | Notes |
|--------|--------|-------|
| Schema areaServed | YES | Tbilisi, Kazbegi, Kakheti, Georgia |
| City/region in H1 | YES | "Tbilisi" in main H1 |
| Service + location in titles | YES | "Kazbegi from Tbilisi", "Kakheti tour from Tbilisi" |
| Landing pages per service area | PARTIAL | Tours cover areas but no dedicated "Tbilisi tours" hub |
| Geo-modified content | YES | Each tour page references specific Georgian locations |
| Local landmarks mentioned | YES | Ananuri, Gergeti, Sighnagi, Svetitskhoveli etc. |
| Language targeting | YES | RU for primary, EN for secondary |

---

## Local Link & Authority Signals

| Signal | Status |
|--------|--------|
| TripAdvisor backlink | YES (Travellers' Choice) |
| Google Maps listing | YES |
| Local directory listings | UNKNOWN -- need backlink audit |
| Local tourism board link | UNKNOWN |
| .ge domain | NO (uses .com) |
| Local press/blog mentions | UNKNOWN |
| Partnership pages (hotels, restaurants) | NO |

**Score: 48/100** -- limited verifiable local authority signals from site data alone

---

## Industry-Specific Findings (Tour / Travel)

1. **Schema type**: `TravelAgency` is acceptable but `TourProvider` (proposed schema.org pending) would be more specific. Current setup is correct.
2. **TouristTrip schema**: Excellent -- 12 trips with Offer, duration, itinerary, touristType. This is best-in-class for tour operators.
3. **No `TouristAttraction` on main page**: Tour pages (batumi, old-tbilisi) use TouristAttraction -- good. Main page could benefit from it too.
4. **Booking flow**: WhatsApp + Telegram as primary booking -- no structured booking schema (ReservationAction). Not critical but would enhance.
5. **Multilingual**: Proper hreflang ru/en with x-default. Strong for reaching both audiences.
6. **Price transparency**: Prices visible in schema Offers (GEL currency). Google can surface in rich results.
7. **AI visibility**: llms.txt present, robots.txt allows all AI crawlers. Forward-thinking.

---

## Top 10 Prioritized Actions

### Critical (impact on rankings)

1. **Enrich schema on top 5 tour pages** (kazbegi, kakheti, kutaisi, mtskheta, old-tbilisi) -- add FAQPage, AggregateRating, Review objects to match the other 7 pages. These are the highest-traffic pages with the weakest schema.

2. **Add "Write a Review" CTA** -- link to `https://search.google.com/local/writereview?placeid=ChIJi8gUuPEHQkAR3dKFrVL72cM` on the reviews section. Review velocity is the #2 GBP factor; direct prompting increases it.

3. **Register on tour-specific directories** -- Viator, GetYourGuide, TourRadar, Klook. These are Tier 1 citations for tour operators. 3 of top 5 AI visibility factors are citation-related (Whitespark 2026).

### High (measurable improvement)

4. **Add Yandex Maps and 2GIS listings** -- critical for Russian-speaking audience. Create and link back to sakhva-travel.com with consistent NAP.

5. **Add `areaServed` to all 12 tour page schemas** -- currently only on main page. Each tour page should declare its specific service area (e.g., Kazbegi page: Stepantsminda, Kazbegi municipality).

6. **Add `datePublished` to Review schema objects** -- required for review rich results eligibility. Currently reviews lack dates.

7. **Create a "Tbilisi Tours" hub page** (`/tours/tbilisi/`) -- dedicated service area landing page for the primary market. This is the #1 local organic factor per Whitespark 2026.

### Medium (incremental)

8. **Add structured FAQ to the 5 tour pages missing it** -- FAQ schema drives position zero. Pages kazbegi, kakheti, kutaisi, mtskheta, old-tbilisi need FAQ sections.

9. **Add local partnership signals** -- reach out to Tbilisi hotels, hostels, restaurants for reciprocal links or "recommended tours" pages. Local backlinks are key authority signals.

10. **Consolidate phone format** -- standardize visible phone to `+995 511 272 623` across all pages, use `tel:+995511272623` in href attributes.

---

## Limitations Disclaimer

The following could not be assessed without paid tools or GBP panel access:

- **Live GBP data**: Primary/secondary categories, GBP post activity, Q&A section, photo count and types, GBP Insights (searches, views, actions)
- **Review velocity**: No access to review dates or frequency from site data
- **Review response rate**: Requires GBP panel or Google Places API with reviews
- **Citation accuracy**: Could not verify NAP on external directories (Yandex Maps, 2GIS, TripAdvisor) -- only confirmed presence/absence of links
- **Backlink profile**: Local link authority requires Ahrefs/Moz/Majestic data
- **Local pack position**: Real-time SERP position for target keywords not checked
- **Competitor gap**: No comparison with competing Tbilisi guides performed
- **Google Ads local extensions**: Not audited
- **Proximity factor**: Accounts for 55.2% of ranking variance (Search Atlas) -- outside optimization control, depends on searcher location
