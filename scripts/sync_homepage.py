#!/usr/bin/env python3
"""Add new tool cards to CN + EN homepages and update sitemap"""
import re, os, datetime

BASE = "/home/chison/tools-site"

# New tools with their card HTML
NEW_TOOLS = [
    {
        "slug": "spaced-repetition-scheduler",
        "cn_name": "间隔重复学习计划表",
        "en_name": "Spaced Repetition Scheduler",
        "emoji": "🧠",
        "cn_desc": "基于遗忘曲线的科学复习计划生成器",
        "en_desc": "Science-based review scheduler using the forgetting curve",
        "category_cn": "学习工具",
        "category_en": "Learning",
    },
    {
        "slug": "pomodoro-tracker",
        "cn_name": "番茄钟计时器",
        "en_name": "Pomodoro Timer",
        "emoji": "🍅",
        "cn_desc": "在线番茄工作法计时器，提升专注力",
        "en_desc": "Online Pomodoro technique timer to boost focus",
        "category_cn": "效率工具",
        "category_en": "Productivity",
    },
    {
        "slug": "pronunciation-guide",
        "cn_name": "英语发音查询工具",
        "en_name": "English Pronunciation Guide",
        "emoji": "🔊",
        "cn_desc": "英式/美式音标查询与发音指导",
        "en_desc": "British & American phonetic lookup with pronunciation tips",
        "category_cn": "学习工具",
        "category_en": "Learning",
    },
    {
        "slug": "vocabulary-builder",
        "cn_name": "英语词汇量测试",
        "en_name": "Vocabulary Builder",
        "emoji": "📚",
        "cn_desc": "科学估算英语词汇量，分级测试",
        "en_desc": "Scientifically estimate your English vocabulary size",
        "category_cn": "学习工具",
        "category_en": "Learning",
    },
    {
        "slug": "multiplication-table-generator",
        "cn_name": "乘法口诀表生成器",
        "en_name": "Multiplication Table Generator",
        "emoji": "✖️",
        "cn_desc": "可打印乘法口诀表，1×1到20×20",
        "en_desc": "Printable multiplication tables from 1×1 to 20×20",
        "category_cn": "教育工具",
        "category_en": "Education",
    },
]

# Count current tools
cn_dirs = [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d)) and d not in ['en', '_gen', 'css', 'js', 'scripts', 'quality', '.git', '.gsc-data'] and not d.startswith('.')]
en_dirs = [d for d in os.listdir(os.path.join(BASE, 'en')) if os.path.isdir(os.path.join(BASE, 'en', d)) and not d.startswith('.')]
new_count = len(NEW_TOOLS)
cn_total = len(cn_dirs) + new_count
en_total = len(en_dirs) + new_count
print(f"CN tools: {len(cn_dirs)} → {cn_total}")
print(f"EN tools: {len(en_dirs)} → {en_total}")

def generate_card_cn(tool):
    return f'''<div class="tool-card" data-category="{tool['category_cn']}" data-name="{tool['cn_name']}">
<span class="icon">{tool['emoji']}</span>
<h3>{tool['cn_name']}</h3>
<p>{tool['cn_desc']}</p>
<div class="tool-meta"><span class="new-tag">NEW</span><span>{tool['category_cn']}</span></div>
<a href="/{tool['slug']}/">立即使用 →</a>
</div>'''

def generate_card_en(tool):
    return f'''<div class="tool-card" data-category="{tool['category_en']}" data-name="{tool['en_name']}">
<span class="icon">{tool['emoji']}</span>
<h3>{tool['en_name']}</h3>
<p>{tool['en_desc']}</p>
<div class="tool-meta"><span class="new-tag">NEW</span><span>{tool['category_en']}</span></div>
<a href="/en/{tool['slug']}/">Use Now →</a>
</div>'''

# Update CN homepage
cn_path = os.path.join(BASE, "index.html")
with open(cn_path, "r", encoding="utf-8") as f:
    cn_content = f.read()

# Insert cards after last existing card in the main grid (find last </div> before "统计" section)
# Strategy: find <!-- TOOLS END --> marker or insert before the last closing of tools grid
# Find a good insertion point: look for the last tool-card before the stats section
insert_marker = '<div class="hero-stat">'
if insert_marker in cn_content:
    cards_html = "\n".join([generate_card_cn(t) for t in NEW_TOOLS])
    cn_content = cn_content.replace(insert_marker, cards_html + "\n" + insert_marker)
    
# Update tool count: 3096 → new number
cn_content = cn_content.replace('3096+', f'{cn_total}+')
cn_content = cn_content.replace('3096', str(cn_total))
# Also fix the FAQ count
cn_content = re.sub(r'(\d{4})\+?(款|个)', f'{cn_total}+\\2', cn_content)

with open(cn_path, "w", encoding="utf-8") as f:
    f.write(cn_content)
print(f"✅ Updated CN homepage: {cn_path}")

# Update EN homepage
en_path = os.path.join(BASE, "en", "index.html")
with open(en_path, "r", encoding="utf-8") as f:
    en_content = f.read()

if insert_marker in en_content:
    cards_html = "\n".join([generate_card_en(t) for t in NEW_TOOLS])
    en_content = en_content.replace(insert_marker, cards_html + "\n" + insert_marker)

en_content = en_content.replace('3091+', f'{en_total}+')
en_content = en_content.replace('3091', str(en_total))
en_content = re.sub(r'(\d{4})\+?(款|个)', f'{en_total}+\\2', en_content)
# Also fix standalone numbers in meta
en_content = re.sub(r'content="Access \d+\+', f'content="Access {en_total}+', en_content)

with open(en_path, "w", encoding="utf-8") as f:
    f.write(en_content)
print(f"✅ Updated EN homepage: {en_path}")

# Update sitemap
sitemap_path = os.path.join(BASE, "sitemap.xml")
today = datetime.date.today().isoformat()
sitemap_entries = []
for tool in NEW_TOOLS:
    sitemap_entries.append(f'''  <url>
    <loc>https://free-toolbase.com/{tool['slug']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')
    sitemap_entries.append(f'''  <url>
    <loc>https://free-toolbase.com/en/{tool['slug']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')

with open(sitemap_path, "r", encoding="utf-8") as f:
    sm = f.read()

# Insert before closing </urlset>
sm = sm.replace("</urlset>", "\n".join(sitemap_entries) + "\n</urlset>")

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sm)
print(f"✅ Updated sitemap: {sitemap_path}")

print(f"\n🎉 Homepage sync done. CN: {cn_total} tools, EN: {en_total} tools")