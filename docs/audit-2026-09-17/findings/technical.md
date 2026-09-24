# Technical SEO Audit — sakhva-travel.com (2026-09-17)

## Score: 90/100

Static HTML on Vercel + Cloudflare, no JS-rendering dependency, security headers strong, sitemap/robots clean, canonicals/hreflang correct on 500 sampled pages. Two real bugs found, rest is polish.

## 1. Crawlability — PASS (95/100)
- robots.txt: valid, `Allow: /`, correct disallows (/dashboard/, /partner/, /demo/, /scripts/, /service-account.json), explicit allow-list for AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.), blocks CCBot/cohere-ai/MJ12bot/DotBot/Bytespider. Sitemap directive present.
- sitemap-index.xml: valid, 5 sub-sitemaps, `blog:357 + tours:245 + landing:124 + pages:83 + pogoda:66 = 875` — matches stated total exactly.
- All 500 sampled URLs returned status 200 (no sitemap 404/redirect leaks).
- `/sitemap.xml` → 301 → `/sitemap-index.xml` (clean, 1 hop).
- **Low**: legacy `/sitemap.xml` still 301s instead of sitemap referencing canonical name directly everywhere external tools might probe — no action needed, works fine.

## 2. Indexability — PASS with 1 High bug (85/100)
- 0 missing titles/descriptions/H1, 0 duplicate titles, 0 duplicate descriptions, 0 duplicate canonicals, 0 canonical/self-URL mismatches, 0 unintended noindex across 500 pages.
- **High — duplicate `<title>` element in raw HTML on at least 3 pages** (invalid markup, confuses crawlers/tools that grab the first vs. last title):
  - `https://sakhva-travel.com/blog/metro-tbilisi/` — head has `<title>Метро Тбилиси 2026 — схема, карта, цены и как пользоваться</title>`, then a **second** `<title>` tag at line 321, inside an inline SVG (`<title>Схема метро Тбилиси 2026 — карта линий и станций</title>` — SVG `<title>` accessibility element, not deduped/namespaced from HTML `<title>`).
  - Same pattern on `/en/blog/tbilisi-metro-guide/` and `/ge/blog/tbilisi-metro-guide/`.
  - Root cause: the SVG metro-map partial uses a literal `<title>` element for its own a11y label; regex/DOM title-extractors (and possibly some SEO crawlers) see two `<title>` tags in the document and some tools concatenate them.
  - Fix: rename the SVG's accessibility title to `<desc>` or `aria-label` on the `<svg>` element, or wrap it in `<svg><title>...</title></svg>` — it's technically valid per-SVG but should never share the tag name at document-scan level; simplest fix is `<title>` → `<desc>` inside the SVG (SVG spec supports both, `<title>` is just the common one but any tooling scanning raw HTML for `<title>` will hit it).
- **Low — 3 titles >60 chars** (SERP truncation risk): the same metro-tbilisi trio above once title is fixed will likely resolve length too — check length after the SVG fix.
- **Low — 4 meta descriptions 161–165 chars** (soft truncation in SERP, ~1–5 chars over Google's ~155-160 practical cutoff): `/en/blog/residence-permit-georgia/`, `/en/blog/document-translation-notary-georgia/`, `/ge/blog/document-translation-notary-georgia/`, `/en/blog/company-registration-georgia/`. Trim to ≤155 chars.
- **Low — 12 titles <30 chars** (per coordinator crawl stats) — under Google's ~30-60 char sweet spot, some SERP real estate left on the table; not broken, just short. No URLs supplied by crawl summary; low priority, revisit when touching those templates.
- No thin content: median 1720 words/page, min sampled well above 300.

## 3. Security — PASS (100/100)
Headers on `/` (Cloudflare + Vercel):
- `strict-transport-security: max-age=31536000; includeSubDomains; preload` — HSTS preload-ready.
- `content-security-policy`: `default-src 'self'` with explicit allow-lists per directive (script-src, style-src, img-src, connect-src, frame-src) — no wildcard `*`, no `unsafe-eval`. Good.
- `x-frame-options: DENY`, `x-content-type-options: nosniff`, `x-permitted-cross-domain-policies: none`, `referrer-policy: strict-origin-when-cross-origin`, `permissions-policy: camera=(), microphone=(), geolocation=()`, `cross-origin-opener-policy: same-origin-allow-popups`.
- HTTPS enforced: `http://` → 301 → `https://` in one hop.
- `www.sakhva-travel.com` → 301 → apex in one hop.
No findings.

## 4. URL Structure / Redirects — PASS with 1 Medium (85/100)
- Clean, lowercase, hyphenated URLs; locale prefixes `/en/`, `/ge/` consistent; ru is root (no `/ru/` prefix) — standard and fine.
- Trailing-slash normalization works (`/tours` → 308 → `/tours/`).
- **Medium — 2-hop redirect chain for legacy tour slugs**: `GET /tours` → 308 → `/tours/` → 301 → `/ekskursiya/` (final 200). Same pattern likely applies to other legacy English-slug entry points. Each extra hop adds latency and dilutes a small amount of link equity, and Googlebot budget. Fix: point `/tours` directly to `/ekskursiya/` (skip the intermediate trailing-slash hop) via a single rewrite rule in Vercel routing.
- 404 handling: unmapped paths first 308-redirect to the trailing-slash variant, *then* serve a real 404 (confirmed: `https://sakhva-travel.com/this-does-not-exist-xyz/` → HTTP 404, custom branded page, `<meta name="robots" content="noindex,follow">`, 3.5KB). Correct behavior, just adds one avoidable redirect hop for non-existent URLs — low priority (crawlers handle it fine, only cost is a wasted request).

## 5. Mobile — PASS (100/100)
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` present on all checked pages (home, /en/, /ge/, /blog/, /about/, /pogoda/).
- Static HTML/CSS, no viewport-breaking fixed-width containers observed in sampled pages.
No findings (full Lighthouse/touch-target audit out of scope for curl-based check).

## 6. Core Web Vitals (source-inspection only) — PASS (90/100)
- Static pre-rendered HTML (`is_spa=false`), Vercel CDN with `s-maxage=86400, stale-while-revalidate=604800` — favorable for LCP (no client-side render blocking).
- `x-vercel-cache: MISS` on 329/500 sampled pages — **Medium**: ~66% cache-miss rate on a supposedly static site means Vercel's edge cache is being evicted/not warmed for the long tail (mostly blog/tour pages beyond the top-trafficked set), so a meaningful share of first-time visitors per region hit origin compute instead of edge cache, adding TTFB/LCP latency. Cross-check against Cloudflare (`cf-cache-status: DYNAMIC` seen on all sampled headers, meaning Cloudflare itself is not caching HTML at all and passing straight to Vercel). Fix: add a Cloudflare Cache Rule to cache static HTML at the edge (respecting existing `cache-control` headers), and/or verify Vercel's ISR/ SSG output isn't being invalidated on each deploy for low-traffic paths.
- `<link rel="preload" as="image" fetchpriority="high">` used for hero images on at least one sampled page (`/blog/metro-tbilisi/`) — good LCP practice, confirms the team is already preloading LCP candidates.
- CLS: no explicit width/height audit performed (would need rendered layout, out of scope for curl-only check) — recommend a follow-up Lighthouse/PSI pass per template (home, tour, blog, country) to get real LCP/INP/CLS field or lab data; this audit only inspected source, not paint timing.

## 7. Structured Data — PASS (100/100)
- Schema present on 100% of 500 sampled pages (0 pages with `no_schema`). Example (`/blog/`): `Blog`, `ItemList`, `BreadcrumbList`, `WebPage`.
No findings from source inspection; recommend running these through Google's Rich Results Test periodically (not done here, no API/JS available).

## 8. JavaScript Rendering — PASS (100/100)
- Confirmed static HTML (`is_spa=false`); no JS-rendering dependency for content, titles, meta, or links. Fully crawlable by any bot including limited-JS crawlers (Yandex, Bing).

## 9. Hreflang (per seo-hreflang scope note — flagged here since caught in this audit)
- **High — 2 known gaps** per coordinator's full crawl: homepage (ru root `/` and `/en/`) lacks a `hreflang="ka"` return tag to `/ge/`, and `/en/ekskursiya/kazbegi-transfer-from-tbilisi/` has no hreflang block at all. Sampled pages beyond the homepage (blog, about, pogoda, contacts) all correctly include ru/en/ka/x-default — this looks like an isolated homepage-template + one orphan-page gap, not a systemic issue.
- Fix: add `<link rel="alternate" hreflang="ka" href="https://sakhva-travel.com/ge/">` to the ru and en homepage templates, and add the full hreflang block to the Kazbegi-transfer EN tour page (check for other orphan pages missing hreflang in the same tour sub-template).
- Full hreflang audit (bidirectional/return-tag validation across all locale pairs) belongs to `seo-hreflang` sub-skill — this is a scoped flag, not exhaustive.

## 9. IndexNow Protocol
- Not tested (no API access from curl-only environment to confirm submission history). CSP `connect-src` allow-lists `https://api.indexnow.org`, indicating the site already calls IndexNow client- or server-side — infra is in place. No further action identified without endpoint/key access.

---

## Priority Fix List

| # | Severity | Issue | Fix | Effort |
|---|----------|-------|-----|--------|
| 1 | High | Homepage + 1 tour page missing `hreflang="ka"` | Add ka alternate tag to ru/en homepage template + fix orphan tour page | 15 min |
| 2 | High | Duplicate `<title>` tag (HTML `<title>` + SVG `<title>`) on 3 metro-guide pages (ru/en/ge) | Rename SVG's internal `<title>` to `<desc>`/`aria-label` | 15 min |
| 3 | Medium | 2-hop redirect chain `/tours` → `/tours/` → `/ekskursiya/` | Point `/tours` directly to `/ekskursiya/` in Vercel rewrites | 10 min |
| 4 | Medium | Vercel edge cache MISS on 66% of sampled pages; Cloudflare `cf-cache-status: DYNAMIC` everywhere (no CDN-level HTML caching) | Add Cloudflare Cache Rule for static HTML respecting `cache-control` | 30 min |
| 5 | Low | 4 meta descriptions 161–165 chars | Trim to ≤155 chars | 10 min |
| 6 | Low | 3 titles >60 chars (metro-guide trio, resolves with fix #2) | Verify after fix #2 | 5 min |
| 7 | Low | 12 titles <30 chars | Review templates, expand where natural | later |
