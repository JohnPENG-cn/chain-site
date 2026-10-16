"""CoWoS 页内容 spec（结论层 + 底稿 13 步）。由 tpl/page.py 渲染成 cowos.html。数字来自 cowos/model.py、cowos/build.py 与 HBM 页 v0.4 模型。"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tpl'))
from nums import HC, CC, CGAP, CGAPU, HGAP, CS27, CD27   # 关键数字从模型算，不手写
from nums import WC26, WC27, WH26, WH27, WS26, WS27, WK26, WK27, WHK26, WHK27, CK26, CK27, W   # 中国账本
def S(x):
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{n}">源{n}</a>' for n in str(x).split(',')) + '</span>'
E = '<span class="tag t-est">估</span>'

GOV = '2027 年 CoWoS 只略紧、不再是头号瓶颈，最紧的是载板；利润往载板迁移，设备景气还没见顶'


LOGIC = dict(
 title='CoWoS 一屏看懂：供需怎么走、卡在哪、预期差在哪',
 qa=[
  (f'台积电产能三年涨了约 9 倍，2027 年总产能再涨约七成，缺口收窄到约 {CGAP}%（只加 KGI 点名的客户需求约 {CGAPU}%）。2028 年看台积电面板级封装（CoPoS）放量 {S(26)}（未建模）',
   f'台积电不接国产 AI 芯片；国内 2.5D 封装 2026 年刚好够 HBM 能配的卡（约 {WH26}%），2027 年产能翻倍，是所需的约 {WH27/100:.1f} 倍 {E}'),
  ('约束在迁移：2023–24 年是 CoWoS，2026 年要看 HBM，2027 年换成封装载板（ABF 载板和它用的 T-glass 玻纤布，数据最弱），2028 年可能轮到数据中心电力 ' + E,
   f'2026 年 HBM 和国产 2.5D 并列最紧（都约 {WK26:.1f} 百万张卡），2027 年只剩 HBM；下一个卡点是 ABF 膜（味之素占 95% 以上）{S(55)}'),
  (f'主流还把 CoWoS 当头号瓶颈（KGI：对客户需求缺 15–20%）{S(1)}；我们算只缺 {CGAP}–{CGAPU}%，利润涨得最快的是扩得慢的载板（欣兴毛利率一年 13.1% → 24.8%）{S(32)}',
   '主流把国产 CoWoS 扩产当主线；我们看 2027 年国内封装会超过 HBM 能配的卡，封装厂可能先遇到产能闲置，载板和 ABF 膜更稀缺'),
 ],
 terms='名词：<b>CoWoS</b> = 台积电把计算芯片和 HBM 并排放在一块硅中介层（带细密走线的硅片）上的封装；<b>2.5D</b> = 这类"并排 + 中介层"封装的统称；<b>ABF 载板</b> = 封装底下那块多层电路板；<b>片</b> = 12 寸晶圆片。',
 three=['AI 芯片要把计算芯片和 HBM 拼在一块硅片上封装（CoWoS）；芯片越大，一片晶圆能封的越少（H100 约 28 颗，Rubin Ultra 约 6 颗），所以要的片数涨得比芯片数快。',
        '台积电拼命扩产，2027 年缺口缩到个位数；扩得慢的是载板和玻纤布，紧张和利润都在往那里走。',
        '中国用不了台积电，只能靠国内封装厂；2026 年国内封装和 HBM 一样紧，2027 年封装扩得快，卡点回到 HBM。'],
 keys=[(f'{CC}%', '2027 年 CoWoS 够出货所需'), ('24.8%', '欣兴毛利率（一年前 13.1%）'), (f'{WH26}%', '2026 年中国 2.5D 够 HBM 能配的卡')],
 fig=[('需求驱动', '三家云厂商资本开支约 1,350 亿美元/季'), ('AI 加速器出货', 'KGI 预测；2027 年英伟达约占一半'), ('CoWoS 晶圆', '每片能封的颗数 28 → 6'),
      ('台积电 + 封测厂', '台积电 2027 年末约 18.5 万片/月'), ('约束：载板', 'ABF 载板 / T-glass；中国卡在 HBM')],
 fig_note=f'产能与出货 KGI {S(1)}；每片颗数锚点 {S(9)}；资本开支 {S(39)}。',
 cons=[
  [f'2027 年 CoWoS 对客户需求仍缺 15–20% {S(1)}；台积电称封装限制了客户成长 {S(13)}',
   f'按可见出货只缺约 {CGAP}%，加上点名的客户差额约 {CGAPU}%', '缺口幅度：主流说明显短缺，我们说个位数',
   f'摩根士丹利、UBS 的需求口径和我们差 ±5% {S("4,5")}；2027 年总产能 +71% {S(1)}',
   '2027 年中券商缺口口径 ≥ 25%，或台积电年末 < 16 万片/月 → 我们错（证伪表 J1）'],
  [f'券商对台积电 2027 年末产能分歧大：키움证券只给约 15 万片/月 {S(63)}，404K 汇总的共识 19–20 万 {S(8)}，摩根士丹利 20 万 {S(3)}',
   '取 KGI 约 18.5 万片/月（共识中间）', '分歧小：我们站在共识中间，主要差在需求口径',
   f'KGI 年末产能 12 万 → 18.5 万 {S(1)}；设备交期 10–12 个月，出机节奏决定能否兑现 {S(27)}',
   '台积电 2027 年末 ≥ 18 万片/月（预测 C7）'],
  [f'瓶颈和利润都在台积电 CoWoS {S("1,13")}',
   '2027 年最紧的是 ABF 载板和 T-glass；利润涨得最快的是载板', '约束位置：主流看 CoWoS，我们看载板',
   f'欣兴毛利率 13.1% → 24.8% {S(32)}；日东纺占 T-glass 约 90%，2027 年才放量 {S(23)}；味之素 ABF 提价 30% {S(25)}',
   '欣兴毛利率连续两季 < 20% → 我们错（证伪表 J3）'],
  [f'<b>中国：</b>国产 CoWoS 2027 年翻倍到约 5 万片/月、国产化率超 60%，被当成主线（调研纪要）{S(53)}',
   '2027 年国内 2.5D 会超过 HBM 能配的卡，封装不是长期约束', '国产封装：主流看稀缺，我们看可能过剩',
   f'HBM 页中国账本：2027 年可用 HBM 只够配约 {CK27:.2f} 百万张卡 {S(62)}；国内 2.5D 2027 年能封约 {WK27:.1f} 百万张 {E}',
   '报道里 2027 年国产卡受限主因仍是 HBM（预测 N5）；国内年底产能 < 1.5 万片/月则我们错（CJ1）'],
 ],
 watch=[
  ['封装设备景气见顶', '弘塑 + 辛耘 + 万润 3 个月营收同比（每月 10 日）', '从峰值回落 ≥ 20 个百分点并连降 3 个月 → 约 4 个月后台积电营收同比见顶', '每月；2027-01-12 打分 C2'],
  ['载板利润能否持续', '欣兴（3037）季度毛利率', '连续两季 < 20% → "利润往载板迁移"错', '每季财报'],
  ['需求上一层', '四大云厂商 2027 年首次资本开支指引', '合计 ≥ 8,500 亿美元 → 需求继续上修；增速 < 10% 或任一家下降 → 需求见顶', '2027-02-15'],
  ['CoWoS 缺口口径', '券商对台积电 2027 年缺口和年末产能', '缺口 ≥ 25% 或年末 < 16 万片/月 → "不再是头号瓶颈"错', '2027 年中'],
  ['国产 2.5D 产能', '盛合 / 通富 / 长电年报里的 2.5D 产能', '2026 年底 ≥ 2 万片/月（N1）；< 1.5 万 → 封装比 HBM 更紧', '2027-03-31'],
 ],
)

SPEC = dict(
 logic=LOGIC,
 file='cowos.html', title='CoWoS 先进封装', pill='CoWoS v0.4.2', other=('hbm.html', 'HBM ⇄'),
 scripts=['toc.js', 'cowos.js', 'cowos_cn.js'],
 ledgers=[('a1', 'gl', '全球账本', f'2027 年 CoWoS 只略紧（缺约 {CGAP}%–{CGAPU}%），最紧的是载板，利润往载板迁移'),
          ('cn', 'cnl', '中国账本', f'台积电已不接国产 AI 芯片；2026 年国产 2.5D 和 HBM 一样紧（够 HBM 能配的卡约 {WH26}%），2027 年产能翻倍、让位给 HBM')],
 kicker='CoWoS 小链 · v0.4.2 · 更新 <span id="cw-upd"></span> · 上游接 <a href="hbm.html">HBM 小链</a>',
 card=f'全球账本：2027 年 CoWoS 只略紧（缺约 {CGAP}%–{CGAPU}%），最紧的是载板，设备景气还没见顶。中国账本：台积电已不接国产 AI 芯片，2026 年国产 2.5D 封装和 HBM 一样紧{E}',
 scqa=[
  'AI 加速器要把 GPU 和 HBM 放在同一块硅中介层上（2.5D 封装），台积电 CoWoS 是主力。2023–24 年 H100 缺货，卡的就是 CoWoS。',
  f'CoWoS 产能三年涨了约 9 倍，2027 年总产能还要再涨约七成（台积电年末 12 万 → 18.5 万片/月）{S(1)}；但封装越做越大，每片晶圆能封的芯片从 H100 的约 28 颗掉到 Rubin Ultra 的约 6 颗，片数涨得比颗数快得多。KGI 仍说对客户需求缺 15–20% {S(1)}；而 HBM 页 v0.4 上修供给后，HBM 也只是略紧。',
  '2027 年 CoWoS 还是 AI 芯片的头号瓶颈吗？如果不是，卡在哪、钱流向哪？封装设备的景气什么时候见顶？'],
 gov=GOV,
 mece='三条论点分别回答"量（卡在哪）""利润（钱去哪）""时点（何时见顶）"，互不重叠。中国的账另算（见<a href="#cn">中国账本</a>）：国产 AI 芯片用不了台积电 CoWoS，两本账不重复。',
 args=[
  dict(tag='量', claim=f'2027 年 CoWoS 总量只缺约 {CGAP}%（客户需求口径约 {CGAPU}%），和 HBM 差不多紧；换成同一单位后，最紧的是 ABF 载板',
   key=f'2027 缺口/需求 <b data-from="cw-gap">—</b> · 客户口径 <b data-from="cw-gapu">—</b> · HBM 满足率 <b data-from="cwHHbm">—</b> {E}',
   sub=f'需求 = 加速器出货 ÷ 每片可封颗数 + 其他（交换芯片、FPGA 等）；供给 = 12 个月的（台积电 + 非台积电）月产能 × 有效稼动率。出货来自 KGI 2026-09 预测 {S(1)}，与 HBM 页共用同一张表。',
   hero=dict(src='cw-cBal', step='balance', t='CoWoS 供需（千片/年）：2027 年缺口收窄到个位数', note='跟随底稿第 5 步的滑块实时重算。'),
   ev=[
    dict(t=f'平衡：可见出货口径只缺约 {CGAP}%', b=f'2027 年供给约 {CS27/1000:.2f} 百万片、可见出货所需约 {CD27/1000:.2f} 百万片 {E}；只把 KGI 点名的客户差额（博通、Trainium3、Venice，约 19 万片）加进去，缺口约 {CGAPU}%，仍低于 KGI 的 15–20% {S(1)}。', steps=['balance']),
    dict(t='交叉验证：和券商口径基本一致', b=f'自下而上的 2026/2027 需求 132 万/255 万片，UBS 131 万/248 万，摩根士丹利 139 万/269 万 {S("4,5")}；模型误差约 ±10%，2023–24 年模型缺口 −10%/−14% 与当年 H100 缺货一致。', steps=['balance']),
    dict(t='供给：产能涨得快，设备交期是节奏', b=f'台积电年末产能 12 万 → 18.5 万片/月（2026→2027），加非台积电合计约 +71% {S(1)}；弘塑设备交期 10–12 个月，出机只够需求的 1/3–1/4 {S(27)}。', steps=['supply']),
    dict(t='需求：封装面积通胀，片数涨得比颗数快', b='英伟达 GPU 颗数 2023→2027 涨约 6 倍，消耗的 CoWoS 片数涨约 23 倍；需求的上一层是云厂商资本开支（三家合计从 2023Q2 约 270 亿美元/季涨到 2026Q2 约 1,350 亿）。', steps=['demand']),
    dict(t='和 HBM 对账：两者差不多紧', b=f'同一口径（KGI 可见出货）下，2027 年 CoWoS 够约 {CC}%、HBM 够约 {HC}%，差距在模型误差内 {S(33)}{E}。', steps=['map']),
    dict(t='要害变量："HBM 更紧"只领先约 3.5 个百分点', b=f'HBM 可供量按 KGI 口径 ×1.08、台积电 2027 年末只有 155k、每片颗数 −20%、英伟达降规格，任何一项都会让短板换成 CoWoS {E}。', steps=['key']),
    dict(t='约束推导：最紧的是 ABF 载板（数据最弱）', b=f'日东纺约占 T-glass 90%，福岛扩产到 2027 年才放量；KGI：2027 年 ABF 只 +25–30% {S("23,24,25,1")}{E}。', steps=['neck']),
   ]),
  dict(tag='利润', claim='钱堆在台积电，但利润涨得最快的是扩得慢的载板：欣兴毛利率一年从 13.1% 升到 24.8%',
   key=f'欣兴毛利率 2Q26 <b>24.8%</b>（一年前 13.1%）{S(32)}',
   sub='Bain 利润池画法：宽度 = 年化营收，高度 = 毛利率，面积 = 毛利。各公司都不单独披露 CoWoS 数字，用的是能拿到的最接近口径。',
   hero=dict(src='cw-cMar', step='profit', t='毛利率迁移（季度，MOPS 财报）', note=f'欣兴 2Q25 13.1% → 2Q26 24.8%；日月光 17.0% → 21.0%；台积电 58.6% → 67.7% {S(32)}。'),
   ev=[
    dict(t='利润池：台积电先进封装最大', b=f'按"低双位数"营收占比和"接近公司平均"的毛利率估，台积电先进封装年营收约 210 亿美元、毛利率约 60% {S("14,15")}{E}，比载板、OSAT、测试、设备加起来还大。', steps=['profit']),
    dict(t='毛利率迁移：载板一年接近翻倍', b=f'欣兴 13.1% → 24.8%，日月光 17.0% → 21.0%，台积电 58.6% → 67.7% {S(32)}。利润在往扩得慢的环节迁移。', steps=['profit']),
    dict(t='载板有定价权：约束就在这里', b=f'味之素 ABF 膜提价 30%，载板短缺看到 2028 年 {S("23,24,25")}；扩得慢的环节拿走增量利润。', steps=['neck']),
    dict(t='OSAT 和 EMIB-T 分走的是溢出量，不是利润中心', b='日月光 ATM 毛利 27%，EMIB-T 基板良率才 45%；台积电自家先进封装毛利已接近公司平均。', steps=['play']),
   ]),
  dict(tag='时点', claim='封装设备景气还在上行：设备三家营收同比 +43% 仍在加速、合约负债重回增长；按回测，设备见顶后中位约 4 个月台积电营收同比才见顶',
   key=f'设备三家 3 个月营收同比 <b>+43%</b>（2026-09）{S(31)}',
   sub='台湾设备商、载板厂每月 10 日前公布上月营收。设备营收是在客户验收时确认的，更接近"产能装进去了"；真正领先的是合约负债和 Disco 的出货额。',
   hero=dict(src='cw-cBt', step='lead', t='设备三家、载板三家 vs 台积电、日月光营收（3 个月滚动同比）', h=380, note=f'MOPS 月营收 2012-01 至 2026-09 {S(31)}。'),
   ev=[
    dict(t='回测：同比拐点领先 1–13 个月', b='设备营收和台积电营收的水平相关很弱（r=0.36），但同比拐点比台积电早 1–13 个月（13 次中 11 次，中位 4 个月）。', steps=['lead']),
    dict(t='合约负债重新上升', b=f'设备三家 2Q26 合约负债 185.5 亿新台币，约 2.6 个季度营收，同比 +10% 重新上升；上一轮合约负债同比领先营收同比约 6 个季度（只有一个周期）{S("32,29")}{E}。', steps=['lead']),
    dict(t='历史：瓶颈一直在迁移', b='技术代际推着瓶颈换位置：从中介层产能到 HBM、载板和测试。', steps=['hist']),
    dict(t='玩家：扩产决定和变化信号', b='台积电愿不愿意扩、英伟达锁多少货、ASIC 阵营找不找第二来源、上游材料商敢不敢扩产。', steps=['play']),
   ]),
 ],

 cn=dict(
  nav='中国账本', kicker='中国视角：国产 AI 芯片只能在大陆做的 2.5D 封装（与全球账本口径不重复）',
  scqa=[
   f'初代昇腾 910 由台积电代工 {S(50)}；2024-10 TechInsights 在 910B 里发现台积电 die 后，台积电停供算能 {S(46)}，2024-11 起不再给中国大陆 AI 客户做 7nm 以下芯片 {S(48)}；2025-01 起 16/14nm 以下逻辑芯片须经白名单设计商或封测厂 {S("44,45")}。国产 AI 卡的 2.5D 封装只能在大陆做。',
   f'全球账本里 2027 年 CoWoS 只缺约 {CGAP}%，但大陆 2.5D 主要靠盛合晶微一家（2024 年份额约 85%）{S(51)}，通富、长电刚开始放量 {S(53)}；HBM 页中国账本显示，可用 HBM 2026 年只够配约 {CK26:.2f} 百万张卡 {S(62)}。',
   '国产 2.5D 封装够不够？它和 HBM 谁更紧？ABF 膜、键合机会不会成为下一个卡点？谁受益？'],
  gov=f'中国的 2.5D 封装是和 HBM 并列的第二道墙：台积电这条路已经关死，2026 年国内给国产 AI 卡的 2.5D 刚好够 HBM 能配的卡（约 {WH26}%），只够不缺货需求的约 {WC26}%；2027 年国内产能翻倍、封装让位给 HBM，下一个卡点是 ABF 膜',
  mece='三条中国论点分别回答"够不够""卡在哪""何时缓解、谁受益"。口径：只算国产 AI 卡要用、只能在大陆做的 2.5D 封装（硅中介层 / 有机中介层 / 硅桥）；产能数字主要来自调研纪要，证据弱，结论跟着第 5 步中国块的滑块走。',
  args=[
   dict(tag='平衡', claim=f'2026 年国产 2.5D 和 HBM 一样紧：国内能给国产 AI 卡的约 {WS26/10:.0f} 万片/年，够 HBM 能配的卡约 {WH26}%、够不缺货需求约 {WC26}%；2027 年产能是 HBM 能配卡数所需的约 {WH27/100:.1f} 倍，封装不再是约束',
    key=f'2026 ÷ HBM 能配的卡 <b data-from="wnH26">—</b> · ÷ 不缺货需求 <b data-from="wnC26">—</b> {E}',
    sub='需求 = 要 2.5D 的国产卡 ÷ 每片可封良品颗数；供给 = 年均月产能 × 12 × 给国产 AI 的比例 × 稼动率。需求给两个口径：不缺货需求，和"HBM 能配的卡"（HBM 页中国账本，加上不用标准 HBM 的 950PR）。',
    hero=dict(src='wn-cBal', step='balance', t='中国 2.5D：国产 AI 可用产能 vs 需求（千片/年）', h=330, note='柱 = 国产 AI 可用产能；实线 = 不缺货需求；虚线 = HBM 能配的卡所需。'),
    ev=[
     dict(t='供给：三家合计约 2–2.6 万片/月（2026 规划）', b=f'调研纪要：通富 0.8–1.0 万、盛合 0.6–0.8 万、长电 0.5–0.8 万片/月，2027 年约 5 万 {S(53)}；另一口径：一供 2026-09 为 S 级 7,500 + L 级 2,000 片/月 {S(54)}。两者都是弱证据，公司没有披露。', steps=['supply']),
     dict(t='需求：卡数 × 每片颗数', b=f'2026 年不缺货需求约 500 万张卡（含 950PR 约 75 万颗 {S(61)}），每片按 14 颗 {E}，约 {W[2026]["du"]:.0f} 千片；HBM 只够配约 {CK26:.2f} 百万张 {S(62)}，加 950PR 约 {WHK26:.2f} 百万张。', steps=['demand']),
     dict(t='校验：2025 年反推', b=f'2025 年实际封了约 130 万张用 HBM 的国产卡 {S(62)}，按每片 18 颗至少要约 7 万片 {E}；本页 2025 年底产能 1.3 万片/月就是这样反推的，和盛合 2.5D 收入（2024 年 19.6 亿元、2025H1 16.9 亿元）{S(51)}的增速方向一致。', steps=['supply', 'balance']),
     dict(t='若 HBM 放开，封装马上变成第一约束', b=f'2026 年国内 2.5D 只够不缺货需求的约 {WC26}%、2027 年约 {WC27}% {E}：HBM 一旦松动（灰色渠道变大、长鑫良率超预期），先卡住的就是封装。', steps=['balance']),
    ]),
   dict(tag='约束', claim=f'台积电这条路 2024 年底已经关死；换成"能封多少张卡"，2026 年 2.5D（约 {WK26:.2f} 百万张）和 HBM（约 {WHK26:.2f} 百万张）并列最紧，2027 年只剩 HBM；ABF 膜是下一个卡点',
    key=f'2026 年 2.5D 能封 <b data-from="wnK26">—</b> 张 · HBM 能配 <b data-from="wnHK26">—</b> 张 {E}',
    sub=f'按约束理论（TOC）把每一环换成"能支撑多少张国产卡"，取最小值。前道逻辑不是约束：最多约 2 万片/月中芯产能就能每月出数百万颗 die {S(49)}。',
    hero=dict(src='wn-cToc', step='neck', t='能支撑多少张国产卡（百万张）：2.5D vs HBM', h=300, note='HBM 一栏 = HBM 页中国账本能配的卡 + 不用标准 HBM 的 950PR。'),
    ev=[
     dict(t='台积电：2024-10 → 2025-01 三步关门', b=f'停供算能 {S(46)} → 停供大陆 AI 客户 7nm 以下 {S(48)} → 白名单经手规则 {S("44,45")}；台积电或被罚 10 亿美元以上 {S(47)}。die bank 约 290 万颗，约 9 个月内用完 {S(49)}。', steps=['play', 'neck']),
     dict(t='TOC：2026 年两道墙几乎一样高', b=f'2.5D 能封约 {WK26:.2f} 百万张、HBM 能配约 {WHK26:.2f} 百万张 {E}；2027 年 2.5D 约 {WK27:.2f}、HBM 约 {WHK27:.2f} 百万张，HBM 成为唯一约束。', steps=['neck']),
     dict(t='ABF 膜：味之素 > 95%，大陆自给率 < 5%', b=f'传 2026-08 对华减供 30%（未获第三方印证）{S(55)}；华正 CBF 良率 85%+、小批量供昇腾 {S(56)}；兴森 FCBGA 仍小批量 {S(57)}，深南 22 层及以下量产 {S(58)}。数据不够量化，列为风险。', steps=['neck', 'map']),
     dict(t='中介层与键合机：暂不是约束', b=f'盛合部分 TSV 中介层由客户供料 {S(51)}；普莱信称国产 TCB 已批量出货、支持 CoWoS {S(59)}（公司宣传稿）；华为 910D 专利用硅桥互连 {S(60)}，可能绕开大面积硅中介层。', steps=['neck', 'play']),
    ]),
   dict(tag='时点', claim='国内 2.5D 年底月产能约 1.3 → 2.3 → 5 万片（2025–27，纪要口径）；受益顺序：2.5D 封装（盛合，证据强）→ 载板（兴森、深南）→ ABF 类膜（华正等，证据中/弱）',
    key=f'年底月产能 <b>1.3 → 2.3 → 5 万片</b>（2025–27）{E}',
    sub='时间表来自监管文件、公司公告和调研纪要。A 股按证据强度分级：强 = 公司公告 / 交易所文件；中 = 媒体或机构；弱 = 纪要或自媒体。',
    hero=dict(src='wn-cCap', step='supply', t='国内 2.5D 年底月产能（千片/月）与国产 AI 可用部分', h=300, note='2024–25 年为反推（估），2026–27 年为纪要口径（弱）。'),
    ev=[
     dict(t='时间表：关门 → die bank → 国产扩产', b=f'2024-11 台积电停供 {S(48)} → 2025 年靠 die bank {S(49)} → 2026-04 盛合上市 {S(52)} → 2026 年底约 2–2.6 万片/月 {S(53)} → 2027 年约 5 万 {S(53)}。', steps=['neck']),
     dict(t='玩家：谁的决定会改变这本账', b=f'BIS 和台积电会不会再补漏洞 {S("44,47")}；华为会不会自建封装（纪要称华为系封装厂已切入二供 {S(54)}）；味之素会不会真的减供 {S(55)}。', steps=['play']),
     dict(t='A 股：按环节，证据强度分级', b=f'强：盛合晶微（688820）{S(51)}、兴森科技 {S(57)}、深南电路 {S(58)}；中：华正新材、莲花控股 {S("55,56")}；弱：通富微电、长电科技（2.5D 产能只有纪要）{S(53)}、华天科技、宏昌电子、生益科技。', steps=['map']),
    ]),
  ]),
 wrong='''<p class="sub">每条判断：现在已经看到的反方证据、什么情况算我错、看哪个公开指标、阈值多少。J1/J2↔论点①、J3↔论点②、J5↔论点③，J4 是需求的上一层（云厂商资本开支）。三个核心争议的完整论证见 <a href="#debate">底稿第 1 步</a>。触发阈值就改判断，不辩护。</p>
<div class="tbl"><table id="cw-falT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：CJ1–CJ3</h3><p class="sub">CJ1↔中国论点❶、CJ2/CJ3↔❷。</p>
<div class="tbl"><table id="wnFalT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 pred='''<p class="sub" id="cw-predSum"></p><p class="sub">到期后按公开数据打分，不改原文，只追加结果。C 系列是本链判断，T 系列是约束迁移（与 HBM 页共用），N 系列是中国账本。</p>
<div class="tbl"><table id="cw-predT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<div id="cw-tpred"></div>
<h3>中国账本：N 系列（2026-10-15 写入）</h3><p class="note" id="wnPredS"></p>
<div class="tbl"><table id="wnPredT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 base_title='CoWoS 产业链底稿',
 base_sub='上面的结论都从这里来。按 SOP 顺序：先找要害变量和争议，再定边界、算供需、看利润和约束，最后看玩家、历史、领先指标和公司。右侧圆圈 = 这一步支撑哪条论点。',
 steps=[
  dict(id='key', h='哪个假设能把结论翻过来', body='''<p class="note" id="cw-torNote"></p>
<div class="grid g2"><div class="card"><b>2027 年 CoWoS 缺口对各假设的敏感度</b><div id="cw-cTorA" class="chart" style="height:300px"></div><div class="note">每一行：只把这个变量调到低端（蓝）/高端（红），其他不动，2027 年缺口变成多少。条越长越要害。虚线 = 缺口为 0。</div></div>
<div class="card"><b>"HBM 比 CoWoS 更紧"这个结论有多稳</b><div id="cw-cTorB" class="chart" style="height:300px"></div><div class="note">指标 = CoWoS 满足率 − HBM 满足率（同一口径：KGI 可见出货，百分点），大于 0 表示 HBM 更紧。HBM 页 v0.4 上修供给后，基准只剩约 +3.5pp：HBM 可供量按 KGI 口径 ×1.08、台积电 2027 年末只有 155k、每片颗数 −20%、英伟达降规格，任何一项都会让短板换成 CoWoS。所以结论是<b>两者差不多紧</b>，不是"HBM 是短板"。<span class="tag t-est">估</span></div></div></div>'''),
  dict(id='debate', h='三个可证伪的核心争议', ctx='对应结论层「可能错在哪」↑', body='<div class="grid g3" id="cw-deb"></div>'),
  dict(id='proc', h='先进封装有哪几种，CoWoS 是怎么做出来的', ctx='背景：定义单位与边界', sub='计量单位：需求和产能用 12 寸 CoWoS 晶圆（片/月、片/年），出货用颗（封装）。一片 CoWoS 晶圆能封几颗芯片，取决于中介层面积，这是整条链的第一性原理。',
   body='''<h3>技术路线对比</h3><div class="tbl"><table id="cw-varT"><thead><tr><th>方案</th><th>结构</th><th>尺寸</th><th>典型产品</th><th>现状</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<h3>CoWoS 工序 → 设备 / 材料 / 供应商</h3><div class="tbl"><table id="cw-procT"><thead><tr><th>工序</th><th>要点</th><th>设备 / 材料 / 供应商</th><th>来源</th></tr></thead><tbody></tbody></table></div>'''),
  dict(id='demand',
  cn=dict(h='国产卡要多少 2.5D：不缺货需求 vs HBM 能配的卡', body=f'''<div class="tbl"><table id="wn-demT" class="stack"><thead><tr><th>年份</th><th>口径</th><th>算法</th><th>依据</th><th>需求（千片）</th></tr></thead><tbody></tbody></table></div>
<div class="note">每片可封良品颗数只有两个公开锚点（H100 约 28、B200 约 16 {S(9)}），国产卡按同类封装尺寸套用并计入较低良率 {E}；第 5 步中国块可调。950PR 的内存是否算 HBM 有争议（<a href="hbm.html#cn-demand">HBM 页证据表</a>），但它是 2 个 AI die 的大封装，本页按也要 2.5D 算 {E}。</div>'''),
  h='需求：谁在拉动，封装面积通胀，上一层是云厂商资本开支', body=f'''<div class="grid g2"><div class="card"><b>需求由谁拉动（千片/年）</b><div id="cw-cMix" class="chart"></div><div class="note">点柱子看每个产品的"出货 ÷ 每片颗数"。2027 年英伟达占比从约 57% 降到约 48%，谷歌 TPU 和 AMD（含 Venice CPU）是最大增量。</div></div>
<div class="card"><b>封装面积通胀：片数涨得比颗数快</b><div id="cw-cInf" class="chart"></div><div class="note">英伟达 GPU 颗数 2023→2027 涨约 6 倍，消耗的 CoWoS 片数涨约 23 倍（对数坐标）。<b>所以"CoWoS 产能 +70%"不等于"GPU +70%"。</b></div></div></div>
<h3>每片可封颗数（单耗）</h3><div class="tbl"><table id="cw-ppwT"><thead><tr><th>产品</th><th>每片良品颗数</th><th>每封装 HBM</th><th>依据</th></tr></thead><tbody></tbody></table></div>
<h3>需求的上一层：云厂商资本开支与 AI 回报</h3>
<div class="grid g2"><div class="card"><b>亚马逊、微软、谷歌季度资本开支（柱）与积压订单（虚线）</b><div id="cw-cDrv" class="chart" style="height:360px"></div><div class="note">十亿美元，取自各公司财报（Midgard Finance 汇编）{S(39)}。微软为含融资租赁口径，三家口径不完全一致。</div></div>
<div class="card"><table id="cw-drvT"><tbody></tbody></table><div class="note" style="margin-top:8px">链条：云收入/积压订单 → 资本开支 → 加速器订单 → CoWoS 片数。资本开支从 2023Q2 的约 270 亿美元/季涨到 2026Q2 的约 1,350 亿美元/季（三家合计），积压订单一年翻倍以上，是 2027 年需求的底气；反方证据是 AWS 资产回报在下降。</div></div></div>'''),
  dict(id='supply',
  cn=dict(h='国内 2.5D 产能：谁有多少', body=f'''<div class="grid g2"><div class="card"><div id="wn-cCap" class="chart" style="height:300px"></div><div class="note">深色 = 国产 AI 可用部分（× 给国产 AI 的比例 × 稼动率）；浅色 = 其余（海外客户、其他芯片）{E}。</div></div>
<div class="card"><div class="tbl"><table id="wn-supT" class="stack"><thead><tr><th>年底</th><th>月产能</th><th>依据</th></tr></thead><tbody></tbody></table></div></div></div>
<div class="note">中芯国际没有规模量产 CoWoS 类封装 {S(53)}。盛合 2.5D 收入 2024 年 19.6 亿元、2025H1 16.9 亿元 {S(51)}，作为对照：台积电先进封装年营收约 210 亿美元（全球账本第 6 步）。</div>'''),
  h='供给：季末产能与各家预测', body=f'''<div class="card"><b>季末产能（千片/月）</b><div id="cw-cCap" class="chart" style="height:360px"></div><div class="note">面积 = KGI 口径，年末为锚点，季度为线性插值 {E}；圆点 = 各家对台积电年末产能的预测。</div>
<div class="tbl"><table id="cw-capT" style="margin-top:8px"><thead><tr><th>机构</th><th>日期</th><th>2026 年末</th><th>2027 年末</th><th>其他</th><th>来源</th></tr></thead><tbody></tbody></table></div></div>'''),
  dict(id='balance',
  cn=dict(h='中国 2.5D 平衡：拖动假设', body=f'''<div class="grid g2"><div class="card">
<div class="ctl">
<label>2026 年底国内 2.5D 月产能（千片）<output id="wno1"></output></label><input type="range" id="wns1" min="12" max="35" step="1" value="23">
<label>2027 年底国内 2.5D 月产能（千片）<output id="wno2"></output></label><input type="range" id="wns2" min="25" max="70" step="5" value="50">
<label>给国产 AI 卡的比例 <output id="wno3"></output></label><input type="range" id="wns3" min="40" max="100" step="5" value="70">
<label>每片可封颗数（相对基准）<output id="wno4"></output></label><input type="range" id="wns4" min="70" max="130" step="5" value="100">
</div><button class="btn" onclick="wnReset()">恢复基准</button>
<div class="grid g2" style="margin-top:14px;gap:8px"><div><div class="note">2026 ÷ HBM 能配的卡</div><div class="big" id="wnH26"></div></div><div><div class="note">2026 ÷ 不缺货需求</div><div class="big" id="wnC26" style="color:var(--warn)"></div></div></div>
<div class="note" id="wnTxt"></div><span id="wnK26" hidden></span><span id="wnHK26" hidden></span>
</div><div class="card"><div id="wn-cBal" class="chart" style="height:330px"></div><div class="note">纪要口径如果高估一半（2026 年底 1.2 万、2027 年底 2.5 万片/月），2026 年只够 HBM 能配的卡约七成、2027 年约九成：结论从"并列"变成"封装更紧"。{E}</div></div></div>'''),
  h='平衡：自己拖动假设', sub='需求 = 加速器出货 ÷ 每片可封颗数 + 其他；供给 = 12 个月的（台积电 + 非台积电）月产能 × 有效稼动率。浏览器里实时重算，结论层的图跟着变。CoWoS 没有公开报价，单位价值见第 6 步。', body=f'''<div class="grid g4" id="cw-stats"></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><div class="ctl">
<label>台积电 2027 年末产能 <output id="cw-o-cap"></output></label><input type="range" id="cw-cap" min="150" max="220" step="5" value="185">
<label>非台积电 2027 年末产能 <output id="cw-o-os"></output></label><input type="range" id="cw-os" min="40" max="110" step="5" value="80">
<label>2026–27 有效稼动率 <output id="cw-o-ut"></output></label><input type="range" id="cw-ut" min="80" max="100" step="1" value="95">
<label>2027 每片可封颗数（相对基准）<output id="cw-o-ppw"></output></label><input type="range" id="cw-ppw" min="80" max="120" step="5" value="100">
<label>2027 加速器出货（相对 KGI）<output id="cw-o-dem"></output></label><input type="range" id="cw-dem" min="70" max="130" step="5" value="100">
<label>2027 每封装 HBM 容量（相对基准）<output id="cw-o-hbm"></output></label><input type="range" id="cw-hbm" min="60" max="110" step="5" value="100">
</div><button class="btn" onclick="resetS()">恢复基准</button>
<div class="grid g2" style="margin-top:16px;gap:8px"><div><div class="note">2027 缺口（可见出货口径）</div><div class="big" id="cw-gap"></div></div><div><div class="note">客户需求口径</div><div class="big" id="cw-gapu" style="color:var(--warn)"></div></div></div><div class="note" id="cw-gapTxt"></div>
</div><div class="card"><div id="cw-cBal" class="chart"></div>
<div class="note">出货来自 KGI 2026-09 预测 {S(1)}，每片颗数为自估（锚点 H100≈28、B200≈16 {S(9)}）{E}。"客户需求口径"只加了 KGI 点名的差额（博通 50 万 vs 38–39 万片、Trainium3 350 万 vs 300 万颗、Venice 600 万 vs 450–500 万颗），约 19 万片。黑色菱形/灰色三角是摩根士丹利、UBS 的需求口径 {S("4,5")}。</div></div></div>
<div class="card" style="margin-top:14px"><b>交叉验证</b><div class="note" style="font-size:13px">① 自下而上的 2026/2027 需求 132 万/255 万片，和 UBS（131 万/248 万）几乎一样，比摩根士丹利（139 万/269 万）低 5%。② 英伟达 2027 年 122 万片（本模型）对摩根士丹利 122.2 万、404K 汇总的 119.6–122.2 万片，基本一致 {S(8)}。③ 2025–26 年模型显示总量略有富余（+5%～+7%），和"全年紧缺"的公开说法不一致：紧张主要来自 S/R 型号错配（KGI）和爬坡良率，而不是总片数。模型误差约 ±10%。④ 2023–24 年模型缺口 −10%/−14%，与当年 H100 缺货一致。</div></div>'''),
  dict(id='profit', h='利润池：钱堆在台积电，利润增速最快的是载板', body=f'''<div class="card"><div id="cw-cPool" class="chart" style="height:330px"></div><div class="tbl"><table id="cw-poolT"><thead><tr><th>环节</th><th>营收（十亿美元/年）</th><th>毛利率</th><th>毛利</th><th>口径</th></tr></thead><tbody></tbody></table></div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>毛利率迁移（季度，MOPS 财报）</b><div id="cw-cMar" class="chart"></div><div class="note">欣兴（载板）毛利率 2Q25 13.1% → 2Q26 24.8%，一年接近翻倍；日月光 17.0% → 21.0%；台积电 58.6% → 67.7% {S(32)}。利润正在往扩得慢的环节（载板）迁移。</div></div>
<div class="card"><b>资本开支与单位价值</b><table id="cw-capexT" style="margin-top:6px"><tbody></tbody></table><table id="cw-ucT" style="margin-top:10px"><tbody></tbody></table><div class="note">台积电先进封装：魏哲家 2024 年说毛利率"以前远低于公司平均，现在接近公司平均" {S(15)}；占营收 2024 约 8%、2025 略超 10%、2026 预计"低双位数" {S(14)}。</div></div></div>'''),
  dict(id='neck',
  cn=dict(h='中国的约束：换成"能支撑多少张国产卡"', body=f'''<div class="tbl"><table id="wn-tocT" class="stack"><thead><tr><th>环节</th><th>2026 年能支撑</th><th>依据</th><th>判断</th></tr></thead><tbody></tbody></table></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><div id="wn-cToc" class="chart" style="height:300px"></div><div class="note">跟随第 5 步中国块滑块；HBM 一栏来自 <a href="hbm.html#cn">HBM 页中国账本</a>基准 {S(62)}。</div></div>
<div class="card"><b>国产化时间表</b><div class="tl" style="margin-top:10px" id="wn-tl"></div></div></div>'''),
  h='约束推导：把每一环换成同一单位，最小的那个才是约束', sub='按 Goldratt 约束理论（TOC）：CoWoS 晶圆 → 封装颗数，DRAM 晶圆 → HBM GB → 封装，键合机台数 → 堆叠数 → 封装，载板片数、数据中心电力 → 封装，统一成"百万颗 AI 加速器封装/季"，每季取最小值。滑块改任何一环，约束实时更新。',
   body='<div id="cw-toc"></div>\n<h3>汇总排序（推导结果 + 定性证据）</h3><p class="sub">条形长度 = 缓解所需月数（示意）。</p><div id="cw-neck" class="grid"></div>'),
  dict(id='play',
  cn=dict(h='中国账本的玩家：谁的决定会改变这本账', body='<div class="grid g2" id="wnPl"></div>'),
  h='谁在做什么决定，为什么，什么信号说明他们变了', sub='供需表是结果，玩家的决策是原因：台积电愿不愿意扩、英伟达锁多少货、ASIC 阵营找不找第二来源、上游材料商敢不敢扩产。', body='<div class="grid g2" id="cw-play"></div>'),
  dict(id='hist', h='技术代际与瓶颈迁移', body='''<p class="sub" id="cw-rule"></p>
<div class="grid g2"><div class="card"><b>技术与格局</b><div class="tl" style="margin-top:12px" id="cw-tl1"></div></div>
<div class="card"><b>产能与瓶颈迁移</b><div class="tl" style="margin-top:12px" id="cw-tl2"></div></div></div>'''),
  dict(id='lead', h='先看哪个数据（已回测）', sub='回测结论：设备营收和台积电营收的<b>水平相关很弱</b>（r=0.36），但<b>同比拐点</b>比台积电早 1–13 个月（13 次中 11 次，中位 4 个月）；设备营收是在客户验收时确认的，更接近"产能装进去了"，真正领先的是合约负债和 Disco 的出货额。', body=f'''<div class="card"><b>回测：设备三家、载板三家 vs 台积电、日月光营收（3 个月滚动同比）</b><div id="cw-cBt" class="chart" style="height:380px"></div><div class="note">MOPS 月营收（经 FinMind API 下载）2012-01 至 2026-09 {S(31)}；同比截断在 −80%～+250% 以便显示。设备三家 = 弘塑 3131 + 辛耘 3583 + 万润 6187；载板三家 = 欣兴 3037 + 南电 8046 + 景硕 3189。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>交叉相关：A 领先 k 个月时与 B 的相关系数</b><div id="cw-cXc" class="chart" style="height:280px"></div><div class="note">设备→台积电最高在 k=+3（0.36），载板→台积电最高在 k=0～1（0.55，同步）。样本 2014–2026，约 153 个月。</div></div>
<div class="card"><b>拐点对照：设备三家同比 → 台积电营收同比</b><div class="tbl"><table id="cw-tpT"><thead><tr><th>设备同比拐点</th><th>台积电同比拐点</th><th>领先（月）</th></tr></thead><tbody></tbody></table></div><div class="note" id="cw-btNow"></div></div></div>
<div class="card" style="margin-top:14px"><b>合约负债（预收款）vs 当季营收：设备三家合计</b><div id="cw-cCl" class="chart" style="height:280px"></div><div class="note">合约负债同比在 1Q23 见顶（+89%），营收同比在 3Q24 见顶（+87%），领先约 6 个季度，但只有这一个周期 {E}。2Q26 合约负债 185.5 亿新台币，约等于 2.6 个季度的营收，同比 +10% 重新上升 {S("32,29")}。</div></div>
<div class="grid g3" id="cw-lead" style="margin-top:14px"></div>'''),
  dict(id='ledger', h='预测台账放在结论层', ctx='台账在结论层「预测台账」↑', body='<p>C 系列（本链判断）和 T 系列（约束迁移，与 HBM 页共用）都在 <a href="#pred">结论层 · 预测台账</a>；每条判断的反方证据和证伪阈值在 <a href="#wrong">可能错在哪</a>。规则：到期按公开数据打分，不改原文，只追加结果；作废要写原因并保留原文。</p>'),
  dict(id='map',
  cn=dict(h='A 股受益：按环节，标明证据强度', body=f'''<p class="sub">2.5D 专项营收只有盛合晶微在招股书里披露。"强"= 公司公告或交易所文件；"中"= 媒体或机构；"弱"= 调研纪要或自媒体。</p>
<div class="tbl"><table id="wn-coT" class="stack"><thead><tr><th>环节</th><th>公司</th><th>代码</th><th>与国产 2.5D 的关系</th><th>证据强度</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">和 HBM 页对账：本页读取 HBM 页中国账本的"能配的卡"（2026 / 2027 年约 {CK26:.2f} / {CK27:.2f} 百万张）{S(62)}；HBM 页约束表里的"2.5D 先进封装"一行读取本页结果。</div>'''),
  h='环节 → 公司 → 订单与资本；和 HBM 对账', sub='点节点看详情；实线边都附来源编号（绿=供货，橙=设备/材料订单）。虚线只表示公司在这个环节有业务，<b>CoWoS 专项营收占比基本都没有披露</b>。', body=f'''<div class="seg" id="cw-fMk"><button class="on" data-m="all">全部</button><button data-m="A">A股</button><button data-m="TW">台</button><button data-m="US">美/欧/日</button><button data-m="HK">港</button></div>
<div class="grid" style="margin-top:12px"><div class="card" style="padding:6px"><div id="cw-cNet" class="chart" style="height:600px"></div><div class="note" style="padding:0 6px">手机上按环节分簇固定排布（方块=环节，圆点=公司，长名称显示代码），可双指缩放、拖动；电脑上为力导向布局。</div><div style="display:flex;justify-content:flex-end;padding:4px 6px"><button class="btn" onclick="CH.net('cw-cNet','#cw-nodeInfo',J.companies,mk)">重置视图</button></div></div>
<div class="card" id="cw-nodeInfo"><b>点击图中任一节点</b><div class="note">显示代码、角色与关联边及来源。</div></div></div>
<h3>公司清单</h3><div class="tbl"><table id="cw-coT"><thead><tr><th>公司</th><th>代码</th><th>环节</th><th>角色/数据</th></tr></thead><tbody></tbody></table></div>
<div id="iface"><h3>对外接口：和 HBM 串起来，谁是木桶短板</h3>
<p class="sub">本页直接读取 <a href="hbm.html#iface">HBM 小链</a>的供给模型，和本页"按出货算出的 HBM 需求"对账。拖动第 5 步的第 6 个滑块（每封装 HBM 容量），可以看英伟达"降规格"能缓解多少。</p>
<div class="grid g2"><div class="card"><div id="cw-cIf" class="chart" style="height:300px"></div><div class="note" id="cw-ifTxt"></div></div>
<div class="card"><b>反向对账（已在 HBM 页 v0.4 修正）</b><div class="note" style="font-size:13px">上一版发现：按 KGI 出货算，2026 年要 HBM 约 3.8 EB，比 HBM 页旧模型供给（2.9 EB）高约 30%。HBM 页 v0.4 改用券商产量校准（iM 证券：2025 年 26.3 亿 GB、2026 年 44.4 亿 GB）和 UBS 年末产能，2026 年供给约 4.4 EB，已高于出货所需；2027 年见左图。{S(33)}</div></div></div>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>输出</th><th>2026</th><th>2027</th><th>说明</th></tr></thead><tbody id="cw-ifT-b"></tbody></table></div>
<p class="card" style="margin-top:12px"><b>约束公式</b><br><span id="cw-formula"></span></p></div>'''),
 ],
 src_small='均于 2026-10-15 打开 · 局限',
 src='''<p class="sub">均于 2026-10-15 用 curl 或浏览器打开（Reuters 401 例外，用搜索摘要；Digitimes 付费墙只看标题）。券商数据多为二手转述，标在标题里。</p><ol class="src" id="cw-srcL"></ol>
<h3>局限（公开数据补不了的）</h3><ul style="font-size:14px" id="cw-lim"></ul>''',
 log='''<div class="tbl"><table id="cw-logT"><tbody></tbody></table></div>
<p><a href="cowos/cowos_model.xlsx">下载模型 Excel</a> · <a href="cowos/cowos_chain.md">报告原文 (Markdown)</a> · <a href="SOP.md">小链研究 SOP</a> · 构建：<code>./build.sh</code>（页面 <code>tpl/page.py</code> + <code>cowos/page.py</code>）</p>''',
)
