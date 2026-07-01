#!/usr/bin/env python3
"""Batch fix schema issues across all tour + blog pages.
Fixes: worstRating, @id, inLanguage, heading h4→h3 in cross-sell widget."""

import json, os, re, glob

ROOT = os.path.expanduser("~/sakhva-travel")

stats = {
    "worstRating": 0,
    "id_added": 0,
    "inLanguage": 0,
    "h4_to_h3": 0,
    "blog_id": 0,
    "updated": 0,
    "total": 0,
}

# === ALL TOUR PAGES (RU + EN) ===
ru_tours = sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
en_tours = sorted(glob.glob(os.path.join(ROOT, "en/ekskursiya/*/index.html")))

for path in ru_tours + en_tours:
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    is_en = "/en/ekskursiya/" in path
    slug = path.split("/ekskursiya/")[1].split("/")[0]
    lang = "en" if is_en else "ru"
    base_url = f"https://sakhva-travel.com/{'en/' if is_en else ''}ekskursiya/{slug}/"

    # 1. worstRating — add after bestRating if missing
    if '"worstRating"' not in html and '"bestRating"' in html:
        html = re.sub(
            r'"bestRating":\s*"5"',
            '"bestRating": "5",\n        "worstRating": "1"',
            html
        )
        # Also handle unquoted variant
        html = re.sub(
            r'"bestRating":\s*5(?![\d.])',
            '"bestRating": 5,\n        "worstRating": 1',
            html
        )
        if '"worstRating"' in html:
            stats["worstRating"] += 1

    # 2. @id for TouristTrip — add after @type if missing
    if '"@type": "TouristTrip"' in html or '"@type":"TouristTrip"' in html:
        # Check if @id already present in TouristTrip block
        tt_match = re.search(r'"@type":\s*"TouristTrip"', html)
        if tt_match:
            # Look backwards for @id in the same JSON block
            block_start = html.rfind('{', 0, tt_match.start())
            block_text = html[block_start:tt_match.end()]
            if '"@id"' not in block_text:
                # Add @id right after @type
                html = html[:tt_match.end()] + f',\n    "@id": "{base_url}#tour"' + html[tt_match.end():]
                stats["id_added"] += 1

    # 3. inLanguage — add to TouristTrip if missing
    if '"inLanguage"' not in html:
        tt_match = re.search(r'"@type":\s*"TouristTrip"', html)
        if tt_match:
            html = html[:tt_match.end()] + f',\n    "inLanguage": "{lang}"' + html[tt_match.end():]
            stats["inLanguage"] += 1

    # 4. Heading h4 → h3 in cross-sell widget (site-wide pattern)
    # Pattern: <h4 class="t-card-title"> in tour card widget
    if '<h4 class="t-card-title">' in html:
        html = html.replace('<h4 class="t-card-title">', '<h3 class="t-card-title">')
        html = html.replace('</h4>', '</h3>')
        stats["h4_to_h3"] += 1

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

# === BLOG PAGES — heading fix + @id for BlogPosting ===
ru_blog = sorted(glob.glob(os.path.join(ROOT, "blog/*/index.html")))
en_blog = sorted(glob.glob(os.path.join(ROOT, "en/blog/*/index.html")))

for path in ru_blog + en_blog:
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    is_en = "/en/blog/" in path
    slug = path.split("/blog/")[1].split("/")[0]
    base_url = f"https://sakhva-travel.com/{'en/' if is_en else ''}blog/{slug}/"

    # BlogPosting @id — add if missing
    bp_match = re.search(r'"@type":\s*"BlogPosting"', html)
    if bp_match:
        block_start = html.rfind('{', 0, bp_match.start())
        block_text = html[block_start:bp_match.end()]
        if '"@id"' not in block_text:
            html = html[:bp_match.end()] + f',\n    "@id": "{base_url}#article"' + html[bp_match.end():]
            stats["blog_id"] += 1

    # Heading h4 → h3 in cross-sell widget
    if '<h4 class="t-card-title">' in html:
        html = html.replace('<h4 class="t-card-title">', '<h3 class="t-card-title">')
        html = html.replace('</h4>', '</h3>')
        stats["h4_to_h3"] += 1

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

# === GEO PAGES — heading fix ===
geo_ru = sorted(glob.glob(os.path.join(ROOT, "tury-v-gruziyu-iz-*/index.html")))
geo_en = sorted(glob.glob(os.path.join(ROOT, "en/tours-from-*/index.html")))

for path in geo_ru + geo_en:
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    if '<h4 class="t-card-title">' in html:
        html = html.replace('<h4 class="t-card-title">', '<h3 class="t-card-title">')
        html = html.replace('</h4>', '</h3>')
        stats["h4_to_h3"] += 1

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

# === ABOUT pages — heading fix ===
for path in [
    os.path.join(ROOT, "about/index.html"),
    os.path.join(ROOT, "en/about/index.html"),
]:
    if not os.path.exists(path):
        continue
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    if '<h4 class="t-card-title">' in html:
        html = html.replace('<h4 class="t-card-title">', '<h3 class="t-card-title">')
        html = html.replace('</h4>', '</h3>')
        stats["h4_to_h3"] += 1

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

print(f"Total pages: {stats['total']}")
print(f"Updated: {stats['updated']}")
print(f"  worstRating added: {stats['worstRating']}")
print(f"  @id (TouristTrip): {stats['id_added']}")
print(f"  inLanguage added: {stats['inLanguage']}")
print(f"  @id (BlogPosting): {stats['blog_id']}")
print(f"  h4→h3 heading fix: {stats['h4_to_h3']}")

# Verify
print("\n=== VERIFICATION ===")
issues = 0
for path in ru_tours + en_tours:
    with open(path, "r") as f:
        h = f.read()
    slug = path.replace(ROOT + "/", "")
    problems = []
    if '"bestRating"' in h and '"worstRating"' not in h:
        problems.append("no worstRating")
    if '"@type": "TouristTrip"' in h or '"@type":"TouristTrip"' in h:
        if '"inLanguage"' not in h:
            problems.append("no inLanguage")
    if problems:
        print(f"  FAIL {slug}: {', '.join(problems)}")
        issues += 1
print(f"Tour issues: {issues}")
