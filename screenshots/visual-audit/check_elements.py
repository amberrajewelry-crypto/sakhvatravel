from playwright.sync_api import sync_playwright
import json

def check_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Mobile check
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)

        # Check tap targets (buttons, links)
        tap_targets = page.evaluate("""() => {
            const results = [];
            const els = document.querySelectorAll('a, button, [onclick], input, select, textarea, [role="button"]');
            els.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    results.push({
                        tag: el.tagName,
                        text: el.textContent?.trim().substring(0, 50),
                        class: el.className?.substring?.(0, 60) || '',
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        top: Math.round(rect.top + window.scrollY),
                        tooSmall: rect.width < 44 || rect.height < 44
                    });
                }
            });
            return results;
        }""")

        # Check font sizes
        fonts = page.evaluate("""() => {
            const results = [];
            const els = document.querySelectorAll('h1, h2, h3, p, span, a, li, button');
            const seen = new Set();
            els.forEach(el => {
                const style = window.getComputedStyle(el);
                const key = el.tagName + '_' + style.fontSize;
                if (!seen.has(key) && el.textContent?.trim()) {
                    seen.add(key);
                    results.push({
                        tag: el.tagName,
                        text: el.textContent?.trim().substring(0, 40),
                        fontSize: style.fontSize,
                        lineHeight: style.lineHeight,
                        color: style.color,
                        fontWeight: style.fontWeight
                    });
                }
            });
            return results;
        }""")

        # Check for horizontal overflow
        overflow = page.evaluate("""() => {
            return {
                bodyWidth: document.body.scrollWidth,
                viewportWidth: window.innerWidth,
                hasHorizontalScroll: document.body.scrollWidth > window.innerWidth
            };
        }""")

        # Cookie banner check
        cookie = page.evaluate("""() => {
            const els = document.querySelectorAll('[class*="cookie"], [id*="cookie"], [class*="consent"], [class*="gdpr"]');
            return {
                found: els.length > 0,
                elements: Array.from(els).map(e => ({
                    tag: e.tagName,
                    class: e.className,
                    visible: e.offsetParent !== null,
                    text: e.textContent?.trim().substring(0, 100)
                }))
            };
        }""")

        # Music toggle
        music = page.evaluate("""() => {
            const els = document.querySelectorAll('[class*="music"], [id*="music"], [class*="sound"], [class*="audio"], audio');
            return {
                found: els.length > 0,
                elements: Array.from(els).map(e => {
                    const rect = e.getBoundingClientRect();
                    return {
                        tag: e.tagName,
                        class: e.className,
                        id: e.id,
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        visible: e.offsetParent !== null || e.tagName === 'AUDIO'
                    };
                })
            };
        }""")

        # Overlapping check - z-index analysis
        zindex = page.evaluate("""() => {
            const results = [];
            const els = document.querySelectorAll('*');
            els.forEach(el => {
                const style = window.getComputedStyle(el);
                const z = parseInt(style.zIndex);
                if (!isNaN(z) && z > 0 && style.position !== 'static') {
                    const rect = el.getBoundingClientRect();
                    results.push({
                        tag: el.tagName,
                        class: el.className?.substring?.(0, 60) || '',
                        zIndex: z,
                        position: style.position,
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        top: Math.round(rect.top + window.scrollY)
                    });
                }
            });
            return results.sort((a, b) => b.zIndex - a.zIndex).slice(0, 20);
        }""")

        page.close()
        browser.close()

        print("=== TAP TARGETS (too small) ===")
        small = [t for t in tap_targets if t['tooSmall']]
        for t in small[:20]:
            print(f"  {t['tag']} [{t['width']}x{t['height']}] - {t['text'][:40]} (class: {t['class'][:40]})")
        print(f"  Total small: {len(small)} / {len(tap_targets)}")

        print("\n=== FONT SIZES ===")
        for f in fonts[:20]:
            print(f"  {f['tag']} {f['fontSize']} / {f['lineHeight']} weight={f['fontWeight']} - {f['text'][:30]}")

        print(f"\n=== HORIZONTAL OVERFLOW ===")
        print(f"  Body: {overflow['bodyWidth']}px, Viewport: {overflow['viewportWidth']}px, Overflow: {overflow['hasHorizontalScroll']}")

        print(f"\n=== COOKIE BANNER ===")
        print(f"  Found: {cookie['found']}")
        for e in cookie['elements']:
            print(f"  {e['tag']} visible={e['visible']} - {e['text'][:60]}")

        print(f"\n=== MUSIC TOGGLE ===")
        print(f"  Found: {music['found']}")
        for e in music['elements']:
            print(f"  {e['tag']} [{e['width']}x{e['height']}] visible={e['visible']} id={e['id']} class={e['class'][:40]}")

        print(f"\n=== Z-INDEX LAYERS (top 20) ===")
        for z in zindex:
            print(f"  z={z['zIndex']} {z['tag']} [{z['width']}x{z['height']}] pos={z['position']} top={z['top']} class={z['class'][:40]}")

if __name__ == "__main__":
    check_elements()
