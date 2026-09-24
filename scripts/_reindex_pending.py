#!/usr/bin/env python3
"""Дослать в Google Indexing API URL из _google_pending.txt (после сброса дневной квоты).
Запуск: python3 scripts/_reindex_pending.py"""
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
PENDING = ROOT / "scripts" / "_google_pending.txt"

creds = service_account.Credentials.from_service_account_file(
    str(ROOT / "service-account.json"),
    scopes=["https://www.googleapis.com/auth/indexing"])
svc = build("indexing", "v3", credentials=creds)

urls = [u.strip() for u in PENDING.read_text().splitlines() if u.strip()]
ok = quota = err = 0
done = []
for u in urls:
    try:
        svc.urlNotifications().publish(body={"url": u, "type": "URL_UPDATED"}).execute()
        ok += 1; done.append(u)
        print("OK  ", u)
    except Exception as e:
        s = str(e)
        if "429" in s or "quota" in s.lower():
            quota += 1; print("QUOTA", u)
        else:
            err += 1; print("ERR ", u, s[:80])

# оставить в файле только недосланные
remaining = [u for u in urls if u not in done]
PENDING.write_text("\n".join(remaining) + ("\n" if remaining else ""))
print(f"\nИтог: OK={ok}, quota={quota}, err={err}, осталось={len(remaining)}")
