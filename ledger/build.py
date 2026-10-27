#!/usr/bin/env python3
"""全局判断总账：data/ledger.json（唯一来源）→ ledger.html + ledger_ids.js。build.sh 调用。
检查（任一不过就失败，不写页面）：
  1) 总账每一条都能对上研究页上的一个条目（旧编号存在，且原文一字不差）；
  2) 研究页上的每条判断/带日期预测都在总账里（不漏）；
  3) 全局编号唯一、格式 G01 / P001；未作废的预测都有概率（0–1）；
  4) 已打分的条目 outcome ∈ {命中, 未中}，Brier 由本脚本计算（不手填）。
ledger_ids.js：{原文 → 全局编号}，chain.js 用它在研究页的判断/预测旁边加小标签链到总账。"""
import json, os, re, sys, html, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources
ROOT = sources.ROOT
E = html.escape
TODAY = datetime.date(2026, 10, 22) if os.environ.get('LEDGER_TODAY') == 'fixed' else datetime.date.today()


EV_W = ('支持', '削弱', '触发证伪', '待核')  # 周度跟踪的证据记录：只追加，不改状态/概率（改判要 John 批准）



# 链条拆页后判断 / 预测住在“主要矛盾追踪”页（ledger.json 里的 page 字段不改，只改链接）
PAGE_MOVED = {'pcb.html': 'pcb-track.html'}

def load():
    return json.load(open(os.path.join(ROOT, 'data', 'ledger.json'), encoding='utf-8'))


def check(doc):
    it, errs = sources.page_items(), []
    items = doc['items']
    gids = [x['gid'] for x in items]
    if len(set(gids)) != len(gids):
        errs.append('全局编号重复：' + ', '.join(k for k, n in collections.Counter(gids).items() if n > 1))
    olds = [x['old'] for x in items]
    if len(set(olds)) != len(olds):
        errs.append('旧编号重复映射')
    for x in items:
        if not re.fullmatch(r'G\d{2}' if x['kind'] == '判断' else r'P\d{3}', x['gid']):
            errs.append(f'{x["gid"]} 编号格式不对')
        src = it.get(x['old'])
        if not src:
            errs.append(f'{x["gid"]} ← {x["old"]}：研究页上找不到这个条目')
        elif src['text'] != x['text']:
            errs.append(f'{x["gid"]} ← {x["old"]}：原文和研究页不一致（研究页改过？请同步总账）')
        elif src['kind'] != x['kind']:
            errs.append(f'{x["gid"]}：类型不一致')
        if x['status'] not in ('有效', '受挑战', '证伪', '作废'):
            errs.append(f'{x["gid"]}：状态 {x["status"]} 不在 有效/受挑战/证伪/作废 里')
        if x['kind'] == '预测' and x['status'] != '作废':
            p = x.get('prob')
            if not isinstance(p, (int, float)) or not 0 <= p <= 1:
                errs.append(f'{x["gid"]}：缺概率或不在 0–1')
            if x.get('outcome') not in ('待验证', '命中', '未中'):
                errs.append(f'{x["gid"]}：outcome 应为 待验证/命中/未中')
        for e in x.get('ev', []):
            if e.get('w') not in EV_W or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', e.get('d', '')) or not e.get('src', '').startswith('http') or not e.get('t'):
                errs.append(f'{x["gid"]}：证据记录格式不对（d=YYYY-MM-DD、w∈{"/".join(EV_W)}、t、src=链接）')
    texts = [x['text'] for x in items]
    if len(set(texts)) != len(texts):
        errs.append('有两条原文完全相同，标签会冲突')
    miss = sorted(set(it) - set(olds))
    if miss:
        errs.append('研究页上有、总账里没有：' + ', '.join(miss))
    return errs


def score(doc):
    for x in doc['items']:
        x['brier'] = round((x['prob'] - (1 if x['outcome'] == '命中' else 0)) ** 2, 4) if x.get('outcome') in ('命中', '未中') else None
    return doc


CSS = '''
.lg-sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:12px 0}
.lg-sum .card{padding:12px 14px}.lg-sum b{display:block;font-size:24px;line-height:1.2;font-variant-numeric:tabular-nums}
.lg-sum span{font-size:var(--t-footnote,13px);color:var(--mut)}
.lg-dist{display:flex;align-items:flex-end;gap:6px;height:72px;margin:6px 0 2px}
.lg-dist i{flex:1;background:var(--tint);opacity:.85;border-radius:4px 4px 0 0;min-height:2px}
.lg-dl{display:flex;gap:6px}.lg-dl span{flex:1;text-align:center;font-size:11px;color:var(--mut)}
.lg-f{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 4px}
.lg-f select{font:inherit;font-size:15px;padding:6px 10px;border-radius:var(--r-ctl,8px);border:0;background:var(--hig-fill);color:var(--fg);min-height:36px}
.lg-n{font-size:var(--t-footnote,13px);color:var(--mut)}
.lg-list{list-style:none;padding:0;margin:8px 0}
.lg-it{background:var(--card);border-radius:var(--r-card,12px);padding:12px 14px;margin:0 0 10px;box-shadow:var(--hig-shadow);scroll-margin-top:110px}
.lg-it:target{outline:2px solid var(--tint)}
.lg-h{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px;color:var(--mut)}
.lg-h .gid{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:700;color:var(--fg);font-size:14px}
.lg-t{margin:6px 0;font-size:16px;line-height:1.6}
.lg-d{display:grid;grid-template-columns:5.5em 1fr;gap:2px 8px;font-size:14px;line-height:1.55;margin:0}
.lg-d dt{color:var(--mut)}.lg-d dd{margin:0;overflow-wrap:anywhere}
.st{font-weight:600;border-radius:var(--r-cap,999px);padding:1px 8px;font-size:12px}
.st-有效{background:var(--hig-ok-fill);color:var(--hig-tx-green)}.st-受挑战{background:var(--hig-warn-fill);color:var(--hig-tx-orange)}
.st-证伪{background:var(--hig-risk-fill);color:var(--hig-tx-red)}.st-作废{background:var(--hig-gray-fill);color:var(--mut)}
.draft{background:var(--hig-est-fill);color:var(--hig-tx-purple);border-radius:var(--r-tag,5px);font-size:11px;font-weight:600;padding:1px 6px;margin-left:4px}
.ev{font-weight:600;border-radius:var(--r-tag,5px);font-size:11px;padding:1px 6px;margin-right:4px}
.ev-支持{background:var(--hig-ok-fill);color:var(--hig-tx-green)}.ev-削弱{background:var(--hig-warn-fill);color:var(--hig-tx-orange)}
.ev-触发证伪{background:var(--hig-risk-fill);color:var(--hig-tx-red)}.ev-待核{background:var(--hig-gray-fill);color:var(--mut)}
.lg-ev{list-style:none;padding:0;margin:0}.lg-ev li{margin:0 0 4px}
.lg-banner{background:var(--hig-est-fill);border-radius:var(--r-card,12px);padding:10px 14px;margin:10px 0;font-size:15px}
'''


def evli(e, gid=None):
    head = f'<a href="#{gid}">{gid}</a> ' if gid else ''
    return f'<li>{head}<span class="ev ev-{e["w"]}">{e["w"]}</span>{E(e["d"])} · {E(e["t"])} <a href="{E(e["src"])}" rel="noopener">来源</a></li>'


def week(items):
    ev = [(x['gid'], e) for x in items for e in x.get('ev', [])]
    if not ev:
        return ''
    last = max(e['d'] for _, e in ev)
    rows = [evli(e, g) for g, e in ev if e['d'] == last]
    return (f'<section><h2>最近一次周度跟踪 · {E(last)}</h2><p class="sub">只记录证据方向，不改状态和概率；改判要 John 批准。</p>'
            f'<ul class="lg-ev">{"".join(rows)}</ul></section>')


def render(doc):
    items = doc['items']
    J = [x for x in items if x['kind'] == '判断']
    P = [x for x in items if x['kind'] == '预测']
    live = [x for x in P if x['status'] != '作废']
    scored = [x for x in live if x['brier'] is not None]
    stc = collections.Counter(x['status'] for x in J)
    probs = [x['prob'] for x in live]
    bins = [(0, .3), (.3, .4), (.4, .5), (.5, .6), (.6, .7), (.7, .8), (.8, 1.01)]
    bl = ['<30', '30', '40', '50', '60', '70', '≥80']
    bc = [sum(lo <= p < hi for p in probs) for lo, hi in bins]
    mx = max(bc) or 1
    nxt = sorted((x for x in live if x['outcome'] == '待验证'), key=lambda x: x['due'])[:3]
    brier = f'{sum(x["brier"] for x in scored) / len(scored):.3f}' if scored else '—'
    hitr = f'{sum(x["outcome"] == "命中" for x in scored)}/{len(scored)}' if scored else '0/0'
    chains = ['HBM', 'CoWoS', 'PCB', '铜', '跨链']
    o = [f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 ledger/build.py 从 data/ledger.json 生成，不要手改 -->
<title>全局判断总账 · 产业链情报研究中心</title><meta name="description" content="所有产业链的核心判断与带日期预测：全局编号、证伪条件、到期日、概率与打分。">
<link rel="stylesheet" href="assets.css"><script src="theme.js"></script><link rel="stylesheet" href="assets/hig.css"><style>{CSS}</style></head><body>
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="hbm.html">HBM</a><a class="btn" href="world/">世界</a><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
<main class="wrap">
<section><div class="kicker">全局判断总账 · 更新 {E(doc["updated"])}</div><h1>我们说过什么，到期对不对</h1>
<p class="dek">四条链的核心判断（G 编号）和带日期的预测（P 编号）都在这一页。判断原文与各研究页一致；到期后按公开数据打分，只追加结果，不改原文。</p>
<div class="lg-banner"><b>概率初稿，待 John 确认</b>：{len(live)} 条预测的概率是 2026-10-22 起草的，每条附一句理由。确认或改动后，这行提示会去掉。</div>
<div class="lg-sum">
<div class="card"><b>{len(J)}</b><span>核心判断 · 有效 {stc["有效"]} · 受挑战 {stc["受挑战"]} · 证伪 {stc["证伪"]} · 作废 {stc["作废"]}</span></div>
<div class="card"><b>{len(P)}</b><span>带日期预测 · 进行中 {len(live)} · 作废 {len(P) - len(live)}</span></div>
<div class="card"><b>{hitr}</b><span>已打分（命中/总数）</span></div>
<div class="card"><b>{brier}</b><span>平均 Brier 分数（越低越好；全猜 50% 为 0.25）</span></div>
</div>
<p class="sub">概率分布（初稿，%）：平均 {sum(probs) / len(probs) * 100:.0f}%，按此预期约 {sum(probs):.0f} 条命中。</p>
<div class="lg-dist" aria-hidden="true">{"".join(f'<i style="height:{max(3, c / mx * 100):.0f}%" title="{c}"></i>' for c in bc)}</div>
<div class="lg-dl">{"".join(f'<span>{l}<br>{c} 条</span>' for l, c in zip(bl, bc))}</div>
<p class="sub">最近到期：{"；".join(f'<a href="#{x["gid"]}">{x["gid"]}</a> {x["due"]}' for x in nxt)}。</p>
</section>
{week(items)}
<section><h2>总账</h2>
<div class="lg-f"><select id="fk" aria-label="类型"><option value="">判断 + 预测</option><option>判断</option><option>预测</option></select>
<select id="fc" aria-label="链"><option value="">全部链</option>{"".join(f"<option>{c}</option>" for c in chains)}</select>
<select id="fs" aria-label="状态"><option value="">全部状态</option><option>有效</option><option>受挑战</option><option>证伪</option><option>作废</option></select>
<span class="lg-n" id="fn"></span></div>
<ol class="lg-list" id="lg">''']
    for x in items:
        dl = [('证伪条件', E(x['falsify']) + (f'<br><span class="note">阈值：{E(x["th"])}</span>' if x.get('th') and x['th'] != '—' else ''))]
        dl.append(('到期', E(x['due']) if x.get('due') else '—'))
        if x['kind'] == '预测':
            if x['prob'] is not None:
                dl.append(('概率', f'{x["prob"] * 100:.0f}%<span class="draft">{"初稿" if x.get("prob_state") == "初稿" else "已确认"}</span><br><span class="note">{E(x["reason"])}</span>'))
            elif x.get('reason'):
                dl.append(('作废说明', E(x['reason'])))
            dl.append(('结果', E(x['outcome']) + (f' · Brier {x["brier"]:.3f}' if x['brier'] is not None else '')))
        if x.get('ev'):
            dl.append(('证据记录', '<ul class="lg-ev">' + ''.join(evli(e) for e in sorted(x['ev'], key=lambda e: e['d'], reverse=True)) + '</ul>'))
        o.append(f'<li class="lg-it" id="{x["gid"]}" data-k="{x["kind"]}" data-c="{E(x["chain"])}" data-s="{x["status"]}">'
                 f'<div class="lg-h"><span class="gid">{x["gid"]}</span><span>旧编号 {E(x["old"])}</span><span>·</span><a href="{PAGE_MOVED.get(x["page"], x["page"])}">{E(x["chain"])}{"" if x["book"] == "全球" else " · 中国账本"}</a><span class="st st-{x["status"]}">{x["status"]}</span></div>'
                 f'<p class="lg-t">{E(x["text"])}</p><dl class="lg-d">' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in dl) + '</dl></li>')
    o.append('''</ol></section>
<section><h2>规则</h2><ul class="sub">
<li>状态：有效＝研究页上“未触发”；受挑战＝“需盯紧”，反方证据接近阈值；证伪＝证伪条件已触发；作废＝前提失效，原文保留。</li>
<li>打分：预测到期后填“命中/未中”，Brier =（概率 − 结果）²，命中记 1、未中记 0；平均值越低越准，0.25 等于每条都猜 50%。</li>
<li>编号：G01… 是核心判断，P001… 是带日期预测；旧编号（如 HBM-J1、铜-中国-N2）保留在每条里，研究页上的小标签链到这里。</li>
<li>改判断、改概率都要 John 批准；日报只写“读数支持/挑战 G05”，不在日报里改。</li></ul></section>
</main>
<footer class="wrap">Kiko 产业笔记 · 公开数据整理 · <b>本页为研究记录，不构成投资建议。</b></footer>
<script>(function(){var k=document.getElementById('fk'),c=document.getElementById('fc'),s=document.getElementById('fs'),n=document.getElementById('fn'),L=document.querySelectorAll('#lg>li');
function f(){var m=0;for(var i=0;i<L.length;i++){var e=L[i],ok=(!k.value||e.dataset.k==k.value)&&(!c.value||e.dataset.c==c.value)&&(!s.value||e.dataset.s==s.value);e.style.display=ok?'':'none';if(ok)m++}n.textContent='显示 '+m+' / '+L.length+' 条'}
k.onchange=c.onchange=s.onchange=f;var h=location.hash.slice(1);if(h&&document.getElementById(h)){}f()})();</script>
</body></html>
''')
    return ''.join(o)


def main():
    doc = load()
    errs = check(doc)
    if errs:
        print('总账检查不通过：'); [print('  ✗', e) for e in errs]
        raise SystemExit(1)
    doc = score(doc)
    json.dump(doc, open(os.path.join(ROOT, 'data', 'ledger.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(ROOT, 'ledger.html'), 'w', encoding='utf-8').write(render(doc))
    ids = {x['text']: x['gid'] for x in doc['items']}
    open(os.path.join(ROOT, 'ledger_ids.js'), 'w', encoding='utf-8').write(
        '/* 由 ledger/build.py 生成：研究页原文 → 全局编号（链到 ledger.html）。不要手改。 */\nwindow.LEDGER_IDS=' + json.dumps(ids, ensure_ascii=False, separators=(',', ':')) + ';\n')
    n = collections.Counter(x['kind'] for x in doc['items'])
    print(f'ledger: 判断 {n["判断"]} 条、预测 {n["预测"]} 条，全部对上研究页 → ledger.html、ledger_ids.js')


if __name__ == '__main__':
    main()
