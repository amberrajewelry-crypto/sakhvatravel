"""Screenshot and check all sakhva-travel.com pages for prices, layout, errors."""
import json
import re
from playwright.sync_api import sync_playwright

PAGES = [
    {"url": "https://sakhva-travel.com/", "name": "homepage-ru", "expected_prices": []},
    {"url": "https://sakhva-travel.com/tour/mtskheta/", "name": "tour-mtskheta", "expected_prices": ["90"]},
    {"url": "https://sakhva-travel.com/tour/kazbegi/", "name": "tour-kazbegi", "expected_prices": ["245"]},
    {"url": "https://sakhva-travel.com/tour/old-tbilisi/", "name": "tour-old-tbilisi", "expected_prices": ["165"]},
    {"url": "https://sakhva-travel.com/tour/kakheti/", "name": "tour-kakheti", "expected_prices": ["195"]},
    {"url": "https://sakhva-travel.com/tour/night-tbilisi/", "name": "tour-night-tbilisi", "expected_prices": ["110"]},
    {"url": "https://sakhva-travel.com/tour/dinner/", "name": "tour-dinner", "expected_prices": ["250"]},
    {"url": "https://sakhva-travel.com/tour/slow-travel/", "name": "tour-slow-travel", "expected_prices": ["700"]},
    {"url": "https://sakhva-travel.com/en/", "name": "homepage-en", "expected_prices": []},
    {"url": "https://sakhva-travel.com/en/tour/kazbegi/", "name": "tour-kazbegi-en", "expected_prices": ["245"]},
]

OLD_PRICES = ["40", "71", "83", "86", "100", "128", "185", "196", "424"]
OUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/price-check"

VIEWPORTS = [
    {"name": "desktop", "width": 1440, "height": 900},
    {"name": "mobile", "width": 375, "height": 812},
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    for pg in PAGES:
        row = {"page": pg["name"], "url": pg["url"]}

        for vp in VIEWPORTS:
            console_errors = []
            console_warnings = []

            context = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)" if vp["name"] == "mobile" else None,
            )
            page = context.new_page()

            def on_console(msg):
                if msg.type == "error":
                    console_errors.append(msg.text)
                elif msg.type == "warning":
                    console_warnings.append(msg.text)

            page.on("console", on_console)

            try:
                page.goto(pg["url"], wait_until="networkidle", timeout=30000)
            except Exception as e:
                row[f"{vp['name']}_error"] = str(e)
                context.close()
                continue

            # Above-the-fold screenshot
            path_atf = f"{OUT_DIR}/{pg['name']}_{vp['name']}_above-fold.png"
            page.screenshot(path=path_atf, full_page=False)

            # Full page screenshot
            path_full = f"{OUT_DIR}/{pg['name']}_{vp['name']}_full.png"
            page.screenshot(path=path_full, full_page=True)

            # Get page text for price checking
            body_text = page.inner_text("body")

            # Check prices
            found_prices = re.findall(r'₾\s*(\d+)', body_text)
            found_old = [p for p in found_prices if p in OLD_PRICES]

            expected_ok = all(ep in found_prices for ep in pg["expected_prices"])
            missing_expected = [ep for ep in pg["expected_prices"] if ep not in found_prices]

            row[f"{vp['name']}_prices_found"] = list(set(found_prices))
            row[f"{vp['name']}_old_prices"] = found_old if found_old else "none"
            row[f"{vp['name']}_expected_ok"] = expected_ok
            row[f"{vp['name']}_missing_prices"] = missing_expected if missing_expected else "none"

            # Check broken images
            broken_imgs = page.evaluate("""() => {
                const imgs = document.querySelectorAll('img');
                const broken = [];
                imgs.forEach(img => {
                    if (!img.complete || img.naturalWidth === 0) {
                        broken.push(img.src || img.getAttribute('data-src') || 'unknown');
                    }
                });
                return broken;
            }""")
            row[f"{vp['name']}_broken_imgs"] = broken_imgs if broken_imgs else "none"

            # Check CTA buttons (WhatsApp/Telegram)
            cta_wa = page.query_selector_all('a[href*="wa.me"], a[href*="whatsapp"], a[href*="api.whatsapp"]')
            cta_tg = page.query_selector_all('a[href*="t.me"], a[href*="telegram"]')
            row[f"{vp['name']}_cta_whatsapp"] = len(cta_wa)
            row[f"{vp['name']}_cta_telegram"] = len(cta_tg)

            # Check horizontal scroll on mobile
            if vp["name"] == "mobile":
                has_hscroll = page.evaluate("""() => {
                    return document.documentElement.scrollWidth > document.documentElement.clientWidth;
                }""")
                row["mobile_hscroll"] = has_hscroll

                # Check hamburger menu
                hamburger = page.query_selector('.hamburger, .menu-toggle, .mobile-menu-btn, [class*="burger"], [class*="mobile-menu"], button[aria-label*="menu"], button[aria-label*="Menu"], .navbar-toggler, #mobile-menu-toggle')
                row["mobile_hamburger_exists"] = hamburger is not None
                if hamburger:
                    try:
                        hamburger.click()
                        page.wait_for_timeout(500)
                        # Check if menu appeared
                        nav_visible = page.evaluate("""() => {
                            const nav = document.querySelector('nav, .mobile-nav, .nav-menu, [class*="mobile-nav"], [class*="nav-links"]');
                            if (!nav) return 'no nav found';
                            const style = window.getComputedStyle(nav);
                            return style.display !== 'none' && style.visibility !== 'hidden';
                        }""")
                        row["mobile_menu_works"] = nav_visible
                    except:
                        row["mobile_menu_works"] = "click failed"

            # Check for overlapping elements (basic check)
            if vp["name"] == "mobile":
                overflow_els = page.evaluate("""() => {
                    const issues = [];
                    const els = document.querySelectorAll('*');
                    const vw = window.innerWidth;
                    for (let i = 0; i < els.length; i++) {
                        const rect = els[i].getBoundingClientRect();
                        if (rect.right > vw + 5 && rect.width > 0 && rect.height > 0) {
                            const tag = els[i].tagName;
                            const cls = els[i].className;
                            if (typeof cls === 'string' && cls.length < 100) {
                                issues.push(`${tag}.${cls.slice(0,50)} overflows by ${Math.round(rect.right - vw)}px`);
                            }
                        }
                        if (issues.length >= 5) break;
                    }
                    return issues;
                }""")
                row["mobile_overflow_elements"] = overflow_els if overflow_els else "none"

            # Console errors
            row[f"{vp['name']}_console_errors"] = console_errors if console_errors else "none"

            # Scroll to footer and take screenshot
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            path_footer = f"{OUT_DIR}/{pg['name']}_{vp['name']}_footer.png"
            page.screenshot(path=path_footer, full_page=False)

            # Check price cards (3 tiers)
            price_cards = page.evaluate("""() => {
                // Look for pricing cards/sections
                const cards = document.querySelectorAll('.price-card, .pricing-card, [class*="price-card"], [class*="pricing"], [class*="tariff"], [class*="package"]');
                if (cards.length > 0) {
                    return Array.from(cards).map(c => ({
                        text: c.innerText.slice(0, 200),
                        visible: c.offsetParent !== null
                    }));
                }
                return [];
            }""")
            row[f"{vp['name']}_price_cards"] = len(price_cards) if price_cards else 0

            context.close()

        results.append(row)

    browser.close()

# Save results
with open(f"{OUT_DIR}/results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("=== RESULTS ===")
for r in results:
    print(f"\n--- {r['page']} ({r['url']}) ---")
    for k, v in r.items():
        if k not in ("page", "url"):
            print(f"  {k}: {v}")
print("\nDone. Screenshots saved to", OUT_DIR)
