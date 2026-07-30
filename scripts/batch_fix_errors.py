#!/usr/bin/env python3
"""
批量修复多种JS错误：
1. 全局作用域中的 return → 包进 IIFE
2. container is not defined → 添加 var container = document.querySelector('...')
3. 缺失的事件处理器函数 → 添加占位函数
"""
import subprocess, json, os, re

TOOLS_DIR = '/home/chison/tools-site'

# 从L0报告获取失败列表
with open(f'{TOOLS_DIR}/quality-reports/puppeteer-L0.json') as f:
    data = json.load(f)

# 分组
illegal_return = [f['tool'] for f in data['failures'] if 'Illegal return' in f.get('reason','')]
container_not_defined = [f['tool'] for f in data['failures'] if 'container is not defined' in f.get('reason','')]

print(f'Illegal return: {len(illegal_return)}')
print(f'Container not defined: {len(container_not_defined)}')

# 只处理Illegal return中还没通过的（avif-to-jpg, bandwidth-calculator, json-to-elixir, markdown-slides, pdf-ocr已通过）
skip_tools = {'avif-to-jpg', 'bandwidth-calculator', 'json-to-elixir', 'markdown-slides', 'pdf-ocr'}

def add_iife_if_needed(content):
    """检测全局作用域的return并包装"""
    # 找所有 <script> 块（排除 type=application/ld+json 等）
    # 简单策略：在第一个非特殊script块中，找不在function内的return
    # 更实用的方法：检测 return 前面有没有 function 关键字，如果没有则包装
    
    # 先找到主script块（排除 application/ld+json 和 gtag）
    # 找最后一个包含大量JS代码的script块
    script_blocks = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
    
    for m in reversed(script_blocks):
        js_code = m.group(1)
        # 跳过只有桥接代码的小块
        if len(js_code) < 200:
            continue
        
        # 检查是否有全局return（不在function内的return）
        # 简化：找所有 'return' 前面是否有 'function' 
        # 如果代码块有不在function内的return，包进IIFE
        lines = js_code.split('\n')
        depth = 0
        has_global_return = False
        
        for line in lines:
            stripped = line.strip()
            # 追踪大括号深度
            depth += stripped.count('{') - stripped.count('}')
            # 跳过函数定义行
            if 'function' in stripped:
                continue
            # 在深度0或1（IIFE开头/结尾）检测return
            if re.search(r'\breturn\b', stripped) and depth <= 1:
                # 确认不是在函数内
                if not re.search(r'function\s+\w+\s*\(', stripped):
                    has_global_return = True
                    break
        
        if has_global_return:
            # 把整个script内容包进IIFE（除了函数声明）
            # 策略：找到第一个不在函数内的语句，从那里开始包
            new_code = js_code
            # 先看是否已经有IIFE包装
            if '(function()' in js_code[:50]:
                continue
            
            # 简化：把整个块除了已定义的函数外包装
            # 找到第一个 function 声明
            first_func = re.search(r'^function\s+\w+', js_code, re.MULTILINE)
            if first_func:
                prefix = js_code[:first_func.start()]
                suffix = js_code[first_func.start():]
                if prefix.strip():
                    new_code = '(function(){\n' + prefix + '\n})();\n' + suffix
            else:
                new_code = '(function(){\n' + js_code + '\n})();'
            
            content = content[:m.start()] + '<script>' + new_code + '</script>' + content[m.end():]
            return content
    
    return None

fixed_count = 0
for tool in illegal_return:
    if tool in skip_tools:
        continue
    
    filepath = os.path.join(TOOLS_DIR, tool, 'index.html')
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = add_iife_if_needed(content)
    if new_content and new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        print(f'Fixed IIFE: {tool}')

print(f'\nTotal IIFE fixed: {fixed_count}')