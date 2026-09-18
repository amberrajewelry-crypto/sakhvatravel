# Sakhva Travel — визуальный аудит (2026-09-18)

Метод: Playwright chromium headless, viewports mobile 390x844 (iPhone UA) и desktop 1440x900.
Скриншоты: `sakhva-travel.com-audit/2026-09-18/screenshots/*.png`
Сырые метрики: DOM-эвалюация (scrollWidth, getBoundingClientRect, computed font-size) на каждой странице.

## Итоговый балл: 82/100

## По страницам

### / (главная)
- H1 «Tours & Excursions in Georgia» виден без скролла (mobile+desktop) ✔
- CTA above-the-fold: mobile 4, desktop 7 (из 39 всего)
- Consent/cookie-баннер обнаружен (эвристика по тексту «персональных данных») — не блокирует контент
- FAB `.sc-fab` (чат) фиксирован bottom-right, не перекрывает основной CTA
- «Оставить отзыв в Google» рендерится: «★ Leave a Google review» видима на mobile и desktop
- smallTargets (<44px): mobile 92, desktop 138 — в основном соц-иконки/навигация, не основной CTA
- Горизонтальный скролл: нет. Картинки без width/height: 0/121
- Скриншоты: `home__mobile.png`, `home__desktop.png`

### /en/
- Идентично главной (общий шаблон), нагрузка быстрее (кэш): 617мс mobile / 256мс desktop
- Скриншоты: `en__mobile.png`, `en__desktop.png`

### /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/
- H1, цена «от ₾175», зелёная CTA «Забронировать от 175 лари» — всё видно без скролла на mobile ✔ (сильная страница тура)
- **Горизонтальный скролл: True на mobile при снимке в момент подгрузки live-погоды** («Сейчас в Степанцминде: +14°, пасмурно · завтра 11...» — строка переносится с обрезкой «завтра 11...» / «14°, дождь» на след. строке). При повторном замере через 1500мс скролла нет (390=390) — баг переходный, не постоянный
- CTA above fold: mobile 2, desktop 5
- Скриншоты: `ekskursiya_ekskursiya-kazbegi-iz-tbilisi__mobile.png`, `..._desktop.png`

### /blog/gruzinskie-frazy/
- H1 виден, above-fold CTA: mobile 1, desktop 6
- Блок «Тур по теме» (`.also-tour`): ширина 358px (mobile) / 696px (desktop), не переполняет родителя, top≈740px mobile / 624px desktop — расположен ниже статьи, вёрстка корректна
- «Оставить отзыв в Google» кнопка НЕ найдена (блог-шаблон не включает блок отзывов) — ожидаемо по структуре страницы, не дефект
- Скриншоты: `blog_gruzinskie-frazy__mobile.png`, `..._desktop.png`

### /tury-v-gruziyu/ (категорийная)
- **CTA above the fold на mobile: 0** — хиро содержит только H1/бейджи/breadcrumb, ближайший интерактивный блок (карточка гида) начинается ниже сгиба. На desktop above-fold CTA: 4
- smallTargets высокие (101 mobile / 130 desktop) — карточки направлений плотные
- Скриншоты: `tury-v-gruziyu__mobile.png`, `..._desktop.png`

### /ekskursiya/transfer-tbilisi-batumi/
- H1 с ценой «от ₾280» виден без скролла, CTA above fold: mobile 1, desktop 2
- Горизонтального скролла нет, small targets умеренно (16/24)
- Скриншоты: `ekskursiya_transfer-tbilisi-batumi__mobile.png`, `..._desktop.png`

## Сводные метрики load-to-content (page load event, мс)
mobile: / 1173, /en/ 617, kazbegi 575, фразы 445, туры 761, трансфер 691
desktop: / 1012, /en/ 256, kazbegi 475, фразы 233, туры 326, трансфер 192

## Severity buckets
- Critical: 0
- High: 1 — переходный горизонтальный скролл на /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ mobile из-за длинной строки live-погоды, обрезающейся на 2 строки
- Medium: 2 — (1) 0 CTA above the fold на /tury-v-gruziyu/ mobile; (2) высокая плотность tap-таргетов <44px на карточных страницах (главная, /tury-v-gruziyu/) — риск промахов пальцем
- Low: 3 — cookie-consent баннер только на главной (не на подстраницах, не мешает); отсутствие кнопки отзывов Google на блог-шаблоне (по дизайну, не баг); мелкий текст <12px — единичные случаи (2 узла) на главной, не системная проблема
