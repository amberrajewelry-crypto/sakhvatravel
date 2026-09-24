#!/usr/bin/env python3
"""Легитимный скан переспама (тошнота) по RU-страницам Sakhva.
Без платных API: pymorphy3 (аналог Mystem) + расчёт академ./классич. тошноты.
Исключает 301-редиректы из vercel.json (мёртвые URL не отдают контент)."""
import re, json, math, sys
from pathlib import Path
from collections import Counter
import pymorphy3

ROOT = Path("/Users/vladimir/sakhva-travel")
morph = pymorphy3.MorphAnalyzer()

# POS, которые не считаем значимыми (служебные)
SKIP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO", "Apro"}
# мусорные леммы (общие глаголы/слова, не ключи)
STOP = {"быть", "это", "весь", "свой", "который", "мочь", "такой", "наш",
        "ваш", "очень", "если", "когда", "уже", "ещё", "более", "также",
        "что", "как", "для", "под", "над", "при", "про", "она", "они"}

def visible_text(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    # вырезаем JSON-LD и meta — мерим читаемый текст
    html = re.sub(r"<head[\s\S]*?</head>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&[a-z]+;", " ", html)
    return html

def lemmas(text: str):
    words = re.findall(r"[а-яёА-ЯЁ]{4,}", text.lower())
    out = []
    for w in words:
        p = morph.parse(w)[0]
        if p.tag.POS in SKIP_POS:
            continue
        lem = p.normal_form
        if lem in STOP or len(lem) < 4:
            continue
        out.append(lem)
    return out

EN_STOP = {"the", "and", "for", "with", "you", "your", "from", "this", "that",
           "are", "our", "out", "can", "all", "but", "not", "have", "has",
           "will", "they", "what", "when", "where", "who", "how", "why",
           "their", "there", "here", "into", "over", "more", "most", "some",
           "any", "each", "than", "then", "them", "its", "his", "her", "she",
           "him", "had", "was", "were", "been", "being", "about", "also",
           "just", "only", "very", "much", "many", "such", "one", "two",
           "get", "got", "see", "way", "day", "use", "may", "per", "via"}

def lemmas_en(text: str):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    out = []
    for w in words:
        if w in EN_STOP:
            continue
        # грубая нормализация множественного числа
        if w.endswith("ies") and len(w) > 4:
            w = w[:-3] + "y"
        elif w.endswith("es") and len(w) > 4:
            w = w[:-2]
        elif w.endswith("s") and not w.endswith("ss") and len(w) > 4:
            w = w[:-1]
        out.append(w)
    return out

def redirected_sources():
    """source-пути с 301 из vercel.json -> множество для исключения."""
    vj = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    red = set()
    for r in vj.get("redirects", []):
        src = r.get("source", "").strip("/")
        red.add(src)
    return red

# служебные/технические страницы — к ранжированию контента не относятся
SKIP_URL = {"", "blog", "gallery", "policy", "terms", "contacts", "privacy",
            "booking", "prices/spasibo", "spasibo", "links", "offer",
            "en", "en/blog", "en/gallery", "en/links", "en/contacts",
            "en/booking", "en/privacy", "en/terms", "en/policy"}

def page_paths(en=False):
    paths = []
    base = ROOT / "en" if en else ROOT
    for p in base.rglob("index.html"):
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if "node_modules" in parts or "scripts" in parts:
            continue
        is_en = "en" in parts
        if en and not is_en:
            continue
        if not en and is_en:
            continue
        paths.append(p)
    return sorted(set(paths))

def main():
    en = "--en" in sys.argv
    red = redirected_sources()
    rows = []
    skipped = 0
    for p in page_paths(en=en):
        url = "/" + str(p.parent.relative_to(ROOT)).replace("\\", "/").strip("/")
        url_key = url.strip("/")
        if url_key in red or url_key in SKIP_URL:   # мёртвый 301 или служебная
            skipped += 1
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        lems = lemmas_en(visible_text(html)) if en else lemmas(visible_text(html))
        total = len(lems)
        if total < 50:
            continue
        c = Counter(lems)
        top_lem, top_cnt = c.most_common(1)[0]
        acad = top_cnt / total * 100
        classic = math.sqrt(top_cnt)
        top3 = ", ".join(f"{l}:{n}" for l, n in c.most_common(3))
        rows.append((acad, classic, top_cnt, total, top_lem, top3, url))
    rows.sort(reverse=True)
    zone = "EN" if en else "RU"
    print(f"Проанализировано: {len(rows)} {zone}-страниц | пропущено 301/служебных: {skipped}\n")
    print(f"{'акад%':>6} {'клас':>5} {'повт':>4} {'слов':>5}  топ-лемма / топ-3")
    print("-" * 90)
    risk = 0
    for acad, classic, cnt, total, lem, top3, url in rows:
        flag = ""
        if acad >= 7:                # строгий флаг: только академ. тошнота (Баден-Баден)
            flag = " ⚠"
            risk += 1
        print(f"{acad:6.1f} {classic:5.1f} {cnt:4d} {total:5d}  [{top3}]  {url}{flag}")
    print("-" * 90)
    print(f"РИСК ПЕРЕСПАМА (академ. тошнота ≥7%): {risk} из {len(rows)}")

if __name__ == "__main__":
    main()
