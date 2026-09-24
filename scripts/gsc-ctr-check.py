#!/usr/bin/env python3
"""Compare 28d clicks/CTR of rewritten pages vs docs/audit-2026-09-18/ctr-baseline.json.
Run on/after 2026-10-02: python3 scripts/gsc-ctr-check.py"""
import json, datetime as dt, pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://sakhva-travel.com/'
base = json.load(open(ROOT / 'docs/audit-2026-09-18/ctr-baseline.json'))['pages']
c = service_account.Credentials.from_service_account_file(
    ROOT / 'service-account.json', scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
svc = build('searchconsole', 'v1', credentials=c)
end = dt.date.today() - dt.timedelta(days=3); start = end - dt.timedelta(days=27)
rows = svc.searchanalytics().query(siteUrl=SITE, body={
    'startDate': str(start), 'endDate': str(end), 'dimensions': ['page'], 'rowLimit': 25000}).execute().get('rows', [])
now = {}
for r in rows:
    pg = r['keys'][0].replace(SITE.rstrip('/'), '').split('#')[0]
    if pg in base:
        a = now.setdefault(pg, [0, 0]); a[0] += r['clicks']; a[1] += r['impressions']
print(f'{start}..{end} vs baseline 2026-08-19..2026-09-15')
print(f"{'page':48} {'clicks':>12} {'CTR':>14}")
tc0 = tc1 = 0
for pg, (c0, i0) in base.items():
    c1, i1 = now.get(pg, [0, 0]); tc0 += c0; tc1 += c1
    ctr0 = c0 / i0 * 100 if i0 else 0; ctr1 = c1 / i1 * 100 if i1 else 0
    print(f'{pg:48} {c0:5d}->{c1:<5d} {ctr0:5.1f}%->{ctr1:<5.1f}%')
print(f'TOTAL clicks {tc0} -> {tc1} ({(tc1 - tc0) / tc0 * 100 if tc0 else 0:+.0f}%)')
