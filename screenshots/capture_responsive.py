from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"

DEVICES = [
    {"name": "iphone14pro", "width": 390, "height": 844, "label": "iPhone 14 Pro (390×844)"},
    {"name": "iphonese",    "width": 375, "height": 667, "label": "iPhone SE (375×667)"},
    {"name": "android_mid", "width": 360, "height": 800, "label": "Android Mid (360×800)"},
]

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for d in DEVICES:
            page = browser.new_page(
                viewport={"width": d["width"], "height": d["height"]},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
            )

            # --- Hero (first screen, no scroll) ---
            page.goto(URL, wait_until="networkidle", timeout=30000)
            time.sleep(2)

            # Close cookie banner if present
            try:
                page.click("button:has-text('Accept')", timeout=2000)
                time.sleep(0.5)
            except:
                pass
            try:
                page.click("button:has-text('OK')", timeout=1000)
                time.sleep(0.5)
            except:
                pass

            hero_path = f"/Users/vladimir/sakhva-travel/screenshots/resp_{d['name']}_hero.png"
            page.screenshot(path=hero_path, full_page=False)
            print(f"SAVED: {hero_path}")

            # --- Tours section (scroll down) ---
            # Try to scroll to tours section
            scrolled = False
            for selector in ["#tours", ".tours", "[class*='tour']", "section:nth-of-type(2)", "main > section:nth-child(2)"]:
                try:
                    element = page.query_selector(selector)
                    if element:
                        element.scroll_into_view_if_needed()
                        time.sleep(1)
                        scrolled = True
                        break
                except:
                    pass

            if not scrolled:
                # Fallback: scroll to ~1.5 screen heights
                page.evaluate(f"window.scrollTo(0, {d['height'] * 2})")
                time.sleep(1)

            tours_path = f"/Users/vladimir/sakhva-travel/screenshots/resp_{d['name']}_tours.png"
            page.screenshot(path=tours_path, full_page=False)
            print(f"SAVED: {tours_path}")

            page.close()

        browser.close()
    print("ALL DONE")

capture_all()
