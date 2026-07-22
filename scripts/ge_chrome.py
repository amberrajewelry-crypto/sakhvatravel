#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Общий chrome-пасс GE: переводит ОДИНАКОВЫЕ на всех страницах UI-лейблы, которые
нельзя гнать через TM (короткие строки Mo/We/Close задели бы Moscow/Month/…).
Только якорная замена (aria-label="X", <div class="bcal-wday">X</div>). Толерантен:
заменяет где найдено, не падает на 0 (у блога нет календаря и т.п.). Идемпотентен.
Ставится ПЕРВЫМ шагом пайплайна любой ge-страницы (пилоты + все скелеты)."""
import sys, glob, re
from pathlib import Path

# regex-правила: унаследованные из EN дефекты, число варьируется (цена «от ₾N»
# — русское «от» в ценниках EN site-wide → груз. постфикс «-დან»)
CHROME_RE = [
    (re.compile(r'>от\s+(&#8382;|₾|\$|€|USD|EUR|GEL)\s?([\d,\.]+)<'), r'>\1\2-დან<'),
]

# aria-label и текст-ноды общего UI. НЕ включать бренды (Visa/Mir/Threads…) — латиница.
CHROME = [
    ('aria-label="Menu"', 'aria-label="მენიუ"'),
    ('aria-label="Close"', 'aria-label="დახურვა"'),
    ('aria-label="Contact"', 'aria-label="კონტაქტი"'),
    ('aria-label="Crypto"', 'aria-label="კრიპტო"'),
    ('aria-label="Pay Online"', 'aria-label="გადახდა ონლაინ"'),
    ('aria-label="Music"', 'aria-label="მუსიკა"'),
    ('aria-label="Sound"', 'aria-label="ხმა"'),
    ('aria-label="Tour details"', 'aria-label="ტურის დეტალები"'),
    ('aria-label="Online booking"', 'aria-label="ონლაინ ჯავშანი"'),
    # календарь: дни недели
    ('<div class="bcal-wday">Mo</div>', '<div class="bcal-wday">ორშ</div>'),
    ('<div class="bcal-wday">Tu</div>', '<div class="bcal-wday">სამ</div>'),
    ('<div class="bcal-wday">We</div>', '<div class="bcal-wday">ოთხ</div>'),
    ('<div class="bcal-wday">Th</div>', '<div class="bcal-wday">ხუთ</div>'),
    ('<div class="bcal-wday">Fr</div>', '<div class="bcal-wday">პარ</div>'),
    ('<div class="bcal-wday">Sa</div>', '<div class="bcal-wday">შაბ</div>'),
    ('<div class="bcal-wday">Su</div>', '<div class="bcal-wday">კვი</div>'),
]

def apply(f):
    html = Path(f).read_text(encoding="utf-8")
    n = 0
    for old, new in CHROME:
        c = html.count(old)
        if c:
            html = html.replace(old, new); n += c
    for rx, rep in CHROME_RE:
        html, c = rx.subn(rep, html); n += c
    if n:
        Path(f).write_text(html, encoding="utf-8")
    return n

if __name__ == "__main__":
    files = sys.argv[1:] or glob.glob("ge/**/*.html", recursive=True)
    tot = 0
    for f in sorted(files):
        n = apply(f)
        tot += n
        if n: print(f"  {f}: {n} chrome-замен")
    print(f"ВСЕГО chrome-замен: {tot} по {len(files)} файлам")
