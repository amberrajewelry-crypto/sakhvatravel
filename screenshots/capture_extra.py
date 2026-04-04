from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots/mobile"
VIEWPORT = {"width": 390, "height": 844}

extra_sections = [
    {"name": "4b_routes_cards", "scroll_y": 3000},
    {"name": "4c_tarot_card", "scroll_y": 3400},
    {"name": "5b_why_us_cards", "scroll_y": 4400},
    {"name": "7b_reviews_bottom", "scroll_y": 7000},
    {"name": "8b_blog_cards", "scroll_y": 8200},
    {"name": "9b_footer_bottom", "scroll_y": 99999},
]

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        print(f"Navigating to {URL}...")
        page.goto(URL, wait_until="networkidle", timeout=60000)
        time.sleep(3)

        total_height = page.evaluate("document.body.scrollHeight")
        print(f"Total page height: {total_height}px")

        for section in extra_sections:
            name = section["name"]
            scroll_y = section["scroll_y"]

            if scroll_y == 99999:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            else:
                page.evaluate(f"window.scrollTo(0, {scroll_y})")

            time.sleep(1.5)

            out_path = f"{OUTPUT_DIR}/{name}.png"
            page.screenshot(path=out_path, full_page=False)
            current_y = page.evaluate("window.scrollY")
            print(f"Captured {name} at scrollY={current_y} -> {out_path}")

        # Capture DOM info for analysis
        print("\n--- DOM Analysis ---")

        # Check for horizontal scroll
        scroll_width = page.evaluate("document.body.scrollWidth")
        client_width = page.evaluate("document.body.clientWidth")
        print(f"Body scrollWidth: {scroll_width}, clientWidth: {client_width}")
        if scroll_width > client_width:
            print("WARNING: Horizontal scroll detected!")

        # Check button sizes
        buttons = page.evaluate("""
            () => {
                const btns = document.querySelectorAll('button, a.btn, .btn, [class*="button"], [class*="Button"]');
                return Array.from(btns).slice(0, 20).map(b => {
                    const rect = b.getBoundingClientRect();
                    const style = window.getComputedStyle(b);
                    return {
                        text: b.textContent.trim().substring(0, 40),
                        tag: b.tagName,
                        className: b.className.substring(0, 60),
                        height: Math.round(rect.height),
                        width: Math.round(rect.width),
                        fontSize: style.fontSize,
                        visible: rect.width > 0 && rect.height > 0
                    };
                });
            }
        """)
        print("\nButtons/Links:")
        for btn in buttons:
            flag = " <-- TOO SMALL" if btn['height'] < 44 and btn['visible'] else ""
            print(f"  [{btn['tag']}] '{btn['text'][:30]}' h={btn['height']} w={btn['width']} fs={btn['fontSize']} class='{btn['className'][:50]}'{flag}")

        # Check font sizes
        text_elements = page.evaluate("""
            () => {
                const tags = ['p', 'span', 'h1', 'h2', 'h3', 'h4', 'li', 'a'];
                let results = [];
                for (const tag of tags) {
                    const els = document.querySelectorAll(tag);
                    Array.from(els).slice(0, 5).forEach(el => {
                        const style = window.getComputedStyle(el);
                        const rect = el.getBoundingClientRect();
                        const fs = parseFloat(style.fontSize);
                        if (rect.width > 0 && el.textContent.trim().length > 0) {
                            results.push({
                                tag,
                                text: el.textContent.trim().substring(0, 40),
                                fontSize: style.fontSize,
                                tooSmall: fs < 12
                            });
                        }
                    });
                }
                return results;
            }
        """)
        print("\nFont sizes:")
        small_fonts = [t for t in text_elements if t['tooSmall']]
        if small_fonts:
            print("  SMALL FONTS (<12px):")
            for t in small_fonts:
                print(f"    [{t['tag']}] '{t['text'][:30]}' fontSize={t['fontSize']}")
        else:
            print("  All visible text >= 12px")

        # Check overflow elements
        overflow = page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                const vw = window.innerWidth;
                let overflowing = [];
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > vw + 5) {
                        overflowing.push({
                            tag: el.tagName,
                            className: el.className ? el.className.toString().substring(0, 60) : '',
                            right: Math.round(rect.right),
                            vw: vw
                        });
                    }
                }
                return overflowing.slice(0, 15);
            }
        """)
        print("\nOverflowing elements (right > viewport width):")
        if overflow:
            for o in overflow:
                print(f"  [{o['tag']}] class='{o['className']}' right={o['right']} vw={o['vw']}")
        else:
            print("  None detected")

        browser.close()
        print("\nDone.")

if __name__ == "__main__":
    capture()
