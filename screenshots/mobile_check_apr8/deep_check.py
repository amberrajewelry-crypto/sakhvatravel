from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/mobile_check_apr8"

def deep_check():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # 1. Cookie banner detail — find the actual banner element (not body)
        print("=== COOKIE BANNER DETAILS ===")
        cookie_info = page.evaluate("""
            (() => {
                // Find by id
                const byId = document.querySelector('[id*="cookie"], [id*="Cookie"], [id*="consent"]');
                // Find small positioned banners
                const allDivs = [...document.querySelectorAll('div, section, aside')];
                const banners = allDivs.filter(el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return (
                        (style.position === 'fixed' || style.position === 'sticky') &&
                        rect.height < 200 &&
                        rect.height > 30 &&
                        (el.textContent.toLowerCase().includes('cookie') ||
                         el.textContent.toLowerCase().includes('cookies'))
                    );
                });
                const results = banners.map(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    const btns = [...el.querySelectorAll('button, a[href], [role="button"]')].map(b => {
                        const br = b.getBoundingClientRect();
                        return {text: b.innerText.trim().substring(0, 30), w: Math.round(br.width), h: Math.round(br.height)};
                    });
                    return {
                        tag: el.tagName,
                        id: el.id,
                        class: el.className.toString().substring(0, 80),
                        x: Math.round(rect.x), y: Math.round(rect.y),
                        w: Math.round(rect.width), h: Math.round(rect.height),
                        position: style.position,
                        bottom: style.bottom,
                        zIndex: style.zIndex,
                        buttons: btns
                    };
                });
                // Also get by id
                const idEl = document.querySelector('[id*="cookie"]');
                if (idEl) {
                    const rect = idEl.getBoundingClientRect();
                    const style = window.getComputedStyle(idEl);
                    const btns = [...idEl.querySelectorAll('button, a[href]')].map(b => {
                        const br = b.getBoundingClientRect();
                        return {text: b.innerText.trim().substring(0, 30), w: Math.round(br.width), h: Math.round(br.height)};
                    });
                    results.push({
                        tag: idEl.tagName, id: idEl.id,
                        class: idEl.className.toString().substring(0, 80),
                        x: Math.round(rect.x), y: Math.round(rect.y),
                        w: Math.round(rect.width), h: Math.round(rect.height),
                        position: style.position,
                        bottom: style.bottom,
                        zIndex: style.zIndex,
                        buttons: btns
                    });
                }
                return results;
            })()
        """)
        import json
        print(json.dumps(cookie_info, indent=2, ensure_ascii=False))

        # 2. Check paragraph font sizes in context
        print("\n=== PARAGRAPH FONT SIZES IN CONTEXT ===")
        fonts = page.evaluate("""
            (() => {
                const results = [];
                // Check all paragraph-like elements
                document.querySelectorAll('p, span, li, .subtitle, .description, [class*="desc"], [class*="text"]').forEach(el => {
                    const style = window.getComputedStyle(el);
                    const size = parseFloat(style.fontSize);
                    const rect = el.getBoundingClientRect();
                    if (size < 16 && el.innerText && el.innerText.trim().length > 10 && rect.height > 0) {
                        results.push({
                            tag: el.tagName,
                            class: el.className.toString().substring(0, 50),
                            fontSize: size,
                            text: el.innerText.trim().substring(0, 60),
                            y: Math.round(rect.y)
                        });
                    }
                });
                // Deduplicate by text
                const seen = new Set();
                return results.filter(r => {
                    if (seen.has(r.text)) return false;
                    seen.add(r.text);
                    return true;
                }).slice(0, 20);
            })()
        """)
        import json
        print(json.dumps(fonts, indent=2, ensure_ascii=False))

        # 3. Filter tabs overflow — check the category filter row
        print("\n=== FILTER TABS ROW ===")
        filter_info = page.evaluate("""
            (() => {
                // Find filter/tab row
                const candidates = [...document.querySelectorAll('[class*="filter"], [class*="tab"], [class*="category"], [class*="Tag"]')];
                return candidates.slice(0, 5).map(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return {
                        tag: el.tagName,
                        class: el.className.toString().substring(0, 60),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height),
                        overflow: style.overflowX,
                        scrollWidth: el.scrollWidth,
                        text: el.innerText.trim().substring(0, 60)
                    };
                });
            })()
        """)
        print(json.dumps(filter_info, indent=2, ensure_ascii=False))

        # 4. Header sticky check — scroll and see if header stays
        print("\n=== HEADER STICKY CHECK AFTER SCROLL ===")
        page.evaluate("window.scrollTo(0, 400)")
        time.sleep(0.5)
        header_after = page.evaluate("""
            (() => {
                const header = document.querySelector('header');
                if (!header) return null;
                const rect = header.getBoundingClientRect();
                const style = window.getComputedStyle(header);
                return {
                    y_in_viewport: Math.round(rect.y),
                    position: style.position,
                    top: style.top,
                    w: Math.round(rect.width),
                    h: Math.round(rect.height)
                };
            })()
        """)
        print(json.dumps(header_after, indent=2))

        # Screenshot after scroll to show header behavior
        page.screenshot(
            path=f"{OUTPUT_DIR}/07_header_after_scroll400.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        # 5. Tour catalog section screenshot
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        # Find tour catalog section
        catalog_y = page.evaluate("""
            (() => {
                const el = document.querySelector('[class*="catalog"], [class*="tours-grid"], [id*="tours"], section:has([class*="tour"])');
                if (!el) return 2000;
                return Math.round(el.getBoundingClientRect().y + window.scrollY);
            })()
        """)
        print(f"\nCatalog section starts at y={catalog_y}")
        page.evaluate(f"window.scrollTo(0, {catalog_y})")
        time.sleep(1)
        page.screenshot(
            path=f"{OUTPUT_DIR}/08_catalog_section.png",
            full_page=False,
            clip={"x": 0, "y": 0, "width": 375, "height": 812}
        )

        browser.close()

if __name__ == "__main__":
    deep_check()
