#!/usr/bin/env python3
"""Добавляет WebPage-узел с datePublished/dateModified в JSON-LD тур-страниц.
Даты берутся из git (реальные first/last commit), не «сегодня» — честный recency-сигнал.
Идемпотентно: если WebPage ld+json уже есть — файл пропускается.
Usage: python3 scripts/add-tour-dates.py [--apply]   (без --apply = dry-run)
"""
import re, json, subprocess, sys, glob

APPLY = '--apply' in sys.argv
LIMIT = None
for a in sys.argv:
    if a.startswith('--limit='):
        LIMIT = int(a.split('=')[1])

TREES = ['ekskursiya/*/index.html', 'en/ekskursiya/*/index.html', 'ge/ekskursiya/*/index.html']

def git_last(f):
    return subprocess.run(['git','log','-1','--format=%as','--',f],capture_output=True,text=True).stdout.strip()
def git_first(f):
    out=subprocess.run(['git','log','--diff-filter=A','--format=%as','--',f],capture_output=True,text=True).stdout.strip().splitlines()
    return out[-1] if out else None

files=[]
for t in TREES:
    files += sorted(glob.glob(t))
if LIMIT: files=files[:LIMIT]

changed=skipped=noanchor=0
for f in files:
    html=open(f,encoding='utf-8').read()
    # уже есть WebPage в ld+json?
    if re.search(r'application/ld\+json[^>]*>\s*\{[^<]*"@type"\s*:\s*"WebPage"', html) or '"@type":"WebPage"' in html:
        skipped+=1; continue
    cm=re.search(r'<link[^>]*rel="canonical"[^>]*>',html)
    url=re.search(r'href="([^"]+)"',cm.group(0)).group(1) if cm else None
    if not url:
        noanchor+=1; continue
    lang='ka' if f.startswith('ge/') else ('en' if f.startswith('en/') else 'ru')
    dp=git_first(f) or '2026-05-10'
    dm=git_last(f) or dp
    node={"@context":"https://schema.org","@type":"WebPage","@id":url+"#webpage",
          "url":url,"datePublished":dp,"dateModified":dm,"inLanguage":lang,
          "isPartOf":{"@id":"https://sakhva-travel.com/#website"}}
    snippet='<script type="application/ld+json">'+json.dumps(node,ensure_ascii=False,separators=(',',':'))+'</script>\n'
    # вставить перед первым ld+json блоком
    anchor=re.search(r'<script type="application/ld\+json">',html)
    if not anchor:
        noanchor+=1; continue
    new=html[:anchor.start()]+snippet+html[anchor.start():]
    if APPLY:
        open(f,'w',encoding='utf-8').write(new)
    changed+=1
    if changed<=2:
        print(f"[{lang}] {f}\n   pub={dp} mod={dm} url={url}")

print(f"\n{'ПРИМЕНЕНО' if APPLY else 'DRY-RUN'}: изменить={changed} пропущено(есть WebPage)={skipped} без_canonical={noanchor} всего={len(files)}")
