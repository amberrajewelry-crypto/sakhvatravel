# Sakhva Travel

Private tour guide service in Tbilisi, Georgia.  
Live: [sakhva-travel.com](https://sakhva-travel.com)

## Stack

- Static HTML (no framework)
- Vercel hosting + CDN
- `main.js` -- booking, quiz, payments, UI logic
- Inline critical CSS + deferred external CSS

## Structure

```
/                       -- RU homepage
/en/                    -- EN homepage
/ekskursiya/            -- 46 tour pages (RU)
/en/ekskursiya/         -- 46 tour pages (EN)
/blog/                  -- 74 blog posts (RU)
/en/blog/               -- 55 blog posts (EN)
/about/                 -- guide profile
/contacts/              -- contacts
10 region pages          -- kakheti/, adjara/, imereti/, etc.
14 geo pages             -- tury-v-gruziyu-iz-moskvy/, etc.
```

**Total:** 266 URLs in sitemap (155 RU + 112 EN)

## Deploy

```bash
npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
```

Pre-deploy check:
```bash
node scripts/predeploy-check.js index.html
```

## SEO

- **Health Score:** 92/100
- **Schema:** TravelAgency, Person, TouristTrip x10, FAQPage (25 Q&A), Review x5, Service x4, ItemList, VideoObject, BreadcrumbList, SpeakableSpecification
- **hreflang:** ru + en + x-default on all pages
- **Indexing:** IndexNow (Yandex + Bing), Google Indexing API, Yandex Webmaster API
- **AI:** robots.txt allows GPTBot, ClaudeBot, PerplexityBot; llms.txt present
- **Wikidata:** Q139498917

## Integrations

- GA4: G-3X83YZHY6S
- Google Ads: AW-8133499399
- Yandex Metrika
- PostHog
- Airtable CRM: appvP72OjZeVJ0XWh
- n8n (Railway): 5 workflows
- NOWPayments (crypto)
- Cloudinary: dtfq3xq3t
- GBP: CID 14070083063461040701

## Guide

- Name: Timur
- WhatsApp: +995511272623
- Telegram: @SakhvaGuideBot
- Rating: 4.9 / 87 reviews
