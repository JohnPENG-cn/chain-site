/* pcb.js — PCB 小链 v0.2（行业版；v0.1 冻结为 pcb_v1.js）：模型与图表。公式与 pcb/model.py 的 calc() / cnbal() 一致（改一处要同步改另一处）。
   通用组件见 chain.js；所有 DOM id 带 pcb- 前缀，不依赖 window[id]。 */
(function(){let J,yr='2027',mk='all';const $=CH.$,V=CH.V,Y=['2025','2026','2027'],E=CH.tag('估');
const NM={cu:'HVLP3+ 铜箔（预测）',gf:'二代布',ccl:'覆铜板',dr:'钻针',abf:'ABF 载板',hbm:'HBM',cw:'CoWoS'},PC=['cu','gf','ccl','dr'];
const pct=v=>v==null?'—':(v*100).toFixed(0)+'%',sv=id=>+document.getElementById(id).value;
const S0={dem:100,g27:50,cn:150,gf:80,mix:115,dr:100,abf:27.5,s:0};
function P(){return{dem:sv('pcb-dem')/100,g26:J.model.P0.g26,g27:sv('pcb-g27')/100,cn:sv('pcb-cn'),gf26:J.model.P0.gf26,gf27:sv('pcb-gf')/100,mix:sv('pcb-mix')/100,dr:sv('pcb-dr')/100,s:sv('pcb-s')/100,abf:sv('pcb-abf')/100}}
function calc(p){const m=J.model,X=J.X,CU=m.CU,ccl27=J.model.CCLg*p.mix/(m.sh[1]/m.sh[0]),out={};
 for(const y of Y){const k=y=='2027'?p.dem:1,r={};
  r.cu={'2025':CU.s25/CU.d25,'2026':1/(1+p.g26),'2027':1/(1+p.g27)+p.cn/CU.d27}[y]/k;
  r.gf={'2025':null,'2026':p.gf26,'2027':p.gf27}[y];if(r.gf!=null)r.gf/=k;
  r.ccl={'2025':null,'2026':1,'2027':ccl27}[y];if(r.ccl!=null)r.ccl/=k;
  r.dr=m.DR[y][0]/m.DR[y][1]*(y=='2027'?p.dr:1)/k;
  for(const q of['cu','gf','ccl'])if(r[q]!=null&&r[q]<1)r[q]=r[q]+(1-r[q])*p.s;
  r.abf=X.abf[y]*(y=='2027'?(1+p.abf)/(1+X.abf_g27):1)/k;
  if(X.hbm[y]!=null)r.hbm=X.hbm[y]/k;if(X.cwlo[y]!=null){r.cwlo=X.cwlo[y]/k;r.cwhi=X.cwhi[y]/k}
  const pc=PC.filter(q=>r[q]!=null);r.pbind=pc.reduce((a,b)=>r[a]<=r[b]?a:b);r.pmin=r[r.pbind];out[y]=r}
 return out}
/* ---- 要害变量 */
function drawTor(){const b=P(),f=q=>calc(q)['2027'].pmin,g=q=>{const r=calc(q)['2027'];return r.pmin-r.abf},w=o=>({...b,...o});
 const L=[['HVLP3+ 缺口（高盛 2026–28 区间，本页分配）',{g27:.45},{g27:.55},'45%','55%','工商时报转述高盛 45–55%'],['大陆 HVLP4 增量',{cn:0},{cn:300},'0 吨/月','300 吨/月','德福 8 月 HVLP4 约 70 吨；估'],['AI 加速器需求',{dem:b.dem*1.1},{dem:b.dem*.9},'+10%','−10%','KGI 与券商口径差约 ±5–10%'],
  ['覆铜板高阶占比提升',{mix:1.0},{mix:1.3},'×1.0','×1.3','M7+ 占比 50%+ → 60–65%'],['二代布满足率',{gf:.6},{gf:1.0},'60%（广发）','100%（纪要）','源 广发 / 纪要'],['钻针有效供给',{dr:.9},{dr:1.1},'−10%','+10%','估'],['降级比例',{s:0},{s:.5},'0','50%','日东纺 NE 替代 NER；估']];
 const mkr=(fn)=>L.map(a=>({n:a[0],lo:fn(w(a[1])),hi:fn(w(a[2])),l1:a[3],l2:a[4],src:a[5]}));
 const abf=calc(b)['2027'].abf;
 CH.tornado('pcb-cTorA',f(b),mkr(f),{flip:abf,flipLbl:'ABF '+pct(abf),fmt:v=>(v*100).toFixed(0)+'%'});
 const LB=L.concat([['ABF 2027 供给增速',{abf:.2},{abf:.35},'+20%','+35%','KGI +25–30%，取宽']]);
 CH.tornado('pcb-cTorB',g(b),LB.map(a=>({n:a[0],lo:g(w(a[1])),hi:g(w(a[2])),l1:a[3],l2:a[4],src:a[5]})),{flip:0,flipLbl:'0：PCB 链比 ABF 更紧',fmt:v=>(v>0?'+':'')+(v*100).toFixed(0)+'pp'})}
/* ---- 平衡 */
function setOut(){const o={dem:v=>v+'%',g27:v=>v+'%',cn:v=>v+' 吨',gf:v=>v+'%',mix:v=>'×'+(v/100).toFixed(2),dr:v=>v+'%',abf:v=>'+'+v+'%',s:v=>v+'%'};for(const k in o)$('#pcb-o-'+k).textContent=o[k](sv('pcb-'+k))}
function drawBal(){setOut();const R=calc(P()),r=R['2027'],fg=V('--fg');
 $('#pcb-min').textContent=pct(r.pmin);$('#pcb-bind').textContent=NM[r.pbind];const sm=$('#pcb-sMin');if(sm)sm.textContent=pct(r.pmin);
 const bind=r.pmin<r.abf?'PCB 链（'+NM[r.pbind]+'）':'ABF 载板',d=(r.pmin-r.abf)*100;
 $('#pcb-balTxt').innerHTML=`2027（预测口径，不是市场观测）：PCB 材料最低 ${NM[r.pbind]} ${pct(r.pmin)}，ABF ${pct(r.abf)}，相差 ${d>0?'+':''}${d.toFixed(0)} 个百分点 → 出货约束是 <b>${bind}</b>${Math.abs(d)<5?'（两者在误差内打平）':''}。降级比例 ${sv('pcb-s')}%。${E}`;
 const ks=['cu','gf','ccl','dr','abf','hbm'],c=CH.C('pcb-cBal');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:44,right:14,top:CH.mob()?56:40,bottom:CH.mob()?54:30},xAxis:{data:ks.map(k=>NM[k]),axisLabel:{interval:0,fontSize:CH.mob()?10:12,rotate:CH.mob()?30:0}},yAxis:{max:1.4,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...CH.ax()},
  tooltip:{trigger:'axis',confine:true,valueFormatter:v=>pct(v)},
  series:['2025','2026','2027'].map((y,i)=>({name:y,type:'bar',barMaxWidth:22,data:ks.map(k=>R[y][k]==null?null:{value:+R[y][k].toFixed(3),itemStyle:{color:['#bcc6d6','#8fa8d8','#d9534f'][i],opacity:k=='abf'||k=='hbm'?.55:1}}),
   label:{show:y=='2027'&&!CH.mob(),position:'top',fontSize:10,color:fg,formatter:p=>pct(p.value)},markLine:i?undefined:{silent:true,symbol:'none',data:[{yAxis:1}],lineStyle:{type:'dashed',color:V('--mut')},label:{formatter:'100%',color:V('--mut')}}}))});
 drawToc(R);drawIf(R);drawTor()}
window.pcbReset=()=>{for(const k in S0)document.getElementById('pcb-'+k).value=S0[k];drawBal()};
/* ---- TOC：能支撑多少 AI 加速器 */
function drawToc(R){const r=R[yr],A=J.A[yr]*(yr=='2027'?sv('pcb-dem')/100:1),ks=['cu','gf','ccl','dr','abf'].concat(r.hbm!=null?['hbm']:[]),fg=V('--fg');
 const v=ks.map(k=>r[k]==null?null:+(r[k]*A).toFixed(2)),c=CH.C('pcb-cToc');
 c.setOption({...CH.base(),grid:{left:44,right:16,top:30,bottom:CH.mob()?54:30},xAxis:{data:ks.map(k=>NM[k]),axisLabel:{interval:0,fontSize:CH.mob()?10:12,rotate:CH.mob()?30:0}},yAxis:{name:'百万颗',max:v=>Math.ceil(Math.max(v.max,A)*1.12),...CH.ax()},tooltip:{trigger:'axis',confine:true,formatter:p=>{const k=ks[p[0].dataIndex];return`${NM[k]}：满足率 ${pct(r[k])}<br>能支撑 ${p[0].value==null?'—':p[0].value+' 百万颗'}<br>KGI 出货 ${A.toFixed(2)} 百万颗`}},
  series:[{type:'bar',barMaxWidth:40,data:v.map((x,i)=>({value:x,itemStyle:{color:ks[i]==r.pbind?'#d9534f':(ks[i]=='abf'||ks[i]=='hbm')?'#9e9e9e':'#5b8def'}})),label:{show:true,position:'top',color:fg,fontSize:11,formatter:p=>p.value==null?'':p.value.toFixed(1)},
   markLine:{silent:true,symbol:'none',data:[{yAxis:+A.toFixed(2)}],lineStyle:{type:'dashed',color:fg},label:{formatter:'KGI '+A.toFixed(1),color:fg,position:'insideEndTop'}}}]});
 const vd=k=>{if(r[k]==null)return'—';if(k=='abf'||k=='hbm')return'跨链（CoWoS 页）';return k==r.pbind?'预测口径最低':r[k]>=1?'不缺':'偏紧'};
 $('#pcb-tocT tbody').innerHTML=ks.map((k,i)=>`<tr><td><b>${NM[k]}</b></td><td>${pct(r[k])}</td><td>${v[i]==null?'—':v[i].toFixed(2)}</td><td><span class="pill" style="color:${k==r.pbind?'var(--acc)':'var(--mut)'}">${vd(k)}</span></td></tr>`).join('')+(yr=='2027'?`<tr><td><b>Q 布</b></td><td>83–100%（2026）</td><td>—</td><td><span class="pill">2028 年的故事</span></td></tr><tr><td><b>PCB 板厂</b></td><td>数据缺口</td><td>—</td><td><span class="pill">定性</span></td></tr>`:'');
 const mn=Math.min(...ks.map(k=>r[k]).filter(x=>x!=null)),bk=ks.find(k=>r[k]==mn);
 $('#pcb-tocTxt').innerHTML=`${yr} 年：预测口径下所有环节里最低的是 <b>${NM[bk]}</b>（${pct(mn)}，能支撑约 ${(mn*A).toFixed(1)} 百万颗）；PCB 材料里最低是 ${NM[r.pbind]}（${pct(r.pmin)}）。材料环节 &lt; 100% 是预测缺口，表示规格和价格受限，不直接等于少出货；可观测信号见短缺检验（ABF 3/4、HVLP4 1/4）${E}。`}
/* ---- 跨链接口 */
function drawIf(R){const ys=['2026','2027'],c=CH.C('pcb-cIf'),fg=V('--fg'),S=[['PCB 材料最低（预测）',y=>R[y].pmin,'#d9534f'],['ABF 载板',y=>R[y].abf,'#9e9e9e'],['HBM',y=>R[y].hbm,'#5b8def'],['CoWoS（下限）',y=>R[y].cwlo,'#26a69a']];
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:44,right:14,top:CH.mob()?56:40,bottom:30},xAxis:{data:ys},yAxis:{max:1.3,axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>pct(v)},
  series:S.map(([n,f,col],i)=>({name:n,type:'bar',barMaxWidth:26,color:col,data:ys.map(y=>f(y)==null?null:+f(y).toFixed(3)),label:{show:!CH.mob(),position:'top',fontSize:10,color:fg,formatter:p=>pct(p.value)},markLine:i?undefined:{silent:true,symbol:'none',data:[{yAxis:1}],lineStyle:{type:'dashed',color:V('--mut')},label:{formatter:'100%',color:V('--mut')}}}))});
 const r=R['2027'];$('#pcb-ifTxt').innerHTML=`2027（同一分母：KGI 加速器，预测口径）：PCB 材料最低 ${pct(r.pmin)}、ABF ${pct(r.abf)}、HBM ${pct(r.hbm)}、CoWoS ${pct(r.cwlo)}–${pct(r.cwhi)}。PCB 链和 ABF 同属"基板与材料"，都比 HBM、CoWoS 紧；区别是 PCB 材料可以降级，ABF 不能。`}
/* ---- 需求 */
function drawDem(){const G=J.gs,c=CH.C('pcb-cDem'),fg=V('--fg'),ys=G.y.map(String);
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:44,right:50,top:CH.mob()?56:40,bottom:30},xAxis:{data:ys},yAxis:[{name:'十亿美元',...CH.ax()},{name:'美元/颗',splitLine:{show:false}}],tooltip:{trigger:'axis',confine:true},
  series:[{name:'AI 服务器 PCB',type:'bar',data:G.pcb,color:'#d9534f',barMaxWidth:28,label:{show:true,position:'top',fontSize:10,color:fg}},{name:'AI CCL',type:'bar',data:G.ccl,color:'#5b8def',barMaxWidth:28},
   {name:'每颗加速器 PCB 价值（估）',type:'line',yAxisIndex:1,data:ys.map(y=>J.per[y]??null),color:'#ff9900',symbolSize:7,label:{show:true,formatter:p=>p.value?'$'+p.value:'',fontSize:10,color:fg}}]});
 const m=J.m9,c2=CH.C('pcb-cM9');
 c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:40,right:14,top:CH.mob()?66:44,bottom:30},xAxis:{data:ys},yAxis:{max:80,axisLabel:{formatter:'{value}%'},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':(+v).toFixed(0)+'%'},
  series:[{name:'30 层以上占 AI PCB（高盛）',type:'line',data:G.l30,color:'#9e9e9e',symbolSize:6},{name:'6+N+6 HDI（高盛）',type:'line',data:G.hdi,color:'#26a69a',symbolSize:6},
   {name:'M9 占 AI CCL（高盛）',type:'line',data:G.m9,color:'#d9534f',lineStyle:{width:3},symbolSize:8,label:{show:true,formatter:p=>p.value!=null?p.value+'%':'',color:fg,fontSize:11}},
   {name:'M9（我们，估）',type:'scatter',symbol:'rect',symbolSize:[14,Math.max(8,(m.hi_s-m.lo_s)*100*2.6)],data:[[2,+(m.mid_s*100).toFixed(1)]],itemStyle:{color:'#8a5cf6',opacity:.75},label:{show:true,position:'right',formatter:()=>(m.lo_s*100).toFixed(0)+'–'+(m.hi_s*100).toFixed(0)+'%',color:'#8a5cf6',fontWeight:'bold'}}]});
 $('#pcb-gsT tbody').innerHTML=G.y.map((y,i)=>`<tr><td><b>${y}</b></td><td>${G.area[i]*100}</td><td>${G.asp[i].toLocaleString()}</td><td>${G.pcb[i]}</td><td>${G.sheets[i]}</td><td>${G.usd_sh[i]}</td><td>${G.ccl[i]}</td><td>${G.m9[i]==null?'—':G.m9[i]+'%'}</td></tr>`).join('')}
/* ---- 供给 */
function drawSup(){const m=J.model,g=J.gs,c=CH.C('pcb-cSup'),fg=V('--fg'),cat=['AI PCB 面积','AI CCL 张数','HVLP3+ 铜箔','二代布','钻针'];
 const dem=[g.area[2]/g.area[1],g.sheets[2]/g.sheets[1],m.CU.d27/m.CU.d26,8000/5250,76.73/51.16],sup=[null,m.CCLg,1000/840,null,69.47/50.05];
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:40,right:14,top:CH.mob()?56:40,bottom:CH.mob()?54:30},xAxis:{data:cat,axisLabel:{interval:0,fontSize:CH.mob()?10:12,rotate:CH.mob()?30:0}},yAxis:{min:.8,axisLabel:{formatter:v=>'×'+v.toFixed(1)},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'无同口径数据':'×'+(+v).toFixed(2)},
  series:[{name:'需求 2027÷2026',type:'bar',data:dem.map(x=>+x.toFixed(2)),color:'#d9534f',barMaxWidth:30,label:{show:true,position:'top',fontSize:10,color:fg,formatter:p=>'×'+p.value.toFixed(2)}},{name:'供给 2027÷2026',type:'bar',data:sup.map(x=>x==null?null:+x.toFixed(2)),color:'#5b8def',barMaxWidth:30,label:{show:true,position:'top',fontSize:10,color:fg,formatter:p=>p.value==null?'':'×'+p.value.toFixed(2)}}]});
 $('#pcb-stT tbody').innerHTML=J.stages.map(r=>`<tr><td><b>${r[1]}</b></td><td>${r[2]}</td><td>${r[3]}</td><td><b>${r[4]}</b></td><td class="note">${CH.srcInline(r[5]).replace(/（估）/g,E)}</td><td>${CH.tag(r[6])}</td></tr>`).join('')}
/* ---- 利润 */
function drawProfit(){const D=J.profit.dgm,c=CH.C('pcb-cDgm'),fg=V('--fg'),col={'玻纤布':'#ff9900','钻针':'#8a5cf6','铜箔':'#c0392b','CCL':'#5b8def','PCB 板厂':'#9e9e9e'},R=D.slice().reverse();
 c.setOption({...CH.base(),grid:{left:CH.mob()?96:120,right:40,top:10,bottom:26},xAxis:{type:'value',axisLabel:{formatter:'{value}pp'},...CH.ax()},yAxis:{type:'category',data:R.map(r=>r[0].replace(/ \d+$/,'')),axisLabel:{fontSize:CH.mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},formatter:p=>{const r=R[p[0].dataIndex];return`${r[0]}（${r[1]}）<br>${r[3]}% → ${r[2]}%（${r[4]}）`}},
  series:[{type:'bar',data:R.map(r=>({value:+(r[2]-r[3]).toFixed(1),itemStyle:{color:col[r[1]]}})),label:{show:true,position:'right',fontSize:10,color:fg,formatter:p=>(p.value>0?'+':'')+p.value}}]});
 $('#pcb-dgmT tbody').innerHTML=D.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}%</td><td>${r[3]}%</td><td>${r[4]}</td><td>${CH.tag(r[5])}</td></tr>`).join('');
 const G=J.profit.margins,N=J.profit.names,c2=CH.C('pcb-cMar'),qs=[...new Set(Object.values(G).flatMap(a=>a.map(x=>x[0])))].sort(),cl={'2383':'#5b8def','6274':'#26a69a','6213':'#9ccc65','2368':'#9e9e9e','8358':'#c0392b','1815':'#ff9900','8021':'#8a5cf6'};
 c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:10},itemWidth:14},grid:{left:40,right:12,top:CH.mob()?70:44,bottom:30},xAxis:{type:'category',data:qs.map(q=>q.slice(0,4)+'Q'+Math.ceil(+q.slice(5,7)/3)),axisLabel:{interval:3}},yAxis:{axisLabel:{formatter:'{value}%'},...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'-':v+'%'},
  series:Object.keys(G).map(k=>({name:N[k],type:'line',showSymbol:false,connectNulls:true,lineStyle:{width:['1815','8021','8358'].includes(k)?3:1.8},color:cl[k],data:qs.map(q=>{const r=G[k].find(x=>x[0]==q);return r?r[2]:null})}))})}
/* ---- 回测 */
function drawBt(){const S=J.bt.series,c=CH.C('pcb-cBt'),L=(k,n,col,w)=>({name:n,type:'line',showSymbol:false,data:S[k].filter(x=>x[1]!=null).map(x=>[x[0]+'-15',Math.max(-80,Math.min(250,x[1]))]),color:col,lineStyle:{width:w}});
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:46,right:14,top:CH.mob()?70:44,bottom:56},xAxis:{type:'time'},yAxis:{name:'3M同比',axisLabel:{formatter:'{value}%'},...CH.ax()},dataZoom:[{type:'slider',height:18,bottom:8,start:30,end:100},{type:'inside'}],tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'-':(+v).toFixed(0)+'%'},
  series:[L('ccl','CCL 三家','#5b8def',2.5),L('mat','上游三家（铜箔+玻纤布+钻针）','#ff9900',1.6),L('2368','金像电','#9e9e9e',2),L('2330','台积电','#d9534f',1.4)]});
 const X=J.bt.xc,ks=Object.keys(X[Object.keys(X)[0]]).map(Number).sort((a,b)=>a-b),c2=CH.C('pcb-cXc'),cl=['#ff9900','#5b8def','#d9534f'];
 c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:V('--fg'),fontSize:11}},grid:{left:40,right:10,top:CH.mob()?56:36,bottom:34},xAxis:{data:ks,name:'k(月)',nameLocation:'middle',nameGap:22},yAxis:{min:-.3,max:1,...CH.ax()},series:Object.keys(X).map((k,i)=>({name:k,type:'bar',data:ks.map(l=>X[k][l]?X[k][l][0]:null),color:cl[i]}))})}
/* ---- 中国账本 */
function cnP(){return{u:sv('pcb-cnu'),usd:sv('pcb-cnusd')}}
function cnCalc(o){const m=J.model.CN,A27=J.A['2027'],kg=J.model.CUKG['2027'],fab=m.fab_cny/m.fx*1e8,need=o.u*1e6*o.usd,cu=o.u*1e6*kg/1000/12,lo=m.ldk_per[0]*1e4/(A27*1e6),hi=m.ldk_per[1]*1e4/(A27*1e6);
 return{fab:need/fab,fabcn:need/(m.cnpcb_usd*1e8),cu:cu/m.cu_t,cut:cu,ldk:[o.u*lo*100/m.ldk,o.u*hi*100/m.ldk],up:{fab:fab/o.usd/1e6,cu:m.cu_t*12*1000/kg/1e6,ldk:[m.ldk*1e4/hi/1e6,m.ldk*1e4/lo/1e6]}}}
function drawCn(){const o=cnP(),r=cnCalc(o),fg=V('--fg');$('#pcb-cno1').textContent=o.u.toFixed(1)+' 百万张';$('#pcb-cno2').textContent=o.usd.toLocaleString()+' 美元';
 $('#pcb-cnFab').textContent=pct(r.fab);$('#pcb-cnCuR').textContent=pct(r.cu);
 $('#pcb-cnTxt').innerHTML=`国产卡 ${o.u.toFixed(2)} 百万张 × ${o.usd.toLocaleString()} 美元 = ${(o.u*o.usd/1000).toFixed(2)} 十亿美元 PCB，占三家龙头年化产值 ${pct(r.fab)}、中国大陆 PCB 产值 ${pct(r.fabcn)}；HVLP 约 ${r.cut.toFixed(0)} 吨/月（德福 HVLP 出货的 ${pct(r.cu)}）；二代布占宏和一家产能的 ${pct(r.ldk[0])}–${pct(r.ldk[1])}。${E}`;
 const c=CH.C('pcb-cnBal'),cat=['PCB（三家龙头）','PCB（中国大陆）','HVLP 铜箔（德福）','二代布（宏和，高）','二代布（宏和，低）'],v=[r.fab,r.fabcn,r.cu,r.ldk[1],r.ldk[0]];
 c.setOption({...CH.base(),grid:{left:CH.mob()?110:130,right:46,top:16,bottom:26},xAxis:{type:'value',axisLabel:{formatter:v=>(v*100).toFixed(0)+'%'},...CH.ax()},yAxis:{type:'category',data:cat,axisLabel:{fontSize:CH.mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},valueFormatter:v=>pct(v)},
  series:[{type:'bar',data:v.map(x=>({value:+x.toFixed(3),itemStyle:{color:x>=1?'#d9534f':x>=.5?'#e0a030':'#5b8def'}})),label:{show:true,position:'right',color:fg,fontSize:11,formatter:p=>pct(p.value)},markLine:{silent:true,symbol:'none',data:[{xAxis:1}],lineStyle:{type:'dashed',color:V('--acc')},label:{formatter:'100%',color:V('--acc')}}}]});
 const N=J.cn,t=CH.C('pcb-cnToc'),tk=[['HBM',N.toc[0][1]],['2.5D',N.toc[1][1]],['板厂',r.up.fab],['HVLP',r.up.cu],['二代布(低)',r.up.ldk[0]]];
 t.setOption({...CH.base(),grid:{left:40,right:14,top:30,bottom:30},xAxis:{data:tk.map(x=>x[0]),axisLabel:{interval:0,fontSize:CH.mob()?10:12}},yAxis:{name:'百万张',max:v=>Math.ceil(Math.max(v.max,o.u)*1.12),...CH.ax()},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(+v).toFixed(2)+' 百万张'},
  series:[{type:'bar',barMaxWidth:40,data:tk.map((x,i)=>({value:+(+x[1]).toFixed(2),itemStyle:{color:i==0?'#d9534f':i==1?'#e0a030':'#5b8def',opacity:i>1?.7:1}})),label:{show:true,position:'top',color:fg,formatter:p=>p.value.toFixed(1)},
   markLine:{silent:true,symbol:'none',data:[{yAxis:o.u}],lineStyle:{type:'dashed',color:fg},label:{formatter:'国产卡 '+o.u.toFixed(2),color:fg,position:'insideEndTop'}}}]});
 const cc=CH.C('pcb-cnCu'),kg=J.model.CUKG['2027'],nd=u=>u*1e6*kg/1000/12;
 cc.setOption({...CH.base(),grid:{left:CH.mob()?116:150,right:46,top:10,bottom:26},xAxis:{type:'value',name:'吨/月',...CH.ax()},yAxis:{type:'category',data:['金居 HVLP4（2H26，对照）','德福 HVLP4（8 月）','德福 HVLP 合计（8 月）','国产卡所需：不缺货需求','国产卡所需：当前滑块'],axisLabel:{fontSize:CH.mob()?10:12}},tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},valueFormatter:v=>(+v).toFixed(0)+' 吨/月'},
  series:[{type:'bar',data:[{value:150,itemStyle:{color:'#9e9e9e'}},{value:70,itemStyle:{color:'#5b8def'}},{value:500,itemStyle:{color:'#5b8def'}},{value:+nd(J.cn.u27).toFixed(0),itemStyle:{color:'#d9534f'}},{value:+nd(o.u).toFixed(0),itemStyle:{color:'#e0a030'}}],label:{show:true,position:'right',color:fg,formatter:p=>p.value}}]})}
window.pcbCnReset=()=>{document.getElementById('pcb-cnu').value=J.cn.whk27.toFixed(1);document.getElementById('pcb-cnusd').value=1621;drawCn()};
function cnOnce(){const N=J.cn,R=(sel,rows,f)=>$(sel).innerHTML=rows.map(f).join('');
 R('#pcb-cnDemT tbody',N.dem,r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${CH.srcInline(r[2]).replace(/（估）/g,E)}</td></tr>`);
 R('#pcb-cnSupT tbody',N.sup,r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${CH.srcInline(r[2])}</td></tr>`);
 R('#pcb-cnTocT tbody',N.toc,r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${CH.srcInline(r[2]).replace(/（估）/g,E)}</td><td><span class="pill" style="color:${/^约束/.test(r[3])?'var(--acc)':/^风险/.test(r[3])?'var(--warn)':'var(--ok)'}">${r[3]}</span></td></tr>`);
 R('#pcb-cnCoT tbody',N.co,c=>`<tr><td>${c[0]}</td><td><b>${c[1]}</b></td><td style="white-space:nowrap">${c[2]}</td><td>${c[3]}</td><td><span class="pill" style="color:${/^强/.test(c[4])?'var(--ok)':/^中/.test(c[4])?'var(--warn)':'var(--mut)'}">${c[4]}</span></td><td>${CH.tag(c[5])}</td></tr>`);
 CH.timeline('#pcb-cntl',N.timeline);CH.players('#pcb-cnPl',N.players);CH.falsify('#pcb-cnFalT tbody',N.falsify);CH.ledger('#pcb-cnPredT tbody','#pcb-cnPredS',N.preds);
 ['pcb-cnu','pcb-cnusd'].forEach(id=>document.getElementById(id).addEventListener('input',drawCn))}
window.pcbNet=()=>CH.net('pcb-cNet','#pcb-nodeInfo',J.companies,mk);
/* ---- v0.2 行业地图：Prismark 分产品规模与增速 */
function drawSeg(){const el=document.getElementById('pcb-cSeg');if(!el||!J.industry)return;const G=J.industry.segs,c=CH.C('pcb-cSeg'),fg=V('--fg');
 c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11}},grid:{left:44,right:44,top:40,bottom:CH.mob()?52:30},xAxis:{data:G.map(g=>g[0]),axisLabel:{interval:0,fontSize:CH.mob()?10:12,rotate:CH.mob()?30:0}},
  yAxis:[{name:'亿美元',...CH.ax()},{name:'增速 %',splitLine:{show:false},axisLabel:{formatter:'{value}%'}}],tooltip:{trigger:'axis',confine:true},
  series:[{name:'2026E 规模（亿美元）',type:'bar',barMaxWidth:34,data:G.map(g=>({value:g[1],itemStyle:{color:g[2]>=20?'#d9534f':g[2]>=10?'#e0a030':'#5b8def'}})),label:{show:true,position:'top',fontSize:10,color:fg}},
   {name:'2026 增速（Q1 口径）',type:'line',yAxisIndex:1,data:G.map(g=>g[2]),color:'#8a5cf6',symbolSize:7,label:{show:!CH.mob(),formatter:p=>'+'+p.value+'%',color:'#8a5cf6',fontSize:10}}]})}
function render(){drawSeg();drawBal();drawDem();drawSup();drawProfit();drawBt();drawCn();CH.driver('pcb-cDrv','#pcb-drvT tbody',J.driver,{srcHref:'cowos.html#src'});window.pcbNet()}
window.redraw=render;
fetch('data/pcb.json?v=9f2df30a32').then(r=>r.json()).then(j=>{J=j;
 $('#pcb-upd').textContent=J.meta.updated;CH.stats('#pcb-stats',J.judgment.stats);CH.debates('#pcb-deb',J.debates);$('#pcb-torNote').textContent=J.tornado_note;
 CH.table('#pcb-varT tbody',J.variants,5);CH.table('#pcb-procT tbody',J.process,3);CH.table('#pcb-prT tbody',J.price,3);
 CH.neck('#pcb-neck',J.neck);CH.players('#pcb-play',J.players);CH.timeline('#pcb-tl1',J.history.tl1,'');CH.timeline('#pcb-tl2',J.history.tl2,'h');$('#pcb-rule').textContent=J.history.rule;
 CH.leadCards('#pcb-lead',J.lead.cards);CH.table('#pcb-tpT tbody',J.bt.tp,-1,false);
 const s=J.bt.series.ccl,l=s[s.length-1];$('#pcb-btNow').innerHTML=`最新：${l[0]} CCL 三家 3 个月营收同比 +${l[1].toFixed(0)}%，还在加速；金像电 +${J.bt.now['2368'].toFixed(0)}%。按历史，CCL 同比见顶后约 1–17 个月（中位 5 个月）金像电同比见顶。拐点用 ±6 个月局部极值识别 ${E}。`;
 CH.ledger('#pcb-predT tbody','#pcb-predSum',J.predictions);CH.falsify('#pcb-falT tbody',J.falsify);CH.coTable('#pcb-coT tbody',J.companies);
 CH.table('#pcb-ifT-b',J.interface.rows,-1);$('#pcb-formula').textContent=J.interface.formula;
 CH.sources('#pcb-srcL',J.sources);CH.list('#pcb-lim',J.limits);CH.table('#pcb-logT tbody',J.changelog,-1);
 Object.keys(S0).forEach(k=>document.getElementById('pcb-'+k).addEventListener('input',drawBal));
 CH.segFilter('#pcb-fMk',m=>{mk=m;window.pcbNet()});CH.segFilter('#pcb-fYr',m=>{yr=m;drawBal()});cnOnce();render()});
})();
