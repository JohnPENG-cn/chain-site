"""统一页面模板（SOP 页面规范 v1.4）。hbm.html、cowos.html、pcb.html、cu.html 都由这里生成，不要手改这些 HTML。
大宗商品页（cu 起）用同一模板；spec 可选 cons_sub 覆盖"主流 vs 我们"的说明句（不给则与芯片页完全相同）。
结构：最上 = 逻辑层（v1.6：三个问题 + 三句话逻辑 + 一张图 + 主流观点 vs 我们 + 我们重点盯什么，手机第一屏）；
     其下 = 结论层（金字塔：SCQA → 中心思想 → 3 条论点卡 → 每条论点的证据块 → 可能错在哪 → 预测台账）；
     下半 = 底稿（SOP 13 步，按 SOP 顺序全部展开）；只有来源、更新记录折叠。
证据块 ↔ 底稿步骤的双向链接由模板根据 spec 自动生成，两页结构不会漂移。
两本账（SOP v1.5）：spec 有 cn=dict(...) 时，结论层在全球论点后加平行的中国账本（#cn、#c1..），
     中心思想下加 ledgers 对照条；底稿 CN_REQ 6 步必须各有 steps[i]['cn'] 中国块（#cn-<步骤>），缺了构建报错。
用法：python3 tpl/page.py（build.sh 最后一步）。spec 在 <链>/page.py。
spec 带 layout='v2' 时改用 tpl/page_v2.py 的行业版结构；layout='v3' 用 tpl/page_v3.py 的九章研究版（2026-10-23 起 pcb.html）（目前只有 pcb.html；旧版 pcb_v1.html 是冻结存档，不由这里生成）。
layout='v4' 用链条 5 页模板（<链>.html 总览 + <链>-pattern / cycle / track / data + changelog.html，见 docs/CHAIN_TEMPLATE.md）：
     2026-10-27 起 PCB（tpl/page_v4.py），2026-10-28 起 HBM / CoWoS / 铜（tpl/page_v4g.py，配置在 <链>/page.py 的 SPEC['v4']）。"""
import importlib.util, os, re, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SOP 13 步：(锚点, 编号, 导航短名, 底稿标题前缀)。两页共用同一组锚点。
STEPS = [('key', '0', '要害', '要害变量'), ('debate', '1', '争议', '核心争议'), ('proc', '2', '工艺', '边界与工艺'),
         ('demand', '3', '需求', '需求（含上一层）'), ('supply', '4', '供给', '供给'), ('balance', '5', '平衡价格', '平衡与价格'),
         ('profit', '6', '利润池', '利润池'), ('neck', '7', '瓶颈', '瓶颈（TOC 推导）'), ('play', '8', '博弈', '关键玩家与博弈'),
         ('hist', '9', '历史', '历史'), ('lead', '10', '领先', '领先指标（回测）'), ('ledger', '11', '台账', '预测台账'),
         ('map', '12', '图谱接口', '公司图谱与对外接口')]
SID = {s[0]: s for s in STEPS}
MID = dict(zip([s[0] for s in STEPS], ['要害变量', '核心争议', '边界与工艺', '需求', '供给', '平衡与价格', '利润池', '瓶颈 TOC', '玩家与博弈', '历史', '领先指标', '预测台账', '图谱与接口']))   # 底稿目录用的中等长度名（手机两列放得下）
CIRC = '①②③④'
CNC = '❶❷❸❹'   # 中国账本论点用实心圈，和全球账本区分
CN_REQ = ['demand', 'supply', 'balance', 'neck', 'play', 'map']   # SOP v1.5：有中国账本的链，这 6 步必须各有中国块


LQ = ('① 未来整体供需怎么走', '② 制约它的是什么', '③ 哪里有没被看到的预期差')


def flow(nodes):
    """一张图看懂：竖排流程图（SVG，颜色全用 CSS 变量，深浅色自动跟随）。nodes = [(标题, 一行说明)]，最后一个是约束。"""
    W, h, g, y, o = 340, 52, 24, 4, []
    for i, (t, d) in enumerate(nodes):
        last = i == len(nodes) - 1
        o.append(f'<rect x="10" y="{y}" width="{W-20}" height="{h}" rx="12" class="{"fk" if last else "fn"}"/>'
                 f'<text x="{W//2}" y="{y+22}" class="ft">{t}</text><text x="{W//2}" y="{y+41}" class="fd">{d}</text>')
        if not last:
            ya = y + h
            o.append(f'<path d="M{W//2} {ya+3} V{ya+g-5}" class="fa"/><path d="M{W//2-5} {ya+g-10} L{W//2} {ya+g-4} L{W//2+5} {ya+g-10}" class="fa"/>')
        y += h + g
    return f'<svg class="flow" viewBox="0 0 {W} {y-g+8}" role="img" aria-label="一张图看懂">{"".join(o)}</svg>'


def render(S):
    args = S['args']
    assert 3 <= len(args) <= 4, '关键论点必须 3 条（最多 4 条）'
    assert [s['id'] for s in S['steps']] == [s[0] for s in STEPS], '底稿必须按 SOP 13 步顺序给全'
    back = {s[0]: [] for s in STEPS}   # 步骤 → 支撑的证据块
    cn = S.get('cn')
    cback = {s[0]: [] for s in STEPS}  # 步骤 → 支撑的中国证据块
    if cn:
        stp = {s['id']: s for s in S['steps']}
        miss = [x for x in CN_REQ if not stp[x].get('cn')]
        assert not miss, f"{S['file']}: 有中国账本时底稿第 {'/'.join(SID[x][1] for x in miss)} 步缺中国块"
        assert S.get('ledgers'), '有中国账本时必须在中心思想下给出"两本账"对照'
        assert 2 <= len(cn['args']) <= 4
        for i, a in enumerate(cn['args'], 1):
            for j, e in enumerate(a['ev'], 1):
                for st in e['steps']:
                    assert stp[st].get('cn'), f'中国证据 {i}.{j} 指向的第 {SID[st][1]} 步没有中国块'
                    cback[st].append((i, j))
    for i, a in enumerate(args, 1):
        for j, e in enumerate(a['ev'], 1):
            for st in e['steps']:
                assert st in SID, st
                back[st].append((i, j))
    for st, lst in back.items():
        if st not in ('ledger',) and not lst and not S['steps'][[x[0] for x in STEPS].index(st)].get('ctx'):
            raise SystemExit(f"{S['file']}: 底稿第 {SID[st][1]} 步 {st} 没有支撑任何论点（如确属背景材料，spec 里标 ctx）")
    L = S['logic']   # v1.6：逻辑层必须有
    assert len(L['qa']) == 3 and len(L['three']) == 3, '逻辑层：恰好 3 个问题、三句话'
    assert 3 <= len(L['watch']) <= 5 and len(L['cons']) >= 3, '逻辑层：盯 3–5 项，主流 vs 我们至少 3 行'
    assert all(len(r) == 4 for r in L['watch']) and all(len(r) == 5 for r in L['cons'])
    o = []
    w = o.append
    w(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 tpl/page.py 根据 {S['spec']} 生成，不要手改；改内容请改 spec 后跑 ./build.sh -->
<title>{S['title']} · 产业链情报研究中心</title><link rel="stylesheet" href="assets.css"><script src="theme.js"></script>
<script src="vendor/echarts.min.js"></script><script src="assets/hig-echarts.js"></script><link rel="stylesheet" href="assets/hig.css"></head><body>
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="world/">世界</a><a class="btn" href="{S['other'][0]}">{S['other'][1]}</a><span class="pill">{S['pill']}</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
''')
    # 两层导航
    t1 = [('logic', '逻辑'), ('top', '结论')] + [(f'a{i}', f'{CIRC[i-1]} {a["tag"]}') for i, a in enumerate(args, 1)]
    if cn:
        t1 += [('cn', cn['nav'])] + [(f'c{i}', f'{CNC[i-1]} {a["tag"]}') for i, a in enumerate(cn['args'], 1)]
    t1 += [('wrong', '可能错在哪'), ('pred', '预测台账')]
    t2 = [('base', '总览')] + [(s[0], f'{s[1]} {s[2]}') for s in STEPS] + [('src', '来源')]
    w('<nav class="sec two" id="nav" data-tier="c"><div class="wrap navw"><span class="tiers"><a href="#logic" data-t="c" class="on">结论层</a><a href="#base" data-t="b">底稿 13 步</a></span>')
    w('<span class="links l-c">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t1) + '</span>')
    w('<span class="links l-b">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t2) + '</span></div></nav>\n<main class="wrap">\n')
    # ⓪ 逻辑层：三个问题（全球 + 中国）→ 三句话 + 一张图 → 主流 vs 我们 → 我们重点盯什么
    w(f'<section id="logic" data-nav="c" class="logic"><div class="kicker">逻辑层 · 先看这一屏 · 往下是<a href="#top">结论层</a>和<a href="#base">底稿</a></div>\n<h1 class="lgt">{L["title"]}</h1>\n<div class="q3">')
    for q, (g, c) in zip(LQ, L['qa']):
        w(f'<div class="qa"><div class="qn">{q}</div><p class="ag"><i>全球</i>{g}</p><p class="ac"><i>中国</i>{c}</p></div>')
    w(f'</div>\n<p class="note terms">{L["terms"]}</p>\n<div class="grid g2 lg2"><div class="card"><b>三句话逻辑</b><ol class="three">' + ''.join(f'<li>{x}</li>' for x in L['three']) + '</ol></div>')
    w('<div class="card"><b>一张图看懂</b><div class="keys">' + ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in L['keys']) + f'</div>{flow(L["fig"])}<div class="note">{L["fig_note"]}</div></div></div>\n')
    w('<h3>主流观点 vs 我们</h3><p class="sub">' + S.get('cons_sub', '左边是券商、研究机构、韩媒的公开说法（带来源）；"差距"一栏就是预期差。') + '</p><div class="tbl"><table class="stack cons"><thead><tr><th>主流观点</th><th>我们</th><th>差距</th><th>证据</th><th>什么能确认</th></tr></thead><tbody>'
      + ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in L['cons']) + '</tbody></table></div>\n')
    w('<h3>我们重点盯什么</h3><div class="tbl"><table class="stack watch"><thead><tr><th>盯什么</th><th>指标</th><th>阈值 → 含义</th><th>日期</th></tr></thead><tbody>'
      + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td style="white-space:nowrap">{d}</td></tr>' for a, b, c, d in L['watch']) + '</tbody></table></div>\n</section>\n')
    # ① SCQA + ② 中心思想 + ③ 论点卡
    w(f'<section id="top" data-nav="c">\n<div class="kicker">结论层 · {S["kicker"]} · <a href="#log">更新记录</a></div>\n<div class="scqa">')
    for lab, txt in zip(('背景', '冲突', '问题'), S['scqa']):
        w(f'<div><b>{lab}</b><span>{txt}</span></div>')
    w(f'</div>\n<div class="kicker" style="margin-top:18px">回答 · 中心思想</div>\n<h1 class="gov" style="margin-top:.2em">{S["gov"]}</h1>\n<div class="kl">')
    nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)   # 卡片本身是链接，里面不能再嵌 <a>
    for i, a in enumerate(args, 1):
        w(f'<a href="#a{i}"><span class="i">{CIRC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>')
    w('</div>\n')
    if S.get('ledgers'):   # 两本账对照：全球 vs 中国（出口管制/国产化重要的链必须有，SOP v1.5）
        w('<div class="twoled">' + ''.join(f'<a href="#{h}" class="{c}"><span class="lb">{lb}</span><span>{nolink(t)}</span></a>' for h, c, lb, t in S['ledgers']) + '</div>\n')
    w(f'<p class="note">{S["mece"]} 标注：<span class="tag t-src">源N</span> = 页末第 N 条公开来源；<span class="tag t-est">估</span> = Kiko 自估，可在底稿里用滑块改。'
      f'上半页是结论层（金字塔），下半页是<a href="#base">底稿</a>：按 <a href="https://github.com/JohnPENG-cn/chain-site/blob/main/SOP.md">SOP</a> 13 步的完整产业链分析；每个证据块都链到底稿对应步骤，底稿每一步也标了它支撑哪条论点。</p>\n</section>\n')
    # ④ 论点节（全球 a1..；中国 c1..，证据块链到底稿各步的中国块）
    def argsec(i, a, pre, circ, evp, lab, link):
        steps_cov = sorted({SID[st][1] for e in a['ev'] for st in e['steps']}, key=int)
        w(f'<section id="{pre}{i}" data-nav="c"{" class=cnarg" if pre == "c" else ""}><div class="kicker">{lab} {circ[i-1]} · {a["tag"]} · 依据底稿第 {"/".join(steps_cov)} 步{"中国块" if pre == "c" else ""}</div>\n<h2 class="claim">{a["claim"]}</h2>\n')
        if a.get('sub'):
            w(f'<p class="sub">{a["sub"]}</p>\n')
        h = a['hero']
        w(f'<div class="card hero"><b>{h["t"]}</b><div id="m-{h["src"]}" data-mirror="{h["src"]}" class="chart" style="height:{h.get("h", 340)}px"></div>'
          f'<div class="note">{h["note"]} <a href="#{link(h["step"])}">原图与假设在底稿第 {SID[h["step"]][1]} 步{"中国块" if pre == "c" else ""} ↓</a></div></div>\n<div class="evs">')
        for j, e in enumerate(a['ev'], 1):
            lk = ' · '.join(f'<a href="#{link(st)}">底稿 {SID[st][1]} {SID[st][3]}{" · 中国" if pre == "c" else ""} ↓</a>' for st in e['steps'])
            w(f'<div class="evc" id="{evp}{i}-{j}"><div class="ev">证据 {i}.{j}</div><b>{e["t"]}</b><p>{e["b"]}</p><div class="go">{lk}</div></div>')
        w('</div>\n</section>\n')
    for i, a in enumerate(args, 1):
        argsec(i, a, 'a', CIRC, 'e', '论点', lambda st: st)
    if cn:   # 平行账本：中国视角的 SCQA + 中心思想 + 论点
        w(f'<section id="cn" data-nav="c" class="cnsec"><div class="kicker">平行账本 · {cn["kicker"]}</div>\n<div class="scqa">')
        for lab, txt in zip(('背景', '冲突', '问题'), cn['scqa']):
            w(f'<div><b>{lab}</b><span>{txt}</span></div>')
        w(f'</div>\n<div class="kicker" style="margin-top:18px">回答 · 中国账本的中心思想</div>\n<h2 class="gov">{cn["gov"]}</h2>\n<div class="kl cn">')
        for i, a in enumerate(cn['args'], 1):
            w(f'<a href="#c{i}"><span class="i">{CNC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>')
        w(f'</div>\n<p class="note">{cn["mece"]}</p>\n</section>\n')
        for i, a in enumerate(cn['args'], 1):
            argsec(i, a, 'c', CNC, 'ce', '中国论点', lambda st: 'cn-' + st)
    # ⑤ 可能错在哪  ⑥ 预测台账
    w(f'<section id="wrong" data-nav="c"><div class="kicker">我们可能错在哪 · 底稿第 1/11 步</div>\n<h2>每条论点都写好了"什么情况算我错"</h2>\n{S["wrong"]}\n</section>\n')
    w(f'<section id="pred" data-nav="c"><div class="kicker">预测台账 · 底稿第 11 步</div><h2>写下来，到期打分</h2>\n{S["pred"]}\n</section>\n')
    # 底稿
    w(f'<section id="base" data-nav="b" class="basehd"><div class="kicker">底稿 · SOP 13 步完整产业链分析</div><h2>{S["base_title"]}</h2><p class="sub">{S["base_sub"]}</p><ol class="stepix">')
    for s in STEPS:
        sup = ''.join(CIRC[i-1] for i in sorted({i for i, _ in back[s[0]]})) + (' <i class="cnm">中</i>' if cn and any(x['id'] == s[0] and x.get('cn') for x in S['steps']) else '')
        w(f'<li><a href="#{s[0]}"><span class="n">{s[1]}</span>{MID[s[0]]}<span class="s">{sup}</span></a></li>')
    w('</ol></section>\n')
    for st, (sid, n, short, ttl) in zip(S['steps'], STEPS):
        chips = ''
        if back[sid]:
            chips = '<div class="sup">' + ''.join(f'<a href="#e{i}-{j}">支撑论点{CIRC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in back[sid]) + '</div>'
        elif st.get('ctx'):
            chips = f'<div class="sup"><span>{st["ctx"]}</span></div>'
        w(f'<section id="{sid}" data-nav="b" class="step"><div class="kicker">底稿 {n} · {ttl}</div>\n<h2>{st["h"]}</h2>{chips}\n')
        if st.get('sub'):
            w(f'<p class="sub">{st["sub"]}</p>\n')
        w(st['body'].strip() + '\n')
        if st.get('cn'):   # 中国块：同一步的中国账本，和全球内容并排放在同一步里
            c = st['cn']
            ch = ''.join(f'<a href="#ce{i}-{j}">支撑中国论点{CNC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in cback[sid])
            w(f'<div class="cnb" id="cn-{sid}"><div class="cnh"><span class="lb">中国账本</span><b>{c["h"]}</b></div>' + (f'<div class="sup">{ch}</div>' if ch else '') + c['body'].strip() + '</div>\n')
        w('</section>\n')
    # 只有来源、更新记录折叠
    w(f'<section id="apx" data-nav="b" class="apxsec"><div class="kicker">附录</div>\n'
      f'<details class="apx" id="apxSrc"><summary>来源与局限 <small>{S["src_small"]}</small></summary><div class="body" id="src">{S["src"]}</div></details>\n'
      f'<details class="apx" id="apxLog"><summary>更新记录与下载 <small>每次改判都记在这里</small></summary><div class="body" id="log">{S["log"]}</div></details>\n</section>\n')
    w(f'</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="{S["other"][0]}">{S["other"][1].replace(" ⇄","")}</a></footer>\n')
    w(''.join(f'<script src="{x}"></script>' for x in ['ledger_ids.js', 'chain.js'] + S['scripts']) + '\n</body></html>\n')
    html = ''.join(o)
    assert not re.search(r'<a\b(?:(?!</a>).)*<a\b', html, re.S), f'{S["file"]}: 有嵌套 <a>'
    # 自检：id 不重复；所有页内锚点存在（#srcN 由脚本生成，跳过）
    ids = re.findall(r'\bid="([^"]+)"', html)
    dup = {x for x in ids if ids.count(x) > 1}
    assert not dup, f'{S["file"]}: 重复 id {dup}'
    miss = {h for h in re.findall(r'href="#([\w-]+)"', html) if h not in ids and not re.match(r'src\d+$', h)}
    assert not miss, f'{S["file"]}: 锚点不存在 {miss}'
    return html


def load(chain):
    p = os.path.join(R0, chain, 'page.py')
    sp = importlib.util.spec_from_file_location(chain + '_page', p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.SPEC['spec'] = f'{chain}/page.py'
    return m.SPEC


if __name__ == '__main__':
    idx = open(os.path.join(R0, 'index.html'), encoding='utf-8').read()
    CL = {}
    for chain in ('hbm', 'cowos', 'pcb', 'cu'):   # cu = 大宗商品系列（铜），同一模板
        S = load(chain)
        if S.get('layout') == 'v2':   # 行业版结构（2026-10-21 起 pcb.html），见 tpl/page_v2.py
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from page_v2 import render_v2
            html = render_v2(S, STEPS, SID, MID, CIRC, CNC)
        elif S.get('layout') == 'v3':   # 九章研究版（2026-10-23 起 pcb.html），见 tpl/page_v3.py
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from page_v3 import render_v3
            html = render_v3(S, STEPS, SID, MID, CIRC, CNC)
        elif S.get('layout') == 'v4':   # 链条 5 页模板（2026-10-27 起 PCB，2026-10-28 起 HBM / CoWoS / 铜），见 tpl/page_v4.py + tpl/page_v4g.py + docs/CHAIN_TEMPLATE.md
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import page_v4
            if chain == 'pcb':
                page_v4.use('pcb')
                pages = page_v4.render_v4(S, STEPS, SID, MID, CIRC, CNC)
                st, CL[chain] = page_v4.render_v4.STAT, page_v4.render_v4.CL
            else:
                from page_v4g import render_v4g
                pages = render_v4g(S, STEPS, SID, MID, CIRC, CNC, chain, flow)
                st, CL[chain] = render_v4g.STAT, render_v4g.CL
            for fn, h in pages.items():
                open(os.path.join(R0, fn), 'w', encoding='utf-8').write(h)
            print('  v4 页面：' + '；'.join(f'{k} 脚注 {v["fn_main"]}、标签 {v["labels"]}' for k, v in st.items()))
            html = None
        else:
            html = render(S)
        if html is not None:
            open(os.path.join(R0, S['file']), 'w', encoding='utf-8').write(html)
        # 首页卡片 = 同一句中心思想
        idx, n = re.subn(rf'(<!--card:{chain}-->).*?(<!--/card-->)', lambda m: m.group(1) + S['card'] + m.group(2), idx, flags=re.S)
        assert n == 1, f'index.html 缺 card:{chain} 标记'
        print(f'{S["file"]}{"（" + S["layout"] + "）" if S.get("layout") else ""}: {len(S["args"])} 条论点、{sum(len(a["ev"]) for a in S["args"])} 个证据块、13 步底稿' + (f'；中国账本 {len(S["cn"]["args"])} 条论点、{sum(len(a["ev"]) for a in S["cn"]["args"])} 个证据块、{sum(1 for x in S["steps"] if x.get("cn"))} 个中国块' if S.get('cn') else ''))
    open(os.path.join(R0, 'index.html'), 'w', encoding='utf-8').write(idx)
    if CL:   # 更新记录页：各链的版本说明、逐版记录、旧网址去处
        open(os.path.join(R0, 'changelog.html'), 'w', encoding='utf-8').write(page_v4.changelog_page(CL))
