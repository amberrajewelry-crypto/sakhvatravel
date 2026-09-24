# GEO Audit — sakhva-travel.com
_Date: 2026-08-13_

---

## GEO Readiness Score: 74 / 100

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Citability | 25% | 72 | 18.0 |
| Structural Readability | 20% | 80 | 16.0 |
| Multi-Modal Content | 15% | 65 | 9.75 |
| Authority & Brand Signals | 20% | 78 | 15.6 |
| Technical Accessibility | 20% | 73 | 14.6 |
| **Total** | | | **73.95 → 74** |

---

## 1. AI Crawler Access — robots.txt

**PASS: все ключевые AI-краулеры явно разрешены**

| Crawler | Status | Примечание |
|---------|--------|-----------|
| GPTBot | ALLOWED | |
| ChatGPT-User | ALLOWED | |
| OAI-SearchBot | ALLOWED | |
| ClaudeBot | ALLOWED | |
| Claude-Web | ALLOWED | |
| PerplexityBot | ALLOWED | |
| Google-Extended | ALLOWED | |
| YandexGPT | ALLOWED | |
| Amazonbot | ALLOWED | |
| AppleBot / Applebot-Extended | ALLOWED | |
| meta-externalagent | ALLOWED | |
| CCBot | BLOCKED | правильно — training only |
| cohere-ai | BLOCKED | правильно |
| anthropic-ai | ALLOWED | аномалия: это training crawler Anthropic, логичнее заблокировать рядом с CCBot |

**Риск:** robots.txt разрешает, но Cloudflare Bot Fight Mode может блокировать на уровне WAF независимо от robots.txt. Проверить в Cloudflare dashboard что AI-боты не попадают под challenge.

---

## 2. llms.txt / llms-full.txt

**ПРИСУТСТВУЕТ. Структура корректна. Есть критические проблемы с URL.**

- Размер: 3719 слов (llms.txt), полная версия в llms-full.txt — ссылка присутствует
- Лицензия: CC BY 4.0 — прописана явно, AI-системы понимают
- RSL 1.0: отсутствует (не блокер, CC BY 4.0 достаточно)
- Last updated: 2026-08-05 (8 дней назад — обновить)

### [CRITICAL] 5 URL в llms.txt — 301 редиректы

AI-краулеры не обязаны следовать редиректам при парсинге llms.txt. Все ссылки должны быть каноническими.

| URL в llms.txt | Реальный канонический URL |
|----------------|--------------------------|
| `/tours/` | `/ekskursiya/` |
| `/en/tours/` | `/en/tours-in-georgia/` |
| `/tour/tbilisi-hidden/` | `/ekskursiya/ekskursiya-stary-tbilisi/` |
| `/tour/batumi/` | `/ekskursiya/tur-batumi-iz-tbilisi/` |
| `/tour/emigrant/` | `/ekskursiya/tur-dlya-emigrantov-tbilisi/` |

Дополнительно: `/tour/tbilisi-hidden/` редиректит на "Старый Тбилиси", тогда как в тексте llms.txt описание для "Скрытые места" — это разные туры. Несоответствие контента.

Те же URL дублируются в llms-full.txt — исправить в обоих файлах.

### Passage-level анализ Q&A блоков (оптимум 134-167 слов)

| Q&A блок | Слов | Статус |
|----------|------|--------|
| Казбеги — цена 2026 | 148 | OPTIMAL |
| Тбилиси — экскурсия цена | 144 | OPTIMAL |
| Виза в Грузию | 118 | ок |
| Когда ехать в Казбеги | 121 | ок |
| Как забронировать | 103 | ок |
| Индивидуальный vs автобусный | 114 | ок |
| Туры для эмигрантов | 120 | ок |
| Отмена тура | 99 | ок |
| Языки гида | 86 | ок |
| Туры для детей | 110 | ок |
| Кто ведёт Батуми/Сванетия | 70 | SHORT |
| Тур в Сванетию — цена | 70 | SHORT |
| Тур в Батуми — цена | 51 | SHORT |
| Как добраться Тбилиси → Батуми | 38 | **SHORT — критично** |

22 из 24 блоков ниже оптимальных 134 слов. Только 2 блока в оптимальной зоне. AI-системы предпочитают самодостаточные пассажи 134-167 слов — они цитируются значительно чаще коротких.

---

## 3. Citability — on-page структура

### Главная страница

| Сигнал | Статус |
|--------|--------|
| SpeakableSpecification | PRESENT (`cssSelector: ["h1","h2"]`) |
| FAQPage schema | PRESENT (4 вопроса) |
| Person schema (Тимур) | PRESENT (`@id`, лицензия №8247109128, `worksFor`, `hasCredential`) |
| TravelAgency + LocalBusiness | PRESENT (aggregateRating 4.9/90) |
| Wikidata sameAs для мест | PRESENT (Тбилиси Q994, Казбеги Q210019, Кахетия Q193261, Грузия Q230) |

**Проблема: H2-заголовки нарративные, не вопросные.**
Из 18 заголовков H2/H3 на главной только 2 сформулированы как вопросы. Примеры нарративных: "Каталог — 71 маршрут с ценами", "Почему выбирают Sakhva Travel?", "Откуда мы возим — 10 регионов Грузии". AI Overviews и Featured Snippets привязываются к вопросным заголовкам (What/How/When/Сколько/Как/Когда).

**Проблема: Саба отсутствует в @graph главной.**
JSON-LD главной содержит только Тимура как Person. Запросы о турах по западной Грузии, Батуми, Сванетии — AI не видит гида Сабу через главную страницу.

### Страницы туров (проверено: Казбеги)

| Сигнал | Статус |
|--------|--------|
| TouristTrip | PRESENT |
| FAQPage | PRESENT (6 вопросов) |
| BreadcrumbList | PRESENT |
| VideoObject | PRESENT |
| SpeakableSpecification | PRESENT |

**Проблема: FAQ-ответы на странице короткие и слабые.**

Примеры ответов в on-page FAQPage:
- "Лучшее время — весна и осень, когда погода комфортная и природа радует яркими красками." — 21 слово. Не цитируется.
- "Да, рекомендуется заранее забронировать экскурсию, особенно в высокий сезон." — 12 слов. Банально.
- "Экскурсия подходит для людей разных возрастов." — 7 слов.

В llms.txt те же вопросы раскрыты в 100-150 слов с конкретикой. Разрыв огромный. On-page FAQ — именно то, что сканирует Google для AI Overviews. llms.txt — для ChatGPT/Perplexity. Нужен паритет.

### Blog posts (проверено: blog/viza-v-gruziyu-2026/)

| Сигнал | Статус |
|--------|--------|
| BlogPosting | PRESENT |
| FAQPage | PRESENT |
| BreadcrumbList | PRESENT |
| Первый параграф с прямым ответом | PRESENT (76 слов) — хорошо |
| author → Person ссылка | НЕ ПРОВЕРЕНО — риск отсутствия |

---

## 4. Authority & Brand Signals

| Канал | В sameAs | Активность |
|-------|---------|-----------|
| YouTube `@SakhvaTravel` | PRESENT (Person + Business) | не проверялась |
| TripAdvisor | PRESENT (Business) | реальная страница |
| Google Maps CID | PRESENT | верифицирован |
| Instagram | PRESENT | |
| Facebook | PRESENT | |
| Яндекс Бизнес | PRESENT | |
| Telegram | PRESENT | |
| **Wikipedia** | **ОТСУТСТВУЕТ** | нет статьи (ожидаемо) |
| **Reddit** | **ОТСУТСТВУЕТ** | нет ни в sameAs, ни упоминаний |

**Ключевой gap: Reddit.** По данным корреляционных исследований, Reddit-упоминания — второй по силе сигнал для ChatGPT-цитируемости (после YouTube ~0.737). Sakhva Travel не упоминается в r/Tbilisi, r/georgia, r/digitalnomad. ChatGPT и Perplexity активно тянут из Reddit при ответах на travel-запросы.

**YouTube — сильнейший сигнал (корреляция ~0.737) присутствует в sameAs** — убедиться что канал `@SakhvaTravel` активен и содержит видео с названиями туров.

---

## 5. Technical Accessibility

- Рендеринг: статический HTML (359 KB), SSR — контент доступен без JS. Хорошо.
- JSON-LD: встроен в `<head>`, парсится при первом обходе. Хорошо.
- robots.txt: Sitemap указан (`sitemap-index.xml`). Хорошо.
- llms.txt/llms-full.txt: доступны по стандартным URL. Хорошо.

**Риск: Cloudflare WAF vs AI-краулеры.** robots.txt разрешает, но если включён Bot Fight Mode или Super Bot Fight Mode в Cloudflare — реальные запросы от GPTBot/ClaudeBot могут получать 403/JS challenge. Это не видно в robots.txt, но блокирует обход.

---

## 6. Platform-Specific Scores

| Платформа | Оценка | Главная проблема |
|-----------|--------|-----------------|
| Google AI Overviews | 70/100 | On-page FAQ слабые; Speakable есть |
| ChatGPT | 74/100 | llms.txt есть; 5 битых URL; мало OPTIMAL-пассажей |
| Perplexity | 76/100 | Структура хорошая; нет Reddit-сигнала |
| Bing Copilot | 68/100 | Bingbot разрешён; EN FAQ слабее RU |

---

## TOP-5 Приоритетных Fixes

### 1. [CRITICAL] Исправить 5 URL в llms.txt и llms-full.txt
**Effort: 15 минут**

Заменить редирект-URL на канонические (список выше). Заодно исправить описание `/tour/tbilisi-hidden/` — оно описывает "Скрытые места", а редирект ведёт на "Старый Тбилиси". Либо поставить правильный URL скрытых мест, либо исправить описание.

### 2. [HIGH] Расширить Q&A блоки в llms.txt до 134+ слов
**Effort: 2 часа**

Приоритет — 4 блока ниже 70 слов: Батуми→как добраться (38w), Батуми→цена тура (51w), Батуми/Сванетия→кто ведёт (70w), Сванетия→цена (70w). Паттерн: прямой ответ (1-2 предложения) → детали с конкретикой → сравнение с альтернативами → совет + контакт.

### 3. [HIGH] Добавить Сабу в @graph главной страницы
**Effort: 20 минут**

В JSON-LD `index.html` добавить второй `Person`-узел `@id: "#guide-saba"` с `worksFor`, `hasCredential` (лицензия №9332412411), `knowsAbout` (Батуми, Аджария, Сванетия), `knowsLanguage: [ru, en, ka]`. Ссылку дать из Business-узла через `employee`.

### 4. [HIGH] Углубить on-page FAQPage на страницах туров
**Effort: 1 час на тур**

Минимум 80-120 слов на каждый FAQ-ответ. Образец — уже написанные ответы в llms.txt. Скопировать логику оттуда в FAQ-схему страниц. Приоритет: Казбеги (самая трафиковая страница), затем Кахетия, Тбилиси.

### 5. [MEDIUM] Reddit-присутствие
**Effort: 2-3 часа разово**

Полезные посты/ответы (не реклама) в:
- `r/Tbilisi` — практические советы по экскурсиям, ответы на вопросы о Казбеги
- `r/digitalnomad` — тур для цифровых кочевников в Тбилиси
- `r/georgia` (страна) — FAQ по визам, ценам, когда ехать

Органическое упоминание sakhva-travel.com в Reddit-постах — второй по силе сигнал для ChatGPT-цитируемости.

---

## Дополнительные находки

**[LOW] anthropic-ai — Allow в robots.txt:** это training crawler Anthropic (не поисковый). Если нет цели попасть в обучающие данные следующих версий Claude — заблокировать рядом с CCBot. Не влияет на цитируемость в AI-поиске.

**[LOW] llms.txt Last-Modified HTTP-заголовок:** проверить что Vercel отдаёт корректный `Last-Modified` для llms.txt. AI-краулеры используют кеш-заголовки для планирования переобхода. Если заголовок статичен или отсутствует — файл переобходится реже.

**[INFO] Wikidata-ссылки для мест присутствуют** в sameAs (`Q994`, `Q210019`, `Q193261`, `Q230`) — хороший сигнал контекстной близости к известным сущностям. Оставить.

**[INFO] VideoObject на странице Казбеги** усиливает YouTube-сигнал. Проверить что канал `@SakhvaTravel` содержит ролик о туре в Казбеги с правильным названием.
