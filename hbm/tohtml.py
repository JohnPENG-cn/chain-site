import markdown
b=markdown.markdown(open('hbm_chain.md').read(),extensions=['tables'])
css="""body{max-width:860px;margin:auto;padding:24px 16px;font-family:-apple-system,"PingFang SC","Noto Sans CJK SC",sans-serif;line-height:1.7;color:#222;background:#fafaf7}
h1{font-size:1.6em;border-bottom:3px solid #d9534f;padding-bottom:6px}h2{margin-top:2em;border-left:5px solid #d9534f;padding-left:10px;font-size:1.25em}
blockquote{background:#fff4e5;border-left:5px solid #f0ad4e;margin:0;padding:10px 16px;border-radius:6px}
table{border-collapse:collapse;width:100%;font-size:.88em;display:block;overflow-x:auto}th,td{border:1px solid #ddd;padding:6px 8px;vertical-align:top}th{background:#f1f1ec}
img{max-width:100%;border-radius:8px;box-shadow:0 1px 6px #0002}a{color:#2a6fdb;word-break:break-all}"""
open('hbm.html','w').write(f'<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HBM 小链研究</title><style>{css}</style></head><body>{b}</body></html>')
