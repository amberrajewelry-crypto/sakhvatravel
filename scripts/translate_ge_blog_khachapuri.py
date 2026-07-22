#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод EN->KA пилота /ge/blog/adjarian-khachapuri-guide/. Анкер + счётчик."""
import sys
from pathlib import Path
F = Path("/Users/vladimir/sakhva-travel/ge/blog/adjarian-khachapuri-guide/index.html")

R = [
# фикс latent-бага: inline EN lang-detect на /ge/ -> убрать (не форсить EN)
("<script>if(!localStorage.getItem('lang')){var bl=navigator.language||navigator.userLanguage||'';if(bl.slice(0,2)!=='ru'){document.cookie='lang_pref=en;path=/;max-age=31536000;SameSite=Lax';localStorage.setItem('lang','en')}}</script>\n", "", 1),
# TITLE / META / OG / TWITTER  (og:image:alt раньше — длиннее, содержит title)
("Adjarian Khachapuri — Recipe, Types &amp; Where to Eat in Tbilisi", "აჭარული ხაჭაპური — რეცეპტი, სახეობები და სად ვჭამოთ თბილისში", 1),
("Adjarian Khachapuri — Recipe, Types", "აჭარული ხაჭაპური — რეცეპტი, სახეობები", 3),
("Adjarian khachapuri: boat-shaped Georgian cheese bread with egg and butter. Types, recipe, how to eat it properly, and the 7 best spots in Tbilisi. 2026.",
 "აჭარული ხაჭაპური: ნავის ფორმის ქართული ყველიანი პური კვერცხითა და კარაქით. სახეობები, რეცეპტი, როგორ ვჭამოთ სწორად და 7 საუკეთესო ადგილი თბილისში. 2026.", 1),
("Everything about Adjarian khachapuri: how it is made, the 5 regional types, how to eat it correctly, and where to find the best in Tbilisi. Prices in GEL.",
 "ყველაფერი აჭარულ ხაჭაპურზე: როგორ მზადდება, 5 რეგიონული სახეობა, როგორ ვჭამოთ სწორად და სად ვიპოვოთ საუკეთესო თბილისში. ფასები ლარებში.", 2),
("Timur · Sakhva Travel", "თიმური · Sakhva Travel", 5),
# SCHEMA @graph
("Adjarian Khachapuri 2026 — Recipe, Types &amp; Where to Eat in Tbilisi", "აჭარული ხაჭაპური 2026 — რეცეპტი, სახეობები და სად ვჭამოთ თბილისში", 1),
("Adjarian khachapuri — the open boat-shaped Georgian cheese bread with egg and butter. Learn how it is made, the 5 regional varieties, how to eat it correctly, and the 7 best spots in Tbilisi.",
 "აჭარული ხაჭაპური — ღია, ნავის ფორმის ქართული ყველიანი პური კვერცხითა და კარაქით. გაიგეთ, როგორ მზადდება, 5 რეგიონული სახეობა, როგორ ვჭამოთ სწორად და 7 საუკეთესო ადგილი თბილისში.", 1),
("\"name\":\"Timur Sakhvadze\"", "\"name\":\"თიმურ სახვაძე\"", 1),
("\"jobTitle\":\"Tbilisi Guide\"", "\"jobTitle\":\"თბილისის გიდი\"", 1),
("Лицензия гида Грузии / Georgia Tour Guide Licence", "საქართველოს გიდის ლიცენზია", 1),
("\"name\":\"Home\"", "\"name\":\"მთავარი\"", 1),
("\"name\":\"Blog\"", "\"name\":\"ბლოგი\"", 1),
("\"name\":\"Adjarian Khachapuri Guide\"", "\"name\":\"აჭარული ხაჭაპურის გზამკვლევი\"", 1),
# SCHEMA FAQ (8)
("\"name\":\"What is Adjarian khachapuri?\"", "\"name\":\"რა არის აჭარული ხაჭაპური?\"", 1),
("Adjarian khachapuri is an open boat-shaped Georgian cheese bread filled with melted suluguni cheese, topped with a raw egg and a knob of butter added just before serving. It comes from the Adjara region on the Black Sea coast. The boat shape traditionally symbolises the fishing boats used by Adjarian fishermen.",
 "აჭარული ხაჭაპური არის ღია, ნავის ფორმის ქართული ყველიანი პური, გამდნარი სულგუნით, რომელსაც თავზე ადევს ნედლი კვერცხი და მირთმევის წინ დამატებული კარაქის ნაჭერი. ის აჭარის მხარიდან, შავი ზღვის სანაპიროდან მოდის. ნავის ფორმა ტრადიციულად აჭარელი მეთევზეების სათევზაო ნავებს განასახიერებს.", 1),
("\"name\":\"How much does Adjarian khachapuri cost in Tbilisi?\"", "\"name\":\"რა ღირს აჭარული ხაჭაპური თბილისში?\"", 1),
("At local cafes and bakeries, Adjarian khachapuri costs 5–8 GEL. At mid-range restaurants it runs 12–18 GEL. Tourist restaurants in the Old Town charge 18–25 GEL for the same dish.",
 "ადგილობრივ კაფეებსა და საცხობებში აჭარული ხაჭაპური ღირს 5–8 ლარი. საშუალო კლასის რესტორნებში — 12–18 ლარი. ძველ ქალაქში ტურისტული რესტორნები იმავე კერძში 18–25 ლარს იღებენ.", 1),
("\"name\":\"How do you eat Adjarian khachapuri correctly?\"", "\"name\":\"როგორ ვჭამოთ აჭარული ხაჭაპური სწორად?\"", 1),
("Step 1: eat it immediately — the texture changes after 10 minutes. Step 2: mix the egg yolk and butter into the melted cheese with a spoon. Step 3: tear off pieces of the bread boat edges and dip them into the filling. Step 4: eat the remaining crust as the grand finale. Never use a knife and fork — that is a tourist move.",
 "ნაბიჯი 1: მიირთვით მაშინვე — ტექსტურა 10 წუთში იცვლება. ნაბიჯი 2: კოვზით აურიეთ კვერცხის გული და კარაქი გამდნარ ყველში. ნაბიჯი 3: მოხიეთ ნავის ნაპირების ნაჭრები და ჩააწექით შიგთავსში. ნაბიჯი 4: ბოლოს, როგორც აპოთეოზი, შეჭამეთ დარჩენილი ქერქი. არასოდეს გამოიყენოთ დანა და ჩანგალი — ეს ტურისტის ნიშანია.", 1),
("\"name\":\"What is the difference between Adjarian and Imeretian khachapuri?\"", "\"name\":\"რა განსხვავებაა აჭარულ და იმერულ ხაჭაპურს შორის?\"", 1),
("Adjarian khachapuri is open-topped, boat-shaped, with suluguni cheese, egg, and butter. It must be eaten hot immediately. Imeretian khachapuri is a closed round flatbread filled with mild imeruli cheese — the everyday version eaten throughout Georgia, milder in flavour and easier to eat on the go.",
 "აჭარული ხაჭაპური ღიაა, ნავის ფორმის, სულგუნით, კვერცხითა და კარაქით. ცხელი უნდა შეიჭამოს მაშინვე. იმერული ხაჭაპური დახურული მრგვალი ლავაშია, რბილი იმერული ყველით — ყოველდღიური ვერსია, რომელსაც მთელ საქართველოში ჭამენ, უფრო რბილი გემოთი და მოსახერხებელი გზაში საჭმელად.", 1),
("\"name\":\"Can you make Adjarian khachapuri at home?\"", "\"name\":\"შესაძლებელია აჭარული ხაჭაპურის სახლში მომზადება?\"", 1),
("Yes. The dough uses matzoni (Georgian yoghurt) or kefir, flour, salt, and a small amount of yeast. Let it rest 30 minutes. Fill with grated suluguni, shape into a boat, bake at 220–230°C for 15–18 minutes, then add the raw egg and return to the oven for 3–4 minutes until the white sets but the yolk remains runny. Drop in a piece of butter and serve.",
 "დიახ. ცომი მზადდება მაწვნით (ქართული იოგურტი) ან კეფირით, ფქვილით, მარილითა და ცოტაოდენი საფუარით. დაასვენეთ 30 წუთი. შეავსეთ გახეხილი სულგუნით, ჩამოაყალიბეთ ნავის ფორმა, გამოაცხვეთ 220–230°C-ზე 15–18 წუთი, შემდეგ ჩაარტყით ნედლი კვერცხი და დააბრუნეთ ღუმელში 3–4 წუთით, სანამ ცილა შედედდება, გული კი თხევადი დარჩება. ჩადეთ კარაქის ნაჭერი და მიირთვით.", 1),
("\"name\":\"Which area of Tbilisi has the best Adjarian khachapuri?\"", "\"name\":\"თბილისის რომელ უბანშია საუკეთესო აჭარული ხაჭაპური?\"", 1),
("The best value is found along Agmashenebeli Avenue, around Marjanishvili Square, and in the Didube area. These are working-class neighbourhoods where locals eat — no tourist markup, and the khachapuri is made fresh throughout the day.",
 "საუკეთესო ფასად ნახავთ აღმაშენებლის გამზირზე, მარჯანიშვილის მოედნის მიდამოებსა და დიდუბის რაიონში. ეს სამუშაო კლასის უბნებია, სადაც ადგილობრივები ჭამენ — ტურისტული ზედნადების გარეშე, ხაჭაპური კი მთელი დღის განმავლობაში ახლად ცხვება.", 1),
("\"name\":\"Where does Adjarian khachapuri come from?\"", "\"name\":\"საიდან მოდის აჭარული ხაჭაპური?\"", 1),
("Adjarian khachapuri originates from the Adjara region in southwestern Georgia on the Black Sea coast, centred on the city of Batumi. The boat shape represents the fishing boats of the region. Georgian bread culture was inscribed on the UNESCO Intangible Cultural Heritage list in 2022.",
 "აჭარული ხაჭაპური წარმოშობით სამხრეთ-დასავლეთ საქართველოს აჭარის მხარიდან, შავი ზღვის სანაპიროდან, ქალაქ ბათუმის ცენტრით. ნავის ფორმა მხარის სათევზაო ნავებს განასახიერებს. ქართული პურის კულტურა 2022 წელს UNESCO-ს არამატერიალური კულტურული მემკვიდრეობის სიაში შევიდა.", 1),
("\"name\":\"Can I join a gastro tour to try khachapuri in Tbilisi?\"", "\"name\":\"შემიძლია შევუერთდე გასტრო-ტურს, რომ თბილისში ხაჭაპური დავაგემოვნო?\"", 1),
("Yes. Sakhva Travel runs a gastro tour of Tbilisi with guide Timur, visiting 4–5 authentic local spots including a traditional bakery and a neighbourhood dukhan. The tour covers khachapuri, khinkali, local wine, and market food. Cost: from ₾165 per person. Book via WhatsApp: +995511272623.",
 "დიახ. Sakhva Travel ატარებს თბილისის გასტრო-ტურს გიდ თიმურთან ერთად, 4–5 ავთენტური ადგილის მონახულებით, ტრადიციული საცხობისა და უბნის დუქნის ჩათვლით. ტური მოიცავს ხაჭაპურს, ხინკალს, ადგილობრივ ღვინოსა და ბაზრის საჭმელს. ფასი: ₾165-დან ერთ ადამიანზე. დაჯავშნა WhatsApp-ით: +995511272623.", 1),
# NAV / DRAWER
(">Tours in Georgia<", ">ტურები საქართველოში<", 2),
(">Excursions<", ">ექსკურსიები<", 2),
(">Prices<", ">ფასები<", 1),
(">About<", ">ჩვენ შესახებ<", 2),
(">Reviews<", ">შეფასებები<", 2),
(">Blog<", ">ბლოგი<", 4),  # nav+drawer+hero-breadcrumb+footer-h4
(">FAQ<", ">FAQ<", 3),
(">Contacts<", ">კონტაქტები<", 2),
(">Book Now</a>", ">დაჯავშნა</a>", 1),
("aria-label=\"Menu\"", "aria-label=\"მენიუ\"", 1),
# HERO
(">Home</a>", ">მთავარი</a>", 2),  # hero-breadcrumb + footer
("<span>Adjarian Khachapuri</span>", "<span>აჭარული ხაჭაპური</span>", 1),
(">Guide · 10 min read</div>", ">გზამკვლევი · 10 წთ საკითხავი</div>", 1),
("Adjarian Khachapuri — Everything You Need to Know (and Where to Find the Best)",
 "აჭარული ხაჭაპური — ყველაფერი, რაც უნდა იცოდე (და სად ვიპოვოთ საუკეთესო)", 1),
("<span>May 17, 2026</span>", "<span>17 მაისი, 2026</span>", 1),
("<span>Georgian Cuisine · Tbilisi Restaurants</span>", "<span>ქართული სამზარეულო · თბილისის რესტორნები</span>", 1),
# AUTHOR BYLINE
("alt=\"Timur — private tour guide in Tbilisi\"", "alt=\"თიმური — კერძო გიდი თბილისში\"", 1),
("Guiding in Georgia since 2023 · 500+ tours · 4.9/5 rating",
 "გიდობა საქართველოში 2023 წლიდან · 500+ ტური · რეიტინგი 4.9/5", 1),
# TOC
("<h2>Contents</h2>", "<h2>შინაარსი</h2>", 1),
("History: why the boat shape and UNESCO heritage", "ისტორია: რატომ ნავის ფორმა და UNESCO-ს მემკვიდრეობა", 2),  # TOC + h2
("The recipe: dough, filling, and baking technique", "რეცეპტი: ცომი, შიგთავსი და ცხობის ტექნიკა", 2),
("5 types of khachapuri — comparison table", "ხაჭაპურის 5 სახეობა — შედარების ცხრილი", 2),
("7 best spots in Tbilisi (with real prices)", "7 საუკეთესო ადგილი თბილისში (რეალური ფასებით)", 1),  # TOC only
("How to eat Adjarian khachapuri — 4 steps", "როგორ ვჭამოთ აჭარული ხაჭაპური — 4 ნაბიჯი", 2),
("Gastro tour of Tbilisi with a local guide", "თბილისის გასტრო-ტური ადგილობრივ გიდთან", 2),
# LEAD
("Adjarian khachapuri costs <strong>5–8 ₾</strong> at a neighbourhood bakery and <strong>12–18 ₾</strong> at tourist restaurants. The difference is not just in price — it is in quality. This guide covers the history, the recipe, five regional varieties, and where in Tbilisi to find the real thing. Don't forget to <a href=\"/en/blog/travel-insurance-georgia-2026/\" style=\"color:#1A3D2E;font-weight:600\">get travel insurance</a> — mandatory for entering Georgia since 2026.",
 "აჭარული ხაჭაპური უბნის საცხობში ღირს <strong>5–8 ₾</strong>, ტურისტულ რესტორნებში კი <strong>12–18 ₾</strong>. განსხვავება მხოლოდ ფასში არ არის — არამედ ხარისხში. ეს გზამკვლევი მოიცავს ისტორიას, რეცეპტს, ხუთ რეგიონულ სახეობასა და იმას, თუ სად ვიპოვოთ ნამდვილი თბილისში. არ დაგავიწყდეთ <a href=\"/en/blog/travel-insurance-georgia-2026/\" style=\"color:#1A3D2E;font-weight:600\">სამოგზაურო დაზღვევის გაფორმება</a> — 2026 წლიდან საქართველოში შესვლისთვის სავალდებულოა.", 1),
("alt=\"Adjarian khachapuri — Georgian cheese bread with egg and butter\"", "alt=\"აჭარული ხაჭაპური — ქართული ყველიანი პური კვერცხითა და კარაქით\"", 1),
# HISTORY
("Adjarian khachapuri comes from the Adjara region — the narrow strip of Georgian coastline on the Black Sea, centred on Batumi. Unlike the rest of Georgia, Adjara had centuries of Ottoman influence, which shaped its architecture, cuisine, and culture in distinctive ways.",
 "აჭარული ხაჭაპური აჭარის მხარიდან მოდის — ეს არის საქართველოს სანაპიროს ვიწრო ზოლი შავ ზღვაზე, ბათუმის ცენტრით. საქართველოს დანარჩენი ნაწილისგან განსხვავებით, აჭარას საუკუნეების ოსმალური გავლენა ჰქონდა, რამაც მისი არქიტექტურა, სამზარეულო და კულტურა თავისებურად ჩამოაყალიბა.", 1),
("The boat shape is not a coincidence. The fishermen of the Black Sea coast used small wooden boats of exactly this profile. When bakers began making an open-topped cheese bread for them — sturdy enough to carry out to sea, rich enough to sustain a long day on the water — they shaped it to match. The boat became the symbol of Adjarian identity.",
 "ნავის ფორმა შემთხვევითი არ არის. შავი ზღვის სანაპიროს მეთევზეები სწორედ ასეთი პროფილის პატარა ხის ნავებს იყენებდნენ. როცა მცხობელებმა მათთვის ღია ყველიანი პურის ცხობა დაიწყეს — საკმარისად მტკიცე ზღვაზე წასაღებად, საკმარისად მკვებავი წყალზე გრძელი დღის გასაძლებად — მას შესაბამისი ფორმა მისცეს. ნავი აჭარული იდენტობის სიმბოლო გახდა.", 1),
("In 2022, the tradition of making Georgian bread was inscribed on the <strong>UNESCO Intangible Cultural Heritage</strong> list. This recognition covers the entire spectrum of Georgian bread culture — from the tone oven (a cylindrical clay pit) to the specific regional forms like Adjarian khachapuri.",
 "2022 წელს ქართული პურის ცხობის ტრადიცია <strong>UNESCO-ს არამატერიალური კულტურული მემკვიდრეობის</strong> სიაში შევიდა. ეს აღიარება მოიცავს ქართული პურის კულტურის მთელ სპექტრს — თონედან (ცილინდრული თიხის ორმო) კონკრეტულ რეგიონულ ფორმებამდე, როგორიც აჭარული ხაჭაპურია.", 1),
("<strong>The name:</strong> \"khachapuri\" combines two Georgian words — \"khacho\" (cottage cheese or curd) and \"puri\" (bread). In practice, modern versions use suluguni rather than pure curd, but the name has stuck. Every region of Georgia has its own variation.",
 "<strong>სახელი:</strong> „ხაჭაპური“ ორ ქართულ სიტყვას აერთიანებს — „ხაჭო“ (ხაჭო ან შრატიანი ყველი) და „პური“. პრაქტიკაში თანამედროვე ვერსიები სუფთა ხაჭოს ნაცვლად სულგუნს იყენებენ, მაგრამ სახელი დამკვიდრდა. საქართველოს ყოველ კუთხეს თავისი ვარიაცია აქვს.", 1),
# RECIPE
("The dough for authentic Adjarian khachapuri uses matzoni — Georgian fermented milk, similar to yoghurt but thinner and more tart. You can substitute kefir. The matzoni gives the dough a slight tang and a soft, chewy texture after baking.",
 "ნამდვილი აჭარული ხაჭაპურის ცომში იყენებენ მაწონს — ქართულ დადუღებულ რძეს, იოგურტის მსგავსს, ოღონდ უფრო თხელსა და მჟავეს. შეგიძლიათ კეფირით ჩაანაცვლოთ. მაწონი ცომს მსუბუქ სიმჟავეს და ცხობის შემდეგ რბილ, საღეჭ ტექსტურას აძლევს.", 1),
("<h3>Dough ingredients (for 2 portions)</h3>", "<h3>ცომის ინგრედიენტები (2 ულუფაზე)</h3>", 1),
("<li>500g flour</li>", "<li>500გ ფქვილი</li>", 1),
("<li>250ml matzoni or kefir</li>", "<li>250მლ მაწონი ან კეფირი</li>", 1),
("<li>1 tsp dry yeast</li>", "<li>1 ჩ/კ მშრალი საფუარი</li>", 1),
("<li>1 tsp salt</li>", "<li>1 ჩ/კ მარილი</li>", 1),
("<li>1 tbsp vegetable oil</li>", "<li>1 ს/კ მცენარეული ზეთი</li>", 1),
("Mix the ingredients, knead for 8–10 minutes until smooth, cover, and rest for 30 minutes at room temperature. The dough should be soft and slightly sticky.",
 "აურიეთ ინგრედიენტები, მოზილეთ 8–10 წუთი გლუვ მასამდე, დააფარეთ და დაასვენეთ 30 წუთი ოთახის ტემპერატურაზე. ცომი უნდა იყოს რბილი და ოდნავ წებოვანი.", 1),
("<h3>Filling</h3>", "<h3>შიგთავსი</h3>", 1),
("<li>400g suluguni (or a mix of suluguni and imeruli cheese)</li>", "<li>400გ სულგუნი (ან სულგუნისა და იმერული ყველის ნაზავი)</li>", 1),
("<li>2 eggs (one per portion)</li>", "<li>2 კვერცხი (თითო ულუფაზე)</li>", 1),
("<li>Butter to finish</li>", "<li>კარაქი დასასრულებლად</li>", 1),
("Grate the suluguni coarsely. If it is very salty, soak in cold water for 20–30 minutes first. A mix of 70% suluguni and 30% imeruli produces a milder, creamier filling.",
 "სულგუნი მსხვილად გახეხეთ. თუ ძალიან მარილიანია, ჯერ ცივ წყალში დაალბეთ 20–30 წუთი. 70% სულგუნისა და 30% იმერულის ნაზავი უფრო რბილ, ნაღებისებრ შიგთავსს იძლევა.", 1),
("<h3>Assembly and baking</h3>", "<h3>აწყობა და ცხობა</h3>", 1),
("<li>Roll the dough into an oval about 25 cm long.</li>", "<li>გააბრტყელეთ ცომი ოვალურად, დაახლოებით 25 სმ სიგრძეზე.</li>", 1),
("<li>Pile the cheese filling down the centre, leaving a 4 cm border on each side.</li>", "<li>ყველის შიგთავსი ცენტრში დააგროვეთ, თითო მხარეს 4 სმ ნაპირი დატოვეთ.</li>", 1),
("<li>Roll the long edges inward to form the boat sides, pinching the ends into pointed tips.</li>", "<li>გრძელი ნაპირები შიგნით მოახვიეთ ნავის გვერდების შესაქმნელად, ბოლოები წაწვეტებულ წვერებად აქციეთ.</li>", 1),
("<li>Bake at 220–230°C for 15–18 minutes until the crust is golden and the cheese is fully melted.</li>", "<li>გამოაცხვეთ 220–230°C-ზე 15–18 წუთი, სანამ ქერქი გაოქროსფერდება და ყველი მთლიანად გადნება.</li>", 1),
("<li>Remove from the oven, make a well in the centre of the cheese, crack a raw egg into it, and return to the oven for 3–4 minutes — the white should set but the yolk remain runny.</li>", "<li>ამოიღეთ ღუმელიდან, ყველის ცენტრში ჩაღრმავება გააკეთეთ, ნედლი კვერცხი ჩაარტყით და დააბრუნეთ ღუმელში 3–4 წუთით — ცილა უნდა შედედდეს, გული კი თხევადი დარჩეს.</li>", 1),
("<li>Immediately drop a knob of butter (about 30g) into the filling and serve at once.</li>", "<li>მაშინვე ჩადეთ კარაქის ნაჭერი (დაახლოებით 30გ) შიგთავსში და მყისვე მიირთვით.</li>", 1),
("<strong>Guide's tip:</strong> The single most common mistake is overbaking the egg. Three to four minutes at 220°C is enough. The yolk should still wobble when you take it out. It continues to cook on the way to the table.",
 "<strong>გიდის რჩევა:</strong> ყველაზე გავრცელებული შეცდომა კვერცხის გადაცხობაა. სამი-ოთხი წუთი 220°C-ზე საკმარისია. ამოღებისას გული ჯერ კიდევ უნდა თრთოდეს. ის მაგიდისკენ მიმავალ გზაზე აგრძელებს მომზადებას.", 1),
# TYPES
("Georgia has at least five distinct regional styles of khachapuri. They differ in shape, cheese, and technique. Adjarian is the most photogenic, but each has its own character.",
 "საქართველოში ხაჭაპურის სულ მცირე ხუთი განსხვავებული რეგიონული სტილია. ისინი განსხვავდებიან ფორმით, ყველითა და ტექნიკით. აჭარული ყველაზე ფოტოგენურია, მაგრამ თითოეულს თავისი ხასიათი აქვს.", 1),
("<thead><tr><th>Type</th><th>Region</th><th>Shape</th><th>Filling</th><th>Price in Tbilisi</th></tr></thead>",
 "<thead><tr><th>სახეობა</th><th>რეგიონი</th><th>ფორმა</th><th>შიგთავსი</th><th>ფასი თბილისში</th></tr></thead>", 1),
("<td>Adjara (Batumi)</td><td>Open boat, egg + butter on top</td><td>Suluguni + raw egg</td>", "<td>აჭარა (ბათუმი)</td><td>ღია ნავი, კვერცხი + კარაქი თავზე</td><td>სულგუნი + ნედლი კვერცხი</td>", 1),
("<td><strong>Imeretian</strong></td><td>Imereti (Kutaisi)</td><td>Closed round flatbread</td><td>Imeruli cheese</td>", "<td><strong>იმერული</strong></td><td>იმერეთი (ქუთაისი)</td><td>დახურული მრგვალი ლავაში</td><td>იმერული ყველი</td>", 1),
("<td><strong>Megrelian</strong></td><td>Samegrelo</td><td>Round, cheese crust on top</td><td>Suluguni inside + outside</td>", "<td><strong>მეგრული</strong></td><td>სამეგრელო</td><td>მრგვალი, ყველის ქერქი თავზე</td><td>სულგუნი შიგნით + გარეთ</td>", 1),
("<td><strong>Penoiani</strong></td><td>Svaneti &amp; Racha</td><td>Folded triangle</td><td>Cheese + potato</td>", "<td><strong>ფენოვანი</strong></td><td>სვანეთი და რაჭა</td><td>დაკეცილი სამკუთხედი</td><td>ყველი + კარტოფილი</td>", 1),
("<td><strong>Achma</strong></td><td>Adjara</td><td>Layered square, like lasagne</td><td>Unsalted cheese between layers</td>", "<td><strong>აჩმა</strong></td><td>აჭარა</td><td>ფენოვანი კვადრატი, ლაზანიასავით</td><td>უმარილო ყველი ფენებს შორის</td>", 1),
("If you are visiting Tbilisi for the first time, start with Imeretian (mild, universal, eaten for breakfast by most Georgians) and then move to Adjarian for the visual spectacle. Megrelian is for serious cheese lovers. Achma is served at celebrations and is rarely found outside home kitchens or specialist restaurants.",
 "თუ თბილისში პირველად ხართ, დაიწყეთ იმერულით (რბილი, უნივერსალური, რომელსაც ქართველების უმეტესობა საუზმეზე ჭამს) და შემდეგ გადადით აჭარულზე ვიზუალური სანახაობისთვის. მეგრული სერიოზული ყველის მოყვარულებისთვისაა. აჩმას ზეიმებზე მიირთმევენ და სახლის სამზარეულოს ან სპეციალიზებული რესტორნის გარეთ იშვიათად ნახავთ.", 1),
# BEST PLACES
("<h2 id=\"best-places\">7 best spots for Adjarian khachapuri in Tbilisi</h2>", "<h2 id=\"best-places\">7 საუკეთესო ადგილი აჭარული ხაჭაპურისთვის თბილისში</h2>", 1),
("<thead><tr><th>Place</th><th>District</th><th>Price</th><th>What to order</th></tr></thead>",
 "<thead><tr><th>ადგილი</th><th>უბანი</th><th>ფასი</th><th>რა შევუკვეთოთ</th></tr></thead>", 1),
("<td>Multiple locations</td><td>10–14 ₾</td><td>Adjarian khachapuri — chain, consistent quality</td>", "<td>რამდენიმე ლოკაცია</td><td>10–14 ₾</td><td>აჭარული ხაჭაპური — ქსელი, სტაბილური ხარისხი</td>", 1),
("<td>Old Town</td><td>15–18 ₾</td><td>Khachapuri + wine — literary atmosphere</td>", "<td>ძველი ქალაქი</td><td>15–18 ₾</td><td>ხაჭაპური + ღვინო — ლიტერატურული ატმოსფერო</td>", 1),
("<td>Old Town</td><td>12–16 ₾</td><td>All khachapuri varieties side by side</td>", "<td>ძველი ქალაქი</td><td>12–16 ₾</td><td>ხაჭაპურის ყველა სახეობა გვერდიგვერდ</td>", 1),
("<td>Vera</td><td>18–22 ₾</td><td>Premium version using a 19th-century recipe</td>", "<td>ვერა</td><td>18–22 ₾</td><td>პრემიუმ ვერსია XIX საუკუნის რეცეპტით</td>", 1),
("<td><strong>Deserter's Market bakery</strong></td><td>Didube</td><td>5–7 ₾</td><td>Cheapest authentic khachapuri in the city, baked in a tone oven</td>", "<td><strong>დეზერტირების ბაზრობის საცხობი</strong></td><td>დიდუბე</td><td>5–7 ₾</td><td>ყველაზე იაფი ავთენტური ხაჭაპური ქალაქში, თონეში გამომცხვარი</td>", 1),
("<td>Chughureti</td><td>14–18 ₾</td><td>Modern Georgian with excellent khachapuri selection</td>", "<td>ჩუღურეთი</td><td>14–18 ₾</td><td>თანამედროვე ქართული, ხაჭაპურის შესანიშნავი არჩევანით</td>", 1),
("<td><strong>Zakaria</strong></td><td>Agmashenebeli Ave</td><td>6–8 ₾</td><td>Neighbourhood place — locals only, extraordinary value</td>", "<td><strong>ზაქარია</strong></td><td>აღმაშენებლის გამზ.</td><td>6–8 ₾</td><td>უბნის ადგილი — მხოლოდ ადგილობრივები, არაჩვეულებრივი ფასი</td>", 1),
("<strong>Best value in the city:</strong> Deserter's Market (Dezerteris Bazroba) has a bakery section near the main entrance where khachapuri comes out of a tone oven fresh throughout the morning. At 5–7 ₾ for a full-sized Adjarian khachapuri, it is the most authentic version at the lowest price. Go before noon.",
 "<strong>საუკეთესო ფასი ქალაქში:</strong> დეზერტირების ბაზრობას მთავარ შესასვლელთან აქვს საცხობის სექცია, სადაც ხაჭაპური თონედან მთელი დილის განმავლობაში ახალი გამოდის. სრული ზომის აჭარული ხაჭაპური 5–7 ₾-ად — ეს ყველაზე ავთენტური ვერსიაა ყველაზე დაბალ ფასად. მიდით შუადღემდე.", 1),
# HOW TO EAT
("Eating Adjarian khachapuri correctly is not optional — the dish has a specific technique and a specific window of time. Here is the sequence.",
 "აჭარული ხაჭაპურის სწორად ჭამა არჩევითი არ არის — კერძს აქვს კონკრეტული ტექნიკა და კონკრეტული დროის ფანჯარა. აი, თანმიმდევრობა.", 1),
("<li><strong>Eat immediately.</strong> The moment it arrives, start. Do not photograph it for five minutes. The cheese cools and congeals, the egg overcooks, and the bread edge loses its crunch. Take one photo, then eat.</li>",
 "<li><strong>ჭამეთ მაშინვე.</strong> როგორც კი მოვა, დაიწყეთ. ხუთი წუთი ნუ გადაიღებთ. ყველი გაცივდება და შედედდება, კვერცხი გადაცხვება, პურის ნაპირი კი ხრაშუნას დაკარგავს. გადაუღეთ ერთი ფოტო და შეჭამეთ.</li>", 1),
("<li><strong>Mix the filling.</strong> Use a spoon (never a fork, never a knife) to mix the raw egg yolk and butter into the melted suluguni. You are looking for a uniform golden, glossy, lightly runny filling.</li>",
 "<li><strong>აურიეთ შიგთავსი.</strong> კოვზით (არასოდეს ჩანგლით, არასოდეს დანით) აურიეთ ნედლი კვერცხის გული და კარაქი გამდნარ სულგუნში. მიზანია ერთგვაროვანი, ოქროსფერი, პრიალა, ოდნავ თხევადი შიგთავსი.</li>", 1),
("<li><strong>Tear and dip.</strong> Tear off pieces of the bread boat edge and dip them directly into the filling. This is not a side action — the dipping is the main event. The bread absorbs the buttery, eggy cheese and becomes something distinct from bread alone.</li>",
 "<li><strong>მოხიეთ და ჩააწექით.</strong> მოხიეთ ნავის ნაპირის ნაჭრები და პირდაპირ შიგთავსში ჩააწექით. ეს არ არის მეორეხარისხოვანი ქმედება — ჩაწება მთავარი მოვლენაა. პური ისრუტავს კარაქიან, კვერცხიან ყველს და მარტო პურისგან განსხვავებულ რაღაცად იქცევა.</li>", 1),
("<li><strong>Eat the remaining crust.</strong> Once the filling is gone, the boat-shaped crust is still there. It has absorbed some of the cheese and butter from the outside during baking. Eat it. It is not a plate.</li>",
 "<li><strong>შეჭამეთ დარჩენილი ქერქი.</strong> შიგთავსის შემდეგ ნავის ფორმის ქერქი კვლავ რჩება. ცხობისას მან გარედან შეისრუტა ყველისა და კარაქის ნაწილი. შეჭამეთ. ის თეფში არ არის.</li>", 1),
("<strong>Common mistakes:</strong> Using cutlery. Eating the crust first. Waiting too long to start. Sharing a single portion between three people. Adjarian khachapuri is sized for one person — order one each.",
 "<strong>გავრცელებული შეცდომები:</strong> დანა-ჩანგლის გამოყენება. ჯერ ქერქის ჭამა. დაწყების ზედმეტად გვიან. ერთი ულუფის სამ ადამიანზე გაყოფა. აჭარული ხაჭაპური ერთ ადამიანზეა გათვლილი — შეუკვეთეთ თითო.", 1),
# GASTRO TOUR
("I run a gastro tour of Tbilisi that covers khachapuri, khinkali, local wine, and market food — all at authentic neighbourhood spots, not tourist restaurants. The tour visits 4–5 places over three to four hours.",
 "ვატარებ თბილისის გასტრო-ტურს, რომელიც მოიცავს ხაჭაპურს, ხინკალს, ადგილობრივ ღვინოსა და ბაზრის საჭმელს — ყველაფერს ავთენტურ, უბნის ადგილებში, არა ტურისტულ რესტორნებში. ტური სამ-ოთხ საათში 4–5 ადგილს ინახულებს.", 1),
("<h3>Gastro Tour of Tbilisi</h3>", "<h3>თბილისის გასტრო-ტური</h3>", 2),
("4–5 authentic spots · khachapuri, khinkali, wine, market food · from ₾165 per person",
 "4–5 ავთენტური ადგილი · ხაჭაპური, ხინკალი, ღვინო, ბაზრის საჭმელი · ₾165-დან ერთ ადამიანზე", 1),
("          Book via WhatsApp", "          დაჯავშნა WhatsApp-ით", 1),
("          Write in Telegram", "          მოგვწერეთ Telegram-ზე", 1),
("The tour also works as a standalone activity — if you want to understand Georgian food properly without spending three hours reading about it, this is the efficient way to do it. We cover history, technique, etiquette, and plenty of actual eating.",
 "ტური დამოუკიდებელ აქტივობადაც მუშაობს — თუ გინდათ ქართული საჭმელი კარგად გაიგოთ ისე, რომ სამი საათი მასზე კითხვას არ დახარჯოთ, ეს ეფექტური გზაა. ვფარავთ ისტორიას, ტექნიკას, ეტიკეტსა და უამრავ რეალურ ჭამას.", 1),
("Group size: 2–8 people. Duration: 3–4 hours. Meeting point: Marjanishvili metro station.",
 "ჯგუფის ზომა: 2–8 ადამიანი. ხანგრძლივობა: 3–4 საათი. შეხვედრის ადგილი: მარჯანიშვილის მეტროსადგური.", 1),
("Get 10% discount →", "მიიღეთ 10% ფასდაკლება →", 1),
# RELATED
("<h2>You may also like</h2>", "<h2>ასევე შეიძლება მოგეწონოთ</h2>", 1),
(">Guide</div>", ">გზამკვლევი</div>", 2),
("<h3>Georgian Food Guide</h3>", "<h3>ქართული საჭმლის გზამკვლევი</h3>", 1),
("15 essential dishes with real prices in GEL and the best local spots. Khinkali, shkmeruli, lobio and more.",
 "15 აუცილებელი კერძი რეალური ფასებით ლარებში და საუკეთესო ადგილობრივი ადგილები. ხინკალი, შქმერული, ლობიო და სხვა.", 1),
(">Read →</a>", ">წაიკითხე →</a>", 2),
("<h3>Best Restaurants in Tbilisi</h3>", "<h3>თბილისის საუკეთესო რესტორნები</h3>", 1),
("Where locals actually eat — from neighbourhood dukhanis to upscale Georgian cooking.",
 "სად ჭამენ ნამდვილად ადგილობრივები — უბნის დუქნებიდან მაღალი კლასის ქართულ სამზარეულომდე.", 1),
(">Tour</div>", ">ტური</div>", 1),
("Authentic local spots, market food, and Georgian wine. 3–4 hours with a local guide.",
 "ავთენტური ადგილობრივი ადგილები, ბაზრის საჭმელი და ქართული ღვინო. 3–4 საათი ადგილობრივ გიდთან.", 1),
(">Learn more →</a>", ">გაიგე მეტი →</a>", 1),
# TRIPADVISOR STRIP
("Rated 4.9/5 on TripAdvisor", "რეიტინგი 4.9/5 TripAdvisor-ზე", 1),
("90+ reviews from tourists who joined Timur's tours in Tbilisi", "90+ შეფასება ტურისტებისგან, რომლებიც თიმურის ტურებს შეუერთდნენ თბილისში", 1),
(">Read Reviews</a>", ">შეფასებების წაკითხვა</a>", 1),
# VISIBLE FAQ
("<h2>Frequently Asked Questions about Adjarian Khachapuri</h2>", "<h2>ხშირად დასმული კითხვები აჭარულ ხაჭაპურზე</h2>", 1),
("What is Adjarian khachapuri?<span", "რა არის აჭარული ხაჭაპური?<span", 1),
("Adjarian khachapuri is an open boat-shaped Georgian cheese bread filled with melted suluguni cheese, topped with a raw egg and a knob of butter added just before serving. It comes from the Adjara region on the Black Sea coast. The boat shape traditionally represents the fishing boats of the region.",
 "აჭარული ხაჭაპური არის ღია, ნავის ფორმის ქართული ყველიანი პური, გამდნარი სულგუნით, რომელსაც თავზე ადევს ნედლი კვერცხი და მირთმევის წინ დამატებული კარაქის ნაჭერი. ის აჭარის მხარიდან, შავი ზღვის სანაპიროდან მოდის. ნავის ფორმა ტრადიციულად მხარის სათევზაო ნავებს განასახიერებს.", 1),
("How much does Adjarian khachapuri cost in Tbilisi?<span", "რა ღირს აჭარული ხაჭაპური თბილისში?<span", 1),
("At local cafes and bakeries: 5–8 GEL. At mid-range restaurants: 12–18 GEL. At tourist restaurants in the Old Town: 18–25 GEL. The cheapest authentic version is at Deserter's Market bakery — 5–7 GEL, freshly baked in a tone oven.",
 "ადგილობრივ კაფეებსა და საცხობებში: 5–8 ლარი. საშუალო კლასის რესტორნებში: 12–18 ლარი. ძველ ქალაქში ტურისტულ რესტორნებში: 18–25 ლარი. ყველაზე იაფი ავთენტური ვერსია დეზერტირების ბაზრობის საცხობშია — 5–7 ლარი, თონეში ახლად გამომცხვარი.", 1),
("How do you eat Adjarian khachapuri correctly?<span", "როგორ ვჭამოთ აჭარული ხაჭაპური სწორად?<span", 1),
("Eat it immediately — do not photograph it for five minutes first. Mix the egg yolk and butter into the melted cheese with a spoon. Tear off pieces of the bread boat edge and dip them into the filling. Finally, eat the remaining crust. Do not use a knife and fork.",
 "ჭამეთ მაშინვე — ჯერ ხუთი წუთი ნუ გადაიღებთ. კოვზით აურიეთ კვერცხის გული და კარაქი გამდნარ ყველში. მოხიეთ ნავის ნაპირის ნაჭრები და ჩააწექით შიგთავსში. ბოლოს შეჭამეთ დარჩენილი ქერქი. ნუ გამოიყენებთ დანა-ჩანგალს.", 1),
("What is the difference between Adjarian and Imeretian khachapuri?<span", "რა განსხვავებაა აჭარულ და იმერულ ხაჭაპურს შორის?<span", 1),
("Adjarian: open boat shape, suluguni cheese filling, raw egg cracked on top, butter added before serving. Must be eaten hot immediately. Imeretian: closed round flatbread filled with mild imeruli cheese — the everyday version eaten throughout Georgia for breakfast, milder and easier to handle.",
 "აჭარული: ღია ნავის ფორმა, სულგუნის შიგთავსი, თავზე ჩარტყმული ნედლი კვერცხი, მირთმევის წინ დამატებული კარაქი. ცხელი უნდა შეიჭამოს მაშინვე. იმერული: დახურული მრგვალი ლავაში, რბილი იმერული ყველით — ყოველდღიური ვერსია, რომელსაც მთელ საქართველოში საუზმეზე ჭამენ, უფრო რბილი და მოსახერხებელი.", 1),
("Can you make Adjarian khachapuri at home?<span", "შესაძლებელია აჭარული ხაჭაპურის სახლში მომზადება?<span", 1),
("Yes. Make a dough from matzoni or kefir, flour, salt, and yeast. Rest 30 minutes. Fill with grated suluguni, shape into a boat, bake at 220–230°C for 15–18 minutes, then crack the egg into the centre and bake 3–4 more minutes until the white sets but the yolk remains runny. Drop in butter and serve immediately.",
 "დიახ. მოზილეთ ცომი მაწვნით ან კეფირით, ფქვილით, მარილითა და საფუარით. დაასვენეთ 30 წუთი. შეავსეთ გახეხილი სულგუნით, ჩამოაყალიბეთ ნავის ფორმა, გამოაცხვეთ 220–230°C-ზე 15–18 წუთი, შემდეგ ცენტრში ჩაარტყით კვერცხი და კიდევ 3–4 წუთი აცხვეთ, სანამ ცილა შედედდება, გული კი თხევადი დარჩება. ჩადეთ კარაქი და მაშინვე მიირთვით.", 1),
("Which area of Tbilisi has the best Adjarian khachapuri?<span", "თბილისის რომელ უბანშია საუკეთესო აჭარული ხაჭაპური?<span", 1),
("The best value is found along Agmashenebeli Avenue, around Marjanishvili Square, and in the Didube area. These are working-class neighbourhoods where locals eat — no tourist markup, and the khachapuri is made fresh all morning.",
 "საუკეთესო ფასად ნახავთ აღმაშენებლის გამზირზე, მარჯანიშვილის მოედნის მიდამოებსა და დიდუბის რაიონში. ეს სამუშაო კლასის უბნებია, სადაც ადგილობრივები ჭამენ — ტურისტული ზედნადების გარეშე, ხაჭაპური კი მთელი დილის განმავლობაში ახლად ცხვება.", 1),
("Where does Adjarian khachapuri come from?<span", "საიდან მოდის აჭარული ხაჭაპური?<span", 1),
("From the Adjara region in southwestern Georgia on the Black Sea coast, centred on Batumi. The boat shape represents the fishing boats of the region. Georgian bread culture was inscribed on the UNESCO Intangible Cultural Heritage list in 2022.",
 "სამხრეთ-დასავლეთ საქართველოს აჭარის მხარიდან, შავი ზღვის სანაპიროდან, ბათუმის ცენტრით. ნავის ფორმა მხარის სათევზაო ნავებს განასახიერებს. ქართული პურის კულტურა 2022 წელს UNESCO-ს არამატერიალური კულტურული მემკვიდრეობის სიაში შევიდა.", 1),
("Can I join a gastro tour to try khachapuri in Tbilisi?<span", "შემიძლია შევუერთდე გასტრო-ტურს, რომ თბილისში ხაჭაპური დავაგემოვნო?<span", 1),
("Yes. Sakhva Travel runs a gastro tour of Tbilisi visiting 4–5 authentic local spots. The tour covers khachapuri, khinkali, local wine, and market food. From ₾165 per person. Book via WhatsApp: +995511272623.",
 "დიახ. Sakhva Travel ატარებს თბილისის გასტრო-ტურს 4–5 ავთენტური ადგილის მონახულებით. ტური მოიცავს ხაჭაპურს, ხინკალს, ადგილობრივ ღვინოსა და ბაზრის საჭმელს. ₾165-დან ერთ ადამიანზე. დაჯავშნა WhatsApp-ით: +995511272623.", 1),
("Read in Russian", "წაიკითხე რუსულად", 1),
# LEAD MAGNET
("Guide: 15 places in Tbilisi not in any guidebook + 5% off", "გზამკვლევი: 15 ადგილი თბილისში, რომელიც არცერთ გიდში არ არის + 5% ფასდაკლება", 1),
(">Get it</button>", ">მიღება</button>", 1),
("Sent — check your inbox", "გაიგზავნა — შეამოწმეთ ფოსტა", 1),
# READY TO EXPLORE
("Ready to explore Georgia?", "მზად ხართ საქართველოს გასაცნობად?", 1),
(">Browse all tours in Georgia</a>", ">ყველა ტური საქართველოში</a>", 1),
(">Tours in Tbilisi</a>", ">ტურები თბილისში</a>", 1),
(">Wine tours</a>", ">ღვინის ტურები</a>", 1),
# AUTHOR BIO
("Private tours in Tbilisi since 2023. 500+ tours completed. 4.9/5 rating on Google. Living in Georgia, knowing the country from inside.",
 "ინდივიდუალური ტურები თბილისში 2023 წლიდან. 500+ ჩატარებული ტური. რეიტინგი 4.9/5 Google-ზე. ვცხოვრობ საქართველოში, ქვეყანას შიგნიდან ვიცნობ.", 1),
(">Book a Tour</a>", ">დაჯავშნე ტური</a>", 1),
# FOOTER
("Private tours in Georgia 2026. Tbilisi, Kazbegi, Kakheti.", "ინდივიდუალური ტურები საქართველოში 2026. თბილისი, ყაზბეგი, კახეთი.", 1),
("<h4>Tours</h4>", "<h4>ტურები</h4>", 1),
(">Kazbegi Day Trip — from ₾175</a>", ">ერთდღიანი ტური ყაზბეგში — ₾175-დან</a>", 1),
(">Hidden Tbilisi — from ₾100</a>", ">დამალული თბილისი — ₾100-დან</a>", 1),
(">Kakheti Wine Tour — from ₾170</a>", ">ღვინის ტური კახეთში — ₾170-დან</a>", 1),
(">Guide: Kazbegi 2026</a>", ">გზამკვლევი: ყაზბეგი 2026</a>", 1),
(">15 Hidden Gems in Tbilisi</a>", ">თბილისის 15 დამალული საგანძური</a>", 1),
(">Georgian Food Guide</a>", ">ქართული საჭმლის გზამკვლევი</a>", 1),
(">Adjarian Khachapuri</a>", ">აჭარული ხაჭაპური</a>", 1),
("© 2026 Sakhva Travel · Tbilisi, Georgia", "© 2026 Sakhva Travel · თბილისი, საქართველო", 1),
(">Leave a review ★</a>", ">დატოვე შეფასება ★</a>", 1),
(">Contact</a>", ">კონტაქტი</a>", 1),
# CONTACT MODAL
("Get 10% off your first tour", "მიიღეთ 10% ფასდაკლება პირველ ტურზე", 1),
("Leave your contact details and Timur will get back to you within 2 hours with a personalised offer.",
 "დატოვეთ საკონტაქტო მონაცემები და თიმური 2 საათში დაგიკავშირდებათ პერსონალური შეთავაზებით.", 1),
("placeholder=\"Your name\"", "placeholder=\"თქვენი სახელი\"", 1),
("placeholder=\"WhatsApp or phone number\"", "placeholder=\"WhatsApp ან ტელეფონის ნომერი\"", 1),
(">Send request</button>", ">განაცხადის გაგზავნა</button>", 1),
]

def main():
    html = F.read_text(encoding="utf-8")
    problems = []
    for i, (old, new, *exp) in enumerate(R):
        want = exp[0] if exp else 1
        cnt = html.count(old)
        if cnt != want:
            problems.append(f"[{i}] ожидал {want}, нашёл {cnt}: {old[:55]!r}")
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
