#!/usr/bin/env python3
"""Strict SEO audit of the 15 cluster articles. Read-only."""
import os, re, json, html
from collections import Counter

ROOT = "/Users/vladimir/sakhva-travel"

FILES = [
    ("RU", "perevodchik-i-soprovozhdenie-v-gruzii/index.html"),
    ("RU", "blog/vid-na-zhitelstvo-v-gruzii/index.html"),
    ("RU", "blog/perevod-i-zaverenie-dokumentov-v-gruzii/index.html"),
    ("RU", "blog/registratsiya-kompanii-v-gruzii/index.html"),
    ("RU", "blog/dom-yustitsii-tbilisi/index.html"),
    ("EN", "en/interpreter-and-support-georgia/index.html"),
    ("EN", "en/blog/residence-permit-georgia/index.html"),
    ("EN", "en/blog/document-translation-notary-georgia/index.html"),
    ("EN", "en/blog/company-registration-georgia/index.html"),
    ("EN", "en/blog/public-service-hall-georgia/index.html"),
    ("GE", "ge/interpreter-and-support-georgia/index.html"),
    ("GE", "ge/blog/residence-permit-georgia/index.html"),
    ("GE", "ge/blog/document-translation-notary-georgia/index.html"),
    ("GE", "ge/blog/company-registration-georgia/index.html"),
    ("GE", "ge/blog/public-service-hall-georgia/index.html"),
]

STOP = set("the a an and or of to in for on with is are be by at as from that this you your we our it its их или для что как под над про при все всё они она это того чтобы если так уже еще ещё был была быть есть нет там где когда чем без про да не на по за из до во со об от ко же ли бы то он но и в с у о к а".split())

def visible_text(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S|re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S|re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return html.unescape(h)

def words(t):
    return re.findall(r"[A-Za-zА-Яа-яЁёႠ-ჿ]{2,}", t)

def url_to_file(u):
    u = u.split("#")[0].split("?")[0]
    if not u.startswith("/") or u.startswith("//"):
        return None
    p = u.strip("/")
    cand = os.path.join(ROOT, p, "index.html")
    if os.path.exists(cand):
        return True
    cand2 = os.path.join(ROOT, p)
    if os.path.exists(cand2):
        return True
    return False  # local page that does not resolve

for lang, rel in FILES:
    path = os.path.join(ROOT, rel)
    h = open(path, encoding="utf-8").read()
    body_match = re.search(r"<article.*?</article>", h, flags=re.S|re.I)
    body = body_match.group(0) if body_match else h
    txt = visible_text(body)
    ws = [w.lower() for w in words(txt)]
    wc = len(ws)
    # keyword density: top content word (>=4 chars, not stopword)
    content = [w for w in ws if len(w) >= 4 and w not in STOP]
    top = Counter(content).most_common(3)
    dens = (top[0][1] / wc * 100) if wc and top else 0

    title = re.search(r"<title>(.*?)</title>", h, flags=re.S|re.I)
    title = title.group(1).strip() if title else ""
    # meta description — both attribute orders
    meta = re.search(r'<meta[^>]*name="description"[^>]*>', h, flags=re.I)
    meta = (re.search(r'content="([^"]*)"', meta.group(0)).group(1) if meta and 'content=' in meta.group(0) else "")
    h1 = re.findall(r"<h1[ >]", h)
    h2 = re.findall(r"<h2[ >]", h)
    hreflang = re.findall(r'hreflang="([^"]+)"', h)
    canon = re.search(r'<link[^>]*rel="canonical"[^>]*>', h, flags=re.I)
    canon = (re.search(r'href="([^"]*)"', canon.group(0)).group(1) if canon else "")
    ld_types = re.findall(r'"@type"\s*:\s*"([^"]+)"', h)
    ogm = re.search(r'<meta[^>]*property="og:image"[^>]*>', h, flags=re.I)
    ogimg = (re.search(r'content="([^"]*)"', ogm.group(0)).group(1) if ogm and 'content=' in ogm.group(0) else "")
    og_ok = "n/a"
    if ogimg:
        p = ogimg.split("?")[0].lstrip("/")
        og_ok = "OK" if os.path.exists(os.path.join(ROOT, p)) else "MISSING"
    # internal links
    links = re.findall(r'href="(/[^"]*)"', body)
    broken = sorted({l for l in links if url_to_file(l) is False})
    nlinks = len(set(links))

    print(f"\n=== [{lang}] {rel}")
    print(f"  words(article)={wc}  top={top}  density={dens:.1f}%")
    print(f"  title[{len(title)}]={title[:70]}")
    print(f"  meta[{len(meta)}]  h1={len(h1)}  h2={len(h2)}")
    print(f"  hreflang={hreflang}  canonical={canon}")
    print(f"  ld_types={sorted(set(ld_types))}")
    print(f"  og:image={og_ok} ({ogimg})")
    print(f"  internal_links={nlinks}  broken={broken if broken else 'нет'}")
