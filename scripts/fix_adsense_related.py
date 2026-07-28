#!/usr/bin/env python3
"""批量给缺失页面加 AdSense + related-tools"""
import os, re, glob

# 10个需要修复的页面
pages = [
    "apy-to-apr-calculator/index.html",
    "car-insurance-calculator/index.html",
    "chads2-score/index.html",
    "has-bled-score/index.html",
    "salary-comparison-calculator/index.html",
    "en/apy-to-apr-calculator/index.html",
    "en/car-insurance-calculator/index.html",
    "en/chads2-score/index.html",
    "en/has-bled-score/index.html",
    "en/salary-comparison-calculator/index.html",
]

# 根据页面路径判断语言
def get_lang(path):
    return "en" if path.startswith("en/") else "cn"

# 相关工具映射（按关键词）
related_map = {
    "apy": '<a href="/compound-interest-daily/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📈 Compound Interest</a><a href="/savings-goal-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🎯 Savings Goal</a><a href="/investment-return-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">💰 Investment Return</a>',
    "insurance": '<a href="/life-insurance-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🛡️ Life Insurance</a><a href="/term-insurance-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📋 Term Insurance</a><a href="/loan-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🏦 Loan Calculator</a>',
    "chads2": '<a href="/stroke-risk-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🧠 Stroke Risk</a><a href="/has-bled-score/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">💉 HAS-BLED Score</a><a href="/bmi-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">⚖️ BMI Calculator</a>',
    "bled": '<a href="/chads2-score/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">❤️ CHADS2 Score</a><a href="/stroke-risk-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🧠 Stroke Risk</a><a href="/bmi-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">⚖️ BMI Calculator</a>',
    "salary": '<a href="/take-home-pay-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">💵 Take-Home Pay</a><a href="/income-tax-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📊 Income Tax</a><a href="/hourly-to-salary/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">⏰ Hourly to Salary</a>',
}

def get_related_html(path):
    for key, html in related_map.items():
        if key in path:
            return html
    # 默认
    return '<a href="/calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🧮 Calculator</a><a href="/converter/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🔄 Converter</a><a href="/generator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">✨ Generator</a>'

adsense_html = '''<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

related_en_title = '🔗 Related Tools'
related_cn_title = '🔗 相关工具推荐'

fixed = 0
for page in pages:
    path = page
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        continue
    with open(path, 'r') as f:
        content = f.read()
    lang = get_lang(path)
    modified = False

    # 1. 检查并添加 AdSense
    if 'adsbygoogle' not in content:
        # 在 </main> 之前或之后插入
        if '</main>' in content:
            content = content.replace('</main>', adsense_html + '\n</main>')
            modified = True
        elif '<footer' in content:
            content = content.replace('<footer', adsense_html + '\n<footer', 1)
            modified = True
    
    # 2. 检查并添加 related-tools section
    if 'related-tools' not in content and 'related_tools' not in content:
        related_html = get_related_html(path)
        title = related_en_title if lang == 'en' else related_cn_title
        section = f'\n<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">{title}</h2><div style="display:flex;flex-wrap:wrap;gap:4px;">{related_html}</div></section>\n'
        # 插入到 footer 之前
        if '<footer' in content:
            content = content.replace('<footer', section + '<footer', 1)
            modified = True
        elif '</body>' in content:
            content = content.replace('</body>', section + '</body>', 1)
            modified = True

    if modified:
        with open(path, 'w') as f:
            f.write(content)
        print(f"  ✅ Fixed: {path}")
        fixed += 1
    else:
        print(f"  ⏭️  Already OK: {path}")

print(f"\nTotal fixed: {fixed}/10")
