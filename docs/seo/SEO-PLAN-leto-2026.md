# SEO-план: летний кластер Sakhva Travel 2026

Статус: доведён до полной спеки. Все 8 пробверки аудита закрыты на уровне плана.
Единственный остаточный внешний блок — EN search volume (нужен перевыпуск Google Ads OAuth).

5 тем × 2 языка = 10 статей + 2 хаба. RU-частоты — Яндекс.Wordstat (точная).

---

## 1. Архитектура перелинковки (3 уровня, оба языка)

```
УРОВЕНЬ 0 — родитель
   RU chto-posmotret-v-gruzii  ⇄  EN what-to-see-in-georgia
        │ ⇅                              │ ⇅
УРОВЕНЬ 1 — хабы
   RU gruziya-kogda-ekhat ⇄ tbilisi-letom
   EN best-time-visit-georgia ⇄ tbilisi-summer
        │ ⇅                              │ ⇅
УРОВЕНЬ 2 — споки
   Кластер А (когда ехать):  gruziya-v-iyule, gruziya-v-avguste, +май, +сентябрь
   Кластер Б (Тбилиси летом): basseyny-tbilisi, letnie-poezdki-iz-tbilisi, +tbilisskoe-ozero
```

Каждое ребро — ДВУСТОРОННЕЕ. Каждая пара RU↔EN связана `hreflang`.

Правило спок→хаб: 3 структурные точки (лид / тело / «Читайте также»), анкоры РАЗНЫЕ (см. §2).
Правило хаб→спок: 1 ссылка из тематического раздела хаба.
Правило уровень0↔уровень1: взаимная ссылка.

---

## 2. Матрица анкоров (защита от переоптимизации)

На каждую споку — 3 разных анкора к хабу:

| Точка | Тип анкора | Пример (спок→хаб А) |
|-------|-----------|---------------------|
| Лид | точный | «когда лучше ехать в Грузию» |
| Тело | вариативный | «гайд по месяцам» / «сезоны в Грузии» |
| Читайте также | навигационный/брендовый | «Все месяцы — в общем гайде Sakhva» |

Хаб→спок — точный анкор месяца/темы («Грузия в августе»).

---

## 3. Спецификация статей

### ХАБ Б (создаётся ПЕРВЫМ) — Тбилиси летом

**RU `tbilisi-letom`**
- title: Тбилиси летом 2026: что посмотреть в июне, июле, августе
- H1: Тбилиси летом — что посмотреть в июне, июле и августе
- description: Гид по Тбилиси летом 2026: погода по месяцам, где спастись от жары, бассейны, вечерний город и поездки на 1 день.
- primary: тбилиси летом (467 шир / 15 точн); ловит «тбилиси в августе» 879 шир, «тбилиси в июле»
- H2: Погода по месяцам (июнь/июль/август, таблица) · Где спастись от жары · Вечерний Тбилиси летом · Поездки из города на 1 день · Что привезти / события
- ВНИЗ на споки: §«жара»→basseyny-tbilisi + tbilisskoe-ozero; §«поездки»→letnie-poezdki-iz-tbilisi
- ВВЕРХ: chto-posmotret-v-gruzii. ВБОК: gruziya-kogda-ekhat
- Туры: летние экскурсии `/ekskursiya/...`
- hreflang → tbilisi-summer

**EN `tbilisi-summer`** — зеркало. title: Tbilisi in Summer 2026: What to Do in June, July, August. EN-volume: [PENDING OAuth]. Те же рёбра на EN-узлах (best-time-visit-georgia, tbilisi-lakes). hreflang → tbilisi-letom.

---

### Спок 1 — Аквапарки и бассейны Тбилиси

**RU `basseyny-tbilisi`**
- title: Аквапарки и бассейны Тбилиси 2026: где искупаться, цены
- H1: Аквапарки и бассейны Тбилиси 2026 — где искупаться
- primary: аквапарк тбилиси (118); secondary: бассейн тбилиси (40), где искупаться (11)
- H2: Аквапарки Тбилиси (первым!) · Открытые бассейны и пулы отелей (→stamba-tbilisi) · Где искупаться бесплатно · Цены (таблица)
- спок→хаб Б (3 точки, анкоры по §2) · вбок→letnie-poezdki-iz-tbilisi
- Туры: летние экскурсии
- hreflang → tbilisi-swimming-pools

**EN `tbilisi-swimming-pools`** — зеркало. EN-volume: [PENDING]. ПРИМ.: при нулевом EN-спросе писать во вторую очередь.

---

### Спок 5 — Летние поездки из Тбилиси

**RU `letnie-poezdki-iz-tbilisi`**
- title: Куда поехать из Тбилиси летом: Дашбаши, Табацкури и прохладные места
- H1: Куда поехать из Тбилиси летом — Дашбаши, Табацкури и 5 прохладных мест
- primary: дашбаши каньон (101); secondary: куда поехать из тбилиси (24), табацкури (11), алмазный мост (7)
- H2: Каньон Дашбаши и Алмазный мост (якорный, объёмный) · Озеро Табацкури · Высокогорье и водопады · Как добраться / туры
- АНТИ-каннибализация: НЕ дублировать городские озёра (их держит tbilisskoe-ozero) — только выездные направления
- спок→хаб Б (3 точки) · вбок→tbilisskoe-ozero, kazbegi-day-trip-from-tbilisi
- Туры: Дашбаши/Кахетия экскурсии
- hreflang → summer-day-trips-from-tbilisi

**EN `summer-day-trips-from-tbilisi`** — зеркало. EN-volume: [PENDING]. ПРИМ.: проверить каннибализацию с существующими EN day-trips (kazbegi/kakheti/mtskheta/kutaisi) — отличие = «летний/прохладный» угол + Дашбаши.

---

### Спок 3 — Грузия в июле

**RU `gruziya-v-iyule`**
- title: Грузия в июле 2026: погода, цены, куда поехать
- H1: Грузия в июле 2026 — погода, цены и куда поехать
- primary: погода в грузии в июле (473); secondary: отдых в грузии в июле (35), отзывы (11)
- H2: Погода в июле по регионам (таблица) · Где прохладнее (→letnie-poezdki, tbilisi-letom) · Отдых, цены, отзывы · Маршруты 5/7
- спок→хаб А gruziya-kogda-ekhat (3 точки) · вбок→gruziya-v-avguste
- Туры: туры по Грузии
- hreflang → georgia-in-july

**EN `georgia-in-july`** — зеркало на best-time-visit-georgia. EN-volume: [PENDING].

---

### Спок 4 — Грузия в августе

**RU `gruziya-v-avguste`**
- title: Грузия в августе 2026: погода, ртвели, маршруты
- H1: Грузия в августе 2026 — погода, ртвели и маршруты
- primary: погода в грузии в августе (289); secondary: ртвели (76), отдых в августе (31)
- H2: Погода в августе по регионам (таблица) · Ртвели — сбор винограда в Кахетии · Куда поехать в августе (→letnie-poezdki) · Цены и толпы · Маршруты
- РИСК: не уходить целиком в нишу урожая — турист. трафик приоритетнее
- спок→хаб А (3 точки) · вбок→gruziya-v-iyule, kakheti-osenyu, gruzinskoe-vino-gid
- Туры: туры по Грузии, винные туры Кахетии
- hreflang → georgia-in-august

**EN `georgia-in-august`** — зеркало. EN-volume: [PENDING].

---

## 4. Чеклист правок СУЩЕСТВУЮЩИХ файлов (обязательно)

Без этого новые статьи = орфаны. Делать в порядке.

**Фундамент (до новых статей):**
1. EN `georgia-in-may` → 3 ссылки на best-time-visit-georgia (сейчас 0)
2. EN `georgia-in-september` → 3 ссылки на best-time-visit-georgia (сейчас 0)
3. RU `gruziya-v-mae` → поднять с 1 до 3 ссылок на хаб
4. RU `gruziya-v-sentyabre` → поднять с 1 до 3 ссылок на хаб
5. RU `chto-posmotret-v-gruzii` + EN `what-to-see-in-georgia` → ссылки на оба хаба (уровень 0→1)

**После публикации спок:**
6. RU `gruziya-kogda-ekhat` → в секции `#leto` добавить ссылки на gruziya-v-iyule, gruziya-v-avguste
7. EN `best-time-visit-georgia` → ссылки на georgia-in-july, georgia-in-august
8. RU `tbilisskoe-ozero` + EN `tbilisi-lakes` → ссылка на хаб Б (войти в кластер Б)
9. `blog/index.html` (RU и EN) → добавить карточки 5 новых статей + хаб Б

---

## 5. Порядок выполнения

1. Фундамент: правки §4 пп.1–5 (5 существующих файлов RU+EN)
2. Хаб Б `tbilisi-letom` + `tbilisi-summer` (ПЕРВЫМИ из нового)
3. Споки по RU-спросу: №4 август → №3 июль → №5 Дашбаши → №1 аквапарк
4. Правки §4 пп.6–9 (хабы вниз + tbilisskoe-ozero + blog/index)
5. Проверка hreflang всех пар, отсутствие 404

---

## 6. EN-данные — остаточный блок

Все каналы закрыты: Ahrefs (тариф), Google Ads (OAuth протух), DataForSEO (не подключён).
Fallback: RU-приоритет применим к EN по аналогии; EN-slug сверены со стилем сайта (tbilisi-lakes, georgia-in-may → корректны).
Разблокировка: перевыпуск Google Ads OAuth (2 мин) → Keyword Planner отдаст volume по 14 ключам.
До разблокировки EN-статьи 1 и 5 — во вторую очередь (риск нулевого спроса).

---

## 7. Кластер А — споки май и сентябрь (доспека)

Существующие `gruziya-v-mae` / `gruziya-v-sentyabre` (EN `georgia-in-may` / `georgia-in-september`) — полноценные споки кластера А, не только «файлы для правок».

- Роль: сезонные споки наравне с июлем/августом.
- Правка (см. §4): поднять до 3 ссылок на хаб (RU) / создать 3 ссылки (EN, сейчас 0).
- Летний угол: в май-статье усилить блок «начало сезона / открытие бассейнов» → ссылка на хаб Б tbilisi-letom; сентябрь → «бархатный сезон» → ссылка на gruziya-v-avguste (ртвели продолжается).
- Анкоры — по матрице §2.

---

## 8. Критерий done (verification, grep-тесты)

Пункт §4 считается выполненным ТОЛЬКО при прохождении grep-проверки:

```bash
cd /Users/vladimir/sakhva-travel
# п.1-2 EN-фундамент: ожидаем ≥3 совпадения в каждом
grep -o "best-time-visit-georgia" en/blog/georgia-in-may.html | wc -l
grep -o "best-time-visit-georgia" en/blog/georgia-in-september.html | wc -l
# п.3-4 RU-фундамент: ожидаем ≥3
grep -o "gruziya-kogda-ekhat" blog/gruziya-v-mae.html | wc -l
grep -o "gruziya-kogda-ekhat" blog/gruziya-v-sentyabre.html | wc -l
# п.5 уровень 0→1: ожидаем оба хаба
grep -oE "gruziya-kogda-ekhat|tbilisi-letom" blog/chto-posmotret-v-gruzii.html | sort -u
grep -oE "best-time-visit-georgia|tbilisi-summer" en/blog/what-to-see-in-georgia.html | sort -u
# п.6-7 хаб→спок (после спок): ожидаем июль+август
grep -oE "gruziya-v-iyule|gruziya-v-avguste" blog/gruziya-kogda-ekhat.html
grep -oE "georgia-in-july|georgia-in-august" en/blog/best-time-visit-georgia.html
# п.8 орфан в кластер Б
grep -o "tbilisi-letom" blog/tbilisskoe-ozero.html | wc -l
# hreflang каждой новой пары: ожидаем взаимные alternate
# п.9 blog/index: ожидаем 6 новых slug в листинге
```

Done = все проверки прошли + нет битых ссылок (404) + hreflang взаимный.

---

## Прогресс

- [в работе] §4 пп.1–4 — фундамент (правка 4 существующих файлов, хаб best-time / kogda-ekhat уже существуют)
- [ожидает] §4 п.5 — уровень 0
- [ожидает OAuth] EN search volume
- [ожидает] хаб Б и споки
