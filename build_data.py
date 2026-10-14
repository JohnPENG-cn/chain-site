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
            t=r['新闻标题']; tg=tag(t)
            if n in t: tg+=[(ch,nd) for ch,ns in CH.items() for _,nd,s in ns if c in s]
            if not tg: continue
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

# ================= v2: 四层 =================
import io,requests,statistics as stt,os
UA={'User-Agent':'Mozilla/5.0'}
L={'date':last,'gen':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
# --- 量价层: 台湾月营收 (MOPS)
TW={'2330':'台积电','3711':'日月光投控','2317':'鸿海','2382':'广达','3231':'纬创'}
tw={k:[] for k in TW}; y,m=datetime.date.today().year-1911,datetime.date.today().month
for i in range(16):
    mm=m-i; yy=y
    while mm<=0: mm+=12; yy-=1
    try:
        r=requests.get(f'https://mopsov.twse.com.tw/nas/t21/sii/t21sc03_{yy}_{mm}_0.html',headers=UA,timeout=30); r.encoding='big5'
        if r.status_code!=200 or len(r.text)<5000: continue
        for t in pd.read_html(io.StringIO(r.text)):
            if t.shape[1]<7: continue
            for _,row in t.iterrows():
                k=str(row.iloc[0]).strip()
                if k in TW and not any(x[0]==f'{yy+1911}-{mm:02d}' for x in tw[k]):
                    tw[k].append([f'{yy+1911}-{mm:02d}',round(float(row.iloc[2])/1e5,1),float(row.iloc[5]),float(row.iloc[6])])
    except Exception as e: print('mops',yy,mm,e)
for k in tw: tw[k].sort()
L['tw']={'src':'MOPS 公开资讯观测站 月营收汇总','url':'https://mopsov.twse.com.tw/mops/web/t21sc04_ifrs','unit':'亿新台币','names':TW,'data':tw}
# --- DRAM 现货 (DRAMeXchange 首页快照，历史靠每日累积)
dram=None
try:
    t=requests.get('https://www.dramexchange.com/',headers=UA,timeout=30).text
    rows={}
    for x in pd.read_html(io.StringIO(t)):
        if x.shape[1]>=7 and str(x.iloc[0,0])=='Item':
            for _,rr in x.iloc[1:].iterrows(): rows.setdefault(str(rr[0]),[float(rr[5]),str(rr[6])])
    want=['DDR5 16Gb (2Gx8) 4800/5600','DDR4 16Gb (2Gx8) 3200','DDR5 RDIMM 32GB 4800/5600','MLC 64Gb 8GBx8']
    dram={k:rows[k] for k in want if k in rows}
    hp='data/dram_hist.json'; h=json.load(open(hp)) if os.path.exists(hp) else {}
    h[last]={k:v[0] for k,v in dram.items()}; json.dump(h,open(hp,'w'))
    dram={'src':'DRAMeXchange 首页现货价（Session Average，美元）','url':'https://www.dramexchange.com/','spot':dram,'hist':h}
except Exception as e: print('dram',e)
L['dram']=dram; L['hbm']=None
# --- 铜
cu=ak.futures_zh_daily_sina(symbol='CU0'); cu['date']=cu['date'].astype(str)
L['cu']={'src':'新浪期货 沪铜主连 CU0','data':cu[['date','close']].tail(400).values.tolist()}
try: inv=ak.futures_inventory_em(symbol='cu'); L['cu_inv']={'src':'东方财富 沪铜库存(交易所口径)','data':[[str(a),float(b)] for a,b in inv[['日期','库存']].values]}
except Exception as e: print('inv',e); L['cu_inv']=None
try: lme=ak.futures_foreign_hist(symbol='CAD'); lme['date']=lme['date'].astype(str); L['lme']={'src':'新浪 LME 3个月铜 CAD（美元/吨）','data':lme[['date','close']].tail(400).values.tolist()}
except Exception as e: print('lme',e); L['lme']=None
L['tcrc']=None; L['lme_stock']=None
def yoyp(data,days=365):
    d=pd.Series({pd.Timestamp(a):float(b) for a,b in data}); last_=d.index[-1]
    prev=d[d.index<=last_-pd.Timedelta(days=days)]
    return round(float(d.iloc[-1]/prev.iloc[-1]-1)*100,1) if len(prev) else None
L['cu_yoy']=yoyp(L['cu']['data']); L['cu_mom']=yoyp(L['cu']['data'],30)
# --- 财务: 毛利率/存货周转天数/合同负债
fin={}
for c in names:
    try:
        fi=q('fina_indicator',ts_code=c,fields='end_date,grossprofit_margin,invturn_days').drop_duplicates('end_date').sort_values('end_date').tail(9)
        bs=q('balancesheet',ts_code=c,fields='end_date,contract_liab,adv_receipts').drop_duplicates('end_date').sort_values('end_date').tail(5)
        fin[c]={'gm':fi[['end_date','grossprofit_margin']].dropna().values.tolist(),'inv':fi[['end_date','invturn_days']].dropna().values.tolist(),
                'cl':[[a,(b if b==b and b is not None else 0)+(d if d==d and d is not None else 0)] for a,b,d in bs.values]}
    except Exception as e: print('fin',c,e)
def med(xs): xs=[x for x in xs if x is not None]; return round(stt.median(xs),2) if xs else None
def chg(series,lag=4):
    if len(series)>lag and series[-1-lag][1]: return series[-1][1]-series[-1-lag][1], series[-1][0]
    return None,None
TWMAP={'晶圆代工':['2330'],'先进封装':['3711'],'服务器整机':['2317','2382','3231']}
nodes={}
for ch,ns in CH.items():
    for lvl,nd,st in ns:
        cs=[c for c in st if c in fin]
        qs=sorted({e for c in cs for e,_ in fin[c]['gm']})[-8:]
        gm_series=[[e,med([dict(map(tuple,fin[c]['gm'])).get(e) for c in cs])] for e in qs]
        gmc=med([chg(fin[c]['gm'])[0] for c in cs]); invc=med([chg(fin[c]['inv'])[0] for c in cs])
        clg=med([ (fin[c]['cl'][-1][1]/fin[c]['cl'][0][1]-1)*100 if len(fin[c]['cl'])==5 and fin[c]['cl'][0][1] else None for c in cs])
        rep=max(qs) if qs else None
        score=0; why=[]
        if gmc is not None: score+=int(gmc>0.5)-int(gmc<-0.5); why.append(f"毛利率同比{gmc:+.1f}pct")
        if invc is not None: score+=(invc<-5)-(invc>5); why.append(f"存货周转天数同比{invc:+.0f}天")
        if clg is not None: score+=int(clg>10)-int(clg<-10); why.append(f"合同负债同比{clg:+.0f}%")
        if nd in TWMAP:
            ys=[tw[k][-1][3] for k in TWMAP[nd] if tw[k]]
            if ys: yv=med(ys); score+=int(yv>15)-int(yv<0); why.append(f"{'/'.join(TW[k] for k in TWMAP[nd])}月营收同比{yv:+.0f}%")
        if nd=='铜矿' and L['cu_yoy'] is not None: score+=int(L['cu_yoy']>10)-int(L['cu_yoy']<-10); why.append(f"沪铜同比{L['cu_yoy']:+.0f}%")
        sig='改善' if score>=2 else '恶化' if score<=-1 else '中性'
        node=[x for x in chains[ch] if x['node']==nd][0]; d20=node['d20']
        flag='产业变好但股价未动' if sig=='改善' and (d20 is None or d20<3) else '股价跑在基本面前' if sig!='改善' and d20 is not None and d20>10 else ('基本面走弱、股价同步走弱' if sig=='恶化' and d20 is not None and d20<0 else '大致同步')
        nodes[f'{ch}|{nd}']={'gm':gm_series,'gm_chg':gmc,'inv_chg':invc,'cl_yoy':clg,'report':rep,'score':score,'signal':sig,'why':why,'d20':d20,'mf':node['mf'],'flag':flag}
L['nodes']=nodes
# --- GB300 模型假设
L['model']={'src':'本工作台 GB300 市场模型 /workspace/gb300/market（inputs.py, market_results_v2.json，2026-10），均为模型假设/一方称，非官方',
 'rows':[['NVIDIA 2026 CoWoS 晶圆','59.5/70/85 万片(低/基/高)','一方称区间'],['CoWoS 可支撑 NVL72 当量柜','4.39 万柜','模型推算'],
 ['全球 HBM 产能(年化)','420/500/600 万片','一方称：月产35–50万片×12'],['HBM 可支撑柜数','4.30 万柜 → 当前瓶颈','模型推算'],
 ['HBM3E 价格','$8.33/12.2/15.6 每GB','一方称'],['2026 NVL72 当量柜 P50','5.08 万柜（区间4.56–5.63）','模型'],['摩根士丹利 2026 柜数','8.25 万柜','一方称（第三方转引）']]}
# --- 事件日历 & 可证伪
td=datetime.date.today()
def nxt(day):
    d=td.replace(day=day) if td.day<day else (td.replace(day=1)+datetime.timedelta(days=32)).replace(day=day); return d.isoformat()
fri=(td+datetime.timedelta(days=(4-td.weekday())%7)).isoformat()
L['events']=[[nxt(5),'鸿海/广达/纬创 月营收（AI服务器出货代理）','AI算力','MOPS'],[nxt(10),'台积电 月营收','AI算力','台积电IR/MOPS'],
 [fri,'上期所 周度库存（沪铜）','铜','SHFE'],['2026-10下旬','SK hynix Q3 财报（HBM 出货与份额）','AI算力','预计'],
 ['2026-10-30','行业ETF 月度调仓信号（本工作台）','两链','ETF 实验室'],['2026-11上旬','日东纺 半年报（T-glass 产能）','AI算力','预计'],
 ['2026-11-18','NVIDIA Q3 FY27 财报','AI算力','数据商预计，公司未确认'],['2027-01中旬','台积电 Q4 法说会（CoWoS 产能）','AI算力','预计']]
L['events'].sort(key=lambda x:x[0])
fz=[]
for ln in open('/workspace/gb300/compare/model_vs_street.md',encoding='utf-8'):
    p=[x.strip() for x in ln.split('|')]
    if len(p)>7 and p[1].isdigit(): fz.append([p[2],p[3],p[4],p[5]])
fz+= [['每月末','行业ETF 12个月动量','跑赢等权约5pct/年','样本外连续12个月跑输则降权'],['每月末','ETF份额反向信号','小仓位跟踪','样本外6–12个月无超额则放弃']]
L['falsify']={'src':'/workspace/gb300/compare/model_vs_street.md；ETF 实验室回测（2026-10）','rows':fz}
# --- cninfo 公告
ann=[];sd=(td-datetime.timedelta(days=60)).isoformat()
codes={c[:6]:c for c in names}
KWS=['扩产','订单','涨价','中标','产能','项目','合同','投资建设']
for c in codes.values():
    try:
        org=requests.post('https://www.cninfo.com.cn/new/information/topSearch/query',data={'keyWord':c[:6],'maxNum':5},headers=UA,timeout=20).json()
        org=[o for o in org if o['code']==c[:6]][0]['orgId']
        col='sse' if c.endswith('SH') else 'szse'
        j=requests.post('https://www.cninfo.com.cn/new/hisAnnouncement/query',data={'pageNum':1,'pageSize':50,'column':col,'tabName':'fulltext','stock':f'{c[:6]},{org}','seDate':f'{sd}~{td}'},headers=UA,timeout=20).json()
        for a in j.get('announcements') or []:
            t=re.sub('<.*?>','',a['announcementTitle']); hit=[k for k in KWS if k in t]
            if hit: ann.append({'code':c,'name':names[c],'title':t,'kw':hit[0],'time':datetime.datetime.fromtimestamp(a['announcementTime']/1000).strftime('%Y-%m-%d'),
                 'url':'https://static.cninfo.com.cn/'+a['adjunctUrl'],'tags':[(ch,nd) for ch,ns in CH.items() for _,nd,s in ns if c in s]})
        time.sleep(0.3)
    except Exception as e: print('cninfo',c,e)
seen=set(); L['ann']={'src':'巨潮资讯 cninfo 全文检索（近60日，标题含 扩产/订单/涨价/中标/产能/项目/合同/投资建设，仅保留节点股）','items':[a for a in sorted(ann,key=lambda x:x['time'],reverse=True) if not (a['url'] in seen or seen.add(a['url']))]}
# --- 一句话判断（规则生成）
summ={}
for ch in CH:
    ns={k.split('|')[1]:v for k,v in nodes.items() if k.startswith(ch)}
    imp=[k for k,v in ns.items() if v['signal']=='改善']; bad=[k for k,v in ns.items() if v['signal']=='恶化']
    gap=[k for k,v in ns.items() if v['flag']=='产业变好但股价未动']; run=[k for k,v in ns.items() if v['flag']=='股价跑在基本面前']
    if ch=='AI算力' and tw['2330']: key=f"台积电{tw['2330'][-1][0][5:]}月营收同比{tw['2330'][-1][3]:+.1f}%（MOPS）"
    elif ch=='铜': key=f"沪铜{L['cu']['data'][-1][0]}收{float(L['cu']['data'][-1][1]):,.0f}元/吨、同比{L['cu_yoy']:+.1f}%（新浪期货）"
    else: key=''
    tone_='产业端偏强' if len(imp)>len(bad) else '产业端偏弱' if len(bad)>len(imp) else '产业端分化'
    px_='但近20日股价多数下跌' if sum((v['d20'] or 0)<0 for v in ns.values())>len(ns)/2 else '股价多数上涨'
    s_=f"{tone_}，{px_}：{len(ns)}个节点中{len(imp)}个改善、{len(bad)}个恶化。"
    if gap: s_+=f"「产业变好但股价未动」：{'、'.join(gap)}。"
    if run: s_+=f"「股价跑在基本面前」：{'、'.join(run)}。"
    summ[ch]={'line':s_,'key':key}
L['summary']=summ
dump('layers',L); print('v2 ok',len(ann),len(fin))
