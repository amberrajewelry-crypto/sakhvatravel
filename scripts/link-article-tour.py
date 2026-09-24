"""Link blog articles to their matching tour and back (SEO plan 24.09, step 12).

Article: inserts the standard `also-tour` block right after the opening
`article-wrap` element, so the offer is visible before the first paragraph.
Tour: appends a "read the guide" link after the first paragraph of the
"Why…" section. Idempotent: skips a side if the link is already there.

Usage: python3 scripts/link-article-tour.py [--dry]
"""
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
WA = "https://wa.me/995511272623?text="
STYLE = "margin:24px 0;padding:14px 18px;border-left:3px solid #1A3D2E;background:#f6f8f7"
LINK_STYLE = "color:#1A3D2E;font-weight:600"

TEXT = {
    "en": {"label": "Tour on this topic:", "book": "Book on WhatsApp →",
           "hello": "Hello! I would like to book: ", "from": "from ₾{}",
           "guide": "Planning the trip yourself? Read our guide: "},
    "ru": {"label": "Тур по теме:", "book": "Забронировать в WhatsApp →",
           "hello": "Здравствуйте! Хочу забронировать: ", "from": "от ₾{}",
           "guide": "Собираетесь сами? Подробный гайд: "},
}

# (lang, article, tour, anchor, duration, price, guide link title)
PAIRS = [
    ("en", "en/blog/martvili-canyon", "en/ekskursiya/ekskursiya-kanyony-zapadnoy-gruzii",
     "Martvili & Okatse canyons tour from Tbilisi", "12–13 h", 180, "Martvili Canyon: prices, boat ride & how to get there"),
    ("en", "en/blog/david-gareja-monastery", "en/ekskursiya/ekskursiya-david-gareji",
     "David Gareja tour from Tbilisi", "10–12 h", 225, "David Gareja Monastery: caves, hike & how to get there"),
    ("en", "en/blog/soviet-tbilisi-tour", "en/ekskursiya/sovetskiy-tur-tbilisi",
     "Soviet architecture walking tour in Tbilisi", "4–5 h", 135, "Soviet Tbilisi: mosaics, brutalism & hidden gems"),
    ("en", "en/blog/narikala-fortress-tbilisi", "en/ekskursiya/ekskursiya-narikala",
     "Narikala Fortress guided tour", "3 h", 135, "Narikala Fortress: entry, cable car & best views"),
    ("en", "en/blog/ureki-beach", "en/ekskursiya/ekskursiya-ureki-iz-tbilisi",
     "Ureki day tour from Tbilisi", "12 h", 180, "Ureki Beach: magnetic black sand, season & stays"),
    ("en", "en/blog/kazbegi-day-trip-from-tbilisi", "en/ekskursiya/ekskursiya-kazbegi-iz-tbilisi",
     "Kazbegi day tour from Tbilisi", "11–12 h", 175, "Kazbegi day trip from Tbilisi: route, cost & tips"),
    ("en", "en/blog/kakheti-one-day-trip", "en/ekskursiya/ekskursiya-kakheti-iz-tbilisi",
     "Kakheti wine tour from Tbilisi", "10–11 h", 170, "Tbilisi to Kakheti day trip: route & wineries"),
    ("ru", "blog/ureki-plyazh", "ekskursiya/ekskursiya-ureki-iz-tbilisi",
     "Экскурсия в Уреки из Тбилиси", "12 ч", 180, "Уреки: магнитный чёрный песок, сезон, жильё"),
    ("ru", "blog/kakheti-za-1-den", "ekskursiya/ekskursiya-kakheti-iz-tbilisi",
     "Экскурсия в Кахетию из Тбилиси", "10–12 ч", 170, "Кахетия за 1 день: маршрут и дегустации"),
    ("ru", "blog/gruziya-7-dney", "ekskursiya/tur-gruziya-7-dney",
     "Тур по Грузии на 7 дней с гидом", "7 дней", 595, "Грузия на 7 дней: маршрут без спешки"),
    ("ru", "blog/sernye-bani-tbilisi", "ekskursiya/ekskursiya-abanotubani",
     "Экскурсия по Абанотубани и серным баням", "3 ч", 135, "Абанотубани: история серных бань Тбилиси"),
    ("ru", "blog/kazbegi-iz-tbilisi-2026", "ekskursiya/ekskursiya-kazbegi-iz-tbilisi",
     "Экскурсия в Казбеги из Тбилиси", "11–12 ч", 175, "Казбеги: что посмотреть по дороге"),
]

WRAP_RE = re.compile(r'<(div|main) class="article-wrap">')
WHY_RE = re.compile(r"<h2[^>]*>\s*(Почему|Why)")


def tour_block(lang: str, tour: str, anchor: str, duration: str, price: int) -> str:
    t = TEXT[lang]
    name = html.escape(f"{anchor} — {duration}, {t['from'].format(price)}", quote=False)
    wa = WA + quote(t["hello"] + anchor, safe="")
    return (f'<p class="also-tour" style="{STYLE}">{t["label"]} '
            f'<a href="/{tour}/"><strong>{name}</strong></a> · '
            f'<a href="{wa}" rel="nofollow noopener" target="_blank">{t["book"]}</a></p>')


def add_to_article(lang, article, tour, anchor, duration, price) -> str:
    f = ROOT / article / "index.html"
    s = f.read_text()
    if 'class="also-tour"' in s:
        return "article: already has block"
    m = WRAP_RE.search(s)
    if not m:
        return "article: NO article-wrap"
    s = s[:m.end()] + "\n" + tour_block(lang, tour, anchor, duration, price) + s[m.end():]
    if not DRY:
        f.write_text(s)
    return "article: block added"


def add_to_tour(lang, article, tour, guide_title) -> str:
    f = ROOT / tour / "index.html"
    s = f.read_text()
    if f'href="/{article}/"' in s:
        return "tour: backlink exists"
    h = WHY_RE.search(s)
    start = h.start() if h else s.find("<h2", s.find("</h1>"))
    end = s.find("</p>", start)
    if start < 0 or end < 0:
        return "tour: NO anchor"
    link = (f' {TEXT[lang]["guide"]}<a href="/{article}/" style="{LINK_STYLE}">'
            f"{html.escape(guide_title, quote=False)}</a>.")
    s = s[:end] + link + s[end:]
    if not DRY:
        f.write_text(s)
    return "tour: backlink added"


DRY = "--dry" in sys.argv

if __name__ == "__main__":
    for lang, article, tour, anchor, duration, price, guide in PAIRS:
        a = add_to_article(lang, article, tour, anchor, duration, price)
        t = add_to_tour(lang, article, tour, guide)
        print(f"{article:40} {a:28} {t}")
