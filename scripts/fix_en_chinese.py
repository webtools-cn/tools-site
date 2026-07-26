#!/usr/bin/env python3
"""修复EN页面中的中文问题"""
import re, json, os

SITE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SITE)  # scripts -> root

CN_RE = re.compile(r'[\u4e00-\u9fff]')

# 工具英文名映射
NAME_MAP = {
    'a1c-calculator': ('A1C Calculator', 'HbA1c to Average Blood Sugar Converter'),
    'beta-calculator': ('Beta Calculator', 'Systematic Risk & Stock Volatility Calculator'),
    'calorie-deficit-calculator': ('Calorie Deficit Calculator', 'Weight Loss Calorie Calculator'),
    'capital-gains-tax-calculator': ('Capital Gains Tax Calculator', 'Stock & Property Capital Gains Tax'),
    'capm-calculator': ('CAPM Calculator', 'Capital Asset Pricing Model'),
    'cholesterol-ratio-calculator': ('Cholesterol Ratio Calculator', 'Cardiovascular Risk Assessment'),
    'debt-payoff-calculator': ('Debt Payoff Calculator', 'Debt Repayment Plan & Snowball Method'),
    'dividend-calculator': ('Dividend Calculator', 'Dividend Yield & Payout Calculator'),
    'self-employment-tax-calculator': ('Self-Employment Tax Calculator', 'Freelancer & Contractor Tax Estimator'),
    'sharpe-ratio': ('Sharpe Ratio Calculator', 'Risk-Adjusted Return Calculator'),
}

def fix_en_page(tool_name):
    path = os.path.join(SITE, 'en', tool_name, 'index.html')
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    en_name, en_subtitle = NAME_MAP.get(tool_name, (tool_name.replace('-',' ').title(), tool_name.replace('-',' ').title()))
    
    # 1. Fix h1 - replace Chinese h1 content with English
    # Pattern: <h1>EMOJI Chinese text</h1>
    content = re.sub(
        r'<h1>[^\x00-\x7F]*([\u4e00-\u9fff][^<]*)</h1>',
        f'<h1>{en_name}</h1>',
        content
    )
    # Also try pattern without emoji
    if CN_RE.search(content):
        content = re.sub(
            r'<h1>([^<]*[\u4e00-\u9fff][^<]*)</h1>',
            f'<h1>{en_name}</h1>',
            content
        )
    
    # 2. Fix subtitle
    content = re.sub(
        r'<p class="subtitle">[^<]*[\u4e00-\u9fff][^<]*</p>',
        f'<p class="subtitle">{en_subtitle}</p>',
        content
    )
    
    # 3. Fix badge
    content = re.sub(
        r'<span class="badge">[^<]*[\u4e00-\u9fff][^<]*</span>',
        '<span class="badge">🆓 Free to use</span>',
        content
    )
    
    # 4. Fix lang-switch - EN should be active
    content = re.sub(
        r'<div class="lang-switch"><a href="[^"]*" class="active">[^<]*[\u4e00-\u9fff][^<]*</a><a href="[^"]*">EN</a></div>',
        lambda m: m.group(0).replace('class="active"', '').replace('>EN<', ' class="active">EN<').replace('active""', 'active"'),
        content
    )
    # Simpler approach for lang-switch
    if 'class="active"' in content and '中文' in content:
        # Swap active: remove from CN link, add to EN link
        content = re.sub(r'(<a href="[^"]*"[^>]*)class="active"', r'\1', content, count=1)
        content = re.sub(r'(<a href="[^"]*en/[^"]*"[^>]*)>EN<', r'\1 class="active">EN<', content, count=1)
    
    # 5. Fix breadcrumb - last item (tool name in Chinese)
    content = re.sub(
        r'&rsaquo;\s*[^<\n]*[\u4e00-\u9fff][^<\n]*</p>',
        f'&rsaquo; {en_name}</p>',
        content
    )
    
    # 6. Fix Schema.org name
    content = re.sub(
        r'"name":"[^"]*[\u4e00-\u9fff][^"]*"',
        f'"name":"{en_name}"',
        content
    )
    
    # 7. Fix BreadcrumbList last item name
    content = re.sub(
        r'"name":"[^"]*[\u4e00-\u9fff][^"]*"',
        f'"name":"{en_name}"',
        content
    )
    
    # 8. Fix common Chinese labels and text
    replacements = [
        ('首页', 'Home'),
        ('工具', 'Tools'),
        ('免费使用', 'Free to use'),
        ('计算', 'Calculate'),
        ('清空', 'Clear'),
        ('复制', 'Copy'),
        ('结果', 'Result'),
        ('输入', 'Input'),
        ('输出', 'Output'),
        ('单位', 'Unit'),
        ('选择', 'Select'),
        ('年', 'year'),
        ('月', 'month'),
        ('天', 'day'),
        ('查看', 'View'),
        ('结果', 'Result'),
    ]
    
    for cn, en_text in replacements:
        # Only replace in visible text, not in URLs or attributes
        content = content.replace(f'>{cn}<', f'>{en_text}<')
        content = content.replace(f'>{cn} ', f'>{en_text} ')
    
    # 9. Fix Chinese labels in input-group
    content = re.sub(r'(<label>[^<]*)([\u4e00-\u9fff]+)([^<]*</label>)', 
                     lambda m: m.group(1) + 'Param' + m.group(3), content)
    
    # 10. Fix privacy note
    content = re.sub(
        r'<div class="privacy-note">[^<]*[\u4e00-\u9fff][^<]*</div>',
        '<div class="privacy-note">🔒 All calculations are done locally in your browser. No data is uploaded to any server.</div>',
        content
    )
    
    # 11. Fix "关于" and "隐私政策" in footer
    content = content.replace('关于', 'About')
    content = content.replace('隐私政策', 'Privacy Policy')
    content = content.replace('保留所有权利', 'All rights reserved')
    
    # 12. Fix "常见问题" / "使用步骤" headers
    content = content.replace('常见问题', 'FAQ')
    content = content.replace('使用步骤', 'How to Use')
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    en_tools_with_chinese = [
        'a1c-calculator', 'beta-calculator', 'calorie-deficit-calculator',
        'capital-gains-tax-calculator', 'capm-calculator', 'cholesterol-ratio-calculator',
        'debt-payoff-calculator', 'dividend-calculator', 'self-employment-tax-calculator',
        'sharpe-ratio'
    ]
    
    fixed = 0
    for tool in en_tools_with_chinese:
        result = fix_en_page(tool)
        if result:
            fixed += 1
            print(f"  ✅ Fixed: en/{tool}/")
        else:
            print(f"  ⚠️ No changes: en/{tool}/")
    
    print(f"\nFixed {fixed}/{len(en_tools_with_chinese)} EN pages")

if __name__ == '__main__':
    main()