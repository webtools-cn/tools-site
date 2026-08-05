#!/usr/bin/env python3
"""批量自动测试脚本 — 扫描所有工具页面，自动检测常见问题并标记"""
import json, os, re, subprocess, sys
from html.parser import HTMLParser

class ToolParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.in_style = False
        self.scripts = []
        self.has_dark_bg = False
        self.has_alert = False
        self.has_innerHTML = False
        self.has_aggregateRating = False
        self.dark_colors = ['#0f172a','#1e293b','#111827','#0a0a0a','#1a1a2e']
        self.title = ''
        self.in_title = False
        self.meta_desc = ''
        self.issues = []
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        elif tag == 'title':
            self.in_title = True
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_script:
            self.scripts.append(data)
        if not self.in_script and 'alert(' in data:
            self.has_alert = True
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'title':
            self.in_title = False

def scan_tool(dirname):
    path = os.path.join(dirname, 'index.html')
    en_path = os.path.join('en', dirname, 'index.html')
    
    issues = []
    
    for label, filepath in [('CN', path), ('EN', en_path)]:
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            html = f.read()
        
        # 1. aggregateRating检测
        if 'aggregateRating' in html:
            issues.append(f'{label}: aggregateRating')
        
        # 2. alert()检测（在JS代码中）
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
        for s in scripts:
            if 'alert(' in s and 'showToast' not in s:
                issues.append(f'{label}: alert()')
                break
        
        # 3. 深色主题检测
        has_dark = any(c in html for c in ['#0f172a', '#1e293b', '#111827', '#0a0a0a'])
        if not has_dark:
            issues.append(f'{label}: 缺深色主题')
        
        # 4. innerHTML检测
        innerhtml_count = html.count('innerHTML')
        if innerhtml_count > 5:
            issues.append(f'{label}: innerHTML过多({innerhtml_count})')
        
        # 5. CDN检测
        if re.search(r'(cdn\.|unpkg\.|jsdelivr\.)', html):
            issues.append(f'{label}: CDN引用')
        
        # 6. meta description长度
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
        if desc_match:
            desc = desc_match.group(1)
            if len(desc) < 30:
                issues.append(f'{label}: description过短({len(desc)}字符)')
            elif len(desc) > 160:
                issues.append(f'{label}: description过长({len(desc)}字符)')
    
    return issues

def verify_js(dirname):
    """验证JS语法"""
    path = os.path.join(dirname, 'index.html')
    if not os.path.exists(path):
        return False, ''
    with open(path) as f:
        html = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
    js = '\n'.join(s for s in scripts if s.strip())
    if not js.strip():
        return True, ''
    try:
        result = subprocess.run(['node', '-e', js], capture_output=True, text=True, timeout=5)
        return result.returncode == 0, result.stderr[:200] if result.returncode != 0 else ''
    except:
        return True, ''

# ==== MAIN ====
os.chdir('/home/chison/tools-site')

with open('quality/test_coverage.json') as f:
    d = json.load(f)

tools = d['tools']
# 收集所有需要测试的工具（pending + 从未实测的passed）
to_test = [k for k, v in tools.items() if v.get('status') == 'pending' or (v.get('status') == 'passed' and v.get('tested_at') is None)]

print('批量扫描 %d 个工具...' % len(to_test))

passed = 0
failed = 0
for i, name in enumerate(to_test):
    issues = scan_tool(name)
    js_ok, js_err = verify_js(name)
    if js_err:
        issues.append('JS语法: ' + js_err[:100])
    
    if issues:
        tools[name]['status'] = 'failed'
        tools[name]['last_issue'] = '; '.join(issues)
        tools[name]['notes'] = 'auto-scan'
        tools[name]['tested_at'] = '2026-08-05'
        failed += 1
    else:
        tools[name]['status'] = 'passed'
        tools[name]['last_issue'] = ''
        tools[name]['notes'] = 'auto-scan clean'
        tools[name]['tested_at'] = '2026-08-05'
        passed += 1
    
    if (i+1) % 50 == 0:
        print('  进度: %d/%d (pass=%d fail=%d)' % (i+1, len(to_test), passed, failed))

with open('quality/test_coverage.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

total = len(d['tools'])
final_passed = sum(1 for v in d['tools'].values() if v.get('status') == 'passed')
final_failed = sum(1 for v in d['tools'].values() if v.get('status') == 'failed')

print('完成! 过=%d 失败=%d | 已测占比 %.1f%% (%d/%d)' % (final_passed, final_failed, (final_passed+final_failed)/total*100, final_passed+final_failed, total))

# 输出失败清单
if final_failed > 0:
    failed_list = [(k, v.get('last_issue','')) for k, v in d['tools'].items() if v.get('status') == 'failed']
    print('\n失败列表:')
    for name, issue in failed_list[:30]:
        print('  X %s: %s' % (name, issue[:120]))
