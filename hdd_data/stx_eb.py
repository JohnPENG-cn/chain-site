"""希捷 10-Q / 10-K 里的「HDD Exabytes Shipped」与「HDD Price per Terabyte」→ hdd_data/stx_eb.json。
原始文件在 hdd_data/raw/stx_f/（gitignore，不入库）；SEC EDGAR 公开文件，2026-10-30 下载。
口径：10-Q 第一列 = 当季；10-K 只给全年，Q4 = 全年 − 前三季（Q3 10-Q 的年初至今列）。价格只取公司披露值（FY2026 起不再披露）。"""
import json, re, pathlib
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).parent
sub = json.load(open(R / 'raw/stx_sub.json'))['filings']['recent']
rows = {}
ytd = {}
for i, f in enumerate(sub['form']):
    if f not in ('10-Q', '10-K') or sub['filingDate'][i] < '2020-01-01':
        continue
    end = sub['reportDate'][i]
    t = re.sub(r'\s+', ' ', BeautifulSoup(open(R / 'raw/stx_f' / sub['primaryDocument'][i], encoding='utf-8', errors='ignore').read(), 'html.parser').get_text(' '))
    m = re.search(r'Exabytes Shipped(.{0,400})', t).group(1)
    nl = [float(x) for x in re.search(r'(?:Nearline|Mass capacity) ([\d. ]+)', m).group(1).split()]
    tot = [float(x) for x in re.search(r'Total ([\d. ]+)', m).group(1).split()]
    pr = re.search(r'Price per Terabyte ((?:\$ \d+ ?)+)', m)
    pr = [int(x) for x in re.findall(r'\d+', pr.group(1))] if pr else []
    if f == '10-Q':
        rows[end] = {'end': end, 'eb': tot[0], 'nl': nl[0], 'px': pr[0] if pr else None}
        if len(tot) == 5:
            ytd[end] = (tot[3], nl[3])
    else:
        rows[end] = {'end': end, 'fy_eb': tot[0], 'fy_nl': nl[0], 'fy_px': pr[0] if pr else None}
ends = sorted(rows)
for k, e in enumerate(ends):
    r = rows[e]
    if 'fy_eb' in r and k and ends[k - 1] in ytd:
        y = ytd[ends[k - 1]]
        r['eb'], r['nl'], r['px'] = round(r['fy_eb'] - y[0], 1), round(r['fy_nl'] - y[1], 1), None
q = {x['end'][:7]: x for x in json.load(open(R / 'quarterly.json'))['stx']}
for e in ends:
    r = rows[e]
    rv = q.get(e[:7], {}).get('rev')
    r['rev'] = rv
    r['rev_per_tb'] = round(rv / r['eb'], 1) if rv and r.get('eb') else None
json.dump([rows[e] for e in ends], open(R / 'stx_eb.json', 'w'), ensure_ascii=False, indent=0)
for e in ends:
    print(rows[e])
