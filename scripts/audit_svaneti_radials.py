# -*- coding: utf-8 -*-
"""Строгий SEO-аудит 12 страниц радиалок Сванетии. Только факты из файлов."""
import re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUGS=["lednik-chalaadi-mestia","ushguli-iz-mestii","ushguli-shkhara-lednik","ozero-koruldi-mestia"]
DIRS={"ru":"ekskursiya","en":"en/ekskursiya","ka":"ge/ekskursiya"}

def rx1(p,h,f=re.S):
    m=re.search(p,h,f); return m.group(1).strip() if m else ""

rows=[]
for lang,d in DIRS.items():
    for slug in SLUGS:
        h=(ROOT/d/slug/"index.html").read_text(encoding="utf-8")
        title=rx1(r"<title>(.*?)</title>",h)
        desc=rx1(r'<meta name="description" content="(.*?)"/>',h)
        h1s=re.findall(r'<h1[^>]*>(.*?)</h1>',h,re.S)
        h2s=re.findall(r'<h2[^>]*>(.*?)</h2>',h,re.S)
        h3s=re.findall(r'<h3[^>]*>(.*?)</h3>',h,re.S)
        # видимый текст: убрать script/style/теги
        body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',h,flags=re.S)
        body=re.sub(r'<[^>]+>',' ',body)
        words=len(re.findall(r'\w+',body,re.U))
        canon=rx1(r'<link href="(https[^"]*)" rel="canonical"/>',h)
        hrefs=sorted(set(re.findall(r'hreflang="([a-z-]+)"',h)))
        lang_attr=rx1(r'<html lang="([a-z]+)"',h)
        # json-ld типы + валидность
        blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S)
        types=[]; bad=0
        for b in blocks:
            try: j=json.loads(b.strip()); types.append(j.get("@type","?"))
            except Exception: bad+=1; types.append("PARSE_ERR")
        og=len(re.findall(r'property="og:',h)); tw=len(re.findall(r'name="twitter:',h))
        imgs=re.findall(r'<img[^>]*>',h); noalt=sum(1 for i in imgs if 'alt=' not in i)
        # внутренние ссылки (href="/...") уникальные
        ilinks=set(re.findall(r'href="(/[^"#]*)"',h))
        faq_q=len(re.findall(r'"@type":"Question"',h))
        og_locale=rx1(r'<meta content="([a-z_]+)" property="og:locale"/>',h)
        price=rx1(r'"price":"(\d+)"',h)
        rows.append(dict(lang=lang,slug=slug,title=title,tlen=len(title),desc=desc,dlen=len(desc),
            h1=len(h1s),h1txt=h1s[0] if h1s else "",h2=len(h2s),h3=len(h3s),words=words,canon=canon,
            href=hrefs,lang_attr=lang_attr,types=types,bad=bad,og=og,tw=tw,noalt=noalt,
            ilinks=len(ilinks),faq=faq_q,og_locale=og_locale,price=price))

def line(s='─',n=92): print(s*n)
# 1. Мета
print("\n### 1. TITLE / DESCRIPTION (длина, лимиты 60/160)")
line()
print(f"{'lang':4} {'slug':24} {'Tlen':>4} {'Dlen':>4}  title")
for r in rows:
    fl="⚠" if r['tlen']>62 or r['dlen']>165 or r['dlen']<120 else "✓"
    print(f"{r['lang']:4} {r['slug']:24} {r['tlen']:>4} {r['dlen']:>4} {fl} {r['title'][:52]}")

# 2. Каннибализация — уникальность title/desc/h1
print("\n### 2. КАННИБАЛИЗАЦИЯ (уникальность title/desc/h1 среди 12)")
line()
for key in ('title','desc','h1txt'):
    vals=[r[key] for r in rows]; uniq=len(set(vals))
    print(f"{key:8}: {uniq}/12 уникальных  -> {'✓ OK' if uniq==12 else '❌ ДУБЛИ'}")
# внутриязыковая уникальность
for lang in DIRS:
    ts=[r['title'] for r in rows if r['lang']==lang]
    print(f"  [{lang}] title уник: {len(set(ts))}/4")

# 3. Структура/объём
print("\n### 3. СТРУКТУРА (H1=1, H2/H3, объём слов; thin<600)")
line()
print(f"{'lang':4} {'slug':24} {'H1':>2} {'H2':>2} {'H3':>2} {'words':>6}  flag")
for r in rows:
    fl="✓" if r['h1']==1 and r['words']>=600 else "⚠"
    print(f"{r['lang']:4} {r['slug']:24} {r['h1']:>2} {r['h2']:>2} {r['h3']:>2} {r['words']:>6}  {fl}")

# 4. Schema
print("\n### 4. SCHEMA JSON-LD (валидность + типы)")
line()
for r in rows:
    fl="✓" if r['bad']==0 else "❌"
    print(f"{r['lang']:4} {r['slug']:24} bad={r['bad']} {fl}  {','.join(r['types'])}")

# 5. hreflang/canonical/lang
print("\n### 5. HREFLANG / CANONICAL / lang / og:locale")
line()
need={'en','ka','ru','x-default'}
for r in rows:
    fl="✓" if set(r['href'])==need and r['slug'] in r['canon'] and f"/{DIRS[r['lang']].split('/')[0] if r['lang']!='ru' else ''}" or True else "⚠"
    ok_href="✓" if set(r['href'])==need else "❌"
    print(f"{r['lang']:4} {r['slug']:24} href={ok_href} lang={r['lang_attr']} og={r['og_locale']} canon…/{r['canon'].split('/')[-2]}/")

# 6. og/twitter/images/links/faq/price
print("\n### 6. OG / TWITTER / IMG-alt / внутр.ссылки / FAQ / price")
line()
print(f"{'lang':4} {'slug':24} {'og':>3} {'tw':>3} {'noalt':>5} {'ilinks':>6} {'faq':>3} {'price':>5}")
for r in rows:
    print(f"{r['lang']:4} {r['slug']:24} {r['og']:>3} {r['tw']:>3} {r['noalt']:>5} {r['ilinks']:>6} {r['faq']:>3} {r['price']:>5}")

# сводка проблем
print("\n### СВОДКА")
line()
issues=[]
for r in rows:
    if r['tlen']>62: issues.append(f"{r['lang']}/{r['slug']}: title {r['tlen']}>62")
    if r['dlen']>165: issues.append(f"{r['lang']}/{r['slug']}: desc {r['dlen']}>165")
    if r['dlen']<120: issues.append(f"{r['lang']}/{r['slug']}: desc {r['dlen']}<120 (коротко)")
    if r['h1']!=1: issues.append(f"{r['lang']}/{r['slug']}: H1={r['h1']}")
    if r['bad']: issues.append(f"{r['lang']}/{r['slug']}: schema parse err")
    if r['noalt']: issues.append(f"{r['lang']}/{r['slug']}: img без alt={r['noalt']}")
    if r['words']<600: issues.append(f"{r['lang']}/{r['slug']}: thin {r['words']}w")
print(f"Всего страниц: {len(rows)} | проблем: {len(issues)}")
for i in issues: print("  ⚠ "+i)
if not issues: print("  чистых блокеров нет")
