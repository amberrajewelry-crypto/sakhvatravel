#!/usr/bin/env python3
"""Ahrefs-style full-site report built on GSC data (own-site organic engine)."""
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
prev_end = start - timedelta(days=1); prev_start = prev_end - timedelta(days=89)

def q(dims, d1, d2, limit=25000, dim_filters=None):
    body = {"startDate": d1, "endDate": d2, "dimensions": dims,
            "rowLimit": limit, "dataState": "all"}
    if dim_filters: body["dimensionFilterGroups"] = dim_filters
    return [r for r in svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", []) if "keys" in r]

d1, d2 = start.isoformat(), end.isoformat()
p1, p2 = prev_start.isoformat(), prev_end.isoformat()

# ---- TOTALS ----
def totals(d1, d2):
    body={"startDate":d1,"endDate":d2,"dimensions":[],"dataState":"all"}
    r=svc.searchanalytics().query(siteUrl=SITE,body=body).execute().get("rows",[])
    return r[0] if r else {"clicks":0,"impressions":0,"ctr":0,"position":0}
t=totals(d1,d2); tp=totals(p1,p2)
print("="*60)
print(f"AHREFS-STYLE ОБЗОР ДОМЕНА sakhva-travel.com")
print(f"Период: {d1}..{d2} (90 дн)  vs пред. 90 дн")
print("="*60)
def dlt(a,b):
    if not b: return "n/a"
    return f"{(a-b)/b*100:+.0f}%"
print(f"\n▼ ТРАФИК (Google organic, GSC — реальные данные)")
print(f"  Клики:      {t['clicks']:>7.0f}   ({dlt(t['clicks'],tp['clicks'])} к пред.)")
print(f"  Показы:     {t['impressions']:>7.0f}   ({dlt(t['impressions'],tp['impressions'])})")
print(f"  CTR:        {t['ctr']*100:>6.2f}%   (пред {tp['ctr']*100:.2f}%)")
print(f"  Ср.позиция: {t['position']:>6.1f}    (пред {tp['position']:.1f})")

# ---- KEYWORDS by position bucket ----
qs=q(["query"],d1,d2)
buckets=Counter(); imp_b=Counter(); clk_b=Counter()
for r in qs:
    p=r["position"]
    b="1-3" if p<=3 else "4-10" if p<=10 else "11-20" if p<=20 else "21-50" if p<=50 else "50+"
    buckets[b]+=1; imp_b[b]+=r["impressions"]; clk_b[b]+=r["clicks"]
print(f"\n▼ ОРГАНИЧЕСКИЕ КЛЮЧИ: {len(qs)} уникальных запросов")
print(f"  {'позиция':<8}{'запросов':>9}{'показов':>10}{'кликов':>9}")
for b in ["1-3","4-10","11-20","21-50","50+"]:
    print(f"  {b:<8}{buckets[b]:>9}{imp_b[b]:>10.0f}{clk_b[b]:>9.0f}")

# ---- TOP PAGES by clicks ----
pg=q(["page"],d1,d2)
print(f"\n▼ ТОП-СТРАНИЦЫ по кликам (всего страниц с показами: {len(pg)})")
for r in sorted(pg,key=lambda x:-x["clicks"])[:15]:
    u=r["keys"][0].replace("https://sakhva-travel.com","") or "/"
    print(f"  clk={r['clicks']:>4.0f} imp={r['impressions']:>6.0f} pos={r['position']:>4.1f}  {u[:55]}")

# ---- TOP QUERIES by clicks ----
print(f"\n▼ ТОП-ЗАПРОСЫ по кликам")
for r in sorted(qs,key=lambda x:-x["clicks"])[:15]:
    print(f"  clk={r['clicks']:>4.0f} imp={r['impressions']:>6.0f} pos={r['position']:>4.1f}  «{r['keys'][0][:45]}»")

# ---- COUNTRIES ----
co=q(["country"],d1,d2)
print(f"\n▼ ГЕОГРАФИЯ (топ стран по кликам)")
for r in sorted(co,key=lambda x:-x["clicks"])[:8]:
    print(f"  clk={r['clicks']:>4.0f} imp={r['impressions']:>7.0f} ctr={r['ctr']*100:>4.1f}%  {r['keys'][0]}")

# ---- DEVICES ----
dev=q(["device"],d1,d2)
print(f"\n▼ УСТРОЙСТВА")
for r in sorted(dev,key=lambda x:-x["clicks"]):
    print(f"  clk={r['clicks']:>4.0f} imp={r['impressions']:>7.0f} ctr={r['ctr']*100:>4.1f}%  {r['keys'][0]}")

# ---- RU vs EN split (by page path) ----
en_c=en_i=ru_c=ru_i=0
for r in pg:
    u=r["keys"][0]
    if "/en/" in u: en_c+=r["clicks"]; en_i+=r["impressions"]
    else: ru_c+=r["clicks"]; ru_i+=r["impressions"]
print(f"\n▼ RU vs EN (по кликам/показам)")
print(f"  RU: clk={ru_c:.0f} imp={ru_i:.0f}")
print(f"  EN: clk={en_c:.0f} imp={en_i:.0f}")
