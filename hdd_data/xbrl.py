"""SEC XBRL companyfacts（raw/*_facts.json，不入库）→ STX / WDC 季度营收、GAAP 毛利率、存货、资本开支（季度值，Q4 = 全年 − 前三季）。输出 quarterly.json（入库）。"""
import json, os
from datetime import date
H = os.path.dirname(os.path.abspath(__file__))
def series(g, tag):
    if tag not in g: return {}
    out = {}
    for x in g[tag]['units']['USD']:
        if 'start' not in x: continue
        out[(x['start'], x['end'])] = x['val']
    return out
def quarterly(sr):
    """把 3 个月值 + 年度/年累计值拼成季度值（按结束日）。"""
    q = {}
    for (s, e), v in sr.items():
        d = (date.fromisoformat(e) - date.fromisoformat(s)).days
        if 80 < d < 100: q[e] = v
    # 年度 / 年累计减已知季度
    for (s, e), v in sorted(sr.items(), key=lambda t: t[0][1]):
        d = (date.fromisoformat(e) - date.fromisoformat(s)).days
        if e in q or d < 170: continue
        parts = [(ee, vv) for ee, vv in q.items() if s < ee < e]
        n = round(d / 91)
        if len(parts) == n - 1:
            q[e] = v - sum(vv for _, vv in parts)
    return q
def capex_q(sr):
    """资本开支是年累计口径：季度 = 本期年累计 − 上期年累计（同一开始日）。"""
    q = {}
    by = {}
    for (s, e), v in sr.items(): by.setdefault(s, []).append((e, v))
    for s, L in by.items():
        L.sort(); prev = 0
        for e, v in L:
            d = (date.fromisoformat(e) - date.fromisoformat(s)).days
            if d < 80: continue
            q.setdefault(e, v - prev); prev = v
    return q
OUT = {}
for k in ('stx', 'wdc'):
    g = json.load(open(os.path.join(H, 'raw', f'{k}_facts.json')))['facts']['us-gaap']
    rev = quarterly(series(g, 'RevenueFromContractWithCustomerExcludingAssessedTax'))
    if k == 'stx':
        cogs = quarterly(series(g, 'CostOfGoodsAndServicesSold'))
        gp = {e: rev[e] - cogs[e] for e in rev if e in cogs}
    else:
        gp = quarterly(series(g, 'GrossProfit'))
    inv = {x['end']: x['val'] for x in g['InventoryNet']['units']['USD']}
    cap = capex_q(series(g, 'PaymentsToAcquirePropertyPlantAndEquipment'))
    rows = []
    for e in sorted(rev):
        if e < '2018-01-01': continue
        r = rev[e]
        rows.append(dict(end=e, rev=round(r / 1e6), gm=round(gp[e] / r * 100, 1) if e in gp else None,
                         inv=round(inv[e] / 1e6) if e in inv else None, capex=round(cap[e] / 1e6) if e in cap else None))
    OUT[k] = rows
json.dump(OUT, open(os.path.join(H, 'quarterly.json'), 'w'), indent=0)
for k in OUT:
    print(k, len(OUT[k]))
    for r in OUT[k]: print(' ', r)
