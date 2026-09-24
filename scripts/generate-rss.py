#!/usr/bin/env python3
"""Generate RSS 2.0 feed for sakhva-travel.com from ALL HTML pages."""

import re
import json
from datetime import datetime, timezone
from pathlib import Path
from email.utils import format_datetime
from xml.sax.saxutils import escape

SITE = "https://sakhva-travel.com"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rss.xml"

# Skip non-content / technical pages
SKIP_DIRS = {
    "node_modules", ".vercel", ".git", ".claude", "dashboard",
    "api", "scripts", "data", "css", "js", "images", "fonts",
}
SKIP_PAGES = {
    "yandex-verify", "yandex_59a834df1510fae1",
    "policy", "privacy", "terms", "partner",
}


def category_for(rel_path: str) -> str:
    """Determine RSS category from relative path."""
    if rel_path.startswith("en/blog/"):
        return "Blog (EN)"
    if rel_path.startswith("en/ekskursiya/"):
        return "Tours (EN)"
    if rel_path.startswith("en/"):
        return "Pages (EN)"
    if rel_path.startswith("blog/"):
        return "Блог"
    if rel_path.startswith("ekskursiya/"):
        return "Экскурсии"
    if rel_path.startswith("tury-v-gruziyu"):
        return "Гео-страницы"
    return "Страницы"


def extract_meta(html: str) -> dict:
    """Extract title, description, datePublished, dateModified, image from HTML."""
    meta = {}

    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        meta["title"] = m.group(1).strip()

    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.S)
    if m:
        meta["description"] = m.group(1).strip()

    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html, re.S)
    if m:
        meta["image"] = m.group(1).strip()

    for ld_match in re.finditer(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.S):
        try:
            data = json.loads(ld_match.group(1))
            if isinstance(data, list):
                data = data[0]
            if "datePublished" in data:
                meta["datePublished"] = data["datePublished"]
            if "dateModified" in data:
                meta["dateModified"] = data["dateModified"]
        except (json.JSONDecodeError, IndexError, TypeError):
            pass

    return meta


def parse_date(date_str: str) -> datetime:
    """Parse ISO date string to timezone-aware UTC datetime."""
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
    return dt.replace(tzinfo=timezone.utc)


def collect_items() -> list[dict]:
    """Collect all RSS items from all content directories."""
    items = []

    for index in ROOT.rglob("index.html"):
        # Skip non-content dirs
        rel = index.relative_to(ROOT)
        parts = rel.parts
        if any(p in SKIP_DIRS for p in parts):
            continue

        # rel_path like "blog/aeroport-tbilisi/index.html" -> "blog/aeroport-tbilisi"
        page_dir = index.parent
        rel_dir = str(page_dir.relative_to(ROOT))

        if rel_dir == ".":
            # root index.html -> skip (main page, already linked)
            continue

        # Skip technical pages
        page_name = parts[-2] if len(parts) >= 2 else ""
        if page_name in SKIP_PAGES:
            continue

        html = index.read_text(encoding="utf-8", errors="ignore")
        meta = extract_meta(html)

        if not meta.get("title"):
            continue

        url = f"{SITE}/{rel_dir}/"
        date_str = meta.get("dateModified") or meta.get("datePublished")

        if date_str:
            dt = parse_date(date_str)
        else:
            # No JSON-LD date: use 2026-04-15 (bulk publish date)
            dt = datetime(2026, 4, 15, tzinfo=timezone.utc)

        category = category_for(rel_dir)

        items.append({
            "title": meta["title"],
            "link": url,
            "description": meta.get("description", ""),
            "pubDate": dt,
            "category": category,
            "image": meta.get("image", ""),
        })

    items.sort(key=lambda x: x["pubDate"], reverse=True)
    return items


def build_rss(items: list[dict]) -> str:
    """Build RSS 2.0 XML string."""
    now = format_datetime(datetime.now(timezone.utc))

    xml_items = []
    for item in items:
        pub = format_datetime(item["pubDate"])
        desc = escape(item["description"])
        title = escape(item["title"])

        enclosure = ""
        if item.get("image"):
            enclosure = f'\n      <enclosure url="{escape(item["image"])}" type="image/jpeg" />'

        xml_items.append(f"""    <item>
      <title>{title}</title>
      <link>{item["link"]}</link>
      <description>{desc}</description>
      <pubDate>{pub}</pubDate>
      <guid isPermaLink="true">{item["link"]}</guid>
      <category>{item["category"]}</category>{enclosure}
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Sakhva Travel — Частный гид по Грузии</title>
    <link>{SITE}/</link>
    <description>Блог и экскурсии по Грузии от частного гида Тимура. Маршруты, советы, авторские туры в Тбилиси, Кахетию, Казбеги и всю Грузию.</description>
    <language>ru</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml" />
    <image>
      <url>{SITE}/images/og-main.jpg</url>
      <title>Sakhva Travel</title>
      <link>{SITE}/</link>
    </image>
{chr(10).join(xml_items)}
  </channel>
</rss>
"""


if __name__ == "__main__":
    items = collect_items()
    rss = build_rss(items)
    OUT.write_text(rss, encoding="utf-8")

    # Stats by category
    cats = {}
    for i in items:
        cats[i["category"]] = cats.get(i["category"], 0) + 1
    print(f"RSS generated: {len(items)} items -> {OUT}")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
