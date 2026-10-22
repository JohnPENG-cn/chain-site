"""总账的“页面条目”读取：每条判断/预测在研究页上的原始位置。build.py 的映射检查和 init.py 都用它。
返回 dict：key = 旧本地编号（如 HBM-J1、CoWoS-N3、TOC-T2），value = dict(kind, chain, page, text, ...)。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda f: json.load(open(os.path.join(ROOT, f), encoding='utf-8'))
ST = {'ok': '有效', 'watch': '受挑战', 'hit': '证伪'}


def _jid(j):
    m = re.match(r"^([A-Z]+\d+′?)\s*(.*)$", j)
    return (m.group(1), m.group(2)) if m else (j, j)


def hbm_pred():
    s = open(os.path.join(ROOT, 'hbm.js'), encoding='utf-8').read()
    m = re.search(r'const PRED=(\[\[.*?\]\]);', s, flags=re.S)
    arr = json.loads(m.group(1).replace("'", '"'))
    return [dict(id=a[0], text=a[1], due=a[2], check=a[3], status='pending') for a in arr]


def page_items():
    out = {}

    def judg(prefix, chain, page, F, ledger='全球'):
        for x in F:
            lid, short = _jid(x['j'])
            out[f'{prefix}-{lid}'] = dict(kind='判断', chain=chain, page=page, book=ledger, local=lid, text=x['j'], short=short,
                                         falsify=x.get('falsify', ''), th=x.get('th', ''), st=ST.get(x.get('st'), '有效'))

    def pred(prefix, chain, page, P, ledger='全球'):
        for x in P:
            out[f'{prefix}-{x["id"]}'] = dict(kind='预测', chain=chain, page=page, book=ledger, local=x['id'], text=x['text'],
                                             due=x['due'], check=x.get('check', ''), st='作废' if x.get('status') == 'void' else '有效',
                                             note=x.get('note', ''))
    hx, h = J('data/hbm_x.json'), J('data/hbm.json')
    cw, pc, cu, toc = J('data/cowos.json'), J('data/pcb.json'), J('data/cu.json'), J('data/toc.json')
    judg('HBM', 'HBM', 'hbm.html', hx['falsify'])
    judg('HBM-中国', 'HBM', 'hbm.html', h['cn']['falsify'], '中国')
    judg('CoWoS', 'CoWoS', 'cowos.html', cw['falsify'])
    judg('CoWoS-中国', 'CoWoS', 'cowos.html', cw['cn']['falsify'], '中国')
    judg('TOC判断', '跨链', 'cowos.html', toc['falsify'])
    judg('PCB', 'PCB', 'pcb.html', pc['falsify'])
    judg('PCB-中国', 'PCB', 'pcb.html', pc['cn']['falsify'], '中国')
    judg('铜', '铜', 'cu.html', cu['falsify'])
    judg('铜-中国', '铜', 'cu.html', cu['cn']['falsify'], '中国')
    claims = {c['id']: c for c in pc.get('industry', {}).get('claims', [])}
    for k in ('J6', 'J7', 'J8'):
        if f'PCB-{k}' in out and k in claims:
            out[f'PCB-{k}']['due'] = claims[k]['due']
    pred('HBM', 'HBM', 'hbm.html', hbm_pred())
    pred('HBM-中国', 'HBM', 'hbm.html', h['cn']['preds'], '中国')
    pred('CoWoS', 'CoWoS', 'cowos.html', cw['predictions'])
    pred('CoWoS-中国', 'CoWoS', 'cowos.html', cw['cn']['preds'], '中国')
    pred('TOC', '跨链', 'cowos.html', toc['preds'])
    pred('PCB', 'PCB', 'pcb.html', pc['predictions'])
    pred('PCB-中国', 'PCB', 'pcb.html', pc['cn']['preds'], '中国')
    pred('铜', '铜', 'cu.html', cu['predictions'])
    pred('铜-中国', '铜', 'cu.html', cu['cn']['preds'], '中国')
    return out
