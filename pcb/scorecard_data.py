"""回报持续性打分卡的补充数据（联网，单独跑；./build.sh 不调用）。2026-10-24 新增。
输出 pcb_data/scorecard.json（只存加工后的小表）：
  alloc  —— 管理层资本配置：17 家 + 兴森科技，每年 资本开支 / 折旧 / 现金分红（实施，按除息年）/ 回购（Tushare repurchase“完成”记录，按方案取累计额）
  xs     —— 兴森科技（A 股 IC 载板代表）财报小表，口径同 filings.json
  sub    —— 台股载板三家（欣兴 3037、南电 8046、景硕 3189）季度毛利率 2019 起（MOPS，经 FinMind）
  top5   —— 宏和、鼎泰、兴森 2021–2025 年报前五大客户占比（巨潮，抽取方式同 pcb/top5.py）
Token 只从 ~/.config/tushare/token 读，不打印。原始下载放 pcb_data/raw/（不进仓库）。"""
import os, json, time, subprocess, datetime as dt
import pandas as pd
import tushare as ts
import filings as F
import top5 as T

R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(R0, 'pcb_data', 'raw')
XS = ('002436.SZ', '兴森科技', '载板')


def pro_():
    p = ts.pro_api(F.tok())
    p._DataApi__http_url = os.environ.get('TUSHARE_HTTP_URL', 'https://api.waditu.com/dataapi')
    return p


def dividends(pro, code):
    d = F.q(pro, 'dividend', ts_code=code, fields='ts_code,end_date,div_proc,cash_div_tax,base_share,ex_date')
    d = d[(d.div_proc == '实施') & d.ex_date.notna()].drop_duplicates(['end_date', 'ex_date'])
    out = {}
    for _, r in d.iterrows():
        if r.cash_div_tax and r.base_share:
            y = str(r.ex_date)[:4]
            out[y] = out.get(y, 0) + float(r.cash_div_tax) * float(r.base_share) * 1e4 / 1e8   # 每股（元）× 万股 → 亿元
    return {k: round(v, 2) for k, v in out.items()}


def buybacks(pro, code):
    """repurchase 表里“完成”行是回购方案的累计进度；按时间排，金额不再增大或间隔 > 13 个月 = 新方案；方案额记到最后一行的年份。
    剔除 high_limit == low_limit 且金额 < 0.2 亿元的行（股权激励限制性股票回购注销，不是股东回报）。"""
    r = F.q(pro, 'repurchase', ts_code=code, start_date='20150101', end_date='20261023')
    if r is None or r.empty:
        return {}
    r = r[(r.proc == '完成') & r.amount.notna() & r.end_date.notna()].copy()
    r = r[~((r.high_limit == r.low_limit) & (r.amount < 2e7))]
    r = r.sort_values('end_date')
    progs, cur = [], None
    for _, x in r.iterrows():
        d = dt.datetime.strptime(str(x.end_date), '%Y%m%d')
        if cur and x.amount >= cur['amt'] and (d - cur['start']).days <= 400:
            cur.update(amt=float(x.amount), end=d)
        else:
            cur = dict(start=d, end=d, amt=float(x.amount)); progs.append(cur)
    out = {}
    for p in progs:
        y = p['end'].strftime('%Y') if p['end'].month > 6 or p['end'].year < 2026 else '2026H1'
        out[y] = out.get(y, 0) + p['amt'] / 1e8
    return {k: round(v, 2) for k, v in out.items()}


def finrows(pro, code):
    kw = dict(ts_code=code, start_date='20150101', end_date='20261231')
    cf = F.q(pro, 'cashflow', fields='ts_code,end_date,report_type,c_pay_acq_const_fiolta,depr_fa_coga_dpba', **kw)
    bs = F.q(pro, 'balancesheet', fields='ts_code,end_date,report_type,cip,fix_assets', **kw)
    ic = F.q(pro, 'income', fields='ts_code,end_date,report_type,revenue', **kw)
    fi = F.q(pro, 'fina_indicator', fields='ts_code,end_date,roic,grossprofit_margin', **kw)
    rows = {}
    for e in F.YEARS:
        r = dict(capex=F.first(cf, e, 'c_pay_acq_const_fiolta'), dep=F.first(cf, e, 'depr_fa_coga_dpba'), cip=F.first(bs, e, 'cip'),
                 fa=F.first(bs, e, 'fix_assets'), rev=F.first(ic, e, 'revenue'), roic=F.first(fi, e, 'roic'), gm=F.first(fi, e, 'grossprofit_margin'))
        for k in ('capex', 'dep', 'cip', 'fa', 'rev'):
            if r[k] is not None:
                r[k] = round(r[k] / 1e8, 2)
        for k in ('roic', 'gm'):
            if r[k] is not None:
                r[k] = round(r[k], 2)
        if any(v is not None for v in r.values()):
            rows['2026H1' if e == '20260630' else e[:4]] = r
    return rows


def substrate():
    out = {}
    for s in ('3037', '8046', '3189'):
        p = os.path.join(RAW, f'fs_{s}_2019.json')
        if not os.path.exists(p):
            subprocess.run(['curl', '-s', f'https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockFinancialStatements&data_id={s}&start_date=2019-01-01', '-o', p], check=True)
            time.sleep(1)
        d = pd.DataFrame(json.load(open(p))['data'])
        pv = d.pivot_table(index='date', columns='type', values='value', aggfunc='first')
        out[s] = [[i, round(r.Revenue / 1e8, 1), round(r.GrossProfit / r.Revenue * 100, 1)] for i, r in pv.iterrows() if r.get('Revenue') and r.get('GrossProfit') is not None]
    return out


def top5_extra():
    import re, requests
    res = []
    for code, name in (('603256', '宏和科技'), ('301377', '鼎泰高科'), ('002436', '兴森科技')):
        oid = T.org(code); anns = T.reports(code, oid); time.sleep(1)
        for fy in T.FY:
            a = T.pick(anns, fy)
            if not a:
                res.append(dict(code=code, name=name, fy=fy, top5=None, url=None)); continue
            url = 'https://static.cninfo.com.cn/' + a['adjunctUrl']
            pdf = os.path.join(T.RAW, f'{code}_{fy}.pdf'); txt = pdf[:-4] + '.txt'
            if not os.path.exists(txt):
                rr = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=120); open(pdf, 'wb').write(rr.content)
                subprocess.run(['pdftotext', '-layout', pdf, txt], check=False); os.remove(pdf); time.sleep(1)
            t = re.sub(r'[ \t\u3000]+', ' ', open(txt, errors='ignore').read())
            m = T.PAT.search(re.sub(r'\s*\n\s*', '', t))
            res.append(dict(code=code, name=name, fy=fy, top5=float(m.group(1) or m.group(2)) if m else None, url=url))
            print(name, fy, res[-1]['top5'], flush=True)
    return res


def main():
    pro = pro_()
    cos = [(c, n) for c, n, _ in F.CO] + [XS[:2]]
    alloc = {}
    for code, name in cos:
        alloc[name] = dict(code=code, div=dividends(pro, code), bb=buybacks(pro, code))
        print(name, alloc[name], flush=True); time.sleep(0.5)
    xs = dict(code=XS[0], name=XS[1], seg=XS[2], data=finrows(pro, XS[0]))
    out = dict(meta=dict(asof=time.strftime('%Y-%m-%d'), unit='亿元；gm 为 %',
                         src='Tushare Pro（dividend、repurchase、cashflow、balancesheet、income、fina_indicator）；MOPS 季报（FinMind）；巨潮年报'),
               alloc=alloc, xs=xs, sub=substrate(), top5=top5_extra())
    json.dump(out, open(os.path.join(R0, 'pcb_data', 'scorecard.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
