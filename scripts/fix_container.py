#!/usr/bin/env python3
"""批量修复 container is not defined"""
import os, re

TOOLS_DIR = '/home/chison/tools-site'

tools = [
    'ai-sentence-rewriter', 'audio-normalize', 'audio-volume-adjuster',
    'bitwise-calculator', 'cagr-calculator', 'cidr-calculator',
    'data-url-converter', 'decimal-to-roman', 'email-security-checker',
    'excel-to-pdf', 'favicon-downloader', 'hex-encoder-decoder',
    'hsl-to-rgb', 'ico-converter', 'image-resize', 'jpg-to-webp',
    'json-merge-patch', 'json-to-table', 'log-viewer', 'md5-hash',
]

def fix_container(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # container not defined通常出现在模式:
    # 1. if (!container ...) 
    # 2. container.querySelector...
    # 需要在使用前加定义
    
    # 策略：在第一个使用container的函数开头，找到var声明区域，插入var container定义
    # 模式：function xxx() { ... if (!container || ...) 
    
    if 'container is not defined' not in content and '!container' not in content:
        # 页面上不包含这个错误模式，跳过
        return False
    
    # 在script块中找到initRating或类似评级函数，在开头加定义
    # 更通用的方法：在第一个使用container的代码前加 var container = document.querySelector(...)
    
    # 找到 var text = ... 附近的 container引用
    # 模式: function initRating() {\n    ...\n    if (!container || !text) return;
    pattern = r'(function\s+\w+\(\)\s*\{[^}]*?)(\s*if\s*\(!container\s*\|\|\s*!text\)\s*return)'
    
    def add_def(m):
        fn_start = m.group(1)
        if_check = m.group(2)
        # 在fn开头（{之后）加定义
        if 'var container' not in fn_start:
            fn_start = fn_start.replace('{', '{\n  var container=document.querySelector(\'.rating-container\')||document.querySelector(\'.container\');var text=document.querySelector(\'.rating-text\');')
        return fn_start + if_check
    
    content = re.sub(pattern, add_def, content, count=1)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

fixed = []
for tool in tools:
    filepath = os.path.join(TOOLS_DIR, tool, 'index.html')
    if not os.path.exists(filepath):
        continue
    if fix_container(filepath):
        fixed.append(tool)

print(f'Fixed {len(fixed)}: {fixed}')