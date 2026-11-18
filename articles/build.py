#!/usr/bin/env python3
"""周期笔记 · 货难买的时候，财报还没写出来 → cycle-ledger.html（阅读模式，tpl/article.py）。

正文和数字全部来自 /workspace/cycle-framework/article_wechat_draft.md（2026-11-18 初稿）。
不要改数字；草稿里的【待补】【缺失】【待John确认】必须原样保留，不得编造。
不要手改 cycle-ledger.html；改内容请改本文件后跑 python3 articles/build.py，再跑
python3 tools/cachebust.py cycle-ledger.html。
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tpl'))
import article as A

# 尾注标题与链接。无公开页的条目不编造 URL，在正文注明待补。
# 站点内页面用相对路径，方便本地预览和 Pages 部署。
SRC = {
    1: ('Citi Research, C. Danely 等, Our 15 Axioms of Semiconductor Investing, 2017。本文依据该报告的公开摘要截图，未取得原报告全文。', None),
    2: ('作者自建「半导体周期看板」第二版，2005–2026Q3。数据来自台积电、联电、中芯国际、华虹、格芯、日月光、安靠、长电科技、通富微电、华天科技、德州仪器、亚德诺、微芯、恩智浦，以及阿斯麦、应用材料等设备厂的季报，2026-11-10 整理。底层整理稿尚未单独做成公开页。', None, '待补'),
    3: ('作者自建「被动元件周期数据集」，2002–2026Q3，数据来自村田、TDK、太阳诱电、三星电机、国巨、华新科的季报和月营收。订单出货比为作者自算。底层整理稿尚未单独做成公开页。', None, '待补'),
    4: ('村田制作所 FY2026 第二季度决算短信，2026-10-30。', 'https://corporate.murata.com/-/media/corporate/about/newsroom/news/irnews/irnews/2026/1030/26q2-e-fls.ashx'),
    5: ('科创板日报/财联社（东方财富转载），2026-09-10。', 'https://finance.eastmoney.com/a/202609103870694270.html'),
    6: ('TrendForce 新闻稿，2026-09-30；一、二季度实际涨幅引自 EffectStory 整理的 TrendForce 历次新闻稿。',
        ['https://www.trendforce.com/presscenter/news/20260930-13258.html',
         'https://effectstory.com/en/data/memory-contract-prices']),
    7: ('TrendForce 存储现货周报，2026-10-21。',
        'https://www.trendforce.com/news/2026/10/21/insights-memory-spot-price-update-ddr5-supply-tight-ddr4-trading-subdued-despite-0-84-gain-in-mainstream-prices/'),
    8: ('世界运行指标·五盏灯，数据日 2026-11-17。', 'world/'),
    9: ('AI 泡沫监测，数据日 2026-11-17。', 'ai-bubble.html'),
    10: ('全局判断总账，数据更新至 2026-11-13，统计时间 2026-11-18。', 'ledger.html'),
    11: ('韩国产业通商部，10 月进出口动向，2026-11-01。', 'https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/172360/view'),
    12: ('新浪财经 7×24，2026-10-29。', 'https://finance.sina.cn/7x24/2026-10-29/detail-iniwwawy6069806.d.html'),
    13: ('CoreWeave 2026 年三季度财报，2026-11-10。',
        'https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Third-Quarter-2026-Results/default.aspx'),
    14: ('远见杂志，2026-11-06。', 'https://www.gvm.com.tw/article/134339'),
    15: ('世界指标历史回测，2026-10-23。', 'world/#bt', '「回测」栏'),
    16: ('NVIDIA Newsroom, "NVIDIA Announces Financial Results for Third Quarter Fiscal 2027", 2026-11-17.',
        'https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2027'),
    17: ('Reuters via Investing.com, "Nvidia earnings beat estimates; firm won\'t take questions on resignation", 2026-11-17；同日 "Nvidia shares set for $335 billion swing after earnings, options show"（Susquehanna：±8.5%）。',
        ['https://www.investing.com/news/stock-market-news/nvidia-earnings-beat-estimates-attention-turns-to-call-5034180',
         'https://www.investing.com/news/stock-market-news/nvidia-shares-set-for-335-billion-swing-after-earnings-options-show-5032318']),
    18: ('CNBC, "Nvidia (NVDA) Q3 2027 earnings report: Live updates", 2026-11-17；CNBC 同日期权预期 ±7%。',
        'https://www.cnbc.com/2026/11/17/nvidia-nvda-earnings-report-q3-2027.html'),
    19: ('作者整理的 A 股 PCB 产业链 17 家公司财报面板。一线、二线的分组是作者的判断，没有回测。公开面板：',
        'pcb_data/filings.json'),
}
T = {k: v[0] for k, v in SRC.items()}


def F(*ns):
    return '<sup class="fn">' + ''.join(
        f'<a class="fn-a" href="#src{n}" aria-label="来源 {n}">{n}</a>' for n in ns
    ) + '</sup>'


def lid(code):
    return f'<a class="lid" href="ledger.html#{code}">{code}</a>'


def todo(text='待补'):
    return f'<span class="tag t-todo">{text}</span>'


def src_li(n, item):
    title, url = item[0], item[1]
    flag = item[2] if len(item) > 2 else ''
    badge = ' ' + todo(flag) if flag and flag.startswith('待') else (f' {flag}' if flag else '')
    if not url:
        return f'<li id="src{n}" value="{n}">{title}{badge}</li>'
    urls = url if isinstance(url, list) else [url]
    parts = []
    for u in urls:
        ext = ' target="_blank" rel="noopener"' if u.startswith('http') else ''
        parts.append(f'<a href="{u}"{ext}>{u}</a>')
    return f'<li id="src{n}" value="{n}">{title} {" ".join(parts)}{badge}</li>'


o = []
w = o.append

w('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 由 articles/build.py（阅读模式 tpl/article.py）根据 2026-11-18 周期长文初稿生成，不要手改；改内容请改 articles/build.py 后跑 python3 articles/build.py -->
<title>货难买的时候，财报还没写出来：一个采购员的半导体周期账本 · 产业链情报研究中心</title>
<meta name="description" content="芯片和电路板行业的冷暖，往往先出现在采购员的交期和报价单上，比公司财报早一到两个季度。但它只能告诉你方向，不能告诉你节奏。不构成投资建议。">
<link rel="stylesheet" href="assets.css"><script src="theme.js"></script><link rel="stylesheet" href="assets/hig.css">
<style>
body.article .tag.t-todo{font-size:10.5px;padding:0 5px;margin:0 2px;border-radius:var(--r-cap,5px);background:var(--hig-warn-fill,rgba(255,149,0,.14));color:var(--hig-tx-orange,#C93400);vertical-align:1px;border:.5px solid rgba(201,52,0,.35);white-space:nowrap}
body.article .todo-note{border-left:3px solid var(--hig-orange,#FF9500);background:var(--hig-warn-fill,rgba(255,149,0,.14));padding:10px 14px;margin:16px 0;border-radius:0 8px 8px 0}
body.article .todo-note p{margin:.2em 0}
</style>
</head><body class="article">
<header class="top"><div class="wrap"><a class="brand back" href="./" aria-label="返回首页">首页</a><span class="sp"></span><a class="btn" href="daily/">日报</a><a class="btn" href="brief/">简报</a><a class="btn" href="ledger.html">总账</a><a class="btn" href="world/">世界</a><span class="pill">周期笔记 · 2026-11-18</span><button class="btn" onclick="toggleTheme()" aria-label="切换深浅色">◐</button></div></header>
<div class="rd-bar" id="rdBar"><div class="rd-in"><button class="rd-cur" id="rdCur" aria-label="打开目录">目录</button><span class="rd-pct" id="rdPct"></span></div><i class="rd-prog" id="rdProg"></i></div>
<nav class="rd-toc" id="rdToc" aria-label="章节目录"></nav>
<main class="wrap">
''')

# ===== 开篇
w('<section id="top" class="hero" data-toc="00 先说结论">'
  '<div class="kicker">周期笔记 · 发布 2026-11-18 · 五盏灯数据日 2026-11-17，总账统计 2026-11-18（北京时间）</div>'
  '<h1>货难买的时候，财报还没写出来：一个采购员的半导体周期账本</h1>'
  '<p class="dek">从交期、报价和配额看周期，把每个判断写成有日期、能对答案的账。对的错的都公开。</p>')
w('<div class="bluf" id="bluf"><span class="pull-k">一句话结论</span>'
  '<p><b>芯片和电路板行业的冷暖，往往先出现在采购员的交期和报价单上，比公司财报早一到两个季度。</b>'
  '但它只能告诉你方向，不能告诉你节奏。所以我把每个判断都写成一笔有日期、能对答案的账，对的错的都公开。</p></div>')
w(A.stats([
    ('103 条', '总账条目：39 条判断、64 条预测'),
    ('1 条', '已到期、能对答案的预测（命中）'),
    ('3.5–4 年', '代工、封测、模拟营收增速的谷底间隔'),
    ('1 绿 1 黄 3 红', '五盏灯截至 2026-11-17'),
]))
w(A.glossary([
    ('交期', '下单以后要等多久才能拿到货。', ''),
    ('配额', '缺货的时候，原厂按什么比例给每个客户分货。', ''),
    ('重复下单', '同一份需求被下了好几次。', '货不够时大家怕买不到，多下单、多囤货，真实需求被放大。'),
    ('订单出货比', '本季新接订单 ÷ 本季营收。大于 1 说明新单比出货多，订单在堆积。', ''),
    ('席勒市盈率', '股价 ÷ 过去 10 年平均利润。用来看美股贵不贵。', ''),
    ('CDS', '为一家公司的债务买一份违约保险，每年要付的保费。用基点表示，10,000 个基点等于本金的 100%。', ''),
    ('Brier 分数', '等于（概率 − 结果）²，越接近 0 越准。', ''),
    ('MLCC', '片式多层陶瓷电容，几乎每块电路板上都有几百颗。', ''),
], summary='名词小白版：页里的行话，一句话说清'))
w('<p class="howto">怎么读：八章从「为什么有周期」讲到「怎么记账」。每章先一句导语、一句判断；'
  '密集的对照表收在「展开细节」里。文中标 ' + todo('待补') + '、' + todo('缺失') + '、'
  + todo('待John确认') + ' 的地方，是初稿里还没补上的材料，没有编造。'
  '小号上标数字是来源编号，点一下看来源，全部列在文末<a href="#src">来源与注释</a>。'
  '总账编号（如 ' + lid('P001') + '）点进去可看原文。本页只整理公开数据，<b>不构成投资建议</b>。</p></section>\n')

# ===== 01 先说结论
w(A.chapter('ch1', 1, '先说结论', '我在 ICT 供应链做采购。这篇讲方法，不是战绩。'))
w(A.callout('我的账才记了不到一个月，真正到期、能对答案的预测只有 1 条。所以这篇讲的是方法，不是战绩。'))
w('<p>我的工作就是买芯片、内存、电路板这些料，所以每天都能看到三样东西：</p>'
  '<ul><li><b>交期</b>：下单以后要等多久才能拿到货。</li>'
  '<li><b>报价</b>：供应商这个月报多少钱。</li>'
  '<li><b>配额</b>：缺货的时候，原厂按什么比例给每个客户分货。</li></ul>'
  '<p>这三样东西变化的时候，大多数公司的财报还没写出来。花旗银行 2017 年总结过「半导体投资 15 条公理」，其中第 7 条是：'
  f'<b>交期拉长时买，交期缩短时卖</b>{F(1)}。</p>'
  '<p>这篇文章讲四件事：</p>'
  '<ol><li>为什么这个行业一定有周期。</li>'
  '<li>为什么一线的采购信号比较早。</li>'
  '<li>我用哪几盏「灯」看大环境，现在亮的是什么颜色。</li>'
  '<li>我怎么给自己的判断记账，目前对了几次、错了几次。</li></ol></section>\n')

# ===== 02 为什么有周期
w(A.chapter('ch2', 2, '为什么半导体和电路板一定有周期', '这个行业像一个反应很慢的水龙头：想要更多芯片，得先盖工厂、买设备。'))
w(A.callout('AI 改变的是周期的幅度和长度，不会让周期消失。'))
w('<p>一座晶圆厂（生产芯片的工厂）从决定投资到真正出货，常常要一到两年。于是会出现下面这个循环：</p>'
  '<ol><li><b>需求突然变大。</b> 比如这两年的 AI 服务器。</li>'
  '<li><b>货不够，大家开始抢。</b> 交期拉长，价格上涨。</li>'
  '<li><b>买家怕买不到，多下单、多囤货。</b> 这叫「重复下单」，同一份需求被下了好几次。</li>'
  '<li><b>厂商看到订单暴涨，加大投资扩产。</b></li>'
  '<li><b>新产能一两年后才出来。</b> 这时候真实需求可能已经放缓，大家手里又堆了很多库存。</li>'
  '<li><b>供过于求，砍单、降价、裁员。</b> 然后再从头开始。</li></ol>')
w(f'<p>这不是我的猜测。我整理过 2005 年到 2026 年三季度晶圆代工、封装测试、模拟芯片三类公司的季度财报{F(2)}。'
  '<b>它们的营收增速大约每 3.5 到 4 年就落到一次谷底</b>：2009、2011–12、2015–16、2019、2023 年前后，三类公司几乎同步。'
  '以代工厂为例，营收增速最低点之间相隔 10、17、13、19 个季度，平均大约 15 个季度（3.7 年）。</p>'
  f'<p>被动元件也一样，比如电容、电阻，其中最常见的叫 MLCC（片式多层陶瓷电容，几乎每块电路板上都有几百颗）。它们也是大约每 3.6 年一个谷底{F(3)}。</p>'
  f'<p>花旗的第 3 条公理说得更直接：<b>半导体就是周期股</b>{F(1)}。</p>'
  f'<p><b>那 AI 会不会让「这次不一样」？</b> 花旗第 8 条说，「这次不一样」很少成真{F(1)}。'
  '我的看法是：AI 改变的是周期的幅度和长度，不会让周期消失。这一轮的特别之处，是需求高度集中在四家美国云厂商'
  '（亚马逊、谷歌、微软、Meta）的资本开支上，也就是它们每年花在服务器和数据中心上的钱。一个买家占比太大，转向的时候就会更猛。</p></section>\n')

# ===== 03 一线信号
w(A.chapter('ch3', 3, '为什么一线采购的信号最早', '财报像月底的水费账单，交期和报价像你拧开龙头时感觉到的水压。'))
w(A.callout('水压变小，你当场就知道；账单要等月底才寄来。'))
w('<p>财报晚，原因有三个：</p>'
  '<ul><li><b>它是季度汇总</b>，季度结束后还要再等一到两个月才公布。</li>'
  '<li><b>它记的是已经交货的生意。</b> 今天签的单子，要一两个季度后才变成营收。</li>'
  f'<li><b>管理层永远偏乐观。</b> 花旗第 2 条和第 10 条都讲这件事：别指望管理层提前告诉你行业要变差{F(1)}。</li></ul>'
  '<p>采购端早，是因为它离需求和产能最近：</p>'
  '<ul><li><b>交期拉长</b>，说明工厂排满了，后面的订单在排队。</li>'
  '<li><b>原厂开始「配额」</b>，说明不是钱的问题，是给多少钱都买不到。</li>'
  '<li><b>报价涨幅变小但配额没松</b>，说明价格涨不动了，但货还是紧。这和「见顶了」不是一回事。</li></ul>'
  '<p><b>有数据支持吗？有一部分。</b></p>'
  f'<ul><li><b>最好用的一个领先指标，是村田的订单出货比。</b> 村田是全球最大的 MLCC 厂。'
  f'从 2002 年的数据看，<b>它领先被动元件营收增速大约两个季度</b>，相关系数 0.63（1 代表完全同步，0 代表毫无关系）{F(3)}。</li>'
  f'<li><b>阿斯麦</b>（全球最大的光刻机厂）的订单领先营收大约一个季度{F(2)}。</li>'
  f'<li><b>反例也要说：应用材料的订单和营收基本同步，没有明显领先</b>{F(2)}。所以「早一到两个季度」是常见情况，不是铁律。</li></ul>')
w(f'<p><b>一个最近的例子。</b> 2026 年 9 月有报道说，村田停产了部分料号，高端 MLCC 的交期从 8–10 周拉长到 20–26 周以上{F(5)}。'
  f'10 月 30 日村田发财报，电容器单季订单比去年同期多 85%，订单出货比 1.39{F(3, 4)}。'
  f'2026 年二季度的 1.47 是 2002 年以来最高{F(3)}。采购端先看到的紧张，后来被财报证实了。</p>'
  '<p>这里要老实说两点：</p>'
  '<ul><li>这次交期和财报只隔了几周，不是一个季度。它只能算一个例子，不算证明。</li>'
  '<li><b>我还没有用自己的交期记录做过系统回测。</b>「交期领先财报一到两个季度」这句话，目前靠的是订单类数据和一线经验，'
  f'<b>交期本身的长期回测</b>{todo("缺失")}。</li></ul>'
  f'<p><b>价格涨得慢，不等于缺货缓解。</b> 2026 年 9 月底，TrendForce（台湾的存储市场研究机构）预测四季度 DRAM（电脑和服务器里的内存）合约价环比涨 10–15%。'
  f'而二季度实际涨了 58–63%，一季度涨了 93–98%{F(6)}。只看这条曲线，很容易得出「见顶了」的结论。'
  f'可同一时期的现货市场上，买家愿意加价也拿不到配额{F(7)}。<b>缺的是配额，不是报价。</b> 财报看不到这一层，采购员看得到。</p></section>\n')

# ===== 04 五盏灯
w(A.chapter('ch4', 4, '五盏灯：大环境怎么看', '交期是「微观水压」，大环境还要看「天气」。'))
w(A.callout('AI 链的需求还很强，但借钱买算力的那一端已经很紧。矛盾不在需求，在资金。'))
w(f'<p>我把几十个公开指标分成五组，每组合成一盏灯。灯的颜色由组里的指标投票：红算 1 票，黄算半票，绿不算票；没数据的指标不投票{F(8)}。</p>'
  '<p><b>一个温度计报警不算数，要几个一起报警才变色。</b></p>'
  f'<p>截至 2026-11-17 的读数{F(8)}：</p>'
  '<ul>'
  '<li><b>🟢 美国衰退风险：会不会衰退？</b> 10 个指标里 0 红 2 黄。失业率和初请失业金（每周新申请失业救济的人数）都没亮。</li>'
  '<li><b>🟡 流动性：钱是不是在变贵？</b> 扣掉通胀以后的 10 年期美债利率（实际利率）到了 2.91%，2003 年以来最高。'
  '美债波动率指数 MOVE 升到 101.3。<b>价格先动了，但借钱的渠道还没堵。</b></li>'
  '<li><b>🔴 估值和情绪：美股贵不贵、热不热？</b> 席勒市盈率（股价 ÷ 过去 10 年平均利润）是 39.2，1871 年以来 98% 的时候都比现在便宜。'
  '<b>这盏灯 11/17 早上由红转黄，晚上又转回红</b>，因为 VIX 期限结构（近期和远期股市恐慌指数的比值）刚好碰到了警戒线。'
  '贴着线的灯会来回跳，这是这套方法的毛病之一。</li>'
  '<li><b>🔴 中国信用与通胀：经济在活化还是失血？</b> 上游的出厂价（PPI）涨得比消费价（CPI）快 5 个百分点，说明原材料成本在挤压中下游的利润。'
  '信贷脉冲（新增贷款是在加速还是减速）是 −1.91% GDP，制造业采购经理指数（PMI）49.3，低于 50 的荣枯线。</li>'
  '<li><b>🔴 AI 和半导体周期：AI 链到了哪一段？</b> 最红的一项是 CoreWeave（一家借钱买英伟达显卡、再租给 AI 公司的云厂商）的 5 年期违约保险价（CDS），大约 1,152 个基点。'
  '意思是：为它的债务买一份 5 年期违约保险，每年保费大约是本金的 11.5%。'
  '<b>借钱最多的玩家最先感到资金紧。</b> 但内存现货价同期是绿的（60.33 美元），需求那一端还没坏。</li>'
  '</ul>')
w(f'<p>另外还有一组专看 AI 泡沫的灯，一共 14 盏，现在是 3 红 6 黄 5 绿，判断的阶段是「<b>一顶后回撤</b>」{F(9)}。'
  '四个阶段依次是：主升浪、一顶后回撤、次高点区、基本面确认见顶。'
  'A 股 PCB（印刷电路板，电子产品的「骨架」）指数离前高大约 38%，最深回撤约 62%；'
  f'但电子行业成交额占全市场的 14.1%，处在 2015 年以来 97% 的分位，<b>钱还扎堆在这里</b>{F(9)}。</p>'
  '<p><b>怎么把这些串起来？</b> 我现在的读法是：<b>AI 链的需求（内存价格、韩国芯片出口）还很强，但借钱买算力的那一端已经很紧，美国的实际利率又在高位。矛盾不在需求，在资金。</b>'
  '对做电路板的人来说，订单还在，但要盯客户的付款和融资。</p>'
  f'<p>这些灯的规则和对错都公开在网站上：<a href="world/">世界指标·五盏灯</a>、'
  f'<a href="ai-bubble.html">AI 泡沫监测</a>{F(8, 9)}。</p></section>\n')

# ===== 05 记账
w(A.chapter('ch5', 5, '记账：怎么让判断可以被检验', '大多数人谈周期，只给观点，不给对答案的日子。'))
w(A.callout('「下半年可能见顶」，错了也能说「还没到」。所以每条判断都要有日期、有证伪条件。'))
w(f'<p>我的做法是把判断写进一本<a href="ledger.html">总账</a>{F(10)}，分两类：</p>'
  '<ul><li><b>判断</b>：方向性的看法，比如「这轮周期最早 2027 年中后期见顶」。每条都写好<b>证伪条件</b>，也就是出现什么情况就算我错了。</li>'
  '<li><b>预测</b>：有数字、有到期日、有概率的具体说法。比如「10 月全月韩国半导体出口同比增长超过 150%，概率 85%」。'
  '到期以后填「命中」或「未中」，再自动算一个分数。这个分数叫 Brier 分数，等于（概率 − 结果）²，越接近 0 越准。</li></ul>'
  '<p>有三条纪律：</p>'
  '<ol><li><b>公司自己的说法不能当证据</b>，只用出口、价格、交期这类硬数据。</li>'
  '<li><b>新证据只追加，不改原文。</b> 想改状态或概率，要单独记一笔，写清理由。</li>'
  '<li><b>前提错了就作废，原文保留</b>，不悄悄删掉。</li></ol>')
w('<p><b>目前的账（截至 2026-11-18）</b></p>'
  '<p>账上一共 103 条：39 条判断、64 条预测。<b>大部分预测要到 2027 年才到期</b>，2027 年到期的有 47 条，2028 年及以后 18 条。</p>')

# 正文只留结论，明细放进展开细节
w('<p><b>✅ 已验证对的：1 条。</b> ' + lid('P001') + '：10 月全月韩国半导体出口同比超过 +150%，概率 85%，2026-11-01 到期。'
  f'实际是 <b>+259.4%</b>{F(11)}，命中，Brier 分数 0.0225。</p>'
  '<p><b>❌ 已验证错的：0 条。</b> 这不是说我没错过，是<b>还没有第二条预测到期</b>。已验证错的例子 ' + todo('缺失') + '。</p>')

w(A.more(
    '作废 2 条、受挑战 18 条、最近要对答案的 3 条',
    '<p><b>🗑 自己作废的：2 条。</b> 这两条算不上对错，但说明我的模型改过：</p><ul>'
    '<li>' + lid('P031') + '（2026-10-15 作废）：原来预测 2027 年的产能瓶颈会从台积电的 CoWoS（一种把多颗芯片封在一起的先进封装）转移到 HBM（AI 芯片旁边的高带宽内存）。'
    '后来我上调了 HBM 供给的估计，<b>模型里的头号瓶颈变成了载板，这条预测的前提不成立了。</b></li>'
    '<li>' + lid('P043') + '（2026-10-21 作废）：原来预测 2027 年电路板链里最紧的是一种高端铜箔（HVLP4）。复核时发现，'
    '<b>我把一家投行的预测区间误当成了观测值</b>。市场信号显示，玻纤布和 ABF 载板材料涨得多得多。</li></ul>'
    '<p><b>⚠️ 受挑战的：18 条判断。</b> 意思是反方证据已经接近证伪线，但还没越过。举三个例子：</p><ul>'
    '<li>' + lid('G01') + '「2026 年 HBM 不缺，2027 年只略紧」：10 月底 SK 海力士说，DRAM 和 HBM 产能到 2029 年基本卖光；三星说 2027 年的 HBM 已经卖完'
    + F(12) + '。<b>离证伪只差一步。</b></li>'
    '<li>' + lid('G12') + '「云厂商资本开支继续上修」：CoreWeave 的财务长说，如果只交付已经承诺的订单，2027 年资本开支可能和 2026 年持平'
    + F(13) + '。这不是正式指引，所以只记为「待核」。</li>'
    '<li>' + lid('G27') + '「电路板链最硬的约束是载板和玻纤布，其次才是设备」：台湾载板厂欣兴的高管说，材料的问题差不多解决了，瓶颈转到了设备，部分设备交期最长三年'
    + F(14) + '。<b>这削弱了我的排序，但还没碰到证伪线。</b></li></ul>'
    '<p><b>⏳ 未到期、最近要对答案的：</b></p><ul>'
    '<li>' + lid('P002') + '：美光下一季营收不低于 600 亿美元，概率 85%，<b>2026-12-20 到期</b>。</li>'
    '<li>' + lid('P054') + '：2027-01-01 美国不会对精炼铜征收 15% 的关税，概率 85%，2027-01-05 到期。</li>'
    '<li>' + lid('P023') + '：四大云厂商首次给出的 2027 年资本开支指引合计不低于 8,500 亿美元，概率 55%，2027-02-15 到期。</li></ul>',
    titles=None,
    small='来自总账，点编号看原文',
    wide=True,
))
w(f'<p><b>说清楚：这些概率都是 2026 年 10 月 22 日的初稿，我还没有逐条确认过</b>{F(10)}。'
  '只有 1 条结果，命中率谈不上，现在说「准」或「不准」都没有意义。几个季度以后，这本账本身才会有说服力。</p>')
w(A.more(
    '指标的历史回测也一样有好有坏',
    '<ul>'
    '<li><b>美债 10 年减 3 个月利差连续倒挂 3 个月，之后 24 个月内衰退</b>：1982 年以来 5 次信号，4 次对了，2022–24 那次失灵。</li>'
    '<li><b>初请失业金比一年低点高 15%，之后 12 个月内衰退</b>：11 次信号只对了 4 次。</li>'
    '<li><b>油价同比涨 50% 以上，之后 12 个月内衰退</b>：8 次只对了 2 次。</li>'
    '</ul><p>所以这些指标只投票，不单独拍板。</p>',
    titles=T,
    small='回测截至 2026-10-23',
) .replace('</div></details>',
           f'<p class="src-line"><span class="sl-k">来源</span>世界指标历史回测 <a class="fn-a" href="#src15">15</a></p></div></details>\n'))
w('</section>\n')

# ===== 06 两个新指标
w(A.chapter('ch6', 6, '新补的两个指标', '对照花旗 15 条，我的框架缺两样。现在先写成草案，还没有回测，也没有放上线。'))
w(A.callout('两个新指标还没有回测，也没有放上线。'))
w('<h3>指标 A：好消息还涨不涨（对应花旗第 15 条）</h3>'
  f'<p>花旗第 15 条：<b>坏消息出来不跌了、好消息出来不涨了，就该停下来想想</b>{F(1)}。</p>'
  '<p>做法：龙头公司发财报后，比较两件事。</p>'
  '<ul><li><b>超预期幅度</b>：成绩比市场预期好多少。</li>'
  '<li><b>股价反应</b>：之后 3 个交易日，股价比大盘多涨还是多跌。</li></ul>'
  '<p>两件事方向一致是正常的。<b>大超预期、股价却不涨，说明想买的人大多已经买了。</b></p>'
  '<p>比喻：一个已经吃饱的人，你再端上一盘好菜，他也吃不下。这个比喻也有漏洞：有时候人不吃，是因为突然听到了坏消息，而不是吃饱了。</p>'
  '<p><b>第一个测试样本：英伟达，2026-11-17 美东时间盘后发布（北京时间 11/18 凌晨）。</b></p>'
  f'<ul><li>营收 1,158 亿美元，比市场预期高 6.2%；下季指引 1,300 亿美元，比预期高 3.9%{F(16, 17)}。</li>'
  f'<li>盘后只涨了大约 2%–3.5%，而期权市场原本押的是 ±7% 到 ±8.5% 的波动{F(17, 18)}。</li>'
  '<li><b>这算「好消息涨得不够」的苗头，还谈不上「好消息不涨」。</b></li>'
  f'<li><b>干扰很大</b>：同一时期公司 CEO 黄仁勋宣布辞职{F(18)}，而且财报前这个月股价已经跌了约 24–25%。所以这个信号要打折看。</li>'
  '</ul>'
  '<p class="todo-note"><b>3 个交易日的完整反应，要等北京时间 11/21 早上才出齐。</b> ' + todo('待补') + '</p>'
  f'<p>我的 A 股版本里有一盏类似的灯：2026 年二季报 52 家公司，财报后 20 天的超额收益中位数是 −0.9%，黄灯{F(9)}。</p>')
w('<h3>指标 B：二线先伤（对应花旗第 13 条）</h3>'
  f'<p>花旗第 13 条：<b>行业变差时，二线公司最先受伤、伤得最重；行业变好时，二线最晚受益、受益最少</b>{F(1)}。</p>'
  '<p>做法：把同一行业的公司分成一线、二线两组，看三条差距：股价谁跑得好、毛利率差多少、营收增速差多少。</p>'
  f'<p><b>分组是按公司在这一轮 AI 周期里的位置，不按营收规模。</b> 以 A 股电路板为例{F(19)}：</p>'
  '<ul><li><b>一线</b>：胜宏科技、沪电股份、深南电路，主要做 AI 服务器和交换机板。</li>'
  '<li><b>二线</b>：鹏鼎控股、崇达技术、超声电子、世运电路，主要做消费电子和汽车板。</li>'
  '<li><b>鹏鼎营收规模很大，但我把它放在二线</b>，因为它的主力是苹果手机的软板，不是 AI 板。</li></ul>'
  '<p><b>这里有一个陷阱。</b> 按这个分法，二线几乎全做消费和汽车板。二线跑输一线，<b>很可能只是「AI 和非 AI 分化」，不是周期信号。</b>'
  '浅水先结冰的比喻在这里不成立：如果浅水和深水根本不是同一个池塘，浅水结冰只说明那个池塘冷，不说明整个湖要冻。</p>'
  '<p>所以我的读法是 ' + todo('待John确认') + '：</p>'
  '<ul><li><b>二线相对一线变差，在意料之中，不报警。</b></li>'
  '<li><b>真正要盯的有两种情况：</b>'
  '<ol><li>二线自己的毛利和营收开始绝对下滑。</li>'
  '<li><b>AI 板公司内部的弱者开始掉队，比如生益电子、广合科技。这才是 AI 周期见顶的早期信号。</b></li></ol></li></ul>'
  '<p><b>存储行业的方向可能反过来。</b> 做内存模组的小厂，低价时囤货，涨价时库存升值，毛利率反而可能比一线先好转。'
  '所以这条规则在存储业要先观察一个完整周期，再决定怎么用。</p></section>\n')

# ===== 07 局限
w(A.chapter('ch7', 7, '这套方法的局限', '这本账的价值，在于错了能看出错在哪里，而不是保证不会错。'))
w(A.callout('这本账的价值，在于错了能看出错在哪里，而不是保证不会错。'))
w('<ol>'
  '<li><b>账太新。</b> 只有 1 条预测到期，没有任何统计意义。概率是初稿，我还没确认。</li>'
  '<li><b>交期领先财报，还没有用我自己的交期数据回测过。</b> 现在的依据是村田、阿斯麦的订单数据和一线经验，而且应用材料就是反例。</li>'
  '<li><b>我只看得到自己经手的料。</b> 一个采购员看到的是几个品类、几家供应商，不是全行业。我说的「交期拉长」，可能只是我们公司的问题，比如份额小、拿货不稳。</li>'
  '<li><b>方向不等于节奏。</b> 交期拉长能告诉你行业在变热，但不能告诉你哪天见顶。从韩国芯片出口、内存现货价这些数据看，AI 链现在还很热，但「最早 2027 年中后期见顶」这个判断已经被挑战了。</li>'
  '<li><b>灯会在阈值附近来回跳</b>，比如 11/17 那盏估值灯一天变了两次。阈值是人定的，新指标的阈值完全没回测过。</li>'
  '<li><b>有些数据靠人工从新闻里摘。</b> CoreWeave 的违约保险价、英伟达的期权预期幅度，各家报的不一样，会过期，也可能摘错。</li>'
  '<li><b>花旗的 15 条是 2017 年针对美股写的</b>，那时没有「四家云厂商买走大部分 AI 芯片」这种结构。第 13 条用在今天的 A 股要打折。</li>'
  '<li><b>任何框架都会有它没见过的情况。</b> 这本账的价值，在于错了能看出错在哪里，而不是保证不会错。</li>'
  '</ol></section>\n')

# ===== 08 结尾
w(A.chapter('ch8', 8, '结尾', '周期一定会来；采购端只能看方向，看不了节奏；判断要写成能对答案的账。'))
w('<p>总结三句：</p>'
  '<ul><li><b>周期一定会来</b>，大约每 3.5 到 4 年一次，AI 改变的是幅度，不是规律。</li>'
  '<li><b>采购端的交期、报价和配额，往往比财报早一到两个季度</b>，但只能看方向，看不了节奏。</li>'
  '<li><b>我把判断写成可以对答案的账。</b> 现在对了 1 条，错了 0 条，作废 2 条，18 条正在受挑战。下一次对答案是 2026 年 12 月 20 日，美光财报。</li></ul>'
  '<p class="todo-note">如果你也在一线，比如采购、销售或计划，最近哪颗料的交期变了，欢迎留言告诉我。'
  + todo('待补') + ' 待John补一线素材：本期「现场一句话」，比如最近哪一颗料的交期或配额有变化。</p>'
  '<p>本文是个人研究记录，基于公开数据整理，<b>不构成投资建议</b>。</p></section>\n')

# ===== 来源
lis = ''.join(src_li(n, SRC[n]) for n in sorted(SRC))
w('<section id="apx" class="apxsec notes" data-toc="注 来源与注释"><header class="ch-h"><span class="ch-n">注</span><h2>来源与注释</h2></header>'
  '<details class="apx" id="apxSrc" open><summary>来源列表 <small>点任一上标会先弹出来源摘要</small></summary>'
  '<div class="body" id="src"><p class="sub">编号与初稿尾注一致。站点内链接用相对路径；标 ' + todo('待补') + ' 的条目，底层整理稿尚未单独做成公开页，没有换成外部链接。</p>'
  f'<ol class="src">{lis}</ol></div></details>\n</section>\n')

w('</main><footer class="wrap">Kiko 产业笔记 · 公开数据整理，不构成投资建议 · <a href="./">首页</a> · <a href="ledger.html">总账</a> · <a href="world/">世界指标</a></footer>\n')
w('<div class="fn-sheet" id="fnSheet" role="dialog" aria-modal="true" aria-label="来源" hidden><div class="fn-bd" data-close></div><div class="fn-card"><button class="fn-x" data-close aria-label="关闭">×</button><div class="fn-body" id="fnBody"></div></div></div>\n')
w('<script src="assets/reading.js"></script></body></html>\n')

html = A.fnify(''.join(o))
assert '不构成投资建议' in html
assert html.count('待补') >= 3
assert 'ledger.html#P001' in html and 'ledger.html#G01' in html
assert '黄仁勋宣布辞职' in html  # 初稿原文，不得改写
assert '1,158' in html and '259.4%' in html and '2.91%' in html and '39.2' in html
assert '/workspace/' not in html  # 不把内部路径写到公开页
out = os.path.join(ROOT, 'cycle-ledger.html')
open(out, 'w', encoding='utf-8').write(html)
print(f'articles/build.py: cycle-ledger.html 已生成（{len(html):,} 字）')
