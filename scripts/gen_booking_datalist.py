#!/usr/bin/env python3
"""Регенерация <datalist id="tour-list"> на страницах бронирования из каталога.

Тянет ВСЕ туры (78) из data/catalog{,-en,-ge}.json по языку → booking.html,
en/booking/index.html, ge/booking/index.html. data-id = slug (совпадает во всех
языках, booking-ссылка = ?tour={slug}), value = локализованный title + цена.
Запускать после изменения каталога. Рантайм-JS booking не трогается.
"""
import json
import pathlib
import re
import html

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (каталог, файл booking, шаблон value) — {t}=title, {p}=price
LANGS = [
    ("data/catalog.json",    "booking.html",           "{t} — от ₾{p}"),
    ("data/catalog-en.json", "en/booking/index.html",  "{t} — from ₾{p}"),
    ("data/catalog-ge.json", "ge/booking/index.html",  "{t} — ₾{p}-დან"),
]

BLOCK_RE = re.compile(r'(<datalist id="tour-list">)(.*?)(</datalist>)', re.DOTALL)


def old_price(p):
    # Единый ~20%-off штрих (воспроизводит существующие data-old точь-в-точь).
    return int(p * 1.25 / 5 + 0.5) * 5


def build_options(catalog_path, value_tpl):
    tours = json.loads((ROOT / catalog_path).read_text(encoding="utf-8"))["excursions"]
    rows = []
    for e in sorted(tours, key=lambda x: x["title"].lower()):
        price = int(e["price"])
        val = value_tpl.format(t=e["title"], p=price)
        days = int(e.get("days") or 0)
        attrs = [
            f'value="{html.escape(val, quote=True)}"',
            f'data-id="{e["slug"]}"',
            f'data-price="{price}"',
            f'data-old="{old_price(price)}"',
        ]
        if days > 1:
            attrs.append(f'data-days="{days}"')
        rows.append("          <option " + " ".join(attrs) + ">")
    return tours, "\n" + "\n".join(rows) + "\n        "


def main():
    for cat, booking, tpl in LANGS:
        fp = ROOT / booking
        html_txt = fp.read_text(encoding="utf-8")
        tours, inner = build_options(cat, tpl)
        m = BLOCK_RE.search(html_txt)
        if not m:
            raise SystemExit(f"[{booking}] не найден <datalist id=\"tour-list\">")
        new = html_txt[:m.start()] + m.group(1) + inner + m.group(3) + html_txt[m.end():]
        fp.write_text(new, encoding="utf-8")
        print(f"  {booking}: {len(tours)} туров")


if __name__ == "__main__":
    main()
