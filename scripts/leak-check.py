"""Prod check: internal files must be 404, site files must stay 200.

Usage: python3 scripts/leak-check.py [base_url]
Exit code 1 if any expectation fails.
"""
import random
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://sakhva-travel.com"
ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PAGES = 30

MUST_BE_CLOSED = [
    "dashboard/backups/bron-20260915-090001.json",
    "dashboard/backups/tours-20260821-090000.json",
    "dashboard/backups/cron.log",
    "dashboard/api/at.js",
    "dashboard/vercel.json",
    "semantic-core-map.csv",
    "SEO-PLAN-leto-2026.md",
    "SEO-AUDIT-2026-05-06.md",
    "telegram-ads-strategy.md",
    "PLAN-hiking-kazbegi.md",
    "DESIGN.md",
    "SPEC-pogoda-cluster.md",
    "_baseline_linking_20260722.json",
    "seo-baseline-20260624.json",
    "seo-baseline-geo-20260820.tsv",
    "_google_pending.txt",
    "skills-lock.json",
    "airtable-dump/_schema.json",
    "ge-locale.bak-20260902-222306.tgz",
    "index.html.bak-count78",
    "main.js.bak_ge_20260724",
    "robots.txt.bak-2026-09-18",
    "sitemap-index.xml.bak-fresh",
    "audit_mobile.py",
    "ffmpeg2pass-0.log",
    "pg-prod.jpeg",
    ".agents/skills/channel-economics-analyzer/channels.example.json",
    ".taskmaster/state.json",
    ".netlify/state.json",
    ".firecrawl/search-comparison.json",
    "sakhva-travel.com-audit/audit-data.json",
    "sakhva-travel-audit/ACTION-PLAN.md",
    "parasite-seo-wave2/dzen-5-ekb.md",
    "parasite-seo-v2/READY-TO-PUBLISH.md",
    "parasite-seo-v3/01-medium-kazbegi-day-trip-EN.md",
    "research/campaign-3groups.csv",
    "schema/kakheti-schema.json",
    "screenshots/mobile-home-snapshot.txt",
    "design-review/desktop-snapshot.txt",
    "test-results/.last-run.json",
    "data/semantic-core.csv",
    "data/semantic-core-sakhva.xlsx",
    "data/competitors_2026-04-22.json",
    "data/yandex-baseline-2026-05-05.json",
    "data/catalog.json.bak-count78",
    "api/reviews.js.bak-2026-09-18",
]

MUST_STAY_OPEN = [
    "",
    "robots.txt",
    "llms.txt",
    "llms-full.txt",
    "en/llms.txt",
    "ge/llms.txt",
    "indexnow-key.txt",
    "323a3fe6d706feaf3b69e9d6919edec3.txt",
    "8d0aedaa48504e51.txt",
    "DE25F3FA51D1F1E934763682A270AF53.txt",
    "a1b2c3d4e5f6g7h8.txt",
    "sakhvatravel3231259ca6306569.txt",
    "sakhvatravela33baf0810a7ac31.txt",
    "yandex_59a834df1510fae1/",
    "yandex-verify/",
    "sitemap-index.xml",
    "sitemap-blog.xml",
    "main.js",
    "data/catalog.json",
    "data/catalog-en.json",
    "data/catalog-ge.json",
    "data/guides.json",
    "data/pogoda-geo.json",
    "dashboard/",
    "links/",
    "prices/",
]


def status(path: str) -> int:
    req = urllib.request.Request(f"{BASE}/{path}", method="HEAD", headers={"User-Agent": "leak-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def sitemap_sample() -> list[str]:
    urls: list[str] = []
    for name in ("sitemap-blog.xml", "sitemap-tours.xml", "sitemap-landing.xml", "sitemap-pages.xml"):
        urls += re.findall(r"<loc>https://sakhva-travel\.com/([^<]*)</loc>", (ROOT / name).read_text())
    random.seed(24)
    return random.sample(urls, min(SAMPLE_PAGES, len(urls)))


def main() -> int:
    open_paths = MUST_STAY_OPEN + sitemap_sample()
    with ThreadPoolExecutor(8) as ex:
        closed = list(zip(MUST_BE_CLOSED, ex.map(status, MUST_BE_CLOSED)))
        opened = list(zip(open_paths, ex.map(status, open_paths)))
    bad = [(p, s) for p, s in closed if s != 404] + [(p, s) for p, s in opened if s != 200]
    print(f"closed ok: {sum(s == 404 for _, s in closed)}/{len(closed)}")
    print(f"open ok:   {sum(s == 200 for _, s in opened)}/{len(opened)}")
    for p, s in bad:
        print(f"  FAIL {s} /{p}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
