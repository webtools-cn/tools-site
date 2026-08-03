#!/usr/bin/env python3
"""批量修复分类页(tools/xxx/和en/tools/xxx/)的浅色背景为深色主题"""

import os
import re
import glob

# 要修复的分类页模式
patterns = [
    'tools/*/index.html',
    'en/tools/*/index.html',
]

# CSS替换规则 (old → new)
replacements = [
    # body背景
    ('background:#f8fafc;', 'background:#0f172a;'),
    ('background: #f8fafc;', 'background: #0f172a;'),
    # 卡片背景
    ('.tool-card { background:#fff;', '.tool-card { background:#1e293b;'),
    ('.tool-card { background: #fff;', '.tool-card { background: #1e293b;'),
    # 卡片边框
    ('border:1px solid #e5e7eb; border-radius:12px; padding:20px;',
     'border:1px solid #334155; border-radius:12px; padding:20px;'),
    # 卡片hover阴影
    ('box-shadow:0 4px 12px rgba(0,0,0,0.1);', 'box-shadow:0 4px 12px rgba(0,0,0,0.3);'),
    # 卡片描述文字
    ('.tool-card p { margin:0; font-size:13px; color:#64748b;', '.tool-card p { margin:0; font-size:13px; color:#94a3b8;'),
    ('.tool-card p { margin:0; font-size:13px; color: #64748b;', '.tool-card p { margin:0; font-size:13px; color: #94a3b8;'),
    # intro文字
    ('.intro { font-size:16px; line-height:1.7; color:#475569;', '.intro { font-size:16px; line-height:1.7; color:#cbd5e1;'),
    ('.intro { font-size:16px; line-height:1.7; color: #475569;', '.intro { font-size:16px; line-height:1.7; color: #cbd5e1;'),
    # FAQ边框
    ('.faq-section details { border:1px solid #e5e7eb;', '.faq-section details { border:1px solid #334155;'),
    # FAQ答案文字
    ('.faq-section details div { padding:0 16px 12px; font-size:14px; color:#475569;',
     '.faq-section details div { padding:0 16px 12px; font-size:14px; color:#cbd5e1;'),
    ('.faq-section details div { padding:0 16px 12px; font-size:14px; color: #475569;',
     '.faq-section details div { padding:0 16px 12px; font-size:14px; color: #cbd5e1;'),
    # cat-tag
    ('.cat-tag { display:inline-block; padding:8px 16px; background:#f1f5f9; border-radius:20px; color:#475569;',
     '.cat-tag { display:inline-block; padding:8px 16px; background:#1e293b; border:1px solid #334155; border-radius:20px; color:#cbd5e1;'),
    ('.cat-tag { display:inline-block; padding:8px 16px; background: #f1f5f9; border-radius:20px; color: #475569;',
     '.cat-tag { display:inline-block; padding:8px 16px; background: #1e293b; border:1px solid #334155; border-radius:20px; color: #cbd5e1;'),
]

fixed_count = 0
total_files = 0

for pattern in patterns:
    for filepath in sorted(glob.glob(pattern)):
        if not os.path.exists(filepath):
            continue
        total_files += 1
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for old, new in replacements:
            content = content.replace(old, new)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"Fixed: {filepath}")

print(f"\nTotal files scanned: {total_files}")
print(f"Files fixed: {fixed_count}")
