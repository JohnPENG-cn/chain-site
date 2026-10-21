"""铜页内容 spec（逻辑层 + 结论层 + 底稿 13 步 + 中国账本）。由 tpl/page.py 渲染成 cu.html。
大宗商品系列第一篇；数字来自 cu/build.py 写出的 cu_data/model_out.json，来源编号来自 cu/src.py。"""
import json, os, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import importlib.util
_sp = importlib.util.spec_from_file_location('cu_src', os.path.join(R0, 'cu', 'src.py'))   # 不用 import src：PCB 页也有 src.py，同进程会撞名
_m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
ID = _m.ID
O = json.load(open(os.path.join(R0, 'cu_data', 'model_out.json')))


def S(*k):
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{ID[x]}">源{ID[x]}</a>' for x in k) + '</span>'


E = '<span class="tag t-est">估</span>'
R, G, X, SC, B = O['R'], O['gbal'], O['exus'], O['SC'], O['B']
G27, X27, X26 = G['2027'], X['2027'], X['2026']
DC27, DDC, KG27 = R['dc27'], R['ddc'], R['kg27']
BEAR, BASE, BULL = SC
EV = O['EV']
f = lambda v: f'{v:,.0f}'.replace('-', '−')   # 负号用 U+2212，与 JS 一致
sg = lambda v: f'{v:+,.0f}'.replace('-', '−')
DUSE = 29305 - 28590
VIS = O['VIS']
CI = O['CI']
TOC = O['TOC']

GOV = f'2027 年铜不缺"量"、缺"位置"：全球小过剩（约 {sg(G27)} 千吨）、美国以外小缺口（约 {sg(X27)} 千吨）；基准均价约 {f(BASE["avg"])} 美元、先紧后松，低于远期和高盛'

LOGIC = dict(
 title='铜 一屏看懂：2027 年供需怎么走、卡在哪、预期差在哪',
 qa=[
  (f'全球精铜 2027 年小过剩：ICSG +368 千吨 {S("icsg")}，我们约 {sg(G27)} {E}；但美国囤了 1.6–2 百万吨 {S("usst", "mcom")}，美国以外是缺口（高盛 −220 {S("gs")}，我们约 {sg(X27)} {E}）',
   f'中国消费占全球 59% {S("icsg")}，2027 年需求基本零增长（麦格理）{S("mcom")}：地产投资 −20.6% {S("nbs")}、空调内销 −23.7% {S("ac")}，电网 +4% {S("grid")}；高价下中国在"让出"金属——9 月精铜进口 −16.7%、出口 +81% {S("cnim")}'),
  (f'约束在精矿，不在冶炼：冶炼想做 31.0 百万吨，精矿只够 29.7 {S("icsg")}；TC 从 2015 年 107 美元跌到现货 −272 {S("tch", "fm")}。快变量是库存的位置：美国以外可见库存只有约 {VIS["tot"]:.0f} 千吨（约 {VIS["days"]} 天）{E}',
   f'中国冶炼占全球约一半，精矿自给约 13% {S("usgs")} {E}；现货冶炼亏损 4,129 元/吨，仍有新厂投产 {S("smm")}——冶炼厂在替矿山"补贴"'),
  (f'主流（高盛 15,400、远期 14,405）{S("gs")} 把中国废铜替代（+2,985）和资金持仓（+775）算进基本面；我们基准 {f(BASE["avg"])}、概率加权 {f(EV)} {E}，2027 年下半年比上半年松，2028 年方向向下',
   f'2027 年最大的中国开关是国储收储和废铜票据政策，而不是 AI：协会 2 月呼吁扩储，至今未见落地 {S("srb")}；反向开票限额让废铜变成精铜需求 {S("vat", "gs")}'),
 ],
 terms='名词：<b>精矿</b> = 矿山选出的铜精矿，冶炼厂的原料；<b>TC/RC</b> = 冶炼厂向矿山收的加工费，负数 = 冶炼厂倒贴买矿，越低说明精矿越紧；<b>美国以外平衡</b> = 全球平衡减去美国囤货（关税悬而未决时，美国库存不服务其他地区）；<b>COMEX / LME / 上期所</b> = 纽约 / 伦敦 / 上海铜交易所；<b>Section 232</b> = 美国以国家安全为由的进口关税。',
 three=[f'2027 年全球精铜并不短缺（ICSG +368 千吨）{S("icsg")}，可美国在关税悬而未决时囤了 1.6–2 百万吨 {S("usst", "mcom")}，美国以外反而缺货（高盛 −220 千吨）{S("gs")}——价格由"铜在哪"定，不由"有多少"定。',
        f'供给的硬约束在精矿：TC 跌到 −272 美元 {S("fm")}，Grasberg 2027 年中才回到 80% {S("fcx")}，智利 2026 年 −7% {S("quiroz")}；新需求里 AI 数据中心 2027 年约 +{DDC:.0f} 千吨（每颗加速器约 {KG27:.0f} kg）{E}，但中国地产、空调、汽车在缩，AI 是补洞不是造周期。',
        f'所以 2027 年是"先紧后松"：上半年最紧，下半年 Grasberg、Kamoa、TC 都在回升 {S("fcx", "ivn2", "cru")}；我们的基准均价 {f(BASE["avg"])} 美元、熊 / 基准 / 牛 = 30% / 50% / 20% {E}，关税决定是最大的开关。'],
 keys=[(sg(X27), '2027 美国以外平衡（千吨，我们）'), (f(BASE['avg']), '2027 基准均价（美元/吨）'), ('−272', '现货 TC（美元/吨，10-09）')],
 fig=[('需求', f'中国 59%：地产 −、电网 +；AI 数据中心 +{DDC:.0f} 千吨'), ('精矿（矿山）', 'Grasberg 67%、智利 −7%、Cobre Panamá 停'), ('冶炼 / 精炼', '产能想做 31.0，精矿只够 29.7（百万吨）'),
      ('库存位置', '美国 1.6–2 百万吨 vs 美国以外约 0.34'), (f'约束：精矿 + 位置', f'美国以外 {sg(X27)} 千吨 → 基准 {f(BASE["avg"])} 美元')],
 fig_note=f'平衡与精矿 {S("icsg")}；美国库存 {S("usst", "mcom")}；矿山 {S("fcx", "quiroz", "panama")}；美国以外平衡、数据中心用铜、价格是 Kiko 的推算 {E}。',
 cons=[
  [f'高盛：2027 年均价 15,400，美国以外缺口 220 千吨 {S("gs")}',
   f'基准 {f(BASE["avg"])}、概率加权 {f(EV)} {E}；美国以外缺口约 {f(-X27)} 千吨', '缺口差不多，差在两项"非基本面加项"：废铜替代 +2,985、持仓 +775',
   f'两项加起来约 3,760 美元，占高盛 2027 均价的约 24% {S("gs")}；废铜替代取决于税务票据政策 {S("vat")}', '中国放宽反向开票 → 我们对；LME + 上期所库存 2027Q1 < 20 万吨 → 高盛对'],
  [f'ICSG / 麦格理：2027 年全球过剩 368 / >700 千吨，麦格理按 Cobre Panamá 2027 年中全面复产算 {S("icsg", "mcom")}',
   f'全球过剩更小（约 {sg(G27)}）；Cobre Panamá 2027 年不复产 {E}', '矿山恢复速度',
   f'巴拿马总统未授权谈判 {S("panama")}；Escondida FY27 指引 1.0–1.1 百万吨（FY26 约 1.26）{S("bhp")}；Kamoa 2026 年趋向下沿 {S("ivn")}', '巴拿马 2027-03 前签复产协议 → 我们错（C4）'],
  [f'AI 带来铜的新超级周期：2040 年需求 42 百万吨（S&P）{S("spg")}',
   f'2027 年数据中心用铜增量约 +{DDC:.0f} 千吨，相当于 ICSG 消费增量（+{DUSE}）的约 {DDC/DUSE*100:.0f}% {E}；但中国传统需求在缩', '量级对，方向被高估：AI 是补洞',
   f'KGI 加速器 × kW × 吨/MW {S("kgi", "semi", "kpler")}；地产投资 −20.6% {S("nbs")}；新能源车零售 −12.8% {S("nev")}', 'ICSG 2027 消费增速上修到 > 3.5% → 我们错（J2）'],
  [f'BMO：美国库存可能"在原地待很多年"，价格有基本面支撑 {S("mcom")}',
   f'美国 1.6–2 百万吨是压着的弹簧：明确不征或推迟 → 熊市情景（30%）{E}', '熊市概率：主流低估',
   f'麦格理：明确不征 → COMEX 崩，带着 LME 一起跌 {S("mcom")}；市场给 15% 关税的概率只有约 8% {S("mcom")}', 'COMEX–LME 价差连续 1 个月 < 0 → 熊市情景开始（J5）'],
  [f'<b>中国：</b>中国迟早会补库（BMO）/ 中国几十年一直在加储备（德银）{S("mcom")}',
   '2026 年中国在高价下让出金属，2027 年基准不补库；补库是牛市情景的开关', '中国开关的方向',
   f'9 月精铜进口 −16.7%、出口 +81% {S("cnim")}；洋山溢价 137 美元 {S("gsr")}；收储只停留在协会呼吁 {S("srb")}', '官方收储公告或精铜进口单月 > 40 万吨 → 切到牛市（N3 / CJ1）'],
 ],
 watch=[
  ['关税决定', 'COMEX 12 月 − LME 三月价差；白宫 / 商务部公告', '> 800 美元 → 最后一波进美国（牛）；连续 1 个月 < 0 → 熊市情景', '11-03 中期选举后；2027-01-01'],
  ['美国以外库存', 'LME + 上期所 + 保税（周）', f'现在约 {VIS["tot"]:.0f} 千吨；< 250 千吨 → 上半年最紧；> 500 千吨 → 基准错', '每周'],
  ['精矿', '现货 TC（Fastmarkets / SMM）', '−272 → 回到 −100 以上 = 精矿松动（M1）；< −350 = 矿山再出事', '每周'],
  ['中国信贷与收储', '信贷脉冲（本站世界页）；精铜进口；国储公告', f'脉冲 −2.58% → 2027-03 铜价同比约 {sg(CI["pred"])}%；转正 = 6 个月后偏多', '每月'],
  ['大矿恢复', 'Grasberg 选厂吨/日；Kamoa 季产；Cochilco 智利月产', 'Grasberg 2027 年中 < 75% 或智利同比仍负 → 牛市情景概率上调', '每季'],
 ],
)

TOCBLOCK = f"""<div class="card"><b>推导过程（每一步都能在 Excel「平衡」表复核）</b><ol style="font-size:14px;margin:8px 0 0 18px;line-height:1.7">
<li><b>定单位</b>：千吨铜 / 年。各环节"能给出的 ÷ 想要的" = 满足率；最低的就是约束（Goldratt TOC）。和 CoWoS / PCB 页的接口另用"每颗 AI 加速器用多少铜"（第 12 步）。</li>
<li><b>冶炼 vs 精矿</b>：ICSG 把冶炼厂按产能想做的精炼量（未调整）2026 / 2027 年 29,294 / 31,012 千吨，按精矿可得量压到 28,693 / 29,673 {S('icsg')} → 满足率 {TOC['2026']['conc']*100:.1f}% / {TOC['2027']['conc_icsg']*100:.1f}%。我们再扣 250 千吨矿山（Escondida FY27 指引、智利 −7%、Cobre Panamá 不复产）{S('bhp', 'quiroz', 'panama')} → 2027 年 <b>{TOC['2027']['conc']*100:.1f}%</b> {E}。冶炼产能本身不缺：亏损时还在投新厂 {S('smm')}。</li>
<li><b>精炼 vs 消费（全球）</b>：2027 年我们 {R['ref27']:,.0f} ÷ {R['use27']:,.0f} = {TOC['2027']['ref']*100:.1f}%——全球不缺。</li>
<li><b>美国以外</b>：把美国净囤货（2026 年约 1,000、2027 年 400 千吨，高盛基准）{S('gs')} 从供给里拿掉 → 2026 / 2027 年 {TOC['2026']['exus']*100:.1f}% / <b>{TOC['2027']['exus']*100:.1f}%</b>。</li>
<li><b>缓冲</b>：美国以外可见库存 LME 233.8 + 上期所 74.0 + 保税 31.2 ≈ {VIS['tot']:.0f} 千吨 {S('lme', 'shfe', 'bond')}，只够全球约 {VIS['days']} 天消费 {E}。缓冲越薄，1% 的缺口对价格的冲击越大。</li>
<li><b>结论</b>：慢约束 = 精矿（矿山，缓解要 2–3 年）；快约束 = 美国以外库存（关税一纸公告就能变）。两者都指向 2027 年上半年最紧。<b>校准</b>：2026 年全球过剩 104 千吨 {S('icsg')}，价格却创纪录 {S('mcom')}——说明"全球满足率 &gt; 100%"不等于价格会跌，看美国以外这一列。</li>
</ol></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><b>各环节满足率（能给出 ÷ 想要）</b><div id="cu-cToc" class="chart" style="height:320px"></div><div class="note">2027 跟随第 5 步滑块重算；100% 以下 = 缺。</div></div>
<div class="card"><b>精矿紧张的价格信号：TC/RC 长单基准（美元/吨）</b><div id="cu-cTc" class="chart" style="height:320px"></div><div class="note">长单 {S('tch', 'tc0')}；2026 年现货 −272（10-09）{S('fm')}；2027 年 Los Pelambres 约 −330 {S('anto')}；CRU 预计 2027Q4 现货回到 −75 {S('cru')}。</div></div></div>"""

SL = lambda k, lo, hi, st, v: f'<label>{{}}<output id="cu-o-{k}"></output></label><input type="range" id="cu-{k}" min="{lo}" max="{hi}" step="{st}" value="{v}">'
LB = {'mine27': '2027 矿山相对 ICSG（千吨）', 'kw27': '2027 每颗加速器 IT 功率（kW）', 'tpm': '数据中心单位用铜（吨/MW）', 'g27': '2027 非数据中心需求增速（%）', 'us27': '2027 美国净囤货（千吨，负 = 回流）',
      'scrap27': '中国废铜→精铜替代（千吨）', 'cn27': '中国国储 / 补库（千吨）', 'pb': '熊市概率（%）', 'pu': '牛市概率（%）'}
SLD = [('mine27', -700, 200, 50, -250), ('kw27', 1.0, 2.4, 0.1, 1.6), ('tpm', 15, 45, 1, 27), ('g27', -2, 2, 0.25, 0.5), ('us27', -800, 1200, 50, 400), ('scrap27', 0, 600, 50, 0), ('cn27', 0, 500, 50, 0)]
SLIDERS = ''.join(SL(k, a, b, c, d).format(LB[k]) for k, a, b, c, d in SLD)
PSL = ''.join(SL(k, a, b, c, d).format(LB[k]) for k, a, b, c, d in [('pb', 0, 70, 5, 30), ('pu', 0, 60, 5, 20)])

SPEC = dict(
 logic=LOGIC,
 file='cu.html', title='铜 · 2027 供需与价格', pill='铜 v0.1', other=('index.html#commod', '大宗 ⇄'), scripts=['cu.js'],
 cons_sub='左边是投行、研究机构、行业组织的公开说法（带来源）；"差距"一栏就是预期差。',
 ledgers=[('a1', 'gl', '全球账本', f'2027 年全球精铜小过剩（约 {sg(G27)} 千吨），美国以外小缺口（约 {sg(X27)}）；约束是精矿和库存位置，价格先紧后松'),
          ('cn', 'cnl', '中国账本', '中国是全球一半的冶炼厂、59% 的买家，却只有约 13% 的精矿自给；2027 年开关在收储和废铜政策')],
 kicker='大宗商品 · 矿产与能源 2027 系列 · 铜 v0.1 · 更新 <span id="cu-upd"></span> · 统一单位接 <a href="cowos.html">CoWoS</a> / <a href="pcb.html">PCB</a> 页的 AI 加速器',
 card=f'全球账本：2027 年铜全球小过剩、美国以外小缺口（约 {sg(X27)} 千吨），约束是精矿和库存位置；基准均价约 {f(BASE["avg"])} 美元、先紧后松。中国账本：冶炼一半、精矿自给约 13%，开关在收储和废铜政策{E}',
 scqa=[
  f'铜价在 2026 年创了纪录：LME 现货 10-12 收在 14,822 美元 {S("mcom")}，2026 年均价约 {f(O["AVG26"])}（11–12 月按 14,500 假设）{E}；实际价格已接近 2011 年高点 {S("fred")}。',
  f'可 ICSG 说 2026、2027 年全球都是过剩（+104 / +368 千吨）{S("icsg")}；美债实际利率在 99 分位、铜金比在 9 分位、中国信贷脉冲 −2.58% {S("wi")}，中国地产投资 −20.6% {S("nbs")}——宏观在说"弱"，价格在说"缺"。',
  '2027 年铜到底缺不缺？卡在哪一环？价格会怎么走、哪几个开关会让它走成熊市或牛市？主流预测哪里多算了、哪里少算了？'],
 gov=GOV,
 mece='四条论点分别回答"量（铜在哪）""需求（新旧）""约束（TOC）""价格与预期差"，互不重叠。AI 数据中心和 CoWoS / PCB 页用同一个分母（KGI 加速器颗数）。中国的账另算（见<a href="#cn">中国账本</a>）。',
 args=[
  dict(tag='平衡', claim=f'2027 年全球精铜小过剩（我们约 {sg(G27)} 千吨，ICSG +368），但美国在关税悬而未决时囤了 1.6–2 百万吨，美国以外是缺口（约 {sg(X27)}）——价格由铜在哪定',
   key=f'2027 全球 <b data-from="cu-sG">—</b> · 美国以外 <b data-from="cu-sX">—</b> 千吨 {E}',
   sub='全球平衡 = ICSG 精炼（按精矿调整）+ 我们的矿山修正 − 消费（非数据中心 × 增速 + AI 数据中心 + 废铜替代 + 中国补库）；美国以外 = 全球 − 美国净囤货。',
   hero=dict(src='cu-cBal', step='balance', t='2027 平衡：从 ICSG 到美国以外（千吨）', h=340, note='跟随底稿第 5 步的滑块实时重算。'),
   ev=[
    dict(t=f'2026 年就是这样：全球过剩、美国以外缺 {f(-X26)} 千吨', b=f'ICSG 2026 年 +104 千吨 {S("icsg")}；高盛：美国 2026 年囤约 1 百万吨，美国以外缺 950 {S("gs")}；麦格理：全球可见库存今年 +300 千吨，全在美国，美国以外 −168 {S("mcom")}。', steps=['balance']),
    dict(t='美国库存：COMEX 约 71.8 万吨，合计 1.6–2 百万吨', b=f'COMEX 791,679 短吨 {S("gsr")}；美国交易所内外约 1.6 百万吨 {S("usst")}，BMO 估近 2 百万吨、约一年美国消费 {S("mcom")}。USGS：美国 2025 年精铜消费约 1.7 百万吨 {S("usgs")}。', steps=['balance', 'play']),
    dict(t='关税是开关：精铜 15%（2027）/ 30%（2028）仍未决定', b=f'2025-07 公告只对半成品征 50% {S("p232")}；9-10 路透报道方案搁置 {S("stall")}；12 月 COMEX 比 LME 高约 170 美元 ≈ 8% 概率 {S("mcom")}。', steps=['play', 'hist']),
    dict(t='要害变量：美国囤货一项就能把缺口翻成过剩', b='龙卷风图里"美国 2027 净囤货"的摆幅最大（回流 500 → 再囤 1,000）；其次是矿山修正和数据中心 kW/颗。', steps=['key']),
   ]),
  dict(tag='需求', claim=f'新需求是真的，但只是补洞：AI 数据中心 2027 年用铜约 {f(DC27)} 千吨（+{DDC:.0f}），每颗加速器约 {KG27:.0f} kg；同时中国地产、空调、汽车在缩，全球消费只增约 {R["ug"]:.1f}%',
   key=f'数据中心增量 <b>+{DDC:.0f}</b> 千吨 ≈ ICSG 增量的 <b>{DDC/DUSE*100:.0f}%</b> {E}',
   sub='数据中心用铜 = KGI 加速器 × 每颗 IT 功率 × 吨/MW；和 CoWoS / PCB 页同一个分母。传统需求用中国的官方高频数据看方向。',
   hero=dict(src='cu-cDem', step='demand', t='2027 年消费增量拆分（千吨）：我们 vs ICSG', h=320, note='跟随第 5 步滑块重算；传统 = 非数据中心部分。'),
   ev=[
    dict(t=f'AI：2027 年约 {f(DC27)} 千吨，每颗约 {KG27:.0f} kg', b=f'KGI 25.75 百万颗 {S("kgi")} × 1.6 kW（SemiAnalysis 2026 年 25 GW ÷ 17.8 百万颗 ≈ 1.41；2027 年 51.2 GW ÷ 25.75 ≈ 1.99）{S("semi", "semi2")} × 27 吨/MW {S("kpler")} {E}。交叉验证：BNEF 年均约 40 万吨、2028 年峰值 57.2 万吨 {S("bnef")}。', steps=['demand']),
    dict(t='传统：中国地产、汽车、空调在负增长', b=f'房地产开发投资 −20.6% {S("nbs")}；新能源乘用车零售 −12.8%（1–9 月）{S("nev")}；空调内销 9 月 −23.7% {S("ac")}；麦格理：2027 年中国需求零增长、建筑用铜每年 −9% {S("mcom")}。', steps=['demand']),
    dict(t='电网是唯一稳的传统需求', b=f'全国电网投资上半年 +4.0% {S("grid")}，国家电网 +12.6% {S("sgcc")}。', steps=['demand']),
    dict(t='高价替代：铝代铜在空调里加速', b=f'铜铝比 4.41；2027 年空调铝代铜渗透率 15–20%，少用铜 4–7 万吨 {S("alsub")}；铜对铝溢价 9 月创纪录 5.08 美元/磅 {S("mcom")}。量不大，但会在 15,000 以上加速。', steps=['demand', 'profit']),
   ]),
  dict(tag='约束', claim=f'约束在精矿，不在冶炼：冶炼想做 31.0 百万吨、精矿只够 29.7；TC 从 2015 年 107 美元跌到现货 −272。2027 年上半年仍紧，下半年随 Grasberg、Kamoa 回升而松',
   key=f'2027 精矿满足率 <b>{TOC["2027"]["conc"]*100:.1f}%</b> · 现货 TC <b>−272</b> 美元 {S("icsg", "fm")}',
   sub='按约束理论：把矿山、冶炼、精炼、库存换成同一单位（千吨/年），最低的满足率就是约束。',
   hero=dict(src='cu-cTc', step='neck', t='TC/RC 长单基准（美元/吨）：十年从 107 到 0，现货已到 −272', h=320, note='长单与现货的来源见底稿第 7 步。'),
   ev=[
    dict(t='TOC 推导：精矿 < 美国以外 < 全球', b=f'精矿满足率 {TOC["2027"]["conc"]*100:.1f}%、美国以外 {TOC["2027"]["exus"]*100:.1f}%、全球 {TOC["2027"]["ref"]*100:.1f}% {E}。', steps=['neck']),
    dict(t='大矿：Grasberg 67%、Kamoa 下沿、智利 −7%、Cobre Panamá 停', b=f'Grasberg 2027 年中 80%、年底接近满产 {S("fcx")}；Kamoa 2027 年 380–420 千吨 {S("ivn2")}；智利财长 2026 年 −7% {S("quiroz")}；Escondida FY27 1.0–1.1 百万吨 {S("bhp")}。', steps=['supply', 'map']),
    dict(t='冶炼不缺：亏损还在扩', b=f'中国现货冶炼亏损 4,129 元/吨，9、10 月仍有两家 30 万吨新厂投产 {S("smm")}；Kamoa 自家冶炼厂只开 60% {S("ivn")}。', steps=['supply', 'neck']),
    dict(t='下半年松动的信号：硫酸、TC、指数定价', b=f'CRU：硫酸 451 → 215 美元（2027Q4），现货 TC 回到 −75 {S("cru")}；年度定价占比 52% → 14%、指数定价 12% → 51%{S("cru")}；2027 长单可能谈不成 {S("dd")}。', steps=['neck', 'hist']),
   ]),
  dict(tag='价格', claim=f'基准 2027 年均价约 {f(BASE["avg"])} 美元（{f(BASE["lo"])}–{f(BASE["hi"])}），熊 / 基准 / 牛 = 30% / 50% / 20%，概率加权约 {f(EV)}；低于远期 14,405 和高盛 15,400，因为我们不把废铜替代和资金持仓当作持久的基本面',
   key=f'概率加权 <b id="cu-kEv">{f(EV)}</b> 美元/吨 · 高盛 <b>15,400</b> {S("gs")}',
   sub='库存-价格的回测失败（第 10 步），所以价格不用公式反推：三情景各自用同一个平衡模型算内部一致性，价格锚在成本曲线、激励价和一致预期上，概率可以拖动。',
   hero=dict(src='cu-cPath', step='balance', t='季度价格：实际（2024–2026）与 2027 三情景（美元/吨）', h=360, note='灰带 = 90 分位全成本（地板）；虚线 = 激励价。'),
   ev=[
    dict(t='地板与天花板：成本曲线 7.7–8.8k，激励价 11–12.1k', b=f'90–95 分位全成本 3.5–4.0 美元/磅 {S("icaa")}；伍德麦肯兹激励价 > 5.00 美元/磅 {S("wm")}；瑞银长期 5.50 {S("icaa")}；北美铜企 1.0 倍 NAV 隐含 5.03 美元/磅 {S("mcom")}。现价比激励价高约 20%。', steps=['profit', 'balance']),
    dict(t='高盛 15,400 里有约 3,760 美元来自两项可逆因素', b=f'中国废铜→精铜替代 +2,985、持仓 +775 {S("gs")}；前者取决于票据政策 {S("vat")}，后者取决于资金是否留在场内。', steps=['debate', 'balance']),
    dict(t=f'信贷脉冲领先 6 个月：2027-03 铜价同比约 {sg(CI["pred"])}%', b=f'中国信贷脉冲领先铜价同比 6 个月，样本外 r = {CI["r_out"]:.2f}、方向命中 {CI["sign_out"]*100:.0f}%；现在 −2.58% → 2027-03 约 {f(O["CI_PX"])} 美元（±1σ {f(O["CI_LO"])}–{f(O["CI_HI"])}）{S("ts", "fred")} {E}。', steps=['lead']),
    dict(t='估值高本身不是卖出信号', b=f'实际价格 z 分数 {O["Z"]["now"]}（滚动 10 年）；历史上 z > 1.5 之后 12 个月下跌的概率只有 {O["Z"]["1.5"]["down"]*100:.0f}%（2005–07 超级周期）{S("fred")} {E}。所以我们不因为"贵"判熊，而是因为"位置会变"。', steps=['lead', 'hist']),
    dict(t='2028 年方向：向下', b=f'矿山 +4.3%（麦格理）{S("mcom")}、Kamoa 500 千吨 {S("ivn2")}、Grasberg 满产 {S("fcx")}，SemiAnalysis 提示 2028 年数据中心过剩风险 {S("semi2")}；反方：BMO 2028 年 16,000、精铜 30% 关税 {S("mcom", "p232")}。', steps=['hist', 'play']),
   ]),
 ],
 cn=dict(
  nav='中国账本', kicker='中国视角：最大的冶炼国和买家，却不是矿主（与全球账本口径不重复）',
  scqa=[f'中国 2025 年精炼铜约 14.0 百万吨、占全球约一半，矿产只有 1.8 百万吨 {S("usgs")}；消费占全球 59% {S("icsg")}。紫金、洛阳钼业在海外快速扩产 {S("zijin", "cmoc")}。',
        f'2026 年铜价创纪录，中国却在少买：9 月精铜进口 −16.7%、出口 +81% {S("cnim")}；冶炼厂按现货精矿每吨亏 4,129 元仍在投新厂 {S("smm")}；地产、空调、汽车需求在缩 {S("nbs", "ac", "nev")}。',
        '中国的需求 2027 年会不会回来？冶炼会不会真减产？国储会不会收储——它会不会把全球的"位置约束"翻过来？'],
  gov='中国在 2026 年高价下让出了金属，2027 年需求接近零增长；冶炼受精矿卡脖子、现货亏损；最大的中国开关是国储收储和废铜票据政策',
  mece='三条中国论点分别回答"需求与贸易（够不够）""冶炼与精矿（卡在哪）""开关与对冲（何时变）"。',
  args=[
   dict(tag='让出', claim='2026 年中国在高价下"让出"金属：精铜进口降、出口升，BMO 估累计净贸易摆动约 1.6 百万吨；2027 年中国需求接近零增长，只有电网在增',
    key='9 月进口 <b>−16.7%</b> · 出口 <b>+81%</b> ' + S('cnim'),
    sub='中国表观消费 = 产量 + 净进口 ± 上期所库存，不含国储与隐性库存（ICSG 口径）。',
    hero=dict(src='cu-cnDem', step='demand', t='中国终端高频：同比（%）', h=300, note='地产、汽车、空调在缩，电网在增。'),
    ev=[
     dict(t='需求：地产 −20.6%、空调内销 −23.7%、电网 +4%', b=f'{S("nbs", "ac", "grid", "sgcc")} 麦格理：2027 年中国需求 0 增长 {S("mcom")}。', steps=['demand']),
     dict(t='贸易：进口降、出口升', b=f'9 月精铜进口 311.6 千吨（−16.7%），出口 47.9 千吨（+81%）{S("cnim")}；洋山溢价 137 美元 {S("gsr")}。', steps=['balance']),
     dict(t='隐性库存：国储可能在被动用', b=f'BMO：净贸易摆动约 1.6 百万吨 = 北京让储备下降、华盛顿在建储备 {S("mcom")}；ICSG 不把国储算进中国表观消费 {S("icsg")}。', steps=['balance', 'play']),
    ]),
   dict(tag='卡脖子', claim='中国冶炼的约束是精矿：精矿自给约 13%，现货 TC −272 美元，冶炼按现货每吨亏 4,129 元；新厂还在投，联合减产未落地——2027 年中国精炼增速会放缓',
    key=f'冶炼亏损 <b>4,129</b> 元/吨 · 精矿自给约 <b>13%</b> {S("smm", "usgs")}',
    sub='精矿自给 = 国内矿产 ÷ 精炼产量（粗算，精炼含再生原料）。',
    hero=dict(src='cu-cnToc', step='neck', t='中国的满足率（%）：精矿是短板', h=300, note='粗算（估）；详见底稿第 7 步中国块。'),
    ev=[
     dict(t='精矿进口占大头', b=f'9 月精矿进口 248.2 万吨（−4.06%），1–9 月 2,197.4 万吨 {S("cnconc")}。', steps=['supply']),
     dict(t='冶炼利润：亏损扩大', b=f'9 月现货冶炼月均亏损 4,129 元/吨，10 月或到 5,000 元；10 月产量预计 108.47 万吨、年内最低 {S("smm")}。', steps=['supply', 'neck']),
     dict(t='TOC：精矿 < 冶炼产能', b=f'矿产 1.8 vs 精炼 14.0 百万吨 {S("usgs")} {E}；新厂在亏损时投产 {S("smm")}。', steps=['neck']),
    ]),
   dict(tag='开关', claim='2027 年中国最大的两个开关是国储收储和废铜票据政策；紫金、洛阳钼业的海外权益矿是对冲精矿依赖的长期解',
    key='紫金 2026 年 <b>120 万吨</b> → 2028 年 <b>150–160 万吨</b> ' + S('zijin'),
    sub='A 股按证据强度分级：强 = 公司公告；中 = 媒体转述；弱 = 只有行业层面数据。只列事实，不构成投资建议。',
    hero=dict(src='cu-cnCo', step='map', t='中国权益矿产量（万吨铜）', h=280, note='紫金 2026 年为规划、2028 年为区间中值；洛钼为 2026 年指引中值。'),
    ev=[
     dict(t='收储：协会呼吁、未落地', b=f'2 月有色协会呼吁扩大国家铜储备、把精矿纳入 {S("srb")}。一旦落地，会把美国以外的缺口放大（牛市情景）。', steps=['play']),
     dict(t='废铜：票据政策让废铜变精铜需求', b=f'反向开票单人 12 个月 500 万元上限 {S("vat")}；高盛估废铜替代给 2027 年均价 +2,985 美元 {S("gs")}。', steps=['play', 'balance']),
     dict(t='海外权益矿：紫金、洛钼', b=f'紫金 2026 年 120 万吨、2028 年 150–160 万吨 {S("zijin")}；洛阳钼业 2026 年 76–82 万吨、上半年 38.8 万吨 {S("cmoc", "cmoc2")}。', steps=['map']),
    ]),
  ]),
 wrong='''<p class="sub">每条判断：现在已经看到的反方证据、什么情况算我错、看哪个公开指标、阈值多少。J1↔论点①、J2↔②、J3↔③、J4/J5↔④。触发阈值就改判断，不辩护。</p>
<div class="tbl"><table id="cu-falT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：CJ1–CJ3</h3><p class="sub">CJ1↔中国论点❶、CJ2↔❷、CJ3↔❸。</p>
<div class="tbl"><table id="cu-cnFalT" class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 pred='''<p class="sub" id="cu-predSum"></p><p class="sub">2026-10-21 写入。到期后按公开数据打分，不改原文，只追加结果。C 系列是价格与平衡判断，M 系列是约束迁移，N 系列是中国账本。</p>
<div class="tbl"><table id="cu-predT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>
<h3>中国账本：N 系列</h3><p class="note" id="cu-cnPredS"></p>
<div class="tbl"><table id="cu-cnPredT" class="stack ledger"><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody></tbody></table></div>''',
 base_title='铜 产业链底稿',
 base_sub='上面的结论都从这里来。按 SOP 顺序：先找要害变量和争议，再定边界、算供需、看利润和约束，最后看玩家、历史、领先指标和公司。右侧圆圈 = 这一步支撑哪条论点。大宗商品版：第 5 步多了价格情景与一致预期，第 6 步是成本曲线。',
 steps=[
  dict(id='key', h='哪个假设能把"美国以外缺口"翻成过剩', body='''<p class="note">指标 = 2027 年美国以外精铜平衡（千吨，负 = 缺）。每一行只动一个变量，其他保持基准。虚线 = 0（翻转线）。</p>
<div class="grid g2"><div class="card"><b>2027 美国以外平衡的龙卷风图（千吨）</b><div id="cu-cTor" class="chart" style="height:340px"></div></div>
<div class="card"><b>怎么读</b><p style="font-size:14px;margin:.4em 0">美国囤货一项的摆幅最大——这就是为什么关税决定是 2027 年的头号开关。第二是矿山修正（ICSG 已含 959 千吨干扰扣减，我们再扣 250）。数据中心 kW/颗、吨/MW 两项合起来约 ±500 千吨，量级和美国囤货相当，但方向只会加需求。<span class="tag t-est">估</span></p><div class="tbl"><table id="cu-torT" class="stack"><thead><tr><th>变量</th><th>低端</th><th>高端</th><th>依据</th></tr></thead><tbody></tbody></table></div></div></div>'''),
  dict(id='debate', h='三个可证伪的核心争议', ctx='对应结论层「可能错在哪」↑', body='<div class="grid g3" id="cu-deb"></div>'),
  dict(id='proc', h='从矿到铜材：环节、计量单位与价格体系', ctx='背景：定义单位与边界', sub='计量单位：千吨铜（含铜量）；价格：LME 现货美元/吨（1 美元/磅 = 2,204.62 美元/吨）。精铜 = 阴极铜；平衡只算精铜，不算精矿和废铜直接利用。',
   body='''<h3>环节</h3><div class="tbl"><table id="cu-procT"><thead><tr><th>环节</th><th>要点</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<h3>价格体系（2026-10 中旬）</h3><div class="tbl"><table id="cu-prT"><thead><tr><th>价格</th><th>读数</th><th>来源</th></tr></thead><tbody></tbody></table></div>'''),
  dict(id='demand',
   cn=dict(h='中国需求：传统在缩、电网在增', body=f'''<div class="grid g2"><div class="card"><div id="cu-cnDem" class="chart" style="height:300px"></div><div class="note">同比（%），时间口径见右表。</div></div>
<div class="card"><div class="tbl"><table id="cu-cnDemT" class="stack"><thead><tr><th>指标</th><th>同比</th><th>期间</th><th>来源</th></tr></thead><tbody></tbody></table></div><div class="note">铝代铜：2027 年空调渗透率 15–20%，少用铜 4–7 万吨，不到国内消费 0.4% {S("alsub")}。</div></div></div>'''),
   h='需求：传统 vs 新兴，AI 用和 CoWoS / PCB 同一个分母', body=f'''<div class="grid g2"><div class="card"><b>2027 年消费增量（千吨）：我们 vs ICSG</b><div id="cu-cDem" class="chart" style="height:320px"></div><div class="note">ICSG 2027 年消费 +{DUSE} 千吨（+2.5%）{S("icsg")}；我们 = 数据中心增量 + 非数据中心增量 + 废铜替代 + 中国补库 {E}。</div></div>
<div class="card"><b>AI 数据中心用铜（千吨）与每颗加速器用铜（kg）</b><div id="cu-cDc" class="chart" style="height:320px"></div><div class="note">柱 = KGI 颗数 × kW/颗 × 吨/MW {E}；点 = 外部口径：BNEF 年均 400、2028 年峰值 572 {S("bnef")}；Kpler 2026 年 15–20 GW × 27 吨/MW ≈ 405–540 {S("kpler")}。</div></div></div>
<div class="card" style="margin-top:12px"><b>AI 数据中心用铜的推导（估）</b><div class="note" style="font-size:13px">① KGI 加速器 2025 / 2026 / 2027 年 11.63 / 17.77 / 25.75 百万颗（不含 CPU）{S("kgi")}。② 每颗 IT 功率：SemiAnalysis 全球（不含中国）IT 容量净新增 2026 年 25.0 GW、2027 年 51.2 GW {S("semi", "semi2")} → ÷ 颗数 = 1.41 / 1.99 kW；机柜规格交叉验证：GB300 NVL72 最高约 142 kW ÷ 72 ≈ 2.0 kW {S("nv")}，Vera Rubin NVL72 190–230 kW ÷ 72 ≈ 2.6–3.2 kW {S("vr")}，ASIC 更低。2027 年取 1.6 kW（介于 Knight Frank 两年 33 GW 的低口径 {S("kf")} 与 SemiAnalysis 之间）。③ 吨/MW：微软芝加哥 2,177 吨 / 81 MW ≈ 27；AI 高密度 30–45（不含电网）{S("kpler")}。④ 2027 年 = 25.75 × 1.6 × 27 ≈ {f(DC27)} 千吨；每颗约 {KG27:.0f} kg（PCB 页 HVLP 铜箔每颗 1.23 kg {S("pcb")}，相差约 35 倍）。⑤ 中国数据中心、电网配套、国防不在这一项里。</div></div>
<h3>全球需求口径对照</h3><div class="tbl"><table class="stack"><thead><tr><th>来源</th><th>2027 消费增速</th><th>说明</th></tr></thead><tbody>
<tr><td><b>ICSG</b></td><td>+2.5%</td><td>中国 2026 年 +2.5%、其他地区持平；2027 年靠经济复苏和新加工厂 {S("icsg")}</td></tr>
<tr><td><b>麦格理</b></td><td>+1.5%</td><td>中国 0、建筑用铜每年 −9%、空调又在看铝代铜 {S("mcom")}</td></tr>
<tr><td><b>BMI</b></td><td>每年 +3–4%（长期）</td><td>电网、电动车、数据中心 {S("mcom")}</td></tr>
<tr><td><b>我们</b></td><td><span id="cu-ug">—</span></td><td>非数据中心 +0.5%（中国 0、海外小增）+ 数据中心（跟随滑块）{E}</td></tr></tbody></table></div>'''),
  dict(id='supply',
   cn=dict(h='中国冶炼：亏损还在扩，精矿靠进口', body='<div class="tbl"><table id="cu-cnSupT" class="stack"><thead><tr><th>项目</th><th>读数</th><th>来源</th></tr></thead><tbody></tbody></table></div>'),
   h='供给：大矿恢复的节奏决定 2027 年的形状', body=f'''<div class="grid g2"><div class="card"><b>ICSG 矿山与精炼增速 vs 我们（%）</b><div id="cu-cSup" class="chart" style="height:320px"></div><div class="note">ICSG 调整后 = 扣除干扰与精矿约束 {S("icsg")}；2026 年 1–7 月实际矿产 −0.8%、精炼 +1.7% {S("icsgt1")}；我们的 2027 年精炼 = ICSG − 矿山修正（跟随滑块）{E}。</div></div>
<div class="card"><b>大矿 2026 → 2027 变化（千吨）</b><div id="cu-cMine" class="chart" style="height:320px"></div><div class="note">取各自指引或机构预测的中值；Escondida 在智利之内，不要相加。Cobre Panamá 无可靠吨数，只在表里定性。</div></div></div>
<div class="tbl" style="margin-top:12px"><table id="cu-mineT" class="stack"><thead><tr><th>矿</th><th>现状</th><th>2026</th><th>2027</th><th>变化（千吨）</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<p class="note">资本开支滞后：S&P 估从发现到投产十几年 {S("spg")}；伍德麦肯兹认为激励价要超过 5 美元/磅才会加速开发 {S("wm")}。2027 年的增量几乎全部来自"恢复"，不是新矿。</p>'''),
  dict(id='balance',
   cn=dict(h='中国平衡：进口、库存与国储', body='''<div class="tbl"><table id="cu-cnBalT" class="stack"><thead><tr><th>项目</th><th>读数</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="note">ICSG 的中国表观消费 = 产量 + 净进口 ± 上期所库存，不含国储、生产商、贸易商、保税库存变化——这些在收放储时可以"显著改变"全球平衡。</div>'''),
   h='平衡与价格：自己拖动假设和概率', sub='平衡 = 千吨；价格 = 三情景 × 概率（不是公式反推，原因见第 10 步回测）。浏览器里实时重算，结论层的图跟着变。',
   body=f'''<div class="grid g4" id="cu-stats"></div>
<div class="grid g2" style="margin-top:14px"><div class="card"><div class="ctl">{SLIDERS}</div><button class="btn" onclick="cuReset()">恢复基准</button>
<div class="grid g2" style="margin-top:16px;gap:8px"><div><div class="note">2027 全球平衡</div><div class="big" id="cu-g"></div></div><div><div class="note">2027 美国以外</div><div class="big" id="cu-x" style="color:var(--warn)"></div></div></div><div class="note" id="cu-balTxt"></div></div>
<div class="card"><div id="cu-cBal" class="chart" style="height:340px"></div><div class="note">从 ICSG 的 +368 一步步走到我们的美国以外平衡；绿 = 加、红 = 减。</div></div></div>
<h3>价格：三情景 × 概率</h3><div class="grid g2"><div class="card"><div id="cu-cPath" class="chart" style="height:360px"></div><div class="note">2024–2026 为 LME 现货季度均价（2026Q4 = 10 月至今）{S("lme")}；2027 年为情景（估）。灰带 = 90–95 分位全成本 {S("icaa")}，虚线 = 瑞银激励价 5.50 美元/磅 {S("icaa")}。</div></div>
<div class="card"><div class="ctl">{PSL}</div><div class="note">基准概率 = 1 − 熊 − 牛。</div><div class="grid g2" style="margin-top:12px;gap:8px"><div><div class="note">概率加权 2027 均价</div><div class="big" id="cu-ev"></div></div><div><div class="note">基准情景</div><div class="big" id="cu-bs" style="color:var(--warn)"></div></div></div><div class="note" id="cu-evTxt"></div></div></div>
<div class="tbl" style="margin-top:12px"><table id="cu-scT" class="stack"><thead><tr><th>情景</th><th>概率</th><th>2027 均价（区间）</th><th>全球 / 美国以外（千吨）</th><th>触发条件</th></tr></thead><tbody></tbody></table></div>
<p class="note">概率依据：市场给 15% 关税的概率约 8%，麦格理把"1 月 1 日无公告"排为最可能、"明确不征"排为最不可能 {S("mcom")}；牛市还包括供给再出事和中国收储；熊市包括关税落空和中国信贷继续收缩。三项都是 Kiko 的判断 {E}。2026 年均价约 {f(O["AVG26"])}（1–10 月实际 {f(O["YTD26"])} + 11–12 月按 14,500）{E}。</p>
<h3>和一致预期比</h3><div class="grid g2"><div class="card"><div id="cu-cCons" class="chart" style="height:340px"></div><div class="note">紫色 = 我们。瑞银是 2027-06 的点位、花旗是 12 个月目标，不是年均；德银 2027Q2 22,050 {S("mcom")} 太远，不画。</div></div>
<div class="card"><b>各家的 2027 平衡口径（千吨）</b><div class="tbl"><table id="cu-balvT"><thead><tr><th>来源</th><th>2027 平衡</th><th>来源</th></tr></thead><tbody></tbody></table></div><div class="note">同样是"缺口"，BMI 只给 12,900、高盛给 15,400——价格差主要不来自平衡，而来自怎么对待美国库存、废铜替代和资金。</div></div></div>'''),
  dict(id='profit', h='利润池与成本曲线：矿山拿走了全部，冶炼在倒贴', body=f'''<div class="grid g2"><div class="card"><b>价格档位（美元/吨）</b><div id="cu-cBand" class="chart" style="height:360px"></div><div class="note">Kamoa 2027 年 C1 2.10–2.50 美元/磅 {S("ivn2")}；90–95 分位全成本 3.5–4.0 {S("icaa")}；伍德麦肯兹激励价 5.00 {S("wm")}；RBC NAV 隐含 5.03 {S("mcom")}；瑞银长期 5.50 {S("icaa")}；麦格理长期 10,500（2025 年美元）{S("mcom")}。</div></div>
<div class="card"><b>利润在哪</b><div class="tbl"><table class="stack"><thead><tr><th>环节</th><th>读数</th><th>判断</th></tr></thead><tbody>
<tr><td><b>矿山</b></td><td>现价约 14,500 vs 90 分位全成本 7.7–8.8k {S("icaa")}；Kamoa 2027 年 C1 约 4.6–5.5k {S("ivn2")}</td><td>拿走几乎全部利润；大型铜企 2026 年股价多在 +29%～+44%（Antofagasta、First Quantum 落后）{S("mcom")}</td></tr>
<tr><td><b>冶炼（精矿冶炼）</b></td><td>现货 TC −272 {S("fm")}；中国现货冶炼亏 4,129 元/吨 {S("smm")}</td><td>倒贴，靠硫酸（Kamoa 三季度约 900 美元/吨 {S("ivn")}）续命；硫酸 2027Q4 回到 215 {S("cru")}，副产品收入会塌</td></tr>
<tr><td><b>精铜升水 / 贸易</b></td><td>Aurubis 2027 年 347 美元（+10%）{S("mcom")}；洋山 137 {S("gsr")}</td><td>欧洲紧、中国松：位置决定升水</td></tr>
<tr><td><b>美国库存持有者</b></td><td>COMEX 12 月比 LME 三月高约 170 美元 {S("mcom")}</td><td>收期限价差，等关税期权</td></tr>
<tr><td><b>铜材 / 终端</b></td><td>无公开毛利数据</td><td>高价下用铝替代（空调）{S("alsub")}</td></tr></tbody></table></div></div></div>'''),
  dict(id='neck',
   cn=dict(h='中国的约束：精矿自给约 13%', body=f'''<div class="grid g2"><div class="card"><div id="cu-cnToc" class="chart" style="height:300px"></div><div class="note">精矿自给 = 国内矿产 1.8 ÷ 精炼 14.0 百万吨（2025，含再生原料，粗算）{S("usgs")}；冶炼占全球 = 14.0 ÷ 29.0 {S("usgs")}；消费占全球 59% {S("icsg")} {E}。</div></div>
<div class="card"><b>中国 TOC</b><p style="font-size:14px">精矿是硬短板（进口 + 海外权益矿）；冶炼产能过剩（亏损仍投产）；需求不是约束。所以中国冶炼厂能做的只有：减产、抬 TC、或者把国储的"精矿储备"变成谈判筹码 {S("srb")}。</p></div></div>'''),
   h='约束推导：把每一环换成千吨/年，最小的那个才是约束', sub='按 Goldratt 约束理论（TOC）：矿山、冶炼、精炼、库存位置 → 统一成千吨铜/年的满足率。数据只支持按年。',
   body=TOCBLOCK + '\n<h3>汇总排序（推导结果 + 定性证据）</h3><p class="sub">条形长度 = 缓解所需月数（示意）。</p><div id="cu-neck" class="grid"></div>'),
  dict(id='play',
   cn=dict(h='中国账本的玩家', body='<div class="grid g2" id="cu-cnPl"></div>'),
   h='谁在做什么决定，为什么，什么信号说明他们变了', sub='美国政府定关税开关、中国国储定隐形库存、Freeport 和智利定 2027 年的矿山增量、资金放大波动。', body='<div class="grid g2" id="cu-play"></div>'),
  dict(id='hist', h='价格周期与约束迁移', body=f'''<p class="sub" id="cu-rule"></p>
<div class="card"><b>实际铜价（2026-09 美元/吨，1992–2026）与成本档位</b><div id="cu-cLong" class="chart" style="height:340px"></div><div class="note">FRED PCOPPUSDM（IMF 月度）+ 2026-08 起 LME 月均，用美国 CPI 平减 {S("fred", "lme")}；灰带 = 今天的 90–95 分位全成本 {S("icaa")}（成本曲线也随时间上移，只作参照）。</div></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><b>市场与政策</b><div class="tl" style="margin-top:12px" id="cu-tl1"></div></div>
<div class="card"><b>约束迁移</b><div class="tl" style="margin-top:12px" id="cu-tl2"></div></div></div>'''),
  dict(id='lead', h='先看哪个数据（已回测，含失败的）', sub=f'回测结论：① 库存天数 → 价格：失败（样本内 R² {O["FIT"]["r2_in"]:.2f}、样本外为负）；② 库存 3 个月变化 → 未来 3 个月方向：命中 {O["HIT"]["all"]*100:.0f}%，低于"一直猜涨"的 {O["HIT"]["base_up"]*100:.0f}%；③ 估值 z 分数：没有预测力；④ 中国信贷脉冲领先 6 个月：唯一有用的，样本外 r = {CI["r_out"]:.2f}。',
   body=f'''<div class="grid g2"><div class="card"><b>中国信贷脉冲（右移 6 个月）vs 铜价同比</b><div id="cu-cCi" class="chart" style="height:340px"></div><div class="note">脉冲 = 社融 12 个月新增的同比变化 ÷ 名义 GDP（与本站世界页同算法）{S("ts", "wi")}；铜价同比用 FRED / LME 月均 {S("fred", "lme")}。2014–2020 拟合、2021 起检验：样本外 r = {CI["r_out"]:.2f}，方向命中 {CI["sign_out"]*100:.0f}%（{CI["n_out"]} 个月），误差 ±{CI["rmse"]:.0f}pp——方向有用，幅度只能参考。</div></div>
<div class="card"><b>LME 库存天数 vs 实际价格（2008–2026）</b><div id="cu-cInv" class="chart" style="height:340px"></div><div class="note">库存天数 = LME 库存 ÷ ICSG 年度消费 / 365 {S("lme", "icsg", "fb20", "fb22", "icsgt1")}。蓝 = 2008–2018（拟合），红 = 2019 起（检验）。散点没有形状：库存在 LME、COMEX、上期所、国储之间搬来搬去，单看一个交易所的库存定不了价。</div></div></div>
<div class="grid g2" style="margin-top:12px"><div class="card"><b>COMEX 相对 LME 溢价（%，月末）</b><div id="cu-cSpr" class="chart" style="height:300px"></div><div class="note">Yahoo HG 近月 vs LME 现货月末 {S("yh", "lme")}；合约月份不同，只看趋势。2025 年关税预期时最高 +14%，公告豁免精铜后归零。</div></div>
<div class="card"><b>实际利率 vs 实际铜价</b><div id="cu-cMac" class="chart" style="height:300px"></div><div class="note">10 年 TIPS（右轴，反向）{S("fred")}；2022 年起两者背离：利率上去了，铜价没下来——供给和位置在定价，不是利率。</div></div></div>
<div class="tbl" style="margin-top:12px"><table class="stack"><thead><tr><th>回测</th><th>样本</th><th>结果</th><th>怎么用</th></tr></thead><tbody>
<tr><td><b>库存天数 → 实际价格（对数回归）</b></td><td>{O["FIT"]["train"]} 拟合，{O["FIT"]["test"]} 检验</td><td>样本内 R² {O["FIT"]["r2_in"]:.2f}，样本外 R² {O["FIT"]["r2_out"]:.2f}</td><td>不用来定价；只看"美国以外"库存的方向</td></tr>
<tr><td><b>库存 3 个月变化 → 未来 3 个月价格方向</b></td><td>{O["HIT"]["n"]} 个月</td><td>命中 {O["HIT"]["all"]*100:.0f}%（2019 起 {O["HIT"]["test"]*100:.0f}%），"一直猜涨" {O["HIT"]["base_up"]*100:.0f}%</td><td>没有优势</td></tr>
<tr><td><b>实际价格 z 分数（滚动 10 年）&gt; 1.5 → 未来 12 个月</b></td><td>1992–2026，{O["Z"]["1.5"]["n"]} 个月触发</td><td>下跌概率 {O["Z"]["1.5"]["down"]*100:.0f}%（无条件 {O["Z"]["all_down"]*100:.0f}%）；现在 z = {O["Z"]["now"]}</td><td>"贵"不是卖出理由</td></tr>
<tr><td><b>信贷脉冲领先 {O["KBEST"]} 个月 → 铜价同比</b></td><td>{CI["n"]} 个月；2021 起样本外 {CI["n_out"]} 个月</td><td>样本外 r = {CI["r_out"]:.2f}，方向 {CI["sign_out"]*100:.0f}%，±{CI["rmse"]:.0f}pp</td><td>2027-03 同比约 {format(CI['pred'], '+.1f').replace('-', '−')}% → 约 {f(O["CI_PX"])} 美元（一个锚）</td></tr></tbody></table></div>
<div class="grid g3" id="cu-lead" style="margin-top:14px"></div>'''),
  dict(id='ledger', h='预测台账放在结论层', ctx='台账在结论层「预测台账」↑', body='<p>C 系列（价格与平衡）、M 系列（约束迁移）和 N 系列（中国账本）都在 <a href="#pred">结论层 · 预测台账</a>；每条判断的反方证据和证伪阈值在 <a href="#wrong">可能错在哪</a>。规则：到期按公开数据打分，不改原文，只追加结果；作废要写原因并保留原文。</p>'),
  dict(id='map',
   cn=dict(h='A 股：按环节，标明证据强度', body=f'''<p class="sub">"强"= 公司公告；"中"= 媒体转述；"弱"= 只有行业层面数据。只列事实，不构成投资建议。</p>
<div class="tbl"><table id="cu-cnCoT" class="stack"><thead><tr><th>环节</th><th>公司</th><th>代码</th><th>与铜的关系</th><th>证据强度</th><th>来源</th></tr></thead><tbody></tbody></table></div>
<div class="card" style="margin-top:12px"><div id="cu-cnCo" class="chart" style="height:280px"></div></div>'''),
   h='环节 → 公司 → 库存；和 CoWoS / PCB 页对账', sub='点节点看详情；实线边都附来源编号（绿 = 供货，橙 = 合同，紫 = 库存流向）。虚线只表示公司在这个环节有业务。', body=f'''<div class="seg" id="cu-fMk"><button class="on" data-m="all">全部</button><button data-m="A">中国</button><button data-m="X">海外</button></div>
<div class="grid" style="margin-top:12px"><div class="card" style="padding:6px"><div id="cu-cNet" class="chart" style="height:560px"></div><div style="display:flex;justify-content:flex-end;padding:4px 6px"><button class="btn" onclick="cuNet()">重置视图</button></div></div>
<div class="card" id="cu-nodeInfo"><b>点击图中任一节点</b><div class="note">显示代码、角色与关联边及来源。</div></div></div>
<h3>公司清单</h3><div class="tbl"><table id="cu-coT"><thead><tr><th>公司</th><th>代码</th><th>环节</th><th>角色 / 数据</th></tr></thead><tbody></tbody></table></div>
<div id="iface"><h3>对外接口：和 CoWoS、PCB 用同一个分母</h3>
<p class="sub">铜不是 AI 加速器的约束（数据中心只占全球精铜消费约 {R["share_dc"]*100:.0f}%），但 AI 是铜需求里增长最快的一项。下表把 CoWoS 页的加速器颗数换成铜。</p>
<div class="tbl"><table><thead><tr><th>输出</th><th>2026</th><th>2027</th><th>说明</th></tr></thead><tbody id="cu-ifT"></tbody></table></div>
<p class="card" style="margin-top:12px"><b>公式</b><br><span id="cu-formula"></span></p>
<p class="note">宏观接口：实际利率、美元、铜金比、中国信贷脉冲见本站<a href="world/">世界仪表盘</a> {S("wi")}。大宗系列后续（铝、锂、铀、油气、电力）沿用本页结构：平衡（实物单位）→ 位置 → 成本曲线 → 情景 × 概率 → 回测。</p></div>'''),
 ],
 src_small='均于 2026-10-20/21 打开 · 局限',
 src='''<p class="sub">均于 2026-10-20/21 用 curl、浏览器或搜索核对（标"转述 / 二手 / 只看到摘要"的除外）。投行数据多为媒体转述，标在标题里。</p><ol class="src" id="cu-srcL"></ol>
<h3>局限（公开数据补不了的）</h3><ul style="font-size:14px" id="cu-lim"></ul>''',
 log='''<div class="tbl"><table id="cu-logT"><tbody></tbody></table></div>
<p><a href="cu/cu_model.xlsx">下载模型 Excel</a> · <a href="cu/cu_chain.md">报告原文 (Markdown)</a> · <a href="SOP.md">小链研究 SOP</a> · 构建：<code>./build.sh</code>（页面 <code>tpl/page.py</code> + <code>cu/page.py</code>，模型 <code>cu/model.py</code>，回测 <code>cu/backtest.py</code> 需联网单独跑）</p>''',
)
