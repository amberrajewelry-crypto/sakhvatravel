#!/usr/bin/env python3
"""Insert the 15 cluster URLs into sitemap sub-maps with hreflang. Idempotent."""
import re, pathlib

ROOT = pathlib.Path("/Users/vladimir/sakhva-travel")
BASE = "https://sakhva-travel.com"
LASTMOD = "2026-09-08"

# (ru, en, ge) triples
TRIPLES = [
    ("/perevodchik-i-soprovozhdenie-v-gruzii/", "/en/interpreter-and-support-georgia/", "/ge/interpreter-and-support-georgia/"),
    ("/blog/vid-na-zhitelstvo-v-gruzii/", "/en/blog/residence-permit-georgia/", "/ge/blog/residence-permit-georgia/"),
    ("/blog/perevod-i-zaverenie-dokumentov-v-gruzii/", "/en/blog/document-translation-notary-georgia/", "/ge/blog/document-translation-notary-georgia/"),
    ("/blog/registratsiya-kompanii-v-gruzii/", "/en/blog/company-registration-georgia/", "/ge/blog/company-registration-georgia/"),
    ("/blog/dom-yustitsii-tbilisi/", "/en/blog/public-service-hall-georgia/", "/ge/blog/public-service-hall-georgia/"),
]

def url_block(loc, ru, en, ge):
    return (f"  <url>\n"
            f"    <loc>{BASE}{loc}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            f'    <xhtml:link rel="alternate" hreflang="ru" href="{BASE}{ru}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="ka" href="{BASE}{ge}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ru}"/>\n'
            f"  </url>\n")

def insert(mapfile, blocks):
    p = ROOT / mapfile
    xml = p.read_text(encoding="utf-8")
    added = []
    for loc, block in blocks:
        if f"<loc>{BASE}{loc}</loc>" in xml:
            continue
        xml = xml.replace("</urlset>", block + "</urlset>")
        added.append(loc)
    p.write_text(xml, encoding="utf-8")
    return added

# pillars -> landing; blog -> blog
landing_blocks, blog_blocks = [], []
for ru, en, ge in TRIPLES:
    target = landing_blocks if ("/blog/" not in ru) else blog_blocks
    for u in (ru, en, ge):
        target.append((u, url_block(u, ru, en, ge)))

a1 = insert("sitemap-landing.xml", landing_blocks)
a2 = insert("sitemap-blog.xml", blog_blocks)
print(f"landing +{len(a1)}: {a1}")
print(f"blog +{len(a2)}: {a2}")
