#!/usr/bin/env python3
"""给5个新工具页面加AdSense、BreadcrumbList、HowTo Schema"""
import re, os

SITE = '/home/chison/tools-site'
TOOLS = ['saas-mrr-calculator', 'startup-runway-calculator', 'lead-conversion-rate-calculator', 'revenue-churn-calculator', 'viral-coefficient-calculator']

ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

BREADCRUMB_TEMPLATES_CN = {
    'saas-mrr-calculator': '首页 > SaaS MRR计算器',
    'startup-runway-calculator': '首页 > 创业跑道计算器',
    'lead-conversion-rate-calculator': '首页 > 线索转化率计算器',
    'revenue-churn-calculator': '首页 > 收入流失率计算器',
    'viral-coefficient-calculator': '首页 > 病毒系数计算器',
}
BREADCRUMB_TEMPLATES_EN = {
    'saas-mrr-calculator': 'Home > SaaS MRR Calculator',
    'startup-runway-calculator': 'Home > Startup Runway Calculator',
    'lead-conversion-rate-calculator': 'Home > Lead Conversion Rate Calculator',
    'revenue-churn-calculator': 'Home > Revenue Churn Calculator',
    'viral-coefficient-calculator': 'Home > Viral Coefficient Calculator',
}

HOWTO_CN = {
    'saas-mrr-calculator': '"@type": "HowTo", "name": "如何使用SaaS MRR计算器", "step": [{"@type": "HowToStep", "name": "输入新客户MRR", "text": "输入每月新客户带来的MRR金额"}, {"@type": "HowToStep", "name": "输入扩展MRR", "text": "输入现有客户的扩展/升级MRR"}, {"@type": "HowToStep", "name": "输入收缩和流失MRR", "text": "输入降级MRR和流失MRR"}, {"@type": "HowToStep", "name": "查看结果", "text": "系统自动计算净新增MRR、总MRR和ARR"}]',
    'startup-runway-calculator': '"@type": "HowTo", "name": "如何使用创业跑道计算器", "step": [{"@type": "HowToStep", "name": "输入现金余额", "text": "输入公司当前可用的现金余额"}, {"@type": "HowToStep", "name": "输入月消耗率", "text": "输入每月平均支出（Burn Rate）"}, {"@type": "HowToStep", "name": "输入月收入", "text": "输入每月获得的收入（如有）"}, {"@type": "HowToStep", "name": "查看跑道", "text": "系统计算净消耗和可持续运营月数"}]',
    'lead-conversion-rate-calculator': '"@type": "HowTo", "name": "如何使用线索转化率计算器", "step": [{"@type": "HowToStep", "name": "输入访问量", "text": "输入网站或广告的总访问人数"}, {"@type": "HowToStep", "name": "输入线索数", "text": "输入从中产生的线索（Leads）数量"}, {"@type": "HowToStep", "name": "输入成交客户数", "text": "输入最终成交的客户数量"}, {"@type": "HowToStep", "name": "查看转化率", "text": "系统计算各阶段转化率和总体转化率"}]',
    'revenue-churn-calculator': '"@type": "HowTo", "name": "如何使用收入流失率计算器", "step": [{"@type": "HowToStep", "name": "输入期初MRR", "text": "输入计算周期开始时的MRR"}, {"@type": "HowToStep", "name": "输入期末MRR", "text": "输入计算周期结束时的MRR"}, {"@type": "HowToStep", "name": "输入新增MRR", "text": "输入该周期内新获取的MRR金额"}, {"@type": "HowToStep", "name": "查看流失率", "text": "系统自动计算毛流失和净收入留存率"}]',
    'viral-coefficient-calculator': '"@type": "HowTo", "name": "如何使用病毒系数计算器", "step": [{"@type": "HowToStep", "name": "输入邀请发送量", "text": "输入每位用户平均发送的邀请数"}, {"@type": "HowToStep", "name": "输入转化率", "text": "输入收到邀请后注册的转化百分比"}, {"@type": "HowToStep", "name": "查看K因子", "text": "系统计算病毒系数K值并给出增长潜力评估"}]',
}
HOWTO_EN = {
    'saas-mrr-calculator': '"@type": "HowTo", "name": "How to Use the SaaS MRR Calculator", "step": [{"@type": "HowToStep", "name": "Enter New Customer MRR", "text": "Input the MRR from new customers per month"}, {"@type": "HowToStep", "name": "Enter Expansion MRR", "text": "Input MRR from existing customer upgrades"}, {"@type": "HowToStep", "name": "Enter Contraction & Churn MRR", "text": "Input downgrade and lost MRR"}, {"@type": "HowToStep", "name": "View Results", "text": "System calculates Net New MRR, Total MRR, and ARR"}]',
    'startup-runway-calculator': '"@type": "HowTo", "name": "How to Use the Startup Runway Calculator", "step": [{"@type": "HowToStep", "name": "Enter Cash Balance", "text": "Input your company current cash balance"}, {"@type": "HowToStep", "name": "Enter Monthly Burn Rate", "text": "Input average monthly spending"}, {"@type": "HowToStep", "name": "Enter Monthly Revenue", "text": "Input any monthly revenue earned"}, {"@type": "HowToStep", "name": "View Runway", "text": "System calculates net burn and operating months"}]',
    'lead-conversion-rate-calculator': '"@type": "HowTo", "name": "How to Use the Lead Conversion Rate Calculator", "step": [{"@type": "HowToStep", "name": "Enter Visitors", "text": "Input total website or ad visitors"}, {"@type": "HowToStep", "name": "Enter Leads", "text": "Input number of leads generated"}, {"@type": "HowToStep", "name": "Enter Customers", "text": "Input number of customers acquired"}, {"@type": "HowToStep", "name": "View Conversion Rates", "text": "System calculates stage-by-stage and overall conversion rates"}]',
    'revenue-churn-calculator': '"@type": "HowTo", "name": "How to Use the Revenue Churn Calculator", "step": [{"@type": "HowToStep", "name": "Enter Starting MRR", "text": "Input MRR at period start"}, {"@type": "HowToStep", "name": "Enter Ending MRR", "text": "Input MRR at period end"}, {"@type": "HowToStep", "name": "Enter New MRR Added", "text": "Input MRR from new customers during period"}, {"@type": "HowToStep", "name": "View Churn Rate", "text": "System calculates gross churn and net revenue retention"}]',
    'viral-coefficient-calculator': '"@type": "HowTo", "name": "How to Use the Viral Coefficient Calculator", "step": [{"@type": "HowToStep", "name": "Enter Invites Sent", "text": "Input average invites sent per user"}, {"@type": "HowToStep", "name": "Enter Conversion Rate", "text": "Input signup conversion percentage"}, {"@type": "HowToStep", "name": "View K-Factor", "text": "System calculates viral coefficient and growth potential"}]',
}

for tool in TOOLS:
    for lang, prefix in [('cn', ''), ('en', 'en/')]:
        path = os.path.join(SITE, prefix, tool, 'index.html')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            content = f.read()
        
        # 加AdSense (在</head>之前)
        if 'adsbygoogle' not in content:
            content = content.replace('</head>', f'  {ADSENSE}\n</head>')
        
        # 加BreadcrumbList Schema (在第一个</script>后)
        breadcrumb_name = BREADCRUMB_TEMPLATES_CN[tool] if lang == 'cn' else BREADCRUMB_TEMPLATES_EN[tool]
        home_name = '首页' if lang == 'cn' else 'Home'
        item_name = breadcrumb_name.split(' > ')[-1]
        bc = f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "{home_name}", "item": "https://free-toolbase.com/{'' if lang == 'cn' else 'en/'}" }},
      {{ "@type": "ListItem", "position": 2, "name": "{item_name}" }}
    ]
  }}
  </script>'''
        if 'BreadcrumbList' not in content:
            content = content.replace('</head>', f'{bc}\n</head>')
        
        # 替换Schema为包含HowTo的版本
        howto = HOWTO_CN[tool] if lang == 'cn' else HOWTO_EN[tool]
        old_schema = '"@type": "SoftwareApplication"'
        new_schema = f'{old_schema},\n    {howto}'
        if howto not in content:
            content = content.replace(old_schema, new_schema)
        
        with open(path, 'w') as f:
            f.write(content)
        print(f'Enhanced: {prefix}{tool}')

print('\nAll 10 pages enhanced!')
