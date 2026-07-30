#!/usr/bin/env python3
"""快速验证 - 先跑100个工具看分析结果"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.chdir('/home/chison/tools-site')

# Monkey-patch the tool discovery to only use first 100
import static_analysis
SKIP = static_analysis.SKIP
dirs = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d not in SKIP and not d.startswith('.')])
static_analysis.tool_dirs = dirs[:100]

# Re-run
import importlib, json
from datetime import datetime

results = {
    'syntax_errors': [],
    'undefined_functions': [],
    'dom_null_risk': [],
    'missing_h1': [],
    'missing_interaction': [],
    'no_js': [],
}

total = 0
for d in static_analysis.tool_dirs:
    html_path = os.path.join(d, 'index.html')
    if not os.path.exists(html_path):
        continue
    total += 1
    try:
        html_content, scripts = static_analysis.extract_scripts(html_path)
        if not scripts:
            results['no_js'].append(d)
            continue
        
        syntax_errors = static_analysis.check_syntax(d, scripts)
        if syntax_errors:
            results['syntax_errors'].append({'tool': d, 'errors': syntax_errors})
            continue
        
        undefined = static_analysis.check_undefined_functions(d, scripts)
        if undefined:
            results['undefined_functions'].append({'tool': d, 'errors': undefined})
        
        dom_issues = static_analysis.check_dom_null(d, html_content, scripts)
        if dom_issues:
            results['dom_null_risk'].append({'tool': d, 'errors': dom_issues})
        
        h1_issues = static_analysis.check_missing_h1(d, html_content)
        if h1_issues:
            results['missing_h1'].append({'tool': d, 'errors': h1_issues})
        
        int_issues = static_analysis.check_missing_interaction(d, html_content)
        if int_issues:
            results['missing_interaction'].append({'tool': d, 'errors': int_issues})
        
    except Exception as e:
        print(f'Error processing {d}: {e}')

total_issues = sum(len(v) for v in results.values())
print(f'Sample: {total} tools')
print(f'No issues: {total - total_issues}')
for k, v in results.items():
    if v:
        print(f'  {k}: {len(v)}')
        for item in v[:5]:
            print(f'    - {item["tool"]}: {item["errors"]}')
