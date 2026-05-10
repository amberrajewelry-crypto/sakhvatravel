# Technical SEO Audit — sakhva-travel.com

**Date:** 2026-05-04
**Pages analyzed:** ~143 (homepage, 24 tours, ~108 blog, category pages, about)
**Stack:** Static HTML on Vercel + Cloudflare CDN

---

## Overall Score: 87 / 100

| Category | Score | Status |
|----------|-------|--------|
| Crawlability | 90 | PASS |
| Indexability | 82 | WARN |
| Security | 95 | PASS |
| URL Structure | 78 | WARN |
| Mobile | 92 | PASS |
| Core Web Vitals | 85 | PASS |
| Structured Data | 93 | PASS |
| JS Rendering | 75 | WARN |
| IndexNow | 90 | PASS |

---

## 1. Crawlability (90/100) -- PASS

### robots.txt -- PASS
- Корректный формат, Sitemap директива присутствует
- AI-краулеры (GPTBot, ClaudeBot, PerplexityBot и др.) -- явно разрешены
- Вредоносные боты (MJ12bot, DotBot, Bytespider) -- заблокированы
- Verification-файлы правильно запрещены (yandex_*.html, google*.html)

### sitemap.xml -- WARN
- **207 URL** в sitemap
- Формат корректный, lastmod присутствует
- Ссылка на sitemap в robots.txt -- есть

**Проблемы:**

| Приоритет | Проблема |
|-----------|----------|
| HIGH | Sitemap содержит URL с редиректами: `/tour/old-tbilisi/` и `/tour/emigrant/` -- эти страницы имеют 301 редиректы в vercel.json, но файлы на диске ещё существуют, поэтому Vercel отдаёт 200. Либо удалить файлы и убрать из sitemap, либо убрать из vercel.json. |
| MEDIUM | `/en/blog/` (index) в sitemap, но физический файл отсутствует (отдаёт 200 -- видимо через rewrite). Проверить что это рабочая страница. |

### llms.txt -- PASS
- Файл существует, грамотно структурирован
- Содержит Q&A для AI-поисковиков
- Ссылка `<link rel="alternate" type="text/plain" href="/llms.txt">` в head -- есть

---

## 2. Indexability (82/100) -- WARN

### Canonical Tags -- PASS
- Все проверенные страницы имеют `<link rel="canonical">`
- Canonical URL совпадает с фактическим URL
- Trailing slash -- единообразно

### Hreflang -- PASS (с оговорками)
- ru/en/x-default тройка присутствует на всех проверенных страницах
- x-default указывает на RU-версию -- корректно для основной аудитории
- Взаимные ссылки (RU→EN, EN→RU) -- есть

**Проблемы:**

| Приоритет | Проблема |
|-----------|----------|
| HIGH | `/en/tour/old-tbilisi/` -- отсутствует на диске, но RU-версия `/tour/old-tbilisi/` ссылается на неё через hreflang. EN-версия вернёт 404. Нужно либо создать страницу, либо убрать hreflang и перенаправить. |
| MEDIUM | Блог-статьи на RU без EN-пары (54 RU vs 52 EN) -- 2 статьи без hreflang на EN. Не критично, но стоит проверить какие именно. |

### Meta Robots -- PASS
- `index,follow,max-image-preview:large,max-snippet:-1` -- оптимальная настройка
- 404-страница имеет `noindex,follow` -- корректно

### Thin Content Risk
- Блог-статьи в целом длинные и качественные
- FAQ schema добавлено на статьях

---

## 3. Security (95/100) -- PASS

### HTTPS -- PASS
- SSL валиден (Cloudflare)
- HTTP→HTTPS редирект: 301 -- корректно
- www→non-www редирект: 301 -- корректно

### Security Headers -- PASS

| Header | Value | Status |
|--------|-------|--------|
| Strict-Transport-Security | max-age=31536000; includeSubDomains; preload | PASS |
| Content-Security-Policy | Полная политика с whitelist | PASS |
| X-Content-Type-Options | nosniff | PASS |
| X-Frame-Options | DENY | PASS |
| Referrer-Policy | strict-origin-when-cross-origin | PASS |
| Permissions-Policy | camera=(), microphone=(), geolocation=() | PASS |

**Замечания:**

| Приоритет | Проблема |
|-----------|----------|
| LOW | CSP содержит `'unsafe-inline'` для script-src. Для статического сайта можно перейти на nonce или hash-based. Не критично для SEO. |
| LOW | `security.txt` отсутствует (404 на /.well-known/security.txt). Не влияет на SEO, но хорошая практика. |

---

## 4. URL Structure (78/100) -- WARN

### Clean URLs -- PASS
- Чистые URL без параметров: `/tour/kazbegi/`, `/blog/kazbegi-iz-tbilisi-2026/`
- Trailing slash единообразен (vercel.json `trailingSlash: true`)
- Без trailing slash возвращает 308 с редиректом -- корректно

### Redirects -- WARN

| Приоритет | Проблема |
|-----------|----------|
| CRITICAL | Vercel redirects в vercel.json НЕ РАБОТАЮТ для `/tour/old-tbilisi/` и `/tour/emigrant/` потому что файлы index.html существуют на диске. Vercel отдаёт файл напрямую (200), игнорируя redirect правило. **Решение:** удалить файлы `/tour/old-tbilisi/index.html` и `/tour/emigrant/index.html` (и EN-аналоги) -- тогда vercel.json redirect заработает. Или: заменить содержимое файлов на meta-refresh + JS redirect. |
| CRITICAL | В sitemap.xml присутствуют 3 URL которые должны быть редиректами: `tour/old-tbilisi/`, `tour/emigrant/`, `en/tour/emigrant/`. Удалить их из sitemap после починки редиректов. |
| MEDIUM | Нет `en/tour/old-tbilisi/` -- RU-страница ссылается на неё через hreflang, но EN-страница вернёт 404. |

### Language redirect (JS) -- WARN

| Приоритет | Проблема |
|-----------|----------|
| HIGH | Главная страница (`/`) содержит JS-скрипт `location.replace("/en"+p)` который перенаправляет на EN-версию на основе localStorage. Для поисковых краулеров это не проблема (они не выполняют localStorage), но для пользователей без JS это невидимо. При первом визите не-RU пользователь получает JS-редирект. Это работает, но `Vary: Accept-Language` или server-side detection было бы надёжнее. |
| MEDIUM | JS-скрипт языковой детекции стоит ДО `<meta charset>` на страницах туров. Рекомендуется переместить после charset. |

---

## 5. Mobile (92/100) -- PASS

### Viewport -- PASS
- `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">` -- корректно
- `viewport-fit=cover` для safe area на iPhone -- хорошо

### Touch Targets -- PASS
- Burger menu: `min-width:44px; min-height:44px` -- соответствует WCAG
- CTA кнопки с достаточным padding

### Mobile UI -- PASS
- FAB кнопка для мобильного CTA
- Drawer навигация для мобилки
- `env(safe-area-inset-bottom)` учтён

### Font Size -- PASS
- Минимум 12px на мобилке (nav: 13px, body: serif)

**Замечания:**

| Приоритет | Проблема |
|-----------|----------|
| LOW | Некоторые страницы туров используют отдельные CSS файлы (raleway.css, montserrat.css) вместо общего all.css. Не критично, но увеличивает количество запросов. |

---

## 6. Core Web Vitals (85/100) -- PASS

### LCP (Largest Contentful Paint) -- PASS
- Hero-изображение предзагружено через `<link rel="preload" fetchpriority="high">`
- Responsive srcset с media query (mob/desktop) -- оптимально
- WebP формат
- Размеры: mob 768w, desktop 1200w -- хорошо

### INP (Interaction to Next Paint) -- PASS
- Минимум JS на критическом пути
- GA загружается отложенно на homepage (по interaction + 7s timeout)
- Event listeners с `{passive: true}` -- хорошо

### CLS (Cumulative Layout Shift) -- PASS
- Все img-теги на homepage имеют `width` и `height` -- предотвращает CLS
- Gallery images: SVG placeholder с размерами + lazy load -- хорошо
- Font preload для Lora -- предотвращает FOUT/CLS

**Проблемы:**

| Приоритет | Проблема |
|-----------|----------|
| HIGH | **54 блог-статьи загружают GA синхронно** (`<script async src="googletagmanager">` + inline `gtag()`). Главная страница использует отложенную загрузку (loadGA по interaction), но блог -- нет. Это +100-200ms к LCP на блоге. Привести к единому паттерну deferred loading. |
| MEDIUM | Страницы туров загружают fonts по отдельным файлам (raleway.css, montserrat.css, lora.css) вместо единого all.css?v=1 как на главной. Больше HTTP-запросов. |
| MEDIUM | CSS на homepage загружен через `preload as="style" onload` (deferred.css, seamless.css) -- хорошо для FCP, но при медленном соединении может вызвать FOUC. |
| LOW | Video-элементы на homepage имеют `preload="none"` -- корректно для CWV, не блокируют загрузку. |

---

## 7. Structured Data (93/100) -- PASS

### Homepage -- PASS
- `@graph` с WebSite, WebPage, TravelAgency
- AggregateRating (4.9, 87 reviews)
- Контактные данные, openingHours, geo, priceRange

### Tour Pages -- PASS
- TouristTrip schema с itinerary, offers, aggregateRating
- BreadcrumbList -- корректно
- WebPage с breadcrumb reference

### Blog Pages -- PASS
- BlogPosting с author (Person), publisher (Organization)
- datePublished, dateModified
- FAQPage schema -- Rich Snippets potential
- BreadcrumbList

**Замечания:**

| Приоритет | Проблема |
|-----------|----------|
| MEDIUM | TouristTrip на всех турах использует один и тот же aggregateRating (4.9, 87 reviews). Если это общий рейтинг бизнеса, лучше привязать к TravelAgency, а не к каждому отдельному туру. Google может посчитать это манипуляцией. |
| LOW | OG image на homepage -- webp формат. Некоторые платформы (старые мессенджеры) не поддерживают webp для OG. Рекомендуется jpg/png fallback. |

---

## 8. JavaScript Rendering (75/100) -- WARN

### SSR vs CSR -- Гибрид
- Основной контент -- статический HTML (серверный рендеринг) -- PASS
- Без SPA фреймворков -- PASS

**Проблемы:**

| Приоритет | Проблема |
|-----------|----------|
| HIGH | **JS language redirect на RU-страницах** -- `location.replace("/en"+p)` выполняется до рендеринга контента. Googlebot видит RU-контент (не выполняет localStorage), но Bing/Yandex могут вести себя иначе. Рекомендация: для SEO-безопасности использовать server-side redirect (Vercel Edge middleware) или оставить как есть с пониманием рисков. |
| HIGH | **JS language detection** на страницах туров стоит ДО `<meta charset>`. Первый `<script>` в `<head>` -- до charset. Браузер может некорректно интерпретировать кириллицу в скрипте. |
| MEDIUM | **NoScript fallback** -- блог-статьи используют `<link rel="stylesheet">` напрямую, а homepage/EN-homepage используют `preload + onload + noscript` паттерн. Нет единообразия. |
| LOW | `main.js` загружается с query string `?v=32` для cache-busting. Работает, но content-hash в имени файла надёжнее. |

---

## 9. IndexNow Protocol (90/100) -- PASS

- IndexNow key file: `DE25F3FA51D1F1E934763682A270AF53.txt` -- доступен, содержит ключ
- CSP connect-src содержит `https://api.indexnow.org` -- разрешено
- Bing Webmaster верифицирован (msvalidate.01)
- Yandex Webmaster верифицирован (yandex-verification)

**Замечания:**

| Приоритет | Проблема |
|-----------|----------|
| LOW | IndexNow ключ совпадает с Bing verification token -- работает, но лучше использовать отдельный ключ. |

---

## Сводка приоритетных действий

### CRITICAL (2)

1. **Сломанные редиректы old-tbilisi и emigrant** -- файлы на диске перебивают vercel.json redirects. Удалить файлы:
   - `/tour/old-tbilisi/index.html`
   - `/tour/emigrant/index.html`
   - `/en/tour/emigrant/index.html`
   
2. **Убрать из sitemap.xml** URL которые должны быть редиректами:
   - `tour/old-tbilisi/`
   - `tour/emigrant/`
   - `en/tour/emigrant/`

### HIGH (4)

3. **Синхронная загрузка GA на 54 блог-статьях** -- перевести на deferred loading (по interaction + timeout) как на homepage. Влияет на LCP.

4. **Hreflang на old-tbilisi** -- RU-страница ссылается на `/en/tour/old-tbilisi/` которой нет. Если страницы убираются -- убрать hreflang. Если остаются -- создать EN-версию.

5. **JS charset order** -- на страницах туров `<script>` стоит до `<meta charset>`. Переместить charset перед любым JS.

6. **JS language redirect** -- `location.replace` на RU-страницах. Рассмотреть Vercel Edge Middleware для серверной языковой детекции. Или Accept-Language header в vercel.json.

### MEDIUM (5)

7. **Единообразие font loading** -- туры загружают 3 отдельных CSS (raleway, montserrat, lora), homepage использует all.css. Унифицировать.

8. **AggregateRating на каждом туре** -- один и тот же рейтинг на всех турах может быть расценен как спам. Привязать к бизнесу, не к туру.

9. **2 блог-статьи без EN-пары** -- найти и либо создать EN-версии, либо убрать hreflang en.

10. **NoScript/font loading единообразие** -- блог vs homepage используют разные паттерны.

11. **OG image формат** -- webp может не работать на старых платформах. Добавить jpg fallback.

### LOW (4)

12. CSP unsafe-inline -- рассмотреть nonce-based.
13. security.txt -- создать файл.
14. Cache-busting main.js -- перейти на content hash.
15. IndexNow ключ = Bing token -- разделить.

---

## Redirect Chain Analysis

| From | To | Status | Hops |
|------|----|--------|------|
| http://sakhva-travel.com | https://sakhva-travel.com/ | 301 | 1 |
| https://www.sakhva-travel.com | https://sakhva-travel.com/ | 301 | 1 |
| /tour/kazbegi (no slash) | /tour/kazbegi/ | 308 | 1 |
| /tour/old-tbilisi/ | (should be 301 to /tour/kutaisi/ but returns 200) | BROKEN | 0 |
| /tour/emigrant/ | (should be 301 to /tour/batumi/ but returns 200) | BROKEN | 0 |

Цепочки редиректов: максимум 1 хоп -- отлично. Нет двойных/тройных цепочек.

---

## HTTP Status Summary

| URL Pattern | Expected | Actual | Status |
|-------------|----------|--------|--------|
| / | 200 | 200 | OK |
| /en/ | 200 | 200 | OK |
| /tour/kazbegi/ | 200 | 200 | OK |
| /blog/kazbegi-iz-tbilisi-2026/ | 200 | 200 | OK |
| /tour/old-tbilisi/ | 301 | 200 | BROKEN |
| /tour/emigrant/ | 301 | 200 | BROKEN |
| /en/tour/old-tbilisi/ | 301 | 404 | PARTIAL |
| /.well-known/security.txt | 200 | 404 | MISSING |
| /robots.txt | 200 | 200 | OK |
| /sitemap.xml | 200 | 200 | OK |
| /llms.txt | 200 | 200 | OK |

---

## Sitemap Coverage

| Segment | On disk | In sitemap | Gap |
|---------|---------|------------|-----|
| RU blog | 54 | 55 (incl /blog/ index) | 0 missing |
| EN blog | 52 | 53 (incl /en/blog/ index) | 0 missing |
| RU tours | 12 | 12 | 0 |
| EN tours | 12 | 12 | 0 |
| Category | 6 | 6 | 0 |
| About | 2 | 2 | 0 |
| Homepages | 2 | 2 | 0 |
| **Total** | **140+** | **207** | Includes redirected URLs |
