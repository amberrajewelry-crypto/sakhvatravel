#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN гео-лендинги "Tours to Georgia from {City}" из донора en/tours-from-samara.
Уникальные зоны (lead, know, flights, tip, FAQ, meta) — честные авиаданные,
параллели рек/культуры как в RU. Practical-карточки универсальны, не трогаем."""
import sys, re
from pathlib import Path

ROOT = Path("/Users/vladimir/sakhva-travel")
DONOR = (ROOT / "en/tours-from-samara/index.html").read_text(encoding="utf-8")

def R(html, old, new, required=True):
    if old not in html:
        if required:
            raise SystemExit(f"[EN ANCHOR NOT FOUND]\n{old[:110]}")
        return html
    return html.replace(old, new, 1)

C = {
 "ufa": {
  "ru":"ufy","Name":"Ufa",
  "title":"Tours to Georgia from Ufa 2026 — Direct Flight &amp; Private Tours",
  "desc":"Tours to Georgia from Ufa: direct Azimuth flight in 2.5 hours from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Direct Ufa–Tbilisi flight in 2.5 hours from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "h1":"Tours to Georgia from Ufa 2026 — flights, budget and routes",
  "lead":"Direct Azimuth flight in just 2.5 hours, accommodation from ₾50/night, private tours from ₾98. Georgia is a surprisingly close and affordable destination from Ufa.",
  "s1n":"2.5h","s1l":"Direct flight","s3n":"from 14.5K","s3l":"Flight, RUB",
  "leadtext":("Ufa sits on the high bank of the Agidel — the Belaya River — among the honey forests of Bashkiria and the first foothills of the Urals. "
   "Georgia is closer than it seems: a direct Azimuth flight gets you to Tbilisi in 2 hours 30 minutes, with no layovers or overnight stops in Moscow. "
   "And the welcome feels both familiar and new. Familiar, because here — as back home — a mosque, a synagogue and a church have stood side by side for centuries: old Tbilisi breathes the same spirit of good-neighbourliness. "
   "New, because instead of linden honey and kumis you'll find kvevri wine from clay vessels buried in the ground 8,000 years ago, and instead of gentle Ural ridges — the sharp five-thousanders of the Caucasus. "
   "The time difference is just one hour: home is UTC+5, Tbilisi is UTC+4."),
  "fsub":"Direct Azimuth flight Ufa–Tbilisi — 2.5 hours, no layovers. Plus connections via Moscow and Istanbul. Real prices for 2026.",
  "rows":("<tr><td>Ufa → Tbilisi (direct)</td><td>Azimuth</td><td>~2h 30m</td><td class=\"highlight\">from 22,000 RUB</td></tr>\n"
   "<tr><td>Ufa → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~7–9h</td><td class=\"highlight\">from 19,000 RUB</td></tr>\n"
   "<tr><td>Ufa → Istanbul → Tbilisi</td><td>Turkish / Pegasus</td><td>~8–10h</td><td class=\"highlight\">from 24,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> the direct Azimuth flight is the easiest option — only 2.5 hours in the air. The carrier accepts Mir, Visa and Mastercard. On sales, one-way tickets have dropped to 4,500 RUB — book 5–7 weeks ahead.",
  "ktitle":"What Ufa Travellers Should Know",
  "know":[("Direct Flight in 2.5 Hours","Azimuth flies Ufa–Tbilisi non-stop in 2 hours 30 minutes and accepts Mir cards. No layovers, no overnight stops in Moscow — you land and start your trip right away."),
   ("Bashkir Honey and Georgian Wine","Bashkiria is famous for linden honey, kumis and herbal teas. Georgia answers with kvevri wine from clay vessels buried underground — a craft older than the pyramids. Not a rivalry, but a pairing of flavours."),
   ("Two Cities of Coexistence","In Ufa a mosque and Orthodox churches stand together. In old Tbilisi a mosque, a synagogue and a church sit within a five-minute walk. Both cities know the culture of different peoples living side by side."),
   ("Almost the Same Time Zone","Ufa is UTC+5, Tbilisi is UTC+4 — just one hour apart. Set your watch back an hour and you're in sync, with barely any jet lag.")],
  "budget":"Ufa travellers win on the direct flight: 2.5 hours in the air versus 7–9 with a Moscow layover. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Ufa?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Ufa%20and%20want%20to%20book%20tours",
  "tip":"From Ufa I always recommend the direct Azimuth flight — 2.5 hours and you're in Tbilisi, no exhausting layovers. Only one hour of time difference. In my experience, those used to Bashkir honey and herbal tea love Kakheti — kvevri wine tasting in a real marani. And after the soft Urals, Kazbegi feels like mountains of a completely different scale. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Ufa in 2026?","The easiest option is the direct Azimuth flight Ufa–Tbilisi — 2 hours 30 minutes, from 22,000 RUB round-trip. Connections also exist via Moscow (7–9h, from 19,000 RUB) or Istanbul. Azimuth accepts Mir, Visa and Mastercard."),
   ("Are there direct flights Ufa–Tbilisi?","Yes. Azimuth operates direct Ufa–Tbilisi flights, 2 hours 30 minutes each way. Red Wings and Georgian Airways are also cleared for Russia–Georgia routes. Book on the carrier's site; payment by Mir, Visa and Mastercard."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Ufa cost?","A self-planned 7-day trip costs from 40,000 RUB: direct flight ~22,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth sells Ufa–Tbilisi tickets for Mir on its website. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Ufa banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Ufa?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti, with a chance to join the rtveli. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October."),
   ("Which tours are must-do for visitors from Ufa?","Three picks: Kakheti — wine country where a lover of Bashkir honey and teas will appreciate kvevri wine (from ₾170); Kazbegi — sharp Caucasus peaks after the soft Urals (from ₾175); Mtskheta — 2,000 years of Christian history and UNESCO sites (from ₾98). Plus Old Tbilisi on foot (from ₾100)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },
 "nizhny-novgorod": {
  "ru":"nizhnego-novgoroda","Name":"Nizhny Novgorod",
  "title":"Tours to Georgia from Nizhny Novgorod 2026 — Direct Flight",
  "desc":"Tours to Georgia from Nizhny Novgorod: direct Red Wings flight in 3.5 hours from 13,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Direct Nizhny Novgorod–Tbilisi flight in 3.5 hours from 13,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "h1":"Tours to Georgia from Nizhny Novgorod 2026 — flights, budget and routes",
  "lead":"Direct Red Wings flight in 3.5 hours, accommodation from ₾50/night, private tours from ₾98. Georgia is a surprisingly easy destination from Nizhny Novgorod.",
  "s1n":"3.5h","s1l":"Direct flight","s3n":"from 13K","s3l":"Flight, RUB",
  "leadtext":("Nizhny Novgorod stands where the Oka meets the Volga — a merchant capital of fairs and kremlin walls above the great river. "
   "Now there's a direct road to Tbilisi: the Red Wings flight from Strigino airport, resumed in June 2026, gets you there in 3 hours 30 minutes. "
   "And Georgia offers an unexpected sense of recognition. The Nizhny Strelka, where the Oka flows into the Volga, echoes in Georgian Mtskheta, where the Aragvi and Mtkvari meet — the very waters sung by Lermontov. "
   "Instead of the flat Volga plain, sharp Caucasus five-thousanders begin; instead of fair rows, the colourful bazaars of Tbilisi, where people haggle, joke and treat you just the same. "
   "The time difference is just one hour: home is UTC+3, Tbilisi is UTC+4."),
  "fsub":"Direct Red Wings flight Nizhny Novgorod–Tbilisi resumed in June 2026 — 3.5 hours, no layovers. Plus connections via Moscow and Istanbul. Real prices for 2026.",
  "rows":("<tr><td>Nizhny Novgorod → Tbilisi (direct)</td><td>Red Wings</td><td>~3h 30m</td><td class=\"highlight\">from 24,000 RUB</td></tr>\n"
   "<tr><td>Nizhny Novgorod → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~6–8h</td><td class=\"highlight\">from 18,000 RUB</td></tr>\n"
   "<tr><td>Nizhny Novgorod → Istanbul → Tbilisi</td><td>Turkish / Pegasus</td><td>~8–10h</td><td class=\"highlight\">from 23,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> the direct Red Wings flight from Strigino airport resumed on 13 June 2026 — morning departure at 9:30, only 3.5 hours. It runs on Saturdays; grab tickets 5–7 weeks ahead.",
  "ktitle":"What Nizhny Novgorod Travellers Should Know",
  "know":[("Direct Flight Resumed in 2026","Red Wings flies Nizhny Novgorod–Tbilisi non-stop from Strigino airport — resumed 13 June 2026, Saturdays at 9:30, about 3.5 hours. Direct flights to Batumi are also available."),
   ("Two Confluences: Oka–Volga and Aragvi–Mtkvari","The Nizhny Strelka, where the Oka joins the Volga, is the city's symbol. Georgia has its own famous confluence — in Mtskheta the Aragvi and Mtkvari meet by Jvari Monastery. A familiar feeling of great waters merging."),
   ("Merchant Fair and Tbilisi Bazaar","Nizhny was a trading capital for centuries — the Makaryev Fair was famous nationwide. The Tbilisi bazaars, Dezerter Market and the Dry Bridge, share the same living stir of trade, spices and character."),
   ("Almost the Same Time Zone","Nizhny Novgorod is UTC+3, Tbilisi is UTC+4 — one hour apart. Set your watch forward an hour and you're in the local rhythm, with barely any jet lag.")],
  "budget":"Nizhny travellers win on the direct Red Wings flight: 3.5 hours instead of 6–8 with a Moscow layover. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Nizhny Novgorod?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Nizhny%20Novgorod%20and%20want%20to%20book%20tours",
  "tip":"From Nizhny I recommend the direct Red Wings flight from Strigino: 3.5 hours and you're in Tbilisi, no layovers in Moscow. Only one hour of time difference. Definitely visit Mtskheta — you'll recognise your own Strelka feeling, only where the Aragvi and Mtkvari meet. And after the flat Volga, Kazbegi feels like mountains of a whole new scale. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Nizhny Novgorod in 2026?","The easiest option is the direct Red Wings flight from Strigino airport, resumed in June 2026: 3 hours 30 minutes, from 24,000 RUB round-trip. Connections also exist via Moscow (6–8h, from 18,000 RUB) or Istanbul. Payment by Mir, Visa and Mastercard."),
   ("Are there direct flights Nizhny Novgorod–Tbilisi?","Yes. Red Wings operates a direct Nizhny Novgorod–Tbilisi flight from Strigino airport — resumed 13 June 2026, Saturdays at 9:30, about 3.5 hours. Direct flights to Batumi run too. Book on the carrier's site; payment by Mir, Visa and Mastercard."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Nizhny Novgorod cost?","A self-planned 7-day trip costs from 42,000 RUB: direct flight ~24,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Red Wings and Aeroflot sell tickets for Mir. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Nizhny banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Nizhny Novgorod?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October."),
   ("Which tours are must-do for visitors from Nizhny Novgorod?","Three picks: Mtskheta — the ancient capital at the Aragvi–Mtkvari confluence, a familiar Strelka and UNESCO sites (from ₾98); Kazbegi — sharp Caucasus peaks after the Volga plain (from ₾175); Kakheti — wine country with kvevri tasting (from ₾170). Plus Old Tbilisi on foot (from ₾100)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },
 "mineralnye-vody": {
  "ru":"mineralnyh-vod","Name":"Mineralnye Vody",
  "title":"Tours to Georgia from Mineralnye Vody 2026 — Direct Flight",
  "desc":"Tours to Georgia from Mineralnye Vody: direct Azimuth flight in 1h 20m from 4,900 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Direct Mineralnye Vody–Tbilisi flight in 1h 20m from 4,900 RUB, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "h1":"Tours to Georgia from Mineralnye Vody 2026 — flights, budget and routes",
  "lead":"Direct Azimuth flight in just 1h 20m, accommodation from ₾50/night, private tours from ₾98. Georgia is the closest getaway from Mineralnye Vody and the Caucasus spa region.",
  "s1n":"1h20","s1l":"Direct flight","s3n":"from 4.9K","s3l":"Flight, RUB",
  "leadtext":("Mineralnye Vody is the gateway to the Caucasus Mineral Waters — the land of narzan, Mount Beshtau and spa pump rooms. "
   "Tbilisi is a stone's throw away: a direct Azimuth flight covers it in just 1 hour 20 minutes — the shortest hop to Georgia from southern Russia. "
   "And the welcome feels almost domestic. To the home of narzan, Georgia answers with Borjomi mineral water from a volcanic gorge and the sulfur baths in the heart of Tbilisi — the same culture of healing water. "
   "The mountains are familiar too: beyond the ridge seen from Mount Mashuk begins the southern Caucasus — Kazbek, the Georgian Military Highway, the Gergeti Trinity. "
   "The time difference is just one hour: home is UTC+3, Tbilisi is UTC+4."),
  "fsub":"Direct Azimuth flight Mineralnye Vody–Tbilisi — just 1 hour 20 minutes, the shortest hop to Georgia from southern Russia. Real prices for 2026.",
  "rows":("<tr><td>Min. Vody → Tbilisi (direct)</td><td>Azimuth</td><td>~1h 20m</td><td class=\"highlight\">from 9,000 RUB</td></tr>\n"
   "<tr><td>Min. Vody → Vladikavkaz → Verkhny Lars</td><td>car / transfer</td><td>~5–6h</td><td class=\"highlight\">from 4,000 RUB</td></tr>\n"
   "<tr><td>Min. Vody → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~7–9h</td><td class=\"highlight\">from 17,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> the direct Azimuth flight is just 1h 20m and runs Mon, Wed, Thu, Sat and Sun. The carrier accepts Mir, Visa and Mastercard. On sales, one-way tickets have dropped to 4,878 RUB.",
  "ktitle":"What Mineralnye Vody Travellers Should Know",
  "know":[("The Caucasus Is Already Home","Mineralnye Vody is the heart of the Caucasus — just 1 hour 20 minutes to Tbilisi by direct Azimuth flight. One climate zone, familiar mountains, one hour of time difference. Almost no route to Georgia is shorter."),
   ("Narzan of the KMV and Georgian Borjomi","The Caucasus Mineral Waters are the home of narzan and healing springs. Georgia answers with Borjomi mineral water from a volcanic gorge and the sulfur baths in central Tbilisi. A spa visitor understands this culture of water instantly."),
   ("One Range, Different Peaks","Pyatigorye, Beshtau and Mashuk are familiar to every local. Beyond the ridge begins the Georgian Caucasus: Kazbek, the Military Highway, the Gergeti Trinity above the clouds. The same massif — but its southern, brighter side."),
   ("Almost the Same Time Zone","Mineralnye Vody is UTC+3, Tbilisi is UTC+4 — one hour apart. With a 1h 20m flight there's virtually no acclimatisation: you land and start walking.")],
  "budget":"KMV travellers win twice over: a direct flight of just 1h 20m from 9,000 RUB round-trip, or the scenic overland route via Vladikavkaz and Verkhny Lars. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Mineralnye Vody?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Mineralnye%20Vody%20and%20want%20to%20book%20tours",
  "tip":"KMV travellers are lucky: the direct Azimuth flight reaches Tbilisi in 1 hour 20 minutes. For lovers of pump rooms and narzan, I always recommend Borjomi — Georgia's own culture of healing water, a volcanic gorge and a famous national park. For a touch of road romance, take the overland route via Verkhny Lars — the Georgian Military Highway is worth it. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Mineralnye Vody in 2026?","The fastest option is the direct Azimuth flight Mineralnye Vody–Tbilisi — just 1 hour 20 minutes, from 9,000 RUB round-trip. For road lovers, the overland route via Vladikavkaz and Verkhny Lars (5–6h). A Moscow connection also exists. Azimuth accepts Mir, Visa and Mastercard."),
   ("Are there direct flights Mineralnye Vody–Tbilisi?","Yes. Azimuth operates direct Mineralnye Vody–Tbilisi flights, 1 hour 20 minutes each way — the shortest hop to Georgia from southern Russia. It runs Mon, Wed, Thu, Sat and Sun. Payment by Mir, Visa and Mastercard."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Mineralnye Vody cost?","A self-planned 7-day trip costs from 34,000 RUB: direct flight ~9,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. The short, cheap flight makes a KMV trip one of the best-value in Russia. A package tour costs 65,000–95,000 RUB."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth sells Mineralnye Vody–Tbilisi tickets for Mir online. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat local banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Mineralnye Vody?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October."),
   ("Which tours are must-do for visitors from Mineralnye Vody?","Three picks: Borjomi — Georgia's home of mineral water, a volcanic gorge and national park, close to KMV visitors' hearts (from ₾178); Kazbegi — the southern side of the familiar Caucasus (from ₾175); Kakheti — wine country with kvevri tasting (from ₾170). Plus Old Tbilisi with sulfur baths (from ₾100)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },
 "volgograd": {
  "ru":"volgograda","Name":"Volgograd",
  "title":"Tours to Georgia from Volgograd 2026 — Flights, Prices &amp; Tours",
  "desc":"Tours to Georgia from Volgograd: flights from 14,000 RUB (seasonal direct plus Moscow connections), guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Volgograd–Tbilisi flights from 14,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "h1":"Tours to Georgia from Volgograd 2026 — flights, budget and routes",
  "lead":"Flights from 14,000 RUB, accommodation from ₾50/night, private tours from ₾98. Georgia is a surprisingly affordable destination from Volgograd.",
  "s1n":"3–4h","s1l":"Travel time","s3n":"from 14K","s3l":"Flight, RUB",
  "leadtext":("Volgograd stretches along the Volga for almost 90 kilometres — a river-city of great memory, watched over from every direction by The Motherland Calls. "
   "Reaching Tbilisi takes different routes: in summer seasonal direct flights appear (about 2h 40m), and year-round a convenient Moscow connection does the job. "
   "Georgia echoes for a Volga native with a familiar sense of great water: Tbilisi stands on the Mtkvari, with its own embankment and bridges. "
   "And the memory set in stone on Mamayev Kurgan finds its Georgian echo in the Narikala fortress above the city, in Ananuri Castle and the Gergeti Trinity above the clouds. "
   "The time difference is just one hour: home is UTC+3, Tbilisi is UTC+4."),
  "fsub":"Direct Volgograd–Tbilisi flights run seasonally (in summer); the reliable year-round option is a Moscow connection. Real prices for 2026.",
  "rows":("<tr><td>Volgograd → Tbilisi (direct, seasonal)</td><td>Azimuth / Red Wings</td><td>~2h 40m</td><td class=\"highlight\">from 16,000 RUB</td></tr>\n"
   "<tr><td>Volgograd → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~6–8h</td><td class=\"highlight\">from 14,000 RUB</td></tr>\n"
   "<tr><td>Volgograd → Istanbul → Tbilisi</td><td>Turkish / Pegasus</td><td>~8–10h</td><td class=\"highlight\">from 22,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> direct flights to Tbilisi appear in high season (summer), but the schedule is unstable — check Yandex Travel. Year-round, a Moscow connection from 14,000 RUB does the job. Azimuth and Aeroflot accept Mir.",
  "ktitle":"What Volgograd Travellers Should Know",
  "know":[("One Hour of Time Difference","Volgograd is UTC+3, Tbilisi is UTC+4 — one hour ahead. A small shift, easily handled: set your watch and skip the long acclimatisation. A short break isn't wasted."),
   ("Volga and Mtkvari: Rivers of Two Cities","Volgograd runs along the Volga for tens of kilometres — a city fused with its river. Tbilisi stands on the Mtkvari, with embankments and bridges. A Volga native knows this feeling of a city grown along great water."),
   ("Memory in Stone: Mamayev Kurgan and Georgian Fortresses","Volgograd is a city of great wartime memory, The Motherland Calls visible from everywhere. Georgia keeps its history in stone differently: Narikala above Tbilisi, Ananuri Castle, the Gergeti Trinity. Different eras, one respect for the past."),
   ("Affordable Alternative to Europe","Georgia offers European-level sights and cuisine at 30–40% lower prices. A 7-day trip from Volgograd is genuinely affordable — and richer than a package.")],
  "budget":"Volgograd travellers should catch seasonal direct flights in summer — faster and often cheaper. Otherwise a Moscow connection from 14,000 RUB does the job. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Volgograd?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Volgograd%20and%20want%20to%20book%20tours",
  "tip":"In summer I'd catch the seasonal direct flights from Volgograd — that's fastest. Off-season, flying via Moscow is more reliable. Volga natives especially love evening Tbilisi on the Mtkvari — its own embankment and bridges, but the lights and sulfur baths make the night feel different. And after the flat Volga, the Kazbegi mountains reveal the Caucasus from an unexpected angle. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Volgograd in 2026?","In summer, seasonal direct flights appear (about 2h 40m, from 16,000 RUB). Year-round, a Moscow connection is more reliable — 6–8 hours, from 14,000 RUB, or via Istanbul. The direct schedule is unstable, so check Yandex Travel. Payment by Mir, Visa and Mastercard."),
   ("Are there direct flights Volgograd–Tbilisi?","Direct Volgograd–Tbilisi flights run seasonally, in the high summer season — operated by Azimuth and Red Wings, about 2h 40m. In winter the schedule is unstable and a Moscow connection is safer. Check current availability before buying."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Volgograd cost?","A self-planned 7-day trip costs from 36,000 RUB: flight ~14,000–16,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth and Aeroflot sell tickets for Mir. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Volgograd banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Volgograd?","Best by weather: spring (April–May) and autumn (September–October). Summer more often has seasonal direct flights but is hot (+35–38°C). September–October is wine harvest season in Kakheti. Kazbegi routes run May–October."),
   ("Which tours are must-do for visitors from Volgograd?","Three picks: Night Tbilisi on the Mtkvari — a Volga native knows the feeling of a city by great water (from ₾100); Kazbegi — the Caucasus after the flat Volga (from ₾175); Kakheti — wine country with kvevri tasting (from ₾170). Plus Mtskheta with UNESCO sites (from ₾98)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },
 "saratov": {
  "ru":"saratova","Name":"Saratov",
  "title":"Tours to Georgia from Saratov 2026 — Flights, Prices &amp; Tours",
  "desc":"Tours to Georgia from Saratov: flights from 11,000 RUB via Moscow, guided tours from ₾98. Same time zone as Tbilisi — no jet lag. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Saratov–Tbilisi flights from 11,000 RUB via Moscow, guided tours from ₾98. Same time zone — no jet lag.",
  "h1":"Tours to Georgia from Saratov 2026 — flights, budget and routes",
  "lead":"Flights from 11,000 RUB, accommodation from ₾50/night, private tours from ₾98. Same time zone as Tbilisi — zero jet lag. Itineraries for 5, 7 and 10 days.",
  "s1n":"0h","s1l":"Jet lag","s3n":"from 11K","s3l":"Flight, RUB",
  "leadtext":("Saratov spreads along the right bank of the Volga, linked to Engels by a legendary bridge, and its sky is written into history: it was on Saratov soil that Gagarin landed, and the airport bears his name. "
   "There are no direct flights to Tbilisi yet — the most convenient way is via Moscow, a 6–8 hour connection. "
   "But Saratov holds a rare trump card: the city runs on UTC+4, exactly like Tbilisi — you arrive and never touch your watch, with zero jet lag. "
   "Georgia echoes for a Volga native with a familiar sense of great water: Tbilisi stands on the Mtkvari, with its own embankments and bridges. "
   "And the pull toward height — from Gagarin's cosmos to the peaks — continues in the Georgian mountains: Kazbek at 5,033 metres, the Military Highway, the Gergeti Trinity above the clouds."),
  "fsub":"There are no direct Saratov–Tbilisi flights — the most convenient way is via Moscow (1–2 hour connection). Real prices and routes for 2026.",
  "rows":("<tr><td>Saratov → Moscow → Tbilisi</td><td>Aeroflot / Pobeda</td><td>~6–8h</td><td class=\"highlight\">from 11,000 RUB</td></tr>\n"
   "<tr><td>Saratov → Min. Vody → Verkhny Lars</td><td>flight + transfer</td><td>~7–8h</td><td class=\"highlight\">from 9,000 RUB</td></tr>\n"
   "<tr><td>Saratov → Istanbul → Tbilisi</td><td>Turkish / Pegasus</td><td>~8–10h</td><td class=\"highlight\">from 20,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> there are no direct flights to Tbilisi from Gagarin airport, but a Moscow connection takes 6–8 hours and costs from 11,000 RUB. Bonus — Saratov and Tbilisi share the UTC+4 time zone, so there's no jet lag at all.",
  "ktitle":"What Saratov Travellers Should Know",
  "know":[("Same Time Zone — Zero Jet Lag","Saratov moved to UTC+4 and now matches Tbilisi exactly. You arrive and never touch your watch — your body clock stays intact from minute one. For a short break that's a real plus: no day lost to adjustment."),
   ("Volga and Mtkvari: Cities on Great Water","Saratov stands on the right bank of the Volga, linked to Engels by a legendary bridge. Tbilisi grew on the Mtkvari. A Volga native knows this feeling of a city by a wide river — embankments, bridges and a life turned to the water."),
   ("From Gagarin to Georgian Heights","It was on Saratov soil that the first cosmonaut landed, and the airport bears Gagarin's name. Georgia offers heights of its own — not cosmic but alpine: Kazbek 5,033 m, the Gergeti Trinity, the Military Highway. A shared pull toward height."),
   ("No Package Lock-in","A self-planned trip with a private tour costs 25–35% less than a package from an agency — and delivers far richer experiences, with your own choice of stay and route.")],
  "budget":"Saratov travellers find it easiest to fly via Moscow — a 6–8 hour connection from 11,000 RUB. A nice bonus: the same time zone as Tbilisi, so no jet lag and no first day lost to adjustment. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Saratov?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Saratov%20and%20want%20to%20book%20tours",
  "tip":"From Saratov I'd not chase direct flights that don't exist — just fly calmly via Moscow, a 1–2 hour connection. Your rare trump card: the same time zone as Tbilisi, zero jet lag, no lost first day. Volga natives love evening Tbilisi on the Mtkvari and, of course, Kazbegi — after the flat Volga the mountains impress twice as much. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Saratov in 2026?","There are no direct Saratov–Tbilisi flights. The most convenient way is via Moscow: a 6–8 hour connection from 11,000 RUB. Routes via Istanbul or via Mineralnye Vody with an overland transfer also exist. Bonus — the same time zone as Tbilisi, no jet lag. Payment by Mir, Visa and Mastercard."),
   ("Are there direct flights Saratov–Tbilisi?","No, there are no direct Saratov–Tbilisi flights. The most convenient option is a Moscow connection (6–8h, from 11,000 RUB), less often via Istanbul. As an alternative, fly to Mineralnye Vody and take the overland route via Verkhny Lars. Bonus: Saratov shares Tbilisi's time zone (UTC+4)."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Saratov cost?","A self-planned 7-day trip costs from 33,000 RUB: flight via Moscow ~11,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. Bonus: the same time zone as Tbilisi — no jet lag, no lost first day. A package tour costs 65,000–95,000 RUB."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Moscow-route tickets can be paid with Mir on Aeroflot and Pobeda sites. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Saratov banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Saratov?","Any season works — the shared time zone removes jet lag. Best by weather: spring (April–May) and autumn (September–October). September–October is wine harvest season in Kakheti. Summer is hot (+35–38°C); Kazbegi runs May–October."),
   ("Which tours are must-do for visitors from Saratov?","Three picks: Kazbegi — the Caucasus after the flat Volga, the Gergeti Trinity below a 5,033 m peak (from ₾175); Night Tbilisi on the Mtkvari — a Volga native knows the feeling of a city by great water (from ₾100); Kakheti — wine country with kvevri tasting (from ₾170). Plus Mtskheta with UNESCO sites (from ₾98)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },

 "makhachkala": {
  "ru":"mahachkaly","Name":"Makhachkala",
  "title":"Tours to Georgia from Makhachkala 2026 — Routes &amp; Prices",
  "desc":"Tours to Georgia from Makhachkala: via Mineralnye Vody and Moscow from 12,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Makhachkala–Tbilisi route via Mineralnye Vody from 12,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "h1":"Tours to Georgia from Makhachkala 2026 — travel, budget and routes",
  "lead":"Via Mineralnye Vody or Moscow, accommodation from ₾50/night, private tours from ₾98. As Caucasus neighbours, Dagestan and Georgia are closer than you think.",
  "s1n":"~6h","s1l":"Via Min. Vody","s3n":"from 12K","s3l":"Travel, RUB",
  "leadtext":("Makhachkala lies on the shore of the Caspian, wedged between the sea and the foothills of the Dagestani mountains — a sunny, many-tongued city where a dozen highland languages meet on a single street. "
   "By Caucasus standards Tbilisi is next door: the same range, the same peaks above the clouds. The easiest way is via Mineralnye Vody, where Azimuth flies to Tbilisi in just 1 hour 20 minutes, or via Moscow. "
   "And Georgia welcomes a Dagestani almost as kin. The culture of the feast, where a tamada leads the table and holds the word, is shared: a Dagestani toast and a Georgian toast speak the same language of respect. "
   "Dagestani khinkal and Georgian khinkali are dishes related even by name. And ancient Derbent with its Naryn-Kala fortress echoes in Tbilisi's Narikala above the Mtkvari — two highland strongholds that have watched over two millennia. "
   "The time difference is just one hour: home is UTC+3, Tbilisi is UTC+4."),
  "fsub":"A direct Makhachkala–Tbilisi flight is unstable, so it's more reliable to fly via Mineralnye Vody (a short Azimuth direct) or via Moscow. Real prices for 2026.",
  "rows":("<tr><td>Makhachkala → Min. Vody → Tbilisi</td><td>Azimuth</td><td>~5–6h</td><td class=\"highlight\">from 12,000 RUB</td></tr>\n"
   "<tr><td>Makhachkala → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~7–9h</td><td class=\"highlight\">from 16,000 RUB</td></tr>\n"
   "<tr><td>Makhachkala → Vladikavkaz → Verkhny Lars</td><td>overland transfer</td><td>~8–10h</td><td class=\"highlight\">from 9,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> the fastest air route is via Mineralnye Vody — a flight to MRV, then Azimuth to Tbilisi in just 1 hour 20 minutes. Road lovers can take the overland route via Vladikavkaz and the Verkhny Lars border along the Georgian Military Highway — scenic, if longer.",
  "ktitle":"What Makhachkala Travellers Should Know",
  "know":[("Just One Hour Apart","Makhachkala is UTC+3, Tbilisi is UTC+4 — one hour apart. As Caucasus neighbours, Dagestan and Georgia share a climate and a rhythm, so there's barely any adjustment: your first holiday day isn't lost to jet lag."),
   ("One Table, One Tamada","In Dagestan and Georgia the feast is a ritual with its own master: for both, the tamada holds the word, leads the toasts, sets the tone. Dagestani khinkal and Georgian khinkali are relatives by name itself. At a Georgian table a Makhachkala native feels at home."),
   ("Two Highland Fortresses","Derbent's Naryn-Kala above the Caspian and Tbilisi's Narikala above the Mtkvari — two ancient strongholds of one Caucasus, each a millennium and a half old. Anyone raised near the Derbent walls instantly reads the language of old Tbilisi: stone, towers, history on every slope."),
   ("No Package Lock-in","A self-planned trip with a private tour costs 25–35% less than an agency package — and delivers far richer experiences, with your own choice of stay and route.")],
  "budget":"Makhachkala travellers benefit from the Mineralnye Vody route: the short Azimuth MRV–Tbilisi flight (1h20) plus a hop to Min. Vody costs less than a long layover, and the overland route via Verkhny Lars is cheaper still and more scenic. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Makhachkala?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Makhachkala%20and%20want%20to%20book%20tours",
  "tip":"From Makhachkala I recommend flying via Mineralnye Vody: the Azimuth MRV–Tbilisi flight is just 1 hour 20 minutes, it doesn't get shorter. One hour of time difference, easy adjustment. In my experience, a Dagestani raised on the culture of the feast loves the Georgian supra — an evening with a tamada in Kakheti where kvevri wine flows under endless toasts. And after the Caspian shores, Kazbegi and the Military Highway show mountains of a whole new scale. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Makhachkala in 2026?","Three convenient options. 1) Via Mineralnye Vody: fly to MRV, then the direct Azimuth MRV–Tbilisi flight of just 1 hour 20 minutes, from 12,000 RUB. 2) Via Moscow with a connection — 7–9 hours, from 16,000 RUB. 3) The overland route via Vladikavkaz and the Verkhny Lars border along the Georgian Military Highway — the cheapest and most scenic, from 9,000 RUB."),
   ("Are there direct flights Makhachkala–Tbilisi?","There is no regular direct Makhachkala–Tbilisi flight: Russia–Georgia routes are operated by Azimuth, Red Wings and Georgian Airways, and the most reliable way is via Mineralnye Vody, where Azimuth reaches Tbilisi in 1 hour 20 minutes. Check current dates on Yandex Travel before buying."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Makhachkala cost?","A self-planned 7-day trip costs from 36,000 RUB: travel via Min. Vody ~12,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth sells tickets for Mir on its website. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Makhachkala banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Makhachkala?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti, with a chance to join the rtveli. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October."),
   ("Which tours are must-do for visitors from Makhachkala?","Three picks: Kakheti — wine country with the Georgian supra, where a Dagestani appreciates the culture of the tamada and toasts (from ₾170); Kazbegi — the Military Highway and the Gergeti Trinity below a 5,033 m peak (from ₾175); Old Tbilisi with Narikala fortress, close to a Derbent native's heart (from ₾100). Plus Mtskheta with UNESCO sites (from ₾98)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },

 "tyumen": {
  "ru":"tyumeni","Name":"Tyumen",
  "title":"Tours to Georgia from Tyumen 2026 — Routes &amp; Prices",
  "desc":"Tours to Georgia from Tyumen: via Moscow from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur.",
  "ogd":"Tyumen–Tbilisi route via Moscow from 14,500 RUB, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "h1":"Tours to Georgia from Tyumen 2026 — travel, budget and routes",
  "lead":"A convenient Moscow connection, accommodation from ₾50/night, private tours from ₾98. Itineraries for 5, 7 and 10 days — cheaper than any package tour.",
  "s1n":"~8h","s1l":"Via Moscow","s3n":"from 14.5K","s3l":"Travel, RUB",
  "leadtext":("Tyumen is the first Russian city of Siberia, capital of the oil country on the bank of the Tura River, famous nationwide for its hot thermal springs. "
   "The easiest way to Tbilisi is via Moscow: the connection adds a couple of hours but offers the widest choice of flights and fares all year round. "
   "And here's what ties a Siberian to the Georgian capital: Tyumen people drive for miles to soak in open-air hot springs even in frost — and in the very heart of old Tbilisi, in the Abanotubani district, natural sulphur waters rise from underground, the very reason the city was founded here a thousand years ago. "
   "Tbilisi itself means 'warm spring'. The Siberian pleasure of hot water in the cold is raised here into a centuries-old tradition of domed bathhouses. "
   "The time difference is just one hour: home is UTC+5, Tbilisi is UTC+4."),
  "fsub":"There are no regular direct Tyumen–Tbilisi flights: aggregators show 'direct', but these are connections. The most reliable way is via Moscow. Real prices for 2026.",
  "rows":("<tr><td>Tyumen → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~7–9h</td><td class=\"highlight\">from 14,500 RUB</td></tr>\n"
   "<tr><td>Tyumen → Istanbul → Tbilisi</td><td>Turkish / Pegasus</td><td>~9–11h</td><td class=\"highlight\">from 21,000 RUB</td></tr>\n"
   "<tr><td>Tyumen → Min. Vody → Tbilisi</td><td>Azimuth (via MRV)</td><td>~7–8h</td><td class=\"highlight\">from 16,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> don't buy a 'direct' aggregator flight at face value — it's almost always a Moscow connection. Choose a ticket with an explicit layover, allow 2 hours between flights. Book 5–7 weeks ahead.",
  "ktitle":"What Tyumen Travellers Should Know",
  "know":[("Just One Hour Apart","Tyumen is UTC+5, Tbilisi is UTC+4 — one hour apart, back. After landing, set your watch back an hour and your body clock is barely disturbed. For a Siberian used to long distances, Georgia's easy adjustment is a pleasant surprise."),
   ("Siberian Hot Springs and Tbilisi Sulphur Baths","Tyumen is famous for open-air thermal springs — Siberians bathe in hot water even in frost. In Tbilisi natural sulphur waters rise from underground: the Abanotubani district with its domed baths is the city's heart. The name 'Tbilisi' itself means 'warm spring'. A familiar pleasure in an ancient tradition."),
   ("First City of Siberia and Ancient Caucasus Capital","Tyumen is the first Russian city beyond the Urals, an outpost of Siberia's settlement. Tbilisi is a capital a millennium and a half old. Both grew by water — Tyumen on the Tura, Tbilisi on the Mtkvari. Siberian scale and Caucasus antiquity: a contrast worth the journey."),
   ("No Package Lock-in","A self-planned trip with a private tour costs 25–35% less than an agency package — and delivers far richer experiences, with your own choice of stay and route.")],
  "budget":"Tyumen travellers find a Moscow connection easiest: plenty of flights year-round, flexible fares, and the layover adds only a couple of hours. Aggregator 'direct' offers are really the same connections — compare honestly by total travel time. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Tyumen?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Tyumen%20and%20want%20to%20book%20tours",
  "tip":"From Tyumen I'd advise not to chase a phantom 'direct' flight: it's a Moscow connection underneath — take it honestly and allow 2 hours for the transfer. Only one hour of time difference. In my experience, a Siberian in love with hot springs must see the Abanotubani sulphur baths — an evening in a domed bath of old Tbilisi you'll remember for a long time. And after flat Siberia, Kazbegi and the Military Highway open mountains of a whole new scale. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Tyumen in 2026?","The optimal option is a Moscow connection: Tyumen → Moscow → Tbilisi, total time 7–9 hours, from 14,500 RUB, with many flights year-round. There are routes via Istanbul (Turkish/Pegasus, 9–11h) and via Mineralnye Vody with the direct Azimuth MRV–Tbilisi flight. There are no regular direct Tyumen–Tbilisi flights."),
   ("Are there direct flights Tyumen–Tbilisi?","No regular direct Tyumen–Tbilisi flight exists. Aggregators sometimes show 'direct', but it's a connection underneath — Russia–Georgia routes are operated only by Azimuth, Red Wings and Georgian Airways, and they don't fly from Tyumen non-stop. The most reliable route is via Moscow; compare options by total travel time."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Tyumen cost?","A self-planned 7-day trip costs from 38,000 RUB: travel via Moscow ~14,500 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth sells tickets for Mir on its website. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Tyumen banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Tyumen?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti. Summer is hot (+35–38°C); the Abanotubani sulphur baths are especially good in the cool season."),
   ("Which tours are must-do for visitors from Tyumen?","Three picks: the Abanotubani sulphur baths in old Tbilisi — a treat for a Siberian who loves hot springs (part of a walking tour, from ₾100); Kazbegi — the Military Highway and the Gergeti Trinity below a 5,033 m peak after flat Siberia (from ₾175); Kakheti — wine country with kvevri tasting (from ₾170). Plus Mtskheta with UNESCO sites (from ₾98)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },

 "stavropol": {
  "ru":"stavropolya","Name":"Stavropol",
  "title":"Tours to Georgia from Stavropol 2026 — Routes &amp; Prices",
  "desc":"Tours to Georgia from Stavropol: via Mineralnye Vody from 11,000 RUB, direct MRV–Tbilisi in 1h20, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "ogd":"Stavropol–Tbilisi via Mineralnye Vody (direct 1h20) from 11,000 RUB, guided tours from ₾98. Itineraries for 5/7/10 days.",
  "h1":"Tours to Georgia from Stavropol 2026 — travel, budget and routes",
  "lead":"Via nearby Mineralnye Vody (direct flight 1h20), accommodation from ₾50/night, private tours from ₾98. Itineraries for 5, 7 and 10 days — 30% cheaper than a package.",
  "s1n":"1h20","s1l":"MRV → Tbilisi","s3n":"from 11K","s3l":"Travel, RUB",
  "leadtext":("Stavropol stands half a kilometre above sea level, on the watershed between the Black and Caspian seas — a green southern capital of the black-earth country, a city they call the Gateway to the Caucasus. "
   "And that gate opens straight onto Georgia: neighbouring Mineralnye Vody is about 165 km away, and from there Azimuth reaches Tbilisi on a direct flight in 1 hour 20 minutes — there simply is no shorter flight to Georgia from Russia. "
   "A Stavropol native comes to the Georgians almost as a relative by the vineyard. Stavropol is wine country: Praskoveya wines have matured here since 1898, one of Russia's oldest wineries. "
   "Georgia answers with kvevri wine from clay vessels buried in the ground, a craft older than the pyramids. Two southern, hospitable peoples, two cultures of the vine and the feast, find a common tongue from the very first toast. "
   "The time difference is just one hour: home is UTC+3, Tbilisi is UTC+4."),
  "fsub":"There's no direct flight from Stavropol itself, but neighbouring Mineralnye Vody, about two hours away, offers the shortest direct flight to Georgia — Azimuth MRV–Tbilisi in 1 hour 20 minutes. Real prices for 2026.",
  "rows":("<tr><td>Stavropol → Min. Vody → Tbilisi (direct)</td><td>Azimuth</td><td>~4–5h</td><td class=\"highlight\">from 11,000 RUB</td></tr>\n"
   "<tr><td>Stavropol → Moscow → Tbilisi</td><td>Aeroflot + connecting</td><td>~7–9h</td><td class=\"highlight\">from 16,000 RUB</td></tr>\n"
   "<tr><td>Stavropol → Vladikavkaz → Verkhny Lars</td><td>overland transfer</td><td>~7–9h</td><td class=\"highlight\">from 8,000 RUB</td></tr>"),
  "infobox":"<strong>Tip:</strong> your ace is neighbouring Mineralnye Vody, about two hours away. Drive to MRV airport by land, then Azimuth to Tbilisi in just 1 hour 20 minutes — the shortest flight to Georgia from Russia. Flights run Mon, Wed, Thu, Sat and Sun.",
  "ktitle":"What Stavropol Travellers Should Know",
  "know":[("Just One Hour Apart","Stavropol is UTC+3, Tbilisi is UTC+4 — one hour apart. Stavropol and Georgia are neighbours in the North Caucasus, so climate and rhythm are familiar: barely any adjustment, and the first holiday day isn't lost to jet lag."),
   ("Praskoveya and Kvevri: Two Wine Lands","Stavropol is wine country: Praskoveya wines have matured since 1898, one of Russia's oldest wineries. Georgia is the birthplace of wine, made in kvevri — clay vessels buried in the ground. A Stavropol winemaker and a Kakhetian peasant speak the same language of the vine — not rivalry, but brotherhood."),
   ("Gateway to the Caucasus and Mineral Neighbours","Stavropol is called the Gateway to the Caucasus, with the Caucasian Mineral Waters and their springs next door. Georgia greets you with the same Caucasus hospitality and its own healing Borjomi waters. The southern culture of the feast, warmth and welcome needs no translation for a Stavropol native."),
   ("No Package Lock-in","A self-planned trip with a private tour costs 25–35% less than an agency package — and delivers far richer experiences, with your own choice of stay and route.")],
  "budget":"Stavropol travellers are lucky with geography: neighbouring Mineralnye Vody, about two hours away, gives the shortest direct flight to Georgia — Azimuth MRV–Tbilisi in 1h20. That's cheaper and faster than a Moscow layover, and the overland route via Verkhny Lars is cheaper still. A package tour costs 65,000–95,000 RUB with no freedom to choose your stay or tours.",
  "cta":"Planning a trip from Stavropol?","wa":"Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Stavropol%20and%20want%20to%20book%20tours",
  "tip":"From Stavropol I always recommend using your ace, neighbouring Min. Vody: drive to MRV in about two hours, then the direct Azimuth flight to Tbilisi in just 1 hour 20 minutes — no shorter flight to Georgia exists. One hour of time difference. In my experience, the wine country of Stavropol loves Kakheti — kvevri wine tasting in a real marani, where your Praskoveya background gains new colours. And the Military Highway and Kazbegi show the Caucasus in full scale. I recommend 7 days minimum.",
  "faq":[("How to get to Tbilisi from Stavropol in 2026?","The best option is via neighbouring Mineralnye Vody: drive to MRV airport (about two hours), then the direct Azimuth MRV–Tbilisi flight of just 1 hour 20 minutes, from 11,000 RUB. Alternatives: a Moscow connection (7–9h, from 16,000 RUB) and the overland route via Vladikavkaz and Verkhny Lars along the Georgian Military Highway."),
   ("Are there direct flights Stavropol–Tbilisi?","There's no direct flight from Stavropol's own airport, but neighbouring Mineralnye Vody, about two hours away, saves the day: Azimuth operates a direct MRV–Tbilisi flight in 1 hour 20 minutes — the shortest flight to Georgia from Russia. Russia–Georgia routes are operated by Azimuth, Red Wings and Georgian Airways."),
   ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days on a foreign or internal passport. Border control at Tbilisi airport takes 10–20 minutes. No forms, invitations or insurance are required."),
   ("How much does a 7-day trip to Georgia from Stavropol cost?","A self-planned 7-day trip costs from 35,000 RUB: travel via Min. Vody ~11,000 RUB, accommodation ~5,500 RUB/week, food ~3,000 RUB, tours from ~12,000 RUB. A package tour costs 65,000–95,000 RUB and excludes private guided tours."),
   ("Do Mir cards work in Georgia?","Mir cards are not accepted inside Georgia, but Azimuth sells MRV–Tbilisi tickets for Mir on its website. Bring cash rubles and exchange them in Tbilisi — rates near Rustaveli metro beat Stavropol banks. Visa and Mastercard from foreign banks work in most places."),
   ("When is the best time to visit Georgia from Stavropol?","Best by weather: spring (April–May) and autumn (September–October). September–October is special — wine harvest season in Kakheti, especially close to a Stavropol wine lover's heart. Summer is hot (+35–38°C); Kazbegi mountain routes run May–October."),
   ("Which tours are must-do for visitors from Stavropol?","Three picks: Kakheti — wine country where a Stavropol winemaker appreciates kvevri wine alongside a Praskoveya background (from ₾170); Kazbegi — the Military Highway and the Gergeti Trinity below a 5,033 m peak (from ₾175); Mtskheta — 2,000 years of Christian history and UNESCO sites (from ₾98). Plus Old Tbilisi on foot (from ₾100)."),
   ("In what language does guide Timur work?","Guide Timur is fluent in English and Russian and has lived in Tbilisi since 2023. Tours run in your language of choice — he explains Georgian history and culture in a way that truly resonates.")],
 },
}

def _sec(h2, body):
    return ('<div class="section">\n<h2 class="section-title">' + h2 + '</h2>\n'
            '<div class="lead-text" style="padding-top:8px"><p style="max-width:900px">' + body + '</p></div>\n</div>\n<hr class="section-divider"/>\n')

AIRPORT = {
 "ufa": _sec("Direct Ufa–Tbilisi Flight: Airport, Days and Prices",
  "Direct flights are operated by Azimuth from Ufa International Airport named after Mustai Karim (code UFA). Flight time is 2 hours 30 minutes, landing at Tbilisi's Shota Rustaveli airport. One-way fares start from 14,500 RUB, round-trip from about 22,000 RUB; on sales, one-way tickets have dropped to 4,500 RUB. Book 5–7 weeks ahead and avoid Friday and Sunday departures for the best prices. Azimuth accepts Mir, Visa and Mastercard, so you can pay from Russia directly. Tip: choose a fare with checked baggage included — paying at the airport costs more, and on the way back from Tbilisi you'll likely carry wine, churchkhela and spices."),
 "nizhny-novgorod": _sec("Direct Nizhny Novgorod–Tbilisi Flight: Airport and Schedule",
  "Direct flights are operated by Red Wings from Strigino airport (code GOJ); the route resumed on 13 June 2026. Departure is on Saturdays at 9:30, flight time about 3 hours 30 minutes, landing at Tbilisi's Shota Rustaveli airport. Round-trip fares start from about 24,000 RUB, one-way from 13,000 RUB. Strigino also has direct flights to Batumi — handy for a seaside trip. Tip: Saturday is the only direct departure day, so plan your holiday Saturday-to-Saturday and book 5–7 weeks ahead. Payment by Mir, Visa and Mastercard on the carrier's site."),
 "mineralnye-vody": _sec("Direct Mineralnye Vody–Tbilisi Flight: The Shortest Route",
  "Azimuth operates direct flights from Mineralnye Vody airport (code MRV) — the shortest hop to Georgia from Russia, just 1 hour 20 minutes. Flights run Mon, Wed, Thu, Sat and Sun, landing at Tbilisi's Shota Rustaveli airport. One-way fares start from 4,878 RUB, round-trip from about 9,000 RUB. Road lovers can take the overland route: from Mineralnye Vody to Vladikavkaz, then across the Verkhny Lars border along the Georgian Military Highway. Tip: the short flight makes even a weekend trip realistic — fly out Saturday morning, return Sunday evening. Payment by Mir, Visa and Mastercard."),
 "volgograd": _sec("Flying from Volgograd to Tbilisi: Seasonal Direct and via Moscow",
  "Direct Volgograd–Tbilisi flights from Gumrak airport (code VOG) are scheduled in high season — usually summer; operated by Azimuth and Red Wings, about 2 hours 40 minutes. The schedule is unstable, so always check availability for your dates on Yandex Travel before buying. Year-round, a Moscow connection works reliably: 6–8 hours, from 14,000 RUB. Tip: in summer, compare direct and connecting options — the price gap is often small while a direct flight saves real time. Mir cards are accepted by Azimuth and Aeroflot."),
 "saratov": _sec("Getting from Saratov to Tbilisi: The Route via Moscow",
  "There are no direct Saratov–Tbilisi flights: from Gagarin airport (code GSV) the easiest way is via Moscow. The Moscow layover takes 1–2 hours, total travel time 6–8 hours, from 11,000 RUB, operated by Aeroflot and Pobeda. A scenic alternative is flying to Mineralnye Vody, then the overland route via Verkhny Lars along the Georgian Military Highway. A nice bonus for Saratov: the city runs on UTC+4, exactly like Tbilisi, so there is no jet lag — you don't lose the first day. Tip: allow at least two hours between flights in Moscow, especially if the airport changes."),
 "makhachkala": _sec("Getting from Makhachkala to Tbilisi: via Min. Vody and Moscow",
  "From Uytash airport (code MCX) there's no regular direct flight to Tbilisi, but Dagestan is Georgia's Caucasus neighbour and the road is short. The fastest by air is via Mineralnye Vody: a flight to MRV, then the direct Azimuth flight to Tbilisi of just 1 hour 20 minutes; total time about 5–6 hours, from 12,000 RUB. A Moscow connection works year-round (7–9 hours, from 16,000 RUB). Road lovers can take the overland route: from Makhachkala to Vladikavkaz, then across the Verkhny Lars border along the Georgian Military Highway — from 9,000 RUB and scenic mountains all the way. Tip: check any seasonal direct flight for your dates on Yandex Travel before buying. Payment by Mir, Visa and Mastercard."),
 "tyumen": _sec("Getting from Tyumen to Tbilisi: The Moscow Connection",
  "From Roshchino airport (code TJM) there's no regular direct flight to Tbilisi: the carriers that fly to Georgia (Azimuth, Red Wings, Georgian Airways) don't operate from Tyumen non-stop, and aggregator 'direct' offers are really connections. The most reliable way is via Moscow: total time 7–9 hours, from 14,500 RUB, with many flights in any season. There are options via Istanbul (Turkish/Pegasus, 9–11 hours) and via Mineralnye Vody with the short direct Azimuth MRV–Tbilisi flight. The time difference with Tbilisi is only one hour (home is UTC+5), so adjustment is easy even after a long flight. Tip: when buying, look not at the word 'direct' but at total travel time and number of layovers — that's the honest comparison."),
 "stavropol": _sec("Getting from Stavropol to Tbilisi: The Min. Vody Ace",
  "From Shpakovskoye airport (code STW) there's no direct flight to Tbilisi, but Stavropol travellers hold a strong ace — the Caucasian Mineral Waters just 165 km away. Drive to MRV airport by land in about two hours, then Azimuth operates a direct flight to Tbilisi in 1 hour 20 minutes — the shortest flight to Georgia from Russia. Flights run Mon, Wed, Thu, Sat and Sun; total travel time about 4–5 hours, from 11,000 RUB. Alternatives are a Moscow connection (7–9 hours, from 16,000 RUB) and the overland route via Vladikavkaz and Verkhny Lars. Tip: the Azimuth MRV–Tbilisi ticket is paid by Mir, Visa and Mastercard straight from Russia."),
}

def faq_schema(city):
    return ",\n".join('        {\n          "@type": "Question",\n          "name": "%s",\n          "acceptedAnswer": {"@type":"Answer","text":"%s"}\n        }'
        % (q.replace('&amp;','&'), a.replace('"','\\"')) for q,a in city["faq"])

def build(en, D):
    h = DONOR
    h = h.replace("en/tours-from-samara", f"en/tours-from-{en}")
    h = h.replace("tury-v-gruziyu-iz-samary", f"tury-v-gruziyu-iz-{D['ru']}")
    # даты создания → сегодня; битый og:image (og-tury-moskva не существует) → og-cover
    h = h.replace('content="2026-05-15" property="article:published_time"', 'content="2026-07-13" property="article:published_time"')
    h = h.replace('content="2026-06-04" property="article:modified_time"', 'content="2026-07-13" property="article:modified_time"')
    h = h.replace("og-tury-moskva", "og-cover")
    # META
    h = R(h, "<title>Tours to Georgia from Samara 2026 — Flights &amp; Private Tours</title>", f"<title>{D['title']}</title>")
    h = R(h, 'content="Planning a trip to Georgia from Samara? Flights/transport to Tbilisi, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur." name="description"', f'content="{D["desc"]}" name="description"')
    h = R(h, 'content="Tours to Georgia from Samara 2026 — Flights &amp; Private Tours" property="og:title"', f'content="{D["title"]}" property="og:title"')
    h = R(h, 'content="Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with guide Timur. 30% cheaper than package tours." property="og:description"', f'content="{D["ogd"]}" property="og:description"')
    h = R(h, 'content="Tours to Georgia from Samara 2026 — Flights &amp; Guided Tours | Sakhva Travel" property="og:image:alt"', f'content="{D["title"].replace("&amp;","&amp;")} | Sakhva Travel" property="og:image:alt"')
    h = R(h, 'content="Tours to Georgia from Samara 2026 — Flights &amp; Private Tours" name="twitter:title"', f'content="{D["title"]}" name="twitter:title"')
    h = R(h, 'content="Flights from 15K RUB, guided tours from ₾98. Itineraries for 5/7/10 days with a private tour." name="twitter:description"', f'content="{D["ogd"]}" name="twitter:description"')
    # FAQ schema @graph
    i = h.index('"@type": "FAQPage"'); frm = h.index('"mainEntity": [', i); end = h.index('\n      ]\n    }\n  ]\n}', frm)
    h = h.replace(h[frm:end], '"mainEntity": [\n' + faq_schema(D), 1)
    # HERO
    h = R(h, "<h1>Tours to Georgia from Samara 2026 — flights, budget and routes</h1>", f"<h1>{D['h1']}</h1>")
    h = R(h, '<p class="lead">Flights from 16,000 RUB, accommodation from ₾50/night, private tours from ₾98. Georgia is a surprisingly affordable and easy destination from Samara.</p>', f'<p class="lead">{D["lead"]}</p>')
    h = R(h, '<div class="stat"><div class="stat-num">from 16K</div><div class="stat-label">Flight, RUB</div></div>', f'<div class="stat"><div class="stat-num">{D["s3n"]}</div><div class="stat-label">{D["s3l"]}</div></div>')
    h = R(h, '<div class="stat"><div class="stat-num">5–8h</div><div class="stat-label">Travel time</div></div>', f'<div class="stat"><div class="stat-num">{D["s1n"]}</div><div class="stat-label">{D["s1l"]}</div></div>')
    # LEAD TEXT
    ls = h.index('<div class="lead-text">'); le = h.index('</div>', h.index('<p>', ls))
    h = h.replace(h[ls:le], '<div class="lead-text">\n<p>\n    ' + D["leadtext"] + '\n  </p>\n', 1)
    # FLIGHTS
    h = R(h, "Direct flights (Pobeda, Red Wings, ~2h) plus connections via Istanbul, Moscow or Dubai. Real prices for 2026 from Samara.", D["fsub"])
    ts = h.index("<tbody>", h.index("How to Get to Georgia")); te = h.index("</tbody>", ts)
    h = h.replace(h[ts:te], "<tbody>\n" + D["rows"] + "\n", 1)
    ibs = h.index('<div class="info-box">', ts); ibe = h.index('</div>', h.index('<p>', ibs))
    h = h.replace(h[ibs:ibe], '<div class="info-box">\n<p>' + D["infobox"] + '</p>\n', 1)
    # KNOW title + 4 cards
    h = R(h, "What Samara Travellers Should Know", D["ktitle"])
    kold = [("Kurumoch Airport","KUF has good connections to Istanbul via Turkish Airlines. The Moscow hub also opens up all Moscow-based connections for a competitive price."),
     ("Volga to Kura River","From the great Volga to the ancient Kura — two river cities with deep historical roots. Samara and Tbilisi share a spirit of openness, culture and riverside walks."),
     ("Affordable Alternative to Europe","Georgia offers European-level sights and cuisine at 30–40% lower prices than European destinations accessible from Samara. A 7-day trip is genuinely affordable."),
     ("Same Time Zone","Samara is UTC+4, same as Tbilisi. Zero jet lag — you arrive and feel at home immediately.")]
    for (oh,op),(nh,np) in zip(kold, D["know"]):
        h = R(h, f'>{oh}</h3>', f'>{nh}</h3>'); h = R(h, op, np)
    # BUDGET note
    h = R(h, "A package tour from Samara costs 65,000–95,000 RUB per person. A self-planned trip with a private tour costs 25–35% less with far better experiences.", D["budget"])
    # CTA + WA
    h = R(h, "Planning a trip from Samara?", D["cta"])
    h = R(h, "Hello!%20I%20am%20travelling%20to%20Georgia%20from%20Samara%20and%20want%20to%20book%20tours", D["wa"])
    # Timur's Tip
    h = R(h, "From Samara the Istanbul connection is best — one layover and 5–7 hours and you're in Tbilisi. I'll plan the itinerary to start same day. Kazbegi + Kakheti is the classic combo for 7 days.", D["tip"])
    # уникальная секция про аэропорт/рейс — перед зелёным блоком «All Tours»
    green = '<div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:12px;padding:16px 20px;margin:32px auto;max-width:1100px">'
    h = R(h, green, AIRPORT[en] + green)
    # убрать каннибал общего запроса «Georgia tours» из тела гео-страницы:
    # донорская CTA-ссылка на общий хаб → гео-конверсия на /en/booking/
    h = R(h,
          '<a href="/en/tours-in-georgia/" style="color:#16A34A;font-weight:700">All Tours in Georgia 2026</a>',
          f'<a href="/en/booking/" style="color:#16A34A;font-weight:700">Book a tour from {D["Name"]}</a>')
    # уникализируем practical money-карточку city-ref
    h = R(h, "Exchange rubles in Tbilisi: best rates on Rustaveli Ave. Mir cards don't work.",
          f"Exchange rubles in Tbilisi: best rates on Rustaveli Ave, better than {D['Name']} banks. Mir cards don't work.")
    # Product name
    h = R(h, "Tours to Georgia from Samara 2026 — How to Plan Your Trip", f"Tours to Georgia from {D['Name']} 2026 — How to Plan Your Trip")
    # FAQ visible 8
    fold = [
     ("How to get to Tbilisi from Samara in 2026?","Via Istanbul (Turkish Airlines, from 16,000 RUB round-trip, ~5–7 hours) is most popular. Also via Moscow or Dubai."),
     ("Do Russian citizens need a visa for Georgia?","No. Russian citizens can stay in Georgia visa-free for up to 365 days. A foreign passport or internal Russian passport is sufficient. Border control normally takes 5–15 minutes."),
     ("How much does a 7-day trip to Georgia from Samara cost?","Costs vary by transport option. See the budget table above for a full breakdown from Samara."),
     ("Do Mir cards work in Georgia?","No, Mir cards are not accepted in Georgia. Bring cash rubles/dollars and exchange to lari in Tbilisi (best rates on Rustaveli and at Dezerter Market). Visa and Mastercard from foreign banks work everywhere. Withdraw lari from TBC Bank and Bank of Georgia ATMs without issues."),
     ("When is the best time to visit Georgia from Samara?","Best times are spring (April–May) and autumn (September–October). May brings cherry blossoms; September–October is wine harvest season in Kakheti. Summer (June–August) is hot (+35–38°C in Tbilisi), winter is mild in the city (+5–10°C) and ski season at Gudauri."),
     ("Which tours are must-do for visitors from Samara?","Top 3 essential tours: 1) Kazbegi — mountains, Gergeti Trinity Church facing Mt. Kazbek (from ₾175/person); 2) Kakheti — wine, Sighnaghi, kvevri tasting (from ₾170/person); 3) Mtskheta — UNESCO, Svetitskhoveli (from ₾98/person). In the city: Old Tbilisi walking tour (from ₾100/person)."),
     ("In what language does guide Timur work?","Guide Timur is fluent in both English and Russian, and has lived in Tbilisi since 2023. All tours are conducted in your language of choice. He explains Georgian history and culture in a way that truly resonates."),
    ]
    # донор: 7 совпадающих + 8-й cancel. Наш faq[8] включает "Are there direct flights" 2-м.
    fd = D["faq"]
    pairs = [(fold[0],fd[0]),(fold[1],fd[2]),(fold[2],fd[3]),(fold[3],fd[4]),(fold[4],fd[5]),(fold[5],fd[6]),(fold[6],fd[7])]
    for (oq,oa),(nq,na) in pairs:
        h = R(h, f'>{oq}</div>', f'>{nq}</div>')
        h = R(h, f'>{oa}</div>', f'>{na}</div>')
    # остаточный Samara -> Name
    h = h.replace("Samara", D["Name"])
    return h

def main():
    keys = sys.argv[1:] or list(C)
    for en in keys:
        D = C[en]
        out = ROOT / f"en/tours-from-{en}"
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build(en, D), encoding="utf-8")
        print(f"OK  en/tours-from-{en}/index.html")

if __name__ == "__main__":
    main()
