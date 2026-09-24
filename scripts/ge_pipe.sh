#!/bin/zsh
# ge_pipe.sh <ge-file> — весь пост-TM конвейер одним вызовом.
# Ожидает, что переводы уже в ge_tm.json. Делает: анкоры, apply, chrome,
# скан, паритет, reciprocity, sitemap. Печатает ИТОГ скана и паритета.
set -e
cd /Users/vladimir/sakhva-travel
F="$1"
python3 - "$F" <<'PY'
import sys
from pathlib import Path
f=sys.argv[1]; p=Path(f); h=p.read_text(encoding="utf-8")
h=h.replace(">Georgia<",">საქართველო<").replace(">and<",">და<").replace("> and <","> და <").replace(">Airline<",">ავიახაზი<")
for a,b in {'aria-label="Меню"':'aria-label="მენიუ"','aria-label="Закрыть"':'aria-label="დახურვა"','aria-label="Контакт"':'aria-label="კონტაქტი"','aria-label="Музыка"':'aria-label="მუსიკა"'}.items():
    h=h.replace(a,b)
p.write_text(h,encoding="utf-8")
PY
python3 scripts/ge_i18n.py apply "$F" >/dev/null 2>&1
python3 scripts/ge_chrome.py "$F" >/dev/null 2>&1
echo -n "СКАН: "; python3 scripts/ge_strict_scan.py "$F" 2>&1 | grep "ИТОГ:"
python3 scripts/ge_strict_scan.py "$F" 2>&1 | grep -E "\[EN\]|\[RU\]" | head -8
echo -n "ПАРИТЕТ: "; python3 scripts/ge_parity.py "$F" 2>&1 | grep "ИТОГ:"
python3 scripts/ge_parity.py "$F" 2>&1 | grep "  | " | head -6
python3 scripts/reciprocity_ge.py "$F" >/dev/null 2>&1
python3 scripts/sitemap_reciprocity_ge.py >/dev/null 2>&1
echo "DONE $F"
