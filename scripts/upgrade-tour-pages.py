#!/usr/bin/env python3
"""Upgrade all 58 tour pages to match Kazbegi standard.
Steps: fonts, colors, hero CTA, facts-box→booking, incl/excl icons, data-anim."""

import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = "ekskursiya-kazbegi-iz-tbilisi"  # reference, already done

# Load catalog for prices
with open(os.path.join(ROOT, "data/catalog.json")) as f:
    catalog = {e["slug"]: e for e in json.load(f)["excursions"]}

pages = sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
stats = {"total": 0, "updated": 0, "errors": []}

for path in pages:
    slug = path.split("/ekskursiya/")[1].split("/")[0]
    if slug == SKIP:
        continue

    stats["total"] += 1
    try:
        with open(path, "r") as f:
            html = f.read()
        original = html

        # === STEP 1: Fonts — preload+onload → blocking ===
        # Pattern: <link rel="preload" href="..." as="style" onload="...">
        html = re.sub(
            r'<link\s+rel="preload"\s+href="(/fonts/[^"]+)"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
            r'<link rel="stylesheet" href="\1">',
            html
        )
        # Remove <noscript> wrappers for fonts
        html = re.sub(
            r'<noscript><link rel="stylesheet" href="/fonts/[^"]+"></noscript>',
            '',
            html
        )
        # Multiple noscript on same line
        html = re.sub(
            r'\s*<noscript><link rel="stylesheet" href="/fonts/[^"]*"><link rel="stylesheet" href="/fonts/[^"]*"></noscript>',
            '',
            html
        )
        # Remove Google Fonts preload+onload for Lora (use local)
        html = re.sub(
            r'<link\s+rel="preload"\s+as="style"\s+href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
            '',
            html
        )
        html = re.sub(
            r'<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Lora[^"]*"></noscript>',
            '',
            html
        )
        # Remove Google Fonts preload for Raleway (deferred pattern)
        html = re.sub(
            r'<link\s+rel="preload"\s+href="https://fonts\.googleapis\.com/css2\?family=Raleway[^"]*"\s+as="style"\s+onload="this\.onload=null;this\.rel=\'stylesheet\'"[^>]*>',
            '',
            html
        )
        # Remove duplicate preconnect to fonts.googleapis if we already have local
        # (keep one preconnect pair just in case)

        # === STEP 2: Colors ===
        html = html.replace("#1A56DB", "#1A3D2E")
        html = html.replace("#1E429F", "#1A3D2E")
        # Salmon CTA in hero button and sticky bar
        html = html.replace("background:#D4845A", "background:#1A3D2E")
        html = html.replace("rgba(212,132,90,.35)", "rgba(26,61,46,.35)")

        # === STEP 3: Hero CTA ===
        info = catalog.get(slug, {})
        price = info.get("price", "")

        # Replace hero CTA button
        old_cta = re.search(
            r'(<div class="hero-btns"[^>]*>)\s*<a[^>]*onclick="event\.preventDefault\(\);openContact\(\)"[^>]*>Получить скидку 10%</a>\s*(</div>)',
            html, re.DOTALL
        )
        if old_cta:
            price_text = f"Забронировать от {price} лари" if price else "Забронировать онлайн"
            wa_text = f"Хочу+забронировать+{slug.replace('-', '+')}"
            new_cta = f'''{old_cta.group(1)}
      <a href="https://wa.me/995511272623?text={wa_text}" class="btn-wa" style="padding:14px 28px;font-size:16px;border-radius:9999px;text-decoration:none;box-shadow:0 4px 14px rgba(37,211,102,.35)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        {price_text}</a>
      <a href="#" class="btn-primary" style="padding:14px 28px;font-size:14px;border-radius:9999px;background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.5);color:#fff;text-decoration:none;backdrop-filter:blur(8px)" onclick="event.preventDefault();openContact()">Скидка 10% — оставить заявку</a>
    {old_cta.group(2)}
    <div style="margin-top:12px;font-size:13px;color:rgba(255,255,255,.7)">&#9733; 4.9/5 · 87 отзывов · ответ за 15 мин</div>'''
            html = html[:old_cta.start()] + new_cta + html[old_cta.end():]

        # === STEP 4: facts-box → booking block ===
        facts_match = re.search(
            r'<div class="facts-box">.*?</div>\s*</div>',
            html, re.DOTALL
        )
        if facts_match and price:
            dur = info.get("durationText", "")
            booking_block = f'''<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:16px;padding:24px;margin:28px 0;text-align:center">
  <div style="font-size:32px;font-weight:700;color:#1A3D2E;margin-bottom:4px">от {price} лари <span style="font-size:14px;font-weight:400;color:#6B7280">с человека</span></div>
  <div style="font-size:13px;color:#B45309;font-weight:600;margin-bottom:16px">Скидка 10-15% для групп от 5 человек</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
    <div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">Длительность</div><div style="font-size:13px;font-weight:700;color:#111827">{dur}</div></div>
    <div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">Группа</div><div style="font-size:13px;font-weight:700;color:#111827">до 7 чел</div></div>
    <div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">Выезд</div><div style="font-size:13px;font-weight:700;color:#111827">08:00</div></div>
    <div style="background:#fff;border:1px solid #D1FAE5;border-radius:8px;padding:10px 8px;text-align:center"><div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:3px">Отмена</div><div style="font-size:13px;font-weight:700;color:#111827">за 24 ч</div></div>
  </div>
  <a href="/booking/?tour={slug}" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#1A3D2E;color:#fff;padding:16px 40px;border-radius:9999px;font-size:16px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(26,61,46,.35);transition:background .2s,transform .15s">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
    Забронировать онлайн</a>
  <div style="margin-top:10px;font-size:12px;color:#6B7280">&#9733; 4.9/5 · 87 отзывов · ответ за 15 мин</div>
</div>'''
            html = html[:facts_match.start()] + booking_block + html[facts_match.end():]

        # === STEP 5: Add [data-anim] to sections ===
        # Add animation CSS if not present
        if '[data-anim]' not in html:
            anim_css = '''/* Scroll animations */
[data-anim]{opacity:0;transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1)}
[data-anim].is-vis{opacity:1;transform:none}
[data-anim="up"]{transform:translateY(40px)}
[data-anim="fade"]{transform:none}
[data-anim="scale"]{transform:scale(.92)}
[data-anim-d="1"]{transition-delay:.1s}[data-anim-d="2"]{transition-delay:.2s}[data-anim-d="3"]{transition-delay:.3s}'''
            html = html.replace('</style>', anim_css + '\n</style>', 1)

        # Add data-anim="up" to key sections
        # article-wrap sections
        html = re.sub(
            r'<div class="article-wrap"(?!\s+data-anim)',
            '<div class="article-wrap" data-anim="up"',
            html
        )
        # section.section
        html = re.sub(
            r'<section class="section"(?!\s+data-anim)(?![^>]*data-anim)',
            '<section class="section" data-anim="up"',
            html
        )
        # callout boxes
        html = re.sub(
            r'<div class="callout-box([^"]*)"(?!\s+data-anim)(?![^>]*data-anim)',
            r'<div class="callout-box\1" data-anim="up"',
            html
        )
        html = re.sub(
            r'<div class="callout-why"(?!\s+data-anim)(?![^>]*data-anim)',
            '<div class="callout-why" data-anim="up"',
            html
        )

        # Add IntersectionObserver script if not present
        if 'data-anim' in html and "querySelectorAll('[data-anim]')" not in html:
            anim_script = '''<script>
!function(){var els=document.querySelectorAll('[data-anim]');if(!els.length)return;var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-vis');io.unobserve(e.target)}})},{threshold:.15,rootMargin:'0px 0px -40px 0px'});els.forEach(function(el){io.observe(el)})}();
</script>'''
            html = html.replace('</body>', anim_script + '\n</body>')

        # === STEP 6: Bottom CTA — upgrade to dark green ===
        old_bottom_cta = re.search(
            r'<section id="cta"[^>]*>.*?<button[^>]*onclick="openContact\(\)"[^>]*>Получить скидку 10%</button>',
            html, re.DOTALL
        )
        if old_bottom_cta:
            price_str = f'{price}' if price else '...'
            new_bottom = f'''<section id="cta" data-anim="up" style="background:#1A3D2E;padding:clamp(40px,5vw,64px) clamp(16px,3.5vw,56px);text-align:center;border-top:none">
  <div style="font-size:11px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:12px">Бронирование</div>
  <h2 style="font-family:'Lora',serif;font-size:clamp(26px,3.5vw,44px);font-weight:400;color:#fff;letter-spacing:-0.02em;margin-bottom:8px">Готовы к приключению?</h2>
  <p style="font-size:16px;color:rgba(255,255,255,.6);margin-bottom:6px">от <strong style="color:#F59E0B;font-size:24px">{price_str} лари</strong> с человека</p>
  <p style="font-size:13px;color:rgba(255,255,255,.5);margin-bottom:20px">&#9733; 4.9/5 · 87 отзывов · ответ за 15 минут</p>
  <div class="cta-btns">
    <button class="btn-primary" onclick="openContact()" style="cursor:pointer;border:none;font-family:inherit;background:#F59E0B;color:#111;padding:14px 32px;border-radius:9999px;font-size:14px;font-weight:700;letter-spacing:.04em;box-shadow:0 4px 14px rgba(245,158,11,.4)">Скидка 10% — оставить заявку</button>'''
            html = html[:old_bottom_cta.start()] + new_bottom + html[old_bottom_cta.end():]

        # === STEP 7: Mobile sticky bar — fix text and color ===
        html = re.sub(
            r'(<div id="mobile-sticky-bar"[^>]*>)\s*<a[^>]*onclick="event\.preventDefault\(\);openContact\(\)"[^>]*>Получить скидку 10%</a>',
            lambda m: f'''{m.group(1)}
<div style="display:flex;flex-direction:column;gap:1px;flex-shrink:0"><span style="font-size:10px;color:#6B7280;font-weight:500">Экскурсия</span><span style="font-size:18px;font-weight:700;color:#111827">от {price} лари</span></div>
<a href="https://wa.me/995511272623?text=Хочу+забронировать+{slug.replace('-', '+')}" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#25D366;color:#fff;padding:13px 24px;border-radius:9999px;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap">
<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
Забронировать</a>''' if price else m.group(0),
            html, flags=re.DOTALL
        )

        if html != original:
            with open(path, "w") as f:
                f.write(html)
            stats["updated"] += 1
            print(f"  OK  {slug}")
        else:
            print(f"  --  {slug} (no changes)")

    except Exception as e:
        stats["errors"].append(f"{slug}: {e}")
        print(f"  ERR {slug}: {e}")

print(f"\nDone: {stats['updated']}/{stats['total']} updated, {len(stats['errors'])} errors")
if stats["errors"]:
    for err in stats["errors"]:
        print(f"  ! {err}")
