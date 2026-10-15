import csv,json,datetime as dt,numpy as np
R='/workspace/chain_site/hbm_data/raw/'
ex={};mem={}
for r in csv.DictReader(open(R+'motie.csv',encoding='utf-8-sig')):
    ex[r['년월']]=float(r['반도체(억불)']);mem[r['년월']]=float(r['메모리(억불)'])
# 2026 from MOTIE press release 2026-09-07 (Jan-Aug, rounded) + Sedaily/MOTIE Sep prelim
for m,v in zip(range(1,10),[207,253,330,320,373,449,412,468,603]): ex[f'2026-{m:02d}']=v
mem['2026-05']=321.4;mem['2026-09']=540.7
months=sorted(ex)
def add(m,k):
    y,mo=map(int,m.split('-'));t=y*12+mo-1+k;return f'{t//12}-{t%12+1:02d}'
def s3(m,d=ex):
    ks=[add(m,-i) for i in range(3)];return sum(d[k] for k in ks) if all(k in d for k in ks) else None
def yoy3(m,d=ex):
    a,b=s3(m,d),s3(add(m,-12),d);return a/b-1 if a and b else None
mu={k:v for k,v in json.load(open(R+'mu_q.json')).items()}
# map micron fiscal quarter end to calendar month (end date -> month, if day<10 use previous month)
muq={}
for k,v in mu.items():
    d=dt.date.fromisoformat(k);m=(d.replace(day=1)-dt.timedelta(days=1)) if d.day<10 else d
    muq[f'{m.year}-{m.month:02d}']=v
mk=sorted(muq)
muy={m:muq[m]/muq[add(m,-12)]-1 for m in mk if add(m,-12) in muq}
hx={'2021-09':11805324,'2021-12':12376609,'2022-03':12155653,'2022-06':13811001,'2022-09':10982883,'2022-12':7672031,'2023-03':5088111,'2023-06':7305932,'2023-09':9066171,'2023-12':11305505,'2024-03':12429598,'2024-06':16423258,'2024-09':17573069,'2024-12':19767035,'2025-03':17639141,'2025-06':22231952,'2025-09':24448929,'2025-12':32826653,'2026-03':52576287,'2026-06':79318746}
hxy={'2021-09':.4523,'2021-12':.5536}
hxy.update({m:hx[m]/hx[add(m,-12)]-1 for m in hx if add(m,-12) in hx})
def xc(target,lo=-3,hi=9,start='2015-12'):
    out={}
    for k in range(lo,hi+1):  # export leads by k months
        a=[];b=[]
        for m,v in target.items():
            if m<start: continue
            e=yoy3(add(m,-k))
            if e is not None: a.append(e);b.append(v)
        out[k]=(round(float(np.corrcoef(a,b)[0,1]),3),len(a))
    return out
res={'micron':xc(muy),'hynix':xc(hxy)}
print(json.dumps(res))
# monthly yoy series for chart
ser=[{'m':m,'ex':ex[m],'y3':(round(yoy3(m)*100,1) if yoy3(m) is not None else None),'mem':mem.get(m)} for m in months if m>='2015-01']
# turning points: local peaks of y3 (max within +-6 months, y3>20%)
y={s['m']:s['y3'] for s in ser if s['y3'] is not None}
pk=[m for m in y if all(y[m]>=y.get(add(m,i),-1e9) for i in range(-6,7) if i) and y[m]>15]
tr=[m for m in y if all(y[m]<=y.get(add(m,i),1e9) for i in range(-6,7) if i) and y[m]<0]
mpk=[m for m in muy if all(muy[m]>=muy.get(add(m,i*3),-1e9) for i in (-2,-1,1,2)) and muy[m]>0.2]
mtr=[m for m in muy if all(muy[m]<=muy.get(add(m,i*3),1e9) for i in (-2,-1,1,2)) and muy[m]<0]
print('export peaks',pk,'troughs',tr);print('mu peaks',mpk,'troughs',mtr)
json.dump({'xcorr':res,'export':ser,'micron':[{'m':m,'rev':round(muq[m]/1e9,3),'yoy':round(muy[m]*100,1) if m in muy else None} for m in mk if m>='2015-01'],
 'hynix':[{'m':m,'rev':round(hx[m]/1e6,2),'yoy':round(hxy[m]*100,1) if m in hxy else None} for m in sorted(hx)],'peaks':{'export':pk,'export_tr':tr,'mu':mpk,'mu_tr':mtr}},open('/workspace/chain_site/hbm_data/backtest.json','w'),ensure_ascii=False)
