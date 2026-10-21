"""铜页数据抓取（需联网，不在 build.sh 里）：LME（Westmetall 公开表）、SHFE 仓单与主连（Tushare，经 /workspace/daily_report/tsq.py，token 不进仓库）、
FRED 月度铜价与 CPI。原始文件放 cu_data/raw/（.gitignore），只把整理后的月度序列写到 cu_data/series.json。"""
import json, os, re, sys, time, glob, io, urllib.request
import pandas as pd
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(R0, 'cu_data', 'raw'); os.makedirs(RAW, exist_ok=True)

def lme():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, 'wm_cu_20*.html'))):
        h = open(f, encoding='utf-8', errors='ignore').read()
        for d, c, t, s in re.findall(r'<tr>\s*<td >(\d{2}\. \w+ \d{4})</td>\s*<td >([\d,\.\-]+)</td>\s*<td >([\d,\.\-]+)</td>\s*<td class="last">([\d,\.\-]+)</td>', h):
            try:
                rows.append((pd.to_datetime(d, format='%d. %B %Y'), float(c.replace(',', '')), float(t.replace(',', '')), float(s.replace(',', ''))))
            except ValueError:
                pass
    df = pd.DataFrame(rows, columns=['d', 'cash', 'm3', 'stock']).drop_duplicates('d').sort_values('d').set_index('d')
    return df

def shfe():
    sys.path.insert(0, '/workspace/daily_report'); from tsq import q
    cache = os.path.join(RAW, 'shfe_wsr.csv')
    old = pd.read_csv(cache, dtype={'d': str}) if os.path.exists(cache) else pd.DataFrame(columns=['d', 'wsr'])
    have = set(old['d'])
    cal = q('trade_cal', exchange='SHFE', start_date='20080101', end_date='20261021', is_open='1')
    cal['m'] = cal['cal_date'].str[:6]
    ends = sorted(cal.groupby('m')['cal_date'].max())
    out = old.to_dict('records')
    for d in ends:
        if d in have: continue
        w = q('fut_wsr', trade_date=d, symbol='CU')
        w = w[w['fut_name'].fillna('').str.strip() == '铜'] if 'fut_name' in w else w
        out.append(dict(d=d, wsr=float(pd.to_numeric(w['vol'], errors='coerce').sum())))
        time.sleep(0.35)
    o = pd.DataFrame(out).sort_values('d'); o.to_csv(cache, index=False)
    px = os.path.join(RAW, 'shfe_cu.csv')
    if not os.path.exists(px):
        fr = []
        for a, b in [('20080101', '20131231'), ('20140101', '20191231'), ('20200101', '20261021')]:
            fr.append(q('fut_daily', ts_code='CU.SHF', start_date=a, end_date=b, fields='trade_date,close,settle,oi')); time.sleep(0.5)
        pd.concat(fr).sort_values('trade_date').to_csv(px, index=False)
    return o, pd.read_csv(px, dtype={'trade_date': str})

def fred(sid):
    f = os.path.join(RAW, f'fred_{sid}.csv')
    if not os.path.exists(f):
        urllib.request.urlretrieve(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}', f)
    d = pd.read_csv(f); d.columns = ['d', 'v']; d['d'] = pd.to_datetime(d['d']); d['v'] = pd.to_numeric(d['v'], errors='coerce')
    return d.set_index('d')['v']

if __name__ == '__main__':
    L = lme(); print('LME', L.index.min(), L.index.max(), len(L))
    W, P = shfe(); print('SHFE wsr', W.head(2).to_dict('records'), W.tail(2).to_dict('records'), len(P))
    for s in ['CPIAUCSL', 'PCOPPUSDM', 'DFII10', 'DTWEXBGS']:
        x = fred(s); print(s, x.index.max(), x.iloc[-1])
