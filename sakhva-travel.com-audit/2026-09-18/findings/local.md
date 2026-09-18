# Local SEO Audit — sakhva-travel.com — 2026-09-18

## Score: 61/100
GBP signals 14/25, Reviews 8/20, On-page local 15/20, NAP/citations 12/15, Schema 8/10, Links/authority 4/10

## CRITICAL (2)
1. **Schema aggregateRating/review fabrication mismatches verified GBP.** LocalBusiness schema on `/`, `/about/`, `/contacts/` declares `aggregateRating":{"ratingValue":4.9,"reviewCount":90...}` plus 6 fake-looking named `Review` entries (Михаил Д., Виталий, Nugo Shengelia, Amovei, Сергей, Тигран Мартиросов) with no verifiable source. Verified live GBP = 4.6 / 10 reviews. This is a structured-data misrepresentation Google's review-snippet guidelines explicitly ban (self-serving/third-party ratings in schema not sourced from the page) — risk of manual action / rich-result suppression on ALL pages carrying this block.
2. **Google Map embed on `/contacts/` points to a generic Tbilisi pin, not the business listing.** `src="https://www.google.com/maps/embed?pb=...!2sTbilisi%2C%20Georgia...0x16a3c239f9e23da9..."` — this CID/place ref is a generic city landmark, not CID `14112587239859278397` (verified real listing) nor even the old dead one. `hasMap` in schema correctly points to the real CID, but the visible embed users/Google see does not — inconsistent, no GBP click-through/proximity credit from the embed itself.

## HIGH (2)
3. **Unattributed 4.9/90+ claim in visible on-page text.** Hero line `★ 4.9 · 90+ отзывов · от ₾80` (index.html:193) and `about/index.html` meta/OG all state 4.9/90+ with zero source label ("по данным Google/Яндекс/агрегатора") anywhere near it — reads as a direct, unsupported rating claim vs the real 4.6/10 GBP. Confirmed by owner as an aggregate from another platform, but the page gives readers no way to know that.
4. **Old dead-listing CID absent (good) but sameAs coverage confirms only Tripadvisor + Yandex + Google Maps as review-bearing citations** — no BBB-equivalent for Georgia (n/a, correctly not chasing GetYourGuide/Viator per owner's business choice), but nothing plugs the review-count gap (18-day freshness rule): with only 10 real GBP reviews and no visible velocity signal on-page, ranking-cliff risk if review cadence stalls.

## MEDIUM (2)
5. **Address never appears as visible text**, only inside `<script type="application/ld+json">` on `/`, `/about/`, `/contacts/` (`14 Merab Kostava St, 0108, Тбилиси, GE` — consistent across all 3, no discrepancy). For a private guide with no walk-in office this may be intentional (SAB reality vs brick-and-mortar schema), but declaring a full street address in schema while never showing it to users is a mixed signal — clarify office vs base-of-operations, or drop street-level schema address if it's not a public location.
6. Phone/name fully consistent everywhere checked: `+995511272623` identical in visible tel: links, body text, and all 3 schema blocks on `/`, `/about/`, `/contacts/`. One unrelated `+7 928 634 5100` appears in `about/index.html` — appears to be a testimonial/case-context number, not a business NAP field; flag only if it renders near contact info.

## LOW (1)
7. Hub pages `/tury-v-gruziyu/` (3523 words) vs `/ekskursiya/` (2491 words) are not near-duplicate by length; content is differentiated, no doorway-page pattern detected in this sampling. Deeper per-city pages under `tury-v-gruziyu-iz-*` not sampled for uniqueness in this pass — recommend spot-checking those (per-origin-city variants are the classic doorway risk).

## Verified OK
- hreflang: ru/en/ka/x-default present and correct on `/`, `/about/`, `/contacts/`.
- Schema subtype `["TravelAgency","LocalBusiness"]`, geo 7-decimal precision, openingHoursSpecification 08:00–22:00, priceRange, areaServed all present.
- No live page links the dead old CID `14070083063461040701`.
- sameAs includes correct new CID URL and correct Yandex Business ID.

## Limitations
No live crawl performed (static source read only, per instructions); GBP/Yandex/Tripadvisor live pages not fetched — findings rely on grep across local HTML source and owner-supplied verified facts. Doorway-page uniqueness only spot-checked on 2 of ~10+ hub-type pages.
