from playwright.sync_api import sync_playwright
import time

VIEWPORT = {'width': 390, 'height': 844}
PAGES = [
    ('https://sakhva-travel.com/', '/Users/vladimir/sakhva-travel/screenshots/home_mobile.png'),
    ('https://sakhva-travel.com/blog/', '/Users/vladimir/sakhva-travel/screenshots/blog_mobile.png'),
    ('https://sakhva-travel.com/tour/kazbegi/', '/Users/vladimir/sakhva-travel/screenshots/kazbegi_mobile.png'),
]

def capture(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        context = browser.new_context(
            viewport=VIEWPORT,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            is_mobile=True,
            has_touch=True,
        )
        page = context.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        time.sleep(2)
        # above the fold screenshot
        page.screenshot(path=output_path, full_page=False)
        print(f'Saved above-fold: {output_path}')
        # full page screenshot
        full_path = output_path.replace('.png', '_full.png')
        page.screenshot(path=full_path, full_page=True)
        print(f'Saved full page: {full_path}')

        # check for horizontal scroll
        scroll_width = page.evaluate('document.body.scrollWidth')
        viewport_width = page.evaluate('window.innerWidth')
        print(f'scrollWidth={scroll_width}, viewportWidth={viewport_width}, hScroll={scroll_width > viewport_width}')

        # check sticky bar
        sticky = page.evaluate('''() => {
            const all = document.querySelectorAll('*');
            const results = [];
            for (const el of all) {
                const style = window.getComputedStyle(el);
                if ((style.position === "fixed" || style.position === "sticky") && el.offsetHeight > 0) {
                    results.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className.toString().slice(0, 80),
                        top: style.top,
                        bottom: style.bottom,
                        height: el.offsetHeight,
                        width: el.offsetWidth,
                        zIndex: style.zIndex,
                        text: el.innerText ? el.innerText.slice(0, 100) : ''
                    });
                }
            }
            return results;
        }''')
        print(f'Fixed/sticky elements: {sticky}')

        # check font sizes of inputs
        inputs = page.evaluate('''() => {
            const els = document.querySelectorAll("input, textarea, select");
            return Array.from(els).map(el => ({
                tag: el.tagName,
                type: el.type || "",
                fontSize: window.getComputedStyle(el).fontSize,
                placeholder: el.placeholder || ""
            }));
        }''')
        print(f'Input font sizes: {inputs}')

        # check button sizes
        buttons = page.evaluate('''() => {
            const els = document.querySelectorAll("button, a[class*='btn'], a[class*='button'], [role='button']");
            return Array.from(els).slice(0, 15).map(el => ({
                tag: el.tagName,
                text: el.innerText ? el.innerText.slice(0, 50) : "",
                height: el.offsetHeight,
                width: el.offsetWidth,
            }));
        }''')
        print(f'Button sizes: {buttons}')

        browser.close()

for url, path in PAGES:
    print(f'\n=== {url} ===')
    try:
        capture(url, path)
    except Exception as e:
        print(f'Error: {e}')
