import json
J='/workspace/chain_site/data/hbm.json'
M=json.load(open(J))
bt=json.load(open('/workspace/chain_site/hbm_data/backtest.json'))
mugm=json.load(open('/workspace/chain_site/hbm_data/raw/mu_gm.json'))
M['updated']='2026-10-15'
# ---------- quarterly capacity (K wafers/month, end of quarter)
Q=[f'{q}Q{y%100}' for y in range(2023,2028) for q in range(1,5)]
def interp(a,b,n=4): return [round(a+(b-a)*(i+1)/n,1) for i in range(n)]
ss={'SK hynix':[15,20,35,45,60,80,110,135],'Samsung':[15,20,35,45,45,45,80,115],'Micron':[4,4,4,4,10,15,25,30],'CXMT':[0]*8}
ye={'SK hynix':[150,190,260],'Samsung':[150,180,250],'Micron':[45,100,120],'CXMT':[0,10,25]}
cap={'q':Q,'kind':['图读数']*8+['插值','插值','插值','锚点']*3}
for k in ss:
    v=ss[k][:];prev=v[-1]
    for t in ye[k]: v+=interp(prev,t);prev=t
    cap[k]=v
cap['anchors']=[
 {'p':'1Q23–4Q24','t':'三星证券 2024-03 报告 HBM Capa 季度图（图上读数，误差约 ±5K；2024 为当时预测）','src':24},
 {'p':'2024 年底','t':'TrendForce 2024-03：三星约 130K、海力士约 120K（含 TSV），全行业约 250K/月；美光 4Q24 约 25K（工商时报）','src':'25,26'},
 {'p':'2025 年底','t':'三星证券 2025-05：三星、海力士各约 150K；TrendForce 2025-10 称海力士扩至 150K；美光实际约 40–50K（ETNews，2026-09 回看），三星证券原预测 65K','src':'27,7'},
 {'p':'2026 年底','t':'三星 180K（BusinessKorea：今年 18 万片/月，明年 25 万）；美光约 100K（ETNews）；海力士 190K 为估（ETNews 称三星、海力士各 15–20 万，叠加 M15X 爬坡）','src':'28,7'},
 {'p':'2027 年底','t':'三星 250K（BusinessKorea 计划）；海力士 260K、美光 120K、长鑫 25K（有效产能）均为估：M15X 目标 8 万片/月、龙仁一厂 2027-02 开出首个洁净室','src':'28,29'}]
M['cap']=cap
# ---------- 2023/24 supply estimate
def avg(k,y):
    i=Q.index(f'1Q{y%100}');return sum(cap[k][i:i+4])/4
hs={}
for y,g,u in[(2023,350,.85),(2024,450,.80)]:
    w=sum(avg(k,y) for k in ['SK hynix','Samsung','Micron','CXMT'])
    hs[str(y)]={'wafers':round(w,1),'gbw':g,'ut':u,'s':round(w*12*g*u/1e6,3)}
M['hist_supply']=hs
M['hist_note']='2023/24 供给 = 季度产能均值 × 12 × 每片有效 GB（350/450，估）× 稼动率（85%%/80%%，估）。交叉验证：2024/2023 = %.1f 倍，TrendForce 2024-03 称 2024 年 HBM 位元供给增长约 260%%（3.6 倍）。'%(hs['2024']['s']/hs['2023']['s'])
# ---------- prices $/GB
M['prices']={
 'DDR5 16Gb 固定价':{'pts':[['2025-05',2.40],['2026-04',17.5],['2026-05',18.75],['2026-06',20.0],['2026-07',22.5],['2026-08',23.25],['2026-09',24.0]],'src':'30,31,20','kind':'实际','note':'韩国产业通商部月报引用的 DDR5 16Gb 固定交易价（$4.80→$48/颗）÷2GB'},
 'DDR4 8Gb 固定价':{'pts':[['2025-05',2.1],['2025-08',5.3],['2025-11',8.1],['2026-02',12.5],['2026-04',16.0],['2026-05',20.0]],'src':'30','kind':'实际','note':'产业通商部 5 月出口报告：DDR4 8Gb 季度/月度固定价（1GB/颗）'},
 'HBM3E 12层':{'pts':[['2025-08',8.3],['2025-12',13.9],['2026-06',12.0],['2026-08',17.5]],'src':'32,33,34','kind':'报道','note':'2025-08 $8.3、2025-12 续约 $13.9 为 Silicon Analysts 汇编的韩媒每颗报价 ÷36GB；2026 约 $1.50/Gb（≈$12/GB，Korea Herald）；$17–18/GB 为富邦研究经 MoneyToday 估计（英伟达口径）'},
 'HBM4 12层':{'pts':[['2025-08',13.9],['2026-01',16.7],['2026-09',16.7],['2027-06',36.1]],'src':'32,35,34','kind':'报道/预期','note':'2025-08 约 $500/颗、2026-01 预期 >$600/颗（汇编）；2026 年约 $600/颗、2027 年约 $1,300/颗（首尔经济，业界估计）；三星 2027 报价 $4.5–4.9/Gb≈$36–39/GB（Korea Herald，为要价非成交价）'}}
M['price_facts']=[
 ['TrendForce 2026-09-29','2027 年 HBM 混合 ASP 同比 +121%；8 层每 Gb 比 12 层贵 10–20%（base die 成本摊薄少）','36'],
 ['TrendForce（经 Korea Herald）','1Q26 起 DDR5 64GB 服务器内存的每片晶圆收入已超过 HBM','34'],
 ['首尔经济 2026-10-01','美光已签完 2027 年大部分 HBM 位元，价格"远高于 2026"；三星称 HBM 占全球 DRAM 投片将由约 20% 升至近 30%','35'],
 ['TrendForce 2025-05','HBM3E 上市时溢价约 20%，HBM4 溢价预计超 30%','37'],
 ['TrendForce 2024-05','HBM 单价约为 DDR5 的 5 倍；2025 年合约价先涨 5–10%','38']]
# ---------- backtest
M['bt']=bt
# ---------- margins
from datetime import date,timedelta
def cq(s):
    d=date.fromisoformat(s);d=d-timedelta(days=10) if d.day<10 else d;return f'{d.year}Q{(d.month-1)//3+1}'
M['mu_gm']={cq(k):v for k,v in mugm.items()}
hx_op=[60542608,37610283,19169574,11383390,9212851,7440504,8082796,7029958,5468536,2886029,346034,-1791961,-2882084,-3402302,-1912229,1660523,4197226,2863897,4219524,4171821]
hx_rev=[79318746,52576287,32826653,24448929,22231952,17639141,19767035,17573069,16423258,12429598,11305505,9066171,7305932,5088111,7672031,10982883,13811001,12155653,12376609,11805324]
qs=[f'{y}Q{q}' for y in range(2021,2027) for q in range(1,5)][2:22][::-1]
M['hx_om']={q:round(o/r*100,1) for q,o,r in zip(qs,hx_op,hx_rev)}
M['share_hist']=[['2025 全年',63.2,19.3,17.4,'IDC（经 Silicon Analysts 转引）','32'],['1Q26',58,21,21,'Counterpoint（经首尔经济）','35'],['2Q26',50,33,18,'Counterpoint','11']]
# ---------- process / suppliers
M['process']=[
 ['① DRAM 前道（1b/1c 制程）','~700 道工序；HBM die 比同容量 DDR5 大 35–45%','光刻/刻蚀/沉积：AMAT（自称 DRAM 设备营收超过其后两家之和）；Lam、TEL、ASML 等为行业通用设备商（业务归属，未单列来源）；国产：北方华创、拓荆（业务归属，HBM 占比未披露）','39'],
 ['② TSV 正面（约 10 步）','刻深孔 → 绝缘衬层 → 阻挡/籽晶 → 电镀填铜 → 微凸点','AMAT：InVia 2 CVD 衬层、Ventura 2 PVD、Nokota 电镀；AMAT 自称 HBM 封装工艺设备份额 >50%','39'],
 ['③ 背面（约 9 步）','临时键合 → 减薄 → 露铜 → 背面钝化/凸点 → 解键合','背面 PECVD 控翘曲（AMAT Avila）；减薄/CMP：华海清科；临时键合胶：鼎龙、飞凯（业务归属）','39'],
 ['④ 堆叠键合','8/12/16 层；HBM4 放宽至 775μm 厚度，16 层仍可用 TCB','SK 海力士 MR-MUF（液态 EMC 由日本 NAMICS 独家供应）；三星、美光 TC-NCF；TCB：韩美、ASMPT（目标 35–40% 份额）；混合键合：Besi、韩美二代（2029–30 主流）','40,17,18,41,19'],
 ['⑤ 测试/KGSD','晶圆级 + 堆叠后测试，良率损失主要在此','爱德万（存储测试机，业务归属）；探针卡供应商未能用公开来源核实','—'],
 ['⑥ base die','HBM4 起逻辑 base die','台积电 12nm/3nm（海力士、美光）；三星自家 4nm','8'],
 ['⑦ 2.5D 集成','HBM + GPU 上 CoWoS','台积电 CoWoS；长电展示 HBM3E 2.5D 方案但无自有 HBM 产能','12,42']]
M['cost']={'steps':[['DDR5（同容量、同制程）',1.0,1.0],['die 面积 +35–45%',1.35,1.45],['良率（含 TSV）低 20–30%',1.69,2.07],['HBM4：2048 I/O 更大 die + 逻辑 base die + 12/16 层堆叠',2.5,3.2]],
 'facts':[['生产周期','比 DDR5 长 1.5–2 个月；从投片到封装完成超过 2 个季度','25'],['每 bit 耗片','约 DDR5 的 3 倍（美光口径，经 Silicon Analysts）','9'],['新增产能资本开支','M15X 投资 >20 万亿韩元，满产约 5 万片/月 → 约 4,000 亿韩元/千片月产能；龙仁一厂 120 万亿韩元、满产约 35 万片/月 → 约 3,400 亿韩元/千片','29'],['洁净室到量产','M15X 首个洁净室 2026-05 完工试产，约 6 个月后量产','29'],['HBM 占 DRAM 产出','约 15%（The Elec 2026-03，SEMI 转述）；投片口径约 20% → 近 30%（三星）','43,35']],
 'parity':'同一片晶圆做 HBM 只出约 1/3 的位元，所以 HBM 每 GB 至少要卖到 DDR5 的约 3 倍，每片晶圆收入才持平（还没算 HBM 多出来的封装测试成本）。按 9 月 DDR5 固定价 $24/GB 算，持平线约 $72/GB；2027 年 HBM4 约 $36/GB 也只有一半。'}
# ---------- exposures (Tushare fina_mainbz 2025 annual)
M['exposure']={'雅克科技':'半导体化学材料 24.6%、光刻胶 22.8%、电子特气 4.8%','华海诚科':'环氧塑封材料 93.6%','飞凯材料':'半导体材料 20.8%','鼎龙股份':'半导体材料及芯片 57.0%（含临时键合胶）','赛腾股份':'自动化设备 74.6%','快克智能':'固晶键合封装设备 4.6%','拓荆科技':'半导体专用设备 96.6%','通富微电':'集成电路封测 97.6%','长电科技':'芯片封测 99.6%','北方华创':'电子工艺装备 93.4%','华海清科':'半导体装备 87.2%','台积电':'先进封装约 8%（2024）→ 略高于 10%（2025）→ 2026 年"十几%"','ASMPT':'先进封装 5.32 亿美元，占 2025 年营收约 30%；TCB 收入创纪录'}
M['changelog']=[
 ['2026-10-15','v0.2','补 2023–24 供给与分厂季度产能（1Q23–4Q27）；HBM/DDR 每 GB 价格实数图；韩国出口领先-滞后回测（2015–2026）；成本结构与资本开支；工艺-设备-材料表；公司图谱补来源、营收占比和设备材料商；手机端图谱不再裁切；新增对外接口。'],
 ['2026-10-14','v0.1','首版：核心判断、供需滑块模型、瓶颈、历史、领先指标、预测台账、资本与公司图谱。']]
new=[
 (24,'三星证券 2024-03 报告（HBM Capa 季度图）','https://www.samsungpop.com/common.do?cmd=down&contentType=application%2Fpdf&fileName=2020%2F2024032107171771K_02_03.pdf&inlineYn=Y&saveKey=research.pdf'),
 (25,'TrendForce 2024-03：2024 HBM 位元供给 +260%、die 大 35–45%、良率低 20–30%、年底产能','https://www.trendforce.com/presscenter/news/20240318-12081.html'),
 (26,'TrendForce 转工商时报：美光广岛 4Q24 约 2.5 万片','https://www.trendforce.com/news/2024/07/10/news-samsung-sk-hynix-and-micron-ramp-up-hbm-production-reportedly-doubling-output-next-year/'),
 (27,'Jukan 转三星证券 2025-05：2025 年底产能','https://www.semiconsam.com/p/samsung-securities-hbm-analysis-2025515'),
 (28,'BusinessKorea：三星 18 万 → 25 万片、M15X 扩至 8 万片','https://www.businesskorea.co.kr/news/articleView.html?idxno=277595'),
 (29,'首尔经济 2025-12：M15X 投资、洁净室时间表、龙仁一厂 35 万片','https://en.sedaily.com/finance/2025/12/25/sk-hynix-to-launch-m15x-fab-in-may-2026-cementing-global-ai'),
 (30,'韩国产业通商部：2015–2025 月度半导体/存储出口（公共数据门户 CSV）','https://www.data.go.kr/data/15051126/fileData.do'),
 (31,'产业通商部：2026 年 1–8 月月度半导体出口','https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/172161/view'),
 (32,'Silicon Analysts：HBM 每 GB 价格汇编（二手汇编，免费部分）','https://siliconanalysts.com/market-data/hbm-pricing'),
 (33,'TrendForce 转富邦/MoneyToday：HBM4 $31–32/GB、HBM3E $17–18/GB','https://www.trendforce.com/news/2026/08/13/news-samsung-sk-hynixs-hbm4-push-puts-hbm-general-memory-pricing-in-the-spotlight-for-2h-earnings/'),
 (34,'Korea Herald 2026-10-07：三星 2027 HBM 价格、HBM3E 约 $1.50/Gb','https://www.koreaherald.com/article/10895833'),
 (35,'首尔经济 2026-10-01：HBM4 $600 → $1,300/颗','https://en.sedaily.com/finance/2026/10/01/hbm-prices-to-more-than-double-next-year-as-shortage'),
 (36,'TrendForce 2026-09-29：2027 HBM 混合 ASP +121%','https://www.trendforce.com/presscenter/news/20260929-13255.html'),
 (37,'TrendForce 2025-05：HBM4 溢价超 30%','https://www.trendforce.com/presscenter/news/20250522-12589.html'),
 (38,'TrendForce 2024-05：HBM 约 DDR5 的 5 倍价','https://www.trendforce.com/presscenter/news/20240506-12125.html'),
 (39,'Applied Materials：HBM 新增 19 道工序、封装设备份额','https://www.appliedmaterials.com/us/en/newsroom/blogs/hbm--materials-innovation-propels-high-bandwidth-memory-into-the.html'),
 (40,'Dealsite：SK 海力士 MR-MUF 材料由 NAMICS 独家供应','https://dealsite.co.kr/articles/119413'),
 (41,'ASMPT 2025 年报公告：先进封装 5.32 亿美元、TCB','https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2025-annual-results/'),
 (42,'Wccftech 转 ZDNet Korea：长鑫 HBM3 延后、长电 HBM3E 方案','https://wccftech.com/china-ymtc-hits-hbm3-roadblock-domestic-makers-rush-hbm-manufacturing/'),
 (43,'The Elec 2026-03：HBM 约占 DRAM 产出 15%','https://www.thelec.net/news/articleView.html?idxno=5886'),
 (44,'NVIDIA 与 SK 海力士多年合作（2026-06-07）','https://nvidianews.nvidia.com/news/sk-hynix-ai-factory'),
 (45,'美光：HBM4 为 NVIDIA Vera Rubin 设计并量产（2026-03-16）','https://investors.micron.com/news/press-release/2026/Micron-in-High-Volume-Production-of-HBM4-Designed-for-NVIDIA-Vera-Rubin-PCIe-Gen6-SSD-and-SOCAMM2-03-16-2026/default.aspx'),
 (46,'三星：首家商用 HBM4 出货（未点名客户）','https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing'),
 (47,'TSMC 4Q25 法说会：先进封装营收占比（转引原话）','https://www.aipredictionindex.com/p/wei-2026-advanced-packaging-low-teens-2026/'),
 (48,'SK 海力士季度营收/利润（StockAnalysis 汇总财报）','https://stockanalysis.com/quote/krx/000660/financials/?p=quarterly'),
 (49,'美光季度营收/毛利（SEC XBRL API）','https://data.sec.gov/api/xbrl/companyfacts/CIK0000723125.json'),
 (50,'Tushare fina_mainbz：A 股公司 2025 年报主营构成','https://tushare.pro/document/2?doc_id=81'),
 (51,'TrendForce 2025-12：三星、海力士 2026 HBM3E 提价约 20%','https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/')]
ids={s['id'] for s in M['sources']}
for i,t,u in new:
    if i not in ids: M['sources'].append({'id':i,'t':t,'u':u})
json.dump(M,open(J,'w'),ensure_ascii=False)
print(hs, M['hist_note']);print({k:cap[k] for k in ['SK hynix','Samsung','Micron']})
