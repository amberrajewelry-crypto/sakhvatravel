#!/usr/bin/env python3
"""
Find unindexed URLs via GSC URL Inspection API, then boost them.
Step 1 (this script): inspect all sitemap URLs, write unindexed list to JSON.

Usage:
  python3 scripts/find-unindexed.py            # inspect all, save report
  python3 scripts/find-unindexed.py --test URL # inspect single URL (debug)
"""

import json
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
SA_FILE = ROOT / "service-account.json"
SITE = "https://sakhva-travel.com/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SUBMAPS = ["sitemap-blog.xml", "sitemap-tours.xml",
           "sitemap-landing.xml", "sitemap-pages.xml", "sitemap-pogoda.xml"]
NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# coverageState values that mean "indexed" — everything else is a candidate
INDEXED_STATES = {"Submitted and indexed", "Indexed, not submitted in sitemap"}


def service():
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds)


def collect_urls():
    import re
    urls = set()
    for sm in SUBMAPS:
        p = ROOT / sm
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text):
            urls.add(m.strip())
    return sorted(urls)


def inspect(svc, url):
    body = {"inspectionUrl": url, "siteUrl": SITE, "languageCode": "ru"}
    resp = svc.urlInspection().index().inspect(body=body).execute()
    res = resp.get("inspectionResult", {}).get("indexStatusResult", {})
    return {
        "url": url,
        "verdict": res.get("verdict", "?"),
        "coverageState": res.get("coverageState", "?"),
        "robotsTxtState": res.get("robotsTxtState", "?"),
        "indexingState": res.get("indexingState", "?"),
        "lastCrawl": res.get("lastCrawlTime", ""),
    }


def main():
    svc = service()

    if len(sys.argv) > 2 and sys.argv[1] == "--test":
        print(json.dumps(inspect(svc, sys.argv[2]), ensure_ascii=False, indent=2))
        return

    urls = collect_urls()
    print(f"Inspecting {len(urls)} URLs (10 threads)...\n", flush=True)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading
    lock = threading.Lock()
    rows = []
    unindexed = []
    done = [0]

    def work(url):
        # each thread builds its own service (httplib2 not thread-safe)
        local = service()
        try:
            r = inspect(local, url)
        except Exception as e:
            r = {"url": url, "verdict": "ERROR", "coverageState": str(e)[:80],
                 "robotsTxtState": "?", "indexingState": "?", "lastCrawl": ""}
        with lock:
            done[0] += 1
            rows.append(r)
            indexed = r["verdict"] == "PASS"
            noindex = r["indexingState"] == "BLOCKED_BY_META_TAG"
            if r["verdict"] != "ERROR" and not indexed and not noindex:
                unindexed.append(r)
            flag = "OK " if indexed else (
                "NIDX" if noindex else ("ERR " if r["verdict"] == "ERROR" else ">>> "))
            print(f"[{done[0]}/{len(urls)}] {flag} {r['coverageState']:<42} {url}",
                  flush=True)
        return r

    with ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(work, urls))

    report = ROOT / "scripts" / "_inspection_report.json"
    report.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    boost = ROOT / "scripts" / "_to_boost.json"
    boost.write_text(json.dumps([r["url"] for r in unindexed],
                                 ensure_ascii=False, indent=2))

    # summary by coverageState
    from collections import Counter
    by_state = Counter(r["coverageState"] for r in rows)
    print("\n=== SUMMARY ===")
    for st, n in by_state.most_common():
        print(f"  {n:>4}  {st}")
    print(f"\nTo boost (not indexed, not noindex): {len(unindexed)}")
    print(f"Report: {report}")
    print(f"Boost list: {boost}")


if __name__ == "__main__":
    main()
