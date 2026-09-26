#!/usr/bin/env python3
"""Tour rows in hub tables: price from data/catalog.json by linked slug, always "from", RUB via NBG rate.

Rows without a tour link (group-size discounts, third-party costs) are left untouched.
Run: python3 scripts/sync-table-prices.py [--check]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUB_PER_GEL = 32.3  # NBG 25.09.2026: 100 RUB = 3.0937 GEL
FMT = {"ru": "от ₾{}", "en": "from ₾{}", "ge": "₾{}-დან"}
PAGES = ["tury-v-gruziyu-s-detmi", "ge/tury-v-gruziyu-s-detmi", "ge/individualnyy-tur-v-gruziyu",
         "ge/ekskursionnye-tury-v-gruziyu", "individualnyy-tur-v-gruziyu", "ekskursionnye-tury-v-gruziyu",
         "tury-v-tbilisi", "en/individualnyy-tur-v-gruziyu", "en/ekskursionnye-tury-v-gruziyu",
         "en/tury-v-gruziyu-s-detmi", "en/tury-v-tbilisi", "ge/tury-v-tbilisi"]
cat = {e["slug"]: e["price"] for e in json.loads((ROOT / "data/catalog.json").read_text())["excursions"]}


def rub(gel):
    return f"{round(gel * RUB_PER_GEL / 50) * 50:,}".replace(",", " ") + " ₽"


def fix_row(lang, row, log):
    m = re.search(r'href="(?:/en|/ge)?/ekskursiya/([^/"]+)/', row)
    if not m or m.group(1) not in cat:
        return row
    p = cat[m.group(1)]
    new, n = re.subn(r"(<td[^>]*>)(?:от |from )?₾ ?\d+(?:-დან)?(</td>)",
                     lambda x: x.group(1) + FMT[lang].format(p) + x.group(2), row, count=1)
    new = re.sub(r"(<td[^>]*>)(?:от )?[\d ]+ ₽(</td>)", lambda x: x.group(1) + "от " + rub(p) + x.group(2), new, count=1)
    if n and new != row:
        log.append(f"{m.group(1)}={p}")
    return new


def main():
    total = 0
    for page in PAGES:
        f = ROOT / page / "index.html"
        if not f.exists():
            continue
        lang = page.split("/")[0] if page.split("/")[0] in ("en", "ge") else "ru"
        s = f.read_text()
        log = []
        s2 = re.sub(r"<tr>.*?</tr>", lambda r: fix_row(lang, r.group(0), log), s, flags=re.S)
        total += len(log)
        print(f"{page}: {len(log)} {' '.join(log)}")
        if s2 != s and "--check" not in sys.argv:
            f.write_text(s2)
    print("rows:", total)


if __name__ == "__main__":
    assert rub(98) == "3 150 ₽" and FMT["ge"].format(80) == "₾80-დან"
    main()
