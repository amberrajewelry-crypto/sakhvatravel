#!/usr/bin/env python3
"""GSC opportunity analysis: striking-distance, CTR gaps, position buckets."""
from datetime import date, timedelta
from pathlib import Path
from collections import Counter
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
SA = ROOT / "service-account.json"
SITE = "https://sakhva-travel.com/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
creds = service_account.Credentials.from_service_account_file(str(SA), scopes=SCOPES)
svc = build("searchconsole", "v1", credentials=creds)

end = date.today(); start = end - timedelta(days=90)
d1, d2 = start.isoformat(), end.isoformat()

def q(dims, limit=25000):
    body = {"startDate": d1, "endDate": d2, "dimensions": dims,
            "rowLimit": limit, "dataState": "all"}
    rows = svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])
    return [r for r in rows if "keys" in r]

qp = q(["query", "page"])
print(f"=== {d1}..{d2} | пар (запрос×страница): {len(qp)} ===\n")

# 1. STRIKING DISTANCE: позиция 4-15, отсортировано по показам — близко к топу
print("### 1. ЗОНА ДОСЯГАЕМОСТИ (поз. 4–15, max показов) — поднять в топ-3 ###\n")
sd = [r for r in qp if 4 <= r["position"] <= 15 and r["impressions"] >= 30]
for r in sorted(sd, key=lambda x: -x["impressions"])[:30]:
    kw, pg = r["keys"]
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f} CTR={r['ctr']*100:>4.1f}%  «{kw}»  {pg.replace('https://sakhva-travel.com','')}")

# 2. CTR GAP: позиция <=10 (на 1й стр) но CTR заметно ниже ожидаемого, много показов
print("\n### 2. УПУЩЕННЫЙ CTR (топ-10, но мало кликают) — переписать title/description ###\n")
gap = [r for r in qp if r["position"] <= 10 and r["impressions"] >= 80 and r["ctr"] < 0.02]
for r in sorted(gap, key=lambda x: -x["impressions"])[:25]:
    kw, pg = r["keys"]
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f} CTR={r['ctr']*100:>4.1f}%  «{kw}»  {pg.replace('https://sakhva-travel.com','')}")

# 3. HIGH-IMP LOW-POS: много показов, позиция 11-30 — спрос есть, нужна работа над страницей
print("\n### 3. ВЫСОКИЙ СПРОС, НИЗКАЯ ПОЗИЦИЯ (поз. 11–30, max показов) ###\n")
hi = [r for r in qp if 11 <= r["position"] <= 30 and r["impressions"] >= 50]
for r in sorted(hi, key=lambda x: -x["impressions"])[:25]:
    kw, pg = r["keys"]
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f}  «{kw}»  {pg.replace('https://sakhva-travel.com','')}")

# 4. POSITION BUCKETS (по запросам)
print("\n### 4. РАСПРЕДЕЛЕНИЕ ЗАПРОСОВ ПО ПОЗИЦИЯМ ###\n")
queries = q(["query"])
buckets = Counter()
imp_by_bucket = Counter()
for r in queries:
    p = r["position"]
    b = "1-3" if p<=3 else "4-10" if p<=10 else "11-20" if p<=20 else "21-50" if p<=50 else "50+"
    buckets[b]+=1; imp_by_bucket[b]+=r["impressions"]
for b in ["1-3","4-10","11-20","21-50","50+"]:
    print(f"  поз {b:<6} : {buckets[b]:>5} запросов, {imp_by_bucket[b]:>8.0f} показов")
print(f"\n  ВСЕГО уникальных запросов: {len(queries)}")
