#!/usr/bin/env python3
"""在CN和EN首页添加5个新工具卡片，更新sitemap"""
import re
import os

TOOLS = [
    {
        'slug': 'energy-cost-calculator',
        'cn_name': '能源成本计算器',
        'cn_desc': '免费在线电器电费估算工具，计算每日/每月/每年电费。',
        'cn_icon': '⚡',
        'cn_cat': 'life-tools',
        'en_name': 'Energy Cost Calculator',
        'en_desc': 'Estimate daily/monthly/yearly electricity cost for your appliances.',
        'en_icon': '⚡',
        'en_cat': 'life-tools',
    },
    {
        'slug': 'sobriety-tracker',
        'cn_name': '清醒天数追踪器',
        'cn_desc': '追踪戒酒/戒烟/戒除任何习惯的天数，实时进度和里程碑成就。',
        'cn_icon': '🎯',
        'cn_cat': 'health-tools',
        'en_name': 'Sobriety Tracker',
        'en_desc': 'Track days sober/smoke-free. Real-time progress and milestones.',
        'en_icon': '🎯',
        'en_cat': 'health-tools',
    },
    {
        'slug': 'mileage-log',
        'cn_name': '里程记录器',
        'cn_desc': '记录每次行程的里程、油耗和费用，自动汇总统计。',
        'cn_icon': '🚗',
        'cn_cat': 'life-tools',
        'en_name': 'Mileage Log',
        'en_desc': 'Log trip distances, fuel, and costs. Auto-calculate totals.',
        'en_icon': '🚗',
        'en_cat': 'life-tools',
    },
    {
        'slug': 'fuel-log',
        'cn_name': '油耗记录器',
        'cn_desc': '追踪每次加油记录，自动计算百公里油耗和每公里费用。',
        'cn_icon': '⛽',
        'cn_cat': 'life-tools',
        'en_name': 'Fuel Log',
        'en_desc': 'Track fill-ups, auto-calculate L/100km and cost per km.',
        'en_icon': '⛽',
        'en_cat': 'life-tools',
    },
    {
        'slug': 'swimming-pace',
        'cn_name': '游泳配速计算器',
        'cn_desc': '计算每100米游泳配速、速度和总时间，支持米和码。',
        'cn_icon': '🏊',
        'cn_cat': 'health-tools',
        'en_name': 'Swimming Pace Calculator',
        'en_desc': 'Calculate pace per 100m, speed, and total time. Meters & yards.',
        'en_icon': '🏊',
        'en_cat': 'health-tools',
    },
]

CN_CARD = '<div class="tool-card" data-category="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/{slug}/" class="btn">立即使用</a></div>'
EN_CARD = '<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/en/{slug}/" class="btn">Use Now</a></div>'


def insert_cards(filepath, is_en=False):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 按分类分组，找到每个分类最后一张卡片的位置
    cat_last_line = {}
    for t in TOOLS:
        cat = t['en_cat'] if is_en else t['cn_cat']
        if cat not in cat_last_line:
            # 找这个分类最后一张卡片
            for i, line in enumerate(lines):
                if (is_en and f'data-cat="{cat}"' in line) or (not is_en and f'data-category="{cat}"' in line):
                    cat_last_line[cat] = i

    # 从后往前插入（按行号排序后反向，避免索引偏移）
    inserts = []
    for t in TOOLS:
        cat = t['en_cat'] if is_en else t['cn_cat']
        insert_line = cat_last_line.get(cat, len(lines) - 10)
        if is_en:
            card = EN_CARD.format(cat=cat, icon=t['en_icon'], name=t['en_name'], desc=t['en_desc'], slug=t['slug'])
        else:
            card = CN_CARD.format(cat=cat, icon=t['cn_icon'], name=t['cn_name'], desc=t['cn_desc'], slug=t['slug'])
        inserts.append((insert_line + 1, card))
        cat_last_line[cat] += 1  # 下一个插入位置后移

    # 按行号倒序插入
    inserts.sort(key=lambda x: -x[0])
    for pos, card in inserts:
        lines.insert(pos, card + '\n')

    with open(filepath, 'w') as f:
        f.writelines(lines)


def update_sitemap():
    sitemap_path = 'sitemap.xml'
    with open(sitemap_path, 'r') as f:
        content = f.read()

    # 找到 </urlset> 前插入新条目
    new_entries = ''
    for t in TOOLS:
        new_entries += f'''  <url>
    <loc>https://free-toolbase.com/{t['slug']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://free-toolbase.com/en/{t['slug']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''

    content = content.replace('</urlset>', new_entries + '</urlset>')
    with open(sitemap_path, 'w') as f:
        f.write(content)
    print(f'Sitemap updated, added {len(TOOLS)*2} URLs')


# 修改CN首页
insert_cards('index.html', is_en=False)
print('CN index.html updated')

# 修改EN首页
insert_cards('en/index.html', is_en=True)
print('EN index.html updated')

# 更新sitemap
update_sitemap()

print('Done!')
