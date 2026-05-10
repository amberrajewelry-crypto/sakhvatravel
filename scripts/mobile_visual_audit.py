"""
Mobile visual audit for sakhva-travel.com
Captures screenshots, checks JS errors, horizontal overflow, touch targets.
"""
import json
import os
from playwright.sync_api import sync_playwright

PAGES = [
    ("https://sakhva-travel.com/", "home"),
    ("https://sakhva-travel.com/tour/kazbegi/", "tour_kazbegi"),
    ("https://sakhva-travel.com/tour/kakheti/", "tour_kakheti"),
    ("https://sakhva-travel.com/about/", "about"),
    ("https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/", "blog_kazbegi"),
    ("https://sakhva-travel.com/en/", "home_en"),
]

SCREENSHOT_DIR = "/Users/vladimir/sakhva-travel/screenshots"
VIEWPORT = {"width": 375, "height": 812}

def run_audit():
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for url, name in PAGES:
            print(f"\n--- Auditing: {url} ---")
            page_results = {
                "url": url,
                "js_errors": [],
                "horizontal_overflow": False,
                "overflow_elements": [],
                "small_touch_targets": [],
            }

            page = browser.new_page(viewport=VIEWPORT)

            # Collect JS errors
            page.on("pageerror", lambda err, pr=page_results: pr["js_errors"].append(str(err)))
            console_errors = []
            page.on("console", lambda msg, ce=console_errors: ce.append({"type": msg.type, "text": msg.text}) if msg.type == "error" else None)

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                page_results["load_error"] = str(e)
                results[name] = page_results
                page.close()
                continue

            # Wait a bit for lazy content
            page.wait_for_timeout(1000)

            # Screenshot above-the-fold
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"mobile_{name}.png")
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"  Screenshot saved: {screenshot_path}")

            # Full-page screenshot
            screenshot_full_path = os.path.join(SCREENSHOT_DIR, f"mobile_{name}_full.png")
            page.screenshot(path=screenshot_full_path, full_page=True)

            # Check horizontal overflow
            overflow_data = page.evaluate("""() => {
                const viewportWidth = window.innerWidth;
                const docWidth = document.documentElement.scrollWidth;
                const hasOverflow = docWidth > viewportWidth;

                // Find elements causing overflow
                const overflowEls = [];
                if (hasOverflow) {
                    const all = document.querySelectorAll('*');
                    for (const el of all) {
                        const rect = el.getBoundingClientRect();
                        if (rect.right > viewportWidth + 2 || rect.left < -2) {
                            const tag = el.tagName.toLowerCase();
                            const cls = el.className ? (typeof el.className === 'string' ? el.className.substring(0, 60) : '') : '';
                            const id = el.id || '';
                            if (overflowEls.length < 10) {
                                overflowEls.push({
                                    tag: tag,
                                    id: id,
                                    class: cls,
                                    right: Math.round(rect.right),
                                    left: Math.round(rect.left),
                                    width: Math.round(rect.width)
                                });
                            }
                        }
                    }
                }
                return {
                    hasOverflow: hasOverflow,
                    docWidth: docWidth,
                    viewportWidth: viewportWidth,
                    overflowElements: overflowEls
                };
            }""")

            page_results["horizontal_overflow"] = overflow_data["hasOverflow"]
            page_results["doc_width"] = overflow_data["docWidth"]
            page_results["viewport_width"] = overflow_data["viewportWidth"]
            page_results["overflow_elements"] = overflow_data["overflowElements"]

            # Check touch targets (buttons, links, inputs)
            touch_data = page.evaluate("""() => {
                const MIN_SIZE = 44;
                const small = [];
                const interactive = document.querySelectorAll('a, button, input, select, textarea, [role="button"], [onclick]');

                for (const el of interactive) {
                    // Skip hidden elements
                    const style = window.getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;

                    const rect = el.getBoundingClientRect();
                    if (rect.width === 0 && rect.height === 0) continue;

                    // Only check elements in viewport (visible area)
                    if (rect.top > 3000) continue;

                    if (rect.width < MIN_SIZE || rect.height < MIN_SIZE) {
                        const tag = el.tagName.toLowerCase();
                        const cls = el.className ? (typeof el.className === 'string' ? el.className.substring(0, 60) : '') : '';
                        const text = (el.textContent || '').trim().substring(0, 40);
                        const href = el.href ? el.href.substring(0, 60) : '';
                        small.push({
                            tag: tag,
                            class: cls,
                            text: text,
                            href: href,
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            top: Math.round(rect.top)
                        });
                    }
                }
                return small;
            }""")

            page_results["small_touch_targets"] = touch_data
            page_results["console_errors"] = console_errors

            # Check CTA visibility above the fold
            cta_data = page.evaluate("""() => {
                const viewportHeight = window.innerHeight;
                const ctas = document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp"], a[href*="t.me"], .cta-button, .btn-primary, [class*="cta"], [class*="book"], button[class*="btn"]');
                const results = [];
                for (const el of ctas) {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    if (style.display === 'none') continue;
                    results.push({
                        tag: el.tagName.toLowerCase(),
                        text: (el.textContent || '').trim().substring(0, 40),
                        top: Math.round(rect.top),
                        visible_above_fold: rect.top < viewportHeight,
                        class: (typeof el.className === 'string' ? el.className.substring(0, 60) : '')
                    });
                }
                return results;
            }""")

            page_results["cta_elements"] = cta_data

            # H1 check
            h1_data = page.evaluate("""() => {
                const h1 = document.querySelector('h1');
                if (!h1) return null;
                const rect = h1.getBoundingClientRect();
                return {
                    text: h1.textContent.trim().substring(0, 80),
                    top: Math.round(rect.top),
                    visible_above_fold: rect.top < window.innerHeight,
                    font_size: window.getComputedStyle(h1).fontSize
                };
            }""")
            page_results["h1"] = h1_data

            print(f"  JS errors: {len(page_results['js_errors'])}")
            print(f"  Console errors: {len(console_errors)}")
            print(f"  Horizontal overflow: {overflow_data['hasOverflow']} (doc: {overflow_data['docWidth']}px)")
            print(f"  Small touch targets: {len(touch_data)}")

            results[name] = page_results
            page.close()

        browser.close()

    # Save results
    report_path = os.path.join(SCREENSHOT_DIR, "audit_results.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {report_path}")

    return results


if __name__ == "__main__":
    run_audit()
