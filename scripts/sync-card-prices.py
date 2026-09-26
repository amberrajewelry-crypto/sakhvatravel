#!/usr/bin/env python3
"""Tour-card links (<a href=/ekskursiya/<slug>/>…₾N…</a>): N := data/catalog.json price.

Only cards with exactly one ₾ price are touched; SKIP = links reused for different products.
Run: python3 scripts/sync-card-prices.py [--check]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP: set[str] = set()
cat = {e["slug"]: e["price"] for e in json.loads((ROOT / "data/catalog.json").read_text())["excursions"]}
LINK = re.compile(r'(<a [^>]*href="(?:/en|/ge)?/ekskursiya/([^/"]+)/"[^>]*>)(.*?)(</a>)', re.S)


def fix(m, log):
    slug, body = m.group(2), m.group(3)
    if slug not in cat or slug in SKIP or "<a " in body:
        return m.group(0)
    prices = re.findall(r"₾\s?(\d{2,4})(?!\d)", body)
    if len(prices) != 1 or int(prices[0]) == cat[slug]:
        return m.group(0)
    log.append(f"{slug}:{prices[0]}->{cat[slug]}")
    return m.group(1) + re.sub(r"₾(\s?)\d{2,4}(?!\d)", rf"₾\g<1>{cat[slug]}", body) + m.group(4)


if __name__ == "__main__":
    total = 0
    for f in ROOT.rglob("index.html"):
        rel = f.relative_to(ROOT)
        if rel.parts[0] in ("_archive", "scripts", "node_modules", "partners"):
            continue
        s = f.read_text(errors="ignore")
        log = []
        s2 = LINK.sub(lambda m: fix(m, log), s)
        if log:
            total += len(log)
            print(rel, *log)
            if "--check" not in sys.argv:
                f.write_text(s2)
    print("fixed:", total)
