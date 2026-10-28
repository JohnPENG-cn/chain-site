/* 万物原理图 · PCB：部件说明、场景（俯视 / 等轴测 / 剖面 SVG）、步内小部件、实时读数。
 * 数据（平台、步骤文字、来源编号、打分卡、资本开支倍数）由 explain/build.py 从 explain/pcb.py 注入为 window.EXD。
 * 图中层厚、线宽、孔径为示意（不按比例）；损耗指数按 √Dk × Df 现算（推算），波形衰减与良率连乘为纯算术示意。 */
(function () {
  'use strict';
  var D = window.EXD, G = D.gens, E = window.EX, SN = D.sn || {};
  function R(k) { var n = SN[k]; if (!n) throw new Error('来源未登记 ' + k); return '<a class="sr" href="#src' + n + '">[' + n + ']</a>'; }
  function num(v, dp) { return (+v).toLocaleString('en-US', { maximumFractionDigits: dp == null ? 0 : dp, minimumFractionDigits: dp || 0 }); }
  var EST = ' <span class="tag t-est">估</span>', CALC = ' <span class="tag t-est">推算</span>', DEMO = ' <span class="tag t-est">示意</span>';
  function f1(x) { return (Math.round(x * 10) / 10).toFixed(1); }

  /* ---------- 材料与铜箔：松下典型值、三井路线图 ---------- */
  var MAT = [
    { k: 'M6', dk: 3.34, df: 0.0037, f: '13 GHz', s: 'm6' },
    { k: 'M7', dk: 3.31, df: 0.0023, f: '14 GHz', s: 'm7' },
    { k: 'M8', dk: 3.08, df: 0.0012, f: '14 GHz', s: 'm8' }
  ];
  var RZ = [['HVLP1', 1.5], ['HVLP2', 1.0], ['HVLP3', 0.6], ['HVLP4', 0.5], ['HVLP5', 0.4]];
  function lossIdx(m) { return Math.sqrt(m.dk) * m.df / (Math.sqrt(MAT[0].dk) * MAT[0].df) * 100; }
  function mat(a) { return MAT[a.st.mat == null ? 2 : a.st.mat]; }
  function rz(a) { return RZ[a.st.rz == null ? 3 : a.st.rz]; }

  /* ---------- 各类板的层数（有来源的才画） ---------- */
  var BOARDS = [
    { n: 'GB300 交换板', l: 24, p: 'b_sw', s: 'ms' },
    { n: 'Rubin 计算板（HDI）', l: 26, p: 'b_cmp', s: 'ms' },
    { n: 'Rubin 交换板', l: 32, p: 'b_sw', s: 'ms' },
    { n: 'TPU V7 主板（弱）', l: 36, p: 'b_tpu', s: 'tpu' },
    { n: 'Rubin 中板', l: 44, p: 'b_mid', s: 'ms' },
    { n: 'TPU V7P 主板（弱）', l: 44, p: 'b_tpu', s: 'tpu' },
    { n: 'Kyber 正交背板', l: 78, p: 'b_bp', s: 'kyber' }
  ];

  var FLOW = [
    ['开料 + 内层线路', '把覆铜板切成大板，贴感光膜、曝光、蚀刻，去掉不要的铜，留下内层线路。'],
    ['内层检查（AOI）', '用光学扫描找断线和短路。压进去以后就修不了了，所以这一步要查干净。'],
    ['压合', '芯板 + 半固化片 + 外层铜箔叠好，在真空里加热加压：树脂熔化再固化，粘成一整块。'],
    ['钻孔', '机械钻头打通孔，激光打盲孔。材料越硬，钻针磨得越快。'],
    ['沉铜 + 电镀', '先在孔壁化学沉一层薄铜，再电镀加厚，上下层就连通了。'],
    ['外层线路', '和内层一样曝光、蚀刻，做出表面的线路和焊盘。'],
    ['阻焊 + 表面处理', '刷阻焊漆，只在焊盘处开口；焊盘镀上金或别的涂层防氧化。'],
    ['电测 + 出货', '飞针或治具逐点测通断，再查外观，合格的才出货。']
  ];

  /* ---------- 部件：名称 + 一句话说明 ---------- */
  var PARTS = {
    board: { n: 'PCB 板', d: function () { return 'AI 服务器用的是高速多层板：Rubin 机柜里有 26 层计算板、32 层交换板、44 层中板 ' + R('ms') + '。'; } },
    chip: { n: '芯片', d: '焊在板上的 GPU、交换芯片或 CPU。芯片和主板之间还隔着一块 IC 载板（第 8 步）。' },
    pad: { n: '焊盘', d: '露在表面、不刷阻焊漆的铜块，芯片或载板底下的锡球焊在这里。' },
    trace: { n: '铜线（走线）', d: '蚀刻出来的铜线。高速信号成对走，叫差分对；信号越快，对材料损耗越敏感（第 5 步）。' },
    via: { n: '过孔', d: '孔壁镀铜的小孔，把信号从一层送到另一层（第 4 步）。' },
    mask: { n: '阻焊', d: '最外层的保护漆，防氧化、防焊锡乱流，只在焊盘处开口。' },
    cu: { n: '铜层', d: function () { return '蚀刻成线路的铜箔。AI 板用低粗糙度的 HVLP 铜箔，Rz 0.4–1.5 μm ' + R('tcf') + '。'; } },
    pp: { n: '半固化片（PP）', d: '浸了树脂、还没完全固化的玻纤布；压合时熔化，把各层粘成一块。' },
    core: { n: '芯板（覆铜板）', d: function () { return '两面贴铜、已经固化的板材，是整块板的骨架。高速覆铜板前三：台光电、生益、建滔 ' + R('iekccl') + '。'; } },
    foil: { n: '铜箔', d: function (a) { var r = rz(a); return r[0] + '：表面粗糙度 Rz ' + r[1] + ' μm ' + R('tcf') + '。越平，高频损耗越小；三井占 HVLP2 以上约 60% ' + R('mitjan') + '。'; } },
    cloth: { n: '玻纤布', d: function () { return '玻璃纤维织成的布，给板子强度。低介电布日东纺 55%、旭化成 31%、台玻 11% ' + R('hh') + '。'; } },
    resin: { n: '树脂', d: function () { return '把玻纤布粘成硬板；配方决定 Dk / Df。高端用 PPO、碳氢树脂 ' + R('sq') + R('dc') + '。份额待补。'; } },
    ccl: { n: '覆铜板（CCL）', d: function () { return '铜箔 + 玻纤布 + 树脂压成的板材；等级 M6 → M9。台光电 16.2%、生益 13.2%、建滔 12.4% ' + R('iekccl') + '。'; } },
    thru: { n: '通孔', d: '机械钻头打穿整块板，孔壁镀铜。简单，但占住了它穿过的每一层。' },
    blind: { n: '盲孔（激光孔）', d: '激光打的小锥形孔，只连表层和下面一两层，镀铜填平后可以叠起来；HDI 板的主角。' },
    buried: { n: '埋孔', d: '藏在板子中间、只连内层的孔，压合前先钻好、镀好。' },
    diel: { n: '绝缘介质', d: function (a) { var m = mat(a); return m.k + '：Dk ' + m.dk + ' / Df ' + m.df + '（' + m.f + '，典型值）' + R(m.s) + '。'; } },
    gnd: { n: '参考地层', d: '信号线下面一整片铜，给高速信号当回程的路。' },
    b_sw: { n: '交换板', d: function () { return 'GB300 24 层 → VR200 32 层，材料 M8 + 二代布（纪要，弱）' + R('ms') + R('doosan'); } },
    b_cmp: { n: '计算板', d: function () { return 'VR200 计算板 26 层 HDI，材料从 M7 升到 M8 ' + R('ms') + '；GB300 计算板层数待补。'; } },
    b_mid: { n: '中板', d: function () { return 'VR200 新增 44 层中板，每柜 18 块 ' + R('ms') + '；中板原计划 M9 + Q 布 ' + R('hf') + '。'; } },
    b_bp: { n: '正交背板', d: function () { return 'Kyber 计划 78 层（3 块 26 层压合）、约 1 m²；据报道推迟到 2028 年 ' + R('kyber') + '。'; } },
    b_tpu: { n: '谷歌 TPU 主板', d: function () { return 'V7 36 层、V7P 44 层（专家纪要，弱）' + R('tpu') + '。'; } },
    drill: { n: '钻针', d: function () { return 'M9 板上一根主钻针只能钻 100–200 个孔，M8 是 400–500 个 ' + R('uad') + '。'; } },
    bump: { n: '凸点', d: '芯片底下的微小焊点，间距比主板焊盘密得多，所以主板直接接不上。' },
    subs: { n: 'IC 载板', d: function () { return '小号、精密版的 PCB，把芯片的密集焊点放大到主板能接的间距；高端载板用味之素 ABF 膜（自述约 95%）' + R('ajiabf') + '。'; } },
    bga: { n: 'BGA 锡球', d: '载板底部的锡球阵列，把整个封装焊到主板上。' },
    capex: { n: '资本开支 ÷ 折旧', d: function () { var N = D.nums; return '10 家 A 股大板厂：' + N.pk + ' 年 ' + N.rPk + ' 倍，2026 年上半年 ' + N.rH1 + ' 倍 ' + R('tsfin') + '。大于 1 说明在净扩产。'; } }
  };

  function txt(x, y, s, cls, anchor) { return '<text class="' + (cls || 'ax') + '" x="' + f1(x) + '" y="' + f1(y) + '"' + (anchor ? ' text-anchor="' + anchor + '"' : '') + '>' + s + '</text>'; }
  function rect(x, y, w, h, cls, p, extra) { return '<rect class="' + cls + '"' + (p ? ' data-p="' + p + '"' : '') + ' x="' + f1(x) + '" y="' + f1(y) + '" width="' + f1(Math.max(0, w)) + '" height="' + f1(Math.max(0, h)) + '"' + (extra || '') + '/>'; }

  /* ---------- 场景 ---------- */
  var SC = {};
  SC.what = function () {
    var s = '';
    s += rect(10, 10, 300, 180, 'pcbt', 'board', ' rx="8"');
    // 走线（差分对）
    var tr = [[96, 70, 150, 70, 150, 46, 230, 46], [96, 76, 156, 76, 156, 52, 230, 52], [96, 120, 170, 120, 170, 150, 230, 150], [96, 126, 164, 126, 164, 156, 230, 156], [60, 150, 60, 176, 260, 176]];
    tr.forEach(function (t) { var d = 'M' + t[0] + ' ' + t[1]; for (var i = 2; i < t.length; i += 2) d += ' L' + t[i] + ' ' + t[i + 1]; s += '<path class="trc" data-p="trace" d="' + d + '"/>'; });
    // 焊盘
    for (var i = 0; i < 6; i++) for (var j = 0; j < 6; j++) s += rect(34 + i * 10, 64 + j * 10, 5, 5, 'padr', 'pad');
    s += rect(30, 60, 64, 64, 'sdie', 'chip', ' rx="3" style="fill-opacity:.55"') + txt(62, 96, 'GPU', 'vl', 'middle');
    s += rect(230, 30, 50, 34, 'sdie', 'chip', ' rx="3"') + txt(255, 51, '交换芯片', 'ax', 'middle');
    s += rect(230, 136, 50, 34, 'shbm', 'chip', ' rx="3"') + txt(255, 157, 'CPU', 'ax', 'middle');
    // 过孔
    [[150, 58], [156, 64], [170, 135], [164, 141], [60, 150], [200, 132], [210, 132], [120, 30]].forEach(function (v) { s += '<circle class="viah" data-p="via" cx="' + v[0] + '" cy="' + v[1] + '" r="2.6"/>'; });
    s += txt(160, 104, '俯视示意，不按比例', 'ax', 'middle');
    return { vb: [0, 0, 320, 200], svg: s };
  };

  SC.stack = function (a) {
    var nl = a.val('nl', 8), N = Math.round(nl), dn = Math.min(N, 12), ap = a.val('apart', 1), W = 150, Dd = 100, s = '', z = 0, items = '';
    function layer(z0, h, k, p, inner) { return E.box({ x: 0, y: 0, z: z0, w: W, d: Dd, h: h, k: k, p: p, inner: inner || '' }).s; }
    function gapz() { return ap * 2.4; }
    items += layer(z, 0.8, 'mask', 'mask'); z += 0.8 + gapz();
    for (var i = 0; i < dn; i++) {
      var inner = '';
      if (i % 2 === 1 || i === 0 || i === dn - 1) for (var q = 1; q < 6; q++) inner += E.line3([q * W / 6, 6, z + 0.6], [q * W / 6, Dd - 6, z + 0.6], 'grv', 'cu');
      items += layer(z, 0.6, 'cu', 'cu', inner); z += 0.6 + gapz();
      if (i < dn - 1) { var core = i % 2 === 0; items += layer(z, 1.8, core ? 'core' : 'pp', core ? 'core' : 'pp'); z += 1.8 + gapz(); }
    }
    items += layer(z, 0.8, 'mask', 'mask'); z += 0.8;
    s += items;
    var zmax = 0.8 + dn * 0.6 + (dn - 1) * 1.8 + 0.8 + (2 * dn) * 2.4;
    var Pt = E.P(W, 0, z + 2);
    s += txt(Pt[0] + 6, Pt[1], N + ' 层铜', 'vl');
    if (N > dn) s += txt(Pt[0] + 6, Pt[1] + 13, '图里只画 ' + dn + ' 层', 'ax');
    var Pb = E.P(W, Dd, 0);
    s += txt(Pb[0], Pb[1] + 14, '层厚为夸大示意', 'ax', 'end');
    return { vb: E.fit([[0, 0, 0], [W, Dd, 0], [0, Dd, 0], [W, 0, 0], [0, 0, zmax + 6], [W + 90, 0, zmax]], 12), svg: s };
  };

  SC.mat = function (a) {
    var s = '', r = rz(a), amp = r[1] * 9;
    // 铜箔剖面：底面齿形
    s += '<g data-p="foil">' + txt(10, 18, '铜箔剖面（' + r[0] + '，Rz ' + r[1] + ' μm；起伏放大示意）', 'bl');
    var d = 'M20 26 L300 26 L300 40';
    for (var x = 300; x >= 20; x -= 7) d += ' L' + (x - 3.5) + ' ' + f1(40 + amp * (0.6 + 0.4 * Math.sin(x * 1.7))) + ' L' + (x - 7) + ' 40';
    s += '<path class="cufill" d="' + d + ' Z"/></g>';
    // 玻纤布：经纬编织
    s += '<g data-p="cloth">' + txt(10, 72, '玻纤布（经纬编织，俯视示意）', 'bl');
    for (var i = 0; i < 4; i++) s += rect(20, 80 + i * 9, 130, 5, 'yarn', null, ' rx="2.5"');
    for (var j = 0; j < 10; j++) s += rect(24 + j * 13, 78 + (j % 2) * 2, 5, 36, 'yarn2', null, ' rx="2.5"');
    s += '</g>';
    // 树脂
    s += '<g data-p="resin">' + txt(170, 72, '树脂（把布粘成硬板）', 'bl') + rect(170, 78, 130, 38, 'resinf', null, ' rx="4"');
    for (i = 0; i < 22; i++) s += '<circle class="resd" cx="' + (178 + (i * 37) % 116) + '" cy="' + (84 + (i * 23) % 28) + '" r="1.6"/>';
    s += '</g>';
    // 覆铜板
    s += '<g data-p="ccl">' + txt(10, 136, '覆铜板 = 铜箔 + （玻纤布 + 树脂）+ 铜箔', 'bl');
    s += rect(20, 144, 280, 5, 'cufill') + rect(20, 149, 280, 28, 'resinf');
    for (x = 26; x < 296; x += 10) s += '<path class="weave" d="M' + x + ' 163 q2.5 -3 5 0 t5 0"/>';
    s += rect(20, 177, 280, 5, 'cufill') + '</g>';
    return { vb: [0, 4, 320, 186], svg: s };
  };

  var VIAM = { thru: '通孔板', hdi: 'HDI（盲孔 + 埋孔）', any: '任意层互连' };
  SC.via = function (a) {
    var m = a.st.via || 'thru', s = '', x0 = 14, x1 = 306, y0 = 22, g = 18, nL = 8;
    // 介质
    for (var i = 0; i < nL - 1; i++) s += rect(x0, y0 + i * g, x1 - x0, g, 'sd' + (i % 2 ? ' gp' : ''), i % 2 ? 'pp' : 'core');
    // 铜层（线路段）
    for (i = 0; i < nL; i++) {
      var y = y0 + i * g;
      for (var x = x0 + 4; x < x1 - 10; x += 26) s += rect(x + ((i * 7) % 13), y - 1.5, 14, 3, 'cuf', 'cu');
      s += txt(x1 + 2, y + 3, 'L' + (i + 1), 'ax');
    }
    function thru(cx) { s += '<g data-p="thru">' + rect(cx - 5, y0 - 4, 10, (nL - 1) * g + 8, 'cuf') + rect(cx - 3, y0 - 4, 6, (nL - 1) * g + 8, 'holef') + '</g>'; }
    function micro(cx, la, lb, p) { var ya = y0 + la * g, yb = y0 + lb * g, up = la < lb; s += '<polygon class="mvia" data-p="' + (p || 'blind') + '" points="' + (cx - 5) + ',' + ya + ' ' + (cx + 5) + ',' + ya + ' ' + (cx + 2.5) + ',' + yb + ' ' + (cx - 2.5) + ',' + yb + '"/>'; }
    function buried(cx, la, lb) { s += '<g data-p="buried">' + rect(cx - 4, y0 + la * g, 8, (lb - la) * g, 'cuf') + rect(cx - 2.2, y0 + la * g, 4.4, (lb - la) * g, 'holef') + '</g>'; }
    if (m === 'thru') { thru(80); thru(160); thru(240); }
    if (m === 'hdi') { thru(250); micro(60, 0, 1); micro(60, 1, 2); micro(60, 7, 6); micro(60, 6, 5); buried(140, 2, 5); micro(190, 0, 1); micro(190, 7, 6); }
    if (m === 'any') { [50, 120, 190].forEach(function (cx, k) { for (var l = 0; l < nL - 1; l++) micro(cx + ((l + k) % 2) * 10, l, l + 1); }); micro(250, 0, 1); micro(250, 1, 2); micro(260, 2, 3); }
    s += txt(x0, 12, VIAM[m] + '：8 层剖面（不按比例）', 'bl');
    return { vb: [0, 0, 320, y0 + (nL - 1) * g + 14], svg: s };
  };

  SC.sig = function (a) {
    var m = mat(a), r = rz(a), idx = lossIdx(m), s = '';
    // 剖面：信号线 + 介质 + 地层
    s += rect(40, 70, 240, 6, 'cuf', 'gnd') + txt(284, 76, '地层', 'ax');
    s += rect(40, 34, 240, 36, 'sd', 'diel') + txt(284, 56, m.k, 'ax');
    var amp = 1.5 + r[1] * 10, d = 'M130 34';
    for (var x = 130; x < 190; x += 4) d += ' L' + (x + 2) + ' ' + f1(34 + amp * (0.6 + 0.4 * Math.sin(x))) + ' L' + (x + 4) + ' 34';
    s += '<g data-p="trace">' + rect(130, 26, 60, 8, 'cuf') + txt(160, 20, '信号线（剖面）', 'ax', 'middle') + '</g>';
    s += '<g data-p="foil"><path class="cufill" d="' + d + ' Z"/>' + txt(196, 32, '← 铜面起伏（放大）', 'ax') + '</g>';
    // 波形：沿线衰减（示意）
    var k = idx / 100 * 1.6 + r[1] * 0.6, pd = 'M20 140', ph = a.val('ph', 0);
    for (x = 0; x <= 280; x += 2) { var A = 26 * Math.exp(-k * x / 280); pd += ' L' + (20 + x) + ' ' + f1(140 - A * Math.sin((x / 280) * 6 * Math.PI * 2 + ph)); }
    s += '<path class="wave" d="' + pd + '"/>' + '<line class="gl dsh" x1="20" y1="140" x2="300" y2="140"/>';
    s += txt(20, 104, '发送端', 'ax') + txt(300, 104, '接收端剩 ' + Math.round(100 * Math.exp(-k)) + '%（示意）', 'ax', 'end');
    s += txt(20, 186, m.k + ' 介质损耗指数 ' + Math.round(idx) + '（M6 = 100，推算）· 铜箔 ' + r[0], 'ax');
    return { vb: [0, 6, 320, 188], svg: s };
  };

  SC.why = function (a) {
    var s = '', sel = a.st.yl || 32, kx = 2.3, y = 20;
    s += txt(8, 12, '各类 AI 板的层数（来源见卡片）', 'ax');
    BOARDS.slice().sort(function (p, q) { return p.l - q.l; }).forEach(function (b) {
      s += '<g data-p="' + b.p + '">' + txt(8, y + 10, b.n, 'bl') + rect(118, y + 1, b.l * kx, 12, 'bar ' + (b.l === sel ? 'bad' : b.l >= 44 ? 'mid' : ''), null, ' rx="3"') + txt(122 + b.l * kx, y + 11, b.l, 'bv') + '</g>';
      y += 18;
    });
    y += 10;
    s += txt(8, y, '每柜 PCB 价值（万美元）', 'ax'); y += 6;
    [['GB300 NVL72', 3.51, ''], ['VR200 NVL72', 11.67, 'mid']].forEach(function (r) {
      s += '<g data-p="board">' + txt(8, y + 10, r[0], 'bl') + rect(118, y + 1, r[1] * 13, 12, 'bar ' + r[2], null, ' rx="3"') + txt(122 + r[1] * 13, y + 11, r[1], 'bv') + '</g>';
      y += 18;
    });
    return { vb: [0, 0, 320, y + 4], svg: s };
  };

  SC.make = function (a) {
    var st = a.st.flow || 1, sep = a.val('sep', 1), s = '', x0 = 30, x1 = 290, W = x1 - x0;
    var Y = 40, cu = 3, cr = 18, pp = 12, gap = sep * 14;
    // 层位置（从上到下）：L1 外层铜、PP、L2 芯板A L3、PP、L4 芯板B L5、PP、L6 外层铜
    var y = Y, L = [];
    function cuLayer(yy, pattern, outer) {
      if (!pattern) return rect(x0, yy, W, cu, 'cuf', 'cu');
      var o = '';
      for (var x = x0 + 6; x < x1 - 8; x += 24) o += rect(x + (outer ? 0 : 5), yy, outer ? 16 : 12, cu, 'cuf', 'cu');
      return o;
    }
    var pressed = st >= 3;
    if (pressed) { s += cuLayer(y, st >= 6, true); L.push(y); y += cu; s += rect(x0, y, W, pp, 'sd gp', 'pp'); y += pp; }
    else y += cu + pp - gap * 0.5;
    s += cuLayer(y, true); L.push(y); y += cu; s += rect(x0, y, W, cr, 'sd', 'core'); y += cr; s += cuLayer(y, true); L.push(y); y += cu;
    if (pressed) { s += rect(x0, y, W, pp, 'sd gp', 'pp'); y += pp; } else y += gap;
    s += cuLayer(y, true); L.push(y); y += cu; s += rect(x0, y, W, cr, 'sd', 'core'); y += cr; s += cuLayer(y, true); L.push(y); y += cu;
    if (pressed) { s += rect(x0, y, W, pp, 'sd gp', 'pp'); y += pp; s += cuLayer(y, st >= 6, true); L.push(y); y += cu; }
    var top = Y, bot = y;
    if (st >= 4) {
      [120, 210].forEach(function (cx) {
        s += '<g data-p="thru">' + (st >= 5 ? rect(cx - 5, top - (st >= 5 ? 1 : 0), 10, bot - top + 2, 'cuf') : '') + rect(cx - 3, top - 1, 6, bot - top + 2, 'holef') + '</g>';
      });
      var ya = top, yb = top + cu + pp;
      s += '<polygon class="' + (st >= 5 ? 'mvia' : 'holef') + '" data-p="blind" points="' + 66 + ',' + ya + ' ' + 76 + ',' + ya + ' ' + 73 + ',' + yb + ' ' + 69 + ',' + yb + '"/>';
      if (st === 4) s += '<g data-p="drill"><path class="drl" d="M117 ' + (top - 30) + ' L123 ' + (top - 30) + ' L123 ' + (top - 8) + ' L120 ' + (top - 2) + ' L117 ' + (top - 8) + ' Z"/></g>' + txt(130, top - 18, '钻针', 'ax');
    }
    if (st >= 7) {
      [[x0, 30], [86, 30], [130, 76], [220, 70]].forEach(function (m) { s += rect(m[0], top - 3, m[1], 3, 'maskf', 'mask'); s += rect(m[0], bot, m[1], 3, 'maskf', 'mask'); });
      [[64, 14], [116, 12], [206, 12]].forEach(function (p) { s += rect(p[0], top - 2, p[1], 2, 'padr', 'pad'); });
    }
    if (st === 2) { s += '<line class="scan" x1="' + (x0 + W * 0.62) + '" y1="' + (Y - 10) + '" x2="' + (x0 + W * 0.62) + '" y2="' + (bot + 10) + '"/>' + txt(x0 + W * 0.62 + 4, Y - 12, '光学扫描', 'ax'); }
    if (st === 3) { s += txt(160, top - 14, '↓ 加热加压 ↓', 'ax', 'middle') + txt(160, bot + 18, '↑', 'ax', 'middle'); }
    if (st >= 8) { [70, 122, 212].forEach(function (x) { s += '<line class="probe" x1="' + x + '" y1="' + (top - 30) + '" x2="' + x + '" y2="' + (top - 3) + '"/>'; }); s += txt(240, top - 16, '✓ 通断合格', 'okt'); }
    s += txt(8, 14, FLOW[st - 1][0] + '（6 层板剖面示意）', 'bl');
    return { vb: [0, 0, 320, 160], svg: s };
  };

  var LS = [['HDI mSAP（以前）', 30, 30, ''], ['HDI mSAP（走向）', 20, 20, ''], ['PCB 现在', 20, 35, ''], ['CoWoP 需要', 10, 10, 'cowop']];
  SC.sub = function (a) {
    var m = a.st.subm || 'abf', s = '';
    // 左：侧视叠层
    s += '<g data-p="chip">' + rect(40, 20, 80, 16, 'sdie', null, ' rx="2"') + txt(80, 31, '芯片', 'ax', 'middle') + '</g>';
    s += '<g data-p="bump">'; for (var i = 0; i < 14; i++) s += '<circle class="bumpr" cx="' + (44 + i * 5.5) + '" cy="39" r="1.7"/>'; s += '</g>';
    s += '<g data-p="subs">' + rect(22, 42, 116, 22, 'subr' + (m !== 'cowop' ? '' : ' dim')) ;
    for (i = 0; i < 5; i++) s += '<line class="cul" x1="26" x2="134" y1="' + (46 + i * 4) + '" y2="' + (46 + i * 4) + '"/>';
    s += txt(80, 56, m === 'cowop' ? 'CoWoP 想省掉这层' : 'IC 载板（ABF）', 'ax', 'middle') + '</g>';
    s += '<g data-p="bga">'; for (i = 0; i < 9; i++) s += '<circle class="bumpr dm" cx="' + (28 + i * 13) + '" cy="68" r="3.4"/>'; s += '</g>';
    s += '<g data-p="board">' + rect(8, 72, 144, 30, 'pcbt', null, ' rx="2"');
    for (i = 0; i < 3; i++) s += '<line class="cul2" x1="12" x2="148" y1="' + (80 + i * 8) + '" y2="' + (80 + i * 8) + '"/>';
    s += txt(80, 116, '主板 PCB（线更宽、层更多）', 'ax', 'middle') + '</g>';
    // 右：线宽 / 线距条纹（1 μm ≈ 0.9 px）
    s += txt(168, 14, '线宽 / 线距（μm，条纹示意）', 'ax');
    LS.forEach(function (r, k) {
      var y = 24 + k * 34, x = 168, st = '';
      while (x + r[1] * 0.9 <= 310) { st += rect(x, y + 12, r[1] * 0.9, 12, 'cuf'); x += (r[1] + r[2]) * 0.9; }
      s += '<g data-p="' + (r[3] === 'cowop' ? 'subs' : 'board') + '"' + (m === 'cowop' && r[3] === 'cowop' ? ' class="sel"' : '') + '>' + txt(168, y + 8, r[0] + ' ' + (r[3] === 'cowop' ? '≤' : '') + r[1] + '/' + r[2], 'bl') + st + '</g>';
    });
    return { vb: [0, 4, 320, 160], svg: s };
  };

  SC.gen = function (a) {
    var g = a.gen(), L = g.L, s = '', cx = 160;
    function hb(x, y, w, l, p, lab) {
      var h = l ? Math.max(4, l * 0.32) : 6;
      return '<g data-p="' + p + '">' + rect(x, y - h / 2, w, h, l ? 'pcbt' : 'pcbt tbd', null, ' rx="1.5"') + txt(x + w / 2, y - h / 2 - 3, lab + ' ' + (l ? l + ' 层' : '层数待补'), 'ax', 'middle') + '</g>';
    }
    function vb(x, y, h, l, p, lab) {
      var w = Math.max(5, l * 0.3);
      return '<g data-p="' + p + '">' + rect(x - w / 2, y, w, h, 'pcbt', null, ' rx="1.5"') + txt(x, y + h + 12, lab + ' ' + l + ' 层', 'vl', 'middle') + '</g>';
    }
    if (L.bp) {
      s += vb(cx, 22, 128, L.bp, 'b_bp', '正交背板');
      for (var i = 0; i < 4; i++) s += hb(40, 40 + i * 30, 100, L.cmp, 'b_cmp', i ? '' : '计算板');
      for (i = 0; i < 4; i++) s += hb(180, 40 + i * 30, 100, L.sw, 'b_sw', i ? '' : '交换板');
    } else if (L.mid) {
      s += vb(cx, 22, 128, L.mid, 'b_mid', '中板');
      for (i = 0; i < 4; i++) s += hb(36, 40 + i * 30, 104, L.cmp, 'b_cmp', i ? '' : '计算板（HDI）');
      for (i = 0; i < 4; i++) s += hb(180, 40 + i * 30, 104, L.sw, 'b_sw', i ? '' : '交换板');
    } else {
      for (i = 0; i < 3; i++) s += hb(30, 40 + i * 36, 110, L.cmp, 'b_cmp', i ? '' : '计算板');
      for (i = 0; i < 3; i++) s += hb(180, 40 + i * 36, 110, L.sw, 'b_sw', i ? '' : '交换板');
      s += txt(cx, 160, '没有中板', 'ax', 'middle');
    }
    s += txt(8, 12, g.name + ' · ' + g.year, 'bl') + txt(312, 12, '侧视示意', 'ax', 'end');
    s += txt(8, 192, '每柜 PCB：' + (g.rack ? '约 ' + g.rack + ' 万美元' : '待补') + ' · 高阶铜箔：' + (g.cuKg ? '约 ' + g.cuKg + ' kg' : '待补'), 'ax');
    return { vb: [0, 0, 320, 198], svg: s };
  };

  var WHO = [['board', '板厂', 'board'], ['ccl', '覆铜板', 'ccl'], ['cloth', '电子布', 'cloth'], ['foil', '铜箔', null], ['drill', '钻针', 'drill'], ['subs', 'IC 载板', 'sub']];
  function scoreOf(k) { var r = (D.score || []).filter(function (x) { return x.k === k; })[0]; return r; }
  SC.who = function (a) {
    var s = '', cur = a.st.who || 'board', kx = 36, y = 22;
    s += txt(8, 12, '打分卡平均分（1–5，越高越像结构性）', 'ax');
    for (var v = 1; v <= 5; v++) s += '<line class="gl dsh" x1="' + (84 + v * kx) + '" x2="' + (84 + v * kx) + '" y1="18" y2="' + (22 + WHO.length * 24) + '"/>' + txt(84 + v * kx, 30 + WHO.length * 24, v, 'ax', 'middle');
    WHO.forEach(function (w) {
      var r = w[2] ? scoreOf(w[2]) : null, on = w[0] === cur;
      s += '<g data-p="' + w[0] + '"' + (on ? ' class="sel"' : '') + '>' + txt(8, y + 11, w[1], 'bl');
      if (r) s += rect(84, y + 2, r.avg * kx, 13, 'bar ' + (on ? 'bad' : r.avg >= 3.5 ? 'okb' : r.avg >= 3 ? 'mid' : ''), null, ' rx="3"') + txt(88 + r.avg * kx, y + 12, r.avg, 'bv');
      else s += txt(88, y + 12, '未单独打分', 'ax');
      s += '</g>'; y += 24;
    });
    return { vb: [0, 0, 320, y + 18], svg: s };
  };

  SC.watch = function () {
    var N = D.nums, s = '', rows = [[N.pk + ' 年（上一轮高点）', +N.rPk, 'mid'], ['2026 年上半年', +N.rH1, 'bad']], kx = 26;
    s += txt(8, 14, '10 家 A 股大板厂：资本开支 ÷ 折旧（倍）', 'ax');
    s += '<line class="gl dsh" x1="' + (120 + kx) + '" x2="' + (120 + kx) + '" y1="20" y2="84"/>' + txt(120 + kx, 96, '1 倍 = 只补旧', 'ax', 'middle');
    rows.forEach(function (r, k) { var y = 26 + k * 28; s += '<g data-p="capex">' + txt(8, y + 12, r[0], 'bl') + rect(120, y + 2, r[1] * kx, 14, 'bar ' + r[2], null, ' rx="3"') + txt(124 + r[1] * kx, y + 13, r[1] + '×', 'bv') + '</g>'; });
    s += txt(8, 120, '新厂大多 2–3 年后集中投产：到时需求接不接得住，', 'ax') + txt(8, 134, '是研究页的主要矛盾。', 'ax');
    return { vb: [0, 0, 320, 142], svg: s };
  };

  /* ---------- 步内小部件 ---------- */
  var WD = {};
  function showBd(el, m) { var sec = el.closest('.ex-step'); if (sec) sec.querySelectorAll('.ex-bd').forEach(function (d) { d.hidden = d.dataset.m !== m; }); }
  function seg(label, items) { return '<div class="ex-seg" role="group" aria-label="' + label + '">' + items.map(function (x) { return '<button type="button" data-v="' + x[0] + '" aria-pressed="false"' + (x[2] ? ' disabled' : '') + '>' + x[1] + '</button>'; }).join('') + '</div>'; }
  function press(el, sel, v) { el.querySelectorAll(sel).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === String(v) ? 'true' : 'false'); }); }
  function inStep(a, sc) { return D.steps[a.st.i] && D.steps[a.st.i].scene === sc; }

  var LAYB = [[4, '4 层（示意）', null], [24, 'GB300 交换板', 'ms'], [26, 'Rubin 计算板', 'ms'], [32, 'Rubin 交换板', 'ms'], [36, 'TPU V7（弱）', 'tpu'], [44, 'Rubin 中板', 'ms'], [78, 'Kyber 背板', 'kyber']];
  WD.layers = function (el, a) {
    el.innerHTML = '<div class="ex-seg lay" role="group" aria-label="层数">' + LAYB.map(function (x) { return '<button type="button" data-v="' + x[0] + '" aria-pressed="false">' + x[0] + '</button>'; }).join('') + '</div>' +
      '<div class="ex-seg ap" role="group" aria-label="展开或压紧"><button type="button" data-a="1" aria-pressed="true">展开</button><button type="button" data-a="0" aria-pressed="false">压紧</button></div><p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(v) {
      var b = LAYB.filter(function (x) { return x[0] === v; })[0];
      a.set('nl', v); press(el, '.lay button', v);
      p.innerHTML = '<b>' + v + ' 层</b>：' + b[1] + (b[2] ? ' ' + R(b[2]) : '') + '。层数 = 铜层数；芯板和半固化片交替夹在中间。';
    }
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.a != null) { a.set('apart', +b.dataset.a); el.querySelectorAll('.ap button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); }
      else up(+b.dataset.v);
    });
    up(24);
  };
  var MATB = [['foil', '铜箔'], ['cloth', '玻纤布'], ['resin', '树脂'], ['ccl', '覆铜板']];
  WD.mat = function (el, a) {
    el.innerHTML = seg('原料', MATB);
    function up(m) { press(el, 'button', m); showBd(el, m); a.st.matm = m; if (inStep(a, 'mat')) a.select(m); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    press(el, 'button', 'foil');
  };
  var VIAT = {
    thru: '通孔：一钻到底，最便宜；但每个孔都占住了全部 8 层的这个位置，线排不密。',
    hdi: 'HDI：表层用激光盲孔（可以叠起来连 2–3 层），中间用埋孔；省出来的位置可以多走线。',
    any: '任意层：每相邻两层都用激光孔连，线最密；每层都要“压合 → 钻 → 镀”一轮，工序最多。'
  };
  WD.via = function (el, a) {
    el.innerHTML = seg('过孔方式', [['thru', '通孔'], ['hdi', 'HDI'], ['any', '任意层']]) + '<p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(m) { a.st.via = m; press(el, 'button', m); p.innerHTML = VIAT[m]; a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    up('thru');
  };
  WD.loss = function (el, a) {
    el.innerHTML = seg('覆铜板等级', MAT.map(function (m, k) { return [k, m.k]; }).concat([['m9', 'M9 待补', true]])) +
      seg('铜箔等级', RZ.map(function (r, k) { return [k, r[0]]; })) + '<p class="ex-o"></p>';
    var segs = el.querySelectorAll('.ex-seg'), p = el.querySelector('.ex-o');
    a.st.mat = 2; a.st.rz = 3;
    function up() {
      var m = mat(a), r = rz(a), idx = lossIdx(m);
      press(segs[0], 'button', a.st.mat); press(segs[1], 'button', a.st.rz);
      p.innerHTML = '<b>' + m.k + '</b>：Dk ' + m.dk + '、Df ' + m.df + '（' + m.f + '）' + R(m.s) + '；介质损耗指数 <b>' + Math.round(idx) + '</b>（M6 = 100）' + CALC +
        '<br><b>' + r[0] + '</b>：铜面粗糙度 Rz ' + r[1] + ' μm ' + R('tcf') + '<br><small>指数按 √Dk × Df 现算，只比相对大小；图中波形衰减把两种损耗合在一起画，是示意，不是实测插损。</small>';
      a.set('ph', 0, true); a.update();
    }
    segs[0].addEventListener('click', function (e) { var b = e.target.closest('button'); if (b && !b.disabled) { a.st.mat = +b.dataset.v; up(); } });
    segs[1].addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { a.st.rz = +b.dataset.v; up(); } });
    up();
  };
  var YL = [24, 26, 32, 44, 78];
  WD.yield = function (el, a) {
    el.innerHTML = '<label class="ex-r">每层良率 <input type="range" min="97" max="99.9" step="0.1" value="99.5" aria-label="每层良率"><output></output></label>' +
      seg('层数', YL.map(function (l) { return [l, l + ' 层']; })) + '<p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    a.st.yl = 32;
    function up() {
      var y = +i.value / 100, n = a.st.yl, t = Math.pow(y, n);
      o.textContent = (+i.value).toFixed(1) + '%'; press(el, 'button', n);
      p.innerHTML = n + ' 层，每层 ' + (+i.value).toFixed(1) + '% → 整块 ≈ ' + (+i.value).toFixed(1) + '%<sup>' + n + '</sup> = <b>' + (t * 100).toFixed(1) + '%</b>' + DEMO +
        '<br><small>纯算术：假设每层出错互不相关，没算压合、钻孔、电镀各自的损失；不是任何厂商的良率。</small>';
      a.update();
    }
    i.addEventListener('input', up);
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { a.st.yl = +b.dataset.v; up(); } });
    up();
  };
  WD.flow = function (el, a) {
    el.innerHTML = '<label class="ex-r">工序 <input type="range" min="1" max="8" step="1" value="1" aria-label="工序"><output></output></label><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    function up() {
      var st = +i.value; a.st.flow = st; a.set('sep', st >= 3 ? 0 : 1);
      o.textContent = st + ' / 8'; p.innerHTML = '<b>' + FLOW[st - 1][0] + '</b>　' + FLOW[st - 1][1];
      a.update();
    }
    i.addEventListener('input', up); up();
  };
  WD.sub = function (el, a) {
    el.innerHTML = seg('载板', [['abf', 'ABF 膜'], ['mkt', '市场与玩家'], ['cowop', 'CoWoP']]);
    function up(m) { a.st.subm = m; press(el, 'button', m); showBd(el, m); if (inStep(a, 'sub')) a.select('subs'); a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    a.st.subm = 'abf'; press(el, 'button', 'abf');
  };
  WD.ladder = function (el, a) {
    function card(g, k) {
      return '<button type="button" class="ex-gc' + (k === a.st.g ? ' on' : '') + '" data-g="' + k + '"><span class="ex-gn">' + g.name + '<small>' + g.arch + ' · ' + g.year + '</small></span>' +
        '<span class="ex-gm"><span>' + g.boards + '</span><span>材料：' + g.mat + '</span><span>铜箔：' + g.cu + '</span><span>' + g.val + '</span></span>' +
        '<span class="ex-gu"><i>解锁</i>' + g.unlock + '</span><span class="ex-gu nk"><i>瓶颈</i>' + g.neck + '</span>' + (g.note ? '<span class="ex-gu"><i class="nt">注</i>' + g.note + '</span>' : '') + '</button>';
    }
    function up() { el.innerHTML = '<div class="ex-gl">' + G.map(card).join('') + '</div>'; }
    el.addEventListener('click', function (e) { if (e.target.closest('a')) return; var b = e.target.closest('.ex-gc'); if (b) a.setGen(+b.dataset.g); });
    document.addEventListener('exgen', up); up();
  };
  WD.who = function (el, a) {
    el.innerHTML = seg('环节', WHO.map(function (w) { return [w[0], w[1]]; }));
    function up(m) { a.st.who = m; press(el, 'button', m); showBd(el, m); if (inStep(a, 'who')) a.select(m); a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    a.st.who = 'board'; press(el, 'button', 'board');
  };
  WD.quiz = function (el) {
    el.innerHTML = D.quiz.map(function (q, k) { return '<details class="ex-q"><summary><b>' + (k + 1) + '.</b> ' + q[0] + '</summary><p>' + q[1] + '</p></details>'; }).join('');
  };

  function readout(a, s) {
    var g = a.gen();
    if (s.scene === 'what') return '2026E 全球 PCB 1,134 亿美元';
    if (s.scene === 'stack') { var n = Math.round(a.st.tgt.nl || 24); return n + ' 层铜 · ' + (n - 1) + ' 层绝缘'; }
    if (s.scene === 'mat') { var r = rz(a); return '铜箔 ' + r[0] + ' · Rz ' + r[1] + ' μm'; }
    if (s.scene === 'via') return VIAM[a.st.via || 'thru'];
    if (s.scene === 'sig') { var m = mat(a); return m.k + ' · Df ' + m.df + ' · 指数 ' + Math.round(lossIdx(m)) + ' · ' + rz(a)[0]; }
    if (s.scene === 'why') return '每柜 PCB 3.51 → 11.67 万美元';
    if (s.scene === 'make') return (a.st.flow || 1) + ' / 8 · ' + FLOW[(a.st.flow || 1) - 1][0];
    if (s.scene === 'sub') return 'CoWoP 要 ≤10/10 μm';
    if (s.scene === 'gen') return g.name + ' · ' + (g.rack ? '每柜 PCB ≈ ' + g.rack + ' 万美元' : '每柜 PCB 待补');
    if (s.scene === 'who') { var w = WHO.filter(function (x) { return x[0] === (a.st.who || 'board'); })[0], sc = w[2] ? scoreOf(w[2]) : null; return w[1] + (sc ? ' · ' + sc.avg + ' 分 · ' + sc.v : ' · 未单独打分'); }
    if (s.scene === 'watch') return '资本开支 ÷ 折旧 ' + D.nums.rH1 + '×（' + D.nums.pk + ' 年 ' + D.nums.rPk + '×）';
    return g.name;
  }

  window.EX.mount({
    steps: D.steps, gens: G, parts: PARTS, scenes: SC, widgets: WD, readout: readout,
    onStep: function (a, s) {
      if (s.scene === 'stack' && a.st.tgt.apart == null) { a.set('apart', 0, true); a.set('apart', 1); }
    }
  });
})();
