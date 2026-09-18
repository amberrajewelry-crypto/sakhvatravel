# Sakhva Travel — строгий полный SEO-аудит (18.09.2026)

Метод: 9 специализированных проходов (technical, content, schema, sitemap/on-page, performance, visual, geo, local, sxo) по живому сайту + локальному репо; каждый Critical/High перепроверен вручную (grep по репо / curl по проду) до включения в отчёт. Отчёты по блокам — `findings/*.md`.

## SEO Health Score: 74 → 80 после фиксов этой сессии

| Категория | Вес | Балл (до) | Балл (после) | Основание |
|---|---|---|---|---|
| Technical | 22% | 78 | 90 | viewport GE (111 стр.) и EN-редиректы починены; остались 308-хоп на 404, image-sitemap |
| Content | 23% | 78 | 78 | 460+/500+ противоречие не решено (вопрос владельцу); AI-клише в 10 EN постах |
| On-page/Sitemap | 20% | 71 | 71 | 84 гео-страниц с 86,5% схожести; 56 EN/GE гео вне sitemap; битые image-URL |
| Schema | 10% | 78 | 92 | 2 невалидных JSON-LD починены; CollectionPage/author/даты добавлены; seller-стабы → @id |
| Performance | 10% | 62 | 62 | измерены 2/7 стр.: `/` TBT 540 мс, `/en/` LCP 2,9 с; deferred.css 85% не используется |
| AI readiness (GEO) | 10% | 79 | 79 | llms.txt 80/754 URL; ответы-пассажи есть на 6/6 стр. |
| Images | 5% | 70 | 70 | 18 записей image-sitemap на 5 отсутствующих файлов |
| Local (вне формулы) | — | 61 | 75 | карта на CID, видимый адрес; GBP 4.6/10 vs сайт 4.9/90+ без атрибуции источника |
| SXO (вне формулы) | — | 62 | 62 | «экскурсии из Тбилиси» → хаб стран, а SERP ждёт каталог однодневок |

## Что подтверждено и исправлено сегодня (задеплоено)
1. Critical/Technical — `ინიtial-scale` вместо `initial-scale` в 111 файлах `ge/` (мобильный масштаб ломался) → починено. Плюс 45 порченых переводчиком токенов: `schema.org/ბლოგიPosting`, `Listპუნქტი`, `Google ნაკლოვანებებიent Mode`, бренды (Carrefour, Bassiani, Mastercard…).
2. Critical/Schema — невалидный JSON-LD: `blog/gruzinskie-frazy` (HTML в ответе FAQ), `blog/metro-tbilisi` (незакрытый `image[]`).
3. Critical/Local — карта на `/contacts/` (ru/en/ge) вела на общий пин Тбилиси → embed на CID 14112587239859278397; добавлен видимый адрес (NAP) над картой.
4. High/Technical — 14 редиректов `/en/tury-v-gruziyu-iz-*/` уводили на RU → теперь на `/en/tours-from-*/`.
5. High/Content+Schema — `about/` (ru/en/ge): `author`, `datePublished`, `dateModified`; `tury-v-gruziyu/`: узел `CollectionPage` + `TravelAgency#business`, 12 seller-стабов заменены на `@id`.
6. GEO — блок «Тур по теме» на `blog/metro-tbilisi` перенесён ниже прямого ответа.

## Открытые находки (по убыванию веса)

### Требуют решения владельца
- **«460+ туров» (главная) против «500+ туров» (подпись автора на 790 страницах, about ru/en/ge).** Одна цифра должна быть везде. Скажите какая — замена делается одним проходом.
- **Рейтинг 4.9/90+ без указания источника** рядом с hero (`index.html:193`) при GBP 4.6/10. Цифры подтверждены владельцем; нужно только добавить «по отзывам Google, Яндекс, Tripadvisor» — это hero главной, трогаю только по команде.
- **84 гео-страниц «туры из <город>» (28×3 локали) при 86,5% общего текста** — по правилам аудита это doorway-риск (hard-stop >50). Варианты: (1) оставить 28 RU в индексе, EN/GE закрыть noindex (они и так вне sitemap, но индексируемы); (2) добавить по 150–200 уникальных слов на город (рейсы/цены/время в пути). Рекомендую 1 сейчас + 2 постепенно.

### Делаются без вопросов (следующая итерация)
- Performance: `/` TBT 540 мс — разобрать long tasks main.js (нельзя без команды) и виджеты; `deferred.css` 85% неиспользуемого; `/en/` LCP 2,9 с vs 2,1 с на RU — найти локальный ресурс. Домерить 5/7 страниц (Lighthouse LanternError).
- Sitemap: 18 image-записей на 5 отсутствующих файлов; 56 EN/GE гео-страниц вне sitemap при RU внутри; 7 страниц без description; lastmod на 2 даты.
- Crawlable мусор: `scripts/_xdefault_backup_20260704/`, `gid/_template/` — закрыть (robots/sitemap — только по команде).
- Сироты (0 входящих): `dashboard/`, `oplata/`, `en/pay/`, `ge/gadakhda/`, `partner/`.
- Visual: временный горизонтальный скролл на мобильном Казбеги из-за строки live-погоды; 0 CTA above-the-fold на `/tury-v-gruziyu/` mobile.
- Content: «hidden gem»-клише в 10 EN постах; `ge/blog/tbilisoba` 1 262 слова.
- Schema: `about/` TravelAgency без telephone/sameAs на верхнем узле.
- GEO: llms.txt покрывает 80/754; `docs/wikidata-entity.md` устарел (Q140518485 существует).
- SXO: отдельная страница-каталог «Экскурсии из Тбилиси на 1 день» (SERP: 8/9 — агрегаторные листинги); Казбеги — галерея 3→10+ фото, видео выше; EN transfer — таблица сравнения сверху + title под CTR.

## Ограничения
- Performance: 2/7 страниц (PSI без ключа — rate-limit; Lighthouse LanternError). Данные памяти 17.09: LH подстраниц 9x/100/100/100.
- Backlinks: Ahrefs «Insufficient plan», Moz/Bing ключей нет — блок не оценён.
- GBP API: квота 0 (тикет 3-6965000041597) — фото/посты/Q&A не проверены.
- Google Places: биллинг отключён по решению владельца — живые отзывы через API невозможны.

## Как поймём, что сработало (ведущие индикаторы)
- GSC → Mobile usability / Page experience: 0 ошибок по `ge/blog/*` через 2–3 недели.
- GSC Enhancements → 0 невалидных FAQ/Product.
- GSC Performance по `/en/tours-from-*` — рост показов после смены редиректов.
- `python3 scripts/gsc-ctr-check.py` 02.10 — сравнение CTR с бейзлайном.
