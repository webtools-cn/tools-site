#!/usr/bin/env python3
"""在CN和EN首页添加5个新工具的卡片，更新sitemap"""
import re

SITE = '/home/chison/tools-site'

NEW_CARDS = [
    {
        'slug': 'cd-ladder-calculator-detailed',
        'cn_name': 'CD阶梯计算器',
        'cn_desc': '计算定期存款阶梯策略收益、到期滚动和总回报',
        'en_name': 'CD Ladder Calculator',
        'en_desc': 'Calculate CD ladder strategy returns, rollover, and total yield',
        'icon': '🏦',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'medicare-cost-calculator',
        'cn_name': 'Medicare费用计算器',
        'cn_desc': '估算Part A/B/C/D保费、IRMAA附加费和自付费用',
        'en_name': 'Medicare Cost Calculator',
        'en_desc': 'Estimate Part A/B/C/D premiums, IRMAA surcharges and OOP costs',
        'icon': '🏥',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'savings-account-comparison',
        'cn_name': '储蓄账户比较器',
        'cn_desc': '对比多个银行APY利率、复利频率和费用',
        'en_name': 'Savings Account Comparator',
        'en_desc': 'Compare multiple bank APYs, compounding frequency and fees',
        'icon': '💰',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'retirement-expense-planner',
        'cn_name': '退休支出规划器',
        'cn_desc': '估算退休后生活开支、医疗费用和通胀调整',
        'en_name': 'Retirement Expense Planner',
        'en_desc': 'Estimate post-retirement expenses, medical costs and inflation',
        'icon': '📊',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'forex-risk-calculator',
        'cn_name': '外汇风险计算器',
        'cn_desc': '计算头寸规模、止损点数和盈亏比',
        'en_name': 'Forex Risk Calculator',
        'en_desc': 'Calculate position size, stop-loss pips and risk-reward ratio',
        'icon': '💱',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
]

CN_CARD_TPL = '''<div class="tool-card" data-category="{category}" data-name="{cn_name}">
<a href="/{slug}/">
<div class="tool-icon">{icon}</div>
<h3>{cn_name}</h3>
<p>{cn_desc}</p>
</a>
</div>'''

EN_CARD_TPL = '''<div class="tool-card" data-category="{en_category}" data-name="{en_name}">
<a href="/en/{slug}/">
<div class="tool-icon">{icon}</div>
<h3>{en_name}</h3>
<p>{en_desc}</p>
</a>
</div>'''

def add_to_index(path, template):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    first_card = html.find('<div class="tool-card"')
    if first_card < 0:
        print(f"ERROR: no tool-card found in {path}")
        return False
    
    new_html = ''
    for c in reversed(NEW_CARDS):
        new_html = template.format(**c) + '\n' + new_html
    
    html = html[:first_card] + new_html + html[first_card:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Updated {path}")
    return True

# CN首页
add_to_index(f'{SITE}/index.html', CN_CARD_TPL)

# EN首页
add_to_index(f'{SITE}/en/index.html', EN_CARD_TPL)

# Update tool count in titles
for path in [f'{SITE}/index.html', f'{SITE}/en/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    old_count = re.search(r'(\d+)\+', html)
    if old_count:
        new_count = str(int(old_count.group(1)) + 5) + '+'
        html = html.replace(old_count.group(0), new_count)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Updated count in {path}: {new_count}")

# Update sitemap
sitemap_path = f'{SITE}/sitemap.xml'
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap = f.read()

new_urls = ''
for c in NEW_CARDS:
    new_urls += f'''  <url>
    <loc>https://free-toolbase.com/{c['slug']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://free-toolbase.com/en/{c['slug']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''

sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)
print(f"✅ Updated sitemap.xml")

print("\nDone! All 5 tools added to homepage + sitemap")