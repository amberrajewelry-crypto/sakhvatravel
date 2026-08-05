# Local SEO Audit — sakhva-travel.com
Дата: 2026-08-05
Аудитор: Local SEO Agent (claude-sonnet-4-6)

---

## Local SEO Score: 71 / 100

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| GBP Signals | 25% | 72 | 18.0 |
| Reviews & Reputation | 20% | 80 | 16.0 |
| Local On-Page SEO | 20% | 75 | 15.0 |
| NAP Consistency & Citations | 15% | 53 | 8.0 |
| Local Schema Markup | 10% | 88 | 8.8 |
| Local Link & Authority Signals | 10% | 52 | 5.2 |
| **ИТОГО** | | | **71.0** |

---

## Бизнес-тип: Hybrid (SAB + физадрес)

Гид Тимур — частный тур-оператор. На сайте указан физический адрес (14 Merab Kostava St, Тбилиси 0108), встроены ссылки на Google Maps и Яндекс Карты. Одновременно бизнес работает как SAB: туры проводятся по всей Грузии (Казбеги, Кахетия, Сванетия), клиенты встречаются у отеля. GBP верифицирован (CID 14070083063461040701).

**Отрасль:** Tourism / Tour Guide (TravelAgency + LocalBusiness)

---

## 1. NAP-консистентность

### Сводная таблица источников

| Поле | index.html (footer) | index.html (schema) | llms.txt | Страницы туров (ekskursiya/) |
|------|---------------------|---------------------|----------|------------------------------|
| Name | Sakhva Travel | Sakhva Travel | Sakhva Travel | Sakhva Travel |
| Address | 14 ул. Мераба Костава, Тбилиси 0108 | 14 Merab Kostava St, 0108 | — (не указан) | — (не указан) |
| Phone | +995 511 272 623 | +995511272623 | +995 511 272 623 | +995511272623 |
| Telegram | t.me/SakhvaGuideBot | t.me/SakhvaGuideBot?start=site | @SakhvaTravel | t.me/SakhvaGuideBot?start=site |
| Email | help@sakhva-travel.com | help@sakhva-travel.com | help@sakhva-travel.com | — |

### Найденные расхождения

**CRITICAL — Telegram handle рассинхронизирован:**
- `llms.txt` (строки 19, 31, 40): указан `@SakhvaTravel` — это публичный канал/username
- `index.html` footer + schema + все страницы туров: `t.me/SakhvaGuideBot` — это бот
- Для AI-агентов, которые цитируют llms.txt, Telegram-контакт будет неверным. Пользователь напишет в @SakhvaTravel (канал), а не в бот бронирования.

**LOW — Phone formatting:**
- Footer: `+995 511 272 623` (с пробелами)
- Schema/wa.me: `+995511272623` (без пробелов)
- Функционально одинаково, но для NAP-консистентности лучше унифицировать в E.164: `+995511272623`

**LOW — Address язык в schema vs footer:**
- Schema: `streetAddress: "14 Merab Kostava St"` (английский)
- Footer bottom bar: `14 ул. Мераба Костава, Тбилиси 0108` (русский)
- GBP ожидает соответствие локальному написанию. Рекомендуется привести к единому: английский в schema (корректно для addressCountry: GE), русский в видимом тексте.

**LOW — llms.txt не содержит адреса:**
- AI-агенты, работающие с llms.txt, не получают физический адрес. Для SAB это приемлемо, но для hybrid-бизнеса лучше добавить.

---

## 2. LocalBusiness / TravelAgency Schema

### Результат валидации

| Свойство | Статус | Значение |
|----------|--------|---------|
| @type | PASS | ["TravelAgency", "LocalBusiness"] |
| name | PASS | "Sakhva Travel" |
| legalName | PASS | "ИП Сахвадзе Т.В." |
| telephone | PASS | "+995511272623" |
| email | PASS | "help@sakhva-travel.com" |
| address (PostalAddress) | PASS | 14 Merab Kostava St, 0108, GE |
| geo (GeoCoordinates) | PASS | lat: 41.7250505, lng: 44.7789235 (5 знаков — норма) |
| openingHoursSpecification | PASS | Пн-Вс 08:00–22:00 |
| aggregateRating | PASS | 4.9 / 90 отзывов |
| priceRange | PASS | "₾98–₾595" |
| currenciesAccepted | PASS | "GEL, USD, EUR" |
| areaServed | PASS | Тбилиси, Казбеги, Кахетия, Батуми, Сванетия |
| sameAs | PASS | 9 платформ (TG, IG, WA, Tripadvisor, YouTube, Maps, Яндекс, FB, Threads) |
| hasMap | PASS | google.com/maps?cid=14070083063461040701 |
| image | PASS | og-cover.jpg (1200×630) |
| logo | PASS | logo-schema.webp (300×60) |
| url | PASS | https://sakhva-travel.com/ |
| description | PASS | Присутствует |

**Замечания:**

- **WARN — Субтип schema:** `TravelAgency` корректен для тур-агентства. Но для индивидуального лицензированного гида точнее добавить `TouristInformationCenter` или `Person` (гид Тимур) как `hasEmployee` / `founder`. Страницы туров используют `TouristTrip` — это правильно.
- **WARN — `reviewCount: 90` в schema vs `90 отзывов` в llms.txt:** Совпадает, но на страницах отдельных туров `aggregateRating` указывает разные значения (от 20 до 47 отзывов) — это отзывы конкретного тура, что допустимо.
- **INFO — `openingHoursSpecification`:** Дан как один объект без массива. Для Rich Results валидно, но рекомендуется проверить через schema.org validator — некоторые парсеры ожидают массив.
- **INFO — `dateModified: "2026-05-13"`:** Устарело на ~3 месяца. При следующем контентном изменении обновить.

---

## 3. Отзывы / Review Health

| Метрика | Значение | Оценка |
|---------|----------|--------|
| AggregateRating в schema (главная) | 4.9 / 90 | Отлично |
| AggregateRating в schema (страницы туров) | 4.7–4.9 / 20–47 | Хорошо |
| Видимые отзывы на главной | Есть (секция с цитатами) | Есть |
| Review schema (отдельные Review объекты) | НЕ ОБНАРУЖЕНЫ | Пробел |
| Ответы на отзывы (видимые на сайте) | Нет | Нет данных |
| Velocity (оценка по llms.txt) | 90 отзывов Google, 2026 | Норма |

**Ключевой пробел подтверждён:** `AggregateRating` в schema присутствует на главной и страницах туров. Контент-агент был неточен — рейтинг В SCHEMA ЕСТЬ. Однако отдельные `Review` объекты (с `author`, `reviewBody`, `datePublished`) не размечены нигде — это ограничивает получение rich snippet с отдельными цитатами отзывов в SERP.

**Правило 18 дней (Sterling Sky):** Нет данных о velocity последних отзывов без доступа к GBP API. Необходимо мониторить — если нет новых отзывов >18 дней, rankings в локальном паке падают.

---

## 4. GBP Signals

| Сигнал | Статус |
|--------|--------|
| GBP верифицирован | PASS (CID 14070083063461040701) |
| Maps CID в sameAs schema | PASS |
| hasMap в schema | PASS |
| Ссылка на Maps в footer | PASS (maps.app.goo.gl/...) |
| Google Maps embed на странице | НЕ ОБНАРУЖЕН |
| Place photos упоминания | Нет явного |
| GBP Posts signal на сайте | Нет |
| Review widget (GBP) | Нет embed; есть ручные цитаты |
| Кнопка "Написать отзыв" | Есть (ссылка на Google Maps reviews) |
| Категория GBP | Не проверить без GBP API (предположительно "Tour operator" или "Tourist attraction") |

**Замечание:** Отсутствие Maps iframe — это не критично для ранжирования, но снижает конверсию мобильных пользователей, которые хотят проверить локацию. Для SAB/hybrid это менее важно, чем для brick-and-mortar.

---

## 5. Citations (Tier 1 директории)

| Платформа | Статус | Примечание |
|-----------|--------|------------|
| Google Business Profile | PASS | CID верифицирован |
| Tripadvisor | PASS | В sameAs schema, прямая ссылка |
| Яндекс Бизнес / Яндекс Карты | PASS | yandex.com.ge/profile/103365004008 в schema и footer |
| 2ГИС | PARTIAL | Ссылка на Батуми-поиск (2gis.ge/batumi/search/sakhva+travel/firm/...) — нет прямой карточки Тбилиси |
| Facebook | PASS | В sameAs (people/Sakhva-Travel/61590273044825) |
| Instagram | PASS | @sakhvatravel в schema и footer |
| YouTube | PASS | @SakhvaTravel в schema |
| Viator | НЕТ | Не найден в schema/llms.txt |
| GetYourGuide | НЕТ | Не найден |
| BBB | N/A | Не релевантен для Грузии |
| Booking.com Experiences | НЕТ | Не найден |

**Критический пробел для тур-гида:** Viator и GetYourGuide — Tier 1 для туристической ниши. Отсутствие профилей на этих платформах = упущенный трафик англоязычных туристов. Они также являются citation-сигналами для GBP.

**2ГИС:** Ссылка ведёт на поиск в Батуми, а не на прямую карточку Тбилиси. Вероятно, карточка в 2ГИС Тбилиси отсутствует или не привязана.

---

## 6. Local On-Page SEO

### Целевые страницы под локальные интенты

| Интент | URL | Статус |
|--------|-----|--------|
| гид Тбилиси / экскурсии Тбилиси | / (главная) | Есть, оптимизирована |
| частный гид Тбилиси | / + /ekskursiya/* | Есть в FAQs и контенте |
| экскурсия Казбеги из Тбилиси | /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ | Есть |
| тур Кахетия | /ekskursiya/ekskursiya-kakheti-iz-tbilisi/ | Есть |
| ночной Тбилиси | /ekskursiya/nochnaya-ekskursiya-tbilisi/ | Есть |
| Tbilisi private tour guide (EN) | /en/tour/* | Структура есть |
| тур для эмигрантов Тбилиси | /tour/emigrant/ | Уникальный, нет конкурентов |
| digital nomad Тбилиси | /tour/digital-nomad/ | Уникальный интент |

**Сильные стороны:**
- Страницы туров используют `TouristTrip` schema с `author` (Person с лицензией) — сильный E-E-A-T сигнал
- FAQ schema на главной
- Уникальные интенты (эмигранты, digital nomad) без прямой конкуренции в локальном паке
- 55 статей блога на RU + 10 на EN — хороший контентный объём

**Пробелы:**
- Нет страницы `/guide/timur/` или `/about/` с Person schema и `hasCredential` (лицензия №8247109128) на главном домене в виде отдельного URL — лицензия есть только в TouristTrip schema страниц туров
- Ценники в llms.txt (₾77–₾595) расходятся с CLAUDE.md (€45+). Нужно унифицировать для AI-агентов

---

## 7. Локальный пак / Maps Ranking Factors

Релевантные факторы (Whitespark 2026):

| Фактор | Оценка | Комментарий |
|--------|--------|-------------|
| Первичная категория GBP | Неизвестно без API | Предположительно "Tour operator" — проверить |
| Proximity | Вне контроля (55.2% variance) | Офис на Kostava St — центр Тбилиси, позиция хорошая |
| Review velocity | Требует мониторинга | 90 отзывов — хорошая база, важна непрерывность |
| Dedicated service pages | PASS | 12+ страниц туров + blog |
| Citation consistency | PARTIAL | Telegram handle рассинхронизирован |
| sameAs depth | Хорошо | 9 платформ |
| Schema completeness | Хорошо | Все обязательные поля |

---

## Топ-10 приоритетных действий

### CRITICAL

**1. Исправить Telegram в llms.txt**
- Проблема: `@SakhvaTravel` в llms.txt vs `t.me/SakhvaGuideBot` везде
- Фикс: заменить все упоминания `@SakhvaTravel` в llms.txt на `@SakhvaGuideBot` (или `t.me/SakhvaGuideBot`)
- Файл: `/Users/vladimir/sakhva-travel/llms.txt` строки 19, 31, 40
- Риск: AI-агенты направляют пользователей в неверный Telegram-контакт

### HIGH

**2. Создать профиль на Viator и GetYourGuide**
- Viator (принадлежит Tripadvisor): https://www.viator.com/partners
- GetYourGuide: https://supplier.getyourguide.com
- NAP должен совпадать с сайтом: "Sakhva Travel", +995511272623
- Влияние: citations для GBP + прямые бронирования от EN-туристов

**3. Добавить индивидуальные `Review` объекты в schema главной**
- Добавить 3–5 `Review` с `author`, `reviewBody`, `datePublished`, `reviewRating` в @graph главной
- Это разблокирует rich snippet с звёздами + цитатой в SERP (сейчас только AggregateRating)

**4. Проверить и исправить категорию GBP**
- По Whitespark 2026, неверная категория — фактор #1 негативного влияния (score 176)
- Проверить в GBP: должно быть "Tour operator" + secondary "Tourist attraction" или "Tour guide"
- Без доступа к GBP Dashboard невозможно подтвердить

**5. Исправить 2ГИС — создать карточку Тбилиси**
- Текущая ссылка ведёт на поиск в Батуми: `2gis.ge/batumi/search/sakhva+travel/...`
- Создать/найти карточку в 2ГИС Тбилиси и обновить ссылку в footer и schema sameAs
- 2ГИС популярен у русскоязычной аудитории — ключевой сегмент Sakhva

### MEDIUM

**6. Обновить `dateModified` в schema**
- `"dateModified": "2026-05-13"` — 3 месяца назад
- Обновлять при каждом контентном изменении; влияет на freshness сигнал для Googlebot

**7. Добавить адрес и Telegram в llms.txt**
- Физический адрес для hybrid-бизнеса полезен для AI-цитирования
- Telegram должен быть `t.me/SakhvaGuideBot`, не username канала

**8. Унифицировать формат телефона**
- Везде использовать `+995511272623` (E.164) — в schema, wa.me href, tel: href
- Видимый текст может остаться `+995 511 272 623`

**9. Добавить Google Maps iframe на страницу контактов / главную**
- Усиливает GBP-сигнал и конверсию
- `<iframe src="https://www.google.com/maps?cid=14070083063461040701&output=embed">`

**10. Создать отдельную страницу `/about/timur/` с Person schema**
- `@type: Person`, `name: "Тимур Сахвадзе"`, `hasCredential` (лицензия №8247109128)
- `jobTitle: "Лицензированный гид Тбилиси"`, `knowsAbout`, `sameAs` (Instagram, YouTube)
- Усиливает E-E-A-T для всех страниц туров через `author` → `sameAs` связку

### LOW

- Добавить Booking.com Experiences профиль (растущая платформа для туров)
- Рассмотреть Klook для азиатских туристов (нишевый, но растёт в Тбилиси)
- `openingHoursSpecification` привести к формату массива для максимальной совместимости

---

## Ограничения аудита

Без платных инструментов не проверялось:
- Реальная позиция в локальном паке Google Maps по запросам "гид Тбилиси", "tour guide Tbilisi" (нет DataForSEO)
- Актуальное состояние GBP (фото, посты, Q&A, primary category) — нет GBP API
- Velocity отзывов за последние 18 дней (нет доступа к GBP dashboard)
- NAP в GBP (телефон/адрес) относительно данных сайта — нет прямого доступа
- Реальные позиции профилей на Tripadvisor/Яндекс в поиске
- Proximity advantage/disadvantage по конкретным запросам (55.2% variance — вне контроля)
