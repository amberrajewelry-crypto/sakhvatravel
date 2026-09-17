# Backlink Profile — sakhva-travel.com
_Дата: 2026-09-17. Источники: Common Crawl web graph, WHOIS domain history, curl-проверка исходящих ссылок. Moz/Bing/DataForSEO недоступны (Tier 0). Ahrefs MCP подключён в родительской сессии, но не в этой — не использовался._

## Common Crawl web graph (confidence: 0.50, domain-level)
Источник: `commoncrawl_graph.py sakhva-travel.com --json`, релиз cc-main-2026-jan-feb-mar

```json
{
  "in_crawl": false,
  "in_rankings": false,
  "pagerank": null,
  "pagerank_rank": null,
  "harmonic_centrality": null,
  "harmonic_centrality_rank": null,
  "n_hosts": null,
  "top_referring_domains": [],
  "referring_domains_sample": 0,
  "note": "Domain not found in Common Crawl data. It may be too new, too small, or not yet crawled."
}
```

**Домен отсутствует в графе Common Crawl.** Ни PageRank, ни harmonic centrality, ни список referring domains не вернулись — источник дал 0 данных, не низкие значения. Причина, по данным CC: домен слишком новый / некрупный / ещё не проиндексирован в этом релизе CC (квартальный снапшот, следующий выйдет через ~3 мес — возможно, домен появится там).

## WHOIS / domain history (confidence: 0.95 для факта регистрации)
Источник: `domain_history.py sakhva-travel.com --json`

- created: 2026-04-01, updated: 2026-04-25, expires: 2027-04-01
- registrar: Name.com, Inc.
- years_registered: 0.46 (≈5.5 мес)
- topical_shift: не проверялся (нет baseline-topic)

Дата регистрации в WHOIS свежая (апрель 2026). Если сайт эксплуатируется дольше — это может означать смену регистратора/трансфер домена, а не фактический возраст проекта; сам скрипт различий не делает, репортим дату как есть.

## Верификация backlinks (verify_backlinks.py)
Известных обратных ссылок для проверки предоставлено не было — `verify_backlinks.py` не запускался (нет входного файла со ссылками).

## Исходящие ссылки — гигиена (curl --compressed, ручная проверка)

### Главная страница (/)
Проверены все `href="https?://..."` на разметку. Партнёрских ссылок на **travelpayouts, kiwitaxi, localrent, cherehapa — НЕ обнаружено вообще** (0 совпадений по grep). Исходящие домены на главной: instagram.com (11), tripadvisor.ru (2), yandex.ru/yandex.com.ge/mc.yandex.ru, facebook.com, vk.com, t.me, x.com, youtube.com, tiktok.com, threads.com, wa.me, 2gis.ge, maps.app.goo.gl, googletagmanager.com — все соцсети/аналитика, не аффилиаты.

### Страница тура (/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/)
Также 0 ссылок на travelpayouts/kiwitaxi/localrent/cherehapa. Исходящие домены: google.com (2), yandex.com.ge, tripadvisor.ru, googletagmanager.com, t.me, mc.yandex.ru, fonts.gstatic.com.
`rel` на внешних анкорах: 3× `rel="noopener noreferrer"`, 1× `rel="noopener"` — nofollow/sponsored нигде не проставлен, но это неважно, так как аффилиатных ссылок на сайте не найдено.

**Вывод по гигиене:** партнёрские программы (travelpayouts/kiwitaxi/localrent/cherehapa), которые ожидались в задаче, на сайте технически отсутствуют — либо ещё не подключены, либо реализованы иначе (через форму бронирования/бота, не прямой href). Если они добавятся позже — на них сразу нужен `rel="sponsored nofollow"`.

## Итоговая оценка

**INSUFFICIENT DATA для числового Backlink Health Score.** При Tier 0 и пустом ответе Common Crawl из 7 факторов скоринга не закрыт ни один (referring domains, quality distribution, anchor text, toxic ratio, velocity, follow/nofollow, geo — везде 0 данных). Единственный источник с содержательным ответом — WHOIS (возраст домена) и ручная проверка исходящих ссылок (не входящих).

Рекомендация: подключить DataForSEO extension (`./extensions/dataforseo/install.sh`) или Ahrefs (в родительской сессии MCP уже есть — можно попросить оркестратора прогнать через него, т.к. в этом сабагенте Ahrefs недоступен) для реальных цифр referring domains/DR/anchor text.

## 5 реалистичных возможностей для ссылок (Tbilisi tour guide)

1. **GetYourGuide supplier profile** — завести/дополнить листинг туров Sakhva как поставщика на GetYourGuide с прямой ссылкой на сайт в профиле — маркетплейс с высоким трастом, стандартная практика для тур-гидов.
2. **Tripadvisor listing (Attraction/Tour Operator)** — сайт уже ссылается на tripadvisor.ru исходящими линками; обратная связь — оформить/актуализировать профиль оператора на Tripadvisor со ссылкой на sakhva-travel.com в разделе "website".
3. **Русскоязычные travel-блоги о Грузии** (тематические ниши: "Грузия самостоятельно", блогеры про Кавказ/Батуми/Кахетию) — гостевой пост или упоминание в подборке "гиды в Тбилиси" с бэклинком; искать через Яндекс/Google по запросам вида "гид в Тбилиси рекомендации блог".
4. **Грузинские туристические каталоги/агрегаторы** (напр. GNTA — Georgian National Tourism Administration партнёрский реестр, Georgia.travel, локальные directories типа Tbilisi.travel/city guides) — регистрация как локальный тур-оператор с NAP-данными и ссылкой.
5. **Локальные напрвления/партнёрства** — отзыв/ссылка от отелей/хостелов Тбилиси, с которыми Sakhva сотрудничает по трансферам (у сайта уже есть WhatsApp-бот для клиентов) — договориться о размещении на страницах "рекомендуемые экскурсии" партнёрских отелей.
