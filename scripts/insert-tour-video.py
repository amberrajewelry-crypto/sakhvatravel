#!/usr/bin/env python3
"""Insert the SAKHVA muted-drone "video about the tour" block into a tour page.

Anchor rule (universal): find the first real content container
`<div class="article-body">` or `<div class="sec-text">` (whichever appears
first), then insert the <figure> right after the first `</p>` that follows it
(the intro paragraph). Idempotent: skips a file that already has .tour-video.

Usage:
  insert-tour-video.py --slug ekskursiya-borjomi-iz-tbilisi \
      --drone borjomi-drone.mp4 --poster borjomi-tour-600.webp \
      --name-ru "Боржоми" --name-en "Borjomi" --name-ge "ბორჯომი"
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SVG = ('<svg width="76" height="43" viewBox="0 0 118 66" fill="none" '
       'xmlns="http://www.w3.org/2000/svg"><circle cx="59" cy="20" r="10" fill="#F59E0B" opacity=".92"/>'
       '<path d="M4 34 L20 20 L32 27 L59 14 L86 27 L98 20 L114 34 Z" fill="currentColor"/>'
       '<path d="M55 18 L59 14 L63 18 Z" fill="#fff" opacity=".85"/>'
       '<text x="59" y="53" text-anchor="middle" font-family="Raleway,system-ui,sans-serif" '
       'font-weight="800" font-size="15" letter-spacing="3" fill="currentColor">SAKHVA</text>'
       '<line x1="4" y1="60" x2="30" y2="60" stroke="#F59E0B" stroke-width=".9" stroke-linecap="round"/>'
       '<text x="59" y="64" text-anchor="middle" font-family="Raleway,system-ui,sans-serif" '
       'font-weight="700" font-size="7" letter-spacing="2.5" fill="#F59E0B">TRAVEL</text>'
       '<line x1="88" y1="60" x2="114" y2="60" stroke="#F59E0B" stroke-width=".9" stroke-linecap="round"/></svg>')

SCRIPT = ("<script>(function(){var f=document.querySelector('.tour-video[data-src]');if(!f)return;"
          "var v=f.querySelector('.tv-v'),loaded=false;\n"
          "function load(){if(loaded)return;loaded=true;var s=document.createElement('source');"
          "s.src=f.getAttribute('data-src');s.type='video/mp4';v.appendChild(s);v.load();"
          "var p=v.play();if(p&&p.catch)p.catch(function(){});}\n"
          "if('IntersectionObserver' in window){new IntersectionObserver(function(es,o){"
          "es.forEach(function(e){if(e.isIntersecting){load();o.disconnect();}});},{threshold:0.35})"
          ".observe(f);}else{load();}})();</script>")


def block(drone: str, poster: str, aria: str) -> str:
    fig = (
        f'<figure class="tour-video" data-src="/images/{drone}" '
        'style="position:relative;margin:26px 0;border-radius:16px;overflow:hidden;'
        'box-shadow:0 12px 38px rgba(0,0,0,.18);aspect-ratio:16/9;'
        f"background:#0F241A center/cover url('/images/{poster}') no-repeat\">\n"
        f'<video class="tv-v" muted loop playsinline preload="none" poster="/images/{poster}" '
        f'aria-label="{aria}" '
        'style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;z-index:1"></video>\n'
        '<span class="tv-brand" aria-hidden="true" '
        'style="position:absolute;top:12px;left:14px;z-index:3;pointer-events:none;color:#fff;'
        'line-height:0;filter:drop-shadow(0 2px 6px rgba(0,0,0,.7))">\n'
        f'{SVG}\n</span>\n</figure>'
    )
    return fig + '\n' + SCRIPT


def find_anchor(html: str) -> int:
    """Return index just after the first intro </p>, or -1."""
    candidates = [html.find('<div class="article-body">'), html.find('<div class="sec-text">')]
    candidates = [c for c in candidates if c != -1]
    if not candidates:
        return -1
    start = min(candidates)
    p_end = html.find('</p>', start)
    if p_end == -1:
        return -1
    return p_end + len('</p>')


def process(path: Path, drone: str, poster: str, aria: str) -> str:
    html = path.read_text(encoding='utf-8')
    if 'class="tour-video"' in html:
        return 'skip (already present)'
    at = find_anchor(html)
    if at == -1:
        return 'ERROR: anchor not found'
    new = html[:at] + '\n' + block(drone, poster, aria) + html[at:]
    path.write_text(new, encoding='utf-8')
    return 'inserted'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', required=True)
    ap.add_argument('--drone', required=True)
    ap.add_argument('--poster', required=True)
    ap.add_argument('--name-ru', required=True)
    ap.add_argument('--name-en', required=True)
    ap.add_argument('--name-ge', required=True)
    a = ap.parse_args()
    aria = {
        'ru': f'{a.name_ru} — виды тура',
        'en': f'{a.name_en} — tour views',
        'ge': f'{a.name_ge} — ტურის ხედები',
    }
    rel = {
        'ru': ROOT / 'ekskursiya' / a.slug / 'index.html',
        'en': ROOT / 'en' / 'ekskursiya' / a.slug / 'index.html',
        'ge': ROOT / 'ge' / 'ekskursiya' / a.slug / 'index.html',
    }
    rc = 0
    for lang, path in rel.items():
        if not path.exists():
            print(f'{lang}: missing file')
            continue
        res = process(path, a.drone, a.poster, aria[lang])
        print(f'{lang}: {res}')
        if res.startswith('ERROR'):
            rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
