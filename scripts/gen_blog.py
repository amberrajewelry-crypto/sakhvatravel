#!/usr/bin/env python3
"""Генератор блог-статей Sakhva по эталону gruziya-perviy-raz.
Берёт эталонный HTML, заменяет head-meta / schema / контентный блок,
сохраняя всю обвязку (nav, footer, CSS, lead-magnet, scripts) идентичной.
"""
import re, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TPL_RU = ROOT / "blog/gruziya-perviy-raz/index.html"
TPL_EN = ROOT / "en/blog/georgia-first-time-tips/index.html"


def build(template_path, out_path, d, lang):
    """d: dict с ключами meta+content. lang: 'ru'|'en'."""
    t = template_path.read_text(encoding="utf-8")
    base = "https://sakhva-travel.com"
    ru_url = f"{base}/blog/{d['ru_slug']}/"
    en_url = f"{base}/en/blog/{d['en_slug']}/"
    self_url = ru_url if lang == "ru" else en_url
    other_url = en_url if lang == "ru" else ru_url

    # --- HEAD META (regex по атрибутам, не по значениям) ---
    t = re.sub(r"<title>.*?</title>", f"<title>{d['title']}</title>", t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" name="description")', rf'\g<1>{d["desc"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" name="keywords")', rf'\g<1>{d["keywords"]}\g<2>', t, count=1)
    # twitter
    t = re.sub(r'(<meta content=")[^"]*(" name="twitter:title")', rf'\g<1>{d["title"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" name="twitter:description")', rf'\g<1>{d["desc"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" name="twitter:image")', rf'\g<1>{base}/images/blog/{d["hero"]}.webp\g<2>', t, count=1)
    # canonical + hreflang + sitemap alt
    t = re.sub(r'(<link href=")[^"]*(" rel="canonical")', rf'\g<1>{self_url}\g<2>', t, count=1)
    t = re.sub(r'(<link href=")[^"]*(" hreflang="ru" rel="alternate")', rf'\g<1>{ru_url}\g<2>', t, count=1)
    t = re.sub(r'(<link href=")[^"]*(" hreflang="en" rel="alternate")', rf'\g<1>{en_url}\g<2>', t, count=1)
    t = re.sub(r'(<link href=")[^"]*(" hreflang="x-default" rel="alternate")', rf'\g<1>{ru_url}\g<2>', t, count=1)
    # og
    t = re.sub(r'(<meta content=")[^"]*(" property="og:title")', rf'\g<1>{d["title"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:description")', rf'\g<1>{d["desc"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:url")', rf'\g<1>{self_url}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:image")', rf'\g<1>{base}/images/blog/{d["hero"]}.jpg\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:image:alt")', rf'\g<1>{d["title"]}\g<2>', t, count=1)
    # preload hero image
    t = re.sub(r'(<link as="image" fetchpriority="high" href=")[^"]*(")', rf'\g<1>/images/blog/{d["hero"]}.webp\g<2>', t, count=1)
    # dates
    t = re.sub(r'(<meta content=")[^"]*(" property="article:published_time")', rf'\g<1>{d["pub"]}\g<2>', t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time")', rf'\g<1>{d["mod"]}\g<2>', t, count=1)

    # --- SCHEMA (первый ld+json) ---
    t = re.sub(r'<script type="application/ld\+json">.*?</script>',
               f'<script type="application/ld+json">{d["schema"]}</script>', t, count=1, flags=re.S)

    # --- CONTENT BLOCK (полная замена региона по маркерам) ---
    # RU:  <div id="content-ru"> ... </div>  →  <section id="lead-magnet"
    # EN:  <header class="article-hero"> ... </section>  →  <section id="lead-magnet"
    start = '<div id="content-ru">' if lang == "ru" else '<header class="article-hero">'
    pat = re.escape(start) + r'.*?(?=\n<section id="lead-magnet")'
    if not re.search(pat, t, flags=re.S):
        raise RuntimeError(f"content region not found for {lang} in {template_path}")
    t = re.sub(pat, lambda m: d["body"], t, count=1, flags=re.S)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(t, encoding="utf-8")
    # validate schema
    json.loads(d["schema"])
    return len(t)


if __name__ == "__main__":
    import importlib.util
    data_file = ROOT / "scripts/blog_content.py"
    spec = importlib.util.spec_from_file_location("blog_content", data_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for art in mod.ARTICLES:
        if only and art["ru_slug"] != only:
            continue
        for lg in ("ru", "en"):
            art[lg]["ru_slug"] = art["ru_slug"]
            art[lg]["en_slug"] = art["en_slug"]
        n_ru = build(TPL_RU, ROOT / f"blog/{art['ru_slug']}/index.html", art["ru"], "ru")
        n_en = build(TPL_EN, ROOT / f"en/blog/{art['en_slug']}/index.html", art["en"], "en")
        print(f"  {art['ru_slug']}: RU {n_ru}b · EN {art['en_slug']} {n_en}b")
