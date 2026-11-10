/* AI 基础设施资本周期工作台 —— 全部数据来自 data.js（由 tools/build_site.py 生成），本文件只负责渲染。 */
(function(){
'use strict';
var D=window.D, V=document.getElementById('view'), POP=document.getElementById('pop');
var LED={}; D.ledger.forEach(function(r){LED[r.gid]=r;});
var CHARTS=[], NOTES=[], NIDX={};
var SEGS0={'1':'算力','2':'存储','3':'光','4':'PCB','5':'电力','6':'云'};function SS(i){return MOB()?SEGS0[i]:SEGN[i];}
var SEGN={'1':'算力芯片','2':'存储/封装','3':'光模块/网络','4':'PCB/散热','5':'电力设备','6':'云/数据中心'};
var COL=['#007AFF','#AF52DE','#30B0C7','#FF9500','#34C759','#FF3B30','#5856D6','#FF2D55','#8E8E93','#FFCC00'];
var MODS=[['m1','1 全景'],['m2','2 周期仪表盘'],['m3','3 公司财务'],['m4','4 库存与资本开支'],['m5','5 供需与产能'],['m6','6 利润池迁移'],
 ['m7','7 历史周期'],['m8','8 情景模拟'],['m9','9 机会/风险'],['m10','10 证据台账'],['qa','20 问'],['method','方法论'],['xc','交叉核对']];
document.getElementById('asof').textContent='统计日期 '+D.asof+'（罗马时间）';

/* ---------- 小工具 ---------- */
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function fnum(v,d){if(v==null||v===''||isNaN(v))return '<span class="miss">缺失</span>';d=d==null?1:d;return Number(v).toLocaleString('zh-CN',{minimumFractionDigits:d,maximumFractionDigits:d});}
function note(id){ if(!(id in NIDX)){NOTES.push(id);NIDX[id]=NOTES.length;} return NIDX[id]; }
function R(t){ /* {{ID}} → 尾注上标 */
  return esc(t).replace(/\{\{([^}]+)\}\}/g,function(_,id){var n=note(id);return '<sup class="fn"><a data-id="'+esc(id)+'" title="'+esc(id)+'">'+n+'</a></sup>';}).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');}
function refs(ids){return ids.map(function(id){var n=note(id);return '<sup class="fn"><a data-id="'+esc(id)+'">'+n+'</a></sup>';}).join('');}
function ttag(t){t=String(t||'');var k=t.charAt(0);var c={A:'tA',E:'tE',F:'tF',J:'tJ'}[k]||'tG';return '<span class="tag '+c+'">'+esc(t.length>8?t.slice(0,8)+'…':t)+'</span>';}
function vtag(v){v=String(v||'');var c=/已核|冲突已解/.test(v)?'tA':/降级|未核|单一/.test(v)?'tX':'tG';return '<span class="tag '+c+'">'+esc(v||'—')+'</span>';}
function cap(src,type,asof,unit){return '<p class="cap">来源：'+R(src)+'｜'+ttag(type)+'统计日期 '+esc(asof||D.asof)+(unit?'｜单位：'+esc(unit):'')+'</p>';}
function tbl(head,rows,numcols){numcols=numcols||[];return '<div class="tbl"><table><thead><tr>'+head.map(function(h,i){return '<th'+(numcols.indexOf(i)>=0?' class="n"':'')+'>'+h+'</th>';}).join('')+'</tr></thead><tbody>'+
  rows.map(function(r){return '<tr>'+r.map(function(c,i){return '<td'+(numcols.indexOf(i)>=0?' class="n"':'')+'>'+c+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table></div>';}
function fold(title,html,open){return '<details'+(open?' open':'')+'><summary>'+title+'</summary><div class="in">'+html+'</div></details>';}
function key(t){return '<div class="key"><b>关键判断</b>　'+R(t)+'</div>';}
function prep(el,opt){opt.animation=false;if(opt.legend){var names=(opt.series||[]).map(function(x){return x.name;}).filter(Boolean),W=el.clientWidth-16,rows=1,x=0;names.forEach(function(n){var w=String(n).replace(/[\x00-\x7f]/g,'').length*11+String(n).replace(/[^\x00-\x7f]/g,'').length*6.5+34;if(x+w>W&&x>0){rows++;x=0;}x+=w;});opt.legend=Object.assign({},opt.legend,{type:'plain',top:0,left:'center',itemGap:8,itemWidth:14,itemHeight:10});var hasName=[].concat(opt.yAxis||[]).some(function(a){return a&&a.name;});opt.grid=Object.assign({},opt.grid);opt.grid.top=Math.max(rows*20+(hasName?28:10),names.length?0:opt.grid.top||0);}return opt;}
function chart(id,opt){var el=document.getElementById(id);if(!el)return;var c=echarts.init(el,null,{renderer:'svg'});c.__el=el;if(opt&&Object.keys(opt).length)c.setOption(prep(el,opt));CHARTS.push(c);return c;}
var MOB=function(){return window.innerWidth<640;};
function grid(o){return Object.assign({left:MOB()?44:56,right:MOB()?12:24,top:40,bottom:MOB()?56:44,containLabel:false},o||{});}
function leg(){return {top:0,type:'scroll',textStyle:{fontSize:11}};}
function segname(s){return s?s+' '+SEGN[s]:'—';}

/* ---------- 尾注与弹层 ---------- */
function endnotes(){
  if(!NOTES.length)return '';
  return '<div class="endnotes"><h3>注释（证据台账 ID）</h3><ol>'+NOTES.map(function(id){var r=LED[id];
    if(!r)return '<li id="en-'+esc(id)+'"><b>'+esc(id)+'</b> <span class="miss">台账中无此 ID</span></li>';
    return '<li id="en-'+esc(id)+'"><b>'+esc(id)+'</b> '+esc(r.claim)+'：'+esc(r.value.length>140?r.value.slice(0,140)+'…':r.value)+' '+esc(r.unit)+(r.currency&&r.unit.indexOf(r.currency)<0?'（'+esc(r.currency)+'）':'')+'，'+esc(r.period)+'。'+
      ttag(r.type)+vtag(r.verify)+' '+(r.url?'<a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.source)+'</a>':esc(r.source))+'</li>';}).join('')+'</ol></div>';}
function showPop(id){var r=LED[id];if(!r){return;}
  POP.innerHTML='<button class="x" aria-label="关闭">×</button><b>'+esc(id)+'</b>　'+ttag(r.type)+vtag(r.verify)+(r.headline_ok==='N'?'<span class="tag tX">不能单独支撑标题结论</span>':'')+
   '<p>'+esc(r.claim)+'</p><p><b>'+esc(r.value)+'</b> '+esc(r.unit)+' '+esc(r.currency)+'｜期间 '+esc(r.period)+'｜环节 '+esc(r.seg)+'</p>'+
   '<p class="note">来源：'+(r.url?'<a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.source)+'</a>':esc(r.source))+'（'+esc(r.tier)+'；'+esc(r.origin)+'）'+(r.note?'<br>备注：'+esc(r.note):'')+'</p>'+
   '<p><a href="#m10?id='+encodeURIComponent(id)+'">在证据台账中查看 →</a></p>';
  POP.hidden=false;}
document.addEventListener('click',function(e){var a=e.target.closest('sup.fn a');if(a){e.preventDefault();showPop(a.getAttribute('data-id'));return;}
  if(e.target.closest('.pop .x')||(!e.target.closest('.pop')&&!POP.hidden)){POP.hidden=true;}});

/* ---------- 导航 ---------- */
var NAV=document.getElementById('nav');
NAV.innerHTML=MODS.map(function(m){return '<a href="#'+m[0]+'" data-k="'+m[0]+'">'+m[1]+'</a>';}).join('');
function route(){
  var h=(location.hash||'#m1').slice(1), parts=h.split('?'), k=parts[0], q={};
  (parts[1]||'').split('&').forEach(function(p){var kv=p.split('=');if(kv[0])q[kv[0]]=decodeURIComponent(kv[1]||'');});
  if(!PAGES[k])k='m1';
  CHARTS.forEach(function(c){c.dispose();});CHARTS=[];NOTES=[];NIDX={};POP.hidden=true;
  [].forEach.call(NAV.children,function(a){var on=a.getAttribute('data-k')===k;a.className=on?'on':'';if(on&&a.scrollIntoView)a.scrollIntoView({block:'nearest',inline:'center'});});
  var out=PAGES[k](q);V.innerHTML=out.html+endnotes();if(out.after)out.after(q);
  window.scrollTo(0,0);document.title=(MODS.filter(function(m){return m[0]===k;})[0]||['',''])[1]+'｜AI 基础设施资本周期工作台';
}
window.addEventListener('hashchange',route);
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){CHARTS.forEach(function(c){c.resize();});},120);});

var PAGES={};
function head(n,title,dek){return '<p class="kicker" style="margin:20px 0 0">模块 '+n+'</p><h1>'+title+'</h1><p class="lead">'+dek+'</p>';}
function ttm(s,k){var x=D.segagg[s].series.TTM;return x?x[k]:null;}

/* ---------- 模块 1 全景 ---------- */
PAGES.m1=function(){
  var S=D.segments, by={};S.forEach(function(s){by[s.id]=s;});
  function node(id){var s=by[id],x=D.segagg[id].series.TTM||{};return '<a class="node" href="#m2" style="border-top-color:'+COL[+id-1]+';text-decoration:none;color:inherit"><b>'+esc(segname(id))+'</b>'+
    esc(s.stage_txt)+'<br><span class="note">近 12 个月营收 '+fnum(x.rev,0)+' / 营业利润 '+fnum(x.oi,0)+' 十亿美元（'+(x.n||0)+' 家）</span></a>';}
  var h=head(1,'全球 AI 基础设施产业链全景','钱从哪里来、流到哪里去、每一段现在处在周期的什么位置。')+
  '<div class="bluf"><div class="k">先说结论</div><p>'+R(D.bluf)+'</p><div class="k" style="margin-top:8px">主要矛盾</div><p>'+R(D.contradiction)+'</p></div>'+
  '<p>'+R(D.analogy)+'</p>'+
  '<h2>钱怎么流：云厂商出钱，五个环节收钱</h2><p class="note">点任意一格进入周期仪表盘。数字是本项目 35 家代表公司的全公司口径（A，按 FRED 汇率折美元），不是全行业。</p>'+
  '<div class="flow">'+node('6')+'<span class="arr">→</span>'+['1','2','3','4','5'].map(node).join('')+'</div>'+
  '<div class="card"><h3>六个环节近 12 个月：利润和投入</h3><div id="c1" class="chart"></div>'+cap('本项目财务面板（SEC XBRL、Tushare、FinMind、公司年报），tools/segagg.py 汇总','A 实际（汇总为 E）',D.asof,'十亿美元；资本开支/经营现金流为 %')+'</div>'+
  key('最大的利润在算力芯片和存储；最大的投入在云。云的资本开支已经接近吃掉全部经营现金流{{FIN-F01}}，而上游（存储、算力）一边赚钱一边扩产。')+
  fold('术语表：这些词是什么意思（'+Object.keys(D.gloss).length+' 个）','<dl class="gloss">'+Object.keys(D.gloss).map(function(k){return '<dt>'+esc(k)+'</dt><dd>'+esc(D.gloss[k])+'</dd>';}).join('')+'</dl>')+
  fold('标签怎么读','<p>'+Object.keys(D.types).map(function(k){return ttag(k)+esc(D.types[k]);}).join('　')+'</p><p>核对状态：'+vtag('已核')+'一手原文已复核　'+vtag('一手未复核')+'来自一手渠道但未逐字核对　'+vtag('单一来源')+vtag('未核')+vtag('已降级')+'不能单独支撑标题结论。</p>');
  return {html:h,after:function(){
    var ids=['1','2','3','4','5','6'];
    chart('c1',{tooltip:{trigger:'axis'},legend:leg(),grid:grid({right:MOB()?40:56}),xAxis:{type:'category',data:ids.map(SS),axisLabel:{interval:0,fontSize:MOB()?10:12}},
      yAxis:[{type:'value',name:'十亿美元'},{type:'value',name:'%',splitLine:{show:false}}],
      series:[{name:'营业利润',type:'bar',data:ids.map(function(i){return ttm(i,'oi');})},{name:'资本开支',type:'bar',data:ids.map(function(i){return ttm(i,'capex');})},
        {name:'资本开支/经营现金流 %',type:'line',yAxisIndex:1,data:ids.map(function(i){return ttm(i,'capex_ocf');})}]});
  }};
};

/* ---------- 模块 2 周期仪表盘 ---------- */
PAGES.m2=function(){
  var h=head(2,'六个环节的周期仪表盘','每个环节在五个阶段里的位置，以及支撑这个判断的指标。阶段位置是判断（J），指标是实际（A）。')+
  '<div class="card"><h3>阶段位置</h3><div id="c2" class="chart short"></div>'+cap('本项目判断，依据见各环节卡片与尾注','J 判断',D.asof,'阶段 1–5')+'</div>'+
  key('同一条链上阶段不同步：电力在稀缺→扩产，存储、光模块和云已接近狂热末段。最可能先见顶的是存储，最可能先过剩的是光模块和 PCB。')+
  '<div class="grid">'+D.segments.map(function(s){var x=D.segagg[s.id].series.TTM||{},m=D.segagg[s.id].med||{};var st=Math.round(s.stage);
    function k(v,mm,l){return '<div class="kpi"><div class="v">'+fnum(v,1)+'%</div><div class="l">'+l+'<br>2016–24 中位 '+fnum(mm,1)+'%</div></div>';}
    return '<div class="card segcard"><h3>'+esc(s.id+' '+s.name)+'</h3><div class="stage">'+[1,2,3,4,5].map(function(i){return '<span class="'+(i<=st?'on':'')+'"></span>';}).join('')+'</div>'+
    '<div class="note">'+ttag('J')+'阶段 '+s.stage.toFixed(1)+'：'+esc(s.stage_txt)+'｜代表公司：'+esc(s.cos)+'</div>'+
    '<div class="kpis">'+k(x.opm,m.opm,'营业利润率')+k(x.capex_rev,m.capex_rev,'资本开支/营收')+k(x.fcf_m,m.fcf_m,'自由现金流率')+'</div>'+
    '<p class="cap">'+ttag('A')+'近 12 个月，'+(x.n||0)+' 家合计，截至最新季报</p>'+
    '<dl><dt>最紧</dt><dd>'+R(s.tight)+'</dd><dt>价格</dt><dd>'+R(s.price)+'</dd><dt>交期</dt><dd>'+R(s.lead)+'</dd><dt>风险</dt><dd>'+R(s.risk)+'</dd></dl>'+
    '<div class="verdict">'+R(s.verdict)+'</div></div>';}).join('')+'</div>'+
  '<h2>五个阶段是什么</h2>'+tbl(['阶段','特征'],[[D.stages[0],'价格高、交期长、客户愿意预付'],[D.stages[1],'资本开支/折旧 >1.5，新进入者增多'],[D.stages[2],'在建产能高、存货升、资本开支增速>收入增速'],[D.stages[3],'价格跌破现金成本、减值、破产'],[D.stages[4],'减产生效、库存回落、价格止跌']])+
  '<p class="note">阈值多为经验值，未经回测，详见<a href="#method">方法论</a>。</p>'+
  fold('自动筛查出的异常信号（'+D.flags.length+' 条，A，财务面板规则）',tbl(['类型','公司','证据'],D.flags.map(function(f){return [esc(f.type),esc(f.company),esc(f.evidence)];})));
  return {html:h,after:function(){
    var S=D.segments.slice().reverse();
    chart('c2',{tooltip:{formatter:function(p){return esc(p.data[2])+'<br>阶段 '+p.data[0]+'：'+esc(p.data[3]);}},grid:grid({left:MOB()?88:110,top:20,bottom:40,right:MOB()?36:40}),
      xAxis:{type:'value',min:1,max:5,interval:1,axisLabel:{formatter:function(v){return D.stages[v-1]||'';},fontSize:MOB()?9:11}},
      yAxis:{type:'category',data:S.map(function(s){return SEGN[s.id];}),axisLabel:{fontSize:MOB()?10:12}},
      series:[{type:'scatter',symbolSize:18,data:S.map(function(s){return [s.stage,SEGN[s.id],s.name,s.stage_txt];}),label:{show:true,position:'right',formatter:function(p){return p.data[0].toFixed(1);},fontSize:11},
        itemStyle:{color:function(p){return COL[+S[p.dataIndex].id-1];}},markArea:{silent:true,itemStyle:{color:'rgba(255,149,0,.08)'},data:[[{xAxis:2.5},{xAxis:3.5}]]}}]});
  }};
};

/* ---------- 模块 3 公司财务对比 ---------- */
var M3={metric:'op_margin',cos:['NVIDIA','TSMC','Micron','SK hynix','Microsoft','Innolight']};
PAGES.m3=function(){
  var ms=D.metrics.map(function(m){return '<option value="'+m.id+'"'+(m.id===M3.metric?' selected':'')+'>'+esc(m.name)+'（'+esc(m.unit)+'）</option>';}).join('');
  var chips=['1','2','3','4','5','6'].map(function(s){return '<div style="margin:6px 0"><span class="note">'+esc(segname(s))+'：</span><span class="chips">'+D.comp.filter(function(c){return c.seg===s;}).map(function(c){
    return '<button class="chip'+(M3.cos.indexOf(c.id)>=0?' on':'')+'" data-co="'+esc(c.id)+'">'+esc(c.cn)+'</button>';}).join('')+'</span></div>';}).join('');
  var h=head(3,'公司财务对比（FY2016–FY2026 + 近 12 个月）','选指标、选公司（可多选），看 35 家代表公司 10 年的走势。')+
  '<div class="card"><div class="ctl"><label for="m3m">指标</label><select id="m3m">'+ms+'</select><button class="chip" id="m3clr">清空公司</button></div>'+chips+'</div>'+
  '<div class="card"><div id="c3" class="chart tall"></div><div id="c3cap"></div></div>'+
  key('看三件事：利润率是不是创了新高（周期高点的特征）；资本开支/营收是不是远高于自己的历史中位数；自由现金流率是不是在利润上升时反而下降。')+
  '<div id="m3t"></div>'+
  fold('财年怎么对齐、汇率怎么折','<p class="note">'+esc(D.finmeta.fiscal_label)+'</p><p class="note">'+esc(D.finmeta.fx)+'</p><p class="note">'+esc(D.finmeta.roic_formula)+'</p><p class="note">'+esc(D.finmeta.fcf_formula)+'</p><p class="note">存货天数此处用期末口径：期末存货 ÷ 营业成本 × 365。</p>')+
  fold('35 家公司快照（近 12 个月，A）',tbl(['公司','环节','营收 十亿美元','营收增速','毛利率','营业利润率','资本开支/营收','FCF 率','ROIC','存货天数','5 年中位'],D.snap.map(function(s){
    var c=D.comp.filter(function(x){return x.id===s.company;})[0]||{};function p(v){return v==null?fnum(null):fnum(v*100,1)+'%';}
    return [esc(c.cn||s.company),esc(segname(c.seg)),fnum(s.rev_usd_bn,1),p(s.ytd_yoy),p(s.gm),p(s.opm),p(s.capex_rev),p(s.fcf_m),p(s.roic),fnum(s.dio,0),fnum(s.dio_med5,0)];}),[2,3,4,5,6,7,8,9,10]));
  return {html:h,after:function(){
    function draw(){
      var m=D.metrics.filter(function(x){return x.id===M3.metric;})[0];
      var per=D.per, series=M3.cos.map(function(co){var v=(D.fin[co]||{})[M3.metric]||{};var c=D.comp.filter(function(x){return x.id===co;})[0];
        return {name:c?c.cn:co,type:'line',connectNulls:false,symbolSize:5,data:per.map(function(p){return v[p]==null?null:v[p];})};});
      var c=CHARTS[0]||chart('c3',{});c.setOption(prep(c.__el,{animation:false,tooltip:{trigger:'axis',valueFormatter:function(v){return v==null?'缺失':v+' '+m.unit;}},legend:leg(),grid:grid({top:48}),xAxis:{type:'category',data:per.map(function(p){return p.replace('FY','');}),axisLabel:{fontSize:11}},
        yAxis:{type:'value',name:m.unit,scale:true},series:series}),true);
      document.getElementById('c3cap').innerHTML='<p class="cap">来源：本项目财务面板（SEC XBRL companyfacts、Tushare、FinMind、公司年报/决算短信；部分早年数据为 stockanalysis 二手转录，见台账）｜'+ttag('A')+'由披露值计算｜统计日期 '+esc(D.asof)+'｜单位：'+esc(m.unit)+'（美元口径按 FRED 汇率）｜缺口不连线＝缺失；日历年财年的公司 FY2026 尚未结束，最新看 TTM（近 12 个月）</p>';
      var rows=M3.cos.map(function(co){var v=(D.fin[co]||{})[M3.metric]||{},fl=((D.finflag[co]||{})[M3.metric])||{};var c=D.comp.filter(function(x){return x.id===co;})[0];
        return [esc(c?c.cn:co)].concat(per.map(function(p){return fnum(v[p],m.unit==='倍'?2:1)+(fl[p]?'<sup>估</sup>':'');}));});
      document.getElementById('m3t').innerHTML=fold('数据表：'+esc(m.name)+'（'+esc(m.unit)+'）',tbl(['公司'].concat(per),rows,per.map(function(_,i){return i+1;})));
    }
    var sel=document.getElementById('m3m');sel.onchange=function(){M3.metric=sel.value;draw();};
    V.querySelectorAll('[data-co]').forEach(function(b){b.onclick=function(){var co=b.getAttribute('data-co'),i=M3.cos.indexOf(co);if(i>=0)M3.cos.splice(i,1);else M3.cos.push(co);b.classList.toggle('on');draw();};});
    document.getElementById('m3clr').onclick=function(){M3.cos=[];V.querySelectorAll('[data-co]').forEach(function(b){b.classList.remove('on');});draw();};
    draw();
  }};
};

/* ---------- 模块 4 库存与资本开支 ---------- */
PAGES.m4=function(){
  var C=D.capex,cos=['MSFT','AMZN','GOOGL','META','ORCL'],cn={MSFT:'微软',AMZN:'亚马逊',GOOGL:'Alphabet',META:'Meta',ORCL:'甲骨文',CRWV:'CoreWeave'};
  var yrs=Object.keys(C.series.MSFT);
  var h=head(4,'库存与资本开支','下游投钱的速度，和上游囤货的速度。两者同时升高，是周期后段的典型组合。')+
  '<div class="card"><h3>云厂商现金资本开支（2016–2026 前三季）</h3><div id="c4a" class="chart"></div>'+cap(esc(C.basis),'A 实际',C.asof,'十亿美元')+'</div>'+
  key('四家云厂商 2026 年前三季已投 '+fnum(C.big4['2026_9M'],1)+' 十亿美元，超过 2024 年全年的 '+fnum(C.big4['2024'],1)+'；2026 年指引合计约 7,200–7,400 亿（指引口径不统一，已降级为背景）。{{KX-01}}{{KX-04}}')+
  '<div class="card"><h3>近 12 个月：资本开支 vs 经营现金流</h3>'+tbl(['公司','资本开支','经营现金流','资本开支/经营现金流','自由现金流','截至'],
    Object.keys(C.ttm).map(function(k){var t=C.ttm[k];return [esc(cn[k]||k),fnum(t.capex,1),fnum(t.ocf,1),'<b>'+fnum(t.capex_ocf,1)+'%</b>',fnum(t.fcf,1),esc(t.thru)];}),[1,2,3,4])+
    cap('SEC 10-Q/10-K（XBRL 季度差分）；自由现金流＝经营现金流−现金资本开支（毛额，不扣融资租赁）{{FIN-F01}}{{KX-05}}','A 实际',D.asof,'十亿美元')+
    '<p class="note">2026 指引（F）：'+Object.keys(C.guide_2026).map(function(k){var g=C.guide_2026[k];return esc(cn[k])+' '+g[0]+(g[1]!==g[0]?'–'+g[1]:'');}).join('；')+'（十亿美元）。2027 年卖方一致预期 '+esc(C.consensus_2027)+'（F，二手）。'+esc(C.note)+'</p></div>'+
  '<div class="card"><h3>季度存货周转天数：上游在囤货吗？</h3><div id="c4b" class="chart"></div>'+cap(esc(D.inv.dio_days.note)+'{{FIN-F11}}{{FIN-F13}}','E 自算',D.asof,'天')+'</div>'+
  key('Coherent 的季度存货天数从 133 升到 211 天，维谛从 74 升到 112 天；英伟达稳定在 115–119 天。光模块链条的库存在上升，这是「先过剩」判断的主要依据之一。{{PRO-COHR}}{{IND-S26}}{{PRO-LC-DOUBLE}}')+
  '<div class="card"><h3>A 股代表公司：2026 年前三季 vs 2025 年前三季</h3><div id="c4c" class="chart tall"></div>'+cap(esc(D.inv.cn_9m.src),'A 实际','2026-09-30','亿元人民币；存货同比 %')+'</div>'+
  fold('A 股 21 家明细（亿元，A）',tbl(['公司','前三季营收','同比%','营业利润','同比%','经营现金流','上年同期','现金/利润','存货 26-09','存货 25-09','存货同比%','资本开支'],D.inv.cn_9m.rows.map(function(r){
    return [esc(r.name),fnum(r.rev_9m26,1),fnum(r.rev_yoy,1),fnum(r.op_9m26,1),fnum(r.op_yoy,1),fnum(r.ocf_9m26,1),fnum(r.ocf_9m25,1),fnum(r.ocf_to_op,2),fnum(r.inv_2609,1),fnum(r.inv_2509,1),fnum(r.inv_yoy,1),fnum(r.capex_9m26,1)];}),[1,2,3,4,5,6,7,8,9,10,11]))+
  fold('美国公司近 12 个月现金转化（十亿美元，A）',tbl(['代码','营收','营业利润','经营现金流','资本开支','经营现金流/营业利润','截至'],Object.keys(D.inv.cash_conversion).map(function(k){var t=D.inv.cash_conversion[k];
    return [esc(k),fnum(t.rev_ttm,1),fnum(t.oi_ttm,1),fnum(t.ocf_ttm,1),fnum(t.capex_ttm,1),t.oi_ttm>0?fnum(t.ocf_ttm/t.oi_ttm*100,0)+'%':'—',esc(t.thru)];}),[1,2,3,4,5]));
  return {html:h,after:function(){
    chart('c4a',{tooltip:{trigger:'axis'},legend:leg(),grid:grid(),xAxis:{type:'category',data:yrs.map(function(y){return y.replace('_9M',' 前三季');})},yAxis:{type:'value',name:'十亿美元'},
      series:cos.map(function(k){return {name:cn[k],type:'bar',stack:'a',data:yrs.map(function(y){return C.series[k][y];})};})});
    var dd=D.inv.dio_days,ks=Object.keys(dd).filter(function(k){return k!=='note';});
    chart('c4b',{tooltip:{trigger:'axis'},legend:leg(),grid:grid({top:48}),xAxis:{type:'time'},yAxis:{type:'value',name:'天',scale:true},
      series:ks.map(function(k){return {name:k,type:'line',symbolSize:5,data:Object.keys(dd[k]).map(function(d){return [d,dd[k][d]];})};})});
    var rr=D.inv.cn_9m.rows.slice().sort(function(a,b){return a.inv_yoy-b.inv_yoy;});
    chart('c4c',{tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},legend:leg(),grid:grid({left:MOB()?70:90,top:40}),yAxis:{type:'category',data:rr.map(function(r){return r.name;}),axisLabel:{fontSize:11}},xAxis:{type:'value'},
      series:[{name:'营收同比',type:'bar',data:rr.map(function(r){return r.rev_yoy;})},{name:'存货同比',type:'bar',data:rr.map(function(r){return r.inv_yoy;})}]});
  }};
};

/* ---------- 模块 5 供需与产能地图 ---------- */
PAGES.m5=function(){
  var P=D.prices;
  var h=head(5,'全球供需与产能地图','收入落在哪些国家、哪里最紧、价格在往哪走。')+
  '<div class="card"><h3>收入分布：环节 × 地区（近 12 个月）</h3><div id="c5a" class="chart"></div>'+cap('本项目财务面板，按公司注册地/上市地归类','A 实际',D.asof,'十亿美元')+
  '<p class="note"><span class="miss">缺失：</span>这是「公司在哪」，不是「工厂在哪」。全球晶圆、HBM、光模块、变压器的产能地理分布没有统一公开数据（例如台积电美国厂、中际旭创泰国厂没有拆开）。</p></div>'+
  '<div class="card"><h3>哪里最紧，哪里先松</h3>'+tbl(D.tight.head.map(esc),D.tight.rows.map(function(r){return r.map(esc);}))+cap(D.tight.src+'；价格与交期来自报道与机构估计','J 判断（依据为 A/E）',D.asof,'')+'</div>'+
  key('最难缓解的是电：变压器交期 128 周以上、燃机交期按年计{{PRO-GEV}}{{PRO-WOODMAC}}；最先松动的是光模块成品价格（年降约 10%），而上游激光器在涨价。')+
  '<div class="grid"><div class="card"><h3>GPU 每小时租价（挂牌中位数）</h3><div id="c5b" class="chart short"></div>'+cap(esc(P.gpu_rent.src),P.gpu_rent.type,'2026-11-09',P.gpu_rent.unit)+'<p class="note">'+esc(P.gpu_rent_tx.note)+'</p></div>'+
  '<div class="card"><h3>DRAM：价格还在涨，但涨得越来越慢</h3><div id="c5c" class="chart short"></div>'+cap(esc(P.dram_contract_qoq.src),P.dram_contract_qoq.type,'2026-11-10',P.dram_contract_qoq.unit)+'<p class="note">DDR5 16Gb 出口单价：'+P.ddr5_16gb.pts.map(function(p){return esc(p[0])+' '+p[1];}).join(' → ')+' 美元（A，'+esc(P.ddr5_16gb.src)+'）。'+esc(P.ddr5_16gb.note)+'</p></div></div>'+
  fold('光模块价格（E，专家口径）',tbl(['产品','价格（美元/只）','方向'],P.optics.rows.map(function(r){return r.map(esc);}))+cap(esc(P.optics.src),P.optics.type,D.asof,P.optics.unit))+
  fold('变压器与电网设备（A/E）',tbl(['项目','数值'],P.transformer.rows.map(function(r){return r.map(esc);}))+cap(esc(P.transformer.src),P.transformer.type,D.asof,''))+
  fold('PCB 材料价格（A/E）',tbl(['材料','涨价'],P.pcb_materials.rows.map(function(r){return r.map(esc);}))+cap(esc(P.pcb_materials.src),'E 报道',D.asof,''))+
  fold('HBM 价格（报道/预期）','<p class="note">'+esc(P.hbm_price.note)+'</p>'+tbl(['时间','HBM3E 12H','HBM4 12H'],P.hbm_price.HBM3E_12H.map(function(p,i){var q=P.hbm_price.HBM4_12H[i]||[];return [esc(p[0]),fnum(p[1],1),fnum(q[1],1)];}),[1,2])+cap(esc(P.hbm_price.src),P.hbm_price.type,D.asof,P.hbm_price.unit));
  return {html:h,after:function(){
    var RG={'US':'美国','US/IE':'美国','TW':'中国台湾','KR':'韩国','JP':'日本','CN-A':'中国大陆','CN-HK':'中国大陆','EU-DE':'欧洲','EU-FR':'欧洲'},regs=['美国','中国台湾','韩国','日本','中国大陆','欧洲'],segs=['1','2','3','4','5','6'],M={},mx=0;
    D.comp.forEach(function(c){var v=((D.fin[c.id]||{}).revenue_usd||{}).TTM;if(v==null)return;var k=c.seg+'|'+RG[c.region];M[k]=(M[k]||0)+v;});
    var data=[];segs.forEach(function(s,i){regs.forEach(function(r,j){var v=M[s+'|'+r];if(v){v=Math.round(v);mx=Math.max(mx,v);}data.push([j,i,v||'-']);});});
    chart('c5a',{tooltip:{formatter:function(p){return esc(SEGN[segs[p.data[1]]])+'｜'+regs[p.data[0]]+'<br>'+(p.data[2]==='-'?'无样本':p.data[2]+' 十亿美元');}},grid:grid({left:MOB()?78:96,top:10,bottom:70}),
      xAxis:{type:'category',data:regs.map(function(r){return MOB()?r.replace('中国',''):r;}),axisLabel:{interval:0,fontSize:MOB()?10:12}},yAxis:{type:'category',data:segs.map(function(s){return SEGN[s];})},
      visualMap:{min:0,max:mx,calculable:false,orient:'horizontal',left:'center',bottom:0,itemHeight:MOB()?100:160,textStyle:{fontSize:10},inRange:{color:['#E5F1FF','#007AFF']}},
      series:[{type:'heatmap',data:data,label:{show:true,fontSize:11}}]});
    var g=P.gpu_rent;chart('c5b',{tooltip:{trigger:'axis'},legend:leg(),grid:grid({top:36}),xAxis:{type:'category',data:g.weeks.map(function(w){return w.slice(2);})},yAxis:{type:'value',name:'美元',scale:true},
      series:['H100','H200','B200'].map(function(k){return {name:k,type:'line',data:g[k]};})});
    var q=P.dram_contract_qoq;chart('c5c',{tooltip:{trigger:'axis'},grid:grid({top:24}),xAxis:{type:'category',data:q.pts.map(function(p){return p[0];})},yAxis:{type:'value'},
      series:[{type:'bar',data:q.pts.map(function(p){return p[1];}),label:{show:true,position:'top',formatter:'+{c}%'}}]});
  }};
};

/* ---------- 模块 6 利润池迁移 ---------- */
PAGES.m6=function(){
  var pp=D.pp,ks=Object.keys(pp.segments),yrs=Object.keys(pp.grand_total);
  var h=head(6,'利润池迁移','整条链赚的营业利润，按环节分，过去几年怎么搬家。两个口径并排，因为它们回答的问题不同。')+
  '<div class="card"><h3>口径一：AI 相关代表公司篮子（48 家），各环节利润占比</h3><div id="c6a" class="chart"></div>'+cap(esc(pp.caveat),pp.type,pp.asof,'% 占比；合计 '+yrs.map(function(y){return y+' '+fnum(pp.grand_total[y],0);}).join(' / ')+' 十亿美元')+'</div>'+
  key('利润从「卖云的」搬到了「卖铲子的」：存储占比从 2023 年的负数升到 2026E 约 47%（口径一）或 37%（口径二），算力芯片约 34%。云厂商占比在下降，因为它们的利润增长慢于上游。{{SD-PP-2}}{{FIN-F07}}')+
  '<div class="card"><h3>口径二：本项目 35 家全公司口径，各环节营业利润（FY2016–近 12 个月）</h3><div id="c6b" class="chart"></div>'+cap('本项目财务面板，tools/segagg.py；全公司口径（含非 AI 业务，如微软 Office、三星手机），各期样本数 n 不同','A 实际（汇总为 E）',D.asof,'十亿美元')+'</div>'+
  fold('口径一明细（十亿美元，E）',ks.map(function(k){var s=pp.segments[k];return '<h3>'+esc(k)+'</h3>'+tbl(['公司'].concat(yrs),s.rows.map(function(r){return [esc(r.name)].concat(yrs.map(function(y){return fnum(r.v[y],1);}));}).concat([['<b>合计</b>'].concat(yrs.map(function(y){return '<b>'+fnum(s.total[y],1)+'</b>';}))]),yrs.map(function(_,i){return i+1;}));}).join(''))+
  '<p class="note">为什么两个口径不一样：口径一尽量只算 AI 相关公司和分部（加了 Marvell、海力士等更多存储/光模块公司）；口径二用 35 家全公司数据，云厂商的非 AI 利润很大，会压低存储占比。看<b>方向</b>，两者一致；看<b>绝对份额</b>，只能给区间。详见<a href="#xc">交叉核对</a>。</p>';
  return {html:h,after:function(){
    chart('c6a',{tooltip:{trigger:'axis',valueFormatter:function(v){return v+'%';}},legend:leg(),grid:grid({top:56}),xAxis:{type:'category',data:yrs},yAxis:{type:'value',name:'%'},
      series:ks.map(function(k,i){return {name:k.replace(/^\d /,''),type:'bar',stack:'s',itemStyle:{color:COL[i]},data:yrs.map(function(y){return pp.share_pct[k][y];})};})});
    var per=['FY2016','FY2017','FY2018','FY2019','FY2020','FY2021','FY2022','FY2023','FY2024','FY2025','TTM'];
    chart('c6b',{tooltip:{trigger:'axis',formatter:function(ps){var p=per[ps[0].dataIndex];return p+'<br>'+ps.map(function(x){var s=D.segagg[String(x.seriesIndex+1)].series[p]||{};return x.marker+x.seriesName+'：'+(x.value==null?'缺失':x.value)+'（n='+(s.n||0)+'）';}).join('<br>');}},
      legend:leg(),grid:grid({top:56}),xAxis:{type:'category',data:per.map(function(p){return p.replace('FY','');})},yAxis:{type:'value',name:'十亿美元'},
      series:['1','2','3','4','5','6'].map(function(s,i){return {name:SEGN[s],type:'bar',stack:'o',itemStyle:{color:COL[i]},data:per.map(function(p){var x=D.segagg[s].series[p];return x?x.oi:null;})};})});
  }};
};

/* ---------- 模块 7 历史周期对比 ---------- */
PAGES.m7=function(){
  var Hc=D.hist,mu=Hc.micron,yrs=Object.keys(mu.rev);
  var h=head(7,'历史周期对比','过去 8 次周期，顶部和底部之前都出现过什么。用美光做一条完整的样板。')+
  '<div class="card"><h3>美光：营收、营业利润、资本开支和存货天数（FY2015–FY2026）</h3><div id="c7" class="chart"></div>'+cap('美光 10-K（SEC XBRL）；存货天数＝期末存货÷年营业成本×365（自算）{{SD-MU-SEC}}','A 实际（天数为 E 自算）',D.asof,'十亿美元；天')+'</div>'+
  key('两次 DRAM 下行都有同一个顺序：价格见顶 → 存货天数上升 → 利润见底 → 资本开支才削减。资本开支是最后一个反应的。美光 2026 财年营收暴涨，但存货天数从 136 天升到 147 天，与 2019 年下行年持平：利润最高时库存已开始积累。{{SD-DRAM-1}}{{SD-DRAM-2}}{{SD-MU-SEC}}')+
  '<div class="grid">'+Hc.cases.map(function(c){return '<div class="card"><h3>'+esc(c.name)+'</h3>'+
    '<dl class="gloss"><dt>顺序</dt><dd>'+esc(c.seq||'—')+'</dd><dt>价格顶 / 底</dt><dd>'+esc(c.peak_price)+' → '+esc(c.price_trough)+'</dd><dt>库存</dt><dd>'+esc(c.inv)+'</dd><dt>利润</dt><dd>'+esc(c.earn)+'</dd><dt>资本开支</dt><dd>'+esc(c.capex)+'</dd><dt>怎么出清</dt><dd>'+esc(c.clear)+'</dd>'+
    (c.lead?'<dt>顶部前的信号</dt><dd>'+c.lead.map(esc).join('；')+'</dd>':'')+'</dl><p class="cap">证据：'+refs((c.src||[]).map(function(s){return 'SD-'+s;}).filter(function(s){return LED[s];}))+'｜'+ttag('A')+'历史实际</p></div>';}).join('')+'</div>'+
  '<h2>这一轮和历史哪里像、哪里不像</h2>'+tbl(['维度','历史（光纤 2000、DRAM、光伏）','这一轮 AI'],[
   ['买方','新进入者，靠高收益债和 IPO','主要是现金流充裕的巨头；边际上转向发债、表外 SPV 和供应商融资'+R('{{KX-09}}{{MAC-S24}}{{IND-S5}}')],
   ['供给集中度','分散（光伏、光纤）','高度集中（台积电、三家存储、英伟达）'],
   ['瓶颈','产能本身','电和许可，交期按年计'+R('{{PRO-GEV}}')],
   ['技术折旧','光纤能用几十年','GPU 每代快 2–3 倍，经济寿命可能短于会计折旧年限（J）'],
   ['需求真实性','流量没有每 100 天翻倍，2001 年长途光纤利用率不到 3%'+R('{{SD-TEL-FIBER}}'),'AI 云收入在加速，但追不上资本开支'+R('{{KX-08}}{{KX-01}}')]])+
  '<p class="note">'+ttag('J')+'对比为判断，来自 Bot「知识与经验」§4，已用本项目财务数据部分验证。</p>';
  return {html:h,after:function(){
    chart('c7',{tooltip:{trigger:'axis'},legend:leg(),grid:grid({right:MOB()?40:56}),xAxis:{type:'category',data:yrs},yAxis:[{type:'value',name:'十亿美元'},{type:'value',name:'天',splitLine:{show:false}}],
      series:[{name:'营收',type:'bar',data:yrs.map(function(y){return mu.rev[y];})},{name:'营业利润',type:'bar',data:yrs.map(function(y){return mu.oi[y];})},{name:'资本开支',type:'bar',data:yrs.map(function(y){return mu.capex[y];})},
        {name:'存货天数',type:'line',yAxisIndex:1,data:yrs.map(function(y){return mu.dio[y];})}]});
  }};
};

/* ---------- 模块 8 情景模拟器 ---------- */
var M8=Object.assign({},D.sim.presets.B);
function simCalc(x){var out={};Object.keys(D.sim.seg).forEach(function(s){var c=D.sim.seg[s];
  var g=c.base+c.b_capex*x.capex+c.b_rent*x.rent+c.b_dram*x.dram+c.b_lead*x.lead+D.sim.spread_val*x.spread;
  var m=c.m0+c.m_capex*x.capex+c.m_rent*x.rent+c.m_dram*x.dram+c.m_lead*x.lead;out[s]={g:Math.round(g*10)/10,m:Math.round(m*10)/10};});return out;}
PAGES.m8=function(){
  var S=D.sim,sc=D.scen;
  var h=head(8,'三情景模拟器','拖动五个输入，看六个环节 2027 年的营收增速和利润率变化怎么跟着动。系数是判断（J），未经回测，只用来理解「谁先受影响、受多大影响」。')+
  '<div class="card"><div class="ctl"><span class="note">预设：</span><span class="seg" id="m8p">'+['A','B','C'].map(function(k){return '<button data-p="'+k+'">'+k+' 情景（'+S.prob[k]+'%）</button>';}).join('')+'</span></div>'+
  '<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">'+S.inputs.map(function(i){return '<div class="slider"><label for="s_'+i[0]+'">'+esc(i[1])+'（'+esc(i[2])+'）</label><output id="o_'+i[0]+'"></output><input type="range" id="s_'+i[0]+'" min="'+i[3]+'" max="'+i[4]+'" step="1" data-k="'+i[0]+'"></div>';}).join('')+'</div></div>'+
  '<div class="card"><h3>六个环节的反应（2027 年，相对 2026 年）</h3><div id="c8" class="chart"></div>'+cap('本项目情景模型 tools/content.py SIM（线性系数，历史校准见下表）','J 判断',D.asof,'营收增速 %；营业利润率变化 百分点')+'<p class="note" id="m8w"></p></div>'+
  key('传导顺序：光模块最快（1–2 季），算力芯片次之，PCB 因为折旧刚性利润先坏，存储有长约缓冲 2–4 季，电力设备有积压缓冲 4–8 季，云厂商收入最后受影响，但折旧负担会持续 4–8 季。')+
  '<div class="card"><h3>每个环节的系数从哪来</h3>'+tbl(['环节','反应滞后','历史校准'],Object.keys(S.seg).map(function(s){return [esc(segname(s)),esc(S.seg[s].lag),R(S.seg[s].calib)];}))+'</div>'+
  '<h2>三个情景是什么</h2><div class="grid">'+['A','B','C'].map(function(k){return '<div class="card"><h3>'+k+' 情景　'+ttag('J')+'概率 '+sc.prob[k]+'%</h3><p>'+esc(sc.defs[k])+'</p><p class="note"><b>看到这些信号就往这个情景靠：</b><br>'+(sc.signals[k]||[]).map(esc).join('<br>')+'</p></div>';}).join('')+'</div>'+
  fold('情景 × 环节 矩阵（定性，J）',tbl(['环节','情景','营收','利润率','自由现金流','估值'],[].concat.apply([],Object.keys(sc.matrix).map(function(s){return ['A','B','C'].map(function(k){var m=sc.matrix[s][k];return [esc(segname(s)),k,esc(m.revenue),esc(m.margin),esc(m.fcf),esc(m.valuation)];});}))))+
  '<p class="note">'+(sc.transmission||[]).map(esc).join('<br>')+'</p>';
  return {html:h,after:function(){
    var segs=['1','2','3','4','5','6'],c=chart('c8',{});
    function draw(){S.inputs.forEach(function(i){var el=document.getElementById('s_'+i[0]);el.value=M8[i[0]];document.getElementById('o_'+i[0]).textContent=(M8[i[0]]>0?'+':'')+M8[i[0]]+(i[2]==='bp'?'bp':'%');});
      var r=simCalc(M8);
      c.setOption(prep(c.__el,{animation:false,tooltip:{trigger:'axis'},legend:leg(),grid:grid({right:MOB()?40:56,top:60}),xAxis:{type:'category',data:segs.map(SS),axisLabel:{interval:0,fontSize:MOB()?10:12}},
        yAxis:[{type:'value',name:'营收增速 %',nameTextStyle:{fontSize:10}},{type:'value',name:'利润率 pp',nameTextStyle:{fontSize:10},splitLine:{show:false},min:function(v){return Math.floor(v.min)-1;},max:function(v){return Math.ceil(v.max)+1;}}],
        series:[{name:'营收增速',type:'bar',data:segs.map(function(s){return r[s].g;})},{name:'营业利润率变化',type:'scatter',symbolSize:12,yAxisIndex:1,clip:false,label:{show:true,fontSize:10,formatter:function(p){return p.value;}},data:segs.map(function(s){return r[s].m;})}]}),true);
      var E={};segs.forEach(function(s){E[s]=0;});['A','B','C'].forEach(function(k){var x=simCalc(S.presets[k]);segs.forEach(function(s){E[s]+=x[s].g*S.prob[k]/100;});});
      document.getElementById('m8w').innerHTML='按概率加权（A '+S.prob.A+'% / B '+S.prob.B+'% / C '+S.prob.C+'%）的 2027 年营收增速：'+segs.map(function(s){return esc(SEGN[s])+' '+fnum(E[s],0)+'%';}).join('，')+'。'+ttag('J')+'判断，不是预测。';
      [].forEach.call(document.querySelectorAll('#m8p button'),function(b){var p=S.presets[b.getAttribute('data-p')],on=Object.keys(p).every(function(k){return p[k]==M8[k];});b.className=on?'on':'';});}
    V.querySelectorAll('input[type=range]').forEach(function(el){el.oninput=function(){M8[el.getAttribute('data-k')]=+el.value;draw();};});
    V.querySelectorAll('#m8p button').forEach(function(b){b.onclick=function(){M8=Object.assign({},S.presets[b.getAttribute('data-p')]);draw();};});
    draw();
  }};
};

/* ---------- 模块 9 机会/风险排名 ---------- */
PAGES.m9=function(){
  var dim=D.rankdim;function tot(o){return o[1].reduce(function(a,b){return a+b;},0);}
  var O=D.opp.slice().sort(function(a,b){return tot(b)-tot(a);}),K=D.risk.slice().sort(function(a,b){return tot(a)-tot(b);});
  function rows(L){return L.map(function(o,i){return [String(i+1),esc(o[0])].concat(o[1].map(String)).concat(['<b>'+tot(o)+'</b>',esc(o[3])+refs(o[2])]);});}
  var hd=['#','对象'].concat(dim).concat(['总分','一句话与证据']),nc=[2,3,4,5,6,7];
  var h=head(9,'未来 12–24 个月：机会与风险排名','五个维度各打 1–5 分（5 最好），总分 25。打分是判断（J），每一行都附证据。')+
  '<div class="card"><h3>机会（总分从高到低）</h3><div id="c9a" class="chart"></div>'+tbl(hd,rows(O),nc)+cap('本项目打分 tools/content.py OPP，证据见尾注','J 判断',D.asof,'分（1–5）')+'</div>'+
  key('最好的位置是「稀缺能持续 + 客户预付 + 自己不乱扩产」：燃机与电网设备、台积电、上游材料（T-glass、激光器）。估值安全分普遍低，意思是好公司已经不便宜。')+
  '<div class="card"><h3>风险（总分从低到高，越靠前越危险）</h3><div id="c9b" class="chart"></div>'+tbl(hd,rows(K),nc)+cap('本项目打分 tools/content.py RISK','J 判断',D.asof,'分（1–5）')+'</div>'+
  fold('估值快照（'+esc(D.val.asof)+'，'+D.val.rows.length+' 家）',tbl(['公司','代码','市值 十亿美元','PE（TTM）','远期 PE','市销率','市值/营业利润','FCF 收益率 %','行情日期'],D.val.rows.map(function(r){
    return [esc(r.company),esc(r.symbol),fnum(r.mktcap_usd_bn,0),fnum(r.pe_ttm,1),fnum(r.pe_fwd,1),fnum(r.ps_ttm,1),fnum(r.ev_proxy_p_oi,1),fnum(r.fcf_yield_pct,1),esc(r.asof)];}),[2,3,4,5,6,7])+'<p class="note">'+esc(D.val.note)+'（'+ttag('A')+'行情；比率为 E 自算；标 * 的不在 35 家面板内，财务数据缺失）'+R('{{KX-14}}')+'</p>');
  return {html:h,after:function(){
    function bars(id,L){chart(id,{tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},legend:leg(),grid:grid({left:8,top:40,containLabel:true}),
      yAxis:{type:'category',inverse:true,data:L.map(function(o){var n=o[0];n=n.replace(/（.*$/,'');return MOB()&&n.length>9?n.slice(0,9)+'…':(n.length>16?n.slice(0,16)+'…':n);}),axisLabel:{fontSize:11}},xAxis:{type:'value',max:25},
      series:dim.map(function(d,j){return {name:d,type:'bar',stack:'t',data:L.map(function(o){return o[1][j];})};})});}
    bars('c9a',O);bars('c9b',K);
  }};
};

/* ---------- 模块 10 证据台账 ---------- */
var M10={q:'',type:'',verify:'',origin:'',page:0};
PAGES.m10=function(q){
  if(q.id){M10.q=q.id;M10.page=0;}
  function uniq(k){var s={};D.ledger.forEach(function(r){s[r[k]]=1;});return Object.keys(s).sort();}
  function opts(k,lab){return '<select data-f="'+k+'"><option value="">'+lab+'：全部</option>'+uniq(k).map(function(v){return '<option'+(M10[k]===v?' selected':'')+'>'+esc(v)+'</option>';}).join('')+'</select>';}
  var h=head(10,'证据台账','本项目所有关键数字的出处。可以搜索、按类型和核对状态筛选。正文里的上标数字都指向这里。')+
  '<div class="card"><div class="ctl"><input type="search" id="m10q" placeholder="搜索 ID、公司、指标、来源…" value="'+esc(M10.q)+'">'+opts('type','类型')+opts('verify','核对')+opts('origin','来源线')+'</div><p class="note" id="m10n"></p><div id="m10t"></div></div>'+
  '<p class="note">'+Object.keys(D.types).map(function(k){return ttag(k)+esc(D.types[k]);}).join('　')+'。「能否支撑标题」为 N 的证据（单一来源、未核、已降级）不单独支撑任何标题级结论。</p>';
  return {html:h,after:function(){
    function draw(){var t=M10.q.toLowerCase();
      var L=D.ledger.filter(function(r){return (!M10.type||r.type===M10.type)&&(!M10.verify||r.verify===M10.verify)&&(!M10.origin||r.origin===M10.origin)&&
        (!t||[r.gid,r.claim,r.value,r.source,r.seg,r.note].join(' ').toLowerCase().indexOf(t)>=0);});
      var per=50,pg=Math.min(M10.page,Math.max(0,Math.ceil(L.length/per)-1));M10.page=pg;
      document.getElementById('m10n').textContent='共 '+L.length+' 条（台账总数 '+D.ledger.length+'）';
      var rows=L.slice(pg*per,pg*per+per).map(function(r){return '<tr id="row-'+esc(r.gid)+'"'+(r.gid===M10.q?' class="hl"':'')+'><td><b>'+esc(r.gid)+'</b></td><td>'+esc(r.seg)+'</td><td style="min-width:220px">'+esc(r.claim)+'</td><td style="min-width:120px">'+esc(r.value)+' '+esc(r.unit)+' '+esc(r.currency)+'</td><td>'+esc(r.period)+'</td><td>'+ttag(r.type)+'</td><td>'+vtag(r.verify)+'</td><td>'+(r.headline_ok==='N'?'<span class="tag tX">N</span>':'Y')+'</td><td style="min-width:160px">'+(r.url?'<a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.source)+'</a>':esc(r.source))+'<br><span class="note">'+esc(r.tier)+'｜'+esc(r.origin)+'</span></td><td style="min-width:140px" class="note">'+esc(r.note)+'</td></tr>';}).join('');
      document.getElementById('m10t').innerHTML='<div class="pager"><button id="pp">上一页</button><span>第 '+(pg+1)+' / '+Math.max(1,Math.ceil(L.length/per))+' 页</span><button id="pn">下一页</button></div><div class="tbl"><table><thead><tr><th>ID</th><th>环节</th><th>说法</th><th>数值</th><th>期间</th><th>类型</th><th>核对</th><th>能否支撑标题</th><th>来源</th><th>备注</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
      document.getElementById('pp').onclick=function(){if(M10.page>0){M10.page--;draw();}};document.getElementById('pn').onclick=function(){M10.page++;draw();};}
    document.getElementById('m10q').oninput=function(e){M10.q=e.target.value;M10.page=0;draw();};
    V.querySelectorAll('select[data-f]').forEach(function(s){s.onchange=function(){M10[s.getAttribute('data-f')]=s.value;M10.page=0;draw();};});
    draw();
  }};
};

/* ---------- 20 问 ---------- */
PAGES.qa=function(){
  var h='<h1>20 个问题的回答</h1><p class="lead">每条先给结论，再给证据、最强反证、置信度，以及什么会让我改主意。上标数字可点开看出处。</p>'+
  '<div class="bluf"><div class="k">先说结论</div><p>'+R(D.bluf)+'</p><div class="k" style="margin-top:8px">主要矛盾</div><p>'+R(D.contradiction)+'</p></div>'+
  '<div class="card"><b>目录</b><ol style="font-size:14px;margin:6px 0;padding-left:22px">'+D.q.map(function(q){return '<li><a href="#qa" data-q="'+q.n+'">'+esc(q.q)+'</a></li>';}).join('')+'</ol></div>'+
  D.q.map(function(q){var c=/高/.test(q.conf)?'tA':/低/.test(q.conf)?'tX':'tJ';
    return '<div class="qa" id="q'+q.n+'"><h3>Q'+q.n+'. '+esc(q.q)+'</h3><div class="ans">'+R(q.a)+'</div>'+
    '<div class="row"><b>为什么</b>'+R(q.why)+'</div><div class="row"><b>证据</b>'+refs(q.ev)+' <span class="note">'+q.ev.map(esc).join('、')+'</span></div>'+
    '<div class="row"><b>最强反证</b>'+R(q.counter)+'</div><div class="row"><b>置信度</b><span class="tag '+c+'">'+esc(q.conf)+'</span></div><div class="row"><b>什么会让我改主意</b>'+R(q.change)+'</div></div>';}).join('');
  return {html:h,after:function(){V.querySelectorAll('a[data-q]').forEach(function(a){a.onclick=function(e){e.preventDefault();document.getElementById('q'+a.getAttribute('data-q')).scrollIntoView({behavior:'smooth'});};});}};
};
PAGES.method=function(){return {html:'<div class="doc">'+D.docs.method+'</div>'};};
PAGES.xc=function(){return {html:'<div class="doc">'+D.docs.crosscheck+'</div>'};};

route();
})();
