#!/usr/bin/env python3
"""批量翻译5个新工具的英文版"""
import os, re

SITE = "/home/chison/tools-site"

tools = [
    {
        "name": "investment-returns-calculator",
        "zh_title": "投资回报计算器",
        "en_title": "Investment Returns Calculator",
        "zh_desc": "免费在线投资回报计算器，计算复利终值、年化收益率、总投入和总收益。支持定期定额投入，自动生成投资增长表，无需注册，数据不上传服务器。",
        "en_desc": "Free online investment returns calculator. Calculate compound future value, annualized return, total investment, and total gains. Supports regular contributions with auto-generated growth tables. No sign-up required.",
        "icon": "📈",
        "en_hero": "Free online investment returns calculator. Calculate compound future value, annualized return, total contributions and gains. Supports recurring investments with year-by-year growth tables. | No registration · Data stays on your device",
        "labels": {
            "初始本金 (¥)": "Initial Principal ($)",
            "预期年收益率 (%)": "Expected Annual Return (%)",
            "投资年限": "Investment Period (Years)",
            "每月定投 (¥)": "Monthly Contribution ($)",
            "通货膨胀率 (%)": "Inflation Rate (%)",
            "计算回报": "Calculate Returns",
            "清空": "Clear",
            "投资终值": "Future Value",
            "总投入": "Total Invested",
            "总收益": "Total Gain",
            "年化收益率": "Annualized Return",
            "实际终值(扣除通胀)": "Real Value (Inflation-Adjusted)",
            "收益倍数": "Gain Multiple",
            "📋 复制结果": "📋 Copy Results",
            "投资增长明细": "Investment Growth Details",
            "年份": "Year",
            "年初本金": "Start Balance",
            "年投入": "Annual Contribution",
            "年收益": "Annual Gain",
            "年末余额": "End Balance",
        },
        "faqs": [
            ("什么是复利投资？", "What is compound interest?", "复利是指在每一个计息期后，将所生利息加入本金再计利息的计算方式。比如投资10000元，年收益率10%，第一年赚1000元，第二年本金变成11000元，就能赚1100元。复利效应随时间增长越滚越大，是长期投资的核心理念。", "Compound interest means earning interest on your interest. For example, if you invest $10,000 at 10% annual return, you earn $1,000 in year one. In year two, your principal becomes $11,000 and you earn $1,100. The compounding effect grows exponentially over time — it's the core principle of long-term investing."),
            ("定期定额投入有什么好处？", "What are the benefits of dollar-cost averaging?", "定期定额投入（定投）可以平摊买入成本，避免一次性买在高点。无论市场涨跌都坚持投入，长期来看可以降低平均持仓成本，同时累积可观的投资本金。每月投入1000元，年化8%，30年后可累积约150万元。", "Dollar-cost averaging (regular investing) smooths out your purchase price and avoids buying at market peaks. By consistently investing regardless of market conditions, you lower your average cost basis while building substantial capital. Investing $200/month at 8% annual return for 30 years accumulates approximately $300,000."),
            ("年化收益率如何计算？", "How is annualized return calculated?", "年化收益率 = (终值/本金)^(1/年数) - 1。如果没有定期投入则直接用此公式。有定期投入时，使用内部收益率(IRR)来计算年化回报率，这更准确反映投资的真实收益水平。", "Annualized Return = (Final Value / Principal)^(1/Years) - 1. For lump-sum investments, use this formula directly. With regular contributions, use Internal Rate of Return (IRR) for a more accurate measure of true investment performance."),
            ("通货膨胀对投资回报有什么影响？", "How does inflation affect investment returns?", "通货膨胀会侵蚀投资的实际购买力。实际回报率 = 名义回报率 - 通货膨胀率。例如名义回报率10%，通胀率3%，实际回报率约7%。本工具同时显示名义回报和考虑通胀后的实际回报，帮你了解投资的真实价值增长。", "Inflation erodes the real purchasing power of your investments. Real Return = Nominal Return - Inflation Rate. For example, 10% nominal return with 3% inflation yields approximately 7% real return. This tool shows both nominal and inflation-adjusted returns so you understand true value growth."),
        ],
    },
    {
        "name": "retirement-age-calculator",
        "zh_title": "退休年龄计算器",
        "en_title": "Retirement Age Calculator",
        "zh_desc": "免费在线退休年龄计算器，根据当前年龄、储蓄、收入、目标退休金计算最早退休年龄。支持社保、年金等收入来源，无需注册，数据不上传服务器。",
        "en_desc": "Free online retirement age calculator. Estimate your earliest retirement age based on current savings, income, and retirement goals. FIRE financial independence planning. No sign-up required.",
        "icon": "🎯",
        "en_hero": "Free online retirement age calculator. Predict your earliest retirement age based on savings, income and expenses. FIRE financial independence planning. | No registration · Data stays on your device",
        "labels": {
            "当前年龄": "Current Age",
            "现有储蓄 (¥)": "Current Savings ($)",
            "年收入 (¥)": "Annual Income ($)",
            "储蓄率 (%)": "Savings Rate (%)",
            "预期年收益率 (%)": "Expected Annual Return (%)",
            "退休后年支出 (¥)": "Annual Retirement Spending ($)",
            "安全提款率 (%)": "Safe Withdrawal Rate (%)",
            "计算退休年龄": "Calculate Retirement Age",
            "清空": "Clear",
            "预计退休年龄": "Estimated Retirement Age",
            "距离退休还有": "Years Until Retirement",
            "目标退休金": "Target Retirement Fund",
            "每年储蓄": "Annual Savings",
            "退休时总资产": "Assets at Retirement",
            "年被动收入": "Annual Passive Income",
            "📋 复制结果": "📋 Copy Results",
        },
        "faqs": [
            ("如何计算退休年龄？", "How is retirement age calculated?", "退休年龄取决于三个核心因素：当前储蓄、每年储蓄金额、退休后的年支出。计算公式为退休年龄 = 当前年龄 + log(1 + (年支出 × 预期收益率) / 年储蓄) / log(1 + 预期收益率)。同时需要考虑社会保障和养老金的领取时间。", "Retirement age depends on three core factors: current savings, annual savings, and post-retirement spending. The formula is: Retirement Age = Current Age + log(1 + (Annual Spending × Expected Return) / Annual Savings) / log(1 + Expected Return). Social Security and pension timing should also be considered."),
            ("什么是FIRE运动？", "What is the FIRE movement?", "FIRE（Financial Independence, Retire Early）是一套实现财务独立和提前退休的方法论。核心原则是：储蓄率达到50%以上，投资低成本的指数基金，当资产达到年支出的25倍（4%法则）时可财务独立。常见有Lean FIRE（低消费提前退休）和Fat FIRE（高消费提前退休）。", "FIRE (Financial Independence, Retire Early) is a methodology for achieving financial freedom and early retirement. Core principles: save 50%+ of income, invest in low-cost index funds, and reach 25× annual expenses (the 4% rule). Variants include Lean FIRE (frugal early retirement) and Fat FIRE (luxurious early retirement)."),
            ("4%法则是什么意思？", "What is the 4% rule?", "4%法则（也称4%安全提款率）是财务规划中的经验法则：如果你每年只从退休金中提取4%，在历史股市表现下，你的资产至少可以维持30年不枯竭。对应地，你需要的退休金总额约等于年支出的25倍（100%/4%=25）。", "The 4% rule (safe withdrawal rate) is a rule of thumb in financial planning: if you withdraw only 4% of your retirement portfolio annually, your assets should last at least 30 years based on historical market performance. This means you need approximately 25× your annual expenses saved (100%/4% = 25)."),
            ("退休需要攒多少钱？", "How much do I need to retire?", "按4%法则，需要的退休金 = 年支出 × 25。例如年支出20万元，需要500万退休金。如果考虑3%的安全提款率，则需要年支出的33倍。本工具会根据你的输入自动计算目标退休金和预计退休年龄。", "Using the 4% rule: Retirement Fund Needed = Annual Expenses × 25. For example, $40,000 annual spending requires $1,000,000. With a more conservative 3% withdrawal rate, you need 33× annual expenses. This calculator automatically computes your target fund and estimated retirement age."),
        ],
    },
    {
        "name": "college-roi-calculator",
        "zh_title": "大学教育ROI计算器",
        "en_title": "College ROI Calculator",
        "zh_desc": "免费在线大学教育投资回报率计算器，对比上大学的成本和未来收入增长，计算净现值和回报周期。帮助你做出明智的教育投资决策，无需注册。",
        "en_desc": "Free online college ROI calculator. Compare the cost of college against future income gains. Calculate NPV and payback period to make informed education investment decisions. No sign-up required.",
        "icon": "🎓",
        "en_hero": "Free online college ROI calculator. Compare education costs against future earnings to calculate net present value and payback period. | No registration · Data stays on your device",
        "labels": {
            "年学费 (¥)": "Annual Tuition ($)",
            "年生活费+书本费 (¥)": "Living + Books ($/yr)",
            "大学年数": "Years in College",
            "高中毕业年薪 (¥)": "High School Graduate Salary ($)",
            "大学毕业起薪 (¥)": "College Graduate Starting Salary ($)",
            "年薪增长率 (%)": "Annual Salary Growth (%)",
            "工作年限": "Working Years",
            "折现率 (%)": "Discount Rate (%)",
            "计算ROI": "Calculate ROI",
            "清空": "Clear",
            "大学总成本": "Total College Cost",
            "终身收入差(名义)": "Lifetime Earnings Gap (Nominal)",
            "净现值(NPV)": "Net Present Value (NPV)",
            "投资回报率(ROI)": "Return on Investment (ROI)",
            "回本周期": "Payback Period",
            "NPV>0则值得投资": "NPV > 0 = Worth It",
            "📋 复制结果": "📋 Copy Results",
        },
        "faqs": [
            ("大学教育的投资回报率怎么算？", "How is college ROI calculated?", "大学教育ROI = (毕业后终身收入增长 - 大学总成本) / 大学总成本。其中大学总成本包括学费、生活费、书本费，以及因上学放弃的4年工资收入（机会成本）。毕业后收入增长是指拥有大学学位相比高中学历的年收入差。", "College ROI = (Lifetime Earnings Increase - Total College Cost) / Total College Cost. Total cost includes tuition, living expenses, books, and the opportunity cost of 4 years of forgone wages. Earnings increase is the annual salary difference between college and high school graduates."),
            ("读大学值不值？", "Is college worth it?", "大学投资回报因专业和学校而异。数据显示STEM（科学、技术、工程、数学）专业的ROI通常很高，终身收入比高中学历多100-300万美元。而一些人文社科专业的ROI相对较低。本工具帮助你量化分析：投入的学费和生活费是否能在职业生涯中获得合理回报。", "College ROI varies significantly by major and school. Data shows STEM (Science, Technology, Engineering, Math) majors typically have very high ROI, with lifetime earnings $1-3M above high school graduates. Some liberal arts majors have lower ROI. This tool helps you quantify whether tuition and living costs will yield reasonable career returns."),
            ("大学成本包括哪些？", "What does college cost include?", "大学成本包括：1) 直接成本：学费、住宿费、书本费、生活费；2) 机会成本：上学期间放弃的工资收入。例如，如果高中毕业年薪3万元，4年大学就放弃了12万元收入。总成本 = 直接成本 + 机会成本。这些都应纳入ROI计算。", "College costs include: 1) Direct costs: tuition, housing, books, living expenses; 2) Opportunity cost: wages forgone during college years. For example, if a high school graduate earns $20,000/year, 4 years of college means $80,000 in forgone income. Total Cost = Direct Costs + Opportunity Cost. All should be included in ROI calculations."),
            ("不同专业的ROI差异有多大？", "How much does ROI vary by major?", "差异非常大。工程、计算机科学等专业终身ROI可达1000%以上；商科约500-800%；教育、社工等专业可能只有200-400%。选择专业时，不仅要考虑兴趣，也要评估经济回报。本工具让你自定义收入差参数，模拟不同专业的ROI。", "The variance is enormous. Engineering and Computer Science majors can achieve 1000%+ lifetime ROI; Business majors around 500-800%; Education and Social Work may only see 200-400%. When choosing a major, consider both passion and economic returns. This tool lets you customize salary parameters to simulate different majors."),
        ],
    },
    {
        "name": "savings-bond-calculator",
        "zh_title": "储蓄债券计算器",
        "en_title": "Savings Bond Calculator",
        "zh_desc": "免费在线储蓄债券计算器，计算美国Series EE/I储蓄债券的到期价值、利息收入和年化收益率。支持不同面额和持有期限，无需注册。",
        "en_desc": "Free online savings bond calculator. Calculate maturity value, interest earned, and annualized return for US Series EE/I savings bonds. Supports different denominations and holding periods. No sign-up required.",
        "icon": "🏦",
        "en_hero": "Free online savings bond calculator. Calculate maturity value, interest, and annualized return for US Series EE/I savings bonds. | No registration · Data stays on your device",
        "labels": {
            "债券类型": "Bond Type",
            "Series EE (固定利率，20年保证翻倍)": "Series EE (Fixed Rate, Guaranteed to Double in 20 Years)",
            "Series I (通胀保护债券)": "Series I (Inflation-Protected Bond)",
            "购买金额 ($)": "Purchase Amount ($)",
            "持有年限": "Holding Period (Years)",
            "固定利率 (%)": "Fixed Rate (%)",
            "通胀率 (%)": "Inflation Rate (%)",
            "计算收益": "Calculate Returns",
            "清空": "Clear",
            "到期价值": "Maturity Value",
            "利息收入": "Interest Earned",
            "年化收益率": "Annualized Return",
            "本金翻倍": "Principal Doubled?",
            "📋 复制结果": "📋 Copy Results",
        },
        "faqs": [
            ("什么是美国储蓄债券？", "What are US Savings Bonds?", "美国储蓄债券是由美国财政部发行的低风险投资产品，主要有两种：Series EE债券（固定利率，20年到期至少翻倍）和Series I债券（通胀保护，利率=固定利率+通胀率）。它们由美国政府全额担保，适合保守型投资者。", "US Savings Bonds are low-risk investments issued by the US Treasury. There are two main types: Series EE bonds (fixed rate, guaranteed to at least double in 20 years) and Series I bonds (inflation-protected, rate = fixed rate + inflation rate). They are fully backed by the US government, ideal for conservative investors."),
            ("Series EE和Series I债券有什么区别？", "What's the difference between Series EE and Series I?", "EE债券提供固定利率（目前约2.5%），保证20年到期时至少翻倍。I债券的利率由两部分组成：固定利率（目前0.4%）+ 每半年调整的通胀率，能保护购买力不受通胀侵蚀。I债券更适合通胀高企时期，EE债券更适合长期持有。", "EE bonds offer a fixed rate (currently ~2.5%) and guarantee doubling in value at 20 years. I bond rates have two components: a fixed rate (currently 0.4%) + a semiannual inflation adjustment, protecting purchasing power. I bonds are better during high inflation; EE bonds are better for very long-term holding."),
            ("储蓄债券的利息要交税吗？", "Are savings bond interest taxable?", "储蓄债券利息需缴纳联邦所得税，但免州税和地方税。如果用于合格教育支出，利息可能免税（有收入限制）。投资者可以选择每年报告利息或赎回时一次性报告。本工具计算的是税前收益。", "Savings bond interest is subject to federal income tax but exempt from state and local taxes. Interest may be tax-free if used for qualified education expenses (income limits apply). Investors can report interest annually or defer until redemption. This calculator shows pre-tax returns."),
            ("储蓄债券何时到期？", "When do savings bonds mature?", "Series EE和Series I债券的原始期限为30年。20年时EE债券保证翻倍。债券在购买满1年后可赎回，但5年内赎回收3个月利息罚金。满5年后无罚金。本工具默认按30年到期计算。", "Series EE and I bonds have an original maturity of 30 years. EE bonds are guaranteed to double at 20 years. Bonds can be redeemed after 1 year, but redemption within 5 years incurs a 3-month interest penalty. No penalty after 5 years. This tool calculates based on your specified holding period."),
        ],
    },
    {
        "name": "mortgage-points-calculator",
        "zh_title": "房贷折扣点计算器",
        "en_title": "Mortgage Points Calculator",
        "zh_desc": "免费在线房贷折扣点计算器，计算购买房贷折扣点的成本和节省金额。对比支付折扣点降低利率带来的长期节省，帮你做出最优决策，无需注册。",
        "en_desc": "Free online mortgage points calculator. Calculate the cost and savings of buying discount points. Compare long-term savings from paying points to lower your interest rate. Make optimal mortgage decisions. No sign-up required.",
        "icon": "🏠",
        "en_hero": "Free online mortgage points calculator. Compare the cost of buying discount points against long-term savings from lower interest rates. | No registration · Data stays on your device",
        "labels": {
            "贷款金额 (¥)": "Loan Amount ($)",
            "贷款期限 (年)": "Loan Term (Years)",
            "原始年利率 (%)": "Original Interest Rate (%)",
            "购买折扣点数": "Points to Purchase",
            "每点降低利率 (%)": "Rate Reduction Per Point (%)",
            "计算对比": "Compare Options",
            "清空": "Clear",
            "方案": "Scenario",
            "利率": "Rate",
            "月供": "Monthly Payment",
            "折扣点成本": "Points Cost",
            "总利息": "Total Interest",
            "总支出": "Total Cost",
            "月供节省": "Monthly Savings",
            "总利息节省": "Total Interest Saved",
            "净节省": "Net Savings",
            "回本周期": "Payback Period",
            "📋 复制结果": "📋 Copy Results",
            "不买点": "No Points",
            "买": "Buy ",
            "个点": " Points",
        },
        "faqs": [
            ("什么是房贷折扣点（Mortgage Points）？", "What are mortgage discount points?", "房贷折扣点是你提前支付的一笔费用，用来降低贷款利率。1个点=贷款金额的1%。每个点通常降低利率0.25%。例如，贷款50万元，买1个点花费5000元，利率从6%降到5.75%，每月可省约80元。", "Mortgage discount points are upfront fees paid to lower your interest rate. 1 point = 1% of the loan amount. Each point typically reduces the rate by 0.25%. For example, on a $500,000 loan, buying 1 point costs $5,000 and might reduce your rate from 6% to 5.75%, saving about $80/month."),
            ("买房贷折扣点值不值？", "Are mortgage points worth buying?", "买折扣点是否划算取决于你打算持有多久。需要计算「收支平衡点」：折扣点成本 / 每月节省金额 = 需要多少个月收回成本。如果你计划持有超过这个月数，买点就划算。一般持有5年以上值得考虑，短期则不宜购买。", "Whether points are worth it depends on how long you'll keep the mortgage. Calculate the break-even point: Points Cost ÷ Monthly Savings = Months to recoup. If you plan to stay beyond this period, buying points makes sense. Generally worth considering if you'll hold for 5+ years; not recommended for short-term ownership."),
            ("折扣点可以抵税吗？", "Are mortgage points tax deductible?", "在美国，房贷折扣点可以作为房贷利息在联邦税中抵扣，但要满足特定条件：贷款用于购买或改善主要住房，折扣点是当地惯例，且金额不超过当地平均水平。建议咨询税务专业人士。本工具展示的是税前对比。", "In the US, mortgage points may be deductible as mortgage interest on federal taxes, subject to conditions: the loan must be for purchasing or improving your primary residence, points must be customary in your area, and the amount must not exceed typical local averages. Consult a tax professional. This tool shows pre-tax comparisons."),
            ("买多少折扣点合适？", "How many points should I buy?", "一般建议购买0-2个点。每个点降低约0.25%利率。具体取决于：1)你能拿出的额外现金；2)计划持有时长；3)当前利率环境。本工具可以帮你对比「不买点」「买1个点」「买2个点」三种方案的总支出，一目了然。", "Generally 0-2 points is recommended. Each point reduces the rate by ~0.25%. The optimal number depends on: 1) available cash; 2) planned holding period; 3) current rate environment. This tool lets you compare 'No Points' vs 'Buy Points' scenarios side by side."),
        ],
    },
]

def translate_page(filepath, tool_info):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # lang
    content = content.replace('lang="zh-CN"', 'lang="en"')

    # canonical
    name = tool_info["name"]
    content = content.replace(f'href="https://free-toolbase.com/{name}/"', f'href="https://free-toolbase.com/en/{name}/"')

    # og:url
    content = content.replace(f'content="https://free-toolbase.com/{name}/"', f'content="https://free-toolbase.com/en/{name}/"')

    # hreflang
    content = content.replace(f'href="https://free-toolbase.com/{name}/"', f'href="https://free-toolbase.com/en/{name}/"')

    # title
    content = content.replace(f'<title>免费{tool_info["zh_title"]}', f'<title>Free {tool_info["en_title"]}')
    content = content.replace(' | 无需注册</title>', ' | No Sign-Up</title>')

    # og:title
    content = content.replace(f'content="免费{tool_info["zh_title"]}', f'content="Free {tool_info["en_title"]}')
    content = content.replace(' | 无需注册"', ' | No Sign-Up"')

    # description
    content = content.replace(f'content="{tool_info["zh_desc"]}"', f'content="{tool_info["en_desc"]}"')

    # h1
    content = content.replace(f'<h1>{tool_info["icon"]} {tool_info["zh_title"]}</h1>', f'<h1>{tool_info["icon"]} {tool_info["en_title"]}</h1>')

    # lang switch
    content = content.replace(f'<a href="index.html" class="active">中文</a><a href="../en/{name}/" class="">EN</a>',
                               f'<a href="../{name}/" class="">中文</a><a href="index.html" class="active">EN</a>')

    # nav-back 首页→Home, 工具→Tools
    content = content.replace('>首页</a>', '>Home</a>')
    content = content.replace('>工具</a>', '>Tools</a>')

    # hero
    old_hero_pattern = re.search(r'<div class="hero"><p>.*?</p>', content)
    if old_hero_pattern:
        old_hero = old_hero_pattern.group()
        new_hero = f'<div class="hero"><p>{tool_info["en_hero"]}</p>'
        content = content.replace(old_hero, new_hero)

    # badge
    content = content.replace('零依赖·可离线使用', 'Zero Dependencies · Works Offline')

    # labels
    for zh, en in tool_info["labels"].items():
        content = content.replace(zh, en)

    # FAQ titles and answers
    for zh_q, en_q, zh_a, en_a in tool_info["faqs"]:
        content = content.replace(f'<h3>{zh_q}</h3>', f'<h3>{en_q}</h3>')
        content = content.replace(f'<p>{zh_a}</p>', f'<p>{en_a}</p>')

    # breadcrumb
    content = content.replace('"name": "首页"', '"name": "Home"')
    content = content.replace('"name": "工具"', '"name": "Tools"')
    content = content.replace(f'"name": "{tool_info["zh_title"]}"', f'"name": "{tool_info["en_title"]}"')

    # Schema names
    content = content.replace(f'"name": "{tool_info["zh_title"]}"', f'"name": "{tool_info["en_title"]}"')

    # HowTo name
    content = content.replace(f'"如何使用{tool_info["zh_title"]}"', f'"How to Use the {tool_info["en_title"]}"')

    # FAQ title in Schema
    content = content.replace(f'"如何使用{tool_info["zh_title"]}"', f'"How to Use the {tool_info["en_title"]}"')

    # 常见问题 → FAQ
    content = content.replace('常见问题', 'Frequently Asked Questions')

    # 首页/全部工具/联系我们/隐私政策/服务条款/关于我们
    content = content.replace('>首页</a>', '>Home</a>')
    content = content.replace('>全部工具</a>', '>All Tools</a>')
    content = content.replace('>联系我们</a>', '>Contact</a>')
    content = content.replace('>隐私政策</a>', '>Privacy Policy</a>')
    content = content.replace('>服务条款</a>', '>Terms of Service</a>')
    content = content.replace('>关于我们</a>', '>About</a>')

    # footer text
    content = content.replace(' | 无需注册 · 数据绝不上传服务器', ' | No Registration · Data Stays On Your Device')
    content = content.replace('问题反馈:', 'Feedback:')

    # showToast messages
    content = content.replace('"已复制"', '"Copied!"')
    content = content.replace('"复制失败"', '"Copy failed"')

    # 投资回报计算结果 → results title in JS
    content = content.replace('"投资回报计算结果"', '"Investment Returns Calculation Results"')
    content = content.replace('"退休年龄计算结果"', '"Retirement Age Calculation Results"')
    content = content.replace('"大学教育ROI计算结果"', '"College ROI Calculation Results"')
    content = content.replace('"储蓄债券计算结果"', '"Savings Bond Calculation Results"')
    content = content.replace('"房贷折扣点计算结果"', '"Mortgage Points Calculation Results"')

    # formatMoney locale
    content = content.replace("'zh-CN'", "'en-US'")

    # Updated date stays same

    # Misc
    content = content.replace('无需注册 · 数据绝不上传服务器', 'No Registration · Data Stays On Your Device')
    content = content.replace('第', 'Year ')
    content = content.replace('年</td>', '</td>')
    content = content.replace('✅ 值得', '✅ Worth It')
    content = content.replace('❌ 不值得', '❌ Not Worth It')
    content = content.replace('✅ 是', '✅ Yes')
    content = content.replace('❌ 否', '❌ No')
    content = content.replace('无法达成', 'Unreachable')
    content = content.replace('约', '~')
    content = content.replace('岁', ' yrs old')
    content = content.replace('年</td>', ' yrs</td>')
    content = content.replace('/年', '/yr')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for tool in tools:
    path = os.path.join(SITE, "en", tool["name"], "index.html")
    translate_page(path, tool)
    print(f"Translated: {tool['name']}")

print("\nAll 5 English versions done!")