# Sakhva Travel — Индексация (Google, Yandex, Bing)

## Google Indexing API
- **Service Account:** sakhva-indexing@mercurial-shine-465511-h4.iam.gserviceaccount.com
- **Project:** mercurial-shine-465511-h4 (My First Project)
- **JSON-ключ:** ~/sakhva-travel/service-account.json
- **SA верифицирован** как владелец через Site Verification API
- **API:** Web Search Indexing API, Site Verification API

### Скрипт
```bash
python3 ~/sakhva-travel/scripts/google-indexing.py        # все URL из sitemap
python3 ~/sakhva-travel/scripts/google-indexing.py --url URL  # один URL
```
Зависимости: google-auth, google-auth-httplib2, google-api-python-client

## IndexNow (Bing / Yandex)
- **Ключ:** DE25F3FA51D1F1E934763682A270AF53
- **Endpoint:** api.indexnow.org
- Файл ключа: ~/sakhva-travel/DE25F3FA51D1F1E934763682A270AF53.txt

## Yandex Webmaster API
- **Endpoint:** recrawl/queue
- **Квота:** 150 URL/день
- **Токен:** в keychain `yandex-webmaster-token`
- **user_id:** 1997617080

## Первая отправка: 2026-04-26
| Платформа | Отправлено | OK |
|-----------|-----------|-----|
| Google    | 159       | 159 |
| Яндекс   | 149       | 149 |
| Bing      | 159       | 159 |

## SEO Аудит (2026-04-26)
Итоговый скор: **94/100**

| Категория | Баллы |
|-----------|-------|
| Technical SEO (22%) | 21/22 |
| Content/E-E-A-T (23%) | 21/23 |
| On-Page (20%) | 19/20 |
| Schema (10%) | 9/10 |
| Performance (10%) | 9/10 |
| AI Search (10%) | 9/10 |
| Images (5%) | 5/5 |

### Что было сделано для 87→94:
- 15 тонких статей расширены до 1500+ слов
- 50 key-fact блоков для AI-цитируемости
- llms-full.txt (642 строки) создан
- Локальные шрифты вместо Google Fonts (62 файла)
- Hero poster 48KB→25KB
- 20 cross-language ссылок RU↔EN
- Цена Мцхета исправлена: 90→40 лари
