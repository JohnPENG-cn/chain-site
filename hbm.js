let M,charts={};const $=s=>document.querySelector(s);
const V=c=>getComputedStyle(document.documentElement).getPropertyValue(c).trim();
function base(){const d=isDark();return{textStyle:{fontFamily:'-apple-system,PingFang SC,sans-serif',color:V('--fg')},backgroundColor:'transparent',tooltip:{trigger:'axis',confine:true},grid:{left:44,right:14,top:40,bottom:30}}}
function C(id){if(charts[id])charts[id].dispose();charts[id]=echarts.init(document.getElementById(id),null,{renderer:'svg'});return charts[id]}
const vend=c=>/Blackwell|Rubin|H100|H200|Hopper/.test(c)?'英伟达':/TPU/.test(c)?'谷歌TPU':/Trainium/.test(c)?'AWS':/AMD/.test(c)?'AMD':'其他/中国';
const VC={'英伟达':'#76b900','谷歌TPU':'#4285f4','AWS':'#ff9900','AMD':'#ed1c24','其他/中国':'#9a9a9a'};
function calc(){const g=+$('#s1').value,u=+$('#s2').value/100,w=+$('#s3').value/100,k=+$('#s4').value/100;const r={};
 for(const y of[2025,2026,2027]){let d=M.demand.filter(x=>x.y==y).reduce((a,x)=>a+x.units*x.gb,0)/1000;
  let wf=Object.values(M.supply[y]).reduce((a,b)=>a+b,0),G=M.gbw[y],U=M.ut[y];
  if(y==2027){d*=k;wf*=w;G=g;U=u}r[y]={d,s:wf*12*G*U/1e6}}return r}
function drawBal(){const r=calc(),ys=[2025,2026,2027];o1.value=s1.value;o2.value=s2.value+'%';o3.value=s3.value+'%';o4.value=s4.value+'%';
 const x=r[2027],gp=(x.s-x.d)/x.d;$('#gap').textContent=(gp>0?'+':'')+(gp*100).toFixed(0)+'%';$('#hGap').textContent=$('#gap').textContent;
 $('#gapTxt').textContent=`需求 ${x.d.toFixed(2)} EB · 供给 ${x.s.toFixed(2)} EB → ${gp<-0.1?'明显短缺':gp<0?'略紧':'供给充足'}`;
 const c=C('cBal');c.setOption({...base(),legend:{top:0,textStyle:{color:V('--fg')}},xAxis:{data:ys.map(String)},yAxis:{name:'EB',splitLine:{lineStyle:{color:V('--line')}}},
 tooltip:{trigger:'axis',confine:true,formatter:p=>{const y=p[0].name,o=r[y];return`${y}<br>需求 ${o.d.toFixed(2)} EB<br>供给 ${o.s.toFixed(2)} EB<br>缺口 ${((o.s-o.d)/o.d*100).toFixed(1)}%`}},
 series:[{name:'需求',type:'bar',data:ys.map(y=>+r[y].d.toFixed(2)),itemStyle:{color:'#d9534f',borderRadius:[4,4,0,0]}},{name:'供给',type:'bar',data:ys.map(y=>+r[y].s.toFixed(2)),itemStyle:{color:'#5b8def',borderRadius:[4,4,0,0]},
 label:{show:true,position:'top',color:V('--fg'),formatter:p=>{const o=r[p.name];return((o.s-o.d)/o.d*100).toFixed(0)+'%'}}}]})}
function resetS(){s1.value=600;s2.value=90;s3.value=100;s4.value=100;drawBal()}
function drawMix(){const ys=[2023,2024,2025,2026,2027],ks=Object.keys(VC);const c=C('cMix');
 c.setOption({...base(),legend:{top:0,textStyle:{color:V('--fg')}},grid:{left:44,right:14,top:56,bottom:30},xAxis:{data:ys.map(String)},yAxis:{name:'EB',splitLine:{lineStyle:{color:V('--line')}}},
 tooltip:{trigger:'axis',confine:true,formatter:p=>{const y=+p[0].name;let s=y+' 需求明细（自估为主）<br>';M.demand.filter(x=>x.y==y).forEach(x=>s+=`${x.chip}: ${x.units}M×${x.gb}GB<br><span style="opacity:.6;font-size:11px">${x.src}</span><br>`);return s}},
 series:ks.map(k=>({name:k,type:'bar',stack:'a',itemStyle:{color:VC[k]},data:ys.map(y=>+(M.demand.filter(x=>x.y==y&&vend(x.chip)==k).reduce((a,x)=>a+x.units*x.gb,0)/1000).toFixed(2))}))})}
function drawMar(){const c=C('cMar');c.setOption({...base(),tooltip:{trigger:'axis',confine:true},legend:{top:0,textStyle:{color:V('--fg')}},xAxis:{data:['上一年同期','最新']},yAxis:{max:100,axisLabel:{formatter:'{value}%'},splitLine:{lineStyle:{color:V('--line')}}},
 series:[{name:'SK海力士 营业利润率(2Q25→2Q26)',type:'line',data:[41,76],label:{show:true,formatter:'{c}%'},lineStyle:{width:3},color:'#d9534f'},{name:'美光 毛利率(FQ4 25→26)',type:'line',data:[45.7,87.0],label:{show:true,formatter:'{c}%'},lineStyle:{width:3},color:'#ff9900'},{name:'台积电 营业利润率 2Q26',type:'line',data:[null,60.3],label:{show:true,formatter:'{c}%'},symbolSize:10,color:'#5b8def'}],grid:{left:44,right:20,top:80,bottom:30}})}
function drawShare(){const c=C('cShare');c.setOption({...base(),tooltip:{trigger:'item',formatter:'{b}: {c}%'},title:{text:'HBM 营收份额 2Q26',left:'center',textStyle:{color:V('--fg'),fontSize:14}},
 series:[{type:'pie',radius:['45%','72%'],top:20,label:{color:V('--fg'),formatter:'{b}\n{c}%'},data:[{name:'SK海力士',value:50,itemStyle:{color:'#d9534f'}},{name:'三星',value:33,itemStyle:{color:'#1428a0'}},{name:'美光',value:18,itemStyle:{color:'#ff9900'}}]}]})}
function drawTier(){const c=C('cTier'),t=['① 现金成本','② 维持老产能价','③ 吸引新建产能价','④ 短缺飞涨价'];
 c.setOption({...base(),tooltip:{trigger:'item',confine:true},grid:{left:10,right:10,top:20,bottom:40,containLabel:true},xAxis:{data:t,axisLabel:{interval:0,fontSize:11,width:80,overflow:'break'}},yAxis:{show:false,max:5},
 series:[{type:'bar',data:[1,2,3,4.4],barWidth:'70%',itemStyle:{color:p=>['#cfd8dc','#b0bec5','#90a4ae','#d9534f'][p.dataIndex],borderRadius:[4,4,0,0]},silent:true},
 {type:'scatter',symbolSize:16,data:[{value:[3,4.7],name:'普通DRAM：短缺暴涨'},{value:[1,1.7],name:'HBM 2026：合约锁低'},{value:[3,3.6],name:'HBM 2027：预期补涨'}],itemStyle:{color:V('--fg')},
 label:{show:true,position:'top',color:V('--fg'),fontSize:12,formatter:p=>p.name}}]})}
const NECK=[['DRAM 晶圆/洁净室','三家同时扩产，HBM 占投片升至 30% [源1]',36,'头号瓶颈'],['HBM4 良率/客户认证','海力士领先；三星约 80% [源8]；长鑫 25–30% [源22]',12,'决定份额'],['base die（台积电 12nm/3nm）','海力士、美光 HBM4E 靠台积电 [源8]',12,'与 CoWoS 共振'],['CoWoS','台积电 2026 年底 12–14 万片/月，2027 年底 19–20 万；缺口 20%→10% [源12,13]',15,'2027 缓解'],['TC 键合机','订单周期约 3–6 个月 [源17,18]',6,'最易缓解，非真瓶颈'],['混合键合','韩美二代开发中，主流 2029–30 [源19]',40,'下一代变量（不卡当前产量）']];
function drawNeck(){$('#neckList').innerHTML=NECK.map((n,i)=>`<div class="card"><div style="display:flex;justify-content:space-between;gap:8px"><b>${i+1}. ${n[0]}</b><span class="pill">${n[3]}</span></div><div class="note" style="margin:4px 0 8px">${n[1]}</div><div class="bar"><i style="width:${n[2]/40*100}%;${i>=4?'background:var(--mut)':''}"></i></div><div class="note">缓解约 ${n[2]>=36?(i==5?'3 年+':'24–36 个月'):n[2]==15?'至 2027 年':n[2]==6?'3–6 个月':'6–12 个月'}</div></div>`).join('')}
const TL1=[['2008–09','寒冬，奇梦达破产'],['2012','尔必达破产（2013 年被美光收购）→ 三家寡头'],['2017–18','超级周期：利润率新高、同时扩产'],['2019','价格腰斩'],['2022–23','再度亏损（海力士 2023 年亏损）→ HBM 救场'],['2026','普通 DRAM 短缺暴涨，美光毛利率 87% [源6]'],['2027H2?','新厂集中投产 → 本轮见顶风险']];
const TL2=[['2015','HBM（AMD Fiji）'],['2016–18','HBM2 / HBM2E'],['2022','HBM3（H100）：海力士翻身'],['2024','HBM3E（H200/B200）：三星掉队'],['2026','HBM4（Rubin）：三星追上，2Q26 份额 33% [源11]'],['2027','HBM4E：定制 base die，利润向最难环节迁移']];
const tl=(a,cls)=>a.map(x=>`<div class="${cls}"><span class="y">${x[0]}</span>　${x[1]}</div>`).join('');
const LEAD=[['韩国 1–10/1–20 日出口','每 10 天','领先三星/海力士营收 0–1 个月','10/1–10 半导体 122 亿美元 +170.9%；9 月存储出口 540.7 亿美元 +358.6%','20,21'],['DRAM 合约/现货价、HBM 合约','周/月','领先原厂毛利 1–2 季','2027 HBM 合约"数倍上涨"预期','1,3'],['原厂财报：售罄、资本开支','季度','领先供给 2–3 年','美光：2027 年大部分已签约；RPO 约 1500 亿美元','6'],['设备订单（韩美、韩华、ASMPT、Besi）','公告','领先 HBM 产能 3–9 个月','4.5 代 TCB 持续下单','17,18'],['台湾月营收（台积电、创意、弘塑、辛耘）','月','CoWoS/base die 产能','待接入','—'],['台积电 CoWoS 产能','季度','可装机 HBM 量','2027 年底 19–20 万片/月','12,13']];
const PRED=[['P1','10 月全月韩国半导体出口同比 > +150%','2026-11-01','产业通商部月报'],['P2','美光 FQ1 2027 营收 ≥ 600 亿美元（指引 615±15）','2026-12-20','美光财报'],['P3','SK 海力士 4Q26 财报会称 2027 HBM 基本售罄/签约完成','2027-01-31','财报会纪要'],['P4','2027 年 HBM 混合均价同比 ≥ +50%','2027-06-30','TrendForce'],['P5','2027 年底前混合键合不进入 HBM 大规模量产','2027-12-31','原厂/设备商公告'],['P6','韩国半导体出口同比在 2027-03 前首次跌破 +100%（见顶信号）','2027-04-01','月度出口数据']];
// network
const SEG=['HBM原厂','键合设备','base die/CoWoS','测试/检测','材料','国产封测/设备','下游加速器','资本方'];
const CO=[['SK海力士','000660.KS','KR',0,'HBM 份额 50%（2Q26）[源11]',30],['三星电子','005930.KS','KR',0,'HBM 份额 33%；自家 4nm base die [源8,11]',26],['美光','MU','US',0,'HBM 份额 18%；年底 10 万片/月 [源7,11]',22],['长鑫 CXMT','未上市','A',0,'良率 25–30%，仅供国内 [源22]',14],
['韩美半导体','042700.KS','KR',1,'TCB 主力供应商',16],['ASMPT','0522.HK','HK',1,'TCB',14],['Besi','BESI.AS','US',1,'混合键合',12],['快克智能','603203.SH','A',1,'TCB 0→1',10],['拓荆科技','688072.SH','A',1,'键合/薄膜设备',10],
['台积电','2330.TW','TW',2,'base die、CoWoS',24],['创意','3443.TW','TW',2,'ASIC/base die 设计',11],['弘塑','3131.TWO','TW',2,'先进封装湿制程',10],['辛耘','3583.TWO','TW',2,'先进封装设备',10],
['爱德万','6857.T','US',3,'存储测试机',12],['赛腾股份','603283.SH','A',3,'检测',10],
['雅克科技','002409.SZ','A',4,'前驱体',10],['华海诚科','688535.SH','A',4,'塑封料',10],['飞凯材料','300398.SZ','A',4,'临时键合材料',10],['鼎龙股份','300054.SZ','A',4,'临时键合材料',10],
['通富微电','002156.SZ','A',5,'封测',10],['长电科技','600584.SH','A',5,'封测',10],['北方华创','002371.SZ','A',5,'前道设备',10],['华海清科','688120.SH','A',5,'CMP/减薄',10],
['英伟达','NVDA','US',6,'2026 Blackwell ~545 万颗 [源14]',20],['谷歌 TPU','GOOGL','US',6,'2026/27 TPU 370/500 万颗 [源15]',16],['AWS','AMZN','US',6,'Trainium（自估）',12],['AMD','AMD','US',6,'MI355/MI450（自估）',12],
['SK Square','402340.KS','KR',7,'SK海力士最大股东',14],['韩国国民年金','—','KR',7,'持股 5% 以上',10]];
const LINKS=[['SK Square','SK海力士','持股 20.5%（2026-05-06）','23','cap'],['韩国国民年金','SK海力士','持股 8.1%（2025-12-31）','23','cap'],['美光','—','RPO 约 1500 亿美元（take-or-pay 长约）','6','cap'],['三星电子','—','3Q26 初步营业利润 107.4 万亿韩元','10','cap'],
['韩美半导体','SK海力士','TCB 订单 442 亿韩元（约 15 台）','17','ord'],['ASMPT','SK海力士','HBM4 TCB 订单','18','ord'],['台积电','SK海力士','base die 代工','8','ord'],['台积电','美光','HBM4E base die','8','ord'],
['SK海力士','英伟达','HBM 供货（行业公认，未单独编号）','公认','sup'],['三星电子','英伟达','HBM4 供货（行业公认）','公认','sup'],['美光','英伟达','HBM 供货（行业公认）','公认','sup'],['台积电','英伟达','CoWoS 封装 [源12]','12','sup']];
let mk='all';
function drawNet(){const dk=isDark(),cols=['#d9534f','#ff9900','#5b8def','#26a69a','#8a5cf6','#c0ca33','#76b900','#9e9e9e'];
 const vis=CO.filter(c=>mk=='all'||c[2]==mk||c[3]==6||c[3]==7&&mk=='KR');const names=new Set(vis.map(c=>c[0]));
 const nodes=SEG.map((s,i)=>({name:s,category:i,symbolSize:34,symbol:'roundRect',label:{show:true,fontWeight:'bold'},seg:1})).concat(vis.map(c=>({name:c[0],category:c[3],symbolSize:c[5],label:{show:true},co:c})));
 const links=vis.filter(c=>c[3]<7).map(c=>({source:SEG[c[3]],target:c[0],lineStyle:{color:dk?'#444':'#ccc',type:'dashed'},rel:'业务归属（报告标的表，营收占比未核实）',src:'报告'}))
 .concat(LINKS.filter(l=>names.has(l[0])&&(l[1]=='—'||names.has(l[1]))&&l[1]!='—').map(l=>({source:l[0],target:l[1],rel:l[2],src:l[3],lineStyle:{width:2.5,color:{cap:'#8a5cf6',ord:'#ff9900',sup:'#2e8b57'}[l[4]],curveness:.2},label:{show:innerWidth>700,formatter:l[2].slice(0,14),fontSize:10,color:V('--mut')}})));
 const c=C('cNet');c.setOption({backgroundColor:'transparent',tooltip:{confine:true,formatter:p=>p.dataType=='edge'?`${p.data.source} → ${p.data.target}<br>${p.data.rel}<br>来源：${p.data.src}`:p.data.co?`${p.name} ${p.data.co[1]}<br>${p.data.co[4]}`:p.name},
 legend:{data:SEG,top:0,textStyle:{color:V('--fg'),fontSize:11},itemWidth:10,itemHeight:10},
 series:[{type:'graph',layout:'force',roam:true,draggable:true,top:60,force:{repulsion:innerWidth<700?70:200,edgeLength:innerWidth<700?[30,80]:[40,110],gravity:innerWidth<700?.25:.12},categories:SEG.map((s,i)=>({name:s,itemStyle:{color:cols[i]}})),
 label:{color:V('--fg'),fontSize:11,position:'right'},edgeSymbol:['none','arrow'],edgeSymbolSize:6,data:nodes,links}]});
 c.off('click');c.on('click',p=>{if(p.dataType!='node')return;const n=p.name,co=CO.find(x=>x[0]==n);
  const rel=LINKS.filter(l=>l[0]==n||l[1]==n);$('#nodeInfo').innerHTML=`<b>${n}</b> ${co?`<span class="pill">${co[1]}</span><div class="note">${SEG[co[3]]} · ${co[4]}</div>`:'<div class="note">环节</div>'}`+
  (rel.length?'<table style="margin-top:8px">'+rel.map(l=>`<tr><td>${l[0]} → ${l[1]=='—'?'':l[1]}</td><td>${l[2]}</td><td>${/^\d/.test(l[3])?l[3].split(',').map(s=>`<a href="#src${s}">源${s}</a>`).join(' '):l[3]}</td></tr>`).join('')+'</table>':'')})}
function render(){drawBal();drawMix();drawMar();drawShare();drawTier();drawNet()}
window.redraw=render;
fetch('data/hbm.json').then(r=>r.json()).then(j=>{M=j;
 drawNeck();$('#tl1').innerHTML=tl(TL1,'');$('#tl2').innerHTML=tl(TL2,'h');
 $('#leadList').innerHTML=LEAD.map(l=>`<div class="card"><b>${l[0]}</b><div class="note">${l[1]} · ${l[2]}</div><p style="margin:.5em 0 0;font-size:15px">${l[3]} ${l[4]!='—'?`<span class="tag t-src">源${l[4]}</span>`:''}</p></div>`).join('');
 const now=new Date('2026-10-14');$('#predT tbody').innerHTML=PRED.map(p=>{const d=Math.round((new Date(p[2])-new Date())/864e5);return`<tr><td>${p[0]}</td><td>${p[1]}</td><td style="white-space:nowrap">${p[2]}<div class="note">${d>0?d+' 天后':'已到期'}</div></td><td>${p[3]}</td><td><span class="pill" style="color:var(--warn)">${d>0?'待验证':'待打分'}</span></td></tr>`}).join('');
 $('#coT tbody').innerHTML=CO.filter(c=>c[3]<7).map(c=>`<tr><td>${c[0]}</td><td style="white-space:nowrap">${c[1]}</td><td>${SEG[c[3]]}</td><td>${c[4]}</td></tr>`).join('');
 $('#srcL').innerHTML=M.sources.map(s=>`<li id="src${s.id}" value="${s.id}">${s.t} <a href="${s.u}" target="_blank" rel="noopener">${s.u}</a></li>`).join('');
 ['s1','s2','s3','s4'].forEach(i=>document.getElementById(i).addEventListener('input',drawBal));
 document.querySelectorAll('#fMk button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#fMk button').forEach(x=>x.classList.remove('on'));b.classList.add('on');mk=b.dataset.m;drawNet()});
 render()});
addEventListener('resize',()=>Object.values(charts).forEach(c=>c.resize()));
const secs=[...document.querySelectorAll('main section')],na=[...document.querySelectorAll('#nav a')];
addEventListener('scroll',()=>{let k=0;secs.forEach((s,i)=>{if(s.getBoundingClientRect().top<140)k=i});na.forEach(a=>a.classList.toggle('on',a.getAttribute('href')=='#'+secs[k].id));const on=na.find(a=>a.classList.contains('on'));if(on)on.scrollIntoView({block:'nearest',inline:'center'})},{passive:true});
