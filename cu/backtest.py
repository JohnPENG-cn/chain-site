"""铜页回测（需先跑 cu/fetch.py 下载原始数据；不在 build.sh 里）。输出 cu_data/backtest.json（只含整理后的月度序列与统计量，不含原始网页）。
1) 库存天数 → 实际铜价：LME 库存 ÷ 全球精炼铜消费（ICSG 年度）换算成"可用天数"，对数回归实际 LME 现货价（CPI 平减到 2026-09 美元）。
   2008-01 至 2018-12 拟合，2019-01 起样本外检验。
2) 方向命中率：过去 3 个月 LME 库存天数下降 → 未来 3 个月铜价上涨？
3) 中国信贷脉冲 → 铜价同比：交叉相关（领先 k 个月）。"""
import json, os, sys, pickle
import numpy as np, pandas as pd
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R0, 'cu'))
import fetch as F
import warnings; warnings.filterwarnings("ignore")

USE = {2008: 17877, 2009: 17889, 2010: 19130, 2011: 19704, 2012: 20468, 2013: 21401, 2014: 22908, 2015: 23057, 2016: 23487, 2017: 23705,
       2018: 24484, 2019: 24427, 2020: 24963, 2021: 25264, 2022: 25857, 2023: 26642, 2024: 27420, 2025: 28200, 2026: 28590}   # ICSG（2026 = 10 月预测）

L = F.lme()
m = L.resample('MS').mean()
cpi = F.fred('CPIAUCSL').resample('MS').mean()
cpi = cpi.reindex(m.index).ffill()
m['real'] = m['cash'] * cpi.iloc[-1] / cpi            # 2026-09（最新 CPI）美元
m['use_d'] = [USE[d.year] / 365 for d in m.index]      # 千吨/天
m['days'] = m['stock'] / 1000 / m['use_d']
m = m.dropna()
x, y = np.log(m['days']), np.log(m['real'])
tr = m.index <= '2018-12-01'
b, a = np.polyfit(x[tr], y[tr], 1)
pred = a + b * x
res = y - pred
r2_in = 1 - ((y[tr] - pred[tr]) ** 2).sum() / ((y[tr] - y[tr].mean()) ** 2).sum()
te = ~tr
r2_out = 1 - ((y[te] - pred[te]) ** 2).sum() / ((y[te] - y[te].mean()) ** 2).sum()
# 全样本再拟合一次（给 2027 情景用）
B, A = np.polyfit(x, y, 1)
resid_full = y - (A + B * x)
sd_full = float(resid_full.std())
# 方向命中率：库存天数 3 个月变化 < 0 → 未来 3 个月实际价格上涨
d3 = m['days'].diff(3)
f3 = np.log(m['real']).shift(-3) - np.log(m['real'])
ok = (~d3.isna()) & (~f3.isna())
sig = d3[ok] < 0
hit = float(((sig & (f3[ok] > 0)) | (~sig & (f3[ok] <= 0))).mean())
base_up = float((f3[ok] > 0).mean())
hit_te = None
ok2 = ok & (m.index >= '2019-01-01')
s2 = d3[ok2] < 0
hit_te = float(((s2 & (f3[ok2] > 0)) | (~s2 & (f3[ok2] <= 0))).mean())
# 价格残差的均值回归：残差 > +1σ 之后 12 个月价格涨跌
f12 = np.log(m['real']).shift(-12) - np.log(m['real'])
hi = (resid_full > sd_full) & (~f12.isna())
lo = (resid_full < -sd_full) & (~f12.isna())
mr = dict(hi_n=int(hi.sum()), hi_med=float(f12[hi].median()) if hi.sum() else None, hi_down=float((f12[hi] < 0).mean()) if hi.sum() else None,
          lo_n=int(lo.sum()), lo_med=float(f12[lo].median()) if lo.sum() else None, lo_up=float((f12[lo] > 0).mean()) if lo.sum() else None)
# 中国信贷脉冲（社融 12 个月新增的同比变化 / 名义 GDP 4 季合计），同 world_indicators 算法
tk = pickle.load(open('/workspace/world_indicators/cache/tushare.pkl', 'rb'))['data']
fl, g = tk['TSF_FLOW'], tk['GDP_CUM']
gq = g - g.groupby(g.index.year).shift(1).fillna(0); g4 = gq.rolling(4).sum().dropna()
f12s = fl.rolling(12).sum(); imp = (f12s - f12s.shift(12)).dropna()
imp = (imp / g4.reindex(imp.index, method='ffill') * 100).dropna()
imp.index = pd.to_datetime(imp.index).to_period('M').to_timestamp()
yoy = (np.log(m['cash']) - np.log(m['cash'].shift(12))) * 100
xc = {}
for k in range(0, 19, 3):
    s = pd.concat([imp.shift(k), yoy], axis=1).dropna()
    xc[k] = round(float(s.corr().iloc[0, 1]), 3) if len(s) > 24 else None
kbest = max((k for k in xc if xc[k] is not None), key=lambda k: xc[k])
nimp = int(len(pd.concat([imp.shift(kbest), yoy], axis=1).dropna()))

# ---- 4) 长序列实际价格（FRED 1992 起 + 2026-08 起用 LME 月均补齐）与估值 z 分数（滚动 10 年，无前视）

fp = F.fred('PCOPPUSDM').resample('MS').mean(); px = pd.concat([fp, m['cash'][m.index > fp.index[-1]]])
c2 = F.fred('CPIAUCSL').resample('MS').mean().reindex(px.index).ffill()
lreal = px * c2.iloc[-1] / c2
lr = np.log(lreal); mu = lr.rolling(120).mean().shift(1); sdv = lr.rolling(120).std().shift(1); z = (lr - mu) / sdv
f12l = lr.shift(-12) - lr
zt = {}
for t in (1.0, 1.5, 2.0):
    k = (z > t) & f12l.notna()
    zt[str(t)] = dict(n=int(k.sum()), med=round(float(f12l[k].median()), 3), down=round(float((f12l[k] < 0).mean()), 3), yrs=sorted({int(d.year) for d in z[k].index}))
kk = f12l.notna() & z.notna(); zt['all_down'] = round(float((f12l[kk] < 0).mean()), 3); zt['n'] = int(kk.sum()); zt['now'] = round(float(z.iloc[-1]), 2)
prior = lreal[:-12]; zt['peak_prior'] = [f"{prior.idxmax():%Y-%m}", round(float(prior.max()))]
# ---- 5) 信贷脉冲样本外：2014–2020 拟合，2021 起检验
yoy_l = (np.log(px) - np.log(px.shift(12))) * 100
dd = pd.concat([imp.shift(kbest), yoy_l], axis=1, keys=['i', 'y'], sort=True).dropna()
trm = dd.index <= '2020-12-01'; bb, aa = np.polyfit(dd.i[trm], dd.y[trm], 1); pr = aa + bb * dd.i
Bf, Af = np.polyfit(dd.i, dd.y, 1)
rmse = float(np.sqrt(((dd.y - (Af + Bf * dd.i)) ** 2).mean()))
ci = dict(rmse=round(rmse, 1), a=round(float(aa), 2), b=round(float(bb), 2), r_in=round(float(np.corrcoef(dd.i[trm], dd.y[trm])[0, 1]), 3), r_out=round(float(np.corrcoef(pr[~trm], dd.y[~trm])[0, 1]), 3),
          sign_out=round(float((np.sign(pr[~trm]) == np.sign(dd.y[~trm])).mean()), 3), n_out=int((~trm).sum()), n=int(len(dd)), A=round(float(Af), 2), B=round(float(Bf), 2),
          pred=round(float(Af + Bf * imp.iloc[-1]), 1), pred_m=f"{(imp.index[-1] + pd.DateOffset(months=kbest)):%Y-%m}",
          base_px=round(float(px[(imp.index[-1] + pd.DateOffset(months=kbest)) - pd.DateOffset(months=12)])))
# ---- 6) COMEX 相对 LME 溢价（月末：COMEX 近月收盘 vs LME 现货月末）
hg = json.load(open(os.path.join(R0, 'cu_data', 'raw', 'yahoo_hg_mo.json')))['chart']['result'][0]
hs = pd.Series(hg['indicators']['quote'][0]['close'], index=pd.to_datetime(hg['timestamp'], unit='s')).dropna()
hs.index = hs.index.to_period('M').to_timestamp(); hs = hs.groupby(level=0).last() * 2204.62
le = L['cash'].resample('MS').last()
spr = ((hs / le - 1) * 100).dropna(); spr = spr[spr.index >= '2008-01-01']
# ---- 7) 实际利率、美元（月均）
ry = F.fred('DFII10').resample('MS').mean(); usd = F.fred('DTWEXBGS').resample('MS').mean()
shf = pd.read_csv(os.path.join(R0, 'cu_data', 'raw', 'shfe_wsr.csv')); shf.index = pd.to_datetime(shf.d.astype(str)).dt.to_period('M').dt.to_timestamp(); shf = shf.wsr
last = m.iloc[-1]
out = dict(
    fit=dict(a=round(float(a), 4), b=round(float(b), 4), r2_in=round(float(r2_in), 3), r2_out=round(float(r2_out), 3), A=round(float(A), 4), B=round(float(B), 4), sd=round(sd_full, 4),
             n=int(len(m)), train='2008-01–2018-12', test=f"2019-01–{m.index[-1]:%Y-%m}"),
    hit=dict(all=round(hit, 3), test=round(hit_te, 3), base_up=round(base_up, 3), n=int(ok.sum())), mr={k: (round(v, 3) if isinstance(v, float) else v) for k, v in mr.items()},
    xc=xc, kbest=kbest, nimp=nimp, imp_last=[f"{imp.index[-1]:%Y-%m}", round(float(imp.iloc[-1]), 2)],
    now=dict(m=f"{m.index[-1]:%Y-%m}", cash=round(float(last['cash'])), real=round(float(last['real'])), stock=round(float(last['stock'])), days=round(float(last['days']), 2),
             fair=round(float(np.exp(A + B * np.log(last['days'])))), resid=round(float(resid_full.iloc[-1]), 3), pct_days=round(float((m['days'] < last['days']).mean() * 100), 1)),
    series=[[f"{d:%Y-%m}", round(float(r.cash)), round(float(r.real)), round(float(r.stock)), round(float(r.days), 2), round(float(np.exp(A + B * np.log(r.days))))] for d, r in m.iterrows()],
    imp=[[f"{d:%Y-%m}", round(float(v), 2)] for d, v in imp.items() if d >= pd.Timestamp('2014-01-01')],
    yoy=[[f"{d:%Y-%m}", round(float(v), 1)] for d, v in yoy_l.items() if d >= pd.Timestamp('2014-01-01') and not np.isnan(v)],
    z=zt, ci=ci, long=[[f"{d:%Y-%m}", round(float(v))] for d, v in lreal.items()],
    spread=[[f"{d:%Y-%m}", round(float(v), 2)] for d, v in spr.items()],
    macro=[[f"{d:%Y-%m}", (round(float(ry.get(d)), 2) if d in ry.index and not np.isnan(ry.get(d)) else None), (round(float(usd.get(d)), 1) if d in usd.index and not np.isnan(usd.get(d)) else None),
            (int(shf.get(d)) if d in shf.index and shf.get(d) > 0 else None)] for d in m.index],
    use=USE)
json.dump(out, open(os.path.join(R0, 'cu_data', 'backtest.json'), 'w'), ensure_ascii=False, indent=0)
print(json.dumps({k: v for k, v in out.items() if k not in ('series', 'imp', 'use', 'yoy', 'long', 'spread', 'macro')}, ensure_ascii=False, indent=1))
