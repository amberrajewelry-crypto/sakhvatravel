#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Универсальный батч перевода гео-лендинга: L-словарь + анкоры.
Использование: правим L под конкретный город, запускаем на его ge-файле."""
import json, sys
from pathlib import Path
TM = Path("scripts/ge_tm.json")
tm = json.loads(TM.read_text(encoding="utf-8"))

L = {
"Planning a tour to Georgia from Kazan in 2026 is entirely doable. With a connection through Istanbul, Dubai or Yerevan you reach Tbilisi in a single day of travel — and from there a whole country opens up: the Kazbegi mountains, kvevri wine in Kakheti, medieval Tbilisi and the sulfur baths. From there, a country awaits where in a single trip you can see the Kazbegi mountains, taste kvevri wine in Kakheti, stroll the medieval streets of Tbilisi and soak in the sulfur baths — all at a budget that will surprise even seasoned travellers. A self-planned trip with a private tour costs 25–35% less than a package tour from a travel agency, and delivers incomparably richer experiences.":
"საქართველოში ტურის დაგეგმვა ყაზანიდან 2026 წელს სავსებით შესაძლებელია. სტამბოლის, დუბაის ან ერევნის გავლით გადაჯდომით თბილისს ერთ დღეში აღწევთ — და იქიდან მთელი ქვეყანა იხსნება: ყაზბეგის მთები, ქვევრის ღვინო კახეთში, შუასაუკუნეების თბილისი და გოგირდის აბანოები. იქიდან იშლება ქვეყანა, სადაც ერთ მოგზაურობაში ნახავთ ყაზბეგის მთებს, დააგემოვნებთ ქვევრის ღვინოს კახეთში, გაივლით თბილისის შუასაუკუნეების ქუჩებში და დატკბებით გოგირდის აბანოებით — და ეს ყველაფერი ისეთ ბიუჯეტში, რომელიც გამოცდილ მოგზაურსაც კი გააკვირვებს. დამოუკიდებლად დაგეგმილი მოგზაურობა კერძო გიდით 25–35%-ით იაფია, ვიდრე პაკეტ-ტური ტურაგენტობიდან, და შეუდარებლად მდიდარ შთაბეჭდილებებს გჩუქნით.",
"Direct flights are back — Red Wings flies Kazan to Tbilisi in about 2h 40m (round-trip from 14,000 RUB). The most popular routes connect via Istanbul (Turkish Airlines), Dubai (flydubai/Emirates), Yerevan or Minsk, with roughly 6–11 hours of total travel depending on the layover. Booking a connecting ticket 1–2 months ahead gives the best fare.":
"პირდაპირი რეისები დაბრუნდა — Red Wings დაფრინავს ყაზანიდან თბილისში დაახლოებით 2 საათსა და 40 წუთში (ორმხრივი 14,000 RUB-დან). ყველაზე პოპულარული მარშრუტები გადის სტამბოლის (Turkish Airlines), დუბაის (flydubai/Emirates), ერევნის ან მინსკის გავლით, სულ დაახლოებით 6–11 საათი მგზავრობით გადაჯდომის მიხედვით. გადაჯდომითი ბილეთის დაჯავშნა 1–2 თვით ადრე საუკეთესო ფასს იძლევა.",
"A self-planned 7-day trip from Kazan covers connecting flights (via Istanbul or Dubai), accommodation from ₾50/night, food, and guided tours from ₾98/person. It usually works out cheaper and far more flexible than a package tour, which rarely includes quality private excursions.":
"დამოუკიდებლად დაგეგმილი 7-დღიანი მოგზაურობა ყაზანიდან მოიცავს გადაჯდომით ფრენებს (სტამბოლის ან დუბაის გავლით), საცხოვრებელს ₾50/ღამედან, საკვებს და ტურებს გიდთან ₾98-დან/ადამიანი. ჩვეულებრივ ეს უფრო იაფი და გაცილებით მოქნილია, ვიდრე პაკეტ-ტური, რომელიც იშვიათად მოიცავს ხარისხიან კერძო ექსკურსიებს.",
"Direct flights are back — Red Wings flies Kazan → Tbilisi in about 2h 40m (round-trip from 14,000 RUB). Connections also work: via Istanbul (Turkish Airlines, from 16,000 RUB, ~6–8h) or via Moscow with any onward route.":
"პირდაპირი რეისები დაბრუნდა — Red Wings დაფრინავს ყაზანი → თბილისი დაახლოებით 2 საათსა და 40 წუთში (ორმხრივი 14,000 RUB-დან). გადაჯდომებიც მუშაობს: სტამბოლის გავლით (Turkish Airlines, 16,000 RUB-დან, ~6–8 საათი) ან მოსკოვის გავლით ნებისმიერი შემდგომი მარშრუტით.",
"Tbilisi is very welcoming to Muslim visitors — halal restaurants are easy to find, especially in the Marjanishvili and Vake districts. Georgian wine tours can be skipped in favour of mineral water tasting in Borjomi.":
"თბილისი ძალიან მასპინძლობს მუსლიმ ვიზიტორებს — ჰალალ რესტორნები ადვილად მოიძებნება, განსაკუთრებით მარჯანიშვილისა და ვაკის უბნებში. ქართული ღვინის ტურები შეიძლება გამოტოვოთ ბორჯომში მინერალური წყლის დეგუსტაციის სასარგებლოდ.",
"Kazan and Tbilisi share a rich multicultural heritage. Visiting Georgia resonates deeply for Kazan residents who appreciate historic mosques, cathedrals, and vibrant street life coexisting side by side.":
"ყაზანსა და თბილისს აქვს მდიდარი მულტიკულტურული მემკვიდრეობა. საქართველოს მონახულება ღრმად ეხმიანება ყაზანელებს, რომლებიც აფასებენ ისტორიულ მეჩეთებს, ტაძრებსა და ცოცხალ ქუჩურ ცხოვრებას, რომლებიც გვერდიგვერდ თანაარსებობენ.",
"From Kazan the easiest connection is via Istanbul. I'll plan your arrival so you start the first tour the same afternoon. Don't miss Kazbegi — the mountains will blow your mind.":
"ყაზანიდან ყველაზე მარტივი გადაჯდომა სტამბოლის გავლითაა. ჩამოსვლას ისე დაგიგეგმავთ, რომ პირველი ტური იმავე შუადღეს დაიწყოთ. არ გამოტოვოთ ყაზბეგი — მთები გაგაოცებთ.",
"No. Russian citizens can stay in Georgia visa-free for up to 365 days. A foreign passport or internal Russian passport is sufficient. Border control normally takes 5–15 minutes.":
"არა. რუსეთის მოქალაქეებს შეუძლიათ საქართველოში უვიზოდ ყოფნა 365 დღემდე. საკმარისია საზღვარგარეთის ან შიდა რუსული პასპორტი. სასაზღვრო კონტროლი ჩვეულებრივ 5–15 წუთს იღებს.",
"KZN airport has direct routes to Istanbul via Turkish Airlines. The Moscow connection is also quick — under 2 hours — opening up all Moscow-based routes to Tbilisi.":
"KZN აეროპორტს აქვს პირდაპირი მარშრუტები სტამბოლში Turkish Airlines-ით. მოსკოვის გადაჯდომაც სწრაფია — 2 საათზე ნაკლები — რაც ხსნის ყველა მოსკოვურ მარშრუტს თბილისისკენ.",
"Kazan has cold winters and hot summers. Georgia's spring (April–May) and autumn (Sept–Oct) offer perfect mild weather — ideal for mountain hikes and city walks.":
"ყაზანს აქვს ცივი ზამთარი და ცხელი ზაფხული. საქართველოს გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტ–ოქტ) იდეალურ რბილ ამინდს გთავაზობთ — შესანიშნავია მთის ლაშქრობებისა და ქალაქის სეირნობისთვის.",
"A package tour from Kazan costs 65,000–95,000 RUB per person. A self-planned trip with a private tour costs 25–35% less with far better quality experiences.":
"პაკეტ-ტური ყაზანიდან ღირს 65,000–95,000 RUB ერთ ადამიანზე. დამოუკიდებლად დაგეგმილი მოგზაურობა კერძო გიდით 25–35%-ით იაფია, ბევრად უკეთესი ხარისხის შთაბეჭდილებებით.",
"Planning a trip to Georgia from Kazan? Flights/transport to Tbilisi, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.":
"გეგმავთ მოგზაურობას საქართველოში ყაზანიდან? ფრენები/ტრანსპორტი თბილისამდე, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან.",
"Flights from 16,000 RUB, accommodation from ₾50/night, private tours from ₾98. Itineraries for 5, 7 and 10 days — easy trip from Kazan.":
"ფრენები 16,000 RUB-დან, საცხოვრებელი ₾50/ღამედან, კერძო ტურები ₾98-დან. მარშრუტები 5, 7 და 10 დღეზე — მარტივი მოგზაურობა ყაზანიდან.",
"“Excellent guide. Showed and told us everything about sunny Georgia. Speaks great English and Russian.”":
"„შესანიშნავი გიდი. ყველაფერი გვაჩვენა და გვიამბო მზიან საქართველოზე. მშვენივრად ლაპარაკობს ინგლისურად და რუსულად.“",
"Costs vary by transport option. See the budget table above for a full breakdown from Kazan.":
"ხარჯები ტრანსპორტის ვარიანტის მიხედვით განსხვავდება. იხილეთ ბიუჯეტის ცხრილი ზემოთ სრული დაყოფისთვის ყაზანიდან.",
"Real cost breakdown for 7 days, one person. Prices for April–October 2026 from Kazan.":
"რეალური ხარჯების დაყოფა 7 დღეზე, ერთ ადამიანზე. ფასები აპრილი–ოქტომბერი 2026-ისთვის ყაზანიდან.",
"“Unforgettable tour! Thank you Timur and his team — absolutely loved every moment.”":
"„დაუვიწყარი ტური! მადლობა თიმურს და მის გუნდს — ყოველ წამს ვტკბებოდი.“",
"Connecting routes via Moscow, Istanbul or Dubai. Real prices for 2026 from Kazan.":
"გადაჯდომითი მარშრუტები მოსკოვის, სტამბოლის ან დუბაის გავლით. რეალური ფასები 2026-ისთვის ყაზანიდან.",
"Tours to Georgia from Kazan 2026 — Flights &amp; Guided Tours | Sakhva Travel":
"ტურები საქართველოში ყაზანიდან 2026 — ფრენები და ტურები გიდით | Sakhva Travel",
"An honest comparison of both formats for a trip to Georgia from Kazan.":
"ორივე ფორმატის პატიოსანი შედარება საქართველოში მოგზაურობისთვის ყაზანიდან.",
"Tours to Georgia from Kazan 2026 — how to get there and what to see":
"ტურები საქართველოში ყაზანიდან 2026 — როგორ მივიდეთ და რა ვნახოთ",
"Frequently Asked Questions about Tours to Georgia from Kazan":
"ხშირად დასმული კითხვები საქართველოში ყაზანიდან ტურებზე",
"Tours to Georgia from Kazan 2026 — How to Plan Your Trip":
"ტურები საქართველოში ყაზანიდან 2026 — როგორ დავგეგმოთ მოგზაურობა",
"Tours to Georgia from Kazan 2026 — Flights &amp; Prices":
"ტურები საქართველოში ყაზანიდან 2026 — ფრენები და ფასები",
"Essential info before your trip from Kazan to Georgia.":
"აუცილებელი ინფო ყაზანიდან საქართველოში მოგზაურობამდე.",
"How much does a 7-day tour to Georgia from Kazan cost?":
"რა ღირს 7-დღიანი ტური საქართველოში ყაზანიდან?",
"How much does a 7-day trip to Georgia from Kazan cost?":
"რა ღირს 7-დღიანი მოგზაურობა საქართველოში ყაზანიდან?",
"When is the best time to visit Georgia from Kazan?":
"როდის არის საქართველოს მონახულების საუკეთესო დრო ყაზანიდან?",
"Georgia Itineraries from Kazan: 5, 7 and 10 Days":
"საქართველოს მარშრუტები ყაზანიდან: 5, 7 და 10 დღე",
"Which tours are must-do for visitors from Kazan?":
"რომელი ტურებია აუცილებელი ყაზანიდან ვიზიტორებისთვის?",
"Tours in Tbilisi — What to Book from Kazan":
"ტურები თბილისში — რა დავჯავშნოთ ყაზანიდან",
"How to get to Tbilisi from Kazan in 2026?":
"როგორ მივიდეთ თბილისში ყაზანიდან 2026-ში?",
"Practical Tips for Travellers from Kazan":
"პრაქტიკული რჩევები ყაზანიდან მოგზაურებისთვის",
"Budget for a Trip to Georgia from Kazan":
"ბიუჯეტი საქართველოში მოგზაურობისთვის ყაზანიდან",
"How to get to Tbilisi from Kazan?":
"როგორ მივიდეთ თბილისში ყაზანიდან?",
"What Kazan Travellers Should Know":
"რა უნდა იცოდნენ ყაზანელმა მოგზაურებმა",
"How to Get to Georgia from Kazan":
"როგორ მივიდეთ საქართველოში ყაზანიდან",
"Kazan International Airport":
"ყაზანის საერთაშორისო აეროპორტი",
"Planning a trip from Kazan?":
"გეგმავთ მოგზაურობას ყაზანიდან?",
"Tours to Georgia from Kazan":
"ტურები საქართველოში ყაზანიდან",
"Halal-Friendly Destination":
"ჰალალ-მეგობრული მიმართულება",
"Kazan → Istanbul → Tbilisi":
"ყაზანი → სტამბოლი → თბილისი",
"Kazan → Moscow → Tbilisi":
"ყაზანი → მოსკოვი → თბილისი",
"Kazan → Tbilisi (direct)":
"ყაზანი → თბილისი (პირდაპირი)",
"Kazan → Dubai → Tbilisi":
"ყაზანი → დუბაი → თბილისი",
"Mild Climate Contrast":
"რბილი კლიმატის კონტრასტი",
"Cultural Parallel":
"კულტურული პარალელი",
"Kazan":
"ყაზანი",
"from Kazan":
"ყაზანიდან",
"from 14,000 RUB":
"14,000 RUB-დან",
"from 16,000 RUB":
"16,000 RUB-დან",
"from 16K":
"16K-დან",
"· February 2026":
"· თებერვალი 2026",
"6–8 hours":
"6–8 საათი",
}
tm.update(L)
TM.write_text(json.dumps(tm, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

ANCHOR = {"Georgia": "საქართველო"}
for f in sys.argv[1:]:
    p = Path(f); html = p.read_text(encoding="utf-8")
    for en, ka in ANCHOR.items():
        html = html.replace(f">{en}<", f">{ka}<")
    for a, b in ((">and<", ">და<"), ("> and <", "> და <"), (">Airline<", ">ავიახაზი<")):
        html = html.replace(a, b)
    for a, b in {'aria-label="Меню"':'aria-label="მენიუ"','aria-label="Закрыть"':'aria-label="დახურვა"',
                 'aria-label="Контакт"':'aria-label="კონტაქტი"','aria-label="Музыка"':'aria-label="მუსიკა"'}.items():
        html = html.replace(a, b)
    p.write_text(html, encoding="utf-8")
print(f"TM: +{len(L)} → {len(tm)}")
