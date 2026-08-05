#!/usr/bin/env python3
"""Fix placeholder steps in 8 new tools (CN + EN)"""
import os

tools_steps = {
    "pace-converter": {
        "cn": ["输入配速值（如5.5表示5分30秒/公里）", "选择换算方向（分钟/公里→分钟/英里或反向）", "点击\"计算\"按钮查看换算结果"],
        "en": ["Enter your pace value (e.g. 5.5 means 5:30/km)", "Select conversion direction (min/km → min/mile or reverse)", "Click \"Calculate\" to see the converted pace"],
    },
    "em-to-px-converter": {
        "cn": ["输入要转换的数值（如1.5）", "选择转换方向（EM→PX、PX→EM或REM→PX）", "输入基础字号（默认16px），点击\"计算\""],
        "en": ["Enter the value to convert (e.g. 1.5)", "Select conversion mode (EM→PX, PX→EM, or REM→PX)", "Enter base font size (default 16px), click \"Calculate\""],
    },
    "oil-to-butter-converter": {
        "cn": ["输入食谱中的黄油用量（克）", "选择替代用油类型（植物油/橄榄油/椰子油）", "点击\"计算\"按钮查看所需油量"],
        "en": ["Enter the butter amount from your recipe (grams)", "Select oil type (vegetable oil / olive oil / coconut oil)", "Click \"Calculate\" to see the required oil amount"],
    },
    "aquarium-volume-calculator": {
        "cn": ["输入鱼缸的长、宽、高（厘米）", "输入玻璃厚度（毫米）", "点击\"计算\"查看实际水容积（升/加仑）"],
        "en": ["Enter aquarium length, width, and height (cm)", "Enter glass thickness (mm)", "Click \"Calculate\" to see actual water volume (L/gal)"],
    },
    "moving-box-calculator": {
        "cn": ["选择住房类型（一居室/两居室/三居室）", "输入房间数量", "点击\"计算\"查看所需纸箱数量和尺寸分配"],
        "en": ["Select housing type (studio / 1-bed / 2-bed / 3-bed)", "Enter number of rooms", "Click \"Calculate\" to see box count and size breakdown"],
    },
    "pond-volume-calculator": {
        "cn": ["选择水池形状（矩形/圆形/椭圆）", "输入水池尺寸（长/宽/深，单位米）", "点击\"计算\"查看水体体积"],
        "en": ["Select pond shape (rectangular / circular / oval)", "Enter pond dimensions (length/width/depth in meters)", "Click \"Calculate\" to see water volume"],
    },
    "curtain-length-calculator": {
        "cn": ["输入窗户高度和宽度（厘米）", "选择窗帘款式（落地/窗台/标准）", "点击\"计算\"查看所需布料尺寸"],
        "en": ["Enter window height and width (cm)", "Select curtain style (floor / sill / standard)", "Click \"Calculate\" to see required fabric size"],
    },
    "package-dimensions-calculator": {
        "cn": ["输入包裹长、宽、高（厘米）", "输入实际重量（公斤）", "点击\"计算\"查看体积重和计费重量"],
        "en": ["Enter package length, width, and height (cm)", "Enter actual weight (kg)", "Click \"Calculate\" to see dimensional and chargeable weight"],
    },
}

cn_placeholder = ['<li>输入第一个参数</li>', '<li>输入第二个参数</li>', '<li>点击"计算"按钮查看结果</li>']
en_placeholder = ['<li>Enter the first parameter</li>', '<li>Enter the second parameter</li>', '<li>Click "Calculate" to see the result</li>']

for tool, steps in tools_steps.items():
    # Fix CN
    fpath = f"{tool}/index.html"
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        for i, (old, new) in enumerate(zip(cn_placeholder, steps["cn"])):
            content = content.replace(old, f'<li>{new}</li>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED CN: {tool}")
    
    # Fix EN
    fpath = f"en/{tool}/index.html"
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        for i, (old, new) in enumerate(zip(en_placeholder, steps["en"])):
            content = content.replace(old, f'<li>{new}</li>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED EN: {tool}")

print("\nDone!")
