from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/mobile"
VIEWPORT = {"width": 390, "height": 844}

sections = [
    {"name": "1_hero", "scroll_y": 0},
    {"name": "2_ticker", "scroll_y": 750},
    {"name": "3_tours_top", "scroll_y": 1300},
    {"name": "4_all_routes_carousel", "scroll_y": 2400},
    {"name": "5_why_us", "scroll_y": 3800},
    {"name": "6_how_to_book", "scroll_y": 5000},
    {"name": "7_reviews", "scroll_y": 6200},
    {"name": "8_blog", "scroll_y": 7400},
    {"name": "9_footer", "scroll_y": 99999},
]

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        print(f"Navigating to {URL}...")
        page.goto(URL, wait_until="networkidle", timeout=60000)
        time.sleep(3)

        # Get total page height
        total_height = page.evaluate("document.body.scrollHeight")
        print(f"Total page height: {total_height}px")

        for section in sections:
            name = section["name"]
            scroll_y = section["scroll_y"]

            # Scroll to position
            if scroll_y == 99999:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            else:
                page.evaluate(f"window.scrollTo(0, {scroll_y})")

            time.sleep(1.5)

            out_path = f"{OUTPUT_DIR}/{name}.png"
            page.screenshot(path=out_path, full_page=False)
            current_y = page.evaluate("window.scrollY")
            print(f"Captured {name} at scrollY={current_y} -> {out_path}")

        # Also capture full page
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
        full_path = f"{OUTPUT_DIR}/full_page.png"
        page.screenshot(path=full_path, full_page=True)
        print(f"Full page captured -> {full_path}")

        browser.close()
        print("Done.")

if __name__ == "__main__":
    capture()
