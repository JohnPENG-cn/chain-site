#!/usr/bin/env python3
"""A股投研日报 → 网站「日报」栏目。幂等：重跑任意次结果相同。

用法:
  python3 daily/publish.py YYYYMMDD           # 发布当日：生成页面、更新索引、提交 'daily: YYYYMMDD' 并推送
  python3 daily/publish.py YYYYMMDD --no-push # 只生成和提交，不推送
  python3 daily/publish.py --all --no-git     # 用 daily_report 里所有现存源重建全部日报页（不提交）

源（由 /workspace/daily_report/build_v3.py 产出，不抓 PDF）:
  report_<d>_<ver>.md  （ver 取最高版本 v4 > v3；正文 + 附录，已合成好的 markdown）
  report_<d>_meta.json （规则引擎“数据速览”，正文没有「今日市场概况」节时用它兜底）
  ladder_<d>.png / chart_sector_<d>.png / chart_flow_<d>.png
  report_<d>_<ver>.pdf （>3MB 不入库，只给网页）
产物（仓库内）: daily/<d>.html、daily/index.html、daily/reports.json、daily/img/*.png、daily/pdf/*.pdf；首页 <!--daily:latest--> 卡片。
"""
import sys, os, re, json, glob, shutil, subprocess, html, datetime
import markdown

SRC = os.environ.get('DAILY_SRC', '/workspace/daily_report')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, 'daily')
MAXPDF = 3 * 1024 * 1024
WD = '一二三四五六日'
DISC = '本报告为基于公开数据的研究分析，不构成投资建议。'


def pick_md(d):
    c = []
    for f in glob.glob(f'{SRC}/report_{d}_v*.md'):
        m = re.fullmatch(rf'report_{d}_v(\d+)\.md', os.path.basename(f))
        if m and int(m.group(1)) >= 3:
            c.append((int(m.group(1)), f))
    return max(c)[1] if c else None


def load_meta(d):
    for f in [f'{SRC}/report_{d}_meta.json'] + sorted(glob.glob(f'{SRC}/report_{d}_v*_meta.json'), reverse=True):
        if os.path.exists(f):
            try:
                return json.load(open(f, encoding='utf-8'))
            except Exception:
                pass
    return {}


def fmt_date(d):
    t = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
    return f'{t.year}-{t.month:02d}-{t.day:02d}', f'周{WD[t.weekday()]}'


def strip_md(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    return re.sub(r'[*`]', '', s).strip()


def short(s, n=150):
    s = strip_md(s)
    return s if len(s) <= n else s[:n].rstrip('，、；：') + '…'


def inline(s):
    return markdown.markdown(s).removeprefix('<p>').removesuffix('</p>')


def slug(i):
    return f's{i}'


def postproc(h, d):
    # 图片 → img/，加 lazy/alt 说明
    h = re.sub(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>',
               lambda m: f'<figure><a href="img/{os.path.basename(m.group(2))}"><img src="img/{os.path.basename(m.group(2))}" alt="{m.group(1)}" loading="lazy"></a><figcaption>{m.group(1)} · 点图放大</figcaption></figure>', h)
    # 来源链接 → 小号角标
    h = re.sub(r'<a href="([^"]+)">来源</a>', r'<a class="src" href="\1" target="_blank" rel="noopener">源</a>', h)
    h = h.replace('【推断】', '<span class="tag t-est">推断</span>')
    # 结论框
    h = re.sub(r'<blockquote>\s*<p><strong>结论</strong>', '<blockquote class="cc"><p><strong>结论</strong>', h)
    # 去 PDF 分页符与 HTML 注释
    h = re.sub(r'<div style="page-break-before:always"></div>', '', h)
    h = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    return h


def tables(h):
    """附录里的数字表 → 横向可滑；正文表 → 手机端卡片（每格带列名）。"""
    out, pos, in_apx = [], 0, False
    for m in re.finditer(r'<table>.*?</table>|<h2 id="[^"]*">附录', h, flags=re.S):
        out.append(h[pos:m.start()]); pos = m.end(); t = m.group(0)
        if t.startswith('<h2'):
            in_apx = True; out.append(t); continue
        heads = [strip_md(re.sub('<[^>]+>', '', x)) for x in re.findall(r'<th[^>]*>(.*?)</th>', t, flags=re.S)]
        if in_apx or len(heads) > 5:
            out.append(f'<div class="tbl num">{t}</div>')
        else:
            def row(rm):
                cells = re.findall(r'<td([^>]*)>(.*?)</td>', rm.group(1), flags=re.S)
                return '<tr>' + ''.join(f'<td data-l="{html.escape(heads[i] if i < len(heads) else "")}"{a}>{c}</td>' for i, (a, c) in enumerate(cells)) + '</tr>'
            t = re.sub(r'<tr>((?:(?!</tr>).)*<td.*?)</tr>', row, t, flags=re.S)
            out.append(f'<div class="tbl"><table class="rc">{t[7:]}</div>')
    out.append(h[pos:])
    return ''.join(out)


def parse(d):
    f = pick_md(d)
    if not f:
        return None
    ver = re.search(r'_v(\d+)\.md$', f).group(1)
    md = open(f, encoding='utf-8').read()
    meta = load_meta(d)
    title = (re.search(r'^#\s+(.+)$', md, re.M) or [None, f'A股投研日报 · {d}'])[1].strip()
    mm = re.search(r'\*\*一句话主线[：:]\s*(.+?)\*\*', md)
    mainline = mm.group(1).strip() if mm else ''
    # 拆成 头部 + 各 h2 节
    body = re.sub(r'^#\s+.+\n', '', md, count=1)
    parts = re.split(r'(?m)^##\s+', body)
    intro, secs = parts[0], []
    for p in parts[1:]:
        hd, _, rest = p.partition('\n')
        secs.append((hd.strip(), rest))
    if mm:
        intro = intro.replace(mm.group(0), '')
    return dict(d=d, ver=ver, md=md, meta=meta, title=title, mainline=mainline, intro=intro, secs=secs, src=f)


def nav_label(hd):
    s = strip_md(hd)
    s = re.sub(r'^[一二三四五六七八九十]+、', '', s)
    s = re.split(r'[：:（(——]', s)[0].strip()
    return s[:8] or strip_md(hd)[:8]


HEAD = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="format-detection" content="telephone=no">
<!-- 由 daily/publish.py 生成，不要手改 -->
<title>{title} · 产业链情报研究中心</title><meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets.css"><link rel="stylesheet" href="daily.css"><script src="../theme.js"></script></head><body class="daily">
<header class="top"><div class="wrap"><a class="brand" href="../"><b>●</b> 产业链情报</a><span class="sp"></span><a class="btn" href="./">日报</a><a class="btn" href="../hbm.html">HBM</a><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
'''
FOOT = '<footer class="wrap">Kiko 产业笔记 · 公开数据整理 · <b>' + DISC + '</b></footer></body></html>\n'


def render_day(r, prev, nxt, pdf_ok):
    d = r['d']; ds, wd = fmt_date(d)
    o = [HEAD.format(title=html.escape(f'日报 {ds}'), desc=html.escape(short(r['mainline'], 140)))]
    names = [s[0] for s in r['secs']]
    has = lambda k: any(k in n for n in names)
    navs = [('top', '主线')]
    if not has('今日市场概况') and r['meta'].get('conclusion'):
        navs.append(('mkt', '市场概况'))
    if not has('变化点'):
        navs.append(('chg', '变化点'))
    navs += [(slug(i), nav_label(n)) for i, n in enumerate(names)]
    if pdf_ok:
        navs.append(('pdf', 'PDF'))
    o.append('<nav class="sec"><div class="wrap">' + ''.join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in navs) + '</div></nav>\n<main class="wrap rpt">\n')
    o.append(f'<section id="top" class="hero"><div class="kicker">A股投研日报 · {ds} {wd}</div>')
    o.append(f'<h1 class="dt">{html.escape(strip_md(r["title"]))}</h1>')
    if r['mainline']:
        o.append(f'<div class="ml"><span class="lb">一句话主线</span><p>{inline(r["mainline"])}</p></div>')
    o.append('<div class="acts">' + (f'<a class="btn" href="pdf/report_{d}.pdf" download>下载 PDF</a>' if pdf_ok else '') + '<a class="btn" href="./">全部日报</a></div>')
    o.append(f'<p class="disc">{DISC}</p></section>\n')
    if not has('今日市场概况') and r['meta'].get('conclusion'):
        o.append('<section id="mkt"><h2>今日市场概况</h2><p class="sub">数据管道速览（Tushare 收盘数据，规则生成，正文判断见下文）</p><ul class="mk">'
                 + ''.join(f'<li>{inline(c)}</li>' for c in r['meta']['conclusion']) + '</ul></section>\n')
    if not has('变化点'):
        chg = [(i, n) for i, n in enumerate(names) if re.match(r'^[一二三四五六七八九十]+、变化', n) or n.startswith('变化')]
        if chg:
            o.append('<section id="chg"><h2>变化点</h2><div class="kl">' + ''.join(
                f'<a href="#{slug(i)}"><span class="i">{k}</span><span>{inline(re.sub(r"^[一二三四五六七八九十]+、", "", n))}</span></a>' for k, (i, n) in enumerate(chg, 1)) + '</div></section>\n')
    intro = r['intro'].strip()
    if intro:
        o.append('<div class="intro">' + postproc(markdown.markdown(intro, extensions=['tables']), d) + '</div>\n')
    for i, (hd, body) in enumerate(r['secs']):
        cls = ' class="apxsec"' if hd.startswith('附录') else ''
        h = markdown.markdown(f'## {hd}\n{body}', extensions=['tables'])
        h = h.replace('<h2>', f'<h2 id="h{i}">', 1)
        h = tables(postproc(h, d))
        if '四层' in body or '第1层' in body:
            h = re.sub(r'<h3>(第(\d)层[^<]*)</h3>', lambda m: f'<h3 class="ly ly{m.group(2)}">{m.group(1)}</h3>', h)
        o.append(f'<section id="{slug(i)}"{cls}>{h}</section>\n')
    if pdf_ok:
        o.append(f'<section id="pdf"><h2>下载</h2><p><a class="btn" href="pdf/report_{d}.pdf" download>下载当日 PDF</a></p></section>\n')
    pn = '<nav class="pn">' + (f'<a href="{prev}.html">← {fmt_date(prev)[0]}</a>' if prev else '<span></span>') + '<a href="./">全部日报</a>' + (f'<a href="{nxt}.html">{fmt_date(nxt)[0]} →</a>' if nxt else '<span></span>') + '</nav>'
    o.append(pn + '</main>\n' + FOOT)
    return ''.join(o)


def render_index(items):
    o = [HEAD.format(title='日报', desc='A股投研日报：每个交易日 20:00 更新')]
    o.append('<main class="wrap rpt"><section class="hero"><div class="kicker">A-share Daily · 每个交易日 20:00</div><h1 class="dt">A股投研日报</h1>'
             '<p class="dek">四层认知阶梯：看价格 → 看机制 → 想套利 → 布局产业。每天挑 1–2 个最重要的变化，写清供需机制、可证伪的验证点，以及和产业链页面（HBM / CoWoS）的联系。</p>'
             f'<p class="disc">{DISC}</p></section><section><ol class="dl">')
    for it in items:
        ds, wd = fmt_date(it['date'])
        o.append(f'<li><a class="card" href="{it["date"]}.html"><div class="dh"><b>{ds}</b><span>{wd}</span>' + ('<span class="pill new">最新</span>' if it is items[0] else '') + '</div>'
                 f'<p>{html.escape(it["short"])}</p></a><div class="lk"><a href="{it["date"]}.html">阅读</a>' + (f'<a href="pdf/report_{it["date"]}.pdf" download>PDF</a>' if it.get('pdf') else '') + '</div></li>')
    o.append('</ol></section></main>\n' + FOOT)
    return ''.join(o)


def build(d):
    r = parse(d)
    if not r:
        raise SystemExit(f'找不到 {SRC}/report_{d}_v3.md（先跑 build_v3.py {d}）')
    os.makedirs(f'{OUT}/img', exist_ok=True); os.makedirs(f'{OUT}/pdf', exist_ok=True)
    for im in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', r['md']):
        s = os.path.join(SRC, os.path.basename(im))
        if os.path.exists(s):
            dst = f'{OUT}/img/{os.path.basename(im)}'
            if not os.path.exists(dst) or open(s, 'rb').read() != open(dst, 'rb').read():
                shutil.copyfile(s, dst)
        else:
            print('  缺图', s)
    pdf = r['src'][:-3] + '.pdf'; pdst = f'{OUT}/pdf/report_{d}.pdf'; pdf_ok = False
    if os.path.exists(pdf) and os.path.getsize(pdf) <= MAXPDF:
        if not os.path.exists(pdst) or open(pdf, 'rb').read() != open(pdst, 'rb').read():
            shutil.copyfile(pdf, pdst)
        pdf_ok = True
    elif os.path.exists(pdf):
        print(f'  PDF {os.path.getsize(pdf)/1e6:.1f}MB > 3MB，不入库')
        if os.path.exists(pdst):
            os.remove(pdst)
    return r, pdf_ok


def main():
    a = sys.argv[1:]
    nogit, nopush = '--no-git' in a, '--no-push' in a
    days = [x for x in a if re.fullmatch(r'\d{8}', x)]
    man_f = f'{OUT}/reports.json'
    man = {it['date']: it for it in (json.load(open(man_f, encoding='utf-8')) if os.path.exists(man_f) else [])}
    if '--all' in a:
        days = sorted({re.search(r'report_(\d{8})_v', f).group(1) for f in glob.glob(f'{SRC}/report_*_v*.md') if pick_md(re.search(r'report_(\d{8})_v', f).group(1))})
    if not days:
        raise SystemExit(__doc__)
    built = {}
    for d in days:
        r, pdf_ok = build(d)
        built[d] = (r, pdf_ok)
        man[d] = {'date': d, 'ver': 'v' + r['ver'], 'mainline': strip_md(r['mainline']), 'short': short(r['mainline']), 'pdf': pdf_ok}
    order = sorted(man)
    # 重写本次的页面 + 相邻页（上一篇/下一篇链接），源还在才重写
    todo = set(days)
    for d in days:
        i = order.index(d)
        if i > 0: todo.add(order[i - 1])
    for d in sorted(todo):
        if d not in built:
            if not pick_md(d):
                continue
            built[d] = build(d)
        i = order.index(d)
        r, pdf_ok = built[d]
        open(f'{OUT}/{d}.html', 'w', encoding='utf-8').write(render_day(r, order[i - 1] if i else None, order[i + 1] if i + 1 < len(order) else None, pdf_ok))
        print('  页面', f'daily/{d}.html')
    items = [man[d] for d in reversed(order)]
    json.dump(items, open(man_f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(f'{OUT}/index.html', 'w', encoding='utf-8').write(render_index(items))
    # 首页卡片
    idx_f = f'{SITE}/index.html'; idx = open(idx_f, encoding='utf-8').read()
    lt = items[0]; ds, wd = fmt_date(lt['date'])
    card = f'<a class="card" href="daily/{lt["date"]}.html" style="color:inherit;text-decoration:none;display:block"><div class="kicker">最新 · {ds} {wd}</div><p style="margin:.3em 0 8px;font-size:15px">{html.escape(lt["short"])}</p><span class="pill">共 {len(items)} 期 · 每个交易日 20:00</span></a>'
    idx, n = re.subn(r'(<!--daily:latest-->).*?(<!--/daily-->)', lambda m: m.group(1) + card + m.group(2), idx, flags=re.S)
    assert n == 1, 'index.html 缺 <!--daily:latest--> 标记'
    open(idx_f, 'w', encoding='utf-8').write(idx)
    print('索引', f'daily/index.html（{len(items)} 期）')
    if nogit:
        return
    g = lambda *c: subprocess.run(['git', '-C', SITE, *c], check=True, capture_output=True, text=True).stdout
    g('add', 'daily', 'index.html')
    if not g('diff', '--cached', '--name-only').strip():
        print('无变化，不提交。')
    else:
        msg = 'daily: ' + (days[-1] if len(days) == 1 else f'{days[0]}-{days[-1]}')
        g('commit', '-m', msg, '--', 'daily', 'index.html')
        print('提交', g('rev-parse', '--short', 'HEAD').strip(), msg)
    if not nopush:
        subprocess.run(['git', '-C', SITE, 'push', 'origin', 'HEAD'], check=True)
        print('已推送：https://johnpeng-cn.github.io/chain-site/daily/' + days[-1] + '.html')


if __name__ == '__main__':
    main()
