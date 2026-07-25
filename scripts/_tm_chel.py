#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гео-лендинг Челябинск: полный перевод город-специфичных строк."""
import json, sys
from pathlib import Path
TM = Path("scripts/ge_tm.json")
tm = json.loads(TM.read_text(encoding="utf-8"))

L = {
"Planning a tour to Georgia from Chelyabinsk in 2026 is entirely doable. With a connection through Istanbul, Dubai or Yerevan you reach Tbilisi in a single day of travel — and from there a whole country opens up: the Kazbegi mountains, kvevri wine in Kakheti, medieval Tbilisi and the sulfur baths. From there, a country awaits where in a single trip you can see the Kazbegi mountains, taste kvevri wine in Kakheti, stroll the medieval streets of Tbilisi and soak in the sulfur baths — all at a budget that will surprise even seasoned travellers. A self-planned trip with a private tour costs 25–35% less than a package tour from a travel agency, and delivers incomparably richer experiences.":
"საქართველოში ტურის დაგეგმვა ჩელიაბინსკიდან 2026 წელს სავსებით შესაძლებელია. სტამბოლის, დუბაის ან ერევნის გავლით გადაჯდომით თბილისს ერთ დღეში აღწევთ — და იქიდან მთელი ქვეყანა იხსნება: ყაზბეგის მთები, ქვევრის ღვინო კახეთში, შუასაუკუნეების თბილისი და გოგირდის აბანოები. იქიდან იშლება ქვეყანა, სადაც ერთ მოგზაურობაში ნახავთ ყაზბეგის მთებს, დააგემოვნებთ ქვევრის ღვინოს კახეთში, გაივლით თბილისის შუასაუკუნეების ქუჩებში და დატკბებით გოგირდის აბანოებით — და ეს ყველაფერი ისეთ ბიუჯეტში, რომელიც გამოცდილ მოგზაურსაც კი გააკვირვებს. დამოუკიდებლად დაგეგმილი მოგზაურობა კერძო გიდით 25–35%-ით იაფია, ვიდრე პაკეტ-ტური ტურაგენტობიდან, და შეუდარებლად მდიდარ შთაბეჭდილებებს გჩუქნით.",
"Georgia uses the lari (GEL, ₾). Exchange rubles, dollars or euros in Tbilisi — the best rates are on Rustaveli Avenue and at Dezerter Market, better than exchanging at home. Best exchange offices are on Rustaveli Avenue and at Dezerter Market. USD and EUR are accepted everywhere. Mir cards are not accepted — bring cash or a foreign bank card (Visa/Mastercard).":
"საქართველო იყენებს ლარს (GEL, ₾). რუბლი, დოლარი ან ევრო გადაცვალეთ თბილისში — საუკეთესო კურსი რუსთაველის გამზირსა და დეზერტირების ბაზარშია, სახლში გადაცვლაზე უკეთესი. საუკეთესო გადამცვლელი პუნქტები რუსთაველის გამზირსა და დეზერტირების ბაზარშია. USD და EUR ყველგან მიიღება. Mir ბარათები არ მიიღება — წაიღეთ ნაღდი ფული ან უცხოური ბანკის ბარათი (Visa/Mastercard).",
"There are no direct flights from Chelyabinsk to Tbilisi since 2022. The most popular routes connect via Istanbul (Turkish Airlines), Dubai (flydubai/Emirates), Yerevan or Minsk, with roughly 6–11 hours of total travel depending on the layover. Booking a connecting ticket 1–2 months ahead gives the best fare.":
"ჩელიაბინსკიდან თბილისში პირდაპირი რეისები 2022 წლიდან არ არის. ყველაზე პოპულარული მარშრუტები გადის სტამბოლის (Turkish Airlines), დუბაის (flydubai/Emirates), ერევნის ან მინსკის გავლით, სულ დაახლოებით 6–11 საათი მგზავრობით გადაჯდომის მიხედვით. გადაჯდომითი ბილეთის დაჯავშნა 1–2 თვით ადრე საუკეთესო ფასს იძლევა.",
"Top 3 essential tours: 1) Kazbegi — mountains, Gergeti Trinity Church facing Mt. Kazbek (from ₾175/person); 2) Kakheti — wine, Sighnaghi, kvevri tasting (from ₾170/person); 3) Mtskheta — UNESCO, Svetitskhoveli (from ₾98/person). In the city: Old Tbilisi walking tour (from ₾100/person).":
"ტოპ 3 აუცილებელი ტური: 1) ყაზბეგი — მთები, გერგეტის სამების ეკლესია ყაზბეგის მწვერვალის ფონზე (₾175-დან/ადამიანი); 2) კახეთი — ღვინო, სიღნაღი, ქვევრის დეგუსტაცია (₾170-დან/ადამიანი); 3) მცხეთა — UNESCO, სვეტიცხოველი (₾98-დან/ადამიანი). ქალაქში: ძველი თბილისის საფეხმავლო ტური (₾100-დან/ადამიანი).",
"A self-planned 7-day trip from Chelyabinsk covers connecting flights (via Istanbul or Dubai), accommodation from ₾50/night, food, and guided tours from ₾98/person. It usually works out cheaper and far more flexible than a package tour, which rarely includes quality private excursions.":
"დამოუკიდებლად დაგეგმილი 7-დღიანი მოგზაურობა ჩელიაბინსკიდან მოიცავს გადაჯდომით ფრენებს (სტამბოლის ან დუბაის გავლით), საცხოვრებელს ₾50/ღამედან, საკვებს და ტურებს გიდთან ₾98-დან/ადამიანი. ჩვეულებრივ ეს უფრო იაფი და გაცილებით მოქნილია, ვიდრე პაკეტ-ტური, რომელიც იშვიათად მოიცავს ხარისხიან კერძო ექსკურსიებს.",
"No, Mir cards are not accepted in Georgia. Bring cash rubles/dollars and exchange to lari in Tbilisi (best rates on Rustaveli and at Dezerter Market). Visa and Mastercard from foreign banks work everywhere. Withdraw lari from TBC Bank and Bank of Georgia ATMs without issues.":
"არა, Mir ბარათები საქართველოში არ მიიღება. წაიღეთ ნაღდი რუბლი/დოლარი და გადაცვალეთ ლარში თბილისში (საუკეთესო კურსი რუსთაველზე და დეზერტირების ბაზარში). Visa და Mastercard უცხოური ბანკებიდან ყველგან მუშაობს. ლარი გაიტანეთ TBC Bank-ისა და Bank of Georgia-ს ბანკომატებიდან უპრობლემოდ.",
"Best times are spring (April–May) and autumn (September–October). May brings cherry blossoms; September–October is wine harvest season in Kakheti. Summer (June–August) is hot (+35–38°C in Tbilisi), winter is mild in the city (+5–10°C) and ski season at Gudauri.":
"საუკეთესო დროა გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტემბერი–ოქტომბერი). მაისში ალუბლის ყვავილობაა; სექტემბერი–ოქტომბერი ღვინის მოსავლის სეზონია კახეთში. ზაფხული (ივნისი–აგვისტო) ცხელა (+35–38°C თბილისში), ზამთარი რბილია ქალაქში (+5–10°C) და სათხილამურო სეზონია გუდაურში.",
"The best time is spring (April–May) and autumn (September–October). Summer is hot (+35–38°C in Tbilisi), winter is mild in the city (+5–10°C) but great for skiing at Gudauri. The Kazbegi season (mountain routes) runs from May to October.":
"საუკეთესო დროა გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტემბერი–ოქტომბერი). ზაფხული ცხელა (+35–38°C თბილისში), ზამთარი რბილია ქალაქში (+5–10°C), მაგრამ შესანიშნავია გუდაურში სათხილამუროდ. ყაზბეგის სეზონი (მთის მარშრუტები) გრძელდება მაისიდან ოქტომბრამდე.",
"Guide Timur is fluent in both English and Russian, and has lived in Tbilisi since 2023. All tours are conducted in your language of choice. He explains Georgian history and culture in a way that truly resonates.":
"გიდი თიმური თავისუფლად ფლობს ინგლისურსა და რუსულს და თბილისში 2023 წლიდან ცხოვრობს. ყველა ტური მიმდინარეობს თქვენს არჩეულ ენაზე. ის ქართულ ისტორიასა და კულტურას ისე ხსნის, რომ ნამდვილად ეხმიანება.",
"No, Russian citizens do not need a visa for Georgia. Russians can stay up to 365 days visa-free with a Russian passport. A foreign passport or internal passport (внутренний паспорт) is accepted at the border.":
"არა, რუსეთის მოქალაქეებს ვიზა საქართველოსთვის არ სჭირდებათ. რუსებს შეუძლიათ 365 დღემდე ყოფნა უვიზოდ რუსული პასპორტით. საზღვარზე მიიღება საზღვარგარეთის ან შიდა პასპორტი.",
"Currency is the lari (₾). 1 GEL ≈ 37 RUB (2026). Exchange rubles in Tbilisi: best rates on Rustaveli Ave. Mir cards don't work. Visa/Mastercard accepted everywhere. ATMs: TBC Bank, Bank of Georgia.":
"ვალუტა ლარია (₾). 1 GEL ≈ 37 RUB (2026). რუბლი გადაცვალეთ თბილისში: საუკეთესო კურსი რუსთაველის გამზირზე. Mir ბარათები არ მუშაობს. Visa/Mastercard ყველგან მიიღება. ბანკომატები: TBC Bank, Bank of Georgia.",
"Search tickets on Yandex Travel or Skyscanner with the \"with connections\" filter. Best prices are 2–3 months before departure. Peak season (July–August) can push prices to 30,000–40,000 RUB.":
"ბილეთები მოძებნეთ Yandex Travel-ზე ან Skyscanner-ზე ფილტრით «გადაჯდომებით». საუკეთესო ფასები გამგზავრებამდე 2–3 თვით ადრეა. პიკ-სეზონზე (ივლისი–აგვისტო) ფასი 30,000–40,000 RUB-მდე ადის.",
"From the Ural's industrial heartland to the ancient stones of Tbilisi and the Caucasus peaks — a journey of transformation that many Chelyabinsk travellers describe as life-changing.":
"ურალის ინდუსტრიული გულიდან თბილისის უძველეს ქვებამდე და კავკასიის მწვერვალებამდე — გარდაქმნის მოგზაურობა, რომელსაც ბევრი ჩელიაბინსკელი მოგზაური ცხოვრების შემცვლელად აღწერს.",
"From Chelyabinsk fly via Istanbul — it's the best price option and only one stop. I'll plan the first tour for your arrival afternoon. Best 7-day combo: Tbilisi + Kazbegi + Kakheti.":
"ჩელიაბინსკიდან იფრინეთ სტამბოლის გავლით — ეს საუკეთესო ფასის ვარიანტია და მხოლოდ ერთი გადაჯდომა. პირველ ტურს თქვენი ჩამოსვლის შუადღისთვის დავგეგმავ. საუკეთესო 7-დღიანი კომბო: თბილისი + ყაზბეგი + კახეთი.",
"CEK has connections to Istanbul (Turkish Airlines) and Moscow. Combine the Moscow option with any connecting route for the most flexible schedule.":
"CEK-ს აქვს კავშირები სტამბოლთან (Turkish Airlines) და მოსკოვთან. მოსკოვის ვარიანტი ნებისმიერ გადაჯდომით მარშრუტთან შეუთავსეთ ყველაზე მოქნილი განრიგისთვის.",
"Planning a trip to Georgia from Chelyabinsk? Flights/transport to Tbilisi, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.":
"გეგმავთ მოგზაურობას საქართველოში ჩელიაბინსკიდან? ფრენები/ტრანსპორტი თბილისამდე, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან.",
"Flights from 18,000 RUB, accommodation from ₾50/night, private tours from ₾98. Georgia — an ancient world one timezone away from Chelyabinsk.":
"ფრენები 18,000 RUB-დან, საცხოვრებელი ₾50/ღამედან, კერძო ტურები ₾98-დან. საქართველო — უძველესი სამყარო ერთი დროის სარტყლის დაშორებით ჩელიაბინსკიდან.",
"We went to Kazbegi — Timur convinced us the special atmosphere was worth it. Snow by the church, silence. The most romantic day of the trip.":
"ყაზბეგში წავედით — თიმურმა დაგვარწმუნა, რომ განსაკუთრებული ატმოსფერო ღირდა. თოვლი ეკლესიასთან, სიჩუმე. მოგზაურობის ყველაზე რომანტიკული დღე.",
"A package tour from Chelyabinsk costs 70,000–100,000 RUB per person. A self-planned trip with a private tour costs 25–35% less.":
"პაკეტ-ტური ჩელიაბინსკიდან ღირს 70,000–100,000 RUB ერთ ადამიანზე. დამოუკიდებლად დაგეგმილი მოგზაურობა კერძო გიდით 25–35%-ით იაფია.",
"Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur. 30% cheaper than package tours.":
"ფრენები 15K RUB-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან. 30%-ით იაფი პაკეტ-ტურებზე.",
"With the travel distance from Chelyabinsk, plan at least 7 days to fully absorb Tbilisi, the mountains and wine country.":
"ჩელიაბინსკიდან მგზავრობის მანძილის გათვალისწინებით, დაგეგმეთ მინიმუმ 7 დღე, რომ სრულად შეიგრძნოთ თბილისი, მთები და ღვინის მხარე.",
"“Booked a private tour for four. Timur is a true professional: knows the history and tells it in a fascinating way.”":
"„დავჯავშნე კერძო ტური ოთხისთვის. თიმური ნამდვილი პროფესიონალია: იცის ისტორია და მომხიბვლელად ჰყვება.“",
"Via Istanbul (Turkish Airlines, from 18,000 RUB round-trip, ~7–9 hours) is most popular. Also via Moscow or Dubai.":
"სტამბოლის გავლით (Turkish Airlines, 18,000 RUB-დან ორმხრივი, ~7–9 საათი) ყველაზე პოპულარულია. ასევე მოსკოვის ან დუბაის გავლით.",
"You have no idea how much I enjoyed it. Nice tiredness, nice people, delicious food. Thank you very much.":
"წარმოდგენა არ გაქვთ, როგორ ვისიამოვნე. სასიამოვნო დაღლილობა, სასიამოვნო ხალხი, გემრიელი საკვები. დიდი მადლობა.",
"Chelyabinsk is UTC+5, Tbilisi UTC+4 — you go back just one hour. Virtually no jet lag adjustment needed.":
"ჩელიაბინსკი UTC+5-ია, თბილისი UTC+4 — სულ ერთი საათით უკან იწევთ. პრაქტიკულად არანაირი ჯეტლაგის ადაპტაცია არ სჭირდება.",
"Excellent guide. Showed and told us everything about sunny Georgia. Speaks great English and Russian.":
"შესანიშნავი გიდი. ყველაფერი გვაჩვენა და გვიამბო მზიან საქართველოზე. მშვენივრად ლაპარაკობს ინგლისურად და რუსულად.",
"Costs vary by transport option. See the budget table above for a full breakdown from Chelyabinsk.":
"ხარჯები ტრანსპორტის ვარიანტის მიხედვით განსხვავდება. იხილეთ ბიუჯეტის ცხრილი ზემოთ სრული დაყოფისთვის ჩელიაბინსკიდან.",
"“Amazing tour, thank you so much! Timur showed us places we would never have found on our own.”":
"„საოცარი ტური, დიდი მადლობა! თიმურმა გვაჩვენა ადგილები, რომლებსაც თვითონ ვერასდროს ვიპოვიდით.“",
"Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with a private tour.":
"ფრენები 15K RUB-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე კერძო ტურით.",
"Real cost breakdown for 7 days, one person. Prices for April–October 2026 from Chelyabinsk.":
"რეალური ხარჯების დაყოფა 7 დღეზე, ერთ ადამიანზე. ფასები აპრილი–ოქტომბერი 2026-ისთვის ჩელიაბინსკიდან.",
"Tours to Georgia from Chelyabinsk 2026 — Flights &amp; Guided Tours | Sakhva Travel":
"ტურები საქართველოში ჩელიაბინსკიდან 2026 — ფრენები და ტურები გიდით | Sakhva Travel",
"Connecting via Istanbul, Moscow or Dubai. Real prices for 2026 from Chelyabinsk.":
"გადაჯდომით სტამბოლის, მოსკოვის ან დუბაის გავლით. რეალური ფასები 2026-ისთვის ჩელიაბინსკიდან.",
"An honest comparison of both formats for a trip to Georgia from Chelyabinsk.":
"ორივე ფორმატის პატიოსანი შედარება საქართველოში მოგზაურობისთვის ჩელიაბინსკიდან.",
"Tours to Georgia from Chelyabinsk 2026 — flights, prices and routes":
"ტურები საქართველოში ჩელიაბინსკიდან 2026 — ფრენები, ფასები და მარშრუტები",
"Frequently Asked Questions about Tours to Georgia from Chelyabinsk":
"ხშირად დასმული კითხვები საქართველოში ჩელიაბინსკიდან ტურებზე",
"Tours to Georgia from Chelyabinsk 2026 — How to Plan Your Trip":
"ტურები საქართველოში ჩელიაბინსკიდან 2026 — როგორ დავგეგმოთ მოგზაურობა",
"Essential info before your trip from Chelyabinsk to Georgia.":
"აუცილებელი ინფო ჩელიაბინსკიდან საქართველოში მოგზაურობამდე.",
"How much does a 7-day tour to Georgia from Chelyabinsk cost?":
"რა ღირს 7-დღიანი ტური საქართველოში ჩელიაბინსკიდან?",
"How much does a 7-day trip to Georgia from Chelyabinsk cost?":
"რა ღირს 7-დღიანი მოგზაურობა საქართველოში ჩელიაბინსკიდან?",
"Tours to Georgia from Chelyabinsk 2026 — Flights &amp; Tours":
"ტურები საქართველოში ჩელიაბინსკიდან 2026 — ფრენები და ტურები",
"When is the best time to visit Georgia from Chelyabinsk?":
"როდის არის საქართველოს მონახულების საუკეთესო დრო ჩელიაბინსკიდან?",
"Georgia Itineraries from Chelyabinsk: 5, 7 and 10 Days":
"საქართველოს მარშრუტები ჩელიაბინსკიდან: 5, 7 და 10 დღე",
"Which tours are must-do for visitors from Chelyabinsk?":
"რომელი ტურებია აუცილებელი ჩელიაბინსკიდან ვიზიტორებისთვის?",
"Tours in Tbilisi — What to Book from Chelyabinsk":
"ტურები თბილისში — რა დავჯავშნოთ ჩელიაბინსკიდან",
"How to get to Tbilisi from Chelyabinsk in 2026?":
"როგორ მივიდეთ თბილისში ჩელიაბინსკიდან 2026-ში?",
"Practical Tips for Travellers from Chelyabinsk":
"პრაქტიკული რჩევები ჩელიაბინსკიდან მოგზაურებისთვის",
"Budget for a Trip to Georgia from Chelyabinsk":
"ბიუჯეტი საქართველოში მოგზაურობისთვის ჩელიაბინსკიდან",
"How to get to Tbilisi from Chelyabinsk?":
"როგორ მივიდეთ თბილისში ჩელიაბინსკიდან?",
"What Chelyabinsk Travellers Should Know":
"რა უნდა იცოდნენ ჩელიაბინსკელმა მოგზაურებმა",
"How to Get to Georgia from Chelyabinsk":
"როგორ მივიდეთ საქართველოში ჩელიაბინსკიდან",
"What currency to bring to Georgia?":
"რა ვალუტა წავიღოთ საქართველოში?",
"Planning a trip from Chelyabinsk?":
"გეგმავთ მოგზაურობას ჩელიაბინსკიდან?",
"Tours to Georgia from Chelyabinsk":
"ტურები საქართველოში ჩელიაბინსკიდან",
"Chelyabinsk → Istanbul → Tbilisi":
"ჩელიაბინსკი → სტამბოლი → თბილისი",
"Chelyabinsk → Moscow → Tbilisi":
"ჩელიაბინსკი → მოსკოვი → თბილისი",
"Chelyabinsk → Dubai → Tbilisi":
"ჩელიაბინსკი → დუბაი → თბილისი",
"Ural Airlines + connecting":
"Ural Airlines + გადაჯდომა",
"Ural Mountains to Caucasus":
"ურალის მთებიდან კავკასიამდე",
"All Tours in Georgia 2026":
"ყველა ტური საქართველოში 2026",
"Balandino Airport":
"ბალანდინოს აეროპორტი",
"Same UTC+5 Zone":
"იგივე UTC+5 სარტყელი",
"Plan 7+ Days":
"დაგეგმეთ 7+ დღე",
"Travel time":
"მგზავრობის დრო",
"Chelyabinsk":
"ჩელიაბინსკი",
"from Chelyabinsk":
"ჩელიაბინსკიდან",
"from Ufa":
"უფადან",
"from 18,000 RUB":
"18,000 RUB-დან",
"from 21,000 RUB":
"21,000 RUB-დან",
"from 23,000 RUB":
"23,000 RUB-დან",
"from 18K":
"18K-დან",
"· April 2026":
"· აპრილი 2026",
"9–11 hours":
"9–11 საათი",
"9–12 hours":
"9–12 საათი",
"7–9 hours":
"7–9 საათი",
}
tm.update(L)
TM.write_text(json.dumps(tm, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

ANCHOR = {"Georgia": "საქართველო"}
for f in sys.argv[1:]:
    p = Path(f); html = p.read_text(encoding="utf-8")
    for en, ka in ANCHOR.items():
        html = html.replace(f">{en}<", f">{ka}<")
    for a, b in ((">and<", ">და<"), ("> and <", "> და <")):
        html = html.replace(a, b)
    for a, b in {'aria-label="Меню"':'aria-label="მენიუ"','aria-label="Закрыть"':'aria-label="დახურვა"',
                 'aria-label="Контакт"':'aria-label="კონტაქტი"','aria-label="Музыка"':'aria-label="მუსიკა"'}.items():
        html = html.replace(a, b)
    p.write_text(html, encoding="utf-8")
print(f"TM: +{len(L)} → {len(tm)}")
