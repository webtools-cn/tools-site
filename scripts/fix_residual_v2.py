#!/usr/bin/env python3
"""修复quality_loop残留：no_related_tools + no_software_app + content_thin + title_long"""
import re, os, json

BASE = '/home/chison/tools-site'

# 需要修复的页面和问题
REMAINING = {
    'cn:basis-point-calculator': ['content_thin', 'no_related_tools'],
    'cn:breakeven-analysis-calculator': ['content_thin', 'no_related_tools'],
    'cn:customer-acquisition-cost-calculator': ['content_thin', 'no_related_tools'],
    'cn:how-much-house-can-i-afford': ['content_thin', 'no_related_tools'],
    'cn:pregnancy-week-calculator': ['content_very_thin', 'no_related_tools'],
    'en:basis-point-calculator': ['no_related_tools'],
    'en:breakeven-analysis-calculator': ['no_related_tools'],
    'en:customer-acquisition-cost-calculator': ['no_related_tools'],
    'en:early-retirement-calculator': ['no_software_app', 'title_long'],
    'en:electric-vehicle-savings-calculator': ['no_software_app', 'title_long'],
    'en:financial-independence-calculator': ['no_software_app', 'title_long'],
    'en:home-buying-calculator': ['no_software_app'],
    'en:how-much-house-can-i-afford': ['no_related_tools'],
    'en:legal-fee-calculator': ['no_software_app', 'title_long'],
    'en:pregnancy-week-calculator': ['no_related_tools'],
}

# 中文content_thin增强内容模板
CN_CONTENT_ENHANCE = {
    'basis-point-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">📊 基点计算器使用指南</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">基点（Basis Point，简称BP）是金融领域常用的计量单位，1个基点等于0.01%。在利率、收益率和利差计算中广泛使用。输入百分比数值，即可快速转换为基点；反之亦可。适用于银行利率调整、债券收益率变化、基金管理费计算等场景。</p>
</section>''',
    'breakeven-analysis-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">📈 盈亏平衡分析指南</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">盈亏平衡点是项目或业务中总收入等于总成本的关键点。输入固定成本、变动成本和销售价格，即可计算需要销售多少单位才能收回全部成本。适用于创业计划、产品定价和新项目评估。</p>
</section>''',
    'customer-acquisition-cost-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">💰 客户获取成本（CAC）解读</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">客户获取成本（CAC）是衡量获取新客户所需投入的关键指标。将营销和销售总费用除以新客户数量即可得出。合理的CAC应低于客户终身价值（LTV），理想比例约为LTV的1/3。适用于SaaS企业、电商和任何需要评估营销效率的业务。</p>
</section>''',
    'how-much-house-can-i-afford': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">🏠 购房能力评估说明</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">购房能力取决于多个因素：年收入、首付比例、贷款利率和贷款期限。通常建议住房支出不超过月收入的28%-36%。输入您的收入、首付和当前利率，即可估算可负担的房价范围。仅供参考，实际贷款额度以银行审批为准。</p>
</section>''',
    'pregnancy-week-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">🤰 孕周计算说明</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">孕周从末次月经第一天开始计算，整个孕期约40周（280天）。输入末次月经日期即可计算当前孕周和预产期。本工具仅供参考，实际孕期情况请咨询专业医生。</p>
</section>''',
}

# EN content_thin增强
EN_CONTENT_ENHANCE = {
    'basis-point-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">📊 What Are Basis Points?</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">A basis point (BP) equals 0.01% and is widely used in finance for interest rates, bond yields, and spreads. Enter a percentage to convert to basis points, or vice versa. Useful for mortgage rate changes, investment fees, and financial analysis.</p>
</section>''',
    'breakeven-analysis-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">📈 Breakeven Analysis Guide</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">The breakeven point is where total revenue equals total costs. Enter fixed costs, variable costs, and selling price to find how many units you need to sell. Ideal for business planning and pricing strategy.</p>
</section>''',
    'customer-acquisition-cost-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">💰 Understanding CAC</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">Customer Acquisition Cost (CAC) measures how much you spend to acquire a new customer. Divide total marketing and sales expenses by new customers gained. A healthy CAC should be about 1/3 of Customer Lifetime Value (LTV).</p>
</section>''',
    'how-much-house-can-i-afford': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">🏠 Home Affordability Guide</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">Your home buying power depends on income, down payment, interest rate, and loan term. Experts recommend housing costs stay below 28-36% of monthly income. Enter your details to estimate your affordable price range.</p>
</section>''',
    'pregnancy-week-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">🤰 Pregnancy Week Guide</h2>
<p style="color:#475569;font-size:.9rem;line-height:1.6">Pregnancy is calculated from the first day of your last menstrual period, lasting about 40 weeks (280 days). Enter your LMP date to find your current week and estimated due date. Always consult your doctor for medical advice.</p>
</section>''',
}

# SoftwareApplication schema模板
def make_software_app(name_en, desc_en, url):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{name_en}",
  "description": "{desc_en}",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "url": "{url}"
}}
</script>'''

# related-tools组件
RELATED_TOOLS_HTML = '''<link rel="stylesheet" href="https://free-toolbase.com/related-tools.css">
<div id="related-tools-section" class="related-tools-section"><div class="related-tools-loading">Loading related tools...</div></div>
<script src="https://free-toolbase.com/related-tools.js"></script>'''

# title修复
TITLE_FIXES = {
    'en:early-retirement-calculator': 'Early Retirement Calculator - FIRE Planning Tool | Free ToolBase',
    'en:electric-vehicle-savings-calculator': 'EV Savings Calculator - Compare Electric vs Gas | Free ToolBase',
    'en:financial-independence-calculator': 'Financial Independence Calculator - FIRE Number | Free ToolBase',
    'en:legal-fee-calculator': 'Legal Fee Calculator - Estimate Attorney Costs | Free ToolBase',
}

# SoftwareApplication信息
SW_APP_INFO = {
    'early-retirement-calculator': ('Early Retirement Calculator', 'Calculate your FIRE number and early retirement timeline with this free online tool. Plan your financial independence journey.', 'https://free-toolbase.com/en/early-retirement-calculator/'),
    'electric-vehicle-savings-calculator': ('EV Savings Calculator', 'Compare electric vehicle costs vs gas vehicles. Calculate fuel savings, maintenance savings, and total cost of ownership.', 'https://free-toolbase.com/en/electric-vehicle-savings-calculator/'),
    'financial-independence-calculator': ('Financial Independence Calculator', 'Calculate your FIRE number and financial independence target. Free retirement planning tool with investment projections.', 'https://free-toolbase.com/en/financial-independence-calculator/'),
    'home-buying-calculator': ('Home Buying Calculator', 'Estimate your total home buying costs including down payment, closing costs, and monthly mortgage payments.', 'https://free-toolbase.com/en/home-buying-calculator/'),
    'legal-fee-calculator': ('Legal Fee Calculator', 'Estimate attorney fees and legal costs for various case types. Free online legal cost estimator.', 'https://free-toolbase.com/en/legal-fee-calculator/'),
}

fixed_count = 0
errors = []

for key, issues in REMAINING.items():
    lang, tool = key.split(':', 1)
    
    if lang == 'cn':
        fpath = os.path.join(BASE, tool, 'index.html')
    else:
        fpath = os.path.join(BASE, 'en', tool, 'index.html')
    
    if not os.path.exists(fpath):
        errors.append(f"MISSING: {fpath}")
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    original = content
    page_fixes = []
    
    # 1. no_related_tools
    if 'no_related_tools' in issues:
        if 'related-tools-section' not in content and 'related-tools' not in content:
            content = content.replace('</body>', RELATED_TOOLS_HTML + '\n</body>')
            page_fixes.append('no_related_tools')
    
    # 2. content_thin / content_very_thin (CN)
    if 'content_thin' in issues or 'content_very_thin' in issues:
        enhance = CN_CONTENT_ENHANCE.get(tool)
        if enhance and enhance not in content:
            # 插入到</main>之前
            if '</main>' in content:
                content = content.replace('</main>', enhance + '\n</main>')
            elif '</body>' in content:
                content = content.replace('</body>', enhance + '\n</body>')
            page_fixes.append('content_thin')
    
    # 3. EN content_thin
    if lang == 'en' and tool in EN_CONTENT_ENHANCE:
        enhance = EN_CONTENT_ENHANCE.get(tool)
        if enhance and enhance not in content:
            if '</main>' in content:
                content = content.replace('</main>', enhance + '\n</main>')
            elif '</body>' in content:
                content = content.replace('</body>', enhance + '\n</body>')
            page_fixes.append('content_thin')
    
    # 4. no_software_app
    if 'no_software_app' in issues:
        if 'SoftwareApplication' not in content:
            info = SW_APP_INFO.get(tool)
            if info:
                sa = make_software_app(*info)
                content = content.replace('</head>', sa + '\n</head>')
                page_fixes.append('no_software_app')
    
    # 5. title_long
    if 'title_long' in issues:
        fix_key = f'en:{tool}'
        new_title = TITLE_FIXES.get(fix_key)
        if new_title:
            import re as re_m
            content = re_m.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content, count=1)
            page_fixes.append('title_long')
    
    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ {key}: {page_fixes}")
    else:
        print(f"⚠️  {key}: no changes applied (issues: {issues})")

print(f"\n总计修复: {fixed_count} 个页面")
if errors:
    print(f"错误: {errors}")