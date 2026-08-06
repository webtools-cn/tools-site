#!/usr/bin/env python3
"""Batch SEO fix for new tools: meta desc, subtitle, related tool links."""
import re, os

base = "/home/chison/tools-site"

tools_data = {
    "roi-rental-calculator": {
        "cn": {
            "meta": "租房回报率计算器：免费在线计算房产投资回报率。输入购房价格、月租金和物业费，自动计算年化回报率与回本周期，助您科学评估投资价值。",
            "subtitle": "输入购房价格、月租金和年物业费，快速计算租房投资回报率。支持年化回报率和回本周期的计算，帮助评估房产投资价值。",
            "related": [
                ("按揭计算器", "/mortgage-calculator/"),
                ("贷款计算器", "/loan-calculator/"),
                ("复利计算器", "/compound-interest-calculator/"),
            ]
        },
        "en": {
            "meta": "Calculate rental property ROI instantly. Enter purchase price, monthly rent, and annual fees to get annualized return rate and payback period. Free online tool, no sign-up required.",
            "subtitle": "Enter the property purchase price, monthly rent, and annual fees to quickly calculate rental ROI. Supports annualized return rate and payback period calculations.",
            "related": [
                ("Mortgage Calculator", "/en/mortgage-calculator/"),
                ("Loan Calculator", "/en/loan-calculator/"),
                ("Compound Interest Calculator", "/en/compound-interest-calculator/"),
            ]
        }
    },
    "blend-ratio-calculator": {
        "cn": {
            "meta": "混合比例计算器：计算两种液体按不同比例混合后的浓度。适用于化学实验、涂料调配、农药稀释等场景。免费在线工具，快速精准计算。",
            "subtitle": "输入两种液体的体积和浓度，计算按不同比例混合后的最终浓度。适用于化学实验、涂料调配、农药稀释等场景。",
            "related": [
                ("浓度计算器", "/concentration-calculator/"),
                ("百分比计算器", "/percentage-calculator/"),
                ("稀释计算器", "/dilution-calculator/"),
            ]
        },
        "en": {
            "meta": "Blend Ratio Calculator: calculate final concentration when mixing two liquids at different ratios. Ideal for chemistry lab work, paint mixing, and pesticide dilution. Free online tool.",
            "subtitle": "Enter the volume and concentration of two liquids to calculate the final concentration at different mixing ratios. Ideal for chemistry, paint mixing, and dilution scenarios.",
            "related": [
                ("Concentration Calculator", "/en/concentration-calculator/"),
                ("Percentage Calculator", "/en/percentage-calculator/"),
                ("Dilution Calculator", "/en/dilution-calculator/"),
            ]
        }
    },
    "pipe-volume-calculator": {
        "cn": {
            "meta": "管道容积计算器：根据管道直径和长度快速计算内部容积和可容纳液体重量。支持多种单位，适用于工程、暖通、给排水等场景。",
            "subtitle": "输入管道内径和长度，快速计算管道内部容积和可容纳液体重量。支持毫米、厘米、米等多种单位，适用于工程、暖通、给排水等场景。",
            "related": [
                ("圆柱体积计算器", "/cylinder-volume-calc/"),
                ("水箱容积计算器", "/rectangular-tank-volume/"),
                ("流速计算器", "/flow-rate-calculator/"),
            ]
        },
        "en": {
            "meta": "Pipe Volume Calculator: compute internal pipe volume and liquid capacity from diameter and length. Supports multiple units. Perfect for plumbing, HVAC, and engineering projects.",
            "subtitle": "Enter pipe inner diameter and length to quickly calculate internal volume and liquid capacity. Supports mm, cm, m and other units. Ideal for engineering, HVAC, and plumbing.",
            "related": [
                ("Cylinder Volume Calculator", "/en/cylinder-volume-calc/"),
                ("Tank Volume Calculator", "/en/rectangular-tank-volume/"),
                ("Flow Rate Calculator", "/en/flow-rate-calculator/"),
            ]
        }
    },
    "concrete-weight-calculator": {
        "cn": {
            "meta": "混凝土重量计算器：根据体积和密度快速计算混凝土总重量。支持多种混凝土标号和自定义密度，适用于建筑工程、材料估算等场景。",
            "subtitle": "输入混凝土体积和密度等级，快速计算混凝土总重量。支持C20/C25/C30等常用标号和自定义密度，适用于建筑工程和材料估算。",
            "related": [
                ("体积计算器", "/volume-calculator/"),
                ("密度计算器", "/density-calculator/"),
                ("钢筋重量计算器", "/rebar-weight-calculator/"),
            ]
        },
        "en": {
            "meta": "Concrete Weight Calculator: compute total concrete weight from volume and density grade. Supports C20/C25/C30 grades and custom density. Essential for construction material estimation.",
            "subtitle": "Enter concrete volume and density grade to quickly calculate total weight. Supports C20/C25/C30 grades and custom density. Ideal for construction and material estimation.",
            "related": [
                ("Volume Calculator", "/en/volume-calculator/"),
                ("Density Calculator", "/en/density-calculator/"),
                ("Rebar Weight Calculator", "/en/rebar-weight-calculator/"),
            ]
        }
    },
    "gold-value-calculator": {
        "cn": {
            "meta": "黄金价值计算器：根据实时金价和重量计算黄金首饰、金条的价值。支持克、盎司、千克等多种单位，快速了解黄金当前市场价值。",
            "subtitle": "输入黄金重量和当前金价，快速计算黄金的总市场价值。支持克、盎司、千克等多种重量单位，适用于黄金投资和首饰估价。",
            "related": [
                ("汇率计算器", "/currency-converter/"),
                ("投资回报计算器", "/roi-calculator/"),
                ("单位换算器", "/unit-converter/"),
            ]
        },
        "en": {
            "meta": "Gold Value Calculator: compute the market value of gold jewelry and bars using live gold price. Supports grams, ounces, and kilograms. Quick and accurate gold valuation tool.",
            "subtitle": "Enter gold weight and current gold price to calculate total market value. Supports grams, ounces, kilograms and more. Ideal for gold investment and jewelry valuation.",
            "related": [
                ("Currency Converter", "/en/currency-converter/"),
                ("ROI Calculator", "/en/roi-calculator/"),
                ("Unit Converter", "/en/unit-converter/"),
            ]
        }
    },
    "bit-hourly-calculator": {
        "cn": {
            "meta": "比特币挖矿收益计算器：根据算力、电费和矿池费率估算每日挖矿收益。支持TH/s和MH/s单位，帮助矿工评估投入产出比。",
            "subtitle": "输入算力、电费单价和矿池费率，估算每日比特币挖矿收益。支持TH/s和MH/s算力单位，帮助矿工评估挖矿投入产出比。",
            "related": [
                ("加密货币计算器", "/crypto-calculator/"),
                ("电费计算器", "/electricity-cost-calculator/"),
                ("投资回报计算器", "/roi-calculator/"),
            ]
        },
        "en": {
            "meta": "Bitcoin Mining Profit Calculator: estimate daily mining profit based on hashrate, electricity cost, and pool fee. Supports TH/s and MH/s. Essential tool for crypto miners.",
            "subtitle": "Enter hashrate, electricity cost, and pool fee to estimate daily Bitcoin mining profit. Supports TH/s and MH/s. Helps miners evaluate ROI of their mining operations.",
            "related": [
                ("Crypto Calculator", "/en/crypto-calculator/"),
                ("Electricity Cost Calculator", "/en/electricity-cost-calculator/"),
                ("ROI Calculator", "/en/roi-calculator/"),
            ]
        }
    },
    "gradient-calculator": {
        "cn": {
            "meta": "坡度计算器：根据垂直高度和水平距离计算坡度百分比和角度。适用于建筑、道路施工、无障碍设计等场景，快速精准计算坡度参数。",
            "subtitle": "输入垂直高度和水平距离，计算坡度百分比和角度。适用于建筑、道路施工、无障碍坡道设计等场景，快速精准计算。",
            "related": [
                ("三角计算器", "/trigonometry-calculator/"),
                ("角度换算器", "/angle-converter/"),
                ("斜率计算器", "/slope-calculator/"),
            ]
        },
        "en": {
            "meta": "Gradient Calculator: calculate slope percentage and angle from vertical rise and horizontal run. Ideal for construction, road design, and ADA-compliant ramp calculations.",
            "subtitle": "Enter vertical rise and horizontal run to calculate slope percentage and angle. Ideal for construction, road design, and ADA-compliant ramp planning.",
            "related": [
                ("Trigonometry Calculator", "/en/trigonometry-calculator/"),
                ("Angle Converter", "/en/angle-converter/"),
                ("Slope Calculator", "/en/slope-calculator/"),
            ]
        }
    },
    "rectangular-tank-volume": {
        "cn": {
            "meta": "矩形水箱容积计算器：根据长宽高快速计算水箱容积和可储水重量。支持多种单位，适用于水箱设计、蓄水容量估算等场景。",
            "subtitle": "输入水箱的长、宽、高，快速计算矩形水箱的容积和可储水重量。支持毫米、厘米、米等多种单位，适用于水箱设计和容量估算。",
            "related": [
                ("圆柱体积计算器", "/cylinder-volume-calc/"),
                ("管道容积计算器", "/pipe-volume-calculator/"),
                ("体积计算器", "/volume-calculator/"),
            ]
        },
        "en": {
            "meta": "Rectangular Tank Volume Calculator: compute tank volume and water storage capacity from length, width, and height. Supports multiple units. Ideal for tank design and capacity planning.",
            "subtitle": "Enter tank length, width, and height to calculate rectangular tank volume and water storage capacity. Supports mm, cm, m and more. Ideal for tank design and capacity estimation.",
            "related": [
                ("Cylinder Volume Calculator", "/en/cylinder-volume-calc/"),
                ("Pipe Volume Calculator", "/en/pipe-volume-calculator/"),
                ("Volume Calculator", "/en/volume-calculator/"),
            ]
        }
    }
}

def related_html(tools_list, lang="cn"):
    title = "相关工具" if lang == "cn" else "Related Tools"
    items = "".join(f'<li><a href="{url}">{name}</a></li>' for name, url in tools_list)
    style_items = "list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:8px;"
    style_link = "color:var(--primary);text-decoration:none;font-size:.9rem;padding:6px 12px;border:1px solid var(--border);border-radius:6px;display:inline-block;"
    items_styled = "".join(f'<li><a href="{url}" style="{style_link}">{name}</a></li>' for name, url in tools_list)
    return f"""<div style="margin-top:32px;padding-top:24px;border-top:1px solid var(--border);">
<h3 style="font-size:1.1rem;margin-bottom:12px;color:var(--text);">{title}</h3>
<ul style="{style_items}">
{items_styled}
</ul>
</div>"""

count = 0
for tool_name, data in tools_data.items():
    for lang, lang_key in [("CN", "cn"), ("EN", "en")]:
        folder = tool_name if lang == "CN" else f"en/{tool_name}"
        path = os.path.join(base, folder, "index.html")
        
        if not os.path.exists(path):
            print(f"SKIP {tool_name}/{lang}: file not found")
            continue
        
        with open(path) as f:
            content = f.read()
        
        d = data[lang_key]
        modified = False
        
        # 1. meta description
        old_meta = re.search(r'<meta name="description" content="[^"]*"', content)
        if old_meta:
            new_meta = f'<meta name="description" content="{d["meta"]}"'
            content = content.replace(old_meta.group(), new_meta)
            modified = True
        
        # og:description
        old_og = re.search(r'<meta property="og:description" content="[^"]*"', content)
        if old_og:
            new_og = f'<meta property="og:description" content="{d["meta"]}"'
            content = content.replace(old_og.group(), new_og)
            modified = True
        
        # 2. subtitle
        old_sub = re.search(r'<p class="subtitle">.+?</p>', content)
        if old_sub:
            new_sub = f'<p class="subtitle">{d["subtitle"]}</p>'
            content = content.replace(old_sub.group(), new_sub)
            modified = True
        
        # 3. related tools
        if "相关工具" not in content and "Related Tools" not in content:
            related = related_html(d["related"], lang_key)
            content = content.replace("</main>", f"{related}\n</main>")
            modified = True
        
        if modified:
            with open(path, "w") as f:
                f.write(content)
            new_meta_len = len(re.search(r'<meta name="description" content="([^"]+)"', content).group(1))
            has_rel = "相关工具" in content or "Related Tools" in content
            print(f"OK {tool_name}/{lang}: meta={new_meta_len}chars related={'YES' if has_rel else 'NO'}")
            count += 1
        else:
            print(f"NOCHANGE {tool_name}/{lang}")

print(f"\nTotal files modified: {count}")
