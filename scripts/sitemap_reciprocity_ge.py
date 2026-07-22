#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ф5 (sitemap): реципрокность hreflang в sitemap для переведённых /ge/.
Для каждого GE-пилота берёт квадру URL из его HTML-hreflang (источник истины),
затем в sitemap-файлах:
  - в записи RU и EN добавляет 4 <xhtml:link> (ru/en/ka/x-default=ru);
  - создаёт новую <url> для /ge/ с той же квадрой;
  - добавляет xmlns:xhtml в <urlset>, если его нет.
Идемпотентно. x-default = RU (соответствие HTML, грабля sync)."""
import re, glob, os

DOMAIN = "https://sakhva-travel.com"
LASTMOD = "2026-07-22"
SITEMAPS = ["sitemap-blog.xml", "sitemap-tours.xml",
            "sitemap-landing.xml", "sitemap-pages.xml"]

def alts(ru, en, ka):
    return ("".join([
        f'\n    <xhtml:link rel="alternate" hreflang="ru" href="{ru}"/>',
        f'\n    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>',
        f'\n    <xhtml:link rel="alternate" hreflang="ka" href="{ka}"/>',
        f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{ru}"/>',
    ]))

def ensure_ns(txt):
    if "xmlns:xhtml" in txt:
        return txt
    return txt.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml"', 1)

def find_url_block(txt, loc_url):
    i = txt.find(f"<loc>{loc_url}</loc>")
    if i < 0:
        return None
    s = txt.rfind("<url>", 0, i)
    e = txt.find("</url>", i) + len("</url>")
    return (s, e, txt[s:e])

def inject_alts(block, ru, en, ka):
    if 'hreflang="ka"' in block:
        return block, False
    # вставить альтернативы после </loc>
    return re.sub(r'(</loc>)', r'\1' + alts(ru, en, ka), block, count=1), True

def get_quad(ge_html):
    def hl(l):
        m = re.search(r'<link[^>]*hreflang="'+l+r'"[^>]*>', ge_html)
        if not m: return None
        return re.search(r'href="([^"]+)"', m.group(0)).group(1)
    return hl("ru"), hl("en"), hl("ka")

def run():
    # загрузить sitemap-ы в память
    S = {f: open(f, encoding="utf-8").read() for f in SITEMAPS if os.path.exists(f)}
    pilots = []
    for f in glob.glob("ge/**/*.html", recursive=True):
        h = open(f, encoding="utf-8").read()
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        if m and re.search(r'[Ⴀ-ჿ]', m.group(1)):
            pilots.append(get_quad(h))
    print(f"пилотов: {len(pilots)}")
    for ru, en, ka in sorted(pilots):
        print(f"\n{ka}")
        for lang, url in (("ru", ru), ("en", en)):
            done = False
            for f in S:
                blk = find_url_block(S[f], url)
                if not blk: continue
                s, e, block = blk
                nb, ch = inject_alts(block, ru, en, ka)
                if ch:
                    S[f] = ensure_ns(S[f][:s] + nb + S[f][e:])
                    print(f"  {lang} alts -> {f}")
                else:
                    print(f"  {lang} alts уже есть ({f})")
                done = True
                break
            if not done:
                print(f"  ✗ {lang} URL не найден в sitemap: {url}")
        # новая /ge/ запись — в тот же файл, где RU
        if f"<loc>{ka}</loc>" in "".join(S.values()):
            print("  ge запись уже есть")
            continue
        placed = False
        for f in S:
            blk = find_url_block(S[f], ru)
            if not blk: continue
            s, e, _ = blk
            ge_entry = (f"\n  <url>\n    <loc>{ka}</loc>\n    <lastmod>{LASTMOD}</lastmod>"
                        f"{alts(ru, en, ka)}\n  </url>")
            S[f] = ensure_ns(S[f][:e] + ge_entry + S[f][e:])
            print(f"  ge запись создана -> {f}")
            placed = True
            break
        if not placed:
            print("  ✗ не удалось разместить ge запись (нет RU-якоря)")
    for f, txt in S.items():
        open(f, "w", encoding="utf-8").write(txt)
    print("\nзаписано:", ", ".join(S))

if __name__ == "__main__":
    run()
