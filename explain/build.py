#!/usr/bin/env python3
"""万物原理图 生成器（可复用模板）。
每个专题一个规格文件 explain/<id>.py（META / GENS / STEPS / QUIZ / SOURCES）+ 一个图形脚本 explain/<id>.js；
通用引擎 explain/engine.js，样式 explain/explain.css。本脚本生成：
  explain-<id>.html   专题页（滚动叙事 + 粘性图卡 + 代际滑块 + 部件点按说明）
  explain.html        万物原理图目录页
  index.html          首页“万物原理图”卡片区（<!--explain:cards--> … <!--/explain:cards-->）
新增专题：复制 explain/hbm.py 与 explain/hbm.js，改内容，在 REGISTRY 里加一行即可。
交互范式参考 Anatomy（https://github.com/wheresryan22/anatomy ，MIT），代码为自写。
"""
import importlib.util, json, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 目录：已发布的专题（spec 文件名）+ 规划中的专题
REGISTRY = ['hbm']
PLANNED = [
    ('CoWoS 是怎么封装的', '中介层、微凸点、RDL、硅桥，CoWoS-S / L / R 的区别，为什么产能卡在中介层和载板。'),
    ('一块 AI 服务器 PCB 是怎么做出来的', '覆铜板、铜箔、玻纤布、钻孔电镀、层压，HVLP 铜箔为什么难。'),
    ('铜从矿山到电线', '采矿、选矿、冶炼、电解，精矿 TC/RC 与冶炼利润，为什么约束在精矿。'),
]
ANATOMY = ('Anatomy', 'https://github.com/wheresryan22/anatomy')

HEADER = ('<header class="top"><div class="wrap"><a class="brand" href="./"><b>●</b> 产业链情报研究中心</a><span class="sp"></span>'
          '<a class="btn" href="daily/">日报</a><a class="btn" href="explain.html">原理图</a><a class="btn" href="hbm.html">HBM</a>'
          '<button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>')


def load(name):
    sp = importlib.util.spec_from_file_location('ex_' + name, os.path.join(ROOT, 'explain', name + '.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def tok(s, ids, used):
    def sref(mo):
        n = int(mo.group(1))
        assert n in ids, f'未知来源编号 {n}'
        used.add(n)
        return f'<a class="sr" href="#src{n}">[{n}]</a>'
    s = re.sub(r'\{s:(\d+)\}', sref, s)
    s = s.replace('{calc}', '<span class="tag t-est">推算</span>').replace('{est}', '<span class="tag t-est">估</span>')
    assert '{' not in re.sub(r'<[^>]+>', '', s) or True
    return s


def render(name):
    m = load(name)
    M, ids, used = m.META, {s[0] for s in m.SOURCES}, set()
    for g in m.GENS:
        for k in ('src_cfg', 'src_std', 'src_prod'):
            assert g[k] in ids, (g['name'], k)
            used.add(g[k])
        g['unlock'] = tok(g['unlock'], ids, used)
        g['neck'] = tok(g['neck'], ids, used)
    steps = []
    for i, s in enumerate(m.STEPS):
        steps.append(dict(id=s['id'], scene=s['scene'], t=s['t'], hint=s.get('hint', ''), parts=s.get('parts', [])))
    quiz = [(tok(q, ids, used), tok(a, ids, used)) for q, a in m.QUIZ]
    bodies = [tok(s['body'], ids, used) for s in m.STEPS]
    unused = ids - used
    assert not unused, f'来源未被引用：{sorted(unused)}'
    ids_seen = [s['id'] for s in m.STEPS]
    assert len(ids_seen) == len(set(ids_seen)), '步骤 id 重复'

    dots = ''.join(f'<a href="#s-{s["id"]}" title="{html.escape(s["t"])}">{i + 1}</a>' for i, s in enumerate(m.STEPS))
    secs = ''.join(
        f'<section class="ex-step" id="s-{s["id"]}" data-i="{i}"><div class="ex-k">第 {i + 1} 步 / {len(m.STEPS)}</div><h2>{s["t"]}</h2>{bodies[i]}</section>'
        for i, s in enumerate(m.STEPS))
    gl = ''.join(f'<span>{g["name"]}</span>' for g in m.GENS)
    g0 = next((i for i, g in enumerate(m.GENS) if g['name'] == 'HBM3E'), 0)
    srcs = ''.join(f'<li id="src{n}"><a href="{u}" rel="noopener">{html.escape(t)}</a></li>' for n, t, u in m.SOURCES)
    rel = ' · '.join(f'<a href="{h}">{t}</a>' for h, t in M['related'])
    data = dict(gens=m.GENS, steps=steps, quiz=quiz)
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{M["title"]} · 万物原理图</title><meta name="description" content="{html.escape(M["card"])}">
<link rel="stylesheet" href="assets.css"><link rel="stylesheet" href="explain/explain.css"><script src="theme.js"></script></head><body class="ex-body">
{HEADER}
<main class="wrap ex-main">
<section class="ex-hero"><div class="kicker">{M["kicker"]}</div><h1>{M["title"]}</h1><p class="dek">{M["dek"]}</p>
<p class="sub">读法：往下滑，上面的图会跟着一步步搭起来；点图里的部件或下面的标签看说明；拖“代际”滑块，从 HBM2E 换到 HBM4E，图和数字一起变。每个数字后面的 [n] 是来源，<span class="tag t-est">推算</span><span class="tag t-est">估</span> 是自己算的或示意。相关：{rel} · {M["ver"]} · {M["date"]}</p>
<nav class="ex-dots" aria-label="步骤">{dots}</nav></section>
<div class="ex-lay">
<div id="ex" class="ex-fig"><div class="ex-card">
<div class="ex-hd"><span class="ex-n">Fig 1</span><div class="ex-pg"><button type="button" class="ex-prev" aria-label="上一步">‹</button><b>1 / {len(m.STEPS)}</b><button type="button" class="ex-next" aria-label="下一步">›</button></div><span class="ex-t"></span></div>
<div class="ex-stage"><svg class="ex-svg" role="img" aria-label="{M["title"]}的分步示意图"></svg></div>
<div class="ex-info" aria-live="polite"></div>
<div class="ex-chips" role="group" aria-label="可点部件"></div>
<div class="ex-ft"><span class="ex-hint"></span><span class="ex-ro" aria-live="polite"></span></div>
<div class="ex-ctl"><label class="ex-gen"><span>代际</span><input type="range" min="0" max="{len(m.GENS) - 1}" step="1" value="{g0}" aria-label="HBM 代际"><output></output></label>
<div class="ex-spd" role="group" aria-label="速率口径"><button type="button" data-s="std" aria-pressed="false">标准</button><button type="button" data-s="prod" aria-pressed="true">量产最快</button></div>
</div>
<div class="ex-gl" aria-hidden="true">{gl}</div>
</div></div>
<div class="ex-steps">{secs}</div>
</div>
<section id="sources"><h2>来源</h2><ol class="ex-src">{srcs}</ol>
<p class="note">口径：单颗带宽 = 线数 × 每根线速率 ÷ 8，由页面现算；“代表配置”取各代已量产或已公布的典型产品（见卡片里的来源），不是唯一配置。良率连乘、HBM 层厚分配、热流强弱是示意，不是厂商数据。</p></section>
<section id="credit"><h2>致谢与做法</h2><p>交互范式参考开源项目 <a href="{ANATOMY[1]}" rel="noopener">{ANATOMY[0]}</a>（wheresryan22/anatomy，MIT 许可，© 2026 Ryan）：把一个概念画成一台“真实的机器”，等轴测实体 + 四档明暗 + 由后往前的绘制顺序，卡片四角放编号、标题、提示和实时读数，图上的数字和部件来自同一个模型。本站代码为自写的轻量原生 JS / SVG（explain/engine.js），未复制 Anatomy 代码，不依赖任何外部 CDN。</p>
<p class="note">本页是科普性质的原理图，不构成投资建议。行业判断以 <a href="hbm.html">HBM 研究页</a> 为准。</p></section>
</main><footer class="wrap">Kiko 产业笔记 · 万物原理图 · 公开数据整理，不构成投资建议</footer>
<script>window.EXD={js};</script><script src="explain/engine.js"></script><script src="{M["js"]}"></script>
</body></html>
'''
    open(M['file'], 'w').write(page)
    return M


def card(M, live=True):
    return (f'<a class="card" href="{M["file"]}" style="color:inherit;text-decoration:none"><div class="kicker">{M["kicker"]}</div>'
            f'<h3 style="margin:.3em 0">{M["title"]}</h3><p style="margin:0 0 10px;font-size:15px">{M["card"]}</p>'
            f'<span class="pill">{M["ver"]} · {M["date"]}</span> <span class="pill" style="color:var(--ok)">已发布</span></a>')


def planned_card(t, d):
    return f'<div class="card" style="opacity:.6"><div class="kicker">规划中</div><h3 style="margin:.3em 0">{t}</h3><p style="margin:0;font-size:15px">{d}</p></div>'


def main():
    metas = [render(n) for n in REGISTRY]
    cards = ''.join(card(M) for M in metas)
    plan = ''.join(planned_card(t, d) for t, d in PLANNED)
    idx = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>万物原理图 · 产业链情报研究中心</title><link rel="stylesheet" href="assets.css"><link rel="stylesheet" href="explain/explain.css"><script src="theme.js"></script></head><body>
{HEADER}
<main class="wrap">
<section><div class="kicker">万物原理图</div><h1>一步一步看懂东西是怎么工作的</h1>
<p class="dek">每一篇把一样东西拆成几步：先讲它为什么存在，再从最小的零件一层层搭起来，最后落到每一代升级的关键和下一步卡在哪。图会跟着滚动一步步搭起来，能点、能拖，手机上也能用。</p>
<p class="sub">每个数字都标来源；自己算的标【推算】，示意的标【估】。研究判断以各链的研究页为准。</p></section>
<section><h2>已发布</h2><div class="grid g3">{cards}</div></section>
<section><h2>规划中</h2><div class="grid g3">{plan}</div></section>
<section><h2>做法</h2><p>交互范式参考开源项目 <a href="{ANATOMY[1]}" rel="noopener">{ANATOMY[0]}</a>（MIT，© 2026 Ryan）：把概念画成一台真实的机器，卡片四角放编号、标题、提示和实时读数，图上每个数字来自同一个模型。本站用自写的原生 JS / SVG 实现（explain/engine.js + 每篇一个规格文件），不依赖外部 CDN。</p></section>
</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议</footer></body></html>
'''
    open('explain.html', 'w').write(idx)
    # 首页卡片区
    p = 'index.html'
    s = open(p).read()
    a, b = '<!--explain:cards-->', '<!--/explain:cards-->'
    if a in s:
        i, j = s.index(a) + len(a), s.index(b)
        s2 = s[:i] + cards + s[j:]
        if s2 != s:
            open(p, 'w').write(s2)
    print('explain: ' + ', '.join(M['file'] for M in metas) + ' + explain.html')


if __name__ == '__main__':
    main()
