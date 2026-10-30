/* hdd.js — HDD 五页的图（数据 window.HDDQ 由 hdd/build.py 写进页面；只画 main 里看得见的图，跳过 #ch-shadow）。 */
(function(){
var Q=window.HDDQ;if(!Q||!window.echarts)return;
var charts=[];
function mk(id,opt){var el=document.getElementById(id);if(!el||el.closest('#ch-shadow'))return;var c=echarts.init(el,null,{renderer:'svg'});c.setOption(opt);charts.push(c);}
var sm=window.matchMedia&&window.matchMedia('(max-width:600px)').matches;
var base={tooltip:{trigger:'axis'},legend:{top:0},grid:{left:44,right:sm?40:52,top:36,bottom:30,containLabel:false}};
function q(e){return e.slice(0,7);}
// 横轴只在每年第一个季度标年份（手机上隔一年标一次），避免标签挤在一起
function xa(arr){var cats=arr.map(function(r){return q(r.end);}),show={},last='',k=0;
 cats.forEach(function(c,i){var y=c.slice(0,4);if(y!==last){if(!sm||k%2===0)show[i]=1;last=y;k++;}});
 return{type:'category',data:cats,axisTick:{alignWithLabel:true,interval:function(i){return !!show[i];}},
  axisLabel:{interval:function(i){return !!show[i];},formatter:function(v){return v.slice(0,4);},hideOverlap:true}};}
function gmOpt(){var w={};Q.wdc.forEach(function(r){w[r.end]=r.gm;});
 return Object.assign({},base,{xAxis:xa(Q.stx),
  yAxis:{type:'value',name:'%',min:0,max:70},
  series:[{name:'希捷',type:'line',showSymbol:false,data:Q.stx.map(function(r){return r.gm;}),markLine:{symbol:'none',label:{formatter:'上一轮顶 {c}%',position:'insideStartTop'},data:[{yAxis:Q.pk}]}},
          {name:'西数',type:'line',showSymbol:false,connectNulls:false,data:Q.stx.map(function(r){return w[r.end]!==undefined?w[r.end]:null;})}]});}
mk('c-ov',gmOpt());
mk('c-gm',Object.assign({},base,{xAxis:xa(Q.stx),
  yAxis:[{type:'value',name:'收入 百万美元'},{type:'value',name:'毛利率 %',min:0,max:70,splitLine:{show:false}}],
  series:[{name:'收入',type:'bar',data:Q.stx.map(function(r){return r.rev;})},{name:'毛利率',type:'line',yAxisIndex:1,showSymbol:false,data:Q.stx.map(function(r){return r.gm;})}]}));
mk('c-tb',Object.assign({},base,{xAxis:xa(Q.eb),
  yAxis:[{type:'value',name:'美元 / TB',min:10},{type:'value',name:'EB',splitLine:{show:false}}],
  series:[{name:'出货 EB',type:'bar',yAxisIndex:1,itemStyle:{opacity:.45},data:Q.eb.map(function(r){return r.eb;})},
          {name:'公司披露 $/TB',type:'line',lineStyle:{type:'dashed'},connectNulls:true,data:Q.eb.map(function(r){return r.px||null;})},
          {name:'总收入 ÷ EB（估）',type:'line',showSymbol:false,data:Q.eb.map(function(r){return r.rev_per_tb;})}]}));
var t;window.addEventListener('resize',function(){clearTimeout(t);t=setTimeout(function(){charts.forEach(function(c){c.resize();});},120);});
document.addEventListener('toggle',function(){charts.forEach(function(c){c.resize();});},true);
})();
