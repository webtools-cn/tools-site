#!/usr/bin/env python3
"""质量门：push 前全站检测（结构/中文/meta/字数/雷同度）
用法: python3 scripts/quality_gate.py [--fix]
退出码: 0=通过 1=有严重问题
"""
import re, os, glob, sys

FIX = '--fix' in sys.argv
skip = {'index.html', 'en/index.html'}
pages = [p for p in glob.glob('*/index.html') + glob.glob('en/*/index.html') if p not in skip and os.path.isfile(p)]

def visible_text(h):
    s = re.sub(r'<script.*?</script>', '', h, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', '', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

issues = {'struct': [], 'cn_in_en': [], 'meta_short': [], 'thin': [], 'dup': []}

# 1. 结构平衡 + 2. EN中文 + 3. meta + 4. 字数
for p in pages:
    h = open(p, encoding='utf-8', errors='ignore').read()
    s = re.sub(r'<script.*?</script>', '', h, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', '', s, flags=re.S | re.I)
    for tag in ['div', 'main', 'footer', 'section']:
        o = len(re.findall(r'<' + tag + r'[\s>]', s))
        c = s.count('</' + tag + '>')
        if o != c:
            issues['struct'].append((p, tag, o, c))
    txt = visible_text(h)
    if p.startswith('en/'):
        body = re.sub(r'<a[^>]*>中文</a>', '', s)
        cn = [x for x in re.findall(r'[\u4e00-\u9fff]{2,}', body) if x != '中文']
        if cn:
            issues['cn_in_en'].append((p, cn[:3]))
    m = re.search(r'name="description"\s+content="([^"]*)"', h)
    if m and len(m.group(1)) < 50:
        issues['meta_short'].append((p, len(m.group(1))))
    if '已迁移' not in h and 'http-equiv="refresh"' not in h.lower() and len(txt) < 500:
        issues['thin'].append((p, len(txt)))

# 5. 雷同度：常见模板句
templates = [
    '该工具完全在本地运行，您的数据不会上传到服务器，保障隐私安全',
    '该工具完全在浏览器端运行，无需安装任何软件，无需注册账号，打开网页即可使用',
    '所有输入数据仅在本地处理，不会上传到任何服务器，确保您的隐私安全',
    'No installation, no registration, just open and use',
    'All processing happens locally in your browser',
    'All processing is done locally',
]
dup_count = {t: 0 for t in templates}
for p in pages:
    h = open(p, encoding='utf-8', errors='ignore').read()
    t = visible_text(h)
    for tmpl in templates:
        if tmpl in t:
            dup_count[tmpl] += 1

print('=' * 50)
print('质量门报告')
print('=' * 50)
print(f'结构不平衡: {len(issues["struct"])}')
for p, tag, o, c in issues['struct'][:10]:
    print(f'  {p}: {tag} {o}v{c}')
print(f'EN含中文: {len(issues["cn_in_en"])}')
for p, cn in issues['cn_in_en'][:5]:
    print(f'  {p}: {cn}')
print(f'meta<50: {len(issues["meta_short"])}')
for p, n in issues['meta_short'][:5]:
    print(f'  {p}: {n}')
print(f'薄页<500: {len(issues["thin"])}')
for p, n in issues['thin'][:5]:
    print(f'  {p}: {n}')
print('雷同模板句:')
for t, n in dup_count.items():
    if n > 10:
        print(f'  [{n}页] {t[:40]}')
print('=' * 50)
n_issues = len(issues['struct']) + len(issues['cn_in_en']) + len(issues['meta_short']) + len(issues['thin'])
n_dup = sum(1 for n in dup_count.values() if n > 10)
print(f'严重问题: {n_issues} 个页面问题 + {n_dup} 类雷同')
sys.exit(1 if n_issues > 0 else 0)
