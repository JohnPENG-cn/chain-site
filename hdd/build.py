#!/usr/bin/env python3
"""HDD 五页（2026-10-30 起）：hdd.html 总览 / hdd-pattern / hdd-cycle / hdd-track / hdd-data。
外壳 = tpl/page_v4.py 的 assemble（与 HBM / CoWoS / PCB / 铜同一套）；正文在 hdd/content.py，来源表在 hdd/sources.py；
数字来自 hdd_data/quarterly.json（SEC XBRL，hdd_data/xbrl.py）和 hdd_data/stx_eb.json（希捷 10-Q / 10-K，hdd_data/stx_eb.py），代码现算。
本页不写入总账：建议判断只列在 hdd-track.html#propose「待 John 确认」。"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tpl')); sys.path.insert(0, os.path.join(ROOT, 'hdd'))
os.chdir(ROOT)
import page_v4 as T
import article as A
import content as C
from sources import TITLES

T.use('hdd')
T.SRC_NOTE = 'hdd/content.py + hdd/sources.py + hdd_data/*.json'
SECS = C.build(A, TITLES)
dq = dict(stx=C.Q['stx'], wdc=[r for r in C.Q['wdc'] if r['end'] >= '2023-09'], eb=C.EB, pk=C.gm_pk['gm'])
tail = '<script>window.HDDQ=' + json.dumps(dq, ensure_ascii=False, separators=(',', ':')) + '</script><script src="hdd.js"></script>'
out, STAT, _ = T.assemble(SECS, TITLES, C.H1, title0=C.TITLE0, desc0=C.DESC0, stub='',
                          scripts='<script src="assets/reading.js"></script>', tail=tail,
                          foot='<a href="explain-hdd.html">原理图：硬盘怎么存</a>')
for fn, h in out.items():
    open(fn, 'w', encoding='utf-8').write(h)
print('HDD 5 页：' + '；'.join(f'{k} 脚注 {v["fn_main"]}、标签 {v["labels"]}、来源 {v["refs"]}' for k, v in STAT.items()))
