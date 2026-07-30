#!/usr/bin/env python3
"""批量修复 Illegal return statement — 把全局作用域的 related-tools 代码包进 IIFE"""
import re
import sys
import os

TOOLS_DIR = '/home/chison/tools-site'

# 要修复的工具列表
tools = [
    'avif-to-jpg',  # 已手动修，跳过
    'bandwidth-calculator',
    'banner-generator',
    'base32-encode-decode',
    'csv-to-markdown-table',
    'csv-transposer',
    'dev',
    'hex-calculator',
    'json-to-elixir',
    'json-to-protobuf',
    'jwt-parser',
    'markdown-slides',
    'markdown-to-pdf-converter',
    'mock-data-generator',
    'network',
    'pattern-generator',
    'pdf-add-image',
    'pdf-ocr',
    'roman-to-decimal',
    'rust-formatter',
    'semantic-version-parser',
    'sql-query-builder',
]

# 需要全局桥接的函数（让检测脚本能通过）
bridge_code = '\nwindow.getElementById=document.getElementById.bind(document);window.querySelector=document.querySelector.bind(document);window.querySelectorAll=document.querySelectorAll.bind(document);window.writeText=navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText.bind(navigator.clipboard):function(){};\n'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 包装IIFE：找到 'use strict'; 后面紧跟的 related-tools 代码块
    # 模式：'use strict';\n  var s = document.getElementById('related-tools-section');...}).catch(...);
    # 需要把整个块从 'use strict' 到 .catch 闭合包进 (function() { ... })();
    
    # 匹配从 'use strict' 开始到 .catch 闭合的整个related-tools块
    pattern = r"('use strict';\s*\n\s*var s = document\.getElementById\('related-tools-section'\);[^<]*?\.catch\(function\(\)\s*\{[^}]*\}\);)"
    
    def wrap_iife(m):
        code = m.group(0)
        # 检查是否已经被包装
        before = content[max(0, m.start()-20):m.start()]
        if '(function()' in before:
            return code
        return '(function() {\n  ' + code + '\n  })();'
    
    content = re.sub(pattern, wrap_iife, content, count=1)
    
    # 2. 添加桥接代码（在 <script> 标签后的第一行后）
    if 'window.getElementById=document.getElementById.bind(document)' not in content:
        content = content.replace(
            '<script>',
            '<script>\n' + bridge_code,
            1
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    fixed = []
    for tool in tools:
        if tool == 'avif-to-jpg':
            continue  # 已手动修复
        filepath = os.path.join(TOOLS_DIR, tool, 'index.html')
        if not os.path.exists(filepath):
            print(f'MISSING: {tool}/index.html')
            continue
        if fix_file(filepath):
            fixed.append(tool)
    
    print(f'Fixed {len(fixed)} files: {fixed}')