const S=(t,d)=>`<div class="src">来源：${t}${d?' · '+d:''}</div>`;
const NA=t=>`<div class="na">未接入：${t}</div>`;
const nodesOf=ch=>Object.entries(L.nodes).filter(([k])=>k.startsWith(ch+'|')).map(([k,v])=>({node:k.split('|')[1],...v}));
const q2=e=>e?`${e.slice(0,4)}Q${Math.ceil(+e.slice(4,6)/3)}`:'—';
function lineMulti(id,series,opt={}){const el=document.getElementById(id);if(!el)return;echarts.init(el).setOption({grid:{left:44,right:opt.r2?44:8,top:24,bottom:22},tooltip:{trigger:'axis'},legend:{top:0,textStyle:{color:'#888',fontSize:10},itemHeight:6},
 xAxis:{type:'category',data:series[0].x,axisLabel:{color:'#888',fontSize:9}},yAxis:[{type:'value',scale:true,axisLabel:{color:'#888',fontSize:9},splitLine:{lineStyle:{color:dark?'#2c2d31':'#eee'}}},{type:'value',scale:true,show:!!opt.r2,axisLabel:{color:'#888',fontSize:9},splitLine:{show:false}}],
 series:series.map((s,i)=>({name:s.n,type:s.t||'line',yAxisIndex:s.r?1:0,data:s.y,showSymbol:false,barMaxWidth:12}))})}
function render(){const m=$('#m');document.querySelectorAll('.chart,[id^=tm]').forEach(e=>echarts.getInstanceByDom(e)?.dispose());let h=seg();const ns=nodesOf(chain),dd=C.date;
 const D=`${dd.slice(0,4)}-${dd.slice(4,6)}-${dd.slice(6)}`;
 if(tab==='sum'){const s=L.summary[chain];h+=`<div class="sum"><div class="sub">${chain} · 一句话判断（规则生成）</div><div class="l">${s.line}</div><div style="margin-top:6px">关键数据：<b>${s.key}</b></div>${S('信号=②③层财务 + ①层量价（见各层）；股价=Tushare 20日涨跌',D)}</div>`;
  h+='<h3>各节点：产业信号 vs 股价</h3><div class="grid">'+ns.map(n=>`<div class="node" style="border-left-color:${n.signal==='改善'?'var(--up)':n.signal==='恶化'?'var(--dn)':'var(--mut)'}" onclick="detail('${n.node}')"><b>${n.node}</b> <span class="pill p${n.signal}">${n.signal}</span>
   <div class="row"><span>20日股价</span><span>${f(n.d20)}</span></div><div class="flag" style="margin-top:4px">${n.flag}</div></div>`).join('')+'</div><div class="sub" style="margin-top:6px">点节点看代表股、财务与新闻</div>';m.innerHTML=h;return}
 if(tab==='l1'){if(chain==='AI算力'){const T=L.tw,ks=Object.keys(T.data);
   h+=`<h3>台湾供应链月营收（同比 %）</h3><div class="kv">${ks.map(k=>{const v=T.data[k].at(-1);return v?`<div><div class="sub">${T.names[k]} ${v[0]}</div><div class="big">${f(v[3])}</div><div class="sub">${v[1].toLocaleString()} 亿新台币 · 环比 ${f(v[2])}</div></div>`:''}).join('')}</div>
   <div class="card"><div class="chart" id="tw1" style="height:240px"></div>${S(`<a href="${T.url}">${T.src}</a>`,'最新 '+T.data['2330'].at(-1)[0])}</div>`;
   const dr=L.dram;h+='<h3>存储现货价</h3>'+(dr?`<div class="card"><table><tr><th>品项</th><th>均价 $</th><th>日变动</th></tr>${Object.entries(dr.spot).map(([k,v])=>`<tr><td>${k}</td><td>${v[0]}</td><td>${v[1]}</td></tr>`).join('')}</table>${S(`<a href="${dr.url}">${dr.src}</a>`,Object.keys(dr.hist).length+' 天累积历史（从今天开始每日留存，暂无同比）')}</div>`:NA('DRAMeXchange'))+NA('HBM 合约价（无免费公开序列；模型假设见②层）');
  }else{const cu=L.cu.data.slice(-260),lm=L.lme?L.lme.data.slice(-260):null,iv=L.cu_inv;
   h+=`<div class="kv"><div><div class="sub">沪铜主连 ${cu.at(-1)[0]}</div><div class="big">${(+cu.at(-1)[1]).toLocaleString()}</div><div class="sub">同比 ${f(L.cu_yoy)} · 30日 ${f(L.cu_mom)}</div></div>
   <div><div class="sub">LME 3M铜 ${lm?lm.at(-1)[0]:''}</div><div class="big">${lm?(+lm.at(-1)[1]).toLocaleString():'—'}</div><div class="sub">美元/吨</div></div></div>
   <div class="card"><div class="chart" id="cu1" style="height:230px"></div>${S(L.cu.src+' / '+(L.lme?L.lme.src:'LME 未接入'),cu.at(-1)[0])}</div>
   <h3>交易所库存</h3>${iv?`<div class="card"><div class="chart" id="inv1"></div>${S(iv.src+'（单日跳变请以上期所周报核对）',iv.data.at(-1)[0])}</div>`:NA('沪铜库存')}${NA('LME 库存')}${NA('铜精矿 TC/RC（无稳定免费源）')}`}
  m.innerHTML=h;
  if(chain==='AI算力'){const T=L.tw.data,x=T['2330'].map(v=>v[0]);lineMulti('tw1',Object.keys(T).map(k=>({n:L.tw.names[k],x,y:x.map(d=>(T[k].find(v=>v[0]===d)||[])[3]??null)})))}
  else{const cu=L.cu.data.slice(-260);lineMulti('cu1',[{n:'沪铜 元/吨',x:cu.map(v=>v[0]),y:cu.map(v=>+v[1])},...(L.lme?[{n:'LME 美元/吨',r:1,x:[],y:cu.map(v=>{const r=L.lme.data.find(z=>z[0]===v[0]);return r?+r[1]:null})}]:[])],{r2:1});
   if(L.cu_inv){const iv=L.cu_inv.data;lineMulti('inv1',[{n:'库存(吨)',t:'bar',x:iv.map(v=>v[0]),y:iv.map(v=>v[1])}])}}return}
 if(tab==='l2'){h+=`<h3>库存周期与订单（节点中位数，最新报告期同比）</h3><div class="card"><table><tr><th>节点</th><th>存货周转天数Δ</th><th>合同负债同比</th><th>报告期</th></tr>${ns.map(n=>`<tr><td>${n.node}</td><td>${n.inv_chg==null?'—':(n.inv_chg>0?'+':'')+n.inv_chg.toFixed(0)+'天'}</td><td>${f(n.cl_yoy)}</td><td>${q2(n.report)}</td></tr>`).join('')}</table>
  ${S('Tushare fina_indicator(invturn_days) / balancesheet(contract_liab+adv_receipts)，代表股中位数','季报')}<div class="sub">读法：周转天数下降+合同负债上升=去库+订单前置（景气上行）。</div></div>`+NA('资本开支 capex、产能利用率、交期（下一版）');
  if(chain==='AI算力')h+=`<h3>GB300 产能瓶颈（模型假设，非官方）</h3><div class="card"><table>${L.model.rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td><td class="sub">${r[2]}</td></tr>`).join('')}</table>${S(L.model.src)}</div>`;m.innerHTML=h;return}
 if(tab==='l3'){h+=`<h3>毛利率趋势（节点中位数，近8季）</h3><div class="card"><div class="chart" id="gm1" style="height:280px"></div>${S('Tushare fina_indicator grossprofit_margin，单位 %','最新 '+q2(ns[0].report))}</div>
  <div class="card"><table><tr><th>节点</th><th>最新毛利率</th><th>同比Δpct</th><th>定价权</th></tr>${ns.map(n=>`<tr><td>${n.node}</td><td>${n.gm.length?n.gm.at(-1)[1].toFixed(1)+'%':'—'}</td><td>${f(n.gm_chg,'')}</td><td>${n.gm_chg>2?'增强':n.gm_chg<-1?'削弱':'持平'}</td></tr>`).join('')}</table><div class="sub">累计口径毛利率（年初至今），同比=对比去年同期。</div></div>`;m.innerHTML=h;
  const x=[...new Set(ns.flatMap(n=>n.gm.map(g=>g[0])))].sort().slice(-8);lineMulti('gm1',ns.map(n=>({n:n.node,x:x.map(q2),y:x.map(e=>(n.gm.find(g=>g[0]===e)||[])[1]??null)})));return}
 if(tab==='l4'){const ev=L.events.filter(e=>e[2]===chain||e[2]==='两链');const an=L.ann.items.filter(a=>a.tags.some(t=>t[0]===chain));
  h+=`<h3>催化剂日历</h3><div class="card"><table>${ev.map(e=>`<tr><td style="white-space:nowrap">${e[0].slice(5)}</td><td style="text-align:left">${e[1]}</td><td class="sub">${e[3]}</td></tr>`).join('')}</table>${S('MOPS/SHFE 规则日期；财报日为预计','生成 '+L.gen)}</div>`;
  if(chain==='AI算力')h+=`<h3>可证伪点（我们若错，会在这里看到）</h3><div class="card">${L.falsify.rows.map(r=>`<div class="news"><b>${r[1]}</b><div class="meta">${r[0]} · 基准 ${r[2]} · 证伪阈值：${r[3]}</div></div>`).join('')}${S(L.falsify.src)}</div>`;
  h+=`<h3>节点股公告（扩产/订单/涨价…）</h3><div class="card">${an.slice(0,40).map(a=>`<div class="news"><a href="${a.url}" target="_blank">${a.name}：${a.title}</a><div class="meta"><span class="tg">${a.tags.find(t=>t[0]===chain)[1]}</span><span class="tg">${a.kw}</span> ${a.time}</div></div>`).join('')||'<div class="sub">近60日无匹配公告</div>'}${S(L.ann.src)}</div>`;m.innerHTML=h;return}
 if(tab==='l5'){window.sub5=window.sub5||'对照';h+=`<div class="seg">${['对照','热力图','新闻'].map(o=>`<button class="${o===sub5?'on':''}" onclick="sub5='${o}';render()">${o}</button>`).join('')}</div>`;
  if(sub5==='对照'){h+=`<div class="card"><table><tr><th>节点</th><th>产业</th><th>20日</th><th>主力亿</th><th>判断</th></tr>${ns.map(n=>`<tr onclick="detail('${n.node}')"><td>${n.node}</td><td><span class="pill p${n.signal}">${n.signal}</span></td><td>${f(n.d20,'')}</td><td>${f(n.mf,'')}</td><td style="font-size:11px">${n.flag}</td></tr>`).join('')}</table>
   ${S('产业=①②③层规则打分（≥2改善，≤-1恶化）；股价/资金=Tushare',D)}<div class="sub">规则：改善且20日涨幅&lt;3% → 产业变好但股价未动；未改善且20日涨幅&gt;10% → 股价跑在基本面前。</div></div>`;m.innerHTML=h;return}
  if(sub5==='热力图'){const nd=C.chains[chain];h+=`<div class="card"><div id="tm" style="height:520px"></div>${S('Tushare daily_basic 总市值 / daily 涨跌',D)}</div>`;m.innerHTML=h;
   echarts.init($('#tm')).setOption({series:[{type:'treemap',data:nd.map(n=>({name:`${n.node} ${n.d1>0?'+':''}${n.d1}%`,children:n.stocks.map(s=>({name:s.name,value:s.mv||1,d1:s.d1,itemStyle:{color:col(s.d1)}}))})),roam:false,nodeClick:false,breadcrumb:{show:false},width:'100%',height:'100%',
    upperLabel:{show:true,height:18,fontSize:10,color:dark?'#eee':'#333',overflow:'truncate',ellipsis:''},itemStyle:{borderColor:dark?'#121315':'#f6f5f1',borderWidth:1,gapWidth:1},levels:[{itemStyle:{borderWidth:3,gapWidth:3,borderColor:dark?'#121315':'#f6f5f1'}},{}],
    label:{formatter:p=>`${p.name}\n${p.data.d1>0?'+':''}${p.data.d1?.toFixed(1)}%`,color:'#fff',fontSize:10,overflow:'break',lineHeight:12}}]});return}
  window.nf='全部';const it=N.items.filter(x=>x.tags.some(t=>t[0]===chain));h+=`<div class="card">${it.slice(0,80).map(nh).join('')||'暂无'}</div><div class="sub">仅显示标题命中节点关键词或个股名称的条目（${it.length}条）</div>`;m.innerHTML=h}}
