# GEO Audit — Sakhva Travel
Date: 2026-08-08

## GEO Readiness Score: 71/100

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Citability | 68/100 | 25% | 17.0 |
| Structural Readability | 80/100 | 20% | 16.0 |
| Multi-Modal Content | 65/100 | 15% | 9.75 |
| Authority & Brand Signals | 78/100 | 20% | 15.6 |
| Technical Accessibility | 95/100 | 20% | 19.0 |
| **Total** | | | **77.35 → 77** |

Скорректировано до 71 с учётом критических дефицитов цитируемости на коммерческих EN-страницах.

---

## 1. AI Crawler Access (robots.txt)

Status: PASS

| Crawler | Status |
|---------|--------|
| GPTBot | Allow / |
| OAI-SearchBot | Allow / |
| ChatGPT-User | Allow / |
| ClaudeBot | Allow / |
| Claude-Web | Allow / |
| PerplexityBot | Allow / |
| Google-Extended | Allow / |
| GoogleOther | Allow / |
| YandexGPT | Allow / |
| AppleBot | Allow / |
| Applebot-Extended | Allow / |
| CCBot | Disallow / (training block — корректно) |
| cohere-ai | Disallow / (training block — корректно) |
| anthropic-ai | Allow / (аномалия: обычно блокируют как training-only, но не критично) |

Все AI search crawlers открыты. Конфигурация близка к идеалу.

---

## 2. llms.txt

Status: PRESENT, хорошее качество — но есть пробелы

Файл: `/llms.txt` (270 строк), ссылка на `llms-full.txt`.

**Плюсы:**
- Быстрые факты в machine-readable формате (цена, длительность, группа, рейтинг)
- Таблица сравнения 12 туров с ценами GEL/USD — идеально для AI-цитирования
- 8 Q&A на русском, 8 Q&A на английском — прямые ответы на коммерческие вопросы
- Таблица трансферов (маршрут / расстояние / время / цена)
- Лицензия CC BY 4.0 явно указана

**Минусы:**
- Нет RSL 1.0 / явного разрешения на коммерческое переиспользование AI-системами
- EN-версия FAQ покрывает общие вопросы (виза, безопасность), но не конкретные туры из EN-каталога (Gomis Mta, Batumi transfers)
- Каталог ссылается на `/tours/` и `/en/tours/`, но реальные EN хабы — `/en/tours-in-georgia/` (расхождение URL)
- Нет упоминания конкретных цен для Gomis Mta (₾220), Kutaisi tours (₾165/195)

---

## 3. Citability — анализ карточек экскурсий

### RU: ekskursiya-kakheti-iz-tbilisi — Score: 75/100

**Сильные стороны:**
- Hero stats: цена (от ₾170), длительность (10–12 ч), группа (до 7), выезд (09:00) — в первых 50 словах экрана
- Facts box с 4 параметрами (Длительность 11ч / Группа до 7 / Выезд 08:00 / Отмена 24ч)
- Блок "Включено / Не включено" — четкий список, извлекаемый без контекста
- FAQ schema (FAQPage JSON-LD) — 6 вопросов: длительность, возраст, погода, дегустация, обед, размер группы
- Product schema с price=170, priceCurrency=GEL, aggregateRating 4.9/30
- Маршрут по часам (route-grid) с временными метками

**Проблемы:**
- Первый абзац body (`<p>Кахетия — главный винодельческий регион...`) — описательный, не отвечает на коммерческий вопрос. AI не получит прямой ответ "сколько стоит / что включено" из первых 60 слов текста
- FAQ вопросы generic (возраст, погода) вместо коммерческих: "Сколько стоит тур в Кахетию из Тбилиси?", "Что входит в стоимость ₾170?"
- Длина FAQ-ответов: 1–2 предложения — ниже оптимального диапазона 134–167 слов для AI-цитирования
- Раздел "Подробный маршрут" (строки 373–375) — дублирующий абзац, плохо структурированный, не несёт дополнительной информации. Dilutes signal.
- Нет явного H2 "Сколько стоит экскурсия в Кахетию?" — коммерческий anchor отсутствует

### EN: ekskursiya-gomis-mta-iz-batumi — Score: 55/100

**Сильные стороны:**
- Hero stats: from ₾220 / 8–9h / up to 7 / 08:00 departure / 24h free cancellation
- Included/Not included grid — четкий, извлекаемый
- Маршрут по часам с описаниями точек
- Product schema price=220, aggregateRating 4.9/35

**Критические проблемы:**
- FAQ schema: только 3 вопроса — "special preparation", "where does it depart", "how is it different from city tour". НИ ОДНОГО коммерческого вопроса: "How much does Gomis Mta tour cost?", "What's included?", "How to book?"
- Первый абзац описательный, нет прямого ответа на "day trip from Batumi"
- Нет явного passage-level ответа формата: "The Gomis Mta tour from Batumi costs ₾220 per person. The tour runs 8–9 hours..." — extractable без контекста
- "Timur's tip" раздел указывает "Timur" как гида, но Gomis Mta ведёт гид Саба — фактическая ошибка, снижает E-E-A-T

---

## 4. Authority & Entity Signals

### Organization Schema (index.html)
- Type: TravelAgency + LocalBusiness — PASS
- legalName: "ИП Сахвадзе Т.В." — PASS
- address с координатами — PASS
- aggregateRating: 4.9 / 90 reviews — PASS
- openingHoursSpecification — PASS
- priceRange — PASS

### sameAs (index.html)
- YouTube: `https://www.youtube.com/@SakhvaTravel` — PASS (сильнейший сигнал, correlation ~0.737)
- TripAdvisor: присутствует — PASS
- Google Maps CID: присутствует — PASS
- Instagram, Facebook, Threads, Telegram — PASS
- **Wikipedia: ОТСУТСТВУЕТ** — значимый gap для AI confidence
- **Wikidata: ОТСУТСТВУЕТ**

### На карточках туров
- TouristTrip schema с author (Person с license) — PASS
- Speakable spec (h1, h2) — PASS
- hreflang RU/EN/GE — PASS

### Что отсутствует
- Нет Review/Testimonial schema с именами рецензентов на страницах туров
- Нет упоминания лицензии на EN Gomis Mta странице в тексте (только в schema)
- Person schema для Саба отсутствует на EN страницах Batumi туров

---

## 5. Structural Readability для AI

### Что работает
- Статический SSR HTML — AI crawlers получают полный контент без JS
- Семантические H1/H2/H3 с правильной иерархией
- route-grid (маршрут по часам) хорошо структурирован
- Includes/Excludes boxes — идеальный формат для извлечения
- Таблицы в llms.txt — оптимальны

### Что мешает
- CSS-анимации `[]{transform:translateY(40px)}` в inline style — шум в HTML для парсера
- Google Maps script (600+ строк JS) в теле страницы увеличивает noise ratio
- Дублирующие параграфы ("Смотрите также" ×3 подряд на Кахетии) — dilute content density
- На EN Gomis Mta нет facts-box (зелёный блок с параметрами) — есть только в hero stats

---

## 6. Platform-Specific Assessment

| Platform | Score | Причина |
|----------|-------|---------|
| Google AIO (RU) | 65/100 | FAQ schema есть, но вопросы не коммерческие; первый абзац описательный |
| Google AIO (EN) | 45/100 | 3 FAQ вопроса, нет passage с прямым ответом на "day trip from Batumi" |
| ChatGPT | 70/100 | llms.txt хороший, RU Q&A сильные; EN карточки слабые |
| Perplexity | 72/100 | SSR + structured data хорошие; YouTube sameAs помогает |
| Bing Copilot | 68/100 | BingSiteAuth.xml есть; Product schema с ценой работает |

---

## Top 5 действий (приоритет по impact/effort)

### 1. КРИТИЧНО: Добавить "Answer Block" в первые 60 слов каждой EN карточки
**Impact: HIGH | Effort: LOW**

Текущий первый абзац Gomis Mta: описание природы.
Нужно: прямой ответ на коммерческий запрос как первый абзац.

Пример для Gomis Mta:
```
The Gomis Mta tour from Batumi costs ₾220 per person and runs 8–9 hours. 
Departure at 08:00 from your Batumi hotel. The route covers Gomis Mta summit 
(2755 m) and Machakhela Gorge — no other tourists, 4WD required. Private group, 
up to 7 people. Free cancellation 24 hours in advance. Guide: Saba, 10 years 
experience in Adjara region. Book via WhatsApp +995 511 272 623.
```
Это 67 слов — самодостаточный AI-цитируемый пассаж.

### 2. КРИТИЧНО: Расширить FAQ до 6–8 коммерческих вопросов на EN карточках
**Impact: HIGH | Effort: MEDIUM**

Gomis Mta сейчас: 3 вопроса, 0 коммерческих.
Добавить:
- "How much does the Gomis Mta tour from Batumi cost?" → ₾220/person, group up to 7
- "What is included in the Batumi mountain tour?" → 4WD, private guide Saba, pick-up/drop-off
- "How do I book a day trip from Batumi?" → WhatsApp +995 511 272 623, answer in 15 min
- "Is the Gomis Mta tour suitable for beginners?" → No technical climbing, comfortable shoes sufficient

Обновить FAQPage JSON-LD синхронно.

### 3. ВАЖНО: Добавить коммерческий H2 с вопросом и ценой на все карточки
**Impact: HIGH | Effort: LOW**

Добавить секцию сразу после hero stats:

RU (Кахетия): `<h2>Сколько стоит экскурсия в Кахетию из Тбилиси?</h2>` + абзац 134–167 слов с ценой, что включено, как забронировать.

EN (Gomis Mta): `<h2>How much does a day trip to Gomis Mta from Batumi cost?</h2>` + self-contained passage.

AI-системы триггерятся на question-based H2 → вероятность цитирования резко выше.

### 4. ВАЖНО: Исправить фактическую ошибку + добавить Person schema для Саба на EN Batumi страницах
**Impact: MEDIUM | Effort: LOW**

На `en/ekskursiya/ekskursiya-gomis-mta-iz-batumi/`: раздел "Timur's tip" — гида зовут Саба, не Тимур. Исправить текст и заголовок на "Saba's tip".

Добавить в TouristTrip schema:
```json
"author": {"@type":"Person","name":"Saba","jobTitle":"Batumi Guide",
  "hasCredential":{"@type":"EducationalOccupationalCredential",
  "name":"Guide license No. 9332412411"}}
```

### 5. ВАЖНО: Обогатить llms.txt EN-секцию конкретными ценами новых туров
**Impact: MEDIUM | Effort: LOW**

В llms.txt отсутствуют:
- Gomis Mta tour: ₾220 / 8–9h / guide Saba
- Kutaisi tours (₾165, ₾195)
- Таблица сравнения EN-туров аналогично RU-таблице

Также исправить URL: каталог ссылается на `/en/tours/`, правильный URL `/en/tours-in-georgia/`.

---

## Дополнительные наблюдения

**Что уже хорошо сделано (не трогать):**
- robots.txt — эталонная конфигурация для AI crawlers
- sameAs с YouTube — самый сильный сигнал AI-цитируемости
- TravelAgency + LocalBusiness + TouristTrip + Product schema на всех страницах
- SSR статический HTML — 100% доступен AI без JS
- llms.txt RU Q&A — ответы 200–400 слов, оптимальный диапазон

**Что требует отдельного решения (не входит в топ-5):**
- Wikipedia/Wikidata entity — создание требует нотабельности, не быстрый фикс
- Дублирующие параграфы на Кахетии (строки 373–375 в HTML) — удалить при следующей правке
- Review schema с именами рецензентов — возможно после накопления 50+ отзывов с именами
