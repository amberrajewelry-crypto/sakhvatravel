# Core Web Vitals & Performance Audit — sakhva-travel.com

**Date:** 2026-05-04
**Method:** Source analysis + TTFB measurement (PSI API quota exceeded)
**Tested pages:** 4

---

## 1. TTFB (Time to First Byte)

| Page | TTFB | HTML Size | Status |
|------|------|-----------|--------|
| `/` (homepage RU) | 118ms | 195 KB | GOOD |
| `/en/` (homepage EN) | 107ms | 120 KB | GOOD |
| `/tour/kazbegi/` | 108ms | 52 KB | GOOD |
| `/blog/kazbegi-iz-tbilisi-2026/` | 155ms | 60 KB | GOOD |

All pages have excellent TTFB (<200ms). Vercel edge CDN works well.

---

## 2. LCP (Largest Contentful Paint) — estimated risk

### Homepage (RU & EN)
- **LCP element:** Hero image (`hero-photo-mob-tall.webp` / `hero-photo-1200.webp`)
- **Mobile hero:** 17 KB (webp) — excellent
- **Desktop hero:** 97 KB (webp) — good
- **Preload:** YES, with `fetchpriority="high"` and `<link rel="preload">` — correct
- **Estimated LCP:** ~1.5-2.5s (GOOD)

### Tour page (`/tour/kazbegi/`)
- **LCP element:** Hero image (`kazbegi-tour.webp`)
- **Preload:** YES (`<link rel="preload" as="image" fetchpriority="high">`)
- **Estimated LCP:** ~1.5-2.5s (GOOD)

### Blog article
- **LCP element:** `.article-h1` text block (no hero image above fold)
- **Font dependency:** Lora (preloaded on homepage, but NOT preloaded on blog page)
- **Risk:** LCP depends on font load without preload = potential delay
- **Estimated LCP:** ~2.0-3.0s (NEEDS IMPROVEMENT on slow connections)

---

## 3. CLS (Cumulative Layout Shift) — estimated risk

| Page | Images w/o width | CLS Risk | Issues |
|------|------------------|----------|--------|
| Homepage RU | 1 (Yandex pixel) | LOW | Yandex pixel has `position:absolute` — no shift |
| Homepage EN | 0 | LOW | -- |
| Tour kazbegi | 0 | LOW | -- |
| Blog | 0 | LOW | -- |

**CLS is well-controlled.** All content images have explicit `width`/`height`. Fonts use `preload as="style"` pattern to minimize FOUT.

**One risk:** EN homepage gallery images (27 images) have NO `loading="lazy"` — they won't cause CLS but waste bandwidth.

---

## 4. INP (Interaction to Next Paint) — risk analysis

| Factor | Homepage | Tour | Blog |
|--------|----------|------|------|
| Script count | 21 | 12 | 9 |
| DOM elements | ~748 | ~400 est | ~350 est |
| Inline JS tasks | Video loader, consent, analytics | Consent, GA (deferred) | Consent, GA (sync) |
| Third-party scripts | Yandex Metrika, Clarity, Google Maps iframe | Clarity (deferred) | GTM (async) |
| Estimated INP | ~150-250ms | ~100-200ms | ~100-150ms |

**Homepage INP risk:** MEDIUM — 21 scripts + Yandex Metrika + Clarity + Google Maps iframe.
**Blog INP risk:** LOW.

---

## 5. Resource Analysis

### CSS Files

| File | Size | Strategy | Issue |
|------|------|----------|-------|
| `/fonts/all.css?v=1` | 28 KB | preload → stylesheet | DUPLICATED (loaded 2x on homepage) |
| `/css/deferred.css?v=48` | ? (gzip) | preload → stylesheet | DUPLICATED (loaded 2x on homepage) |
| `/css/seamless.css?v=52` | ? (gzip) | preload → stylesheet | DUPLICATED (loaded 2x on homepage) |
| `/fonts/raleway.css` | 6.5 KB | preload → stylesheet | DUPLICATED on tour pages (loaded 2x) |
| `/fonts/montserrat.css` | 328 B | preload → stylesheet | DUPLICATED on tour pages |
| `/fonts/lora.css` | 21 KB | preload → stylesheet | DUPLICATED on tour pages |

**CRITICAL: All CSS files are loaded TWICE on every page** — once via `<link rel="preload" as="style" onload="...">` and once via `<link rel="stylesheet">`. The noscript fallback duplicates work in the regular flow.

### JavaScript

| File | Size | Strategy |
|------|------|----------|
| `/js/ui-deferred.js?v=5` | 8.9 KB | `defer` — correct |
| Inline scripts (homepage) | ~5 KB | sync — video loader blocks |
| `/js/main.js?v=32` | 404 | FILE NOT FOUND |

**main.js returns 404.** If it's referenced anywhere, that's a wasted request.

### Fonts

| File | Size | Notes |
|------|------|-------|
| `lora-10.woff2` | 21 KB | Preloaded on homepage — good |
| `all.css` (font declarations) | 28 KB | Contains multiple font faces |

### Videos

| File | Size | Strategy |
|------|------|----------|
| `tours-bg-video.mp4` | **25.6 MB** | Lazy (interaction/idle) |
| `batumi-video.mp4` | **6.7 MB** | `data-src` lazy |
| `kutaisi-video.mp4` | **4.0 MB** | `data-src` lazy |
| `kakheti-video.mp4` | **1.6 MB** | `data-src` lazy |
| `kazbegi-hero-video.mp4` | 900 KB | `data-src` lazy |

**Hero video 25.6 MB is excessive.** Even though it loads lazily on desktop (idle callback / 3s timeout), it still downloads 25 MB. On mobile, it loads on touch/scroll.

### Images (Homepage)

| Image | Size | Format |
|-------|------|--------|
| `hero-photo-mob-tall.webp` | 17 KB | WebP |
| `hero-photo-1200.webp` | 97 KB | WebP |
| `timur.webp` | 98 KB | WebP |
| Gallery images | ~placeholder SVG (lazy) | WebP via data-src |

Images are well-optimized with WebP, lazy loading, and placeholder SVGs.

### Third-Party Scripts

| Script | Page | Impact |
|--------|------|--------|
| Yandex Metrika (109038950) | Homepage RU | ~50KB JS, tracking pixel |
| Microsoft Clarity (wga1e0fbep) | Homepage RU/EN | ~30KB JS |
| Google Maps iframe | Homepage RU | **HEAVY** — loads entire Maps SDK (~200KB+) |
| GTM/gtag | Blog | async — moderate impact |
| GTM/gtag | Tour | **Deferred on interaction** — best practice |
| Cloudflare email-decode | EN, Blog | Minimal |

---

## 6. Critical Issues (Priority Order)

### P0 — HIGH IMPACT

1. **Hero video 25.6 MB** — compress to <5 MB (target 1080p 15fps, CRF 32+)
   - Expected saving: ~20 MB per homepage visit on desktop
   - Use `poster` image only on mobile, don't load video at all

2. **CSS files loaded TWICE** — remove duplicate `<link rel="stylesheet">` tags, keep only the preload+onload pattern with noscript fallback
   - Homepage: 3 CSS files x2 = 6 HTTP requests instead of 3
   - Tour pages: 3 font CSS files x2 = 6 HTTP requests instead of 3

3. **Blog: font not preloaded** — add `<link rel="preload" href="/fonts/lora-10.woff2" as="font" type="font/woff2" crossorigin>` to blog pages
   - LCP on blog is text, which depends on font load
   - Expected improvement: ~200-400ms LCP

### P1 — MEDIUM IMPACT

4. **Google Maps iframe on homepage** — replace with static map image + click-to-load
   - Saves ~200-500 KB initial load, improves INP
   - Pattern: `<img>` → click → replace with `<iframe>`

5. **EN gallery: 27 images without `loading="lazy"`** — add `loading="lazy"` to all below-fold gallery images
   - Currently all 27 load eagerly = wasted bandwidth on mobile

6. **Blog: GTM loaded synchronously** — use interaction-deferred pattern (like tour page does)
   - Blog uses `<script async src="...gtag...">` in head
   - Tour page defers to user interaction — better approach

### P2 — LOW IMPACT

7. **Yandex Metrika pixel image** without `width`/`height` — already `position:absolute`, no CLS impact but should have dimensions for best practice

8. **`main.js?v=32` returns 404** — verify no page references it; remove if dead

9. **`timur.webp` at 98 KB** — compress further to ~30-40 KB (600x600 portrait doesn't need this much)

10. **Inline CSS on blog pages is 21 KB** — consider extracting to external cached file for repeat visitors

---

## 7. Summary by Page

| Page | LCP est | INP est | CLS est | Overall |
|------|---------|---------|---------|---------|
| Homepage RU | GOOD (~2s) | NEEDS IMP (~200-250ms) | GOOD (<0.05) | NEEDS IMPROVEMENT |
| Homepage EN | GOOD (~2s) | GOOD (~150ms) | GOOD (<0.05) | GOOD |
| Tour kazbegi | GOOD (~2s) | GOOD (~150ms) | GOOD (<0.05) | GOOD |
| Blog article | NEEDS IMP (~2.5-3s) | GOOD (~100ms) | GOOD (<0.05) | NEEDS IMPROVEMENT |

---

## 8. Quick Wins (do first)

1. Remove duplicate CSS `<link>` tags — 5 minutes, all pages
2. Add `loading="lazy"` to EN gallery images — 5 minutes
3. Preload Lora font on blog/tour pages — 5 minutes per template
4. Compress hero video to <5 MB — 15 minutes with ffmpeg
5. Defer Google Maps iframe to click-to-load — 30 minutes

**Expected result after fixes: all 4 pages pass Core Web Vitals "Good" threshold.**
