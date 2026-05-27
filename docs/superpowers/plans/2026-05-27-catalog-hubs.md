# Каталог экскурсий и туров — План реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Переделать каталог `/ekskursiya/` в Tripster-формат (фильтры, pill-теги, карточки с фото) и создать новый hub `/tury/` для многодневных туров.

**Architecture:** Скрипт-парсер собирает данные из 59 подстраниц в `data/catalog.json`. Hub-страницы рендерят карточки из JSON на клиенте. Фильтрация и pill-теги работают через vanilla JS без перезагрузки. Живой календарь запрашивает `/api/spots`.

**Tech Stack:** Статический HTML, vanilla JS, Airtable API, существующие Sakhva стили (Lora, #1A3D2E, #F59E0B)

**Spec:** `docs/superpowers/specs/2026-05-27-catalog-hubs-design.md`

---

## Файловая карта

| Действие | Файл | Назначение |
|----------|------|------------|
| Create | `scripts/parse-catalog.js` | Парсер 59 подстраниц → JSON |
| Create | `data/catalog.json` | Данные всех экскурсий/туров |
| Modify | `ekskursiya/index.html` | Hub экскурсий (Tripster-формат) |
| Create | `tury/index.html` | Hub туров (новый URL) |
| Modify | `sitemap.xml` | Добавить `/tury/` |

**НЕ трогаем:** 59 подстраниц, главную, блог, main.src.js, API, footer, geo-страницы.

---

### Task 1: Скрипт-парсер данных

**Files:**
- Create: `scripts/parse-catalog.js`
- Create: `data/catalog.json`

- [ ] **Step 1: Создать скрипт парсера**

Скрипт обходит все папки в `/ekskursiya/*/index.html`, извлекает данные из HTML и schema.org JSON-LD:

```js
// scripts/parse-catalog.js
const fs = require('fs');
const path = require('path');

const EKSKURSIYA_DIR = path.join(__dirname, '..', 'ekskursiya');

// Mapping slug → tags (auto + manual overrides)
const TAG_RULES = {
  keywords: {
    'Пешеходные': ['peshaya', 'stary-tbilisi', 'narikala', 'mtatsminda', 'abanotubani'],
    'Гастро': ['gastronomicheskiy', 'khachapuri', 'chacha', 'dinner', 'degustatsiya'],
    'Винные': ['vinniy', 'vinodelie', 'kvevri', 'kakheti', 'alazani', 'kindzmarauli'],
    'Фото': ['fotosessiya', 'photo'],
    'Ночные': ['nochnaya', 'night'],
    'Старый Тбилиси': ['stary-tbilisi', 'sovetskiy', 'abanotubani'],
    'Мастер-классы': ['master-klass', 'chacha-master', 'khachapuri-master'],
    'Для детей': ['family', 'dlya-detey'],
    'Казбеги': ['kazbegi', 'gudauri', 'truso', 'voennaya-gruzinskaya'],
    'Кахетия': ['kakheti', 'sighnaghi', 'alazani', 'kindzmarauli'],
    'Батуми': ['batumi'],
  },
  // Multi-day tours (go to /tury/ hub)
  multiDay: [
    'tur-gruziya-3-dnya', 'tur-gruziya-5-dney', 'tur-gruziya-7-dney',
    'tur-gruziya-10-dney', 'tur-gruziya-armeniya', 'tur-vsya-gruziya',
    'tur-tbilisi-kazbegi-kakheti', 'tur-tbilisi-svaneti', 'slow-travel'
  ]
};

function parseSubpage(slug) {
  const htmlPath = path.join(EKSKURSIYA_DIR, slug, 'index.html');
  if (!fs.existsSync(htmlPath)) return null;
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Extract title
  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  const title = titleMatch ? titleMatch[1].replace(/\s*\|.*$/, '').trim() : slug;

  // Extract meta description
  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]+)"/);
  const description = descMatch ? descMatch[1] : '';

  // Extract price from JSON-LD offers
  const priceMatch = html.match(/"price":\s*"(\d+)"/);
  const price = priceMatch ? parseInt(priceMatch[1]) : 0;

  // Extract currency
  const currMatch = html.match(/"priceCurrency":\s*"([^"]+)"/);
  const currency = currMatch ? currMatch[1] : 'GEL';

  // Extract duration from JSON-LD (PT14H format)
  const durMatch = html.match(/"duration":\s*"PT(\d+)H"/);
  const hours = durMatch ? parseInt(durMatch[1]) : 0;

  // Extract OG image
  const imgMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/);
  const image = imgMatch ? imgMatch[1] : '/images/og-cover.jpg';

  // Determine type: tour (multi-day) or excursion
  const isMultiDay = TAG_RULES.multiDay.includes(slug);

  // Determine days for multi-day tours
  let days = 0;
  if (isMultiDay) {
    const dayMatch = slug.match(/(\d+)-dn/);
    if (dayMatch) days = parseInt(dayMatch[1]);
    else if (slug === 'slow-travel') days = 3;
    else if (slug.includes('svaneti')) days = 2;
    else if (slug.includes('kazbegi-kakheti')) days = 2;
    else if (slug.includes('armeniya')) days = 5;
    else if (slug === 'tur-vsya-gruziya') days = 7;
  }

  // Auto-tag by slug keywords
  const tags = [];
  for (const [tag, keywords] of Object.entries(TAG_RULES.keywords)) {
    if (keywords.some(kw => slug.includes(kw) || description.toLowerCase().includes(kw))) {
      tags.push(tag);
    }
  }

  // Format: individual or group (default individual)
  const isGroup = hours >= 10 || slug.includes('gruppa');
  const format = isGroup ? 'group' : 'individual';

  // Duration display
  let durationText = '';
  if (isMultiDay && days > 0) {
    durationText = days === 1 ? '1 день' : days < 5 ? `${days} дня` : `${days} дней`;
  } else if (hours > 0) {
    durationText = `${hours}ч`;
  }

  return {
    slug,
    title,
    description: description.substring(0, 120),
    price,
    currency,
    hours,
    days,
    durationText,
    image,
    format,
    tags,
    type: isMultiDay ? 'tour' : 'excursion',
    url: `/ekskursiya/${slug}/`
  };
}

// Parse all subpages
const dirs = fs.readdirSync(EKSKURSIYA_DIR)
  .filter(f => f !== 'index.html' && fs.statSync(path.join(EKSKURSIYA_DIR, f)).isDirectory());

const catalog = dirs.map(parseSubpage).filter(Boolean);

const excursions = catalog.filter(t => t.type === 'excursion');
const tours = catalog.filter(t => t.type === 'tour');

const result = { excursions, tours, generated: new Date().toISOString() };

const outPath = path.join(__dirname, '..', 'data', 'catalog.json');
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(result, null, 2));

console.log(`Parsed: ${excursions.length} excursions, ${tours.length} tours`);
console.log(`Output: ${outPath}`);
```

- [ ] **Step 2: Создать папку data/ и запустить парсер**

```bash
mkdir -p data
node scripts/parse-catalog.js
```

Expected: `Parsed: ~51 excursions, ~8 tours`

- [ ] **Step 3: Проверить catalog.json**

Открыть `data/catalog.json`, убедиться что:
- У каждой записи есть title, price, image, url
- Теги назначены корректно (винные туры помечены "Винные" и т.д.)
- Многодневные туры в секции `tours`, однодневные в `excursions`
- Нет пустых записей

Ручная коррекция тегов при необходимости.

- [ ] **Step 4: Коммит**

```bash
git add scripts/parse-catalog.js data/catalog.json
git commit -m "feat: скрипт-парсер каталога → data/catalog.json (51 экскурсий, 8 туров)"
```

---

### Task 2: Hub "Экскурсии" — переделка `/ekskursiya/index.html`

**Files:**
- Backup: `ekskursiya/index.html` → `ekskursiya/index.html.bak`
- Modify: `ekskursiya/index.html`

**Принцип:** Сохраняем head (meta, schema, analytics) — меняем только body content (секция hero + каталог карточек). Nav и footer НЕ трогаем.

- [ ] **Step 1: Бэкап текущего файла**

```bash
cp ekskursiya/index.html ekskursiya/index.html.bak
```

- [ ] **Step 2: Обновить schema JSON-LD**

В существующем `<script type="application/ld+json">`:
- BreadcrumbList — уже есть, оставить
- ItemList — обновить `numberOfItems` на актуальное число экскурсий
- CollectionPage — оставить

- [ ] **Step 3: Заменить body content**

Заменить секцию hero (строки 465-470) и каталог карточек (строки 472-720) на новый Tripster-формат:

1. Hero: breadcrumbs + H1 + подзаголовок (белый фон, как в mockup)
2. Фильтры: 4 dropdown (Даты, Формат, Откуда едете, Валюта)
3. Pill-теги: тематические + географические
4. Сетка карточек: рендерится из `data/catalog.json` через JS

Карточки загружаются через `fetch('/data/catalog.json')` и рендерятся в DOM.

**Ключевые элементы HTML:**

```html
<!-- Hero -->
<section class="catalog-hero">
  <nav class="breadcrumbs">
    <a href="/">Главная</a> <span>›</span> Экскурсии
  </nav>
  <h1>Экскурсии в Тбилиси и Грузии</h1>
  <p class="catalog-subtitle">Авторские экскурсии на русском языке. Цены от ₾94</p>
</section>

<!-- Filters -->
<div class="catalog-filters">
  <div class="filter-wrap" id="filter-dates">...</div>
  <div class="filter-wrap" id="filter-format">...</div>
  <div class="filter-wrap" id="filter-from">...</div>
  <div class="filter-wrap" id="filter-currency">...</div>
</div>

<!-- Pill tags -->
<div class="catalog-pills" id="pills"></div>

<!-- Cards grid -->
<div class="catalog-grid" id="catalog-grid"></div>
```

CSS — inline в `<style>` в head (как на текущем сайте).
JS — inline `<script>` перед `</body>`:
- fetch catalog.json
- render cards
- pill-tag filtering
- currency switching
- dropdown "Откуда едете" → redirect to geo-pages
- datepicker → fetch /api/spots

- [ ] **Step 4: Predeploy check**

```bash
node scripts/predeploy-check.js ekskursiya/index.html
```

Expected: 0 ошибок

- [ ] **Step 5: Визуальная проверка**

Открыть в браузере `ekskursiya/index.html`, проверить:
- Breadcrumbs отображаются
- Pill-теги кликабельны, фильтруют карточки
- Карточки с фото, ценой, рейтингом
- Мобильная версия (сетка 1 колонка)
- Dropdown фильтры работают
- "Откуда едете" редиректит на geo-страницы

- [ ] **Step 6: Коммит**

```bash
git add ekskursiya/index.html
git commit -m "feat: hub Экскурсии — Tripster-формат (фильтры, pill-теги, карточки)"
```

---

### Task 3: Hub "Туры" — новый `/tury/index.html`

**Files:**
- Create: `tury/index.html`

- [ ] **Step 1: Создать tury/index.html**

Структура аналогична hub экскурсий, но:
- H1: "Туры по Грузии"
- Подзаголовок: "Многодневные авторские туры от 2 дней"
- Pill-теги: `[Все] [3 дня] [5 дней] [7 дней] [10 дней] [Грузия+Армения] [Вся Грузия]`
- Карточки рендерятся из `catalog.json` секция `tours`
- Meta title, description, canonical, OG — уникальные
- Schema: CollectionPage + BreadcrumbList + ItemList
- Nav, footer, analytics — скопировать из `/ekskursiya/index.html`

- [ ] **Step 2: Predeploy check**

```bash
node scripts/predeploy-check.js tury/index.html
```

- [ ] **Step 3: Визуальная проверка**

Открыть `tury/index.html`, проверить все элементы.

- [ ] **Step 4: Коммит**

```bash
git add tury/index.html
git commit -m "feat: hub Туры /tury/ — каталог многодневных (pill-теги по дням)"
```

---

### Task 4: Обновить sitemap.xml

**Files:**
- Modify: `sitemap.xml`

- [ ] **Step 1: Добавить /tury/ в sitemap**

Добавить запись:
```xml
<url>
  <loc>https://sakhva-travel.com/tury/</loc>
  <lastmod>2026-05-27</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

- [ ] **Step 2: Проверить что все 238 существующих URL на месте**

```bash
grep -c "<loc>" sitemap.xml
```

Expected: 239 (238 + 1 новый)

- [ ] **Step 3: Коммит**

```bash
git add sitemap.xml
git commit -m "feat: добавить /tury/ в sitemap.xml"
```

---

### Task 5: Финальная проверка и деплой

- [ ] **Step 1: Predeploy check всех изменённых файлов**

```bash
node scripts/predeploy-check.js ekskursiya/index.html
node scripts/predeploy-check.js tury/index.html
node scripts/predeploy-check.js index.html
```

Все должны быть без ошибок. index.html проверяем что не сломали.

- [ ] **Step 2: Проверить что главная НЕ изменена**

```bash
git diff index.html
```

Expected: пустой diff (ничего не тронуто)

- [ ] **Step 3: Проверить что подстраницы НЕ изменены**

```bash
git diff ekskursiya/ekskursiya-kazbegi-iz-tbilisi/
```

Expected: пустой diff

- [ ] **Step 4: Полный список изменений**

```bash
git status
git diff --stat HEAD~4
```

Должны быть только:
- `scripts/parse-catalog.js` (new)
- `data/catalog.json` (new)
- `ekskursiya/index.html` (modified)
- `tury/index.html` (new)
- `sitemap.xml` (modified)

- [ ] **Step 5: Деплой**

```bash
cd /Users/vladimir/sakhva-travel && npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
```

- [ ] **Step 6: Проверить прод**

Открыть:
- https://sakhva-travel.com/ekskursiya/ — hub экскурсий работает
- https://sakhva-travel.com/tury/ — hub туров работает
- https://sakhva-travel.com/ — главная не сломана
- https://sakhva-travel.com/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ — подстраница работает

- [ ] **Step 7: Удалить бэкап**

```bash
rm ekskursiya/index.html.bak
```
