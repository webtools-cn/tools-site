#!/usr/bin/env python3
"""
EN页面含中文检查脚本 — 检测英文版页面中的中文字符
英文页面 = en/目录下的index.html

用法: python3 scripts/check_en_chinese.py [--verbose]
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

SITE_ROOT = Path(__file__).parent.parent
EN_ROOT = SITE_ROOT / 'en'

# 允许在EN页面中出现的中文字符（技术术语、品牌名等）
# 主要是注释、CSS字体名中的中文
ALLOWED_CONTEXTS = [
    'PingFang SC', 'Microsoft YaHei', 'PingFang', 'Heiti SC',
    'Hiragino Sans GB', 'STHeiti', 'SimHei', 'SimSun',
    'WenQuanYi', 'Noto Sans CJK',
]

def extract_chinese(text):
    """提取文本中的中文字符片段"""
    return re.findall(r'[\u4e00-\u9fff]+[^\u0000-\u007f\s<>"\']*', text)

def check_page(filepath):
    """检查EN页面是否含中文"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    # 检查可见文本（排除script/style/注释）
    # 提取body内容
    body_match = re.search(r'<body[^>]*>(.*)</body>', content, re.DOTALL)
    if not body_match:
        return issues
    
    body = body_match.group(1)
    
    # 移除script和style标签内容
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    
    # 移除允许的中文上下文（CSS字体名）
    for allowed in ALLOWED_CONTEXTS:
        body = body.replace(allowed, '')
    
    # 移除lang-switch中的"中文"标签（EN页面显示语言切换链接是合理的）
    body = re.sub(r'<a[^>]*>中文</a>', '', body)
    # 移除单独的"中文"文字（语言切换标签）
    body = re.sub(r'(?<![\u4e00-\u9fff])中文(?![\u4e00-\u9fff])', '', body)
    
    # 查找中文字符
    chinese_segments = extract_chinese(body)
    if chinese_segments:
        # 去重并取前5个
        unique = list(dict.fromkeys(chinese_segments))[:5]
        issues = unique
    
    return issues

def main():
    verbose = '--verbose' in sys.argv
    
    all_issues = {}
    total_pages = 0
    pages_with_issues = 0
    
    # 遍历EN目录
    if not EN_ROOT.exists():
        print("EN目录不存在")
        return 1
    
    for item in sorted(EN_ROOT.iterdir()):
        if not item.is_dir():
            continue
        filepath = item / 'index.html'
        if not filepath.exists():
            continue
        
        total_pages += 1
        issues = check_page(filepath)
        if issues:
            pages_with_issues += 1
            all_issues[item.name] = issues
            if verbose:
                print(f"[ISSUE] {item.name}: {', '.join(issues[:3])}")
    
    print(f"\n{'='*60}")
    print(f"EN页面含中文检查结果")
    print(f"{'='*60}")
    print(f"总EN页面数: {total_pages}")
    print(f"含中文的页面数: {pages_with_issues}")
    print(f"占比: {pages_with_issues/total_pages*100:.1f}%" if total_pages > 0 else "")
    
    result = {
        'total_pages': total_pages,
        'pages_with_issues': pages_with_issues,
        'issues': {k: v for k, v in all_issues.items()}
    }
    
    output_file = SITE_ROOT / 'quality' / 'en_chinese_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"报告已保存: {output_file}")
    
    return 1 if pages_with_issues > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
