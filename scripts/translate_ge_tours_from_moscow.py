# -*- coding: utf-8 -*-
"""Перевод ge/tours-from-moscow/index.html EN->KA (грузинский).
Каркас (lang/canonical/hreflang/og:locale/ge.css/переключатель) уже сделан gen_ge.py.
Здесь переводится только видимый контент + meta-текст + natural-language в JSON-LD.
URL/атрибуты/JS/структура схемы не трогаются. Порядок: сначала блоки (таблицы,
абзацы, карточки), потом nav/footer — чтобы счётчики совпадали."""
import sys

FILE = "ge/tours-from-moscow/index.html"

GE_TITLE = "ტურები საქართველოში მოსკოვიდან 2026 — ავიაბილეთები და კერძო ტურები"

# (old, new, expected_count) — заполняется по секциям ниже
R = []

def add(old, new, n=1):
    R.append((old, new, n))

# ===================== СЕКЦИИ (заполняются ниже) =====================
# --- HEAD / META ---
add('<title>Tours to Georgia from Moscow 2026 — Flights &amp; Private Tours</title>',
    f'<title>{GE_TITLE}</title>')
add('content="Tours to Georgia from Moscow 2026 — Flights &amp; Private Tours" property="og:title"',
    f'content="{GE_TITLE}" property="og:title"')
add('content="Tours to Georgia from Moscow 2026 — Flights &amp; Private Tours" name="twitter:title"',
    f'content="{GE_TITLE}" name="twitter:title"')
add('Trip to Georgia from Moscow? Flights from 15K RUB, tours from ₾98. Itineraries 5/7/10 days with guide Timur. 30% cheaper than packages.',
    'მოგზაურობა საქართველოში მოსკოვიდან? ავიაბილეთები 15 ათასი ₽-დან, ტურები ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან. პაკეტებზე 30%-ით იაფი.')
add('Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur. 30% cheaper than package tours.',
    'ავიაბილეთები 15 ათასი ₽-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან. პაკეტ-ტურებზე 30%-ით იაფი.')
add('Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with a private tour.',
    'ავიაბილეთები 15 ათასი ₽-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე კერძო ტურით.')
add('Tours to Georgia from Moscow 2026 — Flights &amp; Guided Tours | Sakhva Travel',
    'ტურები საქართველოში მოსკოვიდან 2026 — ავიაბილეთები და ტურები გიდთან | Sakhva Travel')

# --- JSON-LD FAQ (head graph) ---
add('"name": "How to get to Tbilisi from Moscow?"',
    '"name": "როგორ მოვხვდე თბილისში მოსკოვიდან?"')
add('Direct flights operate again — Georgian Airways, Red Wings and Azimuth fly Moscow to Tbilisi in about 2h 50m (round-trip from 13,600 RUB). Connecting options include routes via Istanbul (Turkish Airlines, ~5–6 hours total), Dubai (flydubai/Emirates), Yerevan (Armenia Airlines + minibus), or Minsk (Belavia). Average round-trip ticket: 15,000–25,000 RUB. Alternative: bus to Vladikavkaz then minibus via Upper Lars checkpoint (~16–20 hours from Moscow).',
    'პირდაპირი ფრენები კვლავ მოქმედებს — Georgian Airways, Red Wings და Azimuth მოსკოვიდან თბილისში დაახლოებით 2სთ 50წთ-ში ფრენენ (ორმხრივი 13,600 ₽-დან). გადაჯდომით: სტამბოლის გავლით (Turkish Airlines, ჯამში ~5–6 საათი), დუბაის (flydubai/Emirates), ერევნის (Armenia Airlines + მიკროავტობუსი) ან მინსკის (Belavia) გავლით. საშუალო ორმხრივი ბილეთი: 15,000–25,000 ₽. ალტერნატივა: ავტობუსი ვლადიკავკაზამდე, შემდეგ მიკროავტობუსი ზემო ლარსის გამშვები პუნქტის გავლით (~16–20 საათი მოსკოვიდან).')
add('"name": "How much does a 7-day tour to Georgia from Moscow cost?"',
    '"name": "რამდენი ჯდება 7-დღიანი ტური საქართველოში მოსკოვიდან?"')
add("A self-planned 7-day trip from Moscow costs 40,000–70,000 RUB per person: flights 15,000–25,000 RUB + accommodation 5,000–15,000 RUB/week + food 3,000–5,000 RUB + guided tours from ₾98/person. Package tours cost 60,000–100,000 RUB and don't include quality private excursions.",
    'დამოუკიდებლად დაგეგმილი 7-დღიანი მოგზაურობა მოსკოვიდან ჯდება 40,000–70,000 ₽ ერთ ადამიანზე: ავიაბილეთები 15,000–25,000 ₽ + საცხოვრებელი 5,000–15,000 ₽/კვირა + კვება 3,000–5,000 ₽ + ტურები გიდთან ₾98-დან ერთ ადამიანზე. პაკეტ-ტურები ჯდება 60,000–100,000 ₽ და არ მოიცავს ხარისხიან კერძო ექსკურსიებს.')
add('"name": "Do Russian citizens need a visa for Georgia?"',
    '"name": "სჭირდებათ რუსეთის მოქალაქეებს ვიზა საქართველოსთვის?"')
add('No, Russian citizens do not need a visa for Georgia. Russians can stay up to 365 days visa-free with a Russian passport. A foreign passport or internal passport (внутренний паспорт) is accepted at the border.',
    'არა, რუსეთის მოქალაქეებს საქართველოსთვის ვიზა არ სჭირდებათ. რუსებს შეუძლიათ დარჩნენ 365 დღემდე უვიზოდ რუსული პასპორტით. საზღვარზე მიიღება როგორც საზღვარგარეთის, ისე შიდა პასპორტი (внутренний паспорт).')
add('"name": "When is the best time to visit Georgia from Moscow?"',
    '"name": "როდის არის საუკეთესო დრო საქართველოში მოსკოვიდან ჩამოსასვლელად?"')
add('The best time is spring (April–May) and autumn (September–October). Summer is hot (+35–38°C in Tbilisi), winter is mild in the city (+5–10°C) but great for skiing at Gudauri. The Kazbegi season (mountain routes) runs from May to October.',
    'საუკეთესო დროა გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტემბერი–ოქტომბერი). ზაფხული ცხელია (+35–38°C თბილისში), ზამთარი ქალაქში რბილია (+5–10°C), მაგრამ შესანიშნავია გუდაურში სათხილამუროდ. ყაზბეგის სეზონი (მთის მარშრუტები) გრძელდება მაისიდან ოქტომბრამდე.')
add('"name": "What currency to bring to Georgia?"',
    '"name": "რა ვალუტა წავიღო საქართველოში?"')
add('Georgia uses the lari (GEL, ₾). Exchange rubles in Tbilisi — rates are better than in Moscow. Best exchange offices are on Rustaveli Avenue and at Dezerter Market. USD and EUR are accepted everywhere. Mir cards are not accepted — bring cash or a foreign bank card (Visa/Mastercard).',
    'საქართველოში გამოიყენება ლარი (GEL, ₾). რუბლი გადაცვალეთ თბილისში — კურსი მოსკოვზე უკეთესია. საუკეთესო გადამცვლელი პუნქტებია რუსთაველის გამზირზე და დეზერტირების ბაზარში. დოლარი და ევრო ყველგან მიიღება. „მირ“ ბარათები არ მიიღება — წაიღეთ ნაღდი ფული ან უცხოური ბანკის ბარათი (Visa/Mastercard).')
add('"description": "Private tours in Tbilisi and Georgia. Bespoke tours in English since 2023."',
    '"description": "კერძო ტურები თბილისსა და საქართველოში. ინდივიდუალური ტურები ინგლისურად 2023 წლიდან."')
add('"name":"Home","item":"https://sakhva-travel.com/en/"',
    '"name":"მთავარი","item":"https://sakhva-travel.com/en/"')
add('"name":"Tours to Georgia from Moscow","item":"https://sakhva-travel.com/ge/tours-from-moscow/"',
    '"name":"მოსკოვიდან ტურები საქართველოში","item":"https://sakhva-travel.com/ge/tours-from-moscow/"')

# --- HERO / BREADCRUMB / LEAD ---
add('<h1>Tours to Georgia from Moscow 2026 — direct flights and routes</h1>',
    '<h1>ტურები საქართველოში მოსკოვიდან 2026 — პირდაპირი ფრენები და მარშრუტები</h1>')
add('Flights from 15,000 RUB, accommodation from ₾50/night, private tours from ₾98. Itineraries for 5, 7 and 10 days — 30% cheaper than any package tour.',
    'ავიაბილეთები 15,000 ₽-დან, საცხოვრებელი ₾50/ღამედან, კერძო ტურები ₾98-დან. მარშრუტები 5, 7 და 10 დღეზე — ნებისმიერ პაკეტ-ტურზე 30%-ით იაფი.')
add('<div class="stat-num">from 15K</div><div class="stat-label">Flight, RUB</div>',
    '<div class="stat-num">15 ათასიდან</div><div class="stat-label">ფრენა, ₽</div>')
add('<div class="stat-num">₾98</div><div class="stat-label">Tours from</div>',
    '<div class="stat-num">₾98</div><div class="stat-label">ტურები -დან</div>')
add('<div class="stat-num">3–5h</div><div class="stat-label">Travel time</div>',
    '<div class="stat-num">3–5სთ</div><div class="stat-label">მგზავრობის დრო</div>')
add('<div class="stat-num">Visa-free</div><div class="stat-label">RU passport</div>',
    '<div class="stat-num">უვიზოდ</div><div class="stat-label">რუს. პასპორტი</div>')
add('<span>›</span> Tours to Georgia from Moscow',
    '<span>›</span> მოსკოვიდან ტურები საქართველოში')
add('Planning a tour to Georgia from Moscow in 2026 is entirely doable, despite the lack of direct flights. Via Istanbul, Dubai or Yerevan you can reach Tbilisi in 5–8 hours of total travel time. From there, a country awaits where in a single trip you can see the Kazbegi mountains, taste kvevri wine in Kakheti, stroll the medieval streets of Tbilisi and soak in the sulfur baths — all at a budget that will surprise even seasoned travellers. A self-planned trip with a private tour costs 25–35% less than a package tour from a travel agency, and delivers incomparably richer experiences.',
    '2026 წელს საქართველოში მოსკოვიდან ტურის დაგეგმვა სავსებით შესაძლებელია. პირდაპირი ფრენით ან სტამბოლის, დუბაისა თუ ერევნის გავლით თბილისში ჯამში 3–8 საათში მოხვდებით. იქ კი გელით ქვეყანა, სადაც ერთ მოგზაურობაში ნახავთ ყაზბეგის მთებს, დააგემოვნებთ ქვევრის ღვინოს კახეთში, გაისეირნებთ თბილისის შუა საუკუნეების ქუჩებში და დატკბებით გოგირდის აბანოებით — და ეს ყველაფერი ისეთ ბიუჯეტში, რომელიც გამოცდილ მოგზაურსაც კი გააკვირვებს. დამოუკიდებელი მოგზაურობა კერძო ტურით 25–35%-ით იაფია, ვიდრე ტურ-სააგენტოს პაკეტ-ტური, და შეუდარებლად მდიდარ შთაბეჭდილებებს გაძლევთ.')

# --- FLIGHTS ---
add('<h2 class="section-title">How to Get to Georgia from Moscow</h2>',
    '<h2 class="section-title">როგორ მოხვდეთ საქართველოში მოსკოვიდან</h2>')
add('Direct flights resumed in 2023 — plus plenty of connecting routes. Real prices and travel times for 2026.',
    'პირდაპირი ფრენები 2023 წელს განახლდა — პლუს უამრავი გადაჯდომითი მარშრუტი. რეალური ფასები და მგზავრობის დრო 2026 წლისთვის.')
add('''<table class="price-table">
<thead>
<tr>
<th>Route</th>
<th>Airline</th>
<th>Duration</th>
<th>Round-trip Price</th>
</tr>
</thead>
<tbody>
<tr>
<td>Moscow → Tbilisi (direct)</td>
<td>Georgian Airways, Red Wings, Azimuth</td>
<td>2h 50m</td>
<td class="highlight">from 13,600 RUB</td>
</tr>
<tr>
<td>Moscow → Istanbul → Tbilisi</td>
<td>Turkish Airlines</td>
<td>5–7 hours</td>
<td class="highlight">from 15,000 RUB</td>
</tr>
<tr>
<td>Moscow → Dubai → Tbilisi</td>
<td>flydubai / Emirates</td>
<td>7–9 hours</td>
<td class="highlight">from 18,000 RUB</td>
</tr>
<tr>
<td>Moscow → Yerevan → Tbilisi</td>
<td>Armenia Airlines + minibus</td>
<td>5–6h + 3h bus</td>
<td class="highlight">from 16,000 RUB</td>
</tr>
<tr>
<td>Moscow → Minsk → Tbilisi</td>
<td>Belavia</td>
<td>6–8 hours</td>
<td class="highlight">from 20,000 RUB</td>
</tr>
<tr>
<td>Bus via Vladikavkaz (Upper Lars border)</td>
<td>Minibus / coach</td>
<td>16–20 hours</td>
<td class="highlight">from 3,500 RUB</td>
</tr>
</tbody>
</table>''',
'''<table class="price-table">
<thead>
<tr>
<th>მარშრუტი</th>
<th>ავიაკომპანია</th>
<th>ხანგრძლივობა</th>
<th>ორმხრივი ფასი</th>
</tr>
</thead>
<tbody>
<tr>
<td>მოსკოვი → თბილისი (პირდაპირი)</td>
<td>Georgian Airways, Red Wings, Azimuth</td>
<td>2სთ 50წთ</td>
<td class="highlight">13,600 ₽-დან</td>
</tr>
<tr>
<td>მოსკოვი → სტამბოლი → თბილისი</td>
<td>Turkish Airlines</td>
<td>5–7 საათი</td>
<td class="highlight">15,000 ₽-დან</td>
</tr>
<tr>
<td>მოსკოვი → დუბაი → თბილისი</td>
<td>flydubai / Emirates</td>
<td>7–9 საათი</td>
<td class="highlight">18,000 ₽-დან</td>
</tr>
<tr>
<td>მოსკოვი → ერევანი → თბილისი</td>
<td>Armenia Airlines + მიკროავტობუსი</td>
<td>5–6სთ + 3სთ ავტობუსი</td>
<td class="highlight">16,000 ₽-დან</td>
</tr>
<tr>
<td>მოსკოვი → მინსკი → თბილისი</td>
<td>Belavia</td>
<td>6–8 საათი</td>
<td class="highlight">20,000 ₽-დან</td>
</tr>
<tr>
<td>ავტობუსი ვლადიკავკაზის გავლით (ზემო ლარსის საზღვარი)</td>
<td>მიკროავტობუსი / ავტობუსი</td>
<td>16–20 საათი</td>
<td class="highlight">3,500 ₽-დან</td>
</tr>
</tbody>
</table>''')
add('<p><strong>Tip:</strong> Search tickets on Yandex Travel or Skyscanner with the "with connections" filter. Best prices are 2–3 months before departure. Peak season (July–August) can push prices to 30,000–40,000 RUB.</p>',
    '<p><strong>რჩევა:</strong> ბილეთები მოძებნეთ Yandex Travel-ზე ან Skyscanner-ზე ფილტრით „გადაჯდომებით“. საუკეთესო ფასებია გამგზავრებამდე 2–3 თვით ადრე. პიკის სეზონზე (ივლისი–აგვისტო) ფასი შეიძლება 30,000–40,000 ₽-მდე ავიდეს.</p>')

# --- WHAT MOSCOW TRAVELLERS SHOULD KNOW ---
add('<h2 class="section-title" style="margin-top:32px">What Moscow Travellers Should Know</h2>',
    '<h2 class="section-title" style="margin-top:32px">რა უნდა იცოდეს მოსკოვიდან მოგზაურმა</h2>')
add('<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">Time Zone: Just +1 Hour</h3>',
    '<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">დროის სარტყელი: სულ +1 საათი</h3>')
add('<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">The difference from Moscow is minimal — Tbilisi runs on UTC+4. No jet lag: you land in the morning and start exploring right away. Perfect for staying in touch with colleagues back home.</p>',
    '<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">სხვაობა მოსკოვთან მინიმალურია — თბილისი UTC+4-ზეა. ჯეტლაგი არ არის: დილით ჩამოხვალთ და მაშინვე იწყებთ დათვალიერებას. იდეალურია სახლში დარჩენილ კოლეგებთან კავშირის შესანარჩუნებლად.</p>')
add('<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">Three Airports — More Options</h3>',
    '<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">სამი აეროპორტი — მეტი არჩევანი</h3>')
add('<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">Flights to Tbilisi depart from Sheremetyevo, Domodedovo and Vnukovo. Up to 10 flights per day via Istanbul, Dubai and Yerevan. Always compare all three airports for the best deal.</p>',
    '<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">თბილისში ფრენები გადის შერემეტიევოდან, დომოდედოვოდან და ვნუკოვოდან. დღეში 10-მდე ფრენა სტამბოლის, დუბაისა და ერევნის გავლით. საუკეთესო შეთავაზებისთვის ყოველთვის შეადარეთ სამივე აეროპორტი.</p>')
add('<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">From Skyscrapers to Ancient Streets</h3>',
    '<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">ცათამბჯენებიდან უძველეს ქუჩებამდე</h3>')
add("<p style=\"font-size:14px;color:#4B5563;margin:0;line-height:1.6\">After Moscow's glass towers, Old Tbilisi with its carved wooden balconies and narrow alleys feels like a journey through time. Many Moscow visitors say this contrast is the highlight of their whole trip.</p>",
    '<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">მოსკოვის შუშის კოშკების შემდეგ ძველი თბილისი თავისი მოჩუქურთმებული ხის აივნებითა და ვიწრო შესახვევებით დროში მოგზაურობას მოგაგონებთ. მოსკოვიდან ბევრი სტუმარი ამბობს, რომ სწორედ ეს კონტრასტია მთელი მოგზაურობის მთავარი შთაბეჭდილება.</p>')
add('<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">Moscow Flights Are the Cheapest</h3>',
    '<h3 style="font-size:16px;font-weight:700;color:#1A3D2E;margin:0 0 8px">მოსკოვიდან ფრენები ყველაზე იაფია</h3>')
add('<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">Thanks to strong competition among carriers, Moscow–Tbilisi tickets are among the most affordable. In the off-season you can find round trips from 15,000 RUB on Yandex Travel.</p>',
    '<p style="font-size:14px;color:#4B5563;margin:0;line-height:1.6">გადამზიდავებს შორის ძლიერი კონკურენციის წყალობით მოსკოვი–თბილისის ბილეთები ყველაზე ხელმისაწვდომია. სეზონგარეშე Yandex Travel-ზე ორმხრივი ბილეთი 15,000 ₽-დან იშოვება.</p>')

# --- BUDGET ---
add('<h2 class="section-title">Budget for a Trip to Georgia from Moscow</h2>',
    '<h2 class="section-title">ბიუჯეტი მოგზაურობისთვის საქართველოში მოსკოვიდან</h2>')
add('Real cost breakdown for 7 days, one person. Prices for April–October 2026.',
    'რეალური ხარჯების ჩაშლა 7 დღეზე, ერთ ადამიანზე. ფასები 2026 წლის აპრილი–ოქტომბრისთვის.')
add('''<table class="price-table">
<thead>
<tr>
<th>Expense</th>
<th>Budget</th>
<th>Mid-range</th>
<th>Comfort</th>
</tr>
</thead>
<tbody>
<tr>
<td>Round-trip flights</td>
<td>15,000 RUB</td>
<td>20,000 RUB</td>
<td>30,000 RUB</td>
</tr>
<tr>
<td>Accommodation (7 nights)</td>
<td class="highlight">5,500 RUB (hostel/Airbnb)</td>
<td>12,000 RUB</td>
<td>25,000 RUB</td>
</tr>
<tr>
<td>Food</td>
<td>3,000 RUB</td>
<td>5,000 RUB</td>
<td>9,000 RUB</td>
</tr>
<tr>
<td>Guided tours (3 excursions)</td>
<td class="highlight">from 12,000 RUB</td>
<td>18,000 RUB</td>
<td>25,000 RUB</td>
</tr>
<tr>
<td>Local transport</td>
<td>1,500 RUB</td>
<td>3,000 RUB</td>
<td>5,000 RUB</td>
</tr>
<tr>
<td><strong>Total for 7 days</strong></td>
<td class="highlight"><strong>37,000 RUB</strong></td>
<td><strong>58,000 RUB</strong></td>
<td><strong>94,000 RUB</strong></td>
</tr>
</tbody>
</table>''',
'''<table class="price-table">
<thead>
<tr>
<th>ხარჯი</th>
<th>ეკონომ</th>
<th>საშუალო</th>
<th>კომფორტი</th>
</tr>
</thead>
<tbody>
<tr>
<td>ორმხრივი ავიაბილეთები</td>
<td>15,000 ₽</td>
<td>20,000 ₽</td>
<td>30,000 ₽</td>
</tr>
<tr>
<td>საცხოვრებელი (7 ღამე)</td>
<td class="highlight">5,500 ₽ (ჰოსტელი/Airbnb)</td>
<td>12,000 ₽</td>
<td>25,000 ₽</td>
</tr>
<tr>
<td>კვება</td>
<td>3,000 ₽</td>
<td>5,000 ₽</td>
<td>9,000 ₽</td>
</tr>
<tr>
<td>ტურები გიდთან (3 ექსკურსია)</td>
<td class="highlight">12,000 ₽-დან</td>
<td>18,000 ₽</td>
<td>25,000 ₽</td>
</tr>
<tr>
<td>ადგილობრივი ტრანსპორტი</td>
<td>1,500 ₽</td>
<td>3,000 ₽</td>
<td>5,000 ₽</td>
</tr>
<tr>
<td><strong>ჯამი 7 დღეზე</strong></td>
<td class="highlight"><strong>37,000 ₽</strong></td>
<td><strong>58,000 ₽</strong></td>
<td><strong>94,000 ₽</strong></td>
</tr>
</tbody>
</table>''')
add('A 7-day package tour through a Russian travel agency costs 65,000–95,000 RUB per person and typically includes a 3-star hotel and a group city tour. A self-planned trip with a private tour costs 25–35% less with far better quality experiences.',
    '7-დღიანი პაკეტ-ტური რუსული ტურ-სააგენტოს გავლით ჯდება 65,000–95,000 ₽ ერთ ადამიანზე და ჩვეულებრივ მოიცავს 3-ვარსკვლავიან სასტუმროსა და ჯგუფურ საქალაქო ტურს. დამოუკიდებელი მოგზაურობა კერძო ტურით 25–35%-ით იაფია და ბევრად ხარისხიან შთაბეჭდილებებს გაძლევთ.')

# --- ITINERARIES ---
add('<h2 class="section-title">Georgia Itineraries from Moscow: 5, 7 and 10 Days</h2>',
    '<h2 class="section-title">მარშრუტები საქართველოში მოსკოვიდან: 5, 7 და 10 დღე</h2>')
add('Ready-made trip plans with specific tours included. All itineraries are tried and tested by guide Timur.',
    'მზა მოგზაურობის გეგმები კონკრეტული ტურებით. ყველა მარშრუტი გამოცდილია გიდ თიმურის მიერ.')
add('<h3>5-Day Itinerary</h3>', '<h3>5-დღიანი მარშრუტი</h3>')
add('<h3>7-Day Itinerary</h3>', '<h3>7-დღიანი მარშრუტი</h3>')
add('<h3>10-Day Itinerary</h3>', '<h3>10-დღიანი მარშრუტი</h3>')
add('''<p><strong>Day 1:</strong> Arrival, check-in, stroll through Old Tbilisi<br/>
<strong>Day 2:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">Mtskheta</a> — Jvari, Svetitskhoveli (₾98)<br/>
<strong>Day 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">Kazbegi</a> — mountains, Gergeti Trinity Church (₾175)<br/>
<strong>Day 4:</strong> Night Tbilisi, sulfur baths, Narikala<br/>
<strong>Day 5:</strong> Market, souvenirs, departure</p>''',
'''<p><strong>დღე 1:</strong> ჩამოსვლა, დასახლება, სეირნობა ძველ თბილისში<br/>
<strong>დღე 2:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">მცხეთა</a> — ჯვარი, სვეტიცხოველი (₾98)<br/>
<strong>დღე 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">ყაზბეგი</a> — მთები, გერგეტის სამების ეკლესია (₾175)<br/>
<strong>დღე 4:</strong> ღამის თბილისი, გოგირდის აბანოები, ნარიყალა<br/>
<strong>დღე 5:</strong> ბაზარი, სუვენირები, გამგზავრება</p>''')
add('''<p><strong>Day 1:</strong> Arrival, first impressions of Tbilisi<br/>
<strong>Day 2:</strong> <a href="/en/ekskursiya/ekskursiya-stary-tbilisi/" style="color:#1A3D2E">Old Tbilisi</a> — deep dive (₾100)<br/>
<strong>Day 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">Kazbegi</a> (₾175)<br/>
<strong>Day 4:</strong> <a href="/en/ekskursiya/ekskursiya-kakheti-iz-tbilisi/" style="color:#1A3D2E">Kakheti</a> — wine, Sighnaghi (₾170)<br/>
<strong>Day 5:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">Mtskheta</a> + Borjomi (₾98–178)<br/>
<strong>Day 6:</strong> Night Tbilisi, dinner with a Georgian family<br/>
<strong>Day 7:</strong> Market, departure</p>''',
'''<p><strong>დღე 1:</strong> ჩამოსვლა, თბილისის პირველი შთაბეჭდილება<br/>
<strong>დღე 2:</strong> <a href="/en/ekskursiya/ekskursiya-stary-tbilisi/" style="color:#1A3D2E">ძველი თბილისი</a> — ღრმა ჩაძირვა (₾100)<br/>
<strong>დღე 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">ყაზბეგი</a> (₾175)<br/>
<strong>დღე 4:</strong> <a href="/en/ekskursiya/ekskursiya-kakheti-iz-tbilisi/" style="color:#1A3D2E">კახეთი</a> — ღვინო, სიღნაღი (₾170)<br/>
<strong>დღე 5:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">მცხეთა</a> + ბორჯომი (₾98–178)<br/>
<strong>დღე 6:</strong> ღამის თბილისი, ვახშამი ქართულ ოჯახთან ერთად<br/>
<strong>დღე 7:</strong> ბაზარი, გამგზავრება</p>''')
add('''<p><strong>Days 1–2:</strong> Tbilisi — Old Town, Narikala, evening walk<br/>
<strong>Day 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">Kazbegi</a> (₾175)<br/>
<strong>Day 4:</strong> <a href="/en/ekskursiya/ekskursiya-kakheti-iz-tbilisi/" style="color:#1A3D2E">Kakheti</a> (₾170)<br/>
<strong>Day 5:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">Mtskheta</a> (₾98)<br/>
<strong>Day 6:</strong> <a href="/en/ekskursiya/tur-kutaisi-iz-tbilisi/" style="color:#1A3D2E">Kutaisi</a> — Prometheus Cave (₾183)<br/>
<strong>Day 7:</strong> <a href="/en/ekskursiya/tur-batumi-iz-tbilisi/" style="color:#1A3D2E">Batumi</a> — Black Sea (₾250)<br/>
<strong>Day 8:</strong> <a href="/en/ekskursiya/ekskursiya-borjomi-iz-tbilisi/" style="color:#1A3D2E">Borjomi</a> — national park (₾178)<br/>
<strong>Days 9–10:</strong> Tbilisi — free time, departure</p>''',
'''<p><strong>დღეები 1–2:</strong> თბილისი — ძველი ქალაქი, ნარიყალა, საღამოს სეირნობა<br/>
<strong>დღე 3:</strong> <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/" style="color:#1A3D2E">ყაზბეგი</a> (₾175)<br/>
<strong>დღე 4:</strong> <a href="/en/ekskursiya/ekskursiya-kakheti-iz-tbilisi/" style="color:#1A3D2E">კახეთი</a> (₾170)<br/>
<strong>დღე 5:</strong> <a href="/en/ekskursiya/ekskursiya-mtskheta-iz-tbilisi/" style="color:#1A3D2E">მცხეთა</a> (₾98)<br/>
<strong>დღე 6:</strong> <a href="/en/ekskursiya/tur-kutaisi-iz-tbilisi/" style="color:#1A3D2E">ქუთაისი</a> — პრომეთეს მღვიმე (₾183)<br/>
<strong>დღე 7:</strong> <a href="/en/ekskursiya/tur-batumi-iz-tbilisi/" style="color:#1A3D2E">ბათუმი</a> — შავი ზღვა (₾250)<br/>
<strong>დღე 8:</strong> <a href="/en/ekskursiya/ekskursiya-borjomi-iz-tbilisi/" style="color:#1A3D2E">ბორჯომი</a> — ეროვნული პარკი (₾178)<br/>
<strong>დღეები 9–10:</strong> თბილისი — თავისუფალი დრო, გამგზავრება</p>''')

# --- TOURS GRID ---
add('<h2 class="section-title">Tours in Tbilisi — What to Book from Moscow</h2>',
    '<h2 class="section-title">ტურები თბილისში — რა დაჯავშნოთ მოსკოვიდან</h2>')
add('6 essential routes with guide Timur. All tours in English, groups up to 7 people.',
    '6 მთავარი მარშრუტი გიდ თიმურთან. ყველა ტური ინგლისურად, ჯგუფები 7 ადამიანამდე.')
add('<div class="tour-badge">Best Seller</div>', '<div class="tour-badge">ბესტსელერი</div>')
add('<div class="tour-badge">Wine</div>', '<div class="tour-badge">ღვინო</div>')
add('<div class="tour-badge">Old Town</div>', '<div class="tour-badge">ძველი ქალაქი</div>')
add('<div class="tour-badge">Nature</div>', '<div class="tour-badge">ბუნება</div>')
add('<div class="tour-badge">Evening</div>', '<div class="tour-badge">საღამო</div>')
add('<h3>Kazbegi from Tbilisi</h3>', '<h3>ყაზბეგი თბილისიდან</h3>')
add('<h3>Kakheti Wine Tour</h3>', '<h3>კახეთის ღვინის ტური</h3>')
add('<h3>Mtskheta — Ancient Capital</h3>', '<h3>მცხეთა — უძველესი დედაქალაქი</h3>')
add('<h3>Old Tbilisi Walking Tour</h3>', '<h3>ძველი თბილისის ფეხით ტური</h3>')
add('<h3>Kutaisi Day Trip</h3>', '<h3>ქუთაისი ერთ დღეში</h3>')
add('<h3>Night Tbilisi Tour</h3>', '<h3>ღამის თბილისის ტური</h3>')
add('Gergeti Trinity Church against Mt. Kazbek, Georgian Military Highway, Ananuri Fortress. The most popular day trip — the Caucasus mountains in one route.',
    'გერგეტის სამების ეკლესია მყინვარწვერის ფონზე, საქართველოს სამხედრო გზა, ანანურის ციხე. ყველაზე პოპულარული ერთდღიანი ტური — კავკასიის მთები ერთ მარშრუტში.')
add('Sighnaghi, Bodbe Monastery, kvevri wine tasting. Alazani Valley vineyards and a real marani cellar — perfect for wine lovers and history buffs.',
    'სიღნაღი, ბოდბის მონასტერი, ქვევრის ღვინის დეგუსტაცია. ალაზნის ველის ვენახები და ნამდვილი მარანი — იდეალურია ღვინისა და ისტორიის მოყვარულთათვის.')
add('Jvari Monastery, Svetitskhoveli Cathedral, confluence of Aragvi and Mtkvari rivers. Georgia\'s spiritual heart, 20 minutes from Tbilisi.',
    'ჯვრის მონასტერი, სვეტიცხოვლის საკათედრო ტაძარი, არაგვისა და მტკვრის შესართავი. საქართველოს სულიერი გული, თბილისიდან 20 წუთში.')
add('Narikala Fortress, Metekhi Church, sulfur baths, Sioni Cathedral, colorful Abanotubani balconies. The classic route through Tbilisi\'s historic centre.',
    'ნარიყალას ციხე, მეტეხის ეკლესია, გოგირდის აბანოები, სიონის ტაძარი, ფერადი აბანოთუბნის აივნები. კლასიკური მარშრუტი თბილისის ისტორიულ ცენტრში.')
add('Prometheus Cave, Martvili Canyon, Gelati Monastery (UNESCO). Western Georgia in one day — for travellers who want to see it all.',
    'პრომეთეს მღვიმე, მარტვილის კანიონი, გელათის მონასტერი (UNESCO). დასავლეთ საქართველო ერთ დღეში — მათთვის, ვისაც ყველაფრის ნახვა სურს.')
add('Narikala lit up at night, Peace Bridge, Kura embankment in golden light. Tbilisi after dark is a completely different city — the best photo tour.',
    'ღამით განათებული ნარიყალა, მშვიდობის ხიდი, მტკვრის სანაპირო ოქროსფერ შუქში. ღამის თბილისი სულ სხვა ქალაქია — საუკეთესო ფოტო-ტური.')
add('<span>⏲ 10–12 hours</span>', '<span>⏲ 10–12 საათი</span>', 2)
add('<span>🚗 Transfer included</span>', '<span>🚗 ტრანსფერი შედის</span>', 2)
add('<span>🍷 Tasting included</span>', '<span>🍷 დეგუსტაცია შედის</span>')
add('<span>⏲ 3–4 hours</span>', '<span>⏲ 3–4 საათი</span>', 2)
add('<span>🚶 Walking tour</span>', '<span>🚶 ფეხით ტური</span>')
add('<span>⏲ 12–13 hours</span>', '<span>⏲ 12–13 საათი</span>')
add('<span>🚗 From Tbilisi</span>', '<span>🚗 თბილისიდან</span>')
add('<span>⏲ 2–3 hours</span>', '<span>⏲ 2–3 საათი</span>')
add('<span>🌙 Evening</span>', '<span>🌙 საღამო</span>')
add('<span>/person</span>', '<span>/ადამიანზე</span>', 6)
add('<span class="book-btn">Details</span>', '<span class="book-btn">დეტალები</span>', 6)

# --- COMPARISON ---
add('<h2 class="section-title">Package Tour vs Self-Planned + Private Tour</h2>',
    '<h2 class="section-title">პაკეტ-ტური vs დამოუკიდებელი + კერძო ტური</h2>')
add('An honest comparison of both formats for a trip to Georgia from Moscow.',
    'ორივე ფორმატის გულახდილი შედარება საქართველოში მოსკოვიდან მოგზაურობისთვის.')
add('''<table class="price-table">
<thead>
<tr>
<th>Parameter</th>
<th>Package Tour</th>
<th>Self-planned + Private Tour</th>
</tr>
</thead>
<tbody>
<tr>
<td>Cost for 7 days</td>
<td>65,000–95,000 RUB</td>
<td class="highlight">37,000–60,000 RUB</td>
</tr>
<tr>
<td>Itinerary flexibility</td>
<td class="cross">✗ Fixed schedule</td>
<td class="check">✓ Full freedom</td>
</tr>
<tr>
<td>Tour language</td>
<td class="cross">✗ Often mixed groups</td>
<td class="check">✓ English only</td>
</tr>
<tr>
<td>Group size</td>
<td>20–40 people</td>
<td class="highlight">up to 7 people</td>
</tr>
<tr>
<td>Off-the-beaten-path sites</td>
<td class="cross">✗ Tourist circuit only</td>
<td class="check">✓ Custom routes</td>
</tr>
<tr>
<td>Accommodation quality</td>
<td>3-star hotel (included)</td>
<td class="highlight">Your choice (apt/hotel/hostel)</td>
</tr>
<tr>
<td>Cancellation</td>
<td class="cross">✗ Fees up to 100%</td>
<td class="check">✓ Free up to 24h before</td>
</tr>
</tbody>
</table>''',
'''<table class="price-table">
<thead>
<tr>
<th>პარამეტრი</th>
<th>პაკეტ-ტური</th>
<th>დამოუკიდებელი + კერძო ტური</th>
</tr>
</thead>
<tbody>
<tr>
<td>ღირებულება 7 დღეზე</td>
<td>65,000–95,000 ₽</td>
<td class="highlight">37,000–60,000 ₽</td>
</tr>
<tr>
<td>მარშრუტის მოქნილობა</td>
<td class="cross">✗ ფიქსირებული გრაფიკი</td>
<td class="check">✓ სრული თავისუფლება</td>
</tr>
<tr>
<td>ტურის ენა</td>
<td class="cross">✗ ხშირად შერეული ჯგუფები</td>
<td class="check">✓ მხოლოდ ინგლისური</td>
</tr>
<tr>
<td>ჯგუფის ზომა</td>
<td>20–40 ადამიანი</td>
<td class="highlight">7 ადამიანამდე</td>
</tr>
<tr>
<td>ნაკლებად ცნობილი ადგილები</td>
<td class="cross">✗ მხოლოდ ტურისტული მარშრუტი</td>
<td class="check">✓ ინდივიდუალური მარშრუტები</td>
</tr>
<tr>
<td>საცხოვრებლის ხარისხი</td>
<td>3-ვარსკვლავიანი სასტუმრო (შედის)</td>
<td class="highlight">თქვენი არჩევანი (ბინა/სასტუმრო/ჰოსტელი)</td>
</tr>
<tr>
<td>გაუქმება</td>
<td class="cross">✗ ჯარიმა 100%-მდე</td>
<td class="check">✓ უფასო 24 საათით ადრე</td>
</tr>
</tbody>
</table>''')

# --- PRACTICAL ---
add('<h2 class="section-title">Practical Tips for Travellers from Moscow</h2>',
    '<h2 class="section-title">პრაქტიკული რჩევები მოსკოვიდან მოგზაურთათვის</h2>')
add('What you need to know before you go — visas, money, SIM cards, transport.',
    'რა უნდა იცოდეთ გამგზავრებამდე — ვიზა, ფული, SIM-ბარათები, ტრანსპორტი.')
add('<h3>No Visa Required</h3>', '<h3>ვიზა არ სჭირდება</h3>')
add('Russian citizens can stay in Georgia up to 365 days visa-free. Only a passport (foreign or internal Russian) is needed. Border control typically takes 5–15 minutes.',
    'რუსეთის მოქალაქეებს შეუძლიათ საქართველოში დარჩნენ 365 დღემდე უვიზოდ. საჭიროა მხოლოდ პასპორტი (საზღვარგარეთის ან შიდა რუსული). სასაზღვრო კონტროლი ჩვეულებრივ 5–15 წუთს გრძელდება.')
add('<h3>Money &amp; Exchange</h3>', '<h3>ფული და გადაცვლა</h3>')
add("Currency is the lari (₾). 1 GEL ≈ 37 RUB (2026). Exchange rubles in Tbilisi: best rates on Rustaveli Ave. Mir cards don't work. Visa/Mastercard accepted everywhere. ATMs: TBC Bank, Bank of Georgia.",
    'ვალუტა ლარია (₾). 1 ლარი ≈ 37 ₽ (2026). რუბლი გადაცვალეთ თბილისში: საუკეთესო კურსი რუსთაველის გამზირზე. „მირ“ ბარათები არ მუშაობს. Visa/Mastercard ყველგან მიიღება. ბანკომატები: TBC Bank, Bank of Georgia.')
add('<h3>SIM Card</h3>', '<h3>SIM-ბარათი</h3>')
add('Buy at Tbilisi airport. Operators: Magti, Geocell, Beeline Georgia. 5 GB data plan costs ₾5–10 (≈185–370 RUB/month). Excellent 4G coverage across Georgia.',
    'იყიდეთ თბილისის აეროპორტში. ოპერატორები: Magti, Geocell, Beeline Georgia. 5 GB ინტერნეტ-პაკეტი ჯდება ₾5–10 (≈185–370 ₽/თვე). შესანიშნავი 4G დაფარვა მთელ საქართველოში.')
add('<h3>Transport</h3>', '<h3>ტრანსპორტი</h3>')
add('Within Tbilisi — Bolt taxi (cheaper than Yandex.Go). To other cities — marshrutkas from Didube bus station. Guided tours include transfer in a comfortable vehicle.',
    'თბილისის შიგნით — Bolt ტაქსი (Yandex.Go-ზე იაფი). სხვა ქალაქებში — მარშრუტკები დიდუბის ავტოსადგურიდან. ტურები გიდთან მოიცავს ტრანსფერს კომფორტულ ავტომობილში.')
add('<a href="/en/tours-in-georgia/" style="color:#16A34A;font-weight:700">All Tours in Georgia 2026</a> — itineraries, prices and how to plan your trip',
    '<a href="/en/tours-in-georgia/" style="color:#16A34A;font-weight:700">ყველა ტური საქართველოში 2026</a> — მარშრუტები, ფასები და როგორ დაგეგმოთ მოგზაურობა')

# --- CTA / WHY / TIP ---
add('<div class="cta-label">Planning a trip from Moscow?</div>',
    '<div class="cta-label">გეგმავთ მოგზაურობას მოსკოვიდან?</div>')
add('<h2 class="cta-title">Book your tours early — the best dates fill up fast</h2>',
    '<h2 class="cta-title">დაჯავშნეთ ტურები წინასწარ — საუკეთესო თარიღები სწრაფად ივსება</h2>')
add('<p class="cta-sub">Message guide Timur — reply within 15 minutes. Free cancellation up to 24h. Groups up to 7 people.</p>',
    '<p class="cta-sub">მოგვწერეთ გიდ თიმურს — პასუხი 15 წუთში. უფასო გაუქმება 24 საათამდე. ჯგუფები 7 ადამიანამდე.</p>')
add('WhatsApp — reply in 15 min', 'WhatsApp — პასუხი 15 წუთში')
add('<h2 style="font-family:\'Lora\',serif;font-size:22px;color:#1A3D2E;margin:0 0 12px;font-weight:600">Why Choose Sakhva Travel</h2>',
    '<h2 style="font-family:\'Lora\',serif;font-size:22px;color:#1A3D2E;margin:0 0 12px;font-weight:600">რატომ Sakhva Travel</h2>')
add("I'm not a travel agency or aggregator. I'm Timur, a private tour who has lived in Tbilisi for over 10 years. Every route is designed by me personally, and I know every location from the inside. No 40-person buses, no rushing. Mini-groups up to 7 or private tours. Flexible itinerary: we stop where you want, eat where it's actually good (not where I get commission), and photograph where it's beautiful. 200+ reviews on Google Maps — check for yourself.",
    'მე არ ვარ ტურ-სააგენტო ან აგრეგატორი. მე ვარ თიმური, კერძო გიდი, რომელიც თბილისში 10 წელზე მეტია ცხოვრობს. ყველა მარშრუტი პირადად ჩემ მიერაა შედგენილი და ყველა ადგილს შიგნიდან ვიცნობ. არანაირი 40-ადგილიანი ავტობუსი, არანაირი ჩქარობა. მინი-ჯგუფები 7 ადამიანამდე ან კერძო ტურები. მოქნილი მარშრუტი: ვჩერდებით იქ, სადაც გსურთ, ვჭამთ იქ, სადაც ნამდვილად გემრიელია (და არა იქ, სადაც მე მრგებს საკომისიო), და ვიღებთ იქ, სადაც ლამაზია. 200+ შეფასება Google Maps-ზე — თავად შეამოწმეთ.')
add('<h2 style="font-family:\'Lora\',serif;font-size:20px;color:#92400E;margin:0 0 10px;font-weight:600">Timur\'s Tip</h2>',
    '<h2 style="font-family:\'Lora\',serif;font-size:20px;color:#92400E;margin:0 0 10px;font-weight:600">თიმურის რჩევა</h2>')
add('From Moscow you fly via Istanbul, Dubai or Yerevan — I\'ll help you plan the itinerary so you don\'t lose a single day on layovers. Arrive in the morning, head straight on tour. Best option for 5–7 days: Tbilisi + Kazbegi + Kakheti + one free day.',
    'მოსკოვიდან სტამბოლის, დუბაისა ან ერევნის გავლით ფრენთ — დაგეხმარებით მარშრუტის დაგეგმვაში ისე, რომ გადაჯდომებზე ერთი დღეც არ დაკარგოთ. დილით ჩამოხვალთ და პირდაპირ ტურზე მიდიხართ. საუკეთესო ვარიანტი 5–7 დღეზე: თბილისი + ყაზბეგი + კახეთი + ერთი თავისუფალი დღე.')

# --- PRODUCT SCHEMA + REVIEWS ---
add('"name":"Tours to Georgia from Moscow 2026 — How to Plan Your Trip"',
    '"name":"ტურები საქართველოში მოსკოვიდან 2026 — როგორ დაგეგმოთ მოგზაურობა"')
add('Wonderful trip to Kakheti! The wine was amazing — everyone should visit Georgian vineyards at least once.',
    'შესანიშნავი მოგზაურობა კახეთში! ღვინო საოცარი იყო — ყველამ ერთხელ მაინც უნდა ეწვიოს ქართულ ვენახებს.')
# следующие 3 совпадают со schema reviewBody + видимой цитатой (count 2)
add('Booked a private tour for four. Timur is a true professional: knows the history and tells it in a fascinating way.',
    'დავჯავშნეთ კერძო ტური ოთხისთვის. თიმური ნამდვილი პროფესიონალია: იცის ისტორია და მომხიბლავად ჰყვება.', 2)
add('Everything went perfectly, highly recommend!',
    'ყველაფერი იდეალურად ჩაიარა, ნამდვილად გირჩევთ!', 2)
add('We went to Kazbegi — Timur convinced us the special atmosphere was worth it. Snow by the church, silence. The most romantic day of the trip.',
    'ყაზბეგში წავედით — თიმურმა დაგვარწმუნა, რომ განსაკუთრებული ატმოსფერო ღირდა. თოვლი ეკლესიასთან, სიჩუმე. მოგზაურობის ყველაზე რომანტიული დღე.', 2)
add('Wonderful excursion, thank you so much! Everything was top-notch.',
    'შესანიშნავი ექსკურსია, დიდი მადლობა! ყველაფერი უმაღლეს დონეზე იყო.')
add('You have no idea how much I enjoyed it. Nice tiredness, nice people, delicious food. Thank you very much.',
    'წარმოდგენა არ გაქვთ, როგორ მომეწონა. სასიამოვნო დაღლილობა, სასიამოვნო ხალხი, გემრიელი საჭმელი. დიდი მადლობა.')
add('"name":"Amovei"', '"name":"ამოვეი"')
add('"name":"Sergey"', '"name":"სერგეი"')
add('"name":"Tigran M."', '"name":"ტიგრან მ."')
add('"name":"Vladislav S."', '"name":"ვლადისლავ ს."')
add('"name":"Elena"', '"name":"ელენა"')
add('"name":"Mikhail D"', '"name":"მიხაილ დ."')
add('aria-label="Traveller reviews"', 'aria-label="მოგზაურთა შეფასებები"')
add('>Traveller reviews</h2>', '>მოგზაურთა შეფასებები</h2>')
add('Real traveller reviews on Google Maps · rated 4.9 out of 5',
    'მოგზაურთა ნამდვილი შეფასებები Google Maps-ზე · შეფასდა 4.9/5-დან')
add('<strong style="color:#111827">Sergey</strong> · September 2025',
    '<strong style="color:#111827">სერგეი</strong> · სექტემბერი 2025')
add('<strong style="color:#111827">Vladislav S.</strong> · May 2026',
    '<strong style="color:#111827">ვლადისლავ ს.</strong> · მაისი 2026')
add('<strong style="color:#111827">Elena</strong> · March 2026',
    '<strong style="color:#111827">ელენა</strong> · მარტი 2026')
add('Timur Sakhvadze · licensed guide, license №8247109128 · ',
    'თიმურ სახვაძე · ლიცენზირებული გიდი, ლიცენზია №8247109128 · ')
add('all reviews on Google ↗', 'ყველა შეფასება Google-ზე ↗')

# --- LEAD MAGNET ---
add('Guide: 15 Places in Tbilisi + 5% discount',
    'გზამკვლევი: თბილისის 15 ადგილი + 5% ფასდაკლება')
add('placeholder="Email"', 'placeholder="ელფოსტა"')
add('aria-label="Email for subscription"', 'aria-label="ელფოსტა გამოწერისთვის"')
add('type="submit">Get it</button>', 'type="submit">მიღება</button>')
add('Sent — check your inbox', 'გაიგზავნა — შეამოწმეთ ფოსტა')

# --- VISIBLE FAQ ---
add('<h2>Frequently Asked Questions about Tours to Georgia from Moscow</h2>',
    '<h2>ხშირად დასმული კითხვები ტურებზე საქართველოში მოსკოვიდან</h2>')
def faq(q_en, q_ka, a_en, a_ka):
    add(f'<div class="faq-q" onclick="this.parentElement.classList.toggle(\'open\')">{q_en}</div>',
        f'<div class="faq-q" onclick="this.parentElement.classList.toggle(\'open\')">{q_ka}</div>')
    add(f'<div class="faq-a">{a_en}</div>', f'<div class="faq-a">{a_ka}</div>')
faq('How to get to Tbilisi from Moscow in 2026?',
    'როგორ მოვხვდე თბილისში მოსკოვიდან 2026 წელს?',
    'The fastest way is a direct flight from Vnukovo with Georgian Airways, Red Wings or Azimuth (from 13,600 RUB round-trip, ~2h 50m). Connecting options: via Istanbul on Turkish Airlines (from 15,000 RUB, ~5–6 hours total), via Dubai (flydubai/Emirates, from 18,000 RUB), via Yerevan + minibus (from 16,000 RUB), or bus via Upper Lars from 3,500 RUB.',
    'ყველაზე სწრაფი გზაა პირდაპირი ფრენა ვნუკოვოდან Georgian Airways-ით, Red Wings-ით ან Azimuth-ით (ორმხრივი 13,600 ₽-დან, ~2სთ 50წთ). გადაჯდომით: სტამბოლის გავლით Turkish Airlines-ით (15,000 ₽-დან, ჯამში ~5–6 საათი), დუბაის გავლით (flydubai/Emirates, 18,000 ₽-დან), ერევნის + მიკროავტობუსის გავლით (16,000 ₽-დან) ან ავტობუსით ზემო ლარსის გავლით 3,500 ₽-დან.')
faq('Do Russian citizens need a visa for Georgia?',
    'სჭირდებათ რუსეთის მოქალაქეებს ვიზა საქართველოსთვის?',
    'No. Russian citizens can stay in Georgia visa-free for up to 365 days. A foreign passport or internal Russian passport is sufficient. Border control normally takes 5–15 minutes.',
    'არა. რუსეთის მოქალაქეებს შეუძლიათ საქართველოში დარჩნენ უვიზოდ 365 დღემდე. საკმარისია საზღვარგარეთის ან შიდა რუსული პასპორტი. სასაზღვრო კონტროლი ჩვეულებრივ 5–15 წუთს გრძელდება.')
faq('How much does a 7-day trip to Georgia from Moscow cost?',
    'რამდენი ჯდება 7-დღიანი მოგზაურობა საქართველოში მოსკოვიდან?',
    'A self-planned 7-day trip costs from 37,000 RUB: flights ~15,000 RUB, accommodation ~5,500 RUB, food ~3,000 RUB, guided tours from ~12,000 RUB. A package tour through an agency costs 65,000–95,000 RUB with lower-quality excursions.',
    'დამოუკიდებლად დაგეგმილი 7-დღიანი მოგზაურობა ჯდება 37,000 ₽-დან: ავიაბილეთები ~15,000 ₽, საცხოვრებელი ~5,500 ₽, კვება ~3,000 ₽, ტურები გიდთან ~12,000 ₽-დან. პაკეტ-ტური სააგენტოს გავლით ჯდება 65,000–95,000 ₽ უფრო დაბალი ხარისხის ექსკურსიებით.')
faq('Do Mir cards work in Georgia?',
    'მუშაობს „მირ“ ბარათები საქართველოში?',
    'No, Mir cards are not accepted in Georgia. Bring cash rubles/dollars and exchange to lari in Tbilisi (best rates on Rustaveli and at Dezerter Market). Visa and Mastercard from foreign banks work everywhere. Withdraw lari from TBC Bank and Bank of Georgia ATMs without issues.',
    'არა, „მირ“ ბარათები საქართველოში არ მიიღება. წაიღეთ ნაღდი რუბლი/დოლარი და გადაცვალეთ ლარში თბილისში (საუკეთესო კურსი რუსთაველზე და დეზერტირების ბაზარში). უცხოური ბანკების Visa და Mastercard ყველგან მუშაობს. ლარი უპრობლემოდ გამოიტანეთ TBC Bank-ისა და Bank of Georgia-ის ბანკომატებიდან.')
faq('When is the best time to visit Georgia from Moscow?',
    'როდის არის საუკეთესო დრო საქართველოში მოსკოვიდან ჩამოსასვლელად?',
    'Best times are spring (April–May) and autumn (September–October). May brings cherry blossoms; September–October is wine harvest season in Kakheti. Summer (June–August) is hot (+35–38°C in Tbilisi), winter is mild in the city (+5–10°C) and ski season at Gudauri.',
    'საუკეთესო დროა გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტემბერი–ოქტომბერი). მაისში ალუბლის ყვავილობაა; სექტემბერი–ოქტომბერი კახეთში რთველის სეზონია. ზაფხული (ივნისი–აგვისტო) ცხელია (+35–38°C თბილისში), ზამთარი ქალაქში რბილია (+5–10°C) და გუდაურში სათხილამურო სეზონია.')
faq('Which tours are must-do for visitors from Moscow?',
    'რომელი ტურებია აუცილებელი მოსკოვიდან ჩამოსული სტუმრებისთვის?',
    'Top 3 essential tours: 1) Kazbegi — mountains, Gergeti Trinity Church facing Mt. Kazbek (from ₾175/person); 2) Kakheti — wine, Sighnaghi, kvevri tasting (from ₾170/person); 3) Mtskheta — UNESCO, Svetitskhoveli (from ₾98/person). In the city: Old Tbilisi walking tour (from ₾100/person).',
    'ტოპ-3 აუცილებელი ტური: 1) ყაზბეგი — მთები, გერგეტის სამების ეკლესია მყინვარწვერის ფონზე (₾175-დან ერთ ადამიანზე); 2) კახეთი — ღვინო, სიღნაღი, ქვევრის დეგუსტაცია (₾170-დან ერთ ადამიანზე); 3) მცხეთა — UNESCO, სვეტიცხოველი (₾98-დან ერთ ადამიანზე). ქალაქში: ძველი თბილისის ფეხით ტური (₾100-დან ერთ ადამიანზე).')
faq('In what language does guide Timur work?',
    'რა ენაზე მუშაობს გიდი თიმური?',
    'Guide Timur is fluent in both English and Russian, and has lived in Tbilisi since 2023. All tours are conducted in your language of choice. He explains Georgian history and culture in a way that truly resonates.',
    'გიდი თიმური თავისუფლად ფლობს როგორც ინგლისურს, ისე რუსულს, და თბილისში 2023 წლიდან ცხოვრობს. ყველა ტური თქვენ მიერ არჩეულ ენაზე ტარდება. ის ქართულ ისტორიასა და კულტურას ისე ხსნის, რომ ნამდვილად გულში ჩაგრჩებათ.')
faq('Can I cancel a tour if my plans change?',
    'შემიძლია ტურის გაუქმება, თუ ჩემი გეგმები შეიცვალა?',
    'Yes. All tours can be cancelled free of charge up to 24 hours before the start. Cancellations within 24 hours incur a 50% fee. Rescheduling is always possible — just message via WhatsApp or Telegram.',
    'დიახ. ყველა ტური შეიძლება უფასოდ გაუქმდეს დაწყებამდე 24 საათით ადრე. 24 საათში გაუქმებისას იჭირება 50%. თარიღის გადატანა ყოველთვის შესაძლებელია — უბრალოდ მოგვწერეთ WhatsApp-ზე ან Telegram-ზე.')

# --- INTERNAL CITY LINKS ---
add('Tours to Georgia from other cities:', 'ტურები საქართველოში სხვა ქალაქებიდან:')
_cities = [
    ('Chelyabinsk','ჩელიაბინსკიდან'), ('Kazakhstan','ყაზახეთიდან'), ('Kazan','ყაზანიდან'),
    ('Kislovodsk','კისლოვოდსკიდან'), ('Krasnodar','კრასნოდარიდან'), ('Makhachkala','მახაჩკალადან'),
    ('Mineralnye Vody','მინერალნიე ვოდიდან'), ('Minsk','მინსკიდან'), ('Nalchik','ნალჩიკიდან'),
    ('Nizhny Novgorod','ნიჟნი ნოვგოროდიდან'), ('Novosibirsk','ნოვოსიბირსკიდან'), ('Perm','პერმიდან'),
    ('Pyatigorsk','პიატიგორსკიდან'), ('Rostov','როსტოვიდან'), ('Samara','სამარადან'),
    ('Saratov','სარატოვიდან'), ('Sochi','სოჭიდან'), ('St. Petersburg','სანკტ-პეტერბურგიდან'),
    ('Stavropol','სტავროპოლიდან'), ('Tashkent','ტაშკენტიდან'), ('Tyumen','ტიუმენიდან'),
    ('Ufa','უფადან'), ('Vladikavkaz','ვლადიკავკაზიდან'), ('Volgograd','ვოლგოგრადიდან'),
    ('Voronezh','ვორონეჟიდან'), ('Yekaterinburg','ეკატერინბურგიდან'), ('Yerevan','ერევნიდან'),
]
for en, ka in _cities:
    add(f'>from {en}</a>', f'>{ka}</a>')

# --- NAV / DRAWER / FOOTER (последними: блоки уже перевели дублирующиеся анкоры) ---
add('>Tours in Georgia</a>', '>ტურები საქართველოში</a>', 2)
add('>Excursions</a>', '>ექსკურსიები</a>', 2)
add('>About</a>', '>ჩვენ შესახებ</a>')          # nav (href /en/#guide)
add('>Reviews</a>', '>შეფასებები</a>')
add('>Blog</a>', '>ბლოგი</a>', 3)               # nav+drawer+footer
add('>Home</a>', '>მთავარი</a>', 2)             # drawer + breadcrumb
add('>Prices</a>', '>ფასები</a>')
add('>About Guide</a>', '>გიდის შესახებ</a>', 2) # drawer + footer
add('>Contacts</a>', '>კონტაქტი</a>', 3)         # nav + drawer + footer
add('>Book Now</a>', '>დაჯავშნე ახლავე</a>', 2)  # nav-btn + drawer d-btn
add('<h4>Tours</h4>', '<h4>ტურები</h4>')
add('<h4>Useful</h4>', '<h4>სასარგებლო</h4>')
add('>Kazbegi</a>', '>ყაზბეგი</a>')             # footer (маршруты уже переведены блоками)
add('>Kakheti</a>', '>კახეთი</a>')
add('>Kutaisi</a>', '>ქუთაისი</a>')
add('>Mtskheta</a>', '>მცხეთა</a>')
add('>Night Tbilisi</a>', '>ღამის თბილისი</a>')
add('>Russian</a>', '>რუსული</a>')
add('© 2026 Sakhva Travel. Tbilisi, Georgia', '© 2026 Sakhva Travel. თბილისი, საქართველო')
add('>Leave a Review ★</a>', '>დატოვე შეფასება ★</a>')
add('>Privacy</a>', '>კონფიდენციალურობა</a>')
add('>Terms</a>', '>პირობები</a>')
add('<p class="foot-desc">Private tours in Tbilisi and Georgia. Bespoke tours in English since 2023.</p>',
    '<p class="foot-desc">კერძო ტურები თბილისსა და საქართველოში. ინდივიდუალური ტურები ინგლისურად 2023 წლიდან.</p>')

# SECTIONS_MARKER

def run():
    html = open(FILE, encoding="utf-8").read()
    # Последовательно: проверяем счётчик и сразу заменяем — так footer-анкоры,
    # зависящие от предыдущих блочных замен, дают корректный счёт.
    errs = []
    work = html
    for i, (old, new, n) in enumerate(R):
        c = work.count(old)
        if c != n:
            errs.append(f"[{c}!={n}] #{i} {old[:70]!r}")
            continue
        work = work.replace(old, new)
    if errs:
        print("НЕСОВПАДЕНИЕ СЧЁТЧИКОВ — запись отменена:")
        print("\n".join(errs))
        sys.exit(1)
    open(FILE, "w", encoding="utf-8").write(work)
    print(f"OK: применено {len(R)} замен")

if __name__ == "__main__":
    run()
