from playwright.sync_api import sync_playwright
import os

OUT = "/Users/vladimir/sakhva-travel/screenshots"

def capture_viewports(url, prefix):
    viewports = [
        ("desktop_1440", 1440, 900),
        ("mobile_375", 375, 812),
        ("tablet_768", 768, 1024),
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, w, h in viewports:
            tag = f"{prefix}_{name}"
            print(f"Capturing {tag}...")
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUT, f"{tag}_above_fold.png"), full_page=False)
            page.screenshot(path=os.path.join(OUT, f"{tag}_full.png"), full_page=True)
            page.close()
        browser.close()

os.makedirs(OUT, exist_ok=True)
print("=== RU ===")
capture_viewports("https://sakhva-travel.com", "ru")
print("\nDone!")
