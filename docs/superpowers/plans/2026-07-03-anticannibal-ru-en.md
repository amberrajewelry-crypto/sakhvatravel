# Разведение каннибализации Sakhva (RU + EN) — Implementation Plan

**Goal:** Убрать всех реальных каннибалов (подтверждённых GSC за 90 дней) на RU и EN так, чтобы за каждый запрос конкурировал ровно один URL; RU↔EN держать в паре через hreflang.

**Архитектура:** Каннибала убивает КОНТЕНТ (title/H1/1-й абзац + анкоры), не slug. Поэтому основа — контент-развод и удаление истинных дублей. Переименование URL — только для нулевого трафика. Каждое RU-изменение URL синхронизируется с EN-парой (hreflang).

**Стек:** статический HTML, `vercel.json` (redirects/один хоп), `sitemap*.xml`, `rss.xml`, hreflang link-теги. Проверка: `node scripts/predeploy-check.js`, `curl -sL` на проде, GSC.

**Данные:** реальные каннибалы — `/tmp/gsc_real.json` (19). Классификация страниц по трафику — `/tmp/pagestat.py`.

---

## Принципы (обязательны)
- 301 в один хоп (проверено: цели конечные, цепочек нет в 392 существующих правилах).
- Внутренние ссылки — сразу на конечный URL, НЕ через редирект.
- Разные анкоры у разведённых страниц (одинаковый анкор = продолжение каннибала).
- Топ-30 в GSC НЕ переименовывать (URL менять только при 0 показов за 90 дней).
- Любое RU-переименование → парная правка `hreflang ru` в EN-странице (и наоборот).
- После каждой волны: sitemap → GSC → пауза 2–3 недели.

---

## RU↔EN карта пар (hreflang), затронутая планом

| RU | EN counterpart (slug уже англ.) |
|---|---|
| blog/vardzia | en/blog/vardzia-cave-monastery |
| blog/uplistsikhe | en/blog/uplistsikhe-cave-city |
| blog/mtskheta-iz-tbilisi | en/blog/mtskheta-day-trip |
| blog/kutaisi-iz-tbilisi | en/blog/kutaisi-day-trip |
| blog/narikala-tbilisi | en/blog/narikala-fortress-tbilisi |
| blog/svanetiya | en/blog/svaneti-guide |
| blog/david-gareji | en/blog/david-gareja-monastery |
| blog/ushchelye-truso | en/blog/truso-valley-hike |
| blog/tury-v-batumi-2026 | en/blog/batumi-complete-guide |
| blog/batumi-iz-tbilisi | en/blog/batumi-from-tbilisi |
| blog/tury-v-borzhomi-2026 | en/blog/borjomi-complete-guide |
| blog/tury-v-gori-2026 | en/blog/gori-uplistsikhe-guide |
| blog/tury-v-kazbegi-2026 | en/blog/kazbegi-complete-guide |

> Правило: EN-slug НЕ трогаем (они уже нормальные англ.). Меняется только `hreflang ru href` в EN при смене RU slug.

---

## ВОЛНА 1 — Удалить истинные дубли + 301 (RU и EN)

### RU-дубли (9) — удалить папку, 301 на канон, обновить внутренние ссылки
```
ekskursiya/kazbegi                     → ekskursiya/ekskursiya-kazbegi-iz-tbilisi
ekskursiya/batumi                      → ekskursiya/tur-batumi-iz-tbilisi
ekskursiya/tur-dlya-detey-tbilisi      → ekskursiya/family-tur-tbilisi
ekskursiya/ekskursiya-jvari-iz-tbilisi → ekskursiya/ekskursiya-mtskheta-iz-tbilisi
ekskursiya/tur-vsya-gruziya            → ekskursiya/tur-gruziya-10-dney
ekskursiya/vinodelie-kindzmarauli      → ekskursiya/degustatsiya-vina-kakheti
ekskursiya/kvevri-vino-tur             → ekskursiya/degustatsiya-vina-kakheti
ekskursiya/vinniy-marshrut-alazani     → ekskursiya/degustatsiya-vina-kakheti
gid-v-tbilisi-na-russkom               → chastniy-gid-tbilisi
```
(7 из них уже в vercel.json — проверить, добавить недостающие: tur-dlya-detey, jvari, tur-vsya-gruziya, 3 вина.)

### EN-дубли (англ. slug vs рус. slug — оставить АНГЛ., рус. удалить+301)
```
en/ekskursii-tbilisi          → en/tours-in-tbilisi
en/ekskursii-po-gruzii        → en/tours-in-georgia
en/vinnye-tury-gruzia         → en/wine-tours-georgia
en/gid-v-tbilisi-na-russkom   → en/private-guide-tbilisi
en/ekskursiya/khachapuri-master-klass → en/ekskursiya/khachapuri-masterclass
en/tury-v-gruziyu-iz-moskvy       → en/tours-from-moscow
en/tury-v-gruziyu-iz-spb          → en/tours-from-saint-petersburg
en/tury-v-gruziyu-iz-kazani       → en/tours-from-kazan
en/tury-v-gruziyu-iz-krasnodara   → en/tours-from-krasnodar
en/tury-v-gruziyu-iz-minska       → en/tours-from-minsk
en/tury-v-gruziyu-iz-novosibirska → en/tours-from-novosibirsk
en/tury-v-gruziyu-iz-tashkenta    → en/tours-from-tashkent
en/tury-v-gruziyu-iz-vladikavkaza → en/tours-from-vladikavkaz
en/tury-v-gruziyu-iz-ekaterinburga→ en/tours-from-yekaterinburg
en/tury-v-gruziyu-iz-erevana      → en/tours-from-yerevan
en/tury-v-gruziyu-iz-kazahstana   → en/tours-from-kazakhstan
en/avtorskie-tury-gruzia          → en/ (проверить англ-эквивалент; если нет — оставить)
en/gornye-tury-gruzia             → en/ (проверить)
en/mnogodnevnye-tury-gruzia       → en/ (проверить)
```
Verify: `curl -sL https://sakhva-travel.com/en/ekskursii-tbilisi → 301 → /en/tours-in-tbilisi`.

---

## ВОЛНА 2 — Контент-развод (title + H1 + 1-й абзац). ЭТО убивает каннибалов.

### RU-узлы (из GSC)
| Пара (запрос) | URL → целевой запрос (title/H1) | Действие |
|---|---|---|
| дегустация вина / винный тур | `vinnye-tury-gruzia` = «винные туры, дегустация» · `ekskursiya-kakheti` = «экскурсия Кахетия Сигнахи/Бодбе» (убрать «вино/дегустация» из H1) · `gastronomicheskiy-tur` = «гастро/еда» (убрать вино) | 3 title/H1 |
| экскурсия в Кахетию | `ekskursiya-kakheti` = коммерч. · `blog/kakheti-za-1-den` = инфо «что посмотреть за день» | 2 title |
| экскурсия в Казбеги | `ekskursiya-kazbegi` = «Казбеги» · `ekskursiya-kakheti` — убрать «Казбеги» из текста + внутр.перелинковку | 1 текст+ссылки |
| маршрут Грузия 7 дней | `blog/gruziya-7-dney` = инфо-маршрут · `ekskursiya/tur-gruziya-7-dney` = «купить тур 7 дней» | 2 title |
| серные бани | `blog/sernye-bani-tbilisi` = «цены/как выбрать» · `ekskursiya-abanotubani` = «экскурсия+хамам с гидом» | 2 title |
| Мцхета что посмотреть | `blog/mtskheta-iz-tbilisi` = инфо · `ekskursiya-mtskheta` = коммерч. | 2 title |
| вечер в Тбилиси | `nochnoy-tbilisi` = «ночь/клубы» · `tbilisi-vecherom` уже 301 ✅ | 1 title |

Анкоры: внутренние ссылки на разведённые пары — РАЗНЫЕ (напр. «экскурсия в Кахетию с гидом» vs «Кахетия: что посмотреть за день»).

### EN-узлы (из GSC)
| Пара (запрос) | Действие |
|---|---|
| tbilisi to kazbegi (distance/transfer/marshrutka) | `transfer-tbilisi-to-kazbegi` = логистика (трансфер/цена/маршрутка) · `kazbegi-day-trip-from-tbilisi` = «day trip, what to see» — убрать transfer-ключи | 2 title/H1 |
| georgia visa | `georgia-visa-2026` = виза · `georgia-passport-requirements` = загранпаспорт | 2 title |
| kazbegi to kakheti | `kazbegi-vs-kakheti` = сравнение · `ekskursiya/tur-kazbegi-kakheti-2-dnya` = «купить тур 2 дня» | 2 title |
| all tbilisi tours 2026 | `tbilisi-tours-guide` = обзор-инфо · `/en` не таргетить этот ключ · `korporativniy-tur` = «corporate» | 1 title + внутр.ссылки |
| tbilisi to borjomi day trip | `borjomi-from-tbilisi` = инфо · `en/ekskursiya/ekskursiya-borjomi` = коммерч. | 2 title |
| tbilisi to mtskheta | удалить 3-й дубль `en/tour/mtskheta` → 301 на `en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi` | delete+301 |

---

## ВОЛНА 3 — canonical→self расклейка
Страницы с собственным рангом в GSC, но с canonical на другую — вернуть self + уникальный контент из Волны 2:
`blog/kakheti-za-1-den`, `blog/kakheti-chto-posmotret`, `blog/kazbegi-chto-posmotret`, EN-аналоги.
Verify: `curl -sL <url> | grep canonical` → self.

---

## ВОЛНА 4 — Переименование URL (ТОЛЬКО нулевой трафик, +hreflang sync)
Разрешено (0 показов за 90 дней): **3 RU** + их EN-пары.
```
blog/tury-v-gruziyu-2026 → blog/gruzia-planirovanie-poezdki   (+ EN hreflang, если есть пара)
tury-v-batumi            → otdyh-v-batumi                     (+ en/tours-in-batumi hreflang)
tury-na-kazbek           → gora-kazbek                        (+ EN hreflang)
```
Все прочие ранее предложенные переименования (Вардзиа, Мцхета, Боржоми-блог, серные бани и т.д.) — **в топ-30, НЕ переименовывать**, они решаются Волной 2 (контент).

При каждом переименовании: `git mv` → 301 в vercel.json → внутренние ссылки на новый URL → `hreflang ru` в EN-паре на новый URL → sitemap.

---

## Self-Review (checklist)
- [ ] Каждый из 19 GSC-каннибалов имеет задачу (Волна 1/2). Проверка: `python3 /tmp/verify.py`.
- [ ] Все 301 — один хоп (grep vercel.json: source ≠ чужой destination).
- [ ] Каждое RU-переименование имеет парную правку EN hreflang.
- [ ] Внутренние анкоры разведённых пар — разные (grep по index.html/catalog.json).
- [ ] EN-дубли (Волна 1) удалены, англ. slug оставлен.
- [ ] `node scripts/predeploy-check.js <files> index.html` — 0 ошибок.
- [ ] После деплоя: `curl -sL` на 5 проб + отправка sitemap в GSC.

## Объём
- Волна 1: 9 RU delete + ~19 EN delete/301
- Волна 2: ~14 RU + ~11 EN контент-правок (title/H1/1-й абзац) + анкоры
- Волна 3: ~4 canonical
- Волна 4: 3 RU rename + hreflang
