/* cu.js — 铜 v0.1（大宗商品系列第一篇）：模型与图表。calc() 与 cu/model.py 的 calc() 一致（改一处要同步改另一处）。
   通用组件见 chain.js；所有 DOM id 带 cu- 前缀，不依赖 window[id]。 */
(function(){let J,mk='all';const $=CH.$,V=CH.V,E=CH.tag('估'),sv=id=>+document.getElementById(id).value;
const K=['mine27','kw27','tpm','g27','us27','scrap27','cn27'],f0=v=>Math.round(v).toLocaleString('en-US'),sg=v=>(v>=0?'+':'−')+f0(Math.abs(v)),pc=v=>(v*100).toFixed(1)+'%';
const COL={bear:'#5b8def',base:'#e0a030',bull:'#d9534f',ev:'#8a5cf6'};
function P(){const o={};K.forEach(k=>o[k]=sv('cu-'+k));return o}
function calc(p){const M=J.model,I=M.ICSG,A=M.A,dc26=A['2026']*M.KW26*p.tpm,dc27=A['2027']*p.kw27*p.tpm,base26=I.use['2026']-dc26,trad27=base26*(1+p.g27/100),ref27=I.ref['2027']+p.mine27,use27=trad27+dc27+p.scrap27+p.cn27,g27=ref27-use27;
 return{dc26,dc27,ddc:dc27-dc26,trad27,dtrad:trad27-base26,ref27,use27,g27,x27:g27-p.us27,x26:I.bal['2026']-M.US26,ug:(use27/I.use['2026']-1)*100,kg27:p.kw27*p.tpm,kg26:M.KW26*p.tpm}}
function prob(){let b=sv('cu-pb')/100,u=sv('cu-pu')/100;if(b+u>1)u=1-b;return{bear:b,bull:u,base:1-b-u}}
const ax=()=>CH.ax(),fg=()=>V('--fg'),mob=()=>CH.mob();
/* ---- 要害变量：龙卷风（指标 = 2027 美国以外平衡） */
function drawTor(p){const L=[['美国 2027 净囤货',{us27:-500},{us27:1000},'回流 500','再囤 1,000','高盛基准 +400；麦格理"明确不征"→ 回流'],['矿山相对 ICSG',{mine27:0},{mine27:-600},'按 ICSG','−600','ICSG 已扣 959 千吨干扰；Escondida FY27 −13%～−21%'],
  ['每颗加速器 kW',{kw27:1.2},{kw27:2.0},'1.2 kW','2.0 kW','SemiAnalysis 51.2 GW ÷ KGI ≈ 2.0'],['数据中心吨/MW',{tpm:20},{tpm:45},'20','45','Kpler：27；AI 高密度 30–45'],['非数据中心需求增速',{g27:-1},{g27:1.5},'−1%','+1.5%','麦格理：中国 0、全球 +1.5%'],
  ['中国废铜→精铜替代',{scrap27:0},{scrap27:400},'0','+400','高盛只给价格影响（估）'],['中国国储 / 补库',{cn27:0},{cn27:300},'0','+300','协会呼吁，未落地']];
 const x=q=>calc({...p,...q}).x27,base=x({});
 CH.tornado('cu-cTor',base,L.map(a=>({n:a[0],lo:x(a[1]),hi:x(a[2]),l1:a[3],l2:a[4],src:a[5]})),{flip:0,flipLbl:'0：缺口↔过剩',fmt:v=>sg(v)});
 $('#cu-torT tbody').innerHTML=L.map(a=>`<tr><td><b>${a[0]}</b></td><td>${a[3]} → ${sg(x(a[1]))}</td><td>${a[4]} → ${sg(x(a[2]))}</td><td class="note">${a[5]}</td></tr>`).join('')}
/* ---- 平衡 */
function setOut(){const o={mine27:v=>sg(v),kw27:v=>v.toFixed(1)+' kW',tpm:v=>v+' 吨/MW',g27:v=>(v>0?'+':'')+v+'%',us27:v=>sg(v),scrap27:v=>sg(v),cn27:v=>sg(v),pb:v=>v+'%',pu:v=>v+'%'};for(const k in o)$('#cu-o-'+k).textContent=o[k](sv('cu-'+k))}
function drawBal(){setOut();const p=P(),r=calc(p),I=J.model.ICSG;
 $('#cu-g').textContent=sg(r.g27);$('#cu-x').textContent=sg(r.x27);['cu-sG','cu-sX'].forEach((id,i)=>{const e=document.getElementById(id);if(e)e.textContent=sg(i?r.x27:r.g27)});$('#cu-ug').textContent=(r.ug>0?'+':'')+r.ug.toFixed(1)+'%';
 $('#cu-balTxt').innerHTML=`2027：精炼 ${f0(r.ref27)} − 消费 ${f0(r.use27)}（其中数据中心 ${f0(r.dc27)}、每颗 ${r.kg27.toFixed(0)} kg）= 全球 <b>${sg(r.g27)}</b>；减美国净囤货 ${sg(p.us27)} → 美国以外 <b>${sg(r.x27)}</b> 千吨。消费增速 ${r.ug.toFixed(1)}%（ICSG 2.5%）。${E}`;
 const steps=[['ICSG 全球',I.bal['2027'],1],['矿山修正',p.mine27,0],['消费差（ICSG − 我们）',I.use['2027']-r.use27,0],['我们：全球',r.g27,1],['美国净囤货',-p.us27,0],['我们：美国以外',r.x27,1]];
 let run=0;const lo=[],val=[];steps.forEach(([n,v,tot])=>{if(tot){lo.push(Math.min(0,v));val.push({value:Math.abs(v),itemStyle:{color:v<0?'#d9534f':'#5b8def'},raw:v});run=v}else{const a=run,b=run+v;lo.push(Math.min(a,b));val.push({value:Math.abs(v),itemStyle:{color:v<0?'#e57373':'#66bb6a'},raw:v});run=b}});
 const c=CH.C('cu-cBal');c.setOption({...CH.base(),grid:{left:52,right:14,top:36,bottom:mob()?70:44},xAxis:{data:steps.map(s=>s[0]),axisLabel:{interval:0,fontSize:mob()?9:11,rotate:mob()?35:0,width:90,overflow:'break'}},yAxis:{name:'千吨',...ax()},
  tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},formatter:q=>{const d=q.find(x=>x.seriesIndex==1);return d?`${d.name}：${sg(d.data.raw)} 千吨`:''}},
  series:[{type:'bar',stack:'w',stackStrategy:'all',silent:true,itemStyle:{color:'transparent'},data:lo},{type:'bar',stack:'w',stackStrategy:'all',barMaxWidth:46,data:val,label:{show:true,position:'top',fontSize:10,color:fg(),formatter:q=>sg(q.data.raw)}}]});
 drawDem(r);drawSup(p);drawToc(r);drawTor(p);drawEv();drawIf(r)}
window.cuReset=()=>{const P0=J.model.P0;K.forEach(k=>document.getElementById('cu-'+k).value=P0[k]);drawBal()};
/* ---- 情景与概率 */
function drawEv(){const pr=prob(),S=J.model.SCEN,avg=s=>s.px.reduce((a,b)=>a+b,0)/4,ev=S.reduce((a,s)=>a+pr[s.k]*avg(s),0);
 $('#cu-ev').textContent=f0(ev);$('#cu-bs').textContent=f0(avg(S[1]));const k=document.getElementById('cu-kEv');if(k)k.textContent=f0(ev);
 $('#cu-evTxt').innerHTML=`熊 ${(pr.bear*100).toFixed(0)}% × ${f0(avg(S[0]))} + 基准 ${(pr.base*100).toFixed(0)}% × ${f0(avg(S[1]))} + 牛 ${(pr.bull*100).toFixed(0)}% × ${f0(avg(S[2]))} = <b>${f0(ev)}</b> 美元/吨；高盛 15,400、远期 14,405、摩根大通 13,800、麦格理 12,750。${E}`;
 $('#cu-scT tbody').innerHTML=S.map(s=>{const r=calc({...J.model.P0,...s.a});return`<tr><td><b style="color:${COL[s.k]}">${s.n}</b></td><td>${(pr[s.k]*100).toFixed(0)}%</td><td>${f0(avg(s))}<div class="note">${f0(s.lo)}–${f0(s.hi)}；季度 ${s.px.map(f0).join(' / ')}</div></td><td>${sg(r.g27)} / ${sg(r.x27)}</td><td class="note">${s.trig}</td></tr>`}).join('');
 drawPath(pr)}
function drawPath(pr){const Q=J.qa,S=J.model.SCEN,B=J.model.B,xs=Q.map(q=>q[0]+(q[2]<3?'*':'')).concat(['2027Q1','2027Q2','2027Q3','2027Q4']),n=Q.length,last=Q[n-1][1];
 const sc=s=>Array(n-1).fill(null).concat([last]).concat(s.px),evp=[0,1,2,3].map(i=>S.reduce((a,s)=>a+pr[s.k]*s.px[i],0));
 const c=CH.C('cu-cPath');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:10},itemWidth:14},grid:{left:52,right:14,top:mob()?86:52,bottom:mob()?56:34},xAxis:{type:'category',data:xs,axisLabel:{fontSize:10,interval:mob()?3:1}},
  yAxis:{min:6000,max:19000,name:'美元/吨',...ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':f0(v)},
  series:[{name:'LME 季度均价',type:'line',data:Q.map(q=>q[1]).concat([null,null,null,null]),color:fg(),lineStyle:{width:2.5},symbolSize:5,
    markArea:{silent:true,itemStyle:{color:'rgba(150,150,150,.18)'},label:{show:true,position:'insideBottomLeft',color:V('--mut'),fontSize:10,formatter:'90–95 分位全成本'},data:[[{yAxis:B.c90[0]},{yAxis:B.c90[1]}]]},
    markLine:{silent:true,symbol:'none',lineStyle:{type:'dashed',color:V('--mut')},label:{color:V('--mut'),fontSize:10,position:'insideStartTop'},data:[{yAxis:B.ubs,name:'瑞银激励价',label:{formatter:'激励价 '+f0(B.ubs)}}]}},
   ...S.map(s=>({name:s.n.split('：')[0]+' '+(pr[s.k]*100).toFixed(0)+'%',type:'line',data:sc(s),color:COL[s.k],lineStyle:{width:s.k=='base'?2.6:1.6,type:s.k=='base'?'solid':'dashed'},symbolSize:4})),
   {name:'概率加权',type:'line',data:Array(n-1).fill(null).concat([last]).concat(evp.map(v=>Math.round(v))),color:COL.ev,lineStyle:{width:2,type:'dotted'},symbol:'diamond',symbolSize:6}]})}
/* ---- 一致预期 */
function drawCons(){const C=J.cons.slice(),S=J.model.SCEN,base=S[1].px.reduce((a,b)=>a+b,0)/4,pr=prob(),ev=S.reduce((a,s)=>a+pr[s.k]*s.px.reduce((x,y)=>x+y,0)/4,0);
 const R=C.map(r=>[r[0],r[1],r[2]]).concat([['我们：基准',Math.round(base),'估'],['我们：概率加权',Math.round(ev),'估']]).sort((a,b)=>a[1]-b[1]);
 const c=CH.C('cu-cCons');c.setOption({...CH.base(),grid:{left:mob()?96:118,right:56,top:10,bottom:26},xAxis:{type:'value',min:10000,axisLabel:{formatter:v=>(v/1000)+'k'},...ax()},yAxis:{type:'category',data:R.map(r=>r[0]),axisLabel:{fontSize:mob()?10:12}},
  tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},formatter:q=>{const r=R[q[0].dataIndex];return`${r[0]}：${f0(r[1])}<br>${r[2]=='估'?'Kiko 估':r[2]}`}},
  series:[{type:'bar',data:R.map(r=>({value:r[1],itemStyle:{color:/^我们/.test(r[0])?COL.ev:'#9e9e9e'}})),label:{show:true,position:'right',fontSize:10,color:fg(),formatter:q=>f0(q.value)}}]});
 $('#cu-balvT tbody').innerHTML=J.balv.map(r=>`<tr><td><b>${r[0]}</b></td><td>${typeof r[1]=='number'?sg(r[1]):r[1]}</td><td>${CH.tag(r[2])}</td></tr>`).join('')}
/* ---- 需求 */
function drawDem(r){const I=J.model.ICSG,du=I.use['2027']-I.use['2026'],p=P(),c=CH.C('cu-cDem');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:48,right:14,top:mob()?56:40,bottom:30},xAxis:{data:['ICSG','我们']},yAxis:{name:'千吨',...ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':sg(v)},
  series:[{name:'ICSG 合计',type:'bar',stack:'s',data:[du,null],color:'#9e9e9e',barMaxWidth:60,label:{show:true,formatter:q=>q.value?sg(q.value):'',color:'#fff'}},
   {name:'AI 数据中心',type:'bar',stack:'s',data:[null,Math.round(r.ddc)],color:'#d9534f',label:{show:true,formatter:q=>q.value?sg(q.value):'',color:'#fff'}},
   {name:'非数据中心',type:'bar',stack:'s',data:[null,Math.round(r.dtrad)],color:'#5b8def',label:{show:Math.abs(r.dtrad)>60,formatter:q=>sg(q.value),color:'#fff'}},
   {name:'废铜替代 + 中国补库',type:'bar',stack:'s',data:[null,p.scrap27+p.cn27],color:'#ff9900'}]});
 const A=J.model.A,ys=['2025','2026','2027'],kw={'2025':J.model.KW26,'2026':J.model.KW26,'2027':p.kw27},dc=ys.map(y=>Math.round(A[y]*kw[y]*p.tpm)),c2=CH.C('cu-cDc');
 c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:10}},grid:{left:48,right:46,top:mob()?62:44,bottom:30},xAxis:{data:ys.concat(['2028'])},yAxis:[{name:'千吨',...ax()},{name:'kg/颗',splitLine:{show:false}}],tooltip:{trigger:'axis',confine:true},
  series:[{name:'我们（KGI × kW × 吨/MW）',type:'bar',data:dc.concat([null]),color:'#d9534f',barMaxWidth:36,label:{show:true,position:'top',fontSize:10,color:fg()}},
   {name:'BNEF（年均 400，2028 峰值 572）',type:'scatter',data:[[0,400],[1,400],[2,400],[3,572]],color:'#5b8def',symbolSize:9},
   {name:'Kpler 2026（405–540）',type:'scatter',data:[[1,405],[1,540]],color:'#26a69a',symbol:'triangle',symbolSize:10},
   {name:'每颗加速器 kg（估）',type:'line',yAxisIndex:1,data:ys.map(y=>+(kw[y]*p.tpm).toFixed(1)).concat([null]),color:'#ff9900',label:{show:true,formatter:q=>q.value?q.value+'kg':'',fontSize:10,color:fg()}}]})}
/* ---- 供给 */
function drawSup(p){const I=J.model.ICSG,g=(a,b)=>+((a/b-1)*100).toFixed(2),c=CH.C('cu-cSup'),ys=['2025','2026','2027'];
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:10}},grid:{left:40,right:14,top:mob()?62:44,bottom:30},xAxis:{data:['2026','2027']},yAxis:{axisLabel:{formatter:'{value}%'},...ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':v+'%'},
  series:[{name:'矿山（ICSG 调整后）',type:'bar',data:[g(I.mine['2026'],I.mine['2025']),g(I.mine['2027'],I.mine['2026'])],color:'#9e9e9e'},{name:'矿山（ICSG 未调整）',type:'bar',data:[g(I.mine_u['2026'],I.mine_u['2025']),g(I.mine_u['2027'],I.mine_u['2026'])],color:'#cfd8dc'},
   {name:'精炼（ICSG 调整后）',type:'bar',data:[g(I.ref['2026'],I.ref['2025']),g(I.ref['2027'],I.ref['2026'])],color:'#5b8def'},{name:'精炼（我们）',type:'bar',data:[g(I.ref['2026'],I.ref['2025']),g(I.ref['2027']+p.mine27,I.ref['2026'])],color:'#d9534f'},
   {name:'2026 年 1–7 月实际矿产',type:'scatter',data:[[0,-0.8]],symbol:'diamond',symbolSize:12,color:'#ff9900'}]});
 const M=[['Grasberg',181,'#d9534f'],['Kamoa-Kakula',100,'#d9534f'],['智利（Cochilco）',280,'#5b8def'],['Escondida（含在智利）',-210,'#9e9e9e'],['我们的矿山修正',p.mine27,'#8a5cf6']],c2=CH.C('cu-cMine');
 c2.setOption({...CH.base(),grid:{left:mob()?112:140,right:46,top:10,bottom:26},xAxis:{type:'value',...ax()},yAxis:{type:'category',data:M.map(m=>m[0]).reverse(),axisLabel:{fontSize:mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},valueFormatter:v=>sg(v)+' 千吨'},
  series:[{type:'bar',data:M.slice().reverse().map(m=>({value:m[1],itemStyle:{color:m[2]}})),label:{show:true,position:'right',fontSize:10,color:fg(),formatter:q=>sg(q.value)}}]})}
/* ---- TOC */
function drawToc(r){const T=J.toc,I=J.model.ICSG,t27={conc:r.ref27/I.ref_u['2027'],ref:r.ref27/r.use27,exus:(r.use27+r.x27)/r.use27},cat=['精矿 ÷ 冶炼想做的','精炼 ÷ 消费（全球）','精炼 ÷ 消费（美国以外）'],ks=['conc','ref','exus'],c=CH.C('cu-cToc');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:44,right:14,top:mob()?50:36,bottom:mob()?60:34},xAxis:{data:cat,axisLabel:{interval:0,fontSize:mob()?9:11,width:mob()?80:140,overflow:'break'}},yAxis:{min:.9,max:1.02,interval:.02,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>pc(v)},
  series:[{name:'2026',type:'bar',data:ks.map(k=>+T['2026'][k].toFixed(4)),color:'#8fa8d8',barMaxWidth:28,label:{show:!mob(),position:'top',fontSize:10,color:fg(),formatter:q=>pc(q.value)}},{name:'2027（我们）',type:'bar',color:'#e0a030',data:ks.map(k=>+t27[k].toFixed(4)),barMaxWidth:28,itemStyle:{color:q=>q.dataIndex==0?'#d9534f':'#e0a030'},label:{show:true,position:'top',fontSize:10,color:fg(),formatter:q=>pc(q.value)},
   markLine:{silent:true,symbol:'none',data:[{yAxis:1}],lineStyle:{type:'dashed',color:V('--mut')},label:{formatter:'100%',color:V('--mut')}}}]})}
function drawTc(){const T=J.tc,c=CH.C('cu-cTc'),xs=T.map(t=>String(t[0])).concat(['2026 现货','2027 Pelambres']);
 c.setOption({...CH.base(),grid:{left:44,right:mob()?6:14,top:36,bottom:mob()?48:30},xAxis:{data:xs,axisLabel:{fontSize:mob()?8:9,lineHeight:12,interval:0,formatter:v=>v=='2026 现货'?'26\n现货':v=='2027 Pelambres'?'27\n长单':"'"+v.slice(2)}},yAxis:{name:'美元/吨',...ax()},tooltip:{trigger:'axis',confine:true},
  series:[{type:'bar',barMaxWidth:26,data:T.map(t=>({value:t[1],itemStyle:{color:'#5b8def'}})).concat([{value:-272.2,itemStyle:{color:'#d9534f'}},{value:-330,itemStyle:{color:'#d9534f',opacity:.6}}]),label:{show:!mob(),position:'top',fontSize:10,color:fg()},
   markLine:{silent:true,symbol:'none',data:[{yAxis:-75,name:'CRU 2027Q4'}],lineStyle:{type:'dashed',color:'#26a69a'},label:{formatter:'CRU：2027Q4 现货 −75',color:'#26a69a',fontSize:10,position:'insideStartTop'}}}]})}
/* ---- 利润：价格档位 */
function drawBand(){const B=J.model.B,R=[['Kamoa C1（2027）',B.kk_c1],['90–95 分位全成本',B.c90],['麦格理长期',[10500,10500]],['伍德麦肯兹激励价',[B.wm,B.wm]],['RBC：NAV 隐含',[B.nav,B.nav]],['瑞银长期激励价',[B.ubs,B.ubs]],['LME 现货（10 月均）',[J.bt.now.cash,J.bt.now.cash]],['高盛 2027',[15400,15400]]],c=CH.C('cu-cBand');
 c.setOption({...CH.base(),grid:{left:mob()?112:140,right:56,top:10,bottom:26},xAxis:{type:'value',min:0,axisLabel:{formatter:v=>(v/1000)+'k'},...ax()},yAxis:{type:'category',data:R.map(r=>r[0]),axisLabel:{fontSize:mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},formatter:q=>{const r=R[q[0].dataIndex];return`${r[0]}：${r[1][0]==r[1][1]?f0(r[1][0]):f0(r[1][0])+'–'+f0(r[1][1])}`}},
  series:[{type:'bar',stack:'b',stackStrategy:'all',silent:true,itemStyle:{color:'transparent'},data:R.map(r=>r[1][0]==r[1][1]?0:r[1][0])},{type:'bar',stack:'b',stackStrategy:'all',data:R.map((r,i)=>({value:r[1][0]==r[1][1]?r[1][0]:r[1][1]-r[1][0],itemStyle:{color:i<2?'#9e9e9e':i<6?'#5b8def':i==6?'#d9534f':'#e0a030'}})),label:{show:true,position:'right',fontSize:10,color:fg(),formatter:q=>{const r=R[q.dataIndex];return r[1][0]==r[1][1]?f0(r[1][0]):f0(r[1][0])+'–'+f0(r[1][1])}}}]})}
/* ---- 历史 */
function drawLong(){const L=J.bt.long,B=J.model.B,c=CH.C('cu-cLong');
 c.setOption({...CH.base(),grid:{left:52,right:14,top:36,bottom:56},xAxis:{type:'time'},yAxis:{name:'2026 年美元/吨',...ax()},dataZoom:[{type:'slider',height:18,bottom:8},{type:'inside'}],tooltip:{trigger:'axis',confine:true,valueFormatter:v=>f0(v)},
  series:[{type:'line',showSymbol:false,data:L.map(x=>[x[0]+'-15',x[1]]),color:'#d9534f',lineStyle:{width:1.8},markArea:{silent:true,itemStyle:{color:'rgba(150,150,150,.18)'},data:[[{yAxis:B.c90[0]},{yAxis:B.c90[1]}]]},
   markLine:{silent:true,symbol:'none',lineStyle:{type:'dashed',color:V('--mut')},label:{color:V('--mut'),fontSize:10,position:'insideStartTop'},data:[{yAxis:B.ubs,label:{formatter:'激励价（今天）'}}]}}]});
 $('#cu-rule').textContent=J.history.rule;CH.timeline('#cu-tl1',J.history.tl1,'');CH.timeline('#cu-tl2',J.history.tl2,'h')}
/* ---- 回测 */
function drawLead(){const b=J.bt,sh=(m,k)=>{const d=new Date(m+'-15');d.setMonth(d.getMonth()+k);return d.toISOString().slice(0,10)},c=CH.C('cu-cCi');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:44,right:44,top:mob()?56:40,bottom:30},xAxis:{type:'time'},yAxis:[{name:'铜价同比 %',...ax()},{name:'脉冲 %GDP',splitLine:{show:false}}],tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':(+v).toFixed(1)},
  series:[{name:'铜价同比',type:'line',showSymbol:false,data:b.yoy.map(x=>[x[0]+'-15',x[1]]),color:'#d9534f',lineStyle:{width:1.8}},{name:'信贷脉冲（右移 '+b.kbest+' 个月）',type:'line',yAxisIndex:1,showSymbol:false,data:b.imp.map(x=>[sh(x[0],b.kbest),x[1]]),color:'#5b8def',lineStyle:{width:2.2}}]});
 const S=b.series,c2=CH.C('cu-cInv'),pt=x=>[x[4],x[2],x[0]];
 c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:52,right:14,top:36,bottom:40},xAxis:{type:'log',min:0.5,max:20,name:'库存天数',nameLocation:'middle',nameGap:24,...ax()},yAxis:{type:'value',name:'实际价格',min:4000,...ax()},tooltip:{trigger:'item',confine:true,formatter:q=>`${q.data[2]}<br>库存 ${q.data[0]} 天 · 实际价格 ${f0(q.data[1])}`},
  series:[{name:'2008–2018（拟合）',type:'scatter',symbolSize:5,data:S.filter(x=>x[0]<='2018-12').map(pt),color:'#5b8def'},{name:'2019–2026（检验）',type:'scatter',symbolSize:5,data:S.filter(x=>x[0]>'2018-12').map(pt),color:'#d9534f'}]});
 const c3=CH.C('cu-cSpr');c3.setOption({...CH.base(),grid:{left:44,right:14,top:20,bottom:30},xAxis:{type:'time'},yAxis:{axisLabel:{formatter:'{value}%'},...ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(+v).toFixed(1)+'%'},
  series:[{type:'bar',data:b.spread.map(x=>[x[0]+'-15',x[1]]),itemStyle:{color:q=>q.value[1]>=0?'#d9534f':'#5b8def'},barMaxWidth:4}]});
 const M=b.macro,c4=CH.C('cu-cMac');c4.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:52,right:40,top:mob()?50:36,bottom:30},xAxis:{type:'time'},yAxis:[{name:'实际铜价',...ax()},{name:'TIPS %',nameLocation:'start',inverse:true,splitLine:{show:false}}],tooltip:{trigger:'axis',confine:true},
  series:[{name:'实际铜价（左）',type:'line',showSymbol:false,data:S.map(x=>[x[0]+'-15',x[2]]),color:'#d9534f'},{name:'10 年 TIPS（右，反向）',type:'line',yAxisIndex:1,showSymbol:false,data:M.filter(x=>x[1]!=null).map(x=>[x[0]+'-15',x[1]]),color:'#5b8def'}]});
 CH.leadCards('#cu-lead',J.lead)}
/* ---- 中国 */
function drawCn(){const D=J.cn.dem,c=CH.C('cu-cnDem');
 c.setOption({...CH.base(),grid:{left:mob()?112:140,right:46,top:10,bottom:26},xAxis:{type:'value',axisLabel:{formatter:'{value}%'},...ax()},yAxis:{type:'category',data:D.map(d=>d[0]).reverse(),axisLabel:{fontSize:mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},formatter:q=>{const d=D[D.length-1-q[0].dataIndex];return`${d[0]}（${d[2]}）：${d[1]>0?'+':''}${d[1]}%`}},
  series:[{type:'bar',data:D.slice().reverse().map(d=>({value:d[1],itemStyle:{color:d[1]>=0?'#26a69a':'#d9534f'}})),label:{show:true,position:'right',fontSize:10,color:fg(),formatter:q=>(q.value>0?'+':'')+q.value+'%'}}]});
 $('#cu-cnDemT tbody').innerHTML=D.map(d=>`<tr><td><b>${d[0]}</b></td><td>${d[1]>0?'+':''}${d[1]}%</td><td>${d[2]}</td><td>${CH.tag(d[3])}</td></tr>`).join('');
 const use25=J.model.ICSG.use['2025']*0.59,t=CH.C('cu-cnToc'),v=[['精矿自给（矿产 ÷ 精炼）',1.8/14.0],['精炼自给（精炼 ÷ 消费）',14000/use25]];
 t.setOption({...CH.base(),grid:{left:mob()?130:170,right:50,top:28,bottom:26},xAxis:{type:'value',min:0,max:1.1,interval:mob()?.5:.25,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...ax()},yAxis:{type:'category',data:v.map(x=>x[0]),axisLabel:{fontSize:mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},valueFormatter:v=>pc(v)},
  series:[{type:'bar',barMaxWidth:30,data:v.map((x,i)=>({value:+x[1].toFixed(3),itemStyle:{color:i?'#e0a030':'#d9534f'}})),label:{show:true,position:'right',color:fg(),formatter:q=>pc(q.value)},markLine:{silent:true,symbol:'none',data:[{xAxis:1}],lineStyle:{type:'dashed',color:V('--acc')},label:{formatter:'100%',color:V('--acc')}}}]});
 const co=CH.C('cu-cnCo');co.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg(),fontSize:11}},grid:{left:44,right:14,top:36,bottom:30},xAxis:{data:['紫金矿业','洛阳钼业']},yAxis:{name:'万吨',...ax()},tooltip:{trigger:'axis',confine:true},
  series:[{name:'2026（规划 / 指引中值）',type:'bar',data:[120,79],color:'#5b8def',barMaxWidth:36,label:{show:true,position:'top',color:fg()}},{name:'2028（紫金规划中值）',type:'bar',data:[155,null],color:'#d9534f',barMaxWidth:36,label:{show:true,position:'top',color:fg(),formatter:q=>q.value??''}}]});
 const N=J.cn,R=(sel,rows,fn)=>$(sel).innerHTML=rows.map(fn).join('');
 R('#cu-cnSupT tbody',N.sup,r=>`<tr><td><b>${r[0]}</b></td><td>${CH.srcInline(r[1])}</td><td>${CH.tag(r[2])}</td></tr>`);R('#cu-cnBalT tbody',N.bal,r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${CH.tag(r[2])}</td></tr>`);
 R('#cu-cnCoT tbody',N.co,c=>`<tr><td>${c[0]}</td><td><b>${c[1]}</b></td><td style="white-space:nowrap">${c[2]}</td><td>${c[3]}</td><td><span class="pill" style="color:${/^强/.test(c[4])?'var(--ok)':/^中/.test(c[4])?'var(--warn)':'var(--mut)'}">${c[4]}</span></td><td>${CH.tag(c[5])}</td></tr>`);
 CH.players('#cu-cnPl',N.players);CH.falsify('#cu-cnFalT tbody',N.falsify);CH.ledger('#cu-cnPredT tbody','#cu-cnPredS',N.preds)}
function drawIf(r){$('#cu-ifT').innerHTML=J.interface.rows.map(x=>`<tr><td><b>${x[0]}</b></td><td>${x[1]}</td><td>${x[2]}</td><td>${CH.srcInline(x[3])}</td></tr>`).join('')}
window.cuNet=()=>CH.net('cu-cNet','#cu-nodeInfo',J.companies,mk);
function render(){drawBal();drawCons();drawTc();drawBand();drawLong();drawLead();drawCn();window.cuNet()}
window.redraw=render;
fetch('data/cu.json?v=7a5bc35e3a').then(r=>r.json()).then(j=>{J=j;
 $('#cu-upd').textContent=J.meta.updated;CH.stats('#cu-stats',J.stats);
 $('#cu-deb').innerHTML=J.debates.map(x=>`<div class="card"><b>${x.q}</b><p style="margin:.4em 0;font-size:15px">观点：${CH.srcInline(x.view)}</p><div class="note">证伪：${x.falsify}</div></div>`).join('');
 CH.table('#cu-procT tbody',J.process,2);CH.table('#cu-prT tbody',J.price,2);
 $('#cu-mineT tbody').innerHTML=J.mines.map(m=>`<tr><td><b>${m[0]}</b></td><td>${m[1]}</td><td>${m[2]}</td><td>${m[3]}</td><td><b>${m[4]}</b></td><td>${CH.tag(m[5])}</td></tr>`).join('');
 CH.neck('#cu-neck',J.neck);CH.players('#cu-play',J.players);CH.ledger('#cu-predT tbody','#cu-predSum',J.predictions);CH.falsify('#cu-falT tbody',J.falsify);CH.coTable('#cu-coT tbody',J.companies);
 $('#cu-formula').textContent=J.interface.formula;CH.sources('#cu-srcL',J.sources);CH.list('#cu-lim',J.limits);CH.table('#cu-logT tbody',J.changelog,-1);
 K.forEach(k=>document.getElementById('cu-'+k).addEventListener('input',drawBal));['cu-pb','cu-pu'].forEach(id=>document.getElementById(id).addEventListener('input',()=>{setOut();drawEv();drawCons()}));
 CH.segFilter('#cu-fMk',m=>{mk=m;window.cuNet()});render()});
})();
