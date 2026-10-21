"""铜 v0.1 构建：模型（cu/model.py）+ 回测（cu_data/backtest.json，由 cu/backtest.py 联网生成）+ 手写研究内容
→ data/cu.json、cu_data/model_out.json、cu/cu_model.xlsx、cu/cu_chain.md。重跑结果相同。"""
import json, os, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R0, 'cu'))
import model as M
from src import SRC, ID, n, s
_P = lambda *a: os.path.join(R0, *a)
BT = json.load(open(_P('cu_data', 'backtest.json')))
PCB = json.load(open(_P('data', 'pcb.json')))

R = M.calc()
SC, EV = M.scen()
B = {k: round(v) for k, v in M.BANDS.items() if not isinstance(v, tuple)}
B.update({k: [round(v[0]), round(v[1])] for k, v in M.BANDS.items() if isinstance(v, tuple)})

# ---------------- 价格：月度 → 季度实际值；2026 年均价（11–12 月按 14,500 假设，估）
ser = BT['series']
mon = {x[0]: x[1] for x in ser}
Q = {}
for m_, v in mon.items():
    y, mm = m_.split('-'); q = f"{y}Q{(int(mm) - 1) // 3 + 1}"
    if y >= '2024': Q.setdefault(q, []).append(v)
QA = [[q, round(sum(v) / len(v)), len(v)] for q, v in sorted(Q.items())]
y26 = [mon[f'2026-{i:02d}'] for i in range(1, 11)]
AVG26 = round((sum(y26) + 2 * 14500) / 12)
YTD26 = round(sum(y26) / len(y26))
NOW = BT['now']
# 美国以外可见库存（LME + SHFE + 保税，10 月中旬）
VIS = dict(lme=233.8, shfe=74.0, bond=31.2)
VIS['tot'] = round(sum(VIS.values()), 1)
VIS['days'] = round(VIS['tot'] / (R['use27'] / 365), 1)

# ---------------- TOC（单位：千吨铜/年；满足率 = 能给出的 ÷ 想要的）
TOC = {
 2026: dict(conc=M.ICSG['ref'][2026] / M.ICSG['ref_u'][2026], ref=M.ICSG['ref'][2026] / M.ICSG['use'][2026], exus=(M.ICSG['use'][2026] + R['exus'][2026]) / M.ICSG['use'][2026]),
 2027: dict(conc=R['ref27'] / M.ICSG['ref_u'][2027], conc_icsg=M.ICSG['ref'][2027] / M.ICSG['ref_u'][2027], ref=R['ref27'] / R['use27'], exus=(R['use27'] + R['exus'][2027]) / R['use27']),
}

OUT = dict(R={k: (round(v, 3) if isinstance(v, float) else v) for k, v in R.items() if k not in ('gbal', 'exus')}, gbal={str(k): round(v) for k, v in R['gbal'].items()},
           exus={str(k): round(v) for k, v in R['exus'].items()}, SC=[{**x, 'avg': round(x['avg']), 'gbal': round(x['gbal']), 'exus': round(x['exus']), 'dc27': round(x['dc27']), 'ug': round(x['ug'], 2)} for x in SC],
           EV=round(EV), B=B, AVG26=AVG26, YTD26=YTD26, QA=QA, NOW=NOW, VIS=VIS, TOC={str(y): {k: round(v, 4) for k, v in d.items()} for y, d in TOC.items()},
           CI=BT['ci'], Z=BT['z'], FIT=BT['fit'], HIT=BT['hit'], XC=BT['xc'], KBEST=BT['kbest'], IMP=BT['imp_last'],
           CI_PX=round(BT['ci']['base_px'] * (1 + BT['ci']['pred'] / 100)), CI_LO=round(BT['ci']['base_px'] * (1 + (BT['ci']['pred'] - BT['ci']['rmse']) / 100)),
           CI_HI=round(BT['ci']['base_px'] * (1 + (BT['ci']['pred'] + BT['ci']['rmse']) / 100)), A=M.A, KW26=round(M.KW26, 3), PCBKG=PCB['model']['CUKG'])

# ---------------- 一致预期（2027 年均价，美元/吨）
CONS = [['高盛', 15400, '2027 年均价；美国以外缺口 220 千吨；其中废铜替代 +2,985、持仓 +775', n('gs')],
        ['瑞银（路径）', 15500, '2027-06 目标（点位，不是年均）', n('icaa')],
        ['BMO', 14675, '2027 年；之后小幅缺口，2028 年 16,000', n('mcom')],
        ['远期曲线', 14405, '高盛报告引用的 2027 远期', n('gs')],
        ['花旗（12 个月）', 14500, '12 个月目标；牛市情景 2027 年 17,000', n('citi')],
        ['摩根大通', 13800, '2027 年均价', n('jpm')],
        ['BMI', 12900, '2027 年；2027 起缺口', n('mcom')],
        ['麦格理', 12750, '2027 年；周期低点 2027Q4 12,000；2027 起年过剩 >700 千吨', n('mcom')],
        ['Cochilco', round(5.10 * M.LB), '5.10 美元/磅', n('cochilco')]]
# 机构 2027 平衡口径对照（千吨；只列有数字的）
BALV = [['ICSG（全球，中国表观口径）', 368, n('icsg')], ['麦格理（全球）', '>700', n('mcom')], ['BMO（全球）', '小幅缺口', n('mcom')], ['BMI（全球）', '缺口', n('mcom')],
        ['高盛（美国以外）', -220, n('gs')], ['我们（全球，基准）', round(R['gbal'][2027]), '估'], ['我们（美国以外，基准）', round(R['exus'][2027]), '估']]

# ---------------- 要害变量的龙卷风（指标：2027 美国以外平衡，千吨）
TOR = [['美国 2027 净囤货', dict(us27=-500), dict(us27=1000), '回流 500', '再囤 1,000', '高盛基准 +400；麦格理"明确不征"情景回流'],
       ['矿山相对 ICSG', dict(mine27=0), dict(mine27=-600), '按 ICSG', '−600', 'ICSG 已含 959 千吨干扰扣减；Escondida FY27 指引 −13%～−21%'],
       ['每颗加速器 kW', dict(kw27=1.2), dict(kw27=2.0), '1.2 kW', '2.0 kW', 'SemiAnalysis 51.2 GW ÷ KGI ≈ 2.0'],
       ['数据中心吨/MW', dict(tpm=20), dict(tpm=45), '20', '45', 'Kpler：27（微软芝加哥）、AI 高密度 30–45'],
       ['非数据中心需求增速', dict(g27=-1.0), dict(g27=1.5), '−1%', '+1.5%', '麦格理：中国 0、全球 +1.5%'],
       ['中国废铜→精铜替代', dict(scrap27=0), dict(scrap27=400), '0', '+400', '高盛只给了价格影响，没有吨数（估）'],
       ['中国国储/补库', dict(cn27=0), dict(cn27=300), '0', '+300', '协会呼吁扩储，未见落地']]
TORD = []
for nme, lo, hi, l1, l2, src in TOR:
    TORD.append(dict(n=nme, lo=round(M.calc(lo)['exus'][2027]), hi=round(M.calc(hi)['exus'][2027]), l1=l1, l2=l2, src=src))

DEBATES = [
 dict(q='2027 年铜是过剩还是短缺？', view=f'全球精铜小过剩（我们约 +{R["gbal"][2027]:.0f} 千吨，ICSG +368）{s("icsg")}，但美国以外小缺口（约 {R["exus"][2027]:.0f} 千吨）——价格跟后者走 [估]',
      falsify='美国以外可见库存（LME + 上期所 + 保税）在关税仍未决定时升破 50 万吨'),
 dict(q='AI 数据中心能不能撑起铜的新周期？', view=f'2027 年数据中心用铜增量约 +{R["ddc"]:.0f} 千吨，相当于 ICSG 全年消费增量的约 {R["ddc"]/(M.ICSG["use"][2027]-M.ICSG["use"][2026])*100:.0f}%；但中国地产、空调、汽车在负增长，AI 是补洞不是造周期 [估]',
      falsify='中国 2027 年表观消费增速 > 3%，或 ICSG 把 2027 年消费增速上修到 3.5% 以上'),
 dict(q='关税悬而未决，价格会不会"崩"？', view='明确不征是麦格理排的最不可能情景；我们的基准是悬而未决、美国库存原地不动，熊市概率 30% [估]',
      falsify='2027-01-01 前宣布 15% 精铜关税（切到牛市情景），或明确不征（切到熊市情景）'),
]
DEBATES = [{k: v.replace('[估]', '<span class="tag t-est">估</span>') for k, v in d.items()} for d in DEBATES]

PROCESS = [
 ['矿山 → 精矿', f'全球矿产 23.18 百万吨（2025），ICSG 预计 2027 年 24.22（调整后，含 959 千吨干扰扣减）；中国矿产只有 1.8 百万吨 {s("usgs")}', n('icsg', 'usgs')],
 ['冶炼 / 电解精炼（原生）', '按冶炼产能，2027 年精炼可以做到 31.01 百万吨；按精矿只能做到 29.67——差的 1.34 百万吨就是"精矿约束"', n('icsg')],
 ['湿法（SX-EW）', '用硫酸浸出氧化矿；硫酸 2026 年创纪录 451 美元/吨，2027Q4 预计 215（CRU）——湿法矿成本跟着降', n('cru')],
 ['再生（废铜）', f'中国再生精铜 2.8 → 3.3 百万吨（BMO）{s("mcom")}；ICSG 预计 2027 年全球再生精铜 +4.7%；中国"反向开票"限额收紧废铜流通 {s("vat")}', n('icsg', 'mcom')],
 ['精铜库存与交割', f'LME 约 23.4 万吨、上期所 7.4 万吨、保税约 3.1 万吨 → 美国以外可见约 {VIS["tot"]:.0f} 千吨；COMEX 约 71.8 万吨，美国合计约 1.6–2 百万吨 {s("usst", "mcom")}', n('lme', 'shfe', 'bond', 'gsr')],
 ['铜材加工 → 终端', '中国占全球精铜消费 59%；终端：建筑、电网、家电、汽车、数据中心、国防', n('icsg')],
]
PRICE = [
 ['LME 现货（10-20）', f'{mon["2026-10"]:,} 美元/吨（10 月均价至今）；纪录 14,822（10-12）', n('lme', 'mcom')],
 ['COMEX 12 月 vs LME 三月', '约 +170 美元/吨 ≈ 市场给 15% 关税约 8% 概率', n('mcom')],
 ['上期所主力（10-20）', '109,270 元/吨', n('gsr')],
 ['洋山溢价', '137 美元/吨（10-19）', n('gsr')],
 ['欧洲 2027 年升水', 'Aurubis 347 美元/吨（+10%）', n('mcom')],
 ['精矿加工费 TC', '长单 2026 年 0；现货 −272（10-09，Fastmarkets）；2027 年 Los Pelambres 约 −330', n('tc0', 'fm', 'anto')],
 ['铜相对铝溢价', '9 月纪录 5.08 美元/磅；国内铜铝比 4.41（6 月）', n('mcom', 'alsub')],
]
MINES = [
 ['Grasberg（印尼）', '选厂 14 万吨/日 = 事故前 67%', '阴极铜 8 亿磅（约 363 千吨）', '12 亿磅（约 544 千吨）；2027 年中 80%，年底接近满产', '+181', n('fcx', 'ptfi')],
 ['Kamoa-Kakula（刚果金）', '三季度 76,401 吨，2026 年趋向 290 千吨下沿', '290–310 千吨', '380–420 千吨（指引不变）；2028 年起约 500', '+90～+110', n('ivn', 'ivn2')],
 ['智利（全国）', '财长：2026 年 −7%；Cochilco：−2.6%', '5.27 百万吨（Cochilco）', '5.55 百万吨（+5.2%，Cochilco）；财长说只部分恢复', '+280（Cochilco）', n('cochilco', 'quiroz')],
 ['Escondida（智利，在上一行内）', '三季度 252.6 千吨（−23%），9-23 事故后暂停采矿', 'FY26 约 1.26 百万吨', 'FY27 指引 1.0–1.1 百万吨，品位约 0.70%', '−160～−260', n('bhp')],
 ['Cobre Panamá', '只处理堆存矿；总统未授权谈判', '堆存矿处理', '麦格理假设 2027 年中全面复产；我们假设 2027 年不复产', '我们 0', n('panama', 'mcom', 'icsg')],
]
CNSUP = [
 ['精炼铜产量', '1–9 月 1,041.55 万吨（+3.54%）；9 月 112.06 万吨；10 月预计 108.47 万吨（年内最低）', n('smm')],
 ['冶炼利润', '现货精矿冶炼月均亏损 4,129 元/吨（9 月），10 月或到 5,000 元/吨', n('smm')],
 ['新增产能', '9、10 月各有一家 30 万吨冶炼厂投产（爬坡中）——亏损时还在扩', n('smm')],
 ['精矿进口', '9 月 248.2 万吨（−4.06%），1–9 月 2,197.4 万吨', n('cnconc')],
 ['自给率', f'矿产 1.8 百万吨 vs 精炼 14.0 百万吨（2025）→ 精矿自给约 {1.8/14*100:.0f}%（含再生原料，粗算）', n('usgs')],
 ['海外权益矿', '紫金 2026 年矿产铜 120 万吨 → 2028 年 150–160 万吨；洛阳钼业 2026 年 76–82 万吨（上半年 38.8 万吨）', n('zijin', 'cmoc', 'cmoc2')],
]
CNDEM = [
 ['房地产开发投资', -20.6, '1–9 月', n('nbs')],
 ['固投（扣除房地产）', -4.2, '1–9 月', n('nbs')],
 ['全国电网工程投资', 4.0, '上半年', n('grid')],
 ['国家电网固定资产投资', 12.6, '上半年', n('sgcc')],
 ['新能源乘用车零售', -12.8, '1–9 月', n('nev')],
 ['家用空调内销', -23.7, '9 月', n('ac')],
 ['家用空调出口', 8.0, '9 月', n('ac')],
]
CNBAL = [
 ['精炼铜进口', '9 月 311.6 千吨（同比 −16.7%）', n('cnim')],
 ['精炼铜出口', '9 月 47.9 千吨（同比 +81%）', n('cnim')],
 ['净贸易累计摆动', '关税交易开始以来约 1.6 百万吨（BMO 估，读作国储被动用）', n('mcom')],
 ['上期所库存', '73,962 吨（10-16）', n('shfe')],
 ['保税区库存', '约 3.1 万吨（10-15）', n('bond')],
 ['洋山溢价', '137 美元/吨（10-19）：进口需求偏弱', n('gsr')],
 ['国储', '有色协会 2 月呼吁扩储、把精矿纳入；未见落地', n('srb')],
]
NECK = [
 dict(name='精矿（矿山）', verdict='约束', now=f'精矿只够冶炼想要的 {TOC[2027]["conc"]*100:.1f}%（2027，我们）；现货 TC −272', src=n('icsg', 'fm'), months=36),
 dict(name='美国以外库存（位置）', verdict='最紧的快变量', now=f'LME + 上期所 + 保税约 {VIS["tot"]:.0f} 千吨 ≈ {VIS["days"]} 天全球消费', src=n('lme', 'shfe', 'bond'), months=9),
 dict(name='中国废铜（政策）', verdict='政策约束', now='反向开票限额 → 废铜替代成精铜需求（高盛 +2,985 美元）', src=n('vat', 'gs'), months=12),
 dict(name='冶炼产能', verdict='不缺', now='亏损 4,129 元/吨还在投新厂；产能想做 31.0 百万吨 vs 精矿只够 29.7', src=n('smm', 'icsg'), months=1),
]
PLAYERS = [
 dict(who='美国政府（Section 232）', role='定开关', incentive='既想扶持本土冶炼，又怕制造业成本上升（"可负担性"）[源' + n('stall') + ']', now='半成品已征 50%，精铜 15%/30% 的分阶段方案搁置未决 ' + s('p232', 'stall'),
      history='2025-07 宣布时精铜意外豁免，COMEX 溢价当月从高位归零（本页回测：2025-03 溢价 +14.4% → 2025-07 −0.6%）', signal='中期选举（11-03）后的公告；商务部更新报告；COMEX 12 月合约相对 LME 升水 > 800 美元'),
 dict(who='中国冶炼厂（CSPT）', role='精矿买方', incentive='保开工、保市场份额，硫酸收入一度对冲负 TC', now='现货亏损 4,129 元/吨，仍有新厂投产；联合减产没见落实 ' + s('smm'),
      history='TC 长单从 2015 年 107 美元一路降到 2026 年 0 ' + s('tch', 'tc0'), signal='SMM 月产量连续两月 < 105 万吨 = 真减产；2027 年长单谈判（可能谈不成 ' + s('dd') + '）'),
 dict(who='中国国储 / 有色协会', role='最大的隐形库存', incentive='高价时放、低价时收；把精矿纳入储备以保原料', now='2 月协会呼吁扩储，未见收储；BMO 读出 1.6 百万吨净贸易摆动 = 储备被动用 ' + s('srb', 'mcom'),
      history='ICSG 明确：中国表观消费不含国储变化，收放储会"显著改变"全球平衡 ' + s('icsg'), signal='精铜进口月度 > 40 万吨、洋山溢价 > 150 美元、官方收储公告'),
 dict(who='Freeport（Grasberg）', role='最大单矿变量', incentive='尽快恢复并把精矿送进自家 Manyar 冶炼厂', now='选厂 67%，2027 年中 80%、年底接近满产 ' + s('fcx'),
      history='5 月曾因湿矿拖慢恢复，但坚持 2027 年时间表 ' + s('ptfi'), signal='季度报告里选厂吨/日；PB1S 2027 年中能否复产'),
 dict(who='智利（Codelco / BHP / 政府）', role='第一产铜国', incentive='保产量、保税收', now='财长：2026 年 −7%；Escondida 9 月事故后暂停、FY27 指引 1.0–1.1 百万吨；El Teniente 露天坑塌方 ' + s('quiroz', 'bhp', 'mcom'),
      history='Cochilco 每年都预期"明年恢复"：2026 年 −2.6%、2027 年 +5.2% ' + s('cochilco'), signal='Cochilco 月度产量同比转正；Escondida 季度产量 > 300 千吨'),
 dict(who='巴拿马政府 / First Quantum', role='最大的"开关矿"', incentive='政府要财政和有序关闭，公司要仲裁和复产', now='委员会建议评估"为有序关闭而重启"，总统未授权谈判 ' + s('panama'),
      history='麦格理把它算进 2027 年中全面复产 ' + s('mcom'), signal='总统授权谈判、签协议、复产时间表'),
 dict(who='投机资金', role='放大器', incentive='AI、电气化、能源安全叙事 + 硬资产', now='COMEX 管理基金净多 61,058 手（10-13）；LME 投资基金净多 33,600 手（周减 7,075）' + s('cftc', 'lmecot'),
      history='高盛：持仓若维持在持仓量 16%，给 2027 年均价 +775 美元 ' + s('gs'), signal='净多连续 4 周下降 + 价格跌破 13,500'),
 dict(who='云厂商（AI 资本开支）', role='新增需求', incentive='抢算力', now=f'2027 年 KGI 加速器 25.75 百万颗 {s("kgi")}；SemiAnalysis 2027 年新增 51.2 GW {s("semi")}',
      history='SemiAnalysis 提示 2028 年约 10 GW 过剩风险 ' + s('semi2'), signal='云厂商 2027 年资本开支指引；CoWoS 页的出货表'),
]
CNPLAYERS = [
 dict(who='国家物资储备（国储）', role='开关', incentive='保供与平抑', now='未见收储公告；协会建议把精矿纳入 ' + s('srb'), history='ICSG 不把国储变化算进中国表观消费 ' + s('icsg'), signal='收储公告、精铜进口跳升'),
 dict(who='冶炼厂（江铜、铜陵、云铜等，CSPT 成员）', role='全球一半精炼', incentive='保开工', now='亏损仍投产 ' + s('smm'), history='TC 十年降到 0 ' + s('tch', 'tc0'), signal='SMM 月产量 < 105 万吨'),
 dict(who='紫金 / 洛阳钼业（海外权益矿）', role='对冲精矿依赖', incentive='量增', now='紫金 2026 年 120 万吨、洛钼 76–82 万吨 ' + s('zijin', 'cmoc'), history='紫金规划 2028 年 150–160 万吨 ' + s('zijin'), signal='季度产量对指引的完成度'),
 dict(who='税务部门（废铜票据）', role='废铜供给', incentive='打击虚开发票', now='反向开票单人 12 个月 500 万元上限 ' + s('vat'), history='高盛：废铜不足迫使下游改用精铜 ' + s('gs'), signal='政策放宽 → 废铜回流、精铜需求回落'),
]
HIST = dict(rule='铜的约束在两个速度上来回迁移：慢变量是矿山（从发现到投产十几年，资本开支滞后），快变量是库存放在哪里（关税、国储、交割库）。2025–26 年两者叠加，所以价格和"全球过剩"同时出现。',
 tl1=[['2008', 'LME 铜价随金融危机暴跌，2009 年起中国刺激带动反弹', n('lme')],
      ['2011-02', f'实际价格（2026 年美元）此前高点约 {BT["z"]["peak_prior"][1]:,}（本页按 FRED 与 CPI 计算）', n('fred')],
      ['2015–2016', 'TC 长单 107 → 97.35 美元，冶炼宽松，铜价低迷', n('tch')],
      ['2025-03', 'COMEX 相对 LME 溢价月末约 +14%（关税预期，本页计算）', n('yh', 'lme')],
      ['2025-07-30', 'Section 232：半成品 50%，精铜豁免；精铜 2027 年 15%、2028 年 30% 待定', n('p232')],
      ['2025', 'Grasberg、Kamoa-Kakula 事故；TC 长单 21.25 美元', n('icsg', 'tch')],
      ['2026', 'TC 长单 0；美国库存 1.6–2 百万吨；9-10 关税搁置报道，单日跌 >5%', n('tc0', 'usst', 'mcom')],
      ['2026-10-12', 'LME 现货纪录 14,822 美元', n('mcom')]],
 tl2=[['2015–2019', '冶炼产能过剩、精矿宽松：TC 80–107 美元', n('tch')], ['2020–2024', '矿山投资不足，TC 从 88 降到 80，新矿滞后', n('tch')],
      ['2025', '约束 = 精矿：大矿事故 + TC 跳水', n('icsg', 'tch')], ['2026', '约束 = 精矿 + 位置（美国隔离库存）', n('gs', 'mcom')],
      ['2027（判断）', '上半年仍是位置 + 精矿；下半年精矿松动（CRU：TC 回到 −75）', n('cru')], ['2028（方向）', '矿山增量（麦格理 +4.3%）+ 数据中心可能过剩 → 约束让位给需求', n('mcom', 'semi2')]])
LEAD = [
 ['中国信贷脉冲', '月度 · 领先 6 个月', 'Tushare 社融 + GDP', f'领先 {BT["kbest"]} 个月相关 {BT["xc"][str(BT["kbest"])]:.2f}；样本外 r = {BT["ci"]["r_out"]:.2f}，方向命中 {BT["ci"]["sign_out"]*100:.0f}%（基准 50%）。现在 −2.58% → 2027-03 铜价同比约 {BT["ci"]["pred"]:+.1f}%（±{BT["ci"]["rmse"]:.0f}pp）', n('ts', 'wi')],
 ['COMEX–LME 价差', '日度', 'CME / LME', '关税概率的实时读数：12 月合约 +170 美元 ≈ 8%；> 800 美元 = 最后一波进美国', n('mcom', 'yh')],
 ['美国以外可见库存', '日 / 周', 'LME、上期所、SMM 保税', f'现在约 {VIS["tot"]:.0f} 千吨；回测显示库存水平本身不能预测价格（R² {BT["fit"]["r2_in"]:.2f}），只当状态量用', n('lme', 'shfe', 'bond')],
 ['现货 TC', '周度', 'Fastmarkets / SMM', '−272 美元（10-09）；回到 −100 以上 = 精矿松动', n('fm', 'cru')],
 ['铜金比 · 实际利率', '日度', '本站世界仪表盘', '铜金比 9 分位、实际利率 99 分位：宏观在说"增长弱、钱贵"，铜价在说"缺货"——二者背离', n('wi')],
]
PRED = [
 dict(id='C1', text='2027 年 LME 现货年均价落在 12,800–14,700 美元/吨（基准情景区间）', due='2028-01-15', check='LME / Westmetall 年均价', status='pending'),
 dict(id='C2', text='2027 年下半年 LME 现货均价低于上半年（先紧后松）', due='2028-01-15', check='LME 月均价', status='pending'),
 dict(id='C3', text='2027-01-01 美国不会对精炼铜开征 15% 的 Section 232 关税', due='2027-01-05', check='白宫公告 / 联邦公报', status='pending'),
 dict(id='C4', text='2027 年 Cobre Panamá 不恢复商业化采矿（只处理堆存矿）', due='2028-01-31', check='First Quantum 季报', status='pending'),
 dict(id='C5', text='2027-06 现货精矿 TC 仍低于 −100 美元/吨', due='2027-07-10', check='Fastmarkets / SMM 现货 TC', status='pending'),
 dict(id='C6', text='ICSG 2027 年平衡的初值（2028 年 4 月会议）低于 +368 千吨', due='2028-05-15', check='ICSG 新闻稿', status='pending'),
 dict(id='C7', text='2028 年 LME 年均价低于 2027 年（方向判断）', due='2029-01-15', check='LME 年均价', status='pending'),
 dict(id='M1', text='约束迁移：2027-12 现货 TC 回到 −150 美元以上（精矿开始松动）', due='2028-01-10', check='Fastmarkets / SMM', status='pending'),
 dict(id='M2', text='Grasberg 2027 年二季度选厂达到事故前的 75% 以上', due='2027-08-15', check='Freeport 二季报', status='pending'),
]
CNPRED = [
 dict(id='N1', text='2027 年中国电解铜产量增速 ≤ 2%（2026 年 1–9 月 +3.54%）', due='2028-01-31', check='SMM / 统计局年度产量', status='pending'),
 dict(id='N2', text='2026 年中国精炼铜进口量低于 2025 年', due='2027-01-31', check='海关总署', status='pending'),
 dict(id='N3', text='2027-06-30 前没有官方公布的国储精铜收储', due='2027-07-01', check='国家粮食和物资储备局 / 主流媒体', status='pending'),
 dict(id='N4', text='紫金矿业 2027 年矿产铜 ≥ 120 万吨', due='2028-04-30', check='紫金年报', status='pending'),
]
FALS = [
 dict(j='J1 价格跟美国以外走（↔①）', counter=f'ICSG 全球过剩 +368 千吨 {s("icsg")}；现货 COMEX 套利已消失 {s("mcom")}', falsify='关税仍未决定时，美国以外可见库存升破 50 万吨且价格不跌', ind='LME + 上期所 + 保税（周）', th='> 500 千吨', now=f'约 {VIS["tot"]:.0f} 千吨 {s("lme", "shfe", "bond")}', st='ok'),
 dict(j='J2 AI 补洞不造周期（↔②）', counter=f'S&P：2040 年需求 42 百万吨 {s("spg")}；SemiAnalysis 2027 年 +51.2 GW {s("semi")}', falsify='中国 2027 年表观消费 > +3%，或 ICSG 2027 消费增速上修 > 3.5%', ind='ICSG 4 月会议；SMM 中国表观消费', th='> 3% / > 3.5%', now=f'ICSG +2.5% {s("icsg")}', st='ok'),
 dict(j='J3 约束在精矿（↔③）', counter=f'CRU：TC 2027Q4 回到 −75 {s("cru")}', falsify='2027-06 前现货 TC 回到 0 以上，而没有大规模冶炼减产', ind='Fastmarkets 现货 TC', th='> 0 美元', now=f'−272（10-09）{s("fm")}', st='ok'),
 dict(j='J4 2027 先紧后松，基准 13,700（↔④）', counter=f'高盛 15,400、BMO 14,675 {s("gs", "mcom")}', falsify='2027Q4 均价比 2027Q1 高 5% 以上；或精铜关税宣布（改用牛市情景）', ind='LME 季度均价；白宫公告', th='Q4 ÷ Q1 > 1.05', now='—', st='watch'),
 dict(j='J5 熊市不是主情景', counter=f'麦格理：明确不征 → COMEX 崩、带着 LME 一起跌 {s("mcom")}', falsify='白宫明确不征或推迟 ≥ 6 个月', ind='COMEX–LME 价差', th='连续 1 个月 < 0', now=f'12 月合约约 +170 美元 {s("mcom")}', st='watch'),
]
CNFALS = [
 dict(j='CJ1 中国在高价下让出金属（↔❶）', counter=f'德银：中国几十年一直在加储备 {s("mcom")}', falsify='2026Q4 任一月精铜进口 > 40 万吨且洋山溢价 > 150 美元', ind='海关 + 洋山溢价', th='> 400 千吨 / > 150 美元', now=f'311.6 千吨 / 137 美元 {s("cnim", "gsr")}', st='ok'),
 dict(j='CJ2 冶炼减产会落地（↔❷）', counter=f'9、10 月仍有 2 家 30 万吨新厂投产 {s("smm")}', falsify='2027 年上半年 SMM 月产量都 > 115 万吨', ind='SMM 月度电解铜产量', th='> 1,150 千吨/月', now=f'9 月 1,120.6、10 月预计 1,084.7 {s("smm")}', st='watch'),
 dict(j='CJ3 收储是 2027 最大的中国开关（↔❸）', counter='没有官方收储信息，可能根本不发生', falsify='2027 年全年无收储且精铜进口继续下降 → 这个开关不重要', ind='收储公告；进口', th='—', now=f'协会呼吁，未落地 {s("srb")}', st='watch'),
]
SEG = ['矿山', '冶炼/精炼', '库存与定价', '需求']
CO = dict(seg=SEG, co=[
 ['Freeport', 'FCX', 'X', 0, f'Grasberg 选厂事故前的 67%；PTFI 阴极铜 2026 年 8 亿磅 → 2027 年 12 亿磅 {s("fcx", "ptfi")}', 30],
 ['BHP', 'BHP', 'X', 0, f'季度铜 400.7 千吨（−19%）；Escondida FY27 1.0–1.1 百万吨 {s("bhp")}', 30],
 ['Codelco', '国企', 'X', 0, f'El Teniente 露天坑塌方后停产 {s("mcom")}', 24],
 ['Antofagasta', 'ANTO', 'X', 0, f'2026 年长单 TC 0；2027 年 Los Pelambres 约 −330 {s("tc0", "anto")}', 22],
 ['Ivanhoe', 'IVN', 'X', 0, f'Kamoa-Kakula 2027 年 380–420 千吨 {s("ivn2")}', 22],
 ['First Quantum', 'FM', 'X', 0, f'Cobre Panamá 停产，只处理堆存矿 {s("panama")}', 20],
 ['Southern Copper', 'SCCO', 'X', 0, f'2026 年股价 +44.1%，市值 1,690 亿美元 {s("mcom")}', 18],
 ['紫金矿业', '601899', 'A', 0, f'2026 年矿产铜 120 万吨，2028 年 150–160 万吨 {s("zijin")}', 26],
 ['洛阳钼业', '603993', 'A', 0, f'2026 年铜 76–82 万吨，上半年 38.8 万吨 {s("cmoc", "cmoc2")}', 22],
 ['中国冶炼厂（CSPT）', 'CSPT', 'A', 1, f'全球约一半精炼；现货亏损 4,129 元/吨 {s("smm", "usgs")}', 28],
 ['Aurubis', 'NDA', 'X', 1, f'2027 年欧洲升水 347 美元 {s("mcom")}', 18],
 ['PTFI Manyar 冶炼厂', 'FCX·Manyar', 'X', 1, f'2026-09 复产阴极铜 {s("ptfi")}', 16],
 ['LME', '—', 'X', 2, f'库存约 23.4 万吨（10-20）{s("lme")}', 22],
 ['COMEX', '—', 'X', 2, f'库存约 71.8 万吨（10-19）{s("gsr")}', 26],
 ['上期所', '—', 'A', 2, f'库存 73,962 吨（10-16）{s("shfe")}', 20],
 ['国家电网', '—', 'A', 3, f'上半年投资 +12.6% {s("sgcc")}', 20],
 ['云厂商', '—', 'X', 3, f'2027 年 25.75 百万颗加速器（KGI）{s("kgi")}', 22],
], links=[
 ['Antofagasta', '中国冶炼厂（CSPT）', '2026 年长单 TC 0', n('tc0'), 'ord'],
 ['Freeport', 'PTFI Manyar 冶炼厂', '精矿供给自家冶炼厂', n('ptfi'), 'sup'],
 ['Aurubis', 'LME', '"大量金属搬到美国，仓库很空"', n('mcom'), 'cap'],
 ['LME', 'COMEX', '美国囤货：库存从 LME 流向 COMEX', n('gs', 'mcom'), 'cap'],
])
CNCO = [
 ['矿山（海外权益）', '紫金矿业', '601899', '2026 年矿产铜 120 万吨；Kamoa-Kakula 等海外项目', '强：公司公告', n('zijin')],
 ['矿山（海外权益）', '洛阳钼业', '603993', '2026 年铜 76–82 万吨（刚果金）', '中：媒体转述公司指引', n('cmoc', 'cmoc2')],
 ['冶炼', '江西铜业 / 铜陵有色 / 云南铜业等', '600362 / 000630 / 000878', '在全国冶炼亏损里；个体减产未见公告', '弱：只有行业层面数据', n('smm')],
]
IFACE = [
 ['AI 加速器（百万颗，KGI）', f'{M.A[2026]:.2f}', f'{M.A[2027]:.2f}', f'读 CoWoS 页 {s("kgi")}'],
 ['每颗数据中心 IT 功率（kW）', f'{M.KW26:.2f}', f'{M.P0["kw27"]:.2f}', 'SemiAnalysis GW ÷ KGI 颗数（2026）；2027 取 1.6（估）'],
 ['每颗加速器的机房用铜（kg）', f'{R["kg26"]:.0f}', f'{R["kg27"]:.0f}', 'kW × 吨/MW（27）（估）'],
 ['每颗加速器的 HVLP 铜箔（kg）', f'{PCB["model"]["CUKG"]["2026"]}', f'{PCB["model"]["CUKG"]["2027"]}', f'PCB 页 {s("pcb")}'],
 ['数据中心用铜（千吨）', f'{R["dc26"]:.0f}', f'{R["dc27"]:.0f}', '颗数 × kW × 吨/MW（估）'],
 ['占全球精铜消费', f'{R["dc26"]/M.ICSG["use"][2026]*100:.1f}%', f'{R["share_dc"]*100:.1f}%', '分母：ICSG 2026 / 我们 2027'],
]
FORMULA = '数据中心用铜（千吨）= KGI 加速器（百万颗）× 每颗 IT 功率（kW）× 吨/MW；全球平衡 = ICSG 精炼 + 矿山修正 − [（ICSG 2026 消费 − 2026 数据中心）×（1 + 增速）+ 2027 数据中心 + 废铜替代 + 中国补库]；美国以外 = 全球 − 美国净囤货。'
LIMITS = [
 'SemiAnalysis 的 GW 数字来自 alpharis 二手转述（原文付费）；Knight Frank 33 GW（两年）明显更低，kW/颗这一项误差最大。',
 '数据中心吨/MW 只有一个公开案例（微软芝加哥 2,177 吨 / 81 MW）；AI 高密度 30–45 吨/MW 是 Kpler 区间，不含电网。BNEF、S&P 的口径更宽，相差 2–3 倍。',
 'KGI 的 Rubin 颗数是按芯片还是按封装未确认，所以不做纯自下而上的 kW/颗，只用 GW ÷ 颗数交叉验证（估）。',
 '高盛报告只看到 SquawkNews / 路透转述；废铜替代给了价格影响，没给吨数——滑块里的吨数是我们的假设。',
 '花旗牛市 17,000 / 18,000 只见于 RoadShow 二手转述。',
 '上期所仓单（Tushare fut_wsr）2014 年中以前为 0、部分月份只有少数仓库，不能做长回测；COMEX 库存没有可下载的历史，回测只用 LME。',
 'COMEX–LME 价差用 Yahoo 近月月末收盘 vs LME 现货月末，合约月份不同，只看趋势。',
 '库存天数 → 价格的回测失败（样本内 R² 0.04，样本外为负），所以价格不由公式反推，用情景 + 概率（估）。',
 '中国国储、贸易商、保税以外的隐形库存没有公开数据；BMO 的 1.6 百万吨是推算。',
 '国内电网投资 +4%（能源局）与 Kpler 所说电网 +35–40% 冲突，取官方口径。',
]
CHANGELOG = [['2026-10-21', 'v0.1', '首版：大宗商品系列第一篇。ICSG 10 月预测 + 我们的矿山修正 + AI 数据中心（统一单位 = KGI 加速器）→ 全球 / 美国以外平衡；三情景 × 概率；库存-价格、估值、信贷脉冲三项回测。']]

J = dict(meta=dict(updated='2026-10-21', version='v0.1'),
         model=dict(ICSG={k: {str(a): b for a, b in v.items()} for k, v in M.ICSG.items()}, A={str(k): v for k, v in M.A.items()}, KW26=M.KW26, P0=M.P0, US26=M.US26, LBL=M.LBL, LB=M.LB,
                    SCEN=[dict(k=x['k'], n=x['n'], p=x['p'], px=x['px'], lo=x['lo'], hi=x['hi'], trig=x['trig'], a=x['a']) for x in M.SCEN], B=B),
         stats=[dict(n='—', l='2027 全球精铜平衡（我们，千吨）', tag='估', id='cu-sG'), dict(n='—', l='2027 美国以外平衡（我们，千吨）', tag='估', id='cu-sX'),
                dict(n='+368', l='2027 全球平衡（ICSG，千吨）', tag=n('icsg')), dict(n='−220', l='2027 美国以外（高盛，千吨）', tag=n('gs'))],
         debates=DEBATES, process=PROCESS, price=PRICE, mines=MINES, cons=CONS, balv=BALV, tor=TORD, neck=NECK, players=PLAYERS, history=HIST, lead=LEAD,
         qa=QA, avg26=AVG26, ytd26=YTD26, vis=VIS, toc=OUT['TOC'],
         bt=dict(series=[[x[0], x[1], x[2], x[3], x[4]] for x in BT['series']], long=BT['long'], imp=BT['imp'], yoy=BT['yoy'], spread=BT['spread'], macro=BT['macro'],
                 fit=BT['fit'], hit=BT['hit'], z=BT['z'], ci=BT['ci'], xc=BT['xc'], kbest=BT['kbest'], now=BT['now']),
         tc=[[2015, 107], [2016, 97.35], [2017, 92.5], [2018, 82.25], [2019, 80.8], [2020, 62], [2021, 59.5], [2022, 65], [2023, 88], [2024, 80], [2025, 21.25], [2026, 0]],
         predictions=PRED, falsify=FALS, companies=CO, interface=dict(rows=IFACE, formula=FORMULA), limits=LIMITS, changelog=CHANGELOG,
         cn=dict(sup=CNSUP, dem=CNDEM, bal=CNBAL, players=CNPLAYERS, co=CNCO, preds=CNPRED, falsify=CNFALS),
         sources=[dict(id=ID[k], t=t, u=u) for k, t, u in SRC])
os.makedirs(_P('cu_data'), exist_ok=True)
json.dump(J, open(_P('data', 'cu.json'), 'w'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
json.dump(OUT, open(_P('cu_data', 'model_out.json'), 'w'), ensure_ascii=False, indent=1, sort_keys=True, default=str)


def xlsx():
    try:
        from openpyxl import Workbook
    except ImportError:
        print('openpyxl 未安装，跳过 Excel'); return
    wb = Workbook(); ws = wb.active; ws.title = '说明'
    ws.append(['铜 v0.1（2026-10-21）。单位：千吨铜；价格：LME 现货美元/吨。公式与 cu/model.py、cu.js 一致；本表是导出值，改假设请用网页滑块或改 model.py。'])
    ws.append(['公开数据整理，不构成投资建议。'])
    w = wb.create_sheet('平衡'); w.append(['项目', '2025', '2026', '2027（我们，基准）', '说明'])
    w.append(['ICSG 矿山（调整后）', M.ICSG['mine'][2025], M.ICSG['mine'][2026], M.ICSG['mine'][2027], 'ICSG 2026-10'])
    w.append(['ICSG 精炼（调整后）', M.ICSG['ref'][2025], M.ICSG['ref'][2026], M.ICSG['ref'][2027], ''])
    w.append(['ICSG 精炼（未调整 = 冶炼想做的）', M.ICSG['ref_u'][2025], M.ICSG['ref_u'][2026], M.ICSG['ref_u'][2027], ''])
    w.append(['我们的精炼', None, M.ICSG['ref'][2026], round(R['ref27']), f'矿山修正 {M.P0["mine27"]}'])
    w.append(['ICSG 消费', M.ICSG['use'][2025], M.ICSG['use'][2026], M.ICSG['use'][2027], ''])
    w.append(['我们的消费', None, M.ICSG['use'][2026], round(R['use27']), f'数据中心 {R["dc27"]:.0f}，非数据中心 {R["trad27"]:.0f}'])
    w.append(['全球平衡', 419, 104, round(R['gbal'][2027]), ''])
    w.append(['美国净囤货', None, M.US26, M.P0['us27'], '高盛'])
    w.append(['美国以外平衡', None, round(R['exus'][2026]), round(R['exus'][2027]), ''])
    w = wb.create_sheet('情景'); w.append(['情景', '概率', 'Q1', 'Q2', 'Q3', 'Q4', '年均', '区间低', '区间高', '全球平衡', '美国以外', '触发'])
    for x in OUT['SC']: w.append([x['n'], x['p']] + x['px'] + [x['avg'], x['lo'], x['hi'], x['gbal'], x['exus'], x['trig']])
    w.append(['概率加权', None, None, None, None, None, OUT['EV']])
    w = wb.create_sheet('一致预期'); w.append(['机构', '2027（美元/吨）', '说明', '来源编号']); [w.append(r) for r in CONS]
    w = wb.create_sheet('龙卷风'); w.append(['变量', '低端 → 美国以外平衡', '高端 → 美国以外平衡', '低端', '高端', '依据']); [w.append([t['n'], t['lo'], t['hi'], t['l1'], t['l2'], t['src']]) for t in TORD]
    w = wb.create_sheet('回测'); w.append(['月', 'LME 现货', '实际价格（2026-09 美元）', 'LME 库存（吨）', '库存天数']); [w.append(r[:5]) for r in BT['series']]
    w = wb.create_sheet('回测统计'); [w.append([k, json.dumps(v, ensure_ascii=False)]) for k, v in [('fit', BT['fit']), ('hit', BT['hit']), ('z', BT['z']), ('ci', BT['ci']), ('xc', BT['xc'])]]
    w = wb.create_sheet('来源'); [w.append([ID[k], t, u]) for k, t, u in SRC]
    wb.properties.created = wb.properties.modified = __import__('datetime').datetime(2026, 10, 21)
    wb.save(_P('cu', 'cu_model.xlsx'))


def md():
    L = ['# 铜 v0.1（2026-10-21）', '', '> 由 cu/build.py 生成，不要手改。网页：cu.html。公开数据整理，不构成投资建议。', '',
         '## 2027 平衡（千吨）', '', f"- 全球：ICSG +368；我们 {R['gbal'][2027]:+.0f}（矿山修正 {M.P0['mine27']}、数据中心 {R['dc27']:.0f}）",
         f"- 美国以外：高盛 −220；我们 {R['exus'][2027]:+.0f}（美国净囤货 {M.P0['us27']}）", '', '## 情景（2027 年均价，美元/吨）', '']
    L += [f"- {x['n']}（{x['p']*100:.0f}%）：{x['avg']:,}（{x['lo']:,}–{x['hi']:,}）；触发：{x['trig']}" for x in OUT['SC']]
    L += [f"- 概率加权：{OUT['EV']:,}", '', '## 一致预期', ''] + [f'- {r[0]}：{r[1]:,}（{r[2]}）' for r in CONS]
    L += ['', '## 预测', ''] + [f"- **{p['id']}** {p['text']}（到期 {p['due']}；验证：{p['check']}）" for p in PRED + CNPRED]
    L += ['', '## 证伪', ''] + [f"- **{f['j']}**：{f['falsify']} 阈值：{f['th']}" for f in FALS + CNFALS]
    L += ['', '## 局限', ''] + [f'- {x}' for x in LIMITS] + ['', '## 来源', ''] + [f'{ID[k]}. {t} {u}' for k, t, u in SRC]
    open(_P('cu', 'cu_chain.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


xlsx(); md()
print(f"cu: 2027 全球 {R['gbal'][2027]:+.0f} kt、美国以外 {R['exus'][2027]:+.0f} kt；数据中心 {R['dc27']:.0f} kt（+{R['ddc']:.0f}）；情景加权 {EV:,.0f}；2026E {AVG26:,}")
