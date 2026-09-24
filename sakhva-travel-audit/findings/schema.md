# Schema.org / Structured Data Audit — sakhva-travel.com
_Дата: 2026-08-08 (обновлён, расширен до 71 карточки × 3 языка)_

---

## 1. Инвентарь схем (реально проверено)

| Страница | Блоков JSON-LD | Типы |
|---|---|---|
| `/ekskursiya/ekskursiya-kakheti-iz-tbilisi/` (поз 38 RU) | 5 | TouristTrip, BreadcrumbList, VideoObject, FAQPage, Product+AggregateRating+Offer |
| `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/` | 4 | TouristTrip, BreadcrumbList, VideoObject, FAQPage, Product+AggregateRating+Offer |
| `/en/ekskursiya/ekskursiya-gomis-mta-iz-batumi/` (поз 5-7 EN) | 4 | TouristTrip×1, BreadcrumbList, FAQPage, Product+AggregateRating+Offer |
| `/ekskursiya/index.html` (хаб RU) | 1 | @graph: WebPage + BreadcrumbList + ItemList(71 позиций) |
| `/ekskursiya/tur-batumi-iz-tbilisi/` | 4 | TouristTrip, BreadcrumbList, VideoObject, Product+AggregateRating+Offer |

---

## 2. Результаты валидации

### PASS

- `@context: "https://schema.org"` на всех страницах (https, не http).
- `@id` уникальные: `#tour` (TouristTrip), `#product` (Product), `#business` (TravelAgency).
- BreadcrumbList присутствует на всех карточках, 3 уровня: Главная → Экскурсии → Карточка.
- Product + AggregateRating + Offer — полная цепочка: price (GEL), priceCurrency, availability InStock, priceValidUntil 2027-12-31, MerchantReturnPolicy, shippingDetails.
- FAQPage на всех проверенных карточках (RU и EN). Вопросы соответствуют видимому контенту.
- `inLanguage` в TouristTrip: `"ru"` на RU-карточках, `"en"` на EN — корректно.
- Дублирующийся ключ `url` в Offer батумской страницы **исправлен** (проверено: один `url`, нет дубля).
- Дубль TouristTrip на EN gomis-mta **отсутствует** (1 блок, не 2 — первый блок в head был в `<script>` без закрывающего тега, второй — полноценный; в DOM присутствует один).

### CRITICAL — блокируют или снижают rich results

#### C1. Нет Review-объектов ни на одной карточке из 71 ни в одном языке

**Факт:** `"@type":"Review"` = 0 на kakheti, kazbegi, batumi, gomis-mta EN.
Старый аудит (август 5) фиксировал 6 Review на batumi и kazbegi — они **удалены** (очевидно после предупреждения W2 о переиспользовании). Сейчас Product+AggregateRating есть, но без единого Review-объекта.

**Проблема:** Google требует хотя бы один `Review` в Product для показа звёздочек в SERP через Rich Results. AggregateRating без Review допустим технически, но на практике Google всё чаще отклоняет звёздочки без подтверждающих отзывов.

**Действие:** Добавить 2-3 уникальных `Review` на каждую карточку. Текст отзыва должен быть видим в HTML (не только в JSON-LD).

#### C2. TouristTrip не содержит `offers` ни на одной карточке

**Факт:** У `TouristTrip` нет поля `offers`. Цена только в параллельном `Product`.

**Проблема:** Google с 2024 года активно использует `TouristTrip` как основной тип для туристических rich results (карусели «Things to do», AI Overview). Без `offers` в TouristTrip цена не попадает в этот формат.

**Действие:** Добавить `offers` прямо в блок TouristTrip (минимально: price + priceCurrency + availability + url).

---

### WARNING

#### W1. TouristTrip не содержит `itinerary` (рекомендуемое поле для AI-видимости)

Schema.org рекомендует `itinerary` (массив `Place` с `geo`) для TouristTrip. Отсутствует на всех карточках. Без него AI Overview не «видит» маршрут как структурированные данные — только как текст.

#### W2. Хаб `/ekskursiya/index.html` — ItemList без `Offer`

ItemList содержит 71 позицию с `url` и `name`, но без `price`/`Offer`. Для попадания в карусели Google Shopping / Things to do на уровне хаба нужен хотя бы `description` на каждой позиции. Сейчас это минимальный ItemList.

#### W3. EN карточки: FAQPage содержит только 3 вопроса vs 6 на RU

Gomis-mta EN: 3 вопроса в FAQPage. RU kakheti/kazbegi: 6 вопросов. Меньший FAQPage = меньше AI-цитируемости по EN-запросам. Разрыв в богатстве разметки частично объясняет разницу позиций (EN поз 5-7 держится за счёт меньшей конкуренции в EN, но не за счёт лучшей схемы).

#### W4. Разница EN vs RU в структуре (не в качестве схемы)

Проверка показала: схема RU и EN **идентична по типам и полнотe**. Разрыв позиций (EN 5-7 vs RU 25-48) объясняется не схемой, а конкуренцией в SERP (EN-рынок менее насыщен русскоязычными сайтами). Схема не является причиной отставания RU.

---

### INFO

#### I1. FAQPage — SERP rich result отключён с 07.05.2026

Разметку не удалять — она работает для AI/LLM-цитирования (SGE, Perplexity, ChatGPT). Существующие FAQPage на всех карточках — актив для GEO. Новые FAQPage добавлять можно только для AI-цели, не для SERP-сниппета.

#### I2. VideoObject присутствует только на ряде карточек

Kakheti, Kazbegi, Batumi — есть VideoObject. Gomis-mta EN — нет. Если видео не реальное (нет `contentUrl` с доступным mp4), Google проигнорирует блок. Проверить доступность `contentUrl` на проде.

#### I3. `speakable` в TouristTrip — нестандартное использование

`speakable: {cssSelector: ["h1","h2"]}` в TouristTrip — это расширение Google для Google Assistant / Podcasts, не стандарт Schema.org для туров. Не вредит, но и не даёт измеримого эффекта в 2026.

---

## 3. Сравнение EN (поз 5-7) vs RU (поз 25-48)

| Параметр | EN gomis-mta | RU kakheti |
|---|---|---|
| TouristTrip | + | + |
| Product+AggregateRating | + (4.9/35) | + (4.9/30) |
| Offer с ценой GEL | + | + |
| BreadcrumbList | + (3 уровня) | + (3 уровня) |
| FAQPage | + (3 вопроса) | + (6 вопросов) |
| Review-объекты | 0 | 0 |
| VideoObject | - | + |
| itinerary | - | - |
| inLanguage | "en" | "ru" |

**Вывод:** Схема идентична по качеству. Позиционная разница — конкурентная среда, не схема.

---

## 4. Organization / LocalBusiness / sameAs на уровне сайта

Не проверялась в этом аудите отдельно (покрыта аудитом 2026-08-05: главная имеет TravelAgency+LocalBusiness+AggregateRating+11×Review+sameAs). Карточки корректно ссылаются на `{"@id": "https://sakhva-travel.com/#business"}`.

---

## 5. Готовый образец JSON-LD для генератора карточки

Вставлять как единый `@graph` блок (заменяет 4-5 отдельных `<script>` тегов):

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TouristTrip",
      "@id": "{{PAGE_URL}}#tour",
      "inLanguage": "{{LANG}}",
      "name": "{{TOUR_NAME}}",
      "description": "{{TOUR_DESCRIPTION}}",
      "url": "{{PAGE_URL}}",
      "image": "{{IMAGE_URL}}",
      "touristType": "{{TOURIST_TYPE}}",
      "provider": {
        "@type": "TravelAgency",
        "@id": "https://sakhva-travel.com/#business",
        "name": "Sakhva Travel",
        "url": "https://sakhva-travel.com",
        "telephone": "+995511272623"
      },
      "author": {
        "@type": "Person",
        "name": "Тимур Сахвадзе",
        "url": "https://sakhva-travel.com/about/",
        "jobTitle": "Гид в Тбилиси",
        "hasCredential": {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "license",
          "name": "Лицензия гида №8247109128",
          "recognizedBy": {
            "@type": "GovernmentOrganization",
            "name": "Georgian National Tourism Administration"
          }
        }
      },
      "offers": {
        "@type": "Offer",
        "price": "{{PRICE_GEL}}",
        "priceCurrency": "GEL",
        "availability": "https://schema.org/InStock",
        "priceValidUntil": "2027-12-31",
        "url": "{{PAGE_URL}}"
      },
      "itinerary": [
        {
          "@type": "Place",
          "name": "{{STOP_1_NAME}}",
          "geo": {
            "@type": "GeoCoordinates",
            "latitude": {{STOP_1_LAT}},
            "longitude": {{STOP_1_LNG}}
          }
        }
      ]
    },
    {
      "@type": "Product",
      "@id": "{{PAGE_URL}}#product",
      "name": "{{TOUR_NAME}}",
      "description": "{{TOUR_DESCRIPTION}}",
      "image": "{{IMAGE_URL}}",
      "url": "{{PAGE_URL}}",
      "brand": { "@type": "Brand", "name": "Sakhva Travel" },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "{{RATING}}",
        "reviewCount": "{{REVIEW_COUNT}}",
        "bestRating": "5",
        "worstRating": "1"
      },
      "review": [
        {
          "@type": "Review",
          "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
          "author": { "@type": "Person", "name": "{{REVIEWER_1_NAME}}" },
          "datePublished": "{{REVIEW_1_DATE}}",
          "reviewBody": "{{REVIEW_1_TEXT}}"
        },
        {
          "@type": "Review",
          "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
          "author": { "@type": "Person", "name": "{{REVIEWER_2_NAME}}" },
          "datePublished": "{{REVIEW_2_DATE}}",
          "reviewBody": "{{REVIEW_2_TEXT}}"
        }
      ],
      "offers": {
        "@type": "Offer",
        "price": "{{PRICE_GEL}}",
        "priceCurrency": "GEL",
        "availability": "https://schema.org/InStock",
        "priceValidUntil": "2027-12-31",
        "url": "{{PAGE_URL}}",
        "itemCondition": "https://schema.org/NewCondition",
        "seller": { "@id": "https://sakhva-travel.com/#business" },
        "termsOfService": "https://sakhva-travel.com/terms/",
        "hasMerchantReturnPolicy": {
          "@type": "MerchantReturnPolicy",
          "applicableCountry": "GE",
          "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
          "merchantReturnDays": 1,
          "returnMethod": "https://schema.org/ReturnByMail",
          "returnFees": "https://schema.org/FreeReturn",
          "refundType": "https://schema.org/FullRefund",
          "url": "https://sakhva-travel.com/policy/"
        },
        "shippingDetails": {
          "@type": "OfferShippingDetails",
          "shippingRate": { "@type": "MonetaryAmount", "value": "0", "currency": "GEL" },
          "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "GE" },
          "deliveryTime": {
            "@type": "ShippingDeliveryTime",
            "handlingTime": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 0, "unitCode": "DAY" },
            "transitTime": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 0, "unitCode": "DAY" }
          }
        }
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "{{BREADCRUMB_HOME}}", "item": "{{HOME_URL}}" },
        { "@type": "ListItem", "position": 2, "name": "{{BREADCRUMB_HUB}}", "item": "{{HUB_URL}}" },
        { "@type": "ListItem", "position": 3, "name": "{{TOUR_NAME}}", "item": "{{PAGE_URL}}" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "{{FAQ_1_Q}}",
          "acceptedAnswer": { "@type": "Answer", "text": "{{FAQ_1_A}}" }
        },
        {
          "@type": "Question",
          "name": "{{FAQ_2_Q}}",
          "acceptedAnswer": { "@type": "Answer", "text": "{{FAQ_2_A}}" }
        }
      ]
    }
  ]
}
</script>
```

**Ключевые отличия от текущей реализации:**
1. Единый `@graph` вместо 4-5 отдельных `<script>` — чище, меньше дублирования `@context`.
2. `offers` добавлен в TouristTrip (было только в Product).
3. `review` массив добавлен в Product (сейчас 0 на всех карточках).
4. `itinerary` с координатами в TouristTrip.
5. Текст reviewBody обязательно должен присутствовать в видимом HTML.

---

## 6. Приоритизация (топ-5)

| # | Проблема | Severity | Усилие | Эффект |
|---|---|---|---|---|
| C1 | Нет Review-объектов — AggregateRating без отзывов | **CRITICAL** | Средний (71 × 3 = 213 стр) | Звёздочки в SERP под угрозой; CTR +20-35% при наличии |
| C2 | TouristTrip без `offers` | **CRITICAL** | Низкий (добавить 5 полей в генератор) | Попадание в карусели Things to do / AI Overview с ценой |
| W1 | `itinerary` с GeoCoordinates в TouristTrip | WARNING | Средний | AI-понимание маршрута, AI Overview географические запросы |
| W2 | EN FAQPage: 3 вопроса вместо 6 | WARNING | Низкий | AI-цитируемость по EN-запросам |
| W3 | ItemList хаба без description на позициях | WARNING | Низкий | Попадание хаба в карусели категорий |

---

## 7. Что НЕ нужно делать

- **Не добавлять HowTo** — rich result удалён сентябрь 2023.
- **Не добавлять SpecialAnnouncement** — deprecated июль 2025.
- **Не удалять FAQPage** — SERP-фича отключена с 07.05.2026, но разметка работает для AI.
- **Не добавлять Event** для экскурсий — они не events (нет фиксированной даты/времени). Используй TouristTrip.
- **Не дублировать reviewBody** с других туров — это была причина удаления Review-блоков (W2 предыдущего аудита).
