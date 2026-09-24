#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод EN->KA конкретной пилот-страницы (Казбеги).
Упорядоченные анкер-замены с проверкой счётчика. Ничего не трогает,
кроме перечисленных строк (скрипты/стили/URL/schema-структура целы).
Идемпотентность: применяется к EN-скелету ge/.../index.html один раз.
"""
import sys, re
from pathlib import Path

F = Path("/Users/vladimir/sakhva-travel/ge/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/index.html")

# (old, new, expected_count). None = ровно 1. Порядок ВАЖЕН: длинные/специфичные раньше.
R = [
# --- TITLE / META / OG / TWITTER (специфичные полные строки) ---
("Kazbegi Tour from Tbilisi 2026 — from ₾175 | Sakhva Travel",
 "ყაზბეგის ტური თბილისიდან 2026 — ₾175-დან | Sakhva Travel", 3),
("Kazbegi day trip from Tbilisi with a private tour from ₾175. Gergeti Trinity Church 2170m, Cross Pass, Ananuri Fortress. 11–12 hours, up to 7 people.",
 "ერთდღიანი ტური ყაზბეგში თბილისიდან — ინდივიდუალური ტური ₾175-დან. გერგეტის სამების ეკლესია 2170მ, ჯვრის უღელტეხილი, ანანურის ციხე. 11–12 საათი, 7 ადამიანამდე.", 1),
("Kazbegi day trip from Tbilisi with a private tour from ₾175. Gergeti Trinity Church, Cross Pass 2395m. 11–12 hours.",
 "ერთდღიანი ტური ყაზბეგში თბილისიდან — ინდივიდუალური ტური ₾175-დან. გერგეტის სამების ეკლესია, ჯვრის უღელტეხილი 2395მ. 11–12 საათი.", 1),
("Kazbegi day trip from Tbilisi with a private tour from ₾175. Gergeti Trinity Church, Cross Pass. 11–12 hours.",
 "ერთდღიანი ტური ყაზბეგში თბილისიდან — ინდივიდუალური ტური ₾175-დან. გერგეტის სამების ეკლესია, ჯვრის უღელტეხილი. 11–12 საათი.", 1),
("content=\"Timur — Sakhva Travel\"", "content=\"თიმური — Sakhva Travel\"", 1),
("Kazbegi Tour from Tbilisi — Gergeti Trinity Church",
 "ყაზბეგის ტური თბილისიდან — გერგეტის სამების ეკლესია", 2),  # og:image:alt + hero img alt
# --- SCHEMA: description (TouristTrip + Product одинаковы) ---
("Kazbegi day trip from Tbilisi with a private tour from ₾175. Gergeti Trinity Church 2170m, Cross Pass 2395m, Ananuri Fortress, Friendship of Nations Arch. 11–12 hours, up to 7 people.",
 "ერთდღიანი ტური ყაზბეგში თბილისიდან — ინდივიდუალური ტური ₾175-დან. გერგეტის სამების ეკლესია 2170მ, ჯვრის უღელტეხილი 2395მ, ანანურის ციხე, ხალხთა მეგობრობის თაღი. 11–12 საათი, 7 ადამიანამდე.", 2),
# schema author / credential / jobTitle
("\"name\":\"Timur Sakhvadze\"", "\"name\":\"თიმურ სახვაძე\"", 1),
("\"jobTitle\":\"Tbilisi Guide\"", "\"jobTitle\":\"თბილისის გიდი\"", 1),
("Guide license No. 8247109128", "გიდის ლიცენზია №8247109128", 1),
("Georgian National Tourism Administration", "საქართველოს ტურიზმის ეროვნული ადმინისტრაცია", 1),
("\"touristType\":\"English-speaking tourists\"", "\"touristType\":\"ტურისტები\"", 1),
("\"name\":\"Kazbegi Tour from Tbilisi\"", "\"name\":\"ყაზბეგის ტური თბილისიდან\"", 3),  # TouristTrip + Product + Breadcrumb#3
# --- BREADCRUMB names ---
("{\"@type\":\"ListItem\",\"position\":1,\"name\":\"Home\"", "{\"@type\":\"ListItem\",\"position\":1,\"name\":\"მთავარი\"", 1),
("{\"@type\":\"ListItem\",\"position\":2,\"name\":\"Tours\"", "{\"@type\":\"ListItem\",\"position\":2,\"name\":\"ტურები\"", 1),
# --- FAQ schema (name/text) ---
("\"name\":\"How long is the Kazbegi tour from Tbilisi?\"", "\"name\":\"რამდენ ხანს გრძელდება ყაზბეგის ტური თბილისიდან?\"", 1),
("The Kazbegi tour takes 11–12 hours. We depart at 08:00 and return to Tbilisi around 20:00. The route includes Zhinvali Reservoir, Ananuri Fortress, Cross Pass 2395m, and Gergeti Trinity Church at 2170m.",
 "ყაზბეგის ტური გრძელდება 11–12 საათი. გავდივართ 08:00-ზე და თბილისში ვბრუნდებით დაახლოებით 20:00-ზე. მარშრუტში შედის ჟინვალის წყალსაცავი, ანანურის ციხე, ჯვრის უღელტეხილი 2395მ და გერგეტის სამების ეკლესია 2170მ სიმაღლეზე.", 1),
("\"name\":\"Is the Gergeti Trinity Church accessible without a jeep?\"", "\"name\":\"შესაძლებელია თუ არა გერგეტის სამების ეკლესიამდე მისვლა ჯიპის გარეშე?\"", 1),
("You can hike up to Gergeti Trinity Church (about 1.5 hours each way), or take a local jeep for ₾20 per person. We arrange the jeep on site if you prefer not to hike.",
 "გერგეტის სამების ეკლესიამდე ფეხით ასვლა შესაძლებელია (დაახლოებით 1.5 საათი თითო მიმართულებით), ან ადგილობრივი ჯიპით ₾20 ერთ ადამიანზე. თუ ფეხით ასვლა არ გსურთ, ჯიპს ადგილზე მოვაწყობთ.", 1),
("\"name\":\"What is the best time to visit Kazbegi?\"", "\"name\":\"როდის არის ყაზბეგის მონახულების საუკეთესო დრო?\"", 1),
("The best time is May through October. In summer the church is often cloud-free until noon — we depart early (08:00) precisely for that reason. Winter tours are possible but the view of Mt. Kazbek may be blocked by clouds.",
 "საუკეთესო დროა მაისიდან ოქტომბრამდე. ზაფხულში ეკლესია ხშირად შუადღემდე უღრუბლოა — სწორედ ამიტომ გავდივართ ადრე (08:00). ზამთრის ტურებიც შესაძლებელია, თუმცა მყინვარწვერის ხედი შესაძლოა ღრუბლებმა დაფაროს.", 1),
("\"name\":\"What is included in the Kazbegi tour price?\"", "\"name\":\"რა შედის ყაზბეგის ტურის ფასში?\"", 1),
("Transfer from your Tbilisi hotel and back, private English-speaking guide, Ananuri Fortress stop, Cross Pass 2395m, and Gergeti Trinity Church visit. Jeep to the church (₾20), lunch, and entrance fees not included.",
 "თბილისის სასტუმროდან და უკან ტრანსფერი, ინდივიდუალური გიდი, გაჩერება ანანურის ციხესთან, ჯვრის უღელტეხილი 2395მ და გერგეტის სამების ეკლესიის მონახულება. ფასში არ შედის: ჯიპი ეკლესიამდე (₾20), სადილი და შესვლის საფასური.", 1),
# --- SCHEMA reviews (reviewBody совпадают с видимыми карточками -> replace-all) ---
("We went to Kazbegi — Timur convinced us the special atmosphere was worth it. Snow by the church, silence. The most romantic day of the trip.",
 "ვიყავით ყაზბეგში — თიმურმა დაგვარწმუნა, რომ განსაკუთრებული ატმოსფერო ღირდა. თოვლი ეკლესიასთან, სიჩუმე. მოგზაურობის ყველაზე რომანტიული დღე.", 2),
("You have no idea how much I enjoyed it. Nice tiredness, nice people, delicious food. Thank you very much.",
 "წარმოდგენა არ გაქვთ, რამდენად მომეწონა. სასიამოვნო დაღლილობა, კარგი ხალხი, გემრიელი საჭმელი. დიდი მადლობა.", 2),
("Wonderful excursion, thank you so much! Everything was top-notch.",
 "შესანიშნავი ექსკურსია, უღრმესი მადლობა! ყველაფერი უმაღლეს დონეზე იყო.", 2),
("Excellent guide. Showed and told us everything about sunny Georgia. Speaks great English and Russian.",
 "შესანიშნავი გიდი. ყველაფერი გვაჩვენა და მოგვიყვა მზიან საქართველოზე. მშვენივრად საუბრობს ინგლისურად და რუსულად.", 2),
("Very good guide. We had a great time! The program was tailored to us, recommend!",
 "ძალიან კარგი გიდი. მშვენივრად გავატარეთ დრო! პროგრამა ჩვენზე მოირგო, გირჩევთ!", 2),
("Highly recommend if you want the best advice and travel services across Georgia.",
 "ნამდვილად გირჩევთ, თუ გსურთ საუკეთესო რჩევები და მომსახურება საქართველოში მოგზაურობისთვის.", 2),
# --- NAV / DRAWER ---
(">Tours in Georgia<", ">ტურები საქართველოში<", 2),
(">Excursions<", ">ექსკურსიები<", 1),
(">Prices<", ">ფასები<", 1),
(">About<", ">ჩვენ შესახებ<", 2),  # nav + drawer
(">Blog<", ">ბლოგი<", 3),          # nav + drawer + footer <h4>Blog</h4>
(">Book Now</a>", ">დაჯავშნა</a>", 2),  # nav-btn + drawer d-btn
("aria-label=\"Menu\"", "aria-label=\"მენიუ\"", 1),
# --- HERO ---
(">Kazbegi Tour from Tbilisi</h1>", ">ყაზბეგის ტური თბილისიდან</h1>", 1),
("<span class=\"stat-val\">from ₾175</span><span class=\"stat-lab\">per person</span>",
 "<span class=\"stat-val\">₾175-დან</span><span class=\"stat-lab\">ერთ ადამიანზე</span>", 1),
("<span class=\"stat-val\">11–12 h</span><span class=\"stat-lab\">duration</span>",
 "<span class=\"stat-val\">11–12 სთ</span><span class=\"stat-lab\">ხანგრძლივობა</span>", 1),
("<span class=\"stat-val\">up to 7</span><span class=\"stat-lab\">people</span>",
 "<span class=\"stat-val\">7-მდე</span><span class=\"stat-lab\">ადამიანი</span>", 1),
("<span class=\"stat-val\">08:00</span><span class=\"stat-lab\">departure</span>",
 "<span class=\"stat-val\">08:00</span><span class=\"stat-lab\">გასვლა</span>", 1),
("<span class=\"stat-val\">24 h</span><span class=\"stat-lab\">free cancellation</span>",
 "<span class=\"stat-val\">24 სთ</span><span class=\"stat-lab\">უფასო გაუქმება</span>", 1),
("        Book from 175 GEL</a>", "        დაჯავშნა ₾175-დან</a>", 1),
("10% off — leave a request</a>", "10% ფასდაკლება — დატოვე განაცხადი</a>", 1),
("★ 4.7/5 · reply in 15 min", "★ 4.7/5 · პასუხი 15 წუთში", 2),
# --- PRICE BOX ---
("from 175 GEL <span style=\"font-size:14px;font-weight:400;color:#6B7280\">per person</span>",
 "₾175-დან <span style=\"font-size:14px;font-weight:400;color:#6B7280\">ერთ ადამიანზე</span>", 1),
("10% discount for groups of 4+", "10% ფასდაკლება 4+ ჯგუფისთვის", 1),
("    Book online</a>", "    დაჯავშნა ონლაინ</a>", 1),
# --- AUTHOR BYLINE ---
("alt=\"Timur — Georgia tour author\"", "alt=\"თიმური — ტურების ავტორი საქართველოში\"", 1),
(">Timur · Sakhva Travel</a>", ">თიმური · Sakhva Travel</a>", 1),
("Guiding in Georgia since 2023 · 500+ tours · 4.9/5 rating",
 "გიდობა საქართველოში 2023 წლიდან · 500+ ტური · რეიტინგი 4.9/5", 1),
# --- ITINERARY ---
(">Itinerary</div>", ">მარშრუტი</div>", 1),
(">Tour Schedule</h2>", ">ტურის განრიგი</h2>", 1),
(">Departure from Tbilisi</div>", ">გამგზავრება თბილისიდან</div>", 1),
("Hotel pickup. Georgian Military Highway north.", "წამოყვანა სასტუმროდან. საქართველოს სამხედრო გზა ჩრდილოეთისკენ.", 1),
(">Zhinvali Reservoir</div>", ">ჟინვალის წყალსაცავი</div>", 1),
("Photo stop. Turquoise water and mountain backdrop.", "ფოტო-გაჩერება. ფირუზისფერი წყალი და მთების ფონი.", 1),
(">Ananuri Fortress</div>", ">ანანურის ციხე</div>", 1),
("XVI–XVII century fortress complex above the reservoir. 20 minutes. Free entry.",
 "XVI–XVII საუკუნის ციხე-კომპლექსი წყალსაცავის ზემოთ. 20 წუთი. შესვლა უფასოა.", 1),
(">Friendship of Nations Arch</div>", ">ხალხთა მეგობრობის თაღი</div>", 1),
("Soviet-era mosaic panorama at 2196m. Photo stop, 15 minutes.",
 "საბჭოთა პერიოდის მოზაიკური პანორამა 2196მ სიმაღლეზე. ფოტო-გაჩერება, 15 წუთი.", 1),
(">Cross Pass — 2395m</div>", ">ჯვრის უღელტეხილი — 2395მ</div>", 1),
("Highest point of the Georgian Military Highway. Panoramic views of the Caucasus ridge.",
 "საქართველოს სამხედრო გზის უმაღლესი წერტილი. კავკასიონის ქედის პანორამული ხედები.", 1),
(">Stepantsminda (Kazbegi)</div>", ">სტეფანწმინდა (ყაზბეგი)</div>", 1),
("Village at the foot of Mt. Kazbek 5047m.", "სოფელი მყინვარწვერის ძირას, 5047მ.", 1),
(">Gergeti Trinity Church — 2170m</div>", ">გერგეტის სამების ეკლესია — 2170მ</div>", 1),
("XIV century church above the clouds. Hike (1.5h each way) or local jeep (₾20). 1 hour at the top.",
 "XIV საუკუნის ეკლესია ღრუბლებს ზემოთ. ფეხით (1.5 სთ თითო მიმართულებით) ან ადგილობრივი ჯიპით (₾20). 1 საათი მწვერვალზე.", 1),
(">Lunch in Stepantsminda</div>", ">სადილი სტეფანწმინდაში</div>", 1),
("Georgian mountain cuisine. ~₾20–30/person.", "ქართული მთის სამზარეულო. ~₾20–30 ერთ ადამიანზე.", 1),
(">Return to Tbilisi</div>", ">დაბრუნება თბილისში</div>", 1),
("Scenic drive back through the gorge. ~3 hours.", "მშვენიერი გზა ხეობის გავლით. ~3 საათი.", 1),
(">Arrival in Tbilisi</div>", ">ჩამოსვლა თბილისში</div>", 1),
("Hotel drop-off.", "სასტუმროსთან მიყვანა.", 1),
# --- ARTICLE BODY ---
("Kazbegi is the most popular day trip from Tbilisi. The Georgian Military Highway winds through dramatic gorges past Zhinvali Reservoir, the medieval Ananuri Fortress, and the Cross Pass at 2395m before reaching Stepantsminda — the village at the foot of Mt. Kazbek (5047m).",
 "ყაზბეგი ყველაზე პოპულარული ერთდღიანი ტურია თბილისიდან. საქართველოს სამხედრო გზა ჩამოუყვება ეფექტურ ხეობებს, ჩაივლის ჟინვალის წყალსაცავს, შუა საუკუნეების ანანურის ციხესა და ჯვრის უღელტეხილს 2395მ სიმაღლეზე, სანამ მიაღწევს სტეფანწმინდას — სოფელს მყინვარწვერის (5047მ) ძირას.", 1),
("<h2>Gergeti Trinity Church</h2>", "<h2>გერგეტის სამების ეკლესია</h2>", 1),
("The Tsminda Sameba church (XIV century) stands at 2170m on a rocky spur above Stepantsminda village with Mt. Kazbek (5047m) directly behind it. The combination of medieval stone church, green valley, glaciers and a nearly 6000m peak in the frame is the defining image of Georgia.",
 "წმინდა სამების ეკლესია (XIV საუკუნე) დგას 2170მ სიმაღლეზე, კლდოვან ქიმზე სოფელ სტეფანწმინდის ზემოთ, ხოლო უშუალოდ მის უკან — მყინვარწვერი (5047მ). შუა საუკუნეების ქვის ეკლესია, მწვანე ხეობა, მყინვარები და თითქმის 6000-მეტრიანი მწვერვალი ერთ კადრში — ეს არის საქართველოს სავიზიტო ხატი.", 1),
("The church is still active — monks live here year-round. On clear days the summit of Kazbek is snow-covered and perfectly visible. Timur's advice: Kazbek starts gathering clouds by noon, so the 08:00 departure is not arbitrary — it's the key to a clear view.",
 "ეკლესია დღემდე მოქმედია — ბერები აქ მთელი წელი ცხოვრობენ. ნათელ დღეებში მყინვარწვერის თოვლიანი მწვერვალი შესანიშნავად ჩანს. თიმურის რჩევა: მყინვარწვერი შუადღისთვის ღრუბლებით იფარება, ამიტომ 08:00-ზე გასვლა შემთხვევითი არ არის — ეს არის ნათელი ხედის გასაღები.", 1),
("<h2>The Georgian Military Highway</h2>", "<h2>საქართველოს სამხედრო გზა</h2>", 1),
("The road from Tbilisi to Kazbegi follows the ancient route across the Caucasus — the same path used by traders, armies, and poets for centuries. Lermontov wrote about Daryal Gorge here, and Pushkin crossed the same pass. The entire drive is spectacular scenery.",
 "თბილისიდან ყაზბეგისკენ მიმავალი გზა მიუყვება უძველეს მარშრუტს კავკასიონზე — იმავე გზას, რომელსაც საუკუნეების განმავლობაში იყენებდნენ ვაჭრები, ჯარები და პოეტები. ლერმონტოვმა აქ, დარიალის ხეობაზე დაწერა, ხოლო პუშკინმა იგივე უღელტეხილი გადალახა. მთელი გზა თვალწარმტაცი ხედებია.", 1),
("Key stops along the way: Zhinvali Reservoir (turquoise water between mountains), Ananuri Fortress (XVI–XVII century, free entry), Pasanauri village (junction with Aragvi rivers), and the Friendship of Nations Arch with its Soviet mosaic murals at 2196m.",
 "მთავარი გაჩერებები გზად: ჟინვალის წყალსაცავი (ფირუზისფერი წყალი მთებს შორის), ანანურის ციხე (XVI–XVII საუკუნე, შესვლა უფასოა), სოფელი ფასანაური (არაგვების შესართავი) და ხალხთა მეგობრობის თაღი საბჭოთა მოზაიკური ფრესკებით 2196მ სიმაღლეზე.", 1),
("<h2>Practical Tips</h2>", "<h2>პრაქტიკული რჩევები</h2>", 1),
("Timur's tip: leave Tbilisi by 08:00 without exception — Kazbek clouds over by noon and the view disappears. At Gergeti, take the jeep (₾20 per person) rather than hiking if you want to maximize time at the top. The best café in Stepantsminda is \"Guda\" — ask for khinkali with mountain herbs.",
 "თიმურის რჩევა: თბილისიდან უპირობოდ გადით 08:00-ზე — მყინვარწვერი შუადღისთვის იფარება და ხედი ქრება. გერგეტში, თუ გინდათ მწვერვალზე მეტი დროის გატარება, ფეხით ასვლის ნაცვლად აირჩიეთ ჯიპი (₾20 ერთ ადამიანზე). სტეფანწმინდაში საუკეთესო კაფეა „გუდა“ — სთხოვეთ ხინკალი მთის მწვანილებით.", 1),
("<strong>Dress in layers:</strong> it is typically 10–15°C cooler at 2170m than in Tbilisi, even in summer.",
 "<strong>ჩაიცვით ფენებად:</strong> 2170მ სიმაღლეზე ჩვეულებრივ 10–15°C-ით უფრო გრილა, ვიდრე თბილისში, ზაფხულშიც კი.", 1),
("<strong>Comfortable shoes:</strong> the path up to Gergeti is unpaved and rocky.",
 "<strong>კომფორტული ფეხსაცმელი:</strong> გერგეტისკენ მიმავალი ბილიკი მოუკირწყლავი და კლდოვანია.", 1),
("<strong>Cash in GEL:</strong> jeep drivers and mountain cafés are cash-only.",
 "<strong>ნაღდი ლარი:</strong> ჯიპის მძღოლები და მთის კაფეები მხოლოდ ნაღდ ფულს იღებენ.", 1),
("<strong>Best season:</strong> May–October for the best visibility. November–April the pass may be snowy but accessible.",
 "<strong>საუკეთესო სეზონი:</strong> მაისი–ოქტომბერი საუკეთესო ხილვადობისთვის. ნოემბერი–აპრილში უღელტეხილი შესაძლოა თოვლიანი იყოს, მაგრამ გავლადი.", 1),
("<strong>Read also:</strong> <a href=\"/en/blog/kazbegi-complete-guide/\">Kazbegi: the complete guide</a>",
 "<strong>წაიკითხეთ ასევე:</strong> <a href=\"/en/blog/kazbegi-complete-guide/\">ყაზბეგი: სრული გზამკვლევი</a>", 1),
("<h2>Frequently Asked Questions</h2>", "<h2>ხშირად დასმული კითხვები</h2>", 1),
("<h3>How long is the Kazbegi tour from Tbilisi?</h3>", "<h3>რამდენ ხანს გრძელდება ყაზბეგის ტური თბილისიდან?</h3>", 1),
("The tour takes 11–12 hours total. We depart at 08:00 and return to Tbilisi around 19:00–20:00. The route includes Ananuri Fortress, Cross Pass 2395m, Gergeti Trinity Church 2170m, and lunch in Stepantsminda.",
 "ტური სულ გრძელდება 11–12 საათი. გავდივართ 08:00-ზე და თბილისში ვბრუნდებით დაახლოებით 19:00–20:00-ზე. მარშრუტში შედის ანანურის ციხე, ჯვრის უღელტეხილი 2395მ, გერგეტის სამების ეკლესია 2170მ და სადილი სტეფანწმინდაში.", 1),
("<h3>Is the Gergeti Trinity Church accessible without a jeep?</h3>", "<h3>შესაძლებელია თუ არა გერგეტის სამების ეკლესიამდე მისვლა ჯიპის გარეშე?</h3>", 1),
("Yes — you can hike up in about 1.5 hours each way on a well-marked trail. Alternatively, local jeeps wait at the village square and charge ₾20 per person round trip. We arrange the jeep on site if you prefer not to hike.",
 "დიახ — ფეხით ასვლა შესაძლებელია დაახლოებით 1.5 საათში თითო მიმართულებით, კარგად მონიშნული ბილიკით. ალტერნატივად, ადგილობრივი ჯიპები დგანან სოფლის მოედანზე და ღირს ₾20 ერთ ადამიანზე ორივე მიმართულებით. თუ ფეხით ასვლა არ გსურთ, ჯიპს ადგილზე მოვაწყობთ.", 1),
("<h3>What is the best time to visit Kazbegi?</h3>", "<h3>როდის არის ყაზბეგის მონახულების საუკეთესო დრო?</h3>", 1),
("May through October for clear mountain views. We depart at 08:00 specifically because Mt. Kazbek clouds over by noon. Winter visits are possible but the summit view may be obscured.",
 "მაისიდან ოქტომბრამდე — მთების ნათელი ხედებისთვის. 08:00-ზე გავდივართ სწორედ იმიტომ, რომ მყინვარწვერი შუადღისთვის ღრუბლდება. ზამთარში მონახულებაც შესაძლებელია, თუმცა მწვერვალის ხედი შესაძლოა დაფარული იყოს.", 1),
("<h3>What is included in the Kazbegi tour price?</h3>", "<h3>რა შედის ყაზბეგის ტურის ფასში?</h3>", 1),
("Transfer from your Tbilisi hotel and back, private English-speaking guide, all stops including Ananuri Fortress and Cross Pass. Not included: jeep to Gergeti (₾20), lunch (₾20–30), entrance fees.",
 "თბილისის სასტუმროდან და უკან ტრანსფერი, ინდივიდუალური გიდი, ყველა გაჩერება ანანურის ციხისა და ჯვრის უღელტეხილის ჩათვლით. ფასში არ შედის: ჯიპი გერგეტამდე (₾20), სადილი (₾20–30), შესვლის საფასური.", 1),
("<h2>Timur's Insider Tip</h2>", "<h2>თიმურის ინსაიდერული რჩევა</h2>", 1),
("Most tourists photograph Gergeti from the village square — but the real perspective is from the church itself looking down at the village with Kazbek behind you. That requires being there before 11:00, which is exactly why we leave at 08:00. The descent through Daryal Gorge on the way back is different from the morning drive — the light changes and the gorge walls are 1000m high on both sides. We slow down there for photos.",
 "ტურისტების უმეტესობა გერგეტს სოფლის მოედნიდან იღებს — მაგრამ ნამდვილი რაკურსი თავად ეკლესიიდანაა, საიდანაც სოფელს გადახედავ, ზურგს უკან კი მყინვარწვერი დგას. ამისთვის საჭიროა იქ 11:00-მდე ყოფნა, სწორედ ამიტომ გავდივართ 08:00-ზე. დაბრუნებისას დარიალის ხეობის დაღმართი დილის გზას არ ჰგავს — შუქი იცვლება და ხეობის კედლები ორივე მხრიდან 1000მ სიმაღლისაა. იქ ფოტოებისთვის ვანელებთ.", 1),
("<h2>Why Choose This Tour</h2>", "<h2>რატომ უნდა აირჩიოთ ეს ტური</h2>", 1),
("Kazbegi in a day from Tbilisi: Gergeti Trinity Church at 2170m with Mt. Kazbek behind it, Cross Pass 2395m, and the entire Georgian Military Highway. The scenery is extraordinary and the logistics are complex without a guide — we handle everything so you just enjoy the views.",
 "ყაზბეგი ერთ დღეში თბილისიდან: გერგეტის სამების ეკლესია 2170მ სიმაღლეზე, ზურგში მყინვარწვერით, ჯვრის უღელტეხილი 2395მ და მთელი საქართველოს სამხედრო გზა. ხედები არაჩვეულებრივია, ხოლო ლოგისტიკა გიდის გარეშე რთულია — ჩვენ ყველაფერს ვუზრუნველვყოფთ, თქვენ კი უბრალოდ ტკბებით ხედებით.", 1),
("<h3>Included in Price</h3>", "<h3>ფასში შედის</h3>", 1),
("<li>Transfer from Tbilisi hotel and back</li><li>Private English-speaking guide</li><li>Ananuri Fortress stop</li><li>Cross Pass 2395m</li><li>Gergeti Trinity Church visit</li>",
 "<li>ტრანსფერი თბილისის სასტუმროდან და უკან</li><li>ინდივიდუალური გიდი</li><li>გაჩერება ანანურის ციხესთან</li><li>ჯვრის უღელტეხილი 2395მ</li><li>გერგეტის სამების ეკლესიის მონახულება</li>", 1),
("<h3 style=\"color:#991B1B\">Not Included</h3>", "<h3 style=\"color:#991B1B\">ფასში არ შედის</h3>", 1),
("<li>Jeep to Gergeti Church (₾20/person, optional)</li><li>Lunch (~₾20–30/person)</li><li>Entrance fees</li>",
 "<li>ჯიპი გერგეტის ეკლესიამდე (₾20/ადამიანი, სურვილისამებრ)</li><li>სადილი (~₾20–30/ადამიანი)</li><li>შესვლის საფასური</li>", 1),
("Ready to Book?", "მზად ხართ დასაჯავშნად?", 1),
("Timur — private tour rated 4.9. Groups up to 7 people, hotel pickup included, 10% deposit to confirm.",
 "თიმური — ინდივიდუალური ტური რეიტინგით 4.9. ჯგუფები 7 ადამიანამდე, წამოყვანა სასტუმროდან ფასში შედის, დასადასტურებლად 10% წინასწარი გადახდა.", 1),
("Learn more about our private tour service →", "გაიგეთ მეტი ჩვენი ინდივიდუალური ტურის სერვისზე →", 1),
("<h2>Practical Information</h2>", "<h2>პრაქტიკული ინფორმაცია</h2>", 1),
("The tour starts from your hotel in Tbilisi. I pick you up in a comfortable air-conditioned vehicle. Groups up to 7 people — personal attention to each guest. The itinerary is flexible: I can add stops or adjust based on your preferences. Languages: English, Russian, Georgian.",
 "ტური იწყება თქვენი სასტუმროდან თბილისში. მე გამოგივლით კომფორტული, კონდიცირებული ავტომობილით. ჯგუფები 7 ადამიანამდე — პერსონალური ყურადღება თითოეული სტუმრისადმი. მარშრუტი მოქნილია: შემიძლია დავამატო გაჩერებები ან მოვარგო თქვენს სურვილებს. ენები: ინგლისური, რუსული, ქართული.", 1),
("<h3>Booking and Payment</h3>", "<h3>დაჯავშნა და გადახდა</h3>", 1),
("Message on WhatsApp (+995 511 272 623) — I reply within 10–15 minutes. 10% deposit on booking, balance on the day of the tour. I accept: GEL cash, bank transfer, crypto. Free cancellation 24 hours before departure. In peak season (May–October) book 3–5 days ahead.",
 "მომწერეთ WhatsApp-ზე (+995 511 272 623) — ვპასუხობ 10–15 წუთში. 10% წინასწარ დაჯავშნისას, დანარჩენი — ტურის დღეს. ვიღებ: ნაღდ ლარს, საბანკო გადარიცხვას, კრიპტოს. უფასო გაუქმება გამგზავრებამდე 24 საათით ადრე. პიკის სეზონზე (მაისი–ოქტომბერი) დაჯავშნეთ 3–5 დღით ადრე.", 1),
("<h3>What to Bring</h3>", "<h3>რა წამოიღოთ</h3>", 1),
("Comfortable shoes (there will be walking even if you take the jeep), a water bottle (I provide extra), cash GEL for lunch and souvenirs. In summer bring sunscreen and a light jacket for the mountains.",
 "კომფორტული ფეხსაცმელი (სიარული მოგიწევთ, თუნდაც ჯიპით ისარგებლოთ), წყლის ბოთლი (მე დამატებით მოგცემთ), ნაღდი ლარი სადილისა და სუვენირებისთვის. ზაფხულში წამოიღეთ მზისგან დამცავი კრემი და მსუბუქი ქურთუკი მთებისთვის.", 1),
("<h3>Book the Tour</h3>", "<h3>დაჯავშნე ტური</h3>", 1),
("Timur · Sakhva Travel · licensed guide No. 8247109128 · rating 4.9 · 500+ guests",
 "თიმური · Sakhva Travel · ლიცენზირებული გიდი №8247109128 · რეიტინგი 4.9 · 500+ სტუმარი", 1),
("10% off — leave a request</button>", "10% ფასდაკლება — დატოვე განაცხადი</button>", 1),
# --- SEE ALSO chips ---
(">Gudauri Tour</a>", ">გუდაურის ტური</a>", 1),
(">Truso Gorge</a>", ">თრუსოს ხეობა</a>", 1),
(">Mtskheta Tour</a>", ">მცხეთის ტური</a>", 1),
(">All Tours</a>", ">ყველა ტური</a>", 1),
("See also:", "იხილეთ ასევე:", 1),
# --- REVIEWS SECTION ---
("text-transform:uppercase;color:#1A3D2E;margin-bottom:6px\">Reviews</div>",
 "text-transform:uppercase;color:#1A3D2E;margin-bottom:6px\">შეფასებები</div>", 1),
("Reviews of our mountain routes", "ჩვენი მთის მარშრუტების შეფასებები", 1),
("★ 4.7 out of 5 — 20 reviews on Google, Yandex and TripAdvisor",
 "★ 4.7 5-დან — 20 შეფასება Google-ზე, Yandex-სა და TripAdvisor-ზე", 1),
(">Elena</div>", ">ელენა</div>", 1),
(">February 2026</div>", ">თებერვალი 2026</div>", 1),
(">Mikhail D</div>", ">მიხაილ დ.</div>", 1),
(">Tigran M.</div>", ">ტიგრან მ.</div>", 1),
(">Giorgi V.</div>", ">გიორგი ვ.</div>", 1),
(">Vitaliy</div>", ">ვიტალი</div>", 1),
(">Nugo Shengelia</div>", ">ნუგო შენგელია</div>", 1),
(">April 2026</div>", ">აპრილი 2026</div>", 3),
(">May 2026</div>", ">მაისი 2026</div>", 1),
("All reviews on Google →", "ყველა შეფასება Google-ზე →", 1),
# аватар-инициалы -> грузинские
("flex-shrink:0\">E</div>", "flex-shrink:0\">ე</div>", 1),
("flex-shrink:0\">M</div>", "flex-shrink:0\">მ</div>", 1),
("flex-shrink:0\">T</div>", "flex-shrink:0\">ტ</div>", 1),
("flex-shrink:0\">G</div>", "flex-shrink:0\">გ</div>", 1),
("flex-shrink:0\">V</div>", "flex-shrink:0\">ვ</div>", 1),
("flex-shrink:0\">N</div>", "flex-shrink:0\">ნ</div>", 1),
# --- FOOTER ---
("Private English-speaking guide in Georgia 2026. Tbilisi, Kazbegi, Kakheti.",
 "ინდივიდუალური გიდი საქართველოში 2026. თბილისი, ყაზბეგი, კახეთი.", 1),
("<h4>Tours</h4>", "<h4>ტურები</h4>", 1),
("Kazbegi day trip — from ₾175", "ერთდღიანი ტური ყაზბეგში — ₾175-დან", 1),
("Night Tbilisi — from ₾100", "ღამის თბილისი — ₾100-დან", 1),
("Kakheti &amp; Sighnaghi — from ₾170", "კახეთი და სიღნაღი — ₾170-დან", 1),
("David Gareja — from ₾225", "დავით გარეჯა — ₾225-დან", 1),
(">All articles</a>", ">ყველა სტატია</a>", 1),
(">About Timur</a>", ">თიმურის შესახებ</a>", 1),
("© 2026 Sakhva Travel · Tbilisi, Georgia", "© 2026 Sakhva Travel · თბილისი, საქართველო", 1),
(">Leave a review ★</a>", ">დატოვე შეფასება ★</a>", 1),
(">Home</a>", ">მთავარი</a>", 1),
(">Email us</a>", ">მოგვწერეთ</a>", 1),
# --- CONTACT MODAL ---
("aria-label=\"Close\"", "aria-label=\"დახურვა\"", 1),
(">Book a Tour</div>", ">დაჯავშნე ტური</div>", 1),
("Leave your contact — Timur will get back to you", "დატოვეთ კონტაქტი — თიმური დაგიკავშირდებათ", 1),
(">Your name</label>", ">თქვენი სახელი</label>", 1),
("placeholder=\"Name\"", "placeholder=\"სახელი\"", 1),
(">Phone or WhatsApp</label>", ">ტელეფონი ან WhatsApp</label>", 1),
(">Message</label>", ">შეტყობინება</label>", 1),
("placeholder=\"Dates, number of people...\"", "placeholder=\"თარიღები, ადამიანების რაოდენობა...\"", 1),
(">Send →</button>", ">გაგზავნა →</button>", 1),
("Request sent!", "განაცხადი გაიგზავნა!", 1),
("Timur will contact you shortly", "თიმური მალე დაგიკავშირდებათ", 1),
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
        print("СТОП — расхождения счётчиков, ФАЙЛ НЕ ЗАПИСАН:")
        for p in problems: print("  ", p)
        sys.exit(1)
    F.write_text(html, encoding="utf-8")
    print(f"OK: применено {len(R)} замен")

if __name__ == "__main__":
    main()
