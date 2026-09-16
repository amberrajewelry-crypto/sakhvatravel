"""Make teaser videos indexable: static <source> + VideoObject JSON-LD.

Google Video report showed 175 'video not indexed' after teasers were added:
<video> had no src in HTML (JS injected it on intersection) and no VideoObject.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sakhva-travel.com"
SKIP = ("node_modules", "scripts/", ".vercel")
UPLOAD_DATE = "2026-09-03"  # teasers went live site-wide


def duration(mp4: Path) -> str:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout
    return f"PT{max(1, round(float(out or 0)))}S"


def author(lang: str) -> dict:
    name = {"ru": "Тимур Сахвадзе", "en": "Timur Sakhvadze", "ge": "თიმურ სახვაძე"}[lang]
    url = {"ru": "/about/", "en": "/en/about/", "ge": "/ge/about/"}[lang]
    return {"@type": "Person", "name": name, "url": SITE + url}


def fix(p: Path) -> bool:
    s = p.read_text()
    m = re.search(r'<figure class="tour-video" data-src="([^"]+)"', s)
    if not m:
        return False
    src = m.group(1)
    mp4 = ROOT / src.split("?")[0].lstrip("/")
    if not mp4.exists():
        print("MISSING", src, p); return False
    v = re.search(r'<video class="tv-v"([^>]*)></video>', s)
    if not v:
        return False
    attrs = v.group(1)
    poster = re.search(r'poster="([^"]+)"', attrs).group(1)
    label = re.search(r'aria-label="([^"]+)"', attrs).group(1)
    rel = p.relative_to(ROOT).as_posix()
    lang = "en" if rel.startswith("en/") else "ge" if rel.startswith("ge/") else "ru"
    desc = re.search(r'<meta (?:name="description" content="([^"]*)"|content="([^"]*)" name="description")', s)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    changed = False
    # 1. static <source>: preload="none" keeps it from downloading until play()
    s2 = s.replace(v.group(0),
        f'<video class="tv-v"{attrs}><source src="{src}" type="video/mp4"></video>')
    if s2 != s:
        s, changed = s2, True
    # loader: source already present -> just load/play
    s2 = s.replace(
        "function load(){if(loaded)return;loaded=true;var s=document.createElement('source');"
        "s.src=f.getAttribute('data-src');s.type='video/mp4';v.appendChild(s);v.load();",
        "function load(){if(loaded)return;loaded=true;v.load();")
    if s2 != s:
        s, changed = s2, True
    # 2. VideoObject
    if "VideoObject" not in s:
        vo = {"@context": "https://schema.org", "@type": "VideoObject",
              "name": label, "description": ((desc.group(1) or desc.group(2)) if desc else label),
              "thumbnailUrl": SITE + poster, "contentUrl": SITE + src,
              "uploadDate": UPLOAD_DATE, "duration": duration(mp4),
              "author": author(lang)}
        if canon:
            vo["url"] = canon.group(1)
        tag = ('<script type="application/ld+json">'
               + json.dumps(vo, ensure_ascii=False) + "</script>\n")
        s = s.replace("</head>", tag + "</head>", 1)
        changed = True
    if changed:
        p.write_text(s)
    return changed


if __name__ == "__main__":
    files = [p for p in ROOT.rglob("*.html") if not any(k in p.as_posix() for k in SKIP)]
    n = sum(fix(p) for p in files)
    print("fixed", n)
