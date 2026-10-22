#!/usr/bin/env python3
"""把全站 HTML 接到统一设计系统 assets/hig.css（参照 Apple HIG）。幂等，只动页面"外壳"，不动正文：
  1) </head> 前插入 assets/hig.css（最后加载，统一覆盖各页旧样式）；
  2) vendor/echarts.min.js 之后插入 assets/hig-echarts.js（统一图表主题）；
  3) 页头左上角：首页显示品牌，其余页面统一成 "‹ 首页" 返回按钮（HIG 导航栏）。
模板（tpl/page.py、tpl/page_v2.py、explain/build.py、daily/publish.py、世界页 head.tpl）已直接输出同样的外壳；
本脚本兜底处理手写页面、冻结存档和其它流水线生成的页面。build.sh 在 cachebust 之前调用。
用法：python3 tools/hig_apply.py [html …]（不给参数 = 仓库里全部 HTML）"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_RE = re.compile(r'<a class="brand" href="([^"]*)"><b>●</b>\s*产业链情报(?:研究中心)?</a>')
EC_RE = re.compile(r'(<script src="((?:\.\./)*)vendor/echarts\.min\.js(?:\?v=[0-9a-f]+)?"( defer)?></script>)(?!<script src="(?:\.\./)*assets/hig-echarts\.js)')


def apply(path):
    rel = os.path.relpath(path, ROOT)
    up = '../' * rel.count('/')
    s = old = open(path, encoding='utf-8').read()
    if 'assets/hig.css' not in s and '</head>' in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="{up}assets/hig.css"></head>', 1)
    s = EC_RE.sub(lambda m: m.group(1) + f'<script src="{m.group(2)}assets/hig-echarts.js"{m.group(3) or ""}></script>', s)
    if rel != 'index.html':
        s = BRAND_RE.sub(lambda m: f'<a class="brand back" href="{m.group(1)}" aria-label="返回首页">首页</a>', s)
    if s != old:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def main(files):
    if not files:
        out = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout
        files = [os.path.join(ROOT, f) for f in out.split()]
    n = sum(apply(os.path.abspath(f)) for f in files if os.path.exists(f))
    print(f'hig_apply: {n} 个 HTML 已接入 assets/hig.css')


if __name__ == '__main__':
    main(sys.argv[1:])
