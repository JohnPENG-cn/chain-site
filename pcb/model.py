"""PCB 小链模型（v0.1）。纯函数，build.py 和 pcb.js 用同一套公式（改这里要同步改 pcb.js 的 calc()）。
统一单位：百万颗 AI 加速器（KGI 口径，不含 CPU，读自 CoWoS 页模型）/ 年。
每一环："能支撑的加速器 = 该环节按目标规格的供给 ÷ 需求（来源口径）× 当年加速器出货"——即假设各环节需求和加速器出货同比例（估）。"""
import json, os
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_P = lambda *a: os.path.join(R0, *a)
Y = [2025, 2026, 2027]


def accel():
    """KGI AI 加速器出货（百万颗，不含 Vera / Venice CPU），读自 CoWoS 页"""
    d = json.load(open(_P('data', 'cowos.json')))['model']['demand']
    return {y: round(sum(x['units'] for x in d if x['y'] == y and 'CPU' not in x['chip']), 3) for y in Y}


def xchain():
    """跨链：ABF 载板、HBM、CoWoS 的满足率（供给 ÷ 需求），读自 CoWoS 页 TOC 汇总，不手抄"""
    t = json.load(open(_P('data', 'toc.json')))
    ip, sub = t['ipsum'], t['param']['sub']
    r = lambda v: round(1 + v / 100, 3)
    return dict(abf={2025: sub['2025'], 2026: r(ip['2026']['sub']), 2027: r(ip['2027']['sub'])},
                hbm={2026: r(ip['2026']['hbm']), 2027: r(ip['2027']['hbm'])},
                cwlo={2026: r(ip['2026']['cwlo']), 2027: r(ip['2027']['cwlo'])},
                cwhi={2026: r(ip['2026']['cwhi']), 2027: r(ip['2027']['cwhi'])},
                abf_g27=t['param']['sub27'] - 1)


# ---- 输入（每一项的来源见 build.py 的 STAGES 表）
CU = dict(d25=679, s25=803, d28=5206)          # 高盛 5 月：HVLP3+ 需求 / 有效供给（吨/月）[gscu]
CU['k'] = (CU['d28'] / CU['d25']) ** (1 / 3)    # 2025→28 需求几何插值（估）
CU['d26'], CU['d27'] = CU['d25'] * CU['k'], CU['d25'] * CU['k'] ** 2
CCL = dict(sh26=42, sh27=78,                    # 高盛 AI CCL 张数（百万张）[gs]
           cap=[585, 585, 585, 615, 735, 735, 855, 930])   # 台光电季末月产能（万张）2026Q1–2027Q4：法说会年末 615/930 [emcir] + 新增时序 [udn1]
CCL['g'] = (sum(CCL['cap'][4:]) / 4) / (sum(CCL['cap'][:4]) / 4)   # 年均产能增速
DR = {2025: (38.70, 35.28), 2026: (50.05, 51.16), 2027: (69.47, 76.73)}   # 钻针 有效供给 / 需求（亿支）[uad]
P0 = dict(dem=1.0, g26=0.45, g27=0.50, cn=150, gf26=0.90, gf27=0.80, mix=1.15, dr=1.0, s=0.0, abf=None)


def calc(p, A, X):
    """返回 {y: {stage: ratio}}；ratio = 供给 ÷ 需求（目标规格），s = 能靠降级吸收的缺口比例"""
    abf_g = X['abf_g27'] if p.get('abf') is None else p['abf']
    out = {}
    for y in Y:
        k = p['dem'] if y == 2027 else 1.0
        r = {}
        r['cu'] = {2025: CU['s25'] / CU['d25'], 2026: 1 / (1 + p['g26']), 2027: 1 / (1 + p['g27']) + p['cn'] / CU['d27']}[y] / k
        r['gf'] = {2025: None, 2026: p['gf26'], 2027: p['gf27']}[y]
        r['gf'] = None if r['gf'] is None else r['gf'] / k
        r['ccl'] = {2025: None, 2026: 1.0, 2027: CCL['g'] * p['mix'] / (CCL['sh27'] / CCL['sh26'])}[y]
        r['ccl'] = None if r['ccl'] is None else r['ccl'] / k
        r['dr'] = DR[y][0] / DR[y][1] * (p['dr'] if y == 2027 else 1) / k
        for q in ('cu', 'gf', 'ccl'):   # 降级：缺口里 s 的部分改用低一级材料（日东纺 NE 替代 NER [nqa]）
            if r[q] is not None and r[q] < 1:
                r[q] = r[q] + (1 - r[q]) * p['s']
        r['abf'] = X['abf'][y] * ((1 + abf_g) / (1 + X['abf_g27']) if y == 2027 else 1) / k
        pc = {q: r[q] for q in ('cu', 'gf', 'ccl', 'dr') if r[q] is not None}
        r['pmin'] = min(pc.values())
        r['pbind'] = min(pc, key=pc.get)
        r['units'] = {q: (None if v is None else round(v * A[y], 3)) for q, v in r.items() if q in ('cu', 'gf', 'ccl', 'dr', 'abf')}
        out[y] = r
    return out


# ---- 中国账本：国产卡要用的 PCB 链 vs 国内产能（2027）
CN = dict(usd=1621,            # 每卡 PCB 价值上限：VR200 每 GPU（摩根士丹利）[ms]
          fab_cny=(116.29 + 129.94 + 85.52) * 2,   # 胜宏营收 + 沪电 PCB + 深南 PCB，1H26 × 2（亿元）[sh1h, hd, sn]
          cnpcb_usd=410.7,     # 中国大陆 2025 年 PCB 产值（亿美元）[cninfo]
          fx=6.67,             # 人民币/美元：FinMind 2026-10-20 台币对美元 32.6、对人民币 4.89 套算
          cu_t=500,            # 德福 8 月 HVLP 出货（吨/月）[defu]
          ldk=2281,            # 宏和 2027 年低介电布（万米）[hh]
          ldk_per=(8000, 17000))   # 二代布 2027 年全球需求（万米）：纪要 8,000 [jy] / 广发 17,000 [gf]


def cnbal(cards, usd=CN['usd'], A27=None, cu_kg=None):
    """国产卡 cards（百万张）在 2027 年需要的 PCB 链产能，及国内产能在"全给国产卡"时能支撑的卡数（上限）"""
    fab = CN['fab_cny'] / CN['fx'] * 1e8          # 美元
    need_fab = cards * 1e6 * usd
    cu_need = cards * 1e6 * cu_kg / 1000 / 12      # 吨/月
    lo, hi = CN['ldk_per'][0] * 1e4 / (A27 * 1e6), CN['ldk_per'][1] * 1e4 / (A27 * 1e6)   # 米/颗（估：二代布需求 ÷ 加速器出货，含交换机）
    return dict(
        fab=dict(need=need_fab / 1e9, cap=fab / 1e9, share=need_fab / fab, share_cn=need_fab / (CN['cnpcb_usd'] * 1e8), up=fab / usd / 1e6),
        cu=dict(need=cu_need, cap=CN['cu_t'], share=cu_need / CN['cu_t'], up=CN['cu_t'] * 12 * 1000 / cu_kg / 1e6),
        ldk=dict(per=(lo, hi), need=(cards * lo * 100, cards * hi * 100), cap=CN['ldk'], share=(cards * lo * 100 / CN['ldk'], cards * hi * 100 / CN['ldk']),
                 up=(CN['ldk'] * 1e4 / hi / 1e6, CN['ldk'] * 1e4 / lo / 1e6)))


if __name__ == '__main__':
    A, X = accel(), xchain()
    R = calc(P0, A, X)
    print(A, X)
    for y in Y:
        print(y, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R[y].items() if k != 'units'})
    print('CU', {k: round(v) for k, v in CU.items() if k != 'k'}, 'CCL g', round(CCL['g'], 3))
