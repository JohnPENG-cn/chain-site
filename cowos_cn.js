/* cowos_cn.js — CoWoS v0.4 中国账本：国产 AI 卡只能在大陆做的 2.5D 封装。
   公式与 cowos/build.py 的 cwcn() 一致；HBM 一栏读 data/hbm.json 的中国账本基准（cn.bal）。所有 id 带 wn 前缀。 */
(function(){let N,HB;const $=CH.$,Y=[2025,2026,2027],E='<span class="tag t-est">估</span>';
const S0={c26:23,c27:50,ai:70,pk:100};
function bal(o){const m=N.model,cap={...m.cap,'2026':o.c26,'2027':o.c27},ai=o.ai/100,pk=o.pk/100,out={};
 for(const y of Y){const k=String(y),pw=m.ppw[k]*pk,np=m.npr[k],h=HB[y],s=(cap[y-1]+cap[k])/2*12*ai*m.ut,u=h.u,hc=Math.min(h.cards,u);
  const du=(u+np)/pw*1000,dh=(hc+np)/pw*1000;out[y]={y,s,du,dh,cov:s/du,covh:s/dh,pw,cards:s*pw/1000,hcards:hc+np,cap:cap[k]}}
 return out}
const pct=v=>(v*100).toFixed(0)+'%',sv=id=>+document.getElementById(id).value;
function opt(){return{c26:sv('wns1'),c27:sv('wns2'),ai:sv('wns3'),pk:sv('wns4')}}
function draw(){if(!N)return;const o=opt(),R=bal(o),fg=CH.V('--fg'),mu=CH.V('--mut');
 wno1.value=o.c26+'K';wno2.value=o.c27+'K';wno3.value=o.ai+'%';wno4.value=o.pk+'%';
 $('#wnH26').textContent=pct(R[2026].covh);$('#wnC26').textContent=pct(R[2026].cov);
 $('#wnK26').textContent='约 '+Math.round(R[2026].cards*100)+' 万';$('#wnHK26').textContent='约 '+Math.round(R[2026].hcards*100)+' 万';
 $('#wnTxt').innerHTML=`国产 AI 可用 2.5D：2026 年约 ${R[2026].s.toFixed(0)} 千片、2027 年约 ${R[2027].s.toFixed(0)} 千片。HBM 能配的卡所需 2026 年 ${R[2026].dh.toFixed(0)}、2027 年 ${R[2027].dh.toFixed(0)} 千片；不缺货需求 ${R[2026].du.toFixed(0)} / ${R[2027].du.toFixed(0)} 千片。2027 年覆盖 HBM 能配的卡 ${pct(R[2027].covh)}、不缺货需求 ${pct(R[2027].cov)}。${E}`;
 const c=CH.C('wn-cBal');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11},itemWidth:12,itemHeight:8},grid:{left:44,right:14,top:CH.mob()?62:44,bottom:30},
  tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':Math.round(v)+' 千片'},xAxis:{data:Y.map(String)},yAxis:{...CH.ax()},
  series:[{name:'国产 AI 可用 2.5D',type:'bar',barMaxWidth:44,itemStyle:{color:'#e0a030'},data:Y.map(y=>Math.round(R[y].s)),label:{show:true,position:'insideBottom',distance:6,color:'#222',fontSize:11}},
   {name:'不缺货需求',type:'line',data:Y.map(y=>Math.round(R[y].du)),itemStyle:{color:fg},lineStyle:{width:2.5,color:fg},symbolSize:7},
   {name:'HBM 能配的卡所需',type:'line',data:Y.map(y=>Math.round(R[y].dh)),itemStyle:{color:'#d9534f'},lineStyle:{type:'dashed',width:2,color:'#d9534f'},symbolSize:6}]});
 const t=CH.C('wn-cToc');t.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg}},grid:{left:40,right:14,top:CH.mob()?56:44,bottom:30},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(+v).toFixed(2)+' 百万张'},
  xAxis:{data:Y.map(String)},yAxis:{...CH.ax()},series:[
   {name:'2.5D 能封',type:'bar',barMaxWidth:36,itemStyle:{color:'#e0a030'},data:Y.map(y=>+R[y].cards.toFixed(2)),label:{show:true,position:'top',color:fg,formatter:p=>p.value.toFixed(2)}},
   {name:'HBM 能配（+950PR）',type:'bar',barMaxWidth:36,itemStyle:{color:'#5b8def'},data:Y.map(y=>+R[y].hcards.toFixed(2)),label:{show:true,position:'top',color:fg,formatter:p=>p.value.toFixed(2)}}]});
 const m=N.model,ky=['2024','2025','2026','2027'],cp=ky.map(k=>k=='2026'?o.c26:k=='2027'?o.c27:m.cap[k]),av=cp.map(v=>+(v*o.ai/100*m.ut).toFixed(1));
 const cc=CH.C('wn-cCap');cc.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg}},grid:{left:40,right:14,top:44,bottom:30},tooltip:{trigger:'axis',confine:true,valueFormatter:v=>(+v).toFixed(1)+' 千片/月'},
  xAxis:{data:ky.map(k=>k+(k<'2026'?'（估）':''))},yAxis:{...CH.ax()},series:[
   {name:'国产 AI 可用',type:'bar',stack:'a',barMaxWidth:44,itemStyle:{color:'#e0a030'},data:av},
   {name:'其余',type:'bar',stack:'a',barMaxWidth:44,itemStyle:{color:'#e0a030',opacity:.35},data:cp.map((v,i)=>+(v-av[i]).toFixed(1)),label:{show:true,position:'top',color:fg,formatter:p=>cp[p.dataIndex]}}]});
 const dd={'2025|实际':R[2025].du,'2026|不缺货需求':R[2026].du,'2026|HBM 能配的卡':R[2026].dh,'2027|不缺货需求':R[2027].du,'2027|HBM 能配的卡':R[2027].dh};
 $('#wn-demT tbody').innerHTML=N.dem_basis.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td style="white-space:nowrap">${r[2]}</td><td>${CH.srcInline(r[3]).replace(/（估）/g,E)}</td><td><b>${Math.round(dd[r[0]+'|'+r[1]])}</b></td></tr>`).join('');
 $('#wn-tocT tbody').innerHTML=N.toc.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]=='__HBM__'?`约 ${Math.round(R[2026].hcards*100)} 万张`:r[1]=='__CW__'?`约 ${Math.round(R[2026].cards*100)} 万张（${R[2026].s.toFixed(0)} 千片 × ${R[2026].pw.toFixed(1)} 颗）`:r[1]}</td><td>${CH.srcInline(r[2]).replace('{E}',E)}</td><td><span class="pill" style="color:${/^约束/.test(r[3])?'var(--acc)':/^风险/.test(r[3])?'var(--warn)':'var(--mut)'}">${r[3]}</span></td></tr>`).join('')}
function once(){CH.timeline('#wn-tl',N.timeline);CH.players('#wnPl',N.players);CH.falsify('#wnFalT tbody',N.falsify);CH.ledger('#wnPredT tbody','#wnPredS',N.preds);
 $('#wn-supT tbody').innerHTML=N.sup_basis.map(r=>`<tr><td><b>${r[0]}</b></td><td style="white-space:nowrap">${r[1]}</td><td>${CH.srcInline(r[2]).replace(/（估）/g,E)}</td></tr>`).join('');
 $('#wn-coT tbody').innerHTML=N.co.map(c=>`<tr><td>${c[0]}</td><td><b>${c[1]}</b></td><td style="white-space:nowrap">${c[2]}</td><td>${c[3]}</td><td><span class="pill" style="color:${/^强/.test(c[4])?'var(--ok)':/^中/.test(c[4])?'var(--warn)':'var(--mut)'}">${c[4]}</span></td><td>${CH.tag(c[5])}</td></tr>`).join('');
 ['wns1','wns2','wns3','wns4'].forEach(id=>document.getElementById(id).addEventListener('input',draw))}
window.wnReset=()=>{wns1.value=S0.c26;wns2.value=S0.c27;wns3.value=S0.ai;wns4.value=S0.pk;draw()};
Promise.all([fetch('data/cowos.json?v=ae78e22b59').then(r=>r.json()),fetch('data/hbm.json?v=a4fc96910a').then(r=>r.json())]).then(([j,h])=>{N=j.cn;HB={};h.cn.bal.forEach(r=>HB[r.y]=r);once();draw()});
addEventListener('load',()=>setTimeout(()=>{const o=window.redraw;window.redraw=()=>{o&&o();draw()}},0));
})();
