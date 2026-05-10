from playwright.sync_api import sync_playwright

URL = "https://sakhva-travel.com"

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop check
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    # Music toggle - search broadly
    music_els = page.query_selector_all('[class*="music"], [class*="audio"], [class*="sound"], [id*="music"], [id*="audio"], [id*="sound"], button[aria-label*="music"], button[aria-label*="sound"]')
    print(f"Music elements found: {len(music_els)}")
    for el in music_els:
        print(f"  tag={el.evaluate('e => e.tagName')}, class={el.get_attribute('class')}, id={el.get_attribute('id')}, visible={el.is_visible()}")

    # Also check all buttons
    buttons = page.query_selector_all('button')
    print(f"\nTotal buttons: {len(buttons)}")
    for b in buttons:
        cls = b.get_attribute('class') or ''
        iid = b.get_attribute('id') or ''
        aria = b.get_attribute('aria-label') or ''
        text = b.inner_text()[:50] if b.inner_text() else ''
        if any(kw in (cls + iid + aria + text).lower() for kw in ['music', 'sound', 'audio', 'mute', 'play']):
            print(f"  MUSIC-RELATED: class={cls}, id={iid}, aria={aria}, text={text}, visible={b.is_visible()}")

    # Nav links
    nav_links = page.query_selector_all('nav a, header a')
    print(f"\nNav links: {len(nav_links)}")
    for l in nav_links:
        print(f"  {l.inner_text()[:30]} -> {l.get_attribute('href')}")

    # FAB on mobile
    page.close()
    page = browser.new_page(viewport={"width": 375, "height": 812})
    page.goto(URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    fab = page.query_selector('#fab-main')
    print(f"\nFAB #fab-main: found={fab is not None}, visible={fab.is_visible() if fab else 'N/A'}")

    # Check horizontal scroll
    has_h_scroll = page.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth')
    print(f"Horizontal scroll on mobile: {has_h_scroll}")

    # Check H1
    h1 = page.query_selector('h1')
    print(f"H1 text: {h1.inner_text() if h1 else 'NOT FOUND'}")
    if h1:
        bbox = h1.bounding_box()
        print(f"H1 bounding box: {bbox}")
        print(f"H1 visible above fold (y < 812): {bbox['y'] < 812 if bbox else 'unknown'}")

    browser.close()
