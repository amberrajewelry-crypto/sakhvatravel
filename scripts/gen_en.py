#!/usr/bin/env python3
# Generator: EN hiking-from-Kazbegi tour pages, cloned from en/ekskursiya/ekskursiya-truso etalon.
# Reuses verified chrome (styles/scripts/modal/reviews/nav/footer), rewrites only content blocks.
import re as _re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = (ROOT / "en/ekskursiya/ekskursiya-truso/index.html").read_text(encoding="utf-8")
print("EN etalon loaded")

# ---- exact anchors from etalon ----
E_HEROSTATS = (
 '<div class="stat-item"><span class="stat-val">from ₾265</span><span class="stat-lab">per person</span></div>\n'
 '<div class="stat-item"><span class="stat-val">14 hours</span><span class="stat-lab">duration</span></div>\n'
 '<div class="stat-item"><span class="stat-val">up to 7</span><span class="stat-lab">people</span></div>\n'
 '<div class="stat-item"><span class="stat-val">07:00</span><span class="stat-lab">departure</span></div>\n'
 '<div class="stat-item"><span class="stat-val">24 h</span><span class="stat-lab">free cancellation</span></div>')

E_INTRO = '<p>Truso Gorge is one of the least visited yet most spectacular places in Georgia. Located 15 km from Kazbegi, this high-altitude valley offers mineral springs with vivid orange travertine deposits, abandoned medieval Ossetian villages, and sweeping views of the Caucasus range. Only reachable by 4x4 — which keeps the crowds away.</p>'

E_KEYFACT = '<strong>In short:</strong> Truso Gorge Tour from Tbilisi — 14 hours, from ₾265 per person, up to 7 people, departure 07:00. Route includes Ananuri Fortress, Gudauri, Cross Pass. Private guide from Sakhva Travel, direct booking with no agency fees.'

E_PRICEBOX = '''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
<div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">from 265 GEL <span style="font-size:14px;font-weight:400;color:#6B7280">per person</span></div>
<div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">10% discount for groups of 4+</div>'''

E_SECTITLE = 'Tour Schedule — Hour by Hour'

E_ROUTE_START = '<div class="route-grid">'
E_ROUTE_END = '''<div class="route-item">
<div class="route-time">~20:00</div>
<div><div class="route-name">Return to Tbilisi</div><div class="route-desc">Hotel drop-off.</div></div>
</div>
</div>'''

E_MAPSTOPS = 'var stops=[{"name": "Tbilisi", "lat": 41.6938, "lng": 44.8015}, {"name": "Ananuri", "lat": 42.1642, "lng": 44.7069}, {"name": "Gudauri", "lat": 42.478, "lng": 44.4802}, {"name": "Jvari Pass", "lat": 42.5045, "lng": 44.4534}, {"name": "Truso Valley", "lat": 42.605, "lng": 44.48}];'
E_MAPCAP = 'Route: Tbilisi → Ananuri → Gudauri → Jvari Pass → Truso Valley'

# big content: from first section h2 through the "Full Tour Route" 3rd paragraph (etalon lines 303-316)
E_SEC_A = '''<h2>Truso Gorge — The Hidden Valley Near Kazbegi</h2>
<p>While thousands of tourists visit Gergeti Trinity Church each day, almost none venture into the Truso Gorge. Yet Truso is arguably more spectacular. The gorge runs parallel to Kazbegi along a Terek River tributary, with walls closing in to create a corridor of volcanic rock. At the valley floor, mineral springs bubbling up through iron-rich earth have created orange and ochre travertine formations unlike anything else in Georgia.</p>
<p>The gorge was inhabited until 1991 when the Ossetian-Georgian conflicts caused the local population to leave. The stone towers and farmhouses of Zakagor village remain standing and intact — an abandoned medieval settlement frozen in time. Walking through the empty village with watch towers still upright is one of the most atmospheric experiences available in the entire Caucasus region.</p>
<h2>The Mineral Springs of Truso</h2>
<p>The main attraction of Truso is the mineral springs and the "narzan" travertine lakes they form, with vivid orange banks made of iron deposits. The water here is saturated with CO₂ and various minerals — the same type of springs as Borjomi mineral water, but completely wild and untouched.</p>
<p>The springs emerge at multiple points along the valley floor. The iron content turns the surrounding rocks and sediment vivid orange, while the springs create small travertine pools and terraces of remarkable beauty. The water is drinkable — strongly fizzy and rich in minerals. Local knowledge holds these springs have medicinal properties; geologists confirm they are among the most mineralised natural water sources in Georgia.</p>
<p>The Kviriki waterfall drops 20 metres into a small canyon at the gorge head. On a clear day the water breaks into thousands of rainbows as it falls. The walk to the waterfall takes about 40 minutes along a dirt trail from the mineral springs.</p>
<h2>The Deserted Medieval Villages</h2>
<p>The gorge preserves the ruins of several medieval villages abandoned in the 20th century. Stone houses, churches and defensive towers are gradually being reclaimed by nature — but for now they still stand, creating an atmosphere of lost civilisation. The largest and best-preserved is Zakagor, which has watch towers still fully intact and even climbable with care.</p>
<p>Truso Gorge lies close to Kazbegi, so tours can sometimes be combined: see also our <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/">Kazbegi tour from Tbilisi</a>.</p>
<h2>Full Tour Route — What to See and Do</h2>
<p>The Truso Gorge tour starts early in the morning — your guide meets you in Tbilisi and drives north on the comfortable 4x4 towards Kazbegi. Along the way you enjoy scenic mountain views and stop at Ananuri Fortress for photographs above the Zhinvali Reservoir. Then the route continues through Gudauri and over the Cross Pass (2,395 m) towards the Truso valley entrance.</p>
<p>On arrival at the gorge we begin walking along the banks of the travertine springs, where bright orange and green iron deposits create a completely unique landscape. We then head to the Kviriki waterfall, one of the most beautiful spots in the area, before exploring the deserted medieval village of Zakagor with its intact stone towers. The day ends with a riverside picnic before the return drive to Tbilisi, arriving with memories and photographs that will stay with you forever.</p>
<p>Pay attention to the local flora and fauna along the trail: rare plant and animal species live only in this high-altitude region. Your guide will share stories about the culture and history of Georgia throughout the day. In Truso Gorge you can experience true harmony with nature and enjoy the atmosphere of complete solitude, far from city life.</p>'''

# practical tips block (etalon lines 317-325)
E_SEC_B = '''<h2>Practical Tips for the Tour</h2>
<p>Preparing properly for the Truso Gorge tour will make the day much more enjoyable. The trail involves walking on uneven rocky terrain at altitude, so your footwear choice matters more than for most tours. Light windproof or fleece layers are a good idea since temperatures at altitude are noticeably cooler than in Tbilisi — even in summer.</p>
<ul>
<li><strong>Proper footwear.</strong> Wear trekking boots or trainers with a good sole. Flat sandals or city shoes will make the rocky trail uncomfortable and can be slippery near the springs.</li>
<li><strong>Water and snacks.</strong> Bring enough drinking water and light snacks (nuts, dried fruit, energy bars) to sustain energy throughout the active hiking portions of the day.</li>
<li><strong>Sun protection.</strong> At high altitude UV radiation is significantly stronger. Bring sunscreen and a hat even if the weather feels cool — you will be outdoors for most of the day.</li>
<li><strong>Camera or phone.</strong> The mineral springs with their orange formations, the waterfall, and the deserted village are all highly photogenic. A good camera or phone with a quality lens is essential for making the most of the scenery.</li>
<li><strong>Warm layer for the gorge.</strong> Summer temperatures in Truso are 15–18°C — a light jacket or fleece is recommended even if Tbilisi was 35°C when you left.</li>
</ul>'''

# FAQ visible (etalon lines 330-339, the 5 h3/p after "Frequently Asked Questions")
E_FAQV = '''<h3>How long is the Truso Gorge tour from Tbilisi?</h3>
<p>The tour takes a full day, departing early morning and returning in the evening. Total time on the road and in the gorge is approximately 14 hours, including the drive, stops along the Georgian Military Highway, and 5–6 hours of activity inside the gorge itself.</p>
<h3>Is this tour suitable for families with children?</h3>
<p>Yes, the tour is suitable for families with children, but you should consider your children's level of physical fitness. If they enjoy active outdoor walks and are comfortable on uneven ground, this will be an excellent family experience in a truly wild setting.</p>
<h3>Can I book a private tour?</h3>
<p>Yes, all Sakhva Travel tours are private — you will not be mixed with strangers. The itinerary can be adapted to your preferences and interests. Contact us in advance and we will discuss all the details.</p>
<h3>Why is a 4x4 required for Truso?</h3>
<p>The track into Truso crosses rocky riverbeds and becomes impassable for standard vehicles after rain. Even in dry conditions the terrain requires high clearance and four-wheel drive. A 4x4 is mandatory — Timur uses a properly equipped vehicle for all Truso tours, no exceptions.</p>
<h3>What makes Truso different from Kazbegi?</h3>
<p>Kazbegi is about the mountain panorama and the famous Gergeti Trinity Church. Truso is about true wilderness: orange mineral springs, dramatic travertine geology, an abandoned medieval village, a 20 m waterfall, and almost no other tourists. The landscapes are completely different. Many visitors who have experienced both say Truso was the more memorable of the two.</p>'''

E_TIP = '<p>Truso is the least-known gorge near Kazbegi, and that is precisely its value. While tourists crowd Gergeti, I take my groups to the blue mineral springs where water emerges fully saturated with carbon dioxide — it bubbles out of the rock like natural soda water. The road into the gorge is 4x4 only: after the rainy season the dirt track gets washed out badly. A mandatory stop is the medieval village of Zakagor with its abandoned towers. It has stood empty since 1991, but the walls and floors are still intact. The view from the top of the main watch tower across the deserted village and the gorge below is extraordinary. Gorge temperature in summer is +15–18°C — bring a light jacket even if Tbilisi was +35 when you left.</p>'

E_WHY = '<p>Truso Gorge in one long day from Tbilisi: CO₂ mineral springs with orange travertine deposits, the abandoned medieval village of Zakagor, a 20 m waterfall, and complete solitude. The trail is 12 km one way, but we cover part of the route in the 4x4 and walk only the most beautiful section on foot. The closest thing to exploring an undiscovered wilderness in the Caucasus — 15 km from Kazbegi, but a world away from the tourist trail.</p>'

E_INCL = '<ul><li>4x4 transfer from Tbilisi hotel and back</li><li>Private English-speaking guide</li><li>Truso gorge trail and mineral springs</li><li>Zakagor and Ketristskhe deserted village visit</li><li>Kviriki waterfall</li><li>Ananuri Fortress stop</li></ul>'
E_NOTINCL = '<ul style="color:#991B1B"><li>Food (bring your own picnic)</li><li>Trekking boots (your own equipment)</li></ul>'

E_PRACT = '''<h2>Practical Information</h2>
<p>The tour starts from your hotel in Tbilisi. I pick you up in a comfortable air-conditioned 4x4 vehicle. Maximum 7 people per group — individual attention for every guest. The itinerary is flexible: I can add or remove stops based on your wishes. Languages: English, Russian, Georgian.</p>
<h3>Booking and Payment</h3>
<p>Message me on WhatsApp (+995 511 272 623) — I reply within 10–15 minutes, including evenings. A 10% deposit confirms your booking; the balance is paid on the day of the tour. I accept cash GEL (₾), bank transfer, and cryptocurrency. Free cancellation up to 24 hours before departure. During high season (May–October) book at least 3–5 days in advance.</p>
<h3>What to Bring</h3>
<p>Comfortable shoes suitable for walking on rocky terrain (even for car-based tours there will be walks of 30–60 minutes or more), a water bottle (I provide an extra one), and cash GEL for lunch and souvenirs. In winter: a warm jacket and gloves. In summer: sunscreen and a hat. A light windproof layer is always recommended for the gorge regardless of season.</p>'''

E_READALSO = '<div class="tour-readalso" style="margin:28px 0;padding:16px 20px;background:#f0f7f4;border-left:4px solid #2E7D32;border-radius:0 8px 8px 0;font-size:15px"><strong>Read also:</strong> <a href="/en/blog/kazbegi-complete-guide/">Kazbegi: the complete guide</a></div>'

E_TITLE_FULL = 'Truso Gorge Tour from Tbilisi 2026 | Sakhva Travel'
E_NAME = 'Truso Gorge Tour from Tbilisi'
E_DESC_OGTW = 'Truso Gorge tour from Tbilisi with a private tour from ₾265. Mineral springs, travertine lakes, deserted medieval village Zakagor. 14 hours, up to 7 people.'
E_DESC_META = 'Truso Gorge tour from Tbilisi with a private tour from ₾265. Mineral springs, travertine lakes, medieval village Zakagor. 14 hours, up to 7 people.'
E_DESC_ENT = 'Truso Gorge tour from Tbilisi with a private tour from &#8382;265. Mineral springs, travertine lakes, deserted medieval village Zakagor. 14 hours, up to 7 people.'
E_WA = 'I+want+to+book+Truso+Gorge+tour+from+Tbilisi+2026'
E_OFFER_PRICE = '"price":"265"'
E_READALSO_KEEP = E_READALSO


def rep(h, old, new, count=1):
    if count == 0:
        assert old in h, f"MISS(all): {old[:70]!r}"
        return h.replace(old, new)
    assert h.count(old) >= count, f"MISS x{count}: {old[:70]!r} (found {h.count(old)})"
    return h.replace(old, new, count)


def build(d):
    h = BASE
    # content blocks first (some anchors still contain ekskursiya-truso)
    h = rep(h, E_HEROSTATS, d["herostats"])
    h = rep(h, E_INTRO, d["intro"])
    h = rep(h, E_KEYFACT, d["keyfact"])
    h = rep(h, E_PRICEBOX, d["pricebox"])
    h = rep(h, E_SECTITLE, d["sectitle"])
    # route grid: replace whole inner
    a = h.index(E_ROUTE_START)
    b = h.index(E_ROUTE_END) + len(E_ROUTE_END)
    h = h[:a] + '<div class="route-grid">\n' + d["route"] + '\n</div>' + h[b:]
    h = rep(h, E_MAPSTOPS, d["mapstops"])
    h = rep(h, E_MAPCAP, d["mapcap"], 0)  # appears in caption <p> and boot? only caption -> use count all safe
    h = rep(h, E_SEC_A, d["sec_a"])
    h = rep(h, E_SEC_B, d["sec_b"])
    h = rep(h, E_READALSO_KEEP, d.get("readalso", E_READALSO))
    h = rep(h, E_FAQV, d["faqv"])
    h = rep(h, E_TIP, d["tip"])
    h = rep(h, E_WHY, d["why"])
    h = rep(h, E_INCL, d["incl"])
    h = rep(h, E_NOTINCL, d["notincl"])
    h = rep(h, E_PRACT, d["pract"])
    h = rep(h, d["faq_schema_old"], d["faq_schema"])
    h = rep(h, E_WA, d["wa"])
    # head / meta / globals — replace desc (which still contains ₾265) BEFORE numeric fixes
    h = rep(h, E_TITLE_FULL, d["title"], 0)
    h = rep(h, E_DESC_OGTW, d["desc"], 0)
    h = rep(h, E_DESC_META, d["desc"])
    h = rep(h, E_DESC_ENT, d["desc_ent"], 0)
    h = rep(h, E_NAME, d["name"], 0)
    # numeric / mobile fixes: only mobile-sticky still holds 'from ₾265' now
    h = rep(h, E_OFFER_PRICE, f'"price":"{d["price"]}"')
    h = rep(h, 'from ₾265', f'from ₾{d["price"]}', 0)
    h = rep(h, '>Guided tour<', '>Hike from Kazbegi<')
    h = rep(h, "ekskursiya-truso", d["slug"], 0)
    h = h.replace("__TBILISI_TRUSO__", "ekskursiya-truso")  # restore intent-split link to from-Tbilisi tour
    _img = "truso-tour-600" if "truso" in d["slug"] else ("gveleti-hike-600" if "gveleti" in d["slug"] else "juta-chaukhi-hike-600")
    h = h.replace("truso-tour-600", _img)
    return h


# etalon FAQ schema block (line 46) — needed as anchor
E_FAQ_SCHEMA = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long is the Truso Gorge tour from Tbilisi?","acceptedAnswer":{"@type":"Answer","text":"The Truso Gorge tour takes a full day — departing early morning and returning in the evening. The total time is approximately 14 hours, including the drive from Tbilisi, stops along the way, and the hike through the gorge."}},{"@type":"Question","name":"Is this tour suitable for families with children?","acceptedAnswer":{"@type":"Answer","text":"Yes, the tour is suitable for families with children, but you should consider your children\'s fitness level. If they enjoy active outdoor walks, this will be a great family experience."}},{"@type":"Question","name":"Can I book a private tour?","acceptedAnswer":{"@type":"Answer","text":"Yes, we offer private tours that can be adapted to your preferences and interests. Just contact us in advance and we will discuss all the details."}},{"@type":"Question","name":"Why is a 4x4 required?","acceptedAnswer":{"@type":"Answer","text":"The track into Truso crosses rocky riverbeds and becomes impassable for standard vehicles after rain. Even in dry conditions the terrain requires high clearance. A 4x4 is mandatory — Timur uses a properly equipped vehicle for all Truso tours."}},{"@type":"Question","name":"What makes Truso different from Kazbegi?","acceptedAnswer":{"@type":"Answer","text":"Kazbegi is about the mountain view and the famous church. Truso is about wilderness: orange mineral springs, travertine geology, an abandoned medieval village, a waterfall, and almost no other tourists. Many visitors who have done both say Truso was the more memorable experience."}}]}'


# ===================== GVELETI (EN) =====================
G = dict(
 slug="hayking-gveleti-iz-kazbegi",
 price="350",
 title="Gveleti Waterfall Hike from Kazbegi — from ₾350",
 name="Gveleti Waterfall Hike from Kazbegi",
 desc="Gveleti waterfall hike from Kazbegi — from ₾350 per car. An easy half-day to two waterfalls near Stepantsminda, no jeep needed. 2–3 hours, up to 7 people.",
 desc_ent="Gveleti waterfall hike from Kazbegi — from &#8382;350 per car. An easy half-day to two waterfalls near Stepantsminda, no jeep needed. 2–3 hours, up to 7 people.",
 wa="I+want+to+book+the+Gveleti+waterfall+hike+from+Kazbegi",
 herostats=('<div class="stat-item"><span class="stat-val">from ₾350</span><span class="stat-lab">per car</span></div>\n'
  '<div class="stat-item"><span class="stat-val">2–3 h</span><span class="stat-lab">duration</span></div>\n'
  '<div class="stat-item"><span class="stat-val">up to 7</span><span class="stat-lab">people</span></div>\n'
  '<div class="stat-item"><span class="stat-val">Kazbegi</span><span class="stat-lab">start</span></div>\n'
  '<div class="stat-item"><span class="stat-val">easy</span><span class="stat-lab">level</span></div>'),
 intro='<p>The Gveleti waterfalls are the easiest and most rewarding short hike near Kazbegi. Just 7 km from Stepantsminda, a gentle trail leads through a birch gorge to two waterfalls — a wide lower cascade and a taller, hidden upper one. No jeep and no serious effort required: it is the perfect half-day walk if you are already in Kazbegi and want a real mountain waterfall without a full expedition.</p>',
 keyfact='<strong>In short:</strong> The Gveleti waterfall hike is an easy half-day from Stepantsminda (Kazbegi), from ₾350 per car (a group of up to 7 — the price is split across the group, so the more people, the cheaper per person). We drive to the trailhead near Gveleti village, then walk about 4 km round trip to the two waterfalls, 2–3 hours in total. This is a border zone — bring your passport, but no permit is needed. Access almost year-round. Russian- and English-speaking guide from Sakhva Travel, direct booking with no agency fees.',
 pricebox='''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
<div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">from 350 GEL <span style="font-size:14px;font-weight:400;color:#6B7280">per car</span></div>
<div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">Price per car — the more people, the cheaper per person</div>''',
 sectitle="Hike Schedule — Step by Step",
 route='''<div class="route-item">
<div class="route-time">10:00</div>
<div><div class="route-name">Meeting in Stepantsminda</div><div class="route-desc">Pickup from your accommodation in Kazbegi / Stepantsminda. Short briefing.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:20</div>
<div><div class="route-name">Drive to Gveleti</div><div class="route-desc">7 km north along the Military Highway towards the Dariali gorge.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:40</div>
<div><div class="route-name">Gveleti village — trailhead</div><div class="route-desc">We leave the car and cross the bridge over the Terek to the trail.</div></div>
</div>
<div class="route-item">
<div class="route-time">11:00</div>
<div><div class="route-name">Birch gorge trail</div><div class="route-desc">A gentle path along the stream, easy underfoot.</div></div>
</div>
<div class="route-item">
<div class="route-time">11:20</div>
<div><div class="route-name">Lower Gveleti waterfall</div><div class="route-desc">The wide, powerful cascade — the classic photo spot.</div></div>
</div>
<div class="route-item">
<div class="route-time">11:45</div>
<div><div class="route-name">Upper waterfall</div><div class="route-desc">Taller and hidden higher up the gorge — worth the extra few minutes.</div></div>
</div>
<div class="route-item">
<div class="route-time">12:15</div>
<div><div class="route-name">Free time and photos</div><div class="route-desc">Relax by the falls before heading back.</div></div>
</div>
<div class="route-item">
<div class="route-time">12:45</div>
<div><div class="route-name">Return to Stepantsminda</div><div class="route-desc">Drop-off at your accommodation. The rest of the day is yours.</div></div>
</div>''',
 mapstops='var stops=[{"name": "Stepantsminda", "lat": 42.6579, "lng": 44.6417}, {"name": "Gveleti village", "lat": 42.7069, "lng": 44.6289}, {"name": "Gveleti waterfall", "lat": 42.7156, "lng": 44.6222}];',
 mapcap='Route: Stepantsminda → Gveleti village → Gveleti waterfalls',
 sec_a='''<h2>Two waterfalls in one gorge</h2>
<p>Most visitors know only the lower Gveleti waterfall — the wide, powerful cascade you reach first. But the gorge hides a second, upper waterfall higher up the stream: taller, narrower and far quieter, since most day-trippers turn back at the first one. We walk to both. The extra ten minutes to the upper fall is the difference between a nice photo stop and a proper little mountain adventure.</p>
<p>The whole route runs through a birch gorge along a clear stream, with the Terek valley and the Dariali gorge walls rising behind you. It is short — about 4 km round trip — but genuinely scenic the whole way.</p>
<h2>How to get there — no jeep needed</h2>
<p>Unlike Truso or Juta, Gveleti needs no 4x4. The trailhead sits right off the Georgian Military Highway, 7 km north of Stepantsminda towards the Russian border, and an ordinary car reaches it easily. That is exactly why Gveleti is the ideal light hike when you are already in Kazbegi: minimal driving, an easy walk, two real waterfalls, back before lunch.</p>
<p>If you are coming from the capital instead, it makes more sense as part of a full Kazbegi day — see our <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/">Kazbegi tour from Tbilisi</a>.</p>''',
 sec_b='''<h2>Border zone: bring your passport</h2>
<p>Gveleti lies close to the Russian border, inside Georgia's border zone. There is a checkpoint on the highway and the guards may ask to see your documents, so <strong>bring your passport</strong>. No permit or advance paperwork is needed — access to the waterfalls is free and open. Just keep your ID with you.</p>
<h2>When to go: seasons and weather</h2>
<p>Gveleti is one of the few hikes near Kazbegi that works almost year-round. The best months are May to October, when the trail is dry and the falls are full. In winter the path can be icy and the upper section slippery — passable with care on a clear day, but we check conditions first. At around 1,700–1,900 m it is always cooler than Tbilisi, so bring a light jacket even in summer.</p>
<h2>Difficulty, children and fitness</h2>
<p>This is an easy walk suitable for almost everyone, including children of school age. The trail is short and mostly flat, with only a gentle climb to the upper waterfall. No hiking experience is needed. The only thing that matters is footwear — the ground is rocky and can be muddy or slippery near the water.</p>
<h2>What to bring</h2>
<ul>
<li><strong>Passport.</strong> Border zone — the checkpoint may ask for ID.</li>
<li><strong>Comfortable shoes.</strong> Trainers or trekking shoes with grip; the rock near the falls gets wet and slippery.</li>
<li><strong>A light jacket.</strong> It is cooler and windier by the water, even on a warm day.</li>
<li><strong>Water and a snack.</strong> There are no cafes on the trail.</li>
</ul>
<div style="margin:22px 0;padding:20px 22px;background:#F0F7F2;border-left:4px solid #1A3D2E;border-radius:8px">
<div style="font-family:'Lora',serif;font-size:18px;color:#1A3D2E;font-weight:600;margin-bottom:8px">Weather guarantee</div>
<p style="margin:0;color:#374151;line-height:1.65">Mountain weather changes fast. Timur checks the forecast the day before. If it is unsafe to walk on the day — heavy rain, ice — we <strong>reschedule for free</strong> or offer an equivalent nearby alternative (Gergeti, Juta), so your day is never wasted.</p>
</div>''',
 readalso='<div class="tour-readalso" style="margin:28px 0;padding:16px 20px;background:#f0f7f4;border-left:4px solid #2E7D32;border-radius:0 8px 8px 0;font-size:15px"><strong>Read also:</strong> <a href="/en/blog/kazbegi-complete-guide/">Kazbegi: the complete guide</a></div>',
 faqv='''<h3>How long is the Gveleti waterfall hike?</h3>
<p>An easy half-day, about 2–3 hours in total from Stepantsminda: a short 7 km drive to the trailhead, then roughly 4 km round trip on foot to the two waterfalls. You are back in Kazbegi well before lunch.</p>
<h3>Do I need a jeep or 4x4?</h3>
<p>No. Unlike Truso and Juta, the Gveleti trailhead is right off the Georgian Military Highway and an ordinary car reaches it easily. That is what makes it the perfect light hike near Kazbegi.</p>
<h3>How much does it cost and why per car?</h3>
<p>From ₾350 per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi/Stepantsminda, the drive to the trailhead and back, and a Russian- or English-speaking guide. A 10% deposit confirms; the balance is cash GEL on the day.</p>
<h3>Do I need a passport?</h3>
<p>Yes — Gveleti is in the border zone and there is a checkpoint on the highway where guards may ask for ID. Bring your passport. No permit is required and access to the falls is free.</p>
<h3>Is it suitable for children and people with no experience?</h3>
<p>Yes. The trail is short and mostly flat, with only a gentle climb to the upper fall, so it suits children of school age and anyone without hiking experience. Just wear shoes with grip — the rock near the water is slippery.</p>''',
 tip='<p>My advice: do not stop at the first waterfall like most people do. The lower cascade is the wide, photogenic one, but the upper fall — just ten more minutes up the gorge — is taller and almost always empty. Go in the morning while the light is on the water and the trail is quiet. And keep your passport in your pocket: the checkpoint on the highway is quick, but they do ask. Even in summer bring a light jacket — by the falls it is always a few degrees cooler and the spray is cold.</p>',
 why='<p>Gveleti is the easiest real waterfall near Kazbegi: two cascades, a short scenic trail through a birch gorge, no jeep and no hard climbing — a perfect half-day if you are already in Stepantsminda. Ideal when you have seen Gergeti and Kazbek and want one more genuine mountain spot without committing to a full expedition.</p>',
 incl='<ul><li>Car with driver from Kazbegi/Stepantsminda</li><li>Russian- or English-speaking guide</li><li>Drive to the Gveleti trailhead and back</li><li>Walk to both the lower and upper waterfalls</li><li>Birch gorge and Terek valley views</li></ul>',
 notincl='<ul style="color:#991B1B"><li>Food and snacks (bring your own)</li><li>Personal hiking shoes and clothing</li></ul>',
 pract='''<h2>Practical Information</h2>
<p>The hike starts right in Kazbegi: I pick you up from your accommodation in Stepantsminda or the nearby villages in a comfortable car. Maximum 7 people per group — individual attention. Departure time is flexible, but mornings are best. Languages: English, Russian, Georgian.</p>
<h3>Booking and Payment</h3>
<p>Message me on WhatsApp (+995 511 272 623) — I reply within 10–15 minutes, including at night. A 10% deposit confirms your booking; the balance is paid on the day. I accept cash GEL (₾), bank transfer, and cryptocurrency. Free cancellation up to 24 hours before. In high season (June–September) book 2–3 days ahead.</p>
<h3>A hike from Kazbegi, or a tour from Tbilisi?</h3>
<p>This walk is for travellers who are <strong>already in Kazbegi</strong>. If you are coming from the capital, see the <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/">Kazbegi tour from Tbilisi</a> — Gergeti, Ananuri and the Georgian Military Highway in one day.</p>''',
 faq_schema_old=E_FAQ_SCHEMA,
 faq_schema='{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long is the Gveleti waterfall hike?","acceptedAnswer":{"@type":"Answer","text":"An easy half-day, about 2-3 hours in total from Stepantsminda: a short 7 km drive to the trailhead, then roughly 4 km round trip on foot to the two waterfalls."}},{"@type":"Question","name":"Do I need a jeep or 4x4 for Gveleti?","acceptedAnswer":{"@type":"Answer","text":"No. Unlike Truso and Juta, the Gveleti trailhead is right off the Georgian Military Highway and an ordinary car reaches it easily. That is what makes it the perfect light hike near Kazbegi."}},{"@type":"Question","name":"How much does it cost and why per car?","acceptedAnswer":{"@type":"Answer","text":"From 350 GEL per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi and Stepantsminda, the drive to the trailhead and back, and a Russian or English speaking guide."}},{"@type":"Question","name":"Do I need a passport?","acceptedAnswer":{"@type":"Answer","text":"Yes. Gveleti is in the border zone and there is a checkpoint on the highway where guards may ask for ID. Bring your passport. No permit is required and access to the falls is free."}},{"@type":"Question","name":"Is it suitable for children and people with no experience?","acceptedAnswer":{"@type":"Answer","text":"Yes. The trail is short and mostly flat, with only a gentle climb to the upper fall, so it suits children of school age and anyone without hiking experience."}}]}',
)

html = build(G)
out = ROOT / "en/ekskursiya" / G["slug"] / "index.html"
out.write_text(html, encoding="utf-8")
words = len(_re.sub(r"<[^>]+>", " ", _re.sub(r"<(script|style).*?</\1>", "", html, flags=_re.S)).split())
print(f"Gveleti EN: {out}  ~{words} words")


# ===================== TRUSO (EN, from Kazbegi, per car) =====================
T = dict(
 slug="hayking-truso-iz-kazbegi",
 price="500",
 title="Truso Valley Trek from Kazbegi — from ₾500",
 name="Truso Valley Trek from Kazbegi",
 desc="Truso valley trek from Kazbegi — from ₾500 per car. Orange travertine springs, Zakagori fortress and a wild border valley. 5–7 hours, 4x4 required.",
 desc_ent="Truso valley trek from Kazbegi — from &#8382;500 per car. Orange travertine springs, the Zakagori fortress and a wild border valley. 5-7 hours, 4x4 required, up to 7 people.",
 wa="I+want+to+book+the+Truso+valley+trek+from+Kazbegi",
 herostats=('<div class="stat-item"><span class="stat-val">from ₾500</span><span class="stat-lab">per car</span></div>\n'
  '<div class="stat-item"><span class="stat-val">5–7 h</span><span class="stat-lab">duration</span></div>\n'
  '<div class="stat-item"><span class="stat-val">up to 7</span><span class="stat-lab">people</span></div>\n'
  '<div class="stat-item"><span class="stat-val">Kazbegi</span><span class="stat-lab">start</span></div>\n'
  '<div class="stat-item"><span class="stat-val">moderate</span><span class="stat-lab">level</span></div>'),
 intro='<p>The Truso valley is the wildest place within easy reach of Kazbegi: a broad high-altitude gorge lined with bright orange travertine springs, medieval Ossetian watchtowers and the lonely Zakagori fortress, all framed by the Caucasus ridge and almost no other tourists. A 4x4 takes you deep into the valley, then a long, flat walk along the riverbed brings you past the springs to the fortress. If you are already in Kazbegi and want one real, remote mountain day, this is it.</p>',
 keyfact='<strong>In short:</strong> The Truso valley trek is a half-day from Stepantsminda (Kazbegi), from ₾500 per car (a group of up to 7 — the price is split across the group). A 4x4 is required: only a jeep can cross the fords into the valley. Once inside, we walk the flat valley floor past the travertine mineral springs to the Zakagori fortress (2,231 m), 5–7 hours in total. This is a border zone — passport required, no permit needed. Season May–October. Russian- and English-speaking guide from Sakhva Travel, direct booking with no agency fees.',
 pricebox='''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
<div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">from 500 GEL <span style="font-size:14px;font-weight:400;color:#6B7280">per car</span></div>
<div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">Price per car — the more people, the cheaper per person</div>''',
 sectitle="Trek Schedule — Step by Step",
 route='''<div class="route-item">
<div class="route-time">09:30</div>
<div><div class="route-name">Meeting in Stepantsminda</div><div class="route-desc">Pickup from your accommodation in Kazbegi / Stepantsminda. Short briefing.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:00</div>
<div><div class="route-name">Drive to the valley entrance</div><div class="route-desc">South towards Kobi, then off the highway onto the dirt track — 4x4 only from here.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:40</div>
<div><div class="route-name">4x4 through the fords</div><div class="route-desc">The jeep crosses shallow river braids into the Truso valley — the drive itself is part of the adventure.</div></div>
</div>
<div class="route-item">
<div class="route-time">11:15</div>
<div><div class="route-name">Travertine mineral springs</div><div class="route-desc">CO₂-rich springs staining the valley floor vivid orange — like natural soda bubbling from the rock.</div></div>
</div>
<div class="route-item">
<div class="route-time">12:15</div>
<div><div class="route-name">Zakagori fortress (2,231 m)</div><div class="route-desc">A lonely medieval fortress on a rise, the last point before the closed border.</div></div>
</div>
<div class="route-item">
<div class="route-time">13:00</div>
<div><div class="route-name">Riverside picnic</div><div class="route-desc">Lunch with your own supplies among the towers and meadows.</div></div>
</div>
<div class="route-item">
<div class="route-time">14:00</div>
<div><div class="route-name">Walk and drive back</div><div class="route-desc">Back along the valley floor to the jeep, then out over the fords.</div></div>
</div>
<div class="route-item">
<div class="route-time">15:30</div>
<div><div class="route-name">Return to Stepantsminda</div><div class="route-desc">Drop-off at your accommodation.</div></div>
</div>''',
 mapstops='var stops=[{"name": "Stepantsminda", "lat": 42.6579, "lng": 44.6417}, {"name": "Truso valley entrance", "lat": 42.611, "lng": 44.489}, {"name": "Truso springs", "lat": 42.605, "lng": 44.455}, {"name": "Zakagori fortress", "lat": 42.601, "lng": 44.428}];',
 mapcap='Route: Stepantsminda → Truso valley entrance → travertine springs → Zakagori fortress',
 sec_a='''<h2>Truso from Kazbegi — the wild border valley</h2>
<p>Truso runs parallel to the main Kazbegi valley along a tributary of the Terek. Its walls close into a corridor of volcanic rock, and along the flat floor mineral springs bubble up through iron-rich earth, staining the ground orange and ochre in a way you see nowhere else in Georgia. Because a 4x4 is the only way in, the valley stays almost empty — you often have the springs and the towers entirely to yourself.</p>
<p>Starting from Kazbegi rather than the capital changes the whole day: instead of six hours on the road you get straight to the valley and spend the time on the ground, walking the springs and the fortress at an unhurried pace.</p>
<h2>The travertine mineral springs</h2>
<p>The signature of Truso is its "narzan" springs — carbon-dioxide-saturated water, the same family as Borjomi, but completely wild. The iron content turns the surrounding sediment vivid orange and builds small travertine terraces and pools along the valley floor. The water is drinkable, strongly fizzy and mineral-rich; these are among the most mineralised natural sources in the country.</p>
<h2>Zakagori fortress and the deserted villages</h2>
<p>On a rise deep in the valley stands the Zakagori fortress (2,231 m), the furthest point of the walk — beyond it the valley leads to the closed border and is off-limits. Around it are the stone towers and farmhouses of villages abandoned in the 1990s, still standing, slowly returning to the mountain. Walking among the empty towers with the ridge behind them is one of the most atmospheric experiences in the whole Caucasus.</p>
<h2>Why a 4x4 is required</h2>
<p>There is no paved road into Truso — only a dirt track that crosses several river braids and gets washed out after rain. An ordinary car cannot make it; a proper 4x4 is mandatory, and Timur uses one equipped for these fords. The jeep drive across the water is a genuine part of the adventure, not just transport.</p>''',
 sec_b='''<h2>Border zone: passport required</h2>
<p>Truso sits right against the Russian border, inside Georgia's border zone. There is a checkpoint at the valley entrance and the guards check documents, so a <strong>passport is required</strong> — without it you will not be let in. No advance permit is needed and access is free; the Zakagori fortress is the last point you may reach, beyond it is closed.</p>
<h2>When to go: season and weather</h2>
<p>The Truso season runs <strong>May to October</strong>, with June–September the most reliable. In winter the track is buried in snow and the valley is closed; after heavy rain the entrance is sometimes shut for a day while the fords settle. At around 2,000 m it is cool even in summer (10–18°C) and the weather turns quickly — bring a jacket and a rain layer.</p>
<h2>Difficulty and fitness</h2>
<p>The walking itself is not steep — the valley floor is flat — but it is long, at altitude, and the day is a full one. Basic fitness and proper trekking footwear are enough; no climbing experience is needed. It is more demanding than the easy Gveleti or Juta walks but well within reach of anyone comfortable on a long flat hike.</p>
<h2>What to bring</h2>
<ul>
<li><strong>Passport.</strong> Mandatory — the checkpoint will not let you in without it.</li>
<li><strong>Trekking shoes.</strong> The valley floor is stony and can be wet near the springs.</li>
<li><strong>Jacket and rain layer.</strong> At 2,000 m it is cool and the weather changes fast.</li>
<li><strong>Water and a picnic.</strong> There are no shops or cafes in the valley.</li>
</ul>
<div style="margin:22px 0;padding:20px 22px;background:#F0F7F2;border-left:4px solid #1A3D2E;border-radius:8px">
<div style="font-family:'Lora',serif;font-size:18px;color:#1A3D2E;font-weight:600;margin-bottom:8px">Weather guarantee</div>
<p style="margin:0;color:#374151;line-height:1.65">Truso depends on the fords and the weather. Timur checks conditions the day before. If the valley is closed or unsafe on the day — high water, early snow — we <strong>reschedule for free</strong> or offer an equivalent nearby alternative (Gveleti, Gergeti), so your day is never wasted.</p>
</div>''',
 readalso='<div class="tour-readalso" style="margin:28px 0;padding:16px 20px;background:#f0f7f4;border-left:4px solid #2E7D32;border-radius:0 8px 8px 0;font-size:15px"><strong>Read also:</strong> <a href="/en/blog/kazbegi-complete-guide/">Kazbegi: the complete guide</a></div>',
 faqv='''<h3>How long is the Truso valley trek from Kazbegi?</h3>
<p>About 5–7 hours in total from Stepantsminda: a 4x4 drive to and into the valley, then a long, flat walk along the valley floor past the mineral springs to the Zakagori fortress and back. It is a half-day, not a full expedition.</p>
<h3>Do I really need a 4x4?</h3>
<p>Yes. There is no paved road into Truso — only a dirt track that crosses river fords and gets washed out after rain. An ordinary car cannot make it, so a proper 4x4 is mandatory. Timur uses a vehicle equipped for these crossings.</p>
<h3>How much does it cost and why per car?</h3>
<p>From ₾500 per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi/Stepantsminda, the 4x4 into the valley and back, and a Russian- or English-speaking guide. A 10% deposit confirms; the balance is cash GEL on the day.</p>
<h3>Do I need a passport — is it a border zone?</h3>
<p>Yes, a passport is mandatory: Truso is in the border zone and there is a document check at the valley entrance. No advance permit is needed and access is free. The Zakagori fortress is the furthest point you may reach; beyond it is closed.</p>
<h3>Is this the same as the Truso tour from Tbilisi?</h3>
<p>No — this trek starts in Kazbegi and is priced per car for people already in the mountains. If you are coming from the capital, see our full-day <a href="/en/ekskursiya/__TBILISI_TRUSO__/">Truso Gorge tour from Tbilisi</a> instead, which includes the Georgian Military Highway and is priced per person.</p>''',
 tip='<p>Truso is the wildest thing you can do in a single day out of Kazbegi, and the reason it stays wild is the fords: only a jeep gets in, so the crowds never do. Go on a clear day and start early — the light on the orange springs in the morning is unreal, and the afternoon weather at 2,000 m is unpredictable. Keep your passport in your pocket, not your bag: the checkpoint at the entrance checks everyone. The fortress at Zakagori is the turnaround point; climb the rise for the view back down the whole valley before we head out.</p>',
 why='<p>The Truso valley in one day from Kazbegi: orange travertine mineral springs, the lonely Zakagori fortress, medieval towers and a wild border valley almost no one reaches. A 4x4 carries you in over the fords and you walk only the beautiful flat section on foot. The closest thing to genuine Caucasus wilderness within easy reach of Stepantsminda.</p>',
 incl='<ul><li>4x4 with driver from Kazbegi/Stepantsminda</li><li>Russian- or English-speaking guide</li><li>Jeep drive into the Truso valley and back</li><li>Travertine mineral springs and Zakagori fortress</li><li>Medieval towers and valley views</li></ul>',
 notincl='<ul style="color:#991B1B"><li>Food and picnic (bring your own)</li><li>Personal trekking shoes and clothing</li></ul>',
 pract='''<h2>Practical Information</h2>
<p>The trek starts right in Kazbegi: I pick you up from your accommodation in Stepantsminda or the nearby villages in a proper 4x4. Maximum 7 people per group — individual attention. We start in the morning to beat the afternoon weather. Languages: English, Russian, Georgian.</p>
<h3>Booking and Payment</h3>
<p>Message me on WhatsApp (+995 511 272 623) — I reply within 10–15 minutes, including at night. A 10% deposit confirms your booking; the balance is paid on the day. I accept cash GEL (₾), bank transfer, and cryptocurrency. Free cancellation up to 24 hours before. In high season (June–September) book 2–3 days ahead.</p>
<h3>A trek from Kazbegi, or a tour from Tbilisi?</h3>
<p>This trek is for travellers <strong>already in Kazbegi</strong>. If you are coming from the capital, see the full-day <a href="/en/ekskursiya/__TBILISI_TRUSO__/">Truso Gorge tour from Tbilisi</a> — the same valley with the Georgian Military Highway, priced per person.</p>''',
 faq_schema_old=E_FAQ_SCHEMA,
 faq_schema='{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long is the Truso valley trek from Kazbegi?","acceptedAnswer":{"@type":"Answer","text":"About 5-7 hours in total from Stepantsminda: a 4x4 drive into the valley, then a long flat walk along the valley floor past the mineral springs to the Zakagori fortress and back."}},{"@type":"Question","name":"Do I really need a 4x4 for Truso?","acceptedAnswer":{"@type":"Answer","text":"Yes. There is no paved road into Truso, only a dirt track that crosses river fords and gets washed out after rain. An ordinary car cannot make it, so a proper 4x4 is mandatory."}},{"@type":"Question","name":"How much does it cost and why per car?","acceptedAnswer":{"@type":"Answer","text":"From 500 GEL per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi, the 4x4 into the valley and back, and a Russian or English speaking guide."}},{"@type":"Question","name":"Do I need a passport for Truso?","acceptedAnswer":{"@type":"Answer","text":"Yes, a passport is mandatory: Truso is in the border zone and there is a document check at the valley entrance. No advance permit is needed and access is free. The Zakagori fortress is the furthest point you may reach."}},{"@type":"Question","name":"Is this the same as the Truso tour from Tbilisi?","acceptedAnswer":{"@type":"Answer","text":"No. This trek starts in Kazbegi and is priced per car for people already in the mountains. The tour from Tbilisi is a full day including the Georgian Military Highway, priced per person."}}]}',
)
html = build(T)
out = ROOT / "en/ekskursiya" / T["slug"] / "index.html"
out.write_text(html, encoding="utf-8")
words = len(_re.sub(r"<[^>]+>", " ", _re.sub(r"<(script|style).*?</\1>", "", html, flags=_re.S)).split())
print(f"Truso EN: {out}  ~{words} words")


# ===================== JUTA (EN, light day, per car, NOT border zone) =====================
J = dict(
 slug="hayking-juta-chaukhi-iz-kazbegi",
 price="500",
 title="Juta to Chaukhi Hike from Kazbegi — from ₾500",
 name="Juta to Chaukhi Hike from Kazbegi",
 desc="Juta to Chaukhi hike from Kazbegi — from ₾500 per car. An easy alpine day to the Chaukhi massif, the Georgian Dolomites. 5–6 hours, no border zone.",
 desc_ent="Juta to Chaukhi hike from Kazbegi — from &#8382;500 per car. An easy alpine day to the foot of the Chaukhi massif, the Georgian Dolomites. 5-6 hours, no border zone, up to 7 people.",
 wa="I+want+to+book+the+Juta+to+Chaukhi+hike+from+Kazbegi",
 herostats=('<div class="stat-item"><span class="stat-val">from ₾500</span><span class="stat-lab">per car</span></div>\n'
  '<div class="stat-item"><span class="stat-val">5–6 h</span><span class="stat-lab">duration</span></div>\n'
  '<div class="stat-item"><span class="stat-val">up to 7</span><span class="stat-lab">people</span></div>\n'
  '<div class="stat-item"><span class="stat-val">Kazbegi</span><span class="stat-lab">start</span></div>\n'
  '<div class="stat-item"><span class="stat-val">easy</span><span class="stat-lab">level</span></div>'),
 intro='<p>Juta is the alpine jewel 20 km east of Kazbegi, at the foot of the jagged Chaukhi massif — the peaks locals call the "Georgian Dolomites". This is the easy day version: a gentle walk over flowering alpine meadows from Juta village (~2,200 m) to the base camp beneath the rock towers of Chaukhi, with no pass and no technical ground. Perfect if you are already in Kazbegi and want postcard high-mountain scenery in a single relaxed day, without a punishing trek.</p>',
 keyfact='<strong>In short:</strong> The Juta to Chaukhi hike is an easy day from Stepantsminda (Kazbegi), from ₾500 per car (a group of up to 7 — the price is split across the group). We drive ~20 km to Juta village, then walk about 8 km round trip over alpine meadows to the base of the Chaukhi massif (~2,600 m), no pass involved. Not a border zone — no passport or permit needed. Season May–October. Russian- and English-speaking guide from Sakhva Travel, direct booking with no agency fees.',
 pricebox='''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
<div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">from 500 GEL <span style="font-size:14px;font-weight:400;color:#6B7280">per car</span></div>
<div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">Price per car — the more people, the cheaper per person</div>''',
 sectitle="Hike Schedule — Step by Step",
 route='''<div class="route-item">
<div class="route-time">09:30</div>
<div><div class="route-name">Meeting in Stepantsminda</div><div class="route-desc">Pickup from your accommodation in Kazbegi / Stepantsminda. Short briefing.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:00</div>
<div><div class="route-name">Drive to Juta</div><div class="route-desc">~20 km east. The last stretch is gravel — a higher-clearance car is better.</div></div>
</div>
<div class="route-item">
<div class="route-time">10:45</div>
<div><div class="route-name">Juta village (~2,200 m) — trailhead</div><div class="route-desc">One of the highest villages in Europe. We start walking from here.</div></div>
</div>
<div class="route-item">
<div class="route-time">11:30</div>
<div><div class="route-name">Alpine meadows</div><div class="route-desc">A gentle trail along the river, flowering meadows, the Chaukhi peaks ahead.</div></div>
</div>
<div class="route-item">
<div class="route-time">12:30</div>
<div><div class="route-name">Chaukhi base camp (~2,600 m)</div><div class="route-desc">The foot of the "Georgian Dolomites" — jagged rock towers right overhead.</div></div>
</div>
<div class="route-item">
<div class="route-time">13:00</div>
<div><div class="route-name">Picnic under the peaks</div><div class="route-desc">Rest and lunch with your own supplies at the base of the massif.</div></div>
</div>
<div class="route-item">
<div class="route-time">14:00</div>
<div><div class="route-name">Back to Juta</div><div class="route-desc">A gentle descent along the same meadow trail.</div></div>
</div>
<div class="route-item">
<div class="route-time">15:00</div>
<div><div class="route-name">Return to Stepantsminda</div><div class="route-desc">Drop-off at your accommodation. The rest of the day is yours.</div></div>
</div>''',
 mapstops='var stops=[{"name": "Stepantsminda", "lat": 42.6579, "lng": 44.6417}, {"name": "Juta village", "lat": 42.5497, "lng": 44.7194}, {"name": "Chaukhi base", "lat": 42.523, "lng": 44.743}];',
 mapcap='Route: Stepantsminda → Juta village → base of the Chaukhi massif',
 sec_a='''<h2>Juta and the Chaukhi massif — the "Georgian Dolomites"</h2>
<p>The Chaukhi massif is a row of sharp rock peaks rising to 3,842 m straight out of the green meadows above Juta. Their jagged silhouette earned them the nickname "Georgian Dolomites", and unlike the snowy dome of Kazbek these are dark, sheer towers that are genuinely dramatic up close. Our route reaches the base camp at their foot, where the peaks stand in full view.</p>
<p>Juta village itself (~2,200 m) is one of the highest continuously inhabited settlements in Europe — horses grazing, a handful of guesthouses, and flowering alpine meadows all around, at their brightest in June and July.</p>
<h2>An easy day, no pass</h2>
<p>We do the easy single-day version: Juta to the Chaukhi base and back, about 8 km, 3–4 hours of gentle walking on a mostly flat trail along the river. This does not include the Chaukhi pass (3,338 m) or the descent to the Abudelauri lakes — that is a hard multi-day trek and is not part of this route. Our goal is the alpine scenery and the foot of the massif, comfortably, in one day, with no overnight camping.</p>''',
 sec_b='''<h2>No passport, no permit needed</h2>
<p>Unlike <a href="/en/ekskursiya/hayking-truso-iz-kazbegi/">Truso</a> and <a href="/en/ekskursiya/hayking-gveleti-iz-kazbegi/">Gveleti</a>, Juta is <strong>not in the border zone</strong> — there are no checkpoints or document checks, and access is free and open. That makes it the simplest of the three to organise: you just arrive and start walking.</p>
<h2>When to go: season and weather</h2>
<p>The Juta season runs <strong>late May to October</strong>. The best time is June–July, when the meadows are in full flower, and September for clear autumn light. In winter the village is cut off by snow and the route is closed. At 2,200–2,600 m it is cool and changeable even in summer (10–16°C, windy, occasional rain) — bring a jacket and a rain layer. The Chaukhi peaks often cloud over by midday, so we set off early.</p>
<h2>Difficulty, children and fitness</h2>
<p>An easy day within reach of most people: the trail is gentle, the elevation gain moderate (~400 m over 4 km), with no steep climbs or exposed ground. Fine with children of school age. The only real factor is the altitude (2,200–2,600 m) — we go at a relaxed pace. Proper walking shoes are needed, as the trail is stony and muddy after rain.</p>
<h2>What to bring</h2>
<ul>
<li><strong>Walking shoes.</strong> The trail is stony and can be wet; the elevation gain is gentle but real.</li>
<li><strong>Jacket and rain layer.</strong> At altitude it is 10–16°C, windy, and the weather turns quickly.</li>
<li><strong>Water and a snack.</strong> Juta has guesthouses, but there are no cafes on the trail.</li>
<li><strong>Sun protection.</strong> High-altitude sun is strong: sunscreen and a hat even under cloud.</li>
</ul>
<div style="margin:22px 0;padding:20px 22px;background:#F0F7F2;border-left:4px solid #1A3D2E;border-radius:8px">
<div style="font-family:'Lora',serif;font-size:18px;color:#1A3D2E;font-weight:600;margin-bottom:8px">Weather guarantee</div>
<p style="margin:0;color:#374151;line-height:1.65">Juta is high country, and in bad weather (heavy rain, early snow) the trail and the gravel road to the village can be uncomfortable or impassable. Timur checks the forecast the day before. If it is unsafe on the day, we <strong>reschedule for free</strong> or offer an equivalent nearby alternative (Gveleti, Gergeti), so your day is never wasted.</p>
</div>''',
 readalso='<div class="tour-readalso" style="margin:28px 0;padding:16px 20px;background:#f0f7f4;border-left:4px solid #2E7D32;border-radius:0 8px 8px 0;font-size:15px"><strong>Read also:</strong> <a href="/en/blog/kazbegi-complete-guide/">Kazbegi: the complete guide</a></div>',
 faqv='''<h3>How long is the Juta to Chaukhi hike?</h3>
<p>An easy day, about 5–6 hours from Stepantsminda: ~20 km by car to Juta plus roughly 8 km round trip on foot to the base of the Chaukhi massif. Around 3–4 hours of gentle walking on a mostly flat trail.</p>
<h3>Is this the hard trek with the pass and the Abudelauri lakes?</h3>
<p>No. We do the <strong>easy single-day version</strong>, Juta to the Chaukhi base and back, without the Chaukhi pass (3,338 m) or the Abudelauri lakes — that is a separate hard multi-day route. Our goal is alpine scenery in one comfortable day.</p>
<h3>How much does it cost and why per car?</h3>
<p>From ₾500 per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi/Stepantsminda, the drive to Juta and back, and a Russian- or English-speaking guide. A 10% deposit confirms; the balance is cash GEL on the day.</p>
<h3>Do I need a passport or permit?</h3>
<p>No. Juta is not a border zone — there are no checkpoints or checks and access is free. You do not need to carry your passport.</p>
<h3>Is it suitable for children and people with no experience?</h3>
<p>Yes. The trail is gentle with moderate elevation gain and no exposed ground, so it suits children of school age and anyone without hiking experience. The only factor is the altitude — we go at a relaxed pace.</p>''',
 tip='<p>Juta is the one I recommend for people who want "real mountains" without suffering for them. The trick is to start early: by midday the Chaukhi peaks are almost always wrapped in cloud, but at first light they stand sharp and dark over the green meadows. We walk only to the base camp and back — that is enough for the best views, and the hard pass and lakes we leave to those ready for two nights in a tent. Bring a jacket and rain layer whatever the valley looks like: at 2,500 m the weather flips in half an hour.</p>',
 why="<p>Juta is the most alpine of the easy hikes near Kazbegi: the jagged Chaukhi peaks, flowering meadows and one of Europe's highest villages, all in one relaxed day. A great choice once you have seen Kazbek and Gergeti and want genuine high mountains without the time or effort of a multi-day trek.</p>",
 incl='<ul><li>Car with driver from Kazbegi/Stepantsminda</li><li>Russian- or English-speaking guide</li><li>Drive to Juta and back</li><li>Walk to the base of the Chaukhi massif</li><li>Alpine meadows and views of the "Georgian Dolomites"</li></ul>',
 notincl='<ul style="color:#991B1B"><li>Food and snacks (bring your own)</li><li>Personal hiking shoes and clothing</li></ul>',
 pract='''<h2>Practical Information</h2>
<p>The Juta hike starts right in Kazbegi: I pick you up in Stepantsminda and we drive about 20 km east to Juta village, the final stretch on gravel where a higher-clearance car helps. Maximum 7 people per group — individual attention. We set off in the morning, before the Chaukhi peaks cloud over. Languages: English, Russian, Georgian.</p>
<h3>Booking and Payment</h3>
<p>Message me on WhatsApp (+995 511 272 623) — I reply within 10–15 minutes, including at night. A 10% deposit confirms your booking; the balance is paid on the day. I accept cash GEL (₾), bank transfer, and cryptocurrency. Free cancellation up to 24 hours before. In high season (June–September) book 2–3 days ahead.</p>
<h3>A hike from Kazbegi, or a tour from Tbilisi?</h3>
<p>This walk is for travellers <strong>already in Kazbegi</strong>. If you are coming from the capital, see the <a href="/en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/">Kazbegi tour from Tbilisi</a> — Gergeti, Ananuri and the Georgian Military Highway in one day.</p>''',
 faq_schema_old=E_FAQ_SCHEMA,
 faq_schema='{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long is the Juta to Chaukhi hike?","acceptedAnswer":{"@type":"Answer","text":"An easy day, about 5-6 hours from Stepantsminda: around 20 km by car to Juta plus roughly 8 km round trip on foot to the base of the Chaukhi massif. Around 3-4 hours of gentle walking."}},{"@type":"Question","name":"Is this the hard trek with the pass and the Abudelauri lakes?","acceptedAnswer":{"@type":"Answer","text":"No. We do the easy single-day version, Juta to the Chaukhi base and back, without the Chaukhi pass (3338 m) or the Abudelauri lakes, which is a separate hard multi-day route. Our goal is alpine scenery in one comfortable day."}},{"@type":"Question","name":"How much does it cost and why per car?","acceptedAnswer":{"@type":"Answer","text":"From 500 GEL per car, not per person. A group of up to 7 splits the price, so the more people come, the cheaper it is each. The price includes pickup around Kazbegi, the drive to Juta and back, and a Russian or English speaking guide."}},{"@type":"Question","name":"Do I need a passport or permit for Juta?","acceptedAnswer":{"@type":"Answer","text":"No. Juta is not a border zone, there are no checkpoints or checks and access is free. You do not need to carry your passport."}},{"@type":"Question","name":"Is it suitable for children and people with no experience?","acceptedAnswer":{"@type":"Answer","text":"Yes. The trail is gentle with moderate elevation gain and no exposed ground, so it suits children of school age and anyone without hiking experience. The only factor is the altitude."}}]}',
)
html = build(J)
out = ROOT / "en/ekskursiya" / J["slug"] / "index.html"
out.write_text(html, encoding="utf-8")
words = len(_re.sub(r"<[^>]+>", " ", _re.sub(r"<(script|style).*?</\1>", "", html, flags=_re.S)).split())
print(f"Juta EN: {out}  ~{words} words")
