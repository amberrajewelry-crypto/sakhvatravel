# Sakhva Travel — Тур-гид в Тбилиси, Грузия

## ⛔ ПЕРЕД КАЖДЫМ ДЕПЛОЕМ — ОБЯЗАТЕЛЬНО

```
node scripts/predeploy-check.js <изменённый файл> index.html
```

Если есть ❌ ошибки — исправить, запустить снова, только потом деплоить.

## ⛔ НЕЛЬЗЯ ТРОГАТЬ БЕЗ ЯВНОЙ КОМАНДЫ
- `main.js` — логика букинга, оплат, квиза, языков, валют
- `index.html` — элементы которые не в задаче (FAB, nav, footer, hero)
- Файлы в `/images/` — не перезаписывать без проверки что файл рабочий
- `/blog/` статьи — не удалять, не изменять контент без команды

## ⛔ РЕЖИМ РАБОТЫ
- **НЕ использовать** subagent-driven-development
- **НЕ использовать** dispatching-parallel-agents
- **НЕ использовать** using-git-worktrees
- Все правки напрямую через Edit/Read/Bash

## ГЛАВНОЕ ПРАВИЛО
**Прогресс необратим.** Никогда не откатывать назад без команды пользователя.

## АРХИТЕКТУРА МОБИЛЬНОГО UI (НЕ ЛОМАТЬ)
- **FAB-кнопка** `#fab-main` — мобильный CTA (чат/WA/TG), `bottom:20px right:20px`
- **НЕТ** mobile-sticky-bar на главной — она была удалена намеренно, FAB её заменил
- **`.sticky-wa`** — плавающий WA, скрыт на мобилке через `@media(max-width:768px){display:none}`
- На страницах туров `/tour/*/` — своя `mobile-sticky-bar` есть и должна быть

## Проект
- Живой сайт: https://sakhva-travel.com
- Папка: /Users/vladimir/sakhva-travel/
- Deploy: `cd /Users/vladimir/sakhva-travel && npx vercel deploy --prod --scope amberrajewelry-cryptos-projects`
- Vercel проект: amberrajewelry-cryptos-projects/sakhva-travel
- Vercel Team ID: team_k0iaVI0CPoD0ENniwdu3J4wM
- Vercel Project ID: prj_HyyV19W7zflvjEnKpy2cdHqmacww (актуальный, из .vercel/project.json; старый prj_xTbr… устарел после пере-линка проекта 04.07)
- Vercel Token: в ~/Library/Application Support/com.vercel.cli/auth.json

## Стек
- Статический HTML (index.html + страницы туров + блог)
- Без фреймворков
- Git репозиторий ЕСТЬ: /Users/vladimir/sakhva-travel/.git
- vercel.json для роутинга

## Текущее состояние (обновлено 15.04.2026)
- **Прод (sakhva-travel.com)** = 42 статьи блога, новый дизайн, задеплоен
- Локальные файлы = прод (синхронизированы)

## Vercel Aliases (созданы 10.04.2026)
- https://sakhva-old-38.vercel.app — версия 5 апреля (38 статей)
- https://sakhva-apr8.vercel.app — версия 8 апреля (40 статей)
- https://sakhva-apr9-morning.vercel.app — версия 9 апреля утро (текущий прод)
- https://sakhva-current.vercel.app — снапшот версии до отката

## Структура сайта
- /index.html — главная
- /tour/ — страницы туров (12 маршрутов)
- /blog/ — 42 статьи, все задеплоены
- /about/ — о гиде
- /api/ — API (Google Places, NOWPayments)
- /images/ — изображения
- /images/blog/ — WebP 1200×630 для блога

## Гид
- Имя: Тимур
- WhatsApp: +995511272623

## SEO правила
- Title включает год и цену: "Казбеги из Тбилиси 2026 — от 45€ с гидом"
- Ниша: длиннохвостые запросы
- Агрегаторы (Tripster, Sputnik8, Guidego) — не конкурировать напрямую
- robots.txt и sitemap.xml — не трогать без явной команды

## Туры и цены (в евро €)
- Казбеги за 1 день — от €45/чел
- Кахетия, Мцхета, Ночной Тбилиси, Батуми и др.

## Аудитория
- Русскоязычные релоканты (100–200 тыс. в Тбилиси)
- Туристы по картам ("гид Тбилиси")
- English-speaking tourists

## Интеграции
- GA4: G-3X83YZHY6S ✅
- Google Ads: AW-8133499399 ✅
- GSC: google8598dd92e7bc33ca.html ✅
- Yandex Webmaster: yandex_59a834df1510fae1 ✅
- Bing: sakhvatravel3231259ca6306569.txt ✅
- NOWPayments: NOWPAYMENTS_API_KEY в Vercel env ✅
- Google Places: GOOGLE_PLACES_API_KEY в Vercel env ✅
- IndexNow: DE25F3FA51D1F1E934763682A270AF53.txt ✅
- llms.txt ✅
- Airtable CRM: base appvP72OjZeVJ0XWh ✅
- n8n Railway: n8n-production-f095.up.railway.app ✅
- Cloudinary: cloud dtfq3xq3t, папка sakhva-travel/blog/ ✅
