"""PCB 页来源表（唯一编号来源）。build.py 和 page.py 都从这里取编号，页面里的 [源N] 不手写数字。
均于 2026-10-20 用 curl / 浏览器打开核对；只看到搜索摘要的在标题里注明。"""
SRC = [
 ('prq2', 'Prismark《PCB Market Q2 2026》摘要：2026 年全球 PCB 预计 +32.1% 至 1,134 亿美元，18 层以上 +86.7%、HDI +39.8%；1H26 前 40 大毛利率 20.1%→23.8%、资本开支 +86.5%', 'https://www.prismark.com/_files/ugd/950e51_f051e20bf9dc4317baa5019b5a5a4e0e.pdf'),
 ('prtop', 'Prismark《Top 100 PCB Manufacturers 2024》：全球 PCB 2023 年 635 亿美元 → 2024 年 736 亿美元（+5.8%）；胜宏 2024 年 14.93 亿美元（+33.3%）、沪电（WUS）19.60 亿美元（+42.7%）', 'https://www.prismark.com/_files/ugd/950e51_8ed1a31c4a2e405595e3f214995f9feb.pdf'),
 ('cninfo', '上市公司 2025 年报引用 Prismark：2025 年全球 PCB 产值 854 亿美元（+15.8%），中国大陆约 410.7 亿美元', 'https://static.cninfo.com.cn/finalpage/2026-04-29/1225231066.PDF'),
 ('gs', '财联社 2026-08-06（转述高盛）：AI 服务器 PCB 2027 年 375 亿美元（上调 38%）、2028 年 840 亿；CCL 2027 年 221 亿、2028 年 480 亿；AI PCB 面积 90/130/260/450 万 m²、CCL 2,700/4,200/7,800/13,100 万张（2025–28）；M9 占 AI CCL 7%/41%/58%（2026–28）；2027 年 GPU 板 188.0 亿、ASIC 板 187.3 亿美元', 'https://www.cls.cn/detail/2447667'),
 ('gsx', '河洛投研：高盛 AI PCB/CCL 报告解读（页面为 JS 渲染，只看到搜索摘要；30 层以上占比、6+N+6 HDI 占比、背板套数等细项）', 'https://www.xxquant.com/en/institution/institutional-research/f2333adf1f23fc57c8e9b3239b76b64b'),
 ('jef', '发现报告：杰富瑞 2026-06-22《PCB/CCL 最新动态：Kyber/背板交付延迟可能带来的影响》：2027 年 AI PCB/CCL TAM 下调 5%/8%，若 2028 年仍未落地再下调 11%/16%；短期上游玻纤布、CCL 更受益（只看到摘要页）', 'https://fxbaogao.com/detail/5492546'),
 ('kyber', "Tom's Hardware 2026-07-06：SemiAnalysis 称 Kyber NVL144（Rubin Ultra）因 PCB 中板/正交背板难做推迟到 2028；78 层（3 块 26 层压合）、约 1 m²；NVL72x2 过渡方案取消；英伟达回应\"路线图不变\"", 'https://www.tomshardware.com/pc-components/gpus/nvidias-kyber-rack-for-rubin-ultra-slips-to-2028'),
 ('cnbc', 'CNBC 2026-07-06：Kyber 机柜延迟报道与台湾供应链股价下跌', 'https://www.cnbc.com/2026/07/06/nvidia-kyber-rack-system-delays-manufacturing-taiwan-rubin-chips-.html'),
 ('cpx', "Tom's Hardware：GTC 2026 英伟达把 Rubin CPX 从路线图移除", 'https://www.tomshardware.com/pc-components/gpus/nvidia-removes-rubin-cpx-accelerators-from-its-roadmap-groq-3-lpus-take-center-stage-as-cpx-is-removed'),
 ('ms', '网易/新浪 2026-05-21（转述摩根士丹利 Rubin BOM）：VR200 NVL72 机柜 PCB 约 11.67 万美元 vs GB300 约 3.51 万（+233%）；计算板 26 层 HDI、M7→M8，交换板 24→32 层，新增 44 层中板 18 块、CX 模块板 72 块', 'https://www.163.com/dy/article/KTFQHH6U05198NMR.html'),
 ('gscu', 'BigGo 财经（转述高盛 2026-05 高端铜箔报告）：HVLP3+ 需求 679→5,206 吨/月（2025→2028）、有效供给 803→3,759 吨/月，有效缺口 2026/27/28 年 28%/39%/38%；良率 70–80%、换线损失 10–20%；金居为唯一通过客户认证的 HVLP4 二供', 'https://finance.biggo.com.tw/news/J84_RZ4BX0tZvRTvZP2h'),
 ('gscu2', '工商时报 2026-08-11（高盛上调金居目标价）：HVLP3+ 2026–2028 年供给缺口由 25%–40% 上修到 45%–55%；金居 HVLP3+ 良率 2Q26 逾 50%；3Q/4Q 价格季增 10–15%/5–10%', 'https://www.ctee.com.tw/news/20260811702033-430201'),
 ('uacu', '钜亨网/优分析 2026-09-24：HVLP4 缺口 2026 年约 1,500 吨、2027 年约 2,500 吨；Rubin 整机高阶铜箔约 59 kg（GB300 约 31 kg）；金居 HVLP4 月产能 1H26 约 100 吨 → 2H26 150 吨 → 2027 年 700–800 吨；德福 8 月 HVLP 约 500 吨、其中 HVLP4 约 70 吨；铜冠 HVLP4 量产；HVLP4 加工费 17–20 万元/吨', 'https://news.cnyes.com/news/id/6614743'),
 ('mitsui', '三井金属 2026-08-17 新闻稿：VSP（HVLP）月产能 FY25/26/27/28 为 720/840/1,000/1,200 吨，FY30 1,400 吨、FY32 2,600 吨，新建马来西亚厂', 'https://www.mitsui-kinzoku.com/LinkClick.aspx?fileticket=XzNABg5L0L4%3D&mid=824&tabid=204'),
 ('mitsuiq1', '三井金属 FY2026 Q1 说明会：铜箔投资 420 亿日元，铜箔事业 ROIC 52%，HVLP4 以上占比提升', 'https://www.mitsui-kinzoku.com/LinkClick.aspx?fileticket=nsbvk6VTbbE%3D&mid=1027&tabid=242'),
 ('cotech', '工商时报 2025-11-05：金居 HVLP3/4 2026 年月产能 100–150 吨，2027 上半年 HVLP4 500–600 吨，2027 年二、三季合计逾 1,000 吨', 'https://www.ctee.com.tw/news/20251105700179-439901'),
 ('defu', '新浪/上证报 2026-09-09：德福科技投资者关系纪要：8 月 HVLP 出货约 500 吨，其中 HVLP4 约 70 吨，HVLP4 良率 60% 以上；5 万吨高端铜箔基地 2027 年二季度起分批投产', 'https://finance.sina.com.cn/roll/2026-09-09/doc-inirfqcu8556820.shtml'),
 ('tongguan', '钜亨网 2026-09-24：铜冠铜箔 HVLP4 进入量产及产能爬坡，HVLP1–4 通过认证', 'https://news.cnyes.com/news/id/6614742'),
 ('nqa', 'MarketScreener：日东纺 2025-11-06 说明会问答：T-glass FY2026 增 10–20%、FY2027 为中期计划起点的 2 倍；客户把 NE 布当作 NER 的可获得替代品；产能弹性优先给 T-glass', 'https://www.marketscreener.com/news/nitto-boseki-main-questions-and-answers-at-the-financial-results-briefing-fiscal-year-ending-2026-ce7d5fdbd18bf12c'),
 ('tfn', 'TrendForce 2026-08-06：日东纺电子材料营收 778 亿日元（+27%）、营业利益 280 亿（+44%）；T-glass 产能到 2029 财年为 2026 财年 3 倍\"仍不够\"；英伟达、微软、谷歌、亚马逊订走多数高端产能；不再计划提价', 'https://www.trendforce.com/news/2026/08/06/news-nittobo-raises-fy2027-net-profit-forecast-by-jpy-3b-no-further-t-glass-price-hikes-planned/'),
 ('tft', 'TrendForce 研究摘要：日东纺约占 T-glass 九成、NER 六到七成，新产能最早 2027 年中', 'https://www.trendforce.com/research/download/RP260324EB'),
 ('post', 'Postation：日东纺资本开支 450 亿日元（原 217 亿）；福岛 150 亿日元织布新厂 2027 年 1–3 月投产；2027 年约两成布由南亚代织', 'https://www.postation.jp/news/nittobo-t-glass-capacity-doubling-no-more-price-hike'),
 ('hh', '宏和科技 问询函回复（上交所公告，新浪转载）：2024 年低介电布份额日东纺 55%、旭化成 31%、台玻 11%，低 CTE 布日东纺 85%、Unitika 14%；低介电布需求 2024 年约 8,000 万米、2025 年约 1 亿米；宏和 2027 年电子布 3,321 万米（低介电 2,281 万米），2027-06 达产；泰山玻纤约 1,790 万米、规划新增 9,400 万米', 'https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=11484457&stockid=603256'),
 ('gf', '发现报告：广发建材 2026-08-02：二代 Low-Dk 布 2027 年全球需求约 1.7 亿米，供需缺口超 40%（只看到摘要页）', 'https://fxbaogao.com/detail/5577194'),
 ('jy', '发现报告：电子布供需纪要 2026-07-19（弱）：二代布 2026 年 5,000–5,500 万米、2027 年约 8,000 万米；Low-CTE 2027 年 4,400–4,500 万米；2027 年总需求 2–3 亿米；大陆 2027Q4–2028Q2 新增 4–5 亿米，有过剩风险；2026Q1 起 Rubin 更多改用二代布', 'https://www.fxbaogao.com/detail/5551968'),
 ('cq', '钜亨网 2026-09-16：二代布每米 17.9–22.4 美元、Q 布 38.7–44.7 美元；Q 布供应商日东纺、信越、菲利华；菲利华通过生益、台光电、松下认证，中材通过台光电，宏和通过台光电、斗山', 'https://news.cnyes.com/news/id/6608165'),
 ('cldk', '钜亨网 2026-09-30：Prismark 2025 年低介电玻纤布市场 3.92 亿美元（+41%），2026–27 年每年 >40%；AI 服务器与交换机占 72.3%', 'https://news.cnyes.com/news/id/6618606'),
 ('qy', '群益证券（迈博汇金）菲利华：2026 年 Q 布需求 1,500 万米以上（最多 1,800 万米），有效产能不足 1,500 万米；日东纺新产能 2027 年逐步开出', 'https://www.microbell.com/data/ab56a57961c7e074f66b5665cf9869c7.html'),
 ('gsq', '发现报告：国盛证券 Q 布报告：Q 布 110.6–268.1 元/米；钻针损耗为二代布 2.6 倍；2026 年仍在认证，2027–28 年为首个放量窗口', 'https://www.fxbaogao.com/detail/5605910'),
 ('uad', '优分析 2026-10-08（尖点）：全球钻针需求 2025–28 年 35.28/51.16/76.73/103.60 亿支、有效供给 38.70/50.05/69.47/93.32 亿支；2025 年份额鼎泰 29.2%、金洲 21.1%、佑能 10.4%、尖点 9.9%；M9 主针寿命 100–200 孔（M8 400–500 孔）；进口开槽机交期 1–2 年', 'https://uanalyze.com.tw/articles/9401256786'),
 ('dt', '鼎泰高科 2026 中期报告（港交所）：钻针月产能突破 1.6 亿支', 'https://www.hkexnews.hk/listedco/listconews/sehk/2026/0819/2026081901497_c.pdf'),
 ('cld', '财联社：钻针涨价，普通针约 0.95 → 1.2 元，高端涨幅 35% 以上；钨钢棒价格翻倍（约占成本 20%）', 'https://m.cls.cn/detail/2373325'),
 ('emcir', '台光电 2026-07-29 法说会简报：2Q26 营收 472.75 亿新台币、毛利率 33.9%（2Q25 30.3%）；基板月产能 2024/2025/2026/2027/2028 年 4.35/5.85/6.15/9.30/11.10 百万张；2025 年 CCL 市占 16% 全球第一，高速无卤基板市场 2024 年 26.56 亿 → 2025 年 45.23 亿美元、台光电 38.6%', 'https://www.emctw.com/upload/media/New_Investors/Financial_Information/Presentation_Materials/CH/115/Investor%20Conference%20Presentation_20260729%20final%20CH.pdf'),
 ('udn1', '经济日报 2026-04-30：法人估台光电 M9 高阶材料 2027 年营收占比达双位数；2026/2027 年底月产能 615/945 万张', 'https://money.udn.com/money/story/5612/9474065'),
 ('udn2', '经济日报 2026-09-30：上半年陆资 CCL 涨价约 15%，最缺货料号涨 30–40%、个别逾 50%，四季度逐月续涨；台光电 M7 以上占比 60–65%', 'https://money.udn.com/money/story/5710/9785177'),
 ('ctccl', '工商时报 2026-09-05：CCL 三雄营收创新高；联茂 M9 GPU 料号通过认证，2027 年小量', 'https://www.ctee.com.tw/news/20260905700145-439901'),
 ('doosan', '东方财富财富号（斗山专家纪要，弱）：Rubin compute tray 用 M8 + 一代布，switch tray 用 M8 + 二代布（生益、台光电），中板 M9 + 二代布（台光电约 70%、斗山约 30%）；斗山 M8 月出货约 35 万张、M9 约 1 万张', 'https://caifuhao.eastmoney.com/news/20260916090343317645170'),
 ('shhk', '胜宏科技 2026 中期报告（港交所）：上半年毛利率 33.2%（上年同期 36.2%），主要因人工成本增加和新产能爬坡', 'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0827/2026082701954_c.pdf'),
 ('sh1h', '东方财富 2026-08-28：胜宏科技上半年营收 116.29 亿元（+28.77%）、净利润 28.57 亿元（+33.30%）', 'https://finance.eastmoney.com/a/202608283857870159.html'),
 ('shq2', '新浪（自媒体，弱）：胜宏科技 2Q26 单季毛利率约 32.1%', 'https://www.sina.cn/news/detail/5346228440405204.html'),
 ('shshare', '东方财富财富号（自媒体，弱）：胜宏在 GB200 UBB 份额约 70%、Rubin 约 50–55%（媒体口径）', 'https://caifuhao.eastmoney.com/news/20260724091356688820560'),
 ('hd', '九方智投（券商点评）：沪电股份 1H26 营收 136.89 亿元、净利润 29.23 亿元（+73.72%），毛利率 38.72%（+3.57pp）；PCB 毛利率 40.52%（+4.06pp），数据通讯收入 113.30 亿元（+73.46%）；32 层及以上收入 +190.83%', 'https://www.9fzt.com/detail/sz_002463_10_841564486976.html'),
 ('sy', '上海证券报 2026-08-15：生益科技 1H26 覆铜板营收 123.57 亿元（+47.74%）、毛利率 29.16%（+5.47pp），生产覆铜板 8,810 万 m²', 'https://paper.cnstock.com/html/2026-08/15/content_2255564.htm'),
 ('sn', '九方智投：深南电路 2026 半年报：PCB 收入 85.52 亿元、毛利率 36.85%（+2.43pp）；封装基板 36.67 亿元、毛利率 31.35%（+16.20pp）', 'https://www.9fzt.com/detail/sz_002916_9_4b1927738b55bdbb280e16da7d85a09f.html'),
 ('capex', '财联社/科创板日报 2026-06-10：年内 20 家 A 股 PCB 企业扩产、投资超 800 亿元；胜宏上限 200 亿（约 148 亿用于产能）、沪电累计 176 亿、鹏鼎 110 亿；高端产能 2–3 年后集中释放或迎\"大考\"', 'https://www.cls.cn/detail/2395508'),
 ('fm', 'MOPS 月营收与季报（经 FinMind API 下载）：台光电 2383、台燿 6274、联茂 6213、金像电 2368、金居 8358、富乔 1815、尖点 8021、台积电 2330；汇率同源', 'https://api.finmindtrade.com/api/v4/data'),
 ('dz', '大族数控 2026 半年报（深交所）：营收 49.85 亿元（+109.29%），钻孔设备需求旺盛', 'https://disc.static.szse.cn/download/disc/disk03/finalpage/2026-08-21/d0e5db05-96ad-4d6e-a5b6-663fd0f3a83c.PDF'),
 ('sq', '同花顺 2026-08-25：圣泉集团 PPO 树脂 2,000 吨/年满产满销，新建 2,000 吨 PPO/OPE 2026-09 投产；碳氢树脂 600 吨 + 规划 1,000 吨', 'https://stock.10jqka.com.cn/20260825/c679277603.shtml'),
 ('dc', '东方财富 2026-05-18：东材科技 M9 级碳氢树脂批量稳定供货，M10 验证中', 'https://finance.eastmoney.com/a/202605183740596014.html'),
 ('tpu', '新浪（谷歌 TPU 供应链纪要，弱）：V7 36 层、V7P 44 层主板；沪电约占谷歌 30%；深南做 V7 44 层；CCL 由松下 M8 向 M9 升级', 'https://finance.sina.com.cn/roll/2025-11-24/doc-infyphky3809028.shtml'),
 ('asc', '腾讯新闻（自媒体，弱）：昇腾 PCB 供应链：深南 2025 年净利 32.76 亿元（+74.47%）、沪电 2025 年营收 189.45 亿元', 'https://news.qq.com/rain/a/20260620A05EXR00'),
 ('hf', 'HighFrequencyPCB：Rubin CPX / 中板原计划用 M9 + Q 布，正交背板 78 层；中金估英伟达 AI PCB 2027 年 69.6 亿美元', 'https://www.highfrequencypcb.com/NEWS/Will-M9-Material-Revolutionize-the-PCB-Industry11(1).html'),
 ('hbm', '本站 HBM 页 v0.4 中国账本：国产卡可用 HBM 能配的卡（2026 / 2027 年）', 'hbm.html#cn'),
 ('cowos', '本站 CoWoS 页 v0.4.3 约束推导：ABF 载板 2027 年供给比需求少约 29%（同一 KGI 加速器口径）；国内 2.5D 能封的卡', 'cowos.html#neck'),
 ('kgi', 'KGI 2026-09-15：2027 AI chip outlook（AI 加速器出货预测，CoWoS 页源 1；本页只读取 CoWoS 页模型里的数）', 'https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/semiconductor-sector-_20260915_en.pdf'),
]
ID = {k: i + 1 for i, (k, _, _) in enumerate(SRC)}
assert len(ID) == len(SRC), '来源 key 重复'


def n(*k):
    """CH.tag 用的编号串，如 '4,10'"""
    return ','.join(str(ID[x]) for x in k)


def s(*k):
    """正文里的 [源N]（JSON 字符串里用，chain.js 的 srcInline 会转成标签）"""
    return f'[源{n(*k)}]'
