#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод EN->KA пилот-страницы /ge/about/. Анкер-замены + счётчик."""
import sys
from pathlib import Path
F = Path("/Users/vladimir/sakhva-travel/ge/about/index.html")

R = [
# TITLE / META / OG / TWITTER
("Timur — Georgia Tour Author | Sakhva Travel", "თიმური — ტურების ავტორი საქართველოში | Sakhva Travel", 3),
("Timur — private Russian & English-speaking guide in Tbilisi since 2023. 500+ tours, 4.9/5 rating from 90+ reviews. Kazbegi, Kakheti, Kutaisi. Groups up to 7.",
 "თიმური — კერძო რუსულ- და ინგლისურენოვანი გიდი თბილისში 2023 წლიდან. 500+ ტური, რეიტინგი 4.9/5 90+ შეფასებით. ყაზბეგი, კახეთი, ქუთაისი. ჯგუფები 7 ადამიანამდე.", 1),
("Private tour Timur. 500+ tours across Georgia. 4.9/5 rating from 90+ reviews. Kazbegi, Kakheti, Tbilisi. Groups up to 7.",
 "ინდივიდუალური ტური თიმურთან. 500+ ტური მთელ საქართველოში. რეიტინგი 4.9/5 90+ შეფასებით. ყაზბეგი, კახეთი, თბილისი. ჯგუფები 7 ადამიანამდე.", 1),
("Timur — Private Tour in Tbilisi | Sakhva Travel", "თიმური — ინდივიდუალური ტური თბილისში | Sakhva Travel", 2),  # og:image:alt + ProfilePage name
("500+ tours, 4.9/5 rating. Kazbegi, Kakheti, Tbilisi. Groups up to 7.",
 "500+ ტური, რეიტინგი 4.9/5. ყაზბეგი, კახეთი, თბილისი. ჯგუფები 7 ადამიანამდე.", 1),
("content=\"Timur, Sakhva Travel\"", "content=\"თიმური, Sakhva Travel\"", 1),
# SCHEMA @graph
("Biography and experience of guide Timur in Georgia. 500+ tours, 4.9/5 rating.",
 "გიდ თიმურის ბიოგრაფია და გამოცდილება საქართველოში. 500+ ტური, რეიტინგი 4.9/5.", 1),
("\"name\":\"Home\"", "\"name\":\"მთავარი\"", 1),
("\"name\":\"Guide Timur\"", "\"name\":\"გიდი თიმური\"", 1),
("\"jobTitle\":\"Private Tour in Georgia\"", "\"jobTitle\":\"ინდივიდუალური ტური საქართველოში\"", 1),
("Private tours in Tbilisi since 2023. 500+ tours for tourists, expats and digital nomads. Languages: Russian, English. Groups up to 7 people.",
 "ინდივიდუალური ტურები თბილისში 2023 წლიდან. 500+ ტური ტურისტების, ექსპატებისა და ციფრული მომთაბარეებისთვის. ენები: რუსული, ინგლისური. ჯგუფები 7 ადამიანამდე.", 1),
("Лицензия гида Грузии / Georgia Tour Guide Licence", "საქართველოს გიდის ლიცენზია", 1),
# FAQ schema
("How many tours has Timur conducted?", "რამდენი ტური ჩაატარა თიმურმა?", 1),
("Over 500 tours since 2023. Rated 4.9/5 based on 87 Google reviews.",
 "500-ზე მეტი ტური 2023 წლიდან. რეიტინგი 4.9/5 87 Google-შეფასების საფუძველზე.", 1),
("What languages does Timur speak?", "რომელ ენებზე საუბრობს თიმური?", 1),
("Timur conducts tours in Russian and English.", "თიმური ტურებს ატარებს რუსულ და ინგლისურ ენებზე.", 1),
("How to book a tour with Timur?", "როგორ დავჯავშნო ტური თიმურთან?", 1),
("Message on WhatsApp +995 511 272 623 or Telegram @SakhvaGuideBot. Response within 15 minutes, daily 08:00-22:00.",
 "მომწერეთ WhatsApp-ზე +995 511 272 623 ან Telegram-ზე @SakhvaGuideBot. პასუხი 15 წუთში, ყოველდღე 08:00-22:00.", 1),
("What is the maximum group size?", "რა არის ჯგუფის მაქსიმალური ზომა?", 1),
("Maximum 7 people. Private format only — no bus tours.", "მაქსიმუმ 7 ადამიანი. მხოლოდ ინდივიდუალური ფორმატი — არანაირი ავტობუსური ტური.", 1),
# NAV / DRAWER
(">Tours in Georgia<", ">ტურები საქართველოში<", 2),
(">Excursions<", ">ექსკურსიები<", 2),
(">Prices<", ">ფასები<", 1),
(">About<", ">ჩვენ შესახებ<", 2),
(">Reviews<", ">შეფასებები<", 2),
(">Blog<", ">ბლოგი<", 3),  # nav + drawer + footer <h4>? no: nav+drawer+footer link
(">FAQ<", ">FAQ<", 2),  # аббревиатура остаётся
(">Contacts<", ">კონტაქტები<", 2),
(">Book Now</a>", ">დაჯავშნა</a>", 2),
("aria-label=\"Menu\"", "aria-label=\"მენიუ\"", 1),
# HERO
("Home</span>", "მთავარი</span>", 1),
(">Guide Timur</span>", ">გიდი თიმური</span>", 1),
(">Private Tour · Tbilisi</div>", ">ინდივიდუალური ტური · თბილისი</div>", 1),
("Timur — your guide in Georgia", "თიმური — თქვენი გიდი საქართველოში", 1),
("English & Russian-speaking guide since 2023 · Tbilisi, Georgia",
 "ინგლისურ- და რუსულენოვანი გიდი 2023 წლიდან · თბილისი, საქართველო", 1),
("I show Georgia the way locals see it — no tourist scripts, no crowded buses. Kazbegi, Kakheti, hidden courtyards of Tbilisi, Soviet mosaics — every tour is built around you.",
 "საქართველოს ისე გაჩვენებთ, როგორც მას ადგილობრივები ხედავენ — ტურისტული შაბლონებისა და ხალხმრავალი ავტობუსების გარეშე. ყაზბეგი, კახეთი, თბილისის დამალული ეზოები, საბჭოთა მოზაიკები — ყოველი ტური თქვენ ირგვლივ იგება.", 1),
("<span class=\"stat-lbl\">tours completed</span>", "<span class=\"stat-lbl\">ჩატარებული ტური</span>", 1),
("<span class=\"stat-lbl\">rating (90+ reviews)</span>", "<span class=\"stat-lbl\">რეიტინგი (90+ შეფასება)</span>", 1),
("<span class=\"stat-num\">up to 7</span>", "<span class=\"stat-num\">7-მდე</span>", 1),
("<span class=\"stat-lbl\">people per group</span>", "<span class=\"stat-lbl\">ადამიანი ჯგუფში</span>", 1),
("<span class=\"stat-num\">since 2023</span>", "<span class=\"stat-num\">2023 წლიდან</span>", 1),
("<span class=\"stat-lbl\">working as guide</span>", "<span class=\"stat-lbl\">გიდის საქმიანობა</span>", 1),
("          Message on WhatsApp", "          მოგვწერეთ WhatsApp-ზე", 1),
(">All Tours →</a>", ">ყველა ტური →</a>", 1),
("alt=\"Timur — Georgia tour author, Georgia\"", "alt=\"თიმური — ტურების ავტორი საქართველოში\"", 1),
# ABOUT ME
(">About Me</div>", ">ჩემ შესახებ</div>", 1),
("Tbilisi is my city", "თბილისი ჩემი ქალაქია", 1),
("I grew up in Tbilisi in the 90s — watched the city transform, heard stories from grandmothers in courtyard wells, know where the best wine is made and where you can have a heartfelt conversation with locals. My routes aren't from Lonely Planet — they're a map of a living city.",
 "თბილისში გავიზარდე 90-იან წლებში — ვნახე, როგორ იცვლებოდა ქალაქი, მოვისმინე ბებიების ამბები ეზოს ჭებთან, ვიცი, სად მზადდება საუკეთესო ღვინო და სად შეიძლება გულახდილი საუბარი ადგილობრივებთან. ჩემი მარშრუტები Lonely Planet-იდან არ არის — ეს ცოცხალი ქალაქის რუკაა.", 1),
("There's a cafe in Avlabari with no sign — they make the best khinkali I know. It's not in any guidebook. Or a courtyard on Kote Abkhazi with Soviet-era graffiti that most tourists walk right past. These are exactly the places I show my guests.",
 "ავლაბარში არის კაფე უაბრაოდ — იქ ისეთ ხინკალს აკეთებენ, საუკეთესოს, რაც ვიცი. ის არცერთ გზამკვლევში არ არის. ან ეზო კოტე აფხაზის ქუჩაზე საბჭოთა პერიოდის გრაფიტით, რომელსაც ტურისტების უმეტესობა უბრალოდ ჩაუვლის ხოლმე. სწორედ ასეთ ადგილებს ვაჩვენებ ჩემს სტუმრებს.", 1),
("Tourism isn't just a job. When I see someone looking at Mount Kazbek and their breath catches — I know I'm doing everything right. Over three years I've conducted more than 500 tours for tourists, expats, digital nomads and families with children.",
 "ტურიზმი უბრალოდ სამსახური არ არის. როცა ვხედავ, როგორ უყურებს ვინმე მყინვარწვერს და სუნთქვა ეკვრება — ვიცი, რომ ყველაფერს სწორად ვაკეთებ. სამ წელიწადში 500-ზე მეტი ტური ჩავატარე ტურისტების, ექსპატების, ციფრული მომთაბარეებისა და ბავშვებიანი ოჯახებისთვის.", 1),
("I only work with small groups — up to 7 people. No bus tours with 40 strangers. Just personal attention and a flexible route tailored to you. I speak Russian and English — no language barrier for any guest.",
 "ვმუშაობ მხოლოდ მცირე ჯგუფებთან — 7 ადამიანამდე. არანაირი ავტობუსური ტური 40 უცხო ადამიანთან ერთად. მხოლოდ პერსონალური ყურადღება და მოქნილი მარშრუტი, თქვენზე მორგებული. ვსაუბრობ რუსულად და ინგლისურად — არცერთ სტუმართან ენობრივი ბარიერი არ არის.", 1),
# MY APPROACH
(">My Approach</div>", ">ჩემი მიდგომა</div>", 1),
("How I work", "როგორ ვმუშაობ", 1),
("I respond on WhatsApp within 15 minutes. Pay on the day of the tour in cash or by card. Free cancellation 24 hours before, no questions asked.",
 "WhatsApp-ზე ვპასუხობ 15 წუთში. გადახდა ტურის დღეს, ნაღდით ან ბარათით. უფასო გაუქმება 24 საათით ადრე, ზედმეტი კითხვების გარეშე.", 1),
("Bad weather for Kazbegi? We'll reschedule for free. Want to add sulphur baths or visit a family restaurant with no menu? No problem — the route is flexible. I don't follow a rigid script: if you want to stay 20 minutes longer at a viewpoint — we stay.",
 "ცუდი ამინდი ყაზბეგისთვის? უფასოდ გადავიტანთ სხვა დღეს. გინდათ დაამატოთ გოგირდის აბანოები ან ეწვიოთ საოჯახო რესტორანს მენიუს გარეშე? პრობლემა არ არის — მარშრუტი მოქნილია. მკაცრ სცენარს არ ვიცავ: თუ გინდათ სანახაობის წერტილში 20 წუთით მეტხანს დარჩენა — დავრჩებით.", 1),
("Before each tour I send a detailed route plan with clothing and footwear recommendations. On the day I meet you at the agreed location — no taxi rides to a meeting point at 6 AM.",
 "ყოველი ტურის წინ ვგზავნი დეტალურ მარშრუტის გეგმას ტანსაცმლისა და ფეხსაცმლის რეკომენდაციებით. ტურის დღეს გხვდებით შეთანხმებულ ადგილას — არანაირი ტაქსით გამგზავრება შეხვედრის ადგილამდე დილის 6 საათზე.", 1),
("I work daily from 08:00 to 22:00, including holidays and weekends. In three years, not a single tour has been cancelled due to my fault.",
 "ვმუშაობ ყოველდღე 08:00-დან 22:00-მდე, დღესასწაულებისა და შაბათ-კვირის ჩათვლით. სამ წელიწადში არცერთი ტური არ გაუქმებულა ჩემი ბრალით.", 1),
# VALUES
(">Up to 7 people</div>", ">7 ადამიანამდე</div>", 1),
("No buses. Private format only — personal attention for everyone.", "არანაირი ავტობუსი. მხოლოდ ინდივიდუალური ფორმატი — პერსონალური ყურადღება ყველასთვის.", 1),
(">Reply in 15 minutes</div>", ">პასუხი 15 წუთში</div>", 1),
("Message on WhatsApp or Telegram — I'll reply quickly and help you choose a tour.", "მომწერეთ WhatsApp-ზე ან Telegram-ზე — სწრაფად გიპასუხებთ და ტურის არჩევაში დაგეხმარებით.", 1),
(">Pay on tour day</div>", ">გადახდა ტურის დღეს</div>", 1),
(">Free cancellation 24 hours before.</div>", ">უფასო გაუქმება 24 საათით ადრე.</div>", 1),
(">Kazbegi flexibility</div>", ">მოქნილობა ყაზბეგზე</div>", 1),
("Bad weather? Free reschedule with no penalties.", "ცუდი ამინდი? უფასო გადატანა ჯარიმების გარეშე.", 1),
(">Flexible route</div>", ">მოქნილი მარშრუტი</div>", 1),
("The itinerary can be adjusted on the go — I'm not in a rush.", "მარშრუტის კორექტირება შესაძლებელია გზადაგზა — არსად ვჩქარობ.", 1),
(">4.9/5 rating</div>", ">რეიტინგი 4.9/5</div>", 1),
("90+ reviews on Google and TripAdvisor. Honest ratings, no fakes.", "90+ შეფასება Google-სა და TripAdvisor-ზე. გულწრფელი შეფასებები, ყალბის გარეშე.", 1),
# TEAM
(">Team</div>", ">გუნდი</div>", 1),
("Sakhva Travel guides", "Sakhva Travel-ის გიდები", 1),
("alt=\"Timur Sakhvadze — guide for Kazbegi and Kakheti\"", "alt=\"თიმურ სახვაძე — ყაზბეგისა და კახეთის გიდი\"", 1),
(">Timur Sakhvadze</div>", ">თიმურ სახვაძე</div>", 1),
("Founder · Kazbegi, Kakheti, Tbilisi", "დამფუძნებელი · ყაზბეგი, კახეთი, თბილისი", 1),
("Licensed guide (No. 8247109128), 500+ tours since 2023. English, Russian.",
 "ლიცენზირებული გიდი (№8247109128), 500+ ტური 2023 წლიდან. ინგლისური, რუსული.", 1),
(">More about Timur →</span>", ">მეტი თიმურის შესახებ →</span>", 1),
("alt=\"Saba — guide for Batumi and Svaneti\"", "alt=\"საბა — ბათუმისა და სვანეთის გიდი\"", 1),
(">Saba Skhavadze</div>", ">საბა სხავაძე</div>", 1),
("Guide · Batumi, Adjara, Svaneti", "გიდი · ბათუმი, აჭარა, სვანეთი", 1),
("Licensed guide (No. 9332412411), 10 years of experience. English, Russian, Georgian.",
 "ლიცენზირებული გიდი (№9332412411), 10 წლის გამოცდილება. ინგლისური, რუსული, ქართული.", 1),
(">More about Saba →</span>", ">მეტი საბას შესახებ →</span>", 1),
# TIMELINE
(">Experience</div>", ">გამოცდილება</div>", 1),
("Guide's journey", "გიდის გზა", 1),
("First tours and Sakhva Travel launch", "პირველი ტურები და Sakhva Travel-ის დაარსება", 1),
("Started with Tbilisi tours for Russian-speaking tourists and expats. First 50 tours — and first 5-star Google reviews. Main audience: people who recently relocated and wanted to understand the city from the inside.",
 "დავიწყე თბილისის ტურებით რუსულენოვანი ტურისტებისა და ექსპატებისთვის. პირველი 50 ტური — და პირველი 5-ვარსკვლავიანი შეფასებები Google-ზე. მთავარი აუდიტორია: ადამიანები, ვინც ახლახან გადმოსახლდა და უნდოდა ქალაქის შიგნიდან შეცნობა.", 1),
("Expansion: Kazbegi and Kakheti", "გაფართოება: ყაზბეგი და კახეთი", 1),
("Added day trips — Georgian Military Highway, Gergeti Trinity Church at 2,170m, Sighnaghi and qvevri wine tastings. Over 200 tours in a year. First guests from the US and Germany — switched to bilingual format (RU/EN).",
 "დავამატე ერთდღიანი ტურები — საქართველოს სამხედრო გზა, გერგეტის სამების ეკლესია 2170მ სიმაღლეზე, სიღნაღი და ქვევრის ღვინის დეგუსტაციები. წელიწადში 200-ზე მეტი ტური. პირველი სტუმრები აშშ-დან და გერმანიიდან — გადავედი ორენოვან ფორმატზე (RU/EN).", 1),
("Specialized tours and 400+ completed", "სპეციალიზებული ტურები და 400+ ჩატარებული", 1),
("Launched tours for digital nomads, Soviet Tbilisi, Night Tbilisi, 3-day Slow Travel package, and Tour + Photoshoot. Passed the 400-tour milestone. Launched a Telegram bot for bookings.",
 "გავუშვი ტურები ციფრული მომთაბარეებისთვის, საბჭოთა თბილისი, ღამის თბილისი, 3-დღიანი Slow Travel პაკეტი და ტური + ფოტოსესია. გადავლახე 400 ტურის ზღვარი. ავამუშავე Telegram-ბოტი დაჯავშნისთვის.", 1),
("500+ tours and 4.9/5 rating", "500+ ტური და რეიტინგი 4.9/5", 1),
("Over 500 tours completed. 87 verified reviews, average rating 4.9 out of 5. 11 unique itineraries in the lineup. Sakhva Travel — one of the highest-rated private tours in Tbilisi according to Google Maps.",
 "500-ზე მეტი ჩატარებული ტური. 87 დადასტურებული შეფასება, საშუალო რეიტინგი 4.9 5-დან. 11 უნიკალური მარშრუტი არჩევანში. Sakhva Travel — ერთ-ერთი ყველაზე მაღალშეფასებული ინდივიდუალური ტური თბილისში Google Maps-ის მიხედვით.", 1),
# REVIEWS
(">What guests say</div>", ">რას ამბობენ სტუმრები</div>", 1),
("Reviews about Timur", "შეფასებები თიმურზე", 1),
("\"Timur is the best guide I've ever traveled with. Kazbegi exceeded all expectations. Small group, engaging stories, not a single dull moment.\"",
 "„თიმური საუკეთესო გიდია, ვისთანაც კი მიმოგზაურია. ყაზბეგმა ყველა მოლოდინს გადააჭარბა. მცირე ჯგუფი, საინტერესო ამბები, არცერთი მოსაწყენი წუთი.“", 1),
("Anna K. — Moscow, Kazbegi tour", "ანა კ. — მოსკოვი, ტური ყაზბეგში", 1),
("\"We moved to Tbilisi six months ago and only truly saw the city with Timur. The expat tour is a must-have for everyone who just arrived.\"",
 "„თბილისში ნახევარი წლის წინ გადმოვსახლდით და ქალაქი ნამდვილად მხოლოდ თიმურთან ერთად ვნახეთ. ექსპატ-ტური აუცილებელია ყველასთვის, ვინც ახლახან ჩამოვიდა.“", 1),
("Dmitry R. — expat from Saint Petersburg", "დმიტრი რ. — ექსპატი სანქტ-პეტერბურგიდან", 1),
("\"Kakheti with Timur isn't a tour — it's a story. Lunch with a local family, wine straight from a qvevri, Bodbe Monastery — everything was perfect.\"",
 "„კახეთი თიმურთან ერთად ტური კი არა — ამბავია. სადილი ადგილობრივ ოჯახთან, ღვინო პირდაპირ ქვევრიდან, ბოდბის მონასტერი — ყველაფერი იდეალური იყო.“", 1),
("Maria L. — Almaty, Kakheti tour", "მარია ლ. — ალმათი, ტური კახეთში", 1),
# FAQ visible
(">Q&A</div>", ">კითხვა-პასუხი</div>", 1),
("Frequently asked questions about the guide", "ხშირად დასმული კითხვები გიდზე", 1),
("Who is Timur and how long has he been a guide?", "ვინ არის თიმური და რამდენი ხანია გიდობს?", 1),
("Timur is a private tours in Tbilisi, Georgia, working since 2023. He has conducted over 500 tours for tourists from Russia, Ukraine, Belarus, Kazakhstan, as well as travelers from the US, Germany and other countries. Timur grew up in Tbilisi, knows the city inside out, and speaks Russian and English.",
 "თიმური არის კერძო გიდი თბილისში, საქართველოში, მუშაობს 2023 წლიდან. მან 500-ზე მეტი ტური ჩაატარა ტურისტებისთვის რუსეთიდან, უკრაინიდან, ბელარუსიდან, ყაზახეთიდან, ასევე მოგზაურებისთვის აშშ-დან, გერმანიიდან და სხვა ქვეყნებიდან. თიმური თბილისში გაიზარდა, ქალაქს ბოლომდე იცნობს და საუბრობს რუსულად და ინგლისურად.", 1),
("What tours does Timur offer?", "რა ტურებს სთავაზობს თიმური?", 1),
("Timur offers 11 unique itineraries: Kazbegi Day Trip, Sighnaghi & Kakheti, Mtskheta & Jvari, Hidden Tbilisi, Kutaisi, Soviet Tbilisi, Night Tbilisi, Batumi, Digital Nomad Tbilisi, Tour + Photoshoot, and 3-Day Slow Travel. All tours are in small groups of up to 7 people.",
 "თიმური გთავაზობთ 11 უნიკალურ მარშრუტს: ერთდღიანი ტური ყაზბეგში, სიღნაღი და კახეთი, მცხეთა და ჯვარი, დამალული თბილისი, ქუთაისი, საბჭოთა თბილისი, ღამის თბილისი, ბათუმი, ციფრული მომთაბარის თბილისი, ტური + ფოტოსესია და 3-დღიანი Slow Travel. ყველა ტური მცირე ჯგუფებში, 7 ადამიანამდე.", 1),
("How does payment work?", "როგორ ხდება გადახდა?", 1),
("Payment is made on the day of the tour — cash (GEL or EUR) or card. Free cancellation is available 24 hours before without any fees or explanations.",
 "გადახდა ხდება ტურის დღეს — ნაღდი ფული (ლარი ან ევრო) ან ბარათი. უფასო გაუქმება შესაძლებელია 24 საათით ადრე, ყოველგვარი საფასურისა და ახსნა-განმარტების გარეშე.", 1),
("How to contact the guide for booking?", "როგორ დავუკავშირდე გიდს დასაჯავშნად?", 1),
("The quickest way is WhatsApp at +995 511 272 623. Timur responds within 15 minutes on average. You can also message on Telegram via ",
 "ყველაზე სწრაფი გზაა WhatsApp: +995 511 272 623. თიმური საშუალოდ 15 წუთში პასუხობს. ასევე შეგიძლიათ მოწეროთ Telegram-ზე: ", 1),
(">@SakhvaGuideBot</a>. Working hours: daily 08:00-22:00, including holidays.",
 ">@SakhvaGuideBot</a>. სამუშაო საათები: ყოველდღე 08:00-22:00, დღესასწაულების ჩათვლით.", 1),
# PROFILES
(">Find us</div>", ">სად მოგვძებნით</div>", 1),
("Guide profiles and reviews", "გიდის პროფილები და შეფასებები", 1),
("All reviews about Timur are verified, from real guests. Check profiles on independent platforms:",
 "ყველა შეფასება თიმურზე დადასტურებულია, რეალური სტუმრებისგან. იხილეთ პროფილები დამოუკიდებელ პლატფორმებზე:", 1),
("@sakhvatravel — tour photos & reviews", "@sakhvatravel — ტურების ფოტოები და შეფასებები", 1),
("@SakhvaGuideBot — quick booking", "@SakhvaGuideBot — სწრაფი დაჯავშნა", 1),
("+995 511 272 623 — message now", "+995 511 272 623 — მოგვწერეთ ახლავე", 1),
# TOURS CTA
(">Book a Tour</div>", ">დაჯავშნე ტური</div>", 1),
("Choose your tour with Timur", "აირჩიე შენი ტური თიმურთან ერთად", 1),
("All tours in small groups up to 7 people.", "ყველა ტური მცირე ჯგუფებში, 7 ადამიანამდე.", 1),
(">Kazbegi Day Trip</div>", ">ერთდღიანი ტური ყაზბეგში</div>", 1),
("from ₾175/person · 14h", "₾175-დან/ადამიანი · 14სთ", 1),
(">Night Tbilisi</div>", ">ღამის თბილისი</div>", 1),
("from ₾100/person · 4h", "₾100-დან/ადამიანი · 4სთ", 1),
(">Sighnaghi & Kakheti</div>", ">სიღნაღი და კახეთი</div>", 1),
("from ₾170/person · 10-12h", "₾170-დან/ადამიანი · 10-12სთ", 1),
(">Batumi</div>", ">ბათუმი</div>", 1),
("from ₾250/person · 15h", "₾250-დან/ადამიანი · 15სთ", 1),
(">Kutaisi</div>", ">ქუთაისი</div>", 1),
("from ₾183/person · 12-13h", "₾183-დან/ადამიანი · 12-13სთ", 1),
(">Slow Travel 3 Days</div>", ">Slow Travel 3 დღე</div>", 1),
("from ₾595/person · 3 days", "₾595-დან/ადამიანი · 3 დღე", 1),
# FOOTER
("Private tours in Tbilisi. Kazbegi, Kakheti, hidden gems. Up to 7 people per group.",
 "ინდივიდუალური ტურები თბილისში. ყაზბეგი, კახეთი, დამალული მარგალიტები. 7 ადამიანამდე ჯგუფში.", 1),
("<h4>Tours</h4>", "<h4>ტურები</h4>", 1),
(">Kazbegi — from ₾175</a>", ">ყაზბეგი — ₾175-დან</a>", 1),
(">Night Tbilisi — from ₾100</a>", ">ღამის თბილისი — ₾100-დან</a>", 1),
(">Kakheti — from ₾170</a>", ">კახეთი — ₾170-დან</a>", 1),
(">Batumi — from ₾250</a>", ">ბათუმი — ₾250-დან</a>", 1),
("<h4>Contact</h4>", "<h4>კონტაქტი</h4>", 1),
("© 2026 Sakhva Travel · Tbilisi, Georgia", "© 2026 Sakhva Travel · თბილისი, საქართველო", 1),
(">Privacy</a>", ">კონფიდენციალურობა</a>", 1),
(">Guide Timur</a>", ">გიდი თიმური</a>", 1),
]

def main():
    html = F.read_text(encoding="utf-8")
    problems = []
    for i, (old, new, *exp) in enumerate(R):
        want = exp[0] if exp else 1
        cnt = html.count(old)
        if cnt != want:
            problems.append(f"[{i}] ожидал {want}, нашёл {cnt}: {old[:60]!r}")
            continue
        html = html.replace(old, new)
    if problems:
        print("СТОП — расхождения, файл НЕ записан:")
        for p in problems: print("  ", p)
        sys.exit(1)
    F.write_text(html, encoding="utf-8")
    print(f"OK: применено {len(R)} замен")

if __name__ == "__main__":
    main()
