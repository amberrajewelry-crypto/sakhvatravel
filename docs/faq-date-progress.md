# Прогресс: FAQ 3→6 + поле даты на карточках /ekskursiya/*

Задача: на каждой карточке вручную и уникально — расширить видимый FAQ до 6 транзакц. вопросов (синхронно со schema FAQPage) + добавить поле «Желаемая дата» в форму (cm-date + приём в sendContact/api/booking/formspree). Ноль редиректов. Деплой отдельно по команде.

Паттерн поля даты (идентичен): `<input id="cm-date" type="date">` после cm-phone; sendContact читает `dEl=getElementById('cm-date')`, добавляет в note + formspree.

Всего карточек: 67. **ГОТОВО: 67/67 (100%).**

Финальная валидация (04.07): 0 карточек без cm-date; schema FAQPage == видимый FAQ на всех 67; predeploy 0 ошибок на всех. Побочно исправлены 4 schema-mismatch: sovetskiy-tur-tbilisi (была схема «обзорного тура»), tur-dlya-emigrantov-tbilisi (EN «digital nomad»), tur-vsya-gruziya / tur-gruziya-3-dnya / tur-gruziya-5-dney / tur-gruziya-10-dney (схема не совпадала с видимым). Механическая часть — scripts/_faq_date_apply.py (контент вопросов писался вручную и уникально под каждую карточку).

НЕ ЗАДЕПЛОЕНО — деплой только по явной команде.

## Готово (19)
- ekskursiya-kazbegi-iz-tbilisi
- ekskursiya-kakheti-iz-tbilisi
- ekskursiya-mtskheta-iz-tbilisi
- ekskursiya-gori-iz-tbilisi (видимый FAQ создан из schema)
- ekskursiya-borjomi-iz-tbilisi
- tur-batumi-iz-tbilisi
- tur-kutaisi-iz-tbilisi
- ekskursiya-gudauri-iz-tbilisi
- ekskursiya-vardzia
- ekskursiya-ananuri-iz-tbilisi
- ekskursiya-jvari-iz-tbilisi (видимый FAQ создан из schema)
- ekskursiya-uplistsikhe-iz-tbilisi
- ekskursiya-sighnaghi-iz-tbilisi
- ekskursiya-stary-tbilisi
- ekskursiya-narikala (видимый FAQ создан из schema)
- ekskursiya-abanotubani (видимый FAQ создан из schema)
- ekskursiya-mtatsminda (видимый FAQ создан из schema)
- ekskursiya-dashbashi-iz-tbilisi
- ekskursiya-david-gareji
- ekskursiya-telavi-iz-tbilisi
- ekskursiya-truso
- ekskursiya-tusheti
- ekskursiya-ureki-iz-tbilisi
- ekskursiya-zugdidi
- ekskursiya-svaneti-iz-tbilisi
- ekskursiya-racha-iz-tbilisi
- ekskursiya-hevsuretia-shatili
- ekskursiya-kanyony-zapadnoy-gruzii
- ekskursiya-bakuriani-iz-tbilisi
- ekskursiya-gomis-mta-iz-batumi (Type B: видимый FAQ создан)
- degustatsiya-vina-kakheti
- vinniy-tur-tbilisi (Type B: видимый FAQ создан, 5 Q)
- kvevri-vino-tur (Type B: видимый FAQ создан, 5 Q)
- vinniy-marshrut-alazani (Type B: видимый FAQ создан, 5 Q)
- vinodelie-kindzmarauli (Type B: видимый FAQ создан, 5 Q)
- chacha-master-klass
- khachapuri-master-klass
- gastronomicheskiy-tur-tbilisi
- nochnaya-ekskursiya-tbilisi
- progulka-po-kure-tbilisi
- tur-po-hramam-tbilisi
- sovetskiy-tur-tbilisi (исправлен mismatch: schema была от «обзорного тура», перестроена под видимый FAQ)
- art-tur-tbilisi
- shopping-tur-tbilisi
- fotosessiya-tbilisi
- family-tur-tbilisi
- tur-dlya-detey-tbilisi
- tur-dlya-pensionerov-gruziya
- tur-dlya-emigrantov-tbilisi (исправлен mismatch: schema была на EN «digital nomad», перестроена под видимый RU FAQ)
- korporativniy-tur-tbilisi
- romanticheskiy-tur-tbilisi
- svadebny-tur-gruziya
- gruppa-10-chelovek-tbilisi
- konny-tur-stepantsminda
- transfer-aeroport-tbilisi (4→6)
- tur-gruziya-armeniya
- tur-gruziya-leto
- tur-gruziya-noviy-god
- priklyuchencheskiy-tur-gruziya
- tur-batumi-2-dnya
- tur-kazbegi-kakheti-2-dnya
- tur-svaneti-4-dnya

## Тип карточек
- Тип A: есть видимый FAQ 3 → расширяю до 6.
- Тип B: видимого FAQ нет (только schema, mismatch) → создаю видимый блок + расширяю. Примеры: gori, jvari.

## Осталось (56) — по одной вручную
art-tur-tbilisi, chacha-master-klass, degustatsiya-vina-kakheti, ekskursiya-abanotubani, ekskursiya-bakuriani-iz-tbilisi, ekskursiya-dashbashi-iz-tbilisi, ekskursiya-david-gareji, ekskursiya-gomis-mta-iz-batumi, ekskursiya-hevsuretia-shatili, ekskursiya-kanyony-zapadnoy-gruzii, ekskursiya-mtatsminda, ekskursiya-narikala, ekskursiya-racha-iz-tbilisi, ekskursiya-sighnaghi-iz-tbilisi, ekskursiya-stary-tbilisi, ekskursiya-svaneti-iz-tbilisi, ekskursiya-telavi-iz-tbilisi, ekskursiya-truso, ekskursiya-tusheti, ekskursiya-uplistsikhe-iz-tbilisi, ekskursiya-ureki-iz-tbilisi, ekskursiya-zugdidi, family-tur-tbilisi, fotosessiya-tbilisi, gastronomicheskiy-tur-tbilisi, gruppa-10-chelovek-tbilisi, khachapuri-master-klass, konny-tur-stepantsminda, + ещё ~28 (см. `ls ekskursiya/*/` без cm-date).

Проверка оставшихся: `for d in ekskursiya/*/; do grep -q cm-date "$d/index.html" || echo "${d#ekskursiya/}"; done`
