"""Mobile audit of sakhva-travel.com - iPhone 14 viewport (375x812)"""
import json
from playwright.sync_api import sync_playwright

MOBILE_VP = {"width": 375, "height": 812}
BASE = "https://sakhva-travel.com"
OUT = "/Users/vladimir/sakhva-travel/screenshots/mobile"

TOUR_PAGES = [
    "/tour/kakheti-wine-tour/",
    "/tour/kazbegi-gudauri/",
    "/tour/tbilisi-walking-tour/",
]
BLOG_PAGES = [
    "/blog/tbilisi-za-3-dnya/",
    "/blog/kazbegi-iz-tbilisi-2026/",
    "/blog/gruzinskoe-vino-gid/",
]

def run():
    console_errors = []
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport=MOBILE_VP,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            device_scale_factor=3,
        )
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append({
            "type": msg.type,
            "text": msg.text,
            "url": page.url
        }) if msg.type in ("error", "warning") else None)

        page.on("pageerror", lambda err: console_errors.append({
            "type": "pageerror",
            "text": str(err),
            "url": page.url
        }))

        # 1. Homepage
        print("=== HOMEPAGE MOBILE ===")
        page.goto(BASE, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=f"{OUT}/01_homepage_hero.png", full_page=False)
        page.screenshot(path=f"{OUT}/01_homepage_full.png", full_page=True)

        # Check hero H1 visibility
        h1 = page.query_selector("h1")
        if h1:
            h1_box = h1.bounding_box()
            results["h1_visible_above_fold"] = h1_box and h1_box["y"] + h1_box["height"] < 812
            results["h1_text"] = h1.inner_text()
        else:
            results["h1_visible_above_fold"] = False
            results["h1_text"] = "NO H1 FOUND"

        # Check CTA buttons above fold
        cta_buttons = page.query_selector_all("a.btn, button.btn, .cta-button, a[href*='whatsapp'], a[href*='tel:'], a[href*='wa.me']")
        cta_info = []
        for btn in cta_buttons:
            box = btn.bounding_box()
            if box:
                cta_info.append({
                    "text": btn.inner_text()[:50],
                    "visible_above_fold": box["y"] < 812,
                    "y": round(box["y"]),
                    "width": round(box["width"]),
                    "height": round(box["height"]),
                })
        results["cta_buttons"] = cta_info

        # 2. Scroll to tour cards
        page.evaluate("window.scrollBy(0, 900)")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"{OUT}/02_tour_cards.png", full_page=False)

        # 3. Scroll to footer
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"{OUT}/03_footer.png", full_page=False)

        # 4. FAB buttons (WhatsApp/Telegram floating)
        fab_selectors = [
            "#fab-main", ".fab", ".floating-btn", ".whatsapp-float", ".telegram-float",
            "[class*='float']", "[class*='fab']", ".sticky-wa",
            "a[href*='wa.me']", "a[href*='t.me']"
        ]
        fab_results = []
        for sel in fab_selectors:
            els = page.query_selector_all(sel)
            for el in els:
                box = el.bounding_box()
                fab_results.append({
                    "selector": sel,
                    "text": el.inner_text()[:30],
                    "href": el.get_attribute("href") or "",
                    "visible": box is not None and box["width"] > 0 and box["height"] > 0,
                    "box": {"x": round(box["x"]), "y": round(box["y"]), "w": round(box["width"]), "h": round(box["height"])} if box else None
                })
        results["fab_buttons"] = fab_results

        # 5. Burger menu - find it
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        # Try multiple selectors
        burger_selectors = [
            ".burger", ".hamburger", ".menu-toggle", ".navbar-toggler",
            "[class*='burger']", "[class*='menu-btn']",
            "button[aria-label*='menu']", "button[aria-label*='Menu']",
            ".mobile-menu-toggle", "#menu-toggle"
        ]
        burger = None
        burger_sel = None
        for sel in burger_selectors:
            el = page.query_selector(sel)
            if el:
                box = el.bounding_box()
                if box and box["width"] > 0:
                    burger = el
                    burger_sel = sel
                    break

        if burger:
            results["burger_found"] = True
            results["burger_selector"] = burger_sel
            try:
                burger.click()
                page.wait_for_timeout(800)
                page.screenshot(path=f"{OUT}/04_burger_open.png", full_page=False)

                nav_links = page.query_selector_all("nav a, .mobile-nav a, .nav-menu a, .menu a, .nav-links a")
                results["nav_links"] = [{"text": a.inner_text()[:40], "href": a.get_attribute("href") or ""} for a in nav_links[:15]]

                # Close by pressing Escape or clicking burger again
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)
            except Exception as e:
                results["burger_error"] = str(e)[:100]
        else:
            results["burger_found"] = False
            # Dump all interactive elements for debug
            buttons_debug = page.evaluate("""() => {
                const btns = document.querySelectorAll('button, [role="button"], .burger, .hamburger');
                return Array.from(btns).map(b => ({
                    tag: b.tagName,
                    class: b.className?.substring(0, 60),
                    text: b.innerText?.substring(0, 30),
                    ariaLabel: b.getAttribute('aria-label'),
                    id: b.id
                }));
            }""")
            results["buttons_debug"] = buttons_debug

        # 6. Font check
        fonts = page.evaluate("""() => {
            const computed = window.getComputedStyle(document.body);
            const h1 = document.querySelector('h1');
            return {
                bodyFont: computed.fontFamily,
                bodyFontSize: computed.fontSize,
                h1Font: h1 ? window.getComputedStyle(h1).fontFamily : 'no h1',
                h1FontSize: h1 ? window.getComputedStyle(h1).fontSize : 'no h1',
            }
        }""")
        results["fonts"] = fonts

        font_loaded = page.evaluate("() => document.fonts.check('16px Raleway')")
        results["raleway_loaded"] = font_loaded

        # 7. Horizontal scroll
        has_h_scroll = page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
        results["horizontal_scroll"] = has_h_scroll

        # 8. Images
        images_info = page.evaluate("""() => {
            const imgs = document.querySelectorAll('img');
            const broken = [];
            let lazyCount = 0;
            imgs.forEach(img => {
                if (!img.complete || img.naturalWidth === 0) {
                    broken.push({src: img.src?.substring(0, 100), alt: img.alt});
                }
                if (img.loading === 'lazy') lazyCount++;
            });
            return {total: imgs.length, broken: broken, lazyCount: lazyCount};
        }""")
        results["images"] = images_info

        # 9. Tour pages
        for i, tour_url in enumerate(TOUR_PAGES):
            full_url = BASE + tour_url
            print(f"  Tour: {full_url}")
            try:
                resp = page.goto(full_url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1500)
                status = resp.status if resp else "no response"
                page.screenshot(path=f"{OUT}/05_tour_{i+1}.png", full_page=False)

                # Check mobile sticky bar on tour pages
                sticky = page.query_selector(".mobile-sticky-bar, [class*='sticky-bar'], [class*='mobile-book']")
                has_sticky = sticky is not None and (sticky.bounding_box() or {}).get("height", 0) > 0

                results[f"tour_{i+1}"] = {
                    "url": tour_url,
                    "status": status,
                    "title": page.title(),
                    "has_mobile_sticky_bar": has_sticky
                }
            except Exception as e:
                results[f"tour_{i+1}"] = {"url": tour_url, "error": str(e)[:100]}

        # 10. Blog pages
        for i, blog_url in enumerate(BLOG_PAGES):
            full_url = BASE + blog_url
            print(f"  Blog: {full_url}")
            try:
                resp = page.goto(full_url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1500)
                status = resp.status if resp else "no response"
                page.screenshot(path=f"{OUT}/06_blog_{i+1}.png", full_page=False)
                results[f"blog_{i+1}"] = {"url": blog_url, "status": status, "title": page.title()}
            except Exception as e:
                results[f"blog_{i+1}"] = {"url": blog_url, "error": str(e)[:100]}

        # 11. Payment modal
        page.goto(BASE, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        booking_btns = page.query_selector_all("[data-modal], [onclick*='modal'], [class*='book'], [href*='#book'], [href*='#pay']")
        results["booking_buttons_count"] = len(booking_btns)

        # Also try finding by text
        all_btns_text = page.evaluate("""() => {
            const btns = document.querySelectorAll('a, button');
            return Array.from(btns).filter(b => /забронировать|оплатить|книг|book/i.test(b.innerText))
                .map(b => ({text: b.innerText.substring(0, 40), class: b.className?.substring(0, 50), href: b.getAttribute('href')}))
                .slice(0, 10);
        }""")
        results["booking_buttons_by_text"] = all_btns_text

        if all_btns_text:
            # Click the first booking button
            try:
                first_book = page.query_selector(f"text=/{all_btns_text[0]['text'][:15]}/i")
                if first_book:
                    first_book.click()
                    page.wait_for_timeout(1500)
                    page.screenshot(path=f"{OUT}/07_payment_modal.png", full_page=False)
                    modal = page.query_selector(".modal, .popup, [class*='modal'], [class*='popup'], [class*='overlay'], [class*='payment']")
                    results["payment_modal"] = {"found": modal is not None, "visible": modal.is_visible() if modal else False}
            except Exception as e:
                results["payment_modal_error"] = str(e)[:100]

        # 12. Touch target check
        touch_targets = page.evaluate("""() => {
            const interactive = document.querySelectorAll('a, button, input, select, textarea, [role="button"]');
            const small = [];
            interactive.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
                    small.push({
                        tag: el.tagName,
                        text: el.innerText?.substring(0, 30) || el.getAttribute('aria-label') || '',
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        class: el.className?.substring(0, 50) || ''
                    });
                }
            });
            return small;
        }""")
        results["small_touch_targets"] = touch_targets

        # 13. Base font size check
        base_font = page.evaluate("""() => {
            const body = window.getComputedStyle(document.body);
            const p = document.querySelector('p');
            return {
                bodySize: body.fontSize,
                pSize: p ? window.getComputedStyle(p).fontSize : 'no p',
                viewportMeta: document.querySelector('meta[name="viewport"]')?.content || 'MISSING'
            };
        }""")
        results["base_font"] = base_font

        browser.close()

    results["console_errors"] = console_errors
    print("\n=== RESULTS ===")
    print(json.dumps(results, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    run()
