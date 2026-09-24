#!/usr/bin/env python3
"""Honest consolidation of ratings/reviews (per owner decision 2026-09-07).

Rule:
  - Business nodes (TravelAgency/LocalBusiness/Organization/Person): real 4.9/90
    (Google-backed, matches visible "4.9/5 · 90+ отзывов Google"). Added to home
    business node if missing; existing biz ratings normalised to 4.9/90.
  - Product/TouristTrip nodes WITHOUT visible reviews on the page: aggregateRating
    removed (unsupported per-item rating = policy risk / fabrication).
  - Product/TouristTrip nodes WITH visible review-card blocks: reviewCount = number
    of visible cards, ratingValue = avg of visible stars, and Review objects mirror
    the visible cards (schema reflects on-page content).

Usage: python3 scripts/fix-reviews-honest.py [--apply]   (default = dry run)
"""
import re, json, glob, sys, os

ROOT = os.path.expanduser("~/sakhva-travel")
APPLY = "--apply" in sys.argv

BIZ = {"TravelAgency", "LocalBusiness", "Organization", "Person", "TouristInformationCenter"}
PROD = {"Product", "TouristTrip", "Service", "Trip"}
HOME = {"index.html", "en/index.html", "ge/index.html"}
BIZ_RATING = {"ratingValue": 4.9, "reviewCount": 90}
SKIP = ("node_modules", ".venv", "design-", "qa-", "graphify", "_backup", "_template", "scripts/")

LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def types_of(n):
    t = n.get("@type") if isinstance(n, dict) else None
    return set(t) if isinstance(t, list) else ({t} if t else set())


def nodes_of(d):
    if isinstance(d, list):
        return d
    if isinstance(d, dict):
        return d.get("@graph", [d])
    return []


def parse_visible(html):
    revs = []
    for ch in html.split('<div class="review-card">')[1:]:
        seg = ch.split('<div class="review-card">')[0]
        stars = len(re.findall("★", seg.split("</div>")[0]))
        tx = re.search(r'review-text">(.*?)</p>', seg, re.S)
        au = re.search(r'review-author">(.*?)</div>', seg, re.S)
        if not (tx and au):
            continue
        clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
        revs.append({"stars": stars or 5, "text": clean(tx.group(1)), "author": clean(au.group(1))})
    return revs


def review_objs(revs):
    out = []
    for r in revs:
        out.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": r["author"]},
            "reviewRating": {"@type": "Rating", "ratingValue": r["stars"], "bestRating": 5, "worstRating": 1},
            "reviewBody": r["text"],
        })
    return out


def process(path):
    html = open(path, encoding="utf-8").read()
    rel = path[len(ROOT) + 1:] if path.startswith(ROOT) else path
    is_home = rel in HOME
    visible = parse_visible(html)
    nvis = len(visible)
    avg = round(sum(r["stars"] for r in visible) / nvis, 1) if nvis else None
    changes = {"biz_norm": 0, "biz_added": 0, "prod_removed": 0, "prod_fixed": 0, "rev_added": 0}

    def repl(m):
        raw = m.group(2)
        try:
            d = json.loads(raw)
        except Exception:
            return m.group(0)
        dirty = False
        for n in nodes_of(d):
            if not isinstance(n, dict):
                continue
            t = types_of(n)
            if t & BIZ:
                ar = n.get("aggregateRating")
                if ar:
                    if ar.get("ratingValue") != 4.9 or str(ar.get("reviewCount")) != "90":
                        ar["@type"] = "AggregateRating"
                        ar["ratingValue"] = 4.9
                        ar["reviewCount"] = 90
                        ar["bestRating"] = 5
                        ar["worstRating"] = 1
                        dirty = True
                        changes["biz_norm"] += 1
                elif is_home and (t & {"TravelAgency", "LocalBusiness", "Organization"}):
                    n["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": 4.9,
                                            "reviewCount": 90, "bestRating": 5, "worstRating": 1}
                    dirty = True
                    changes["biz_added"] += 1
                # mirror visible reviews onto the node that carries the rating
                if nvis and n.get("aggregateRating") and not n.get("review"):
                    n["review"] = review_objs(visible)
                    dirty = True
                    changes["rev_added"] += 1
            elif t & PROD and (n.get("aggregateRating") or n.get("review")):
                if nvis:
                    n["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": avg,
                                            "reviewCount": nvis, "bestRating": 5, "worstRating": 1}
                    n["review"] = review_objs(visible)
                    dirty = True
                    changes["prod_fixed"] += 1
                else:
                    # no visible reviews on page -> strip BOTH unsupported rating and
                    # schema-only review objects (same fabrication risk)
                    if n.pop("aggregateRating", None) is not None or n.pop("review", None) is not None:
                        dirty = True
                        changes["prod_removed"] += 1
        if not dirty:
            return m.group(0)
        return m.group(1) + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + m.group(3)

    new = LD_RE.sub(repl, html)
    changed = new != html
    if changed and APPLY:
        open(path, "w", encoding="utf-8").write(new)
    return changed, changes


def main():
    tot = {"files": 0, "biz_norm": 0, "biz_added": 0, "prod_removed": 0, "prod_fixed": 0, "rev_added": 0}
    fixed_files = []
    for path in glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True):
        if any(s in path for s in SKIP):
            continue
        changed, ch = process(path)
        if changed:
            tot["files"] += 1
            for k in ch:
                tot[k] += ch[k]
            if ch["prod_fixed"]:
                fixed_files.append(path[len(ROOT) + 1:])
    print(("APPLIED" if APPLY else "DRY-RUN") + " — honest reviews consolidation")
    print(f"  файлов изменено:        {tot['files']}")
    print(f"  biz рейтинг норм.→4.9/90: {tot['biz_norm']}")
    print(f"  biz рейтинг добавлен:    {tot['biz_added']} (только home)")
    print(f"  product рейтинг УДАЛЁН:   {tot['prod_removed']} (без отзывов)")
    print(f"  product рейтинг+Review:   {tot['prod_fixed']} (с видимыми отзывами)")
    print(f"  Review-объекты добавлены: {tot['prod_fixed'] + tot['rev_added']} узлов (product+biz)")
    print("  файлы с Review-объектами (product-ветка):")
    for f in fixed_files:
        print("    " + f)


if __name__ == "__main__":
    main()
