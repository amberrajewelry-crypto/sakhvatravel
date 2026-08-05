# Полный SEO-аудит — sakhva-travel.com

**Дата:** 2026-08-05 · **Health Score: 73/100** · **Тип:** Local Service (частный тур-гид Тбилиси, мультиязычный RU/EN/GE)
Метод: 8 профильных специалистов (technical, content, schema, sitemap, performance, geo, local, sxo) + прямые проверки прода. Детали — в `findings/*.md`.

## Executive Summary

Сайт технически здоров (Яндекс «No problems detected», SQI 10), с сильной schema-базой и лучшим-в-нише llms.txt. Основные потери — не в технике, а в **обесцененной Review-разметке** (перекрёстные отзывы → нет звёзд в SERP), **page-type mismatch** на ключевых коммерческих страницах и **слабой EN-видимости**. Ни одного блокера индексации.

### Реальные проблемы (перепроверены прямым чтением HTML/файлов) + статус
1. **Дублированный canonical на 106 GE-страницах** — ✅ ИСПРАВЛЕНО (дедуп 106 файлов, 0 дублей, hreflang цел). Ждёт деплоя.
2. **Рассинхрон Telegram-контакта** — ✅ ИСПРАВЛЕНО (унифицировано → `@SakhvaGuideBot`, 7 замен, метка канал→бот). Ждёт деплоя.
3. **Рецикл отзывов на турах** — проверено: те же авторы/тексты (Елена, Mikhail D, Giorgi V., Виталий, Nugo Shengelia) на большинстве из 68 туров; 5/6 reviewBody идентичны Батуми=Казбеги. Риск обесценивания Review-разметки. ⚠️ Требует решения (реальные отзывы или снять разметку — не фабрикуем).
4. **GEO/llms** — meta-externalagent заблокирован (robots), нет EUR в en/llms.txt, рассинхрон числа отзывов/дат между llms-файлами.
5. **miralinks-article.html → 404** — в .vercelignore; проблема только если ведёт живой платный бэклинк (verify).

> **Ревизия точности (строгая перепроверка, включая мои собственные ошибки):** ОПРОВЕРГНУТЫ как ложные — «Гид как автор Review» (МОЯ ошибка: Тимур — автор контента тура, не отзывов), «17 orphan-экскурсий», «rtveli 404» (разные слаги по языкам, все 200), «AggregateRating нет нигде», «дубль url в Offer», sitemap «4 файла» (их 5). ПОДТВЕРЖДЕНЫ прямой проверкой — GE-canonical ×106 (исправлено), рецикл отзывов, Telegram (исправлено). HTTP-свип: 737 loc + 732 hreflang = все 200.

## Оценки по категориям

| Категория | Вес | Балл | Главное |
|-----------|-----|------|---------|
| Technical SEO | 22% | 74 | GE canonical-дубль (Crit), miralinks 404 (High), sitemap lastmod |
| Content / E-E-A-T | 23% | 68 | 5 тонких статей, 2 каннибализации, GE тоньше EN |
| On-Page / SXO | 20% | 70 | page-type mismatch /tury-v-gruziyu/ (Crit), /en/ generic |
| Schema | 10% | 80 | база сильная; перекрёстные Review (High) |
| Performance | 10% | 82 | главная 358KB, 8 render-blocking CSS; SVG метро ок |
| AI / GEO | 10% | 74 | Telegram-рассинхрон (Crit), Meta заблокирован, EN слаб |
| Images | 5% | 78 | webp+lazy ок; alt-покрытие не верифицировано |

**Дополнительно:** Sitemap 76 · Local 71.

## Ключевые разрешения конфликтов между специалистами
- **AggregateRating:** content и sxo-агенты заявили «нет нигде» — **ошибка**. Schema-специалист (чтение сырого HTML) подтвердил: главная + 68 тур-страниц имеют полную цепочку Product+AggregateRating+Review. Реальная проблема — не отсутствие, а **перекрёстное дублирование отзывов**, из-за чего Google не показывает звёзды. Это объясняет симптом «нет звёзд» при наличии разметки.
- **Perf-агент** упал по socket — замер выполнен вручную (performance.md).

## Разделы
Технический — `findings/technical.md` · Контент — `content.md` · Schema — `schema.md` · Sitemap — `sitemap.md` · Performance — `performance.md` · GEO/AI — `geo.md` · Local — `local.md` · SXO — `sxo.md`.

## План действий
См. `ACTION-PLAN.md` — 4 фазы (Critical неделя 1 → Monitoring постоянно).

## Что работает и не требует правок
Security headers (HTTPS/HSTS/CSP), hreflang-взаимность ru↔en↔ka, self-canonical, полная schema главной (TravelAgency+LocalBusiness, geo, openingHours, AggregateRating 4.9/90, лицензия), Person+опыт-от-первого-лица на 102 постах, inline-SVG схема метро, отложенная аналитика, llms.txt RU (лучший в нише). Потолок PSI держат 3rd-party (Yandex Metrica/GTM/PostHog) + Vercel TTFB — код оптимизировать смысла нет без отказа от трекинга.
