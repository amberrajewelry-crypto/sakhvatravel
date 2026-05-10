from playwright.sync_api import sync_playwright
import time

MOBILE_W = 375
MOBILE_H = 812
BASE = '/Users/vladimir/sakhva-travel/screenshots/mobile-sections'

def capture(url, sections, prefix):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': MOBILE_W, 'height': MOBILE_H})
        page.goto(url, wait_until='networkidle', timeout=30000)
        time.sleep(2)
        for name, scroll_y in sections:
            page.evaluate(f'window.scrollTo(0, {scroll_y})')
            time.sleep(0.5)
            path = f'{BASE}/{prefix}_{name}.png'
            page.screenshot(path=path, full_page=False)
            print(f"  {prefix}_{name}.png")
        browser.close()

# FAQ and footer on main
capture('https://sakhva-travel.com', [
    ('24_faq_top', 8462),
    ('25_faq_questions', 8600),
    ('26_prefooter', 9158),
    ('27_footer', 9400),
], 'main')
