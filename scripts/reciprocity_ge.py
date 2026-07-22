#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ф5: реципрокность hreflang + GE-кнопка на RU/EN двойниках переведённых /ge/.
Для каждого переведённого GE-пилота (груз. <title>):
  - извлекает RU/EN/KA URL из hreflang-квадры GE-страницы;
  - в RU- и EN-файле: добавляет <link hreflang="ka"> рядом с hreflang="en"
    и GE-кнопку в переключатель (desktop+drawer). Идемпотентно.
Правило спеки: GE-кнопку добавляем ТОЛЬКО при наличии GE-двойника (здесь — есть).
"""
import re, glob, os, sys

DOMAIN = "https://sakhva-travel.com"

def url2path(u):
    p = u.replace(DOMAIN, "").strip("/")
    return "index.html" if p == "" else p + "/index.html"

def hreflang_href(h, lang):
    m = re.search(r'<link[^>]*hreflang="'+lang+r'"[^>]*>', h)
    if not m: return None, None
    tag = m.group(0)
    hm = re.search(r'href="([^"]+)"', tag)
    return (hm.group(1) if hm else None), tag

def add_hreflang_ka(h, ka_url):
    if 'hreflang="ka"' in h:
        return h, False
    en_href, en_tag = hreflang_href(h, "en")
    if not en_tag:
        return h, False
    ka_tag = f'<link href="{ka_url}" hreflang="ka" rel="alternate"/>'
    return h.replace(en_tag, en_tag + ka_tag, 1), True

def add_ge_button(h, ge_path):
    # уже есть GE-кнопка?
    if re.search(r'(?:lang-btn|d-lang-btn)[^>]*>GE</', h):
        return h, 0
    # найти каждый EN-элемент переключателя (desktop lang-btn + drawer d-lang-btn)
    pat = re.compile(r'<(a|span|button) class="([^"]*lang-btn[^"]*)"([^>]*)>EN</\1>')
    cnt = [0]
    def repl(m):
        tag, cls, attrs = m.group(1), m.group(2), m.group(3)
        el = m.group(0)
        is_drawer = 'd-lang-btn' in cls
        base_cls = 'd-lang-btn' if is_drawer else 'lang-btn'
        close = ';closeDrawer()' if is_drawer else ''
        cnt[0] += 1
        if 'setLang' in el:
            # in-page toggle страница → GE как навигация на отдельную /ge/ страницу
            ge = (f'<button class="{base_cls}" '
                  f'onclick="location.href=\'{ge_path}\'{close}">GE</button>')
            return el + ge
        # link-вариант: cookie ka + сепаратор перед GE
        st = 'text-decoration:none'
        sm = re.search(r'style="([^"]*)"', attrs)
        if sm and 'font-size' in sm.group(1):
            st = 'text-decoration:none;font-size:15px;padding:10px 12px'
        sep_st = ' style="font-size:15px"' if 'font-size' in st else ''
        ge = (f'<span class="lang-sep"{sep_st}>|</span>'
              f'<a class="{base_cls}" href="{ge_path}" '
              f'onclick="document.cookie=\'lang_pref=ka;path=/;max-age=31536000;SameSite=Lax\';'
              f'localStorage.setItem(\'lang\',\'ka\'){close}" style="{st}">GE</a>')
        return el + ge
    h2 = pat.sub(repl, h)
    return h2, cnt[0]

def process(twin_path, ka_url, ge_path):
    if not os.path.exists(twin_path):
        return f"  ✗ нет {twin_path}"
    h = open(twin_path, encoding="utf-8").read()
    h, hl = add_hreflang_ka(h, ka_url)
    h, nb = add_ge_button(h, ge_path)
    open(twin_path, "w", encoding="utf-8").write(h)
    return f"  {twin_path}: hreflang_ka={'+' if hl else '·(уже)'} GE-кнопок={nb}"

def run():
    ge_files = []
    for f in glob.glob("ge/**/*.html", recursive=True):
        h = open(f, encoding="utf-8").read()
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        if m and re.search(r'[Ⴀ-ჿ]', m.group(1)):
            ge_files.append(f)
    print(f"переведённых GE-пилотов: {len(ge_files)}")
    for gf in sorted(ge_files):
        h = open(gf, encoding="utf-8").read()
        ru_url, _ = hreflang_href(h, "ru")
        en_url, _ = hreflang_href(h, "en")
        ka_url, _ = hreflang_href(h, "ka")
        if not (ru_url and en_url and ka_url):
            print(f"[{gf}] ✗ неполная hreflang-квадра — пропуск"); continue
        ge_path = ka_url.replace(DOMAIN, "")
        print(f"\n{gf}  (GE={ge_path})")
        print(process(url2path(ru_url), ka_url, ge_path))
        print(process(url2path(en_url), ka_url, ge_path))

if __name__ == "__main__":
    run()
