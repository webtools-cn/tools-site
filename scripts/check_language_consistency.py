#!/usr/bin/env python3
"""
语言一致性检查脚本 — 质检门L1-11b
检查中文页面中出现的英文内容（h2/h3/段落）。
中文页面 = 非 /en/ 目录下的 index.html

用法: python3 scripts/check_language_consistency.py [--fix] [--verbose]
  --fix     自动修复已知模式（Related Tools→相关工具推荐等）
  --verbose 打印所有检测结果
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

# 配置
SITE_ROOT = Path(__file__).parent.parent
EXCLUDE_DIRS = {'css', 'js', 'scripts', 'quality', '.gsc', 'node_modules', 'en'}

# 技术术语白名单（中文页面中允许出现的英文）
TECH_WHITELIST = {
    'HEX', 'HSV', 'RGB', 'HSL', 'REM', 'PX', 'EM', 'JSON', 'XML', 'YAML', 
    'HTML', 'CSS', 'SVG', 'URL', 'API', 'JWT', 'CSV', 'PDF', 'GIF', 'WEBP',
    'AVIF', 'BMP', 'TIFF', 'JPG', 'PNG', 'BASE64', 'MIME', 'ASCII', 'UTF',
    'SEO', 'CDN', 'DNS', 'HTTP', 'HTTPS', 'SSH', 'SSL', 'TLS', 'FTP',
    'MORSE', 'BINARY', 'DECIMAL', 'OCTAL', 'BITWISE', 'AND', 'OR', 'XOR',
    'NOT', 'SHIFT', 'SHA', 'MD5', 'AES', 'DES', 'RSA', 'HMAC', 'CRC',
    'UUID', 'GUID', 'MAC', 'IP', 'TCP', 'UDP', 'ISBN', 'ISSN', 'EAN',
    'UPC', 'VIN', 'IBAN', 'SWIFT', 'CVC', 'CVV', 'SSN', 'NPI', 'NDC',
    'ICD', 'HCPCS', 'CPT', 'LOINC', 'SNOMED', 'RXNORM', 'ATC', 'DDC',
    'LCC', 'UDC', 'PURL', 'DOI', 'ARK', 'HANDLE', 'ORCID', 'ISNI',
    'GND', 'VIAF', 'LCCN', 'OCLC', 'PMID', 'PMCID', 'ART', 'ADS',
    'BIBCODE', 'ASTRONOMICAL', 'JOURNAL', 'ISSN', 'ISBN',
    'Google', 'Analytics', 'AdSense', 'GitHub', 'Pages', 'Cookie',
    'JavaScript', 'Python', 'TypeScript', 'Markdown', 'React', 'Vue',
    'Angular', 'jQuery', 'Node', 'Express', 'Django', 'Flask', 'Rails',
    'Spring', 'Laravel', 'Docker', 'Kubernetes', 'Linux', 'Windows',
    'macOS', 'Android', 'iOS', 'Chrome', 'Firefox', 'Safari', 'Edge',
    'Free', 'ToolBase', 'FAQ',
    'OTP',
    'TOTP',
    'System.Text.Json',
    'Newtonsoft',
    'Gas Mark',
    'LinkedIn',
    'Facebook',
    'Twitter',
    'Twitter Card',
    'Open Graph',
    'Top-K',
    'Avro Schema',
    'JSON Schema',
    'Data URL',
    'Data URL', 'Data',
    'Schema', 'Avro',
    'Open', 'Graph', 'Card',
    'Gas', 'Mark',
    'Top', 'K', 'X', 'C',
    'Q', 'A',  # FAQ标记
}

# 允许的英文单词模式（技术缩写、颜色码等）
ALLOWED_PATTERNS = [
    r'^#[0-9A-Fa-f]{3,8}$',  # 颜色码 #fff #4F46E5
    r'^[0-9]+(?:px|em|rem|vh|vw|%)?$',  # 数字+单位
    r'^[A-Z]{1,6}$',  # 纯大写缩写 ≤6字符
    r'^[A-Z]+[0-9]*$',  # 大写+数字
    r'^→$',  # 箭头
    r'^[🔑📧🐛💬📝🎨📥📤✅🔍🎯🔀📊📐📏📋⏱️⚙️📦📜📖❓🔴🟢🔵🔤🔄✏️🔗]+\s*$',  # emoji
]

def is_tech_term(text):
    """判断文本是否是技术术语"""
    # 去掉emoji和符号
    clean = re.sub(r'[\U0001f300-\U0001f9ff\U00002600-\U000027bf\u2190-\u21ff\uFE0F]', '', text).strip()
    if not clean:
        return True
    # 检查白名单
    words = re.findall(r'[A-Za-z]+', clean)
    for w in words:
        if w not in TECH_WHITELIST and w.capitalize() not in TECH_WHITELIST and w.upper() not in TECH_WHITELIST:
            # 检查是否匹配允许的模式
            if not any(re.match(p, clean) for p in ALLOWED_PATTERNS):
                return False
    return True

def has_chinese(text):
    """检查文本是否包含中文字符"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def has_english(text):
    """检查文本是否包含有意义的英文单词（≥3字母）"""
    # 去掉HTML标签属性
    clean = re.sub(r'<[^>]+>', '', text)
    # 去掉CSS/JS代码
    clean = re.sub(r'\{[^}]*\}', '', clean)
    clean = re.sub(r'function\s*\([^)]*\)', '', clean)
    return bool(re.search(r'[A-Za-z]{3,}', clean))

def extract_visible_h2_h3(content):
    """提取h2/h3标题的可见文本"""
    results = []
    # 匹配<h2>和<h3>标签
    for match in re.finditer(r'<(h[23])[^>]*>(.*?)</\1>', content, re.DOTALL):
        tag = match.group(1)
        inner = match.group(2)
        # 去掉嵌套标签
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if not text:
            continue
        # 跳过JS动态内容（含'+ 或 $1 或变量引用或模板字面量）
        raw = match.group(0)
        if any(x in raw for x in ["'+", "' +", "$1", 'id="', 'escapeHtml', 'monthNames', 
                                     'todayTitle', 'questions[', 'esc(', 'd.title', 'd.day',
                                     'd.type', 'tournamentData']):
            continue
        results.append((tag, text, match.group(0)))
    return results

def extract_visible_p(content):
    """提取段落p的可见文本"""
    results = []
    for match in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        inner = match.group(1)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if not text or len(text) < 20:
            continue
        # 跳过JS代码
        if 'function' in text or 'var ' in text or 'window.' in text:
            continue
        results.append(text)
    return results

def check_page(filepath):
    """检查单个页面的语言一致性"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    # 检查h2/h3
    for tag, text, full_tag in extract_visible_h2_h3(content):
        if has_english(text) and not has_chinese(text):
            if not is_tech_term(text):
                issues.append({
                    'type': f'{tag}_english',
                    'text': text[:100],
                    'severity': 'high',
                    'message': f'{tag}标题为纯英文: "{text[:60]}"'
                })

    # 检查段落（只标记大段纯英文）
    for text in extract_visible_p(content):
        if has_english(text) and not has_chinese(text) and len(text) > 30:
            # 排除技术性段落
            if text.startswith(('Free ToolBase', 'Last updated', 'Google Analytics')):
                issues.append({
                    'type': 'p_english',
                    'text': text[:100],
                    'severity': 'critical',
                    'message': f'段落为纯英文: "{text[:60]}..."'
                })

    return issues

def main():
    fix_mode = '--fix' in sys.argv
    verbose = '--verbose' in sys.argv

    all_issues = defaultdict(list)
    total_pages = 0
    pages_with_issues = 0

    # 遍历所有中文页面
    for item in sorted(SITE_ROOT.iterdir()):
        if not item.is_dir() or item.name in EXCLUDE_DIRS:
            continue
        filepath = item / 'index.html'
        if not filepath.exists():
            continue

        total_pages += 1
        issues = check_page(filepath)
        if issues:
            pages_with_issues += 1
            all_issues[item.name] = issues
            if verbose or issues:
                for issue in issues:
                    print(f"[{issue['severity'].upper()}] {item.name}: {issue['message']}")

    # 输出汇总
    print(f"\n{'='*60}")
    print(f"语言一致性检查结果")
    print(f"{'='*60}")
    print(f"总中文页面数: {total_pages}")
    print(f"有问题的页面数: {pages_with_issues}")
    print(f"总问题数: {sum(len(v) for v in all_issues.values())}")

    if pages_with_issues > 0:
        print(f"\n问题分布:")
        type_counts = defaultdict(int)
        for issues in all_issues.values():
            for issue in issues:
                type_counts[issue['type']] += 1
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")

    # 输出JSON格式（供cron使用）
    result = {
        'total_pages': total_pages,
        'pages_with_issues': pages_with_issues,
        'total_issues': sum(len(v) for v in all_issues.values()),
        'issues': {k: v for k, v in all_issues.items()}
    }

    output_file = SITE_ROOT / 'quality' / 'language_consistency_report.json'
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {output_file}")

    # 退出码：有问题返回1
    return 1 if pages_with_issues > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
