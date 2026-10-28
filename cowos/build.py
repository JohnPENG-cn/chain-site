"""CoWoS 链唯一构建脚本（v0.3 起，合并原 build_cowos.py + ext_v02.py + 只写进 JSON 的来源 41–43）。
输入：cowos_data/model_out.json（cowos/model.py 生成）、backtest.json、cl.json、margins.json、data/hbm.json（HBM 页供给，跨链对账用）。
输出：data/cowos.json，并刷新 data/toc.json 里依赖数字的文字。顺序：cowos/model.py → hbm/build.py → cowos/build.py（见 build.sh）。"""
import json,os,subprocess
R0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=lambda *a:os.path.join(R0,*a)
M=json.load(open(P('cowos_data','model_out.json')))
B=json.load(open(P('cowos_data','backtest.json')))
CL=json.load(open(P('cowos_data','cl.json')))
MG=json.load(open(P('cowos_data','margins.json')))
R=M['res']
# ---- 跨链：HBM 页 v0.4 供给（与 TOC、cowos.js 同一公式）
H=json.load(open(P('data','hbm.json')))
hsup=lambda y:sum(H['supply'][str(y)].values())*12*H['gbw'][str(y)]*H['ut'][str(y)]/1e6
HC=round(hsup(2027)/R['2027']['hbm']*100)          # 2027 HBM 满足率（可见出货口径）
CC=round(R['2027']['s']/R['2027']['d']*100)        # 2027 CoWoS 满足率（同一口径）
HS26,HS27=hsup(2026),hsup(2027)
S=lambda *a:','.join(map(str,a))
GOV=__import__('re').search(r"^GOV = '(.*)'$",open(P('cowos','page.py'),encoding='utf-8').read(),__import__('re').M).group(1)
J={}
J['meta']=dict(id='cowos',name='CoWoS 先进封装',version='v0.3',updated='2026-10-15',schema='chain/v1',
  unit='需求与产能用 12 寸 CoWoS 晶圆（片/月、片/年）；出货用颗（封装）；HBM 用 GB/EB。')
J['judgment']=dict(
 title=GOV,   # 中心思想只写在 cowos/page.py 一处（页面 h1、首页卡片、这里同一句）
 dek=f'CoWoS 产能三年涨了 9 倍，2027 年还要再涨约七成，总量缺口收窄到个位数。但封装越做越大，每片晶圆能封的芯片从 H100 的约 28 颗掉到 Rubin Ultra 的约 6 颗，<b>片数涨得比颗数快得多</b>；而 HBM、ABF 基板的扩产速度只有 CoWoS 的一半左右。HBM 页 v0.4 按券商产量重新校准后，HBM 供给比上一版高约五成：2027 年 HBM 够出货所需的约 {HC}%，CoWoS 约 {CC}%，两者都只略紧、差距在误差内；约束模型里最紧的是 ABF 载板（数据最弱，估）。',
 stats=[dict(id='cwHGap',n=f"{R['2027']['gap']:+.0f}%",l='2027 CoWoS 缺口/需求（可见出货口径）',tag='估'),
        dict(id='cwHHbm',n=f'约 {HC}%',l='2027 HBM 可供量 ÷ CoWoS 出货所需 HBM',tag='估'),
        dict(n='12 万→18.5 万',l='台积电 CoWoS 年末产能（片/月，2026→2027）',tag='源1'),
        dict(n='10–12 个月',l='弘塑设备交期；产能只够需求 1/3–1/4',tag='源27')])
J['debates']=[
 dict(q='Q1 2027 年 CoWoS 还会是 AI 芯片的头号瓶颈吗？',view=f'不会。总量缺口约 4%–11%；HBM 只够出货所需的约 {HC}%，和 CoWoS 差不多紧；约束模型里最紧的是 ABF/T-glass 基板（估）。',falsify='2027 年出现 HBM 或基板库存积压、而 CoWoS 订单仍排不进，或台积电 2027 年报仍称 CoWoS 是首要限制。'),
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
 dict(name='ABF 载板 / T-glass 玻纤布',now='日东纺约占 T-glass 90%，福岛扩产到 2027 年才放量；载板短缺看到 2028 年；味之素 ABF 膜提价 30%；KGI：2027 年 ABF 只 +25–30%',months=24,verdict='2027 头号短板（估）',src='23,24,25,1'),
 dict(name='HBM（跨链：见 HBM 页）',now=f'KGI：2027 年 HBM 供给 +45–50%，CoWoS +71%；按本页出货口径 2027 需 HBM 约 {R["2027"]["hbm"]:.1f} EB，HBM 页 v0.4 模型供给约 {HS27:.1f} EB（够 {HC}%）',months=36,verdict='与 CoWoS 并列偏紧',src='1,33'),
 dict(name='封装设备交付',now='弘塑交期 10–12 个月，2026 年出机 220–240 台、2027 年约 325 台，只够需求 1/3–1/4',months=12,verdict='决定扩产速度',src='27'),
 dict(name='测试机与测试产能',now='台积电 2Q26 法说会：测试机也短缺，资本开支在测试/封装间移动',months=9,verdict='容易被忽视',src='13'),
 dict(name='CoWoS-S / R 结构性缺口',now='KGI：S、R 型产能都缺，博通 2027 指引 50 万片只能排进 38–39 万；R 型被 Vera CPU 占满',months=12,verdict='总量够、型号不够',src='1'),
 dict(name='台积电 CoWoS 总产能',now='12 万（2026 年末）→ 18.5–20 万（2027 年末），缺口从 30–35% 收窄到 15–20%（对客户需求）',months=15,verdict='2027 年缓解',src='1,3'),
 dict(name='超大中介层翘曲 / 9× 光罩',now='9× 光罩 CoWoS-L 还要解决翘曲、成本与良率',months=18,verdict='下一代变量',src='11')]
J['history']=dict(
 tl1=[['2011–12','CoWoS 首个产品：赛灵思 Virtex-7 2000T（28nm）','19,35'],['2016','英伟达 GP100 用 CoWoS + HBM2；同年 InFO 量产（苹果 A10，公认史实）','19'],['2017–18','Intel EMIB 首批产品（Stratix 10、Kaby Lake-G，公认史实）','—'],['2019–20','中介层从 1× 到 2× 光罩以上；A100 用 CoWoS-S','19'],['2022','SoIC 首个量产（AMD 3D V-Cache，公认史实）','—'],['2024','CoWoS-L 量产（B200），突破硅中介层约 2,700mm² 上限','10'],['2026','5.5× 光罩；CoPoS 试产线建成；谷歌 TPU v9 选 EMIB-T','26,1'],['2027','9× 光罩 CoWoS-L；日月光 310mm 面板线 1Q27 投产','11,16'],['2028–29','CoPoS 起量（KGI：2029 年才有意义贡献）；玻璃基板','1,26']],
 tl2=[['2023','ChatGPT → H100 缺货，瓶颈就是 CoWoS 产能本身（年末约 1.3 万片/月）','1'],['2024','产能翻 2.6 倍到 3.4 万片；先进封装约占台积电营收 8%','1,14'],['2025','7.2 万片；先进封装占比略超 10%；日月光 LEAP 16 亿美元','1,14,17'],['2026','12 万片；"封装产能紧到限制客户成长"；设备交期 10–12 个月；载板毛利率翻倍','13,27,32'],['2027E','18.5–20 万片；CoWoS +71% 快于 ABF（+25–30%）和 HBM（+45–50%）→ 短板移到元件','1']],
 rule='每轮扩产后，瓶颈会移到扩得最慢的相邻环节，利润也跟着走（克里斯坦森"利润守恒"）：2023 年在 CoWoS 产线，2026 年开始移到设备交付和载板（欣兴毛利率一年翻倍），2027 年移到载板和 HBM。')
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
 'HBM 页 v0.4（2026-10-15）把 HBM 供给上修约五成（每片有效 GB 600–650 → 750–880，年末产能改用 UBS 口径），本页 2027 年 HBM 满足率随之从约 61% 变为约 '+str(HC)+'%，短板判断由"HBM"改为"载板（估）+ HBM 略紧"。',
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


# ===== v0.2 扩展：要害变量、玩家、证伪、需求上一层 =====
j=J
S=j['sources'];ids={s['id'] for s in S}
new=[(36,'NVIDIA CFO Commentary Q2 FY2027（SEC 8-K 附件）：供应与产能承诺 1,190 亿 → 2,790 亿美元，主要为存储；库存 258 → 316 亿美元','https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm'),
 (37,'Datacentres.com：四大云厂商 2026 年资本开支指引（7 月财报，引各公司电话会）','https://www.datacentres.com/guides/hyperscaler-capex-trends'),
 (38,'CRN 2026-07：AWS/微软/谷歌云 Q2 2026 营收、增速、营业利润','https://www.crn.com/news/cloud/2026/aws-vs-microsoft-vs-google-cloud-earnings-q2-2026-face-off'),
 (39,'Midgard Finance：云业务季度营收、积压订单（RPO）、资本开支、AWS 资产回报（取自各公司财报）','https://www.midgardfinance.com/research/cloud/'),
 (40,'Reuters 2026-07-30：亚马逊上调资本开支，Jassy 称 2026、2027 年算力都不够（页面拒绝抓取，搜索摘要）','https://www.reuters.com/business/retail-consumer/amazon-beats-estimates-quarterly-cloud-revenue-growth-2026-07-30/')]
for i,t,u in new:
  if i not in ids:S.append({'id':i,'t':t,'u':u})
# 需求上一层：季度资本开支（百万美元）与积压订单（十亿美元），源39
Q=['2023Q1','2023Q2','2023Q3','2023Q4','2024Q1','2024Q2','2024Q3','2024Q4','2025Q1','2025Q2','2025Q3','2025Q4','2026Q1','2026Q2']
j['driver']={'q':Q,
 'capex':{'亚马逊':[14207,11455,12479,14588,14925,17620,22620,27834,25019,32183,35095,39522,44203,54208],
          '微软':[6607,8943,9917,9735,10952,13873,14923,15804,16745,17079,19394,29876,30876,35802],
          '谷歌':[6289,6888,8055,11019,12012,13186,13061,14276,17197,22446,23953,27851,35674,44924]},
 'backlog':{'亚马逊':[122.0,132.1,133.0,155.7,157.7,156.6,164.0,177.0,189,195,200,244,364,496],
            '微软':[196,224,212,222,235,269,259,298,315,368,392,625,627,678],
            '谷歌云':[61.7,60.6,64.9,74.1,72.5,78.8,86.8,93.2,92.4,108.2,157.7,242.8,462.3,513.9]},
 'facts':[['2026 年资本开支指引（四大云厂商）','约 7,200–7,450 亿美元：亚马逊约 2,200、谷歌 1,950–2,050、微软约 1,750、Meta 1,300–1,450；年内每家都上调或维持','37'],
  ['AI 回报：云业务 Q2 2026','AWS 营收 422 亿美元 +37%、营业利润 166 亿；谷歌云 248 亿 +82%、营业利润 88 亿（利润率 35.6%）；微软智能云 393 亿 +32%','38,39'],
  ['积压订单（已签未确认）','三家合计约 1.69 万亿美元；亚马逊 Q1、Q2 各有约 1,000 亿来自 OpenAI、Anthropic','39'],
  ['反方：AWS 资产回报在下降','AWS 过去 12 个月营业利润 ÷ 期末固定资产 = 21%，一年前 30%；新增固定资产已等于营收的 101%','39'],
  ['英伟达数据中心营收','Q2 FY27 890 亿美元，同比 +117%；Q3 指引总营收 1,080 亿美元','36'],
  ['亚马逊：算力仍不够','Jassy：即使 2,200 亿美元，2026 年仍不够满足需求，2027 年也会如此（Reuters 搜索摘要）','40']]}
j['players']=[
 {'who':'台积电','role':'供给方·定价者','incentive':'保护先进封装毛利率（已接近公司平均）[源15]，不想重演过剩；但大客户逼着扩产。',
  'now':'连续上调 CoWoS 扩产计划：2026 年末 12 万 → 2027 年末 18.5–19 万片/月，2028 年再加 4–5 万；把溢出订单交给日月光、Amkor，自己留 CoWoS-L 大单 [源1]。CoPoS 2028 年起量 [源1]。',
  'history':'2023–2026 年每年都比年初计划多扩（KGI 称"continues to revise up"）[源1]；扩产主要跟着英伟达的确定订单走，不做投机性产能。',
  'signal':'法说会不再说"封装限制客户成长"[源13]，或年末产能目标第一次下调；资本开支中先进封装占比下降。'},
 {'who':'英伟达','role':'最大买家','incentive':'把出货量最大化、锁住稀缺零部件，挤压竞争对手可用的产能。',
  'now':'一个季度内把供应与产能承诺从 1,190 亿美元加到 2,790 亿美元，主要是存储 [源36]；为最大化出货下调 HBM 规格、提价 15% 转嫁成本；Vera CPU 60% 给台积电和日月光、其余给 Amkor（多家供应）[源1]。',
  'history':'2023–24 年 CoWoS 紧缺时包下台积电大部分产能，并把 oS 后段外包给 OSAT（行业共识，未单独核实）；库存在新架构前上升（Q2 FY27 库存 258 → 316 亿美元，为 Vera Rubin 备货）[源36]。',
  'signal':'供应承诺环比下降或出现取消；库存天数持续上升而营收增速放缓；继续下调每封装 HBM 容量（说明 HBM 比 CoWoS 紧）。'},
 {'who':'谷歌 / 博通 / 联发科','role':'ASIC 阵营','incentive':'不被单一供应商卡脖子：设计伙伴、封装路线都要有第二来源。',
  'now':'TPU v9（Humufish）采用 Intel EMIB-T，理由是美国本土化、9 倍光罩大尺寸和台积电产能不足；联发科做 I/O；明显贡献要到 2Q28 [源1]。博通 2027 年要 50 万片 CoWoS，只能排进 38–39 万 [源1]。',
  'history':'TPU 长期只给博通设计；2026 年起对外部客户（Anthropic）出售或租赁 TPU [源1]。',
  'signal':'EMIB-T 良率（基板良率约 45%，供应商目标 1Q27 到 60%）[源21]；谷歌是否把第二代产品也放到 EMIB。'},
 {'who':'日月光 / Amkor','role':'第二供给方','incentive':'从"做 oS 后段"升级成"全流程 CoWoS 第二来源"，拿溢出订单和 CPU 订单。',
  'now':'日月光全流程 CoWoS 2 万 → 4.5 万片/月（+125%），拿到约一半 Vera CPU 和大部分 Venice CPU；Amkor 1.5 万 → 2.5 万片/月 [源1]。LEAP 营收 2026 年超过 35 亿美元 [源16]。',
  'history':'2023–24 年承接台积电外包的 oS 后段；扩产比台积电保守，靠客户确定订单。',
  'signal':'日月光资本开支指引下调，或 LEAP 增速明显低于 CoWoS 总产能增速。'},
 {'who':'Intel','role':'挑战者','incentive':'用 EMIB/Foveros 把代工业务带起来，吃美国本土化需求。',
  'now':'为了让基板供应商优先配合，Intel 甚至"必须预付款"[源21]。',
  'history':'EMIB 2017–18 年就量产，但一直以自家产品为主（公认史实）。',
  'signal':'出现月产万颗以上的外部 AI 加速器订单（见预测 C6）。'},
 {'who':'设备与材料商（弘塑、日东纺、味之素等）','role':'上游卡点','incentive':'扩得慢、延长交期、提价，而不是追着需求大扩产。',
  'now':'弘塑交期 10–12 个月、订单排到 2030 年 [源27]；味之素 ABF 提价 30% [源25]；日东纺 T-glass 扩产 2027 年才放量 [源23]。',
  'history':'上一轮周期被伤过：载板三家营收 3 个月同比在 2023-11 跌到 −36%（本站回测，源31），所以这次扩产克制。',
  'signal':'载板厂/材料商宣布大幅扩产或降价；欣兴毛利率掉头（现在 24.8%）[源32]。'},
 {'who':'云厂商（亚马逊、谷歌、微软、Meta）','role':'需求的上一层','incentive':'抢 AI 算力份额；只要云收入和积压订单还在涨，就不会减资本开支。',
  'now':'2026 年资本开支指引合计约 7,200–7,450 亿美元，年内都上调过 [源37]；云业务 Q2 增速 32%–82% [源38]。',
  'history':'2022–23 年云增速放缓时，亚马逊资本开支从季度 166 亿美元降到 115 亿美元（2022Q4 → 2023Q2）[源39]，这是上一次"需求上一层"收缩。',
  'signal':'任何一家下调资本开支指引；云业务增速连续两季放缓；AWS 资产回报继续下降（已从 30% 降到 21%）[源39]。'}]
j['falsify']=[
 {'j':'J1 2027 年 CoWoS 不再是头号瓶颈','counter':'KGI 仍估台积电对"客户需求"缺口 15–20%，S/R 型都缺 [源1]；2025–26 年本模型显示总量富余，但市场普遍说紧，说明模型可能低估了需求。',
  'falsify':'2027 年 CoWoS 订单仍大量排不进，同时 HBM 和基板没有出现缺货迹象。','ind':'券商对台积电 2027 年 CoWoS 缺口的口径；台积电法说会措辞','th':'2027 年中缺口口径 ≥ 25%，或台积电 2027 年末产能 < 16 万片/月','now':'15–20%（KGI）；年末 18.5–19 万 [源1]','st':'ok'},
 {'j':'J2 2027 年 HBM 略紧于 CoWoS（不再是唯一短板）','counter':f'HBM 页 v0.4 已按券商产量上修供给：2026 年 {HS26:.1f} EB，高于本页按出货算的需求 {R["2026"]["hbm"]:.1f} EB；2027 年 HBM 够 {HC}%、CoWoS 够 {CC}%，差距在误差内，结论很容易翻转 [源33]。',
  'falsify':'2027 年 HBM 合约价涨幅很小，或英伟达不降规格。','ind':'2027 年 HBM 混合均价；Rubin Ultra 每封装 HBM 容量','th':'均价同比 < +30%，或 Rubin Ultra ≥ 512GB','now':'TrendForce 预测 2027 年混合均价 +121%（HBM 页源36）；KGI 称英伟达在下调 HBM 规格 [源1]','st':'ok'},
 {'j':'J3 利润往载板迁移','counter':'欣兴毛利率含非 ABF 业务；毛利率跳升可能部分来自一次性因素。','falsify':'载板毛利率回落，而台积电/OSAT 毛利率继续上升。','ind':'欣兴（3037）季度毛利率','th':'连续两季 < 20%','now':'2Q26 24.8%（一年前 13.1%）[源32]','st':'ok'},
 {'j':'J4 需求上一层（云厂商资本开支）继续上修','counter':'AWS 资产回报已从 30% 降到 21%，新增固定资产等于营收的 101% [源39]；资本开支增长有一部分是存储涨价，不是更多算力 [源37]。',
  'falsify':'云厂商 2027 年资本开支指引持平或下降。','ind':'四大云厂商 2027 年首次资本开支指引（2027 年 1–2 月财报）','th':'合计同比 < +10%，或任一家下降','now':'2026 年约 7,325 亿美元（中值）；谷歌、微软都说 2027 年继续增长 [源37]','st':'watch'},
 {'j':'J5 封装周期还没见顶','counter':'设备三家营收同比已到 +43%，历史上这个位置之后几个月常见顶。','falsify':'设备三家营收同比见顶回落。','ind':'弘塑+辛耘+万润 3 个月营收同比（每月 10 日 MOPS）','th':'从峰值回落 ≥ 20 个百分点并连续 3 个月下行 → 按回测约 4 个月后台积电营收同比见顶','now':'2026-09 +43%，仍在上升 [源31]','st':'ok'}]
j['tornado_note']='要害变量：① 每片可封颗数（面积通胀）——只有 H100、B200 两个公开锚点，其余是估；② HBM 可供量——两条链的结论都取决于它。研究时间主要花在这两个变量上。'
if not any(p['id']=='C8' for p in j['predictions']):
  j['predictions'].append({'id':'C8','text':'四大云厂商（亚马逊、谷歌、微软、Meta）首次给出的 2027 年资本开支指引合计 ≥ 8,500 亿美元（2026 年中值约 7,325 亿，+16%）','due':'2027-02-15','check':'各公司 4Q26 财报电话会','status':'pending'})
j['meta']['version']='v0.3'   # 修正：合并旧 ext_v02 时遗留，曾把版本写回 v0.2
cl=j['changelog']
if not any(c[1]=='v0.2' for c in cl):cl.insert(0,['2026-10-15','v0.2','新增：要害变量龙卷风图、关键玩家与博弈、反方证据/证伪条件表、需求上一层（云厂商资本开支、积压订单、AI 回报），预测 C8。'])


# ===== v0.3 =====
S=J['sources'];ids={x['id'] for x in S}
for i,t,u in [(41,'电子新闻 ETNews 2025-07-30：韩美半导体 TC 键合机月产能 35 台，2026 年扩到 45 台；HBM3E 12 层用 TC 键合机份额 90% 以上','https://www.etnews.com/20250730000336'),
 (42,'亚洲经济 2024-07-05：韩美半导体年产 264 台（月 22 台）TC 键合机','https://www.asiae.co.kr/en/article/2024070519155971905'),
 (43,'The Elec 2025-03-14：SK 海力士 2025 年计划采购约 80 台 TC 键合机，每条 HBM 线 2 台','https://www.thelec.net/news/articleView.html?idxno=5189')]:
  if i not in ids:S.append({'id':i,'t':t,'u':u})
if not any(c[1]=='v0.3' for c in cl):cl.insert(0,['2026-10-15','v0.3',f'跟随 HBM 页 v0.4 重新校准：HBM 供给上修约五成，2027 年 HBM 满足率约 61% → 93%；结论由"短板是 HBM"改为"最紧是 ABF 载板（估），HBM 与 CoWoS 都只略紧"。CoWoS 与 HBM 满足率改为同一口径（可见出货）比较。构建合并为 cowos/build.py（重跑不丢来源 41–43）。'])
if not any(c[1]=='v0.3 · 版式' for c in cl):cl.insert(0,['2026-10-15','v0.3 · 版式','页面改为与 HBM 页同一模板：上半结论层（SCQA、中心思想、3 条论点：量 / 利润 / 时点，证据卡、可能错在哪、预测台账），下半底稿按 SOP 13 步全部展开；证据卡与底稿步骤双向链接；约束迁移预测 T 系列移入预测台账。<b>数字未改</b>；修正 data/cowos.json 版本号（曾被旧扩展代码写回 v0.2）。'])
if not any(c[1]=='v0.3.1' for c in cl):cl.insert(0,['2026-10-15','v0.3.1',f'跟随 HBM 页 v0.5：长鑫产能移到 HBM 页的中国账本（只能卖给中国，KGI 出货表里也没有国产卡），不再计入全球 HBM 供给；2027 年 HBM 满足率约 93% → {HC}%，CoWoS 结论不变。'])
# ===== v0.4 中国账本（SOP v1.5 两本账）：国产 AI 卡要用、只能在大陆做的 2.5D 封装。公式与 cowos_cn.js 一致 =====
CN=json.load(open(P('cowos','cn.json'),encoding='utf-8'))
HB={r['y']:r for r in H['cn']['bal']}   # HBM 页中国账本（hbm/build.py 先跑）
def cwcn(m,o={}):
  cap={**m['cap'],**{k:v for k,v in o.get('cap',{}).items()}};ai=o.get('ai',m['ai']);ut=o.get('ut',m['ut']);pk=o.get('ppw',1.0);out=[]
  for y in (2025,2026,2027):
    k=str(y);pw=m['ppw'][k]*pk;npr=m['npr'][k];h=HB[y]
    s=(cap[str(y-1)]+cap[k])/2*12*ai*ut;u=h['u'];hc=min(h['cards'],u)
    du=(u+npr)/pw*1000;dh=(hc+npr)/pw*1000
    out.append(dict(y=y,s=round(s,1),du=round(du,1),dh=round(dh,1),cov=round(s/du,4),covh=round(s/dh,4),ppw=pw,cards=round(s*pw/1000,3),hcards=round(hc+npr,3)))
  return out
CN['bal']=cwcn(CN['model'])
S=J['sources'];ids={x['id'] for x in S}
for i,t,u in CN.pop('sources'):
  if i not in ids:S.append({'id':i,'t':t,'u':u})
J['cn']=CN
for i,t,u in [(63,'톱스타뉴스 2026-10（汇总韩国券商）：키움증권估 CoWoS 产能 12 万 → 15 万片/月，HBM 2027 年需求 +56%、产量 +50%','https://www.topstarnews.net/news/articleView.html?idxno=16160242')]:
  if i not in {x['id'] for x in S}:S.append({'id':i,'t':t,'u':u})
_ids={x['id'] for x in S};_bad=sorted({int(n) for n in __import__('re').findall(r'源(\d+)',json.dumps(CN,ensure_ascii=False)+open(P('cowos','page.py'),encoding='utf-8').read()) if int(n) not in _ids})
assert not _bad,f'CoWoS 中国账本引用了不存在的来源 {_bad}'
J['meta']['version']='v0.4'
if not any(c[1]=='v0.4' for c in cl):cl.insert(0,['2026-10-15','v0.4','新增中国账本（SOP v1.5 两本账）：国产 AI 卡只能在大陆做的 2.5D 封装。台积电通道 2024-11 / 2025-01 关闭；按 HBM 页中国账本能配的卡算，2026 年国产 2.5D 和 HBM 一样紧，2027 年国内产能翻倍后让位给 HBM；ABF 膜是下一个卡点（数据弱）。新增来源 44–62、预测 N1–N5、证伪 CJ1–CJ3。产能数字主要来自调研纪要，标为弱证据。'])
if not any(c[1]=='v0.4.1' for c in cl):cl.insert(0,['2026-10-15','v0.4.1','页面最上方新增"逻辑层"（SOP v1.6）：三个问题（全球 + 中国）、三句话逻辑、一张图看懂、主流观点 vs 我们（新增来源 63：韩国券商口径）、我们重点盯什么。数字不变。'])
# ===== v0.4.2 台积电 3Q26 法说会（2026-10-15）：J1 观察项更新，数字不变 =====
for i,t,u in [(64,'钜亨网 2026-10-15：台积电 3Q26 法说会，魏哲家称"后段产能确实有些短缺"（7 月法说会措辞为"先进封装仍严重供不应求"）；与格罗方德签 5 年约 20 亿美元协议，在美国纽约州生产 CoWoS 用硅中介层，2028 年上半年放量；已量产 5 倍光罩封装，推进 9 倍、14 倍与 CoPoS；表示愿为采用对手封装方案的客户做备援','https://news.cnyes.com/news/id/6631199')]:
  if i not in {x['id'] for x in S}:S.append({'id':i,'t':t,'u':u})
for f in j['falsify']:
  if f['j'].startswith('J1'):
    f['now']='15–20%（KGI）；年末 18.5–19 万 [源1]；台积电 3Q26 法说会措辞从 7 月"严重供不应求"降为"后段产能确实有些短缺"，并把部分硅中介层外包给格罗方德（2028 上半年放量）[源64]'
if not any(c[1]=='v0.4.2' for c in cl):cl.insert(0,['2026-10-16','v0.4.2','台积电 3Q26 法说会（10-15）：J1 观察项更新（封装短缺措辞由"严重供不应求"降为"确实有些短缺"，方向支持"2027 年 CoWoS 只略紧"；硅中介层部分外包格罗方德，2028 上半年放量），新增来源 64。数字不变。'])
# ===== v0.4.3 硅中介层单独成一环（John 2026-10-16 批准）：model.py 算需求/供给，toc.js 换成"百万颗封装/季" =====
IP=M['ip'];IR=IP['res'];g=lambda y,k:IR[str(y)][k]
for i,t,u in [
 (65,'经济日报 2025-12-02（转述摩根士丹利）：台积电扩建 65nm 中介层产能每月 2 万片、主要给 CoWoS-S（推估终端为谷歌 TPU）；博通 CoWoS-S 订单 15.5 万 → 20 万片；英伟达 Spectrum 增加 CoWoS-S 约 5,000 片/月','https://money.udn.com/money/story/11162/9176309'),
 (66,'财联社 2026-06-25（转述摩根士丹利）：台积电把 Fab 15A 部分 28/22nm 空间改成 55nm 中介层；博通 TPU v7+v8i 约 34.3 万片 CoWoS-S、联发科 18 万片 CoWoS-S（TPU v8t）；AMD 在台积电 CoWoS-L 24 万片；非台积电扩产集中在 L、R 型','https://finance.sina.com.cn/roll/2026-06-25/doc-inierpqn0965351.shtml'),
 (67,'格罗方德新闻稿 2026-10-08：与台积电签 5 年约 20 亿美元协议，在纽约 Malta 为 CoWoS 生产硅中介层（含嵌入式深沟槽电容），2028 年上半年开始放量','https://investors.gf.com/news-releases/news-release-details/globalfoundries-reaches-agreement-establish-us-based-supply'),
 (68,'TrendForce 2026-10-12：中介层一般用 65/90nm 成熟工艺，外包可腾出 12 寸产能；联电中介层 3,000 → 6,000 片/月，并给 Intel EMIB 供硅桥；力积电供 EMIB 硅电容','https://www.trendforce.com/news/2026/10/12/news-tsmcs-2b-silicon-interposer-deal-with-gf-could-fast-track-u-s-packaging-to-1h28-free-up-fab-capacity/'),
 (69,'民视财经/财讯 2026-05-29：联电财务长称硅中介层产能已由 3,000 片提升至 6,000 片/月，后续是否扩产视客户需求而定','https://finance.ftvnews.com.tw/news/detail/2026529W0248'),
 (70,'TrendForce 2023-08-25（转述工商时报）：2023 年 CoWoS 扩产的关键卡点是硅中介层不足；联电 3k 片/月，翻倍到 6k（最早 1Q24），并评估 10k','https://www.trendforce.com/news/2023/08/25/news-nvidia-establishes-non-tsmc-cowos-supply-chain-umc-doubles-interposer-capacity/'),
 (71,'优分析 2026-10-12：台积电已把部分硅中介层交给世界先进；VSMC（新加坡）把中介层纳入产品，2027Q1 量产、2029 年满载 4.4 万片/月（全厂，非全为中介层），尚未确认承接台积电订单','https://uanalyze.com.tw/articles/2073056855'),
 (72,'经济日报 2026-10-12：法人认为台积电为确保中介层产能无虞而扩大委外；联电、力积电扩中介层','https://udn.com/news/story/7240/9808153'),
 (73,'TrendForce 2026-09-18：CoWoS-S 最多 2 颗 SoC + 8 颗 HBM，Maia 200 仍用 S；英伟达、AMD、Meta MTIA 400 已用 CoWoS-L，AWS、微软 2027 年转 L；谷歌 2027 年导入 EMIB-T','https://www.trendforce.com/presscenter/news/20260918-13241.html'),
 (74,'TrendForce 2026-05-21：AMD 与日月光/矽品开发晶圆级 2.5D 硅桥 EFB，用于 Venice CPU；与力成验证面板级 EFB','https://www.trendforce.com/news/2026/05/21/news-amds-lisa-su-reportedly-to-visit-tsmc-for-2nm-capacity-announces-us10b-taiwan-ai-packaging-investment/'),
 (75,'武汉新芯招股说明书（上交所 2025-09-29）：2.5D 硅转接板（Interposer）平台已规模量产；募投 12 寸线 5 万片/月，其中三维集成（含 2.5D）4 万片/月','https://static.sse.com.cn/stock/disclosure/announcement/c/202509/002044_20250929_SM99.pdf'),
 (76,'财联社 2026-08-13：中芯国际 2Q26 月产能 109.65 万片（折合 8 寸），产能利用率 93.7%','https://finance.sina.com.cn/jjxw/2026-08-13/doc-inineqhh4636728.shtml'),
 (77,'工商时报 2026-08-12：台积电副总何军称 CoWoS 已量产 5.5 倍光罩、多项产品良率 >98%；点名未来数年短缺的是存储和 ABF 载板','https://www.ctee.com.tw/news/20260812700094-439901'),
 (78,'TVBS 2026-07-14：力积电法说会称 CoWoS 供不应求，硅中介层"有订单外溢"，新竹中介层产线已复线量产','https://news.tvbs.com.tw/tech/3257362')]:
  if i not in {x['id'] for x in S}:S.append({'id':i,'t':t,'u':u})
J['ip']=dict(rows=[[y,g(y,'sw') if y<2028 else None,g(y,'need') if y<2028 else None,g(y,'cap'),g(y,'ts'),g(y,'umc'),g(y,'oth_s'),g(y,'sup'),g(y,'gap') if y<2028 else None] for y in range(2024,2029)],
  x=IP['x'],be27=IP['be27'],be28=IP['be28'],br=IP['br'],eff=IP['eff'])
J['variants'][0][4]='成熟主力；KGI 称 S 型产能 2027 仍紧；整片硅中介层由台积电自制 + 联电/世界先进/力积电，2028 起加格罗方德'
J['variants'][0][5]='10,1,67'
J['process'][0][2]='台积电自制（65/55nm 级，Fab 15A 部分改产，源66）+ 委外：联电约 6,000 片/月、世界先进、力积电，2028 上半年起格罗方德纽约厂；L 型硅桥同样由台积电做。CoWoS-S 中介层每片价值约 1 万美元、L 型约 1.5 万美元'
J['process'][0][3]='10,9,66,67,69,71'
if not any(n['name'].startswith('硅中介层') for n in J['neck']):
  J['neck'].insert(4,dict(name='硅中介层（只卡 S 型）',now=f"2026 年余量约 {g(2026,'gap'):+.0f}%，2027 年约 {g(2027,'gap'):+.0f}%（估）：S 型需求 +{(g(2027,'need')/g(2026,'need')-1)*100:.0f}%（谷歌 TPU），台积电 2027 年要再加约 {IP['be27']:.1f} 千片/月才不缺；格罗方德 2028 上半年才放量",months=18,verdict='2027 年和 S 型需求打平，不是总约束',src='65,66,67,69'))
if not any(f['j'].startswith('J6') for f in J['falsify']):
  J['falsify'].append({'j':'J6 硅中介层 2027 年只和 S 型需求打平，不是总约束；2028 年转松','counter':f"中介层产能没有任何公司披露：台积电 2024–25 年自制量是按“2025 年多 10%”反推的（估），2027 年新增 2 万片/月是假设；格罗方德协议、世界先进接单、法人说“为确保产能无虞而扩大委外” [源67,71,72]，都说明台积电自己觉得偏紧",
   'falsify':'2027 年谷歌 TPU（CoWoS-S）出货被下修、原因指向中介层；或台积电/券商把中介层列为 CoWoS-S 的首要限制',
   'ind':'① 券商对博通+联发科 2027 年 CoWoS-S 片数（MS 现为 34.3 万 + 18 万）；② 台积电 2027 年中介层自制新增；③ 新的中介层委外签约',
   'th':f"① 下修 ≥ 10% 且归因中介层；② 新增 < {IP['be27']:.0f} 千片/月（盈亏平衡）；③ 2027 年内再出现一家新委外厂或联电扩到 ≥ 1 万片/月 → 都说明比我们算的紧",
   'now':'台积电 2026 年 +2 万片/月 [源65]、Fab 15A 部分改产 [源66]；联电 6,000 片/月 [源69]；格罗方德 2028 上半年 [源67]；台积电点名的短缺是存储和 ABF 载板 [源77]','st':'watch'})
if not any(p['id']=='C9' for p in J['predictions']):
  J['predictions'].append({'id':'C9','text':'2027 年内没有主流券商或台积电把"硅中介层"列为 CoWoS 出货的首要限制（我们判断 2027 年中介层只和 S 型需求打平，首要限制仍在载板/HBM）','due':'2027-12-31','check':'台积电法说会；KGI/MS/TrendForce','status':'pending'})
  J['predictions'].append({'id':'C10','text':'格罗方德 Malta 中介层 2028-06-30 前开始量产出货（新闻稿口径"2028 上半年放量"）','due':'2028-08-15','check':'格罗方德 2Q28 财报','status':'pending'})
J['limits'].insert(5,f"硅中介层（v0.4.3）：没有公司披露中介层产能。需求是第一性原理换算（1 片 CoWoS-S = 1 片中介层），较可靠；供给只有增量有来源（台积电 2026 +2 万、联电 6,000、格罗方德 2028），台积电 2024–25 年自制约 {IP['x']:.0f} 千片/月是按“2025 年多 10%”反推的，2027 年新增 2 万是假设（盈亏平衡 {IP['be27']:.1f} 千片）。CoWoS-L 硅桥按每片 {IP['br']} 片硅折算（LSI 面积未公开）。")
if 'cn' in J and not any(r[0].startswith('硅中介层') for r in J['cn']['toc']):
  J['cn']['toc'].insert(3,['硅中介层（TSV 转接板）','不少于 2.5D 封装产能','65/55nm 级成熟工艺 [源68]，不在 16/14nm 以下的管制线内 [源44]；武汉新芯 2.5D 硅转接板已规模量产、募投三维集成（含 2.5D）4 万片/月 [源75]；中芯月产能 109.65 万片（8 寸约当）[源76]；盛合部分 TSV 转接板由客户供料 [源51]。国内 2.5D 2026 年底约 2.3 万片/月，最多也就要这么多中介层','不是约束（估）'])
J['meta']['version']='v0.4.3';J['meta']['updated']='2026-10-16'
if not any(c[1]=='v0.4.3' for c in cl):cl.insert(0,['2026-10-16','v0.4.3',f"硅中介层单独成为约束推导的一环（John 批准）：1 片 CoWoS-S = 1 片良品中介层，L/EFB 只算硅桥；改正 2027 年 AMD MI450/455 为 CoWoS-L、Venice 为 EFB 硅桥（源66,74，不影响 CoWoS 片数）。结论：中介层 2026 年余量约 {g(2026,'gap'):+.0f}%，2027 年约 {g(2027,'gap'):+.0f}%，只卡谷歌 TPU 等 S 型、不改变总约束；2028 年格罗方德/世界先进放量后，需求涨 {IP['be28']:.0f}% 以内都不缺（估）。中国账本：中介层不是约束。新增来源 65–78、证伪 J6、预测 C9–C10。核心判断不变。"])
for r in CN['bal']:print('中国 2.5D',r['y'],'供给 %.0f 千片 / 不缺货需求 %.0f / HBM 能配需求 %.0f，覆盖 %.0f%%（%.0f%%），能封 %.2fM 张 vs HBM 能配 %.2fM'%(r['s'],r['du'],r['dh'],r['cov']*100,r['covh']*100,r['cards'],r['hcards']))
# ===== 2026-10-28 页面拆成 5 页（只是版式，模型和判断不变）=====
if not any(c[0]=='2026-10-28' for c in cl):cl.insert(0,['2026-10-28','5 页版式','CoWoS 拆成和 PCB 同一套 5 页模板：总览（一分钟看懂 + 五句话 + 一张图 + 三个信号 + 三条证伪）、格局与钱在哪赚、周期与产能、主要矛盾追踪、底稿与数据；左侧整站导航（解释页并入导航树）、每页目录、上一页 / 下一页；节标题改成短问句；正文里的版本号说明（v0.4 / v0.4.2 / v0.4.3）改成中性说法，版本细节留在本表。只搬内容、不删数字；判断、证伪条件、预测台账、模型数字未改。旧网址 cowos.html#锚点 自动跳到新页。'])
json.dump(J,open(P('data','cowos.json'),'w'),ensure_ascii=False,separators=(',',':'))
# ---- 刷新 toc.json 中依赖数字的文字（用 toc.js 同一套算法）
T=json.load(open(P('data','toc.json')))
if not any(x['k']=='ip' for x in T['stages']):
    T['stages'].insert(1,{'k':'ip','n':'硅中介层','c':'#c2185b','native':'','conv':''})
for x in T['stages']:
    if x['k']=='ip': x['native']=f"中介层投片 千片/月（季末）：台积电自制（2024–25 年约 {IP['x']:.0f} 千片，按“2025 年最紧一季仍多 10%”反推，估；2026 年 +2 万 {{ipms}}；2027 年 +2 万，估，Fab 15A 改产 {{ipfab}}）+ 联电 6 千 {{ipumc}} + 世界先进/力积电（2027 年 2 千，估）{{ipvis}}"
    if x['k']=='ip': x['conv']=f"× 3 × 稼动率 95% × 良率 97%（估）→ 良品片/季；先扣 L/EFB 硅桥（每片 {IP['br']} 片硅，估）和交换芯片用量，剩下的 × S 型每片颗数（2026 年 {g(2026,'su')/g(2026,'sw')*1000:.1f}、2027 年 {g(2027,'su')/g(2027,'sw')*1000:.1f} 颗）= 能封的 S 型颗数；L/R 型不用整片中介层，直接通过 <span class=\"tag t-est\">估</span>"
T['srcmap']['cw'].update({'ipms':'65','ipfab':'66','ipumc':'69','ipvis':'71,78','ipgf':'67'});T['srcmap']['hx'].update({'ipms':'56','ipfab':'56','ipumc':'56','ipvis':'56','ipgf':'56'})
gp=[x for x in T['gaps'] if '中介层' in x]
if not gp: T['gaps'].append('硅中介层：没有公司披露产能，台积电自制量按 2025 年反推、2027 年新增为假设；2028 年格罗方德放量 {ipgf} 在本图之外（图只到 2027Q4），见 CoWoS 页第 7 步中介层表。')
json.dump(T,open(P('data','toc.json'),'w'),ensure_ascii=False,indent=1)
js=r"""const TOC=require(process.argv[1]+'/toc.js'),fs=require('fs'),r=p=>JSON.parse(fs.readFileSync(process.argv[1]+'/data/'+p));
const J=r('cowos.json'),H=r('hbm.json'),T=r('toc.json'),o=TOC.calc(J,H,T,{}),o2=TOC.calc(J,H,T,{hbm:.8});
console.log(JSON.stringify({raw:o.out.map(x=>[x.q,x.D,x.st.cw,x.st.ip,x.st.hbm,x.st.tcb,x.st.sub,x.st.pw,x.min,x.bind,x.thru]),b:o.out.map(x=>[x.q,x.bind,Object.fromEntries(Object.entries(x.st).map(([k,v])=>[k,v/x.D-1]))]),b2:o2.out.map(x=>[x.q,x.bind]),coef:o.coef}))"""
t=json.loads(subprocess.run(['node','-e',js,R0],capture_output=True,text=True,check=True).stdout)
NM={'cw':'CoWoS','ip':'硅中介层','hbm':'HBM','tcb':'键合机','sub':'ABF 载板','pw':'电力','dem':'各环节都够'}
def runs(b):
    out=[]
    for q,k in b:
        if out and out[-1][2]==k: out[-1][1]=q
        else: out.append([q,q,k])
    return '；'.join((a if a==z else a+'–'+z[-2:] if a[:4]==z[:4] else a+'–'+z)+' '+NM[k] for a,z,k in out)
seq=runs([(q,k) for q,k,_ in t['b']]);seq2=runs(t['b2'])
last=t['b'][-1][2];h27=[x[2]['hbm'] for x in t['b'] if x[0].startswith('2027')];s27=[x[2]['sub'] for x in t['b'] if x[0].startswith('2027')]
pw26=[x[2]['pw'] for x in t['b'] if x[0].startswith('2026')]
c=t['coef'];g=lambda y:H['gbw'][str(y)]
next(x for x in T['stages'] if x['k']=='hbm')['conv']=f"× 3 × 每片有效 GB（{g(2025)}/{g(2026)}/{g(2027)}，按券商产量校准 HBM 页源65）× 稼动率 = GB，÷ 每封装 HBM（产品加权：2025 年 {c['2025']['gb']:.0f}、2026 年 {c['2026']['gb']:.0f}、2027 年 {c['2027']['gb']:.0f} GB）<span class=\"tag t-est\">估</span>"
T['steps'][0][2]=f"模型（v0.4 校准后）：{seq}。HBM 可供量下调 20% 时：{seq2}。行为证据：英伟达下调 HBM 规格以多出货 {{kgi}}；供应承诺一季加到 2,790 亿美元、主要是存储 {{nv}}"
T['steps'][4][2]=f"2027 年模型约束在 ABF 载板（相对需求 {min(s27)*100:+.0f}%，估，数据最弱），HBM 紧随其后（{min(h27)*100:+.0f}%）；电力余量从 2026 年约 {min(pw26)*100:+.0f}%～{max(pw26)*100:+.0f}% 降到 2027Q4 约 {t['b'][-1][2]['pw']*100:+.0f}%，2028 年可能轮到电力 <span class=\"tag t-est\">估</span>"
for p in T['preds']:
    if p['id']=='T1' and p['status']=='pending':
        p['status']='void';p['note']='2026-10-15 作废：HBM 页 v0.4 上修 HBM 供给约五成后，模型里 2027 年约束不再是 HBM（改为载板，HBM 次之），以 T4 替代。原文保留。'
if not any(p['id']=='T4' for p in T['preds']):
    T['preds'].append({'id':'T4','text':'2027 年 HBM 位元产量同比 ≥ +35%（HBM 页 v0.4 模型 +37%）：2027-12-31 前 TrendForce 或主要券商给出的 2027 年 HBM 产量/出货增速 ≥ +35%；若 < +25%，说明 v0.4 上修过头、约束仍在 HBM','due':'2027-12-31','check':'TrendForce HBM 季报摘要；iM/UBS 等券商','status':'pending'})
for f in T['falsify']:
    if f['j'].startswith('T1'):
        f.update({'j':'T1′ 2027 年约束不在 HBM（v0.4）','counter':f'HBM 只比需求低约 {-min(h27)*100:.0f}%，载板产能是估的；只要载板实际扩产比 KGI 的 +25–30% 快，约束就回到 HBM','falsify':'2027 年 HBM 原厂称需配额、无法满足客户，同时载板价格松动','ind':'HBM 原厂财报会措辞；欣兴毛利率；ABF 报价','th':'HBM 2027 年产量增速 < +25%（见 T4）','now':'iM 证券 2026 年产量 44.4 亿 GB（HBM 页源65）','st':'watch'})
_ip=lambda y,k:[x[2][k] for x in t['b'] if x[0].startswith(str(y))]
T['ipsum']={str(y):dict(ip=round(min(_ip(y,'ip'))*100,1),cwlo=round(min(_ip(y,'cw'))*100,1),cwhi=round(max(_ip(y,'cw'))*100,1),hbm=round(min(_ip(y,'hbm'))*100,1),sub=round(min(_ip(y,'sub'))*100,1)) for y in (2026,2027)}
json.dump(T,open(P('data','toc.json'),'w'),ensure_ascii=False,indent=1)
# ---- 两个 Excel 都附上同一张"TOC约束"表（以前是手工追加的，重跑会丢）
import openpyxl
from openpyxl.styles import Font
for xf in [P('cowos','cowos_model.xlsx'),P('hbm','hbm_model.xlsx')]:
    wb=openpyxl.load_workbook(xf)
    if 'TOC约束' in wb.sheetnames: del wb['TOC约束']
    ws=wb.create_sheet('TOC约束');ws.append(['单位：百万颗 AI 加速器封装/季；算法见 toc.js / data/toc.json；除 CoWoS、HBM 外各环节规模为估计（含校准）；由 cowos/build.py 生成'])
    ws.append(['季度','需求','CoWoS','硅中介层','HBM','TC键合机','ABF载板','电力','最小环节','约束','通过量']);[setattr(c,'font',Font(bold=True)) for c in ws[2]]
    for r in t['raw']: ws.append([r[0]]+[round(v,3) for v in r[1:8]]+[NM[r[8]],'需求（各环节都够）' if r[9]=='dem' else NM[r[9]],round(r[10],3)])
    wb.save(xf)
print('ok · 来源',len(S),'· HBM 满足率',HC,'CoWoS',CC,'\n',seq,'\n',seq2)
