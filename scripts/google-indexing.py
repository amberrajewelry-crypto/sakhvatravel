#!/usr/bin/env python3
"""
Submit URLs to Google Indexing API via Service Account.
Usage: python3 scripts/google-indexing.py [--all | --url URL]

Requires:
  - service-account.json in project root
  - pip install google-auth google-auth-httplib2 google-api-python-client
  - Service Account added as Owner in GSC
"""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("Installing dependencies...")
    import subprocess
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "google-auth", "google-auth-httplib2",
        "google-api-python-client"
    ])
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).parent.parent
SA_FILE = PROJECT_ROOT / "service-account.json"
SITEMAP = PROJECT_ROOT / "sitemap.xml"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def get_service():
    if not SA_FILE.exists():
        print(f"ERROR: {SA_FILE} not found")
        print("Download from Google Cloud Console → Service Accounts → Keys")
        sys.exit(1)

    credentials = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES
    )
    return build("indexing", "v3", credentials=credentials)


def submit_url(service, url: str, action: str = "URL_UPDATED"):
    body = {"url": url, "type": action}
    try:
        response = service.urlNotifications().publish(body=body).execute()
        print(f"  OK: {url}")
        return True
    except Exception as e:
        print(f"  FAIL: {url} — {e}")
        return False


def get_sitemap_urls() -> list[str]:
    import glob
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for sm in sorted(glob.glob("sitemap-*.xml")):
        if "index" in sm:
            continue
        tree = ET.parse(sm)
        urls += [loc.text for loc in tree.findall(".//ns:loc", ns)]
    return sorted(set(urls))


def main():
    service = get_service()

    if len(sys.argv) > 1 and sys.argv[1] == "--url":
        url = sys.argv[2]
        print(f"Submitting 1 URL...")
        submit_url(service, url)
        return

    # Default: submit all from sitemap
    urls = get_sitemap_urls()
    print(f"Submitting {len(urls)} URLs from sitemap.xml...")

    ok = 0
    fail = 0
    for url in urls:
        if submit_url(service, url):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} OK, {fail} failed out of {len(urls)}")


if __name__ == "__main__":
    main()
