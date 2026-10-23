"""PCB 技术路线图 + 格局图（底图层）。2026-10-23 起内容并入 pcb.html（第 2、3 章：原理图 / 路线图 / 格局图），由 pcb/page.py import 本文件的 ROAD / AI / MAP / GAPS；\npcb-map.html 只保留为跳转页（旧锚点 #road #ai #map #check #gap #sN 映射到 pcb.html 对应位置）。\n原说明：
每个数字都挂来源与日期；没有可靠来源的写“数据缺口”，不估。来源：复用 pcb/src.py（2026-10-20 核对）+ 本页新增 NEW（2026-10-23 核对）。
本页不新增判断/预测，只用 G/P 编号链接到 ledger.html，不改总账任何判断与概率。由 ./build.sh 调用。"""
import os, sys
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R0, 'pcb'))
from src import SRC, ID

# NEW 已并入 pcb/src.py（2026-10-23），编号接在原 80 条之后
NEWK = {'pr25t','iekccl','cnasub','ajiabf','yole','dzar','m6','m7','m8','tcf','msap','cowop'}

USE = ['prq2', 'pr25t', 'prtop25', 'ms', 'tpu', 'kyber', 'hf', 'm6', 'm7', 'm8', 'emcir', 'udn2', 'doosan', 'tcf', 'mitjan', 'mitqa', 'mitsuiq1', 'ctcuf', 'ctcud', 'uacu', 'bfc', 'tgh1', 'hh', 'tft', 'tfn', 'cq', 'gsq', 'jm', 'sq', 'dc',
       'iekccl', 'sy', 'hd', 'sn', 'cnasub', 'ajiabf', 'yole', 'mdjabf', 'cnyabf', 'ctsub', 'uad', 'dzar', 'msap', 'cowop']


def S(*k):   # 合并进 pcb.html 后统一用 pcb/src.py 的编号（#srcN）
    return '<span class="tag t-src">' + ' '.join(f'<a href="#src{ID[x]}">源{ID[x]}</a>' for x in k) + '</span>'


E = '<span class="tag t-est">推算</span>'
GAP = '<span class="pill gap">数据缺口</span>'
L = lambda i: f'<a class="lid" href="ledger.html#{i}">{i}</a>'

# 技术路线图：(代号, 标题, 一句话, 改了什么, 为什么, 卡在哪（材料/设备/工艺）, 谁领先, 账本)
ROAD = [
 ('①', '普通多层板', '几层铜 + 几层绝缘料压在一起，机械钻通孔把层连起来。',
  '基本做法：减成法（先整面铜、再蚀刻掉不要的）+ 机械钻通孔 + 电镀。',
  '最便宜、最成熟；服务器以外的消费、汽车、工控大多还是它。',
  '成本推动型：铜、玻纤布、CCL 涨价直接挤毛利（普通板厂毛利率下滑，崇达 7.67%）' + S('jm') + '。',
  '分散：前 10 大板厂营收合计约占前 100 大的 37%' + E + S('pr25t') + '（含非 PCB 收入）。', [L('G26')]),
 ('②', 'HDI（高密度互连）', '用激光打很小的盲孔，一层一层“积”上去，同样面积走更多线。',
  '激光盲孔 + 电镀填孔 + 逐层压合（1+N+1 → 更多阶）。',
  '手机先要“小”，现在 AI 计算板也要“密”：Rubin 计算板是 26 层 HDI' + S('ms') + '；2026 年 HDI 预计 +39.8%' + S('prq2') + '。',
  '激光钻孔、填孔电镀、多次压合对位，阶数越高良率越难。',
  '分环节份额 ' + GAP + '（Prismark 有，但未公开）。', []),
 ('③', '任意层 / mSAP（类载板 SLP）', '线细到减成法蚀刻不出来，改成“先薄铜、再按图形长铜”。',
  '线宽/线距从 30/30 μm 走向 25/25、20/20 μm；mSAP 线形接近矩形，阻抗更准' + S('msap') + '。',
  '手机主板塞更多芯片；这是 PCB 往载板工艺靠拢的第一步。',
  '曝光（DI）、AOI 检测、薄铜与图形电镀良率' + S('msap') + '。',
  '厂商份额 ' + GAP + '。', []),
 ('④', 'IC 载板（BT / ABF）', '芯片和 PCB 之间的“转接板”，线更细，是封装的一部分。',
  'BT 树脂载板（存储、手机芯片）→ ABF 积层膜载板（CPU/GPU 的 FC-BGA）；ABF 1999 年上市' + S('ajiabf') + '。',
  'AI 芯片面积和 I/O 越来越大，载板层数、面积一起涨；先进载板 2024 年 142 亿美元 → 2030 年 310 亿美元' + S('yole') + '。',
  'ABF 膜几乎一家（味之素自述约 95%）' + S('ajiabf') + '；ABF 交期 3–4 个月 → 逾 12 个月、压膜设备交期 12–18 个月' + S('mdjabf') + '；新厂要到 2029 年' + S('ctsub') + '。',
  '欣兴 16%、SEMCO 9.9%、Ibiden 9.3%、AT&S 9.1%、南电 8.7%（TPCA，2025-04 发布）' + S('cnasub') + '。', [L('G27'), L('G11'), L('G19')]),
]
AI = [
 ('Ⓐ', '高层数板', '层数越多 = 越难压、越难钻、良率连乘。',
  'Rubin：计算板 26 层 HDI、交换板 24 → 32 层、新增 44 层中板' + S('ms') + '；谷歌 TPU V7 36 层 / V7P 44 层（纪要，弱）' + S('tpu') + '。',
  'GPU 互连和高速信号通道更多；VR200 NVL72 机柜 PCB 约 11.67 万美元 vs GB300 约 3.51 万' + S('ms') + '；2026 年 18 层以上 +86.7%' + S('prq2') + '。',
  '钻孔：M9 主钻针寿命只有 100–200 孔（M8 400–500 孔）' + S('uad') + '；压合对位；进口开槽机交期 1–2 年' + S('uad') + '。',
  'AI 板龙头 2025 年增长超 50%，多数板厂不到 10%' + S('prtop25') + '；沪电 PCB 毛利率 40.52%' + S('hd') + '。', [L('G21'), L('G26'), L('P046')]),
 ('Ⓑ', '覆铜板等级 M6 → M7 → M8 → M9', '“M 几”是行业对低损耗等级的叫法（源自松下 Megtron），数字越大信号损耗越低。',
  '以松下实测典型值为例：M6 Df 0.0037 @13GHz' + S('m6') + ' → M7 0.0023 @14GHz' + S('m7') + ' → M8 0.0012 @14GHz' + S('m8') + '。M9 是下一档，公开厂商规格 ' + GAP + '。',
  '速率翻倍时，介质损耗（Df）和铜面粗糙度成为主要损耗；换料比加层更省事。',
  '树脂（PPO、碳氢）' + S('sq', 'dc') + '、低 Dk 布和 HVLP 铜箔三样要一起升级，客户认证周期长。',
  '台光电：高速无卤 CCL 2025 年份额 38.6%' + S('emcir') + '，M7 以上占其出货 60–65%' + S('udn2') + '；Rubin 中板 M9：台光电约 70%、斗山约 30%（纪要，弱）' + S('doosan') + '。', [L('G22')]),
 ('Ⓒ', 'HVLP 铜箔 1 → 5', '铜箔贴树脂那一面越平，高频信号越不“绕路”，损耗越低。',
  'B 面粗糙度 Rz：HVLP 1.5 → HVLP2 1.0 → HVLP3 0.6 → HVLP4 0.5 → HVLP5 0.4 μm（三井代表值，非 IPC 统一等级）' + S('tcf') + '。',
  '高频电流贴着表面走（趋肤效应），表面越粗损耗越大；材料等级越高，对铜面越平的要求越高（具体搭配看客户规格）。',
  '不是没铜，是“又平又粘得牢”难做：良率 + 客户认证；HVLP1/2 转 3/4 有效产能约减半' + S('ctcud') + '；三井马来西亚厂认证延迟，下调销量预测 840 → 730 吨/月' + S('mitqa') + '。',
  '三井约占 HVLP2+ 60%、HVLP5 80%' + S('mitjan') + '；德福、铜冠在追，铜冠出货以 HVLP2 为主' + S('tgh1') + '。', [L('G27'), L('P044'), L('P045')]),
 ('Ⓓ', '低 Dk 玻纤布：一代 → 二代 → Q 布', '板子里的“布”也是介质，玻璃成分决定损耗和热胀冷缩。',
  '一代低 Dk 布 → 二代低 Dk 布 → 石英布（Q 布）；另有低 CTE 布（T-glass）用于载板，管翘曲。二代布约 17.9–22.4 美元/米、Q 布 38.7–44.7 美元/米' + S('cq') + '。',
  'M8/M9 等级只换树脂不够，布也要低损耗；载板越大越怕翘。',
  '玻纤纱 + 织布产能，产线建设 18–24 个月' + S('jm') + '；Q 布极硬，钻针损耗是二代布 2.6 倍' + S('gsq') + '。',
  '2024 年低 Dk 布：日东纺 55%、旭化成 31%、台玻 11%；低 CTE 布：日东纺 85%、Unitika 14%' + S('hh') + '；T-glass 日东纺约九成' + S('tft') + '。', [L('G27'), L('G28'), L('P042')]),
 ('Ⓔ', '正交背板（Kyber）', '用一块超厚的板代替机柜里的铜缆，把计算板和交换板垂直插在一起。',
  '78 层（3 块 26 层压合）、约 1 m²；原计划 M9 + Q 布' + S('kyber', 'hf') + '。',
  '机柜里的铜缆太多太长，用板子走线更短更好装。',
  '超大尺寸压合良率、钻孔；据 SemiAnalysis 报道推迟到 2028 年（英伟达称路线图不变）' + S('kyber') + '。',
  '谁量产 ' + GAP + '（还没量产）。', [L('P037'), L('P047')]),
 ('Ⓕ', 'CoWoP（芯片直接贴 PCB）', '设想：省掉 ABF 载板，把“芯片 + 中介层”直接放到 PCB 上。',
  'PCB 要承担载板的细线，线宽线距要从 20/35 μm 缩到 10/10 μm 以下' + S('cowop') + '。',
  '想绕开最紧的 ABF 载板、降成本；但成本只是挪到更难做的 PCB 和组装上' + S('cowop') + '。',
  'mSAP/SAP 细线能力；板厂普遍存疑，2025-07 时仍属“很早期”' + S('cowop') + '。',
  '谁领先 ' + GAP + '。', [L('G27')]),
]

# 格局图：(环节, 集中度, 头部与份额, 定价权, 利润池, 账本)
MAP = [
 ('铜箔（HVLP 高端）', '高（高端一家独大）',
  '三井约占 HVLP2+ 60%、HVLP5 80%（2026-01）' + S('mitjan') + '；全品类份额 ' + GAP,
  '有，但克制：三井 2025-10 与 2026-07 两次“选择性”提价' + S('mitqa') + '；金居高阶加工费累计约 +5–10%' + S('ctcuf') + '；HVLP4 加工费 17–20 万元/吨' + S('uacu') + '（另一份纪要 22–25 万，弱' + S('bfc') + '）',
  '集中在高端：三井铜箔事业 ROIC 52%' + S('mitsuiq1') + '；以 HVLP2 为主的铜冠 PCB 铜箔毛利率 11.60%' + S('tgh1'), [L('G27'), L('P044')]),
 ('玻纤布 / 树脂', '很高（日系寡头）',
  '低 Dk 布 日东纺 55% / 旭化成 31% / 台玻 11%；低 CTE 布 日东纺 85% / Unitika 14%（2024）' + S('hh') + '；树脂份额 ' + GAP,
  '最强：宏和电子布均价 4.81 → 11.91 元/米（+147.6%）' + S('jm') + '；日东纺称不再提价、优先扩产' + S('tfn'),
  '日东纺电子材料营业利益 280 亿日元（+44%），营收 778 亿日元' + S('tfn') + '，营业利益率约 36%' + E, [L('G27'), L('G28'), L('P042')]),
 ('覆铜板 CCL', '中（前 3 约四成）',
  'Prismark 2025（扣除大宗标准型、含 PP，市场 186.76 亿美元）：台光电 16.2%、生益 13.2%、建滔 12.4%' + S('iekccl') + '，前 3 合计 41.8%' + E + '；高速无卤细分台光电 38.6%' + S('emcir'),
  '强：上半年陆资 CCL 涨约 15%，缺货料号 30–40%' + S('udn2') + '；建滔年内第 7 次涨价函' + S('jm'),
  '台光电毛利率 33.9%（2Q26）' + S('emcir') + '；生益 CCL 毛利率 29.16%（1H26）' + S('sy'), [L('G23'), L('G24')]),
 ('PCB 板厂', '低（分散）',
  '2025 营收：臻鼎 58.7 亿美元、欣兴 42.3、东山 35.7、深南 33.0、TTM 29.1、沪电 27.6、胜宏 26.9' + S('pr25t') + '；前 10 合计约占前 100 大营收 37%' + E + '；中国大陆企业约 36% 产值、台湾约 30%' + S('pr25t'),
  '两极：AI 板量价齐升，普通板被成本挤压' + S('prtop25', 'jm'),
  '前 40 大净利率 8.3%（2025）' + S('pr25t') + '；沪电 PCB 毛利率 40.52% vs 崇达 7.67%' + S('hd', 'jm'), [L('G23'), L('G26')]),
 ('IC 载板 + ABF 膜', '高（前 5 过半；ABF 膜一家）',
  '欣兴 16%、SEMCO 9.9%、Ibiden 9.3%、AT&S 9.1%、南电 8.7%' + S('cnasub') + '；ABF 膜味之素约 95%（自述）' + S('ajiabf'),
  '强：载板均价每季涨逾 7%' + S('ctsub') + '，ABF 单季 +10–15%' + S('mdjabf') + '；欣兴 ABF 稼动率逾 90%' + S('cnyabf'),
  '深南封装基板毛利率 31.35%（+16.2pp，1H26）' + S('sn') + '；味之素 ABF 利润 ' + GAP, [L('G27'), L('G11'), L('G19')]),
 ('钻孔 / 电镀 / 压合设备与耗材', '中高（钻机、钻针集中）',
  '机械钻孔机：大族数控约 50%（公司按 Prismark + 自有交付测算，2025）' + S('dzar') + '；钻针：鼎泰 29.2%、金洲 21.1%、佑能 10.4%、尖点 9.9%（2025）' + S('uad') + '，前 4 合计 70.6%' + E + '；电镀、曝光、压合设备份额 ' + GAP,
  '交期就是定价权：压膜设备 12–18 个月' + S('mdjabf') + '，进口开槽机 1–2 年' + S('uad') + '；M9 让钻针变“消耗品”' + S('uad'),
  '设备商利润率 ' + GAP + '（本页未核）', [L('G27'), L('G28')]),
 ('终端客户', '很高（少数买家）',
  '英伟达、微软、谷歌、亚马逊订走多数高端 T-glass 产能' + S('tfn') + '；各家采购份额 ' + GAP,
  '买家定规格和认证名单：材料等级（M8/M9、HVLP4、二代布）由客户平台决定' + S('ms', 'doosan'),
  '单机柜 PCB 价值：VR200 NVL72 约 11.67 万美元 vs GB300 约 3.51 万' + S('ms'), [L('G25')]),
]

CHECK = [
 ('HVLP4 到底缺不缺？', '过去 12 个月，你们实际买到的 HVLP3/4 加工费涨了多少？交期有没有超过 3 个月、有没有被限量（配额）？同期二代布、CCL 涨了多少？',
  '你说没看到大涨价——如果 HVLP4 只涨个位数、而布和 CCL 涨两位数，说明铜箔是“认证/良率瓶颈”，不是“缺货”；这正是 ' + L('G27') + ' / ' + L('P044') + ' 在赌的。若加工费单季 ≥ +15% 或出现配额，G27 要改。'),
 ('二代布 / PP 怎么拿货？', '你们的二代低 Dk 布或 PP 现在是按月排单还是能锁量？交期多久？有没有客户同意用一代布 + 更好的树脂替代？',
  '布是我们认为最紧的材料之一（' + L('G27') + '）；2027 年下半年会不会先松（' + L('G28') + ' / ' + L('P042') + '），你最先看得到。'),
 ('22–30 层板开始比价了吗？', '客户对 22–30 层 AI 板有没有开始压价或找第二家？M9 板实际钻针寿命、良率大概多少？',
  '对应 ' + L('P046') + '（22–30 层先降价、40 层以上不降）和钻孔瓶颈；公开数据只有“M9 主针 100–200 孔”这一个来源' + S('uad') + '。'),
]

GAPS = [
 'HDI、任意层 / mSAP、高层数板的厂商份额（Prismark 分技术排名未公开）',
 'M9 等级的公开厂商 Df/Dk 规格（目前只有 M6–M8 的松下数据）',
 '电子级树脂（PPO、碳氢、BMI）全球份额',
 '电镀、曝光（DI）、压合设备份额；设备商利润率',
 'ABF 膜业务的利润（味之素不单独披露这一块）',
 '终端客户（英伟达 / 云厂商）的 PCB 采购份额',
 '载板份额是 TPCA 2025-04 发布的口径（年份应为 2024），2025 年新份额待补',
 '板厂集中度只能用“前 10 / 前 100 营收”近似，营收含组装和非 PCB 业务',
]


def card(r, ai=False):
    n, t, one, what, why, neck, lead, led = r
    return (f'<details class="card rd"{" open" if n in ("④", "Ⓒ") else ""}><summary><span class="rn">{n}</span><b>{t}</b><span class="one">{one}</span></summary>'
            f'<dl><dt>改了什么</dt><dd>{what}</dd><dt>为什么</dt><dd>{why}</dd><dt>卡在哪</dt><dd>{neck}</dd><dt>谁领先</dt><dd>{lead}</dd>'
            + (f'<dt>账本</dt><dd>{" ".join(led)}</dd>' if led else '') + '</dl></details>')


CSS = """<style>
.rd>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:34px 1fr;gap:2px 8px;align-items:start;min-height:44px}
.rd>summary::-webkit-details-marker{display:none}.rd .rn{grid-row:span 2;font-size:22px;color:var(--acc);line-height:1.2}
.rd .one{font-size:14px;color:var(--mut);grid-column:2}.rd dl{margin:10px 0 0 42px}.rd dt{font-size:12px;color:var(--mut);margin-top:8px;font-weight:600}.rd dd{margin:2px 0 0;font-size:15px;line-height:1.6}
.rd[open]>summary b::after{content:" ▾";color:var(--mut)}.rd:not([open])>summary b::after{content:" ▸";color:var(--mut)}
.arrow{text-align:center;color:var(--mut);font-size:13px;margin:-4px 0}
.mp td{vertical-align:top;font-size:14px;line-height:1.55}.mp td:first-child{white-space:nowrap}
.lid{display:inline-block;font-size:12px;font-weight:700;padding:1px 7px;border-radius:10px;border:1px solid var(--line);margin:2px 2px 0 0;text-decoration:none}
.pill.gap{background:color-mix(in srgb,var(--warn) 16%,transparent);color:var(--warn);font-size:11px}
.bluf{font-size:17px;line-height:1.7}.qq p{margin:4px 0 10px;font-size:15px}
ol.src{font-size:13px;line-height:1.6;padding-left:22px;word-break:break-word}ol.src li{scroll-margin-top:80px}
@media(max-width:700px){table.mp.stack td[data-l]::before{content:attr(data-l)"　";color:var(--mut);font-size:12px;font-weight:600;display:block}table.mp.stack td:first-child{white-space:normal;font-size:16px}}
</style>"""


# 旧 pcb-map.html 锚点 → pcb.html 新位置
HASH = {'road': 'road', 'ai': 'road-ai', 'map': 'pattern', 'check': 'check', 'gap': 'gaps', 'src': 'src'}


def main():
    js = ('var h=location.hash.slice(1),M=' + __import__('json').dumps(HASH) + ',U=' + __import__('json').dumps({f's{i}': f'src{ID[k]}' for i, k in enumerate(USE, 1)}) +
          ';location.replace("pcb.html#"+(M[h]||U[h]||"layers"));')
    html = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<!-- 由 pcb/map.py 生成：底图已并入 pcb.html（2026-10-23），本页只做跳转 -->\n'
            '<title>PCB 底图已并入 PCB 研究页</title><meta http-equiv="refresh" content="0; url=pcb.html#layers"><link rel="canonical" href="pcb.html">'
            f'<script>{js}</script></head><body style="font-family:-apple-system,sans-serif;padding:24px">'
            '<p>PCB 技术路线图 + 格局图已并入 <a href="pcb.html#layers">PCB 研究页</a>（第 2、3 章）。正在跳转…</p>'
            '<ul><li><a href="pcb.html#road">技术路线图</a></li><li><a href="pcb.html#pattern">格局图</a></li><li><a href="pcb.html#check">一线校验</a></li><li><a href="pcb.html#gaps">数据缺口</a></li></ul></body></html>\n')
    open(os.path.join(R0, 'pcb-map.html'), 'w', encoding='utf-8').write(html)
    print('pcb-map.html → 跳转到 pcb.html（旧锚点已映射）')


if __name__ == '__main__':
    main()
