#!/usr/bin/env python3
"""Tour-card links (<a href=/ekskursiya/<slug>/>…₾N or N GEL…</a>): N := data/catalog.json price.

Only cards with exactly one ₾ price are touched; SKIP = links reused for different products.
Run: python3 scripts/sync-card-prices.py [--check]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP: set[str] = set()
cat = {e["slug"]: e["price"] for e in json.loads((ROOT / "data/catalog.json").read_text())["excursions"]}
# "₾N" or "N GEL / N лари / N ლარი"
PRICE = re.compile(r"₾\s?(\d{2,4})(?!\d)|(?<!\d)(\d{2,4})\s?(?:GEL|лари|ლარი)")
LINK = re.compile(r'(<a [^>]*href="(?:/en|/ge)?/ekskursiya/([^/"]+)/"[^>]*>)(.*?)(</a>)', re.S)


def fix(m, log):
    slug, body = m.group(2), m.group(3)
    if slug not in cat or slug in SKIP or "<a " in body:
        return m.group(0)
    prices = PRICE.findall(body)
    if len(prices) != 1 or int(prices[0][0] or prices[0][1]) == cat[slug]:
        return m.group(0)
    log.append(f"{slug}:{prices[0][0] or prices[0][1]}->{cat[slug]}")
    body = re.sub(r"₾(\s?)\d{2,4}(?!\d)", rf"₾\g<1>{cat[slug]}", body)
    body = re.sub(r"(?<!\d)\d{2,4}(\s?(?:GEL|лари|ლარი))", rf"{cat[slug]}\g<1>", body)
    return m.group(1) + body + m.group(4)


# Price right after a tour link in the same clause: "Kazbegi</a> (₾175)", "</a> — от ₾175/чел",
# "</a> (2-3 часа, от 100 лари)". Stops at tags, sentence ends and other currencies.
NEAR = re.compile(r'(href="(?:/en|/ge)?/ekskursiya/([^/"]+)/"[^>]*>[^<]{1,80}</a>[^<.$€]{0,70}?)'
                  r'(?:₾\s?(\d{2,4})|(?<!\d)(\d{2,4})(\s?(?:GEL|лари|ლარი)))(?![\d–-]\d)')
# Region/hub cards: <div class="tour-card">…link…<div class="tour-card-price">от ₾N</div>
CARD = re.compile(r'(<div class="tour-card">(?:(?!<div class="tour-card">).)*?'
                  r'href="(?:/en|/ge)?/ekskursiya/([^/"]+)/"(?:(?!<div class="tour-card">).)*?'
                  r'<div class="tour-card-price">[^<₾]*₾\s?)(\d{2,4})(?!\d)', re.S)


FROM = {"ru": ("от ₾{}", ""), "en": ("from ₾{}", ""), "ge": ("₾{}", "-დან")}


def fix_near(m, log, lang):
    slug = m.group(2)
    n = m.group(3) or m.group(4)
    if slug not in cat or slug in SKIP or int(n) == cat[slug]:
        return m.group(0)
    log.append(f"~{slug}:{n}->{cat[slug]}")
    if m.group(3):
        if m.group(1).endswith("("):  # bare "(₾N)" in itineraries gets "from"
            pre, post = FROM[lang]
            return m.group(1) + pre.format(cat[slug]) + post
        return f"{m.group(1)}₾{cat[slug]}"
    return f"{m.group(1)}{cat[slug]}{m.group(5)}"


# Links to the whole catalogue: "all tours — from ₾N" where N = cheapest catalogue price
MIN_PRICE = min(cat.values())
HUB = re.compile(r'(href="/(?:en/|ge/)?(?:ekskursiya|tours-in-georgia|prices)/"[^>]*>[^<]{1,80}</a>'
                 r'[^<.$€]{0,40}?(?:(?:от|from) ₾\s?|₾))(\d{2,4})(?=/|-დან|\s|\.|,|\))')


def fix_hub(m, log):
    if int(m.group(2)) == MIN_PRICE:
        return m.group(0)
    log.append(f"*hub:{m.group(2)}->{MIN_PRICE}")
    return f"{m.group(1)}{MIN_PRICE}"


# Price box on a tour's own page: "от N лари" / "from N GEL" / "N GEL-დან" / "N ლარიდან" / "დან N ლარი"
BOX = re.compile(r'(color:#1A3D2E;margin-bottom:4px">(?:от |from |დან )?)(\d{2,4})( ?(?:лари|GEL|ლარი)(?:-დან|დან)? <span)')


def fix_card(m, log):
    slug = m.group(2)
    if slug not in cat or slug in SKIP or int(m.group(3)) == cat[slug]:
        return m.group(0)
    log.append(f"#{slug}:{m.group(3)}->{cat[slug]}")
    return f"{m.group(1)}{cat[slug]}"


if __name__ == "__main__":
    total = 0
    for f in ROOT.rglob("index.html"):
        rel = f.relative_to(ROOT)
        if rel.parts[0] in ("_archive", "scripts", "node_modules", "partners"):
            continue
        s = f.read_text(errors="ignore")
        log = []
        s2 = LINK.sub(lambda m: fix(m, log), s)
        lang = rel.parts[0] if rel.parts[0] in ("en", "ge") else "ru"
        s2 = NEAR.sub(lambda m: fix_near(m, log, lang), s2)
        s2 = CARD.sub(lambda m: fix_card(m, log), s2)
        s2 = HUB.sub(lambda m: fix_hub(m, log), s2)
        if len(rel.parts) >= 3 and rel.parts[-3] == "ekskursiya" and rel.parts[-2] in cat:
            own = cat[rel.parts[-2]]
            def box(m, own=own, slug=rel.parts[-2]):
                if int(m.group(2)) == own:
                    return m.group(0)
                log.append(f"=box:{slug}:{m.group(2)}->{own}")
                return f"{m.group(1)}{own}{m.group(3)}"
            s2 = BOX.sub(box, s2)
        if log:
            total += len(log)
            print(rel, *log)
            if "--check" not in sys.argv:
                f.write_text(s2)
    print("fixed:", total)
