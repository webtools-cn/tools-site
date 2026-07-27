#!/usr/bin/env python3
"""在CN和EN首页添加5个新工具的卡片"""
import re

SITE = '/home/chison/tools-site'

NEW_CARDS = [
    {
        'slug': 'interest-rate-calculator',
        'cn_name': '利率换算计算器',
        'cn_desc': '年/月/日利率互相转换，计算有效年利率(EAR)',
        'en_name': 'Interest Rate Converter',
        'en_desc': 'Convert between annual/monthly/daily rates and EAR',
        'icon': '📊',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'dca-calculator',
        'cn_name': '定投收益计算器',
        'cn_desc': '模拟定期定额投资，对比定投vs一次性投入',
        'en_name': 'DCA Investment Calculator',
        'en_desc': 'Simulate dollar-cost averaging vs lump sum returns',
        'icon': '💰',
        'category': '金融计算器',
        'en_category': 'Finance',
    },
    {
        'slug': 'fuel-economy-calculator',
        'cn_name': '油耗计算器',
        'cn_desc': '计算百公里油耗、MPG换算、年燃油成本',
        'en_name': 'Fuel Economy Calculator',
        'en_desc': 'Calculate L/100km, MPG conversion, annual fuel cost',
        'icon': '⛽',
        'category': '生活工具',
        'en_category': 'Lifestyle',
    },
    {
        'slug': 'tdde-calculator',
        'cn_name': '每日能量消耗计算器',
        'cn_desc': '计算TDEE、BMR，减重/增重热量目标',
        'en_name': 'TDEE Calculator',
        'en_desc': 'Calculate TDEE, BMR, weight loss/gain calorie targets',
        'icon': '🔥',
        'category': '健康工具',
        'en_category': 'Health',
    },
    {
        'slug': 'rental-property-calculator',
        'cn_name': '出租房产收益计算器',
        'cn_desc': '计算租金收益率、月现金流、投资回报率',
        'en_name': 'Rental Property ROI Calculator',
        'en_desc': 'Calculate rental yield, cash flow, and ROI',
        'icon': '🏠',
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

def add_to_index(path, template, slug_key='slug'):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 在最后一个tool-card后面插入新卡片
    # 先找到最后一个 </div> 在 tools-grid 中的位置
    # 更简单：找到第一个tool-card，在它前面插入
    first_card = html.find('<div class="tool-card"')
    if first_card < 0:
        print(f"ERROR: no tool-card found in {path}")
        return False
    
    new_html = ''
    for c in reversed(NEW_CARDS):
        data = {
            'slug': c[slug_key] if slug_key in c else c['slug'],
            'cn_name': c['cn_name'],
            'cn_desc': c['cn_desc'],
            'en_name': c['en_name'],
            'en_desc': c['en_desc'],
            'icon': c['icon'],
            'category': c['category'],
            'en_category': c['en_category'],
        }
        new_html = template.format(**data) + '\n' + new_html
    
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
for path, lang in [(f'{SITE}/index.html', 'zh'), (f'{SITE}/en/index.html', 'en')]:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Update the count in description/title: 3076+ → 3081+
    old_count = re.search(r'(\d+)\+', html)
    if old_count:
        new_count = str(int(old_count.group(1)) + 5) + '+'
        html = html.replace(old_count.group(0), new_count, 1)  # first occurrence only
        # Also replace all occurrences
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

# Insert before </urlset>
sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)
print(f"✅ Updated sitemap.xml")

print("\nDone! All 5 tools added to homepage + sitemap")