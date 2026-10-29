#!/usr/bin/env python3
"""AI 泡沫监控页 ai-bubble.html（世界看板的一个分页，2026-10-29 起）。
读数来自 world/ai_bubble.json：由 research-pipeline 的 world_indicators/wi/bubble.py 每天随世界看板一起现算（本文件不联网、不算数）。
框架参考国信证券策略专题（2026-07-09）及其后续两篇；只借思路，不抄原文、不放 PDF。
本页不改总账里的任何判断和概率：建议的新预测只列在「待 John 确认」。外壳用 tpl/page_v4.py（同 hdd.html）。"""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tpl'))
os.chdir(ROOT)
import page_v4 as T
A = T.A

VER = 'v0.1'
E = {'red': '🔴', 'amber': '🟡', 'green': '🟢', 'grey': '⚪'}
CLS = {'red': 'r', 'amber': 'y', 'green': 'g', 'grey': ''}
WORD = {'red': '红灯', 'amber': '黄灯', 'green': '绿灯', 'grey': '待补'}
SRC = {
    'gx0709': ('国信证券策略专题《二十年六大景气行情启示：本轮 AI 何时见顶？》（2026-07-09，吴信坤等）· 华尔街见闻转载', 'https://wallstreetcn.com/articles/3776630'),
    'gx0709b': ('同上 · 发现报告摘要页（原文 PDF 本站不转存）', 'https://fxbaogao.com/detail/5519599'),
    'gx0808': ('国信证券策略周报《再议科技 M 顶：科技第二波何时来？》（2026-08-08）· 迈博汇金摘要', 'https://www.microbell.com/data/66f0656331302078071b7f8b132fb40c.html'),
    'gx0927': ('国信证券《科技 M 顶第二波启动了吗？》（2026-09-27）· 新浪财经转载', 'https://finance.sina.com.cn/roll/2026-09-27/doc-initfxsh3511668.shtml'),
    'ts': ('Tushare Pro：中证指数日线、每日指标、财务指标、复权因子（脚本现拉）', 'https://tushare.pro/document/2'),
    'sec': ('SEC EDGAR XBRL companyfacts：微软、亚马逊、谷歌、Meta 现金流量表（脚本现拉）', 'https://www.sec.gov/search-filings/edgar-application-programming-interfaces'),
    'yh': ('Yahoo Finance：费城半导体指数 ^SOX 日线（脚本现拉）', 'https://finance.yahoo.com/quote/%5ESOX/'),
    'world': ('本站世界看板（同一天的快照）', 'world/'),
    'ledger': ('本站全局判断总账', 'ledger.html'),
}
ORDER = []


def s(k):
    if k not in ORDER:
        ORDER.append(k)
    i = ORDER.index(k) + 1
    return f'<sup class="fn"><a aria-label="来源 {i}" class="fn-a" href="#src{i}">{i}</a></sup>'


def esc(x):
    return html.escape(str(x)) if x is not None else '待补'


def pct(x, sign=False):
    return '待补' if x is None else (f'{x:+.1f}%' if sign else f'{x:.1f}%')


def build():
    p = os.path.join('world', 'ai_bubble.json')
    R = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
    secs = []

    def sec(i, sid, title, body):
        assert len(title) <= 15, title
        secs.append(f'<section id="{sid}" class="ch" data-toc="{i:02d} {title}"><header class="ch-h"><span class="ch-n">{i:02d}</span><h2>{title}</h2></header>{body}</section>\n')

    if not R:
        hero = ('<section id="top" class="hero" data-toc="01 一分钟看懂"><h1>AI 泡沫监控</h1><p>读数待补：world/ai_bubble.json 还没生成（世界看板每日更新时生成）。<b>不构成投资建议</b>。</p></section>')
        main = hero
        L, st, D = [], None, ''
    else:
        L = R['lights']; st = R['stage']; D = f'{R["date"][:4]}-{R["date"][4:6]}-{R["date"][6:]}'
        Lm = {x['id']: x for x in L}
        a = [x for x in R['mtop'] if x['code'] != '^SOX']
        cx = R.get('capex') or {}
        g = cx.get('agg') or {}
        c = st['count']
        rx = R.get('reaction') or []
        roe = R.get('roe') or []
        # ---------- 开篇
        steps = ''.join(f'<li class="{"on" if i == st["i"] else ""}"><b>{i + 1}</b>{n}</li>' for i, n in enumerate(st['steps']))
        hi_txt = '、'.join(f'{x["name"].replace("中证", "")}现在是前高的 {x["ratio"]:.0f}%' for x in a)
        low_n = sum(1 for x in a if x['ratio'] - (100 + x['maxdd']) < 3)
        low_txt = f'其中 {low_n} 个指数现价就在本轮最低点附近（离最低不到 3 个百分点），一顶之后的反弹没守住。' if low_n else ''
        tp0 = next((x for x in a if x['code'] == '931160.CSI'), None)
        rx_ok = [x for x in rx if x.get('med_full') is not None and x['n'] >= 10 and x['n_full'] >= 0.6 * x['n']]
        rx_med = rx_ok[-1]['med_full'] if rx_ok else None
        hero = (f'<section id="top" class="hero" data-toc="01 一分钟看懂"><div class="kicker">世界看板 · AI 泡沫监控 · {VER} · 数据日 {D}</div>'
                '<h1>AI 行情走到哪一步了</h1>'
                '<p class="dek">借国信证券“六轮景气行情怎么见顶”的框架，每天用真实数据给本轮 AI 打一次分。</p>'
                '<p class="howto">怎么读：先看“一分钟看懂”和下面的阶段条。每盏灯都写了数据从哪来、多久更新、为什么这么定线。'
                '<b>所有阈值都是草案</b>，还没经过 John 确认。读数由脚本从公开数据算出，不是我们手填的。小号上标数字是来源，点一下能看。公开数据整理，<b>不构成投资建议</b>。</p>'
                '<div class="onemin" id="onemin"><span class="pull-k">一分钟看懂</span><ol>'
                f'<li><span class="om-k">是什么</span>报告发现：过去六轮景气行情，股价总比赚钱能力早 8–19 个月见顶 {s("gx0709")}。顶部常像字母 M：先冲高、跌一段、再反弹到前高的八九成。</li>'
                f'<li><span class="om-k">现在在哪</span>按规则算，本轮读数是<b>“{esc(st["name"])}”</b>。{hi_txt}。{low_txt}</li>'
                f'<li><span class="om-k">钱在哪</span>A 股 AI 硬件（光模块、PCB、芯片）的订单，靠美国四大云厂商买服务器的钱。四家里有 {cx.get("n_dec", "待补")} 家开支增速比上季慢。</li>'
                f'<li><span class="om-k">最大风险</span>股价跌的时候，财报往往还很好看。所以“业绩还在涨”不能当作“没到顶”的证据。</li>'
                '<li><span class="om-k">什么算我们错</span>A 股 AI 硬件指数涨破前高 5% 以上，或者四家云厂商开支增速重新一起加快。详见第 07 章。</li>'
                '</ol></div>'
                f'<ol class="bb-steps" aria-label="阶段">{steps}</ol>'
                f'<p class="note">阶段条按第 04 章的规则从灯里推出来，不是主观打分。今天 {c["red"]} 红、{c["amber"]} 黄、{c["green"]} 绿、{c["grey"]} 待补。</p>'
                + A.stats([(pct(tp0['ratio']) if tp0 else '待补', 'A 股通信设备指数：现价 ÷ 本轮最高收盘'),
                           (pct(g.get('yoy'), True), f'四大云厂商开支同比（{esc(g.get("last"))}）'),
                           (pct(rx_med, True), '好财报之后 20 日跑赢大盘多少（中位数）'),
                           (f'{c["red"]} / {len(L)}', '红灯数 / 灯总数')])
                + A.glossary([('M 顶', '股价先冲到一个最高点，跌一段，再涨回去但没超过，形状像字母 M。', '爬山：第一座峰最高，下山后又爬上一座矮一点的峰。'),
                              ('ROE', '净资产收益率：公司每 100 元自有本钱，一年赚多少钱。', ''),
                              ('TTM', '最近 12 个月加总，不受季节影响。', ''),
                              ('资本开支', '公司买厂房、机器、服务器的钱。', ''),
                              ('二阶导转负', '还在涨，但涨得比上次慢了。', '车还在往前开，但油门松了。'),
                              ('超额收益', '个股涨幅减去大盘涨幅。', ''),
                              ('换手率', '一天里成交的股票占流通股的比例，越高说明越多人在抢着买卖。', ''),
                              ('分位', '把历史读数从低到高排队，现在排在百分之几。90% 表示比历史上 90% 的日子都高。', ''),
                              ('市盈率', '股价是每年利润的多少倍。', ''),
                              ('CDS', '信用违约互换：给一家公司“会不会还不起钱”买的保险，价越高越危险。', '')])
                + '</section>\n')

        # ---------- 02 报告框架
        sec(2, 'frame', '报告说了什么', '<p>只摘框架，不抄原文。下面 5 条是报告的结论，不是我们的判断。</p><ol class="ov5">'
            f'<li><span class="fj f">报告</span>六个行业（消费电子、通信设备、半导体、光伏设备、电池、能源金属），股价最高点比 ROE 最高点早 8–19 个月，中位数约 12.6 个月 {s("gx0709")}。</li>'
            '<li><span class="fj f">报告</span>顶部可以出现在普及的早期。2010 年底消费电子见顶时，智能手机普及率才约 25%；之后普及率涨到 47%，股价却最多跌了约 46%。</li>'
            '<li><span class="fj f">报告</span>顶部常是 M 形。第二个高点的中位数是第一个高点的 87.1%；两个高点相隔约 4–5 个月；第一轮下跌平均 41.5% '
            f'{s("gx0808")}。</li>'
            '<li><span class="fj f">报告</span>最早的信号是“好消息不涨了”。好财报公布后 20 个交易日，主升浪里平均跑赢 +3.2%，顶部窗口变成 −1.5%，次高点 −2.7%（都是中位数）。</li>'
            f'<li><span class="fj f">报告</span>本轮最该盯的是四大云厂商的资本开支。微软、Meta 一季度增速已经放慢；如果亚马逊、谷歌也慢下来，要小心 {s("gx0709b")}。9 月 27 日的后续报告认为第二波已经开始，可能持续到四季度 {s("gx0927")}。</li>'
            '</ol>'
            + A.plain('报告的意思是：别等财报变差才觉得到顶了。股价会提前反应，最早的迹象是好财报公布后股价不涨。')
            + '<p class="note">没核到的：六个案例各自的高点日期和领先月数（表格在 PDF 里，免费摘要没给）；“超额收益”用的是哪个基准；“好财报”的具体定义。这几项本页都按自己的口径重算，写在各章。</p>')

        # ---------- 03 历史六轮
        rows = ''.join(f'<tr><td><b>{esc(x["name"])}</b><br><small>{esc(x["proxy"])}</small></td><td>{esc(x.get("high_date"))}</td><td>{pct(x.get("dd"))}</td>'
                       f'<td>{pct(x.get("second")) if x.get("second") else "待补"}</td><td><small>{esc(x["note"])}</small></td></tr>' for x in R['cases'])
        sec(3, 'cases', '过去六轮：顶长什么样',
            '<p>报告没公开每个案例的日期，我们用中证指数自己复核了“股价”这一半。ROE 那一半要逐家算财报，还没做，标待补。</p>'
            '<div class="tbl"><table><thead><tr><th>行业 / 代理</th><th>股价最高点</th><th>之后 9 个月最大跌幅</th><th>反弹高点 ÷ 最高点</th><th>说明</th></tr></thead><tbody>'
            + rows + '</tbody></table></div>'
            + f'<p>我们复核的六轮里，第一轮下跌的中位数是 {pct(R.get("cases_med_dd"))}，反弹高点的中位数是前高的 {pct(R.get("cases_med_second"))}。'
            f'报告给的是 87.1%（第二个高点 ÷ 第一个高点）{s("gx0709")}。</p>'
            + A.plain('过去几轮的共同点：第一次跌得很深，之后能反弹，但多数涨不回前高。')
            + '<p class="note">口径说明：我们用中证指数，报告可能用申万行业指数，所以高点日期和比例会有出入。算法是简化版：最高点之后 9 个月里找最低点，再在最低点之后 12 个月里找反弹高点。'
            f'能源金属没有可用的指数，用天齐锂业、赣锋锂业两家等权近似，代表性弱 {s("ts")}。</p>')

        # ---------- 04 红绿灯
        lis = []
        for x in L:
            tag = '' if x.get('reuse') else '<span class="tag t-est">草案</span>'
            lis.append(f'<li class="{CLS.get(x["light"], "")}"><i class="lt"></i><div><b>{esc(x["name"])}</b>'
                       f'<span><span class="st">{E.get(x["light"], "")} {WORD.get(x["light"], "")}</span>　{esc(x["val"])}</span>'
                       f'<span><span class="k">线</span>{esc(x["rule"])} {tag}</span>'
                       f'<span><span class="k">为什么</span>{esc(x["why"])}</span>'
                       f'<span class="bb-m">来源 {esc(x["src"])} · {esc(x["freq"])} · 数据 {esc(x.get("obs"))}</span></div></li>')
        rule = ('<p class="note">阶段规则：①四家云厂商合计开支增速跌破 +20%，或 ROE 连降两季且 3 家以上云厂商减速，算“基本面确认见顶”；'
                '②否则，看 4 个 A 股 AI 硬件指数：半数以上还没从最高点跌过 20%，算“主升浪”；③跌过 20% 且半数以上涨回前高 80% 以上，算“次高点区”；④其余算“一顶后回撤”。规则也是草案。</p>')
        sec(4, 'lights', '今天的红绿灯',
            f'<p>共 {len(L)} 盏灯。前面几盏对应报告的逻辑，后面 4 盏直接沿用世界看板的同名卡片 {s("world")}。</p>'
            f'<ul class="sig3">{"".join(lis)}</ul>' + rule
            + A.more('“好消息还涨不涨”：每个报告期的样本', '<div class="tbl"><table><thead><tr><th>报告期</th><th>好财报家数</th><th>窗口走满</th><th>20 日超额中位数</th></tr></thead><tbody>'
                     + ''.join(f'<tr><td>{x["q"][:4]}Q{int(x["q"][4:6]) // 3}</td><td>{x["n"]}</td><td>{x["n_full"]}</td><td>{pct(x.get("med_full"), True)}</td></tr>' for x in rx)
                     + f'</tbody></table></div><p class="note">样本：{esc((R.get("univ") or {}).get("rule"))}，共 {esc((R.get("univ") or {}).get("n"))} 家。“好财报”= 单季净利同比 ≥ 30%；超额 = 公告前一交易日到之后第 20 个交易日，个股（复权）涨幅减中证全指涨幅。和报告口径不完全一样。</p>')
            + A.figure('figM', 'A 股 AI 硬件指数：现价是本轮最高点的百分之几（周线）', '<div class="chart" id="cM" style="height:300px"></div>',
                       f'虚线是报告的 87%（M 顶第二个高点的中位数）和我们定的 80% 线。{s("ts")}', {ORDER.index("ts") + 1: SRC["ts"][0]}))

        # ---------- 05 云厂商开支
        crow = ''.join(f'<tr><td><b>{esc(x["name"])}</b></td><td>{esc(x["last"])}</td><td>{x["capex"]:.1f}</td><td>{pct(x.get("yoy"), True)}</td><td>{pct(x.get("yoy_prev"), True)}</td>'
                       f'<td>{"<b>变慢</b>" if (x.get("d2") or 0) < 0 else "变快"} {pct(x.get("d2"), True).replace("%", " 个百分点")}</td><td>{pct(x.get("cap_ocf"))}</td></tr>' for x in cx.get('co', []))
        agg = ''.join(f'<tr><td>{k}</td><td>{v:,.1f}</td><td>{pct(y, True)}</td></tr>' for k, v, y in g.get('rows', []))
        sec(5, 'capex', '云厂商开支：还在加速吗',
            f'<p>四家公司的“买厂房和设备的钱”（现金流量表口径）{s("sec")}。单位十亿美元。季度按自然季（微软财年 6 月结束，这里换成自然季）。</p>'
            '<div class="tbl"><table><thead><tr><th>公司</th><th>最新季</th><th>开支</th><th>同比</th><th>上季同比</th><th>增速变化</th><th>近 4 季开支 ÷ 经营现金流</th></tr></thead><tbody>'
            + crow + '</tbody></table></div>'
            + (f'<p>四家都已披露的最新季度是 {esc(g.get("last"))}，合计同比 {pct(g.get("yoy"), True)}，上季 {pct(g.get("yoy_prev"), True)}。</p>' if g else '<p>四家合计：待补。</p>')
            + A.plain('还在多花钱，但多花的速度有没有变慢——这才是报告说的关键。')
            + A.more('四家合计（近 8 季）', '<div class="tbl"><table><thead><tr><th>季度</th><th>合计开支</th><th>同比</th></tr></thead><tbody>' + agg + '</tbody></table></div>')
            + '<p class="note">口径说明：亚马逊用“购买固定资产”毛额（没减去政府补贴和出售）；Meta 不含融资租赁。报告引用的 2026 年指引（约 7,100 亿美元，+88%）来自公司电话会，本页没有自动核对，待补。'
            + (f' 拉取问题：{"；".join(map(esc, cx.get("err")))}' if cx.get('err') else '') + '</p>')

        # ---------- 06 总账
        LG = json.load(open('data/ledger.json', encoding='utf-8'))['items']
        lk = {x['gid']: x for x in LG}
        rel = [('G12', '“云厂商开支继续上修”：第 05 章的开支灯直接检验它。'), ('G25', 'PCB 需求的上一层也是云厂商开支，和 G12 同一个变量。'),
               ('G13', '“封装周期还没见顶”：如果股价先见顶，要提前看设备营收。'), ('G01', 'HBM 紧不紧，看云厂商开支能不能撑住。'), ('G28', '2027 年下半年先松的环节，和二顶后的下跌时间可能重合。')]
        lrows = ''.join(f'<tr><td><a class="lid" href="ledger.html#{k}">{k}</a></td><td>{esc(lk[k]["text"])}</td><td style="white-space:nowrap">{esc(lk[k]["status"])}</td><td><small>{esc(lk[k]["falsify"])}</small></td><td><small>{w}</small></td></tr>'
                        for k, w in rel if k in lk)
        sec(6, 'ledger', '和总账的关系',
            f'<p>本页<b>不改</b>总账里任何判断、状态和概率 {s("ledger")}。下面只说明哪盏灯能帮着检验哪条判断。</p>'
            '<div class="tbl"><table><thead><tr><th>编号</th><th>判断（原文）</th><th>状态</th><th>证伪条件（原文）</th><th>本页怎么帮</th></tr></thead><tbody>' + lrows + '</tbody></table></div>')

        # ---------- 07 证明我们错
        top = max(a, key=lambda x: x['high']) if a else None
        sec(7, 'wrong', '什么会证明我们错', '<ul>'
            '<li><b>“M 顶”说法错</b>：中证通信设备或半导体指数收盘涨破本轮最高点 5% 以上。那说明还是主升浪，不是二顶。</li>'
            '<li><b>“开支减速”警报错</b>：下一季四家里有 3 家以上开支增速比本季快，而且 2027 年指引上调。</li>'
            '<li><b>“好消息不涨”信号错</b>：下一季好财报之后 20 日超额中位数回到 +3% 以上（报告的主升浪水平）。</li>'
            '<li><b>“股价先于业绩”的规律本轮失效</b>：ROE 连降两季，而 AI 硬件指数不跌反涨。</li>'
            '<li><b>本页阈值定错</b>：灯全绿时指数大跌 30%，或灯多数红时指数还在创新高。出现一次就回头改线。</li>'
            '</ul>')

        # ---------- 08 待确认
        tp = next((x for x in a if x['code'] == '931160.CSI'), None)
        sec(8, 'confirm', '待 John 确认',
            '<p>下面是建议的新预测。<b>还没写进总账</b>，也没有概率。确认后才入账。</p><ol>'
            + (f'<li>到 2027-06-30，中证通信设备指数（931160）收盘不超过本轮最高收盘 {tp["high"]:,.0f}（{tp["high_date"]}）的 1.05 倍。证伪：任一交易日收盘高于 {tp["high"] * 1.05:,.0f}。</li>' if tp else '')
            + '<li>四大云厂商 2027 年合计资本开支的同比增速低于 2026 年（2028 年 2 月看全年 10-K）。证伪：2027 年增速 ≥ 2026 年增速。</li>'
            + '<li>2026 年三季报“好财报”（单季净利同比 ≥ 30%）的 20 日超额中位数 ≤ 0（2026-12-15 前窗口走满后结算）。证伪：中位数 > +1.5%。</li>'
            '</ol>')

        # ---------- 09 待补
        sec(9, 'todo', '待补清单', '<ul>'
            '<li>六个案例的 ROE 高点日期和领先月数（报告 PDF 里的表）。</li>'
            '<li>报告“超额收益”的基准和“正面业绩公告”的精确定义。本页用中证全指、单季净利同比 ≥ 30% 近似。</li>'
            '<li>卖方盈利预测上调 / 下调比例（没有免费数据源）。</li>'
            '<li>英伟达、云厂商的前瞻市盈率（没有免费的一致预期）。</li>'
            '<li>美股 AI 相关 IPO 热度（没有免费数据源）。</li>'
            '<li>云厂商 AI 收入增速（9/27 报告说第二波高度看它；财报口径不统一，要人工录入）。</li>'
            '<li>四家公司 2026、2027 年开支指引的自动核对（现在只有世界看板的人工卡片）。</li>'
            '</ul>')

    src = ''.join(f'<li id="src{i}"><a href="{html.escape(SRC[k][1])}" target="_blank" rel="noopener">{html.escape(SRC[k][0])}</a></li>' for i, k in enumerate(ORDER, 1))
    secs.append('<section id="apx" class="ch" data-toc="10 来源"><header class="ch-h"><span class="ch-n">10</span><h2>来源</h2></header>'
                f'<div class="body" id="src"><p class="sub">研报只读了公开转载和摘要页（2026-10-29 打开核对），原文 PDF 不转存。读数每天由脚本重算。</p><ol class="src">{src}</ol></div></section>\n')
    if R:
        main = hero + ''.join(secs)
    else:
        main = main + ''.join(secs)
    ids = re.findall(r'\bid="([^"]+)"', main)
    assert len(ids) == len(set(ids)), 'id 重复'
    for m in re.findall(r'href="#(src\d+)"', main):
        assert f'id="{m}"' in main, m
    chart = ''
    if R:
        ser = [dict(name=x['name'].replace('中证', ''), type='line', showSymbol=False, data=x['spark'], lineStyle={'width': 1.6}) for x in R['mtop'] if x['code'] != '^SOX']
        ser[0]['markLine'] = {'symbol': 'none', 'silent': True, 'lineStyle': {'type': 'dashed'}, 'data': [{'yAxis': 87, 'label': {'formatter': '87%'}}, {'yAxis': 80, 'label': {'formatter': '80%'}}]}
        opt = dict(tooltip={'trigger': 'axis'}, legend={'top': 0}, grid={'left': 8, 'right': 40, 'top': 40, 'bottom': 8, 'containLabel': True},
                   xAxis={'type': 'time'}, yAxis={'type': 'value', 'min': 0, 'max': 100, 'name': '% 前高'}, series=ser)
        chart = ('<script>(function(){var el=document.getElementById("cM");if(!el||!window.echarts)return;var c=echarts.init(el,null,{renderer:"svg"});c.setOption('
                 + json.dumps(opt, ensure_ascii=False) + ');})();</script>\n')
    css = ('<style>.bb-steps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:0;margin:16px 0 6px}'
           '.bb-steps li{background:var(--hig-fill);border-radius:10px;padding:8px 6px;font-size:13px;text-align:center;line-height:1.35;color:var(--mut);min-width:0;overflow-wrap:anywhere}'
           '.bb-steps li b{display:block;font-size:11px}.bb-steps li.on{background:var(--tint);color:#fff;font-weight:600}'
           '.sig3 .bb-m{color:var(--mut);font-size:12.5px}.sig3 li>div{min-width:0}.sig3 span{overflow-wrap:anywhere}</style>')
    T.use('hdd'); T.SRC_NOTE = 'bubble/build.py + world/ai_bubble.json'
    nav = T.nav_html('ai-bubble.html', secs_here=False, key='-').replace('</nav>', '<div class="sn-h">世界看板</div><a class="sn-s" href="world/">世界看板首页</a>'
                                                                         '<a class="sn-s on" href="ai-bubble.html" aria-current="page">AI 泡沫监控</a><div class="sn-here" id="snHere"></div></nav>')
    page = (T.head('AI 泡沫监控', 'AI 泡沫监控：借国信证券六轮景气行情框架，每天用公开数据判断本轮 AI 硬件行情所处阶段（阈值为草案）', T.V3.CSS2 + T.PM.CSS + T.V3.CSS3 + T.CSS4 + css, '', 'ai-bubble.html')
            + '<body class="article chain" data-src-page="ai-bubble.html" data-page="AI 泡沫监控">\n' + T.topbar('AI 泡沫监控', f'{VER} · {D}')
            + nav + '<main class="wrap">\n' + main + '</main>\n<footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="world/">世界看板</a> · <a href="ledger.html">总账</a></footer>\n'
            + '<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n'
            + chart + '<script src="assets/reading.js"></script>\n</body></html>\n')
    open('ai-bubble.html', 'w', encoding='utf-8').write(page)
    print(f'bubble: ai-bubble.html（{len(ORDER)} 条来源；{len(L)} 盏灯；阶段 {st["name"] if st else "待补"}）')


if __name__ == '__main__':
    build()
