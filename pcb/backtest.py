"""PCB 链领先指标回测 + 毛利率（台股 MOPS，经 FinMind API）。原始下载在 pcb_data/raw/（不进仓库），输出 pcb_data/backtest.json、margins.json。
方法与 CoWoS 页相同（SOP 第 10 步）：3 个月滚动合计同比；交叉相关 k=−12…+12；±6 个月局部极值配对拐点。
运行：python3 pcb/backtest.py（需要网络时会自动下载缺的原始文件）。"""
import json, os, subprocess, pandas as pd, numpy as np
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(R0, 'pcb_data', 'raw'); os.makedirs(RAW, exist_ok=True)
API = 'https://api.finmindtrade.com/api/v4/data?dataset={}&data_id={}&start_date={}'
def get(ds, sid, start, fn):
    p = os.path.join(RAW, fn)
    if not os.path.exists(p):
        subprocess.run(['curl', '-s', API.format(ds, sid, start), '-o', p], check=True)
    return json.load(open(p))['data']
END = '2026-09-01'
def rev(s):
    df = pd.DataFrame(get('TaiwanStockMonthRevenue', s, '2012-01-01', f'rev_{s}.json'))
    df['m'] = pd.to_datetime(dict(year=df.revenue_year, month=df.revenue_month, day=1))
    return df.set_index('m')['revenue'].astype(float).replace(0, np.nan).sort_index()
IDS = ['2383', '6274', '6213', '2368', '8358', '1815', '8021', '2330']
idx = pd.date_range('2013-01-01', END, freq='MS')
df = pd.DataFrame({s: rev(s).reindex(idx) for s in IDS})
df['ccl'] = df[['2383', '6274', '6213']].sum(axis=1, min_count=3)      # CCL 三家：台光电 + 台燿 + 联茂
df['mat'] = df[['8358', '1815', '8021']].sum(axis=1, min_count=3)      # 上游材料三家：金居（铜箔）+ 富乔（玻纤布）+ 尖点（钻针）
def y3(x):
    r = x.rolling(3).sum(); return (r / r.shift(12) - 1) * 100
Y = pd.DataFrame({k: y3(df[k]) for k in ['ccl', 'mat', '2368', '2330', '8358', '1815', '8021', '2383']})
def xc(a, b):
    o = {}
    for k in range(-12, 13):
        z = pd.concat([Y[a].shift(k), Y[b]], axis=1).dropna(); z = z[z.index >= '2015-01-01']
        o[k] = [round(z.corr().iloc[0, 1], 3), len(z)]
    return o
out = {'xc': {'材料→CCL': xc('mat', 'ccl'), 'CCL→金像电': xc('ccl', '2368'), '台积电→CCL': xc('2330', 'ccl')}}
def turns(s, kind):
    s = s.dropna(); s = s[s.index >= '2015-01-01']; f = max if kind == 'pk' else min
    return [d for i, d in enumerate(s.index) if 6 <= i < len(s) - 6 and s.iloc[i] == f(s.iloc[i - 6:i + 7])]
def pair(a, b):   # A 的每个拐点配 B 之后（−3…+18 个月内）最近的同类拐点
    rows = []
    for kind, lab in (('pk', '见顶'), ('tr', '见底')):
        tb = turns(Y[b], kind)
        for d in turns(Y[a], kind):
            c = [x for x in tb if -3 <= (x.year - d.year) * 12 + x.month - d.month <= 18]
            if c:
                x = min(c, key=lambda x: abs((x.year - d.year) * 12 + x.month - d.month))
                rows.append([d.strftime('%Y-%m') + ' ' + lab, x.strftime('%Y-%m'), (x.year - d.year) * 12 + x.month - d.month])
            else:
                rows.append([d.strftime('%Y-%m') + ' ' + lab, '—', None])
    return sorted(rows)
out['tp'] = {'材料→CCL': pair('mat', 'ccl'), 'CCL→金像电': pair('ccl', '2368')}
ser = lambda s: [[d.strftime('%Y-%m'), None if pd.isna(v) else round(v, 1)] for d, v in s.items() if d >= pd.Timestamp('2015-01-01')]
out['series'] = {k: ser(Y[k]) for k in ['ccl', 'mat', '2368', '2330']}
out['now'] = {k: round(float(Y[k].dropna().iloc[-1]), 1) for k in Y.columns}
out['now_m'] = Y.dropna(how='all').index[-1].strftime('%Y-%m')
out['n'] = int(Y[['mat', 'ccl']].dropna().query('index>="2015-01-01"').shape[0])
json.dump(out, open(os.path.join(R0, 'pcb_data', 'backtest.json'), 'w'), ensure_ascii=False)
# 毛利率（季度）：营收（亿新台币）、毛利率、营业利益率
M = {}
for s in ['2383', '6274', '6213', '2368', '8358', '1815', '8021']:
    d = pd.DataFrame(get('TaiwanStockFinancialStatements', s, '2021-01-01', f'fs_{s}.json'))
    p = d.pivot_table(index='date', columns='type', values='value', aggfunc='first')
    M[s] = [[i, round(r.Revenue / 1e8, 1), round(r.GrossProfit / r.Revenue * 100, 1), round(r.OperatingIncome / r.Revenue * 100, 1)] for i, r in p.iterrows() if r.Revenue]
json.dump(M, open(os.path.join(R0, 'pcb_data', 'margins.json'), 'w'), ensure_ascii=False)
if __name__ == '__main__':
    for k, v in out['xc'].items():
        b = max(v.items(), key=lambda t: t[1][0]); print(k, '峰值 k=', b, {l: v[l][0] for l in (-3, 0, 3, 6, 9)})
    for k, v in out['tp'].items(): print(k, v)
    print('now', out['now_m'], out['now'], 'n', out['n'])
    for s, a in M.items(): print(s, a[-5:])
