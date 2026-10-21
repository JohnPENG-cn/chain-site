/* hbm_x.js — HBM v0.3 增补（v0.4 参数更新）：要害变量龙卷风、关键玩家与博弈、反方证据。独立于 hbm.js（不改其逻辑），所有 id 带 hx- 前缀。 */
(function(){let M,X,CJ,tocDraw=null;
function gap(o){const y=2027,d0=M.demand.filter(x=>x.y==y).reduce((a,x)=>a+x.units*x.gb,0)/1000,wf=Object.values(M.supply[y]).reduce((a,b)=>a+b,0);
 const d=d0*(o.dem||1)*(o.gb||1),s=wf*(o.wf||1)*12*(o.g||M.gbw[y])*(o.u||M.ut[y])/1e6;return(s-d)/d}
function draw(){if(!M)return;const b=gap({}),R=[['每片有效 GB',{g:780},{g:980},'780','980','券商产量反推 880（源65）；HBM4E die 更大可能更低；估'],['DRAM 晶圆分给 HBM 的量',{wf:.9},{wf:1.1},'−10%','+10%','下：三星转产 DDR5（源65）；上：三星自报投片（源66）'],['稼动率',{u:.8},{u:.95},'80%','95%','估'],['加速器出货',{dem:.8},{dem:1.2},'−20%','+20%','估'],['每颗 HBM 容量',{gb:.8},{gb:1.1},'−20%（降规格）','+10%','KGI：英伟达下调规格 源55']]
 .map(a=>({n:a[0],lo:gap(a[1]),hi:gap(a[2]),l1:a[3],l2:a[4],src:a[5]}));
 CH.tornado('hx-cTor',b,R,{flip:0,flipLbl:'0：短缺消失'});if(CJ)CH.driver('hx-cDrv','#hx-drvT tbody',CJ.driver,{srcHref:'cowos.html#src'})}
Promise.all([fetch('data/hbm.json?v=8a4bbe97f9').then(r=>r.json()),fetch('data/hbm_x.json?v=364be12598').then(r=>r.json()),fetch('data/cowos.json?v=1f41496d73').then(r=>r.json()),fetch('data/toc.json?v=4dd7367735').then(r=>r.json())]).then(([m,x,cj,tj])=>{M=m;X=x;CJ=cj;tocDraw=TOC.render('hx','#hx-toc',cj,m,tj,{ledger:'#hx-tpred'});
 CH.$('#hx-torNote').textContent=X.tornado_note;CH.players('#hx-play',X.players);CH.falsify('#hx-falT tbody',X.falsify);draw()});
addEventListener('load',()=>setTimeout(()=>{const o=window.redraw;window.redraw=()=>{o&&o();draw();tocDraw&&tocDraw()}},0));
})();
