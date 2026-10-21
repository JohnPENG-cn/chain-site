/* 万物原理图 · CoWoS：部件说明、场景（等轴测 + 剖面 SVG）、步内小部件、实时读数。
 * 数据（产品、步骤文字、来源）由 explain/build.py 从 explain/cowos.py 注入为 window.EXD。
 * 图中尺寸与层厚为示意（不按比例）；晶圆摆放个数按矩形几何现算（推算）。 */
(function () {
  'use strict';
  var D = window.EXD, G = D.gens, E = window.EX;
  function R(n) { return '<a class="sr" href="#src' + n + '">[' + n + ']</a>'; }
  function num(v, dp) { return (+v).toLocaleString('en-US', { maximumFractionDigits: dp == null ? 0 : dp, minimumFractionDigits: dp || 0 }); }
  var EST = ' <span class="tag t-est">估</span>', CALC = ' <span class="tag t-est">推算</span>';
  var VN = ['S', 'R', 'L'];

  /* ---------- 部件：名称 + 一句话说明 ---------- */
  var PARTS = {
    reticle: { n: '光罩上限', d: '光刻机一次能曝光的最大面积，理论最大约 858 mm² ' + R(5) + '。单颗芯片不能比它大。' },
    die: { n: '计算芯片', d: function (a) { var g = a.gen(); return g.dies === 1 ? 'H100：一颗 814 mm² 的芯片，离光罩上限只差约 5% ' + R(5) : g.name + '：' + g.dies + ' 颗大芯片拼成一颗 GPU' + (g.dies === 2 ? '，片间 10 TB/s ' + R(6) : '，每颗约 800 mm² ' + R(10)); } },
    lorg: { n: '普通封装走线', d: '有机基板上的走线：最长约 25 mm，每传 1 位约 0.5–1 pJ ' + R(12) + '，线也排不密。' },
    ladv: { n: '先进封装短线', d: '硅中介层或硅桥上的走线：2 mm 以内，每位约 0.25–0.5 pJ ' + R(12) + '，线可以排得很密。' },
    pcb: { n: '主板 / 加速卡 PCB', d: '最底下的电路板，走电源和对外高速线。PCB 怎么做见本站 <a href="pcb.html">PCB 研究页</a>。' },
    bga: { n: 'BGA 焊球', d: '封装底部的锡球阵列，把整个封装焊到电路板上。' },
    abf: { n: 'ABF 封装载板', d: function (a) { return '十几层 ABF 绝缘膜 + 铜线 + 玻纤芯层的小电路板 ' + R(23) + R(22) + '，把中介层的密集连接放大到电路板能接的间距。5.5× 封装要用 >100×100 mm 的载板 ' + R(4) + '。研究页模型：2027 年最紧的一环，约比需求少 29%' + EST + R(16); } },
    c4: { n: 'C4 凸点', d: '中介层和载板之间的焊点。R / L 型的 RDL 层能缓冲芯片与载板热胀冷缩不一致带来的应力 ' + R(1) + '。' },
    interp: { n: '中介层', d: function (a) { return a.gen().var === 'S' ? 'CoWoS-S 硅中介层：整片硅，TSV + 多层 RDL + 深沟槽电容；最大约 3.3× 光罩（约 2,700 mm²）' + R(1) : 'CoWoS-L 中介层：模塑料 + 正反面 RDL，只在芯片接缝下面埋 LSI 硅桥 ' + R(1) + '；研究页口径每片约 1.5 万美元' + R(16); } },
    ubump: { n: '微凸点', d: '芯片和中介层之间的极小焊点，数以万计；贴上去就拆不下来，坏一处整颗封装可能报废。' },
    gpu: { n: 'GPU 计算芯片', d: function (a) { var g = a.gen(); return g.name + '（' + g.arch + '）：' + g.dies + ' 颗计算芯片；功耗 ' + g.tgpT; } },
    hbm: { n: 'HBM 堆栈', d: function (a) { var g = a.gen(); return g.name + '：' + g.mem + '，带宽 ' + g.bw + '。HBM 怎么叠起来见 <a href="explain-hbm.html">HBM 原理图</a>。'; } },
    uf: { n: '底部填充胶', d: '灌进芯片和中介层之间的缝里，把微凸点包住，防止热胀冷缩把焊点扯断。' },
    lid: { n: '盖板 / 导热', d: '芯片顶上涂导热材料、盖金属盖，再接冷板。B300 最高 1,400W ' + R(7) + '，热全从这里走。（半透明示意）' },
    si: { n: '硅中介层（S）', d: '整块硅，TSV 打穿、RDL 线最细；2012 年量产，最大约 3.3× 光罩（约 2,700 mm²）' + R(1) },
    tsv: { n: 'TSV 硅通孔', d: '竖直打穿硅中介层的铜柱，把上面芯片的信号和电送到下面的 C4 凸点。' },
    rdl: { n: 'RDL 布线层', d: '一层层横向铜线 + 绝缘层，负责“左右连”。R 型 RDL 最细线宽 / 间距 2 µm ' + R(1) + '。' },
    lsi: { n: 'LSI 硅桥', d: '局部硅互连：只在芯片—芯片、芯片—HBM 的接缝下面埋一小块硅，线宽亚微米、规格与 S 型一致 ' + R(1) + '。' },
    mold: { n: '模塑中介层（L）', d: 'L 型中介层的主体：模塑料 + 正反两面较宽的 RDL，走电源和高频信号损耗低 ' + R(1) + '；图中竖线为上下连通的铜柱（示意）。' },
    wafer: { n: '300 mm 圆片', d: '中介层晶圆，面积 π × 150² ≈ 70,686 mm²' + CALC + '。边缘切不出完整的大矩形。' },
    site: { n: '一个中介层位置', d: function (a) { return '一颗封装占一个位置。研究页口径：H100 每片约 28 颗、B200 约 16 颗 ' + R(16) + '；当前 ' + a.gen().name + '：' + a.gen().ppw; } },
    panel: { n: 'CoPoS 方形面板', d: '310 × 310 mm 方片 ' + R(17) + '，面积 96,100 mm²，约为圆片的 1.36 倍' + CALC + '，大矩形摆得更满。' },
    probe: { n: '测试', d: 'Blackwell 的测试时间是 Hopper 的 3–4 倍：每颗要在不同机台上测几十次 ' + R(13) + '。' },
    b_ip: { n: '硅中介层', d: '研究页模型：2027 年按封装颗数约 +2%（S 型口径约 +3%），只卡用整片硅的 S 型' + EST + R(16) + ' → <a href="cowos.html#ip">中介层一环</a>' },
    b_cw: { n: 'CoWoS 封装产能', d: '台积电年末产能约 12 万（2026）→ 18.5 万片/月（2027）；2027 年余量 −8%～+7%' + EST + R(16) + ' → <a href="cowos.html#cw-toc">TOC 图</a>' },
    b_hbm: { n: 'HBM', d: '2027 年约比需求少 11%' + EST + R(16) + '。HBM 本身怎么造见 <a href="explain-hbm.html">HBM 原理图</a>。' },
    b_abf: { n: 'ABF 载板', d: '2027 年约比需求少 29%，是模型里最紧的一环' + EST + R(16) + '；T-glass 日东纺约占 90% ' + R(22) + '，味之素 ABF 提价 ' + R(23) + ' → <a href="cowos.html#neck">瓶颈表</a>' },
    test: { n: '测试', d: 'Blackwell 测试时间是 Hopper 的 3–4 倍 ' + R(13) + '；研究页：台积电称测试机也短缺，测试产能无公开数据（数据缺口）' + R(16) },
    pwr: { n: '功耗与散热', d: '最大功耗 H100 700W → Blackwell 1,200W → Blackwell Ultra 1,400W ' + R(7) + '；Rubin Ultra 整柜约 600 kW ' + R(11) + '。研究页：2028 年约束可能轮到数据中心电力' + EST + R(16) },
    soic: { n: 'SoIC 3D 堆叠', d: '芯片叠芯片、铜对铜直接键合；台积电 2026 年月产能约 1–1.5 万片 ' + R(19) + '，A14 叠 A14 计划 2029 年 ' + R(2) + '。' },
    glass: { n: '玻璃基板', d: '载板芯层换成玻璃：更平、不怕热胀冷缩；预计 2027 年起步、2030 年前后放量 ' + R(18) + '。' },
    cpo: { n: '共封装光学', d: '光引擎放进封装：台积电 COUPE 2026 年量产，能效约 2 倍、延迟约 1/10（对比可插拔光模块）' + R(2) + '。' },
    cn: { n: '国产 2.5D', d: '研究页中国账本：国产 2.5D 产能 2026 年底约 2.3 万片/月、2027 年底约 5 万（估，来源较弱）' + R(16) + '；台积电 2024-11 起停供 ' + R(20) + '。' }
  };

  /* ---------- 布局模型：一颗封装的平面摆放（单位约等于 mm，示意） ---------- */
  var DW = 26, DDp = 33, HW = 8, HD = 11, GP = 1.5, MG = 3;
  function lay(g) {
    var n = g.dies, Lx = n * DW + (n - 1) * GP, k = g.hbm / 2, dies = [], hbms = [];
    for (var i = 0; i < n; i++) dies.push({ x: i * (DW + GP), y: 0, w: DW, d: DDp });
    for (var j = 0; j < k; j++) {
      var x = k > 1 ? j * (Lx - HW) / (k - 1) : (Lx - HW) / 2;
      hbms.push({ x: x, y: -GP - HD, w: HW, d: HD, on: true });
      hbms.push({ x: x, y: DDp + GP, w: HW, d: HD, on: !(g.hbmOn < g.hbm && j === k - 1) });
    }
    var ip = { x: -MG, y: -GP - HD - MG, w: Lx + 2 * MG, d: DDp + 2 * GP + 2 * HD + 2 * MG };
    return { dies: dies, hbms: hbms, ip: ip, Lx: Lx };
  }
  function grow(r, m) { return { x: r.x - m, y: r.y - m, w: r.w + 2 * m, d: r.d + 2 * m }; }
  /* 接缝处的 LSI 硅桥位置 */
  function bridges(L) {
    var b = [];
    for (var i = 0; i < L.dies.length - 1; i++) b.push({ x: L.dies[i].x + DW - 4, y: 6, w: 8 + GP, d: DDp - 12 });
    L.hbms.forEach(function (h) { b.push({ x: h.x + 1.5, y: h.y < 0 ? -GP - 3 : DDp - 3, w: HW - 3, d: GP + 6 }); });
    return b;
  }

  /* ---------- 封装（等轴测）：从主板到盖板，逐层由下往上 ---------- */
  function pkg(a, o) {
    var g = a.gen(), L = lay(g), ap = o.ap || 0, neck = o.neck || {}, s = '', pts = [];
    var sub = grow(L.ip, 16), pcb = grow(sub, 14), vr = o.vr || g.var;
    var e1 = 0.8 + 9 * ap, e2 = 0.6 + 9 * ap, e3 = 0.4 + 9 * ap, z = 0;
    function grid(r, z0, step, cls, p, inset) {
      var out = '';
      for (var x = r.x + inset; x <= r.x + r.w - inset + 1e-6; x += step) for (var y = r.y + inset; y <= r.y + r.d - inset + 1e-6; y += step) out += E.dot3([x, y, z0], cls === 'bga' ? 1.3 : cls === 'c4' ? 0.9 : 0.55, 'bmp ' + cls, p);
      return out;
    }
    if (o.pcb) {
      s += E.box({ x: pcb.x, y: pcb.y, z: 0, w: pcb.w, d: pcb.d, h: 2, k: 'pcb', p: 'pcb' }).s;
      z = 2;
      if (ap > 0.05) s += '<g style="opacity:' + Math.min(1, ap * 3).toFixed(2) + '">' + grid(sub, z + e1 / 2, 9, 'bga', 'bga', 4) + '</g>';
      z += e1;
    }
    var zs = z;
    var cap = '';
    for (var c = 0; c < 8; c++) cap += E.box({ x: sub.x + 6 + c * (sub.w - 16) / 7, y: sub.y + sub.d - 6, z: zs + 3, w: 3.5, d: 2.2, h: 1.4, k: 'cap', p: 'abf' }).s;
    s += E.box({ x: sub.x, y: sub.y, z: zs, w: sub.w, d: sub.d, h: 3, k: 'sub', p: 'abf', cls: neck.abf ? 'neck' : '' }).s + cap;
    z = zs + 3;
    if (ap > 0.05) s += '<g style="opacity:' + Math.min(1, ap * 3).toFixed(2) + '">' + grid(L.ip, z + e2 / 2, 6, 'c4', 'c4', 2) + '</g>';
    z += e2;
    var zi = z, it = '';
    var kI = vr === 'S' ? 'interp' : vr === 'R' ? 'rdl' : 'mold';
    s += E.box({ x: L.ip.x, y: L.ip.y, z: zi, w: L.ip.w, d: L.ip.d, h: 1.6, k: kI, p: 'interp', cls: neck.interp ? 'neck' : '' }).s;
    if (vr === 'L') bridges(L).forEach(function (b) { it += E.box({ x: b.x, y: b.y, z: zi + 1.6, w: b.w, d: b.d, h: 0.35, k: 'logic', p: 'lsi' }).s; });
    // 中介层顶面走线（HBM → 芯片，示意）
    L.hbms.forEach(function (h) {
      var top = h.y < 0, y0 = top ? h.y + h.d : h.y, y1 = top ? 0 : DDp;
      for (var q = 1; q < 4; q++) it += E.line3([h.x + q * h.w / 4, y0, zi + 1.6], [h.x + q * h.w / 4, y1, zi + 1.6], 'trace', 'interp');
    });
    s += it;
    z = zi + 1.6;
    if (ap > 0.05) {
      var ub = '';
      L.dies.forEach(function (d) { ub += grid(d, z + e3 / 2, 4, 'ub', 'ubump', 2); });
      L.hbms.forEach(function (h) { ub += grid(h, z + e3 / 2, 3.5, 'ub', 'ubump', 1.5); });
      s += '<g style="opacity:' + Math.min(1, ap * 3).toFixed(2) + '">' + ub + '</g>';
    }
    // 底部填充胶：在微凸点那一层（压紧时正好填满缝）
    var uz = z + (e3 - 0.4) * 0.5, uf = [];
    L.dies.concat(L.hbms).forEach(function (r) { var q = grow(r, 0.8); uf.push(E.box({ x: q.x, y: q.y, z: uz, w: q.w, d: q.d, h: 0.4, k: 'uf', p: 'uf' })); });
    s += E.paint(uf);
    z += e3;
    var zc = z, chips = [];
    L.dies.forEach(function (d) {
      var gi = '';
      for (var u = 1; u < 4; u++) gi += E.line3([d.x + u * d.w / 4, d.y + 3, zc + 2.4], [d.x + u * d.w / 4, d.y + d.d - 3, zc + 2.4], 'grv', 'gpu');
      chips.push(E.box({ x: d.x, y: d.y, z: zc, w: d.w, d: d.d, h: 2.4, k: 'gpu', p: 'gpu', inner: gi, cls: neck.gpu ? 'neck' : '' }));
    });
    L.hbms.forEach(function (h) {
      var hi = '';
      for (var l = 1; l < 4; l++) hi += E.line3([h.x, h.y + h.d, zc + l * 0.6], [h.x + h.w, h.y + h.d, zc + l * 0.6], 'grv', 'hbm');
      chips.push(E.box({ x: h.x, y: h.y, z: zc, w: h.w, d: h.d, h: 2.4, k: h.on ? 'dram' : 'dram2', p: 'hbm', inner: hi, op: h.on ? 1 : 0.45, cls: neck.hbm && h.on ? 'neck' : '' }));
    });
    s += E.paint(chips);
    z = zc + 2.4;
    if (o.heat) {
      var n = g.tgp ? Math.round(g.tgp / 350) : 0, cx = L.Lx / 2, hw = '';
      for (var h2 = 0; h2 < n; h2++) {
        var P0 = E.P(cx - (n - 1) * 5 + h2 * 10, DDp / 2, z + 2);
        hw += '<path class="heatw" d="M' + P0[0].toFixed(1) + ' ' + P0[1].toFixed(1) + ' q4 -5 0 -10 t0 -10"/>';
      }
      var Pt = E.P(cx, DDp / 2, z + 2);
      if (!g.tgp) hw += '<text class="ax" x="' + Pt[0].toFixed(1) + '" y="' + (Pt[1] - 8).toFixed(1) + '" text-anchor="middle">功耗未公布</text>';
      else hw += '<text class="ax" x="' + (Pt[0] + n * 6 + 6).toFixed(1) + '" y="' + (Pt[1] - 10).toFixed(1) + '">≤' + num(g.tgp) + 'W</text>';
      s += '<g data-p="gpu">' + hw + '</g>';
    }
    if (o.lid) {
      var lz = z + 0.3 + 12 * ap, lr = grow(L.ip, 2);
      s += E.box({ x: lr.x, y: lr.y, z: lz, w: lr.w, d: lr.d, h: 1, k: 'lid', p: 'lid', op: 0.16 + 0.3 * ap }).s;
      z = lz + 1;
    }
    var base = o.pcb ? pcb : sub;
    pts.push([base.x, base.y, 0], [base.x + base.w, base.y + base.d, 0], [base.x, base.y + base.d, 0], [base.x + base.w, base.y, 0], [L.ip.x, L.ip.y, z + (o.heat ? 24 : 2)]);
    return { s: s, pts: pts };
  }

  /* ---------- 晶圆 / 面板上能摆几个矩形（几何上限，推算） ---------- */
  var tcache = {};
  function tiles(w, h, shape) {
    var key = w.toFixed(1) + 'x' + h.toFixed(1) + shape;
    if (tcache[key]) return tcache[key];
    var best = [], ex = 3, sc = 2;
    function inside(x, y) {
      if (shape === 'panel') return x >= -155 + ex && x <= 155 - ex && y >= -155 + ex && y <= 155 - ex;
      return x * x + y * y <= (150 - ex) * (150 - ex);
    }
    [[w, h], [h, w]].forEach(function (wh) {
      var tw = wh[0], th = wh[1], px = tw + sc, py = th + sc;
      for (var ox = 0; ox < 1; ox += 0.25) for (var oy = 0; oy < 1; oy += 0.25) {
        var out = [];
        for (var x = -160 + ox * px; x + tw <= 160; x += px) for (var y = -160 + oy * py; y + th <= 160; y += py) {
          if (inside(x, y) && inside(x + tw, y) && inside(x, y + th) && inside(x + tw, y + th)) out.push([x, y, tw, th]);
        }
        if (out.length > best.length) best = out;
      }
    });
    tcache[key] = best;
    return best;
  }
  function tileDims(m) { var A = m * 858, w = Math.sqrt(A * 1.25); return [w, A / w]; }

  /* ---------- 场景 ---------- */
  var SC = {};
  SC.why = function (a) {
    var g = a.gen(), s = '', k = 2.9, rx = 14, ry = 20, rw = 26 * k, rh = 33 * k;
    s += '<g data-p="reticle"><rect class="ret" x="' + rx + '" y="' + ry + '" width="' + rw + '" height="' + rh + '"/><text class="ax" x="' + rx + '" y="' + (ry - 6) + '">光罩上限 858 mm²</text></g>';
    var f = Math.sqrt(814 / 858), dw = rw * f, dh = rh * f;
    s += '<g data-p="die"><rect class="sdie" x="' + (rx + (rw - dw) / 2).toFixed(1) + '" y="' + (ry + (rh - dh) / 2).toFixed(1) + '" width="' + dw.toFixed(1) + '" height="' + dh.toFixed(1) + '"/><text class="ax" x="' + (rx + rw / 2) + '" y="' + (ry + rh / 2 + 3) + '" text-anchor="middle">H100 814</text></g>';
    // 右边：当前产品的平面图（俯视，示意）
    var L = lay(g), bx = 118, by = 14, bw = 196, bh = 104, sc = Math.min(bw / L.ip.w, bh / L.ip.d);
    var ox = bx + (bw - L.ip.w * sc) / 2 - L.ip.x * sc, oy = by + (bh - L.ip.d * sc) / 2 - L.ip.y * sc;
    function rr(r, cls, p, op) { return '<rect class="' + cls + '" data-p="' + p + '"' + (op != null ? ' style="opacity:' + op + '"' : '') + ' x="' + (ox + r.x * sc).toFixed(1) + '" y="' + (oy + r.y * sc).toFixed(1) + '" width="' + (r.w * sc).toFixed(1) + '" height="' + (r.d * sc).toFixed(1) + '" rx="1"/>'; }
    s += rr(L.ip, 'pip', 'ladv');
    L.dies.forEach(function (d) { s += rr(d, 'sdie', 'die'); });
    L.hbms.forEach(function (h) { s += rr(h, 'shbm', 'ladv', h.on ? null : 0.4); });
    s += '<text class="ax" x="' + (bx + bw / 2) + '" y="' + (by + bh + 12) + '" text-anchor="middle">' + g.name + '：' + g.dies + ' 颗芯片 + ' + g.hbm + ' 个 HBM 位置（俯视示意）</text>';
    // 下方：两种连线
    var y1 = 160, y2 = 196;
    s += '<g data-p="lorg"><rect class="sdie" x="14" y="' + (y1 - 9) + '" width="22" height="18"/><rect class="shbm" x="' + (36 + 200) + '" y="' + (y1 - 9) + '" width="16" height="18"/>';
    for (var i = 0; i < 3; i++) s += '<line class="lk" x1="36" x2="236" y1="' + (y1 - 5 + i * 5) + '" y2="' + (y1 - 5 + i * 5) + '"/>';
    s += '<text class="ax" x="258" y="' + (y1 + 3) + '">≤25 mm</text><text class="ax lbl" x="40" y="' + (y1 - 12) + '">普通封装（有机基板）0.5–1 pJ/bit</text></g>';
    s += '<g data-p="ladv"><rect class="sdie" x="14" y="' + (y2 - 9) + '" width="22" height="18"/><rect class="shbm" x="' + (36 + 16) + '" y="' + (y2 - 9) + '" width="16" height="18"/>';
    for (i = 0; i < 9; i++) s += '<line class="lk2" x1="36" x2="52" y1="' + (y2 - 8 + i * 2) + '" y2="' + (y2 - 8 + i * 2) + '"/>';
    s += '<text class="ax" x="74" y="' + (y2 + 3) + '">≤2 mm · 0.25–0.5 pJ/bit · 线更密</text><text class="ax lbl" x="40" y="' + (y2 - 12) + '">先进封装（中介层 / 硅桥）</text></g>';
    return { vb: [0, 0, 320, 212], svg: s };
  };

  SC.stack = function (a) {
    var r = pkg(a, { ap: a.val('apart', 0.2), pcb: true, lid: true });
    return { vb: E.fit(r.pts.concat([[0, 0, 60]]), 6), svg: r.s };
  };
  function pkgScene(o) {
    return function (a) { var r = pkg(a, o); return { vb: E.fit(r.pts, 8), svg: r.s }; };
  }
  SC.ladder = pkgScene({ heat: true });
  SC.keys = pkgScene({ neck: { abf: 1, hbm: 1 } });

  /* 剖面：S / R / L 三种中介层（滑块在三者之间渐变） */
  SC.variant = function (a) {
    var v = a.val('vr', 2), wS = Math.max(0, 1 - Math.abs(v)), wR = Math.max(0, 1 - Math.abs(v - 1)), wL = Math.max(0, 1 - Math.abs(v - 2));
    var s = '', X0 = 12, X1 = 308, yC = 84, yI = 90, hI = 30, yS = yI + hI + 8;
    var chips = [[16, 62, 'hbm'], [70, 152, 'gpu'], [158, 240, 'gpu'], [248, 304, 'hbm']];
    // 芯片
    chips.forEach(function (c) {
      var top = c[2] === 'hbm' ? 30 : 44;
      s += '<g data-p="' + c[2] + '"><rect class="sd' + (c[2] === 'gpu' ? ' gp' : '') + '" x="' + c[0] + '" y="' + top + '" width="' + (c[1] - c[0]) + '" height="' + (yC - top) + '"/>';
      if (c[2] === 'hbm') for (var l = 1; l < 9; l++) s += '<line class="sdl" x1="' + c[0] + '" x2="' + c[1] + '" y1="' + (top + l * (yC - top) / 9).toFixed(1) + '" y2="' + (top + l * (yC - top) / 9).toFixed(1) + '"/>';
      s += '<text class="ax" x="' + ((c[0] + c[1]) / 2) + '" y="' + (top - 4) + '" text-anchor="middle">' + (c[2] === 'hbm' ? 'HBM' : 'GPU 芯片') + '</text></g>';
      for (var x = c[0] + 4; x < c[1] - 2; x += 6) s += '<rect class="bumpr" data-p="ubump" x="' + x + '" y="' + yC + '" width="3" height="' + (yI - yC) + '" rx="1"/>';
    });
    // 中介层：三种结构叠在一起，按滑块权重显示
    function grp(w, inner) { return w > 0.01 ? '<g style="opacity:' + w.toFixed(2) + '">' + inner + '</g>' : ''; }
    var gS = '<rect class="si" data-p="si" x="' + X0 + '" y="' + yI + '" width="' + (X1 - X0) + '" height="' + hI + '"/>';
    for (var r = 0; r < 3; r++) gS += '<line class="cul" data-p="rdl" x1="' + X0 + '" x2="' + X1 + '" y1="' + (yI + 2 + r * 2.2) + '" y2="' + (yI + 2 + r * 2.2) + '"/>';
    for (var t = X0 + 10; t < X1; t += 16) gS += '<rect class="tsvr" data-p="tsv" x="' + t + '" y="' + (yI + 8) + '" width="3.2" height="' + (hI - 8) + '"/>';
    var gR = '<rect class="rdlb" data-p="rdl" x="' + X0 + '" y="' + yI + '" width="' + (X1 - X0) + '" height="' + hI + '"/>';
    for (r = 0; r < 6; r++) {
      var yy = yI + 3 + r * 4.6;
      for (var x0 = X0 + 4 + (r % 2) * 9; x0 < X1 - 10; x0 += 22) gR += '<line class="cul2" data-p="rdl" x1="' + x0 + '" x2="' + (x0 + 15) + '" y1="' + yy.toFixed(1) + '" y2="' + yy.toFixed(1) + '"/>';
      for (var vx = X0 + 18 + (r % 2) * 11; vx < X1 - 8; vx += 30) gR += '<rect class="tsvr" data-p="rdl" x="' + vx + '" y="' + yy.toFixed(1) + '" width="2" height="4.6"/>';
    }
    var gL = '<rect class="moldb" data-p="mold" x="' + X0 + '" y="' + yI + '" width="' + (X1 - X0) + '" height="' + hI + '"/>';
    for (r = 0; r < 2; r++) { gL += '<line class="cul2" data-p="rdl" x1="' + X0 + '" x2="' + X1 + '" y1="' + (yI + 2 + r * 2.4) + '" y2="' + (yI + 2 + r * 2.4) + '"/><line class="cul2" data-p="rdl" x1="' + X0 + '" x2="' + X1 + '" y1="' + (yI + hI - 2 - r * 2.4) + '" y2="' + (yI + hI - 2 - r * 2.4) + '"/>'; }
    [[46, 82], [138, 172], [226, 262]].forEach(function (b) {
      gL += '<g data-p="lsi"><rect class="lsir" x="' + b[0] + '" y="' + (yI + 7) + '" width="' + (b[1] - b[0]) + '" height="11"/>';
      for (var q = 0; q < 4; q++) gL += '<line class="cul" x1="' + (b[0] + 2) + '" x2="' + (b[1] - 2) + '" y1="' + (yI + 9 + q * 2.2) + '" y2="' + (yI + 9 + q * 2.2) + '"/>';
      gL += '</g>';
    });
    [24, 34, 100, 118, 196, 212, 284, 294].forEach(function (px) { gL += '<rect class="tsvr" data-p="mold" x="' + px + '" y="' + (yI + 7) + '" width="3" height="' + (hI - 14) + '"/>'; });
    s += grp(wS, gS) + grp(wR, gR) + grp(wL, gL);
    // C4 + 载板
    for (var cx = X0 + 8; cx < X1 - 4; cx += 12) s += '<circle class="bumpr" data-p="c4" cx="' + cx + '" cy="' + (yI + hI + 4) + '" r="3.6"/>';
    s += '<g data-p="abf"><rect class="subr" x="' + (X0 - 6) + '" y="' + yS + '" width="' + (X1 - X0 + 12) + '" height="34"/>';
    for (r = 1; r < 6; r++) s += '<line class="sdl" x1="' + (X0 - 6) + '" x2="' + (X1 + 6) + '" y1="' + (yS + r * 34 / 6).toFixed(1) + '" y2="' + (yS + r * 34 / 6).toFixed(1) + '"/>';
    s += '<text class="ax" x="' + (X1 - 2) + '" y="' + (yS + 20) + '" text-anchor="end">ABF 载板</text></g>';
    var lab = ['CoWoS-S · 整片硅 + TSV · ≤3.3×（约 2,700 mm²）', 'CoWoS-R · 聚合物 + 铜 RDL · 线宽 2 µm', 'CoWoS-L · 模塑 + RDL + 局部硅桥 · 3.5× 起'];
    var vi = Math.round(v);
    s += '<text class="vl" x="' + X0 + '" y="' + (yS + 46) + '">' + lab[vi] + '</text>';
    return { vb: [0, 14, 320, yS + 40], svg: s };
  };

  /* 工序：中介层晶圆上的 CoW → 填胶 → 减薄 → 切割 → 上载板 → 测试（等轴测） */
  var FLOW = [
    ['① 做中介层晶圆', '在 300 mm 晶圆上做 TSV、多层 RDL、深沟槽电容（台积电约 65/55nm 级旧产线），外加联电等代工；L 型做的是 RDL + 硅桥。'],
    ['② CoW：芯片上片', '把 GPU 芯片和 HBM 用微凸点一颗颗贴到整片中介层晶圆上（贴片机 / 热压键合机）。从这一步起，芯片拆不下来了。'],
    ['③ 填胶、模封', '点底部填充胶、模封，把整片包起来；控制翘曲是关键（点胶 / AOI 设备）。'],
    ['④ 减薄、露 TSV', '临时贴到载片上，从背面研磨减薄，露出 TSV 的铜头，再做背面焊点（研磨、湿法清洗、临时键合 / 解键合）。'],
    ['⑤ 切割', '把整片切成一个个“芯片 + 中介层”的小模块（切割机、激光）。'],
    ['⑥ oS：上载板', '每个模块用 C4 凸点贴到 ABF 载板上（大封装 100 mm 级），再加盖板。'],
    ['⑦ 测试', '最终测试 / 老化；大封装测试时间长：Blackwell 是 Hopper 的 3–4 倍 ' + R(13) + '。']
  ];
  SC.flow = function (a) {
    var g = a.gen(), L = lay(g), stg = a.st.flow || 1;
    var fd = a.val('fd', 0), fm = a.val('fm', 0), th = a.val('th', 7), sep = a.val('sep', 0), fo = a.val('fo', 1), sb = a.val('sb', 0), tst = a.val('tst', 0);
    var T = tiles(L.ip.w, L.ip.d, 'wafer'), s = '', it = [];
    // 圆片：底面 + 顶面（厚度夸大）
    var c0 = [], c1 = [];
    for (var k = 0; k < 64; k++) { var an = k / 64 * Math.PI * 2; c0.push([150 * Math.cos(an), 150 * Math.sin(an), 0]); c1.push([150 * Math.cos(an), 150 * Math.sin(an), th]); }
    var wop = Math.max(0, 1 - sep);
    if (wop > 0.01) s += '<g data-p="wafer" style="opacity:' + wop.toFixed(2) + '">' + E.poly3(c0, 'wf0') + E.poly3(c1, 'wf1') + '</g>';
    // 找最靠中心的一个位置
    var ci = 0, bd = 1e9;
    T.forEach(function (t, i) { var dx = t[0] + t[2] / 2, dy = t[1] + t[3] / 2, dd = dx * dx + dy * dy; if (dd < bd) { bd = dd; ci = i; } });
    var spread = 1 + 0.18 * sep;
    // 载板（第 ⑥ 步出现在中心模块下面）
    var ct = T[ci];
    if (ct && sb > 0.01) {
      var cx = (ct[0] + ct[2] / 2) * spread, cy = (ct[1] + ct[3] / 2) * spread, sw = ct[2] + 34, sd = ct[3] + 34;
      s += E.box({ x: cx - sw / 2, y: cy - sd / 2, z: th - 6, w: sw, d: sd, h: 6, k: 'sub', p: 'abf', op: sb }).s;
    }
    T.forEach(function (t, i) {
      var cx = (t[0] + t[2] / 2) * spread, cy = (t[1] + t[3] / 2) * spread, x0 = cx - t[2] / 2, y0 = cy - t[3] / 2;
      var op = i === ci ? 1 : fo, inner = '';
      var site = E.box({ x: x0, y: y0, z: th - 0.01, w: t[2], d: t[3], h: 0.6, k: g.var === 'S' ? 'interp' : 'mold', p: 'site', op: op * (0.35 + 0.65 * Math.max(sep, 0.6)) });
      it.push({ d: cx + cy, z: 0, s: site.s });
      if (fd > 0.01) {
        var parts = '', sx = t[2] / L.ip.w, sy = t[3] / L.ip.d, swap = Math.abs(t[2] - L.ip.w) > 0.01;
        L.dies.concat(L.hbms).forEach(function (r) {
          var rx = swap ? r.y - L.ip.y : r.x - L.ip.x, ry = swap ? r.x - L.ip.x : r.y - L.ip.y, rw = swap ? r.d : r.w, rd = swap ? r.w : r.d;
          parts += E.box({ x: x0 + rx, y: y0 + ry, z: th + 0.6, w: rw, d: rd, h: 3, k: r.w === DW ? 'gpu' : 'dram', p: r.w === DW ? 'gpu' : 'hbm', op: fd * op }).s;
        });
        it.push({ d: cx + cy + 0.1, z: 1, s: parts });
      }
      if (fm > 0.01) it.push({ d: cx + cy + 0.2, z: 2, s: E.box({ x: x0, y: y0, z: th + 0.6, w: t[2], d: t[3], h: 3.4, k: 'uf', p: 'site', op: 0.55 * fm * op }).s });
    });
    s += E.paint(it);
    if (ct && tst > 0.01) {
      var px = (ct[0] + ct[2] / 2) * spread, py = (ct[1] + ct[3] / 2) * spread, pr = '';
      for (var q = -2; q <= 2; q++) pr += E.line3([px + q * 6, py, th + 4.2], [px + q * 6 + 4, py - 4, th + 40], 'probe', 'probe');
      var Pp = E.P(px, py, th + 44);
      s += '<g data-p="probe" style="opacity:' + tst.toFixed(2) + '">' + pr + '<text class="okt" x="' + Pp[0].toFixed(1) + '" y="' + (Pp[1] - 4).toFixed(1) + '" text-anchor="middle">✓ 测试</text></g>';
    }
    var vb = E.fit([[-160, -160, 0], [160, 160, 0], [-160, 160, 0], [160, -160, 0], [0, 0, 50]], 6);
    return { vb: vb, svg: s };
  };

  /* 尺寸：一片圆片 / 方片能摆几个（俯视，几何上限） */
  SC.size = function (a) {
    var m = a.val('m', 5.5), shp = a.st.shape || 'wafer', dm = tileDims(m), T = tiles(dm[0], dm[1], shp);
    var k = 0.8, cx = 160, cy = 132, s = '';
    s += '<circle class="' + (shp === 'wafer' ? 'wfr on' : 'wfr') + '" data-p="wafer" cx="' + cx + '" cy="' + cy + '" r="' + (150 * k) + '"/>';
    s += '<rect class="' + (shp === 'panel' ? 'pnl on' : 'pnl') + '" data-p="panel" x="' + (cx - 155 * k) + '" y="' + (cy - 155 * k) + '" width="' + (310 * k) + '" height="' + (310 * k) + '"/>';
    T.forEach(function (t) { s += '<rect class="tile" data-p="site" x="' + (cx + t[0] * k).toFixed(1) + '" y="' + (cy + t[1] * k).toFixed(1) + '" width="' + (t[2] * k).toFixed(1) + '" height="' + (t[3] * k).toFixed(1) + '" rx="1"/>'; });
    s += '<g data-p="reticle"><rect class="ret" x="' + (cx + 132 * k) + '" y="' + (cy + 120 * k) + '" width="' + (26 * k) + '" height="' + (33 * k) + '"/><text class="ax" x="' + (cx + 128 * k) + '" y="' + (cy + 150 * k) + '" text-anchor="end">1 个光罩</text></g>';
    s += '<text class="vl" x="' + (cx - 155 * k) + '" y="' + (cy - 155 * k - 6) + '">' + num(m, 1) + '× ≈ ' + num(m * 858) + ' mm² · ' + (shp === 'wafer' ? '300 mm 圆片' : '310 mm 方片') + ' ' + T.length + ' 个</text>';
    return { vb: [0, cy - 155 * k - 20, 320, 310 * k + 26], svg: s };
  };

  /* 瓶颈：研究页模型 2027 年各环余量（估）+ 测试时间 + 功耗 */
  var NECKS = [['b_ip', '硅中介层（S 型）', 2, 2], ['b_cw', 'CoWoS 封装', -8, 7], ['b_hbm', 'HBM', -11, -11], ['b_abf', 'ABF 载板', -29, -29]];
  SC.hard = function (a) {
    var s = '', x0 = 196, k = 4, top = 26;
    function X(v) { return x0 + v * k; }
    s += '<text class="ax" x="8" y="14">2027 年各环产能 ÷ 需求 − 1（研究页模型，估）</text>';
    s += '<line class="gl" x1="' + X(0) + '" x2="' + X(0) + '" y1="' + (top - 4) + '" y2="' + (top + 4 * 24) + '"/>';
    [-30, -20, -10, 10].forEach(function (v) { s += '<text class="ax" x="' + X(v) + '" y="' + (top + 4 * 24 + 10) + '" text-anchor="middle">' + (v > 0 ? '+' : '') + v + '%</text><line class="gl dsh" x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (top - 4) + '" y2="' + (top + 4 * 24) + '"/>'; });
    NECKS.forEach(function (n, i) {
      var y = top + i * 24, lo = Math.min(0, n[2]), hi = Math.max(0, n[3]), worst = n[2];
      var cls = worst <= -20 ? 'bar bad' : worst < 0 ? 'bar mid' : 'bar okb';
      s += '<g data-p="' + n[0] + '"><text class="bl" x="8" y="' + (y + 12) + '">' + n[1] + '</text>';
      if (n[2] !== n[3]) s += '<rect class="' + cls + '" x="' + X(n[2]) + '" y="' + (y + 2) + '" width="' + ((n[3] - n[2]) * k) + '" height="14" rx="3"/>';
      else s += '<rect class="' + cls + '" x="' + X(lo) + '" y="' + (y + 2) + '" width="' + Math.max(2, (hi - lo) * k) + '" height="14" rx="3"/>';
      var lab = n[2] === n[3] ? (n[2] > 0 ? '+' : '') + n[2] + '%' : n[2] + '%～+' + n[3] + '%';
      s += '<text class="bv" x="' + (X(Math.max(0, n[3])) + 4) + '" y="' + (y + 13) + '">' + lab + '</text></g>';
    });
    // 测试时间与功耗（公开数据）
    var yb = top + 4 * 24 + 26;
    s += '<g data-p="test"><text class="bl" x="8" y="' + (yb + 11) + '">测试时间</text>';
    s += '<rect class="bar okb" x="80" y="' + yb + '" width="' + 14 + '" height="12" rx="2"/><text class="ax" x="98" y="' + (yb + 10) + '">Hopper 1×</text>';
    s += '<rect class="bar mid" x="152" y="' + yb + '" width="' + 42 + '" height="12" rx="2"/><rect class="bar mid" style="opacity:.4" x="194" y="' + yb + '" width="14" height="12" rx="2"/><text class="ax" x="212" y="' + (yb + 10) + '">Blackwell 3–4×</text></g>';
    var yp = yb + 22;
    s += '<g data-p="pwr"><text class="bl" x="8" y="' + (yp + 11) + '">最大功耗</text>';
    [[700, 'H100'], [1200, 'B200'], [1400, 'B300']].forEach(function (p, i) {
      var w = p[0] / 1400 * 66, x = 80 + i * 78;
      s += '<rect class="bar ' + (i ? 'mid' : 'okb') + '" x="' + x + '" y="' + yp + '" width="' + w.toFixed(1) + '" height="12" rx="2"/><text class="ax" x="' + x + '" y="' + (yp + 22) + '">' + p[1] + ' ' + num(p[0]) + 'W</text>';
    });
    s += '</g>';
    return { vb: [0, 0, 320, yp + 28], svg: s };
  };

  /* 下一步：五条路线 */
  SC.alt = function (a) {
    var m = a.st.alt || 'soic', s = '';
    if (m === 'soic') {
      var it = '';
      it += E.box({ x: -10, y: -10, z: 0, w: 140, d: 110, h: 4, k: 'mold', p: 'soic' }).s;
      it += E.box({ x: 10, y: 10, z: 4.4, w: 90, d: 70, h: 6, k: 'gpu', p: 'soic' }).s;
      it += E.box({ x: 10, y: 10, z: 10.4, w: 90, d: 70, h: 0.8, k: 'cu', p: 'soic' }).s;
      it += E.box({ x: 18, y: 16, z: 11.2 + a.val('lift', 0), w: 74, d: 58, h: 6, k: 'logic', p: 'soic' }).s;
      var P1 = E.P(100, 10, 18 + a.val('lift', 0));
      it += '<text class="ax" x="' + (P1[0] + 6).toFixed(1) + '" y="' + P1[1].toFixed(1) + '">上层芯片（铜对铜直接键合）</text>';
      var P2 = E.P(100, 80, 5);
      it += '<text class="ax" x="' + (P2[0] + 6).toFixed(1) + '" y="' + (P2[1] + 10).toFixed(1) + '">下层芯片 → 再放到 CoWoS 上</text>';
      return { vb: E.fit([[-10, -10, 0], [130, 100, 0], [-10, 100, 0], [130, -10, 0], [18, 16, 30]], 10).map(function (v, i) { return i === 2 ? v + 40 : v; }), svg: it };
    }
    if (m === 'panel') {
      var dm = tileDims(5.5), Tw = tiles(dm[0], dm[1], 'wafer'), Tp = tiles(dm[0], dm[1], 'panel'), k = 0.45;
      [[80, 'wafer', Tw], [240, 'panel', Tp]].forEach(function (o) {
        var cx = o[0], cy = 92;
        s += o[1] === 'wafer' ? '<circle class="wfr on" data-p="panel" cx="' + cx + '" cy="' + cy + '" r="' + (150 * k) + '"/>' : '<rect class="pnl on" data-p="panel" x="' + (cx - 155 * k) + '" y="' + (cy - 155 * k) + '" width="' + (310 * k) + '" height="' + (310 * k) + '"/>';
        o[2].forEach(function (t) { s += '<rect class="tile" data-p="panel" x="' + (cx + t[0] * k).toFixed(1) + '" y="' + (cy + t[1] * k).toFixed(1) + '" width="' + (t[2] * k).toFixed(1) + '" height="' + (t[3] * k).toFixed(1) + '"/>'; });
        s += '<text class="bl" x="' + cx + '" y="' + (cy + 155 * k + 16) + '" text-anchor="middle">' + (o[1] === 'wafer' ? '300 mm 圆片' : '310 mm 方片') + '：' + o[2].length + ' 个</text>';
      });
      s += '<text class="ax" x="160" y="14" text-anchor="middle">5.5× 光罩中介层，几何上限（推算）</text>';
      return { vb: [0, 0, 320, 180], svg: s };
    }
    if (m === 'glass') {
      // 两种载板剖面：有机（会翘）vs 玻璃（平）
      var bow = 6;
      s += '<g data-p="abf"><text class="bl" x="10" y="26">有机载板（玻纤 + 树脂芯层）</text>';
      s += '<path class="subr" d="M20 ' + (48 + bow) + ' Q160 ' + (48 - bow) + ' 300 ' + (48 + bow) + ' L300 ' + (78 + bow) + ' Q160 ' + (78 - bow) + ' 20 ' + (78 + bow) + ' Z"/>';
      for (var x = 26; x < 296; x += 10) s += '<path class="weave" d="M' + x + ' ' + (63 + bow * (Math.pow((x - 160) / 140, 2) * 2 - 1)).toFixed(1) + ' q2.5 -3 5 0 t5 0"/>';
      s += '<text class="ax" x="300" y="98" text-anchor="end">尺寸越大越容易翘（示意）</text></g>';
      s += '<g data-p="glass"><text class="bl" x="10" y="122">玻璃芯载板</text><rect class="glsr" x="20" y="132" width="280" height="30"/>';
      for (x = 34; x < 300; x += 22) s += '<rect class="tsvr" x="' + x + '" y="132" width="3" height="30"/>';
      s += '<text class="ax" x="300" y="176" text-anchor="end">更平、热胀冷缩小；竖孔为玻璃通孔（示意）</text></g>';
      return { vb: [0, 8, 320, 176], svg: s };
    }
    if (m === 'cpo') {
      var ic = '';
      ic += E.box({ x: 0, y: 0, z: 0, w: 140, d: 140, h: 4, k: 'sub', p: 'cpo' }).s;
      var oe = [];
      [[10, 55], [110, 55], [55, 10], [55, 110]].forEach(function (p) { oe.push(E.box({ x: p[0], y: p[1], z: 4, w: 20, d: 20, h: 3, k: 'logic', p: 'cpo' })); });
      oe.push(E.box({ x: 40, y: 40, z: 4, w: 60, d: 60, h: 3.4, k: 'gpu', p: 'cpo' }));
      ic += E.paint(oe);
      [[20, 55, 20, -30], [120, 65, 160, 65], [65, 20, 65, -30], [65, 130, 65, 170]].forEach(function (f) { ic += E.line3([f[0], f[1], 6], [f[2], f[3], 6], 'fiber', 'cpo'); });
      var Pc = E.P(70, 70, 10);
      ic += '<text class="ax" x="' + Pc[0].toFixed(1) + '" y="' + (Pc[1] - 6).toFixed(1) + '" text-anchor="middle">交换 / 计算芯片</text>';
      var Po = E.P(130, 65, 8);
      ic += '<text class="ax" x="' + (Po[0] + 4).toFixed(1) + '" y="' + Po[1].toFixed(1) + '">光引擎 → 光纤</text>';
      return { vb: E.fit([[0, -30, 0], [160, 170, 0], [0, 170, 0], [160, -30, 0], [70, 70, 30]], 10), svg: ic };
    }
    // 中国：国产 2.5D vs 台积电 CoWoS（研究页，估）
    var rows = [['国产 2.5D 2025', 1.3], ['国产 2.5D 2026', 2.3], ['国产 2.5D 2027', 5.0], ['台积电 2026', 12], ['台积电 2027', 18.5]], kx = 11;
    s += '<text class="ax" x="8" y="14">年末产能，万片/月（研究页口径；国产为估、来源较弱）</text>';
    rows.forEach(function (r, i) {
      var y = 26 + i * 26, cn = i < 3;
      s += '<g data-p="cn"><text class="bl" x="8" y="' + (y + 12) + '">' + r[0] + '</text><rect class="bar ' + (cn ? 'mid' : 'okb') + '" x="104" y="' + (y + 2) + '" width="' + (r[1] * kx).toFixed(1) + '" height="14" rx="3"/><text class="bv" x="' + (108 + r[1] * kx).toFixed(1) + '" y="' + (y + 13) + '">' + r[1] + '</text></g>';
    });
    return { vb: [0, 0, 320, 160], svg: s };
  };

  /* ---------- 步内小部件 ---------- */
  var WD = {};
  WD.energy = function (el, a) {
    el.innerHTML = '<label class="ex-r">带宽 <input type="range" min="1" max="30" step="1" value="22" aria-label="带宽 TB/s"><output></output></label><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    function up() {
      var tb = +i.value, bits = tb * 8;
      o.textContent = tb + ' TB/s';
      p.innerHTML = tb + ' TB/s = 每秒 ' + bits + ' Tb。普通封装 0.5–1 pJ/bit → <b>' + num(bits * 0.5) + '–' + num(bits) + ' W</b>；先进封装 0.25–0.5 pJ/bit → <b>' + num(bits * 0.25) + '–' + num(bits * 0.5) + ' W</b>' + CALC +
        '<br><small>只算芯片间搬数据这一段（按 UCIe 口径 ' + R(12) + '）。22 TB/s 是 Rubin 的 HBM 带宽 ' + R(8) + '；而且普通基板根本排不下这么多线。</small>';
    }
    i.addEventListener('input', up); up();
  };
  WD.apart = function (el, a) {
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="展开或压紧"><button type="button" data-v="1" aria-pressed="true">展开</button><button type="button" data-v="0" aria-pressed="false">压紧</button></div><p class="ex-o">图里每层的厚度是夸大的示意；拖顶上的“产品”滑块，可以看 1 颗芯片（H100）到 4 颗芯片（Rubin Ultra 计划版）的摆法。</p>';
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; a.set('apart', +b.dataset.v); el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); });
  };
  function showBd(el, m) { var sec = el.closest('.ex-step'); if (sec) sec.querySelectorAll('.ex-bd').forEach(function (d) { d.hidden = d.dataset.m !== m; }); }
  WD.variant = function (el, a) {
    el.innerHTML = '<label class="ex-r">中介层 <input type="range" min="0" max="2" step="1" value="2" aria-label="CoWoS 类型 S R L"><output></output></label>' +
      '<div class="ex-seg" role="group" aria-label="CoWoS 类型"><button type="button" data-v="0">S 硅</button><button type="button" data-v="1">R 有机 RDL</button><button type="button" data-v="2">L 硅桥</button></div>';
    var i = el.querySelector('input'), o = el.querySelector('output');
    function up(v) {
      i.value = v; a.st.vr = v; a.set('vr', v); o.textContent = 'CoWoS-' + VN[v];
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', +b.dataset.v === v ? 'true' : 'false'); });
      showBd(el, VN[v]);
    }
    i.addEventListener('input', function () { up(+i.value); });
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(+b.dataset.v); });
    document.addEventListener('exgen', function () { up(VN.indexOf(a.gen().var)); });
    up(VN.indexOf(a.gen().var));
  };
  WD.flow = function (el, a) {
    el.innerHTML = '<label class="ex-r">工序 <input type="range" min="1" max="7" step="1" value="2" aria-label="工序"><output></output></label><p class="ex-o fl"></p>' +
      '<label class="ex-r">每颗芯片良率 <input type="range" min="95" max="100" step="0.1" value="99" aria-label="每颗芯片良率"><output></output></label>' +
      '<label class="ex-r">每次贴片良率 <input type="range" min="97" max="100" step="0.1" value="99.5" aria-label="每次贴片良率"><output></output></label><p class="ex-o yl"></p>';
    var ins = el.querySelectorAll('input'), outs = el.querySelectorAll('output'), pf = el.querySelector('.fl'), py = el.querySelector('.yl');
    function up() {
      var st = +ins[0].value; a.st.flow = st;
      a.set('fd', st >= 2 ? 1 : 0); a.set('fm', st >= 3 ? 1 : 0); a.set('th', st >= 4 ? 3 : 7); a.set('sep', st >= 5 ? 1 : 0);
      a.set('fo', st >= 6 ? 0.08 : 1); a.set('sb', st >= 6 ? 1 : 0); a.set('tst', st >= 7 ? 1 : 0);
      outs[0].textContent = st + ' / 7'; pf.innerHTML = '<b>' + FLOW[st - 1][0] + '</b>　' + FLOW[st - 1][1];
      var g = a.gen(), n = g.dies + g.hbmOn, pk = +ins[1].value / 100, pb = +ins[2].value / 100, y = Math.pow(pk * pb, n);
      outs[1].textContent = (+ins[1].value).toFixed(1) + '%'; outs[2].textContent = (+ins[2].value).toFixed(1) + '%';
      py.innerHTML = g.name + '：' + g.dies + ' 颗计算芯片 + ' + g.hbmOn + ' 颗 HBM = ' + n + ' 颗，任何一颗坏或贴坏，整颗封装报废。整颗良率 ≈ (' + (pk * 100).toFixed(1) + '% × ' + (pb * 100).toFixed(1) + '%)<sup>' + n + '</sup> = <b>' + (y * 100).toFixed(1) + '%</b> <span class="tag t-est">纯算术示意，不是厂商良率</span>';
      a.update();
    }
    [].forEach.call(ins, function (x) { x.addEventListener('input', up); });
    document.addEventListener('exgen', up); up();
  };
  var MARKS = [[1.5, '2016 年约 1.5× ' + R(4)], [3.3, 'S 型上限 3.3×，放 8 颗 HBM3 ' + R(4) + R(1)], [3.5, '首款 L 型 3.5×，2024 年量产 ' + R(1)], [5.5, '5.5×，2026 年已量产，最多 12 颗 HBM4 ' + R(2) + R(4)], [9, '9× 约 7,722 mm²，载板 >120 mm ' + R(4)], [9.5, '9.5×，计划 2027 年 ' + R(3)], [14, '14×，约 10 颗大芯片 + 20 颗 HBM，计划 2028 年 ' + R(2)]];
  WD.size = function (el, a) {
    el.innerHTML = '<label class="ex-r">光罩倍数 <input type="range" min="1" max="14" step="0.1" value="5.5" aria-label="中介层光罩倍数"><output></output></label>' +
      '<div class="ex-seg" role="group" aria-label="路线图节点">' + MARKS.map(function (m) { return '<button type="button" data-m="' + m[0] + '">' + m[0] + '×</button>'; }).join('') + '</div>' +
      '<div class="ex-seg" role="group" aria-label="圆片或方片"><button type="button" data-s="wafer">300 mm 圆片</button><button type="button" data-s="panel">310 mm 方片（CoPoS）</button></div><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    a.st.shape = 'wafer';
    function up() {
      var m = +i.value, dm = tileDims(m), nw = tiles(dm[0], dm[1], 'wafer').length, np = tiles(dm[0], dm[1], 'panel').length;
      a.set('m', m); o.textContent = m.toFixed(1) + '×';
      el.querySelectorAll('button[data-m]').forEach(function (b) { b.setAttribute('aria-pressed', Math.abs(+b.dataset.m - m) < 0.05 ? 'true' : 'false'); });
      el.querySelectorAll('button[data-s]').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.s === a.st.shape ? 'true' : 'false'); });
      var mk = MARKS.filter(function (x) { return Math.abs(x[0] - m) < 0.05; })[0];
      p.innerHTML = m.toFixed(1) + '× ≈ ' + num(m * 858) + ' mm²：圆片最多 <b>' + nw + '</b> 个，方片 <b>' + np + '</b> 个' + CALC + (mk ? '<br>' + mk[1] : '') +
        '<br><small>按 858 mm² × 倍数、长宽比 1.25、切割道 2 mm、边缘留 3 mm 现算的几何上限，没扣良率；研究页的“每片可封颗数”另有口径 ' + R(16) + '。</small>';
      a.update();
    }
    i.addEventListener('input', up);
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.m) i.value = b.dataset.m; else a.st.shape = b.dataset.s;
      up();
    });
    up();
  };
  var NECKTX = {
    b_ip: '硅中介层只卡用整片硅的 S 型（谷歌 TPU 等）。研究页：2026 年余量约 +20%，2027 年约 +3%（S 型口径）；台积电 2027 年自制新增 ≥ 16.1 千片/月就不缺，格罗方德 2028 上半年才放量' + EST + R(16) + ' → <a href="cowos.html#ip">中介层一环</a>',
    b_cw: 'CoWoS 封装产能：台积电年末约 12 万（2026）→ 18.5 万片/月（2027），设备交期 10–12 个月；2027 年余量 −8%～+7%，“只略紧”' + EST + R(16) + ' → <a href="cowos.html#cw-toc">TOC 图</a>',
    b_hbm: 'HBM：2027 年约比需求少 11%，和 CoWoS 差不多紧' + EST + R(16) + '。HBM 本身的瓶颈（堆叠良率、16 层）见 <a href="explain-hbm.html#s-hard">HBM 原理图第 8 步</a>。',
    b_abf: 'ABF 载板：封装越大载板越大（5.5× 要 >100 mm、9× 要 >120 mm）' + R(4) + '，越大越容易翘、良率越低；上游 T-glass 玻纤布日东纺约占 90% ' + R(22) + '，味之素 ABF 膜提价 ' + R(23) + '。研究页模型 2027 年约 −29%，最紧' + EST + R(16) + ' → <a href="cowos.html#neck">瓶颈表</a>',
    test: '测试：Blackwell 测试时间是 Hopper 的 3–4 倍，每颗要在不同机台上测几十次 ' + R(13) + '；研究页把测试列为“数据缺口”，没有画进 TOC 图 ' + R(16) + '。',
    pwr: '功耗与散热：最大功耗 700 → 1,200 → 1,400W ' + R(7) + '，热和供电都压在封装、盖板和载板上；Rubin Ultra 整柜约 600 kW ' + R(11) + '。研究页：2028 年约束可能轮到数据中心电力' + EST + R(16) + '。'
  };
  WD.neck = function (el, a) {
    var keys = ['b_ip', 'b_cw', 'b_hbm', 'b_abf', 'test', 'pwr'];
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="瓶颈环节">' + keys.map(function (k) { return '<button type="button" data-k="' + k + '" aria-pressed="false">' + PARTS[k].n + '</button>'; }).join('') + '</div><p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(k) {
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.k === k ? 'true' : 'false'); });
      p.innerHTML = NECKTX[k];
      if (D.steps[a.st.i] && D.steps[a.st.i].scene === 'hard') a.select(k);
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.k); });
    p.innerHTML = NECKTX.b_abf; el.querySelector('[data-k=b_abf]').setAttribute('aria-pressed', 'true');
  };
  WD.ladder = function (el, a) {
    function card(g, k) {
      return '<button type="button" class="ex-gc' + (k === a.st.g ? ' on' : '') + '" data-g="' + k + '"><span class="ex-gn">' + g.name + '<small>' + g.arch + ' · ' + g.year + '</small></span>' +
        '<span class="ex-gm"><span>' + g.dies + ' 颗计算芯片 · CoWoS-' + g.var + '</span><span>' + g.mem + '</span><span>带宽 ' + g.bw + '</span><span>功耗 ' + g.tgpT + '</span>' +
        '<span>中介层：' + g.ip + '</span><span>' + g.ppw + '</span></span>' +
        '<span class="ex-gu"><i>解锁</i>' + g.unlock + '</span><span class="ex-gu nk"><i>瓶颈</i>' + g.neck + '</span>' + (g.note ? '<span class="ex-gu"><i class="nt">注</i>' + g.note + '</span>' : '') + '</button>';
    }
    function up() { el.innerHTML = '<div class="ex-gl">' + G.map(card).join('') + '</div>'; }
    el.addEventListener('click', function (e) { if (e.target.closest('a')) return; var b = e.target.closest('.ex-gc'); if (b) a.setGen(+b.dataset.g); });
    document.addEventListener('exgen', up); up();
  };
  var ALTS = [['soic', 'SoIC 3D'], ['panel', 'CoPoS 面板'], ['glass', '玻璃基板'], ['cpo', '共封装光学'], ['cn', '中国路径']];
  WD.alt = function (el, a) {
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="路线">' + ALTS.map(function (x) { return '<button type="button" data-m="' + x[0] + '">' + x[1] + '</button>'; }).join('') + '</div>';
    function up(m) {
      a.st.alt = m; showBd(el, m);
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.m === m ? 'true' : 'false'); });
      if (m === 'soic') { a.set('lift', 14, true); a.set('lift', 0); }
      a.update();
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.m); });
    up('soic');
  };
  WD.quiz = function (el) {
    el.innerHTML = D.quiz.map(function (q, k) { return '<details class="ex-q"><summary><b>' + (k + 1) + '.</b> ' + q[0] + '</summary><p>' + q[1] + '</p></details>'; }).join('');
  };

  function readout(a, s) {
    var g = a.gen();
    if (s.scene === 'why') return g.name + ' · ' + g.dies + ' 颗芯片 · 光罩上限 858 mm²';
    if (s.scene === 'variant') return ['CoWoS-S · 整片硅 · ≤3.3×', 'CoWoS-R · 有机 RDL · 2 µm', 'CoWoS-L · RDL + 硅桥 · 3.5× 起'][a.st.vr == null ? 2 : a.st.vr];
    if (s.scene === 'flow') { var L = lay(g); return FLOW[(a.st.flow || 1) - 1][0] + ' · 示意 ' + tiles(L.ip.w, L.ip.d, 'wafer').length + ' 个/片'; }
    if (s.scene === 'size') { var m = a.st.tgt.m || 5.5, dm = tileDims(m); return num(m, 1) + '× · 圆片 ' + tiles(dm[0], dm[1], 'wafer').length + ' / 方片 ' + tiles(dm[0], dm[1], 'panel').length + ' 个'; }
    if (s.scene === 'hard') return '2027 最紧：ABF 载板 −29%（估）';
    if (s.scene === 'alt') return (ALTS.filter(function (x) { return x[0] === (a.st.alt || 'soic'); })[0] || ALTS[0])[1];
    if (s.scene === 'keys') return '红色：载板（最紧）、HBM（次紧）';
    return g.name + ' · ' + g.dies + ' 芯 + ' + g.hbmOn + ' HBM · CoWoS-' + g.var + ' · ' + (g.tgp ? '≤' + num(g.tgp) + 'W' : '功耗未公布');
  }

  window.EX.mount({
    steps: D.steps, gens: G, parts: PARTS, scenes: SC, widgets: WD, readout: readout,
    onStep: function (a, s) {
      if (s.scene === 'stack' && a.st.tgt.apart == null) { a.set('apart', 0, true); a.set('apart', 1); }
    }
  });
})();
