# Technical SEO Audit — sakhva-travel.com
**Дата:** 2026-08-13 | **Проверено на реальном проде** (curl live, не кэш файлов)
**Score: 71/100**

---

## Итоговая таблица

| Категория | Статус | Score |
|-----------|--------|-------|
| Crawlability | PASS | 95/100 |
| Indexability | WARN | 75/100 |
| Security headers | PASS | 92/100 |
| URL / Redirects | WARN | 80/100 |
| hreflang | FAIL | 45/100 |
| Mobile | PASS | 90/100 |
| Core Web Vitals (source signals) | WARN | 70/100 |
| Structured data | PASS | 85/100 |
| Sitemaps / IndexNow | PASS | 90/100 |
| JS rendering / middleware | PASS | 88/100 |

---

## CRITICAL

### C1. hreflang="ka" сломан на главной — href отсутствует в продакшн HTML

**Доказательство (live curl):**
```
curl https://sakhva-travel.com/
→ <link hreflang="ka" rel="alternate"/>   ← href ОТСУТСТВУЕТ
```
В index.html два тега слеплены в одну строку без пробела — при сборке/минификации href теряется:
```html
<link rel="alternate" hreflang="en" href="...en/"><link href="...ge/" hreflang="ka" rel="alternate"/>
```
Google Search Console не видит ka-альтернативу главной. GE-версия фактически отключена от главной в графе hreflang.

**Фикс:** В index.html разделить на отдельные строки, стандартный порядок атрибутов:
```html
<link rel="alternate" hreflang="ka" href="https://sakhva-travel.com/ge/">
```

### C2. hreflang="ka" отсутствует на /ge/ главной

**Доказательство (live curl):**
```
curl https://sakhva-travel.com/ge/
→ hreflang="ru" href="https://sakhva-travel.com/"
→ hreflang="en" href="https://sakhva-travel.com/en/"
← hreflang="ka" ОТСУТСТВУЕТ
```
Нарушена reciprocity: /ge/ не объявляет себя как ka-версию. Google не может замкнуть граф hreflang — ka-страница "невидима" в кластере.

**Фикс:** В ge/index.html (и все ge/ шаблоны) добавить:
```html
<link rel="alternate" hreflang="ka" href="https://sakhva-travel.com/ge/">
```

---

## HIGH

### H1. /ekskursiya-v-kazbegi/ — 404 без редиректа

**Доказательство:**
```
curl -sI https://sakhva-travel.com/ekskursiya-v-kazbegi/ → 404
```
Старый URL тура (формат до переименования). Нет в sitemap (хорошо), но нет и 301. Если существуют внешние ссылки или URL в индексе — link equity теряется.

**Фикс:** В vercel.json добавить:
```json
{ "source": "/ekskursiya-v-kazbegi/", "destination": "/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/", "permanent": true }
```

### H2. /rtveli-grape-harvest/ — 404 без редиректа (не починен с аудита 05.08)

**Доказательство:**
```
curl -sI https://sakhva-travel.com/rtveli-grape-harvest/ → 404
```
Актуальные URL работают (200): `/ekskursiya/rtveli-sbor-vinograda/`, `/en/ekskursiya/rtveli-grape-harvest/`, `/ge/ekskursiya/rtveli-grape-harvest/`. Старый корневой путь — без редиректа.

**Фикс:** В vercel.json:
```json
{ "source": "/rtveli-grape-harvest/", "destination": "/ekskursiya/rtveli-sbor-vinograda/", "permanent": true }
```

### H3. Главная: 359 KB HTML — граница допустимого для LCP

**Доказательство:**
```
wc -c main.html → 359,529 bytes (gzip ~80-100 KB)
```
26 тегов `<script>`, весь контент трёх языков в одном документе. После gzip приемлемо, но парсинг 360 KB DOM задерживает LCP и увеличивает TBT. 3 fetchpriority="high" preload настроены корректно, но общий вес документа остаётся риском.

**Фикс (средний срок):** Вынести EN/GE блоки из единого HTML — edge middleware уже обеспечивает роутинг, но контент всех версий сейчас в одном файле.

### H4. en/blog/things-to-see-kazbegi/ — orphan без ru hreflang

**Доказательство (sitemap-blog.xml):**
```xml
<loc>https://sakhva-travel.com/en/blog/things-to-see-kazbegi/</loc>
← hreflang="ru" ОТСУТСТВУЕТ (нет ru-версии)
x-default → EN (нестандартно, обычно x-default → RU на этом сайте)
```
Страница выпадает из общей hreflang-стратегии сайта. Google может снизить доверие к кластеру.

**Фикс:** Создать RU-версию `/blog/chto-smotret-v-kazbegi/` и добавить в sitemap с полным hreflang-кластером, либо убрать страницу из sitemap и поставить canonical → EN.

---

## MEDIUM

### M1. /ru/ — двухшаговый редирект (308 + 301)

**Доказательство:**
```
https://sakhva-travel.com/ru  → 308 → /ru/
https://sakhva-travel.com/ru/ → 301 → /
```
Два хопа вместо одного. Для `/ru/blog/article/` цепочка ещё длиннее.

**Фикс:** В vercel.json добавить прямой редирект: `/ru/:path*` → `/:path*` с `permanent: true`, убрав зависимость от trailing-slash Vercel.

### M2. Trailing slash: 308 вместо 301

**Доказательство:**
```
curl -I https://sakhva-travel.com/ekskursiya → 308
curl -I https://sakhva-travel.com/blog → 308
```
Vercel по умолчанию отдаёт 308 для trailing-slash добавления. Google понимает 308 = 301, Яндекс исторически предпочитает 301.

**Фикс:** В vercel.json явно задать redirects с `permanent: true` (301) вместо дефолтного Vercel 308.

### M3. blog/ хаб: hreflang="ka" отсутствует

**Доказательство:**
```
curl https://sakhva-travel.com/blog/
→ 3 hreflang-тега: ru, en, x-default
← ka ОТСУТСТВУЕТ
```
GE-версия хаба блога не объявлена. Если /ge/blog/ существует — нужно добавить.

### M4. Sitemap lastmod: статичная дата 2026-08-09 во всех файлах

**Доказательство:**
```xml
<lastmod>2026-08-09</lastmod> — одинаково в sitemap-index и всех дочерних
```
Статичная дата снижает приоритет переобхода краулерами. Google использует lastmod как сигнал свежести.

**Фикс:** Генерировать lastmod динамически из фактической даты изменения файла при деплое.

### M5. CSP: unsafe-inline для script-src

**Доказательство (response header):**
```
script-src 'self' 'unsafe-inline' ...
```
Открывает XSS-вектор через inline скрипты. Приемлемо для статического сайта с inline аналитикой, но не идеал.

**Фикс (долгосрок):** Перейти на nonce или hash-based CSP для script-src.

---

## LOW

### L1. Middleware bot-bypass: не клоакинг, список неполный

**Анализ middleware.js:**
```js
const BOT_UA_RE = /googlebot|yandexbot|bingbot|...gptbot|claudebot.../i
// При совпадении: return (без редиректа) — бот видит RU версию
```
Вердикт: **НЕ клоакинг**. Боты получают RU-версию без изменения содержимого; EN/GE доступны всем по прямым URL. Google видит обе версии. Логика корректна.

Мелкий риск: отсутствуют `Google-InspectionTool`, `Googlebot-Image`, `Googlebot-Video` в списке — они получат 302 на /en/ при заходе на RU-путь. Не критично, но нежелательно.

**Фикс (LOW):** Добавить в BOT_UA_RE: `google-inspectiontool|googlebot-image|googlebot-video`

### L2. Клиентский JS редирект дублирует edge middleware

В index.html есть inline JS с `navigator.language → location.replace()`. При рабочем middleware этот код никогда не срабатывает для новых пользователей (edge отрабатывает раньше). Оставить как fallback — намеренно, документировать.

### L3. Отсутствует preconnect для Cloudinary

Cloudinary (`res.cloudinary.com`) — основной CDN изображений блога. preconnect не объявлен, хотя GTM и Яндекс.Метрика — есть.

**Фикс:**
```html
<link rel="preconnect" href="https://res.cloudinary.com" crossorigin>
```

---

## Подтверждённые исправления с аудита 05.08

| Находка (05.08) | Статус на 13.08 |
|-----------------|-----------------|
| scroll-effects 404 | ПОЧИНЕНО (git d57d2533) |
| miralinks 301 редирект | ПОЧИНЕНО |
| blog robots meta — пустой content | ПОЧИНЕНО (`index,follow,max-image-preview:large,max-snippet:-1`) |
| rtveli в sitemap как broken | ЧАСТИЧНО: `/ekskursiya/rtveli-sbor-vinograda/` работает (200), старый `/rtveli-grape-harvest/` — 404 без редиректа |
| ekskursiya-v-kazbegi 404 | НЕ ПОЧИНЕНО (нет редиректа) |

---

## Crawlability — детали

- robots.txt: корректный, training-scrapers заблокированы (CCBot, cohere-ai), AI-боты разрешены
- Sitemap-index: 4 дочерних файла, итого **746 URLs** (tours 221 / blog 315 / landing 121 / pages 89)
- HTTPS: принудительный, HSTS `max-age=31536000; includeSubDomains; preload`
- www → non-www: 301
- http → https: 301
- /ru/ → /: 301 (через двойной хоп — см. M1)

## Security headers (проверено на живом проде)

| Заголовок | Значение | Оценка |
|-----------|----------|--------|
| HSTS | max-age=31536000; includeSubDomains; preload | PASS |
| X-Frame-Options | DENY | PASS |
| X-Content-Type-Options | nosniff | PASS |
| Referrer-Policy | strict-origin-when-cross-origin | PASS |
| Permissions-Policy | camera=(), microphone=(), geolocation=() | PASS |
| CSP | Присутствует, но unsafe-inline script-src | WARN |
| X-Permitted-Cross-Domain-Policies | none | PASS |
| CORS | access-control-allow-origin: * | INFO |

## Core Web Vitals — сигналы из HTML (без реального замера)

| Сигнал | Статус | Детали |
|--------|--------|--------|
| LCP image preload | PASS | fetchpriority="high" + WebP srcset mobile/desktop |
| Font preload | PASS | woff2 Lora preloaded, CSS async через onload |
| CLS risk | WARN | 44 lazy-img — нужны width/height на всех |
| INP/TBT risk | WARN | 26 тегов script в одном HTML |
| HTML weight | WARN | 359 KB raw (gzip ~80-100 KB) |

*Реальные CWV данные — только через CrUX / PageSpeed Insights с реальным трафиком.*

---

## Приоритеты действий

| Приоритет | Действие | Время |
|-----------|----------|-------|
| 1 (сейчас) | Исправить hreflang="ka" href на главной (C1) | 5 мин |
| 2 (сейчас) | Добавить hreflang="ka" на /ge/ главную (C2) | 5 мин |
| 3 (сегодня) | 301 редиректы /ekskursiya-v-kazbegi/ и /rtveli-grape-harvest/ (H1, H2) | 10 мин |
| 4 (неделя) | Закрыть orphan en/blog/things-to-see-kazbegi/ (H4) | 30 мин |
| 5 (планово) | Снизить HTML главной < 280 KB (H3) | крупная задача |
