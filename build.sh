#!/usr/bin/env bash
# 全站数据的唯一构建入口：重跑任何次结果相同，不会丢内容（手写内容在 hbm/content.json 与 cowos/build.py，数字由脚本算）。
# 页面 hbm.html / cowos.html 由 tpl/page.py 从 hbm/page.py、cowos/page.py 生成，不要手改。
# 顺序有依赖：CoWoS 模型（出货表）→ HBM（需求读出货表）→ CoWoS 成稿（读 HBM 供给做对账，并刷新 toc.json 文字）。
set -euo pipefail
cd "$(dirname "$0")"
python3 cowos/model.py
python3 hbm/build.py
python3 cowos/build.py
python3 tpl/page.py      # 两页同一模板（结论层 + 底稿 13 步），见 SOP 页面规范
echo "构建完成。"
