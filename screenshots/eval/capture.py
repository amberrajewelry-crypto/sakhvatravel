from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUT = "/Users/vladimir/sakhva-travel/screenshots/eval"

def capture():
    with sync_playwright() as p:
        # --- DESKTOP ---
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        time.sleep(2)

        # Full desktop page
        page.screenshot(path=f"{OUT}/desktop_full.png", full_page=True)
        print("desktop_full.png saved")

        # Hero (viewport only)
        page.screenshot(path=f"{OUT}/desktop_hero.png", full_page=False)
        print("desktop_hero.png saved")

        # Section: Все туры — scroll to it
        try:
            tours = page.locator("text=Все туры").first
            tours.scroll_into_view_if_needed()
            time.sleep(1)
            page.screenshot(path=f"{OUT}/desktop_tours.png", full_page=False)
            print("desktop_tours.png saved")
        except Exception as e:
            print(f"Tours section not found: {e}")

        # Section: Почему мы
        try:
            why = page.locator("text=Почему").first
            why.scroll_into_view_if_needed()
            time.sleep(1)
            page.screenshot(path=f"{OUT}/desktop_why.png", full_page=False)
            print("desktop_why.png saved")
        except Exception as e:
            print(f"Why section not found: {e}")

        # Footer
        try:
            footer = page.locator("footer").first
            footer.scroll_into_view_if_needed()
            time.sleep(1)
            page.screenshot(path=f"{OUT}/desktop_footer.png", full_page=False)
            print("desktop_footer.png saved")
        except Exception as e:
            print(f"Footer not found: {e}")

        browser.close()

        # --- MOBILE ---
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        time.sleep(2)

        # Full mobile page
        page.screenshot(path=f"{OUT}/mobile_full.png", full_page=True)
        print("mobile_full.png saved")

        # Mobile hero
        page.screenshot(path=f"{OUT}/mobile_hero.png", full_page=False)
        print("mobile_hero.png saved")

        # Mobile tours
        try:
            tours = page.locator("text=Все туры").first
            tours.scroll_into_view_if_needed()
            time.sleep(1)
            page.screenshot(path=f"{OUT}/mobile_tours.png", full_page=False)
            print("mobile_tours.png saved")
        except Exception as e:
            print(f"Mobile tours not found: {e}")

        # Mobile footer
        try:
            footer = page.locator("footer").first
            footer.scroll_into_view_if_needed()
            time.sleep(1)
            page.screenshot(path=f"{OUT}/mobile_footer.png", full_page=False)
            print("mobile_footer.png saved")
        except Exception as e:
            print(f"Mobile footer not found: {e}")

        browser.close()
        print("All screenshots done.")

capture()
