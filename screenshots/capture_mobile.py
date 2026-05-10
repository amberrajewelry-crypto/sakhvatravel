from playwright.sync_api import sync_playwright
import time

URL = "https://sakhva-travel.com"
OUT = "/Users/vladimir/sakhva-travel/screenshots"
W, H = 375, 812

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    page.goto(URL, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    # 1. Hero section (above the fold)
    page.screenshot(path=f"{OUT}/01_hero.png", full_page=False)
    print("1. Hero done")

    # 2. Tours section
    tours = page.query_selector("#tours") or page.query_selector("[id*='tour']") or page.query_selector(".tours")
    if tours:
        tours.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{OUT}/02_tours.png", full_page=False)
        print("2. Tours done (selector found)")
    else:
        page.evaluate("window.scrollTo(0, window.innerHeight * 1.5)")
        time.sleep(1)
        page.screenshot(path=f"{OUT}/02_tours.png", full_page=False)
        print("2. Tours done (manual scroll)")

    # 3. Reviews section
    reviews = page.query_selector("#reviews") or page.query_selector("[id*='review']") or page.query_selector(".reviews")
    if reviews:
        reviews.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{OUT}/03_reviews.png", full_page=False)
        print("3. Reviews done (selector found)")
    else:
        page.evaluate("window.scrollTo(0, window.innerHeight * 3)")
        time.sleep(1)
        page.screenshot(path=f"{OUT}/03_reviews.png", full_page=False)
        print("3. Reviews done (manual scroll)")

    # 4. FAQ section
    faq = page.query_selector("#faq") or page.query_selector("[id*='faq']") or page.query_selector(".faq")
    if faq:
        faq.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{OUT}/04_faq.png", full_page=False)
        print("4. FAQ done (selector found)")
    else:
        page.evaluate("window.scrollTo(0, window.innerHeight * 4.5)")
        time.sleep(1)
        page.screenshot(path=f"{OUT}/04_faq.png", full_page=False)
        print("4. FAQ done (manual scroll)")

    # 5. Footer
    footer = page.query_selector("footer") or page.query_selector("#footer")
    if footer:
        footer.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=f"{OUT}/05_footer.png", full_page=False)
        print("5. Footer done (selector found)")
    else:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        page.screenshot(path=f"{OUT}/05_footer.png", full_page=False)
        print("5. Footer done (scroll to bottom)")

    # 6. Hamburger menu
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    hamburger = page.query_selector(".hamburger") or page.query_selector("[class*='burger']") or page.query_selector("[class*='menu-toggle']") or page.query_selector("button[aria-label*='menu']") or page.query_selector(".mobile-menu-btn") or page.query_selector("nav button") or page.query_selector(".nav-toggle")
    if hamburger:
        hamburger.click()
        time.sleep(1)
        page.screenshot(path=f"{OUT}/06_hamburger_menu.png", full_page=False)
        print("6. Hamburger menu done (clicked)")
    else:
        all_btns = page.query_selector_all("header button, header [role='button'], header .btn")
        print(f"   Found {len(all_btns)} header buttons")
        for btn in all_btns:
            txt = btn.inner_text().strip()
            cls = btn.get_attribute("class") or ""
            print(f"   Button: text='{txt}', class='{cls}'")
        svg_btn = page.query_selector("header svg")
        if svg_btn:
            parent = svg_btn.evaluate_handle("el => el.closest('button') || el.closest('a') || el.parentElement")
            if parent:
                parent.as_element().click()
                time.sleep(1)
                page.screenshot(path=f"{OUT}/06_hamburger_menu.png", full_page=False)
                print("6. Hamburger menu done (svg parent clicked)")
        else:
            page.screenshot(path=f"{OUT}/06_hamburger_menu.png", full_page=False)
            print("6. Hamburger - could not find toggle")

    # Full page for reference
    page.screenshot(path=f"{OUT}/00_full_page.png", full_page=True)
    print("Full page screenshot done")

    browser.close()
    print("All done!")
