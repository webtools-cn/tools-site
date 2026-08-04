#!/usr/bin/env python3
"""Fix meta descriptions: expand short ones (<120) and trim long ones (>160) to 120-160 chars."""
import os, re, html

# All fixes: path_prefix -> new_description
fixes = {
    # CN short descriptions → expand to 120-160
    'online-clock': '免费在线时钟工具，支持模拟时钟和数字时钟双模式显示，可查看全球各时区当前时间，实时精准走时毫秒级更新。支持全屏模式、12/24小时制切换、世界时钟多城市对比，适合工作计时和跨时区协作。纯前端运行无需注册，数据绝不上传服务器，完全免费即开即用。',
    'asphalt-calculator': '免费在线沥青计算器，快速计算车道、停车场等铺装项目所需沥青体积、吨数和成本。支持矩形和圆形区域计算，公制和英制单位自由切换，内置压实系数和材料密度参数，自动估算项目总成本。适合道路施工和停车场建设预算规划，纯前端本地处理数据不上传，无需注册。',
    'rebar-calculator': '免费在线钢筋计算器，精确计算混凝土板钢筋网格数量、总长度、总重量和材料成本。支持公制与英制单位切换、搭接长度自动计算、SVG布局可视化预览，内置多种钢筋规格数据表，适合建筑工程预算和施工材料采购规划，纯前端本地运算数据不上传服务器，无需注册。',
    'insulation-calculator': '免费在线保温层计算器，快速计算墙体、天花板、地面所需保温材料面积和包数。支持玻璃纤维棉、岩棉、喷涂泡沫等多种材料类型，R值热阻计算，公制英制单位切换，多区域汇总统计。适合建筑节能改造和装修预算规划，纯前端本地处理数据不上传服务器，无需注册。',
    'pool-volume-calculator': '免费在线泳池水量计算器，支持矩形、圆形、椭圆和肾形等多种形状泳池的加仑与升水量计算。自动计算平均深度、水重量、滤水循环时间和初次注水成本估算，适用于泳池维护和化学品用量精确参考。纯前端本地计算无需安装注册，数据绝不上传服务器，完全免费即开即用。',
    'board-foot-calculator': '免费在线板英尺计算器，快速计算木材板英尺BF体积。支持多板批量输入、标准尺寸快捷选择、15种以上木材种类重量估算、浪费率系数设置、公制英制自由切换、成本估算含税费计算。木工和建筑行业必备工具，纯前端本地处理数据不上传服务器，无需注册即开即用。',
    'retaining-wall-calculator': '免费挡土墙计算器，输入墙长和墙高自动计算所需砌块数量、碎石回填量、基底沙子量和项目总成本。支持多种块材预设和自定义尺寸，公制英制切换，SVG布局可视化，含建筑规范安全提示。适合景观工程和DIY挡土墙项目规划，纯前端本地处理数据不上传服务器。',
    'wire-size-calculator': '免费在线电线尺寸计算器，根据电流、电压、距离自动推荐AWG电线规格。支持铜线和铝线、单相和三相电路，内置NEC标准载流量数据，同时验证电压降和载流量双重安全条件。电工布线和DIY配电必备工具，纯前端本地处理数据不上传服务器，无需注册即开即用。',
    'prorated-rent-calculator': '免费在线按比例租金计算器，支持月中入住或退房时按天精确计算应交租金金额。提供按当月天数、按365天、按30天标准月等多种计算方法对比，支持跨月日期范围自动拆分计算。搬家租房必备实用工具，纯前端本地运算数据不上传服务器，完全免费无需注册即开即用。',
    # EN long descriptions → trim to 120-160
    'en/deck-calculator': 'Free online deck calculator. Calculate deck boards, screws, fasteners, and cost. Supports wood and composite decking with waste factor. No signup required.',
    'en/grass-seed-calculator': 'Free online grass seed calculator. Enter lawn area to find seed needed. Supports 8 grass types, overseeding mode, and cost estimation. No signup required.',
    'en/board-foot-calculator': 'Free online board foot calculator. Calculate lumber volume in BF. Batch input, weight by species, waste factor, and cost estimation. No signup required.',
    'en/prorated-rent-calculator': 'Free prorated rent calculator. Calculate partial rent when moving in mid-month or out early. Compare 4 methods with cross-month support. No signup required.',
    'en/retaining-wall-calculator': 'Free retaining wall calculator. Enter wall dimensions to calculate blocks, gravel backfill, base sand, and total cost. Supports metric/imperial and SVG layout.',
    'en/wire-size-calculator': 'Free online wire size calculator. Find correct AWG gauge by current, voltage, and distance. Supports copper/aluminum with NEC ampacity and voltage drop.',
    'en/decibel-calculator': 'Free online decibel calculator. Convert dB to power/amplitude ratios, sum sound levels, and calculate dB gain or loss. For audio and acoustics. No signup.',
    'en/asphalt-calculator': 'Free online asphalt calculator. Calculate volume, tonnage, and cost for driveways and roads. Supports rectangular/circular areas, metric/imperial. No signup.',
    'en/insulation-calculator': 'Free online insulation calculator. Estimate fiberglass, mineral wool, spray foam, or rigid board for walls and ceilings. R-value lookup and multi-area totals.',
    'en/firewood-cord-calculator': 'Free online firewood cord calculator. Calculate cords, face cords, cubic volume, and cost. Includes BTU comparison for common firewood species. No registration.',
    'en/rebar-calculator': 'Free online rebar calculator. Calculate rebar pieces, length, weight, and cost for concrete slabs. Supports metric/imperial and SVG layout. No signup required.',
    'en/pool-volume-calculator': 'Free online pool volume calculator. Calculate gallons or liters for rectangular, circular, oval, and kidney pools. Includes fill cost estimate. No signup.',
    'en/jpg-to-webp': 'Free online JPG to WebP converter. Batch convert JPG images to WebP for smaller files. Pure frontend, images never leave your browser. No signup required.',
}

changed = 0
errors = 0

for prefix, new_desc in fixes.items():
    filepath = f'./{prefix}/index.html'
    if not os.path.exists(filepath):
        print(f'❌ NOT FOUND: {filepath}')
        errors += 1
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the meta description line and replace the content attribute
    old_len = None
    lines = content.split('\n')
    found = False
    for i, line in enumerate(lines):
        if 'name="description"' in line or "name='description'" in line:
            # Extract old content
            m = re.search(r'content\s*=\s*"([^"]*)"', line)
            if not m:
                m = re.search(r"content\s*=\s*'([^']*)'", line)
            if m:
                old_desc = m.group(1)
                old_len = len(html.unescape(old_desc))
                # Escape new desc for HTML attribute
                escaped = new_desc.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                lines[i] = line.replace(old_desc, escaped)
                found = True
                break

    if not found:
        print(f'❌ DESCRIPTION NOT FOUND: {filepath}')
        errors += 1
        continue

    new_content = '\n'.join(lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    status = '✅' if 120 <= len(new_desc) <= 160 else '⚠️'
    print(f'{status} {prefix}: {old_len} → {len(new_desc)} chars')
    changed += 1

print(f'\nChanged: {changed}, Errors: {errors}')
