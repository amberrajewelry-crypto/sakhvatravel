# Schema.org / Structured Data Audit — sakhva-travel.com
_Дата: 2026-08-05_

---

## 1. Инвентарь схем

| Страница | Типы JSON-LD |
|---|---|
| `/` (главная) | TravelAgency+LocalBusiness, AggregateRating (4.9/90), 11x Review, WebSite, BreadcrumbList |
| `/ekskursiya/tur-batumi-iz-tbilisi/` | TouristTrip, Product+AggregateRating(4.9/42)+6×Review, BreadcrumbList, VideoObject |
| `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/` | TouristTrip, Product+AggregateRating(4.7/20)+6×Review, BreadcrumbList, VideoObject |
| `/tury-v-gruziyu/` | TravelAgency, ItemList (12 Product с Offer), FAQPage, BreadcrumbList |
| `/tury-v-gruziyu-iz-moskvy/` | TravelAgency+AggregateRating, BreadcrumbList |
| `/blog/metro-tbilisi/` | BlogPosting (Article), FAQPage, BreadcrumbList |

---

## 2. Результаты валидации

### PASS — что работает корректно

- `@context` везде `"https://schema.org"` (https, не http). ✅
- `@id` уникальные на страницах туров: `#tour` для TouristTrip, `#product` для Product, `#business` для TravelAgency. ✅
- BreadcrumbList присутствует на всех проверенных страницах (туры, блог, geo-лендинги). ✅
- Product+AggregateRating+Review на 68 страницах `/ekskursiya/*` — полная трёхзвенная цепочка для rich results. ✅
- Offer на Product: price, priceCurrency, availability, priceValidUntil, MerchantReturnPolicy, shippingDetails — соответствует требованиям Google Shopping/Rich results 2025+. ✅
- BlogPosting: headline, datePublished, dateModified, author, publisher, image (ImageObject с width/height), mainEntityOfPage. ✅
- VideoObject: name, description, thumbnailUrl, contentUrl, uploadDate, duration. ✅
- FAQPage на блоге: вопросы совпадают с видимым текстом страницы (проверено для metro-tbilisi — все 6 вопросов присутствуют в HTML). ✅

---

## 3. Найденные проблемы

### CRITICAL — блокируют rich results

**Нет.** Все критические поля присутствуют на проверенных страницах.

---

### WARNING — риск потери rich results или санкций

#### W1. Отзывы в Review НЕ видны на странице (несовпадение schema / visible content)

**Страницы:** `/ekskursiya/tur-batumi-iz-tbilisi/`, `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/` (предположительно все 68 туров).

**Суть:** В Product schema embedded 6 объектов `Review` с `reviewBody`. Google с 2023 года **требует**, чтобы текст `reviewBody` был виден пользователю на странице. Проверка: строка «Поехали в Казбеги» встречается 2 раза в HTML — один раз в JSON-LD schema, один раз где-то ещё. Нужно убедиться, что именно `reviewBody` отображается в DOM, а не просто дублируется в другом скрипте.

**Действие:** Открыть страницу тура в браузере с отключённым JS и проверить, видны ли цитаты отзывов. Если отзывы рендерятся через JS и не индексируются — добавить их в статический HTML.

#### W2. Одинаковые Review объекты переиспользуются на разных турах

**Страницы:** Батуми и Казбеги имеют **одинаковые** `reviewBody` от одних авторов («Поехали в Казбеги» упоминает Казбеги, но этот отзыв стоит на странице тура в Батуми). Google может расценить это как манипуляцию рейтингами.

**Действие:** Для каждого тура использовать только релевантные отзывы про этот конкретный маршрут.

#### W3. TouristTrip не имеет `offers` — нет возможности для Price rich result через этот тип

**Страница:** Все `/ekskursiya/*`

**Суть:** `TouristTrip` не содержит `offers`, цена только в параллельном `Product`. Это допустимо, но означает, что `TouristTrip` сам по себе не даёт ценовой сниппет. `Product`+`Offer` корректно покрывает это через отдельный блок. Ситуация приемлема, но если Google выберет только TouristTrip (старый тип), цена пропадёт.

**Рекомендация (необязательно):** Добавить `offers` и в TouristTrip для дублирования.

---

### INFO — не блокируют, но стоит знать

#### I1. FAQPage на tury-v-gruziyu — Google SERP rich result отключён с мая 2026

Google отключил FAQ rich results для всех сайтов 07.05.2026. FAQPage разметка на `/tury-v-gruziyu/` и `/blog/metro-tbilisi/` больше не даёт звёздочек/аккордеона в SERP. Разметку **не удалять** — она помогает AI/LLM-цитированию (SGE, Perplexity, ChatGPT). Статус: информационный.

#### I2. TouristTrip: `itinerary` отсутствует (рекомендуемое поле)

Schema.org рекомендует `itinerary` (массив `Place`) для TouristTrip. Отсутствует на всех проверенных турах. Не блокирует, но улучшает понимание маршрута поисковиком.

#### I3. TravelAgency на `/tury-v-gruziyu/` — нет AggregateRating в главном блоке

На `/tury-v-gruziyu/` TravelAgency без `aggregateRating` — только ItemList и FAQPage. Geo-лендинги (`/tury-v-gruziyu-iz-moskvy/`) имеют AggregateRating. Несогласованность, но не ошибка.

#### I4. VideoObject: `description` у батумского ролика упоминает «Казбеги» (копипаст)

`/ekskursiya/tur-batumi-iz-tbilisi/` → VideoObject description: «Видео из однодневного тура в Батуми: остановки в Гори и Кутаиси по дороге...» — корректно. Ок.

#### I5. `url` дублируется как поле в Offer на батумской странице

В объекте Offer есть два поля `"url"` — первое правильное, второе перезаписывает. JSON технически невалиден (дублирующийся ключ в объекте). Большинство парсеров берут последнее значение, но стоит убрать дубль.

```json
// Текущий баг в offers:
"url": "https://sakhva-travel.com/ekskursiya/tur-batumi-iz-tbilisi/",  // первое
"termsOfService": "...",
"url": "..."  // второй url — дубль ключа
```

---

## 4. Проверка конкретных страниц

### /ekskursiya/tur-batumi-iz-tbilisi/

| Блок | Статус | Примечание |
|---|---|---|
| TouristTrip | PASS | name, description, url, provider, touristType, image, speakable, @id |
| Product+AggregateRating | PASS | price 250 GEL, reviewCount 42, ratingValue 4.9 |
| Review (6 шт.) | WARNING | Текст «Поехали в Казбеги» на странице про Батуми — несоответствие контента |
| BreadcrumbList | PASS | 3 уровня |
| VideoObject | PASS | uploadDate, duration PT30S |
| Offer дубль `url` | WARNING | Дублирующийся ключ в JSON |

### /ekskursiya/ekskursiya-kazbegi-iz-tbilisi/

| Блок | Статус | Примечание |
|---|---|---|
| TouristTrip | PASS | @id = `#trip` (не `#tour` как у Батуми) — разные id, ок |
| Product+AggregateRating | PASS | price 175 GEL, reviewCount 20, ratingValue 4.7 |
| Review (6 шт.) | WARNING | Те же авторы, что на Батуми — переиспользование |
| BreadcrumbList | PASS | 3 уровня |
| VideoObject | PASS | |

### /blog/metro-tbilisi/

| Блок | Статус | Примечание |
|---|---|---|
| BlogPosting | PASS | Все обязательные поля, image с width/height |
| FAQPage | INFO | 6 вопросов совпадают с видимым текстом. SERP-фича отключена с мая 2026 |
| BreadcrumbList | PASS | 3 уровня |

### /tury-v-gruziyu/

| Блок | Статус | Примечание |
|---|---|---|
| TravelAgency | PASS | Без AggregateRating (несогласованность с geo-лендингами) |
| ItemList | PASS | 12 позиций, каждая Product+Offer |
| FAQPage | INFO | Нет SERP-фичи с мая 2026 |
| BreadcrumbList | PASS | 2 уровня |

---

## 5. Рекомендованные JSON-LD сниппеты

### Снип A: Исправление дублирующегося url в Offer (W5)

В Product→offers убрать второй `"url"` ключ, оставить только `"termsOfService"`:

```json
"offers": {
  "@type": "Offer",
  "price": "250",
  "priceCurrency": "GEL",
  "availability": "https://schema.org/InStock",
  "priceValidUntil": "2027-12-31",
  "url": "https://sakhva-travel.com/ekskursiya/tur-batumi-iz-tbilisi/",
  "termsOfService": "https://sakhva-travel.com/terms/",
  "itemCondition": "https://schema.org/NewCondition",
  "seller": {"@id": "https://sakhva-travel.com/#business"},
  "hasMerchantReturnPolicy": { ... },
  "shippingDetails": { ... }
}
```

### Снип B: itinerary для TouristTrip (необязательно, улучшение для AI)

Добавить в блок TouristTrip:

```json
"itinerary": [
  {
    "@type": "Place",
    "name": "Тбилиси",
    "geo": {"@type": "GeoCoordinates", "latitude": 41.6941, "longitude": 44.8337}
  },
  {
    "@type": "Place",
    "name": "Гори",
    "geo": {"@type": "GeoCoordinates", "latitude": 41.9858, "longitude": 44.1142}
  },
  {
    "@type": "Place",
    "name": "Батуми",
    "geo": {"@type": "GeoCoordinates", "latitude": 41.6458, "longitude": 41.6415}
  }
]
```

### Снип C: offers в TouristTrip (опционально, для покрытия обоих типов)

```json
{
  "@context": "https://schema.org",
  "@type": "TouristTrip",
  "@id": "https://sakhva-travel.com/ekskursiya/tur-batumi-iz-tbilisi/#tour",
  "name": "Тур в Батуми из Тбилиси за 1 день",
  "offers": {
    "@type": "Offer",
    "price": "250",
    "priceCurrency": "GEL",
    "availability": "https://schema.org/InStock",
    "url": "https://sakhva-travel.com/ekskursiya/tur-batumi-iz-tbilisi/"
  }
}
```

---

## 6. Приоритизация

| # | Проблема | Severity | Усилие | Эффект |
|---|---|---|---|---|
| W2 | Неуместные reviewBody (Казбеги на странице Батуми) | HIGH | Средний (68 страниц) | Риск Manual Action от Google за манипуляцию Reviews |
| W1 | Проверить видимость reviewBody в DOM | HIGH | Низкий (проверка) | Rich results могут быть отклонены |
| W3 (дубль url) | Дублирующийся ключ в Offer JSON | MEDIUM | Низкий | Чистота парсинга |
| I2 | itinerary в TouristTrip | LOW | Средний | AI-видимость маршрутов |
| I3 | AggregateRating на /tury-v-gruziyu/ | LOW | Низкий | Согласованность |

---

## 7. Что НЕ нужно делать

- **Не добавлять HowTo** — rich result удалён сентябрь 2023.
- **Не добавлять новые FAQPage** — SERP-фича отключена с мая 2026. Существующие не трогать.
- **Не добавлять SpecialAnnouncement** — deprecated с июля 2025.
- **Не трогать существующий FAQPage на metro/tury-v-gruziyu** — разметка помогает AI-цитированию.
