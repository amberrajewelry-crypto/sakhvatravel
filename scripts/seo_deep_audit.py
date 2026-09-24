#!/usr/bin/env python3
"""Deeper site audit (read-only): JSON-LD validity, image alt/dimensions/broken src,
og:image file existence, viewport/charset/lang. Over all sitemap URLs -> local files."""
import os, re, json, glob
from collections import Counter, defaultdict
ROOT="/Users/vladimir/sakhva-travel"; DOMAIN="https://sakhva-travel.com"; os.chdir(ROOT)

def loc_list(p): return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", open(p,encoding="utf-8").read())
maps=[m for m in glob.glob("sitemap*.xml") if m!="sitemap-index.xml"]
urls=sorted({u for m in maps for u in loc_list(m)})

def u2f(u):
    if not u.startswith(DOMAIN): return None
    p=u[len(DOMAIN):].split("#")[0].split("?")[0].strip("/")
    if p=="" : return "index.html"
    for c in (os.path.join(p,"index.html"),p,p+".html"):
        if os.path.isfile(c): return c
    return None

def img_exists(src):
    src=src.split("?")[0].split("#")[0]
    if src.startswith("http"):
        return None  # external, skip
    if src.startswith("//"): return None
    if src.startswith("data:"): return True
    p=src.lstrip("/")
    return os.path.isfile(os.path.join(ROOT,p))

bad_jsonld=[]; jsonld_types=Counter()
img_no_alt=defaultdict(int); img_no_dim=defaultdict(int); img_broken=defaultdict(list)
no_viewport=[]; no_charset=[]; no_lang=[]
checked=0
for u in urls:
    f=u2f(u)
    if not f: continue
    checked+=1
    h=open(f,encoding="utf-8",errors="replace").read()

    # JSON-LD validity
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S|re.I):
        raw=m.group(1).strip()
        try:
            data=json.loads(raw)
            objs=data if isinstance(data,list) else [data]
            for o in objs:
                if isinstance(o,dict):
                    t=o.get("@type");
                    if isinstance(t,list): [jsonld_types.update([x]) for x in t]
                    elif t: jsonld_types.update([t])
                    if "@graph" in o:
                        for g in o["@graph"]:
                            if isinstance(g,dict) and g.get("@type"):
                                tt=g["@type"]; jsonld_types.update(tt if isinstance(tt,list) else [tt])
        except Exception as e:
            bad_jsonld.append(f"{u}  ({str(e)[:50]})")

    # images
    for tag in re.findall(r'<img\b[^>]*>', h, re.I):
        if 'alt=' not in tag.lower(): img_no_alt[f]+=1
        else:
            am=re.search(r'alt="([^"]*)"',tag,re.I)
            if am and am.group(1).strip()=="" : img_no_alt[f]+=1
        if not (re.search(r'\bwidth=',tag,re.I) and re.search(r'\bheight=',tag,re.I)):
            img_no_dim[f]+=1
        sm=re.search(r'\bsrc="([^"]+)"',tag,re.I)
        if sm:
            ex=img_exists(sm.group(1))
            if ex is False: img_broken[f].append(sm.group(1))

    # head essentials
    if 'name="viewport"' not in h: no_viewport.append(u)
    if not re.search(r'<meta[^>]*charset',h,re.I): no_charset.append(u)
    if not re.search(r'<html[^>]*\blang=',h,re.I): no_lang.append(u)

print(f"проверено файлов: {checked}")
print("="*60)
print(f"\n[JSON-LD НЕвалидный] {len(bad_jsonld)}")
for x in bad_jsonld[:15]: print("   ",x)
print(f"\n[JSON-LD типы на сайте] {dict(jsonld_types.most_common())}")

tot_no_alt=sum(img_no_alt.values()); tot_no_dim=sum(img_no_dim.values())
print(f"\n[img без alt] всего {tot_no_alt} на {len(img_no_alt)} стр. Топ:")
for f,n in sorted(img_no_alt.items(),key=lambda kv:-kv[1])[:8]: print(f"    {n:>3}  {f}")
print(f"\n[img без width/height (CLS)] всего {tot_no_dim} на {len(img_no_dim)} стр. Топ:")
for f,n in sorted(img_no_dim.items(),key=lambda kv:-kv[1])[:8]: print(f"    {n:>3}  {f}")
nb=sum(len(v) for v in img_broken.values())
print(f"\n[битые img src (локально нет файла)] всего {nb} на {len(img_broken)} стр.")
for f,v in list(img_broken.items())[:10]: print(f"    {f}: {v[:3]}")

print(f"\n[нет viewport] {len(no_viewport)}"); [print('   ',x) for x in no_viewport[:5]]
print(f"[нет charset] {len(no_charset)}"); [print('   ',x) for x in no_charset[:5]]
print(f"[нет <html lang>] {len(no_lang)}"); [print('   ',x) for x in no_lang[:5]]
