/* chain.js — 产业链小链页面的通用组件（schema chain/v1）。HBM v0.2 仍用 hbm.js；新链用本文件 + <chain>.js。
   约定：所有 DOM id 带链前缀（如 cw-），不依赖 window[id] 全局变量（HBM 踩过的坑）。 */
const CH={charts:{}};
CH.$=s=>document.querySelector(s);
CH.V=c=>getComputedStyle(document.documentElement).getPropertyValue(c).trim();
CH.mob=()=>innerWidth<700;
CH.base=()=>({textStyle:{fontFamily:'-apple-system,PingFang SC,sans-serif',color:CH.V('--fg')},backgroundColor:'transparent',tooltip:{trigger:'axis',confine:true},grid:{left:44,right:14,top:40,bottom:30}});
CH.ax=()=>({splitLine:{lineStyle:{color:CH.V('--line')}}});
CH.C=id=>{if(CH.charts[id])CH.charts[id].dispose();const el=document.getElementById(id);CH.charts[id]=echarts.init(el,null,{renderer:'svg'});return CH.charts[id]};
CH.esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
/* 来源标签：'12' / '1,3' → 源 tag；'估' → 估 tag；'—' → 空 */
CH.tag=x=>{x=String(x??'');if(!x||x=='—')return'';if(x=='估')return'<span class="tag t-est">估</span>';
 if(/^[\d,]+$/.test(x))return'<span class="tag t-src">'+x.split(',').map(s=>`<a href="#src${s}">源${s}</a>`).join(' ')+'</span>';
 return`<span class="tag t-src">${CH.esc(x)}</span>`};
CH.srcInline=t=>String(t).replace(/\[源([\d,]+)\]/g,(m,a)=>CH.tag(a));
CH.stats=(el,st)=>{CH.$(el).innerHTML=st.map(s=>`<div class="card stat"><div class="n"${s.id?` id="${s.id}"`:''}${s.id?' style="color:var(--acc)"':''}>${s.n}</div><div class="l">${s.l} ${s.tag=='估'?CH.tag('估'):CH.tag(String(s.tag).replace('源',''))}</div></div>`).join('')};
CH.debates=(el,d)=>{CH.$(el).innerHTML=d.map(x=>`<div class="card"><b>${x.q}</b><p style="margin:.4em 0;font-size:15px">观点：${x.view}</p><div class="note">证伪：${x.falsify}</div></div>`).join('')};
/* rows: 数组的数组；srcCol: 哪一列是来源编号 */
CH.table=(el,rows,srcCol=-1,bold0=true)=>{CH.$(el).innerHTML=rows.map(r=>'<tr>'+r.map((c,i)=>`<td>${i==srcCol?CH.tag(c):i==0&&bold0?'<b>'+c+'</b>':CH.srcInline(c)}</td>`).join('')+'</tr>').join('')};
CH.neck=(el,N)=>{const mx=Math.max(...N.map(n=>n.months));CH.$(el).innerHTML=N.map((n,i)=>`<div class="card"><div style="display:flex;justify-content:space-between;gap:8px"><b>${i+1}. ${n.name}</b><span class="pill">${n.verdict}</span></div><div class="note" style="margin:4px 0 8px">${n.now} ${CH.tag(n.src)}</div><div class="bar"><i style="width:${n.months/mx*100}%"></i></div><div class="note">缓解约需 ${n.months>=36?'3 年左右':n.months+' 个月'}（示意）</div></div>`).join('')};
CH.timeline=(el,a,cls)=>{CH.$(el).innerHTML=a.map(x=>`<div class="${cls||''}"><span class="y">${x[0]}</span>　${x[1]} ${CH.tag(x[2])}</div>`).join('')};
CH.leadCards=(el,a)=>{CH.$(el).innerHTML=a.map(l=>`<div class="card"><b>${l[0]}</b><div class="note">${l[1]} · ${l[2]}</div><p style="margin:.5em 0 0;font-size:15px">${l[3]} ${CH.tag(l[4])}</p></div>`).join('')};
/* 预测台账：status = pending | hit | miss | void；到期自动变成"待打分" */
CH.ledger=(tb,sumEl,P,today=new Date())=>{const st={hit:['命中','var(--ok)'],miss:['未中','var(--acc)'],void:['作废','var(--mut)']};let due=0,hit=0,miss=0;
 CH.$(tb).innerHTML=P.map(p=>{const d=Math.ceil((new Date(p.due)-today)/864e5);let s;if(st[p.status]){s=st[p.status];if(p.status=='hit')hit++;if(p.status=='miss')miss++}else if(d<=0){s=['待打分','var(--warn)'];due++}else s=['待验证','var(--mut)'];
  return`<tr><td>${p.id}</td><td>${p.text}${p.note?`<div class="note">${p.note}</div>`:''}</td><td style="white-space:nowrap">${p.due}<div class="note">${d>0?d+' 天后':'已到期'}</div></td><td>${p.check}</td><td><span class="pill" style="color:${s[1]}">${s[0]}</span></td></tr>`}).join('');
 const sc=hit+miss;CH.$(sumEl).innerHTML=`共 ${P.length} 条 · 已打分 ${sc} 条${sc?` · 命中率 ${(hit/sc*100).toFixed(0)}%`:''} · 待打分 ${due} 条。规则：到期后按"验证来源"的公开数据判定命中/未中，不改原文，只追加结果。`};
CH.sources=(el,S)=>{CH.$(el).innerHTML=S.map(s=>`<li id="src${s.id}" value="${s.id}">${s.t} <a href="${s.u}" target="_blank" rel="noopener">${s.u}</a></li>`).join('')};
CH.list=(el,a)=>{CH.$(el).innerHTML=a.map(x=>`<li>${x}</li>`).join('')};
/* 公司图谱：co=[名,代码,市场,环节idx,角色,大小]，links=[a,b,关系,来源,sup|ord|cap] */
CH.net=(id,infoEl,G,mk)=>{const dk=isDark(),SEG=G.seg,cols=['#d9534f','#ff9900','#5b8def','#26a69a','#8a5cf6','#9e9e9e','#76b900','#c0ca33'];const mob=CH.mob();
 const vis=G.co.filter(c=>mk=='all'||c[2]==mk||c[3]==SEG.length-1),names=new Set(vis.map(c=>c[0]));
 const nodes=SEG.map((s,i)=>({name:s,category:i,symbolSize:mob?22:32,symbol:'roundRect',label:{show:!mob,fontWeight:'bold',fontSize:11},seg:1})).concat(vis.map(c=>({name:c[0],category:c[3],symbolSize:mob?Math.max(8,c[5]*.7):c[5],label:{show:true,fontSize:mob?9:11},co:c})));
 if(mob){const half=Math.ceil(SEG.length/2),P=SEG.map((s,i)=>[i<half?-.45:.45,(i<half?i:i-half)*1.0]);
  nodes.forEach(n=>{if(n.seg){[n.x,n.y]=P[n.category];return}const sib=nodes.filter(m=>!m.seg&&m.category==n.category),k=sib.indexOf(n),N=sib.length,sd=P[n.category][0]<0?-1:1;
   n.x=P[n.category][0]+sd*(.30+(k%2)*.16);n.y=P[n.category][1]+(N>1?(-.42+.84*k/(N-1)):0);n.label.position=sd>0?'right':'left';if(n.name.length>6)n.label.formatter=n.co[1]});
  const el=document.getElementById(id),vw=el.clientWidth-150,vh=el.clientHeight-110,xs=nodes.map(n=>n.x),ys=nodes.map(n=>n.y),wx=Math.max(...xs)-Math.min(...xs),wy=Math.max(...ys)-Math.min(...ys)||1,k=(vh/vw)*wx/wy;nodes.forEach(n=>n.y*=k)}
 const links=vis.map(c=>({source:SEG[c[3]],target:c[0],lineStyle:{color:dk?'#444':'#ccc',type:'dashed'},rel:'业务归属（环节内公司，占比多未披露）',src:'—'}))
 .concat(G.links.filter(l=>l[1]!='—'&&names.has(l[0])&&names.has(l[1])).map(l=>({source:l[0],target:l[1],rel:l[2],src:l[3],lineStyle:{width:2.2,color:{cap:'#8a5cf6',ord:'#ff9900',sup:'#2e8b57'}[l[4]],curveness:.2},label:{show:!mob,formatter:l[2].slice(0,12),fontSize:10,color:CH.V('--mut')}})));
 const c=CH.C(id);c.setOption({backgroundColor:'transparent',tooltip:{confine:true,formatter:p=>p.dataType=='edge'?`${p.data.source} → ${p.data.target}<br>${p.data.rel}<br>来源：${p.data.src}`:p.data.co?`${p.name} ${p.data.co[1]}<br>${p.data.co[4]}`:p.name},
  legend:{data:SEG,top:0,textStyle:{color:CH.V('--fg'),fontSize:mob?10:11},itemWidth:10,itemHeight:10,itemGap:mob?6:10},
  series:[{type:'graph',layout:mob?'none':'force',nodeScaleRatio:mob?0:.6,roam:true,draggable:true,top:80,bottom:mob?30:20,left:mob?75:10,right:mob?75:10,scaleLimit:{min:.4,max:3},force:{repulsion:210,edgeLength:[40,110],gravity:.2,friction:.2},categories:SEG.map((s,i)=>({name:s,itemStyle:{color:cols[i%cols.length]}})),
  label:{color:CH.V('--fg'),fontSize:11,position:'right'},edgeSymbol:['none','arrow'],edgeSymbolSize:6,data:nodes,links}]});
 c.off('click');c.on('click',p=>{if(p.dataType!='node')return;const n=p.name,co=G.co.find(x=>x[0]==n),rel=G.links.filter(l=>l[0]==n||l[1]==n);
  CH.$(infoEl).innerHTML=`<b>${n}</b> ${co?`<span class="pill">${co[1]}</span><div class="note">${SEG[co[3]]} · ${CH.srcInline(co[4])}</div>`:'<div class="note">环节</div>'}`+(rel.length?'<table style="margin-top:8px">'+rel.map(l=>`<tr><td>${l[0]} → ${l[1]=='—'?'':l[1]}</td><td>${l[2]}</td><td>${CH.tag(l[3])}</td></tr>`).join('')+'</table>':'')})};
CH.coTable=(el,G)=>{CH.$(el).innerHTML=G.co.map(c=>`<tr><td>${c[0]}</td><td style="white-space:nowrap">${c[1]}</td><td>${G.seg[c[3]]}</td><td>${CH.srcInline(c[4])}</td></tr>`).join('')};
CH.segFilter=(el,cb)=>document.querySelectorAll(el+' button').forEach(b=>b.onclick=()=>{document.querySelectorAll(el+' button').forEach(x=>x.classList.remove('on'));b.classList.add('on');cb(b.dataset.m)});
CH.scrollspy=()=>{const secs=[...document.querySelectorAll('main section')],na=[...document.querySelectorAll('#nav a')];
 addEventListener('scroll',()=>{let k=0;secs.forEach((s,i)=>{if(s.getBoundingClientRect().top<140)k=i});na.forEach(a=>a.classList.toggle('on',a.getAttribute('href')=='#'+secs[k].id));const on=na.find(a=>a.classList.contains('on'));if(on)on.scrollIntoView({block:'nearest',inline:'center'})},{passive:true})};
addEventListener('resize',()=>Object.values(CH.charts).forEach(c=>c.resize()));
/* 要害变量：龙卷风图。rows=[{n, lo, hi, l1, l2}]，lo/hi 为把该变量调到低/高端时的指标值；base 为基准值；flip 为结论翻转线（指标值） */
CH.tornado=(id,base,rows,o={})=>{const R=rows.map(r=>({...r,rg:Math.abs(r.hi-r.lo)})).sort((a,b)=>a.rg-b.rg),f=o.fmt||(v=>(v>0?'+':'')+(v*100).toFixed(0)+'%'),mob=CH.mob();
 const c=CH.C(id),mk=o.flip!=null?{silent:true,symbol:'none',data:[{xAxis:+(o.flip-base).toFixed(4)}],lineStyle:{color:CH.V('--acc'),type:'dashed',width:1.5},label:{formatter:o.flipLbl||'结论翻转',color:CH.V('--acc'),fontSize:10,position:'end'}}:null;
 c.setOption({...CH.base(),grid:{left:mob?112:150,right:mob?22:60,top:34,bottom:26},legend:{top:0,textStyle:{color:CH.V('--fg'),fontSize:11},data:['变量取低端','变量取高端']},
  tooltip:{trigger:'axis',axisPointer:{type:'shadow'},confine:true,formatter:p=>{const r=R[p[0].dataIndex];return`<b>${r.n}</b><br>基准：${f(base)}<br>${r.l1} → ${f(r.lo)}<br>${r.l2} → ${f(r.hi)}${r.src?'<br><span style="opacity:.7">区间依据：'+r.src+'</span>':''}`}},
  xAxis:{type:'value',min:v=>v.min-(mob?0:(v.max-v.min)*.25),max:v=>v.max+(mob?0:(v.max-v.min)*.25),axisLabel:{formatter:v=>f(base+v),hideOverlap:true},...CH.ax()},yAxis:{type:'category',data:R.map(r=>r.n),axisLabel:{fontSize:mob?10:12,width:mob?104:140,overflow:'break'}},
  series:[{name:'变量取低端',type:'bar',barGap:'-100%',barWidth:'55%',data:R.map(r=>+(r.lo-base).toFixed(4)),itemStyle:{color:'#5b8def'},label:{show:!mob,position:'outside',formatter:p=>R[p.dataIndex].l1,fontSize:10,color:CH.V('--mut')},markLine:mk},
   {name:'变量取高端',type:'bar',barWidth:'55%',data:R.map(r=>+(r.hi-base).toFixed(4)),itemStyle:{color:'#d9534f'},label:{show:!mob,position:'outside',formatter:p=>R[p.dataIndex].l2,fontSize:10,color:CH.V('--mut')}}]})};
/* 关键玩家与博弈：[{who, role, incentive, now, history, signal, src}] */
CH.players=(el,P)=>{CH.$(el).innerHTML=P.map(p=>`<div class="card"><div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline"><b>${p.who}</b><span class="pill">${p.role}</span></div>
 <div class="note" style="margin-top:6px"><b>动机</b>　${CH.srcInline(p.incentive)}</div><div class="note"><b>现在在做</b>　${CH.srcInline(p.now)}</div><div class="note"><b>历史上周期里怎么做</b>　${CH.srcInline(p.history)}</div>
 <div class="note" style="color:var(--fg)"><b>行为改变的信号</b>　${CH.srcInline(p.signal)}</div></div>`).join('')};
/* 反方证据/证伪条件：[{j, counter, falsify, ind, th, now, st}]，st = ok | watch | hit */
CH.falsify=(tb,F)=>{const S={ok:['未触发','var(--ok)'],watch:['需盯紧','var(--warn)'],hit:['已触发','var(--acc)']};CH.$(tb).innerHTML=F.map(x=>{const s=S[x.st]||S.ok;return`<tr><td><b>${x.j}</b></td><td>${CH.srcInline(x.counter)}</td><td>${CH.srcInline(x.falsify)}</td><td>${CH.srcInline(x.ind)}<div class="note">阈值：${x.th}</div></td><td>${CH.srcInline(x.now)}</td><td><span class="pill" style="color:${s[1]}">${s[0]}</span></td></tr>`}).join('')};
