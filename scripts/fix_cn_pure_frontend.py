#!/usr/bin/env python3
"""批量替换"纯前端本地处理"为"无需注册"（CN版）"""
import os
import re
import glob

BASE_DIR = '/home/chison/tools-site'
files = glob.glob(f'{BASE_DIR}/**/*.html', recursive=True)

EXCLUDE_DIRS = ['en/', 'scripts/', 'quality/', 'chrome-extension/', '.git/', '_gen/', 'node_modules/', 'cron-reports/', 'docs/']

modified = 0
for f in files:
    rel = os.path.relpath(f, BASE_DIR)
    if any(rel.startswith(d) for d in EXCLUDE_DIRS):
        continue
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except:
        continue
    
    if '纯前端本地处理' not in content:
        continue
    
    original = content
    
    # 1. 替换title中的"|纯前端本地处理"->"|无需注册"
    content = re.sub(r'\|纯前端本地处理', ' | 无需注册', content)
    # 2. 替换正文中的"纯前端本地处理"（但不替换已经有的"无需注册"后面的）
    content = content.replace('纯前端本地处理', '无需注册')
    # 3. 防止出现"无需注册|无需注册"或"无需注册无需注册"
    content = re.sub(r'无需注册\s*[|｜]\s*无需注册', '无需注册', content)
    content = re.sub(r'无需注册无需注册', '无需注册', content)
    # 4. 防止 title 里出现重复 "无需注册"
    # 匹配 "工具名 - 免费在线工具|无需注册" 变成 "工具名 - 无需注册在线"
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        modified += 1
        if modified <= 10:
            print(f'  Fixed: {rel}')

print(f'\nTotal files modified: {modified}')

# 验证：统计剩余
remaining = 0
for f in glob.glob(f'{BASE_DIR}/**/*.html', recursive=True):
    rel = os.path.relpath(f, BASE_DIR)
    if any(rel.startswith(d) for d in EXCLUDE_DIRS):
        continue
    try:
        with open(f, 'r') as fh:
            if '纯前端本地处理' in fh.read():
                remaining += 1
    except:
        pass
print(f'Remaining "纯前端本地处理" files: {remaining}')
