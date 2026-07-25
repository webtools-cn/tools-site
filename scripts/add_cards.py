#!/usr/bin/env python3
"""添加新工具卡片到中英文首页"""
import re

BASE = '/home/chison/tools-site'

# 新工具列表
NEW_TOOLS = [
    {
        'slug': 'meeting-cost-calculator',
        'category': 'calculators',
        'cn_name': '会议成本计算器',
        'cn_desc': '计算会议总成本，量化无效会议开销',
        'en_name': 'Meeting Cost Calculator',
        'en_desc': 'Calculate meeting costs, quantify inefficient meetings',
    },
    {
        'slug': 'blood-alcohol-calculator',
        'category': 'calculators',
        'cn_name': '血液酒精浓度计算器',
        'cn_desc': '根据体重、饮酒量和时间估算BAC值',
        'en_name': 'BAC Calculator',
        'en_desc': 'Estimate blood alcohol content based on weight & drinks',
    },
    {
        'slug': 'invoice-template',
        'category': 'generators',
        'cn_name': '发票模板生成器',
        'cn_desc': '创建专业发票，一键导出PDF或打印',
        'en_name': 'Invoice Template Generator',
        'en_desc': 'Create professional invoices, export as PDF or print',
    },
    {
        'slug': 'moon-phase-calendar',
        'category': 'calculators',
        'cn_name': '月相日历',
        'cn_desc': '查询任意日期月相状态、月龄和可见度',
        'en_name': 'Moon Phase Calendar',
        'en_desc': 'Check moon phase, age & illumination for any date',
    },
    {
        'slug': 'amortization-schedule',
        'category': 'calculators',
        'cn_name': '分期还款计划表',
        'cn_desc': '生成等额本息/等额本金还款计划表',
        'en_name': 'Amortization Schedule',
        'en_desc': 'Generate equal installment/principal repayment schedule',
    },
]

def add_cards(filepath, is_en=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 tools-grid 的结束位置 (</div> 之前)
    # 找到最后一个 </div> 在 tools-grid 之后
    grid_start = content.find('class="tools-grid"')
    if grid_start == -1:
        print(f"❌ 未找到 tools-grid")
        return
    
    # 找到对应的闭合 </div>
    depth = 0
    insert_pos = grid_start
    i = content.find('<div', grid_start)
    while i != -1:
        tag_start = content[i:i+4]
        if tag_start == '<div':
            # 检查是否是自闭合或只是开头
            if not content[i:i+5].startswith('<div '):
                # 可能是 <div> 或 <div class=...
                pass
            depth += 1
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                insert_pos = i
                break
        i = content.find('<div', i+1) if content.find('<div', i+1) != -1 else content.find('</div>', i+1)
        if i == -1:
            break
    
    if insert_pos == grid_start:
        print(f"❌ 未找到 tools-grid 闭合标签")
        return
    
    cards_html = ''
    for tool in NEW_TOOLS:
        if is_en:
            cards_html += f'\n        <div class="tool-card" data-category="{tool["category"]}"><span>{tool["en_name"]}</span><p>{tool["en_desc"]}</p><a href="/en/{tool["slug"]}/" class="btn">Use Now</a></div>'
        else:
            cards_html += f'\n        <div class="tool-card" data-category="{tool["category"]}"><span>{tool["cn_name"]}</span><p>{tool["cn_desc"]}</p><a href="/{tool["slug"]}/" class="btn">立即使用</a></div>'
    
    new_content = content[:insert_pos] + cards_html + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    count = new_content.count('tool-card')
    print(f"{'EN' if is_en else 'CN'}首页: 添加5张卡片, 总计 {count} 张")

# 添加中英文首页
add_cards(f'{BASE}/index.html', is_en=False)
add_cards(f'{BASE}/en/index.html', is_en=True)