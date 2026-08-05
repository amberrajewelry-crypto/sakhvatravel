# Technical SEO Audit — sakhva-travel.com
Date: 2026-08-05
Auditor: Claude (seo-technical skill)
Branch audited: fix/a11y-lighthouse-100

---

## Score: 74 / 100

---

## CRITICAL

### 1. Дублированный `<link rel="canonical">` на всех GE-страницах (106 страниц)

**Симптом:** Каждый `index.html` в `/ge/` содержит ровно 2 тега `<link rel="canonical">`. Пример — `ge/blog/tbilisi-metro-guide/index.html`:
```html
<link href="https://sakhva-travel.com/ge/blog/tbilisi-metro-guide/" rel="canonical"/>
...
<link href="https://sakhva-travel.com/ge/blog/tbilisi-metro-guide/" rel="canonical"/>
```
Оба указывают на один URL (значения совпадают), но по спеке Google берёт первый canonical и игнорирует второй с предупреждением — это сигнал неряшливости шаблона и может вызвать предупреждение в GSC.

**Масштаб:** 106 из ~110+ GE-страниц (все blog + ekskursiya + about/saba + blog/index).

**Фикс:** В шаблоне генерации GE-страниц найти и убрать дублирующий canonical. Скорее всего один вставлен в `<head>`-шаблоне, второй — в компоненте страницы. Проверить скрипт-генератор GE.

```bash
grep -rn 'rel="canonical"' ge/ | grep -v "node_modules" | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -5
```

---

## HIGH

### 2. `miralinks-article.html` → 308 → 404 (битый публичный URL)

**Симптом:** `https://sakhva-travel.com/miralinks-article.html` отвечает `308 Permanent Redirect` → `/miralinks-article/` → `404`. Файл существует локально с `noindex`, но Vercel с `cleanUrls:true` делает 308 редирект `.html` → slug, а директории `/miralinks-article/` нет.

**Риск:** Внешние ссылки (miralinks — платный линкбилдинг-сервис), которые могут уже вести на этот URL, упираются в 404. Кроме того, файл с `noindex` публично доступен через `.html`-URL до редиректа.

**Фикс (вариант 1):** Добавить в `vercel.json`:
```json
{ "source": "/miralinks-article", "destination": "/", "statusCode": 301 }
```
**Фикс (вариант 2):** Переименовать в директорию `miralinks-article/index.html` — тогда `cleanUrls` отдаст 200.

---

### 3. `dashboard/` и `partner/` открыты (HTTP 200), несмотря на `Disallow`

**Симптом:** Оба отдают `200 OK` на проде. `robots.txt` закрывает их (`Disallow: /dashboard/`, `Disallow: /partner/`), и оба имеют `noindex` в HTML — это правильно. Но сами страницы доступны без авторизации.

**Это не SEO-баг** (robots + noindex работают), однако если страницы содержат служебные данные — это потенциальный security-риск. Рекомендуется добавить password-protect или переместить за `/api/`.

**SEO-оценка:** Medium (noindex есть, robots закрыт) → но помечен как HIGH из-за security-аспекта.

---

### 4. Sitemap lastmod застряли в июле 2026

**Симптом:**
- `sitemap-blog.xml` → lastmod `2026-07-15`
- `sitemap-tours.xml` → lastmod `2026-07-17`
- `sitemap-landing.xml` → lastmod `2026-07-14`
- `sitemap-pages.xml` → lastmod `2026-07-16`

С тех пор деплоились новые страницы (metro, content dojatie, EN/GE туры). Google/Yandex видят устаревший lastmod и могут занижать приоритет перекраулинга.

**Фикс:** Обновлять `lastmod` в sitemap-index при каждом деплое. Добавить в билд-скрипт:
```bash
TODAY=$(date +%Y-%m-%d)
sed -i '' "s/<lastmod>[0-9-]*<\/lastmod>/<lastmod>$TODAY<\/lastmod>/g" sitemap-index.xml
```

---

## MEDIUM

### 5. Hreflang: непоследовательный формат между страницами

**Симптом:** На главной (`/`) и EN-главной (`/en/`) hreflang-теги написаны в разном порядке атрибутов:
- RU: `<link rel="alternate" hreflang="ru" href="...">`
- GE: `<link href="..." hreflang="ka" rel="alternate"/>` (порядок инвертирован, самозакрывающийся)

Google обрабатывает оба формата корректно, но это признак разных шаблонов/генераторов и увеличивает риск будущих рассинхронов.

**Фикс:** Унифицировать формат в шаблонах — выбрать один порядок атрибутов.

---

### 6. Hreflang x-default = RU на турах, EN на главной — непоследовательно

**Симптом:**
- Главная (`/`): `x-default` → `https://sakhva-travel.com/` (RU) — ОК
- `/en/`: `x-default` → `https://sakhva-travel.com/` (RU) — ОК  
- `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/`: `x-default` → та же RU-страница — ОК

Это последовательно. Однако для тур-страниц, ориентированных на EN-аудиторию (иностранцы), логичнее `x-default` → EN-версия. Это спорный момент, не баг.

**Рекомендация:** Оставить как есть для RU-ориентированных страниц, рассмотреть смену `x-default` на EN для туров, где EN — основная аудитория.

---

### 7. Robots.txt: `Disallow: /dashboard/` и `/partner/` дублируются трижды

**Симптом:** В `robots.txt` правила для dashboard/partner повторяются 3 раза (под `User-agent: *`, под `AhrefsBot`, под `AhrefsSiteAudit`). Технически не баг, но увеличивает файл и усложняет поддержку.

**Фикс:** Вынести общие правила только в `User-agent: *`, оставить специфичные только в именованных блоках.

---

### 8. Sitemap: sitemap.xml → 301 → sitemap-index.xml (лишний хоп)

**Симптом:** `https://sakhva-travel.com/sitemap.xml` отвечает `301` → `/sitemap-index.xml`. В `robots.txt` указан `Sitemap: https://sakhva-travel.com/sitemap-index.xml` (прямая ссылка), что правильно. Но если кто-то (GSC, сторонний инструмент) читает `sitemap.xml` — получает редирект.

**Фикс:** Либо сохранить файл `sitemap.xml` с содержимым sitemap-index, либо оставить как есть (не критично, т.к. robots.txt указывает напрямую).

---

## LOW

### 9. Core Web Vitals — известный контекст (не исследовался повторно)

По данным из памяти проекта (PSI mobile 79-93):
- Реальный LCP ~690мс (хорошо, <2.5s)
- Потолок держат Yandex Metrica / GTM / PostHog (~870мс задержка)
- CLS: не обнаружено проблем (hero-image имеет явные `width="1920" height="1434"`, `fetchpriority="high"`)
- INP: не анализировался (статический HTML, JS минимален)

**Статус:** Pass для LCP. Аналитика — известный потолок, не трогать без явного решения удалить трекинг.

---

### 10. JavaScript-редиректы по языку работают на клиенте

**Симптом:** Все три homepage (RU/EN/GE) содержат inline JS для автоперенаправления по `navigator.language`. Боты исключены через UA-проверку. Это ОК с точки зрения SEO (боты не редиректируются, canonical корректный).

**Единственный риск:** Если бот не попал в список regex (`/bot|crawl|spider.../`), он может быть перенаправлен — это cloaking-риск. Список UA достаточно широкий, риск низкий.

---

### 11. IndexNow: ключ присутствует, но lastmod sitemap не обновляется

`indexnow-key.txt` существует, ключ `323a3fe6d706feaf3b69e9d6919edec3` совпадает. Три ключа верификации (`323a3...txt`, `8d0ae...txt`, `DE25F...txt`) также в корне.

**Статус:** IndexNow настроен корректно. Добавить автоматический `submit` после деплоя новых/обновлённых URL (Bing, Yandex).

---

## Пройдено без замечаний

| Категория | Статус |
|-----------|--------|
| HTTPS / HSTS | Pass — `max-age=31536000; includeSubDomains; preload` |
| CSP | Pass — подробный, покрывает все внешние источники |
| X-Content-Type-Options | Pass — `nosniff` |
| X-Frame-Options | Pass — `DENY` |
| Permissions-Policy | Pass — `camera=(), microphone=(), geolocation=()` |
| Referrer-Policy | Pass — `strict-origin-when-cross-origin` |
| Canonical: self-canonical | Pass — RU/EN/GE указывают на себя |
| Hreflang взаимность | Pass — ru↔en↔ka взаимны, x-default присутствует |
| Hreflang несуществующие URL | Pass — 0 битых EN/GE counterparts |
| Redirect chains >1 хоп | Pass — 0 цепочек в 394 редиректах |
| www → non-www | Pass — 301 redirect настроен |
| TrailingSlash консистентность | Pass — `trailingSlash: true`, `cleanUrls: true` |
| robots.txt | Pass — служебные пути закрыты, AI-боты явно разрешены |
| Structured data (JSON-LD) | Pass — присутствует на всех ключевых типах страниц |
| Mobile viewport | Pass — `width=device-width, initial-scale=1.0, viewport-fit=cover` |
| Hero LCP image | Pass — `fetchpriority="high"`, `loading="eager"`, явные размеры, srcset |
| noindex на утилитарных страницах | Pass — booking, payment-*, links/ имеют noindex |
| Rendering (SSR vs CSR) | Pass — статический HTML, JS не требуется для контента |

---

## Итоговые приоритеты

| # | Severity | Проблема | Затронуто |
|---|----------|----------|-----------|
| 1 | Critical | Дублированный canonical в `/ge/` | 106 страниц |
| 2 | High | miralinks-article.html → 308 → 404 | 1 URL + входящие ссылки |
| 3 | High | Sitemap lastmod устарел | 4 sitemap-файла |
| 4 | Medium | Непоследовательный формат hreflang-тегов | Все страницы |
| 5 | Medium | sitemap.xml → 301 → sitemap-index.xml | Лишний хоп |
| 6 | Low | Robots.txt дублирование правил | Косметика |
