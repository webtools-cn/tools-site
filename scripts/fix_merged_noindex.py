#!/usr/bin/env python3
"""为 merged tool 重定向页面添加 noindex 并优化 meta description"""
import glob, re, os

merged_files = []
for f in glob.glob('en/*/index.html'):
    with open(f) as fh:
        c = fh.read()
    if 'merged tool' in c.lower() and 'Redirecting' in c:
        merged_files.append(f)

print(f'Found {len(merged_files)} merged redirect pages')

fixed = 0
for f in merged_files:
    with open(f) as fh:
        content = fh.read()
    
    modified = False
    new_content = content
    
    # 1. 添加 noindex (如果没有)
    if 'noindex' not in content:
        # 在 <meta charset 之后添加
        new_content = new_content.replace(
            '<meta charset="UTF-8">',
            '<meta charset="UTF-8">\n<meta name="robots" content="noindex, follow">'
        )
        modified = True
    
    # 2. 优化 description - 从 merged into 提取目标工具名
    m = re.search(r'merged into.*?<a[^>]*>([^<]+)</a>', content)
    target_tool = m.group(1).strip() if m else ''
    
    # 提取工具名
    tool_name = os.path.basename(os.path.dirname(f))
    readable_name = tool_name.replace('-', ' ').title()
    
    new_desc = f'{readable_name} has moved. Use our free {target_tool} instead — same great features, no signup required.'
    if len(new_desc) > 160:
        new_desc = f'{readable_name} has moved — try our free {target_tool} tool instead. No signup, works in browser.'
    
    # Replace description
    old_desc_pattern = r'<meta name="description" content="[^"]*">'
    new_content = re.sub(old_desc_pattern, f'<meta name="description" content="{new_desc}">', new_content)
    modified = True
    
    if modified:
        with open(f, 'w') as fh:
            fh.write(new_content)
        fixed += 1

print(f'Fixed {fixed} pages')