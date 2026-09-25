#!/usr/bin/env python3
"""Блог: строка «Тур по теме» (p.also-tour) получает частную цену и метку источника в WhatsApp.

- после названия тура: «частный выезд от ₾X за 1–2» (если тур есть в data/private_prices.json);
- в текст WhatsApp добавляется [site:<lang>:blog:<статья>], чтобы бот/CRM видели, откуда лид.
Идемпотентно: обработанный <p> помечается data-sk="also-v1".
"""
import json, re, glob, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
priv = {t["slug"]: t["private"]["1-2"] for t in json.loads((ROOT / "data/private_prices.json").read_text())["tours"] if t.get("confirmed")}
LBL = {"ru": "частный выезд от ₾{p} за 1–2", "en": "private from ₾{p} for 1–2", "ka": "კერძო ₾{p}-დან 1–2 ადამიანზე"}

changed = tagged = priced = 0
for pat, lang in (("blog/*/index.html", "ru"), ("en/blog/*/index.html", "en"), ("ge/blog/*/index.html", "ka")):
    for f in glob.glob(str(ROOT / pat)):
        s = Path(f).read_text()
        m = re.search(r'<p class="also-tour"([^>]*)>(.*?)</p>', s, re.S)
        if not m or 'data-sk="also-v1"' in m.group(1):
            continue
        art = Path(f).parent.name
        body = m.group(2)
        tour = re.search(r'href="[^"]*/ekskursiya/([^/"]+)/"', body)
        if tour and tour.group(1) in priv:
            body, n = re.subn(r"(</strong></a>)", r"\1 <span style=\"color:#B45309;font-weight:600\">· " + LBL[lang].format(p=priv[tour.group(1)]) + "</span>", body, count=1)
            priced += n
        def tag(w):
            url = w.group(1)
            base, _, q = url.partition("?text=")
            txt = urllib.parse.unquote(q) + f"\n[site:{lang}:blog:{art}]"
            return f'href="{base}?text={urllib.parse.quote(txt)}"'
        body, n = re.subn(r'href="(https://wa\.me/\d+\?text=[^"]*)"', tag, body, count=1)
        tagged += n
        new = f'<p class="also-tour" data-sk="also-v1"{m.group(1)}>{body}</p>'
        s = s[:m.start()] + new + s[m.end():]
        Path(f).write_text(s)
        changed += 1
print(f"статей: {changed}, с меткой WA: {tagged}, с частной ценой: {priced}")
