#!/usr/bin/env python3
"""
批量SEO优化脚本：为缺少tool-description和相关工具内链的新工具添加SEO元素
"""
import re, os

TOOLS_DIR = "/home/chison/tools-site"

# 工具配置: slug -> {cn_desc, en_desc, related: [(slug, label)]}
TOOLS = {
    "biorhythm-calculator": {
        "cn_desc": "基于经典生物节律理论，输入出生日期自动计算体力（23天）、情绪（28天）和智力（33天）三条正弦曲线，可视化展示高潮期、低潮期和临界日，帮助您合理安排工作和生活节奏。",
        "en_desc": "Calculate your physical (23-day), emotional (28-day), and intellectual (33-day) biorhythm cycles based on your birth date. Visualize sine curves with high, low, and critical day indicators for better daily planning.",
        "related_cn": [("age-calculator", "🎂 在线年龄计算器"), ("bmi-calculator", "🧮 在线BMI计算器"), ("body-fat-calculator", "体脂率计算器")],
        "related_en": [("age-calculator", "🎂 Age Calculator"), ("bmi-calculator", "🧮 BMI Calculator"), ("body-fat-calculator", "Body Fat Calculator")],
    },
    "bird-age-calculator": {
        "cn_desc": "根据宠物鸟品种和实际年龄，自动换算人类等效年龄。支持鹦鹉、金丝雀、鸽子、虎皮鹦鹉、金刚鹦鹉等常见品种，帮助宠物主人了解爱鸟所处的生命阶段。",
        "en_desc": "Convert your pet bird's actual age to human equivalent years based on species. Supports parrots, canaries, pigeons, budgies, macaws, and more common pet bird breeds.",
        "related_cn": [("dog-age-calculator", "🐕 狗狗年龄计算器"), ("cat-age-calculator", "🐱 猫咪年龄计算器"), ("age-calculator", "🎂 在线年龄计算器")],
        "related_en": [("dog-age-calculator", "🐕 Dog Age Calculator"), ("cat-age-calculator", "🐱 Cat Age Calculator"), ("age-calculator", "🎂 Age Calculator")],
    },
    "brew-ratio-calculator": {
        "cn_desc": "根据咖啡豆重量和冲泡水量自动计算咖啡粉水比，支持手冲、法压壶、意式浓缩、冷萃等多种冲泡方式，帮助咖啡爱好者精准控制口感浓度。",
        "en_desc": "Calculate the optimal coffee-to-water brewing ratio based on your coffee weight and water volume. Supports pour-over, French press, espresso, and cold brew methods for perfect extraction.",
        "related_cn": [("caffeine-calculator", "☕ 咖啡因计算器"), ("water-intake-calculator", "💧 每日饮水计算器"), ("recipe-converter", "🍳 食谱换算器")],
        "related_en": [("caffeine-calculator", "☕ Caffeine Calculator"), ("water-intake-calculator", "💧 Water Intake Calculator"), ("recipe-converter", "🍳 Recipe Converter")],
    },
    "decking-calculator": {
        "cn_desc": "输入露台面积和单块地板尺寸，自动计算所需地板数量（含合理损耗率）。支持多种地板规格，帮助DIY爱好者和施工方精确估算材料用量和采购成本。",
        "en_desc": "Calculate the number of decking boards needed based on your deck area and board dimensions, including a reasonable waste factor. Perfect for DIY enthusiasts and contractors planning material orders.",
        "related_cn": [("area-calculator", "📐 面积计算器"), ("paint-estimator", "🎨 涂料用量计算器"), ("tile-estimator", "🧱 瓷砖用量计算器")],
        "related_en": [("area-calculator", "📐 Area Calculator"), ("paint-estimator", "🎨 Paint Estimator"), ("tile-estimator", "🧱 Tile Estimator")],
    },
    "electricity-bill-calculator": {
        "cn_desc": "根据用电量（度）和电价自动计算每日、每月和年度电费支出。支持阶梯电价和峰谷电价模式，帮助家庭和企业快速估算用电成本，合理规划用电预算。",
        "en_desc": "Calculate daily, monthly, and annual electricity costs based on your consumption (kWh) and unit rate. Supports tiered pricing and peak/off-peak rates for accurate bill estimation.",
        "related_cn": [("electricity-cost-calculator", "⚡ 用电成本计算器"), ("carbon-footprint-calculator", "🌍 碳足迹计算器"), ("roi-calculator", "📈 ROI计算器")],
        "related_en": [("electricity-cost-calculator", "⚡ Electricity Cost Calculator"), ("carbon-footprint-calculator", "🌍 Carbon Footprint"), ("roi-calculator", "📈 ROI Calculator")],
    },
    "employee-cost-calculator": {
        "cn_desc": "综合计算员工年度总成本，包括基本工资、社保公积金、年终奖金、办公场地、设备折旧等费用。帮助企业HR和创业者精确核算人力成本，做出合理的招聘决策。",
        "en_desc": "Estimate the total annual cost of an employee including base salary, social insurance, bonuses, office space, and equipment. Helps HR professionals and business owners budget accurately for hiring.",
        "related_cn": [("salary-calculator", "💵 工资计算器"), ("roi-calculator", "📈 ROI计算器"), ("compound-interest-calculator", "💰 复利计算器")],
        "related_en": [("salary-calculator", "💵 Salary Calculator"), ("roi-calculator", "📈 ROI Calculator"), ("compound-interest-calculator", "💰 Compound Interest")],
    },
    "fish-tank-volume-calculator": {
        "cn_desc": "输入鱼缸长宽高，自动计算水体体积（支持升和加仑两种单位）。帮助水族爱好者确定合理饲养密度、加药量和换水量，确保鱼类健康生长。",
        "en_desc": "Calculate your aquarium's water volume in liters and gallons by entering the tank dimensions. Helps fish keepers determine proper stocking density, medication dosage, and water change amounts.",
        "related_cn": [("volume-calculator", "📦 体积计算器"), ("water-intake-calculator", "💧 每日饮水计算器"), ("cylinder-volume-calculator", "🛢️ 圆柱体积计算器")],
        "related_en": [("volume-calculator", "📦 Volume Calculator"), ("water-intake-calculator", "💧 Water Intake"), ("cylinder-volume-calculator", "🛢️ Cylinder Volume")],
    },
    "gear-ratio-calculator": {
        "cn_desc": "输入主动轮和从动轮齿数，一键计算齿轮传动比、输出转速和输出扭矩。支持多级齿轮串联计算，适用于机械工程学习、DIY项目设计和自行车变速系统调试。",
        "en_desc": "Enter the number of teeth on your driving and driven gears to instantly calculate gear ratio, output RPM, and torque. Supports multi-stage gear trains for mechanical engineering and bicycle gearing.",
        "related_cn": [("unit-converter", "📏 单位换算器"), ("speed-converter", "🚀 速度换算器"), ("torque-converter", "🔧 扭矩换算器")],
        "related_en": [("unit-converter", "📏 Unit Converter"), ("speed-converter", "🚀 Speed Converter"), ("torque-converter", "🔧 Torque Converter")],
    },
    "golf-handicap-calculator": {
        "cn_desc": "输入多轮杆数和各球场难度指数，使用WHS世界差点系统标准公式自动计算差点指数。帮助高尔夫爱好者客观评估实战水平，公平制定比赛让杆方案。",
        "en_desc": "Calculate your golf handicap index using the WHS (World Handicap System) formula. Enter your scores and course ratings across multiple rounds to get an accurate, globally recognized handicap.",
        "related_cn": [("bmi-calculator", "🧮 BMI计算器"), ("pace-calculator", "🏃 配速计算器"), ("swim-pace-calculator", "🏊 游泳配速计算器")],
        "related_en": [("bmi-calculator", "🧮 BMI Calculator"), ("pace-calculator", "🏃 Pace Calculator"), ("swim-pace-calculator", "🏊 Swim Pace Calculator")],
    },
    "number-converter": {
        "cn_desc": "免费在线阿拉伯数字与大写中文数字互转工具。支持中文大写（壹贰叁）、小写数字和人民币金额大写三种模式，适用于财务报销单填写、合同金额书写和发票开具等正式场景。",
        "en_desc": "Convert Arabic numerals to uppercase Chinese characters (壹贰叁) and vice versa. Supports standard uppercase, lowercase Chinese numbers, and RMB amount format for financial documents and contracts.",
        "related_cn": [("case-converter", "🔤 大小写转换"), ("text-counter", "📝 字数统计"), ("random-number-generator", "🎲 随机数生成器")],
        "related_en": [("case-converter", "🔤 Case Converter"), ("text-counter", "📝 Text Counter"), ("random-number-generator", "🎲 Random Number Generator")],
    },
    "swim-pace-calculator": {
        "cn_desc": "输入游泳距离和完成时间，自动计算每100米配速、平均时速和不同距离预估完赛时间。帮助游泳爱好者科学制定训练计划，追踪进步曲线。",
        "en_desc": "Enter your swimming distance and time to calculate pace per 100m, average speed, and estimated finish times for various distances. Helps swimmers plan workouts and track performance improvements.",
        "related_cn": [("pace-calculator", "🏃 配速计算器"), ("golf-handicap-calculator", "⛳ 高尔夫差点计算器"), ("bmi-calculator", "🧮 BMI计算器")],
        "related_en": [("pace-calculator", "🏃 Pace Calculator"), ("golf-handicap-calculator", "⛳ Golf Handicap"), ("bmi-calculator", "🧮 BMI Calculator")],
    },
}


def insert_after_h1(content, insertion, anchor_pattern):
    """在h1后面的指定位置插入HTML"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if anchor_pattern in line:
            lines.insert(i + 1, insertion)
            return '\n'.join(lines)
    return content


def insert_before_footer(content, insertion):
    """在</footer>前面插入HTML"""
    return content.replace('</footer>', insertion + '\n</footer>')


def process_cn_file(slug, info):
    """处理CN页面"""
    filepath = os.path.join(TOOLS_DIR, f"{slug}/index.html")
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. 检查是否已有tool-description
    if 'class="tool-description"' not in content and 'tool-description' not in content:
        # 找到h1后插入tool-description的p标签
        # 类型A: 有hero区的页面 (biorhythm, gear-ratio, number-converter)
        # 类型B: 有 subtitle 类的页面
        desc_html = f'\n<p class="tool-description" style="color:#94a3b8;font-size:.95rem;margin:8px 0 16px;line-height:1.6">{info["cn_desc"]}</p>'
        
        if '<p class="subtitle">' in content:
            # 类型B: 在subtitle p后面插入
            content = content.replace(
                '</p>\n<div class="card">',
                f'</p>\n{desc_html}\n<div class="card">'
            )
            # 如果没有匹配到card，尝试其他
            if desc_html not in content:
                content = insert_after_h1(content, desc_html, '<p class="subtitle">')
            modified = True
        elif '<div class="hero">' in content:
            # 类型A: 在hero区域内，badge span前面或后面
            if '<span class="badge">' in content:
                content = content.replace(
                    '</span>\n</div>',
                    f'</span>\n{desc_html}\n</div>'
                )
                if desc_html not in content:
                    content = content.replace(
                        '<span class="badge">',
                        f'{desc_html}\n<span class="badge">'
                    )
            else:
                # hero没有badge
                content = content.replace(
                    '</p>\n</div>',
                    f'</p>\n{desc_html}\n</div>'
                )
            modified = True
        else:
            # 直接找h1后
            content = insert_after_h1(content, desc_html, '</h1>')
            modified = True
    
    # 2. 检查是否已有related-tools
    if 'class="related-tools"' not in content and 'related-tools' not in content:
        links = ''.join(
            f'  <a href="../{slug}/" style="color:#06b6d4;text-decoration:none;font-size:14px;display:block;padding:6px 0">{label}</a>\n'
            for slug, label in info["related_cn"]
        )
        related_html = f'\n<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#1e293b;border-radius:8px;border:1px solid rgba(148,163,184,.1)"><h2 style="color:#f1f5f9;font-size:18px;margin-bottom:12px">🔗 相关工具推荐</h2>\n{links}</section>\n'
        content = insert_before_footer(content, related_html)
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def process_en_file(slug, info):
    """处理EN页面"""
    filepath = os.path.join(TOOLS_DIR, f"en/{slug}/index.html")
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. tool-description
    if 'class="tool-description"' not in content and 'tool-description' not in content:
        desc_html = f'\n<p class="tool-description" style="color:#94a3b8;font-size:.95rem;margin:8px 0 16px;line-height:1.6">{info["en_desc"]}</p>'
        
        if '<p class="subtitle">' in content:
            content = content.replace(
                '</p>\n<div class="card">',
                f'</p>\n{desc_html}\n<div class="card">'
            )
            if desc_html not in content:
                content = insert_after_h1(content, desc_html, '<p class="subtitle">')
            modified = True
        elif '<div class="hero">' in content:
            if '<span class="badge">' in content:
                content = content.replace(
                    '</span>\n</div>',
                    f'</span>\n{desc_html}\n</div>'
                )
                if desc_html not in content:
                    content = content.replace(
                        '<span class="badge">',
                        f'{desc_html}\n<span class="badge">'
                    )
            else:
                content = content.replace(
                    '</p>\n</div>',
                    f'</p>\n{desc_html}\n</div>'
                )
            modified = True
        else:
            content = insert_after_h1(content, desc_html, '</h1>')
            modified = True
    
    # 2. related-tools
    if 'class="related-tools"' not in content and 'related-tools' not in content:
        links = ''.join(
            f'  <a href="../{slug}/" style="color:#06b6d4;text-decoration:none;font-size:14px;display:block;padding:6px 0">{label}</a>\n'
            for slug, label in info["related_en"]
        )
        related_html = f'\n<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#1e293b;border-radius:8px;border:1px solid rgba(148,163,184,.1)"><h2 style="color:#f1f5f9;font-size:18px;margin-bottom:12px">🔗 Related Tools</h2>\n{links}</section>\n'
        content = insert_before_footer(content, related_html)
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    cn_count = 0
    en_count = 0
    
    for slug, info in TOOLS.items():
        print(f"Processing: {slug}")
        if process_cn_file(slug, info):
            cn_count += 1
            print(f"  CN ✅")
        else:
            print(f"  CN ⏭️ (already done)")
        
        if process_en_file(slug, info):
            en_count += 1
            print(f"  EN ✅")
        else:
            print(f"  EN ⏭️ (already done)")
    
    print(f"\nDONE: {cn_count} CN + {en_count} EN files modified")


if __name__ == "__main__":
    main()
