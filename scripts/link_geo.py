#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перестраивает footer-блок перелинковки "Туры в Грузию из других городов"
во ВСЕХ гео-страницах: каждая ссылается на все прочие города (26 всего)."""
import re, glob
from pathlib import Path

ROOT = Path("/Users/vladimir/sakhva-travel")
files = sorted(glob.glob(str(ROOT / "tury-v-gruziyu-iz-*/index.html")))

# 1) собрать slug -> label из существующих чипов (объединение по всем файлам)
labels = {}
chip_re = re.compile(r'href="/tury-v-gruziyu-iz-([a-z-]+)/"[^>]*>([^<]+)</a>')
for f in files:
    for slug, lab in chip_re.findall(Path(f).read_text(encoding="utf-8")):
        labels.setdefault(slug, lab.strip())

# 2) новые города
labels.update({
    "ufy": "из Уфы",
    "nizhnego-novgoroda": "из Нижнего Новгорода",
    "mineralnyh-vod": "из Минеральных Вод",
    "volgograda": "из Волгограда",
    "saratova": "из Саратова",
    "mahachkaly": "из Махачкалы",
    "tyumeni": "из Тюмени",
    "stavropolya": "из Ставрополя",
})
print(f"Всего городов в сетке: {len(labels)}")

CHIP = ('<a href="/tury-v-gruziyu-iz-{slug}/" style="padding:8px 18px;border:1px solid '
        '#E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#1A3D2E;'
        'display:inline-block;margin:4px">{lab}</a>')

START = 'Туры в Грузию из других городов:</p><div style="display:flex;flex-wrap:wrap;justify-content:center;gap:6px">'

def rebuild(html, self_slug):
    i = html.find(START)
    if i < 0:
        return html, False
    chips_start = i + len(START)
    # закрытие: первый '</div></div>' после начала чипов
    end = html.find('</div></div>', chips_start)
    others = sorted([s for s in labels if s != self_slug], key=lambda s: labels[s].lower())
    chips = "".join(CHIP.format(slug=s, lab=labels[s]) for s in others)
    return html[:chips_start] + chips + html[end:], True

changed = 0
for f in files:
    slug = re.search(r'tury-v-gruziyu-iz-([a-z-]+)/index\.html', f).group(1)
    html = Path(f).read_text(encoding="utf-8")
    new, ok = rebuild(html, slug)
    if ok and new != html:
        Path(f).write_text(new, encoding="utf-8")
        changed += 1
print(f"Обновлено файлов: {changed}/{len(files)}")
