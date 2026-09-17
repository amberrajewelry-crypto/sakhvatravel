# Погодный SEO-кластер — Implementation Plan

> **Исполнение:** инлайн, задача-за-задачей (проект запрещает subagent-driven/parallel/worktrees — см. CLAUDE.md). Чекбоксы `- [ ]` для трекинга. Спека: `SPEC-pogoda-cluster.md`.

**Goal:** Развернуть кластер `/pogoda/` (хаб + 11 регионов + ~25 городов, RU) — краткие страницы с климат-таблицей + live-виджетом + перелиновкой на туры, для органического трафика туристов на этапе планирования.

**Architecture:** Статический HTML, генерация Python-скриптом (образец `scripts/gen-blog.py`). Live-погода — edge `api/weather.js` (Open-Meteo, без ключа). Климат-нормали — из Open-Meteo archive, статикой в HTML (индексируется). Перелинковка mesh: хаб↔регион↔город↔тур.

**Tech Stack:** HTML/CSS (существующий шаблон), Python 3 (генератор + сбор климата), Open-Meteo API, Vercel edge, IndexNow + Google Indexing API.

**SEO-методология (seo-cluster):** intent всех страниц — informational (погода) с commercial-мостом (тур); navigational нет. Анти-каннибализация: регион и город — разные primary keyword и canonical. Link matrix: min 3 входящих на страницу, 0 orphans. Полный SERP-overlap прогон НЕ делаем (ПФ + очевидный спрос; экономия) — решение зафиксировано.

---

## File Structure

- Create: `data/pogoda-geo.json` — регионы+города: slug, name, coords, tour_slug, region, neighbors[]
- Create: `data/climate.json` — климат-нормали по месяцам на каждую точку (из archive)
- Create: `scripts/fetch-climate.py` — разовый сбор нормалей из Open-Meteo archive
- Create: `scripts/gen-pogoda.py` — генератор страниц (хаб + регион + город) из geo+climate
- Modify: `api/weather.js` — добавить города в REGIONS из geo.json
- Generated: `pogoda/index.html`, `pogoda/{slug}/index.html` (~37 файлов)
- Modify: тур-страницы (`tour/*/`, `ekskursiya/*/`) — блок «Проверить погоду»
- Modify: футер-шаблон — ссылка на `/pogoda/`
- Modify: `sitemap.xml` — добавить URL кластера

---

## Task 1: Гео-данные кластера

**Files:**
- Create: `data/pogoda-geo.json`

- [ ] **Step 1:** Собрать JSON: 11 регионов (slug = папки сайта) + ~25 городов. Каждая запись:
```json
{ "slug": "kazbegi", "type": "city", "name": "Казбеги", "name_case": "Казбеги",
  "lat": 42.66, "lon": 44.64, "region": "mtskheta-mtianeti",
  "tour_slug": "kazbegi", "neighbors": ["gudauri", "ananuri", "mtskheta"] }
```
Регионы — `type:"region"`, координаты из `api/weather.js`. Города без тура → `tour_slug:null` (линк на ближайший регион/тур).

- [ ] **Step 2 (verify):** `python3 -c "import json;d=json.load(open('data/pogoda-geo.json'));print(len(d),'точек');assert all('lat' in x and 'slug' in x for x in d)"` — ожидать ~37, без ошибок.

- [ ] **Step 3 (commit):** `git add data/pogoda-geo.json && git commit -m "data(pogoda): гео-точки кластера (регионы+города)"`

**Acceptance:** ~37 точек, у каждой slug/coords/type/region; города связаны с турами где есть.

---

## Task 2: Сбор климат-нормалей из archive

**Files:**
- Create: `scripts/fetch-climate.py`
- Create: `data/climate.json`

- [ ] **Step 1:** Скрипт читает `pogoda-geo.json`, для каждой точки тянет Open-Meteo **archive** (`archive-api.open-meteo.com/v1/archive`, daily t2m max/min/precip за ~10 лет), усредняет по месяцам → `{slug:{month:{tmax,tmin,precip_days,...}}}`. Прибрежным (Батуми/Кобулети/Уреки/Поти) — доп. темп. моря если доступна. Пауза 1с между точками (вежливость к API). Кеш: если точка уже в climate.json — пропускать (resume).

- [ ] **Step 2 (verify):** `python3 scripts/fetch-climate.py` затем `python3 -c "import json;d=json.load(open('data/climate.json'));print(len(d),'точек');print(d['kazbegi']['1'])"` — январь Казбеги должен показать минусовые t (проверка правдоподобия).

- [ ] **Step 3 (commit):** `git add scripts/fetch-climate.py data/climate.json && git commit -m "data(pogoda): климат-нормали по месяцам из Open-Meteo archive"`

**Acceptance:** climate.json покрывает все точки, 12 месяцев, цифры правдоподобны (Казбеги зимой минус, Батуми лето +28).

---

## Task 3: Расширить live-эндпоинт городами

**Files:**
- Modify: `api/weather.js`

- [ ] **Step 1:** Заменить хардкод-словарь REGIONS на полный набор из geo.json (регионы + города). Держать координаты синхронно с geo.json (одни значения).

- [ ] **Step 2 (verify):** локально `node -e` прогнать парсинг на ответе Open-Meteo для нового города (напр. gudauri) — как проверяли Батуми. Ожидать current+daily.

- [ ] **Step 3 (commit):** `git add api/weather.js && git commit -m "feat(weather): все города кластера в live-эндпоинте"`

**Acceptance:** `/api/weather?region={любой slug}` вернёт данные для всех ~37 точек.

---

## Task 4: Шаблон страницы + генератор

**Files:**
- Create: `scripts/gen-pogoda.py`

- [ ] **Step 1:** Шаблон страницы (краткий, не лонгрид), берёт head/nav/footer/CSS-ссылки из образца `kakheti/index.html` для единого дизайна. Блоки: H1 → live-виджет (JS fetch `/api/weather?region=slug`, WMO-код→эмодзи/текст) → климат-таблица 12 мес (статика из climate.json) → «когда ехать» + абзац гида (из geo.json поле guide_text) → CTA на тур → FAQ (schema FAQPage, 2-3 Q) → перелинковка (соседи + хаб) → schema Place/WebPage/BreadcrumbList.

- [ ] **Step 2:** Хаб-шаблон: сетка всех точек с мини live-t°, таблица «когда куда» (сезон×регион), ссылки на все страницы, сезонный обзор + CTA.

- [ ] **Step 3:** Генератор: `gen-pogoda.py [--only slug]` — из geo+climate пишет `pogoda/{slug}/index.html` и `pogoda/index.html`. hreflang ru + canonical. `?v=` на CSS/виджет-JS.

- [ ] **Step 4 (verify):** проверка шаблона — dry-run на 1 точке без записи, глазами глянуть HTML-вывод (виджет-JS, таблица заполнена, ссылки).

- [ ] **Step 5 (commit):** `git add scripts/gen-pogoda.py && git commit -m "feat(pogoda): шаблон страниц + генератор кластера"`

**Acceptance:** генератор пишет валидную страницу с виджетом, таблицей, тур-CTA, FAQ, перелинковкой.

---

## Task 5: Прототип (GATE — показать до раскатки)

**Files:**
- Generated: `pogoda/index.html`, `pogoda/kakheti/index.html`

- [ ] **Step 1:** `python3 scripts/gen-pogoda.py --only kakheti` + хаб.

- [ ] **Step 2 (verify):** `node scripts/predeploy-check.js pogoda/kakheti/index.html pogoda/index.html` — зелёный.

- [ ] **Step 3:** Локальный просмотр (vercel dev или файл) — live-виджет тянет данные, таблица реальная, ссылки живые.

- [ ] **Step 4 (GATE):** Показать Владимиру хаб + Кахетию. **Не раскатывать остальное без ок.**

**Acceptance:** прототип одобрен — дизайн/структура/качество контента подтверждены.

---

## Task 6: Тексты гида + генерация всех страниц

**Files:**
- Modify: `data/pogoda-geo.json` (поле guide_text на каждую точку)
- Generated: все `pogoda/{slug}/index.html`

- [ ] **Step 1:** Написать уникальный абзац опыта гида на каждую точку (анти-тонкий-контент; ~37 коротких абзацев). Не клонировать.

- [ ] **Step 2:** `python3 scripts/gen-pogoda.py` (все) + хаб.

- [ ] **Step 3 (verify):** `node scripts/predeploy-check.js` по выборке (5-6 разных страниц) — зелёный. Проверить: нет двух одинаковых guide_text, у каждой страницы ≥1 тур-ссылка + ≥3 входящих (link matrix).

- [ ] **Step 4 (commit):** `git add data/pogoda-geo.json pogoda/ && git commit -m "feat(pogoda): все страницы кластера (RU) с текстами гида"`

**Acceptance:** ~37 страниц сгенерированы, каждая уникальна, перелинковка mesh соблюдена (scorecard: coverage 100%, orphans 0, cannibalization 0).

---

## Task 7: Обратная перелинковка тур→погода + футер

**Files:**
- Modify: тур-страницы `tour/*/index.html`, `ekskursiya/*/index.html`
- Modify: футер (на всех/шаблонных страницах)

- [ ] **Step 1:** На каждой тур-странице — блок «🌤 Проверить погоду перед туром» → ссылка на соответствующую `/pogoda/{slug}/` (по тур↔slug из geo.json). Единый сниппет, вставить скриптом, не ломая существующий контент (образец правки — на 1 странице, глазами, потом раскатка).

- [ ] **Step 2:** В футер добавить ссылку «Погода в Грузии» → `/pogoda/` (НЕ в шапку).

- [ ] **Step 3 (verify):** `node scripts/predeploy-check.js` по 2-3 тур-страницам — зелёный; ссылки тур→погода ведут на существующие страницы (нет 404).

- [ ] **Step 4 (commit):** `git add tour/ ekskursiya/ ... && git commit -m "feat(pogoda): блок 'проверить погоду' на турах + ссылка в футере"`

**Acceptance:** каждая тур-страница ведёт на свою погоду; футер линкует хаб; ноль битых ссылок.

---

## Task 8: Sitemap + индексация

**Files:**
- Modify: `sitemap.xml` (или sitemap-туров/отдельный)

- [ ] **Step 1:** Добавить все URL `/pogoda/*` в sitemap.

- [ ] **Step 2:** `node scripts/indexnow-ping.js` по новым URL (Bing+Яндекс, без квоты).

- [ ] **Step 3:** `python3 scripts/google-indexing.py` (SA — владелец GSC) по новым URL (квота ~200/день).

- [ ] **Step 4 (verify):** ответы IndexNow 200 + Google publish ok по выборке.

- [ ] **Step 5 (commit):** `git add sitemap.xml && git commit -m "seo(pogoda): sitemap + отправка в индекс"`

**Acceptance:** все URL в sitemap, отправлены в IndexNow + Google.

---

## Task 9: Финальный predeploy + деплой (по команде)

- [ ] **Step 1:** `node scripts/predeploy-check.js` по репрезентативной выборке (хаб + регион + город + тур + футер).

- [ ] **Step 2 (GATE):** деплой **только по явной команде** (красная зона): `npx vercel deploy --prod --scope amberrajewelry-cryptos-projects`.

- [ ] **Step 3 (verify):** живьё — `/pogoda/` открывается, виджет тянет `/api/weather`, климат-таблица на месте, тур→погода работает.

**Acceptance:** кластер в проде, live-виджет работает, перелинковка целая.

---

## Self-Review (по writing-plans)

- **Spec coverage:** хаб ✓(T4,5) регионы+города ✓(T6) live+климат ✓(T2,3,4) краткий-не-тонкий ✓(T4) тур→погода ✓(T7) футер-не-шапка ✓(T7) индексация ✓(T8) RU-only ✓. Все требования спеки покрыты.
- **Placeholder scan:** guide_text — реальные абзацы в T6 (не placeholder); климат — реальные данные T2. Ок.
- **Type consistency:** slug — единый ключ через geo.json → climate.json → api/weather.js → URL. tour_slug связывает погода↔тур в обе стороны (T6, T7). Согласовано.
- **Риск тонкого контента** снят: климат-таблица (уникальные данные) + guide_text (уникальный текст) + FAQ на каждой.
