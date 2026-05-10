"""Mobile visual audit for sakhva-travel.com — 4 pages, console errors, touch targets, text size"""
import json
from playwright.sync_api import sync_playwright

PAGES = [
    ("https://sakhva-travel.com/", "homepage"),
    ("https://sakhva-travel.com/tour/kazbegi/", "tour-kazbegi"),
    ("https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/", "blog-kazbegi"),
    ("https://sakhva-travel.com/en/tour/kazbegi/", "en-tour-kazbegi"),
]

OUT = "/Users/vladimir/sakhva-travel/screenshots/audit-mobile"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            is_mobile=True,
            has_touch=True,
        )

        for url, name in PAGES:
            page = context.new_page()

            errors = []
            page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda err: errors.append(f"[PAGE_ERROR] {err}"))

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"TIMEOUT {name}: {e}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                except:
                    print(f"FAILED {name}")
                    page.close()
                    continue

            page.screenshot(path=f"{OUT}/{name}-above-fold.png", full_page=False)
            page.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)

            small_targets = page.evaluate("""() => {
                const issues = [];
                const clickables = document.querySelectorAll('a, button, input, select, textarea, [role="button"], [onclick]');
                clickables.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
                        const text = (el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 50);
                        issues.push({tag: el.tagName, text: text, width: Math.round(rect.width), height: Math.round(rect.height), href: el.getAttribute('href') || ''});
                    }
                });
                return issues;
            }""")

            small_text = page.evaluate("""() => {
                const issues = [];
                const all = document.querySelectorAll('p, span, a, li, td, th, label, div');
                const seen = new Set();
                all.forEach(el => {
                    const style = window.getComputedStyle(el);
                    const size = parseFloat(style.fontSize);
                    if (size > 0 && size < 14 && el.textContent.trim().length > 5) {
                        const key = size.toFixed(0) + '-' + el.tagName;
                        if (!seen.has(key)) { seen.add(key); issues.push({tag: el.tagName, fontSize: Math.round(size*10)/10, text: el.textContent.trim().slice(0, 40)}); }
                    }
                });
                return issues.slice(0, 20);
            }""")

            h_overflow = page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")

            broken_images = page.evaluate("""() => {
                const issues = [];
                document.querySelectorAll('img').forEach(img => { if (!img.complete || img.naturalWidth === 0) issues.push({src: img.src.slice(0, 100), alt: img.alt || ''}); });
                return issues;
            }""")

            h1_visible = page.evaluate("""() => {
                const h1 = document.querySelector('h1');
                if (!h1) return {exists: false};
                const rect = h1.getBoundingClientRect();
                return {exists: true, text: h1.textContent.trim().slice(0, 80), visible_above_fold: rect.top < 812 && rect.bottom > 0, top: Math.round(rect.top)};
            }""")

            cta_visible = page.evaluate("""() => {
                const btns = document.querySelectorAll('a.btn, a.cta, button, .btn, [class*="book"], [class*="whatsapp"], [class*="fab"]');
                const results = [];
                btns.forEach(b => { const rect = b.getBoundingClientRect(); if (rect.width > 0) results.push({text: b.textContent.trim().slice(0, 40), visible_above_fold: rect.top < 812, top: Math.round(rect.top)}); });
                return results.slice(0, 8);
            }""")

            print(f"\n{'='*60}")
            print(f"PAGE: {name} ({url})")
            print(f"{'='*60}")
            print(f"H1: {json.dumps(h1_visible, ensure_ascii=False)}")
            print(f"CTA: {json.dumps(cta_visible, ensure_ascii=False, indent=2)}")
            print(f"Horizontal overflow: {h_overflow}")
            print(f"Broken images: {json.dumps(broken_images, ensure_ascii=False)}")
            print(f"Console errors ({len(errors)}):")
            for e in errors[:10]:
                print(f"  {e}")
            print(f"Small touch targets ({len(small_targets)}):")
            for t in small_targets[:10]:
                print(f"  {t['tag']} '{t['text'][:30]}' {t['width']}x{t['height']}px")
            if len(small_targets) > 10:
                print(f"  ... and {len(small_targets)-10} more")
            print(f"Small text ({len(small_text)}):")
            for t in small_text[:10]:
                print(f"  {t['tag']} {t['fontSize']}px: '{t['text']}'")

            page.close()

        browser.close()

if __name__ == "__main__":
    run()
