/* reading.js — 阅读模式（body.article）的交互，模板说明见 docs/READING_MODE.md。
   1) 来源脚注：JS 后渲染的行内「源N」标签也转成上标；点上标弹出来源摘要（手机底部抽屉），可跳到文末「来源与注释」。
   2) 顶部细进度条 + 当前章节名；点开是目录抽屉；宽屏（≥1180px）目录常驻左侧。
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
  fnify(document);
  var pend=false,mo=new MutationObserver(function(){if(pend)return;pend=true;requestAnimationFrame(function(){pend=false;mo.disconnect();fnify(document);watch()})});
  function watch(){mo.observe($('main'),{childList:true,subtree:true})}
  watch();

  var sheet=$('#fnSheet'),body=$('#fnBody'),last=null;
  function close(){if(!sheet)return;sheet.hidden=true;if(last){last.classList.remove('on');last.focus({preventScroll:true})}}
  function open(a){
    var href=a.getAttribute('href'),n=a.textContent.replace(/\D/g,''),html;
    if(href.charAt(0)==='#'){
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
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){close();closeToc()}});

  /* ---------- 2. 进度条 + 目录 ---------- */
  var secs=$$('main section[data-toc]'),toc=$('#rdToc'),cur=$('#rdCur'),prog=$('#rdProg'),pct=$('#rdPct');
  if(!toc||!secs.length)return;
  toc.innerHTML=secs.map(function(s){var t=s.getAttribute('data-toc'),i=t.indexOf(' ');
    return '<a href="#'+s.id+'"><b>'+t.slice(0,i)+'</b><span>'+t.slice(i+1)+'</span></a>'}).join('');
  var links=$$('a',toc),k=-1;
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
      var t=secs[n].getAttribute('data-toc');cur.textContent=t;}
  }
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});
  addEventListener('resize',upd);upd();
})();
