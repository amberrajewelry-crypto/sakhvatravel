# ACTION PLAN — sakhva-travel.com

Health Score: **73/100**. Приоритет: Critical → High → Medium → Low.
Все правки — через генераторы/шаблоны (не по одному файлу). robots.txt/sitemap менять по CLAUDE.md с проверкой. predeploy-check перед деплоем.

## Phase 1 — Critical (неделя 1)

| # | Задача | Файл/место | Эффект | Статус |
|---|--------|-----------|--------|--------|
| 1 | Дедуп `<link rel=canonical>` на 106 GE-страницах | HTML GE | снять GSC/Яндекс-предупреждение | ✅ СДЕЛАНО (106 файлов, 0 дублей, hreflang цел) |
| 2 | Унифицировать Telegram → `@SakhvaGuideBot` | `llms*.txt` | AI даёт верный контакт | ✅ СДЕЛАНО (7 замен, метка канал→бот) |
| 3 | Рецикл отзывов на турах (те же авторы/тексты на большинстве 68 туров; 5/6 идентичны Батуми=Казбеги) | генератор/данные отзывов | вернуть доверие к Review-разметке | ⚠️ РЕШЕНИЕ ВЛАДИМИРА: реальные отзывы по турам ИЛИ снять Review-разметку (не фабрикую) |
| 4 | 301 `miralinks-article.html` → целевая статья (если есть живой бэклинк) | `vercel.json` | вернуть входящие ссылки | verify |

❌ Снятые как ложные находки (строгая перепроверка, вкл. мою собственную):
- «Гид как автор Review» (МОЯ ошибка) — Тимур автор контента тура, НЕ отзывов; авторы Review — клиенты.
- «17 orphan-экскурсий вне sitemap» — у всех собственный `<loc>` ×3 языка.
- «rtveli-grape-harvest → 404» — это EN/GE-слаг, RU-слаг `rtveli-sbor-vinograda`; все три 200.
- «AggregateRating нет нигде» — есть на 68 турах.
- «Дубль ключа url в Offer» — не воспроизведено (0 JSON-LD parse-ошибок на 745 стр).
- sitemap «4 файла» — их 5.

## Phase 2 — High (недели 2-3)

| # | Задача | Эффект |
|---|--------|--------|
| 7 | `/tury-v-gruziyu/` → каталог-first (карточки+цена+WA вверх, аналитика вниз) | закрыть page-type mismatch по ВЧ-таргету |
| 8 | `/tury-v-gruziyu-iz-moskvy/` → дисклеймер в 1-м абзаце + deeplink авиабилеты + отзыв из Москвы | снизить отказы (product-intent) |
| 9 | `/en/` → H1 «Private Guide in Tbilisi — Timur» + Person schema + виджет отзывов | конкуренция с ToursByLocals/TripAdvisor |
| 10 | 5 тонких RU-статей (sladosti/karty-nalichnye/taksi/chaevye/frazy) → +FAQPage, до 1200-1500w | дожатие FAQ-интента |
| 11 | robots.txt: `meta-externalagent` Allow; en/llms.txt: EUR-цены | Meta AI 20→~70; EN-цитируемость |
| 12 | sitemap lastmod → дата деплоя (билд-скрипт) | приоритет перекраула |

## Phase 3 — Medium (месяц 2)

- Каннибализация: `oteli-tbilisi` vs `rayony-tbilisi-gde-ostanovitsya`; `arenda-avto-tbilisi` vs `-gruziya` — консолидация/дифференциация.
- Viator + GetYourGuide профили (Tier-1 citations + EN); фикс 2ГИС (Тбилиси, не Батуми).
- About: блок отзывов + sameAs (Tripadvisor/Viator/Google).
- Наращивание EN-контента (10 vs 55 RU — структурный долг западной аудитории).
- Reddit r/Tbilisi, r/georgia, r/digitalnomad — органичные упоминания бренда.
- Главная: below-fold секции в отложенную загрузку (−100-150 KB критического HTML); не-критические CSS через media=print swap.
- Дубль ключа `url` в Offer JSON-LD — фикс в генераторе.

## Phase 4 — Monitoring (постоянно)

- Уникальность 28 гео-лендингов ×3 языка (doorway-риск).
- GE-паритет по объёму при новых переводах (8 GE <1000w).
- Процесс фактопроверки при зеркалировании RU→EN→GE (кейс метро).
- Мониторинг возврата звёзд в SERP после уникализации отзывов (Phase 1 #4).

## Что НЕ трогать (сильные стороны)
Security headers, hreflang-взаимность, self-canonical, schema главной (полная), Person+лицензия на постах, inline-SVG метро, отложенная аналитика, llms.txt RU. Потолок PSI держат 3rd-party+TTFB — код менять смысла нет.
