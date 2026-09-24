# Technical SEO Audit — Sakhva Travel
**Date:** 2026-08-08  
**Scope:** Tour card pages RU/EN/GE, hreflang, canonicals, sitemap-tours.xml, crawlability, internal linking, CWV  
**Goal:** Raise commercial tour card pages from pos ~22.5 (RU: 25–48) toward top-5

---

## Score: 61/100

Primary drag: sitemap orphans + EN hub redirect mismatch + one hub card unlinked. EN cards perform (pos 5–15) because EN indexation is intact. RU cards lag (pos 25–48) because ~17 orphan RU card URLs never got proper sitemap coverage, and the hub architecture has a redirect that breaks hreflang trust signals.

---

## CRITICAL

### C1 — `/en/ekskursiya/` redirects 301 → `/en/tours-in-georgia/` (hreflang broken for EN cards)

**What's happening:** Every RU tour card has:
```html
<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/ekskursiya/ekskursiya-kakheti-iz-tbilisi/">
```
But `/en/ekskursiya/` (hub) 301-redirects to `/en/tours-in-georgia/`. This means the EN *hub* hreflang points to a redirect, while EN *cards* correctly live at `/en/ekskursiya/<slug>/` (200 OK). Google follows the redirect for the hub but sees inconsistency — the card-level hreflang for `en` points through a redirected prefix path pattern. This is a trust signal problem: Googlebot may fail to confirm the reciprocal link chain.

**Sitemap compound issue:** sitemap-tours.xml hub entry has hreflang `en` → `/en/tours-in-georgia/` (correct canonical for hub), but individual card entries have hreflang `en` → `/en/ekskursiya/<slug>/` — two different path patterns for "EN" depending on page type. Confusing for crawlers.

**Fix:**
1. Either: keep `/en/tours-in-georgia/` as the canonical EN hub AND ensure all RU cards' hreflang `en` points to `/en/ekskursiya/<slug>/` (current state — ACCEPTABLE for cards, broken only at hub level).
2. Verify the RU hub `/ekskursiya/index.html` hreflang `en` points to `/en/tours-in-georgia/` not `/en/ekskursiya/`. Check and align.
3. Ensure sitemap-tours.xml hub entry consistently uses `/en/tours-in-georgia/` for `en` alternate, and all 71 card entries use `/en/ekskursiya/<slug>/` for `en` alternate. No mixing.

---

### C2 — 8 entries of `rtveli-grape-harvest` in sitemap-tours.xml (confirmed 404)

URL `https://sakhva-travel.com/ekskursiya/rtveli-grape-harvest/` does not exist on disk. Correct slug is `ekskursiya-rtveli-sbor-vinograda`. This 404 appears **8 times** in the sitemap (RU + GE + EN variants and duplicates). Google's crawl budget hits this, logs 404, and the crawl error degrades trust in the sitemap's reliability.

**Fix:** Remove all 8 `rtveli-grape-harvest` entries from sitemap-tours.xml. Add `rtveli-sbor-vinograda` if not already present.

```bash
grep 'rtveli' /Users/vladimir/sakhva-travel/sitemap-tours.xml
```

---

## HIGH

### H1 — 17 RU tour card orphans missing from sitemap-tours.xml

**Confirmed on disk, returning 200, absent from `<loc>` in sitemap-tours.xml:**

| Slug | Commercial intent |
|------|-------------------|
| `ekskursiya-abanotubani` | High — Tbilisi landmark |
| `ekskursiya-ananuri-iz-tbilisi` | High |
| `ekskursiya-bakuriani-iz-tbilisi` | High — ski resort |
| `ekskursiya-dashbashi-iz-tbilisi` | High — canyon |
| `ekskursiya-gori-iz-tbilisi` | High |
| `ekskursiya-gudauri-iz-tbilisi` | High — ski |
| `ekskursiya-hevsuretia-shatili` | High |
| `ekskursiya-jvari-iz-tbilisi` | High |
| `ekskursiya-kakheti-iz-tbilisi` | **VERY HIGH** — pos 38–48 in GSC |
| `ekskursiya-kanyony-zapadnoy-gruzii` | High |
| `ekskursiya-mtatsminda` | High |
| `ekskursiya-mtskheta-iz-tbilisi` | High |
| `ekskursiya-racha-iz-tbilisi` | Medium |
| `ekskursiya-telavi-iz-tbilisi` | High |
| `ekskursiya-truso` | Medium |
| `ekskursiya-uplistsikhe-iz-tbilisi` | High |
| `ekskursiya-ureki-iz-tbilisi` | Medium |

These pages are only discoverable via internal links from the hub. No sitemap signal = Google treats them as lower-priority. Direct correlation: `ekskursiya-kakheti-iz-tbilisi` is at pos 38–48 despite being a top commercial page — absence from sitemap is a confirmed contributing factor.

**Fix:** Add all 17 slugs to sitemap-tours.xml with full RU/EN/GE hreflang blocks. Each block needs all 3 `<xhtml:link>` entries plus x-default.

---

### H2 — EN hub `en/tours-in-georgia/` has no `<loc>` in sitemap-tours.xml

`/en/tours-in-georgia/` is the canonical EN hub (200 OK). It appears only as an `hreflang` target in other entries, never as its own `<loc>`. Google won't treat it as a prioritized URL.

**Fix:** Add one `<url>` block for `https://sakhva-travel.com/en/tours-in-georgia/` with lastmod and hreflang alternates pointing to `ekskursiya/` (RU) and `ge/ekskursiya/` (GE).

---

### H3 — Hub links to 71 cards; 1 card (`ekskursiya-kakheti-iz-tbilisi`) unlinked from hub

Hub `/ekskursiya/index.html` has 71 unique card links but 72 cards exist on disk. The missing one is `ekskursiya-kakheti-iz-tbilisi` — ironically one of the highest-value commercial pages and one of the worst-ranked (pos 38–48). A card not linked from its own hub = 2-click depth broken = weaker PageRank flow.

**Fix:** Add link to `ekskursiya-kakheti-iz-tbilisi` in hub `/ekskursiya/index.html`. Verify same for `/en/tours-in-georgia/` and `/ge/ekskursiya/`.

---

### H4 — `en/ekskursiya/khachapuri-masterclass/` missing from sitemap-tours.xml

Disk has 72 EN cards. Sitemap has 71 EN card `<loc>` entries. Missing: `en/ekskursiya/khachapuri-masterclass/`. The RU and GE variants are in the sitemap but EN is not. This creates an hreflang signal gap: EN version exists but Google won't be told about it via sitemap.

**Fix:** Add `<loc>https://sakhva-travel.com/en/ekskursiya/khachapuri-masterclass/</loc>` entry with hreflang block.

---

## MEDIUM

### M1 — Hreflang x-default should be EN for commercial intent, not RU

On every RU card:
```html
<link href="https://sakhva-travel.com/ekskursiya/ekskursiya-kakheti-iz-tbilisi/" hreflang="x-default" rel="alternate"/>
```
x-default points to the RU version. For a commercial tour site targeting international tourists (EN-speaking buyers are the highest-value segment), x-default should point to the EN version. x-default signals Google which page to serve for unmatched locales — if a user in the US or Germany hits Google, they should get EN, not RU.

**Fix:** Change x-default on all RU cards from RU URL → EN URL (`/en/ekskursiya/<slug>/`). Same change in sitemap-tours.xml. This is a single-template change if cards are generated.

---

### M2 — Category hubs could cannibalize card rankings (controlled risk)

Pages like `/vinnye-tury-gruzia/`, `/goryne-tury-gruzia/`, `/avtorskie-tury-gruzia/` target category keywords ("винные туры Грузия") that overlap with individual wine tour cards. Currently each has its own self-canonical pointing to its own URL — no conflict in canonical chain. However:
- These hub pages rank but their cards don't get full PageRank transfer if the hub doesn't link to enough individual cards.
- Verified: canonicals are correct (no cross-canonical). Risk is keyword overlap, not technical duplication.

**Fix:** Ensure each category hub (`vinnye-tury-gruzia/`) links to all relevant /ekskursiya/ cards with descriptive anchor text. This converts category pages from potential cannibals into PageRank distributors.

---

### M3 — `tury-v-tbilisi/` has zero hreflang in sitemap

Already documented in previous audit. Page in sitemap-pages.xml with no `<xhtml:link>` entries at all. If EN version exists, this is a missed signal. If RU-only, at minimum add `hreflang="ru"` + `hreflang="x-default"`.

---

### M4 — sitemap-index lastmod stale by 10–15 days

| Child sitemap | sitemap-index lastmod | Actual newest |
|---|---|---|
| sitemap-blog.xml | 2026-07-15 | 2026-07-26 |
| sitemap-tours.xml | 2026-07-17 | 2026-07-29 |
| sitemap-landing.xml | 2026-07-14 | 2026-07-24 |
| sitemap-pages.xml | 2026-07-16 | 2026-07-26 |

Google ignores sitemap-index lastmod in practice, but it's a signal to crawlers for re-fetch priority.

---

## LOW

### L1 — 6 foreign country pages in sitemap (thin content risk)

`/turkey/`, `/egypt/`, `/uae/`, `/thailand/`, `/maldives/`, `/vietnam/`, `/cyprus/` are in sitemap-landing.xml. If these are thin placeholder pages with no real content about Georgia tours, they dilute crawl budget and could trigger quality signals. Audit content depth; if under 500 words of unique content → add `noindex` or remove from sitemap.

### L2 — 28 geo-landing pages (RU-only, from-city pattern) — quality gate

`/tury-v-gruziyu-iz-moskvy/` etc. 28 pages × 3 languages = 84 sitemap entries. If city-specific content is just a template with the city name swapped, doorway page risk. Verify unique transport/crossing details per city.

### L3 — robots meta on RU cards uses `max-image-preview:large`

This is correct and positive — allows Google to show large image previews in search. Confirmed on sampled cards. No issue.

---

## Crawlability

| Check | Result |
|---|---|
| robots.txt blocks /ekskursiya/ | PASS — fully open |
| Googlebot / YandexBot explicitly allowed | PASS |
| noindex on tour cards | PASS — all sampled cards have `index,follow` |
| HTTPS | PASS |
| Sitemap declared in robots.txt | PASS — sitemap-index.xml |

---

## Hreflang Summary

| Aspect | Status |
|---|---|
| RU card → EN card (hreflang) | PASS — `/en/ekskursiya/<slug>/` (correct) |
| RU card → GE card (hreflang) | PASS — `/ge/ekskursiya/<slug>/` (correct) |
| EN card → RU card (reciprocal) | PASS |
| GE card → RU card (reciprocal) | PASS |
| EN hub redirect mismatch | FAIL — C1 above |
| x-default → RU (should be EN) | FAIL — M1 above |
| Sitemap hreflang blocks complete | PARTIAL — H4 (khachapuri-masterclass EN missing) |

---

## Internal Linking / Click Depth

| Layer | Depth | Status |
|---|---|---|
| Homepage → Hub (/ekskursiya/) | 1 click | PASS — 46 internal links from homepage |
| Hub → Card | 2 clicks | PASS for 71/72 cards |
| Hub → ekskursiya-kakheti-iz-tbilisi | 2 clicks | FAIL — not in hub (H3) |
| Category hub → Cards | 2–3 clicks | PARTIAL — verify anchor count per category |

All cards are within 3 clicks from homepage. One card (highest-value: Kakheti) is unreachable from hub = effectively 404 from hub's perspective for crawlers.

---

## Core Web Vitals

Previous PSI audits recorded mobile 97–99 (PSI score). No regression indicators found in source:
- Font loading: `onload` lazy + noscript fallback (correct)
- Hero video: MP4 with assumed faststart (per prior audit)
- Inline critical CSS present in `<head>`
- GA4/GTM loaded via `requestIdleCallback` (correct — no TBT impact)
- No render-blocking scripts detected in sampled cards

**Recommendation:** Run PSI on `/ekskursiya/ekskursiya-kakheti-iz-tbilisi/` specifically (the worst-ranked card) to confirm mobile LCP < 2.5s. Card pages may have heavier above-fold images than hub.

---

## Structured Data

- TouristTrip schema: present on all sampled cards ✓
- BreadcrumbList: present, correct depth (Home → Hub → Card) ✓
- FAQPage: present on EN cards ✓; verify RU cards also have it
- VideoObject: present on RU cards (Kakheti confirmed) ✓

---

## Action Priority Table

| Priority | Issue | Fix | Effort |
|---|---|---|---|
| CRITICAL | C1: EN hub redirect breaks hreflang pattern | Verify RU hub hreflang `en` points to `/en/tours-in-georgia/`; align sitemap | 30 min |
| CRITICAL | C2: 8× `rtveli-grape-harvest` 404 in sitemap | Delete from sitemap-tours.xml | 5 min |
| HIGH | H1: 17 RU orphan cards not in sitemap | Add 17 × 3-lang blocks to sitemap-tours.xml | 2 hr |
| HIGH | H2: `en/tours-in-georgia/` no `<loc>` | Add `<loc>` entry to sitemap-tours.xml | 10 min |
| HIGH | H3: Kakheti card unlinked from hub | Add card link to `/ekskursiya/index.html` | 15 min |
| HIGH | H4: EN khachapuri-masterclass missing sitemap | Add `<loc>` entry | 5 min |
| MEDIUM | M1: x-default → RU (change to EN) | Template edit on all cards + sitemap | 1 hr |
| MEDIUM | M2: Category hubs → add card links | Edit category hub pages | 2 hr |
| MEDIUM | M3: tury-v-tbilisi/ hreflang missing | Add xhtml:link block in sitemap | 5 min |
| LOW | L1: Foreign country pages thin content | noindex or expand | varies |
