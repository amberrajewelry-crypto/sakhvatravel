#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Кластерная перелинковка гео-страниц "Туры в Грузию из <города>".

В отличие от link_geo.py (all-to-all, ~750 ссылок = риск ссылочной сетки),
каждая страница ссылается только на 8 ЛОГИЧЕСКИХ соседей:
регион-кластер (Кавказ/Юг/Урал-Сибирь/Поволжье/Центр/зарубеж) + добор хабами.
Анкоры ротируются (2 формата) для снижения шаблонности.
"""
import re, glob, hashlib
from pathlib import Path

ROOT = Path("/Users/vladimir/sakhva-travel")
files = sorted(glob.glob(str(ROOT / "tury-v-gruziyu-iz-*/index.html")))

# родительный падеж для анкоров
LABELS = {
    "chelyabinska": "Челябинска", "ekaterinburga": "Екатеринбурга",
    "erevana": "Еревана", "kazahstana": "Казахстана", "kazani": "Казани",
    "kislovodska": "Кисловодска", "krasnodara": "Краснодара",
    "mahachkaly": "Махачкалы", "mineralnyh-vod": "Минеральных Вод",
    "minska": "Минска", "moskvy": "Москвы", "nalchika": "Нальчика",
    "nizhnego-novgoroda": "Нижнего Новгорода", "novosibirska": "Новосибирска",
    "permi": "Перми", "pyatigorska": "Пятигорска", "rostova": "Ростова",
    "samary": "Самары", "saratova": "Саратова", "sochi": "Сочи",
    "spb": "СПб", "stavropolya": "Ставрополя", "tashkenta": "Ташкента",
    "tyumeni": "Тюмени", "ufy": "Уфы", "vladikavkaza": "Владикавказа",
    "volgograda": "Волгограда", "voronezha": "Воронежа",
}

REGIONS = {
    "kavkaz": ["kislovodska", "mineralnyh-vod", "pyatigorska", "stavropolya",
               "nalchika", "mahachkaly", "vladikavkaza"],
    "yug": ["krasnodara", "sochi", "rostova", "volgograda", "voronezha"],
    "ural_sib": ["ekaterinburga", "chelyabinska", "permi", "tyumeni", "novosibirska"],
    "povolzhye": ["kazani", "samary", "saratova", "nizhnego-novgoroda", "ufy"],
    "centr": ["moskvy", "spb"],
    "zarubezh": ["erevana", "kazahstana", "minska", "tashkenta"],
}
CITY_REGION = {c: r for r, cs in REGIONS.items() for c in cs}
N = 8

# Ненаправленный сбалансированный граф степени ~N: ссылки взаимные,
# входящие ≈ исходящие → ни один хаб не собирает переспам-долю.
def build_graph():
    cities = sorted(LABELS)
    adj = {c: set() for c in cities}
    # 1) внутри региона — все со всеми (кластер)
    for cs in REGIONS.values():
        for a in cs:
            for b in cs:
                if a != b:
                    adj[a].add(b)
    # 2) добор до N: жадно соединяем города с наименьшей текущей степенью (мосты между регионами)
    def deg(c): return len(adj[c])
    changed = True
    while changed:
        changed = False
        for a in sorted(cities, key=deg):
            if deg(a) >= N:
                continue
            # кандидаты: не сам, не сосед, ещё не заполнен, из другого региона (приоритет разнообразия)
            cand = [b for b in cities if b != a and b not in adj[a] and deg(b) < N]
            if not cand:
                continue
            cand.sort(key=lambda b: (deg(b), CITY_REGION[b] == CITY_REGION[a]))
            b = cand[0]
            adj[a].add(b); adj[b].add(a)
            changed = True
    return adj

_GRAPH = build_graph()

def neighbors(slug):
    # стабильный порядок с ротацией по hash — наборы чипов не выглядят одинаково
    nb = sorted(_GRAPH[slug], key=lambda x: LABELS[x])
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    if nb:
        k = h % len(nb)
        nb = nb[k:] + nb[:k]
    return nb

# два формата анкора — ротация детерминированная (city_slug, target_slug)
def anchor(target, i):
    lab = LABELS[target]
    return f"из {lab}" if i % 2 == 0 else f"туры из {lab}"

CHIP = ('<a href="/tury-v-gruziyu-iz-{slug}/" style="padding:8px 18px;border:1px solid '
        '#E5E7EB;border-radius:9999px;font-size:13px;font-weight:600;color:#1A3D2E;'
        'display:inline-block;margin:4px">{lab}</a>')
START = ('Туры в Грузию из других городов:</p><div style="display:flex;flex-wrap:wrap;'
         'justify-content:center;gap:6px">')

def rebuild(html, self_slug):
    i = html.find(START)
    if i < 0:
        return html, False, 0
    cs = i + len(START)
    end = html.find('</div></div>', cs)
    if end < 0:
        return html, False, 0
    nbrs = neighbors(self_slug)
    chips = "".join(CHIP.format(slug=s, lab=anchor(s, j)) for j, s in enumerate(nbrs))
    return html[:cs] + chips + html[end:], True, len(nbrs)

changed = 0
inbound = {c: 0 for c in LABELS}
for f in files:
    slug = re.search(r'tury-v-gruziyu-iz-([a-z-]+)/index\.html', f).group(1)
    if slug not in LABELS:
        print("WARN: неизвестный город", slug); continue
    html = Path(f).read_text(encoding="utf-8")
    new, ok, n = rebuild(html, slug)
    if ok:
        for t in neighbors(slug):
            inbound[t] += 1
        if new != html:
            Path(f).write_text(new, encoding="utf-8")
            changed += 1

print(f"Обновлено: {changed}/{len(files)} | ссылок с каждой: {N}")
orphans = [c for c, v in inbound.items() if v == 0]
print(f"Входящих min={min(inbound.values())} max={max(inbound.values())} | орфанов(0 входящих): {len(orphans)} {orphans}")
