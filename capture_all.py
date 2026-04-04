from playwright.sync_api import sync_playwright
import os

screenshots_dir = "/Users/vladimir/sakhva-travel/screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

pages_to_capture = [
    ("https://sakhva-travel.com/", "home_desktop", 1920, 1080),
    ("https://sakhva-travel.com/", "home_mobile", 375, 812),
    ("https://sakhva-travel.com/about/", "about_desktop", 1920, 1080),
    ("https://sakhva-travel.com/about/", "about_mobile", 375, 812),
    ("https://sakhva-travel.com/privacy/", "privacy_desktop", 1920, 1080),
    ("https://sakhva-travel.com/privacy/", "privacy_mobile", 375, 812),
    ("https://sakhva-travel.com/tour/old-tbilisi/", "tour_old_tbilisi_desktop", 1920, 1080),
    ("https://sakhva-travel.com/tour/old-tbilisi/", "tour_old_tbilisi_mobile", 375, 812),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url, name, width, height in pages_to_capture:
        print(f"Capturing {name} ({width}x{height}) from {url}")
        page = browser.new_page(viewport={"width": width, "height": height})
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            # Above-the-fold screenshot
            output_path = f"{screenshots_dir}/{name}_atf.png"
            page.screenshot(path=output_path, full_page=False)
            print(f"  ATF saved: {output_path}")
            # Full page screenshot
            output_path_full = f"{screenshots_dir}/{name}_full.png"
            page.screenshot(path=output_path_full, full_page=True)
            print(f"  Full saved: {output_path_full}")
        except Exception as e:
            print(f"  ERROR: {e}")
        finally:
            page.close()
    browser.close()
    print("All done!")
