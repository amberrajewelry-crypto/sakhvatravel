#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Site-wide fix: bare-key TM corruption leaked Georgian into CSS class/style/id.
Repairs class="...", style="..." and the JS-bound id="tour-route-map" across /ge/.
Leaves visible text and section-anchor ids untouched (those are consistent with #anchors).
"""
import re, glob, sys

# Georgian tokens that leaked into technical zones -> correct English/CSS token.
# Order: longer first (tours before tour) for safety.
CLASS_MAP = [('ტურები', 'tours'), ('ტური', 'tour'), ('ფასი', 'price'),
             ('ბლოგი', 'blog'), ('სეზონი', 'season'), ('დიახ', 'yes'),
             ('მარჯვნივ', 'right'), ('მარცხნივ', 'left')]
STYLE_MAP = [('მარჯვნივ', 'right'), ('მარცხნივ', 'left')]  # CSS prop & value: left/right

def _fix_class(m):
    v = m.group(2)
    for a, b in CLASS_MAP:
        v = v.replace(a, b)
    return m.group(1) + v + m.group(3)

def _fix_style(m):
    v = m.group(2)
    for a, b in STYLE_MAP:
        v = v.replace(a, b)
    for a, b in CLASS_MAP:      # safety net; style should never hold these otherwise
        v = v.replace(a, b)
    return m.group(1) + v + m.group(3)

# Inside <style> blocks: CSS selectors (.ფასი-table), props/values (left/right),
# and the 'Georgia' font name mistranslated to the country საქართველო.
STYLEBLOCK_MAP = CLASS_MAP + [
    ('საქართველო', 'Georgia'),          # font-family name
    ('უნიcode', 'unicode'),             # @font-face unicode-range (uni->უნი)
    ('პირველი-child', 'first-child'),   # :first-child pseudo-selector
    ('რატომ-choose', 'why-choose'),     # CSS comment label
    ('თიმურის რჩევა', "Timur's tip"),   # CSS comment label
]

def _fix_styleblock(m):
    css = m.group(2)
    for a, b in STYLEBLOCK_MAP:
        css = css.replace(a, b)
    return m.group(1) + css + m.group(3)

def main():
    total = changed = 0
    for f in sorted(glob.glob('ge/**/*.html', recursive=True)):
        s = open(f, encoding='utf-8').read()
        o = s
        s = re.sub(r'(class=")([^"]*)(")', _fix_class, s)
        s = re.sub(r'(style=")([^"]*)(")', _fix_style, s)
        s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', _fix_styleblock, s, flags=re.S)
        s = s.replace('id="ტური-route-map"', 'id="tour-route-map"')
        s = s.replace('Content-ტიპი', 'Content-Type')  # broken fetch header in newsletter onsubmit
        if s != o:
            open(f, 'w', encoding='utf-8').write(s)
            changed += 1
        total += 1
    print(f"обработано {total} GE-файлов, изменено {changed}")

if __name__ == '__main__':
    main()
