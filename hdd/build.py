#!/usr/bin/env python3
"""HDD 链库页 hdd.html（v0.1，一页总览，待补较多）。
外壳用 tpl/page_v4.py 的 head / topbar / nav_html（导航里 HDD 只有 1 页）。
来源：复用 explain/hdd.py 的来源表 + 本页 A 股映射的 4 条；链库节点数字读 data/chains.json、data/layers.json（hdd/add_node.py 生成）。
本页不写入任何判断：建议判断只列在「待 John 确认」，不进总账。改内容改本文件后跑 ./build.sh。"""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tpl')); sys.path.insert(0, os.path.join(ROOT, 'explain'))
os.chdir(ROOT)
import page_v4 as T
import hdd as X   # explain/hdd.py

VER, DATE = 'v0.1', '2026-10-29'
SRC = {k: v for k, v in X._ALL.items() if not k.startswith('x_')}
SRC.update({
    'ys': ('新浪财经 · 董秘问答：宁波韵升谈 HDD 磁材需求（2026-06-17）', 'https://finance.sina.com.cn/stock/relnews/dongmiqa/2026-06-17/doc-inictaex2856744.shtml'),
    'lens': ('同花顺：蓝思科技 HDD 玻璃盘片客户验证、小批量出货（2026-10-28）', 'https://yuanchuang.10jqka.com.cn/20261028/c681196391.shtml'),
    'kf_n': ('同花顺：深科技 2025 年盘基片销量大幅增长（2026-06-18）', 'https://news.10jqka.com.cn/20260618/c677578666.shtml'),
    'kf_ar': ('深科技 2025 年年度报告（深交所披露，2026-04-29）', 'https://disc.static.szse.cn/download/disc/disk03/finalpage/2026-04-29/4af384f1-22b1-446d-ad13-b40719c6b05c.PDF'),
})
ORDER = []


def s(k):
    assert k in SRC, k
    if k not in ORDER:
        ORDER.append(k)
    i = ORDER.index(k) + 1
    return f'<sup class="fn"><a aria-label="来源 {i}" class="fn-a" href="#src{i}">{i}</a></sup>'


def node():
    """链库节点：只读脚本算好的数，不在这里算判断。"""
    try:
        C = json.load(open('data/chains.json', encoding='utf-8'))
        L = json.load(open('data/layers.json', encoding='utf-8'))
    except Exception:
        return None, None, None
    hit = None
    def walk(o):
        nonlocal hit
        if isinstance(o, dict):
            if o.get('node') == 'HDD硬盘' and 'stocks' in o:
                hit = o
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(C)
    lay = next((v for k, v in (L.get('nodes') or {}).items() if k.endswith('|HDD硬盘')), None)
    return hit, lay, C.get('date') or C.get('trade_date')


def build():
    nd, lay, day = node()
    ROLE = {
        '000021.SZ': ('深科技', f'苏州子公司做磁头和 HDD 电路板；深科技精密做盘基片（铝基板）{s("kf_ar")}。2025 年盘基片销量大幅增长 {s("kf_n")}。', 'HDD 业务占营收多少：待补。公司主业还有存储封测和电子代工。'),
        '600366.SH': ('宁波韵升', f'做钕铁硼磁钢，用在硬盘的音圈电机（VCM）上，不做硬盘 {s("ys")}。', '董秘称 HDD 出货稳定，没有 AI 带来的爆发式增长；2026 上半年有过缺货。份额：待补。'),
        '300433.SZ': ('蓝思科技', f'HDD 玻璃盘片在客户验证，小批量出货 {s("lens")}。', '量产时间未披露；营收大头是手机等消费电子玻璃，HDD 占比：待补。'),
    }
    rows = []
    for code, (nm, what, gap) in ROLE.items():
        st = next((x for x in (nd or {}).get('stocks', []) if x['code'] == code), None)
        d20 = f'{st["d20"]:+.2f}%' if st else '待补'
        rows.append(f'<tr><td><b>{nm}</b><br><small>{code}</small></td><td>{what}</td><td>{gap}</td><td>{d20}</td></tr>')
    if nd:
        nodeline = (f'<p>链库节点“HDD硬盘”（上游）用这 3 只股票算。截至 {(day or "")[:4]}-{(day or "")[4:6]}-{(day or "")[6:]}，近 20 个交易日平均涨跌 {nd["d20"]:+.2f}%，'
                    f'相当于每 100 元市值变成约 {100 + nd["d20"]:.0f} 元。</p>')
        if lay:
            nodeline += (f'<p>产业端信号（脚本按 3 家财报自动算）：<b>{html.escape(lay.get("signal", "待补"))}</b>'
                         f'（{"；".join(html.escape(w) for w in lay.get("why", []))}；报告期 {lay.get("report", "待补")}）。'
                         f'注意：这 3 家都不是纯 HDD 公司，信号反映的是整家公司，不只是 HDD 业务。</p>')
    else:
        nodeline = '<p>链库节点数据：待补（拉数据失败）。</p>'

    secs = []
    def sec(i, sid, title, body, cls='ch'):
        assert len(title) <= 15, title
        secs.append(f'<section id="{sid}" class="{cls}" data-toc="{i:02d} {title}"><header class="ch-h"><span class="ch-n">{i:02d}</span><h2>{title}</h2></header>{body}</section>\n')

    hero = (f'<section id="top" class="hero" data-toc="01 一分钟看懂"><div class="kicker">HDD 研究 · 一页总览 · {VER} · {DATE}</div>'
            '<h1>HDD：AI 的数据，大多存在机械硬盘里</h1>'
            '<p class="howto">怎么读：这是第一版，只有一页。先看“一分钟看懂”。想知道硬盘怎么工作，看'
            '<a href="explain-hdd.html">原理图：硬盘怎么存</a>。小号上标数字是来源，点一下就能看。标“待补”的是还没查到的；标“弱”的是二手转述。公开数据整理，<b>不构成投资建议</b>。</p>'
            '<div class="onemin" id="onemin"><span class="pull-k">一分钟看懂</span><ol>'
            f'<li><span class="om-k">是什么</span>机械硬盘（HDD）用旋转的磁盘存数据。每 TB 比固态硬盘（SSD）便宜很多。纪要称 2026 年约便宜 15 倍（弱）{s("jpm")}。</li>'
            f'<li><span class="om-k">为什么和 AI 有关</span>AI 产生的数据大多很少被读，但要长期存。希捷称超大规模云厂超过 90% 的数据放在 HDD 上 {s("stxb")}。</li>'
            f'<li><span class="om-k">现在的状态</span>缺货。近线硬盘交期约 50 周，正常约 16 周 {s("tf_lt")}。相当于下单后快一年才到货。</li>'
            f'<li><span class="om-k">钱在哪</span>整机只有三家：西部数据、希捷、东芝。两家美国公司本季毛利率都在 58% 左右 {s("wdc_q")}。</li>'
            '<li><span class="om-k">什么算我们错</span>本页还没有入账的判断，所以还没有“证伪条件”。建议判断见下面“待 John 确认”。</li>'
            '</ol></div></section>\n')

    sec(2, 'five', '五句话说清楚', '<ol class="ov5">'
        f'<li><span class="fj f">事实</span>大容量硬盘一代代变大：希捷 30TB（2024）{s("moz3pr")} → 44TB（2026）{s("moz4")}。</li>'
        f'<li><span class="fj f">事实</span>变大靠新写入技术。希捷用 HAMR（用激光加热再写）{s("moz3")}；西部数据计划 2027 年上半年量产 HAMR {s("wdc_t")}。</li>'
        f'<li><span class="fj f">事实</span>价格在涨：西部数据每 TB 价格同比涨 28% {s("wdc_t")}。希捷说 2027 年价格已经谈定 {s("stx_t")}。</li>'
        f'<li><span class="fj f">事实</span>扩产慢：新建一座厂至少要两年（二手转述，弱）{s("lb")}。</li>'
        f'<li><span class="fj j">推断</span>我们推断：整机厂和独家零件厂议价力最强，因为玩家少、扩产慢。这只是推断，未入账。</li>'
        '</ol>')

    sec(3, 'map', '链条地图：谁做什么',
        '<p>一块硬盘由这些主要零件组成。每一环能做的公司很少。</p>'
        '<div class="tbl"><table><thead><tr><th>环节</th><th>谁在做</th><th>集中度</th></tr></thead><tbody>'
        f'<tr><td>整机</td><td>西部数据、希捷、东芝</td><td>2025 年台数份额 42.3% / 40.8% / 17.0%（弱）{s("cough")}</td></tr>'
        f'<tr><td>磁头（读写数据的“笔尖”）</td><td>希捷、西部数据自制；TDK 对外卖</td><td>弱 {s("lb")}；A 股深科技做磁头制造</td></tr>'
        f'<tr><td>介质（盘片上的磁性涂层）</td><td>整机厂自制 + Resonac</td><td>Resonac 是唯一对外卖的厂 {s("reso")}</td></tr>'
        f'<tr><td>玻璃基板（盘片的底子）</td><td>HOYA；蓝思在验证</td><td>HOYA 自称唯一 {s("hoya")}</td></tr>'
        f'<tr><td>铝基板</td><td>深科技精密等</td><td>份额：待补 {s("kf_ar")}</td></tr>'
        f'<tr><td>主轴电机（让盘片转的电机）</td><td>尼得科</td><td>70% 以上 {s("nidec")}</td></tr>'
        f'<tr><td>音圈电机磁钢（推磁头臂的磁铁）</td><td>宁波韵升等</td><td>份额：待补 {s("ys")}</td></tr>'
        '</tbody></table></div>'
        '<p class="note">中国大陆目前没有自主的整机厂（弱）。A 股公司都在零件环节。</p>')

    sec(4, 'ashare', 'A 股映射', '<p>下面 3 家公司和 HDD 有直接业务关系。它们都不是纯 HDD 公司。</p>'
        '<div class="tbl"><table><thead><tr><th>公司</th><th>在 HDD 链里做什么</th><th>还不知道的</th><th>近 20 日</th></tr></thead><tbody>'
        + ''.join(rows) + '</tbody></table></div>' + nodeline +
        '<p class="note">兴民智通没放进来：它收购 PCPL 的交易 2022 年已经终止。</p>')

    sec(5, 'todo', '待补清单', '<ul>'
        '<li>三家 A 股公司 HDD 业务占营收的比例。</li>'
        '<li>西部数据 40TB ePMR 每张盘片的容量。</li>'
        '<li>希捷每碟 10TB（约 100TB 整盘）的年份。</li>'
        '<li>磁头、介质、VCM 磁钢的全球份额（现有数字多为二手）。</li>'
        '<li>近线 HDD 价格的连续时间序列（现在只有几个时点）。</li>'
        '<li>2025 年份额原文（Forbes 页本站打不开，只看到搜索摘要）。</li>'
        '</ul>')

    sec(6, 'confirm', '待 John 确认', '<p>下面是建议的判断。<b>还没有写进总账</b>，也没有概率。确认后才入账。</p><ol>'
        f'<li>近线 HDD 每 TB 价格 2027 年继续同比上涨。依据：2027 年价格已谈定 {s("stx_t")}。</li>'
        f'<li>西部数据 HAMR 2027 年上半年开始量产出货。依据：公司电话会表态 {s("wdc_t")}。</li>'
        f'<li>2027 年 HDD 和 SSD 每 GB 价差仍大于 5 倍。依据：纪要称 2026 年约 15 倍（弱）{s("jpm")}。</li>'
        '</ol>')

    sec(7, 'how', '怎么读这一页', '<ul>'
        '<li>“事实”有来源；“推断”是我们的看法，未入账。</li>'
        '<li>“弱”= 二手转述或纪要，原文没核到。</li>'
        '<li>股价数字由脚本从行情数据算出，不是推荐。</li>'
        '<li>公开数据整理，<b>不构成投资建议</b>。</li>'
        '</ul>')

    src = ''.join(f'<li id="src{i}"><a href="{html.escape(SRC[k][1])}" target="_blank" rel="noopener">{html.escape(SRC[k][0])}</a></li>' for i, k in enumerate(ORDER, 1))
    secs.append('<section id="apx" class="ch" data-toc="08 来源"><header class="ch-h"><span class="ch-n">08</span><h2>来源</h2></header>'
                f'<div class="body" id="src"><p class="sub">均于 2026-10-28/29 打开核对；标“弱”的是二手或只看到摘要。</p><ol class="src">{src}</ol></div></section>\n')

    main = hero + ''.join(secs)
    ids = re.findall(r'\bid="([^"]+)"', main)
    assert len(ids) == len(set(ids)), 'id 重复'
    for m in re.findall(r'href="#(src\d+)"', main):
        assert f'id="{m}"' in main, m
    T.use('hdd')
    css = T.V3.CSS2 + T.PM.CSS + T.V3.CSS3 + T.CSS4
    page = (T.head('HDD 总览', 'HDD 硬盘产业链一页总览：原理、格局、A 股映射、待补与待确认清单（v0.1）', css, '', 'hdd.html')
            + '<body class="article chain" data-src-page="hdd.html" data-page="HDD 总览">\n' + T.topbar('HDD 总览', f'{VER} · {DATE}')
            + T.nav_html('hdd.html')
            + '<main class="wrap">\n' + main + '</main>\n<footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">链库</a> · <a href="explain-hdd.html">原理图：硬盘怎么存</a> · <a href="ledger.html">总账</a></footer>\n'
            + '<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n'
            + '<script src="assets/reading.js"></script>\n</body></html>\n')
    open('hdd.html', 'w', encoding='utf-8').write(page)
    print(f'hdd: hdd.html（{len(ORDER)} 条来源；节点数据 {"有" if nd else "无"}）')


if __name__ == '__main__':
    build()
