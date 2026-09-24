"""
Visual & Mobile SEO Audit — sakhva-travel.com
Captures desktop (1440x900) and mobile (390x844) screenshots for 3 pages.
"""

from playwright.sync_api import sync_playwright
import os, time, json

PAGES = [
    ("homepage",  "https://sakhva-travel.com/"),
    ("kazbegi_tour", "https://sakhva-travel.com/tour/kazbegi/"),
    ("kazbegi_blog", "https://sakhva-travel.com/blog/kazbegi-iz-tbilisi-2026/"),
]

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("mobile",  390,  844),
]

OUT = "/Users/vladimir/sakhva-travel/screenshots"
os.makedirs(OUT, exist_ok=True)

metrics = {}

def run():
    with sync_playwright() as p:
        for vp_name, w, h in VIEWPORTS:
            browser = p.chromium.launch(args=["--no-sandbox"])
            ctx = browser.new_context(
                viewport={"width": w, "height": h},
                user_agent=(
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
                    if vp_name == "mobile" else
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                ),
            )

            for slug, url in PAGES:
                page = ctx.new_page()
                t0 = time.time()

                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                load_time = round((time.time() - t0) * 1000)

                # --- above-the-fold screenshot (viewport only) ---
                atf_path = f"{OUT}/{slug}_{vp_name}_atf.png"
                page.screenshot(path=atf_path, full_page=False)

                # --- full-page screenshot ---
                full_path = f"{OUT}/{slug}_{vp_name}_full.png"
                page.screenshot(path=full_path, full_page=True)

                # --- DOM metrics ---
                data = page.evaluate("""() => {
                    const h1 = document.querySelector('h1');
                    const h1Rect = h1 ? h1.getBoundingClientRect() : null;

                    // Find primary CTA buttons
                    const ctaBtns = [...document.querySelectorAll(
                        'a[href*="book"], a[href*="tour"], button, .cta, .btn, [class*="book"], [class*="cta"]'
                    )].filter(el => {
                        const r = el.getBoundingClientRect();
                        return r.width > 0 && r.height > 0;
                    });
                    const firstCta = ctaBtns[0];
                    const ctaRect  = firstCta ? firstCta.getBoundingClientRect() : null;

                    // Nav / burger
                    const nav    = document.querySelector('nav, header nav, .nav, #nav');
                    const burger = document.querySelector(
                        '.burger, .hamburger, [class*="burger"], [class*="menu-icon"], [class*="nav-toggle"], button[aria-label*="menu"]'
                    );

                    // Lang switcher
                    const lang = document.querySelector(
                        '.lang, [class*="lang"], [class*="language"], select[name*="lang"]'
                    );

                    // Hero video
                    const video = document.querySelector('video');
                    const videoRect = video ? video.getBoundingClientRect() : null;

                    // Touch targets: buttons/links smaller than 44px
                    const allTouchTargets = [...document.querySelectorAll('a, button')].filter(el => {
                        const r = el.getBoundingClientRect();
                        return r.width > 0 && r.height > 0;
                    });
                    const smallTargets = allTouchTargets.filter(el => {
                        const r = el.getBoundingClientRect();
                        return r.width < 44 || r.height < 44;
                    });

                    // Images: check loading attribute and src format
                    const imgs = [...document.querySelectorAll('img')];
                    const lazyImgs   = imgs.filter(i => i.loading === 'lazy').length;
                    const webpImgs   = imgs.filter(i => (i.currentSrc || i.src || '').includes('.webp')).length;
                    const noAltImgs  = imgs.filter(i => !i.alt).length;

                    // OG tags
                    const ogImage = document.querySelector('meta[property="og:image"]');
                    const ogTitle = document.querySelector('meta[property="og:title"]');
                    const ogDesc  = document.querySelector('meta[property="og:description"]');

                    // Canonical
                    const canonical = document.querySelector('link[rel="canonical"]');

                    // Font size on body
                    const bodyFontSize = parseFloat(getComputedStyle(document.body).fontSize);

                    // Viewport meta
                    const viewportMeta = document.querySelector('meta[name="viewport"]');

                    return {
                        title:          document.title,
                        h1_text:        h1 ? h1.innerText.trim() : null,
                        h1_in_viewport: h1Rect ? (h1Rect.top >= 0 && h1Rect.bottom <= window.innerHeight) : false,
                        h1_top:         h1Rect ? Math.round(h1Rect.top) : null,

                        first_cta_text:       firstCta ? firstCta.innerText.trim().substring(0, 60) : null,
                        cta_in_viewport:      ctaRect ? (ctaRect.top >= 0 && ctaRect.bottom <= window.innerHeight) : false,
                        cta_top:              ctaRect ? Math.round(ctaRect.top) : null,

                        nav_found:     !!nav,
                        burger_found:  !!burger,
                        lang_found:    !!lang,

                        video_found:        !!video,
                        video_in_viewport:  videoRect ? (videoRect.top < window.innerHeight && videoRect.bottom > 0) : false,
                        video_autoplay:     video ? video.autoplay : false,
                        video_muted:        video ? video.muted : false,

                        total_touch_targets: allTouchTargets.length,
                        small_touch_targets: smallTargets.length,
                        small_target_examples: smallTargets.slice(0, 3).map(el => ({
                            tag:  el.tagName,
                            text: el.innerText.trim().substring(0, 40),
                            w:    Math.round(el.getBoundingClientRect().width),
                            h:    Math.round(el.getBoundingClientRect().height),
                        })),

                        total_images: imgs.length,
                        lazy_images:  lazyImgs,
                        webp_images:  webpImgs,
                        no_alt_images: noAltImgs,

                        og_image:   ogImage ? ogImage.content : null,
                        og_title:   ogTitle ? ogTitle.content : null,
                        og_desc:    ogDesc  ? ogDesc.content  : null,

                        canonical:      canonical ? canonical.href : null,
                        body_font_size: bodyFontSize,
                        viewport_meta:  viewportMeta ? viewportMeta.content : null,

                        page_height:    document.body.scrollHeight,
                        viewport_h:     window.innerHeight,
                        viewport_w:     window.innerWidth,
                    };
                }""")

                key = f"{slug}_{vp_name}"
                metrics[key] = {"load_ms": load_time, **data}
                print(f"[OK] {key} — {load_time}ms")

                page.close()

            ctx.close()
            browser.close()

    with open(f"{OUT}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("\nDone. Files written to:", OUT)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run()
