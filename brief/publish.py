#!/usr/bin/env python3
"""周五变化点简报 → 网站「简报」栏目（2026-10-30 起）。幂等。
用法: python3 brief/publish.py YYYYMMDD          # 生成 brief/<d>.html、brief/index.html、brief/pdf/brief_<d>.pdf（不提交，提交由人做）
源: $BRIEF_SRC/brief_<d>.md（默认 /workspace/research-pipeline/weekly_brief/）。格式：# 标题、> 读法、## 首屏（5 行，同日报口径）、
   ## 一、主要问题（≤3）/ 二、其他变化 / 三、总账本周读数 / 四、待 John 确认 / 五、一线校验 / 附件。正文 ≤1500 汉字（与日报同口径计数）。
PDF: 用日报 build_v3 的样式和 common.chrome 打印（CHROME=.../tools/chrome_pw.py 可替换）。"""
import os, sys, re, glob, json, html, markdown
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SITE, 'daily'))
import publish as dp  # 复用日报的首屏解析、计数、表格与编号链接
SRC = os.environ.get('BRIEF_SRC', '/workspace/research-pipeline/weekly_brief')
DR = os.environ.get('DAILY_REPORT', '/workspace/research-pipeline/daily_report')
OUT = os.path.join(SITE, 'brief')
DISC = dp.DISC
LIMIT = 1500

HEAD = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<!-- 由 brief/publish.py 生成，不要手改 -->
<title>{title} · 产业链情报研究中心</title><meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets.css"><link rel="stylesheet" href="../daily/daily.css"><script src="../theme.js"></script><link rel="stylesheet" href="../assets/hig.css"></head><body class="daily">
<header class="top"><div class="wrap"><a class="brand back" href="../" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="./">简报</a><a class="btn" href="../daily/">日报</a><a class="btn" href="../ledger.html">总账</a><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
'''
FOOT = dp.FOOT


def parse(d):
    f = f'{SRC}/brief_{d}.md'
    md = open(f, encoding='utf-8').read()
    title = re.search(r'^#\s+(.+)$', md, re.M).group(1).strip()
    body = re.sub(r'^#\s+.+\n', '', md, count=1)
    parts = re.split(r'(?m)^##\s+', body)
    intro, secs = parts[0], [(p.partition('\n')[0].strip(), p.partition('\n')[2]) for p in parts[1:]]
    fs = []
    for i, (hd, rest) in enumerate(secs):
        if hd.startswith('首屏'):
            fs = dp.parse_fs(rest); secs.pop(i); break
    if [k for k, _ in fs] != dp.FS_KEYS:
        raise SystemExit('首屏应为 5 行：' + ' / '.join(dp.FS_KEYS))
    n = dp.zh_count(secs)
    if n > LIMIT:
        raise SystemExit(f'正文 {n} 汉字 > {LIMIT}')
    if '不构成投资建议' not in md:
        raise SystemExit('缺免责声明')
    return dict(d=d, md=md, title=title, intro=intro, secs=secs, fs=fs, zh=n)


def render(r, pdf_ok):
    ds, wd = dp.fmt_date(r['d'])
    o = [HEAD.format(title=html.escape(f'简报 {ds}'), desc=html.escape(dp.short(dict(r['fs'])['主线'], 140)))]
    navs = [('top', '首屏')] + [(dp.slug(i), dp.nav_label(n)) for i, (n, _) in enumerate(r['secs'])]
    o.append('<nav class="sec"><div class="wrap">' + ''.join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in navs) + '</div></nav>\n<main class="wrap rpt">\n')
    o.append(f'<section id="top" class="hero"><div class="kicker">周五变化点简报 · {ds} {wd}</div><h1 class="dt">{html.escape(dp.strip_md(r["title"]))}</h1>')
    o.append('<div class="fs" role="region" aria-label="首屏"><div class="fs-h">首屏 · 五行读懂本周</div><dl>'
             + ''.join(f'<div class="fs-r"><dt>{html.escape(k)}</dt><dd>{dp.link_ids(dp.inline(v))}</dd></div>' for k, v in r['fs']) + '</dl></div>')
    o.append('<div class="acts">' + (f'<a class="btn" href="pdf/brief_{r["d"]}.pdf" download>下载 PDF</a>' if pdf_ok else '') + '<a class="btn" href="./">全部简报</a></div>')
    o.append(f'<p class="disc">{DISC}</p></section>\n')
    intro = r['intro'].strip()
    if intro:
        o.append('<div class="intro">' + dp.postproc(markdown.markdown(intro), r['d']) + '</div>\n')
    for i, (hd, body) in enumerate(r['secs']):
        h = markdown.markdown(f'## {hd}\n{body}', extensions=['tables'])
        h = dp.link_ids(dp.tables(dp.postproc(h, r['d'])))
        o.append(f'<section id="{dp.slug(i)}">{h}</section>\n')
    o.append('</main>\n' + FOOT)
    return ''.join(o)


def pdf(r):
    sys.path.insert(0, DR)
    from common import chrome
    from build_v3 import CSS
    hp = f'{SRC}/brief_{r["d"]}.html'; pp = f'{SRC}/brief_{r["d"]}.pdf'
    h = markdown.markdown(r['md'], extensions=['tables', 'sane_lists'])
    open(hp, 'w', encoding='utf-8').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
    chrome([f'--print-to-pdf={pp}', '--no-pdf-header-footer', 'file://' + hp], timeout=180)
    if not os.path.exists(pp):
        raise SystemExit('PDF 失败')
    return pp


def index():
    items = sorted((os.path.basename(f)[6:14] for f in glob.glob(f'{SRC}/brief_*.md')), reverse=True)
    o = [HEAD.format(title='周五变化点简报', desc='每周五：本周变了什么、对全局判断总账意味着什么')]
    o.append('<main class="wrap rpt"><section class="hero"><div class="kicker">Weekly Brief · 每周五</div><h1 class="dt">周五变化点简报</h1>'
             '<p class="dek">一屏读完：本周最多 3 个主要问题、其他变化、总账证据（不改概率）、待 John 确认、一线校验问题。</p>'
             f'<p class="disc">{DISC}</p></section><section><ol class="dl">')
    for d in items:
        if not os.path.exists(f'{OUT}/{d}.html'):
            continue
        ds, wd = dp.fmt_date(d); r = parse(d)
        o.append(f'<li><a class="card" href="{d}.html"><div class="dh"><b>{ds}</b><span>{wd}</span></div><p>{html.escape(dp.short(dict(r["fs"])["主线"]))}</p></a>'
                 f'<div class="lk"><a href="{d}.html">阅读</a>' + (f'<a href="pdf/brief_{d}.pdf" download>PDF</a>' if os.path.exists(f'{OUT}/pdf/brief_{d}.pdf') else '') + '</div></li>')
    o.append('</ol></section></main>\n' + FOOT)
    open(f'{OUT}/index.html', 'w', encoding='utf-8').write(''.join(o))


def main():
    d = sys.argv[1]
    r = parse(d)
    pp = pdf(r)
    import shutil
    ok = os.path.getsize(pp) <= dp.MAXPDF
    if ok:
        shutil.copyfile(pp, f'{OUT}/pdf/brief_{d}.pdf')
    open(f'{OUT}/{d}.html', 'w', encoding='utf-8').write(render(r, ok))
    index()
    print(f'正文 {r["zh"]} 汉字；{OUT}/{d}.html；PDF {pp} ({os.path.getsize(pp)/1e6:.2f} MB)')


if __name__ == '__main__':
    main()
