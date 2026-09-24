#!/usr/bin/env python3
"""Fix GSC 'Duplicate unique resources': remove offers+aggregateRating from
TouristTrip JSON-LD so they live only in the Product node (which carries stars).
Targets RU /ekskursiya/*/ and EN /en/ekskursiya/*/ tour pages."""
import re
import sys
import json
import glob
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = "--apply" not in sys.argv
BACKUP = ROOT / "scripts" / "_schema_dup_backup"

LD_RE = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)
REMOVE_KEYS = ("offers", "aggregateRating")

targets = sorted(
    glob.glob(str(ROOT / "ekskursiya" / "*" / "index.html"))
    + glob.glob(str(ROOT / "en" / "ekskursiya" / "*" / "index.html"))
)

changed = 0
skipped = 0
for fp in targets:
    html = Path(fp).read_text(encoding="utf-8")
    new_html = html
    file_touched = False

    for m in LD_RE.finditer(html):
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body)
        except Exception:
            continue
        if not isinstance(data, dict) or data.get("@type") != "TouristTrip":
            continue
        removed = [k for k in REMOVE_KEYS if k in data]
        if not removed:
            continue
        for k in removed:
            del data[k]
        new_body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        old_block = open_tag + body + close_tag
        new_block = open_tag + new_body + close_tag
        new_html = new_html.replace(old_block, new_block, 1)
        file_touched = True
        rel = fp.replace(str(ROOT) + "/", "")
        print(f"  {rel}: убрал {removed} из TouristTrip")

    if file_touched:
        changed += 1
        if not DRY:
            bdest = BACKUP / Path(fp).relative_to(ROOT)
            bdest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp, bdest)
            Path(fp).write_text(new_html, encoding="utf-8")
    else:
        skipped += 1

mode = "DRY-RUN (без записи)" if DRY else "ПРИМЕНЕНО"
print(f"\n{mode}: изменено {changed}, без дубля {skipped}, всего {len(targets)}")
if DRY:
    print("Для применения: python3 scripts/fix-schema-duplicate.py --apply")
else:
    print(f"Бэкапы: {BACKUP}")
