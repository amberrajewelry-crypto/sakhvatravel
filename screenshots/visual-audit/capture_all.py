from playwright.sync_api import sync_playwright
import os

OUT = "/Users/vladimir/sakhva-travel/screenshots/visual-audit"

def scroll_and_capture(page, y_offset, filename, wait=500):
    page.evaluate(f"window.scrollTo(0, {y_offset})")
    page.wait_for_timeout(wait)
    page.screenshot(path=os.path.join(OUT, filename), full_page=False)

def capture_sections():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # === DESKTOP 1440x900 ===
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        # Hero (top)
        scroll_and_capture(page, 0, "desktop_hero.png")

        # Get page height and section positions via JS
        positions = page.evaluate("""() => {
            const body = document.body.scrollHeight;
            const sections = {};
            document.querySelectorAll('[id], section, [class]').forEach(el => {
                const id = el.id || el.className;
                if (id) sections[id] = el.getBoundingClientRect().top + window.scrollY;
            });
            return { body, sections };
        }""")
        print(f"Page height: {positions['body']}")

        # Tours section - try scrolling to various likely positions
        scroll_and_capture(page, 900, "desktop_tours.png")
        scroll_and_capture(page, 1800, "desktop_tours2.png")

        # Reviews
        scroll_and_capture(page, 3600, "desktop_reviews.png")
        scroll_and_capture(page, 4500, "desktop_reviews2.png")

        # Footer
        scroll_and_capture(page, positions['body'] - 900, "desktop_footer.png")

        # Full page
        page.screenshot(path=os.path.join(OUT, "desktop_full.png"), full_page=True)
        page.close()

        # === MOBILE 375x812 ===
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        mob_height = page.evaluate("document.body.scrollHeight")
        print(f"Mobile page height: {mob_height}")

        scroll_and_capture(page, 0, "mobile_hero.png")
        scroll_and_capture(page, 800, "mobile_tours.png")
        scroll_and_capture(page, 1600, "mobile_tours2.png")
        scroll_and_capture(page, 3200, "mobile_reviews.png")
        scroll_and_capture(page, 4000, "mobile_reviews2.png")
        scroll_and_capture(page, mob_height - 812, "mobile_footer.png")

        page.screenshot(path=os.path.join(OUT, "mobile_full.png"), full_page=True)
        page.close()

        # === MOBILE TOUR SUBPAGE ===
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto("https://sakhva-travel.com/tour/kazbegi/", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT, "mobile_kazbegi_hero.png"), full_page=False)
        page.screenshot(path=os.path.join(OUT, "mobile_kazbegi_full.png"), full_page=True)
        page.close()

        browser.close()
        print("All screenshots captured.")

if __name__ == "__main__":
    capture_sections()
