"""前五大客户销售占比（联网，单独跑；./build.sh 不调用）：巨潮资讯年报全文 → pdftotext → 抽“前五名客户合计销售金额占年度销售总额比例”。
PDF 与文本只放 pcb_data/raw/ar/（.gitignore），只把结果写进 pcb_data/top5.json（含每份年报的巨潮链接）。抽不到的记 None（页面写“数据缺口”）。"""
import os, re, json, subprocess, time, requests
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(R0, 'pcb_data', 'raw', 'ar')
CO = [('300476', '胜宏科技'), ('002463', '沪电股份'), ('002916', '深南电路'), ('603228', '景旺电子'), ('002938', '鹏鼎控股'), ('002815', '崇达技术'),
      ('000823', '超声电子'), ('603920', '世运电路'), ('688183', '生益电子'), ('001389', '广合科技'), ('600183', '生益科技'), ('688519', '南亚新材')]
FY = [2021, 2022, 2023, 2024, 2025]
H = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
B = 'https://www.cninfo.com.cn/new'


def org(code):
    return requests.post(f'{B}/information/topSearch/query', data=dict(keyWord=code, maxNum=5), headers=H, timeout=30).json()[0]['orgId']


def reports(code, oid):
    col = 'sse' if code.startswith('6') else 'szse'
    out = []
    for pg in (1, 2):
        d = requests.post(f'{B}/hisAnnouncement/query', headers=H, timeout=30, data=dict(
            pageNum=pg, pageSize=30, column=col, tabName='fulltext', stock=f'{code},{oid}', category='category_ndbg_szsh',
            seDate='2022-01-01~2026-10-23', isHLtitle='true')).json()
        out += d.get('announcements') or []
    return out


def pick(anns, fy):
    c = [a for a in anns if f'{fy}年年度报告' in re.sub('<[^>]+>', '', a['announcementTitle'])]
    c = [a for a in c if not re.search('摘要|英文|English|已取消', a['announcementTitle'])]
    c.sort(key=lambda a: ('更正' in a['announcementTitle'] or '修订' in a['announcementTitle'], a['announcementTime']), reverse=True)
    return c[0] if c else None


PAT = re.compile(r'前五名客户合计销售金额占年度销售总额比例\s*([\d.]+)\s*%|前五名客户销售额\s*[\d,.]+\s*[万亿]?元，占年度销售总额\s*([\d.]+)\s*%')


def main():
    os.makedirs(RAW, exist_ok=True)
    res = []
    for code, name in CO:
        oid = org(code); anns = reports(code, oid); time.sleep(1)
        for fy in FY:
            a = pick(anns, fy)
            if not a:
                res.append(dict(code=code, name=name, fy=fy, top5=None, url=None, note='巨潮未检索到年报')); continue
            url = 'https://static.cninfo.com.cn/' + a['adjunctUrl']
            pdf = os.path.join(RAW, f'{code}_{fy}.pdf'); txt = pdf[:-4] + '.txt'
            if not os.path.exists(txt):
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=120); open(pdf, 'wb').write(r.content)
                subprocess.run(['pdftotext', '-layout', pdf, txt], check=False); os.remove(pdf); time.sleep(1)
            t = re.sub(r'[ \t\u3000]+', ' ', open(txt, errors='ignore').read())
            t2 = re.sub(r'\s*\n\s*', '', t)
            m = PAT.search(t2)
            res.append(dict(code=code, name=name, fy=fy, top5=float(m.group(1) or m.group(2)) if m else None, url=url))
            print(name, fy, res[-1]['top5'], flush=True)
    json.dump(dict(asof=time.strftime('%Y-%m-%d'), src='巨潮资讯网 上市公司年度报告“主要销售客户情况”', rows=res),
              open(os.path.join(R0, 'pcb_data', 'top5.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
