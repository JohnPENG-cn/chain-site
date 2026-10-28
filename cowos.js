/* cowos.js — CoWoS 小链：模型与图表。通用组件见 chain.js */
let J,H=null,mk='all';const $=CH.$,V=CH.V;
const VC={'英伟达':'#76b900','AMD':'#ed1c24','其他GPU':'#9a9a9a','谷歌TPU':'#4285f4','AWS':'#ff9900','其他ASIC':'#8a5cf6'};
const sv=id=>+document.getElementById(id).value;
function supply(y,ts,nt,ut){return(12*(ts[y-1]+nt[y-1])+6.5*((ts[y]-ts[y-1])+(nt[y]-nt[y-1])))*ut}
function hbmSup(y){if(!H||!H.supply[y])return null;const s=Object.values(H.supply[y]).reduce((a,b)=>a+b,0);return s*12*H.gbw[y]*H.ut[y]/1e6}
function P0(){return{cap:sv('cw-cap'),os:sv('cw-os'),ut:sv('cw-ut')/100,ppw:sv('cw-ppw')/100,dem:sv('cw-dem')/100,hbm:sv('cw-hbm')/100,oth:1,hs:1}}
function calc(p=P0()){const m=J.model,ts={...m.ts},nt={...m.nt};ts[2027]=p.cap;nt[2027]=p.os;
 const r={};for(let y=2023;y<=2027;y++){const rows=m.demand.filter(x=>x.y==y),L=y==2027;const k=L?p.dem:1,pp=L?p.ppw:1,g=L?p.hbm:1;
  const d=rows.reduce((a,x)=>a+x.units*k/(x.ppw*pp)*1000,0)+m.other[y]*(L?p.oth*k:1),s=supply(y,ts,nt,y>=2026?p.ut:m.ut),hbm=rows.reduce((a,x)=>a+x.units*k*x.gb*g,0)/1000,hs0=hbmSup(y);
  r[y]={d,s,du:d+(m.uncon[y]||0)*(L?k/pp:1),hbm,hs:hs0==null?null:hs0*(L?p.hs:1)}}return r}
function drawTor(){const b=P0(),g=q=>{const x=calc(q)[2027];return(x.s-x.d)/x.d},sh=q=>{const x=calc(q)[2027];return x.s/x.d-x.hs/x.hbm},w=(o)=>({...b,...o});
 const A=[['每片可封颗数（面积通胀）',{ppw:b.ppw*.8},{ppw:b.ppw*1.2},'−20%','+20%','只有 H100/B200 两个公开锚点'],['加速器出货',{dem:b.dem*.8},{dem:b.dem*1.2},'−20%','+20%','KGI 与 MS/UBS 需求口径差约 ±5%，取宽'],['台积电 2027 年末产能',{cap:155},{cap:200},'155k（JPM）','200k（MS）','券商区间 源1,3,6'],['非台积电 2027 年末产能',{os:50},{os:110},'50k','110k','UBS 行业口径推算'],['2026–27 有效稼动率',{ut:.88},{ut:1},'88%','100%','估'],['其他需求（交换芯片等）',{oth:.5},{oth:1.5},'×0.5','×1.5','估']];
 const B=[['HBM 可供量',{hs:.85},{hs:1.08},'×0.85','×1.08（KGI +45–50%）','下限：三星把 HBM 产能转去做 DDR5（HBM 页源65）；上限：KGI 2027 供给增速'],['每封装 HBM 容量',{hbm:b.hbm*.7},{hbm:b.hbm*1.1},'−30%（降规格）','+10%','KGI：英伟达下调规格'],['每片可封颗数',{ppw:b.ppw*.8},{ppw:b.ppw*1.2},'−20%','+20%','估'],['台积电 2027 年末产能',{cap:155},{cap:200},'155k','200k','源1,3,6'],['加速器出货',{dem:b.dem*.8},{dem:b.dem*1.2},'−20%','+20%','估']];
 const mk=(L,f)=>L.map(a=>({n:a[0],lo:f(w(a[1])),hi:f(w(a[2])),l1:a[3],l2:a[4],src:a[5]}));
 CH.tornado('cw-cTorA',g(b),mk(A,g),{flip:0,flipLbl:'0：供需平衡'});
 CH.tornado('cw-cTorB',sh(b),mk(B,sh),{flip:0,flipLbl:'0：短板换成 CoWoS',fmt:v=>(v>0?'+':'')+(v*100).toFixed(0)+'pp'})}
function setOut(){['cap','os','ut','ppw','dem','hbm'].forEach(k=>{const v=sv('cw-'+k);$('#cw-o-'+k).textContent=k=='cap'||k=='os'?v+'k':v+'%'})}
function drawBal(){setOut();const r=calc(),ys=[2023,2024,2025,2026,2027],x=r[2027],g=(x.s-x.d)/x.d,gu=(x.s-x.du)/x.du;
 const f=v=>(v>0?'+':'')+(v*100).toFixed(0)+'%';$('#cw-gap').textContent=f(g);$('#cw-gapu').textContent=f(gu);$('#cwHGap').textContent=f(g);
 $('#cw-gapTxt').textContent=`2027 需求 ${(x.d/1000).toFixed(2)} 百万片（客户需求口径 ${(x.du/1000).toFixed(2)}）· 供给 ${(x.s/1000).toFixed(2)} 百万片`;
 const c=CH.C('cw-cBal');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:44,right:14,top:CH.mob()?62:40,bottom:30},xAxis:{data:ys.map(String)},yAxis:{name:'千片/年',...CH.ax()},
  tooltip:{trigger:'axis',confine:true,formatter:p=>{const o=r[p[0].name];return`${p[0].name}<br>需求 ${o.d.toFixed(0)}k 片<br>供给 ${o.s.toFixed(0)}k 片<br>缺口 ${((o.s-o.d)/o.d*100).toFixed(1)}%`}},
  series:[{name:'需求（可见出货）',type:'bar',data:ys.map(y=>+r[y].d.toFixed(0)),itemStyle:{color:'#d9534f',borderRadius:[4,4,0,0]}},{name:'供给',type:'bar',data:ys.map(y=>+r[y].s.toFixed(0)),itemStyle:{color:'#5b8def',borderRadius:[4,4,0,0]},label:{show:true,position:'top',color:V('--fg'),fontSize:11,formatter:p=>{const o=r[p.name];return((o.s-o.d)/o.d*100).toFixed(0)+'%'}}},
  {name:'MS 需求口径',type:'scatter',symbol:'diamond',symbolSize:11,data:[[3,1394],[4,2694]],itemStyle:{color:V('--fg')}},{name:'UBS 需求口径',type:'scatter',symbol:'triangle',symbolSize:11,data:[[3,1307],[4,2475]],itemStyle:{color:'#999'}}]});
 drawIf(r);drawTor()}
function resetS(){[['cw-cap',185],['cw-os',80],['cw-ut',95],['cw-ppw',100],['cw-dem',100],['cw-hbm',100]].forEach(([i,v])=>document.getElementById(i).value=v);drawBal()}
function drawCap(){const K=J.model.cap,c=CH.C('cw-cCap'),mob=CH.mob(),src=[['KGI',[[15,120],[19,185]],'#d9534f'],['MS',[[15,130],[19,200]],'#333'],['UBS',[[19,180]],'#888'],['JPM',[[15,115],[19,155]],'#2e8b57']];
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:44,right:12,top:mob?64:44,bottom:30},xAxis:{type:'category',data:K.q,axisLabel:{interval:3}},yAxis:{name:'千片/月',...CH.ax()},
  tooltip:{trigger:'axis',confine:true},series:[{name:'台积电',type:'line',stack:'c',areaStyle:{opacity:.4},showSymbol:false,data:K.tsmc,color:'#d9534f'},{name:'非台积电',type:'line',stack:'c',areaStyle:{opacity:.4},showSymbol:false,data:K.osat,color:'#9ccc65'}]
  .concat(src.map(s=>({name:'台积电年末·'+s[0],type:'scatter',symbolSize:9,data:s[1],itemStyle:{color:s[2]},tooltip:{trigger:'item',formatter:p=>s[0]+' '+K.q[p.value[0]]+'：'+p.value[1]+'k'}})))})}
function drawMix(){const m=J.model,ys=[2023,2024,2025,2026,2027],c=CH.C('cw-cMix');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:44,right:14,top:CH.mob()?62:44,bottom:30},xAxis:{data:ys.map(String)},yAxis:{name:'千片',...CH.ax()},
  tooltip:{trigger:'axis',confine:true,formatter:p=>{const y=+p[0].name;let s=y+' 明细（出货 ÷ 每片颗数）<br>';m.demand.filter(x=>x.y==y).forEach(x=>s+=`${x.v} ${x.chip}: ${x.units}M ÷ ${x.ppw} = ${(x.units/x.ppw*1000).toFixed(0)}k<br>`);return s+`其他（交换芯片/FPGA 等，估）: ${m.other[y]}k`}},
  series:Object.keys(VC).map(k=>({name:k,type:'bar',stack:'a',itemStyle:{color:VC[k]},data:ys.map(y=>+m.demand.filter(x=>x.y==y&&x.v==k).reduce((a,x)=>a+x.units/x.ppw*1000,0).toFixed(0))})).concat([{name:'其他',type:'bar',stack:'a',itemStyle:{color:'#cfd8dc'},data:ys.map(y=>m.other[y])}])})}
function drawInf(){const m=J.model,ys=[2023,2024,2025,2026,2027],nv=m.demand.filter(x=>x.v=='英伟达'&&!/CPU/.test(x.chip)),u=ys.map(y=>nv.filter(x=>x.y==y).reduce((a,x)=>a+x.units,0)),w=ys.map(y=>nv.filter(x=>x.y==y).reduce((a,x)=>a+x.units/x.ppw,0));
 const c=CH.C('cw-cInf');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:44,right:14,top:CH.mob()?56:40,bottom:30},xAxis:{data:ys.map(String)},yAxis:{name:'2023=100',type:'log',...CH.ax()},
  tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(+v).toFixed(0)},series:[{name:'英伟达 GPU 颗数',type:'line',data:u.map(x=>+(x/u[0]*100).toFixed(0)),color:'#76b900',symbolSize:8,label:{show:true,formatter:'{c}',fontSize:10}},{name:'对应 CoWoS 片数',type:'line',data:w.map(x=>+(x/w[0]*100).toFixed(0)),color:'#d9534f',symbolSize:8,label:{show:true,formatter:'{c}',fontSize:10}}]})}
function drawPool(){const P=J.profit.pool.slice().sort((a,b)=>b.gm-a.gm),c=CH.C('cw-cPool');let x0=0;const data=P.map(p=>{const d=[x0,x0+p.rev,p.gm,p.seg,p.rev*p.gm/100,p.est];x0+=p.rev;return d}),tot=x0,cl=['#d9534f','#5b8def','#26a69a','#8a5cf6','#ff9900','#9ccc65'];
 c.setOption({...CH.base(),tooltip:{trigger:'item',confine:true,formatter:p=>{const q=P[p.dataIndex];return`<b>${q.seg}</b><br>营收约 ${q.rev} 十亿美元/年 · 毛利率 ${q.gm}%${q.est?'（估）':''}<br>毛利约 ${(q.rev*q.gm/100).toFixed(1)} 十亿美元<br><span style="font-size:11px;opacity:.7">${q.note}</span>`}},grid:{left:44,right:14,top:34,bottom:44},
  xAxis:{type:'value',max:Math.ceil(tot),name:'年化营收（十亿美元，宽度）',nameLocation:'middle',nameGap:26,...CH.ax()},yAxis:{type:'value',max:70,name:'毛利率%',...CH.ax()},
  series:[{type:'custom',renderItem:(pr,api)=>{const a=api.coord([api.value(0),api.value(2)]),b=api.coord([api.value(1),0]);return{type:'group',children:[{type:'rect',shape:{x:a[0],y:a[1],width:b[0]-a[0]-1,height:b[1]-a[1]},style:{fill:cl[pr.dataIndex%cl.length],opacity:api.value(5)?.55:.9}},{type:'text',style:{text:CH.mob()&&api.value(1)-api.value(0)<3?'':P[pr.dataIndex].seg.replace(/（.*）/,''),x:(a[0]+b[0])/2,y:a[1]-4,align:'center',verticalAlign:'bottom',fill:V('--fg'),fontSize:10,width:Math.max(30,b[0]-a[0]),overflow:'break'}}]}},encode:{x:[0,1],y:2},data}]})
 $('#cw-poolT').innerHTML=P.map(p=>`<tr><td><b>${p.seg}</b></td><td>${p.rev}</td><td>${p.gm}%${p.est?CH.tag('估'):''}</td><td>${(p.rev*p.gm/100).toFixed(1)}</td><td class="note">${p.note} ${CH.tag(p.src)}</td></tr>`).join('')}
function drawMar(){const G=J.profit.margins,N=J.profit.names,c=CH.C('cw-cMar'),qs=[...new Set(Object.values(G).flatMap(a=>a.map(x=>x[0])))].sort(),cl={'2330':'#d9534f','3711':'#5b8def','3037':'#26a69a','2449':'#8a5cf6','3131':'#ff9900','6187':'#9a9a9a'};
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:10},itemWidth:14},grid:{left:40,right:12,top:CH.mob()?78:50,bottom:30},xAxis:{type:'category',data:qs.map(q=>q.slice(0,4)+'Q'+Math.ceil(+q.slice(5,7)/3)),axisLabel:{interval:3}},yAxis:{max:75,axisLabel:{formatter:'{value}%'},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'-':v+'%'},
  series:Object.keys(G).map(k=>({name:N[k],type:'line',showSymbol:false,connectNulls:true,lineStyle:{width:k=='3037'?3.5:2},color:cl[k],data:qs.map(q=>{const r=G[k].find(x=>x[0]==q);return r?r[2]:null})}))})}
function drawBt(){const S=J.bt.series,c=CH.C('cw-cBt'),L=(k,n,col,w)=>({name:n,type:'line',showSymbol:false,data:S[k].filter(x=>x[1]!=null).map(x=>[x[0]+'-15',Math.max(-80,Math.min(250,x[1]))]),color:col,lineStyle:{width:w}});
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:46,right:14,top:CH.mob()?70:44,bottom:56},xAxis:{type:'time'},yAxis:{name:'3M同比',axisLabel:{formatter:'{value}%'},...CH.ax()},dataZoom:[{type:'slider',height:18,bottom:8,start:35,end:100},{type:'inside'}],tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'-':(+v).toFixed(0)+'%'},
  series:[L('equip','设备三家(弘塑+辛耘+万润)','#ff9900',2.5),L('2330','台积电','#d9534f',2),L('3711','日月光投控','#5b8def',1.5),L('abf','载板三家','#26a69a',1.5)]})}
function drawXc(){const X=J.bt.xc,ks=Object.keys(X['设备→台积电']).map(Number).sort((a,b)=>a-b),c=CH.C('cw-cXc'),cl=['#ff9900','#5b8def','#26a69a'];
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:40,right:10,top:CH.mob()?56:36,bottom:34},xAxis:{data:ks,name:'k(月)',nameLocation:'middle',nameGap:22},yAxis:{min:-.3,max:.8,...CH.ax()},
  series:Object.keys(X).map((k,i)=>({name:k,type:'bar',data:ks.map(l=>X[k][l][0]),color:cl[i]}))})}
function drawCl(){const L=J.bt.cl,c=CH.C('cw-cCl');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:48,right:14,top:CH.mob()?56:40,bottom:30},xAxis:{data:L.q.map(q=>q.slice(0,4)+'Q'+Math.ceil(+q.slice(5,7)/3)),axisLabel:{interval:CH.mob()?7:3}},yAxis:{name:'亿新台币',...CH.ax()},
  tooltip:{trigger:'axis',confine:true},series:[{name:'合约负债（季末）',type:'bar',data:L.cl,itemStyle:{color:'#8a5cf6',opacity:.7}},{name:'当季营收',type:'line',data:L.rev,color:'#ff9900',symbolSize:5}]})}
function drawIf(r){const c=CH.C('cw-cIf'),ys=[2026,2027];if(!H){$('#cw-ifTxt').textContent='HBM 数据未加载';return}
 const cov=ys.map(y=>({c:r[y].s/r[y].d,cu:r[y].s/r[y].du,h:r[y].hs/r[y].hbm,h2:r[y].hs*1.08/r[y].hbm}));
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:44,right:30,top:CH.mob()?78:46,bottom:30},xAxis:{data:ys.map(String)},yAxis:{max:1.4,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(v*100).toFixed(0)+'%'},
  series:[{name:'CoWoS 供给 ÷ 可见出货所需',type:'bar',markLine:{silent:true,symbol:'none',data:[{yAxis:1}],lineStyle:{type:'dashed',color:V('--mut')},label:{formatter:'100%',color:V('--mut')}},data:cov.map(x=>+x.c.toFixed(3)),color:'#5b8def',label:{show:true,position:'top',formatter:p=>(p.value*100).toFixed(0)+'%',color:V('--fg')}},{name:'HBM 供给 ÷ CoWoS 出货所需（HBM 页基准）',type:'bar',data:cov.map(x=>+x.h.toFixed(3)),color:'#d9534f',label:{show:true,position:'top',formatter:p=>(p.value*100).toFixed(0)+'%',color:V('--fg')}},{name:'同上，HBM 供给 ×1.08（KGI 口径）',type:'bar',data:cov.map(x=>+x.h2.toFixed(3)),color:'#f0a8a6',label:{show:!CH.mob(),position:'top',formatter:p=>(p.value*100).toFixed(0)+'%',color:V('--fg')}}]});
 const x=cov[1],bind=x.h<x.c?'HBM':'CoWoS',pp=Math.abs(x.c-x.h)*100;$('#cwHHbm').textContent='约 '+(x.h*100).toFixed(0)+'%';
 $('#cw-ifTxt').innerHTML=`2027（同一口径：KGI 可见出货）：CoWoS 够 <b>${(x.c*100).toFixed(0)}%</b>，HBM 够 <b>${(x.h*100).toFixed(0)}%</b>（按 KGI 供给 +45–50% 口径 ${(x.h2*100).toFixed(0)}%）→ <b>${bind}</b> 略紧，两者只差 ${pp.toFixed(0)} 个百分点，在模型误差内。对客户需求口径，CoWoS 只够 ${(x.cu*100).toFixed(0)}%。HBM 供给直接读自 HBM 页的模型（${r[2027].hs.toFixed(2)} EB），出货所需 ${r[2027].hbm.toFixed(2)} EB。`}
function drawDrv(){CH.driver('cw-cDrv','#cw-drvT tbody',J.driver)}
function render(){if(H&&T){if(tocDraw)tocDraw();else tocDraw=TOC.render('cw','#cw-toc',J,H,T,{ledger:'#cw-tpred'})}drawDrv();drawBal();drawCap();drawMix();drawInf();drawPool();drawMar();drawBt();drawXc();drawCl();CH.net('cw-cNet','#cw-nodeInfo',J.companies,mk)}
window.redraw=render;
let T,tocDraw=null;Promise.all([fetch('data/cowos.json?v=1f83339c33').then(r=>r.json()),fetch('data/hbm.json?v=a4fc96910a').then(r=>r.json()).catch(()=>null),fetch('data/toc.json?v=4dd7367735').then(r=>r.json())]).then(([j,h,t])=>{J=j;H=h;T=t;
 $('#cw-upd').textContent=J.meta.updated;CH.stats('#cw-stats',J.judgment.stats);CH.debates('#cw-deb',J.debates);
 CH.table('#cw-varT tbody',J.variants,5);CH.table('#cw-procT tbody',J.process,3);CH.table('#cw-capT tbody',J.cap_src,5);CH.table('#cw-ppwT tbody',J.ppw,-1);
 CH.table('#cw-capexT tbody',J.profit.capex,2);CH.table('#cw-ucT tbody',J.profit.unit_cost,2);
 CH.neck('#cw-neck',J.neck);CH.timeline('#cw-tl1',J.history.tl1,'');CH.timeline('#cw-tl2',J.history.tl2,'h');$('#cw-rule').textContent=J.history.rule;
 CH.leadCards('#cw-lead',J.lead.cards);CH.table('#cw-tpT tbody',J.bt.tp,-1,false);
 const e=J.bt.series.equip.filter(x=>x[1]!=null),le=e[e.length-1];$('#cw-btNow').innerHTML=`最新：${le[0]} 设备三家 3 个月营收同比 +${le[1].toFixed(0)}%，从 2025-10 的谷底回升、仍在加速；按历史，等它见顶后约 1–13 个月（中位 4 个月）台积电营收同比见顶。拐点用 ±6 个月局部极值识别 ${CH.tag('估')}。`;
 CH.ledger('#cw-predT tbody','#cw-predSum',J.predictions);CH.falsify('#cw-falT tbody',J.falsify);CH.players('#cw-play',J.players);$('#cw-torNote').textContent=J.tornado_note;CH.coTable('#cw-coT tbody',J.companies);
 CH.table('#cw-ifT-b',J.interface.rows,3);$('#cw-formula').textContent=J.interface.formula;
 CH.sources('#cw-srcL',J.sources);CH.list('#cw-lim',J.limits);CH.table('#cw-logT tbody',J.changelog,-1);
 ['cap','os','ut','ppw','dem','hbm'].forEach(k=>document.getElementById('cw-'+k).addEventListener('input',drawBal));
 CH.segFilter('#cw-fMk',m=>{mk=m;CH.net('cw-cNet','#cw-nodeInfo',J.companies,mk)});render()});

