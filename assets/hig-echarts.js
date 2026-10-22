/* hig-echarts.js — 全站 ECharts 主题（与 assets/hig.css 同一套 Apple 系统色）。放在 vendor/echarts.min.js 之后加载。
   1) 注册 hig-light / hig-dark 两个主题，echarts.init(dom) 不指定主题时按当前深浅色自动套用；
   2) 各页图表代码里写死的旧配色（#d9534f 红、#5b8def 蓝 …）在 setOption 时映射成对应的系统色，图表代码与数据都不用改。 */
(function(){
if(!window.echarts||echarts.__hig)return;echarts.__hig=1;
var FONT='-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif';
var P={light:{blue:'#007AFF',orange:'#FF9500',green:'#34C759',red:'#FF3B30',purple:'#AF52DE',teal:'#30B0C7',indigo:'#5856D6',pink:'#FF2D55',yellow:'#FFCC00',gray:'#8E8E93',gray3:'#C7C7CC',blue2:'#99C9FF',label:'#000000',label2:'#6E6E73',sep:'rgba(60,60,67,.18)',tip:'rgba(255,255,255,.96)'},
       dark:{blue:'#0A84FF',orange:'#FF9F0A',green:'#30D158',red:'#FF453A',purple:'#BF5AF2',teal:'#40C8E0',indigo:'#5E5CE6',pink:'#FF375F',yellow:'#FFD60A',gray:'#8E8E93',gray3:'#48484A',blue2:'#3A6EA5',label:'#FFFFFF',label2:'#98989D',sep:'rgba(84,84,88,.65)',tip:'rgba(44,44,46,.96)'}};
function theme(c){var ax={axisLine:{lineStyle:{color:c.sep}},axisTick:{lineStyle:{color:c.sep}},axisLabel:{color:c.label2},splitLine:{lineStyle:{color:c.sep}},nameTextStyle:{color:c.label2}};
 return{color:[c.blue,c.orange,c.green,c.red,c.purple,c.teal,c.indigo,c.pink,c.yellow,c.gray],backgroundColor:'transparent',
  textStyle:{fontFamily:FONT,color:c.label},title:{textStyle:{color:c.label,fontWeight:600},subtextStyle:{color:c.label2}},
  legend:{textStyle:{color:c.label2},icon:'roundRect'},
  tooltip:{backgroundColor:c.tip,borderColor:c.sep,borderWidth:.5,textStyle:{color:c.label,fontFamily:FONT},extraCssText:'border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.12);'},
  categoryAxis:ax,valueAxis:ax,timeAxis:ax,logAxis:ax,
  line:{symbolSize:5,lineStyle:{width:2}},bar:{itemStyle:{borderRadius:[3,3,0,0]}},
  markLine:{lineStyle:{color:c.label2}}}}
echarts.registerTheme('hig-light',theme(P.light));echarts.registerTheme('hig-dark',theme(P.dark));
function dark(){var t=document.documentElement.dataset.t;return t?t=='dark':!!(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)}
/* 旧配色 → 系统色 */
var MAP={'#d9534f':'red','#d64541':'red','#c0392b':'red','#e74c3c':'red','#d6303a':'red','#ff6b5b':'red',
 '#5b8def':'blue','#2f6fde':'blue','#1f4e79':'blue','#6ea2ff':'blue','#7fb0e0':'blue',
 '#ff9900':'orange','#e08a20':'orange','#e0a030':'orange','#d98b00':'orange','#ff9800':'orange','#f0b35a':'orange','#a86400':'orange',
 '#8a5cf6':'purple','#26a69a':'teal','#2e8b57':'green','#1a9a5a':'green','#9ccc65':'green',
 '#9e9e9e':'gray','#9aa5b1':'gray','#888':'label2','#888888':'label2','#999':'label2','#6b6b6b':'label2','#bcc6d6':'gray3','#8fa8d8':'blue2',
 '#9a9a9a':'gray','#cfd8dc':'gray3','#ccc':'gray3','#b0bec5':'gray3','#90a4ae':'gray','#7a869a':'gray','#e57373':'red','#f0a8a6':'red','#66bb6a':'green',
 '#333':'label','#444':'label','#222':'label','#1a1a1a':'label','#eee':'sep','#e6e2da':'sep','#2c2d31':'sep','#2a2a2a':'sep'};
function remap(o,c,d){if(!o||d>14)return o;if(Array.isArray(o)){for(var i=0;i<o.length;i++){var v=o[i];if(typeof v=='string'){var k=MAP[v.toLowerCase()];if(k)o[i]=c[k]}else if(v&&typeof v=='object')remap(v,c,d+1)}return o}
 if(typeof o=='object'&&!(o instanceof Node)){for(var p in o){if(!Object.prototype.hasOwnProperty.call(o,p))continue;var x=o[p];if(typeof x=='string'){var m=MAP[x.toLowerCase()];if(m)o[p]=c[m]}else if(x&&typeof x=='object')remap(x,c,d+1)}}return o}
var init=echarts.init;
echarts.init=function(dom,th,opts){var dk=dark(),inst=init.call(echarts,dom,th==null?(dk?'hig-dark':'hig-light'):th,opts),so=inst.setOption;
 inst.setOption=function(o){if(o&&typeof o=='object')remap(o,dk?P.dark:P.light,0);return so.apply(inst,arguments)};return inst};
window.HIG_CHART={palette:function(){return P[dark()?'dark':'light']},dark:dark};
})();
