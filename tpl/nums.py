"""两页结论层文字里引用的关键数字，统一从模型输出算（不手写），保证 HBM 页、CoWoS 页、首页三处一致。"""
import json, os
R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_P = lambda *a: os.path.join(R0, *a)
H = json.load(open(_P('data', 'hbm.json')))
R = json.load(open(_P('cowos_data', 'model_out.json')))['res']
U = json.load(open(_P('cowos_data', 'model_out.json')))['uncon']
hsup = lambda y: sum(H['supply'][str(y)].values()) * 12 * H['gbw'][str(y)] * H['ut'][str(y)] / 1e6
hdem = lambda y: sum(x['units'] * x['gb'] for x in H['demand'] if x['y'] == y) / 1000
HC = round(hsup(2027) / R['2027']['hbm'] * 100)                      # 2027 HBM 满足率（KGI 可见出货口径）
CC = round(R['2027']['s'] / R['2027']['d'] * 100)                     # 2027 CoWoS 满足率（同一口径）
CGAP = round(-(R['2027']['s'] - R['2027']['d']) / R['2027']['d'] * 100)              # CoWoS 2027 缺口（正数 = 缺）
CGAPU = round(-(R['2027']['s'] - R['2027']['d'] - U['2027']) / (R['2027']['d'] + U['2027']) * 100)
HGAP = round(-(hsup(2027) - hdem(2027)) / hdem(2027) * 100)           # HBM 页 2027 缺口
CS27, CD27 = R['2027']['s'], R['2027']['d']
assert abs(hdem(2027) - R['2027']['hbm']) < 0.02, 'HBM 页需求与 CoWoS 页出货所需 HBM 不一致'
if __name__ == '__main__':
    print(dict(HC=HC, CC=CC, CGAP=CGAP, CGAPU=CGAPU, HGAP=HGAP, CS27=CS27, CD27=CD27, h27=round(hsup(2027), 2), d27=round(hdem(2027), 2), cw_hbm27=R['2027']['hbm']))
