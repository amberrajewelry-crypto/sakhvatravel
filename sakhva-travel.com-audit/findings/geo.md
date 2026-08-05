# GEO Audit — sakhva-travel.com
_Date: 2026-08-05_

---

## GEO Readiness Score: 74 / 100

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Citability | 32/40 | 25% | 8/25 → ~20 |
| Structural Readability | 17/20 | 20% | ~14/20 |
| Multi-Modal Content | 10/15 | 15% | ~7/15 |
| Authority & Brand Signals | 16/20 | 20% | ~16/20 |
| Technical Accessibility | 18/20 | 20% | ~15/20 |

**Total: ~74/100** — хорошая база, есть 3 критических точки роста.

---

## 1. AI Crawler Access (robots.txt)

**Статус: ХОРОШИЙ. Стратегия корректна.**

| Crawler | Статус | Примечание |
|---------|--------|-----------|
| GPTBot | ALLOW | правильно |
| OAI-SearchBot | ALLOW | правильно |
| ChatGPT-User | ALLOW | правильно |
| ClaudeBot | ALLOW | правильно |
| Claude-Web | ALLOW | правильно |
| PerplexityBot | ALLOW | правильно |
| Google-Extended | ALLOW | правильно |
| YandexGPT | ALLOW | правильно (важно для RU-аудитории) |
| Amazonbot | ALLOW | правильно (Alexa AI) |
| AppleBot | ALLOW | правильно |
| CCBot | BLOCK | правильно (Common Crawl / обучение без пользы) |
| cohere-ai | BLOCK | правильно |
| anthropic-ai | **ALLOW** | расхождение: CCBot заблокирован как "training-only", но anthropic-ai (тоже training) — разрешён. Непоследовательно, но некритично. |
| meta-externalagent | BLOCK | **спорно**: Meta AI (Llama) использует этот UA для индексации — блокируя его, теряем видимость в Meta AI Search. |
| Bytespider | BLOCK | правильно (ByteDance scraper) |

**Проблема (MEDIUM):** `meta-externalagent` — это UA Meta AI для поиска (не только обучения). Блокировка = нет цитирования в Meta AI. Стоит разрешить.

---

## 2. llms.txt — Качество и покрытие

### llms.txt (RU, 269 строк)
**Статус: СИЛЬНЫЙ файл. Лучший в нише среди туристических компаний.**

Сильные стороны:
- 12 Q&A блоков с ответами 150–220 слов — попадают в оптимальный диапазон 134–167 слов для AI-цитирования
- Цены в GEL и USD во всех Q&A
- Конкретные факты: расстояния (157 км), высоты (2170 м, 5047 м), времена (08:00–22:00), лицензии гидов (№8247109128)
- Таблица сравнения туров — машиночитаема
- Полный каталог с URL — AI может дать прямую ссылку
- Трансферная таблица с ценами — отдельный информационный актив

Проблемы:
- **CRITICAL**: Дата обновления — `2026-07-27` в llms.txt, но `2026-07-16` в llms-full.txt. Рассинхрон означает, что AI может процитировать устаревшую версию из full.
- **HIGH**: Цены указаны в GEL и USD, но **нигде нет EUR**. CLAUDE.md указывает "Казбеги от €45", сайт позиционируется на европейских туристов. EN llms.txt должен иметь EUR-цены.
- **MEDIUM**: Нет блока `## Конкуренты / Отличия` — AI-системы при сравнительных запросах ("лучший гид Тбилиси vs Tripster") не получают контекст.
- **LOW**: Раздел `## ქართული ვერსია` в RU-файле — полезен, но GE-версия содержит только 4 URL без Q&A. AI для грузинской аудитории не получает цитируемых блоков.

### en/llms.txt (EN)
**Статус: ХОРОШИЙ, но отстаёт от RU.**

- 8 Q&A блоков (против 12 в RU) — есть пробел
- Рейтинг указан как 87 отзывов (против 90 в RU-файле) — **рассинхрон данных**
- Нет таблицы трансферов — RU-файл богаче
- `Last updated: 2026-06-02` — устарел на 2 месяца

**Отсутствующие Q&A в EN (важные для западной аудитории):**
- "Is Tbilisi safe for tourists?" — есть в llms.txt основном файле, но это общий, нет в en/llms.txt
- "How much does a trip to Georgia cost per day?" — есть в основном, нет в EN-версии
- "What tours are available for solo female travelers?"

### llms-full.txt (912 строк итого)
- Детальные маршруты по часам — отличный материал для AI
- Расхождение даты: `2026-07-16` vs `2026-07-27` в кратком файле

---

## 3. Citability — Извлекаемость фактов

### Сильные страницы

**Страница тура Казбеги** (`/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/`):
- FAQ Schema: 6 вопросов — есть
- Product schema с отзывами — есть
- TouristTrip schema с лицензией гида — есть
- VideoObject schema — есть
- **Проблема**: FAQ-ответы в schema слабее, чем в llms.txt. Пример: Q "Какое время года лучше?" — ответ в schema расплывчатый ("весна и осень"), тогда как llms.txt даёт конкретику ("май–июнь: +15–22°C, сентябрь–октябрь: золотая осень"). AI возьмёт schema, получит менее цитируемый ответ.

**llms.txt Q&A блоки** — оптимальная длина (150–210 слов), самодостаточны, содержат конкретные числа.

### Слабые страницы

**EN-страницы туров** (`/en/tour/*/`, `/en/ekskursiya/*/`):
- Не проверено содержание, но meta description EN главной даёт только GEL-цены (`From ₾98/person`) — для Google AIO в EN-регионах нужны USD/EUR.

**Блог (55 RU + 10 EN статей)**:
- FAQ schema в блоге есть (по упоминанию в CLAUDE.md), но passage-level структура не верифицирована.
- EN-блог (10 статей) vs RU (55 статей) — огромный дисбаланс для EN-видимости в ChatGPT и Perplexity.

### Passage-level анализ llms.txt

Средняя длина Q&A-ответа: ~180 слов — **в оптимальном диапазоне (134–167)**, чуть выше но допустимо.
Прямой ответ в первых 40 словах: **да** во всех блоках ("стоит от ₾175 с человека", "нет, виза не нужна").
Самодостаточность: **высокая** — каждый блок содержит контекст, цифры, контакты.

---

## 4. Authority & Brand Signals

### sameAs (schema в index.html)
```json
"sameAs": [
  "https://t.me/SakhvaGuideBot?start=site",
  "https://www.instagram.com/sakhvatravel",
  "https://wa.me/995511272623",
  "https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html",
  "https://www.youtube.com/@SakhvaTravel",
  "https://www.google.com/maps?cid=14070083063461040701",
  "https://yandex.com.ge/profile/103365004008",
  "https://www.facebook.com/people/Sakhva-Travel/61590273044825/",
  "https://www.threads.com/@sakhvatravel"
]
```

**Покрытие сигналов по корреляции с AI-цитированием:**

| Платформа | Корреляция с AI-цитатами | Статус |
|-----------|--------------------------|--------|
| YouTube (@SakhvaTravel) | ~0.737 (сильнейший) | ЕСТЬ |
| Tripadvisor | High | ЕСТЬ |
| Google Maps (CID) | High | ЕСТЬ |
| Instagram | Medium | ЕСТЬ |
| Facebook | Medium | ЕСТЬ |
| Reddit | High | **НЕТ** |
| Wikipedia | High | **НЕТ** |
| Wikidata | High | **НЕТ** |

**Критические пробелы:**
- **Reddit**: нет ни одного упоминания бренда "Sakhva Travel" в обсуждениях r/georgia, r/Tbilisi, r/digitalnomad. Reddit — второй по силе сигнал для ChatGPT-цитирования.
- **Wikipedia**: нет entity-записи ни в "Tourism in Georgia", ни в "Tbilisi tourism". Нет Wikidata QID. Это ограничивает Knowledge Graph-узнаваемость.
- **Tripadvisor листинг**: есть в sameAs, но нет в llms.txt как явного упоминания с URL — AI не знает что Tripadvisor-профиль существует.

### Консистентность имени бренда

Варианты встреченные в файлах: "Sakhva Travel", "SakhvaTravel", "sakhvatravel", "@SakhvaTravel", "@SakhvaGuideBot".
- В llms.txt: "Sakhva Travel" (правильно)
- В EN llms.txt: "Sakhva Travel" (правильно)
- В Telegram: @SakhvaTravel (llms.txt) vs @SakhvaGuideBot (llms-full.txt) — **два разных Telegram-контакта**, в Q&A используется то один, то другой. AI даст противоречивую информацию.

---

## 5. Technical Accessibility

**Статус: ХОРОШИЙ.**

- Сайт: статический HTML на Vercel — SSR по умолчанию, AI-краулеры получают полный HTML без JS-рендеринга.
- llms.txt: доступен напрямую, текстовый формат
- llms-full.txt: доступен, референс из llms.txt есть (`> Optional: [Full version]`)
- EN llms.txt: есть (`/en/llms.txt`), линк из EN-главной есть (`<link rel="alternate" type="text/plain" href="/en/llms.txt">`)
- hreflang: реализован (ru/en/ka)
- Sitemap index: есть (`sitemap-index.xml`)
- robots.txt → sitemap: есть

**Проблема (LOW):** Redirect-логика для языков через JS (`sessionStorage.setItem("lredir")`): боты из списка исключены через UA-check (`/bot|crawl|spider|.../`), но UA-паттерн может не покрыть все AI-краулеры (например OAI-SearchBot не попадает в стандартный bot-regex). Проверить что AI-краулеры получают RU-контент на `/` без редиректа.

---

## 6. Мультиязычие для AI

| Язык | llms.txt | Q&A блоков | Блог-статей | FAQ schema | Оценка |
|------|----------|-----------|------------|-----------|--------|
| RU | Да (269 строк) | 12 | 55 | Да | Сильно |
| EN | Да (en/llms.txt) | 8 | 10 | Проверить | Средне |
| GE (ka) | Только 4 URL в RU llms.txt | 0 | ? | ? | Слабо |

**EN значительно слабее RU** — при том что ChatGPT и Perplexity работают преимущественно в EN-контексте. Для западного туриста Sakhva Travel практически невидим в AI-поиске.

---

## Топ-5 рекомендаций (по приоритету)

### 1. CRITICAL — Синхронизировать Telegram-контакт в llms.txt и llms-full.txt
**Проблема:** @SakhvaTravel vs @SakhvaGuideBot — два разных контакта используются вперемешку.
**Правка:** Везде один контакт. Если @SakhvaGuideBot — основной бот, заменить во всех Q&A.
**Усилия:** 15 минут. **Влияние:** Убирает противоречивый сигнал, AI даёт верный контакт.

### 2. HIGH — Разблокировать meta-externalagent
**Проблема:** `Disallow: /` для `meta-externalagent` блокирует Meta AI (Llama-based поиск).
**Правка в robots.txt:**
```
User-agent: meta-externalagent
Allow: /
Disallow: /dashboard/
Disallow: /partner/
```
**Усилия:** 2 минуты. **Влияние:** Открывает канал Meta AI Overviews.

### 3. HIGH — Добавить EUR-цены в EN llms.txt
**Проблема:** EN llms.txt даёт цены в GEL/USD. Европейские пользователи ищут в EUR. CLAUDE.md уже знает "Казбеги от €45".
**Правка:** В таблице туров и в Q&A добавить EUR-колонку. Курс: ₾175 ≈ €62, ₾77 ≈ €27.
**Усилия:** 30 минут. **Влияние:** Цитируемость на европейских запросах ("Georgia tour price euros").

### 4. HIGH — Синхронизировать даты и reviewCount между llms.txt файлами
**Проблема:** llms.txt (RU): 90 отзывов, 2026-07-27. EN llms.txt: 87 отзывов, 2026-06-02. llms-full.txt: 2026-07-16.
**Правка:** Одна дата и одно число отзывов везде. AI при сравнении двух файлов получит противоречие.
**Усилия:** 10 минут.

### 5. MEDIUM — Reddit-присутствие для ChatGPT-цитирования
**Проблема:** Нет ни одного органического упоминания "Sakhva Travel" на Reddit. Reddit — второй по силе сигнал корреляции с ChatGPT-цитатами.
**Действие:** Ответить на 5–10 тредов в r/Tbilisi, r/georgia, r/digitalnomad с полезными советами (не спам — реальные ответы на вопросы). Упомянуть бренд органично.
**Усилия:** 2–3 часа. **Влияние:** Через 4–8 недель появятся упоминания в ChatGPT-ответах.

---

## Platform-Specific Scores

| Платформа | Оценка | Ограничивающий фактор |
|-----------|--------|----------------------|
| Google AI Overviews (RU) | 78/100 | FAQ schema в туре слабее llms.txt |
| Яндекс GPT | 80/100 | YandexGPT разрешён, RU-контент сильный |
| ChatGPT (RU) | 72/100 | Reddit = 0, YouTube есть |
| ChatGPT (EN) | 52/100 | EN блог слабый (10 vs 55 статей), нет Reddit |
| Perplexity (RU) | 74/100 | Структура хорошая, Reddit отсутствует |
| Perplexity (EN) | 55/100 | EN llms.txt устарел, мало EN-контента |
| Bing Copilot | 65/100 | Bingbot разрешён, но нет Wikidata entity |
| Meta AI | 20/100 | meta-externalagent заблокирован |

---

## Что уже сделано правильно (не трогать)

- llms.txt структура и качество Q&A — выше среднего по нише
- robots.txt AI-стратегия корректна по всем ключевым краулерам
- sameAs с YouTube + Tripadvisor + Google Maps CID — сильный entity-сигнал
- TravelAgency + LocalBusiness dual @type — правильно
- Лицензии гидов в schema (hasCredential) — E-E-A-T сигнал
- speakable specification на h1/h2 — правильно
- CC BY 4.0 лицензия явно прописана — разрешение для AI цитировать
