#!/usr/bin/env python3
"""Apply mechanical Google-lift protocol to EN striking-distance pages.

Idempotent: freshness dates, Organization sameAs, Wikidata about-entities.
FAQ expansion and factual fixes are done by hand (semantic, per-page).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TODAY = "2026-07-14"

SAMEAS = (
    '"sameAs":['
    '"https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html",'
    '"https://www.google.com/maps?cid=14112587239859278397",'
    '"https://www.instagram.com/sakhvatravel/"]'
)
WD = {
    "georgia": ('{"@type":"Place","name":"Georgia",'
                '"sameAs":"https://www.wikidata.org/wiki/Q230"}'),
    "tbilisi": ('{"@type":"Place","name":"Tbilisi",'
                '"sameAs":"https://www.wikidata.org/wiki/Q994"}'),
    "kazbegi": ('{"@type":"Place","name":"Kazbegi",'
                '"sameAs":"https://www.wikidata.org/wiki/Q748547"}'),
}

PAGES = [
    "en/blog/georgia-first-time-tips/index.html",
    "en/blog/georgia-visa-2026/index.html",
    "en/blog/tbilisi-rainy-day/index.html",
    "en/blog/botanical-garden-tbilisi/index.html",
    "en/blog/tbilisi-metro-guide/index.html",
    "en/blog/transfer-tbilisi-to-kazbegi/index.html",
]


def about_for(slug: str) -> str:
    """Pick Wikidata entities relevant to the page slug (Georgia always)."""
    ents = [WD["georgia"]]
    if "tbilisi" in slug or "botanical" in slug or "metro" in slug or "rainy" in slug:
        ents.append(WD["tbilisi"])
    if "kazbegi" in slug:
        ents.append(WD["kazbegi"])
    return '"about":[' + ",".join(ents) + "]"


def process(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    orig = html
    changes = []

    # 1. Freshness — meta article:modified_time
    def _mt(m):
        return f'<meta content="{TODAY}" property="article:modified_time"/>'
    html, n = re.subn(
        r'<meta content="20\d\d-\d\d-\d\d" property="article:modified_time"/>',
        _mt, html)
    if n and TODAY not in orig.split('article:modified_time')[0][-60:]:
        changes.append("meta modified_time")

    # 2. Freshness — schema dateModified
    html2, n = re.subn(r'"dateModified":"20\d\d-\d\d-\d\d"',
                       f'"dateModified":"{TODAY}"', html)
    if html2 != html:
        changes.append("schema dateModified")
    html = html2

    # 3. Organization sameAs — inject into publisher logo block if absent
    if '"sameAs"' not in html:
        # match publisher's logo object close: ...width":300,"height":60}}
        pat = (r'("publisher":\{"@type":"Organization".*?"logo":\{[^}]*"height":60\})\}')
        new = re.sub(pat, r'\1,' + SAMEAS + '}', html, count=1)
        if new != html:
            html = new
            changes.append("publisher sameAs")

    # 4. Wikidata about — inject after publisher object if absent
    if '"about"' not in html:
        slug = str(path)
        about = about_for(slug)
        # insert right before "datePublished" of the BlogPosting
        new = re.sub(r'(\},)("datePublished":)', r'\1' + about + r',\2',
                     html, count=1)
        if new != html:
            html = new
            changes.append("about entities")

    if html != orig:
        path.write_text(html, encoding="utf-8")
    return changes


def main():
    for rel in PAGES:
        p = ROOT / rel
        if not p.exists():
            print(f"  MISSING {rel}")
            continue
        ch = process(p)
        tag = ", ".join(ch) if ch else "already up-to-date"
        print(f"  {rel.split('/')[-2]:32s} -> {tag}")


if __name__ == "__main__":
    main()
