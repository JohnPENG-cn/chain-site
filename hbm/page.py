"""HBM 页内容 spec（结论层 + 底稿 13 步）。由 tpl/page.py 渲染成 hbm.html。数字来自 hbm/build.py 的模型；这里的文字数字须与模型一致。"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tpl'))
from nums import HC, CC, CGAP, CGAPU, HGAP, CS27, CD27   # 关键数字从模型算，不手写
from nums import CC26, CC27, CL26, CL27, CA26, CA27, CD26, CK26, CK27   # 中国账本
def S(x):  # 来源胶囊
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{n}">源{n}</a>' for n in str(x).split(',')) + '</span>'
E = '<span class="tag t-est">估</span>'


LOGIC = dict(
 title='HBM 一屏看懂：供需怎么走、卡在哪、预期差在哪',
 qa=[
  (f'2026 年不缺（产量约 4.4 EB，出货要约 3.8 EB）；2027 年需求再涨约七成，只是略紧：够约 {HC}%、缺约 {HGAP}%。2028 年三家产能再 +38%，要防转向过剩（未建模）{E}',
   f'国产 AI 卡能用上的 HBM：2026 年只够需求约 {CC26}%，2027 年囤货用完只剩约 {CC27}%，2028 年前看不到缓解 {E}'),
  ('卡在"分给 HBM 的 DRAM 晶圆"：同一片晶圆做普通内存（DDR5）更赚钱，原厂不愿多转。把各环节换成同一单位后，2027 年最紧的一环换成封装载板，2028 年可能轮到电力 ' + E,
   f'卡在长鑫：HBM 投片 2026 年底约 3 万片/月（三家约 50 万），堆叠良率约 25% {S("73,80")}；逻辑芯片不是约束'),
  (f'主流说 2027 年"史上最缺"、涨价是因为 HBM 缺货；我们算只缺约 {HGAP}%，涨价主要靠 DDR5 抢晶圆。所以要盯的风险是 DDR5 先跌，而不是 HBM 需求变弱',
   '主流盯长鑫"突破"；我们算 2027 年长鑫 HBM 投片只有三家的约 8%，国产卡缺 HBM 会比缺封装更久'),
 ],
 terms='名词：<b>HBM</b> = 高带宽内存，把 8–16 层 DRAM 芯片叠起来、贴在 GPU 旁边；<b>DDR5</b> = 服务器和电脑用的普通内存；<b>投片</b> = 每月投进产线的 12 寸晶圆片数；<b>EB</b> = 10 亿 GB。',
 three=['AI 芯片越卖越多、每颗配的 HBM 越来越大，2027 年 HBM 需求再涨约七成。',
        '三家原厂（SK 海力士、三星、美光）扩得动，但同一片晶圆做 DDR5 现在更赚钱，所以 HBM 只是略紧，价格被 DDR5 拉着涨。',
        f'中国被禁运，囤货 2026 年用完，长鑫的产量和良率都跟不上，国产 AI 卡只拿到需要的约 {CC26}%。'],
 keys=[(f'{HC}%', '2027 年 HBM 够出货所需'), (f'{CC26}%', '2026 年中国够需求'), ('约 10 倍', 'DDR5 一年涨价')],
 fig=[('需求驱动', '三家云厂商资本开支约 1,350 亿美元/季'), ('HBM 需求', '2027 年再涨约七成'), ('DRAM 晶圆', '三家年底投片 500 → 690 千片/月'),
      ('三家原厂', '海力士 · 三星 · 美光（中国：长鑫）'), ('约束：晶圆分给谁', 'HBM 还是 DDR5；中国卡在良率')],
 fig_note=f'投片：UBS {S(63)}；DDR5 涨价 {S("30,20")}；资本开支见第 3 步。',
 cons=[
  [f'2027 年是"史上最缺的一年"：SK 海力士 CEO {S(98)}；美光 CEO 说 2027、2028 年都供不应求 {S(101)}；키움证券：2027 年需求 +56%、产量只 +50% {S(99)}',
   f'2026 年不缺，2027 年只缺约 {HGAP}%', '缺口幅度：主流说严重短缺，我们说略紧',
   f'iM 证券：2026 年产量 44.4 亿 GB，高于需求 42.3 亿 {S(65)}；TrendForce 称 2026 年 HBM 价格"暂停" {S(2)}；GPU 厂考虑 12 层降到 8 层，用规格换数量 {S(36)}',
   '2026 年实际产量 ≥ 40 亿 GB（预测 P7）支持我们；原厂称 2027 年要配额、大客户拿不到量 → 我们错（证伪表 J1）'],
  [f'涨价是因为 HBM 自己缺货：TrendForce 预测 2027 年混合均价 +121% {S(36)}；HBM4 一颗从 600 涨到 1,300 美元 {S(35)}',
   '涨价主要是 DDR5 抢晶圆：原厂要求 HBM 每片晶圆赚得不少于 DDR5', '价格靠什么：主流看 HBM 需求，我们看 DDR5 价格',
   f'DDR5 16Gb 一年从 4.8 涨到 48 美元/颗 {S("30,20")}；供应商要求按普通 DRAM 晶圆产值定价 {S(67)}；三星满产能做 16.3 亿 GB，只打算做 13.8 亿 {S(65)}',
   'DDR5 先跌而 HBM 均价仍涨 > 50% → 我们错（证伪表 J2）'],
  [f'短缺持续到 2028 年：摩根大通 {S(100)}；SK 海力士称需求到 2030 年后仍高于产能 {S(98)}',
   '周期顶部看 2027 年下半年；2028 年三家投片再 +38%，要防过剩', '时点：主流看 2028 年以后，我们看 2027 年下半年',
   f'UBS：三家年底投片 500 → 690 千片/月（2026→27）{S(63)}；韩国半导体出口同比两轮都比营收早约 9–10 个月见顶 {S(30)}',
   '韩国半导体出口同比在 2027-03 前跌破 +100%（P6）'],
  [f'<b>中国：</b>长鑫"突破"、已小批量做 HBM3E {S(79)}；韩媒称 2026 年拿约 6 万片/月做 HBM {S(88)}',
   f'国产 AI 卡能用上的 HBM 2026 年只够约 {CC26}%、2027 年约 {CC27}%', '国产替代速度：主流快，我们慢',
   f'SemiAnalysis：长鑫 HBM 投片 2026 年底约 3 万片/月 {S(73)}；HBM3 良率约 25% {S(80)}；国产卡两个月涨价 20–50% {S(78)}',
   '950DT 报价回落到 20 万元以下（证伪表 CJ1），或长鑫投片确认 ≥ 6 万片/月 → 我们高估了缺口'],
 ],
 watch=[
  ['2026 年 HBM 实际产量', 'TrendForce / 券商的 2026 年回看', '≥ 40 亿 GB → "2026 年不缺"成立；< 40 亿 → 我们高估了供给', '2027-03-31'],
  ['SK 海力士怎么说 2027', '4Q26 财报会措辞', '"基本签完" → 正常；"要配额、客户拿不到量" → 我们低估了缺口', '2027-01-31'],
  ['DDR5 和 HBM 谁先松', 'DDR5 16Gb 固定价；TrendForce 2027 年 HBM 混合均价', 'DDR5 先跌而 HBM 仍 > +50% → "机会成本"说法错', '2027-06-30'],
  ['周期见顶信号', '韩国半导体出口 3 个月同比（每月 1 日公布）', '首次跌破 +100% → 约 9–10 个月后原厂营收见顶', '2027-04-01 前'],
  ['中国缺口有没有松', '950DT 卡报价；长鑫 HBM 投片', '报价 < 20 万元，或投片 ≥ 6 万片/月 → 中国缺口比我们算的小', '每月；2027-06-30 回看'],
 ],
)

SPEC = dict(
 logic=LOGIC,
 file='hbm.html', title='HBM 产业链', pill='HBM v0.5.2', other=('cowos.html', 'CoWoS ⇄'),
 scripts=['toc.js', 'hbm.js', 'hbm_x.js', 'hbm_cn.js'],
 kicker='HBM 小链 · v0.5.2 · 更新 <span id="upd">2026-10-15</span> · 下游接 <a href="cowos.html">CoWoS 小链</a>',
 card=f'全球账本：2027 年 HBM 只是略紧（缺约 {HGAP}%），涨价靠的是 DDR5 抢晶圆；周期顶部看 2027 年下半年。中国账本：2026 年国产 AI 芯片能用上的 HBM 只够需求约 {CC26}%，严重短缺{E}',
 scqa=[
  'AI 加速器每颗要 192–432GB HBM（B300/Rubin 288GB、MI450 432GB）。HBM 和普通 DRAM 用同一批晶圆，三家原厂（海力士、三星、美光）决定给 HBM 分多少。',
  f'普通 DRAM 一年多涨了约 10 倍 {S("30,20")}，1Q26 起 DDR5 服务器内存每片晶圆收入已超过 HBM {S("1,34")}；同时三家把 HBM 年末产能从 39 万片/月扩到 69 万（+77%）{S(63)}。我们上一版供给模型比券商统计的实际产量低约三分之一，"2027 年缺 19%"的结论站不住。',
  '2027 年 HBM 到底缺不缺？如果不怎么缺，价格为什么还要翻倍？风险在什么时候？'],
 gov='2027 年 HBM 只是略紧，涨价靠的是 DDR5 抢晶圆而不是 HBM 缺货；周期顶部看 2027 年下半年',
 mece='三条论点分别回答"量""价""时点"，互不重叠。中国的账另算（见<a href="#cn">中国账本</a>）：两本账口径不重复，长鑫产能只计入中国账本。',
 ledgers=[('a1', 'gl', '全球账本', f'2027 年 HBM 够出货所需约 {HC}%：略紧（缺约 {HGAP}%），涨价靠晶圆机会成本'),
          ('cn', 'cnl', '中国账本', f'2026 年国产 AI 芯片能用上的 HBM 只够需求约 {CC26}%、2027 年约 {CC27}%：严重短缺，卡在晶圆分配和堆叠良率')],
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
    dict(t='要害变量："略紧"很容易被推翻', b=f'单变量区间约 −25%～+12%：每片有效 GB 980 或投片 +10% 都能让缺口基本消失，出货 −20% 则富余 12%，出货 +20% 则缺 25% {E}。', steps=['key']),
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
 cn=dict(
  nav='中国账本', kicker='中国视角：国产 AI 芯片能用上的 HBM（与全球账本口径不重复）',
  scqa=[
   f'2024 年中国赶在禁令前囤了约 1,300 万颗 HBM（多为 HBM2E 16GB，合计约 0.21 EB）{S(72)}；2024-12 起美国禁止所有在产 HBM 对华出口 {S(68)}，英伟达对华芯片 2026 年也基本进不来（H200 进入大陆约 2 万颗）{S(84)}。',
   f'全球账本里 2027 年 HBM 只缺约 {HGAP}%，但国产 AI 卡 2026 年两个月集体涨价 20–50%，灰色渠道 HBM 价格是海外的数倍 {S(78)}；华为说需求超过供给 {S(77)}。',
   '国产 AI 芯片到底缺多少 HBM？卡在哪一环？什么时候缓解、谁受益？'],
  gov=f'中国看到的是另一本账：2026 年国产 AI 芯片能用上的 HBM 只够需求的约 {CC26}%，2027 年囤货已经用完、国产补不上，只够约 {CC27}%；卡住的是分给 HBM 的 DRAM 晶圆和堆叠良率，2028 年前看不到缓解',
  mece='三条中国论点分别回答"缺多少""卡在哪""何时缓解、谁受益"。口径：只算国产加速卡能用上的裸 HBM；英伟达对华芯片自带 HBM，不在这本账里。',
  args=[
   dict(tag='缺口', claim=f'囤货撑过了 2025 年，2026 年起断档：可用 HBM 约 {CA26:.2f} EB，只够不缺货需求的约 {CC26}%；2027 年已无囤货，只够约 {CC27}%',
    key=f'2026 覆盖率 <b data-from="cnG26">—</b> · 2027 <b data-from="cnG27">—</b> {E}',
    sub='需求 = 卡数 × 每卡 HBM；可用 = 期初库存 + 合法进口 + 灰色渠道 + 长鑫 + 武汉新芯。需求给两个口径：不缺货时的需求（估），和机构出货预测（拿得到 HBM 才出得了，是需求下限）。',
    hero=dict(src='cn-cBal', step='balance', t='中国账本：国产卡能用上的 HBM vs 需求（EB）', h=340, note='柱 = 可用（按来源堆叠），实线 = 不缺货需求，虚线 = 机构出货口径（需求下限）。'),
    ev=[
     dict(t='囤货：禁令前囤了约 0.21 EB，2025 年用掉大半', b=f'约 1,300 万颗，其中 1,140 万直接来自三星、禁令生效前一个月约 700 万，多为 8 层 HBM2E 16GB {S(72)}；够 2024–25 年出货，2026 年用完 {S(74)}。三星禁令前约 20%–30% 的 HBM 营收来自中国 {S("70,71")}。', steps=['supply', 'balance']),
     dict(t='需求：英伟达退出后要国产卡补', b=f'2025 年中国加速卡约 400 万张、国产 165 万 {S(81)}；2026 年英伟达基本缺席 {S(84)}。不缺货需求约 {CD26:.2f} EB {E}；就算只按机构出货预测（受限量）算，2026 年覆盖率也只有约 {CL26}%、2027 年约 {CL27}%。', steps=['demand', 'balance']),
     dict(t='价格信号：国产卡两个月涨 20–50%', b=f'950DT 报价超过 25 万元，950PR 6 万 → 8 万元以上，910C 9 万 → 11 万元以上，寒武纪 690 +20–30%；灰色渠道 HBM 价格是海外的数倍 {S(78)}。全球账本里 HBM 2026 年合约价"暂停" {S(2)}，两本账方向相反。', steps=['balance']),
     dict(t='替代：950PR 用"低成本"内存，是否算 HBM 有争议', b=f'华为称 HiBL 1.0 是"自研低成本 HBM" {S(75)}、Atlas 350 官方规格写"112GB HBM、1.4TB/s" {S(91)}；路透称基础版用传统 DDR {S(92)}，Epoch 看照片推测接近 LPDDR {S(74)}；<b>还没有拆解</b>。本页把约 75 万颗 950PR 放在 HBM 账外（推测）；若计入，2026 年覆盖率从约 {CC26}% 降到约 21%。', steps=['demand', 'play']),
    ]),
   dict(tag='约束', claim='卡住中国的不是逻辑芯片，而是"分给 HBM 的 DRAM 晶圆 × 堆叠良率"：长鑫 2026 年底约 3 万片/月做 HBM（韩美三家约 50 万），综合良率约 25%',
    key=f'2026 年可用 HBM 只够配 <b data-from="cnK26">—</b> 张卡 {E}',
    sub=f'按约束理论（TOC）把每一环换成"能配多少张国产卡"，取最小值。HBM 最少；逻辑芯片有台积电代工的 die bank 超过 290 万颗加中芯产出 {S(72)}。',
    hero=dict(src='cn-cCx', step='supply', t='HBM 投片：长鑫 vs 韩美三家（千片/月，年底）', h=300, note=f'韩美三家为 UBS 口径 {S(63)}，长鑫为 SemiAnalysis 口径 {S(73)}（另一口径 2026 年 6 万片 {S(88)}）。'),
    ev=[
     dict(t='TOC：换成同一单位，HBM 最少', b=f'2026 年可用 HBM 只能配约 {CK26:.2f} 百万张卡 {E}；SemiAnalysis 判断没有外国 HBM，华为 2026 年做不出 100 万颗昇腾 {S(72)}。2.5D 封装按 <a href="cowos.html#cn">CoWoS 页中国账本</a>估算，2026 年和 HBM 几乎一样紧（加上 950PR 都约 180 万张卡），2027 年不再是约束 {E}。', steps=['neck']),
     dict(t='晶圆：长鑫按经济账不愿多做 HBM', b=f'普通 DRAM 每片位元约是 HBM 3 倍、毛利更高；2025 年约 99% 收入是 DDR/LPDDR，招股书没有 HBM 募投项目 {S(73)}。HBM 投片 2025 年底约 5K → 2026 年底约 30K（另一口径 60K {S(88)}）。', steps=['supply', 'play']),
     dict(t='良率：TSV 与堆叠是瓶颈', b=f'HBM3 8 层前段约 35% × 后段约 70% ≈ 综合约 25%，12 层更低 {S("73,80")}；对照：成熟 1z 节点前段良率 85–90% {S(73)}。', steps=['supply', 'neck']),
     dict(t='设备与制程：买得到，但爬坡慢', b=f'TSV 刻蚀部分受控（Lam 受控、TEL 不受控），韩美 TCB 受限 {S("74,72")}；国产 TCB（快克智能）仍在打样、未出单 {S(87)}；北方华创 2026-03 发布混合键合机 {S(74)}。G4 ≈ 1z、G5 ≈ 1a 不用 EUV 也能做，2028 年前不是主约束 {S(73)}。', steps=['neck', 'map']),
    ]),
   dict(tag='时点', claim='2026–27 年最紧：囤货 2026 年用完，长鑫 HBM3E 2027 年才扩产；先受益的是国产 HBM 链（长鑫、后段封测、键合设备），但 A 股公司的 HBM 收入基本没有披露',
    key=f'长鑫 HBM 投片 <b>5K → 30K → 55K</b> 片/月（2025–27 年底）{S(73)}',
    sub='时间表来自公告、华为发布会和机构预测。A 股按"证据强度"分级：强 = 公司公告；中 = 机构报告；弱 = 只有业务线或自媒体。',
    hero=dict(src='cn-cCov', step='neck', t='中国账本覆盖率：2026 年断档，2027 年更低', h=300, note='可用 ÷ 需求；100% 以上 = 有库存。'),
    ev=[
     dict(t='时间表：禁令 → 囤货 → 断档 → 国产扩产', b=f'2024-12 禁令 {S(68)} → 2025 年囤货变成 65 万颗 910C {S(72)} → 2026 年囤货用完 {S(74)} → 2027 年长鑫 HBM3E 扩产 {S(79)}，华为 960DT（Q1）、960PR（Q3）{S(76)} → 2028 年长鑫约 10 万片/月 {S(74)}。', steps=['neck']),
     dict(t='玩家：谁的决定会改变这本账', b=f'BIS 是否补漏洞或放松；长鑫是否在政策压力下多分晶圆给 HBM；发改委是否放行更多 H200（会分走国产卡需求）{S(84)}。', steps=['play']),
     dict(t='A 股：按环节，证据强度分级', b=f'强：长鑫科技（688825）{S(85)}；中：通富微电（HBM 后段，机构称）{S(73)}、北方华创（混合键合）{S(74)}、寒武纪（需求侧，涨价但受 HBM 制约）{S(78)}；弱：快克智能（TCB 未出单）{S(87)}、长电、拓荆、华海清科、赛腾、华海诚科（HBM 收入未披露）。', steps=['map']),
    ]),
  ]),
 wrong=f'''<p class="sub">每条论点一一对应一条证伪条件：J1↔论点①、J2↔论点②、J3↔论点③，J4 是需求的上一层（云厂商资本开支）。三个核心争议的完整论证见 <a href="#debate">底稿第 1 步</a>。触发阈值就改判断，不辩护。</p>
<div class="tbl"><table id="hx-falT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：CJ1–CJ4</h3><p class="sub">CJ1↔中国论点❶、CJ2↔❷、CJ3/CJ4↔❸。</p>
<div class="tbl"><table id="cnFalT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 pred='''<p class="sub">到期后按公开数据打分，不改原文，只追加结果。P 系列是本链判断，T 系列是约束迁移（与 CoWoS 页共用），C 系列是中国账本。</p>
<div class="tbl"><table id="predT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<div id="hx-tpred"></div>
<h3>中国账本：C 系列（2026-10-15 写入）</h3><p class="note" id="cnPredS"></p>
<div class="tbl"><table id="cnPredT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 base_title='HBM 产业链底稿',
 base_sub='上面的结论都从这里来。按 SOP 顺序：先找要害变量和争议，再定边界、算供需、看利润和约束，最后看玩家、历史、领先指标和公司。右侧圆圈 = 这一步支撑哪条论点。',
 steps=[
  dict(id='key', h='哪个假设能把结论翻过来', body=f'''<div class="card"><b>2027 年 HBM 缺口对各假设的敏感度</b><p class="note" id="hx-torNote" style="margin-top:4px"></p><div id="hx-cTor" class="chart" style="height:290px"></div><div class="note">每行只动一个变量（蓝 = 低端、红 = 高端），其他保持基准。单变量区间约 −25%～+12%：每片有效 GB 980 或投片 +10% 都能让缺口基本消失，出货 −20% 则富余 12%，出货 +20% 则缺 25%。<b>"略紧"本身就是一个容易被推翻的结论</b>，要盯每片有效 GB 和出货。{E}</div></div>'''),
  dict(id='debate', h='三个可证伪的核心争议', ctx='对应结论层「可能错在哪」↑', body=f'''<div class="grid g3">
<div class="card"><b>Q1 2027 年 HBM 过剩还是短缺？</b><p style="margin:.4em 0;font-size:15px">观点：略紧（约 −{HGAP}%），不是严重短缺；价格大涨主要是晶圆机会成本。</p><div class="note">证伪：2027 年原厂称 HBM 要配额、大客户拿不到量；或 2026 年实际产量 &lt; 40 亿 GB（预测 P7）。</div></div>
<div class="card"><b>Q2 三家扩产会让 HBM 很快过剩吗？</b><p style="margin:.4em 0;font-size:15px">观点：2027 年不会：年末产能 +38%，出货所需 +71%；但 2028 年要警惕。</p><div class="note">证伪：2027 年普通 DRAM 价格先跌、晶圆转回 HBM，HBM 价格松动。</div></div>
<div class="card"><b>Q3 这轮存储周期何时见顶？</b><p style="margin:.4em 0;font-size:15px">观点：最早 2027 年中后期，看新厂投产节奏。</p><div class="note">证伪：2027Q1 前韩国半导体出口同比仍 &gt;+100% 且加速 → 判断太早。</div></div>
</div>'''),
  dict(id='proc', h='计量单位与工序：每道工序用谁的设备和材料', ctx='背景：定义单位与边界', sub=f'计量单位：需求用 GB，产能用 12 寸晶圆片/月，出货用颗（stack）。HBM3E/HBM4 12 层 = 36GB，16 层 = 48GB。HBM 在普通 DRAM 约 700 道工序之外再加约 19 道（正面 10、背面 9）{S(39)}。',
   body='<div class="tbl"><table id="procT"><thead><tr><th>工序</th><th>要点</th><th>设备 / 材料 / 供应商</th><th>来源</th></tr></thead><tbody></tbody></table></div>'),
  dict(id='demand',
  cn=dict(h='国产卡要多少 HBM：不缺货需求 vs 机构出货口径', body=f'''<div class="tbl"><table id="cn-demT" class="stack"><thead><tr><th>年份</th><th>口径</th><th>算法</th><th>依据</th><th>需求（EB）</th></tr></thead><tbody></tbody></table></div>
<div class="card" style="margin-top:12px"><b>每颗芯片要多少 HBM：华为路线图</b><div class="tbl"><table><thead><tr><th>芯片</th><th>内存</th><th>时间</th><th>来源</th></tr></thead><tbody>
<tr><td>910B</td><td>64GB HBM2E（4 颗）</td><td>2023–</td><td>{S(72)}</td></tr><tr><td>910C</td><td>128GB HBM2E（8 颗 16GB）</td><td>2025–</td><td>{S(72)}</td></tr>
<tr><td>950PR</td><td>自研 HiBL 1.0；芯片最大 128GB、1.6TB/s，出货的 Atlas 350 卡为 112GB、1.4TB/s（内存类型有争议，见下表）</td><td>2026Q1 发布，4 月量产</td><td>{S("90,91,92")}</td></tr><tr><td>950DT</td><td>自研 HiZQ 2.0，144GB、4TB/s（另有 96GB 版）</td><td>2026Q4</td><td>{S("75,74")}</td></tr>
<tr><td>960DT / 960PR</td><td>未公布；Atlas 960E 超节点 4,096 颗、最多 1PB HBM，折合每颗约 244GB</td><td>2027Q1 / Q3</td><td>{S(76)}</td></tr></tbody></table></div>
<div class="note">寒武纪、平头哥、昆仑芯等单卡 HBM 容量没有找到可靠公开数据，按 64–96GB 估 {E}。</div></div>
<div class="card" style="margin-top:12px"><b>950PR 用的到底是不是 HBM：证据分级</b><div class="tbl"><table class="stack"><thead><tr><th>说法</th><th>级别</th><th>来源</th></tr></thead><tbody>
<tr><td>HiBL 1.0 是"自研低成本 HBM，比 HBM3E/HBM4E 更划算"，与 950 die 合封</td><td><span class="pill" style="color:var(--ok)">官方</span></td><td>{S(75)}</td></tr>
<tr><td>950PR 最大 128GB、1.6TB/s"高速片上内存"（官网没写 HBM）；Atlas 350 卡写"112GB HBM、1.4TB/s、ECC"</td><td><span class="pill" style="color:var(--ok)">官方</span></td><td>{S("90,91")}</td></tr>
<tr><td>基础版 950PR 用"传统 DDR"（约 5 万元/卡），高配版用 HBM（约 7 万元）</td><td><span class="pill" style="color:var(--warn)">媒体报道</span></td><td>{S(92)}</td></tr>
<tr><td>封装为 2 个 AI die + 8 个内存模块（950DT 为 4 个 HiZQ 堆栈）</td><td><span class="pill" style="color:var(--mut)">泄露图，未证实</span></td><td>{S(96)}</td></tr>
<tr><td>内存模块离计算 die 太远、像 LPDDR；"可能是接近 LPDDR 的非 HBM"</td><td><span class="pill" style="color:var(--mut)">推测（照片判读）</span></td><td>{S("74,95")}</td></tr>
<tr><td>910C 里是三星、SK 海力士的 HBM2E + 台积电 die；910B 里有台积电 die</td><td><span class="pill" style="color:var(--acc2)">第三方拆解</span></td><td>{S("93,94")}</td></tr>
<tr><td>950PR / 950DT 的拆解</td><td><span class="pill" style="color:var(--mut)">没有找到</span></td><td>—</td></tr></tbody></table></div>
<div class="note">Kiko 的判断（推测）：1.4–1.6TB/s 分到 8 个模块，每个约 175–200GB/s，不到一颗 HBM2E 堆栈（约 410GB/s）的一半，更像宽位 LPDDR/DDR 封装；而且若 75 万颗 × 112GB ≈ 0.08 EB 都出自长鑫 HBM 线，要比本页估的 2026 年长鑫 HBM 产出（约 0.03 EB）大 2–3 倍。所以基准里 950PR 不计入 HBM 账，也不占长鑫 HBM 产能，但它占用长鑫普通 DRAM。若拆解证明是 TSV 堆叠 HBM，2026 年需求 +0.08 EB、覆盖率约 {CC26}% → 21%（见预测 C8）。{E}</div></div>'''),
  h='需求：谁在拉动，上一层是云厂商资本开支', body='''<div class="card"><b>HBM 需求按芯片厂商（EB）</b><div id="cMix" class="chart"></div><div class="note">KGI 出货 × 每封装 HBM（与 CoWoS 页同一张表），按芯片厂商汇总，单位 EB。2027 年需求 +71%。点击图例可隐藏。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>需求的上一层：亚马逊、微软、谷歌季度资本开支（柱）与积压订单（虚线）</b><div id="hx-cDrv" class="chart" style="height:360px"></div><div class="note">十亿美元，与 CoWoS 页同一组数据（各公司财报，Midgard Finance 汇编，<a href="cowos.html#src39">CoWoS 页源39</a>）。微软为含融资租赁口径。</div></div>
<div class="card"><table id="hx-drvT"><tbody></tbody></table><div class="note" style="margin-top:8px">链条：云收入/积压订单 → 资本开支 → 加速器订单 → HBM GB。表中来源编号指 <a href="cowos.html#src">CoWoS 页的来源表</a>（点开跳转）。反方证据是 AWS 资产回报在下降（证伪表 J4）。</div></div></div>'''),
  dict(id='supply',
  cn=dict(h='可用 HBM 从哪来：囤货、灰色渠道、长鑫、武汉新芯', body=f'''<div class="grid g2"><div class="card"><div id="cn-cCx" class="chart" style="height:300px"></div><div class="note">韩美三家合计（UBS {S(63)}）vs 长鑫 HBM 投片（SemiAnalysis {S(73)}）。2027 年底长鑫约是三家的 8%。</div></div>
<div class="card"><div class="tbl"><table id="cn-supT" class="stack"><thead><tr><th>年份</th><th>期初库存</th><th>合法进口</th><th>灰色渠道</th><th>长鑫</th><th>武汉新芯</th><th>可用合计</th></tr></thead><tbody></tbody></table></div><div class="note">单位 EB。合法进口 = 囤货里直接来自三星的 1,140 万颗 × 16GB；灰色渠道 2024 年 = 其余约 160 万颗（CoAsia/Faraday 绕道等）{S(72)}，2025 年约 0.024、2026 年约 0.010 EB 由 Epoch 的"走私 HBM 支撑的芯片数"倒推 {S(74)}{E}。</div></div></div>
<div class="card" style="margin-top:12px"><b>长鑫的产出怎么算</b><p class="note" style="font-size:13px">年均 HBM 投片（年末值线性平均）× 12 × 每片有效 GB。每片有效 GB 取 150（2026）/ 165（2027）{E}：按综合良率约 25% {S("73,80")}，并与 SemiAnalysis"2026 年约 200 万颗（16GB）"对齐 {S(72)}；领先三家约 880。武汉新芯约为长鑫的 1/10 {S(74)}（媒体称其 HBM 厂规划 3,000 片/月 {S(86)}）。<b>两个口径冲突</b>：SemiAnalysis 2026 年底约 3 万片/月 {S(73)}，韩媒称 2026 年拿 20%（约 6 万片/月）做 HBM3 {S(88)}——本页用前者，后者见第 5 步滑块。长鑫 2026-07-27 上市 {S(85)}，招股书没有单列 HBM 产能 {S(73)}。</p></div>'''),
  h='供给：分厂产能，以及为什么要按券商产量重新校准', body=f'''<div class="card"><b>分厂季度产能（千片/月，季末）</b><div id="cCap" class="chart" style="height:360px"></div><div class="note">实线 = 有来源的锚点或图上读数，年内为线性插值 {E}。锚点：</div><ul id="capA" class="note" style="padding-left:18px;margin:4px 0 0"></ul></div>
<div class="card" style="margin-top:14px"><b>校准：旧模型和券商统计的实际产量对不上</b><div class="note" id="calNote" style="font-size:13px"></div>
<div class="tbl"><table id="calT" style="margin-top:8px"><thead><tr><th>项目（EB）</th><th>本模型 v0.5（不含长鑫）</th><th>外部口径</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">外部口径也不一致：iM 证券按"实际需求"算 2026 年要 4.23 EB，比 KGI 出货口径（3.84 EB）高约 10%，按它算 2026 年只富余约 5% {S(65)}。所以"2026 年富余"的幅度不可靠，方向（不缺）比较可靠：TrendForce 也称 2026 年 HBM 价格"暂停"、均价小跌 {S(2)}。</div></div>'''),
  dict(id='balance',
  cn=dict(h='中国平衡：拖动假设看缺口', body=f'''<div class="grid g2"><div class="card">
<div class="ctl">
<label>2026–27 需求增速（相对 2025 年总量）<output id="cno1"></output></label><input type="range" id="cns1" min="0" max="50" step="5" value="25">
<label>长鑫 2027 年底 HBM 投片（千片/月）<output id="cno2"></output></label><input type="range" id="cns2" min="30" max="100" step="5" value="55">
<label>长鑫 2027 每片有效 GB（≈良率）<output id="cno3"></output></label><input type="range" id="cns3" min="100" max="400" step="5" value="165">
<label>2026–27 灰色渠道（PB/年）<output id="cno4"></output></label><input type="range" id="cns4" min="0" max="80" step="5" value="10">
</div><button class="btn" onclick="cnReset()">恢复基准</button>
<div class="grid g2" style="margin-top:14px;gap:8px"><div><div class="note">2026 可用 ÷ 需求</div><div class="big" id="cnG26"></div></div><div><div class="note">2027 可用 ÷ 需求</div><div class="big" id="cnG27"></div></div></div>
<div class="note" id="cnTxt"></div><span id="cnK26" hidden></span>
</div><div class="card"><div id="cn-cBal" class="chart" style="height:340px"></div><div class="note">把长鑫拉到 10 万片/月、每片 400GB（接近领先厂商一半），2027 年覆盖率也到不了一半：缺口是量级问题，不是参数问题。{E}</div></div></div>
<div class="card" style="margin-top:12px"><b>价格信号（中国）</b><div class="tbl"><table><tbody>
<tr><td><b>950DT 卡</b></td><td>报价 &gt; 25 万元，两个月 +20–50%</td><td>{S(78)}</td></tr><tr><td><b>950PR 卡</b></td><td>年初约 6 万 → 8 万元以上（+30%）</td><td>{S(78)}</td></tr>
<tr><td><b>910C 卡</b></td><td>年初约 9 万 → 11 万元以上</td><td>{S(78)}</td></tr><tr><td><b>寒武纪 690</b></td><td>报价 +20–30%；沐曦、天数跟涨</td><td>{S(78)}</td></tr><tr><td><b>灰色渠道 HBM</b></td><td>价格是海外的数倍</td><td>{S(78)}</td></tr></tbody></table></div></div>'''),
  h='平衡与价格：自己拖动假设', sub='供给 = 年均月投片 × 12 × 每片有效 GB × 稼动率；需求 = KGI 出货 × 每封装 HBM。浏览器里实时重算，结论层的图跟着变。', body=f'''<div class="grid g2"><div class="card">
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
  dict(id='neck',
  cn=dict(h='中国的约束：换成"能配多少张国产卡"，HBM 最少，2.5D 封装几乎一样紧', body=f'''<div class="tbl"><table id="cn-tocT" class="stack"><thead><tr><th>环节</th><th>2026 年能支撑</th><th>依据</th><th>判断</th></tr></thead><tbody></tbody></table></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><div id="cn-cCov" class="chart" style="height:300px"></div><div class="note">实线 = 可用 ÷ 不缺货需求；虚线 = 可用 ÷ 机构出货口径。跟随第 5 步中国块滑块。</div></div>
<div class="card"><b>国产化时间表（约束什么时候松）</b><div class="tl" style="margin-top:10px" id="cn-tl"></div></div></div>'''),
  h='约束推导：换成同一单位后，2027 年 HBM 不是最紧的一环', sub='按约束理论（TOC）把 DRAM 晶圆、CoWoS、硅中介层（2026-10-16 加入，见 CoWoS 页）、键合机、载板、电力都换成"百万颗 AI 加速器封装/季"，每季取最小值；与 CoWoS 页共用同一个模型。', body=f'''<div id="hx-toc"></div>
<h3>汇总排序（推导结果 + 定性证据）</h3><p class="sub">条形长度 = 缓解所需月数（取区间上限，示意）。</p><div id="neckList" class="grid"></div>
<p class="note">键合机是跟着扩产走的环节，不是卡脖子：韩美一单 442 亿韩元（约 15 台）{S(17)}，ASMPT 也拿到海力士 HBM4 TCB 订单 {S(18)}。</p>'''),
  dict(id='play',
  cn=dict(h='中国账本的玩家：谁的决定会改变缺口', body='<div class="grid g2" id="cnPl"></div>'),
  h='谁在做什么决定，什么信号说明他们变了', body=f'''<div class="grid g2" id="hx-play"></div>
<p class="note">行为证据：三星 HBM 产能满产可做 16.3 亿 GB，但 2026 年只打算做 13.8 亿，把部分产能转去做利润更高的普通 DRAM {S(65)}。</p>'''),
  dict(id='hist', h='DRAM 周期与 HBM 代际', body='''<div class="grid g2"><div class="card"><b>DRAM 周期与格局</b><div class="tl" style="margin-top:12px" id="tl1"></div></div>
<div class="card"><b>HBM 代际：谁先过英伟达认证谁拿利润</b><div class="tl" style="margin-top:12px" id="tl2"></div></div></div>'''),
  dict(id='lead', h='先看哪个数据：韩国出口 vs 原厂营收（已回测）', body=f'''<div class="card"><div id="cBt" class="chart" style="height:380px"></div><div class="note">韩国半导体出口 3 个月滚动同比，2015-01 至 2026-09：2015–2025 产业通商部公共数据 {S(30)}，2026-01 至 08 产业通商部 9 月通报 {S(31)}，2026-09 初值 {S(20)}。美光营收 SEC XBRL {S(49)}；SK 海力士 {S(48)}。出口与营收<b>同步</b>（相关 0.97），不领先营收本身；但<b>同比见顶</b>两轮都比营收见顶早约 9–10 个月。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>交叉相关：出口领先 k 个月的相关系数</b><div id="cXc" class="chart" style="height:280px"></div><div class="note">k&gt;0 表示出口在前。两家都在 k = 0 或 −1 最高（0.97–0.98），k ≥ 6 降到 0.5 以下。美光 n≈42 个季度，海力士 n=18，样本少。</div></div>
<div class="card"><b>拐点对照</b><div class="tbl"><table id="tpT"><thead><tr><th>出口同比拐点</th><th>美光营收同比拐点</th><th>营收绝对值见顶</th></tr></thead><tbody></tbody></table></div><div class="note" id="btNow"></div></div></div>
<div class="grid g3" id="leadList" style="margin-top:14px"></div>'''),
  dict(id='ledger', h='预测台账放在结论层', ctx='台账在结论层「预测台账」↑', body='<p>P 系列（本链判断）和 T 系列（约束迁移，与 CoWoS 页共用）都在 <a href="#pred">结论层 · 预测台账</a>；每条判断的反方证据和证伪阈值在 <a href="#wrong">可能错在哪</a>。规则：到期按公开数据打分，不改原文，只追加结果；作废要写原因并保留原文。</p>'),
  dict(id='map',
  cn=dict(h='A 股受益：按环节，标明证据强度', body=f'''<p class="sub">HBM 专项营收基本没有披露。"强"= 公司公告或交易所文件；"中"= 机构报告；"弱"= 只有业务线（年报主营构成）或自媒体。受益方向是"国产 HBM 放量"，不是"全球 HBM 涨价"。</p>
<div class="tbl"><table id="cn-coT" class="stack"><thead><tr><th>环节</th><th>公司</th><th>代码</th><th>与中国 HBM 的关系</th><th>证据强度</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">对外接口（给大链）：中国账本可用 HBM 2026 / 2027 年约 {CA26:.2f} / {CA27:.2f} EB，可配国产卡约 {CK26:.2f} / {CK27:.2f} 百万张 {E}。</div>'''),
  h='环节 → 公司 → 资本与订单；交给 CoWoS 的数字', body='''<p class="sub">点节点看详情；实线边都附来源编号。虚线"业务归属"边只表示公司在这个环节有业务，<b>HBM 专项营收占比基本没有披露</b>，表里是年报相关业务线占比。</p>
<div class="seg" id="fMk"><button class="on" data-m="all">全部</button><button data-m="A">A股</button><button data-m="KR">韩</button><button data-m="TW">台</button><button data-m="US">美/欧/日</button><button data-m="HK">港</button></div>
<div class="grid" style="margin-top:12px"><div class="card" style="padding:6px"><div id="cNet" class="chart" style="height:560px"></div><div class="note" style="padding:0 6px">手机上按环节分簇固定排布（方块=环节，圆点=公司），可双指缩放、拖动；电脑上为力导向布局。</div><div style="display:flex;gap:8px;justify-content:flex-end;padding:4px 6px"><button class="btn" onclick="drawNet()">重置视图</button></div></div>
<div class="card" id="nodeInfo"><b>点击图中任一节点</b><div class="note">显示代码、角色、份额与关联边及来源。</div></div></div>
<h3>公司清单</h3><div class="tbl"><table id="coT"><thead><tr><th>公司</th><th>代码</th><th>环节</th><th>角色/份额</th><th>相关业务营收占比</th></tr></thead><tbody></tbody></table></div>
<div id="iface"><h3>对外接口：交给 CoWoS 和大链的数字</h3><p class="sub">下游 <a href="cowos.html#iface">CoWoS 小链</a>直接读取这里的供给模型，算"能出多少颗加速器"。</p>
<div class="tbl"><table><thead><tr><th>输出</th><th>2026</th><th>2027</th><th>说明</th></tr></thead><tbody id="ifT"></tbody></table></div>
<div class="card" style="margin-top:12px"><b>与 CoWoS 小链对账</b><div class="note" style="font-size:13px" id="ifTxt"></div></div></div>'''),
 ],
 src_small='<span id="srcN"></span> 条公开来源',
 src='''<p class="sub">1–23 于 2026-10-14、24–62 于 2026-10-15、63–67 于 2026-10-15（v0.4）、68–89 于 2026-10-15（v0.5 中国账本）用 curl 或浏览器打开。路透（源71,77,79,84）需登录，内容据搜索摘要；DIGITIMES（源80,82）为付费内容，据标题与摘要；源89 是个人自媒体，只作线索，未证实。未单独验证：Magica（Rubin 下调，搜索摘要）；源63 是研究频道对 UBS 报告的转述（原报告未见）；TrendForce"2027 年 HBM 需求 780 亿 Gb"只见于转载站，未采用。</p><ol class="src" id="srcL"></ol>
<h3>局限（公开数据补不了的）</h3><ul style="font-size:14px">
<li>每片有效 GB 没有原厂披露，v0.4 用券商产量反推；不同券商、不同月份的版本之间差约 5%，需求口径之间差约 10%。2027 年缺口对它极敏感（单变量 −25%～+12%）。</li>
<li>中国账本数据最弱：没有官方的中国 HBM 进口、产量或库存数据；囤货量、灰色渠道全部来自 SemiAnalysis、Epoch 的估算；长鑫 HBM 投片有 3 万与 6 万片/月两个冲突口径；良率只有一家媒体（DIGITIMES）和一家机构的数字；"不缺货需求"是 Kiko 的估计（机构只给受限出货量）。</li>
<li>分厂产能只有年末锚点（UBS 一家口径，经转述）和一张 2024 年券商季度图，季度值多为插值；三星自称 2026 年平均约 18 万片，比 UBS 高约 10%，美光 2025 年 ETNews 口径比 UBS 低。</li>
<li>HBM 合约价不公开，价格点来自韩媒报道和券商估计（一部分经 Silicon Analysts 二手汇编），不是成交数据。</li>
<li>韩国分品类存储出口 2026 年只公布零散月份，回测用半导体总出口；SK 海力士季度数据只有 18 个同比点。</li>
<li>A 股、台股公司的 HBM 专项营收占比基本未披露。探针卡、韩华 TCB 等供应关系没找到可打开的公开来源，没画进图谱。</li><li>不构成投资建议。</li></ul>''',
 log='''<div class="tbl"><table id="logT"><tbody></tbody></table></div>
<p><a href="hbm/hbm_model.xlsx">下载模型 Excel</a> · <a href="hbm/hbm_chain.md">报告原文（Markdown）</a> · 构建：<code>./build.sh</code>（数据 <code>hbm/build.py</code>，页面 <code>tpl/page.py</code> + <code>hbm/page.py</code>）</p>''',
)
