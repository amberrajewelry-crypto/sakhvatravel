# Schema.org Audit — sakhva-travel.com (2026-09-17)

**Score: 78/100**

Pages checked: `/`, `/en/`, `/about/`, `/contacts/`, `/ekskursiya/vinniy-marshrut-alazani/`,
`/ekskursiya/khachapuri-master-klass/`, `/ekskursiya/art-tur-tbilisi/`,
`/blog/rayony-tbilisi-gde-ostanovitsya/`, `/blog/tury-v-gori-2026/`,
`/pogoda/tbilisi/`, `/pogoda/adjara/`, `/tury-v-gruziyu-iz-kazani/` (landing).

## Detection summary

| Page | Types found |
|---|---|
| `/` | WebSite, TravelAgency/LocalBusiness, Person(founder), Product×10, ItemList, VideoObject, FAQPage, BreadcrumbList, Service×4 |
| `/en/` | WebSite, TravelAgency/LocalBusiness, Person, TouristTrip×10, ItemList, VideoObject, FAQPage, Review×5, BreadcrumbList, Service×4 |
| `/about/` | ProfilePage, Person, FAQPage |
| `/contacts/` | WebPage, TravelAgency |
| tour pages (3) | WebPage, TouristTrip, BreadcrumbList, FAQPage, Product, VideoObject |
| blog posts (2) | BlogPosting, BreadcrumbList, FAQPage |
| pogoda pages (2) | WebPage, BreadcrumbList, FAQPage |
| landing (kazan) | TravelAgency, WebPage, BreadcrumbList, FAQPage, Product(AggregateOffer) |

No HowTo, no SpecialAnnouncement, no CourseInfo/EstimatedSalary/LearningVideo anywhere — clean on deprecated types.

## Validation results

**Ratings — PASS (no fabrication).** `AggregateRating {ratingValue:4.9, reviewCount:90}` appears only on the `TravelAgency`/`LocalBusiness` `#business` entity on `/` and `/en/`, matches the real 4.9/90 figure given, and is not duplicated onto every `Product`/`TouristTrip` (would have been fabricated per-tour data). Correctly, no `aggregateRating`/`review` was added to tour `Product` blocks. Note: self-serving reviews/ratings on your own Organization/LocalBusiness are ignored by Google for rich results — this hurts nothing but also earns nothing in SERP; keep it for AI/LLM citation value only. Severity: Info.

**TravelAgency/LocalBusiness NAP — PASS on `/`.** Full NAP, `geo`, `openingHoursSpecification` (Mo–Su 08:00–22:00), `sameAs` (11 profiles), `hasOfferCatalog`, `areaServed` with Wikidata `sameAs`. Solid.

**TravelAgency entity consistency — FAIL (Critical).** The same `@id: https://sakhva-travel.com/#business` is restated with three different, incomplete property sets:
- `/contacts/`: uses `openingHours: "Mo-Su 08:00-22:00"` (string) instead of `openingHoursSpecification`, drops `legalName`, `logo`, `sameAs`, `hasOfferCatalog`.
- `/tury-v-gruziyu-iz-kazani/` (landing): drops `geo`, `openingHours` entirely, drops `postalCode`/`streetAddress`, drops `sameAs`, `logo`.
Since it's the same `@id`, Google's entity graph may merge conflicting/partial data unpredictably per crawl. Fix: either (a) restate the identical full object every time, or (b) reference `{"@id":"https://sakhva-travel.com/#business"}` only and let `/` be the canonical full definition (Google does support cross-page @id linking within the same site, but only reliably when tested per-URL — safest is to keep the full block only where it's rendered, and keep a **consistent subset** everywhere else).

**Product used for services — WARN (Medium).** Tours are marked `@type: Product` with `Offer`/`AggregateOffer` (home, 3 tour pages, landing). Schema.org allows this, but Google's structured data guidelines direct services/experiences to `Service` or `TouristTrip`, not `Product` — `Product` rich results are scoped to physical/merchant goods and increasingly gated behind Merchant Center policies. You already use `TouristTrip` correctly on `/en/` and inside the tour pages' own dedicated `TouristTrip` block — the parallel `Product` block on the same tour pages is redundant and the higher-risk one for a Search Console "Product" warning. Recommend dropping `Product` on tour pages/home listing in favor of the existing `TouristTrip`+`Offer`, or downgrading to `Service`.

**BlogPosting — PASS.** Both posts have `headline`, `author` (Person with `@id`, credential), `datePublished`, `dateModified`, `publisher` w/ logo, `image`, `mainEntityOfPage`, `wordCount`, `inLanguage`. No gaps.

**BreadcrumbList — PASS** everywhere checked (tour pages, blog, pogoda, landing). Absolute URLs, correct `position`.

**VideoObject — PASS.** All 5 instances (`/`, `/en/`, 3 tour pages) have `name`, `description`, `thumbnailUrl`, `contentUrl`, `uploadDate`, `duration` — the three Google-required fields are present everywhere. Minor: tour-page videos lack `publisher` (optional, home/en have it) — cosmetic only.

**FAQPage — Info only, not Critical (per current Google policy: FAQ rich results retired site-wide as of 2026-05-07).** Present on `/`, `/about/`, all 3 tour pages, both blog posts, both pogoda pages, and the landing page — 9 of 12 pages checked. No SERP benefit for any of them now, gov/health or not. Keep as-is for AI/LLM answer-extraction value; do not spend more effort adding it net-new, and do not remove what exists.

**WebSite SearchAction — FAIL (missing).** `WebSite` block on `/` and `/en/` has `name`, `url`, `alternateName`, `description`, `inLanguage` but no `potentialAction` (`SearchAction`) — no Sitelinks Searchbox eligibility. Low traffic impact for this site size, but zero-cost to add if a working search endpoint exists.

**hreflang / inLanguage — FAIL (Critical, cross-cutting).** `/ge/` (Georgian locale) exists, is in the sitemaps, and has its own JSON-LD with `"inLanguage":"ka"` — but:
- `WebSite.inLanguage` on `/` and `/en/` is `["ru","en"]` only, missing `"ka"`.
- No page anywhere (checked `/`, `/en/`, `/ge/`) emits an `hreflang="ka"` alternate link — `/ge/` only self-declares `ru`/`en` alternates, never `ka`, and `/`/`/en/` never reference `/ge/` at all.
This orphans the Georgian locale from hreflang clustering entirely; search engines can't associate `/ge/*` with its `ru`/`en` counterparts, which also undermines the `inLanguage`/`WebSite` schema signal consistency the audit was asked to check.

## Ready-to-paste JSON-LD — top 3 fixes

### 1. WebSite SearchAction (add to the existing `WebSite` node in the `/` and `/en/` `@graph`)
```json
{
  "@type": "WebSite",
  "@id": "https://sakhva-travel.com/#website",
  "url": "https://sakhva-travel.com/",
  "name": "Sakhva Travel",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://sakhva-travel.com/search/?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```
Skip if no working `/search/?q=` endpoint exists — do not point this at a URL that doesn't return results.

### 2. Consistent `#business` entity on secondary pages (replace the partial restatements on `/contacts/` and the landing page)
```json
{
  "@context": "https://schema.org",
  "@type": ["TravelAgency", "LocalBusiness"],
  "@id": "https://sakhva-travel.com/#business",
  "name": "Sakhva Travel",
  "legalName": "ИП Сахвадзе Т.В.",
  "url": "https://sakhva-travel.com/",
  "telephone": "+995511272623",
  "email": "help@sakhva-travel.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "14 Merab Kostava St",
    "addressLocality": "Тбилиси",
    "postalCode": "0108",
    "addressCountry": "GE"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 41.7250505, "longitude": 44.7789235 },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "08:00",
    "closes": "22:00"
  },
  "sameAs": [
    "https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html",
    "https://www.google.com/maps?cid=14070083063461040701"
  ]
}
```
Use this exact shape (or a straight copy of the `/` block) on `/contacts/` and the landing pages instead of the current stripped-down variants.

### 3. `ka` locale in hreflang + WebSite.inLanguage
Add to `<head>` of `/`, `/en/`, and `/ge/`:
```html
<link rel="alternate" hreflang="ka" href="https://sakhva-travel.com/ge/">
<link rel="alternate" hreflang="ru" href="https://sakhva-travel.com/">
<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/">
<link rel="alternate" hreflang="x-default" href="https://sakhva-travel.com/">
```
And update the `WebSite` JSON-LD:
```json
"inLanguage": ["ru", "en", "ka"]
```

## Not recommended / left as-is
- Do not add `HowTo`, `SpecialAnnouncement`, `CourseInfo`. None present — good.
- Do not add `aggregateRating`/`review` to individual tour `Product`/`TouristTrip` items — no per-tour review data exists; would be fabrication.
- Do not remove existing `FAQPage` blocks — no SERP loss from keeping them, real loss (AI/LLM citation) from removing them.
