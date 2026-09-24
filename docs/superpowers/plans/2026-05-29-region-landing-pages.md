# 10 Regional SEO Landing Pages — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 10 SEO landing pages for Georgian regions that capture informational traffic and funnel visitors to commercial tour pages.

**Architecture:** Static HTML pages in `/regionName/index.html`, same design system as existing tour pages (Lora font, #1A3D2E brand color, #D4845A CTA). Each page ~1500 words unique content. Homepage `#regions` section updated with clickable links + SVG map links.

**Tech Stack:** Static HTML, inline CSS (matching tour pages), JSON-LD schema (FAQPage + BreadcrumbList), Vercel deploy.

---

## File Structure

### New files (10 pages):
- `kakheti/index.html` — Кахетия
- `mtskheta-mtianeti/index.html` — Мцхета-Мтианети
- `samtskhe-javakheti/index.html` — Самцхе-Джавахети
- `shida-kartli/index.html` — Шида Картли
- `adjara/index.html` — Аджария
- `imereti/index.html` — Имеретия
- `kvemo-kartli/index.html` — Квемо Картли
- `racha/index.html` — Рача
- `samegrelo/index.html` — Самегрело
- `guria/index.html` — Гурия

### Modified files:
- `index.html` — make #regions cards clickable + SVG map links
- `sitemap.xml` — add 10 new URLs
- `vercel.json` — add trailing slash redirects if needed

### Region images (existing, from carousel):
- kakheti: `/images/kakheti-tour-600.webp`
- mtskheta: `/images/kazbegi-tour-600.webp`
- samtskhe: `/images/vardzia-tour-600.webp`
- shida: `/images/uplistsikhe-tour-600.webp`
- adjara: `/images/batumi-tour-600.webp`
- imereti: `/images/kutaisi-tour-600.webp`
- kvemo: `/images/david-gareji-tour-600.webp`
- racha: `/images/gomis-mta-tour-600.webp`
- samegrelo: `/images/svaneti-tour-600.webp`
- guria: `/images/leto-batumi-tour-600.webp`

### Tour pages to link FROM each region:
- kakheti → degustatsiya-vina-kakheti, ekskursiya-sighnaghi-iz-tbilisi, ekskursiya-telavi-iz-tbilisi
- mtskheta → ekskursiya-kazbegi-iz-tbilisi, ekskursiya-mtskheta-iz-tbilisi, ekskursiya-gudauri-iz-tbilisi, ekskursiya-ananuri-iz-tbilisi
- samtskhe → ekskursiya-borjomi-iz-tbilisi, ekskursiya-vardzia
- shida → ekskursiya-gori-iz-tbilisi, ekskursiya-uplistsikhe-iz-tbilisi
- adjara → tur-batumi-iz-tbilisi
- imereti → tur-kutaisi-iz-tbilisi
- kvemo → ekskursiya-david-gareji
- racha → tur-gruziya-7-dney (closest multi-day)
- samegrelo → ekskursiya-zugdidi, ekskursiya-svaneti-iz-tbilisi
- guria → tur-batumi-iz-tbilisi (closest)

---

## Task 1: Create HTML template for region pages

**Files:**
- Create: `_templates/region-template.html` (working reference, not deployed)

- [ ] **Step 1: Create the base HTML template**

Build a complete HTML template with these sections:
1. Head: meta tags, OG, schema, fonts (matching tour pages)
2. Nav: identical to tour pages (burger menu, logo, links)
3. Hero: full-width image, H1, breadcrumbs, distance badges
4. Section "О регионе" (~500 words placeholder)
5. Section "Что посмотреть" with H3 sub-items (~500 words)
6. Section "Когда ехать и что взять" (~300 words)
7. Section "Наши экскурсии в [регион]" — tour cards grid
8. CTA section: WhatsApp + Telegram
9. FAQ accordion with JSON-LD FAQPage schema
10. "Другие регионы" grid — links to 9 other region pages
11. Footer: identical to tour pages
12. BreadcrumbList JSON-LD schema
13. Inline burger/closeDrawer/toggleFaq JS (same as index.html fix)
14. Cookie bar with inline functions (same as index.html fix)

Template variables to replace per page:
- `{{REGION_NAME}}` — "Кахетия"
- `{{REGION_SLUG}}` — "kakheti"
- `{{TITLE}}` — optimized title
- `{{META_DESC}}` — 150-160 chars
- `{{HERO_IMG}}` — image path
- `{{H1}}` — H1 text
- `{{DISTANCES}}` — Tbilisi/Batumi/Kutaisi hours
- `{{ABOUT_CONTENT}}` — ~500 words
- `{{PLACES_CONTENT}}` — ~500 words with H3s
- `{{PRACTICAL_CONTENT}}` — ~300 words
- `{{TOUR_CARDS}}` — 2-4 tour card HTML blocks
- `{{FAQ_ITEMS}}` — FAQ HTML + JSON-LD
- `{{OTHER_REGIONS}}` — 9 links

CSS: inline in `<style>` tag, reusing tour page styles (.section, .hero-*, .article-body, .cta-btns, etc.) plus new region-specific classes (.region-distances, .region-places-grid, .other-regions-grid).

- [ ] **Step 2: Verify template renders correctly**

Open in browser locally, check mobile responsive.

- [ ] **Step 3: Commit template**

```bash
git add _templates/region-template.html
git commit -m "feat: HTML template for regional SEO pages"
```

---

## Task 2: Research & write content for Wave 1 (Кахетия, Мцхета-Мтианети, Самцхе-Джавахети)

**Files:**
- Create: `kakheti/index.html`
- Create: `mtskheta-mtianeti/index.html`
- Create: `samtskhe-javakheti/index.html`

For each page, use Tavily Search + Tavily Extract to gather unique facts from:
- georgia.travel (official tourism site)
- wikitravel / wikivoyage
- Local blogs and travel guides

### Кахетия `/kakheti/index.html`

- [ ] **Step 1: Research Kakheti via Tavily**

Search queries:
- "Кахетия регион Грузии история виноделие"
- "Кахетия достопримечательности Алазанская долина"
- "Сигнахи город любви Грузия"
Extract: georgia.travel/regions/kakheti

- [ ] **Step 2: Write 1500 words unique content**

Title: `Кахетия — виноделие, Сигнахи и Алазанская долина | Sakhva Travel`
H1: `Кахетия — край виноделия и Алазанская долина`
Meta desc: `Кахетия — винный регион Грузии: Сигнахи, Телави, Алазанская долина, монастырь Бодбе. Как добраться из Тбилиси за 1:50. Экскурсии с гидом от ₾170.`

Sections:
- О регионе: квеври, 8000 лет виноделия, Алазани, климат
- Что посмотреть: Сигнахи, Бодбе, Телави, Алаверди, Греми, Кварели, Цинандали
- Когда ехать: сентябрь-октябрь (ртвели), весна
- Distances: Тбилиси 1:50, Батуми 7:15, Кутаиси 5:10

Tour cards: degustatsiya-vina-kakheti, ekskursiya-sighnaghi-iz-tbilisi, ekskursiya-telavi-iz-tbilisi

FAQ:
1. Как добраться в Кахетию из Тбилиси?
2. Сколько стоит экскурсия в Кахетию?
3. Когда лучше ехать в Кахетию?

- [ ] **Step 3: Create kakheti/index.html from template with content**

- [ ] **Step 4: Validate with predeploy-check**

```bash
node scripts/predeploy-check.js kakheti/index.html
```

- [ ] **Step 5: Commit**

```bash
git add kakheti/index.html
git commit -m "feat: региональная SEO-страница Кахетия (1500 слов)"
```

### Мцхета-Мтианети `/mtskheta-mtianeti/index.html`

- [ ] **Step 6: Research Mtskheta-Mtianeti**

- [ ] **Step 7: Write 1500 words**

Title: `Мцхета и Казбеги — древняя столица и горы Грузии | Sakhva Travel`
H1: `Мцхета и Казбеги — древняя столица и Большой Кавказ`
Meta desc: `Мцхета-Мтианети: Светицховели, Джвари, гора Казбек 5047м, Гудаури, Военно-Грузинская дорога. Из Тбилиси за 40 мин (Мцхета) и 2:10 (Казбеги). Экскурсии с гидом.`

Distances: Тбилиси 0:40/2:10, Батуми 7:00, Кутаиси 4:55
Tour cards: ekskursiya-kazbegi-iz-tbilisi, ekskursiya-mtskheta-iz-tbilisi, ekskursiya-gudauri-iz-tbilisi, ekskursiya-ananuri-iz-tbilisi

- [ ] **Step 8: Create mtskheta-mtianeti/index.html**
- [ ] **Step 9: Validate**
- [ ] **Step 10: Commit**

### Самцхе-Джавахети `/samtskhe-javakheti/index.html`

- [ ] **Step 11: Research Samtskhe-Javakheti**
- [ ] **Step 12: Write 1500 words**

Title: `Вардзия и Боржоми — пещерный город и целебные воды | Sakhva Travel`
H1: `Самцхе-Джавахети — Вардзия, Боржоми и средневековые крепости`
Meta desc: `Самцхе-Джавахети: пещерный город Вардзия, парк Боржоми, крепость Рабат. Из Тбилиси 3 часа. Экскурсии с русскоязычным гидом от ₾195.`

Distances: Тбилиси 3:00, Батуми 3:15, Кутаиси 2:30
Tour cards: ekskursiya-borjomi-iz-tbilisi, ekskursiya-vardzia

- [ ] **Step 13: Create samtskhe-javakheti/index.html**
- [ ] **Step 14: Validate**
- [ ] **Step 15: Commit**

---

## Task 3: Wave 2 (Шида Картли, Аджария, Имеретия)

**Files:**
- Create: `shida-kartli/index.html`
- Create: `adjara/index.html`
- Create: `imereti/index.html`

### Шида Картли `/shida-kartli/index.html`

- [ ] **Step 1: Research + Write 1500 words**

Title: `Гори и Уплисцихе — пещерный город и история Грузии | Sakhva Travel`
H1: `Шида Картли — Гори, Уплисцихе и сердце древней Грузии`
Distances: Тбилиси 1:20, Батуми 5:30, Кутаиси 2:00
Tour cards: ekskursiya-gori-iz-tbilisi, ekskursiya-uplistsikhe-iz-tbilisi

ANTI-CANNIBALIZATION: H1 uses "Шида Картли" (not "экскурсия Гори"). Content focuses on HISTORY and ARCHAEOLOGY (info intent), not tour booking (commercial intent). Tour booking CTA only in dedicated card block.

- [ ] **Step 2: Create, validate, commit**

### Аджария `/adjara/index.html`

- [ ] **Step 3: Research + Write 1500 words**

Title: `Горная Аджария — водопады, крепости и хинкали над облаками | Sakhva Travel`
H1: `Аджария — горы, субтропики и Чёрное море`
Distances: Тбилиси 5:30, Кутаиси 2:30
Tour cards: tur-batumi-iz-tbilisi

ANTI-CANNIBALIZATION: Content 70% about MOUNTAIN Adjara (Khulo, Goderdzi, Machakhela), 30% coastal overview. Word "Батуми" appears only in distances and as starting point for mountain trips. Does NOT target "батуми экскурсии" — that stays with /ekskursiya/tur-batumi-iz-tbilisi/.

- [ ] **Step 4: Create, validate, commit**

### Имеретия `/imereti/index.html`

- [ ] **Step 5: Research + Write 1500 words**

Title: `Имеретия — Кутаиси, пещера Прометея и каньон Мартвили | Sakhva Travel`
H1: `Имеретия — Кутаиси, пещеры и каньоны западной Грузии`
Distances: Тбилиси 3:40, Батуми 2:30
Tour cards: tur-kutaisi-iz-tbilisi

- [ ] **Step 6: Create, validate, commit**

---

## Task 4: Wave 3 (Квемо Картли, Рача, Самегрело, Гурия)

**Files:**
- Create: `kvemo-kartli/index.html`
- Create: `racha/index.html`
- Create: `samegrelo/index.html`
- Create: `guria/index.html`

### Квемо Картли

- [ ] **Step 1: Research + Write 1500 words**

Title: `Квемо Картли — Давид Гареджи, Болниси и древняя Грузия | Sakhva Travel`
H1: `Квемо Картли — монастырь Давид Гареджи и древний Болниси`
Distances: Тбилиси 1:10, Батуми 6:30, Кутаиси 4:30
Tour cards: ekskursiya-david-gareji

- [ ] **Step 2: Create, validate, commit**

### Рача

- [ ] **Step 3: Research + Write 1500 words**

Title: `Рача — горное вино, Амбролаури и скрытый рай Грузии | Sakhva Travel`
H1: `Рача-Лечхуми — горное вино Хванчкара и альпийские озёра`
Distances: Тбилиси 5:00, Батуми 6:00, Кутаиси 2:00
Tour cards: tur-gruziya-7-dney (closest match)

- [ ] **Step 4: Create, validate, commit**

### Самегрело

- [ ] **Step 5: Research + Write 1500 words**

Title: `Самегрело — Зугдиди, Мартвильский каньон и Колхида | Sakhva Travel`
H1: `Самегрело — дворец Дадиани, Мартвильский каньон и путь в Сванетию`
Distances: Тбилиси 5:00, Батуми 2:30, Кутаиси 1:40
Tour cards: ekskursiya-zugdidi, ekskursiya-svaneti-iz-tbilisi

- [ ] **Step 6: Create, validate, commit**

### Гурия

- [ ] **Step 7: Research + Write 1500 words**

Title: `Гурия — чайные плантации, море и нетуристическая Грузия | Sakhva Travel`
H1: `Гурия — чай, Бахмаро и самый нетуристический регион Грузии`
Distances: Тбилиси 4:30, Батуми 1:00, Кутаиси 1:30
Tour cards: tur-batumi-iz-tbilisi (closest)

- [ ] **Step 8: Create, validate, commit**

---

## Task 5: Update homepage — clickable region cards + SVG map

**Files:**
- Modify: `index.html` — lines 832-877 (region JS) + lines 671-690 (region card HTML) + SVG paths

- [ ] **Step 1: Make region card clickable**

Wrap region-card content in an `<a>` tag. Add `href` to the `show()` function output. Change card to be a link when clicked.

Add URL mapping to the R{} data object:
```javascript
kakheti:{name:"Кахетия",cities:[...],img:"...",url:"/kakheti/"},
mtskheta:{name:"Мцхета-Мтианети",cities:[...],img:"...",url:"/mtskheta-mtianeti/"},
// etc for all 10 regions
// tbilisi, abkhazia, samachablo — no url (no pages)
```

Add a "Подробнее" link below cities that updates with region URL:
```html
<a id="rg-link" href="/kakheti/" style="...">Подробнее о регионе →</a>
```

Update `show()` function to set `rg-link` href.

- [ ] **Step 2: Make SVG map paths clickable**

Change SVG path click handler from just `show()` to navigate:
```javascript
p.addEventListener('click',function(){
  locked=true;show(p.dataset.region);
  var d=R[p.dataset.region];
  if(d&&d.url) window.location.href=d.url;
});
```

Add `cursor:pointer` to SVG paths that have URLs.

- [ ] **Step 3: Validate no broken functionality**

Test carousel still works, arrows still work, hover still works. Only CLICK navigates.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: кликабельные регионы на главной (карточки + SVG карта)"
```

---

## Task 6: Update sitemap.xml

**Files:**
- Modify: `sitemap.xml`

- [ ] **Step 1: Add 10 new URLs to sitemap**

```xml
<url><loc>https://sakhva-travel.com/kakheti/</loc><lastmod>2026-05-29</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
<url><loc>https://sakhva-travel.com/mtskheta-mtianeti/</loc><lastmod>2026-05-29</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
<!-- etc for all 10 -->
```

- [ ] **Step 2: Commit**

```bash
git add sitemap.xml
git commit -m "feat: 10 региональных страниц в sitemap"
```

---

## Task 7: Deploy & verify

- [ ] **Step 1: Run predeploy-check on index.html**

```bash
node scripts/predeploy-check.js index.html
```

- [ ] **Step 2: Deploy to Vercel**

```bash
cd /Users/vladimir/sakhva-travel && npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
```

- [ ] **Step 3: Verify all 10 pages load**

Check each URL responds 200:
```bash
for slug in kakheti mtskheta-mtianeti samtskhe-javakheti shida-kartli adjara imereti kvemo-kartli racha samegrelo guria; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com/$slug/")
  echo "$slug: $code"
done
```

- [ ] **Step 4: Verify homepage region clicks work**

Use Playwright to click a region on the map and verify navigation.

- [ ] **Step 5: Submit to IndexNow**

```bash
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{"host":"sakhva-travel.com","key":"DE25F3FA51D1F1E934763682A270AF53","urlList":["https://sakhva-travel.com/kakheti/","https://sakhva-travel.com/mtskheta-mtianeti/","https://sakhva-travel.com/samtskhe-javakheti/","https://sakhva-travel.com/shida-kartli/","https://sakhva-travel.com/adjara/","https://sakhva-travel.com/imereti/","https://sakhva-travel.com/kvemo-kartli/","https://sakhva-travel.com/racha/","https://sakhva-travel.com/samegrelo/","https://sakhva-travel.com/guria/"]}'
```

---

## Anti-Cannibalization Checklist (verify after all pages created)

- [ ] No two pages share the same primary keyword in title
- [ ] All region pages use info-intent modifiers ("достопримечательности", "что посмотреть", "как добраться")
- [ ] All tour pages use commercial-intent modifiers ("экскурсия", "тур", "из Тбилиси", price)
- [ ] Region pages LINK TO tour pages (not compete with them)
- [ ] No region page contains `<a>` with text "Забронировать" or "Купить тур" — only "Подробнее" links to tour pages
