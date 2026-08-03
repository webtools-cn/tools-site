#!/usr/bin/env python3
"""批量删除模式2的stub函数（真实实现存在，stub覆盖了它）"""
import os, re

site_dir = '/home/chison/tools-site'
tools_to_fix = [
    'pdf-crop', 'regex-crossword', 'pdf-merge', 'ip-cidr-merger',
    'css-animation-builder', 'svg-icon-search', 'css-z-index-manager',
    'recipe-cost-calculator', 'eye-test', 'yaml-merger',
    'crypto-tax-calculator', 'pem-parser', 'gradient-css-generator',
    'json-pointer-explorer', 'text-similarity-calculator', 'subscription-auditor'
]

fixed = 0
for tool in tools_to_fix:
    fpath = os.path.join(site_dir, tool, 'index.html')
    if not os.path.exists(fpath):
        print(f"SKIP {tool}: file not found")
        continue
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'coming soon' not in content:
        print(f"SKIP {tool}: no 'coming soon' found")
        continue
    
    stub_marker = '// === 重写的函数实现 ==='
    stub_idx = content.find(stub_marker)
    if stub_idx == -1:
        print(f"SKIP {tool}: no stub marker found")
        continue
    
    # Find the end of the stub section - it goes until </script>
    script_end = content.find('</script>', stub_idx)
    if script_end == -1:
        print(f"SKIP {tool}: no </script> after stub")
        continue
    
    stub_section = content[stub_idx:script_end]
    
    # Find all functions in the stub section
    # Only remove functions that contain "coming soon"
    # Keep functions that have real implementations (clearAll, copyResult, etc.)
    
    # Strategy: parse function by function
    lines = stub_section.split('\n')
    new_lines = []
    skip_until_close = False
    brace_depth = 0
    current_func_has_coming_soon = False
    func_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a function definition
        func_match = re.match(r'^\s*function\s+(\w+)\s*\(', line)
        
        if func_match and not skip_until_close:
            # Start collecting function
            func_lines = [line]
            brace_depth = line.count('{') - line.count('}')
            current_func_has_coming_soon = 'coming soon' in line
            i += 1
            while i < len(lines) and brace_depth > 0:
                func_lines.append(lines[i])
                current_func_has_coming_soon = current_func_has_coming_soon or 'coming soon' in lines[i]
                brace_depth += lines[i].count('{') - lines[i].count('}')
                i += 1
            
            if not current_func_has_coming_soon:
                # Keep this function (it's a real implementation like clearAll)
                new_lines.extend(func_lines)
            # else: skip (delete) this function
        else:
            new_lines.append(line)
            i += 1
    
    new_stub_section = '\n'.join(new_lines)
    
    # Also remove the stub marker line if no functions remain
    # Check if there are any function definitions left after the marker
    remaining_funcs = re.findall(r'function\s+\w+\s*\(', new_stub_section)
    
    if len(remaining_funcs) == 0:
        # Remove the entire stub section including marker
        new_content = content[:stub_idx] + content[script_end:]
    else:
        new_content = content[:stub_idx] + new_stub_section + content[script_end:]
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    fixed += 1
    print(f"FIXED {tool}")

print(f"\nTotal fixed: {fixed}")
