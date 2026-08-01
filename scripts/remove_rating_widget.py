#!/usr/bin/env python3
"""删除所有工具页的假评分widget（rating-widget）"""
import os, re, glob

def remove_rating_widget(content):
    """删除rating-widget相关HTML/CSS/JS"""
    original = content
    
    # 1. 删除rating-widget HTML div (多种格式)
    content = re.sub(r'<div\s+class="rating-widget"[^>]*>.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div\s+class="rating-widget"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    
    # 2. 删除rating-widget CSS
    content = re.sub(r'\.rating-widget\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-widget\s*\.[^{]*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-widget\s+[^{]*\{[^}]*\}', '', content)
    content = re.sub(r'\.stars\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.stars\s*\.\w+\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-text\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-count\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.rating-thanks\s*\{[^}]*\}', '', content)
    
    # 3. 删除rating-widget JS函数
    content = re.sub(r'function\s+getConsistentRating\s*\(\)\s*\{.*?return\s*\{[^}]*\}\s*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'function\s+initRating\s*\(\)\s*\{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'function\s+updateDisplay\s*\([^)]*\)\s*\{.*?\}', '', content, flags=re.DOTALL)
    
    # 4. 删除rating相关的调用和变量
    content = re.sub(r"const\s+STORAGE_KEY\s*=\s*'wt_rating_'.*?;", '', content)
    content = re.sub(r'initRating\(\);?', '', content)
    content = re.sub(r'updateDisplay\([^)]*\);?', '', content)
    
    # 5. 清理多余空行
    content = re.sub(r'\n{4,}', '\n\n', content)
    
    return content if content != original else None

os.chdir('/home/chison/tools-site')

# 处理CN页面
cn_files = glob.glob('*/index.html')
cn_count = 0
for f in cn_files:
    if f == 'index.html' or f.startswith('en/'):
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'rating-widget' not in content and 'getConsistentRating' not in content:
        continue
    result = remove_rating_widget(content)
    if result:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(result)
        cn_count += 1

# 处理EN页面
en_files = glob.glob('en/*/index.html')
en_count = 0
for f in en_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'rating-widget' not in content and 'getConsistentRating' not in content:
        continue
    result = remove_rating_widget(content)
    if result:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(result)
        en_count += 1

print(f'CN修改: {cn_count} 页')
print(f'EN修改: {en_count} 页')
