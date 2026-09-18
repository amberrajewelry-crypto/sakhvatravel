# Technical SEO Audit — sakhva-travel.com — 2026-09-18

**Score: 78/100**

## Findings by severity

### Critical (1)
1. **Corrupted viewport meta on 103/120 Georgian blog pages + 1 ge/ekskursiya page.** Machine-translation script mangled the word "init" inside `initial-scale`. Evidence: `https://sakhva-travel.com/ge/blog/tbilisoba/` → `<meta content="width=device-width, ინიtial-scale=1.0, viewport-fit=cover" name="viewport"/>`. Confirmed via local source: `grep -rL "initial-scale=1.0" ge/blog/*/index.html | wc -l` = 103 (of 120 total). Breaks mobile scale control on those pages (Mobile category fail).

### High (2)
2. **English redirect targets drop the `/en/` locale, landing on Russian-language pages** (locale mismatch, not a 404 but poor UX/relevance signal). Evidence from `vercel.json` redirects: `/en/tury-v-gruziyu-iz-minska/` → `/tury-v-gruziyu-iz-minska/` (301, confirmed live), `/en/tury-v-gruziyu-iz-pyatigorska/` → `/tury-v-gruziyu-iz-pyatigorska/` (301, confirmed live). Both destinations are Russian pages with no English equivalent redirect target.
3. **Machine-translation corruption also hits non-technical strings on ge/ pages**, indicating the translation pass runs over raw HTML/attributes rather than content nodes only — same root cause as #1. Evidence: `<link rel="alternate" type="text/plain" href="/en/llms.txt" title="LLM-წაკითხვადი საიტის ინფო">` on `/ge/` (title attribute value machine-translated, breaking the intended English label).

### Medium (2)
4. **Extensionless 404 paths return an interim 308 before the real 404**, adding a redirect hop that Googlebot must follow to discover the true non-existent status. Evidence: `curl -sI https://sakhva-travel.com/this-page-does-not-exist-xyz` → `HTTP/2 308` `location: /this-page-does-not-exist-xyz/`, then `https://sakhva-travel.com/this-page-does-not-exist-xyz/` → `HTTP/2 404`. Trailing-slash normalization is otherwise consistent (all 10 sampled canonical pages use trailing slash), so this is a minor waste, not a broken policy.
5. **Sitemap-images.xml (769 URLs) has no equivalent 1:1 check performed against `<image:loc>` liveness** — flagged as unverified, see coverage table (not a confirmed defect, listed as a gap).

### Low (1)
6. Home/`/en/`/`/ge/` pages hreflang sets omit `ka`→`ka` reciprocal link on the `/tury-v-gruziyu/` cluster pattern is fine, but earlier automated extraction on minified HTML (attribute order `href` before `hreflang`) initially mis-flagged hreflang as absent on `/ekskursiya/*` and `/blog/*` detail pages; **re-verified against local source: all 117 ru blog pages and all 80 ru ekskursiya pages carry hreflang tags** (`grep -rl hreflang blog/*/index.html | wc -l` = 117 of 117; `ekskursiya/*/index.html` = 80 of 80). No real defect — logged so the false-positive isn't re-raised.

## Verified passes (no issue found)
- `robots.txt`: no blanket Disallow, correct crawler-specific rules (Googlebot/Bingbot/YandexBot open; CCBot/anthropic-ai/cohere-ai/MJ12bot/DotBot/BLEXBot/PetalBot/Bytespider/serpstatbot blocked), `Sitemap:` directive present and correct.
- `sitemap-index.xml`: 6 child sitemaps, all 200, counts — blog 358, tours 245, landing 68, pages 83, pogoda 66, images 769.
- Canonical self-reference correct on all 10 sampled pages (exact match to requested URL, own-page, absolute HTTPS).
- `meta robots` = `index,follow,max-image-preview:large,max-snippet:-1` on all 10 sampled pages — no accidental noindex found.
- Security headers on `/`: `strict-transport-security: max-age=31536000; includeSubDomains; preload`, `x-frame-options: DENY`, `x-content-type-options: nosniff`, `referrer-policy: strict-origin-when-cross-origin`, `permissions-policy: camera=(), microphone=(), geolocation=()`, CSP present (broad but no `unsafe-eval`, blocks inline in most directives except `unsafe-inline` for script/style). HSTS also confirmed present on `/en/`.
- Viewport meta correct (`width=device-width, initial-scale=1.0, viewport-fit=cover`) on all non-`ge/` sampled pages and on the majority (17/120) of ge/blog pages not hit by the corruption bug.
- Redirects: 20-source random sample from `vercel.json` (493 total rules) — all single-hop 301, zero chains, zero loops.
- 404 handling: genuine non-existent trailing-slash URL returns real `404` (not a soft-404 with 200).

## Not checked / gaps (explicitly out of scope given no-new-crawl instruction)
- JS-rendered vs raw text diff (home/tour/blog) — not run this pass.
- Image alt coverage on 5 pages — not run this pass.
- Page weight / Core Web Vitals proxies (render-blocking, preloads) — not run this pass.
- Mixed content scan — not run this pass.
- Structured data validation — not run this pass.
- IndexNow protocol check — not run this pass.
- Full hreflang reciprocity matrix beyond the 3 homepages + tury-v-gruziyu cluster — not run this pass.
- Sitemap-images.xml URL liveness sampling — not run this pass.

## Coverage table

| # | Category | Checked | Result |
|---|----------|---------|--------|
| 1 | Crawlability (robots.txt, sitemaps, noindex) | Yes | Pass |
| 2 | Indexability (canonicals, duplicates, thin content) | Partial (canonicals only) | Pass on sample |
| 3 | Security (HTTPS, headers) | Yes | Pass |
| 4 | URL structure / redirects | Yes (20-sample) | Pass, 1 medium (308+404 double hop) |
| 5 | Mobile (viewport) | Yes | Critical fail (ge/ corruption) |
| 6 | Core Web Vitals (source-level) | No | Not run |
| 7 | Structured data | No | Not run |
| 8 | JS rendering (CSR vs SSR) | No | Not run |
| 9 | IndexNow | No | Not run |

## Summary
Static-HTML Vercel site with solid crawl/security/redirect fundamentals: clean robots.txt, correct sitemap index (1,589 URLs across 6 files), consistent canonicals, full security header set including HSTS+CSP, and zero broken redirect chains in a 20-rule sample. The one critical defect is a machine-translation bug corrupting `initial-scale` inside the viewport meta tag on 103 of 120 Georgian blog pages (root cause: translation pass touching raw HTML/attribute strings, not content nodes — same bug also mangles an English title attribute). English-locale redirects for two `iz-minska`/`iz-pyatigorska` tour variants incorrectly resolve to Russian pages, a locale-relevance gap. CWV, structured data, JS-rendering, image-alt, IndexNow and image-sitemap-liveness checks were not run this pass and remain open gaps.
