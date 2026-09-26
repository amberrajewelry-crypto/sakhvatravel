#!/usr/bin/env python3
"""Winter 2-day packages: Gudauri+Kazbegi and Borjomi+Bakuriani, RU/EN/GE (6 URLs).

Pages are cloned from tur-kazbegi-kakheti-2-dnya (same nav/footer/CSS/LocalBusiness),
head meta + JSON-LD + <main> content are rebuilt from PACKAGES below.
Anti-cannibal: titles/H1 own "2 дня / с ночёвкой / зимой"; day-trip pages keep
"за 1 день"; cross-links make the split explicit. Idempotent: re-run overwrites pages,
link blocks are guarded by data-sk="winter-2d".

Run: python3 scripts/build-winter-packages.py
"""
import html
import json
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL_SLUG = "tur-kazbegi-kakheti-2-dnya"
SITE = "https://sakhva-travel.com"
TODAY = "2026-09-26"
WA = "995511272623"
PREFIX = {"ru": "", "en": "/en", "ge": "/ge"}
MARK = 'data-sk="winter-2d"'

UI = {
    "ru": dict(pp="с человека", dur="длительность", days="2 дня", grp="до 7", grp_l="человек",
               night="ночь", cancel="отмена с возвратом", book="Забронировать от {p} лари",
               book_online="Забронировать онлайн", route_lbl="Маршрут", route_h="Программа по дням",
               inc="Включено в стоимость", exc="Не включено", faq="Часто задаваемые вопросы",
               short="Коротко:", see="Смотрите также", home="Главная", tours="Экскурсии",
               tours_url="/ekskursiya/", wa="Хочу забронировать", rating="★ 4.9/5 · ответ за 15 мин",
               cta="Готовы ехать в горы?", cta_sub="Sakhva Travel · рейтинг 4.9 · русскоязычные гиды"),
    "en": dict(pp="per person", dur="duration", days="2 days", grp="up to 7", grp_l="people",
               night="night", cancel="free cancellation", book="Book from ₾{p}",
               book_online="Book online", route_lbl="Route", route_h="Day-by-day itinerary",
               inc="Included", exc="Not included", faq="Frequently asked questions",
               short="In short:", see="See also", home="Home", tours="Tours",
               tours_url="/en/tours-in-georgia/", wa="I want to book", rating="★ 4.9/5 · reply in 15 min",
               cta="Ready for the mountains?", cta_sub="Sakhva Travel · rated 4.9 · local guides"),
    "ge": dict(pp="ერთ ადამიანზე", dur="ხანგრძლივობა", days="2 დღე", grp="7-მდე", grp_l="ადამიანი",
               night="ღამე", cancel="უფასო გაუქმება", book="დაჯავშნა ₾{p}-დან",
               book_online="ონლაინ დაჯავშნა", route_lbl="მარშრუტი", route_h="პროგრამა დღეების მიხედვით",
               inc="ფასში შედის", exc="ფასში არ შედის", faq="ხშირად დასმული კითხვები",
               short="მოკლედ:", see="ასევე ნახეთ", home="მთავარი", tours="ექსკურსიები",
               tours_url="/ge/ekskursiya/", wa="მინდა დაჯავშნა", rating="★ 4.9/5 · პასუხი 15 წუთში",
               cta="მზად ხართ მთებისთვის?", cta_sub="Sakhva Travel · რეიტინგი 4.9 · ადგილობრივი გიდები"),
}

PACKAGES = {
    "tur-gudauri-kazbegi-2-dnya": {
        "price": 520, "img": "gudauri-zima", "img_wh": (1600, 840), "video": "gudauri-drone.mp4", "night_place": {
            "ru": "Гудаури", "en": "Gudauri", "ge": "გუდაური"},
        "ru": {
            "title": "Гудаури и Казбеги за 2 дня — зимний тур с ночёвкой от ₾520",
            "h1": "Гудаури + Казбеги: зимний тур на 2 дня",
            "name": "Гудаури + Казбеги за 2 дня зимой",
            "desc": "Зимний тур на 2 дня из Тбилиси от ₾520: лыжи в Гудаури, ночь в горах, Крестовый перевал и Гергети в снегу. Отель с завтраком включён.",
            "short": "Гудаури + Казбеги — зимний тур на 2 дня из Тбилиси с ночёвкой в Гудаури, от ₾520 "
                     "с человека, группа до 7 человек. День 1 — склоны Гудаури, день 2 — Крестовый "
                     "перевал, Степанцминда и Гергети. Сезон — обычно с конца декабря до начала апреля.",
            "intro": "Однодневной поездки в Гудаури зимой мало: 4–5 часов дороги туда-обратно съедают "
                     "половину катания. В двухдневном туре вы ночуете прямо у склонов, катаетесь полный "
                     "день, а утром второго дня едете через Крестовый перевал к Казбеку — пока дорога "
                     "чистая и небо обычно ясное.",
            "days": [
                ("День 1 — Гудаури", "Тбилиси → Жинвальское водохранилище → Ананури → Гудаури (120 км, "
                 "около 2,5 часа). Катание, инструктор или прогулка по курорту; вечером — ужин с видом "
                 "на горы и ночь в отеле Гудаури."),
                ("День 2 — Казбеги", "Крестовый перевал (2379 м) → арка Дружбы → Степанцминда → "
                 "церковь Гергети (2170 м) и вид на Казбек (5047 м). Возвращение в Тбилиси к 19:00–20:00."),
            ],
            "details": [
                ("Первый день: склоны Гудаури",
                 "Выезд из Тбилиси в 08:00, по дороге — короткая остановка у крепости Ананури над "
                 "Жинвальским водохранилищем. К 11:00 вы в Гудаури (2196 м): верхние станции подъёмников "
                 "поднимаются выше 3000 м, трассы есть и для новичков, и для опытных. Ски-пасс, прокат "
                 "и инструктора помогаем взять на месте — без очередей и переплаты. Не катаетесь? "
                 "Прогулка по курорту, подъём на канатке ради видов, полёт на параплане в тандеме "
                 "(по погоде) или просто терраса с глинтвейном. Вечер и ночь — в отеле Гудаури, "
                 "завтрак включён."),
                ("Второй день: Крестовый перевал и Гергети",
                 "После завтрака едем через Крестовый перевал (2379 м) к смотровой «Арка Дружбы» "
                 "над Гудаурской котловиной и дальше в Степанцминду (1740 м). Зимой к церкви Гергети "
                 "поднимаются на джипе, когда дорога открыта, — это 15 минут по снегу; оттуда лучший "
                 "вид на Казбек. Обед в Степанцминде (хинкали, чакапули, местное пиво) и возвращение "
                 "в Тбилиси к 19:00–20:00."),
                ("Если закроют перевал",
                 "Зимой участок Гудаури — Коби иногда закрывают из-за снегопада и лавинной опасности. "
                 "Мы следим за сводками дорожной службы и меняем программу без доплаты: второй день "
                 "катания в Гудаури или Ананури и Мцхета на обратном пути. Поездку в Казбеги можно "
                 "перенести на другой день вашего отпуска."),
            ],
            "tips": ["Тёплая непромокаемая одежда, шапка, перчатки и солнцезащитные очки — на высоте "
                     "2000+ м снег сильно слепит", "Наличные ₾150–250 на ски-пасс, прокат и обед",
                     "Горнолыжный костюм можно взять в прокате в Гудаури",
                     "Паспорт — нужен для ски-пасса и отеля"],
            "inc": ["Минивэн на зимней резине на оба дня", "Гид-водитель на русском языке",
                    "Ночь в отеле Гудаури (2-местный номер, завтрак)", "Остановки в Ананури и на "
                    "Крестовом перевале"],
            "exc": ["Ски-пасс, прокат, инструктор", "Обеды и ужины", "Джип до Гергети (оплата на месте)",
                    "Параплан и другие активности"],
            "faq": [
                ("Чем этот тур отличается от однодневной экскурсии в Гудаури?",
                 "Однодневная экскурсия в Гудаури стоит от ₾225 и возвращается в Тбилиси вечером — на "
                 "склонах остаётся 4–5 часов. В двухдневном туре за ₾520 вы ночуете в Гудаури, "
                 "катаетесь полный день и на второй день видите Казбеги и Гергети."),
                ("Сколько стоит тур Гудаури + Казбеги на 2 дня и что входит?",
                 "От ₾520 с человека: транспорт на оба дня, гид-водитель и ночь в отеле Гудаури с "
                 "завтраком. Ски-пасс, прокат, обеды и джип до Гергети оплачиваются на месте."),
                ("Нужно ли уметь кататься на лыжах?",
                 "Нет. Новичкам берём инструктора на 1–2 часа, а тем, кто не катается, предлагаем "
                 "канатку ради видов, параплан или прогулку по курорту."),
                ("Что будет, если закроют Крестовый перевал?",
                 "Меняем программу без доплаты: второй день катания в Гудаури или Ананури и Мцхета. "
                 "Казбеги можно перенести на другой день."),
                ("Когда сезон в Гудаури?",
                 "Обычно с конца декабря до начала апреля — в сезоне 2025/26 подъёмники открылись "
                 "27 декабря. Точные даты зависят от снега. На "
                 "новогодние праздники места в отелях лучше бронировать за 3–4 недели."),
            ],
        },
        "en": {
            "title": "Gudauri & Kazbegi 2-Day Winter Tour from Tbilisi — ₾520",
            "h1": "Gudauri & Kazbegi 2-Day Winter Tour",
            "name": "Gudauri & Kazbegi 2-Day Winter Tour",
            "desc": "2-day winter tour from Tbilisi from ₾520 per person: skiing in Gudauri, a night in the mountains, the Cross Pass and snowy Gergeti. Hotel included.",
            "short": "Gudauri & Kazbegi is a 2-day winter tour from Tbilisi with a night in Gudauri, "
                     "from ₾520 per person, up to 7 people. Day 1 — Gudauri slopes, day 2 — the Cross "
                     "Pass, Stepantsminda and Gergeti. Season: usually late December to early April.",
            "intro": "A Gudauri day trip in winter is short: 4–5 hours on the road eat half of your "
                     "ski time. On this 2-day tour you sleep next to the slopes, ski a full day, and "
                     "the next morning drive over the Cross Pass to Mount Kazbek while the road is clear "
                     "and the sky is usually at its best.",
            "days": [
                ("Day 1 — Gudauri", "Tbilisi → Zhinvali Reservoir → Ananuri → Gudauri (120 km, about "
                 "2.5 h). Skiing, a lesson or a snow walk; dinner with a mountain view and a night in "
                 "a Gudauri hotel."),
                ("Day 2 — Kazbegi", "Cross Pass (2,379 m) → Friendship Monument → Stepantsminda → "
                 "Gergeti Trinity Church (2,170 m) with Mount Kazbek (5,047 m). Back in Tbilisi by "
                 "7–8 pm."),
            ],
            "details": [
                ("Day one: the Gudauri slopes",
                 "We leave Tbilisi at 8:00 and stop briefly at Ananuri fortress above the Zhinvali "
                 "Reservoir. By 11:00 you are in Gudauri (2,196 m): top lift stations are above "
                 "3,000 m, with runs for beginners and confident skiers. We help you get the ski pass, "
                 "rental and an instructor on the spot. Not skiing? Ride a gondola for the views, fly "
                 "a tandem paraglider (weather permitting) or relax on a terrace with mulled wine. "
                 "Night in a Gudauri hotel, breakfast included."),
                ("Day two: Cross Pass and Gergeti",
                 "After breakfast we cross the Cross Pass (2,379 m), stop at the Friendship Monument "
                 "above the Gudauri valley and continue to Stepantsminda (1,740 m). In winter Gergeti "
                 "church is reached by 4x4 when the road is open — 15 minutes over snow — for the best "
                 "view of Kazbek. Lunch in Stepantsminda (khinkali, chakapuli, local beer), back in "
                 "Tbilisi by 7–8 pm."),
                ("If the pass is closed",
                 "In winter the Gudauri — Kobi section sometimes closes because of heavy snow or "
                 "avalanche risk. We follow the road service updates and change the plan at no extra "
                 "cost: a second ski day in Gudauri, or Ananuri and Mtskheta on the way back. Kazbegi "
                 "can be moved to another day of your trip."),
            ],
            "tips": ["Warm waterproof layers, hat, gloves and sunglasses — snow glare is strong above "
                     "2,000 m", "Cash ₾150–250 for ski pass, rental and lunch",
                     "Ski suits can be rented in Gudauri", "Passport — needed for the ski pass and hotel"],
            "inc": ["Minivan with winter tyres for both days", "English/Russian-speaking driver-guide",
                    "1 night in a Gudauri hotel (double room, breakfast)",
                    "Stops at Ananuri and the Cross Pass"],
            "exc": ["Ski pass, rental, instructor", "Lunches and dinners",
                    "4x4 to Gergeti (paid on the spot)", "Paragliding and other activities"],
            "faq": [
                ("How is this different from the Gudauri day trip?",
                 "The Gudauri day trip costs from ₾225 and returns to Tbilisi the same evening, "
                 "leaving 4–5 hours on the slopes. The 2-day tour (₾520) includes a night in Gudauri, "
                 "a full ski day and Kazbegi with Gergeti on day two."),
                ("How much is the Gudauri & Kazbegi 2-day tour and what is included?",
                 "From ₾520 per person: transport for both days, a driver-guide and a night in a "
                 "Gudauri hotel with breakfast. Ski pass, rental, meals and the 4x4 to Gergeti are "
                 "paid on the spot."),
                ("Do I need to know how to ski?",
                 "No. Beginners get an instructor for 1–2 hours; non-skiers can take the gondola, "
                 "paraglide or simply enjoy the resort."),
                ("What if the Cross Pass is closed?",
                 "We change the plan at no extra cost: a second ski day in Gudauri, or Ananuri and "
                 "Mtskheta. Kazbegi can be moved to another day."),
                ("When is the ski season in Gudauri?",
                 "Usually late December to early April — in 2025/26 the lifts opened on December 27. "
                 "Exact dates depend on snow. For New Year holidays book "
                 "hotels 3–4 weeks ahead."),
            ],
        },
        "ge": {
            "title": "გუდაური და ყაზბეგი 2 დღეში — ზამთრის ტური ₾520-დან",
            "h1": "გუდაური + ყაზბეგი: ზამთრის ტური 2 დღით",
            "name": "გუდაური + ყაზბეგი — ზამთრის ორდღიანი ტური",
            "desc": "ზამთრის ორდღიანი ტური თბილისიდან ₾520-დან: თხილამური გუდაურში, ღამე მთაში, ჯვრის უღელტეხილი და თოვლიანი გერგეტი. სასტუმრო შედის.",
            "short": "გუდაური + ყაზბეგი — ზამთრის ორდღიანი ტური თბილისიდან, ღამისთევით გუდაურში, "
                     "₾520-დან ერთ ადამიანზე, 7 ადამიანამდე. 1-ლი დღე — გუდაურის ფერდობები, მე-2 დღე — "
                     "ჯვრის უღელტეხილი, სტეფანწმინდა და გერგეტი. სეზონი: ჩვეულებრივ დეკემბრის ბოლოდან "
                     "აპრილის დასაწყისამდე.",
            "intro": "ზამთარში გუდაურში ერთდღიანი მოგზაურობა მოკლეა: 4–5 საათი გზაში სრიალის დროის "
                     "ნახევარს ჭამს. ორდღიან ტურში ღამეს ფერდობებთან ათევთ, მთელ დღეს სრიალებთ, მეორე "
                     "დილით კი ჯვრის უღელტეხილით ყაზბეგისკენ მიდიხართ, როცა გზა სუფთაა და ცა ხშირად "
                     "მოწმენდილი.",
            "days": [
                ("დღე 1 — გუდაური", "თბილისი → ჟინვალის წყალსაცავი → ანანური → გუდაური (120 კმ, "
                 "დაახლოებით 2,5 საათი). სრიალი, ინსტრუქტორი ან გასეირნება; ვახშამი მთის ხედით და ღამე "
                 "გუდაურის სასტუმროში."),
                ("დღე 2 — ყაზბეგი", "ჯვრის უღელტეხილი (2379 მ) → მეგობრობის თაღი → სტეფანწმინდა → "
                 "გერგეტის სამების ტაძარი (2170 მ) და ყაზბეგის მწვერვალი (5047 მ). თბილისში "
                 "დაბრუნება 19:00–20:00-ზე."),
            ],
            "details": [
                ("პირველი დღე: გუდაურის ფერდობები",
                 "თბილისიდან გავდივართ 08:00-ზე, გზად მოკლე გაჩერება ანანურის ციხესთან ჟინვალის "
                 "წყალსაცავის თავზე. 11:00-ისთვის გუდაურში ხართ (2196 მ): საბაგიროების ზედა სადგურები "
                 "3000 მ-ზე მაღლაა, ტრასები არის დამწყებთათვისაც და გამოცდილი მოთხილამურეებისთვისაც. "
                 "სკიპასის, აღჭურვილობის და ინსტრუქტორის აღებაში ადგილზე დაგეხმარებით. არ სრიალებთ? "
                 "საბაგირო ხედებისთვის, ტანდემ-პარაპლანი (ამინდის მიხედვით) ან ტერასა ცხელი ღვინით. "
                 "ღამე გუდაურის სასტუმროში, საუზმე შედის ფასში."),
                ("მეორე დღე: ჯვრის უღელტეხილი და გერგეტი",
                 "საუზმის შემდეგ გადავდივართ ჯვრის უღელტეხილს (2379 მ), ვჩერდებით მეგობრობის თაღთან "
                 "და მივდივართ სტეფანწმინდაში (1740 მ). ზამთარში გერგეტის ტაძართან ჯიპით ადიან, როცა "
                 "გზა ღიაა — 15 წუთი თოვლში; იქიდან ყაზბეგის საუკეთესო ხედია. სადილი სტეფანწმინდაში "
                 "(ხინკალი, ჩაქაფული) და თბილისში დაბრუნება 19:00–20:00-ზე."),
                ("თუ უღელტეხილი დაიკეტება",
                 "ზამთარში გუდაური — კობის მონაკვეთი ზოგჯერ იკეტება თოვლისა და ზვავსაშიშროების გამო. "
                 "საგზაო სამსახურის ინფორმაციას ვადევნებთ თვალს და პროგრამას დამატებითი გადასახადის "
                 "გარეშე ვცვლით: მეორე დღე გუდაურში ან ანანური და მცხეთა უკანა გზაზე."),
            ],
            "tips": ["თბილი, წყალგაუმტარი ტანსაცმელი, ქუდი, ხელთათმანი და მზის სათვალე",
                     "ნაღდი ფული ₾150–250 სკიპასის, აღჭურვილობის და სადილისთვის",
                     "სათხილამურო კოსტიუმის ქირაობა გუდაურშიც შეიძლება",
                     "პასპორტი — სკიპასისა და სასტუმროსთვის"],
            "inc": ["მინივენი ზამთრის საბურავებით ორივე დღეს", "გიდი-მძღოლი",
                    "ერთი ღამე გუდაურის სასტუმროში (ორადგილიანი ნომერი, საუზმე)",
                    "გაჩერებები ანანურსა და ჯვრის უღელტეხილზე"],
            "exc": ["სკიპასი, აღჭურვილობა, ინსტრუქტორი", "სადილი და ვახშამი",
                    "ჯიპი გერგეტამდე (ადგილზე)", "პარაპლანი და სხვა აქტივობები"],
            "faq": [
                ("რით განსხვავდება ეს ტური გუდაურის ერთდღიანი ექსკურსიისგან?",
                 "ერთდღიანი ექსკურსია გუდაურში ₾225-დან ღირს და საღამოს თბილისში ბრუნდება — "
                 "ფერდობზე 4–5 საათი რჩება. ორდღიან ტურში (₾520) ღამეს გუდაურში ათევთ, მთელ დღეს "
                 "სრიალებთ და მეორე დღეს ყაზბეგსა და გერგეტს ნახულობთ."),
                ("რა ღირს გუდაური + ყაზბეგის ორდღიანი ტური და რა შედის ფასში?",
                 "₾520-დან ერთ ადამიანზე: ტრანსპორტი ორივე დღეს, გიდი-მძღოლი და ღამე გუდაურის "
                 "სასტუმროში საუზმით. სკიპასი, აღჭურვილობა, კვება და ჯიპი ადგილზე იხდება."),
                ("უნდა ვიცოდე თხილამურებით სრიალი?",
                 "არა. დამწყებთათვის ინსტრუქტორს ვიღებთ 1–2 საათით, ვინც არ სრიალებს — საბაგირო, "
                 "პარაპლანი ან გასეირნება კურორტზე."),
                ("რა მოხდება, თუ ჯვრის უღელტეხილი დაიკეტება?",
                 "პროგრამას დამატებითი გადასახადის გარეშე ვცვლით: მეორე დღე გუდაურში ან ანანური და "
                 "მცხეთა. ყაზბეგი სხვა დღეზე გადაიტანება."),
                ("როდის არის სეზონი გუდაურში?",
                 "ჩვეულებრივ დეკემბრის ბოლოდან აპრილის დასაწყისამდე — 2025/26 სეზონში საბაგიროები "
                 "27 დეკემბერს გაიხსნა. ზუსტი თარიღები თოვლზეა დამოკიდებული. საახალწლოდ "
                 "სასტუმრო 3–4 კვირით ადრე დაჯავშნეთ."),
            ],
        },
    },
    "tur-borjomi-bakuriani-2-dnya": {
        "price": 520, "img": "bakuriani-zima", "img_wh": (1600, 840), "video": "borjomi-drone.mp4", "night_place": {
            "ru": "Боржоми", "en": "Borjomi", "ge": "ბორჯომი"},
        "ru": {
            "title": "Боржоми и Бакуриани за 2 дня — зимний тур с ночёвкой от ₾520",
            "h1": "Боржоми + Бакуриани: зимний тур на 2 дня",
            "name": "Боржоми + Бакуриани за 2 дня зимой",
            "desc": "Зимний тур на 2 дня из Тбилиси от ₾520: тёплые серные бассейны Боржоми под снегом, ночь в Боржоми и курорт Бакуриани. Отель с завтраком.",
            "short": "Боржоми + Бакуриани — зимний тур на 2 дня из Тбилиси с ночёвкой в Боржоми, от "
                     "₾520 с человека, группа до 7 человек. День 1 — парк и тёплые бассейны Боржоми, "
                     "день 2 — курорт Бакуриани: санки, лыжи, снегоходы. Спокойный темп, подходит для семей.",
            "intro": "Это самый мягкий зимний маршрут по Грузии: без высоких перевалов и закрытых дорог, "
                     "с тёплыми минеральными бассейнами под открытым небом и серпантином через "
                     "заснеженный сосновый лес. Подходит для семей с детьми и тех, кто не катается на лыжах.",
            "days": [
                ("День 1 — Боржоми", "Тбилиси → Боржоми (160 км, около 2,5 часа). Центральный парк, "
                 "минеральный источник, канатка на плато, купание в тёплых серных бассейнах под снегом. "
                 "Ночь в отеле Боржоми."),
                ("День 2 — Бакуриани", "Серпантин через Цагвери, 30 км и около 40 минут → Бакуриани "
                 "(1700 м): санки, лыжи, снегоходы. Возвращение в Тбилиси к "
                 "19:00–20:00."),
            ],
            "details": [
                ("Первый день: парк и тёплые бассейны Боржоми",
                 "Выезд из Тбилиси в 09:00, к полудню вы в Боржоми (около 800 м). Центральный парк в "
                 "ущелье, источник минеральной воды «Боржоми» — пить можно бесплатно прямо из крана, "
                 "канатка на плато над городом. Главное зимнее удовольствие — тёплые серные бассейны "
                 "под открытым небом над парком: вода +32…+38 °C, вокруг снег. Вечером — ужин и "
                 "ночь в отеле Боржоми, завтрак включён."),
                ("Второй день: Бакуриани",
                 "После завтрака — 40 минут по серпантину через сосновый лес и Цагвери. Узкоколейка "
                 "«Кукушка» с сезона 2025/26 закрыта на реконструкцию, запуск обещают около января "
                 "2027 года: если поезд пойдёт, включим поездку в программу. "
                 "Бакуриани (1700 м) — семейный курорт: пологие трассы Дидвели и Кохта, санки, "
                 "снегоходы, прокат снаряжения. После обеда — дорога в Тбилиси, приезд к 19:00–20:00."),
                ("Почему этот маршрут надёжный зимой",
                 "В отличие от Военно-Грузинской дороги, трасса на Боржоми и Бакуриани не проходит "
                 "через высокие перевалы и закрывается крайне редко. Если метель всё-таки поменяет "
                 "планы, заменяем Бакуриани на Зелёный монастырь и дворец Романовых в Ликани."),
            ],
            "tips": ["Купальник и шлёпанцы для бассейнов, полотенце можно взять в отеле",
                     "Тёплая обувь и одежда — в Бакуриани заметно холоднее, чем в Тбилиси",
                     "Наличные ₾80–150 на бассейны, канатку и обед",
                     "Детям — санки можно взять в прокате в Бакуриани"],
            "inc": ["Минивэн на зимней резине на оба дня", "Гид-водитель на русском языке",
                    "Ночь в отеле Боржоми (2-местный номер, завтрак)", "Переезд Боржоми — Бакуриани и "
                    "обратно в Тбилиси"],
            "exc": ["Вход в бассейны и канатка", "Обеды и ужины",
                    "Ски-пасс, прокат, санки, снегоходы"],
            "faq": [
                ("Чем этот тур отличается от однодневных экскурсий в Боржоми или Бакуриани?",
                 "Однодневная экскурсия в Боржоми стоит от ₾178, в Бакуриани — отдельный выезд. За 1 день "
                 "не успеть и бассейны, и Бакуриани. В двухдневном туре за ₾520 — ночь в Боржоми, "
                 "бассейны вечером и Бакуриани на свежую голову утром."),
                ("Сколько стоит тур Боржоми + Бакуриани на 2 дня и что входит?",
                 "От ₾520 с человека: транспорт на оба дня, гид-водитель и ночь в отеле Боржоми с "
                 "завтраком. Бассейны, канатка, питание и катание оплачиваются на месте."),
                ("Работают ли серные бассейны Боржоми зимой?",
                 "Да, круглый год. Зимой это самое атмосферное место: тёплая вода под открытым небом "
                 "и снег вокруг."),
                ("Подходит ли тур для детей?",
                 "Да, это самый спокойный зимний маршрут: без высоких перевалов, с санками и пологими "
                 "трассами Бакуриани и тёплыми бассейнами Боржоми."),
                ("Когда лучше ехать?",
                 "Снег в Бакуриани обычно лежит с конца декабря до середины марта. Боржоми и бассейны "
                 "хороши весь год."),
            ],
        },
        "en": {
            "title": "Borjomi & Bakuriani 2-Day Winter Tour from Tbilisi — ₾520",
            "h1": "Borjomi & Bakuriani 2-Day Winter Tour",
            "name": "Borjomi & Bakuriani 2-Day Winter Tour",
            "desc": "2-day winter tour from Tbilisi from ₾520 per person: warm Borjomi sulfur pools in the snow, a night in Borjomi and Bakuriani ski resort.",
            "short": "Borjomi & Bakuriani is a 2-day winter tour from Tbilisi with a night in Borjomi, "
                     "from ₾520 per person, up to 7 people. Day 1 — Borjomi park and warm pools, day 2 — "
                     "Bakuriani resort: sledding, skiing, snowmobiles. Easy pace, family-friendly.",
            "intro": "This is the gentlest winter route in Georgia: no high passes and road closures, "
                     "open-air mineral pools in the snow and a winding road through a snowy pine forest. "
                     "Great for families with kids and for travellers who don't ski.",
            "days": [
                ("Day 1 — Borjomi", "Tbilisi → Borjomi (160 km, about 2.5 h). Central Park, the "
                 "mineral spring, cable car to the plateau and a swim in warm sulfur pools in the snow. "
                 "Night in a Borjomi hotel."),
                ("Day 2 — Bakuriani", "Mountain road via Tsagveri, 30 km, about 40 minutes → Bakuriani "
                 "(1,700 m): sledding, skiing, snowmobiles. Back in Tbilisi by 7–8 pm."),
            ],
            "details": [
                ("Day one: Borjomi park and warm pools",
                 "We leave Tbilisi at 9:00 and reach Borjomi (about 800 m) by noon. Central Park in the "
                 "gorge, the Borjomi mineral spring — free to drink straight from the tap — and the cable "
                 "car to the plateau above town. The winter highlight is the open-air sulfur pools above "
                 "the park: water 32–38 °C with snow all around. Dinner and a night in a Borjomi "
                 "hotel, breakfast included."),
                ("Day two: Bakuriani",
                 "After breakfast — 40 minutes up a winding road through pine forest and Tsagveri. The "
                 "Kukushka narrow-gauge train has been closed for restoration since the 2025/26 season, "
                 "with a restart announced for around January 2027: if it runs, we add the ride. Bakuriani "
                 "(1,700 m) is a family resort with gentle Didveli and Kokhta runs, sledding, snowmobiles "
                 "and gear rental. After lunch we drive back, arriving in Tbilisi by 7–8 pm."),
                ("Why this route is reliable in winter",
                 "Unlike the Georgian Military Highway, the road to Borjomi and Bakuriani has no high "
                 "passes and rarely closes. If a snowstorm still changes plans, we swap Bakuriani for the "
                 "Green Monastery and the Romanov palace in Likani."),
            ],
            "tips": ["Swimsuit and flip-flops for the pools; towels are usually available at the hotel",
                     "Warm boots and layers — Bakuriani is much colder than Tbilisi",
                     "Cash ₾80–150 for pools, cable car and lunch",
                     "Sleds for kids can be rented in Bakuriani"],
            "inc": ["Minivan with winter tyres for both days", "English/Russian-speaking driver-guide",
                    "1 night in a Borjomi hotel (double room, breakfast)",
                    "Borjomi — Bakuriani drive and return to Tbilisi"],
            "exc": ["Pools and cable car", "Lunches and dinners",
                    "Ski pass, rental, sleds, snowmobiles"],
            "faq": [
                ("How is this different from the Borjomi or Bakuriani day trips?",
                 "The Borjomi day trip starts at ₾178 and Bakuriani is a separate day out — in one day "
                 "you can't do both the pools and Bakuriani. The 2-day tour (₾520) adds a night "
                 "in Borjomi: pools in the evening, Bakuriani fresh in the morning."),
                ("How much is the Borjomi & Bakuriani 2-day tour and what is included?",
                 "From ₾520 per person: transport for both days, a driver-guide and a night in a Borjomi "
                 "hotel with breakfast. Pools, cable car, meals and ski activities are paid on "
                 "the spot."),
                ("Are the Borjomi sulfur pools open in winter?",
                 "Yes, all year round. Winter is the most atmospheric time: warm water outdoors with snow "
                 "around."),
                ("Is the tour good for kids?",
                 "Yes, it is the easiest winter route: no high passes, sledding and gentle slopes in "
                 "Bakuriani, warm pools in Borjomi."),
                ("When is the best time to go?",
                 "Snow in Bakuriani usually lasts from late December to mid-March. Borjomi and the pools "
                 "are good all year."),
            ],
        },
        "ge": {
            "title": "ბორჯომი და ბაკურიანი 2 დღეში — ზამთრის ტური ₾520-დან",
            "h1": "ბორჯომი + ბაკურიანი: ზამთრის ტური 2 დღით",
            "name": "ბორჯომი + ბაკურიანი — ზამთრის ორდღიანი ტური",
            "desc": "ზამთრის ორდღიანი ტური თბილისიდან ₾520-დან: ბორჯომის თბილი გოგირდის აუზები თოვლში, ღამე ბორჯომში და ბაკურიანი. სასტუმრო შედის.",
            "short": "ბორჯომი + ბაკურიანი — ზამთრის ორდღიანი ტური თბილისიდან, ღამისთევით ბორჯომში, "
                     "₾520-დან ერთ ადამიანზე, 7 ადამიანამდე. 1-ლი დღე — ბორჯომის პარკი და თბილი "
                     "აუზები, მე-2 დღე — ბაკურიანი: ციგა, თხილამური, თოვლმავალი. მშვიდი ტემპი, ოჯახებისთვის.",
            "intro": "ეს ყველაზე რბილი ზამთრის მარშრუტია საქართველოში: მაღალი უღელტეხილებისა და "
                     "დაკეტილი გზების გარეშე, ღია ცის ქვეშ თბილი მინერალური აუზებით და "
                     "მთის გზით თოვლიან ფიჭვნარში. შესაფერისია ოჯახებისთვის და მათთვის, ვინც არ სრიალებს.",
            "days": [
                ("დღე 1 — ბორჯომი", "თბილისი → ბორჯომი (160 კმ, დაახლოებით 2,5 საათი). ცენტრალური "
                 "პარკი, მინერალური წყარო, საბაგირო პლატოზე და ბანაობა თბილ გოგირდის აუზებში თოვლში. "
                 "ღამე ბორჯომის სასტუმროში."),
                ("დღე 2 — ბაკურიანი", "მთის გზა წაღვერის გავლით, 30 კმ, დაახლოებით 40 წუთი → "
                 "ბაკურიანი (1700 მ): ციგა, თხილამური, თოვლმავალი. თბილისში დაბრუნება "
                 "19:00–20:00-ზე."),
            ],
            "details": [
                ("პირველი დღე: ბორჯომის პარკი და თბილი აუზები",
                 "თბილისიდან გავდივართ 09:00-ზე, შუადღისთვის ბორჯომში ხართ (დაახლოებით 800 მ). "
                 "ცენტრალური პარკი ხეობაში, „ბორჯომის“ მინერალური წყარო — უფასოდ, პირდაპირ ონკანიდან, "
                 "და საბაგირო ქალაქის თავზე პლატოზე. ზამთრის მთავარი სიამოვნება — ღია ცის ქვეშ "
                 "გოგირდის აუზები პარკის ზემოთ: წყალი +32…+38 °C, გარშემო თოვლი. ვახშამი "
                 "და ღამე ბორჯომის სასტუმროში, საუზმე შედის ფასში."),
                ("მეორე დღე: ბაკურიანი",
                 "საუზმის შემდეგ — 40 წუთი მთის გზით ფიჭვნარსა და წაღვერში. ვიწროლიანდაგიანი "
                 "„კუკუშკა“ 2025/26 სეზონიდან რეკონსტრუქციაზეა, გახსნა დაახლოებით 2027 წლის "
                 "იანვრისთვისაა დაანონსებული: თუ იმუშავებს, პროგრამაში ჩავრთავთ. "
                 "ბაკურიანი (1700 მ) საოჯახო კურორტია: დიდველისა და კოხტის რბილი ტრასები, ციგა, "
                 "თოვლმავალი, აღჭურვილობის ქირაობა. სადილის შემდეგ — თბილისში, 19:00–20:00-ზე."),
                ("რატომ არის ეს მარშრუტი საიმედო ზამთარში",
                 "საქართველოს სამხედრო გზისგან განსხვავებით, ბორჯომისა და ბაკურიანის გზა მაღალ "
                 "უღელტეხილებზე არ გადის და იშვიათად იკეტება. თუ ქარბუქი მაინც შეცვლის გეგმას, "
                 "ბაკურიანს მწვანე მონასტრითა და ლიკანის რომანოვების სასახლით ვცვლით."),
            ],
            "tips": ["საცურაო კოსტიუმი და ჩუსტები აუზებისთვის", "თბილი ფეხსაცმელი და ტანსაცმელი — "
                     "ბაკურიანში თბილისზე ბევრად ცივა", "ნაღდი ფული ₾80–150 აუზების, საბაგიროს "
                     "და სადილისთვის", "ბავშვებისთვის ციგის ქირაობა ბაკურიანშია"],
            "inc": ["მინივენი ზამთრის საბურავებით ორივე დღეს", "გიდი-მძღოლი",
                    "ერთი ღამე ბორჯომის სასტუმროში (ორადგილიანი ნომერი, საუზმე)",
                    "გზა ბორჯომი — ბაკურიანი და დაბრუნება თბილისში"],
            "exc": ["აუზები და საბაგირო", "სადილი და ვახშამი",
                    "სკიპასი, აღჭურვილობა, ციგა, თოვლმავალი"],
            "faq": [
                ("რით განსხვავდება ეს ტური ბორჯომის ან ბაკურიანის ერთდღიანი ექსკურსიისგან?",
                 "ერთდღიანი ექსკურსია ბორჯომში ₾178-დან ღირს, ბაკურიანი ცალკე გასვლაა — ერთ დღეში "
                 "აუზებსაც და ბაკურიანსაც ვერ მოასწრებთ. ორდღიან ტურში (₾520) ღამე ბორჯომშია: "
                 "აუზები საღამოს, ბაკურიანი დილით."),
                ("რა ღირს ბორჯომი + ბაკურიანის ორდღიანი ტური და რა შედის ფასში?",
                 "₾520-დან ერთ ადამიანზე: ტრანსპორტი ორივე დღეს, გიდი-მძღოლი და ღამე ბორჯომის "
                 "სასტუმროში საუზმით. აუზები, საბაგირო, კვება და სრიალი ადგილზე იხდება."),
                ("მუშაობს ბორჯომის გოგირდის აუზები ზამთარში?",
                 "დიახ, მთელი წლის განმავლობაში. ზამთარში ყველაზე ატმოსფერულია: თბილი წყალი ღია ცის "
                 "ქვეშ და თოვლი გარშემო."),
                ("შესაფერისია ტური ბავშვებისთვის?",
                 "დიახ, ეს ყველაზე მშვიდი ზამთრის მარშრუტია: ციგა, ბაკურიანის რბილი ტრასები და "
                 "ბორჯომის თბილი აუზები."),
                ("როდის ჯობია წასვლა?",
                 "ბაკურიანში თოვლი ჩვეულებრივ დეკემბრის ბოლოდან მარტის შუა რიცხვებამდე დევს. ბორჯომი "
                 "და აუზები მთელი წელი კარგია."),
            ],
        },
    },
}

# Related links per package: (url, label) per language — day trips + winter content.
RELATED = {
    "tur-gudauri-kazbegi-2-dnya": {
        "ru": [("/ekskursiya/ekskursiya-gudauri-iz-tbilisi/", "Гудаури за 1 день"),
               ("/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/", "Казбеги за 1 день"),
               ("/ekskursiya/tur-kazbegi-kakheti-2-dnya/", "Казбеги + Кахетия за 2 дня"),
               ("/ekskursiya/tur-gruziya-noviy-god/", "Новогодний тур на 5–7 дней"),
               ("/tury-v-gruziyu-zimoy/", "Все туры в Грузию зимой"),
               ("/blog/kazbegi-zimoy/", "Казбеги зимой: дорога и погода")],
        "en": [("/en/ekskursiya/ekskursiya-gudauri-iz-tbilisi/", "Gudauri day trip"),
               ("/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/", "Kazbegi day trip"),
               ("/en/ekskursiya/tur-kazbegi-kakheti-2-dnya/", "Kazbegi + Kakheti 2 days"),
               ("/en/ekskursiya/tur-gruziya-noviy-god/", "New Year tour, 5–7 days"),
               ("/en/blog/kazbegi-in-winter/", "Kazbegi in winter guide"),
               ("/en/tury-v-gruziyu-zimoy/", "All winter tours in Georgia")],
        "ge": [("/ge/ekskursiya/ekskursiya-gudauri-iz-tbilisi/", "გუდაური 1 დღეში"),
               ("/ge/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/", "ყაზბეგი 1 დღეში"),
               ("/ge/ekskursiya/tur-kazbegi-kakheti-2-dnya/", "ყაზბეგი + კახეთი 2 დღეში"),
               ("/ge/ekskursiya/tur-gruziya-noviy-god/", "ახალი წლის ტური 5–7 დღე"),
               ("/ge/tury-v-gruziyu-zimoy/", "ზამთრის ტურები"),
               ("/ge/blog/kazbegi-in-winter/", "ყაზბეგი ზამთარში")],
    },
    "tur-borjomi-bakuriani-2-dnya": {
        "ru": [("/ekskursiya/ekskursiya-borjomi-iz-tbilisi/", "Боржоми за 1 день"),
               ("/ekskursiya/ekskursiya-bakuriani-iz-tbilisi/", "Бакуриани за 1 день"),
               ("/ekskursiya/tur-gudauri-kazbegi-2-dnya/", "Гудаури + Казбеги за 2 дня"),
               ("/tury-v-gruziyu-zimoy/", "Все туры в Грузию зимой"),
               ("/blog/gruziya-zimoy/", "Грузия зимой: куда ехать")],
        "en": [("/en/ekskursiya/ekskursiya-borjomi-iz-tbilisi/", "Borjomi day trip"),
               ("/en/ekskursiya/ekskursiya-bakuriani-iz-tbilisi/", "Bakuriani day trip"),
               ("/en/ekskursiya/tur-gudauri-kazbegi-2-dnya/", "Gudauri + Kazbegi 2 days"),
               ("/en/blog/borjomi-complete-guide/", "Borjomi complete guide"),
               ("/en/tury-v-gruziyu-zimoy/", "All winter tours in Georgia")],
        "ge": [("/ge/ekskursiya/ekskursiya-borjomi-iz-tbilisi/", "ბორჯომი 1 დღეში"),
               ("/ge/ekskursiya/ekskursiya-bakuriani-iz-tbilisi/", "ბაკურიანი 1 დღეში"),
               ("/ge/ekskursiya/tur-gudauri-kazbegi-2-dnya/", "გუდაური + ყაზბეგი 2 დღეში"),
               ("/ge/tury-v-gruziyu-zimoy/", "ზამთრის ტურები"),
               ("/ge/blog/borjomi-complete-guide/", "ბორჯომის გზამკვლევი")],
    },
}

# Inbound link blocks: page -> packages to promote (intent split: day trip vs 2 days).
INBOUND = {
    "ekskursiya/ekskursiya-gudauri-iz-tbilisi": ["tur-gudauri-kazbegi-2-dnya"],
    "ekskursiya/ekskursiya-kazbegi-iz-tbilisi": ["tur-gudauri-kazbegi-2-dnya"],
    "ekskursiya/tur-kazbegi-kakheti-2-dnya": ["tur-gudauri-kazbegi-2-dnya"],
    "ekskursiya/ekskursiya-borjomi-iz-tbilisi": ["tur-borjomi-bakuriani-2-dnya"],
    "ekskursiya/ekskursiya-bakuriani-iz-tbilisi": ["tur-borjomi-bakuriani-2-dnya"],
    "ekskursiya/tur-gruziya-noviy-god": ["tur-gudauri-kazbegi-2-dnya", "tur-borjomi-bakuriani-2-dnya"],
    "blog/gruziya-zimoy": ["tur-gudauri-kazbegi-2-dnya", "tur-borjomi-bakuriani-2-dnya"],
    "blog/kazbegi-zimoy": ["tur-gudauri-kazbegi-2-dnya"],
    "blog/noviy-god-v-gruzii": ["tur-gudauri-kazbegi-2-dnya", "tur-borjomi-bakuriani-2-dnya"],
    "blog/georgia-in-winter": ["tur-gudauri-kazbegi-2-dnya", "tur-borjomi-bakuriani-2-dnya"],
    "blog/kazbegi-in-winter": ["tur-gudauri-kazbegi-2-dnya"],
    "blog/new-year-in-georgia": ["tur-gudauri-kazbegi-2-dnya", "tur-borjomi-bakuriani-2-dnya"],
    "blog/borjomi-complete-guide": ["tur-borjomi-bakuriani-2-dnya"],
    "blog/borjomi-from-tbilisi": ["tur-borjomi-bakuriani-2-dnya"],
    "blog/tury-v-borzhomi-2026": ["tur-borjomi-bakuriani-2-dnya"],
}
ANCHORS = {
    "tur-gudauri-kazbegi-2-dnya": {
        "ru": ["Гудаури + Казбеги за 2 дня", "зимний тур в Гудаури с ночёвкой",
               "два дня: лыжи в Гудаури и Казбеги в снегу"],
        "en": ["Gudauri & Kazbegi 2-day winter tour", "Gudauri ski trip with an overnight stay",
               "two days: Gudauri slopes and snowy Kazbegi"],
        "ge": ["გუდაური + ყაზბეგი 2 დღეში", "ზამთრის ტური გუდაურში ღამისთევით",
               "ორი დღე: გუდაურის ფერდობები და თოვლიანი ყაზბეგი"]},
    "tur-borjomi-bakuriani-2-dnya": {
        "ru": ["Боржоми + Бакуриани за 2 дня", "Боржоми и Бакуриани с ночёвкой",
               "два дня: тёплые бассейны Боржоми и снег Бакуриани"],
        "en": ["Borjomi & Bakuriani 2-day winter tour", "Borjomi and Bakuriani with an overnight stay",
               "two days: Borjomi warm pools and Bakuriani snow"],
        "ge": ["ბორჯომი + ბაკურიანი 2 დღეში", "ბორჯომი და ბაკურიანი ღამისთევით",
               "ორი დღე: ბორჯომის თბილი აუზები და ბაკურიანის თოვლი"]},
}
PRICE_FMT = {"ru": "от ₾{p}", "en": "from ₾{p}", "ge": "₾{p}-დან"}
HUB_TAIL = {"en": ' · <a href="/en/tury-v-gruziyu-zimoy/" style="color:#1A3D2E">all winter tours</a>'}
INBOUND_LEAD = {"ru": "Зимой с ночёвкой:", "en": "Winter, with an overnight stay:",
                "ge": "ზამთარში, ღამისთევით:"}

e = html.escape


def url(lang, slug):
    return f"{SITE}{PREFIX[lang]}/ekskursiya/{slug}/"


def ld(obj):
    return ('<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False)
            + "</script>")


def build_main(lang, slug, pk, c):
    u, p = UI[lang], pk["price"]
    wa_text = f"{u['wa']} {c['name']}".replace(" ", "+")
    stats = "".join(
        f'<div class="stat-item"><span class="stat-val">{v}</span><span class="stat-lab" style="color:rgba(255,255,255,.9);text-shadow:0 1px 3px rgba(0,0,0,.6)">{lab}</span></div>'
        for v, lab in [(PRICE_FMT[lang].format(p=p), u["pp"]), (u["days"], u["dur"]),
                       (u["grp"], u["grp_l"]), (e(pk["night_place"][lang]), u["night"]),
                       ("14+", u["cancel"])])
    days = "".join(
        f'<div class="route-item"><div class="route-time">{e(t.split(" — ")[0])}</div><div>'
        f'<div class="route-name">{e(t.split(" — ")[1])}</div><div class="route-desc">{e(d)}</div>'
        f"</div></div>" for t, d in c["days"])
    details = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in c["details"])
    faq = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in c["faq"])
    rel = " · ".join(f'<a href="{h}">{e(t)}</a>' for h, t in RELATED[slug][lang])
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return f"""<section class="page-hero">
<img alt="{e(c['name'])}" fetchpriority="high" height="400" src="/images/{pk['img']}.webp?v=2" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0" width="600"/>
<div aria-hidden="true" style="position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.1) 0%,rgba(0,0,0,.35) 45%,rgba(0,0,0,.72) 100%)"></div>
<div class="hero-inner">
<h1 class="hero-h1">{e(c['h1'])}</h1>
<div class="hero-stats">{stats}</div>
<div class="hero-btns" style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
<a class="btn-wa" href="https://wa.me/{WA}?text={wa_text}+[site:{'ka' if lang == 'ge' else lang}:tour:{slug}]" style="padding:14px 28px;font-size:16px;border-radius:9999px;text-decoration:none">{e(u['book'].format(p=p))}</a>
<a href="/booking/?tour={slug}" style="padding:14px 28px;font-size:14px;border-radius:9999px;background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.5);color:#fff;text-decoration:none">{e(u['book_online'])}</a>
</div>
<div style="margin-top:12px;font-size:13px;color:rgba(255,255,255,.7)">{e(u['rating'])}</div>
</div></section>
<div class="article-wrap"><div class="article-body">
<div class="key-fact" style="background:#f0f7f4;border-left:4px solid #2E7D32;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0;font-size:16px;line-height:1.6"><strong>{e(u['short'])}</strong> {e(c['short'])}</div>
<p>{e(c['intro'])}</p>
<figure class="tour-video" style="position:relative;margin:26px 0;border-radius:16px;overflow:hidden;aspect-ratio:16/9;background:#0F241A">
<video muted loop playsinline autoplay preload="none" poster="/images/{pk['img']}.webp?v=2" aria-label="{e(c['name'])}" style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover"><source src="/images/{pk['video']}" type="video/mp4"></video>
</figure>
</div></div>
<section class="section" style="background:#fff"><div class="sec-inner">
<div class="sec-label">{e(u['route_lbl'])}</div>
<h2 class="sec-title">{e(u['route_h'])}</h2>
<div class="route-grid">{days}</div>
</div></section>
<div class="article-wrap"><div class="article-body">
{details}
<ul>{li(c['tips'])}</ul>
<div class="incl-grid">
<div class="includes-box"><h3>{e(u['inc'])}</h3><ul>{li(c['inc'])}</ul></div>
<div class="includes-box" style="background:#FEF2F2;border-left-color:#EF4444"><h3 style="color:#991B1B">{e(u['exc'])}</h3><ul style="color:#991B1B">{li(c['exc'])}</ul></div>
</div>
<h2>{e(u['faq'])}</h2>
{faq}
<div class="tour-readalso" style="margin:28px 0;padding:16px 20px;background:#f0f7f4;border-left:4px solid #2E7D32;border-radius:0 8px 8px 0;font-size:15px"><strong>{e(u['see'])}:</strong> {rel}</div>
</div>
<div class="article-cta">
<h3>{e(u['cta'])}</h3>
<p>{e(u['cta_sub'])}</p>
<div class="cta-btns"><a class="btn-wa" href="/booking/?tour={slug}">{e(u['book_online'])}</a><a class="btn-tg" href="https://t.me/SakhvaGuideBot?start=site">Telegram</a></div>
</div>
</div>
"""


def build_head(head, lang, slug, pk, c):
    u = UI[lang]
    img = f"{SITE}/images/{pk['img']}.jpg"
    head = re.sub(r"<title>.*?</title>", f"<title>{e(c['title'])}</title>", head, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(rf'<meta content="[^"]*" {attr}/>', f'<meta content="{e(c["desc"])}" {attr}/>', head)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(rf'<meta content="[^"]*" {attr}/>', f'<meta content="{e(c["title"])}" {attr}/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{img}" property="og:image"/>', head)
    head = re.sub(r'<meta content="[^"]*" property="og:image:alt"/>',
                  f'<meta content="{e(c["name"])}" property="og:image:alt"/>', head)
    w, h = pk["img_wh"]
    head = re.sub(r'<meta content="\d+" property="og:image:width"/>', f'<meta content="{w}" property="og:image:width"/>', head)
    head = re.sub(r'<meta content="\d+" property="og:image:height"/>', f'<meta content="{h}" property="og:image:height"/>', head)
    head = re.sub(r'<meta content="[^"]*" name="twitter:image"/>',
                  f'<meta content="{SITE}/images/{pk["img"]}.webp" name="twitter:image"/>', head)
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', head, flags=re.S)
    keep = [b for b in blocks if '"WebPage"' not in b and '"Product"' not in b and '"BreadcrumbList"' not in b
            and '"FAQPage"' not in b and '"VideoObject"' not in b]
    page = url(lang, slug)
    new = [
        ld({"@context": "https://schema.org", "@type": "WebPage", "@id": page + "#webpage", "url": page,
            "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ka" if lang == "ge" else lang,
            "isPartOf": {"@id": f"{SITE}/#website"}}),
        ld({"@context": "https://schema.org", "@type": "Product", "@id": page + "#product", "name": c["name"],
            "description": c["desc"], "url": page, "image": img,
            "brand": {"@type": "Brand", "name": "Sakhva Travel"},
            "offers": {"@type": "Offer", "seller": {"@type": "Organization", "name": "Sakhva Travel",
                                                     "url": f"{SITE}/"},
                       "price": str(pk["price"]), "priceCurrency": "GEL",
                       "availability": "https://schema.org/InStock", "priceValidUntil": "2027-04-30",
                       "url": page, "termsOfService": f"{SITE}/terms/"}}),
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": f"{SITE}{PREFIX[lang]}/"},
            {"@type": "ListItem", "position": 2, "name": u["tours"], "item": SITE + u["tours_url"]},
            {"@type": "ListItem", "position": 3, "name": c["name"], "item": page}]}),
        ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in c["faq"]]}),
    ]
    for b in blocks:
        head = head.replace(b, "", 1)
    return head.replace("</head>", "\n".join(new + keep) + "\n</head>")


def build_page(lang, slug, pk):
    c = pk[lang]
    src = ROOT / PREFIX[lang].lstrip("/") / "ekskursiya" / TPL_SLUG / "index.html"
    s = src.read_text()
    hi = s.index("</head>") + len("</head>")
    head, body = s[:hi], s[hi:]
    a, b = body.index('<section class="page-hero">'), body.index("<!-- trv:start -->")
    body = body[:a] + build_main(lang, slug, pk, c) + body[b:]
    # stray template visuals in head (hero preload etc.)
    head = head.replace("tbilisi-kazbegi-kakheti-tour-600", pk["img"])
    out = build_head(head, lang, slug, pk, c) + body
    out = out.replace(TPL_SLUG, slug)
    out = out.replace(f'/images/{pk["img"]}.webp"', f'/images/{pk["img"]}.webp?v=2"')
    dst = ROOT / PREFIX[lang].lstrip("/") / "ekskursiya" / slug / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out)
    return dst


def inbound_links():
    changed = []
    for rel, slugs in INBOUND.items():
        for lang in ("ru", "en", "ge"):
            f = ROOT / PREFIX[lang].lstrip("/") / rel / "index.html"
            if not f.exists():
                continue
            s = f.read_text()
            s = re.sub(r'<p data-sk="winter-2d"[^>]*>.*?</p>\n', "", s)
            k = zlib.crc32(rel.encode()) % 3
            links = " · ".join(
                f'<a href="{PREFIX[lang]}/ekskursiya/{sl}/" style="color:#1A3D2E;font-weight:600">'
                f'{e(ANCHORS[sl][lang][k])}</a> ({PRICE_FMT[lang].format(p=PACKAGES[sl]["price"])})'
                for sl in slugs)
            block = (f'<p {MARK} style="margin:20px auto;max-width:720px;padding:14px 18px;'
                     f'background:#EFF6FF;border-radius:8px;font-size:15px;color:#374151">'
                     f'{e(INBOUND_LEAD[lang])} {links}{HUB_TAIL.get(lang, "")}</p>\n')
            anchor = "<!-- trv:start -->" if "<!-- trv:start -->" in s else "</main>"
            if anchor not in s:
                continue
            f.write_text(s.replace(anchor, block + anchor, 1))
            changed.append(str(f.relative_to(ROOT)))
    return changed


def selftest(paths):
    for p in paths:
        s = p.read_text()
        assert s.count("<h1") == 1, p
        assert TPL_SLUG not in s, p
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S):
            json.loads(b)
        canon = re.search(r'<link href="([^"]+)" rel="canonical"/>', s).group(1)
        assert canon.endswith(p.parent.name + "/"), (p, canon)


if __name__ == "__main__":
    built = [build_page(lang, slug, pk) for slug, pk in PACKAGES.items() for lang in ("ru", "en", "ge")]
    selftest(built)
    print("pages:", *[str(p.relative_to(ROOT)) for p in built], sep="\n  ")
    print("inbound links:", *inbound_links(), sep="\n  ")
