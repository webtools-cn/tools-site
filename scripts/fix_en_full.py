#!/usr/bin/env python3
"""全面修复8个EN页面的占位符和中文残留"""
import os, re

# 每个工具的英文内容
TOOLS = {
    'paint-needed-calculator': {
        'name': 'Paint Needed Calculator',
        'desc_seo': 'Calculate exact paint liters needed based on wall area, coverage per liter, and number of coats. Essential for home renovation planning.',
        'desc_short': 'Calculate exact paint liters needed based on wall area, coverage, and coats.',
        'seo_intro': 'Paint Needed Calculator is a free online tool that calculates the exact amount of paint required based on wall area, paint coverage per liter, and number of coats. It works on both mobile and desktop, with all calculations done locally in your browser — your data never leaves your device.',
        'steps': ['Enter the wall area in square meters', 'Enter the paint coverage per liter', 'Enter the number of coats needed', 'Click "Calculate" to see the result'],
        'faq': '<h3>Is this tool accurate?</h3><p>The calculation is based on standard mathematical formulas, providing precise and reliable results.</p><h3>Do I need to download anything?</h3><p>No download required — simply open the webpage and start calculating. Everything runs in your browser.</p>',
        'faq_json': '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The calculation is based on standard mathematical formulas, providing precise and reliable results."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download required. Simply open the webpage and start calculating."}}]',
        'js_result': 'a.toLocaleString()+"m² × "+c+" coats ÷ "+b+"m²/L = "+r.toFixed(1)+" L"',
        'js_error': 'Please enter all values',
    },
    'paper-size-calculator': {
        'name': 'Paper Size Converter',
        'desc_seo': 'Convert ISO A-series paper sizes (A0-A10) to mm, inches, and pixels at any DPI. Quick reference for printing and design.',
        'desc_short': 'Convert A-series paper sizes to mm, inches, and pixels at any DPI.',
        'seo_intro': 'Paper Size Converter is a free online tool that converts ISO A-series paper sizes (A0 through A10) to millimeters, inches, and pixels at any DPI setting. Perfect for printing, graphic design, and document preparation. All calculations run locally in your browser.',
        'steps': ['Enter the A-series number (0-10, e.g. 4 for A4)', 'Optionally enter a DPI value (default 300)', 'Click "Calculate" to see dimensions'],
        'faq': '<h3>Is this tool accurate?</h3><p>Yes, dimensions follow the ISO 216 standard for A-series paper sizes.</p><h3>What DPI should I use?</h3><p>300 DPI is standard for print quality. Use 72 for screen/web, 150 for draft prints.</p>',
        'faq_json': '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, dimensions follow the ISO 216 standard for A-series paper sizes."}},{"@type":"Question","name":"What DPI should I use?","acceptedAnswer":{"@type":"Answer","text":"300 DPI is standard for print quality. Use 72 for screen/web, 150 for draft prints."}}]',
        'js_result': '"A"+a+": "+w+"×"+h+"mm | "+(w/25.4).toFixed(1)+"×"+(h/25.4).toFixed(1)+"in | "+(Math.round(w/25.4*b))+"×"+(Math.round(h/25.4*b))+"px @"+b+"dpi"',
        'js_error': 'Please enter 0-10',
    },
    'mix-ratio-calculator': {
        'name': 'Mix Ratio Calculator',
        'desc_seo': 'Calculate exact quantities for two-component mixtures based on ratio and total volume. Perfect for epoxy, resin, paint, and chemical mixing.',
        'desc_short': 'Calculate component quantities for any two-part mixture ratio.',
        'seo_intro': 'Mix Ratio Calculator is a free online tool that calculates the exact amount of each component needed when mixing two substances at a given ratio. Ideal for epoxy resin, paint mixing, chemical solutions, and cooking. All calculations run locally in your browser.',
        'steps': ['Enter the ratio for component A', 'Enter the ratio for component B', 'Enter the total amount needed', 'Click "Calculate" to see quantities'],
        'faq': '<h3>Is this tool accurate?</h3><p>Yes, calculations use standard proportional math for precise results.</p><h3>Can I use decimal ratios?</h3><p>Yes, you can enter decimal values like 1.5:1 for precise mixing.</p>',
        'faq_json': '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, calculations use standard proportional math for precise results."}},{"@type":"Question","name":"Can I use decimal ratios?","acceptedAnswer":{"@type":"Answer","text":"Yes, you can enter decimal values like 1.5:1 for precise mixing."}}]',
        'js_result': '"A:B="+a+":"+b+", total "+c+" → A needs "+qa.toFixed(2)+", B needs "+qb.toFixed(2)',
        'js_error': 'Please enter all values',
    },
    'coffee-cost-calculator': {
        'name': 'Coffee Cost Calculator',
        'desc_seo': 'Compare homemade vs store-bought coffee costs. See daily, monthly, and yearly savings from brewing at home.',
        'desc_short': 'Compare homemade vs store-bought coffee costs and see your savings.',
        'seo_intro': 'Coffee Cost Calculator is a free online tool that compares the cost of making coffee at home versus buying it from a cafe. See exactly how much you save per day, month, and year. All calculations run locally in your browser.',
        'steps': ['Enter the cost per cup when making at home', 'Enter the cost per cup at a cafe', 'Enter how many cups per day', 'Click "Calculate" to see savings'],
        'faq': '<h3>Is this tool accurate?</h3><p>Yes, it uses simple multiplication based on your input values.</p><h3>Does it account for equipment costs?</h3><p>No, it only compares per-cup costs. Factor in equipment separately for full analysis.</p>',
        'faq_json': '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, it uses simple multiplication based on your input values."}},{"@type":"Question","name":"Does it account for equipment costs?","acceptedAnswer":{"@type":"Answer","text":"No, it only compares per-cup costs. Factor in equipment separately for full analysis."}}]',
        'js_result': '"Save $"+dy.toFixed(1)+"/day → $"+mo.toFixed(0)+"/month → $"+yr.toFixed(0)+"/year"',
        'js_error': 'Please enter all values',
    },
    'ramp-slope-calculator': {
        'name': 'Ramp Slope Calculator',
        'desc_seo': 'Calculate ramp slope percentage, angle in degrees, and ratio from height and length. ADA compliance check for accessibility ramps.',
        'desc_short': 'Calculate ramp slope, angle, and ratio from height and length.',
        'seo_intro': 'Ramp Slope Calculator is a free online tool that calculates the slope percentage, angle in degrees, and ratio of a ramp based on its height and horizontal length. Useful for accessibility planning, wheelchair ramps, and construction. All calculations run locally in your browser.',
        'steps': ['Enter the ramp height (rise)', 'Enter the horizontal length (run)', 'Click "Calculate" to see slope details'],
        'faq': '<h3>What is ADA-compliant slope?</h3><p>ADA recommends a maximum slope of 1:12 (8.33%) for wheelchair ramps.</p><h3>Is this tool accurate?</h3><p>Yes, it uses standard trigonometric formulas for precise results.</p>',
        'faq_json': '[{"@type":"Question","name":"What is ADA-compliant slope?","acceptedAnswer":{"@type":"Answer","text":"ADA recommends a maximum slope of 1:12 (8.33%) for wheelchair ramps."}},{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, it uses standard trigonometric formulas for precise results."}}]',
        'js_result': '"Slope "+p+"% | Angle "+deg.toFixed(1)+"° | Ratio 1:"+(b/a).toFixed(1)',
        'js_error': 'Please enter all values',
    },
    'carpet-cost-calculator': {
        'name': 'Carpet Cost Calculator',
        'desc_seo': 'Calculate total carpet cost including waste allowance. Enter area, price per unit, and waste percentage for accurate budgeting.',
        'desc_short': 'Calculate total carpet cost with waste allowance for accurate budgeting.',
        'seo_intro': 'Carpet Cost Calculator is a free online tool that estimates the total cost of carpeting a room, including a configurable waste allowance percentage. Perfect for home renovation budgeting. All calculations run locally in your browser.',
        'steps': ['Enter the room area in square meters', 'Enter the carpet price per square meter', 'Optionally enter waste percentage (default 10%)', 'Click "Calculate" to see total cost'],
        'faq': '<h3>Why add waste allowance?</h3><p>Cutting and pattern matching requires extra material. 10% is standard for simple rooms.</p><h3>Is this tool accurate?</h3><p>Yes, it uses standard area and percentage calculations.</p>',
        'faq_json': '[{"@type":"Question","name":"Why add waste allowance?","acceptedAnswer":{"@type":"Answer","text":"Cutting and pattern matching requires extra material. 10% is standard for simple rooms."}},{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, it uses standard area and percentage calculations."}}]',
        'js_result': '"With "+c+"% waste: "+area.toFixed(1)+"m² × "+b+" = Total $"+cost.toFixed(0)',
        'js_error': 'Please enter all values',
    },
    'soil-volume-calculator': {
        'name': 'Soil Volume Calculator',
        'desc_seo': 'Calculate soil volume for round or square pots. Get liters and approximate weight in kilograms for your gardening needs.',
        'desc_short': 'Calculate soil volume in liters for round or square planters.',
        'seo_intro': 'Soil Volume Calculator is a free online tool that calculates the volume of soil needed for round or square planters. Get results in cubic centimeters, liters, and approximate weight. Perfect for gardening and planting. All calculations run locally in your browser.',
        'steps': ['Enter the pot diameter (round) or side length (square) in cm', 'Enter the pot depth in cm', 'Select pot type: 1 for round, 2 for square', 'Click "Calculate" to see soil volume'],
        'faq': '<h3>How is soil weight estimated?</h3><p>We use an average soil density of 0.6 kg/liter. Actual weight varies by soil type and moisture.</p><h3>Is this tool accurate?</h3><p>Yes, it uses standard geometric volume formulas.</p>',
        'faq_json': '[{"@type":"Question","name":"How is soil weight estimated?","acceptedAnswer":{"@type":"Answer","text":"We use an average soil density of 0.6 kg/liter. Actual weight varies by soil type and moisture."}},{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, it uses standard geometric volume formulas."}}]',
        'js_result': '(c===1?"Round":"Square")+" volume "+vol.toFixed(0)+"cm³ = "+lit.toFixed(1)+"L ≈ "+kg.toFixed(1)+"kg"',
        'js_error': 'Please enter all values',
    },
    'event-budget-calculator': {
        'name': 'Event Budget Calculator',
        'desc_seo': 'Allocate event budget across catering, venue, and other costs. Enter total budget and percentage splits for instant breakdown.',
        'desc_short': 'Allocate your event budget across catering, venue, and other costs.',
        'seo_intro': 'Event Budget Calculator is a free online tool that helps you allocate your event budget across catering, venue, and other expenses. Enter your total budget and percentage allocations to see the breakdown instantly. All calculations run locally in your browser.',
        'steps': ['Enter your total event budget', 'Enter the percentage for catering', 'Enter the percentage for venue', 'Click "Calculate" to see the breakdown'],
        'faq': '<h3>What if percentages exceed 100%?</h3><p>The calculator shows the combined total when catering and venue exceed 100%, indicating you need to adjust.</p><h3>Is this tool accurate?</h3><p>Yes, it uses standard percentage calculations.</p>',
        'faq_json': '[{"@type":"Question","name":"What if percentages exceed 100%?","acceptedAnswer":{"@type":"Answer","text":"The calculator shows the combined total when catering and venue exceed 100%, indicating you need to adjust."}},{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Yes, it uses standard percentage calculations."}}]',
        'js_result': '"Catering: $"+(a*b/100).toFixed(0)+" | Venue: $"+(a*c/100).toFixed(0)+(i>0?" | Other: $"+(a*i/100).toFixed(0)+" ("+i.toFixed(0)+"%)":" | Total "+(b+c).toFixed(0)+"%")',
        'js_error': 'Please enter all values',
    },
}

# 通用EN footer
EN_FOOTER_LINKS = {
    '联系我们': 'Contact',
    '隐私政策': 'Privacy Policy',
    '服务条款': 'Terms of Service',
    '关于我们': 'About',
}

EN_FOOTER_COPYRIGHT = '© 2026 Free ToolBase — All calculations run locally in your browser. No data uploaded to servers.'

for tool, data in TOOLS.items():
    filepath = f'en/{tool}/index.html'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 修复 meta description
    content = content.replace('TOOL_DESC_CN_SEO', data['desc_seo'])
    
    # 2. 修复 subtitle
    content = content.replace('TOOL_DESC_CN_SHORT', data['desc_short'])
    
    # 3. 修复 FAQ schema JSON
    content = content.replace('"mainEntity":FAQ_CN_JSON', f'"mainEntity":{data["faq_json"]}')
    
    # 4. 修复 SEO intro
    content = content.replace('TOOL_SEO_INTRO_CN', data['seo_intro'])
    
    # 5. 修复 "如何使用" → "How to Use"
    content = content.replace('如何使用', 'How to Use')
    
    # 6. 修复 steps
    content = content.replace('TOOL_STEP1_CN', data['steps'][0])
    content = content.replace('TOOL_STEP2_CN', data['steps'][1])
    content = content.replace('TOOL_STEP3_CN', data['steps'][2])
    
    # 7. 修复 FAQ placeholder
    content = content.replace('FAQ_PLACEHOLDER_CN', data['faq'])
    
    # 8. 修复 footer 中文链接
    for cn, en in EN_FOOTER_LINKS.items():
        content = content.replace(f'>{cn}<', f'>{en}<')
    
    # 9. 修复 footer copyright
    content = re.sub(r'© 2026 Free ToolBase —.*?</div>', f'{EN_FOOTER_COPYRIGHT}</div>', content, flags=re.DOTALL)
    
    # 10. 修复 lang-switch 链接 (应指向CN版)
    content = re.sub(r'href="/en/{tool}/"">English'.format(tool=tool), f'href="/{tool}/">中文', content)
    # 更通用：找到lang-switch里的链接
    content = re.sub(
        r'(<div class="lang-switch">)<a href="/en/[^"]*">English</a>(</div>)',
        rf'\1<a href="/{tool}/">中文</a>\2',
        content
    )
    
    # 11. 修复 hreflang zh 指向
    content = content.replace(
        f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/en/{tool}/">',
        f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{tool}/">'
    )
    
    # 12. 修复 JS 输出中文
    # 替换 show("请输入完整参数") → show("Please enter all values")
    content = content.replace('show("请输入完整参数")', f'show("{data["js_error"]}")')
    content = content.replace('show("请输入0-10")', f'show("{data["js_error"]}")')
    
    # 替换计算结果中的中文
    # 需要找到 result.textContent=... 的部分并替换
    # 先处理特定的JS中文片段
    if tool == 'paint-needed-calculator':
        content = content.replace(
            'a.toLocaleString()+"m² ×"+c+"层 ÷"+b+"m²/L = "+r.toFixed(1)+" 升"',
            data['js_result']
        )
    elif tool == 'mix-ratio-calculator':
        content = content.replace(
            '"A:B="+a+":"+b+", 总量"+c+" → A需要 "+qa.toFixed(2)+", B需要 "+qb.toFixed(2)',
            data['js_result']
        )
    elif tool == 'coffee-cost-calculator':
        content = content.replace(
            '"每天省"+dy.toFixed(1)+"元 → 每月"+mo.toFixed(0)+"元 → 每年"+yr.toFixed(0)+"元"',
            data['js_result']
        )
    elif tool == 'ramp-slope-calculator':
        content = content.replace(
            '"坡度 "+p+"% | 角度 "+deg.toFixed(1)+"° | 比值 1:"+(b/a).toFixed(1)',
            data['js_result']
        )
    elif tool == 'carpet-cost-calculator':
        content = content.replace(
            '"含"+c+"%损耗: "+area.toFixed(1)+"m² × "+b+" = 总费用 "+cost.toFixed(0)+""',
            data['js_result']
        )
    elif tool == 'soil-volume-calculator':
        content = content.replace(
            '(c===1?"圆形":"方形")+"体积 "+vol.toFixed(0)+"cm³ = "+lit.toFixed(1)+"L ≈ "+kg.toFixed(1)+"kg"',
            data['js_result']
        )
    elif tool == 'event-budget-calculator':
        content = content.replace(
            '"餐饮: "+(a*b/100).toFixed(0)+" | 场地: "+(a*c/100).toFixed(0)+(i>0?" | 其他: "+(a*i/100).toFixed(0)+"("+i.toFixed(0)+"%)":" | 合计"+(b+c).toFixed(0)+"%")',
            data['js_result']
        )
    elif tool == 'paper-size-calculator':
        # paper-size 没有中文在JS输出里，但show("请输入0-10")需要修
        pass
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    changes = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
    print(f"FIXED: {filepath} ({changes} lines changed)")

print("\nDone!")
