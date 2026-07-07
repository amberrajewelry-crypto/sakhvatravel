#!/usr/bin/env python3
"""Полный технический аудит сайта: JSON-LD, мета, hreflang, canonical, дубли ID, alt."""
import json, re, html
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/Users/vladimir/sakhva-travel")
SKIP_DIRS = ("node_modules", "_schema_dup_backup", "_shadow_backup", "scripts/")
SKIP_FILES = re.compile(r'(google[0-9a-f]+\.html|yandex_[0-9a-f]+\.html|preview-gallery|'
                        r'miralinks-article|tour-cards-video|payment-success|hero3d|'
                        r'_backup|links-preview|test|template)', re.I)
import re as _re
files = [p for p in ROOT.rglob("*.html")
         if not any(d in str(p) for d in SKIP_DIRS)
         and not SKIP_FILES.search(p.name)]

issues = defaultdict(list)
titles = Counter(); descs = Counter()

def rel(p): return str(p.relative_to(ROOT))

for p in files:
    try:
        s = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        issues["read_error"].append(f"{rel(p)}: {e}"); continue
    r = rel(p)

    # --- JSON-LD ---
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', s, re.S|re.I):
        raw = m.group(1).strip()
        if not raw:
            issues["jsonld_empty"].append(r); continue
        try:
            data = json.loads(raw)
        except Exception as e:
            issues["jsonld_invalid"].append(f"{r}: {str(e)[:60]}"); continue
        objs = data if isinstance(data, list) else [data]
        for o in objs:
            if not isinstance(o, dict): continue
            if "@context" not in o and "@graph" not in o:
                issues["jsonld_no_context"].append(f"{r}: {o.get('@type','?')}")
            graph = o.get("@graph", [o])
            for g in (graph if isinstance(graph,list) else [graph]):
                if not isinstance(g,dict): continue
                t = g.get("@type","")
                # пустые/битые значения
                for k,v in g.items():
                    if v in ("", None, "null", "undefined", "{price}", "{year}"):
                        issues["jsonld_empty_field"].append(f"{r}: {t}.{k}={v!r}")
                    if isinstance(v,str) and re.search(r'\{[a-z_]+\}', v):
                        issues["jsonld_placeholder"].append(f"{r}: {t}.{k}={v[:30]!r}")
                # Product без offers/price
                if t=="Product":
                    off=g.get("offers")
                    if not off: issues["product_no_offer"].append(f"{r}")
                # aggregateRating без reviewCount/ratingValue
                if t=="AggregateRating" or "aggregateRating" in g:
                    ar=g.get("aggregateRating",g) if t!="AggregateRating" else g
                    if isinstance(ar,dict) and (not ar.get("ratingValue") or not (ar.get("reviewCount") or ar.get("ratingCount"))):
                        issues["rating_incomplete"].append(f"{r}")

    # --- TITLE ---
    tm = re.search(r'<title[^>]*>(.*?)</title>', s, re.S|re.I)
    if not tm or not tm.group(1).strip():
        issues["no_title"].append(r)
    else:
        t = html.unescape(re.sub(r'\s+',' ',tm.group(1))).strip()
        titles[t]+=1
        L=len(t)
        if L>65: issues["title_long"].append(f"{r}: {L}ch")
        if L<15: issues["title_short"].append(f"{r}: {L}ch «{t}»")

    # --- META DESCRIPTION ---
    dm = re.search(r'<meta[^>]*name=["\']description["\'][^>]*>', s, re.I) or \
         re.search(r'<meta[^>]*content=["\'][^"\']*["\'][^>]*name=["\']description["\']', s, re.I)
    if not dm:
        issues["no_desc"].append(r)
    else:
        cm=re.search(r'content=["\']([^"\']*)["\']', dm.group(0))
        d=html.unescape(cm.group(1)).strip() if cm else ""
        if not d: issues["desc_empty"].append(r)
        else:
            descs[d]+=1
            if len(d)>170: issues["desc_long"].append(f"{r}: {len(d)}ch")

    # --- CANONICAL ---
    cans = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*>', s, re.I)
    if len(cans)>1: issues["canonical_multi"].append(f"{r}: {len(cans)}")
    for c in cans:
        hrefm=re.search(r'href=["\']([^"\']*)["\']', c)
        if not hrefm or not hrefm.group(1).strip(): issues["canonical_empty"].append(r)

    # --- HREFLANG дубли ---
    hl = re.findall(r'hreflang=["\']([^"\']+)["\']', s, re.I)
    hc = Counter(hl)
    for lang,n in hc.items():
        if n>1: issues["hreflang_dup"].append(f"{r}: {lang}×{n}")

    # --- ДУБЛИ ID ---
    ids = re.findall(r'\sid=["\']([^"\']+)["\']', s)
    idc = Counter(ids)
    dups=[i for i,n in idc.items() if n>1]
    if dups: issues["dup_id"].append(f"{r}: {dups[:5]}")

    # --- IMG без alt ---
    imgs = re.findall(r'<img[^>]*>', s, re.I)
    noalt=[i for i in imgs if not re.search(r'\balt=', i, re.I)]
    if noalt: issues["img_no_alt"].append(f"{r}: {len(noalt)}шт")

    # --- битые placeholder в тексте ---
    for ph in re.findall(r'\{(?:price|year|city|region|name)\}', s):
        issues["text_placeholder"].append(f"{r}: {ph}"); break

# дубли title/desc
dup_titles=[(t,n) for t,n in titles.items() if n>1]
dup_descs=[(d,n) for d,n in descs.items() if n>1]

print("="*64)
print("ТЕХНИЧЕСКИЙ АУДИТ САЙТА —", len(files), "HTML")
print("="*64)
order=["read_error","jsonld_invalid","jsonld_empty","jsonld_no_context","jsonld_placeholder",
       "jsonld_empty_field","product_no_offer","rating_incomplete","text_placeholder",
       "no_title","title_long","title_short","no_desc","desc_empty","desc_long",
       "canonical_multi","canonical_empty","hreflang_dup","dup_id","img_no_alt"]
total=0
for k in order:
    v=issues.get(k,[])
    if v:
        total+=len(v)
        print(f"\n⚠ {k}: {len(v)}")
        for x in v[:6]: print(f"    {x}")
        if len(v)>6: print(f"    … ещё {len(v)-6}")
print(f"\n⚠ дубли TITLE: {len(dup_titles)}")
for t,n in sorted(dup_titles,key=lambda x:-x[1])[:6]: print(f"    ×{n}: {t[:60]}")
print(f"⚠ дубли DESCRIPTION: {len(dup_descs)}")
for dsc,n in sorted(dup_descs,key=lambda x:-x[1])[:6]: print(f"    ×{n}: {dsc[:60]}")
print(f"\n{'='*64}\nВСЕГО проблемных пунктов (без дублей мета): {total}")
