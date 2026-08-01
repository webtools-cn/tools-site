#!/usr/bin/env python3
"""第二轮：删除残留的getConsistentRating等假评分JS函数"""
import os, re, glob

def remove_rating_js(content):
    """删除假评分相关JS函数和调用"""
    original = content
    
    # 1. 删除getConsistentRating函数（多行，含嵌套大括号）
    # 用状态机方式匹配
    while 'getConsistentRating' in content:
        idx = content.find('function getConsistentRating')
        if idx == -1:
            break
        # 找到函数体的匹配大括号
        brace_count = 0
        start = content.find('{', idx)
        if start == -1:
            break
        brace_count = 1
        i = start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        content = content[:idx] + content[i:]
    
    # 2. 删除initRating函数
    while 'function initRating' in content:
        idx = content.find('function initRating')
        if idx == -1:
            break
        start = content.find('{', idx)
        if start == -1:
            break
        brace_count = 1
        i = start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        content = content[:idx] + content[i:]
    
    # 3. 删除updateDisplay函数
    while 'function updateDisplay' in content:
        idx = content.find('function updateDisplay')
        if idx == -1:
            break
        start = content.find('{', idx)
        if start == -1:
            break
        brace_count = 1
        i = start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        content = content[:idx] + content[i:]
    
    # 4. 删除相关调用
    content = re.sub(r"var\s+avgData\s*=\s*getConsistentRating\(\)\s*;?", '', content)
    content = re.sub(r"if\s*\(!avgData\)\s*avgData\s*=\s*getConsistentRating\(\)\s*;?", '', content)
    content = re.sub(r'avgData\.value\s*\|\|\s*4\.5', '4.5', content)
    content = re.sub(r'avgData\.count\s*\|\|\s*128', '128', content)
    content = re.sub(r"const\s+STORAGE_KEY\s*=\s*'wt_rating_'.*?;", '', content)
    content = re.sub(r'initRating\(\)\s*;?', '', content)
    content = re.sub(r'updateDisplay\([^)]*\)\s*;?', '', content)
    
    # 5. 删除.stars和.star相关的CSS（残留）
    content = re.sub(r'\.stars\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.stars\s+\.star\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.stars\s+\.star:hover\s*,?\s*\.stars\s+\.star\.active\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.star\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.star\.active\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-text\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-count\s*\{[^}]*\}', '', content)
    
    # 6. 清理多余空行
    content = re.sub(r'\n{4,}', '\n\n', content)
    
    return content if content != original else None

os.chdir('/home/chison/tools-site')

# 处理所有CN工具页
cn_count = 0
for f in glob.glob('*/index.html'):
    if f == 'index.html' or f.startswith('en/'):
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'getConsistentRating' not in content:
        continue
    result = remove_rating_js(content)
    if result:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(result)
        cn_count += 1

# 处理所有EN工具页
en_count = 0
for f in glob.glob('en/*/index.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'getConsistentRating' not in content:
        continue
    result = remove_rating_js(content)
    if result:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(result)
        en_count += 1

print(f'CN修改: {cn_count} 页')
print(f'EN修改: {en_count} 页')
