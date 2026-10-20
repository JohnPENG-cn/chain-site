"""PCB 页内容 spec（逻辑层 + 结论层 + 底稿 13 步 + 中国账本）。由 tpl/page.py 渲染成 pcb.html。
数字全部来自 pcb/build.py 写出的 pcb_data/model_out.json（不手写）；来源编号来自 pcb/src.py。"""
import json, os, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R0, 'pcb'))
from src import ID
O = json.load(open(os.path.join(R0, 'pcb_data', 'model_out.json')))


def S(*k):
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{ID[x]}">源{ID[x]}</a>' for x in k) + '</span>'


E = '<span class="tag t-est">估</span>'
p = lambda v: f'{v*100:.0f}%'
R26, R27, X, A = O['R']['2026'], O['R']['2027'], O['X'], O['A']
CU, GF, CCL, DR, ABF = p(R27['cu']), p(R27['gf']), p(R27['ccl']), p(R27['dr']), p(X['abf']['2027'])
PER, M9, UPM, FBM, BT, CN = O['PER'], O['M9'], O['UPM'], O['FBM'], O['BTS'], O['CN']
M9L, M9H = f"{M9['lo_s']*100:.0f}", f"{M9['hi_s']*100:.0f}"
CB, CBU = CN['cb'], CN['cbu']
GAP = (R27['cu'] - X['abf']['2027']) * 100

GOV = f'2027 年 PCB 链卡规格、不卡出货：HVLP4 铜箔最紧（约 {CU}，与 ABF 载板打平），利润往上游材料走'

LOGIC = dict(
 title='PCB 一屏看懂：供需怎么走、卡在哪、预期差在哪',
 qa=[
  (f'AI 服务器 PCB 2027 年面积翻倍（130 → 260 万 m²），市场约 375 亿美元 {S("gs")}；每颗加速器的 PCB 价值约 {PER["2026"]:,} → {PER["2027"]:,} 美元 {E}',
   f'国产卡被 HBM 卡在约 {CN["WHK27"]*100:.0f} 万张（2027）{S("hbm")}，所需 PCB 只占三家龙头产值约 {CB["fab"]["share"]*100:.0f}% {E}'),
  (f'PCB 链最紧的是 HVLP4 铜箔：2027 年按目标规格只够约 {CU}，和 ABF 载板（{ABF}）打平 {E}；材料能降一级用，卡的是规格和价格',
   f'墙是 HBM，不是 PCB；国内 PCB 链的短板在 Low-CTE 纱（日东纺 85%）{S("hh")}、HVLP5 和进口开槽机 {S("uad")}'),
  (f'主流按 M9 2027 年占 AI 覆铜板 41% 算 {S("gs")}；正交背板推迟、CPX 移除后，我们估只有 {M9L}–{M9H}% {E}；利润在往上游材料走',
   f'主流把二代布、Q 布当国产替代主线；大陆二代布 2027Q4 起新增 4–5 亿米 {S("jy")}，可能先过剩，更稀缺的是高端铜箔'),
 ],
 terms='名词：<b>PCB</b> = 印制电路板；<b>CCL</b> = 覆铜板（铜箔 + 玻纤布 + 树脂压成，PCB 的基材），M6 → M9 是按松下 Megtron 分的等级，数字越大信号损耗越低；<b>HVLP</b> = 极低轮廓铜箔，表面越平损耗越小（HVLP4/5 最高）；<b>Low-Dk / Q 布</b> = 低介电玻纤布 / 石英布；<b>满足率</b> = 供给 ÷ 需求。',
 three=[f'AI 服务器的 PCB 越做越厚、材料越来越贵：VR200 每柜 PCB 价值是 GB300 的约 3.3 倍 {S("ms")}，2027 年 AI PCB 面积再翻倍 {S("gs")}。',
        f'板厂和压机一两年就能扩（台光电 2027 年底产能 +51%）{S("emcir")}；扩不快的是上游材料——HVLP4 铜箔、二代布、钻针 2027 年只够需求的 72–90% {E}。但它们都能降一级用，所以缺口变成涨价和利润上移，真正卡出货的仍是 ABF 载板（CoWoS 页）。',
        '中国是这条链的主产地（板厂、钻针、Q 布已在前列），国产卡被 HBM 卡住、用不完国内 PCB 产能；国内的短板在 Low-CTE 纱、HVLP5 和进口设备。'],
 keys=[(CU, '2027 年 HVLP 铜箔满足率（目标规格）'), (ABF, '2027 年 ABF 载板（CoWoS 页）'), (f'+{UPM:.1f}pp', f'上游毛利率一年中位变化（板厂 +{FBM:.1f}pp）')],
 fig=[('需求驱动', '云厂商资本开支 → AI 加速器（KGI）'), ('AI 服务器 PCB', '2027 年 260 万 m²、约 375 亿美元'), ('覆铜板 CCL', 'M8/M9；台光电 615 → 930 万张/月'),
      ('上游材料', 'HVLP4 铜箔 · 二代布 · 钻针'), (f'约束：铜箔 ≈ ABF', f'2027 年 PCB 链最紧 {CU}，ABF {ABF}')],
 fig_note=f'需求与市场规模 {S("gs")}；台光电产能 {S("emcir")}；铜箔 {S("gscu", "gscu2")}；ABF 读 CoWoS 页 {S("cowos")}。满足率是 Kiko 按来源口径换算的 {E}。',
 cons=[
  [f'2027 年 M9 及以上占 AI 覆铜板 41%（90 亿美元），背板约 2,000 套（高盛）{S("gs", "gsx")}',
   f'只有约 {M9L}–{M9H}%（中值约 {M9["mid_s"]*100:.0f}%）{E}', 'M9 渗透节奏：主流按背板 / CPX 都上，我们按推迟算',
   f'Kyber 推迟到 2028 {S("kyber")}；CPX 移除 {S("cpx")}；Rubin 计算板用 M8 {S("doosan")}；台光电 M9 2027 年营收占比只是"双位数" {S("udn1")}',
   '台光电 2027 年 M9 占比 ≥ 30%，或第三方 M9 占比 ≥ 35% → 我们错（J2 / C2）'],
  [f'高端铜箔 2027 年缺 39%，8 月上修到 45–55%；只有金居是合格二供（高盛）{S("gscu", "gscu2")}',
   f'缺口差不多，略小：按目标规格满足约 {CU}（高盛口径约 67%）{E}', '小：差在大陆 HVLP4 能否通过认证',
   f'德福 8 月 HVLP4 约 70 吨、良率 60%+ {S("defu")}；铜冠 HVLP4 量产 {S("tongguan")}；金居 2027 年 700–800 吨/月 {S("uacu")}',
   '德福 2026-12 HVLP4 ≥ 150 吨/月（N1）；< 100 吨则大陆增量归零（CJ2）'],
  [f'玻纤布最紧：二代布 2027 年缺口超 40%（广发）{S("gf")}；Kyber 推迟后上游玻纤布、CCL 最受益（杰富瑞）{S("jef")}',
   f'二代布 2027 年偏紧但 2027Q4 后可能转松；最耐久的是 HVLP4/5 铜箔 {E}', '哪个材料先松',
   f'大陆 2027Q4–2028Q2 新增 4–5 亿米 vs 2027 年总需求 2–3 亿米 {S("jy")}；日东纺称客户用 NE 布替代 NER {S("nqa")}；三井 HVLP 到 FY28 才 1,200 吨 {S("mitsui")}',
   '2027 年内二代布报价环比跌 ≥ 15%（C8）→ 我们对'],
  [f'AI 板厂量价齐升，扩产就是份额（A 股 20 家扩产超 800 亿元）{S("capex")}',
   f'增量利润在往上游走：上游毛利率一年中位 +{UPM:.1f}pp，板厂 +{FBM:.1f}pp，胜宏 −3.0pp', '利润位置：主流看板厂，我们看材料',
   f'富乔 24.5% → 40.0%、尖点 29.4% → 41.8%、金居 18.9% → 27.4% {S("fm")}；胜宏 36.2% → 33.2% {S("shhk")}',
   '2027H1 胜宏毛利率 ≥ 36% 且金居 < 25% → 我们错（J3）'],
  [f'<b>中国：</b>国产替代主线是 Q 布、二代布（菲利华、宏和等），2027–28 年放量 {S("gsq", "qy")}',
   '国产卡被 HBM 卡住，PCB 链不是国产卡的约束；最稀缺的国产替代是 HVLP4/5 铜箔，二代布和板厂扩产最集中', '国产替代：主流看玻纤布，我们看铜箔',
   f'国产卡 2027 年所需 PCB 只占三家龙头产值约 {CB["fab"]["share"]*100:.0f}% {E}；大陆二代布新增 4–5 亿米 {S("jy")}',
   '2027 年国产卡因 PCB 缺货延期（CJ1）→ 我们错'],
 ],
 watch=[
  ['CCL 景气见顶', 'CCL 三家（台光电 + 台燿 + 联茂）3 个月营收同比（每月 10 日）', f'从峰值回落 ≥ 30 个百分点并连降 3 个月 → 约 {BT["med"]:.0f} 个月后 AI 板厂营收同比见顶（回测）', '每月；C7'],
  ['M9 节奏', '台光电法说会 M9 营收占比；GTC 2027 的 Kyber 时间表', 'M9 占比 ≥ 30% → 预期差错（J2）；Kyber 2027 年量产 → C3 错', '2027-03 / 2028-01'],
  ['HVLP4 能否放量', '德福 / 金居月出货与良率；高盛缺口口径', '德福 ≥ 150 吨/月（2026-12）、金居 ≥ 500 吨/月（2027 年中）→ 铜箔缺口收窄', '2027-01 / 2027-07'],
  ['板厂利润', '胜宏、沪电季度毛利率', '胜宏连续两季 < 30% → 板厂先被挤压；回到 ≥ 36% → 利润迁移判断错（J3）', '每季财报'],
  ['二代布价格', '国内二代布 / Q 布报价', '2027 年内环比跌 ≥ 15% → 玻纤布先松（C8）', '每月'],
 ],
)

# ---------------- 第 7 步：TOC 推导块
TOCBLOCK = f"""<div class="card"><b>推导过程（每一步都能在 Excel「TOC」「环节依据」表复核）</b><ol style="font-size:14px;margin:8px 0 0 18px;line-height:1.7">
<li><b>定单位</b>：和 HBM、CoWoS 页用同一个分母——KGI 的 AI 加速器出货（不含 Vera / Venice CPU）：2025 / 2026 / 2027 年 {A['2025']:.2f} / {A['2026']:.2f} / {A['2027']:.2f} 百万颗，直接读 CoWoS 页模型 {S('kgi', 'cowos')}。</li>
<li><b>每一环换算</b>：能支撑的加速器 = 该环节的满足率（来源自己的供给 ÷ 需求，按目标规格）× 当年加速器颗数。隐含假设：各环节的需求和加速器出货同比例（交换机、光模块用的高速材料也在需求里）{E}。交叉验证：高盛 AI PCB 市场 ÷ KGI 颗数 = 每颗约 {PER['2027']:,} 美元（2027），摩根士丹利自下而上 VR200 约 1,621 美元/GPU {S('ms')}，同一量级。</li>
<li><b>铜箔</b>：高盛 5 月缺口 28% / 39%（2026 / 27）{S('gscu')}，8 月上修到 45–55% {S('gscu2')}；取 2027 年 50% → 1 ÷ 1.5 = 67%，加大陆 HVLP4 +150 吨/月 ÷ 需求约 {O['CU']['d27']:,.0f} 吨/月 → <b>{CU}</b> {E}。</li>
<li><b>二代布</b> {GF}（广发 60% ~ 纪要 ≥ 100% 的中间）{S('gf', 'jy')}；<b>覆铜板</b> {CCL}（台光电年均产能 ×{O['CCLg']:.2f} × 高阶占比 ×1.15 ÷ 高盛张数 ×1.86）{S('emcir', 'gs')}；<b>钻针</b> {DR}（优分析供需表）{S('uad')}；<b>ABF 载板</b> {ABF}（读 CoWoS 页，不重复）{S('cowos')}。</li>
<li><b>取最小值</b>：2027 年 PCB 链内最紧 = 铜箔 {CU}，比 ABF 高约 {GAP:+.0f} 个百分点——在误差内打平。<b>校准</b>：2026 年铜箔按同一算法只够约 {p(R26['cu'])}，但没有任何公开报道说 AI 机柜因铜箔减产 → 材料缺口在 2026 年是靠降级、涨价、库存消化的；所以"满足率 &lt; 1"在材料环节表示<b>规格和价格</b>受限，不直接等于少出货 {E}。ABF 不能降级，所以出货的约束仍是 ABF。</li>
<li><b>不在 2027 主路径的</b>：Q 布 2026 年约 83–100%（群益）{S('qy')}，但正交背板推迟到 2028 {S('kyber')}；PCB 板厂产能没有可信统计，只定性 {S('capex')}。</li>
</ol></div>
<div class="seg" id="pcb-fYr" style="margin-top:12px"><button data-m="2026">2026</button><button class="on" data-m="2027">2027</button></div>
<div class="grid g2" style="margin-top:8px"><div class="card"><b>能支撑多少 AI 加速器（百万颗）</b><div id="pcb-cToc" class="chart" style="height:340px"></div><div class="note">柱 = 各环节能支撑的颗数（跟随第 5 步滑块）；虚线 = KGI 出货。红色 = PCB 链内最紧；灰色 = 跨链（读 CoWoS 页）。</div></div>
<div class="card"><div class="tbl"><table id="pcb-tocT" class="stack"><thead><tr><th>环节</th><th>满足率</th><th>能支撑（百万颗）</th><th>判断</th></tr></thead><tbody></tbody></table></div><div class="note" id="pcb-tocTxt"></div></div></div>"""

STAGE_TBL = '<div class="tbl"><table id="pcb-stT" class="stack"><thead><tr><th>环节</th><th>2025</th><th>2026</th><th>2027 基准</th><th>依据</th><th>来源</th></tr></thead><tbody></tbody></table></div>'

SPEC = dict(
 logic=LOGIC,
 file='pcb.html', title='PCB 印制电路板', pill='PCB v0.1', other=('cowos.html', 'CoWoS ⇄'), scripts=['pcb.js'],
 ledgers=[('a1', 'gl', '全球账本', f'2027 年 PCB 链最紧的是 HVLP4 铜箔（约 {CU}），和 ABF 载板打平；材料能降级，缺口变成涨价，利润往上游走'),
          ('cn', 'cnl', '中国账本', f'国产卡被 HBM 卡在约 {CN["WHK27"]*100:.0f} 万张，PCB 链不是约束；国内短板在 Low-CTE 纱、HVLP5 和进口设备')],
 kicker='PCB 小链 · v0.1 · 更新 <span id="pcb-upd"></span> · 统一单位接 <a href="cowos.html">CoWoS</a> / <a href="hbm.html">HBM</a> 页',
 card=f'全球账本：2027 年 PCB 链最紧的是 HVLP4 铜箔（约 {CU}，与 ABF 载板打平），卡规格不卡出货，利润往上游材料走。中国账本：国产卡被 HBM 卡住，PCB 链不是约束{E}',
 scqa=[
  f'AI 服务器把 PCB 变成了高端件：VR200 每柜 PCB 约 11.67 万美元，是 GB300 的约 3.3 倍 {S("ms")}；全球 PCB 2026 年预计 +32.1%，18 层以上 +86.7% {S("prq2")}。',
  f'高盛预计 2027 年 AI PCB 面积翻倍、M9 占 AI 覆铜板 41% {S("gs")}，同时说高端铜箔缺 45–55% {S("gscu2")}、广发说二代布缺 40% 以上 {S("gf")}；可 Kyber 正交背板已推迟到 2028 {S("kyber")}，A 股板厂又在扩产 800 亿元以上 {S("capex")}。',
  '2027 年 PCB 会不会卡住 AI 加速器？最紧的是哪一环、紧多少？钱流向谁？主流的 M9 / 玻纤布叙事哪里高估了？'],
 gov=GOV,
 mece='三条论点分别回答"量（卡在哪）""利润（钱去哪）""预期差与时点"，互不重叠。统一单位和 CoWoS / HBM 页相同（KGI 加速器颗数），ABF 载板只读 CoWoS 页结果，不重复。中国的账另算（见<a href="#cn">中国账本</a>）。',
 args=[
  dict(tag='量', claim=f'2027 年 AI PCB 面积翻倍；PCB 链最紧的是 HVLP4 铜箔，按目标规格只够约 {CU}，和 ABF 载板（{ABF}）打平。但材料能降一级用，所以卡的是规格和价格，出货的约束仍是 ABF',
   key=f'2027 PCB 链最紧 <b data-from="pcb-min">—</b> · 最紧环节 <b data-from="pcb-bind">—</b> · ABF <b>{ABF}</b> {E}',
   sub='每一环的满足率 = 来源自己的供给 ÷ 需求（目标规格），乘以 KGI 加速器颗数 = 能支撑多少颗；取最小值就是约束（TOC）。',
   hero=dict(src='pcb-cToc', step='neck', t='能支撑多少 AI 加速器（百万颗，2027）：铜箔 ≈ ABF', h=340, note='跟随底稿第 5 步的滑块实时重算；灰柱读自 CoWoS 页。'),
   ev=[
    dict(t=f'铜箔：按目标规格只够约 {CU}', b=f'高盛 8 月把 HVLP3+ 缺口上修到 45–55% {S("gscu2")}；金居 HVLP3+ 良率 2Q26 才 50% 以上 {S("gscu2")}；三井 FY27 只有 1,000 吨/月 {S("mitsui")}。加上大陆 HVLP4 增量 {E}，满足率约 {CU}。', steps=['balance', 'neck']),
    dict(t='需求：面积翻倍、每颗加速器的 PCB 价值翻倍', b=f'AI PCB 面积 130 → 260 万 m²、单价 10,258 → 14,405 美元/m² {S("gs")}；每颗加速器约 {PER["2026"]:,} → {PER["2027"]:,} 美元 {E}，与摩根士丹利 VR200 约 1,621 美元/GPU 同一量级 {S("ms")}。', steps=['demand']),
    dict(t='供给：板厂和压机扩得快，材料扩得慢', b=f'台光电年均产能 +{(O["CCLg"]-1)*100:.0f}%、年底 +51% {S("emcir")}；三井 HVLP FY26→27 只 +19% {S("mitsui")}；钻针有效供给 +39% vs 需求 +50% {S("uad")}。', steps=['supply']),
    dict(t='降级是现实选项：缺口变成价格，不变成少出货', b=f'日东纺：客户把 NE 布当作 NER 的替代 {S("nqa")}；Rubin 计算板用 M8 + 一代布 {S("doosan")}；2026 年铜箔按同一算法只够约 {p(R26["cu"])}，没有出货因铜箔受限的报道 {E}。', steps=['balance']),
    dict(t='TOC：和 HBM、CoWoS、ABF 放在同一张图', b=f'2027 年 ABF {ABF}、PCB 链最紧 {CU}、二代布 {GF}、覆铜板 {CCL}、钻针 {DR}、HBM {p(X["hbm"]["2027"])}（CoWoS 页口径）{E}。', steps=['neck']),
    dict(t=f'要害变量："铜箔比 ABF 松"只领先约 {GAP:.0f} 个百分点', b='大陆 HVLP4 认证归零、高盛缺口取 55%、需求 +10%，任何一项都会让铜箔比 ABF 更紧；允许降级一半，PCB 链就远松于 ABF（见龙卷风图）。', steps=['key']),
    dict(t='跨链对账：PCB 不改变 HBM / CoWoS 页的结论', b='三页同一个分母；PCB 链和 ABF 同属"基板与材料"，都比 HBM、CoWoS 紧，但 PCB 材料可降级。', steps=['map']),
   ]),
  dict(tag='利润', claim=f'增量利润往扩得慢的上游走：一年里玻纤布（富乔）毛利率 +15.5pp、钻针（尖点）+12.4pp、铜箔（金居）+8.5pp，板厂中位只 +{FBM:.1f}pp（胜宏 −3.0pp）；2027 年最耐久的是铜箔',
   key=f'上游毛利率中位 <b>+{UPM:.1f}pp</b> · 板厂 <b>+{FBM:.1f}pp</b>（一年）{S("fm")}',
   sub='台湾公司用 MOPS 季报（2Q26 vs 2Q25），A 股用半年报（分产品毛利率）；口径不完全可比，但方向一致。',
   hero=dict(src='pcb-cDgm', step='profit', t='毛利率一年变化（百分点）：上游材料 > 覆铜板 > 板厂', h=360, note=f'富乔 24.5% → 40.0%，尖点 29.4% → 41.8%，金居 18.9% → 27.4%，胜宏 36.2% → 33.2% {S("fm", "shhk")}。'),
   ev=[
    dict(t='毛利率迁移：上游涨得最快', b=f'上游（铜箔、玻纤布、钻针、覆铜板）中位 +{UPM:.1f}pp；板厂（金像电、沪电、深南、胜宏）中位 +{FBM:.1f}pp {S("fm", "hd", "sn", "shhk")}。', steps=['profit']),
    dict(t='价格：涨价在材料端', b=f'CCL 最缺料号涨 30–40% {S("udn2")}；金居价格 3Q 季增 10–15% {S("gscu2")}；钻针高端 +35% 以上、钨钢棒翻倍 {S("cld")}。', steps=['balance']),
    dict(t='扩产最多的是板厂', b=f'A 股 20 家板厂年内扩产超 800 亿元，2–3 年后集中释放 {S("capex")}；胜宏毛利率下滑的原因正是人工和新产能爬坡 {S("shhk")}。', steps=['supply', 'play']),
    dict(t='谁最耐久：铜箔 > 钻针 > 覆铜板 > 二代布 > 板厂', b=f'铜箔 2028 年缺口仍 38–55% {S("gscu", "gscu2")}、认证 2–3 年 {S("uacu")}；二代布 2027Q4 起大陆新增 4–5 亿米 {S("jy")} {E}。', steps=['neck']),
   ]),
  dict(tag='预期差', claim=f'主流按 M9 2027 年占 AI 覆铜板 41% 定价；正交背板推迟到 2028、CPX 移除后，我们估只有 {M9L}–{M9H}%，增量更多来自 ASIC 的层数。CCL 营收同比领先板厂约 {BT["med"]:.0f} 个月，现在 +{BT["now"]["ccl"]:.0f}% 仍在加速',
   key=f'M9 2027：高盛 <b>41%</b> vs 我们 <b>{M9L}–{M9H}%</b> {E}',
   sub='M9 的倒推：台光电 2026Q3 营收年化 × 2027 年均产能 ÷ 2026Q3 产能 → 2027 年营收；× M9 营收占比 10–25%（"双位数"）÷ 台光电 M9 份额 50–70% → M9 市场；÷ 高盛 2027 年 AI CCL 221 亿美元。',
   hero=dict(src='pcb-cM9', step='demand', t='高端规格渗透率（占 AI PCB / CCL）：高盛 vs 我们', h=330, note=f'高盛数据 {S("gs", "gsx")}；我们的 M9 区间 {E}。'),
   ev=[
    dict(t=f'M9 倒推：约 {M9L}–{M9H}%', b=f'台光电 7–9 月营收 608.85 亿新台币 {S("fm")} → 年化约 {O["EMC"]["run"]:.1f} 十亿美元 × {O["EMC"]["cap"]:.2f}（2027 年均产能 ÷ 2026Q3）{S("emcir", "udn1")} = 2027 年约 {O["EMC"]["y27"]:.1f} 十亿美元；M9 占"双位数" {S("udn1")} → M9 市场约 {M9["lo"]:.1f}–{M9["hi"]:.1f} 十亿美元，高盛 {M9["gs"]:.1f} {S("gs")} {E}。', steps=['demand']),
    dict(t='变局：背板推迟、CPX 移除', b=f'GTC 2026 移除 Rubin CPX {S("cpx")}；Kyber NVL144 因中板/背板难做推迟到 2028 {S("kyber", "cnbc")}；杰富瑞下调 2027 年 AI PCB/CCL TAM 5%/8% {S("jef")}，高盛 8 月反而上调 38% {S("gs")}。', steps=['hist']),
    dict(t='2027 年增量一半来自 ASIC', b=f'高盛：2027 年 GPU 服务器 PCB 188.0 亿美元、ASIC 187.3 亿 {S("gs")}；谷歌 V7P 44 层主板 {S("tpu")}。ASIC 的增量在层数，不一定在 M9。', steps=['demand']),
    dict(t=f'时点：CCL 营收同比领先板厂中位 {BT["med"]:.0f} 个月', b=f'{BT["n"]} 次拐点中 {BT["pos"]} 次领先（{BT["lo"]}–{BT["hi"]} 个月）{S("fm")}；{BT["m"]} CCL 三家 3 个月同比 +{BT["now"]["ccl"]:.0f}% 仍在加速，金像电 +{BT["now"]["2368"]:.0f}%（7 月 +81%）可能在见顶。', steps=['lead']),
    dict(t='玩家：英伟达宁可推迟也不降规格', b=f'Kyber 推迟而不是降规格量产 {S("kyber")}；台光电 M9 下半年小量出货、2027 年"双位数" {S("udn1")}。', steps=['play']),
   ]),
 ],
 cn=dict(
  nav='中国账本', kicker='中国视角：国产 AI 卡要用的 PCB 链 vs 国内产能（与全球账本口径不重复）',
  scqa=[f'中国大陆 2025 年 PCB 产值约 410.7 亿美元，约占全球一半 {S("cninfo")}；胜宏、沪电、深南是英伟达、谷歌的主力板厂 {S("shshare", "tpu")}，鼎泰 + 金洲占全球钻针一半 {S("uad")}。',
        f'但国产 AI 卡被 HBM 卡在约 {CN["WHK27"]*100:.0f} 万张（2027）{S("hbm")}；同时上游 Low-CTE 纱（日东纺 85%）{S("hh")}、HVLP4/5 铜箔 {S("gscu")}、进口开槽机 {S("uad")} 仍靠海外。',
        '国产卡会不会被 PCB 卡住？国内 PCB 链自己的短板在哪？谁在国产替代里真正稀缺？'],
  gov=f'国产卡的墙是 HBM 不是 PCB：2027 年所需 PCB 只占三家龙头产值约 {CB["fab"]["share"]*100:.0f}% {E}；国内短板在 Low-CTE 纱、HVLP5 和进口设备，最稀缺的国产替代是高端铜箔',
  mece='三条中国论点分别回答"够不够""卡在哪""谁稀缺、何时变"。国产卡数读自 HBM / CoWoS 页中国账本；每卡用量没有公开数据，用全球口径或 VR200 上限（估）。',
  args=[
   dict(tag='平衡', claim=f'国产卡不被 PCB 卡：2027 年 HBM 能配约 {CN["WHK27"]*100:.0f} 万张，所需 PCB 约 {CB["fab"]["need"]:.1f} 十亿美元（按 VR200 上限），只占三家龙头年化产值约 {CB["fab"]["share"]*100:.0f}%、中国 PCB 产值约 {CB["fab"]["share_cn"]*100:.0f}%',
    key=f'所需 ÷ 龙头产值 <b data-from="pcb-cnFab">—</b> {E}',
    sub='需求 = 国产卡数 × 每卡用量；供给 = 国内已披露的产能或营收。滑块可调国产卡数和每卡 PCB 价值。',
    hero=dict(src='pcb-cnBal', step='balance', t='国产卡需要占国内产能的比例（2027）', h=300, note='低于 100% = 不卡；HBM 若放开到不缺货需求，看第 5 步中国块滑块。'),
    ev=[
     dict(t='需求：卡数 × 每卡用量', b=f'HBM 能配的卡 + 950/960PR 约 {CN["WHK27"]:.2f} 百万张 {S("hbm", "cowos")}；每卡 PCB 价值用 VR200 每 GPU 1,621 美元作上限 {S("ms")} {E}。', steps=['demand']),
     dict(t='供给：三家龙头年化约 663 亿元', b=f'胜宏 116.29 亿 + 沪电 PCB 129.94 亿 + 深南 PCB 85.52 亿元（1H26）{S("sh1h", "hd", "sn")}，×2 约 {CN["fab_usd"]:.1f} 十亿美元。', steps=['supply']),
     dict(t='若 HBM 放开：铜箔和板厂先紧', b=f'不缺货需求约 {CN["U27"]:.2f} 百万张时，所需 PCB 约等于三家龙头产值的 {CBU["fab"]["share"]*100:.0f}%、德福 HVLP 出货的 {CBU["cu"]["share"]:.1f} 倍 {E}。', steps=['balance']),
    ]),
   dict(tag='约束', claim='国内 PCB 链自己的短板在上游：Low-CTE（T-glass）纱日东纺占 85%、HVLP5 靠三井、进口开槽机交期 1–2 年、超细钨钢棒涨价翻倍；板厂、钻针、Q 布已在前列',
    key=f'能支撑的卡：HBM <b>{CN["WHK27"]:.2f}</b> · 2.5D <b>{CN["WK27"]:.2f}</b> · 板厂 <b>{CB["fab"]["up"]:.1f}</b> 百万张 {E}',
    sub='按约束理论把每一环换成"能支撑多少张国产卡"：HBM、2.5D 读自其他两页；PCB 各环是"国内产能全给国产卡"的上限。',
    hero=dict(src='pcb-cnToc', step='neck', t='能支撑多少张国产卡（百万张，2027）', h=300, note='PCB 各环为上限（估）；HBM 一栏是约束。'),
    ev=[
     dict(t='TOC：HBM 最低', b=f'HBM 约 {CN["WHK27"]:.2f}、2.5D 约 {CN["WK27"]:.2f}、板厂上限约 {CB["fab"]["up"]:.1f}、HVLP 铜箔上限约 {CB["cu"]["up"]:.1f}、二代布（只算宏和）{CB["ldk"]["up"][0]:.1f}–{CB["ldk"]["up"][1]:.1f} 百万张 {E}。', steps=['neck']),
     dict(t='短板：材料与设备', b=f'低 CTE 布日东纺 85%、Unitika 14% {S("hh")}；进口开槽机交期 1–2 年 {S("uad")}；钨钢棒价格翻倍 {S("cld")}。', steps=['neck', 'supply']),
     dict(t='领先：板厂、钻针、Q 布', b=f'鼎泰 29.2% + 金洲 21.1% {S("uad")}；菲利华 Q 布通过生益、台光电、松下认证 {S("cq")}。', steps=['supply', 'play']),
    ]),
   dict(tag='稀缺', claim='最稀缺的国产替代是 HVLP4/5 铜箔（德福、铜冠刚量产）；二代布和板厂是扩产最集中的地方，2027Q4–2028 可能先过剩',
    key='德福 HVLP4 <b>约 70 吨/月</b>（8 月）· 大陆二代布 2027Q4 起 <b>+4–5 亿米</b>',
    sub='A 股按证据强度分级：强 = 公司公告 / 交易所文件；中 = 媒体或机构；弱 = 纪要或自媒体。',
    hero=dict(src='pcb-cnCu', step='neck', t='高端铜箔：国产卡需要多少 vs 国内供应（吨/月）', h=300, note='HBM 一旦放开（不缺货需求），国产卡要的 HVLP 超过德福目前全部 HVLP 出货（估）。'),
    ev=[
     dict(t='铜箔：认证是门槛', b=f'德福 HVLP4 良率 60%+、5 万吨基地 2027Q2 起投产 {S("defu")}；高盛只认金居为合格二供 {S("gscu")}；二供认证要 2–3 年 {S("uacu")}。', steps=['play', 'map']),
     dict(t='二代布：扩产最集中', b=f'大陆 2027Q4–2028Q2 新增 4–5 亿米 vs 2027 年总需求 2–3 亿米 {S("jy")}；宏和 2027 年 2,281 万米 {S("hh")}。', steps=['neck']),
     dict(t='A 股：按环节，证据强度分级', b=f'强：德福、生益、宏和、鼎泰、大族数控、胜宏、沪电、深南；中：铜冠、菲利华、东材、圣泉、中材、中钨高新 {S("defu", "sy", "hh", "dt", "dz")}。', steps=['map']),
    ]),
  ]),
 wrong='''<p class="sub">每条判断：现在已经看到的反方证据、什么情况算我错、看哪个公开指标、阈值多少。J1↔论点①、J3↔论点②、J2/J4↔论点③，J5 是需求的上一层。触发阈值就改判断，不辩护。</p>
<div class="tbl"><table id="pcb-falT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：CJ1–CJ3</h3><p class="sub">CJ1↔中国论点❶、CJ2↔❷、CJ3↔❸。</p>
<div class="tbl"><table id="pcb-cnFalT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 pred='''<p class="sub" id="pcb-predSum"></p><p class="sub">2026-10-20 写入。到期后按公开数据打分，不改原文，只追加结果。C 系列是本链判断，M 系列是约束迁移，N 系列是中国账本。和 CoWoS 页 T 系列（约束迁移）对照：CoWoS 页说 2027 年最紧是载板，本页补上"PCB 材料与载板打平但可降级"。</p>
<div class="tbl"><table id="pcb-predT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：N 系列</h3><p class="note" id="pcb-cnPredS"></p>
<div class="tbl"><table id="pcb-cnPredT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 base_title='PCB 产业链底稿',
 base_sub='上面的结论都从这里来。按 SOP 顺序：先找要害变量和争议，再定边界、算供需、看利润和约束，最后看玩家、历史、领先指标和公司。右侧圆圈 = 这一步支撑哪条论点。',
 steps=[
  dict(id='key', h='哪个假设能把结论翻过来', body='''<p class="note" id="pcb-torNote"></p>
<div class="grid g2"><div class="card"><b>2027 年 PCB 链最紧环节的满足率</b><div id="pcb-cTorA" class="chart" style="height:320px"></div><div class="note">每一行：只把这个变量调到低端（蓝）/ 高端（红），其他不动。虚线 = ABF 载板满足率（CoWoS 页）：越过它，PCB 链就比 ABF 更紧。</div></div>
<div class="card"><b>"PCB 链不比 ABF 更紧"这个结论有多稳</b><div id="pcb-cTorB" class="chart" style="height:320px"></div><div class="note">指标 = PCB 链最紧满足率 − ABF 满足率（百分点），小于 0 表示 PCB 链变成头号约束。基准只有几个百分点：结论是<b>两者打平</b>，PCB 链不更紧的前提是"能降级"。<span class="tag t-est">估</span></div></div></div>'''),
  dict(id='debate', h='三个可证伪的核心争议', ctx='对应结论层「可能错在哪」↑', body='<div class="grid g3" id="pcb-deb"></div>'),
  dict(id='proc', h='AI 服务器里有哪些板，PCB 是怎么做出来的', ctx='背景：定义单位与边界', sub='计量单位：PCB 用面积（m²）和金额，覆铜板用张，铜箔用吨/月，玻纤布用米，钻针用支；统一换算成"能支撑多少颗 AI 加速器"（第 7 步）。ABF 封装载板不在本页重复，见 CoWoS 页。',
   body='''<h3>板型对比</h3><div class="tbl"><table id="pcb-varT"><thead><tr><th>板型</th><th>用途</th><th>层数 / 单价 / 用量</th><th>材料</th><th>现状</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<h3>材料与工序 → 供应商</h3><div class="tbl"><table id="pcb-procT"><thead><tr><th>环节</th><th>要点</th><th>供应商</th><th>来源</th></tr></thead><tbody></tbody></table></div>'''),
  dict(id='demand',
   cn=dict(h='国产卡要多少 PCB 链产能', body=f'''<div class="tbl"><table id="pcb-cnDemT" class="stack"><thead><tr><th>项目</th><th>数值（2027）</th><th>依据</th></tr></thead><tbody></tbody></table></div>
<div class="note">国产卡的 PCB 规格和用量没有公开数据；VR200 是目前最贵的 AI 机柜之一，用它作上限，结论偏保守 {E}。</div>'''),
   h='需求：面积 × 单价 × 规格，上一层是云厂商资本开支', body=f'''<div class="grid g2"><div class="card"><b>AI 服务器 PCB / CCL 市场（十亿美元）与每颗加速器 PCB 价值</b><div id="pcb-cDem" class="chart" style="height:340px"></div><div class="note">市场 = 高盛面积 × 单价、张数 × 单价 {S("gs")}；每颗价值 = 市场 ÷ KGI 颗数 {E}。2028 年不在 KGI 预测里，只画市场。</div></div>
<div class="card"><b>高端规格渗透：高盛 vs 我们</b><div id="pcb-cM9" class="chart" style="height:340px"></div><div class="note">30 层以上、6+N+6 HDI 占比来自高盛细项（只看到搜索摘要）{S("gsx")}；M9 占比 {S("gs")}；紫色区间 = 我们的 M9 倒推 {E}。</div></div></div>
<div class="tbl" style="margin-top:12px"><table id="pcb-gsT" class="stack"><thead><tr><th>年</th><th>面积（万 m²）</th><th>单价（美元/m²）</th><th>AI PCB（十亿美元）</th><th>CCL（百万张）</th><th>美元/张</th><th>AI CCL（十亿美元）</th><th>M9 占比</th></tr></thead><tbody></tbody></table></div>
<div class="card" style="margin-top:12px"><b>M9 倒推（估）</b><div class="note" style="font-size:13px">① 台光电 2026 年 7–9 月营收 192.07 + 201.46 + 215.32 = 608.85 亿新台币 {S("fm")}，年化 ÷ 32.63 ≈ {O["EMC"]["run"]:.2f} 十亿美元。② 2027 年均月产能（735 / 735 / 855 / 930 万张的平均）÷ 2026Q3 的 585 万张 = ×{O["EMC"]["cap"]:.3f} {S("emcir", "udn1")} → 2027 年约 {O["EMC"]["y27"]:.1f} 十亿美元（不计涨价）。③ M9 占营收 10–25%（"双位数" {S("udn1")}），台光电占 M9 市场 50–70%（中板约 70% {S("doosan")}，高速无卤基板 38.6% {S("emcir")}）→ M9 市场 {M9["lo"]:.2f}–{M9["hi"]:.2f} 十亿美元。④ ÷ 高盛 2027 年 AI CCL {M9["ccl27"]:.1f} 十亿美元 = <b>{M9L}–{M9H}%</b>；高盛 41%（{M9["gs"]:.2f} 十亿美元）。即使台光电份额只有 35%、M9 占营收 25%，也只有约 34%。</div></div>
<h3>需求的上一层：云厂商资本开支</h3>
<div class="grid g2"><div class="card"><div id="pcb-cDrv" class="chart" style="height:340px"></div><div class="note">读 CoWoS 页的同一组数据（来源链接到 CoWoS 页）。</div></div><div class="card"><table id="pcb-drvT"><tbody></tbody></table></div></div>'''),
  dict(id='supply',
   cn=dict(h='国内产能：谁有多少', body='<div class="tbl"><table id="pcb-cnSupT" class="stack"><thead><tr><th>环节</th><th>国内产能 / 产值</th><th>依据</th></tr></thead><tbody></tbody></table></div>'),
   h='供给：哪一环扩得比需求慢', body=f'''<div class="card"><b>2027 ÷ 2026：需求增速 vs 供给增速（倍）</b><div id="pcb-cSup" class="chart" style="height:320px"></div><div class="note">需求：高盛面积、张数 {S("gs")}，铜箔插值 {S("gscu")}，二代布纪要 {S("jy")}，钻针 {S("uad")}。供给：台光电年均产能 {S("emcir")}，三井 VSP FY26→27 {S("mitsui")}，钻针有效供给 {S("uad")}。板厂、二代布供给没有可信的同口径数据，不画。</div></div>
<h3>各环节供需依据</h3>{STAGE_TBL}'''),
  dict(id='balance',
   cn=dict(h='中国平衡：拖动国产卡数和每卡价值', body=f'''<div class="grid g2"><div class="card"><div class="ctl">
<label>2027 年国产卡数（百万张）<output id="pcb-cno1"></output></label><input type="range" id="pcb-cnu" min="0.5" max="7" step="0.1" value="{CN["WHK27"]:.1f}">
<label>每卡 PCB 价值（美元）<output id="pcb-cno2"></output></label><input type="range" id="pcb-cnusd" min="500" max="2500" step="50" value="1621">
</div><button class="btn" onclick="pcbCnReset()">恢复基准</button>
<div class="grid g2" style="margin-top:14px;gap:8px"><div><div class="note">所需 ÷ 三家龙头产值</div><div class="big" id="pcb-cnFab"></div></div><div><div class="note">所需 ÷ 德福 HVLP 出货</div><div class="big" id="pcb-cnCuR" style="color:var(--warn)"></div></div></div><div class="note" id="pcb-cnTxt"></div></div>
<div class="card"><div id="pcb-cnBal" class="chart" style="height:300px"></div><div class="note">基准 = HBM 能配的卡 {CN["WHK27"]:.2f} 百万张；拖到 {CN["U27"]:.2f}（不缺货需求）看 HBM 放开后的情形 {E}。</div></div></div>'''),
   h='平衡与价格：自己拖动假设', sub='满足率 = 供给 ÷ 需求（目标规格）。浏览器里实时重算，结论层的图跟着变。降级比例 = 缺口里能用低一级材料吸收的部分。', body=f'''<div class="grid g4" id="pcb-stats"></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><div class="ctl">
<label>2027 AI 加速器需求（相对 KGI）<output id="pcb-o-dem"></output></label><input type="range" id="pcb-dem" min="80" max="120" step="5" value="100">
<label>2027 高端铜箔缺口（高盛口径）<output id="pcb-o-g27"></output></label><input type="range" id="pcb-g27" min="25" max="60" step="5" value="50">
<label>2027 大陆 HVLP4 通过认证的增量（吨/月）<output id="pcb-o-cn"></output></label><input type="range" id="pcb-cn" min="0" max="400" step="25" value="150">
<label>2027 二代布满足率<output id="pcb-o-gf"></output></label><input type="range" id="pcb-gf" min="60" max="110" step="5" value="80">
<label>2027 覆铜板高阶占比提升（倍）<output id="pcb-o-mix"></output></label><input type="range" id="pcb-mix" min="100" max="135" step="5" value="115">
<label>2027 钻针有效供给（相对优分析）<output id="pcb-o-dr"></output></label><input type="range" id="pcb-dr" min="85" max="115" step="5" value="100">
<label>2027 ABF 载板供给增速（CoWoS 页基准 27.5%）<output id="pcb-o-abf"></output></label><input type="range" id="pcb-abf" min="15" max="40" step="2.5" value="27.5">
<label>降级比例（缺口里用低一级材料吸收的部分）<output id="pcb-o-s"></output></label><input type="range" id="pcb-s" min="0" max="100" step="10" value="0">
</div><button class="btn" onclick="pcbReset()">恢复基准</button>
<div class="grid g2" style="margin-top:16px;gap:8px"><div><div class="note">2027 PCB 链最紧</div><div class="big" id="pcb-min"></div></div><div><div class="note">最紧环节</div><div class="big" id="pcb-bind" style="color:var(--warn)"></div></div></div><div class="note" id="pcb-balTxt"></div>
</div><div class="card"><div id="pcb-cBal" class="chart" style="height:380px"></div><div class="note">柱 = 各环节满足率；灰色 = 跨链（ABF、HBM，读 CoWoS 页）。100% 线以下 = 缺。</div></div></div>
<h3>价格：涨价在哪</h3><div class="tbl"><table id="pcb-prT"><thead><tr><th>环节</th><th>报价 / 涨幅</th><th>出处</th><th>来源</th></tr></thead><tbody></tbody></table></div>'''),
  dict(id='profit', h='利润池：钱在板厂和覆铜板，利润增速最快的是上游材料', body=f'''<div class="grid g2"><div class="card"><b>毛利率一年变化（百分点）</b><div id="pcb-cDgm" class="chart" style="height:360px"></div></div>
<div class="card"><b>毛利率迁移（季度，MOPS 财报）</b><div id="pcb-cMar" class="chart" style="height:360px"></div><div class="note">富乔（玻纤布）、尖点（钻针）2025 年起上得最快；金像电（板厂）一直较高但涨得慢 {S("fm")}。</div></div></div>
<div class="tbl" style="margin-top:12px"><table id="pcb-dgmT" class="stack"><thead><tr><th>公司</th><th>环节</th><th>现在</th><th>一年前</th><th>口径</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<h3>利润池（2027，按环节）</h3><div class="tbl"><table class="stack"><thead><tr><th>环节</th><th>市场规模</th><th>毛利率参照</th><th>判断</th></tr></thead><tbody>
<tr><td><b>AI 服务器 PCB（板厂）</b></td><td>约 375 亿美元 {S("gs")}</td><td>沪电 PCB 40.5%、深南 36.9%、金像电 34.7%、胜宏 33.2% {S("hd", "sn", "fm", "shhk")}</td><td>盘子最大，扩产最多，毛利率涨得最慢</td></tr>
<tr><td><b>AI 覆铜板 CCL</b></td><td>约 221 亿美元 {S("gs")}</td><td>台光电 33.9%、台燿 29.7%、生益 CCL 29.2% {S("fm", "sy")}</td><td>有定价权（龙头 >50% 份额 {S("emcir")}）</td></tr>
<tr><td><b>HVLP3+ 铜箔</b></td><td>2025 年 2.16 亿 → 2028 年 24 亿美元（高盛）{S("gscu")}</td><td>高端 40–60% vs 普通 0–10% {S("gscu")}；三井铜箔 ROIC 52% {S("mitsuiq1")}</td><td>盘子小、利润率最高、最耐久</td></tr>
<tr><td><b>低介电玻纤布</b></td><td>2025 年 3.92 亿美元，2026–27 年每年 >40% {S("cldk")}</td><td>富乔 40.0%（一年前 24.5%）{S("fm")}；日东纺电子材料营业利益 +44% {S("tfn")}</td><td>涨得最猛，2027Q4 后过剩风险</td></tr>
<tr><td><b>钻针 / 钻孔设备</b></td><td>钻针 2027 年需求 76.7 亿支 {S("uad")}</td><td>尖点 41.8% {S("fm")}；大族数控营收 +109% {S("dz")}</td><td>耗材属性，跟层数和材料硬度走</td></tr>
</tbody></table></div>'''),
  dict(id='neck',
   cn=dict(h='中国的约束：换成"能支撑多少张国产卡"', body=f'''<div class="tbl"><table id="pcb-cnTocT" class="stack"><thead><tr><th>环节</th><th>能支撑（百万张）</th><th>依据</th><th>判断</th></tr></thead><tbody></tbody></table></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><div id="pcb-cnToc" class="chart" style="height:300px"></div><div class="note">HBM、2.5D 读自 HBM / CoWoS 页中国账本；PCB 各环为"国内产能全给国产卡"的上限（估）。</div></div>
<div class="card"><b>国产化时间表</b><div class="tl" style="margin-top:10px" id="pcb-cntl"></div></div></div>
<div class="card" style="margin-top:12px"><b>高端铜箔：国产卡需要多少 vs 国内供应（吨/月）</b><div id="pcb-cnCu" class="chart" style="height:300px"></div><div class="note">需求 = 国产卡数 × 每卡约 {O["CUKG"]["2027"]} kg ÷ 12（全球口径，估）{E}；供应：德福 8 月 HVLP 约 500 吨、其中 HVLP4 约 70 吨 {S("defu")}；金居 HVLP4 2H26 约 150 吨/月作对照 {S("uacu")}。</div></div>'''),
   h='约束推导：把每一环换成同一单位，最小的那个才是约束', sub='按 Goldratt 约束理论（TOC）：铜箔吨、玻纤布米、覆铜板张、钻针支、ABF 载板 → 统一成"能支撑多少颗 AI 加速器 / 年"（和 HBM、CoWoS 页同一个分母），取最小值。数据质量不支持按季，只按年。',
   body=TOCBLOCK + '\n<h3>汇总排序（推导结果 + 定性证据）</h3><p class="sub">条形长度 = 缓解所需月数（示意）。</p><div id="pcb-neck" class="grid"></div>'),
  dict(id='play',
   cn=dict(h='中国账本的玩家：谁的决定会改变这本账', body='<div class="grid g2" id="pcb-cnPl"></div>'),
   h='谁在做什么决定，为什么，什么信号说明他们变了', sub='英伟达定规格、台光电定 CCL 价格、三井和日东纺决定上游扩多快、板厂决定扩产节奏、ASIC 阵营决定 2027 年的增量。', body='<div class="grid g2" id="pcb-play"></div>'),
  dict(id='hist', h='技术代际与瓶颈迁移', body='''<p class="sub" id="pcb-rule"></p>
<div class="grid g2"><div class="card"><b>市场与平台</b><div class="tl" style="margin-top:12px" id="pcb-tl1"></div></div>
<div class="card"><b>瓶颈迁移</b><div class="tl" style="margin-top:12px" id="pcb-tl2"></div></div></div>'''),
  dict(id='lead', h='先看哪个数据（已回测）', sub=f'回测结论：CCL 三家营收同比和 AI 板厂（金像电）同比在 k=+{BT["k"][0]} 时相关最高（r={BT["k"][1][0]:.2f}）；同比拐点 {BT["n"]} 次中 {BT["pos"]} 次领先，中位 {BT["med"]:.0f} 个月。上游三家（铜箔、玻纤布、钻针）和 CCL 同步，不领先。', body=f'''<div class="card"><b>回测：CCL 三家、上游三家、金像电、台积电营收（3 个月滚动同比）</b><div id="pcb-cBt" class="chart" style="height:380px"></div><div class="note">MOPS 月营收（经 FinMind API 下载）2014-01 至 {BT["m"]} {S("fm")}；同比截断在 −80%～+250%。CCL 三家 = 台光电 2383 + 台燿 6274 + 联茂 6213；上游三家 = 金居 8358 + 富乔 1815 + 尖点 8021。</div></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><b>交叉相关：A 领先 k 个月时与 B 的相关系数</b><div id="pcb-cXc" class="chart" style="height:280px"></div><div class="note">样本约 141 个月。"台积电→CCL"在 k=−7 最高：CCL 反而领先台积电约 7 个月。</div></div>
<div class="card"><b>拐点对照：CCL 三家同比 → 金像电同比</b><div class="tbl"><table id="pcb-tpT"><thead><tr><th>CCL 同比拐点</th><th>金像电同比拐点</th><th>领先（月）</th></tr></thead><tbody></tbody></table></div><div class="note" id="pcb-btNow"></div></div></div>
<div class="grid g3" id="pcb-lead" style="margin-top:14px"></div>'''),
  dict(id='ledger', h='预测台账放在结论层', ctx='台账在结论层「预测台账」↑', body='<p>C 系列（本链判断）、M 系列（约束迁移）和 N 系列（中国账本）都在 <a href="#pred">结论层 · 预测台账</a>；每条判断的反方证据和证伪阈值在 <a href="#wrong">可能错在哪</a>。规则：到期按公开数据打分，不改原文，只追加结果；作废要写原因并保留原文。</p>'),
  dict(id='map',
   cn=dict(h='A 股：按环节，标明证据强度', body=f'''<p class="sub">"强"= 公司公告或交易所文件；"中"= 媒体或机构；"弱"= 调研纪要或自媒体。AI 专项营收占比基本都没有披露。只列事实，不构成投资建议。</p>
<div class="tbl"><table id="pcb-cnCoT" class="stack"><thead><tr><th>环节</th><th>公司</th><th>代码</th><th>与 AI PCB 的关系</th><th>证据强度</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">和其他两页对账：本页读取 HBM 页中国账本"能配的卡"和 CoWoS 页"国内 2.5D 能封的卡"（2027 年约 {CN["WHK27"]:.2f} / {CN["WK27"]:.2f} 百万张）{S("hbm", "cowos")}。</div>'''),
   h='环节 → 公司 → 订单；和 HBM、CoWoS 对账', sub='点节点看详情；实线边都附来源编号（绿 = 供货，橙 = 委托 / 订单）。虚线只表示公司在这个环节有业务。', body=f'''<div class="seg" id="pcb-fMk"><button class="on" data-m="all">全部</button><button data-m="A">A股</button><button data-m="TW">台</button><button data-m="US">美/日/韩</button></div>
<div class="grid" style="margin-top:12px"><div class="card" style="padding:6px"><div id="pcb-cNet" class="chart" style="height:600px"></div><div class="note" style="padding:0 6px">手机上按环节分簇固定排布，可双指缩放、拖动；电脑上为力导向布局。</div><div style="display:flex;justify-content:flex-end;padding:4px 6px"><button class="btn" onclick="pcbNet()">重置视图</button></div></div>
<div class="card" id="pcb-nodeInfo"><b>点击图中任一节点</b><div class="note">显示代码、角色与关联边及来源。</div></div></div>
<h3>公司清单</h3><div class="tbl"><table id="pcb-coT"><thead><tr><th>公司</th><th>代码</th><th>环节</th><th>角色 / 数据</th></tr></thead><tbody></tbody></table></div>
<div id="iface"><h3>对外接口：和 HBM、CoWoS 串起来，谁是木桶短板</h3>
<p class="sub">三页用同一个分母（KGI AI 加速器颗数）。本页读取 CoWoS 页的约束推导结果（ABF、HBM、CoWoS 满足率），不重复建模；拖动第 5 步滑块，左图实时更新。</p>
<div class="grid g2"><div class="card"><div id="pcb-cIf" class="chart" style="height:320px"></div><div class="note" id="pcb-ifTxt"></div></div>
<div class="card"><div class="tbl"><table><thead><tr><th>输出</th><th>2026</th><th>2027</th><th>说明</th></tr></thead><tbody id="pcb-ifT-b"></tbody></table></div></div></div>
<p class="card" style="margin-top:12px"><b>约束公式</b><br><span id="pcb-formula"></span></p></div>'''),
 ],
 src_small='均于 2026-10-20 打开 · 局限',
 src='''<p class="sub">均于 2026-10-20 用 curl 或浏览器打开核对（标"只看到搜索摘要 / 摘要页"的除外）。券商数据多为二手转述，标在标题里；纪要、自媒体标"弱"。</p><ol class="src" id="pcb-srcL"></ol>
<h3>局限（公开数据补不了的）</h3><ul style="font-size:14px" id="pcb-lim"></ul>''',
 log='''<div class="tbl"><table id="pcb-logT"><tbody></tbody></table></div>
<p><a href="pcb/pcb_model.xlsx">下载模型 Excel</a> · <a href="pcb/pcb_chain.md">报告原文 (Markdown)</a> · <a href="SOP.md">小链研究 SOP</a> · 构建：<code>./build.sh</code>（页面 <code>tpl/page.py</code> + <code>pcb/page.py</code>，模型 <code>pcb/model.py</code>）</p>''',
)
