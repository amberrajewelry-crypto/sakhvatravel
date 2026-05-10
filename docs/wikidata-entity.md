# Wikidata Entity — Sakhva Travel

Инструкция по созданию Q-item на wikidata.org для туристического агентства Sakhva Travel.

---

## Важно: Notability Guidelines

Wikidata принимает сущности, если они соответствуют хотя бы одному критерию:

1. **Наличие Wikipedia-статьи** на любом языке — самый сильный аргумент
2. **Наличие Wikidata-совместимого идентификатора** (TripAdvisor ID, VIAF и т.д.)
3. **Значимость** — компания должна быть упомянута в авторитетных независимых источниках

Sakhva Travel проходит по критерию 2 (TripAdvisor listing d15318013) и частично по критерию 3 (87 Google отзывов, рейтинг 4.9).

**Риск удаления:** item для небольшого локального бизнеса может быть помечен как `no claim` и удалён. Минимизируй риск: добавь как можно больше проверяемых claims со ссылками на внешние источники.

---

## Шаг 1 — Создание Q-item

1. Зайди на https://www.wikidata.org/wiki/Special:NewItem
2. Авторизуйся (нужен аккаунт Wikimedia)
3. Заполни поля:

| Поле | Значение |
|------|----------|
| Language | Russian (ru) |
| Label | Sakhva Travel |
| Description | туристическое агентство в Тбилиси, Грузия |
| Also known as | Сахва Тревел |

4. Нажми **Create**
5. Запомни присвоенный Q-номер (например, Q12345678)

---

## Шаг 2 — Добавление меток на других языках

После создания item — нажми **Add** в секции Terms:

| Language | Label | Description |
|----------|-------|-------------|
| en | Sakhva Travel | travel agency in Tbilisi, Georgia |
| ka | სახვა ტრეველი | სატურისტო სააგენტო თბილისში |
| ru | Sakhva Travel | туристическое агентство в Тбилиси, Грузия |

---

## Шаг 3 — Statements (Properties)

### P31 — instance of
- **Value:** travel agency (Q131524)
- **Reference:** нет (общеизвестный факт)

### P17 — country
- **Value:** Georgia (Q230)
- **Reference:** сайт https://sakhva-travel.com

### P131 — located in administrative territorial entity
- **Value:** Tbilisi (Q994)
- **Reference:** сайт https://sakhva-travel.com

### P856 — official website
- **Value:** https://sakhva-travel.com
- **Reference:** прямая ссылка (retrieved: текущая дата)

### P571 — inception (год основания)
- **Value:** 2023
- **Reference:** 
  - URL: https://sakhva-travel.com
  - retrieved: текущая дата

### P112 — founded by
- **Value:** создай или найди Q-item для "Timur" (частное лицо — лучше пропустить если нет отдельного notable Q-item)
- **Примечание:** для частных лиц без Wikipedia-статьи это claim часто удаляется. Пропусти если нет подтверждения.

### P18 — image
- Пропусти или загрузи фото на Wikimedia Commons отдельно, затем укажи файл

### P2002 — Twitter username / P2003 — Instagram username
- **P2003 (Instagram):** sakhvatravel
- **Reference:** https://www.instagram.com/sakhvatravel

### P2397 — YouTube channel ID
- **Value:** @SakhvaTravel (или числовой ID канала)
- **Reference:** https://www.youtube.com/@SakhvaTravel

### P625 — coordinate location
- Координаты офиса в Тбилиси (если известны)
- Source: Google Maps

### P4900 — Google Knowledge Graph ID / P4081 — TripAdvisor ID
- **P4081 (TripAdvisor ID):** d15318013
- **Reference:** https://www.tripadvisor.com/Attraction_Review-g294195-d15318013
- **Примечание:** это самый сильный идентификатор для notability

### P856 — official website (уже выше)

---

## Шаг 4 — References (источники для каждого claim)

Для каждого statement добавь reference. Wikidata поддерживает:

| Property Reference | Описание |
|-------------------|----------|
| P854 (reference URL) | Прямая ссылка на страницу |
| P813 (retrieved) | Дата проверки (формат: YYYY-MM-DD) |
| P123 (publisher) | Издатель (Google, TripAdvisor и т.д.) |

**Минимальный набор references:**

```
P571 (inception: 2023):
  - P854: https://sakhva-travel.com
  - P813: 2026-05-02

P4081 (TripAdvisor ID: d15318013):
  - P854: https://www.tripadvisor.com/Attraction_Review-g294195-d15318013
  - P813: 2026-05-02

P2003 (Instagram: sakhvatravel):
  - P854: https://www.instagram.com/sakhvatravel
  - P813: 2026-05-02

P2397 (YouTube):
  - P854: https://www.youtube.com/@SakhvaTravel
  - P813: 2026-05-02
```

---

## Шаг 5 — Google Maps / CID

Wikidata не имеет стандартного property для Google Maps CID. Варианты:

- **P1566 (GeoNames ID)** — не подходит
- **P3749 (Google Maps CID)** — существует как external identifier
  - Value: 14070083063461040701
  - Reference: https://maps.google.com/?cid=14070083063461040701

Проверь существование P3749 в Wikidata перед добавлением.

---

## Шаг 6 — Проверка перед публикацией

- [ ] Хотя бы один внешний идентификатор (TripAdvisor ID — обязателен)
- [ ] instance of (P31) заполнен
- [ ] country (P17) заполнен
- [ ] official website (P856) заполнен
- [ ] Все claims имеют references
- [ ] Метки на ru + en

---

## Итоговый список Properties

| Property | ID | Значение |
|----------|----|----------|
| instance of | P31 | Q131524 (travel agency) |
| country | P17 | Q230 (Georgia) |
| located in | P131 | Q994 (Tbilisi) |
| inception | P571 | 2023 |
| official website | P856 | https://sakhva-travel.com |
| TripAdvisor ID | P4081 | d15318013 |
| Instagram username | P2003 | sakhvatravel |
| YouTube channel | P2397 | @SakhvaTravel |
| Google Maps CID | P3749 | 14070083063461040701 |

---

## Ссылки

- TripAdvisor: https://www.tripadvisor.com/Attraction_Review-g294195-d15318013
- Сайт: https://sakhva-travel.com
- Instagram: https://www.instagram.com/sakhvatravel
- YouTube: https://www.youtube.com/@SakhvaTravel
- Google Maps: https://maps.google.com/?cid=14070083063461040701
- Wikidata New Item: https://www.wikidata.org/wiki/Special:NewItem
- Wikidata Property search: https://www.wikidata.org/wiki/Special:ListProperties
