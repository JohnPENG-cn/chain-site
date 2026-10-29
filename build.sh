#!/usr/bin/env bash
# 全站数据的唯一构建入口：重跑任何次结果相同，不会丢内容（手写内容在 hbm/content.json 与 cowos/build.py，数字由脚本算）。
# 页面 hbm.html / cowos.html 由 tpl/page.py 从 hbm/page.py、cowos/page.py 生成，不要手改。
# 顺序有依赖：CoWoS 模型（出货表）→ HBM（需求读出货表）→ CoWoS 成稿（读 HBM 供给做对账，并刷新 toc.json 文字）。
set -euo pipefail
cd "$(dirname "$0")"
python3 cowos/model.py
python3 hbm/build.py
python3 cowos/build.py
python3 pcb/build.py     # PCB 小链：读 CoWoS 页出货表与 TOC 汇总、HBM 页中国账本（回测数据由 pcb/backtest.py 单独联网生成）
python3 pcb/map.py       # PCB 底图层：技术路线图 + 格局图 → pcb-map.html（只链接 G/P 编号，不新增判断）
python3 cu/build.py      # 大宗商品系列：铜（回测数据由 cu/backtest.py 单独联网生成）
python3 tpl/page.py      # 三页同一模板（结论层 + 底稿 13 步），见 SOP 页面规范；pcb.html 用 tpl/page_v2.py 行业版。pcb_v1.html / pcb_v1.js / data/pcb_v1.json 是 v1 冻结存档，构建不重写
python3 ledger/build.py  # 全局判断总账：data/ledger.json → ledger.html + ledger_ids.js；检查每条都对得上研究页条目（不过就停）
python3 hdd/build.py     # HDD 链库页 v0.1：一页总览（读 explain/hdd.py 来源表 + data/chains.json 节点数字）
python3 bubble/build.py  # AI 泡沫监控页：读 world/ai_bubble.json（世界看板每日更新时现算）→ ai-bubble.html；json 缺失时整页显示待补
python3 explain/build.py # 万物原理图：explain/<专题>.py 规格 + explain/<专题>.js 图形 + explain/engine.js 通用引擎 → explain-<专题>.html、explain.html、首页卡片
python3 tools/hig_apply.py  # 全站接入统一设计系统 assets/hig.css（Apple HIG）；幂等，只动页面外壳
python3 tools/cachebust.py # 全站静态资源加 ?v=内容哈希（防 iOS Safari / CDN 新旧混用）；必须最后跑
# 阅读版排版检查：9 个宽度 × 两档缩放，查横向滚动、出视口、压目录栏、图表文字出界/重叠（约 1 分钟；SKIP_LAYOUT_CHECK=1 跳过）
if [ "${SKIP_LAYOUT_CHECK:-0}" != "1" ]; then python3 tools/overflow_check.py; fi
echo "构建完成。"
