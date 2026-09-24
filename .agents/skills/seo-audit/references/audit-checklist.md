# SEO Audit Checklist (80+ Points)

Comprehensive pass/fail checklist organized by category. Use with the `seo-audit` skill.

## Crawlability & Indexation (15 checks)

- [ ] robots.txt exists and returns 200
- [ ] robots.txt has valid syntax (no malformed directives)
- [ ] robots.txt does not block critical resources (CSS, JS, images)
- [ ] robots.txt references XML sitemap
- [ ] XML sitemap exists and returns 200
- [ ] XML sitemap contains only 200-status URLs
- [ ] XML sitemap includes `<lastmod>` dates
- [ ] Sitemap has fewer than 50,000 URLs per file (spec limit)
- [ ] Sitemap index used if multiple sitemaps needed
- [ ] No redirect chains (3+ hops between any two URLs)
- [ ] No redirect loops
- [ ] Canonical tags present on all indexable pages
- [ ] Canonical tags are self-referencing (not pointing elsewhere unless intentional)
- [ ] No conflicting signals (canonical says X, robots says noindex)
- [ ] No accidental noindex on important pages

## HTTPS & Security (8 checks)

- [ ] Site loads over HTTPS
- [ ] HTTP requests 301 redirect to HTTPS (single hop)
- [ ] No mixed content (HTTP resources on HTTPS pages)
- [ ] SSL certificate is valid and not expiring within 30 days
- [ ] HSTS header present with max-age >= 31536000
- [ ] X-Content-Type-Options: nosniff header present
- [ ] X-Frame-Options or CSP frame-ancestors header present
- [ ] Referrer-Policy header set

## Core Web Vitals & Performance (12 checks)

- [ ] LCP < 2.5 seconds (field data)
- [ ] INP < 200 milliseconds (field data)
- [ ] CLS < 0.1 (field data)
- [ ] TTFB < 800 milliseconds
- [ ] No render-blocking CSS in `<head>` above the fold
- [ ] No render-blocking JS without async/defer
- [ ] Images use modern formats (WebP or AVIF)
- [ ] Images have explicit width and height attributes
- [ ] Below-fold images use loading="lazy"
- [ ] Fonts use font-display: swap or optional
- [ ] Total page weight < 3MB (target < 1.5MB)
- [ ] JavaScript bundle < 300KB compressed

## Mobile Usability (8 checks)

- [ ] Viewport meta tag present: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] No horizontal scrollbar on mobile (320px-428px widths)
- [ ] Tap targets >= 48x48px
- [ ] Minimum 8px spacing between tap targets
- [ ] Base font size >= 16px
- [ ] No content hidden on mobile that exists on desktop
- [ ] No intrusive interstitials or popups on mobile
- [ ] Touch-friendly navigation (hamburger menu or equivalent)

## URL Structure (7 checks)

- [ ] URLs are lowercase
- [ ] URLs use hyphens (not underscores or spaces)
- [ ] No session IDs or tracking parameters in indexed URLs
- [ ] URL length < 100 characters
- [ ] Consistent trailing slash handling (all with or all without)
- [ ] www/non-www canonicalized (one redirects to the other)
- [ ] URL hierarchy reflects site architecture

## On-Page SEO (14 checks)

- [ ] Every page has a unique `<title>` tag
- [ ] Title tags are 50-60 characters
- [ ] Title tags contain the primary keyword
- [ ] Every page has a unique meta description
- [ ] Meta descriptions are 150-160 characters
- [ ] Meta descriptions contain the primary keyword
- [ ] Single H1 per page
- [ ] H1 contains primary keyword
- [ ] Heading hierarchy follows H1 > H2 > H3 (no skipped levels)
- [ ] Images have descriptive alt text
- [ ] No duplicate alt text across images on the same page
- [ ] Internal links use descriptive anchor text (not "click here" or "read more")
- [ ] At least 3 internal links per content page
- [ ] Open Graph and Twitter Card meta tags present

## Structured Data (8 checks)

- [ ] JSON-LD format used (not Microdata or RDFa)
- [ ] Homepage has Organization or WebSite schema
- [ ] Blog posts have Article schema
- [ ] BreadcrumbList schema on all pages with breadcrumbs
- [ ] FAQ sections have FAQPage schema
- [ ] No validation errors in Google Rich Results Test
- [ ] All required properties present for each schema type
- [ ] Schema matches visible page content (no hidden/misleading data)

## Internal Linking (7 checks)

- [ ] No orphan pages (every page linked from at least one other page)
- [ ] Key pages reachable within 3 clicks from homepage
- [ ] No broken internal links (404s)
- [ ] Anchor text varies for the same target URL
- [ ] No pages with excessive internal links (> 100 unique)
- [ ] Navigation links are crawlable HTML (not JS-only)
- [ ] Pagination uses rel="next"/rel="prev" or load-more with crawlable links

## E-E-A-T Signals (7 checks)

- [ ] About page exists with Organization/company information
- [ ] Contact page or contact information accessible
- [ ] Privacy policy page exists and is linked from footer
- [ ] Terms of service page exists
- [ ] Author bylines on content pages
- [ ] Author pages exist with bio, credentials, and Person schema
- [ ] External citations/references in content with working links

## AI Search Readiness (9 checks)

- [ ] GPTBot not blocked in robots.txt (unless intentional)
- [ ] PerplexityBot not blocked in robots.txt
- [ ] ClaudeBot / Claude-Web not blocked in robots.txt
- [ ] GoogleOther / Google-Extended not blocked in robots.txt
- [ ] Content renders without JavaScript (SSR or SSG)
- [ ] Direct-answer paragraphs (50-70 words) under each H2
- [ ] Definition patterns present ("X is..." format)
- [ ] FAQ sections with clear question-answer structure
- [ ] Publication dates and author attribution visible in HTML

## Internationalization (bonus, if applicable) (6 checks)

- [ ] hreflang tags present on all localized pages
- [ ] hreflang includes x-default
- [ ] hreflang tags are reciprocal (page A points to B, B points to A)
- [ ] Each locale has a unique canonical URL
- [ ] Language-specific XML sitemaps or sitemap index
- [ ] Content is natively written (not machine-translated without review)

---

**Total: 101 checks**

Scoring:
- Count passing checks per category
- Calculate percentage per category
- Apply grade: A (90-100%), B (75-89%), C (60-74%), D (40-59%), F (<40%)
- Calculate weighted overall score using weights from SKILL.md
