/* toc.js — 约束理论（TOC）推导：把每一环产能换成同一单位（AI 加速器封装，百万颗/季），取最小值 = 当季约束。
   HBM 页与 CoWoS 页共用；数据：data/cowos.json（需求、CoWoS 产能、每片颗数）+ data/hbm.json（HBM 季度投片、每片 GB）+ data/toc.json（其他环节参数与来源）。 */
const TOC={};
TOC.calc=(J,H,T,s={})=>{const k=x=>s[x]??1,m=J.model,P=T.param,Q=[],W=P.ramp,yrs=[2024,2025,2026,2027];
 const rows=y=>m.demand.filter(x=>x.y==y),U=y=>rows(y).reduce((a,x)=>a+x.units,0);
 const coef={};yrs.forEach(y=>{const R=rows(y),u=U(y);coef[y]={u,ppw:u/R.reduce((a,x)=>a+x.units/x.ppw,0),gb:R.reduce((a,x)=>a+x.units*x.gb,0)/u,
  weq:R.reduce((a,x)=>a+x.units*(/CPU/.test(x.chip)?P.pw_cpu:/TPU|AWS|ASIC/.test(x.v)?P.pw_asic:1),0)/u,stk:P.stack_gb[y]}});
 const hq=H.cap.q,hi=hq.indexOf('1Q24'),ci=m.cap.q.indexOf('2024Q1'),mk=['SK hynix','Samsung','Micron','CXMT'];
 const hk=i=>mk.reduce((a,n)=>a+(H.cap[n][hi+i]||0),0),h24=[0,1,2,3].reduce((a,i)=>a+hk(i),0);
 let B=P.tcb_b0;const out=[];
 for(let i=0;i<16;i++){const y=2024+Math.floor(i/4),qi=i%4,c=coef[y],w=W[qi];
  const D=c.u*w*k('dem');
  const ut=y==2024?m.ut:y==2025?m.ut:(s.cwut??0.95);
  const wf=3*(m.cap.tsmc[ci+i]+m.cap.osat[ci+i])*ut-m.other[y]/4;const cw=wf*c.ppw/1000*k('cw');
  const GB=y==2024?H.hist_supply[2024].s*1e9*hk(i)/h24:hk(i)*1000*3*H.gbw[y]*H.ut[y];const hbm=GB/c.gb/1e6*k('hbm');
  const B0=B;B+=P.tcb_add[y]*3*P.tcb_util/P.tcb_share;
  const tcb=B0*c.stk/c.gb/1e6;
  const sub=P.sub[y]*c.u*w*k('sub')/(y==2027?1:1);
  const pw=P.gw[i]*P.ai_share*1e6/P.kw_gpu/c.weq/1e6;
  out.push({q:y+'Q'+(qi+1),y,D,st:{cw,hbm,tcb,sub,pw},GB,wf,B:B0})}
 // 基板：2027 年 = 2026 年产能 × (1+KGI 增速)
 const s26=out.filter(o=>o.y==2026).reduce((a,o)=>a+o.st.sub/k('sub'),0);out.filter(o=>o.y==2027).forEach((o,j)=>o.st.sub=s26*P.sub27*W[j]*k('sub'));
 // 校准（估）：键合机、电力在 2024–26 年没有卡住出货（出货已发生 / HBM 页研究结论），按"历史最紧时仍有 10% 余量"反推规模系数；未来只看增速
 const hist=out.filter(o=>o.y<=P.cal_to);const fT=P.cal_slack*Math.max(...hist.map(o=>(o.st.hbm/k('hbm'))/o.st.tcb)),fP=P.cal_slack*Math.max(...hist.map(o=>(o.D/k('dem'))/o.st.pw));
 out.forEach(o=>{o.st.tcb*=fT*k('tcb');o.st.pw*=fP*k('pw')});TOC.cal={tcb:fT,pw:fP};
 out.forEach(o=>{let b=null,v=1e9;for(const n in o.st)if(o.st[n]<v){v=o.st[n];b=n}o.min=b;o.bind=v>=o.D?'dem':b;o.cap=v;o.thru=Math.min(o.D,v)});return{out,coef}};
if(typeof module!='undefined')module.exports=TOC;
/* 渲染：p = 页面前缀（cw / hx），host = 容器选择器 */
TOC.render=(p,host,J,H,T)=>{const f=t=>CH.srcInline(String(t).replace(/\{(\w+)\}/g,(m,a)=>T.srcmap[p][a]?`[源${T.srcmap[p][a]}]`:'')),id=x=>`${p}-t-${x}`,S=T.stages,N=Object.fromEntries(S.map(s=>[s.k,s]));N.dem={k:'dem',n:'需求（各环节都够）',c:'#7a869a'};
 const SL=[['dem','需求（相对 KGI 出货）',70,130,100],['cw','CoWoS 产能',70,130,100],['hbm','HBM 可供量（125 = TrendForce 口径）',70,140,100],['tcb','TC 键合机',50,150,100],['sub','ABF 载板',70,140,100],['pw','电力',50,150,100]];
 CH.$(host).innerHTML=`<div class="grid g2"><div class="card"><div class="ctl">${SL.map(s=>`<label>${s[1]} <output id="${id('o-'+s[0])}"></output></label><input type="range" id="${id(s[0])}" min="${s[2]}" max="${s[3]}" step="5" value="${s[4]}">`).join('')}
 <label>查看季度 <output id="${id('o-q')}"></output></label><input type="range" id="${id('q')}" min="0" max="15" step="1" value="11"></div><button class="btn" id="${id('rst')}">恢复基准</button>
 <div style="margin-top:12px"><div class="note">当季约束（木桶短板）</div><div class="big" style="font-size:28px" id="${id('bind')}"></div><div class="note" id="${id('bindTxt')}"></div></div></div>
 <div class="card"><b>所选季度：各环节可支撑的封装数（百万颗/季）</b><div id="${id('cBar')}" class="chart" style="height:300px"></div><div class="note">红色 = 最小值 = 约束；虚线 = 需求。条越长，余量越大。</div></div></div>
 <div class="card" style="margin-top:14px"><b>2024–2027 每季各环节产能（同一单位）与需求</b><div id="${id('cLine')}" class="chart" style="height:380px"></div><div class="note" id="${id('mig')}"></div></div>
 <h3>每一环怎么换算成同一单位</h3><div class="tbl"><table class="fal2"><thead><tr><th>环节</th><th>原始单位与来源</th><th>换算系数（单耗）</th><th>所选季度产能</th><th>利用率</th><th>余量</th></tr></thead><tbody id="${id('stT')}"></tbody></table></div>
 <div class="note">${T.gaps.map(f).join('<br>')}</div>
 <h3>缓冲（库存与预订）</h3><div class="tbl"><table><tbody>${T.buffers.map(b=>`<tr><td><b>${b[0]}</b></td><td>${f(b[1])}</td><td class="note">${b[2]}</td></tr>`).join('')}</tbody></table></div>
 <h3>TOC 五步，逐条落到这条链</h3><div class="tbl"><table><thead><tr><th>步骤</th><th>含义</th><th>这条链现在</th><th>盯什么</th></tr></thead><tbody>${T.steps.map(r=>`<tr><td style="white-space:nowrap"><b>${r[0]}</b></td><td>${r[1]}</td><td>${f(r[2])}</td><td class="note">${r[3]}</td></tr>`).join('')}</tbody></table></div>
 <h3>约束迁移预测（到期打分）</h3><p class="sub" id="${id('pSum')}"></p><div class="tbl"><table><thead><tr><th>#</th><th>预测</th><th>到期</th><th>验证来源</th><th>状态</th></tr></thead><tbody id="${id('pT')}"></tbody></table></div>
 <div class="tbl" style="margin-top:10px"><table class="fal"><thead><tr><th>判断</th><th>反方证据</th><th>证伪条件</th><th>观察指标与阈值</th><th>当前读数</th><th>状态</th></tr></thead><tbody id="${id('fT')}"></tbody></table></div>`;
 CH.ledger('#'+id('pT'),'#'+id('pSum'),T.preds);CH.falsify('#'+id('fT'),T.falsify.map(x=>({...x,counter:x.counter.replace(/\{(\w+)\}/g,(m,a)=>`[源${T.srcmap[p][a]}]`),now:x.now.replace(/\{(\w+)\}/g,(m,a)=>`[源${T.srcmap[p][a]}]`)})));
 const draw=()=>{const s={};SL.forEach(x=>{const v=+document.getElementById(id(x[0])).value;s[x[0]]=v/100;CH.$('#'+id('o-'+x[0])).textContent=v+'%'});
  const {out}=TOC.calc(J,H,T,s),qi=+document.getElementById(id('q')).value,o=out[qi];CH.$('#'+id('o-q')).textContent=o.q;
  CH.$('#'+id('bind')).textContent=N[o.bind].n;CH.$('#'+id('bind')).style.color=N[o.bind].c;
  CH.$('#'+id('bindTxt')).textContent=`${o.q}：需求 ${o.D.toFixed(2)}，${o.bind=='dem'?'最紧的 '+N[o.min].n+' 能支撑 '+o.cap.toFixed(2)+'，各环节都够，约束在市场需求':'约束环节只能支撑 '+o.cap.toFixed(2)+' 百万颗（满足 '+(o.cap/o.D*100).toFixed(0)+'%）'}`;
  const ks=S.map(x=>x.k).sort((a,b)=>o.st[a]-o.st[b]),c1=CH.C(id('cBar'));
  c1.setOption({...CH.base(),grid:{left:CH.mob()?100:120,right:30,top:26,bottom:26},tooltip:{trigger:'item',confine:true,formatter:q=>`${q.name}：${q.value} 百万颗/季`},xAxis:{type:'value',...CH.ax()},yAxis:{type:'category',inverse:true,data:ks.map(k=>N[k].n)},
   series:[{type:'bar',data:ks.map((k,i)=>({value:+o.st[k].toFixed(2),itemStyle:{color:i==0?'#d9534f':'#9aa5b1'}})),label:{show:true,position:'right',fontSize:11,color:CH.V('--fg')},markLine:{silent:true,symbol:'none',data:[{xAxis:+o.D.toFixed(2)}],lineStyle:{type:'dashed',color:CH.V('--fg')},label:{formatter:'需求',position:'start',color:CH.V('--fg')}}}]});
  const c2=CH.C(id('cLine'));c2.setOption({...CH.base(),legend:{top:0,textStyle:{color:CH.V('--fg'),fontSize:10},itemWidth:14,itemGap:6},grid:{left:40,right:12,top:CH.mob()?78:46,bottom:30},xAxis:{type:'category',data:out.map(x=>x.q),axisLabel:{interval:CH.mob()?3:1}},yAxis:{name:'百万颗/季',...CH.ax()},
   tooltip:{trigger:'axis',confine:true,formatter:q=>{const x=out[q[0].dataIndex];return`<b>${x.q}</b> 需求 ${x.D.toFixed(2)}<br>`+S.map(z=>`${z.k==x.bind?'▶ ':''}${z.n}：${x.st[z.k].toFixed(2)}`).join('<br>')}},
   series:[{name:'需求',type:'bar',data:out.map(x=>+x.D.toFixed(2)),itemStyle:{color:CH.V('--line')},barWidth:'60%'}].concat(S.map(z=>({name:z.n,type:'line',showSymbol:false,data:out.map(x=>+x.st[z.k].toFixed(2)),color:z.c,lineStyle:{width:z.k==o.bind?3:1.6}})))
   .concat([{name:'约束',type:'scatter',symbolSize:9,data:out.map(x=>({value:+x.cap.toFixed(2),itemStyle:{color:N[x.bind].c,borderColor:'#000',borderWidth:1}})),tooltip:{show:false}}])});
  const seg=[];out.forEach(x=>{const l=seg[seg.length-1];if(l&&l.b==x.bind)l.e=x.q;else seg.push({b:x.bind,s:x.q,e:x.q})});
  CH.$('#'+id('mig')).innerHTML='<b>约束迁移（模型）：</b>'+seg.map(g=>`${N[g.b].n}（${g.s}${g.e!=g.s?'–'+g.e:''}）`).join(' → ')+'。黑边圆点 = 当季最小值。所有非 CoWoS/HBM 环节的规模都是估计，拖滑块看结论怎么变。';
  CH.$('#'+id('stT')).innerHTML=S.map(z=>{const cap=o.st[z.k],u=o.thru/cap,sl=cap/o.thru-1;return`<tr><td><b style="color:${z.c}">${z.n}</b>${z.k==o.bind?' <span class="pill" style="color:var(--acc)">约束</span>':''}</td><td>${f(z.native)}</td><td>${f(z.conv)}</td><td>${cap.toFixed(2)}</td><td>${(u*100).toFixed(0)}%</td><td>${z.k==o.bind?'0（约束）':(sl>=0?'+':'')+(sl*100).toFixed(0)+'%'}</td></tr>`}).join('')};
 SL.concat([['q']]).forEach(x=>document.getElementById(id(x[0])).addEventListener('input',draw));
 document.getElementById(id('rst')).onclick=()=>{SL.forEach(x=>document.getElementById(id(x[0])).value=x[4]);document.getElementById(id('q')).value=11;draw()};
 draw();return draw};
