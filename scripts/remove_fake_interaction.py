#!/usr/bin/env python3
"""批量删除EN版工具页面中的假交互区域（quickInput/quickResult）"""
import os
import re
import sys

def remove_fake_interaction(filepath):
    """Remove the auto-injected minimal interaction div from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: <!-- auto-injected minimal interaction --> followed by the div
    pattern = r'\s*<!-- auto-injected minimal interaction -->\s*\n<div style="margin-top:16px;padding:16px;background:rgba\(99,102,241,\.06\);border:1px dashed rgba\(99,102,241,\.2\);border-radius:8px">.*?</div>\s*\n'
    
    new_content = re.sub(pattern, '\n', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    en_dir = os.path.join(base_dir, 'en')
    
    if not os.path.isdir(en_dir):
        print("EN directory not found")
        return
    
    fixed = 0
    failed = []
    
    for tool_name in sorted(os.listdir(en_dir)):
        tool_path = os.path.join(en_dir, tool_name, 'index.html')
        if not os.path.isfile(tool_path):
            continue
        
        try:
            if remove_fake_interaction(tool_path):
                fixed += 1
                print(f"  ✅ Fixed: en/{tool_name}/index.html")
        except Exception as e:
            failed.append(f"en/{tool_name}: {e}")
    
    print(f"\n完成: 修复了 {fixed} 个文件")
    if failed:
        print(f"失败 {len(failed)} 个:")
        for f in failed:
            print(f"  ❌ {f}")

if __name__ == '__main__':
    main()
