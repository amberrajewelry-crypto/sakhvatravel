#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гео-лендинг tours-from-ufa (шаблон для всех 27 городов).
Проза+метки вручную; города/дни/часы/цены-from генерятся. Имена → AUTHORS."""
import json, sys
from pathlib import Path
TM = Path("scripts/ge_tm.json")
tm = json.loads(TM.read_text(encoding="utf-8"))

L = {
# --- проза (город-специфичная, Уфа) ---
"Ufa sits on the high bank of the Agidel — the Belaya River — among the honey forests of Bashkiria and the first foothills of the Urals. Georgia is closer than it seems: a direct Azimuth flight gets you to Tbilisi in 2 hours 30 minutes, with no layovers or overnight stops in Moscow. And the welcome feels both familiar and new. Familiar, because here — as back home — a mosque, a synagogue and a church have stood side by side for centuries: old Tbilisi breathes the same spirit of good-neighbourliness. New, because instead of linden honey and kumis you'll find kvevri wine from clay vessels buried in the ground 8,000 years ago, and instead of gentle Ural ridges — the sharp five-thousanders of the Caucasus. The time difference is just one hour: home is UTC+5, Tbilisi is UTC+4.":
"უფა დგას აღიდელის — მდინარე ბელაიას — მაღალ ნაპირზე, ბაშკირეთის თაფლოვან ტყეებსა და ურალის პირველ მთისწინეთს შორის. საქართველო უფრო ახლოსაა, ვიდრე ჩანს: პირდაპირი ავიარეისი Azimuth-ით თბილისში 2 საათსა და 30 წუთში მიგიყვანთ, გადაჯდომებისა და მოსკოვში ღამისთევის გარეშე. და მისაღები ერთდროულად ნაცნობი და ახალია. ნაცნობი, რადგან აქ — როგორც სახლში — მეჩეთი, სინაგოგა და ეკლესია საუკუნეების განმავლობაში გვერდიგვერდ დგანან: ძველი თბილისი იმავე კეთილმეზობლობის სულს სუნთქავს. ახალი, რადგან ცაცხვის თაფლისა და ქუმისის ნაცვლად აქ ნახავთ ქვევრის ღვინოს თიხის ჭურჭლიდან, 8000 წლის წინ მიწაში ჩაფლულიდან, და რბილი ურალის ქედების ნაცვლად — კავკასიის მკვეთრ ხუთათასიანებს. დროის სხვაობა სულ ერთი საათია: სახლი UTC+5-ია, თბილისი — UTC+4.",
"Direct flights are operated by Azimuth from Ufa International Airport named after Mustai Karim (code UFA). Flight time is 2 hours 30 minutes, landing at Tbilisi's Shota Rustaveli airport. One-way fares start from 14,500 RUB, round-trip from about 22,000 RUB; on sales, one-way tickets have dropped to 4,500 RUB. Book 5–7 weeks ahead and avoid Friday and Sunday departures for the best prices. Azimuth accepts Mir, Visa and Mastercard, so you can pay from Russia directly. Tip: choose a fare with checked baggage included — paying at the airport costs more, and on the way back from Tbilisi you'll likely carry wine, churchkhela and spices.":
"პირდაპირ რეისებს ახორციელებს Azimuth უფას საერთაშორისო აეროპორტიდან, მუსტაი ქარიმის სახელობის (კოდი UFA). ფრენის დრო 2 საათი და 30 წუთია, დაფრენა თბილისის შოთა რუსთაველის აეროპორტში. ცალმხრივი ბილეთი იწყება 14,500 RUB-დან, ორმხრივი დაახლოებით 22,000 RUB-დან; აქციებზე ცალმხრივი ბილეთი 4,500 RUB-მდე დაეცა. დაჯავშნეთ 5–7 კვირით ადრე და აიცილეთ პარასკევსა და კვირას გამგზავრება საუკეთესო ფასებისთვის. Azimuth იღებს Mir-ს, Visa-სა და Mastercard-ს, ასე რომ რუსეთიდან პირდაპირ გადაიხდით. რჩევა: აირჩიეთ ტარიფი ჩასაბარებელი ბარგის ჩათვლით — აეროპორტში გადახდა უფრო ძვირია, თბილისიდან უკან კი სავარაუდოდ ღვინოს, ჩურჩხელასა და სანელებლებს წაიღებთ.",
"I'm not a travel agency or aggregator. I'm Timur, a private tour who has lived in Tbilisi for over 10 years. Every route is designed by me personally, and I know every location from the inside. No 40-person buses, no rushing. Mini-groups up to 7 or private tours. Flexible itinerary: we stop where you want, eat where it's actually good (not where I get commission), and photograph where it's beautiful. 200+ reviews on Google Maps — check for yourself.":
"მე არ ვარ ტურაგენტობა ან აგრეგატორი. მე ვარ თიმური, კერძო გიდი, თბილისში 10 წელზე მეტია ვცხოვრობ. ყოველი მარშრუტი პირადად ჩემ მიერაა შედგენილი და ყველა ადგილს შიგნიდან ვიცნობ. არანაირი 40-ადგილიანი ავტობუსი, არანაირი ჩქარობა. მინი-ჯგუფები 7 ადამიანამდე ან კერძო ტურები. მოქნილი მარშრუტი: ვჩერდებით სადაც გსურთ, ვჭამთ სადაც ნამდვილად კარგია (და არა სადაც კომისიას ვიღებ) და ვიღებთ ფოტოებს სადაც ლამაზია. 200+ შეფასება Google Maps-ზე — თავად შეამოწმეთ.",
"From Ufa I always recommend the direct Azimuth flight — 2.5 hours and you're in Tbilisi, no exhausting layovers. Only one hour of time difference. In my experience, those used to Bashkir honey and herbal tea love Kakheti — kvevri wine tasting in a real marani. And after the soft Urals, Kazbegi feels like mountains of a completely different scale. I recommend 7 days minimum.":
"უფადან ყოველთვის ვურჩევ პირდაპირ Azimuth-ის რეისს — 2.5 საათი და თბილისში ხართ, დამქანცველი გადაჯდომების გარეშე. სულ ერთი საათი დროის სხვაობა. ჩემი გამოცდილებით, ვისაც ბაშკირული თაფლი და მცენარეული ჩაი უყვარს, კახეთი მოსწონს — ქვევრის ღვინის დეგუსტაცია ნამდვილ მარანში. და რბილი ურალის შემდეგ ყაზბეგი სრულიად სხვა მასშტაბის მთებად აღიქმება. ვურჩევ მინიმუმ 7 დღეს.",
"Three picks: Kakheti — wine country where a lover of Bashkir honey and teas will appreciate kvevri wine (from ₾170); Kazbegi — sharp Caucasus peaks after the soft Urals (from ₾175); Mtskheta — 2,000 years of Christian history and UNESCO sites (from ₾98). Plus Old Tbilisi on foot (from ₾100).":
"სამი არჩევანი: კახეთი — ღვინის მხარე, სადაც ბაშკირული თაფლისა და ჩაის მოყვარული დააფასებს ქვევრის ღვინოს (₾170-დან); ყაზბეგი — კავკასიის მკვეთრი მწვერვალები რბილი ურალის შემდეგ (₾175-დან); მცხეთა — 2000 წლის ქრისტიანული ისტორია და UNESCO-ს ძეგლები (₾98-დან). პლუს ძველი თბილისი ფეხით (₾100-დან).",
"Mir cards are not accepted inside Georgia, but Azimuth sells Ufa–Tbilisi tickets for Mir on its website. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Ufa banks. Visa and Mastercard from foreign banks work in most places.":
"Mir ბარათები საქართველოში არ მიიღება, მაგრამ Azimuth უფა–თბილისის ბილეთებს Mir-ით ყიდის საკუთარ საიტზე. წაიღეთ ნაღდი რუბლი და თბილისში გადაცვალეთ — რუსთაველის მეტროსთან კურსი უფას ბანკებს სჯობს. Visa და Mastercard უცხოური ბანკებიდან უმეტეს ადგილას მუშაობს.",
"Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti, with a chance to join the rtveli. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October.":
"ამინდით საუკეთესოა: გაზაფხული (აპრილი–მაისი) და შემოდგომა (სექტემბერი–ოქტომბერი). სექტემბერი–ოქტომბერი განსაკუთრებულია — ღვინის მოსავლის სეზონი კახეთში, რთველში მონაწილეობის შანსით. ზაფხული ცხელა (+35–38°C); ყაზბეგის მთის მარშრუტები მაისი–ოქტომბერში მუშაობს.",
"The easiest option is the direct Azimuth flight Ufa–Tbilisi — 2 hours 30 minutes, from 22,000 RUB round-trip. Connections also exist via Moscow (7–9h, from 19,000 RUB) or Istanbul. Azimuth accepts Mir, Visa and Mastercard.":
"ყველაზე მარტივი ვარიანტია პირდაპირი Azimuth-ის რეისი უფა–თბილისი — 2 საათი და 30 წუთი, 22,000 RUB-დან ორმხრივი. გადაჯდომებიც არსებობს მოსკოვის (7–9სთ, 19,000 RUB-დან) ან სტამბოლის გავლით. Azimuth იღებს Mir-ს, Visa-სა და Mastercard-ს.",
"A self-planned 7-day trip costs from 40,000 RUB: direct flight ~22,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours.":
"დამოუკიდებლად დაგეგმილი 7-დღიანი მოგზაურობა ღირს 40,000 RUB-დან: პირდაპირი ფრენა ~22,000 RUB, საცხოვრებელი ~5,500 RUB/კვირა, საკვები ~3,000 RUB, ტურები ~12,000 RUB-დან. პაკეტ-ტური ღირს 65,000–95,000 RUB და არ მოიცავს კერძო ტურებს გიდთან.",
"Currency is the lari (₾). 1 GEL ≈ 37 RUB (2026). Exchange rubles in Tbilisi: best rates on Rustaveli Ave, better than Ufa banks. Mir cards don't work. Visa/Mastercard accepted everywhere. ATMs: TBC Bank, Bank of Georgia.":
"ვალუტა ლარია (₾). 1 GEL ≈ 37 RUB (2026). რუბლი გადაცვალეთ თბილისში: საუკეთესო კურსი რუსთაველის გამზირზე, უფას ბანკებზე უკეთესი. Mir ბარათები არ მუშაობს. Visa/Mastercard ყველგან მიიღება. ბანკომატები: TBC Bank, Bank of Georgia.",
"Yes. Azimuth operates direct Ufa–Tbilisi flights, 2 hours 30 minutes each way. Red Wings and Georgian Airways are also cleared for Russia–Georgia routes. Book on the carrier's site; payment by Mir, Visa and Mastercard.":
"დიახ. Azimuth ახორციელებს პირდაპირ უფა–თბილისის რეისებს, 2 საათი და 30 წუთი თითო მიმართულებით. Red Wings და Georgian Airways ასევე დაშვებულია რუსეთი–საქართველოს რეისებზე. დაჯავშნეთ გადამზიდავის საიტზე; გადახდა Mir-ით, Visa-თი და Mastercard-ით.",
"No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required.":
"არა. რუსეთის მოქალაქეებს შეუძლიათ საქართველოში უვიზოდ ყოფნა 365 დღემდე საზღვარგარეთის ან შიდა პასპორტით. სასაზღვრო კონტროლი თბილისის აეროპორტში 10–20 წუთს იღებს. არანაირი ფორმა, მოსაწვევი ან დაზღვევა არ არის საჭირო.",
"Bashkiria is famous for linden honey, kumis and herbal teas. Georgia answers with kvevri wine from clay vessels buried underground — a craft older than the pyramids. Not a rivalry, but a pairing of flavours.":
"ბაშკირეთი ცნობილია ცაცხვის თაფლით, ქუმისითა და მცენარეული ჩაებით. საქართველო პასუხობს ქვევრის ღვინით თიხის ჭურჭლიდან, მიწაში ჩაფლულიდან — ხელობა პირამიდებზე ძველი. არა მეტოქეობა, არამედ გემოების შერწყმა.",
"In Ufa a mosque and Orthodox churches stand together. In old Tbilisi a mosque, a synagogue and a church sit within a five-minute walk. Both cities know the culture of different peoples living side by side.":
"უფაში მეჩეთი და მართლმადიდებლური ეკლესიები ერთად დგანან. ძველ თბილისში მეჩეთი, სინაგოგა და ეკლესია ხუთწუთიან სავალზეა. ორივე ქალაქმა იცის სხვადასხვა ხალხის გვერდიგვერდ ცხოვრების კულტურა.",
"Yes. All tours can be cancelled free of charge up to 24 hours before the start. Cancellations within 24 hours incur a 50% fee. Rescheduling is always possible — just message via WhatsApp or Telegram.":
"დიახ. ყველა ტური შეიძლება უფასოდ გაუქმდეს დაწყებამდე 24 საათით ადრე. 24 საათში გაუქმებას 50% საკომისიო აქვს. გადატანა ყოველთვის შესაძლებელია — უბრალოდ მისწერეთ WhatsApp-ით ან Telegram-ით.",
"the direct Azimuth flight is the easiest option — only 2.5 hours in the air. The carrier accepts Mir, Visa and Mastercard. On sales, one-way tickets have dropped to 4,500 RUB — book 5–7 weeks ahead.":
"პირდაპირი Azimuth-ის რეისი ყველაზე მარტივი ვარიანტია — სულ 2.5 საათი ჰაერში. გადამზიდავი იღებს Mir-ს, Visa-სა და Mastercard-ს. აქციებზე ცალმხრივი ბილეთი 4,500 RUB-მდე დაეცა — დაჯავშნეთ 5–7 კვირით ადრე.",
"Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.":
"გიდი თიმური თავისუფლად ფლობს ინგლისურსა და რუსულს და თბილისში 2023 წლიდან ცხოვრობს. ტურები თქვენს არჩეულ ენაზე მიდის — ის ქართულ ისტორიასა და კულტურას ისე ხსნის, რომ ნამდვილად ეხმიანება.",
"Ufa travellers win on the direct flight: 2.5 hours in the air versus 7–9 with a Moscow layover. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.":
"უფას მოგზაურები იგებენ პირდაპირ ფრენაზე: 2.5 საათი ჰაერში 7–9-ის ნაცვლად მოსკოვში გადაჯდომით. პაკეტ-ტური ღირს 65,000–95,000 RUB საცხოვრებლისა თუ ტურების არჩევის თავისუფლების გარეშე.",
"Azimuth flies Ufa–Tbilisi non-stop in 2 hours 30 minutes and accepts Mir cards. No layovers, no overnight stops in Moscow — you land and start your trip right away.":
"Azimuth დაფრინავს უფა–თბილისი უშუალოდ 2 საათსა და 30 წუთში და იღებს Mir ბარათებს. არანაირი გადაჯდომა, არანაირი ღამისთევა მოსკოვში — დაეშვებით და მაშინვე იწყებთ მოგზაურობას.",
"Russian citizens can stay in Georgia up to 365 days visa-free. Only a passport (foreign or internal Russian) is needed. Border control typically takes 5–15 minutes.":
"რუსეთის მოქალაქეებს შეუძლიათ საქართველოში 365 დღემდე ყოფნა უვიზოდ. საჭიროა მხოლოდ პასპორტი (საზღვარგარეთის ან შიდა რუსული). სასაზღვრო კონტროლი ჩვეულებრივ 5–15 წუთს იღებს.",
"Direct Azimuth flight in just 2.5 hours, accommodation from ₾50/night, private tours from ₾98. Georgia is a surprisingly close and affordable destination from Ufa.":
"პირდაპირი Azimuth-ის რეისი სულ 2.5 საათში, საცხოვრებელი ₾50/ღამედან, კერძო ტურები ₾98-დან. საქართველო გასაკვირად ახლო და ხელმისაწვდომი მიმართულებაა უფადან.",
"Within Tbilisi — Bolt taxi (cheaper than Yandex.Go). To other cities — marshrutkas from Didube bus station. Guided tours include transfer in a comfortable vehicle.":
"თბილისში — Bolt ტაქსი (Yandex.Go-ზე იაფი). სხვა ქალაქებში — მარშრუტკები დიდუბის ავტოსადგურიდან. ტურები გიდთან მოიცავს ტრანსფერს კომფორტული მანქანით.",
"Buy at Tbilisi airport. Operators: Magti, Geocell, Beeline Georgia. 5 GB data plan costs ₾5–10 (≈185–370 RUB/month). Excellent 4G coverage across Georgia.":
"იყიდეთ თბილისის აეროპორტში. ოპერატორები: Magti, Geocell, Beeline Georgia. 5 GB მონაცემთა პაკეტი ღირს ₾5–10 (≈185–370 RUB/თვე). შესანიშნავი 4G დაფარვა მთელ საქართველოში.",
"Gergeti Trinity Church against Mt. Kazbek, Georgian Military Highway, Ananuri Fortress. The most popular day trip — the Caucasus mountains in one route.":
"გერგეტის სამების ეკლესია ყაზბეგის ფონზე, საქართველოს სამხედრო გზა, ანანურის ციხე. ყველაზე პოპულარული ერთდღიანი ტური — კავკასიის მთები ერთ მარშრუტში.",
"Narikala Fortress, Metekhi Church, sulfur baths, Sioni Cathedral, colorful Abanotubani balconies. The classic route through Tbilisi's historic centre.":
"ნარიყალას ციხე, მეტეხის ეკლესია, გოგირდის აბანოები, სიონის ტაძარი, აბანოთუბნის ფერადი აივნები. კლასიკური მარშრუტი თბილისის ისტორიულ ცენტრში.",
"Tours to Georgia from Ufa: direct Azimuth flight in 2.5 hours from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.":
"ტურები საქართველოში უფადან: პირდაპირი Azimuth-ის რეისი 2.5 საათში 14,500 RUB-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან.",
"Narikala lit up at night, Peace Bridge, Kura embankment in golden light. Tbilisi after dark is a completely different city — the best photo tour.":
"ღამით განათებული ნარიყალა, მშვიდობის ხიდი, მტკვრის სანაპირო ოქროსფერ შუქში. თბილისი ღამით სრულიად სხვა ქალაქია — საუკეთესო ფოტოტური.",
"Sighnaghi, Bodbe Monastery, kvevri wine tasting. Alazani Valley vineyards and a real marani cellar — perfect for wine lovers and history buffs.":
"სიღნაღი, ბოდბის მონასტერი, ქვევრის ღვინის დეგუსტაცია. ალაზნის ველის ვენახები და ნამდვილი მარანი — იდეალური ღვინისა და ისტორიის მოყვარულთათვის.",
"“We went to Kazbegi — Timur convinced us the special atmosphere was worth it. Snow by the church, silence. The most romantic day of the trip.”":
"„ყაზბეგში წავედით — თიმურმა დაგვარწმუნა, რომ განსაკუთრებული ატმოსფერო ღირდა. თოვლი ეკლესიასთან, სიჩუმე. მოგზაურობის ყველაზე რომანტიკული დღე.“",
"Jvari Monastery, Svetitskhoveli Cathedral, confluence of Aragvi and Mtkvari rivers. Georgia's spiritual heart, 20 minutes from Tbilisi.":
"ჯვრის მონასტერი, სვეტიცხოვლის ტაძარი, არაგვისა და მტკვრის შესართავი. საქართველოს სულიერი გული, თბილისიდან 20 წუთში.",
"Prometheus Cave, Martvili Canyon, Gelati Monastery (UNESCO). Western Georgia in one day — for travellers who want to see it all.":
"პრომეთეს გამოქვაბული, მარტვილის კანიონი, გელათის მონასტერი (UNESCO). დასავლეთ საქართველო ერთ დღეში — მოგზაურთათვის, ვისაც ყველაფრის ნახვა სურს.",
"Ufa is UTC+5, Tbilisi is UTC+4 — just one hour apart. Set your watch back an hour and you're in sync, with barely any jet lag.":
"უფა UTC+5-ია, თბილისი UTC+4 — სულ ერთი საათის სხვაობა. საათი ერთი საათით უკან გადაწიეთ და სინქრონში ხართ, თითქმის უჯეტლაგოდ.",
"Direct Ufa–Tbilisi flight in 2.5 hours from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.":
"პირდაპირი უფა–თბილისის რეისი 2.5 საათში 14,500 RUB-დან, ტურები გიდთან ₾98-დან. მარშრუტები 5/7/10 დღეზე გიდ თიმურთან.",
"Direct Azimuth flight Ufa–Tbilisi — 2.5 hours, no layovers. Plus connections via Moscow and Istanbul. Real prices for 2026.":
"პირდაპირი Azimuth-ის რეისი უფა–თბილისი — 2.5 საათი, გადაჯდომების გარეშე. პლუს გადაჯდომები მოსკოვისა და სტამბოლის გავლით. რეალური ფასები 2026-ისთვის.",
"Ready-made trip plans with specific tours included. All itineraries are tried and tested by guide Timur.":
"მზა მოგზაურობის გეგმები კონკრეტული ტურების ჩათვლით. ყველა მარშრუტი გამოცდილია გიდ თიმურის მიერ.",
"Message guide Timur — reply within 15 minutes. Free cancellation up to 24h. Groups up to 7 people.":
"მისწერეთ გიდ თიმურს — პასუხი 15 წუთში. უფასო გაუქმება 24სთ-მდე. ჯგუფები 7 ადამიანამდე.",
"Real cost breakdown for 7 days, one person. Prices for April–October 2026 from Ufa.":
"რეალური ხარჯების დაყოფა 7 დღეზე, ერთ ადამიანზე. ფასები აპრილი–ოქტომბერი 2026-ისთვის უფადან.",
"Tours to Georgia from Ufa 2026 — Direct Flight &amp; Private Tours | Sakhva Travel":
"ტურები საქართველოში უფადან 2026 — პირდაპირი ფრენა და კერძო ტურები | Sakhva Travel",
"6 essential routes with guide Timur. All tours in English, groups up to 7 people.":
"6 აუცილებელი მარშრუტი გიდ თიმურთან. ყველა ტური ინგლისურად, ჯგუფები 7 ადამიანამდე.",
"Private tours in Tbilisi and Georgia. Bespoke tours in English since 2023.":
"კერძო ტურები თბილისსა და საქართველოში. ინდივიდუალური ტურები ინგლისურად 2023 წლიდან.",
"An honest comparison of both formats for a trip to Georgia from Ufa.":
"ორივე ფორმატის პატიოსანი შედარება საქართველოში მოგზაურობისთვის უფადან.",
"“Wonderful excursion, thank you so much! Everything was top-notch.”":
"„შესანიშნავი ექსკურსია, დიდი მადლობა! ყველაფერი უმაღლეს დონეზე იყო.“",
"Tours to Georgia from Ufa 2026 — Direct Flight &amp; Private Tours":
"ტურები საქართველოში უფადან 2026 — პირდაპირი ფრენა და კერძო ტურები",
# --- метки ---
"Tours to Georgia from Ufa 2026 — flights, budget and routes":
"ტურები საქართველოში უფადან 2026 — ფრენები, ბიუჯეტი და მარშრუტები",
"Frequently Asked Questions about Tours to Georgia from Ufa":
"ხშირად დასმული კითხვები საქართველოში უფადან ტურებზე",
"Real traveller reviews on Google Maps · rated 4.9 out of 5":
"ნამდვილი მოგზაურების შეფასებები Google Maps-ზე · შეფასება 4.9 5-დან",
"Timur Sakhvadze · licensed guide, license №8247109128 ·":
"თიმურ სახვაძე · ლიცენზირებული გიდი, ლიცენზია №8247109128 ·",
"Tours to Georgia from Ufa 2026 — Direct Flights & Tours":
"ტურები საქართველოში უფადან 2026 — პირდაპირი ფრენები და ტურები",
"Tours to Georgia from Ufa 2026 — How to Plan Your Trip":
"ტურები საქართველოში უფადან 2026 — როგორ დავგეგმოთ მოგზაურობა",
"Essential info before your trip from Ufa to Georgia.":
"აუცილებელი ინფო უფადან საქართველოში მოგზაურობამდე.",
"How much does a 7-day trip to Georgia from Ufa cost?":
"რა ღირს 7-დღიანი მოგზაურობა საქართველოში უფადან?",
"Book your tours early — the best dates fill up fast":
"დაჯავშნეთ ტურები ადრე — საუკეთესო თარიღები სწრაფად ივსება",
"Direct Ufa–Tbilisi Flight: Airport, Days and Prices":
"პირდაპირი უფა–თბილისის რეისი: აეროპორტი, დღეები და ფასები",
"When is the best time to visit Georgia from Ufa?":
"როდის არის საქართველოს მონახულების საუკეთესო დრო უფადან?",
"— itineraries, prices and how to plan your trip":
"— მარშრუტები, ფასები და როგორ დავგეგმოთ მოგზაურობა",
"Georgia Itineraries from Ufa: 5, 7 and 10 Days":
"საქართველოს მარშრუტები უფადან: 5, 7 და 10 დღე",
"Which tours are must-do for visitors from Ufa?":
"რომელი ტურებია აუცილებელი უფადან ვიზიტორებისთვის?",
"“Everything went perfectly, highly recommend!”":
"„ყველაფერი იდეალურად ჩაიარა, ძალიან გირჩევთ!“",
"Arrival, check-in, stroll through Old Tbilisi":
"ჩამოსვლა, დარეგისტრირება, სეირნობა ძველ თბილისში",
"Do Russian citizens need a visa for Georgia?":
"სჭირდებათ რუსეთის მოქალაქეებს ვიზა საქართველოსთვის?",
"Night Tbilisi, dinner with a Georgian family":
"ღამის თბილისი, ვახშამი ქართულ ოჯახთან",
"Package Tour vs Self-Planned + Private Tour":
"პაკეტ-ტური vs დამოუკიდებელი + კერძო ტური",
"Tbilisi — Old Town, Narikala, evening walk":
"თბილისი — ძველი ქალაქი, ნარიყალა, საღამოს სეირნობა",
"— mountains, Gergeti Trinity Church (₾175)":
"— მთები, გერგეტის სამების ეკლესია (₾175)",
"Guide: 15 Places in Tbilisi + 5% discount":
"გზამკვლევი: 15 ადგილი თბილისში + 5% ფასდაკლება",
"Tours in Tbilisi — What to Book from Ufa":
"ტურები თბილისში — რა დავჯავშნოთ უფადან",
"Can I cancel a tour if my plans change?":
"შემიძლია ტურის გაუქმება თუ გეგმები შემეცვალა?",
"How to get to Tbilisi from Ufa in 2026?":
"როგორ მივიდეთ თბილისში უფადან 2026-ში?",
"In what language does guide Timur work?":
"რა ენაზე მუშაობს გიდი თიმური?",
"Practical Tips for Travellers from Ufa":
"პრაქტიკული რჩევები უფადან მოგზაურებისთვის",
"© 2026 Sakhva Travel. Tbilisi, Georgia":
"© 2026 Sakhva Travel. თბილისი, საქართველო",
"Are there direct flights Ufa–Tbilisi?":
"არის თუ არა პირდაპირი რეისები უფა–თბილისი?",
"Arrival, first impressions of Tbilisi":
"ჩამოსვლა, თბილისის პირველი შთაბეჭდილებები",
"Budget for a Trip to Georgia from Ufa":
"ბიუჯეტი საქართველოში მოგზაურობისთვის უფადან",
"Night Tbilisi, sulfur baths, Narikala":
"ღამის თბილისი, გოგირდის აბანოები, ნარიყალა",
"Tours to Georgia from other cities:":
"ტურები საქართველოში სხვა ქალაქებიდან:",
"Bashkir Honey and Georgian Wine":
"ბაშკირული თაფლი და ქართული ღვინო",
"What Ufa Travellers Should Know":
"რა უნდა იცოდნენ უფას მოგზაურებმა",
"How to Get to Georgia from Ufa":
"როგორ მივიდეთ საქართველოში უფადან",
"Tbilisi — free time, departure":
"თბილისი — თავისუფალი დრო, გამგზავრება",
"Your choice (apt/hotel/hostel)":
"თქვენი არჩევანი (ბინა/სასტუმრო/ჰოსტელი)",
"Do Mir cards work in Georgia?":
"მუშაობს Mir ბარათები საქართველოში?",
"— Jvari, Svetitskhoveli (₾98)":
"— ჯვარი, სვეტიცხოველი (₾98)",
"Market, souvenirs, departure":
"ბაზარი, სუვენირები, გამგზავრება",
"Guided tours (3 excursions)":
"ტურები გიდთან (3 ექსკურსია)",
"Self-planned + Private Tour":
"დამოუკიდებელი + კერძო ტური",
"Direct Flight in 2.5 Hours":
"პირდაპირი ფრენა 2.5 საათში",
"Mtskheta — Ancient Capital":
"მცხეთა — უძველესი დედაქალაქი",
"WhatsApp — reply in 15 min":
"WhatsApp — პასუხი 15 წუთში",
"5,500 RUB (hostel/Airbnb)":
"5,500 RUB (ჰოსტელი/Airbnb)",
"Almost the Same Time Zone":
"თითქმის იგივე დროის სარტყელი",
"Off-the-beaten-path sites":
"გზიდან გადახვეული ადგილები",
"Planning a trip from Ufa?":
"გეგმავთ მოგზაურობას უფადან?",
"Tours to Georgia from Ufa":
"ტურები საქართველოში უფადან",
"Two Cities of Coexistence":
"თანაარსებობის ორი ქალაქი",
"Accommodation (7 nights)":
"საცხოვრებელი (7 ღამე)",
"Old Tbilisi Walking Tour":
"ძველი თბილისის საფეხმავლო ტური",
"Ufa → Istanbul → Tbilisi":
"უფა → სტამბოლი → თბილისი",
"Why Choose Sakhva Travel":
"რატომ Sakhva Travel",
"— Prometheus Cave (₾183)":
"— პრომეთეს გამოქვაბული (₾183)",
"— wine, Sighnaghi (₾170)":
"— ღვინო, სიღნაღი (₾170)",
"3-star hotel (included)":
"3-ვარსკვლავიანი სასტუმრო (ჩათვლილი)",
"Sent — check your inbox":
"გაიგზავნა — შეამოწმეთ ფოსტა",
"all reviews on Google ↗":
"ყველა შეფასება Google-ზე ↗",
"✓ Free up to 24h before":
"✓ უფასო 24სთ-მდე",
"Email for subscription":
"ელფოსტა გამოწერისთვის",
"Ufa → Moscow → Tbilisi":
"უფა → მოსკოვი → თბილისი",
"Ufa → Tbilisi (direct)":
"უფა → თბილისი (პირდაპირი)",
"— national park (₾178)":
"— ეროვნული პარკი (₾178)",
"✗ Tourist circuit only":
"✗ მხოლოდ ტურისტული მარშრუტი",
"Accommodation quality":
"საცხოვრებლის ხარისხი",
"Aeroflot + connecting":
"Aeroflot + გადაჯდომა",
"Itinerary flexibility":
"მარშრუტის მოქნილობა",
"Book a tour from Ufa":
"დაჯავშნეთ ტური უფადან",
"Kazbegi from Tbilisi":
"ყაზბეგი თბილისიდან",
"Money &amp; Exchange":
"ფული და გადაცვლა",
"✗ Often mixed groups":
"✗ ხშირად შერეული ჯგუფები",
"+ Borjomi (₾98–178)":
"+ ბორჯომი (₾98–178)",
"🚗 Transfer included":
"🚗 ტრანსფერი ჩათვლილი",
"Night Tbilisi Tour":
"ღამის თბილისის ტური",
"Round-trip flights":
"ორმხრივი ფრენები",
"— Black Sea (₾250)":
"— შავი ზღვა (₾250)",
"— deep dive (₾100)":
"— ღრმა ჩაძირვა (₾100)",
"🍷 Tasting included":
"🍷 დეგუსტაცია ჩათვლილი",
"Kakheti Wine Tour":
"კახეთის ღვინის ტური",
"Market, departure":
"ბაზარი, გამგზავრება",
"Traveller reviews":
"მოგზაურების შეფასებები",
"Turkish / Pegasus":
"Turkish / Pegasus",
"✗ Fees up to 100%":
"✗ საკომისიო 100%-მდე",
"10-Day Itinerary":
"10-დღიანი მარშრუტი",
"Kutaisi Day Trip":
"ქუთაისის ერთდღიანი ტური",
"Leave a Review ★":
"დატოვეთ შეფასება ★",
"No Visa Required":
"ვიზა არ არის საჭირო",
"Round-trip Price":
"ორმხრივი ფასი",
"Total for 7 days":
"სულ 7 დღეზე",
"✗ Fixed schedule":
"✗ ფიქსირებული განრიგი",
"5-Day Itinerary":
"5-დღიანი მარშრუტი",
"7-Day Itinerary":
"7-დღიანი მარშრუტი",
"Cost for 7 days":
"ღირებულება 7 დღეზე",
"Local transport":
"ადგილობრივი ტრანსპორტი",
"✓ Custom routes":
"✓ ინდივიდუალური მარშრუტები",
"up to 7 people":
"7 ადამიანამდე",
"✓ English only":
"✓ მხოლოდ ინგლისური",
"✓ Full freedom":
"✓ სრული თავისუფლება",
"🚗 From Tbilisi":
"🚗 თბილისიდან",
"🚶 Walking tour":
"🚶 საფეხმავლო ტური",
"Direct flight":
"პირდაპირი ფრენა",
"Night Tbilisi":
"ღამის თბილისი",
"Tour language":
"ტურის ენა",
"20–40 people":
"20–40 ადამიანი",
"Cancellation":
"გაუქმება",
"Package Tour":
"პაკეტ-ტური",
"About Guide":
"გიდის შესახებ",
"Best Seller":
"ბესტსელერი",
"Flight, RUB":
"ფრენა, RUB",
"RU passport":
"რუსული პასპორტი",
"Timur's Tip":
"თიმურის რჩევა",
"Mid-range":
"საშუალო კლასი",
"Parameter":
"პარამეტრი",
"Transport":
"ტრანსპორტი",
"Visa-free":
"უვიზო",
"🌙 Evening":
"🌙 საღამო",
"Old Town":
"ძველი ქალაქი",
"SIM Card":
"SIM-ბარათი",
"/person":
"/ადამიანი",
"Airline":
"ავიახაზი",
"Borjomi":
"ბორჯომი",
"Comfort":
"კომფორტი",
"Details":
"დეტალები",
"Evening":
"საღამო",
"Expense":
"ხარჯი",
"Russian":
"რუსული",
"Get it":
"მიიღეთ",
"Useful":
"სასარგებლო",
"Terms":
"პირობები",
"Food":
"საკვები",
"Tip:":
"რჩევა:",
"Wine":
"ღვინო",
"Group size":
"ჯგუფის ზომა",
"Tours from":
"ტურები ქალაქიდან",
"from 14.5K":
"14.5K-დან",
}
# города (from X → Xდან)
CITY = {"Moscow":"მოსკოვიდან","St. Petersburg":"სანქტ-პეტერბურგიდან","Yekaterinburg":"ეკატერინბურგიდან",
"Novosibirsk":"ნოვოსიბირსკიდან","Kazan":"ყაზანიდან","Nizhny Novgorod":"ნიჟნი ნოვგოროდიდან",
"Chelyabinsk":"ჩელიაბინსკიდან","Samara":"სამარადან","Rostov":"როსტოვიდან","Krasnodar":"კრასნოდარიდან",
"Sochi":"სოჭიდან","Mineralnye Vody":"მინერალნიე ვოდიდან","Pyatigorsk":"პიატიგორსკიდან",
"Kislovodsk":"კისლოვოდსკიდან","Stavropol":"სტავროპოლიდან","Nalchik":"ნალჩიკიდან",
"Vladikavkaz":"ვლადიკავკაზიდან","Makhachkala":"მახაჩკალადან","Volgograd":"ვოლგოგრადიდან",
"Saratov":"სარატოვიდან","Voronezh":"ვორონეჟიდან","Perm":"პერმიდან","Tyumen":"ტიუმენიდან",
"Kazakhstan":"ყაზახეთიდან","Tashkent":"ტაშკენტიდან","Minsk":"მინსკიდან","Yerevan":"ერევანიდან"}
for c, ka in CITY.items():
    L[f"from {c}"] = ka
# дни, часы, from-цены
for n in range(1, 9): L[f"Day {n}:"] = f"დღე {n}:"
L["Days 1–2:"] = "დღეები 1–2:"; L["Days 9–10:"] = "დღეები 9–10:"
for a in ["2–3","3–4","10–12","12–13"]: L[f"⏲ {a} hours"] = f"⏲ {a} საათი"
for n in ["12,000","19,000","22,000","24,000"]: L[f"from {n} RUB"] = f"{n} RUB-დან"

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
