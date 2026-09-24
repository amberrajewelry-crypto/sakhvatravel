#!/usr/bin/env python3
"""URL Inspection API: what Google actually sees (crawl time + rich results)."""
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
creds = service_account.Credentials.from_service_account_file(
    str(ROOT / "service-account.json"),
    scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
svc = build("searchconsole", "v1", credentials=creds)
SITE = "https://sakhva-travel.com/"

urls = [
    "https://sakhva-travel.com/ekskursiya/vinniy-marshrut-alazani/",
    "https://sakhva-travel.com/ekskursiya/art-tur-tbilisi/",
    "https://sakhva-travel.com/",
]
for u in urls:
    print("="*70)
    print(u)
    try:
        r = svc.urlInspection().index().inspect(
            body={"inspectionUrl": u, "siteUrl": SITE}).execute()
        res = r.get("inspectionResult", {})
        idx = res.get("indexStatusResult", {})
        print("  verdict:", idx.get("verdict"),
              "| coverage:", idx.get("coverageState"))
        print("  lastCrawl:", idx.get("lastCrawlTime"))
        rich = res.get("richResultsResult", {})
        if rich:
            print("  rich verdict:", rich.get("verdict"))
            for item in rich.get("detectedItems", []):
                t = item.get("richResultType")
                its = item.get("items", [])
                for it in its:
                    iss = it.get("issues", [])
                    bad = [x for x in iss if x.get("severity") == "ERROR"]
                    print(f"    [{t}] {it.get('name','')[:40]} — errors: {len(bad)}")
                    for x in bad[:4]:
                        print("        ERROR:", x.get("issueMessage"))
        else:
            print("  rich: нет данных (Google ещё не оценил rich results)")
    except Exception as e:
        print("  ERR:", str(e)[:120])
