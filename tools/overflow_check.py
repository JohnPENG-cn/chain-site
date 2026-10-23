#!/usr/bin/env python3
"""阅读模式版面检查（docs/READING_MODE.md「验收」）。

对每个 <body class="article"> 页面，在 9 个宽度 × 2 个缩放（devicePixelRatio 1 / 1.25）下，
展开全部「展开细节」后检查：
  1. 页面没有横向滚动（scrollWidth ≤ 视口宽）；
  2. 正文里任何可见元素都没有超出视口（在自身横向滚动容器内的除外——那是允许的“表格内滚动”）；
  3. 左侧目录栏出现时，正文里的图、表、对比、细节块都不和目录栏横向重叠；
  4. 每张 ECharts 图：图宽不超过容器，图内文字不超出画布、文字之间不互相压住。
用法：python3 tools/overflow_check.py [--base URL] [--pages pcb.html ...] [--shots DIR]
不给 --base 时在仓库根目录起一个本地 http 服务。缺 playwright 时打印 SKIP 并返回 0。
"""
import argparse, functools, glob, http.server, json, os, re, socketserver, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTHS = [360, 390, 430, 768, 1024, 1180, 1280, 1440, 1920]
SCALES = [1, 1.25]   # 设备像素比：CSS 宽度不变，只换像素密度
# 另测「系统缩放 / 浏览器缩放 125%」：同一块屏幕，CSS 视口变成 宽/1.25（如 1920 屏 → 1536px），只对 ≥1024 的桌面宽度测
ZOOM = 1.25

JS = r"""
() => {
 const vw = document.documentElement.clientWidth, out = [];
 const d = e => { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id;
   else if (e.className && typeof e.className == 'string') s += '.' + e.className.trim().split(/\s+/).slice(0,2).join('.');
   const sec = e.closest('section[id]'); return (sec ? sec.id + ' › ' : '') + s };
 const vis = e => { const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return null;
   const cs = getComputedStyle(e); if (cs.visibility == 'hidden' || cs.display == 'none') return null; return r };
 const clipped = e => { for (let p = e.parentElement; p && p.tagName != 'MAIN'; p = p.parentElement) {
     const o = getComputedStyle(p).overflowX; if (o == 'auto' || o == 'scroll' || o == 'hidden') return p } return null };
 if (document.documentElement.scrollWidth > vw + 1) out.push({k:'hscroll', m:`scrollWidth ${document.documentElement.scrollWidth} > ${vw}`});
 const main = document.querySelector('main');
 // 2. 超出视口
 const seen = new Set();
 for (const e of main.querySelectorAll('*')) {
   if (e.closest('svg') && e.tagName.toLowerCase() != 'svg') continue;
   const r = vis(e); if (!r) continue;
   if (r.right <= vw + 1 && r.left >= -1) continue;
   const c = clipped(e); if (c) { const cr = c.getBoundingClientRect(); if (cr.right <= vw + 1 && cr.left >= -1) continue }
   const k = d(e); if (seen.has(k)) continue; seen.add(k);
   out.push({k:'viewport', m:`${k} [${Math.round(r.left)},${Math.round(r.right)}] vw=${vw}`});
 }
 // 3. 目录栏
 const rail = document.getElementById('rdToc'); let rr = null;
 if (rail) { const cs = getComputedStyle(rail); if (cs.display != 'none' && cs.position == 'fixed' && !rail.classList.contains('open')) rr = rail.getBoundingClientRect() }
 if (rail && rail.classList.contains('open') && vw >= 1200) { const cs = getComputedStyle(rail); if (cs.bottom == '0px') out.push({k:'rail', m:'open sheet at desktop'}) }
 if (rr && rr.width) {
   const B = 'figure,.chart,details.more,.tbl,table,.cmp,.stat-row,.lay,.bluf,.pull,p,h2,h3,ol,ul,.aside,.cols2';
   const seen2 = new Set();
   for (const e of main.querySelectorAll(B)) { const r = vis(e); if (!r) continue;
     if (r.left < rr.right + 8) { const k = d(e); if (seen2.has(k)) continue; seen2.add(k);
       out.push({k:'rail', m:`${k} left=${Math.round(r.left)} < rail.right ${Math.round(rr.right)}+8`}) } }
 }
 // 4. 图
 const charts = [];
 for (const el of document.querySelectorAll('[_echarts_instance_]')) {
   const cr = vis(el); if (!cr) continue; const svg = el.querySelector('svg'); if (!svg) { out.push({k:'chart', m:`${d(el)} no svg`}); continue }
   const sr = svg.getBoundingClientRect(); if (sr.width > cr.width + 1) out.push({k:'chart', m:`${d(el)} svg ${Math.round(sr.width)} > box ${Math.round(cr.width)}`});
   const T = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && getComputedStyle(t).opacity != '0' && t.getAttribute('fill-opacity') !== '0' && !t.closest('[opacity="0"]'))
     .map(t => ({t: t.textContent.trim(), r: t.getBoundingClientRect()})).filter(x => x.r.width > 0);
  // 关系图（graph）是可拖动、可缩放的力导向图，每次布局都不一样，节点名贴边或互相挨着属正常：只查 svg 不超容器，不查文字（见 docs/READING_MODE.md）
  let graph = false; try { graph = (echarts.getInstanceByDom(el).getOption().series || []).some(s => s.type == 'graph') } catch (e) {}
  let bad = [];
  if (!graph) for (const x of T) if (x.r.left < sr.left - 1 || x.r.right > sr.right + 1 || x.r.top < sr.top - 1 || x.r.bottom > sr.bottom + 1) bad.push(`clip「${x.t}」`);
  // 字形框上下各收 15%（行距留白），避免多行标签的相邻两行被误判
  const sh = r => ({left: r.left, right: r.right, top: r.top + r.height * .15, bottom: r.bottom - r.height * .15, width: r.width, height: r.height * .7});
  if (!graph) for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) { const a = sh(T[i].r), b = sh(T[j].r);
     const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
     if (ox > 2 && oy > 2 && ox * oy > 0.25 * Math.min(a.width * a.height, b.width * b.height)) bad.push(`「${T[i].t}」×「${T[j].t}」`) }
   if (bad.length) out.push({k:'label', m:`${d(el)}: ${bad.slice(0,6).join(' ')}${bad.length > 6 ? ' …+' + (bad.length - 6) : ''}`});
   charts.push(el.id);
 }
 return {vw, out, charts, rail: rr ? Math.round(rr.right) : null};
}
"""

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Q, directory=ROOT)
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{s.server_address[1]}/'

def article_pages():
    return sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html'))
                  if re.search(r'<body[^>]*class="[^"]*\barticle\b', open(f, encoding='utf-8').read()))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base'); ap.add_argument('--pages', nargs='*'); ap.add_argument('--shots')
    ap.add_argument('--widths', nargs='*', type=int); a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('overflow_check: SKIP（没装 playwright）'); return 0
    base = a.base or serve(); base = base if base.endswith('/') else base + '/'
    pages = a.pages or article_pages(); widths = a.widths or WIDTHS
    exe = next((p for p in ['/usr/bin/google-chrome', '/usr/bin/chromium'] if os.path.exists(p)), None)
    fails = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=['--no-sandbox']) if exe else p.chromium.launch()
        for pg_name in pages:
            for w in widths:
                runs = [(w, sc, f'×{sc}') for sc in SCALES] + ([(round(w / ZOOM), ZOOM, f'缩放{int(ZOOM*100)}%→{round(w / ZOOM)}px')] if w >= 1024 else [])
                for vw, sc, lab in runs:
                    mob = vw <= 430
                    ctx = b.new_context(viewport={'width': vw, 'height': 900}, device_scale_factor=sc * 2 if mob else sc,
                                        is_mobile=mob, has_touch=mob)
                    pg = ctx.new_page(); errs = []
                    pg.on('pageerror', lambda e: errs.append(str(e)))
                    pg.goto(base + pg_name, wait_until='networkidle'); pg.wait_for_timeout(1200)
                    pg.evaluate("document.querySelectorAll('main details').forEach(d=>d.open=true)")
                    pg.wait_for_timeout(900)
                    r = pg.evaluate(JS)
                    if r['out']:   # 图表动画 / 重排还没走完时可能误报：等 1.5 秒再测一次，只报两次都在的问题
                        pg.wait_for_timeout(1500); r = pg.evaluate(JS)
                    for e in errs: r['out'].append({'k': 'js', 'm': e})
                    tag = f'{pg_name} {w}px {lab}'
                    if r['out']:
                        fails += len(r['out'])
                        print(f'FAIL {tag}  rail={r["rail"]}')
                        for o in r['out'][:25]: print(f'   [{o["k"]}] {o["m"]}')
                        if len(r['out']) > 25: print(f'   … +{len(r["out"]) - 25}')
                    else:
                        print(f'ok   {tag}  charts={len(r["charts"])} rail={r["rail"]}')
                    ctx.close()
        b.close()
    print(f'overflow_check: {"PASS" if not fails else f"{fails} 处问题"}')
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
