# 产业链行情情报站 · 调研与方案（2026-10-14）

## 一、最值得抄的 5 个做法（链接均已从 box 验证 200）
1. **Finviz 板块地图** https://finviz.com/map.ashx 、**TradingView 热力图** https://www.tradingview.com/heatmap/stock/
   抄：方块面积=市值、颜色=涨跌、按 行业→子行业→个股 嵌套；点方块下钻。我们改成按"产业链节点"分组而不是按申万行业。
2. **Prewave** https://www.prewave.com
   抄：供应商节点图 + 事件（新闻/公告）自动打标签挂到节点上 + 风险评分。我们的 GB300 风险模型已有这套方法。
3. **Koyfin** https://www.koyfin.com
   抄：自定义 watchlist 仪表盘、一屏多指标小图（价格、估值、宏观序列并排），"关键指标监控"页照此做。
4. **Simon Willison 的 git scraping** https://simonwillison.net/2020/Oct/9/git-scraping/ （配套 https://github.com/simonw/git-history ）
   抄：定时任务抓数据→写 JSON 提交进 Git 仓库→静态页读取；历史自动留痕，零服务器，完美契合 GitHub Pages。
5. **World Monitor（开源情报仪表盘）** https://github.com/koala73/worldmonitor
   抄：多源 RSS/新闻聚合 + LLM 分类摘要 + 单页仪表盘的信息架构。新闻源可用 **RSSHub** https://github.com/DIYgod/RSSHub 补齐（自建/公共实例，可生成财联社等路由）。
   备选可 fork：OpenBB https://github.com/OpenBB-finance/OpenBB （数据层大而全，偏海外）、AKShare https://github.com/akfamily/akshare （A股免费数据）、TradingAgents https://github.com/TauricResearch/TradingAgents （多 agent 研究流程参考）。
   国内参考：发现报告 https://www.fxbaogao.com （研报检索可达）；萝卜投研 robo.datayes.com 从 box 连不上，未验证。同花顺/东财产业链图谱需登录，只作版式参考。

## 二、推荐架构
- 静态站：GitHub Pages（JohnPENG-cn/chain-site），单页多 tab，纯 HTML+ECharts，手机可加主屏。
- 数据：box 上每交易日 19:30 跑 Python（Tushare+AKShare+cninfo），输出 data/*.json 提交推送（git scraping）。GitHub Actions 境外 IP 访问国内源不稳，优先 box。
- 页面：
  1. 产业链图谱：上中下游节点卡片（节点→代表股/ETF，当日涨跌、主力资金、近 24h 新闻数、风险色）
  2. 行情热力图：按链节点分组的 treemap
  3. 关键指标监控：每条链 3–5 个先行指标。AI算力：台积电月营收(MOPS)、HBM/DRAM 现货价、光模块龙头股价与资金、NVIDIA 季报；铜：沪铜主连、LME、库存
  4. 新闻与公告流：财联社电报+个股新闻+cninfo 公告，LLM 打"链/节点/利好利空/重要度"标签
  5. 信号与可证伪点：沿用 GB300 的验证日历（如 ODM 月出货≥8000 台则认错），自动标绿/红

## 三、MVP（第一版，1–2 天）
只做 AI 算力 + 铜 两条链；页面 1、2、4 + 简版 3；新闻 LLM 打标；复用现有日报的 Tushare 代码。第 5 页和更多链放第二版。

## 四、数据源表（box 实测 2026-10-14）
| 来源 | 内容 | 免费 | box 实测 |
|---|---|---|---|
| Tushare（现账号） | daily、moneyflow、基金/ETF 份额 | 积分制 | 可用；无 sw_daily/news/anns_d；近期报 IP 超限，token 需重置 |
| AKShare stock_news_em | 东财个股新闻 | 是 | ✅ OK |
| AKShare stock_info_global_cls | 财联社电报 | 是 | ✅ OK（20 条） |
| AKShare futures_zh_daily_sina CU0 | 沪铜主连日线 | 是 | ✅ OK（5295 行） |
| AKShare stock_board_industry_name_em | 东财行业/概念板块 | 是 | ❌ 连接被断（东财反爬/限频），需重试或降频 |
| cninfo hisAnnouncement/query | 巨潮公告 | 是 | ✅ HTTPS 返回 200（HTTP 不通） |
| MOPS 月营收 mopsov.twse.com.tw | 台积电等台股月营收 | 是 | ✅ 200 |
| 统计局/海关 | 宏观、进出口 | 是 | 未测 |
| TrendForce/DRAMeXchange | DRAM/HBM 价格 | 首页免费、明细付费 | 未测，只能取公开摘要 |
| NVIDIA/TSMC IR、SEC EDGAR | 财报、法说会 | 是 | 未测 |

合规：只抓公开页、低频、标注来源；不转载全文研报/付费内容；东财、财联社等内容版权归原站，站点仅放标题+摘要+链接。仓库公开时不要提交 token。
