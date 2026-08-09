# Аудит внутренней перелинковки — Sakhva Travel
_Дата: 2026-08-08_

## 1. Общее состояние

### Ссылочная концентрация (проблема)

Blog → card ссылки крайне неравномерно распределены. Почти весь ссылочный вес идёт на 2–3 карточки:

| Карточка (RU) | Входящих ссылок из блога |
|---|---|
| ekskursiya-kazbegi-iz-tbilisi | **80** |
| ekskursiya-kakheti-iz-tbilisi | **77** |
| nochnaya-ekskursiya-tbilisi | 57 |
| ekskursiya-stary-tbilisi | 49 |
| tur-dlya-emigrantov-tbilisi | 37 |
| ekskursiya-mtskheta-iz-tbilisi | 24 |
| gastronomicheskiy-tur-tbilisi | 21 |
| tur-batumi-iz-tbilisi | 12 |
| ekskursiya-borjomi-iz-tbilisi | 9 |

**Сироты (0 входящих из блога):**
- ekskursii-iz-kutaisi, ekskursiya-ananuri-iz-tbilisi, ekskursiya-bakuriani-iz-tbilisi
- ekskursiya-batumi-kutaisi, ekskursiya-dashbashi-iz-tbilisi, ekskursiya-gomis-mta-iz-batumi
- ekskursiya-hevsuretia-shatili, ekskursiya-jvari-iz-tbilisi, ekskursiya-racha-iz-tbilisi
- ekskursiya-sighnaghi-iz-tbilisi, ekskursiya-telavi-iz-tbilisi, ekskursiya-tusheti
- pohod-v-gory-gruzia, tur-gruziya-armeniya, vinniy-tur-tbilisi, vinodelie-kindzmarauli
- konny-tur-stepantsminda, progulka-po-kure-tbilisi, tur-batumi-2-dnya, tur-gruziya-3-dnya
- gruppa-10-chelovek-tbilisi, tur-svaneti-4-dnya, ekskursiya-bakuriani-iz-tbilisi

EN сироты (добавляются): chacha-master-klass, degustatsiya-vina-kakheti, ekskursiya-gudauri-iz-tbilisi, ekskursiya-jvari-iz-tbilisi, ekskursiya-uplistsikhe-iz-tbilisi, ekskursiya-vardzia, khachapuri-masterclass, kvevri-vino-tur, priklyuchencheskiy-tur-gruziya, tur-gruziya-5-dney, tur-gruziya-10-dney и ещё ~20.

## 2. Анкоры существующих ссылок

**RU:** В целом анкоры нормальные на топ-2 карточках (ключевые фразы). Слабые места:
- `тур с гидом` (david-gareji из blog/david-gareji) — слабый, без топонима
- `Подробнее →` встречается периодически в footer-блоках

**EN:** Критическая проблема. Топ анкоров по частоте:
- `Learn more →` — 80 вхождений (мусорный)
- `Tours` — 75 вхождений (мусорный)
- `Learn more about private tours in Tbilisi →` — 20 вхождений (общий)
- `Details →` — 8 вхождений (мусорный)

Конкретные карточки с ключевыми анкорами (`Kazbegi Day Trip from Tbilisi — from ₾175`) используются хорошо только для kazbegi и kakheti. Всё остальное — generic.

## 3. Глубина клика

```
Главная (/) → /ekskursiya/ : клик 1 (7 ссылок с главной на хаб)
/ekskursiya/ → /ekskursiya/<slug>/ : клик 2 (73 карточки охвачены)
```

Глубина нормальная — 2 клика. Проблема не в глубине, а в том, что блог (с сильным трафиком) не перетекает в карточки через контекстные ссылки.

**Тематические хабы работают слабо:**
- `/kakheti/` → ведёт только на `/ekskursiya/degustatsiya-vina-kakheti/` (1 карточка + хаб)
- `/adjara/` → ведёт только на `/ekskursiya/tur-batumi-iz-tbilisi/` (1 карточка + хаб)
- `/avtorskie-tury-gruzia/` → только nochnaya + stary-tbilisi

## 4. Взаимная перелинковка между карточками

Есть `related tours` блок. Работает для топ-карточек (kazbegi ↔ kakheti ↔ tbilisi). Сироты не появляются в related blocks сильных карточек.

Пример: в karточке kazbegi related tours — kakheti, stary-tbilisi, truso, nochnaya, batumi. Ananuri, Jvari, Gudauri, Hevsuretia — отсутствуют, хотя географически смежны.

## 5. Несвязанные блог-пары (блог о теме есть, ссылки на карточку нет)

| Блог RU | Соответствующая карточка | Ссылка есть? |
|---|---|---|
| /blog/svanetiya/ | ekskursiya-svaneti-iz-tbilisi | ДА (OK) |
| /blog/ushchelye-truso/ | ekskursiya-truso | ДА (OK) |
| /blog/david-gareji/ | ekskursiya-david-gareji | ДА, но анкор слабый (`тур с гидом`) |
| — | ekskursiya-ananuri-iz-tbilisi | НЕТ блога и НЕТ ссылок |
| — | ekskursiya-jvari-iz-tbilisi | НЕТ блога и НЕТ ссылок |
| — | ekskursiya-hevsuretia-shatili | НЕТ блога и НЕТ ссылок |
| — | ekskursiya-gudauri-iz-tbilisi | НЕТ блога RU |
| — | ekskursiya-bakuriani-iz-tbilisi | НЕТ блога |
| — | ekskursiya-dashbashi-iz-tbilisi | НЕТ блога |

| Блог EN | Соответствующая карточка | Ссылка есть? |
|---|---|---|
| /en/blog/svaneti-guide/ | ekskursiya-svaneti-iz-tbilisi (EN) | НЕТ — пропущено! |
| /en/blog/truso-valley-hike/ | ekskursiya-truso (EN) | НЕТ — пропущено! |
| /en/blog/david-gareja-monastery/ | ekskursiya-david-gareji (EN) | ДА |
| /en/blog/best-time-visit-kazbegi/ | ekskursiya-kazbegi-iz-tbilisi | НЕТ — 0 ссылок |
| /en/blog/georgia-7-day-itinerary/ | ekskursii-iz-kutaisi (EN) | НЕТ |
| /en/blog/georgia-7-day-itinerary/ | ekskursiya-batumi-kutaisi (EN) | НЕТ |
| /en/blog/georgia-with-kids/ | семейный тур / kutaisi | НЕТ |

---

## 6. Топ-25 конкретных пар для добавления ссылок

Приоритет: A = немедленно (высокий трафик блога + нет ссылки), B = важно, C = дополнительно.

### ПРИОРИТЕТ A — EN блог с трафиком, 0 ссылок на карточку

| # | Страница-источник | Карточка-цель | Рекомендуемый анкор EN |
|---|---|---|---|
| 1 | /en/blog/best-time-visit-kazbegi/ | /en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ | `Kazbegi day trip from Tbilisi — from ₾175` |
| 2 | /en/blog/svaneti-guide/ | /en/ekskursiya/ekskursiya-svaneti-iz-tbilisi/ | `guided Svaneti tour from Tbilisi` |
| 3 | /en/blog/truso-valley-hike/ | /en/ekskursiya/ekskursiya-truso/ | `Truso Valley day tour from Tbilisi` |
| 4 | /en/blog/georgia-7-day-itinerary/ | /en/ekskursiya/ekskursii-iz-kutaisi/ | `day trips from Kutaisi` |
| 5 | /en/blog/georgia-7-day-itinerary/ | /en/ekskursiya/ekskursiya-batumi-kutaisi/ | `Batumi to Kutaisi tour` |
| 6 | /en/blog/georgia-with-kids/ | /en/ekskursiya/ekskursiya-gudauri-iz-tbilisi/ | `Gudauri day trip from Tbilisi` |
| 7 | /en/blog/kazbegi-in-winter/ | /en/ekskursiya/ekskursiya-gudauri-iz-tbilisi/ | `Gudauri ski day trip from Tbilisi` |
| 8 | /en/blog/kazbegi-vs-kakheti/ | /en/ekskursiya/ekskursiya-ananuri-iz-tbilisi/ | `Ananuri Castle day tour from Tbilisi` |
| 9 | /en/blog/things-to-see-kazbegi/ | /en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ | `Kazbegi guided day trip from Tbilisi — ₾175` |
| 10 | /en/blog/kakheti-in-autumn/ | /en/ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/ | `Sighnaghi wine tour from Tbilisi` |

### ПРИОРИТЕТ A — RU блог, нет ссылки на релевантную карточку

| # | Страница-источник | Карточка-цель | Рекомендуемый анкор RU |
|---|---|---|---|
| 11 | /blog/david-gareji/ | /ekskursiya/ekskursiya-david-gareji/ | ЗАМЕНИТЬ анкор `тур с гидом` → `экскурсия в Давид Гареджи из Тбилиси` |
| 12 | /blog/kazbegi-samostoyatelno-ili-s-gidom/ | /ekskursiya/ekskursiya-ananuri-iz-tbilisi/ | `экскурсия к крепости Ананури` |
| 13 | /blog/tury-v-kakheti-2026/ | /ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/ | `экскурсия в Сигнаги из Тбилиси` |
| 14 | /blog/tury-v-kakheti-2026/ | /ekskursiya/ekskursiya-telavi-iz-tbilisi/ | `тур в Телави и Алазанскую долину` |
| 15 | /blog/kazbegi-iz-tbilisi-2026/ | /ekskursiya/ekskursiya-gudauri-iz-tbilisi/ | `экскурсия в Гудаури из Тбилиси` |

### ПРИОРИТЕТ B — Тематические хабы: расширить карточки

| # | Страница-источник | Карточка-цель | Рекомендуемый анкор |
|---|---|---|---|
| 16 | /kakheti/ | /ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/ | `экскурсия в Сигнаги` |
| 17 | /kakheti/ | /ekskursiya/ekskursiya-telavi-iz-tbilisi/ | `тур в Телави из Тбилиси` |
| 18 | /adjara/ | /ekskursiya/ekskursiya-batumi-kutaisi/ | `тур Батуми–Кутаиси` |
| 19 | /adjara/ | /ekskursiya/ekskursiya-gomis-mta-iz-batumi/ | `экскурсия Гомис-мта из Батуми` |
| 20 | /avtorskie-tury-gruzia/ | /ekskursiya/romanticheskiy-tur-tbilisi/ | `романтический тур по Тбилиси` |

### ПРИОРИТЕТ B — Related tours блок в карточках: добавить соседей

| # | Карточка-источник | Карточка-цель | Логика |
|---|---|---|---|
| 21 | ekskursiya-kazbegi-iz-tbilisi | ekskursiya-ananuri-iz-tbilisi | По пути Тбилиси–Казбеги |
| 22 | ekskursiya-kazbegi-iz-tbilisi | ekskursiya-gudauri-iz-tbilisi | Тот же горный маршрут |
| 23 | ekskursiya-kakheti-iz-tbilisi | ekskursiya-sighnaghi-iz-tbilisi | Сигнаги = часть Кахетии |
| 24 | ekskursiya-kakheti-iz-tbilisi | ekskursiya-telavi-iz-tbilisi | Телави = часть Кахетии |
| 25 | ekskursiya-borjomi-iz-tbilisi | ekskursiya-bakuriani-iz-tbilisi | Борджоми–Бакуриани рядом |

---

## 7. Критический EN-баг: анкоры «Learn more»

80 ссылок с анкором `Learn more →` в EN-блоге. Google их девальвирует — это ссылки без контекста. Нужно массово заменить на тематические анкоры с топонимом + типом тура. Быстрый скрипт по `blog_content.py` или скрипт замены в HTML.

Примеры замен:
- `Learn more →` в контексте Borjomi → `Borjomi day tour from Tbilisi — from ₾178`
- `Learn more →` в контексте Svaneti → `Svaneti guided tour from Tbilisi`
- `Tours` → `day tours from Tbilisi` (контекстно)

---

## 8. Итоговые приоритеты

1. **Немедленно** — добавить 10 A-ссылок в EN-блог (особенно best-time-visit-kazbegi, svaneti-guide, truso-valley-hike — вероятно высокотрафиковые по GSC показам)
2. **Немедленно** — 5 A-ссылок в RU-блог (david-gareji анкор-фикс + 4 новых)
3. **Неделя** — заменить 80 `Learn more →` EN-анкоров на ключевые
4. **Неделя** — расширить related-tours блок в kazbegi/kakheti карточках (+ananuri, +gudauri, +sighnaghi, +telavi)
5. **Месяц** — создать блог-статьи под 5 сиротских карточек без блога (ananuri, jvari, dashbashi, hevsuretia, bakuriani)
