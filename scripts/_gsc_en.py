#!/usr/bin/env python3
"""GSC analysis for the English segment only."""
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

def q(dims, flt=None, limit=25000):
    body={"startDate":d1,"endDate":d2,"dimensions":dims,"rowLimit":limit,"dataState":"all"}
    if flt: body["dimensionFilterGroups"]=[{"filters":flt}]
    rows=svc.searchanalytics().query(siteUrl=SITE,body=body).execute().get("rows",[])
    return [r for r in rows if "keys" in r]

EN=[{"dimension":"page","operator":"contains","expression":"/en/"}]

# EN totals
pages=q(["page"], EN)
clk=sum(r["clicks"] for r in pages); imp=sum(r["impressions"] for r in pages)
print(f"=== EN-СЕГМЕНТ {d1}..{d2} ===")
print(f"EN-страниц с показами: {len(pages)} | клики={clk:.0f} | показы={imp:.0f} | CTR={clk/imp*100:.2f}%\n")

print("### ТОП-20 EN-СТРАНИЦ по показам ###")
for r in sorted(pages,key=lambda x:-x["impressions"])[:20]:
    u=r["keys"][0].replace("https://sakhva-travel.com","")
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f} CTR={r['ctr']*100:>4.1f}%  {u}")

# EN striking distance: query×page on /en/, pos 4-15
qp=q(["query","page"], EN)
print(f"\n### EN ЗОНА ДОСЯГАЕМОСТИ (поз 4-15, imp>=20) ###")
sd=[r for r in qp if 4<=r["position"]<=15 and r["impressions"]>=20]
for r in sorted(sd,key=lambda x:-x["impressions"])[:30]:
    kw,pg=r["keys"]; pg=pg.replace("https://sakhva-travel.com","")
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f}  «{kw}»  {pg}")

# countries for EN pages
print(f"\n### СТРАНЫ (по EN-страницам) ###")
cc=q(["country"], EN)
for r in sorted(cc,key=lambda x:-x["impressions"])[:12]:
    print(f"  imp={r['impressions']:>5.0f} clk={r['clicks']:>3.0f} pos={r['position']:>4.1f}  {r['keys'][0]}")

# position buckets EN queries
print(f"\n### EN: РАСПРЕДЕЛЕНИЕ (query×page на /en/) ###")
b=Counter(); ib=Counter()
for r in qp:
    p=r["position"]; k="1-3" if p<=3 else "4-10" if p<=10 else "11-20" if p<=20 else "21-50" if p<=50 else "50+"
    b[k]+=1; ib[k]+=r["impressions"]
for k in ["1-3","4-10","11-20","21-50","50+"]:
    print(f"  поз {k:<6}: {b[k]:>4} пар, {ib[k]:>7.0f} показов")
