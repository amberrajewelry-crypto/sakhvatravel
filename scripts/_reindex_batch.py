#!/usr/bin/env python3
"""One-shot Indexing API batch for key tour pages (single auth, fast)."""
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
creds = service_account.Credentials.from_service_account_file(
    str(ROOT / "service-account.json"),
    scopes=["https://www.googleapis.com/auth/indexing"])
svc = build("indexing", "v3", credentials=creds)

slugs = [
    "vinniy-marshrut-alazani", "art-tur-tbilisi", "khachapuri-master-klass",
    "ekskursiya-kazbegi-iz-tbilisi", "ekskursiya-tusheti",
]
urls = []
for s in slugs:
    urls.append(f"https://sakhva-travel.com/ekskursiya/{s}/")
    urls.append(f"https://sakhva-travel.com/en/ekskursiya/{s}/")

ok = err = 0
for u in urls:
    try:
        svc.urlNotifications().publish(
            body={"url": u, "type": "URL_UPDATED"}).execute()
        print("OK  ", u)
        ok += 1
    except Exception as e:
        print("ERR ", u, str(e)[:80])
        err += 1
print(f"\n{ok} ok / {err} err")
