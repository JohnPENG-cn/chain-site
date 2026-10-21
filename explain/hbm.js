/* 万物原理图 · HBM：部件说明、场景（等轴测 SVG）、步内小部件、实时读数。
 * 数据（代际、步骤文字、来源）由 explain/build.py 从 explain/hbm.py 注入为 window.EXD。 */
(function () {
  'use strict';
  var D = window.EXD, G = D.gens;
  function R(n) { return '<a class="sr" href="#src' + n + '">[' + n + ']</a>'; }
  D.ref = R;
  function num(v, dp) { return (+v).toLocaleString('en-US', { maximumFractionDigits: dp == null ? 0 : dp, minimumFractionDigits: dp || 0 }); }
  function bwTxt(gbs) { return gbs >= 1000 ? num(gbs / 1000, 2) + ' TB/s' : num(gbs) + ' GB/s'; }

  /* ---------- 部件：名称 + 一句话说明（可带来源编号） ---------- */
  var PARTS = {
    cmp: { n: '算力曲线', d: '服务器芯片峰值算力，约每 2 年 ×3.0 ' + R(15) },
    bw: { n: '带宽曲线', d: '内存（DRAM）带宽，约每 2 年 ×1.6 ' + R(15) },
    gap: { n: '内存墙', d: '两条线之间的空隙：算力等数据的时间越来越长。纵轴是对数刻度。' },
    die: { n: 'DRAM 裸片', d: function (a) { return '一颗存储芯片。' + a.gen().name + ' 每层 ' + a.gen().dieGb + 'Gb = ' + (a.gen().dieGb / 8) + 'GB ' + R(a.gen().src_cfg); } },
    bank: { n: '存储阵列（bank）', d: '几十亿个存储单元排成的方阵，可以各自独立读写，好让多个请求同时进行。' },
    cell: { n: '存储单元（1T1C）', d: '1 个晶体管（阀门）+ 1 个电容（小水桶）= 1 位。桶里有电荷是 1，没有是 0；会漏电，所以要定期刷新。' },
    sa: { n: '读出放大器', d: '电容里的电荷很少，读出放大器把位线上微小的电压差放大成清楚的 0 或 1，并顺手把电荷写回去。' },
    wl: { n: '字线 / 位线', d: '字线（横）控制一排晶体管开关；位线（竖）把选中单元的电荷送到读出放大器。' },
    core: { n: '核心 DRAM 层', d: function (a) { var g = a.gen(); return g.name + '：' + g.layers + ' 层 × ' + g.dieGb + 'Gb = ' + (g.layers * g.dieGb / 8) + 'GB ' + R(g.src_cfg) + '。层越多，每层越要磨薄。'; } },
    tsv: { n: 'TSV 硅通孔', d: '穿透整颗硅片的竖直铜孔，HBM2E 每颗 die 超过 5,000 个 ' + R(5) + '。信号、电源和地都从这里直上直下。' },
    bump: { n: '微凸点', d: '上下两层之间的小焊点，把 TSV 对准接通。MR-MUF 现在的焊点间距约 30 µm ' + R(13) + '。' },
    thin: { n: 'die 厚度', d: '12 层 HBM3E 的 DRAM 比 8 层薄 40% ' + R(7) + '；16 层 HBM4 约 50 µm ' + R(13) + '。' },
    basedie: { n: '底座 die', d: function (a) { var g = a.gen(); return g.base === 'DRAM' ? g.name + '：底座由内存厂用 DRAM 工艺做，1.1V ' + R(12) : g.name + '：底座用逻辑工艺——台积电 12FFC/N5（0.75–0.8V）、三星 4nm；HBM4E 可定制 ' + R(12) + R(11); } },
    phy: { n: '收发电路 PHY', d: function (a) { return '对外 ' + a.gen().io + ' 根数据线的收发电路，在底座 die 上。HBM4 线数翻倍后，GPU 侧 PHY 约从 11 mm² 增到 15 mm² ' + R(12); } },
    film: { n: 'NCF 薄膜', d: 'TC-NCF 的不导电薄膜：每叠一层铺一层，加热加压后把两层粘牢。三星 12 层把缝压到 7 µm ' + R(8) },
    mold: { n: '模塑填充（EMC）', d: 'MR-MUF 一次回流焊好所有凸点后，灌进液态环氧模塑料把缝填满，导热比薄膜好 ' + R(6) },
    pad: { n: '铜焊盘', d: '混合键合不用凸点：两面的铜焊盘磨平后直接贴合，加热时铜膨胀连成一体；间距可到 18 µm 以下 ' + R(13) },
    gpu: { n: 'GPU', d: '计算芯片。HBM 必须挨着它放，因为几千根线只能走几毫米。Rubin 配 288GB HBM4、22 TB/s ' + R(17) },
    stackp: { n: 'HBM 堆栈', d: function (a) { var g = a.gen(); return '一颗 HBM = 底座 die + ' + g.layers + ' 层 DRAM。图中 8 颗，和 Rubin 一样 ' + R(18) + '；8 × ' + (g.layers * g.dieGb / 8) + 'GB = ' + (8 * g.layers * g.dieGb / 8) + 'GB（按本代代表配置推算）。'; } },
    interp: { n: '硅中介层', d: '一块不做计算的硅片，里面刻满细线，把 HBM 和 GPU 连起来（2.5D 封装，台积电叫 CoWoS）。HBM 能出多少货也受它的产能限制。' },
    subs: { n: '封装基板', d: '中介层下面的有机基板，把信号和电源再扇出到电路板。研究页判断 2027 年最紧的一环是封装载板。' },
    strand: { n: '数据通道', d: function (a) { var g = a.gen(); return '每一束 = 一个独立通道。' + g.name + '：' + g.ch + ' 个通道、共 ' + g.io + ' 位 ' + R(g.io === 2048 ? 2 : 1) + '。'; } },
    ruler: { n: '高度上限', d: function (a) { var g = a.gen(); return g.hlim ? g.name + '：总高 ≤ ' + g.hlim + ' µm（逻辑晶圆厚 775 µm，HBM 不能比 GPU 高）' + R(13) : g.name + '：这一代的高度上限没查到公开数字，图中不画。'; } },
    heat: { n: '热流', d: '热要穿过一层层 die 和填充材料才能到顶上的散热板；海力士称这几代热负担升了约 2.2 倍 ' + R(13) + '。' }
  };

  /* ---------- 一颗 HBM 堆栈（等轴测，逐层由下往上画） ---------- */
  var W = 120, DD = 84, T = 8, TB = 10;
  function stackSvg(a, o) {
    var E = window.EX, n = a.val('n', a.gen().layers), ap = o.apart == null ? a.val('apart', 0.6) : o.apart;
    var nf = Math.ceil(n - 1e-3), g = 2 + ap * Math.min(16, 170 / Math.max(8, n));
    var logic = a.gen().base !== 'DRAM', s = '', pts = [];
    var neck = o.neck || {};
    var bx = -4, by = -4, bw = W + 30, bd = DD + 8;
    s += E.box({ x: bx, y: by, z: 0, w: bw, d: bd, h: TB, k: logic ? 'logic' : 'dram2', p: 'basedie', cls: neck.basedie ? 'neck' : '' }).s;
    // PHY：底座露出的一侧，一排焊盘刻线
    var phy = E.box({ x: W + 6, y: 6, z: TB, w: 16, d: DD - 12, h: 1.4, k: 'phy', p: 'phy' }).s, ticks = '';
    for (var t = 0; t < 14; t++) ticks += E.line3([W + 8, 9 + t * (DD - 18) / 13, TB + 1.4], [W + 20, 9 + t * (DD - 18) / 13, TB + 1.4], 'tk', 'phy');
    s += phy + ticks;
    var xs = [], ys = [36, 48];
    for (var i = 0; i < 9; i++) xs.push(18 + i * 10.5);
    var z = TB;
    function bumps(z0, gh) {
      if (gh < 3 || o.bumps === false) return '';
      var r = '';
      ys.forEach(function (yy) { xs.forEach(function (xx) { r += E.box({ x: xx - 1.3, y: yy - 1.3, z: z0, w: 2.6, d: 2.6, h: gh, k: 'cu', p: 'bump' }).s; }); });
      return r;
    }
    for (var k = 0; k < nf; k++) {
      s += bumps(z, g);
      z += g;
      var op = Math.min(1, n - k);
      var top = k === nf - 1, inner = '';
      if (top) {
        // 顶层：bank 刻线 + TSV 点阵 + 厚度标尺
        for (var bx2 = 0; bx2 < 4; bx2++) for (var by2 = 0; by2 < 2; by2++) {
          var x0 = 6 + bx2 * 28, y0 = 5 + by2 * 52;
          inner += E.poly3([[x0, y0, z + T], [x0 + 24, y0, z + T], [x0 + 24, y0 + 22, z + T], [x0, y0 + 22, z + T]], 'grv');
        }
        ys.forEach(function (yy) { xs.forEach(function (xx) { inner += E.dot3([xx, yy, z + T], 1.1, 'tsvd', 'tsv'); }); });
        inner += E.line3([W, DD + 6, z], [W, DD + 6, z + T], 'rl', 'thin') + E.line3([W - 3, DD + 6, z], [W + 3, DD + 6, z], 'rl', 'thin') + E.line3([W - 3, DD + 6, z + T], [W + 3, DD + 6, z + T], 'rl', 'thin');
      }
      s += E.box({ x: 0, y: 0, z: z, w: W, d: DD, h: T, k: 'dram', p: 'core', op: op, inner: inner, cls: neck.core ? 'neck' : '' }).s;
      z += T;
    }
    // 数据线：从 PHY 向外伸出（通道束）
    if (o.strands) {
      var ch = a.val('ch', a.gen().ch), cf = Math.ceil(ch - 1e-3), sw = a.gen().io / a.gen().ch > 64 ? 'st2' : 'st';
      for (var c = 0; c < cf; c++) {
        var yy = 8 + (c + 0.5) * (DD - 16) / cf, opc = Math.min(1, ch - c);
        s += '<g style="opacity:' + opc.toFixed(2) + '">' + E.line3([W + 22, yy, TB + 1], [W + 70, yy, TB + 1], sw, 'strand') + E.dot3([W + 70, yy, TB + 1], 0.9, 'dt', 'strand') + '</g>';
      }
    }
    pts.push([bx, by, 0], [bx + bw + (o.strands ? 50 : 0), by + bd, 0], [0, 0, z + 4], [W + 30, DD + 8, z + 4], [bx, by + bd, 0], [bx + bw, by, 0]);
    return { s: s, pts: pts, top: z };
  }

  /* ---------- 场景 ---------- */
  var SC = {};
  SC.wall = function (a) {
    var yr = a.val('yr', 20), w = 320, h = 200, L = 34, B = 176, Tp = 14;
    var maxv = Math.log10(Math.pow(3, 10));
    function X(t) { return L + t / 20 * (w - L - 12); }
    function Y(v) { return B - Math.log10(v) / maxv * (B - Tp); }
    var cp = '', bp = '', gp = '';
    for (var t = 0; t <= yr + 1e-6; t += 0.5) {
      var c = Math.pow(3, t / 2), b = Math.pow(1.6, t / 2);
      cp += (t ? 'L' : 'M') + X(t).toFixed(1) + ' ' + Y(c).toFixed(1);
      bp += (t ? 'L' : 'M') + X(t).toFixed(1) + ' ' + Y(b).toFixed(1);
    }
    var tt = [];
    for (t = 0; t <= yr + 1e-6; t += 0.5) tt.push(t);
    gp = 'M' + tt.map(function (t) { return X(t).toFixed(1) + ' ' + Y(Math.pow(3, t / 2)).toFixed(1); }).join('L') + 'L' + tt.slice().reverse().map(function (t) { return X(t).toFixed(1) + ' ' + Y(Math.pow(1.6, t / 2)).toFixed(1); }).join('L') + 'Z';
    var s = '';
    [1, 10, 100, 1000, 10000].forEach(function (v) { s += '<line class="gl" x1="' + L + '" x2="' + (w - 12) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '"/><text class="ax" x="' + (L - 4) + '" y="' + (Y(v) + 3).toFixed(1) + '" text-anchor="end">×' + (v >= 1000 ? v / 1000 + 'k' : v) + '</text>'; });
    [0, 5, 10, 15, 20].forEach(function (t) { s += '<text class="ax" x="' + X(t).toFixed(1) + '" y="' + (B + 14) + '" text-anchor="middle">' + t + ' 年</text>'; });
    s += '<path class="gapf" data-p="gap" d="' + gp + '"/>';
    s += '<path class="cv1" data-p="cmp" d="' + cp + '"/><path class="cv2" data-p="bw" d="' + bp + '"/>';
    var cx = X(yr), c1 = Math.pow(3, yr / 2), b1 = Math.pow(1.6, yr / 2);
    s += '<line class="cur" x1="' + cx.toFixed(1) + '" x2="' + cx.toFixed(1) + '" y1="' + Tp + '" y2="' + B + '"/>';
    s += '<circle class="pt1" data-p="cmp" cx="' + cx.toFixed(1) + '" cy="' + Y(c1).toFixed(1) + '" r="4"/><circle class="pt2" data-p="bw" cx="' + cx.toFixed(1) + '" cy="' + Y(b1).toFixed(1) + '" r="4"/>';
    s += '<text class="lb1" x="' + (L + 6) + '" y="' + (Tp + 10) + '">— 算力 ×3.0 / 2 年</text><text class="lb2" x="' + (L + 6) + '" y="' + (Tp + 24) + '">— 内存带宽 ×1.6 / 2 年</text>';
    return { vb: [0, 0, w, h + 6], svg: s };
  };

  SC.cell = function (a) {
    var E = window.EX, it = [], s = '';
    s += E.box({ x: 0, y: 0, z: 0, w: 200, d: 140, h: 8, k: 'dram2', p: 'die' }).s;
    var top = '';
    for (var i = 0; i < 4; i++) for (var j = 0; j < 2; j++) {
      var x0 = 8 + i * 48, y0 = 8 + j * 66;
      top += E.box({ x: x0, y: y0, z: 8, w: 40, d: 54, h: 1.6, k: 'dram', p: 'bank' }).s;
      for (var g = 1; g < 6; g++) {
        top += E.line3([x0 + g * 40 / 6, y0, 9.6], [x0 + g * 40 / 6, y0 + 54, 9.6], 'grv', 'bank');
        top += E.line3([x0, y0 + g * 54 / 6, 9.6], [x0 + 40, y0 + g * 54 / 6, 9.6], 'grv', 'bank');
      }
      top += E.box({ x: x0, y: y0 + 55, z: 8, w: 40, d: 4, h: 1, k: 'sa', p: 'sa' }).s;
    }
    s += top;
    // 选中的一个单元（亮）
    var cx = 8 + 2 * 48 + 40 * 4 / 6, cy = 8 + 54 * 2 / 6;
    s += E.box({ x: cx - 2, y: cy - 2, z: 9.6, w: 4, d: 4, h: 3, k: 'lit', p: 'cell' }).s;
    var A = E.P(cx, cy, 12.6);
    // 放大框：1T1C 示意（二维），用一根线连到被选中的单元
    var ix = 70, iy = -150, iw = 150, ih = 118;
    s += '<path class="wire" d="M' + A[0].toFixed(1) + ' ' + A[1].toFixed(1) + ' L' + (ix + 20) + ' ' + (iy + ih) + '"/><circle class="dt" cx="' + A[0].toFixed(1) + '" cy="' + A[1].toFixed(1) + '" r="1.6"/><circle class="dt" cx="' + (ix + 20) + '" cy="' + (iy + ih) + '" r="1.6"/>';
    s += '<g transform="translate(' + ix + ',' + iy + ')"><rect class="inset" width="' + iw + '" height="' + ih + '" rx="8"/>' +
      '<g data-p="wl"><line class="wl" x1="12" y1="26" x2="' + (iw - 12) + '" y2="26"/><line class="wl" x1="32" y1="10" x2="32" y2="' + (ih - 10) + '"/>' +
      '<text class="ax" x="' + (iw - 14) + '" y="20" text-anchor="end">字线</text><text class="ax" x="38" y="' + (ih - 12) + '">位线</text></g>' +
      '<g data-p="cell"><line class="sch" x1="32" y1="66" x2="64" y2="66"/><line class="sch" x1="64" y1="58" x2="64" y2="74"/><line class="sch" x1="70" y1="58" x2="70" y2="74"/>' +
      '<line class="sch" x1="70" y1="66" x2="104" y2="66"/><line class="sch" x1="67" y1="26" x2="67" y2="56"/>' +
      '<line class="sch" x1="104" y1="66" x2="104" y2="76"/><line class="schc" x1="92" y1="76" x2="116" y2="76"/><line class="schc" x1="92" y1="82" x2="116" y2="82"/>' +
      '<line class="sch" x1="104" y1="82" x2="104" y2="92"/><line class="sch" x1="96" y1="92" x2="112" y2="92"/><line class="sch" x1="99" y1="96" x2="109" y2="96"/>' +
      '<circle class="dt" cx="32" cy="66" r="2"/><circle class="dt" cx="67" cy="26" r="2"/>' +
      '<text class="ax" x="58" y="52" text-anchor="end">晶体管</text><text class="ax" x="122" y="82">电容</text></g></g>';
    var vb = E.fit([[0, 0, 0], [200, 140, 0], [0, 140, 0], [200, 0, 0], [0, 0, 12]], 10);
    var y0 = Math.min(vb[1], iy - 8), x1 = Math.max(vb[0] + vb[2], ix + iw + 8);
    return { vb: [vb[0], y0, x1 - vb[0], vb[1] + vb[3] - y0], svg: s };
  };

  function stackScene(o) {
    return function (a) {
      var r = stackSvg(a, o), E = window.EX;
      return { vb: E.fit(r.pts.concat([[0, 0, 16 * (T + 2) + TB + 6]]), 12), svg: r.s };
    };
  }
  SC.stack = stackScene({});
  SC.base = stackScene({ apart: 0.3 });
  SC.ladder = stackScene({ apart: 0.12, strands: true });

  SC.bond = function (a) {
    var m = a.st.bond || 'mr', gap = a.val('gap', 14), film = a.val('film', 0), mold = a.val('mold', 1), bmp = a.val('bmp', 1), dmy = a.val('dmy', 1);
    var w = 300, L = 30, R2 = L + 240, dh = 34, s = '', y = 30, tsx = [60, 100, 140, 180, 220, 250 - 10];
    if (m === 'tc') s += '<g data-p="film"><rect class="press" x="' + (L + 20) + '" y="2" width="200" height="14" rx="3"/>' + [70, 150, 230].map(function (x) { return '<path class="arr" d="M' + x + ' 18 v8 m-4 -4 l4 4 l4 -4"/>'; }).join('') + '</g>';
    var dies = [];
    for (var i = 0; i < 3; i++) { dies.push(y); y += dh + gap; }
    // 填充（先画，位于 die 之间）
    for (i = 0; i < 2; i++) {
      var gy = dies[i] + dh;
      if (film > 0.01) s += '<rect class="filmr" data-p="film" style="opacity:' + film.toFixed(2) + '" x="' + L + '" y="' + gy + '" width="' + (R2 - L) + '" height="' + Math.max(gap, 0.1).toFixed(1) + '"/>';
      if (mold > 0.01) s += '<rect class="moldr" data-p="mold" style="opacity:' + mold.toFixed(2) + '" x="' + (L - 8) + '" y="' + gy + '" width="' + (R2 - L + 16) + '" height="' + Math.max(gap, 0.1).toFixed(1) + '"/>';
    }
    if (mold > 0.01) s += '<rect class="moldr" data-p="mold" style="opacity:' + (mold * 0.9).toFixed(2) + '" x="' + (L - 8) + '" y="' + dies[0] + '" width="8" height="' + (y - gap - dies[0]) + '"/><rect class="moldr" data-p="mold" style="opacity:' + (mold * 0.9).toFixed(2) + '" x="' + R2 + '" y="' + dies[0] + '" width="8" height="' + (y - gap - dies[0]) + '"/>';
    dies.forEach(function (yy, k) {
      s += '<g data-p="core"><rect class="sd" x="' + L + '" y="' + yy + '" width="' + (R2 - L) + '" height="' + dh + '"/>' +
        '<line class="sdl" x1="' + L + '" x2="' + R2 + '" y1="' + (yy + dh - 5) + '" y2="' + (yy + dh - 5) + '"/></g>';
      tsx.forEach(function (x) { s += '<rect class="tsvr" data-p="tsv" x="' + (x - 2.5) + '" y="' + yy + '" width="5" height="' + dh + '"/>'; });
      if (k < 2) {
        var gy = yy + dh;
        tsx.forEach(function (x) {
          if (bmp > 0.01) s += '<rect class="bumpr" data-p="bump" style="opacity:' + bmp.toFixed(2) + '" x="' + (x - 6) + '" y="' + gy + '" width="12" height="' + Math.max(gap, 0.1).toFixed(1) + '" rx="' + Math.min(5, gap / 2).toFixed(1) + '"/>';
          if (bmp < 0.99) s += '<rect class="padr" data-p="pad" style="opacity:' + (1 - bmp).toFixed(2) + '" x="' + (x - 5) + '" y="' + (gy - 3) + '" width="10" height="6"/>';
        });
        // MR-MUF 的导热假凸点
        if (dmy > 0.01) [80, 120, 160, 200].forEach(function (x) { s += '<rect class="bumpr dm" data-p="bump" style="opacity:' + dmy.toFixed(2) + '" x="' + (x - 4) + '" y="' + gy + '" width="8" height="' + Math.max(gap, 0.1).toFixed(1) + '" rx="3"/>'; });
        if (bmp < 0.5) s += '<line class="bondl" x1="' + L + '" x2="' + R2 + '" y1="' + gy + '" y2="' + gy + '"/>';
      }
    });
    if (m === 'mr') s += [70, 150, 230].map(function (x) { return '<path class="heatw" d="M' + x + ' ' + (y + 4) + ' q4 4 0 8 q-4 4 0 8"/>'; }).join('');
    return { vb: [0, 0, w, Math.max(y + 26, 180)], svg: s };
  };

  function pkgScene(neckOf) {
    return function (a) {
      var E = window.EX, it = [], g = a.gen(), n = a.val('n', g.layers), nf = Math.ceil(n - 1e-3);
      var neck = neckOf ? neckOf(g) : {};
      var sub = E.box({ x: 20, y: -26, z: -8, w: 300, d: 290, h: 8, k: 'sub', p: 'subs', depth: -1e9 });
      it.push(sub);
      // 基板上的小电容（细节）
      for (var c = 0; c < 6; c++) { it.push(E.box({ x: 30 + c * 48, y: 248, z: 0, w: 8, d: 5, h: 3, k: 'cap', p: 'subs' })); it.push(E.box({ x: 300, y: -10 + c * 44, z: 0, w: 5, d: 8, h: 3, k: 'cap', p: 'subs' })); }
      it.push(E.box({ x: 50, y: 0, z: 0, w: 240, d: 238, h: 6, k: 'interp', p: 'interp', cls: neck.interp ? 'neck' : '', depth: -1e8 }));
      var gx = 70, gy = 68, gw = 200, gd = 102, GH = 14;
      // 中介层走线（HBM → GPU）
      var tr = '';
      for (var k = 0; k < 4; k++) {
        var sx = 70 + k * 51 + 21;
        for (var q = -2; q <= 2; q++) { tr += E.line3([sx + q * 4, 58, 6], [sx + q * 4, gy, 6], 'trace', 'interp'); tr += E.line3([sx + q * 4, gy + gd, 6], [sx + q * 4, 180, 6], 'trace', 'interp'); }
      }
      it.push({ d: -1e7, z: 0, s: tr });
      var gi = '';
      for (var u = 1; u < 6; u++) gi += E.line3([gx + u * gw / 6, gy + 6, 6 + GH], [gx + u * gw / 6, gy + gd - 6, 6 + GH], 'grv', 'gpu');
      gi += E.line3([gx + gw / 2, gy + 3, 6 + GH], [gx + gw / 2, gy + gd - 3, 6 + GH], 'grv2', 'gpu');
      it.push(E.box({ x: gx, y: gy, z: 6, w: gw, d: gd, h: GH, k: 'gpu', p: 'gpu', inner: gi, cls: neck.gpu ? 'neck' : '' }));
      // 8 颗 HBM：总高和 GPU 平齐（逐层厚度 = 可用高度 / 层数，示意）
      [8, 180].forEach(function (yy) {
        for (var k = 0; k < 4; k++) {
          var x = 70 + k * 51, lt = (GH - 3) / Math.max(n, 1), ss = '';
          ss += E.box({ x: x, y: yy, z: 6, w: 42, d: 50, h: 3, k: g.base === 'DRAM' ? 'dram2' : 'logic', p: 'basedie', cls: neck.basedie ? 'neck' : '' }).s;
          for (var l = 0; l < nf; l++) ss += E.box({ x: x + 1, y: yy + 1, z: 9 + l * lt, w: 40, d: 48, h: lt * 0.86, k: 'dram', p: 'core', op: Math.min(1, n - l), cls: neck.core ? 'neck' : '' }).s;
          it.push({ d: x + 21 + yy + 25, z: 6, s: '<g data-p="stackp">' + ss + '</g>' });
        }
      });
      return { vb: E.fit([[20, -26, -8], [320, 264, -8], [20, 264, -8], [320, -26, -8], [70, 68, 30]], 8), svg: E.paint(it) };
    };
  }
  SC.pkg = pkgScene(null);
  var NECK = { HBM2E: { basedie: 1 }, HBM3: { core: 1 }, HBM3E: { core: 1 }, HBM4: { basedie: 1, interp: 1 }, HBM4E: { core: 1 } };
  SC.next = pkgScene(function (g) { return NECK[g.name] || {}; });

  SC.io = function (a) {
    var E = window.EX, g = a.gen(), it = [], s = '';
    var cw = a.st.calcW || g.io, chT = cw === g.io ? g.ch : cw / 64;
    var ch = a.val('ch', chT), cf = Math.ceil(ch - 1e-3);
    s += E.box({ x: -10, y: -6, z: 0, w: 280, d: 102, h: 6, k: 'interp', p: 'interp' }).s;
    var n = g.layers, lt = 22 / n, st = E.box({ x: 0, y: 12, z: 6, w: 64, d: 66, h: 4, k: g.base === 'DRAM' ? 'dram2' : 'logic', p: 'basedie' }).s;
    st += E.box({ x: 52, y: 16, z: 10, w: 10, d: 58, h: 0.8, k: 'phy', p: 'phy' }).s;
    for (var l = 0; l < n; l++) st += E.box({ x: 2, y: 14, z: 10 + l * lt, w: 46, d: 62, h: lt * 0.86, k: 'dram', p: 'core' }).s;
    s += st;
    var bits = cw / chT, cls = bits > 64 ? 'st2' : 'st';
    for (var c = 0; c < cf; c++) {
      var yy = 18 + (c + 0.5) * 56 / cf, op = Math.min(1, ch - c);
      s += '<g style="opacity:' + op.toFixed(2) + '">' + E.line3([62, yy, 6.2], [176, yy, 6.2], cls, 'strand') + E.dot3([62, yy, 6.2], 0.8, 'dt', 'strand') + E.dot3([176, yy, 6.2], 0.8, 'dt', 'strand') + '</g>';
    }
    var gi = '';
    for (var u = 1; u < 4; u++) gi += E.line3([176 + u * 20, 8, 22], [176 + u * 20, 82, 22], 'grv', 'gpu');
    s += E.box({ x: 176, y: 4, z: 6, w: 84, d: 82, h: 16, k: 'gpu', p: 'gpu', inner: gi }).s;
    return { vb: E.fit([[-10, -6, 0], [270, 96, 0], [-10, 96, 0], [270, -6, 0], [0, 12, 36]], 8), svg: s };
  };

  SC.hard = function (a) {
    var g = a.gen(), nn = a.st.yn || g.layers, n = a.val('yn', nn), nf = Math.ceil(n - 1e-3), p = a.val('p', 99) / 100;
    var w = 320, H = 230, B = 210, k = 0.24, L = 56, sw = 120, s = '';
    function Y(um) { return B - um * k; }
    // 标尺 0–800 µm
    s += '<g data-p="ruler"><line class="rl" x1="40" x2="40" y1="' + Y(0) + '" y2="' + Y(800) + '"/>';
    for (var u = 0; u <= 800; u += 100) s += '<line class="rl" x1="' + (u % 200 ? 36 : 32) + '" x2="40" y1="' + Y(u) + '" y2="' + Y(u) + '"/>' + (u % 200 ? '' : '<text class="ax" x="28" y="' + (Y(u) + 3) + '" text-anchor="end">' + u + '</text>');
    s += '<text class="ax" x="28" y="' + (Y(800) - 8) + '" text-anchor="end">µm</text>';
    [720, 775].forEach(function (lim) {
      var on = g.hlim === lim;
      s += '<line class="' + (on ? 'lim on' : 'lim') + '" x1="40" x2="' + (L + sw + 16) + '" y1="' + Y(lim) + '" y2="' + Y(lim) + '"/><text class="' + (on ? 'limt on' : 'limt') + '" x="' + (L + sw + 18) + '" y="' + (Y(lim) + 3) + '">' + lim + (lim === 720 ? '（≤HBM3E）' : '（HBM4）') + '</text>';
    });
    s += '</g>';
    // 堆栈（示意：层厚按上限平均分配）
    var lim = g.hlim || 720, bh = 40, avail = (lim - bh - 10) / Math.max(n, 1);
    s += '<rect class="sd base' + (g.base === 'DRAM' ? '' : ' lg') + '" data-p="basedie" x="' + L + '" y="' + Y(bh) + '" width="' + sw + '" height="' + (bh * k) + '"/>';
    for (var l = 0; l < nf; l++) {
      var z0 = bh + l * avail, op = Math.min(1, n - l);
      s += '<rect class="sd" data-p="core" style="opacity:' + op.toFixed(2) + '" x="' + L + '" y="' + Y(z0 + avail * 0.82) + '" width="' + sw + '" height="' + (avail * 0.82 * k).toFixed(2) + '"/>';
    }
    // 热流：从底座往上
    var gi = G.indexOf(g), hot = 0.35 + gi * 0.16;
    s += '<g data-p="heat" style="opacity:' + hot.toFixed(2) + '">' + [L + 24, L + 60, L + 96].map(function (x) { return '<path class="heatw" d="M' + x + ' ' + (Y(bh) - 4) + ' q5 -' + (avail * k * 2).toFixed(1) + ' 0 -' + (avail * k * 4).toFixed(1) + ' t0 -' + (avail * k * 4).toFixed(1) + '"/>'; }).join('') + '</g>';
    // 良率柱：p^n
    var yv = Math.pow(p, nn), bx = 262, bt = Y(800), bb = Y(0);
    s += '<rect class="ybg" x="' + bx + '" y="' + bt + '" width="26" height="' + (bb - bt) + '" rx="4"/><rect class="yfg" x="' + bx + '" y="' + (bb - (bb - bt) * yv).toFixed(1) + '" width="26" height="' + ((bb - bt) * yv).toFixed(1) + '" rx="4"/>';
    s += '<text class="ax" x="' + (bx + 13) + '" y="' + (bt - 6) + '" text-anchor="middle">整摞良率</text><text class="yv" x="' + (bx + 13) + '" y="' + (bb - (bb - bt) * yv - 6).toFixed(1) + '" text-anchor="middle">' + (yv * 100).toFixed(1) + '%</text>';
    return { vb: [0, Y(800) - 22, w, H + 4], svg: s };
  };

  /* ---------- 步内小部件 ---------- */
  var WD = {};
  WD.wall = function (el, a) {
    el.innerHTML = '<label class="ex-r">年份 <input type="range" min="0" max="20" step="1" value="20" aria-label="年份"><output></output></label><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    function up() {
      var t = +i.value, c = Math.pow(3, t / 2), b = Math.pow(1.6, t / 2);
      o.textContent = t + ' 年'; a.set('yr', t);
      p.innerHTML = t + ' 年后：算力 ×' + num(c) + '，带宽 ×' + num(b, b < 10 ? 1 : 0) + '，差距 ×' + num(c / b, c / b < 10 ? 1 : 0) + ' <span class="tag t-est">推算</span>';
    }
    i.addEventListener('input', up); up();
  };
  WD.apart = function (el, a) {
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="展开或压紧"><button type="button" data-v="1" aria-pressed="false">展开</button><button type="button" data-v="0" aria-pressed="true">压紧</button></div>';
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; a.set('apart', +b.dataset.v); el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); });
  };
  var BOND = { tc: { gap: 9, film: 1, mold: 0, bmp: 1, dmy: 0 }, mr: { gap: 12, film: 0, mold: 1, bmp: 1, dmy: 1 }, hb: { gap: 0, film: 0, mold: 0, bmp: 0, dmy: 0 } };
  var BONDRO = { tc: 'TC-NCF · 每层热压 · 三星 12H 层间 7 µm', mr: 'MR-MUF · 一次回流 + 灌模 · 焊点间距约 30 µm', hb: '混合键合 · 无凸点 · 间距 < 18 µm · 最早 HBM5' };
  function setBond(a, m) {
    a.st.bond = m; var v = BOND[m]; Object.keys(v).forEach(function (k) { a.set(k, v[k]); });
    document.querySelectorAll('.ex-bd').forEach(function (d) { d.hidden = d.dataset.m !== m; });
  }
  WD.bond = function (el, a) {
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="键合方式"><button type="button" data-m="tc" aria-pressed="false">TC-NCF</button><button type="button" data-m="mr" aria-pressed="true">MR-MUF</button><button type="button" data-m="hb" aria-pressed="false">混合键合</button></div>';
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; setBond(a, b.dataset.m); el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); });
    setBond(a, 'mr');
  };
  WD.calc = function (el, a) {
    el.innerHTML = '<div class="ex-seg" role="group" aria-label="线数"><button type="button" data-w="1024">1024 位</button><button type="button" data-w="2048">2048 位</button></div>' +
      '<label class="ex-r">每根线 <input type="range" min="1" max="16" step="0.1" aria-label="每根线速率 Gb/s"><output></output></label>' +
      '<label class="ex-r">几颗 <input type="range" min="1" max="12" step="1" value="8" aria-label="HBM 颗数"><output></output></label><p class="ex-o"></p>';
    var sp = el.querySelectorAll('input')[0], nk = el.querySelectorAll('input')[1], o1 = el.querySelectorAll('output')[0], o2 = el.querySelectorAll('output')[1], p = el.querySelector('.ex-o');
    function up() {
      var w = a.st.calcW, v = +sp.value, n = +nk.value, bw = w * v / 8;
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', +b.dataset.w === w ? 'true' : 'false'); });
      o1.textContent = v.toFixed(1) + ' Gb/s'; o2.textContent = n + ' 颗';
      p.innerHTML = w + ' × ' + v.toFixed(1) + ' ÷ 8 = <b>' + num(bw) + ' GB/s</b> 一颗；× ' + n + ' 颗 = <b>' + num(bw * n / 1000, 1) + ' TB/s</b> <span class="tag t-est">现算</span>';
      var g = a.gen(); a.set('ch', w === g.io ? g.ch : w / 64); a.update();
    }
    function fromGen() { var g = a.gen(); a.st.calcW = g.io; sp.value = a.speed(); up(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; a.st.calcW = +b.dataset.w; up(); });
    sp.addEventListener('input', up); nk.addEventListener('input', up);
    document.addEventListener('exgen', fromGen); fromGen();
  };
  WD.yield = function (el, a) {
    el.innerHTML = '<label class="ex-r">每层良率 <input type="range" min="95" max="99.9" step="0.1" value="99" aria-label="每层良率"><output></output></label>' +
      '<div class="ex-seg" role="group" aria-label="层数"><button type="button" data-n="8">8 层</button><button type="button" data-n="12">12 层</button><button type="button" data-n="16">16 层</button></div><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    function up() {
      var v = +i.value / 100, n = a.st.yn;
      o.textContent = (+i.value).toFixed(1) + '%'; a.set('p', +i.value); a.set('yn', n);
      el.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', +b.dataset.n === n ? 'true' : 'false'); });
      p.innerHTML = [8, 12, 16].map(function (k) { return (k === n ? '<b>' : '') + k + ' 层 ' + (Math.pow(v, k) * 100).toFixed(1) + '%' + (k === n ? '</b>' : ''); }).join(' · ') + ' <span class="tag t-est">纯算术示意，不是厂商良率</span>';
      a.update();
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; a.st.yn = +b.dataset.n; up(); });
    i.addEventListener('input', up);
    document.addEventListener('exgen', function () { a.st.yn = a.gen().layers; up(); });
    a.st.yn = a.gen().layers; up();
  };
  WD.ladder = function (el, a) {
    function card(g, k) {
      var cap = g.layers * g.dieGb / 8, b1 = g.io * g.std / 8, b2 = g.io * g.prod / 8;
      return '<button type="button" class="ex-gc' + (k === a.st.g ? ' on' : '') + '" data-g="' + k + '"><span class="ex-gn">' + g.name + '<small>' + g.year + '</small></span>' +
        '<span class="ex-gm"><span>' + g.layers + ' 层 × ' + g.dieGb + 'Gb = <b>' + cap + 'GB</b> ' + D.ref(g.src_cfg) + '</span>' +
        '<span>' + g.io + ' 位 · ' + g.ch + ' 通道</span>' +
        '<span>标准 ' + g.std + ' Gb/s ' + D.ref(g.src_std) + ' → ' + bwTxt(b1) + '</span>' +
        '<span>最快量产 ' + g.prod + ' Gb/s ' + D.ref(g.src_prod) + ' → <b>' + bwTxt(b2) + '</b></span>' +
        '<span>底座 ' + g.base + ' · 高度上限 ' + (g.hlim ? g.hlim + ' µm' : '未查到') + '</span>' +
        '<span>键合：' + g.bond + '</span></span>' +
        '<span class="ex-gu"><i>解锁</i>' + g.unlock + '</span><span class="ex-gu nk"><i>瓶颈</i>' + g.neck + '</span></button>';
    }
    function up() { el.innerHTML = '<div class="ex-gl">' + G.map(card).join('') + '</div>'; }
    el.addEventListener('click', function (e) { if (e.target.closest('a')) return; var b = e.target.closest('.ex-gc'); if (b) a.setGen(+b.dataset.g); });
    document.addEventListener('exgen', up); up();
  };
  WD.quiz = function (el) {
    el.innerHTML = D.quiz.map(function (q, k) { return '<details class="ex-q"><summary><b>' + (k + 1) + '.</b> ' + q[0] + '</summary><p>' + q[1] + '</p></details>'; }).join('');
  };

  function readout(a, s) {
    var g = a.gen(), cap = g.layers * g.dieGb / 8, v = a.speed();
    if (s.scene === 'wall') { var t = a.st.tgt.yr == null ? 20 : a.st.tgt.yr; return t + ' 年 · 差距 ×' + num(Math.pow(3 / 1.6, t / 2), 0); }
    if (s.scene === 'bond') return BONDRO[a.st.bond || 'mr'];
    if (s.scene === 'hard') return (g.hlim ? '上限 ' + g.hlim + ' µm · ' : '') + (a.st.yn || g.layers) + ' 层良率 ' + (Math.pow(a.val('p', 99) / 100, a.st.yn || g.layers) * 100).toFixed(1) + '%';
    if (s.scene === 'cell') return g.name + ' · 每层 ' + g.dieGb + 'Gb = ' + g.dieGb / 8 + 'GB';
    if (s.scene === 'next') return g.name + ' · 瓶颈见红色部件';
    return g.name + ' · ' + g.layers + '×' + g.dieGb + 'Gb=' + cap + 'GB · ' + g.io + '×' + v + '÷8 ≈ ' + bwTxt(g.io * v / 8);
  }

  window.EX.mount({
    steps: D.steps, gens: G, parts: PARTS, scenes: SC, widgets: WD, readout: readout,
    onGen: function (a) {
      a.set('n', a.gen().layers); a.set('ch', a.gen().ch);
      var s = D.steps[a.st.i]; if (s && s.scene === 'next' && !a.st.sel) { document.querySelector('.ex-info').innerHTML = '<b>' + a.gen().name + ' 的瓶颈</b>　' + a.gen().neck; }
    },
    onStep: function (a, s) {
      if (s.scene === 'stack' && a.st.tgt.apart == null) { a.set('apart', 1, true); a.set('apart', 0); }
      if (s.scene === 'next') { var g = a.gen(); var inf = document.querySelector('.ex-info'); inf.innerHTML = '<b>' + g.name + ' 的瓶颈</b>　' + g.neck; }
    }
  });
})();
