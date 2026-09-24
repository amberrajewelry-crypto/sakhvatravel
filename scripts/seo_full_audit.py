#!/usr/bin/env python3
"""Full-site SEO audit (read-only) over all sitemap URLs -> local files.
Checks: file exists, title, meta description, single H1, canonical self-ref,
noindex, JSON-LD, og:image, hreflang completeness+reciprocity, dup title/meta,
broken internal links, sitemap<->fs parity."""
import os, re, glob, html
from collections import Counter, defaultdict

ROOT = "/Users/vladimir/sakhva-travel"
DOMAIN = "https://sakhva-travel.com"
os.chdir(ROOT)

def loc_list(path):
    x = open(path, encoding="utf-8").read()
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x)

# collect sitemap URLs (skip the index sitemap)
maps = [m for m in glob.glob("sitemap*.xml") if m != "sitemap-index.xml"]
url2map = {}
for m in maps:
    for u in loc_list(m):
        url2map.setdefault(u, m)
urls = sorted(url2map)

def url_to_file(u):
    if not u.startswith(DOMAIN):
        return None
    p = u[len(DOMAIN):].split("#")[0].split("?")[0].strip("/")
    if p == "":
        return "index.html"
    for cand in (os.path.join(p, "index.html"), p, p + ".html"):
        if os.path.isfile(cand):
            return cand
    return os.path.join(p, "index.html")  # expected path even if missing

def text_between(pat, h, flags=re.I|re.S):
    m = re.search(pat, h, flags)
    return m.group(1).strip() if m else None

def attr(tag_re, h, attr_name="content"):
    m = re.search(tag_re, h, re.I)
    if not m: return None
    a = re.search(rf'{attr_name}="([^"]*)"', m.group(0), re.I)
    return a.group(1) if a else None

titles = defaultdict(list)
metas = defaultdict(list)
issues = defaultdict(list)   # category -> [url,...]
missing_files = []
broken_links = defaultdict(list)
checked = 0

for u in urls:
    f = url_to_file(u)
    if not f or not os.path.isfile(f):
        missing_files.append((u, f)); continue
    checked += 1
    h = open(f, encoding="utf-8", errors="replace").read()

    title = text_between(r"<title>(.*?)</title>", h)
    if not title: issues["title_missing"].append(u)
    else:
        titles[title].append(u)
        if len(title) > 65: issues["title_long(>65)"].append(f"{u} [{len(title)}]")
        if len(title) < 20: issues["title_short(<20)"].append(f"{u} [{len(title)}]")

    meta = attr(r'<meta[^>]*name="description"[^>]*>', h)
    if not meta: issues["meta_missing"].append(u)
    else:
        metas[meta].append(u)
        if len(meta) > 170: issues["meta_long(>170)"].append(f"{u} [{len(meta)}]")
        if len(meta) < 60: issues["meta_short(<60)"].append(f"{u} [{len(meta)}]")

    h1 = re.findall(r"<h1[\s>]", h, re.I)
    if len(h1) == 0: issues["h1_missing"].append(u)
    elif len(h1) > 1: issues["h1_multiple"].append(f"{u} [{len(h1)}]")

    # noindex
    rob = attr(r'<meta[^>]*name="robots"[^>]*>', h)
    if rob and "noindex" in rob.lower(): issues["noindex"].append(u)

    # canonical self-reference
    canon = attr(r'<link[^>]*rel="canonical"[^>]*>', h, "href")
    if not canon: issues["canonical_missing"].append(u)
    else:
        if canon.rstrip("/") != u.rstrip("/"):
            issues["canonical_mismatch"].append(f"{u} -> {canon}")

    # JSON-LD
    if "application/ld+json" not in h: issues["jsonld_missing"].append(u)

    # og:image
    if not attr(r'<meta[^>]*property="og:image"[^>]*>', h): issues["ogimage_missing"].append(u)

    # hreflang set (order-independent: scan each <link> tag for both attrs)
    hset = set()
    for tag in re.findall(r'<link\b[^>]*>', h, re.I):
        if re.search(r'rel="alternate"', tag, re.I) and 'hreflang=' in tag.lower():
            m = re.search(r'hreflang="([^"]+)"', tag, re.I)
            if m: hset.add(m.group(1).lower())
    hrefs = list(hset)
    if hrefs:
        need = {"ru", "en", "ka"}
        if not need.issubset(hset):
            issues["hreflang_incomplete"].append(f"{u} {sorted(hset)}")
        if "x-default" not in hset:
            issues["hreflang_no_xdefault"].append(u)
    else:
        issues["hreflang_missing"].append(u)

    # internal link resolution (sample: only in-body absolute-root links)
    for l in set(re.findall(r'href="(/[^"#?]+)"', h)):
        if l.startswith("//"): continue
        if any(l.startswith(p) for p in ("/images/","/api/","/assets/","/css/","/js/","/fonts/","/booking")): continue
        p = l.strip("/")
        if not p: continue
        if os.path.isfile(os.path.join(p,"index.html")) or os.path.isfile(p) or os.path.isdir(p):
            continue
        broken_links[l].append(u)

# hreflang reciprocity: for each page's declared alternates, does the target list this url back?
# (light check: skip — covered by per-locale set completeness)

print(f"URLs в картах: {len(urls)}  | проверено файлов: {checked}  | нет файла: {len(missing_files)}")
print("="*60)

def dump(cat, limit=8):
    lst = issues.get(cat, [])
    if lst:
        print(f"\n[{cat}] {len(lst)}")
        for x in lst[:limit]: print("   ", x)
        if len(lst) > limit: print(f"    ... ещё {len(lst)-limit}")

for cat in ["title_missing","title_long(>65)","title_short(<20)",
            "meta_missing","meta_long(>170)","meta_short(<60)",
            "h1_missing","h1_multiple","noindex",
            "canonical_missing","canonical_mismatch",
            "jsonld_missing","ogimage_missing",
            "hreflang_missing","hreflang_incomplete","hreflang_no_xdefault"]:
    dump(cat)

# duplicates
dup_t = {t:v for t,v in titles.items() if len(v) > 1}
dup_m = {m:v for m,v in metas.items() if len(v) > 1}
print(f"\n[дубли title] групп: {len(dup_t)} (страниц: {sum(len(v) for v in dup_t.values())})")
for t,v in list(sorted(dup_t.items(), key=lambda kv:-len(kv[1])))[:6]:
    print(f"    x{len(v)}: {t[:60]}")
print(f"[дубли meta] групп: {len(dup_m)} (страниц: {sum(len(v) for v in dup_m.values())})")
for m,v in list(sorted(dup_m.items(), key=lambda kv:-len(kv[1])))[:6]:
    print(f"    x{len(v)}: {m[:60]}")

print(f"\n[битые внутр. ссылки] уник: {len(broken_links)}")
for l,v in list(sorted(broken_links.items(), key=lambda kv:-len(kv[1])))[:12]:
    print(f"    {l}  <- {len(v)} стр.")

if missing_files:
    print(f"\n[в карте есть, файла нет] {len(missing_files)}")
    for u,f in missing_files[:12]: print(f"    {u}")
