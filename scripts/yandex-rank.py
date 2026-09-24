#!/usr/bin/env python3
"""
Трекер позиций в Яндексе через Yandex Cloud Search API v2.

Зачем: у Яндекса нет GSC-аналога с API, Вебмастер отдаёт позиции скудно.
Этот скрипт снимает живую выдачу и пишет историю в data/yandex-ranks.jsonl,
чтобы видеть движение после ПФ/правок, а не верить на слово.

Использование:
    python3 scripts/yandex-rank.py --targets scripts/rank-targets.csv
    python3 scripts/yandex-rank.py --query "гид в тбилиси" --region 10277
    python3 scripts/yandex-rank.py --diff          # что изменилось с прошлого прогона

Регионы: 10277 = Тбилиси (основная аудитория), 213 = Москва (спрос на туры).
Формат rank-targets.csv: url,запрос,регион
"""
import argparse, csv, json, os, re, subprocess, sys, datetime
import concurrent.futures as cf

# Mac keeps skills in ~/.claude/skills, VPS in ~/.claude-data/skills
SKILL = next((p for p in map(os.path.expanduser, ('~/.claude/skills/yandex-search-api',
                                                  '~/.claude-data/skills/yandex-search-api'))
              if os.path.isdir(p)), os.path.expanduser('~/.claude/skills/yandex-search-api'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, 'data', 'yandex-ranks.jsonl')
DOMAIN = 'sakhva-travel.com'
DEPTH = 30


def serp(query, region, depth=DEPTH):
    """Одна выдача. Возвращает (позиция|None, найденный_url, топ-5 доменов)."""
    p = subprocess.run(
        ['bash', f'{SKILL}/scripts/web_search_sync.sh',
         '-q', query, '-r', str(region), '-n', str(depth)],
        capture_output=True, text=True, timeout=180, cwd=SKILL)
    m = re.search(r'JSON:\s*(\S+)', p.stdout)
    if not m:
        return None, '', [], 'ERR'
    d = json.load(open(m.group(1)))
    rs = d if isinstance(d, list) else d.get('results', d.get('items', []))
    urls = [x.get('url', '') for x in rs]
    pos = next((i + 1 for i, u in enumerate(urls) if DOMAIN in u), None)
    found = next((u for u in urls if DOMAIN in u), '')
    top = [re.sub(r'https?://(www\.)?', '', u).split('/')[0] for u in urls[:5]]
    return pos, found, top, 'OK'


def load_targets(path):
    out = []
    with open(path, encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if not row or row[0].startswith('#') or row[0] == 'url':
                continue
            url, query = row[0].strip(), row[1].strip()
            regions = [int(x) for x in (row[2].split('|') if len(row) > 2 and row[2] else ['10277', '213'])]
            for r in regions:
                out.append((url, query, r))
    return out


def run(targets, workers=5):
    stamp = datetime.date.today().isoformat()
    rows = []

    def one(t):
        url, query, region = t
        try:
            pos, found, top, st = serp(query, region)
        except Exception as e:
            pos, found, top, st = None, '', [], f'ERR:{e.__class__.__name__}'
        return {'date': stamp, 'url': url, 'query': query, 'region': region,
                'pos': pos, 'found_url': found, 'top5': top, 'status': st}

    with cf.ThreadPoolExecutor(workers) as ex:
        for r in ex.map(one, targets):
            rows.append(r)
            p = r['pos'] or '>%d' % DEPTH
            print(f"{r['region']:>6} {str(p):>4}  {r['query'][:44]:<44} {r['url']}")
    os.makedirs(os.path.dirname(HIST), exist_ok=True)
    with open(HIST, 'a', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f"\n{len(rows)} замеров дописано в {HIST}")
    return rows


def diff():
    """Сравнить два последних прогона."""
    if not os.path.exists(HIST):
        sys.exit('нет истории — сначала сделай прогон')
    recs = [json.loads(l) for l in open(HIST, encoding='utf-8')]
    dates = sorted({r['date'] for r in recs})
    if len(dates) < 2:
        sys.exit('нужно минимум два прогона в разные дни')
    prev, cur = dates[-2], dates[-1]
    key = lambda r: (r['url'], r['query'], r['region'])
    a = {key(r): r['pos'] for r in recs if r['date'] == prev}
    b = {key(r): r['pos'] for r in recs if r['date'] == cur}
    moves = []
    for k in b:
        if k not in a:
            continue
        pa, pb = a[k] or 99, b[k] or 99
        if pa != pb:
            moves.append((pa - pb, pa, pb, k))
    moves.sort(reverse=True)
    print(f"{prev} -> {cur}\n")
    for delta, pa, pb, k in moves:
        sign = '+' if delta > 0 else ''
        print(f"{sign}{delta:>4}  {pa:>3} -> {pb:<3}  рег{k[2]}  {k[1][:40]:<40} {k[0]}")
    if not moves:
        print('без движения')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--targets')
    ap.add_argument('--query')
    ap.add_argument('--region', type=int, default=10277)
    ap.add_argument('--diff', action='store_true')
    ap.add_argument('--workers', type=int, default=5)
    a = ap.parse_args()
    if a.diff:
        diff()
    elif a.query:
        pos, found, top, st = serp(a.query, a.region)
        print(json.dumps({'query': a.query, 'region': a.region, 'pos': pos,
                          'url': found, 'top5': top}, ensure_ascii=False, indent=2))
    elif a.targets:
        run(load_targets(a.targets), a.workers)
    else:
        ap.print_help()
