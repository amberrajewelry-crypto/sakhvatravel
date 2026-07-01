#!/usr/bin/env python3
"""Upgrade EN tour pages + geo pages to match Kazbegi standard.
Same fixes: colors, fonts, CTA text, booking link, animations."""

import json, os, re, glob

ROOT = os.path.expanduser("~/sakhva-travel")

with open(os.path.join(ROOT, "data/catalog.json")) as f:
    catalog = {e["slug"]: e for e in json.load(f)["excursions"]}

# Collect all target pages
en_tours = sorted(glob.glob(os.path.join(ROOT, "en/ekskursiya/*/index.html")))
geo_ru = sorted(glob.glob(os.path.join(ROOT, "tury-v-gruziyu-iz-*/index.html")))
geo_en = sorted(glob.glob(os.path.join(ROOT, "en/tours-from-*/index.html")))

all_pages = en_tours + geo_ru + geo_en
stats = {"total": 0, "updated": 0}

for path in all_pages:
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    # Determine slug for booking link
    slug = ""
    if "/en/ekskursiya/" in path:
        slug = path.split("/en/ekskursiya/")[1].split("/")[0]
    elif "tury-v-gruziyu-iz-" in path:
        slug = path.split("/")[-2]
    elif "tours-from-" in path:
        slug = path.split("/")[-2]

    info = catalog.get(slug, {})
    price = info.get("price", "")

    # === STEP 1: Colors ===
    html = html.replace("#1A56DB", "#1A3D2E")
    html = html.replace("#1E429F", "#1A3D2E")
    html = html.replace("#1F2937", "#1A3D2E")
    html = html.replace("background:#D4845A", "background:#1A3D2E")
    html = html.replace("rgba(212,132,90,.35)", "rgba(26,61,46,.35)")

    # === STEP 2: Fonts — preload+onload → blocking ===
    html = re.sub(
        r'<link\s+rel="preload"\s+href="(/fonts/[^"]+)"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        r'<link rel="stylesheet" href="\1">',
        html
    )
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="/fonts/[^"]*"></noscript>', '', html)
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="/fonts/[^"]*"><link rel="stylesheet" href="/fonts/[^"]*"></noscript>', '', html)
    html = re.sub(
        r'<link\s+rel="preload"\s+as="style"\s+href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        '', html
    )
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"></noscript>', '', html)
    html = re.sub(
        r'<link\s+rel="preload"\s+href="https://fonts\.googleapis\.com/css2\?family=Raleway[^"]*"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        '', html
    )
    html = re.sub(
        r'<link\s+rel="preload"\s+href="/fonts/montserrat\.css"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        '', html
    )

    # === STEP 3: CTA text fixes (EN) ===
    html = html.replace('>Get 10% discount<', '>Get 10% off — leave a request<')
    html = html.replace('>Получить скидку 10%<', '>Скидка 10% — оставить заявку<')
    html = re.sub(r'Получить скидку 10%', 'Скидка 10% — оставить заявку', html)

    # === STEP 4: Add scroll animations if missing ===
    if '[data-anim]' not in html:
        anim_css = '''/* Scroll animations */
[data-anim]{opacity:0;transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1)}
[data-anim].is-vis{opacity:1;transform:none}
[data-anim="up"]{transform:translateY(40px)}
[data-anim="fade"]{transform:none}
[data-anim-d="1"]{transition-delay:.1s}[data-anim-d="2"]{transition-delay:.2s}[data-anim-d="3"]{transition-delay:.3s}'''
        html = html.replace('</style>', anim_css + '\n</style>', 1)

    html = re.sub(r'<div class="article-wrap"(?!\s+data-anim)', '<div class="article-wrap" data-anim="up"', html)
    html = re.sub(r'<section class="section"(?![^>]*data-anim)', '<section class="section" data-anim="up"', html)
    html = re.sub(r'<div class="callout-box([^"]*)"(?![^>]*data-anim)', r'<div class="callout-box\1" data-anim="up"', html)
    html = re.sub(r'<div class="callout-why"(?![^>]*data-anim)', '<div class="callout-why" data-anim="up"', html)

    if 'data-anim' in html and "querySelectorAll('[data-anim]')" not in html:
        anim_script = '''<script>
!function(){var els=document.querySelectorAll('[data-anim]');if(!els.length)return;var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-vis');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -40px 0px'});els.forEach(function(el){io.observe(el)})}();
</script>'''
        html = html.replace('</body>', anim_script + '\n</body>')

    # === STEP 5: Add booking link if missing (EN tours only) ===
    if '/en/ekskursiya/' in path and '/booking/?tour=' not in html and price:
        is_en = True
        booking_block = f'''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center" data-anim="up">
  <div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">from {price} GEL <span style="font-size:14px;font-weight:400;color:#6B7280">per person</span></div>
  <div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">10-15% discount for groups of 5+</div>
  <a href="/booking/?tour={slug}" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#1A3D2E;color:#fff;padding:16px 40px;border-radius:9999px;font-size:16px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(26,61,46,.35)">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
    Book online</a>
  <div style="margin-top:10px;font-size:12px;color:#6B7280">&#9733; 4.9/5 · 87 reviews · reply in 15 min</div>
</div>
'''
        # Insert before author-byline or first section
        marker = html.find('<div class="author-byline"')
        if marker == -1:
            marker = html.find('<section class="section"')
        if marker > -1:
            html = html[:marker] + booking_block + html[marker:]

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

print(f"Updated: {stats['updated']}/{stats['total']}")

# Verify
remaining_blue = 0
for path in all_pages:
    with open(path, "r") as f:
        if '#1A56DB' in f.read():
            remaining_blue += 1
print(f"Remaining #1A56DB: {remaining_blue}")
