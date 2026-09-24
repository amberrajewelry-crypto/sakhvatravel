"""Desktop audit of sakhva-travel.com - 1440x900 viewport"""
import json
from playwright.sync_api import sync_playwright

DESKTOP_VP = {"width": 1440, "height": 900}
BASE = "https://sakhva-travel.com"
OUT = "/Users/vladimir/sakhva-travel/screenshots/desktop"

def run():
    console_errors = []
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport=DESKTOP_VP)
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

        # 1. Homepage hero
        print("=== HOMEPAGE DESKTOP ===")
        page.goto(BASE, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=f"{OUT}/01_hero.png", full_page=False)

        # 2. Scroll sections
        sections = [
            ("tours", 900),
            ("about", 1800),
            ("reviews", 2700),
            ("faq", 3600),
            ("footer", 99999),  # bottom
        ]
        for name, scroll_y in sections:
            if scroll_y == 99999:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            else:
                page.evaluate(f"window.scrollTo(0, {scroll_y})")
            page.wait_for_timeout(800)
            page.screenshot(path=f"{OUT}/02_{name}.png", full_page=False)

        # Full page
        page.screenshot(path=f"{OUT}/00_full_page.png", full_page=True)

        # 3. Navigation check
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        nav_links = page.query_selector_all("nav a, header a, .navbar a")
        nav_info = []
        for a in nav_links[:20]:
            box = a.bounding_box()
            nav_info.append({
                "text": a.inner_text()[:40],
                "href": a.get_attribute("href") or "",
                "visible": box is not None and box["width"] > 0,
            })
        results["nav_links"] = nav_info

        # 4. Check for overlapping elements
        overlap_check = page.evaluate("""() => {
            const els = document.querySelectorAll('h1, h2, h3, p, a, button, img, .card, .tour-card');
            const issues = [];
            const rects = [];
            els.forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) {
                    rects.push({el: el.tagName + '.' + (el.className || '').substring(0, 30), rect: r});
                }
            });
            return {totalElements: rects.length};
        }""")
        results["element_check"] = overlap_check

        # 5. Check broken images
        images_info = page.evaluate("""() => {
            const imgs = document.querySelectorAll('img');
            const broken = [];
            imgs.forEach(img => {
                if (!img.complete || img.naturalWidth === 0) {
                    broken.push({src: img.src?.substring(0, 100), alt: img.alt});
                }
            });
            return {total: imgs.length, broken: broken};
        }""")
        results["images"] = images_info

        # 6. CSS/Layout issues
        layout_issues = page.evaluate("""() => {
            const issues = [];
            // Check for overflow
            const hasHScroll = document.documentElement.scrollWidth > document.documentElement.clientWidth;
            if (hasHScroll) issues.push("Horizontal scroll detected");

            // Check z-index stacking
            const fixedEls = document.querySelectorAll('[style*="position: fixed"], [style*="position:fixed"]');
            const stickyEls = document.querySelectorAll('[style*="position: sticky"], [style*="position:sticky"]');

            // Check for text overflow
            const textEls = document.querySelectorAll('h1, h2, h3, h4, p, span, a');
            let overflowCount = 0;
            textEls.forEach(el => {
                if (el.scrollWidth > el.clientWidth + 2) {
                    overflowCount++;
                }
            });

            return {
                hasHScroll,
                fixedElements: fixedEls.length,
                stickyElements: stickyEls.length,
                textOverflowCount: overflowCount,
                issues
            };
        }""")
        results["layout"] = layout_issues

        # 7. Hover states on nav
        for link in nav_links[:5]:
            try:
                link.hover()
                page.wait_for_timeout(300)
            except:
                pass
        page.screenshot(path=f"{OUT}/03_nav_hover.png", full_page=False)

        # 8. Check all links for 404s (sample)
        all_links = page.evaluate("""() => {
            const links = document.querySelectorAll('a[href]');
            const hrefs = new Set();
            links.forEach(l => {
                const h = l.getAttribute('href');
                if (h && h.startsWith('/') && !h.startsWith('//')) hrefs.add(h);
            });
            return Array.from(hrefs).slice(0, 20);
        }""")
        results["internal_links_sample"] = all_links

        # 9. Performance metrics
        perf = page.evaluate("""() => {
            const timing = performance.getEntriesByType('navigation')[0];
            return timing ? {
                domContentLoaded: Math.round(timing.domContentLoadedEventEnd),
                loadComplete: Math.round(timing.loadEventEnd),
                domInteractive: Math.round(timing.domInteractive),
                transferSize: Math.round(timing.transferSize / 1024) + 'KB',
            } : {};
        }""")
        results["performance"] = perf

        # 10. Accessibility basics
        a11y = page.evaluate("""() => {
            const imgs_no_alt = document.querySelectorAll('img:not([alt])');
            const inputs_no_label = document.querySelectorAll('input:not([aria-label]):not([id])');
            const low_contrast = [];
            const lang = document.documentElement.getAttribute('lang');
            const title = document.title;
            const meta_desc = document.querySelector('meta[name="description"]')?.content || '';

            return {
                images_without_alt: imgs_no_alt.length,
                inputs_without_label: inputs_no_label.length,
                html_lang: lang,
                page_title: title,
                meta_description: meta_desc?.substring(0, 160),
            };
        }""")
        results["accessibility"] = a11y

        browser.close()

    results["console_errors"] = console_errors
    print("\n=== DESKTOP RESULTS ===")
    print(json.dumps(results, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    run()
