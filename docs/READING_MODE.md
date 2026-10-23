# 阅读模式（article）模板

2026-10-23 起 `pcb.html` 使用。HBM / CoWoS / 铜页面以后想换成这个版式时，照下面的步骤做。这一轮还没有改这几个页面。

版式参照 SemiAnalysis 长文：单栏、留白多、先给结论、图表做全宽、来源做成脚注，界面元素尽量少。整套样式仍然在 HIG 设计系统里，不另起一套。

## 三个文件

| 文件 | 作用 |
|---|---|
| `assets/hig.css` 第 12 节 | 所有样式都挂在 `body.article` 下面，别的页面不受影响 |
| `assets/reading.js` | ① 把 JS 后渲染出来的行内“源N”标签也转成上标；② 点上标弹出来源摘要（手机上是底部抽屉）；③ 顶部细进度条、当前章节名、目录抽屉，宽屏（≥1180px）时目录常驻左侧 |
| `tpl/article.py` | 生成页面时用的 Python 助手，见下表 |

## 版式规则

* **正文**：17px，行高 1.75。单栏最宽 680px，大约一行 40 个汉字。
* **开篇**：
  1. kicker（栏目小字）
  2. 大标题
  3. dek（标题下的一段灰字说明）
  4. BLUF：大字摘要，“一句话版本”，第一句加粗放大
  5. `stats()`：一排 4 个关键数字
  6. “什么会证明我们错”
  7. “怎么读”说明，里面写明“不构成投资建议”
* **每一章**依次是：
  1. `chapter()`：章号 01–09 + 标题 + 导语
  2. `callout()`：这一章的关键判断，一句话
  3. 正文和图
  4. `more()`：密集表格、证据放进去，默认收起
* **图**：用 `figure()`。顺序是图标题 → 图 → 一句图注 → 一行灰字“来源 …”。宽屏上最宽 960px，手机上左右贴边。
* **对比**：用 `compare()`。宽屏左右两栏，手机上下叠放（比如“市场 vs 本页”“海外 vs 中国”）。
* **来源**：
  * 行内不再出现“源N”标签，改成小号上标数字，点一下可以看来源。
  * 编号就是页末来源表里的全局编号，所以稳定、可追溯。
  * 每张图、每张表下面有一行来源。
  * 页末是「来源与注释」（`#src`，默认展开）。
  * **一个来源都不能丢**，只是换了位置。
* **标签**：
  * 总账编号 `.lid` / `.gtag` 做成淡色小胶囊。
  * `估` 用浅紫色小胶囊。
  * `数据缺口` / `付费 · 未核` 保持醒目。

## tpl/article.py 助手

| 函数 | 用途 |
|---|---|
| `fnify(html)` | 把 `<span class="tag t-src"><a href="#srcN">源N</a></span>` 换成 `<sup class="fn"><a class="fn-a" href="#srcN">N</a></sup>`。整页生成完最后调一次 |
| `src_line(html, titles, extra='')` | 从一段 html 里收集来源编号，生成“来源：短标题 N；…”这一行。`titles = {编号: 标题}` |
| `strip_fn(html)` | 去掉图注里的来源标签（来源已经挪到下面那一行） |
| `figure(id, 标题, 图html, 图注, titles, wide=True, extra='')` | 全宽图 |
| `more(摘要, 内容, titles=None, small='', open_=False, wide=False)` | “展开细节”；传了 `titles` 会自动在下面加来源行，`wide=True` 时宽屏展开后比正文宽 |
| `callout(一句话, label='本章判断')` | 本章判断（只复述页面里已有的判断，不新增） |
| `chapter(id, 序号, 标题, 导语)` | 章节开头。会写上 `data-toc`，`reading.js` 靠它生成目录 |
| `compare(rows, 左标签, 右标签)` | 并排对比，`rows = [(题, 左, 右, 尾注)]` |
| `stats([(数字, 说明)])` | 关键数字一排 |

## 迁移一个页面（例如 hbm.html）

1. 生成函数里输出 `<body class="article">`。
2. 页头后面放：
   * `<div class="rd-bar" id="rdBar">…</div>`
   * `<nav class="rd-toc" id="rdToc">`

   照抄 `tpl/page_v3.py`。旧的 `nav#nav.two` 可以去掉，`chain.js` 找不到它会自动跳过。
3. 每个 `<section>` 加上 `data-toc="序号 短标题"`，章节用 `A.chapter()` 生成。
4. 图表用 `A.figure()` 包起来，原来的图注照传，来源会自动挪到来源行。
5. 宽表用 `A.more(…, wide=True)` 包起来。
6. 页末放上 `#src` 来源列表，以及脚注弹层 `<div class="fn-sheet" id="fnSheet">…</div>`（照抄）。
7. 脚本最后加载 `assets/reading.js`。
8. 整页 html 最后过一遍 `A.fnify()`。`page_v3` 会断言页面里不再有行内来源标签。
9. 跑 `./build.sh`，再按下面的“验收”逐项检查。

## 验收（每次改完都要做）

* 在 390px 和 1280px 宽度下，`document.documentElement.scrollWidth` 都等于视口宽度，也就是没有横向滚动。
* 所有图里都有 `svg path`，也就是图都画出来了。
* 点任意一个上标，`#fnSheet` 会出现，里面有来源标题和“打开原文 / 在来源列表中查看”。
* 来源引用对比：用旧页和新页逐个编号统计 `href="…#srcN"` 的次数，新页每个编号都不能少于旧页。
* 截图放在 `shots/`，命名为 `{page}_read_before|after_{390|1280}.png`。
