"""Visual audit screenshots for sakhva-travel.com"""
from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/visual-audit-2026-04-24"

CAPTURES = [
    # Desktop captures
    {"name": "desktop_hero", "w": 1440, "h": 900, "full": False, "scroll": 0},
    {"name": "desktop_tours", "w": 1440, "h": 900, "full": False, "scroll": 900},
    {"name": "desktop_footer", "w": 1440, "h": 900, "full": False, "scroll": 99999},
    {"name": "desktop_full", "w": 1440, "h": 900, "full": True, "scroll": 0},
    # Mobile captures
    {"name": "mobile_hero", "w": 375, "h": 812, "full": False, "scroll": 0},
    {"name": "mobile_tours", "w": 375, "h": 812, "full": False, "scroll": 812},
    {"name": "mobile_footer", "w": 375, "h": 812, "full": False, "scroll": 99999},
    {"name": "mobile_full", "w": 375, "h": 812, "full": True, "scroll": 0},
]

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for cap in CAPTURES:
            page = browser.new_page(
                viewport={"width": cap["w"], "height": cap["h"]},
                device_scale_factor=2 if cap["w"] <= 375 else 1,
            )
            page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)  # let animations finish

            if cap["scroll"] > 0 and not cap["full"]:
                page.evaluate(f"window.scrollTo(0, {cap['scroll']})")
                page.wait_for_timeout(500)

            path = os.path.join(OUTPUT_DIR, f"{cap['name']}.png")
            page.screenshot(path=path, full_page=cap["full"])
            print(f"Saved: {path}")
            page.close()

        # Now measure elements
        page = browser.new_page(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
        )
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        measurements = page.evaluate("""() => {
            const results = {};

            // Cookie banner buttons
            const cookieBtns = document.querySelectorAll('.cookie-banner button, .cookie-consent button, [class*="cookie"] button');
            results.cookie_buttons = Array.from(cookieBtns).map(b => {
                const r = b.getBoundingClientRect();
                return {text: b.textContent.trim(), width: r.width, height: r.height, visible: r.height > 0};
            });

            // Currency buttons
            const currBtns = document.querySelectorAll('.currency-btn, [class*="currency"] button, button[data-currency]');
            results.currency_buttons = Array.from(currBtns).map(b => {
                const r = b.getBoundingClientRect();
                return {text: b.textContent.trim(), width: r.width, height: r.height};
            });

            // Filter tabs
            const filterTabs = document.querySelectorAll('.filter-tab, .tour-filter, [class*="filter"] button, .tab-btn');
            results.filter_tabs = Array.from(filterTabs).map(t => {
                const r = t.getBoundingClientRect();
                return {text: t.textContent.trim(), width: r.width, height: r.height, overflow: t.scrollWidth > t.clientWidth};
            });

            // Hero subtitle
            const subtitle = document.querySelector('.hero-subtitle, .subtitle, [class*="subtitle"]');
            if (subtitle) {
                const cs = getComputedStyle(subtitle);
                results.hero_subtitle = {
                    text: subtitle.textContent.trim().substring(0, 80),
                    fontSize: cs.fontSize,
                    lineHeight: cs.lineHeight,
                };
            }

            // H1
            const h1 = document.querySelector('h1');
            if (h1) {
                const cs = getComputedStyle(h1);
                const r = h1.getBoundingClientRect();
                results.h1 = {
                    text: h1.textContent.trim().substring(0, 80),
                    fontSize: cs.fontSize,
                    top: r.top,
                    bottom: r.bottom,
                    visible_above_fold: r.bottom <= 812,
                };
            }

            // Music toggle
            const musicBtn = document.querySelector('.music-toggle, .music-btn, [class*="music"], #musicToggle, button[aria-label*="music"]');
            results.music_button = musicBtn ? {
                width: musicBtn.getBoundingClientRect().width,
                height: musicBtn.getBoundingClientRect().height,
                visible: musicBtn.getBoundingClientRect().height > 0,
                classes: musicBtn.className,
            } : null;

            // YouTube icon in footer
            const ytLinks = document.querySelectorAll('a[href*="youtube"], a[href*="youtu.be"]');
            results.youtube_links = Array.from(ytLinks).map(a => {
                const r = a.getBoundingClientRect();
                return {href: a.href, width: r.width, height: r.height, visible: r.height > 0};
            });

            // All buttons - tap target check
            const allBtns = document.querySelectorAll('button, a.btn, .btn, [role="button"], a[class*="btn"]');
            results.small_tap_targets = Array.from(allBtns).filter(b => {
                const r = b.getBoundingClientRect();
                return r.height > 0 && r.height < 44;
            }).map(b => {
                const r = b.getBoundingClientRect();
                return {
                    text: b.textContent.trim().substring(0, 40),
                    tag: b.tagName,
                    classes: b.className.substring(0, 60),
                    width: Math.round(r.width),
                    height: Math.round(r.height),
                    top: Math.round(r.top),
                };
            });

            // CTA buttons
            const ctas = document.querySelectorAll('.cta-btn, .hero-cta, [class*="cta"], .whatsapp-btn, a[href*="whatsapp"]');
            results.cta_buttons = Array.from(ctas).map(c => {
                const r = c.getBoundingClientRect();
                return {text: c.textContent.trim().substring(0, 40), width: Math.round(r.width), height: Math.round(r.height), top: Math.round(r.top)};
            });

            // Check horizontal overflow
            results.has_horizontal_scroll = document.documentElement.scrollWidth > document.documentElement.clientWidth;
            results.page_width = document.documentElement.scrollWidth;
            results.viewport_width = document.documentElement.clientWidth;

            return results;
        }""")

        print("\n=== MOBILE MEASUREMENTS ===")
        import json
        print(json.dumps(measurements, indent=2, ensure_ascii=False))

        page.close()

        # Desktop measurements
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        desktop_m = page.evaluate("""() => {
            const results = {};

            const currBtns = document.querySelectorAll('.currency-btn, [class*="currency"] button, button[data-currency]');
            results.currency_buttons = Array.from(currBtns).map(b => {
                const r = b.getBoundingClientRect();
                return {text: b.textContent.trim(), width: r.width, height: r.height};
            });

            const filterTabs = document.querySelectorAll('.filter-tab, .tour-filter, [class*="filter"] button, .tab-btn');
            results.filter_tabs = Array.from(filterTabs).map(t => {
                const r = t.getBoundingClientRect();
                return {text: t.textContent.trim().substring(0, 40), width: r.width, height: r.height};
            });

            const ytLinks = document.querySelectorAll('a[href*="youtube"], a[href*="youtu.be"]');
            results.youtube_links = Array.from(ytLinks).map(a => {
                const r = a.getBoundingClientRect();
                return {href: a.href, width: r.width, height: r.height};
            });

            return results;
        }""")

        print("\n=== DESKTOP MEASUREMENTS ===")
        print(json.dumps(desktop_m, indent=2, ensure_ascii=False))

        page.close()
        browser.close()

if __name__ == "__main__":
    main()
