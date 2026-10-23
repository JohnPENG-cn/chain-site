/* pcb_fin.js — PCB 页 v0.3 财报图（数据由 pcb/page.py 从 pcb_data/filings.json、top5.json 写进 window.PCBFIN；口径见页内说明）。 */
(function(){const D=window.PCBFIN;if(!D||!window.echarts)return;const $=id=>document.getElementById(id);
const mob=()=>innerWidth<700,G=()=>({left:mob()?40:52,right:mob()?40:56,top:46,bottom:28,containLabel:false});
function cap(){if(!$('fin-cCap'))return;const c=CH.C('fin-cCap'),A=D.agg;
 c.setOption({tooltip:{trigger:'axis'},legend:{top:0,itemWidth:12,textStyle:{fontSize:11}},grid:G(),
  xAxis:{type:'category',data:D.yrs.map(y=>y=='2026H1'?'26H1':y.slice(2)),axisLabel:{fontSize:11}},
  yAxis:[{type:'value',name:'亿元',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11}},{type:'value',name:'倍',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11},splitLine:{show:false}}],
  series:[{name:'资本开支',type:'bar',data:A.capex,itemStyle:{color:'#5b8def'}},{name:'折旧',type:'bar',data:A.dep,itemStyle:{color:'#999'}},
   {name:'在建工程',type:'line',data:A.cip,symbolSize:5,itemStyle:{color:'#e08a20'}},
   {name:'资本开支÷折旧',type:'line',yAxisIndex:1,data:A.ratio,symbolSize:6,lineStyle:{width:3},itemStyle:{color:'#d9534f'},label:{show:!mob(),fontSize:10,formatter:p=>p.value}}]})}
function roic(){if(!$('fin-cRoic'))return;const c=CH.C('fin-cRoic'),C={'板厂':'#5b8def','覆铜板':'#3aa','上游':'#e08a20'};
 c.setOption({tooltip:{trigger:'axis'},legend:{top:0,textStyle:{fontSize:11}},grid:G(),xAxis:{type:'category',data:D.ry.map(y=>y.slice(2)),axisLabel:{fontSize:11}},
  yAxis:{type:'value',name:'ROIC 中位数 %',nameTextStyle:{fontSize:11},axisLabel:{fontSize:11}},
  series:Object.keys(D.roic).map(k=>({name:k,type:'line',data:D.roic[k],symbolSize:5,itemStyle:{color:C[k]},lineStyle:{width:k=='板厂'?3:2}}))})}
function gm(){if(!$('fin-cGm'))return;const c=CH.C('fin-cGm'),R=D.gm.slice().sort((a,b)=>a[2]-b[2]);
 c.setOption({tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},legend:{top:0,textStyle:{fontSize:11}},grid:{left:mob()?62:80,right:16,top:30,bottom:20},
  xAxis:{type:'value',axisLabel:{fontSize:11,formatter:'{value}%'}},yAxis:{type:'category',data:R.map(r=>r[0]),axisLabel:{fontSize:11}},
  series:[{name:'2025',type:'bar',data:R.map(r=>r[1]),itemStyle:{color:'#bbb'},barGap:'10%'},{name:'2026H1',type:'bar',data:R.map(r=>({value:r[2],itemStyle:{color:{'板厂':'#5b8def','覆铜板':'#3aa','上游':'#e08a20'}[r[3]]}}))}]})}
function top5(){if(!$('fin-cTop5'))return;const c=CH.C('fin-cTop5'),Y=[2021,2022,2023,2024,2025],K=['胜宏科技','沪电股份','生益电子','广合科技','鹏鼎控股','生益科技'];
 c.setOption({tooltip:{trigger:'axis'},legend:{top:0,itemWidth:12,textStyle:{fontSize:11}},grid:Object.assign(G(),{top:mob()?70:50}),xAxis:{type:'category',data:Y.map(String),axisLabel:{fontSize:11}},
  yAxis:{type:'value',max:100,axisLabel:{fontSize:11,formatter:'{value}%'}},series:K.map(k=>({name:k.slice(0,2),type:'line',connectNulls:false,symbolSize:5,data:Y.map(y=>D.top5[k]?.[y]??null)}))})}
function all(){cap();roic();gm();top5()}
all();
})();
