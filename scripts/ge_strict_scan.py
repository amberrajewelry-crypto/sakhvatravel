#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""СТРОГИЙ сканер GE: на грузинской странице не должно быть НИ РУССКОГО, НИ
АНГЛИЙСКОГО слова, кроме легитимных keeps (бренды/имена авторов/email/@хэндл/
URL/entity/коды валют/авиалинии). Кириллица на GE = русский остаток (алфавиты
не пересекаются). Латиница {2,} вне keeps = английский остаток. Зоны проверки:
текст-ноды, alt/aria-label/placeholder/title, человеко-мета, JSON-LD-значения."""
import re, json, sys, glob
from pathlib import Path

BRANDS = {
    "SAKHVA","TRAVEL","Travel","Sakhva","FAQ","TIN","NOWPayments","USDT","TRC-20",
    "Bitcoin","BTC","Ethereum","ETH","BNB","Visa","Mastercard","MIR","AMEX","WhatsApp",
    "Telegram","Instagram","WiFi","Timur","Google","TripAdvisor","Yandex","Maps","2GIS",
    "Viator","Tripster","UNESCO","GEL","USD","EUR","QR","USB","AC","4WD","SUV","SBP",
    "Email","Wise","Revolut","SWIFT","flydubai","Emirates","Turkish","Airlines",
    "Georgian","Airways","Wizz","Air","Pegasus","FlyArystan","SCAT","Red","Wings",
    "Azimuth","Aeroflot","S7","Nordwind","Utair","Pobeda","AI","GPS","OK",
    "Slow","Armenia","Airbnb","Bolt","Skyscanner","Magti","Geocell","Beeline",
    "Ferrari","Formula","SIM","Go","RUB","Georgia","Tbilisi","Batumi","Kazbegi",
    "VK","VKontakte","YouTube","UTC","GB","TBC","Bank","ALA","NQZ","Guda","Puris Sakhli","Puris","Sakhli","Uzbekistan Airways","UZ","Air Astana","BYN","Belavia","Lonely","Planet",
    "vs","Bolt","Yandex.Go","Skyscanner","Threads","Mir","American","Express","Homo","erectus","georgicus",
    "FlyOne","Armenia Airlines","ASAN","Silknet","Cellfie","UFA","IATA","Ural","Rossiya","CEK","KZN","SVX","OVB","KUF","ROV","KRR","AER","MRV","NAL","OGZ","MCX","VOG","GSV","VOZ","PEE","TJM","GOJ","LED","STW","MSQ","EVN","TAS","DME","SVO","VKO","BQS",
}
ROMAN_RE = re.compile(r'^[IVXLCDM]{1,7}$')                    # римские цифры (века)
# переключатель языков — коды остаются латиницей (это НЕ англ-остаток)
SWITCHER = {"RU","EN","GE","KA"}
BRAND_RE = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, BRANDS), key=len, reverse=True)) + r')\b')
# ЯВНЫЙ список авторов отзывов (латиница-транслит остаётся). Ломкий regex-матч
# «[A-Z][a-z]+» глотал англ. UI-лейблы (Contact/Crypto/Pay Online) как «имена».
AUTHORS = {"Amovei","Giorgi V.","Mikhail D","Mikhail D.","Nugo Shengelia","Nugo S.",
           "Tigran M.","Vitaly","Vladislav S.","Sergey","Amber R","Elena","Vitaliy"}
CYR = re.compile(r'[а-яА-ЯёЁ]')                                # русский
LAT = re.compile(r'[A-Za-z]{2,}')                             # английский
JSONLD_KEYS = {"name","description","text","reviewBody","headline","alternateName"}

def is_keep(t):
    """строка после снятия брендов/entity/чисел/пунктуации не содержит букв → keep"""
    if t in AUTHORS: return True
    if t.startswith('@'): return True
    if re.match(r'^@?[\w.\-]+@[\w.\-]+$', t): return True     # email
    if re.match(r'^https?://', t) or re.match(r'^[\w.\-]+\.(com|ge|ru|org)\b', t): return True
    r = re.sub(r'&\w+;', ' ', t)
    r = BRAND_RE.sub(' ', r)
    r = re.sub(r'[0-9\W_]+', ' ', r)
    return not re.search(r'[A-Za-z]{2,}', r)

def flag(t):
    """вернёт (LANG, offending_token, full) если строка содержит остаток; иначе None.
    Репортит КОНКРЕТНЫЙ токен (кирилл-ран или лат-слово вне бренда), не весь текст."""
    t = t.strip()
    if not t or t in SWITCHER: return None
    if t in AUTHORS or t.startswith('@'): return None
    if re.match(r'^[\w.\-]+@[\w.\-]+', t): return None        # email
    if "'+" in t or "+t." in t: return None                  # JS-шаблон в атрибуте
    # русский: любой кирилл-ран (груз. алфавит не пересекается)
    if CYR.search(t):
        run = re.search(r'[а-яА-ЯёЁ][а-яА-ЯёЁ \-]*', t).group(0).strip()
        return ("RU", run, t)
    # английский: снять entity/@хэндлы/email/бренды → остались лат-слова?
    cleaned = re.sub(r'&#?x?\w+;', ' ', t)
    cleaned = re.sub(r'@\w+|[\w.\-]+@[\w.\-]+', ' ', cleaned)
    cleaned = cleaned.replace("Bank of Georgia", " ")   # бренд-банк
    cleaned = BRAND_RE.sub(' ', cleaned)
    lat = [w for w in re.findall(r'[A-Za-z]{2,}', cleaned)
           if w not in SWITCHER and not ROMAN_RE.match(w)]
    if lat:
        return ("EN", " ".join(lat[:4]), t)
    return None

def walk_jsonld(o, emit):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in JSONLD_KEYS and isinstance(v, str): emit(v)
            else: walk_jsonld(v, emit)
    elif isinstance(o, list):
        for x in o: walk_jsonld(x, emit)

def scan(f):
    html = Path(f).read_text(encoding="utf-8")
    hits = []
    # 1) текст-ноды (без script/style)
    body = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    for t in re.findall(r'>([^<>]+)<', body):
        r = flag(t)
        if r: hits.append(("text", *r))
    # 2) человеко-атрибуты
    for attr in ("alt","aria-label","placeholder","title"):
        for m in re.findall(attr + r'="([^"]*)"', html):
            r = flag(m)
            if r: hits.append((attr, *r))
    # 3) человеко-мета
    for tag in re.findall(r'<meta\b[^>]*>', html):
        key = re.search(r'(?:name|property)="([^"]+)"', tag)
        cont = re.search(r'content="([^"]*)"', tag)
        if key and cont and key.group(1) in (
            "description","og:title","og:description","twitter:title",
            "twitter:description","og:image:alt"):
            r = flag(cont.group(1))
            if r: hits.append(("meta:"+key.group(1), *r))
    # 4) JSON-LD значения
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: data = json.loads(m.group(1))
        except Exception:
            hits.append(("jsonld","ERR","не распарсился")); continue
        walk_jsonld(data, lambda v: (lambda r: hits.append(("jsonld", *r)) if r else None)(flag(v)))
    return hits

if __name__ == "__main__":
    files = sys.argv[1:] or [f for f in glob.glob("ge/**/*.html", recursive=True)
        if (m := re.search(r'<title>(.*?)</title>', Path(f).read_text(encoding="utf-8"), re.S))
        and re.search(r'[Ⴀ-ჿ]', m.group(1))]
    total_ru = total_en = 0
    for f in sorted(files):
        hits = scan(f)
        ru = [h for h in hits if h[1]=="RU"]
        en = [h for h in hits if h[1]=="EN"]
        total_ru += len(ru); total_en += len(en)
        mark = "✅ ЧИСТО" if not hits else f"⚠ RU:{len(ru)} EN:{len(en)}"
        print(f"{mark}  {f}")
        for zone, lang, token, full in hits[:30]:
            print(f"      [{lang}] «{token[:40]}» ({zone}) ← {full[:60]}")
    print(f"\n{'='*60}\nИТОГ: RU-остатков {total_ru}, EN-остатков {total_en} по {len(files)} стр")
    print("ЧИСТО 100%" if total_ru==0 and total_en==0 else "ЕСТЬ ОСТАТКИ")
