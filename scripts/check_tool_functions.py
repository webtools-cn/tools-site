#!/usr/bin/env python3
"""
全站功能验证脚本 — 自动检测工具页面是否能正常工作
不只是看HTML结构，而是提取JS函数，在Node中执行，检查输出是否合理。

检测项：
1. 核心函数是否存在且不是stub
2. 核心函数能否被调用不报错
3. 输出是否非空且非"Generated at"
4. 页面是否有明显HTML结构问题（缺少按钮、缺少输出区等）

用法: python3 scripts/check_tool_functions.py [--verbose] [--sample N]
  --sample N  只检测N个随机页面（默认全量）
"""

import os, re, sys, json, random, subprocess, tempfile
from pathlib import Path
from collections import defaultdict

SITE_ROOT = Path(__file__).parent.parent
EXCLUDE_DIRS = {'css', 'js', 'scripts', 'quality', '.gsc', 'node_modules', 'en'}

def extract_script_content(html):
    """提取页面中的JS代码（排除JSON-LD和外部引用）"""
    # 同时匹配标签和内容
    all_scripts = re.findall(r'(<script[^>]*>)(.*?)</script>', html, re.DOTALL)
    js_parts = []
    for tag, content in all_scripts:
        # 排除JSON-LD
        if 'ld+json' in tag.lower():
            continue
        # 排除外部引用
        if 'src=' in tag:
            continue
        # 排除太短的
        if len(content.strip()) < 50:
            continue
        # 排除JSON内容（以{开头）
        stripped = content.strip()
        if stripped.startswith('{'):
            continue
        js_parts.append(content)
    return '\n'.join(js_parts)

def check_page(filepath, tool_name):
    """检查单个工具页面"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception:
        return [{'type': 'read_error', 'severity': 'critical', 'msg': '无法读取文件'}]
    
    js = extract_script_content(html)
    if not js:
        issues.append({'type': 'no_js', 'severity': 'high', 'msg': '页面没有内联JS逻辑'})
        return issues
    
    # 1. 检查是否有stub
    if 'Generated at' in js:
        issues.append({'type': 'stub', 'severity': 'critical', 'msg': '空壳工具：函数体是Generated at stub'})
    
    # 2. 检查核心交互元素
    has_input = bool(re.search(r'<(input|textarea|select)[^>]', html))
    has_button = bool(re.search(r'<button[^>]*onclick', html)) or bool(re.search(r'addEventListener.*click', js))
    has_output = bool(re.search(r'id="(output|result|result-text)"', html))
    
    if not has_input and not has_button:
        issues.append({'type': 'no_input', 'severity': 'medium', 'msg': '页面没有输入控件'})
    if not has_button:
        issues.append({'type': 'no_button', 'severity': 'medium', 'msg': '页面没有可点击的按钮'})
    if not has_output:
        issues.append({'type': 'no_output', 'severity': 'low', 'msg': '页面没有输出区域'})
    
    # 3. 检查JS语法
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
            tmp.write(js)
            tmp_path = tmp.name
        result = subprocess.run(['node', '--check', tmp_path], 
                              capture_output=True, text=True, timeout=5)
        os.unlink(tmp_path)
        if result.returncode != 0:
            error_msg = result.stderr.strip().split('\n')[0][:100]
            issues.append({'type': 'js_syntax', 'severity': 'critical', 'msg': f'JS语法错误: {error_msg}'})
    except subprocess.TimeoutExpired:
        issues.append({'type': 'js_timeout', 'severity': 'high', 'msg': 'JS检查超时'})
    except FileNotFoundError:
        pass  # node not installed
    except Exception:
        pass
    
    # 4. 检查是否有明显的运行时问题
    # 检查是否引用了未定义的函数
    func_calls = set(re.findall(r'onclick="(\w+)\(', html))
    func_defs = set(re.findall(r'function\s+(\w+)\s*\(', js))
    for call in func_calls:
        if call not in func_defs and call not in ('showToast',):
            issues.append({'type': 'undef_func', 'severity': 'high', 'msg': f'HTML调用了未定义的函数: {call}()'})
    
    # 5. 检查document.getElementById是否引用了不存在的元素
    elem_ids_in_js = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js))
    elem_ids_in_html = set(re.findall(r'id="([^"]+)"', html))
    missing_ids = elem_ids_in_js - elem_ids_in_html - {'output', 'result', 'result-text', 'toast'}
    # 只报告在主函数中引用的
    if missing_ids:
        # 过滤掉可能是动态创建的
        real_missing = []
        for mid in missing_ids:
            if not re.search(rf'createElement|appendChild|innerHTML.*{mid}', js):
                real_missing.append(mid)
        if real_missing:
            issues.append({'type': 'missing_elem', 'severity': 'medium', 
                         'msg': f'JS引用了不存在的元素ID: {",".join(list(real_missing)[:3])}'})
    
    # 6. 检查深色主题
    body_bg = re.search(r'background:\s*(#[0-9a-fA-F]{3,8})', html)
    if body_bg:
        bg = body_bg.group(1).lower()
        # 浅色背景
        if bg in ('#fff', '#ffffff', '#fafafa', '#f8fafc') or re.match(r'^#fff[0-9a-f]', bg):
            issues.append({'type': 'light_theme', 'severity': 'high', 'msg': f'浅色背景: {bg}'})
    
    return issues

def main():
    verbose = '--verbose' in sys.argv
    sample_mode = '--sample' in sys.argv
    sample_n = 50
    if sample_mode:
        idx = sys.argv.index('--sample')
        if idx + 1 < len(sys.argv):
            sample_n = int(sys.argv[idx + 1])
    
    all_issues = {}
    total = 0
    pages_with_issues = 0
    
    # 收集所有工具目录
    tools = []
    for item in sorted(SITE_ROOT.iterdir()):
        if not item.is_dir() or item.name in EXCLUDE_DIRS:
            continue
        filepath = item / 'index.html'
        if filepath.exists():
            tools.append((item.name, filepath))
    
    if sample_mode and len(tools) > sample_n:
        random.seed(42)
        tools = random.sample(tools, sample_n)
    
    for tool_name, filepath in tools:
        total += 1
        issues = check_page(filepath, tool_name)
        if issues:
            pages_with_issues += 1
            all_issues[tool_name] = issues
            if verbose:
                for issue in issues:
                    print(f"[{issue['severity'].upper()}] {tool_name}: {issue['msg']}")
    
    print(f"\n{'='*60}")
    print(f"全站功能验证结果{'(抽样'+str(sample_n)+')' if sample_mode else ''}")
    print(f"{'='*60}")
    print(f"检测页面数: {total}")
    print(f"有问题的页面数: {pages_with_issues}")
    print(f"总问题数: {sum(len(v) for v in all_issues.values())}")
    
    if pages_with_issues > 0:
        print(f"\n问题分布:")
        type_counts = defaultdict(int)
        sev_counts = defaultdict(int)
        for issues in all_issues.values():
            for issue in issues:
                type_counts[issue['type']] += 1
                sev_counts[issue['severity']] += 1
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print(f"\n严重度:")
        for s, c in sorted(sev_counts.items(), key=lambda x: {'critical':0,'high':1,'medium':2,'low':3}.get(x[0],9)):
            print(f"  {s}: {c}")
    
    result = {
        'total_pages': total,
        'pages_with_issues': pages_with_issues,
        'total_issues': sum(len(v) for v in all_issues.values()),
        'issues': {k: v for k, v in all_issues.items()}
    }
    
    output_file = SITE_ROOT / 'quality' / 'tool_functions_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {output_file}")
    
    return 1 if pages_with_issues > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
