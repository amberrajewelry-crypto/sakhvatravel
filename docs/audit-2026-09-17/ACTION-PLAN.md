# Sakhva Travel — план действий (17.09.2026)

## Фаза 1 — Critical/High, неделя 1
1. Язык только из URL: убрать `navigator.language`-переключение hero/виджета на `/` и блоге (Critical).
2. Решение по 84 гео-лендингам: обогатить или noindex хвоста (High). Требует решения Владимира.
3. hreflang ka на `/`, `/en/`; блок hreflang на `/en/ekskursiya/kazbegi-transfer-from-tbilisi/`; inLanguage +ka.
4. SVG `<title>` → `<desc>` на 3 метро-страницах.
5. Единый блок `#business` TravelAgency на всех страницах.
6. Развести плавающие элементы на мобиле: звук — в шапку/скрыть при sticky-баре; чат-пузырь не поверх CTA.
7. Sticky WhatsApp-бар на блог-страницах (mobile).
8. Убрать Product-дубль, оставить TouristTrip+Offer.

## Фаза 2 — Medium, недели 2–3
9. LCP: критический CSS, hero srcset; сторонние скрипты после idle.
10. Cloudflare cache rule для HTML; проверить Vercel edge.
11. `/tours` → `/ekskursiya/` в один хоп.
12. Лендинг-профиль гида (фото, лицензия, отзывы с источниками) под «гид в Тбилиси»/EN; объединить Кахетия/вино и Батуми-кластеры.
13. dateModified по факту; даты на /about/, /pogoda/*; обновить llms.txt.
14. Добить `/blog/chaevye-v-gruzii/`, `/voprosy/`; имя гида на `/en/`.
15. Блок «тур в этот сезон» в первом экране /pogoda/*.
16. AggregateRating → ссылка на источник; листинги GetYourGuide/Viator.
17. Фото гида; line-иконки вместо эмодзи; цена+рейтинг в hero главной.
18. Title/description топ-20 striking-distance (грузинский алфавит, visa rules, спасибо по-грузински) + десктопные сниппеты.

## Фаза 3 — контент и авторитет, месяц 2
19. Ссылки: Tripadvisor актуализация, GetYourGuide supplier, гостевые посты RU-travel-блогов, GNTA/Georgia.travel, отели-партнёры.
20. Сванетия: контент под 6 тур-страниц (сейчас 1 инфо-пост).
21. FAQ-ответы 100–160 слов на ключевых страницах (AI-цитаты).

## Фаза 4 — мониторинг
22. lastmod по факту; image/video sitemap; SearchAction; rsl.xml; унификация robots для AI-ботов.
23. GSC: починить пагинацию скрипта, вытянуть 90-дн. запросы; добавить GOOGLE_API_KEY для CrUX; еженедельный PSI.
