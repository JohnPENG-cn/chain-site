/* hbm_cn.js — HBM v0.5 中国账本：国产加速卡能用上的裸 HBM（需求 vs 可用 = 期初库存 + 合法进口 + 灰色渠道 + 长鑫 + 武汉新芯）。
   公式与 hbm/build.py 的 cnbal() 一致；所有 id 带 cn 前缀。数据：data/hbm.json 的 cn 字段。 */
(function(){let M,N,CW=null;const $=CH.$,Y=[2024,2025,2026,2027],E='<span class="tag t-est">估</span>';
const S0={g:25,w27:55,g27:165,gray:10};
function bal(o){const m=N.model,g=o.g/100,cxw={...m.cxw,'2027':o.w27},cxg={...m.cxg,'2027':o.g27};let inv=0;const out={};
 for(const y of Y){const k=String(y);let u,gb,ul;
  if(m.act[k]){[u,gb]=m.act[k];ul=u}else{const n=y-2025;u=m.mkt25*(1+g)**n-m.lpddr[k];gb=m.gb[k];ul=m.low26*(1+m.low_g)**(n-1)-m.lpddr[k]}
  const d=u*gb/1000,dl=ul*gb/1000,cx=y>2024?(cxw[y-1]+cxw[k])/2*12*(cxg[k]||0)/1e6:0,gy=y<2026?m.gray[k]:o.gray/1000;
  const f={inv,imp:m.imp[k]||0,gray:gy,cx,xmc:cx*m.xmc},a=Object.values(f).reduce((p,q)=>p+q,0);
  out[y]={y,u,gb,d,dl,...f,a,cov:a/d,covl:a/dl,cards:a/gb*1000};inv=a-Math.min(d,a)}
 return out}
const pct=v=>(v*100).toFixed(0)+'%',f3=v=>v<0.0005?'0':v.toFixed(3);
function opt(){const o={};[['g','cns1'],['w27','cns2'],['g27','cns3'],['gray','cns4']].forEach(([k,id])=>o[k]=+document.getElementById(id).value);return o}
function draw(){if(!N)return;const o=opt(),R=bal(o),fg=CH.V('--fg'),ln=CH.V('--line');
 cno1.value=o.g+'%';cno2.value=o.w27+'K';cno3.value=o.g27;cno4.value=o.gray;
 $('#cnG26').textContent=pct(R[2026].cov);$('#cnG27').textContent=pct(R[2027].cov);$('#cnK26').textContent='约 '+Math.round(R[2026].cards*100)+' 万';
 $('#cnTxt').innerHTML=`2026 年需求 ${R[2026].d.toFixed(2)} EB、可用 ${R[2026].a.toFixed(2)} EB；2027 年需求 ${R[2027].d.toFixed(2)} EB、可用 ${R[2027].a.toFixed(2)} EB。按机构出货口径（需求下限）覆盖率 2026 ${pct(R[2026].covl)}、2027 ${pct(R[2027].covl)}。可用 HBM 能配国产卡：2026 约 ${Math.round(R[2026].cards*100)} 万张、2027 约 ${Math.round(R[2027].cards*100)} 万张。${E}`;
 const ser=[['inv','期初库存','#9e9e9e'],['imp','合法进口（禁令前）','#5b8def'],['gray','灰色渠道','#8a5cf6'],['cx','长鑫','#d9534f'],['xmc','武汉新芯','#ff9900']].map(([k,n,c])=>({name:n,type:'bar',stack:'a',barMaxWidth:44,itemStyle:{color:c},data:Y.map(y=>+R[y][k].toFixed(4))}));
 const c=CH.C('cn-cBal');c.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg,fontSize:11},itemWidth:12,itemHeight:8},grid:{left:44,right:14,top:CH.mob()?76:50,bottom:30},
  tooltip:{trigger:'axis',confine:true,valueFormatter:v=>v==null?'—':(+v).toFixed(3)+' EB'},xAxis:{data:Y.map(String)},yAxis:{...CH.ax()},
  series:[...ser,{name:'不缺货需求',type:'line',data:Y.map(y=>+R[y].d.toFixed(3)),itemStyle:{color:fg},lineStyle:{width:2.5,color:fg},symbolSize:7},
   {name:'机构出货口径',type:'line',data:Y.map(y=>+R[y].dl.toFixed(3)),itemStyle:{color:fg},lineStyle:{type:'dashed',color:fg},symbolSize:5}]});
 const cv=CH.C('cn-cCov'),cap=v=>Math.min(v,1.6)*100;cv.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg}},tooltip:{trigger:'axis',confine:true},xAxis:{data:Y.map(String)},
  grid:{left:44,right:14,top:CH.mob()?56:44,bottom:30},yAxis:{max:160,axisLabel:{formatter:'{value}%'},...CH.ax()},series:[{name:'可用 ÷ 不缺货需求',type:'line',data:Y.map(y=>({value:cap(R[y].cov),label:{show:true,formatter:pct(R[y].cov),color:fg,position:y>2025?'bottom':'top'}})),itemStyle:{color:'#d9534f'},lineStyle:{width:2.5},symbolSize:8,
   markLine:{silent:true,symbol:'none',data:[{yAxis:100}],lineStyle:{color:CH.V('--mut'),type:'dotted'},label:{formatter:'100% = 够用',color:CH.V('--mut'),position:'insideEndTop'}}},
   {name:'可用 ÷ 机构出货口径',type:'line',data:Y.map(y=>({value:cap(R[y].covl),label:{show:y>2025,formatter:pct(R[y].covl),color:CH.V('--mut'),position:'top'}})),itemStyle:{color:'#5b8def'},lineStyle:{type:'dashed'}}]});
 // 投片对照（年底，千片/月）：韩美三家 = UBS 年末产能（data/hbm.json cap 季末值），长鑫 = SemiAnalysis
 const q=M.cap.q,ky=['2025','2026','2027'],kr=ky.map(y=>['SK hynix','Samsung','Micron'].reduce((a,n)=>a+M.cap[n][q.indexOf('4Q'+y.slice(2))],0)),cx=ky.map(y=>y=='2027'?o.w27:N.model.cxw[y]);
 const cc=CH.C('cn-cCx');cc.setOption({...CH.base(),legend:{top:0,textStyle:{color:fg}},grid:{left:44,right:14,top:44,bottom:30},xAxis:{data:ky.map(y=>y+' 年底')},yAxis:{...CH.ax()},
  series:[{name:'韩美三家合计',type:'bar',barMaxWidth:40,data:kr.map(Math.round),itemStyle:{color:'#5b8def'},label:{show:true,position:'top',color:fg}},
   {name:'长鑫（HBM 投片）',type:'bar',barMaxWidth:40,data:cx,itemStyle:{color:'#d9534f'},label:{show:true,position:'top',color:fg,formatter:p=>p.value+'（'+(p.value/kr[p.dataIndex]*100).toFixed(0)+'%）'}}]});
 // 表
 $('#cn-supT tbody').innerHTML=Y.map(y=>{const r=R[y];return`<tr><td><b>${y}</b></td>${['inv','imp','gray','cx','xmc','a'].map(k=>`<td>${k=='a'?'<b>'+f3(r[k])+'</b>':f3(r[k])}</td>`).join('')}</tr>`}).join('');
 const dd={'2024|实际':R[2024].d,'2025|实际':R[2025].d,'2026|不缺货需求':R[2026].d,'2026|机构出货口径（下限）':R[2026].dl,'2027|不缺货需求':R[2027].d,'2027|机构出货口径（下限）':R[2027].dl};
 $('#cn-demT tbody').innerHTML=N.dem_basis.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td style="white-space:nowrap">${r[2]}</td><td>${CH.srcInline(r[3]).replace(/（估）/g,E)}</td><td><b>${f3(dd[r[0]+'|'+r[1]])}</b></td></tr>`).join('');
 $('#cn-tocT tbody').innerHTML=N.toc.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]=='__HBM__'?`约 ${Math.round(R[2026].cards*100)} 万张卡（${R[2026].a.toFixed(2)} EB ÷ ${R[2026].gb}GB）`:r[1]=='__CW__'?(CW?`约 ${Math.round(CW.cards*100)} 万张卡（含不用标准 HBM 的 950PR 约 ${Math.round(CW.np*100)} 万；对照 HBM ${Math.round(R[2026].cards*100)} 万 + 950PR）`:'—'):CH.srcInline(r[1])}</td><td>${/^源[\d,]+$/.test(r[2])?CH.tag(r[2].slice(1)):CH.srcInline(r[2]).replace('{E}',E)}</td><td><span class="pill" style="color:${r[3]=='约束'||r[3]=='约束之一'?'var(--acc)':'var(--mut)'}">${r[3]}</span></td></tr>`).join('')}
function once(){CH.timeline('#cn-tl',N.timeline);CH.players('#cnPl',N.players);CH.falsify('#cnFalT tbody',N.falsify);CH.ledger('#cnPredT tbody','#cnPredS',N.preds);
 $('#cn-coT tbody').innerHTML=N.co.map(c=>`<tr><td>${c[0]}</td><td><b>${c[1]}</b></td><td style="white-space:nowrap">${c[2]}</td><td>${c[3]}</td><td><span class="pill" style="color:${/^强/.test(c[4])?'var(--ok)':/^中/.test(c[4])?'var(--warn)':'var(--mut)'}">${c[4]}</span></td><td>${CH.tag(c[5])}</td></tr>`).join('');
 ['cns1','cns2','cns3','cns4'].forEach(id=>document.getElementById(id).addEventListener('input',draw))}
window.cnReset=()=>{cns1.value=S0.g;cns2.value=S0.w27;cns3.value=S0.g27;cns4.value=S0.gray;draw()};
fetch('data/hbm.json').then(r=>r.json()).then(m=>{M=m;N=m.cn;once();draw()});
fetch('data/cowos.json').then(r=>r.json()).then(j=>{const b=j.cn.bal.find(x=>x.y==2026);CW={cards:b.cards,np:j.cn.model.npr['2026']};draw()}).catch(()=>{});
addEventListener('load',()=>setTimeout(()=>{const o=window.redraw;window.redraw=()=>{o&&o();draw()}},0));
})();
