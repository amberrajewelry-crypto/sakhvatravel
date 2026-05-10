#!/usr/bin/env python3
"""Visual audit script for sakhva-travel.com"""

from playwright.sync_api import sync_playwright
import time

SCREENSHOTS_DIR = "/Users/vladimir/sakhva-travel/screenshots/audit-2026-05-06"

URLS = {
    "home": "https://sakhva-travel.com",
    "tour": "https://sakhva-travel.com/tour/kazbegi/",
    "blog": "https://sakhva-travel.com/blog/",
    "en_home": "https://sakhva-travel.com/en/",
}

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile": {"width": 390, "height": 844},
}

def capture(page, url, output_path, full_page=False):
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(2)
    page.screenshot(path=output_path, full_page=full_page)
    print(f"Saved: {output_path}")

def run():
    with sync_playwright() as p:
        # Desktop screenshots
        browser = p.chromium.launch()
        ctx_desktop = browser.new_context(viewport=VIEWPORTS["desktop"])
        page_d = ctx_desktop.new_page()

        capture(page_d, URLS["home"], f"{SCREENSHOTS_DIR}/desktop_home.png")
        capture(page_d, URLS["tour"], f"{SCREENSHOTS_DIR}/desktop_tour_kazbegi.png")
        capture(page_d, URLS["blog"], f"{SCREENSHOTS_DIR}/desktop_blog.png")

        # Mobile screenshots (above fold)
        ctx_mobile = browser.new_context(
            viewport=VIEWPORTS["mobile"],
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        )
        page_m = ctx_mobile.new_page()

        capture(page_m, URLS["home"], f"{SCREENSHOTS_DIR}/mobile_home_top.png")
        capture(page_m, URLS["tour"], f"{SCREENSHOTS_DIR}/mobile_tour_kazbegi.png")
        capture(page_m, URLS["blog"], f"{SCREENSHOTS_DIR}/mobile_blog.png")
        capture(page_m, URLS["en_home"], f"{SCREENSHOTS_DIR}/mobile_en_home.png")

        # Mobile home - full page scroll
        page_m.goto(URLS["home"], wait_until="networkidle", timeout=30000)
        time.sleep(2)
        page_m.screenshot(path=f"{SCREENSHOTS_DIR}/mobile_home_full.png", full_page=True)
        print(f"Saved: {SCREENSHOTS_DIR}/mobile_home_full.png")

        # Mobile home - scrolled to mid-page (check sticky nav / FAB)
        page_m.goto(URLS["home"], wait_until="networkidle", timeout=30000)
        time.sleep(2)
        page_m.evaluate("window.scrollTo(0, 800)")
        time.sleep(1)
        page_m.screenshot(path=f"{SCREENSHOTS_DIR}/mobile_home_scrolled_800.png")
        print(f"Saved: {SCREENSHOTS_DIR}/mobile_home_scrolled_800.png")

        page_m.evaluate("window.scrollTo(0, 2000)")
        time.sleep(1)
        page_m.screenshot(path=f"{SCREENSHOTS_DIR}/mobile_home_scrolled_2000.png")
        print(f"Saved: {SCREENSHOTS_DIR}/mobile_home_scrolled_2000.png")

        # Mobile tour - full page
        capture(page_m, URLS["tour"], f"{SCREENSHOTS_DIR}/mobile_tour_full.png", full_page=True)

        # Mobile - check for horizontal scroll
        page_m.goto(URLS["home"], wait_until="networkidle", timeout=30000)
        time.sleep(2)
        h_scroll = page_m.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        body_scroll = page_m.evaluate("document.body.scrollWidth > document.body.clientWidth")
        print(f"HORIZONTAL SCROLL CHECK - html: {h_scroll}, body: {body_scroll}")

        # Get page metrics
        metrics = page_m.evaluate("""() => {
            return {
                bodyScrollWidth: document.body.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                viewportWidth: window.innerWidth,
                hasHorizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth
            }
        }""")
        print(f"METRICS: {metrics}")

        browser.close()
        print("Done.")

if __name__ == "__main__":
    run()
