#!/usr/bin/env python3
"""Remove empty BlogPosting microdata wrappers (<article itemscope itemtype=BlogPosting>
with zero itemprop inside) — they cause GSC "Unparsable structured data".
Real markup is already in JSON-LD. Breadcrumb/ListItem microdata is left intact.
Idempotent and safe: only strips the itemscope+itemtype=BlogPosting attribute pair.
"""
import re, glob, os

ROOT = os.path.expanduser("~/sakhva-travel")

# match itemscope (with or without ="") + itemtype=BlogPosting, in any order,
# anywhere inside a tag — remove just those two attributes.
PAT_A = re.compile(
    r'\s+itemscope(?:="")?\s+itemtype="https://schema\.org/BlogPosting"')
PAT_B = re.compile(
    r'\s+itemtype="https://schema\.org/BlogPosting"\s+itemscope(?:="")?')

stats = {"files": 0, "changed": 0, "removed": 0}

files = [f for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True)
         if not any(x in f for x in
                    (".backup", ".base-clean", ".original", "/research/"))]

for p in files:
    stats["files"] += 1
    with open(p, encoding="utf-8") as f:
        html = f.read()
    if "schema.org/BlogPosting" not in html:
        continue
    # only touch pages where the BlogPosting microdata is EMPTY (no itemprop)
    if 'itemprop=' in html and re.search(r'itemprop="(headline|author|datePublished|articleBody|image)"', html):
        # has real microdata props — skip to be safe
        continue
    new, n1 = PAT_A.subn("", html)
    new, n2 = PAT_B.subn("", new)
    total = n1 + n2
    if total:
        with open(p, "w", encoding="utf-8") as f:
            f.write(new)
        stats["changed"] += 1
        stats["removed"] += total

import json
print(json.dumps(stats, indent=2, ensure_ascii=False))
