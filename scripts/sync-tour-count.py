"""Sync tour count from data/catalog.json into homepage + partner pages (ru/en/ka)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N = len(json.load(open(ROOT / "data/catalog.json"))["excursions"])
FILES = ["index.html", "en/index.html", "ge/index.html",
         "partners/index.html", "partners/en/index.html", "partners/ge/index.html"]
# ponytail: phrase list, not template markers — add a phrase here if a new counter appears
PHRASES = [r"туров в каталоге", r"авторских туров", r"авторских маршрутов", r"каталогом \d+ туров",
           r"tours in", r"authentic tours", r"authentic routes", r"catalog of \d+ tours",
           r"საავტორო ტურ", r"ტურის კატალოგ"]
PAT = re.compile(r"(?<![\d.#])\b\d{2}\b(?=(?:</div><div class=\"cap\">)?\s*(?:%s))" %
                 "|".join(p.replace(r"\d+", "") for p in PHRASES))
NUM_CAP = re.compile(r'<div class="num">\d{2}</div>(?=<div class="cap">)')
changed = 0
for f in FILES:
    p = ROOT / f; s = p.read_text()
    t = PAT.sub(str(N), s)
    t = re.sub(r"(каталогом |catalog of )\d+( туров| tours)", rf"\g<1>{N}\g<2>", t)
    if t != s:
        p.write_text(t); changed += 1; print("updated", f)
print(f"tours={N} files_changed={changed}")
if __name__ == "__main__" and "--check" in sys.argv:
    assert PAT.sub("XX", '<div class="num">67</div><div class="cap">авторских туров') .startswith('<div class="num">XX')
