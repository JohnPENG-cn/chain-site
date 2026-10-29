"""万物原理图 · 04：一块机械硬盘（HDD）是怎么存数据的（规格文件，由 explain/build.py 读取）。
数字只来自下面 _ALL 登记的公开来源（编号按出现顺序）；二手纪要标“弱”，没有来源的写“待补”，示意 / 自己算的标 {est} / {calc}。
"""

# ---------- 来源表：key -> (标题, url)；本页内按出现顺序编号 1..N ----------
_ALL = {
    'moz3': ('Seagate：What is Mozaic 3+（HAMR 原理、每碟 3TB、功耗 / TB 对比，2024）',
             'https://www.seagate.com/resources/what-is-mozaic-3plus-how-does-it-work-and-what-can-it-do-for-my-data-center/'),
    'he': ('Western Digital 博客：Explained: Helium Hard Drives（2023-08-29）', 'https://blog.westerndigital.com/helium-hard-drives-explained/'),
    'smr': ('Zoned Storage（WD 主导的开源文档）：Shingled Magnetic Recording Hard Disks', 'https://zonedstorage.io/docs/introduction/smr'),
    'moz': ('Seagate：Mozaic 平台介绍页（每碟 10TB 路线图）', 'https://www.seagate.com/innovation/mozaic/'),
    'moz4': ('Seagate 新闻稿：Mozaic 4+，最高 44TB（2026-03-03）',
             'https://investors.seagate.com/news/news-details/2026/Seagate-Delivers-Industrys-Highest-Capacity-Hard-Drives-with-Next-Generation-Mozaic-4/default.aspx'),
    'moz3pr': ('Seagate 新闻稿：30TB Mozaic 3+ 开始放量（2024-01-17）',
               'https://investors.seagate.com/news/news-details/2024/Seagates-Breakthrough-30TB-Hard-Drives-Ramp-Volume-Marking-an-Inflection-Point-in-the-Storage-Industry/default.aspx'),
    'tsb12': ('东芝新闻稿：业界首个验证 12 碟堆叠（2025）',
              'https://news.toshiba.com/press-releases/press-release-details/2025/Toshiba-First-in-Industry-to-Verify-12-Disk-Stacking-Technology-for-Hard-Drives/default.aspx'),
    'tsbr': ('TechRadar：东芝路线图幻灯片（40TB 级 MAMR、HAMR 45TB、2030 年 55TB）',
             'https://www.techradar.com/pro/toshiba-wants-to-launch-a-55tb-hard-drive-by-2030-40tb-model-set-to-appear-in-2026-new-slides-show'),
    'wdc_q': ('WD 新闻稿：2027 财年第一季度业绩', 'https://investor.wdc.com/news-releases/news-release-details/wd-reports-fiscal-first-quarter-2027-financial-results'),
    'wdc_t': ('WD 2027 财年 Q1 电话会文字稿（The Motley Fool，2026-10-22）', 'https://www.fool.com/earnings/call-transcripts/2026/10/22/wdc-wdc-q1-2027-earnings-call-transcript/'),
    'stx_q': ('Seagate 新闻稿：2027 财年第一季度业绩',
              'https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-First-Quarter-2027-Financial-Results/default.aspx'),
    'stx_t': ('Seagate 2027 财年 Q1 电话会文字稿（The Motley Fool，2026-10-28）', 'https://www.fool.com/earnings/call-transcripts/2026/10/28/seagate-stx-q1-2027-earnings-call-transcript/'),
    'stxb': ('Seagate 博客：Why HDDs dominate hyperscale cloud architecture', 'https://www.seagate.com/blog/why-hdds-dominate-hyperscale-cloud-architecture/'),
    'jpm': ('摩根大通 × TSR 专家会纪要（发现报告转载；二手纪要，弱）', 'https://www.fxbaogao.com/detail/5682004'),
    'tf_px': ('TrendForce：HDD 缺货推动 QLC SSD（2025-10-14）', 'https://www.trendforce.com/presscenter/news/20251014-12744.html'),
    'tf_52': ('TrendForce：近线 HDD 交期超过 52 周（2025-09-15）', 'https://www.trendforce.com/presscenter/news/20250915-12714.html'),
    'tf_lt': ('TrendForce Weekly Radar #006（HDD 交期约 50 周、缺货延续到 2028）', 'https://insights.trendforce.com/p/weekly-radar-006'),
    'lb': ('长桥海豚投研：HDD 行业分析（二手，弱）', 'https://longbridge.com/zh-CN/dolphin/post/44544204'),
    'cough': ('Forbes / Tom Coughlin：2025 年 HDD 行业回顾（原文本站未能打开，据搜索摘要转述，弱）',
              'https://www.forbes.com/sites/tomcoughlin/2026/02/02/c4q-2025-and-2025-hard-disk-drive-industry-update/'),
    'nidec': ('StorageNewsletter：尼得科 2023 财年 Q4（HDD 主轴电机份额 >70%）', 'https://www.storagenewsletter.com/2024/05/13/nidec-fiscal-4q23-financial-results/'),
    'hoya': ('HOYA 投资者材料：10 分钟读懂 HOYA（玻璃基板）', 'https://www.hoya.com/ir/2025/en/common/files/10min_read.pdf'),
    'reso': ('Resonac 新闻稿：HDD 介质增产与价格调整（2026-07-28）', 'https://www.resonac.com/news/2026/07/28/3953.html'),
    'x_hdd': ('本站 HDD 链库页（总览，待补较多）', 'hdd.html'),
    'x_hbm': ('本站 HBM 原理图（AI 用的另一种“存储”）', 'explain-hbm.html'),
}
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


for _k in ['moz3', 'he', 'smr', 'moz3pr', 'moz4', 'moz', 'tsb12', 'tsbr', 'wdc_q', 'wdc_t', 'stx_q', 'stx_t',
           'stxb', 'jpm', 'tf_px', 'tf_52', 'tf_lt', 'lb', 'cough', 'nidec', 'hoya', 'reso', 'x_hbm', 'x_hdd']:
    s(_k)

META = dict(
    id='hdd', file='explain-hdd.html', js='explain/hdd.js',
    title='一块机械硬盘是怎么存数据的', short='机械硬盘 HDD',
    kicker='万物原理图 · 04', ver='v0.1', date='2026-10-29',
    dek='一步一步拆开一块数据中心用的机械硬盘：盘片、主轴、磁头、音圈电机怎么配合；一个 0 或 1 怎么写进去、读出来；'
        'SMR、充氦、HAMR 各解决什么；容量怎么从 20TB 走向 40TB 以上；AI 为什么还离不开它；以及谁在卡谁的脖子。',
    card='从盘片和磁头讲起：一个比特怎么写和读，CMR 与 SMR，充氦，PMR → MAMR → HAMR 代际滑块，'
         '每 TB 成本计算器（HDD 对 SSD），交期与长约，三家整机厂和磁头、介质、玻璃基板、电机的格局。',
    related=[('hdd.html', 'HDD 链库页（总览）'), ('explain-hbm.html', 'HBM 原理图'), ('explain-pcb.html', 'PCB 原理图')],
    nav=('hdd.html', 'HDD'), g0='HAMR · Mozaic 4+', gen_label='代际', gen_aria='硬盘记录技术代际', spd=False,
    howto='拖“代际”滑块，从传统 PMR 换到 MAMR、HAMR，第 5 步的盘片堆和卡片一起变；第 2、3、4、8、10 步还有各自的按钮或滑块。',
    caliber='口径：原理部分取自希捷、西部数据官方技术文章与开源文档；容量、路线图来自公司新闻稿、财报电话会与媒体转述的路线图幻灯片；'
            '每 GB 价格、份额等来自专家纪要与媒体（标“弱”）。图中盘片、磁头、磁粒都不按比例。'
            '成本计算器只做“价格 × 容量”的算术，不含服务器、电力和机房，不是总拥有成本（TCO）。没有公开来源的格子写“待补”。',
    judge=('hdd.html', 'HDD 链库页'),
    gen_src=('srcs',), gen_tok=('tech', 'per', 'unlock', 'neck', 'note'),
)

# ---------- 代际数据：第 5 步的图、读数、卡片都从这里来 ----------
# tb：每张盘片容量（TB，None=待补）；nd：盘片数（None=待补）；cap：整盘标称容量（TB）
GENS = [
    dict(name='PMR / CMR · 16TB', year='基准（约 2019 起的主流）', tb=1.78, nd=9, cap=16, heat=False, mamr=False,
         srcs=[n('moz3')],
         tech='传统垂直记录（PMR），磁道之间留空隙（CMR）',
         per='每碟 1.78TB；16TB 整盘约 9 碟 ' + s('moz3') + ' {calc}',
         unlock='把磁粒“站起来”排（垂直记录），再充氦多塞几张盘片',
         neck='传统材料每碟过了约 2.4TB 就很难再密 ' + s('moz3'),
         note='年份为本站 {est}；希捷用它做功耗对比的基准：0.59 瓦 / TB ' + s('moz3')),
    dict(name='ePMR · 40TB（WD）', year='2026–27', tb=None, nd=None, cap=40, heat=False, mamr=False,
         srcs=[n('wdc_t')],
         tech='加强版 PMR（ePMR），不用激光',
         per='每碟容量、碟数：待补（WD 未公开）',
         unlock='不换介质，靠更精细的写头和信号处理继续挤密度 {est}',
         neck='WD 自己也在准备 HAMR：认证 2027 年一季度、量产 2027 年上半年 ' + s('wdc_t'),
         note='WD 称 40TB ePMR 在 FQ2 占近线出货约 30%、FQ3 约 50% ' + s('wdc_t')),
    dict(name='MAMR · 12 碟（东芝）', year='2027（路线图）', tb=None, nd=12, cap=40, heat=False, mamr=True,
         srcs=[n('tsb12'), n('tsbr')],
         tech='微波辅助记录（MAMR）：写的时候加一点微波能量',
         per='12 碟堆叠已验证 ' + s('tsb12') + '；每碟容量：待补',
         unlock='盘片更薄、塞 11–12 张，配合 MAMR 做到 40TB 级 ' + s('tsbr'),
         neck='12 碟要更薄的玻璃基板；东芝下一步也转 HAMR（2028 年 45TB）' + s('tsbr'),
         note='东芝是三家里最小的一家 ' + s('cough')),
    dict(name='HAMR · Mozaic 3+', year='2024 放量', tb=3, nd=10, cap=30, heat=True, mamr=False,
         srcs=[n('moz3'), n('moz3pr')],
         tech='热辅助记录（HAMR）：激光把一小点盘面加热再写',
         per='每碟 3TB，30TB 约 10 碟 ' + s('moz3') + ' {calc}',
         unlock='换成更“硬”的铁铂合金磁粒，常温下极稳，靠激光加热才写得动 ' + s('moz3'),
         neck='激光、近场“天线”和玻璃基板都要重新做，良率爬坡慢',
         note='同样存 1TB，功耗从 0.59 降到 0.32 瓦（−45%）' + s('moz3')),
    dict(name='HAMR · Mozaic 4+', year='2026', tb=4, nd=10, cap=44, heat=True, mamr=False,
         srcs=[n('moz4')],
         tech='第二代量产 HAMR',
         per='每碟 4TB 以上，10 碟，最高 44TB ' + s('moz4'),
         unlock='同一套平台继续把每碟做密 ' + s('moz4'),
         neck='产能：希捷说 2026 年底 HAMR 约占近线出货 EB 的一半 ' + s('stx_t'),
         note='已在两家超大规模云厂通过认证 ' + s('moz4')),
    dict(name='路线图 · 每碟 10TB', year='待补（希捷未给年份）', tb=10, nd=10, cap=100, heat=True, mamr=False,
         srcs=[n('moz')],
         tech='HAMR 继续迭代',
         per='每碟 10TB 目标 ' + s('moz') + '；10 碟约 100TB {calc}',
         unlock='更小的磁粒、更准的加热点',
         neck='年份没有公开来源：待补',
         note='东芝路线图：约 2030 年 55TB ' + s('tsbr')),
]

EXTRA = dict(sn={k: i + 1 for i, k in enumerate(_ORDER)})

STEPS = [
dict(id='what', scene='what', t='机械硬盘里有什么？', hint='点图上的部件看说明',
     parts=['platter', 'spindle', 'arm', 'head', 'vcm', 'pcb'], body=f'''
<p><b>先说结论：</b>机械硬盘（HDD）像一台极小的唱片机。几张亮晶晶的圆盘一直在转，一根细臂带着磁头在盘面上来回扫，把数据写成一个个小磁点。</p>
<ol class="ex-keys">
<li><b>盘片</b>：存数据的圆盘，表面镀了一层很薄的磁性材料。</li>
<li><b>主轴电机</b>：让盘片高速旋转。</li>
<li><b>磁头</b>：在盘面上方“飞”，负责写和读。</li>
<li><b>磁头臂 + 音圈电机（VCM）</b>：音圈电机像喇叭里的线圈，通电就推着臂转，把磁头送到要去的那一圈。</li>
<li><b>电路板</b>：控制芯片和缓存，指挥上面这一切。</li>
</ol>
<p class="ex-ana"><b>打个比方：</b>盘片是唱片，磁头是唱针。不同的是，唱针压着唱片，磁头不碰盘面。</p>
<p>磁头离盘面只有“几埃”的距离 {s('moz3')}。1 埃是 0.1 纳米，比一根头发细几十万倍 {{est}}。</p>
<p class="note">图是俯视示意，比例不准。</p>'''),

dict(id='bit', scene='bit', t='一个 0 或 1 怎么写进去、读出来？', hint='点“写 / 读” · 点比特翻转',
     parts=['writer', 'reader', 'grain', 'track'], w='bit', body=f'''
<p>盘面上的磁性层由很多极小的<b>磁粒</b>组成。一小撮磁粒朝上，算 1；朝下，算 0。</p>
<ol class="ex-keys">
<li><b>写</b>：写头是一块小电磁铁。电流一换方向，下方磁粒的方向就跟着翻。</li>
<li><b>读</b>：读头不发力，只“感觉”下方磁场。朝上和朝下时，它的电阻不一样，电路就读出 1 或 0。</li>
</ol>
<div class="ex-w" data-w="bit"></div>
<p>现在的读头用隧穿磁阻（TMR）效应：磁场方向一变，电阻就跳一下 {s('moz3')}。希捷 HAMR 盘上，铁铂合金磁粒只有几纳米大 {s('moz3')}。</p>
<p>磁粒越小，一张盘能存越多。但磁粒太小会“自己翻”，数据就丢了。整个硬盘行业几十年都在和这个矛盾较劲。</p>'''),

dict(id='density', scene='density', t='磁道挨得多近？CMR 和 SMR', hint='点 CMR / SMR 比较',
     parts=['track', 'gap', 'zone'], w='trk', body=f'''
<p>数据沿着一圈一圈的<b>磁道</b>写。希捷 HAMR 盘每英寸超过 100 万条磁道 {s('moz3')}，也就是 1 毫米里约 4 万条 {{calc}}。</p>
<div class="ex-w" data-w="trk"></div>
<div class="ex-bd" data-m="cmr"><p><b>CMR（常规记录）：</b>磁道之间留一条缝，互不干扰。改哪里就写哪里，随机写很快 {s('smr')}。</p></div>
<div class="ex-bd" data-m="smr" hidden><p><b>SMR（叠瓦记录）：</b>写头比磁道宽，后一条磁道压住前一条的一部分，像屋顶的瓦片。省下了缝，能多存一些 {s('smr')}。</p>
<p>代价是：改一个地方，要把压在上面的整片磁道（叫“区”）重写一遍。所以 SMR 适合一次写好、很少改的数据 {s('smr')}。</p></div>
<p class="ex-ana"><b>打个比方：</b>CMR 像停车场每个车位都留通道；SMR 像把车一辆挨一辆塞紧，要挪里面那辆，外面的都得先开走。</p>'''),

dict(id='helium', scene='helium', t='为什么要往硬盘里充氦气？', hint='点“空气 / 氦气”比较',
     parts=['platter', 'gas', 'seal'], w='gas', body=f'''
<p>盘片转得很快，空气会搅出乱流，晃动磁头，也费电。</p>
<p>氦气的密度只有空气的约 1/7 {s('he')}。乱流小了，盘片可以做得更薄、摆得更密。空气盘最多放 6 张盘片，氦气盘最多 10 张 {s('he')}。</p>
<div class="ex-w" data-w="gas"></div>
<p>难点是“关住”氦气。氦原子很小，容易漏，硬盘外壳要完全密封 {s('he')}。第一块商用充氦硬盘 2013 年由 HGST（现属西部数据）推出 {s('he')}。</p>
<p>盘片还在加：东芝已经验证把盘片做到 12 张 {s('tsb12')}。</p>'''),

dict(id='ladder', scene='gen', t='一代一代升级了什么？', hint='拖“代际”滑块，或点卡片',
     parts=['platter', 'head'], w='ladder', body=f'''
<p>整盘容量 ≈ 每张盘片的容量 × 盘片数。所以升级只有两条路：<b>每张存更多</b>，或者<b>塞更多张</b>。</p>
<div class="ex-w" data-w="ladder"></div>
<p>三家走的路不同：希捷直接上 HAMR {s('moz4')}；西部数据先把 ePMR 做到 40TB，再接 HAMR {s('wdc_t')}；东芝先用 MAMR 加 12 碟 {s('tsbr')}。</p>
<p class="note">卡片里没有公开来源的格子写“待补”，不猜。</p>'''),

dict(id='hamr', scene='hamr', t='HAMR：用激光“烫”一下再写', hint='点激光开 / 关',
     parts=['laser', 'nft', 'media', 'glass'], w='laser', body=f'''
<p><b>先说结论：</b>想让磁粒更小又不“自己翻”，就要用更“硬”的磁性材料。可是太硬了，写头也翻不动它。HAMR 的办法是：写的那一瞬间，用激光把那一小点加热，让它暂时变软。</p>
<ol class="ex-keys">
<li><b>激光</b>：装在磁头上的微型激光器。</li>
<li><b>光“漏斗”和“天线”</b>：把光挤到比光波长还小的一点上（近场光学）。</li>
<li><b>加热</b>：不到 2 纳秒，把那一点烧到 800°F（约 430°C）以上 {s('moz3')}。</li>
<li><b>写完就冷</b>：冷下来后磁粒又变“硬”，数据稳稳留住。</li>
</ol>
<div class="ex-w" data-w="laser"></div>
<p>介质换成铁铂超晶格合金，长在特制玻璃基板上 {s('moz3')}。普通铝基板受不了这种反复加热，HAMR 需要玻璃基板 {s('hoya')}。</p>
<p class="ex-ana"><b>打个比方：</b>像给冷蜡封盖章：先用火烤软一个点，盖完印，蜡一凉就定型。</p>'''),

dict(id='road', scene='road', t='容量路线图：20 → 30 → 40+TB', hint='点图上的点看来源',
     parts=['p_stx', 'p_wdc', 'p_tsb'], w='road', body=f'''
<p>把三家公开过的节点放在一张图上：</p>
<div class="ex-w" data-w="road"></div>
<ol class="ex-keys">
<li><b>希捷</b>：2024 年 30TB Mozaic 3+ 放量 {s('moz3pr')}；2026 年 Mozaic 4+ 最高 44TB {s('moz4')}；目标每碟 10TB {s('moz')}。</li>
<li><b>西部数据</b>：40TB ePMR 正在放量；HAMR 2027 年一季度认证、上半年量产 {s('wdc_t')}。</li>
<li><b>东芝</b>：40TB 级 MAMR（11–12 碟）2027 年；HAMR 45TB 2028 年；约 2030 年 55TB {s('tsbr')}。</li>
</ol>
<p class="note">东芝节点来自媒体转述的幻灯片；希捷 100TB 没给年份，图上放在最右边并标“待补”。</p>'''),

dict(id='why', scene='why', t='AI 为什么还要机械硬盘？', hint='拖容量滑块 · 看两种盘各要多少钱',
     parts=['b_hdd', 'b_ssd'], w='cost', body=f'''
<p><b>先说结论：</b>AI 要存的东西太多：训练数据、模型版本、日志、生成的图片视频。大部分很少被读，但必须留着。这类数据按每 TB 算钱，机械硬盘便宜得多。</p>
<p>专家纪要给出的 2026 年价格：HDD 每 GB 约 0.016 美元，企业级 SSD 约 0.243 美元，差约 15 倍；2025 年约 6–7 倍（弱）{s('jpm')}。TrendForce 的口径：HDD 每 GB 从 0.012–0.013 美元涨到 0.015–0.016 美元 {s('tf_px')}。</p>
<div class="ex-w" data-w="cost"></div>
<p>希捷称超大规模云厂超过 90% 的数据（按 EB 算）放在 HDD 上 {s('stxb')}。1 EB（艾字节）= 100 万 TB，相当于 2.5 万块 40TB 硬盘 {{calc}}。</p>
<p>SSD 的长处是快：每秒读写次数（IOPS）高、功耗低 {s('tf_px')}。所以常见做法是热数据放 SSD，冷数据放 HDD。和 GPU 贴身的高速内存是另一回事，见 <a href="explain-hbm.html">HBM 原理图</a> {s('x_hbm')}。</p>'''),

dict(id='supply', scene='supply', t='为什么现在缺货、涨价？', hint='点按钮比较交期',
     parts=['b_lt0', 'b_lt1'], w='lt', body=f'''
<p><b>先说结论：</b>需求涨得比产能快，而新建产能很慢。</p>
<p>TrendForce：近线硬盘交期约 50 周，供需平衡时约 16 周；缺货可能延续到 2028 年 {s('tf_lt')}。2025 年 9 月交期已超过 52 周 {s('tf_52')}。“近线盘”指数据中心用的 3.5 英寸大容量盘。</p>
<div class="ex-w" data-w="lt"></div>
<p>摩根士丹利估计 2026 年需求增长 40–50%、供给只增 30–35%；新建一座厂至少要两年（二手转述，弱）{s('lb')}。</p>
<p>厂商把缺口变成了长约：希捷说大部分近线产能已签长约到 2028 年，部分到 2030 年，2027 年价格已定 {s('stx_t')}。西部数据每 TB 价格同比涨 28% {s('wdc_t')}。</p>
<p>结果是利润率很高：希捷本季非 GAAP 毛利率 57.8% {s('stx_q')}；西部数据 58.1% {s('wdc_q')}。</p>'''),

dict(id='who', scene='who', t='谁在做？谁说了算？', hint='点环节看玩家和证据',
     parts=['m_drive', 'm_head', 'm_media', 'm_sub', 'm_motor', 'm_mag'], w='who', body=f'''
<p><b>先说结论：</b>整机只有三家，几个关键零件也只有一两家能做。越集中、越难扩产的环节，越能谈价格。</p>
<div class="ex-w" data-w="who"></div>
<div class="ex-bd" data-m="drive"><p><b>整机：</b>2025 年按出货台数，西部数据 42.3%、希捷 40.8%、东芝 17.0%（弱）{s('cough')}。中国大陆没有自主整机厂（弱）{s('lb')}。</p>
<p>本季出货：希捷 220 EB {s('stx_q')}，西部数据 248 EB {s('wdc_q')}。</p></div>
<div class="ex-bd" data-m="head" hidden><p><b>磁头：</b>只有希捷、西部数据自己做，外加日本 TDK 对外卖（弱）{s('lb')}。一块近线盘约 20 个磁头（弱）{s('lb')}。纪要称 TDK 供希捷的磁头从每季 600 万颗升到 1,000 万颗，磁头价格还有 5–10% 上调空间（弱）{s('jpm')}。</p>
<p>HAMR 磁头上的激光器，索尼约占希捷用量的 60%（弱）{s('jpm')}。</p></div>
<div class="ex-bd" data-m="media" hidden><p><b>盘片（介质）：</b>Resonac 是唯一对外卖介质的厂，产能从每年 1.6 亿片扩到 2.3 亿片，并和客户调了价 {s('reso')}。整机厂也自己做一部分。</p></div>
<div class="ex-bd" data-m="sub" hidden><p><b>玻璃基板：</b>HOYA 自称是唯一的硬盘玻璃基板厂；近线盘约 40% 用玻璃，HAMR 必须用玻璃 {s('hoya')}。纪要称 HOYA 给西部数据的玻璃 2027 年小量、2028 年放量（弱）{s('jpm')}。</p></div>
<div class="ex-bd" data-m="motor" hidden><p><b>主轴电机：</b>尼得科（Nidec）占 70% 以上 {s('nidec')}。</p></div>
<div class="ex-bd" data-m="mag" hidden><p><b>音圈电机磁钢：</b>用钕铁硼永磁。A 股宁波韵升为 VCM 供应磁材，份额：待补。详见 <a href="hdd.html">HDD 链库页</a> {s('x_hdd')}。</p></div>
<p>我们推断：定价权最强的是整机厂（三家、长约、价格已锁到 2027）和独家零件（玻璃基板、对外介质、主轴电机）。这是推断，不是判断，以链库页为准。</p>'''),

dict(id='watch', scene='watch', t='接下来盯什么？', hint='三个信号',
     parts=['p_stx', 'p_wdc'], body=f'''
<ol class="ex-keys">
<li><b>HAMR 爬坡</b>：希捷说 2026 年底 HAMR 约占近线出货 EB 一半 {s('stx_t')}；西部数据 HAMR 能不能按 2027 年上半年量产 {s('wdc_t')}。</li>
<li><b>价格和交期</b>：每 TB 价格还涨不涨 {s('wdc_t')}；交期是否从约 50 周回落 {s('tf_lt')}。</li>
<li><b>SSD 替代</b>：HDD 和 SSD 每 GB 的价差会不会缩小（弱）{s('jpm')}。差距越小，冷数据转向 SSD 越多。</li>
</ol>
<p>下季指引：希捷营收约 48 亿美元 {s('stx_q')}；西部数据 50–52 亿美元 {s('wdc_q')}。</p>
<p class="note">以上只是观察清单，不构成投资建议。</p>'''),

dict(id='quiz', scene='who', t='小测验：五个问题', hint='点问题看答案',
     parts=['m_drive', 'm_head', 'm_media', 'm_sub', 'm_motor', 'm_mag'], w='quiz', body='''
<p>不看上面，试着回答：</p>
<div class="ex-w" data-w="quiz"></div>'''),
]

QUIZ = [
    ('磁头会碰到盘面吗？', '不会。它在盘面上方“飞”，只隔几埃 ' + s('moz3') + '。碰上就是“划盘”，数据会坏。'),
    ('SMR 为什么能多存？代价是什么？', '磁道像瓦片一样叠着写，省掉了缝；代价是改一处要重写一整区，随机写慢 ' + s('smr') + '。'),
    ('为什么要充氦气？', '氦气密度约为空气的 1/7，乱流小；盘片能更薄更密，最多从 6 张变 10 张 ' + s('he') + '。'),
    ('HAMR 的激光是干什么的？', '写的瞬间把一小点盘面加热到约 430°C 以上，让很“硬”的磁粒暂时变软、写得动；冷下来就稳住 ' + s('moz3') + '。'),
    ('AI 时代为什么不全用 SSD？', '冷数据按每 TB 算钱，纪要称 2026 年 SSD 每 GB 约贵 15 倍（弱）' + s('jpm') + '；超大规模云厂超过 90% 的数据放 HDD ' + s('stxb') + '。'),
]

SOURCES = [(i + 1, _ALL[k][0], _ALL[k][1]) for i, k in enumerate(_ORDER)]
