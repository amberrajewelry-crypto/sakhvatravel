#!/usr/bin/env python3
"""Upgrade all blog pages: colors, fonts, CTA, animations.
NO regex on nested HTML. Only safe string/regex replacements."""

import os, re, glob

ROOT = os.path.expanduser("~/sakhva-travel")

# Collect all blog pages
ru_blog = sorted(glob.glob(os.path.join(ROOT, "blog/*/index.html")))
en_blog = sorted(glob.glob(os.path.join(ROOT, "en/blog/*/index.html")))
all_pages = ru_blog + en_blog

stats = {"total": 0, "updated": 0, "font_fixed": 0, "color_fixed": 0, "cta_fixed": 0, "anim_fixed": 0}

for path in all_pages:
    stats["total"] += 1
    with open(path, "r") as f:
        html = f.read()
    original = html

    # === 1. FONTS: preload+onload → blocking ===
    html = re.sub(
        r'<link\s+rel="preload"\s+href="(/fonts/[^"]+)"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        r'<link rel="stylesheet" href="\1">',
        html
    )
    # Noscript wrappers
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="/fonts/raleway\.css"><link rel="stylesheet" href="/fonts/lora\.css"></noscript>', '', html)
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="/fonts/[^"]*"></noscript>', '', html)
    # Google Fonts deferred Lora
    html = re.sub(
        r'<link\s+rel="preload"\s+as="style"\s+href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        '', html
    )
    html = re.sub(r'\s*<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"></noscript>', '', html)
    # Google Fonts deferred Raleway
    html = re.sub(
        r'<link\s+rel="preload"\s+href="https://fonts\.googleapis\.com/css2\?family=Raleway[^"]*"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
        '', html
    )

    if 'onload="this.onload=null' not in html and 'onload="this.onload=null' in original:
        stats["font_fixed"] += 1

    # === 2. COLORS: all old → new ===
    color_changed = False
    for old, new in [
        ("#1A56DB", "#1A3D2E"),
        ("#1E429F", "#1A3D2E"),
        ("#1F2937", "#1A3D2E"),
        ("#D4845A", "#1A3D2E"),
        ("rgba(212,132,90,.35)", "rgba(26,61,46,.35)"),
        # EFF6FF (light blue bg) → F0FDF4 (light green bg) for callout boxes
        ("background:#EFF6FF", "background:#F0FDF4"),
        ("border-left:4px solid #1A3D2E;", "border-left:4px solid #1A3D2E;"),  # already green after replace
    ]:
        if old in html:
            html = html.replace(old, new)
            color_changed = True
    if color_changed:
        stats["color_fixed"] += 1

    # === 3. CTA: "Получить скидку 10%" → "Забронировать" / "Get 10% Discount" → "Book a tour" ===
    cta_changed = False

    # RU: Salmon CTA button → green with new text
    html = re.sub(
        r'<a[^>]*onclick="event\.preventDefault\(\);openContact\(\)"[^>]*>Получить скидку 10%</a>',
        '<a href="/booking/" style="display:inline-block;padding:12px 28px;font-size:14px;font-weight:600;letter-spacing:0.5px;border-radius:9999px;background:#1A3D2E;color:#fff;text-decoration:none;transition:opacity .2s">Забронировать экскурсию</a>',
        html
    )
    # EN variant
    html = re.sub(
        r'<a[^>]*onclick="event\.preventDefault\(\);openContact\(\)"[^>]*>Get 10% Discount</a>',
        '<a href="/booking/" style="display:inline-block;padding:12px 28px;font-size:14px;font-weight:600;letter-spacing:0.5px;border-radius:9999px;background:#1A3D2E;color:#fff;text-decoration:none;transition:opacity .2s">Book a tour</a>',
        html
    )

    # Button variants (in article-cta section)
    html = re.sub(
        r'(<button[^>]*onclick="openContact\(\)"[^>]*>)Получить скидку 10%(</button>)',
        r'\1Забронировать экскурсию\2',
        html
    )
    html = re.sub(
        r'(<button[^>]*onclick="openContact\(\)"[^>]*>)Get 10% Discount(</button>)',
        r'\1Book a tour\2',
        html
    )

    # Remaining text
    html = html.replace('>Получить скидку 10%<', '>Забронировать экскурсию<')
    html = html.replace('>Get 10% Discount<', '>Book a tour<')

    # Modal title
    html = html.replace(
        'color:#111;margin-bottom:4px">Получить скидку 10%</div>',
        'color:#111;margin-bottom:4px">Забронировать экскурсию</div>'
    )
    html = html.replace(
        'color:#111;margin-bottom:4px">Get 10% Discount</div>',
        'color:#111;margin-bottom:4px">Book a Tour</div>'
    )

    if 'Получить скидку 10%' not in html and 'Get 10% Discount' not in html:
        if 'Получить скидку 10%' in original or 'Get 10% Discount' in original:
            stats["cta_fixed"] += 1

    # === 4. SCROLL ANIMATIONS ===
    if '[data-anim]' not in html:
        anim_css = '''/* Scroll animations */
[data-anim]{opacity:0;transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1)}
[data-anim].is-vis{opacity:1;transform:none}
[data-anim="up"]{transform:translateY(40px)}
[data-anim="fade"]{transform:none}
[data-anim-d="1"]{transition-delay:.1s}[data-anim-d="2"]{transition-delay:.2s}[data-anim-d="3"]{transition-delay:.3s}'''
        # Insert before last </style>
        last_style = html.rfind('</style>')
        if last_style > -1:
            html = html[:last_style] + anim_css + '\n' + html[last_style:]

    # Add data-anim to key elements (safe — only adds attribute, no structural changes)
    html = re.sub(r'<div class="article-wrap"(?!\s+data-anim)', '<div class="article-wrap" data-anim="up"', html)
    html = re.sub(r'<div class="article-cta"(?!\s+data-anim)', '<div class="article-cta" data-anim="up"', html)

    # Add IO script if needed
    if 'data-anim' in html and "querySelectorAll('[data-anim]')" not in html:
        anim_script = '''<script>!function(){var els=document.querySelectorAll('[data-anim]');if(!els.length)return;var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-vis');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -40px 0px'});els.forEach(function(el){io.observe(el)})}();</script>'''
        html = html.replace('</body>', anim_script + '\n</body>')
        stats["anim_fixed"] += 1

    # === WRITE ===
    if html != original:
        with open(path, "w") as f:
            f.write(html)
        stats["updated"] += 1

print(f"Updated: {stats['updated']}/{stats['total']}")
print(f"  Fonts fixed: {stats['font_fixed']}")
print(f"  Colors fixed: {stats['color_fixed']}")
print(f"  CTA fixed: {stats['cta_fixed']}")
print(f"  Animations added: {stats['anim_fixed']}")

# === VERIFY ===
print("\n=== VERIFICATION ===")
issues = 0
for path in all_pages:
    with open(path, "r") as f:
        h = f.read()
    slug = path.replace(ROOT + "/", "").replace("/index.html", "")
    problems = []
    if '#1A56DB' in h: problems.append("#1A56DB")
    if '#1E429F' in h: problems.append("#1E429F")
    if '#D4845A' in h: problems.append("#D4845A")
    if 'onload="this.onload=null' in h: problems.append("deferred-font")
    if 'Получить скидку 10%' in h: problems.append("old-CTA-RU")
    if 'Get 10% Discount' in h: problems.append("old-CTA-EN")
    if problems:
        print(f"  FAIL {slug}: {', '.join(problems)}")
        issues += 1

print(f"\nTotal issues: {issues}/{stats['total']}")
