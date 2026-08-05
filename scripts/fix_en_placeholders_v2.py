#!/usr/bin/env python3
"""Fix EN placeholder content for all 9 new tools"""
import os, re

BASE = "/home/chison/tools-site/en"

tools = {
    "warehouse-capacity-calculator": {
        "name": "Warehouse Capacity Calculator",
        "title": "Warehouse Capacity Calculator",
        "desc": "Calculate warehouse pallet capacity based on area, aisle space, and pallet size",
        "h1": "Warehouse Capacity Calculator",
        "seo_h2": "About Warehouse Capacity Calculator",
        "seo_p": "The Warehouse Capacity Calculator is a free online tool that calculates how many pallets fit in your warehouse based on floor area, aisle percentage, pallet dimensions, and stacking layers. Helps optimize storage layout and space utilization.",
        "steps": [
            "Enter total warehouse floor area (m²)",
            "Enter aisle space percentage (e.g. 30 for 30%)",
            "Enter pallet area (m²) and number of stacking layers, then click Calculate",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>Calculations use standard warehouse layout formulas, results are precise and reliable.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
    "fence-cost-calculator": {
        "name": "Fence Cost Calculator",
        "title": "Fence Cost Calculator",
        "desc": "Calculate fence installation cost based on length, material, and labor rates",
        "h1": "Fence Cost Calculator",
        "seo_h2": "About Fence Cost Calculator",
        "seo_p": "The Fence Cost Calculator is a free online tool that estimates fence installation costs based on length, material price per meter, and labor rate. Perfect for home improvement and construction planning.",
        "steps": [
            "Enter fence length (meters)",
            "Enter material cost per meter",
            "Enter labor cost per meter, then click Calculate",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>Calculations are based on standard cost formulas, results are estimates for planning purposes.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
    "postage-calculator": {
        "name": "Postage Calculator",
        "title": "Postage Calculator",
        "desc": "Calculate shipping costs based on weight, distance, and delivery method",
        "h1": "Postage Calculator",
        "seo_h2": "About Postage Calculator",
        "seo_p": "The Postage Calculator is a free online tool that estimates shipping costs based on package weight, distance, and delivery method (standard, express, priority). Perfect for e-commerce and personal shipping.",
        "steps": [
            "Enter package weight (kg)",
            "Enter shipping distance (km)",
            "Select delivery method (1=Standard, 2=Express, 3=Priority), then click Calculate",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>Calculations use standard shipping rate formulas, results are estimates for reference.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
    "recipe-scaler-calculator": {
        "name": "Recipe Scaler Calculator",
        "title": "Recipe Scaler Calculator",
        "desc": "Scale recipe ingredient amounts up or down for different serving sizes",
        "h1": "Recipe Scaler Calculator",
        "seo_h2": "About Recipe Scaler Calculator",
        "seo_p": "The Recipe Scaler Calculator is a free online tool that scales recipe ingredients up or down. Enter original servings, target servings, and ingredient amount to get the scaled quantity instantly.",
        "steps": [
            "Enter original recipe servings (e.g. 4)",
            "Enter target servings (e.g. 8)",
            "Enter ingredient amount (g) and name, then click Calculate",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>Calculations use precise ratio scaling, results are exact.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
    "celsius-to-kelvin": {
        "name": "Celsius to Kelvin Converter",
        "title": "Celsius to Kelvin Converter",
        "desc": "Convert temperature from Celsius to Kelvin with formula display",
        "h1": "Celsius to Kelvin Converter",
        "seo_h2": "About Celsius to Kelvin Converter",
        "seo_p": "The Celsius to Kelvin Converter is a free online tool that converts temperatures from Celsius to Kelvin. Simply enter the Celsius value to get the Kelvin equivalent with the conversion formula shown.",
        "steps": [
            "Enter temperature in Celsius (°C)",
            "The tool may also accept a second value (ignored for single conversion)",
            "Click Calculate to see the Kelvin result",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>The conversion uses the exact formula K = °C + 273.15, results are precise.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start converting.</p>',
    },
    "fahrenheit-to-kelvin": {
        "name": "Fahrenheit to Kelvin Converter",
        "title": "Fahrenheit to Kelvin Converter",
        "desc": "Convert temperature from Fahrenheit to Kelvin with formula display",
        "h1": "Fahrenheit to Kelvin Converter",
        "seo_h2": "About Fahrenheit to Kelvin Converter",
        "seo_p": "The Fahrenheit to Kelvin Converter is a free online tool that converts temperatures from Fahrenheit to Kelvin. Enter the Fahrenheit value to get the Kelvin equivalent instantly.",
        "steps": [
            "Enter temperature in Fahrenheit (°F)",
            "The tool may also accept a second value (ignored for single conversion)",
            "Click Calculate to see the Kelvin result",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>The conversion uses the exact formula K = (°F - 32) × 5/9 + 273.15, results are precise.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start converting.</p>',
    },
    "kelvin-to-fahrenheit": {
        "name": "Kelvin to Fahrenheit Converter",
        "title": "Kelvin to Fahrenheit Converter",
        "desc": "Convert temperature from Kelvin to Fahrenheit with formula display",
        "h1": "Kelvin to Fahrenheit Converter",
        "seo_h2": "About Kelvin to Fahrenheit Converter",
        "seo_p": "The Kelvin to Fahrenheit Converter is a free online tool that converts temperatures from Kelvin to Fahrenheit. Enter the Kelvin value to get the Fahrenheit equivalent instantly.",
        "steps": [
            "Enter temperature in Kelvin (K)",
            "The tool may also accept a second value (ignored for single conversion)",
            "Click Calculate to see the Fahrenheit result",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>The conversion uses the exact formula °F = (K - 273.15) × 9/5 + 32, results are precise.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start converting.</p>',
    },
    "hexagon-area-calculator": {
        "name": "Hexagon Area Calculator",
        "title": "Hexagon Area Calculator",
        "desc": "Calculate the area of a regular hexagon from its side length",
        "h1": "Hexagon Area Calculator",
        "seo_h2": "About Hexagon Area Calculator",
        "seo_p": "The Hexagon Area Calculator is a free online tool that calculates the area of a regular hexagon from its side length. Uses the formula (3√3/2) × s² for precise results.",
        "steps": [
            "Enter the side length of the hexagon (s)",
            "The tool may also accept a second value (ignored for single input)",
            "Click Calculate to see the hexagon area",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>The calculation uses the exact formula (3√3/2) × s², results are precise.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
    "ellipse-area-calculator": {
        "name": "Ellipse Area Calculator",
        "title": "Ellipse Area Calculator",
        "desc": "Calculate the area of an ellipse from its semi-major and semi-minor axes",
        "h1": "Ellipse Area Calculator",
        "seo_h2": "About Ellipse Area Calculator",
        "seo_p": "The Ellipse Area Calculator is a free online tool that calculates the area of an ellipse from its semi-major axis (a) and semi-minor axis (b). Uses the formula π × a × b for precise results.",
        "steps": [
            "Enter the semi-major axis length (a)",
            "Enter the semi-minor axis length (b)",
            "Click Calculate to see the ellipse area",
        ],
        "faq": '<h3>Is this tool accurate?</h3><p>The calculation uses the exact formula π × a × b, results are precise.</p><h3>Do I need to download anything?</h3><p>No download needed, just open the page and start calculating.</p>',
    },
}

fixed = 0
for tool, data in tools.items():
    fpath = os.path.join(BASE, tool, "index.html")
    if not os.path.exists(fpath):
        print(f"SKIP: {fpath}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace TOOL_NAME_CN everywhere
    content = content.replace("TOOL_NAME_CN", data["name"])
    
    # Replace title
    content = content.replace(
        f'<title>{data["name"]} — Free ToolBase</title>',
        f'<title>{data["title"]} - Free ToolBase</title>'
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{data["desc"]}">',
        content
    )
    
    # Replace og:title
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{data["title"]} - Free ToolBase">',
        content
    )
    
    # Replace og:description if exists
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{data["desc"]}">',
        content
    )
    
    # Fix priceCurrency CNY -> USD
    content = content.replace('"priceCurrency":"CNY"', '"priceCurrency":"USD"')
    
    # Replace h1
    content = re.sub(r'<h1>[^<]+</h1>', f'<h1>{data["h1"]}</h1>', content)
    
    # Replace SEO section
    content = content.replace(f'<h2>关于 {data["name"]}</h2>', f'<h2>{data["seo_h2"]}</h2>')
    content = content.replace("TOOL_SEO_INTRO_CN", data["seo_p"])
    content = content.replace('<h3>如何使用</h3>', '<h3>How to Use</h3>')
    
    # Replace steps
    content = content.replace("TOOL_STEP1_CN", data["steps"][0])
    content = content.replace("TOOL_STEP2_CN", data["steps"][1])
    content = content.replace("TOOL_STEP3_CN", data["steps"][2])
    
    # Replace FAQ
    content = content.replace("FAQ_PLACEHOLDER_CN", data["faq"])
    
    # Fix footer Chinese
    content = content.replace(">联系我们<", ">Contact<")
    content = content.replace(">隐私政策<", ">Privacy<")
    content = content.replace(">服务条款<", ">Terms<")
    content = content.replace(">关于我们<", ">About<")
    
    # Fix copyright Chinese
    content = content.replace(
        "All calculations run locally in your browser，数据不上传服务器",
        "All calculations run locally in your browser, no data uploaded"
    )
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {fpath}")
        fixed += 1
    else:
        print(f"NO CHANGE: {fpath}")

print(f"\nTotal fixed: {fixed}")
