# Local SEO Audit: sakhva-travel.com

**Дата:** 2026-08-13  
**Аудитор:** Claude Sonnet 4.6 (automated)  
**Бизнес:** Sakhva Travel — частный гид Тимур Сахвадзе, Тбилиси, Грузия  
**Лицензия:** #8247109128 | WhatsApp: +995511272623

---

## Local SEO Score: 78 / 100

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| GBP Signals | 25% | 82 | 20.5 |
| Reviews & Reputation | 20% | 85 | 17.0 |
| Local On-Page SEO | 20% | 82 | 16.4 |
| NAP Consistency & Citations | 15% | 72 | 10.8 |
| Local Schema Markup | 10% | 70 | 7.0 |
| Local Link & Authority Signals | 10% | 62 | 6.2 |
| **TOTAL** | | | **78** |

*Прирост +4 балла vs предыдущий аудит (74/100, май 2026): добавлены Yandex Maps, Facebook, Threads в sameAs; reviewCount 87→90.*

---

## Тип бизнеса

**Hybrid SAB (Service Area Business + точка встречи)**

- Адрес в schema: `14 Merab Kostava St, Тбилиси, 0108, GE` — присутствует в JSON-LD, визуально на contacts не выделен как полный физический адрес
- GBP CID: `14070083063461040701` — подтверждён в `sameAs` и `hasMap`
- Maps embed: iframe на contacts (RU/EN/GE)
- Модель: гид выезжает к туристам, не офис для посещения

**Индустриальный вертикаль: Tour / Travel (private tour guide)**

---

## NAP Consistency Audit

### Таблица источников

| Поле | index schema | contacts RU schema | contacts visible | en/index schema | ge/index schema | Footer |
|------|--------------|--------------------|------------------|-----------------|-----------------|--------|
| Name | Sakhva Travel | Sakhva Travel | Sakhva Travel | Sakhva Travel | Sakhva Travel | Sakhva Travel |
| streetAddress | 14 Merab Kostava St | 14 Merab Kostava St | не выделен | 14 Merab Kostava St | 14 Merab Kostava St | отсутствует |
| addressLocality | Тбилиси (RU) | Тбилиси (RU) | Тбилиси | Tbilisi (EN) | Tbilisi (EN) | Тбилиси |
| postalCode | 0108 | 0108 | — | 0108 | 0108 | — |
| telephone | +995511272623 | +995511272623 | +995 511 272 623 | +995511272623 | +995511272623 | оба формата |
| email | help@sakhva-travel.com | help@sakhva-travel.com | help@sakhva-travel.com | help@sakhva-travel.com | help@sakhva-travel.com | help@sakhva-travel.com |

### Расхождения

**[MEDIUM]** Footer содержит одновременно `+995511272623` (в href) и `+995 511 272 623` (visible text). Для пользователя нормально, но создаёт два варианта NAP при скрейпинге. Видимый текст везде должен быть `+995 511 272 623`.

**[MEDIUM]** contacts RU — streetAddress есть в schema, но не отображается явно для пользователя. SAB это допускает, но снижает доверие.

**[HIGH]** ge/contacts — `areaServed` как простой массив строк `["Tbilisi"]`, тогда как ge/index использует типизированные объекты `{"@type":"City","name":"თბილისი","sameAs":"wikidata"}`. Несогласованность внутри одного языка.

**[HIGH]** ge/contacts — два конфликтующих `reviewCount` в одной странице: 90 (TravelAgency блок) и 36 (отдельный Review объект). Google берёт первый встреченный; второй создаёт противоречие.

**[LOW]** contacts EN schema — нет `telephone` и `streetAddress` в TravelAgency блоке. EN-версия страницы контактов передаёт неполный NAP.

**[LOW]** `addressLocality` на contacts RU — кириллица `"Тбилиси"`. Для PostalAddress Google рекомендует латиницу в международном контексте.

---

## GBP Signals на сайте

| Сигнал | Статус | Детали |
|--------|--------|--------|
| Google Maps embed | ДА | iframe на contacts (RU/EN/GE) |
| GBP CID ссылка | ДА | `cid=14070083063461040701` в sameAs + hasMap |
| Google Maps place link | ДА | В sameAs главной |
| Yandex Maps профиль | ДА | profile/103365004008 — добавлено с мая 2026 |
| TripAdvisor badge | ДА | Travellers' Choice, в sameAs |
| Facebook | ДА | В sameAs — добавлено с мая 2026 |
| Threads | ДА | В sameAs — добавлено с мая 2026 |
| Review виджет (живой) | НЕТ | Только статичные цитаты |
| CTA «Оставить отзыв» Google | НЕТ | Отсутствует на всех страницах |
| Directions link | НЕТ | Нет кнопки «Построить маршрут» |
| GBP фото / Places API | НЕТ | Нет интеграции |
| GBP посты на сайте | НЕТ | Не вынесены |

---

## Review Health Snapshot

| Метрика | Значение | Оценка |
|---------|----------|--------|
| Рейтинг (schema main) | 4.9 / 5 | Отлично |
| Кол-во отзывов (main) | 90 | Хорошо для нишевого SAB |
| datePublished в Review | НЕТ — contacts RU | Блокирует Review Rich Snippet |
| datePublished в Review | ДА — contacts EN/GE (2025-12 – 2026-05) | ОК |
| Видимые reviewBody на главной | 15 элементов | ОК |
| CTA «Write a review» | ОТСУТСТВУЕТ | Критично |
| TripAdvisor Travellers' Choice | ДА, linked | Сильный сигнал |
| Review velocity | Неизвестна | Требует GBP панели |
| Response rate | Неизвестен | Требует GBP панели |

**Правило 18 дней (Sterling Sky)**: без CTA стимулировать отзывы сложнее — риск velocity cliff при спаде сезона.

---

## Local Schema Validation

### Главная страница (index.html)

| Свойство | Статус | Примечание |
|----------|--------|------------|
| @type | `["TravelAgency","LocalBusiness"]` | Массив — правильно |
| name | ДА | "Sakhva Travel" |
| legalName | ДА | "ИП Сахвадзе Т.В." |
| streetAddress | ДА | "14 Merab Kostava St" |
| postalCode | ДА | "0108" |
| geo (precision) | ДА | 41.7250505 / 44.7789235 (7 знаков) |
| telephone | ДА | +995511272623 |
| email | ДА | help@sakhva-travel.com |
| openingHoursSpecification | ДА | Mon-Sun 08:00-22:00 |
| aggregateRating | ДА | 4.9, 90 reviews |
| priceRange | ДА | ₾98–₾595 |
| areaServed (типизированные) | ДА | City/Place/Country с wikidata sameAs |
| sameAs (9 платформ) | ДА | TG, IG, WA, TA, YT, GMaps, Yandex, FB, Threads |
| hasMap | ДА | CID URL |
| currenciesAccepted | ДА | GEL, USD, EUR |
| Person (гид) | ДА | Timur, jobTitle, worksFor, knowsLanguage |
| TouristTrip | ДА | Все туры с Offer, duration |
| FAQPage | ДА | 9+ пар |
| VideoObject | ДА | Промо-видео |
| addressRegion | ПРОБЛЕМА | "Тбилиси" — город, не регион |

**Замечания:**

- **[MEDIUM]** `addressRegion = "Тбилиси"` — должен быть административный регион, а не город. Для Тбилиси как самостоятельной административной единицы правильно либо опустить поле, либо использовать `"Tbilisi"` (EN). Текущее значение технически верно, но создаёт дублирование с `addressLocality`.
- **[LOW]** `openingHoursSpecification` — единый объект вместо массива. Валидно, но массив с разбивкой по дням более гибкий.

### Страницы туров / направлений

| Страница | Блоков schema | FAQPage | AggregateRating | areaServed | Review | hreflang EN |
|----------|--------------|---------|-----------------|------------|--------|-------------|
| kakheti | 2 | ДА | НЕТ | НЕТ | НЕТ | ДА |
| tury-na-kazbek | 1 | ДА | НЕТ | НЕТ | НЕТ | **НЕТ** |
| mtskheta-mtianeti | 2 | ДА | НЕТ | НЕТ | НЕТ | ДА |
| tury-v-tbilisi | 2 | ДА | ДА (14) | НЕТ | НЕТ | **НЕТ** |
| ekskursiya | 2 | ДА | НЕТ | НЕТ | НЕТ | ДА |

**Критично:** 4 из 5 ключевых страниц туров без `AggregateRating` — нет звёзд в SERP сниппете. `tury-v-tbilisi` имеет AggregateRating с 14 отзывами вместо реальных 90.

**Все 5 страниц туров не имеют `areaServed`** — потеря гео-релевантности.

### Страница contacts

| Свойство | contacts RU | contacts EN | contacts GE |
|----------|------------|------------|------------|
| telephone | ДА | НЕТ | ДА |
| streetAddress | ДА | НЕТ | НЕТ |
| aggregateRating (reviewCount) | ДА (90) | ДА (36 — занижено) | КОНФЛИКТ (90 + 36) |
| Review datePublished | НЕТ | ДА | ДА |
| areaServed формат | строки (деградация) | типизированный | строки (деградация) |
| ContactPoint | ДА | НЕТ | НЕТ |

---

## Мультиязычность локальных данных

### hreflang покрытие

| Страница | ru | en | ka | x-default |
|----------|----|----|----|-----------|
| index | ДА | ДА | ДА | ДА |
| contacts | ДА | ДА | ДА | ДА |
| kakheti | ДА | ДА | ДА | ДА |
| tury-na-kazbek | ДА | **НЕТ** | ДА | ДА |
| tury-v-tbilisi | ДА | **НЕТ** | **НЕТ** | ДА |
| mtskheta-mtianeti | ДА | ДА | ДА | ДА |
| ekskursiya | ДА | ДА | ДА | ДА |

**[HIGH]** `tury-na-kazbek` — нет EN hreflang. Казбеги — топ-запрос у англоязычных туристов.

**[HIGH]** `tury-v-tbilisi` — нет EN и GE hreflang. Главный коммерческий хаб для «tour in Tbilisi».

### Локализация schema

| Поле | RU | EN | GE |
|------|----|----|----|
| addressLocality | "Тбилиси" (кириллица) | "Tbilisi" | "Tbilisi" |
| areaServed (index) | кириллица + wikidata | EN + wikidata | грузинский + wikidata |
| areaServed (contacts) | строки без типов | типизированные | строки без типов |
| reviewBody language | RU + EN смесь | EN + RU | EN + RU |

GE-версия корректно использует грузинский алфавит в `areaServed` — best practice для `inLanguage: ka`.

---

## Citation Presence (Tier 1 Directories)

| Директория | Статус | Примечание |
|------------|--------|------------|
| Google Business Profile | ДА | CID 14070083063461040701 |
| TripAdvisor | ДА | Travellers' Choice, в sameAs |
| Yandex Maps | ДА | profile/103365004008 |
| Instagram | ДА | @sakhvatravel |
| YouTube | ДА | @SakhvaTravel |
| Telegram | ДА | @SakhvaGuideBot |
| Facebook | ДА | Добавлено с мая 2026 |
| Threads | ДА | Добавлено с мая 2026 |
| WhatsApp | ДА | wa.me/995511272623 |
| 2GIS | НЕИЗВЕСТНО | Не linked на сайте |
| Viator | НЕИЗВЕСТНО | Не linked |
| GetYourGuide | НЕИЗВЕСТНО | Не linked |
| TourRadar | НЕИЗВЕСТНО | Не linked |
| Klook | НЕИЗВЕСТНО | Не linked |
| Booking.com Experiences | НЕИЗВЕСТНО | Не linked |

---

## Location Page Quality

Одна локация (Тбилиси). SAB с сервисными страницами по направлениям.

| Метрика | Оценка |
|---------|--------|
| Уникальность контента | ВЫСОКАЯ |
| Риск doorway-page | НИЗКИЙ |
| Внутренняя перелинковка | ХОРОШАЯ — ItemList, nav, breadcrumbs |
| hreflang полнота | ЧАСТИЧНАЯ — 2 ключевых страницы без EN |
| Canonical | Корректный на всех проверенных |
| Страница /contacts/ | ДА, с картой, часами, всеми каналами |
| City hub /tury-v-tbilisi/ | ДА, но только RU — нет EN/GE hreflang |

---

## Топ-10 приоритетных действий

### Critical

**1. AggregateRating на страницы туров**

`kakheti`, `tury-na-kazbek`, `mtskheta-mtianeti`, `ekskursiya` — без звёзд в SERP. Добавить в schema каждой:
```json
"aggregateRating": {
  "@type": "AggregateRating",
  "ratingValue": 4.9,
  "reviewCount": 90,
  "bestRating": 5,
  "worstRating": 1
}
```
Также исправить `tury-v-tbilisi`: заменить 14 на 90.

**2. CTA «Оставить отзыв» на Google**

Ссылка: `https://search.google.com/local/writereview?placeid=ChIJi8gUuPEHQkAR3dKFrVL72cM`  
Разместить в секции отзывов на index.html и contacts. Review velocity — #2 GBP фактор. Правило 18 дней: velocity cliff при паузе 3+ недели.

**3. hreflang на tury-na-kazbek (EN) и tury-v-tbilisi (EN + GE)**

`tury-na-kazbek` — добавить `<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/...">`.  
`tury-v-tbilisi` — добавить EN и GE варианты. Это главные коммерческие страницы для иностранных туристов.

### High

**4. areaServed на все страницы туров**

Добавить в schema каждой страницы конкретный `areaServed` с wikidata:
- kakheti: `{"@type":"Place","name":"Kakheti","sameAs":"https://www.wikidata.org/wiki/Q193261"}`
- tury-na-kazbek: `{"@type":"Place","name":"Kazbegi","sameAs":"https://www.wikidata.org/wiki/Q210019"}`
- mtskheta-mtianeti: `{"@type":"Place","name":"Mtskheta","sameAs":"https://www.wikidata.org/wiki/Q178499"}`
- ekskursiya / tury-v-tbilisi: `{"@type":"City","name":"Tbilisi","sameAs":"https://www.wikidata.org/wiki/Q994"}`

**5. Унифицировать schema на contacts EN и GE**

- contacts EN: добавить `telephone: "+995511272623"` и `streetAddress: "14 Merab Kostava St"`
- contacts GE: убрать конфликт reviewCount — оставить 90, убрать дублирующий блок с 36
- contacts RU + GE: заменить `areaServed: ["Тбилиси", ...]` (строки) на типизированные объекты с wikidata

**6. datePublished в Review на contacts RU**

5 Review объектов без дат. Добавить `"datePublished"` (реальные или приближённые: `"2026-01-15"`). Без даты Google не показывает Review Rich Snippet.

**7. Зарегистрироваться на Viator и GetYourGuide**

3 из 5 топ-факторов AI visibility — citation-related (Whitespark 2026). Viator и GetYourGuide — Tier 1 для tour operators. Каждый листинг = backlink + citation + независимый источник отзывов. После создания — добавить URL в `sameAs` на главной.

### Medium

**8. Исправить areaServed формат в contacts RU**

Заменить строковый массив на типизированные объекты с wikidata (как на main page). Единый формат критичен для Knowledge Graph парсинга.

**9. Добавить «Построить маршрут» на contacts**

Прямая ссылка: `https://maps.google.com/maps?daddr=14+Merab+Kostava+St,+Tbilisi+0108`.  
Directions link — прямой GBP-signal и удобство для пользователя.

**10. Проверить и создать листинг в 2GIS**

2GIS — Tier 1 citation для RU/CIS аудитории, популярен среди релокантов в Тбилиси. Создать/верифицировать профиль с консистентным NAP, добавить ссылку в sameAs.

---

## Limitations Disclaimer

Не оценивалось без платных инструментов или GBP панели:

- GBP live данные: категории, количество фото, Q&A, посты, Insights
- Review velocity и response rate — требуют GBP API или панели
- Позиция в local pack по целевым запросам
- Backlink профиль и локальный link authority
- NAP accuracy на внешних платформах (Yandex Maps, TripAdvisor) — только presence, не content
- Proximity фактор: 55.2% variance в local rankings (Search Atlas ML) — вне контроля
- Конкурентный анализ по Тбилиси-гидам не выполнялся
