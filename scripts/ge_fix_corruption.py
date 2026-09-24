#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ge_fix_corruption.py — пост-процессор порчи после ge_i18n apply.

apply делает bare-replace EN-подстрок ВЕЗДЕ (включая URL/onclick/id/class/JS),
из-за чего короткие TM-ключи (tour/wine/blog/Contact/Music/and/Guide...) ломают
технические зоны. Этот скрипт откатывает порчу в НЕ-текстовых зонах, не трогая
переведённый текст (там მუსიკა/კონტაქტი = легит).

Слои: (1) and→და внутри слов; (2) гибридные JS-идентификаторы; (3) URL-слаги
(реверс+валидация по ФС, абс+относит); (4) внешние URL — трансплант из EN-двойника.

Usage: python3 scripts/ge_fix_corruption.py ge/**/*.html   (или конкретные файлы)
       python3 scripts/ge_fix_corruption.py                 (все ge/)
"""
import sys, re, os, glob, itertools

ROOT = "/Users/vladimir/sakhva-travel"
os.chdir(ROOT)

# (1) and→да внутри латинских слов + прочие слитные and-артефакты
AND_FIX = [('yდაex', 'yandex'), ('Yდაex', 'Yandex'), ('brდაy', 'brandy'),
           ('expდაed', 'expanded'), ('lდაscape', 'landscape'), ('stდაard', 'standard'),
           ('sდა', 'sand'), ('/ბლოგი/', '/blog/')]

# (2) явная карта гибридных JS/CSS-идентификаторов
IDMAP = {
    'closeკონტაქტი': 'closeContact', 'openკონტაქტი': 'openContact',
    'sendკონტაქტი': 'sendContact', 'toggleმუსიკა': 'toggleMusic',
    'bgმუსიკა': 'bgMusic', 'foot-brდა': 'foot-brand', 'brდა': 'brand',
    'SakhvaგიდიBot': 'SakhvaGuideBot', 'Sakhvaმოგზაურობა': 'SakhvaTravel',
    'თბილიsi': 'tbilisi', 'ფასიs': 'prices', 'comპარიson': 'comparison',
    'სეზონიs': 'seasons', 'ნარიkala': 'Narikala', 'compანიes': 'companies',
    'ტურიist': 'tourist', 'ტურიst': 'tourist', 'წყალიfall': 'waterfall',
    'boტანიcal': 'botanical', 'bassiანი': 'bassiani', 'restorნებისმიერი': 'restorany',
    'ტურიs': 'tours', 'ბლოგიGrid': 'blogGrid', 'adjარა': 'adjara',
    'chrონიcles': 'chronicles', 'shardენი': 'shardeni', 'ღვინოries': 'wineries',
    'bakuriანი': 'bakuriani', 'commუნიty': 'community', 'sulugუნი': 'sulguni',
    'souvენიrs': 'souvenirs', 'ღვინოs': 'wines', 'pirosმანი': 'pirosmani',
    'qvevri-ღვინო': 'qvevri-wine', '{ტური:': '{tour:',
}

# (3) реверс URL-слагов (мультикандидат, валидация по ФС)
REVM = {'ბლოგი': ['blog'], 'თბილისი': ['tbilisi'], 'თბილი': ['tbili'],
        'ტურები': ['tury', 'tours'], 'ტური': ['tour', 'tur'], 'გიდი': ['gid', 'guide'],
        'ჭაჭა': ['chacha'], 'ლარი': ['lari'], 'უფასო': ['free'], 'სასტუმროები': ['hotels'],
        'სასტუმრო': ['hotel'], 'სეზონი': ['sezon', 'season'], 'როუმინგი': ['roaming'],
        'ნებისმიერი': ['any'], 'პირველი': ['first', 'perviy'], 'მარშრუტი': ['marshrut', 'itinerary'],
        'ფასი': ['price', 'tsena'], 'ღვინო': ['wine', 'vino'], 'ტანი': ['tani'], 'ნარი': ['nari'],
        'ბანი': ['bani'], 'ენი': ['eni'], 'ჰაე': ['hae'], 'სვადბა': ['svadba'], 'svadba': ['svadba']}


def _lp(u):
    p = u.split('#')[0].split('?')[0].strip('/')
    if re.search(r'\.(jpg|jpeg|png|webp|svg|ico|pdf)$', p):
        return p
    return (p + '/index.html') if p else 'index.html'


def _resolve(u):
    words = [w for w in REVM if w in u]
    if not words:
        return u
    for combo in itertools.product(*[REVM[w] for w in words]):
        cu = u
        for w, r in zip(words, combo):
            cu = cu.replace(w, r)
        if not re.search(r'[ა-ჰ]', cu) and os.path.exists(_lp(cu.replace('https://sakhva-travel.com', ''))):
            return cu
    cu = u
    for w in words:
        cu = cu.replace(w, REVM[w][0])
    return cu


def _en_twin(gf):
    en = 'en/' + gf[len('ge/'):]
    return en if os.path.exists(en) else None


def fix(gf):
    h = open(gf, encoding='utf-8').read()
    o = h
    # (1) and-артефакты
    for a, b in AND_FIX:
        h = h.replace(a, b)
    # (2) идентификаторы
    for a, b in sorted(IDMAP.items(), key=lambda x: -len(x[0])):
        h = h.replace(a, b)
    # (3) URL: абсолютные + относительные (href/src + location.href в onclick)
    def _urlfix(m):
        pre, q, u = m.group(1), m.group(2), m.group(3)
        return f'{pre}={q}{_resolve(u)}{q}' if re.search(r'[ა-ჰ]', u) else m.group(0)
    h = re.sub(r'''(href|src)=(['"])((?:https://sakhva-travel\.com)?/[^'"]*)\2''', _urlfix, h)
    h = re.sub(r'''(location\.href\s*=\s*)(['"])(/[^'"]*)\2''',
               lambda m: f'{m.group(1)}{m.group(2)}{_resolve(m.group(3))}{m.group(2)}'
               if re.search(r'[ა-ჰ]', m.group(3)) else m.group(0), h)
    # (4) внешние URL — трансплант чистых из EN-двойника по порядку доменов
    en = _en_twin(gf)
    if en:
        eh = open(en, encoding='utf-8').read()
        dompat = r'https://(?:www\.)?(?:tripadvisor|google|facebook|instagram|youtube|wa|t)\.[a-z.]+/[^\'"\s]*'
        from collections import defaultdict
        def _dom(u):
            return re.search(r'https://(?:www\.)?([a-z]+)\.', u).group(1)
        en_by = defaultdict(list)
        for u in re.findall(dompat, eh):
            en_by[_dom(u)].append(u)
        idx = defaultdict(int)
        for gu in re.findall(dompat, h):
            d = _dom(gu)
            if re.search(r'[ა-ჰ]', gu) and idx[d] < len(en_by[d]):
                h = h.replace(gu, en_by[d][idx[d]], 1)
            idx[d] += 1
    if h != o:
        open(gf, 'w', encoding='utf-8').write(h)
        return True
    return False


if __name__ == "__main__":
    files = sys.argv[1:] or glob.glob("ge/**/*.html", recursive=True)
    n = sum(fix(f) for f in files)
    print(f"ge_fix_corruption: исправлено {n}/{len(files)} файлов")
