"""CoWoS 小链供需模型 v0.1 (2026-10-15, Kiko)
需求(片/年) = Σ 出货(百万颗) / 每片可封良品颗数(ppw)
供给(片/年) = Σ 月份产能(千片/月, 季末锚点线性插值) × 有效稼动率
HBM 接口:  隐含 HBM 需求(EB) = Σ 出货 × 每封装 HBM 容量(GB)
出货: KGI 2026-09-15 Figure 10 [源1]; CPU: KGI 正文/MS(经36Kr) [源1,5]; ppw: 估(锚点 H100≈28, B200≈16 [源9])
"""
import json, openpyxl
from openpyxl.styles import Font, PatternFill
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/tmp/wenkai.ttf'); FN=fm.FontProperties(fname='/tmp/wenkai.ttf').get_name()
plt.rcParams['font.family']=FN; plt.rcParams['axes.unicode_minus']=False
# (year, vendor, product, units_M, ppw, hbm_GB_per_pkg, pkg, src_units)
K='KGI Fig.10'
D=[
(2023,'英伟达','A100',1.450,30,80,'S',K),(2023,'AMD','MI250/MI300',0.168,18,128,'S',K),(2023,'其他GPU','Gaudi等',0.027,25,96,'S',K),
(2023,'谷歌TPU','TPU v4/v5',1.464,30,32,'S',K),(2023,'AWS','Trainium1/Inferentia2',0.495,30,32,'S',K),(2023,'其他ASIC','其他',0.300,30,32,'S',K),
(2024,'英伟达','A100',0.088,30,80,'S',K),(2024,'英伟达','H100/H200',3.218,28,90,'S',K),(2024,'英伟达','B200',0.532,14,192,'L',K),
(2024,'AMD','MI300X',0.490,18,192,'S',K),(2024,'其他GPU','Gaudi/其他',0.402,25,96,'S',K),
(2024,'谷歌TPU','TPU v5/v6',2.099,30,40,'S',K),(2024,'AWS','Trainium',1.225,25,64,'S',K),(2024,'其他ASIC','MTIA/Maia/其他',0.660,30,64,'S',K),
(2025,'英伟达','H100/H200/H20',0.522,28,110,'S',K),(2025,'英伟达','B200',2.873,15,192,'L',K),(2025,'英伟达','B300',1.915,13,288,'L',K),
(2025,'AMD','MI325/MI355',0.927,15,288,'S',K),(2025,'其他GPU','其他',0.516,25,96,'S',K),
(2025,'谷歌TPU','Trillium/Ironwood',2.527,22,128,'S',K),(2025,'AWS','Trainium2',1.600,22,96,'S',K),(2025,'其他ASIC','MTIA/Maia/其他',0.750,25,96,'S',K),
(2026,'英伟达','H100/H200/H20',0.943,25,120,'S',K),(2026,'英伟达','B200',1.128,14,192,'L',K),(2026,'英伟达','B300',4.514,12,288,'L',K),(2026,'英伟达','Rubin',1.950,9,288,'L',K),
(2026,'英伟达','Vera CPU',2.000,45,0,'R','KGI 正文'),
(2026,'AMD','MI355/MI450',1.152,11,320,'S',K),(2026,'其他GPU','其他',0.550,25,96,'S',K),
(2026,'谷歌TPU','Ironwood(v7)',4.020,20,192,'S',K),(2026,'AWS','Trainium2/3',2.428,24,120,'R',K),
(2026,'其他ASIC','MTIA/Maia/OpenAI/其他',1.084,22,150,'S',K),
(2027,'英伟达','B300',0.266,13,288,'L',K),(2027,'英伟达','Rubin',5.890,10,288,'L',K),(2027,'英伟达','Rubin Ultra',2.850,6,256,'L',K),
(2027,'英伟达','Vera CPU',6.000,45,0,'R','KGI 正文'),
(2027,'AMD','MI450/MI455',1.680,9,432,'S',K),(2027,'AMD','Venice CPU',4.750,25,0,'S','KGI 正文(4.5–5.0M)'),(2027,'其他GPU','其他',0.600,25,96,'S',K),
(2027,'谷歌TPU','v8i Sunfish + v8t Zebrafish',9.104,17,260,'S',K),(2027,'AWS','Trainium3',3.060,24,144,'R',K),
(2027,'其他ASIC','Maia/MTIA/OpenAI/其他',2.300,20,200,'S',K),
]
OTHER={2023:15,2024:30,2025:60,2026:90,2027:150}   # 千片: 交换芯片/FPGA/网络等, 估(MS 总量与自下而上之差)
UNCON={2027:190}   # 千片: KGI 称客户需求高于可供 (Broadcom 500k vs 380–390k; Trn3 3.5M vs 3.0M; Venice 6.0M vs 4.5–5.0M)
# 季末产能 千片/月  年末锚点
TS={2022:8,2023:13,2024:34,2025:72,2026:120,2027:185}   # KGI [源1]
NT={2022:0,2023:2,2024:5,2025:17,2026:35,2027:80}       # KGI 2.5D 合计 - TSMC [源1]
UT=0.95
def quarters():
    q=[];vt=[];vn=[]
    for y in range(2023,2028):
        for k in range(1,5):
            f=k/4;q.append(f'{y}Q{k}');vt.append(round(TS[y-1]+(TS[y]-TS[y-1])*f,1));vn.append(round(NT[y-1]+(NT[y]-NT[y-1])*f,1))
    return q,vt,vn
def annual_supply(y,ts=TS,nt=NT,ut=UT):
    # 月度线性插值, 年内 12 个月平均
    s=0
    for m in range(1,13):
        f=m/12; s+= (ts[y-1]+(ts[y]-ts[y-1])*f) + (nt[y-1]+(nt[y]-nt[y-1])*f)
    return s*ut   # 千片/年
def demand(y):
    w=sum(u/p*1000 for yy,_,_,u,p,*_ in D if yy==y)+OTHER[y]; return w
def hbm_need(y): return sum(u*g for yy,_,_,u,p,g,*_ in D if yy==y)/1000  # EB
res={}
for y in range(2023,2028):
    d=demand(y); s=annual_supply(y); res[y]=dict(d=round(d),s=round(s),gap=round((s-d)/d*100,1),hbm=round(hbm_need(y),2),
        units=round(sum(u for yy,_,_,u,*_ in D if yy==y),2),acc_units=round(sum(u for yy,_,pr,u,p,g,*_ in D if yy==y and g>0),2))
for y,r in res.items(): print(y,r)
d27u=res[2027]['d']+UNCON[2027]; print('2027 unconstrained',d27u,round((res[2027]['s']-d27u)/d27u*100,1))
by={}
for y in range(2023,2028):
    for yy,v,_,u,p,*_ in D:
        if yy==y: by.setdefault(v,{}).setdefault(y,0); by[v][y]+=u/p*1000
for v in by: print(v,{y:round(x) for y,x in by[v].items()})
q,vt,vn=quarters()
out=dict(demand=[dict(y=a,v=b,chip=c,units=u,ppw=p,gb=g,pkg=k,src=s) for a,b,c,u,p,g,k,s in D],other=OTHER,uncon=UNCON,
 ts=TS,nt=NT,ut=UT,cap=dict(q=q,tsmc=vt,osat=vn),res=res)
json.dump(out,open('/workspace/chain_site/cowos_data/model_out.json','w'),ensure_ascii=False)
# ---------- Excel ----------
wb=openpyxl.Workbook();b=Font(bold=True);inp=PatternFill('solid',fgColor='FFF2CC')
ws=wb.active;ws.title='说明'
for r in ['CoWoS 先进封装供需模型 v0.1（2026-10-15，Kiko）','黄色格=可改假设；其余为公式。单位：千片(12寸 CoWoS 晶圆)/年；EB=10亿GB。',
 '需求 = Σ 出货(百万颗) ÷ 每片可封良品颗数 × 1000 + 其他(交换芯片/FPGA等)','供给 = Σ 12个月 (TSMC + 非TSMC 月产能) × 有效稼动率；月产能=年末锚点线性插值',
 '出货：KGI 2026-09-15 AI 加速器预测(Figure 10)；每片颗数(ppw)与每封装HBM容量多为自估，锚点：H100≈28、B200≈16 颗/片（爱建证券引 SemiAnalysis）',
 '产能锚点：KGI（TSMC 年末 13/34/72/120/185 千片/月；2.5D 合计 15/39/89/155/265）。其他口径：MS 2026/27 年末 130/200；UBS 180(+ASE 70、Amkor 20)；JPM 115/155。',
 '不构成投资建议。']: ws.append([r])
wd=wb.create_sheet('需求');wd.append(['年份','厂商','产品','出货(百万颗)','每片颗数ppw','封装类型','HBM GB/封装','CoWoS片(千)','HBM需求(PB)','出货来源']);[setattr(c,'font',b) for c in wd[1]]
for i,(y,v,c,u,p,g,k,s) in enumerate(D,start=2):
    wd.append([y,v,c,u,p,k,g,f'=D{i}/E{i}*1000',f'=D{i}*G{i}',s])
    for col in 'DEG': wd[f'{col}{i}'].fill=inp
n=len(D)+1
wo=wb.create_sheet('其他与供给');wo.append(['年份','其他需求(千片)','TSMC年末(千片/月)','非TSMC年末(千片/月)','有效稼动率']);[setattr(c,'font',b) for c in wo[1]]
yrs=[2022,2023,2024,2025,2026,2027]
for i,y in enumerate(yrs,start=2):
    wo.append([y,OTHER.get(y,0),TS[y],NT[y],UT]);[setattr(wo[f'{c}{i}'],'fill',inp) for c in 'BCDE']
wbal=wb.create_sheet('平衡表');wbal.append(['年份','需求(千片)','供给(千片)','缺口(供-需)','缺口/需求','隐含HBM需求(EB)']);[setattr(c,'font',b) for c in wbal[1]]
for i,y in enumerate(range(2023,2028),start=2):
    r=i+1  # row of year y in 其他与供给 (y-1 is row r-1)
    sup=f"=(12*(其他与供给!C{r-1}+其他与供给!D{r-1})+((其他与供给!C{r}-其他与供给!C{r-1})+(其他与供给!D{r}-其他与供给!D{r-1}))*78/12)*其他与供给!E{r}"
    wbal.append([y,f'=SUMIF(需求!A2:A{n},A{i},需求!H2:H{n})+其他与供给!B{r}',sup,f'=C{i}-B{i}',f'=D{i}/B{i}',f'=SUMIF(需求!A2:A{n},A{i},需求!I2:I{n})/1000'])
wq=wb.create_sheet('季度产能');wq.append(['季度','TSMC(千片/月)','非TSMC(千片/月)','合计','类型']);[setattr(c,'font',b) for c in wq[1]]
for a,x,z in zip(q,vt,vn): wq.append([a,x,z,round(x+z,1),'锚点' if a.endswith('Q4') else '插值(估)'])
wb.create_sheet('来源').append(['见 cowos_chain.md 附录'])
wb.save('cowos_model.xlsx')
# ---------- charts ----------
ys=list(range(2023,2028))
fig,ax=plt.subplots(figsize=(8,4.6),dpi=150)
ax.bar([y-.2 for y in ys],[res[y]['d']/1000 for y in ys],.4,label='需求（可见出货口径）',color='#d9534f')
ax.bar([y+.2 for y in ys],[res[y]['s']/1000 for y in ys],.4,label='供给（TSMC+OSAT）',color='#5b8def')
for y in ys: ax.text(y+.2,res[y]['s']/1000+.03,f"{res[y]['gap']:+.0f}%",ha='center',fontsize=10)
ax.scatter([2026,2027],[1.394,2.694],marker='D',color='k',zorder=5,label='MS 需求口径');ax.scatter([2026,2027],[1.307,2.475],marker='^',color='gray',zorder=5,label='UBS 需求口径')
ax.set_ylabel('百万片/年');ax.set_title('CoWoS 供需平衡（2023–2027，估）');ax.legend(fontsize=9);ax.set_xticks(ys);fig.tight_layout();fig.savefig('chart_balance.png')
fig,ax=plt.subplots(figsize=(8,4.2),dpi=150)
ax.stackplot(range(len(q)),vt,vn,labels=['台积电','非台积电(日月光/矽品/Amkor等)'],colors=['#d9534f','#9ccc65'],alpha=.8)
ax.set_xticks(range(0,len(q),4));ax.set_xticklabels(q[::4]);ax.set_ylabel('千片/月');ax.legend(loc='upper left');ax.set_title('CoWoS 季末产能（年末为锚点，季度插值）');fig.tight_layout();fig.savefig('chart_capacity.png')
fig,ax=plt.subplots(figsize=(8,4.2),dpi=150)
nv=[(y,res[y]) for y in ys]
units=[sum(u for yy,v,c,u,*_ in D if yy==y and v=='英伟达' and 'CPU' not in c) for y in ys]
wafs=[sum(u/p*1000 for yy,v,c,u,p,*_ in D if yy==y and v=='英伟达' and 'CPU' not in c) for y in ys]
ax.plot(ys,[u/units[0]*100 for u in units],'o-',label='英伟达 GPU 颗数（2023=100）',color='#76b900');ax.plot(ys,[w/wafs[0]*100 for w in wafs],'s-',label='对应 CoWoS 片数（2023=100）',color='#d9534f')
ax.set_title('封装面积通胀：片数涨得比颗数快');ax.legend();ax.set_xticks(ys);fig.tight_layout();fig.savefig('chart_inflation.png')
print('nv units',[round(u,2) for u in units],'wafers',[round(w) for w in wafs])
