#!/usr/bin/env python3
"""批量替换alert()为toast通知"""
import re
import os
import glob

TOAST_TEMPLATE = """function showToast(msg){const t=document.createElement('div');t.textContent=msg;t.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:10px 24px;border-radius:8px;z-index:99999;font-size:14px;animation:toastIn .3s ease';document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
document.head.insertAdjacentHTML('beforeend','<style>@keyframes toastIn{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}</style>')"""

TOAST_MAP = [
    # 复制成功
    (r"alert\(['\"]Copied to clipboard!['\"]\)", "showToast('Copied!')"),
    (r"alert\(['\"]Copied!['\"]\)", "showToast('Copied!')"),
    (r"alert\(['\"]Copied['\"]\)", "showToast('Copied!')"),
    # 复制失败
    (r"alert\(['\"]Copy failed['\"]\)", "showToast('Copy failed')"),
    (r"alert\(['\"]Copy failed!['\"]\)", "showToast('Copy failed')"),
    # 通用提示
    (r"alert\(['\"]([^'\"]{1,80})['\"]\)", lambda m: f"showToast('{m.group(1)}')"),
]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # 先检查是否有alert
    if 'alert(' not in content:
        return False
    
    # 确保有showToast函数
    if 'function showToast' not in content and 'function showToast(' not in content:
        # 在</script>前插入toast
        content = content.replace('</script>', TOAST_TEMPLATE + '\n</script>', 1)
        changed = True
    
    # 替换alert调用
    for pattern, replacement in TOAST_MAP:
        if callable(replacement):
            new_content = re.sub(pattern, replacement, content)
        else:
            new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base = '/home/chison/tools-site'
    html_files = glob.glob(os.path.join(base, 'en', '**', 'index.html'), recursive=True)
    cn_files = glob.glob(os.path.join(base, '*', 'index.html'), recursive=True)
    cn_files = [f for f in cn_files if '/en/' not in f]
    
    all_files = html_files + cn_files
    
    count = 0
    for f in all_files:
        if process_file(f):
            count += 1
            print(f"Fixed: {f}")
    
    print(f"\nTotal fixed: {count}")

if __name__ == '__main__':
    main()