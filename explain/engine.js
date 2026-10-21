/* 万物原理图 · 通用引擎（无依赖，原生 JS + SVG）
 * 交互范式参考 Anatomy（github.com/wheresryan22/anatomy，MIT，© 2026 Ryan）：
 * 等轴测实体 + 四档明暗 + 由后往前的绘制顺序；卡片四角“Fig 编号 / 标题 / 提示 / 实时读数”；
 * 图上每个数字都来自同一个小模型；缓动跟随目标值、尊重“减少动态效果”；触屏点按即生效、键盘可操作。
 * 本文件为自写实现，未复制 Anatomy 代码。
 * 用法：EX.mount({steps, gens, parts, scenes, widgets, readout})，各专题在自己的 js 里提供 scenes / widgets。
 */
(function () {
  'use strict';
  var C30 = Math.cos(Math.PI / 6), S30 = 0.5;
  function P(x, y, z) { return [(x - y) * C30, (x + y) * S30 - z]; }
  function f(n) { return Math.round(n * 10) / 10; }
  function pts(a) { return a.map(function (p) { return f(p[0]) + ',' + f(p[1]); }).join(' '); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  /* 等轴测长方体：x,y 在地面，z 向上。返回 {d: 绘制深度, s: svg}。
     可见三面：顶面（最亮）、朝 +y 的左前面、朝 +x 的右前面（两档侧光），外加描边（第四档）。 */
  function box(o) {
    var x = o.x, y = o.y, z = o.z || 0, w = o.w, d = o.d, h = o.h;
    var A = P(x, y, z + h), B = P(x + w, y, z + h), Cc = P(x + w, y + d, z + h), D = P(x, y + d, z + h);
    var E = P(x + w, y, z), F = P(x + w, y + d, z), G = P(x, y + d, z);
    var cls = 'b k-' + (o.k || 'dram') + (o.cls ? ' ' + o.cls : '');
    var s = '<g class="' + cls + '"' + (o.p ? ' data-p="' + o.p + '"' : '') + (o.op != null ? ' style="opacity:' + f(o.op * 100) / 100 + '"' : '') + '>' +
      '<polygon class="fl" points="' + pts([D, Cc, F, G]) + '"/>' +
      '<polygon class="fr" points="' + pts([B, Cc, F, E]) + '"/>' +
      '<polygon class="ft" points="' + pts([A, B, Cc, D]) + '"/>' + (o.inner || '') + '</g>';
    return { d: o.depth != null ? o.depth : (x + w / 2) + (y + d / 2) + z * 0.001, z: z, s: s };
  }
  /* 顶面上的一条线 / 一组点（细节：刻线、TSV 点阵、焊点） */
  function line3(a, b, cls, p) {
    var A = P(a[0], a[1], a[2]), B = P(b[0], b[1], b[2]);
    return '<line class="' + (cls || 'ln') + '"' + (p ? ' data-p="' + p + '"' : '') + ' x1="' + f(A[0]) + '" y1="' + f(A[1]) + '" x2="' + f(B[0]) + '" y2="' + f(B[1]) + '"/>';
  }
  function dot3(a, r, cls, p) {
    var A = P(a[0], a[1], a[2]);
    return '<circle class="' + (cls || 'dt') + '"' + (p ? ' data-p="' + p + '"' : '') + ' cx="' + f(A[0]) + '" cy="' + f(A[1]) + '" r="' + r + '"/>';
  }
  function poly3(arr, cls, p) {
    return '<polygon class="' + cls + '"' + (p ? ' data-p="' + p + '"' : '') + ' points="' + pts(arr.map(function (a) { return P(a[0], a[1], a[2]); })) + '"/>';
  }
  /* 由后往前排序（深度相同时先画低的） */
  function paint(items) {
    items.sort(function (a, b) { return (a.d - b.d) || (a.z - b.z); });
    return items.map(function (i) { return i.s; }).join('');
  }
  /* 根据一组世界坐标点算 viewBox */
  function fit(points, pad) {
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    points.forEach(function (p) { var q = P(p[0], p[1], p[2] || 0); x0 = Math.min(x0, q[0]); y0 = Math.min(y0, q[1]); x1 = Math.max(x1, q[0]); y1 = Math.max(y1, q[1]); });
    pad = pad || 10;
    return [f(x0 - pad), f(y0 - pad), f(x1 - x0 + 2 * pad), f(y1 - y0 + 2 * pad)];
  }

  var still = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };

  function mount(cfg) {
    var steps = cfg.steps, gens = cfg.gens, parts = cfg.parts || {};
    var root = document.getElementById('ex');
    var stage = root.querySelector('.ex-stage'), svg = stage.querySelector('svg');
    var info = root.querySelector('.ex-info'), chips = root.querySelector('.ex-chips');
    var figN = root.querySelector('.ex-n'), figT = root.querySelector('.ex-t'), hint = root.querySelector('.ex-hint'), ro = root.querySelector('.ex-ro');
    var genIn = root.querySelector('.ex-gen input'), genL = root.querySelector('.ex-gen output');
    var spdB = root.querySelectorAll('.ex-spd button');
    var secs = [].slice.call(document.querySelectorAll('.ex-step'));
    var pager = root.querySelector('.ex-pg b');

    /* 状态：目标值 + 缓动值（同一个模型驱动图形与读数） */
    var st = { i: -1, g: +(genIn ? genIn.value : 0), spd: 'prod', sel: null, v: {}, tgt: {} };
    var api = {
      st: st, gen: function () { return gens[st.g]; },
      speed: function (g) { g = g || gens[st.g]; return st.spd === 'std' ? g.std : g.prod; },
      bw: function (g) { g = g || gens[st.g]; return g.io * api.speed(g) / 8; },
      set: function (k, val, jump) { st.tgt[k] = val; if (jump || st.v[k] == null || still.matches) st.v[k] = val; kick(); },
      val: function (k, def) { return st.v[k] == null ? def : st.v[k]; },
      update: function () { kick(); },
      setGen: setGen, select: select, box: box, line3: line3, dot3: dot3, poly3: poly3, paint: paint, fit: fit, P: P, f: f
    };
    window.EXapi = api;

    function setGen(g) {
      st.g = Math.max(0, Math.min(gens.length - 1, g));
      if (genIn) { genIn.value = st.g; genIn.setAttribute('aria-valuetext', gens[st.g].name); }
      if (genL) genL.textContent = gens[st.g].name;
      if (cfg.onGen) cfg.onGen(api);
      document.dispatchEvent(new CustomEvent('exgen', { detail: st.g }));
      kick();
    }
    if (genIn) genIn.addEventListener('input', function () { setGen(+genIn.value); });
    [].forEach.call(spdB, function (b) {
      b.addEventListener('click', function () {
        st.spd = b.dataset.s; [].forEach.call(spdB, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        document.dispatchEvent(new CustomEvent('exgen', { detail: st.g })); kick();
      });
    });

    /* 部件说明：点图中部件或下方标签 → 高亮 + 说明（触屏可用，不依赖悬停） */
    function select(p) {
      st.sel = (p && parts[p]) ? p : null;
      [].forEach.call(chips.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b.dataset.p === st.sel ? 'true' : 'false'); });
      if (st.sel) { var pt = parts[st.sel]; info.innerHTML = '<b>' + pt.n + '</b>　' + (typeof pt.d === 'function' ? pt.d(api) : pt.d); info.classList.add('on'); }
      else { info.innerHTML = steps[st.i] ? '点图中的部件，或点下面的标签看说明' : ''; info.classList.remove('on'); }
      draw();
    }
    svg.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('[data-p]');
      select(t && t.dataset.p !== st.sel ? t.dataset.p : null);
    });
    chips.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      select(b.dataset.p === st.sel ? null : b.dataset.p);
    });

    function setStep(i) {
      if (i === st.i || i < 0 || i >= steps.length) return;
      st.i = i; var s = steps[i];
      figN.textContent = 'Fig ' + (i + 1); figT.textContent = s.t; hint.textContent = s.hint || '';
      if (pager) pager.textContent = (i + 1) + ' / ' + steps.length;
      chips.innerHTML = (s.parts || []).filter(function (p) { return parts[p]; }).map(function (p, k) {
        return '<button type="button" data-p="' + p + '" aria-pressed="false"><i>' + (k + 1) + '</i>' + parts[p].n + '</button>';
      }).join('');
      secs.forEach(function (el, k) { el.classList.toggle('act', k === i); });
      document.querySelectorAll('.ex-dots a').forEach(function (a, k) { a.classList.toggle('act', k === i); });
      st.sel = null; select(null);
      if (cfg.onStep) cfg.onStep(api, s);
      kick();
    }
    api.setStep = setStep;

    /* 动画循环：缓动所有数值到目标；停稳后停止 */
    var frame = 0, last = 0;
    function tick(now) {
      var dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60; last = now;
      var moving = false;
      Object.keys(st.tgt).forEach(function (k) {
        var t = st.tgt[k], v = st.v[k];
        if (v == null || still.matches) { st.v[k] = t; return; }
        var nv = v + (t - v) * (1 - Math.exp(-dt / 0.22));
        if (Math.abs(nv - t) < 1e-3 * Math.max(1, Math.abs(t))) nv = t; else moving = true;
        st.v[k] = nv;
      });
      draw();
      frame = moving ? requestAnimationFrame(tick) : 0;
      if (!frame) last = 0;
    }
    function kick() { if (!frame) frame = requestAnimationFrame(tick); }

    function draw() {
      var s = steps[st.i]; if (!s) return;
      var sc = cfg.scenes[s.scene]; if (!sc) return;
      var out = sc(api, s);
      svg.setAttribute('viewBox', out.vb.join(' '));
      svg.setAttribute('data-sc', s.scene);
      svg.innerHTML = out.svg;
      if (st.sel) [].forEach.call(svg.querySelectorAll('[data-p="' + st.sel + '"]'), function (n) { n.classList.add('sel'); });
      svg.classList.toggle('has-sel', !!st.sel);
      ro.textContent = cfg.readout ? cfg.readout(api, s) : '';
    }
    window.redraw = draw;

    /* 步骤切换：滚动到哪一步，图就切到哪一步（滚动叙事）；也可点按钮、圆点、键盘左右键 */
    function figBottom() { var r = root.getBoundingClientRect(); return getComputedStyle(root).position === 'sticky' && innerWidth < 900 ? r.bottom : 60; }
    function onScroll() {
      var y = innerWidth < 900 ? figBottom() + (innerHeight - figBottom()) * 0.35 : innerHeight * 0.45, cur = 0;
      secs.forEach(function (el, k) { if (el.getBoundingClientRect().top < y) cur = k; });
      setStep(cur);
    }
    var ticking = false;
    addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; onScroll(); }); } }, { passive: true });
    addEventListener('resize', onScroll);
    function go(i) {
      i = Math.max(0, Math.min(steps.length - 1, i));
      var el = secs[i], off = innerWidth < 900 ? figBottom() + 8 : 80;
      var top = el.getBoundingClientRect().top + scrollY - off;
      scrollTo({ top: top, behavior: still.matches ? 'auto' : 'smooth' });
      setStep(i);
    }
    api.go = go;
    root.querySelector('.ex-prev').addEventListener('click', function () { go(st.i - 1); });
    root.querySelector('.ex-next').addEventListener('click', function () { go(st.i + 1); });
    document.querySelectorAll('.ex-dots a').forEach(function (a, k) { a.addEventListener('click', function (e) { e.preventDefault(); go(k); }); });
    addEventListener('keydown', function (e) {
      var tg = e.target.tagName; if (tg === 'INPUT' || tg === 'TEXTAREA' || e.metaKey || e.ctrlKey) return;
      if (e.key === 'ArrowRight' || e.key === 'j') { go(st.i + 1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft' || e.key === 'k') { go(st.i - 1); e.preventDefault(); }
      else if (e.key === 'Escape') select(null);
    });
    /* 左右轻扫图卡也能翻步（触屏） */
    var sx = null, sy = null;
    stage.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (sx == null) return; var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; sx = null;
      if (Math.abs(dx) > 60 && Math.abs(dx) > 2 * Math.abs(dy)) go(st.i + (dx < 0 ? 1 : -1));
    }, { passive: true });

    /* 步内小部件 */
    document.querySelectorAll('.ex-w').forEach(function (el) {
      var w = cfg.widgets && cfg.widgets[el.dataset.w];
      if (w) w(el, api);
    });
    setGen(st.g);
    onScroll(); if (st.i < 0) setStep(0);
    return api;
  }

  window.EX = { mount: mount, P: P, box: box, line3: line3, dot3: dot3, poly3: poly3, paint: paint, fit: fit, esc: esc };
})();
