#!/usr/bin/env python3
"""Генератор блог-статей Sakhva из scripts/blog-template.html.
Данные темы — JSON (3 языка сразу). Slug: ru=/blog/SLUG_RU/, en=/en/blog/SLUG_EN/, ge=/ge/blog/SLUG_EN/.
Usage: python3 scripts/gen-blog.py scripts/blog-data/<theme>.json
"""
import json, sys, re, html as _html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = (ROOT / "scripts/blog-template.html").read_text(encoding="utf-8")
BASE = "https://sakhva-travel.com"

UI = {
 "ru": dict(contents="Содержание", label="Гайд", read="мин чтения", book="Забронировать экскурсию",
   related="Похожие туры от Sakhva Travel", questions="Вопросы", home="Главная", blog="Блог",
   author="Тимур · Sakhva Travel", creds="Индивидуальная экскурсия с 2023 · 500+ туров · 4.9/5 рейтинг",
   tour_lbl="Тур", more="Подробнее →", alt_txt="Read in English",
   ta_title="Рейтинг 4.9 из 5 на TripAdvisor", ta_sub="90+ отзывов от туристов, которые уже побывали на экскурсиях с Тимуром",
   ta_btn="Читать отзывы", need="Нужен индивидуальный тур по Грузии?"),
 "en": dict(contents="Contents", label="Guide", read="min read", book="Book a tour",
   related="Related tours by Sakhva Travel", questions="FAQ", home="Home", blog="Blog",
   author="Timur · Sakhva Travel", creds="Private tours since 2023 · 500+ tours · 4.9/5 rating",
   tour_lbl="Tour", more="Learn more →", alt_txt="Читать по-русски",
   ta_title="Rated 4.9 / 5 on TripAdvisor", ta_sub="90+ reviews from travellers who toured with Timur",
   ta_btn="Read reviews", need="Need a private tour of Georgia?"),
 "ka": dict(contents="სარჩევი", label="გზამკვლევი", read="წთ კითხვა", book="ტურის დაჯავშნა",
   related="მსგავსი ტურები Sakhva Travel-ისგან", questions="კითხვები", home="მთავარი", blog="ბლოგი",
   author="თიმური · Sakhva Travel", creds="კერძო ტურები 2023 წლიდან · 500+ ტური · 4.9/5 რეიტინგი",
   tour_lbl="ტური", more="დაწვრილებით →", alt_txt="Read in English",
   ta_title="რეიტინგი 4.9 / 5 TripAdvisor-ზე", ta_sub="90+ მიმოხილვა მოგზაურებისგან, ვინც თიმურთან იმოგზაურა",
   ta_btn="მიმოხილვების ნახვა", need="გჭირდებათ საქართველოს კერძო ტური?"),
}
LOCALE = {"ru": "ru_RU", "en": "en_US", "ka": "ka_GE"}

def esc(s): return _html.escape(s, quote=True)

_ATTR_Q = re.compile(r"\b(class|style|href|rel|target|id|src|alt|width|height|loading|fetchpriority|colspan|scope)='([^']*)'")
def nq(html):
    """Нормализует одинарные кавычки атрибутов в двойные (консистентность с сайтом).
    Значения этих атрибутов не содержат апострофов; апострофы в тексте между тегами не затрагиваются."""
    return _ATTR_Q.sub(r'\1="\2"', html)

def urls(d):
    return {"ru": f"{BASE}/blog/{d['slug_ru']}/",
            "en": f"{BASE}/en/blog/{d['slug_en']}/",
            "ka": f"{BASE}/ge/blog/{d['slug_en']}/"}

def hreflang(u):
    return (f'<link href="{u["en"]}" hreflang="en" rel="alternate"/>'
            f'<link href="{u["ru"]}" hreflang="ru" rel="alternate"/>'
            f'<link href="{u["ka"]}" hreflang="ka" rel="alternate"/>'
            f'<link href="{u["ru"]}" hreflang="x-default" rel="alternate"/>')

def langsw(u, lang):
    def cell(code, url, on):
        if on: return f'<span class="lang-btn on">{code}</span>'
        oc = "" if code!="GE" else " onclick=\"document.cookie='lang_pref=ka;path=/;max-age=31536000;SameSite=Lax';localStorage.setItem('lang','ka')\""
        return f'<a class="lang-btn" href="{url}"{oc} style="text-decoration:none">{code}</a>'
    ru = cell("RU", u["ru"], lang=="ru")
    en = cell("EN", u["en"], lang=="en")
    ge = cell("GE", u["ka"], lang=="ka")
    return f'<div class="lang-sw">{ru}<span class="lang-sep">|</span>{en}<span class="lang-sep">|</span>{ge}</div>'

def breadcrumb(loc, t, lang):
    blog_url = "/blog/" if lang=="ru" else f"/{ 'en' if lang=='en' else 'ge'}/blog/"
    home_url = "/" if lang=="ru" else f"/{ 'en' if lang=='en' else 'ge'}/"
    return (f'<div class="breadcrumb">\n<a href="{home_url}">{loc["home"]}</a><span>/</span>\n'
            f'<a href="{blog_url}">{loc["blog"]}</a><span>/</span>\n<span>{esc(t["crumb"])}</span>\n</div>')

def hero_text(loc, t):
    metas = "".join(f"<span>{esc(m)}</span>\n" for m in t["meta"])
    return (f'<div class="article-label">{loc["label"]} · {t["read"]} {loc["read"]}</div>\n'
            f'<h1 class="article-h1">{esc(t["h1"])}</h1>\n'
            f'<div class="article-meta">\n<span>{esc(t["date"])}</span>\n<span>{loc["author"]}</span>\n{metas}</div>')

def toc_block(loc, t):
    fig = (f'<figure style="margin:24px 0;border-radius:12px;overflow:hidden">\n'
           f'<img alt="{esc(t["hero_alt"])}" fetchpriority="high" height="630" loading="eager" '
           f'src="{t["hero_webp"]}" style="width:100%;display:block" width="1200"/>\n</figure>')
    items = "".join(f'<li><a href="#{i["id"]}">{esc(i["t"])}</a></li>\n' for i in t["toc"])
    return (f'<nav class="article-toc">\n{fig}\n<h2>{loc["contents"]}</h2>\n<ol>\n{items}</ol>\n</nav>')

def jsonld(d, t, u, lang):
    faq = [{"@type":"Question","name":q["q"],
            "acceptedAnswer":{"@type":"Answer","text":q["a"]}} for q in t["faq"]]
    crumbs = {"ru":("Главная","Блог"),"en":("Home","Blog"),"ka":("მთავარი","ბლოგი")}[lang]
    blog_url = u[lang].rsplit("/",2)[0]+"/"
    home_url = BASE+"/" if lang=="ru" else f"{BASE}/{'en' if lang=='en' else 'ge'}/"
    graph = [
     {"@type":"BlogPosting","@id":u[lang]+"#article","inLanguage":lang,"wordCount":t.get("wc",1600),
      "articleSection":t["section"],"headline":t["title"],"description":t["desc"],
      "author":{"@type":"Person","@id":BASE+"/#guide-timur","name":UI[lang]["author"].split(" · ")[0],
        "jobTitle":"Guide","url":BASE+"/about/",
        "image":{"@type":"ImageObject","url":BASE+"/images/timur.webp","width":72,"height":72},
        "hasCredential":{"@type":"EducationalOccupationalCredential","credentialCategory":"Tour guide licence",
          "identifier":"8247109128","recognizedBy":{"@type":"GovernmentOrganization","name":"Georgian National Tourism Administration"}}},
      "publisher":{"@type":"Organization","name":"Sakhva Travel","url":BASE+"/",
        "logo":{"@type":"ImageObject","url":BASE+"/images/logo-schema.webp","width":300,"height":60}},
      "datePublished":d["pub"],"dateModified":d["mod"],
      "image":{"@type":"ImageObject","url":t["og_image"],"width":1200,"height":630},
      "url":u[lang],"mainEntityOfPage":{"@type":"WebPage","@id":u[lang]}},
     {"@type":"BreadcrumbList","itemListElement":[
       {"@type":"ListItem","position":1,"name":crumbs[0],"item":home_url},
       {"@type":"ListItem","position":2,"name":crumbs[1],"item":blog_url},
       {"@type":"ListItem","position":3,"name":t["crumb"],"item":u[lang]}]},
     {"@type":"FAQPage","mainEntity":faq},
    ]
    doc = {"@context":"https://schema.org","@graph":graph}
    return '<script type="application/ld+json">'+json.dumps(doc,ensure_ascii=False,separators=(",",":"))+'</script>'

def article_body(t):
    return f'<div class="article-body">\n{nq(t["body"])}\n</div>\n</div>'

def after_body(loc, t, u, lang):
    # блок «читайте также»
    also = nq(t.get("also_html",""))
    # related tours grid
    cards = ""
    for c in t["related"]:
        cards += (f'<div class="rc-card">\n<div class="rc-card-label">{loc["tour_lbl"]}</div>\n'
                  f'<h3>{esc(c["t"])}</h3>\n<p>{esc(c["d"])}</p>\n'
                  f'<a href="{c["href"]}">{loc["more"]}</a>\n</div>\n')
    related = (f'<section class="related">\n<h2>{loc["related"]}</h2>\n<div class="related-grid">\n{cards}</div>\n</section>')
    # tripadvisor
    ta = (f'<div style="max-width:800px;margin:32px auto;padding:20px 24px;background:#f0fdf4;border-radius:12px;'
          f'border:1px solid #bbf7d0;display:flex;align-items:center;gap:16px;flex-wrap:wrap">\n'
          f'<div style="flex:1;min-width:200px">\n<p style="margin:0 0 4px;font-size:16px;font-weight:700;color:#111827">{loc["ta_title"]}</p>\n'
          f'<p style="margin:0;font-size:13px;color:#6B7280">{loc["ta_sub"]}</p>\n</div>\n'
          f'<a href="https://www.tripadvisor.com/Attraction_Review-g294195-d15318013-Reviews-Sakhva_Travel-Tbilisi.html" '
          f'rel="noopener" style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#007A52;color:#fff;'
          f'font-size:13px;font-weight:700;border-radius:9999px;text-decoration:none;white-space:nowrap" target="_blank">{loc["ta_btn"]}</a>\n</div>')
    # faq visible
    faq_items = ""
    for q in t["faq"]:
        faq_items += (f'<div class="fi">\n<button class="fq" onclick="toggleFaq(this)">{esc(q["q"])}<span class="fq-ic">+</span></button>\n'
                      f'<div class="fa"><div class="fa-inner">{esc(q["a"])}</div></div>\n</div>\n')
    faq = f'<section id="faq">\n<div class="faq-inner">\n<h2>{esc(t.get("faq_h", loc["questions"]))}</h2>\n{faq_items}</div>\n</section>'
    return f'{also}\n{related}\n{ta}\n{faq}'

def alt_link(loc, u, lang):
    target = u["en"] if lang!="en" else u["ru"]
    return f'<a href="{target}" style="font-size:14px;color:#1A3D2E;font-weight:600;text-decoration:none">{loc["alt_txt"]}</a>'

def build(d, lang):
    t = d[lang]; loc = UI[lang]; u = urls(d)
    out = TPL
    repl = {
     "LANG": lang, "TITLE": esc(t["title"]), "DESC": esc(t["desc"]),
     "PUB": d["pub"], "MOD": d["mod"], "OG_IMAGE": t["og_image"], "LOCALE": LOCALE[lang],
     "CANONICAL": u[lang], "HREFLANG": hreflang(u), "HERO_WEBP": t["hero_webp"],
     "JSONLD": jsonld(d, t, u, lang), "LANGSW": langsw(u, lang),
     "BREADCRUMB": breadcrumb(loc, t, lang), "HERO_TEXT": hero_text(loc, t),
     "TOC_BLOCK": toc_block(loc, t), "ARTICLE_BODY": article_body(t),
     "AFTER_BODY": after_body(loc, t, u, lang), "ALT_LINK": alt_link(loc, u, lang),
    }
    for k, v in repl.items():
        out = out.replace("{{"+k+"}}", v)
    if lang == "ka":
        ge_head = ('<link rel="preload" href="/fonts/noto-sans-georgian.woff2" as="font" type="font/woff2" crossorigin>\n'
                   '<link rel="stylesheet" href="/css/ge.css">\n')
        out = out.replace("</head>", ge_head + "</head>", 1)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    assert not left, f"незаполненные слоты: {set(left)}"
    return out

def path_for(d, lang):
    if lang=="ru": return ROOT / "blog" / d["slug_ru"] / "index.html"
    sub = "en" if lang=="en" else "ge"
    return ROOT / sub / "blog" / d["slug_en"] / "index.html"

def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    apply = "--apply" in sys.argv
    for lang in ("ru","en","ka"):
        html = build(data, lang)
        p = path_for(data, lang)
        if apply:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(html, encoding="utf-8")
        print(f"[{lang}] {p.relative_to(ROOT)}  {'ЗАПИСАН' if apply else 'dry'}  {len(html)}b  wc≈{data[lang].get('wc','?')}")

if __name__ == "__main__":
    main()
