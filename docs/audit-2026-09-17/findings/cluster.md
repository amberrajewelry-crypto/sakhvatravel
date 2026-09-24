# Семантическая кластеризация — sakhva-travel.com (RU)

**Оценка архитектуры: 52/100** — хабы почти все уже существуют (`sitemap-pages.xml`), но не используются как хабы: нет очевидной прошивки хаб↔спицы, и по 5 темам параллельно растут блог/тур/хаб-страницы под один и тот же запрос.

Источники: `sm-tours.xml` (82 RU тура), `sm-blog.xml` (~100 постов), `sm-pogoda.xml` (20 регионов), `sitemap-landing.xml` (25 гео-лендингов «туры из city»), + `sitemap-pages.xml` (найден отдельно, содержит 31 RU-страницу — это и есть недостающие пилlarы: 11 регионов Грузии + 20 тематических хабов типа `/kakheti/`, `/tury-na-kazbek/`, `/tury-v-svaneti/`, `/vinnye-tury-gruzia/`, `/tury-v-batumi/`, `/tury-v-tbilisi/`, `/tury-v-gruziyu/`). Google уже их проиндексировал (подтверждено `site:` поиском).

## 1. Кластеры по seed-словам

| Seed | Хаб (pillar, есть) | Спицы (транзакционные туры) | Спицы (инфо-блог) | Проблема |
|---|---|---|---|---|
| казбеги | `/tury-na-kazbek/` | `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/`, `hayking-*-iz-kazbegi` ×3, `konny-tur-stepantsminda/`, `ekskursiya-truso/`, `ekskursiya-gudauri-iz-tbilisi/` | `kazbegi-iz-tbilisi-2026`, `kogda-ekhat-v-kazbegi`, `kazbegi-samostoyatelno-ili-s-gidom`, `kazbegi-zimoy`, `kazbegi-ili-kakheti`, `transfer-tbilisi-kazbegi`, `voenno-gruzinskaya-doroga` + `/pogoda/kazbegi/` | 9+ страниц на тему, хаб не главный — риск каннибализации (см. §2) |
| кахетия винный тур | `/kakheti/` + `/vinnye-tury-gruzia/` (дублируют друг друга по смыслу) | `ekskursiya-kakheti-iz-tbilisi`, `degustatsiya-vina-kakheti`, `vinniy-marshrut-alazani`, `vinodelie-kindzmarauli`, `kvevri-vino-tur`, `rtveli-sbor-vinograda`, `ekskursiya-sighnaghi-iz-tbilisi`, `ekskursiya-telavi-iz-tbilisi` | `kakheti-za-1-den`, `kakheti-osenyu`, `gruzinskoe-vino-gid`, `degustatsiya-vina-gruziya` + `/pogoda/kakheti/`, `/pogoda/signagi/`, `/pogoda/telavi/` | 2 хаба на одну тему (`/kakheti/` регион vs `/vinnye-tury-gruzia/` тема вина) — решить, какой первичный |
| сванетия | `/tury-v-svaneti/` | `ekskursiya-svaneti-iz-tbilisi`, `tur-svaneti-4-dnya`, `ushguli-iz-mestii`, `ushguli-shkhara-lednik`, `ozero-koruldi-mestia`, `lednik-chalaadi-mestia` | `blog/svanetiya` (1 пост) + `/pogoda/mestia/` | норм, но всего 1 инфо-пост — недокрыто (мало спиц контента) |
| батуми экскурсии | `/tury-v-batumi/` | `tur-batumi-iz-tbilisi`, `tur-batumi-2-dnya`, `ekskursii-iz-batumi`, `ekskursiya-gomis-mta-iz-batumi`, `transfer-tbilisi-batumi`, `ekskursiya-batumi-kutaisi` | `batumi-iz-tbilisi`, `tury-v-batumi-2026`, `poezd-tbilisi-batumi`, `chernoe-more-gruzii`, `ureki-plyazh` + `/pogoda/batumi/`, `/pogoda/adjara/` | хаб + 2 блог-поста метят в один и тот же запрос «туры в батуми» — каннибализация |
| гид тбилиси / экскурсии тбилиси | `/ekskursiya/` (список) — **нет отдельного «услуги гида» хаба**, ближайшее — `/about/saba/` | все ~55 `/ekskursiya/*-tbilisi` туров | `russkoyazychny-gid-tbilisi`, `chastny-gid-ili-gruppa-tbilisi`, `gid-tbilisi-vs-gid-gruziya`, `skolko-stoit-gid-tbilisi`, `uslugi-chastnogo-gida-tbilisi` | 5 блог-постов делят один интент «нанять гида в Тбилиси» без единого хаба — прямая каннибализация |
| что посмотреть в тбилиси | нет пилlara-агрегатора (только `/blog/chto-posmotret-v-tbilisi/` как де-факто хаб) | `ekskursiya-stary-tbilisi`, `ekskursiya-mtatsminda`, `ekskursiya-narikala`, `ekskursiya-abanotubani`, `progulka-po-kure-tbilisi`, `nochnaya-ekskursiya-tbilisi`, `fotosessiya-tbilisi` | `tbilisi-za-1-den`, `tbilisi-za-3-dnya`, `tbilisi-besplatno`, `skrytye-mesta-tbilisi`, `tbilisi-s-detmi-chto-posmotret`, `muzei-tbilisi`, `narikala-tbilisi`, `botanicheskiy-sad-tbilisi`, `kanatnaya-doroga-tbilisi`, `sernye-bani-tbilisi`, `tbilisskoe-ozero`, `nochnoy-tbilisi`, `sovetskiy-tbilisi`, `istoriya-tbilisi`, `tbilisi-fotolokatsii` | 15+ блог-постов без хаба, который решает, кто на кого ссылается — самый большой рыхлый кластер |
| погода в тбилиси по месяцам | `/pogoda/` (индекс) → `/pogoda/tbilisi/` | — | 20 региональных `/pogoda/{region}/` | структура ОК, hub-and-spoke уже правильный, только проверить, что `/pogoda/` реально ссылается на все 20 |
| туры в грузию из [город] | `/tury-v-gruziyu/` (хаб есть в sitemap-pages, НЕ найден в sitemap-landing) | 25 гео-лендингов `tury-v-gruziyu-iz-*` | — | хаб есть, но не факт что 25 лендингов на него ссылаются и наоборот — проверить шаблон |

## 2. Каннибализация (риск high/med)

| Кластер | Конкурирующие URL | Оценка риска | Фикс |
|---|---|---|---|
| Казбеги (общий запрос) | `/tury-na-kazbek/` vs `/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/` vs `/blog/kazbegi-iz-tbilisi-2026/` | High | `/tury-na-kazbek/` = пиллар (обзор+цены+сезон), `/ekskursiya/...` = карточка тура (бронирование), `/blog/kazbegi-iz-tbilisi-2026/` — либо удалить/склеить с пилларом (301 или canonical), либо сузить intent на «в этом году что нового» |
| Кахетия/вино (2 хаба) | `/kakheti/` vs `/vinnye-tury-gruzia/` | High | Развести: `/kakheti/` — регион (что где как добраться), `/vinnye-tury-gruzia/` — продуктовая тема (сравнение виноделен по всей Грузии, не только Кахетии); прописать разные title/H1 и перелинковать друг на друга 1 раз |
| Батуми | `/tury-v-batumi/` vs `/blog/tury-v-batumi-2026/` vs `/blog/batumi-iz-tbilisi/` | Med-High | Оставить хаб транзакционным, `tury-v-batumi-2026` смержить в хаб (контент почти дублирует), `batumi-iz-tbilisi` — сделать чисто «как добраться» (транспорт), не «что посмотреть» |
| Гид Тбилиси (5 постов, без хаба) | `russkoyazychny-gid-tbilisi`, `chastny-gid-ili-gruppa-tbilisi`, `gid-tbilisi-vs-gid-gruziya`, `skolko-stoit-gid-tbilisi`, `uslugi-chastnogo-gida-tbilisi` | High | Нужен 1 pillar «Гид в Тбилиси» (цены+как выбрать+сравнение), 5 постов превратить в спицы с разными long-tail (цена / группа vs частный / кто такой Саба) — сейчас все 5 бьют в top-of-funnel «нанять гида» одновременно |
| Что посмотреть в Тбилиси (15+ постов) | весь список выше | Med | Назначить `/blog/chto-posmotret-v-tbilisi/` официальным пилларом (или создать `/tury-v-tbilisi/` как коммерческий пиллар + блог как инфо-спицы), прописать явные ссылки пиллар→каждый спот-пост |

## 3. Пробелы (missing hub-and-spoke)

- **Свои хабы не используются как хабы.** `sitemap-pages.xml` содержит 20 готовых тематических/регио-пилларов (`/kakheti/`, `/tury-na-kazbek/`, `/tury-v-svaneti/`, `/vinnye-tury-gruzia/`, `/tury-v-batumi/`, `/tury-v-tbilisi/`, `/gornye-tury-gruzia/`, `/mnogodnevnye-tury-gruzia/`, `/avtorskie-tury-gruzia/`, `/tury-v-gruziyu/`, `/tury-v-gruziyu-s-detmi/`, `/grupovye-tury-v-gruziyu/`, `/individualnyy-tur-v-gruziyu/`, `/ekskursionnye-tury-v-gruziyu/`, `/tury-v-gruziyu-letom/`, `/tury-v-gruziyu-zimoy/`), но НИ ОДИН не подтверждён в `sitemap-tours.xml`/`sm-tours.xml` как связанный перелинковкой — нужен HTML-аудит (grep по `href` в самих страницах), сейчас это не проверено, только факт их существования и индексации Google.
- **Нет хаба «гид в Тбилиси»** — 5 блог-постов существуют без пиллара (см. §2).
- **Сванетия недокрыта контентом**: 1 инфо-пост на 6 тур-страниц — стоит добавить 2-3 спицы (например «Ушгули самостоятельно», «когда ехать в Сванетию»).
- **25 гео-лендингов `tury-v-gruziyu-iz-*`** не имеют общего видимого хаба в `sitemap-landing.xml` (хаб `/tury-v-gruziyu/` лежит в отдельном `sitemap-pages.xml`) — риск, что они орфанные (никто на них массово не ссылается, кроме, возможно, футера).

## 4. Матрица внутренних ссылок (обязательные хаб→спица, ≤30 строк)

| Хаб | → Спицы (мандаторно, спица тоже должна ссылаться назад) |
|---|---|
| `/tury-na-kazbek/` | `ekskursiya-kazbegi-iz-tbilisi`, `hayking-truso-iz-kazbegi`, `hayking-juta-chaukhi-iz-kazbegi`, `hayking-gveleti-iz-kazbegi`, `konny-tur-stepantsminda`, `/blog/kogda-ekhat-v-kazbegi/`, `/pogoda/kazbegi/` |
| `/kakheti/` | `ekskursiya-kakheti-iz-tbilisi`, `ekskursiya-sighnaghi-iz-tbilisi`, `ekskursiya-telavi-iz-tbilisi`, `/blog/kakheti-za-1-den/`, `/pogoda/kakheti/` |
| `/vinnye-tury-gruzia/` | `degustatsiya-vina-kakheti`, `vinniy-marshrut-alazani`, `vinodelie-kindzmarauli`, `kvevri-vino-tur`, `rtveli-sbor-vinograda`, `/blog/gruzinskoe-vino-gid/` |
| `/tury-v-svaneti/` | `ekskursiya-svaneti-iz-tbilisi`, `tur-svaneti-4-dnya`, `ushguli-iz-mestii`, `ushguli-shkhara-lednik`, `ozero-koruldi-mestia`, `lednik-chalaadi-mestia`, `/blog/svanetiya/`, `/pogoda/mestia/` |
| `/tury-v-batumi/` | `tur-batumi-iz-tbilisi`, `tur-batumi-2-dnya`, `ekskursii-iz-batumi`, `transfer-tbilisi-batumi`, `/blog/poezd-tbilisi-batumi/`, `/pogoda/batumi/` |
| `/tury-v-tbilisi/` (коммерч. пиллар) | `ekskursiya-stary-tbilisi`, `ekskursiya-mtatsminda`, `ekskursiya-narikala`, `ekskursiya-abanotubani`, `progulka-po-kure-tbilisi`, `nochnaya-ekskursiya-tbilisi` |
| `/blog/chto-posmotret-v-tbilisi/` (инфо-пиллар) | `tbilisi-za-1-den`, `tbilisi-za-3-dnya`, `skrytye-mesta-tbilisi`, `muzei-tbilisi`, `botanicheskiy-sad-tbilisi`, `kanatnaya-doroga-tbilisi`, `sernye-bani-tbilisi`, `tbilisskoe-ozero`, `nochnoy-tbilisi`, `sovetskiy-tbilisi`, `istoriya-tbilisi`, `tbilisi-fotolokatsii`, `tbilisi-besplatno`, `tbilisi-s-detmi-chto-posmotret` |
| **(новый) «Гид в Тбилиси»** — создать | `russkoyazychny-gid-tbilisi`, `chastny-gid-ili-gruppa-tbilisi`, `gid-tbilisi-vs-gid-gruziya`, `skolko-stoit-gid-tbilisi`, `uslugi-chastnogo-gida-tbilisi`, `/about/saba/` |
| `/tury-v-gruziyu/` | все 25 `tury-v-gruziyu-iz-{city}` |
| `/pogoda/` | все 20 `/pogoda/{region}/` (уже правильная структура — проверить факт) |

## 5. Приоритет фиксов

1. **High**: развести/склеить дубли-хабы `/kakheti/` vs `/vinnye-tury-gruzia/` и `/tury-v-batumi/` vs `/blog/tury-v-batumi-2026/` — разное намерение или canonical/301.
2. **High**: собрать 5 постов «гид тбилиси» под один пиллар (новый или `/about/saba/` расширить) — прямая каннибализация top-of-funnel коммерческого intent.
3. **Med**: прошить `/tury-na-kazbek/`, `/tury-v-svaneti/`, `/tury-v-batumi/`, `/kakheti/` как явные хабы со ссылками на все спицы из таблицы §4 (сейчас не подтверждено HTML-аудитом — нужен grep по `href` внутри страниц).
4. **Med**: назначить `/blog/chto-posmotret-v-tbilisi/` официальным инфо-пилларом для 15 разрозненных tbilisi-постов, прописать двустороннюю перелинковку.
5. **Low**: добавить 2-3 инфо-спицы под Сванетию (сейчас только 1 пост на 6 тур-страниц).
