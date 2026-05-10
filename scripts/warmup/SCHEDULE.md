# Расписание прогрева — 20 профилей, 3 дня

## Распределение по слотам (не более 3 одновременных из одного гео)

### Day 1 — базовая жизнь (30-45 мин/профиль)

| Слот (UTC) | Профиль | Гео | Локальное время |
|------------|---------|-----|-----------------|
| 05:00-05:45 | P02 MSK_business | Moscow | 08:00 MSK |
| 05:00-05:45 | P10 SPB_business | SPb | 08:00 MSK |
| 05:15-06:00 | P17 DXB_business | Dubai | 09:15 GST |
| 06:00-06:45 | P01 MSK_relocant | Moscow | 09:00 MSK |
| 06:00-06:45 | P05 KZN_family | Kazan | 09:00 MSK |
| 06:15-07:00 | P20 LDN_business | London | 07:15 BST |
| 07:00-07:45 | P03 SPB_relocant | SPb | 10:00 MSK |
| 07:00-07:45 | P08 KRD_family | Krasnodar | 10:00 MSK |
| 07:00-07:45 | P06 NSK_tourist | Novosibirsk | 13:00 NOVT |
| 08:00-08:45 | P07 EKB_relocant | Ekb | 13:00 YEKT |
| 08:00-08:45 | P12 EKB_family | Ekb | 13:00 YEKT |
| 08:00-08:45 | P13 BER_relocant | Berlin | 10:00 CEST |
| 09:00-09:45 | P04 SPB_tourist | SPb | 12:00 MSK |
| 09:00-09:45 | P14 LDN_tourist | London | 10:00 BST |
| 09:00-09:45 | P15 PAR_tourist | Paris | 11:00 CEST |
| 10:00-10:45 | P11 MSK_tourist | Moscow | 13:00 MSK |
| 10:00-10:45 | P16 IST_backpacker | Istanbul | 13:00 TRT |
| 10:00-10:45 | P18 NYC_tourist | New York | 06:00 EDT |
| 11:00-11:45 | P09 MSK_backpacker | Moscow | 14:00 MSK |
| 11:00-11:45 | P19 BER_backpacker | Berlin | 13:00 CEST |

### Day 2 — расширение + travel (40-60 мин/профиль)

Тот же порядок слотов, сдвиг на +30 мин для рандомизации.

| Слот (UTC) | Профиль | Гео |
|------------|---------|-----|
| 05:30-06:30 | P02, P10 | MSK/SPB |
| 05:45-06:45 | P17 | Dubai |
| 06:30-07:30 | P01, P05 | MSK/KZN |
| 06:45-07:30 | P20 | London |
| 07:30-08:30 | P03, P08, P06 | SPB/KRD/NSK |
| 08:30-09:30 | P07, P12, P13 | EKB/BER |
| 09:30-10:30 | P04, P14, P15 | SPB/LDN/PAR |
| 10:30-11:30 | P11, P16, P18 | MSK/IST/NYC |
| 11:30-12:30 | P09, P19 | MSK/BER |

### Day 3 — первое касание travel + Грузия в контексте (45-60 мин/профиль)

Тот же порядок слотов, сдвиг на -15 мин.

---

## Правила неперекрытия

- Максимум 3 профиля из одного города одновременно
- Между двумя профилями из одного города — минимум 15 мин паузы
- Business-профили запускаются раньше (7-9 утра по локали)
- Backpacker-профили запускаются позже (11+ утра по локали)
- Бизнес-сессии короче (25-40 мин), бэкпекеры длиннее (40-60 мин)

## Proxy-провайдеры по гео

| Провайдер | Гео | Профили | Примечание |
|-----------|-----|---------|-----------|
| Brightdata | RU (Moscow, SPb, Novosibirsk) | P01, P04, P06, P10 | Лучшее покрытие RU |
| Brightdata | DE, AE, GB | P13, P17, P20 | Tier-1 страны |
| IPRoyal | RU (Moscow, Ekb) | P02, P07, P09 | Дешевле, хорошие sticky |
| IPRoyal | GB, TR | P14, P16 | |
| Soax | RU (SPb, Kazan, Krasnodar, Moscow) | P03, P05, P08, P11 | Хороший RU coverage |
| Soax | FR, US, DE | P15, P18, P19 | |

### Рекомендации по провайдерам

- **Brightdata**: лучшее качество, $15/GB residential. Для бизнес-профилей и tier-1 стран.
- **IPRoyal**: $7/GB, хорошие sticky до 30 дней. Для бюджетных профилей.
- **Soax**: $8/GB, хорошее покрытие РФ (включая регионы). Для RU-профилей из небольших городов.

## Чек-лист Day 1

- [ ] Все 20 профилей созданы в Multilogin X
- [ ] Прокси привязаны и проверены (ip-check.info с каждого профиля)
- [ ] Google аккаунты залогинены (Gmail + YouTube)
- [ ] .env заполнен (MLX_EMAIL, MLX_PASSWORD, TELEGRAM_*)
- [ ] warmup-config.json заполнен реальными profile ID
- [ ] Node.js 20+ установлен
- [ ] Playwright установлен: `npx playwright install chromium`
- [ ] Тестовый прогон одного профиля: `node warmup.mjs --day 1 --profiles P01`
- [ ] Логи пишутся в scripts/warmup/logs/
- [ ] Telegram-уведомления приходят
- [ ] Проверить что IP каждого профиля соответствует гео (whoer.net)
- [ ] Убедиться что timezone в Multilogin совпадает с прокси
- [ ] Canvas/WebGL fingerprint уникален (browserleaks.com)
