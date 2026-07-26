#!/usr/bin/env python3
"""Add new tool cards to CN and EN homepages"""
import os, re

SITE = "/home/chison/tools-site"

NEW_TOOLS = {
    "cd-calculator": {
        "cn": {"icon": "🏦", "name": "定期存款(CD)计算器", "desc": "计算存款证到期收益，支持不同存期、复利频率和提前支取罚息", "cat": "finance-tools"},
        "en": {"icon": "🏦", "name": "CD Calculator", "desc": "Calculate certificate of deposit returns with compounding and early withdrawal penalty", "cat": "finance-tools"},
    },
    "restaurant-tip-calculator": {
        "cn": {"icon": "🍽️", "name": "餐厅小费计算器", "desc": "按比例或固定金额计算小费，支持AA制分账和国际小费习俗参考", "cat": "finance-tools"},
        "en": {"icon": "🍽️", "name": "Restaurant Tip Calculator", "desc": "Calculate tip percentage, split bills, with international tipping customs guide", "cat": "finance-tools"},
    },
    "bmi-children-calculator": {
        "cn": {"icon": "👶", "name": "儿童青少年BMI计算器", "desc": "基于CDC生长曲线百分位评估2-19岁儿童体重状况和BMI百分位", "cat": "health-tools"},
        "en": {"icon": "👶", "name": "Child & Teen BMI Calculator", "desc": "Evaluate BMI percentile for ages 2-19 using CDC growth charts", "cat": "health-tools"},
    },
    "metabolic-age-calculator": {
        "cn": {"icon": "🔥", "name": "代谢年龄计算器", "desc": "基于基础代谢率(BMR)对比同龄均值评估身体代谢年龄", "cat": "health-tools"},
        "en": {"icon": "🔥", "name": "Metabolic Age Calculator", "desc": "Estimate body metabolic age by comparing BMR with peer averages", "cat": "health-tools"},
    },
    "wilks-score-calculator": {
        "cn": {"icon": "🏋️", "name": "Wilks系数力量计算器", "desc": "力量举跨体重级别排名，输入深蹲卧推硬拉计算Wilks分数", "cat": "health-tools"},
        "en": {"icon": "🏋️", "name": "Wilks Score Calculator", "desc": "Powerlifting cross-weight ranking with Wilks coefficient formula", "cat": "health-tools"},
    },
}

def add_cards(filepath, lang, tool_count_before):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the end of the tools grid — insert before the last closing </div> of tools-grid
    # Strategy: find all tool cards by looking for the last tool card pattern then insert after it
    # But easier: insert right after the last existing tool card
    
    # Find all tool-card lines to count
    existing_cards = re.findall(r'<div class="tool-card"', content)
    print(f"  {filepath}: found {len(existing_cards)} existing cards")
    
    # Build cards HTML
    new_cards = ""
    for slug, data in NEW_TOOLS.items():
        t = data[lang]
        cat = lang + "_" + t["cat"]  # data-category uses same names for both langs
        # Use data-cat for CN, data-category for EN? Let's check
        new_cards += f'<div class="tool-card" data-cat="{t["cat"]}"><span class="tool-icon">{t["icon"]}</span><span class="tool-name">{t["name"]}</span><span class="tool-desc">{t["desc"]}</span><a href="/{slug}/" class="btn">{"立即使用" if lang == "cn" else "Use Now"}</a></div>\n'
    
    # Find the last tool card closing tag and the next closing div
    # Find position of the last tool-card div end
    last_card_end = content.rfind('</div>', content.rfind('tool-card'))
    # Actually need more precision: find the last complete tool-card line
    # Insert after the last </a></div> of a tool-card
    
    # Simpler: find a unique anchor point - the last tool-card in the grid
    last_tool_card_idx = content.rfind('<div class="tool-card"')
    # Find the closing </div> for this card - count nested divs
    pos = last_tool_card_idx
    depth = 0
    in_tag = False
    in_comment = False
    while pos < len(content):
        if content[pos:pos+4] == '<!--':
            in_comment = True
            pos += 4
            continue
        if in_comment and content[pos:pos+3] == '-->':
            in_comment = False
            pos += 3
            continue
        if in_comment:
            pos += 1
            continue
        if content[pos:pos+4] == '<div':
            depth += 1
            pos += 4
            continue
        if content[pos:pos+5] == '</div':
            depth -= 1
            if depth == 0:
                # Found end of last tool-card
                insert_pos = pos + 6  # after </div>
                break
            pos += 5
            continue
        pos += 1
    
    new_content = content[:insert_pos] + '\n' + new_cards + content[insert_pos:]
    
    # Update tool count: find all 4-digit numbers like 2881, 2901 etc and increment by 5
    # Match patterns like "2881+" or "2871+"
    def replace_count(m):
        num = int(m.group(1))
        new_num = num + 5
        return str(new_num) + m.group(2)
    
    new_content = re.sub(r'(\d{4})\+', replace_count, new_content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    new_count = len(re.findall(r'<div class="tool-card"', new_content))
    print(f"  Updated: {len(existing_cards)} → {new_count} cards")

# Process both pages
add_cards(os.path.join(SITE, "index.html"), "cn", 2901)
add_cards(os.path.join(SITE, "en", "index.html"), "en", 2881)

print("\n✅ Homepage cards updated!")