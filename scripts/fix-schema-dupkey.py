#!/usr/bin/env python3
"""Fix GSC 'Unparsable structured data / Duplicate unique resources':
some BlogPosting JSON-LD nodes contain the SAME key (`@id`) twice — invalid
JSON that Google can't parse. Detect duplicate keys and re-serialize the block
(json.loads keeps the last value; both @id values are identical here)."""
import re
import sys
import json
import glob
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = "--apply" not in sys.argv
BACKUP = ROOT / "scripts" / "_schema_dupkey_backup"
LD_RE = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)


class DupKey(Exception):
    pass


def detect_dupes(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise DupKey(k)
        seen.add(k)
    return dict(pairs)


targets = sorted(
    glob.glob(str(ROOT / "blog" / "*" / "index.html"))
    + glob.glob(str(ROOT / "en" / "blog" / "*" / "index.html"))
)

changed = 0
for fp in targets:
    html = Path(fp).read_text(encoding="utf-8")
    new_html = html
    touched_keys = []

    for m in LD_RE.finditer(html):
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        # is it parseable at all?
        try:
            normal = json.loads(body)
        except Exception:
            continue
        # does it contain a duplicate key anywhere?
        try:
            json.loads(body, object_pairs_hook=detect_dupes)
            continue  # no dup keys -> leave untouched
        except DupKey as e:
            touched_keys.append(str(e))
        # re-serialize clean (compact) — last value wins, dup key dropped
        clean = json.dumps(normal, ensure_ascii=False, separators=(",", ":"))
        new_html = new_html.replace(open_tag + body + close_tag,
                                    open_tag + clean + close_tag, 1)

    if touched_keys:
        changed += 1
        rel = fp.replace(str(ROOT) + "/", "")
        print(f"  {rel}: дубль ключей {touched_keys}")
        if not DRY:
            bdest = BACKUP / Path(fp).relative_to(ROOT)
            bdest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp, bdest)
            Path(fp).write_text(new_html, encoding="utf-8")

mode = "DRY-RUN (без записи)" if DRY else "ПРИМЕНЕНО"
print(f"\n{mode}: файлов с дублем ключей {changed} из {len(targets)}")
if DRY:
    print("Применить: python3 scripts/fix-schema-dupkey.py --apply")
else:
    print(f"Бэкапы: {BACKUP}")
