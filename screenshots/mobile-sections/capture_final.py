"""Capture detailed mobile screenshots of all sections."""
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

# Main page - 12 screenshots covering all sections
main_sections = [
    ('01_hero_top', 0),
    ('02_hero_cta', 400),
    ('03_tours_heading', 812),
    ('04_tours_filters', 920),
    ('05_tours_cards', 1100),
    ('06_why_top', 1986),
    ('07_why_bottom', 2500),
    ('08_how_top', 2988),
    ('09_how_bottom', 3400),
    ('10_guide', 3684),
    ('11_guide_text', 4000),
    ('12_reviews_top', 4380),
    ('13_reviews_cards', 4600),
    ('14_fortune', 5076),
    ('15_included_top', 5553),
    ('16_included_bottom', 5900),
    ('17_blog_top', 6325),
    ('18_blog_cards', 6700),
    ('19_blog_cards2', 7200),
    ('20_faq', 8462),
    ('21_faq_bottom', 8800),
    ('22_prefooter_cta', 9158),
    ('23_footer', 9500),
]

print("=== MAIN PAGE ===")
capture('https://sakhva-travel.com', main_sections, 'main')

# Tour page
tour_sections = [
    ('01_hero', 0),
    ('02_hero_panel', 400),
    ('03_booking_panel', 619),
    ('04_description', 1425),
    ('05_description2', 1800),
    ('06_description3', 2200),
    ('07_program_top', 3287),
    ('08_program_mid', 3700),
    ('09_program_bottom', 4100),
    ('10_included', 4842),
    ('11_who_fits', 5700),
    ('12_best_time', 6533),
    ('13_reviews', 7438),
    ('14_reviews2', 7900),
    ('15_faq', 8875),
    ('16_similar', 9407),
    ('17_cta', 10383),
    ('18_footer', 10700),
]

print("\n=== TOUR PAGE ===")
capture('https://sakhva-travel.com/tour/kazbegi/', tour_sections, 'tour')

# Blog page
blog_sections = [
    ('01_hero', 0),
    ('02_toc', 500),
    ('03_why', 1354),
    ('04_why2', 1800),
    ('05_how_get', 2551),
    ('06_marshrutka', 3096),
    ('07_taxi', 3455),
    ('08_route', 3799),
    ('09_ananuri', 3885),
    ('10_gudauri', 4288),
    ('11_gergeti', 4813),
    ('12_prices', 5879),
    ('13_prices2', 6400),
    ('14_what_take', 7122),
    ('15_best_time', 7794),
    ('16_overnight', 8697),
    ('17_food', 10044),
    ('18_photo', 10864),
    ('19_related', 12189),
    ('20_faq', 12853),
    ('21_footer', 13400),
]

print("\n=== BLOG PAGE ===")
capture('https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/', blog_sections, 'blog')

print("\nDone!")
