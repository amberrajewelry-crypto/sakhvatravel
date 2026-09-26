#!/usr/bin/env python3
"""Add a "check the weather" card linking tour/blog pages to /pogoda/<place>/ (ru/en/ge).

Idempotent: pages that already have id="pogoda-check" are skipped.
EN/GE counterparts are resolved through the RU page's hreflang links.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sakhva-travel.com"

# RU source page -> weather place
PAGES: dict[str, str] = {
    "ekskursiya/ekskursiya-kakheti-iz-tbilisi": "kakheti",
    "ekskursiya/degustatsiya-vina-kakheti": "kakheti",
    "ekskursiya/tur-kazbegi-kakheti-2-dnya": "kakheti",
    "blog/tury-v-kakheti-2026": "kakheti",
    "blog/kazbegi-ili-kakheti": "kakheti",
    "blog/kakheti-osenyu": "kakheti",
    "ekskursiya/ekskursiya-sighnaghi-iz-tbilisi": "signagi",
    "ekskursiya/vinniy-marshrut-alazani": "signagi",
    "blog/kakheti-za-1-den": "signagi",
    "ekskursiya/ekskursiya-telavi-iz-tbilisi": "telavi",
    "ekskursiya/vinodelie-kindzmarauli": "telavi",
    "ekskursiya/kvevri-vino-tur": "telavi",
    "ekskursiya/ekskursiya-racha-iz-tbilisi": "racha",
    "ekskursiya/ekskursiya-stary-tbilisi": "tbilisi",
    "ekskursiya/progulka-po-kure-tbilisi": "tbilisi",
    "blog/chto-posmotret-v-tbilisi": "tbilisi",
    "blog/tbilisi-za-1-den": "tbilisi",
    "blog/tbilisi-za-3-dnya": "tbilisi",
}

NAMES = {
    "ru": {"kakheti": "в Кахетии", "signagi": "в Сигнахи", "telavi": "в Телави",
           "racha": "в Раче", "tbilisi": "в Тбилиси"},
    "en": {"kakheti": "in Kakheti", "signagi": "in Signagi", "telavi": "in Telavi",
           "racha": "in Racha", "tbilisi": "in Tbilisi"},
    "ka": {"kakheti": "კახეთში", "signagi": "სიღნაღში", "telavi": "თელავში",
           "racha": "რაჭაში", "tbilisi": "თბილისში"},
}
TEXT = {
    "ru": ("Проверить погоду {n}", "Прогноз на неделю и климат по месяцам перед поездкой"),
    "en": ("Check the weather {n}", "7-day forecast and month-by-month climate before your trip"),
    "ka": ("შეამოწმეთ ამინდი {n}", "კვირის პროგნოზი და კლიმატი თვეების მიხედვით მოგზაურობამდე"),
}
PREFIX = {"ru": "", "en": "/en", "ka": "/ge"}

SVG = ('<svg width="30" height="30" viewBox="0 0 64 64" style="flex-shrink:0" aria-hidden="true">'
       '<circle cx="26" cy="26" r="11" fill="#F59E0B"/><g stroke="#F59E0B" stroke-width="3" '
       'stroke-linecap="round"><line x1="26" y1="6" x2="26" y2="12"/><line x1="26" y1="40" '
       'x2="26" y2="46"/><line x1="6" y1="26" x2="12" y2="26"/><line x1="40" y1="26" x2="46" '
       'y2="26"/><line x1="12" y1="12" x2="16" y2="16"/><line x1="36" y1="36" x2="40" y2="40"/>'
       '</g><path d="M30 44a10 10 0 010-20 13 13 0 0125-3 9 9 0 01-2 23z" fill="#e3e8ec" '
       'stroke="#b3bfc9" stroke-width="1.5"/></svg>')


def block(lang: str, place: str) -> str:
    title, sub = TEXT[lang]
    href = f"{PREFIX[lang]}/pogoda/{place}/"
    return (
        '<section id="pogoda-check" style="max-width:1000px;margin:0 auto;padding:8px 16px 44px">'
        f'<a href="{href}" style="display:flex;align-items:center;gap:14px;padding:18px 22px;'
        'border:1px solid #ECECE4;border-radius:16px;background:linear-gradient(160deg,#fff,#fafaf7);'
        'box-shadow:0 1px 2px rgba(0,0,0,.03);text-decoration:none">' + SVG +
        '<span style="flex:1"><strong style="display:block;font-size:16px;color:#1A3D2E;'
        f'font-family:Lora,Georgia,serif">{title.format(n=NAMES[lang][place])}</strong>'
        '<span style="font-size:13px;color:#6B7280;font-family:Lora,Georgia,serif">'
        f'{sub}</span></span><span style="color:#B45309;font-weight:700;font-size:18px">→</span>'
        '</a></section>\n'
    )


def insert(path: Path, lang: str, place: str) -> bool:
    s = path.read_text(encoding="utf-8")
    if 'id="pogoda-check"' in s:
        return False
    b = block(lang, place)
    if "<!-- trv:end -->" in s:
        s = s.replace("<!-- trv:end -->", "<!-- trv:end -->\n" + b, 1)
    else:
        i = s.find("<footer")
        assert i > 0, f"no footer: {path}"
        s = s[:i] + b + s[i:]
    path.write_text(s, encoding="utf-8")
    return True


def counterparts(ru_html: str) -> dict[str, Path]:
    out = {}
    for lang in ("en", "ka"):
        m = re.search(rf'<link[^>]*href="{SITE}(/[^"]*)"[^>]*hreflang="{lang}"', ru_html) or \
            re.search(rf'<link[^>]*hreflang="{lang}"[^>]*href="{SITE}(/[^"]*)"', ru_html)
        if m:
            p = ROOT / m.group(1).strip("/") / "index.html"
            if p.exists():
                out[lang] = p
    return out


def main() -> None:
    added = 0
    for rel, place in PAGES.items():
        ru = ROOT / rel / "index.html"
        added += insert(ru, "ru", place)
        for lang, p in counterparts(ru.read_text(encoding="utf-8")).items():
            added += insert(p, lang, place)
    print("added", added)


if __name__ == "__main__":
    assert 'href="/en/pogoda/racha/"' in block("en", "racha")
    assert "რაჭაში" in block("ka", "racha")
    main()
