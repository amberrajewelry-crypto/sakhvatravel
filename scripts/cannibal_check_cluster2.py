#!/usr/bin/env python3
"""Strict cannibalization check for cluster-2 (thermal/dental/camping/marriage/rafting)
x ru/en/ka. Cannibal = ANOTHER same-language page whose <title> or <h1> targets the
same query token. Body mentions are donors, not cannibals — so we match title+H1 only."""
import os, re, glob
ROOT="/Users/vladimir/sakhva-travel"; os.chdir(ROOT)

# cluster-2 canonical pages (the page itself is never its own cannibal)
CLUSTER = {
 "ru": ["blog/termalnye-istochniki-gruzii","blog/lechenie-zubov-v-gruzii","blog/kemping-glamping-gruziya","blog/kak-raspisatsya-v-gruzii","blog/rafting-v-gruzii"],
 "en": ["en/blog/thermal-springs-georgia","en/blog/dental-tourism-georgia","en/blog/camping-glamping-georgia","en/blog/how-to-get-married-in-georgia","en/blog/rafting-in-georgia"],
 "ka": ["ge/blog/thermal-springs-georgia","ge/blog/dental-tourism-georgia","ge/blog/camping-glamping-georgia","ge/blog/how-to-get-married-in-georgia","ge/blog/rafting-in-georgia"],
}
# per-theme query tokens by language (core intent word in title/H1)
THEMES = {
 "thermal": {"ru":r"термальн", "en":r"thermal spring", "ka":r"თერმ"},
 "dental":  {"ru":r"(лечени[ея] зуб|стоматолог|зубн)", "en":r"dental", "ka":r"(სტომატ|კბილ)"},
 "camping": {"ru":r"(кемпинг|глэмпинг|глемпинг)", "en":r"(camping|glamping)", "ka":r"(კემპინგ|გლემპ)"},
 "marriage":{"ru":r"(расписат|регистраци[яю] брак|брак в грузии|заключить брак|ЗАГС)", "en":r"(get married|marriage regist|register.* marriage|wedding regist)", "ka":r"(ქორწ|დაქორწ)"},
 "rafting": {"ru":r"рафтинг", "en":r"rafting", "ka":r"რაფტინგ"},
}

def lang_of(p):
    if p.startswith("ge/"): return "ka"
    if p.startswith("en/"): return "en"
    return "ru"

def title_h1(h):
    t=re.search(r"<title>(.*?)</title>",h,re.S|re.I); t=t.group(1).strip() if t else ""
    h1=""
    m=re.search(r"<h1[^>]*>(.*?)</h1>",h,re.S|re.I)
    if m: h1=re.sub(r"<[^>]+>"," ",m.group(1)).strip()
    return t,h1

# index all pages by language
pages=[]  # (relpath, lang, title, h1)
for p in glob.glob("**/*.html", recursive=True):
    if any(s in p for s in (".worktrees/","node_modules/","_stars_backup","scripts/","/demo/","index.html.base")): continue
    try: h=open(p,encoding="utf-8",errors="ignore").read()
    except: continue
    t,h1=title_h1(h); pages.append((p,lang_of(p),t,h1))

def norm(rel): return rel[:-len("/index.html")] if rel.endswith("/index.html") else rel

print(f"проиндексировано страниц: {len(pages)}\n"+"="*64)
any_flag=False
for theme,langs in THEMES.items():
    for lang,tok in langs.items():
        rx=re.compile(tok,re.I)
        cluster_norms={c for c in CLUSTER[lang]}
        hits=[]
        for rel,pl,t,h1 in pages:
            if pl!=lang: continue
            if rx.search(t) or rx.search(h1):
                hits.append((norm(rel),t[:70]))
        # split self vs others
        others=[(r,t) for r,t in hits if r not in cluster_norms]
        selfhit=[(r,t) for r,t in hits if r in cluster_norms]
        status = "OK (только своя)" if not others else f"⚠ ВОЗМОЖНЫЙ КАННИБАЛ x{len(others)}"
        if others: any_flag=True
        print(f"\n[{theme} / {lang}] {status}  токен=/{tok}/")
        for r,t in selfhit: print(f"    self: {r}  «{t}»")
        for r,t in others:  print(f"    >>>> {r}  «{t}»")
        if not hits: print("    (нет страниц с этим токеном в title/H1 — тема-сирота? проверь)")

print("\n"+"="*64)
print("ИТОГ: "+("есть кандидаты в каннибалы (см. >>>>)" if any_flag else "ЧИСТО — каннибалов в title/H1 не найдено"))
