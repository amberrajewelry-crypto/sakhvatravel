#!/usr/bin/env python3
"""Дослать URL блога в Google Indexing API (после исчерпания дневной квоты).
Запускается разово по cron на следующий день. Идемпотентен: пишет marker,
повторно за сутки не шлёт.
"""
import re
import subprocess
import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
MARKER = ROOT / "scripts" / ".blog_reindex_done"
LOG = ROOT / "scripts" / "_reindex_blog.log"


def log(msg: str) -> None:
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"{stamp} {msg}"
    print(line)
    with LOG.open("a") as f:
        f.write(line + "\n")


def main() -> None:
    today = datetime.date.today().isoformat()
    if MARKER.exists() and MARKER.read_text().strip() == today:
        log("already done today, skip")
        return

    xml = subprocess.run(
        ["curl", "-sL", "https://sakhva-travel.com/sitemap-blog.xml"],
        capture_output=True, text=True).stdout
    urls = list(dict.fromkeys(re.findall(r"<loc>([^<]+)</loc>", xml)))
    log(f"blog urls: {len(urls)}")

    creds = service_account.Credentials.from_service_account_file(
        str(ROOT / "service-account.json"),
        scopes=["https://www.googleapis.com/auth/indexing"])
    svc = build("indexing", "v3", credentials=creds)

    ok = err = quota = 0
    for u in urls:
        try:
            svc.urlNotifications().publish(
                body={"url": u, "type": "URL_UPDATED"}).execute()
            ok += 1
        except Exception as e:  # noqa: BLE001
            s = str(e)
            if "429" in s or "quota" in s.lower():
                quota += 1
            else:
                err += 1
    log(f"Google Indexing blog: {ok} ok / {err} err / {quota} quota")
    MARKER.write_text(today)


if __name__ == "__main__":
    main()
