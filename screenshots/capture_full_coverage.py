from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots"

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile":  {"width": 375,  "height": 812},
}

def capture_section(page, name, viewport_name, y_start, height):
    """Scroll to position and capture a viewport-sized clip."""
    page.evaluate(f"window.scrollTo(0, {y_start})")
    time.sleep(0.4)
    path = f"{OUTPUT_DIR}/{viewport_name}_{name}.png"
    page.screenshot(path=path, clip={"x": 0, "y": 0, "width": page.viewport_size["width"], "height": height})
    print(f"  Saved: {path}")
    return path


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for vp_name, vp in VIEWPORTS.items():
            print(f"\n=== {vp_name.upper()} ({vp['width']}x{vp['height']}) ===")
            page = browser.new_page(viewport=vp)
            page.goto(URL, wait_until="networkidle", timeout=30000)
            time.sleep(1.5)  # let lazy images settle

            total_height = page.evaluate("document.body.scrollHeight")
            print(f"  Page total height: {total_height}px")

            # 1. Full-page screenshot
            full_path = f"{OUTPUT_DIR}/{vp_name}_full_page.png"
            page.screenshot(path=full_path, full_page=True)
            print(f"  Saved full-page: {full_path}")

            # 2. Above-the-fold / Hero
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(0.3)
            hero_path = f"{OUTPUT_DIR}/{vp_name}_hero.png"
            page.screenshot(path=hero_path, clip={"x": 0, "y": 0, "width": vp["width"], "height": vp["height"]})
            print(f"  Saved hero: {hero_path}")

            # 3. Detect sections via JS and screenshot each
            sections_info = page.evaluate("""
                () => {
                    const selectors = [
                        { key: 'hero',    sel: 'section:first-of-type, .hero, [class*="hero"], header' },
                        { key: 'tours',   sel: '[class*="tour"], [class*="Tour"], [id*="tour"], [id*="Tour"]' },
                        { key: 'reviews', sel: '[class*="review"], [class*="Review"], [class*="testimonial"], [class*="Testimonial"], [id*="review"]' },
                        { key: 'cta',     sel: '[class*="cta"], [class*="CTA"], [class*="call-to-action"], [class*="contact"], [id*="cta"], [id*="contact"]' },
                        { key: 'footer',  sel: 'footer, [class*="footer"], [id*="footer"]' },
                    ];
                    const result = [];
                    for (const { key, sel } of selectors) {
                        const el = document.querySelector(sel);
                        if (el) {
                            const rect = el.getBoundingClientRect();
                            const scrollY = window.pageYOffset;
                            result.push({
                                key,
                                top: rect.top + scrollY,
                                height: el.offsetHeight,
                                found: true
                            });
                        } else {
                            result.push({ key, found: false });
                        }
                    }
                    return result;
                }
            """)
            print(f"  Detected sections: {sections_info}")

            # Capture each detected section
            viewport_h = vp["height"]
            for sec in sections_info:
                if sec.get("found") and sec.get("height", 0) > 10:
                    y = int(sec["top"])
                    h = min(int(sec["height"]), viewport_h * 2)  # cap at 2x viewport
                    # scroll to section top
                    page.evaluate(f"window.scrollTo(0, {max(0, y - 20)})")
                    time.sleep(0.4)
                    # capture from current scroll position
                    sec_path = f"{OUTPUT_DIR}/{vp_name}_section_{sec['key']}.png"
                    # Use full element clip relative to page
                    # We screenshot full_page clip
                    clip_y = max(0, y - 20)
                    clip_h = min(h + 40, viewport_h)
                    page.screenshot(
                        path=sec_path,
                        clip={"x": 0, "y": 0, "width": vp["width"], "height": clip_h}
                    )
                    print(f"  Saved section '{sec['key']}': {sec_path}")

            # 4. Viewport-based scroll captures — every viewport height step
            step = vp["height"]
            scroll_pos = 0
            scroll_idx = 0
            while scroll_pos < total_height:
                page.evaluate(f"window.scrollTo(0, {scroll_pos})")
                time.sleep(0.3)
                scroll_path = f"{OUTPUT_DIR}/{vp_name}_scroll_{scroll_idx:02d}.png"
                page.screenshot(path=scroll_path, clip={"x": 0, "y": 0, "width": vp["width"], "height": step})
                print(f"  Saved scroll chunk {scroll_idx}: y={scroll_pos} → {scroll_path}")
                scroll_pos += step
                scroll_idx += 1

            page.close()

        browser.close()
        print("\nAll screenshots captured.")


if __name__ == "__main__":
    run()
