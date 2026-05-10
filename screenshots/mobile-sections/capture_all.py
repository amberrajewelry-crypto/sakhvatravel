"""Capture detailed mobile screenshots of all sections on sakhva-travel.com"""
from playwright.sync_api import sync_playwright
import time

MOBILE_W = 375
MOBILE_H = 812

def capture_sections(url, sections, prefix):
    """Scroll through page and capture screenshots at specific scroll positions."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': MOBILE_W, 'height': MOBILE_H})
        page.goto(url, wait_until='networkidle', timeout=30000)
        time.sleep(2)  # let animations settle

        # Get full page height
        total_height = page.evaluate('document.body.scrollHeight')
        print(f"Page: {url}")
        print(f"Total height: {total_height}px")

        for name, scroll_y in sections:
            page.evaluate(f'window.scrollTo(0, {scroll_y})')
            time.sleep(0.5)
            path = f'/Users/vladimir/sakhva-travel/screenshots/mobile-sections/{prefix}_{name}.png'
            page.screenshot(path=path, full_page=False)
            print(f"  Captured: {name} at y={scroll_y}")

        # Also capture full page
        full_path = f'/Users/vladimir/sakhva-travel/screenshots/mobile-sections/{prefix}_full.png'
        page.screenshot(path=full_path, full_page=True)
        print(f"  Captured: full page")

        browser.close()

def get_section_positions(url):
    """Find actual section positions on the page."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': MOBILE_W, 'height': MOBILE_H})
        page.goto(url, wait_until='networkidle', timeout=30000)
        time.sleep(2)

        total_height = page.evaluate('document.body.scrollHeight')
        print(f"\nPage: {url}, total height: {total_height}px")

        # Find all sections and key elements
        positions = page.evaluate('''() => {
            const results = [];
            // Get all sections
            const sections = document.querySelectorAll('section, .section, [id]');
            sections.forEach(s => {
                const rect = s.getBoundingClientRect();
                const scrollY = window.scrollY;
                results.push({
                    tag: s.tagName,
                    id: s.id || '',
                    className: s.className?.substring?.(0, 80) || '',
                    top: rect.top + scrollY,
                    height: rect.height
                });
            });
            // Get all h1, h2, h3
            const headings = document.querySelectorAll('h1, h2, h3');
            headings.forEach(h => {
                const rect = h.getBoundingClientRect();
                const scrollY = window.scrollY;
                results.push({
                    tag: h.tagName,
                    text: h.textContent.trim().substring(0, 60),
                    top: rect.top + scrollY,
                    height: rect.height
                });
            });
            return results;
        }''')

        for p_item in sorted(positions, key=lambda x: x['top']):
            print(f"  y={int(p_item['top']):5d} h={int(p_item['height']):5d} {p_item['tag']:8s} {p_item.get('id',''):20s} {p_item.get('text',''):60s} {p_item.get('className','')[:50]}")

        browser.close()
        return positions

# Step 1: Discover section positions
print("=== DISCOVERING SECTIONS ===")
main_positions = get_section_positions('https://sakhva-travel.com')

print("\n=== DISCOVERING TOUR PAGE SECTIONS ===")
tour_positions = get_section_positions('https://sakhva-travel.com/tour/kazbegi/')

print("\n=== DISCOVERING BLOG PAGE SECTIONS ===")
blog_positions = get_section_positions('https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/')
