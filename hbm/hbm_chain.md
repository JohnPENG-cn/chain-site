# HBM 小链研究样板 v0.2（最近更新 2026-10-15）

> 更新记录：v0.2（2026-10-15）补 2023–24 供给和分厂季度产能、每 GB 价格实数、韩国出口回测、成本与资本开支、工艺-设备-材料表、公司图谱来源与营收占比；v0.1（2026-10-14）首版。

> 一句话判断：**HBM 的天花板不在封装设备，而在 DRAM 晶圆本身。** 一片晶圆做 HBM 只出约 1/3 的位元，现在普通 DRAM 也在涨价、利润率 70–80%，原厂每多做一片 HBM 就少赚一片普通 DRAM 的钱。所以 2026 年 HBM 价格被年度合约"锁低"了，**2027 年一定要重新定价**。按我的模型，2027 年 HBM 缺口约 **19%**（区间 5%–26%），价格大涨的确定性高；**真正的风险是 2027 年下半年起新厂集中投产，这轮存储超级周期见顶。**

标注规则：【源】= 公开来源（附录有链接）；【估】= Kiko 自己估的，假设写在旁边。

---

## 结论先看（5 条）
1. **2026 年供需基本平衡（模型 -3%），2027 年明显短缺（-19%）。** 需求从约 3.0 EB 涨到 4.9 EB【估】，主要靠 Rubin/Rubin Ultra 和谷歌 TPU；供给从约 2.9 EB 只涨到 4.0 EB【估】，因为 HBM4 的芯片更大、堆叠层数更多，每片晶圆出的 GB 反而变少。
2. **利润堆在内存厂，已经超过台积电。** SK 海力士 2Q26 营业利润率 76%，美光 FQ4 2026 毛利率 87%，台积电 2Q26 营业利润率 60.3%【源】。但这些利润主要来自**普通 DRAM 涨价**：TrendForce 说 1Q26 HBM 每片晶圆的产值和毛利都低于 DDR5 服务器内存【源】。
3. **瓶颈排序**：① DRAM 晶圆和洁净室（最慢，新厂要 2–3 年）> ② HBM4 良率与客户认证（三星、美光追赶的关键）> ③ TSMC 基础裸片 (base die) 和 CoWoS 配套 > ④ TC 键合机（订单周期约 3–6 个月，最容易缓解）。
4. **韩国出口数据是"同步+提前公布"的指标（已回测）**：和美光、海力士营收同比的相关系数 0.97–0.98，最高点在滞后 0–1 个月，不领先营收本身；但它比财报早 1–2 个月公布，而且**出口同比见顶比营收绝对值见顶早约 9–10 个月**（2017–18、2021–22 两轮都成立，2024 年一次假信号）。9 月半导体出口 603 亿美元、+262.8%，还在加速【源】。
5. **周期位置**：普通 DRAM 处在"短缺暴涨"档；HBM 合约价还在"被锁低"档，2027 年会补涨。这像 2017–2018 年的 DRAM 超级周期顶部区：利润率创历史新高、各家同时宣布大扩产。

## 0. 核心争议（3 个可证伪问题）
| # | 争议 | 我的观点 | 怎么证伪 |
|---|---|---|---|
| Q1 | 2027 年 HBM 会过剩还是短缺？ | 短缺，价格大涨 | 2027 年 HBM 合约价同比没涨 ≥50%，或 SK 海力士/美光说 2027 年产能没卖完 |
| Q2 | 三星、美光扩产会不会让 HBM 很快过剩？ | 2027 年不会，因为和普通 DRAM 抢同一批晶圆 | 2027 年普通 DRAM 价格先跌、原厂把晶圆转回 HBM，HBM 价格跟着松动 |
| Q3 | 这轮存储周期什么时候见顶？ | 最早 2027 年中后期，看新厂投产节奏 | 韩国半导体出口同比在 2027 年一季度前仍高于 +100% 并继续加速 → 我判断太早 |

## 1. 边界、工艺、计量单位

（v0.2 新增工序-设备-材料表见文末"v0.2 增补 A"。）
- **产品**：把 8/12/16 层 DRAM 裸片用 TSV（硅通孔）竖着叠起来，底下放一颗 base die（逻辑底座），通过 CoWoS 和 GPU 封在一起。
- **计量单位**：需求用 **GB（容量）**，产能用 **片/月（12 寸晶圆投片）**，出货单位是 **颗（stack）**。换算：一颗 HBM3E 12 层 = 36GB；HBM4 12 层 = 36GB、16 层 = 48GB（JEDEC 公开规格）。
- **工艺**：DRAM 前道 → TSV 刻蚀/填铜 → 减薄 + 临时键合/解键合 → 堆叠键合（TC-NCF / MR-MUF，下一代是混合键合）→ 测试 → 交给 CoWoS。
- **关键物理事实**：HBM 每个位元耗用的晶圆约是 DDR5 的 **3 倍**【源 siliconanalysts 转述美光】。TrendForce 估计年底 HBM 占 DRAM 投片 18%/22%/30%（2025/26/27），但只占位元的 8%/9%/13%【源】。**这就是整条链的第一性原理：HBM 吃晶圆很凶。**

## 2. 需求 = 加速器出货 × 每颗 HBM 容量
| 年份 | 主要拉动 | 需求 (EB) |
|---|---|---|
| 2023 | H100（80GB） | 0.17【估】 |
| 2024 | H100/H200、TPU、MI300 | 0.56【估】 |
| 2025 | Blackwell 192GB、TPU | 1.75【估】 |
| 2026 | Blackwell 约 545 万颗（B300 288GB）、TPU 370 万颗、Rubin 约 150 万颗 | 3.01【估，出货部分有源】 |
| 2027 | Rubin + Ultra 约 700 万颗（Ultra 384GB）、TPU 500 万颗 | 4.92【估，出货部分有源】 |

![需求结构](chart_demand_mix.png)

- 有来源的数字：Blackwell 2026 约 540–550 万颗、2027 年 Rubin+Ultra 近 700 万颗（Hilo 转述券商报告）；Rubin 2026 下调到约 150 万颗（Magica）；TPU 2026/27 年 370 万/500 万颗（JPMorgan）；单颗容量 96/192GB → 216/288GB，Rubin Ultra 384GB（TrendForce）【源】。
- 其余拆分（B200/B300 4:6、AWS、AMD、中国芯片）都是【估】，在 Excel"需求"页黄色格可改。
- **判断**：2027 年需求增速（+63%）主要是 **单颗容量提升 + ASIC 放量**，英伟达占比下降，谷歌是最快的增量（与 TrendForce"谷歌增长最快"一致）。

## 3. 供给（按厂）
| 厂商 | 2025 | 2026 平均 | 2027 计划 | 来源与说明 |
|---|---|---|---|---|
| SK 海力士 | ~15 万片/月【估】 | 15–20 万【源 ETNews 行业估计】，模型取 17 万 | 23 万【估】：M15X、龙仁 | HBM4 2Q26 量产，良率"接近 HBM3E"【源 财报会】 |
| 三星 | ~11 万【估】 | 15 万（Chosun）~18 万（BigGo）【源】，取 16.5 万 | ~25 万【源 BigGo】 | HBM4 良率约 80%【源 BigGo，媒体口径】；用自家 4nm base die |
| 美光 | 4–5 万【源】 | 年底 10 万【源】，平均取 7 万 | 11 万【估】 | 2027 年 HBM 大部分已签约、价格大涨【源 财报】 |
| 长鑫 CXMT | 0 | 规划 6 万但良率仅 25–30%【源 媒体】，有效取 1 万 | 2.5 万【估】 | 只供国内，暂时不影响全球平衡 |

- **2023–24 补建模（v0.2）**：季度产能均值 2023 年约 6.2 万片/月、2024 年约 18.8 万片/月（三星证券 2024-03 季度图读数）× 每片有效 GB 350/450【估】× 稼动率 85%/80%【估】→ 供给约 **0.22 EB / 0.81 EB**。2024/2023 = 3.7 倍，和 TrendForce"2024 年位元供给 +260%（3.6 倍）"对得上【源 25】。但比可见加速器需求（0.17/0.56 EB）高，说明 2024 年需求被低估（中国囤货、库存、三星未过认证的产出）。
- **TrendForce 交叉验证**：2025-05 它预测 2026 年 HBM 出货超过 300 亿 Gb（约 3.75 EB），比本模型 2026 年高约 25%【源 37】。
- 每片有效 GB：2025 年 600、2026 年 650、2027 年 600【估】；稼动率 85%/90%/90%【估】。这个参数最敏感：2027 年取 550 → 缺口 26%；取 700 → 缺口 5.5%。**所以方向是短缺，但幅度区间很宽。**

## 4. 供需平衡表 + 价格档位
| 年份 | 需求 EB | 供给 EB | 缺口 | 价格表现 |
|---|---|---|---|---|
| 2023 | 0.17 | 未建模 | 公开口径：售罄 | 涨 |
| 2024 | 0.56 | 未建模 | 公开口径：售罄 | 涨 |
| 2025 | 1.75 | 1.84 | +5% | 签 2026 年合约，价格偏低 |
| 2026 | 3.01 | 2.91 | -3%（基本平衡） | 年度合约锁价，均价"暂停/小跌"【源 TrendForce】 |
| 2027 | 4.92 | 3.99 | **-19%** | 合约价"数倍"上涨【源 TrendForce 预期】；美光说"大幅上涨"【源】 |

![平衡表](chart_balance.png)

**价格四档（麦肯锡成本曲线框架）**：
- 普通 DRAM：已经在**第 4 档"短缺暴涨"**，美光 FQ4 DRAM 价格环比涨十几个百分点【源】。
- HBM：2026 年被年度合约压在**第 2 档以下**（每片产值低于 DDR5）。HBM 的真实价格底 = 同一片晶圆做普通 DRAM 能赚的钱 × 约 3。只要普通 DRAM 还贵，HBM 2027 年就得补涨。

## 5. 利润池
![利润率](chart_margin.png)
- 内存厂利润率：SK 海力士 41% → 76%（2Q25 → 2Q26），美光毛利率 45.7% → 87.0%（FQ4 25 → FQ4 26）【源】；三星 3Q26 初步营业利润 107.4 万亿韩元【源】。
- HBM 市场份额（按营收）2Q26：海力士 50%、三星 33%、美光 18%（Counterpoint）【源】。三星一个季度从 21% 跳到 33%。
- **利润迁移判断（克里斯坦森"利润守恒"）**：2023–2025 年，利润从"会做 HBM 的人"（海力士）身上来；2026 年 HBM 开始被三家都能做（逐渐商品化），利润转回"晶圆本身"（普通 DRAM 也赚钱）；2027 年以后，利润会继续往**最难的那一环**走：定制 HBM4E 的 base die（台积电 3nm、美光与英伟达合作 NVHBM【源】）和混合键合。

## 6. 瓶颈与交期
| 环节 | 现状 | 缓解需要多久 | 判断 |
|---|---|---|---|
| DRAM 晶圆/洁净室 | 三家同时扩，HBM 占投片到 30% | 新厂 2–3 年 | **头号瓶颈** |
| HBM4 良率/认证 | 海力士领先；三星约 80%；长鑫 25–30% | 6–12 个月 | 决定份额 |
| base die（台积电 12nm/3nm） | 海力士、美光（HBM4E）靠台积电 | 跟着台积电产能走 | 与 CoWoS 共振 |
| CoWoS | 台积电 2026 年底 12–14 万片/月，2027 年底 19–20 万；缺口从 20% 收窄到 10%【源】 | 2027 年缓解 | 决定 HBM 能不能"装上去" |
| TC 键合机 | 韩美一单 442 亿韩元（约 15 台）给海力士【源】；韩华、ASMPT 也拿单 | 3–6 个月 | 最容易缓解，不是真瓶颈 |
| 混合键合 | 韩美二代混合键合机开发中，主流预计 2029–2030【源】 | 3 年+ | 是下一代的变量 |

**与你案例 3（固晶机/键合机）对齐**：案例 3 判断"键合从引线 → TCB → 混合键合"，这里验证了 TCB 是 HBM4 的主线；但从供需看，键合机是**跟随者，不是卡脖子环节**。国产高端键合机≈0、快克 TCB 从 0 到 1，要找"卡住的环节"应该看晶圆和良率。案例 10（临时键合材料）是 HBM 减薄工序的必需品，跟着 HBM 晶圆量走。

## 7. 历史与格局
- **DRAM 周期**：2008–09 年寒冬奇梦达破产，2012 年尔必达破产（美光收购），格局变成三家寡头；2017–18 年超级周期 → 2019 年价格腰斩；2022–23 年再次亏损（海力士 2023 年亏损）→ HBM 救场。规律是：**利润率历史新高 + 同时大扩产 → 18–24 个月后过剩。**
- **HBM 代际**：HBM（2015，AMD Fiji）→ HBM2 → HBM2E → HBM3（2022，H100）→ HBM3E（2024，H200/B200）→ HBM4（2026，Rubin）→ HBM4E（2027，定制 base die）。每一代谁先过英伟达认证，谁拿大部分利润：海力士靠 HBM3 翻身；三星在 HBM3E 掉队，到 HBM4 才追上。
- **类比**：现在像 **2017 年底到 2018 年**：利润率创新高、资本开支加速。不同之处是 HBM 加了一层"抢晶圆"的机制，长期合约（美光 RPO 约 1500 亿美元，take-or-pay）会把过剩推迟，但不会让周期消失。

## 8. 领先指标
| 指标 | 频率 | 领先什么 | 现在读数 |
|---|---|---|---|
| 韩国 1–10 日/1–20 日出口（半导体、存储） | 每 10 天 | 三星/海力士当季营收 0–1 个月 | 10 月 1–10 日 +170.9%；9 月存储出口 540.7 亿美元 +358.6%【源】 |
| TrendForce DRAM 合约/现货价、HBM 合约新闻 | 周/月 | 原厂毛利 1–2 个季度 | 2027 年 HBM 合约"数倍上涨"预期 |
| 原厂财报：HBM 售罄说法、资本开支 | 季度 | 供给 2–3 年 | 美光：2027 年大部分已签 |
| 设备订单（韩美、韩华、ASMPT、Besi） | 公告 | HBM 产能 3–9 个月 | 4.5 代 TCB 持续下单 |
| 台湾月营收（台积电、创意、弘塑、辛耘） | 月 | CoWoS/base die 产能 | 待接入 |
| 台积电 CoWoS 产能预测 | 季度 | 可装机 HBM 量 | 2027 年底 19–20 万片 |

**回测（v0.2 完成）**：数据用韩国产业通商部 2015-01 至 2025-12 月度半导体/存储出口 CSV（公共数据门户），2026 年 1–9 月用产业部通报补齐；营收用美光 SEC XBRL 季度营收（42 个同比点）和 SK 海力士季度营收（18 个同比点）。

| 出口领先 k 个月 | −1 | 0 | +1 | +3 | +6 | +9 |
|---|---|---|---|---|---|---|
| 与美光营收同比相关 | 0.979 | 0.972 | 0.949 | 0.83 | 0.481 | 0.09 |
| 与海力士营收同比相关 | 0.954 | 0.966 | 0.956 | 0.816 | 0.345 | -0.059 |

拐点：出口同比见顶 2017-11 / 2021-08 / 2024-06，美光营收同比见顶 2017-05 / 2021-08 / 2024-08；营收绝对值见顶 2018-08（+9 个月）、2022-05（+9 个月，海力士 2022-06 +10 个月），2024 年只回落一个季度（假信号）。见底：2016-03/2019-10/2023-03 对 2016-02/2019-08/2023-05。
**结论**：它是同步指标，用来"提前 1–2 个月知道财报"；真正有预判价值的是"出口同比见顶 → 约 9 个月后营收见顶"。最新 3 个月同比还在上升，没有见顶。

## 9. 可验证的预测（到期打分）
| # | 预测 | 检查日期 | 怎样算对 |
|---|---|---|---|
| P1 | 10 月全月韩国半导体出口同比 > +150% | 2026-11-01 | 产业通商部月报 |
| P2 | 美光 FQ1 2027 营收 ≥ 600 亿美元（指引 615±15） | 2026-12-20 | 美光财报 |
| P3 | SK 海力士 4Q26 财报会说 2027 年 HBM 已基本售罄/签约完成 | 2027-01-31 | 财报会纪要 |
| P4 | 2027 年 HBM 混合均价同比 ≥ +50%（TrendForce 等公开口径） | 2027-06-30 | TrendForce 新闻稿 |
| P5 | 2027 年底前混合键合不会进入 HBM 大规模量产，TCB 仍是主流 | 2027-12-31 | 原厂/设备商公告 |
| P6 | 韩国半导体出口同比在 2027 年 3 月（含）之前首次跌破 +100%（周期见顶第一信号） | 2027-04-01 | 月度出口数据 |

## 10. 对外接口（串到大链）
| 输出 | 2026 | 2027 | 说明 |
|---|---|---|---|
| 可供量 | 约 2.9 EB | 约 4.0 EB | 【估】 |
| 单耗：每颗 GPU 用几颗 HBM | B300：8 颗 × 36GB = 288GB | Rubin：8 颗 HBM4 = 288GB；Ultra 每 GPU 384GB | 规格为公开口径 |
| 等价颗数（按 36GB/颗） | ~8,100 万颗 | ~1.1 亿颗 | 【估】 |
| 价格方向 | 合约锁价，小跌 | 大涨 | TrendForce |
| 下游接口 | CoWoS：每片 CoWoS 晶圆封装约 X 颗 GPU（下一条小链来定）；**可出货 GPU = min(CoWoS 产能, HBM 可供量 ÷ 单颗容量, 前道晶圆)** | | |

## 验证用标的（按环节，非推荐；业务关联来自公开报道，占比未逐一核实）
| 环节 | 韩/美/台/港 | A 股 |
|---|---|---|
| HBM 原厂 | SK 海力士 000660.KS、三星 005930.KS、美光 MU | 长鑫（未上市） |
| TC/混合键合 | 韩美半导体 042700.KS、ASMPT 0522.HK、Besi BESI.AS | 快克智能 603203、拓荆科技 688072 |
| base die/CoWoS | 台积电 2330.TW、创意 3443.TW、弘塑 3131.TWO、辛耘 3583.TWO | — |
| 测试/检测 | 爱德万 6857.T | 赛腾股份 603283 |
| 材料 | — | 雅克科技 002409（前驱体）、华海诚科 688535（塑封料）、飞凯材料 300398/鼎龙股份 300054（临时键合） |
| 国产封测/设备 | — | 通富微电 002156、长电科技 600584、北方华创 002371、华海清科 688120 |

## 说明与不足
- 2027 年缺口对"每片有效 GB"非常敏感（5%–26%），这是自估参数，没有公开精确值。
- 出货拆分大量是自估；2023–2024 年供给是用季度产能图读数 + 自估参数补的，只适合看量级。
- 回测样本少（海力士 18 点），2026 年用的是半导体总出口而非存储分项。
- 媒体口径（BigGo、The Economy、Magica）可靠度低于公司公告，已在文中标出。
- 不构成投资建议。

## 附录：来源（2026-10-14 均已用 curl 打开，HTTP 200）
1. TrendForce：HBM 投片/位元占比、2027 合约价 https://www.trendforce.com/presscenter/news/20260602-13074.html
2. TrendForce HBM 3Q26 报告摘要 https://www.trendforce.com/research/download/RP260805KC3
3. TrendForce HBM 价格展望摘要 https://www.trendforce.com/research/download/RP260527UC
4. SK 海力士 2Q26 财报 https://news.skhynix.com/en/q2-2026-business-results/
5. 首尔经济：海力士财报会（HBM4 良率） https://en.sedaily.com/finance/2026/07/29/sk-hynix-ramps-up-hbm4-in-second-half-to-boost-record-763
6. 美光 FQ4 2026 财报 https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/default.aspx
7. TrendForce 转 ETNews/Chosun：美光 10 万片、三星 15 万片 https://www.trendforce.com/news/2026/09/04/news-micron-reportedly-to-add-60k-hbm-wafersm-reaching-100k-by-year-end-to-narrow-gap-with-samsung-sk-hynix/
8. BigGo：三星 18 万 → 25 万片、base die 路线 https://finance.biggo.com/news/a6fce0cd-0fa5-463a-843d-d450cb21504a
9. Silicon Analysts：良率才是瓶颈、3 倍耗片 https://siliconanalysts.com/analysis/hbm4-capacity-bottleneck-2026-samsung-sk-hynix-qual
10. 三星 3Q26 业绩指引 https://news.samsung.com/global/samsung-electronics-announces-earnings-guidance-for-third-quarter-2026
11. Counterpoint HBM 份额 https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share
12. TrendForce 转经济日报：CoWoS 产能 https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands/
13. Hilo 转述摩根士丹利：2027 CoWoS 200k https://www.xxquant.com/en/institution/institutional-research/f7e9d2c0b2fbcc074e2beadf4a047434
14. Hilo：Blackwell/Rubin 出货 https://www.xxquant.com/en/institution/institutional-research/0a814e35a57b0479f86051f2dabbc088
15. 老虎证券转 JPMorgan：TPU 370 万/500 万 https://www.itiger.com/hans/news/1109625222
16. TrendForce：Blackwell 占 2026 高端 GPU 超 70% https://www.trendforce.com/presscenter/news/20260408-13003.html
17. 首尔经济：韩美 442 亿韩元 TCB 订单 https://en.sedaily.com/finance/2026/06/08/hanmi-semiconductor-wins-442-billion-won-order-to-supply
18. The Elec：ASMPT 获海力士 HBM4 TCB 订单 https://www.thelec.net/news/articleView.html?idxno=5517
19. 亚洲经济：韩美二代混合键合机 https://www.asiae.co.kr/en/article/2026040909273077978
20. 首尔经济：韩国 9 月出口 https://en.sedaily.com/finance/2026/10/01/koreas-september-exports-hit-record-1209-billion-on-chip
21. 亚洲经济：10 月 1–10 日出口 https://www.asiae.co.kr/en/article/2026101209183424033
22. The Economy：长鑫 HBM 良率 25% https://economy.ac/news/2026/09/202609295581
- 未单独打开验证：Magica（Rubin 下调）为搜索摘要；DRAM 历史（奇梦达、尔必达破产）为公认史实。


---
## v0.2 增补（2026-10-15）

### A. 工序 → 设备 / 材料 / 供应商
| 工序 | 要点 | 设备 / 材料 / 供应商 | 来源 |
|---|---|---|---|
| ① DRAM 前道（1b/1c 制程） | ~700 道工序；HBM die 比同容量 DDR5 大 35–45% | 光刻/刻蚀/沉积：AMAT（自称 DRAM 设备营收超过其后两家之和）；Lam、TEL、ASML 等为行业通用设备商（业务归属，未单列来源）；国产：北方华创、拓荆（业务归属，HBM 占比未披露） | 39 |
| ② TSV 正面（约 10 步） | 刻深孔 → 绝缘衬层 → 阻挡/籽晶 → 电镀填铜 → 微凸点 | AMAT：InVia 2 CVD 衬层、Ventura 2 PVD、Nokota 电镀；AMAT 自称 HBM 封装工艺设备份额 >50% | 39 |
| ③ 背面（约 9 步） | 临时键合 → 减薄 → 露铜 → 背面钝化/凸点 → 解键合 | 背面 PECVD 控翘曲（AMAT Avila）；减薄/CMP：华海清科；临时键合胶：鼎龙、飞凯（业务归属） | 39 |
| ④ 堆叠键合 | 8/12/16 层；HBM4 放宽至 775μm 厚度，16 层仍可用 TCB | SK 海力士 MR-MUF（液态 EMC 由日本 NAMICS 独家供应）；三星、美光 TC-NCF；TCB：韩美、ASMPT（目标 35–40% 份额）；混合键合：Besi、韩美二代（2029–30 主流） | 40,17,18,41,19 |
| ⑤ 测试/KGSD | 晶圆级 + 堆叠后测试，良率损失主要在此 | 爱德万（存储测试机，业务归属）；探针卡供应商未能用公开来源核实 | — |
| ⑥ base die | HBM4 起逻辑 base die | 台积电 12nm/3nm（海力士、美光）；三星自家 4nm | 8 |
| ⑦ 2.5D 集成 | HBM + GPU 上 CoWoS | 台积电 CoWoS；长电展示 HBM3E 2.5D 方案但无自有 HBM 产能 | 12,42 |

### B. 分厂季度产能（千片/月，季末）
| 季度 | SK 海力士 | 三星 | 美光 | 长鑫(有效) | 类型 |
|---|---|---|---|---|---|
| 4Q23 | 45 | 45 | 4 | 0 | 图读数 |
| 1Q24 | 60 | 45 | 10 | 0 | 图读数 |
| 2Q24 | 80 | 45 | 15 | 0 | 图读数 |
| 3Q24 | 110 | 80 | 25 | 0 | 图读数 |
| 4Q24 | 135 | 115 | 30 | 0 | 图读数 |
| 4Q25 | 150.0 | 150.0 | 45.0 | 0.0 | 锚点 |
| 4Q26 | 190.0 | 180.0 | 100.0 | 10.0 | 锚点 |
| 4Q27 | 260.0 | 250.0 | 120.0 | 25.0 | 锚点 |

（完整 1Q23–4Q27 季度序列在 data/hbm.json 的 cap 字段，年内为线性插值。）
- 1Q23–4Q24：三星证券 2024-03 报告 HBM Capa 季度图（图上读数，误差约 ±5K；2024 为当时预测）【源 24】
- 2024 年底：TrendForce 2024-03：三星约 130K、海力士约 120K（含 TSV），全行业约 250K/月；美光 4Q24 约 25K（工商时报）【源 25,26】
- 2025 年底：三星证券 2025-05：三星、海力士各约 150K；TrendForce 2025-10 称海力士扩至 150K；美光实际约 40–50K（ETNews，2026-09 回看），三星证券原预测 65K【源 27,7】
- 2026 年底：三星 180K（BusinessKorea：今年 18 万片/月，明年 25 万）；美光约 100K（ETNews）；海力士 190K 为估（ETNews 称三星、海力士各 15–20 万，叠加 M15X 爬坡）【源 28,7】
- 2027 年底：三星 250K（BusinessKorea 计划）；海力士 260K、美光 120K、长鑫 25K（有效产能）均为估：M15X 目标 8 万片/月、龙仁一厂 2027-02 开出首个洁净室【源 28,29】

### C. 每 GB 价格（实际 / 报道 / 预期）
- **DDR5 16Gb 固定价**（实际）：2025-05 $2.4/GB，2026-04 $17.5/GB，2026-05 $18.75/GB，2026-06 $20.0/GB，2026-07 $22.5/GB，2026-08 $23.25/GB，2026-09 $24.0/GB。韩国产业通商部月报引用的 DDR5 16Gb 固定交易价（$4.80→$48/颗）÷2GB【源 30,31,20】
- **DDR4 8Gb 固定价**（实际）：2025-05 $2.1/GB，2025-08 $5.3/GB，2025-11 $8.1/GB，2026-02 $12.5/GB，2026-04 $16.0/GB，2026-05 $20.0/GB。产业通商部 5 月出口报告：DDR4 8Gb 季度/月度固定价（1GB/颗）【源 30】
- **HBM3E 12层**（报道）：2025-08 $8.3/GB，2025-12 $13.9/GB，2026-06 $12.0/GB，2026-08 $17.5/GB。2025-08 $8.3、2025-12 续约 $13.9 为 Silicon Analysts 汇编的韩媒每颗报价 ÷36GB；2026 约 $1.50/Gb（≈$12/GB，Korea Herald）；$17–18/GB 为富邦研究经 MoneyToday 估计（英伟达口径）【源 32,33,34】
- **HBM4 12层**（报道/预期）：2025-08 $13.9/GB，2026-01 $16.7/GB，2026-09 $16.7/GB，2027-06 $36.1/GB。2025-08 约 $500/颗、2026-01 预期 >$600/颗（汇编）；2026 年约 $600/颗、2027 年约 $1,300/颗（首尔经济，业界估计）；三星 2027 报价 $4.5–4.9/Gb≈$36–39/GB（Korea Herald，为要价非成交价）【源 32,35,34】
- **关键发现**：DDR5 固定价从 2025-05 的 $2.4/GB 涨到 2026-09 的 $24/GB，已经高于 2026 年 HBM3E（约 $12–18/GB）和 HBM4（约 $16.7/GB）。HBM 每 bit 耗片约是 DDR5 的 3 倍，所以每 GB 至少要卖到 DDR5 的 3 倍（约 $72/GB）才能让每片晶圆收入持平【估】。2027 年 HBM4 约 $36/GB、混合 ASP +121%【源 35,36】，仍只有持平线的一半，说明原厂没有动力把晶圆从 DDR5 挪回 HBM，2027 年短缺的判断更稳了。反过来，如果 DDR5 价格先掉头，HBM 的相对吸引力会立刻上升，这就是 Q2 的证伪路径。

### D. 成本与资本开支
- 生产周期：比 DDR5 长 1.5–2 个月；从投片到封装完成超过 2 个季度【源 25】
- 每 bit 耗片：约 DDR5 的 3 倍（美光口径，经 Silicon Analysts）【源 9】
- 新增产能资本开支：M15X 投资 >20 万亿韩元，满产约 5 万片/月 → 约 4,000 亿韩元/千片月产能；龙仁一厂 120 万亿韩元、满产约 35 万片/月 → 约 3,400 亿韩元/千片【源 29】
- 洁净室到量产：M15X 首个洁净室 2026-05 完工试产，约 6 个月后量产【源 29】
- HBM 占 DRAM 产出：约 15%（The Elec 2026-03，SEMI 转述）；投片口径约 20% → 近 30%（三星）【源 43,35】
- 耗片倍数拆解：die 面积 ×1.35–1.45 → 良率 ÷0.7–0.8 → 约 1.7–2.1 倍（HBM3E 时代，TrendForce）；HBM4 加上 2048 I/O 更大 die、逻辑 base die、12/16 层堆叠 → 约 2.5–3.2 倍【估，按美光"约 3 倍"倒推】。
- 推论：全球 HBM 每多 1 万片/月产能，大约要 3.4–4 万亿韩元和 2–3 年（新厂）或约 6 个月（已有洁净室）。

### E. 利润池时间序列
- 美光 GAAP 毛利率：上轮顶点 2018-08 季 61%，2023-03 季 −32.7%，2026-09 季 86.8%（SEC XBRL）【源 49】。
- SK 海力士营业利润率：2023Q1 −66.9%，2026Q2 76.3%【源 48】。
- HBM 营收份额：2025 全年 63.2/19.3/17.4（IDC，二手转引）→ 1Q26 58/21/21 → 2Q26 50/33/18（Counterpoint）。

### F. 公司图谱补充
- 三条原"公认"供货边已补来源：SK 海力士 → 英伟达（NVIDIA 官方 2026-06-07 多年合作，为 Vera Rubin 共同开发并供应内存）【源 44】；美光 → 英伟达（美光 2026-03-16：HBM4 36GB 12H 为 Vera Rubin 设计并量产）【源 45】；三星 → 英伟达（三星 2026-02 商用 HBM4 出货，官方未点名客户，媒体称供英伟达）【源 46】。
- 新增：NAMICS（SK 海力士 MR-MUF 液态 EMC 独家）【源 40】、Applied Materials（HBM 封装工艺设备份额 >50%）【源 39】、ASMPT 先进封装占营收约 30%【源 41】。
- 国产化：长鑫 HBM3 量产推迟，试产良率约 25%【源 22,42】；长电展示 HBM3E 2.5D 方案但没有自有 HBM 产能【源 42】。通富微电的 HBM 业务没找到可核实的公开来源。
- 相关业务营收占比（HBM 专项均未披露；A 股来自 Tushare 2025 年报主营构成【源 50】，台积电【源 47】，ASMPT【源 41】）：

| 公司 | 相关业务营收占比 |
|---|---|
| 雅克科技 | 半导体化学材料 24.6%、光刻胶 22.8%、电子特气 4.8% |
| 华海诚科 | 环氧塑封材料 93.6% |
| 飞凯材料 | 半导体材料 20.8% |
| 鼎龙股份 | 半导体材料及芯片 57.0%（含临时键合胶） |
| 赛腾股份 | 自动化设备 74.6% |
| 快克智能 | 固晶键合封装设备 4.6% |
| 拓荆科技 | 半导体专用设备 96.6% |
| 通富微电 | 集成电路封测 97.6% |
| 长电科技 | 芯片封测 99.6% |
| 北方华创 | 电子工艺装备 93.4% |
| 华海清科 | 半导体装备 87.2% |
| 台积电 | 先进封装约 8%（2024）→ 略高于 10%（2025）→ 2026 年"十几%" |
| ASMPT | 先进封装 5.32 亿美元，占 2025 年营收约 30%；TCB 收入创纪录 |

### G. 公开数据补不了的
- 各厂每片良品 GB、TSV/堆叠良率：不公开，只能自估，这也是 2027 缺口区间宽的原因。
- 分厂季度产能：只有年末锚点和一张 2024 年券商图，海力士 2026–27 年没有可靠公开数字。
- HBM 合约价：没有现货和公开报价，只有韩媒报道和券商估计。
- 韩国 2026 年存储分项月度出口：只公布零散月份，回测用半导体总出口。
- HBM 专项营收占比：A 股/台股公司基本不披露。
- 探针卡、韩华 TCB、SEMES 等供应关系：这次没找到能打开的公开来源，没有画进图谱。

### v0.2 新增来源（2026-10-15 已打开）
24. 三星证券 2024-03 报告（HBM Capa 季度图） https://www.samsungpop.com/common.do?cmd=down&contentType=application%2Fpdf&fileName=2020%2F2024032107171771K_02_03.pdf&inlineYn=Y&saveKey=research.pdf
25. TrendForce 2024-03：2024 HBM 位元供给 +260%、die 大 35–45%、良率低 20–30%、年底产能 https://www.trendforce.com/presscenter/news/20240318-12081.html
26. TrendForce 转工商时报：美光广岛 4Q24 约 2.5 万片 https://www.trendforce.com/news/2024/07/10/news-samsung-sk-hynix-and-micron-ramp-up-hbm-production-reportedly-doubling-output-next-year/
27. Jukan 转三星证券 2025-05：2025 年底产能 https://www.semiconsam.com/p/samsung-securities-hbm-analysis-2025515
28. BusinessKorea：三星 18 万 → 25 万片、M15X 扩至 8 万片 https://www.businesskorea.co.kr/news/articleView.html?idxno=277595
29. 首尔经济 2025-12：M15X 投资、洁净室时间表、龙仁一厂 35 万片 https://en.sedaily.com/finance/2025/12/25/sk-hynix-to-launch-m15x-fab-in-may-2026-cementing-global-ai
30. 韩国产业通商部：2015–2025 月度半导体/存储出口（公共数据门户 CSV） https://www.data.go.kr/data/15051126/fileData.do
31. 产业通商部：2026 年 1–8 月月度半导体出口 https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/172161/view
32. Silicon Analysts：HBM 每 GB 价格汇编（二手汇编，免费部分） https://siliconanalysts.com/market-data/hbm-pricing
33. TrendForce 转富邦/MoneyToday：HBM4 $31–32/GB、HBM3E $17–18/GB https://www.trendforce.com/news/2026/08/13/news-samsung-sk-hynixs-hbm4-push-puts-hbm-general-memory-pricing-in-the-spotlight-for-2h-earnings/
34. Korea Herald 2026-10-07：三星 2027 HBM 价格、HBM3E 约 $1.50/Gb https://www.koreaherald.com/article/10895833
35. 首尔经济 2026-10-01：HBM4 $600 → $1,300/颗 https://en.sedaily.com/finance/2026/10/01/hbm-prices-to-more-than-double-next-year-as-shortage
36. TrendForce 2026-09-29：2027 HBM 混合 ASP +121% https://www.trendforce.com/presscenter/news/20260929-13255.html
37. TrendForce 2025-05：HBM4 溢价超 30% https://www.trendforce.com/presscenter/news/20250522-12589.html
38. TrendForce 2024-05：HBM 约 DDR5 的 5 倍价 https://www.trendforce.com/presscenter/news/20240506-12125.html
39. Applied Materials：HBM 新增 19 道工序、封装设备份额 https://www.appliedmaterials.com/us/en/newsroom/blogs/hbm--materials-innovation-propels-high-bandwidth-memory-into-the.html
40. Dealsite：SK 海力士 MR-MUF 材料由 NAMICS 独家供应 https://dealsite.co.kr/articles/119413
41. ASMPT 2025 年报公告：先进封装 5.32 亿美元、TCB https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2025-annual-results/
42. Wccftech 转 ZDNet Korea：长鑫 HBM3 延后、长电 HBM3E 方案 https://wccftech.com/china-ymtc-hits-hbm3-roadblock-domestic-makers-rush-hbm-manufacturing/
43. The Elec 2026-03：HBM 约占 DRAM 产出 15% https://www.thelec.net/news/articleView.html?idxno=5886
44. NVIDIA 与 SK 海力士多年合作（2026-06-07） https://nvidianews.nvidia.com/news/sk-hynix-ai-factory
45. 美光：HBM4 为 NVIDIA Vera Rubin 设计并量产（2026-03-16） https://investors.micron.com/news/press-release/2026/Micron-in-High-Volume-Production-of-HBM4-Designed-for-NVIDIA-Vera-Rubin-PCIe-Gen6-SSD-and-SOCAMM2-03-16-2026/default.aspx
46. 三星：首家商用 HBM4 出货（未点名客户） https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing
47. TSMC 4Q25 法说会：先进封装营收占比（转引原话） https://www.aipredictionindex.com/p/wei-2026-advanced-packaging-low-teens-2026/
48. SK 海力士季度营收/利润（StockAnalysis 汇总财报） https://stockanalysis.com/quote/krx/000660/financials/?p=quarterly
49. 美光季度营收/毛利（SEC XBRL API） https://data.sec.gov/api/xbrl/companyfacts/CIK0000723125.json
50. Tushare fina_mainbz：A 股公司 2025 年报主营构成 https://tushare.pro/document/2?doc_id=81
51. TrendForce 2025-12：三星、海力士 2026 HBM3E 提价约 20% https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/
