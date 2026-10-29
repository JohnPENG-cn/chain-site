"""链条模板 v4（2026-10-27 起 PCB 用；2026-10-28 起 HBM / CoWoS / 铜 也用，见 tpl/page_v4g.py 与 docs/CHAIN_TEMPLATE.md）。
一条链 = 5 页，同一外壳：
  ① 总览（pcb.html）           主要矛盾、五句话、一张主图、三个信号红绿灯、什么会证明我们错
  ② 格局与钱在哪赚（pcb-pattern）  产业地图 → 利润池 → 议价力 → 打分卡 → 中国 vs 海外
  ③ 周期与产能（pcb-cycle）      扩产 → 现在缺什么 → 约束 → 需求与技术 → 替代
  ④ 主要矛盾追踪（pcb-track）     要点版、核心判断、指标、待 John 确认 X1–X8、证伪与台账、一线校验、数据缺口
  ⑤ 底稿与数据（pcb-data）       13 步底稿（拖动模型、对账）、读后五问、名词、怎么读、下载、来源与注释
  + 更新记录（changelog.html）：版本说明、并入说明、旧版链接都在这里，内容页不留。
内容一个字不删，只搬家：所有块仍来自 pcb/page.py SPEC + pcb/research.py + pcb/map.py（同 tpl/page_v3.py），数字全部由代码现算。
实现要点：
  - pcb.js / chain.js 会找固定 id 画图、填表。每页把“别的页的块”原样放进 main 外面的隐藏容器 #ch-shadow（hidden + inert），
    JS 照常跑、镜像图照常复制，读者看不到；字数、脚注、版面检查都只算 main。
  - 页内 #id 链接若指向别的页的块，构建时改成 那一页.html#id；JS 后渲染出来的这类链接由 reading.js 运行时改道（window.CH_HOME）。
  - 旧网址：pcb.html#旧锚点 → 自动跳到新页（head 里的跳转脚本 + CH_HOME）；pcb-map.html 仍跳 pcb.html#…，再转一次。
  - 每段最多 1 个脚注上标（留第一个，一般就是关键数字的来源）；其余收进每章末尾折叠的「本章来源」，完整列表在底稿页「来源与注释」。
  - 段落标签：事实 / 判断，规则见 docs/CHAIN_TEMPLATE.md §4。"""
import json, os, re, statistics as st, sys
from bs4 import BeautifulSoup, NavigableString
import page_v3 as V3
R, SRCM, PM, A = V3.R, V3.SRCM, V3.PM, V3.A
SIG, stcls = V3.SIG, V3.stcls
R0 = V3.R0

# ---------------- 站点导航配置（以后加链条只改这里）
PG5 = [('总览', '总览'), ('格局与钱在哪赚', '格局'), ('周期与产能', '周期'), ('主要矛盾追踪', '追踪'), ('底稿与数据', '底稿')]
SUFFIX = ['', '-pattern', '-cycle', '-track', '-data']


def _pages(key, ds):
    return [(f'{key}{x}.html', t, s, d) for x, (t, s), d in zip(SUFFIX, PG5, ds)]


CHAINS = [  # (键, 名称, 5 页 (文件, 页名, 短名, 一句话), 链内附加链接) —— 导航顺序 = 上下游顺序
    ('hbm', 'HBM', _pages('hbm', ['主要矛盾一页看懂', '工序、利润池、谁说了算', '需求、供给、约束', '判断、信号、台账', '给想核数的人']),
     [('原理图：HBM 怎么叠', 'explain-hbm.html')]),
    ('cowos', 'CoWoS', _pages('cowos', ['主要矛盾一页看懂', '工序、利润池、谁说了算', '需求、产能、约束', '判断、信号、台账', '给想核数的人']),
     [('原理图：CoWoS 怎么封', 'explain-cowos.html')]),
    ('pcb', 'PCB', _pages('pcb', ['主要矛盾一页看懂', '地图、利润池、谁说了算', '扩产潮、约束、需求', '判断、指标、待确认', '给想核数的人']),
     [('原理图：PCB 怎么做', 'explain-pcb.html')]),
    ('cu', '铜', _pages('cu', ['主要矛盾一页看懂', '环节、利润池、谁说了算', '需求、矿山、缺口与价格', '判断、信号、台账', '给想核数的人']), []),
    # HDD v0.1 只有 1 页（hdd/build.py 生成），待补较多；以后补满 5 页再换成 _pages('hdd', …)
    ('hdd', 'HDD', [('hdd.html', '一页总览（待补较多）', '总览', '原理、格局、A 股映射、待补与待确认')],
     [('原理图：硬盘怎么存', 'explain-hdd.html')]),
]
CFG = {c[0]: c for c in CHAINS}
SITE = [('总账', 'ledger.html'), ('日报', 'daily/'), ('原理图', 'explain.html'), ('更新记录', 'changelog.html')]
KEY = CHAIN = PAGES = DATA_PAGE = ALIAS = None


def use(key):
    """切到某条链：导航、底稿页、旧锚点去处都按这条链来。"""
    global KEY, CHAIN, PAGES, DATA_PAGE, ALIAS, SRC_NOTE
    KEY, CHAIN, PAGES = key, CFG[key][1], CFG[key][2]
    SRC_NOTE = 'pcb/page.py + pcb/research.py + pcb/map.py' if key == 'pcb' else f'{key}/page.py + tpl/page_v4g.py'
    DATA_PAGE = PAGES[-1][0]
    # 旧锚点 → 现在没有同名块的去处（值里带 # 就原样跳，不再拼 #id）
    ALIAS = {'log': 'changelog.html', 'apxLog': 'changelog.html'} if key == 'pcb' else {'log': f'changelog.html#log-{key}', 'apxLog': f'changelog.html#log-{key}'}


SRC_NOTE = None
use('pcb')

CSS4 = '''<style>
.ov5{list-style:none;padding:0;margin:12px 0;display:grid;gap:8px}.ov5 li{background:var(--card);border-radius:var(--r-card);padding:12px 14px;font-size:16px;line-height:1.65}
.fj{display:inline-block;font-size:11.5px;font-weight:700;line-height:1;padding:3px 6px;border-radius:5px;margin-right:6px;vertical-align:2px;letter-spacing:.02em}
.fj.f{background:var(--hig-tint-fill);color:var(--tint)}.fj.j{background:var(--hig-warn-fill);color:var(--warn)}
.sig3{list-style:none;padding:0;margin:12px 0;display:grid;gap:8px}.sig3 li{display:flex;gap:12px;background:var(--card);border-radius:var(--r-card);padding:12px 14px}
.sig3 .lt{flex:0 0 14px;height:14px;border-radius:50%;margin-top:5px;background:var(--mut)}.sig3 .r .lt{background:var(--hig-red)}.sig3 .y .lt{background:var(--warn)}.sig3 .g .lt{background:var(--ok)}
.sig3 b{display:block;font-size:16px}.sig3 span{display:block;font-size:14.5px;line-height:1.6}.sig3 .k{color:var(--mut);font-size:12px;font-weight:600;margin-right:4px;display:inline}
.sig3 .st{font-weight:600}.sig3 .r .st{color:var(--hig-tx-red)}.sig3 .g .st{color:var(--hig-tx-green)}.sig3 .y .st{color:var(--warn)}
.pg-steps{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 4px}.pg-steps a{display:flex;gap:5px;align-items:baseline;font-size:13px;text-decoration:none;color:var(--mut);background:var(--hig-fill);border-radius:999px;padding:5px 10px;min-height:20px}
.pg-steps a b{font-size:11px;font-variant-numeric:tabular-nums}.pg-steps a.on{background:var(--tint);color:#fff}.pg-steps a.on b{color:#fff}
.pg-pn{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:36px 0 12px}.pg-pn a{display:block;background:var(--card);border-radius:var(--r-card);padding:12px 14px;text-decoration:none;color:var(--fg);box-shadow:var(--hig-shadow);min-width:0}
.pg-pn a.nx{text-align:right;grid-column:2}.pg-pn small{display:block;color:var(--mut);font-size:12px}.pg-pn b{font-size:15px;overflow-wrap:anywhere}
.ov-next{display:block;text-align:center;font-weight:600;margin:18px 0 0}
.chsrc ol{margin:0;padding-left:0;list-style:none}.chsrc li{font-size:13.5px;line-height:1.55;margin:0 0 4px;overflow-wrap:anywhere}.chsrc li a{font-variant-numeric:tabular-nums;margin-right:6px}
.forwho{display:inline-block;background:var(--hig-gray-fill);border-radius:6px;font-size:12.5px;font-weight:600;padding:3px 8px;margin:4px 0 8px}
.sn a.pg-x{font-size:13px;padding:5px 8px;color:var(--mut)}.sn a.pg-x b{font-size:11px}
.xr{white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:600}
#ch-shadow{display:none!important}
.cl-log td{font-size:14px;line-height:1.6;vertical-align:top}.cl-log td:first-child{white-space:nowrap}
</style>
'''

LBL = {'f': '<span class="fj f">事实</span>', 'j': '<span class="fj j">判断</span>'}
# 判断用词：出现任一个就标“判断”（估算标签 t-est 也算）。其余带数字或来源上标的段落标“事实”；都没有（操作说明、过渡句）不标。
JWORDS = ('估', '我们', '本页', '判断', '可能', '大概', '更像', '预计', '看不出', '推断', '意味', '提议', '如果', '若', '应该', '倾向', '未必', '不一定', '说明', '更可能', '恐怕', '风险', '经验')
NOLBL = {'note', 'lead', 'sub', 'howto', 'kicker', 'dek', 'src-line', 'plain', 'fig-c', 'cl-t', 'wr', 'fn-t', 'ax'}
BLOCK = ('p', 'li', 'dd', 'dt', 'td', 'th', 'figcaption', 'h1', 'h2', 'h3', 'h4', 'summary', 'blockquote')


def classify(el):
    t = el.get_text()
    if el.find(class_='t-est') or any(x in t for x in JWORDS):
        return 'j'
    if re.search(r'\d', t) or el.find('sup', class_='fn'):
        return 'f'
    return None


def label_and_limit(html, keep_lbl=True):
    """一段 html（某一页看得见的一节）：① 给段落贴 事实/判断 标签；② 每段只留第一个脚注上标。返回 (html, 本节引用的全部来源号, 贴了几个标签)。"""
    soup = BeautifulSoup(html, 'html.parser')
    refs = []
    for a in soup.find_all('a', href=True):
        m = re.search(r'#src(\d+)$', a['href'])
        if m and a['href'].split('#')[0] in ('', DATA_PAGE) and int(m.group(1)) not in refs:
            refs.append(int(m.group(1)))
    nl = 0
    if keep_lbl:
        for p in soup.find_all('p'):
            cls = set(p.get('class') or [])
            if cls & NOLBL or p.find_parent(['table', 'aside']) or p.find_parent(class_=['onemin', 'ov5', 'fq', 'sig3', 'bluf', 'pull', 'chsrc']):
                continue
            if p.find(class_='fj'):
                continue
            k = classify(p)
            if k:
                p.insert(0, BeautifulSoup(LBL[k], 'html.parser'))
                nl += 1
    seen = {}
    for a in soup.select('sup.fn a.fn-a'):
        if a.find_parent(class_='src-line') or a.find_parent(class_='chsrc'):
            continue
        blk = a.find_parent(BLOCK) or a.find_parent('div')
        key = id(blk)
        if key in seen:
            sup = a.parent
            a.decompose()
            if not sup.find('a'):
                sup.decompose()
        else:
            seen[key] = 1
    return str(soup), refs, nl


def relink(m, pf, home):
    """页内锚点：家在别的页 → 那一页.html#id；来源号 srcN 的家是底稿页。"""
    i = m.group(1)
    h = DATA_PAGE if re.match(r'src\d+$', i) else home.get(i, pf)
    return m.group(0) if h == pf else (f'href="{h}"' if '#' in h else f'href="{h}#{i}"')


def chsrc(refs, T, page):
    if not refs:
        return ''
    href = '#src' if page == DATA_PAGE else DATA_PAGE + '#src'
    lis = ''.join(f'<li><a href="{href}{n}">{n}</a>{T.get(n, "")}</li>' for n in refs)
    return (f'<details class="more chsrc"><summary><span>来源</span><b>本章来源</b><small>{len(refs)} 条 · 每段只留 1 个上标，其余在这里</small></summary>'
            f'<div class="more-b"><ol>{lis}</ol><p class="note">完整列表与局限见<a href="{DATA_PAGE}#apx">底稿与数据 · 来源与注释</a>。</p></div></details>\n')


def nav_html(cur, secs_here=True, key=None):
    """固定导航树：四条链都是 5 页；当前链展开（含原理图），别的链收起。key=None（更新记录页）= 全部收起。"""
    key = KEY if key is None else key
    o = ['<nav class="rd-toc sn" id="rdToc" aria-label="站内导航"><div class="sn-h">链条</div>']
    for k, name, pages, extra in CHAINS:
        if k != key:
            o.append(f'<div class="sn-chain"><a class="sn-c" href="{pages[0][0]}"><b>{name}</b><span>{len(pages)} 页</span></a></div>')
            continue
        o.append(f'<div class="sn-chain on"><a class="sn-c" href="{pages[0][0]}"><b>{name}</b><span>{len(pages)} 页</span></a><ol class="sn-pg">')
        for i, (f, t, s, d) in enumerate(pages, 1):
            on = f == cur
            o.append(f'<li{" class=\"cur\"" if on else ""}><a href="{f}"{" aria-current=\"page\" class=\"pg on\"" if on else " class=\"pg\""}><b>{i}</b><span>{t}</span></a>'
                     + ('<div class="sn-here" id="snHere"></div>' if on and secs_here else '') + '</li>')
        for t, f in extra:
            o.append(f'<li class="sn-x"><a class="pg-x" href="{f}"><b>↗</b><span>{t}</span></a></li>')
        o.append('</ol></div>')
    o.append('<div class="sn-h">站内</div>' + ''.join(f'<a class="sn-s{" on" if f == cur else ""}" href="{f}">{n}</a>' for n, f in SITE) + '</nav>\n')
    return ''.join(o)


def steps_strip(cur):
    return (f'<nav class="pg-steps" aria-label="{CHAIN} 五页">' + ''.join(f'<a href="{f}"{" class=\"on\" aria-current=\"page\"" if f == cur else ""}><b>{i}</b>{s}</a>' for i, (f, t, s, d) in enumerate(PAGES, 1)) + '</nav>\n')


def prevnext(cur):
    fs = [p[0] for p in PAGES]
    i = fs.index(cur)
    o = '<nav class="pg-pn" aria-label="上一页 / 下一页">'
    if i > 0:
        o += f'<a class="pv" href="{PAGES[i-1][0]}"><small>← 上一页</small><b>{PAGES[i-1][1]}</b></a>'
    if i < len(PAGES) - 1:
        o += f'<a class="nx" href="{PAGES[i+1][0]}"><small>下一页 →</small><b>{PAGES[i+1][1]}</b></a>'
    return o + '</nav>\n'



def head(title, desc, extra_css, home_js, page):
    return (f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 tpl/page_v4.py（链条 5 页模板，见 docs/CHAIN_TEMPLATE.md）根据 {SRC_NOTE} 生成，不要手改；改内容请改这些文件后跑 ./build.sh -->
<title>{title} · 产业链情报研究中心</title><meta name="description" content="{desc}">{home_js}<link rel="stylesheet" href="assets.css"><script src="theme.js"></script>
<script src="vendor/echarts.min.js"></script><script src="assets/hig-echarts.js"></script>{extra_css}<link rel="stylesheet" href="assets/hig.css"></head>''')


def topbar(page_name, pill):
    return (f'<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="world/">世界</a>'
            f'<a class="btn" href="ledger.html">总账</a><a class="btn" href="changelog.html">更新记录</a><span class="pill">{pill}</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>\n'
            f'<div class="rd-bar" id="rdBar"><div class="rd-in"><button class="rd-cur" id="rdCur" aria-label="打开导航">{page_name}</button><span class="rd-pct" id="rdPct"></span></div><i class="rd-prog" id="rdProg"></i></div>\n')


def render_v4(S, STEPS, SID, MID, CIRC, CNC):
    """返回 {文件名: html}：5 个内容页 + changelog.html。"""
    args, cn = S['args'], S.get('cn')
    back = {s[0]: [] for s in STEPS}
    cback = {s[0]: [] for s in STEPS}
    for i, a in enumerate(args, 1):
        for j, e in enumerate(a['ev'], 1):
            for s_ in e['steps']:
                back[s_].append((i, j))
    if cn:
        for i, a in enumerate(cn['args'], 1):
            for j, e in enumerate(a['ev'], 1):
                for s_ in e['steps']:
                    cback[s_].append((i, j))
    assert [s['id'] for s in S['steps']] == [s[0] for s in STEPS], '底稿必须按 SOP 13 步顺序给全'
    assert len(S['claims']) <= 3 and len(S['quiz']) == 5 and 3 <= len(R.BLUF) <= 5
    nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)
    T = {SRCM.ID[k]: t for k, t, _ in SRCM.SRC}
    fig = lambda *a, **k: A.figure(*a, titles=T, **k)
    more = lambda *a, **k: A.more(*a, titles=T, **k)
    tbl = lambda head_, body, cls='hm stack': f'<div class="tbl"><table class="{cls}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head_) + f'</tr></thead><tbody>{body}</tbody></table></div>'
    capt, roict, t5t, finjs = V3.fin_tables()
    J = json.load(open(os.path.join(R0, 'data', 'pcb.json'), encoding='utf-8'))
    N = R.NUMS

    SECS = []   # dict(page, id, title, lead, body[list], cls, toc)

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
        if collapse:   # 整个论点（含主证据图）收进一个展开细节：summary 写论点本身
            html = f'<details class="more wide argd"><summary><span>{lab} {circ[i-1]}</span><b>{nolink(a["claim"])}</b><small>含主证据图 · {len(a["ev"])} 条证据</small></summary><div class="more-b">{html}</div></details>\n'
        w(html)

    P1, P2, P3, P4, P5 = [p[0] for p in PAGES]
    H1 = 'PCB：扩产潮能不能等到需求接住'

    # ======================= ① 总览 =======================
    sec(P1, 'top', '一分钟看懂', cls='hero')
    w(f'<div class="kicker">{CHAIN} 研究 · 第 1 页 / 共 5 页 · 数据更新 <span id="pcb-upd"></span></div>\n<h1>{H1}</h1>\n')
    w(f'<p class="howto">怎么读：先看“一分钟看懂”，再看五句话和一张图；想知道怎么盯、什么算我们错，看下面的三个信号。小号上标数字是来源，点一下就能看。看不懂的词查<a href="{P5}#gloss">名词小白版</a>。公开数据整理，<b>不构成投资建议</b>。</p>\n')
    w(A.one_min(R.ONE_MIN))
    w('<p class="note">先想知道一块 AI 服务器板是怎么做出来的（铜箔、玻纤布、树脂、层压、钻孔、HDI、M6→M9），看<a href="explain-pcb.html">PCB 原理图</a>：12 步，可点可拖。</p>\n')
    sec(P1, 'ov5', '五句话说清楚')
    g = lambda n, y, k: R.g(n, y, k)
    OV5 = [  # 每句只用页里已有的说法和代码现算的数（R.NUMS / R.T5），不新增判断；标签见 docs/CHAIN_TEMPLATE.md
        ('j', nolink(R.BLUF[0])),
        ('f', f'10 家 A 股大板厂 2026 年上半年花在厂房和机器上的钱（资本开支）有 {N["capH1"]} 亿元，是同期折旧的 {N["rH1"]} 倍；上一轮扩产最猛的 {N["pk"]} 年也只有 {N["rPk"]} 倍。<span class="tag t-src"><a href="#src93">源93</a></span>'),
        ('f', f'钱花了、厂还没开工的在建工程有 {N["cipH1"]} 亿元，是 2024 年底的 {N["cipX"]} 倍，2027–2028 年陆续开工。<span class="tag t-src"><a href="#src93">源93</a></span>'),
        ('j', '到时候 AI 需求接得住，龙头还能接着赚；接不住，最先降价的大概是扩产最多的 22–30 层板。'),
        ('f', f'眼下赚得最多的是新产能出来得慢的原料：宏和、鼎泰 2026 年上半年毛利率 {N["hh"]}%、{N["dt"]}%；可买家越来越集中，胜宏前五大客户占比一年从 {N["sh24"]}% 升到 {N["sh25"]}%。<span class="tag t-src"><a href="#src94">源94</a></span>'),
    ]
    for k, t in OV5[1:]:
        for num in re.findall(r'(\d+(?:\.\d+)?)(?=[%倍亿 ])', t):
            assert num in ''.join(R.BLUF) + str(N), f'OV5 数字 {num} 不在 BLUF / NUMS 里'
    w('<ol class="ov5">' + ''.join(f'<li>{LBL[k]}{t}</li>' for k, t in OV5) + '</ol>\n')
    w(f'<p class="note">完整的要点版（含 ROIC 回落、观察项）在<a href="{P4}#bluf">主要矛盾追踪</a>。</p>\n')
    sec(P1, 'ov-cap', '钱投了多少？')
    w(fig('f-ov', '10 家 A 股板厂：资本开支、折旧（亿元）与资本开支 ÷ 折旧（倍）', '<div id="m-fin-cCap" data-mirror="fin-cCap" class="chart" style="height:320px"></div>',
          f'红线是投资除以旧机器磨损：2026 年上半年 {N["rH1"]} 倍，高过上一轮 {N["pk"]} 年的 {N["rPk"]} 倍。{R.SF}', extra=f'<a href="{P3}#capex">逐家数字在周期与产能 →</a>'))
    sec(P1, 'ov-sig', '盯哪三个信号？')
    # 三个信号 = 主要矛盾 #1 的三个先行指标（R.TRACK[0]，阈值不变）；灯色按阈值现算
    t0 = R.TRACK[0]
    assert len(t0['ind']) == 3
    rH1 = R.AGG['2026H1']['ratio']
    s1 = 'r' if rH1 >= 4.0 else 'g'
    cc = J['bt']['series']['ccl']
    last = cc[-1]
    pk12 = max(v for _, v in cc[-12:])
    drop = pk12 - last[1]
    s3 = 'r' if drop >= 30 else ('y' if drop >= 15 else 'g')
    LT = {'r': '红灯', 'y': '黄灯', 'g': '绿灯', 'x': '灰灯'}
    SG = [
        (s1, '大厂还在加码建厂吗？', f'2026 年上半年资本开支是折旧的 {rH1:.1f} 倍，在建工程 {N["cipH1"]} 亿元<span class="tag t-src"><a href="#src93">源93</a></span>',
         '全年 ≥ 4 倍且在建工程继续升 = 扩产还在加速（本页提议）', '已越线：扩产还在加速' if s1 == 'r' else '没越线'),
        ('x', '22–30 层板报价松了吗？', '公开报价查不到（数据缺口）', '22–30 层降价、40 层以上不降 = 主要矛盾开始兑现', '没有可靠数据，靠一线校验'),
        (s3, '云厂商明年还肯多花钱吗？', f'{last[0]} 三家覆铜板厂 3 个月营收同比 +{last[1]:.0f}%，比近 12 个月最高点低 {drop:.0f} 个百分点<span class="tag t-src"><a href="#src46">源46</a></span>',
         '从峰值回落 ≥ 30 个百分点（本页提议），或云厂商合计投资增速 &lt; 10%（G25）', {'g': '没触发：需求还在加速', 'y': '接近：同比开始回落', 'r': '已越线：需求开始降温'}[s3]),
    ]
    w('<ol class="sig3">' + ''.join(f'<li class="{c}"><i class="lt" aria-hidden="true"></i><div><b>{t}</b><span><i class="k">现在</i>{now}</span><span><i class="k">警戒线</i>{th}</span><span class="st">{LT[c]} · {s}</span></div></li>' for c, t, now, th, s in SG) + '</ol>\n')
    w(f'<p class="note">{LBL["j"]}灯色是 Kiko 按上面的警戒线读出来的：红 = 已越过警戒线（往“扩产过头”那边走）；绿 = 还没触发；灰 = 没有可靠公开数据。覆铜板是板子的原料，它的收入一般比板厂早约 5 个月反映需求。三个信号的出处、总账编号和另两个矛盾的指标在<a href="{P4}#track">主要矛盾追踪</a>。</p>\n')
    sec(P1, 'prove', '什么会证明我们错？')
    w('<ol class="wt">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in R.WRONG_TOP[:3]) + '</ol>\n')
    w(f'<p class="note">第 4 条（钱流回板厂）和每条的证伪表在<a href="{P4}#wrongtop">主要矛盾追踪</a>。</p>\n')
    w(f'<a class="ov-next" href="{P2}">下一页：格局与钱在哪赚 →</a>\n')

    # ======================= ② 格局与钱在哪赚 =======================
    sec(P2, 'ch2', '一块板从哪来？', R.CH[2][1])
    w(A.callout(R.CALL[2]))
    w('<div class="lay" id="layers"><div class="ax">↓ 从买家往上游走 · 点开任一层看功能、代际、玩家</div>')
    for L in R.LAYERS:
        led = f'<dt>账本</dt><dd>{R.L(*L["led"])}</dd>' if L['led'] else ''
        w(f'<details name="layer" id="{L["id"]}" style="--c:{L["c"]}"><summary><b>{L["n"]}</b><span>{L["f"]}</span></summary><dl><dt>代际升级</dt><dd>{L["gen"]}</dd><dt>玩家与集中度</dt><dd>{L["who"]}</dd><dt>钱在哪</dt><dd>{L["money"]}</dd>{led}</dl></details>')
    w('</div>\n<p class="note">层的顺序按供应链，不是板子的物理叠层。“钱在哪”里的毛利率是公司整体口径（Tushare），包含非 AI 业务。</p>\n')
    hb = ''
    for r in S['heat']:
        sg = ''.join(f'<td class="sg" data-l="{l}"><b class="{SIG[x][1]}" title="{SIG[x][2]}">{SIG[x][0]}</b></td>' for l, x in zip('价期配稼', r[4:8]))
        hb += (f'<tr><td>{r[0]}</td><td class="num" data-l="规模">{r[1]}</td><td data-l="增速">{r[2]}</td><td data-l="驱动">{r[3]}</td>{sg}'
               f'<td class="st {stcls(r[8])}" data-l="2026">{r[8]}</td><td class="st {stcls(r[9])}" data-l="2027">{r[9]}</td><td data-l="约束">{r[10]}</td><td data-l="预期差">{r[11]}</td></tr>')
    legend = '<p class="note">四信号：<b>价</b> 价格 · <b>期</b> 交期 · <b>配</b> 配额 · <b>稼</b> 稼动率；' + ' '.join(f'<b class="{c}">{x}</b> {t}' for x, c, t in SIG.values()) + '。2027 列是我们的估计。</p>'
    w(f'<div id="heat"><h3 class="sec-h">哪些细分紧、哪些松？</h3>'
      + more('按产品与终端：细分图 + 热力表（规模、增速、四信号、主约束、预期差）', f'<p>{S["heat_note"]}</p>\n' + fig('f-seg', S['seg_t'], '<div id="pcb-cSeg" class="chart" style="height:320px"></div>', S['seg_note'])
             + legend + tbl(['细分', '2026E（亿美元）', '2026 增速', '驱动', '价', '期', '配', '稼', '2026', '2027', '主约束', '预期差'], hb), small=f'1 张图 · {len(S["heat"])} 行', wide=True) + '</div>\n')
    road = ''.join(PM.card(r) + ('\n<div class="arrow">↓ 线更细、孔更小</div>\n' if i < len(PM.ROAD) - 1 else '\n') for i, r in enumerate(PM.ROAD))
    w('<div id="road"><h3 class="sec-h">板子怎么越做越密？</h3>' + more('技术路线图：一代代怎么变“密”', road, small=f'{len(PM.ROAD)} 代') + '</div>\n')
    w('<div id="road-ai"><h3 class="sec-h">AI 带来哪些新变量？</h3>' + more('AI 服务器带来的新变量（Ⓐ–Ⓕ）', '<p class="note">Ⓐ–Ⓓ 已在出货或爬坡；Ⓔ 推迟；Ⓕ 还在测试。</p>\n' + '\n'.join(PM.card(r, True) for r in PM.AI), small=f'{len(PM.AI)} 项') + '</div>\n')
    w('<div id="mech"><h3 class="sec-h">一块板怎么做出来？</h3>')
    w('<div class="flowp">' + '<i>→</i>'.join(f'<span>{x}</span>' for x in S['flow']) + '</div>\n')
    w(more('材料 / 工序：管什么、AI 板为什么难', tbl(['材料 / 工序', '管什么', 'AI 板为什么难'], ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in S['mech']), 'stack') + f'<p class="note">{S["terms"]}</p>', small=f'{len(S["mech"])} 项'))
    w('</div>\n')

    sec(P2, 'ch3', '钱在哪一层？', R.CH[3][1])
    w(A.callout(R.CALL[3]))
    mp = ''.join(f'<tr><td><b>{seg}</b></td><td data-l="集中度">{c}</td><td data-l="头部与份额">{top}</td><td data-l="定价权">{pw}</td><td data-l="利润池">{pf}</td><td data-l="账本">{" ".join(led)}</td></tr>\n' for seg, c, top, pw, pf, led in PM.MAP)
    w('<div id="pattern"><h3 class="sec-h">谁占多少、谁能涨价？</h3><p>从上游到下游排。“集中度”看几家公司占了多少；“定价权”看谁能说涨就涨。越往上游，最高端那一小段越集中，但铜箔这样的环节集中了也不一定赚钱。</p>\n'
      + more('格局图全表：集中度、头部与份额、定价权、利润池', tbl(['环节', '集中度', '头部与份额', '定价权', '利润池', '账本'], mp, 'mp stack'), small=f'{len(PM.MAP)} 环', wide=True) + '</div>\n')
    w(fig('f-gm', '毛利率：2025 → 2026H1（17 家 A 股，公司整体口径）', '<div id="fin-cGm" class="chart" style="height:520px"></div>',
          f'蓝 = 板厂、青 = 覆铜板、橙 = 上游（玻纤布、钻针、铜箔）。上游里分化很大：玻纤布、钻针大涨，铜箔仍低。钱在新产能来得慢、客户认证难的环节，不在卖得多的环节。{R.SF}'))
    w(fig('f-roic', 'ROIC 中位数：板厂 / 覆铜板 / 上游（2015–2025）', '<div id="fin-cRoic" class="chart" style="height:300px"></div>',
          f'上一轮 2020–21 年扩产后，三个环节的 ROIC 都在 2022–24 年回落，覆铜板和上游一度为负。ROIC 用 Tushare 口径，各家投入资本算法未统一调整 {R.SF}。我们没有逐家算资本成本；如果按制造业常用的约 8% 粗看 {R.E}，2023–24 年多数公司低于资本成本。',
          extra=f'<a href="{P5}#fin">逐家 ROIC 表在底稿与数据 →</a>'))
    w('<h3 id="cost" class="sec-h">成本能核到哪？</h3>'
      + more('成本结构：成本项、证据、含义（能核的写数，不能核的写缺口）', tbl(['成本项', '证据', '含义'], ''.join(f'<tr><td><b>{a}</b></td><td data-l="证据">{b}</td><td data-l="含义">{c}</td></tr>' for a, b, c in R.COST), 'stack'), small=f'{len(R.COST)} 项'))
    w(more('为什么“涨了”却不“缺”？', f'<div id="price" class="aside"><p>{S["pricebox"]}</p></div>'))
    argsec(2, args[1], 'a', CIRC, 'e', '论点', lambda s_: s_, collapse=True)

    sec(P2, 'ch4', '谁说了算价格？', R.CH[4][1])
    w(A.callout(R.CALL[4]))
    w(more('五力表：供应商议价、买方议价、新进入者、替代、护城河', tbl(['环节', '供应商议价', '买方议价', '新进入者', '替代', '护城河'], ''.join(f'<tr><td><b>{a}</b></td><td data-l="供应商">{b}</td><td data-l="买方">{c}</td><td data-l="新进入">{d}</td><td data-l="替代">{e}</td><td data-l="护城河">{f}</td></tr>' for a, b, c, d, e, f in R.FORCE)) + f'<p class="note">{R.FORCE_NOTE}</p>', small=f'{len(R.FORCE)} 环', wide=True))
    w('<div id="buyer">' + fig('f-top5', '买方力量：前五大客户占比（年报）', '<div id="fin-cTop5" class="chart" style="height:300px"></div>',
          f'AI 板厂的客户越来越集中：胜宏 2024 → 2025 年从 {R.T5["胜宏科技"][2024]:.0f}% 升到 {R.T5["胜宏科技"][2025]:.0f}%，生益电子到 {R.T5["生益电子"][2025]:.0f}%；鹏鼎（苹果链）长期约 90%。客户越集中，它压价、找第二家供应商时板厂越难说不；不过占比升高，一部分也只是因为最大客户自己的订单涨得快。{R.SC}',
          extra=f'<a href="{P5}#fin">全表在底稿与数据 →</a>') + '</div>\n')
    w(f'<h3 class="sec-h">高回报稳不稳？</h3><p>2025 年 ROIC 已经分成两组——广合 {g("广合科技","2025","roic"):.1f}%、胜宏 {g("胜宏科技","2025","roic"):.1f}%、生益电子 {g("生益电子","2025","roic"):.1f}%、沪电 {g("沪电股份","2025","roic"):.1f}% vs 崇达 {g("崇达技术","2025","roic"):.1f}%、超声 {g("超声电子","2025","roic"):.1f}%、景旺 {g("景旺电子","2025","roic"):.1f}% {R.SF}。高回报只持续了 1–2 年，还看不出是护城河还是周期 {R.E}。下面的打分卡就是用来回答这个问题的。</p>\n')

    sec(P2, 'score', '真本事还是运气？', '用一张打分卡回答：别人能不能抢走这门生意。')
    cell = lambda v: f'<td class="sc s{v}">{v}</td>' if v is not None else '<td class="sc s0" title="待补">?</td>'
    body = ''
    for r in R.SCORE:
        body += (f'<tr><th scope="row">{V3.SHORT[r["k"]]}</th>' + ''.join(cell(c[0]) for c in r['cells'])
                 + f'<td class="sc avg">{r["avg"]:.1f}</td><td class="sc fl{" neg" if r["floor"] < 0 else ""}">{r["floor"]:.0f}%</td></tr>')
    hd = '<tr><th>环节</th>' + ''.join(f'<th>{d[0]}</th>' for d in R.DIMS) + '<th>均分</th><th>谷底<br>毛利率</th></tr>'
    w('<p>这里借用投资书《资本回报》（Marathon）的办法：不问需求有多大，只问“别人能不能抢走这门生意”。六个问题：别人能不能照着做、客户敢不敢换、换了要多麻烦、是不是靠少数大客户、新技术会不会让工厂作废、要不要一直砸钱。每项 1–5 分，5 分 = 高回报更能撑得久。'
      '最后一列“谷底毛利率”是上一轮行业不景气时（2021–2025），这个环节里最抗跌那家最差的一年（台股是最差一个季度），用来检验打分准不准。</p>')
    w('<div class="tbl"><table class="scm"><thead>' + hd + '</thead><tbody>' + body + '</tbody></table></div>')
    sc_note = f'<p class="note">{R.SC_NOTE} ? = 待补。谷底毛利率：A 股为年度、台股为单季 {R.SF} {R.S("fm")} {R.SSUB} {R.SD}。</p>'
    w(A.callout(R.CALL['score']))
    w(more('打分卡读出来的三条 + 宏和 59%、鼎泰 56%：护城河还是短缺峰值？',
           '<ul class="sc-l">' + ''.join(f'<li>{x}</li>' for x in R.SC_CALL[:3]) + '</ul>'
           + '<div class="sc-hh"><h4>宏和 59%、鼎泰 56%：护城河还是短缺峰值？</h4><p>' + R.SC_CALL[3] + '</p><p>' + R.SC_CALL[4] + '</p>'
           '<p class="note">这一判断不改主要矛盾（#1 板厂扩产潮 vs 需求能撑多久；#2 利润流向新产能来得慢的上游），只是把 #2 说细：流到上游的利润里，钻针更可能留得住，电子布更可能在 2027–28 年新产能出来后吐回去。</p></div>', small='3 条 + 1 个专题'))
    dt = ''.join(f'<tr><td><b>{d[1]}</b></td><td data-l="定义">{d[2]}</td><td data-l="1 分">{d[3]}</td><td data-l="5 分">{d[4]}</td><td data-l="证据数据">{d[5]}</td></tr>' for d in R.DIMS)
    ev = ''
    for r in R.SCORE:
        ev += f'<tr class="sum"><td colspan="3"><b>{r["n"]}</b> · {r["rep"]} · 均分 {r["avg"]:.1f}（{r["cnt"]}/6 格有分）· 判定：{r["v"]}</td></tr>'
        for d, (v, t) in zip(R.DIMS, r['cells']):
            ev += f'<tr><td>{d[0]}</td><td class="sc s{v if v is not None else 0}">{v if v is not None else "待补"}</td><td data-l="证据">{t or "待补"}</td></tr>'
        ck = '；'.join(f'{a} {p} {lo:.1f}% → {q} {hi:.1f}%' for a, p, lo, hi, q in r['chk'])
        ev += f'<tr><td>谷底检验</td><td>—</td><td data-l="谷底 → 现在">{ck} {R.CHK_SRC[r["k"]]}</td></tr>'
    w(more('打分定义：分数怎么读、六维怎么打 1 分 / 5 分', sc_note + tbl(['维度', '定义', '1 分', '5 分', '证据数据'], dt), small='6 维'))
    w(more('逐格证据：5 个环节 × 6 维 + 谷底检验', tbl(['维度', '分', '证据'], ev, 'hm scev'), small='30 格 · 含待补', wide=True))
    w(f'<h4 id="alloc">管理层怎么花钱？</h4>' + more('跟踪指标：管理层资本配置（分红 + 回购 vs 建厂投资）', f'<p>{R.ALLOC_CALL}</p>' + f'<p class="note">逐家资本配置表（18 家）在<a href="{P5}#fin">底稿与数据</a>。</p>', small='只跟踪，不打分'))

    sec(P2, 'ch8', '中国和海外差在哪？', R.CH[8][1])
    if cn:
        w(A.callout(cn['gov'], '中国账本判断') + A.plain(R.PLAIN_CN))
    w(more('海外龙头 vs 中国龙头：逐项差距', A.compare([(a, b, c, f'<b>差距</b> {d}') for a, b, c, d in R.CNOS], '海外龙头', '中国龙头')
           + f'<p class="note">“差距”是我们的归纳 {R.E}。海外和中国口径不同（季度 / 半年、营业利益率 / 毛利率），只看方向。</p>', small=f'{len(R.CNOS)} 项', wide=True))
    if cn:
        sq = '<div class="scqa">' + ''.join(f'<div><b>{lab}</b><span>{txt}</span></div>' for lab, txt in zip(('背景', '冲突', '问题'), cn['scqa'])) + '</div>'
        o = [f'<div id="cn" class="cnsec"><div class="kicker">平行账本 · {cn["kicker"]}</div>\n' + more('中国账本从哪来：背景、冲突、问题', sq, small='3 句')]
        o.append('\n<div class="kl cn">')
        for i, a in enumerate(cn['args'], 1):
            o.append(f'<a href="#c{i}"><span class="i">{CNC[i-1]}</span><span>{nolink(a["claim"])}<span class="k">{nolink(a["key"])}</span></span></a>')
        o.append(f'</div>\n<p class="note">{cn["mece"]}</p></div>\n')
        w(''.join(o))
        for i, a in enumerate(cn['args'], 1):
            argsec(i, a, 'c', CNC, 'ce', '中国论点', lambda s_: 'cn-' + s_, collapse=True)

    # ======================= ③ 周期与产能 =======================
    sec(P3, 'ch6', '扩产潮有多大？', R.CH[6][1])
    w(A.callout(R.CALL[6]))
    w(A.stats(R.STATS))
    w('<div id="capex">' + fig('f-cap', '10 家 A 股板厂：资本开支、折旧、在建工程（亿元）与资本开支 ÷ 折旧（倍）', '<div id="fin-cCap" class="chart" style="height:340px"></div>',
          f'2026H1 是半年数（柱子只有半年），倍数是同期相除可比。上一轮 {R.PEAK} 年 {R.NUMS["rPk"]}× 之后，板厂 ROIC 中位数 2023 年降到 {R.NUMS["roic23"]}%。2016–2021 年为 8–9 家（生益电子、广合数据不全）。{R.SF}') + '</div>\n')
    w(more('逐家资本开支、折旧倍数、在建工程', f'{capt}<p class="note">{R.SF}</p>', small='10 家板厂', wide=True))
    w(f'<p>胜宏 1H26 资本开支 {g("胜宏科技","2026H1","capex"):.1f} 亿元、是折旧的 {g("胜宏科技","2026H1","capex")/g("胜宏科技","2026H1","dep"):.1f} 倍；鹏鼎在建工程 {g("鹏鼎控股","2026H1","cip"):.1f} 亿元。公司公告的扩产计划合计超 800 亿元 {R.S("capex")}。{R.SF}</p>\n')
    sec(P3, 'test', '现在缺什么？', S['test_rule'])
    tb = ''
    for r in S['test']:
        tb += f'<tr><td>{r[7]}</td><td><b>{r[0]}</b></td><td data-l="价格">{r[1]}</td><td data-l="交期">{r[2]}</td><td data-l="配额">{r[3]}</td><td data-l="稼动率">{r[4]}</td><td class="num" data-l="得分">{r[5]}</td><td class="st {stcls(r[6])}" data-l="判定">{r[6]}</td></tr>'
    w(more('约束排序表：价格、交期、配额、稼动率', tbl(['#', '环节', '价格', '交期', '配额', '稼动率', '得分', '判定'], tb) + f'<p class="note">{S["test_note"]}</p>', small=f'{len(S["test"])} 环', wide=True))
    w('<p class="note">先行指标：CCL 三家营收同比领先 AI 板厂约 5 个月（已回测，见<a href="#lead">底稿第 10 步</a>）；历史上玻纤布 2018 年后价格回落约两年（<a href="#hist">底稿第 9 步</a>）。</p>\n')
    argsec(1, args[0], 'a', CIRC, 'e', '论点', lambda s_: s_)
    sec(P3, 'ch5', '谁在买，能买多久？', R.CH[5][1])
    w(A.callout(R.BLUF[4]))
    w(f'<div id="ai"><h3 class="sec-h">AI 板会不会缺？</h3><p>{S["ai_sub"]}</p>\n'
      + more(f'{S["ai_h"]}：各环节 2027 满足率（模型）vs 可观测信号', tbl(['环节', '预测口径（2027 满足率，模型）', '可观测信号（得分）', '判定'], ''.join(f'<tr><td><b>{a}</b></td><td data-l="预测">{b}</td><td data-l="可观测">{c}</td><td class="st {stcls(d)}" data-l="判定">{d}</td></tr>' for a, b, c, d in S['ai_tbl'])), small=f'{len(S["ai_tbl"])} 环') + '</div>\n')
    w('<p class="note">需求曲线、云厂商资本开支和每柜 PCB 价值在<a href="#demand">底稿第 3 步</a>；技术代际见<a href="#road-ai">AI 新变量</a>。</p>\n')
    argsec(3, args[2], 'a', CIRC, 'e', '论点', lambda s_: s_)
    sec(P3, 'ch7', '能绕开最贵的吗？', R.CH[7][1])
    w(A.callout(R.CALL[7]))
    w('<ol class="subst">' + ''.join(f'<li><h4>{a}</h4><p>{b}</p><dl><dt>现状</dt><dd>{c}</dd><dt>看什么</dt><dd>{d}</dd>' + (f'<dt>账本</dt><dd>{e}</dd>' if e and e != '—' else '') + '</dl></li>' for a, b, c, d, e in R.SUBST) + '</ol>\n')

    # ======================= ④ 主要矛盾追踪 =======================
    sec(P4, 'ch1', '和市场哪里不同？', R.CH[1][1])
    w(A.callout(R.BLUF[0]))
    w(A.more('要点版：再多说一点（五段）', '<div class="bluf" id="bluf">' + ''.join(f'<p>{x}</p>' for x in R.BLUF) + A.src_line(R.BLUF_SRC, T, extra=A.strip_fn(R.BLUF_SRC).replace('数字：', '').lstrip('；')) + '</div>', small=f'{len(R.BLUF)} 段'))
    w(more('市场 / 卖方怎么看 vs 本页怎么看', A.compare(R.VIEW, '市场 / 卖方', '本页') + f'<p class="note">{R.VIEW_NOTE}</p>', small=f'{len(R.VIEW)} 处分歧', wide=True))
    sec(P4, 'claims', '现在的判断是什么？', '2026 年的现状和三条已入账的核心判断；每条写了“若我错，你会看到什么”。')
    w(f'<p>{S["gov"]}</p>' + A.plain(R.PLAIN_GOV) + '\n')
    w('<ol class="claims">')
    for i, c in enumerate(S['claims'], 1):
        w(f'<li><div class="jid">判断 {i} · {c["id"]} · 检查日 {c["due"]}</div><p class="cl-t">{c["t"]}</p>' + (A.plain(R.PLAIN_CLAIMS[c["id"]]) if c["id"] in R.PLAIN_CLAIMS else '') + f'<p class="note">依据：{c["ev"]}</p><p class="wr"><b>若我错，你会看到：</b>{c["wrong"]}</p></li>')
    w('</ol>\n')
    sec(P4, 'ch9', '每个矛盾盯什么？', R.CH[9][1])
    w('<div id="track">')
    for ti, t in enumerate(R.TRACK):   # 主要矛盾 #1 展开，其余两条收起（内容不变）
        h = f'<div class="trk"><div class="role">{t["n"]} · {t["role"]}</div><h3>{t["t"]}</h3><ol>'
        for ind, now, th, led in t['ind']:
            h += f'<li><b>{ind}</b><br><span class="k">现在</span> {now}<br><span class="k">阈值</span> {th}<br><span class="k">账本</span> {led}</li>'
        h += f'</ol><div class="wr"><b>证伪：</b>{t["wrong"]}</div></div>'
        w(h if ti == 0 else more(f'{t["n"]} · {nolink(t["t"])}', h, small=f'{len(t["ind"])} 个指标'))
    w('</div>\n<p class="note">没有总账编号的阈值是本页提议，要变成预测需 John 确认（见下方“待 John 确认”）。“现在”一栏随每周五周报的公开数据跟踪更新（见本页“一线校验”里的公开数据替代跟踪），改了就重跑构建。</p>\n')
    sec(P4, 'propose', '待 John 确认什么？', '这些预测草案还没有入账；到期日、验证来源和“现在读数”都列在表里。')
    XR = {  # 现在读数：和草案括号里的数同一口径、同一代码现算；下面 assert 保证两边一致
        'X1': f'{R.AGG["2026H1"]["ratio"]:.1f} 倍（1H26）',
        'X2': f'{R.AGG["2026H1"]["cip"]:.0f} 亿元（1H26）',
        'X3': f'{R.MED["板厂"]["2025"]:.1f}%（2025）',
        'X4': f'{st.median([g(n, "2025", "gm") for n in ("崇达技术", "超声电子", "世运电路")]):.1f}%（2025）',
        'X5': f'{R.T5["胜宏科技"][2025]:.1f}%（2025）',
        'X6': f'{g("宏和科技", "2026H1", "gm"):.1f}%（1H26）',
        'X7': f'{R.DT["2026H1"]:.1f}%（1H26）',
        'X8': f'{g("宏和科技","2026H1","capex")/g("宏和科技","2026H1","rev")*100:.0f}%（1H26）',
    }
    assert [p[0] for p in R.PROPOSE] == list(XR), 'X1–X8 顺序变了'
    for p in R.PROPOSE:
        num = re.match(r'[\d.]+', XR[p[0]]).group(0)
        assert num in p[1], f'{p[0]} 现在读数 {num} 和草案文字对不上'
    w(f'<div id="propose-t"><p>这些<b>没有</b>写进总账（data/ledger.json），概率只是 Kiko 的建议；John 确认后才入账、才打分。</p>'
      + tbl(['#', '预测（草案）', '到期', '现在读数', '验证来源', '建议概率', '对应矛盾'], ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td data-l="到期">{c}</td><td data-l="现在"><span class="xr">{XR[a]}</span></td><td data-l="来源">{d}</td><td data-l="建议">{e} <span class="pill">待确认</span></td><td data-l="矛盾">{f}</td></tr>' for a, b, c, d, e, f in R.PROPOSE), 'stack ledger')
      + '<p class="note">现在读数由 pcb/research.py 从财报现算，和草案括号里的数同口径；年报出来后按“验证来源”一栏打分。</p></div>\n')
    sec(P4, 'wrongtop', '什么算我们错？', '四条证伪信号，加上已入账判断的证伪表和预测台账。')
    w(A.callout(f'{R.WRONG_TOP[0][0]}——{R.WRONG_TOP[0][1]}', '最该盯的证伪'))
    w('<ol class="wt">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in R.WRONG_TOP) + '</ol>\n')
    w(more('已入账判断的证伪表（J1–J8、CJ1–CJ3）', f'<div id="wrong">{S["wrong"]}</div>', small='JS 渲染 · 含来源', wide=True))
    w(more('预测台账（已入账）', f'<div id="pred">{S["pred"]}</div>', wide=True))
    sec(P4, 'check', '一线要问什么？', '工厂里的人比公开数据早知道。问题保持开放，先用公开数据每周五替代跟踪。')
    fq = ''.join(f'<li class="fq"><b>Q{i} {t}</b> <span class="pill">{ref}</span><p>{q}</p><p class="note">为什么问：{why}</p></li>' for i, (t, q, why, ref) in enumerate(R.FIELD, 1))
    w(more(f'一线校验：{len(R.FIELD)} 个问题', f'<ol class="fqs">{fq}</ol>', small=f'Q1–Q{len(R.FIELD)}'))
    w(more('公开数据替代跟踪（每周五）', f'<p class="sub">{S["check_sub"]}</p>' + tbl(['问题', '公开替代数据', '频率', '判读阈值', '当前读数'], ''.join(f'<tr><td><b>{a}</b></td><td data-l="数据">{b}</td><td data-l="频率">{c}</td><td data-l="阈值">{d}</td><td data-l="当前">{e}</td></tr>' for a, b, c, d, e in S['checks'])), small=f'{len(S["checks"])} 个问题', wide=True))
    sec(P4, 'gaps', '还缺哪些数据？')
    w(more('这次补上的 / 还缺的', '<div class="cols2"><div><h4>这次补上的</h4><ul>' + ''.join(f'<li>{x}</li>' for x in R.FILLED) + '</ul></div>'
      '<div><h4>还缺的</h4><ul>' + ''.join(f'<li>{x}</li>' for x in R.REMAIN) + '</ul></div></div>', small=f'补上 {len(R.FILLED)} · 还缺 {len(R.REMAIN)}')
      + more('原底图缺口逐条', '<ul class="note">' + ''.join(f'<li>{x}</li>' for x in PM.GAPS) + '</ul>', small=f'{len(PM.GAPS)} 条'))

    # ======================= ⑤ 底稿与数据 =======================
    sec(P5, 'base', '底稿怎么算的？', 'SOP 13 步底稿：需求、供给、平衡、瓶颈、回测、对账；滑块能拖，图跟着重算。默认折叠，点开或点任一“底稿 ↓”链接自动展开。')
    w('<span class="forwho">给想核数的人</span>\n')
    w('<p class="note">底稿里的层数、材料等级、HVLP、钻针寿命，在<a href="explain-pcb.html">PCB 原理图</a>里有图解（一步一张图）。</p>\n')
    o = [f'<details class="apx base2" id="baseD"><summary>{S["base_title"]} <small>{S["base_sub"]}</small></summary><div class="body"><ol class="stepix">']
    for s in STEPS:
        sup = ''.join(CIRC[i-1] for i in sorted({i for i, _ in back[s[0]]})) + (' <i class="cnm">中</i>' if cn and any(x['id'] == s[0] and x.get('cn') for x in S['steps']) else '')
        o.append(f'<li><a href="#{s[0]}"><span class="n">{s[1]}</span>{MID[s[0]]}<span class="s">{sup}</span></a></li>')
    o.append('</ol>\n')
    for st_, (sid, n, short, ttl) in zip(S['steps'], STEPS):
        chips = ''
        if back[sid]:
            chips = '<div class="sup">' + ''.join(f'<a href="#e{i}-{j}">支撑论点{CIRC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in back[sid]) + '</div>'
        elif st_.get('ctx'):
            chips = f'<div class="sup"><span>{st_["ctx"]}</span></div>'
        o.append(f'<div id="{sid}" class="step"><div class="kicker">底稿 {n} · {ttl}</div>\n<h2>{st_["h"]}</h2>{chips}\n')
        if st_.get('sub'):
            o.append(f'<p class="sub">{st_["sub"]}</p>\n')
        o.append(st_['body'].strip() + '\n')
        if st_.get('cn'):
            c = st_['cn']
            ch = ''.join(f'<a href="#ce{i}-{j}">支撑中国论点{CNC[i-1]} · 证据 {i}.{j} ↑</a>' for i, j in cback[sid])
            o.append(f'<div class="cnb" id="cn-{sid}"><div class="cnh"><span class="lb">中国账本</span><b>{c["h"]}</b></div>' + (f'<div class="sup">{ch}</div>' if ch else '') + c['body'].strip() + '</div>\n')
        o.append('</div>\n')
    o.append('</div></details>\n')
    w(''.join(o))
    sec(P5, 'fin', '逐家财报宽表', '17 家 A 股 PCB 链公司的逐家数字：图在前几页，表在这里。')
    w(more('逐家 ROIC 表（2019–2025 + 1H26 毛利率）', f'{roict}<p class="note">红色 = 负值；1H26 ROIC 是半年口径、没年化，所以表里不放。{R.SF}</p>', small='17 家', wide=True))
    w(more('前五大客户占比全表', f'{t5t}<p class="note">世运 2022 年报在巨潮未检索到；广合 2023 年上市，之前没有年报。{R.SC}</p>', small='12 家 · 2021–2025', wide=True))
    ar = ''
    for seg in ('板厂', '覆铜板', '上游', '载板'):
        for x in [x for x in R.ALLOC if x['seg'] == seg]:
            ar += (f'<tr><td>{x["n"]}<span class="note"> {seg}</span></td><td>{x["cip"]:.1f}</td><td>{x["r"]:.1f}×</td><td>{x["cap"]:.1f}</td><td>{x["div"]:.1f}</td><td>{x["bb"]:.1f}</td>'
                   f'<td>{x["pay"]:.0f}%</td></tr>')
    at = ('<div class="tbl"><table class="fin"><thead><tr><th>公司（亿元）</th><th>在建工程 1H26</th><th>资本开支÷折旧 1H26</th><th>资本开支 2021–25</th><th>现金分红 2021–25</th><th>回购 2021–25</th><th>(分红+回购)÷资本开支</th></tr></thead><tbody>'
          + ar + '</tbody></table></div>')
    w(more('逐家资本配置表（18 家）', at + f'<p class="note">分红按除息日归年，回购按方案归到最后一笔“完成”的年份，股权激励回购注销已剔除；兴森科技为 IC 载板参照，含 PCB 业务。{R.SD} {R.SF}</p>', small='18 家 · 2021–2025', wide=True))
    sec(P5, 'quiz', '读完能答这五问吗？')
    w(''.join(f'<details class="more qd"><summary><span>Q{i}</span><b>{q}</b></summary><div class="more-b"><p>{a}</p></div></details>' for i, (q, a) in enumerate(S['quiz'], 1)) + '\n')
    sec(P5, 'words', '这些词什么意思？')
    w(f'<p class="howto">怎么读这套页面：五页从“总览”往下展开到“底稿”，每节先一句导语、一句判断，细表收在“展开细节”里。正文里的小号上标数字<sup class="fn"><a class="fn-a" href="#src93">93</a></sup>是来源编号，点一下看来源，全部列在本页<a href="#src">来源与注释</a>；每段最多留 1 个上标，其余在每章末尾的“本章来源”。'
      f'图表下方一行灰字是这张图的来源。{R.E} = Kiko 自估；{R.GAP} = 没有可靠公开数据，不估；{R.PAY} = 付费数据，没看到原文。G / P 编号链接到<a href="ledger.html">总账</a>。'
      '段首小标签：<span class="fj f">事实</span> = 能查到出处的数或事；<span class="fj j">判断</span> = 我们的推断或估计。公开数据整理，<b>不构成投资建议</b>，不对任何个股给买卖意见。</p>\n')
    w(A.glossary(R.GLOSS))
    w('<p class="note">下载：<a href="pcb/pcb_model.xlsx">模型 Excel</a> · <a href="pcb/pcb_chain.md">报告原文 (Markdown)</a> · <a href="SOP.md">小链研究 SOP</a> · 构建：<code>./build.sh</code>（页面 <code>tpl/page_v4.py</code> + <code>pcb/page.py</code> + <code>pcb/research.py</code>，模型 <code>pcb/model.py</code>）</p>\n')
    MERGE = '第 81–92 条原在底图页（pcb-map.html），2026-10-23 并入本页、编号改为全站统一；'
    assert MERGE in S['src'], 'pcb/page.py 的来源说明改了，请同步 page_v4 的并入说明搬家'
    sec(P5, 'apx', '数字从哪来？', f'正文上标数字 = 下面的来源编号（全站统一编号，图表下方的“来源”行用同一套编号）。{S["src_small"]}')
    w(f'<details class="apx" id="apxSrc"><summary>来源列表与局限 <small>点任一上标会先弹出来源摘要</small></summary><div class="body" id="src">{S["src"].replace(MERGE, "第 81–92 条原在底图页，编号已改为全站统一（见<a href=\"changelog.html#merge\">更新记录</a>）；")}</div></details>\n')

    # ---------------- 组装
    stub = '<div hidden id="ch-stub"><table id="pcb-logT"><tbody></tbody></table></div>'   # pcb.js 会往更新记录表里填；表本身在 changelog.html
    out, STAT, home_js = assemble(SECS, T, H1, title0='PCB 总览：扩产潮能不能等到需求接住', desc0=nolink(R.BLUF[0]), stub=stub,
                                  scripts=finjs + ''.join(f'<script src="{x}"></script>' for x in ['ledger_ids.js', 'chain.js'] + S['scripts'] + ['pcb_fin.js', 'assets/reading.js']),
                                  tail='<script>document.getElementById("baseD").addEventListener("toggle",function(){if(this.open&&window.redraw)setTimeout(window.redraw,30)});</script>\n',
                                  foot='<a href="cowos.html">CoWoS</a>')
    render_v4.STAT = STAT
    render_v4.CL = changelog_secs(S, J)
    return out


CSS_ALL = None


def assemble(SECS, T, H1, title0, desc0, stub, scripts, tail, foot):
    """SECS（每节 page/id/title/lead/body/cls）→ {文件名: html}。别的页的节放进隐藏的 #ch-shadow；返回 (out, STAT, home)。"""
    global CSS_ALL
    for s in SECS:
        s['html'] = A.fnify(''.join(s['body']))
    home = {}
    for s in SECS:
        for i in re.findall(r'\bid="([^"]+)"', s['html']) + [s['id']]:
            assert i not in home, f'id 重复：{i}'
            home[i] = s['page']
    for k, v in ALIAS.items():
        home.setdefault(k, v)
    home_js = {k: v for k, v in home.items()}
    STAT = {}
    out = {}
    css = CSS_ALL = V3.CSS2 + PM.CSS + V3.CSS3 + CSS4
    nolink = lambda t: re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', t)
    for pi, (pf, pt, ps, pd) in enumerate(PAGES):
        mine = [s for s in SECS if s['page'] == pf]
        rest = [s for s in SECS if s['page'] != pf]
        vis, nlb, allrefs = [], 0, []
        for k, s in enumerate(mine, 1):
            body = s['html']
            body = re.sub(r'href="#([\w-]+)"', lambda m: relink(m, pf, home), body)
            body, refs, nl = label_and_limit(body)
            nlb += nl
            allrefs += [r for r in refs if r not in allrefs]
            if s['cls'] == 'hero':
                v = f'<section id="{s["id"]}" class="hero" data-toc="{k:02d} {s["title"]}">{steps_strip(pf)}{body}{chsrc(refs, T, pf)}</section>\n'
            else:
                v = (f'<section id="{s["id"]}" class="ch" data-toc="{k:02d} {s["title"]}"><header class="ch-h"><span class="ch-n">{k:02d}</span><h2>{s["title"]}</h2></header>'
                     + (f'<p class="lead">{s["lead"]}</p>\n' if s['lead'] else '') + body + chsrc(refs, T, pf) + '</section>\n')
            vis.append(v)
        main_html = ''.join(vis)
        if pi > 0:
            main_html = f'<section id="pg-top" class="hero pg-h"><div class="kicker">{CHAIN} 研究 · 第 {pi+1} 页 / 共 {len(PAGES)} 页{" · 给想核数的人" if pf == DATA_PAGE else ""}</div><h1>{pt}</h1><p class="dek">{pd}。主线：{H1.split("：", 1)[1]}。</p>{steps_strip(pf)}</section>\n' + main_html
        main_html += prevnext(pf)
        # 隐藏区：JS 照常画图填表；去掉 data-mirror，免得同一张源图的镜像被隐藏副本抢走（chain.js 一个源只认一个镜像）
        shadow = '<div id="ch-shadow" hidden inert aria-hidden="true">' + ''.join(f'<section id="{s["id"]}" class="ch">{re.sub(r" data-mirror=\"[^\"]*\"", "", s["html"])}</section>' for s in rest) + '</div>\n'
        redirect = ('<script>window.CH_PAGE=' + json.dumps(pf) + ';window.CH_HOME=' + json.dumps(home_js, ensure_ascii=False, separators=(',', ':'))
                    + ';(function(){var h=decodeURIComponent(location.hash.slice(1)),p=h&&(window.CH_HOME[h]||(/^src\\d+$/.test(h)?"'+DATA_PAGE+'":""));if(p&&p!==window.CH_PAGE)location.replace(p.indexOf("#")>-1?p:p+"#"+h)})();</script>')
        desc = desc0 if pi == 0 else f'{CHAIN} · {pt}：{pd}'
        title = title0 if pi == 0 else f'{CHAIN} · {pt}'
        html = (head(title, desc, css, redirect, pf) + f'<body class="article chain" data-src-page="{DATA_PAGE}" data-fnmax="1" data-page="{ps}">\n'
                + topbar(pt, CHAIN) + nav_html(pf) + '<main class="wrap">\n' + main_html + '</main>\n' + shadow + stub
                + f'<footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="ledger.html">总账</a> · <a href="changelog.html">更新记录</a> · {foot}</footer>\n'
                + '<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n'
                + scripts + '\n' + tail + '</body></html>\n')
        assert 'class="tag t-src"' not in html.replace('<span class="tag t-src">源', ''), f'{pf}: 还有没转成脚注的行内来源'
        assert not re.search(r'<a\b(?:(?!</a>).)*<a\b', html, re.S), f'{pf}: 有嵌套 <a>'
        ids = re.findall(r'\bid="([^"]+)"', html)
        dup = {x for x in ids if ids.count(x) > 1}
        assert not dup, f'{pf}: 重复 id {dup}'
        vids = set(re.findall(r'\bid="([^"]+)"', main_html))
        miss = {h for h in re.findall(r'href="#([\w-]+)"', main_html) if h not in vids and not re.match(r'src\d+$', h)}
        assert not miss, f'{pf}: 看得见的锚点指到隐藏块 {miss}'
        bad = re.findall(r'(?<!页 )v0\.\d|旧版|并入', re.sub(r'<[^>]+>', '', main_html))
        if bad:
            tx = re.sub(r'<[^>]+>', '', main_html)
            for mm in re.finditer(r'(?<!页 )v0\.\d|旧版|并入', tx): print(pf, '…' + tx[max(0, mm.start()-60):mm.end()+40] + '…')
        assert not bad, f'{pf}: 内容页还有版本说明字样 {set(bad)}（应搬到 changelog.html）'
        STAT[pf] = dict(fn_main=sum(len(re.findall(r'class="fn-a"', re.sub(r'<details class="more chsrc">.*?</details>', '', v, flags=re.S))) for v in vis), labels=nlb, refs=len(allrefs))
        out[pf] = html
    return out, STAT, home_js


def log_rows(J):
    return A.fnify(''.join(f'<tr><td><b>{d}</b><br>{v}</td><td>{t}</td></tr>' for d, v, t in J['changelog']))


def log_table(J):
    return f'<div class="tbl"><table class="cl-log"><thead><tr><th>日期 · 版本</th><th>改了什么</th></tr></thead><tbody>{log_rows(J)}</tbody></table></div>'


def changelog_secs(S, J):
    """PCB 在更新记录页的几节：[(id, 标题, html)]。来源上标指到 PCB 底稿页。"""
    secs = [
        ('cl-pcb', 'PCB 现在是哪一版？',
         f'<p>{S["pill"]} → 2026-10-27 拆成 5 页（总览 / 格局与钱在哪赚 / 周期与产能 / 主要矛盾追踪 / 底稿与数据）。'
         f'原页眉：{S["kicker"].replace(" · 更新 <span id=\"pcb-upd\"></span>", "")}。</p><p>{S["vbar"].replace("#ch2", "pcb-pattern.html#ch2").replace("#ch3", "pcb-pattern.html#ch3")}</p>'),
        ('log', 'PCB 逐版记录', log_table(J) + '<p class="note">已入账判断、概率和模型数字只在 John 确认后改，每次改都在这里留一行。</p>'),
        ('merge', 'PCB 并入与旧版',
         '<ul><li>原“底图”页 <a href="pcb-map.html">pcb-map.html</a>（技术路线图、格局图、一线校验、缺口）2026-10-23 并入 PCB 页；旧链接自动跳转到新位置（现在在<a href="pcb-pattern.html#road">格局与钱在哪赚</a>、<a href="pcb-track.html#check">主要矛盾追踪</a>）。</li>'
         '<li>来源第 81–92 条原在底图页，2026-10-23 并入时编号改为全站统一；第 93 条起接着编。</li>'
         '<li>2026-10-27：一页九章拆成 5 页。旧网址 <code>pcb.html#锚点</code> 仍可用，会自动跳到新页的同一块。</li>'
         '<li>2026-10-28：格局页“打分定义”和中国账本的背景 / 冲突 / 问题收进展开细节，默认可见字数 4328 → 3929（不删内容）。</li>'
         '<li>“2026 年的现状”一段是 v0.2 起的结论，未改；“公开数据替代跟踪”是 v0.2 的四个问题；“读后五问”沿用 v0.2。</li>'
         f'<li>版本对比：<a href="{S["archive"][0]}">旧版 v1 存档（2026-10-20）</a> ⇄ 现在的 5 页版。</li></ul>'),
    ]
    return [(i, t, re.sub(r'href="#(src\d+)"', rf'href="{DATA_PAGE}#\1"', h)) for i, t, h in secs]


def changelog_page(parts):
    """更新记录页：parts = {链键: [(id, 标题, html)]}，按导航顺序分链成段。版本说明、并入说明、旧版存档链接（内容页不留这些）。"""
    order = [c for c in CHAINS if c[0] in parts]
    jump = ' · '.join(f'<a href="#{parts[k][0][0]}">{n}</a>' for k, n, _, _ in order)
    main = [f'<section id="top" class="hero" data-toc="01 更新记录"><div class="kicker">站内 · 更新记录</div><h1>更新记录</h1>'
            f'<p class="dek">每次改版、改判断都记在这里。研究页只放内容，版本说明、并入说明、旧版链接都搬到本页。</p><p>按链跳：{jump}</p></section>\n']
    k = 1
    for key, name, pages, _ in order:
        for sid, t, h in parts[key]:
            k += 1
            assert len(t) <= 15, t
            main.append(f'<section id="{sid}" class="ch" data-toc="{k:02d} {t}"><header class="ch-h"><span class="ch-n">{k:02d}</span><h2>{t}</h2></header>{h}</section>\n')
    main = ''.join(main)
    ids = re.findall(r'\bid="([^"]+)"', main)
    assert len(ids) == len(set(ids)), '更新记录页 id 重复'
    nav = nav_html('changelog.html', secs_here=False, key='').replace('<div class="sn-h">站内</div>', '<div class="sn-h">站内</div><div class="sn-here" id="snHere"></div>', 1)
    return (head('更新记录', '产业链情报研究中心：各研究页的版本说明、并入说明与旧版存档', CSS_ALL, '', 'changelog.html')
            + '<body class="article chain" data-src-page="pcb-data.html" data-page="更新记录">\n' + topbar('更新记录', '更新记录') + nav
            + '<main class="wrap">\n' + main + '</main>\n<footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="ledger.html">总账</a> · ' + ' · '.join(f'<a href="{p[0][0]}">{n}</a>' for _, n, p, _ in order) + '</footer>\n'
            + '<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n'
            + '<script src="assets/reading.js"></script>\n</body></html>\n')
