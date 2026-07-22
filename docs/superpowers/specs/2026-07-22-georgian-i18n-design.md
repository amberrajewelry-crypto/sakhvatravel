# Spec: Грузинская версия sakhva-travel.com (/ge/, hreflang=ka)

_Дата: 2026-07-22 · Ветка: feature/georgian-lang · Статус: DRAFT (ожидает утверждения)_

## Objective

Добавить третий язык — грузинский — на статический сайт турагентства sakhva-travel.com
(сейчас RU + EN). Грузинская версия живёт в папке `/ge/` как зеркало EN-версии,
с 3-язычным переключателем RU | EN | GE, корректным hreflang (`ka`), без поломок вёрстки,
SEO и живого RU/EN-сайта.

**Точный объём:** EN = 237 стр (68 туров + 104 блог + 28 гео + 11 регионов + 9 стран +
16 одиночных + главная). GE-зеркало = **234** (237 минус 3 аномалии: booking/policy/links —
noindex/без переключателя, не зеркалим). Двойники под реципрокность: 234 RU + 234 EN.

**Пользователь:** грузиноязычный посетитель (местный рынок + SEO-полнота + имидж).
**Успех:** `/ge/` полностью индексируема, hreflang-квадры реципрокны, вязь Mkhedruli
рендерится корректно на всех брейкпоинтах, переключатель работает во все стороны,
RU/EN-версии не деградировали.

**ВАЖНО (стратегическая оговорка):** туры покупают приезжие рус/англоговорящие, не местные.
ROI грузинской версии — в SEO/полноте/имидже, не в прямой конверсии. Объём (237 стр,
~475K слов) утверждён владельцем осознанно.

## Tech Stack

- Статический HTML (без сборщика; файлы = роуты).
- Хостинг Vercel; `cleanUrls:true`, `trailingSlash:true`.
- Vercel Edge Middleware (`middleware.js`) — server-side язык-редирект по Accept-Language/cookie.
- Vanilla JS (`main.js`, общий на весь сайт) — динамика: карточки туров, квиз, календарь, отзывы (fetch `/api/reviews`).
- Serverless `api/*` (отзывы, чат, бронь, ваучеры, telegram).
- Шрифты локальные woff2 (Lora + Raleway; **не покрывают грузинский** → добавляем Noto Sans Georgian).
- Sitemap — 4 статических XML с `xhtml:link alternate`.

## Commands

```
Предеплой-проверка:   node scripts/predeploy-check.js <files...>
Трансформер каркаса:  node scripts/gen-ge.js <en-file> → ge-file   (создаём в фазе 3)
Деплой прод:          npx vercel deploy --prod --scope amberrajewelry-cryptos-projects
Проверка hreflang:    curl -sL https://sakhva-travel.com/ge/<path>/ | grep -E 'hreflang|canonical|og:locale'
Индексация:           существующие скрипты Google Indexing / IndexNow / Yandex
```
Сборки нет. «Build» = запуск трансформера + перевод субагентами + предеплой-проверка.

## Project Structure

```
/ge/                        → грузинское зеркало (НОВОЕ, аналог /en/)
  index.html                  главная
  ekskursiya/<slug>/          68 туров (слаги как в EN/RU)
  blog/<slug>/                104 статьи
  tours-from-<city>/          28 гео-лендингов
  <region>/ <country>/        11 регионов + 9 стран
  <single>/                   13 одиночных (16 минус booking/policy/links)
/fonts/noto-sans-georgian-{400,600,700}.woff2   → НОВЫЕ, subset Mkhedruli
/css/ или инлайн-<style>     → ka-CSS блок (font-family + оверрайды nowrap/padding)
scripts/gen-ge.js            → НОВЫЙ трансформер EN→GE-каркас
scripts/predeploy-check.js   → +GE-проверки
middleware.js                → +ветка ka→/ge/
main.js                      → +ветка ge (redirect/setLang guard, EN-фолбэк динамики)
api/reviews.js               → +REVIEWS_GE, ветка isGe, Vary-заголовок
sitemap-*.xml                → +/ge/ url + xhtml:link ka в RU/EN записи
docs/superpowers/specs/      → эта спека
```

## Code Style

Перевод меняет **только текст-ноды**; структуру/скрипты/ключи schema/классы не трогаем.
Трансформер детерминированно правит `<head>`. Пример корректного результата (главная):

```html
<html lang="ka">
<link rel="canonical" href="https://sakhva-travel.com/ge/">           <!-- НЕ /en/ -->
<meta property="og:locale" content="ka_GE">
<meta property="og:locale:alternate" content="ru_RU">
<meta property="og:locale:alternate" content="en_US">
<link rel="alternate" hreflang="ru" href="https://sakhva-travel.com/">
<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/">
<link rel="alternate" hreflang="ka" href="https://sakhva-travel.com/ge/">
<link rel="alternate" hreflang="x-default" href="https://sakhva-travel.com/">
<!-- preload грузинского шрифта ТОЛЬКО в /ge/-файлах -->
<link rel="preload" href="/fonts/noto-sans-georgian-400.woff2" as="font" type="font/woff2" crossorigin>
```

JSON-LD: `inLanguage:"ka"`, `@id`/`url`/breadcrumb-URL `/en/→/ge/`, `knowsLanguage` +`ka`,
`priceCurrency` GEL без изменений, `author.name`/`ratingValue` без изменений, `reviewBody` перевести.

CSS-оверрайд (глобальный `@font-face` с `unicode-range` безопасен — не качается без грузинских глифов):
```css
@font-face{font-family:'Noto Sans Georgian';src:url(/fonts/noto-sans-georgian-400.woff2) format('woff2');
  unicode-range:U+10A0-10FF;font-weight:400;font-display:swap}
html[lang="ka"] body,html[lang="ka"] h1,html[lang="ka"] .nav-links a,html[lang="ka"] .btn-primary{
  font-family:'Noto Sans Georgian','Lora',serif}
html[lang="ka"] .nav-links a,html[lang="ka"] .btn-primary,html[lang="ka"] .btn-outline-hero{
  white-space:normal}   /* грузинский на 15-20% длиннее — снимаем nowrap */
```

## Testing Strategy

- **predeploy-check.js + GE-проверки:** на каждом `/ge/`-файле: `lang="ka"`, `hreflang="ka"`,
  `canonical` указывает на **self /ge/**, `og:locale=ka_GE`, наличие грузинского шрифта,
  отсутствие непереведённого EN-прозы в body, валидный JSON-LD с `ka`.
- **seo-hreflang (скилл):** реципрокность квадр RU↔EN↔GE (двусторонние ссылки на всех трёх + в sitemap).
- **chrome-devtools MCP:** рендер вязи + отсутствие обрезки на 375 / 768 / 1920 px; переключатель RU↔EN↔GE во все стороны.
- **check-translations (скилл):** паритет — нет пропущенного/непереведённого текста.
- **Качество вязи без носителя (3 слоя):**
  1. *Грунтинг:* корпус живого грузинского с реальных `.ge`-турсайтов (+ georgia.travel) → native-терминология и регистр как эталон перевода.
  2. *Глоссарий:* замкнутый словарь повторяющихся терминов (тур/гид/бронь/Тбилиси=თბილისი/₾) → единообразие на 234 стр.
  3. *Состязательный цикл:* переводчик-субагент → независимый критик (беглость/грамматика/кальки, 1-5, флаг «машинно») → обратный перевод KA→RU на смысл → правка до прохождения. Приближение к native-ревью алгоритмически (не заменяет носителя на 100%, но снимает грубые кальки/галлюцинации).
- **Регресс-тест общих файлов:** после правок `main.js`/`reviews.js`/`middleware.js` — проверить, что RU и EN версии НЕ изменили поведение (карточки, квиз, отзывы, редиректы).

## Boundaries

**Always (автономно):**
- Переводить только текст-ноды; canonical/hreflang/og/schema править трансформером.
- Прогонять predeploy-check перед деплоем; curl-проверка на проде после.
- Коммит после каждого атомарного шага в ветке `feature/georgian-lang`.
- EN-фолбэк для динамики `main.js` на `/ge/`.

**Only by explicit command (только по явной команде владельца):**
- **Деплой на прод** (`vercel deploy --prod`) — НИКОГДА автономно.
- **Отправка индексации** (Google Indexing / IndexNow / Yandex) — НИКОГДА автономно.
- Вся работа Ф0-Ф6 (изоляция, ассеты, общие файлы, трансформер, перевод, двойники, локальная QA) идёт до момента деплоя; деплой ждёт команды.

**Ask first (спросить владельца):**
- Любое изменение RU/EN-контента сверх добавления GE-кнопки+hreflang.
- Расширение объёма за пределы 234 (например GE для booking/policy/links).
- Бэкенд-паритет фазы 2 (chat/voucher/telegram на грузинском) — старт.
- Изменение x-default или canonical-стратегии.

**Never:**
- Пушить в main (только ветка/PR).
- Ломать реципрокность hreflang (нереципрокный = Google игнорирует).
- Копировать EN→GE без переписи canonical (де-индексация `/ge/`).
- Ставить noindex/убирать из sitemap без команды.
- Деплоить общий `main.js` без пройденного регресс-теста RU/EN.

## Success Criteria

**Гейт пилота (6 страниц: `/ge/`, тур, блог, гео, регион, about) — GO/NO-GO для масштаба:**
1. Все 6 отдаются 200, `lang="ka"`, canonical→self `/ge/`.
2. hreflang-квадры реципрокны (curl RU/EN/GE + sitemap) — `seo-hreflang` зелёный.
3. Вязь Mkhedruli рендерится, 0 обрезки на 375/768/1920 (chrome-devtools).
4. Переключатель RU↔EN↔GE работает во все стороны (cookie + редирект).
5. Отзывы на `/ge/` приходят грузинские (`reviews.js` Vary+GE), не RU/EN.
6. `middleware.js`: Accept-Language `ka` → `/ge/`; RU/EN редиректы не изменились.
7. RU/EN динамика/вёрстка не деградировали (регресс-тест).
8. predeploy-check зелёный, обратный перевод без критичных расхождений.

**Полный релиз:** все 237 `/ge/` + 237 RU + 237 EN двойников с реципрокным hreflang;
sitemap обновлён; 0 непереведённого; индексация отправлена.

## Полный план (фазы)

- **Ф0. Изоляция:** закоммитить/синхронизировать 478 текущих файлов (уже на проде) одним коммитом «sync deployed state»; создать ветку. Гейт: `git status` чист.
- **Ф1. Ассеты:** Noto Sans Georgian → `/fonts/`; ka-CSS блок. Гейт: рендер в изоляции.
- **Ф2. Общие файлы:** `main.js` (ветка ge в redirect-блоке — иначе `setLang('ge')` обнулит текст на RU/EN; EN-фолбэк динамики; `lang=ge` в fetch отзывов), `reviews.js` (REVIEWS_GE+Vary), `middleware.js` (ka→/ge/, SKIP+matcher). Гейт: **регресс RU/EN**. Риск: 🔴 общие файлы.
- **Ф3. Трансформер (пер-типовый, 2-3 скрипта — не один):** общее ядро `gen-ge-core.js` (canonical→/ge/, hreflang квадры, og:locale+alternates, `lang=ka`, schema `@id`/url/inLanguage/knowsLanguage/breadcrumb, переключатель RU|EN|GE desktop+drawer, preload шрифта только в /ge/) + пер-типовые доводки (блог-скрипт-патч; главная — данные main.js; аномалии). Текст пока EN. Гейт: predeploy+GE на 1 файле каждого типа.
- **Ф4. Перевод (качество без носителя):** сбор грунтинг-корпуса .ge + глоссарий → субагент EN→KA (только текст-ноды) → критик-субагент (беглость/кальки) → обратный перевод KA→RU. Гейт: паритет + критик≥4/5 + сверка смысла.
- **Ф5. Двойники+sitemap:** hreflang ka + GE-кнопка на RU/EN двойниках (правило: GE-кнопка только при наличии двойника); `/ge/` url + `xhtml:link ka` в старые записи sitemap. Гейт: реципрокность.
- **Ф6. Деплой+QA пилот (6 стр):** атомарный деплой (страницы+общие файлы вместе); гейт из Success Criteria = GO/NO-GO.
- **Ф7. Масштаб (231 стр):** тот же пайплайн батчами по категориям, loop-until-parity; индексация.
- **Ф8. Бэк-паритет (отдельно, Ask first):** chat/voucher/booking/telegram на грузинском.

## Известные ошибки, которые спека закрывает (аудит найден)

1. **canonical** — трансформер переписывает на self `/ge/` (иначе де-индексация как дубль EN). Проверено в коде: EN canonical-ит на `/en/`.
2. **main.js `setLang`/фолбэк** — `setLang` ЖИВОЙ; на `/ge/` без ветки ge обнулит текст. Логика бинарная `"en"===lang` → без правки динамика на `/ge/` = русская; делаем EN-фолбэк.
3. **Реципрокность** — правим не 237, а ~711 файлов (GE + RU + EN двойники) + sitemap.
4. **Общие файлы** — регресс-тест RU/EN обязателен перед деплоем.
5. **preload шрифта** — только в /ge/; глобально лишь `@font-face` с unicode-range.
6. **reviews.js** — `Vary` отсутствует (проверено), CDN отдаст RU/EN на /ge/ → добавляем.
7. **Точность вязи** — обратный перевод; литературность = ревью носителя (вне объёма, зафиксировано).

## Open Questions

- ~~Ревью носителя грузинского~~ — РЕШЕНО: носителя нет → качество через 3-слойный пайплайн (грунтинг-корпус .ge + глоссарий + состязательный критик). Остаточный предел: без человека 100% литературность негарантируема, но грубые кальки/галлюцинации сняты.
- ~~Индексация пилота~~ — РЕШЕНО: деплой и индексация **только по команде владельца** (не автономно).
