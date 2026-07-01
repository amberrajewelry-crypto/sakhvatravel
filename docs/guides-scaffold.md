# Каркас гидов — как устроено и как добавить гида

**Дата:** 2026-06-26 · статус: КАРКАС ГОТОВ, НЕ ЗАДЕПЛОЕН (ждём реальных 2-3 гидов).

## Архитектура

| Часть | Файл | Роль |
|-------|------|------|
| Данные | `data/guides.json` | Источник правды. Карточки рендерятся отсюда (как `/ekskursiya/` из `catalog.json`). |
| Каталог | `gidy-tbilisi/index.html` | Страница `/gidy-tbilisi/` — сетка карточек гидов, fetch `guides.json`. Готова, предеплай 0 ошибок. |
| Шаблон профиля | `gid/_template/index.html` | Болванка `/gid/<slug>/` с плейсхолдерами `{{...}}` + Person-схема. В `.vercelignore` — в прод не уходит. |

**Тимур (реальный, уже на сайте):** карточка в каталоге ведёт на существующий `/chastniy-gid-tbilisi/` (3380 слов, Person+aggregateRating) — НЕ на `/gid/timur/`, чтобы не каннибализировать ранжирующуюся страницу. Новые гиды получают свой `/gid/<slug>/`.

## Добавить нового гида (только РЕАЛЬНЫЙ человек, с его согласия — 152-ФЗ)

1. Фото гида → `/images/<slug>.webp`.
2. Запись в `data/guides.json` → массив `guides` (схема — см. объект Тимура). `status:"active"`, `profile_url:"/gid/<slug>/"`.
3. Профиль: `cp -r gid/_template gid/<slug>`, заменить все `{{...}}` реальными данными.
4. Бамп `?v=` у `guides.json` в `gidy-tbilisi/index.html` (2 места: preload + fetch).
5. `node scripts/predeploy-check.js gid/<slug>/index.html gidy-tbilisi/index.html index.html` → 0 ошибок.
6. Deploy → отправить URL в индекс (`scripts/google-indexing.py --url ...` + IndexNow).

## Что ещё сделать при выкате (НЕ сделано — каркас без деплоя)

- Перелинковка: ссылка на `/gidy-tbilisi/` с главной и/или из футера + с хаба `/ekskursiya/` (анкор «Наши гиды»/«Гиды в Тбилиси»). Сейчас страница ни на что не залинкована.
- EN-версия каталога `/en/...` при необходимости (поля `*_en` в `guides.json` уже есть).
- Реальные отзывы по гидам (если появятся) — Review-схема на профиле.

## Плейсхолдеры шаблона
`{{NAME}} {{ROLE}} {{SLUG}} {{PHOTO}} {{PHOTO_ALT}} {{LANGS}} {{RATING}} {{REVIEWS_COUNT}} {{TOURS_COUNT}} {{EXPERIENCE_YEARS}} {{SPEC_1..4}} {{BIO_PARA_1}} {{BIO_PARA_2}} {{META_DESC}}`
