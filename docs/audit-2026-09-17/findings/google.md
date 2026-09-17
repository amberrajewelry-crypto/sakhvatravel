# Google SEO Data — sakhva-travel.com

Property: `https://sakhva-travel.com/` (URL-prefix, GSC). Config file had wrong property (`sc-domain:sakhva-travel.com`, 403) — corrected to URL-prefix, which is what the service account (`sakhva-indexing@mercurial-shine-465511-h4.iam.gserviceaccount.com`) actually has `siteOwner` on.

Credential tier: 1 (service account only, no `GOOGLE_API_KEY`, no GA4 property configured).

## What succeeded / failed

| Check | Status |
|---|---|
| GSC queries (28d) | OK |
| GSC pages (28d/90d) | OK |
| GSC totals by date (28d/90d) | OK |
| GSC country/device (28d) | OK |
| GSC query×page striking-distance (28d) | OK |
| GSC queries (90d) | FAILED — script returned empty output (timed out/killed after ~6 min; GSC API paginates full query-dimension result set before truncating to `--limit`, which is slow for high-cardinality query sets) |
| GSC sitemaps | OK |
| URL Inspection (10 URLs) | NOT RUN — ran out of time budget in this session; not fabricated |
| PageSpeed Insights / CrUX / CrUX History | FAILED — no `GOOGLE_API_KEY` in `~/.config/claude-seo/google-api.json` or env |
| GA4 | SKIPPED — not configured (no `ga4_property_id`) |

## GSC totals (Google API, field data, sums from date-dimension query)

| Period | Clicks | Impressions | CTR | Avg. position |
|---|---|---|---|---|
| 28 days | 8,073 | 586,219 | 1.38% | 6.95 |
| 90 days | 16,324 | 1,302,860 | 1.25% | 7.23 |

Note: 2-3 day GSC data lag applies; date coverage returned 26 days (28d req.) / 88 days (90d req.).

## Top 25 queries (28 days, by clicks)

| Query | Clicks | Impr. | CTR% | Pos. |
|---|---|---|---|---|
| თბილისობა 2026 | 299 | 2322 | 12.88 | 1.9 |
| მარტვილის კანიონი ფასები 2026 | 149 | 898 | 16.59 | 2.8 |
| тбилисоба 2026 | 115 | 1257 | 9.15 | 2.5 |
| tbilisoba 2026 | 102 | 1027 | 9.93 | 2.7 |
| грузинский алфавит | 97 | 9117 | 1.06 | 4.8 |
| თბილისი ყაზბეგი | 53 | 123 | 43.09 | 1.7 |
| სადღეგრძელოები ქართულ სუფრაზე | 43 | 956 | 4.5 | 6.5 |
| тбилисоба 2026 когда | 34 | 281 | 12.1 | 2.5 |
| что привезти из грузии | 26 | 1041 | 2.5 | 8.6 |
| თბილისი ყაზბეგი მარშუტკა | 26 | 77 | 33.77 | 1.6 |
| tbilisoba | 24 | 468 | 5.13 | 6.4 |
| გოგირდის აბანოების ფასი | 23 | 191 | 12.04 | 6.1 |
| თბილისობა | 23 | 924 | 2.49 | 6.7 |
| ქართული სადღეგრძელოები | 23 | 377 | 6.1 | 4.7 |
| ტურები სვანეთში 2026 | 22 | 92 | 23.91 | 4.0 |
| თბილისი ყაზბეგი ტრანსპორტი | 21 | 52 | 40.38 | 1.3 |
| ლამაზი სადღეგრძელოები | 21 | 601 | 3.49 | 6.3 |
| грузинский алфавит на русском | 20 | 741 | 2.7 | 4.5 |
| თბილისობა 2026 თარიღი | 20 | 66 | 30.3 | 2.1 |
| georgia souvenirs | 19 | 182 | 10.44 | 3.9 |
| tbilisoba festival 2026 | 19 | 504 | 3.77 | 3.9 |
| what to buy in georgia | 18 | 92 | 19.57 | 2.0 |
| спасибо по грузински | 18 | 3965 | 0.45 | 9.3 |
| день города тбилиси 2026 | 15 | 73 | 20.55 | 2.7 |
| თბილისი ყაზბეგი მგზავრობა | 15 | 43 | 34.88 | 1.1 |

90-day top queries unavailable (script timed out — see above). Raw 28d query set has 14,269 rows total; full list is in `google-data.json`.

## Top 25 pages (28 days, by clicks)

| Page | Clicks | Impr. | CTR% | Pos. |
|---|---|---|---|---|
| /en/blog/what-to-buy-in-georgia/ | 503 | 7491 | 6.71 | 4.3 |
| /ge/blog/tbilisoba/ | 502 | 5524 | 9.09 | 3.3 |
| /ge/blog/georgian-toasts/ | 331 | 7034 | 4.71 | 6.4 |
| /blog/gruzinskie-frazy/ | 318 | 41477 | 0.77 | 7.8 |
| /ge/blog/transfer-tbilisi-to-kazbegi/ | 294 | 2479 | 11.86 | 4.1 |
| /blog/gruzinskiy-alfavit/ | 289 | 22962 | 1.26 | 5.3 |
| /blog/tbilisoba/ | 280 | 4429 | 6.32 | 4.1 |
| /ge/blog/martvili-canyon/ | 242 | 6505 | 3.72 | 6.6 |
| /en/blog/tbilisoba/ | 228 | 4972 | 4.59 | 4.6 |
| /en/blog/transfer-tbilisi-to-kazbegi/ | 162 | 8791 | 1.84 | 6.2 |
| /blog/gruzinskie-tosty/ | 152 | 3727 | 4.08 | 5.2 |
| /en/blog/georgia-in-september/ | 150 | 31978 | 0.47 | 5.8 |
| /blog/restorany-tbilisi/ | 115 | 4741 | 2.43 | 9.2 |
| /blog/chto-privezti-iz-gruzii/ | 103 | 4675 | 2.2 | 7.7 |
| /blog/karty-nalichnye-gruziya/ | 95 | 7346 | 1.29 | 6.4 |
| /blog/rouming-v-gruzii/ | 91 | 6825 | 1.33 | 6.0 |
| /ge/blog/what-to-see-in-tbilisi/ | 89 | 2128 | 4.18 | 6.1 |
| /blog/ureki-plyazh/ | 86 | 5219 | 1.65 | 6.4 |
| /en/blog/tbilisi-cable-car/ | 84 | 11182 | 0.75 | 6.6 |
| /en/blog/kazbegi-in-winter/ | 83 | 3514 | 2.36 | 4.8 |
| /ge/blog/sulfur-baths-tbilisi/ | 80 | 1973 | 4.05 | 7.2 |
| /blog/basseyny-tbilisi/ | 79 | 3623 | 2.18 | 7.6 |
| /en/blog/tbilisi-techno-scene/ | 79 | 6261 | 1.26 | 6.7 |
| /blog/kanatnaya-doroga-tbilisi/ | 78 | 5548 | 1.41 | 7.7 |
| /blog/metro-tbilisi/ | 73 | 14736 | 0.5 | 5.4 |

## Top countries (28 days, by clicks)

| Country | Clicks | Impr. | CTR% | Pos. |
|---|---|---|---|---|
| GEO | 3900 | 214,414 | 1.82 | 7.1 |
| RUS | 848 | 60,402 | 1.4 | 8.0 |
| USA | 243 | 57,058 | 0.43 | 6.8 |
| DEU | 233 | 17,376 | 1.34 | 6.1 |
| ISR | 216 | 12,339 | 1.75 | 6.5 |
| GBR | 212 | 35,166 | 0.6 | 6.9 |
| UKR | 200 | 14,015 | 1.43 | 6.8 |
| BLR | 192 | 9,469 | 2.03 | 6.8 |
| IND | 176 | 15,940 | 1.1 | 7.2 |
| ARE | 126 | 10,344 | 1.22 | 6.2 |

## By device (28 days)

| Device | Clicks | Impr. | CTR% | Pos. |
|---|---|---|---|---|
| Mobile | 6190 | 343,647 | 1.80 | 6.9 |
| Desktop | 1806 | 238,699 | 0.76 | 7.1 |
| Tablet | 77 | 3,873 | 1.99 | 6.5 |

Desktop CTR is less than half of mobile at similar position — worth checking desktop SERP snippet/title rendering.

## Striking-distance opportunities (position 4-15, impressions ≥50, query×page, 28 days)

650 query×page combinations qualify. Highest-impression ones (near-zero clicks despite big impressions = biggest quick-win pool):

| Query | Page | Impr. | Clicks | Pos. |
|---|---|---|---|---|
| грузинский алфавит | /blog/gruzinskiy-alfavit/ | 9117 | 97 | 4.8 |
| спасибо по грузински | /blog/gruzinskie-frazy/ | 3965 | 18 | 9.3 |
| georgian alphabet | /en/blog/georgian-alphabet/ | 3934 | 8 | 8.8 |
| georgia visa rules for russians 2025 2026 residence | /en/blog/georgia-visa-2026/ | 2741 | 0 | 5.1 |
| спасибо на грузинском | /blog/gruzinskie-frazy/ | 2102 | 3 | 8.4 |
| narikala fortress | /en/blog/narikala-fortress-tbilisi/ | 1887 | 4 | 10.4 |
| what to do on a rainy day | /en/blog/tbilisi-rainy-day/ | 1648 | 0 | 6.5 |
| чача сколько градусов | /blog/chacha-gruzinskaya/ | 1582 | 4 | 6.3 |
| best parks for kids near me | /en/blog/tbilisi-with-kids-guide/ | 1496 | 0 | 8.9 |
| карта метро тбилиси | /blog/metro-tbilisi/ | 1460 | 3 | 7.3 |
| здравствуйте по грузински | /blog/gruzinskie-frazy/ | 1290 | 4 | 7.4 |
| მარტვილის კანიონი | /ge/blog/martvili-canyon/ | 1269 | 9 | 9.9 |
| museums open on monday | /en/blog/tbilisi-museums/ | 1221 | 0 | 8.0 |
| ქართული ანბანი | /ge/blog/georgian-alphabet/ | 1119 | 6 | 6.8 |
| tbilisi to batumi | /en/blog/batumi-from-tbilisi/ | 1067 | 1 | 9.3 |
| ურეკი | /ge/blog/ureki-beach/ | 1043 | 2 | 11.7 |
| что привезти из грузии | /blog/chto-privezti-iz-gruzii/ | 1041 | 25 | 8.6 |
| სადღეგრძელოები ქართულ სუფრაზე | /ge/blog/georgian-toasts/ | 956 | 43 | 6.5 |
| თბილისობა | /ge/blog/tbilisoba/ | 924 | 23 | 6.7 |
| tbilisi to kazbegi | /en/blog/transfer-tbilisi-to-kazbegi/ | 883 | 10 | 7.3 |

Full 650-row list in `google-data.json` under `gsc_28d_qp`.

## Sitemaps (GSC API)

| Sitemap | Submitted URLs | Errors/Warnings | Last submitted |
|---|---|---|---|
| sitemap-index.xml (index) | 875 | 0/0 | 2026-09-17 |
| sitemap.xml (index) | 875 | 0/0 | 2026-07-04 |
| sitemap-pages.xml | 83 | 0/0 | 2026-09-01 |
| sitemap-tours.xml | 245 | 0/0 | 2026-09-01 |
| sitemap-blog.xml | 357 | 0/0 | 2026-08-29 |
| sitemap-landing.xml | 124 | 0/0 | 2026-08-07 |

API note: `contents[].submitted` is submitted-count only, not proof of indexation — needs URL Inspection API (not run this session, see failures above).

## Core Web Vitals

Not fetched — no PSI/CrUX API key configured. To unlock: add `api_key` to `~/.config/claude-seo/google-api.json` or set `GOOGLE_API_KEY`.

## Recommendations (priority)

- **High**: Fix `gsc_site_url` in `~/.config/claude-seo/google-api.json` — it's `sc-domain:sakhva-travel.com` but the service account only has access to the URL-prefix property `https://sakhva-travel.com/`. Every future automated GSC check will 403 until this is corrected.
- **High**: 650 striking-distance query×page pairs at position 4-15 with real impression volume (up to 9k/query) and near-zero clicks — title/meta/snippet optimization on top 20-30 of these is the single largest available CTR win.
- **Medium**: Desktop CTR (0.76%) is less than half mobile (1.80%) at a similar average position — check desktop SERP snippet rendering/schema.
- **Medium**: Add `GOOGLE_API_KEY` to unlock PSI/CrUX field CWV data — currently zero visibility into Core Web Vitals from Google's side.
- **Low**: Add `ga4_property_id` to unlock organic traffic/landing-page tier 2 checks.
