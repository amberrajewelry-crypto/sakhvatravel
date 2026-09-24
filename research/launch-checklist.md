# Google Ads Launch Checklist -- Sakhva Travel

_Кампания: Sakhva_Search_ROI_
_Аккаунт: AW-8133499399_
_Бюджет: $20/день_

---

## 1. Проверить валюту аккаунта (USD)

**Где:** Google Ads > Settings (шестерёнка) > Account settings > Account currency
- Валюта должна быть USD
- НЕЛЬЗЯ менять после создания аккаунта
- Если не USD -- создать новый аккаунт

---

## 2. Настроить биллинг

**Где:** Google Ads > Billing > Settings
- Добавить карту или банковский счёт
- Выбрать "Automatic payments" (списание после расхода)
- Порог списания: $50 или по итогам месяца
- Проверить что платёж прошёл (тестовое списание ~$1)

---

## 3. Конверсии: проверить трекинг

**Где:** Google Ads > Goals > Conversions > Summary

Должны быть настроены:
- [ ] **WA-клик** -- клик по кнопке WhatsApp (основная конверсия)
- [ ] **begin_checkout** -- начало оформления заказа
- [ ] **payment** -- завершение оплаты

Проверка:
- Открыть сайт в Chrome
- Нажать кнопку WhatsApp
- Google Ads > Goals > Conversions -- статус "Recording" через 24ч
- Google Tag Assistant (tagassistant.google.com) -- проверить что тег AW-8133499399 срабатывает

---

## 4. Импортировать CSV через Google Ads Editor

**Шаги:**
1. Скачать Google Ads Editor: ads.google.com/intl/en/home/tools/ads-editor/
2. Открыть > File > Import > From CSV
3. Выбрать `campaign-import.csv`
4. Preview changes -- проверить что нет ошибок
5. Post changes -- загрузить в аккаунт

**Возможные ошибки при импорте:**
- "Invalid keyword format" -- проверить квадратные скобки для exact match
- "Headline too long" -- заголовок >30 символов (считать кириллицу)
- "Description too long" -- описание >90 символов

---

## 5. Проверить все URL (каждый landing page)

Открыть каждый URL и проверить что страница загружается:

- [ ] https://sakhva-travel.com/tour/kazbegi/
- [ ] https://sakhva-travel.com/tour/kakheti/
- [ ] https://sakhva-travel.com/tour/hidden-tbilisi/
- [ ] https://sakhva-travel.com/tour/old-tbilisi/
- [ ] https://sakhva-travel.com/tour/mtskheta/
- [ ] https://sakhva-travel.com/tour/night-tbilisi/

Проверить на мобильном:
- Страница не обрезается
- Кнопка WhatsApp видна без скролла
- Загрузка <3 секунд

---

## 6. Search Partners: OFF

**Где:** Google Ads > Campaign > Settings > Networks
- [ ] Снять галочку "Include Google search partners"
- Причина: трафик с Search Partners дешевле, но конверсия ниже. Включить позже после оптимизации.

---

## 7. Display Network: OFF

**Где:** Google Ads > Campaign > Settings > Networks
- [ ] Снять галочку "Include Google Display Network"
- КРИТИЧНО: Display Network сольёт бюджет без конверсий для нашего типа бизнеса

---

## 8. Location: Georgia, "Presence" only

**Где:** Google Ads > Campaign > Settings > Locations
1. Выбрать "Georgia" (2268)
2. Нажать "Location options"
3. Выбрать **"Presence: People in or regularly in your targeted locations"**
4. НЕ выбирать "Presence or interest" (по умолчанию!) -- это покажет рекламу людям в России, которые "интересуются" Грузией, но находятся далеко

---

## 9. Language: Russian

**Где:** Google Ads > Campaign > Settings > Languages
- [ ] Выбрать "Russian"
- Это фильтрует по языку браузера пользователя
- Наша ЦА: русскоязычные туристы в Грузии

---

## 10. Ad Schedule: 09:00-22:00

**Где:** Google Ads > Campaign > Ad Schedule
- [ ] Установить показ 09:00-22:00 по местному времени (Georgia, UTC+4)
- Причина: ночью конверсия близка к нулю, а клики расходуют бюджет
- После 2 недель можно проанализировать и сузить

---

## 11. Device adjustments: мобильные +20%

**Где:** Google Ads > Campaign > Devices
- [ ] Мобильные: ставка +20%
- [ ] Десктопы: без изменений (0%)
- [ ] Планшеты: ставка -10%
- Причина: туристы ищут с телефона, конверсия в WhatsApp выше с мобильного

---

## 12. Sitelink extensions: 4 штуки

**Где:** Google Ads > Ads & extensions > Extensions > Sitelinks

| Sitelink | URL | Описание |
|----------|-----|----------|
| Тур в Казбеги | /tour/kazbegi/ | Троицкая церковь, Ананури. От $93 |
| Винный тур Кахетия | /tour/kakheti/ | 3 винодельни за 1 день. От $74 |
| Старый Тбилиси | /tour/old-tbilisi/ | Пешая экскурсия 3 часа. От $42 |
| Экскурсия Мцхета | /tour/mtskheta/ | Древняя столица Грузии. От $15 |

---

## 13. Callout extensions: 4 штуки

**Где:** Google Ads > Ads & extensions > Extensions > Callouts

1. "Рейтинг 4.9 на Google"
2. "Бесплатная отмена за 24ч"
3. "Ответ за 15 минут"
4. "Группа до 6 человек"

---

## 14. Call extension

**Где:** Google Ads > Ads & extensions > Extensions > Calls
- [ ] Номер: +995511272623
- [ ] Страна: Georgia
- [ ] Показывать только на мобильных: ДА
- [ ] Расписание: совпадает с расписанием кампании (09:00-22:00)

---

## Финальная проверка перед запуском

- [ ] Все 14 пунктов выполнены
- [ ] CSV импортирован без ошибок
- [ ] Объявления в статусе "Eligible" или "Under review"
- [ ] Бюджет $20/день установлен
- [ ] Конверсии трекаются (тестовый клик)
- [ ] Запись в daily_tasks.md: "День 1 Google Ads -- проверить одобрение объявлений"
