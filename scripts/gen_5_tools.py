#!/usr/bin/env python3
"""批量生成5个高CPM工具：CN+EN版"""
import os, json

SITE = '/home/chison/tools-site'

TOOLS = [
    {
        "slug": "interest-rate-calculator",
        "cn_name": "利率换算计算器",
        "en_name": "Interest Rate Converter",
        "cn_desc": "免费在线利率换算计算器，支持年利率、月利率、日利率互相转换。自动计算有效年利率，适用于贷款对比、投资收益分析。纯前端计算，数据不上传服务器。",
        "en_desc": "Free online interest rate converter. Convert between annual, monthly, and daily rates. Automatically calculates effective annual rate for loan comparison and investment analysis. All calculations are done locally in your browser.",
        "cn_keywords": "利率换算,年利率,月利率,日利率,有效年利率,APR,利率转换器",
        "en_keywords": "interest rate converter, APR, effective annual rate, rate conversion, annual rate, monthly rate",
        "cn_h1": "📊 利率换算计算器",
        "en_h1": "📊 Interest Rate Converter",
        "cn_intro": "输入任意一种利率，自动换算出年利率、月利率、日利率及有效年利率。支持复利频率选择。",
        "en_intro": "Enter any rate and automatically convert between annual, monthly, daily rates and effective annual rate. Supports compounding frequency selection.",
        "cn_faqs": [
            ("什么是有效年利率？", "有效年利率(EAR)考虑了复利效应。例如月利率1%对应的有效年利率约为12.68%，而非简单的12%。"),
            ("年利率和月利率如何换算？", "月利率 = (1+年利率)^(1/12)-1。例如年利率12%对应月利率约0.95%。反之年利率 = (1+月利率)^12-1。"),
            ("为什么有效年利率比名义利率高？", "因为复利效应。每月结算利息后，下月的利息基于更大的本金计算，所以实际年化成本更高。"),
            ("日利率怎么算？", "日利率 = 年利率 ÷ 365（或360，取决于金融机构）。精确日利率 = (1+年利率)^(1/365)-1。"),
        ],
        "en_faqs": [
            ("What is Effective Annual Rate?", "Effective Annual Rate (EAR) accounts for compounding. For example, a 1% monthly rate translates to ~12.68% EAR, not simply 12%."),
            ("How to convert annual to monthly rate?", "Monthly rate = (1 + annual rate)^(1/12) - 1. For example, 12% annual ≈ 0.95% monthly. Reverse: annual = (1 + monthly)^12 - 1."),
            ("Why is EAR higher than nominal rate?", "Due to compounding. Interest earned each period adds to the principal, so the next period's interest is calculated on a larger base."),
            ("How to calculate daily rate?", "Daily rate = annual rate ÷ 365 (or 360 for some institutions). Exact: (1 + annual)^(1/365) - 1."),
        ],
    },
    {
        "slug": "dca-calculator",
        "cn_name": "定投收益计算器",
        "en_name": "DCA Investment Calculator",
        "cn_desc": "免费在线定投收益计算器，模拟定期定额投资策略。可视化展示定投vs一次性投入的收益对比，支持多种资产类别。纯前端计算，数据安全不上传。",
        "en_desc": "Free online Dollar Cost Averaging calculator. Simulate regular investment strategies and compare DCA vs lump sum returns. Supports multiple asset classes. All calculations run locally in your browser.",
        "cn_keywords": "定投计算器,DCA,定期定额,基金定投,投资规划,复利,成本平均",
        "en_keywords": "DCA calculator, dollar cost averaging, regular investment, ETF investing, compound interest, investment planning",
        "cn_h1": "💰 定投收益计算器",
        "en_h1": "💰 DCA Investment Calculator",
        "cn_intro": "模拟定期定额投资策略，对比定投与一次性投入的收益差异。输入投资金额、频率和预期年化收益率。",
        "en_intro": "Simulate dollar-cost averaging strategy and compare DCA vs lump sum returns. Enter investment amount, frequency, and expected annual return.",
        "cn_faqs": [
            ("什么是定投(DCA)？", "定投是定期投入固定金额的投资策略。无论市场涨跌都坚持买入，长期可以平摊成本，降低择时风险。"),
            ("定投和一次性投入哪个更好？", "各有优劣。牛市时一次性投入收益更高，熊市时定投可以摊低成本。历史数据表明定投在震荡市中表现更稳健。"),
            ("定投频率怎么选？", "月定投最常见。更频繁的定投（如周投）摊平效果更好，但差别通常不大。关键是坚持长期投资。"),
            ("预期收益率设多少合适？", "股票型基金长期年化约8-12%，债券型约4-6%，货币基金约2-3%。建议保守估计。"),
        ],
        "en_faqs": [
            ("What is DCA?", "DCA (Dollar Cost Averaging) means investing a fixed amount regularly regardless of market conditions. It smooths out purchase prices and reduces timing risk over the long term."),
            ("DCA vs lump sum: which is better?", "Lump sum tends to outperform in bull markets; DCA reduces risk in volatile/bear markets. DCA is generally more robust for most investors."),
            ("What DCA frequency should I choose?", "Monthly is most common. More frequent DCA (weekly) provides slightly better averaging but the difference is usually marginal. Consistency matters most."),
            ("What expected return should I use?", "Stock funds: ~8-12% long-term; bonds: ~4-6%; money market: ~2-3%. Be conservative in your estimates."),
        ],
    },
    {
        "slug": "fuel-economy-calculator",
        "cn_name": "油耗计算器",
        "en_name": "Fuel Economy Calculator",
        "cn_desc": "免费在线油耗计算器，计算百公里油耗、每公里油费、年燃油成本。支持多种单位（L/100km、MPG、km/L），对比不同车型的燃油经济性。",
        "en_desc": "Free online fuel economy calculator. Calculate fuel consumption per 100km, cost per km, and annual fuel cost. Supports multiple units (L/100km, MPG, km/L). Compare fuel efficiency across vehicles.",
        "cn_keywords": "油耗计算器,百公里油耗,油费计算,MPG转换,燃油经济性,汽车油耗",
        "en_keywords": "fuel economy calculator, MPG converter, fuel cost calculator, gas mileage, fuel efficiency, L/100km",
        "cn_h1": "⛽ 油耗计算器",
        "en_h1": "⛽ Fuel Economy Calculator",
        "cn_intro": "输入行驶距离、油耗和油价，计算每公里费用、百公里油耗和年度燃油成本。支持多单位切换。",
        "en_intro": "Enter distance, fuel consumption, and fuel price to calculate cost per km, L/100km, and annual fuel cost. Multi-unit support.",
        "cn_faqs": [
            ("百公里油耗怎么算？", "百公里油耗 = (加油量 ÷ 行驶里程) × 100。例如加50升油跑了600公里，百公里油耗约8.33升。"),
            ("MPG和L/100km怎么换算？", "MPG（英里每加仑）≈ 235.215 ÷ L/100km。例如8L/100km ≈ 29.4 MPG。"),
            ("如何降低油耗？", "保持匀速行驶、定期保养、胎压正常、减少怠速、清理车内重物都可以有效降低油耗。"),
            ("年燃油成本怎么估算？", "年燃油成本 = 百公里油耗 × 年行驶里程 ÷ 100 × 油价。以年行驶15000公里、油耗8L/100km、油价7元/L计算，年成本约8400元。"),
        ],
        "en_faqs": [
            ("How to calculate fuel consumption?", "Fuel consumption = (fuel used ÷ distance) × 100. E.g., 50L for 600km = 8.33 L/100km."),
            ("How to convert MPG to L/100km?", "MPG ≈ 235.215 ÷ L/100km. E.g., 8 L/100km ≈ 29.4 MPG."),
            ("How to reduce fuel consumption?", "Maintain steady speed, regular maintenance, proper tire pressure, reduce idling, and remove unnecessary weight."),
            ("How to estimate annual fuel cost?", "Annual cost = L/100km × annual km ÷ 100 × fuel price. E.g., 15,000 km/year, 8 L/100km, $1/L = $1,200/year."),
        ],
    },
    {
        "slug": "tdde-calculator",
        "cn_name": "每日能量消耗计算器",
        "en_name": "TDEE Calculator",
        "cn_desc": "免费在线TDEE计算器，计算每日总能量消耗。基于Mifflin-St Jeor公式，结合活动水平，精确估算维持、减重、增重所需热量。健身减脂必备工具。",
        "en_desc": "Free online TDEE (Total Daily Energy Expenditure) calculator. Based on Mifflin-St Jeor equation with activity level adjustment. Accurately estimates calories for maintenance, weight loss, and muscle gain. Essential fitness tool.",
        "cn_keywords": "TDEE计算器,每日能量消耗,热量计算,减脂,增肌,基础代谢,BMR,健身",
        "en_keywords": "TDEE calculator, total daily energy expenditure, calorie calculator, BMR, weight loss, muscle gain, fitness",
        "cn_h1": "🔥 每日能量消耗计算器",
        "en_h1": "🔥 TDEE Calculator",
        "cn_intro": "输入身高、体重、年龄和活动水平，计算每日总能量消耗(TDEE)及减重/增重所需热量。",
        "en_intro": "Enter height, weight, age, and activity level to calculate your Total Daily Energy Expenditure (TDEE) and calorie targets for weight goals.",
        "cn_faqs": [
            ("什么是TDEE？", "TDEE（每日总能量消耗）是你一天消耗的总热量，包括基础代谢(BMR)、食物热效应和运动消耗。了解TDEE是体重管理的基础。"),
            ("TDEE和BMR有什么区别？", "BMR是维持生命所需的最基础热量（躺着不动也消耗的），TDEE = BMR × 活动系数。例如BMR=1600、活动系数1.55，则TDEE=2480大卡。"),
            ("减重需要多少热量缺口？", "减重1公斤需要约7700大卡热量缺口。建议每天300-500大卡缺口，每周减0.3-0.5公斤，健康且可持续。"),
            ("活动水平怎么选？", "久坐（几乎不运动）×1.2、轻度活动（1-3天/周）×1.375、中度活动（3-5天/周）×1.55、高度活跃（6-7天/周）×1.725、极度活跃（运动员）×1.9。"),
        ],
        "en_faqs": [
            ("What is TDEE?", "TDEE (Total Daily Energy Expenditure) is the total calories you burn per day, including BMR, thermic effect of food, and physical activity. It's the foundation of weight management."),
            ("TDEE vs BMR: what's the difference?", "BMR is the minimum calories to sustain life at rest. TDEE = BMR × activity factor. E.g., BMR=1600, activity 1.55 → TDEE=2480 kcal."),
            ("How large a calorie deficit for weight loss?", "~7,700 kcal deficit = 1 kg fat loss. A 300-500 kcal daily deficit is recommended for healthy, sustainable weight loss of 0.3-0.5 kg/week."),
            ("How to choose activity level?", "Sedentary (little/no exercise) ×1.2, Light (1-3 days/week) ×1.375, Moderate (3-5 days/week) ×1.55, Very active (6-7 days/week) ×1.725, Extra active (athlete) ×1.9."),
        ],
    },
    {
        "slug": "rental-property-calculator",
        "cn_name": "出租房产收益计算器",
        "en_name": "Rental Property ROI Calculator",
        "cn_desc": "免费在线出租房产投资回报计算器。计算年租金收益率、现金流、投资回报率(ROI)，考虑房贷、税费、维修等成本。房产投资者必备工具。",
        "en_desc": "Free online rental property ROI calculator. Calculate annual rental yield, cash flow, and return on investment considering mortgage, taxes, and maintenance costs. Essential tool for real estate investors.",
        "cn_keywords": "出租房产计算器,租金收益率,房产投资,ROI,现金流,房贷计算,出租回报率",
        "en_keywords": "rental property calculator, rental yield, real estate ROI, cash flow, cap rate, property investment, landlord",
        "cn_h1": "🏠 出租房产收益计算器",
        "en_h1": "🏠 Rental Property ROI Calculator",
        "cn_intro": "输入房价、首付、租金和各项费用，计算年租金收益率、月现金流和投资回报率。",
        "en_intro": "Enter property price, down payment, rent, and expenses to calculate annual rental yield, monthly cash flow, and ROI.",
        "cn_faqs": [
            ("什么是租金收益率？", "租金收益率 = 年租金收入 ÷ 房产总价 × 100%。例如房价200万、年租金8万，收益率为4%。一线城市通常在1.5-3%之间。"),
            ("出租房产要考虑哪些成本？", "房贷月供、物业费、维修基金（约年租金5-10%）、空置期损失（约1个月租金/年）、房产税、保险费、中介费等。"),
            ("什么样的租金收益率算好？", "国内一线城市3%以上算不错，二线城市4-6%较常见。但也要考虑房价升值潜力，综合回报才是关键。"),
            ("如何提高出租回报率？", "选择交通便利地段、精装修提高租金、分租增加总收益、长期持有摊低交易成本、利用公积金降低贷款成本。"),
        ],
        "en_faqs": [
            ("What is rental yield?", "Rental yield = annual rent ÷ property price × 100%. E.g., $300K property, $18K annual rent = 6% yield. Most markets target 5-8%."),
            ("What costs should I consider?", "Mortgage payments, property taxes, insurance, maintenance (~1% of property value/year), vacancy loss (~1 month/year), HOA fees, and property management fees."),
            ("What's a good rental yield?", "5-8% is considered good in most markets. The 1% rule: monthly rent should be ~1% of property price. Also consider appreciation potential."),
            ("How to improve rental ROI?", "Choose high-demand locations, renovate to increase rent, consider multi-unit properties, long-term hold to reduce transaction costs, and optimize financing."),
        ],
    },
]

def gen_tool(t):
    slug = t['slug']
    cn_dir = os.path.join(SITE, slug)
    en_dir = os.path.join(SITE, 'en', slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    cn_url = f'https://free-toolbase.com/{slug}/'
    en_url = f'https://free-toolbase.com/en/{slug}/'
    
    # 中文版
    cn_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['cn_desc']}">
<meta name="keywords" content="{t['cn_keywords']}">
<title>{t['cn_name']} - Free ToolBase</title>
<link rel="canonical" href="{cn_url}">
<meta property="og:title" content="{t['cn_name']} - Free ToolBase">
<meta property="og:description" content="{t['cn_desc']}">
<meta property="og:url" content="{cn_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<link rel="alternate" hreflang="zh" href="{cn_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{t['cn_name']}","description":"{t['cn_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in t['cn_faqs'])}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{t['cn_name']}","description":"如何使用{t['cn_name']}的详细步骤指南","totalTime":"PT1M","tool":{{"@type":"HowToTool","name":"{t['cn_name']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入数据","text":"在输入框中输入需要计算的数值"}},{{"@type":"HowToStep","position":2,"name":"选择选项","text":"根据需要选择计算模式或参数"}},{{"@type":"HowToStep","position":3,"name":"点击计算","text":"点击计算按钮获取结果"}},{{"@type":"HowToStep","position":4,"name":"查看结果","text":"查看计算结果，支持一键复制"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['cn_name']}","item":"{cn_url}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4)}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-grid{{display:grid;grid-template-columns:1fr;gap:12px}}
.result-item{{background:#0a0f1e;border-radius:8px;padding:14px}}
.result-item .label{{color:#94a3b8;font-size:.8rem}}
.result-item .value{{font-size:1.3rem;font-weight:700;color:#22d3ee;margin-top:4px}}
.result-item .value.highlight{{color:#fbbf24;font-size:1.8rem}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-item h3{{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}}
.faq-item p{{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}}
.footer{{text-align:center;color:#64748b;font-size:.85rem;margin-top:32px;padding-top:20px;border-top:1px solid rgba(148,163,184,.08)}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}.header h1{{font-size:1.2rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{t['cn_h1']}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="/">首页</a> &rsaquo; <a href="/#tools">工具</a> &rsaquo; {t['cn_name']}</p>
<div class="section">
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{t['cn_intro']}</p>
<div id="inputs"></div>
<div class="btn-group">
<button class="btn btn-primary" onclick="calculate()">计算</button>
<button class="btn btn-secondary" onclick="clearAll()">清空</button>
</div>
</div>
<div class="section" id="results" style="display:none">
<h2>计算结果</h2>
<div class="result-grid" id="resultGrid"></div>
<div class="btn-group">
<button class="btn btn-secondary" onclick="copyResults()">📋 复制结果</button>
</div>
</div>
<div class="section">
<h2>常见问题</h2>
{''.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in t['cn_faqs'])}
</div>
<div class="footer">&copy; 2026 Free ToolBase · 免费在线工具 · 无需注册 · 数据不上传服务器</div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
function copyResults(){{var r=document.getElementById('resultGrid').innerText;navigator.clipboard.writeText(r).then(function(){{showToast('已复制到剪贴板')}}).catch(function(){{showToast('复制失败，请手动选择')}})}}
function clearAll(){{document.querySelectorAll('input').forEach(function(el){{el.value=''}});document.getElementById('results').style.display='none'}}
</script>
</body>
</html>'''
    
    with open(os.path.join(cn_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    # 英文版
    en_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['en_desc']}">
<meta name="keywords" content="{t['en_keywords']}">
<title>{t['en_name']} - Free ToolBase</title>
<link rel="canonical" href="{en_url}">
<meta property="og:title" content="{t['en_name']} - Free ToolBase">
<meta property="og:description" content="{t['en_desc']}">
<meta property="og:url" content="{en_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="zh" href="{cn_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{t['en_name']}","description":"{t['en_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in t['en_faqs'])}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"How to use {t['en_name']}","description":"Step-by-step guide on how to use {t['en_name']}","totalTime":"PT1M","tool":{{"@type":"HowToTool","name":"{t['en_name']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"Enter data","text":"Enter the values you want to calculate"}},{{"@type":"HowToStep","position":2,"name":"Select options","text":"Choose calculation mode or parameters as needed"}},{{"@type":"HowToStep","position":3,"name":"Click Calculate","text":"Click the calculate button to get results"}},{{"@type":"HowToStep","position":4,"name":"View results","text":"View the calculation results with one-click copy support"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['en_name']}","item":"{en_url}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4)}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-grid{{display:grid;grid-template-columns:1fr;gap:12px}}
.result-item{{background:#0a0f1e;border-radius:8px;padding:14px}}
.result-item .label{{color:#94a3b8;font-size:.8rem}}
.result-item .value{{font-size:1.3rem;font-weight:700;color:#22d3ee;margin-top:4px}}
.result-item .value.highlight{{color:#fbbf24;font-size:1.8rem}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-item h3{{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}}
.faq-item p{{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}}
.footer{{text-align:center;color:#64748b;font-size:.85rem;margin-top:32px;padding-top:20px;border-top:1px solid rgba(148,163,184,.08)}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}.header h1{{font-size:1.2rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{t['en_h1']}</h1><div class="lang-switch"><a href="/{slug}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="/en/">Home</a> &rsaquo; <a href="/en/#tools">Tools</a> &rsaquo; {t['en_name']}</p>
<div class="section">
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{t['en_intro']}</p>
<div id="inputs"></div>
<div class="btn-group">
<button class="btn btn-primary" onclick="calculate()">Calculate</button>
<button class="btn btn-secondary" onclick="clearAll()">Clear</button>
</div>
</div>
<div class="section" id="results" style="display:none">
<h2>Results</h2>
<div class="result-grid" id="resultGrid"></div>
<div class="btn-group">
<button class="btn btn-secondary" onclick="copyResults()">📋 Copy Results</button>
</div>
</div>
<div class="section">
<h2>FAQ</h2>
{''.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in t['en_faqs'])}
</div>
<div class="footer">&copy; 2026 Free ToolBase · Free Online Tools · No Signup Required · Data Never Uploaded</div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('toast')}},2000)}}
function copyResults(){{var r=document.getElementById('resultGrid').innerText;navigator.clipboard.writeText(r).then(function(){{showToast('Copied to clipboard')}}).catch(function(){{showToast('Copy failed, please select manually')}})}}
function clearAll(){{document.querySelectorAll('input').forEach(function(el){{el.value=''}});document.getElementById('results').style.display='none'}}
</script>
</body>
</html>'''
    
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print(f"✅ {slug}: CN + EN created")

if __name__ == '__main__':
    import os
    for t in TOOLS:
        gen_tool(t)
    print(f"\n总计: {len(TOOLS)}个工具已生成框架")