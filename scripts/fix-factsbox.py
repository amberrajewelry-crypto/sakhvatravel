#!/usr/bin/env python3
"""Fix: properly remove facts-box remnants and orphaned booking blocks.
The first script's regex didn't match nested divs correctly."""

import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = "ekskursiya-kazbegi-iz-tbilisi"

with open(os.path.join(ROOT, "data/catalog.json")) as f:
    catalog = {e["slug"]: e for e in json.load(f)["excursions"]}

def find_matching_close(html, start_idx):
    """Find the closing </div> that matches the <div at start_idx, counting nesting."""
    depth = 0
    i = start_idx
    while i < len(html):
        open_m = html.find('<div', i)
        close_m = html.find('</div>', i)
        if close_m == -1:
            return -1
        if open_m != -1 and open_m < close_m:
            depth += 1
            i = open_m + 4
        else:
            depth -= 1
            if depth == 0:
                return close_m + 6  # len('</div>')
            i = close_m + 6
    return -1

pages = sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
fixed = 0

for path in pages:
    slug = path.split("/ekskursiya/")[1].split("/")[0]
    if slug == SKIP:
        continue

    with open(path, "r") as f:
        html = f.read()
    original = html

    # Check if facts-box still exists (wasn't properly removed)
    fb_idx = html.find('<div class="facts-box">')
    if fb_idx == -1:
        continue  # already clean

    # Find the full facts-box block (with proper nesting)
    fb_end = find_matching_close(html, fb_idx)
    if fb_end == -1:
        print(f"  SKIP {slug}: couldn't find matching close for facts-box")
        continue

    # Check if there's already a booking block before facts-box
    booking_exists = 'Забронировать онлайн' in html[:fb_idx]

    if booking_exists:
        # Just remove the orphaned facts-box
        html = html[:fb_idx] + html[fb_end:]
    else:
        # Replace facts-box with booking block
        info = catalog.get(slug, {})
        price = info.get("price", "")
        dur = info.get("durationText", "")
        if not price:
            print(f"  SKIP {slug}: no price in catalog")
            continue

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
        html = html[:fb_idx] + booking_block + html[fb_end:]

    # Also check for duplicate booking blocks (from first script inserting before facts-box)
    first_booking = html.find('Забронировать онлайн')
    if first_booking > -1:
        second_booking = html.find('Забронировать онлайн', first_booking + 20)
        if second_booking > -1:
            # Find and remove the first (orphaned) booking block
            # It's inside article-wrap before the proper one
            block_start = html.rfind('<div style="background:#F0FDF4', 0, first_booking)
            block_end_marker = html.find('ответ за 15 мин</div>', first_booking)
            if block_start > -1 and block_end_marker > -1:
                block_end = html.find('</div>', block_end_marker + 20) + 6
                html = html[:block_start] + html[block_end:]

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        fixed += 1
        print(f"  FIX {slug}")

print(f"\nFixed: {fixed} pages")
