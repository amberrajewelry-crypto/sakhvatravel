#!/usr/bin/env python3
"""Коммерческое ядро русских страниц sakhva-travel.com по иерархии (сверху вниз).
Источник — уже собранные данные (meta keywords + n-граммы) + прямой подсчёт
вхождений по контенту. Только коммерческие запросы. Частота = вхождений по сайту.
"""
from __future__ import annotations
import re
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path("/Users/vladimir/sakhva-travel")
XLSX = ROOT / "scripts" / "semcore_ru.xlsx"


def is_ru_page(p: Path) -> bool:
    s = str(p)
    if "/en/" in s or "/node_modules/" in s:
        return False
    bad = ["_bak", "backup", "preview", "demo", "proto", "hero3d",
           "dashboard", "/partner/", "miralinks"]
    if any(b in s for b in bad):
        return False
    name = p.name
    if name == "404.html":
        return False
    if re.match(r"google[0-9a-f]+\.html", name) or name.startswith("yandex_") \
       or re.match(r"sakhvatravel.*\.html", name):
        return False
    return True


CHROME = re.compile(
    r"(nav|menu|footer|header|cookie|fab|modal|breadcrumb|sticky|"
    r"drawer|burger|topbar|hidden|sr-only|skip)", re.I)


def page_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "nav", "header", "footer"]):
        t.decompose()
    for el in soup.find_all(attrs={"class": CHROME}):
        el.decompose()
    for el in soup.find_all(attrs={"id": CHROME}):
        el.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" ").lower())


# --- коммерческий фильтр ---
COMM_STEMS = ("экскурс", "тур", "гид", "трансфер", "бронир", "заказ", "куп",
              "цен", "стоим", "аренд", "прокат", "такси", "поездк", "путев",
              "путёв", "винн", "дегуст", "индивид", "частн", "однодн", "многодн")
GEO_FROM = re.compile(r"\bиз\s+(тбилиси|батуми|кутаиси|москв|нальчик|владикавказ|"
                      r"минеральн|минвод|ставропол|краснодар|пятигорск|грозн|"
                      r"махачкал|ереван|баку)", re.I)
INFO_BLOCK = re.compile(r"(что посмотр|как добра|нужна ли|можно ли|почему|погод|"
                        r"история|достопримеч|карта|виза|valюt|сколько денег|"
                        r"бюджет|что попроб|рецепт)", re.I)


def tokens(phrase: str) -> list[str]:
    return re.findall(r"[а-яё]+", phrase.lower())


def is_commercial(phrase: str) -> bool:
    if INFO_BLOCK.search(phrase):
        return False
    toks = tokens(phrase)
    if any(t.startswith(COMM_STEMS) for t in toks):
        return True
    if GEO_FROM.search(phrase):
        return True
    return False


# --- иерархия: (заголовок кластера, regex). Порядок = приоритет назначения. ---
CLUSTERS: list[tuple[str, re.Pattern]] = [
    ("Гео-туры из городов РФ/Кавказа",
     re.compile(r"\bиз\s+(москв|нальчик|владикавказ|минеральн|минвод|ставропол|"
                r"краснодар|пятигорск|грозн|махачкал|ереван|баку)")),
    ("Трансфер", re.compile(r"трансфер|аэропорт|такси")),
    ("Частный гид", re.compile(r"\bгид")),
    ("Винные туры (Кахетия)", re.compile(r"винн|дегустац|\bвино\b|квеври")),
    ("Гастрономические туры", re.compile(r"гастроном|кулинарн|ужин|хинкал|хачапур|готов")),
    ("Казбеги / Гудаури", re.compile(r"казбег|степанцминд|гергет|гудаур|ананури|жинвал")),
    ("Кахетия / Сигнахи", re.compile(r"кахет|сигнаг|сигнах|бодбе|телав|цинандал|алаверд")),
    ("Мцхета", re.compile(r"мцхет|джвар|светицховел")),
    ("Кутаиси / каньоны", re.compile(r"кутаис|прометея|окаце|мартвил|каньон|кинчх")),
    ("Гори / Уплисцихе", re.compile(r"\bгори\b|уплисцих|сталин")),
    ("Боржоми / Бакуриани", re.compile(r"боржом|бакуриан")),
    ("Сванетия", re.compile(r"сванет|местиа|ушгул|мести")),
    ("Вардзиа / Самцхе", re.compile(r"вардзи|ахалцих|рабат")),
    ("Многодневные туры по Грузии", re.compile(r"многодн|\d\s*дн|недел|тур по грузии|"
                                              r"туры по грузии|туры в грузию|тур в грузию")),
    ("Ночной Тбилиси", re.compile(r"ночн")),
    ("Обзорные / пешие по Тбилиси", re.compile(r"обзорн|пешеход|пеш|прогулк|старый город|"
                                              r"серн")),
    ("Экскурсии по Тбилиси (общее)", re.compile(r"тбилиси")),
    ("Цены и бронирование", re.compile(r"цен|стоим|бронир|заказ|предоплат")),
]


def cluster_of(phrase: str) -> str:
    for name, rx in CLUSTERS:
        if rx.search(phrase):
            return name
    return "Прочее коммерческое"


def main() -> None:
    # 1. кандидаты из уже собранного ядра
    wb = load_workbook(XLSX, read_only=True)
    cands: dict[str, int] = {}   # meta keyword -> страниц использует (из ядра)
    for r in wb["Ядро (meta keywords)"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            cands[r[0].strip().lower()] = r[1] or 0
    comm = sorted({c for c in cands if len(tokens(c)) >= 1 and is_commercial(c)})
    print(f"meta-ключей: {len(cands)}, коммерческих: {len(comm)}")

    # 2. частота вхождений + охват страниц по реальному контенту
    files = sorted(p for p in ROOT.rglob("*.html") if is_ru_page(p))
    occ = Counter()
    pages = Counter()
    for p in files:
        try:
            txt = page_text(p.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        for kw in comm:
            n = txt.count(kw)
            if n:
                occ[kw] += n
                pages[kw] += 1

    # частотность ключа = на скольких страницах он прописан в ядре (meta),
    # вторично — вхождений в видимом тексте
    def freq(k: str) -> int:
        return cands.get(k, 0)

    # 3. иерархия
    tree: dict[str, list[str]] = defaultdict(list)
    for k in comm:
        tree[cluster_of(k)].append(k)
    for c in tree:
        tree[c].sort(key=lambda k: (-freq(k), -occ[k], k))
    cluster_total = {c: sum(freq(k) for k in ks) for c, ks in tree.items()}
    order = sorted(tree, key=lambda c: (-cluster_total[c], -len(tree[c])))

    # 4. печать дерева
    print("\n" + "=" * 60)
    for c in order:
        print(f"\n■ {c}  ({len(tree[c])} ключей)")
        for k in tree[c]:
            print(f"    ядро:{freq(k)}  текст:{occ[k]:>3}  {k}")

    # 5. Excel
    out_wb = Workbook()
    ws = out_wb.active
    ws.title = "Коммерческое ядро"
    ws.append(["Кластер (уровень 1)", "Ключ (коммерческий)",
               "Частота в ядре (страниц)", "Вхождений в тексте"])
    hf = PatternFill("solid", fgColor="1A3D2E")
    ff = Font(color="FFFFFF", bold=True)
    cf = Font(bold=True, color="1A3D2E")
    sub = PatternFill("solid", fgColor="EAF3EE")
    for c in range(1, 5):
        ws.cell(1, c).fill = hf
        ws.cell(1, c).font = ff
    for c in order:
        rrow = ws.max_row + 1
        ws.cell(rrow, 1, f"{c}  ({len(tree[c])})").font = cf
        for cc in range(1, 5):
            ws.cell(rrow, cc).fill = sub
        for k in tree[c]:
            ws.append(["", k, cands.get(k, 0), occ[k]])
    for i, w in enumerate([34, 50, 22, 18], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    out = ROOT / "scripts" / "semcore_commercial.xlsx"
    out_wb.save(out)
    print(f"\nСохранено: {out}  (ключей: {len(comm)}, кластеров: {len(order)})")


if __name__ == "__main__":
    main()
