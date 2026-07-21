#!/usr/bin/env python3
"""
质检-门2：首页一致性检测
检测项：
1. 统计数字一致性（hero数字 vs 实际目录数 vs HTML卡片数 vs SEO描述）
2. 所有首页数字必须统一为实际工具数
3. 卡片分类完整性（每个卡片必须有非NEW的分类标签）
4. 按钮样式统一性（\"立即使用\"必须有class=\"btn\"）
"""

import re, sys, json, subprocess

BASE = '/home/chison/tools-site'

def count_tool_dirs():
    """统计实际工具目录数（有index.html且不是en子目录的才算工具）"""
    import os
    count = 0
    for d in sorted(os.listdir(BASE)):
        if os.path.isdir(os.path.join(BASE, d)) and not d.startswith('.') and d != 'en':
            if os.path.exists(os.path.join(BASE, d, 'index.html')):
                count += 1
    return count

def scan_page(path, label):
    """扫描首页，提取所有数字和问题"""
    with open(path) as f:
        content = f.read()
    
    issues = []
    findings = {}
    
    # 1. 提取所有声明的工具数（排除分类数如33）
    numbers = set()
    # hero stat-number
    for m in re.finditer(r'stat-number["\']>(\d+)\+?<', content):
        n = int(m.group(1))
        if n >= 100:  # 工具数至少3位数
            numbers.add(n)
    # meta description
    for m in re.finditer(r'(\d{3,5})\+\s*(?:免费在线工具|free online tools)', content):
        numbers.add(int(m.group(1)))
    # title
    for m in re.finditer(r'>[^<]*?(\d{3,5})\+\s*(?:Free Online Tools|免费在线工具)', content):
        numbers.add(int(m.group(1)))
    
    findings['declared_numbers'] = sorted(numbers)
    
    # 2. 统计HTML卡片数
    h3_count = len(re.findall(r'<h3>', content))
    findings['card_count'] = h3_count
    
    # 3. 检查缺分类的卡片
    # 有tool-meta但只有NEW标签
    no_cat = []
    cards = re.finditer(
        r'<div class="tool-card" data-cats="([^"]*)">\s*.*?'
        r'(<div class="tool-meta">(.*?)</div>)?\s*'
        r'<a href="([^"]*?)/"', 
        content, re.DOTALL
    )
    for m in cards:
        h3 = re.search(r'<h3>(.*?)</h3>', m.group(0))
        name = h3.group(1) if h3 else '?'
        meta_content = m.group(3) or ''
        if not meta_content.strip():
            no_cat.append(f'{name}(无meta)')
        else:
            spans = re.findall(r'<span[^>]*>(.*?)</span>', meta_content)
            cats = [s for s in spans if 'NEW' not in s]
            if not cats:
                no_cat.append(f'{name}(仅NEW)')
    
    findings['missing_category'] = no_cat
    
    # 4. 检查\"立即使用\"按钮样式
    bare_links = len(re.findall(r'(?<!class="btn" )<a href="[^"]+">立即使用</a>', content))
    findings['bare_links'] = bare_links
    
    return findings

def main():
    actual = count_tool_dirs()
    zh = scan_page(f'{BASE}/index.html', '中文')
    en = scan_page(f'{BASE}/en/index.html', '英文')
    
    all_issues = []
    
    # 一致性检查
    all_numbers = set(zh['declared_numbers'] + en['declared_numbers'])
    
    print(f'实际工具目录数: {actual}')
    print(f'中文首页声明: {zh["declared_numbers"]}')
    print(f'英文首页声明: {en["declared_numbers"]}')
    print(f'中文卡片数: {zh["card_count"]}')
    print(f'英文卡片数: {en["card_count"]}')
    print(f'中文缺分类: {len(zh["missing_category"])} 个')
    print(f'英文缺分类: {len(en["missing_category"])} 个')
    print(f'中文裸链接: {zh["bare_links"]} 个')
    print(f'英文裸链接: {en["bare_links"]} 个')
    
    # 判定问题
    if len(all_numbers) > 1:
        all_issues.append({
            'severity': 'P0',
            'type': '数字不一致',
            'detail': f'首页出现{len(all_numbers)}个不同数字: {sorted(all_numbers)}，应统一为{actual}'
        })
    
    for n in all_numbers:
        if n != actual:
            all_issues.append({
                'severity': 'P1',
                'type': '数字错误',
                'detail': f'声明{n}不等于实际{actual}'
            })
    
    if zh['card_count'] != actual:
        all_issues.append({
            'severity': 'P2', 
            'type': '卡片未全覆盖',
            'detail': f'中文首页{zh["card_count"]}个卡片 vs 实际{actual}个工具（差{actual-zh["card_count"]}个待添加）'
        })
    
    if en['card_count'] != actual:
        all_issues.append({
            'severity': 'P2',
            'type': '卡片未全覆盖',
            'detail': f'英文首页{en["card_count"]}个卡片 vs 实际{actual}个工具（差{actual-en["card_count"]}个待添加）'
        })
    
    if zh['missing_category']:
        all_issues.append({
            'severity': 'P1',
            'type': '缺分类标签',
            'detail': f'中文{len(zh["missing_category"])}个卡片无分类: {zh["missing_category"][:5]}...'
        })
    
    if en['missing_category']:
        all_issues.append({
            'severity': 'P1',
            'type': '缺分类标签',
            'detail': f'英文{len(en["missing_category"])}个卡片无分类: {en["missing_category"][:5]}...'
        })
    
    if zh['bare_links'] > 0:
        all_issues.append({
            'severity': 'P2',
            'type': '按钮样式缺失',
            'detail': f'中文{zh["bare_links"]}个"立即使用"链接无class="btn"'
        })
    
    if en['bare_links'] > 0:
        all_issues.append({
            'severity': 'P2',
            'type': '按钮样式缺失', 
            'detail': f'英文{en["bare_links"]}个"立即使用"链接无class="btn"'
        })
    
    # 输出JSON结果
    result = {
        'timestamp': subprocess.run(['date', '-Iseconds'], capture_output=True, text=True).stdout.strip(),
        'actual_tools': actual,
        'zh_declared': zh['declared_numbers'],
        'en_declared': en['declared_numbers'],
        'zh_cards': zh['card_count'],
        'en_cards': en['card_count'],
        'zh_missing_cat': len(zh['missing_category']),
        'en_missing_cat': len(en['missing_category']),
        'zh_bare_links': zh['bare_links'],
        'en_bare_links': en['bare_links'],
        'issues': all_issues,
        'pass': len(all_issues) == 0
    }
    
    # 写报告
    with open(f'{BASE}/quality-reports/homepage-check.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\n{"✅ 全部通过" if result["pass"] else "❌ 发现问题: " + str(len(all_issues)) + "个"}')
    
    if all_issues:
        for i in all_issues:
            print(f'  [{i["severity"]}] {i["type"]}: {i["detail"]}')
    
    sys.exit(0 if result['pass'] else 1)

if __name__ == '__main__':
    main()
