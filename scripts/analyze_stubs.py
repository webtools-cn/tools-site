#!/usr/bin/env python3
"""批量识别和处理空壳工具的stub函数"""
import os, re

site_dir = '/home/chison/tools-site'
results = {'mode2_delete': [], 'mode3_implement': []}

for root, dirs, files in os.walk(site_dir):
    if 'en' in root.split(os.sep):
        continue  # skip EN pages for now
    for fname in files:
        if fname != 'index.html':
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if 'coming soon' not in content:
            continue
        
        tool_name = os.path.basename(os.path.dirname(fpath))
        
        # Find stub section
        stub_marker = '// === 重写的函数实现 ==='
        stub_idx = content.find(stub_marker)
        if stub_idx == -1:
            continue
        
        # Get function names in stub section
        stub_section = content[stub_idx:]
        stub_funcs = re.findall(r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*coming soon[^}]*\}', stub_section)
        
        # Check if these functions have real implementations before the stub section
        before_stub = content[:stub_idx]
        
        has_real_impl = False
        for func_name in stub_funcs:
            # Check for window.funcName= or function funcName with real body before stub
            patterns = [
                r'window\.' + re.escape(func_name) + r'\s*=',
                r'function\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*\{(?:(?!coming soon).)*\}',
            ]
            for pat in patterns:
                if re.search(pat, before_stub, re.DOTALL):
                    has_real_impl = True
                    break
        
        # Also check for non-stub functions in the stub section (clearAll, copyResult etc that work)
        non_stub_funcs = re.findall(r'function\s+(\w+)\s*\([^)]*\)\s*\{(?:(?!coming soon).)*\}', stub_section)
        
        if has_real_impl:
            results['mode2_delete'].append(tool_name)
        else:
            results['mode3_implement'].append(tool_name)

print(f"Mode 2 (delete stub, real impl exists): {len(results['mode2_delete'])}")
for t in results['mode2_delete']:
    print(f"  - {t}")

print(f"\nMode 3 (need implementation): {len(results['mode3_implement'])}")
for t in results['mode3_implement']:
    print(f"  - {t}")
