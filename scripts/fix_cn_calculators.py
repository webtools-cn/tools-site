#!/usr/bin/env python3
"""Fix 8 CN calculator pages: replace generic steps and FAQ with tool-specific content."""

import re

# CN tool-specific content
CN_TOOLS = {
    'apr-calculator': {
        'name': '年化利率计算器',
        'steps': [
            '输入贷款金额（如10万元）',
            '输入年利率和手续费比例（如5%利率、1%手续费）',
            '点击"计算"按钮查看实际年化利率',
        ],
        'faq': [
            ('APR和利率有什么区别？', 'APR（年化利率）包含了利率和手续费等全部费用，反映真实的借款成本。名义利率只算利息，不含费用，所以APR通常更高。'),
            ('APR是怎么算的？', '先从贷款金额中扣除手续费得到净到手金额，再按月利率等额本息还款，最后将总还款额与净到手金额的差额折算为年化百分比。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'tip-calculator': {
        'name': '小费计算器',
        'steps': [
            '输入账单总金额',
            '设置小费比例（如15%、18%、20%）',
            '输入分摊人数，点击"计算"查看每人应付金额',
        ],
        'faq': [
            ('小费一般给多少？', '在美国，15%-20%是常见的小费比例，18%是比较标准的默认值。其他国家的小费文化不同，请根据当地习惯调整。'),
            ('人均金额怎么算的？', '人均金额 =（账单 + 小费）÷ 分摊人数。如果人数填0，则显示总金额。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'discount-calculator': {
        'name': '折扣计算器',
        'steps': [
            '输入商品原价',
            '输入折扣百分比（如25表示打75折）',
            '输入额外满减金额（如有），点击"计算"查看折后价',
        ],
        'faq': [
            ('折后价怎么算的？', '折后价 = 原价 - 原价×折扣% - 额外满减。结果不会为负数。'),
            ('支持叠加折扣吗？', '本工具支持一个百分比折扣加一个固定满减。如果是多个百分比折扣，请分次计算。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'commission-calculator': {
        'name': '佣金计算器',
        'steps': [
            '输入销售总额',
            '输入佣金比例（如5%表示5%）',
            '输入基础工资，点击"计算"查看总收入',
        ],
        'faq': [
            ('佣金怎么算的？', '佣金 = 销售额 × 佣金比例。总收入 = 佣金 + 基础工资。'),
            ('支持阶梯佣金吗？', '本工具使用单一佣金比例。如果是阶梯佣金，请分别计算每个阶梯后相加。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'fuel-cost-calculator': {
        'name': '油费计算器',
        'steps': [
            '输入单程距离（公里）',
            '输入车辆百公里油耗（升/100km）',
            '输入油价（元/升），点击"计算"查看单程和往返油费',
        ],
        'faq': [
            ('油费怎么算的？', '油耗量 = 距离 ÷ 100 × 百公里油耗。费用 = 油耗量 × 油价。往返费用为单程的2倍。'),
            ('支持往返计算吗？', '支持，结果同时显示单程费用和往返费用。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'electricity-cost-calculator': {
        'name': '电费计算器',
        'steps': [
            '输入电器功率（瓦，如1500W）',
            '输入每日使用时长（小时）',
            '输入电价（元/度），点击"计算"查看每日/每月/每年电费',
        ],
        'faq': [
            ('电费怎么算的？', '每日用电量(度) = 功率(W) × 使用时长(h) ÷ 1000。每日电费 = 用电量 × 电价。月费 = 日费 × 30，年费 = 日费 × 365。'),
            ('为什么按30天算月费？', '为方便计算，按每月30天估算。如需精确值，请用日费乘以实际计费天数。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'body-fat-calculator': {
        'name': '体脂率计算器',
        'steps': [
            '输入身高（厘米）',
            '输入体重（公斤）',
            '输入腰围（厘米），点击"计算"查看体脂率',
        ],
        'faq': [
            ('什么是美国海军体脂测量法？', '美国海军方法通过身体围度（如腰围）来估算体脂率，是一种简便的体脂估算方法。'),
            ('这个计算器准确吗？', '本工具基于公式估算，仅供参考。如需精确的体成分分析，请咨询专业医疗机构或使用DEXA等专业设备。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
            ('数据安全吗？', '所有计算在浏览器本地完成，数据不会上传到任何服务器。'),
        ],
    },
    'calorie-calculator': {
        'name': '每日热量计算器',
        'steps': [
            '输入体重（公斤）',
            '输入身高（厘米）',
            '输入年龄，点击"计算"查看基础代谢和每日热量需求',
        ],
        'faq': [
            ('什么是基础代谢率(BMR)？', '基础代谢率是身体在完全静息状态下维持基本生命功能（如呼吸、循环）所消耗的最低热量。'),
            ('什么是TDEE？', 'TDEE（每日总能量消耗）= BMR × 活动系数。久坐=1.2，中等=1.55，高强度=1.9。'),
            ('用的是什么公式？', '本工具使用Mifflin-St Jeor公式，这是目前最被推荐的基础代谢率估算公式之一。'),
            ('这个工具免费吗？', '完全免费，无需注册、无需下载，打开网页即可使用。'),
        ],
    },
}

def build_cn_faq_html(faq_items):
    html = '<div class="faq">\n'
    for q, a in faq_items:
        html += f'<h3>{q}</h3>\n<p>{a}</p>\n'
    html += '</div>'
    return html

def build_cn_faq_json(faq_items):
    items = []
    for q, a in faq_items:
        # Escape quotes for JSON
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        items.append(f'{{"@type":"Question","name":"{q_esc}","acceptedAnswer":{{"@type":"Answer","text":"{a_esc}"}}}}')
    return '[' + ','.join(items) + ']'

for tool, config in CN_TOOLS.items():
    path = f'{tool}/index.html'
    html = open(path).read()
    
    # Replace steps
    old_steps = re.search(r'<ol>\s*<li>输入第一个参数</li>\s*<li>输入第二个参数</li>\s*<li>点击"计算"按钮查看结果</li>\s*</ol>', html)
    if old_steps:
        new_steps = '<ol>\n' + '\n'.join(f'  <li>{s}</li>' for s in config['steps']) + '\n</ol>'
        html = html.replace(old_steps.group(0), new_steps)
    
    # Replace FAQ visible HTML
    old_faq = re.search(r'<div class="faq">.*?</div>\s*</main>', html, re.DOTALL)
    if old_faq:
        new_faq = build_cn_faq_html(config['faq']) + '\n</main>'
        html = html.replace(old_faq.group(0), new_faq)
    
    # Replace FAQ JSON in schema
    old_faq_json = re.search(r'"mainEntity":FAQ_CN_JSON', html)
    if old_faq_json:
        new_faq_json = f'"mainEntity":{build_cn_faq_json(config["faq"])}'
        html = html.replace('FAQ_CN_JSON', new_faq_json.split('"mainEntity":')[1])
    
    with open(path, 'w') as f:
        f.write(html)
    print(f"✅ {tool} CN updated")

print("\nAll 8 CN pages updated!")
