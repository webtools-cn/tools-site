#!/usr/bin/env python3
"""门9：工具页面结构检测 — H1重复、FAQ重复、H2过多、底部空白"""
import re, os, sys, json
from pathlib import Path

TOOLS_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = TOOLS_ROOT / 'quality' / 'gate9-issues.json'

SKIP = {'en','assets','scripts','quality','css','js','images','node_modules',
        '.git','.github','fonts','libs','vendor','dist','build','.gsc-data'}

def find_tools():
    dirs = []
    for d in TOOLS_ROOT.iterdir():
        if d.is_dir() and d.name not in SKIP and (d / 'index.html').exists():
            dirs.append(d.name)
    return sorted(dirs)

def check_tool(name, html):
    issues = []
    
    # H1计数
    h1_count = len(re.findall(r'<h1[^>]*>', html))
    if h1_count == 0:
        issues.append({'severity': 'P1', 'type': '缺少H1', 'detail': '页面无H1标题'})
    elif h1_count >= 2:
        # 检查第二个H1是否合法（hero区允许，但必须包含评分或tag）
        h1_texts = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        for i, t in enumerate(h1_texts):
            clean = re.sub(r'<[^>]+>', '', t).strip()
            if i == 1 and ('★' in clean or 'display:flex' in t):
                continue  # hero区H1允许
            if i > 0:
                issues.append({'severity': 'P1', 'type': 'H1重复',
                    'detail': f'{h1_count}个H1: [{clean[:40]}]'})
                break
    
    # H2计数
    h2_count = len(re.findall(r'<h2[^>]*>', html))
    if h2_count > 8:
        issues.append({'severity': 'P2', 'type': 'H2过多',
            'detail': f'{h2_count}个H2(>8), 可能有多余区块'})
    
    # FAQ重复
    faq_sections = re.findall(r'<h2[^>]*>.*?(?:常见问题|FAQ).*?</h2>', html)
    if len(faq_sections) > 1:
        issues.append({'severity': 'P1', 'type': 'FAQ重复',
            'detail': f'{len(faq_sections)}个FAQ标题'})
    
    # 底部空白div
    body_end = html.rfind('</body>')
    tail = html[body_end-2000:body_end] if body_end > 0 else ''
    blank_divs = len(re.findall(r'<div[^>]*>\s*</div>', tail))
    if blank_divs >= 2:
        issues.append({'severity': 'P2', 'type': '底部空白div',
            'detail': f'{blank_divs}个空白div在</body>前'})
    
    return issues

def main():
    tools = find_tools()
    all_issues = []
    stats = {'ok': 0, 'h1_dup': 0, 'faq_dup': 0, 'h2_exc': 0, 'blank': 0}
    
    for name in tools:
        path = TOOLS_ROOT / name / 'index.html'
        with open(path) as f:
            html = f.read()
        
        issues = check_tool(name, html)
        if issues:
            for iss in issues:
                all_issues.append({'tool': name, **iss})
                if 'H1重复' in iss['type']: stats['h1_dup'] += 1
                elif 'FAQ重复' in iss['type']: stats['faq_dup'] += 1
                elif 'H2过多' in iss['type']: stats['h2_exc'] += 1
                elif '空白' in iss['type']: stats['blank'] += 1
        else:
            stats['ok'] += 1
    
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({'stats': stats, 'issues': all_issues}, f, indent=2, ensure_ascii=False)
    
    print(f"门9检测完成: {len(tools)}个工具")
    print(f"  ✅ 正常: {stats['ok']}")
    print(f"  ❌ H1重复: {stats['h1_dup']}")
    print(f"  ❌ FAQ重复: {stats['faq_dup']}")
    print(f"  ⚠️ H2过多: {stats['h2_exc']}")
    print(f"  ⚠️ 底部空白: {stats['blank']}")
    print(f"  结果: {OUTPUT_FILE}")
    
    sys.exit(0 if stats['ok'] == len(tools) else 1)

if __name__ == '__main__':
    main()
