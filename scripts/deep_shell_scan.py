#!/usr/bin/env python3
"""深度扫描空壳工具 - 检查有交互UI但无真实JS业务逻辑的页面"""
import os, re, sys

shells = []

for root, dirs, files in os.walk('.'):
    if '/.git' in root or '/node_modules' in root:
        continue
    for f in files:
        if f != 'index.html':
            continue
        filepath = os.path.join(root, f)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except:
            continue
        
        # 跳过重定向页面
        if 'meta http-equiv="refresh"' in content[:500]:
            continue
        
        # 检查是否有 onclick="process()" 调用
        has_process_call = 'onclick="process()"' in content
        has_toolInput = 'id="toolInput"' in content
        
        # 提取所有script内容
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        js = '\n'.join(scripts)
        
        # 检查是否有 process 函数定义
        process_match = re.search(r'function\s+process\s*\([^)]*\)\s*\{', js)
        
        if has_process_call and has_toolInput:
            if not process_match:
                # 有process()调用但没定义 -> 模板空壳
                shells.append(('NO_PROCESS_DEF', filepath))
            else:
                # 提取process函数体检查是否空壳
                start = process_match.end() - 1  # position of {
                depth = 0
                end = start
                for i in range(start, len(js)):
                    if js[i] == '{':
                        depth += 1
                    elif js[i] == '}':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                body = js[start+1:end-1].strip()
                
                # 检查是否空壳：短函数体 + 无业务关键字
                # 注意：getElementById/querySelector 只是DOM访问，不算业务逻辑
                business_keywords = ['Math.', 'split', 'replace', 'join', 'map', 'filter',
                                    'reduce', 'parse', 'JSON', 'for ', 'while ', 'if ',
                                    'addEventListener', 'fetch', 'canvas', 'getContext',
                                    'crypto', 'btoa', 'atob',
                                    'charCodeAt', 'fromCharCode', 'toString(', 'parseInt',
                                    'parseFloat', '.test(', '.exec(', '.match(']
                has_business = any(kw in body for kw in business_keywords)

                # 回显型空壳：var output = input 或 .textContent = input
                is_echo = ('var output = input' in body or
                          'output.textContent = input' in body or
                          'output.value = input' in body)

                if (len(body) < 250 and not has_business) or is_echo:
                    shells.append(('STUB_BODY', filepath, body[:150]))

# 也检查 "重写的函数实现" 标记后面是否跟了 var output = input 回显
for root, dirs, files in os.walk('.'):
    if '/.git' in root or '/node_modules' in root:
        continue
    for f in files:
        if f != 'index.html':
            continue
        filepath = os.path.join(root, f)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except:
            continue
        
        if '重写的函数实现' in content or '// === Implementation ===' in content:
            # 检查标记后面是否有 var output = input 回显
            for marker in ['重写的函数实现', '// === Implementation ===']:
                idx = content.find(marker)
                while idx != -1:
                    after = content[idx:idx+500]
                    if 'var output = input' in after and 'Generated at' in after:
                        shells.append(('STUB_MARKER', filepath, marker))
                        break
                    idx = content.find(marker, idx + 1)

print(f"Found {len(shells)} potential shells:")
for s in shells:
    print(f"  {s}")
