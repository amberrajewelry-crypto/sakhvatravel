#!/usr/bin/env python3
"""/prices/ ×3: one row per catalog tour (price, duration from data/catalog*.json), sorted by price.

Existing rows keep their names; missing tours are appended from the catalog. Idempotent.
Run: python3 scripts/sync-price-list.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = {"ru": ("prices", "", "catalog.json", "от ₾{}"), "en": ("en/prices", "/en", "catalog-en.json", "from ₾{}"),
         "ge": ("ge/prices", "/ge", "catalog-ge.json", "₾{}-დან")}
ROW = re.compile(r'<tr><td><a href="(?:/en|/ge)?(?:/ekskursiya)?/([^/"]+)/">.*?</tr>', re.S)


def main():
    for lang, (page, pre, cfile, fmt) in LANGS.items():
        cat = {e["slug"]: e for e in json.loads((ROOT / "data" / cfile).read_text())["excursions"]}
        f = ROOT / page / "index.html"
        s = f.read_text()
        rows = {m.group(1): m.group(0) for m in ROW.finditer(s) if m.group(1) in cat}
        for slug, e in cat.items():
            url = e["url"] if e["url"].startswith(pre + "/") and pre else pre + e["url"]
            if slug not in rows and (ROOT / url.strip("/") / "index.html").exists():
                rows[slug] = (f'<tr><td><a href="{url}">{e["title"]}</a></td>'
                              f'<td>{fmt.format(e["price"])}</td><td>{e["durationText"]}</td></tr>')
        for slug, r in rows.items():  # price cell always from catalog
            rows[slug] = re.sub(r"(</a></td><td>)[^<]*(</td>)", lambda m: m.group(1) + fmt.format(cat[slug]["price"]) + m.group(2), r, count=1)
        body = "\n".join(rows[k] for k in sorted(rows, key=lambda k: cat[k]["price"]))
        first, last = [m for m in ROW.finditer(s)][0], [m for m in ROW.finditer(s)][-1]
        between = s[first.start():last.end()]
        assert "</table>" not in between and "<table" not in between
        f.write_text(s[:first.start()] + body + s[last.end():])
        print(page, len(rows), "rows; missing pages:", [k for k in cat if k not in rows])


if __name__ == "__main__":
    main()
