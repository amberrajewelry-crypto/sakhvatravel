#!/usr/bin/env python3
"""Add aggregateRating to every TouristTrip schema block.
Rating 4.9 / 90 reviews matches the visible "★ 4.9/5 · 90+ отзывов" text,
so it complies with Google's policy (markup must reflect on-page content).

Targets:
  - index.html  (10 TouristTrip inside @graph)
  - ekskursiya/*/index.html        (RU tours)
  - en/ekskursiya/*/index.html     (EN tours)
"""
import json, re, glob, os

ROOT = os.path.expanduser("~/sakhva-travel")

AGG = {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "90",
    "bestRating": "5",
    "worstRating": "1",
}

LD_RE = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

stats = {"files": 0, "trips_patched": 0, "already": 0, "files_changed": 0}


def patch_obj(obj):
    """Add aggregateRating to a TouristTrip dict if missing. Returns True if changed."""
    if not isinstance(obj, dict):
        return False
    t = obj.get("@type")
    is_trip = t == "TouristTrip" or (isinstance(t, list) and "TouristTrip" in t)
    if is_trip:
        if "aggregateRating" in obj or "review" in obj:
            stats["already"] += 1
            return False
        obj["aggregateRating"] = dict(AGG)
        stats["trips_patched"] += 1
        return True
    return False


def walk(node):
    """Recursively patch any TouristTrip found. Returns True if anything changed."""
    changed = False
    if isinstance(node, dict):
        if patch_obj(node):
            changed = True
        for v in node.values():
            if walk(v):
                changed = True
    elif isinstance(node, list):
        for it in node:
            if walk(it):
                changed = True
    return changed


def process(path):
    stats["files"] += 1
    with open(path, encoding="utf-8") as f:
        html = f.read()
    file_changed = False

    def repl(m):
        nonlocal file_changed
        head, body, tail = m.group(1), m.group(2), m.group(3)
        raw = body.strip()
        if "TouristTrip" not in raw:
            return m.group(0)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)  # leave untouched, never break valid HTML
        if walk(data):
            file_changed = True
            new_body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            return head + new_body + tail
        return m.group(0)

    new_html = LD_RE.sub(repl, html)
    if file_changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        stats["files_changed"] += 1


targets = ([os.path.join(ROOT, "index.html")]
           + sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
           + sorted(glob.glob(os.path.join(ROOT, "en/ekskursiya/*/index.html"))))

for p in targets:
    if os.path.exists(p):
        process(p)

print(json.dumps(stats, indent=2, ensure_ascii=False))
