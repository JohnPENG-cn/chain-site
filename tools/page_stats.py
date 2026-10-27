#!/usr/bin/env python3
"""页面体量统计（docs/CHAIN_TEMPLATE.md「验收」）：每页可见字数（默认收起 / 全部展开）、手机 390px 高度与屏数、脚注上标数、表格数、图数。
只统计 <main> 里看得见的内容（隐藏的 #ch-shadow 不算）。用法：python3 tools/page_stats.py pcb.html pcb-pattern.html …"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overflow_check import serve

JS = r"""(open) => {
 if (open) document.querySelectorAll('main details').forEach(d => d.open = true);
 const m = document.querySelector('main');
 const vis = e => { for (let d = e.closest('details:not([open])'); d; d = d.parentElement && d.parentElement.closest('details:not([open])')) { const sm = d.querySelector(':scope>summary'); if (!(sm && sm.contains(e))) return false }
   const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 };
 const txt = m.innerText.replace(/\s+/g, '');
 return {chars: txt.length, h: document.documentElement.scrollHeight,
   fn: [...m.querySelectorAll('sup.fn a.fn-a')].filter(vis).length,
   fnAll: m.querySelectorAll('sup.fn a.fn-a').length,
   tables: [...m.querySelectorAll('table')].filter(vis).length,
   charts: [...m.querySelectorAll('[_echarts_instance_]')].filter(vis).length}
}"""

def main(pages):
    from playwright.sync_api import sync_playwright
    base = serve(); res = {}
    exe = next((p for p in ['/usr/bin/google-chrome', '/usr/bin/chromium'] if os.path.exists(p)), None)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=['--no-sandbox']) if exe else p.chromium.launch()
        for pg_name in pages:
            ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page(); pg.goto(base + pg_name, wait_until='networkidle'); pg.wait_for_timeout(1500)
            a = pg.evaluate(JS, False); z = pg.evaluate(JS, True)
            res[pg_name] = dict(chars=a['chars'], chars_open=z['chars'], h390=a['h'], screens=round(a['h'] / 844, 1), h390_open=z['h'],
                                fn_default=a['fn'], fn_open=z['fn'], fn_dom=z['fnAll'], tables=a['tables'], tables_open=z['tables'], charts=a['charts'], charts_open=z['charts'])
            ctx.close()
        b.close()
    print(json.dumps(res, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main(sys.argv[1:] or ['pcb.html'])
