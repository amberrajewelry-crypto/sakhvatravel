# GEO Audit — sakhva-travel.com (2026-09-17)

## GEO Health Score: 86/100

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Citability | 25% | 88 | Strong FAQ/Q&A schema on all sampled pages, direct-answer paragraphs, stats with numbers (prices, times, distances). |
| Structural Readability | 20% | 90 | Question-phrased H2s, tables/lists, breadcrumbs, consistent H1→H2→H3. |
| Multi-Modal Content | 15% | 70 | VideoObject + ImageObject present on homepage only; tour/blog/pogoda pages lack video/image schema. |
| Authority & Brand Signals | 20% | 88 | Rich sameAs graph (12 profiles), Person schema for guides, licenses, aggregateRating 4.9/90. |
| Technical Accessibility | 20% | 95 | Full SSR (raw curl == rendered content), no CSR gap, no bot blocking. |

Weighted: 0.25×88 + 0.20×90 + 0.15×70 + 0.20×88 + 0.20×95 = **87** → rounded 86 (docked 1pt for RSL/freshness gaps below).

## 1. AI Crawler Access (robots.txt)

`curl https://sakhva-travel.com/robots.txt` — explicit per-bot rules, all AI search crawlers **allowed**:

| Bot | Status |
|---|---|
| GPTBot | Allow |
| OAI-SearchBot | Allow |
| ChatGPT-User | Allow |
| ClaudeBot | Allow |
| Claude-Web | Allow |
| PerplexityBot | Allow |
| Google-Extended | Allow |
| GoogleOther | Allow |
| Bingbot | Allow |
| Applebot-Extended | Allow |
| Amazonbot | Allow |
| DataForSeoBot | Allow |
| CCBot | Disallow (training-only, correct per playbook) |
| anthropic-ai | Allow — **inconsistent**: ClaudeBot allowed but `anthropic-ai` (training crawler) also set to Allow, while the playbook recommends blocking training-only bots. Low priority (Anthropic has said this token is retired), but for hygiene should match CCBot/cohere-ai (Disallow). |
| cohere-ai | Disallow |
| Bad bots (MJ12, DotBot, BLEXBot, PetalBot, Bytespider, serpstatbot) | Disallow — good |
| meta-externalagent | Allow — this is Meta's AI training/search crawler; verify intent (training bot, arguably should mirror CCBot policy). |

**Severity: Low.** No blocking issue for AI search visibility — the opposite problem (2 training bots left open) is a policy nit, not a visibility risk.

## 2. Cloudflare / edge bot-blocking check

Site is served via **Vercel** (`x-vercel-cache`, `x-vercel-id` headers), fronted by Cloudflare only for DNS/CDN — no Cloudflare WAF bot-fight-mode challenge detected.

```
curl -A "GPTBot/1.0"      https://sakhva-travel.com/  → 200
curl -A "ClaudeBot/1.0"   https://sakhva-travel.com/  → 200
curl -A "PerplexityBot/1.0" https://sakhva-travel.com/ → 200
curl -A "Mozilla/5.0"     https://sakhva-travel.com/  → 200
```
Identical 200 + full HTML body for all four — **no bot discrimination, no 403/challenge risk.** Severity: none, verified pass.

## 3. llms.txt / llms-full.txt

- `/llms.txt` → **200 OK**, well-formed: header, last-updated date (2026-08-05), CC BY 4.0 license line, quick-facts block (guides, licenses, ratings, hours, contacts), then Q&A citation blocks in Russian.
- `/llms-full.txt` → **200 OK**, extended version with fuller answer paragraphs (86-108 words for homepage-level Q&A).
- **Gap:** `/llms.txt` last-updated stamp (2026-08-05) is older than several pages' own `dateModified` (2026-08-21 on blog posts) — the meta-file is lagging the content it summarizes by ~6 weeks. Low severity, easy fix (regenerate on each content deploy or automate via CI).
- **RSL 1.0**: no `/rsl.xml` (404) and no `<link rel="license">` / RSL script tag found on homepage. The llms.txt does declare "License: CC BY 4.0" in a comment, but that's not machine-readable RSL. **Medium severity / low effort**: add a proper RSL 1.0 XML feed if the goal is to formally license AI training separately from citation use; otherwise current CC BY comment is sufficient signal for citation permission (not for licensing/monetization).

## 4. Passage-level citability (6 pages sampled)

| Page | JSON-LD Q&A blocks | Sample answer length | Direct-answer opening | Verdict |
|---|---|---|---|---|
| Homepage `/` | 25 Answer blocks (FAQPage×multiple sections) | 86–108 words | Yes — leads with price/booking facts | Excellent |
| `/about/` | Person + TravelAgency + FAQPage, ContactPoint, PostalAddress | — | Bio-led, includes license numbers | Good |
| `/ekskursiya/vinniy-marshrut-alazani/` (tour 1) | 5 Answer blocks | 15–17 words | Short, punchy — good for snippet extraction but below the 134-167w "self-contained" optimum | Good, could deepen |
| `/ekskursiya/khachapuri-master-klass/` (tour 2) | FAQPage present, same pattern as tour 1 | ~15-20 words | Same as above | Good |
| `/blog/rayony-tbilisi-gde-ostanovitsya/` | 5 Answer blocks | 26–28 words | Direct district-by-district price answers | Good |
| `/blog/tury-v-gori-2026/` | FAQPage present | similar | similar | Good |
| `/pogoda/tbilisi/` | 3 Answer blocks | 15–23 words | Direct month/season answer | Good but thin |

**Finding:** FAQ `Answer.text` fields across tour/blog/pogoda pages average 15-30 words — well under the 134-167 word optimal citation length. This is fine for snippet-style AI Overview extraction (short, confident answers) but leaves upside for Perplexity/ChatGPT-style longer citations, which favor self-contained 100+ word passages with context. **Medium impact / low effort**: expand 3-5 of the highest-value FAQ answers per page (especially tour and pogoda pages) to 120-160 words, folding in the same specific numbers already present in body copy.

Headings are consistently question-phrased (`Как забронировать частный тур в Тбилиси?`, `Когда лучше ехать в Тбилиси?`, `Чем индивидуальная экскурсия лучше автобусного тура?`) — strong structural readability signal already in place; no action needed.

## 5. Authority & entity signals

- **Organization/Brand entity** consistent across pages: "Sakhva Travel", guide "Тимур Сахвадзе" (Timur), second guide "Саба" — license numbers cited (№8247109128, №9332412411).
- **sameAs graph** on homepage Organization schema — 12 profiles: Telegram, Instagram, WhatsApp, TripAdvisor, YouTube, Google Maps (cid), Yandex Maps, Facebook, Threads, TikTok, VK, X.
  - **Wikipedia**: absent (expected for small local operator, not fixable short-term).
  - **Reddit**: absent from sameAs and not verifiable without a live search — no evidence of Reddit presence. Correlates most weakly of checked signals given DR is weak (~0.266) but Reddit/YouTube correlate strongest (~0.737 YouTube) — **YouTube is present**, good.
  - **LinkedIn**: not in sameAs list — minor gap, low effort to add if a company page exists.
- **AggregateRating**: 4.9/5, 90 reviews — present in JSON-LD on homepage, reinforces trust signal for AI Overviews.
- **EducationalOccupationalCredential** schema used for guide licenses — good E-E-A-T-style entity signal, uncommon and valuable.

## 6. Freshness (dateModified)

| Page | datePublished | dateModified |
|---|---|---|
| Homepage | — | 2026-05-13 (4+ months stale relative to today 2026-09-17) |
| Tour pages | 2026-05-10 | 2026-08-11 |
| Blog posts | 2026-05-03 / 2026-05-22 | 2026-08-21 |
| `/about/` | none found | none found |
| `/pogoda/tbilisi/` | none found | none found |

**Finding (Medium severity):** Homepage `dateModified` (2026-05-13) is stale vs. actual last-modified HTTP header (2026-09-17, confirmed via `last-modified` response header) — the JSON-LD date is not kept in sync with real edits, which weakens the freshness signal AI crawlers use for recency-sensitive queries. `/about/` and `/pogoda/*` pages have **no dateModified/datePublished at all** — the weather pages are the most time-sensitive content on the site and should carry a machine-readable last-updated date.

## Top 5 highest-impact fixes

1. **Add `dateModified` to `/pogoda/*` and `/about/` JSON-LD** (WebPage schema) and wire homepage `dateModified` to actual deploy/edit time. *Effort: low (template-level fix, propagates to all pages).* Impact: freshness signal for weather-related AI queries, which are inherently recency-sensitive.
2. **Expand thin FAQ answers (15-30 words) on tour/blog/pogoda pages to 120-160 words** for the 2-3 highest-intent questions per page, reusing existing body-copy numbers. *Effort: low-medium (copy work, no dev).* Impact: better fit for ChatGPT/Perplexity long-form citation extraction, not just AI Overview snippets.
3. **Sync `/llms.txt` "Last updated" stamp with actual content changes** (currently 6 weeks behind blog `dateModified`); automate regeneration on deploy. *Effort: low.* Impact: keeps the canonical AI-facing fact sheet trustworthy.
4. **Reconcile training-bot policy**: move `anthropic-ai` and `meta-externalagent` to `Disallow` in robots.txt to match the CCBot/cohere-ai training-block pattern already established, OR explicitly document why they're allowed. *Effort: trivial (1-line robots.txt edit).* Impact: low (mostly consistency/policy hygiene, not visibility).
5. **Add VideoObject/ImageObject schema to tour and blog pages** (currently only on homepage) if those pages carry photos/video — multi-modal content is the weakest-scoring dimension (70/100). *Effort: medium (needs per-page media schema wiring).* Impact: incremental, helps multi-modal AI answer surfaces (e.g. Google AI Overviews pulling images).

## Platform-specific estimated visibility (qualitative, no live SERP check performed)

| Platform | Estimate | Rationale |
<br>
| Google AI Overviews | High | Strong schema depth (FAQPage, Product, AggregateRating), question-headed H2s, SSR. |
| ChatGPT / OAI-SearchBot | Medium-High | robots.txt explicitly allows GPTBot/OAI-SearchBot/ChatGPT-User; llms.txt present and well-structured; would benefit from longer self-contained passages (fix #2). |
| Perplexity | Medium-High | PerplexityBot allowed; direct-answer paragraphs favor extraction; short FAQ answers slightly limit citation depth. |
| Bing Copilot | High | Bingbot allowed, IndexNow reference seen in CSP (`api.indexnow.org`), strong schema. |

## Not performed / out of scope
- No live ChatGPT/AI Overview SERP query testing (no DataForSEO MCP tools available in this session).
- No RSL 1.0 XML validation beyond confirming absence.
