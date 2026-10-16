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
# ---- 中国账本（v0.5）：国产加速卡能用上的裸 HBM，见 hbm/build.py cnbal()
CN = {r['y']: r for r in H['cn']['bal']}
CC26, CC27 = round(CN[2026]['cov'] * 100), round(CN[2027]['cov'] * 100)          # 可用 ÷ 不缺货需求
CL26, CL27 = round(CN[2026]['covl'] * 100), round(CN[2027]['covl'] * 100)        # 可用 ÷ 机构出货口径（下限）
CA26, CA27 = CN[2026]['a'], CN[2027]['a']                                          # 可用 EB
CD26, CD27X = CN[2026]['d'], CN[2027]['d']
CK26, CK27 = CN[2026]['cards'], CN[2027]['cards']                                  # 可用 HBM 能配的卡（百万张）
# ---- CoWoS 中国账本（v0.4）：国产 AI 卡只能在大陆做的 2.5D 封装，见 cowos/build.py cwcn()
W = {r['y']: r for r in json.load(open(_P('data', 'cowos.json')))['cn']['bal']}
WC26, WC27 = round(W[2026]['cov'] * 100), round(W[2027]['cov'] * 100)          # 国产 AI 可用 2.5D ÷ 不缺货需求
WH26, WH27 = round(W[2026]['covh'] * 100), round(W[2027]['covh'] * 100)        # ÷ HBM 能配的卡所需
WS26, WS27 = W[2026]['s'], W[2027]['s']                                          # 国产 AI 可用 2.5D（千片/年）
WK26, WK27 = W[2026]['cards'], W[2027]['cards']                                  # 2.5D 能封的卡（百万张）
WHK26, WHK27 = W[2026]['hcards'], W[2027]['hcards']                              # HBM 能配的卡 + 950PR（百万张）
# ---- CoWoS v0.4.3 硅中介层（cowos/model.py ip；TOC 汇总由 cowos/build.py 写进 toc.json ipsum）
IPM = json.load(open(_P('cowos_data', 'model_out.json')))['ip']
IPR = {int(k): v for k, v in IPM['res'].items()}
IPG26, IPG27 = round(IPR[2026]['gap']), round(IPR[2027]['gap'])        # 中介层余量（良品片，%）
IPBE27, IPBE28, IPX = IPM['be27'], IPM['be28'], IPM['x']
IPT = json.load(open(_P('data', 'toc.json'))).get('ipsum', {})
