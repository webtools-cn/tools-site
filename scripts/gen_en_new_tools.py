#!/usr/bin/env python3
"""为CN新工具创建EN版本"""
import os, re

SITE = '/home/chison/tools-site'

tools = ['ebay-fee-calculator', 'paypal-fee-calculator', 'metabolism-calculator', '1rm-calculator', 'hiking-time']

translations = {
    'ebay-fee-calculator': {
        'title': 'eBay Fee Calculator - Free ToolBase',
        'desc': 'Calculate eBay seller fees including final value fees, insertion fees and net profit. Supports different store levels and categories.',
        'og_desc': 'Calculate eBay seller fees including final value fees, insertion fees and net profit.',
        'schema_name': 'eBay Fee Calculator',
        'schema_desc': 'Calculate eBay seller fees including final value fees, insertion fees and net profit.',
        'app_cat': 'FinanceApplication',
        'h1': '🧾 eBay Fee Calculator',
        'subtitle': 'Calculate eBay seller fees, final value fees and net profit',
        'labels': {
            '💰 商品售价 ($)': '💰 Selling Price ($)',
            '📦 运费 ($)': '📦 Shipping ($)',
            '🏪 店铺等级': '🏪 Store Level',
            '无店铺': 'No Store',
            'Starter (基础)': 'Starter',
            'Basic (基本)': 'Basic',
            'Premium (高级)': 'Premium',
            'Anchor (旗舰)': 'Anchor',
            '📋 品类': '📋 Category',
            '大多数品类 (13.25%)': 'Most Categories (13.25%)',
            '图书 (14.95%)': 'Books (14.95%)',
            '电子产品 (8%)': 'Electronics (8%)',
            '服装鞋帽 (12.35%)': 'Clothing & Shoes (12.35%)',
            '珠宝手表 (15%)': 'Jewelry & Watches (15%)',
            '汽车零部件 (11.7%)': 'Auto Parts (11.7%)',
            '📉 商品成本 ($)': '📉 Item Cost ($)',
            '📊 计算费用': '📊 Calculate Fees',
            '🏷️ 成交费 (Final Value Fee)': '🏷️ Final Value Fee',
            '📋 刊登费 (Insertion Fee)': '📋 Insertion Fee',
            '💳 支付手续费': '💳 Payment Processing Fee',
            '📦 运费': '📦 Shipping',
            '📉 商品成本': '📉 Item Cost',
            '📊 总费用': '📊 Total Fees',
            '📋 复制结果': '📋 Copy Results',
            '🔄 清空重置': '🔄 Clear & Reset',
            '净利润': 'Net Profit',
            '净亏损': 'Net Loss',
            '关于eBay费用计算器': 'About eBay Fee Calculator',
            '如何使用eBay费用计算器？': 'How to use eBay Fee Calculator?',
            '这个工具收费吗？': 'Is this tool free?',
            'eBay费用计算器是免费在线工具。完全免费使用，无需注册登录，数据在浏览器本地处理，保护你的隐私安全。': 'eBay Fee Calculator is a free online tool. No registration required — all data is processed locally in your browser, protecting your privacy.',
            '输入商品售价、运费、店铺等级和品类，点击计算按钮即可查看各项费用明细和净利润。支持计算eBay Final Value Fee、刊登费和支付手续费，帮助卖家优化定价策略。': 'Enter the selling price, shipping cost, store level and category, then click calculate to see detailed fee breakdown and net profit. Supports eBay Final Value Fee, insertion fee and payment processing fee calculations to help sellers optimize pricing.',
        },
        'English': '中文',
        '/en/ebay-fee-calculator/': '/ebay-fee-calculator/',
        'breadcrumb': 'eBay Fee Calculator',
        'home': 'Home',
        'footer': '© 2026 Free ToolBase · Free Online Tools Collection',
    },
    'paypal-fee-calculator': {
        'title': 'PayPal Fee Calculator - Free ToolBase',
        'desc': 'Calculate PayPal transaction fees and net received amount. Supports domestic, international and micropayment rates across multiple currencies.',
        'og_desc': 'Calculate PayPal transaction fees and net received amount.',
        'schema_name': 'PayPal Fee Calculator',
        'schema_desc': 'Calculate PayPal transaction fees and net received amount.',
        'app_cat': 'FinanceApplication',
        'h1': '💸 PayPal Fee Calculator',
        'subtitle': 'Calculate PayPal fees and know your net received amount',
        'labels': {
            '💰 收款金额': '💰 Amount Received',
            '🌍 交易类型': '🌍 Transaction Type',
            '国内交易 (2.9% + $0.30)': 'Domestic (2.9% + $0.30)',
            '国际交易 (4.4% + 固定费)': 'International (4.4% + fixed)',
            '微支付 (<$10, 5% + $0.05)': 'Micropayment (<$10, 5% + $0.05)',
            '💱 币种': '💱 Currency',
            '美元 USD ($)': 'USD - US Dollar ($)',
            '欧元 EUR (€)': 'EUR - Euro (€)',
            '英镑 GBP (£)': 'GBP - British Pound (£)',
            '人民币 CNY (¥)': 'CNY - Chinese Yuan (¥)',
            '日元 JPY (¥)': 'JPY - Japanese Yen (¥)',
            '📌 固定手续费': '📌 Fixed Fee',
            '📊 费率 (%)': '📊 Rate (%)',
            '📊 计算手续费': '📊 Calculate Fees',
            '💸 收款金额': '💸 Gross Amount',
            '📊 手续费率': '📊 Fee Rate',
            '📌 固定费用': '📌 Fixed Fee',
            '💳 总手续费': '💳 Total Fee',
            '📈 手续费占比': '📈 Fee Percentage',
            '📋 复制结果': '📋 Copy Results',
            '🔄 清空重置': '🔄 Clear & Reset',
            '实际到账金额': 'Net Received Amount',
            '关于PayPal手续费计算器': 'About PayPal Fee Calculator',
            '如何使用PayPal手续费计算器？': 'How to use PayPal Fee Calculator?',
            '这个工具收费吗？': 'Is this tool free?',
            'PayPal手续费计算器是免费在线工具。完全免费使用，无需注册登录，数据在浏览器本地处理，保护你的隐私安全。': 'PayPal Fee Calculator is a free online tool. No registration required — all data is processed locally in your browser, protecting your privacy.',
            '输入收款金额，选择交易类型和币种，点击计算按钮即可查看PayPal扣除的手续费和实际到账金额。支持国内交易、国际交易和微支付三种费率模式，帮助卖家准确预估利润。': 'Enter the amount, select transaction type and currency, then click calculate to see PayPal fees and net received amount. Supports domestic, international and micropayment rate models to help sellers accurately estimate profits.',
        },
        'English': '中文',
        '/en/paypal-fee-calculator/': '/paypal-fee-calculator/',
        'breadcrumb': 'PayPal Fee Calculator',
        'home': 'Home',
        'footer': '© 2026 Free ToolBase · Free Online Tools Collection',
    },
    'metabolism-calculator': {
        'title': 'BMR Metabolism Calculator - Free ToolBase',
        'desc': 'Calculate your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor equation. Get calorie targets for weight loss and muscle gain.',
        'og_desc': 'Calculate your BMR and TDEE using the Mifflin-St Jeor equation.',
        'schema_name': 'BMR Metabolism Calculator',
        'schema_desc': 'Calculate BMR and TDEE using the Mifflin-St Jeor equation.',
        'app_cat': 'HealthApplication',
        'h1': '🔥 BMR Metabolism Calculator',
        'subtitle': 'Calculate daily calorie expenditure using the Mifflin-St Jeor equation',
        'labels': {
            '⚖️ 体重 (kg)': '⚖️ Weight (kg)',
            '📏 身高 (cm)': '📏 Height (cm)',
            '🎂 年龄': '🎂 Age',
            '👤 性别': '👤 Gender',
            '男性': 'Male',
            '女性': 'Female',
            '🏃 活动水平': '🏃 Activity Level',
            '久坐 (几乎不运动)': 'Sedentary (little or no exercise)',
            '轻度活动 (每周运动1-3天)': 'Lightly Active (1-3 days/week)',
            '中度活动 (每周运动3-5天)': 'Moderately Active (3-5 days/week)',
            '高度活动 (每周运动6-7天)': 'Very Active (6-7 days/week)',
            '极高强度 (体力劳动者/专业运动员)': 'Extremely Active (physical job/athlete)',
            '📊 计算代谢率': '📊 Calculate Metabolism',
            '🏃 TDEE (每日总消耗)': '🏃 TDEE (Daily Total)',
            '📉 减肥热量 (减0.5kg/周)': '📉 Weight Loss (-0.5kg/wk)',
            '📈 增肌热量 (增0.25kg/周)': '📈 Muscle Gain (+0.25kg/wk)',
            '⚖️ 维持体重热量': '⚖️ Maintenance Calories',
            '📋 复制结果': '📋 Copy Results',
            '🔄 清空重置': '🔄 Clear & Reset',
            '基础代谢率 (BMR) kcal/天': 'Basal Metabolic Rate (BMR) kcal/day',
            '关于基础代谢率计算器': 'About BMR Metabolism Calculator',
            '如何使用基础代谢率计算器？': 'How to use the BMR Calculator?',
            '什么是BMR和TDEE？': 'What are BMR and TDEE?',
            '输入你的体重、身高、年龄和性别，选择日常活动水平，点击计算按钮即可获得BMR基础代谢率和TDEE每日总热量消耗。使用Mifflin-St Jeor公式（最准确的BMR计算公式），同时提供减肥和增肌的热量建议。': 'Enter your weight, height, age and gender, select your activity level, then click calculate to get your BMR and TDEE. Uses the Mifflin-St Jeor equation (the most accurate BMR formula), with calorie targets for weight loss and muscle gain.',
            'BMR（基础代谢率）是身体在完全休息状态下消耗的热量。TDEE（每日总消耗）是BMR乘以活动系数后的总热量。要达到减肥目标，摄入热量应低于TDEE 500 kcal/天；增肌则需要高于TDEE 250-300 kcal/天。': 'BMR (Basal Metabolic Rate) is the calories your body burns at complete rest. TDEE (Total Daily Energy Expenditure) is BMR multiplied by your activity factor. To lose weight, eat 500 kcal below TDEE; to gain muscle, eat 250-300 kcal above TDEE.',
        },
        'English': '中文',
        '/en/metabolism-calculator/': '/metabolism-calculator/',
        'breadcrumb': 'BMR Metabolism Calculator',
        'home': 'Home',
        'footer': '© 2026 Free ToolBase · Free Online Tools Collection',
    },
    '1rm-calculator': {
        'title': 'One Rep Max (1RM) Calculator - Free ToolBase',
        'desc': 'Calculate your one rep max for squat, bench press, deadlift and more. Uses Epley, Brzycki, Lombardi and O\'Conner formulas with training weight percentages.',
        'og_desc': 'Calculate your one rep max using Epley, Brzycki and other formulas.',
        'schema_name': 'One Rep Max Calculator',
        'schema_desc': 'Calculate your one rep max for squat, bench press, deadlift using multiple formulas.',
        'app_cat': 'HealthApplication',
        'h1': '🏋️ One Rep Max (1RM) Calculator',
        'subtitle': 'Estimate your max weight for squat, bench, deadlift using the Epley formula',
        'labels': {
            '🏋️ 训练动作': '🏋️ Exercise',
            '深蹲 (Squat)': 'Squat',
            '卧推 (Bench Press)': 'Bench Press',
            '硬拉 (Deadlift)': 'Deadlift',
            '实力举 (Overhead Press)': 'Overhead Press',
            '杠铃划船 (Barbell Row)': 'Barbell Row',
            '⚖️ 使用重量 (kg)': '⚖️ Weight Used (kg)',
            '🔢 重复次数': '🔢 Repetitions',
            '📐 计算公式': '📐 Formula',
            'Epley (最常用)': 'Epley (Most Common)',
            'Brzycki': 'Brzycki',
            'Lombardi': 'Lombardi',
            "O'Conner": "O'Conner",
            '📊 计算1RM': '📊 Calculate 1RM',
            '⚖️ 使用重量': '⚖️ Weight Used',
            '🔢 完成次数': '🔢 Reps Completed',
            '%1RM': '%1RM',
            '重量 (kg)': 'Weight (kg)',
            '建议次数': 'Reps',
            '热身': 'Warmup',
            '📋 复制结果': '📋 Copy Results',
            '🔄 清空重置': '🔄 Clear & Reset',
            '估算1RM最大重量': 'Estimated 1RM Max',
            '关于1RM最大重量计算器': 'About 1RM Calculator',
            '如何使用1RM计算器？': 'How to use the 1RM Calculator?',
            '1RM计算准确吗？': 'Is 1RM calculation accurate?',
            '选择训练动作，输入你使用的重量和能完成的次数，点击计算按钮即可估算1RM最大重量。支持Epley、Brzycki、Lombardi和O\'Conner四种公式，同时提供不同百分比的训练重量建议，帮助科学规划力量训练。': 'Select the exercise, enter the weight used and reps completed, then click calculate to estimate your 1RM. Supports Epley, Brzycki, Lombardi and O\'Conner formulas, with percentage-based training weight recommendations for scientific strength programming.',
            '1RM计算公式提供估算值，对于5次以下的重复最为准确。Epley公式是健身界最常用的估算方法。安全起见，建议在有人保护的情况下进行1RM测试。': '1RM formulas provide estimates and are most accurate for 5 reps or fewer. The Epley formula is the most widely used in fitness. For safety, always test 1RM with a spotter.',
        },
        'English': '中文',
        '/en/1rm-calculator/': '/1rm-calculator/',
        'breadcrumb': '1RM Calculator',
        'home': 'Home',
        'footer': '© 2026 Free ToolBase · Free Online Tools Collection',
    },
    'hiking-time': {
        'title': 'Hiking Time Calculator - Free ToolBase',
        'desc': 'Estimate hiking duration and calorie burn based on distance, elevation gain and difficulty. Uses Naismith\'s Rule with pack weight adjustment.',
        'og_desc': 'Estimate hiking duration and calorie burn based on distance and elevation.',
        'schema_name': 'Hiking Time Calculator',
        'schema_desc': 'Estimate hiking duration and calorie burn based on distance, elevation gain and difficulty.',
        'app_cat': 'HealthApplication',
        'h1': '🥾 Hiking Time Calculator',
        'subtitle': 'Estimate hiking duration and calories based on distance and elevation',
        'labels': {
            '📏 徒步距离': '📏 Distance',
            '📐 距离单位': '📐 Unit',
            '公里 (km)': 'Kilometers (km)',
            '英里 (mi)': 'Miles (mi)',
            '⛰️ 总海拔爬升 (米)': '⛰️ Elevation Gain (m)',
            '🏔️ 难度等级': '🏔️ Difficulty',
            '轻松 (平坦步道)': 'Easy (flat trail)',
            '中等 (缓坡)': 'Moderate (gentle slopes)',
            '困难 (陡坡/碎石路)': 'Hard (steep/rocky)',
            '专家 (攀爬/技术路段)': 'Expert (climbing/technical)',
            '⚖️ 体重 (kg)': '⚖️ Body Weight (kg)',
            '🎒 背包重量 (kg)': '🎒 Pack Weight (kg)',
            '📊 计算徒步时间': '📊 Calculate Hiking Time',
            '📏 徒步距离': '📏 Distance',
            '⛰️ 海拔爬升': '⛰️ Elevation Gain',
            '🏃 步行时间': '🏃 Walking Time',
            '⛰️ 爬升附加时间': '⛰️ Climb Time',
            '⏸️ 休息时间': '⏸️ Rest Time',
            '🔥 预估消耗热量': '🔥 Estimated Calories',
            '📋 复制结果': '📋 Copy Results',
            '🔄 清空重置': '🔄 Clear & Reset',
            '预计总耗时': 'Estimated Total Time',
            '关于徒步时间计算器': 'About Hiking Time Calculator',
            '如何使用徒步时间计算器？': 'How to use the Hiking Time Calculator?',
            '什么是Naismith法则？': 'What is Naismith\'s Rule?',
            '输入徒步距离、海拔爬升、难度等级和个人体重，点击计算按钮即可获得预估耗时和热量消耗。基于Naismith法则（每公里12分钟+每100米爬升10分钟），综合考虑背包重量和难度系数，帮助你合理规划户外行程。': 'Enter distance, elevation gain, difficulty level and body weight, then click calculate to get estimated time and calorie burn. Based on Naismith\'s Rule (12 min/km + 10 min per 100m climb), with pack weight and difficulty adjustments to help plan your outdoor trips.',
            'Naismith法则是苏格兰登山家William Naismith在1892年提出的徒步时间估算法则：成年人每小时可走5公里平路，每爬升600米需额外1小时。本计算器采用改良版，考虑背包重量和路径难度。': 'Naismith\'s Rule was proposed by Scottish mountaineer William Naismith in 1892: an adult walks 5 km/h on flat ground, with an extra hour for every 600m of ascent. This calculator uses an improved version, accounting for pack weight and trail difficulty.',
        },
        'English': '中文',
        '/en/hiking-time/': '/hiking-time/',
        'breadcrumb': 'Hiking Time Calculator',
        'home': 'Home',
        'footer': '© 2026 Free ToolBase · Free Online Tools Collection',
    },
}

for tool in tools:
    cn_path = os.path.join(SITE, tool, 'index.html')
    en_dir = os.path.join(SITE, 'en', tool)
    os.makedirs(en_dir, exist_ok=True)
    en_path = os.path.join(en_dir, 'index.html')
    
    with open(cn_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    t = translations[tool]
    
    # 1. 替换标题
    content = content.replace(f'<title>{tool} - Free ToolBase'.replace('-', ' ').title(), f'<title>{t["title"]}')
    content = re.sub(r'<title>.*? - Free ToolBase</title>', f'<title>{t["title"]}</title>', content)
    
    # 2. 替换描述
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', content)
    
    # 3. 替换OG
    content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t["title"]}">', content)
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{t["og_desc"]}">', content)
    
    # 4. 替换Schema
    content = re.sub(r'"name":"[^"]*"', f'"name":"{t["schema_name"]}"', content, count=1)
    
    # 5. 替换h1
    content = re.sub(r'<h1>[^<]*</h1>', f'<h1>{t["h1"]}</h1>', content)
    
    # 6. 替换subtitle
    content = re.sub(r'<p class="subtitle">[^<]*</p>', f'<p class="subtitle">{t["subtitle"]}</p>', content)
    
    # 7. 替换canonical
    content = re.sub(r'href="https://free-toolbase\.com/[^/]+/', f'href="https://free-toolbase.com/en/{tool}/', content, count=1)
    
    # 8. 替换hreflang
    content = re.sub(r'hreflang="zh" href="https://free-toolbase\.com/[^"]*"', f'hreflang="zh" href="https://free-toolbase.com/{tool}/"', content)
    content = re.sub(r'hreflang="en" href="https://free-toolbase\.com/en/[^"]*"', f'hreflang="en" href="https://free-toolbase.com/en/{tool}/"', content)
    content = re.sub(r'hreflang="x-default" href="https://free-toolbase\.com/[^"]*"', f'hreflang="x-default" href="https://free-toolbase.com/{tool}/"', content)
    
    # 9. 替换lang属性
    content = content.replace('lang="zh-CN"', 'lang="en"')
    
    # 10. 替换header链接
    content = content.replace(f'href="/en/{tool}/"', f'href="/{tool}/"')
    
    # 11. 替换文本标签
    for cn_text, en_text in t['labels'].items():
        content = content.replace(cn_text, en_text)
    
    # 12. 替换breadcrumb
    content = re.sub(r'"name":"[^"]*","item"', f'"name":"{t["breadcrumb"]}","item"', content)
    content = content.replace('"name":"首页"', f'"name":"{t["home"]}"', 1)
    
    # 13. 替换footer
    content = re.sub(r'© 2026 Free ToolBase · 免费在线工具集合', t['footer'], content)
    
    # 14. 替换BreadcrumbList中的首页
    content = content.replace('"name":"首页"', f'"name":"{t["home"]}"', 1)
    
    # 15. 替换alert中的中文
    content = re.sub(r"alert\('[^']*'\)", "alert('Please enter valid data')", content, count=1)
    content = re.sub(r"alert\('[^']*'\)", "alert('1 rep is your 1RM!')", content)
    content = re.sub(r"alert\('[^']*'\)", "alert('Please fill in all fields')", content)
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {tool}/en")

print(f"\n完成 {len(tools)} 个EN版本")