"""行业版页面模板 v3（2026-10-23 起 pcb.html 用；John 定的九章研究框架）。
顶部：BLUF（主要矛盾，3–5 句）→ 什么会证明我们错 → 九章：
① 结论与市场观点 ② 地图与细分（分层原理图 / 路线图）③ 利润池与成本结构（格局图）④ 为什么：力量、护城河、份额稳定性
⑤ 需求与技术 ⑥ 周期与产能 ⑦ 替代 ⑧ 中国 vs 海外 ⑨ 主要矛盾、指标与证伪（含一线校验、待 John 确认、数据缺口）→ 附录（底稿 13 步、读后五问、来源、更新记录）。
pcb-map.html 的路线图 / 格局图已并进第 2、3 章（内容仍在 pcb/map.py）；新内容在 pcb/research.py；其余沿用 pcb/page.py 的 SPEC 与 v2 的块。
所有 pcb.js / chain.js 用到的 id 原样保留（总账标签、证伪表、预测台账照旧由 JS 渲染）。"""
import json, os, re, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R0, 'pcb'))
import research as R
import map as PM
from page_v2 import SIG, stcls, CSS as CSS2

CSS3 = '''<style>
.bluf{background:var(--card);border-radius:var(--r-card);padding:16px 18px;margin:14px 0;border-left:4px solid var(--tint)}
.bluf p{margin:0 0 .55em;font-size:17px;line-height:1.7}.bluf p:first-child{font-weight:700;font-size:19px}.bluf p:last-of-type{margin-bottom:.3em}
.wt{display:grid;gap:8px;margin:10px 0}.wt div{background:var(--card);border-radius:var(--r-card);padding:12px 14px;font-size:15px;line-height:1.6;border-left:4px solid var(--hig-red)}.wt b{display:block;font-size:16px}
.chh{margin-top:8px;padding-top:28px;border-top:.5px solid var(--hig-sep-op)}.chh>.kicker{color:var(--tint)}
.chq{font-size:15px;color:var(--mut);margin:-2px 0 12px}
.lay{margin:12px 0}.lay details{background:var(--card);border-radius:10px;margin:0 0 6px;border-left:8px solid var(--c);box-shadow:var(--hig-shadow)}
.lay summary{list-style:none;cursor:pointer;padding:10px 12px;min-height:44px;display:flex;flex-direction:column;justify-content:center}
.lay summary::-webkit-details-marker{display:none}.lay summary b{font-size:16px}.lay summary b::after{content:" ›";color:var(--mut);font-weight:400}.lay details[open] summary b::after{content:" ⌄"}
.lay summary span{font-size:13.5px;color:var(--mut);line-height:1.45}.lay dl{margin:0;padding:0 12px 12px}.lay dt{font-size:12px;color:var(--mut);font-weight:600;margin-top:8px}.lay dd{margin:2px 0 0;font-size:15px;line-height:1.6}
.lay .ax{font-size:12px;color:var(--mut);text-align:center;margin:2px 0 8px}
table.fin td,table.fin th{font-size:13px;white-space:nowrap;text-align:right}table.fin td:first-child,table.fin th:first-child{text-align:left;position:sticky;left:0;background:var(--card)}
table.fin tr.sum td{font-weight:700;border-top:1px solid var(--line)}.neg{color:var(--hig-tx-red)}
.trk{background:var(--card);border-radius:var(--r-card);padding:14px;margin:0 0 12px}.trk h3{margin:0 0 2px}.trk .role{font-size:12px;font-weight:700;color:var(--tint)}
.trk ol{margin:8px 0 0;padding-left:20px}.trk li{margin:0 0 10px;font-size:14.5px;line-height:1.6}.trk .k{color:var(--mut);font-size:12px;font-weight:600}.trk .wr{border-left:3px solid var(--warn);padding:4px 8px;font-size:14px}
.fq{background:var(--card);border-radius:var(--r-card);padding:12px 14px;margin:0 0 8px}.fq b{font-size:16px}.fq p{margin:4px 0;font-size:15px}
.cls{columns:2;column-gap:24px}@media(max-width:700px){.cls{columns:1}}
.pill.gap{background:var(--hig-warn-fill);color:var(--warn);font-size:11px}
</style>
'''


def fin_tables():
    D = R.FIN
    cos = {c['name']: c for c in D['cos']}
    o = []
    # 资本开支表
    rows = ''
    for c in R.BOARD:
        d = c['data']
        h, y = d['2026H1'], d['2025']
        rows += (f'<tr><td>{c["name"]}</td><td>{y["capex"]:.1f}</td><td>{h["capex"]:.1f}</td><td>{h["capex"]/h["dep"]:.1f}×</td>'
                 f'<td>{d["2024"]["cip"]:.1f}</td><td>{h["cip"]:.1f}</td><td>{y["roic"]:.1f}</td></tr>')
    A, Y5, A24 = R.AGG['2026H1'], R.AGG['2025'], R.AGG['2024']
    rows += (f'<tr class="sum"><td>10 家合计</td><td>{Y5["capex"]:.0f}</td><td>{A["capex"]:.0f}</td><td>{A["ratio"]:.1f}×</td><td>{A24["cip"]:.0f}</td><td>{A["cip"]:.0f}</td><td>中位 {R.MED["板厂"]["2025"]:.1f}</td></tr>')
    o.append('<div class="tbl"><table class="fin"><thead><tr><th>板厂（亿元）</th><th>资本开支 2025</th><th>资本开支 1H26</th><th>÷折旧 1H26</th><th>在建工程 2024末</th><th>在建工程 1H26</th><th>ROIC 2025 %</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
    capt = o.pop()
    # ROIC 表
    ys = [str(y) for y in range(2019, 2026)]
    rr = ''
    for seg in ('板厂', '覆铜板', '上游'):
        for c in [c for c in D['cos'] if c['seg'] == seg]:
            cells = ''.join((f'<td class="neg">{c["data"][y]["roic"]:.1f}</td>' if c['data'][y]['roic'] < 0 else f'<td>{c["data"][y]["roic"]:.1f}</td>') if c['data'].get(y, {}).get('roic') is not None else '<td>—</td>' for y in ys)
            gm = c['data']['2026H1']['gm']
            rr += f'<tr><td>{c["name"]}<span class="note"> {seg}</span></td>{cells}<td>{gm:.1f}</td></tr>'
        rr += f'<tr class="sum"><td>{seg}中位数</td>' + ''.join(f'<td>{R.MED[seg][y]:.1f}</td>' for y in ys) + f'<td>{R.GMED[seg]["2026H1"]:.1f}</td></tr>'
    roict = '<div class="tbl"><table class="fin"><thead><tr><th>ROIC %</th>' + ''.join(f'<th>{y}</th>' for y in ys) + '<th>毛利率 1H26</th></tr></thead><tbody>' + rr + '</tbody></table></div>'
    # 前五大客户
    tr = ''
    for name, v in R.T5.items():
        tr += f'<tr><td>{name}</td>' + ''.join(f'<td>{v[y]:.1f}</td>' if y in v else f'<td>{R.GAP}</td>' for y in range(2021, 2026)) + '</tr>'
    t5t = '<div class="tbl"><table class="fin"><thead><tr><th>前五大客户占比 %</th>' + ''.join(f'<th>{y}</th>' for y in range(2021, 2026)) + '</tr></thead><tbody>' + tr + '</tbody></table></div>'
    js = dict(yrs=R.YRS, agg={k: [round(R.AGG[y][k], 1) for y in R.YRS] for k in ('capex', 'dep', 'cip')} | {'ratio': [round(R.AGG[y]['ratio'], 2) for y in R.YRS]},
              ry=[str(y) for y in range(2015, 2026)], roic={k: [None if v is None else round(v, 1) for v in R.MED[k].values()] for k in R.MED},
              gm=[[c['name'][:2] if c['name'] not in ('生益电子', '生益科技') else c['name'][:2] + c['name'][2], c['data']['2025']['gm'], c['data']['2026H1']['gm'], c['seg']] for c in D['cos']],
              top5={n: {str(k): v for k, v in d.items()} for n, d in R.T5.items()})
    return capt, roict, t5t, '<script>window.PCBFIN=' + json.dumps(js, ensure_ascii=False) + '</script>'


def render_v3(S, STEPS, SID, MID, CIRC, CNC):
    args, cn = S['args'], S.get('cn')
    back = {s[0]: [] for s in STEPS}
    cback = {s[0]: [] for s in STEPS}
    for i, a in enumerate(args, 1):
        for j, e in enumerate(a['ev'], 1):
            for st in e['steps']:
                back[st].append((i, j))
    if cn:
        for i, a in enumerate(cn['args'], 1):
            for j, e in enumerate(a['ev'], 1):
                for st in e['steps']:
                    cback[st].append((i, j))
    assert [s['id'] for s in S['steps']] == [s[0] for s in STEPS], '底稿必须按 SOP 13 步顺序给全'
    assert len(S['claims']) <= 3 and len(S['quiz']) == 5 and 3 <= len(R.BLUF) <= 5
    nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)
    capt, roict, t5t, finjs = fin_tables()
    o = []
    w = o.append
    w(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 tpl/page_v3.py 根据 {S['spec']} + pcb/research.py + pcb/map.py 生成，不要手改；改内容请改这些文件后跑 ./build.sh -->
<title>{S['title']} · 产业链情报研究中心</title><meta name="description" content="{nolink(R.BLUF[0])}"><link rel="stylesheet" href="assets.css"><script src="theme.js"></script>
<script src="vendor/echarts.min.js"></script><script src="assets/hig-echarts.js"></script>{CSS2}{PM.CSS}{CSS3}<link rel="stylesheet" href="assets/hig.css"></head><body>
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="world/">世界</a><a class="btn" href="{S['other'][0]}">{S['other'][1]}</a><a class="btn" href="{S['archive'][0]}">{S['archive'][1]}</a><span class="pill">{S['pill']}</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
<div class="v2bar"><div class="wrap">{S['vbar']}</div></div>
''')
    CH = [('ch1', '结论'), ('ch2', '地图'), ('ch3', '利润池'), ('ch4', '为什么'), ('ch5', '需求与技术'), ('ch6', '周期'), ('ch7', '替代'), ('ch8', '中国'), ('ch9', '矛盾与证伪')]
    t1 = [('top', '主要矛盾')] + [(i, f'{n} {t}') for n, (i, t) in zip('①②③④⑤⑥⑦⑧⑨', CH)]
    t2 = [('base', '底稿总览')] + [(s[0], f'{s[1]} {s[2]}') for s in STEPS] + [('quiz', '读后五问'), ('src', '来源')]
    w('<nav class="sec two" id="nav" data-tier="c"><div class="wrap navw"><span class="tiers"><a href="#top" data-t="c" class="on">九章</a><a href="#base" data-t="b">底稿 13 步</a></span>')
    w('<span class="links l-c">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t1) + '</span>')
    w('<span class="links l-b">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t2) + '</span></div></nav>\n<main class="wrap">\n')

    def chap(i, n, t, q):
        w(f'<section id="{i}" data-nav="c" class="chh"><div class="kicker">第 {n} 章</div><h2>{t}</h2><p class="chq">{q}</p>\n')

    # ===== 顶部：BLUF + 什么会证明我们错
    w(f'<section id="top" data-nav="c"><div class="kicker">{S["kicker"]} · <a href="#log">更新记录</a></div>\n<h1 class="gov" style="margin-top:.2em">PCB：扩产潮能不能等到需求接住</h1>\n')
    w('<div class="bluf" id="bluf">' + ''.join(f'<p>{x}</p>' for x in R.BLUF) + f'<div class="note">{R.BLUF_SRC}</div></div>\n')
    w('<h3 id="prove">什么会证明我们错</h3><div class="wt">' + ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in R.WRONG_TOP) + '</div>\n')
    w('<div class="v2keys">' + ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in [
        (f'{R.NUMS["rH1"]}×', f'10 家板厂 1H26 资本开支 ÷ 折旧（{R.PEAK} 年高点 {R.NUMS["rPk"]}×）{R.SF}'),
        (f'{R.NUMS["cipH1"]} 亿', f'在建工程 1H26（2024 末 {R.NUMS["cip24"]} 亿）{R.SF}'),
        (f'{R.NUMS["roic25"]}%', f'板厂 ROIC 中位数 2025（2023 年 {R.NUMS["roic23"]}%）{R.SF}'),
        (f'{R.NUMS["sh25"]}%', f'胜宏前五大客户占比 2025（2024 年 {R.NUMS["sh24"]}%）{R.SC}')]) + '</div>\n')
    w(f'<p class="note">怎么读：九章从“结论”往下展开到“怎么证伪”；每章开头一句话说这章回答什么。<span class="tag t-src">源N</span> = 页末来源；<span class="tag t-est">估</span> = Kiko 自估；{R.GAP} = 没有可靠公开数据，不估；{R.PAY} = 付费数据，没看到原文。G / P 编号链接到<a href="ledger.html">总账</a>。公开数据整理，<b>不构成投资建议</b>，不对任何个股给买卖意见。</p>\n</section>\n')

    # ===== ① 结论与市场观点
    chap('ch1', '1', '结论与市场观点：我们和市场哪里不一样', '先说结论，再说和共识的差别；共识只用能公开核到的。')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>问题</th><th>市场 / 卖方</th><th>本页</th><th>账本</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="市场">{b}</td><td data-l="本页">{c}</td><td data-l="账本">{d}</td></tr>' for a, b, c, d in R.VIEW) + '</tbody></table></div>\n')
    w(f'<p class="note">{R.VIEW_NOTE}</p>\n')
    w(f'<div class="card" style="margin-top:12px"><b>2026 年的现状（v0.2 起的结论，未改）</b><p style="margin:.3em 0 0;font-size:15px">{S["gov"]}</p></div>\n')
    w('<div id="claims"><h3>三条核心判断（每条写了“若我错，你会看到什么”）</h3><div class="grid g3">')
    for i, c in enumerate(S['claims'], 1):
        w(f'<div class="card cl"><div class="jid">判断 {i} · {c["id"]} · 检查日 {c["due"]}</div><p style="margin:.3em 0;font-size:16px"><b>{c["t"]}</b></p><div class="note">依据：{c["ev"]}</div><div class="wr"><b>若我错，你会看到：</b>{c["wrong"]}</div></div>')
    w('</div></div>\n</section>\n')

    # ===== ② 地图与细分
    chap('ch2', '2', '产业地图与细分：一层一层看', '每一层做什么、怎么升级、谁在做。点开任一层。')
    w('<div class="lay" id="layers"><div class="ax">↓ 从买家往上游走 · 点开任一层看功能、代际、玩家</div>')
    for L in R.LAYERS:
        led = f'<dt>账本</dt><dd>{R.L(*L["led"])}</dd>' if L['led'] else ''
        w(f'<details name="layer" id="{L["id"]}" style="--c:{L["c"]}"><summary><b>{L["n"]}</b><span>{L["f"]}</span></summary><dl><dt>代际升级</dt><dd>{L["gen"]}</dd><dt>玩家与集中度</dt><dd>{L["who"]}</dd><dt>钱在哪</dt><dd>{L["money"]}</dd>{led}</dl></details>')
    w('</div>\n<p class="note">层的顺序按供应链，不是板子的物理叠层。“钱在哪”里的毛利率是公司整体口径（Tushare），包含非 AI 业务。</p>\n')
    w(f'<div id="heat"><h3>按产品与终端：哪些细分紧、哪些松</h3><p class="sub">{S["heat_note"]}</p>\n')
    w('<p class="note">四信号：<b>价</b> 价格 · <b>期</b> 交期 · <b>配</b> 配额 · <b>稼</b> 稼动率；' + ' '.join(f'<b class="{c}">{x}</b> {t}' for x, c, t in SIG.values()) + '。2027 列是我们的估计。</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>细分</th><th>2026E（亿美元）</th><th>2026 增速</th><th>驱动</th><th>价</th><th>期</th><th>配</th><th>稼</th><th>2026</th><th>2027</th><th>主约束</th><th>预期差</th></tr></thead><tbody>')
    for r in S['heat']:
        sg = ''.join(f'<td class="sg" data-l="{l}"><b class="{SIG[x][1]}" title="{SIG[x][2]}">{SIG[x][0]}</b></td>' for l, x in zip('价期配稼', r[4:8]))
        w(f'<tr><td>{r[0]}</td><td class="num" data-l="规模">{r[1]}</td><td data-l="增速">{r[2]}</td><td data-l="驱动">{r[3]}</td>{sg}'
          f'<td class="st {stcls(r[8])}" data-l="2026">{r[8]}</td><td class="st {stcls(r[9])}" data-l="2027">{r[9]}</td><td data-l="约束">{r[10]}</td><td data-l="预期差">{r[11]}</td></tr>')
    w('</tbody></table></div>\n')
    w(f'<div class="card" style="margin-top:12px"><b>{S["seg_t"]}</b><div id="pcb-cSeg" class="chart" style="height:320px"></div><div class="note">{S["seg_note"]}</div></div></div>\n')
    w('<div id="road"><h3>技术路线图：板子怎么一代代变“密”</h3>')
    for i, r in enumerate(PM.ROAD):
        w(PM.card(r) + ('\n<div class="arrow">↓ 线更细、孔更小</div>\n' if i < len(PM.ROAD) - 1 else '\n'))
    w('</div>\n<div id="road-ai"><h3>AI 服务器带来的新变量</h3><div class="note">Ⓐ–Ⓓ 已在出货或爬坡；Ⓔ 推迟；Ⓕ 还在测试。</div>\n' + '\n'.join(PM.card(r, True) for r in PM.AI) + '</div>\n')
    w('<div id="mech"><h3>原理：一块板怎么做出来，每种材料管什么</h3>')
    w('<div class="flowp">' + '<i>→</i>'.join(f'<span>{x}</span>' for x in S['flow']) + '</div>\n')
    w('<div class="tbl"><table class="stack"><thead><tr><th>材料 / 工序</th><th>管什么</th><th>AI 板为什么难</th></tr></thead><tbody>' + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in S['mech']) + '</tbody></table></div>\n')
    w(f'<p class="note">{S["terms"]}</p></div>\n</section>\n')

    def argsec(i, a, pre, circ, evp, lab, link):
        steps_cov = sorted({SID[st][1] for e in a['ev'] for st in e['steps']}, key=int)
        w(f'<div id="{pre}{i}"{" class=cnarg" if pre == "c" else ""} style="margin-top:20px"><div class="kicker">{lab} {circ[i-1]} · {a["tag"]} · 依据底稿第 {"/".join(steps_cov)} 步{"中国块" if pre == "c" else ""}</div>\n<h3 class="claim" style="font-size:19px">{a["claim"]}</h3>\n')
        if a.get('sub'):
            w(f'<p class="sub">{a["sub"]}</p>\n')
        h = a['hero']
        w(f'<div class="card hero"><b>{h["t"]}</b><div id="m-{h["src"]}" data-mirror="{h["src"]}" class="chart" style="height:{h.get("h", 340)}px"></div>'
          f'<div class="note">{h["note"]} <a href="#{link(h["step"])}">原图与假设在底稿第 {SID[h["step"]][1]} 步{"中国块" if pre == "c" else ""} ↓</a></div></div>\n<div class="evs">')
        for j, e in enumerate(a['ev'], 1):
            lk = ' · '.join(f'<a href="#{link(st)}">底稿 {SID[st][1]} {SID[st][3]}{" · 中国" if pre == "c" else ""} ↓</a>' for st in e['steps'])
            w(f'<div class="evc" id="{evp}{i}-{j}"><div class="ev">证据 {i}.{j}</div><b>{e["t"]}</b><p>{e["b"]}</p><div class="go">{lk}</div></div>')
        w('</div></div>\n')

    # ===== ③ 利润池与成本结构
    chap('ch3', '3', '利润池与成本结构：钱在哪一层', '先看每一环的格局，再看真实回报（ROIC）和毛利率怎么在变。')
    w('<div id="pattern"><h3>格局图：谁占多少、谁能涨价、钱在哪</h3><div class="note">从上游到下游排。越往上越集中、越有定价权。</div>\n'
      '<div class="tbl"><table class="mp stack"><thead><tr><th>环节</th><th>集中度</th><th>头部与份额</th><th>定价权</th><th>利润池</th><th>账本</th></tr></thead><tbody>\n')
    for seg, c, top, pw, pf, led in PM.MAP:
        w(f'<tr><td><b>{seg}</b></td><td data-l="集中度">{c}</td><td data-l="头部与份额">{top}</td><td data-l="定价权">{pw}</td><td data-l="利润池">{pf}</td><td data-l="账本">{" ".join(led)}</td></tr>\n')
    w('</tbody></table></div></div>\n')
    w(f'<div class="card" style="margin-top:12px"><b>毛利率：2025 → 2026H1（17 家 A 股，公司整体口径）</b><div id="fin-cGm" class="chart" style="height:520px"></div>'
      f'<div class="note">蓝 = 板厂、青 = 覆铜板、橙 = 上游（玻纤布、钻针、铜箔）。上游里分化很大：玻纤布、钻针大涨，铜箔仍低——钱在扩得慢、认证难的环节，不在吨数。{R.SF}</div></div>\n')
    w(f'<div class="card" style="margin-top:12px"><b>ROIC 中位数：板厂 / 覆铜板 / 上游（2015–2025）</b><div id="fin-cRoic" class="chart" style="height:300px"></div>'
      f'<div class="note">上一轮 2020–21 年扩产后，三个环节的 ROIC 都在 2022–24 年回落，覆铜板和上游一度为负。ROIC 用 Tushare 口径，各家投入资本算法未统一调整 {R.SF}。我们没有逐家算资本成本；如果按制造业常用的约 8% 粗看 {R.E}，2023–24 年多数公司低于资本成本。</div></div>\n')
    w(f'<details class="apx" style="margin-top:12px"><summary>逐家 ROIC 表（2019–2025 + 1H26 毛利率）<small>17 家</small></summary><div class="body">{roict}<p class="note">红色 = 负值；1H26 ROIC 是半年口径、没年化，所以表里不放。{R.SF}</p></div></details>\n')
    w('<h3 id="cost">成本结构：能核的写数，不能核的写缺口</h3><div class="tbl"><table class="stack"><thead><tr><th>成本项</th><th>证据</th><th>含义</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="证据">{b}</td><td data-l="含义">{c}</td></tr>' for a, b, c in R.COST) + '</tbody></table></div>\n')
    w(f'<div class="card" id="price" style="margin-top:12px"><b>价格分解：为什么“涨了”却不“缺”</b><p style="margin:.4em 0 0;font-size:15px">{S["pricebox"]}</p></div>\n')
    argsec(2, args[1], 'a', CIRC, 'e', '论点', lambda st: st)
    w('</section>\n')

    # ===== ④ 为什么
    chap('ch4', '4', '为什么：力量、护城河、份额稳定性', '谁有议价力、靠什么守住、份额稳不稳。')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>环节</th><th>供应商议价</th><th>买方议价</th><th>新进入者</th><th>替代</th><th>护城河</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="供应商">{b}</td><td data-l="买方">{c}</td><td data-l="新进入">{d}</td><td data-l="替代">{e}</td><td data-l="护城河">{f}</td></tr>' for a, b, c, d, e, f in R.FORCE) + '</tbody></table></div>\n')
    w(f'<p class="note">{R.FORCE_NOTE}</p>\n')
    w(f'<div class="card" style="margin-top:12px" id="buyer"><b>买方力量：前五大客户占比（年报）</b><div id="fin-cTop5" class="chart" style="height:300px"></div>'
      f'<div class="note">AI 板厂的客户越来越集中：胜宏 2024 → 2025 年从 {R.T5["胜宏科技"][2024]:.0f}% 升到 {R.T5["胜宏科技"][2025]:.0f}%，生益电子到 {R.T5["生益电子"][2025]:.0f}%；鹏鼎（苹果链）长期约 90%。集中度高 = 客户压价、导入二供的筹码大。{R.SC}</div></div>\n')
    w(f'<details class="apx" style="margin-top:12px"><summary>前五大客户占比全表<small>12 家 · 2021–2025</small></summary><div class="body">{t5t}<p class="note">世运 2022 年报在巨潮未检索到；广合 2023 年上市，之前没有年报。{R.SC}</p></div></details>\n')
    w(f'<p class="note" style="margin-top:12px">份额稳定性：2025 年 ROIC 已经分成两组——广合 {R.g("广合科技","2025","roic"):.1f}%、胜宏 {R.g("胜宏科技","2025","roic"):.1f}%、生益电子 {R.g("生益电子","2025","roic"):.1f}%、沪电 {R.g("沪电股份","2025","roic"):.1f}% vs 崇达 {R.g("崇达技术","2025","roic"):.1f}%、超声 {R.g("超声电子","2025","roic"):.1f}%、景旺 {R.g("景旺电子","2025","roic"):.1f}% {R.SF}。高回报只持续了 1–2 年，还看不出是护城河还是周期 {R.E}。</p>\n</section>\n')

    # ===== ⑤ 需求与技术
    chap('ch5', '5', '需求与技术：谁在拉、拉多久', '需求的上一层是云厂商资本开支；技术决定每台机柜用多少、用多好的板。')
    w(f'<div id="ai"><h3>{S["ai_h"]}</h3><p class="sub">{S["ai_sub"]}</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>环节</th><th>预测口径（2027 满足率，模型）</th><th>可观测信号（得分）</th><th>判定</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="预测">{b}</td><td data-l="可观测">{c}</td><td class="st {stcls(d)}" data-l="判定">{d}</td></tr>' for a, b, c, d in S['ai_tbl']) + '</tbody></table></div></div>\n')
    w('<p class="note">需求曲线、云厂商资本开支和每柜 PCB 价值在<a href="#demand">底稿第 3 步</a>；技术代际见第 2 章<a href="#road-ai">AI 新变量</a>。</p>\n')
    argsec(3, args[2], 'a', CIRC, 'e', '论点', lambda st: st)
    w('</section>\n')

    # ===== ⑥ 周期与产能
    chap('ch6', '6', '周期与产能：扩产潮有多大', '主要矛盾的证据在这里：钱已经投出去了，产能 2027–28 年到。')
    w(f'<div class="card" id="capex"><b>10 家 A 股板厂：资本开支、折旧、在建工程（亿元）与资本开支 ÷ 折旧（倍）</b><div id="fin-cCap" class="chart" style="height:340px"></div>'
      f'<div class="note">2026H1 是半年数（柱子只有半年），倍数是同期相除可比。上一轮 {R.PEAK} 年 {R.NUMS["rPk"]}× 之后，板厂 ROIC 中位数 2023 年降到 {R.NUMS["roic23"]}%。2016–2021 年为 8–9 家（生益电子、广合数据不全）。{R.SF}</div></div>\n')
    w(f'<div style="margin-top:12px">{capt}</div><p class="note">胜宏 1H26 资本开支 {R.g("胜宏科技","2026H1","capex"):.1f} 亿元、是折旧的 {R.g("胜宏科技","2026H1","capex")/R.g("胜宏科技","2026H1","dep"):.1f} 倍；鹏鼎在建工程 {R.g("鹏鼎控股","2026H1","cip"):.1f} 亿元。公司公告的扩产计划合计超 800 亿元 {R.S("capex")}。{R.SF}</p>\n')
    w(f'<div id="test" style="margin-top:16px"><h3>现在缺什么：四个信号排出来的约束顺序</h3><p class="sub">{S["test_rule"]}</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>#</th><th>环节</th><th>价格</th><th>交期</th><th>配额</th><th>稼动率</th><th>得分</th><th>判定</th></tr></thead><tbody>')
    for r in S['test']:
        w(f'<tr><td>{r[7]}</td><td><b>{r[0]}</b></td><td data-l="价格">{r[1]}</td><td data-l="交期">{r[2]}</td><td data-l="配额">{r[3]}</td><td data-l="稼动率">{r[4]}</td><td class="num" data-l="得分">{r[5]}</td><td class="st {stcls(r[6])}" data-l="判定">{r[6]}</td></tr>')
    w(f'</tbody></table></div>\n<p class="note">{S["test_note"]}</p></div>\n')
    w('<p class="note">先行指标：CCL 三家营收同比领先 AI 板厂约 5 个月（已回测，见<a href="#lead">底稿第 10 步</a>）；历史上玻纤布 2018 年后价格回落约两年（<a href="#hist">底稿第 9 步</a>）。</p>\n')
    argsec(1, args[0], 'a', CIRC, 'e', '论点', lambda st: st)
    w('</section>\n')

    # ===== ⑦ 替代
    chap('ch7', '7', '替代：什么能绕过最贵的那一环', '替代是上游涨价的天花板，也是 #4 观察项。')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>替代路径</th><th>替代什么</th><th>现状</th><th>看什么</th><th>账本</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="替代">{b}</td><td data-l="现状">{c}</td><td data-l="看">{d}</td><td data-l="账本">{e}</td></tr>' for a, b, c, d, e in R.SUBST) + '</tbody></table></div>\n</section>\n')

    # ===== ⑧ 中国 vs 海外
    chap('ch8', '8', '中国 vs 海外', '同一环节，海外龙头和中国龙头差在哪；再看国产 AI 卡这本账。')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>环节</th><th>海外龙头</th><th>中国龙头</th><th>差距</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="海外">{b}</td><td data-l="中国">{c}</td><td data-l="差距">{d}</td></tr>' for a, b, c, d in R.CNOS) + '</tbody></table></div>\n'
      f'<p class="note">“差距”一列是我们的归纳 {R.E}。海外和中国口径不同（季度 / 半年、营业利益率 / 毛利率），只看方向。</p>\n')
    if cn:
        w(f'<div id="cn" class="cnsec" style="margin-top:16px"><div class="kicker">平行账本 · {cn["kicker"]}</div>\n<div class="scqa">')
        for lab, txt in zip(('背景', '冲突', '问题'), cn['scqa']):
            w(f'<div><b>{lab}</b><span>{txt}</span></div>')
        w(f'</div>\n<h3 class="gov">{cn["gov"]}</h3>\n<div class="kl cn">')
        for i, a in enumerate(cn['args'], 1):
            w(f'<a href="#c{i}"><span class="i">{CNC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>')
        w(f'</div>\n<p class="note">{cn["mece"]}</p></div>\n')
        for i, a in enumerate(cn['args'], 1):
            argsec(i, a, 'c', CNC, 'ce', '中国论点', lambda st: 'cn-' + st)
    w('</section>\n')

    # ===== ⑨ 主要矛盾、指标与证伪
    chap('ch9', '9', '主要矛盾、先行指标与证伪', '每个矛盾 2–3 个先行指标，写好阈值和“什么算我错”，挂总账编号。')
    w('<div id="track">')
    for t in R.TRACK:
        w(f'<div class="trk"><div class="role">{t["n"]} · {t["role"]}</div><h3>{t["t"]}</h3><ol>')
        for ind, now, th, led in t['ind']:
            w(f'<li><b>{ind}</b><br><span class="k">现在</span> {now}<br><span class="k">阈值</span> {th}<br><span class="k">账本</span> {led}</li>')
        w(f'</ol><div class="wr"><b>证伪：</b>{t["wrong"]}</div></div>')
    w('</div>\n<p class="note">没有总账编号的阈值是本页提议，要变成预测需 John 确认（见下方“待 John 确认”）。</p>\n')
    w(f'<div id="check"><h3>一线校验：6 个问题，工厂比公开数据早知道</h3>')
    for i, (t, q, why, ref) in enumerate(R.FIELD, 1):
        w(f'<div class="fq"><b>Q{i} {t}</b> <span class="pill">{ref}</span><p>{q}</p><p class="note">为什么问：{why}</p></div>')
    w(f'<details class="apx" style="margin-top:8px"><summary>公开数据替代跟踪（每周五）<small>v0.2 的四个问题</small></summary><div class="body"><p class="sub">{S["check_sub"]}</p>'
      '<div class="tbl"><table class="hm stack"><thead><tr><th>问题</th><th>公开替代数据</th><th>频率</th><th>判读阈值</th><th>当前读数</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="数据">{b}</td><td data-l="频率">{c}</td><td data-l="阈值">{d}</td><td data-l="当前">{e}</td></tr>' for a, b, c, d, e in S['checks']) + '</tbody></table></div></div></details></div>\n')
    w(f'<div id="propose"><h3>待 John 确认：新预测草案</h3><p class="sub">这些<b>没有</b>写进总账（data/ledger.json），概率只是 Kiko 的建议；John 确认后才入账、才打分。</p>'
      '<div class="tbl"><table class="stack ledger"><thead><tr><th>#</th><th>预测（草案）</th><th>到期</th><th>验证来源</th><th>建议概率</th><th>对应矛盾</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td data-l="到期">{c}</td><td data-l="来源">{d}</td><td data-l="建议">{e} <span class="pill">待确认</span></td><td data-l="矛盾">{f}</td></tr>' for a, b, c, d, e, f in R.PROPOSE) + '</tbody></table></div></div>\n')
    w(f'<div id="wrong" style="padding-top:16px"><h3>已入账判断的证伪表（J1–J8、CJ1–CJ3）</h3>\n{S["wrong"]}\n</div>\n')
    w(f'<div id="pred" style="padding-top:16px"><h3>预测台账（已入账）</h3>\n{S["pred"]}\n</div>\n')
    w('<div id="gaps"><h3>数据缺口</h3><div class="grid g2"><div class="card"><b>这次补上的</b><ul>' + ''.join(f'<li>{x}</li>' for x in R.FILLED) + '</ul></div>'
      '<div class="card"><b>还缺的</b><ul>' + ''.join(f'<li>{x}</li>' for x in R.REMAIN) + '</ul><p class="note">原底图缺口逐条：</p><ul class="note">' + ''.join(f'<li>{x}</li>' for x in PM.GAPS) + '</ul></div></div></div>\n')
    w('</section>\n')

    # ===== 附录：底稿 13 步
    w(f'<section id="base" data-nav="b" class="apxsec"><div class="kicker">附录 · SOP 13 步底稿（默认折叠，点开或点任一“底稿 ↓”链接自动展开）</div>\n'
      f'<details class="apx base2" id="baseD"><summary>{S["base_title"]} <small>{S["base_sub"]}</small></summary><div class="body"><ol class="stepix">')
    for s in STEPS:
        sup = ''.join(CIRC[i-1] for i in sorted({i for i, _ in back[s[0]]})) + (' <i class="cnm">中</i>' if cn and any(x['id'] == s[0] and x.get('cn') for x in S['steps']) else '')
        w(f'<li><a href="#{s[0]}"><span class="n">{s[1]}</span>{MID[s[0]]}<span class="s">{sup}</span></a></li>')
    w('</ol>\n')
    for st, (sid, n, short, ttl) in zip(S['steps'], STEPS):
        chips = ''
        if back[sid]:
            chips = '<div class="sup">' + ''.join(f'<a href="#e{i}-{j}">支撑论点{CIRC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in back[sid]) + '</div>'
        elif st.get('ctx'):
            chips = f'<div class="sup"><span>{st["ctx"]}</span></div>'
        w(f'<div id="{sid}" class="step"><div class="kicker">底稿 {n} · {ttl}</div>\n<h2>{st["h"]}</h2>{chips}\n')
        if st.get('sub'):
            w(f'<p class="sub">{st["sub"]}</p>\n')
        w(st['body'].strip() + '\n')
        if st.get('cn'):
            c = st['cn']
            ch = ''.join(f'<a href="#ce{i}-{j}">支撑中国论点{CNC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in cback[sid])
            w(f'<div class="cnb" id="cn-{sid}"><div class="cnh"><span class="lb">中国账本</span><b>{c["h"]}</b></div>' + (f'<div class="sup">{ch}</div>' if ch else '') + c['body'].strip() + '</div>\n')
        w('</div>\n')
    w('</div></details>\n</section>\n')
    w('<section id="quiz" data-nav="b"><div class="kicker">附录 · 读后五问（v0.2）</div>\n'
      + ''.join(f'<details class="card qd"><summary>Q{i} {q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(S['quiz'], 1)) + '\n</section>\n')
    w(f'<section id="apx" data-nav="b" class="apxsec"><div class="kicker">附录</div>\n'
      f'<details class="apx" id="apxSrc"><summary>来源与局限 <small>{S["src_small"]}</small></summary><div class="body" id="src">{S["src"]}</div></details>\n'
      f'<details class="apx" id="apxLog"><summary>更新记录与下载 <small>每次改判都记在这里 · 旧版 v1 存档可对比</small></summary><div class="body" id="log">{S["log"]}</div></details>\n</section>\n')
    w(f'</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="ledger.html">总账</a> · <a href="{S["archive"][0]}">旧版 v1 存档</a> · <a href="{S["other"][0]}">{S["other"][1].replace(" ⇄","")}</a></footer>\n')
    w(finjs + ''.join(f'<script src="{x}"></script>' for x in ['ledger_ids.js', 'chain.js'] + S['scripts'] + ['pcb_fin.js']) + '\n')
    w('<script>document.getElementById("baseD").addEventListener("toggle",function(){if(this.open&&window.redraw)setTimeout(window.redraw,30)});</script>\n</body></html>\n')
    html = ''.join(o)
    assert not re.search(r'<a\b(?:(?!</a>).)*<a\b', html, re.S), f'{S["file"]}: 有嵌套 <a>'
    ids = re.findall(r'\bid="([^"]+)"', html)
    dup = {x for x in ids if ids.count(x) > 1}
    assert not dup, f'{S["file"]}: 重复 id {dup}'
    miss = {h for h in re.findall(r'href="#([\w-]+)"', html) if h not in ids and not re.match(r'src\d+$', h)}
    assert not miss, f'{S["file"]}: 锚点不存在 {miss}'
    return html
