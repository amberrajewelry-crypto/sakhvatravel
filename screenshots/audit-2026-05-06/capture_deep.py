#!/usr/bin/env python3
"""Deep mobile audit — tour page scroll states, FAB, sticky bar, booking form"""

from playwright.sync_api import sync_playwright
import time

DIR = "/Users/vladimir/sakhva-travel/screenshots/audit-2026-05-06"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
VP = {"width": 390, "height": 844}

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport=VP, user_agent=UA)
        page = ctx.new_page()

        # Tour page — scroll to booking form area
        page.goto("https://sakhva-travel.com/tour/kazbegi/", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Check sticky bar visibility and FAB
        sticky_info = page.evaluate("""() => {
            const sticky = document.querySelector('.mobile-sticky-bar, [class*="sticky"], [id*="sticky"]');
            const fab = document.querySelector('#fab-main, .fab, [id*="fab"]');
            const bookBtn = document.querySelector('.book-btn, [class*="book"], button[class*="cta"]');
            const cookieBanner = document.querySelector('[class*="cookie"], #cookie-banner, .cookie-consent');
            return {
                stickyBar: sticky ? {
                    tag: sticky.tagName,
                    className: sticky.className,
                    id: sticky.id,
                    rect: sticky.getBoundingClientRect(),
                    visible: sticky.offsetHeight > 0
                } : null,
                fab: fab ? {
                    tag: fab.tagName,
                    className: fab.className,
                    id: fab.id,
                    rect: fab.getBoundingClientRect(),
                    visible: fab.offsetHeight > 0
                } : null,
                cookieBanner: cookieBanner ? {
                    rect: cookieBanner.getBoundingClientRect(),
                    visible: cookieBanner.offsetHeight > 0
                } : null
            }
        }""")
        print(f"STICKY/FAB INFO (tour top): {sticky_info}")

        # Scroll to booking form
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.6)")
        time.sleep(1)
        page.screenshot(path=f"{DIR}/mobile_tour_booking_area.png")
        print(f"Saved: mobile_tour_booking_area.png")

        # Check for sticky bar at scroll position
        sticky_scrolled = page.evaluate("""() => {
            const sticky = document.querySelector('.mobile-sticky-bar, [class*="sticky-bar"], [class*="sticky_bar"]');
            const allSticky = Array.from(document.querySelectorAll('*')).filter(el => {
                const style = window.getComputedStyle(el);
                return (style.position === 'sticky' || style.position === 'fixed') && el.offsetHeight > 0;
            }).map(el => ({
                tag: el.tagName,
                id: el.id,
                className: el.className.substring(0, 80),
                rect: el.getBoundingClientRect(),
                position: window.getComputedStyle(el).position
            }));
            return { sticky, allSticky };
        }""")
        print(f"ALL FIXED/STICKY ELEMENTS (tour scrolled): {len(sticky_scrolled['allSticky'])} found")
        for el in sticky_scrolled['allSticky']:
            print(f"  - {el['position']} | #{el['id']} .{el['className'][:50]} rect={el['rect']}")

        # Home page — check FAB and cookie overlap
        page.goto("https://sakhva-travel.com", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        overlap_check = page.evaluate("""() => {
            const fixed_els = Array.from(document.querySelectorAll('*')).filter(el => {
                const style = window.getComputedStyle(el);
                return (style.position === 'fixed') && el.offsetHeight > 0 && el.offsetWidth > 0;
            }).map(el => ({
                id: el.id,
                className: el.className.substring(0, 60),
                rect: el.getBoundingClientRect(),
                zIndex: window.getComputedStyle(el).zIndex,
                bottom: el.getBoundingClientRect().bottom
            }));

            // Check for overlaps
            const overlaps = [];
            for (let i = 0; i < fixed_els.length; i++) {
                for (let j = i+1; j < fixed_els.length; j++) {
                    const a = fixed_els[i].rect;
                    const b = fixed_els[j].rect;
                    const aRect = fixed_els[i].rect;
                    const bRect = fixed_els[j].rect;
                    if (!(aRect.right < bRect.left || aRect.left > bRect.right ||
                          aRect.bottom < bRect.top || aRect.top > bRect.bottom)) {
                        overlaps.push({a: fixed_els[i].id || fixed_els[i].className.substring(0,30),
                                       b: fixed_els[j].id || fixed_els[j].className.substring(0,30)});
                    }
                }
            }
            return { fixed_els, overlaps };
        }""")
        print(f"\nFIXED ELEMENTS on home: {len(overlap_check['fixed_els'])} found")
        for el in overlap_check['fixed_els']:
            r = el['rect']
            print(f"  #{el['id']} .{el['className'][:40]} | z:{el['zIndex']} | top:{r['top']:.0f} left:{r['left']:.0f} w:{r['width']:.0f} h:{r['height']:.0f}")
        print(f"OVERLAPS: {overlap_check['overlaps']}")

        # Check touch target sizes for CTA buttons
        touch_targets = page.evaluate("""() => {
            const buttons = Array.from(document.querySelectorAll('button, a[href], input[type="submit"]'));
            return buttons.filter(el => el.offsetHeight > 0).map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    text: (el.textContent || el.value || '').trim().substring(0, 30),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    tooSmall: rect.width < 44 || rect.height < 44
                }
            }).filter(el => el.tooSmall);
        }""")
        print(f"\nTOUCH TARGETS TOO SMALL (<44px) on home: {len(touch_targets)}")
        for t in touch_targets[:15]:
            print(f"  {t['tag']} '{t['text'][:25]}' {t['w']}x{t['h']}")

        # Check font sizes
        font_check = page.evaluate("""() => {
            const textEls = Array.from(document.querySelectorAll('p, span, li, a, label'));
            const small = textEls.filter(el => {
                if (el.offsetHeight === 0) return false;
                const fs = parseFloat(window.getComputedStyle(el).fontSize);
                return fs < 14;
            }).map(el => ({
                tag: el.tagName,
                text: el.textContent.trim().substring(0, 30),
                fontSize: parseFloat(window.getComputedStyle(el).fontSize)
            }));
            return small;
        }""")
        print(f"\nFONT < 14px on home mobile: {len(font_check)}")
        for f in font_check[:10]:
            print(f"  {f['tag']} '{f['text'][:25]}' = {f['fontSize']}px")

        browser.close()
        print("\nDone.")

if __name__ == "__main__":
    run()
