#!/usr/bin/env python3
"""T699: 批量标准化CN工具title - 替换"纯前端"→"无需注册" + 去重复"""
import os
import re
import glob

BASE_DIR = '/home/chison/tools-site'
files = glob.glob(f'{BASE_DIR}/**/index.html', recursive=True)

EXCLUDE_DIRS = ['en/', 'scripts/', 'quality/', 'chrome-extension/', '.git/', '_gen/', 'node_modules/', 'cron-reports/', 'docs/', 'tools/', 'category/']

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
    
    original = content
    
    # 匹配 <title>...</title>
    title_match = re.search(r'<title>(.*?)</title>', content)
    if not title_match:
        continue
    old_title = title_match.group(1)
    new_title = old_title
    
    # 1. 替换"|纯前端"→"|无需注册"（如果在title中）
    if '|纯前端' in new_title or '｜纯前端' in new_title:
        new_title = new_title.replace('|纯前端', ' | 无需注册')
        new_title = new_title.replace('｜纯前端', ' | 无需注册')
        changed = True
    
    # 2. 替换"|免费在线工具|无需注册"去重复
    new_title = re.sub(r'\| 免费在线工具\s*\| 无需注册', ' | 无需注册', new_title)
    new_title = re.sub(r'\| 免费在线工具\s*\|', ' | 无需注册 |', new_title)
    
    # 3. "纯前端本地处理"在title中的替换（已由上一步脚本处理，这里保底）
    new_title = new_title.replace('纯前端本地处理', '无需注册')
    
    # 4. 去emoji
    new_title = re.sub(r'[📄🎹🎵🎶🎸🥁🎧🎤🎼📋📝✏️✂️📐📏🔧🔨⚙️🛠️💻🖥️⌨️🖱️🖨️📱]', '', new_title)
    
    # 5. 清理多余空格
    new_title = re.sub(r'\s+', ' ', new_title).strip()
    new_title = re.sub(r'\s*\|', ' |', new_title)
    new_title = re.sub(r'\|\s*', '| ', new_title)
    
    # 6. 防止双竖线
    new_title = re.sub(r'\|\s*\|', '|', new_title)
    
    if new_title != old_title:
        content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
        
        # 同步og:title
        og_match = re.search(r'<meta property="og:title" content="(.*?)">', content)
        if og_match:
            old_og = og_match.group(1)
            # 简单替换
            new_og = new_title
            content = content.replace(f'<meta property="og:title" content="{old_og}">', f'<meta property="og:title" content="{new_og}">')
        
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        modified += 1
        if modified <= 15:
            print(f'  {rel}: {old_title[:60]} → {new_title[:60]}')

print(f'\nTotal CN titles modified: {modified}')