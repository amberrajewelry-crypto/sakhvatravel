# Sakhva Travel — Конверсионный буст: план реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Увеличить конверсию сайта через динамические цены, WhatsApp pre-fill, urgency-счётчик, exit-popup, сравнение с агрегаторами, страницы городов и улучшенный UI.

**Architecture:** Все фичи — фронтенд (статический HTML + vanilla JS). Данные о загрузке — из существующего api/spots.js (Airtable). Новые страницы — статический HTML по шаблону существующих тур-страниц.

**Tech Stack:** HTML, CSS (inline), vanilla JS, Airtable REST API, Vercel serverless

---

## Приоритеты (по ROI)

| # | Фича | Эффект | Время |
|---|-------|--------|-------|
| 1 | Динамическая цена на карточках по кол-ву людей | Убирает "от", +конверсия | 1.5ч |
| 2 | WhatsApp pre-filled с туром, датой, кол-вом | Ускоряет первый контакт | 30мин |
| 3 | Счётчик "осталось N мест" из Airtable | Urgency | 1ч |
| 4 | Exit-intent popup с промокодом | +3-5% от уходящих | 45мин |
| 5 | Страница "Tripster vs Sakhva Travel" | SEO + конверсия | 2ч |
| 6 | Блок "Включено / Не включено" на всех турах | Снимает вопросы | 1.5ч |
| 7 | Языковой переключатель в header (заметнее) | +15-20% EN трафик | 30мин |
| 8 | 5 лендингов городов-источников | SEO-активы | 3ч |

---

## Task 1: Динамическая цена на карточках по количеству людей

**Files:**
- Modify: `index.html` — секция tours-grid (карточки .tg), inline script с ценами
- Modify: `js/main.src.js` — добавить расчёт цен, слушатель на селектор кол-ва

### Контекст для разработчика

Сейчас карточки туров (`<div class="tg">`) показывают `.tg-price` = статический текст "от ₾77". Есть shared calculator `.tsc-ppl` с кнопками data-n="1"..data-n="6". При клике кнопка получает класс `.on`. Но карточки не реагируют на выбор.

Массив цен уже есть в `main.src.js:422` — `BK_TOURS[]` с `price_usd`, базовые per-person цены. Скидки за группу: 4 чел = -10%, 5-6 чел = -15%.

Каждая карточка `.tg` имеет `data-tour="kazbegi"` (или аналог) и `.tg-price` для отображения.

- [ ] **Step 1: Добавить data-атрибуты цен на карточки**

В `index.html` на каждую карточку `.tg` добавить `data-price-gel` и `data-price-usd`:
```html
<div class="tg" data-tour="kazbegi" data-price-gel="175" data-price-usd="67">
```

Найти все `.tg` в index.html (grep `class="tg"`) и добавить атрибуты из BK_TOURS.

- [ ] **Step 2: Написать функцию пересчёта**

В конце inline-скрипта (или в main.src.js) добавить:
```js
function updateTourPrices() {
  var n = parseInt(document.querySelector('.tsc-ppl button.on')?.dataset.n || '1');
  var curr = document.querySelector('.tsc-curr button.on')?.textContent?.trim() || '₾';
  var disc = n >= 5 ? 0.15 : n >= 4 ? 0.10 : 0;
  document.querySelectorAll('.tg[data-price-gel]').forEach(function(card) {
    var base = curr === '₾' ? +card.dataset.priceGel : +card.dataset.priceUsd;
    var total = Math.round(base * n * (1 - disc));
    var sym = curr === '₾' ? '₾' : '$';
    var label = n > 1 ? ' за ' + n + ' чел.' : ' / чел.';
    card.querySelector('.tg-price').textContent = sym + total + label;
  });
}
```

- [ ] **Step 3: Привязать к селектору количества**

Добавить слушатели на кнопки `.tsc-ppl button[data-n]`:
```js
document.querySelectorAll('.tsc-ppl button[data-n]').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.tsc-ppl button[data-n]').forEach(function(b) { b.classList.remove('on') });
    this.classList.add('on');
    updateTourPrices();
  });
});
// Также на переключатель валюты
document.querySelectorAll('.tsc-curr button').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.tsc-curr button').forEach(function(b) { b.classList.remove('on') });
    this.classList.add('on');
    updateTourPrices();
  });
});
```

- [ ] **Step 4: Убрать "от" из начальных цен**

Заменить все `.tg-price` с "от ₾77" на "₾77 / чел." (без "от").

- [ ] **Step 5: Показать скидку если выбрано 4+**

Если disc > 0, показать бейдж:
```js
var discEl = card.querySelector('.tg-disc');
if (discEl) discEl.style.display = disc > 0 ? 'inline-block' : 'none';
```
Добавить `<span class="tg-disc" style="display:none;background:#F59E0B;color:#111;font-size:10px;padding:2px 6px;border-radius:10px;margin-left:4px">-10%</span>` в каждую карточку рядом с ценой.

- [ ] **Step 6: Деплой и проверка**

```bash
node scripts/predeploy-check.js index.html
npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
```

---

## Task 2: WhatsApp pre-filled message с контекстом тура

**Files:**
- Modify: `index.html` — карточки туров, CTA-кнопки
- Modify: `ekskursiya/*/index.html` — кнопки WA на страницах туров

### Контекст

Сейчас WA-ссылки на карточках ведут на `wa.me/995511272623?text=generic`. Нужно добавить контекст: название тура + количество людей.

- [ ] **Step 1: Обновить WA-ссылки на карточках главной**

Каждая карточка `.tg` уже имеет `data-tour`. Добавить JS, который при клике на WA-кнопку формирует ссылку:
```js
document.querySelectorAll('.tg .tg-cta').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    var card = this.closest('.tg');
    var tour = card.querySelector('.tg-info h3')?.textContent || '';
    var n = document.querySelector('.tsc-ppl button.on')?.dataset.n || '1';
    var msg = encodeURIComponent('Здравствуйте! Хочу забронировать "' + tour + '" на ' + n + ' чел.');
    window.open('https://wa.me/995511272623?text=' + msg, '_blank');
    e.preventDefault();
  });
});
```

- [ ] **Step 2: Обновить WA-ссылки на страницах туров**

Python-скрипт для массового обновления:
Для каждого `ekskursiya/*/index.html` — найти `wa.me/995511272623` и обновить `?text=` на контекстное сообщение с названием тура из `<h1>`.

- [ ] **Step 3: Деплой**

---

## Task 3: Счётчик "осталось N мест на эту неделю"

**Files:**
- Modify: `index.html` — добавить блок urgency под shared calculator
- Create: `api/weekly-spots.js` — Vercel function, читает Airtable бронирования на неделю
- Modify: `js/main.src.js` — fetch и отображение

### Контекст

`api/spots.js` уже существует и читает из Airtable. Тимур ведёт макс 1-2 тура/день, 7 чел макс = ~50-70 мест/неделю минус забронированные.

- [ ] **Step 1: Создать API endpoint**

```js
// api/weekly-spots.js
const Airtable = require('airtable');
module.exports = async (req, res) => {
  const base = new Airtable({apiKey: process.env.AIRTABLE_API_KEY})
    .base(process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh');
  const now = new Date();
  const weekEnd = new Date(now);
  weekEnd.setDate(weekEnd.getDate() + 7);
  const records = await base('tbl0rlhK4KyAMk8UB').select({
    filterByFormula: `AND(IS_AFTER({Дата тура}, '${now.toISOString().split('T')[0]}'), IS_BEFORE({Дата тура}, '${weekEnd.toISOString().split('T')[0]}'), {Статус} != 'Отменён')`,
    fields: ['Guests']
  }).all();
  const booked = records.reduce((sum, r) => sum + (r.get('Guests') || 1), 0);
  const maxWeekly = 70; // ~10 туров × 7 мест
  const remaining = Math.max(0, maxWeekly - booked);
  res.json({ remaining, booked });
};
```

- [ ] **Step 2: Добавить UI-блок urgency**

Под `.tsc-row` в index.html:
```html
<div id="spots-urgency" style="display:none;text-align:center;margin-top:12px">
  <span style="background:#FEF3C7;color:#92400E;font-size:13px;font-weight:700;padding:6px 16px;border-radius:8px;display:inline-flex;align-items:center;gap:6px">
    🔥 Осталось <span id="spots-count">—</span> мест на эту неделю
  </span>
</div>
```

- [ ] **Step 3: Fetch и отображение**

В inline-скрипте или main.src.js:
```js
fetch('/api/weekly-spots').then(r=>r.json()).then(d=>{
  if(d.remaining<50){
    document.getElementById('spots-count').textContent=d.remaining;
    document.getElementById('spots-urgency').style.display='block';
  }
}).catch(()=>{});
```

- [ ] **Step 4: Деплой и проверка**

---

## Task 4: Exit-intent popup с промокодом

**Files:**
- Modify: `index.html` — добавить popup HTML + CSS + JS

### Контекст

Промокод СУДЬБА5 уже существует в системе (карта фортуны). Используем SAKHVA5 для exit-intent.

- [ ] **Step 1: Добавить HTML popup**

Перед `</body>`:
```html
<div id="exit-popup" style="display:none;position:fixed;inset:0;z-index:99998;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);align-items:center;justify-content:center">
  <div style="background:#fff;border-radius:20px;padding:36px 32px;max-width:420px;width:90%;text-align:center;position:relative">
    <button onclick="document.getElementById('exit-popup').style.display='none'" style="position:absolute;top:12px;right:16px;font-size:24px;color:#9CA3AF;cursor:pointer;background:none;border:none">×</button>
    <div style="font-size:36px;margin-bottom:12px">🎁</div>
    <h3 style="font-size:22px;font-weight:700;color:#111;margin-bottom:8px" data-ru="Подождите! У нас подарок">Подождите! У нас подарок</h3>
    <p style="color:#6B7280;font-size:15px;margin-bottom:16px" data-ru="Промокод на скидку 5% на любой тур">Промокод на скидку 5% на любой тур</p>
    <div style="background:#F0FDF4;border:2px dashed #16A34A;border-radius:12px;padding:14px;font-size:24px;font-weight:800;color:#16A34A;letter-spacing:.1em;margin-bottom:16px">SAKHVA5</div>
    <a href="https://wa.me/995511272623?text=Здравствуйте!+Хочу+забронировать+тур+с+промокодом+SAKHVA5" target="_blank" rel="noopener" class="btn-wa" style="padding:14px 32px;font-size:14px;width:100%;justify-content:center" data-ru="Забронировать со скидкой">Забронировать со скидкой</a>
  </div>
</div>
```

- [ ] **Step 2: Добавить exit-intent JS**

```js
(function(){
  var shown=false;
  document.addEventListener('mouseout',function(e){
    if(shown||e.clientY>50||localStorage.getItem('exit_popup_closed'))return;
    if(localStorage.getItem('cookies_v4')!=='1')return; // не показываем если cookie bar открыт
    shown=true;
    document.getElementById('exit-popup').style.display='flex';
    localStorage.setItem('exit_popup_closed','1');
  });
})();
```

- [ ] **Step 3: Деплой**

---

## Task 5: Страница "Tripster vs Sakhva Travel"

**Files:**
- Create: `tripster-vs-sakhva/index.html` — боевая сравнительная страница
- Modify: `sitemap.xml` — добавить URL

### Контекст

Целевые запросы: "tripster отзывы", "sputnik8 или частный гид", "tripster тбилиси". Страница должна быть SEO-оптимизирована И конверсионной.

- [ ] **Step 1: Создать страницу**

Взять шаблон из `gid-v-tbilisi-na-russkom/index.html` (структура head, nav, footer). Контент:

**H1:** Частный гид vs Tripster / Sputnik8 — сравнение 2026

**Структура:**
1. Hero: "Почему 87% наших клиентов раньше бронировали на агрегаторах"
2. Таблица сравнения (3 колонки: Tripster | Sputnik8 | Sakhva Travel)
   - Цена Казбеги: ₾200-350 | ₾180-300 | ₾175
   - Комиссия: 20-30% | 15-25% | 0%
   - Гид: случайный | случайный | Тимур лично
   - Группа: до 15-20 | до 10-15 | до 7
   - Отмена: штраф | штраф | бесплатно
   - Оплата: предоплата | предоплата | в день тура
   - Маршрут: стандартный | стандартный | индивидуальный
3. Блок отзывов (переиспользовать с главной)
4. "Как это работает" — 3 шага
5. FAQ: "Можно ли доверять частному гиду", "Почему дешевле без агрегатора"
6. CTA с формой бронирования + WhatsApp

**Schema:** FAQPage + TouristTrip + Review

- [ ] **Step 2: Добавить в sitemap**

- [ ] **Step 3: Добавить внутренние ссылки** с `/blog/` и `/gid-v-tbilisi-na-russkom/`

- [ ] **Step 4: Деплой**

---

## Task 6: Блок "Включено / Не включено" на всех турах

**Files:**
- Modify: `ekskursiya/*/index.html` — 57+ страниц

### Контекст

Казбеги уже имеет `includes-box`. Нужно стандартизировать формат и добавить на все туры которые его не имеют.

- [ ] **Step 1: Создать стандартный HTML-шаблон**

```html
<div class="incl-excl">
  <div class="incl-col incl-yes">
    <h4>✓ Включено</h4>
    <ul>
      <li>Комфортный авто с кондиционером</li>
      <li>Русскоязычный гид Тимур</li>
      <li>Фото-стопы по маршруту</li>
    </ul>
  </div>
  <div class="incl-col incl-no">
    <h4>✕ Не включено</h4>
    <ul>
      <li>Питание (обед ~₾15-25)</li>
      <li>Входные билеты (указаны в маршруте)</li>
    </ul>
  </div>
</div>
```

- [ ] **Step 2: Python-скрипт для массовой вставки**

Для каждого тура — уникальный набор включённого/не включённого (зависит от маршрута). Подготовить JSON с данными для каждого тура и вставить скриптом.

- [ ] **Step 3: Добавить CSS в inline-стили тур-страниц**

- [ ] **Step 4: Деплой**

---

## Task 7: Языковой переключатель заметнее

**Files:**
- Modify: `index.html` — nav секция

### Контекст

Переключатель `.lang-sw` уже есть в nav. Нужно сделать его заметнее — добавить флажки и увеличить.

- [ ] **Step 1: Обновить HTML переключателя**

Заменить текстовые "RU | EN" на:
```html
<div class="lang-sw">
  <button class="lang-btn on" id="btnRu" onclick="setLang('ru')">🇷🇺 RU</button>
  <span class="lang-sep">|</span>
  <button class="lang-btn" id="btnEn" onclick="setLang('en')">🇬🇧 EN</button>
</div>
```

- [ ] **Step 2: Обновить стили** — увеличить padding, сделать фон-подложку

- [ ] **Step 3: Деплой**

---

## Task 8: 5 лендингов городов-источников

**Files:**
- Create: `iz-moskvy/index.html`
- Create: `iz-spb/index.html`
- Create: `iz-minska/index.html`
- Create: `iz-almaty/index.html`
- Create: `iz-tashkenta/index.html`
- Modify: `sitemap.xml`

### Контекст

Шаблон — аналог категорийных страниц (`ekskursii-po-gruzii/`). Каждая страница: перелёт, виза, что взять, + блок туров.

- [ ] **Step 1: Создать шаблон**

Базовый шаблон с секциями:
1. Hero с городом
2. "Как добраться" (прямые рейсы, цена, время)
3. "Виза и документы"
4. "Что взять с собой"
5. Блок туров (переиспользовать карточки)
6. CTA

- [ ] **Step 2: Наполнить уникальным контентом** для каждого города

- [ ] **Step 3: Добавить в sitemap и внутреннюю перелинковку**

- [ ] **Step 4: Деплой**

---

## Порядок исполнения

**День 1 (сегодня):** Task 1 + Task 2 — максимальный ROI за минимум времени
**День 2:** Task 3 + Task 4 — urgency + exit-intent
**День 3:** Task 5 — страница сравнения
**День 4:** Task 6 + Task 7 — включено/не включено + язык
**День 5:** Task 8 — лендинги городов
