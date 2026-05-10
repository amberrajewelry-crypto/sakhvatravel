from playwright.sync_api import sync_playwright
import os

OUT = "/Users/vladimir/sakhva-travel/screenshots/visual-audit"

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Desktop footer
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        # Scroll to absolute bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUT, "desktop_footer_real.png"), full_page=False)

        # Also get footer element info
        footer_info = page.evaluate("""() => {
            const footer = document.querySelector('footer');
            if (!footer) return { found: false };
            const rect = footer.getBoundingClientRect();
            const links = footer.querySelectorAll('a');
            const socials = [];
            links.forEach(a => {
                const href = a.href || '';
                if (href.includes('instagram') || href.includes('youtube') || href.includes('telegram') || href.includes('tiktok') || href.includes('tripadvisor') || href.includes('facebook')) {
                    const r = a.getBoundingClientRect();
                    socials.push({ href, width: Math.round(r.width), height: Math.round(r.height), text: a.textContent?.trim().substring(0,30) });
                }
            });
            return { found: true, top: Math.round(rect.top + window.scrollY), height: Math.round(rect.height), socials };
        }""")
        print(f"Footer: {footer_info}")
        page.close()

        # Mobile footer
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUT, "mobile_footer_real.png"), full_page=False)
        page.close()

        browser.close()
        print("Footer screenshots done.")

if __name__ == "__main__":
    capture()
