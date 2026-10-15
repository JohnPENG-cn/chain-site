/* hbm_x.js — HBM v0.3 增补：要害变量龙卷风、关键玩家与博弈、反方证据。独立于 hbm.js（不改其逻辑），所有 id 带 hx- 前缀。 */
(function(){let M,X,tocDraw=null;
function gap(o){const y=2027,d0=M.demand.filter(x=>x.y==y).reduce((a,x)=>a+x.units*x.gb,0)/1000,wf=Object.values(M.supply[y]).reduce((a,b)=>a+b,0);
 const d=d0*(o.dem||1)*(o.gb||1),s=wf*(o.wf||1)*12*(o.g||M.gbw[y])*(o.u||M.ut[y])/1e6;return(s-d)/d}
function draw(){if(!M)return;const b=gap({}),R=[['每片有效 GB',{g:500},{g:700},'500','700','TrendForce 良率/die 口径 源9,25；估'],['DRAM 晶圆分给 HBM 的量',{wf:.8},{wf:1.2},'−20%','+20%','HBM 约占 DRAM 产出 15% 源43；估'],['稼动率',{u:.8},{u:.95},'80%','95%','估'],['加速器出货',{dem:.8},{dem:1.2},'−20%','+20%','估'],['每颗 HBM 容量',{gb:.8},{gb:1.1},'−20%（降规格）','+10%','KGI：英伟达下调规格 源55']]
 .map(a=>({n:a[0],lo:gap(a[1]),hi:gap(a[2]),l1:a[3],l2:a[4],src:a[5]}));
 CH.tornado('hx-cTor',b,R,{flip:0,flipLbl:'0：短缺消失'})}
Promise.all([fetch('data/hbm.json').then(r=>r.json()),fetch('data/hbm_x.json').then(r=>r.json()),fetch('data/cowos.json').then(r=>r.json()),fetch('data/toc.json').then(r=>r.json())]).then(([m,x,cj,tj])=>{M=m;X=x;tocDraw=TOC.render('hx','#hx-toc',cj,m,tj);
 CH.$('#hx-torNote').textContent=X.tornado_note;CH.players('#hx-play',X.players);CH.falsify('#hx-falT tbody',X.falsify);draw()});
addEventListener('load',()=>setTimeout(()=>{const o=window.redraw;window.redraw=()=>{o&&o();draw();tocDraw&&tocDraw()}},0));
})();
