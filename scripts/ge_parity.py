#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Строгий аудит паритета GE ↔ EN: GE обязан быть 1:1 зеркалом EN (перевод меняет
ТОЛЬКО текст, структура идентична). Сверяет каждую переведённую GE-страницу с её
EN-оригиналом (из hreflang en). Флагует расхождения структуры/контента/схемы и
англ-остатки в GE."""
import re, json, glob, sys
from pathlib import Path

DOMAIN = "https://sakhva-travel.com"

def rd(p): return Path(p).read_text(encoding="utf-8")

def en_path_of(ge_html):
    m = re.search(r'<link[^>]*hreflang="en"[^>]*>', ge_html)
    if not m: return None
    u = re.search(r'href="([^"]+)"', m.group(0)).group(1)
    rel = u.replace(DOMAIN, "").strip("/")
    return (rel + "/index.html") if rel else "index.html"

def counts(html):
    body = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    def n(p, h=body): return len(re.findall(p, h, re.S))
    return {
        "h1": n(r'<h1[\s>]'), "h2": n(r'<h2[\s>]'), "h3": n(r'<h3[\s>]'),
        "table": n(r'<table[\s>]'), "tr": n(r'<tr[\s>]'), "td": n(r'<t[dh][\s>]'),
        "p": n(r'<p[\s>]'), "li": n(r'<li[\s>]'), "img": n(r'<img[\s>]'),
        "FAQ(fq)": n(r'class="fq"'), "reviews(rc-text)": n(r'rc-text'),
        "section": n(r'<section[\s>]'), "figure": n(r'<figure[\s>]'),
        "img_src": len(set(re.findall(r'<img[^>]*src="([^"]+)"', body))),
    }

def meta_presence(html):
    def has(p): return bool(re.search(p, html))
    return {
        "title": has(r'<title>[^<]{5,}</title>'),
        "description": has(r'name="description"') or has(r'content="[^"]+"[^>]*name="description"'),
        "og:title": has(r'og:title'), "og:description": has(r'og:description'),
        "og:image": has(r'og:image'), "canonical": has(r'rel="canonical"'),
    }

def jsonld_types(html):
    types = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: data = json.loads(m.group(1))
        except Exception: return None
        def walk(o):
            if isinstance(o, dict):
                t = o.get("@type")
                if t: types.append(t if isinstance(t, str) else "|".join(t))
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for x in o: walk(x)
        walk(data)
    return sorted(types)

# англ-остатки в GE (reuse логики движка, упрощённо)
BRAND_RE = re.compile(r'\b(SAKHVA|TRAVEL|Sakhva|Timur|NOWPayments|WhatsApp|Telegram|'
    r'Instagram|TripAdvisor|Yandex|Google|Maps|Email|2GIS|Revolut|Wise|SWIFT|Visa|'
    r'Mastercard|MIR|AMEX|WiFi|USB|GEL|USD|EUR|UNESCO|Wizz Air|BTC|ETH|USDT|BNB|'
    r'Bitcoin|Ethereum|FAQ|Viator|Tripster|Avatar|Ali|Nino|Jason|David|Constantine|'
    r'Bagrat|Trajan|Matthias|Andrey Krasnov|Wikipedia|Turkish Airlines|flydubai|'
    r'Georgian Airways|Pegasus|Aeroflot|Travel|Emirates|Red Wings|Azimuth|Nordwind|'
    r'Utair|Pobeda|FlyArystan|SCAT|Airways|Georgian|Turkish|RUB|UFA|Bolt|'
    r'Magti|Geocell|Beeline|Silknet|Cellfie|ASAN|Airbnb|Mir|TBC|Bank|Ural|Airlines|Wings|Rossiya|Platov|'
    r'Koltsovo|Marjanishvili|Vake|Borjomi|Alazani|Dezerter|Gudauri|Balandino|Uzbekistan Airways|Air Astana|BYN|Belavia|FlyOne|Armenia Airlines|Kilikia|Bagratashen|Sadakhlo|TBS|Toyota|Camry|BOG|Metromoney|Stambo|Vanilla Sky|Vanilla|Sky|Platanus|orientalis|Kapilamuris|Marani|CO|Wine Underground|Vino Underground|Underground|Vino|g\.Vino|Rkatsiteli|Twins Wine Cellar|Twins|Cellar|iPhone|iPhone 15 Pro|Pro)\b')
# латиница-имена авторов отзывов (транслит, остаются латиницей — не остаток)
NAME_RE = re.compile(r'^[A-Z][a-z]+( [A-Z][a-z]*\.?)?$')

def en_leftovers(html):
    body = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    out = []
    for t in re.findall(r'>([^<>]+)<', body):
        t = t.strip()
        if not re.search(r'[A-Za-z]{4,}', t): continue
        if re.search(r'[Ⴀ-ჿ]', t): continue
        if NAME_RE.match(t): continue          # имя автора отзыва
        if re.match(r'^@?[\w.\-]+@?[\w.\-]*$', t) and (' ' not in t) and \
           ('@' in t or '.com' in t): continue  # email / @handle / бот
        if t.startswith('@'): continue          # соц-хэндл
        # убрать бренды/entity/числа — остался ли англ-текст?
        rest = re.sub(r'&\w+;', ' ', t)
        rest = BRAND_RE.sub(' ', rest)
        rest = re.sub(r'[0-9\W_]+', ' ', rest)
        if re.search(r'[A-Za-z]{4,}', rest):
            out.append(t)
    return out

def audit(ge_file):
    ge = rd(ge_file)
    enp = en_path_of(ge)
    print(f"\n{'='*70}\nGE: {ge_file}")
    if not enp or not Path(enp).exists():
        print(f"  ✗ EN-оригинал не найден ({enp})"); return False
    en = rd(enp)
    print(f"EN: {enp}")
    ok = True
    # 1) структура
    ce, cg = counts(en), counts(ge)
    diffs = {k: (ce[k], cg[k]) for k in ce if ce[k] != cg[k]}
    if diffs:
        ok = False
        print("  ⚠ СТРУКТУРА расходится (EN→GE):")
        for k, (a, b) in diffs.items(): print(f"      {k}: {a} → {b}")
    else:
        print("  ✅ структура 1:1 (h1/h2/h3/table/tr/img/FAQ/reviews/section/figure)")
    # 2) мета
    me, mg = meta_presence(en), meta_presence(ge)
    mmiss = [k for k in mg if mg[k] != me[k]]
    print("  ✅ мета-теги паритет" if not mmiss else f"  ⚠ мета расхождение: {mmiss}")
    ok = ok and not mmiss
    # 3) JSON-LD узлы
    te, tg = jsonld_types(en), jsonld_types(ge)
    if te is None or tg is None:
        print("  ⚠ JSON-LD не распарсился"); ok = False
    elif te != tg:
        print(f"  ⚠ JSON-LD узлы расходятся: EN {len(te)} vs GE {len(tg)}")
        from collections import Counter
        print("      только в EN:", Counter(te) - Counter(tg))
        print("      только в GE:", Counter(tg) - Counter(te))
        ok = False
    else:
        print(f"  ✅ JSON-LD узлы паритет ({len(te)} шт)")
    # 4) англ-остатки в GE
    left = en_leftovers(ge)
    if left:
        ok = False
        print(f"  ⚠ АНГЛ-ОСТАТКИ в GE: {len(left)}")
        for l in left[:20]: print(f"      | {l[:90]}")
    else:
        print("  ✅ англ-остатков нет")
    return ok

if __name__ == "__main__":
    files = sys.argv[1:] or [f for f in glob.glob("ge/**/*.html", recursive=True)
        if (m := re.search(r'<title>(.*?)</title>', rd(f), re.S)) and re.search(r'[Ⴀ-ჿ]', m.group(1))]
    results = {f: audit(f) for f in sorted(files)}
    print(f"\n{'='*70}\nИТОГ: паритет 100% у {sum(results.values())}/{len(results)} страниц")
    bad = [f for f, v in results.items() if not v]
    if bad:
        print("НЕ 100%:"); [print("  -", f) for f in bad]
