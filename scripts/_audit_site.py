#!/usr/bin/env python3
"""Сквозной аудит sakhva-travel: программные + текстовые ошибки. Read-only."""
import re, glob, json, html as htmllib, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
EXCLUDE = ('node_modules', 'scripts/', 'backup', '.backup', 'preview-', 'hero3d', 'demo/',
           'design-previews/', 'gid/_template/', '-verify', 'miralinks', 'payment-success',
           'tour-cards-video', '_schema_dupkey_backup', '/google', '/yandex_', 'google5', 'google8',
           'yandex_', 'tour-card', 'preview')
allf = [f for f in glob.glob('**/*.html', recursive=True) if not any(x in f for x in EXCLUDE)]
# PROD = реальные SEO-страницы (есть canonical). Остальное (404, служебное) — вне аудита контента.
files = []
for f in allf:
    try:
        head = open(f, encoding='utf-8', errors='ignore').read(12000)
    except: continue
    if 'rel="canonical"' in head:
        files.append(f)

issues = defaultdict(list)  # category -> [ (file, detail) ]

# индекс существующих путей для проверки внутренних ссылок
def exists_route(href):
    href = href.split('#')[0].split('?')[0]
    if not href.startswith('/'):
        return True  # внешние/относительные/mailto/tel — пропускаем отдельно
    p = href.lstrip('/')
    if p == '' or href == '/':
        return os.path.exists('index.html')
    cands = [p, p+'index.html', p.rstrip('/')+'/index.html', p.rstrip('/')+'.html']
    # статика
    if os.path.exists(p): return True
    return any(os.path.exists(c) for c in cands)

titles = {}
descs = {}

for f in files:
    h = open(f, encoding='utf-8', errors='ignore').read()
    raw = h

    # --- ПРОГРАММНЫЕ ---
    # 1. JSON-LD валидность
    for m in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            json.loads(m.strip())
        except Exception as e:
            issues['jsonld_invalid'].append((f, str(e)[:60]))

    # 2. div-баланс
    opens = len(re.findall(r'<div\b', h)); closes = len(re.findall(r'</div>', h))
    if opens != closes:
        issues['div_balance'].append((f, f'{opens} open / {closes} close (Δ{opens-closes})'))

    # 3. битые внутренние ссылки
    for href in set(re.findall(r'href="(/[^"#][^"]*)"', h)):
        if href.startswith('//'): continue
        if not exists_route(href):
            issues['broken_link'].append((f, href))

    # 4. битые изображения (src/href на /images/ или /…webp|jpg|png)
    for src in set(re.findall(r'(?:src|href)="(/[^"]+\.(?:webp|jpg|jpeg|png|svg|avif))"', h, re.I)):
        if not os.path.exists(src.lstrip('/').split('?')[0]):
            issues['broken_image'].append((f, src))

    # 5. title/description дубли + длина
    mt = re.search(r'<title>([^<]*)</title>', h)
    if mt:
        t = mt.group(1).strip()
        titles.setdefault(t, []).append(f)
        if len(t) > 65: issues['title_long'].append((f, f'{len(t)}: {t[:50]}'))
        if len(t) < 15: issues['title_short'].append((f, f'{len(t)}: {t}'))
    else:
        issues['no_title'].append((f, ''))
    md = re.search(r'name="description"[^>]*content="([^"]*)"|content="([^"]*)"[^>]*name="description"', h)
    if md:
        d = (md.group(1) or md.group(2) or '').strip()
        descs.setdefault(d, []).append(f)
        if len(d) > 170: issues['desc_long'].append((f, f'{len(d)}'))
        if 0 < len(d) < 50: issues['desc_short'].append((f, f'{len(d)}'))
    else:
        issues['no_desc'].append((f, ''))

    # 6. canonical присутствует
    if not re.search(r'rel="canonical"', h):
        issues['no_canonical'].append((f, ''))

    # 7. несколько H1
    h1 = len(re.findall(r'<h1\b', h))
    if h1 == 0: issues['no_h1'].append((f, ''))
    elif h1 > 1: issues['multi_h1'].append((f, f'{h1} H1'))

    # --- ТЕКСТОВЫЕ (по видимому тексту) ---
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S|re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = htmllib.unescape(body)

    # артефакты
    for pat, name in [(r'%%', 'двойной %%'), (r'>\s*undefined\s*<', 'undefined'),
                      (r'>\s*NaN\s*<', 'NaN'), (r'\[object Object\]', '[object Object]'),
                      (r'\{\{[^}]+\}\}', 'незаменённый {{шаблон}}'),
                      (r'\bлорем\b|\blorem ipsum\b', 'lorem'),
                      (r'�', 'битый юникод'), (r'\bTODO\b|\bFIXME\b|\bXXX\b', 'TODO/FIXME')]:
        if re.search(pat, body, re.I):
            issues['text_artifact'].append((f, name))

# дубли title/desc
for t, fs in titles.items():
    if len(fs) > 1:
        issues['dup_title'].append((fs[0], f'×{len(fs)}: "{t[:45]}" + {len(fs)-1} др.'))
for d, fs in descs.items():
    if len(fs) > 1 and d:
        issues['dup_desc'].append((fs[0], f'×{len(fs)}: "{d[:40]}…"'))

# --- ОТЧЁТ ---
order = ['jsonld_invalid','div_balance','broken_link','broken_image','no_title','no_h1','multi_h1',
         'no_canonical','no_desc','dup_title','dup_desc','title_long','title_short','desc_long','desc_short',
         'text_artifact']
labels = {
 'jsonld_invalid':'❌ JSON-LD невалиден','div_balance':'❌ Дисбаланс <div>','broken_link':'❌ Битая внутр. ссылка',
 'broken_image':'❌ Битое изображение','no_title':'❌ Нет <title>','no_h1':'⚠️ Нет H1','multi_h1':'⚠️ Несколько H1',
 'no_canonical':'⚠️ Нет canonical','no_desc':'⚠️ Нет description','dup_title':'⚠️ Дубль title','dup_desc':'⚠️ Дубль description',
 'title_long':'· title >65','title_short':'⚠️ title <15','desc_long':'· desc >170','desc_short':'· desc <50',
 'text_artifact':'❌ Текст-артефакт','word_repeat':'⚠️ Повтор слова','double_space':'· Двойной пробел',
 'space_before_punct':'· Пробел перед пунктуацией'}

print(f"АУДИТ sakhva-travel — {len(files)} HTML\n"+"="*52)
total=0
for k in order:
    v = issues.get(k, [])
    if not v: continue
    total += len(v)
    print(f"\n{labels[k]} — {len(v)}")
    for f, d in v[:12]:
        print(f"    {f}  {d}")
    if len(v) > 12:
        print(f"    … ещё {len(v)-12}")
print("\n"+"="*52)
crit = sum(len(issues.get(k,[])) for k in ['jsonld_invalid','div_balance','broken_link','broken_image','no_title','text_artifact'])
print(f"ИТОГО проблем: {total}  |  критических: {crit}")
