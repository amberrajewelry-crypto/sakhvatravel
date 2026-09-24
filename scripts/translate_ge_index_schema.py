#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод естественно-языковых значений JSON-LD графа главной GE.
Парсит единственный @graph, переводит значения ключей name/description/text/
reviewBody/headline по точному словарю TRANS, сериализует обратно компактно.
Структуру (@type/@id/URL/числа/inLanguage) НЕ трогает. Имена людей и бренды
остаются латиницей (в TRANS не входят). Идемпотентно: повторный запуск не портит."""
import re, json, sys

FILE = "ge/index.html"

TRANS = {
 # --- WebSite / business / WebPage ---
 "Private tour guide in Georgia. Kazbegi, Kakheti, hidden gems of Tbilisi. Up to 7 people.":
   "კერძო გიდი საქართველოში. ყაზბეგი, კახეთი, თბილისის ფარული ადგილები. მაქსიმუმ 7 ადამიანი.",
 "Private Tour in Tbilisi ★4.9 | Sakhva Travel":
   "კერძო ტური თბილისში ★4.9 | Sakhva Travel",
 "Private tour Timur. Kazbegi from ₾175, hidden Tbilisi from ₾98, Kakheti. Up to 7 people. Free cancellation. Reply in 15 minutes.":
   "კერძო ტური თიმურთან. ყაზბეგი ₾175-დან, ფარული თბილისი ₾98-დან, კახეთი. მაქსიმუმ 7 ადამიანი. უფასო გაუქმება. პასუხი 15 წუთში.",
 # --- toponyms (Place name) ---
 "Tbilisi": "თბილისი",
 "Kazbegi": "ყაზბეგი",
 "Kakheti": "კახეთი",
 "Georgia": "საქართველო",
 # --- guide Person ---
 "Professional tour guide in Tbilisi since 2023. Conducts tours to Kazbegi, Kakheti, and hidden spots of Tbilisi.":
   "პროფესიონალი გიდი თბილისში 2023 წლიდან. ატარებს ტურებს ყაზბეგში, კახეთსა და თბილისის ფარულ ადგილებში.",
 "Лицензия гида Грузии / Georgia Tour Guide Licence":
   "საქართველოს გიდის ლიცენზია",
 # --- TouristTrip name + description ---
 "Kazbegi Day Trip from Tbilisi": "ერთდღიანი ტური ყაზბეგში თბილისიდან",
 "Georgian Military Highway, Ananuri fortress, Gergeti Trinity Church with views of Mt Kazbek 5047m.":
   "საქართველოს სამხედრო გზა, ანანურის ციხე, გერგეტის სამების ეკლესია მყინვარწვერის ხედით (5047 მ).",
 "Sighnaghi & Kakheti Wine Tour": "სიღნაღი და კახეთის ღვინის ტური",
 "City of Love, Bodbe Monastery, qvevri wine, lunch with locals. 10-12 hours.":
   "სიყვარულის ქალაქი, ბოდბის მონასტერი, ქვევრის ღვინო, სადილი ადგილობრივებთან. 10-12 საათი.",
 "Kutaisi Day Trip from Tbilisi": "ერთდღიანი ტური ქუთაისში თბილისიდან",
 "Bagrati Cathedral, Okatse Canyon, Prometheus Cave and Kinchkha Waterfall. 12-13 hours with a private tour.":
   "ბაგრატის ტაძარი, ოკაცეს კანიონი, პრომეთეს მღვიმე და კინჩხის ჩანჩქერი. 12-13 საათი კერძო ტურით.",
 "Batumi Day Trip from Tbilisi": "ერთდღიანი ტური ბათუმში თბილისიდან",
 "Batumi Boulevard, Old Town, cable car and seaside promenade. Black Sea pearl of Georgia in one day.":
   "ბათუმის ბულვარი, ძველი ქალაქი, საბაგირო და ზღვისპირა სასეირნო. საქართველოს შავი ზღვის მარგალიტი ერთ დღეში.",
 "Night Tbilisi Tour": "ღამის თბილისის ტური",
 "Sulfur baths by candlelight, illuminated Bridge of Peace, courtyard dinner. Starts at 20:00, 2.5 hours.":
   "გოგირდის აბანოები სანთლების შუქზე, განათებული მშვიდობის ხიდი, ვახშამი ეზოში. დაწყება 20:00-ზე, 2.5 საათი.",
 "Food Tour & Dinner with Locals": "გასტრო-ტური და ვახშამი ადგილობრივებთან",
 "Walking tour + home dinner with Georgian family: khinkali, qvevri wine, authentic conversation. 6-7 hours.":
   "ფეხით ტური + სახლის ვახშამი ქართულ ოჯახთან: ხინკალი, ქვევრის ღვინო, ავთენტური საუბარი. 6-7 საათი.",
 "Tbilisi City Tour": "თბილისის ქალაქის ტური",
 "Bridge of Peace, Abanotubani sulfur baths, Metekhi, Sameba, Freedom Square, Mtatsminda. 4-5 hours.":
   "მშვიდობის ხიდი, აბანოთუბნის გოგირდის აბანოები, მეტეხი, სამება, თავისუფლების მოედანი, მთაწმინდა. 4-5 საათი.",
 "Mtskheta Tour from Tbilisi": "მცხეთის ტური თბილისიდან",
 "Jvari Monastery, Svetitskhoveli Cathedral — UNESCO sites 40 minutes from Tbilisi. 3-4 hours.":
   "ჯვრის მონასტერი, სვეტიცხოვლის ტაძარი — UNESCO-ს ძეგლები თბილისიდან 40 წუთში. 3-4 საათი.",
 "Digital Nomad Tour Tbilisi": "ციფრული მომთაბარის ტური თბილისში",
 "3 hours: best coworking spaces, WiFi cafes and neighborhoods for remote work in Tbilisi.":
   "3 საათი: საუკეთესო ქოვორქინგები, WiFi-კაფეები და უბნები დისტანციური მუშაობისთვის თბილისში.",
 "Slow Travel Package — 3 Days in Georgia": "Slow Travel პაკეტი — 3 დღე საქართველოში",
 "3 days with Timur: new route every day, airport transfer included. Full immersion in Georgia.":
   "3 დღე თიმურთან: ყოველდღე ახალი მარშრუტი, აეროპორტის ტრანსფერი ჩათვლილი. სრული ჩაძირვა საქართველოში.",
 # --- ItemList ---
 "Private Tours in Georgia": "კერძო ტურები საქართველოში",
 "Private tours from Tbilisi. Kazbegi, Kakheti, hidden Tbilisi and other routes.":
   "კერძო ტურები თბილისიდან. ყაზბეგი, კახეთი, ფარული თბილისი და სხვა მარშრუტები.",
 "Kutaisi Day Trip": "ერთდღიანი ტური ქუთაისში",
 "Batumi Day Trip": "ერთდღიანი ტური ბათუმში",
 # --- VideoObject ---
 "Timur — Private Tour Guide in Georgia": "თიმური — კერძო გიდი საქართველოში",
 "Guide Timur talks about tours to Kazbegi, Kakheti and Mtskheta.":
   "გიდი თიმური მოგითხრობთ ტურებზე ყაზბეგში, კახეთსა და მცხეთაში.",
 # --- Services ---
 "Private Tour Guide in Georgia": "კერძო გიდი საქართველოში",
 "Private tours with guide Timur. Kazbegi, Kakheti, Tbilisi, Mtskheta, Batumi.":
   "კერძო ტურები გიდ თიმურთან. ყაზბეგი, კახეთი, თბილისი, მცხეთა, ბათუმი.",
 "Tbilisi Airport Transfer": "თბილისის აეროპორტის ტრანსფერი",
 "Airport meet & greet in Tbilisi. Comfortable vehicle, check-in assistance.":
   "შეხვედრა თბილისის აეროპორტში. კომფორტული ავტომობილი, დახმარება რეგისტრაციაში.",
 "Kakheti Wine Tour": "კახეთის ღვინის ტური",
 "Private tour from Tbilisi to Kakheti with tastings at boutique wineries. Sighnaghi, Bodbe, Tsinandali, Telavi.":
   "კერძო ტური თბილისიდან კახეთში დეგუსტაციებით ბუტიკ-მარნებში. სიღნაღი, ბოდბე, წინანდალი, თელავი.",
 "Tbilisi Food Tour": "თბილისის გასტრო-ტური",
 "Georgian cuisine tasting: khinkali, khachapuri, churchkhela. Dezerter Bazaar, tone bakery, home dinner.":
   "ქართული სამზარეულოს დეგუსტაცია: ხინკალი, ხაჭაპური, ჩურჩხელა. დეზერტირების ბაზარი, თონე, სახლის ვახშამი.",
 # --- BreadcrumbList ---
 "Home": "მთავარი",
 # --- FAQPage: Question name + Answer text ---
 "How much does a Kazbegi tour cost in 2026?": "რა ღირს ყაზბეგის ტური 2026 წელს?",
 "A private Kazbegi tour from Tbilisi costs from 175 GEL per person (about $65). The price includes comfortable vehicle transfer from your hotel in central Tbilisi, guide Timur for the full day, and entrance tickets to all sites. Departure at 08:00, return to Tbilisi around 22:00 — 14 hours total. The route includes Ananuri Fortress, Georgian Military Highway, Friendship Arch viewpoint, and Gergeti Trinity Church with views of Mt Kazbek (5047m). Maximum 7 people: no buses, no strangers. For a group of four, it is just 32 GEL per person — cheaper than any bus tour. 10% prepayment on booking, remainder in cash or by card on tour day.":
   "კერძო ტური ყაზბეგში თბილისიდან ღირს 175 ლარიდან ერთ ადამიანზე (დაახლოებით $65). ფასში შედის კომფორტული ტრანსფერი თბილისის ცენტრში მდებარე თქვენი სასტუმროდან, გიდი თიმური მთელი დღის განმავლობაში და შესვლის ბილეთები ყველა ობიექტზე. გამგზავრება 08:00-ზე, დაბრუნება თბილისში დაახლოებით 22:00-ზე — სულ 14 საათი. მარშრუტში შედის ანანურის ციხე, საქართველოს სამხედრო გზა, მეგობრობის თაღის ხედვის წერტილი და გერგეტის სამების ეკლესია მყინვარწვერის ხედით (5047 მ). მაქსიმუმ 7 ადამიანი: არანაირი ავტობუსი, არანაირი უცნობი. ოთხი ადამიანის ჯგუფისთვის ეს მხოლოდ 32 ლარია ერთ ადამიანზე — ნებისმიერ ავტობუსურ ტურზე იაფი. 10% წინასწარი გადახდა დაჯავშნისას, დანარჩენი — ნაღდი ან ბარათით ტურის დღეს.",
 "How to book a tour?": "როგორ დავჯავშნო ტური?",
 "Book a private tour with guide Timur via WhatsApp at +995 511 272 623 or Telegram bot @SakhvaGuideBot. Timur responds daily from 08:00 to 22:00 Tbilisi time, average response time 15 minutes. To book, just provide your preferred date, number of people, and which tour interests you. 10% prepayment on booking — the remainder is paid on tour day in cash (GEL, USD, EUR), by card, or cryptocurrency. After confirming the date, Timur will send a detailed route plan, departure time, and clothing recommendations.":
   "დაჯავშნეთ კერძო ტური გიდ თიმურთან WhatsApp-ზე +995 511 272 623 ან Telegram-ბოტით @SakhvaGuideBot. თიმური პასუხობს ყოველდღე 08:00-დან 22:00-მდე თბილისის დროით, საშუალო პასუხის დრო 15 წუთი. დასაჯავშნად უბრალოდ მიუთითეთ სასურველი თარიღი, ადამიანების რაოდენობა და რომელი ტური გაინტერესებთ. 10% წინასწარი გადახდა დაჯავშნისას — დანარჩენი იხდება ტურის დღეს ნაღდით (ლარი, USD, EUR), ბარათით ან კრიპტოვალუტით. თარიღის დადასტურების შემდეგ თიმური გამოგიგზავნით დეტალურ მარშრუტს, გამგზავრების დროსა და ჩაცმის რეკომენდაციებს.",
 "Can I cancel or reschedule a tour?": "შემიძლია ტურის გაუქმება ან თარიღის გადატანა?",
 "Free cancellation is available 24 hours before the tour — no questions asked, no penalties. For Kazbegi tours, there is a special policy: if the weather is bad on tour day and clouds cover the mountains, guide Timur will contact you and offer to reschedule for free. Unlimited reschedules — you can change the date as many times as needed until you catch perfect weather. For Tbilisi and Kakheti tours, rain is not a reason to cancel: sulfur baths, markets, wine cellars, and restaurants are equally great in any weather. Prepayment is only 10%, fully refundable if cancelled 24 hours ahead.":
   "უფასო გაუქმება ხელმისაწვდომია ტურამდე 24 საათით ადრე — ზედმეტი კითხვების და ჯარიმების გარეშე. ყაზბეგის ტურებისთვის მოქმედებს განსაკუთრებული პირობა: თუ ტურის დღეს ამინდი ცუდია და ღრუბლები ფარავს მთებს, გიდი თიმური დაგიკავშირდებათ და შემოგთავაზებთ უფასო გადატანას. შეზღუდვის გარეშე — თარიღი შეგიძლიათ იმდენჯერ შეცვალოთ, რამდენჯერაც საჭიროა, სანამ იდეალურ ამინდს დაიჭერთ. თბილისისა და კახეთის ტურებისთვის წვიმა გაუქმების მიზეზი არ არის: გოგირდის აბანოები, ბაზრები, ღვინის მარნები და რესტორნები თანაბრად მშვენივრად მუშაობს ნებისმიერ ამინდში. წინასწარი გადახდა მხოლოდ 10%-ია და სრულად ბრუნდება, თუ გააუქმებთ 24 საათით ადრე.",
 "What is the best season for Kazbegi in 2026?": "როდის არის საუკეთესო სეზონი ყაზბეგისთვის 2026 წელს?",
 "The best time to visit Kazbegi from Tbilisi is May-June and September-October. Hillsides are green, skies clear, and Mt Kazbek fully visible. July-August also works but can be hotter with more clouds. Winter is unique: Gergeti Church in snow without tourists, though Cross Pass may close due to avalanche risk. Distance from Tbilisi to Kazbegi: 157 km along the Georgian Military Highway, 2.5-3 hours. Sakhva Travel operates year-round. Guide Timur checks weather and road conditions before every tour, offering free reschedule if needed.":
   "ყაზბეგის მოსანახულებლად საუკეთესო დროა მაისი-ივნისი და სექტემბერი-ოქტომბერი. ფერდობები მწვანეა, ცა უღრუბლო, მყინვარწვერი სრულად ჩანს. ივლისი-აგვისტოც კარგია, მაგრამ შეიძლება უფრო ცხელი და ღრუბლიანი იყოს. ზამთარი უნიკალურია: გერგეტის ეკლესია თოვლში ტურისტების გარეშე, თუმცა ჯვრის უღელტეხილი შეიძლება დაიხუროს ზვავის საფრთხის გამო. მანძილი თბილისიდან ყაზბეგამდე: 157 კმ საქართველოს სამხედრო გზაზე, 2.5-3 საათი. Sakhva Travel მუშაობს მთელი წლის განმავლობაში. გიდი თიმური ამოწმებს ამინდსა და გზის მდგომარეობას ყოველი ტურის წინ და გთავაზობთ უფასო გადატანას საჭიროების შემთხვევაში.",
 "Do I need a visa for Georgia?": "მჭირდება ვიზა საქართველოსთვის?",
 "No visa needed for most tourists. Citizens of Russia, Belarus, Kazakhstan, Ukraine, Armenia and other CIS countries can enter Georgia visa-free for up to 365 days with a passport. EU, US, UK, Israel, Japan and 90+ other countries also enjoy visa-free entry. Georgia is one of the most open countries in the world. At the border, just show your passport — no forms, invitations or return tickets required. For Russian citizens, there are no direct flights, but convenient connections via Istanbul, Yerevan and Minsk are available.":
   "ტურისტების უმეტესობას ვიზა არ სჭირდება. რუსეთის, ბელარუსის, ყაზახეთის, უკრაინის, სომხეთისა და სხვა დსთ-ის ქვეყნების მოქალაქეებს შეუძლიათ საქართველოში უვიზოდ შემოსვლა 365 დღემდე პასპორტით. ევროკავშირის, აშშ-ის, დიდი ბრიტანეთის, ისრაელის, იაპონიისა და 90-ზე მეტი ქვეყნის მოქალაქეებიც უვიზოდ შემოდიან. საქართველო მსოფლიოში ერთ-ერთი ყველაზე ღია ქვეყანაა. საზღვარზე უბრალოდ წარადგინეთ პასპორტი — არანაირი ფორმა, მოწვევა ან უკან დაბრუნების ბილეთი არ არის საჭირო. რუსეთის მოქალაქეებისთვის პირდაპირი ფრენები არ არის, მაგრამ ხელმისაწვდომია მოსახერხებელი გადაჯდომები სტამბოლის, ერევნისა და მინსკის გავლით.",
 "Are there tours for expats living in Tbilisi?": "არის ტურები თბილისში მცხოვრები ექსპატებისთვის?",
 "Yes, Sakhva Travel offers several tours specifically for expats in Tbilisi. The Expat Tour is a 4-hour off-the-beaten-path route: Dezerter Bazaar, Saburtalo and Gldani neighborhoods, coworking spaces, hidden bars, practical tips on renting and banking. The Digital Nomad Tour covers the best coworking spaces, fast WiFi cafes, and comfortable work neighborhoods. Day trips to Kutaisi and Batumi are also available for those who have already explored Tbilisi. The Night Tbilisi tour shows the city from a new angle: sulfur baths by candlelight, illuminated Bridge of Peace, courtyard dinner.":
   "დიახ, Sakhva Travel გთავაზობთ რამდენიმე ტურს სპეციალურად თბილისის ექსპატებისთვის. ექსპატ-ტური არის 4-საათიანი არასტანდარტული მარშრუტი: დეზერტირების ბაზარი, საბურთალოსა და გლდანის უბნები, ქოვორქინგები, ფარული ბარები, პრაქტიკული რჩევები ქირავნობასა და ბანკინგზე. ციფრული მომთაბარის ტური მოიცავს საუკეთესო ქოვორქინგებს, სწრაფ WiFi-კაფეებსა და მუშაობისთვის კომფორტულ უბნებს. ერთდღიანი ტურები ქუთაისსა და ბათუმში ასევე ხელმისაწვდომია მათთვის, ვინც უკვე გაიცნო თბილისი. ღამის თბილისის ტური გაჩვენებთ ქალაქს ახალი კუთხით: გოგირდის აბანოები სანთლების შუქზე, განათებული მშვიდობის ხიდი, ვახშამი ეზოში.",
 "Is Georgia safe to visit in 2026?": "უსაფრთხოა საქართველოში მოგზაურობა 2026 წელს?",
 "Georgia is one of the safest countries for tourists in the region. Street crime is minimal, and locals are very friendly to visitors. Tbilisi is a modern, well-equipped city with developed infrastructure. All tourist routes — Kazbegi, Kakheti, Mtskheta, Batumi — run on paved roads with good infrastructure. Guide Timur checks weather and road conditions before every tour and does not depart if conditions are unsafe. In 3 years of operation, Sakhva Travel has conducted over 460 tours with zero incidents. Georgia ranks high in global traveler safety ratings.":
   "საქართველო რეგიონში ერთ-ერთი ყველაზე უსაფრთხო ქვეყანაა ტურისტებისთვის. ქუჩის დანაშაული მინიმალურია, ადგილობრივები კი ძალიან სტუმართმოყვარეები არიან. თბილისი თანამედროვე, კარგად აღჭურვილი ქალაქია განვითარებული ინფრასტრუქტურით. ყველა ტურისტული მარშრუტი — ყაზბეგი, კახეთი, მცხეთა, ბათუმი — გადის ასფალტიან გზებზე კარგი ინფრასტრუქტურით. გიდი თიმური ამოწმებს ამინდსა და გზის მდგომარეობას ყოველი ტურის წინ და არ გადის, თუ პირობები სახიფათოა. 3 წლის განმავლობაში Sakhva Travel-მა ჩაატარა 460-ზე მეტი ტური ნულოვანი ინციდენტით. საქართველო მაღალ ადგილს იკავებს მოგზაურთა უსაფრთხოების გლობალურ რეიტინგებში.",
 "What if the weather is bad on tour day?": "რა მოხდება, თუ ტურის დღეს ამინდი ცუდია?",
 "For Kazbegi tours, guide Timur monitors the weather forecast days in advance. If mountains are covered by clouds and Gergeti Church is not visible, Timur will contact you and offer a free reschedule — unlimited reschedules available. For Tbilisi and Kakheti tours, rain is not a problem: sulfur baths, covered markets, wine cellars, and restaurants are equally great in any weather. If you decide to go on a cloudy day anyway, the full route runs without any extra charges. Timur adapts the program: more time at stops that do not depend on visibility.":
   "ყაზბეგის ტურებისთვის გიდი თიმური ამინდის პროგნოზს დღეებით ადრე აკვირდება. თუ მთებს ღრუბლები დაფარავს და გერგეტის ეკლესია არ ჩანს, თიმური დაგიკავშირდებათ და შემოგთავაზებთ უფასო გადატანას — შეზღუდვის გარეშე. თბილისისა და კახეთის ტურებისთვის წვიმა პრობლემა არ არის: გოგირდის აბანოები, დახურული ბაზრები, ღვინის მარნები და რესტორნები თანაბრად მშვენივრად მუშაობს ნებისმიერ ამინდში. თუ მაინც გადაწყვეტთ ღრუბლიან დღეს წასვლას, სრული მარშრუტი ტარდება ყოველგვარი დამატებითი გადასახადის გარეშე. თიმური არგებს პროგრამას: მეტი დრო იმ გაჩერებებზე, რომლებიც ხილვადობაზე არ არის დამოკიდებული.",
 "Can I pay with cryptocurrency?": "შემიძლია გადახდა კრიპტოვალუტით?",
 "Yes, Sakhva Travel accepts cryptocurrency payments via NOWPayments. Available: USDT (TRC-20), Bitcoin, Ethereum, BNB and other popular coins. The process is simple: you receive a wallet address and QR code, transfer the amount, and payment is confirmed automatically. Exchange rate is locked for 20 minutes to protect you from fluctuations. No hidden fees from Sakhva Travel — only the standard blockchain network fee. If it is your first crypto payment, guide Timur will walk you through the process step by step via WhatsApp. Cash and card payments are also available.":
   "დიახ, Sakhva Travel იღებს გადახდას კრიპტოვალუტით NOWPayments-ის მეშვეობით. ხელმისაწვდომია: USDT (TRC-20), Bitcoin, Ethereum, BNB და სხვა პოპულარული მონეტები. პროცესი მარტივია: მიიღებთ საფულის მისამართსა და QR-კოდს, გადარიცხავთ თანხას და გადახდა ავტომატურად დასტურდება. კურსი ფიქსირდება 20 წუთით, რომ დაცული იყოთ რყევებისგან. არანაირი ფარული საკომისიო Sakhva Travel-ისგან — მხოლოდ ბლოკჩეინის ქსელის სტანდარტული საკომისიო. თუ ეს თქვენი პირველი კრიპტო-გადახდაა, გიდი თიმური ნაბიჯ-ნაბიჯ გაგაცნობთ პროცესს WhatsApp-ზე. ასევე ხელმისაწვდომია ნაღდი და ბარათით გადახდა.",
 "How is a private tour different from a group excursion?": "რით განსხვავდება კერძო ტური ჯგუფური ექსკურსიისგან?",
 "Group excursions in Georgia typically mean 20-40 people on a bus, a fixed schedule, and mandatory stops at tourist shops. A private tour with Sakhva Travel means maximum 7 people in your own group, personal guide Timur, and a route adapted to your interests and pace. No buses, no strangers, no forced stops. The price looks higher but splits across your group: for four people, a Kazbegi tour is just 32 GEL per person — about $12, cheaper than any bus tour. The quality is incomparable: you stop where you want, photograph as long as you want, and eat where you choose.":
   "ჯგუფური ექსკურსია საქართველოში ჩვეულებრივ ნიშნავს 20-40 ადამიანს ავტობუსში, ფიქსირებულ გრაფიკსა და სავალდებულო გაჩერებებს ტურისტულ მაღაზიებთან. კერძო ტური Sakhva Travel-თან ნიშნავს მაქსიმუმ 7 ადამიანს თქვენს საკუთარ ჯგუფში, პირად გიდ თიმურს და თქვენს ინტერესებსა და ტემპზე მორგებულ მარშრუტს. არანაირი ავტობუსი, არანაირი უცნობი, არანაირი იძულებითი გაჩერება. ფასი უფრო მაღალი ჩანს, მაგრამ იყოფა ჯგუფზე: ოთხი ადამიანისთვის ყაზბეგის ტური მხოლოდ 32 ლარია ერთ ადამიანზე — დაახლოებით $12, ნებისმიერ ავტობუსურ ტურზე იაფი. ხარისხი შეუდარებელია: ჩერდებით სადაც გსურთ, იღებთ იმდენ ხანს, რამდენიც გსურთ, და ჭამთ სადაც აირჩევთ.",
 "What language are tours conducted in?": "რა ენებზე ტარდება ტურები?",
 "All Sakhva Travel tours are available in Russian and English. Guide Timur is fluent in both languages. If your group includes both Russian and English speakers, Timur conducts the tour in both languages. Fully English tours are available for all routes.":
   "Sakhva Travel-ის ყველა ტური ხელმისაწვდომია რუსულ და ინგლისურ ენებზე. გიდი თიმური ორივე ენას თავისუფლად ფლობს. თუ თქვენს ჯგუფში არიან როგორც რუსულ-, ისე ინგლისურენოვანი მონაწილეები, თიმური ტურს ორ ენაზე ატარებს. სრულად ინგლისურენოვანი ტურები ხელმისაწვდომია ყველა მარშრუტისთვის.",
 "How many people can be in a group?": "რამდენი ადამიანი შეიძლება იყოს ჯგუფში?",
 "Maximum 7 people in one vehicle. It is your group only — no strangers. If you are more than 7, we arrange two vehicles with two guides at the same per-person price. Child seat on request, children under 6 — free.":
   "მაქსიმუმ 7 ადამიანი ერთ ავტომობილში. ეს მხოლოდ თქვენი ჯგუფია — არანაირი უცნობი. თუ 7-ზე მეტი ხართ, ვაწყობთ ორ ავტომობილს ორი გიდით იმავე ფასად ერთ ადამიანზე. ბავშვის სავარძელი მოთხოვნისამებრ, 6 წლამდე ბავშვები — უფასოდ.",
 "Where do you pick up for the tour?": "საიდან ხდება ტურზე წამოყვანა?",
 "We pick up from any hotel or apartment in central Tbilisi. If you are staying far from the center (Digomi, Gldani, Varketili), just share your address and we will calculate departure time. For Kazbegi tours, departure is usually at 08:00. For Tbilisi city tours — at your preferred time.":
   "წამოგიყვანთ თბილისის ცენტრში მდებარე ნებისმიერი სასტუმროდან ან ბინიდან. თუ ცენტრიდან შორს ცხოვრობთ (დიღომი, გლდანი, ვარკეთილი), უბრალოდ გაგვიზიარეთ მისამართი და გამოვთვლით გამგზავრების დროს. ყაზბეგის ტურებისთვის გამგზავრება ჩვეულებრივ 08:00-ზეა. თბილისის საქალაქო ტურებისთვის — თქვენთვის მოსახერხებელ დროს.",
 "What vehicle is used?": "რა ავტომობილი გამოიყენება?",
 "Comfortable SUV or minivan with AC, USB charging, and child seat on request. For mountain routes (Kazbegi, Kutaisi) we use a 4WD vehicle. The car is clean and well-maintained — we understand that comfort on the road matters.":
   "კომფორტული ჯიპი ან მინივენი კონდიციონერით, USB-დამტენითა და ბავშვის სავარძლით მოთხოვნისამებრ. მთის მარშრუტებისთვის (ყაზბეგი, ქუთაისი) ვიყენებთ 4WD ავტომობილს. მანქანა სუფთა და კარგად მოვლილია — გვესმის, რომ კომფორტი გზაზე მნიშვნელოვანია.",
 "What is included in the tour price?": "რა შედის ტურის ფასში?",
 "Included: round-trip transfer from your hotel, guide service for the full day, entrance tickets to all sites on the route. Not included: meals (lunch and dinner) and souvenirs. The guide will recommend places with great food at fair prices — no forced restaurant stops.":
   "შედის: სასტუმროდან წამოყვანა და დაბრუნება, გიდის მომსახურება მთელი დღის განმავლობაში, შესვლის ბილეთები მარშრუტის ყველა ობიექტზე. არ შედის: კვება (სადილი და ვახშამი) და სუვენირები. გიდი გირჩევთ ადგილებს გემრიელი საჭმლითა და სამართლიანი ფასებით — არანაირი იძულებითი გაჩერება რესტორანთან.",
 "Can I change the route during the tour?": "შემიძლია მარშრუტის შეცვლა ტურის განმავლობაში?",
 "Yes, this is the main advantage of a private tour. Want to stay longer at a waterfall or visit a village you spotted from the window — just say so. The route is flexible, time is in your hands. The only limitation is the overall tour duration.":
   "დიახ, ეს კერძო ტურის მთავარი უპირატესობაა. გინდათ ჩანჩქერთან მეტხანს დარჩენა ან სოფლის მონახულება, რომელიც ფანჯრიდან დაინახეთ — უბრალოდ თქვით. მარშრუტი მოქნილია, დრო თქვენს ხელშია. ერთადერთი შეზღუდვა ტურის საერთო ხანგრძლივობაა.",
 "Where to eat during the Kazbegi tour?": "სად ვჭამოთ ყაზბეგის ტურზე?",
 "On the Kazbegi route, guide Timur recommends 2-3 tested restaurants: one near Ananuri Fortress with reservoir views, one in Stepantsminda with authentic Georgian cuisine at local prices. Average lunch is 25-40 GEL per person. You can also bring your own food.":
   "ყაზბეგის მარშრუტზე გიდი თიმური გირჩევთ 2-3 გამოცდილ რესტორანს: ერთი ანანურის ციხესთან წყალსაცავის ხედით, ერთი სტეფანწმინდაში ავთენტური ქართული სამზარეულოთი ადგილობრივ ფასებში. საშუალო სადილი 25-40 ლარია ერთ ადამიანზე. ასევე შეგიძლიათ თქვენი საჭმელი წამოიღოთ.",
 "Do you offer winter tours?": "ატარებთ ტურებს ზამთარში?",
 "Yes, Sakhva Travel operates year-round. Winter highlights: Kazbegi in snow (if Cross Pass is open), nighttime Tbilisi with festive lights, Abanotubani sulfur baths. Kakheti in winter means quiet wineries without crowds. We check weather and road conditions before every winter tour.":
   "დიახ, Sakhva Travel მუშაობს მთელი წლის განმავლობაში. ზამთრის მთავარი მომენტები: თოვლიანი ყაზბეგი (თუ ჯვრის უღელტეხილი ღიაა), ღამის თბილისი სადღესასწაულო განათებით, აბანოთუბნის გოგირდის აბანოები. კახეთი ზამთარში ნიშნავს მშვიდ მარნებს ხალხმრავლობის გარეშე. ვამოწმებთ ამინდსა და გზის მდგომარეობას ყოველი ზამთრის ტურის წინ.",
 "Can I book a tour for tomorrow?": "შემიძლია ტურის დაჯავშნა ხვალისთვის?",
 "Yes, if the date is available. Message us on WhatsApp (+995 511 272 623) or Telegram (@SakhvaGuideBot) — Timur responds within 15 minutes. In high season (May-October), booking 2-3 days ahead is recommended. 10% prepayment on booking.":
   "დიახ, თუ თარიღი ხელმისაწვდომია. მოგვწერეთ WhatsApp-ზე (+995 511 272 623) ან Telegram-ზე (@SakhvaGuideBot) — თიმური პასუხობს 15 წუთში. მაღალ სეზონზე (მაისი-ოქტომბერი) რეკომენდებულია დაჯავშნა 2-3 დღით ადრე. 10% წინასწარი გადახდა დაჯავშნისას.",
 "Do you offer multi-day tours?": "გთავაზობთ მრავალდღიან ტურებს?",
 "Yes. Slow Travel package — 3 days with guide Timur: new route every day, airport transfer included. 595 GEL for the whole package. We can also create a custom multi-day route: for example, Tbilisi + Kazbegi + Kakheti in 4 days. Pricing calculated individually.":
   "დიახ. Slow Travel პაკეტი — 3 დღე გიდ თიმურთან: ყოველდღე ახალი მარშრუტი, აეროპორტის ტრანსფერი ჩათვლილი. 595 ლარი მთელ პაკეტზე. ასევე შეგვიძლია ინდივიდუალური მრავალდღიანი მარშრუტის შექმნა: მაგალითად, თბილისი + ყაზბეგი + კახეთი 4 დღეში. ფასი გამოითვლება ინდივიდუალურად.",
 "Are tours suitable for seniors?": "ტურები შესაფერისია ხანდაზმული მოგზაურებისთვის?",
 "Yes. All our routes run on paved roads with comfortable stops. In Kazbegi, we drive up — no hiking required. Tour pace adapts to the group. The only walking section is the ascent to Gergeti Trinity (optional — you can stay below and enjoy the view).":
   "დიახ. ჩვენი ყველა მარშრუტი გადის ასფალტიან გზებზე კომფორტული გაჩერებებით. ყაზბეგში მანქანით ავდივართ — ფეხით სიარული საჭირო არ არის. ტურის ტემპი ჯგუფზეა მორგებული. ერთადერთი ფეხით მონაკვეთი არის ასვლა გერგეტის სამებამდე (არასავალდებულო — შეგიძლიათ ქვემოთ დარჩეთ და ხედით დატკბეთ).",
 "Do you accept card payments?": "იღებთ ბარათით გადახდას?",
 "Yes. We accept: cash (GEL, USD, EUR), bank cards (Visa, Mastercard), cryptocurrency (USDT, BTC, ETH via NOWPayments). 10% prepayment on booking, remainder on tour day. Tips are not included and are at your discretion.":
   "დიახ. ვიღებთ: ნაღდს (ლარი, USD, EUR), საბანკო ბარათებს (Visa, Mastercard), კრიპტოვალუტას (USDT, BTC, ETH NOWPayments-ის მეშვეობით). 10% წინასწარი გადახდა დაჯავშნისას, დანარჩენი ტურის დღეს. ჩაი არ შედის და თქვენი შეხედულებისამებრ.",
 "How is Sakhva Travel different from Tripster and Viator?": "რით განსხვავდება Sakhva Travel Tripster-სა და Viator-ისგან?",
 "On aggregator platforms, you book a tour. With us, you book a specific guide — Timur. The route adapts to you in real time. No platform commission — lower price, same quality. Direct WhatsApp communication without middlemen. And free cancellation without the penalties that aggregators charge.":
   "აგრეგატორ-პლატფორმებზე თქვენ ჯავშნით ტურს. ჩვენთან კი ჯავშნით კონკრეტულ გიდს — თიმურს. მარშრუტი რეალურ დროში გერგებათ. არანაირი პლატფორმის საკომისიო — უფრო დაბალი ფასი იმავე ხარისხით. პირდაპირი კომუნიკაცია WhatsApp-ზე შუამავლების გარეშე. და უფასო გაუქმება იმ ჯარიმების გარეშე, რომლებსაც აგრეგატორები იღებენ.",
 "What to bring on a Kazbegi tour?": "რა წამოვიღო ყაზბეგის ტურზე?",
 "Comfortable shoes (sneakers), jacket or windbreaker (mountains are 10-15°C cooler), sunscreen, water. For the hike to Gergeti Trinity — athletic shoes required. In winter — warm jacket, hat, gloves. Before the tour, Timur sends recommendations based on the weather forecast.":
   "კომფორტული ფეხსაცმელი (სპორტული), ქურთუკი ან ქარსაფარი (მთებში 10-15°C-ით უფრო გრილა), მზისგან დამცავი კრემი, წყალი. გერგეტის სამებამდე ასვლისთვის — სპორტული ფეხსაცმელი აუცილებელია. ზამთარში — თბილი ქურთუკი, ქუდი, ხელთათმანები. ტურის წინ თიმური გამოგზავნის რეკომენდაციებს ამინდის პროგნოზის მიხედვით.",
 "Do you offer corporate tours?": "გთავაზობთ კორპორატიულ ტურებს?",
 "Yes. We organize corporate tours for groups of 5-30 people. Team building, khinkali cooking class, restaurant dinner, Old Tbilisi quest. Multiple vehicles, multilingual guides. From 2200 GEL per group. Contact us for custom pricing.":
   "დიახ. ვაწყობთ კორპორატიულ ტურებს 5-30 ადამიანის ჯგუფებისთვის. თიმბილდინგი, ხინკლის კულინარიული კლასი, ვახშამი რესტორანში, ძველი თბილისის ქვესტი. რამდენიმე ავტომობილი, მრავალენოვანი გიდები. 2200 ლარიდან ჯგუფზე. დაგვიკავშირდით ინდივიდუალური ფასისთვის.",
 # --- Review reviewBody (varianты в @graph) ---
 "We went to Kazbegi — Timur convinced us the special atmosphere was worth it. Snow by the church, silence. The most romantic day of the trip.":
   "ყაზბეგში წავედით — თიმურმა დაგვარწმუნა, რომ განსაკუთრებული ატმოსფერო ღირდა. თოვლი ეკლესიასთან, სიჩუმე. მოგზაურობის ყველაზე რომანტიული დღე.",
 "Wonderful trip to Kakheti! The wine was amazing — everyone should visit Georgian vineyards at least once.":
   "მშვენიერი მოგზაურობა კახეთში! ღვინო საოცარი იყო — ყველამ ერთხელ მაინც უნდა მოინახულოს ქართული ვენახები.",
 "Booked a private tour for four. Timur is a true professional: knows the history and tells it in a fascinating way.":
   "დავჯავშნეთ კერძო ტური ოთხისთვის. თიმური ნამდვილი პროფესიონალია: იცის ისტორია და მომხიბლავად ჰყვება.",
 "Highly recommend if you want the best advice and travel services across Georgia.":
   "ნამდვილად გირჩევთ, თუ გსურთ საუკეთესო რჩევა და სამოგზაურო მომსახურება მთელ საქართველოში.",
 "You have no idea how much I enjoyed it. Nice tiredness, nice people, delicious food. Thank you very much.":
   "წარმოდგენა არ გაქვთ, რამდენად მომეწონა. სასიამოვნო დაღლილობა, სასიამოვნო ხალხი, გემრიელი საჭმელი. დიდი მადლობა.",
 "Everything went perfectly, highly recommend!":
   "ყველაფერი იდეალურად ჩაიარა, ნამდვილად გირჩევთ!",
 "Excellent guide. Showed and told us everything about sunny Georgia. Speaks great English and Russian.":
   "შესანიშნავი გიდი. გვაჩვენა და მოგვითხრო ყველაფერი მზიან საქართველოზე. მშვენივრად საუბრობს ინგლისურად და რუსულად.",
 "Wonderful trip to Kakheti! The wine was amazing, everyone should visit Georgian vineyards at least once in their life. Thank you so much for such a wonderful time.":
   "მშვენიერი მოგზაურობა კახეთში! ღვინო საოცარი იყო, ყველამ სიცოცხლეში ერთხელ მაინც უნდა მოინახულოს ქართული ვენახები. დიდი მადლობა ასეთი მშვენიერი დროისთვის.",
 "Unforgettable tour! Thank you Timur and his team — absolutely loved every moment.":
   "დაუვიწყარი ტური! მადლობა თიმურსა და მის გუნდს — ყოველი წამი ძალიან მომეწონა.",
 "You have no idea how much I enjoyed it. It was really fun. Nice tiredness. Nice people. Delicious food. Thank you very much.":
   "წარმოდგენა არ გაქვთ, რამდენად მომეწონა. ნამდვილად სახალისო იყო. სასიამოვნო დაღლილობა. სასიამოვნო ხალხი. გემრიელი საჭმელი. დიდი მადლობა.",
 "Excellent guide. Showed and told us everything about sunny Georgia. Speaks fluent English.":
   "შესანიშნავი გიდი. გვაჩვენა და მოგვითხრო ყველაფერი მზიან საქართველოზე. თავისუფლად საუბრობს ინგლისურად.",
 "Highly recommended if you want the best advice and services for traveling in Georgia.":
   "ნამდვილად გირჩევთ, თუ გსურთ საუკეთესო რჩევა და მომსახურება საქართველოში მოგზაურობისთვის.",
}

# Значения, которые НАМЕРЕННО остаются латиницей (бренд/имена/URL-текст) —
# для верификации «не осталось непереведённого».
ALLOW_LATIN = {
 "Sakhva Travel", "Timur", "Elena", "Amovei", "Sergey", "Nugo Shengelia",
 "Mikhail D", "Vladislav S.", "Giorgi V.", "Amber R",
}

KEYS = {"name", "description", "text", "reviewBody", "headline"}

def translate(o):
    if isinstance(o, dict):
        return {k: (TRANS.get(v, v) if (k in KEYS and isinstance(v, str)) else translate(v))
                for k, v in o.items()}
    if isinstance(o, list):
        return [translate(x) for x in o]
    return o

def run():
    h = open(FILE, encoding="utf-8").read()
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', h, re.S)
    if not m:
        print("JSON-LD не найден"); sys.exit(1)
    g = json.loads(m.group(2))
    g2 = translate(g)
    new = json.dumps(g2, ensure_ascii=False, separators=(",", ":"))
    # проверка непереведённых значений
    leftover = []
    def check(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in KEYS and isinstance(v, str):
                    if not re.search(r'[Ⴀ-ჿ]', v) and v not in ALLOW_LATIN:
                        leftover.append(f"{k}: {v[:70]}")
                else: check(v)
        elif isinstance(o, list):
            for x in o: check(x)
    check(g2)
    if leftover:
        print("НЕПЕРЕВЕДЁННЫЕ значения — запись отменена:")
        print("\n".join(leftover)); sys.exit(1)
    out = h[:m.start()] + m.group(1) + new + m.group(3) + h[m.end():]
    open(FILE, "w", encoding="utf-8").write(out)
    print(f"OK: JSON-LD переведён, {new.count(chr(0x10D0))+1} узлов обработано")

if __name__ == "__main__":
    run()
