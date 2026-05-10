#!/usr/bin/env python3
"""Mobile visual audit script for sakhva-travel.com — iPhone 14 viewport (390x844)."""

from playwright.sync_api import sync_playwright
import os
import time

OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/mobile-audit-2026-05-06"
VIEWPORT = {"width": 390, "height": 844}

PAGES = [
    ("home_ru", "https://sakhva-travel.com/"),
    ("home_en", "https://sakhva-travel.com/en/"),
    ("tour_kazbegi", "https://sakhva-travel.com/tour/kazbegi/"),
    ("blog_kazbegi", "https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/"),
]

SCROLL_POSITIONS = [0, 400, 1200]


def capture_page(page, slug: str, url: str) -> None:
    print(f"\n[CAPTURE] {slug} — {url}")
    page.goto(url, wait_until="networkidle", timeout=30000)
    # Wait for fonts and lazy images to settle
    time.sleep(2)

    # Above-the-fold (scroll=0)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    path = os.path.join(OUTPUT_DIR, f"{slug}_scroll0.png")
    page.screenshot(path=path, full_page=False)
    print(f"  saved: {path}")

    # Scroll 400px
    page.evaluate("window.scrollTo(0, 400)")
    time.sleep(0.8)
    path = os.path.join(OUTPUT_DIR, f"{slug}_scroll400.png")
    page.screenshot(path=path, full_page=False)
    print(f"  saved: {path}")

    # Scroll 1200px
    page.evaluate("window.scrollTo(0, 1200)")
    time.sleep(0.8)
    path = os.path.join(OUTPUT_DIR, f"{slug}_scroll1200.png")
    page.screenshot(path=path, full_page=False)
    print(f"  saved: {path}")

    # Full page
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    path = os.path.join(OUTPUT_DIR, f"{slug}_fullpage.png")
    page.screenshot(path=path, full_page=True)
    print(f"  saved: {path}")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = context.new_page()

        for slug, url in PAGES:
            try:
                capture_page(page, slug, url)
            except Exception as e:
                print(f"  ERROR on {slug}: {e}")

        browser.close()
    print("\n[DONE] All screenshots captured.")


if __name__ == "__main__":
    main()
