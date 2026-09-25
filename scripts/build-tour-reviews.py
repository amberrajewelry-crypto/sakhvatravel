#!/usr/bin/env python3
"""Fresh real Google reviews block on every tour page (/ekskursiya/*, RU/EN/GE).

Texts are the actual Google Maps reviews of Sakhva Travel (collected 26.09.2026), quoted as
written or translated faithfully with a "translated" mark. The block is visible HTML only, no
Review schema: these are reviews of the company, not of the particular tour. Each page gets 3
reviews: ones matching the route first (Batumi/Kutaisi, multi-day, night Tbilisi), the rest
rotated by page slug so neighbouring pages differ. Reviews whose author is already on the page
(the older shared "reviews" section) are skipped. The block goes right after that section, or
before the footer when a page has none. Idempotent (<!-- trv:start/end -->).
Run:  python3 scripts/build-tour-reviews.py [site root]
Add a review: append to REVIEWS (all three languages optional; a missing language = not shown).
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
MAPS = "https://maps.app.goo.gl/WcvnBvaPgYdQRxQ78"
BLOCK = re.compile(r"\n?<!-- trv:start -->.*?<!-- trv:end -->\n?", re.S)
PER_PAGE = 3

# (author, date, text) per language; tags pick routes the review is about.
# Giorgi V., Tigran and Nugo are not here: they are already in the older shared section.
REVIEWS = [
    {"tags": ["batumi", "dnya", "dney", "mnogodnev"],
     "ru": ("Юлия З.", "август 2026", "Прекрасная надёжная компания, информацию предоставляет подробно, все сотрудники очень дружелюбные и заботливые, всегда на связи. Мы заказывали трёхдневный маршрут от Батуми до Тбилиси с 4-месячным ребёнком и с посещением достопримечательностей, помогли с решением всех вопросов и аккуратно провезли по маршруту не меньше 700 км."),
     "en": ("Yulia Z.", "August 2026", "A wonderful, reliable company: detailed information, very friendly and caring staff, always in touch. We booked a three-day route from Batumi to Tbilisi with a 4-month-old baby and sightseeing; they helped with every question and drove us carefully along a route of at least 700 km. (translated from Russian)"),
     "ge": ("იულია ზ.", "აგვისტო 2026", None)},
    {"tags": ["batumi", "kutaisi"],
     "ru": ("Glen Nicholson", "сентябрь 2026", "Искали индивидуальную поездку на день из Батуми в Кутаиси с главными храмами и природой региона. Sakhva составили идеальный график, дали отличного водителя Мамуку и быстро были на связи при бронировании и накануне тура, чтобы всё подтвердить. Оказалось, что мы были в соборе Баграти в воскресенье, когда там проходили три свадьбы, — очень красивый и запоминающийся день. (перевод с английского)"),
     "en": ("Glen Nicholson", "September 2026", "We were looking for a customized day trip from Batumi to Kutaisi that covered the key religious sites as well as the natural beauty of the area. Sakhva delivered a perfect schedule, an excellent driver, Mamuka, and they stayed in touch with us quickly during the booking process and the day before the tour to confirm details. As it turned out we were in Bagrati Cathedral on a Sunday when 3 weddings were taking place for a very beautiful and memorable day."),
     "ge": ("Glen Nicholson", "სექტემბერი 2026", None)},
    {"tags": ["nochn", "night", "vecher"],
     "ru": ("Eric Mushtukov", "август 2026", "Огромное спасибо Сабе и Тимуру за то, что наш мальчишник получился таким потрясающим! Профессиональные и дружелюбные. Всё было идеально организовано, весело и незабываемо. Лучших гидов и не пожелать. Очень рекомендую, 10/10! (перевод с английского)"),
     "en": ("Eric Mushtukov", "August 2026", "Huge thanks to Saba and Timur for making our bachelor party such an amazing experience! They were professional, friendly. Everything was perfectly organized, fun, and unforgettable. Couldn’t have asked for better guides. Highly recommended, 10/10!")},
    {"tags": ["individ", "chastn", "private"],
     "ru": ("Регина", "сентябрь 2026", "Не люблю групповые туры, поэтому очень обрадовалась, когда узнала, что у SakhvaTravel можно собрать индивидуальную поездку. Нам подобрали маршрут под наши пожелания, подсказали красивые локации и всё организовали без лишней суеты. Грузия теперь в сердце, обязательно вернёмся ещё."),
     "en": ("Regina", "September 2026", "I don’t like group tours, so I was very glad to find out that SakhvaTravel can put together an individual trip. They picked a route to our wishes, suggested beautiful spots and organised everything without any fuss. Georgia is in our hearts now, we will definitely come back. (translated from Russian)")},
    {"tags": [],
     "ru": ("Ralph Grunewald", "сентябрь 2026", "Саба, наш гид и водитель, был замечательным. Приехал вовремя, много знает и подарил нам незабываемый день. (перевод с английского)"),
     "en": ("Ralph Grunewald", "September 2026", "Saba, our guide and driver, was wonderful. He was on time, knowledgeable, and provided a memorable day for us.")},
    {"tags": [],
     "ru": ("Ангелина", "сентябрь 2026", "Хочу отдельно отметить организацию. До поездки всё подробно объяснили, на вопросы отвечали быстро, во время путешествия тоже были на связи. Для меня это очень важно, потому что не люблю отдых, где приходится самой решать сто организационных вопросов. С SakhvaTravel всё прошло спокойно."),
     "en": ("Angelina", "September 2026", "I want to single out the organisation. Everything was explained in detail before the trip, questions were answered quickly, and they stayed in touch during the journey too. That matters a lot to me, because I don’t like holidays where I have to sort out a hundred organisational issues myself. With SakhvaTravel everything went smoothly. (translated from Russian)")},
    {"tags": [],
     "ru": ("Gideon Truter", "июль 2026", "Пять звёзд с плюсом! Исключительный уровень сервиса, понятная связь и огромное желание сделать больше, чем нужно, — всё это сложилось в прекрасный опыт работы с агентством Sakhva. (перевод с английского)"),
     "en": ("Gideon Truter", "July 2026", "Five stars +! Exceptional service level, clear communication and extreme willingness to go the extra mile all added up to the marvelous experience dealing with Sakhva agency.")},
    {"tags": [],
     "ru": ("Арам Геворкян", "сентябрь 2026", "Отдыхом доволен. Буду рекомендовать вас! Лучшие в Грузии!"),
     "en": ("Aram Gevorkyan", "September 2026", "Happy with the trip. I will recommend you! The best in Georgia! (translated from Russian)"),
     "ge": ("არამ გევორქიანი", "სექტემბერი 2026", None)},
]

UI = {
    "ru": ("Новые отзывы о Sakhva Travel в Google", "Все отзывы в Google Картах"),
    "en": ("New Sakhva Travel reviews on Google", "All reviews on Google Maps"),
    "ge": ("Sakhva Travel-ის ახალი შეფასებები Google-ში", "ყველა შეფასება Google Maps-ზე"),
}
CSS = ('<style>.trv{max-width:1100px;margin:0 auto;padding:40px 20px}.trv h2{font-size:26px;margin:0 0 18px}'
       '.trv-g{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}'
       '.trv-c{background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:22px;color:#1f2937}'
       '.trv-s{color:#F59E0B;letter-spacing:2px}.trv-c p{margin:10px 0;font-size:15px;line-height:1.6}'
       '.trv-a{font-size:13px;color:#6b7280}.trv-l{display:inline-block;margin-top:16px;font-weight:600;color:#1A3D2E}</style>')


def ge_texts() -> dict:
    """Georgian texts are the ones already published on /ge/about/ (faithful translations)."""
    s = (ROOT / "ge/about/index.html").read_text()
    out = {}
    for t, a in re.findall(r'class="rev-text">(.*?)</p>\s*<div class="rev-author">(.*?)</div>', s, re.S):
        out[re.sub(r"<[^>]+>", "", a).split("—")[0].strip()] = re.sub(r"<[^>]+>", "", t).strip().strip("«»")
    return out


def pick(slug: str, lang: str, ge: dict, page: str) -> list:
    pool = []
    for r in REVIEWS:
        if lang not in r:
            continue
        a, d, t = r[lang]
        t = t or ge.get(a)
        if t and a not in page:
            pool.append((any(k in slug for k in r["tags"]), a, d, t))
    first = [x for x in pool if x[0]]
    rest = [x for x in pool if not x[0]]
    shift = int(hashlib.md5(slug.encode()).hexdigest(), 16) % max(len(rest), 1)
    return (first + rest[shift:] + rest[:shift])[:PER_PAGE]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def block(lang: str, items: list) -> str:
    title, more = UI[lang]
    cards = "".join(f'<div class="trv-c"><div class="trv-s">★★★★★</div><p>{esc(t)}</p>'
                    f'<div class="trv-a">{esc(a)} — Google, {d}</div></div>' for _, a, d, t in items)
    return (f'\n<!-- trv:start -->{CSS}<section class="trv"><h2>{title}</h2><div class="trv-g">{cards}</div>'
            f'<a class="trv-l" href="{MAPS}" rel="noopener" target="_blank">{more} →</a></section><!-- trv:end -->\n')


def main() -> None:
    ge = ge_texts()
    changed = 0
    for p in sorted(ROOT.glob("*ekskursiya/*/index.html")) + sorted(ROOT.glob("*/ekskursiya/*/index.html")):
        rel = p.relative_to(ROOT).parts
        lang = rel[0] if rel[0] in ("en", "ge") else "ru"
        s = p.read_text()
        base = BLOCK.sub("", s)
        sec = base.find('id="reviews"')
        cut = base.find("</section>", sec) + len("</section>") if sec >= 0 else base.find("<footer")
        items = pick(rel[-2], lang, ge, base)
        if cut < 0 or not items or re.search(r"<meta[^>]*noindex", base):
            continue
        new = base[:cut] + block(lang, items) + base[cut:]
        if new != s:
            p.write_text(new)
            changed += 1
    print(f"tour reviews: {changed} pages updated")


if __name__ == "__main__":
    main()
