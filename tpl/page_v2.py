"""行业版页面模板 v2（2026-10-21 起 pcb.html 用；hbm / cowos / cu 仍用 tpl/page.py 的 render，输出不受影响）。
结构（为"看懂"而排）：一句话 + 读后五问预告 → 行业地图（热力表）→ 短缺检验（四信号）→ 机制入门 + 价格分解 → 三条核心判断（若错你会看到）
→ AI 下钻（可观测 vs 预测 + 原论点 / 中国账本，压缩）→ 一线校验 → 可能错在哪 → 预测台账 → 底稿 13 步（默认折叠）→ 读后五问 → 来源与更新记录。
spec 字段见 pcb/page.py（layout='v2'）。底稿 13 步与证据块双向链接沿用 v1 规则；折叠块里的图在展开时重画（window.redraw）。"""
import re

SIG = {'Y': ('✓', 'sgY', '成立'), 'H': ('½', 'sgH', '部分成立'), 'N': ('✗', 'sgN', '不成立'), 'Q': ('?', 'sgQ', '没有可引用证据')}


def stcls(t):
    if t.startswith('紧') or t.startswith('实缺'):
        return 'hot'
    if t.startswith('偏紧') or t.startswith('结构') or t.startswith('认证'):
        return 'warm'
    if t.startswith('需求松') or t.startswith('平'):
        return 'mix'
    if t.startswith('松') or t.startswith('不缺'):
        return 'cold'
    return 'na'


CSS = '''<style>
.v2bar{background:var(--card);border-bottom:1px solid var(--line);font-size:13px;padding:6px 0;color:var(--mut)}.v2bar a{font-weight:600}
table.hm td,table.hm th{font-size:13px;vertical-align:top}table.hm .num{white-space:nowrap}table.hm .sg{text-align:center;font-size:15px}
.st{font-weight:700}.st.hot{background:rgba(217,83,79,.18)}.st.warm{background:rgba(230,140,40,.20)}.st.mix{background:rgba(230,190,60,.16)}.st.cold{background:rgba(91,141,239,.16)}.st.na{color:var(--mut)}
.sgY{color:#d9534f}.sgH{color:#e08a20}.sgN{color:#5b8def}.sgQ{color:var(--mut);font-weight:400}
.flowp{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px;margin:6px 0 12px}.flowp span{border:1px solid var(--line);border-radius:6px;padding:3px 8px;background:var(--card)}
.v2keys{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0}.v2keys div{border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:var(--card)}.v2keys b{display:block;font-size:22px;color:var(--acc)}.v2keys span{font-size:12.5px;color:var(--mut)}
@media(max-width:700px){.v2keys{grid-template-columns:repeat(2,1fr)}.v2keys b{font-size:19px}}
.cl .jid{font-size:12px;color:var(--mut)}.cl .wr{border-left:3px solid var(--warn);padding:4px 8px;margin-top:8px;font-size:14px}
ol.q5{margin:6px 0 0 18px;padding:0;line-height:1.7}details.qd{margin:8px 0}details.qd>summary{font-weight:600}details.qd p{margin:4px 16px 14px;font-size:15px}
details.base2>summary{font-size:17px}details.base2 .step{padding:28px 0;border-bottom:1px solid var(--line);scroll-margin-top:100px}details.base2 .card{background:var(--card)}details.base2>.body{overflow-x:visible}
@media(max-width:700px){table.hm.stack td.sg{display:inline-block;margin-right:10px}table.hm.stack td.sg::before{content:attr(data-l)" ";color:var(--mut);font-size:12px}table.hm.stack td[data-l]:not(.sg)::before{content:attr(data-l)"　";color:var(--mut);font-size:12px;font-weight:400}}
</style>
'''


def render_v2(S, STEPS, SID, MID, CIRC, CNC):
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
    assert len(S['claims']) <= 3 and len(S['quiz']) == 5
    nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)
    o = []
    w = o.append
    w(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 tpl/page_v2.py 根据 {S['spec']} 生成，不要手改；改内容请改 spec 后跑 ./build.sh -->
<title>{S['title']} · 产业链情报研究中心</title><link rel="stylesheet" href="assets.css"><script src="theme.js"></script>
<script src="vendor/echarts.min.js"></script><script src="assets/hig-echarts.js"></script>{CSS}<link rel="stylesheet" href="assets/hig.css"></head><body>
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="world/">世界</a><a class="btn" href="{S['other'][0]}">{S['other'][1]}</a><a class="btn" href="{S['archive'][0]}">{S['archive'][1]}</a><span class="pill">{S['pill']}</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
<div class="v2bar"><div class="wrap">{S['vbar']}</div></div>
''')
    t1 = [('top', '一句话'), ('heat', '行业地图'), ('test', '短缺检验'), ('mech', '机制'), ('claims', '三条判断'), ('ai', 'AI 下钻')]
    t1 += [(f'a{i}', f'{CIRC[i-1]} {a["tag"]}') for i, a in enumerate(args, 1)]
    if cn:
        t1 += [('cn', cn['nav'])]
    t1 += [('check', '一线校验'), ('wrong', '可能错在哪'), ('pred', '预测台账'), ('quiz', '读后五问')]
    t2 = [('base', '底稿总览')] + [(s[0], f'{s[1]} {s[2]}') for s in STEPS] + [('src', '来源')]
    w('<nav class="sec two" id="nav" data-tier="c"><div class="wrap navw"><span class="tiers"><a href="#top" data-t="c" class="on">正文</a><a href="#base" data-t="b">底稿 13 步</a></span>')
    w('<span class="links l-c">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t1) + '</span>')
    w('<span class="links l-b">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in t2) + '</span></div></nav>\n<main class="wrap">\n')
    # ⓪ 一句话
    w(f'<section id="top" data-nav="c"><div class="kicker">{S["kicker"]} · <a href="#log">更新记录</a></div>\n<h1 class="gov" style="margin-top:.2em">{S["gov"]}</h1>\n')
    w('<div class="v2keys">' + ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in S['keys']) + '</div>\n')
    w('<div class="card"><b>读完这一页，你应该能回答这五个问题</b>（答案在<a href="#quiz">页末</a>）<ol class="q5">' + ''.join(f'<li>{q}</li>' for q, _ in S['quiz']) + '</ol></div>\n')
    if S.get('ledgers'):
        w('<div class="twoled">' + ''.join(f'<a href="#{h}" class="{c}"><span class="lb">{lb}</span><span>{nolink(t)}</span></a>' for h, c, lb, t in S['ledgers']) + '</div>\n')
    w(f'<p class="note">{S["mece"]} 标注：<span class="tag t-src">源N</span> = 页末第 N 条公开来源；<span class="tag t-est">估</span> = Kiko 自估。</p>\n</section>\n')
    # ① 行业地图
    w(f'<section id="heat" data-nav="c"><div class="kicker">① 行业地图 · 先看全局，AI 只是其中几行</div><h2>哪些细分紧、哪些松：按产品与终端</h2>\n<p class="sub">{S["heat_note"]}</p>\n')
    w('<p class="note">四信号：<b>价</b> 价格 · <b>期</b> 交期 · <b>配</b> 配额 · <b>稼</b> 稼动率；' + ' '.join(f'<b class="{c}">{x}</b> {t}' for x, c, t in SIG.values()) + '。2026 / 2027 列：紧 = 至少两个信号成立，偏紧 = 一个，平 / 松 = 没有或需求在降；2027 列是我们的估计。</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>细分</th><th>2026E（亿美元）</th><th>2026 增速</th><th>驱动</th><th>价</th><th>期</th><th>配</th><th>稼</th><th>2026</th><th>2027</th><th>主约束</th><th>预期差</th></tr></thead><tbody>')
    for r in S['heat']:
        sg = ''.join(f'<td class="sg" data-l="{l}"><b class="{SIG[x][1]}" title="{SIG[x][2]}">{SIG[x][0]}</b></td>' for l, x in zip('价期配稼', r[4:8]))
        w(f'<tr><td>{r[0]}</td><td class="num" data-l="规模">{r[1]}</td><td data-l="增速">{r[2]}</td><td data-l="驱动">{r[3]}</td>{sg}'
          f'<td class="st {stcls(r[8])}" data-l="2026">{r[8]}</td><td class="st {stcls(r[9])}" data-l="2027">{r[9]}</td><td data-l="约束">{r[10]}</td><td data-l="预期差">{r[11]}</td></tr>')
    w('</tbody></table></div>\n')
    w(f'<div class="card" style="margin-top:12px"><b>{S["seg_t"]}</b><div id="pcb-cSeg" class="chart" style="height:320px"></div><div class="note">{S["seg_note"]}</div></div>\n</section>\n')
    # ② 短缺检验
    w(f'<section id="test" data-nav="c"><div class="kicker">② 短缺检验 · 凭什么说"缺"</div><h2>四个信号排出来的约束顺序</h2>\n<p class="sub">{S["test_rule"]}</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>#</th><th>环节</th><th>价格</th><th>交期</th><th>配额</th><th>稼动率</th><th>得分</th><th>判定</th></tr></thead><tbody>')
    for r in S['test']:
        w(f'<tr><td>{r[7]}</td><td><b>{r[0]}</b></td><td data-l="价格">{r[1]}</td><td data-l="交期">{r[2]}</td><td data-l="配额">{r[3]}</td><td data-l="稼动率">{r[4]}</td><td class="num" data-l="得分">{r[5]}</td><td class="st {stcls(r[6])}" data-l="判定">{r[6]}</td></tr>')
    w(f'</tbody></table></div>\n<p class="note">{S["test_note"]}</p>\n</section>\n')
    # ③ 机制 + 价格分解
    w('<section id="mech" data-nav="c"><div class="kicker">③ 机制入门 · 一块板怎么做出来，每种材料管什么</div><h2>为什么 AI 板难做、材料会卡</h2>\n')
    w('<div class="flowp">' + '<i>→</i>'.join(f'<span>{x}</span>' for x in S['flow']) + '</div>\n')
    w('<div class="tbl"><table class="stack"><thead><tr><th>材料 / 工序</th><th>管什么</th><th>AI 板为什么难</th></tr></thead><tbody>' + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in S['mech']) + '</tbody></table></div>\n')
    w(f'<div class="card" id="price" style="margin-top:12px"><b>价格分解：为什么"涨了"却不"缺"</b><p style="margin:.4em 0 0;font-size:15px">{S["pricebox"]}</p></div>\n')
    w(f'<p class="note">{S["terms"]}</p>\n</section>\n')
    # ④ 三条核心判断
    w('<section id="claims" data-nav="c"><div class="kicker">④ 三条核心判断 · 每条都写了"若我错，你会看到什么"</div><h2>少而硬：三条判断</h2>\n<div class="grid g3">')
    for i, c in enumerate(S['claims'], 1):
        w(f'<div class="card cl"><div class="jid">判断 {i} · {c["id"]} · 检查日 {c["due"]}</div><p style="margin:.3em 0;font-size:16px"><b>{c["t"]}</b></p><div class="note">依据：{c["ev"]}</div><div class="wr"><b>若我错，你会看到：</b>{c["wrong"]}</div></div>')
    w('</div>\n<p class="note">J6–J8 的阈值和当前读数在<a href="#wrong">可能错在哪</a>里跟踪；触发就改判断，不辩护。</p>\n</section>\n')
    # ⑤ AI 下钻
    w(f'<section id="ai" data-nav="c"><div class="kicker">⑤ AI 下钻 · 行业地图里"18 层以上 / AI HDI / 载板"三行的细节</div><h2>{S["ai_h"]}</h2>\n<p class="sub">{S["ai_sub"]}</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>环节</th><th>预测口径（2027 满足率，模型）</th><th>可观测信号（得分）</th><th>判定</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="预测">{b}</td><td data-l="可观测">{c}</td><td class="st {stcls(d)}" data-l="判定">{d}</td></tr>' for a, b, c, d in S['ai_tbl']) + '</tbody></table></div>\n')
    w('<div class="kl">' + ''.join(f'<a href="#a{i}"><span class="i">{CIRC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>' for i, a in enumerate(args, 1)) + '</div>\n</section>\n')

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
        argsec(i, a, 'a', CIRC, 'e', 'AI 下钻 · 论点', lambda st: st)
    if cn:
        w(f'<section id="cn" data-nav="c" class="cnsec"><div class="kicker">AI 下钻 · 平行账本 · {cn["kicker"]}</div>\n<div class="scqa">')
        for lab, txt in zip(('背景', '冲突', '问题'), cn['scqa']):
            w(f'<div><b>{lab}</b><span>{txt}</span></div>')
        w(f'</div>\n<h2 class="gov">{cn["gov"]}</h2>\n<div class="kl cn">')
        for i, a in enumerate(cn['args'], 1):
            w(f'<a href="#c{i}"><span class="i">{CNC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>')
        w(f'</div>\n<p class="note">{cn["mece"]}</p>\n</section>\n')
        for i, a in enumerate(cn['args'], 1):
            argsec(i, a, 'c', CNC, 'ce', '中国论点', lambda st: 'cn-' + st)
    # ⑥ 一线校验
    w(f'<section id="check" data-nav="c"><div class="kicker">⑥ 一线校验 · 问题保持开放</div><h2>业内问题：暂无内部答案，改由公开数据每周五跟踪</h2>\n<p class="sub">{S["check_sub"]}</p>\n')
    w('<div class="tbl"><table class="hm stack"><thead><tr><th>问题</th><th>公开替代数据</th><th>频率</th><th>判读阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody>'
      + ''.join(f'<tr><td><b>{a}</b></td><td data-l="数据">{b}</td><td data-l="频率">{c}</td><td data-l="阈值">{d}</td><td data-l="当前">{e}</td><td><span class="pill">开放 · 待答</span></td></tr>' for a, b, c, d, e in S['checks']) + '</tbody></table></div>\n</section>\n')
    # ⑦ 可能错在哪 ⑧ 预测台账
    w(f'<section id="wrong" data-nav="c"><div class="kicker">⑦ 我们可能错在哪 · 底稿第 1/11 步</div>\n<h2>每条判断都写好了"什么情况算我错"</h2>\n{S["wrong"]}\n</section>\n')
    w(f'<section id="pred" data-nav="c"><div class="kicker">⑧ 预测台账 · 底稿第 11 步</div><h2>写下来，到期打分</h2>\n{S["pred"]}\n</section>\n')
    # ⑨ 底稿（折叠）
    w(f'<section id="base" data-nav="b" class="apxsec"><div class="kicker">⑨ 底稿 · SOP 13 步完整产业链分析（默认折叠，点开或点任一"底稿 ↓"链接自动展开）</div>\n'
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
    # ⑩ 读后五问
    w('<section id="quiz" data-nav="c"><div class="kicker">⑩ 读后五问 · 先自己答，再点开对答案</div><h2>你能回答这五个问题吗？</h2>\n'
      + ''.join(f'<details class="card qd"><summary>Q{i} {q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(S['quiz'], 1)) + '\n</section>\n')
    w(f'<section id="apx" data-nav="b" class="apxsec"><div class="kicker">附录</div>\n'
      f'<details class="apx" id="apxSrc"><summary>来源与局限 <small>{S["src_small"]}</small></summary><div class="body" id="src">{S["src"]}</div></details>\n'
      f'<details class="apx" id="apxLog"><summary>更新记录与下载 <small>每次改判都记在这里 · 旧版 v1 存档可对比</small></summary><div class="body" id="log">{S["log"]}</div></details>\n</section>\n')
    w(f'</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="{S["archive"][0]}">旧版 v1 存档</a> · <a href="{S["other"][0]}">{S["other"][1].replace(" ⇄","")}</a></footer>\n')
    w(''.join(f'<script src="{x}"></script>' for x in ['ledger_ids.js', 'chain.js'] + S['scripts']) + '\n')
    w('<script>document.getElementById("baseD").addEventListener("toggle",function(){if(this.open&&window.redraw)setTimeout(window.redraw,30)});</script>\n</body></html>\n')
    html = ''.join(o)
    assert not re.search(r'<a\b(?:(?!</a>).)*<a\b', html, re.S), f'{S["file"]}: 有嵌套 <a>'
    ids = re.findall(r'\bid="([^"]+)"', html)
    dup = {x for x in ids if ids.count(x) > 1}
    assert not dup, f'{S["file"]}: 重复 id {dup}'
    miss = {h for h in re.findall(r'href="#([\w-]+)"', html) if h not in ids and not re.match(r'src\d+$', h)}
    assert not miss, f'{S["file"]}: 锚点不存在 {miss}'
    return html
