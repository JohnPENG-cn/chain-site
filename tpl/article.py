"""阅读模式（article）模板助手 —— 参照 SemiAnalysis 长文版式，放在 HIG 设计系统里。
用法见 docs/READING_MODE.md。页面 <body class="article">，样式在 assets/hig.css 第 12 节，交互在 assets/reading.js。
这里只管"怎么摆"，不改内容：来源一个不丢，只是从正文行内标签挪到上标脚注 + 图表下一行来源 + 页末「来源与注释」。"""
import re

# 行内来源标签：<span class="tag t-src"><a href="#src12">源12</a> <a href="#src13">源13</a></span>
TAG_RE = re.compile(r'\s?<span class="tag t-src">((?:\s*<a href="([^"]*#src\d+)">源\d+</a>)+)\s*</span>')
A_RE = re.compile(r'<a href="([^"]*#src(\d+))">源\d+</a>')
FN_RE = re.compile(r'<sup class="fn">.*?</sup>', re.S)
EST = '<span class="tag t-est">估</span>'


def fn_sup(m):
    links = ''.join(f'<a class="fn-a" href="{h}" aria-label="来源 {n}">{n}</a>' for h, n in A_RE.findall(m.group(1)))
    return f'<sup class="fn">{links}</sup>'


def fnify(html):
    """把行内「源N」标签换成上标脚注（编号 = 页末来源表里的全局编号，稳定、可追溯）。"""
    return TAG_RE.sub(fn_sup, html)


def ids_in(html):
    """html 里引用到的来源编号（按首次出现排序，去重）。行内标签和已转换的上标都认。"""
    seen = []
    for h, n in A_RE.findall(html) + re.findall(r'class="fn-a" href="([^"]*#src(\d+))"', html):
        if (h, n) not in seen:
            seen.append((h, n))
    return seen


def short(title, n=26):
    t = re.split(r'[：:（(]', re.sub(r'<[^>]+>', '', title), 1)[0].strip()
    return t if len(t) <= n else t[:n - 1] + '…'


def src_line(html, titles, extra=''):
    """图表 / 表格下方一行灰字来源：「来源：Tushare 财务指标 93 · 巨潮年报 94」。titles: {编号: 标题}。"""
    ids = ids_in(html)
    if not ids and not extra:
        return ''
    parts = []
    for h, n in ids:
        nm = short(titles.get(int(n), '')) if h.startswith('#') else '见 CoWoS 页来源'
        parts.append(f'{nm} <a class="fn-a" href="{h}">{n}</a>')
    tail = f'<span class="sl-x">{extra}</span>' if extra else ''
    return f'<p class="src-line"><span class="sl-k">来源</span>{"；".join(parts)}{tail}</p>'


def strip_fn(html):
    """图注里的来源挪到下面的来源行后，图注本身去掉上标，读起来干净。"""
    return TAG_RE.sub('', FN_RE.sub('', html)).strip()


def figure(fid, title, chart, caption, titles, wide=True, extra=''):
    """全宽图：标题 + 图 + 一句话图注 + 一行来源（SemiAnalysis：图 → 'Source: X'）。"""
    return (f'<figure class="fig{" bleed" if wide else ""}" id="{fid}"><figcaption class="fig-t">{title}</figcaption>{chart}'
            f'<figcaption class="fig-c">{strip_fn(caption)}</figcaption>{src_line(caption, titles, extra)}</figure>\n')


def more(summary, body, titles=None, small='', open_=False, did='', wide=False):
    """展开细节：密集表格 / 证据默认收起，正文只留结论。"""
    sl = src_line(body, titles) if titles is not None else ''
    sm = f'<small>{small}</small>' if small else ''
    i = f' id="{did}"' if did else ''
    return f'<details class="more{" wide" if wide else ""}"{i}{" open" if open_ else ""}><summary><span>展开细节</span><b>{summary}</b>{sm}</summary><div class="more-b">{body}{sl}</div></details>\n'


def callout(text, label='本章判断'):
    """每章一句关键判断（只复述页面已有的判断，不新增）。"""
    return f'<aside class="pull"><span class="pull-k">{label}</span><p>{text}</p></aside>\n'


def chapter(cid, n, title, lead, nav='c'):
    """章头：大号章号 + 标题 + 导语。data-toc 给 reading.js 生成目录。"""
    return (f'<section id="{cid}" data-nav="{nav}" class="ch" data-toc="{n:02d} {re.split("[：:]", title)[0]}"><header class="ch-h"><span class="ch-n">{n:02d}</span>'
            f'<h2>{title}</h2></header><p class="lead">{lead}</p>\n')


def compare(rows, left, right, head='', extra=None):
    """并排对比：宽屏左右两栏，手机上下叠。rows = [(题, 左, 右, 尾注)]。"""
    o = [f'<div class="cmp">{head}']
    for r in rows:
        t, a, b = r[0], r[1], r[2]
        x = r[3] if len(r) > 3 and r[3] and r[3] != '—' else ''
        o.append(f'<div class="cmp-r"><h4>{t}</h4><div class="cmp-g"><div><span class="cmp-k">{left}</span>{a}</div><div class="me"><span class="cmp-k">{right}</span>{b}</div></div>'
                 + (f'<div class="cmp-x">{x}</div>' if x else '') + '</div>')
    o.append('</div>\n')
    return ''.join(o)


def stats(items):
    """关键数字一排：[(数, 说明html)]。说明里的来源变成上标。"""
    return '<div class="stat-row">' + ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in items) + '</div>\n'
