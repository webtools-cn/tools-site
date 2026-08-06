#!/usr/bin/env python3
"""Add related-tools sections to batch5 + batch9 new calculator tools (CN + EN)."""

import os
import re

BASE = '/home/chison/tools-site'

# Related tools mapping: tool_slug -> [(name_cn, name_en, slug)]
# CN page uses CN names, EN page uses EN names
RELATED = {
    'screen-resolution-calculator': [
        ('PPI计算器', 'PPI Calculator', 'ppi-calculator'),
        ('像素转换器', 'Pixel Converter', 'pixel-converter'),
        ('宽高比计算器', 'Aspect Ratio Calculator', 'aspect-ratio-calculator'),
    ],
    'mortgage-afford-calculator': [
        ('贷款EMI计算器', 'Loan EMI Calculator', 'emi-calculator'),
        ('房贷计算器', 'Mortgage Calculator', 'mortgage-calculator'),
        ('复利计算器', 'Compound Interest Calculator', 'compound-interest-calc'),
    ],
    'ovulation-calc': [
        ('预产期计算器', 'Due Date Calculator', 'due-date-calculator'),
        ('孕期计算器', 'Pregnancy Calculator', 'pregnancy-calculator'),
        ('BMI计算器', 'BMI Calculator', 'bmi-calculator'),
    ],
    'concrete-volume-calc': [
        ('体积计算器', 'Volume Calculator', 'volume-calculator'),
        ('面积计算器', 'Area Calculator', 'area-calculator'),
        ('立方体积计算器', 'Cubic Volume Calculator', 'cubic-volume-calculator'),
    ],
    'travel-time-calc': [
        ('速度转换器', 'Speed Converter', 'speed-converter'),
        ('距离计算器', 'Distance Calculator', 'distance-calculator'),
        ('时区转换器', 'Timezone Converter', 'timezone-converter'),
    ],
    'composting-calculator': [
        ('碳足迹计算器', 'Carbon Footprint Calculator', 'carbon-footprint-calculator'),
        ('水足迹计算器', 'Water Footprint Calculator', 'water-footprint-calculator'),
        ('重量转换器', 'Weight Converter', 'weight-converter'),
    ],
    'food-cost-calculator': [
        ('单位价格计算器', 'Unit Price Calculator', 'unit-price-calculator'),
        ('折扣计算器', 'Discount Calculator', 'discount-calculator'),
        ('小费计算器', 'Tip Calculator', 'tip-calculator'),
    ],
    'language-difficulty-calculator': [
        ('单词计数器', 'Word Counter', 'word-counter'),
        ('字符计数器', 'Character Counter', 'character-counter'),
        ('阅读时间计算器', 'Reading Time Calculator', 'reading-time-calculator'),
    ],
    'octave-calculator': [
        ('频率转换器', 'Frequency Converter', 'frequency-converter'),
        ('分贝计算器', 'Decibel Calculator', 'decibel-calculator'),
        ('科学计算器', 'Scientific Calculator', 'scientific-calculator'),
    ],
    'pomodoro-planner': [
        ('倒计时器', 'Countdown Timer', 'countdown-timer'),
        ('秒表计时器', 'Stopwatch', 'stopwatch'),
        ('时间计算器', 'Time Calculator', 'time-calculator'),
    ],
    'retirement-score-calculator': [
        ('退休储蓄计算器', 'Retirement Corpus Calculator', 'retirement-corpus-calc'),
        ('复利计算器', 'Compound Interest Calculator', 'compound-interest-calc'),
        ('财务自由计算器', 'FIRE Calculator', 'fire-calculator'),
    ],
    'spring-rate-calculator': [
        ('力矩计算器', 'Torque Calculator', 'torque-calculator'),
        ('力转换器', 'Force Converter', 'force-converter'),
        ('压力计算器', 'Pressure Calculator', 'pressure-calculator'),
    ],
    'subnet-calculator-v6': [
        ('IP子网计算器', 'IP Subnet Calculator', 'subnet-calculator'),
        ('CIDR计算器', 'CIDR Calculator', 'cidr-calculator'),
        ('带宽计算器', 'Bandwidth Calculator', 'bandwidth-calculator'),
    ],
    'water-footprint-calculator': [
        ('碳足迹计算器', 'Carbon Footprint Calculator', 'carbon-footprint-calculator'),
        ('面积计算器', 'Area Calculator', 'area-calculator'),
        ('体积计算器', 'Volume Calculator', 'volume-calculator'),
    ],
}

# CSS for related tools (inline, consistent across pages)
RELATED_CSS = """
.related-tools { margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border); }
.related-tools h2 { font-size: 1.1rem; color: var(--text); margin-bottom: 12px; }
.related-tools .related-links { display: flex; flex-wrap: wrap; gap: 10px; }
.related-tools .related-links a { display: inline-block; padding: 8px 16px; background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; color: var(--primary); text-decoration: none; font-size: .9rem; transition: border-color .2s; }
.related-tools .related-links a:hover { border-color: var(--primary); }
"""

# HTML template for CN
CN_HTML_TEMPLATE = """<div class="related-tools">
<h2>相关工具推荐</h2>
<div class="related-links">
{links}
</div>
</div>"""

# HTML template for EN
EN_HTML_TEMPLATE = """<div class="related-tools">
<h2>Related Tools</h2>
<div class="related-links">
{links}
</div>
</div>"""


def add_related_to_page(filepath, is_en=False):
    """Add related-tools section before </main>"""
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has related-tools
    if 'related-tools' in content.lower():
        print(f"  SKIP: {filepath} already has related-tools")
        return False
    
    # Extract tool slug from path
    parts = filepath.replace(BASE + '/', '').split('/')
    if parts[0] == 'en':
        tool_slug = parts[1]
    else:
        tool_slug = parts[0]
    
    if tool_slug not in RELATED:
        print(f"  SKIP: {tool_slug} not in RELATED map")
        return False
    
    related = RELATED[tool_slug]
    
    # Build links
    links_html = []
    for cn_name, en_name, slug in related:
        if is_en:
            href = f'/en/{slug}/'
            name = en_name
        else:
            href = f'/{slug}/'
            name = cn_name
        links_html.append(f'<a href="{href}">{name}</a>')
    
    links_str = '\n'.join(links_html)
    
    if is_en:
        section_html = EN_HTML_TEMPLATE.format(links=links_str)
    else:
        section_html = CN_HTML_TEMPLATE.format(links=links_str)
    
    # Insert before </main>
    if '</main>' in content:
        new_content = content.replace('</main>', section_html + '\n</main>', 1)
    else:
        print(f"  ERROR: </main> not found in {filepath}")
        return False
    
    # Also add the CSS if not already present
    if '.related-tools' not in content and '</style>' in content:
        new_content = new_content.replace('</style>', RELATED_CSS + '\n</style>', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def extend_meta_description(filepath):
    """Ensure meta description is 50-160 chars"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract current meta description
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if not m:
        m = re.search(r"<meta\s+name='description'\s+content='([^']+)'", content)
    if not m:
        return False
    
    desc = m.group(1)
    if len(desc) >= 50:
        return False  # Already good
    
    # Extend it by adding a generic SEO suffix
    # But don't repeat content - add a complementary sentence
    extended = desc.rstrip('。.') + '。免费在线使用，无需下载安装，所有计算在浏览器本地完成。'
    if len(extended) > 160:
        extended = desc.rstrip('。.') + '。免费在线工具，纯前端计算。'
    
    content = content.replace(f'content="{desc}"', f'content="{extended}"', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Meta extended: {len(desc)}→{len(extended)} chars")
    return True


def main():
    tools = list(RELATED.keys())
    modified = 0
    
    for slug in tools:
        cn_path = os.path.join(BASE, slug, 'index.html')
        en_path = os.path.join(BASE, 'en', slug, 'index.html')
        
        print(f"\n--- {slug} ---")
        
        # CN page
        if add_related_to_page(cn_path, is_en=False):
            print(f"  CN: related-tools added")
            modified += 1
        extend_meta_description(cn_path)
        
        # EN page
        if add_related_to_page(en_path, is_en=True):
            print(f"  EN: related-tools added")
            modified += 1
        extend_meta_description(en_path)
    
    print(f"\n=== Done: {modified} pages modified ===")
    return modified


if __name__ == '__main__':
    main()
