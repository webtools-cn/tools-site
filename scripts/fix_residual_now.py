#!/usr/bin/env python3
"""批量修复 no_adsense + title_long 残留"""
import os, re, sys

SITE = '/home/chison/tools-site'

ADSENSE_SCRIPT = '''    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1808725918793791" crossorigin="anonymous"></script>
'''

def get_all_files():
    files = []
    for root, dirs, fnames in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('.git','.gsc-data','scripts','css','js','docs','quality','blog','node_modules')]
        for f in fnames:
            if f == 'index.html':
                files.append(os.path.join(root, f))
    return files

def fix_no_adsense(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'adsbygoogle' in c:
        return False
    if 'noindex' in c and 'content="noindex' in c:
        return False  # noindex页面不需要adsense
    
    # 在</head>前插入
    head_end = c.find('</head>')
    if head_end == -1:
        return False
    
    c = c[:head_end] + ADSENSE_SCRIPT + c[head_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

def fix_title_long(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    tm = re.search(r'<title>([^<]+)</title>', c)
    if not tm:
        return False
    t = tm.group(1)
    if len(t) <= 60:
        return False
    
    # 策略：去掉"Free Online"前缀，缩短核心名
    nt = t
    # 先尝试移除冗余前缀
    for prefix in ['Free Online ', 'Free online ', 'Online ', 'free online ']:
        if nt.startswith(prefix):
            nt = nt[len(prefix):]
            break
    
    # 如果还是太长，截断核心名
    if len(nt) > 60:
        # 找到 " - Free ToolBase" 或类似后缀
        suffix = ''
        for sfx in [' - Free ToolBase', ' - free-toolbase.com', ' | Free ToolBase']:
            if sfx in nt:
                suffix = sfx
                nt = nt.replace(sfx, '')
                break
        
        max_core = 60 - len(suffix) - 1  # -1 for …
        if max_core > 5:
            nt = nt[:max_core-1] + '…' + suffix
    
    if len(nt) <= 60 and nt != t:
        c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    
    return False

files = get_all_files()
print(f"扫描 {len(files)} 个文件")

no_adsense_fixed = 0
title_fixed = 0

for f in files:
    if fix_no_adsense(f):
        no_adsense_fixed += 1
        print(f"  [adsense] {os.path.relpath(f, SITE)}")
    if fix_title_long(f):
        title_fixed += 1
        print(f"  [title] {os.path.relpath(f, SITE)}")

print(f"\n修复: no_adsense={no_adsense_fixed}, title_long={title_fixed}")