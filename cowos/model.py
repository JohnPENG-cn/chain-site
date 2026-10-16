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
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
FP=next((f for f in ['/tmp/wenkai.ttf','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'] if os.path.exists(f)),None)
if FP: fm.fontManager.addfont(FP); FN=fm.FontProperties(fname=FP).get_name()
else: FN='sans-serif'
plt.rcParams['font.family']=FN; plt.rcParams['axes.unicode_minus']=False
# (year, vendor, product, units_M, ppw, hbm_GB_per_pkg, pkg, src_units)
# pkg: S=整片硅中介层 L=RDL+局部硅桥 R=有机 RDL B=封测厂 2.5D 硅桥(EFB)。v0.4.3 改正：2027 AMD MI450/MI455 为 CoWoS-L（MS：AMD 在台积电 CoWoS-L 24 万片，源66）；Venice 为日月光/矽品 EFB 硅桥（源74）。pkg 只影响硅中介层一环，不影响 CoWoS 片数。
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
(2027,'AMD','MI450/MI455',1.680,9,432,'L',K),(2027,'AMD','Venice CPU',4.750,25,0,'B','KGI 正文(4.5–5.0M)'),(2027,'其他GPU','其他',0.600,25,96,'S',K),
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
# ---------- v0.4.3 硅中介层（整片 TSV 硅中介层，CoWoS-S 用）----------
# 第一性原理：CoWoS-S 的"CoW"就是把芯片贴在一整片未切割的硅中介层晶圆上，所以 1 片 CoWoS-S 晶圆 = 1 片良品中介层晶圆（面积通胀已在 ppw 里）。
# CoWoS-L / EFB 只用小块硅桥（LSI），按每片封装晶圆折 BR 片中介层晶圆；CoWoS-R 不用硅。
SFRAC={(2026,'MTIA/Maia/OpenAI/其他'):0.5,(2027,'Maia/MTIA/OpenAI/其他'):0.5}  # 估：Maia 200 用 S、MTIA 400 用 L（源73）
BR=0.05      # 估：每片 L/EFB 封装晶圆消耗的硅桥面积 ≈ 0.05 片 12 寸硅晶圆（LSI 面积未公开，区间 0.02–0.15）
OTH_SI=0.6   # 估："其他"（交换芯片等）里用整片中介层的比例；MS：英伟达 Spectrum 交换芯片 CoWoS-S 约 5k 片/月（源65）
IP_UT,IP_Y=0.95,0.97   # 估：中介层产线稼动率；中介层良率（台积电称多项 CoWoS 产品良率 >98%，源77；中介层取略低）
IPE=IP_UT*IP_Y
def ip_need(y):
    sw=su=br=0
    for yy,_,ch,u,p,g,k,_s in D:
        if yy!=y: continue
        f=SFRAC.get((y,ch),1.0 if k=='S' else 0.0); w=u/p*1000
        sw+=w*f; su+=u*f
        if k in 'SLB': br+=BR*w*(1-f)
    oth=OTH_SI*OTHER[y]
    return dict(sw=round(sw,1),su=round(su,3),br=round(br,1),oth=round(oth,1),need=round(sw+br+oth,1))
IPN={y:ip_need(y) for y in range(2023,2028)}
# 供给（年末，千片/月，投片口径）
IP_UMC={2022:3,2023:3,2024:6,2025:6,2026:6,2027:6,2028:6}          # 源70（2023 年 3k，1Q24 起 6k）、源69（CFO 2026-05：已由 3,000 提升至 6,000）
IP_OTH={2022:0,2023:0,2024:0,2025:0,2026:0,2027:2,2028:5}          # 估：世界先进/VSMC 2027Q1 量产（源71）、力积电复线（源78），量未披露
IP_GF={2027:0,2028:5}                                              # 估：20 亿美元/5 年 ≈ 4 亿美元/年 ÷ 每片 4k–10k 美元 ≈ 3–8 千片/月，2028 上半年起量（源67）
IP_ADD={2026:20,2027:20,2028:0}   # 台积电自制新增：2026 +2 万（MS，源65）；2027 估与 2026 同速（Fab 15A 转产，量未披露，源66）；2028 估 0（改为委外，源67,68）
def ann(a,b): return 12*a+6.5*(b-a)   # 与 CoWoS 供给同一插值公式（千片/年）
# 校准（估）：台积电 2023 年末 = 当年 CoWoS 产能（2023 年全是 S 型，源1）；2024–25 年 CoWoS 增量几乎都是 L 型、S 型片数持平（302k→319k），
# 所以设 2024 年末 = 2025 年末 = X，X 取"2025 年最紧的一季中介层仍多 10%"（与 TOC 里键合机、电力同一校准规则；季度需求权重同 toc.json ramp）
RAMP=[0.22,0.24,0.26,0.28]
_qn=[(IPN[2025]['sw']+IPN[2025]['br'])*RAMP[k]+IPN[2025]['oth']/4 for k in range(4)]   # 2025 各季良品需求（千片/季）
X=round(max(_qn)*1.10/(3*IPE)-IP_UMC[2025],1)    # 2025 年产能持平，最紧在 Q4
IP_TS={2022:TS[2022],2023:TS[2023],2024:X,2025:X}
for y in (2026,2027,2028): IP_TS[y]=IP_TS[y-1]+IP_ADD[y]
IPC={y:IP_TS[y]+IP_UMC[y]+IP_OTH[y]+IP_GF.get(y,0) for y in range(2022,2029)}
ipres={}
for y in range(2023,2029):
    sup=ann(IPC[y-1],IPC[y])*IPE   # 良品中介层 千片/年
    r=dict(cap=round(IPC[y],1),ts=round(IP_TS[y],1),umc=IP_UMC[y],oth_s=IP_OTH[y]+IP_GF.get(y,0),sup=round(sup,1))
    if y in IPN: r.update(IPN[y]); r['gap']=round((sup-IPN[y]['need'])/IPN[y]['need']*100,1)
    ipres[y]=r
# 盈亏平衡：2027 年台积电自制要新增多少才不缺；2028 年需求最多能涨多少
_n27=IPN[2027]['need']/IPE; _a=IPC[2026]
BE27=round((_n27-12*_a)/6.5-IP_OTH[2027],1)       # 台积电 2027 新增（千片/月）
BE28=round(ipres[2028]['sup']/IPN[2027]['need']*100-100,1)   # 2028 中介层需求同比上限（%）
# 敏感度（2027 年中介层余量 %，其他不动）
def gap27(br=BR,oth=OTH_SI,add27=IP_ADD[2027],x=None,amd_s=False,eff=IPE):
    sw=su=b2=0
    for yy,_,ch,u,p,g,k,_s in D:
        if yy!=2027: continue
        if amd_s and ch=='MI450/MI455': k='S'
        f=SFRAC.get((2027,ch),1.0 if k=='S' else 0.0); w=u/p*1000; sw+=w*f
        if k in 'SLB': b2+=br*w*(1-f)
    need=sw+b2+oth*OTHER[2027]; xx=X if x is None else x
    a=xx+IP_UMC[2026]+IP_OTH[2026]+IP_ADD[2026]; b=a+add27+IP_OTH[2027]
    return round((ann(a,b)*eff-need)/need*100,1)
_xa=round(IPN[2025]['need']*1.10/IPE/12-IP_UMC[2025],1)   # 另一种校准：2025 全年多 10%
SENS=[['基准',f"{gap27():+.0f}%"],['硅桥折算 0.02 / 0.10 / 0.15 片（LSI 面积未公开）',f"{gap27(br=0.02):+.0f}% / {gap27(br=0.10):+.0f}% / {gap27(br=0.15):+.0f}%"],
 ['台积电 2027 年自制新增 1 万 / 3 万片/月',f"{gap27(add27=10):+.0f}% / {gap27(add27=30):+.0f}%"],
 [f'校准改为“2025 全年多 10%”（台积电 2024–25 年末 {_xa:.0f} 千片）',f"{gap27(x=_xa):+.0f}%"],
 ['交换芯片等用整片中介层的比例 30% / 90%',f"{gap27(oth=0.3):+.0f}% / {gap27(oth=0.9):+.0f}%"],
 ['AMD MI450/455 仍按 CoWoS-S 算（v0.4.2 的标签）',f"{gap27(amd_s=True):+.0f}%"],
 ['良率 90%（基准 97%）',f"{gap27(eff=IP_UT*0.90):+.0f}%"]]
print('敏感度',SENS)
ipq=[];
for y in range(2023,2028):
    for k in range(1,5): ipq.append(round(IPC[y-1]+(IPC[y]-IPC[y-1])*k/4,1))
print('硅中介层', {y:(r['cap'],r['sup'],r.get('need'),r.get('gap')) for y,r in ipres.items()},'X',X,'BE27',BE27,'BE28',BE28)
out=dict(demand=[dict(y=a,v=b,chip=c,units=u,ppw=p,gb=g,pkg=k,src=s) for a,b,c,u,p,g,k,s in D],other=OTHER,uncon=UNCON,
 ts=TS,nt=NT,ut=UT,cap=dict(q=q,tsmc=vt,osat=vn,ip=ipq),res=res,
 ip=dict(res=ipres,eff=IPE,ut=IP_UT,yld=IP_Y,br=BR,oth_si=OTH_SI,x=X,add=IP_ADD,be27=BE27,be28=BE28,sens=SENS,umc=IP_UMC,oth=IP_OTH,gf=IP_GF))
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
wi=wb.create_sheet('硅中介层');wi.append(['v0.4.3：1 片 CoWoS-S 晶圆 = 1 片良品硅中介层晶圆；L/EFB 按每片 %.2f 片硅桥折算；R 型不用硅。单位：千片 12 寸/年（需求、供给）与千片/月（年末产能）。估=自估'%BR])
wi.append(['年份','S 型片数','S 型颗数(百万)','硅桥折算','其他(交换芯片)','中介层需求','年末产能(千片/月)','其中台积电','联电','其他/格罗方德','良品供给(千片/年)','余量%']);[setattr(c,'font',b) for c in wi[2]]
for y in range(2023,2029):
    r=ipres[y];wi.append([y,r.get('sw'),r.get('su'),r.get('br'),r.get('oth'),r.get('need'),r['cap'],r['ts'],r['umc'],r['oth_s'],r['sup'],r.get('gap')])
wi.append([]);wi.append(['台积电 2024/2025 年末自制（校准）',X]);wi.append(['2027 年台积电自制新增的盈亏平衡（千片/月）',BE27]);wi.append(['2028 年中介层需求同比上限（%）',BE28])
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
