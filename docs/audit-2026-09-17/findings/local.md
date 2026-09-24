# Local SEO Audit — sakhva-travel.com
Date: 2026-09-17 | Method: raw HTML fetch (curl), no JS render, no live GBP/Tripadvisor API check

## Score: 78/100

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| GBP Signals | 25% | 20/25 | Real Place ID + CID linked, Maps embed present, no on-page GBP review widget/posts feed |
| Reviews & Reputation | 20% | 15/20 | 4.9/90 aggregateRating consistent, linked to Google Maps place; no visible owner-response evidence; Tripadvisor listed but not schema-linked |
| Local On-Page SEO | 20% | 17/20 | Strong destination-page coverage, local keywords in titles/H1, but titles inconsistent RU vs EN vs KA pattern |
| NAP Consistency & Citations | 15% | 12/15 | Phone/address identical across all checked pages+schema; GetYourGuide/Viator not verified as live listings |
| Local Schema Markup | 10% | 9/10 | Correct TravelAgency+LocalBusiness, geo 7-decimal precision, openingHoursSpecification, E.164 phone; minor: about.html Person schema has no geo/telephone (acceptable — not the business node) |
| Local Link & Authority Signals | 10% | 5/10 | Tripadvisor link found; GetYourGuide/Viator not confirmed as real profiles (only appears as FAQ text "Viator?"); no BBB (not applicable — not a US business) |

## Business type
Hybrid: has a real street address in schema/footer (14 Merab Kostava St, Tbilisi 0108) + Google Maps Place ID (`0x604207f1b914c88b:0xc3d9fb52ad85d23d`, CID `14070083063461040701`), AND serves a wide area (areaServed: Тбилиси, Казбеги, Кахетия, Мцхета, Грузия). This is a legitimate GBP-linked storefront/office address, not a fake SAB address — confirms real GBP profile "Sakhva Travel" exists.

## Industry vertical
Tour operator / travel agency (TravelAgency schema — correct subtype, better than generic LocalBusiness). Local keyword coverage strong: "гид Тбилиси", "экскурсии Тбилиси", "туры по Грузии", "Kazbegi/Kakheti/Svaneti/Batumi tours".

## NAP consistency (source comparison)

| Source | Name | Phone | Address |
|---|---|---|---|
| Home HTML/schema | Sakhva Travel | +995511272623 | 14 Merab Kostava St, Тбилиси 0108, GE |
| /contacts/ HTML/schema | Sakhva Travel | +995511272623 | 14 Merab Kostava St, Тбилиси 0108, GE |
| /about/ HTML | (Тимур Сахвадзе, guide persona) | +995511272623 | not repeated (Person schema, no address — expected) |
| /en/ | Sakhva Travel | +995511272623 | 14 Merab Kostava St, Tbilisi 0108, GE |
| /ge/ | Sakhva Travel | +995511272623 | (not independently re-verified, phone matches) |
| Google Maps embed/place link | Sakhva Travel | — | matches lat/lng 41.7250505, 44.7789235 |

**No discrepancies found.** Phone is consistently E.164-clean (+995511272623) in schema and displayed as "+995 511 272 623" in visible text — correct pattern (display formatted, tel:/schema raw).

## GBP optimization checklist

| Signal | Status |
|---|---|
| Maps embed on page | Present (2 iframes: business pin + Tbilisi overview) |
| Direct Google Maps place link | Present (`google.com/maps/place/SakhvaTravel/...`) |
| Maps short link (maps.app.goo.gl) | Present |
| CID reference | Present (`?cid=14070083063461040701`) |
| Review widget / rating badge on page | Rating shown as static text "4.9/5 · 90+ отзывов" — not a live embedded widget |
| GBP posts indicator | Not detected |
| Photo evidence tied to GBP | Not verifiable from HTML alone |

## Review health snapshot
- Rating: 4.9 / 5, reviewCount: 90 (schema aggregateRating, consistent RU/EN/KA)
- Source: implied Google (given Maps place link adjacency) — **not explicitly cited** in schema (no `sameAs` linking aggregateRating to the Google Maps listing) — this is a missed trust signal
- Velocity: cannot assess from static HTML (no review dates/timeline visible) — flagged as limitation
- Response rate: cannot assess — no visible replies

## Citation presence
- Google Business Profile: confirmed real (Place ID + CID + short link present and internally consistent — strong signal profile exists and is claimed)
- Tripadvisor: listing URL present in HTML (`Attraction_Review-g294195-d15318013...`), not independently verified live
- GetYourGuide / Viator: **no real listing links found** — only appears as plain text "Viator?" (likely FAQ copy, e.g. "own site vs Viator"), not a citation
- BBB: not applicable (Georgia-based, not US)

## Location/landing page structure
- sitemap-tours.xml: 245 URLs, strong destination coverage — Kazbegi 78, Batumi 66, Kakheti 45, Svaneti 30, Mtskheta 15 (RU/EN/KA variants)
- sitemap-landing.xml: 124 URLs — these are **origin-city pages** ("туры в Грузию из Казани/Нальчика/..."), a programmatic SEO pattern for RU-speaking source markets, not destination location pages. Doorway-page risk if these are thin/duplicated — not assessed for uniqueness % in this pass (would need per-page content diff).

## Top 10 prioritized actions

1. **[High]** Link aggregateRating schema to its source via `sameAs`/`review` pointing to the Google Maps listing URL — currently rating floats unattributed in schema.
2. **[High]** Verify/create real GetYourGuide and Viator listings — 3 of top-5 AI-visibility factors are citation-related; currently these are absent as real citations, appearing only as FAQ text.
3. **[Medium]** Add live review velocity signal (visible review dates or a rotating widget) — 18-day rule means stale review appearance risks ranking cliffs even if backend is fine.
4. **[Medium]** Audit sitemap-landing.xml (124 origin-city pages) for unique-content % — programmatic city-swap pages are a classic doorway-page red flag if templated with only city name changed.
5. **[Medium]** Add explicit GBP review widget (not static text) to homepage to make rating a live trust signal, not just schema text.
6. **[Low]** about.html Person schema for guide Тимур has no `telephone`/geo — acceptable since business schema carries it, but consider `worksFor.telephone` link for AI-answer engines.
7. **[Low]** Confirm /ge/ page NAP matches exactly (only phone spot-checked, not full address string) — full ka-locale schema pass recommended.
8. **[Low]** Add openingHoursSpecification per-day granularity if actual hours vary (currently uniform Mo-Su 08:00-22:00, likely fine for SAB tour guide).
9. **[Low]** Confirm GBP primary category is correct (e.g., "Tour operator" not generic "Travel agency") — cannot verify without GBP dashboard/API access; wrong category is the #1 negative ranking factor.
10. **[Low]** Add photo/post freshness indicators to page if GBP posts are active — not currently surfaced anywhere in HTML.

## Limitations disclaimer
- No JS-render pass performed (raw curl fetch only) — if any GBP widget, reviews carousel, or Maps interaction is client-side injected beyond the two static iframes found, it was not captured.
- No live query to Google Business Profile, Tripadvisor, GetYourGuide, or Viator (no WebSearch/DataForSEO tool invoked this pass) — GBP category, live review count/velocity, and citation NAP-match on those platforms are inferred, not confirmed.
- Doorway-page duplicate-content check on the 124 origin-city pages not performed (would require pairwise content diff).
- Proximity (55.2% of ranking variance per Search Atlas) is outside site control and not scored here.
