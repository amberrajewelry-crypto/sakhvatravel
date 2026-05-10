# Sakhva Travel — проектный контекст

## Стек
- Статический HTML + Vercel Serverless Functions
- Без git (деплой напрямую через vercel CLI)
- JS: main.js (вся логика — букинг, оплата, квиз, UI)
- CSS: встроен в index.html

## Деплой
```bash
cd /Users/vladimir/sakhva-travel && npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
```

## Ключевые файлы
- `index.html` — главная (1850+ строк)
- `main.js?v=3` — вся логика
- `vercel.json` — роутинг, CSP, кеш, редиректы
- `api/create-payment.js` — NOWPayments invoice
- `sitemap.xml` — 93 URL
- `blog/` — 42 статьи RU. ЗАПРЕЩЕНО убирать статьи из блога.
- `en/blog/` — 10 статей EN
- `tour/` — 12 страниц туров RU
- `en/tour/` — 12 страниц туров EN
- `tours/` — 3 категорийные страницы RU (day-trips, walking, wine)
- `en/tours/` — 3 категорийные страницы EN

## Переменные (Vercel env)
- NOWPAYMENTS_API_KEY
- FORMSPREE_ID
- GOOGLE_PLACES_API_KEY

## Интеграции
- GA4: G-3X83YZHY6S
- Google Ads: AW-8133499399
- GSC: верифицирован
- Airtable CRM: base appvP72OjZeVJ0XWh
- n8n: Railway (5 воркфлоу)
- Cloudinary: cloud dtfq3xq3t, папка sakhva-travel/blog/
- GBP: верифицирован CID 14070083063461040701

## Запреты
- НИКОГДА не удалять статьи блога
- НИКОГДА не менять vercel.json редиректы без проверки
- НЕ деплоить без проверки sitemap.xml
- Версия 8 апреля = основная для блога

## SEO приоритеты
- hreflang ru/en на всех страницах
- FAQ schema на статьях блога
- Review-quotes для E-E-A-T
- Thin content: расширить статьи < 1500 слов
