import json,pandas as pd,numpy as np
R='/workspace/chain_site/cowos_data/raw/'
def load(s):
    d=json.load(open(R+f'rev_{s}.json'))['data']
    df=pd.DataFrame(d);df['m']=pd.to_datetime(dict(year=df.revenue_year,month=df.revenue_month,day=1))
    return df.set_index('m')['revenue'].astype(float).replace(0,np.nan).sort_index()
S={s:load(s) for s in ['3131','3583','6187','6640','3711','2330','3037','8046','3189','2449','6510','3443']}
idx=pd.date_range('2012-01-01','2026-09-01',freq='MS')
df=pd.DataFrame({k:v.reindex(idx) for k,v in S.items()})
df['equip']=df[['3131','3583','6187']].sum(axis=1,min_count=3)
df['abf']=df[['3037','8046','3189']].sum(axis=1,min_count=3)
def y3(x):  # 3M rolling sum yoy %
    r=x.rolling(3).sum();return (r/r.shift(12)-1)*100
Y={k:y3(df[k]) for k in ['equip','2330','3711','abf','2449','6640','3131','3583','6187']}
Y=pd.DataFrame(Y)
out={}
def xc(a,b,lags=range(-12,13)):
    res={}
    for k in lags:
        z=pd.concat([Y[a].shift(k),Y[b]],axis=1).dropna()
        z=z[z.index>='2014-01-01']
        res[k]=[round(z.corr().iloc[0,1],3),len(z)]
    return res
out['xc_equip_tsmc']=xc('equip','2330');out['xc_equip_ase']=xc('equip','3711');out['xc_abf_tsmc']=xc('abf','2330')
for k,v in out.items():
    best=max(v.items(),key=lambda t:t[1][0]);print(k,'best lag',best, {l:v[l][0] for l in [-6,-3,0,3,6,9,12]})
# annual revenue (NT$bn) for equipment trio and capacity increments
A=df[['3131','3583','6187','6640','3711','2330','abf']].groupby(df.index.year).sum()/1e9
print(A.round(1).tail(8))
cap={2022:8,2023:13,2024:34,2025:72,2026:120,2027:185}  # TSMC end-year, KGI
# turning points of equip y3 (local maxima ±6m)
e=Y['equip'].dropna();e=e[e.index>='2014-01-01']
pk=[d for i,d in enumerate(e.index) if 6<=i<len(e)-6 and e.iloc[i]==e.iloc[i-6:i+7].max()]
tr=[d for i,d in enumerate(e.index) if 6<=i<len(e)-6 and e.iloc[i]==e.iloc[i-6:i+7].min()]
t=Y['2330'].dropna();t=t[t.index>='2014-01-01']
pk2=[d for i,d in enumerate(t.index) if 6<=i<len(t)-6 and t.iloc[i]==t.iloc[i-6:i+7].max()]
tr2=[d for i,d in enumerate(t.index) if 6<=i<len(t)-6 and t.iloc[i]==t.iloc[i-6:i+7].min()]
print('equip peaks',[d.strftime('%Y-%m') for d in pk],'troughs',[d.strftime('%Y-%m') for d in tr])
print('tsmc peaks',[d.strftime('%Y-%m') for d in pk2],'troughs',[d.strftime('%Y-%m') for d in tr2])
print(Y.tail(12).round(0))
ser=lambda s:[[d.strftime('%Y-%m'),None if pd.isna(v) else round(v,1)] for d,v in s.items() if d>=pd.Timestamp('2014-01-01')]
out['series']={k:ser(Y[k]) for k in ['equip','2330','3711','abf']}
out['annual']={c:{int(y):round(v,1) for y,v in A[c].items() if y>=2016} for c in A.columns}
out['monthly_last']={k:[[d.strftime('%Y-%m'),round(v/1e8,2)] for d,v in df[k].dropna().items() if d>=pd.Timestamp('2024-01-01')] for k in ['3131','3583','6187','6640','3711','2330']}
out['peaks']={'equip':[d.strftime('%Y-%m') for d in pk],'equip_tr':[d.strftime('%Y-%m') for d in tr],'tsmc':[d.strftime('%Y-%m') for d in pk2],'tsmc_tr':[d.strftime('%Y-%m') for d in tr2]}
json.dump(out,open('/workspace/chain_site/cowos_data/backtest.json','w'),ensure_ascii=False)
