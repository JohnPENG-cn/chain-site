#!/usr/bin/env python3
"""长期投资笔记 · A股有没有“巴菲特式”股票 → buffett-style.html（阅读模式，tpl/article.py）。
数字全部来自 invest/buffett_data.json（2026-11-10 由 Tushare / 东方财富 / 中证指数 / Yahoo Finance 算出，见页末来源与方法），
页面文字里的其他数字（茅台 2021 年市盈率等）同样来自那次计算，改动前请重算。图片在 invest/img/。不要手改 buffett-style.html。"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tpl'))
import article as A

D = json.load(open(os.path.join(ROOT, 'invest/buffett_data.json'), encoding='utf-8'))
SRC = {
    1: ('Tushare Pro 数据接口：日线行情 daily、复权因子 adj_factor、每日指标 daily_basic（市盈率、股息率）、分红送股 dividend（取数 2026-11-10）', 'https://tushare.pro/document/2'),
    2: ('东方财富数据中心：分红送配明细 RPT_SHAREBONUS_DET、业绩报表 RPT_LICO_FN_CPD（加权ROE、每股收益）、日K线（不复权和后复权，取数 2026-11-10）', 'https://data.eastmoney.com/yjfp/'),
    3: ('中证指数有限公司：沪深300全收益指数 H00300', 'https://www.csindex.com.cn/#/indices/family/detail?indexCode=H00300'),
    4: ('中证指数有限公司：中证红利全收益指数 H00922', 'https://www.csindex.com.cn/#/indices/family/detail?indexCode=H00922'),
    5: ('中证指数有限公司：沪深300、中证500、中证红利成分股名单（2026-11-09），另两份见 000905cons.xls、000922cons.xls', 'https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/file/autofile/cons/000300cons.xls'),
    6: ('Yahoo Finance 历史行情：KO、AXP、AAPL、BAC、CVX、OXY、SPY 的复权收盘价和分红记录', 'https://finance.yahoo.com/quote/KO/history/'),
    7: ('Berkshire Hathaway 1989 年致股东信（“用合理的价格买好公司”）', 'https://www.berkshirehathaway.com/letters/1989.html'),
}
T = {k: v[0] for k, v in SRC.items()}


def F(*ns):
    return '<sup class="fn">' + ''.join(f'<a class="fn-a" href="#src{n}" aria-label="来源 {n}">{n}</a>' for n in ns) + '</sup>'


def pct(v, s='%'):
    return '—' if v is None else f'{v:.1f}{s}'


def img(name, alt):
    return f'<img src="invest/img/{name}" alt="{alt}" decoding="async" style="display:block;width:100%;height:auto;border-radius:10px">'


def fig(fid, title, name, cap, srcs, wide=True):
    srcline = '<p class="src-line"><span class="sl-k">来源</span>' + '；'.join(f'{A.short(T[n])} <a class="fn-a" href="#src{n}">{n}</a>' for n in srcs) + '</p>'
    return (f'<figure class="fig{" bleed" if wide else ""}" id="{fid}"><figcaption class="fig-t">{title}</figcaption>{img(name, title)}'
            f'<figcaption class="fig-c">{cap}</figcaption>{srcline}</figure>\n')


def tbl(head, rows, num_from=1):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td{" class=\"num\"" if i >= num_from else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


HEAD = ['名称', '代码', '行业', '10年总回报年化', '10年股价年化', '15年总回报年化', '10年平均股息率', '连续现金分红（年）', '每股分红10年年化增长', '10年里分红降过几次', 'ROE平均（2016–2025）', '市盈率（现价÷2025年每股利润）']


def big(rows):
    return tbl(HEAD, [[r['name'], r['code'], r['ind'] or '', pct(r['tr10']), pct(r['px10']), pct(r['tr15']), pct(r['yld']), r['consec'], pct(r['dpsg']), r['cuts'], pct(r['roe']), pct(r['pe'], '')] for r in rows], num_from=3)


C = {r['code']: r for r in D['core'] + D['six'] + D['grow']}
U = D['us']; TP = D['trpe']; IX = D['index']
n10, ncore = D['n_10y'], len(D['core'])

o = []; w = o.append
w('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 invest/build.py（阅读模式 tpl/article.py）根据 invest/buffett_data.json 生成，不要手改；改内容请改 invest/build.py 后跑 ./build.sh -->
<title>A股有没有“巴菲特式”股票？ · 产业链情报研究中心</title><meta name="description" content="有完整10年行情的570只A股里，又涨得好、分红又稳定增长的只有20只；10年总回报年化10%–26%，和可口可乐、美国银行、雪佛龙同一档，同期沪深300全收益4.3%。不构成投资建议。">
<link rel="stylesheet" href="assets.css"><script src="theme.js"></script><link rel="stylesheet" href="assets/hig.css"></head><body class="article">
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="brief/">简报</a><a class="btn" href="ledger.html">总账</a><span class="pill">长期投资笔记 · 2026-11-10</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
<div class="rd-bar" id="rdBar"><div class="rd-in"><button class="rd-cur" id="rdCur" aria-label="打开目录">目录</button><span class="rd-pct" id="rdPct"></span></div><i class="rd-prog" id="rdProg"></i></div>
<nav class="rd-toc" id="rdToc" aria-label="章节目录"></nav>
<main class="wrap">
''')

# ===== 开篇
w('<section id="top" class="hero" data-toc="00 先说结论"><div class="kicker">长期投资笔记 · 发布 2026-11-10 · 数据截至 2026-11-09 收盘（北京时间）</div>\n'
  f'<h1>A股有没有“巴菲特式”股票？有，但{n10}只里只有{ncore}只</h1>\n'
  '<p class="dek">持续分红的公司，股价看着不太行？用分红再投入后的10年总回报重新算一遍，再和巴菲特的持仓、沪深300放在一起比。</p>\n')
w('<div class="bluf" id="bluf"><span class="pull-k">先说结论</span>'
  f'<p>有，但很少：有完整10年行情的{n10}只A股里，又涨得好、分红又稳定增长的只有{ncore}只。</p>'
  f'<p>这{ncore}只把分红再买回去，10年平均每年赚<b>10%到26%</b>。茅台{pct(C["600519"]["tr10"])}、美的{pct(C["000333"]["tr10"])}、福耀{pct(C["600660"]["tr10"])}、招商银行{pct(C["600036"]["tr10"])}、长江电力{pct(C["600900"]["tr10"])}，'
  f'和巴菲特持有的可口可乐（{pct(U["KO"]["tr10"])}）、美国银行（{pct(U["BAC"]["tr10"])}）、雪佛龙（{pct(U["CVX"]["tr10"])}）在同一档。同期沪深300全收益只有<b>{pct(IX["H00300"]["tr10"])}</b>。{F(1, 3, 6)}</p>'
  '<p>觉得“分红股股价不行”，一是只看了股价、<b>没把分红算进去</b>；二是<b>2021年买得太贵</b>：茅台那时市盈率接近60倍，那个月底买入，算上分红到今天还亏20.5%。</p>'
  '<p>要打折扣：名单集中在白酒、家电、汽车零部件、银行、水电和几个周期行业；而且是拿今天的成分股往回看，结果偏乐观。</p></div>\n')
w(A.stats([(f'{ncore} / {n10}', '过了五道门槛的只数 / 有完整10年行情的只数'), ('10%–26%', '这20只的10年总回报年化（分红再投入）'),
           (pct(IX['H00300']['tr10']), '同期沪深300全收益指数的10年年化'), ('20.5%', '2021年2月底按59.8倍市盈率买茅台，到今天的亏损（含分红）')]))
w(A.glossary([
    ('总回报', '股价涨的钱，加上分红的钱。这篇都假设每次分红都在除息那天买回同一只股票（分红再投入）。', '一棵果树：股价是树长高了多少，分红是每年结的果子；把果子换成树苗再种下去，十年后一共有多少棵树。'),
    ('年化', '十年下来平均每年涨多少，按利滚利算。年化10%，十年后本金约变成原来的2.6倍。', '像存款的年利率。'),
    ('股息率', '一年分红 ÷ 股价。', '买一套房出租，一年房租 ÷ 房价，就是租金回报率。'),
    ('市盈率', '股价 ÷ 每股一年的利润。数字越大，买得越贵。', '花20万买一家每年赚1万的小店，就是20倍；利润不变的话要20年回本。'),
    ('复权', '公司送股、拆股后，一股变两股，股价对半跌，但你的钱没少。复权就是把以前的股价换算到同一把尺子上。', '一个披萨切成更多块，每块变小，总量没变。'),
    ('ROE（净资产收益率）', '股东投进去的每100元，一年给公司赚回多少。', '100元本钱的小摊，一年赚20元，ROE就是20%。'),
    ('幸存者偏差', '只看今天还留在场上的选手，被淘汰的不算，结论会偏好。', '只采访中了奖的人，问买彩票划不划算。'),
]))
w('<p class="howto">怎么读：八章从“问题”讲到“方法”。每章先一句导语、一句判断；密集的表格收在“展开细节”里。正文里的小号上标数字是来源编号，点一下看来源，全部列在文末<a href="#src">来源与注释</a>；图下面一行灰字是这张图的来源。'
  '本页只整理公开数据，<b>不构成投资建议</b>。过去的回报不代表以后。</p>\n</section>\n')

# ===== 01 问题
w(A.chapter('ch1', 1, '问题：持续分红的公司，股价看着不太行？', '前几天把茅台、苏泊尔、双汇、海天、海尔、伊利这六只的股价和分红画在一张图上，第一反应是：这些年年分红的公司，股价怎么不太行？'))
w('<p>时寒冰举的巴菲特持仓例子，都是又涨得好、又分红不错。A股就没有这样的公司吗？</p>'
  '<p>要回答这个问题，先得把“涨得好”算对。只看股价不够，因为分红那部分钱，股价图上看不到。所以这篇全部用<b>总回报</b>来比：股价涨的钱，加上分红再买回去攒下的钱。</p></section>\n')

# ===== 02 答案
core_cmp = [('苹果（巴菲特持仓）', U['AAPL']), ('生益科技', C['600183']), ('贵州茅台', C['600519']), ('美国运通（巴菲特持仓）', U['AXP']), ('美的集团', C['000333']),
            ('福耀玻璃', C['600660']), ('标普500 ETF（SPY）', U['SPY']), ('美国银行（巴菲特持仓）', U['BAC']), ('招商银行', C['600036']), ('长江电力', C['600900']),
            ('可口可乐（巴菲特持仓）', U['KO']), ('雪佛龙（巴菲特持仓）', U['CVX'])]
rows = []
for nm, r in core_cmp:
    if 'yld' in r: rows.append([nm, pct(r['tr10']), pct(r['px10']), pct(r['yld'])])
    else: rows.append([nm, pct(r['tr10']), pct(r['px10']), pct(r['avg_yield'])])
rows += [['中证红利全收益（H00922）', pct(IX['H00922']['tr10']), '—', '—'], ['沪深300全收益（H00300）', pct(IX['H00300']['tr10']), '—', '—'],
         ['西方石油（巴菲特持仓）', pct(U['OXY']['tr10']), pct(U['OXY']['px10']), pct(U['OXY']['avg_yield'])]]
w(A.chapter('ch2', 2, f'答案：有，但{n10}只里只有{ncore}只', '先把范围放大到今天三份指数的全部成分股，再定五道门槛，最后和巴菲特持仓、指数放在一起比。'))
w(A.callout(f'A股里确实有和巴菲特那几只同一档的公司，但要从几百只里挑；整体指数（沪深300全收益{pct(IX["H00300"]["tr10"])}）远不如标普500（{pct(U["SPY"]["tr10"])}）。“A股没有好公司”不对，“随便买A股就能拿到这种回报”也不对。', '本章判断'))
w(f'<p>范围：今天的沪深300、中证500、中证红利三份成分股名单，再加上点名要看的几只，一共{D["n_pool"]}只。{F(5)}其中{n10}只在10年前（2016年10月底）已经上市，有完整行情。</p>'
  '<p>五道门槛，要<b>同时</b>满足：</p><ol><li>10年总回报年化 ≥10%（2016-10-31 到 2026-11-09）；</li><li>10年平均股息率 ≥2%；</li><li>2016到2025这十个财年，每年都有现金分红；</li>'
  '<li>每股分红10年平均每年至少多5%，中间比上一年少一成以上的最多两次；</li><li>2016–2025年平均ROE ≥12%。</li></ol>'
  f'<p><b>过了五道门槛的只有{ncore}只，占{n10}只的3.5%。</b>对比一下：{n10}只里10年总回报年化达到10%的有154只，是负数的有160只，排在正中间那只是4.4%。{F(1)}</p>')
w(fig('fig-cmp', '10年总回报年化：A股核心名单 vs 沪深300 vs 巴菲特持仓', 'buffett-style-compare.png',
      '2016-10-31 到 2026-11-09，分红再投入，未扣税费；A股按人民币、美股按美元，没有换算汇率。', [1, 2, 3, 4, 6], wide=False))
w('<p>挑几行看：</p>' + tbl(['', '10年总回报年化', '10年股价年化', '10年平均股息率'], rows)
  + '<p class="src-line"><span class="sl-k">来源</span>Tushare <a class="fn-a" href="#src1">1</a>；中证指数 <a class="fn-a" href="#src3">3</a> <a class="fn-a" href="#src4">4</a>；Yahoo Finance <a class="fn-a" href="#src6">6</a></p>')
w(A.more(f'{ncore}只核心名单全表（按10年总回报排序）', big(D['core']) + '<p class="fig-c">“—”表示上市不满15年。市盈率这一列是现价 ÷ 2025年报每股利润，和下文图里的市盈率（近12个月利润）口径不同。</p>', titles=None, small='12 列，可左右滑动', wide=True)
  .replace('</div></details>', '<p class="src-line"><span class="sl-k">来源</span>Tushare <a class="fn-a" href="#src1">1</a>；东方财富 <a class="fn-a" href="#src2">2</a></p></div></details>'))
w('</section>\n')

# ===== 03 为什么觉得不行
w(A.chapter('ch3', 3, '为什么会觉得“股价不行”', '两个原因：一个是看法上的，分红没算进去；一个是价格上的，2021年太贵。'))
w(A.callout('公司没变坏，变的是买入价。', '本章判断'))
w(f'<p><b>第一，分红没算进股价。</b>分红越多的公司，股价图越“吃亏”：每次分红，股价都要扣掉同样多的钱（除息），钱进了你的口袋，图上却像是跌了。'
  f'长江电力10年股价年化{pct(C["600900"]["px10"])}，加上分红是{pct(C["600900"]["tr10"])}；招商银行股价{pct(C["600036"]["px10"])}，加上分红是{pct(C["600036"]["tr10"])}。'
  f'双汇最明显：从2010年1月算起，股价年化只有{TP["000895"]["price_cagr"]:.1f}%，加上分红是{TP["000895"]["tr_cagr"]:.1f}%。</p>')
w(fig('fig-sh', '双汇发展：股价和总回报，以及市盈率历史', 'tr-pe-000895.png',
      '红线是总回报，黑线只看股价，2010-01 = 100，对数刻度。两条线中间那块粉色，就是分红再投入攒出来的钱；只看黑线，会以为这家公司十几年没怎么赚钱。下栏是市盈率（近12个月）和它的中位数。', [1, 2]))
w(f'<p><b>第二，2021年太贵。</b>茅台的市盈率在2021年2月底到了59.8倍（那个月盘中最高73.3倍），是2010年以来月底的最高值。那个月底买入的人，算上这几年的分红，到2026年11月9日还亏20.5%，平均每年−4.0%。'
  f'同一家公司，2016年10月底市盈率24.1倍时买入，10年平均每年赚{pct(C["600519"]["tr10"])}。{F(1)}</p>'
  f'<p>巴菲特在1989年的股东信里写过：用合理的价格买一家好公司，远比用好价格买一家普通公司强。{F(7)}2021年按60倍买茅台，是好公司、价格不合理；之后回报差，正好印证了这句话。</p></section>\n')

# ===== 04 名单里的五只
w(A.chapter('ch4', 4, '名单里五只有代表性的公司', f'{ncore}只里挑了分红最稳、最像巴菲特风格的五只画图：茅台、美的、长江电力、福耀、招商银行。'))
w(A.callout('这五只的总回报里，分红占了明显的一块；现在相对自己最贵的是长江电力。', '本章判断'))
w('<p>它们10年里每股分红比上一年少一成以上的次数是0到1次。没有按涨幅挑，因为涨得最多的几只（生益科技、潍柴动力、鄂尔多斯）更偏周期，第六章会讲。</p>'
  '<p>每张图上半部分是股价（黑）和总回报（红），起点都算100；下半部分是市盈率和它自己的历史中位数（橙色虚线）。蓝线在橙线上面很多的时候买，等于付了比平时更高的价钱。'
  '下面五张图的年化都从2010年1月（美的从2013年9月）算到2026年11月9日，和上一章表里的10年数字不是同一段时间。</p>')
five = [
    ('600519', '贵州茅台', 'tr-pe-600519.png', f'茅台：{TP["600519"]["years"]:.1f}年股价年化{TP["600519"]["price_cagr"]:.1f}%，总回报年化{TP["600519"]["tr_cagr"]:.1f}%。市盈率现在{TP["600519"]["pe_last"]:.1f}倍，低于它2010年以来的中位数{TP["600519"]["pe_median"]:.1f}倍。ROE平均{pct(C["600519"]["roe"])}，名单里最高。'),
    ('000333', '美的集团', 'tr-pe-000333.png', f'美的：{TP["000333"]["years"]:.1f}年股价年化{TP["000333"]["price_cagr"]:.1f}%，总回报年化{TP["000333"]["tr_cagr"]:.1f}%。市盈率{TP["000333"]["pe_last"]:.1f}倍，和中位数{TP["000333"]["pe_median"]:.1f}倍差不多。10年里每股分红没有一次比上一年少一成以上。'),
    ('600900', '长江电力', 'tr-pe-600900.png', f'长江电力：股价年化{TP["600900"]["price_cagr"]:.1f}%，总回报年化{TP["600900"]["tr_cagr"]:.1f}%，差不多三分之一的回报来自分红。<b>市盈率现在{TP["600900"]["pe_last"]:.1f}倍，明显高于它的中位数{TP["600900"]["pe_median"]:.1f}倍</b>，是这五只里现在相对自己最贵的一只。'),
    ('600660', '福耀玻璃', 'tr-pe-600660.png', f'福耀：股价年化{TP["600660"]["price_cagr"]:.1f}%，总回报年化{TP["600660"]["tr_cagr"]:.1f}%。市盈率{TP["600660"]["pe_last"]:.1f}倍，中位数{TP["600660"]["pe_median"]:.1f}倍。'),
    ('600036', '招商银行', 'tr-pe-600036.png', f'招商银行：股价年化{TP["600036"]["price_cagr"]:.1f}%，总回报年化{TP["600036"]["tr_cagr"]:.1f}%，红线和黑线拉得最开。市盈率{TP["600036"]["pe_last"]:.1f}倍，略低于中位数{TP["600036"]["pe_median"]:.1f}倍；10年平均股息率{pct(C["600036"]["yld"])}。'),
]
for code, nm, f, txt in five:
    start = TP[code]['start']
    w(fig(f'fig-{code}', f'{nm}：股价、总回报和市盈率', f, f'{start[:4]}-{start[4:6]} = 100，对数刻度；下栏橙色虚线是市盈率的历史中位数。', [1, 2]))
    w(f'<p>{txt}</p>')
w('</section>\n')

# ===== 05 差一点
w(A.chapter('ch5', 5, '差一点没进名单的', '没过门槛不等于不好，只是不符合“涨得好、分红稳、还在涨”这一套标准。几个常被问到的：'))
w(A.callout('高股息的煤炭、化工股涨得多，但分红跟着行业大起大落，不是“年年稳着加”的那一类。', '本章判断'))
w('<ul><li><b>中国神华</b>：10年总回报年化20.0%，平均股息率7.3%，都很高。但按财报年份，2017年每股分红3.42元（含特别分红），2018年只有0.88元；10年里降过3次。</li>'
  '<li><b>陕西煤业（21.7%）、兖矿能源（18.0%）、万华化学（18.4%）</b>：涨得多，分红跟着煤价、化工品价格大起大落。</li>'
  '<li><b>宁沪高速</b>：分红很稳，每股分红从2015年的0.40元慢慢加到2025年的0.49元；但10年总回报9.1%，差一点到10%。</li>'
  '<li><b>格力电器</b>：总回报11.5%，平均股息率5.3%，但2017年度没有分红。</li>'
  '<li><b>海螺水泥（5.3%）、伟星新材（4.5%）</b>：分红不少，但股价拖了后腿。</li>'
  '<li><b>恒瑞医药（11.5%）、片仔癀（11.9%）</b>：涨得可以，但股息率分别只有0.3%和0.7%，主要靠股价。</li>'
  '<li><b>中国移动、公牛集团、迈瑞医疗</b>：A股上市不满10年，没法算。</li></ul>')
w(f'<p>最早看的六只，是之前按“赚钱能力强（ROE长期≥15%）、自由现金流多数年份为正、连续分红”挑出来的，生意本身都不差。按10年总回报看，茅台和海尔过了全部门槛；海天股息率不够2%；伊利{pct(C["600887"]["tr10"])}、苏泊尔{pct(C["002032"]["tr10"])}、双汇{pct(C["000895"]["tr10"])}没到10%。</p>')
w(A.more('茅台、海尔、海天、伊利、苏泊尔、双汇（同口径）', big(D['six']), titles=None, small='12 列，可左右滑动', wide=True))
w('<p>还有一批“涨得多、分红少”的，10年总回报年化≥15%，但平均股息率不到2%，比如中际旭创、恒立液压、紫金矿业、山西汾酒、立讯精密。它们更像成长股，不是这篇要找的类型。</p>')
w(A.more(f'涨得多但股息率不到2%的{len(D["grow"])}只', big(D['grow']), titles=None, small='12 列，可左右滑动', wide=True))
w('</section>\n')

# ===== 06 折扣
w(A.chapter('ch6', 6, '这份名单要打几个折扣', '下面五条，都会让结果看起来比实际好，或者让人误用。'))
w(A.callout('这是“回头看谁跑赢了”，不是“以后谁会跑赢”。', '本章判断'))
w('<ol><li><b>幸存者偏差。</b>名单是今天的成分股往回看。10年里被踢出指数、退市、或者表现太差没进指数的公司，都不在样本里。真在2016年闭着眼买一篮子，结果会比这里差。</li>'
  '<li><b>行业集中。</b>20只里白酒3只（茅台、泸州老窖、五粮液），银行3只（招商、宁波、南京），家电2只（美的、海尔），电力2只（长江电力、川投），汽车零部件2只（潍柴、福耀）；剩下8只各占一个行业，多是覆铜板、铁合金、基建、化工、电网设备、水泥这类周期行业。周期股的分红会跟着行业起伏，不像可口可乐那样年年平稳地加。</li>'
  '<li><b>买入价决定回报。</b>同一只茅台，24倍市盈率买和60倍买，是两种结果（见第三章）。</li>'
  f'<li><b>生益科技排第一，但现在很贵。</b>它现价 ÷ 2025年每股利润约{pct(C["600183"]["pe"], "")}倍，涨幅主要来自最近这一段行情。过去10年的{pct(C["600183"]["tr10"])}，不能直接拿来当以后的预期。</li>'
  f'<li><b>巴菲特的持仓也不是只只都好。</b>西方石油10年总回报{pct(U["OXY"]["tr10"])}。另外美股是美元计、A股是人民币计，没有换算汇率，也没扣分红的税。</li></ol></section>\n')

# ===== 07 怎么用
pe_rows = [[nm, f'{TP[c]["pe_last"]:.1f}', f'{TP[c]["pe_median"]:.1f}', lab] for c, nm, lab in
           [('600519', '贵州茅台', '低于中位数'), ('000333', '美的集团', '接近'), ('600660', '福耀玻璃', '接近'), ('600036', '招商银行', '略低'), ('600900', '长江电力', '明显高于')]]
w(A.chapter('ch7', 7, '这些数字怎么用', '最实用的一招：看一只好公司的市盈率，现在高于还是低于它自己的历史中位数。'))
w(A.callout('它不能告诉你明天涨还是跌，但能告诉你，现在的价格比这家公司过去十几年的平常价格贵还是便宜。', '本章判断'))
w('<p>按这个看法（市盈率是近12个月口径，中位数取2010年以来，美的从2013年9月起）：</p>'
  + tbl(['', '现在的市盈率', '自己的历史中位数', '相对自己'], pe_rows)
  + '<p class="src-line"><span class="sl-k">来源</span>Tushare 每日指标 <a class="fn-a" href="#src1">1</a>，截至 2026-11-09</p>'
  '<p>三条使用提醒：</p><ul><li>只拿<b>好公司</b>比。生意变坏的公司，市盈率低可能是因为它真的值这么多。</li>'
  '<li><b>周期股要反过来想。</b>煤、化工、钢铁的利润在顶点时，市盈率反而最低；看起来便宜的时候，可能正是利润最好、要往下走的时候。</li>'
  '<li>想要分红，就要把分红算进回报里看，不要只盯着股价图。</li></ul></section>\n')

# ===== 08 方法
w(A.chapter('ch8', 8, '方法和数据说明', '每个数字怎么来的，哪些数据源有坑。'))
w(A.more('总回报、股价、股息率、分红、ROE 的算法，以及为什么不用东方财富后复权', 
  '<ul><li><b>时间：</b>10年是2016-10-31收盘到2026-11-09收盘，15年从2011-10-31起。A股以人民币、美股以美元计，没扣税费。</li>'
  f'<li><b>总回报怎么算：</b>用Tushare的复权因子（收盘价 × 复权因子）{F(1)}，等于在每次除息那天，按除权后的参考价把现金分红买回这只股票。抽查茅台2026-06-26那次除息：复权因子跳了1.02367倍，和“前一天收盘价 ÷（前一天收盘价 − 每股分红）”算出来一样。</li>'
  f'<li><b>为什么没用东方财富的“后复权”价格：</b>抽查发现，它在两次除息之间价格比例会慢慢漂移，不是严格按比例复权，算出来的10年年化比实际低约1.3个百分点：茅台17.3%对18.8%，双汇4.4%对6.0%，海尔9.5%对10.8%。{F(2)}</li>'
  f'<li><b>交叉核对：</b>又用东方财富的不复权日线加分红记录{F(2)}自己算了一遍，和Tushare结果的中间值差0.0个百分点。差超过0.3个百分点的有30只，原因是东方财富的分红表漏了特别分红（比如茅台2022、2023年的两笔特别分红，中国神华2017年那笔）和配股，所以以Tushare为准。格力、云南白药等26只在2016-10-31停牌，Tushare当天没有价格，用的是自算值。</li>'
  '<li><b>股价年化：</b>不复权价格，只把送股、转增换算回来，不含分红。</li>'
  f'<li><b>股息率：</b>Tushare的近12个月股息率，取2016–2025每年最后一个交易日，求平均。{F(1)}</li>'
  f'<li><b>连续分红、每股分红增长、降了几次：</b>Tushare分红数据，只算已经实施的，含特别分红，按送转换算到今天的股本，按财报年份加总；“降”指比上一年少一成以上。{F(1)}</li>'
  f'<li><b>ROE：</b>东方财富年报加权ROE，2016–2025平均。{F(2)}</li>'
  f'<li><b>指数：</b>中证指数官网沪深300全收益（2016-10-31为{IX["H00300"]["start"]}，2026-11-09为{IX["H00300"]["end"]}）和中证红利全收益（{IX["H00922"]["start"]}和{IX["H00922"]["end"]}）。{F(3, 4)}官网接口查不到2011年的数，所以指数没有15年对比。</li>'
  f'<li><b>美股：</b>Yahoo Finance的复权收盘价（含分红再投入），股息率用当年分红 ÷ 年末收盘价。{F(6)}</li>'
  '<li><b>数据截止：</b>2026-11-09收盘（北京时间15:00）。</li></ul>', titles=None, open_=True))
w('<p>本页只整理公开数据，<b>不构成投资建议</b>。</p></section>\n')

# ===== 来源
lis = ''.join(f'<li id="src{n}" value="{n}">{t} <a href="{u}" target="_blank" rel="noopener">{u}</a></li>' for n, (t, u) in SRC.items())
w('<section id="apx" class="apxsec notes" data-toc="注 来源与注释"><header class="ch-h"><span class="ch-n">注</span><h2>来源与注释</h2></header>'
  f'<details class="apx" id="apxSrc" open><summary>来源列表 <small>点任一上标会先弹出来源摘要</small></summary><div class="body" id="src"><p class="sub">均于 2026-11-10 用接口或浏览器取数核对。原始下载不入库，加工后的数字在 invest/buffett_data.json。</p><ol class="src">{lis}</ol></div></details>\n</section>\n')
w('</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">首页</a> · <a href="ledger.html">总账</a></footer>\n')
w('<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n')
w('<script src="assets/reading.js"></script></body></html>\n')

html = A.fnify(''.join(o))
assert '不构成投资建议' in html and html.count('<details') >= 5
for f in os.listdir(os.path.join(ROOT, 'invest/img')):
    assert f in html, f
open(os.path.join(ROOT, 'buffett-style.html'), 'w', encoding='utf-8').write(html)
print('invest/build.py: buffett-style.html 已生成')
