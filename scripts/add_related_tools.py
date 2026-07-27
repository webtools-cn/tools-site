#!/usr/bin/env python3
"""批量给缺related_tools的页面添加相关工具推荐"""
import os
import re

SITE = '/home/chison/tools-site'

# 每个工具 -> [(slug, emoji, name_cn, name_en)]
tool_meta = {}
for d in sorted(os.listdir(SITE)):
    path = os.path.join(SITE, d)
    if not os.path.isdir(path) or d.startswith('.') or d.startswith('en') or d.startswith('quality') or d.startswith('scripts') or d.startswith('css') or d.startswith('js'):
        continue
    f = os.path.join(path, 'index.html')
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        content = fh.read()
    m = re.search(r'<title>([^<]+)</title>', content)
    title = m.group(1) if m else d
    # 提取emoji
    em = re.search(r'<h1[^>]*>\s*([^\s<]{1,3})\s*', content)
    emoji = em.group(1) if em else '🔧'
    tool_meta[d] = (emoji, title)

# 推荐关系
recommend = {
    'airport-code-lookup': ['timezone-converter', 'time-duration-calculator', 'currency-converter'],
    'cd-ladder-calculator-detailed': ['compound-interest-calculator', 'savings-goal-calculator', 'fixed-deposit-calculator'],
    'forex-risk-calculator': ['currency-converter', 'profit-margin-calculator', 'roi-calculator'],
    'medicare-cost-calculator': ['health-insurance-cost-calculator', 'retirement-expense-planner', 'budget-calculator'],
    'parking-fine-calculator': ['expense-tracker', 'currency-converter', 'budget-calculator'],
    'retirement-expense-planner': ['retirement-calculator', 'compound-interest-calculator', 'budget-calculator'],
    'savings-account-comparison': ['compound-interest-calculator', 'savings-goal-calculator', 'apy-calculator'],
    'tip-calculator-by-country': ['currency-converter', 'split-bill-calculator', 'percentage-calculator'],
}

def gen_related_html(slugs, lang='cn'):
    """生成related-tools HTML"""
    links = []
    for slug in slugs:
        if slug not in tool_meta:
            continue
        emoji, title = tool_meta[slug]
        # 简化title（去掉 | Free ToolBase后缀）
        short = title.split('|')[0].strip().replace(' - Free Online Tool', '').replace(' - free-toolbase.com', '')
        if lang == 'en':
            href = f'/en/{slug}/'
        else:
            href = f'/{slug}/'
        links.append(f'<a href="{href}" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">{emoji} {short}</a>')
    heading = '相关工具推荐' if lang == 'cn' else 'Related Tools'
    html = f'<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 {heading}</h2><div style="display:flex;flex-wrap:wrap;gap:4px;">{" ".join(links)}</div></section>'
    return html

# 处理CN + EN页面
processed = 0
for tool, slugs in recommend.items():
    for lang, prefix in [('cn', ''), ('en', 'en/')]:
        path = os.path.join(SITE, prefix, tool, 'index.html')
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            content = fh.read()
        if 'class="related-tools"' in content:
            continue  # 已存在
        
        html = gen_related_html(slugs, lang)
        # 插入到 </footer> 之前，或者 </body> 之前
        if '</footer>' in content:
            content = content.replace('</footer>', f'{html}\n</footer>')
        elif '</body>' in content:
            content = content.replace('</body>', f'{html}\n</body>')
        else:
            continue
        
        with open(path, 'w') as fh:
            fh.write(content)
        processed += 1
        print(f'Added related-tools: {prefix}{tool}')

print(f'\nTotal processed: {processed}')
