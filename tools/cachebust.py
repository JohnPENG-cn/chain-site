#!/usr/bin/env python3
"""给全站本地静态资源加版本号（?v=<内容哈希前 10 位>），防止 iOS Safari / GitHub Pages CDN（max-age=600）
把新 HTML 和旧 CSS/JS/JSON 混着用。幂等：内容不变，版本号不变；只改资源引用，不改页面内容。
  1) *.js 里的 fetch('data/x.json') → fetch('data/x.json?v=…')（先做，因为它会改变 JS 自身的哈希）
  2) *.html 里 href="*.css" / src="*.js" → ?v=…（相对路径按 HTML 所在目录解析；外链、不存在的文件不动）
用法：python3 tools/cachebust.py [html 文件 …]（不给参数 = 仓库里全部 HTML）
"""
import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}


def ver(path):
    path = os.path.normpath(path)
    if path not in _cache:
        with open(path, 'rb') as f:
            _cache[path] = hashlib.sha1(f.read()).hexdigest()[:10]
    return _cache[path]


def write_if_changed(p, s):
    old = open(p, encoding='utf-8').read()
    if old != s:
        open(p, 'w', encoding='utf-8').write(s)
        return True
    return False


JSON_RE = re.compile(r"""fetch\((['"])((?:\.\./)*data/[^'"?]+\.json)(?:\?v=[0-9a-f]+)?\1\)""")
REF_RE = re.compile(r"""\b(href|src)=(["'])(?!https?:|//|data:|#|mailto:)([^"'?#]+\.(?:css|js))(?:\?v=[0-9a-f]+)?\2""")


def bust_js(js_path):
    d = os.path.dirname(js_path)
    s = open(js_path, encoding='utf-8').read()

    def rep(m):
        # JS 里的 fetch 路径相对于引用它的 HTML（都在站点根目录），这里按仓库根解析
        target = os.path.join(ROOT, m.group(2))
        if not os.path.exists(target):
            return m.group(0)
        return f"fetch({m.group(1)}{m.group(2)}?v={ver(target)}{m.group(1)})"
    return write_if_changed(js_path, JSON_RE.sub(rep, s))


def bust_html(html_path):
    d = os.path.dirname(html_path)
    s = open(html_path, encoding='utf-8').read()

    def rep(m):
        target = os.path.join(d, m.group(3))
        if not os.path.isfile(target):
            return m.group(0)
        return f'{m.group(1)}={m.group(2)}{m.group(3)}?v={ver(target)}{m.group(2)}'
    return write_if_changed(html_path, REF_RE.sub(rep, s))


def main(args):
    os.chdir(ROOT)
    files = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard'], capture_output=True, text=True).stdout.split()
    files = [f for f in files if '_v1.' not in f]  # pcb_v1.* 是冻结存档，不动
    js = [f for f in files if f.endswith('.js') and not f.startswith('vendor/') and 'fetch(' in open(f, encoding='utf-8', errors='ignore').read()]
    nj = sum(bust_js(os.path.join(ROOT, f)) for f in js)
    htmls = args or [f for f in files if f.endswith('.html')]
    nh = sum(bust_html(os.path.join(ROOT, f)) for f in htmls)
    print(f'cachebust: {nj} 个 JS、{nh} 个 HTML 更新了版本号')


if __name__ == '__main__':
    main(sys.argv[1:])
