#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перевод EN->KA пилота /ge/kakheti/. Анкер-замены + счётчик."""
import sys
from pathlib import Path
F = Path("/Users/vladimir/sakhva-travel/ge/kakheti/index.html")

R = [
# TITLE / META / OG / TWITTER
("Kakheti — Wine Region, Sighnaghi & Alazani Valley | Sakhva Travel", "კახეთი — ღვინის მხარე, სიღნაღი და ალაზნის ველი | Sakhva Travel", 1),  # og:image:alt (длиннее — раньше)
("Kakheti — Wine Region, Sighnaghi & Alazani Valley", "კახეთი — ღვინის მხარე, სიღნაღი და ალაზნის ველი", 1),  # title (literal &)
("Kakheti — Wine Region, Sighnaghi &amp; Alazani Valley", "კახეთი — ღვინის მხარე, სიღნაღი და ალაზნის ველი", 2),  # og/twitter title
("Kakheti wine region: Telavi, Sighnaghi, Alaverdi monastery, qvevri wineries, Alazani Valley. Day trips and multi-day tours with a private tour from Tbilisi.",
 "კახეთის ღვინის მხარე: თელავი, სიღნაღი, ალავერდის მონასტერი, ქვევრის მარნები, ალაზნის ველი. ერთდღიანი და მრავალდღიანი ტურები კერძო გიდთან თბილისიდან.", 1),
("content=\"Timur — Sakhva Travel\"", "content=\"თიმური — Sakhva Travel\"", 1),
("Kakheti — Georgia's wine region: Sighnaghi, Telavi, Alazani Valley, Bodbe Monastery. 1:50 from Tbilisi.",
 "კახეთი — საქართველოს ღვინის მხარე: სიღნაღი, თელავი, ალაზნის ველი, ბოდბის მონასტერი. თბილისიდან 1:50.", 1),
("Kakheti — wine region: Sighnaghi, Telavi, Alazani Valley, Bodbe. 1:50 from Tbilisi.",
 "კახეთი — ღვინის მხარე: სიღნაღი, თელავი, ალაზნის ველი, ბოდბე. თბილისიდან 1:50.", 1),
# BREADCRUMB schema
("\"name\":\"Home\"", "\"name\":\"მთავარი\"", 1),
("\"name\":\"Regions\"", "\"name\":\"მხარეები\"", 1),
("\"name\":\"Kakheti\"", "\"name\":\"კახეთი\"", 1),
# FAQ schema-only answers (тексты отличаются от видимых)
("Tbilisi to Kakheti is 110 km, about 1h50m by car. Minibus from Samgori metro (5-7 lari) or private transfer. Most convenient: guided tour with hotel pickup and drop-off.",
 "თბილისიდან კახეთამდე 110 კმ, მანქანით დაახლოებით 1სთ 50წთ. მარშრუტკა სამგორის მეტროდან (5-7 ლარი) ან კერძო ტრანსფერი. ყველაზე მოხერხებული: ტური გიდთან, სასტუმროდან წამოყვანითა და დაბრუნებით.", 1),
("Best time: September-October during rtveli (grape harvest). Spring (April-May) also lovely: blooming valleys, few tourists. Summer hot (up to +38°C) but wineries have AC. Winter quiet and atmospheric.",
 "საუკეთესო დრო: სექტემბერ-ოქტომბერი, რთველის დროს (ყურძნის მოსავალი). გაზაფხულიც (აპრილი-მაისი) მშვენიერია: აყვავებული ველები, ცოტა ტურისტი. ზაფხული ცხელა (+38°C-მდე), მაგრამ მარნებში კონდიციონერია. ზამთარი მშვიდი და ატმოსფერულია.", 1),
("One day: Bodbe Monastery, Sighnaghi (city of love) with Alazani Valley views, family winery tasting with qvevri. Via Telavi: add Alaverdi Cathedral and Gremi Castle. Both routes available as day trips from Tbilisi.",
 "ერთ დღეში: ბოდბის მონასტერი, სიღნაღი (სიყვარულის ქალაქი) ალაზნის ველის ხედებით, ოჯახურ მარანში დეგუსტაცია ქვევრით. თელავის გავლით: დაამატეთ ალავერდის ტაძარი და გრემის ციხე. ორივე მარშრუტი ხელმისაწვდომია ერთდღიან ტურად თბილისიდან.", 1),
("Must-try: Saperavi (dry red), Rkatsiteli (white aged in qvevri), Kindzmarauli (semi-sweet red), Mukuzani (aged red). At family wineries try amber wine — orange-hued with tannins, unique style.",
 "აუცილებლად: საფერავი (მშრალი წითელი), რქაწითელი (ქვევრში დავარგებული თეთრი), ქინძმარაული (ნახევრადტკბილი წითელი), მუკუზანი (დავარგებული წითელი). ოჯახურ მარნებში დააგემოვნეთ ქარვისფერი ღვინო — ნარინჯისფერი, ტანინებით, უნიკალური სტილი.", 1),
# FAQ questions (schema name + visible span идентичны) -> count 2
("How to get to Kakheti from Tbilisi?", "როგორ მივიდე კახეთში თბილისიდან?", 2),
("How much does a guided Kakheti tour cost?", "რა ღირს კახეთის ტური გიდთან?", 2),
("When is the best time to visit Kakheti?", "როდის არის კახეთის მონახულების საუკეთესო დრო?", 2),
("What are the must-sees for one day?", "რა უნდა ვნახო აუცილებლად ერთ დღეში?", 2),
("What wines to try in Kakheti?", "რომელი ღვინოები დავაგემოვნო კახეთში?", 2),
# FAQ a2 идентичен schema+visible -> count 2
("A Kakheti tour with a private tour from Sakhva Travel starts from 170 lari per person (~60 EUR). The price includes hotel transfer, full-day guide services, entrance tickets and wine tasting. Groups up to 7.",
 "კახეთის ტური Sakhva Travel-ის კერძო გიდთან იწყება 170 ლარიდან ერთ ადამიანზე (~60 ევრო). ფასში შედის სასტუმროდან ტრანსფერი, გიდის სრული დღის მომსახურება, შესვლის ბილეთები და ღვინის დეგუსტაცია. ჯგუფები 7 ადამიანამდე.", 2),
# NAV / DRAWER
(">Tours in Georgia<", ">ტურები საქართველოში<", 2),
(">Excursions<", ">ექსკურსიები<", 2),
(">Prices<", ">ფასები<", 2),
(">About<", ">ჩვენ შესახებ<", 2),
(">Reviews<", ">შეფასებები<", 2),
(">Media<", ">მედია<", 2),
(">Blog<", ">ბლოგი<", 2),
(">FAQ<", ">FAQ<", 2),
(">Contacts<", ">კონტაქტები<", 2),
(">Book Online</a>", ">დაჯავშნა ონლაინ</a>", 1),
(">Book Now</a>", ">დაჯავშნა</a>", 1),
("aria-label=\"Menu\"", "aria-label=\"მენიუ\"", 1),
# HERO
(">Home</a>", ">მთავარი</a>", 1),
(">Regions</a>", ">მხარეები</a>", 1),
("<strong>Kakheti</strong>", "<strong>კახეთი</strong>", 1),
("Kakheti — Wine Country and the Alazani Valley", "კახეთი — ღვინის მხარე და ალაზნის ველი", 1),
("<div class=\"rd-city\">Tbilisi</div>", "<div class=\"rd-city\">თბილისი</div>", 1),
("<div class=\"rd-city\">Batumi</div>", "<div class=\"rd-city\">ბათუმი</div>", 1),
("<div class=\"rd-city\">Kutaisi</div>", "<div class=\"rd-city\">ქუთაისი</div>", 1),
# BODY: About Kakheti
("<h2>About Kakheti</h2>", "<h2>კახეთის შესახებ</h2>", 1),
("Kakheti occupies the entire eastern edge of Georgia — from the snow-capped Greater Caucasus peaks in the north to the semi-deserts of David Gareja in the south. Just over three hundred thousand people live here, yet this region feeds and wines the entire country: more than half of Georgia's vineyards are located in the Alazani Valley, at an elevation of 200-450 meters above sea level.",
 "კახეთი იკავებს საქართველოს მთელ აღმოსავლეთ კიდეს — ჩრდილოეთში დიდი კავკასიონის თოვლიანი მწვერვალებიდან სამხრეთში დავით გარეჯის ნახევრადუდაბნოებამდე. აქ ცოტა მეტი, ვიდრე სამასი ათასი ადამიანი ცხოვრობს, თუმცა ეს მხარე მთელ ქვეყანას კვებავს და ღვინით ამარაგებს: საქართველოს ვენახების ნახევარზე მეტი ალაზნის ველშია, ზღვის დონიდან 200-450 მეტრ სიმაღლეზე.", 1),
("Winemaking in Kakheti is not an industry but a way of life. Archaeologists found stone wine presses and fragments of qvevri (clay vessels for fermentation) here dating back over eight thousand years. These are the oldest evidence of winemaking on the planet — which is why UNESCO added the Georgian qvevri method to its Intangible Cultural Heritage list. I take groups to family maranis where the fourth generation of winemakers still buries qvevri in the ground and makes wine the way their great-grandfathers did.",
 "მეღვინეობა კახეთში არა ინდუსტრია, არამედ ცხოვრების წესია. არქეოლოგებმა აქ იპოვეს ქვის საწნახელები და ქვევრის (თიხის ჭურჭელი დუღილისთვის) ფრაგმენტები, რვა ათას წელზე მეტის დათარიღებით. ეს პლანეტაზე მეღვინეობის უძველესი კვალია — სწორედ ამიტომ UNESCO-მ ქართული ქვევრის მეთოდი არამატერიალური კულტურული მემკვიდრეობის სიაში შეიტანა. ჯგუფებს დავყავარ ოჯახურ მარნებში, სადაც მეღვინეთა მეოთხე თაობა დღემდე მარხავს ქვევრს მიწაში და ღვინოს ისე აყენებს, როგორც მათი დიდი ბაბუები.", 1),
("The Alazani Valley is the heart of the region. On one side it is embraced by the Caucasus Range, on the other by the Tsivi-Gombori mountains. Between them stretches a flat, sun-drenched plain where Saperavi, Rkatsiteli, Mtsvane and over five hundred indigenous grape varieties grow. In autumn, September-October, rtveli begins — the grape harvest. The entire valley smells of crushed grapes, courtyards fill with songs, and every home offers young wine. If you want to see the real Georgia unfiltered — come to Kakheti during rtveli.",
 "ალაზნის ველი მხარის გულია. ერთი მხრიდან მას კავკასიონის ქედი ეხუტება, მეორე მხრიდან — ცივ-გომბორის მთები. მათ შორის გადაჭიმულია ბრტყელი, მზით გაჟღენთილი ვაკე, სადაც იზრდება საფერავი, რქაწითელი, მწვანე და ხუთასზე მეტი ადგილობრივი ყურძნის ჯიში. შემოდგომაზე, სექტემბერ-ოქტომბერში, იწყება რთველი — ყურძნის მოსავალი. მთელ ველს დაჭყლეტილი ყურძნის სუნი ასდის, ეზოები სიმღერებით ივსება და ყოველი სახლი ახალ ღვინოს გთავაზობთ. თუ გინდათ ნახოთ ნამდვილი, გაუფილტრავი საქართველო — ეწვიეთ კახეთს რთველის დროს.", 1),
("The regional capital is Telavi, a city with a thousand-year history. The beloved Soviet film \"Mimino\" was shot here, and the plane tree in the courtyard of King Heraclius II's fortress still stands — it's seven hundred years old. And the town of Sighnaghi, dubbed the \"city of love,\" sits on a hill above the Alazani Valley, encircled by fortress walls with twenty-three towers. The local registry office performs weddings 24/7, no appointment needed — and yes, it actually works.",
 "მხარის დედაქალაქი თელავია, ათასწლოვანი ისტორიის ქალაქი. აქ გადაიღეს საყვარელი საბჭოთა ფილმი „მიმინო“, ხოლო მეფე ერეკლე II-ის ციხის ეზოში დღემდე დგას ჭადარი — შვიდასი წლისაა. ქალაქი სიღნაღი კი, რომელსაც „სიყვარულის ქალაქს“ ეძახიან, ალაზნის ველის ზემოთ, გორაკზეა გაშენებული და ოცდაცამეტკოშკიანი ციხის კედლებითაა შემოზღუდული. ადგილობრივი მოქალაქეობის აქტების რეგისტრაციის სამსახური ქორწინებებს ატარებს 24/7, წინასწარი ჩაწერის გარეშე — და კი, ეს ნამდვილად მუშაობს.", 1),
# What to See
("<h2>What to See in Kakheti</h2>", "<h2>რა ვნახოთ კახეთში</h2>", 1),
("<h3>Sighnaghi — City of Love</h3>", "<h3>სიღნაღი — სიყვარულის ქალაქი</h3>", 1),
("A small town with cobblestone streets, Italian-style balconies and a breathtaking panorama of the Alazani Valley. The 4th-century fortress wall encircles the entire hill — walk along it for a bird's-eye view of the valley. Sighnaghi is often compared to Italian towns, and the resemblance is truly striking. I recommend arriving for sunset — when the sun sets behind the Alazani Valley, the sky turns purple and the mountains on the horizon glow blue.",
 "პატარა ქალაქი ქვაფენილიანი ქუჩებით, იტალიური სტილის აივნებითა და ალაზნის ველის თვალწარმტაცი პანორამით. IV საუკუნის ციხის კედელი მთელ გორაკს შემოუყვება — გაჰყევით მას ველის ჩიტის თვალით სახედავად. სიღნაღს ხშირად ადარებენ იტალიურ ქალაქებს და მსგავსება მართლაც თვალშისაცემია. გირჩევთ მისვლას მზის ჩასვლისას — როცა მზე ალაზნის ველს უკან ჩადის, ცა იისფრდება და ჰორიზონტზე მთები ლურჯად ბრწყინავს.", 1),
("<h3>Bodbe Monastery</h3>", "<h3>ბოდბის მონასტერი</h3>", 1),
("Two kilometers from Sighnaghi stands Bodbe Monastery — the burial place of Saint Nino, who converted Georgia to Christianity. The grounds are lush with cypresses, and from the viewing platform you can see the entire Alazani Valley. Below, in the forest, there's a holy spring with a baptismal font — the water is ice-cold year-round. Bodbe is an active convent; visitors are asked to cover their heads and shoulders.",
 "სიღნაღიდან ორ კილომეტრში დგას ბოდბის მონასტერი — წმინდა ნინოს განსასვენებელი, რომელმაც საქართველო გააქრისტიანა. ეზო კვიპაროსებითაა სავსე, ხოლო სანახავი მოედნიდან მთელი ალაზნის ველი ჩანს. ქვემოთ, ტყეში, არის წმინდა წყარო ნათლობის აუზით — წყალი მთელი წელი ყინულივით ცივია. ბოდბე მოქმედი დედათა მონასტერია; მნახველებს სთხოვენ თავისა და მხრების დაფარვას.", 1),
("<h3>Alaverdi Cathedral</h3>", "<h3>ალავერდის ტაძარი</h3>", 1),
("An 11th-century cathedral standing 50 meters tall — until Tsminda Sameba was built in Tbilisi, it was the tallest church in Georgia. Alaverdi stands in the middle of the plain, its silhouette visible for kilometers. The grounds grow peaches, olives and grapes, and monks still make wine in the monastery's marani. The cathedral is nominated for UNESCO listing.",
 "XI საუკუნის ტაძარი 50 მეტრი სიმაღლისა — სანამ თბილისში წმინდა სამება აშენდებოდა, ის საქართველოში ყველაზე მაღალი ეკლესია იყო. ალავერდი ვაკის შუაგულში დგას და მისი სილუეტი კილომეტრებზე ჩანს. ეზოში ხარობს ატამი, ზეთისხილი და ყურძენი, ბერები კი დღემდე აყენებენ ღვინოს მონასტრის მარანში. ტაძარი UNESCO-ს სიაში შესატანადაა წარდგენილი.", 1),
("<h3>Gremi Castle</h3>", "<h3>გრემის ციხე</h3>", 1),
("Former capital of the Kakhetian Kingdom — a hilltop fortress with the 16th-century Church of the Archangels. Frescoes are preserved inside, and from the tower you can see the entire valley. Nearby is a small museum with excavation artifacts. Gremi was destroyed by the Persian invasion of 1615, but the church and royal tower survived.",
 "კახეთის სამეფოს ყოფილი დედაქალაქი — გორაზე მდებარე ციხე XVI საუკუნის მთავარანგელოზთა ეკლესიით. შიგნით შემორჩენილია ფრესკები, ხოლო კოშკიდან მთელი ველი ჩანს. ახლოს არის პატარა მუზეუმი გათხრების არტეფაქტებით. გრემი 1615 წლის სპარსეთის შემოსევამ გაანადგურა, მაგრამ ეკლესია და სამეფო კოშკი გადარჩა.", 1),
("<h3>Tsinandali</h3>", "<h3>წინანდალი</h3>", 1),
("The Chavchavadze princes' estate — the first European-style manor in Georgia. Alexander Griboyedov visited here (he married Nino Chavchavadze), as did Alexandre Dumas and others. Today it's a museum, garden and wine cellar — one of the largest collections of Georgian wines. You can taste 19th-century wines if you're willing to pay several hundred lari per bottle.",
 "ჭავჭავაძეების სათავადო მამული — საქართველოში პირველი ევროპული სტილის სასახლე. აქ სტუმრობდნენ ალექსანდრე გრიბოედოვი (რომელიც ნინო ჭავჭავაძეზე დაქორწინდა), ალექსანდრ დიუმა და სხვები. დღეს ეს არის მუზეუმი, ბაღი და ღვინის მარანი — ქართული ღვინოების ერთ-ერთი უდიდესი კოლექცია. შეგიძლიათ დააგემოვნოთ XIX საუკუნის ღვინოები, თუ მზად ხართ ბოთლში რამდენიმე ასეული ლარი გადაიხადოთ.", 1),
("<h3>Kvareli and Lake Ilia</h3>", "<h3>ყვარელი და ილიას ტბა</h3>", 1),
("The town of Kvareli is the birthplace of Kindzmarauli wine. The eponymous winery is here, along with the man-made Lake Ilia surrounded by mountains. Painter Niko Pirosmani was born in Kvareli — his house-museum in Mirzaani village is worth visiting to understand the origins of this naive yet profound Georgian style.",
 "ქალაქი ყვარელი ქინძმარაულის ღვინის სამშობლოა. აქ არის ამავე სახელწოდების მარანი და ხელოვნური ილიას ტბა, მთებით გარშემორტყმული. ყვარელში დაიბადა მხატვარი ნიკო ფიროსმანი — მისი სახლ-მუზეუმი სოფელ მირზაანში ღირს მოსანახულებლად, რომ გაიგოთ ამ გულუბრყვილო, მაგრამ ღრმა ქართული სტილის სათავე.", 1),
("<h3>Nekresi</h3>", "<h3>ნეკრესი</h3>", 1),
("A monastic complex on a mountain above the Alazani Valley. The ascent is by shuttle bus on a switchback road. At the top — ruins of a 4th-century palace and a panorama worth the trip alone. Nekresi is one of the earliest Christian sites in Georgia.",
 "სამონასტრო კომპლექსი მთაზე, ალაზნის ველის ზემოთ. ასვლა ხდება სამარშრუტო ავტობუსით, სერპანტინის გზაზე. ზემოთ — IV საუკუნის სასახლის ნანგრევები და პანორამა, რომელიც მარტო თავისთავად ღირს მოგზაურობად. ნეკრესი საქართველოში ერთ-ერთი ადრეული ქრისტიანული ადგილია.", 1),
# When to Visit
("<h2>When to Visit and What to Bring</h2>", "<h2>როდის ეწვიოთ და რა წამოიღოთ</h2>", 1),
("<strong>Best time:</strong> September-October (rtveli harvest, perfect weather, +22-28°C) and April-May (blooming, few tourists). Summer is hot — up to +38°C in the valley, but wineries have AC. Winter is mild (+2-8°C), quiet and atmospheric, especially at Christmas.",
 "<strong>საუკეთესო დრო:</strong> სექტემბერ-ოქტომბერი (რთველი, იდეალური ამინდი, +22-28°C) და აპრილ-მაისი (აყვავება, ცოტა ტურისტი). ზაფხული ცხელა — ველში +38°C-მდე, მაგრამ მარნებში კონდიციონერია. ზამთარი რბილია (+2-8°C), მშვიდი და ატმოსფერული, განსაკუთრებით შობას.", 1),
("<strong>What to bring:</strong> comfortable shoes for walking Sighnaghi's cobblestone streets, head covering for monasteries (women — headscarf, men — long pants). Sunscreen is essential May-September. Cash lari — village maranis don't accept cards.",
 "<strong>რა წამოიღოთ:</strong> კომფორტული ფეხსაცმელი სიღნაღის ქვაფენილიან ქუჩებში სასეირნოდ, თავსაბურავი მონასტრებისთვის (ქალები — თავსაფარი, კაცები — გრძელი შარვალი). მზისგან დამცავი კრემი აუცილებელია მაისი-სექტემბერში. ნაღდი ლარი — სოფლის მარნები ბარათებს არ იღებენ.", 1),
("<strong>Getting there:</strong> Tbilisi to Sighnaghi is 110 km, about 1 hour 50 minutes by car. To Telavi slightly further, via the scenic Gombori Pass (1,816 m). Minibuses run from Samgori metro station (5-7 lari), but with a guide it's more convenient: we pick you up from your hotel, show everything along the way and drive you back.",
 "<strong>როგორ მიხვიდეთ:</strong> თბილისიდან სიღნაღამდე 110 კმ, მანქანით დაახლოებით 1 საათი და 50 წუთი. თელავამდე ოდნავ შორსაა, თვალწარმტაცი გომბორის უღელტეხილის (1816 მ) გავლით. მარშრუტკები დადიან სამგორის მეტროსადგურიდან (5-7 ლარი), მაგრამ გიდთან უფრო მოხერხებულია: სასტუმროდან წამოგიყვანთ, გზადაგზა ყველაფერს გაჩვენებთ და უკან დაგაბრუნებთ.", 1),
# Tours
("<h2>Our Wine Tours in Kakheti</h2>", "<h2>ჩვენი ღვინის ტურები კახეთში</h2>", 1),
("alt=\"Wine Tasting in Kakheti — Tour from Tbilisi\"", "alt=\"ღვინის დეგუსტაცია კახეთში — ტური თბილისიდან\"", 1),
(">Wine Tasting in Kakheti</a>", ">ღვინის დეგუსტაცია კახეთში</a>", 1),
("alt=\"Sighnaghi Tour — City of Love\"", "alt=\"სიღნაღის ტური — სიყვარულის ქალაქი\"", 1),
(">Sighnaghi Tour</a>", ">სიღნაღის ტური</a>", 1),
("alt=\"Telavi and Alazani Valley Tour\"", "alt=\"თელავისა და ალაზნის ველის ტური\"", 1),
(">Telavi Tour</a>", ">თელავის ტური</a>", 1),
("Full day · up to 7 pax", "სრული დღე · 7 ადამიანამდე", 3),
("от ₾170", "₾170-დან", 3),
(">Details →</a>", ">დეტალები →</a>", 3),
# Region CTA
("Want a custom wine tour in Kakheti?", "გინდათ ინდივიდუალური ღვინის ტური კახეთში?", 1),
("Message Timur — we'll plan a route for you. Reply within 15 minutes.", "მოწერეთ თიმურს — მარშრუტს თქვენთვის დავგეგმავთ. პასუხი 15 წუთში.", 1),
# FAQ visible (тексты отличаются от schema)
("<h2>FAQ about Kakheti</h2>", "<h2>ხშირად დასმული კითხვები კახეთზე</h2>", 1),
("Tbilisi to Kakheti is 110 km, about 1 hour 50 minutes by car. You can take a minibus from Samgori metro (5-7 lari) or book a private transfer. The most convenient option is a ",
 "თბილისიდან კახეთამდე 110 კმ, მანქანით დაახლოებით 1 საათი და 50 წუთი. შეგიძლიათ მარშრუტკით სამგორის მეტროდან (5-7 ლარი) ან დაჯავშნოთ კერძო ტრანსფერი. ყველაზე მოხერხებული ვარიანტია ", 1),
(">guided tour</a>: hotel pickup and drop-off.", ">ტური გიდთან</a>: სასტუმროდან წამოყვანა და დაბრუნება.", 1),
("Best time is September-October during rtveli (grape harvest). Spring (April-May) is also lovely: blooming valleys and few tourists. Summer is hot (up to +38°C) but wineries have AC. Winter is quiet and atmospheric.",
 "საუკეთესო დროა სექტემბერ-ოქტომბერი, რთველის დროს (ყურძნის მოსავალი). გაზაფხულიც (აპრილი-მაისი) მშვენიერია: აყვავებული ველები და ცოტა ტურისტი. ზაფხული ცხელა (+38°C-მდე), მაგრამ მარნებში კონდიციონერია. ზამთარი მშვიდი და ატმოსფერულია.", 1),
("Bodbe Monastery, the city of love Sighnaghi with views of Alazani Valley, and a tasting at a family winery with qvevri. Via Telavi — add Alaverdi Cathedral and Gremi Castle.",
 "ბოდბის მონასტერი, სიყვარულის ქალაქი სიღნაღი ალაზნის ველის ხედებით და დეგუსტაცია ოჯახურ მარანში ქვევრით. თელავის გავლით — დაამატეთ ალავერდის ტაძარი და გრემის ციხე.", 1),
("Must-try: Saperavi (dry red), Rkatsiteli (white from qvevri), Kindzmarauli (semi-sweet red) and Mukuzani (aged red). At family wineries try homemade amber wine — orange-hued, tannic, a completely unique style.",
 "აუცილებლად: საფერავი (მშრალი წითელი), რქაწითელი (თეთრი ქვევრიდან), ქინძმარაული (ნახევრადტკბილი წითელი) და მუკუზანი (დავარგებული წითელი). ოჯახურ მარნებში დააგემოვნეთ ხელნაკეთი ქარვისფერი ღვინო — ნარინჯისფერი, ტანინიანი, სრულიად უნიკალური სტილი.", 1),
# Other regions
("<h2>Other Regions of Georgia</h2>", "<h2>საქართველოს სხვა მხარეები</h2>", 1),
(">Mtskheta-Mtianeti</a>", ">მცხეთა-მთიანეთი</a>", 1),
(">Adjara</a>", ">აჭარა</a>", 1),
(">Imereti</a>", ">იმერეთი</a>", 1),
(">Samtskhe-Javakheti</a>", ">სამცხე-ჯავახეთი</a>", 1),
(">Shida Kartli</a>", ">შიდა ქართლი</a>", 1),
(">Kvemo Kartli</a>", ">ქვემო ქართლი</a>", 1),
(">Samegrelo</a>", ">სამეგრელო</a>", 1),
(">Racha-Lechkhumi</a>", ">რაჭა-ლეჩხუმი</a>", 1),
(">Guria</a>", ">გურია</a>", 1),
# Footer
(">Privacy Policy</a>", ">კონფიდენციალურობის პოლიტიკა</a>", 1),
("Guide Timur · +995 511 272 623", "გიდი თიმური · +995 511 272 623", 1),
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
