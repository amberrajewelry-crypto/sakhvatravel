# Google Ads Sakhva Travel — полная настройка

## Файлы для импорта
- `campaign-3groups.csv` — кампания (3 группы, 21 ключ, 9 RSA, 53 негатива)
- `campaign-extensions.csv` — расширения (4 sitelinks, 6 callouts, 1 snippet)
- `google-ads-daily-script.js` — скрипт ежедневного отчёта

---

## ШАГ 1: Создать конверсии (5 минут)

Google Ads → Goals → Conversions → + New conversion action → Website

Для каждой: Category = **Lead**, Count = **One**, Window = **30 days**

| # | Название | Value | Что отслеживает |
|---|----------|-------|-----------------|
| 1 | WhatsApp Click | $5 | Клик по кнопке WhatsApp |
| 2 | Telegram Click | $5 | Клик по кнопке Telegram |
| 3 | Booking Form | $10 | Нажал "Забронировать" |
| 4 | Contact Form | $8 | Отправил контактную форму |
| 5 | Phone Click | $3 | Нажал на номер телефона |

При создании выбери **"Use Google Tag Manager"** или **"Install tag manually"**.
Для manual: тег уже на сайте, нужен только Conversion Label.

После создания каждой конверсии Google покажет Conversion Label — 
он выглядит как `AW-8133499399/AbCdEfGhIjKl`.

**Скинь мне все 5 Labels — я заменю в коде сайта за 1 минуту.**

Сейчас на сайте стоят временные метки:
- `AW-8133499399/wa_click` → заменить
- `AW-8133499399/tg_click` → заменить
- `AW-8133499399/booking_form` → заменить
- `AW-8133499399/contact_form` → заменить
- `AW-8133499399/phone_click` → заменить

---

## ШАГ 2: Импорт кампании (3 минуты)

**Вариант A (быстрый):** Google Ads → Tools → Bulk Actions → Uploads → выбрать `campaign-3groups.csv`

**Вариант B (надёжный):** Скачать Google Ads Editor → Account → Import → From CSV

После импорта проверь:
- [ ] 3 группы: Kakheti_Vino, Gid_Tbilisi, Tur_Gruziya
- [ ] 21 ключевое слово
- [ ] 9 объявлений (по 3 на группу)
- [ ] 53 негативных слова
- [ ] Location = Georgia, **Presence only** (НЕ Presence or Interest)
- [ ] Language = Russian
- [ ] Budget = $15/day
- [ ] Schedule = 08:00-23:00

---

## ШАГ 3: Добавить расширения (10 минут)

Google Ads → Ads & assets → Assets

### 3.1 Sitelinks (+ Sitelink → Campaign level)

| Текст ссылки | URL | Описание 1 | Описание 2 |
|-------------|-----|------------|------------|
| Винный тур Кахетия | sakhva-travel.com/tour/kakheti/ | 3 винодельни за 1 день | Дегустация + Сигнахи от $74 |
| Казбеги за 1 день | sakhva-travel.com/tour/kazbegi/ | Троицкая церковь + горы | Трансфер из отеля от $93 |
| Мцхета от $15 | sakhva-travel.com/tour/mtskheta/ | Древняя столица Грузии | Джвари + Светицховели |
| Все 12 маршрутов | sakhva-travel.com/tours/ | Пешие винные ночные | Отмена бесплатно за 24ч |

### 3.2 Callouts (+ Callout → Campaign level)
- Рейтинг 4.9 на Google
- Бесплатная отмена за 24ч
- Ответ за 15 минут
- Группа до 6 человек
- Без комиссий агрегатора
- Оплата в день тура

### 3.3 Structured Snippets (+ Structured snippet → Campaign level)
- Header: **Destinations**
- Values: Казбеги, Кахетия, Мцхета, Старый Тбилиси, Ночной Тбилиси, Батуми

### 3.4 Location Extension
- Assets → Location → Link Google Business Profile
- GBP уже верифицирован (CID 14070083063461040701)

### 3.5 Call Extension
- Assets → Call → +995 511 272 623
- Schedule: 09:00-21:00

---

## ШАГ 4: Скрипт ежедневного отчёта (3 минуты)

1. Создай пустую Google Sheets таблицу
2. Google Ads → Tools → Bulk Actions → Scripts → +
3. Вставь код из `google-ads-daily-script.js`
4. Замени `ВСТАВЬ_ССЫЛКУ_НА_GOOGLE_SHEET` на URL таблицы
5. Run → Authorize → OK
6. Frequency: Daily, 08:00

---

## ШАГ 5: Проверка и запуск

- [ ] Конверсии созданы (5 штук)
- [ ] Labels скинуты мне и заменены в коде
- [ ] Сайт задеплоен с обновлённым трекингом
- [ ] Кампания импортирована
- [ ] Расширения добавлены
- [ ] GBP привязан
- [ ] Скрипт отчётов настроен
- [ ] Location = Presence only (проверить дважды!)
- [ ] Кампания включена
