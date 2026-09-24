# GEO Audit — sakhva-travel.com — 2026-09-18

## Score: 79/100

## AI Crawler Access (robots.txt, live == local, verified)
- GPTBot: Allow — OAI-SearchBot: Allow — ClaudeBot: Allow — PerplexityBot: Allow — Google-Extended: Allow — Applebot/Applebot-Extended: Allow
- CCBot: Disallow — anthropic-ai: Disallow — cohere-ai: Disallow — Bytespider: Disallow
- Config matches recommended posture exactly (allow AI search crawlers, block training-only bots). No issue.

## llms.txt
- Present, live, valid, dated 2026-09-17, links to llms-full.txt (200), CC BY 4.0 license note. Good facts block (rating, guides, licenses, hours, contact).
- **Coverage gap (HIGH):** 80 unique internal links in llms.txt vs ~754 URLs across sitemap-blog(358)+tours(245)+pages(83)+landing(68). ~10.6% sitemap coverage. None of the 6 audited pages except one excursion appear in llms.txt/llms-full.txt: missing gruzinskie-frazy, chacha-gruzinskaya, metro-tbilisi, georgian-alphabet, transfer-tbilisi-batumi.
- Sampled links (about/saba, tury-v-batumi, vip-tur-v-gruziyu, ge/prices) all return 200 — no stale/broken links found in sample.

## Passage-level citability (6 pages, extracted from index.html)
| Page | First-100w direct answer | Q-style H2 | Tables/Lists | Numbers+units |
|---|---|---|---|---|
| blog/gruzinskie-frazy | **FAIL** — first `<p>` is nav widget "Тур по теме..." (18 words, no answer) | 0 | 6/2 | yes |
| blog/chacha-gruzinskaya | OK — 64w definitional answer | 0 | 2/5 | yes |
| blog/metro-tbilisi | **FAIL** — same nav-widget boilerplate as first paragraph | 0 | 2/9 | yes |
| en/blog/georgian-alphabet | OK — 89w direct answer | 0 | 2/5 | yes |
| ekskursiya/ekskursiya-kazbegi-iz-tbilisi | Weak — first block is price/CTA widget text, not prose answer | 1 | 0/1 | yes |
| ekskursiya/transfer-tbilisi-batumi | OK — 22w concise answer (315 km / 5h) | 0 | 0/2 | yes |
- Zero question-phrased H2/H3 on 5 of 6 pages — weak for AIO-style Q&A extraction despite llms.txt Q&A format existing site-wide.

## Entity consistency (6 pages)
- Phone: single form `+995511272623` everywhere — consistent.
- Brand: "Sakhva Travel"/"Sakhva"/"Сахва" all present, no divergent naming.
- Guide: "Тимур"/"Timur" consistent; Saba correctly absent (out of scope tours).
- No street address on any page (city-only "Тбилиси") — no LocalBusiness postal address signal in visible text.

## Brand/entity signals
- **Wikidata item confirmed LIVE**: Q140518485, label "Sakhva Travel", en description "private tour guide company in Tbilisi, Georgia" — matches docs/wikidata-entity.md plan, already created (doc was stale, said "to create").
- TripAdvisor ID (d15318013) referenced as notability claim per docs; not re-verified live in this pass.

## Severity buckets
- CRITICAL: 0
- HIGH: 1 — llms.txt sitemap coverage ~10.6%, 5/6 sampled target pages absent from llms.txt
- MEDIUM: 2 — 2/6 pages have boilerplate (not answer) as first paragraph (gruzinskie-frazy, metro-tbilisi); near-zero question-phrased H2s across sampled pages
- LOW: 1 — no visible postal address entity signal on sampled pages
- INFO: 1 — Wikidata item already live (docs outdated, said pending)
