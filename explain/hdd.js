/* 万物原理图 · HDD：部件说明、场景（俯视 / 剖面 SVG）、步内小部件、实时读数。
 * 数据（代际、步骤文字、来源编号）由 explain/build.py 从 explain/hdd.py 注入为 window.EXD。
 * 图中盘片、磁头、磁粒都不按比例；成本计算只做“每 TB 价格 × 容量”的算术（推算），不是 TCO。 */
(function () {
  'use strict';
  var D = window.EXD, G = D.gens, E = window.EX, SN = D.sn || {};
  function R(k) { var n = SN[k]; if (!n) throw new Error('来源未登记 ' + k); return '<a class="sr" href="#src' + n + '">[' + n + ']</a>'; }
  function num(v, dp) { return (+v).toLocaleString('en-US', { maximumFractionDigits: dp == null ? 0 : dp, minimumFractionDigits: dp || 0 }); }
  var EST = ' <span class="tag t-est">估</span>', CALC = ' <span class="tag t-est">推算</span>', DEMO = ' <span class="tag t-est">示意</span>';
  function f1(x) { return (Math.round(x * 10) / 10).toFixed(1); }
  function txt(x, y, s, cls, anchor) { return '<text class="' + (cls || 'ax') + '" x="' + f1(x) + '" y="' + f1(y) + '"' + (anchor ? ' text-anchor="' + anchor + '"' : '') + '>' + s + '</text>'; }
  function rect(x, y, w, h, cls, p, extra) { return '<rect class="' + cls + '"' + (p ? ' data-p="' + p + '"' : '') + ' x="' + f1(x) + '" y="' + f1(y) + '" width="' + f1(Math.max(0, w)) + '" height="' + f1(Math.max(0, h)) + '"' + (extra || '') + '/>'; }
  function circ(cx, cy, r, cls, p) { return '<circle class="' + cls + '"' + (p ? ' data-p="' + p + '"' : '') + ' cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="' + f1(r) + '"/>'; }

  /* ---------- 价格（每 TB，美元）：专家纪要 2026 年口径（弱）；TrendForce HDD 口径 ---------- */
  var PX = { hdd: 16.0, ssd: 243.4 };   // 0.0160 / 0.2434 美元每 GB × 1000
  /* ---------- 路线图节点：[公司, 年份(x), 容量 TB, 标签, 来源, 部件, 是否无年份] ---------- */
  // [厂, 年, TB, 全称, 来源, 部件, 待补?, 图上短标签, dx, dy, 对齐]
  var ROAD = [
    ['stx', 2024, 30, '希捷 30TB（HAMR）', 'moz3pr', 'p_stx', false, '希捷 30TB', 0, 14, 'middle'],
    ['stx', 2026, 44, '希捷 44TB（HAMR）', 'moz4', 'p_stx', false, '希捷 44TB', 0, -8, 'middle'],
    ['wdc', 2026.5, 40, 'WD 40TB（ePMR）', 'wdc_t', 'p_wdc', false, 'WD 40TB', -2, 14, 'end'],
    ['tsb', 2027, 40, '东芝 40TB 级（MAMR）', 'tsbr', 'p_tsb', false, '东芝 40TB 级', 4, 14, null],
    ['tsb', 2028, 45, '东芝 45TB（HAMR）', 'tsbr', 'p_tsb', false, '东芝 45TB', 8, 3, null],
    ['tsb', 2030, 55, '东芝约 55TB', 'tsbr', 'p_tsb', false, '东芝约 55TB', -8, -6, 'end'],
    ['stx', 2030.8, 100, '希捷每碟 10TB ≈ 100TB（年份待补）', 'moz', 'p_stx', true, '希捷 ≈100TB（年份待补）', -8, 3, 'end']
  ];
  var CO = { stx: '希捷', wdc: '西部数据', tsb: '东芝' };
  var LT = [['bal', '供需平衡', 16, 'tf_lt'], ['s25', '2025 年 9 月', 52, 'tf_52'], ['now', '最新', 50, 'tf_lt']];

  /* ---------- 部件：名称 + 一句话说明 ---------- */
  var PARTS = {
    platter: { n: '盘片', d: function () { return '镀了磁性薄膜的圆盘，两面都能存。数据中心盘一般 9–10 张，空气盘最多 6 张、氦气盘最多 10 张 ' + R('he') + '。'; } },
    spindle: { n: '主轴电机', d: function () { return '让所有盘片一起高速旋转。尼得科占全球 70% 以上 ' + R('nidec') + '。'; } },
    arm: { n: '磁头臂', d: '一叠细长的臂，每面盘片配一根，末端装着磁头；所有臂一起转动。' },
    head: { n: '磁头', d: function () { return '前面是写头（小电磁铁），后面是读头（感应磁场）。离盘面只有几埃 ' + R('moz3') + '。'; } },
    vcm: { n: '音圈电机（VCM）', d: '线圈夹在两块强磁钢中间，通电就转，推着磁头臂精确定位。磁钢用钕铁硼。' },
    pcb: { n: '电路板', d: '装在硬盘背面：控制芯片、缓存和电机驱动，负责定位、纠错和接口。' },
    writer: { n: '写头', d: '一块微型电磁铁。电流方向一变，下面磁粒的方向就跟着翻。' },
    reader: { n: '读头', d: function () { return '利用隧穿磁阻（TMR）：磁场方向不同，电阻不同，于是读出 1 或 0 ' + R('moz3') + '。'; } },
    grain: { n: '磁粒', d: function () { return '磁性层里极小的颗粒。希捷 HAMR 介质是铁铂合金，磁粒只有几纳米 ' + R('moz3') + '。一个比特由一小撮磁粒组成。'; } },
    track: { n: '磁道', d: function () { return '一圈一圈的数据“跑道”。希捷 HAMR 盘每英寸超过 100 万条 ' + R('moz3') + '。'; } },
    gap: { n: '磁道间隙', d: function () { return 'CMR 在磁道之间留的空隙，防止写一条时擦掉旁边那条 ' + R('smr') + '。'; } },
    zone: { n: '区（zone）', d: function () { return 'SMR 把叠在一起的磁道编成一个个“区”，区和区之间留缝；改数据要整区重写 ' + R('smr') + '。'; } },
    gas: { n: '盘腔里的气体', d: function () { return '氦气密度约为空气的 1/7，乱流小、发热少 ' + R('he') + '。'; } },
    seal: { n: '密封外壳', d: function () { return '氦原子很小，容易漏，外壳要完全密封 ' + R('he') + '。'; } },
    laser: { n: '激光器', d: function () { return '装在磁头上的微型激光器。纪要称索尼约占希捷 HAMR 激光器的 60%（弱）' + R('jpm') + '。'; } },
    nft: { n: '近场“天线”', d: function () { return '把光挤到比波长还小的一点，不到 2 纳秒加热到约 430°C 以上 ' + R('moz3') + '。'; } },
    media: { n: '铁铂磁性层', d: function () { return '铁铂超晶格合金，常温下很“硬”、很稳，加热后才写得动 ' + R('moz3') + '。'; } },
    glass: { n: '玻璃基板', d: function () { return 'HAMR 必须用玻璃基板；HOYA 自称是唯一的硬盘玻璃基板厂 ' + R('hoya') + '。'; } },
    p_stx: { n: '希捷', d: function () { return '本季营收 42.33 亿美元，非 GAAP 毛利率 57.8% ' + R('stx_q') + '；HAMR 量产最早。'; } },
    p_wdc: { n: '西部数据', d: function () { return '本季营收 43.8 亿美元，非 GAAP 毛利率 58.1% ' + R('wdc_q') + '；HAMR 2027 年上半年量产 ' + R('wdc_t') + '。'; } },
    p_tsb: { n: '东芝', d: function () { return '三家里最小（2025 年台数约 17%，弱）' + R('cough') + '；先走 MAMR + 12 碟 ' + R('tsbr') + '。'; } },
    b_hdd: { n: 'HDD', d: function () { return '每 GB 约 0.016 美元（2026 年，纪要，弱）' + R('jpm') + '。'; } },
    b_ssd: { n: '企业级 SSD', d: function () { return '每 GB 约 0.243 美元（2026 年，纪要，弱）' + R('jpm') + '；胜在速度和功耗 ' + R('tf_px') + '。'; } },
    b_lt0: { n: '平衡时交期', d: function () { return '约 16 周 ' + R('tf_lt') + '。'; } },
    b_lt1: { n: '缺货时交期', d: function () { return '约 50 周，2025 年 9 月一度超过 52 周 ' + R('tf_lt') + R('tf_52') + '。'; } },
    m_drive: { n: '整机三家', d: function () { return '2025 年台数：西部数据 42.3%、希捷 40.8%、东芝 17.0%（弱）' + R('cough') + '。'; } },
    m_head: { n: '磁头', d: function () { return '希捷、西部数据自制，TDK 对外卖（弱）' + R('lb') + '。'; } },
    m_media: { n: '介质（盘片）', d: function () { return 'Resonac 是唯一对外卖介质的厂 ' + R('reso') + '。'; } },
    m_sub: { n: '玻璃基板', d: function () { return 'HOYA 自称唯一；HAMR 必须用玻璃 ' + R('hoya') + '。'; } },
    m_motor: { n: '主轴电机', d: function () { return '尼得科 70% 以上 ' + R('nidec') + '。'; } },
    m_mag: { n: 'VCM 磁钢', d: '钕铁硼永磁；A 股宁波韵升供应 VCM 磁材，份额待补。' }
  };

  /* ---------- 场景 ---------- */
  var SC = {};
  SC.what = function () {
    var s = '';
    s += '<g data-p="seal">' + rect(8, 8, 304, 184, 'hcase', null, ' rx="10"') + '</g>';
    s += '<g data-p="pcb">' + rect(16, 160, 92, 24, 'pcbt tbd', null, ' rx="3"') + txt(62, 176, '背面：电路板', 'ax', 'middle') + '</g>';
    s += '<g data-p="platter">' + circ(124, 92, 78, 'plat');
    for (var r = 30; r < 76; r += 8) s += circ(124, 92, r, 'gl dsh');
    s += '</g>';
    s += '<g data-p="spindle">' + circ(124, 92, 14, 'spin') + txt(124, 95, '主轴', 'ax', 'middle') + '</g>';
    s += '<g data-p="vcm"><path class="vcmf" d="M262 128 L300 112 L304 168 L268 176 Z"/>' + txt(286, 186, '音圈电机', 'ax', 'middle') + '</g>';
    s += '<g data-p="arm"><path class="armf" d="M270 150 L176 70 L170 76 L262 160 Z"/>' + circ(266, 154, 7, 'spin') + '</g>';
    s += '<g data-p="head">' + rect(160, 62, 14, 10, 'headr', null, ' rx="2" transform="rotate(40 167 67)"') + txt(150, 52, '磁头', 'vl', 'middle') + '</g>';
    s += txt(190, 186, '俯视示意，不按比例', 'ax', 'middle');
    return { vb: [0, 0, 320, 200], svg: s };
  };

  function bits(a) { return a.st.bits || [0, 1, 0, 0, 1, 0, 0, 0]; }
  SC.bit = function (a) {
    var b = bits(a), mode = a.st.bm || 'w', s = '', x0 = 20, gw = 34, y = 110;
    s += txt(8, 14, mode === 'w' ? '写：写头的磁场把下方磁粒“拧”成朝上(1)或朝下(0)' : '读：读头经过时，电阻随磁场方向变化', 'bl');
    s += '<g data-p="track">' + rect(x0 - 6, y - 6, gw * 8 + 12, 44, 'trkb', null, ' rx="3"') + '</g>';
    for (var i = 0; i < 8; i++) {
      var up = b[i] === 1, x = x0 + i * gw;
      s += '<g data-p="grain">';
      for (var g = 0; g < 3; g++) s += rect(x + 2 + g * 10, y, 9, 32, up ? 'grU' : 'grD', null, ' rx="2"');
      s += txt(x + gw / 2 - 1, y + 21, up ? '↑' : '↓', 'vl', 'middle') + txt(x + gw / 2 - 1, y + 50, String(b[i]), 'bv', 'middle') + '</g>';
    }
    var hx = x0 + (a.st.bpos == null ? 3 : a.st.bpos) * gw;
    s += '<g data-p="writer">' + rect(hx - 4, 58, 18, 40, 'headr' + (mode === 'w' ? ' on' : ' dim'), null, ' rx="2"') + txt(hx + 5, 52, '写头', 'ax', 'middle') + '</g>';
    if (mode === 'w') s += '<path class="field" d="M' + (hx + 1) + ' 98 q0 12 8 12 q8 0 8 -12"/>';
    s += '<g data-p="reader">' + rect(hx + 22, 64, 8, 34, 'readr' + (mode === 'r' ? ' on' : ' dim'), null, ' rx="1.5"') + txt(hx + 26, 58, '读头', 'ax', 'middle') + '</g>';
    s += txt(8, 186, '8 个比特 = 1 个字节；每格画 3 颗磁粒，示意', 'ax');
    return { vb: [0, 0, 320, 194], svg: s };
  };

  SC.density = function (a) {
    var m = a.st.trk || 'cmr', s = '', H = 150, x0 = 30, w = 260, y = 26, n = 0;
    s += txt(8, 14, m === 'cmr' ? 'CMR：磁道之间留缝' : 'SMR：磁道像瓦片一样叠着写', 'bl');
    if (m === 'cmr') {
      while (y + 14 <= 26 + H) { s += '<g data-p="track">' + rect(x0, y, w, 14, 'trkf', null, ' rx="2"') + '</g>'; if (y + 20 <= 26 + H) s += '<g data-p="gap">' + rect(x0, y + 14, w, 6, 'gapf2') + '</g>'; y += 20; n++; }
    } else {
      var z = 0;
      while (y + 14 <= 26 + H) {
        s += '<g data-p="track">' + rect(x0, y, w, 14, 'trkf' + (z % 2 ? ' alt' : ''), null, ' rx="2"') + '</g>';
        y += 9; n++; z++;
        if (z === 7 && y + 14 <= 26 + H) { s += '<g data-p="zone">' + rect(x0, y + 5, w, 8, 'gapf2') + txt(x0 + w + 4, y + 12, '区间隙', 'ax') + '</g>'; y += 14; z = 0; }
      }
      s += txt(x0 + w + 4, 40, '宽写头', 'ax');
    }
    s += txt(160, 192, '同样宽度画了 ' + n + ' 条磁道（示意，不是真实比例）', 'ax', 'middle');
    return { vb: [0, 0, 320, 198], svg: s };
  };

  SC.helium = function (a) {
    var m = a.st.gas || 'he', s = '';
    function stack(x0, k, nd, th, lab) {
      var on = m === k, t = '', top = 40, H = 120, gap = (H - nd * th) / (nd + 1);
      t += '<g class="' + (on ? '' : 'dimg') + '">';
      t += '<g data-p="seal">' + rect(x0, top - 10, 120, H + 20, 'hcase', null, ' rx="6"') + '</g>';
      var dots = k === 'air' ? 70 : 10;
      t += '<g data-p="gas">'; for (var i = 0; i < dots; i++) t += circ(x0 + 8 + (i * 37) % 104, top - 4 + (i * 53) % (H + 8), 1.1, 'gasd'); t += '</g>';
      if (k === 'air') for (i = 0; i < 4; i++) t += '<path class="swirl" d="M' + (x0 + 14 + i * 26) + ' ' + (top + 30 + (i % 2) * 40) + ' q8 -10 16 0 t16 0"/>';
      t += '<g data-p="platter">'; for (i = 0; i < nd; i++) t += rect(x0 + 12, top + gap * (i + 1) + th * i, 96, th, 'plat', null, ' rx="1"'); t += '</g>';
      t += rect(x0 + 56, top - 6, 8, H + 12, 'spin') + txt(x0 + 60, top + H + 24, lab, on ? 'vl' : 'ax', 'middle') + '</g>';
      return t;
    }
    s += stack(24, 'air', 6, 6, '空气：最多 6 张');
    s += stack(176, 'he', 10, 3.6, '氦气：最多 10 张');
    s += txt(8, 14, '侧视示意：同样大小的盒子里能放几张盘片', 'bl');
    return { vb: [0, 0, 320, 196], svg: s };
  };

  SC.gen = function (a) {
    var g = a.gen(), s = '', nd = g.nd, top = 30, H = 120, x0 = 30, w = 150;
    s += txt(8, 14, g.name + ' · ' + g.year, 'bl') + txt(312, 14, '侧视示意', 'ax', 'end');
    s += rect(x0 - 8, top - 8, w + 16, H + 16, 'hcase', null, ' rx="6"');
    if (nd) {
      var th = Math.max(2.4, 40 / nd), gap = (H - nd * th) / (nd + 1);
      for (var i = 0; i < nd; i++) s += '<g data-p="platter">' + rect(x0, top + gap * (i + 1) + th * i, w, th, 'plat' + (g.heat ? ' hot' : ''), null, ' rx="1"') + '</g>';
      s += txt(x0 + w / 2, top + H + 22, nd + ' 张盘片 × ' + (g.tb ? g.tb + 'TB' : '每碟待补'), 'vl', 'middle');
    } else {
      s += rect(x0, top, w, H, 'pcbt tbd', 'platter', ' rx="2"') + txt(x0 + w / 2, top + H / 2, '碟数、每碟容量：待补', 'ax', 'middle');
      s += txt(x0 + w / 2, top + H + 22, '整盘 ' + g.cap + 'TB', 'vl', 'middle');
    }
    s += '<g data-p="head">' + txt(x0 + w + 20, top + 12, g.heat ? '激光加热写入' : g.mamr ? '微波辅助写入' : '普通写头', 'bl') + '</g>';
    // 容量条：0–100TB
    var bx = x0 + w + 20, bw = 100, by = top + 40;
    s += txt(bx, by - 6, '整盘容量', 'ax');
    s += rect(bx, by, bw, 12, 'trkb', null, ' rx="3"') + rect(bx, by, bw * Math.min(1, g.cap / 100), 12, 'bar ' + (g.heat ? 'bad' : 'okb'), null, ' rx="3"');
    s += txt(bx, by + 28, g.cap + 'TB', 'vl') + txt(bx + bw, by + 28, '刻度 0–100TB', 'ax', 'end');
    if (g.tb) s += txt(bx, by + 50, '每碟 ' + g.tb + 'TB', 'bl');
    return { vb: [0, 0, 320, 182], svg: s };
  };

  SC.hamr = function (a) {
    var on = a.st.las !== 0, s = '';
    s += txt(8, 14, on ? '激光开：一小点被加热，磁粒变“软”，写得进去' : '激光关：磁粒太“硬”，写头翻不动', 'bl');
    s += rect(60, 30, 200, 50, 'headb', null, ' rx="6"') + txt(70, 44, '磁头（剖面示意）', 'ax');
    s += '<g data-p="laser">' + rect(80, 50, 30, 16, 'lasr' + (on ? ' on' : ''), null, ' rx="2"') + txt(95, 61, '激光', 'ax', 'middle') + '</g>';
    s += '<path class="wg' + (on ? ' on' : '') + '" d="M110 58 L150 58 L150 76"/>';
    s += '<g data-p="nft"><polygon class="nftf" points="140,70 160,70 150,82"/>' + txt(170, 76, '近场天线', 'ax') + '</g>';
    s += rect(200, 50, 20, 30, 'headr', 'nft', ' rx="2"') + txt(210, 46, '写头', 'ax', 'middle');
    s += '<g data-p="media">';
    for (var i = 0; i < 26; i++) s += rect(20 + i * 11, 92, 9, 16, 'grU' + (i % 3 === 1 ? ' d' : ''), null, ' rx="1.5"');
    s += txt(300, 104, '铁铂层', 'ax', 'end') + '</g>';
    if (on) s += circ(150, 100, 12, 'hotsp') + txt(150, 126, '> 430°C，< 2 纳秒', 'okt', 'middle');
    s += '<g data-p="glass">' + rect(20, 110, 284, 34, 'glsr2') + txt(160, 160, '玻璃基板', 'ax', 'middle') + '</g>';
    return { vb: [0, 0, 320, 168], svg: s };
  };

  SC.road = function (a) {
    var s = '', X0 = 40, X1 = 300, Y0 = 170, Y1 = 26, sel = a.st.co || '';
    function X(y) { return X0 + (y - 2024) / (2031 - 2024) * (X1 - X0); }
    function Y(t) { return Y0 - t / 110 * (Y0 - Y1); }
    [0, 20, 40, 60, 80, 100].forEach(function (t) { s += '<line class="gl dsh" x1="' + X0 + '" x2="' + X1 + '" y1="' + f1(Y(t)) + '" y2="' + f1(Y(t)) + '"/>' + txt(X0 - 4, Y(t) + 3, t, 'ax', 'end'); });
    for (var y = 2024; y <= 2030; y += 2) s += txt(X(y), Y0 + 14, y, 'ax', 'middle');
    s += txt(8, 14, '容量（TB）× 年份；点越右越是计划', 'bl');
    ROAD.forEach(function (r) {
      var on = !sel || sel === r[0];
      s += '<g data-p="' + r[5] + '"' + (on ? '' : ' class="dimg"') + '>' + circ(X(r[1]), Y(r[2]), 5, 'rd ' + r[0] + (r[6] ? ' tbd' : ''));
      s += txt(X(r[1]) + r[8], Y(r[2]) + r[9], r[7], 'ax', r[10]) + '</g>';
    });
    return { vb: [0, 0, 320, 192], svg: s };
  };

  function pb(a) { return a.st.pb || 10; }
  SC.why = function (a) {
    var P = pb(a), h = P * 1000 * PX.hdd / 1e6, d = P * 1000 * PX.ssd / 1e6, s = '', kx = 200 / d;
    s += txt(8, 14, '买 ' + P + ' PB（= ' + num(P * 1000) + ' TB）硬盘本身要多少钱', 'bl');
    s += '<g data-p="b_hdd">' + txt(8, 46, 'HDD', 'bl') + rect(60, 34, Math.max(2, h * kx), 18, 'bar okb', null, ' rx="3"') + txt(66 + Math.max(2, h * kx), 47, num(h, 2) + ' 百万美元', 'bv') + '</g>';
    s += '<g data-p="b_ssd">' + txt(8, 86, 'SSD', 'bl') + rect(60, 74, d * kx, 18, 'bar bad', null, ' rx="3"') + txt(56 + d * kx, 104, num(d, 1) + ' 百万美元', 'bv', 'end') + '</g>';
    s += txt(8, 132, '差 ' + f1(PX.ssd / PX.hdd) + ' 倍：只算盘本身，不含服务器、电和机房', 'ax');
    s += txt(8, 148, '价格：2026 年专家纪要口径（弱）', 'ax');
    return { vb: [0, 0, 320, 156], svg: s };
  };

  SC.supply = function (a) {
    var s = '', kx = 4, cur = a.st.lt || 'now';
    s += txt(8, 14, '近线硬盘交期（周）', 'bl');
    LT.forEach(function (r, k) {
      var y = 28 + k * 34, on = r[0] === cur, p = r[0] === 'bal' ? 'b_lt0' : 'b_lt1';
      s += '<g data-p="' + p + '"' + (on ? ' class="sel"' : '') + '>' + txt(8, y + 12, r[1], 'bl') + rect(90, y, r[2] * kx, 16, 'bar ' + (r[0] === 'bal' ? 'okb' : 'bad'), null, ' rx="3"') + txt(94 + r[2] * kx, y + 12, r[2] + (r[0] === 's25' ? '+' : ''), 'bv') + '</g>';
    });
    s += txt(8, 140, '50 周 ≈ 一年：今天下单，明年才到', 'ax');
    return { vb: [0, 0, 320, 150], svg: s };
  };

  var WHO = [['drive', '整机', 'm_drive'], ['head', '磁头', 'm_head'], ['media', '介质', 'm_media'], ['sub', '玻璃基板', 'm_sub'], ['motor', '主轴电机', 'm_motor'], ['mag', 'VCM 磁钢', 'm_mag']];
  var SUP = [['head', '磁头', '希捷 / WD 自制 + TDK'], ['media', '介质', '自制 + Resonac'], ['sub', '玻璃基板', 'HOYA'], ['motor', '主轴电机', '尼得科 >70%'], ['mag', 'VCM 磁钢', '钕铁硼（份额待补）']];
  var SH = [['西部数据', 42.3], ['希捷', 40.8], ['东芝', 17.0]];
  SC.who = function (a) {
    var s = '', cur = a.st.who || 'drive';
    s += txt(8, 14, '零件 → 整机（2025 年台数份额，弱）', 'bl');
    SUP.forEach(function (r, k) {
      var y = 26 + k * 30, on = r[0] === cur;
      s += '<g data-p="m_' + r[0] + '"' + (on ? ' class="sel"' : '') + '>' + rect(8, y, 140, 24, 'nodef', null, ' rx="4"') + txt(14, y + 11, r[1], 'bl') + txt(14, y + 21, r[2], 'ax') + '</g>';
      s += '<path class="arrw" d="M150 ' + (y + 12) + ' L184 96"/>';
    });
    var on = cur === 'drive';
    s += '<g data-p="m_drive"' + (on ? ' class="sel"' : '') + '>' + rect(186, 50, 126, 96, 'nodef', null, ' rx="6"') + txt(194, 66, '整机三家', 'bl');
    SH.forEach(function (r, k) { var y = 76 + k * 22; s += txt(194, y + 10, r[0], 'ax') + rect(240, y, r[1] * 1.4, 12, 'bar ' + (k < 2 ? 'mid' : ''), null, ' rx="2"') + txt(244 + r[1] * 1.4, y + 10, r[1] + '%', 'bv'); });
    s += '</g>';
    return { vb: [0, 0, 320, 182], svg: s };
  };

  SC.watch = function () {
    var s = '', kx = 40, rows = [['希捷 本季', 4.233, 'p_stx', 'mid'], ['希捷 下季指引', 4.8, 'p_stx', 'bad'], ['WD 本季', 4.38, 'p_wdc', 'mid'], ['WD 下季指引（中值）', 5.1, 'p_wdc', 'bad']];
    s += txt(8, 14, '季度营收（十亿美元）', 'bl');
    rows.forEach(function (r, k) { var y = 26 + k * 26; s += '<g data-p="' + r[2] + '">' + txt(8, y + 12, r[0], 'bl') + rect(120, y, r[1] * kx, 15, 'bar ' + r[3], null, ' rx="3"') + txt(124 + r[1] * kx - 40, y + 12, r[1], 'bv') + '</g>'; });
    s += txt(8, 140, 'WD 指引 5.0–5.2，取中值 5.1（推算）', 'ax');
    return { vb: [0, 0, 320, 150], svg: s };
  };

  /* ---------- 步内小部件 ---------- */
  var WD = {};
  function showBd(el, m) { var sec = el.closest('.ex-step'); if (sec) sec.querySelectorAll('.ex-bd').forEach(function (d) { d.hidden = d.dataset.m !== m; }); }
  function seg(label, items) { return '<div class="ex-seg" role="group" aria-label="' + label + '">' + items.map(function (x) { return '<button type="button" data-v="' + x[0] + '" aria-pressed="false"' + (x[2] ? ' disabled' : '') + '>' + x[1] + '</button>'; }).join('') + '</div>'; }
  function press(el, sel, v) { el.querySelectorAll(sel).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === String(v) ? 'true' : 'false'); }); }
  function inStep(a, sc) { return D.steps[a.st.i] && D.steps[a.st.i].scene === sc; }

  function chr(b) { var v = 0; b.forEach(function (x) { v = v * 2 + x; }); return v >= 32 && v < 127 ? '“' + String.fromCharCode(v) + '”' : '（不可打印）'; }
  WD.bit = function (el, a) {
    el.innerHTML = '<div class="ex-seg md" role="group" aria-label="写或读"><button type="button" data-m="w" aria-pressed="true">写</button><button type="button" data-m="r" aria-pressed="false">读</button></div>' +
      '<div class="ex-seg bt" role="group" aria-label="点比特翻转">' + [0, 1, 2, 3, 4, 5, 6, 7].map(function (k) { return '<button type="button" data-v="' + k + '" aria-pressed="false">' + (k + 1) + '</button>'; }).join('') + '</div><p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    a.st.bits = [0, 1, 0, 0, 1, 0, 0, 0]; a.st.bm = 'w';
    function up() {
      var b = a.st.bits;
      el.querySelectorAll('.bt button').forEach(function (x, k) { x.textContent = b[k]; x.setAttribute('aria-pressed', b[k] ? 'true' : 'false'); x.disabled = a.st.bm === 'r'; });
      el.querySelectorAll('.md button').forEach(function (x) { x.setAttribute('aria-pressed', x.dataset.m === a.st.bm ? 'true' : 'false'); });
      p.innerHTML = a.st.bm === 'w' ? '写模式：点上面的数字翻转比特，写头就把那一格磁粒翻过来。'
        : '读模式：读头读出 <b>' + b.join('') + '</b>，按 ASCII 编码就是 <b>' + chr(b) + '</b>。' + DEMO;
      a.update();
    }
    el.addEventListener('click', function (e) {
      var x = e.target.closest('button'); if (!x || x.disabled) return;
      if (x.dataset.m) a.st.bm = x.dataset.m; else { var k = +x.dataset.v; a.st.bits[k] = 1 - a.st.bits[k]; a.st.bpos = k; }
      up();
    });
    up();
  };
  WD.trk = function (el, a) {
    el.innerHTML = seg('记录方式', [['cmr', 'CMR 常规'], ['smr', 'SMR 叠瓦']]);
    function up(m) { a.st.trk = m; press(el, 'button', m); showBd(el, m); a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    a.st.trk = 'cmr'; press(el, 'button', 'cmr');
  };
  WD.gas = function (el, a) {
    el.innerHTML = seg('盘腔气体', [['air', '空气'], ['he', '氦气']]) + '<p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(m) {
      a.st.gas = m; press(el, 'button', m);
      p.innerHTML = m === 'air' ? '空气：分子多、乱流大，盘片要厚一点才稳，最多 6 张 ' + R('he') + '。' : '氦气：密度约为空气的 1/7，乱流小，盘片能更薄，最多 10 张 ' + R('he') + '。';
      a.update();
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    up('he');
  };
  WD.laser = function (el, a) {
    el.innerHTML = seg('激光', [['1', '激光开'], ['0', '激光关']]);
    function up(v) { a.st.las = +v; press(el, 'button', v); a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    a.st.las = 1; press(el, 'button', '1');
  };
  WD.road = function (el, a) {
    el.innerHTML = seg('公司', [['', '全部'], ['stx', '希捷'], ['wdc', '西部数据'], ['tsb', '东芝']]) + '<p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(m) {
      a.st.co = m; press(el, 'button', m);
      p.innerHTML = ROAD.filter(function (r) { return !m || r[0] === m; }).map(function (r) { return r[3] + ' ' + R(r[4]); }).join('；');
      a.update();
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    up('');
  };
  var PBS = [1, 10, 100, 1000];
  WD.cost = function (el, a) {
    el.innerHTML = '<label class="ex-r">容量 <input type="range" min="0" max="3" step="1" value="1" aria-label="存储容量"><output></output></label><p class="ex-o"></p>';
    var i = el.querySelector('input'), o = el.querySelector('output'), p = el.querySelector('.ex-o');
    function up() {
      var P = PBS[+i.value]; a.st.pb = P; o.textContent = P >= 1000 ? '1 EB' : P + ' PB';
      var h = P * 1000 * PX.hdd, d = P * 1000 * PX.ssd;
      p.innerHTML = '<b>' + (P >= 1000 ? '1 EB' : P + ' PB') + '</b>：HDD 约 ' + num(h / 1e6, 2) + ' 百万美元，SSD 约 ' + num(d / 1e6, 1) + ' 百万美元' + CALC + ' ' + R('jpm') +
        '<br><small>按 2026 年纪要价（每 GB HDD 0.016、SSD 0.243 美元，弱）现算；只算盘本身。1 PB = 1,000 TB，1 EB = 1,000 PB。</small>';
      a.update();
    }
    i.addEventListener('input', up); up();
  };
  WD.lt = function (el, a) {
    el.innerHTML = seg('交期', LT.map(function (r) { return [r[0], r[1]]; })) + '<p class="ex-o"></p>';
    var p = el.querySelector('.ex-o');
    function up(m) {
      var r = LT.filter(function (x) { return x[0] === m; })[0];
      a.st.lt = m; press(el, 'button', m);
      p.innerHTML = '<b>' + r[1] + '</b>：约 ' + r[2] + ' 周' + (m === 's25' ? '以上' : '') + ' ' + R(r[3]) + '。';
      a.update();
    }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    up('now');
  };
  WD.ladder = function (el, a) {
    function card(g, k) {
      return '<button type="button" class="ex-gc' + (k === a.st.g ? ' on' : '') + '" data-g="' + k + '"><span class="ex-gn">' + g.name + '<small>' + g.year + '</small></span>' +
        '<span class="ex-gm"><span>' + g.tech + '</span><span>' + g.per + '</span><span>整盘 ' + g.cap + 'TB</span></span>' +
        '<span class="ex-gu"><i>解锁</i>' + g.unlock + '</span><span class="ex-gu nk"><i>瓶颈</i>' + g.neck + '</span>' + (g.note ? '<span class="ex-gu"><i class="nt">注</i>' + g.note + '</span>' : '') + '</button>';
    }
    function up() { el.innerHTML = '<div class="ex-gl">' + G.map(card).join('') + '</div>'; }
    el.addEventListener('click', function (e) { if (e.target.closest('a')) return; var b = e.target.closest('.ex-gc'); if (b) a.setGen(+b.dataset.g); });
    document.addEventListener('exgen', up); up();
  };
  WD.who = function (el, a) {
    el.innerHTML = seg('环节', WHO.map(function (w) { return [w[0], w[1]]; }));
    function up(m) { a.st.who = m; press(el, 'button', m); showBd(el, m); if (inStep(a, 'who')) a.select('m_' + m); a.update(); }
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) up(b.dataset.v); });
    a.st.who = 'drive'; press(el, 'button', 'drive');
  };
  WD.quiz = function (el) {
    el.innerHTML = D.quiz.map(function (q, k) { return '<details class="ex-q"><summary><b>' + (k + 1) + '.</b> ' + q[0] + '</summary><p>' + q[1] + '</p></details>'; }).join('');
  };

  function readout(a, s) {
    var g = a.gen();
    if (s.scene === 'what') return '盘片 + 主轴 + 磁头臂 + 音圈电机';
    if (s.scene === 'bit') { var b = bits(a); return b.join('') + ' → ' + chr(b); }
    if (s.scene === 'density') return (a.st.trk || 'cmr') === 'cmr' ? 'CMR · 随机写快' : 'SMR · 多存，改数据要整区重写';
    if (s.scene === 'helium') return (a.st.gas || 'he') === 'he' ? '氦气 · 最多 10 张盘片' : '空气 · 最多 6 张盘片';
    if (s.scene === 'gen') return g.name + ' · 整盘 ' + g.cap + 'TB';
    if (s.scene === 'hamr') return a.st.las === 0 ? '激光关 · 写不进' : '激光开 · > 430°C · < 2 ns';
    if (s.scene === 'road') return '30TB（2024）→ 44TB（2026）→ 55TB（约 2030）';
    if (s.scene === 'why') { var P = pb(a); return (P >= 1000 ? '1 EB' : P + ' PB') + ' · SSD 贵约 ' + f1(PX.ssd / PX.hdd) + ' 倍'; }
    if (s.scene === 'supply') { var r = LT.filter(function (x) { return x[0] === (a.st.lt || 'now'); })[0]; return '交期 ' + r[2] + ' 周 · ' + r[1]; }
    if (s.scene === 'who') { var w = WHO.filter(function (x) { return x[0] === (a.st.who || 'drive'); })[0]; return w[1]; }
    if (s.scene === 'watch') return '下季指引：希捷 4.8、WD 5.0–5.2（十亿美元）';
    return g.name;
  }

  window.EX.mount({ steps: D.steps, gens: G, parts: PARTS, scenes: SC, widgets: WD, readout: readout });
})();
