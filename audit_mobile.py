#!/usr/bin/env python3
"""
Mobile rendering and above-the-fold audit for sakhva-travel.com
"""

import json
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright required. Install with: pip install playwright && playwright install chromium")
    sys.exit(1)

PAGES = [
    {"slug": "homepage", "url": "https://sakhva-travel.com"},
    {"slug": "night-tbilisi", "url": "https://sakhva-travel.com/tour/night-tbilisi/"},
    {"slug": "photo-tour", "url": "https://sakhva-travel.com/tour/photo/"},
]

MOBILE_VIEWPORT = {"width": 375, "height": 812}
OUTPUT_DIR = "/Users/vladimir/sakhva-travel/screenshots"


def audit_page(page, url, slug):
    """Run all audit checks on a page and return results."""
    results = {
        "url": url,
        "slug": slug,
        "issues": [],
        "warnings": [],
        "passes": [],
    }

    # Navigate
    page.goto(url, wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(1500)

    # ── 1. Horizontal overflow check ──────────────────────────────────────────
    overflow_data = page.evaluate("""() => {
        const bodyWidth = document.body.scrollWidth;
        const viewportWidth = window.innerWidth;
        const overflowing = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > viewportWidth + 2) {
                overflowing.push({
                    tag: el.tagName,
                    id: el.id || '',
                    classes: el.className && typeof el.className === 'string' ? el.className.trim().substring(0, 80) : '',
                    right: Math.round(rect.right),
                    width: Math.round(rect.width),
                    overflowBy: Math.round(rect.right - viewportWidth)
                });
            }
        });
        return {bodyScrollWidth: bodyWidth, viewportWidth, overflowing: overflowing.slice(0, 10)};
    }""")

    if overflow_data["bodyScrollWidth"] > overflow_data["viewportWidth"] + 2:
        results["issues"].append({
            "type": "horizontal_overflow",
            "severity": "HIGH",
            "detail": f"body.scrollWidth={overflow_data['bodyScrollWidth']}px exceeds viewport {overflow_data['viewportWidth']}px",
            "elements": overflow_data["overflowing"],
        })
    else:
        results["passes"].append("No horizontal overflow detected")

    # ── 2. Above-the-fold: H1 visibility ─────────────────────────────────────
    h1_data = page.evaluate("""() => {
        const h1 = document.querySelector('h1');
        if (!h1) return {found: false};
        const rect = h1.getBoundingClientRect();
        const style = window.getComputedStyle(h1);
        return {
            found: true,
            text: h1.textContent.trim().substring(0, 80),
            top: Math.round(rect.top),
            bottom: Math.round(rect.bottom),
            visible: rect.top < window.innerHeight && rect.bottom > 0,
            fontSize: style.fontSize,
            color: style.color,
            classes: h1.className || ''
        };
    }""")

    if not h1_data["found"]:
        results["issues"].append({"type": "missing_h1", "severity": "HIGH", "detail": "No H1 found on page"})
    elif not h1_data["visible"]:
        results["issues"].append({
            "type": "h1_below_fold",
            "severity": "HIGH",
            "detail": f"H1 '{h1_data['text']}' not visible above fold (top={h1_data['top']}px)",
            "element": "h1",
        })
    else:
        results["passes"].append(
            f"H1 visible above fold: '{h1_data['text']}' (top={h1_data['top']}px, font={h1_data['fontSize']})"
        )

    # ── 3. CTA button visibility above fold ───────────────────────────────────
    cta_data = page.evaluate("""() => {
        const selectors = [
            'a.btn', 'button.btn', '.cta', 'a[class*="button"]', 'button',
            'a[class*="cta"]', '.hero a', '.hero button',
            'a[class*="btn"]', '[class*="book"]', '[class*="reserve"]',
            'a[href*="book"]', 'a[href*="contact"]', 'a[href*="tour"]'
        ];
        const btns = [];
        const seen = new Set();
        for (const sel of selectors) {
            document.querySelectorAll(sel).forEach(el => {
                if (seen.has(el)) return;
                seen.add(el);
                const rect = el.getBoundingClientRect();
                if (rect.width === 0) return;
                const style = window.getComputedStyle(el);
                btns.push({
                    selector: sel,
                    tag: el.tagName,
                    text: el.textContent.trim().substring(0, 50),
                    top: Math.round(rect.top),
                    bottom: Math.round(rect.bottom),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    aboveFold: rect.top < window.innerHeight && rect.bottom > 0,
                    fontSize: style.fontSize,
                    classes: el.className && typeof el.className === 'string' ? el.className.trim().substring(0, 80) : ''
                });
            });
        }
        return btns.slice(0, 15);
    }""")

    above_fold_ctas = [b for b in cta_data if b["aboveFold"] and b["text"]]
    if not above_fold_ctas:
        results["issues"].append({
            "type": "no_cta_above_fold",
            "severity": "HIGH",
            "detail": "No CTA button/link visible above the fold",
        })
    else:
        results["passes"].append(
            f"{len(above_fold_ctas)} CTA(s) visible above fold: {[b['text'] for b in above_fold_ctas[:3]]}"
        )

    # ── 4. Touch target sizes ─────────────────────────────────────────────────
    touch_data = page.evaluate("""() => {
        const interactive = document.querySelectorAll('a, button, input, select, textarea, [role="button"]');
        const small = [];
        interactive.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) return;
            if (rect.width < 44 || rect.height < 44) {
                small.push({
                    tag: el.tagName,
                    text: el.textContent.trim().substring(0, 40),
                    href: el.href || '',
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    classes: el.className && typeof el.className === 'string' ? el.className.trim().substring(0, 60) : '',
                    top: Math.round(rect.top)
                });
            }
        });
        return small.slice(0, 15);
    }""")

    if touch_data:
        results["warnings"].append({
            "type": "small_touch_targets",
            "severity": "MEDIUM",
            "detail": f"{len(touch_data)} interactive elements smaller than 44x44px",
            "elements": touch_data,
        })
    else:
        results["passes"].append("All interactive elements meet 44px touch target minimum")

    # ── 5. Font size readability ───────────────────────────────────────────────
    font_data = page.evaluate("""() => {
        const small = [];
        const textNodes = document.querySelectorAll('p, span, li, td, div, a');
        textNodes.forEach(el => {
            if (!el.textContent.trim()) return;
            const style = window.getComputedStyle(el);
            const size = parseFloat(style.fontSize);
            if (size > 0 && size < 12) {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0) {
                    small.push({
                        tag: el.tagName,
                        text: el.textContent.trim().substring(0, 40),
                        fontSize: style.fontSize,
                        classes: el.className && typeof el.className === 'string' ? el.className.trim().substring(0, 60) : ''
                    });
                }
            }
        });
        return small.slice(0, 10);
    }""")

    if font_data:
        results["warnings"].append({
            "type": "small_font_size",
            "severity": "MEDIUM",
            "detail": f"{len(font_data)} elements with font-size < 12px (risk of unreadable text on mobile)",
            "elements": font_data,
        })
    else:
        results["passes"].append("No font sizes below 12px detected")

    # ── 6. Viewport meta tag ──────────────────────────────────────────────────
    viewport_meta = page.evaluate("""() => {
        const meta = document.querySelector('meta[name="viewport"]');
        return meta ? meta.getAttribute('content') : null;
    }""")

    if not viewport_meta:
        results["issues"].append({
            "type": "missing_viewport_meta",
            "severity": "CRITICAL",
            "detail": "No <meta name='viewport'> tag found — page will not scale on mobile",
        })
    elif "user-scalable=no" in viewport_meta or "maximum-scale=1" in viewport_meta:
        results["warnings"].append({
            "type": "zoom_disabled",
            "severity": "MEDIUM",
            "detail": f"Viewport meta disables zoom: '{viewport_meta}' — accessibility violation",
            "element": "meta[name='viewport']",
        })
    else:
        results["passes"].append(f"Viewport meta tag present: '{viewport_meta}'")

    # ── 7. Hero section check ─────────────────────────────────────────────────
    hero_data = page.evaluate("""() => {
        const heroSelectors = ['.hero', '#hero', '[class*="hero"]', '.banner', '[class*="banner"]',
                                '.jumbotron', '.masthead', 'header.page-header', '.page-header'];
        for (const sel of heroSelectors) {
            const el = document.querySelector(sel);
            if (el) {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                const img = el.querySelector('img');
                return {
                    found: true,
                    selector: sel,
                    top: Math.round(rect.top),
                    height: Math.round(rect.height),
                    backgroundImage: style.backgroundImage.substring(0, 100),
                    hasImg: !!img,
                    imgSrc: img ? img.src.substring(0, 80) : '',
                    visible: rect.top < window.innerHeight
                };
            }
        }
        return {found: false};
    }""")

    if not hero_data["found"]:
        results["warnings"].append({
            "type": "no_hero_section",
            "severity": "LOW",
            "detail": "No recognizable hero section (.hero, .banner, etc.) found",
        })
    elif not hero_data["visible"]:
        results["issues"].append({
            "type": "hero_not_visible",
            "severity": "HIGH",
            "detail": f"Hero section '{hero_data['selector']}' not visible above fold (top={hero_data['top']}px)",
        })
    else:
        results["passes"].append(
            f"Hero section visible: '{hero_data['selector']}' height={hero_data['height']}px"
        )

    # ── 8. Image scaling issues ───────────────────────────────────────────────
    img_data = page.evaluate("""() => {
        const issues = [];
        document.querySelectorAll('img').forEach(img => {
            const rect = img.getBoundingClientRect();
            if (rect.width > window.innerWidth + 2) {
                issues.push({
                    src: img.src.substring(0, 60),
                    alt: img.alt,
                    width: Math.round(rect.width),
                    naturalWidth: img.naturalWidth,
                    classes: img.className || ''
                });
            }
        });
        return issues.slice(0, 10);
    }""")

    if img_data:
        results["issues"].append({
            "type": "images_overflow",
            "severity": "HIGH",
            "detail": f"{len(img_data)} images wider than viewport",
            "elements": img_data,
        })
    else:
        results["passes"].append("All images fit within viewport width")

    # ── 9. Navigation accessibility on mobile ────────────────────────────────
    nav_data = page.evaluate("""() => {
        const nav = document.querySelector('nav, header');
        if (!nav) return {found: false};
        const hamburgerSel = '[class*="hamburger"],[class*="menu-toggle"],[class*="navbar-toggler"],[class*="mobile-menu"]';
        const hamburger = nav.querySelector(hamburgerSel);
        const rect = nav.getBoundingClientRect();
        return {
            found: true,
            hasHamburger: !!hamburger,
            hamburgerVisible: hamburger ? hamburger.getBoundingClientRect().width > 0 : false,
            navHeight: Math.round(rect.height),
            classes: nav.className && typeof nav.className === 'string' ? nav.className.trim().substring(0, 80) : ''
        };
    }""")

    if nav_data["found"]:
        if not nav_data["hasHamburger"]:
            results["warnings"].append({
                "type": "no_hamburger_menu",
                "severity": "MEDIUM",
                "detail": (
                    f"No hamburger/mobile menu toggle found in nav "
                    f"(nav height={nav_data['navHeight']}px). Full nav may render raw on mobile."
                ),
                "element": f"nav / header .{nav_data['classes'][:40]}",
            })
        else:
            results["passes"].append(
                f"Mobile hamburger menu present (visible={nav_data['hamburgerVisible']})"
            )

    # ── 10. Text contrast – basic check ───────────────────────────────────────
    contrast_data = page.evaluate("""() => {
        const issues = [];
        document.querySelectorAll('p, h1, h2, h3, h4, span, a, button').forEach(el => {
            if (!el.textContent.trim()) return;
            const style = window.getComputedStyle(el);
            const color = style.color;
            const match = color.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
            if (match) {
                const r = parseInt(match[1]), g = parseInt(match[2]), b = parseInt(match[3]);
                const luminance = (0.299*r + 0.587*g + 0.114*b);
                if (luminance > 200) {
                    const bg = window.getComputedStyle(el).backgroundColor;
                    const bgMatch = bg.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
                    if (bgMatch) {
                        const br = parseInt(bgMatch[1]), bg2 = parseInt(bgMatch[2]), bb = parseInt(bgMatch[3]);
                        const bgLum = (0.299*br + 0.587*bg2 + 0.114*bb);
                        if (bgLum > 180) {
                            issues.push({
                                tag: el.tagName,
                                text: el.textContent.trim().substring(0, 30),
                                color: color,
                                bg: bg,
                                classes: el.className && typeof el.className === 'string' ? el.className.trim().substring(0, 50) : ''
                            });
                        }
                    }
                }
            }
        });
        return issues.slice(0, 8);
    }""")

    if contrast_data:
        results["warnings"].append({
            "type": "potential_contrast_issues",
            "severity": "MEDIUM",
            "detail": f"{len(contrast_data)} elements may have low contrast (light text on light background)",
            "elements": contrast_data,
        })
    else:
        results["passes"].append("No obvious contrast issues detected")

    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for page_info in PAGES:
            print(f"\n{'='*60}")
            print(f"Auditing: {page_info['url']}")
            print(f"{'='*60}")

            context_mobile = browser.new_context(
                viewport=MOBILE_VIEWPORT,
                device_scale_factor=2,
                user_agent=(
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/15E148 Safari/604.1"
                ),
            )
            page_mobile = context_mobile.new_page()

            result = audit_page(page_mobile, page_info["url"], page_info["slug"])

            # Screenshot above fold
            shot_atf = f"{OUTPUT_DIR}/{page_info['slug']}_mobile_atf.png"
            page_mobile.screenshot(path=shot_atf, full_page=False)
            result["screenshot_atf"] = shot_atf

            # Screenshot full page
            shot_full = f"{OUTPUT_DIR}/{page_info['slug']}_mobile_full.png"
            page_mobile.screenshot(path=shot_full, full_page=True)
            result["screenshot_full"] = shot_full

            context_mobile.close()
            all_results.append(result)

            print(f"  Issues:   {len(result['issues'])}")
            print(f"  Warnings: {len(result['warnings'])}")
            print(f"  Passes:   {len(result['passes'])}")

        browser.close()

    # Save JSON report
    report_path = f"{OUTPUT_DIR}/audit_report.json"
    with open(report_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nReport saved to: {report_path}")

    return all_results


if __name__ == "__main__":
    main()
