from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/mobile_check_apr8"

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Mobile viewport (iPhone 13 Mini approx)
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()

        print("Loading page...")
        page.goto(URL, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # 1. Above-the-fold (375x812) - no scroll
        print("Capturing above-the-fold...")
        page.screenshot(
            path=f"{OUTPUT_DIR}/01_above_fold_375x812.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        # 2. Full page scroll
        print("Capturing full page...")
        page.screenshot(
            path=f"{OUTPUT_DIR}/02_full_page_mobile.png",
            full_page=True
        )

        # 3. Measure key elements
        print("\n=== ELEMENT MEASUREMENTS ===\n")

        # Cookie banner
        cookie_selectors = [
            "[class*='cookie']", "[id*='cookie']",
            "[class*='Cookie']", "[id*='Cookie']",
            "[class*='consent']", "[id*='consent']",
            "[class*='banner']", ".cc-banner",
            "#CybotCookiebotDialog", ".cookieConsent",
            "[data-testid*='cookie']"
        ]
        for sel in cookie_selectors:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    box = el.bounding_box()
                    print(f"COOKIE BANNER [{sel}]: x={box['x']:.0f} y={box['y']:.0f} w={box['width']:.0f} h={box['height']:.0f}")
                    # Try to find buttons inside
                    btns = el.query_selector_all("button, a[href], [role='button']")
                    for i, btn in enumerate(btns):
                        if btn.is_visible():
                            bbox = btn.bounding_box()
                            txt = btn.inner_text().strip()[:40]
                            print(f"  Cookie button[{i}] '{txt}': w={bbox['width']:.0f} h={bbox['height']:.0f}")
            except:
                pass

        # Hero CTAs
        hero_cta_selectors = [
            "section:first-of-type a", ".hero a", ".hero button",
            "[class*='hero'] a", "[class*='hero'] button",
            "header a[href*='tour']", "header button",
            "main > section:first-child a",
            "main > div:first-child a"
        ]
        print("\n--- HERO CTAs ---")
        found_ctas = set()
        for sel in hero_cta_selectors:
            try:
                els = page.query_selector_all(sel)
                for el in els[:3]:
                    if el.is_visible():
                        box = el.bounding_box()
                        txt = el.inner_text().strip()[:40]
                        key = f"{txt}_{box['y']:.0f}"
                        if key not in found_ctas and box['height'] > 0:
                            found_ctas.add(key)
                            tap_ok = "OK" if box['height'] >= 44 else "TOO SMALL"
                            print(f"  CTA '{txt}': w={box['width']:.0f} h={box['height']:.0f} [{tap_ok}]")
            except:
                pass

        # Tour cards "Подробнее" buttons
        print("\n--- TOUR CARD BUTTONS ---")
        tour_btn_selectors = [
            "a[href*='tour']", "a[href*='экскурс']",
            "[class*='card'] a", "[class*='tour'] a",
            "[class*='Card'] a", "article a",
            "a:has-text('Подробнее')", "a:has-text('подробнее')",
            "a:has-text('Узнать')", "button:has-text('Подробнее')"
        ]
        found_tour = set()
        for sel in tour_btn_selectors:
            try:
                els = page.query_selector_all(sel)
                for el in els[:5]:
                    if el.is_visible():
                        box = el.bounding_box()
                        txt = el.inner_text().strip()[:50]
                        key = f"{txt}_{box['y']:.0f}"
                        if key not in found_tour and box['height'] > 0:
                            found_tour.add(key)
                            tap_ok = "OK" if box['height'] >= 44 else f"TOO SMALL (need {44-box['height']:.0f}px more)"
                            print(f"  '{txt}': w={box['width']:.0f} h={box['height']:.0f} [{tap_ok}]")
            except:
                pass

        # Navigation header
        print("\n--- NAVIGATION HEADER ---")
        nav_selectors = ["header", "nav", "[class*='header']", "[class*='Header']", "[class*='nav']"]
        for sel in nav_selectors:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    box = el.bounding_box()
                    # Check if sticky/fixed
                    position = page.evaluate(f"""
                        (() => {{
                            const el = document.querySelector('{sel}');
                            if (!el) return null;
                            return window.getComputedStyle(el).position;
                        }})()
                    """)
                    print(f"  [{sel}]: x={box['x']:.0f} y={box['y']:.0f} w={box['width']:.0f} h={box['height']:.0f} position={position}")
                    break
            except:
                pass

        # Font sizes
        print("\n--- FONT SIZES ---")
        font_checks = [
            ("body", "Base font"),
            ("h1", "H1"),
            ("h2", "H2"),
            ("p", "Paragraph"),
            ("[class*='card'] p", "Card text"),
            ("nav a", "Nav links"),
        ]
        for sel, label in font_checks:
            try:
                size = page.evaluate(f"""
                    (() => {{
                        const el = document.querySelector('{sel}');
                        if (!el) return null;
                        return parseFloat(window.getComputedStyle(el).fontSize);
                    }})()
                """)
                if size:
                    ok = "OK" if size >= 16 else f"SMALL (min 16px)"
                    print(f"  {label}: {size:.1f}px [{ok}]")
            except:
                pass

        # Horizontal overflow check
        print("\n--- OVERFLOW CHECK ---")
        overflow = page.evaluate("""
            (() => {
                const bodyWidth = document.body.scrollWidth;
                const viewportWidth = window.innerWidth;
                const overflowing = [];
                document.querySelectorAll('*').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > viewportWidth + 5) {
                        overflowing.push({
                            tag: el.tagName,
                            class: el.className.toString().substring(0, 50),
                            right: Math.round(rect.right),
                            width: Math.round(rect.width)
                        });
                    }
                });
                return {
                    bodyScrollWidth: bodyWidth,
                    viewportWidth: viewportWidth,
                    hasOverflow: bodyWidth > viewportWidth,
                    overflowingElements: overflowing.slice(0, 10)
                };
            })()
        """)
        print(f"  Body scroll width: {overflow['bodyScrollWidth']}px vs viewport: {overflow['viewportWidth']}px")
        print(f"  Has horizontal overflow: {overflow['hasOverflow']}")
        if overflow['overflowingElements']:
            print("  Overflowing elements:")
            for el in overflow['overflowingElements']:
                print(f"    <{el['tag']} class='{el['class']}'> right={el['right']}px w={el['width']}px")

        # Scroll down and take section screenshots
        print("\nCapturing mid-page sections...")
        page.evaluate("window.scrollTo(0, 812)")
        time.sleep(1)
        page.screenshot(
            path=f"{OUTPUT_DIR}/03_scroll_section2.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        page.evaluate("window.scrollTo(0, 1624)")
        time.sleep(1)
        page.screenshot(
            path=f"{OUTPUT_DIR}/04_scroll_section3.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        page.evaluate("window.scrollTo(0, 2436)")
        time.sleep(1)
        page.screenshot(
            path=f"{OUTPUT_DIR}/05_scroll_section4.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.screenshot(
            path=f"{OUTPUT_DIR}/06_scroll_bottom.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        browser.close()
        print("\nAll screenshots captured.")

if __name__ == "__main__":
    capture_all()
