#!/usr/bin/env python3
"""验证28页JS语法 — 提取所有非JSON-LD的<script>块, 用node --check逐个验证"""
import re, subprocess, sys

PAGES = [
    'audio-joiner/index.html',
    'contrast-ratio-checker/index.html',
    'css-at-starting-style-generator/index.html',
    'css-variable-extractor/index.html',
    'drum-machine/index.html',
    'en/asset-allocation-calculator/index.html',
    'en/audio-joiner/index.html',
    'en/base58-encoder/index.html',
    'en/calendar-printable/index.html',
    'en/code-highlighter/index.html',
    'en/color-picker-hex/index.html',
    'en/content-repurposer/index.html',
    'en/contrast-ratio-checker/index.html',
    'en/crc32-calculator/index.html',
    'en/css-content-visibility-generator/index.html',
    'en/css-drop-cap-generator/index.html',
    'en/css-formatter/index.html',
    'en/css-image-rendering-generator/index.html',
    'en/css-keyframe-animation-generator/index.html',
    'en/css-parallax-generator/index.html',
    'en/css-ribbon-generator/index.html',
    'en/css-scroll-snap-generator/index.html',
    'en/css-selection-color-generator/index.html',
    'en/css-text-overflow-generator/index.html',
    'en/css-transition-generator/index.html',
    'en/css-user-select-generator/index.html',
    'en/css-variable-extractor/index.html',
    'en/css-view-transition-generator/index.html',
]

def get_scripts(content):
    scripts = []
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL):
        attrs, body = m.group(1), m.group(2)
        if 'application/ld+json' in attrs or 'src=' in attrs or 'type="application/json"' in attrs:
            continue
        body = body.strip()
        if body:
            scripts.append(body)
    return scripts

def check_page(path):
    with open(path) as f:
        content = f.read()
    scripts = get_scripts(content)
    if not scripts:
        return False, ['NO_JS']
    errors = []
    for i, body in enumerate(scripts):
        with open('/tmp/jsfix/verify_block.js', 'w') as f:
            f.write(body)
        r = subprocess.run(['node', '-c', '/tmp/jsfix/verify_block.js'],
                           capture_output=True, text=True, timeout=15)
        if r.returncode != 0:
            errors.append(f'block#{i}: {r.stderr.strip().splitlines()[0] if r.stderr.strip() else "?"}')
    return (len(errors) == 0), errors

def main():
    root = '/home/chison/tools-site'
    ok, fail = [], []
    for p in PAGES:
        path = f'{root}/{p}'
        passed, errors = check_page(path)
        if passed:
            ok.append(p)
            print(f'PASS: {p}')
        else:
            fail.append((p, errors))
            print(f'FAIL: {p}')
            for e in errors:
                print(f'       {e}')
    print(f'\n===== 结果 =====')
    print(f'通过: {len(ok)}/{len(PAGES)}')
    print(f'失败: {len(fail)}/{len(PAGES)}')
    if fail:
        for p, e in fail:
            print(f'  FAIL: {p}')
            for x in e:
                print(f'    {x}')

if __name__ == '__main__':
    main()
