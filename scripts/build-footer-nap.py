#!/usr/bin/env python3
"""Company contacts block (NAP: name, address, phone + licence, hours, legal links) in every footer.

Yandex weighs commercial factors per page: phone, address, hours, legal pages, rating.
Tour and blog footers had none of it, so the block goes before the last </footer> of every page
(home pages excluded: they carry all of it in their own markup). Pages without the #business
entity also get it as JSON-LD. Business data is read from the home page JSON-LD, so the rating
and contacts stay in one place. Idempotent: re-running replaces the block between the markers.
Run:  python3 scripts/build-footer-nap.py [site root]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "_archive", ".worktrees", ".vercel", "graphify-out", "docs",
             "demo", "dashboard", "design-previews", "scripts", "partner", "partners"}
HOMES = {"index.html", "en/index.html", "ge/index.html"}
BLOCK = re.compile(r"\n?<!-- nap:start -->.*?<!-- nap:end -->\n?", re.S)
LICENCE = "8247109128"
TG = "https://t.me/SakhvaGuideBot"

TEXT = {
    "ru": {
        "who": "гид Тимур Сахвадзе, лицензия гида №",
        "addr": "ул. Мераба Костава 14, Тбилиси 0108, Грузия", "hours": "Пн–Вс 8:00–22:00 (UTC+4)",
        "rating": "{r} ★ в Google, {n} отзывов",
        "links": [("/contacts/", "Контакты"), ("/privacy/", "Политика конфиденциальности"),
                  ("/terms/", "Условия бронирования"), ("/policy/", "Отмена и возврат")],
    },
    "en": {
        "who": "guide Timur Sakhvadze, guide licence No. ",
        "addr": "14 Merab Kostava St, Tbilisi 0108, Georgia", "hours": "Mon–Sun 8:00–22:00 (UTC+4)",
        "rating": "{r} ★ on Google, {n} reviews",
        # no English privacy page exists; the Russian one is the only version
        "links": [("/en/contacts/", "Contacts"), ("/en/terms/", "Booking terms"),
                  ("/en/policy/", "Cancellation & refunds")],
    },
    "ge": {
        "who": "გიდი თიმურ სახვაძე, გიდის ლიცენზია №",
        "addr": "მერაბ კოსტავას ქ. 14, თბილისი 0108, საქართველო", "hours": "ორშ-კვი 8:00-22:00 (UTC+4)",
        "rating": "{r} ★ Google-ში, {n} შეფასება",
        "links": [("/ge/contacts/", "კონტაქტები"), ("/ge/privacy/", "კონფიდენციალურობის პოლიტიკა"),
                  ("/ge/terms/", "დაჯავშნის პირობები"), ("/ge/policy/", "გაუქმება და დაბრუნება")],
    },
}


def business() -> dict:
    """The #business node from the home page JSON-LD (single source of contacts and rating)."""
    s = (ROOT / "index.html").read_text()
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        d = json.loads(raw)
        for node in d.get("@graph", [d]):
            if str(node.get("@id", "")).endswith("#business"):
                return node
    raise SystemExit("home page has no #business JSON-LD")


def block(lang: str, biz: dict, with_ld: bool) -> str:
    t = TEXT[lang]
    ar = biz["aggregateRating"]
    rating = t["rating"].format(r=str(ar["ratingValue"]).replace(".", ","), n=ar["reviewCount"])
    tel = biz["telephone"]
    tel_h = f"{tel[:4]} {tel[4:7]} {tel[7:9]} {tel[9:11]} {tel[11:]}"  # +995 511 27 26 23
    sep = " · "
    lines = [
        f'Sakhva Travel — {t["who"]}{LICENCE}{sep}<a href="{ar["url"]}" rel="noopener">{rating}</a>',
        f'{t["addr"]}{sep}{t["hours"]}',
        sep.join([f'<a href="tel:{tel}">{tel_h}</a>',
                  f'<a href="https://wa.me/{tel[1:]}" rel="noopener">WhatsApp</a>',
                  f'<a href="{TG}" rel="noopener">Telegram</a>',
                  f'<a href="mailto:{biz["email"]}">{biz["email"]}</a>']),
        sep.join(f'<a href="{h}">{n}</a>' for h, n in t["links"]),
    ]
    # every footer variant is dark (#111827 / #1a3d2e / #1a1a2e) but not all set a text colour
    html = ('<style>.nap{margin-top:16px;font-size:13px;line-height:1.7;color:rgba(255,255,255,.75)}'
            '.nap a{color:inherit;text-decoration:underline}</style><div class="nap">'
            + "".join(f'<p style="margin:0">{x}</p>' for x in lines) + "</div>")
    if with_ld:
        ld = {"@context": "https://schema.org", **{k: v for k, v in biz.items() if k != "@context"}}
        html += ('<script type="application/ld+json">'
                 + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>")
    return f"\n<!-- nap:start -->{html}<!-- nap:end -->"


def main() -> None:
    biz = business()
    changed = 0
    for p in sorted(ROOT.rglob("index.html")):
        rel = p.relative_to(ROOT)
        if SKIP_DIRS & set(rel.parts[:-1]) or str(rel) in HOMES:
            continue
        s = p.read_text()
        base = BLOCK.sub("", s)
        cut = base.rfind("</footer>")
        if cut < 0:
            continue
        lang = rel.parts[0] if rel.parts[0] in ("en", "ge") else "ru"
        new = base[:cut] + block(lang, biz, "#business" not in base) + "\n" + base[cut:]
        if new != s:
            p.write_text(new)
            changed += 1
    print(f"nap footer: {changed} pages updated")


if __name__ == "__main__":
    main()
