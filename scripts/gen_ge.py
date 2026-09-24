#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_ge.py — трансформер EN→GE каркаса (Ф3).

Берёт EN-страницу, создаёт /ge/-зеркало со ВСЕЙ структуркой под грузинский,
НЕ трогая текст (перевод — отдельная фаза Ф4).

Хирургический принцип: меняем только СОБСТВЕННЫЙ URL страницы (canonical,
og:url, schema @id/url self-ссылки), защищая тег hreflang="en" и навигацию
на другие /en/ страницы (иначе 404 в пилоте).

Usage: python3 scripts/gen_ge.py en/ekskursiya/<slug>/index.html
"""
import sys, re, os
from pathlib import Path

ROOT = Path("/Users/vladimir/sakhva-travel")
DOMAIN = "https://sakhva-travel.com"

FONT_INJECT = (
    '<link rel="preload" href="/fonts/noto-sans-georgian.woff2" as="font" '
    'type="font/woff2" crossorigin>'
    '<link rel="stylesheet" href="/css/ge.css">'
)

def die(msg):
    print(f"[gen_ge] СТОП: {msg}", file=sys.stderr)
    sys.exit(1)

def transform(en_rel):
    en_path = ROOT / en_rel
    if not en_path.exists():
        die(f"нет файла {en_rel}")
    # путь страницы без префикса en/ и без index.html: /ekskursiya/<slug>/
    assert en_rel.startswith("en/"), "ожидался путь вида en/..."
    inner = en_rel[len("en/"):]                      # ekskursiya/<slug>/index.html
    page_path = "/" + inner[:-len("index.html")]     # /ekskursiya/<slug>/
    self_en_url = f"{DOMAIN}/en{page_path}"          # .../en/ekskursiya/<slug>/
    self_ge_url = f"{DOMAIN}/ge{page_path}"
    self_ru_url = f"{DOMAIN}{page_path}"

    html = en_path.read_text(encoding="utf-8")
    orig = html
    log = []

    # 1. <html lang="en"> -> ka
    html, n = re.subn(r'<html([^>]*?)\blang="en"', r'<html\1lang="ka"', html, count=1)
    if n != 1: die("не найден <html lang=\"en\">")
    log.append("html lang=ka")

    # 2. Защитить тег hreflang="en" (не должен стать /ge/)
    #    формат: <link href="SELF_EN_URL" hreflang="en" rel="alternate"/>
    m = re.search(r'<link[^>]*href="'+re.escape(self_en_url)+r'"[^>]*hreflang="en"[^>]*>', html)
    if not m:
        # запасной порядок атрибутов
        m = re.search(r'<link[^>]*hreflang="en"[^>]*href="'+re.escape(self_en_url)+r'"[^>]*>', html)
    if not m: die("не найден hreflang=en self-тег")
    hreflang_en_tag = m.group(0)
    PLACEHOLDER = "___HREFLANG_EN_PROTECTED___"
    html = html.replace(hreflang_en_tag, PLACEHOLDER, 1)

    # 3. Глобально: собственный /en/-URL -> /ge/ (canonical, og:url, schema @id/url)
    cnt = html.count(self_en_url)
    html = html.replace(self_en_url, self_ge_url)
    log.append(f"self /en/->/ge/ x{cnt}")

    # 4. Вернуть защищённый hreflang=en + добавить hreflang=ka рядом
    ka_tag = f'<link href="{self_ge_url}" hreflang="ka" rel="alternate"/>'
    html = html.replace(PLACEHOLDER, hreflang_en_tag + ka_tag, 1)
    log.append("hreflang ka добавлен")

    # 5. og:locale en_US -> ka_GE + alternates (оба порядка атрибутов)
    def og_repl(_):
        return ('<meta content="ka_GE" property="og:locale"/>'
                '<meta content="ru_RU" property="og:locale:alternate"/>'
                '<meta content="en_US" property="og:locale:alternate"/>')
    # устойчиво к порядку атрибутов и наличию слэша; og:locale" (не :alternate)
    html, n = re.subn(r'<meta[^>]*\bog:locale"[^>]*>', og_repl, html, count=1)
    if n != 1: die("не найден og:locale en_US")
    log.append("og:locale ka_GE + alternates")

    # 6. schema inLanguage en -> ka (если есть)
    html, n = re.subn(r'"inLanguage":"en"', '"inLanguage":"ka"', html)
    if n: log.append(f'inLanguage ka x{n}')

    # 7. Переключатель(и): активный <span class="lang-btn on"[style?]>EN</span> ->
    #    ссылка EN + активный GE. RU-ссылка и sep RU|EN уже в блоке (оставляем).
    #    Ловит ОБА переключателя: desktop (без style) и drawer (inline style),
    #    сохраняя inline-стиль кнопки, чтобы GE выглядел идентично EN.
    def sw_repl(m):
        btn_style = m.group(1) or ''                       # ' style="..."' или ''
        inner = ''
        if btn_style:
            inner = re.search(r'style="([^"]*)"', btn_style).group(1)
        en_style = 'text-decoration:none' + ((';' + inner) if inner else '')
        sep_style = ' style="font-size:14px"' if inner else ''
        en_link = (f'<a class="lang-btn" href="/en{page_path}" '
                   f'onclick="document.cookie=\'lang_pref=en;path=/;max-age=31536000;SameSite=Lax\'" '
                   f'style="{en_style}">EN</a>')
        sep = f'<span class="lang-sep"{sep_style}>|</span>'
        ge_span = f'<span class="lang-btn on"{btn_style}>GE</span>'
        return en_link + sep + ge_span
    total_sw = 0
    html, n = re.subn(r'<span class="lang-btn on"( style="[^"]*")?>EN</span>', sw_repl, html)
    total_sw += n
    # Вариант B: переключатель на <button> (desktop lang-btn / drawer d-lang-btn)
    en_onclick = (f"document.cookie='lang_pref=en;path=/;max-age=31536000;SameSite=Lax';"
                  f"window.location.href='/en{page_path}'")
    def sw_btn_desktop(_):
        return (f'<button class="lang-btn" onclick="{en_onclick}">EN</button>'
                f'<span class="lang-sep">|</span>'
                f'<button class="lang-btn on">GE</button>')
    html, n = re.subn(r'<button class="lang-btn on">EN</button>', sw_btn_desktop, html)
    total_sw += n
    def sw_btn_drawer(_):
        return (f'<button class="d-lang-btn" onclick="{en_onclick}">EN</button>'
                f'<button class="d-lang-btn on">GE</button>')
    html, n = re.subn(r'<button class="d-lang-btn on">EN</button>', sw_btn_drawer, html)
    total_sw += n
    # Вариант C: <div class="lang-sw"><a>RU</a><a class="on">EN</a></div>
    #   Структурная замена (href игнорируем — шаг 3 их уже мог мутировать).
    #   RU -> RU-двойник (page_path), EN -> /en, добавляем активный GE.
    def sw_langsw(_):
        return (f'<a href="{page_path}">RU</a>'
                f'<a href="/en{page_path}">EN</a>'
                f'<a href="/ge{page_path}" class="on">GE</a>')
    # container-agnostic: пара анкоров RU + активный EN (любая обёртка/пробелы)
    html, n = re.subn(r'<a href="[^"]*">RU</a>\s*<a href="[^"]*" class="on">EN</a>',
                      sw_langsw, html)
    total_sw += n
    if total_sw == 0:
        # Вариант D: голая nav-ссылка "RU" (без виджета; EN — текущая страница).
        # RU-href сохраняем как в исходнике (RU-слаг может отличаться), дописываем EN+GE.
        def sw_navru(m):
            ru_href, attrs = m.group(1), m.group(2)
            return (f'<a href="{ru_href}"{attrs}>RU</a>'
                    f'<a href="/en{page_path}"{attrs}>EN</a>'
                    f'<a href="/ge{page_path}"{attrs}>GE</a>')
        html, n = re.subn(r'<a href="([^"]*)"([^>]*)>RU</a>', sw_navru, html)
        total_sw += n
    if total_sw == 0: die("не найден активный переключатель EN")
    log.append(f"переключатель RU|EN|GE x{total_sw}")

    # 8. Инъекция шрифта + ge.css перед </head>
    if "noto-sans-georgian" not in html:
        html, n = re.subn(r'</head>', FONT_INJECT + '</head>', html, count=1)
        if n != 1: die("не найден </head>")
        log.append("шрифт+ge.css")

    if html == orig: die("ничего не изменилось")

    # запись в ge/<inner>
    ge_path = ROOT / ("ge/" + inner)
    ge_path.parent.mkdir(parents=True, exist_ok=True)
    ge_path.write_text(html, encoding="utf-8")
    print(f"[gen_ge] OK {en_rel} -> ge/{inner}")
    print("         " + " · ".join(log))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        die("usage: gen_ge.py en/<path>/index.html")
    transform(sys.argv[1])
