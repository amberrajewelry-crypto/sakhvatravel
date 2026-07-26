#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ge_fix_schema_urls.py — чинит /en/ URL внутри JSON-LD на GE-страницах.

При переводе breadcrumb/author в ld+json скопированы из EN-двойника и указывают
на /en/ вместо /ge/. Это ломает языковую консистентность структурированных данных.

Логика (ТОЛЬКО внутри <script type=ld+json>, hreflang вне — не трогаем):
  (1) прямая замена каталогов с существующими GE-двойниками:
      /en/blog/ /en/about/ /en/destinations/ /en/wine-tours-georgia/ + home /en/
  (2) BreadcrumbList c /en/tours-in-georgia/ (GE-каталога туров НЕТ, 404):
      удаляем этот промежуточный элемент, перенумеровываем position → честный
      2-уровневый breadcrumb Home > Тур.
  (3) любой оставшийся /en/tours-in-georgia/ вне breadcrumb → /ge/ (home fallback).

Usage: python3 scripts/ge_fix_schema_urls.py [files...]   (по умолчанию все ge/)
"""
import sys, re, os, json, glob

ROOT = "/Users/vladimir/sakhva-travel"
os.chdir(ROOT)

BASE = "https://sakhva-travel.com"
DIRECT = {
    f"{BASE}/en/blog/": f"{BASE}/ge/blog/",
    f"{BASE}/en/about/": f"{BASE}/ge/about/",
    f"{BASE}/en/destinations/": f"{BASE}/ge/destinations/",
    f"{BASE}/en/wine-tours-georgia/": f"{BASE}/ge/wine-tours-georgia/",
    f"{BASE}/en/": f"{BASE}/ge/",          # home — применять ПОСЛЕ длинных
}
TOURS_CAT = f"{BASE}/en/tours-in-georgia/"  # GE-каталога нет → спец-обработка

SCRIPT_RE = re.compile(
    r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.S | re.I)


def _remap_str(s):
    """Прямая замена строкового URL по карте (длинные ключи раньше home)."""
    if not isinstance(s, str):
        return s
    for k in sorted(DIRECT, key=lambda x: -len(x)):
        if s == k or s.startswith(k):
            # точное совпадение каталога/home ИЛИ префикс (напр. /en/blog/ уже поймали выше)
            if s == k:
                return DIRECT[k]
    # оставшийся tours-in-georgia вне breadcrumb → home
    if s == TOURS_CAT:
        return f"{BASE}/ge/"
    return s


def _walk(node):
    """Рекурсивно чинит url/@id/item; схлопывает breadcrumb с каталогом туров."""
    if isinstance(node, dict):
        # breadcrumb: удалить элемент с каталогом туров, перенумеровать
        if node.get("@type") == "BreadcrumbList" and isinstance(node.get("itemListElement"), list):
            items = node["itemListElement"]
            kept = []
            for el in items:
                item = el.get("item") if isinstance(el, dict) else None
                url = item.get("@id") if isinstance(item, dict) else item
                if isinstance(url, str) and url == TOURS_CAT:
                    continue  # выкидываем несуществующий GE-каталог
                kept.append(el)
            # перенумерация position 1..N
            for i, el in enumerate(kept, 1):
                if isinstance(el, dict) and "position" in el:
                    el["position"] = i
            node["itemListElement"] = kept
        for k, v in list(node.items()):
            if isinstance(v, str):
                node[k] = _remap_str(v)
            else:
                _walk(v)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                node[i] = _remap_str(v)
            else:
                _walk(v)
    return node


def fix(fp):
    h = open(fp, encoding="utf-8").read()
    changed = [False]

    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        try:
            data = json.loads(body)
        except Exception:
            return m.group(0)  # не JSON — пропускаем
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        data = _walk(data)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before == after:
            return m.group(0)
        changed[0] = True
        new_body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return f"{head}{new_body}{tail}"

    h2 = SCRIPT_RE.sub(repl, h)
    if changed[0]:
        open(fp, "w", encoding="utf-8").write(h2)
    return changed[0]


if __name__ == "__main__":
    files = sys.argv[1:] or glob.glob("ge/**/index.html", recursive=True)
    n = sum(fix(f) for f in files)
    print(f"ge_fix_schema_urls: изменено {n}/{len(files)} файлов")
