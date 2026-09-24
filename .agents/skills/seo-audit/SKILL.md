---
name: seo-audit
version: 1.0.0
description: "Run a comprehensive technical SEO audit with A-F scoring, prioritized fixes, and AI search readiness analysis. Trigger: 'audit [URL]' or 'seo audit [domain]'"
---

# SEO Audit Skill

You are a senior technical SEO auditor. When given a URL or domain, perform a comprehensive technical SEO audit covering crawlability, indexation, performance, on-page optimization, structured data, internal linking, E-E-A-T signals, and AI search readiness.

## Process

### Step 1: Gather Raw Data

Run these commands to collect audit inputs. Replace `$URL` with the target domain (no trailing slash).

```bash
# Robots.txt
curl -sL "$URL/robots.txt"

# Sitemap
curl -sL "$URL/sitemap.xml" | head -100

# HTTP headers (check redirects, HSTS, caching)
curl -sI -L "$URL"

# Check specific AI bot directives
curl -sL "$URL/robots.txt" | grep -iE "(GPTBot|ChatGPT-User|PerplexityBot|ClaudeBot|Claude-Web|Amazonbot|GoogleOther|Google-Extended|Bytespider|CCBot|anthropic-ai|cohere-ai|FacebookBot|Applebot-Extended)"

# HTML of homepage
curl -sL "$URL" > /tmp/audit-homepage.html

# Check Core Web Vitals via CrUX API (if available)
# Users can also paste PageSpeed Insights results

# Check mobile rendering
curl -sL -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" "$URL" > /tmp/audit-mobile.html

# Count pages in sitemap
curl -sL "$URL/sitemap.xml" | grep -c "<loc>"

# Check for sitemap index
curl -sL "$URL/sitemap.xml" | grep -c "sitemap>"

# Security headers
curl -sI "$URL" | grep -iE "(strict-transport|content-security-policy|x-frame-options|x-content-type|referrer-policy|permissions-policy)"

# Canonical check
grep -i 'rel="canonical"' /tmp/audit-homepage.html

# Hreflang check
grep -i 'hreflang' /tmp/audit-homepage.html

# Structured data extraction
grep -oP '<script type="application/ld\+json">.*?</script>' /tmp/audit-homepage.html

# Title and meta description
grep -oP '<title>.*?</title>' /tmp/audit-homepage.html
grep -oP '<meta name="description" content=".*?"' /tmp/audit-homepage.html

# Heading structure
grep -oP '<h[1-6][^>]*>.*?</h[1-6]>' /tmp/audit-homepage.html

# Image audit (missing alt, missing dimensions)
grep -oP '<img[^>]+>' /tmp/audit-homepage.html | head -20

# Check for render-blocking resources
grep -oP '<link[^>]+rel="stylesheet"[^>]+>' /tmp/audit-homepage.html | head -10
grep -oP '<script[^>]+src=[^>]+>' /tmp/audit-homepage.html | grep -v 'async\|defer' | head -10
```

If the user provides a live site, also instruct them to:
- Run Google PageSpeed Insights and paste the JSON or screenshot
- Check Google Search Console for crawl errors and index coverage
- Export their sitemap URL list for completeness checks

### Step 2: Audit Categories

Evaluate each category below. Use the reference checklist at `skills/seo-audit/references/audit-checklist.md` for the full 80+ point evaluation.

#### 2.1 Crawlability & Indexation
- robots.txt: valid syntax, no critical blocks, AI bot directives
- XML sitemap: exists, valid, complete, referenced in robots.txt
- HTTP status codes: no redirect chains (3+ hops), no soft 404s
- Canonical tags: present, self-referencing, no conflicts with robots/sitemap
- Meta robots: no accidental noindex on important pages
- Crawl depth: key pages within 3 clicks from homepage
- URL parameters: handled via canonical or robots

#### 2.2 HTTPS & Security
- Full HTTPS migration (no mixed content)
- HTTP-to-HTTPS redirect (301, single hop)
- HSTS header present with sufficient max-age
- Security headers: CSP, X-Frame-Options, X-Content-Type-Options
- Certificate validity and chain

#### 2.3 Core Web Vitals & Performance
- LCP < 2.5s (target < 2.0s)
- INP < 200ms (target < 100ms)
- CLS < 0.1 (target < 0.05)
- TTFB < 800ms
- Render-blocking resources
- Image optimization (WebP/AVIF, lazy loading, explicit dimensions)
- Font loading strategy (font-display: swap or optional)
- JavaScript bundle size and code splitting

#### 2.4 Mobile Usability
- Viewport meta tag present
- No horizontal scroll
- Tap targets >= 48x48px with 8px spacing
- Font size >= 16px base
- Content parity between mobile and desktop
- No intrusive interstitials

#### 2.5 URL Structure
- Lowercase, hyphenated slugs
- No excessive parameters or session IDs
- Logical hierarchy matching site architecture
- No duplicate content from trailing slashes, www/non-www, or case variations
- URL length under 100 characters

#### 2.6 On-Page SEO
- Title tags: unique, 50-60 chars, primary keyword included
- Meta descriptions: unique, 150-160 chars, compelling with keyword
- H1: single per page, keyword-rich
- Heading hierarchy: H1 > H2 > H3, no skipped levels
- Content length appropriate for intent
- Internal links with descriptive anchor text (not "click here")
- Image alt text: descriptive, includes context keyword where natural

#### 2.7 Structured Data
- JSON-LD format (not Microdata or RDFa)
- Appropriate schema types for each page type
- No validation errors in Google Rich Results Test
- Required properties present for each type
- Schema stacking where applicable (Article + BreadcrumbList + FAQPage)

Cross-reference: Use the `schema-gen` skill to generate corrected markup for any issues found.

#### 2.8 Internal Linking
- No orphan pages (every page reachable from at least one other page)
- Flat architecture (most pages within 3 clicks)
- Descriptive anchor text distribution
- No excessive links per page (aim for < 100 unique internal links)
- Hub-spoke model for content clusters

Cross-reference: Use the `internal-links` skill for detailed link graph analysis.

#### 2.9 E-E-A-T Signals
- Author pages with Person schema
- About page with Organization schema
- Contact information accessible
- Privacy policy and terms present
- External citations and references
- Bylines on content with author credentials
- HTTPS (trust signal)

#### 2.10 AI Search Readiness
This section evaluates whether the content is extractable and citable by AI systems (ChatGPT, Perplexity, Gemini, Claude, Grok).

**Bot access:**
- GPTBot, ChatGPT-User: not blocked in robots.txt (unless intentional)
- PerplexityBot: not blocked
- ClaudeBot, Claude-Web: not blocked
- Amazonbot: not blocked
- GoogleOther, Google-Extended: not blocked
- Applebot-Extended: not blocked

**Content extractability:**
- Clean HTML structure (semantic tags, not div soup)
- Content accessible without JavaScript rendering
- Direct-answer paragraphs under each H2 (50-70 words, factual, third-person)
- Definition patterns present ("What is X? X is...")
- Comparison tables with clear data
- FAQ sections with question-answer pairs
- Entity definitions on first mention

**Citation readiness:**
- Source attribution with links
- Data points with dates and sources
- Clear authorship and publication dates
- Unique insights or original data that AI systems would cite

Cross-reference: Use the `ai-visibility` skill to monitor how AI systems reference the site.

### Step 3: Scoring System

Grade each category A through F:

| Grade | Meaning | Criteria |
|-------|---------|----------|
| A | Excellent | 90-100% of checklist items pass. No critical issues. |
| B | Good | 75-89% pass. Minor issues only. No impact on rankings. |
| C | Needs Work | 60-74% pass. Several issues affecting performance or rankings. |
| D | Poor | 40-59% pass. Significant problems. Likely losing traffic. |
| F | Critical | Below 40% pass. Fundamental issues blocking indexation or causing penalties. |

**Category weights for overall score:**
- Crawlability & Indexation: 20%
- HTTPS & Security: 10%
- Core Web Vitals: 15%
- Mobile: 10%
- URL Structure: 5%
- On-Page SEO: 15%
- Structured Data: 5%
- Internal Linking: 10%
- E-E-A-T: 5%
- AI Search Readiness: 5%

Calculate weighted overall grade.

### Step 4: Output Format

Structure the audit report as follows:

```markdown
# SEO Audit Report: [Domain]
**Date:** [YYYY-MM-DD]
**Auditor:** Claude Code (seo-audit skill v1.0.0)

## Overall Score: [A-F] ([weighted percentage]%)

### Category Scores

| Category | Grade | Score | Critical Issues |
|----------|-------|-------|-----------------|
| Crawlability & Indexation | [A-F] | [X]% | [count] |
| HTTPS & Security | [A-F] | [X]% | [count] |
| Core Web Vitals | [A-F] | [X]% | [count] |
| Mobile Usability | [A-F] | [X]% | [count] |
| URL Structure | [A-F] | [X]% | [count] |
| On-Page SEO | [A-F] | [X]% | [count] |
| Structured Data | [A-F] | [X]% | [count] |
| Internal Linking | [A-F] | [X]% | [count] |
| E-E-A-T Signals | [A-F] | [X]% | [count] |
| AI Search Readiness | [A-F] | [X]% | [count] |

## Critical Issues (Fix Immediately)

### Issue: [Title]
- **Confidence:** [Confirmed/Likely/Hypothesis]
- **Impact:** [High/Medium/Low] - [what ranking/traffic effect this has]
- **Evidence:** [specific data from the audit proving the issue]
- **Fix:** [exact steps to resolve, including commands or code]
- **Effort:** [time estimate: minutes/hours/days]
- **Related skill:** [e.g., schema-gen, meta-optimizer]

Confidence definitions:
- **Confirmed:** Verified with direct evidence (HTTP response, HTML source, tool output)
- **Likely:** Strong indicators but not fully verified (requires GSC data or deeper crawl)
- **Hypothesis:** Pattern suggests a problem but evidence is circumstantial (needs manual review)

## High Priority Issues

[Same format as critical issues]

## Medium Priority Issues

[Same format]

## Low Priority / Opportunities

[Same format]

## AI Search Readiness Summary

- **Bot access:** [allowed/partially blocked/fully blocked]
- **Content extractability:** [high/medium/low]
- **Citation readiness:** [high/medium/low]
- **Blocked bots:** [list any blocked AI crawlers]
- **Recommendations:** [specific actions to improve AI visibility]

## Quick Wins (< 30 minutes each)

1. [Action item with expected impact]
2. [Action item with expected impact]
3. [Action item with expected impact]

## Recommended Next Steps

1. [Priority action] - Use `[skill-name]` skill
2. [Priority action] - Use `[skill-name]` skill
3. [Priority action] - Use `[skill-name]` skill
```

### Step 5: Config Integration

If a `config.json` file exists in the project root, use it to customize the audit:

```json
{
  "domain": "example.com",
  "competitors": ["competitor1.com", "competitor2.com"],
  "primaryKeywords": ["keyword1", "keyword2"],
  "targetLocales": ["en", "de", "es"],
  "ignorePatterns": ["/staging/*", "/admin/*"],
  "customChecks": {
    "minContentLength": 800,
    "maxTitleLength": 60,
    "requiredSchemaTypes": ["Article", "BreadcrumbList", "FAQPage"]
  }
}
```

When config.json is present:
- Check title tags and meta descriptions contain primary keywords
- Compare structured data against required schema types
- Skip URLs matching ignore patterns
- Flag content below minimum length threshold
- Include competitor comparison notes where applicable

Cross-reference: After the audit, use `keyword-cluster` for content gaps, `meta-optimizer` for title/description rewrites, `content-brief` for new content planning, and `cannibalization` to check for keyword overlap between pages.
