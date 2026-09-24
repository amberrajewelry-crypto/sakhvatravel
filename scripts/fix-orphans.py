#!/usr/bin/env python3
"""Fix orphaned fact-item divs and extra closing tags left by facts-box removal."""

import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = "ekskursiya-kazbegi-iz-tbilisi"

pages = sorted(glob.glob(os.path.join(ROOT, "ekskursiya/*/index.html")))
fixed = 0

for path in pages:
    slug = path.split("/ekskursiya/")[1].split("/")[0]
    if slug == SKIP:
        continue

    with open(path, "r") as f:
        html = f.read()
    original = html

    body_start = html.find('<body')
    if body_start == -1:
        continue

    body = html[body_start:]

    # Check if orphaned fact-items exist in body
    if 'fact-item' not in body and 'fact-label' not in body and 'fact-value' not in body:
        # Check div balance anyway
        opens = body.count('<div')
        closes = body.count('</div>')
        if opens == closes:
            continue

    # Strategy: find the booking block, then check what comes after it
    # for orphaned fact-item divs and extra </div> tags

    # Pattern: the booking block ends with "ответ за 15 мин</div>\n</div>"
    # After that, there might be orphaned fact-items and closing divs

    # Find all fact-item remnants in body and remove them
    # They look like: <div class="fact-item"><div class="fact-label">...</div><div class="fact-value">...</div></div>
    html = re.sub(
        r'\s*<div class="fact-item"><div class="fact-label">[^<]*</div><div class="fact-value">[^<]*</div></div>',
        '',
        html
    )

    # Remove orphaned </div>\n</div> that were the facts-grid and facts-box closers
    # These appear right after fact-items were removed, as standalone closing tags
    # Pattern: after booking block close, there might be \n  </div>\n</div> orphans

    # Also remove orphaned facts-grid opening if it exists
    html = re.sub(r'\s*<div class="facts-grid">\s*', '\n', html)

    # Now recount divs
    body_start2 = html.find('<body')
    body2 = html[body_start2:]
    opens = body2.count('<div')
    closes = body2.count('</div>')
    diff = opens - closes

    if diff < 0:
        # More closes than opens — remove extra </div> from the area after booking block
        # Find the booking block end
        booking_end = html.find('ответ за 15 мин</div>')
        if booking_end > -1:
            after_booking = booking_end + len('ответ за 15 мин</div>')
            # Look in next 50 chars for extra </div>
            segment = html[after_booking:after_booking+100]
            for _ in range(abs(diff)):
                close_idx = segment.find('</div>')
                if close_idx != -1:
                    # Remove this orphaned </div>
                    abs_idx = after_booking + close_idx
                    html = html[:abs_idx] + html[abs_idx+6:]
                    # Recalculate segment
                    segment = html[after_booking:after_booking+100]

    if html != original:
        with open(path, "w") as f:
            f.write(html)
        fixed += 1

        # Verify
        body3 = html[html.find('<body'):]
        o = body3.count('<div')
        c = body3.count('</div>')
        status = "OK" if o == c else f"STILL OFF by {o-c}"
        print(f"  FIX {slug} ({status})")

print(f"\nFixed: {fixed} pages")
