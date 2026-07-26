#!/usr/bin/env python3
"""深度翻译5个EN页面 - 替换残留中文"""
import re, os

SITE = "/home/chison/tools-site"

# 每个工具的完整翻译映射（zh -> en），按优先级
translations = {
    'investment-returns-calculator': {
        # section description
        '输入初始本金、预期年收益率和投资年限，支持每月定投，自动计算终值和总收益。': 'Enter initial principal, expected annual return, and investment period. Supports monthly contributions, automatically calculates future value and total gains.',
        # FAQ answers (zh -> en, already translated in tool info)
        '复利是指在每一个计息期后，将所生利息加入本金再计利息的计算方式。比如投资10000元，年收益率10%，第一年赚1000元，第二年本金变成11000元，就能赚1100元。复利效应随时间增长越滚越大，是长期投资的核心理念。': 'Compound interest means earning interest on your interest. For example, if you invest $10,000 at 10% annual return, you earn $1,000 in year one. In year two, your principal becomes $11,000 and you earn $1,100. The compounding effect grows exponentially over time — it\'s the core principle of long-term investing.',
        '定期定额投入（定投）可以平摊买入成本，避免一次性买在高点。无论市场涨跌都坚持投入，长期来看可以降低平均持仓成本，同时累积可观的投资本金。每月投入1000元，年化8%，30年后可累积约150万元。': 'Dollar-cost averaging (regular investing) smooths out your purchase price and avoids buying at market peaks. By consistently investing regardless of market conditions, you lower your average cost basis while building substantial capital. Investing $200/month at 8% annual return for 30 years accumulates approximately $300,000.',
        '年化收益率 = (终值/本金)^(1/年数) - 1。如果没有定期投入则直接用此公式。有定期投入时，使用内部收益率(IRR)来计算年化回报率，这更准确反映投资的真实收益水平。': 'Annualized Return = (Final Value / Principal)^(1/Years) - 1. For lump-sum investments, use this formula directly. With regular contributions, use Internal Rate of Return (IRR) for a more accurate measure of true investment performance.',
        '通货膨胀会侵蚀投资的实际购买力。实际回报率 = 名义回报率 - 通货膨胀率。例如名义回报率10%，通胀率3%，实际回报率约7%。本工具同时显示名义回报和考虑通胀后的实际回报，帮你了解投资的真实价值增长。': 'Inflation erodes the real purchasing power of your investments. Real Return = Nominal Return - Inflation Rate. For example, 10% nominal return with 3% inflation yields approximately 7% real return. This tool shows both nominal and inflation-adjusted returns so you understand true value growth.',
        # footer
        '投资回报计算器 | No Registration · Data Stays On Your Device': 'Investment Returns Calculator | No Registration · Data Stays On Your Device',
        '投资回报计算器 | 无需注册 · 数据绝不上传服务器': 'Investment Returns Calculator | No Registration · Data Stays On Your Device',
        # breadcrumb already fixed
    },
    'retirement-age-calculator': {
        '输入当前财务数据，计算达到财务独立并可以退休的年龄。': 'Enter your current financial data to calculate the age at which you can achieve financial independence and retire.',
        '退休年龄取决于三个核心因素：当前储蓄、每年储蓄金额、退休后的年支出。计算公式为退休年龄 = 当前年龄 + log(1 + (年支出 × 预期收益率) / 年储蓄) / log(1 + 预期收益率)。同时需要考虑社会保障和养老金的领取时间。': 'Retirement age depends on three core factors: current savings, annual savings, and post-retirement spending. The formula is: Retirement Age = Current Age + log(1 + (Annual Spending × Expected Return) / Annual Savings) / log(1 + Expected Return). Social Security and pension timing should also be considered.',
        'FIRE（Financial Independence, Retire Early）是一套实现财务独立和提前退休的方法论。核心原则是：储蓄率达到50%以上，投资低成本的指数基金，当资产达到年支出的25倍（4%法则）时可财务独立。常见有Lean FIRE（低消费提前退休）和Fat FIRE（高消费提前退休）。': 'FIRE (Financial Independence, Retire Early) is a methodology for achieving financial freedom and early retirement. Core principles: save 50%+ of income, invest in low-cost index funds, and reach 25× annual expenses (the 4% rule). Variants include Lean FIRE (frugal early retirement) and Fat FIRE (luxurious early retirement).',
        '4%法则（也称4%安全提款率）是财务规划中的经验法则：如果你每年只从退休金中提取4%，在历史股市表现下，你的资产至少可以维持30年不枯竭。对应地，你需要的退休金总额约等于年支出的25倍（100%/4%=25）。': 'The 4% rule (safe withdrawal rate) is a rule of thumb in financial planning: if you withdraw only 4% of your retirement portfolio annually, your assets should last at least 30 years based on historical market performance. This means you need approximately 25× your annual expenses saved (100%/4% = 25).',
        '按4%法则，需要的退休金 = 年支出 × 25。例如年支出20万元，需要500万退休金。如果考虑3%的安全提款率，则需要年支出的33倍。本工具会根据你的输入自动计算目标退休金和预计退休年龄。': 'Using the 4% rule: Retirement Fund Needed = Annual Expenses × 25. For example, $40,000 annual spending requires $1,000,000. With a more conservative 3% withdrawal rate, you need 33× annual expenses. This calculator automatically computes your target fund and estimated retirement age.',
        '退休年龄计算器 | 无需注册 · 数据绝不上传服务器': 'Retirement Age Calculator | No Registration · Data Stays On Your Device',
    },
    'college-roi-calculator': {
        '输入大学成本和预期收入差，计算教育投资的净现值和回报周期。': 'Enter college costs and expected income differential to calculate the net present value and payback period of your education investment.',
        '大学教育ROI = (毕业后终身收入增长 - 大学总成本) / 大学总成本。其中大学总成本包括学费、生活费、书本费，以及因上学放弃的4年工资收入（机会成本）。毕业后收入增长是指拥有大学学位相比高中学历的年收入差。': 'College ROI = (Lifetime Earnings Increase - Total College Cost) / Total College Cost. Total cost includes tuition, living expenses, books, and the opportunity cost of 4 years of forgone wages. Earnings increase is the annual salary difference between college and high school graduates.',
        '大学投资回报因专业和学校而异。数据显示STEM（科学、技术、工程、数学）专业的ROI通常很高，终身收入比高中学历多100-300万美元。而一些人文社科专业的ROI相对较低。本工具帮助你量化分析：投入的学费和生活费是否能在职业生涯中获得合理回报。': 'College ROI varies significantly by major and school. Data shows STEM (Science, Technology, Engineering, Math) majors typically have very high ROI, with lifetime earnings $1-3M above high school graduates. Some liberal arts majors have lower ROI. This tool helps you quantify whether tuition and living costs will yield reasonable career returns.',
        '大学成本包括：1) 直接成本：学费、住宿费、书本费、生活费；2) 机会成本：上学期间放弃的工资收入。例如，如果高中毕业年薪3万元，4年大学就放弃了12万元收入。总成本 = 直接成本 + 机会成本。这些都应纳入ROI计算。': 'College costs include: 1) Direct costs: tuition, housing, books, living expenses; 2) Opportunity cost: wages forgone during college years. For example, if a high school graduate earns $20,000/year, 4 years of college means $80,000 in forgone income. Total Cost = Direct Costs + Opportunity Cost. All should be included in ROI calculations.',
        '差异非常大。工程、计算机科学等专业终身ROI可达1000%以上；商科约500-800%；教育、社工等专业可能只有200-400%。选择专业时，不仅要考虑兴趣，也要评估经济回报。本工具让你自定义收入差参数，模拟不同专业的ROI。': 'The variance is enormous. Engineering and Computer Science majors can achieve 1000%+ lifetime ROI; Business majors around 500-800%; Education and Social Work may only see 200-400%. When choosing a major, consider both passion and economic returns. This tool lets you customize salary parameters to simulate different majors.',
        '大学教育ROI计算器 | 无需注册 · 数据绝不上传服务器': 'College ROI Calculator | No Registration · Data Stays On Your Device',
    },
    'savings-bond-calculator': {
        '选择债券类型，输入购买金额和持有年限，计算到期价值和收益。': 'Select bond type, enter purchase amount and holding period to calculate maturity value and returns.',
        '美国储蓄债券是由美国财政部发行的低风险投资产品，主要有两种：Series EE债券（固定利率，20年到期至少翻倍）和Series I债券（通胀保护，利率=固定利率+通胀率）。它们由美国政府全额担保，适合保守型投资者。': 'US Savings Bonds are low-risk investments issued by the US Treasury. There are two main types: Series EE bonds (fixed rate, guaranteed to at least double in 20 years) and Series I bonds (inflation-protected, rate = fixed rate + inflation rate). They are fully backed by the US government, ideal for conservative investors.',
        'EE债券提供固定利率（目前约2.5%），保证20年到期时至少翻倍。I债券的利率由两部分组成：固定利率（目前0.4%）+ 每半年调整的通胀率，能保护购买力不受通胀侵蚀。I债券更适合通胀高企时期，EE债券更适合长期持有。': 'EE bonds offer a fixed rate (currently ~2.5%) and guarantee doubling in value at 20 years. I bond rates have two components: a fixed rate (currently 0.4%) + a semiannual inflation adjustment, protecting purchasing power. I bonds are better during high inflation; EE bonds are better for very long-term holding.',
        '储蓄债券利息需缴纳联邦所得税，但免州税和地方税。如果用于合格教育支出，利息可能免税（有收入限制）。投资者可以选择每年报告利息或赎回时一次性报告。本工具计算的是税前收益。': 'Savings bond interest is subject to federal income tax but exempt from state and local taxes. Interest may be tax-free if used for qualified education expenses (income limits apply). Investors can report interest annually or defer until redemption. This calculator shows pre-tax returns.',
        'Series EE和Series I债券的原始期限为30年。20年时EE债券保证翻倍。债券在购买满1年后可赎回，但5年内赎回收3个月利息罚金。满5年后无罚金。本工具默认按30年到期计算。': 'Series EE and I bonds have an original maturity of 30 years. EE bonds are guaranteed to double at 20 years. Bonds can be redeemed after 1 year, but redemption within 5 years incurs a 3-month interest penalty. No penalty after 5 years. This tool calculates based on your specified holding period.',
        '储蓄债券计算器 | 无需注册 · 数据绝不上传服务器': 'Savings Bond Calculator | No Registration · Data Stays On Your Device',
    },
    'mortgage-points-calculator': {
        '输入贷款金额、原始利率和计划购买的折扣点数，对比总支出差异和回本周期。': 'Enter loan amount, original interest rate, and points to purchase. Compare total cost differences and payback period.',
        '房贷折扣点是你提前支付的一笔费用，用来降低贷款利率。1个点=贷款金额的1%。每个点通常降低利率0.25%。例如，贷款50万元，买1个点花费5000元，利率从6%降到5.75%，每月可省约80元。': 'Mortgage discount points are upfront fees paid to lower your interest rate. 1 point = 1% of the loan amount. Each point typically reduces the rate by 0.25%. For example, on a $500,000 loan, buying 1 point costs $5,000 and might reduce your rate from 6% to 5.75%, saving about $80/month.',
        '买折扣点是否划算取决于你打算持有多久。需要计算「收支平衡点」：折扣点成本 / 每月节省金额 = 需要多少个月收回成本。如果你计划持有超过这个月数，买点就划算。一般持有5年以上值得考虑，短期则不宜购买。': 'Whether points are worth it depends on how long you\'ll keep the mortgage. Calculate the break-even point: Points Cost ÷ Monthly Savings = Months to recoup. If you plan to stay beyond this period, buying points makes sense. Generally worth considering if you\'ll hold for 5+ years; not recommended for short-term ownership.',
        '在美国，房贷折扣点可以作为房贷利息在联邦税中抵扣，但要满足特定条件：贷款用于购买或改善主要住房，折扣点是当地惯例，且金额不超过当地平均水平。建议咨询税务专业人士。本工具展示的是税前对比。': 'In the US, mortgage points may be deductible as mortgage interest on federal taxes, subject to conditions: the loan must be for purchasing or improving your primary residence, points must be customary in your area, and the amount must not exceed typical local averages. Consult a tax professional. This tool shows pre-tax comparisons.',
        '一般建议购买0-2个点。每个点降低约0.25%利率。具体取决于：1)你能拿出的额外现金；2)计划持有时长；3)当前利率环境。本工具可以帮你对比「不买点」「买1个点」「买2个点」三种方案的总支出，一目了然。': 'Generally 0-2 points is recommended. Each point reduces the rate by ~0.25%. The optimal number depends on: 1) available cash; 2) planned holding period; 3) current rate environment. This tool lets you compare \'No Points\' vs \'Buy Points\' scenarios side by side.',
        '房贷折扣点计算器 | 无需注册 · 数据绝不上传服务器': 'Mortgage Points Calculator | No Registration · Data Stays On Your Device',
    },
}

for tool_name, trans_map in translations.items():
    filepath = os.path.join(SITE, "en", tool_name, "index.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for zh, en in trans_map.items():
        if zh in content:
            content = content.replace(zh, en)
    
    # 额外替换：页面中可能还存在 "中文" 和残留的tool名在footer
    # 中文 label in lang-switch is fine
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Deep translated: {tool_name}")

print("Done!")