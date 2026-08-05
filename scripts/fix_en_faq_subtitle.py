#!/usr/bin/env python3
"""Fix remaining FAQ_CN_JSON and TOOL_DESC_CN_SHORT in EN pages"""
import os

BASE = "/home/chison/tools-site/en"

# FAQ JSON for each tool (English)
faq_json = {
    "warehouse-capacity-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Calculations use standard warehouse layout formulas, results are precise and reliable."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
    "fence-cost-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Calculations are based on standard cost formulas, results are estimates for planning."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
    "postage-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Calculations use standard shipping rate formulas, results are estimates."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
    "recipe-scaler-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Calculations use precise ratio scaling, results are exact."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
    "celsius-to-kelvin": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The conversion uses the exact formula K = °C + 273.15, results are precise."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start converting."}}]',
    "fahrenheit-to-kelvin": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The conversion uses the exact formula K = (°F - 32) × 5/9 + 273.15, results are precise."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start converting."}}]',
    "kelvin-to-fahrenheit": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The conversion uses the exact formula °F = (K - 273.15) × 9/5 + 32, results are precise."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start converting."}}]',
    "hexagon-area-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The calculation uses the exact formula (3√3/2) × s², results are precise."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
    "ellipse-area-calculator": '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"The calculation uses the exact formula π × a × b, results are precise."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No download needed, just open the page and start calculating."}}]',
}

subtitles = {
    "warehouse-capacity-calculator": "Calculate warehouse pallet capacity from area and pallet size",
    "fence-cost-calculator": "Estimate fence installation cost from length and rates",
    "postage-calculator": "Calculate shipping costs by weight, distance, and method",
    "recipe-scaler-calculator": "Scale recipe ingredients up or down for any serving size",
    "celsius-to-kelvin": "Convert Celsius temperature to Kelvin",
    "fahrenheit-to-kelvin": "Convert Fahrenheit temperature to Kelvin",
    "kelvin-to-fahrenheit": "Convert Kelvin temperature to Fahrenheit",
    "hexagon-area-calculator": "Calculate regular hexagon area from side length",
    "ellipse-area-calculator": "Calculate ellipse area from semi-major and semi-minor axes",
}

fixed = 0
for tool in faq_json:
    fpath = os.path.join(BASE, tool, "index.html")
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = content.replace("FAQ_CN_JSON", faq_json[tool])
    content = content.replace("TOOL_DESC_CN_SHORT", subtitles[tool])
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {fpath}")
        fixed += 1

print(f"\nTotal: {fixed}")
