#!/usr/bin/env python3
"""
Boost unindexed URLs to Google Indexing API, IndexNow (Bing/Yandex), Yandex Webmaster.
Reads scripts/_to_boost.json (produced by find-unindexed.py).

Usage: python3 scripts/boost-unindexed.py [--limit N]
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).parent.parent
SA_FILE = ROOT / "service-account.json"
BOOST_JSON = ROOT / "scripts" / "_to_boost.json"
INDEXNOW_KEY = "DE25F3FA51D1F1E934763682A270AF53"
YANDEX_HOST = "https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"
YANDEX_DAILY_LIMIT = 140  # quota ~150/day, keep margin


def google_service():
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=["https://www.googleapis.com/auth/indexing"])
    return build("indexing", "v3", credentials=creds)


def yandex_token():
    return subprocess.check_output(
        ["security", "find-generic-password", "-a", subprocess.os.environ["USER"],
         "-s", "yandex-webmaster-token", "-w"]).decode().strip()


def boost_google(svc, url):
    try:
        svc.urlNotifications().publish(
            body={"url": url, "type": "URL_UPDATED"}).execute()
        return True, ""
    except Exception as e:
        return False, str(e)[:80]


def boost_indexnow(urls):
    body = json.dumps({
        "host": "sakhva-travel.com",
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://sakhva-travel.com/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def boost_yandex(token, url):
    body = json.dumps({"url": url}).encode()
    req = urllib.request.Request(
        f"{YANDEX_HOST}/recrawl/queue", data=body,
        headers={"Authorization": f"OAuth {token}",
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "msg": e.read().decode()[:120]}


def main():
    urls = json.loads(BOOST_JSON.read_text())
    if "--limit" in sys.argv:
        n = int(sys.argv[sys.argv.index("--limit") + 1])
        urls = urls[:n]
    print(f"Boosting {len(urls)} URLs\n")

    # 1. Google Indexing API
    svc = google_service()
    g_ok = 0
    print("--- Google Indexing API ---")
    for u in urls:
        ok, err = boost_google(svc, u)
        g_ok += ok
        print(f"  {'OK ' if ok else 'FAIL'} {u}{'' if ok else ' :: ' + err}")
        time.sleep(0.25)
    print(f"Google: {g_ok}/{len(urls)} OK\n")

    # 2. IndexNow (batch, Bing + Yandex)
    print("--- IndexNow (Bing/Yandex) ---")
    code = boost_indexnow(urls)
    print(f"  HTTP {code} (200/202 = accepted)\n")

    # 3. Yandex Webmaster recrawl (rate-limited)
    print("--- Yandex Webmaster recrawl ---")
    tok = yandex_token()
    y_ok = 0
    for u in urls[:YANDEX_DAILY_LIMIT]:
        r = boost_yandex(tok, u)
        ok = "task_id" in r or "error" not in r
        y_ok += ok
        print(f"  {'OK ' if ok else 'ERR'} {u} :: {r}")
        time.sleep(0.4)
    if len(urls) > YANDEX_DAILY_LIMIT:
        print(f"  (skipped {len(urls) - YANDEX_DAILY_LIMIT} — Yandex daily quota)")
    print(f"Yandex: {y_ok} queued\n")

    print("=== DONE ===")


if __name__ == "__main__":
    main()
