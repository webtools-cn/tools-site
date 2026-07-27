#!/usr/bin/env python3
"""更新首页卡片和sitemap，添加5个新工具"""
import os, re

SITE = '/home/chison/tools-site'

new_tools = [
    {
        'name': 'ebay-fee-calculator',
        'cn_title': 'eBay费用计算器',
        'en_title': 'eBay Fee Calculator',
        'cn_desc': '计算eBay卖家费用、成交费和净利润',
        'en_desc': 'Calculate eBay seller fees and net profit',
        'emoji': '🧾',
    },
    {
        'name': 'paypal-fee-calculator',
        'cn_title': 'PayPal手续费计算器',
        'en_title': 'PayPal Fee Calculator',
        'cn_desc': '计算PayPal收款手续费和实际到账金额',
        'en_desc': 'Calculate PayPal fees and net received amount',
        'emoji': '💸',
    },
    {
        'name': 'metabolism-calculator',
        'cn_title': '基础代谢率计算器',
        'en_title': 'BMR Metabolism Calculator',
        'cn_desc': '计算BMR基础代谢率和TDEE每日热量消耗',
        'en_desc': 'Calculate BMR and daily calorie expenditure',
        'emoji': '🔥',
    },
    {
        'name': '1rm-calculator',
        'cn_title': '1RM最大重量计算器',
        'en_title': 'One Rep Max Calculator',
        'cn_desc': '推算深蹲/卧推/硬拉最大重量和训练重量',
        'en_desc': 'Estimate 1RM for squat, bench and deadlift',
        'emoji': '🏋️',
    },
    {
        'name': 'hiking-time',
        'cn_title': '徒步时间计算器',
        'en_title': 'Hiking Time Calculator',
        'cn_desc': '根据距离和海拔估算徒步耗时和热量消耗',
        'en_desc': 'Estimate hiking time and calories burned',
        'emoji': '🥾',
    },
]

# 更新CN首页
cn_path = os.path.join(SITE, 'index.html')
with open(cn_path, 'r', encoding='utf-8') as f:
    cn_content = f.read()

# 更新EN首页
en_path = os.path.join(SITE, 'en', 'index.html')
with open(en_path, 'r', encoding='utf-8') as f:
    en_content = f.read()

for tool in new_tools:
    name = tool['name']
    
    # CN首页卡片
    cn_card = f'''      <div class="tool-card">
        <a href="/{name}/">
          <span class="tool-icon">{tool['emoji']}</span>
          <h3>{tool['cn_title']}</h3>
          <p>{tool['cn_desc']}</p>
        </a>
      </div>'''
    
    # 插入到最后一个tool-card之前找个参考位置
    # 找tools-grid里的最后一个card之后
    grid_match = re.search(r'(<div class="tools-grid">.*?)(</div>\s*</section>)', cn_content, re.DOTALL)
    if grid_match:
        insert_pos = grid_match.end(1)
        cn_content = cn_content[:insert_pos] + '\n' + cn_card + cn_content[insert_pos:]
    
    # EN首页卡片
    en_card = f'''      <div class="tool-card">
        <a href="/en/{name}/">
          <span class="tool-icon">{tool['emoji']}</span>
          <h3>{tool['en_title']}</h3>
          <p>{tool['en_desc']}</p>
        </a>
      </div>'''
    
    en_grid_match = re.search(r'(<div class="tools-grid">.*?)(</div>\s*</section>)', en_content, re.DOTALL)
    if en_grid_match:
        insert_pos = en_grid_match.end(1)
        en_content = en_content[:insert_pos] + '\n' + en_card + en_content[insert_pos:]

# 更新CN首页数字
cn_content = re.sub(r'(\d+)\s*个免费在线工具', lambda m: f'{int(m.group(1))+5} 个免费在线工具', cn_content)
# 更新EN首页数字
en_content = re.sub(r'(\d+)\s*Free Online Tools', lambda m: f'{int(m.group(1))+5} Free Online Tools', en_content)

with open(cn_path, 'w', encoding='utf-8') as f:
    f.write(cn_content)
with open(en_path, 'w', encoding='utf-8') as f:
    f.write(en_content)

print("✅ CN+EN首页卡片已更新")

# 更新sitemap
sitemap_path = os.path.join(SITE, 'sitemap.xml')
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap = f.read()

for tool in new_tools:
    name = tool['name']
    cn_entry = f'''  <url>
    <loc>https://free-toolbase.com/{name}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>'''
    en_entry = f'''  <url>
    <loc>https://free-toolbase.com/en/{name}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>'''
    
    # 插入到最后一个</url>之后
    last_url = sitemap.rfind('</url>')
    sitemap = sitemap[:last_url+7] + '\n' + cn_entry + '\n' + en_entry + sitemap[last_url+7:]

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print("✅ sitemap.xml已更新")

# 更新llms.txt
llms_path = os.path.join(SITE, 'llms.txt')
with open(llms_path, 'r', encoding='utf-8') as f:
    llms = f.read()

for tool in new_tools:
    name = tool['name']
    llms += f'/{name}/ | {tool["cn_title"]} | {tool["cn_desc"]}\n'
    llms += f'/en/{name}/ | {tool["en_title"]} | {tool["en_desc"]}\n'

with open(llms_path, 'w', encoding='utf-8') as f:
    f.write(llms)

print("✅ llms.txt已更新")
print(f"\n完成! 新增5个工具: {[t['name'] for t in new_tools]}")