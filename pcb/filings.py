"""PCB 链 A 股财报数据（联网，单独跑；./build.sh 不调用）：Tushare 财报接口 → pcb_data/filings.json（只存加工后的小表，不存原始返回）。
口径：capex = 现金流量表“购建固定资产、无形资产和其他长期资产支付的现金”(c_pay_acq_const_fiolta)；折旧 = “固定资产折旧、油气资产折耗、生产性生物资产折旧”(depr_fa_coga_dpba)；
在建工程 = 资产负债表 cip；ROIC、毛利率 = fina_indicator（Tushare 计算口径）；营收 = 利润表 revenue。年度用 12-31 合并报表；2026H1 用 06-30（半年数，不年化）。
Token 只从环境变量 / ~/.config/tushare/token 读，不打印、不落盘到仓库。"""
import os, json, time
import tushare as ts

R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CO = [  # (代码, 简称, 环节)
 ('300476.SZ', '胜宏科技', '板厂'), ('002463.SZ', '沪电股份', '板厂'), ('002916.SZ', '深南电路', '板厂'), ('603228.SH', '景旺电子', '板厂'),
 ('002938.SZ', '鹏鼎控股', '板厂'), ('002815.SZ', '崇达技术', '板厂'), ('000823.SZ', '超声电子', '板厂'), ('603920.SH', '世运电路', '板厂'),
 ('688183.SH', '生益电子', '板厂'), ('001389.SZ', '广合科技', '板厂'),
 ('600183.SH', '生益科技', '覆铜板'), ('688519.SH', '南亚新材', '覆铜板'), ('603186.SH', '华正新材', '覆铜板'),
 ('603256.SH', '宏和科技', '上游'), ('301511.SZ', '德福科技', '上游'), ('301377.SZ', '鼎泰高科', '上游'), ('301217.SZ', '铜冠铜箔', '上游'),
]
YEARS = [f'{y}1231' for y in range(2015, 2026)] + ['20260630']


def tok():
    p = os.path.expanduser('~/.config/tushare/token')
    return open(p).read().strip() if os.path.exists(p) else os.environ['TUSHARE_TOKEN'].strip()


def q(pro, api, **kw):
    for i in range(10):
        try:
            return getattr(pro, api)(**kw)
        except Exception as e:  # 偶发超时 / “IP数量超限”（box 出口 IP 轮换）：退避重试
            time.sleep(15 * (i + 1)); err = e
    raise err


def first(df, end, col):
    d = df[df.end_date == end]
    if 'report_type' in d:
        d = d[d.report_type.astype(str) == '1']
    v = d[col].dropna()
    return None if v.empty else float(v.iloc[0])


def main():
    pro = ts.pro_api(tok())
    pro._DataApi__http_url = os.environ.get('TUSHARE_HTTP_URL', 'https://api.waditu.com/dataapi')
    part = os.path.join(R0, 'pcb_data', 'raw', 'filings_partial.json')  # 断点续跑缓存（raw/ 不进仓库）
    os.makedirs(os.path.dirname(part), exist_ok=True)
    done = json.load(open(part)) if os.path.exists(part) else {}
    out = []
    for code, name, seg in CO:
        if code in done:
            out.append(done[code]); continue
        kw = dict(ts_code=code, start_date='20150101', end_date='20261231')
        cf = q(pro, 'cashflow', fields='ts_code,end_date,report_type,c_pay_acq_const_fiolta,depr_fa_coga_dpba', **kw)
        bs = q(pro, 'balancesheet', fields='ts_code,end_date,report_type,cip,fix_assets', **kw)
        ic = q(pro, 'income', fields='ts_code,end_date,report_type,revenue', **kw)
        fi = q(pro, 'fina_indicator', fields='ts_code,end_date,roic,grossprofit_margin', **kw)
        rows = {}
        for e in YEARS:
            r = dict(capex=first(cf, e, 'c_pay_acq_const_fiolta'), dep=first(cf, e, 'depr_fa_coga_dpba'), cip=first(bs, e, 'cip'),
                     fa=first(bs, e, 'fix_assets'), rev=first(ic, e, 'revenue'), roic=first(fi, e, 'roic'), gm=first(fi, e, 'grossprofit_margin'))
            for k in ('capex', 'dep', 'cip', 'fa', 'rev'):
                if r[k] is not None:
                    r[k] = round(r[k] / 1e8, 2)  # 亿元
            for k in ('roic', 'gm'):
                if r[k] is not None:
                    r[k] = round(r[k], 2)
            if any(v is not None for v in r.values()):
                rows['2026H1' if e == '20260630' else e[:4]] = r
        out.append(dict(code=code, name=name, seg=seg, data=rows))
        done[code] = out[-1]; json.dump(done, open(part, 'w'), ensure_ascii=False)
        print(name, len(rows))
        time.sleep(0.6)
    meta = dict(asof=time.strftime('%Y-%m-%d'), unit='亿元；roic、gm 为 %', src='Tushare Pro 财报接口（cashflow / balancesheet / income / fina_indicator），源自上市公司定期报告',
                note='2026H1 为半年数（capex、折旧、营收未年化；ROIC 为半年口径，Tushare 未年化）')
    json.dump(dict(meta=meta, cos=out), open(os.path.join(R0, 'pcb_data', 'filings.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
