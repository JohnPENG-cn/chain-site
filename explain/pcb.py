"""万物原理图 · 03：一块 AI 服务器 PCB 是怎么做出来的（规格文件，由 explain/build.py 读取）。
数字只来自 pcb/src.py 登记的公开来源（编号在本页内重排）与本站 PCB 研究页；没有来源的写“待补”，示意 / 自己算的标 {est} / {calc}。
"""
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, 'pcb'))
import src as _src          # noqa: E402  PCB 研究页来源表（key, 标题, url）
import research as _R       # noqa: E402  打分卡、BLUF、资本开支 / 折旧（Tushare）

# ---------- 来源：从 pcb/src.py 按 key 取，本页内按出现顺序编号 1..N；另加本站页面 ----------
_SITE = {
    'x_cowos': ('本站 CoWoS 原理图（封装那一层怎么做）', 'explain-cowos.html'),
    'x_pcb': ('本站 PCB 研究页（一分钟看懂、主要矛盾、判断；其中模型与判断为估）', 'pcb.html'),
    'x_pat': ('本站 PCB 格局页：六问打分卡（1–5 分，逐格证据与反例检验）', 'pcb-pattern.html'),
    'x_trk': ('本站 PCB 跟踪页（观察信号与阈值）', 'pcb-track.html'),
}
_ALL = {k: (t, u) for k, t, u in _src.SRC}
_ALL.update(_SITE)
_ORDER = []


def s(*keys):
    out = []
    for k in keys:
        assert k in _ALL, f'未知来源 {k}'
        if k not in _ORDER:
            _ORDER.append(k)
        out.append('{s:%d}' % (_ORDER.index(k) + 1))
    return ' '.join(out)


def n(k):
    s(k)
    return _ORDER.index(k) + 1


# 先按“讲到的顺序”登记，保证编号从第 1 步开始递增
for _k in ['prtop25', 'prq2', 'ms', 'tpu', 'kyber', 'tcf', 'mitjan', 'ctcud', 'hh', 'cq', 'jm', 'sq', 'dc', 'iekccl',
           'msap', 'm6', 'm7', 'm8', 'hd', 'uad', 'gsq', 'dzar', 'cowop', 'ajiabf', 'mdjabf', 'yole', 'cnasub', 'ctsub', 'sn',
           'x_cowos', 'doosan', 'uacu', 'hf', 'pr25t', 'emcir', 'udn2', 'sy', 'tft', 'tfn', 'x_pat', 'x_pcb', 'tsfin', 'capex', 'x_trk']:
    s(_k)

NUMS = _R.NUMS
SCORE = [dict(k=x['k'], n=x['n'], avg=x['avg'], v=x['v']) for x in _R.SCORE]
_best = max(SCORE, key=lambda x: x['avg'])

META = dict(
    id='pcb', file='explain-pcb.html', js='explain/pcb.js',
    title='一块 AI 服务器 PCB 是怎么做出来的', short='AI 服务器 PCB',
    kicker='万物原理图 · 03', ver='v0.1', date='2026-10-28',
    dek='一步一步拆开一块 AI 服务器的电路板：它由哪三样原料叠成，层和层怎么连，信号为什么会变弱，'
        'AI 为什么要 20 层以上、HDI 和低损耗材料，工厂里怎么一道道做出来，载板和 PCB 差在哪，以及每一环谁在赚钱。',
    card='从铜箔、玻纤布、树脂讲起，一层层压出一块多层板：覆铜板 → 压合 → 钻孔电镀 → 外层 → 测试；'
         'M6→M8 损耗滑块、HVLP 铜箔、HDI 与任意层，GB300 → Rubin → Kyber 平台滑块，最后看谁有定价权。',
    related=[('pcb.html', 'PCB 研究页（判断与信号）'), ('pcb-pattern.html', 'PCB 格局与打分卡'), ('explain-cowos.html', 'CoWoS 原理图')],
    nav=('pcb.html', 'PCB'), g0='VR200 NVL72', gen_label='平台', gen_aria='英伟达机柜平台', spd=False,
    howto='拖“平台”滑块，从 GB300 换到 Rubin、Kyber，第 9 步的图和卡片一起变；第 2、5、6、7 步还有各自的小滑块。',
    caliber='口径：层数、材料等级、机柜 PCB 价值取自券商与媒体转述（专家纪要标“弱”），英伟达官方不公布 PCB 规格；'
            '图中层厚、线宽、孔径都不按比例。信号损耗对比按教科书近似（介质损耗大致与 √Dk × Df 成正比）用松下公布的典型值现算，只比相对大小，不是实测插损；'
            '波形衰减与良率连乘是纯算术示意，不是厂商数据。份额、毛利率、打分来自本站 PCB 研究页与其来源；没有公开来源的格子写“待补”。',
    judge=('pcb.html', 'PCB 研究页'),
    gen_src=('srcs',), gen_tok=('boards', 'mat', 'cu', 'val', 'unlock', 'neck', 'note'),
)

# ---------- 平台数据：第 9 步的图、读数、卡片都从这里来 ----------
# L：每类板的层数（None = 没有这块板或待补）；rack：每柜 PCB 价值（万美元，None = 待补）
GENS = [
    dict(name='GB300 NVL72', year='2025', arch='Blackwell Ultra', L=dict(cmp=None, sw=24, mid=None, bp=None), rack=3.51, cuKg=31,
         srcs=[n('ms'), n('uacu')],
         boards='交换板 24 层 ' + s('ms') + '；计算板层数 待补；还没有中板（Rubin 才新增）',
         mat='计算板 M7 级覆铜板（Rubin 升到 M8）' + s('ms'),
         cu='整机高阶铜箔约 31 kg ' + s('uacu'),
         val='每柜 PCB 约 3.51 万美元 ' + s('ms'),
         unlock='72 颗 GPU 装进一个机柜，计算板和交换板之间要走大量高速线，带动 18 层以上的高多层板',
         neck='材料停在 M7，下一代要整体换到 M8，覆铜板、玻纤布、铜箔都要重新认证 ' + s('ms'),
         note='18 层以上高多层板 2026 年预计 +86.7%（全行业口径）' + s('prq2')),
    dict(name='VR200 NVL72', year='2026', arch='Vera Rubin', L=dict(cmp=26, sw=32, mid=44, bp=None), rack=11.67, cuKg=59,
         srcs=[n('ms'), n('doosan'), n('uacu'), n('uad')],
         boards='计算板 26 层 HDI；交换板 24 → 32 层；新增 44 层中板，每柜 18 块 ' + s('ms'),
         mat='计算板 M8 + 一代布、交换板 M8 + 二代布、中板 M9 + 二代布（专家纪要，弱）' + s('doosan'),
         cu='整机高阶铜箔约 59 kg，约为 GB300 的 1.9 倍 ' + s('uacu') + ' {calc}',
         val='每柜 PCB 约 11.67 万美元，约为 GB300 的 3.3 倍 ' + s('ms') + ' {calc}',
         unlock='用一块 44 层中板把计算板和交换板直接插在一起，层数、材料、铜箔一起升级 ' + s('ms'),
         neck='M9 板太硬：一根主钻针只能钻 100–200 个孔（M8 是 400–500 个）' + s('uad') + '；HVLP4 铜箔要把老线改造，有效产能约减半 ' + s('ctcud'),
         note='中板 M9 材料：台光电约 70%、斗山约 30%（纪要，弱）' + s('doosan')),
    dict(name='Kyber（Rubin Ultra）', year='2028（据报道推迟）', arch='Rubin Ultra', L=dict(cmp=None, sw=None, mid=None, bp=78), rack=None, cuKg=None,
         srcs=[n('kyber'), n('hf'), n('gsq')],
         boards='正交背板 78 层（3 块 26 层压在一起）、约 1 m² ' + s('kyber') + '；计算 / 交换板层数 待补',
         mat='原计划 M9 + Q 布（石英玻纤布）' + s('hf'),
         cu='待补',
         val='待补（尚未量产）',
         unlock='用一块超厚背板取代机柜里的线缆，计算板、交换板垂直插在背板两面 ' + s('kyber'),
         neck='超大、超厚的板难压合、难钻孔；SemiAnalysis 称推迟到 2028 年，英伟达回应路线图不变 ' + s('kyber'),
         note='Q 布很硬，钻针损耗是二代布的 2.6 倍 ' + s('gsq')),
]

# 给 JS 用的额外数据：来源编号、研究页数字（不手抄，构建时现取）
EXTRA = dict(sn={k: i + 1 for i, k in enumerate(_ORDER)}, score=SCORE, nums=NUMS)

_score_txt = '、'.join(f"{x['n'].split('（')[0]} {x['avg']}" for x in SCORE)

STEPS = [
dict(id='what', scene='what', t='什么是 PCB？', hint='点板上的部件看说明',
     parts=['board', 'chip', 'pad', 'trace', 'via'], body=f'''
<p><b>先说结论：</b>PCB（印制电路板）是电子设备的“地基 + 路网”。芯片、内存、电源都焊在它上面，它里面一层层的铜线负责把电和信号送到该去的地方。</p>
<p class="ex-ana"><b>打个比方：</b>芯片是一栋栋楼，PCB 是楼下的路网。楼越多、越高，路就要修得越多层、越密、越平。</p>
<p>这是一门大生意：2025 年全球 PCB 产值约 858 亿美元 {s('prtop25')}。Prismark 预计 2026 年涨到 1,134 亿美元（+32.1%）；涨得最快的是 18 层以上的板（+86.7%）和 HDI 板（+39.8%）{s('prq2')}，这两类正是 AI 服务器用的。</p>
<p class="note">图是一块服务器板的俯视示意：芯片、焊盘、铜线和过孔，尺寸不按比例。</p>'''),

dict(id='stack', scene='stack', t='一块板是怎么叠起来的？', hint='点层数按钮 · 点“展开 / 压紧”',
     parts=['mask', 'cu', 'pp', 'core'], w='layers', body=f'''
<p>PCB 不是一整块，而是像千层饼一样叠起来的：一层铜、一层绝缘，再一层铜、一层绝缘……最外面刷一层阻焊漆保护。</p>
<ol class="ex-keys">
<li><b>铜层</b>：真正走电和信号的地方，蚀刻成一根根线。</li>
<li><b>芯板（覆铜板，CCL）</b>：两面贴好铜箔、已经烤硬的绝缘板，是整块板的骨架。</li>
<li><b>半固化片（PP）</b>：浸了树脂、还没完全烤硬的玻纤布。压合时受热熔化，把芯板粘在一起。</li>
<li><b>阻焊</b>：最外面的保护漆（常见是绿色），只在要焊零件的地方开口。</li>
</ol>
<div class="ex-w" data-w="layers"></div>
<p>层数越多，能走的线越多，但压合对准和钻孔都更难。AI 服务器的板动辄几十层：英伟达 Rubin 机柜的交换板 32 层、中板 44 层 {s('ms')}；谷歌 TPU V7P 主板 44 层（专家纪要，弱）{s('tpu')}；Kyber 背板计划 78 层 {s('kyber')}。</p>'''),

dict(id='mat', scene='mat', t='三样原料：铜箔、玻纤布、树脂', hint='点按钮切换原料',
     parts=['foil', 'cloth', 'resin', 'ccl'], w='mat', body=f'''
<p>拆到最小，一块板只有三样东西：<b>铜箔</b>负责导电，<b>玻纤布</b>（玻璃纤维织的布）像钢筋，<b>树脂</b>像水泥，把布粘成硬板。三样压在一起，就是<b>覆铜板（CCL）</b>。</p>
<div class="ex-w" data-w="mat"></div>
<div class="ex-bd" data-m="foil"><p><b>铜箔：</b>AI 板要很平的铜箔，叫 HVLP（极低轮廓）。表面粗糙度 Rz 从 HVLP1 的 1.5 μm 降到 HVLP4 的 0.5 μm、HVLP5 的 0.4 μm {s('tcf')}。0.5 μm 大约是头发丝粗细的百分之一 {{est}}。</p>
<p>三井金属占 HVLP2 以上约 60%、HVLP5 约 80% {s('mitjan')}。把老线改做 HVLP3/4，有效产能约减半 {s('ctcud')}。</p></div>
<div class="ex-bd" data-m="cloth" hidden><p><b>玻纤布：</b>AI 板用低介电（low-Dk）布，从一代布、二代布，再到石英做的 Q 布。2024 年低介电布日东纺占 55%、旭化成 31%、台玻 11% {s('hh')}。</p>
<p>二代布每米 17.9–22.4 美元，Q 布 38.7–44.7 美元 {s('cq')}。宏和的电子布均价从 4.81 涨到 11.91 元/米，约 2.5 倍 {s('jm')} {{calc}}。</p></div>
<div class="ex-bd" data-m="resin" hidden><p><b>树脂：</b>决定信号损耗的关键配方。高端板用 PPO、碳氢树脂：圣泉的 PPO 树脂 2,000 吨/年满产满销 {s('sq')}；东材的 M9 级碳氢树脂已批量供货，M10 在验证 {s('dc')}。树脂的全球份额：待补。</p></div>
<div class="ex-bd" data-m="ccl" hidden><p><b>覆铜板：</b>把三样压成板材，卖给 PCB 厂。2025 年高速覆铜板市场 186.76 亿美元，台光电 16.2%、生益 13.2%、建滔 12.4% {s('iekccl')}。</p>
<p>行业习惯用松下 MEGTRON 的等级当行话：M6 → M7 → M8 → M9，数字越大，信号损耗越低（第 5 步细讲）。</p></div>'''),

dict(id='via', scene='via', t='层和层怎么连？', hint='点通孔 / HDI / 任意层',
     parts=['thru', 'blind', 'buried', 'cu'], w='via', body=f'''
<p>铜线只能在一层里横着走。要换层，就得打一个孔、在孔壁镀上铜，叫<b>过孔（via）</b>。</p>
<ol class="ex-keys">
<li><b>通孔</b>：机械钻头从上打穿到下。最简单，但它穿过的每一层，那个位置都被占了。</li>
<li><b>盲孔 / 埋孔</b>：只连相邻几层。盲孔用激光打，一头露在表面；埋孔藏在中间。大量用盲孔的板叫 <b>HDI（高密度互连）</b>。</li>
<li><b>任意层</b>：每一层都能用激光孔连到相邻层。线最密，工序也最多。</li>
</ol>
<div class="ex-w" data-w="via"></div>
<p>线也越做越细：HDI 常用的 mSAP 工艺，线宽 / 线距从 30/30 μm 走向 20/20 μm {s('msap')}。Rubin 的计算板是 26 层 HDI {s('ms')}，又高又密，两种难度叠在一起。</p>'''),

dict(id='sig', scene='sig', t='信号为什么会变弱？', hint='点材料与铜箔等级 · 看波形',
     parts=['trace', 'diel', 'foil', 'gnd'], w='loss', body=f'''
<p><b>先说结论：</b>信号跑得越快（频率越高），路上丢得越多。主要丢在两个地方：</p>
<ol class="ex-keys">
<li><b>被绝缘材料吸走（介质损耗）</b>：看两个数。Dk（介电常数）越低，信号跑得越快；Df（损耗因子）越低，被吸走的越少。</li>
<li><b>被粗糙的铜面消耗（导体损耗）</b>：频率很高时，电流只贴着铜线表面跑。表面坑坑洼洼，路就变长、损耗变大，所以要用很平的 HVLP 铜箔。</li>
</ol>
<p class="ex-ana"><b>打个比方：</b>像在跑道上跑步。Df 高是跑道太软、吸力气；铜面粗是跑道坑洼、要多绕路。</p>
<div class="ex-w" data-w="loss"></div>
<p>松下公布的典型值：M6 的 Df 是 0.0037（13 GHz）{s('m6')}，M7 是 0.0023 {s('m7')}，M8 是 0.0012（14 GHz）{s('m8')}。M8 的 Df 不到 M6 的三分之一 {{calc}}。M9 的公开 Df 值：待补。</p>'''),

dict(id='why', scene='why', t='AI 服务器为什么要这么多层？', hint='拖良率滑块 · 点层数',
     parts=['b_sw', 'b_cmp', 'b_mid', 'b_bp', 'b_tpu'], w='yield', body=f'''
<p><b>先说结论：</b>一个 AI 机柜里，几十颗 GPU 要高速互传数据，还要吃下很大的电流。线多，层就多；线快，材料就要低损耗；线密，就要 HDI。三样一起升级，PCB 从配角变成了贵重部件。</p>
<p>摩根士丹利拆了英伟达机柜：GB300 NVL72 每柜 PCB 约 3.51 万美元，VR200 NVL72 约 11.67 万美元（+233%）；交换板从 24 层升到 32 层，还新增 18 块 44 层中板 {s('ms')}。</p>
<p>层多的代价是良率：一块几十层的板，只要一层出问题，整块就报废。拖下面的滑块，看每层良率连乘以后剩多少。</p>
<div class="ex-w" data-w="yield"></div>
<p>做得出高层板的厂，现在赚得多：沪电 2026 年上半年 32 层及以上的收入增长 190.83%，PCB 毛利率 40.52% {s('hd')}。</p>'''),

dict(id='make', scene='make', t='工厂里怎么做出来？', hint='拖工序滑块 · 看剖面一步步长出来',
     parts=['core', 'pp', 'thru', 'cu', 'mask', 'drill'], w='flow', body=f'''
<p>一块多层板在工厂里大致走下面八步，每一步里还有很多小工序。HDI 板要把“压合 → 钻孔 → 电镀 → 做线”重复好几轮，每加一层盲孔就多一轮。</p>
<div class="ex-w" data-w="flow"></div>
<p>最难的是<b>压合</b>和<b>钻孔</b>。压合时几十层要对得很准；钻孔时材料越高端越硬。在 M9 板上，一根主钻针只能钻 100–200 个孔，M8 板是 400–500 个 {s('uad')}。Q 布对钻针的损耗是二代布的 2.6 倍 {s('gsq')}。</p>
<p>所以上游的钻针和钻孔机也跟着紧：钻针鼎泰占 29.2%、金洲 21.1%，进口开槽机交期 1–2 年 {s('uad')}；机械钻孔机大族数控约占全球 50%（公司测算）{s('dzar')}。电镀、曝光、压合设备的份额：待补。</p>'''),

dict(id='sub', scene='sub', t='IC 载板和 PCB 差在哪？', hint='点按钮切换 · 比较线宽',
     parts=['chip', 'bump', 'subs', 'bga', 'board'], w='sub', body=f'''
<p><b>先说结论：</b>IC 载板是小号、精密版的 PCB。它夹在芯片和主板中间：芯片底下的焊点太密，主板接不上，载板负责把间距一层层放大。</p>
<p>差在线宽：PCB 上 HDI 的线宽 / 线距在 20–30 μm {s('msap')}。如果要让 PCB 直接接芯片（CoWoP，省掉载板），要从现在约 20/35 μm 缩到 10/10 μm 以下 {s('cowop')}。</p>
<div class="ex-w" data-w="sub"></div>
<div class="ex-bd" data-m="abf"><p><b>ABF 膜：</b>高端载板的绝缘层用味之素的 ABF 膜，1999 年上市，公司自述全球份额约 95% {s('ajiabf')}。ABF 交期从 3–4 个月拉长到 12 个月以上，压膜设备交期 12–18 个月 {s('mdjabf')}。</p></div>
<div class="ex-bd" data-m="mkt" hidden><p><b>市场与玩家：</b>先进载板 2024 年 142 亿美元，Yole 预计 2030 年 310 亿 {s('yole')}。前五大：欣兴 16%、SEMCO 9.9%、Ibiden 9.3%、AT&amp;S 9.1%、南电 8.7% {s('cnasub')}；2025 年份额：待补。</p>
<p>载板均价每季涨 7% 以上，新厂要到 2029 年 {s('ctsub')}。深南电路上半年载板毛利率 31.35% {s('sn')}。</p></div>
<div class="ex-bd" data-m="cowop" hidden><p><b>CoWoP：</b>想把芯片 + 中介层直接贴到 PCB 上，省掉 ABF 载板；但仍很早期，板厂自己也存疑 {s('cowop')}。中介层那一层怎么封，见 <a href="explain-cowos.html">CoWoS 原理图</a> {s('x_cowos')}。</p></div>'''),

dict(id='ladder', scene='gen', t='一代一代升级了什么？', hint='拖“平台”滑块，或点卡片',
     parts=['b_cmp', 'b_sw', 'b_mid', 'b_bp'], w='ladder', body=f'''
<p>拖顶上的“平台”滑块，看英伟达机柜每换一代，板子多了什么。层数、材料、铜箔来自券商和媒体转述，英伟达官方不公布 PCB 规格。</p>
<div class="ex-w" data-w="ladder"></div>
<p>谷歌 TPU 也在走同一条路：V7 主板 36 层、V7P 44 层，覆铜板从 M8 向 M9 升（专家纪要，弱）{s('tpu')}。</p>
<p class="note">没有公开来源的格子写“待补”，不猜。</p>'''),

dict(id='who', scene='who', t='谁在赚钱？谁说了算？', hint='点环节看玩家和证据',
     parts=['board', 'ccl', 'cloth', 'foil', 'drill', 'subs'], w='who', body=f'''
<p><b>先说结论：</b>一块 AI 板的钱分给好几环。越往上游、越集中、越难复制的环节，越有涨价的底气。</p>
<div class="ex-w" data-w="who"></div>
<div class="ex-bd" data-m="board"><p><b>板厂：</b>2025 年营收臻鼎 58.7 亿美元、欣兴 42.3、东山 35.7、深南 33.0、TTM 29.1、沪电 27.6、胜宏 26.9 {s('pr25t')}。AI 板龙头增长超过 50%，多数板厂不到 10% {s('prtop25')}。高层板、HDI 按厂的份额：待补。</p></div>
<div class="ex-bd" data-m="ccl" hidden><p><b>覆铜板：</b>台光电在高速无卤覆铜板占 38.6%，二季度毛利率 33.9% {s('emcir')}；台光电 M7 以上占比 60–65%，陆资覆铜板上半年涨价约 15%、最缺的料号涨 30–40% {s('udn2')}。生益覆铜板毛利率 29.16% {s('sy')}。</p></div>
<div class="ex-bd" data-m="cloth" hidden><p><b>电子布：</b>低介电布日东纺 55%、低 CTE 布日东纺 85% {s('hh')}；T-glass 日东纺约占九成 {s('tft')}。日东纺电子材料营业利益 280 亿日元（+44%），英伟达、微软、谷歌、亚马逊订走了多数高端产能 {s('tfn')}。新产线要 18–24 个月 {s('jm')}。</p></div>
<div class="ex-bd" data-m="foil" hidden><p><b>铜箔：</b>三井金属占 HVLP2 以上约 60%、HVLP5 约 80% {s('mitjan')}。Rubin 整机高阶铜箔约 59 kg，GB300 约 31 kg {s('uacu')}。</p></div>
<div class="ex-bd" data-m="drill" hidden><p><b>钻针与设备：</b>钻针鼎泰 29.2%、金洲 21.1%、佑能 10.4%、尖点 9.9% {s('uad')}；机械钻孔机大族数控约 50% {s('dzar')}。材料越硬，针耗越多。</p></div>
<div class="ex-bd" data-m="subs" hidden><p><b>IC 载板：</b>ABF 膜味之素自述约 95% {s('ajiabf')}；载板前五大合计过半 {s('cnasub')}。见第 8 步。</p></div>
<p>本站 PCB 格局页按六个问题给每一环打分（1–5 分，越高越像结构性好生意）{s('x_pat')}。上面图里的柱子是平均分：{_score_txt}。最高的是{_best['n']}（{_best['v']}）。</p>'''),

dict(id='watch', scene='watch', t='接下来盯什么？', hint='三个信号',
     parts=['capex'], body=f'''
<p>研究页最要紧的一句话：{_R.BLUF[0]} {s('x_pcb')}</p>
<p>10 家 A 股大板厂 2026 年上半年花在厂房和机器上的钱（资本开支）有 {NUMS['capH1']} 亿元，是同期折旧的 {NUMS['rH1']} 倍；上一轮扩产最猛的 {NUMS['pk']} 年也只有 {NUMS['rPk']} 倍 {s('tsfin')}。年内 20 家 A 股板厂宣布的扩产投资超过 800 亿元，高端产能 2–3 年后集中释放 {s('capex')}。</p>
<ol class="ex-keys">
<li><b>平台节奏</b>：Kyber 是不是真推迟到 2028 年 {s('kyber')}。</li>
<li><b>材料价格</b>：覆铜板、电子布、铜箔还在不在涨价；建滔年内已发第 7 次覆铜板涨价函 {s('jm')}。</li>
<li><b>板厂毛利率</b>：龙头和中小厂的差距；沪电 PCB 毛利率 40.52% {s('hd')}，崇达只有 7.67% {s('jm')}。</li>
</ol>
<p>逐项阈值见 <a href="pcb-track.html">PCB 跟踪页</a> {s('x_trk')}。</p>'''),

dict(id='quiz', scene='who', t='小测验：五个问题', hint='点问题看答案',
     parts=['board', 'ccl', 'cloth', 'foil', 'drill', 'subs'], w='quiz', body='''
<p>不看上面，试着回答：</p>
<div class="ex-w" data-w="quiz"></div>'''),
]

QUIZ = [
    ('芯板和半固化片有什么区别？',
     '芯板（覆铜板）已经烤硬、两面贴着铜箔，是骨架；半固化片是浸了树脂、还没完全固化的玻纤布，压合时熔化，把芯板粘成一整块。'),
    ('Df 低意味着什么？M6 和 M8 差多少？',
     '信号被绝缘材料吸走的少。松下典型值 M6 是 0.0037 ' + s('m6') + '，M8 是 0.0012 ' + s('m8') + '，不到三分之一 {calc}。'),
    ('为什么层数越多越难做？',
     '每一层都可能出错，良率要连乘；层越多、材料越硬，钻孔也越难：M9 板一根主钻针只能钻 100–200 个孔 ' + s('uad') + '。'),
    ('IC 载板和 PCB 最大的不同是什么？',
     '载板离芯片最近、线更细，负责把芯片的密集焊点放大到主板能接的间距。高端载板用味之素 ABF 膜（公司自述约 95%）' + s('ajiabf') + '；想让 PCB 直接接芯片（CoWoP），线宽线距要缩到 10/10 μm 以下 ' + s('cowop') + '。'),
    ('按本站打分卡，哪一环最接近“结构性”好生意？',
     f"{_best['n']}，平均 {_best['avg']} 分（{_best['v']}）" + s('x_pat') + '：材料越硬针耗越多，换代反而让用量变多。'),
]

SOURCES = [(i + 1, _ALL[k][0], _ALL[k][1]) for i, k in enumerate(_ORDER)]
