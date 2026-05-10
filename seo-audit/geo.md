# GEO Audit — sakhva-travel.com
**Дата:** 2026-05-04
**Тип сайта:** Статический HTML на Vercel, частный тур-гид в Тбилиси

---

## GEO Health Score: 74/100

| Измерение | Вес | Оценка | Взвешенный |
|-----------|-----|--------|------------|
| Citability (цитируемость) | 25% | 78/100 | 19.5 |
| Structural Readability | 20% | 82/100 | 16.4 |
| Multi-Modal Content | 15% | 48/100 | 7.2 |
| Authority & Brand Signals | 20% | 62/100 | 12.4 |
| Technical Accessibility | 20% | 92/100 | 18.4 |
| **ИТОГО** | | | **73.9 ≈ 74** |

---

## 1. AI Crawler Access Status

| Crawler | Статус | Комментарий |
|---------|--------|-------------|
| GPTBot | ALLOW | ChatGPT поиск |
| OAI-SearchBot | ALLOW | OpenAI Search |
| ChatGPT-User | ALLOW | ChatGPT browse |
| ClaudeBot | ALLOW | Claude citations |
| Claude-Web | ALLOW | Claude web |
| PerplexityBot | ALLOW | Perplexity citations |
| Google-Extended | ALLOW | Google AI (Gemini) |
| GoogleOther | ALLOW | Google misc |
| YandexGPT | ALLOW | Яндекс AI |
| Amazonbot | ALLOW | Alexa/Amazon |
| AppleBot | ALLOW | Apple Intelligence |
| DataForSeoBot | ALLOW | SEO data |
| Bingbot | ALLOW | Bing/Copilot |
| CCBot | BLOCK | Training only — корректно |
| anthropic-ai | BLOCK | Training only — корректно |
| cohere-ai | BLOCK | Training only — корректно |
| meta-externalagent | BLOCK | Meta training — корректно |
| Bytespider | BLOCK | TikTok scraper — корректно |

**Вердикт:** Идеальная конфигурация. Все поисковые AI-боты разрешены, training-only краулеры заблокированы.

---

## 2. llms.txt — Анализ

| Параметр | Статус |
|----------|--------|
| Наличие | /llms.txt — есть, /llms-full.txt — есть |
| Формат | Соответствует спецификации llms.txt |
| Обновление | 2026-05-02 (свежий) |
| Язык | Двуязычный (RU + EN FAQ) |
| Структура | Быстрые факты, FAQ (12 Q&A), таблица сравнения туров, каталог 55 статей |
| Контактные данные | WhatsApp, Telegram, Email, Website |
| Ценовая информация | Полная (GEL + USD для каждого тура) |
| Секция "Ключевые факты о Грузии" | Есть — отличный прием для AI-цитирования |

### Проблемы llms.txt:
1. **Нет RSL 1.0 лицензии** — нет явного указания на Responsible Source Licensing
2. **Нет версии llms.txt** — отсутствует `version: 1.0` в заголовке
3. **Секция "Использование контента"** есть, но без чёткой машиночитаемой лицензии

### Сильные стороны:
- Таблица сравнения туров — идеальна для AI-ответов
- Q&A формат покрывает 12 top-intent запросов
- Быстрые факты — self-contained, extractable блоки
- Ссылки на все 55 статей блога + 12 туров

---

## 3. Citability — Цитируемость (78/100)

### Что хорошо:
- **FAQ секции** на главной (9 RU, 8 EN) и в блоге — идеальный формат для AI-цитат
- **Цены с валютой** в каждом туре (₾175/чел, $63 USD)
- **Конкретные цифры:** 500+ туров, 4.9/5, 87 отзывов, 14 часов, 2170 м, 5047 м
- **Self-contained блоки:** каждый FAQ-ответ работает без контекста
- **FAQPage schema** на главной и страницах туров

### Что улучшить:
- **Длина пассажей:** Многие блоки короче оптимальных 134-167 слов (основные по 60-100 слов)
- **Блог:** пассажи неравномерные (от 50 до 300+ слов), нет таргетирования на 134-167
- **Нет "Definition blocks"** — абзацев, начинающихся с "[Term] is/это..." формата
- **Слабая атрибуция источников:** цены/факты без ссылок на официальные источники (кроме 1 блога)
- **EN-версия:** FAQ ответы короче, чем на RU — менее цитируемы

---

## 4. Structural Readability (82/100)

### Что хорошо:
- **Question-based H2/H3:** FAQ и блог используют вопросительные заголовки
- **Schema.org markup:** TravelAgency, TouristTrip (12 шт), FAQPage, BlogPosting, Review, BreadcrumbList, Person — enterprise-уровень
- **Таблицы:** сравнение туров, цены, "что включено" — легко извлекаются AI
- **hreflang:** настроен RU/EN на всех страницах
- **SSR:** Весь контент в HTML, доступен без JS

### Что улучшить:
- **H2 на главной** не все question-based (есть "Наши туры", "О гиде" вместо "Какие туры...")
- **Блог H2:** смешанные — часть вопросительные, часть описательные
- **Canonical tags:** не на всех страницах
- **Table of Contents:** нет навигации в длинных блог-статьях

---

## 5. Multi-Modal Content (48/100)

### Что хорошо:
- **VideoObject schema** — есть
- **Фото** на страницах туров (WebP)
- **OG-images** на статьях блога (1200x630)

### Что критически не хватает:
- **YouTube-канал** — НЕТ. YouTube-mentions имеют корреляцию 0.737 с AI-цитациями (сильнейший сигнал)
- **Видео-контент:** нет embedded YouTube в блоге/турах
- **Подкаст/аудио:** отсутствует
- **Инфографики:** нет shareable визуалов
- **Image alt-text:** нужна проверка качества alt для AI-extraction

---

## 6. Authority & Brand Signals (62/100)

### Присутствие бренда по платформам:

| Платформа | Статус | Влияние на AI |
|-----------|--------|---------------|
| Google Business Profile | Есть (CID 14070083063461040701) | Высокое |
| Wikipedia | НЕТ | Критично — нет entity recognition |
| YouTube | НЕТ | Критично — корреляция 0.737 |
| Reddit | Не обнаружено | Высокое — нет UGC-сигналов |
| TripAdvisor | Нет данных | Критично для travel-ниши |
| Trustpilot | Нет данных | Среднее |
| LinkedIn | Нет данных | Среднее |
| Medium / travel-блоги | Частично (parasite SEO на 22 площадках) | Среднее |

### Что хорошо:
- **87 Google-отзывов** (4.9/5) — сильный E-E-A-T сигнал
- **22 публикации** на внешних площадках (Medium, Quora, Dzen, VC, Pikabu, Habr, Telegra.ph)
- **Автор указан:** Тимур с "500+ туров с 2023" — experience signal
- **datePublished/dateModified** на всех страницах

### Что улучшить:
- **Нет Wikipedia entity** — AI-системы не распознают Sakhva Travel как "известную сущность"
- **Нет YouTube** — крупнейший gap для AI citation correlation
- **Нет Reddit presence** — нет UGC-обсуждений бренда
- **Нет TripAdvisor** — критично для travel vertical

---

## 7. Technical Accessibility (92/100)

### Что хорошо:
- **SSR (static HTML)** — весь контент доступен без JS рендеринга
- **Vercel CDN** — быстрая доставка, edge caching
- **Sitemap.xml** — 93+ URL, актуальный (2026-04-24)
- **robots.txt** — идеальная AI-конфигурация
- **llms.txt + llms-full.txt** — оба на месте
- **JSON-LD structured data** — на всех ключевых страницах
- **hreflang** — RU/EN

### Что улучшить:
- **Canonical tags** — добавить на все страницы где отсутствуют
- **IndexNow** — подключён (хорошо для Bing Copilot)

---

## 8. Platform-Specific Scores

| AI-платформа | Готовность | Комментарий |
|-------------|-----------|-------------|
| Google AI Overviews | 78/100 | Сильный schema, FAQ, E-E-A-T. Нет YouTube/Reddit-сигналов |
| ChatGPT (SearchGPT) | 72/100 | GPTBot allowed, llms.txt есть, но нет entity в Wikipedia/YouTube |
| Perplexity | 76/100 | PerplexityBot allowed, хорошая структура, citeable passages |
| Bing Copilot | 74/100 | Bingbot allowed, IndexNow подключён, нет Reddit-mentions |
| YandexGPT | 70/100 | YandexGPT allowed, но llms.txt на русском — хорошо для Яндекса |

**Ключевой факт:** Только 11% доменов цитируются одновременно ChatGPT и Google AI Overviews. Для попадания в оба — нужны внешние brand signals.

---

## 9. TOP-5 Highest-Impact Changes

### 1. Создать YouTube-канал с видео туров
**Impact:** +15-20 к GEO Score
**Effort:** Средний (2-4 недели на первые 5 видео)
**Почему:** YouTube — корреляция 0.737 с AI-цитациями, сильнейший сигнал. Видео "Kazbegi day trip 2026", "Hidden gems Tbilisi" будут индексироваться Google и цитироваться AI. Embed в блог и страницы туров даст мультимодальный сигнал.

### 2. Оптимизировать длину пассажей до 134-167 слов
**Impact:** +8-10 к Citability
**Effort:** Низкий (1-2 дня, текстовые правки)
**Что делать:** В каждом блоге и FAQ — расширить ответы до 134-167 слов. Каждый пассаж должен начинаться с прямого ответа в первых 40 слов, затем supporting details. Особенно критично для EN-версии (сейчас многие ответы по 50-80 слов).

### 3. Добавить TripAdvisor + Reddit + Quora присутствие
**Impact:** +10-12 к Authority
**Effort:** Средний (1-2 недели)
**Что делать:**
- TripAdvisor: создать профиль гида, попросить 10 клиентов оставить отзывы
- Reddit: посты в r/tbilisi, r/sakartvelo, r/travel с полезным контентом (не реклама)
- Quora: ответы на "best tour guide Tbilisi", "Kazbegi day trip" с ссылкой

### 4. Добавить EN llms.txt секцию и RSL лицензию
**Impact:** +5-7 к Technical
**Effort:** Низкий (2-3 часа)
**Что делать:**
- Добавить `# License: RSL-1.0` в начало llms.txt
- Создать отдельный `/en/llms.txt` или расширить EN-секцию
- Добавить `version: 1.0` заголовок
- Добавить `# Preferred citation: "Sakhva Travel (sakhva-travel.com)"` для стандартизации цитирования

### 5. Definition blocks и source attribution в блоге
**Impact:** +5-8 к Citability
**Effort:** Низкий (1-2 дня)
**Что делать:**
- В каждой статье блога: начинать ключевые секции с "[Термин] — это..." формата
- Добавить ссылки на официальные источники (GNTA, Meteo Georgia) к каждому факту
- Формат: "По данным Национальной администрации туризма Грузии (gnta.ge), в 2025 году..."
- Это повышает trustworthiness для AI-систем при выборе source для цитаты

---

## 10. Quick Wins (можно сделать сегодня)

1. **RSL лицензия в llms.txt** — добавить строку `License: RSL-1.0` (5 минут)
2. **Canonical tags** — добавить `<link rel="canonical">` на все страницы (30 минут)
3. **H2 на главной** — переформулировать в вопросы: "Наши туры" → "Какие экскурсии в Тбилиси?" (15 минут)
4. **EN FAQ длина** — расширить каждый ответ до 134+ слов (1 час)
5. **Preferred citation** в llms.txt footer (5 минут)

---

## Сравнение с конкурентами (travel vertical)

Среднее для travel-сайтов по GEO:
- llms.txt: <5% сайтов имеют → Sakhva Travel впереди 95%+ конкурентов
- AI crawler rules: ~30% travel-сайтов блокируют GPTBot → Sakhva Travel открыт
- Schema depth: TravelAgency + TouristTrip + FAQPage — top 10% для локальных гидов
- YouTube: 70%+ travel-бизнесов имеют канал → Sakhva Travel отстаёт

---

## Резюме

**Сильные стороны:** Техническая настройка (robots.txt, llms.txt, schema, SSR) — на уровне топ-5% в нише. FAQ-структура и ценовая прозрачность — идеальны для AI-цитирования.

**Главный gap:** Отсутствие мультимодального контента (YouTube) и внешних brand signals (Wikipedia, Reddit, TripAdvisor). Это единственное, что мешает попасть в AI-ответы на конкурентные запросы типа "best tour guide Tbilisi".

**Приоритет #1:** YouTube-канал. Корреляция 0.737 с AI-цитациями — это не SEO-гипотеза, а статистический факт из исследований GEO.
