#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Движок перевода /ge/ с translation-memory (TM).
Метод пилотов (якорная замена html.replace(en,ka) + счётчик), но TM общий на
семейство: повторяющиеся шаблонные строки переводятся ОДИН раз.

  extract <files...>  — печатает НОВЫЕ англ-строки (нет в TM, не груз/бренд/число)
                        в JSON, чтобы перевести и дописать в TM.
  apply   <files...>  — применяет TM ко всем строкам файла + верификация:
                        каждый ключ TM, если встречается, заменяется; после —
                        ассерт «нет непереведённых видимых англ-строк».
TM: scripts/ge_tm.json  (плоский {en: ka}).  Идемпотентно.
"""
import sys, re, json, os, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TM_PATH = ROOT / "scripts/ge_tm.json"

# Бренды/латиница, которые ОСТАЮТСЯ как есть (не переводить, не флагать)
BRANDS = {
    "SAKHVA", "TRAVEL", "Sakhva Travel", "Sakhva", "FAQ", "TIN", "NOWPayments",
    "USDT", "TRC-20", "Bitcoin", "BTC", "Ethereum", "ETH", "BNB", "Visa",
    "Mastercard", "MIR", "AMEX", "WhatsApp", "Telegram", "Instagram", "WiFi",
    "Timur", "Google", "TripAdvisor", "Yandex", "Yandex Maps", "2GIS", "Viator",
    "Tripster", "UNESCO", "GEL", "USD", "EUR", "QR", "USB", "AC", "4WD", "SUV",
    "flydubai", "Emirates", "Turkish Airlines", "Georgian Airways", "Wizz Air",
    "Pegasus", "FlyArystan", "SCAT", "Red Wings", "Azimuth", "Aeroflot",
    "S7", "Nordwind", "Utair", "Pobeda", "Slow Travel", "Bo3", "ASAN",
}

def load_tm():
    if TM_PATH.exists():
        return json.loads(TM_PATH.read_text(encoding="utf-8"))
    return {}

def save_tm(tm):
    TM_PATH.write_text(json.dumps(tm, ensure_ascii=False, indent=1, sort_keys=True),
                       encoding="utf-8")

def is_georgian(s):
    return bool(re.search(r'[Ⴀ-ჿ]', s))

def has_letters(s):
    return bool(re.search(r'[A-Za-z]{2,}', s))

def is_brandy(s):
    """строка целиком из брендов/чисел/пунктуации → не переводить"""
    t = s.strip()
    if not has_letters(t):
        return True
    # убрать HTML-entity (&copy; и пр.), бренды, римские цифры веков, числа, пунктуацию
    rest = re.sub(r'&#?x?\w+;', ' ', t)
    for b in sorted(BRANDS, key=len, reverse=True):
        rest = rest.replace(b, " ")
    rest = re.sub(r'\b[IVXLCDM]{1,7}\b', ' ', rest)   # XII/XVI/I — века, не англ
    rest = re.sub(r'[0-9\W_]+', ' ', rest)
    return not re.search(r'[A-Za-z]{2,}', rest)

# машинные значения, которые НЕЛЬЗЯ переводить (даже если латиница)
_SKIP_EXACT = {"en_US", "ka_GE", "ru_RU", "summary_large_image", "article", "website",
               "EN", "RU", "GE", "index,follow"}
_HUMAN_META = ("description", "og:title", "og:description", "twitter:title",
               "twitter:description", "og:image:alt")

def _machine(t):
    """структурный/машинный токен — не человеко-текст"""
    if t in _SKIP_EXACT: return True
    if re.match(r'^https?://', t): return True                 # URL
    if re.match(r'^[\w.:-]+/[\w.:-]+', t) and ' ' not in t: return True  # mime/path
    if re.search(r'(max-image-preview|initial-scale|device-width|max-snippet)', t): return True
    if re.match(r'^[a-z]+([,;][a-z-]+)+$', t): return True      # index,follow / key;key
    # только «copy»/entity-мусор
    if not re.search(r'[A-Za-z]{3,}', re.sub(r'&\w+;', ' ', t)): return True
    return False

JSONLD_KEYS = {"name", "description", "text", "reviewBody", "headline", "alternateName"}

def _jsonld_blocks(html):
    return list(re.finditer(
        r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))

def _walk_strings(o, emit):
    """emit(value) для каждого nl-значения по JSONLD_KEYS; вернуть (опц.) новый объект"""
    if isinstance(o, dict):
        return {k: (emit(v) if (k in JSONLD_KEYS and isinstance(v, str))
                    else _walk_strings(v, emit)) for k, v in o.items()}
    if isinstance(o, list):
        return [_walk_strings(x, emit) for x in o]
    return o

def jsonld_candidates(html):
    out = set()
    for m in _jsonld_blocks(html):
        try:
            data = json.loads(m.group(2))
        except Exception:
            continue
        def emit(v):
            t = v.strip()
            # НЕ гейтить по is_georgian: смешанная строка (груз. топоним + англ.
            # предложение) обязана попасть в кандидаты. has_letters требует латиницу,
            # поэтому чисто грузинские строки и так отсеиваются; is_brandy убирает
            # строки, где латиница — только бренды.
            if t and has_letters(t) and not is_brandy(t) and not _machine(t):
                out.add(t)
            return v
        _walk_strings(data, emit)
    return out

def candidates(html):
    """множество кандидатных англ-строк: текст-ноды + человеко-мета + alt/aria/placeholder"""
    out = set()
    body = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    def ok(t):
        # без is_georgian-гейта: ловим и смешанные строки (см. jsonld_candidates)
        return (t and has_letters(t)
                and not is_brandy(t) and not _machine(t))
    # текст-ноды
    for m in re.findall(r'>([^<>]+)<', body):
        t = m.strip()
        if ok(t): out.add(t)
    # человеко-мета: только whitelisted name/property
    for tag in re.findall(r'<meta\b[^>]*>', html):
        key = re.search(r'(?:name|property)="([^"]+)"', tag)
        cont = re.search(r'content="([^"]+)"', tag)
        if key and cont and key.group(1) in _HUMAN_META:
            t = cont.group(1).strip()
            if ok(t): out.add(t)
    # человеко-атрибуты
    for attr in ("alt", "aria-label", "placeholder", "title"):
        for m in re.findall(attr + r'="([^"]+)"', html):
            t = m.strip()
            if ok(t): out.add(t)
    return out

def cmd_extract(files):
    tm = load_tm()
    new = set()
    for f in files:
        html = Path(f).read_text(encoding="utf-8")
        for c in candidates(html) | jsonld_candidates(html):
            if c not in tm:
                new.add(c)
    new = sorted(new, key=lambda s: (-len(s), s))
    print(json.dumps({"new_count": len(new), "tm_size": len(tm), "new": new},
                     ensure_ascii=False, indent=1))

def cmd_apply(files):
    tm = load_tm()
    # длинные ключи первыми — чтобы подстроки не съедали надстроки
    keys = sorted(tm.keys(), key=len, reverse=True)
    for f in files:
        html = Path(f).read_text(encoding="utf-8")
        # 1) JSON-LD: перевести nl-значения через TM (структуру/ключи не трогаем)
        for m in reversed(_jsonld_blocks(html)):
            try:
                data = json.loads(m.group(2))
            except Exception:
                continue
            data2 = _walk_strings(data, lambda v: tm.get(v.strip(), v))
            new_json = json.dumps(data2, ensure_ascii=False, separators=(",", ":"))
            html = html[:m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]
        # 2) видимый текст/атрибуты: якорная замена.
        #    Защищаем ВСЕ <script> (инлайн-JS + JSON-LD уже переведён) — чтобы
        #    bare-replace не задел JS-строки, совпадающие с лейблами (квиз/booking).
        protected = {}
        def _prot(m):
            key = f"\x00SCRIPT{len(protected)}\x00"
            protected[key] = m.group(0)
            return key
        html = re.sub(r'<script.*?</script>', _prot, html, flags=re.S)
        for k in keys:
            if k in html:
                html = html.replace(k, tm[k])
        for key, orig in protected.items():
            html = html.replace(key, orig)
        Path(f).write_text(html, encoding="utf-8")
        # верификация: непереведённые видимые + JSON-LD
        left = list(candidates(html) | jsonld_candidates(html))
        status = "OK" if not left else f"⚠ {len(left)} непереведённых"
        print(f"  {f}: {status}")
        for l in left[:12]:
            print(f"      | {l[:80]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ge_i18n.py extract|apply <files...>"); sys.exit(1)
    cmd, files = sys.argv[1], sys.argv[2:]
    # раскрыть glob
    exp = []
    for f in files:
        exp += glob.glob(f) if any(c in f for c in "*?[") else [f]
    {"extract": cmd_extract, "apply": cmd_apply}[cmd](exp)
