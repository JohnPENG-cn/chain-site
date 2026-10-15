import json,pandas as pd,numpy as np
R='/workspace/chain_site/cowos_data/raw/'
rows=[]
for s in ['3131','3583','6187']:
    d=json.load(open(R+f'bs_{s}.json'))['data']
    for r in d:
        if r['type']=='CurrentContractLiabilities': rows.append((s,r['date'],r['value']))
cl=pd.DataFrame(rows,columns=['s','d','v']);cl['d']=pd.to_datetime(cl.d)
p=cl.pivot_table(index='d',columns='s',values='v');p=p.dropna();p['sum']=p.sum(axis=1)
print((p/1e8).round(1).tail(16))
# quarterly revenue
def q(s):
    d=pd.DataFrame(json.load(open(R+f'rev_{s}.json'))['data']);d['m']=pd.to_datetime(dict(year=d.revenue_year,month=d.revenue_month,day=1))
    x=d.set_index('m').revenue.astype(float);return x.resample('QE').sum()
Q=pd.DataFrame({s:q(s) for s in ['3131','3583','6187']});Q['sum']=Q.sum(axis=1)
P=p['sum'];P.index=P.index.to_period('Q').to_timestamp('Q').normalize()
Qs=Q['sum'];Qs.index=Qs.index.to_period('Q').to_timestamp('Q').normalize()
z=pd.concat([P.rename('cl'),Qs.rename('rev')],axis=1).dropna()
z['cl_y']=z.cl.pct_change(4)*100; z['rev_y']=z.rev.pct_change(4)*100
for k in range(0,7):
    w=pd.concat([z.cl_y.shift(k),z.rev_y],axis=1).dropna();print('CL leads rev by',k,'Q corr',round(w.corr().iloc[0,1],3),len(w))
z['ratio']=z.cl/z.rev
print((z[['cl','rev']]/1e8).round(1).assign(ratio=z.ratio.round(2),cl_y=z.cl_y.round(0),rev_y=z.rev_y.round(0)).tail(14))
json.dump({'q':[d.strftime('%Y-%m') for d in z.index],'cl':[round(v/1e8,2) for v in z.cl],'rev':[round(v/1e8,2) for v in z.rev],
 'xc':{k:round(pd.concat([z.cl_y.shift(k),z.rev_y],axis=1).dropna().corr().iloc[0,1],3) for k in range(0,7)},'n':int(len(z))},open('/workspace/chain_site/cowos_data/cl.json','w'))
