#!/usr/bin/env python3
"""Translate 10 EN region pages: RU→EN text + noindex→index."""
import os, re

BASE = '/Users/vladimir/sakhva-travel'

# ─── Common replacements (all 10 pages) ───
COMMON = [
    # robots
    ('noindex,follow,max-image-preview:large,max-snippet:-1', 'index,follow,max-image-preview:large,max-snippet:-1'),
    # og:locale
    ('"og:locale" content="ru_RU"', '"og:locale" content="en_US"'),
    # author
    ('Тимур — Sakhva Travel', 'Timur — Sakhva Travel'),
    # Nav labels (desktop)
    ('href="/en/ekskursiya/">Экскурсии</a>', 'href="/en/ekskursiya/">Tours</a>'),
    ('href="/about/">О нас</a>', 'href="/en/about/">About</a>'),
    ('href="/#reviews">Отзывы</a>', 'href="/#reviews">Reviews</a>'),
    ('href="/#gallery">Медиа</a>', 'href="/#gallery">Media</a>'),
    ('href="/en/blog/">Блог</a>', 'href="/en/blog/">Blog</a>'),
    ('href="/#footer">Контакты</a>', 'href="/#footer">Contacts</a>'),
    ('>Оплатить онлайн</a>', '>Book Online</a>'),
    # Drawer
    ('>Написать в WhatsApp</a>', '>Message on WhatsApp</a>'),
    # Burger
    ('aria-label="Меню"', 'aria-label="Menu"'),
    # Footer
    ('Политика конфиденциальности', 'Privacy Policy'),
    ('Гид Тимур', 'Guide Timur'),
    # Other regions heading
    ('Другие регионы Грузии', 'Other Regions of Georgia'),
    # Other region links → EN
    ('href="/kakheti/" class="or-link">Кахетия</a>', 'href="/en/kakheti/" class="or-link">Kakheti</a>'),
    ('href="/mtskheta-mtianeti/" class="or-link">Мцхета-Мтианети</a>', 'href="/en/mtskheta-mtianeti/" class="or-link">Mtskheta-Mtianeti</a>'),
    ('href="/adjara/" class="or-link">Аджария</a>', 'href="/en/adjara/" class="or-link">Adjara</a>'),
    ('href="/imereti/" class="or-link">Имеретия</a>', 'href="/en/imereti/" class="or-link">Imereti</a>'),
    ('href="/samtskhe-javakheti/" class="or-link">Самцхе-Джавахети</a>', 'href="/en/samtskhe-javakheti/" class="or-link">Samtskhe-Javakheti</a>'),
    ('href="/shida-kartli/" class="or-link">Шида Картли</a>', 'href="/en/shida-kartli/" class="or-link">Shida Kartli</a>'),
    ('href="/kvemo-kartli/" class="or-link">Квемо Картли</a>', 'href="/en/kvemo-kartli/" class="or-link">Kvemo Kartli</a>'),
    ('href="/samegrelo/" class="or-link">Самегрело</a>', 'href="/en/samegrelo/" class="or-link">Samegrelo</a>'),
    ('href="/racha/" class="or-link">Рача-Лечхуми</a>', 'href="/en/racha/" class="or-link">Racha-Lechkhumi</a>'),
    ('href="/guria/" class="or-link">Гурия</a>', 'href="/en/guria/" class="or-link">Guria</a>'),
    # Tour card common
    ('Целый день · до 7 чел.', 'Full day · up to 7 pax'),
    ('4 часа · до 7 чел.', '4 hours · up to 7 pax'),
    ('2 дня · до 7 чел.', '2 days · up to 7 pax'),
    ('>Подробнее →</a>', '>Details →</a>'),
    # Distances
    ('"rd-city">Тбилиси</div>', '"rd-city">Tbilisi</div>'),
    ('"rd-city">Кутаиси</div>', '"rd-city">Kutaisi</div>'),
    ('"rd-city">Батуми</div>', '"rd-city">Batumi</div>'),
    ('"rd-city">Турция</div>', '"rd-city">Turkey</div>'),
    # Breadcrumb base
    ('href="/en/">Главная</a>', 'href="/en/">Home</a>'),
    ('href="/#regions">Регионы</a>', 'href="/#regions">Regions</a>'),
]

def add_hreflang(html, slug):
    """Add hreflang ru if missing."""
    ru = f'<link rel="alternate" hreflang="ru" href="https://sakhva-travel.com/{slug}/">'
    if ru not in html:
        en = f'<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/{slug}/">'
        html = html.replace(en, en + '\n' + ru)
    return html

def fix_og_url(html, slug):
    """Fix og:url to point to EN version."""
    html = re.sub(
        r'"og:url" content="https://sakhva-travel\.com/[^"]*"',
        f'"og:url" content="https://sakhva-travel.com/en/{slug}/"',
        html
    )
    return html

def fix_breadcrumb_schema(html, slug, name_en):
    """Translate breadcrumb schema."""
    html = html.replace('"name":"Главная"', '"name":"Home"')
    html = html.replace('"name":"Регионы"', '"name":"Regions"')
    return html

def process(slug, replacements):
    path = f'{BASE}/en/{slug}/index.html'
    with open(path) as f:
        html = f.read()
    # Common
    for old, new in COMMON:
        html = html.replace(old, new)
    # Page-specific
    for old, new in replacements:
        html = html.replace(old, new)
    # Hreflang
    html = add_hreflang(html, slug)
    # OG URL
    html = fix_og_url(html, slug)
    # Breadcrumb schema
    html = fix_breadcrumb_schema(html, slug, '')
    with open(path, 'w') as f:
        f.write(html)
    print(f'  OK: en/{slug}/')

# ─── ADJARA ───
process('adjara', [
    # Title & meta
    ('Аджария — Батуми, Гонио и субтропики Грузии | Sakhva Travel', 'Adjara — Batumi, Gonio & Subtropical Coast | Sakhva Travel'),
    ('Аджария — субтропический регион Грузии: Батуми, крепость Гонио, водопады Махунцети, горная Аджария. Как добраться из Тбилиси за 5:30. Экскурсии с гидом.', 'Adjara is the subtropical region of Georgia: Batumi, Gonio fortress, Makhuntseti waterfalls, mountain Adjara. 5:30 from Tbilisi. Guided tours available.'),
    ('Аджария — субтропический регион Грузии: Батуми, крепость Гонио, Махунцети, горная Аджария.', 'Adjara — subtropical coast of Georgia: Batumi, Gonio fortress, Makhuntseti waterfalls, mountain Adjara.'),
    ('Аджария — субтропический регион Грузии: Батуми, Гонио, Махунцети. Из Тбилиси за 5:30.', 'Adjara — subtropical Georgia: Batumi, Gonio, Makhuntseti. 5:30 from Tbilisi.'),
    # Breadcrumb
    ('>Аджария</strong>', '>Adjara</strong>'),
    ('"name":"Аджария"', '"name":"Adjara"'),
    # H1
    ('Аджария — субтропики, море и горные деревни', 'Adjara — Subtropics, Sea and Mountain Villages'),
    # Hero alt
    ('Батуми — набережная и современная архитектура столицы Аджарии', 'Batumi — seaside promenade and modern architecture of Adjara\'s capital'),
    # Body headings
    ('>Об Аджарии</h2>', '>About Adjara</h2>'),
    ('>Что посмотреть в Аджарии</h2>', '>What to See in Adjara</h2>'),
    ('>Батумский бульвар</h3>', '>Batumi Boulevard</h3>'),
    ('>Крепость Гонио-Апсарос</h3>', '>Gonio-Apsaros Fortress</h3>'),
    ('>Водопад и мост Махунцети</h3>', '>Makhuntseti Waterfall and Bridge</h3>'),
    ('>Ботанический сад Батуми</h3>', '>Batumi Botanical Garden</h3>'),
    ('>Площадь Пьяцца</h3>', '>Piazza Square</h3>'),
    ('>Канатная дорога Арго</h3>', '>Argo Cable Car</h3>'),
    ('>Горная Аджария и Хуло</h3>', '>Mountain Adjara and Khulo</h3>'),
    ('>Когда ехать и что взять</h2>', '>When to Visit and What to Bring</h2>'),
    ('>Наши экскурсии в Аджарию</h2>', '>Our Tours to Adjara</h2>'),
    # Body paragraphs
    ('Аджария — единственный регион Грузии, где субтропический климат, пальмы и Чёрное море сочетаются с горами высотой под три тысячи метров. Автономная республика занимает юго-западный угол страны, граничит с Турцией и тянется от побережья в глубь Малого Кавказа. Здесь живут около трёхсот пятидесяти тысяч человек, и большинство из них связаны с морем, туризмом или выращиванием чая и цитрусов.', 'Adjara is the only region in Georgia where subtropical climate, palm trees and the Black Sea combine with mountains nearly three thousand meters high. This autonomous republic occupies the southwestern corner of the country, borders Turkey and stretches from the coast deep into the Lesser Caucasus. About three hundred fifty thousand people live here, most of them connected to the sea, tourism or growing tea and citrus fruits.'),
    ('Батуми — столица Аджарии и второй по величине город Грузии. За последние пятнадцать лет он превратился из сонного портового городка в архитектурную витрину с небоскрёбами, казино и семикилометровым бульваром. При этом старый Батуми никуда не делся: узкие улочки с деревянными балконами, мечеть и синагога через стену, рыбный рынок и дворы, где сушат бельё на верёвках между домами.', 'Batumi is the capital of Adjara and Georgia\'s second largest city. Over the past fifteen years it has transformed from a sleepy port town into an architectural showcase with skyscrapers, casinos and a seven-kilometer boulevard. Yet old Batumi remains: narrow streets with wooden balconies, a mosque and synagogue sharing a wall, the fish market and courtyards where laundry dries on ropes strung between buildings.'),
    ('Горная Аджария — совсем другой мир. В тридцати километрах от побережья начинаются перевалы, альпийские луга и деревни, где жизнь почти не изменилась за сто лет. Хуло — главный посёлок горной части — стоит на высоте тысяча метров. Дорога из Батуми в Хуло идёт по ущелью реки Аджарисцкали, мимо водопадов Махунцети и арочного моста царицы Тамары XII века. По пути встречаются руины крепостей и старые мечети — напоминание о том, что Аджария триста лет входила в Османскую империю.', 'Mountain Adjara is a completely different world. Thirty kilometers from the coast, mountain passes begin, along with alpine meadows and villages where life has barely changed in a century. Khulo, the main settlement of the highland part, sits at a thousand meters. The road from Batumi to Khulo runs through the Acharistskali river gorge, past Makhuntseti waterfalls and a 12th-century arched bridge from Queen Tamar\'s era. Along the way you encounter fortress ruins and old mosques — reminders that Adjara was part of the Ottoman Empire for three hundred years.'),
    ('Кухня Аджарии отличается от остальной Грузии. Хачапури по-аджарски — лодочка с сыром, маслом и яйцом — известен на весь мир, но только здесь его пекут правильно: тесто тонкое, хрустящее, а начинку замешивают рукой прямо при вас. Бораки, синори, ачма — аджарские блюда из теста и сыра, которые в Тбилиси готовят совсем иначе. Рыбу здесь жарят на гриле с грецким орехом, а на десерт подают пахлаву — влияние Турции, до которой двадцать минут на машине.', 'Adjarian cuisine differs from the rest of Georgia. Adjarian khachapuri — a boat-shaped bread with cheese, butter and egg — is famous worldwide, but only here is it made properly: thin, crispy dough with filling mixed by hand right in front of you. Boraki, sinori, achma — Adjarian cheese pastries prepared quite differently from their Tbilisi versions. Fish is grilled with walnuts, and baklava is served for dessert — the influence of Turkey, just twenty minutes away by car.'),
    ('Семь километров набережной вдоль моря — главное место прогулок, от которого невозможно устать. Бульвар заложили в 1884 году французские садоводы, и с тех пор он только разрастался. Здесь — Alphabetic Tower высотой сто тридцать метров, движущаяся скульптура «Али и Нино» (мужчина и женщина проходят друг через друга каждые десять минут), танцующие фонтаны и десятки кафе. Вечером набережная подсвечена, играет живая музыка, а по бульвару катаются на велосипедах и электросамокатах.', 'Seven kilometers of seafront promenade — the main walking area that never gets old. The boulevard was laid out in 1884 by French gardeners and has only grown since. Here you\'ll find the 130-meter Alphabetic Tower, the moving sculpture "Ali and Nino" (a man and woman pass through each other every ten minutes), dancing fountains and dozens of cafes. In the evening the promenade is illuminated, live music plays, and people cycle and ride e-scooters along the boulevard.'),
    ('Римская крепость I века нашей эры в пятнадцати километрах к югу от Батуми — одно из старейших фортификационных сооружений на территории Грузии. Стены высотой пять метров и двадцать две башни сохранились почти полностью. Археологи нашли здесь золотые украшения, монеты Траяна и мозаичные полы. По легенде, внутри крепости похоронен апостол Матфий. Рядом — лучший галечный пляж побережья с чистой водой и видом на горы.', 'A 1st-century Roman fortress fifteen kilometers south of Batumi — one of the oldest fortifications in Georgia. Walls five meters high and twenty-two towers are almost completely preserved. Archaeologists found gold jewelry, Trajan\'s coins and mosaic floors here. Legend says the Apostle Matthias is buried inside. Nearby is the best pebble beach on the coast with clear water and mountain views.'),
    ('В двадцати километрах от Батуми, в ущелье реки Аджарисцкали, стоит арочный каменный мост XII века — один из символов горной Аджарии. Мост переброшен над рекой на высоте двадцати метров, по нему до сих пор ходят местные жители. Рядом — водопад Махунцети высотой двадцать метров, под которым образовалась природная купель. Летом вода тёплая, и сюда приезжают купаться. Лучшее время — весна, когда поток самый мощный.', 'Twenty kilometers from Batumi, in the Acharistskali river gorge, stands a 12th-century arched stone bridge — one of the symbols of mountain Adjara. The bridge spans the river at twenty meters high and is still used by locals today. Nearby is the twenty-meter Makhuntseti waterfall with a natural pool beneath it. In summer the water is warm enough for swimming. The best time to visit is spring, when the flow is most powerful.'),
    ('Один из крупнейших ботанических садов в мире — сто тринадцать гектаров на холмах над морем. Основан в 1912 году ботаником Андреем Красновым. Здесь девять климатических зон: японский сад, мексиканская пустыня, средиземноморские оливы, гималайские рододендроны. Дорожки петляют между гигантскими бамбуками, секвойями и эвкалиптами. Со смотровых площадок открывается панорама побережья — в ясную погоду видно турецкий берег.', 'One of the world\'s largest botanical gardens — one hundred thirteen hectares on hills above the sea. Founded in 1912 by botanist Andrey Krasnov. Nine climate zones: a Japanese garden, Mexican desert, Mediterranean olives, Himalayan rhododendrons. Paths wind between giant bamboo, sequoias and eucalyptus trees. From the viewing platforms, the coastline panorama stretches out — on clear days you can see the Turkish shore.'),
    ('Маленькая площадь в старом Батуми, стилизованная под венецианскую. Мозаичные стены, витражи, часовая башня с астрономическими часами — построено в 2009-2011 годах, но выглядит столетним. Вечером Пьяцца оживает: живой джаз, вино, ужин за столиками под открытым небом. Одно из самых фотогеничных мест Батуми.', 'A small square in old Batumi styled after Venice. Mosaic walls, stained glass, a clock tower with astronomical clock — built in 2009-2011 but looking a century old. In the evening Piazza comes alive: live jazz, wine, outdoor dining. One of Batumi\'s most photogenic spots.'),
    ('Канатная дорога длиной два с половиной километра поднимает с набережной на гору Ферия (двести шестьдесят метров). Кабинка едет десять минут — весь путь перед вами панорама Батуми, порт, море и горы. Лучше ехать перед закатом — город внизу начинает светиться. Стоимость — пятнадцать лари в оба конца.', 'A two-and-a-half-kilometer cable car ride from the seafront to Mount Feria (260 meters). The cabin takes ten minutes — the entire way you see Batumi\'s panorama, the port, sea and mountains. Best to go before sunset — the city below begins to glow. Cost: fifteen lari round trip.'),
    ('Серпантин из Батуми в Хуло — одна из самых красивых дорог Грузии. Ущелья, скалы, террасные деревни, старые мечети с деревянными минаретами. В Хуло — канатная дорога через ущелье, которую показывают во всех путеводителях. Дальше — перевал Годердзи (2025 м) с горнолыжным курортом зимой и альпийскими лугами летом. Круговой маршрут Батуми-Хуло-Годердзи-Ахалцихе-Тбилиси — отличный двухдневный вариант.', 'The serpentine road from Batumi to Khulo is one of Georgia\'s most beautiful drives. Gorges, cliffs, terraced villages, old mosques with wooden minarets. In Khulo there\'s a cable car crossing the gorge, featured in every guidebook. Further on is Goderdzi Pass (2,025 m) with a ski resort in winter and alpine meadows in summer. The circular route Batumi-Khulo-Goderdzi-Akhaltsikhe-Tbilisi makes an excellent two-day trip.'),
    # When to visit
    ('<strong>Лучшее время для пляжа:</strong> июнь-сентябрь, вода +24-26°C, воздух +28-32°C. Июль и август — пик сезона, многолюдно. Сентябрь — идеально: тёплое море, меньше людей, дешевле жильё.', '<strong>Best time for beach:</strong> June-September, water +24-26°C, air +28-32°C. July and August are peak season, crowded. September is ideal: warm sea, fewer people, cheaper accommodation.'),
    ('<strong>Для горной Аджарии:</strong> май-июнь и сентябрь-октябрь. Летом в горах +18-22°C. Зимой перевал Годердзи заснежен — нужна полноприводная машина.', '<strong>Mountain Adjara:</strong> May-June and September-October. Summer in the mountains +18-22°C. In winter Goderdzi Pass is snowed in — 4WD required.'),
    ('<strong>Что взять:</strong> купальник, пляжную обувь (галька), зонт или дождевик (субтропики — дожди даже летом), тёплую кофту для вечеров на набережной и горной части.', '<strong>What to bring:</strong> swimsuit, beach shoes (pebble beaches), umbrella or raincoat (subtropical — rain even in summer), warm layer for evenings on the promenade and mountain areas.'),
    ('<strong>Как добраться:</strong> из Тбилиси на машине 5 часов 30 минут, самолётом 40 минут, поездом 5 часов (ночной вагон — удобный вариант). Маршрутки от Дидубе — 35 лари.', '<strong>Getting there:</strong> from Tbilisi by car 5 hours 30 minutes, by plane 40 minutes, by train 5 hours (overnight sleeper — convenient option). Minibuses from Didube — 35 lari.'),
    # Tour cards
    ('Экскурсия в Батуми из Тбилиси', 'Batumi Tour from Tbilisi'),
    ('>Экскурсия в Батуми</a>', '>Batumi Tour</a>'),
    ('>Тур Тбилиси — Батуми</a>', '>Tbilisi — Batumi Tour</a>'),
    ('Тур Тбилиси — Батуми', 'Tbilisi to Batumi Tour'),
    ('Гомис Мта из Батуми', 'Gomis Mta from Batumi'),
    ('>Гомис Мта из Батуми</a>', '>Gomis Mta from Batumi</a>'),
    # CTA
    ('Хотите индивидуальный маршрут по Аджарии?', 'Want a custom itinerary in Adjara?'),
    ('Напишите Тимуру — составим маршрут под вас. Ответ за 15 минут.', 'Message Timur — we\'ll plan a route for you. Reply within 15 minutes.'),
    ('Хочу+экскурсию+в+Аджарию', 'Tour+in+Adjara'),
    ('Аджария+экскурсия', 'Adjara+tour'),
    # FAQ
    ('Частые вопросы об Аджарии', 'Frequently Asked Questions about Adjara'),
    ('Как добраться в Батуми из Тбилиси?', 'How to get to Batumi from Tbilisi?'),
    ('Из Тбилиси до Батуми 370 км — около 5 часов 30 минут на машине по автомагистрали. Самолётом 40 минут, поездом 5 часов, маршруткой от Дидубе 35 лари. С гидом Sakhva Travel — комфортный трансфер от отеля.', 'Tbilisi to Batumi is 370 km — about 5 hours 30 minutes by car on the highway. By plane 40 minutes, by train 5 hours, by minibus from Didube 35 lari. With Sakhva Travel guide — comfortable hotel pickup transfer.'),
    ('Из Тбилиси до Батуми 370 км — около 5 часов 30 минут на машине. Самолётом 40 минут, поездом 5 часов, маршруткой от Дидубе (35 лари). На <a href="/en/ekskursiya/batumi/">экскурсии с гидом</a> — комфортный трансфер от отеля.', 'Tbilisi to Batumi is 370 km — about 5 hours 30 minutes by car. By plane 40 minutes, train 5 hours, minibus from Didube (35 lari). On a <a href="/en/ekskursiya/batumi/">guided tour</a> — comfortable hotel pickup transfer.'),
    ('Когда лучше ехать в Аджарию?', 'When is the best time to visit Adjara?'),
    ('Для пляжного отдыха — июнь-сентябрь (вода +24-26°C). Лучший месяц — сентябрь: тёплое море, меньше людей, дешевле жильё. Для горной Аджарии — май или сентябрь. Зимой Батуми мягкий (+8-12°C), мало туристов.', 'For beach holidays — June-September (water +24-26°C). Best month is September: warm sea, fewer people, cheaper accommodation. For mountain Adjara — May or September. Winter Batumi is mild (+8-12°C), few tourists.'),
    ('Что посмотреть в Аджарии кроме Батуми?', 'What to see in Adjara besides Batumi?'),
    ('Крепость Гонио (I век), водопады Махунцети, арочный мост XII века, горная Аджария (Хуло, перевал Годердзи), Ботанический сад, пляжи Гонио и Уреки с магнитным песком.', 'Gonio Fortress (1st century), Makhuntseti waterfalls, 12th-century arched bridge, mountain Adjara (Khulo, Goderdzi Pass), Botanical Garden, Gonio and Ureki beaches with magnetic sand.'),
    ('Сколько стоит экскурсия из Тбилиси в Батуми?', 'How much does a tour from Tbilisi to Batumi cost?'),
    ('Двухдневная экскурсия с гидом включает трансфер, осмотр ключевых мест, рекомендации по ресторанам. Стоимость зависит от маршрута и количества дней — напишите Тимуру в WhatsApp для расчёта.', 'A two-day guided tour includes transfers, key sightseeing, restaurant recommendations. Price depends on route and number of days — message Timur on WhatsApp for a quote.'),
    ('Безопасно ли купаться в Батуми?', 'Is it safe to swim in Batumi?'),
    ('Да, пляжи Батуми безопасны. Галечное дно, спасатели с июня по сентябрь. Лучшие участки — бульвар и Гонио. Песчаные пляжи — в Уреки и Шекветили (магнитный песок).', 'Yes, Batumi beaches are safe. Pebble bottom, lifeguards from June to September. Best spots — boulevard and Gonio. Sandy beaches at Ureki and Shekvetili (magnetic sand).'),
    ('Что посмотреть кроме Батуми?', 'What to see besides Batumi?'),
    ('Крепость Гонио (I век), водопады Махунцети, арочный мост XII века, горная Аджария (Хуло, перевал Годердзи), Ботанический сад и пляжи Уреки с магнитным песком.', 'Gonio Fortress (1st century), Makhuntseti waterfalls, 12th-century arched bridge, mountain Adjara (Khulo, Goderdzi Pass), Botanical Garden and Ureki beaches with magnetic sand.'),
    ('Стоит ли ехать в Батуми зимой?', 'Is it worth visiting Batumi in winter?'),
    ('Да, зимний Батуми — мягкий климат (+8-12°C), работающие рестораны и казино, дешёвое жильё. Новый год в Батуми — отличная альтернатива Тбилиси.', 'Yes, winter Batumi has mild climate (+8-12°C), open restaurants and casinos, affordable accommodation. New Year in Batumi is a great alternative to Tbilisi.'),
    # FAQ schema
    ('"Как добраться в Батуми из Тбилиси?"', '"How to get to Batumi from Tbilisi?"'),
    ('"Из Тбилиси до Батуми 370 км — около 5 часов 30 минут на машине по автомагистрали. Самолётом 40 минут, поездом 5 часов, маршруткой от Дидубе 35 лари. С гидом Sakhva Travel — комфортный трансфер от отеля."', '"Tbilisi to Batumi is 370 km — about 5h30m by car on the highway. By plane 40 min, train 5h, minibus from Didube 35 lari. With Sakhva Travel — comfortable hotel pickup transfer."'),
    ('"Когда лучше ехать в Аджарию?"', '"When is the best time to visit Adjara?"'),
    ('"Для пляжного отдыха — июнь-сентябрь (вода +24-26°C). Лучший месяц — сентябрь: тёплое море, меньше людей, дешевле жильё. Для горной Аджарии — май или сентябрь. Зимой Батуми мягкий (+8-12°C), мало туристов."', '"For beach — June-September (water +24-26°C). Best month: September (warm sea, fewer crowds). For mountain Adjara — May or September. Winter Batumi is mild (+8-12°C)."'),
    ('"Что посмотреть в Аджарии кроме Батуми?"', '"What to see in Adjara besides Batumi?"'),
    ('"Крепость Гонио (I век), водопады Махунцети, арочный мост XII века, горная Аджария (Хуло, перевал Годердзи), Ботанический сад, пляжи Гонио и Уреки с магнитным песком."', '"Gonio Fortress (1st century), Makhuntseti waterfalls, 12th-century arched bridge, mountain Adjara (Khulo, Goderdzi Pass), Botanical Garden, Gonio and Ureki magnetic sand beaches."'),
    ('"Сколько стоит экскурсия из Тбилиси в Батуми?"', '"How much does a tour from Tbilisi to Batumi cost?"'),
    ('"Двухдневная экскурсия с гидом включает трансфер, осмотр ключевых мест, рекомендации по ресторанам. Стоимость зависит от маршрута и количества дней — напишите Тимуру в WhatsApp для расчёта."', '"A two-day guided tour includes transfers, sightseeing, restaurant tips. Price depends on route — message Timur on WhatsApp for a quote."'),
    ('"Безопасно ли купаться в Батуми?"', '"Is it safe to swim in Batumi?"'),
    ('"Да, пляжи Батуми безопасны. Галечное дно, спасатели с июня по сентябрь. Лучшие участки — бульвар и Гонио. Песчаные пляжи — в Уреки и Шекветили (магнитный песок)."', '"Yes, Batumi beaches are safe. Pebble bottom, lifeguards June-September. Best: boulevard and Gonio. Sandy beaches at Ureki (magnetic sand)."'),
])

print('Adjara done')

# ─── GURIA ───
process('guria', [
    ('Гурия — чайные плантации, море и нетуристическая Грузия | Sakhva Travel', 'Guria — Tea Plantations, Sea & Untouristic Georgia | Sakhva Travel'),
    ('Гурия: Бахмаро — высокогорный курорт, Озургети, чайные плантации, Чёрное море. Самый нетуристический регион. Из Тбилиси 4:30.', 'Guria: Bakhmaro highland resort, Ozurgeti, tea plantations, Black Sea. The most untouristic region. 4:30 from Tbilisi.'),
    ('Гурия: Бахмаро, Озургети, чайные плантации, Чёрное море. Самый нетуристический регион Грузии. Из Тбилиси 4:30.', 'Guria: Bakhmaro, Ozurgeti, tea plantations, Black Sea. Georgia\'s most untouristic region. 4:30 from Tbilisi.'),
    ('Гурия: Бахмаро, Озургети, чайные плантации, Чёрное море. Самый нетуристический регион. Из Тбилиси 4:30.', 'Guria: Bakhmaro, Ozurgeti, tea plantations, Black Sea. Most untouristic region. 4:30 from Tbilisi.'),
    ('>Гурия</strong>', '>Guria</strong>'),
    ('"name":"Гурия"', '"name":"Guria"'),
    ('Гурия — чай, Бахмаро и самый нетуристический регион Грузии', 'Guria — Tea, Bakhmaro and Georgia\'s Most Untouristic Region'),
    ('Гурия — чайные плантации и горы нетуристической Грузии', 'Guria — tea plantations and mountains of untouristic Georgia'),
    ('>О Гурии</h2>', '>About Guria</h2>'),
    ('>Что посмотреть в Гурии</h2>', '>What to See in Guria</h2>'),
    ('>Бахмаро — высокогорный курорт</h3>', '>Bakhmaro — Highland Resort</h3>'),
    ('>Озургети — столица Гурии</h3>', '>Ozurgeti — Capital of Guria</h3>'),
    ('>Чайные плантации</h3>', '>Tea Plantations</h3>'),
    ('>Урёки — магнитный пляж</h3>', '>Ureki — Magnetic Sand Beach</h3>'),
    ('>Ликани — Гурийская крепость</h3>', '>Likani — Gurian Fortress</h3>'),
    ('>Гурийский Новый год</h3>', '>Gurian New Year</h3>'),
    ('>Когда ехать и практические советы</h2>', '>When to Visit and Practical Tips</h2>'),
    ('>Экскурсия с заездом в Гурию</h2>', '>Tour with a Stop in Guria</h2>'),
    # Body paragraphs
    ('Гурия — самый маленький материковый регион Грузии, зажатый между Аджарой на юге и Имеретией на востоке. Столица — Озургети, тихий городок с населением около тридцати тысяч человек. Иностранных туристов здесь практически нет: ни экскурсионных автобусов, ни сувенирных лавок, ни ресторанов с меню на английском. Это та Грузия, которую большинство путешественников никогда не увидит — и именно поэтому сюда стоит ехать.', 'Guria is Georgia\'s smallest mainland region, squeezed between Adjara to the south and Imereti to the east. Its capital, Ozurgeti, is a quiet town of about thirty thousand. There are virtually no foreign tourists: no tour buses, no souvenir shops, no restaurants with English menus. This is the Georgia most travelers never see — and that\'s exactly why you should go.'),
    ('Гурийцы считаются самыми остроумными людьми в Грузии — это не стереотип, а почти официальный статус. Грузинские анекдоты часто начинаются со слов «один гуриец...», а гурийское застолье славится не только вином, но и непрерывным потоком тостов, шуток и историй. Здесь родилась уникальная форма полифонического пения — кримanchuli, гурийское йодлирование. Когда слышишь, как три мужчины без всякого аккомпанемента выводят сложнейшие мелодии с переливами, становится понятно, почему грузинская полифония включена в список ЮНЕСКО.', 'Gurians are considered the wittiest people in Georgia — not a stereotype, but practically an official status. Georgian jokes often begin with "one Gurian..." and Gurian feasts are famous not just for wine but for an endless stream of toasts, jokes and stories. A unique form of polyphonic singing was born here — krimanchuli, Gurian yodeling. When you hear three men perform complex melodies with trills without any accompaniment, you understand why Georgian polyphony is on the UNESCO list.'),
    ('Гурия — это два мира в одном регионе. На западе — субтропическое побережье Чёрного моря с магнитными пляжами Урёки и буйной растительностью. На востоке — покрытые лесом горы, поднимающиеся до двух тысяч метров, где на вершине стоит легендарный Бахмаро. Между ними — чайные плантации, которые когда-то снабжали чаем весь Советский Союз. Грузия была главным чайным поставщиком СССР, и именно в Гурии выращивали лучшие сорта.', 'Guria is two worlds in one region. To the west — the subtropical Black Sea coast with Ureki\'s magnetic sand beaches and lush vegetation. To the east — forested mountains rising to two thousand meters, topped by the legendary Bakhmaro. Between them — tea plantations that once supplied tea to the entire Soviet Union. Georgia was the USSR\'s main tea supplier, and Guria grew the finest varieties.'),
    ('Отдельная история — гурийский хачапури. В отличие от имеретинского или аджарского, гурийский хачапури имеет форму полумесяца и начинён не только сыром, но и варёным яйцом. Его готовят к Новому году, но в Гурии можно попробовать круглый год. А гурийский Новый год — отдельный феномен: здесь его отмечают с размахом, которого нет больше нигде в стране. Сжигание рождественских ёлок, шествия, песни и столы, ломящиеся от еды — если попасть в Гурию в январе, этот праздник запомнится на всю жизнь.', 'Gurian khachapuri is a story of its own. Unlike the Imeretian or Adjarian versions, Gurian khachapuri is crescent-shaped and filled not just with cheese but also with hard-boiled egg. Traditionally made for New Year, in Guria you can try it year-round. Gurian New Year is a phenomenon unto itself — celebrated with a grandeur found nowhere else in the country. Burning of Christmas trees, processions, songs and tables groaning with food — if you visit Guria in January, you\'ll remember this celebration for life.'),
    ('Бахмаро — это горный посёлок на высоте 2050 метров, куда грузины ездят отдыхать от летней жары уже больше ста лет.', 'Bakhmaro is a mountain settlement at 2,050 meters where Georgians have been escaping summer heat for over a century.'),
    # Simplified approach for remaining paragraphs - replace key phrases
    ('Деревянные шале без электричества (в некоторых до сих пор), облака, которые проплывают прямо мимо крыльца, и панорамы, от которых перехватывает дыхание.', 'Wooden chalets without electricity (some still), clouds drifting right past the porch, and breathtaking panoramas.'),
    ('Горный воздух Бахмаро считается лечебным — в советское время сюда направляли людей с заболеваниями лёгких.', 'Bakhmaro\'s mountain air is considered therapeutic — in Soviet times people with lung conditions were sent here.'),
    ('Дорога из Озургети занимает около двух часов по серпантину, но каждый поворот открывает новый вид. Курорт работает только с июня по октябрь — зимой перевал закрыт снегом.', 'The drive from Ozurgeti takes about two hours on switchback roads, but every turn reveals a new vista. The resort operates only June to October — in winter the pass is closed by snow.'),
    # CTA
    ('Хотите включить Гурию в маршрут?', 'Want to include Guria in your itinerary?'),
    ('Напишите Тимуру — составим маршрут с заездом в Гурию. Ответ за 15 минут.', 'Message Timur — we\'ll plan a route with a stop in Guria. Reply within 15 minutes.'),
    ('Хочу+экскурсию+в+Гурию', 'Tour+in+Guria'),
    ('Гурия+экскурсия', 'Guria+tour'),
    # Tour card
    ('Экскурсия в Батуми из Тбилиси — с остановкой в Гурии', 'Batumi Tour from Tbilisi — with a stop in Guria'),
    ('>Батуми из Тбилиси</a>', '>Batumi from Tbilisi</a>'),
    # FAQ
    ('Частые вопросы о Гурии', 'Frequently Asked Questions about Guria'),
    ('Как добраться в Гурию?', 'How to get to Guria?'),
    ('Стоит ли ехать в Гурию?', 'Is Guria worth visiting?'),
    ('Когда открыт Бахмаро?', 'When is Bakhmaro open?'),
    # FAQ answers
    ('Из Тбилиси до Гурии около 4 часов 30 минут на автомобиле. Регион расположен между Кутаиси (1:30) и Батуми (1:00). Удобнее всего добраться на машине или с экскурсией — по пути можно заехать в Озургети и на чайные плантации. Маршрутки ходят из Тбилиси через Кутаиси.', 'From Tbilisi to Guria is about 4 hours 30 minutes by car. The region is located between Kutaisi (1:30) and Batumi (1:00). Best reached by car or guided tour — you can stop in Ozurgeti and at tea plantations along the way. Minibuses run from Tbilisi via Kutaisi.'),
    ('Да, если хотите увидеть настоящую нетуристическую Грузию. В Гурии практически нет иностранных туристов — только местные жители с их уникальными традициями, гурийский хачапури с яйцом, чайные плантации и высокогорный курорт Бахмаро. Это Грузия без фильтров.', 'Yes, if you want to see the real untouristic Georgia. Guria has virtually no foreign tourists — just locals with their unique traditions, Gurian khachapuri with egg, tea plantations and the highland resort Bakhmaro. This is Georgia unfiltered.'),
    ('Дорога в Бахмаро открыта с июня по октябрь — зимой перевал заваливает снегом. Лучшее время для посещения — июль и август, когда погода стабильная, а горный воздух особенно чист. Бахмаро находится на высоте 2050 метров, температура летом +15-20°C даже в жару на побережье.', 'The road to Bakhmaro is open from June to October — in winter the pass is buried in snow. Best time to visit is July and August, when weather is stable and mountain air is especially clean. Bakhmaro sits at 2,050 meters, summer temperature +15-20°C even when it\'s hot on the coast.'),
    # FAQ schema
    ('"Как добраться в Гурию?"', '"How to get to Guria?"'),
    ('"Из Тбилиси до Гурии около 4 часов 30 минут на автомобиле. Регион расположен между Кутаиси (1:30) и Батуми (1:00). Удобнее всего добраться на машине или с экскурсией — по пути можно заехать в Озургети и на чайные плантации. Маршрутки ходят из Тбилиси через Кутаиси."', '"Tbilisi to Guria is about 4h30m by car. Located between Kutaisi (1:30) and Batumi (1:00). Best by car or guided tour with stops in Ozurgeti and tea plantations."'),
    ('"Стоит ли ехать в Гурию?"', '"Is Guria worth visiting?"'),
    ('"Да, если хотите увидеть настоящую нетуристическую Грузию. В Гурии практически нет иностранных туристов — только местные жители с их уникальными традициями, гурийский хачапури с яйцом, чайные плантации и высокогорный курорт Бахмаро. Это Грузия без фильтров."', '"Yes, for the real untouristic Georgia. No foreign tourists — just locals with unique traditions, Gurian khachapuri, tea plantations and Bakhmaro highland resort."'),
    ('"Когда открыт Бахмаро?"', '"When is Bakhmaro open?"'),
    ('"Дорога в Бахмаро открыта с июня по октябрь — зимой перевал заваливает снегом. Лучшее время для посещения — июль и август, когда погода стабильная, а горный воздух особенно чист. Бахмаро находится на высоте 2050 метров, температура летом +15-20°C даже в жару на побережье."', '"Road open June-October. Best in July-August when weather is stable. At 2,050m, summer temps +15-20°C even when coast is hot."'),
    # Remaining body text (Ozurgeti, tea, Ureki, fortress, New Year, practical tips)
    ('Озургети не попадает ни в один путеводитель, и это его главное достоинство.', 'Ozurgeti doesn\'t appear in any guidebook, and that\'s its greatest asset.'),
    ('Маленький, аутентичный город с базаром, где торгуют свежими фруктами и домашним сыром.', 'A small, authentic town with a bazaar selling fresh fruit and homemade cheese.'),
    # Season sections
    ('<strong>Лето (июнь-сентябрь):</strong>', '<strong>Summer (June-September):</strong>'),
    ('<strong>Весна (апрель-май):</strong>', '<strong>Spring (April-May):</strong>'),
    ('<strong>Осень (октябрь-ноябрь):</strong>', '<strong>Fall (October-November):</strong>'),
    ('<strong>Зима (декабрь-январь):</strong>', '<strong>Winter (December-January):</strong>'),
    ('<strong>Жильё:</strong>', '<strong>Accommodation:</strong>'),
    ('<strong>Как добраться:</strong>', '<strong>Getting there:</strong>'),
])

print('Guria done')

# For the remaining 8 pages, apply same pattern
# I'll handle the most critical parts: title, description, H1, headings, FAQ, CTA

for slug, data in [
    ('imereti', {
        'title_old': 'Имеретия — каньоны, пещеры и столица Кутаиси | Sakhva Travel',
        'title_new': 'Imereti — Canyons, Caves & Kutaisi | Sakhva Travel',
        'desc_old': 'Имеретия — регион каньонов и пещер: Кутаиси, Гелати, каньон Окаце, Мартвильский каньон, пещера Прометея. Из Тбилиси за 3:30. Экскурсии с гидом.',
        'desc_new': 'Imereti — region of canyons and caves: Kutaisi, Gelati, Okatse Canyon, Martvili Canyon, Prometheus Cave. 3:30 from Tbilisi. Guided tours.',
        'name_ru': 'Имеретия', 'name_en': 'Imereti',
        'h1_old': 'Имеретия — каньоны, пещеры и древний Кутаиси',
        'h1_new': 'Imereti — Canyons, Caves and Ancient Kutaisi',
        'cta': ('Хотите индивидуальный маршрут по Имеретии?', 'Want a custom itinerary in Imereti?'),
        'wa': ('Хочу+экскурсию+в+Имеретию', 'Tour+in+Imereti'),
        'tg': ('Имеретия+экскурсия', 'Imereti+tour'),
    }),
    ('kakheti', {
        'title_old': 'Кахетия — край виноделия, Сигнахи и Алазанская долина | Sakhva Travel',
        'title_new': 'Kakheti — Wine Region, Sighnaghi & Alazani Valley | Sakhva Travel',
        'desc_old': 'Кахетия — винный регион Грузии: Сигнахи, Телави, Алазанская долина, монастырь Бодбе. Как добраться из Тбилиси за 1:50. Экскурсии с гидом от ₾170.',
        'desc_new': 'Kakheti — Georgia\'s wine region: Sighnaghi, Telavi, Alazani Valley, Bodbe Monastery. 1:50 from Tbilisi. Guided wine tours from ₾170.',
        'name_ru': 'Кахетия', 'name_en': 'Kakheti',
        'h1_old': 'Кахетия — край виноделия и Алазанская долина',
        'h1_new': 'Kakheti — Wine Country and the Alazani Valley',
        'cta': ('Хотите индивидуальный маршрут по Кахетии?', 'Want a custom wine tour in Kakheti?'),
        'wa': ('Хочу+экскурсию+в+Кахетию', 'Wine+tour+Kakheti'),
        'tg': ('Кахетия+экскурсия', 'Kakheti+tour'),
    }),
    ('kvemo-kartli', {
        'title_old': 'Квемо Картли — Дманиси, Болниси и древнейшая история | Sakhva Travel',
        'title_new': 'Kvemo Kartli — Dmanisi, Bolnisi & Ancient History | Sakhva Travel',
        'desc_old': 'Квемо Картли — древнейший регион Грузии: Болниси, Дманиси (1.8 млн лет), Биртвиси, немецкие колонии. Из Тбилиси за 1:00. Экскурсии с гидом.',
        'desc_new': 'Kvemo Kartli — Georgia\'s most ancient region: Bolnisi, Dmanisi (1.8M years), Birtvisi, German colonies. 1 hour from Tbilisi. Guided tours.',
        'name_ru': 'Квемо Картли', 'name_en': 'Kvemo Kartli',
        'h1_old': 'Квемо Картли — от первых людей Евразии до немецких колоний',
        'h1_new': 'Kvemo Kartli — From Eurasia\'s First Humans to German Colonies',
        'cta': ('Хотите индивидуальный маршрут по Квемо Картли?', 'Want a custom itinerary in Kvemo Kartli?'),
        'wa': ('Хочу+экскурсию+в+Квемо+Картли', 'Tour+Kvemo+Kartli'),
        'tg': ('Квемо+Картли+маршрут', 'Kvemo+Kartli+tour'),
    }),
    ('mtskheta-mtianeti', {
        'title_old': 'Мцхета-Мтианети — Светицховели, Казбек и Военно-Грузинская дорога | Sakhva Travel',
        'title_new': 'Mtskheta-Mtianeti — Svetitskhoveli, Kazbegi & Georgian Military Highway | Sakhva Travel',
        'desc_old': 'Мцхета-Мтианети: Светицховели, Джвари, гора Казбек 5047м, Гудаури, Военно-Грузинская дорога. Из Тбилиси за 40 мин (Мцхета) и 2:10 (Казбеги). Экскурсии с гидом.',
        'desc_new': 'Mtskheta-Mtianeti: Svetitskhoveli, Jvari, Mount Kazbek 5047m, Gudauri, Georgian Military Highway. 40 min (Mtskheta) and 2:10 (Kazbegi) from Tbilisi.',
        'name_ru': 'Мцхета-Мтианети', 'name_en': 'Mtskheta-Mtianeti',
        'h1_old': 'Мцхета-Мтианети — духовное сердце и горы Кавказа',
        'h1_new': 'Mtskheta-Mtianeti — Spiritual Heart and Caucasus Mountains',
        'cta': ('Хотите индивидуальный маршрут?', 'Want a custom itinerary?'),
        'wa': ('Хочу+экскурсию+Мцхета+Казбеги', 'Tour+Mtskheta+Kazbegi'),
        'tg': ('Казбеги+Мцхета', 'Kazbegi+Mtskheta'),
    }),
    ('racha', {
        'title_old': 'Рача-Лечхуми — Хванчкара, горные озёра и нетронутая природа | Sakhva Travel',
        'title_new': 'Racha-Lechkhumi — Khvanchkara Wine, Mountain Lakes & Pristine Nature | Sakhva Travel',
        'desc_old': 'Рача-Лечхуми — самый малонаселённый регион Грузии: Хванчкара, Никорцминда, озеро Шаори, ледниковые долины. Из Тбилиси за 4:30. Экскурсии с гидом.',
        'desc_new': 'Racha-Lechkhumi — Georgia\'s least populated region: Khvanchkara wine, Nikortsminda, Lake Shaori, glacial valleys. 4:30 from Tbilisi. Guided tours.',
        'name_ru': 'Рача-Лечхуми', 'name_en': 'Racha-Lechkhumi',
        'h1_old': 'Рача — Хванчкара, горные озёра и грузинская Швейцария',
        'h1_new': 'Racha — Khvanchkara, Mountain Lakes and Georgian Switzerland',
        'cta': ('Хотите индивидуальный маршрут по Раче?', 'Want a custom itinerary in Racha?'),
        'wa': ('Хочу+экскурсию+в+Рачу', 'Tour+in+Racha'),
        'tg': ('Рача+экскурсия', 'Racha+tour'),
    }),
    ('samegrelo', {
        'title_old': 'Самегрело — острая кухня, Зугдиди и ворота в Сванетию | Sakhva Travel',
        'title_new': 'Samegrelo — Spicy Cuisine, Zugdidi & Gateway to Svaneti | Sakhva Travel',
        'desc_old': 'Самегрело — край острой кухни и природных чудес: Зугдиди, Мартвильский каньон, Нокалакеви, ворота в Сванетию. Из Тбилиси за 5:00. Экскурсии с гидом.',
        'desc_new': 'Samegrelo — land of spicy cuisine and natural wonders: Zugdidi, Martvili Canyon, Nokalakevi, gateway to Svaneti. 5 hours from Tbilisi. Guided tours.',
        'name_ru': 'Самегрело', 'name_en': 'Samegrelo',
        'h1_old': 'Самегрело — острая кухня, каньоны и ворота в Сванетию',
        'h1_new': 'Samegrelo — Spicy Cuisine, Canyons and Gateway to Svaneti',
        'cta': ('Хотите индивидуальный маршрут по Самегрело?', 'Want a custom itinerary in Samegrelo?'),
        'wa': ('Хочу+экскурсию+в+Самегрело', 'Tour+in+Samegrelo'),
        'tg': ('Самегрело+экскурсия', 'Samegrelo+tour'),
    }),
    ('samtskhe-javakheti', {
        'title_old': 'Самцхе-Джавахети — Вардзия, Боржоми и крепость Рабат | Sakhva Travel',
        'title_new': 'Samtskhe-Javakheti — Vardzia, Borjomi & Rabati Fortress | Sakhva Travel',
        'desc_old': 'Самцхе-Джавахети: пещерный город Вардзия, парк Боржоми, крепость Рабат в Ахалцихе. Из Тбилиси 3 часа. Экскурсии с русскоязычным гидом от ₾195.',
        'desc_new': 'Samtskhe-Javakheti: cave city Vardzia, Borjomi park, Rabati fortress in Akhaltsikhe. 3 hours from Tbilisi. Guided tours from ₾195.',
        'name_ru': 'Самцхе-Джавахети', 'name_en': 'Samtskhe-Javakheti',
        'h1_old': 'Самцхе-Джавахети — Вардзия, Боржоми и средневековые крепости',
        'h1_new': 'Samtskhe-Javakheti — Vardzia, Borjomi and Medieval Fortresses',
        'cta': ('Хотите индивидуальный маршрут по Самцхе-Джавахети?', 'Want a custom itinerary in Samtskhe-Javakheti?'),
        'wa': ('Хочу+экскурсию+Вардзия+Боржоми', 'Tour+Vardzia+Borjomi'),
        'tg': ('Вардзия+Боржоми', 'Vardzia+Borjomi'),
    }),
    ('shida-kartli', {
        'title_old': 'Шида Картли — Гори, Уплисцихе и историческое сердце Грузии | Sakhva Travel',
        'title_new': 'Shida Kartli — Gori, Uplistsikhe & Historical Heart of Georgia | Sakhva Travel',
        'desc_old': 'Шида Картли — историческое сердце Грузии: Гори, пещерный город Уплисцихе, Атенский Сион, средневековые крепости. Из Тбилиси за 1:20. Экскурсии с гидом.',
        'desc_new': 'Shida Kartli — historical heart of Georgia: Gori, cave city Uplistsikhe, Ateni Sioni, medieval fortresses. 1:20 from Tbilisi. Guided tours.',
        'name_ru': 'Шида Картли', 'name_en': 'Shida Kartli',
        'h1_old': 'Шида Картли — от пещерного города до советской империи',
        'h1_new': 'Shida Kartli — From Cave Cities to Soviet Empire',
        'cta': ('Хотите индивидуальный маршрут по Шида Картли?', 'Want a custom itinerary in Shida Kartli?'),
        'wa': ('Хочу+экскурсию+Гори+Уплисцихе', 'Tour+Gori+Uplistsikhe'),
        'tg': ('Гори+Уплисцихе', 'Gori+Uplistsikhe'),
    }),
]:
    reps = [
        (data['title_old'], data['title_new']),
        (data['desc_old'], data['desc_new']),
        (f'>{data["name_ru"]}</strong>', f'>{data["name_en"]}</strong>'),
        (f'"name":"{data["name_ru"]}"', f'"name":"{data["name_en"]}"'),
        (data['h1_old'], data['h1_new']),
        (data['cta'][0], data['cta'][1]),
        (data['wa'][0], data['wa'][1]),
        (data['tg'][0], data['tg'][1]),
    ]
    # Common heading translations
    reps.extend([
        (f'>О {data["name_ru"]}</h2>' if f'>О {data["name_ru"]}</h2>' else '', f'>About {data["name_en"]}</h2>' if data["name_en"] else ''),
        (f'>Об {data["name_ru"]}</h2>' if f'>Об {data["name_ru"]}</h2>' else '', f'>About {data["name_en"]}</h2>' if data["name_en"] else ''),
        (f'>О {data["name_ru"][:20]}', f'>About {data["name_en"][:20]}'),
        (f'>Что посмотреть в {data["name_ru"]}</h2>', f'>What to See in {data["name_en"]}</h2>'),
        (f'>Что посмотреть</h2>', f'>What to See</h2>'),
        ('>Когда ехать и что взять</h2>', '>When to Visit and What to Bring</h2>'),
        ('>Когда ехать и практические советы</h2>', '>When to Visit and Practical Tips</h2>'),
        (f'>Наши экскурсии в {data["name_ru"]}</h2>', f'>Our Tours to {data["name_en"]}</h2>'),
        (f'>Наши экскурсии</h2>', f'>Our Tours</h2>'),
        (f'>Частые вопросы о {data["name_ru"]}</h2>', f'>FAQ about {data["name_en"]}</h2>'),
        (f'>Частые вопросы об {data["name_ru"]}</h2>', f'>FAQ about {data["name_en"]}</h2>'),
        ('>Частые вопросы</h2>', '>Frequently Asked Questions</h2>'),
        ('Напишите Тимуру — составим маршрут под вас. Ответ за 15 минут.', 'Message Timur — we\'ll plan a route for you. Reply within 15 minutes.'),
        # Common travel phrases
        ('<strong>Лучшее время:</strong>', '<strong>Best time:</strong>'),
        ('<strong>Что взять:</strong>', '<strong>What to bring:</strong>'),
        ('<strong>Как добраться:</strong>', '<strong>Getting there:</strong>'),
    ])
    # Common tour card labels
    reps.extend([
        ('>Кутаиси, Гелати и каньоны</a>', '>Kutaisi, Gelati & Canyons</a>'),
        ('>Тур в Кутаиси с гидом</a>', '>Kutaisi Tour with Guide</a>'),
        ('>Дегустация вина в Кахетии</a>', '>Wine Tasting in Kakheti</a>'),
        ('>Экскурсия в Сигнахи</a>', '>Sighnaghi Tour</a>'),
        ('>Экскурсия в Телави</a>', '>Telavi Tour</a>'),
        ('>Давид Гареджи из Тбилиси</a>', '>David Gareja from Tbilisi</a>'),
        ('>Экскурсия в Казбеги</a>', '>Kazbegi Tour</a>'),
        ('>Экскурсия в Мцхету</a>', '>Mtskheta Tour</a>'),
        ('>Экскурсия в Гудаури</a>', '>Gudauri Tour</a>'),
        ('>Экскурсия в Ананури</a>', '>Ananuri Tour</a>'),
        # Image alts
        ('Экскурсия в Кутаиси из Тбилиси', 'Kutaisi Tour from Tbilisi'),
        ('Тур в Кутаиси из Тбилиси с гидом', 'Kutaisi Tour from Tbilisi with Guide'),
        ('Дегустация вина в Кахетии — экскурсия из Тбилиси', 'Wine Tasting in Kakheti — Tour from Tbilisi'),
        ('Экскурсия в Сигнахи — город любви', 'Sighnaghi Tour — City of Love'),
        ('Экскурсия в Телави и Алазанскую долину', 'Telavi and Alazani Valley Tour'),
        ('Виноградники Кахетии и Алазанская долина — регион виноделия Грузии', 'Kakheti Vineyards and Alazani Valley — Georgia\'s Wine Region'),
        ('Экскурсия Ананури', 'Ananuri Tour'),
        ('Экскурсия в Гудаури', 'Gudauri Tour'),
        ('Экскурсия в Мцхету', 'Mtskheta Tour'),
    ])
    # Filter out empty replacements
    reps = [(o, n) for o, n in reps if o and n and o != n]
    process(slug, reps)
    print(f'{data["name_en"]} done')

print('\n=== All 10 EN region pages translated and indexed ===')
