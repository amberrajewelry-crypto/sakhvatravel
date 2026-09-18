#!/usr/bin/env python3
"""Submit URLs from a pending list to Google Indexing API until quota (429); keep the rest."""
import sys
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
PENDING = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts" / "_gidx_pending.txt"
creds = service_account.Credentials.from_service_account_file(
    str(ROOT / "service-account.json"), scopes=["https://www.googleapis.com/auth/indexing"])
svc = build("indexing", "v3", credentials=creds)
urls = [u.strip() for u in PENDING.read_text().splitlines() if u.strip()]
ok, left, err = 0, [], None
for u in urls:
    if err:
        left.append(u); continue
    try:
        svc.urlNotifications().publish(body={"url": u, "type": "URL_UPDATED"}).execute(); ok += 1
    except Exception as e:  # 429 = daily quota, stop and keep the rest
        err = str(e)[:100]; left.append(u)
PENDING.write_text("\n".join(left))
print(f"submitted {ok}, left {len(left)}, stop: {err}")
