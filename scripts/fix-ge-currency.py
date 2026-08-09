#!/usr/bin/env python3
"""RUB->GEL on 8 Georgian hub pages.
Pages declare canonical ₾ next to every ₽ (parenthetical, inline "₾/₽", or a ₾/₽
two-column table). We use the page's OWN declared ₾ (never blindly ÷35), drop the
₽ column/segment, and convert ruble-only spots (title/meta/schema) via a per-page
₽->₾ map. ÷35 is a last-resort fallback and every use of it is reported.
Usage: python3 scripts/fix-ge-currency.py [--apply]   (default = dry-run)
"""
import re, sys, pathlib

RATE = 35
APPLY = "--apply" in sys.argv
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["ge/tury-na-kazbek", "ge/grupovye-tury-v-gruziyu", "ge/ekskursionnye-tury-v-gruziyu",
         "ge/individualnyy-tur-v-gruziyu", "ge/tury-v-gruziyu-zimoy", "ge/tury-v-gruziyu-s-detmi",
         "ge/tury-v-gruziyu-letom", "ge/tury-v-batumi"]

RATE_NOTE = "ფასები რუბლებში გამოითვლება კურსით ₾1 = 35 ₽. საბოლოო თანხა დამოკიდებულია მიმდინარე კურსზე. დაზუსტდება გიდთან."
CLEAN_NOTE = "ფასები მოცემულია ლარში (₾)."
SP = "[\\d   ]"          # digit or (space, nbsp, narrow-nbsp)
GE = "[Ⴀ-ჿ]"            # Georgian letters

def num(s): return int(re.sub(r"\s| | ", "", s))

def build_map(s):
    m = {}
    for rx, gi, ri in [
        (re.compile(r"(\d%s*?)\s*₽(?:-%s+)?\s*\(₾(\d+)" % (SP, GE)), 2, 1),  # N ₽[-suf] (₾M
        (re.compile(r"₾(\d+)%s*\s*/\s*(\d%s*?)\s*₽" % (GE, SP)), 1, 2),     # ₾M / N ₽
        (re.compile(r"(\d%s*?)\s*₽[/%s.]*\s*/\s*₾(\d+)" % (SP, GE)), 2, 1), # N ₽ / ₾M
        (re.compile(r"<td>₾(\d+)[^<]*</td>\s*<td>\s*(\d%s*?)\s*₽" % SP), 1, 2),  # <td>₾M</td><td>N ₽
    ]:
        for g in rx.finditer(s):
            m[num(g.group(ri))] = int(g.group(gi))
    return m

def convert(path, s):
    warns = []
    m = build_map(s)
    def lari(r):
        r = num(r)
        if r in m: return m[r]
        warns.append(r); return round(r / RATE)
    s = re.sub(r"ფასები რუბლებში გამოითვლება კურსით ₾1 = 35 ₽\.", CLEAN_NOTE, s)
    s = s.replace("ფასები ₽-სა და ₾-ში", "ფასები ₾-ში")
    # strip ruble hint after a lari price: "25 ₾-დან (~700 ₽)" / "80 ₾ (დაახლოებით 2800 ₽)" -> keep lari
    s = re.sub(r"((?:\d+\s*₾|₾\d+)(?:-%s+)?)\s*\((?:~|დაახლოებით)?\s*\d%s*\s*₽[^)]*\)" % (GE, SP), r"\1", s)
    # 1. two-column table: drop ₽ header + the ₽ <td> after a ₾ <td>
    s = re.sub(r"\s*<th>[^<]*₽[^<]*</th>", "", s)
    s = re.sub(r"(<td>₾\d+[^<]*</td>)\s*<td>[^<]*₽[^<]*</td>", r"\1", s)
    # 2. parenthetical "N ₽[-suf] (₾M...)" -> "₾M[-suf]" (via map)
    s = re.sub(r"(\d%s*?)\s*₽(-%s+)?\s*\(₾\d+[^)]*\)" % (SP, GE),
               lambda g: "₾%d%s" % (lari(g.group(1)), g.group(2) or ""), s)
    # 3. remaining ruble-only -> ₾ via map (fallback ÷35, reported)
    s = re.sub(r"(\d%s*?)\s*₽(-%s+)?" % (SP, GE),
               lambda g: "₾%d%s" % (lari(g.group(1)), g.group(2) or ""), s)
    # 4. collapse inline dup "₾X / ₾X" (was "₾X / N ₽") -> "₾X"
    s = re.sub(r"₾(\d+)\s*/\s*₾\1(?!\d)", r"₾\1", s)
    # 5. schema currency label + numeric via map
    s = re.sub(r'"(price|lowPrice|highPrice)":"(\d+)","priceCurrency":"RUB"',
               lambda g: '"%s":"%d","priceCurrency":"GEL"' % (g.group(1), lari(g.group(2))), s)
    s = re.sub(r'"priceCurrency":"RUB","(price|lowPrice|highPrice)":"(\d+)"',
               lambda g: '"priceCurrency":"GEL","%s":"%d"' % (g.group(1), lari(g.group(2))), s)
    return s, warns

def demo():
    s = ('<title>7 700 ₽-იდან</title>'
         '<th>ფასი ₾</th><th>ფასი ₽</th>'
         '<td>₾98</td><td>2 700 ₽</td>'
         '<td>₾58 / 2 030 ₽</td>'
         '7 700 ₽-დან (₾220/კაცზე) 12 250 ₽-დან (₾350/კაცზე)'
         '"price":"2700","priceCurrency":"RUB"')
    out, w = convert("demo", s)
    assert "₽" not in out and '"RUB"' not in out, out
    assert "<th>ფასი ₽</th>" not in out, out                                        # ₽ header removed
    assert "<td>₾98</td>" in out and "700" not in out, out                          # ₽ col cell dropped
    assert "<td>₾58</td>" in out and "/ ₾" not in out, out                          # inline collapsed
    assert '<title>₾220-იდან' in out, out                                          # title mapped 7700->220
    assert '"price":"98","priceCurrency":"GEL"' in out, out                        # schema 2700->98 via map
    assert w == [], "unexpected ÷35 fallback in demo: %s" % w
    print("demo OK")

demo()
total_warn = {}
for p in PAGES:
    f = ROOT / p / "index.html"
    src = f.read_text(encoding="utf-8")
    out, warns = convert(p, src)
    left = out.count("₽") + len(re.findall(r'"RUB"', out))
    changed = sum(1 for a, b in zip(src.splitlines(), out.splitlines()) if a != b)
    if warns: total_warn[p] = sorted(set(warns))
    print(f"{p:38s} строк={changed:3d}  ост.₽/RUB={left}  ÷35-fallback={sorted(set(warns))}")
    if APPLY and out != src:
        f.write_text(out, encoding="utf-8")
if total_warn:
    print("\n⚠ ÷35 fallback (нет пары ₾ на странице) — проверить:", total_warn)
print("APPLIED" if APPLY else "DRY-RUN (add --apply to write)")
