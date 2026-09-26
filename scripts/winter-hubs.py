#!/usr/bin/env python3
"""Winter hubs: fix RU/GE /tury-v-gruziyu-zimoy/ (prices, photos, facts, package cards)
and build EN /en/tury-v-gruziyu-zimoy/ (shell = RU hub head/CSS + EN nav/footer).

Idempotent. Run after build-winter-packages.py.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sakhva-travel.com"
TODAY = "2026-09-26"
CARD_MARK = 'data-sk="winter-2d"'
e = html.escape

CARD = """
    <a {mark} href="{href}" class="tour-card">
      <div class="tour-img" style="background-image:url('/images/{img}')">
        <div class="tour-badge">{badge}</div>
      </div>
      <div class="tour-body">
        <h3>{h3}</h3>
        <p class="tour-desc">{desc}</p>
        <div class="tour-meta"><span>&#9202; {dur}</span><span>&#127976; {night}</span></div>
        <div class="tour-price">
          <div class="price">{price} <span>{pp}</span></div>
          <span class="book-btn">{more}</span>
        </div>
      </div>
    </a>
"""

CARDS = {
    "ru": [dict(href="/ekskursiya/tur-gudauri-kazbegi-2-dnya/", img="gudauri-zima.webp",
                badge="2 дня · ночёвка", h3="Гудаури + Казбеги за 2 дня",
                desc="День на склонах Гудаури, ночь в горах, утром — Крестовый перевал и Гергети в снегу. "
                     "Отель с завтраком включён, план Б при закрытом перевале.",
                dur="2 дня", night="ночь в Гудаури", price="от ₾520", pp="/ чел", more="Подробнее"),
           dict(href="/ekskursiya/tur-borjomi-bakuriani-2-dnya/", img="bakuriani-zima.webp",
                badge="2 дня · семьям", h3="Боржоми + Бакуриани за 2 дня",
                desc="Тёплые серные бассейны Боржоми под открытым небом, ночь в Боржоми, утром — санки и "
                     "пологие трассы Бакуриани. Без высоких перевалов.",
                dur="2 дня", night="ночь в Боржоми", price="от ₾520", pp="/ чел", more="Подробнее")],
    "ge": [dict(href="/ge/ekskursiya/tur-gudauri-kazbegi-2-dnya/", img="gudauri-zima.webp",
                badge="2 დღე · ღამისთევა", h3="გუდაური + ყაზბეგი 2 დღეში",
                desc="დღე გუდაურის ფერდობებზე, ღამე მთაში, დილით — ჯვრის უღელტეხილი და თოვლიანი გერგეტი. "
                     "სასტუმრო საუზმით შედის ფასში.",
                dur="2 დღე", night="ღამე გუდაურში", price="₾520", pp="/ კაცი", more="დეტალურად"),
           dict(href="/ge/ekskursiya/tur-borjomi-bakuriani-2-dnya/", img="bakuriani-zima.webp",
                badge="2 დღე · ოჯახებს", h3="ბორჯომი + ბაკურიანი 2 დღეში",
                desc="ბორჯომის თბილი გოგირდის აუზები ღია ცის ქვეშ, ღამე ბორჯომში, დილით — ციგა და "
                     "ბაკურიანის რბილი ტრასები.",
                dur="2 დღე", night="ღამე ბორჯომში", price="₾520", pp="/ კაცი", more="დეტალურად")],
}

FIXES = {
    "ru": [("url('/images/kazbegi-tour.webp')", "url('/images/gudauri-tour-600.webp')"),
           ("url('/images/batumi-tour.webp')", "url('/images/noviy-god-tour-600.webp')"),
           ("url('/images/kutaisi-tour.webp')", "url('/images/borjomi-tour-600.webp')"),
           ("7 700 ₽ <span>", "от ₾225 <span>"), ("35 000 ₽ <span>", "от ₾850 <span>"),
           ("6 230 ₽ <span>", "от ₾178 <span>"), ("3 500 ₽ <span>", "от ₾135 <span>"),
           ("Бесплатная отмена за 48ч.", "Полный возврат при отмене за 14+ дней."),
           ("Скипас на день — от 80 ₾ (около 2800 ₽).", "Скипас на день — около 70 ₾ (сезон 2025/26)."),
           ("Гудаури открывается в середине месяца", "Гудаури открывается в конце месяца (в 2025/26 — 27 декабря)"),
           ("Сезон: январь–март.", "Сезон: конец декабря — начало апреля.")],
    "ge": [("url('/images/kazbegi-tour.webp')", "url('/images/gudauri-tour-600.webp')"),
           ("url('/images/batumi-tour.webp')", "url('/images/noviy-god-tour-600.webp')"),
           ("url('/images/kutaisi-tour.webp')", "url('/images/borjomi-tour-600.webp')"),
           ('class="price">₾220 ', 'class="price">₾225 '), ('class="price">₾1000 ', 'class="price">₾850 '),
           ('class="price">₾100 ', 'class="price">₾135 '),
           ("უფასო გაუქმება 48 საათით ადრე.", "სრული დაბრუნება 14+ დღით ადრე გაუქმებისას."),
           ("სკი-ფასი დღეზე — 80 ₾-დან.", "სკიპასი დღეზე — დაახლოებით 70 ₾ (2025/26 სეზონი)."),
           ("გუდაური თვის შუა რიცხვებში იხსნება", "გუდაური თვის ბოლოს იხსნება (2025/26-ში — 27 დეკემბერს)"),
           ("სეზონი: იანვარი–მარტი.", "სეზონი: დეკემბრის ბოლოდან აპრილის დასაწყისამდე.")],
}

META = {
    "ru": dict(title="Туры в Грузию зимой 2026–27 — Гудаури, Казбеги, Боржоми",
               desc='Туры в Грузию зимой 2026–27: Гудаури, Казбеги в снегу, бассейны Боржоми, Новый год в Тбилиси. Экскурсии от ₾135, туры на 2 дня от ₾520.', h1=("Туры в Грузию зимой 2026<", "Туры в Грузию зимой 2026–27<")),
    "ge": dict(title="ზამთრის ტურები საქართველოში 2026–27 — გუდაური, ბორჯომი",
               desc='ზამთრის ტურები საქართველოში 2026–27: გუდაური, თოვლიანი ყაზბეგი, ბორჯომის აუზები, ახალი წელი თბილისში. ორდღიანი ტურები ₾520-დან.', h1=("ზამთარში 2026<", "ზამთარში 2026–27<")),
}


def fix_meta(s, lang):
    m = META[lang]
    s = re.sub(r"<title>.*?</title>", "<title>" + e(m["title"]) + "</title>", s, count=1, flags=re.S)
    for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")',
                r'(<meta content=")[^"]*(" name="description")', r'(<meta content=")[^"]*(" property="og:description")'):
        s = re.sub(pat, lambda x: x.group(1) + e(m["desc"]) + x.group(2), s)
    for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta content=")[^"]*(" property="og:title")'):
        s = re.sub(pat, lambda x: x.group(1) + e(m["title"]) + x.group(2), s)
    if m["h1"]:
        s = s.replace(*m["h1"])
    return s


def add_cards(s, cards):
    if CARD_MARK in s[s.find('class="tours-grid"'):s.find("</main>")].split("<hr")[0]:
        return s
    g = s.index('<div class="tours-grid"')
    first_end = s.index("</a>", g) + len("</a>")
    html_cards = "".join(CARD.format(mark=CARD_MARK, **c) for c in cards)
    return s[:first_end] + html_cards + s[first_end:]


def fix_hub(lang):
    f = ROOT / ("" if lang == "ru" else "ge") / "tury-v-gruziyu-zimoy" / "index.html"
    s = f.read_text()
    for a, b in FIXES[lang]:
        s = s.replace(a, b)
    if lang == "ru":  # region cards: one currency, like tour pages
        s = re.sub(r"от [\d ]+ ₽ \((₾\d+)/чел\)", r"от \1/чел", s)
    s = re.sub(r'<p data-sk="winter-2d"[^>]*>.*?</p>\n', "", s)
    s = add_cards(s, CARDS[lang])
    s = fix_meta(s, lang)
    # hreflang: EN version now exists
    en = f'<link rel="alternate" hreflang="en" href="{SITE}/en/tury-v-gruziyu-zimoy/"/>'
    if 'hreflang="en"' not in s:
        s = s.replace('<link rel="alternate" hreflang="ru"', en + '\n<link rel="alternate" hreflang="ru"', 1)
    f.write_text(s)
    return f


# ---------------- EN hub ----------------
EN_TITLE = "Winter Tours in Georgia 2026–27 — Gudauri, Kazbegi, Borjomi"
EN_DESC = ("Winter tours in Georgia: Gudauri skiing, snowy Kazbegi, Borjomi warm "
           "pools, New Year in Tbilisi. Day trips from ₾135, 2-day tours from ₾520.")
EN_CARDS = [
    dict(href="/en/ekskursiya/tur-gudauri-kazbegi-2-dnya/", img="gudauri-zima.webp",
         badge="2 days · overnight", h3="Gudauri + Kazbegi, 2 days",
         desc="A full day on the Gudauri slopes, a night in the mountains, then the Cross Pass and snowy "
              "Gergeti. Hotel with breakfast included, plan B if the pass closes.",
         dur="2 days", night="night in Gudauri", price="from ₾520", pp="/ person", more="Details"),
    dict(href="/en/ekskursiya/tur-borjomi-bakuriani-2-dnya/", img="bakuriani-zima.webp",
         badge="2 days · families", h3="Borjomi + Bakuriani, 2 days",
         desc="Open-air warm sulfur pools in Borjomi, a night in Borjomi, then sledding and gentle slopes "
              "in Bakuriani. No high passes.",
         dur="2 days", night="night in Borjomi", price="from ₾520", pp="/ person", more="Details"),
    dict(href="/en/ekskursiya/ekskursiya-gudauri-iz-tbilisi/", img="gudauri-tour-600.webp",
         badge="Day trip", h3="Gudauri day trip from Tbilisi",
         desc="Georgia's main ski resort in one day: Ananuri on the way, 4–5 hours on the slopes or a "
              "gondola ride, back in Tbilisi in the evening.",
         dur="1 day", night="no overnight", price="from ₾225", pp="/ person", more="Details"),
    dict(href="/en/ekskursiya/tur-gruziya-noviy-god/", img="noviy-god-tour-600.webp",
         badge="New Year", h3="New Year in Georgia",
         desc="New Year's Eve in Tbilisi, then winter Kazbegi and Kakheti with a local guide. "
              "Book 4–8 weeks ahead: the holidays sell out fast.",
         dur="multi-day", night="Tbilisi", price="from ₾850", pp="/ person", more="Details"),
    dict(href="/en/ekskursiya/ekskursiya-borjomi-iz-tbilisi/", img="borjomi-tour-600.webp",
         badge="Day trip", h3="Borjomi day trip from Tbilisi",
         desc="Borjomi Central Park, the mineral spring you can drink from for free, the cable car "
              "and warm pools — back in Tbilisi the same evening.",
         dur="1 day", night="no overnight", price="from ₾178", pp="/ person", more="Details"),
    dict(href="/en/ekskursiya/ekskursiya-stary-tbilisi/", img="gruziya-zimoy.webp",
         badge="Tbilisi · winter", h3="Old Tbilisi and sulfur baths",
         desc="Narikala fortress, the Bridge of Peace and Abanotubani, the domed bath quarter over hot "
              "springs. Best in winter, when the warm water feels like magic.",
         dur="4–5 hours", night="city", price="from ₾135", pp="/ person", more="Details"),
]
EN_FAQ = [
    ("Is Georgia worth visiting in winter?",
     "Yes. Gudauri is one of the best ski resorts in the Caucasus, Tbilisi is quiet and cosy without "
     "crowds, and hotels are noticeably cheaper than in summer. The trade-off: Tusheti is closed "
     "and Svaneti roads are harder in snow."),
    ("When is the ski season in Gudauri?",
     "Usually from late December to early April; in 2025/26 the lifts opened on December 27. February and "
     "March have the most reliable snow and sunny days. A day ski pass cost about ₾70 in 2025/26."),
    ("Can I visit Kazbegi in winter?",
     "Yes. The Georgian Military Highway stays open most days, but the Gudauri — Kobi section can close "
     "after heavy snow or avalanche risk. We watch road updates and keep a plan B, such as a second ski "
     "day in Gudauri or Ananuri and Mtskheta."),
    ("What is the weather like in Tbilisi in winter?",
     "December to February is usually 0 to +8 °C, often grey and damp; snow in the city is rare and "
     "melts fast. Gudauri at the same time is around −5 to −15 °C with good snow."),
    ("Should I choose a day trip or a 2-day tour?",
     "A day trip is cheaper but leaves 4–5 hours at the destination after the drive. A 2-day tour adds a "
     "night in the mountains or in Borjomi, so you get a full day of skiing or pools and a second "
     "destination the next morning."),
]


def build_en():
    ru = (ROOT / "tury-v-gruziyu-zimoy" / "index.html").read_text()
    shell = (ROOT / "en" / "odnodnevnye-ekskursii-iz-tbilisi" / "index.html").read_text()
    head = ru[:ru.index("<nav id=\"nav\">")]
    head = re.sub(r'<html lang="[^"]*"', '<html lang="en"', head)
    head = re.sub(r"<title>.*?</title>", f"<title>{e(EN_TITLE)}</title>", head, flags=re.S)
    head = re.sub(r'<meta[^>]*name="description"[^>]*>', f'<meta name="description" content="{e(EN_DESC)}">', head)
    head = re.sub(r'<meta[^>]*property="og:[^"]*"[^>]*>\s*', "", head)
    head = re.sub(r'<meta[^>]*name="twitter:[^"]*"[^>]*>\s*', "", head)
    head = re.sub(r'<link[^>]*rel="(?:canonical|alternate)"[^>]*hreflang[^>]*>\s*|<link[^>]*hreflang[^>]*>\s*', "", head)
    head = re.sub(r'<link[^>]*rel="canonical"[^>]*>\s*', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    url = f"{SITE}/en/tury-v-gruziyu-zimoy/"
    meta = [
        f'<link rel="canonical" href="{url}"/>',
        f'<link rel="alternate" hreflang="en" href="{url}"/>',
        f'<link rel="alternate" hreflang="ru" href="{SITE}/tury-v-gruziyu-zimoy/"/>',
        f'<link rel="alternate" hreflang="ka" href="{SITE}/ge/tury-v-gruziyu-zimoy/"/>',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/tury-v-gruziyu-zimoy/"/>',
        '<meta property="og:type" content="website"/>',
        f'<meta property="og:title" content="{e(EN_TITLE)}"/>',
        f'<meta property="og:description" content="{e(EN_DESC)}"/>',
        f'<meta property="og:url" content="{url}"/>',
        f'<meta property="og:image" content="{SITE}/images/gudauri-zima.jpg"/>',
        '<meta property="og:image:width" content="1600"/><meta property="og:image:height" content="840"/>',
        '<meta property="og:locale" content="en_US"/><meta property="og:site_name" content="Sakhva Travel"/>',
        '<meta name="twitter:card" content="summary_large_image"/>',
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#webpage", "url": url,
         "name": EN_TITLE, "description": EN_DESC, "inLanguage": "en", "datePublished": TODAY,
         "dateModified": TODAY, "isPartOf": {"@id": f"{SITE}/#website"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": SITE + c["href"], "name": c["h3"]}
             for i, c in enumerate(EN_CARDS)]}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/en/"},
            {"@type": "ListItem", "position": 2, "name": "Tours", "item": f"{SITE}/en/tours-in-georgia/"},
            {"@type": "ListItem", "position": 3, "name": "Winter tours in Georgia", "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in EN_FAQ]},
    ]
    head += "\n".join(meta) + "\n" + "\n".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in ld) + "\n"

    faq = "".join(
        f'<div class="faq-item"><div class="faq-q" onclick="this.parentElement.classList.toggle(\'open\')">'
        f'{e(q)}</div><div class="faq-a">{e(a)}</div></div>\n' for q, a in EN_FAQ)
    cards = "".join(CARD.format(mark=CARD_MARK if "2-dnya" in c["href"] else "", **c) for c in EN_CARDS)
    main = f"""<main>
<section style="padding:clamp(100px,14vw,160px) clamp(16px,3.5vw,56px) 48px;background:linear-gradient(135deg,#1A3D2E 0%,#2D5A40 100%);text-align:center">
<h1 style="font-size:clamp(26px,3.8vw,46px);font-weight:800;color:#fff;margin:0 0 12px;line-height:1.2">Winter Tours in Georgia 2026–27</h1>
<p style="font-size:clamp(14px,1.6vw,18px);color:rgba(255,255,255,.75);max-width:700px;margin:0 auto;line-height:1.6">Skiing in Gudauri, snowy Kazbegi, Borjomi warm pools and a quiet Tbilisi. Private tours with a local guide, up to 7 people.</p>
</section>
<div class="lead-text"><p>Winter in Georgia runs from late December to March: the Caucasus is under snow, Tbilisi is calm and cheaper than in summer, and the mountains are two hours from the city. Below are the winter routes we actually run — one-day trips for a quick taste and 2-day tours with an overnight stay when you want a full day on the slopes or in the pools.</p></div>
<div class="tours-grid" style="margin-top:32px">{cards}</div>

<hr class="section-divider">
<div class="section" style="background:#F9FAFB;max-width:100%;padding:56px 0">
<div style="max-width:1200px;margin:0 auto;padding:0 clamp(16px,3.5vw,56px)">
  <h2 class="section-title">Gudauri — the main ski resort of the Caucasus</h2>
  <p class="section-sub">About 120 km from Tbilisi, 2,196–3,007 m above sea level, runs for every level.</p>
  <div class="spots-grid">
    <div class="spot-card"><div class="spot-num">1</div><h3>Runs for every level</h3><p>Gentle blue runs near the village for beginners, red and black ones higher up with views of the Main Caucasus Range. A day ski pass cost about ₾70 in 2025/26; rental and instructors are available on the spot.</p></div>
    <div class="spot-card"><div class="spot-num">2</div><h3>Season and snow</h3><p>The lifts usually open in late December (December 27 in 2025/26) and run until early April. February and March are the safest bet for snow and sunshine.</p></div>
    <div class="spot-card"><div class="spot-num">3</div><h3>Bakuriani — the family option</h3><p>Georgia's second resort, near Borjomi at 1,700 m: gentler slopes, pine forest and sledding. Easy to combine with the warm pools of Borjomi on a 2-day trip.</p></div>
    <div class="spot-card"><div class="spot-num">4</div><h3>Day trip or overnight?</h3><p>The drive takes about 2.5 hours each way, so a day trip leaves 4–5 hours on the slopes. With a night in Gudauri you ski a full day and see Kazbegi the next morning.</p></div>
  </div>
</div>
</div>

<hr class="section-divider">
<div class="section">
  <h2 class="section-title">Winter Tbilisi — quiet and atmospheric</h2>
  <p class="section-sub">December to February is the best time to see the city without crowds.</p>
  <div class="usp-grid">
    <div class="usp-item"><div class="usp-icon">&#9832;</div><h3>Abanotubani sulfur baths</h3><p>The domed bath quarter sits on hot sulfur springs around +37 °C. A private room after a cold walk is the best winter experience in the city.</p></div>
    <div class="usp-item"><div class="usp-icon">&#127968;</div><h3>No tourist crowds</h3><p>Old Town restaurants are full of locals, Narikala has no tour buses, and photos come out without strangers in the frame.</p></div>
    <div class="usp-item"><div class="usp-icon">&#127876;</div><h3>New Year and Christmas</h3><p>Tbilisi is decorated from mid-December. Georgian Orthodox Christmas (Shoba) is on January 7, with the Alilo processions through the streets.</p></div>
    <div class="usp-item"><div class="usp-icon">&#128176;</div><h3>Lower prices</h3><p>Hotels are much cheaper than in summer. The exception is the New Year peak, roughly December 27 to January 3 — book early.</p></div>
  </div>
</div>

<section class="faq-section">
  <h2>Winter in Georgia — frequently asked questions</h2>
{faq}</section>

<div class="section" style="text-align:center;padding-top:32px;padding-bottom:32px">
  <p style="font-size:15px;color:#374151;margin-bottom:14px">Read more: <a href="/en/blog/georgia-in-winter/">Georgia in winter — full guide</a> · <a href="/en/blog/kazbegi-in-winter/">Kazbegi in winter</a> · <a href="/en/blog/new-year-in-georgia/">New Year in Georgia</a></p>
  <a href="https://wa.me/995511272623?text=Hello!%20I%27d%20like%20a%20winter%20tour%20in%20Georgia%20[site:en:hub:winter]" class="btn-wa" style="text-decoration:none">WhatsApp — reply in 15 min</a>
</div>
</main>"""
    body_start = shell.index("</head>")
    nav = shell[body_start:shell.index("<main")]
    tail = shell[shell.index("</main>") + len("</main>"):]
    nav = nav.replace("/ge/odnodnevnye-ekskursii-iz-tbilisi/", "/ge/tury-v-gruziyu-zimoy/")
    nav = nav.replace("/odnodnevnye-ekskursii-iz-tbilisi/", "/tury-v-gruziyu-zimoy/")
    out = head + nav + main + tail
    f = ROOT / "en" / "tury-v-gruziyu-zimoy" / "index.html"
    f.parent.mkdir(exist_ok=True)
    f.write_text(out)
    return f


if __name__ == "__main__":
    for lang in ("ru", "ge"):
        print("fixed", fix_hub(lang).relative_to(ROOT))
    en = build_en()
    s = en.read_text()
    assert s.count("<h1") == 1 and "odnodnevnye" not in s[:s.index("</head>")]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S):
        json.loads(b)
    print("built", en.relative_to(ROOT), len(EN_TITLE), len(EN_DESC))
