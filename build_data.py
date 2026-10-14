# Regenerates data/*.json. Token read from ~/.config/tushare/token via tsq; never written out.
import sys,json,datetime,re,time
sys.path.insert(0,'/workspace/daily_report'); from tsq import q
import akshare as ak, pandas as pd
CH={'AI算力':[('上游','晶圆代工',{'688981.SH':'中芯国际','688347.SH':'华虹公司'}),
 ('上游','HBM存储',{'603986.SH':'兆易创新','688525.SH':'佰维存储','301308.SZ':'江波龙'}),
 ('中游','先进封装',{'600584.SH':'长电科技','002156.SZ':'通富微电','002185.SZ':'华天科技'}),
 ('中游','PCB载板',{'002463.SZ':'沪电股份','300476.SZ':'胜宏科技','002916.SZ':'深南电路','002436.SZ':'兴森科技'}),
 ('中游','光模块',{'300308.SZ':'中际旭创','300502.SZ':'新易盛','300394.SZ':'天孚通信'}),
 ('中游','铜缆连接',{'002130.SZ':'沃尔核材','300913.SZ':'兆龙互连','688629.SH':'华丰科技'}),
 ('下游','服务器整机',{'601138.SH':'工业富联','000977.SZ':'浪潮信息','603019.SH':'中科曙光'}),
 ('下游','液冷电源',{'002837.SZ':'英维克','300870.SZ':'欧陆通','002851.SZ':'麦格米特'})],
 '铜':[('上游','铜矿',{'601899.SH':'紫金矿业','603993.SH':'洛阳钼业','601168.SH':'西部矿业'}),
 ('中游','冶炼',{'600362.SH':'江西铜业','000878.SZ':'云南铜业','000630.SZ':'铜陵有色'}),
 ('中游','铜材加工',{'601137.SH':'博威合金','002171.SZ':'楚江新材','601609.SH':'金田股份'}),
 ('下游','电网电力',{'600406.SH':'国电南瑞','600089.SH':'特变电工','601179.SH':'中国西电'}),
 ('下游','新能源车',{'002594.SZ':'比亚迪','300750.SZ':'宁德时代','601127.SH':'赛力斯'}),
 ('下游','AI数据中心',{'601138.SH':'工业富联','002837.SZ':'英维克','002130.SZ':'沃尔核材'})]}
KW={'晶圆代工':['晶圆','代工','中芯','华虹','台积电','制程'],'HBM存储':['HBM','存储','DRAM','NAND','内存','美光','海力士'],
 '先进封装':['封装','CoWoS','封测','Chiplet'],'PCB载板':['PCB','载板','覆铜板'],'光模块':['光模块','CPO','光通信','1.6T','800G'],
 '铜缆连接':['铜缆','高速连接','连接器'],'服务器整机':['服务器','英伟达','GB300','GB200','算力','智算'],'液冷电源':['液冷','电源','数据中心'],
 '铜矿':['铜矿','矿山','紫金','洛阳钼业'],'冶炼':['冶炼','加工费','精炼铜','沪铜','铜价','LME'],'铜材加工':['铜箔','铜材','铜板带'],
 '电网电力':['电网','特高压','变压器','国家电网'],'新能源车':['新能源车','电动车','比亚迪','宁德','锂电'],'AI数据中心':['数据中心','IDC','AIDC']}
POS=['增长','上涨','涨停','超预期','中标','签约','突破','创新高','回购','增持','大涨','扩产','提价']
NEG=['下跌','跌停','亏损','减持','下滑','暴跌','处罚','立案','低于预期','下调','风险']
def tone(t):
    p=sum(w in t for w in POS); n=sum(w in t for w in NEG); return '利好' if p>n else '利空' if n>p else '中性'
def tag(t):
    return [(c,nd) for c,ns in CH.items() for _,nd,_s in ns if any(k.lower() in t.lower() for k in KW[nd])]
def dump(n,o): json.dump(o,open(f'data/{n}.json','w'),ensure_ascii=False,default=str)
today=datetime.date.today().strftime('%Y%m%d')
cal=q('trade_cal',exchange='SSE',start_date='20260701',end_date=today,is_open='1').sort_values('cal_date')
dates=list(cal.cal_date)[-22:]
allc={c for ns in CH.values() for *_,s in ns for c in s}
px={}
for d in dates:
    df=q('daily',trade_date=d,fields='ts_code,close,pct_chg,amount')
    if len(df)==0: continue
    px[d]=df[df.ts_code.isin(allc)].set_index('ts_code')
dates=sorted(px); last=dates[-1]
def ret(c,k):
    try: return round((px[last].close[c]/px[dates[-1-k]].close[c]-1)*100,2)
    except Exception: return None
db=q('daily_basic',trade_date=last,fields='ts_code,total_mv').set_index('ts_code').total_mv
try: mf=q('moneyflow',trade_date=last); mf=mf.set_index('ts_code'); mf=((mf.buy_lg_amount+mf.buy_elg_amount-mf.sell_lg_amount-mf.sell_elg_amount)/1e4)
except Exception as e: print('moneyflow fail',e); mf=pd.Series(dtype=float)
# news
news=[]
try:
    cls=ak.stock_info_global_cls(symbol='全部')
    for _,r in cls.iterrows():
        t=f"{r.get('标题','')} {r.get('内容','')}"
        news.append({'title':(r.get('标题') or str(r.get('内容',''))[:60]),'time':f"{r.get('发布日期','')} {r.get('发布时间','')}",'src':'财联社电报','url':'https://www.cls.cn/telegraph','tags':tag(t),'tone':tone(t)})
except Exception as e: print('cls fail',e)
names={c:n for ns in CH.values() for *_,s in ns for c,n in s.items()}
for c,n in names.items():
    try:
        ne=ak.stock_news_em(symbol=c[:6]).head(5)
        for _,r in ne.iterrows():
            t=r['新闻标题']; tg=tag(t)+[(ch,nd) for ch,ns in CH.items() for _,nd,s in ns if c in s]
            news.append({'title':t,'time':str(r['发布时间']),'src':r.get('文章来源','东方财富'),'url':r['新闻链接'],'tags':sorted(set(map(tuple,tg))),'tone':tone(t),'stock':n})
        time.sleep(0.3)
    except Exception as e: print('news fail',c,e)
seen=set(); news=[x for x in sorted(news,key=lambda x:x['time'],reverse=True) if not (x['title'] in seen or seen.add(x['title']))]
chains={}
for ch,ns in CH.items():
    out=[]
    for lvl,nd,s in ns:
        st=[{'code':c,'name':n,'close':float(px[last].close.get(c,float('nan'))),'d1':ret(c,1),'d5':ret(c,5),'d20':ret(c,20),
             'mv':round(float(db.get(c,0) or 0)/1e4,1),'mf':round(float(mf.get(c)),2) if c in mf.index else None} for c,n in s.items()]
        avg=lambda k:round(sum(x[k] for x in st if x[k] is not None)/max(1,sum(x[k] is not None for x in st)),2)
        out.append({'level':lvl,'node':nd,'stocks':st,'d1':avg('d1'),'d5':avg('d5'),'d20':avg('d20'),
          'mf':round(sum(x['mf'] or 0 for x in st),2) if len(mf) else None,'news':sum((ch,nd) in [tuple(t) for t in x['tags']] for x in news)})
    chains[ch]=out
dump('chains',{'date':last,'chains':chains}); dump('news',{'date':last,'items':news[:300]})
ind={'date':last}
cu=ak.futures_zh_daily_sina(symbol='CU0').tail(120); ind['cu0']=cu[['date','close']].astype(str).values.tolist()
etf={'512480.SH':'半导体ETF','515880.SH':'通信ETF','512400.SH':'有色ETF','159611.SZ':'电力ETF'}
ind['etf']={}
for c,n in etf.items():
    try: f=q('fund_daily',ts_code=c,start_date='20260501',end_date=last).merge(q('fund_adj',ts_code=c,start_date='20260501',end_date=last)[['trade_date','adj_factor']],on='trade_date').sort_values('trade_date'); f['close']=(f.close*f.adj_factor/f.adj_factor.iloc[-1]).round(4); ind['etf'][n]=f[['trade_date','close']].values.tolist()
    except Exception as e: print('etf fail',c,e)
ind['tsmc']=None
dump('indicators',ind); print('ok',last,len(news))
