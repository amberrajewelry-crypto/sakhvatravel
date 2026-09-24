#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Слой-1: механический аудит КАЧЕСТВА перевода GE (не смысл — дефекты).
Ловит: потерю/искажение данных (цены/телефоны/годы/валюты EN≠GE), битые замены
(склейки латиница×грузиница, двойные пробелы, дубли-слова, пустые теги, обрывы),
битые внутр-ссылки, неверный canonical/hreflang-self, обрезанные мета."""
import re, glob, sys
from pathlib import Path
from collections import Counter

DOMAIN = "https://sakhva-travel.com"
def rd(p): return Path(p).read_text(encoding="utf-8")

def en_of(ge_html):
    m = re.search(r'<link[^>]*hreflang="en"[^>]*>', ge_html)
    if not m: return None
    u = re.search(r'href="([^"]+)"', m.group(0)).group(1).replace(DOMAIN,"").strip("/")
    return (u+"/index.html") if u else "index.html"

def body_of(h):
    b = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    return re.sub(r'<style.*?</style>', '', b, flags=re.S)

# --- 1) данные: цены/валюты/телефоны/годы должны совпасть EN↔GE ---
def money(h):
    return Counter(re.findall(r'[₾€$₽]\s?\d[\d,.]*|\d[\d,.]*\s?(?:lari|ლარი|EUR|USD|GEL)', h))
def phones(h):
    return Counter(re.findall(r'\+\d[\d\s()\-]{7,}\d', h))
def years(h):
    return Counter(re.findall(r'\b20\d{2}\b', h))

# --- 2) битые замены ---
def defects(h):
    body = body_of(h)
    out = []
    # склейка латиница×грузиница без дефиса/пробела (Sakhva Travel-ის ОК; SakhvaТури — нет)
    for m in re.findall(r'[A-Za-z]{2,}[ა-ჰ]{2,}|[ა-ჰ]{2,}[A-Za-z]{2,}', body):
        if '-' not in m: out.append(("склейка", m[:40]))
    # двойной пробел в тексте
    for m in re.findall(r'>([^<>]*  [^<>]*)<', body):
        if m.strip(): out.append(("двойной-пробел", m.strip()[:40]))
    # дубль слова подряд (груз/лат)
    for m in re.findall(r'\b(\w{3,})\s+\1\b', body):
        out.append(("дубль-слова", m[:30]))
    # дубль-дефис-склейка QR-QR / ტური-ტური
    for m in re.findall(r'\b(\w{2,})-\1\b', body):
        out.append(("дубль-дефис", m[:30]))
    # пустой видимый тег-контейнер с двоеточием-остатком «: <» или «— <»
    for m in re.findall(r'>\s*[—:-]\s*<', body):
        out.append(("висячий-знак", m.strip()))
    # обрыв мультибайт (заканчивается на латинский предлог)
    for m in re.findall(r'>([^<>]*\b(?:the|and|for|with|from|of|to|in)\s*)<', body):
        out.append(("англ-обрыв", m.strip()[:40]))
    return out

# --- 3) внутренние ссылки не битые ---
def broken_links(h):
    out = []
    for href in set(re.findall(r'href="(/[^"#?]*)"', h)):
        if href.startswith('//'): continue
        rel = href.strip('/')
        if not rel: continue
        # каталог → index.html
        cands = [rel, rel+"/index.html", rel+".html"]
        if any(Path(c).exists() for c in cands): continue
        # статические (css/js/img/xml/txt/ico/woff)
        if re.search(r'\.(css|js|png|jpg|jpeg|webp|svg|xml|txt|ico|woff2?|json|pdf|avif|gif)$', href):
            if not Path(rel).exists(): out.append(("нет-файла", href))
            continue
        out.append(("битая-ссылка", href))
    return out

# --- 4) canonical/hreflang self ---
def canon_hreflang(h, ge_file):
    out = []
    exp = DOMAIN + "/" + str(Path(ge_file).parent).replace("\\","/").replace("ge","ge",1)
    m = re.search(r'<link[^>]*rel="canonical"[^>]*>', h)
    if not m: out.append(("нет-canonical",""))
    else:
        u = re.search(r'href="([^"]+)"', m.group(0)).group(1)
        if "/ge/" not in u and not u.rstrip("/").endswith("/ge"):
            out.append(("canonical-не-ge", u))
    ka = re.search(r'<link[^>]*hreflang="ka"[^>]*href="([^"]+)"', h)
    can = re.search(r'rel="canonical"[^>]*href="([^"]+)"', h) or \
          re.search(r'href="([^"]+)"[^>]*rel="canonical"', h)
    if ka and can and ka.group(1).rstrip("/") != can.group(1).rstrip("/"):
        out.append(("hreflang-ka≠canonical", f"{ka.group(1)} vs {can.group(1)}"))
    for lang in ("ru","en","ka","x-default"):
        if not re.search(rf'hreflang="{lang}"', h):
            out.append(("нет-hreflang", lang))
    return out

# --- 5) мета не обрезаны ---
def meta_trunc(h):
    out = []
    t = re.search(r'<title>(.*?)</title>', h, re.S)
    if t:
        tt = t.group(1).strip()
        if tt.endswith(('-','—','…','...',' в',' и',' на')): out.append(("title-обрыв", tt[-25:]))
        if len(tt) < 8: out.append(("title-короткий", tt))
    d = re.search(r'name="description"[^>]*content="([^"]*)"', h) or \
        re.search(r'content="([^"]*)"[^>]*name="description"', h)
    if d:
        dd = d.group(1).strip()
        if len(dd) < 40: out.append(("desc-короткий", dd[:40]))
        if dd.endswith(('-','—',' в',' и',' на',' the',' a')): out.append(("desc-обрыв", dd[-25:]))
    return out

def audit(ge):
    h = rd(ge); enp = en_of(h)
    print(f"\n{'='*72}\n{ge}")
    issues = 0
    # данные EN↔GE
    if enp and Path(enp).exists():
        e = rd(enp)
        for name, fn in (("валюта/цены",money),("телефоны",phones),("годы",years)):
            ce, cg = fn(body_of(e)), fn(body_of(h))
            miss, extra = ce-cg, cg-ce
            if miss or extra:
                # годы могут отличаться (2024-2026 диапазоны) — показываем как WARN
                issues += 1
                print(f"  ⚠ {name}: потеряно {dict(miss)} / добавлено {dict(extra)}")
        # длина текста (не потерян ли блок): число видимых символов груз±
        te = len(re.sub(r'\s+',' ',body_of(e))); tg = len(re.sub(r'\s+',' ',body_of(h)))
        r = tg/te if te else 0
        if not (0.7 <= r <= 1.6):
            issues += 1; print(f"  ⚠ объём текста GE/EN = {r:.2f} (ожидалось 0.7–1.6)")
    else:
        print(f"  ✗ EN-оригинал не найден: {enp}"); issues += 1
    # дефекты замен
    d = defects(h)
    if d:
        issues += len(d); print(f"  ⚠ дефекты замен: {len(d)}")
        for k,v in d[:15]: print(f"      [{k}] {v}")
    # ссылки
    bl = broken_links(h)
    if bl:
        issues += len(bl); print(f"  ⚠ ссылки: {len(bl)}")
        for k,v in bl[:12]: print(f"      [{k}] {v}")
    # canonical/hreflang
    ch = canon_hreflang(h, ge)
    if ch:
        issues += len(ch); print(f"  ⚠ canonical/hreflang: {len(ch)}")
        for k,v in ch: print(f"      [{k}] {v}")
    # мета
    mt = meta_trunc(h)
    if mt:
        issues += len(mt); print(f"  ⚠ мета: {len(mt)}")
        for k,v in mt: print(f"      [{k}] {v}")
    if issues == 0: print("  ✅ дефектов не найдено")
    return issues

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(f for f in glob.glob("ge/**/*.html", recursive=True)
        if (m:=re.search(r'<title>(.*?)</title>', rd(f), re.S)) and re.search(r'[Ⴀ-ჿ]', m.group(1)))
    tot = sum(audit(f) for f in files)
    print(f"\n{'='*72}\nИТОГ: суммарно проблем/варнингов {tot} по {len(files)} стр")
