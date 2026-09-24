#!/usr/bin/env python3
"""Add a Google-eligible Product schema to every tour page so Google can show
star ratings + price in search results (TouristTrip alone is not rich-eligible).

Source of truth: the existing TouristTrip block on each page (name, description,
url, image, offers). Rating 4.9/90 matches the visible "★ 4.9/5 · 90+ отзывов".
Idempotent: skips a page that already has a Product block.
"""
import json, re, glob, os

ROOT = os.path.expanduser("~/sakhva-travel")
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

stats = {"files": 0, "added": 0, "skipped_has_product": 0, "no_trip": 0}


def find_trip(html):
    for raw in LD_RE.findall(html):
        try:
            d = json.loads(raw.strip())
        except json.JSONDecodeError:
            continue
        # tour pages: TouristTrip is the top-level object
        if isinstance(d, dict) and d.get("@type") == "TouristTrip":
            return d
    return None


def build_product(trip):
    offers = trip.get("offers", {})
    prod = {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": trip.get("url", "") + "#product",
        "name": trip.get("name", ""),
        "description": trip.get("description", ""),
        "brand": {"@type": "Brand", "name": "Sakhva Travel"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "90",
            "bestRating": "5",
            "worstRating": "1",
        },
    }
    if trip.get("image"):
        prod["image"] = trip["image"]
    if trip.get("url"):
        prod["url"] = trip["url"]
    if offers:
        o = {"@type": "Offer"}
        for k in ("price", "priceCurrency", "availability", "priceValidUntil", "url"):
            if k in offers:
                o[k] = offers[k]
        if "url" not in o and trip.get("url"):
            o["url"] = trip["url"]
        prod["offers"] = o
    return prod


def process(path):
    stats["files"] += 1
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if '"@type":"Product"' in html or '"@type": "Product"' in html:
        stats["skipped_has_product"] += 1
        return
    trip = find_trip(html)
    if not trip:
        stats["no_trip"] += 1
        return

    prod = build_product(trip)
    block = ('<script type="application/ld+json">'
             + json.dumps(prod, ensure_ascii=False, separators=(",", ":"))
             + '</script>')

    # insert right before </head> (fallback: after the TouristTrip script)
    if "</head>" in html:
        html = html.replace("</head>", block + "\n</head>", 1)
    else:
        html = html.replace("</script>", "</script>\n" + block, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    stats["added"] += 1


targets = (sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
           + sorted(glob.glob(os.path.join(ROOT, "en/ekskursiya/*/index.html"))))
for p in targets:
    process(p)

print(json.dumps(stats, indent=2, ensure_ascii=False))
