"""
Visual audit: sakhva-travel.com — desktop 1440x900 + mobile 375x812
Captures hero, tours, reviews, gallery, blog, footer sections.
"""
from playwright.sync_api import sync_playwright
import os

URL = "https://sakhva-travel.com"
OUT = "/Users/vladimir/sakhva-travel/screenshots/audit_2026_05_01"

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile": {"width": 375, "height": 812},
}

# Scroll positions (px from top) for key sections
SCROLL_POSITIONS = {
    "desktop": [
        ("hero", 0),
        ("tours", 1000),
        ("tours_mid", 2000),
        ("guide", 3200),
        ("reviews", 4500),
        ("blog", 5500),
        ("faq", 6500),
        ("footer", 99999),
    ],
    "mobile": [
        ("hero", 0),
        ("tours", 900),
        ("tours_mid", 1800),
        ("guide", 3000),
        ("reviews", 4200),
        ("blog", 5500),
        ("faq", 7000),
        ("footer", 99999),
    ],
}

def run():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, vp in VIEWPORTS.items():
            scale = 2 if vp_name == "mobile" else 1
            page = browser.new_page(
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=scale,
            )
            page.goto(URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            # Full page
            page.screenshot(
                path=os.path.join(OUT, f"{vp_name}_full.png"),
                full_page=True,
            )
            print(f"[OK] {vp_name}_full.png")

            # Scroll-based sections
            for name, y in SCROLL_POSITIONS[vp_name]:
                if y == 99999:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                else:
                    page.evaluate(f"window.scrollTo(0, {y})")
                page.wait_for_timeout(800)
                page.screenshot(
                    path=os.path.join(OUT, f"{vp_name}_{name}.png"),
                    full_page=False,
                )
                print(f"[OK] {vp_name}_{name}.png")

            # Mobile: check hamburger menu
            if vp_name == "mobile":
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(500)
                burger = page.locator('.hamburger, .burger, .menu-toggle, [class*="burger"], [class*="menu-btn"], button[aria-label*="menu"], .nav-toggle')
                if burger.count() > 0 and burger.first.is_visible():
                    burger.first.click()
                    page.wait_for_timeout(800)
                    page.screenshot(
                        path=os.path.join(OUT, f"{vp_name}_menu_open.png"),
                        full_page=False,
                    )
                    print(f"[OK] {vp_name}_menu_open.png")
                else:
                    print(f"[INFO] No burger menu found")

            # Collect page metrics
            metrics = page.evaluate("""() => {
                const body = document.body;
                const h1 = document.querySelector('h1');
                const ctas = document.querySelectorAll('a[href*="whatsapp"], a[href*="wa.me"], .cta-btn, [class*="book"], [class*="cta"]');
                const imgs = document.querySelectorAll('img');
                const brokenImgs = [...imgs].filter(i => !i.complete || i.naturalWidth === 0);
                const hScroll = body.scrollWidth > window.innerWidth;
                return {
                    title: document.title,
                    h1Text: h1 ? h1.textContent.trim() : null,
                    h1Rect: h1 ? h1.getBoundingClientRect() : null,
                    ctaCount: ctas.length,
                    ctaTexts: [...ctas].slice(0, 5).map(c => ({text: c.textContent.trim().substring(0,50), rect: c.getBoundingClientRect()})),
                    totalImages: imgs.length,
                    brokenImages: brokenImgs.length,
                    brokenImgSrcs: brokenImgs.map(i => i.src).slice(0, 10),
                    bodyWidth: body.scrollWidth,
                    viewportWidth: window.innerWidth,
                    hasHorizontalScroll: hScroll,
                    pageHeight: body.scrollHeight,
                    fontSize: getComputedStyle(body).fontSize,
                };
            }""")
            print(f"\n=== {vp_name.upper()} METRICS ===")
            for k, v in metrics.items():
                print(f"  {k}: {v}")
            print()

            page.close()
        browser.close()

if __name__ == "__main__":
    run()
