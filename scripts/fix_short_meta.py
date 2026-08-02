#!/usr/bin/env python3
"""批量扩写CN短meta description到120-160字符"""
import os, re, json

# Load tools data - format: {category: [[emoji, name, desc, url], ...]}
with open('tools-data-cn.json', 'r', errors='ignore') as f:
    tools_data = json.load(f)

tool_info = {}
for cat, tools in tools_data.items():
    for t in tools:
        if len(t) < 4: continue
        name = t[1]  # name
        desc = t[2]  # description
        slug = t[3].strip('/').split('/')[-1] if t[3] else ''
        if slug:
            tool_info[slug] = {'name': name, 'desc': desc, 'cat': cat}

fixed = 0

for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    m = re.search(r'<meta name="description" content="([^"]*)"', c)
    if not m: continue
    desc = m.group(1)
    l = len(desc)
    
    if l >= 100: continue
    
    info = tool_info.get(d, {})
    name = info.get('name', '')
    json_desc = info.get('desc', '')
    
    # Use JSON description if available and longer
    if json_desc and len(json_desc) > l:
        new_desc = json_desc
    elif l < 30:
        new_desc = f"{name}在线工具，{desc}。支持实时计算与预览，无需注册，完全免费，所有数据本地处理不上传。"
    elif l < 60:
        new_desc = f"{desc}。支持实时计算与预览，无需注册，完全免费，数据本地处理不上传服务器。"
    else:
        new_desc = f"{desc}。无需注册，完全免费，数据本地处理。"
    
    # Trim to 160 chars max
    if len(new_desc) > 160:
        new_desc = new_desc[:157] + "..."
    
    # If still too short, pad
    if len(new_desc) < 100:
        new_desc = f"{new_desc} 支持多种输入格式，操作简单快捷。"
        if len(new_desc) > 160:
            new_desc = new_desc[:157] + "..."
    
    old = f'<meta name="description" content="{desc}"'
    new = f'<meta name="description" content="{new_desc}"'
    c = c.replace(old, new, 1)
    open(p, 'w', encoding='utf-8', errors='ignore').write(c)
    fixed += 1

print(f"CN meta description fixed: {fixed}")
