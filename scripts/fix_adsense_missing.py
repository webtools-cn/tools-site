#!/usr/bin/env python3
"""
修复缺少AdSense代码的页面
在 <meta charset="UTF-8"> 后面插入AdSense script标签
"""
import os
import re
import sys

ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

# 不需要AdSense的页面（验证文件、404、插件弹窗等）
SKIP_PATTERNS = [
    'googlefd',  # Google验证
    '404.html',
    'feedback-widget.html',
    'chrome-extension/',
]

def needs_skip(path):
    for p in SKIP_PATTERNS:
        if p in path:
            return True
    return False

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 跳过已有adsbygoogle的
    if 'adsbygoogle' in content:
        return 'skip'
    
    if needs_skip(filepath):
        return 'skip_legit'
    
    # 在 <meta charset="UTF-8"> 后插入
    # 使用不同的charset变体
    for pattern in [
        r'(<meta\s+charset=["\']UTF-8["\']\s*/?>)',
        r'(<meta\s+charset=["\']utf-8["\']\s*/?>)',
        r'(<meta\s+http-equiv=["\']Content-Type["\'][^>]*>)',
    ]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            insert_pos = match.end()
            new_content = content[:insert_pos] + '\n' + ADSENSE_SCRIPT + content[insert_pos:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'fixed'
    
    return 'no_charset_meta'

def main():
    base_dir = '/home/chison/tools-site'
    results = {'fixed': 0, 'skip': 0, 'skip_legit': 0, 'no_charset_meta': 0, 'error': 0}
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'quality', 'scripts', '.gsc-data', 'css', 'js']]
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                try:
                    r = fix_file(fp)
                    results[r] = results.get(r, 0) + 1
                    if r == 'fixed':
                        print(f'  ✅ {fp}')
                    elif r == 'no_charset_meta':
                        print(f'  ⚠️  No charset meta: {fp}')
                except Exception as e:
                    print(f'  ❌ Error: {fp}: {e}')
                    results['error'] += 1
    
    print(f'\n结果: {results}')

if __name__ == '__main__':
    main()
