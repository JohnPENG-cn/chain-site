"""把 HDD 节点补进 data/chains.json、data/layers.json（不重跑全站行情，只算这一个节点）。
口径与 build_data.py 完全一致：同一组交易日（以 chains.json 的 date 为最后一天，往前 22 个交易日），
同样的涨跌幅、市值、主力净流入、财务（毛利率 / 存货周转天数 / 合同负债）与信号打分。
Tushare token 由 /workspace/daily_report/common.py 从 ~/.config/tushare/token 读取，从不打印、不写出。
以后整站重跑 build_data.py 时，CH / KW 里已有同一节点，会被正常覆盖。"""
import json, os, statistics as stt, sys
sys.path.insert(0, '/workspace/daily_report')
from common import pro
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_NAME, LVL, ND = 'AI算力', '上游', 'HDD硬盘'
STOCKS = {'000021.SZ': '深科技', '600366.SH': '宁波韵升', '300433.SZ': '蓝思科技'}   # 与 build_data.py CH 保持一致
KW = ['硬盘', 'HDD', '希捷', '西部数据', 'HAMR', '磁头', '盘基片']                     # 与 build_data.py KW 保持一致
P = pro()
q = lambda api, **kw: P.query(api, **kw)

cj = json.load(open(f'{ROOT}/data/chains.json'))
last = cj['date']
cal = q('trade_cal', exchange='SSE', start_date='20260701', end_date=last, is_open='1').sort_values('cal_date')
dates = list(cal.cal_date)[-22:]
px = {}
for d in dates:
    df = q('daily', trade_date=d, fields='ts_code,close,pct_chg,amount')
    if len(df): px[d] = df[df.ts_code.isin(STOCKS)].set_index('ts_code')
dates = sorted(px)
assert dates[-1] == last, (dates[-1], last)


def ret(c, k):
    try: return round((px[last].close[c] / px[dates[-1 - k]].close[c] - 1) * 100, 2)
    except Exception: return None


db = q('daily_basic', trade_date=last, fields='ts_code,total_mv').set_index('ts_code').total_mv
mf = q('moneyflow', trade_date=last).set_index('ts_code')
mf = (mf.buy_lg_amount + mf.buy_elg_amount - mf.sell_lg_amount - mf.sell_elg_amount) / 1e4
st = [{'code': c, 'name': n, 'close': float(px[last].close.get(c, float('nan'))), 'd1': ret(c, 1), 'd5': ret(c, 5), 'd20': ret(c, 20),
       'mv': round(float(db.get(c, 0) or 0) / 1e4, 1), 'mf': round(float(mf.get(c)), 2) if c in mf.index else None} for c, n in STOCKS.items()]
avg = lambda k: round(sum(x[k] for x in st if x[k] is not None) / max(1, sum(x[k] is not None for x in st)), 2)
nj = json.load(open(f'{ROOT}/data/news.json'))
nn = 0
for it in nj['items']:
    if any(k.lower() in it['title'].lower() for k in KW):
        tg = [tuple(t) for t in it['tags']]
        if (CH_NAME, ND) not in tg: it['tags'] = it['tags'] + [[CH_NAME, ND]]
        nn += 1
node = {'level': LVL, 'node': ND, 'stocks': st, 'd1': avg('d1'), 'd5': avg('d5'), 'd20': avg('d20'),
        'mf': round(sum(x['mf'] or 0 for x in st), 2), 'news': nn}
arr = [x for x in cj['chains'][CH_NAME] if x['node'] != ND]
i = max(k for k, x in enumerate(arr) if x['level'] == '上游') + 1      # 放在上游最后（HBM存储 后面）
arr.insert(i, node)
cj['chains'][CH_NAME] = arr

# ---- 财务层（同 build_data.py v2）
fin = {}
for c in STOCKS:
    fi = q('fina_indicator', ts_code=c, fields='end_date,grossprofit_margin,invturn_days').drop_duplicates('end_date').sort_values('end_date').tail(9)
    bs = q('balancesheet', ts_code=c, fields='end_date,contract_liab,adv_receipts').drop_duplicates('end_date').sort_values('end_date').tail(5)
    fi = fi[fi.end_date <= last]; bs = bs[bs.end_date <= last]
    fin[c] = {'gm': fi[['end_date', 'grossprofit_margin']].dropna().values.tolist(), 'inv': fi[['end_date', 'invturn_days']].dropna().values.tolist(),
              'cl': [[a, (b if b == b and b is not None else 0) + (d if d == d and d is not None else 0)] for a, b, d in bs.values]}


def med(xs): xs = [x for x in xs if x is not None]; return round(stt.median(xs), 2) if xs else None


def chg(series, lag=4):
    if len(series) > lag and series[-1 - lag][1]: return series[-1][1] - series[-1 - lag][1], series[-1][0]
    return None, None


cs = list(fin)
qs = sorted({e for c in cs for e, _ in fin[c]['gm']})[-8:]
gm_series = [[e, med([dict(map(tuple, fin[c]['gm'])).get(e) for c in cs])] for e in qs]
gmc = med([chg(fin[c]['gm'])[0] for c in cs]); invc = med([chg(fin[c]['inv'])[0] for c in cs])
clg = med([(fin[c]['cl'][-1][1] / fin[c]['cl'][0][1] - 1) * 100 if len(fin[c]['cl']) == 5 and fin[c]['cl'][0][1] else None for c in cs])
score = 0; why = []
if gmc is not None: score += int(gmc > 0.5) - int(gmc < -0.5); why.append(f"毛利率同比{gmc:+.1f}pct")
if invc is not None: score += (invc < -5) - (invc > 5); why.append(f"存货周转天数同比{invc:+.0f}天")
if clg is not None: score += int(clg > 10) - int(clg < -10); why.append(f"合同负债同比{clg:+.0f}%")
sig = '改善' if score >= 2 else '恶化' if score <= -1 else '中性'
d20 = node['d20']
flag = '产业变好但股价未动' if sig == '改善' and (d20 is None or d20 < 3) else '股价跑在基本面前' if sig != '改善' and d20 is not None and d20 > 10 else ('基本面走弱、股价同步走弱' if sig == '恶化' and d20 is not None and d20 < 0 else '大致同步')
L = json.load(open(f'{ROOT}/data/layers.json'))
L['nodes'][f'{CH_NAME}|{ND}'] = {'gm': gm_series, 'gm_chg': gmc, 'inv_chg': invc, 'cl_yoy': clg, 'report': max(qs) if qs else None, 'score': int(score),
                                 'signal': sig, 'why': why, 'd20': d20, 'mf': node['mf'], 'flag': flag}
# 一句话判断按 build_data.py 同一规则重算（key 不变）
ns = {k.split('|')[1]: v for k, v in L['nodes'].items() if k.startswith(CH_NAME + '|')}
imp = [k for k, v in ns.items() if v['signal'] == '改善']; bad = [k for k, v in ns.items() if v['signal'] == '恶化']
gap = [k for k, v in ns.items() if v['flag'] == '产业变好但股价未动']; run = [k for k, v in ns.items() if v['flag'] == '股价跑在基本面前']
tone_ = '产业端偏强' if len(imp) > len(bad) else '产业端偏弱' if len(bad) > len(imp) else '产业端分化'
px_ = '但近20日股价多数下跌' if sum((v['d20'] or 0) < 0 for v in ns.values()) > len(ns) / 2 else '股价多数上涨'
s_ = f"{tone_}，{px_}：{len(ns)}个节点中{len(imp)}个改善、{len(bad)}个恶化。"
if gap: s_ += f"「产业变好但股价未动」：{'、'.join(gap)}。"
if run: s_ += f"「股价跑在基本面前」：{'、'.join(run)}。"
L['summary'][CH_NAME]['line'] = s_


def dump(n, o): json.dump(o, open(f'{ROOT}/data/{n}.json', 'w'), ensure_ascii=False, default=str)


dump('chains', cj); dump('layers', L); dump('news', nj)
print('HDD 节点', last, json.dumps(node, ensure_ascii=False))
print('layers', json.dumps(L['nodes'][f'{CH_NAME}|{ND}'], ensure_ascii=False))
print('summary', s_)
