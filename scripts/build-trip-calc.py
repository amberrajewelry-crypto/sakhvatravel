#!/usr/bin/env python3
"""Refresh the trip budget widget (js/trip-calc.js) and bust its cache on every page using it.

- tour prices from data/catalog.json, RUB rate from the National Bank of Georgia API,
  open.er-api.com if NBG blocks the request, else the rate already in the file;
- rewrites the DATA block between /* gen:start */ and /* gen:end */;
- sets /js/trip-calc.js?v=<content hash> on every page that has data-trip-calc
  (/js/ is served immutable, so the version must change with the file).
Run after price changes:  python3 scripts/build-trip-calc.py
Embed on a page:  <div data-trip-calc data-tours="ekskursiya-kazbegi-iz-tbilisi"></div>
                  <script src="/js/trip-calc.js?v=..." defer></script>
"""
import datetime
import hashlib
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "js/trip-calc.js"
NBG = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?currencies=RUB"
ER_API = "https://open.er-api.com/v6/latest/GEL"
GEN = re.compile(r"(/\* gen:start \*/\n).*?(\n\s*/\* gen:end \*/)", re.S)
SCRIPT = re.compile(r'/js/trip-calc\.js(\?v=[0-9a-f]+)?')
SKIP_DIRS = {".git", "node_modules", "_archive", ".worktrees", ".vercel"}
TOURS = [  # (catalog slug, short label)
    ("ekskursiya-kazbegi-iz-tbilisi", "Казбеги"),
    ("ekskursiya-kakheti-iz-tbilisi", "Кахетия"),
    ("ekskursiya-mtskheta-iz-tbilisi", "Мцхета"),
    ("ekskursiya-stary-tbilisi", "Старый Тбилиси"),
    ("nochnaya-ekskursiya-tbilisi", "Ночной Тбилиси"),
    ("ekskursiya-david-gareji", "Давид-Гареджа"),
    ("degustatsiya-vina-kakheti", "Дегустация вина"),
    ("ekskursiya-borjomi-iz-tbilisi", "Боржоми"),
]


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def rub_rate() -> tuple[float, str, str] | None:
    """(RUB per 1 GEL, date, source); NBG first, open.er-api.com if NBG blocks the client."""
    try:
        cur = fetch_json(NBG)[0]["currencies"][0]
        day = datetime.date.fromisoformat(cur["date"][:10]).strftime("%d.%m.%Y")
        return round(cur["quantity"] / cur["rate"], 1), day, "Нацбанк Грузии"
    except Exception as e:
        print(f"NBG unavailable ({str(e)[:60]}), trying open.er-api.com")
    try:
        d = fetch_json(ER_API)
        day = datetime.datetime.fromtimestamp(d["time_last_update_unix"], datetime.UTC).strftime("%d.%m.%Y")
        return round(d["rates"]["RUB"], 1), day, "рыночный курс"
    except Exception as e:  # both down: keep the previous rate
        print(f"rate unavailable ({str(e)[:60]}); keeping the old one")
        return None


def main() -> None:
    src = JS.read_text()
    old = json.loads(re.search(r"var DATA = (\{.*?\});", src).group(1))
    rate = rub_rate() or (old["rub"], old["rateDate"], old.get("rateSrc", "Нацбанк Грузии"))
    cat = {x["slug"]: x for x in json.loads((ROOT / "data/catalog.json").read_text())["excursions"]}
    data = {
        "rub": rate[0], "rateDate": rate[1], "rateSrc": rate[2],
        # KeyError here = tour removed from catalog, update TOURS
        "tours": [{"slug": s, "name": n, "price": int(cat[s]["price"])} for s, n in TOURS],
    }
    src = GEN.sub(lambda m: f"{m.group(1)}  var DATA = {json.dumps(data, ensure_ascii=False)};{m.group(2)}", src)
    JS.write_text(src)
    ver = hashlib.sha1(src.encode()).hexdigest()[:8]
    pages = []
    for p in ROOT.rglob("*.html"):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        s = p.read_text()
        if "data-trip-calc" not in s:
            continue
        new = SCRIPT.sub(f"/js/trip-calc.js?v={ver}", s)
        if new != s:
            p.write_text(new)
        pages.append(str(p.relative_to(ROOT)))
    print(f"trip-calc: 1 ₾ = {rate[0]} ₽ ({rate[1]}), {len(data['tours'])} tours, v={ver}, pages: {pages}")


if __name__ == "__main__":
    main()
