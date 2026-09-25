#!/usr/bin/env python3
"""Блок «группа / частный выезд» + «продлите поездку» на страницах однодневных туров (RU/EN/GE).

Источник цен: data/private_prices.json (копия прайса бота, confirmed=true) + data/catalog.json.
Идемпотентно: блок между маркерами <!--sk-formats:start--> ... <!--sk-formats:end--> пересобирается.
Заодно правит ложное «private tour from ₾<групповая>» / «индивидуальный тур от ₾<групповая>».

Запуск: python3 scripts/inject-price-formats.py [--check]
"""
import json, re, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv
WA = "995511272623"

prices = json.loads((ROOT / "data/private_prices.json").read_text())["tours"]
catalog = {e["slug"]: e for e in json.loads((ROOT / "data/catalog.json").read_text())["excursions"]}

EAST = "tur-kazbegi-kakheti-2-dnya"
UPSELL = {  # однодневка -> пакеты (первый — основной)
    "ekskursiya-kazbegi-iz-tbilisi": [EAST, "tur-gruziya-5-dney"],
    "ekskursiya-ananuri-iz-tbilisi": [EAST, "tur-gruziya-5-dney"],
    "ekskursiya-gudauri-iz-tbilisi": [EAST, "tur-gruziya-5-dney"],
    "ekskursiya-jvari-iz-tbilisi": [EAST, "tur-gruziya-3-dnya"],
    "ekskursiya-mtskheta-iz-tbilisi": [EAST, "tur-gruziya-3-dnya"],
    "ekskursiya-kakheti-iz-tbilisi": [EAST, "tur-gruziya-5-dney"],
    "degustatsiya-vina-kakheti": [EAST, "tur-gruziya-5-dney"],
    "chacha-master-klass": [EAST, "tur-gruziya-3-dnya"],
    "rtveli-sbor-vinograda": [EAST, "tur-gruziya-3-dnya"],
    "ekskursiya-david-gareji": [EAST, "tur-gruziya-3-dnya"],
    "ekskursiya-gori-iz-tbilisi": ["tur-gruziya-3-dnya", "tur-gruziya-5-dney"],
    "ekskursiya-borjomi-iz-tbilisi": ["tur-gruziya-5-dney", "tur-batumi-2-dnya"],
    "tur-kutaisi-iz-tbilisi": ["tur-batumi-2-dnya", "tur-gruziya-5-dney"],
    "tur-batumi-iz-tbilisi": ["tur-batumi-2-dnya", "tur-gruziya-5-dney"],
}

PKG_TITLE = {
    "ru": {EAST: "Казбеги + Кахетия за 2 дня", "tur-gruziya-3-dnya": "Тур по Грузии на 3 дня",
           "tur-gruziya-5-dney": "Тур по Грузии на 5 дней", "tur-batumi-2-dnya": "Батуми на 2 дня с ночёвкой"},
    "en": {EAST: "Kazbegi + Kakheti in 2 days", "tur-gruziya-3-dnya": "Georgia 3-day tour",
           "tur-gruziya-5-dney": "Georgia 5-day tour", "tur-batumi-2-dnya": "Batumi 2 days with overnight"},
    "ka": {EAST: "ყაზბეგი + კახეთი 2 დღეში", "tur-gruziya-3-dnya": "საქართველოს 3-დღიანი ტური",
           "tur-gruziya-5-dney": "საქართველოს 5-დღიანი ტური", "tur-batumi-2-dnya": "ბათუმი 2 დღე ღამისთევით"},
}
PKG_DAYS = {EAST: 2, "tur-gruziya-3-dnya": 3, "tur-gruziya-5-dney": 5, "tur-batumi-2-dnya": 2}

T = {
    "ru": dict(h="Мини-группа или частный выезд", g="Мини-группа", gu="с человека",
               gb=["до 7 человек в минивэне — не автобус на 40 мест", "гид Тимур или гид команды, выезд по расписанию", "выгоднее всего для 1–3 человек"],
               gc="Выбрать дату", p="Частный выезд", pu="за 1–2 человек", pu34="за 3–4 человек",
               pb=["только ваша компания", "время старта и остановки — под вас", "одна цена за машину и гида"],
               pc="Узнать о частном", wa="Здравствуйте! Интересует частный выезд: {t}. Нас человек: , дата: \n[{src}]",
               note="От 5 человек частный выезд не нужен — действует групповая цена за каждого. Предоплата 10% фиксирует дату, отмена бесплатна за 48 часов.",
               uh="Продлите поездку", ul="Чаще всего к этому туру добавляют:", pp="с человека", d="дн.", from_="от"),
    "en": dict(h="Small group or private trip", g="Small group", gu="per person",
               gb=["up to 7 people in a minivan — not a 40-seat bus", "scheduled departures with a local guide", "best value for 1–3 people"],
               gc="Pick a date", p="Private trip", pu="for 1–2 people", pu34="for 3–4 people",
               pb=["just your party", "your start time and stops", "one price for car and guide"],
               pc="Ask about private", wa="Hi! I'm interested in a private trip: {t}. People: , date: \n[{src}]",
               note="From 5 people a private trip isn't needed — the group rate applies per person. A 10% deposit secures the date, free cancellation up to 48 hours before.",
               uh="Extend your trip", ul="Most guests add to this tour:", pp="per person", d="days", from_="from"),
    "ka": dict(h="მცირე ჯგუფი თუ კერძო ტური", g="მცირე ჯგუფი", gu="ერთ ადამიანზე",
               gb=["7 ადამიანამდე მინივენში — არა 40-ადგილიანი ავტობუსი", "გასვლა განრიგით ადგილობრივ გიდთან ერთად", "ყველაზე ხელსაყრელი 1–3 ადამიანისთვის"],
               gc="თარიღის არჩევა", p="კერძო ტური", pu="1–2 ადამიანზე", pu34="3–4 ადამიანზე",
               pb=["მხოლოდ თქვენი კომპანია", "დაწყების დრო და გაჩერებები — თქვენზე", "ერთი ფასი მანქანასა და გიდზე"],
               pc="კერძო ტურის შესახებ", wa="გამარჯობა! მაინტერესებს კერძო ტური: {t}. ადამიანები: , თარიღი: \n[{src}]",
               note="5 ადამიანიდან კერძო ტური არ არის საჭირო — მოქმედებს ჯგუფური ფასი თითოეულზე. 10% წინასწარი გადახდა ადასტურებს თარიღს, გაუქმება უფასოა 48 საათით ადრე.",
               uh="გააგრძელეთ მოგზაურობა", ul="ამ ტურს ყველაზე ხშირად ამატებენ:", pp="ერთ ადამიანზე", d="დღე", from_=""),
}
PREFIX = {"ru": "", "en": "/en", "ka": "/ge"}
DIRS = {"ru": "ekskursiya", "en": "en/ekskursiya", "ka": "ge/ekskursiya"}

CARD = "background:#fff;border:1px solid #D1FAE5;border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:8px"


def price_str(lang, n):
    return f"₾{n}-დან" if lang == "ka" else f"{T[lang]['from_']} ₾{n}"


def block(lang, slug, tour_title):
    t, pr = T[lang], next(p for p in prices if p["slug"] == slug)
    g, p12, p34 = pr["group_price"], pr["private"]["1-2"], pr["private"]["3-4"]
    wa = f"https://wa.me/{WA}?text=" + urllib.parse.quote(t["wa"].format(t=tour_title, src=f"site:{lang}:{slug}:private"))
    li = lambda xs: "".join(f'<li style="margin:2px 0">{x}</li>' for x in xs)
    pk = ""
    for ps in UPSELL[slug]:
        c = catalog[ps]
        pk += (f'<a href="{PREFIX[lang]}/ekskursiya/{ps}/" style="{CARD};text-decoration:none;color:#111827">'
               f'<span style="font-weight:700;font-size:16px">{PKG_TITLE[lang][ps]}</span>'
               f'<span style="font-size:14px;color:#374151">{PKG_DAYS[ps]} {t["d"]} · {price_str(lang, c["price"])} {t["pp"]}</span>'
               f'<span style="font-size:14px;font-weight:600;color:#1A3D2E">→</span></a>')
    return f"""<!--sk-formats:start-->
<section class="sk-formats" data-sk="formats-v1" style="margin:28px 0">
<h2 style="font-size:24px;margin:0 0 14px;color:#1A3D2E">{t['h']}</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px">
<div style="{CARD}"><span style="font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#6B7280">{t['g']}</span>
<span style="font-size:28px;font-weight:700;color:#1A3D2E">₾{g} <span style="font-size:14px;font-weight:400;color:#6B7280">{t['gu']}</span></span>
<ul style="margin:0;padding-left:18px;font-size:14px;color:#374151">{li(t['gb'])}</ul>
<a href="/booking/?tour={slug}" style="margin-top:auto;text-align:center;background:#1A3D2E;color:#fff;padding:12px 18px;border-radius:9999px;font-weight:700;text-decoration:none">{t['gc']}</a></div>
<div style="{CARD};border-color:#F59E0B"><span style="font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#B45309">{t['p']}</span>
<span style="font-size:28px;font-weight:700;color:#1A3D2E">₾{p12} <span style="font-size:14px;font-weight:400;color:#6B7280">{t['pu']}</span></span>
<span style="font-size:14px;color:#374151">₾{p34} {t['pu34']}</span>
<ul style="margin:0;padding-left:18px;font-size:14px;color:#374151">{li(t['pb'])}</ul>
<a href="{wa}" target="_blank" rel="noopener" data-track="wa-private" style="margin-top:auto;text-align:center;background:#25D366;color:#fff;padding:12px 18px;border-radius:9999px;font-weight:700;text-decoration:none">{t['pc']}</a></div>
</div>
<p style="font-size:13px;color:#6B7280;margin:10px 0 0">{t['note']}</p>
<h3 style="font-size:20px;margin:24px 0 6px;color:#1A3D2E">{t['uh']}</h3>
<p style="font-size:14px;color:#6B7280;margin:0 0 10px">{t['ul']}</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">{pk}</div>
</section>
<!--sk-formats:end-->"""


def fix_claims(lang, s, g, p12):
    rules = {
        "en": [
            (rf"with a private tour from ₾{g}\b", f"from ₾{g} per person in a group, private from ₾{p12} for 1–2"),
            (rf"with a private guide,? from ₾{g}\b", f"with a guide, from ₾{g} per person in a group (private from ₾{p12})"),
            (rf"Private tour from Tbilisi from ₾{g}\b", f"Group tour from Tbilisi from ₾{g} per person, private from ₾{p12}"),
            (rf"Private (4x4 )?tour from ₾{g}\b", rf"Group \1tour from ₾{g} per person, private from ₾{p12}"),
            (rf"Private tour, ([^,]{{1,20}}), from ₾{g}\b", rf"Group tour, \1, from ₾{g} per person (private from ₾{p12})"),
        ],
        "ka": [
            (rf"კერძო გიდით,? ₾{g}-დან", f"ჯგუფში ₾{g}-დან, კერძო ტური ₾{p12}-დან 1–2 ადამიანზე"),
            (rf"კერძო გიდთან ₾{g}-დან", f"ჯგუფში ₾{g}-დან, კერძო ტური ₾{p12}-დან 1–2 ადამიანზე"),
            (rf"კერძო (4x4 )?ტური ₾{g}-დან", rf"ჯგუფური \1ტური ₾{g}-დან, კერძო ₾{p12}-დან"),
            (rf"კერძო ტური, ([^,]{{1,20}}), ₾{g}-დან", rf"ჯგუფური ტური, \1, ₾{g}-დან (კერძო ₾{p12}-დან)"),
        ],
        "ru": [
            (rf"индивидуальный тур на ([^,<]{{1,25}}?) от ₾{g} с человека",
             rf"тур на \1: в группе от ₾{g} с человека, частный выезд от ₾{p12} за 1–2 человек"),
        ],
    }
    n = 0
    for pat, rep in rules[lang]:
        s, k = re.subn(pat, rep, s)
        n += k
    return s, n


report, bad = [], []
for pr in prices:
    slug = pr["slug"]
    if not pr.get("confirmed") or slug not in UPSELL:
        continue
    for lang, d in DIRS.items():
        f = ROOT / d / slug / "index.html"
        if not f.exists():
            continue
        s = src = f.read_text()
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = re.sub(r"<[^>]+>|\s+2026", "", h1.group(1)).strip() if h1 else slug
        s = re.sub(r"\n?<!--sk-formats:start-->.*?<!--sk-formats:end-->", "", s, flags=re.S)
        m = re.search(r'<div class="key-fact"[^>]*>', s)
        if not m:
            bad.append(f"{f.relative_to(ROOT)}: нет key-fact"); continue
        end = s.find("</div>", m.end())
        if "<div" in s[m.end():end]:
            bad.append(f"{f.relative_to(ROOT)}: вложенный div в key-fact"); continue
        end += len("</div>")
        s = s[:end] + "\n" + block(lang, slug, title) + s[end:]
        s, n = fix_claims(lang, s, pr["group_price"], pr["private"]["1-2"])
        report.append(f"{f.relative_to(ROOT)}  claims_fixed={n}")
        if s != src and not CHECK:
            f.write_text(s)

print("\n".join(report)); print(f"страниц: {len(report)}")
if bad:
    print("ПРОПУЩЕНО:\n" + "\n".join(bad)); sys.exit(1)
