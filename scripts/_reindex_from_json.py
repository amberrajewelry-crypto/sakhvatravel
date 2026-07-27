#!/usr/bin/env python3
"""Дослать в Google Indexing API URL из _pending/google_index_rest.json.
Досланные удаляются из файла, недосланные (quota/err) остаются на следующий прогон.
Запуск: python3 scripts/_reindex_from_json.py"""
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
PENDING = ROOT / "scripts" / "_pending" / "google_index_rest.json"

creds = service_account.Credentials.from_service_account_file(
    str(ROOT / "service-account.json"),
    scopes=["https://www.googleapis.com/auth/indexing"])
svc = build("indexing", "v3", credentials=creds)

urls = json.loads(PENDING.read_text())
ok = quota = err = 0
done = []
for u in urls:
    try:
        svc.urlNotifications().publish(body={"url": u, "type": "URL_UPDATED"}).execute()
        ok += 1; done.append(u); print("OK  ", u)
    except Exception as e:
        s = str(e)
        if "429" in s or "quota" in s.lower() or "RESOURCE_EXHAUSTED" in s:
            quota += 1; print("QUOTA", u)
        else:
            err += 1; print("ERR ", u, s[:100])

remaining = [u for u in urls if u not in done]
PENDING.write_text(json.dumps(remaining, ensure_ascii=False, indent=0))
print(f"\nИтог: OK={ok}, quota={quota}, err={err}, осталось={len(remaining)}")
