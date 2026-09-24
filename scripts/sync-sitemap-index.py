#!/usr/bin/env python3
"""Sync <lastmod> in sitemap-index.xml to the real max(lastmod) of each child.

Root fix for index-lastmod staleness: the index is hand-maintained, so its
lastmod drifts behind child sitemaps after new URLs are added. Run this after
regenerating any child sitemap. Idempotent, stdlib-only.

Usage: python3 scripts/sync-sitemap-index.py [--check]
  --check  exit 1 if index is stale (CI gate), write nothing.
"""
import os
import re
import sys

INDEX = "sitemap-index.xml"


def max_child_lastmod(child_path):
    """Max <lastmod> across a child sitemap's <url> entries, or None."""
    if not os.path.exists(child_path):
        return None
    txt = open(child_path, encoding="utf-8").read()
    dates = re.findall(r"<lastmod>\s*([^<]+?)\s*</lastmod>", txt)
    return max(dates) if dates else None  # ISO dates sort lexically


def sync(check_only=False):
    idx = open(INDEX, encoding="utf-8").read()
    stale = []

    def repl(m):
        block, loc, cur = m.group(0), m.group("loc"), m.group("cur")
        child = os.path.basename(loc.strip())
        real = max_child_lastmod(child)
        if real is None or real == cur:
            return block
        stale.append((child, cur, real))
        return block.replace(f"<lastmod>{cur}</lastmod>",
                             f"<lastmod>{real}</lastmod>", 1)

    # one <sitemap> block = one <loc> + one <lastmod>
    pat = re.compile(
        r"<sitemap>\s*<loc>(?P<loc>[^<]+)</loc>\s*"
        r"<lastmod>(?P<cur>[^<]+)</lastmod>\s*</sitemap>")
    new = pat.sub(repl, idx)

    if check_only:
        for child, cur, real in stale:
            print(f"STALE {child}: index={cur} < real={real}")
        return 1 if stale else 0

    if stale:
        open(INDEX, "w", encoding="utf-8").write(new)
        for child, cur, real in stale:
            print(f"fixed {child}: {cur} -> {real}")
    else:
        print("sitemap-index.xml already in sync")

    # self-check: after write, every index lastmod == max child lastmod
    verify = open(INDEX, encoding="utf-8").read()
    for loc, cur in pat.findall(verify):
        real = max_child_lastmod(os.path.basename(loc.strip()))
        assert real is None or cur == real, f"{loc}: {cur} != {real}"
    return 0


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.exit(sync(check_only="--check" in sys.argv))
