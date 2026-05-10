from playwright.sync_api import sync_playwright
import os

OUT = "/Users/vladimir/sakhva-travel/screenshots/visual-audit"

def scroll_and_capture(page, y_offset, filename, wait=500):
    page.evaluate(f"window.scrollTo(0, {y_offset})")
    page.wait_for_timeout(wait)
    page.screenshot(path=os.path.join(OUT, filename), full_page=False)

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop - find reviews and real footer
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        height = page.evaluate("document.body.scrollHeight")
        # Scan through page to find reviews
        scroll_and_capture(page, 2700, "desktop_2700.png")
        scroll_and_capture(page, 4500, "desktop_4500.png")
        scroll_and_capture(page, 5400, "desktop_5400.png")
        scroll_and_capture(page, 6300, "desktop_6300.png")
        scroll_and_capture(page, 7200, "desktop_7200.png")
        scroll_and_capture(page, height - 900, "desktop_bottom.png")
        page.close()

        # Mobile - reviews and footer
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        mob_h = page.evaluate("document.body.scrollHeight")
        scroll_and_capture(page, 4800, "mobile_4800.png")
        scroll_and_capture(page, 5600, "mobile_5600.png")
        scroll_and_capture(page, 6400, "mobile_6400.png")
        scroll_and_capture(page, 7200, "mobile_7200.png")
        scroll_and_capture(page, 8000, "mobile_8000.png")
        scroll_and_capture(page, 8800, "mobile_8800.png")
        scroll_and_capture(page, mob_h - 812, "mobile_bottom.png")
        page.close()

        browser.close()
        print(f"Desktop height: {height}, Mobile height: {mob_h}")
        print("Extra screenshots done.")

if __name__ == "__main__":
    capture()
