#!/usr/bin/env python3
"""修复L1失败的页面：把stub中的 result/output 替换成页面实际存在的容器ID"""
import re, os

BASE = '/home/chison/tools-site'

# L1失败的页面
failed_l1 = {
    'ai-debate-generator': 'resultArea',
    'ai-prompt-generator': None,  # 需要检查
    'ai-system-prompt-generator': None,
    'api-key-generator': None,
    'alarm-clock': None,
    'aspect-ratio-calculator': None,
}

for tool, real_id in failed_l1.items():
    html_path = f'{BASE}/{tool}/index.html'
    if not os.path.exists(html_path):
        continue
    
    with open(html_path) as f:
        content = f.read()
    
    # 找页面中可能的输出容器
    output_ids = re.findall(r'id="(output|result|resultArea|resultText|resultBox|outputArea|outputBox|display)"', content)
    if not output_ids and not real_id:
        # 找所有看起来像容器的id
        output_ids = re.findall(r'id="(\w*(?:result|output|display|area|container|box)\w*)"', content)
    
    if output_ids:
        real_id = output_ids[0]
        print(f'{tool}: using id="{real_id}"')
    elif real_id:
        print(f'{tool}: using provided id="{real_id}"')
    else:
        print(f'{tool}: NO output container found, skip')
        continue
    
    # 替换 stub 中的 result 为实际id
    # 找到我们生成的stub块
    stub_pattern = re.compile(r'(\nfunction \w+\(\)\{var r=document\.getElementById\(\')[^\']*(\'[^}]*\}window\.\w+=\w+;)')
    new_content = stub_pattern.sub(f'\\1{real_id}\\2', content)
    
    with open(html_path, 'w') as f:
        f.write(new_content)
    
    print(f'  Fixed {tool}')
