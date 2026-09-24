#!/usr/bin/env python3
"""Quick GSC Search Analytics pull: pages + queries + totals (last 90 days)."""
import json
from datetime import date, timedelta
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
SA = ROOT / "service-account.json"
SITE = "https://sakhva-travel.com/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

creds = service_account.Credentials.from_service_account_file(str(SA), scopes=SCOPES)
svc = build("searchconsole", "v1", credentials=creds)

end = date.today()
start = end - timedelta(days=90)
d1, d2 = start.isoformat(), end.isoformat()

def q(dims, limit=1000):
    body = {"startDate": d1, "endDate": d2, "dimensions": dims,
            "rowLimit": limit, "dataState": "all"}
    rows = svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])
    return [r for r in rows if "keys" in r]

# Totals
tot = svc.searchanalytics().query(siteUrl=SITE, body={
    "startDate": d1, "endDate": d2, "dataState": "all"}).execute().get("rows", [])
print(f"=== ПЕРИОД {d1} .. {d2} (90 дней) ===")
if tot:
    r = tot[0]
    print(f"ИТОГО: clicks={r['clicks']:.0f}  impressions={r['impressions']:.0f}  "
          f"CTR={r['ctr']*100:.2f}%  pos={r['position']:.1f}")

pages = q(["page"])
print(f"\n=== СТРАНИЦ С ПОКАЗАМИ В ПОИСКЕ: {len(pages)} ===")
print("(это страницы, реально находящиеся в индексе Google и получающие показы)\n")
for r in sorted(pages, key=lambda x: -x["clicks"])[:30]:
    u = r["keys"][0].replace("https://sakhva-travel.com", "")
    print(f"  clk={r['clicks']:>4.0f}  imp={r['impressions']:>6.0f}  "
          f"pos={r['position']:>5.1f}  {u}")

queries = q(["query"])
print(f"\n=== ТОП-25 ЗАПРОСОВ (всего уникальных: {len(queries)}) ===\n")
for r in sorted(queries, key=lambda x: -x["clicks"])[:25]:
    print(f"  clk={r['clicks']:>4.0f}  imp={r['impressions']:>6.0f}  "
          f"pos={r['position']:>5.1f}  {r['keys'][0]}")

# save pages with impressions for cross-check
out = ROOT / "scripts" / "_pages_with_traffic.json"
out.write_text(json.dumps([r["keys"][0] for r in pages], ensure_ascii=False, indent=2))
print(f"\nСохранено: {out}")
