#!/usr/bin/env python3
"""批量生成英文版工具页面"""
import re, os

BASE = '/home/chison/tools-site'

tools = {
    'hdl-cholesterol-calculator': {
        'zh_title': '免费在线HDL胆固醇计算器',
        'en_title': 'Free Online HDL Cholesterol Calculator',
        'en_desc': 'Calculate HDL cholesterol from total cholesterol, LDL and triglycerides. Assess cardiovascular health risk. Pure client-side local computing, data secure.',
        'en_og_title': 'Free Online HDL Cholesterol Calculator - HDL Cholesterol Calculator | Heart Health | No Signup',
        'en_h1': '🫀 HDL Cholesterol Calculator',
        'en_hero': 'Calculate HDL cholesterol value from total cholesterol, LDL, and triglyceride levels. Assess cardiovascular health risk. Supports mg/dL and mmol/L units.',
        'en_badge': '🩺 Health Tool',
        'en_faq': [
            ('What is HDL cholesterol?', 'HDL (High-Density Lipoprotein) is the "good cholesterol" that transports excess cholesterol from artery walls back to the liver for metabolism. Higher HDL levels mean lower cardiovascular disease risk. Ideal HDL: men >40 mg/dL, women >50 mg/dL.'),
            ('What are normal HDL levels?', 'Low HDL (High Risk): men <40 mg/dL, women <50 mg/dL; Moderate: 40-59 mg/dL; Optimal (Protective): ≥60 mg/dL. HDL below 40 mg/dL is an independent risk factor for coronary heart disease.'),
            ('How can I raise HDL cholesterol?', 'Ways to increase HDL: 1) 150+ min/week aerobic exercise; 2) Quit smoking; 3) Weight loss; 4) Consume healthy fats (olive oil, fish oil, nuts); 5) Moderate red wine (1 glass/day); 6) Increase soluble fiber intake.'),
            ('What is the Friedewald formula?', 'Friedewald formula: LDL = TC - HDL - TG/5 (in mg/dL). This formula is inaccurate when triglycerides >400 mg/dL; use direct measurement or Martin-Hopkins formula instead.')
        ],
        'zh_labels': {'输入血脂数据':'Enter Lipid Data','单位制':'Unit System','mg/dL（美国标准）':'mg/dL (US Standard)','mmol/L（国际标准）':'mmol/L (International)','总胆固醇 (TC)':'Total Cholesterol (TC)','LDL胆固醇':'LDL Cholesterol','甘油三酯 (TG)':'Triglycerides (TG)','计算HDL':'Calculate HDL','清空':'Clear','复制结果':'Copy Result','计算结果':'Results','HDL参考范围':'HDL Reference Range','水平':'Level','男性':'Men','女性':'Women','理想':'Optimal','中等':'Moderate','高风险':'High Risk','常见问题':'FAQ','计算公式：':'Formula: ','注意：':'Note: ','免责声明：':'Disclaimer: ','详细血脂分析':'Detailed Lipid Analysis','指标':'Metric','数值':'Value','单位':'Unit','已清空':'Cleared','已复制到剪贴板':'Copied to clipboard','复制失败':'Copy failed','请填写所有数值':'Please fill in all values','所有工具均免费使用':'All tools are free to use','数据不上传服务器':'Data is not uploaded to any server','返回首页':'← Back to Home','健康工具':'Health Tools','已复制':'Copied'},
        'category': 'health-tools'
    },
    'kpi-calculator': {
        'zh_title': '免费在线KPI计算器',
        'en_title': 'Free Online KPI Calculator',
        'en_desc': 'Calculate KPI completion rate, achievement rate, with YoY and QoQ analysis. Support target comparison and trend forecasting. Essential business analytics tool.',
        'en_og_title': 'Free Online KPI Calculator - KPI Calculator | Performance Metrics | No Signup',
        'en_h1': '📊 KPI Calculator',
        'en_hero': 'Calculate Key Performance Indicator (KPI) completion and achievement rates. Support YoY analysis and target comparison. Quickly assess business performance.',
        'en_badge': '💼 Business Tool',
        'en_faq': [
            ('How to calculate KPI completion rate?', 'KPI Completion Rate = (Actual Value ÷ Target Value) × 100%. Example: Target sales $1M, actual $1.2M, completion rate = 120%.'),
            ('How to calculate YoY growth rate?', 'YoY Growth Rate = (Current Value - Last Year Value) ÷ Last Year Value × 100%. This reflects growth compared to the same period last year.'),
            ('What if KPI is below 100%?', 'First analyze the gap causes (market, resources, unrealistic goals), then adjust strategy. Use SWOT analysis + action plan, focusing on high-leverage improvement points.')
        ],
        'zh_labels': {'输入数据':'Enter Data','KPI名称（可选）':'KPI Name (optional)','目标值':'Target Value','实际完成值':'Actual Value','单位':'Unit','去年同期值（可选，同比分析）':'Last Year Value (optional, YoY)','计算KPI':'Calculate KPI','清空':'Clear','复制结果':'Copy Result','KPI分析结果':'KPI Analysis Results','KPI公式速查':'KPI Formula Reference','完成率':'Completion Rate','差距':'Gap','达成率':'Achievement Rate','同比增长率':'YoY Growth Rate','使用建议':'Tips','商业工具':'Business Tools','距目标差距':'Gap to Target','同比增长':'YoY Growth','超额完成！':'Overachieved! 🎉','接近目标，加把劲！':'Almost there, push harder! ⚠️','严重落后，需要重点关注！':'Severely behind, needs urgent attention! 🚨','还需完成':'Still need','才能达标':'to reach target'},
        'category': 'finance-tools'
    },
    'ai-content-idea-generator': {
        'zh_title': '免费AI内容创意生成器',
        'en_title': 'Free AI Content Idea Generator',
        'en_desc': 'Enter keywords to instantly generate 100+ content ideas covering blogs, videos, podcasts, and social media. The ultimate inspiration tool for marketers and content creators.',
        'en_og_title': 'Free AI Content Idea Generator - Content Idea Generator | Blog & Social Media | No Signup',
        'en_h1': '💡 AI Content Idea Generator',
        'en_hero': 'Enter 1-3 keywords to instantly generate 50+ content ideas. Covers blogs, videos, social media, podcasts, and more. Never run out of inspiration!',
        'en_badge': '✨ AI Tool',
        'en_faq': [
            ('How to use the content idea generator?', 'Enter 1-3 keywords (e.g., "fitness diet"), select platform type, and click generate to get 50+ content ideas. Each idea combines title templates with your keywords, perfect for blog posts, video scripts, or social media posts.'),
            ('Can I publish generated ideas directly?', 'These are creative titles and directional inspirations to help you create unique content. We recommend using them as a foundation and developing original content with your own experience and perspective.')
        ],
        'zh_labels': {'输入设置':'Input Settings','关键词（逗号分隔，最多3个）':'Keywords (comma separated, max 3)','平台类型':'Platform Type','全部平台':'All Platforms','博客文章':'Blog Posts','视频/YouTube':'Video/YouTube','社交媒体':'Social Media','播客':'Podcast','生成创意':'Generate Ideas','清空':'Clear','复制全部':'Copy All','内容创意列表':'Content Idea List'},
        'category': 'text-tools'
    },
    'web-performance-checker': {
        'zh_title': '免费在线网页性能检查器',
        'en_title': 'Free Online Web Performance Checker',
        'en_desc': 'Analyze page size, resource count, image optimization, DOM complexity and more. Get actionable optimization recommendations. Essential for web developers.',
        'en_og_title': 'Free Online Web Performance Checker - Web Performance Checker | Page Speed & Optimization | No Signup',
        'en_h1': '⚡ Web Performance Checker',
        'en_hero': 'Analyze current or any webpage performance metrics: page size, resource count, image optimization, DOM complexity. Pure frontend based on Performance API. Or paste HTML code for manual analysis.',
        'en_badge': '🛠️ Dev Tool',
        'en_faq': [
            ('What can the web performance checker do?', 'This tool analyzes key performance metrics of the current page: DOM node count, resource count and size, image optimization status, script/stylesheet statistics, and cache header checks. Pure frontend implementation based on Performance API and Resource Timing API.'),
            ('How to improve web performance?', 'Common optimization methods: 1) Compress images using WebP format; 2) Enable Gzip/Brotli compression; 3) Reduce DOM node count; 4) Combine CSS/JS files; 5) Use CDN; 6) Set appropriate cache headers; 7) Lazy load images and scripts.')
        ],
        'zh_labels': {'分析设置':'Analysis Settings','网页URL或HTML代码（留空分析当前页）':'Webpage URL or HTML code (leave blank to analyze current page)','分析性能':'Analyze Performance','分析当前页面':'Analyze Current Page','清空':'Clear','复制报告':'Copy Report','性能分析报告':'Performance Analysis Report','DOM节点数':'DOM Nodes','页面大小':'Page Size','资源总数':'Total Resources','图片数量':'Images','JS脚本':'JS Scripts','CSS样式':'CSS Styles','TTFB':'TTFB','完整加载':'Full Load','资源总大小':'Total Resource Size','优化建议':'Optimization Recommendations','开发工具':'Developer Tools','请先分析':'Please analyze first'},
        'category': 'dev-tools'
    },
    'startup-name-generator': {
        'zh_title': '免费创业公司名称生成器',
        'en_title': 'Free Startup Name Generator',
        'en_desc': 'Enter industry keywords to instantly generate 100+ creative brand names. Smart domain availability check, multiple naming styles. Find the perfect name for your startup!',
        'en_og_title': 'Free Startup Name Generator - Startup Name Generator | Brand Name Ideas | No Signup',
        'en_h1': '🚀 Startup Name Generator',
        'en_hero': 'Enter industry keywords to instantly generate 100+ creative brand names. Support multiple naming styles with domain suggestions. Find the perfect name for your startup!',
        'en_badge': '💼 Startup Tool',
        'en_faq': [
            ('How to choose a good startup name?', 'Criteria for a good name: 1) Short and memorable (2-3 syllables); 2) Easy to spell and pronounce; 3) Domain available (prefer .com); 4) Brand extensibility; 5) No trademark infringement. This tool helps you from name generation to domain checking in one step.'),
            ('How to check domain availability?', 'This tool auto-generates .com domain suggestions after name generation. You can copy and check actual availability at domain registrars (GoDaddy/Namecheap, etc.). The tool provides name ideas; actual registration must be done at a registrar.')
        ],
        'zh_labels': {'输入设置':'Input Settings','核心关键词（逗号分隔，1-3个）':'Core Keywords (comma separated, 1-3)','命名风格':'Naming Style','现代科技风':'Modern Tech','创意组合风':'Creative Combo','经典短名':'Classic Short','抽象概念风':'Abstract','混合风格':'Mixed Styles','生成名称':'Generate Names','清空':'Clear','复制全部':'Copy All','品牌名称创意':'Brand Name Ideas','域名建议':'Domain Suggestions','请到域名注册商查询实际可用性':'Please check actual availability at a domain registrar','创业工具':'Startup Tools'},
        'category': 'business-tools'
    }
}

def build_en_page(tool_name, config):
    cn_path = os.path.join(BASE, tool_name, 'index.html')
    en_path = os.path.join(BASE, 'en', tool_name, 'index.html')
    
    with open(cn_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace lang
    content = content.replace('lang="zh-CN"', 'lang="en"')
    
    # Replace titles
    content = content.replace(f'<title>{config["zh_title"]}', f'<title>{config["en_title"]}')
    
    # Replace description
    old_desc = re.search(r'<meta name="description" content="([^"]+)"', content)
    if old_desc:
        content = content.replace(old_desc.group(1), config['en_desc'])
    
    # Replace OG title
    old_og_title = re.search(r'<meta property="og:title" content="([^"]+)"', content)
    if old_og_title:
        content = content.replace(old_og_title.group(1), config['en_og_title'])
    
    # Replace OG description
    old_og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', content)
    if old_og_desc:
        content = content.replace(old_og_desc.group(1), config['en_desc'])
    
    # Replace hreflang
    content = content.replace(f'href="https://free-toolbase.com/{tool_name}/"', f'href="https://free-toolbase.com/en/{tool_name}/"')
    content = content.replace(f'href="https://free-toolbase.com/en/{tool_name}/"', f'href="https://free-toolbase.com/en/{tool_name}/"', 1)  # first one already correct
    
    # Replace h1
    old_h1 = re.search(r'<h1>[^<]+</h1>', content)
    if old_h1:
        content = content.replace(old_h1.group(0), f'<h1>{config["en_h1"]}</h1>')
    
    # Replace hero paragraph
    old_hero = re.search(r'<div class="hero">.*?<p>([^<]+)</p>', content, re.DOTALL)
    if old_hero:
        content = content.replace(old_hero.group(1), config['en_hero'])
    
    # Replace badge
    old_badge = re.search(r'<span class="badge">[^<]+</span>', content)
    if old_badge:
        content = content.replace(old_badge.group(0), f'<span class="badge">{config["en_badge"]}</span>')
    
    # Replace labels
    for zh, en in config['zh_labels'].items():
        content = content.replace(zh, en)
    
    # Replace FAQ JSON
    faq_str = build_faq_json(config['en_faq'])
    old_faq = re.search(r'"@type": "FAQPage".*?\}\]', content, re.DOTALL)
    if old_faq:
        content = content.replace(old_faq.group(0), faq_str)
    
    # Replace canonical
    content = re.sub(
        r'<link rel="canonical" href="https://free-toolbase\.com/' + tool_name + r'/"',
        f'<link rel="canonical" href="https://free-toolbase.com/en/{tool_name}/"',
        content
    )
    
    # Replace og:url
    content = re.sub(
        r'<meta property="og:url" content="https://free-toolbase\.com/' + tool_name + r'/"',
        f'<meta property="og:url" content="https://free-toolbase.com/en/{tool_name}/"',
        content
    )
    
    # Replace BreadcrumbList
    content = content.replace(f'"item": "https://free-toolbase.com/{tool_name}/"', f'"item": "https://free-toolbase.com/en/{tool_name}/"')
    content = content.replace('"name": "首页"', '"name": "Home"')
    content = content.replace('"name": "工具"', '"name": "Tools"')
    
    # Replace SoftwareApplication name
    content = re.sub(r'"name": "在线[^"]+"', f'"name": "{config["en_title"].replace("Free Online ", "")}"', content)
    
    # Replace HowTo
    content = content.replace('"name": "如何使用在线', '"name": "How to Use ')
    
    # Replace lang switch active
    content = content.replace(f'<a href="/{tool_name}/" class="active">中文</a><a href="/en/{tool_name}/">English</a>',
                              f'<a href="/{tool_name}/">中文</a><a href="/en/{tool_name}/" class="active">English</a>')
    
    # Replace nav back
    content = content.replace('← 返回首页', '← Back to Home')
    content = content.replace('href="/"', 'href="/en/"')
    
    # Footer
    content = content.replace('所有工具均免费使用 · 数据不上传服务器', 'All tools are free · Data is not uploaded')
    
    # Fix duplicate en/ path
    content = content.replace('href="/en/en/', 'href="/en/')
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✅ {tool_name} EN created')

def build_faq_json(faq_list):
    items = []
    for q, a in faq_list:
        items.append(f'''{{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a}"
      }}
    }}''')
    return f'''"@type": "FAQPage",
  "mainEntity": [
    {",".join(items)}
  ]'''

for tool_name, config in tools.items():
    build_en_page(tool_name, config)

print('Done!')