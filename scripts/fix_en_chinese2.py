#!/usr/bin/env python3
"""Fix remaining Chinese in EN calculator files."""
import os

TOOLS = [
    "investment-return-calculator",
    "loan-installment-calculator",
    "marketing-roi-calculator",
    "simplify-fractions",
    "sip-return-calculator",
    "net-present-value",
    "rule-72-calculator",
    "daily-calorie-burn",
]

fixed = []
for tool in TOOLS:
    path = f"en/{tool}/index.html"
    if not os.path.exists(path):
        continue
    
    with open(path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix footer links
    content = content.replace('>隐私政策<', '>Privacy<')
    content = content.replace('>关于我们<', '>About<')
    content = content.replace('>服务条款<', '>Terms<')
    content = content.replace('>联系我们<', '>Contact<')
    content = content.replace('>首页<', '>Home<')
    
    # Fix SIP calculator remaining Chinese
    content = content.replace("'最终价值: <strong>'", "'<br>Final Value: <strong>'")
    content = content.replace("'收益: <strong>'", "'<br>Gain: <strong>'")
    
    # Fix daily-calorie-burn select options (Chinese activity levels)
    content = content.replace('<option value="久坐不动">久坐不动</option>', '<option value="Sedentary">Sedentary</option>')
    content = content.replace('<option value="轻度运动(1-3天/周)">轻度运动(1-3天/周)</option>', '<option value="Light Exercise(1-3 days/week)">Light Exercise (1-3 days/week)</option>')
    content = content.replace('<option value="中度运动(3-5天/周)">中度运动(3-5天/周)</option>', '<option value="Moderate Exercise(3-5 days/week)">Moderate Exercise (3-5 days/week)</option>')
    content = content.replace('<option value="高强度运动(6-7天/周)">高强度运动(6-7天/周)</option>', '<option value="Heavy Exercise(6-7 days/week)">Heavy Exercise (6-7 days/week)</option>')
    content = content.replace('<option value="极高强度(每天2次)">极高强度(每天2次)</option>', '<option value="Athlete(2x per day)">Athlete (2x per day)</option>')
    
    # Fix NPV verdict text
    content = content.replace("'值得投资'", "'Worth investing'")
    content = content.replace("'不建议投资'", "'Not recommended'")
    
    # Fix SEO section text that might still be Chinese
    content = content.replace('是一款免费在线工具，', ' is a free online tool that ')
    content = content.replace('。支持手机和电脑，所有计算在浏览器本地完成，数据安全不上传。', '. Works on mobile and desktop. All calculations run locally in your browser, your data never leaves your device.')
    
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        fixed.append(path)

print(f"Fixed: {len(fixed)}")
for f in fixed:
    print(f"  ✅ {f}")
