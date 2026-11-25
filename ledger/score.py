#!/usr/bin/env python3
"""总账到期打分 + 校准 + 陈旧标记（2026-11-25 起）。

用法：python3 ledger/score.py [--today YYYY-MM-DD] [--apply]
  不带 --apply：只报告（到期/将到期清单、可打分候选、校准表、陈旧条目），不写文件。
  带 --apply：把有证据的结果写进 data/ledger.json，并写 data/ledger_scoring.json，然后应由 ledger/build.py 重建页面。

打分规则（不编造）：
  1) 只给 due ≤ 今天、outcome=待验证 的条目打分。
  2) 结果只来自两处：条目里的 resolve = {outcome, d, t, src}（人工/例程按 check 字段取数后写入，src 必须是链接），
     或证据记录里 w=触发证伪 的一条（预测记 未中；判断记 未中）。
  3) 两处都没有：保持 待验证，写 pending_reason（到期几天、按什么取数）。
  4) outcome ∈ 命中 / 未中 / 部分命中；Brier 记分 命中=1、部分命中=0.5、未中=0。
判断（G）的概率含义：到期日前（无到期日的按 2027-12-31）不被证伪的概率。
陈旧：未作废、未打分的条目，最近一条证据（没有证据则用入账日 since）距今天 > 30 天 → 黄标。
"""
import json, os, sys, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, 'data', 'ledger.json')
OUT = os.path.join(ROOT, 'data', 'ledger_scoring.json')
OUTCOMES = ('命中', '未中', '部分命中')
SCORE = {'命中': 1.0, '部分命中': 0.5, '未中': 0.0}
STALE_DAYS = 30
BUCKETS = [(0, .3, '<30%'), (.3, .5, '30–49%'), (.5, .7, '50–69%'), (.7, .85, '70–84%'), (.85, 1.01, '≥85%')]
DEFAULT_H = '2027-12-31'


def D(s):
    return datetime.date.fromisoformat(s)


def last_touch(x):
    ds = [e['d'] for e in x.get('ev', [])] + ([x['since']] if x.get('since') else [])
    return max(ds) if ds else None


def is_open(x):
    return x['status'] != '作废' and x.get('outcome') not in OUTCOMES + ('作废',)


def stale(items, today):
    out = []
    for x in items:
        if not is_open(x):
            continue
        lt = last_touch(x)
        if lt and (today - D(lt)).days > STALE_DAYS:
            out.append((x['gid'], lt, (today - D(lt)).days))
    return out


def brier(x):
    return round((x['prob'] - SCORE[x['outcome']]) ** 2, 4) if x.get('outcome') in OUTCOMES and isinstance(x.get('prob'), (int, float)) else None


def quarter(s):
    d = D(s)
    return f'{d.year}Q{(d.month - 1) // 3 + 1}'


def calib(items):
    sc = [x for x in items if x.get('outcome') in OUTCOMES and isinstance(x.get('prob'), (int, float))]
    rows = []
    for lo, hi, lab in BUCKETS:
        g = [x for x in sc if lo <= x['prob'] < hi]
        rows.append(dict(bucket=lab, n=len(g),
                         mean_prob=round(sum(x['prob'] for x in g) / len(g), 3) if g else None,
                         hit_rate=round(sum(SCORE[x['outcome']] for x in g) / len(g), 3) if g else None,
                         brier=round(sum(brier(x) for x in g) / len(g), 4) if g else None))
    byq = collections.defaultdict(list)
    for x in sc:
        byq[quarter(x['due'])].append(x)
    qrows = [dict(quarter=q, n=len(g), hits=sum(x['outcome'] == '命中' for x in g), partial=sum(x['outcome'] == '部分命中' for x in g),
                  brier=round(sum(brier(x) for x in g) / len(g), 4)) for q, g in sorted(byq.items())]
    byb = collections.defaultdict(list)
    for x in sc:
        byb[x['book']].append(x)
    brows = [dict(book=b, n=len(g), brier=round(sum(brier(x) for x in g) / len(g), 4)) for b, g in sorted(byb.items())]
    return dict(n=len(sc), brier=round(sum(brier(x) for x in sc) / len(sc), 4) if sc else None,
                buckets=rows, quarters=qrows, books=brows)


def run(doc, today, apply=False):
    items = doc['items']
    newly, pending, soon = [], [], []
    for x in items:
        if x['status'] == '作废' or x.get('outcome') != '待验证' or not x.get('due'):
            continue
        dd = D(x['due'])
        if dd > today:
            if (dd - today).days <= 14:
                soon.append((x['gid'], x['due'], x.get('check', '')))
            continue
        res = x.get('resolve')
        fal = [e for e in x.get('ev', []) if e['w'] == '触发证伪']
        if res and res.get('outcome') in OUTCOMES and str(res.get('src', '')).startswith('http'):
            newly.append((x['gid'], res['outcome'], res['src']))
            if apply:
                x['outcome'] = res['outcome']; x.pop('pending_reason', None)
        elif fal:
            newly.append((x['gid'], '未中', fal[-1]['src']))
            if apply:
                x['outcome'] = '未中'; x.pop('pending_reason', None)
        else:
            why = f'到期 {(today - dd).days} 天，尚无可核实的结果证据；按「{x.get("check") or x.get("falsify", "")[:40]}」取数后写入 resolve'
            pending.append((x['gid'], x['due'], why))
            if apply:
                x['pending_reason'] = why
    for x in items:
        x['brier'] = brier(x)
    rep = dict(asof=today.isoformat(), newly_scored=newly, expired_pending=pending, due_14d=soon,
               stale=stale(items, today), calibration=calib(items))
    if apply:
        json.dump(doc, open(LEDGER, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(rep, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return rep


def main():
    a = sys.argv[1:]
    today = D(a[a.index('--today') + 1]) if '--today' in a else datetime.date.today()
    doc = json.load(open(LEDGER, encoding='utf-8'))
    rep = run(doc, today, apply='--apply' in a)
    c = rep['calibration']
    print(f'总账打分 · {rep["asof"]}')
    print(f'  本次新打分 {len(rep["newly_scored"])} 条：' + ('；'.join(f'{g} {o}' for g, o, _ in rep['newly_scored']) or '无'))
    print(f'  已到期未能打分 {len(rep["expired_pending"])} 条' + ''.join(f'\n    {g}（到期 {d}）：{w}' for g, d, w in rep['expired_pending']))
    print(f'  14 天内到期 {len(rep["due_14d"])} 条：' + ('；'.join(f'{g} {d}' for g, d, _ in rep['due_14d']) or '无'))
    print(f'  已打分合计 {c["n"]} 条，平均 Brier {c["brier"]}')
    for r in c['buckets']:
        if r['n']:
            print(f'    {r["bucket"]}: n={r["n"]} 平均概率 {r["mean_prob"]} 实际命中 {r["hit_rate"]} Brier {r["brier"]}')
    print(f'  陈旧（>{STALE_DAYS} 天无新证据）{len(rep["stale"])} 条：' + ' '.join(g for g, _, _ in rep['stale']))


if __name__ == '__main__':
    main()
