# Google Ads — Sakhva Travel

## Аккаунт
- Account ID: 8133499399 (MCC) → 7002261178 (клиент)
- Email: ay.alians26@gmail.com
- Composio: googleads_genoa-gooma (ACTIVE)
- API: composio proxy + GOOGLEADS_SEARCH_STREAM_GAQL

## Текущие настройки (14.05.2026)

### Кампании

| Кампания | Статус | Стратегия | Бюджет | Цель |
|----------|--------|-----------|--------|------|
| Sakhva_Search_Flagships | ENABLED | MANUAL_CPC | $30/day | Казбеги, Кахетия, Мцхета — лучший ROI |
| Sakhva_Search_General | ENABLED | MANUAL_CPC | $15/day | Общие запросы, гид, экскурсии |
| Sakhva_Search_Destinations | ENABLED | MANUAL_CPC | $5/day | Кутаиси, Батуми, Боржоми |
| Sakhva_Search_EN_Tourists | ENABLED | MANUAL_CPC | $5/day | EN аудитория, Kakheti_EN ждёт модерацию |

### Ad Groups и ставки

| Кампания | Ad Group | Max CPC | Заметки |
|----------|----------|---------|---------|
| Flagships | Kazbegi | $0.65 | CTR 12.9%, CPA $12, лучший конвертер |
| Flagships | Kakheti_Wine | $0.60 | Объявления без алкоголя (пересозданы 14.05) |
| Flagships | Mtskheta | $0.35 | CPA $3.97 — лучший в аккаунте |
| General | Tours_General | $0.40 | LP: /tour/soviet/ (было /), CPA $39 |
| General | Gid_Tbilisi | $0.55 | LP: /tour/soviet/ (было /), NEW 14.05 |
| General | Excursions_City | $0.50 | NEW 14.05 — пешеходные/обзорные |
| General | Gastro_Tours | $0.50 | NEW 14.05 — гастро/ужин |
| Destinations | Kutaisi | $0.35 | Оживлено с $0.01 |
| Destinations | Batumi | $0.35 | Оживлено с $0.01 |
| Destinations | Borjomi | $0.35 | Оживлено с $0.01 |
| EN_Tourists | Tbilisi_Tours_EN | $0.40 | PAUSED |
| EN_Tourists | Kazbegi_EN | $0.45 | PAUSED |
| EN_Tourists | Kakheti_EN | $0.40 | Модерация: LP очищена от алкоголя, ждём 24-48ч |

### Минус-слова
- **1635 штук** синхронизированы во все 4 кампании
- EN: 100 (casino, hotel, flight, visa, etc.)
- RU: что посмотреть, самостоятельно, бесплатно, форум, отзывы, погода, карта, видео, фото, блог, достопримечательности, куда сходить, маршрут самостоятельно, экскурсовод, gou trip

### Ad Schedule
- 0:00-8:00: -30% ставки (Пн-Пт), -50% (Сб)
- Применено к Flagships и General

### Extensions (уровень аккаунта)
- 10 sitelinks (Казбеги, Кахетия, Ночной Тбилиси, Все туры + старые)
- 4 callouts: Бесплатная отмена, Рейтинг 4.9, Ответ за 15 минут, Оплата после тура
- 2 structured snippets (Destinations, Услуги)
- 1 call extension
- 1 business logo

### Конверсии
- GA4 → Google Ads: generate_lead, qualify_lead, close_convert_lead
- PostHog: form_submit, cta_click, whatsapp_click

## Базовые метрики (30 дней до оптимизации)

| Метрика | Значение |
|---------|----------|
| Расход | $341 |
| Клики | 706 |
| Конверсии | 16 |
| CPA | $21.31 |
| CPC | $0.48 |
| CTR | 7.4% |
| CR | 2.3% |
| IS Flagships | 34% |
| IS General | 36% |

## Оценка: 8/10 (обновлено 14.05 вечер)

### Сильные стороны
- CTR 7.4% (выше среднего для туризма 3-5%)
- CPC $0.49 (дёшево для ниши)
- Flagships CPA $10.41 (ROI 4-7x)
- Mtskheta CPA $3.97, Kazbegi $12.04 — лучшие ad groups
- 1635 минус-слов во всех 4 кампаниях
- Manual CPC — полный контроль
- Все RSA "Отличное"/"Хорошее" качество
- LP оптимизированы: H1 с ключами, Final URL на быстрые страницы (LCP 380ms)
- Enhanced Conversions включены

### Слабые стороны
- LP Experience BELOW_AVERAGE у 92% ключей (QS avg 5.6) — H1 и URL исправлены, ждём пересчёт 3-7 дней
- IS 36-38% — теряем 53-64% аукционов из-за ранга
- General CPA $39 — в 4 раза хуже Flagships
- Kakheti_EN — отклонено (алкоголь), LP очищена, ждём пересмотр модерации
- Нет ремаркетинга

## Изменения 14.05.2026

### Утро (структура и ставки)
1. TARGET_SPEND → MANUAL_CPC (все кампании)
2. Бюджеты: Flagships $30, General $15, Destinations $5
3. Destinations оживлена ($0.01 → $0.35)
4. 2 алкогольных объявления Kakheti исправлены
5. +3 тематических ad groups в General (Gid, Excursions, Gastro)
6. EN кампания создана (3 ad groups, 12 ключей, 3 RSA)
7. 1635 минус-слов синхронизированы
8. +4 sitelinks, +4 callouts, +1 structured snippet
9. Waste BROAD ключи приостановлены (-$60/мес)
10. Ad schedule ночь -30%/-50%
11. Ставки Flagships подняты до $0.60-0.65
12. +13 RU информационных минус-слов

### Вечер (LP Experience + алкоголь fix)
13. H1 оптимизированы под Ads-ключи:
    - Kazbegi: "Тур в Казбеги из Тбилиси за 1 день — от ₾175 с гидом"
    - Kakheti: "Винный тур в Кахетию из Тбилиси — от ₾170 с гидом"
    - Mtskheta: "Экскурсия в Мцхету из Тбилиси — от ₾90 с гидом"
    - Soviet: "Обзорная экскурсия по Тбилиси с частным гидом — от ₾135"
14. Final URL исправлены (через Playwright UI):
    - Tours_General: sakhva-travel.com → /tour/soviet/ (LCP 7.7s → 380ms)
    - Gid_Tbilisi: sakhva-travel.com/ → /tour/soviet/ (LCP 7.7s → 380ms)
15. EN LP /en/tour/kakheti/ очищена от алкоголя:
    - 68 вхождений wine/tasting/winery → заменены на cuisine/tradition/estate
    - 0 алкогольных слов на странице
    - Задеплоено на прод
16. Kakheti_EN RSA: "Georgian Tasting Included" → "Georgian Cuisine Included", описание без tasting
17. Все изменения задеплоены на sakhva-travel.com

## Ежедневный мониторинг

### Чек-лист
- [ ] IS Flagships (цель: 50%+, было 34%)
- [ ] IS General (цель: 40%+, было 36%)
- [ ] Дневной расход (цель: $20-30, было $11)
- [ ] Конверсии (цель: 1+/день)
- [ ] CPA (цель: <$20)
- [ ] Новые search terms — добавлять минус-слова

### Команды для проверки (Composio)
```bash
# Дневные метрики
composio execute GOOGLEADS_SEARCH_STREAM_GAQL -d '{"query": "SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros FROM campaign WHERE segments.date = \"2026-05-15\" AND campaign.status = \"ENABLED\""}'

# Impression Share
composio execute GOOGLEADS_SEARCH_STREAM_GAQL -d '{"query": "SELECT campaign.name, metrics.search_impression_share, metrics.search_rank_lost_impression_share FROM campaign WHERE segments.date DURING LAST_7_DAYS AND campaign.status = \"ENABLED\""}'

# Поисковые запросы (слив)
composio execute GOOGLEADS_SEARCH_STREAM_GAQL -d '{"query": "SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_7_DAYS AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 20"}'
```

## TODO

### Срочно (15-16 мая)
- [ ] Проверить модерацию Kakheti_EN (24-48ч после очистки LP)
- [ ] В UI: запаузить ключ "kakheti wine tour" в Kakheti_EN → заменить на "kakheti day trip"
- [ ] В UI: sitelink "Кахетия вино от $40/чел" → убрать слово "вино"
- [ ] Проверить IS через 3 дня (цель: 50%+ Flagships)
- [ ] Мониторить Destinations — появились ли показы
- [ ] Проверить QS через 5-7 дней (ожидаем рост после LP fix)

### Важно (следующая неделя)
- [x] LP Experience: H1 с ключевыми словами — DONE 14.05
- [x] Final URL на быстрые LP — DONE 14.05
- [x] EN LP очищена от алкоголя — DONE 14.05
- [ ] Переключить BROAD→PHRASE в General оставшиеся
- [ ] Перераспределить бюджет: General $10, Flagships $35 (после QS пересчёта)

### На перспективу
- [ ] Ремаркетинг (Display) — CPC $0.05-0.15, бюджет $3-5/день
- [ ] Offline conversions из Airtable CRM (gclid → n8n → Ads API)
- [ ] При 30+ conv/мес → Maximize Conversions

## Гео
- Только Грузия (PRESENCE) — НЕ МЕНЯТЬ
- Аудитория: русскоязычные в Тбилиси + EN туристы
