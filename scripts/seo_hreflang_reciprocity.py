#!/usr/bin/env python3
"""hreflang reciprocity: real bugs only.
For every page collect (locale->url) alternates (order-independent).
Bug types:
  A) alternate URL has no local file (points nowhere)
  B) alternate exists but does NOT list this page back (broken reciprocity)
  C) alternate set mismatch between reciprocal pages (A says {ru,en,ka}, B says {ru,en})
A page with only its own locale + x-default and NO cross-locale alternate is
'untranslated' (reported separately, not a bug)."""
import os, re, glob
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

def alts(f):
    h=open(f,encoding="utf-8",errors="replace").read()
    d={}
    for tag in re.findall(r'<link\b[^>]*>',h,re.I):
        if re.search(r'rel="alternate"',tag,re.I) and 'hreflang=' in tag.lower():
            lm=re.search(r'hreflang="([^"]+)"',tag,re.I); hm=re.search(r'href="([^"]+)"',tag,re.I)
            if lm and hm: d[lm.group(1).lower()]=hm.group(1).rstrip("/")
    return d

pages={}  # url(norm)->(file, alts dict)
for u in urls:
    f=u2f(u)
    if f: pages[u.rstrip("/")]=(f,alts(f))

bugA=[]; bugB=[]; bugC=[]; untranslated=0
for u,(f,d) in pages.items():
    cross={k:v for k,v in d.items() if k not in ("x-default",)}
    # locales other than self that this page points to
    others={k:v for k,v in cross.items() if v.rstrip("/")!=u}
    if not others:
        untranslated+=1; continue
    for loc,tgt in others.items():
        t=tgt.rstrip("/")
        if t not in pages:
            # file may still exist though not in sitemap
            if not u2f(tgt):
                bugA.append(f"{u}  [{loc}]->  {tgt} (нет файла)")
            continue
        td=pages[t][1]
        # reciprocity: target must point back to u
        back={v.rstrip("/") for k,v in td.items()}
        if u not in back:
            bugB.append(f"{u} -> {t} [{loc}] (нет обратной ссылки)")
        else:
            # set equality (ignore x-default)
            s1={k for k in d if k!='x-default'}; s2={k for k in td if k!='x-default'}
            if s1!=s2:
                bugC.append(f"{u}{sorted(s1)}  <>  {t}{sorted(s2)}")

print(f"страниц с hreflang: {len(pages)}  | 'непереведённых' (только своя локаль): {untranslated}")
print(f"\n[A] альтернейт указывает в никуда: {len(bugA)}")
for x in bugA[:15]: print("   ",x)
print(f"\n[B] нет обратной ссылки: {len(bugB)}")
for x in bugB[:15]: print("   ",x)
print(f"\n[C] несовпадение набора локалей у реципрокных страниц: {len(set(bugC))}")
for x in sorted(set(bugC))[:20]: print("   ",x)
