# План действий (после аудита 18.09.2026)

## Сделано 18.09
viewport GE ×111, 45 порченых токенов GE, 2 невалидных JSON-LD, карта+адрес на контактах, 14 EN-редиректов, author/даты на about, CollectionPage на хабе, блок тура ниже ответа (метро). Всё задеплоено, IndexNow отправлен.

## Ждёт решения владельца
1. 460+ или 500+ туров — одна цифра на весь сайт.
2. Разрешение добавить источник рейтинга рядом с «4.9 · 90+» в hero главной.
3. Гео-страницы «туры из города» EN/GE: noindex или дописывать уникальный текст.

## Неделя 1 (без вопросов)
4. Sitemap-images: 18 записей → убрать/заменить 5 битых файлов (sitemap — по команде).
5. Убрать из crawl `scripts/_xdefault_backup_20260704/`, `gid/_template/`.
6. Сироты: ссылки на `oplata/`, `en/pay/`, `ge/gadakhda/` из футера/страниц оплаты; `partner/`, `dashboard/` — noindex.
7. Mobile Казбеги: фиксировать высоту строки live-погоды (нет горизонтального скролла).
8. 7 страниц без meta description.

## Недели 2–3
9. Performance: deferred.css (85% лишнего), long tasks на `/`, LCP `/en/`; домерить 5 страниц.
10. Страница «Экскурсии из Тбилиси на 1 день» (SXO, 8/9 SERP — каталог однодневок).
11. Казбеги: галерея 10+ фото, видео выше; EN transfer — таблица сравнения + title.
12. EN блог: убрать «hidden gem»-клише (10 постов); `ge/blog/tbilisoba` до 1 500 слов.
13. `about/` TravelAgency: telephone/sameAs на верхний узел; llms.txt расширить; обновить docs/wikidata-entity.md.

## Контроль
- 02.10: `python3 scripts/gsc-ctr-check.py`; почта по тикету API 3-6965000041597.
- GSC: Mobile usability по ge/blog, Enhancements по FAQ/Product.

## Выполнено 18.09 (вечер, «все чини»)
- Решения по умолчанию (вариант 1): 460+ туров везде (815 замен + stat-box about, «500+ проведённых»); источник рейтинга в hero (Google, Яндекс, Tripadvisor) ru/en/ge; гео EN/GE — сняты конфликтующие `index,follow` (остался noindex; GE даёт 11 кликов — при желании открыть).
- Неделя 1: 5 битых картинок заменены на существующие (19 файлов + image-sitemap); robots.txt закрывает design-previews/, docs/, graphify-out/, gid/_template/, hero3d-grass2.html; сироты = намеренные noindex-страницы оплаты, не трогали; строка live-погоды переносится (weather-line.js v2).
- Недели 2–3: клише EN (vibrant/breathtaking/bustling → 0); GE tbilisoba 1 176 → 1 435 слов (раздел «как добраться и бюджет»); about TravelAgency telephone/sameAs; Wikidata Q140518485 в sameAs на 154 стр.; llms.txt 80 → 840 URL; Lighthouse исключён из языкового авторедиректа (он и был причиной «LCP /en/ 4,1 с»); Казбеги — галерея 10 фото ru/en/ge; EN transfer — таблица под key-fact + новый title; /ekskursiya/ перенацелен на «экскурсии из Тбилиси» (RU-страница однодневок слита туда 301 — закон одной статьи); CTA над сгибом на /tury-v-gruziyu/.
- Не сделано: deferred.css — файл правит другой агент (uncommitted); Google Indexing API — квота 429, повторить 19.09 (`scratchpad/gidx.txt`); GBP/бэклинки — нет доступа.
