"""万物原理图 · HBM 是怎么工作的 —— 页面规格（文字、代际数据、来源、读后五问）。
图形与模型在 explain/hbm.js；通用引擎在 explain/engine.js；页面由 explain/build.py 生成 explain-hbm.html。
规则：每个数字带来源编号 {s:N}；自己算的标 {calc}（推算），示意数字标 {est}（估/示意）。
"""

META = dict(
    id='hbm', file='explain-hbm.html', js='explain/hbm.js',
    title='HBM 是怎么工作的', short='HBM 高带宽内存',
    kicker='万物原理图 · 01', ver='v0.1', date='2026-10-21',
    dek='一步一步把一颗 HBM 拆开再装回去：为什么 AI 缺的是“带宽”，一颗 DRAM 怎么存 1 位，几千个竖孔怎么把 12 层芯片连成一摞，'
        '它怎么贴到 GPU 旁边，每一代升级到底升了什么、又卡在哪。',
    card='从“内存墙”讲起，逐层搭出一颗 HBM：DRAM 单元 → TSV 堆叠 → 底座 die → 三种键合 → 中介层 → 带宽算术 → 良率连乘；代际滑块从 HBM2E 拉到 HBM4E。',
    related=[('hbm.html', 'HBM 研究页（供需与判断）'), ('cowos.html', 'CoWoS 先进封装')],
)

# ---------- 代际数据：图、读数、表格都从这里来（Anatomy 的做法：图上每个数字来自同一个模型） ----------
# layers/dieGb：代表性量产产品；std：JEDEC 标准速率；prod：已公布的最快量产/出货速率。
GENS = [
    dict(name='HBM2E', year='2020', layers=8, dieGb=16, io=1024, ch=8, std=3.2, prod=3.6,
         src_cfg=4, src_std=3, src_prod=4, hlim=None, base='DRAM', bond='海力士 MR-MUF；同行 TC-NCF',
         prod_note='SK 海力士 2020 年量产：8 × 16Gb = 16GB，3.6 Gb/s，> 460 GB/s',
         unlock='一颗 16GB、约 460 GB/s，把 8 层 TSV 堆叠做成量产常规件 {s:4}',
         neck='通道只有 8 个、每根线 3.6 Gb/s：要更快只能把每根线提速、把通道拆细（→ HBM3） {s:1}'),
    dict(name='HBM3', year='2022', layers=12, dieGb=16, io=1024, ch=16, std=6.4, prod=6.4,
         src_cfg=6, src_std=1, src_prod=1, hlim=720, base='DRAM', bond='海力士 Advanced MR-MUF（12 层）；同行 TC-NCF',
         prod_note='JEDEC：6.4 Gb/s = 819 GB/s，首批用 16Gb 层；12 层 = 24GB',
         unlock='速率翻倍到 6.4 Gb/s、通道 8 → 16，单颗 819 GB/s；H100 用 80GB 做到 3.35 TB/s {s:1} {s:16}',
         neck='单颗容量：12 层要在原高度里塞进去，die 必须磨薄 40%，翘曲和散热成了难点（→ HBM3E 换 24Gb die） {s:6}'),
    dict(name='HBM3E', year='2024', layers=12, dieGb=24, io=1024, ch=16, std=9.2, prod=9.6,
         src_cfg=7, src_std=12, src_prod=7, hlim=720, base='DRAM', bond='海力士 Advanced MR-MUF；三星 TC-NCF（层间 7 µm）',
         prod_note='SK 海力士 12 层 36GB，9.6 Gb/s，约 1.2 TB/s；美光 8 层 24GB，> 9.2 Gb/s',
         unlock='单颗 36GB、约 1.2 TB/s；8 层 24GB 版本用在 H200 {s:7} {s:9}',
         neck='1024 根线已推到约 9.6 Gb/s，再提速很难；高度上限 720 µm 卡住层数（→ HBM4 把线数翻倍） {s:7} {s:13}'),
    dict(name='HBM4', year='2025–26', layers=12, dieGb=24, io=2048, ch=32, std=8.0, prod=11.7,
         src_cfg=11, src_std=2, src_prod=11, hlim=775, base='逻辑', bond='海力士 Advanced MR-MUF；三星 TC-NCF；混合键合未用',
         prod_note='JEDEC：2048 位 × 8 Gb/s = 2 TB/s；三星量产 11.7 Gb/s（最高 13，3.3 TB/s）；Rubin 用 8 颗 12 层 = 288GB、22 TB/s',
         unlock='线数 1024 → 2048、通道 16 → 32，单颗 2 TB/s 起；Rubin 一颗 GPU 288GB、22 TB/s {s:2} {s:17}',
         neck='底座 die 要交给代工厂做逻辑工艺 + GPU 侧 PHY 变大；16 层（48GB）还在客户认证，薄 die 和窄缝是主要难点 {s:12} {s:13}'),
    dict(name='HBM4E', year='2027', layers=12, dieGb=32, io=2048, ch=32, std=12.0, prod=16.0,
         src_cfg=14, src_std=12, src_prod=14, hlim=775, base='逻辑（可定制）', bond='MR-MUF / TC-NCF 延续；海力士称混合键合赶不上',
         prod_note='JEDEC 参考 12 Gb/s = 3 TB/s；三星 14 Gb/s 样品已出货、准备 16 Gb/s（4 TB/s），12 层 48GB',
         unlock='单颗 3–4 TB/s、48–64GB；底座可放客户自己的逻辑（定制 HBM） {s:12} {s:14}',
         neck='775 µm 高度 + 16 层散热；混合键合推迟到 HBM5（约 2029–30）；定制底座把买卖双方绑在一家代工厂 {s:13} {s:12}'),
]

# ---------- 步骤 ----------
# scene：hbm.js 里的场景；parts：本步可点的部件（顺序即标签顺序）；w：步内交互小部件
STEPS = [
dict(id='why', scene='wall', t='为什么 AI 需要 HBM：内存墙', hint='拖动年份 · 看算力和带宽差多少',
     parts=['cmp', 'bw', 'gap'], w='wall', body='''
<p><b>一句话：</b>GPU 算得越来越快，但从内存里“喂数据”的速度跟不上。过去约 20 年，服务器芯片的峰值算力大约每 2 年 ×3.0，内存带宽每 2 年只 ×1.6 {s:15}。差距每 2 年再放大近一倍，这就是“内存墙”。</p>
<div class="ex-w" data-w="wall"></div>
<p><b>容量和带宽不是一回事。</b>容量是能装多少（GB），决定模型放不放得下；带宽是每秒能搬多少（TB/s），决定算一步要等多久。大模型生成文字时，每出一个词，基本要把全部权重从内存里读一遍 {s:15}，所以出字速度主要看带宽。</p>
<p class="ex-ana"><b>打个比方：</b>容量像仓库有多大，带宽像装卸口每秒能进出多少货。<b>落到芯片上：</b>“装卸口”就是内存和 GPU 之间的数据线有多少根 × 每根线每秒传多少位。HBM 的办法是：线不靠拼命提速，而是一下拉 1024 根（HBM4 是 2048 根），并把内存贴到 GPU 旁边几毫米的地方。</p>
<p><b>算一下：</b>H100 有 80GB 内存、带宽 3.35 TB/s {s:16}，把整块内存读一遍约 80 ÷ 3,350 ≈ 24 毫秒 {calc}。SK 海力士举的例子：一颗 GPU 配 4 颗 12 层 HBM3E，每秒能把 Llama 3 70B 的 700 亿个参数读 35 遍 {s:7}。</p>'''),
dict(id='cell', scene='cell', t='最小单元：DRAM 存储单元与裸片', hint='点一个 bank 或存储单元',
     parts=['die', 'bank', 'cell', 'sa', 'wl'], body='''
<p><b>1 位数据 = 1 个晶体管 + 1 个电容。</b>电容像一个极小的水桶：桶里有电荷记作 1，没有记作 0；晶体管是桶口的阀门，由“字线”控制开关，打开后电荷流到“位线”上被读出。电容会慢慢漏电，所以 DRAM 要不停地“刷新”（重新充电），这就是 D（Dynamic，动态）的意思。</p>
<p><b>几十亿个单元排成阵列（bank）</b>，旁边配读出放大器和行、列译码电路，就是一颗 DRAM 裸片（die）。HBM 每层 die 的容量：HBM2E 16Gb {s:4}，HBM3E 24Gb（3GB）{s:7}，HBM4 24 或 32Gb {s:2}（8 Gb = 1 GB）。</p>
<p><b>关键：HBM 的存储 die 本身还是 DRAM 工艺</b>（海力士 HBM4 用 1b，三星用 1c）{s:10} {s:11}。HBM 的本事不在单元，而在后面几步：怎么叠、怎么连、怎么贴到 GPU 旁边。</p>'''),
dict(id='stack', scene='stack', t='叠起来：TSV、微凸点、减薄', hint='点“展开 / 压紧” · 点 TSV 或凸点',
     parts=['core', 'tsv', 'bump', 'thin'], w='apart', body='''
<p><b>一层不够就叠 8、12、16 层。</b>层与层怎么通电？在每颗硅片上打几千个竖直的细孔，灌满铜，叫<b>硅通孔（TSV）</b>：HBM2E 每颗 die 有 5,000 多个 {s:5}。上下两层的 TSV 用<b>微凸点</b>（极小的焊点）对准接通，信号、电源、地都走这些竖线，不再绕外面的长引线 {s:5}。</p>
<div class="ex-w" data-w="apart"></div>
<p><b>为什么要磨薄：</b>总高度有上限（第 7 步），层数越多每层就得越薄。12 层 HBM3E 的每颗 DRAM 比 8 层产品薄 40%，总厚度不变、容量多 50% {s:7}；16 层 HBM4 的核心 die 约 50 µm，比头发丝还细，层间缝隙也比 12 层少一半 {s:13}。越薄越容易翘、越难拿，这是堆叠的头号工艺难点。</p>'''),
dict(id='base', scene='base', t='最底下那一层：底座（逻辑）die', hint='拖代际滑块 · 看底座换工艺',
     parts=['basedie', 'phy', 'core'], body='''
<p><b>一摞的最底层不存数据</b>，叫底座 die（base / logic die）。它管对外的 1024 或 2048 根数据线的收发电路（PHY）、测试和供电分配，把上面各层的数据汇总后送给 GPU。</p>
<p><b>HBM3E 及以前</b>，底座由内存厂用 DRAM 工艺自己做，工作电压 1.1V {s:12}。<b>HBM4 线数翻倍</b>，收发电路更大更复杂，于是底座改用代工厂的逻辑工艺：台积电 12FFC / N5，电压降到 0.75–0.8V，能效最高约为 HBM3E 底座的 2 倍 {s:12}；三星用自家 4nm {s:11}；美光 HBM4 用自研 CMOS 底座、HBM4E 交给台积电 {s:12}。</p>
<p><b>HBM4E 起可以“定制底座”</b>：保留标准的存储层，把客户自己的逻辑放进底座（台积电 N3P 可做）{s:12}。内存开始从标准件变成半定制件。把滑块拉到 HBM4，底座会变成蓝色（逻辑工艺）。</p>'''),
dict(id='bond', scene='bond', t='层间怎么粘：TC-NCF vs MR-MUF vs 混合键合', hint='切换三种键合方式',
     parts=['film', 'mold', 'bump', 'pad', 'tsv'], w='bond', body='''
<div class="ex-w" data-w="bond"></div>
<div class="ex-bd" data-m="tc"><p><b>TC-NCF（热压 + 不导电薄膜）：</b>每叠一层，先铺一层薄膜，再加热加压把凸点焊上，一层一层来。三星 12 层 HBM3E 用改进版，把层间缝隙压到 7 µm，12 层做到和 8 层一样高 {s:8}。海力士称同行用的都是这条路线 {s:6}。</p></div>
<div class="ex-bd" data-m="mr"><p><b>MR-MUF（一次回流 + 灌模）：</b>先把所有层叠好，一次加热把全部凸点焊上，再灌进液态环氧模塑料把缝填满。SK 海力士 2019 年起用在 HBM2E，散热比 HBM2 好 36%，导热用的假凸点最多可加到 4 倍 {s:6}；12 层用 Advanced MR-MUF，HBM4 继续用 {s:6} {s:10}。</p></div>
<div class="ex-bd" data-m="hb"><p><b>混合键合（铜对铜直连）：</b>不要凸点，把两层的铜焊盘和氧化层磨到极平，直接贴合再加热，铜受热膨胀连成一体。20 层时核心 die 可以厚 24%、热阻降约 35%，焊点间距从 MR-MUF 的约 30 µm 降到 18 µm 以下 {s:13}。难在 16–20 层每一面都要极平极干净。海力士表示 HBM4E 用不上、最早 HBM5；Counterpoint 预计 2029–30 年才进入量产 {s:13}。</p></div>
<p class="ex-ana"><b>为什么值得关心：</b>键合方式决定能叠多高、热能不能散出去、良率多少，也决定买谁的设备（热压机、回流炉、混合键合机）。</p>'''),
dict(id='pkg', scene='pkg', t='贴到 GPU 旁边：硅中介层与 2.5D 封装', hint='点 GPU、HBM、中介层',
     parts=['gpu', 'stackp', 'interp', 'subs'], body='''
<p><b>HBM 不插在主板上</b>，而是和 GPU 并排放在一块<b>硅中介层</b>（interposer）上。中介层里刻着几千根极细的线，把每颗 HBM 的底座直接连到 GPU，距离只有几毫米；中介层再放到封装基板上。两颗芯片“并排 + 一层硅桥”，叫 2.5D 封装，台积电的版本就是 <a href="cowos.html">CoWoS</a>。</p>
<p><b>为什么非这样不可：</b>每颗 HBM 有 1024 或 2048 根数据线，普通电路板上根本走不了这么密。图里是 8 颗：Rubin GPU 配 8 颗 12 层 HBM4 {s:18}，合计 288GB、22 TB/s {s:17}。</p>
<p><b>所以 HBM 能出多少货，不只看内存厂</b>，还要看 CoWoS 中介层和封装基板的产能 → 见 <a href="cowos.html">CoWoS 页</a>；中介层、硅桥、载板一层层怎么搭，见 <a href="explain-cowos.html">CoWoS 原理图</a>。</p>'''),
dict(id='io', scene='io', t='数据线：1024 位到 2048 位，带宽怎么算', hint='拖速率 · 切 1024 / 2048 位',
     parts=['strand', 'phy', 'gpu'], w='calc', body='''
<p><b>公式只有一行：带宽 = 线数 × 每根线每秒传的位数 ÷ 8</b>（8 位 = 1 字节）。HBM3：1024 × 6.4 ÷ 8 = 819 GB/s {s:1}；HBM4：2048 × 8 ÷ 8 = 2,048 GB/s ≈ 2 TB/s {s:2}。</p>
<div class="ex-w" data-w="calc"></div>
<p><b>线分成独立“通道”：</b>HBM2 8 个，HBM3 16 个，HBM4 32 个，HBM3 / HBM4 每个通道 64 位 {s:1} {s:2}。图里每一束线就是一个通道，滑块拉到 HBM4，线束会翻倍。</p>
<p><b>为什么加线而不是提速：</b>每根线越快，信号越难做干净、功耗越高。HBM3E 时 1024 根线已推到约 9.6 Gb/s {s:7}，再往上很难，HBM4 就把线数翻倍 {s:2} {s:10}。代价是 GPU 那一侧的收发电路（PHY）面积从约 11 mm² 增到约 15 mm² {s:12}，中介层上的走线也更密。</p>'''),
dict(id='hard', scene='hard', t='为什么难：高度、热、良率连乘', hint='拖每层良率 · 看整摞良率',
     parts=['ruler', 'heat', 'core', 'basedie'], w='yield', body='''
<p><b>① 高度：</b>GPU 封装要盖散热板，HBM 和 GPU 得一样高；逻辑晶圆厚 775 µm，所以 HBM 总高到 HBM3E 都限在 720 µm，HBM4 放宽到 775 µm {s:13}。层越多，每层越薄、缝越窄。</p>
<p><b>② 热：</b>热量要穿过更多层才出得去；die 越薄，导热差的氧化层占比越大；每根线从 1 Gb/s 提到 8 Gb/s，同样面积里功耗更集中。海力士给出的热负担在这几代里升了约 2.2 倍 {s:13}。</p>
<p><b>③ 良率连乘：</b>一摞里只要有一层或一个焊点坏，整摞就可能报废——已经焊死，拆不下来。假设每层（含键合）的良率是 p，n 层整摞的良率约为 p 的 n 次方。拖动看看：</p>
<div class="ex-w" data-w="yield"></div>
<p class="ex-ana">所以厂商要先把每颗 die 测好（“已知良品 die”）再叠，也解释了为什么 16 层比 12 层难得多、为什么同一年各家 HBM 的良率差距会直接变成供给差距。</p>'''),
dict(id='ladder', scene='ladder', t='代际阶梯：每一代升了什么、卡在哪', hint='拖代际滑块 · 对照下表',
     parts=['core', 'basedie', 'strand'], w='ladder', body='''
<p>把上面几步合起来看：每一代都是在<b>层数、单层容量、线数、每根线速率、底座工艺、键合方式</b>这几个旋钮里拧一两个，然后撞上下一个瓶颈。</p>
<div class="ex-w" data-w="ladder"></div>
<p class="note">“标准”= JEDEC 规定的速率；“最快量产”= 厂商已公布的最快出货速率；单颗带宽按“线数 × 速率 ÷ 8”现算 {calc}。HBM3E 没有单独的 JEDEC 标准号，9.2 Gb/s 取自 EE Times 汇总表 {s:12}。</p>'''),
dict(id='next', scene='next', t='下一次升级的关键（接回 HBM 研究页）', hint='拖代际滑块 · 红色是这一代的瓶颈',
     parts=['basedie', 'interp', 'core', 'gpu'], body='''
<ol class="ex-keys">
<li><b>堆叠良率与 16 层：</b>16 层 HBM4（48GB）还在客户认证，薄 die（约 50 µm）和减半的缝是主要难点 {s:13}。这直接决定 <a href="hbm.html#logic">HBM 研究页</a>的第一个观察项“2026 年实际产量能否 ≥ 40 亿 GB”；中国账本里卡住国产 HBM 的也正是“分给 HBM 的 DRAM 晶圆和堆叠良率”。</li>
<li><b>晶圆从哪来：</b>层数、单层容量往上加，每 GB 都要吃 DRAM 晶圆。研究页的核心判断是“2027 年涨价靠 DDR5 抢晶圆（机会成本），不是 HBM 缺货”，对应观察项“DDR5 和 HBM 谁先松”→ <a href="hbm.html#a2">论据 2</a>。</li>
<li><b>底座交给代工 + 封装产能：</b>HBM4 起底座用台积电等代工厂的逻辑工艺 {s:12}，HBM 能出多少要和代工、CoWoS 产能一起看；研究页的结论是 2027 年最紧的一环换成封装载板 → <a href="cowos.html">CoWoS 页</a>。</li>
<li><b>混合键合的时点：</b>海力士说 HBM4E 用不上，最早 HBM5，Counterpoint 预计约 2029–30 年；海力士已下了第一套量产用混合键合设备订单（约 200 亿韩元）{s:13}。设备订单是比产品发布更早的信号。</li>
<li><b>定制底座：</b>HBM4E 可做定制底座，美光说定制版毛利更高 {s:12}。如果定制占比上来，HBM 会更像长约定制件、周期性可能变弱——这是推断 {est}，研究页“周期顶部看 2027 年下半年”的判断暂不因此改动。</li>
</ol>'''),
dict(id='quiz', scene='pkg', t='读完你应该能回答这 5 个问题', hint='点问题看答案',
     parts=['gpu', 'stackp', 'interp'], w='quiz', body='''<div class="ex-w" data-w="quiz"></div>'''),
]

QUIZ = [
    ('为什么 AI 芯片更缺“带宽”，而不只是“容量”？',
     '容量决定模型放不放得下，带宽决定每一步要等多久。生成每个词基本要把全部权重读一遍，所以出字速度看带宽；而算力每 2 年 ×3.0、带宽只 ×1.6，差距越拉越大（内存墙）。'),
    ('一颗 HBM 的带宽怎么算？HBM3E → HBM4 带宽翻倍主要靠什么？',
     '带宽 = 线数 × 每根线速率 ÷ 8。HBM3E 是 1024 位 × 约 9.6 Gb/s ≈ 1.2 TB/s；HBM4 主要靠线数翻倍到 2048 位（通道 16 → 32），标准速率 8 Gb/s 就有 2 TB/s，量产 11.7 Gb/s 约 3 TB/s。'),
    ('TSV、微凸点、MR-MUF / TC-NCF / 混合键合各解决什么问题？',
     'TSV 是穿过硅片的竖直铜孔，让上下层直接通电；微凸点把相邻两层的 TSV 焊在一起；TC-NCF 一层一层热压 + 薄膜，MR-MUF 一次回流再灌模（散热更好），混合键合去掉凸点、铜对铜直连，能叠更高、更薄、更凉，但工艺最难，最早 HBM5。'),
    ('为什么 HBM4 的底座 die 要交给台积电等代工厂？这对产业链意味着什么？',
     '线数翻倍后收发电路更大更复杂，逻辑工艺电压更低（0.75–0.8V vs 1.1V）、能效更好；结果是 HBM 供给要和代工、CoWoS 产能一起看，底座还能定制，内存从标准件走向半定制件，也让买卖双方更依赖同一家代工厂。'),
    ('为什么堆得越高越难？775 µm 和良率连乘分别卡在哪？',
     '总高要和 GPU 一样（≤ 775 µm），层越多每层越薄、缝越窄，易翘、难散热；整摞良率约是每层良率的 n 次方，比如每层 99% 时 16 层只剩约 85%（示意），坏一层整摞报废。'),
]

SOURCES = [
    (1, 'JEDEC：JESD238 HBM3 标准发布（2022-01-27）', 'https://www.jedec.org/news/pressreleases/jedec-publishes-hbm3-update-high-bandwidth-memory-hbm-standard'),
    (2, 'JEDEC：JESD270-4 HBM4 标准发布（2025-04-16）', 'https://www.jedec.org/news/pressreleases/jedec%C2%AE-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard-advancing'),
    (3, "Tom's Hardware：HBM3 规格 819 GB/s（含 HBM2/2E 对比，2022-01-28）", 'https://www.tomshardware.com/news/hbm3-spec-reaches-819-gbps-of-bandwidth-and-64gb-of-capacity'),
    (4, 'SK 海力士：HBM2E 量产（16GB、3.6 Gb/s、460 GB/s，2020-07）', 'https://news.skhynix.com/en/sk-hynix-starts-mass-production-of-high-speed-dram-hbm2e/'),
    (5, 'SK 海力士：HBM2E 开启超高速内存时代（TSV 超过 5,000 个）', 'https://news.skhynix.com/en/hbm2e-opens-the-era-of-ultra-speed-memory-semiconductors/'),
    (6, 'SK 海力士：MR-MUF 如何解决 HBM 散热（2024-07-30）', 'https://news.skhynix.com/en/rulebreaker-revolutions-mr-muf-unlocks-hbm-heat-control/'),
    (7, 'SK 海力士：12 层 HBM3E 量产（36GB、9.6 Gb/s、die 薄 40%，2024-09-26）', 'https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/'),
    (8, '三星：36GB HBM3E 12H（Advanced TC NCF、层间 7 µm，2024-02-27）', 'https://news.samsung.com/global/samsung-develops-industry-first-36gb-hbm3e-12h-dram'),
    (9, '美光：HBM3E 量产（24GB 8 层、> 9.2 Gb/s、> 1.2 TB/s，2024-02-26）', 'https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx'),
    (10, 'SK 海力士：HBM4 完成开发（2,048 I/O、> 10 Gb/s、Advanced MR-MUF、1b，2025-09-12）', 'https://news.skhynix.com/en/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/'),
    (11, '三星：HBM4 量产出货（11.7 Gb/s、最高 13 Gb/s、3.3 TB/s、4nm 底座、1c，2026-02-12）', 'https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing'),
    (12, 'EE Times：Beyond Bandwidth—定制内存（HBM4E 12 GT/s、台积电底座、PHY 面积，2026-03-10）', 'https://www.eetimes.com/beyond-bandwidth-the-industry-is-striving-for-custom-memory-part-1/'),
    (13, "Tom's Hardware：Hot Chips 2026 SK 海力士（775 µm、16 层、混合键合推到 HBM5，2026-08-24）", 'https://www.tomshardware.com/tech-industry/semiconductors/sk-hynix-says-hybrid-bonding-wont-be-ready-for-hbm4e-as-ai-memory-runs-into-a-775-micron-ceiling'),
    (14, 'TechPowerUp：三星 HBM4E 16 Gb/s（14 Gb/s 样品、12 层 48GB、SF4 底座，2026-08-24）', 'https://www.techpowerup.com/351859/samsung-confirms-hbm4e-memory-running-at-16-gbps-per-pin'),
    (15, 'Gholami 等：AI and Memory Wall（IEEE Micro 2024；算力 3.0×/2 年 vs 带宽 1.6×/2 年）', 'https://arxiv.org/abs/2403.14123'),
    (16, 'NVIDIA：H100 产品页（80GB、3.35 TB/s）', 'https://www.nvidia.com/en-us/data-center/h100/'),
    (17, 'NVIDIA：HGX 平台页（Rubin GPU 288GB HBM4、22 TB/s）', 'https://www.nvidia.com/en-us/data-center/hgx/'),
    (18, 'Korea Herald：SK 海力士完成 HBM4（Rubin 用 8 颗 12 层 HBM4，2025-09-12）', 'https://www.koreaherald.com/article/10574552'),
]
