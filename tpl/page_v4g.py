"""链条 5 页模板（v4）的通用渲染：HBM / CoWoS / 铜（2026-10-28 起）。外壳、导航、组装全部复用 tpl/page_v4.py，和 PCB 同一套。
内容一个字不删，只搬家：逻辑层、结论层（论点、中国账本、可能错在哪、预测台账）、13 步底稿，全部来自 <链>/page.py 的 SPEC / LOGIC；
页面怎么分（哪一块放哪一页、节标题）写在 SPEC['v4']；总览的三个信号灯在 <链>/page.py 里按 data/<链>.json 现算。
  ① 总览 <链>.html          主要矛盾、一分钟看懂、五句话、一张图看懂 + 主图、三个信号、什么会证明我们错
  ② 格局与钱在哪赚 -pattern   工艺、利润池、玩家、公司图谱、价格论点、中国账本
  ③ 周期与产能 -cycle         需求、供给、平衡、约束、历史、领先指标 + 量 / 时点论点
  ④ 主要矛盾追踪 -track       和主流差在哪、判断、盯什么、要害变量、争议、可能错在哪、预测台账
  ⑤ 底稿与数据 -data          13 步索引、名词、怎么读、下载、来源与局限
旧网址 <链>.html#旧锚点 → 自动跳到新页；版本说明在 changelog.html#cl-<链>。"""
import json, os, re
import page_v4 as V4
A = V4.A
R0 = V4.R0
LBL = V4.LBL
nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)
untag = lambda t: re.sub(r'<[^>]+>', '', t)
LT = {'r': '红灯', 'y': '黄灯', 'g': '绿灯', 'x': '灰灯'}


def gloss_items(terms):
    """逻辑层「名词：A = …；B = …」→ [(词, 解释, '')]。"""
    t = re.sub(r'^\s*名词[：:]\s*', '', terms.strip()).rstrip('。')
    out = []
    for part in re.split(r'；', t):
        if '=' not in part:
            continue
        k, v = part.split('=', 1)
        out.append((untag(k).strip(), v.strip(), ''))
    return out


def render_v4g(S, STEPS, SID, MID, CIRC, CNC, key, flow):
    V4.use(key)
    C, L, cn, args = S['v4'], S['logic'], S['cn'], S['args']
    CHAIN = V4.CHAIN
    J = json.load(open(os.path.join(R0, 'data', f'{key}.json'), encoding='utf-8'))
    T = {int(s['id']): s['t'] for s in J['sources']}
    fig = lambda *a, **k: A.figure(*a, titles=T, **k)
    more = lambda *a, **k: A.more(*a, titles=T, **k)
    stp = {s['id']: s for s in S['steps']}
    back = {s[0]: [] for s in STEPS}
    cback = {s[0]: [] for s in STEPS}
    for i, a in enumerate(args, 1):
        for j, e in enumerate(a['ev'], 1):
            for s_ in e['steps']:
                back[s_].append((i, j))
    for i, a in enumerate(cn['args'], 1):
        for j, e in enumerate(a['ev'], 1):
            for s_ in e['steps']:
                cback[s_].append((i, j))
    assert [s['id'] for s in S['steps']] == [s[0] for s in STEPS], '底稿必须按 SOP 13 步顺序给全'
    P1, P2, P3, P4, P5 = [p[0] for p in V4.PAGES]
    H1 = C['h1']
    SECS = []
    placed = []

    def sec(page, sid, title, lead='', cls='ch'):
        assert len(title) <= 15, f'节标题超过 15 字：{title}'
        SECS.append(dict(page=page, id=sid, title=title, lead=lead, body=[], cls=cls))

    def w(x):
        SECS[-1]['body'].append(x)

    def argsec(i, a, pre, circ, evp, lab, link, collapse=False):
        steps_cov = sorted({SID[s_][1] for e in a['ev'] for s_ in e['steps']}, key=int)
        o = [f'<div id="{pre}{i}" class="arg{" cnarg" if pre == "c" else ""}"><div class="kicker">{lab} {circ[i-1]} · {a["tag"]} · 依据底稿第 {"/".join(steps_cov)} 步{"中国块" if pre == "c" else ""}</div>\n<h3 class="claim">{a["claim"]}</h3>\n']
        if a.get('sub'):
            o.append(f'<p>{a["sub"]}</p>\n')
        h = a['hero']
        o.append(fig(f'f-{pre}{i}', h['t'], f'<div id="m-{h["src"]}" data-mirror="{h["src"]}" class="chart" style="height:{h.get("h", 340)}px"></div>',
                     h['note'], extra=f'<a href="#{link(h["step"])}">原图与假设在底稿第 {SID[h["step"]][1]} 步{"中国块" if pre == "c" else ""} ↓</a>'))
        ev = ''
        for j, e in enumerate(a['ev'], 1):
            lk = ' · '.join(f'<a href="#{link(s_)}">底稿 {SID[s_][1]} {SID[s_][3]}{" · 中国" if pre == "c" else ""} ↓</a>' for s_ in e['steps'])
            ev += f'<div class="evc" id="{evp}{i}-{j}"><div class="ev">证据 {i}.{j}</div><b>{e["t"]}</b><p>{e["b"]}</p><div class="go">{lk}</div></div>'
        o.append(more(f'{len(a["ev"])} 条证据：{" / ".join(nolink(e["t"]) for e in a["ev"])}', f'<div class="evs">{ev}</div>', small=f'{lab} {circ[i-1]}'))
        o.append('</div>\n')
        html = ''.join(o)
        if collapse:
            html = f'<details class="more wide argd"><summary><span>{lab} {circ[i-1]}</span><b>{nolink(a["claim"])}</b><small>含主证据图 · {len(a["ev"])} 条证据</small></summary><div class="more-b">{html}</div></details>\n'
        w(html)

    def step(page, sid, title, open_=False):
        st = stp[sid]
        _, n, short, ttl = SID[sid]
        placed.append(sid)
        sub = st.get('sub', '')
        short_sub = sub and len(untag(sub)) <= 90
        sec(page, sid, title, lead=sub if short_sub else '')
        w(A.callout(st['h'], f'底稿第 {n} 步 · {MID[sid]}'))
        if back[sid]:
            w('<div class="sup">' + ''.join(f'<a href="#e{i}-{j}">支撑论点{CIRC[i-1]} · 证据 {i}.{j}</a>' for i, j in back[sid]) + '</div>\n')
        elif st.get('ctx'):
            w(f'<div class="sup"><span>{st["ctx"]}</span></div>\n')
        body = ('' if short_sub or not sub else f'<p class="sub">{sub}</p>\n') + st['body'].strip()
        w(more(f'{MID[sid]}：图表、数据与推导', body, small=f'底稿第 {n} 步', open_=open_, wide=True))
        if st.get('cn'):
            c = st['cn']
            ch = ''.join(f'<a href="#ce{i}-{j}">支撑中国论点{CNC[i-1]} · 证据 {i}.{j}</a>' for i, j in cback[sid])
            w(more(f'中国账本：{nolink(c["h"])}', f'<div class="cnb" id="cn-{sid}"><div class="cnh"><span class="lb">中国账本</span><b>{c["h"]}</b></div>' + (f'<div class="sup">{ch}</div>' if ch else '') + c['body'].strip() + '</div>', small='中国块', wide=True))

    def tbl(head_, rows, cls='stack'):
        return (f'<div class="tbl"><table class="{cls}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head_) + '</tr></thead><tbody>'
                + ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows) + '</tbody></table></div>')

    def custom(page, kind, title):
        if kind == 'arg':
            return
        if kind == 'cn':
            sec(page, 'cn', title, cn['kicker'])
            w(A.callout(cn['gov'], '中国账本的结论'))
            w('<div class="kl cn">' + ''.join(f'<a href="#c{i}"><span class="i">{CNC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>' for i, a in enumerate(cn['args'], 1)) + '</div>\n')
            w(more('中国账本的背景 / 冲突 / 问题', '<div class="scqa">' + ''.join(f'<div><b>{lab}</b><span>{txt}</span></div>' for lab, txt in zip(('背景', '冲突', '问题'), cn['scqa'])) + '</div>'))
            w(f'<p class="note">{cn["mece"]}</p>\n')
            for i, a in enumerate(cn['args'], 1):
                argsec(i, a, 'c', CNC, 'ce', '中国论点', lambda s_: 'cn-' + s_, collapse=True)
        elif kind == 'diff':
            sec(page, 'diff', title, S.get('cons_sub', '左边是券商、研究机构、媒体的公开说法（带来源）；“差距”一栏就是预期差。'))
            w('<ol class="wt">' + ''.join(f'<li><b>{r[2]}</b><span>我们：{r[1]}</span></li>' for r in L['cons']) + '</ol>\n')
            w(more('主流观点 vs 我们：全表（主流、我们、差距、证据、什么能确认）', tbl(['主流观点', '我们', '差距', '证据', '什么能确认'], L['cons'], 'stack cons'), small=f'{len(L["cons"])} 行', wide=True))
            w(more('结论层的背景 / 冲突 / 问题', '<div class="scqa">' + ''.join(f'<div><b>{lab}</b><span>{txt}</span></div>' for lab, txt in zip(('背景', '冲突', '问题'), S['scqa'])) + '</div>'))
        elif kind == 'claims':
            sec(page, 'claims', title)
            w(A.callout(S['gov'], '中心思想'))
            w('<div class="kl">' + ''.join(f'<a href="#a{i}"><span class="i">{CIRC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>' for i, a in enumerate(args, 1)) + '</div>\n')
            w('<div class="twoled">' + ''.join(f'<a href="#{h}" class="{c}"><span class="lb">{lb}</span><span>{nolink(t)}</span></a>' for h, c, lb, t in S['ledgers']) + '</div>\n')
            w(f'<p class="note">{S["mece"]}</p>\n')
        elif kind == 'watch':
            sec(page, 'watch', title, '每一项都写好了阈值和日期：越线就改判断，不辩护。总览的三个信号灯取自这里。')
            w('<div class="tbl"><table class="stack watch"><thead><tr><th>盯什么</th><th>指标</th><th>阈值 → 含义</th><th>日期</th></tr></thead><tbody>'
              + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td style="white-space:nowrap">{d}</td></tr>' for a, b, c, d in L['watch']) + '</tbody></table></div>\n')
        elif kind == 'wrong':
            sec(page, 'wrong', title, '每条论点都写好了“什么情况算我错”，触发阈值就改判断。')
            w(more('证伪表：判断、反方证据、证伪条件、观察指标与阈值、当前读数', S['wrong'], small='全球 J + 中国 CJ', wide=True))
        elif kind == 'pred':
            sec(page, 'pred', title, '写下来，到期按公开数据打分，不改原文，只追加结果。')
            w(more('预测台账：全部预测与到期打分', S['pred'], small='P / T / C 系列', wide=True))
        else:
            raise SystemExit(f'未知块 {kind}')

    # ======================= ① 总览 =======================
    upd = re.search(r'<span id="[\w-]*upd"[^>]*>.*?</span>', S['kicker']).group(0)
    sec(P1, 'top', '一分钟看懂', cls='hero')
    w(f'<div class="kicker">{CHAIN} 研究 · 第 1 页 / 共 5 页 · 数据更新 {upd}</div>\n<h1>{H1}</h1>\n')
    w(f'<p class="howto">怎么读：先看“一分钟看懂”，再看五句话和一张图；想知道怎么盯、什么算我们错，看下面的三个信号。小号上标数字是来源，点一下就能看。看不懂的词查<a href="{P5}#gloss">名词小白版</a>。公开数据整理，<b>不构成投资建议</b>。</p>\n')
    assert len(C['one_min']) == 5
    assert [k for k, _ in C['one_min']] == ['是什么', '钱在哪', '最大风险', '盯什么', '什么算我们错']
    w(A.one_min([t for _, t in C['one_min']]))
    sec(P1, 'ov5', '五句话说清楚')
    w('<ol class="ov5">' + ''.join(f'<li>{LBL[k]}{t}</li>' for k, t in C['ov5']) + '</ol>\n')
    w(f'<p class="note">完整的判断、论点和两本账对照在<a href="{P4}#claims">主要矛盾追踪</a>。</p>\n')
    sec(P1, 'ov-fig', '一张图看懂')
    w('<div class="card"><div class="keys">' + ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in L['keys']) + f'</div>{flow(L["fig"])}<div class="note">{L["fig_note"]}</div></div>\n')
    ai, ot = C['ov_fig']
    sec(P1, 'ov-cap', ot)
    h = args[ai - 1]['hero']
    w(fig('f-ov', h['t'], f'<div id="m-ov-{h["src"]}" data-mirror="{h["src"]}" class="chart" style="height:{h.get("h", 340)}px"></div>', h['note'],
          extra=f'<a href="#a{ai}">论点{CIRC[ai-1]}和证据 →</a>'))
    sec(P1, 'ov-sig', '盯哪三个信号？')
    assert len(C['sig']) == 3
    w('<ol class="sig3">' + ''.join(f'<li class="{c}"><i class="lt" aria-hidden="true"></i><div><b>{t}</b><span><i class="k">现在</i>{now}</span><span><i class="k">警戒线</i>{th}</span><span class="st">{LT[c]} · {s}</span></div></li>' for c, t, now, th, s in C['sig']) + '</ol>\n')
    w(f'<p class="note">{LBL["j"]}灯色是代码按警戒线现算的：红 = 已越过警戒线；绿 = 还没触发；灰 = 还没到公布日或没有可靠公开数据。警戒线原样取自<a href="{P4}#watch">我们重点盯什么</a>，没有改。{C.get("sig_note", "")}</p>\n')
    sec(P1, 'prove', '什么会证明我们错？')
    w('<ol class="wt">' + ''.join(f'<li><b>{r[2]}</b><span>{r[4]}</span></li>' for r in L['cons'][:3]) + '</ol>\n')
    w(f'<p class="note">每条论点的证伪表在<a href="{P4}#wrong">主要矛盾追踪</a>。</p>\n')
    w(f'<a class="ov-next" href="{P2}">下一页：格局与钱在哪赚 →</a>\n')

    # ======================= ②③④ 按 SPEC['v4']['pages'] 摆 =======================
    for page, items in zip((P2, P3, P4), (C['pattern'], C['cycle'], C['track'])):
        for it in items:
            if it[0] == 'step':
                step(page, it[1], it[2], open_=len(it) > 3 and it[3])
            elif it[0] == 'arg':
                sec(page, f'arg{it[1]}', it[2], it[3] if len(it) > 3 else '')
                argsec(it[1], args[it[1] - 1], 'a', CIRC, 'e', '论点', lambda s_: s_)
            else:
                custom(page, it[0], it[1])
    miss = [s[0] for s in STEPS if s[0] not in placed]
    assert not miss, f'{key}: 底稿步骤没放进任何一页 {miss}'

    # ======================= ⑤ 底稿与数据 =======================
    sec(P5, 'base', '底稿怎么读？', S['base_sub'])
    PG = {p[0]: p[2] for p in V4.PAGES}
    home_of = {s['id']: s['page'] for s in SECS}
    w('<ol class="stepix">' + ''.join(
        f'<li><a href="#{s[0]}"><span class="n">{s[1]}</span>{MID[s[0]]}<span class="s">{"".join(CIRC[i-1] for i in sorted({i for i, _ in back[s[0]]}))}'
        + (' <i class="cnm">中</i>' if stp[s[0]].get('cn') else '') + f' · {PG[home_of[s[0]]]}</span></a></li>' for s in STEPS) + '</ol>\n')
    w(f'<p class="note">13 步底稿按主题分到了第 2–4 页：工艺、利润、玩家、图谱在“格局”；需求、供给、平衡、约束、历史、领先指标在“周期”；要害变量、争议、台账在“追踪”。每步的图表、滑块和推导都在该节的“展开细节”里。圆圈 = 这一步支撑哪条论点，“中” = 有中国块。</p>\n')
    sec(P5, 'words', '这些词什么意思？')
    E = '<span class="tag t-est">估</span>'
    w(f'<p class="howto">怎么读这套页面：五页从“总览”往下展开到“底稿”，每节先一句导语、一句判断，细表收在“展开细节”里。正文里的小号上标数字是来源编号，点一下看来源，全部列在本页<a href="#src">来源与注释</a>；每段最多留 1 个上标，其余在每章末尾的“本章来源”。'
      f'图表下方一行灰字是这张图的来源。{E} = Kiko 自估，可在底稿里用滑块改。P / T / C / J 编号链接到<a href="ledger.html">总账</a>。'
      '段首小标签：<span class="fj f">事实</span> = 能查到出处的数或事；<span class="fj j">判断</span> = 我们的推断或估计。公开数据整理，<b>不构成投资建议</b>，不对任何个股给买卖意见。</p>\n')
    gi = gloss_items(L['terms'])
    assert len(gi) >= 3, f'{key}: 名词表解析失败'
    w(A.glossary(gi))
    lm = re.match(r'\s*(<div class="tbl"><table id="[\w-]+"><tbody></tbody></table></div>)\s*(.*)$', S['log'], re.S)
    assert lm, f'{key}: SPEC["log"] 结构变了'
    w(f'<p class="note">下载与构建：{re.sub(r"^<p>|</p>$", "", lm.group(2).strip())}</p>\n')
    sec(P5, 'apx', '数字从哪来？', f'正文上标数字 = 下面的来源编号（本链统一编号，图表下方的“来源”行用同一套编号）。')
    w(f'<details class="apx" id="apxSrc"><summary>来源列表与局限 <small>{S["src_small"]}</small></summary><div class="body" id="src">{S["src"]}</div></details>\n')

    # ---------------- 组装
    stub = f'<div hidden id="ch-stub">{lm.group(1)}</div>'
    V4.ALIAS.update({'logic': P1, 'nav': P1})
    out, STAT, home_js = V4.assemble(SECS, T, H1, title0=C['title0'], desc0=untag(S['gov']), stub=stub,
                                     scripts=''.join(f'<script src="{x}"></script>' for x in ['ledger_ids.js', 'chain.js'] + S['scripts'] + ['assets/reading.js']),
                                     tail='', foot=f'<a href="{S["other"][0]}">{S["other"][1].replace(" ⇄", "")}</a>')
    render_v4g.STAT = STAT
    nm = {p[0]: p[2] for p in V4.PAGES}
    old = {'top': '页眉', 'ov5': '逻辑层·三问三答', 'ov-fig': '逻辑层·一张图', 'ov-cap': '论点主图', 'ov-sig': '逻辑层·重点盯什么', 'prove': '逻辑层·主流 vs 我们',
           'diff': '逻辑层·主流 vs 我们 + 结论层 SCQA', 'claims': '结论层·中心思想 / 两本账 / 论点卡', 'watch': '逻辑层·重点盯什么', 'wrong': '结论层·可能错在哪',
           'pred': '结论层·预测台账', 'cn': '结论层·中国账本', 'base': '底稿说明', 'words': '逻辑层·名词 + 下载', 'apx': '来源与局限'}
    old.update({f'arg{i}': f'论点{CIRC[i-1]} #a{i}' for i in range(1, len(args) + 1)})
    old.update({s[0]: f'底稿第 {s[1]} 步 {MID[s[0]]}' for s in STEPS})
    C = dict(C, moved=[f'<b>{nm[p]}</b>（<a href="{p}">{p}</a>）：' + '；'.join(f'{old.get(x["id"], x["id"])} → {x["title"]}' for x in SECS if x['page'] == p)
                       for p in nm] + ['更新记录表 → 本页“逐版记录”。'])
    render_v4g.CL = changelog_secs(S, J, key, C)
    return out


def changelog_secs(S, J, key, C):
    V4.use(key)
    CH, P = V4.CHAIN, V4.PAGES
    kick = re.sub(r'\s*·\s*更新 <span id="[\w-]*upd"[^>]*>.*?</span>', '', S['kicker'])
    secs = [
        (f'cl-{key}', f'{CH} 现在是哪一版？',
         f'<p>{S["pill"]} → 2026-10-28 拆成 5 页（{" / ".join(f"<a href=\"{f}\">{t}</a>" for f, t, _, _ in P)}）。原页眉：{kick}。判断、概率、模型数字都没改。</p>'),
        (f'log-{key}', f'{CH} 逐版记录', V4.log_table(J) + '<p class="note">已入账判断、概率和模型数字只在 John 确认后改，每次改都在这里留一行。</p>'),
        (f'old-{key}', f'{CH} 旧网址去哪了',
         f'<ul><li>2026-10-28：原来一页（逻辑层 + 结论层 + 13 步底稿）拆成 5 页。旧网址 <code>{P[0][0]}#锚点</code> 仍可用，会自动跳到新页的同一块；<code>#log</code> 跳到本页。</li>'
         + ''.join(f'<li>{x}</li>' for x in C['moved']) + '</ul>'),
    ]
    return [(i, t, re.sub(r'href="#(src\d+)"', rf'href="{V4.DATA_PAGE}#\1"', h)) for i, t, h in secs]
