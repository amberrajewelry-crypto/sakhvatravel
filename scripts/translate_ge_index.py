# -*- coding: utf-8 -*-
"""Перевод ge/index.html (главная) EN->KA. Каркас уже сделан gen_ge.py.
Переводится видимый контент + meta + natural-language в JSON-LD. URL/JS/схема-структура
не трогаются. Последовательная обработка: счётчик проверяется на текущем состоянии."""
import sys
FILE = "ge/index.html"
R = []
def add(old, new, n=1):
    R.append((old, new, n))

GE_TITLE = "ტურები და ექსკურსიები საქართველოში — თბილისი, ბათუმი, ქუთაისი"

# --- HEAD / META ---
add('<title>Georgia Tours & Excursions — Tbilisi, Batumi, Kutaisi</title>',
    f'<title>{GE_TITLE}</title>')
add('Georgia Tours &amp; Excursions — Tbilisi, Batumi, Kutaisi', GE_TITLE, 2)  # og:title + twitter:title
add('Georgia tours & excursions with Timur. Kazbegi ₾175, Kakheti ₾170, Old Tbilisi ₾98. Up to 7 people, 500+ tours, rating 4.9. Free cancellation 24h.',
    'ტურები და ექსკურსიები საქართველოში თიმურთან. ყაზბეგი ₾175, კახეთი ₾170, ძველი თბილისი ₾98. 7 ადამიანამდე, 500+ ტური, რეიტინგი 4.9. უფასო გაუქმება 24სთ.')
add('Private tours in Tbilisi and Georgia. Kazbegi, Kakheti, Kutaisi. Local guide Timur, up to 7 people. From ₾98/person.',
    'კერძო ტურები თბილისსა და საქართველოში. ყაზბეგი, კახეთი, ქუთაისი. ადგილობრივი გიდი თიმური, 7 ადამიანამდე. ₾98-დან ერთ ადამიანზე.')
add('Private tour Timur — tours in Tbilisi and Georgia | Sakhva Travel',
    'კერძო გიდი თიმური — ტურები თბილისსა და საქართველოში | Sakhva Travel')
add('Private tours in Tbilisi and Georgia with local guide. Kazbegi, Kakheti, hidden spots. From ₾98/person.',
    'კერძო ტურები თბილისსა და საქართველოში ადგილობრივ გიდთან. ყაზბეგი, კახეთი, ფარული ადგილები. ₾98-დან ერთ ადამიანზე.')

# --- NAV / DRAWER ---
add('>Tours in Georgia</a>', '>ტურები საქართველოში</a>', 2)
add('>Excursions</a>', '>ექსკურსიები</a>', 2)
add('>Prices</a>', '>ფასები</a>', 2)
add('>About us</a>', '>ჩვენ შესახებ</a>', 2)
add('>Reviews</a>', '>შეფასებები</a>', 3)
add('>Media</a>', '>მედია</a>', 2)
add('>Blog</a>', '>ბლოგი</a>', 3)
add('>Contacts</a>', '>კონტაქტი</a>', 3)
add('>Book online</a>', '>დაჯავშნე ონლაინ</a>', 2)

# --- HERO ---
add('<h1 class="hero-h1 hero-typewriter">Tours & Excursions in Georgia</h1>',
    '<h1 class="hero-h1 hero-typewriter">ტურები და ექსკურსიები საქართველოში</h1>')
add('>Tbilisi, Batumi, Kutaisi, Borjomi</p>', '>თბილისი, ბათუმი, ქუთაისი, ბორჯომი</p>')
add('>Guided excursions · Tbilisi and all of Georgia</p>',
    '>ექსკურსიები გიდთან · თბილისი და მთელი საქართველო</p>')
add('display:inline-block">Contact me</a>', 'display:inline-block">დამიკავშირდი</a>')
add('border-radius:9999px">Choose a tour</button>', 'border-radius:9999px">აირჩიე ტური</button>')
add('<p class="hero-micro">Free cancellation 24h · Reply in 15 min</p>',
    '<p class="hero-micro">უფასო გაუქმება 24სთ · პასუხი 15 წუთში</p>')

# --- CATALOG FILTERS ---
add('<a href="/" style="color:#1A3D2E;text-decoration:underline;text-underline-offset:2px">Home</a> <span>›</span> Tours',
    '<a href="/" style="color:#1A3D2E;text-decoration:underline;text-underline-offset:2px">მთავარი</a> <span>›</span> ტურები')
add('>Tours in Tbilisi and Georgia</h2>', '>ტურები თბილისსა და საქართველოში</h2>')
add('>Private tours with English-speaking guide. From ₾98/person</p>',
    '>კერძო ტურები ინგლისურენოვან გიდთან. ₾98-დან ერთ ადამიანზე</p>')
add('<span>Any date, 1 person</span>', '<span>ნებისმიერი თარიღი, 1 ადამიანი</span>')
add('<span id="hp-format-label">Tour format</span>', '<span id="hp-format-label">ტურის ფორმატი</span>')
add('<strong>All formats</strong>', '<strong>ყველა ფორმატი</strong>')
add('<strong>Private</strong><br><span style="font-size:12px;color:#6B7280;font-weight:400">Personal meeting with guide just for you</span>',
    '<strong>კერძო</strong><br><span style="font-size:12px;color:#6B7280;font-weight:400">პირადი შეხვედრა გიდთან მხოლოდ თქვენთვის</span>')
add('<strong>Small group</strong><br><span style="font-size:12px;color:#6B7280;font-weight:400">Up to 8 people with other guests</span>',
    '<strong>მცირე ჯგუფი</strong><br><span style="font-size:12px;color:#6B7280;font-weight:400">8 ადამიანამდე სხვა სტუმრებთან ერთად</span>')
add('<span id="hp-cur-label">₾ Currency</span>', '<span id="hp-cur-label">₾ ვალუტა</span>')
add('data-hp-cur="GEL">₾ GEL — Lari</div>', 'data-hp-cur="GEL">₾ GEL — ლარი</div>')
add('data-hp-cur="USD">$ USD — Dollar</div>', 'data-hp-cur="USD">$ USD — დოლარი</div>')
add('data-hp-cur="EUR">€ EUR — Euro</div>', 'data-hp-cur="EUR">€ EUR — ევრო</div>')
add('data-hp-cur="RUB">₽ RUB — Ruble</div>', 'data-hp-cur="RUB">₽ RUB — რუბლი</div>')
add('<span id="hp-price-label">Price</span>', '<span id="hp-price-label">ფასი</span>')
add('data-hp-price="all" style="padding:10px 18px"><strong>Any price</strong>',
    'data-hp-price="all" style="padding:10px 18px"><strong>ნებისმიერი ფასი</strong>')
add('data-hp-price="low" style="padding:10px 18px">up to ₾150</div>',
    'data-hp-price="low" style="padding:10px 18px">₾150-მდე</div>')
add('cf-btn cf-btn-adv" style="text-decoration:none">\n    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 4h12M2 8h12M2 12h12"/><circle cx="5" cy="4" r="1.5" fill="currentColor"/><circle cx="11" cy="8" r="1.5" fill="currentColor"/><circle cx="7" cy="12" r="1.5" fill="currentColor"/></svg>\n    Filters',
    'cf-btn cf-btn-adv" style="text-decoration:none">\n    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 4h12M2 8h12M2 12h12"/><circle cx="5" cy="4" r="1.5" fill="currentColor"/><circle cx="11" cy="8" r="1.5" fill="currentColor"/><circle cx="7" cy="12" r="1.5" fill="currentColor"/></svg>\n    ფილტრები')
add('<span id="hp-expand-label">All 67 tours</span>', '<span id="hp-expand-label">ყველა 67 ტური</span>')

# --- catalog inline-JS UI labels (page-local) ---
add("badgeTxt=t.format==='group'?'Small group':'Private';", "badgeTxt=t.format==='group'?'მცირე ჯგუფი':'კერძო';")
add("var syms={GEL:'\\u20BE Currency',USD:'$ USD',EUR:'\\u20AC EUR',RUB:'\\u20BD RUB'};",
    "var syms={GEL:'\\u20BE ვალუტა',USD:'$ USD',EUR:'\\u20AC EUR',RUB:'\\u20BD RUB'};")
add("document.getElementById('hp-cur-label').textContent=syms[curCur]||'\\u20BE Currency';",
    "document.getElementById('hp-cur-label').textContent=syms[curCur]||'\\u20BE ვალუტა';")
add("var labels={all:'Price',low:'up to \\u20BE150',mid:'\\u20BE150\\u2013300',high:'\\u20BE300+'};",
    "var labels={all:'ფასი',low:'\\u20BE150-მდე',mid:'\\u20BE150\\u2013300',high:'\\u20BE300+'};")
add("document.getElementById('hp-price-label').textContent=labels[curPrice]||'Price';",
    "document.getElementById('hp-price-label').textContent=labels[curPrice]||'ფასი';")
add("document.getElementById('hp-format-label').textContent=curFormat==='all'?'Tour format':el.querySelector('strong').textContent;",
    "document.getElementById('hp-format-label').textContent=curFormat==='all'?'ტურის ფორმატი':el.querySelector('strong').textContent;")
add("if(expandLabel)expandLabel.textContent='All '+total+' tours'", "if(expandLabel)expandLabel.textContent='სულ '+total+' ტური'")

# --- NOSCRIPT catalog list ---
add('>Kazbegi Day Trip — from 175 GEL</a>', '>ყაზბეგი ერთ დღეში — 175 GEL-დან</a>')
add('>Kakheti Wine Tour — from 170 GEL</a>', '>კახეთის ღვინის ტური — 170 GEL-დან</a>')
add('>Night Tbilisi — from 94 GEL</a>', '>ღამის თბილისი — 94 GEL-დან</a>')
add('>Mtskheta — from 77 GEL</a>', '>მცხეთა — 77 GEL-დან</a>')
add('>Food Tour — from 165 GEL</a>', '>გასტრონომიული ტური — 165 GEL-დან</a>')
add('>Wine Tasting Kakheti — from 225 GEL</a>', '>ღვინის დეგუსტაცია კახეთში — 225 GEL-დან</a>')
add('>Sighnaghi — from 175 GEL</a>', '>სიღნაღი — 175 GEL-დან</a>')
add('>Batumi Day Trip — from 250 GEL</a>', '>ბათუმი ერთ დღეში — 250 GEL-დან</a>')
add('>Old Tbilisi Walking — from 135 GEL</a>', '>ძველი თბილისი ფეხით — 135 GEL-დან</a>')
add('>Art Tour — from 145 GEL</a>', '>არტ-ტური — 145 GEL-დან</a>')
add('>Family Tour — from 165 GEL</a>', '>საოჯახო ტური — 165 GEL-დან</a>')
add('>Svaneti — from 345 GEL</a>', '>სვანეთი — 345 GEL-დან</a>')
add('>Georgia 3 Days — from 450 GEL</a>', '>საქართველო 3 დღე — 450 GEL-დან</a>')
add('>Georgia 7 Days — from 595 GEL</a>', '>საქართველო 7 დღე — 595 GEL-დან</a>')
add('>All 67 Tours →</a>', '>ყველა 67 ტური →</a>')
add('<h2 style="font-size:24px;margin-bottom:16px">All Tours in Georgia</h2>',
    '<h2 style="font-size:24px;margin-bottom:16px">ყველა ტური საქართველოში</h2>')

# --- GUIDE SECTION ---
add('<div class="sec-label" data-anim="down">About us</div>', '<div class="sec-label" data-anim="down">ჩვენ შესახებ</div>')
add('>Why do tourists choose Sakhva Travel?</h2>', '>რატომ ირჩევენ ტურისტები Sakhva Travel-ს?</h2>')
add('<div class="guide-badge-lbl">Tourists</div>', '<div class="guide-badge-lbl">ტურისტი</div>')
add('<p class="guide-bio">Sakhva Travel is a private tour service in Tbilisi, founded by Timur in 2023. Timur was born in Tbilisi, grew up in the Caucasus, and returned home 10 years ago — not as a tourist, but for good. Sakhva Travel grew out of this personal knowledge of the city.</p>',
    '<p class="guide-bio">Sakhva Travel — კერძო ტურების სერვისი თბილისში, დაარსებული თიმურის მიერ 2023 წელს. თიმური დაიბადა თბილისში, გაიზარდა კავკასიაში და 10 წლის წინ სამშობლოში დაბრუნდა — არა ტურისტად, არამედ სამუდამოდ. Sakhva Travel სწორედ ქალაქის ამ პირადი ცოდნიდან გაიზარდა.</p>')
add('We show Georgia the way a local sees it: not from a checklist of sights, but in layers. First the facades, then the courtyards, then the people. We know when to head to Kazbegi so the mountains are cloud-free. We know which courtyard in the Old Town makes the best homemade wine. We know the unmarked cafe where locals eat khinkali at 7am. You can\'t Google this — it comes with years.',
    'ჩვენ საქართველოს ისე გაჩვენებთ, როგორც მას ადგილობრივი ხედავს: არა ღირსშესანიშნაობების სიიდან, არამედ ფენებად. ჯერ ფასადები, მერე ეზოები, მერე ხალხი. ვიცით, როდის წავიდეთ ყაზბეგში, რომ მთები უღრუბლო იყოს. ვიცით, ძველ ქალაქში რომელ ეზოში მზადდება საუკეთესო საშინაო ღვინო. ვიცით უწარწერო კაფე, სადაც ადგილობრივები დილის 7 საათზე ხინკალს ჭამენ. ამას Google-ში ვერ იპოვით — ეს წლებთან ერთად მოდის.')
add('Since 2023, over 500 tourists have traveled with Sakhva Travel, and no route has ever been repeated — because every group is different.',
    '2023 წლიდან Sakhva Travel-თან 500-ზე მეტმა ტურისტმა იმოგზაურა და არც ერთი მარშრუტი არ განმეორებულა — რადგან ყველა ჯგუფი განსხვავებულია.')
add('Licensed guide of Georgia — licence No. 8247109128.',
    'საქართველოს ლიცენზირებული გიდი — ლიცენზია №8247109128.')
add('<div class="gf-title">Operating since 2023</div><div class="gf-sub">500+ tourists, rating 4.9</div>',
    '<div class="gf-title">მუშაობს 2023 წლიდან</div><div class="gf-sub">500+ ტურისტი, რეიტინგი 4.9</div>')
add('<div class="gf-title">English & Russian tours</div><div class="gf-sub">Bilingual guide — we speak your language</div>',
    '<div class="gf-title">ტურები ინგლისურად და რუსულად</div><div class="gf-sub">ორენოვანი გიდი — ვსაუბრობთ თქვენს ენაზე</div>')
add('<div class="gf-title">Based in Tbilisi</div><div class="gf-sub">Up-to-date spots, not an old guidebook</div>',
    '<div class="gf-title">ბაზირებული თბილისში</div><div class="gf-sub">აქტუალური ადგილები, და არა ძველი გზამკვლევი</div>')
add('<div class="gf-title">4.9 / 5 · 90+ reviews</div><div class="gf-sub">Google · Personal recommendations</div>',
    '<div class="gf-title">4.9 / 5 · 90+ შეფასება</div><div class="gf-sub">Google · პირადი რეკომენდაციები</div>')
add('<span>Message Timur</span>', '<span>მოგვწერე თიმურს</span>')

# --- INSTAGRAM ---
add('>Follow us on Instagram</span>', '>გამოგვყევით Instagram-ზე</span>')
add('>@sakhvatravel · 823 followers</a>', '>@sakhvatravel · 823 გამომწერი</a>')
add('alt="Georgian cuisine with Timur"', 'alt="ქართული სამზარეულო თიმურთან"')
add('alt="National Wine Day, Tbilisi"', 'alt="ღვინის ეროვნული დღე, თბილისი"')
add('alt="Guide Timur — Sakhva Travel"', 'alt="გიდი თიმური — Sakhva Travel"')
add('alt="Sunset over Tbilisi — Sameba"', 'alt="მზის ჩასვლა თბილისზე — სამება"')
add('alt="Wine tour in Kakheti"', 'alt="ღვინის ტური კახეთში"')
add('alt="Georgian bread — shoti from tone"', 'alt="ქართული პური — შოთი თონედან"')
add('alt="Timur on a mountain tour"', 'alt="თიმური მთის ტურზე"')
add('alt="Expat tour — Tbilisi"', 'alt="ექსპატ-ტური — თბილისი"')
add('>\n    Follow on Instagram\n  </a>', '>\n    გამოყევი Instagram-ზე\n  </a>')

# --- WHY US ---
add('<div class="sec-label" style="color:#1A3D2E">Why us</div>', '<div class="sec-label" style="color:#1A3D2E">რატომ ჩვენ</div>')
add('<h2 class="sec-title" style="color:#111827">Why choose a private tour over a tour agency?</h2>',
    '<h2 class="sec-title" style="color:#111827">რატომ ჯობია კერძო ტური ტურ-სააგენტოს?</h2>')
add('<p class="sec-sub" style="color:#4B5563">Four things that make a private tour worth it.</p>',
    '<p class="sec-sub" style="color:#4B5563">ოთხი მიზეზი, რის გამოც კერძო ტური ღირს.</p>')
add('<div class="wa-title">We create emotions</div>', '<div class="wa-title">ჩვენ ვქმნით ემოციებს</div>')
add('<p class="wa-text">We pay attention to details: a bottle of water in the heat, a blanket at the Kazbegi viewpoint, great coffee on the way. It\'s not "service" — it\'s simply care. These small things make a day you\'ll remember.</p>',
    '<p class="wa-text">ყურადღებას ვაქცევთ დეტალებს: წყლის ბოთლი სიცხეში, საბანი ყაზბეგის ხედვის წერტილზე, გემრიელი ყავა გზაში. ეს არ არის „სერვისი“ — ეს უბრალოდ ზრუნვაა. სწორედ ეს წვრილმანები ქმნის დღეს, რომელიც დაგამახსოვრდებათ.</p>')
add('<div class="wa-title">Fewer people — more of your tour</div>', '<div class="wa-title">ნაკლები ხალხი — მეტი შენი ტური</div>')
add('<p class="wa-text">In a group of 25, the pace is set by the slowest and the mood by the loudest. With us it\'s four, six — maximum seven. Nobody is 40 minutes late after lunch, nobody ruins your rest on the road, nobody photobombs your shots. You travel with your people, not strangers.</p>',
    '<p class="wa-text">25-კაციან ჯგუფში ტემპს ყველაზე ნელი აწესებს, განწყობას კი — ყველაზე ხმაურიანი. ჩვენთან ეს ოთხი, ექვსი — მაქსიმუმ შვიდი ადამიანია. არავინ აგვიანებს 40 წუთით სადილის შემდეგ, არავინ გიფუჭებთ დასვენებას გზაში, არავინ გერევათ კადრში. თქვენ თქვენს ხალხთან ერთად მოგზაურობთ, და არა უცნობებთან.</p>')
add('<div class="wa-title">One price — all included.</div>', '<div class="wa-title">ერთი ფასი — ყველაფერი შედის.</div>')
add('<p class="wa-text">Transfer, guide, parking, tastings — calculated before you leave. The price won\'t change by the end.</p>',
    '<p class="wa-text">ტრანსფერი, გიდი, პარკინგი, დეგუსტაციები — ყველაფერი დათვლილია გამგზავრებამდე. ფასი ბოლომდე არ შეიცვლება.</p>')
add('<div class="wa-title">The route is yours, not ours!</div>', '<div class="wa-title">მარშრუტი შენია, და არა ჩვენი!</div>')
add('<p class="wa-text">Love a spot — we stay as long as you want. Want to detour to a lake not in the program — we go. Tired — head back, not tired — we visit a winemaker. We don\'t follow a schedule. We help you spend the day exactly the way you want.</p>',
    '<p class="wa-text">მოგეწონათ ადგილი — ვრჩებით იმდენ ხანს, რამდენიც გსურთ. გინდათ გადაუხვიოთ ტბასთან, რომელიც პროგრამაში არ არის — მივდივართ. დაიღალეთ — ვბრუნდებით, არ დაიღალეთ — ვსტუმრობთ მეღვინეს. ჩვენ გრაფიკს არ მივყვებით. ჩვენ გეხმარებით დღე ისე გაატაროთ, როგორც ზუსტად გსურთ.</p>')

# --- COMPARISON TABLE ---
add('<span class="col-name">Bus Tour</span>', '<span class="col-name">ავტობუსური ტური</span>')
add('<span class="col-name">Self-guided</span>', '<span class="col-name">დამოუკიდებლად</span>')
add('<span class="col-name">With Timur</span>', '<span class="col-name">თიმურთან ერთად</span>')
add('<td class="col-bus">Waiting at the fountain for 40 strangers to gather</td>',
    '<td class="col-bus">ფონტანთან ლოდინი, სანამ 40 უცნობი შეიკრიბება</td>')
add('<td class="col-self">Taxi ₾180, driver doesn\'t speak English</td>',
    '<td class="col-self">ტაქსი ₾180, მძღოლმა ინგლისური არ იცის</td>')
add('<td class="col-timur">Timur at your hotel. Coffee in the car and the day\'s route</td>',
    '<td class="col-timur">თიმური თქვენს სასტუმროსთან. ყავა მანქანაში და დღის მარშრუტი</td>')
add('<td class="col-bus">Guide speaks Georgian, then translates</td>',
    '<td class="col-bus">გიდი ქართულად ლაპარაკობს, მერე თარგმნის</td>')
add('<td class="col-self">Driving on the highway. Nobody told you there\'s a scenic road</td>',
    '<td class="col-self">მიდიხართ ავტობანზე. არავინ გითხრათ, რომ არის ულამაზესი გზა</td>')
add('<td class="col-timur">"Let me show you a spot tourists never reach"</td>',
    '<td class="col-timur">„მოდი, გაჩვენებ ადგილს, სადაც ტურისტები არასდროს აღწევენ“</td>')
add('<td class="col-bus">"We leave in 10 minutes." No time to eat</td>',
    '<td class="col-bus">„10 წუთში მივდივართ.“ ჭამის დრო არ არის</td>')
add('<td class="col-self">Roadside cafe — the only one you could find</td>',
    '<td class="col-self">გზისპირა კაფე — ერთადერთი, რომელიც იპოვეთ</td>')
add('<td class="col-timur">Lunch at Manana\'s. You make khinkali yourself, wine from qvevri</td>',
    '<td class="col-timur">სადილი მანანასთან. ხინკალს თავად აკეთებთ, ღვინო ქვევრიდან</td>')
add('<td class="col-bus">Queue at Gergeti: 60 people ahead of you</td>',
    '<td class="col-bus">რიგი გერგეტთან: თქვენს წინ 60 ადამიანი</td>')
add('<td class="col-self">Gergeti Trinity closed on Mondays</td>',
    '<td class="col-self">გერგეტის სამება ორშაბათობით დაკეტილია</td>')
add('<td class="col-timur">Timur knows everyone. You go in while others wait outside</td>',
    '<td class="col-timur">თიმური ყველას იცნობს. თქვენ შედიხართ, სანამ სხვები გარეთ ელოდებიან</td>')
add('<td class="col-bus">Bus heads home. Mt Kazbek in clouds — not your day</td>',
    '<td class="col-bus">ავტობუსი სახლში მიდის. მყინვარწვერი ღრუბლებში — არა თქვენი დღე</td>')
add('<td class="col-self">Wanted to see the lake — didn\'t know where it was</td>',
    '<td class="col-self">გინდოდათ ტბის ნახვა — არ იცოდით, სად იყო</td>')
add('<td class="col-timur">We wait for the clouds to clear. We\'ll go higher</td>',
    '<td class="col-timur">ველოდებით, სანამ ღრუბლები გაიფანტება. უფრო მაღლა ავალთ</td>')
add('<td class="col-bus">Home. Exhausted by the crowd</td>',
    '<td class="col-bus">სახლში. ხალხმრავლობით დაღლილი</td>')
add('<td class="col-self">Home. Lost half the day</td>',
    '<td class="col-self">სახლში. დაკარგეთ ნახევარი დღე</td>')
add('<td class="col-timur">Home. 200 photos, secret location contacts, memories for life</td>',
    '<td class="col-timur">სახლში. 200 ფოტო, საიდუმლო ადგილების კონტაქტები, მოგონებები მთელი ცხოვრებისთვის</td>')

# --- REGIONS ---
add('<h2 class="sec-title reveal" style="color:#111;font-size:clamp(26px,3.5vw,48px);font-weight:300;line-height:1.15;margin-bottom:40px">Where we go — 10 regions</h2>',
    '<h2 class="sec-title reveal" style="color:#111;font-size:clamp(26px,3.5vw,48px);font-weight:300;line-height:1.15;margin-bottom:40px">სად დავდივართ — 10 რეგიონი</h2>')
add('alt="Region of Georgia"', 'alt="საქართველოს რეგიონი"')
add('<h3 id="rg-name" style="font-size:clamp(22px,2.5vw,32px);font-weight:600;margin:0 0 8px;color:#111">Mtskheta-Mtianeti</h3>',
    '<h3 id="rg-name" style="font-size:clamp(22px,2.5vw,32px);font-weight:600;margin:0 0 8px;color:#111">მცხეთა-მთიანეთი</h3>')
add('<p id="rg-label" style="font-size:13px;color:#999;margin:0 0 10px;text-transform:uppercase;letter-spacing:.5px">Main destinations</p>',
    '<p id="rg-label" style="font-size:13px;color:#999;margin:0 0 10px;text-transform:uppercase;letter-spacing:.5px">მთავარი მიმართულებები</p>')
add('<p id="rg-cities" style="font-size:15px;color:#444;margin:0 0 12px">Mtskheta · Kazbegi · Gudauri</p>',
    '<p id="rg-cities" style="font-size:15px;color:#444;margin:0 0 12px">მცხეთა · ყაზბეგი · გუდაური</p>')
add('text-decoration:none;transition:color .2s">More about region <svg', 'text-decoration:none;transition:color .2s">მეტი რეგიონის შესახებ <svg')
add('<span class="rg-dot" style="width:14px;height:14px;border-radius:50%;border:2px solid #1A3D2E;background:#1A3D2E;display:inline-block"></span><strong>Main cities</strong>',
    '<span class="rg-dot" style="width:14px;height:14px;border-radius:50%;border:2px solid #1A3D2E;background:#1A3D2E;display:inline-block"></span><strong>მთავარი ქალაქები</strong>')
add('<span class="rg-dot" style="width:14px;height:14px;border-radius:50%;border:2px solid #ccc;background:transparent;display:inline-block"></span><strong>Travel time</strong>',
    '<span class="rg-dot" style="width:14px;height:14px;border-radius:50%;border:2px solid #ccc;background:transparent;display:inline-block"></span><strong>მგზავრობის დრო</strong>')
# SVG region name labels
add('<text x="134" y="90">Abkhazia</text>', '<text x="134" y="90">აფხაზეთი</text>')
add('<text x="254" y="312">Adjara</text>', '<text x="254" y="312">აჭარა</text>')
add('<text x="270" y="260">Guria</text>', '<text x="270" y="260">გურია</text>')
add('<text x="369" y="230">Imereti</text>', '<text x="369" y="230">იმერეთი</text>')
add('<text x="721" y="288">Kakheti</text>', '<text x="721" y="288">კახეთი</text>')
add('<text x="555" y="338">Kvemo Kartli</text>', '<text x="555" y="338">ქვემო ქართლი</text>')
add('<text x="584" y="220">Mtskheta-</text><text x="584" y="233">Mtianeti</text>',
    '<text x="584" y="220">მცხეთა-</text><text x="584" y="233">მთიანეთი</text>')
add('<text x="387" y="152">Shida Kartli</text>', '<text x="387" y="152">შიდა ქართლი</text>')
add('<text x="398" y="338">Samtskhe-</text><text x="398" y="351">Javakheti</text>',
    '<text x="398" y="338">სამცხე-</text><text x="398" y="351">ჯავახეთი</text>')
add('<text x="493" y="255">Samegrelo</text>', '<text x="493" y="255">სამეგრელო</text>')
add('<text x="292" y="148">Racha-</text><text x="292" y="161">Lechkhumi</text>',
    '<text x="292" y="148">რაჭა-</text><text x="292" y="161">ლეჩხუმი</text>')
add('<text x="490" y="190" font-size="9">Samachablo</text>', '<text x="490" y="190" font-size="9">სამაჩაბლო</text>')
add('<text x="597" y="306" font-size="10">Tbilisi</text>', '<text x="597" y="306" font-size="10">თბილისი</text>')
# time badges
add('<text y="3" fill="#EF3A50">1h 40m</text>', '<text y="3" fill="#EF3A50">1სთ 40წთ</text>')
add('<text y="3" fill="#EF3A50">1h</text>', '<text y="3" fill="#EF3A50">1სთ</text>')
add('<text y="3" fill="#EF3A50">2h 30m</text>', '<text y="3" fill="#EF3A50">2სთ 30წთ</text>')
add('<text y="3" fill="#EF3A50">5 ч</text>', '<text y="3" fill="#EF3A50">5სთ</text>')
add('<text y="3" fill="#EF3A50">4h 52m</text>', '<text y="3" fill="#EF3A50">4სთ 52წთ</text>')
add('<text y="3" fill="#EF3A50">3h 30m</text>', '<text y="3" fill="#EF3A50">3სთ 30წთ</text>')
add('<text y="3" fill="#EF3A50">1h 20m</text>', '<text y="3" fill="#EF3A50">1სთ 20წთ</text>')
add('<text y="3" fill="#EF3A50">40 м</text>', '<text y="3" fill="#EF3A50">40წთ</text>')
add('<text y="3" fill="#EF3A50">4h 30m</text>', '<text y="3" fill="#EF3A50">4სთ 30წთ</text>')
add('<text y="3" fill="#EF3A50">4 ч</text>', '<text y="3" fill="#EF3A50">4სთ</text>')
# JS region data (names + cities)
add('abkhazia:{name:"Abkhazia",cities:["Sukhumi","Gali","Ochamchire"]', 'abkhazia:{name:"აფხაზეთი",cities:["სოხუმი","გალი","ოჩამჩირე"]')
add('tbilisi:{name:"Tbilisi",cities:["Tbilisi","Kojori","Kiketi"]', 'tbilisi:{name:"თბილისი",cities:["თბილისი","კოჯორი","კიკეთი"]')
add('kakheti:{name:"Kakheti",cities:["Telavi","Akhmeta","Dedoplistsqaro"]', 'kakheti:{name:"კახეთი",cities:["თელავი","ახმეტა","დედოფლისწყარო"]')
add('mtskheta:{name:"Mtskheta-Mtianeti",cities:["Stepantsminda","Mtskheta","Dusheti"]', 'mtskheta:{name:"მცხეთა-მთიანეთი",cities:["სტეფანწმინდა","მცხეთა","დუშეთი"]')
add('kvemo:{name:"Kvemo Kartli",cities:["Rustavi","Bolnisi","Dmanisi"]', 'kvemo:{name:"ქვემო ქართლი",cities:["რუსთავი","ბოლნისი","დმანისი"]')
add('shida:{name:"Shida Kartli",cities:["Gori","Uplistsikhe","Khashuri"]', 'shida:{name:"შიდა ქართლი",cities:["გორი","უფლისციხე","ხაშური"]')
add('samtskhe:{name:"Samtskhe-Javakheti",cities:["Akhaltsikhe","Borjomi","Vardzia"]', 'samtskhe:{name:"სამცხე-ჯავახეთი",cities:["ახალციხე","ბორჯომი","ვარძია"]')
add('imereti:{name:"Imereti",cities:["Kutaisi","Tskaltubo","Bagdati"]', 'imereti:{name:"იმერეთი",cities:["ქუთაისი","წყალტუბო","ბაღდათი"]')
add('racha:{name:"Racha-Lechkhumi and Lower Svaneti",cities:["Ambrolauri","Oni","Shovi"]', 'racha:{name:"რაჭა-ლეჩხუმი და ქვემო სვანეთი",cities:["ამბროლაური","ონი","შოვი"]')
add('samegrelo:{name:"Samegrelo-Upper Svaneti",cities:["Mestia","Poti","Abasha"]', 'samegrelo:{name:"სამეგრელო-ზემო სვანეთი",cities:["მესტია","ფოთი","აბაშა"]')
add('guria:{name:"Guria",cities:["Bakhmaro","Lanchkhuti","Ozurgeti"]', 'guria:{name:"გურია",cities:["ბახმარო","ლანჩხუთი","ოზურგეთი"]')
add('adjara:{name:"Adjara",cities:["Batumi","Kobuleti","Keda"]', 'adjara:{name:"აჭარა",cities:["ბათუმი","ქობულეთი","ქედა"]')
add('samachablo:{name:"Samachablo",cities:["Tskhinvali","Java","Akhalgori"]', 'samachablo:{name:"სამაჩაბლო",cities:["ცხინვალი","ჯავა","ახალგორი"]')

# --- HOW TO BOOK ---
add('<div class="sec-label" style="color:#1A3D2E">Simple & fast</div>', '<div class="sec-label" style="color:#1A3D2E">მარტივი და სწრაფი</div>')
add('<h2 class="sec-title" style="color:#111827">How do you book a private tour in Tbilisi?</h2>',
    '<h2 class="sec-title" style="color:#111827">როგორ დაჯავშნოთ კერძო ტური თბილისში?</h2>')
add('<p class="sec-sub" style="color:#4B5563">Three steps — from message to unforgettable day</p>',
    '<p class="sec-sub" style="color:#4B5563">სამი ნაბიჯი — შეტყობინებიდან დაუვიწყარ დღემდე</p>')
add('<h3 class="hw-title">Fill the form online</h3>', '<h3 class="hw-title">შეავსეთ ფორმა ონლაინ</h3>')
add('<p class="hw-text">Pick your tour and date from the calendar — takes 2 minutes. Or message us on WhatsApp / Telegram.</p>',
    '<p class="hw-text">აირჩიეთ ტური და თარიღი კალენდრიდან — 2 წუთი სჭირდება. ან მოგვწერეთ WhatsApp / Telegram-ზე.</p>')
add('<h3 class="hw-title">Confirmation</h3>', '<h3 class="hw-title">დადასტურება</h3>')
add('<p class="hw-text">Timur writes within 2 hours to confirm details and meeting time.</p>',
    '<p class="hw-text">თიმური 2 საათში მოგწერთ, რომ დაადასტუროს დეტალები და შეხვედრის დრო.</p>')
add('<h3 class="hw-title">Tour day</h3>', '<h3 class="hw-title">ტურის დღე</h3>')
add('<p class="hw-text">We meet and go. Pay on the day of the tour — cash or card. No surprises.</p>',
    '<p class="hw-text">ვხვდებით და მივდივართ. გადაიხდით ტურის დღეს — ნაღდით ან ბარათით. სიურპრიზების გარეშე.</p>')
add('<div class="group-discount-bar" style="font-size:14px;padding:12px 28px">Group of 4+ — 10% off</div>',
    '<div class="group-discount-bar" style="font-size:14px;padding:12px 28px">ჯგუფი 4+ — 10% ფასდაკლება</div>')
add('style="cursor:pointer;font-family:inherit;background:#1A3D2E">Not sure which tour? Take the quiz →</button>',
    'style="cursor:pointer;font-family:inherit;background:#1A3D2E">არ ხართ დარწმუნებული, რომელი ტური? გაიარეთ ქვიზი →</button>')

# --- REVIEWS ---
add('<div class="sec-label" style="color:#111827">Reviews</div>', '<div class="sec-label" style="color:#111827">შეფასებები</div>')
add('<h2 class="sec-title">What do tourists say about Sakhva Travel?</h2>',
    '<h2 class="sec-title">რას ამბობენ ტურისტები Sakhva Travel-ზე?</h2>')
add('<span>Read all reviews on Google →</span>', '<span>წაიკითხეთ ყველა შეფასება Google-ზე →</span>')
add('<p class="rc-text">Wonderful tour! Thank you so much!</p>', '<p class="rc-text">შესანიშნავი ტური! დიდი მადლობა!</p>')
add('<p class="rc-text">Excellent guide. Showed and told us everything about sunny Georgia. Speaks fluent English.</p>',
    '<p class="rc-text">შესანიშნავი გიდი. ყველაფერი გვაჩვენა და მოგვიყვა მზიან საქართველოზე. თავისუფლად ლაპარაკობს ინგლისურად.</p>')
add('<p class="rc-text">Highly recommend if you want the best travel recommendations and services in Georgia.</p>',
    '<p class="rc-text">ნამდვილად გირჩევთ, თუ გსურთ საუკეთესო რეკომენდაციები და მომსახურება საქართველოში მოგზაურობისთვის.</p>')
add('<div class="rc-meta">April 2026</div>', '<div class="rc-meta">აპრილი 2026</div>', 3)
add('>Reviews on Yandex</span>', '>შეფასებები Yandex-ზე</span>')
add('<p class="rc-text">This year we traveled to Georgia as a group. Thanks to Timur and the whole team. It was incredible!</p>',
    '<p class="rc-text">წელს საქართველოში ჯგუფურად ვიმოგზაურეთ. მადლობა თიმურსა და მთელ გუნდს. წარმოუდგენელი იყო!</p>')
add('<p class="rc-text">Everything went great, highly recommend!</p>', '<p class="rc-text">ყველაფერი შესანიშნავად ჩაიარა, ნამდვილად გირჩევთ!</p>')
add('<p class="rc-text">Great guide. Had an amazing time! Individual program, highly recommend!</p>',
    '<p class="rc-text">შესანიშნავი გიდი. საოცრად გავატარეთ დრო! ინდივიდუალური პროგრამა, ნამდვილად გირჩევთ!</p>')
add('<div class="rc-meta">May 2026</div>', '<div class="rc-meta">მაისი 2026</div>', 3)
add('style="display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#FC3F1D;text-decoration:none">Read all reviews on Yandex →</a>',
    'style="display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#FC3F1D;text-decoration:none">წაიკითხეთ ყველა შეფასება Yandex-ზე →</a>')
add('>TripAdvisor Reviews</span>', '>TripAdvisor შეფასებები</span>')
add('>Travellers\' Choice</span>', '>მოგზაურთა არჩევანი</span>')
add('<p class="rc-text">"Wonderful trip to Kakheti! The wine was amazing — everyone should visit Georgian vineyards at least once."</p>',
    '<p class="rc-text">„შესანიშნავი მოგზაურობა კახეთში! ღვინო საოცარი იყო — ყველამ ერთხელ მაინც უნდა ეწვიოს ქართულ ვენახებს.“</p>')
add('<div class="rc-meta">Kakheti</div>', '<div class="rc-meta">კახეთი</div>')
add('<p class="rc-text">"You have no idea how much I enjoyed it. Nice tiredness, nice people, delicious food. Thank you very much."</p>',
    '<p class="rc-text">„წარმოდგენა არ გაქვთ, როგორ მომეწონა. სასიამოვნო დაღლილობა, სასიამოვნო ხალხი, გემრიელი საჭმელი. დიდი მადლობა.“</p>')
add('<p class="rc-text">"Here you can see the real Georgia. Very cool tours — I\'ll definitely be back again!"</p>',
    '<p class="rc-text">„აქ ნამდვილ საქართველოს ნახავთ. ძალიან მაგარი ტურები — აუცილებლად დავბრუნდები!“</p>')
add('style="display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#00AA6C;text-decoration:none">Read all reviews on TripAdvisor →</a>',
    'style="display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#00AA6C;text-decoration:none">წაიკითხეთ ყველა შეფასება TripAdvisor-ზე →</a>')

# --- GALLERY ---
add('style="text-align:center;padding:24px 20px 20px;margin:0;font-size:clamp(20px,5.5vw,48px)">Photos from our tours</h2>',
    'style="text-align:center;padding:24px 20px 20px;margin:0;font-size:clamp(20px,5.5vw,48px)">ფოტოები ჩვენი ტურებიდან</h2>')
add('>See all photos & videos</a>', '>ნახეთ ყველა ფოტო და ვიდეო</a>')
add('alt="Tour group at monastery arch with mountain views"', 'alt="ტურ-ჯგუფი მონასტრის თაღთან მთის ხედებით"', 2)
add('alt="Wine tasting at a Kakheti winery"', 'alt="ღვინის დეგუსტაცია კახეთის მარანში"', 2)
add('alt="Old Tbilisi view from a carved balcony"', 'alt="ძველი თბილისის ხედი მოჩუქურთმებული აივნიდან"', 2)
add('alt="Tourist group at Kazbegi summit"', 'alt="ტურ-ჯგუფი ყაზბეგის მწვერვალზე"', 2)
add('alt="Tourist group at Gergeti church in Kazbegi"', 'alt="ტურ-ჯგუფი გერგეტის ეკლესიასთან ყაზბეგში"')
add('alt="Couple at Chronicles of Georgia monument in Tbilisi"', 'alt="წყვილი „საქართველოს ისტორიის“ მონუმენტთან თბილისში"')
add('alt="Family walk on tour"', 'alt="ოჯახური სეირნობა ტურზე"')
add('alt="Tourist at Batumi seaside sculpture"', 'alt="ტურისტი ბათუმის ზღვისპირა სკულპტურასთან"')
add('alt="Couple at Tsminda Sameba cathedral in Tbilisi"', 'alt="წყვილი წმინდა სამების ტაძართან თბილისში"')
add('alt="Guide Timur with tourists on tour"', 'alt="გიდი თიმური ტურისტებთან ერთად ტურზე"')
add('alt="Group resting in Kazbegi mountains"', 'alt="ჯგუფი ისვენებს ყაზბეგის მთებში"')
add('alt="Tourists at Tbilisi viewpoint"', 'alt="ტურისტები თბილისის ხედვის წერტილზე"')
add('alt="Guide Timur with tourists"', 'alt="გიდი თიმური ტურისტებთან ერთად"')
add('alt="On the road to Kazbegi"', 'alt="ყაზბეგისკენ მიმავალ გზაზე"')
add('alt="On the road to Georgian mountains"', 'alt="ქართული მთებისკენ მიმავალ გზაზე"')
add('alt="Ferrari Formula 1 at Tbilisi art space"', 'alt="Ferrari Formula 1 თბილისის არტ-სივრცეში"')
add('alt="Church in Kakheti among cypresses"', 'alt="ეკლესია კახეთში კვიპაროსებს შორის"')
add('alt="Flower market in old Tbilisi"', 'alt="ყვავილების ბაზარი ძველ თბილისში"')
add('alt="Cathedral in Kakheti among cypresses"', 'alt="ტაძარი კახეთში კვიპაროსებს შორის"')
add('alt="Interior of ancient Georgian temple with frescoes"', 'alt="უძველესი ქართული ტაძრის ინტერიერი ფრესკებით"')
add('alt="Khachapuri and wine on terrace with mountain view"', 'alt="ხაჭაპური და ღვინო ტერასაზე მთის ხედით"')
add('alt="Teliani Valley — wine tasting in Kakheti"', 'alt="თელიანი ველი — ღვინის დეგუსტაცია კახეთში"')
add('alt="Old Tbilisi — street with flags in rain"', 'alt="ძველი თბილისი — ქუჩა დროშებით წვიმაში"')
add('alt="Tourists at Zhinvali reservoir with Georgian flags"', 'alt="ტურისტები ჟინვალის წყალსაცავთან ქართული დროშებით"')
add('alt="Lunch with a tour group at a beer restaurant in Tbilisi"', 'alt="სადილი ტურ-ჯგუფთან ერთად ლუდის რესტორანში თბილისში"')

# --- BLOG SECTION ---
add('<div class="sec-label" data-anim="down">Useful articles</div>', '<div class="sec-label" data-anim="down">სასარგებლო სტატიები</div>')
add('<h2 class="sec-title" data-anim="up">Georgia Travel Guides</h2>', '<h2 class="sec-title" data-anim="up">საქართველოს გზამკვლევები</h2>')
add('>Everything you need to know before your trip — honest and to the point</p>',
    '>ყველაფერი, რაც უნდა იცოდეთ მოგზაურობამდე — გულახდილად და საქმიანად</p>')
add('<div class="bc-h-cat">Kazbegi</div>\n<h3 class="bc-h-title">Kazbegi from Tbilisi: complete guide</h3>',
    '<div class="bc-h-cat">ყაზბეგი</div>\n<h3 class="bc-h-title">ყაზბეგი თბილისიდან: სრული გზამკვლევი</h3>')
add('<div class="bc-h-cat">Kakheti</div>\n<h3 class="bc-h-title">Kakheti day trip from Tbilisi</h3>',
    '<div class="bc-h-cat">კახეთი</div>\n<h3 class="bc-h-title">კახეთი ერთ დღეში თბილისიდან</h3>')
add('<div class="bc-h-cat">Tbilisi</div>\n<h3 class="bc-h-title">15 hidden gems of Tbilisi</h3>',
    '<div class="bc-h-cat">თბილისი</div>\n<h3 class="bc-h-title">თბილისის 15 ფარული ადგილი</h3>')
add('<span class="bc-h-read">8 min →</span>', '<span class="bc-h-read">8 წთ →</span>')
add('<span class="bc-h-read">6 min →</span>', '<span class="bc-h-read">6 წთ →</span>', 2)
add('>Complete Georgia Travel Guide →</a>', '>საქართველოს სრული გზამკვლევი →</a>')
add('>All articles →</a>', '>ყველა სტატია →</a>')

# --- BLOG MARQUEE (each paired: visible + aria-hidden) ---
add('>When to visit Kazbegi</a>', '>როდის ეწვიოთ ყაზბეგს</a>', 2)
add('>Sulfur baths of Tbilisi</a>', '>თბილისის გოგირდის აბანოები</a>', 2)
add('>15 hidden gems of Tbilisi</a>', '>თბილისის 15 ფარული ადგილი</a>', 2)
add('>Georgia visa guide</a>', '>საქართველოს ვიზის გზამკვლევი</a>', 2)
add('>Digital Nomad Tbilisi</a>', '>ციფრული მომთაბარე თბილისში</a>', 2)
add('>Batumi from Tbilisi</a>', '>ბათუმი თბილისიდან</a>', 2)
add('>Tbilisi in 1 day</a>', '>თბილისი 1 დღეში</a>', 2)
add('>Tbilisi in 3 days</a>', '>თბილისი 3 დღეში</a>', 2)
add('>Georgia in 7 days</a>', '>საქართველო 7 დღეში</a>', 2)
add('>Georgia on a budget</a>', '>საქართველო ბიუჯეტში</a>', 2)
add('>Mtskheta from Tbilisi</a>', '>მცხეთა თბილისიდან</a>', 2)
add('>Kazbegi in winter</a>', '>ყაზბეგი ზამთარში</a>', 2)
add('>David Gareja</a>', '>დავით გარეჯა</a>', 2)
add('>Vardzia</a>', '>ვარძია</a>', 2)
add('>Borjomi</a>', '>ბორჯომი</a>', 2)
add('>Georgia with kids</a>', '>საქართველო ბავშვებთან ერთად</a>', 2)
add('>Georgian wine guide</a>', '>ქართული ღვინის გზამკვლევი</a>', 2)
add('>Georgia in winter</a>', '>საქართველო ზამთარში</a>', 2)
add('>Kakheti in autumn</a>', '>კახეთი შემოდგომაზე</a>', 2)
add('>Free things in Tbilisi</a>', '>უფასო რამეები თბილისში</a>', 2)
add('>What to bring from Georgia</a>', '>რა წამოიღოთ საქართველოდან</a>', 2)
add('>Night Tbilisi</a>', '>ღამის თბილისი</a>', 2)
add('>What to see in Tbilisi</a>', '>რა ვნახოთ თბილისში</a>')
add('>Tours in Tbilisi</a>', '>ტურები თბილისში</a>')
add('>Cost of vacation in Georgia</a>', '>საქართველოში დასვენების ღირებულება</a>')

# --- FAQ (visible accordion) ---
add('<h2 class="sec-title" data-anim="up">Frequently Asked Questions</h2>',
    '<h2 class="sec-title" data-anim="up">ხშირად დასმული კითხვები</h2>')
add('>Can\'t find the answer? Message WhatsApp — reply in 15 min</p>',
    '>პასუხს ვერ პოულობთ? მოგვწერეთ WhatsApp — პასუხი 15 წუთში</p>')
def faqi(q_en, q_ka, a_en, a_ka):
    add(f'<span>{q_en}</span><span class="fq-ic">+</span>', f'<span>{q_ka}</span><span class="fq-ic">+</span>')
    add(f'<div class="fa-inner">{a_en}</div>', f'<div class="fa-inner">{a_ka}</div>')
faqi('How much does a Kazbegi tour cost?', 'რამდენი ჯდება ყაზბეგის ტური?',
 'From <strong>₾175 per person</strong> (approximately $65). The price includes a comfortable car transfer from your hotel in central Tbilisi, English-speaking guide Timur for the whole day, and entrance fees to all sites. Departure at 08:00, return to Tbilisi around 22:00 — 14 hours total. Maximum 7 people per group: no buses, no strangers. For a group of four, the cost is just ₾32 per person. Pay in cash or by card on the day of the tour.',
 '<strong>₾175-დან ერთ ადამიანზე</strong> (დაახლოებით $65). ფასში შედის კომფორტული ტრანსფერი მანქანით თბილისის ცენტრში მდებარე თქვენი სასტუმროდან, ინგლისურენოვანი გიდი თიმური მთელი დღის განმავლობაში და შესვლის ბილეთები ყველა ობიექტზე. გამგზავრება 08:00-ზე, თბილისში დაბრუნება დაახლოებით 22:00-ზე — სულ 14 საათი. მაქსიმუმ 7 ადამიანი ჯგუფში: არანაირი ავტობუსი, არანაირი უცნობი. ოთხკაციანი ჯგუფისთვის ღირებულება მხოლოდ ₾32-ია ერთ ადამიანზე. გადაიხადეთ ნაღდით ან ბარათით ტურის დღეს.')
faqi('How to book?', 'როგორ დავჯავშნო?',
 'Message us on WhatsApp <strong>+995 511 272 623</strong> or Telegram @SakhvaGuideBot — reply within 15 minutes, daily 08:00–22:00. Just share the date, number of people, and which tour — we\'ll find the right option. Pay on tour day by cash (GEL, USD, EUR) or card.',
 'მოგვწერეთ WhatsApp-ზე <strong>+995 511 272 623</strong> ან Telegram-ზე @SakhvaGuideBot — პასუხი 15 წუთში, ყოველდღე 08:00–22:00. უბრალოდ მოგვწერეთ თარიღი, ადამიანების რაოდენობა და რომელი ტური — შესაფერის ვარიანტს მოვძებნით. გადაიხადეთ ტურის დღეს ნაღდით (GEL, USD, EUR) ან ბარათით.')
faqi('Can I cancel or reschedule?', 'შემიძლია გაუქმება ან თარიღის გადატანა?',
 '<strong>Free cancellation</strong> up to 24 hours before — no questions asked, no penalties. For Kazbegi: if weather is poor on the day, Timur will suggest rescheduling at no charge. You can change the date as many times as needed.',
 '<strong>უფასო გაუქმება</strong> 24 საათით ადრე — ზედმეტი კითხვების და ჯარიმების გარეშე. ყაზბეგისთვის: თუ იმ დღეს ამინდი ცუდია, თიმური შემოგთავაზებთ თარიღის უფასოდ გადატანას. თარიღი შეგიძლიათ იმდენჯერ შეცვალოთ, რამდენჯერაც საჭიროა.')
faqi('When is the best season for Kazbegi?', 'როდის არის საუკეთესო სეზონი ყაზბეგისთვის?',
 'Best months are <strong>May–June</strong> and <strong>September–October</strong>: green slopes, clear skies, Mt. Kazbek fully visible. July–August are fine but can be hot. Winter is magical — snow-covered peaks and almost no tourists. We operate year-round. Tbilisi–Kazbegi is 157 km, about 2.5–3 hours.',
 'საუკეთესო თვეებია <strong>მაისი–ივნისი</strong> და <strong>სექტემბერი–ოქტომბერი</strong>: მწვანე ფერდობები, უღრუბლო ცა, სრულად ხილული მყინვარწვერი. ივლისი–აგვისტო კარგია, მაგრამ შეიძლება ცხელოდეს. ზამთარი ჯადოსნურია — თოვლიანი მწვერვალები და თითქმის არც ერთი ტურისტი. ჩვენ წელიწადის ნებისმიერ დროს ვმუშაობთ. თბილისი–ყაზბეგი 157 კმ-ია, დაახლოებით 2.5–3 საათი.')
faqi('Do I need a visa for Georgia?', 'მჭირდება ვიზა საქართველოსთვის?',
 'No visa is required for most tourists. Citizens of the EU, USA, UK, and 90+ countries enter Georgia visa-free. CIS citizens can enter for up to 365 days. At the border, simply present your passport — no forms or invitations needed.',
 'ტურისტების უმეტესობას ვიზა არ სჭირდება. ევროკავშირის, აშშ-ის, დიდი ბრიტანეთისა და 90-ზე მეტი ქვეყნის მოქალაქეები საქართველოში უვიზოდ შემოდიან. დსთ-ის მოქალაქეებს 365 დღემდე შემოსვლა შეუძლიათ. საზღვარზე უბრალოდ წარადგინეთ პასპორტი — არანაირი ფორმა ან მოწვევა არ არის საჭირო.')
faqi('Are there tours for expats living in Tbilisi?', 'არის ტურები თბილისში მცხოვრები ექსპატებისთვის?',
 'Yes. The Expat Tour is a 4-hour off-the-beaten-path route: markets, neighborhoods, coworking spaces, hidden bars. The Digital Nomad Tour covers best WiFi cafes and comfortable neighborhoods for remote work.',
 'დიახ. ექსპატ-ტური არის 4-საათიანი არასტანდარტული მარშრუტი: ბაზრები, უბნები, ქოვორქინგები, ფარული ბარები. ციფრული მომთაბარის ტური მოიცავს საუკეთესო WiFi-კაფეებსა და დისტანციური მუშაობისთვის კომფორტულ უბნებს.')
faqi('Can I pay with cryptocurrency?', 'შემიძლია გადახდა კრიპტოვალუტით?',
 'Yes, via NOWPayments. USDT (TRC-20), Bitcoin, Ethereum, BNB. You receive a wallet address and QR code. Exchange rate locked for 20 minutes. Cash and card also accepted.',
 'დიახ, NOWPayments-ის მეშვეობით. USDT (TRC-20), Bitcoin, Ethereum, BNB. მიიღებთ საფულის მისამართსა და QR-კოდს. კურსი ფიქსირდება 20 წუთით. ასევე მიიღება ნაღდი და ბარათი.')
faqi('How is a private tour different from a group excursion?', 'რით განსხვავდება კერძო ტური ჯგუფური ექსკურსიისგან?',
 'Group excursions mean 20–40 people on a bus, a fixed schedule, and mandatory tourist shop stops. A private tour with Sakhva Travel means <strong>maximum 7 people</strong>, personal guide Timur, a route adapted to your interests. No buses, no strangers. Four people on Kazbegi = ₾32 per person — cheaper than any bus tour. The quality is incomparable: you stop where you want, photograph as long as you want, eat where you choose.',
 'ჯგუფური ექსკურსია ნიშნავს 20–40 ადამიანს ავტობუსში, ფიქსირებულ გრაფიკსა და სავალდებულო გაჩერებებს ტურისტულ მაღაზიებთან. კერძო ტური Sakhva Travel-თან ნიშნავს <strong>მაქსიმუმ 7 ადამიანს</strong>, პირად გიდ თიმურს, თქვენს ინტერესებზე მორგებულ მარშრუტს. არანაირი ავტობუსი, არანაირი უცნობი. ოთხი ადამიანი ყაზბეგზე = ₾32 ერთ ადამიანზე — ნებისმიერ ავტობუსურ ტურზე იაფი. ხარისხი შეუდარებელია: ჩერდებით სადაც გსურთ, იღებთ იმდენ ხანს, რამდენიც გსურთ, ჭამთ სადაც აირჩევთ.')
faqi('Is it safe to travel to Georgia?', 'უსაფრთხოა საქართველოში მოგზაურობა?',
 '<strong>Georgia is one of the safest countries for tourists.</strong> Street crime is minimal, locals are welcoming. All tourist routes use paved roads with good infrastructure. In 3+ years and 500+ tours, Sakhva Travel has had zero incidents. Georgia ranks highly in global safety indexes.',
 '<strong>საქართველო ერთ-ერთი ყველაზე უსაფრთხო ქვეყანაა ტურისტებისთვის.</strong> ქუჩის დანაშაული მინიმალურია, ადგილობრივები სტუმართმოყვარეები არიან. ყველა ტურისტული მარშრუტი გადის კარგი ინფრასტრუქტურის მქონე ასფალტიან გზებზე. 3+ წლისა და 500+ ტურის განმავლობაში Sakhva Travel-ს არც ერთი ინციდენტი არ ჰქონია. საქართველო მაღალ ადგილს იკავებს გლობალურ უსაფრთხოების ინდექსებში.')
faqi('What if the weather is bad on tour day?', 'რა მოხდება, თუ ტურის დღეს ამინდი ცუდია?',
 'For Kazbegi — guide Timur monitors weather days ahead. If clouds cover the mountains, he\'ll contact you and offer free rescheduling. For Tbilisi and Kakheti — rain is not a problem: sulfur baths, covered markets, wine cellars work great in any weather.',
 'ყაზბეგისთვის — გიდი თიმური ამინდს დღეებით ადრე აკვირდება. თუ ღრუბლები მთებს დაფარავს, დაგიკავშირდებათ და შემოგთავაზებთ უფასო გადატანას. თბილისისა და კახეთისთვის — წვიმა პრობლემა არ არის: გოგირდის აბანოები, დახურული ბაზრები, ღვინის მარნები ნებისმიერ ამინდში მშვენივრად მუშაობს.')
faqi('What languages are tours conducted in?', 'რა ენებზე ტარდება ტურები?',
 'All Sakhva Travel tours are available in <strong>Russian and English</strong>. Guide Timur is fluent in both. For mixed groups, Timur conducts the tour bilingually.',
 'Sakhva Travel-ის ყველა ტური ხელმისაწვდომია <strong>რუსულ და ინგლისურ</strong> ენებზე. გიდი თიმური ორივეს თავისუფლად ფლობს. შერეული ჯგუფებისთვის თიმური ტურს ორ ენაზე ატარებს.')
faqi('How many people can be in a group?', 'რამდენი ადამიანი შეიძლება იყოს ჯგუფში?',
 'Maximum 7 people in one vehicle. Your private group — no strangers. If over 7, we arrange two vehicles. Child seats available; children under 6 ride free.',
 'მაქსიმუმ 7 ადამიანი ერთ ავტომობილში. თქვენი კერძო ჯგუფი — არანაირი უცნობი. თუ 7-ზე მეტია, ვაწყობთ ორ ავტომობილს. ხელმისაწვდომია ბავშვის სავარძლები; 6 წლამდე ბავშვები უფასოდ მგზავრობენ.')
faqi('Where do you pick up for tours?', 'საიდან ხდება ტურებზე წამოყვანა?',
 'From any hotel or apartment in central Tbilisi. Outside the center (Digomi, Gldani, Varketili) — share your address. For Kazbegi, departure at 08:00; for city tours — any time convenient for you.',
 'თბილისის ცენტრში მდებარე ნებისმიერი სასტუმროდან ან ბინიდან. ცენტრის გარეთ (დიღომი, გლდანი, ვარკეთილი) — გაგვიზიარეთ თქვენი მისამართი. ყაზბეგისთვის გამგზავრება 08:00-ზე; საქალაქო ტურებისთვის — თქვენთვის ნებისმიერ მოსახერხებელ დროს.')

faqi('What vehicle is used for tours?', 'რა ავტომობილი გამოიყენება ტურებზე?',
 'Comfortable SUV or minivan with AC, USB charging, child seats on request. For mountain routes (Kazbegi, Kutaisi) we use 4WD vehicles.',
 'კომფორტული ჯიპი ან მინივენი კონდიციონერით, USB-დამტენით, ბავშვის სავარძლებით მოთხოვნისამებრ. მთის მარშრუტებისთვის (ყაზბეგი, ქუთაისი) ვიყენებთ 4WD ავტომობილებს.')
faqi('What is included in the tour price?', 'რა შედის ტურის ფასში?',
 'Hotel pickup and drop-off, English/Russian speaking guide for the full day, entrance tickets to all sites. Not included: meals and souvenirs. Guide recommends restaurants with great food at fair prices.',
 'სასტუმროდან წამოყვანა და დაბრუნება, ინგლისურ/რუსულენოვანი გიდი მთელი დღის განმავლობაში, შესვლის ბილეთები ყველა ობიექტზე. არ შედის: კვება და სუვენირები. გიდი გირჩევთ რესტორნებს გემრიელი საჭმლითა და სამართლიანი ფასებით.')
faqi('Can I change the route during the tour?', 'შემიძლია მარშრუტის შეცვლა ტურის განმავლობაში?',
 'Yes — that\'s the main advantage of a private tour. Want to linger at a waterfall or visit a village you spotted from the window? Just say the word. The route is flexible and the time is yours.',
 'დიახ — ეს კერძო ტურის მთავარი უპირატესობაა. გინდათ ჩანჩქერთან შეყოვნება ან სოფლის მონახულება, რომელიც ფანჯრიდან დაინახეთ? უბრალოდ თქვით. მარშრუტი მოქნილია და დრო თქვენია.')
faqi('Where to eat on the Kazbegi tour?', 'სად ვჭამოთ ყაზბეგის ტურზე?',
 'Guide Timur recommends 2-3 tried restaurants: one near Ananuri Fortress (khinkali with reservoir views), one in Stepantsminda (authentic cuisine without tourist markups). Average lunch: 25-40 GEL per person.',
 'გიდი თიმური გირჩევთ 2-3 გამოცდილ რესტორანს: ერთი ანანურის ციხესთან (ხინკალი წყალსაცავის ხედით), ერთი სტეფანწმინდაში (ავთენტური სამზარეულო ტურისტული ზედნადებების გარეშე). საშუალო სადილი: 25-40 GEL ერთ ადამიანზე.')
faqi('Do you run tours in winter?', 'ატარებთ ტურებს ზამთარში?',
 'Yes, Sakhva Travel operates <strong>year-round</strong>. Winter highlights: snow-covered Kazbegi (when Cross Pass is open), night Tbilisi with festive illumination, Abanotubani sulfur baths. Kakheti in winter = quiet wineries without crowds.',
 'დიახ, Sakhva Travel მუშაობს <strong>მთელი წლის განმავლობაში</strong>. ზამთრის მთავარი მომენტები: თოვლიანი ყაზბეგი (როცა ჯვრის უღელტეხილი ღიაა), ღამის თბილისი სადღესასწაულო განათებით, აბანოთუბნის გოგირდის აბანოები. კახეთი ზამთარში = მშვიდი მარნები ხალხმრავლობის გარეშე.')
faqi('Can I book a tour for tomorrow?', 'შემიძლია ტურის დაჯავშნა ხვალისთვის?',
 'Yes, subject to availability. Message WhatsApp (<strong>+995 511 272 623</strong>) or Telegram (@SakhvaGuideBot) — Timur responds within 15 minutes. In high season (May-October) booking 2-3 days ahead is recommended.',
 'დიახ, ხელმისაწვდომობის მიხედვით. მოგვწერეთ WhatsApp-ზე (<strong>+995 511 272 623</strong>) ან Telegram-ზე (@SakhvaGuideBot) — თიმური პასუხობს 15 წუთში. მაღალ სეზონზე (მაისი-ოქტომბერი) რეკომენდებულია დაჯავშნა 2-3 დღით ადრე.')
faqi('Do you offer multi-day tours?', 'გთავაზობთ მრავალდღიან ტურებს?',
 'Yes. <strong>Slow Travel — 3 days</strong> with guide Timur: a new route each day, airport transfer included. ₾595 all-in. Custom multi-day itineraries also available (e.g. Tbilisi + Kazbegi + Kakheti over 4 days).',
 'დიახ. <strong>Slow Travel — 3 დღე</strong> გიდ თიმურთან: ყოველდღე ახალი მარშრუტი, აეროპორტის ტრანსფერი ჩათვლილი. ₾595 ყველაფრის ჩათვლით. ასევე ხელმისაწვდომია ინდივიდუალური მრავალდღიანი მარშრუტები (მაგ. თბილისი + ყაზბეგი + კახეთი 4 დღეში).')
faqi('Are tours suitable for elderly travelers?', 'ტურები შესაფერისია ხანდაზმული მოგზაურებისთვის?',
 'Yes. All routes follow paved roads with comfortable stops. In Kazbegi we drive up by car, not on foot. The pace is adjusted to your group. The only walking section is the optional ascent to Gergeti Trinity Church.',
 'დიახ. ყველა მარშრუტი გადის ასფალტიან გზებზე კომფორტული გაჩერებებით. ყაზბეგში მანქანით ავდივართ, და არა ფეხით. ტემპი თქვენს ჯგუფზეა მორგებული. ერთადერთი ფეხით მონაკვეთი არის არასავალდებულო ასვლა გერგეტის სამების ეკლესიამდე.')
faqi('What payment methods do you accept?', 'რა გადახდის მეთოდებს იღებთ?',
 'Cash (GEL, USD, EUR), bank cards (Visa, Mastercard), cryptocurrency (USDT, BTC, ETH via NOWPayments). Payment after the tour, no prepayment required. Tips at your discretion.',
 'ნაღდი (GEL, USD, EUR), საბანკო ბარათები (Visa, Mastercard), კრიპტოვალუტა (USDT, BTC, ETH NOWPayments-ის მეშვეობით). გადახდა ტურის შემდეგ, წინასწარი გადახდა არ არის საჭირო. ჩაი — თქვენი შეხედულებისამებრ.')
faqi('How is Sakhva Travel different from Tripster and Viator?', 'რით განსხვავდება Sakhva Travel Tripster-სა და Viator-ისგან?',
 'On aggregator platforms you book an "excursion"; with us you book a specific guide — Timur. The route adapts to you in real time. No platform commission = lower prices. Direct WhatsApp communication, no intermediaries. Free cancellation without the penalties aggregators charge.',
 'აგრეგატორ-პლატფორმებზე თქვენ ჯავშნით „ექსკურსიას“; ჩვენთან კი ჯავშნით კონკრეტულ გიდს — თიმურს. მარშრუტი რეალურ დროში გერგება. პლატფორმის საკომისიოს გარეშე = უფრო დაბალი ფასები. პირდაპირი კომუნიკაცია WhatsApp-ზე, შუამავლების გარეშე. უფასო გაუქმება იმ ჯარიმების გარეშე, რომლებსაც აგრეგატორები იღებენ.')
faqi('What to bring on the Kazbegi tour?', 'რა წავიღოთ ყაზბეგის ტურზე?',
 'Comfortable shoes (trainers), jacket or windbreaker (10-15°C cooler in mountains), sunscreen, water. For Gergeti climb — sports shoes. Winter: warm jacket, hat, gloves. Before each tour, Timur sends recommendations based on weather forecast.',
 'კომფორტული ფეხსაცმელი (ბოტასები), ქურთუკი ან ქარსაფარი (მთებში 10-15°C-ით გრილა), მზისგან დამცავი კრემი, წყალი. გერგეტზე ასვლისთვის — სპორტული ფეხსაცმელი. ზამთარი: თბილი ქურთუკი, ქუდი, ხელთათმანები. ყოველი ტურის წინ თიმური აგზავნის რეკომენდაციებს ამინდის პროგნოზის მიხედვით.')
faqi('Do you offer corporate tours?', 'გთავაზობთ კორპორატიულ ტურებს?',
 'Yes. Groups of 5 to 30 people. Team building, khinkali cooking classes, old Tbilisi quests. Multiple vehicles, English/Russian guides. <strong>From ₾2,200 per group.</strong>',
 'დიახ. ჯგუფები 5-დან 30 ადამიანამდე. თიმბილდინგი, ხინკლის კეთების მასტერკლასები, ძველი თბილისის ქვესტები. რამდენიმე ავტომობილი, ინგლისურ/რუსულენოვანი გიდები. <strong>₾2,200-დან ჯგუფზე.</strong>')
add('cursor:pointer;transition:all .2s">Show more questions <svg', 'cursor:pointer;transition:all .2s">მეტი კითხვის ჩვენება <svg')

# --- LEAD MAGNET ---
add('>Guide: 15 places in Tbilisi + 5% off%</p>', '>გზამკვლევი: თბილისის 15 ადგილი + 5% ფასდაკლება</p>')
add('type="email" placeholder="Email" required aria-label="Email subscribe"',
    'type="email" placeholder="ელფოსტა" required aria-label="ელფოსტის გამოწერა"')
add('white-space:nowrap">Get it</button>', 'white-space:nowrap">მიღება</button>')
add('font-size:15px;color:#111827">Sent — check your inbox</span>',
    'font-size:15px;color:#111827">გაიგზავნა — შეამოწმეთ ფოსტა</span>')

# --- FOOTER ---
add('<p style="color:#6B7280;font-size:13px;line-height:1.6;margin-bottom:16px">Private tours in Georgia. Tbilisi, Kakheti, Kazbegi, Batumi.</p>',
    '<p style="color:#6B7280;font-size:13px;line-height:1.6;margin-bottom:16px">კერძო ტურები საქართველოში. თბილისი, კახეთი, ყაზბეგი, ბათუმი.</p>')
add('text-transform:uppercase">Tours</div>', 'text-transform:uppercase">ტურები</div>')
add('text-transform:uppercase">Destinations</div>', 'text-transform:uppercase">მიმართულებები</div>')
add('text-transform:uppercase">Information</div>', 'text-transform:uppercase">ინფორმაცია</div>')
add('text-transform:uppercase">Contact</div>', 'text-transform:uppercase">კონტაქტი</div>')
add('style="display:block;color:#374151;padding:4px 0">All tours</a>', 'style="display:block;color:#374151;padding:4px 0">ყველა ტური</a>')
add('style="display:block;color:#374151;padding:4px 0">Day trips</a>', 'style="display:block;color:#374151;padding:4px 0">ერთდღიანი ტურები</a>')
add('style="display:block;color:#374151;padding:4px 0">Walking</a>', 'style="display:block;color:#374151;padding:4px 0">ფეხით</a>')
add('style="display:block;color:#374151;padding:4px 0">Wine</a>', 'style="display:block;color:#374151;padding:4px 0">ღვინის</a>')
add('style="display:block;color:#374151;padding:4px 0">Mountain</a>', 'style="display:block;color:#374151;padding:4px 0">მთის</a>')
add('style="display:block;color:#374151;padding:4px 0">Multi-day</a>', 'style="display:block;color:#374151;padding:4px 0">მრავალდღიანი</a>')
add('style="display:block;color:#374151;padding:4px 0">Tbilisi</a>', 'style="display:block;color:#374151;padding:4px 0">თბილისი</a>')
add('style="display:block;color:#374151;padding:4px 0">Kazbegi</a>', 'style="display:block;color:#374151;padding:4px 0">ყაზბეგი</a>')
add('style="display:block;color:#374151;padding:4px 0">Kakheti</a>', 'style="display:block;color:#374151;padding:4px 0">კახეთი</a>')
add('style="display:block;color:#374151;padding:4px 0">Batumi</a>', 'style="display:block;color:#374151;padding:4px 0">ბათუმი</a>')
add('style="display:block;color:#374151;padding:4px 0">Mtskheta</a>', 'style="display:block;color:#374151;padding:4px 0">მცხეთა</a>')
add('style="display:block;color:#374151;padding:4px 0">Svaneti</a>', 'style="display:block;color:#374151;padding:4px 0">სვანეთი</a>')
add('style="display:block;color:#374151;padding:4px 0">About guide</a>', 'style="display:block;color:#374151;padding:4px 0">გიდის შესახებ</a>')
add('style="display:block;color:#374151;padding:4px 0">Gallery</a>', 'style="display:block;color:#374151;padding:4px 0">გალერეა</a>')
add('<div style="font-size:12px;color:#6B7280;margin-bottom:10px">Daily 08:00–22:00</div>',
    '<div style="font-size:12px;color:#6B7280;margin-bottom:10px">ყოველდღე 08:00–22:00</div>')
add('text-transform:uppercase">Find us on maps</div>', 'text-transform:uppercase">გვიპოვეთ რუკებზე</div>')
add('<span>Sakhvadze T.V. TIN 307367383</span>', '<span>სახვაძე თ.ვ. TIN 307367383</span>')
add('<span>14 Merab Kostava St, Tbilisi 0108</span>', '<span>მერაბ კოსტავას ქ. 14, თბილისი 0108</span>')
add('text-underline-offset:2px">Privacy</a>', 'text-underline-offset:2px">კონფიდენციალურობა</a>')
add('text-underline-offset:2px">Refund</a>', 'text-underline-offset:2px">დაბრუნება</a>')

# SECTIONS_MARKER

def run():
    work = open(FILE, encoding="utf-8").read()
    errs = []
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
