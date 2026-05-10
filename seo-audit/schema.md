# Schema.org Audit — sakhva-travel.com

Дата: 2026-05-04

---

## 1. Обзор обнаруженной разметки

| Страница | Формат | Типы Schema |
|---|---|---|
| `/` (RU homepage) | JSON-LD @graph | WebSite, WebPage, TravelAgency, Person, TouristTrip x12, ItemList, VideoObject, FAQPage (10 Q), Review x3, BreadcrumbList |
| `/en/` (EN homepage) | JSON-LD @graph | Точная копия RU homepage (см. CRITICAL ниже) |
| `/tour/kazbegi/` | JSON-LD @graph | WebPage, BreadcrumbList, TouristTrip, TouristAttraction x2, FAQPage |
| `/blog/kazbegi-iz-tbilisi-2026/` | JSON-LD @graph | BlogPosting, BreadcrumbList, FAQPage |
| `/blog/bani-tbilisi/` | JSON-LD @graph + Microdata | BlogPosting, BreadcrumbList, FAQPage + `<article itemscope itemtype="BlogPosting">` |

---

## 2. Валидация по блокам

### 2.1 RU Homepage `/`

**WebSite** -- PASS
- @context: https://schema.org -- OK
- @id, url, name, description, inLanguage -- OK

**WebPage** -- PASS
- isPartOf, about, primaryImageOfPage, datePublished, dateModified -- OK
- Даты ISO 8601 -- OK

**TravelAgency** -- PASS (отлично проработано)
- address, geo, openingHoursSpecification -- OK
- aggregateRating (4.9, 87 reviews) -- OK
- sameAs массив (6 платформ) -- OK
- areaServed с wikidata sameAs -- OK
- priceRange, currenciesAccepted, paymentAccepted -- OK
- logo с width/height -- OK

**Person (guide-timur)** -- PASS
- knowsLanguage, jobTitle, worksFor, image -- OK

**TouristTrip x12** -- PASS
- offers с price, priceCurrency, availability, priceValidUntil -- OK
- duration в ISO 8601 (PT14H, P3D и т.д.) -- OK
- provider ссылка через @id -- OK

**ItemList (tour-list)** -- PASS
- 12 ListItem с position и url -- OK
- numberOfItems: 12 -- совпадает

**VideoObject** -- PASS
- thumbnailUrl, uploadDate (ISO 8601 с timezone), duration, contentUrl -- OK
- publisher с logo -- OK

**FAQPage (10 вопросов)** -- INFO
- Структура корректна: Question + acceptedAnswer
- INFO: FAQPage на коммерческом сайте не дает rich results в Google с августа 2023. Сохранить для AI/LLM discoverability (GEO).

**Review x3** -- PASS
- itemReviewed через @id -- OK
- reviewRating, author (Person), datePublished -- OK

**BreadcrumbList** -- PASS
- Единственный элемент "Главная" -- корректно для homepage

---

### 2.2 EN Homepage `/en/` -- 2 CRITICAL ISSUES

**CRITICAL-1: inLanguage = "ru" вместо "en"**
- WebSite.inLanguage: "ru" -- WRONG, должно быть "en"
- WebPage.inLanguage: "ru" -- WRONG, должно быть "en"

**CRITICAL-2: Все URL ведут на RU-версию**
- WebSite.url: "https://sakhva-travel.com/" -- WRONG, должно быть "https://sakhva-travel.com/en/"
- WebPage.url: "https://sakhva-travel.com/" -- WRONG
- Все TouristTrip.url ведут на `/tour/kazbegi/` вместо `/en/tour/kazbegi/`
- BreadcrumbList item: "https://sakhva-travel.com/" вместо "/en/"

**CRITICAL-3: Контент на русском**
- Все name, description, reviewBody, FAQ answers -- на русском языке
- EN homepage должна иметь английские тексты в schema

**Рекомендация:** Полностью пересобрать JSON-LD для /en/ с:
- inLanguage: "en"
- URL-ами /en/*
- Английскими текстами

---

### 2.3 Tour Page `/tour/kazbegi/`

**WebPage** -- PASS
- isPartOf через @id на #website -- OK
- dateModified, primaryImageOfPage -- OK

**BreadcrumbList** -- PASS
- 3 уровня: Главная > Туры > Казбеги -- OK
- Все URL абсолютные -- OK

**TouristTrip** -- PASS (расширенный)
- itinerary с ItemList (6 stops) -- OK
- maximumAttendeeCapacity: 7 -- OK
- availableLanguage: ["ru", "en"] -- OK
- aggregateRating -- OK
- review x2 с datePublished -- OK
- provider как inline TravelAgency (а не @id ссылка) -- дублирует данные, но не ошибка

**TouristAttraction x2** -- PASS
- geo с координатами -- OK
- address -- OK

**FAQPage** -- INFO (см. замечание по FAQPage выше)

---

### 2.4 Blog `/blog/kazbegi-iz-tbilisi-2026/`

**BlogPosting** -- PASS
- headline, description, author (Person с @id), publisher (Organization с logo) -- OK
- datePublished, dateModified -- ISO 8601 OK
- image -- абсолютный URL OK
- mainEntityOfPage -- OK

**BreadcrumbList** -- PASS
- 3 уровня: Главная > Блог > Казбеги из Тбилиси 2026 -- OK

**FAQPage** -- INFO

Замечание: BlogPosting отсутствует `wordCount`, `articleSection`, `keywords` -- рекомендуемые, не обязательные.

---

### 2.5 Blog `/blog/bani-tbilisi/`

**BlogPosting** -- PASS
- Аналогично kazbegi -- корректный формат

**BreadcrumbList** -- PASS

**FAQPage** -- INFO

**Microdata на `<article>`** -- WARNING
- `<article itemscope itemtype="https://schema.org/BlogPosting">` дублирует JSON-LD BlogPosting
- Нет itemprop атрибутов внутри article -- Microdata объявлен, но не заполнен
- Рекомендация: убрать itemscope/itemtype с `<article>`, т.к. JSON-LD уже полностью покрывает BlogPosting

---

## 3. Сводка проблем

| # | Приоритет | Страница | Проблема |
|---|---|---|---|
| 1 | CRITICAL | `/en/` | inLanguage="ru", все URL на RU-версию, тексты на русском |
| 2 | WARNING | `/blog/bani-tbilisi/` | Пустой Microdata `itemscope` дублирует JSON-LD |
| 3 | INFO | Все страницы | FAQPage не дает rich results (коммерческий сайт), но полезна для GEO/AI |

---

## 4. Упущенные возможности

### 4.1 SiteNavigationElement (все страницы)

Навигация сайта не размечена. Добавит понимание структуры для поисковиков.

### 4.2 BlogPosting: расширенные свойства

На обеих статьях блога отсутствуют:
- `wordCount` -- помогает AI/LLM оценить глубину контента
- `articleSection` -- категория статьи
- `inLanguage` -- явное указание языка

### 4.3 Отдельная страница `/tour/kazbegi/` -- нет hreflang-связи в schema

TouristTrip на `/tour/kazbegi/` не ссылается на EN-версию. Если есть `/en/tour/kazbegi/`, стоит добавить `workTranslation`/`translationOfWork` или хотя бы `availableLanguage` уже есть.

### 4.4 Review snippet для страниц туров

На homepage есть Review x3 + AggregateRating на TravelAgency. На `/tour/kazbegi/` есть Review x2 + AggregateRating на TouristTrip. Это хорошо. Проверить, что на остальных 11 tour pages также есть Review + AggregateRating.

---

## 5. JSON-LD для исправления CRITICAL: EN Homepage

Заменить весь JSON-LD на `/en/index.html`. Ниже -- скелет с ключевыми отличиями от RU (тексты нужно перевести полностью):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://sakhva-travel.com/en/#website",
      "url": "https://sakhva-travel.com/en/",
      "name": "Sakhva Travel",
      "description": "Private English-speaking guide in Georgia. Kazbegi, Kakheti, hidden Tbilisi. Up to 7 people.",
      "inLanguage": "en"
    },
    {
      "@type": "WebPage",
      "@id": "https://sakhva-travel.com/en/#webpage",
      "url": "https://sakhva-travel.com/en/",
      "name": "Private Guide in Tbilisi 2026 ★4.9 | Sakhva Travel",
      "description": "Private guide Timur. Kazbegi from ₾175, hidden Tbilisi from ₾140, Kakheti. Up to 7 people. Free cancellation. Reply in 15 min.",
      "inLanguage": "en",
      "isPartOf": { "@id": "https://sakhva-travel.com/en/#website" },
      "about": { "@id": "https://sakhva-travel.com/#business" },
      "primaryImageOfPage": {
        "@type": "ImageObject",
        "url": "https://sakhva-travel.com/images/og-cover.webp"
      },
      "datePublished": "2024-03-01",
      "dateModified": "2026-04-30"
    },
    {
      "@type": "TravelAgency",
      "@id": "https://sakhva-travel.com/#business",
      "name": "Sakhva Travel",
      "url": "https://sakhva-travel.com/",
      "telephone": "+995511272623",
      "email": "help@sakhva-travel.com",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Tbilisi",
        "addressRegion": "Tbilisi",
        "postalCode": "0105",
        "addressCountry": "GE"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 41.7250505,
        "longitude": 44.7789235
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "08:00",
        "closes": "22:00"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 4.9,
        "reviewCount": 87,
        "bestRating": 5,
        "worstRating": 1
      },
      "priceRange": "₾77–₾595",
      "currenciesAccepted": "GEL, USD, EUR",
      "paymentAccepted": "Cash, Card, Cryptocurrency",
      "description": "Private guide in Georgia. Kazbegi, Kakheti, hidden spots in Tbilisi. Up to 7 people.",
      "image": "https://sakhva-travel.com/images/og-cover.webp",
      "logo": {
        "@type": "ImageObject",
        "url": "https://sakhva-travel.com/images/logo-schema.webp",
        "width": 300,
        "height": 60
      },
      "sameAs": [
        "https://t.me/SakhvaGuideBot?start=site",
        "https://www.instagram.com/sakhvatravel",
        "https://wa.me/995511272623",
        "https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html",
        "https://www.youtube.com/@SakhvaTravel",
        "https://www.google.com/maps?cid=14070083063461040701"
      ],
      "areaServed": [
        { "@type": "City", "name": "Tbilisi" },
        { "@type": "Place", "name": "Kazbegi" },
        { "@type": "Place", "name": "Kakheti" },
        { "@type": "Country", "name": "Georgia" }
      ],
      "foundingDate": "2023-01-01"
    },
    {
      "@type": "Person",
      "@id": "https://sakhva-travel.com/#guide-timur",
      "name": "Timur",
      "url": "https://sakhva-travel.com/en/about/",
      "jobTitle": "Private Guide in Georgia",
      "description": "Professional guide in Tbilisi since 2023. Leads tours to Kazbegi, Kakheti, and hidden spots in Tbilisi.",
      "worksFor": { "@id": "https://sakhva-travel.com/#business" },
      "knowsLanguage": ["ru", "en"],
      "telephone": "+995511272623",
      "image": "https://sakhva-travel.com/images/timur.webp"
    },
    {
      "@type": "TouristTrip",
      "@id": "https://sakhva-travel.com/en/#trip-kazbegi",
      "name": "Kazbegi Day Trip from Tbilisi",
      "url": "https://sakhva-travel.com/en/tour/kazbegi/",
      "description": "Georgian Military Highway, Ananuri fortress, Gergeti Trinity Church with views of Mt. Kazbek 5047m. Private English-speaking guide.",
      "touristType": "English-speaking tourists",
      "offers": {
        "@type": "Offer",
        "price": "175",
        "priceCurrency": "GEL",
        "availability": "https://schema.org/InStock",
        "priceValidUntil": "2027-12-31",
        "url": "https://sakhva-travel.com/en/tour/kazbegi/"
      },
      "duration": "PT14H",
      "provider": { "@id": "https://sakhva-travel.com/#business" },
      "image": "https://sakhva-travel.com/images/kazbegi-tour.webp"
    }
  ]
}
```

**NOTE:** Выше показан сокращенный пример. Нужно аналогично перевести все 12 TouristTrip, ItemList, VideoObject, FAQPage (10 Q на EN), Review x3, BreadcrumbList с EN URL-ами.

---

## 6. Исправление WARNING: убрать Microdata с bani-tbilisi

В файле `/blog/bani-tbilisi/index.html`, строка 329:

```html
<!-- Было -->
<article itemscope itemtype="https://schema.org/BlogPosting">

<!-- Заменить на -->
<article>
```

---

## 7. Рекомендуемые улучшения BlogPosting (низкий приоритет)

Добавить в каждый BlogPosting:

```json
"inLanguage": "ru",
"wordCount": 2500,
"articleSection": "Путеводитель",
"keywords": ["казбеги", "тбилиси", "грузия", "тур"]
```

---

## 8. Итог

| Метрика | Значение |
|---|---|
| Всего schema-блоков | 5 страниц, ~40 entities |
| CRITICAL | 1 (EN homepage -- неправильный язык и URL) |
| WARNING | 1 (дублирующий Microdata) |
| INFO | 1 (FAQPage без rich results) |
| Покрытие типов | Отличное: TravelAgency, TouristTrip, Person, BlogPosting, Review, AggregateRating, VideoObject, BreadcrumbList, ItemList, TouristAttraction |
| Упущено | SiteNavigationElement, расширенные BlogPosting props |

**Следующий шаг:** Исправить EN homepage JSON-LD -- это самая критичная проблема, Google видит EN-страницу как русскоязычную.
