"""HBM 页内容 spec（结论层 + 底稿 13 步）。由 tpl/page.py 渲染成 hbm.html。数字来自 hbm/build.py 的模型；这里的文字数字须与模型一致。"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tpl'))
from nums import HC, CC, CGAP, CGAPU, HGAP, CS27, CD27   # 关键数字从模型算，不手写
def S(x):  # 来源胶囊
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{n}">源{n}</a>' for n in str(x).split(',')) + '</span>'
E = '<span class="tag t-est">估</span>'

SPEC = dict(
 file='hbm.html', title='HBM 产业链', pill='HBM v0.4', other=('cowos.html', 'CoWoS ⇄'),
 scripts=['toc.js', 'hbm.js', 'hbm_x.js'],
 kicker='HBM 小链 · v0.4 · 更新 <span id="upd">2026-10-15</span> · 下游接 <a href="cowos.html">CoWoS 小链</a>',
 card=f'2027 年 HBM 只是略紧（缺约 {HGAP}%），涨价靠的是 DDR5 抢晶圆而不是 HBM 缺货；周期顶部看 2027 年下半年{E}',
 scqa=[
  'AI 加速器每颗要 192–432GB HBM（B300/Rubin 288GB、MI450 432GB）。HBM 和普通 DRAM 用同一批晶圆，三家原厂（海力士、三星、美光）决定给 HBM 分多少。',
  f'普通 DRAM 一年多涨了约 10 倍 {S("30,20")}，1Q26 起 DDR5 服务器内存每片晶圆收入已超过 HBM {S("1,34")}；同时三家把 HBM 年末产能从 39 万片/月扩到 69 万（+77%）{S(63)}。我们上一版供给模型比券商统计的实际产量低约三分之一，"2027 年缺 19%"的结论站不住。',
  '2027 年 HBM 到底缺不缺？如果不怎么缺，价格为什么还要翻倍？风险在什么时候？'],
 gov='2027 年 HBM 只是略紧，涨价靠的是 DDR5 抢晶圆而不是 HBM 缺货；周期顶部看 2027 年下半年',
 mece='三条论点分别回答"量""价""时点"，互不重叠。',
 args=[
  dict(tag='量', claim=f'按券商产量重新校准后，HBM 供给比上一版高约五成：2025–26 年供给多于出货所需，2027 年只缺约 {HGAP}%',
   key=f'2027 缺口/需求 <b id="hGap">—</b> · 2026 <b id="hGap26">—</b> {E}',
   sub=f'需求 = 加速器出货 × 每封装 HBM，和 <a href="cowos.html#iface">CoWoS 页</a>共用同一张 KGI 出货表 {S("55,56")}；供给 = 年均月投片 × 12 × 每片有效 GB × 稼动率。',
   hero=dict(src='cBal', step='balance', t='HBM 供需（EB）：2027 年供给略低于需求', note='跟随底稿第 5 步的滑块实时重算。'),
   ev=[
    dict(t='供需平衡：2025–26 年有富余，2027 年略缺', b=f'基准（每片有效 GB 880、稼动率 90%）下 2027 年缺口/需求 <b data-from="gap">—</b>。2026 年的富余幅度不可靠（iM 证券的"实际需求"口径比 KGI 出货口径高约 10%），方向比较可靠 {S(65)}。', steps=['balance']),
    dict(t='为什么改：旧模型比券商统计的实际产量低约三分之一', b=f'iM 证券统计 2025 年 HBM 产量 26.3 亿 GB、2026 年 44.4 亿 GB {S(65)}；v0.4 用它反推每片有效 GB（2026–27 年 880），并用 UBS 年末产能做投片锚点 {S(63)}。', steps=['supply']),
    dict(t='产能：三家同时大扩产', b=f'海力士、三星、美光 HBM 年末产能 2025→2027 年从 39 万片/月到 69 万（+77%），2026→2027 年 +38% {S(63)}。', steps=['supply']),
    dict(t='需求：与 CoWoS 页同一张出货表', b=f'KGI 出货 × 每封装 HBM，2027 年 HBM 需求 +71%；需求的上一层是云厂商资本开支和积压订单。CoWoS 页反向对账：2027 年 HBM 够出货所需的约 {HC}%，CoWoS 约 {CC}%。', steps=['demand', 'map']),
    dict(t='要害变量："略紧"很容易被推翻', b=f'单变量区间约 −23%～+16%：每片有效 GB 980、投片 +10% 或出货 −20% 都能让缺口消失，出货 +20% 则缺 23% {E}。', steps=['key']),
    dict(t='约束推导：2027 年 HBM 不是最紧的一环', b=f'把 DRAM 晶圆、CoWoS、键合机、载板、电力换成同一单位（百万颗加速器封装/季）后，2027 年最紧的是 ABF 载板（数据最弱）{E}。', steps=['neck']),
   ]),
  dict(tag='价', claim='2027 年 HBM 涨价的动力是晶圆机会成本：DDR5 每片晶圆收入已超过 HBM，原厂要把 HBM 价格抬到"晶圆等价线"才肯继续分晶圆',
   key=f'2027 混合均价 <b>+121%</b> {S(36)}',
   sub=f'HBM 没有现货市场，只有年度/多年合约。TrendForce：2027 年合约谈判僵持，供应商要求涨价"让 HBM 的晶圆产值对齐普通 DRAM" {S(67)}。',
   hero=dict(src='cPx', step='balance', t='每 GB 价格：普通 DRAM 已经比 HBM 贵', h=380, note='HBM 为报道与券商估计的每 GB 价格，DDR4/DDR5 为韩国产业通商部固定交易价。'),
   ev=[
    dict(t='普通 DRAM 一年涨约 10 倍', b=f'DDR5 16Gb 固定价一年从 $4.80 涨到 $48/颗 {S("30,20")}，在"短缺飞涨"档；HBM 2026 年度合约锁在约 $12–18/GB，每片晶圆收入已低于 DDR5。', steps=['balance']),
    dict(t='2027 年 HBM 价格回到"吸引新建产能"档', b=f'2027 年约 $36/GB（+121%）{S("35,36")}，仍低于 DDR5 晶圆等价线 {E}。', steps=['balance']),
    dict(t='成本：每 GB HBM 耗片约是 DDR5 的 3 倍', b=f'所以同样一片晶圆，HBM 每 GB 要卖到 DDR5 的约 3 倍才打平 {S("25,9")}{E}。', steps=['profit']),
    dict(t='行为证据：三星把 HBM 产能转去做普通 DRAM', b=f'三星 HBM 产能满产可做 16.3 亿 GB，但 2026 年只打算做 13.8 亿 {S(65)}——原厂在用脚投票。', steps=['play']),
    dict(t='利润池：钱堆在存储', b=f'美光 GAAP 毛利率现在 87%，上一轮顶点（2018 年 8 月）61%，主要来自普通 DRAM 涨价 {S("49,1,34")}。', steps=['profit']),
   ]),
  dict(tag='时点', claim='周期还在上行，风险在 2027 年下半年：三家在利润率高点同时扩产，韩国出口同比还没见顶，见顶后约 9 个月营收才见顶',
   key=f'韩国半导体出口 10/1–10 <b>+170.9%</b> {S(21)}',
   sub=f'DRAM 的老规律：利润率创新高 + 同时大扩产 → 18–24 个月后过剩。三家 HBM 年末产能 2025 → 2027 年 +77% {S(63)}，现在像 2017 年底到 2018 年。',
   hero=dict(src='cBt', step='lead', t='韩国半导体出口同比 vs 原厂营收同比（3 个月滚动）', h=380, note='出口同比见顶两轮都比营收见顶早约 9–10 个月。'),
   ev=[
    dict(t='领先指标：出口同比还在高位', b=f'出口与营收同步（相关 0.97），不领先营收本身；但同比见顶两轮都比营收见顶早约 9–10 个月 {S("30,49")}。现在还没见顶。', steps=['lead']),
    dict(t='历史：利润率新高 + 同时扩产 = 下一轮过剩', b='DRAM 每轮周期都是这个顺序；HBM 代际上，谁先过英伟达认证谁拿利润。', steps=['hist']),
    dict(t='玩家：三家都在扩，份额在重排', b=f'UBS 预计 2027 年按位元三星 41%、海力士 39% {S(64)}；三家的扩产决定和信号见底稿。', steps=['play', 'profit']),
   ]),
 ],
 wrong=f'''<p class="sub">每条论点一一对应一条证伪条件：J1↔论点①、J2↔论点②、J3↔论点③，J4 是需求的上一层（云厂商资本开支）。三个核心争议的完整论证见 <a href="#debate">底稿第 1 步</a>。触发阈值就改判断，不辩护。</p>
<div class="tbl"><table id="hx-falT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 pred='''<p class="sub">到期后按公开数据打分，不改原文，只追加结果。P 系列是本链判断，T 系列是约束迁移（与 CoWoS 页共用）。</p>
<div class="tbl"><table id="predT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<div id="hx-tpred"></div>''',
 base_title='HBM 产业链底稿',
 base_sub='上面的结论都从这里来。按 SOP 顺序：先找要害变量和争议，再定边界、算供需、看利润和约束，最后看玩家、历史、领先指标和公司。右侧圆圈 = 这一步支撑哪条论点。',
 steps=[
  dict(id='key', h='哪个假设能把结论翻过来', body=f'''<div class="card"><b>2027 年 HBM 缺口对各假设的敏感度</b><p class="note" id="hx-torNote" style="margin-top:4px"></p><div id="hx-cTor" class="chart" style="height:290px"></div><div class="note">每行只动一个变量（蓝 = 低端、红 = 高端），其他保持基准。单变量区间约 −23%～+16%：每片有效 GB 980、投片 +10% 或出货 −20% 都能让缺口消失，出货 +20% 则缺 23%。<b>"略紧"本身就是一个容易被推翻的结论</b>，要盯每片有效 GB 和出货。{E}</div></div>'''),
  dict(id='debate', h='三个可证伪的核心争议', ctx='对应结论层「可能错在哪」↑', body=f'''<div class="grid g3">
<div class="card"><b>Q1 2027 年 HBM 过剩还是短缺？</b><p style="margin:.4em 0;font-size:15px">观点：略紧（约 −{HGAP}%），不是严重短缺；价格大涨主要是晶圆机会成本。</p><div class="note">证伪：2027 年原厂称 HBM 要配额、大客户拿不到量；或 2026 年实际产量 &lt; 40 亿 GB（预测 P7）。</div></div>
<div class="card"><b>Q2 三家扩产会让 HBM 很快过剩吗？</b><p style="margin:.4em 0;font-size:15px">观点：2027 年不会：年末产能 +38%，出货所需 +71%；但 2028 年要警惕。</p><div class="note">证伪：2027 年普通 DRAM 价格先跌、晶圆转回 HBM，HBM 价格松动。</div></div>
<div class="card"><b>Q3 这轮存储周期何时见顶？</b><p style="margin:.4em 0;font-size:15px">观点：最早 2027 年中后期，看新厂投产节奏。</p><div class="note">证伪：2027Q1 前韩国半导体出口同比仍 &gt;+100% 且加速 → 判断太早。</div></div>
</div>'''),
  dict(id='proc', h='计量单位与工序：每道工序用谁的设备和材料', ctx='背景：定义单位与边界', sub=f'计量单位：需求用 GB，产能用 12 寸晶圆片/月，出货用颗（stack）。HBM3E/HBM4 12 层 = 36GB，16 层 = 48GB。HBM 在普通 DRAM 约 700 道工序之外再加约 19 道（正面 10、背面 9）{S(39)}。',
   body='<div class="tbl"><table id="procT"><thead><tr><th>工序</th><th>要点</th><th>设备 / 材料 / 供应商</th><th>来源</th></tr></thead><tbody></tbody></table></div>'),
  dict(id='demand', h='需求：谁在拉动，上一层是云厂商资本开支', body='''<div class="card"><b>HBM 需求按芯片厂商（EB）</b><div id="cMix" class="chart"></div><div class="note">KGI 出货 × 每封装 HBM（与 CoWoS 页同一张表），按芯片厂商汇总，单位 EB。2027 年需求 +71%。点击图例可隐藏。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>需求的上一层：亚马逊、微软、谷歌季度资本开支（柱）与积压订单（虚线）</b><div id="hx-cDrv" class="chart" style="height:360px"></div><div class="note">十亿美元，与 CoWoS 页同一组数据（各公司财报，Midgard Finance 汇编，<a href="cowos.html#src39">CoWoS 页源39</a>）。微软为含融资租赁口径。</div></div>
<div class="card"><table id="hx-drvT"><tbody></tbody></table><div class="note" style="margin-top:8px">链条：云收入/积压订单 → 资本开支 → 加速器订单 → HBM GB。表中来源编号指 <a href="cowos.html#src">CoWoS 页的来源表</a>（点开跳转）。反方证据是 AWS 资产回报在下降（证伪表 J4）。</div></div></div>'''),
  dict(id='supply', h='供给：分厂产能，以及为什么要按券商产量重新校准', body=f'''<div class="card"><b>分厂季度产能（千片/月，季末）</b><div id="cCap" class="chart" style="height:360px"></div><div class="note">实线 = 有来源的锚点或图上读数，年内为线性插值 {E}。锚点：</div><ul id="capA" class="note" style="padding-left:18px;margin:4px 0 0"></ul></div>
<div class="card" style="margin-top:14px"><b>校准：旧模型和券商统计的实际产量对不上</b><div class="note" id="calNote" style="font-size:13px"></div>
<div class="tbl"><table id="calT" style="margin-top:8px"><thead><tr><th>项目（EB）</th><th>本模型 v0.4</th><th>外部口径</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">外部口径也不一致：iM 证券按"实际需求"算 2026 年要 4.23 EB，比 KGI 出货口径（3.84 EB）高约 10%，按它算 2026 年只富余约 5% {S(65)}。所以"2026 年富余"的幅度不可靠，方向（不缺）比较可靠：TrendForce 也称 2026 年 HBM 价格"暂停"、均价小跌 {S(2)}。</div></div>'''),
  dict(id='balance', h='平衡与价格：自己拖动假设', sub='供给 = 年均月投片 × 12 × 每片有效 GB × 稼动率；需求 = KGI 出货 × 每封装 HBM。浏览器里实时重算，结论层的图跟着变。', body=f'''<div class="grid g2"><div class="card">
<div class="ctl">
<label>2027 每片有效 GB <output id="o1"></output></label><input type="range" id="s1" min="700" max="1050" step="10" value="880">
<label>2027 稼动率 <output id="o2"></output></label><input type="range" id="s2" min="70" max="100" step="1" value="90">
<label>2027 投片计划达成率 <output id="o3"></output></label><input type="range" id="s3" min="70" max="120" step="5" value="100">
<label>2027 加速器出货（相对基准）<output id="o4"></output></label><input type="range" id="s4" min="70" max="130" step="5" value="100">
</div><button class="btn" onclick="resetS()">恢复基准</button>
<div style="margin-top:16px"><div class="note">2027 缺口（供 − 需）/ 需求</div><div class="big" id="gap"></div><div class="note" id="gapTxt"></div></div>
</div><div class="card"><div id="cBal" class="chart"></div>
<div class="note">基准：每片有效 GB 2025/26/27 = 750/880/880、稼动率 85/90/90% {E}，校准方法见第 4 步；投片用 UBS 年末产能插值 {S(63)}。2023–24 为估算（浅色柱）：<span id="histNote"></span></div></div></div>
<h3>价格：每 GB 价格与四档价格</h3>
<div class="card"><div id="cPx" class="chart" style="height:380px"></div><div class="note" id="pxNote"></div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>价格档位（四档）现在落在哪</b><div id="cTier" class="chart" style="height:250px"></div>
<div class="note">DDR5 16Gb 固定价一年涨约 10 倍（$4.80 → $48/颗）{S("30,20")}，在"短缺飞涨"档。HBM 2026：年度合约锁在约 $12–18/GB，每片晶圆收入已低于 DDR5，在"维持价"附近。HBM 2027：约 $36/GB（+121%）{S("35,36")}，回到"吸引新建产能"档，仍低于 DDR5 晶圆等价线。</div></div>
<div class="card"><b>价格事实（按时间倒序）</b><table id="pxF" style="margin-top:6px"><tbody></tbody></table></div></div>'''),
  dict(id='profit', h='利润池与成本：钱堆在存储，每 GB HBM 耗片约是 DDR5 的 3 倍', body=f'''<div class="grid g2">
<div class="card"><div id="cMar" class="chart"></div><div class="note">美光 GAAP 毛利率 2015–2026（SEC XBRL，按日历季度归位）{S(49)}；SK 海力士营业利润率 2021Q3–2026Q2 {S(48)}。美光上一轮顶点 2018 年 8 月 61%，现在 87%，主要来自普通 DRAM 涨价 {S("1,34")}。</div></div>
<div class="card"><div id="cShare" class="chart"></div><div class="note">HBM 营收份额：2025 全年 IDC（经 Silicon Analysts 转引）{S(32)}；1Q26、2Q26 Counterpoint {S("35,11")}。UBS 预计 2027 年按位元三星 41%、海力士 39% {S(64)}。</div></div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>每 GB 耗用晶圆面积（相对 DDR5）</b><div id="cCost" class="chart" style="height:300px"></div><div class="note">前三步来自 TrendForce 2024 {S(25)}；HBM4 一步按美光"约 3 倍"倒推 {E}{S(9)}。</div></div>
<div class="card"><b>成本与资本开支要点</b><table id="costF" style="margin-top:6px"><tbody></tbody></table><p style="font-size:15px;margin:.8em 0 0" id="parity"></p><div class="note">晶圆等价线是 Kiko 的推算 {E}：DDR5 固定价是 PC 颗粒口径，服务器 RDIMM 不同；HBM 长约的确定性也值钱。</div></div></div>'''),
  dict(id='neck', h='约束推导：换成同一单位后，2027 年 HBM 不是最紧的一环', sub='按约束理论（TOC）把 DRAM 晶圆、CoWoS、键合机、载板、电力都换成"百万颗 AI 加速器封装/季"，每季取最小值；与 CoWoS 页共用同一个模型。', body=f'''<div id="hx-toc"></div>
<h3>汇总排序（推导结果 + 定性证据）</h3><p class="sub">条形长度 = 缓解所需月数（取区间上限，示意）。</p><div id="neckList" class="grid"></div>
<p class="note">键合机是跟着扩产走的环节，不是卡脖子：韩美一单 442 亿韩元（约 15 台）{S(17)}，ASMPT 也拿到海力士 HBM4 TCB 订单 {S(18)}。</p>'''),
  dict(id='play', h='谁在做什么决定，什么信号说明他们变了', body=f'''<div class="grid g2" id="hx-play"></div>
<p class="note">行为证据：三星 HBM 产能满产可做 16.3 亿 GB，但 2026 年只打算做 13.8 亿，把部分产能转去做利润更高的普通 DRAM {S(65)}。</p>'''),
  dict(id='hist', h='DRAM 周期与 HBM 代际', body='''<div class="grid g2"><div class="card"><b>DRAM 周期与格局</b><div class="tl" style="margin-top:12px" id="tl1"></div></div>
<div class="card"><b>HBM 代际：谁先过英伟达认证谁拿利润</b><div class="tl" style="margin-top:12px" id="tl2"></div></div></div>'''),
  dict(id='lead', h='先看哪个数据：韩国出口 vs 原厂营收（已回测）', body=f'''<div class="card"><div id="cBt" class="chart" style="height:380px"></div><div class="note">韩国半导体出口 3 个月滚动同比，2015-01 至 2026-09：2015–2025 产业通商部公共数据 {S(30)}，2026-01 至 08 产业通商部 9 月通报 {S(31)}，2026-09 初值 {S(20)}。美光营收 SEC XBRL {S(49)}；SK 海力士 {S(48)}。出口与营收<b>同步</b>（相关 0.97），不领先营收本身；但<b>同比见顶</b>两轮都比营收见顶早约 9–10 个月。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>交叉相关：出口领先 k 个月的相关系数</b><div id="cXc" class="chart" style="height:280px"></div><div class="note">k&gt;0 表示出口在前。两家都在 k = 0 或 −1 最高（0.97–0.98），k ≥ 6 降到 0.5 以下。美光 n≈42 个季度，海力士 n=18，样本少。</div></div>
<div class="card"><b>拐点对照</b><div class="tbl"><table id="tpT"><thead><tr><th>出口同比拐点</th><th>美光营收同比拐点</th><th>营收绝对值见顶</th></tr></thead><tbody></tbody></table></div><div class="note" id="btNow"></div></div></div>
<div class="grid g3" id="leadList" style="margin-top:14px"></div>'''),
  dict(id='ledger', h='预测台账放在结论层', ctx='台账在结论层「预测台账」↑', body='<p>P 系列（本链判断）和 T 系列（约束迁移，与 CoWoS 页共用）都在 <a href="#pred">结论层 · 预测台账</a>；每条判断的反方证据和证伪阈值在 <a href="#wrong">可能错在哪</a>。规则：到期按公开数据打分，不改原文，只追加结果；作废要写原因并保留原文。</p>'),
  dict(id='map', h='环节 → 公司 → 资本与订单；交给 CoWoS 的数字', body='''<p class="sub">点节点看详情；实线边都附来源编号。虚线"业务归属"边只表示公司在这个环节有业务，<b>HBM 专项营收占比基本没有披露</b>，表里是年报相关业务线占比。</p>
<div class="seg" id="fMk"><button class="on" data-m="all">全部</button><button data-m="A">A股</button><button data-m="KR">韩</button><button data-m="TW">台</button><button data-m="US">美/欧/日</button><button data-m="HK">港</button></div>
<div class="grid" style="margin-top:12px"><div class="card" style="padding:6px"><div id="cNet" class="chart" style="height:560px"></div><div class="note" style="padding:0 6px">手机上按环节分簇固定排布（方块=环节，圆点=公司），可双指缩放、拖动；电脑上为力导向布局。</div><div style="display:flex;gap:8px;justify-content:flex-end;padding:4px 6px"><button class="btn" onclick="drawNet()">重置视图</button></div></div>
<div class="card" id="nodeInfo"><b>点击图中任一节点</b><div class="note">显示代码、角色、份额与关联边及来源。</div></div></div>
<h3>公司清单</h3><div class="tbl"><table id="coT"><thead><tr><th>公司</th><th>代码</th><th>环节</th><th>角色/份额</th><th>相关业务营收占比</th></tr></thead><tbody></tbody></table></div>
<div id="iface"><h3>对外接口：交给 CoWoS 和大链的数字</h3><p class="sub">下游 <a href="cowos.html#iface">CoWoS 小链</a>直接读取这里的供给模型，算"能出多少颗加速器"。</p>
<div class="tbl"><table><thead><tr><th>输出</th><th>2026</th><th>2027</th><th>说明</th></tr></thead><tbody id="ifT"></tbody></table></div>
<div class="card" style="margin-top:12px"><b>与 CoWoS 小链对账</b><div class="note" style="font-size:13px" id="ifTxt"></div></div></div>'''),
 ],
 src_small='<span id="srcN"></span> 条公开来源',
 src='''<p class="sub">1–23 于 2026-10-14、24–62 于 2026-10-15、63–67 于 2026-10-15（v0.4）用 curl 或浏览器打开。未单独验证：Magica（Rubin 下调，搜索摘要）；源63 是研究频道对 UBS 报告的转述（原报告未见）；TrendForce"2027 年 HBM 需求 780 亿 Gb"只见于转载站，未采用。</p><ol class="src" id="srcL"></ol>
<h3>局限（公开数据补不了的）</h3><ul style="font-size:14px">
<li>每片有效 GB 没有原厂披露，v0.4 用券商产量反推；不同券商、不同月份的版本之间差约 5%，需求口径之间差约 10%。2027 年缺口对它极敏感（单变量 −23%～+16%）。</li>
<li>分厂产能只有年末锚点（UBS 一家口径，经转述）和一张 2024 年券商季度图，季度值多为插值；三星自称 2026 年平均约 18 万片，比 UBS 高约 10%，美光 2025 年 ETNews 口径比 UBS 低。</li>
<li>HBM 合约价不公开，价格点来自韩媒报道和券商估计（一部分经 Silicon Analysts 二手汇编），不是成交数据。</li>
<li>韩国分品类存储出口 2026 年只公布零散月份，回测用半导体总出口；SK 海力士季度数据只有 18 个同比点。</li>
<li>A 股、台股公司的 HBM 专项营收占比基本未披露。探针卡、韩华 TCB 等供应关系没找到可打开的公开来源，没画进图谱。</li><li>不构成投资建议。</li></ul>''',
 log='''<div class="tbl"><table id="logT"><tbody></tbody></table></div>
<p><a href="hbm/hbm_model.xlsx">下载模型 Excel</a> · <a href="hbm/hbm_chain.md">报告原文（Markdown）</a> · 构建：<code>./build.sh</code>（数据 <code>hbm/build.py</code>，页面 <code>tpl/page.py</code> + <code>hbm/page.py</code>）</p>''',
)
