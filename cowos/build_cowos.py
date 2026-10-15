import json
M=json.load(open('/workspace/chain_site/cowos_data/model_out.json'))
B=json.load(open('/workspace/chain_site/cowos_data/backtest.json'))
CL=json.load(open('/workspace/chain_site/cowos_data/cl.json'))
MG=json.load(open('/workspace/chain_site/cowos_data/margins.json'))
R=M['res']
S=lambda *a:','.join(map(str,a))
J={}
J['meta']=dict(id='cowos',name='CoWoS 先进封装',version='v0.1',updated='2026-10-15',schema='chain/v1',
  unit='需求与产能用 12 寸 CoWoS 晶圆（片/月、片/年）；出货用颗（封装）；HBM 用 GB/EB。')
J['judgment']=dict(
 title='2027 年卡住 AI 芯片的，<br>不再是 CoWoS，而是 HBM 和基板',
 dek='CoWoS 产能三年涨了 9 倍，2027 年还要再涨约七成，总量缺口收窄到个位数。但封装越做越大，每片晶圆能封的芯片从 H100 的约 28 颗掉到 Rubin Ultra 的约 6 颗，<b>片数涨得比颗数快得多</b>；而 HBM、ABF 基板的扩产速度只有 CoWoS 的一半左右。按两条小链对账，2027 年木桶的短板是 HBM。',
 stats=[dict(id='cwHGap',n=f"{R['2027']['gap']:+.0f}%",l='2027 CoWoS 缺口/需求（可见出货口径）',tag='估'),
        dict(id='cwHHbm',n='约 6 成',l='2027 HBM 可供量 ÷ CoWoS 出货所需 HBM',tag='估'),
        dict(n='12 万→18.5 万',l='台积电 CoWoS 年末产能（片/月，2026→2027）',tag='源1'),
        dict(n='10–12 个月',l='弘塑设备交期；产能只够需求 1/3–1/4',tag='源27')])
J['debates']=[
 dict(q='Q1 2027 年 CoWoS 还会是 AI 芯片的头号瓶颈吗？',view='不会。总量缺口约 4%–11%，真正更紧的是 HBM（只够约六成）和 ABF/T-glass 基板。',falsify='2027 年出现 HBM 或基板库存积压、而 CoWoS 订单仍排不进，或台积电 2027 年报仍称 CoWoS 是首要限制。'),
 dict(q='Q2 OSAT 和 EMIB-T 会分走台积电的利润吗？',view='分走的是"溢出量"，不是利润中心。台积电自家先进封装毛利已接近公司平均，日月光 ATM 毛利 27%，EMIB-T 基板良率才 45%。',falsify='2027 年日月光/Amkor 的 2.5D 产能占比超过 35%，或 EMIB-T 在 2027 年内拿到 10 万颗以上外部 AI 芯片量产。'),
 dict(q='Q3 设备股的这轮景气什么时候见顶？',view='还没见顶：设备三家 3 个月营收同比 9 月 +43% 还在加速，合约负债重新增长。历史上设备营收同比的拐点比台积电营收同比拐点早 1–13 个月（中位 4 个月）。',falsify='2027 年上半年设备三家营收同比掉头向下，而台积电 2027 年产能指引仍上修 → 指标失灵。')]
J['variants']=[
 ['CoWoS-S','整片硅中介层（带 TSV）','≤约 2,700mm²（3.3× 光罩）','H100/H200、MI300/355、TPU v7/v8i','成熟主力；KGI 称 S 型产能 2027 仍紧','10,1'],
 ['CoWoS-L','有机 RDL + 局部硅桥 LSI','2026 年 5.5×、2027 年 9× 光罩，路线图到 14×','B200/B300、Rubin、Rubin Ultra','英伟达主力；大尺寸翘曲待解决','10,11,13'],
 ['CoWoS-R','有机 RDL 中介层','大，成本低','Trainium3、Vera CPU、交换芯片','2027 年被 Vera CPU 大量占用','1,5'],
 ['SoIC','3D 混合键合（Cu-Cu）','—','AMD MI300、Rubin Ultra/Feynman','2026 年 1–1.5 万片/月；每单位资本开支远高于 CoWoS','20'],
 ['InFO / CoPoS','扇出型；CoPoS 为 310×310mm 方形面板','面板利用率高于圆片','手机 SoC；CoPoS 面向大芯片','CoPoS 试产线 2026 建成，2028 起量、2029 才有意义贡献','26,1'],
 ['OSAT 类 CoWoS','日月光 FOCoS/全流程、矽品 oS、Amkor 2.5D','—','Vera CPU、Venice CPU、博通交换芯片','日月光全流程 2026 约 3 亿美元；Amkor 2.5D 约 1.5→2.5 万片/月','16,1'],
 ['Intel EMIB-T / Foveros','基板内嵌硅桥 + TSV；Foveros 为 3D','9× 光罩以上','谷歌 TPU v9 Humufish（2028）','基板良率约 45%，供应链目标 1Q27 达 60%','21,22,1']]
J['process']=[
 ['① 中介层制造','硅中介层：TSV、多层 RDL、深沟槽电容（台积电约 65nm 级产线）；L 型为 RDL + 局部硅桥','台积电自制；L 型硅桥同样由台积电做。CoWoS-S 中介层每片价值约 1 万美元、L 型约 1.5 万美元','10,9'],
 ['② CoW 芯片上片','把 SoC 和 HBM 用微凸块键合到中介层晶圆上','Sorter/Die Bonder：均华；TCB：ASMPT、韩美等（业务归属）','28'],
 ['③ 底部填充与模封','点胶、underfill、模封，控制翘曲','点胶/AOI：万润（2Q26 合约负债季增 304%）','29'],
 ['④ 减薄、露 TSV、暂时性贴合','研磨减薄、临时键合/解键合、湿法清洗与去胶','研磨/切割：Disco；湿制程：弘塑、辛耘；暂时性贴合：辛耘','30,28'],
 ['⑤ 切割','把中介层晶圆切成单个封装体','Disco 切割机、激光','30'],
 ['⑥ oS 上基板','贴到 ABF 载板上（大封装 100mm 级）','载板：欣兴、Ibiden、南电；ABF 膜：味之素；T-glass 玻纤布：日东纺（约 90%）','23,25'],
 ['⑦ 测试','CP/FT/老化，大封装测试时间长','测试机：Advantest 等（台积电称测试机也短缺）；探针卡：精测、旺矽；代测：京元电','13,1']]
J['model']=M
J['cap_src']=[
 ['KGI','2026-09-15','120','185–190','非台积电 2.5D：2026 年 35、2027 年 80；台积电仍缺 15–20%','1'],
 ['UBS','2026-09-22','行业 160','180（行业 270：日月光 70、Amkor 20）','ASIC 占 CoWoS 需求 28%→33%','2'],
 ['摩根士丹利','2026-09-13','130','200（2028 年 260）','2027 年 CoWoS-L 订单 21 万片，+200%','3'],
 ['摩根士丹利','2026-06-23','—','200（非台积电 80）','全球需求 139.4 万→269.4 万片/年','4'],
 ['摩根大通','2026 年中','115','155（2028 年 175）','非台积电 2027 年约 25','6'],
 ['Digitimes','2026-07-10','—','≥200','市场传闻（付费墙，只看到标题）','7'],
 ['爱建证券','2026-05-12','115–140','170','2026 年 S:L 约 5.5:4.5','9']]
J['ppw']=[['H100（CoWoS-S）','~28','5–6 颗 HBM3，80GB','源9'],['B200（CoWoS-L）','~16（模型 14–15）','8 颗 HBM3E，192GB','源9'],['B300','12–13','8 颗 HBM3E 12 层，288GB','估'],['Rubin','9（2026）→10（2027 良率改善）','8 颗 HBM4，288GB','估'],['Rubin Ultra','~6','KGI 表：72 封装共 18.4TB → 约 256GB','估；容量源1'],['Vera CPU（CoWoS-R）','~45','无 HBM','估；MS：575 万颗用 >10 万片'],['Venice CPU','~25','无 HBM','估；MS：675 万颗用 27 万片'],['TPU v7 / v8','20 / 17','192GB / v8i 288GB、v8t 216GB','估；容量源1'],['Trainium3（CoWoS-R）','~24','144GB','估；MS：AWS 2027 约 12.6 万片']]
pool=[
 dict(seg='台积电 先进封装',rev=21.0,gm=60,src='14,15,32',note='营收 = 2026 年营收约 1,700 亿美元 × "低双位数"（取 12.5%）；毛利率 = "接近公司平均"（2024 年说法），取 60%',est=True),
 dict(seg='载板（欣兴）',rev=5.4,gm=24.8,src='32',note='2Q26 单季年化；含非 ABF 业务；毛利率一年从 13.1% 升到 24.8%',est=False),
 dict(seg='日月光 LEAP',rev=3.7,gm=27.3,src='16,17',note='2026 LEAP >35 亿美元；毛利率用 ATM 整体 27.3% 代替（LEAP 未单独披露）',est=True),
 dict(seg='Amkor 先进产品',rev=6.2,gm=16.8,src='18',note='2Q26 先进产品 15.6 亿美元年化；含倒装/存储等，非 2.5D 专项；毛利率用公司整体',est=False),
 dict(seg='测试（京元电）',rev=1.4,gm=39.5,src='32',note='2Q26 单季年化',est=False),
 dict(seg='台系设备（弘塑+辛耘+万润+均华）',rev=1.0,gm=45,src='32',note='2Q26 单季年化；四家加权毛利率约 45%',est=False)]
J['profit']=dict(pool=pool,margins={k:MG[k] for k in ['2330','3711','3037','2449','3131','6187']},
 names={'2330':'台积电(公司整体)','3711':'日月光投控','3037':'欣兴(载板)','2449':'京元电(测试)','3131':'弘塑(设备)','6187':'万润(设备)'},
 capex=[['台积电','2026 资本开支 600–640 亿美元，其中先进封装、测试、光罩等 10–20%','13'],['日月光投控','2026 资本开支 105 亿美元（年内第三次上调），设备约 56% 封装、40% 测试','16'],['Amkor','2026 资本开支 25–30 亿美元；亚利桑那厂 2028 年投产','18'],['LEAP 营收','日月光：2024 约 6 亿 → 2025 约 16 亿 → 2026 >35 亿美元 → 2027 再翻倍','16,17']],
 unit_cost=[['CoWoS-S 中介层','约 1 万美元/片','9'],['CoWoS-L 中介层','约 1.5 万美元/片','9'],['H100 封装成本','约 750 美元/颗','9,10'],['B200 封装成本','1,000–1,100 美元/颗','10']])
J['neck']=[
 dict(name='HBM（跨链：见 HBM 页）',now='KGI：2027 年 HBM 供给 +45–50%，CoWoS +71%；按本页出货口径 2027 需 HBM 约 6.5 EB，HBM 页模型供给约 4.0 EB',months=36,verdict='2027 头号短板',src='1,33'),
 dict(name='ABF 载板 / T-glass 玻纤布',now='日东纺约占 T-glass 90%，福岛扩产到 2027 年才放量；载板短缺看到 2028 年；味之素 ABF 膜提价 30%；KGI：2027 年 ABF 只 +25–30%',months=24,verdict='第二短板',src='23,24,25,1'),
 dict(name='封装设备交付',now='弘塑交期 10–12 个月，2026 年出机 220–240 台、2027 年约 325 台，只够需求 1/3–1/4',months=12,verdict='决定扩产速度',src='27'),
 dict(name='测试机与测试产能',now='台积电 2Q26 法说会：测试机也短缺，资本开支在测试/封装间移动',months=9,verdict='容易被忽视',src='13'),
 dict(name='CoWoS-S / R 结构性缺口',now='KGI：S、R 型产能都缺，博通 2027 指引 50 万片只能排进 38–39 万；R 型被 Vera CPU 占满',months=12,verdict='总量够、型号不够',src='1'),
 dict(name='台积电 CoWoS 总产能',now='12 万（2026 年末）→ 18.5–20 万（2027 年末），缺口从 30–35% 收窄到 15–20%（对客户需求）',months=15,verdict='2027 年缓解',src='1,3'),
 dict(name='超大中介层翘曲 / 9× 光罩',now='9× 光罩 CoWoS-L 还要解决翘曲、成本与良率',months=18,verdict='下一代变量',src='11')]
J['history']=dict(
 tl1=[['2011–12','CoWoS 首个产品：赛灵思 Virtex-7 2000T（28nm）','19,35'],['2016','英伟达 GP100 用 CoWoS + HBM2；同年 InFO 量产（苹果 A10，公认史实）','19'],['2017–18','Intel EMIB 首批产品（Stratix 10、Kaby Lake-G，公认史实）','—'],['2019–20','中介层从 1× 到 2× 光罩以上；A100 用 CoWoS-S','19'],['2022','SoIC 首个量产（AMD 3D V-Cache，公认史实）','—'],['2024','CoWoS-L 量产（B200），突破硅中介层约 2,700mm² 上限','10'],['2026','5.5× 光罩；CoPoS 试产线建成；谷歌 TPU v9 选 EMIB-T','26,1'],['2027','9× 光罩 CoWoS-L；日月光 310mm 面板线 1Q27 投产','11,16'],['2028–29','CoPoS 起量（KGI：2029 年才有意义贡献）；玻璃基板','1,26']],
 tl2=[['2023','ChatGPT → H100 缺货，瓶颈就是 CoWoS 产能本身（年末约 1.3 万片/月）','1'],['2024','产能翻 2.6 倍到 3.4 万片；先进封装约占台积电营收 8%','1,14'],['2025','7.2 万片；先进封装占比略超 10%；日月光 LEAP 16 亿美元','1,14,17'],['2026','12 万片；"封装产能紧到限制客户成长"；设备交期 10–12 个月；载板毛利率翻倍','13,27,32'],['2027E','18.5–20 万片；CoWoS +71% 快于 ABF（+25–30%）和 HBM（+45–50%）→ 短板移到元件','1']],
 rule='每轮扩产后，瓶颈会移到扩得最慢的相邻环节，利润也跟着走（克里斯坦森"利润守恒"）：2023 年在 CoWoS 产线，2026 年开始移到设备交付和载板（欣兴毛利率一年翻倍），2027 年移到 HBM。')
J['lead']=dict(
 cards=[
  ['设备三家月营收（弘塑、辛耘、万润）','每月 10 日前','同比拐点比台积电营收同比拐点早 1–13 个月（13 次中 11 次领先，中位 4 个月）；水平相关弱（r=0.36）','9 月 3 个月合计同比 +43%，还在加速','31'],
  ['设备商合约负债（预收款）','季度','一轮周期里同比见顶比营收同比见顶早约 6 个季度（只有 1 个周期）','2Q26 三家合计 185.5 亿新台币，同比 +10%，重新上升；约等于 2.6 个季度营收','32,29'],
  ['Disco 季度出货额','季度（季后第 6 天）','出货早于确认营收（设备验收后才确认）','7–9 月出货 1,239 亿日元 +60%，销售 +39%','30'],
  ['载板三家月营收（欣兴、南电、景硕）','月','与台积电营收同步（r=0.55，滞后 0–1 个月）','9 月 3 个月同比 +51%','31'],
  ['台积电/日月光法说会产能口径','季度','直接给出产能与缺口','台积电 4Q26 法说会 2027-01 中旬','13,16'],
  ['券商产能预测修正（KGI/MS/UBS）','月','上修 = 需求还在加','2027 年末从 155–175k 上修到 180–200k','1,2,3,6']])
J['bt']=dict(series=B['series'],xc={'设备→台积电':B['xc_equip_tsmc'],'设备→日月光':B['xc_equip_ase'],'载板→台积电':B['xc_abf_tsmc']},peaks=B['peaks'],cl=CL,
 tp=[['2016-10 见顶','2016-11','+1'],['2018-01 见顶','2018-05','+4'],['2019-03 见顶','2020-03','+12'],['2021-04 见顶','2022-05','+13'],['2024-09 见顶','2025-04','+7'],['2015-11 见底','2016-01','+2'],['2017-03 见底','2017-06','+3'],['2018-12 见底','2019-04','+4'],['2020-03 见底','2020-12','+9'],['2023-02 见底','2023-05','+3'],['2025-10 见底','2025-12','+2']],
 annual=B['annual'])
J['predictions']=[
 dict(id='C1',text='台积电 2026 全年先进封装营收占比 ≥ 12%（魏哲家口径"低双位数"）',due='2027-01-21',check='台积电 4Q26 法说会',status='pending'),
 dict(id='C2',text='设备三家（弘塑+辛耘+万润）2026 年 10–12 月营收合计同比 ≥ +30%（7–9 月为 +43%）',due='2027-01-12',check='MOPS 月营收',status='pending'),
 dict(id='C3',text='日月光 2026 全年 LEAP 营收 ≥ 37 亿美元（指引 >35 亿，"再多数亿"）',due='2027-02-28',check='日月光 4Q26 法说会',status='pending'),
 dict(id='C4',text='设备三家 4Q26 合约负债合计同比 ≥ +15%（2Q26 为 +10%）',due='2027-03-31',check='三家 2026 年报',status='pending'),
 dict(id='C5',text='英伟达 Rubin Ultra 正式规格每个封装 HBM ≤ 384GB（原路线图约 1TB），说明 HBM 比 CoWoS 更紧',due='2027-06-30',check='GTC 2027 / 官方规格',status='pending'),
 dict(id='C6',text='2027 年内 Intel EMIB-T 没有外部客户的 AI 加速器进入月产万颗以上量产',due='2027-12-31',check='Intel/谷歌公告、供应链报道',status='pending'),
 dict(id='C7',text='台积电 2027 年末 CoWoS 产能 ≥ 18 万片/月（主流券商 180–200k）',due='2028-01-31',check='台积电法说会/主流券商口径',status='pending')]
J['companies']=dict(seg=['台积电/代工','OSAT 封测','设备','载板与材料','测试','竞争方案','客户/设计服务'],
 co=[['台积电','2330.TW','TW',0,'CoWoS 年末 12 万→18.5 万片/月 [源1]',30],
 ['日月光投控(含矽品)','3711.TW','TW',1,'LEAP 2026 >35 亿美元；全流程约 3 亿美元 [源16]',22],['Amkor','AMKR','US',1,'2.5D 约 1.5→2.5 万片/月 [源1]',16],['力成','6239.TW','TW',1,'KGI 2.5D 产能图列入 [源1]',10],['长电科技','600584.SH','A',1,'2.5D/XDFOI（业务归属，占比未披露）',10],['通富微电','002156.SZ','A',1,'AMD 封测伙伴（业务归属）',10],
 ['弘塑','3131.TWO','TW',2,'湿制程；交期 10–12 个月 [源27]',12],['辛耘','3583.TWO','TW',2,'湿制程、暂时性贴合；合约负债约 150 亿新台币 [源29]',12],['万润','6187.TWO','TW',2,'CoWoS 点胶/AOI [源28,29]',11],['均华','6640.TWO','TW',2,'Sorter/Die Bonder [源28]',9],['Disco','6146.T','US',2,'研磨/切割；季度出货 +60% [源30]',13],['BESI','BESI.AS','US',2,'混合键合（SoIC）[源20]',11],['ASMPT','0522.HK','HK',2,'TCB（业务归属）',10],
 ['欣兴','3037.TW','TW',3,'ABF 载板；毛利率 13.1%→24.8% [源32]',13],['南电','8046.TW','TW',3,'ABF 载板',9],['Ibiden','4062.T','US',3,'ABF 载板（业务归属）',11],['日东纺','3110.T','US',3,'T-glass 约 90% [源23]',12],['味之素','2802.T','US',3,'ABF 膜，提价 30% [源25]',11],['兴森科技','002436.SZ','A',3,'ABF 载板（业务归属，占比未披露）',9],['深南电路','002916.SZ','A',3,'封装基板（业务归属）',9],
 ['京元电','2449.TW','TW',4,'测试；毛利率 39.5% [源32]',11],['中华精测','6510.TWO','TW',4,'探针卡 [源1]',9],['旺矽','6223.TWO','TW',4,'探针卡 [源1]',9],['Advantest','6857.T','US',4,'测试机（台积电称测试机短缺 [源13]）',11],
 ['Intel','INTC','US',5,'EMIB-T/Foveros；基板良率约 45% [源21]',14],
 ['英伟达','NVDA','US',6,'2027 年 CoWoS 约 122 万片 [源4]',20],['博通','AVGO','US',6,'2027 年约 48 万片 [源5]',15],['AMD','AMD','US',6,'2027 年约 53 万片 [源5]',14],['谷歌','GOOGL','US',6,'TPU 2027 年约 910 万颗 [源1]',13],['联发科','2454.TW','TW',6,'TPU v8t，2027 年约 18 万片 [源5]',11],['AWS','AMZN','US',6,'Trainium3 2027 年约 306 万颗 [源1]',11],['世芯','3661.TW','TW',6,'AWS 后端设计 [源1]',9]],
 links=[['台积电','英伟达','CoWoS-L 主力；2027 年约 122 万片','4','sup'],['台积电','博通','第二大 CoWoS 客户（KGI）','1','sup'],['台积电','AMD','2027 年约 53 万片（含 Venice 外包部分）','5','sup'],['日月光投控(含矽品)','英伟达','约 50% Vera CPU','1','sup'],['日月光投控(含矽品)','AMD','多数 Venice CPU','1','sup'],['Amkor','英伟达','Vera CPU 余量','1','sup'],['Amkor','博通','连接芯片 2.5D','1','sup'],['Intel','谷歌','TPU v9 采用 EMIB-T，2Q28 起显著','1','sup'],['联发科','谷歌','TPU v8t/v9 设计','1','sup'],['博通','谷歌','TPU v7/v8i 设计','1','sup'],['世芯','AWS','Trainium 后端设计','1','sup'],
  ['弘塑','台积电','湿制程设备','28','ord'],['均华','台积电','CoWoS/SoIC Sorter、Die Bonder','28','ord'],['万润','台积电','CoWoS 点胶/AOI','28','ord'],['辛耘','台积电','湿制程、暂时性贴合','28','ord'],['BESI','台积电','SoIC 混合键合','20','ord'],['日东纺','欣兴','T-glass 供给','23','sup'],['日东纺','Ibiden','T-glass 供给','23','sup'],['味之素','欣兴','ABF 膜提价','25','sup'],
  ['台积电','—','2026 资本开支 600–640 亿美元','13','cap'],['日月光投控(含矽品)','—','2026 资本开支 105 亿美元','16','cap'],['Amkor','—','2026 资本开支 25–30 亿美元','18','cap']])
J['interface']=dict(rows=[
 ['产出单位','12 寸 CoWoS 晶圆（片/年）','—','本页模型'],
 ['可供量（本页模型）',f"约 {R['2026']['s']/1000:.2f} 百万片",f"约 {R['2027']['s']/1000:.2f} 百万片",'台积电 + 非台积电，有效稼动率 95%（估）'],
 ['每片可封颗数（单耗）','B300 12–13、Rubin 9','Rubin 10、Rubin Ultra 6','估；锚点 H100 28、B200 16（源9）'],
 ['每封装 HBM','B300/Rubin 288GB（8 颗）','Rubin Ultra ~256GB；MI450 432GB；TPU v8i 288GB','源1 与公开规格'],
 ['每片 CoWoS 消耗 HBM','B300 ≈ 3.5 TB/片','Rubin ≈ 2.9 TB/片；Rubin Ultra ≈ 1.5 TB/片','= 每片颗数 × 每封装 HBM（估）'],
 ['出货隐含 HBM 需求',f"{R['2026']['hbm']} EB",f"{R['2027']['hbm']} EB",'KGI 出货 × 每封装 HBM（估）'],
 ['价格','中介层 S 约 1 万、L 约 1.5 万美元/片','封装成本 B200 1,000–1,100 美元/颗','源9,10']],
 formula='可出货加速器 = min( CoWoS 片 × 每片颗数 , HBM 可供量 ÷ 每封装 HBM , 载板 , 前道逻辑晶圆 )')
J['limits']=['台积电不单独披露 CoWoS 产能、营收和毛利率。产能用券商口径（KGI 为基准，其他口径并列），季度值是年末锚点之间的线性插值。',
 '每片可封颗数（ppw）大多是自估，只有 H100≈28、B200≈16 两个公开锚点；它直接决定需求片数，是本模型最敏感的假设（滑块可调）。',
 '出货量用 KGI 的预测（已经考虑了供给限制），所以"可见出货口径"的缺口天然偏小；"客户需求口径"只加了 KGI 点名的三项差额（约 19 万片），不是完整的未受限需求。',
 '2025–26 年模型显示总量略有富余（+5%～+7%），与"全年紧缺"的公开说法不完全一致，可能来自：爬坡期良率、S/L/R 型号错配、在制品时滞。误差约 ±10%。',
 '利润池里只有台积电先进封装毛利率是估的（"接近公司平均"）；其他公司毛利率是公司整体或业务线口径，不是 CoWoS 专项。',
 '多家券商数据来自转述（TechFlow、Longbridge、36Kr、Hilo、KuCoin），原报告未见；Digitimes 2026-07-10 有付费墙只看到标题；Reuters 页面拒绝我的抓取（401），LEAP 2025 年数据来自搜索摘要。',
 '回测样本：设备月营收 2014–2026 共 153 个月，但只有约 6 个完整周期；合约负债只有 33 个季度、1 个完整周期。',
 '不构成投资建议。']
J['sources']=[
 (1,'KGI 2026-09-15：2027 AI chip outlook（CoWoS 产能、出货、AI 加速器预测）','https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/semiconductor-sector-_20260915_en.pdf'),
 (2,'UBS 2026-09-22（TechFlow 转述）：行业 CoWoS 2027 年末 270kwpm','https://www.techflowpost.com/en-US/newsletter/137464'),
 (3,'摩根士丹利 2026-09-13（Longbridge 转述）：台积电 130k/200k/260k','https://longbridge.com/en/topics/100000000898184'),
 (4,'摩根士丹利 2026-06-23（KuCoin 转述）：全球需求 1.394M→2.694M 片','https://www.kucoin.com/news/flash/morgan-stanley-report-tsmc-s-2027-ai-revenue-to-double-cowos-capacity-remains-a-bottleneck'),
 (5,'36Kr 转述摩根士丹利：分客户 CoWoS 需求','https://eu.36kr.com/en/p/3892020701149697'),
 (6,'Hilo 转述摩根大通：115K/155K/175K','https://www.xxquant.com/en/institution/institutional-research/16bdea7eb4987ae838d029976ec407bd'),
 (7,'Digitimes 2026-07-10：2027 年至少 20 万片（付费墙）','https://www.digitimes.com/news/a20260710PD226/tsmc-cowos-2027-packaging-capacity.html'),
 (8,'404K Research 2026-07-10：190–200kwpm 共识、英伟达 1,196–1,222k 片','https://404kresearch.substack.com/p/tsmc-cowos-capacity-allocation-update'),
 (9,'爱建证券 2026-05-12 先进封装设备点评（引 SemiAnalysis：H100 28 颗/片、B200 16 颗/片、中介层价值）','https://pdf.dfcfw.com/pdf/H3_AP202605121822218877_1.pdf?1778609220000.pdf='),
 (10,'Silicon Analysts：CoWoS 成本与 S/L/R 对比','https://siliconanalysts.com/analysis/cowos-packaging-cost-chiplet-vs-monolithic-2026'),
 (11,'TechNews 2026-04-10：摩根士丹利谈 Rubin Ultra、9× 光罩、EMIB-T','https://technews.tw/2026/04/10/tsmc-rubin-ultra-cowos-l/'),
 (12,'Hilo：CoWoS-L 与 SoIC 仍是关键变量','https://www.xxquant.com/en/institution/institutional-research/2365b6ed14516412f14dcd33cbc276c1'),
 (13,'FinmoConf：台积电 2Q26 法说会纪要（封装限制客户成长、测试机短缺、资本开支）','https://finmoconf.diveinvest.net/en/tsmc/2026-q2'),
 (14,'AI Prediction Index：魏哲家 4Q25 法说会原话（先进封装 2024 约 8%、2025 略超 10%、2026 低双位数）','https://www.aipredictionindex.com/p/wei-2026-advanced-packaging-low-teens-2026/'),
 (15,'StockAnalysis：台积电 2Q24 法说会逐字稿（先进封装毛利率接近公司平均）','https://stockanalysis.com/quote/tpe/2330/transcripts/185629-q2-2024/'),
 (16,'FinmoConf：日月光 2Q26 法说会纪要（LEAP、资本开支、面板线、ATM 毛利率）','https://finmoconf.diveinvest.net/en/ase/2026-q2'),
 (17,'Reuters 2025-02-13：日月光 2025 LEAP 16 亿美元（页面拒绝抓取，搜索摘要）','https://www.reuters.com/technology/taiwans-ase-sees-2025-advanced-packaging-testing-revenue-more-than-doubling-16-2025-02-13/'),
 (18,'Amkor 2Q26 财报','https://ir.amkor.com/news-releases/news-release-details/amkor-technology-reports-financial-results-second-quarter-2026'),
 (19,'台积电 CoWoS 技术页（The Chronicle of CoWoS）','https://www.tsmc.com/english/dedicatedFoundry/technology/CoWoS'),
 (20,'TrendForce 2026-03-18：SoIC 产能、Besi 受益','https://www.trendforce.com/news/2026/03/18/news-nvidia-rubin-ultra-and-feynman-reportedly-to-boost-tsmc-soic-besi-applied-materials-tel-to-benefit/'),
 (21,'TrendForce 2026-09-23：Intel EMIB 基板良率约 45%','https://www.trendforce.com/news/2026/09/23/breaking-intel-emib-substrate-yields-reportedly-hit-45-suppliers-eye-60-by-1q27/'),
 (22,"Tom's Hardware 2026-07-15：EMIB 受青睐、谷歌 TPU v9",'https://www.tomshardware.com/tech-industry/semiconductors/intels-emib-packaging-gains-traction-as-chip-designers-look-to-skirt-tsmcs-cowos-constraints-googles-reported-decision-for-9th-gen-tpus-highlights-intels-attractive-alternative'),
 (23,"Tom's Hardware 2026-03-09：T-glass 短缺，日东纺约 90%",'https://www.tomshardware.com/tech-industry/shortages-of-crucial-chip-packaging-material-threatens-ai-accelerator-supply-chains-nittobos-fukushima-plant-is-tripling-capacity-but-itll-take-years-before-market'),
 (24,'Digitimes 2026-08-14：T-glass 需求激增，载板短缺看到 2028（标题与摘要）','https://www.digitimes.com/news/a20260814PD224/demand-ic-substrate-2028-fiberglass-cloth-infrastructure.html'),
 (25,'Wccftech 2026-05-11：味之素 ABF 提价 30%，缺口延续到 2027','https://wccftech.com/msg-maker-ajinomoto-to-raise-prices-as-abf-substrate-supply-demand-gap-extends-to-2027/'),
 (26,'首尔经济 2026-08-11：台积电 CoPoS 产线完成','https://en.sedaily.com/international/2026/08/11/tsmc-completes-line-for-next-gen-copos-packaging-sees-year'),
 (27,'优分析 2026-09-17：弘塑订单看到 2030 年、交期 10–12 个月','https://uanalyze.com.tw/articles/7953455522'),
 (28,'工商时报 2026-04-08：弘塑、万润、均华、辛耘','https://www.ctee.com.tw/news/20260408700071-439901'),
 (29,'理财周刊 2026-08-19：万润、弘塑、辛耘合约负债','https://www.moneyweekly.com.tw/ArticleData/Info/Article/243680'),
 (30,'BigGo 2026-10-06：Disco 7–9 月出货创新高','https://finance.biggo.com/news/7d02eada-b120-4191-92ea-9a9702976288'),
 (31,'MOPS 月营收（经 FinMind 开放 API 下载：3131/3583/6187/3711/2330/3037/8046/3189 等）','https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue&data_id=3131&start_date=2012-01-01'),
 (32,'MOPS 季报（经 FinMind：毛利率、合约负债）','https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockFinancialStatements&data_id=2330&start_date=2022-01-01'),
 (33,'本站 HBM 小链（供给模型、每封装容量）','https://johnpeng-cn.github.io/chain-site/hbm.html'),
 (34,'TrendForce 2025-05：2026 年 HBM 出货超过 300 亿 Gb','https://www.trendforce.com/presscenter/news/20250522-12589.html'),
 (35,'台积电新闻稿：赛灵思 28nm CoWoS 量产','https://pr.tsmc.com/english/news/1792')]
J['sources']=[dict(id=a,t=b,u=c) for a,b,c in J['sources']]
J['changelog']=[['2026-10-15','v0.1','首版：按 SOP 11 节完成。供需滑块模型（出货 × 每片颗数）、季度产能、封装面积通胀、利润池与毛利率迁移、瓶颈排序、历史、设备月营收与合约负债回测、7 条预测、公司图谱、与 HBM 的接口对账。']]
json.dump(J,open('/workspace/chain_site/data/cowos.json','w'),ensure_ascii=False)
print('ok',len(json.dumps(J,ensure_ascii=False)))
