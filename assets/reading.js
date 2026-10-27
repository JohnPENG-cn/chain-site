/* reading.js — 阅读模式（body.article）的交互，模板说明见 docs/READING_MODE.md。
   1) 来源脚注：JS 后渲染的行内「源N」标签也转成上标；点上标弹出来源摘要（手机底部抽屉），可跳到文末「来源与注释」。
   2) 顶部细进度条 + 当前章节名；点开是目录抽屉；宽屏（≥1200px）目录常驻左侧。
      链条 5 页模板（tpl/page_v4.py）：#rdToc 是服务端写好的整站导航树，本页小节填进 #snHere；每段最多 1 个上标（body[data-fnmax]）；
      指向别的页的锚点按 window.CH_HOME 跳过去；来源在“底稿与数据”页，本页隐藏区有副本时照样弹摘要。
   3) 图表自适应：每张 ECharts 图用 ResizeObserver 跟着容器宽度重排（含「展开细节」里先隐藏后展开的图），
      并按图的实际宽度调标签：坐标轴文字放进画布、图例换行时自动下移绘图区、窄图隐藏折线数值标签、
      分类轴文字太挤时斜放、所有标签开启防重叠。各页画图代码不用改。
   不依赖其它脚本；页面没有 body.article 时什么都不做。 */
(function(){
  if(!document.body.classList.contains('article'))return;
  var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};

  /* ---------- 1. 脚注 ---------- */
  function fnify(root){
    $$('.tag.t-src',root).forEach(function(t){
      if(t.closest('.howto'))return;
      var links=t.tagName==='A'?[t]:$$('a',t);
      if(!links.length){t.classList.add('fn-txt');return}           // 纯文字来源（如“公司公告”）保留为灰色小字
      var sup=document.createElement('sup');sup.className='fn';
      links.forEach(function(a){var b=document.createElement('a');b.className='fn-a';b.href=a.getAttribute('href');
        var m=(a.textContent||'').match(/\d+/);b.textContent=m?m[0]:a.textContent;
        if(b.getAttribute('href').charAt(0)!=='#')b.title='另一页的来源 '+b.textContent;sup.appendChild(b)});
      var prev=t.previousSibling;if(prev&&prev.nodeType===3)prev.nodeValue=prev.nodeValue.replace(/\s+$/,'');
      t.replaceWith(sup)});
  }
  var FNMAX=document.body.getAttribute('data-fnmax')==='1',SRCP=document.body.getAttribute('data-src-page')||'';
  var BLK='p,li,dd,dt,td,th,figcaption,h1,h2,h3,h4,summary,blockquote';
  function limit(){   // 链条模板：每段只留第一个上标（一般是关键数字的来源），其余进本节末尾折叠的「本章来源」
    if(!FNMAX)return;var seen=new Map();
    $$('main sup.fn a.fn-a').forEach(function(a){
      if(a.closest('.src-line,.chsrc,.fn-sheet'))return;
      var b=a.closest(BLK)||a.closest('div');if(!b)return;
      if(!seen.has(b)){seen.set(b,1);return}
      var sup=a.parentNode,sec=a.closest('section'),n=a.textContent.replace(/\D/g,''),h=a.getAttribute('href');a.remove();if(!sup.querySelector('a'))sup.remove();
      if(!sec||!n)return;var box=sec.querySelector(':scope>.chsrc ol');
      if(!box){var d=document.createElement('details');d.className='more chsrc';d.innerHTML='<summary><span>来源</span><b>本章来源</b><small>每段只留 1 个上标，其余在这里</small></summary><div class="more-b"><ol></ol></div>';
        var pn=sec.querySelector(':scope>.pg-pn');sec.insertBefore(d,pn||null);box=d.querySelector('ol')}
      if(box.querySelector('[data-n="'+n+'"]'))return;
      var t=document.getElementById(h.slice(h.indexOf('#')+1)),li=document.createElement('li');li.setAttribute('data-n',n);
      var tx=t?t.textContent.replace(/\s+/g,' ').trim():'';if(tx.length>90)tx=tx.slice(0,88)+'…';
      li.innerHTML='<a href="'+h+'">'+n+'</a>';li.appendChild(document.createTextNode(tx));box.appendChild(li)});
  }
  fnify(document);limit();
  var pend=false,mo=new MutationObserver(function(){if(pend)return;pend=true;requestAnimationFrame(function(){pend=false;mo.disconnect();fnify(document);limit();watch()})});
  function watch(){mo.observe($('main'),{childList:true,subtree:true})}
  watch();

  var sheet=$('#fnSheet'),body=$('#fnBody'),last=null;
  function close(){if(!sheet)return;sheet.hidden=true;if(last){last.classList.remove('on');last.focus({preventScroll:true})}}
  function open(a){
    var href=a.getAttribute('href'),n=a.textContent.replace(/\D/g,''),html,hi=href.indexOf('#'),pg=hi>0?href.slice(0,hi):'';
    var li0=hi>=0&&document.getElementById(href.slice(hi+1));
    if(li0&&pg&&li0.closest('#ch-shadow')){   // 链条多页：来源表在“底稿与数据”页，本页隐藏区里有同一份 → 弹摘要，按钮去那一页
      var c0=li0.cloneNode(true),u0=c0.querySelector('a[href^="http"]');var url0=u0?u0.href:'';if(u0)u0.remove();
      html='<div class="fn-n">来源 '+n+'</div><p class="fn-t">'+c0.innerHTML.trim()+'</p><div class="fn-go">'+(url0?'<a href="'+url0+'" target="_blank" rel="noopener">打开原文 ↗</a>':'')+'<a href="'+href+'">在来源列表中查看 →</a></div>';
    }else if(href.charAt(0)==='#'){
      var li=document.getElementById(href.slice(1));
      if(li){var c=li.cloneNode(true),u=c.querySelector('a[href^="http"]');var url=u?u.href:'';if(u)u.remove();
        html='<div class="fn-n">来源 '+n+'</div><p class="fn-t">'+c.innerHTML.trim()+'</p><div class="fn-go">'+(url?'<a href="'+url+'" target="_blank" rel="noopener">打开原文 ↗</a>':'')+'<a href="'+href+'" data-jump>在来源列表中查看 ↓</a></div>';}
      else html='<div class="fn-n">来源 '+n+'</div><p class="fn-t">来源列表还在加载，稍后再点一次，或直接跳到文末。</p><div class="fn-go"><a href="'+href+'" data-jump>跳到来源 ↓</a></div>';
    }else{
      html='<div class="fn-n">来源 '+n+'（另一页）</div><p class="fn-t">这条来源在别的研究页的来源表里。</p><div class="fn-go"><a href="'+href+'">打开那一页的来源 '+n+' ↗</a></div>';
    }
    body.innerHTML=html;sheet.hidden=false;if(last)last.classList.remove('on');last=a;a.classList.add('on');
    var x=$('.fn-x',sheet);if(x)x.focus({preventScroll:true});
  }
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a.fn-a');
    if(a&&sheet&&!e.metaKey&&!e.ctrlKey){e.preventDefault();open(a);return}
    if(e.target.closest&&e.target.closest('[data-close]')){close();return}
    var j=e.target.closest&&e.target.closest('a[data-jump]');
    if(j){var id=j.getAttribute('href').slice(1),t=document.getElementById(id);close();
      if(t){var d=t.closest('details');if(d)d.open=true;$$('#src li.hl').forEach(function(x){x.classList.remove('hl')});t.classList.add('hl')}}
  });
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||a.classList.contains('fn-a')||a.hasAttribute('data-jump')||!window.CH_HOME)return;
    var id=decodeURIComponent(a.getAttribute('href').slice(1)),t=document.getElementById(id),pg=window.CH_HOME[id]||(/^src\d+$/.test(id)?SRCP:'');
    if((!t||t.closest('#ch-shadow'))&&pg&&pg!==window.CH_PAGE){e.preventDefault();e.stopPropagation();location.href=pg.indexOf('#')>-1?pg:pg+'#'+id}
  },true);
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){close();closeToc()}});

  /* ---------- 2. 进度条 + 目录 ---------- */
  var secs=$$('main section[data-toc]'),toc=$('#rdToc'),cur=$('#rdCur'),prog=$('#rdProg'),pct=$('#rdPct');
  if(!toc||!secs.length)return;
  var here=$('#snHere',toc),pname=document.body.getAttribute('data-page');
  var items=secs.map(function(s){var t=s.getAttribute('data-toc'),i=t.indexOf(' ');
    return '<a href="#'+s.id+'"><b>'+t.slice(0,i)+'</b><span>'+t.slice(i+1)+'</span></a>'}).join('');
  if(here)here.innerHTML=items;else toc.innerHTML=items;
  var links=$$('a',here||toc),k=-1;
  function closeToc(){toc.classList.remove('open')}
  cur.addEventListener('click',function(){toc.classList.toggle('open')});
  toc.addEventListener('click',function(e){if(e.target.closest('a'))closeToc()});
  document.addEventListener('click',function(e){if(toc.classList.contains('open')&&!e.target.closest('#rdToc')&&!e.target.closest('#rdCur'))closeToc()},true);
  var tick=false;
  function upd(){tick=false;
    var h=document.documentElement,max=h.scrollHeight-innerHeight,p=max>0?Math.min(1,Math.max(0,scrollY/max)):0;
    prog.style.transform='scaleX('+p.toFixed(4)+')';pct.textContent=Math.round(p*100)+'%';
    var n=0,lim=innerHeight*0.3;secs.forEach(function(s,i){if(s.getBoundingClientRect().top<lim)n=i});
    if(n!==k){k=n;links.forEach(function(a,i){a.classList.toggle('on',i===n)});
      var t=secs[n].getAttribute('data-toc');cur.textContent=here&&pname?pname+' · '+t.slice(t.indexOf(' ')+1):t;
      if(here&&links[n]&&toc.scrollHeight>toc.clientHeight&&getComputedStyle(toc).position==='fixed'){var r=links[n].getBoundingClientRect(),q=toc.getBoundingClientRect();if(r.top<q.top||r.bottom>q.bottom)toc.scrollTop+=r.top-q.top-q.height/2}}
  }
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});
  addEventListener('resize',upd);upd();
})();

/* ---------- 3. 图表自适应（ResizeObserver + 按宽度调标签） ---------- */
(function(){
  if(!document.body.classList.contains('article')||!window.echarts||!window.ResizeObserver)return;
  var main=document.querySelector('main');if(!main)return;
  var arr=function(x){return x==null?[]:Array.isArray(x)?x:[x]};
  var tw=function(t,fs){t=String(t==null?'':t);var w=0;for(var i=0;i<t.length;i++)w+=t.charCodeAt(i)>255?fs:fs*0.58;return w};
  var bg=function(){var v=getComputedStyle(document.body).getPropertyValue('--hig-card').trim()||getComputedStyle(document.body).backgroundColor;return v||'#fff'};
  /* 记住画图代码给的原始设置（只从调用参数里取，避免把自适应改过的值当成原值） */
  function remember(inst,o){var m=inst.__rdO||(inst.__rdO={series:{},grid:null,legendTop:null});
    if(!o||typeof o!=='object')return;
    if(o.grid)m.grid=arr(o.grid).map(function(g){return {left:g.left,right:g.right,top:g.top,bottom:g.bottom}});
    if(o.legend)arr(o.legend).forEach(function(l){if(l.top!=null)m.legendTop=l.top});
    arr(o.series).forEach(function(x,i){var k=x.name||i;m.series[k]={lab:!!(x.label&&x.label.show),pos:x.label&&x.label.position}});
  }
  function fit(inst,el){
    if(inst.isDisposed()||!el.clientWidth)return;
    var w=el.clientWidth,o=inst.getOption();if(!o)return;
    var m=inst.__rdO||{series:{},grid:null},narrow=w<520,mid=w<720,S=o.series||[];
    var cart=S.some(function(x){return x.type==='bar'||x.type==='line'||x.type==='scatter'});
    var hasBar=S.some(function(x){return x.type==='bar'});
    var p={series:S.map(function(x,i){var r={id:x.id,labelLayout:{hideOverlap:true}},k=x.name||i,orig=m.series[k];
      var on=orig?orig.lab:!!(x.label&&x.label.show);
      if(x.type==='line'&&hasBar&&on){            // 双轴：折线数值标签压在柱子上 → 加底色；窄图直接隐藏（看 tooltip）
        r.label=narrow?{show:false}:{show:true,backgroundColor:bg(),padding:[1,3],borderRadius:3,distance:6}}
      if(x.type==='bar'&&on&&narrow)r.label={fontSize:9};
      return r})};
    if(S.some(function(x){return x.type==='graph'})&&narrow)p.series.forEach(function(r,i){if(S[i].type==='graph')r.edgeLabel={show:false}});  // 关系图：窄屏只留节点名
    if(cart&&o.grid){
      var base=narrow?6:10,legH=0,L=(o.legend||[])[0];
      if(L&&L.show!==false){var fs=narrow?10:((L.textStyle&&L.textStyle.fontSize)||12),iw=narrow?12:(L.itemWidth||25),gap=narrow?8:(L.itemGap||10);
        var names=(L.data&&L.data.length?L.data:S.map(function(x){return x.name})).map(function(d){return typeof d==='object'?d.name:d}).filter(Boolean);
        var rowW=0,rows=names.length?1:0;names.forEach(function(n){var iwid=iw+5+tw(n,fs)+gap;if(rowW+iwid>w-26&&rowW>0){rows++;rowW=0}rowW+=iwid});
        legH=rows?5+rows*(Math.max(fs+2,14)+gap):0;p.legend={textStyle:{fontSize:fs},itemWidth:iw,itemGap:gap,left:'center',width:w-16}}
      var Y=o.yAxis||[],X=o.xAxis||[];
      var yNamed=Y.some(function(a){return a.name&&a.show!==false});
      var hBar=Y.some(function(a){return a.type==='category'});        // 横向柱：数值标签在右侧
      var rNeed=base;
      if(Y.length<2&&m.grid&&m.grid[0]&&typeof m.grid[0].right==='number')rNeed=Math.max(rNeed,Math.min(m.grid[0].right,60));
      if(hBar&&S.some(function(x){return x.type==='bar'&&x.label&&x.label.show}))rNeed=Math.max(rNeed,narrow?34:40);
      if(S.some(function(x){return x.markLine&&x.markLine.data&&x.markLine.data.length}))rNeed=Math.max(rNeed,44);
      X.forEach(function(a){if(a.name&&a.nameLocation!=='middle'&&a.nameLocation!=='center'&&a.nameLocation!=='start')rNeed=Math.max(rNeed,tw(a.name,12)+12)});
      p.grid=(o.grid||[]).map(function(g,i){var og=(m.grid&&m.grid[i])||g,t=typeof og.top==='number'?og.top:null;
        var r={containLabel:true,left:base,right:rNeed};
        if(t!=null){var need=(legH?legH+4:0)+(yNamed?28:6);r.top=Math.max(t,need)}
        return r});
      var lOut=hBar&&S.some(function(x){return x.type==='bar'&&x.label&&x.label.show&&(x.label.position==='left'||x.label.position==='outside')});  // 龙卷风图：左侧柱的数值标签要和分类名隔开
      p.yAxis=Y.map(function(a,i){var r={axisLabel:{hideOverlap:true},nameTextStyle:{align:a.position==='right'||(i>0&&a.position!=='left')?'right':'left'}};
        if(lOut&&a.type==='category')r.axisLabel.margin=narrow?40:48;
        if(a.type==='value'||a.type==='log')try{       // 顶/底刻度离上一格太近（如 max=1、间隔 0.3）→ 不画那一个
          var tk=inst.getModel().getComponent('yAxis',i).axis.scale.getTicks().map(function(t){return t.value});
          if(tk.length>3){var st=tk[2]-tk[1];if(tk[tk.length-1]-tk[tk.length-2]<st*0.6)r.axisLabel.showMaxLabel=false;if(tk[1]-tk[0]<st*0.6)r.axisLabel.showMinLabel=false}}catch(e){}
        return r});
      p.xAxis=X.map(function(a){var r={axisLabel:{}};
        if(a.type!=='category'||a.boundaryGap===false){r.axisLabel.alignMinLabel='left';r.axisLabel.alignMaxLabel='right'}
        if(a.type!=='category')r.axisLabel.hideOverlap=true;
        if(a.type==='category'&&a.data&&a.data.length){var fs=(a.axisLabel&&a.axisLabel.fontSize)||12,each=(w-40)/a.data.length,long=0;
          a.data.forEach(function(d){long=Math.max(long,tw(typeof d==='object'?d.value:d,fs))});
          if(long>each-6){
            if(each>=30){r.axisLabel.width=Math.floor(each-4);r.axisLabel.overflow='break';r.axisLabel.lineHeight=fs+2;r.axisLabel.rotate=0;r.axisLabel.interval=0}  // 分类名折行，不斜放
            else{r.axisLabel.rotate=45;r.axisLabel.width=null;r.axisLabel.overflow='none';r.grid0Left=Math.ceil(long*0.71)}}
          else{r.axisLabel.rotate=0;r.axisLabel.width=null}}
        return r});
      p.xAxis.forEach(function(r){if(r.grid0Left){p.grid[0].left=Math.max(p.grid[0].left,r.grid0Left);delete r.grid0Left}});
    }
    inst.__rdBusy=true;try{inst.__rdSo.call(inst,p)}finally{inst.__rdBusy=false}
  }
  var ro=new ResizeObserver(function(es){es.forEach(function(e){var el=e.target,inst=echarts.getInstanceByDom(el);if(!inst||inst.isDisposed())return;
    var w=Math.round(e.contentRect.width),h=Math.round(e.contentRect.height);if(!w||(el.__rdW===w&&el.__rdH===h))return;el.__rdW=w;el.__rdH=h;
    inst.resize();fit(inst,el)})});
  function adopt(el){var inst=echarts.getInstanceByDom(el);if(!inst||inst.__rdSo)return;
    var so=inst.setOption;inst.__rdSo=so;
    inst.setOption=function(o){var r=so.apply(inst,arguments);if(!inst.__rdBusy){remember(inst,o);clearTimeout(inst.__rdT);inst.__rdT=setTimeout(function(){fit(inst,el)},0)}return r};
    var o=inst.getOption();if(o)remember(inst,{grid:o.grid,series:o.series,legend:o.legend});
    el.__rdW=0;ro.observe(el);fit(inst,el)}
  function scan(){[].forEach.call(main.querySelectorAll('[_echarts_instance_]'),adopt)}
  var t=0;new MutationObserver(function(){clearTimeout(t);t=setTimeout(scan,30)}).observe(main,{subtree:true,childList:true,attributes:true,attributeFilter:['_echarts_instance_']});
  scan();
})();
