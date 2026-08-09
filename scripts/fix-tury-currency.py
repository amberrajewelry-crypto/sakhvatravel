#!/usr/bin/env python3
"""C2 fix: JSON-LD priceCurrency RUB -> GEL across hub/geo/index tour pages.

Prices are shown to users in GEL (₾) but JSON-LD Offer/AggregateOffer declared
RUB with stale rouble values -> Google price mismatch. We parse every ld+json
block, and for blocks containing RUB:
  - Product.offers (RUB)   -> GEL price of that tour (from its detail page)
  - AggregateOffer (RUB)   -> GEL; low/high = min/max GEL of the page's tours
Re-serialising the block also drops the duplicate "url" key bug (W1).

GEL map auto-loaded from ekskursiya/<slug>/index.html (source of truth).
Run:  python3 scripts/fix-tury-currency.py [--dry]
"""
import re, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRY = "--dry" in sys.argv
PR = re.compile(r'"price":\s*"(\d+)",\s*"priceCurrency":\s*"GEL"')
BLK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL)


def load_gel():
    m = {}
    for d in (ROOT / "ekskursiya").glob("*/index.html"):
        h = d.read_text(encoding="utf-8")
        hit = PR.search(h)
        if hit:
            m[d.parent.name] = int(hit.group(1))
    return m


GEL = load_gel()
# name-substring fallback for products whose url slug differs from catalog
NAME_FALLBACK = [("риключен", "priklyuchencheskiy-tur-gruziya"),
                 ("пинг-тур", "shopping-tur-tbilisi")]


def slug_for(product):
    dump = json.dumps(product, ensure_ascii=False)
    for m in re.finditer(r'/ekskursiya/([a-z0-9-]+)/', dump):
        s = m.group(1)
        for cand in (s, s + "-iz-tbilisi"):
            if cand in GEL:
                return cand
    name = product.get("name", "")
    for sub, slug in NAME_FALLBACK:
        if sub in name and slug in GEL:
            return slug
    return None


def fix_products(obj, page_prices, unmapped):
    """Walk, set every RUB Offer to its tour's GEL price. Returns nothing."""
    if isinstance(obj, dict):
        off = obj.get("offers")
        if isinstance(off, dict) and off.get("priceCurrency") == "RUB" \
                and off.get("@type") == "Offer":
            slug = slug_for(obj)
            if slug is None:
                unmapped.append(obj.get("name", "?"))
            else:
                off["price"] = str(GEL[slug])
                off["priceCurrency"] = "GEL"
                page_prices.append(GEL[slug])
        for v in obj.values():
            fix_products(v, page_prices, unmapped)
    elif isinstance(obj, list):
        for v in obj:
            fix_products(v, page_prices, unmapped)


def fix_aggregate(obj, lo, hi):
    if isinstance(obj, dict):
        if obj.get("@type") == "AggregateOffer" and obj.get("priceCurrency") == "RUB":
            obj["priceCurrency"] = "GEL"
            obj["lowPrice"] = str(lo)
            obj["highPrice"] = str(hi)
        for v in obj.values():
            fix_aggregate(v, lo, hi)
    elif isinstance(obj, list):
        for v in obj:
            fix_aggregate(v, lo, hi)


def linked_range(html):
    ps = sorted({GEL[s] for s in re.findall(r'/ekskursiya/([a-z0-9-]+)/', html) if s in GEL})
    return (ps[0], ps[-1]) if ps else (98, 595)


def process(path):
    html = path.read_text(encoding="utf-8")
    if not re.search(r'priceCurrency":\s*"RUB"', html):
        return None
    page_prices, unmapped = [], []
    parsed = []           # (open, data_or_none, raw, close)
    for m in BLK.finditer(html):
        raw = m.group(2)
        if '"RUB"' not in raw:
            parsed.append((m.group(1), None, raw, m.group(3)))
            continue
        data = json.loads(raw)          # duplicate keys collapse (fixes W1)
        fix_products(data, page_prices, unmapped)
        parsed.append((m.group(1), data, raw, m.group(3)))
    if unmapped:
        raise SystemExit(f"UNMAPPED in {path.relative_to(ROOT)}: {unmapped}")
    lo, hi = (min(page_prices), max(page_prices)) if page_prices else linked_range(html)
    out, i = [], 0
    for m in BLK.finditer(html):
        op, data, raw, cl = parsed[i]; i += 1
        if data is None:
            new = raw
        else:
            fix_aggregate(data, lo, hi)
            new = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        out.append((m.start(2), m.end(2), new))
    # splice new block bodies back in
    res, prev = [], 0
    for s, e, new in out:
        res.append(html[prev:s]); res.append(new); prev = e
    res.append(html[prev:])
    result = "".join(res)
    assert '"priceCurrency":"RUB"' not in result and '"priceCurrency": "RUB"' not in result, \
        f"RUB left in {path.relative_to(ROOT)}"
    return result, len(page_prices), lo, hi


def main():
    assert len(GEL) > 50, f"GEL map too small ({len(GEL)})"
    files = [f for f in ROOT.rglob("*.html")
             if "backup" not in str(f)
             and re.search(r'priceCurrency":\s*"RUB"', f.read_text(encoding="utf-8"))]
    changed = 0
    for f in sorted(files):
        r = process(f)
        if not r:
            continue
        result, nprod, lo, hi = r
        print(f"{f.relative_to(ROOT)}: products={nprod} range=₾{lo}-{hi}")
        if not DRY:
            f.write_text(result, encoding="utf-8")
        changed += 1
    print(f"\nfiles={changed}{'  [DRY]' if DRY else ''}")


if __name__ == "__main__":
    main()
