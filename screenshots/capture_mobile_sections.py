#!/usr/bin/env python3
"""Capture mobile section screenshots for sakhva-travel.com"""

from playwright.sync_api import sync_playwright

URL = "https://sakhva-travel.com"
VIEWPORT = {"width": 375, "height": 812}
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots"

def capture(page, path, full_page=False):
    page.screenshot(path=path, full_page=full_page)
    print(f"Saved: {path}")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()

        print(f"Loading {URL}...")
        page.goto(URL, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)

        # ── 1. Hero section (top of page, viewport shot) ────────────────────
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        capture(page, f"{OUTPUT_DIR}/mobile_hero.png")

        # ── 2. Check horizontal overflow ────────────────────────────────────
        overflow_info = page.evaluate("""() => {
            const body = document.body;
            const html = document.documentElement;
            return {
                bodyScrollWidth: body.scrollWidth,
                windowInnerWidth: window.innerWidth,
                htmlScrollWidth: html.scrollWidth,
                overflow: body.scrollWidth > window.innerWidth
            };
        }""")
        print(f"Horizontal overflow check: {overflow_info}")

        # ── 3. Measure page sections ─────────────────────────────────────────
        sections = page.evaluate("""() => {
            const results = {};

            // Nav / header
            const nav = document.querySelector('nav, header, [class*="nav"], [class*="header"]');
            if (nav) {
                const r = nav.getBoundingClientRect();
                results.nav = {tag: nav.tagName, class: nav.className.substring(0,80), top: r.top, height: r.height, width: r.width};
            }

            // Hero / banner section
            const hero = document.querySelector(
                '[class*="hero"], [class*="banner"], [class*="Hero"], section:first-of-type, main > *:first-child'
            );
            if (hero) {
                const r = hero.getBoundingClientRect();
                results.hero = {tag: hero.tagName, class: hero.className.substring(0,80), top: r.top, height: r.height};
            }

            // H1 visibility
            const h1 = document.querySelector('h1');
            if (h1) {
                const r = h1.getBoundingClientRect();
                results.h1 = {
                    text: h1.innerText.substring(0,80),
                    top: r.top,
                    bottom: r.bottom,
                    visibleWithoutScroll: r.top >= 0 && r.bottom <= window.innerHeight,
                    fontSize: window.getComputedStyle(h1).fontSize
                };
            }

            // CTA buttons
            const btns = Array.from(document.querySelectorAll('a[class*="btn"], button, a[class*="cta"], [class*="button"]'));
            results.buttons = btns.slice(0, 5).map(b => {
                const r = b.getBoundingClientRect();
                return {
                    text: b.innerText.substring(0,40),
                    width: Math.round(r.width),
                    height: Math.round(r.height),
                    top: Math.round(r.top),
                    touchFriendly: r.height >= 44 && r.width >= 44
                };
            });

            // Tour cards
            const cards = document.querySelectorAll('[class*="card"], [class*="Card"], [class*="tour"], article');
            results.cardCount = cards.length;
            results.firstCard = cards[0] ? (() => {
                const r = cards[0].getBoundingClientRect();
                return {class: cards[0].className.substring(0,80), width: r.width, height: r.height};
            })() : null;

            // Footer
            const footer = document.querySelector('footer, [class*="footer"], [class*="Footer"]');
            if (footer) {
                const r = footer.getBoundingClientRect();
                results.footer = {tag: footer.tagName, class: footer.className.substring(0,80), top: r.top, height: r.height};
            }

            // Burger menu
            const burger = document.querySelector(
                '[class*="burger"], [class*="hamburger"], [class*="menu-toggle"], [class*="nav-toggle"], button[aria-label*="menu"], button[aria-label*="Menu"]'
            );
            results.burgerMenu = burger ? {
                found: true,
                class: burger.className.substring(0,60),
                ariaLabel: burger.getAttribute('aria-label'),
                visible: window.getComputedStyle(burger).display !== 'none'
            } : {found: false};

            return results;
        }""")
        print("\n=== Page structure analysis ===")
        import json
        print(json.dumps(sections, indent=2))

        # ── 4. Scroll to tour cards ──────────────────────────────────────────
        # Find the approximate Y offset of cards
        cards_y = page.evaluate("""() => {
            const card = document.querySelector('[class*="card"], [class*="Card"], [class*="tour"], article');
            if (!card) return 600;
            const rect = card.getBoundingClientRect();
            return window.scrollY + rect.top - 60;
        }""")
        print(f"\nScrolling to tour cards at Y={cards_y}")
        page.evaluate(f"window.scrollTo(0, {cards_y})")
        page.wait_for_timeout(800)
        capture(page, f"{OUTPUT_DIR}/mobile_tour_cards.png")

        # ── 5. Footer ────────────────────────────────────────────────────────
        # Scroll to bottom
        page_height = page.evaluate("document.body.scrollHeight")
        print(f"\nPage total height: {page_height}px")
        page.evaluate(f"window.scrollTo(0, {page_height})")
        page.wait_for_timeout(800)
        capture(page, f"{OUTPUT_DIR}/mobile_footer.png")

        # ── 6. Full-page mobile screenshot ──────────────────────────────────
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        capture(page, f"{OUTPUT_DIR}/mobile_full_page.png", full_page=True)

        # ── 7. Test burger menu interaction ─────────────────────────────────
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        burger_result = page.evaluate("""() => {
            const burger = document.querySelector(
                '[class*="burger"], [class*="hamburger"], [class*="menu-toggle"], [class*="nav-toggle"], button[aria-label*="menu"], button[aria-label*="Menu"]'
            );
            return burger ? burger.outerHTML.substring(0, 200) : 'not found';
        }""")
        print(f"\nBurger menu HTML: {burger_result}")

        try:
            burger_sel = '[class*="burger"], [class*="hamburger"], [class*="menu-toggle"], [class*="nav-toggle"]'
            burger_el = page.query_selector(burger_sel)
            if burger_el:
                burger_el.click()
                page.wait_for_timeout(800)
                capture(page, f"{OUTPUT_DIR}/mobile_nav_open.png")
                print("Nav opened and captured.")
            else:
                print("No burger element found to click.")
        except Exception as e:
            print(f"Burger click error: {e}")

        browser.close()
        print("\nAll captures complete.")

if __name__ == "__main__":
    run()
