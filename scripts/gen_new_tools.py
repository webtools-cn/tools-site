#!/usr/bin/env python3
"""批量生成5个新工具：fertility / epf / fixed-deposit / esop / cap-table"""
import os

TOOLS = {
    "fertility-calculator": {
        "zh_name": "排卵期与受孕计算器",
        "en_name": "Fertility & Ovulation Calculator",
        "zh_desc": "免费在线排卵期与受孕计算器，基于月经周期预测排卵日和易孕期，支持日历视图和受孕窗口期显示。纯前端本地计算，数据安全不上传服务器。",
        "en_desc": "Free online fertility & ovulation calculator. Predict ovulation day and fertile window based on menstrual cycle. Calendar view with conception window. 100% client-side, no data upload.",
        "zh_keywords": "排卵期计算器,受孕计算器,易孕期,排卵日预测,备孕",
        "en_keywords": "ovulation calculator,fertility calculator,fertile window,conception calculator,ovulation predictor",
        "category": "健康",
        "en_category": "Health",
        "faq": [
            {"q": "如何计算排卵期？", "a": "对于28天周期的女性，排卵通常发生在下次月经前14天。本工具根据您输入的月经周期长度和末次月经日期，自动计算排卵日和易孕期窗口（排卵前5天+排卵日当天）。"},
            {"q": "易孕期是什么？", "a": "易孕期（fertile window）是指最有可能受孕的时期，通常包括排卵前5天和排卵日当天，共约6天。精子在女性体内可存活3-5天，卵子排出后可存活12-24小时。"},
            {"q": "这个计算器准确吗？", "a": "本工具基于标准排卵计算方法，对于周期规律的女性准确率较高。但实际排卵可能受压力、疾病、药物等因素影响。建议结合排卵试纸或基础体温测量获取更精确的结果。"},
            {"q": "月经不规律怎么办？", "a": "如果月经周期不规律，可以取最近3-6个月的平均周期长度进行计算。对于严重不规律的周期，建议咨询妇产科医生。"},
            {"q": "最佳同房时间是什么时候？", "a": "在排卵日前1-2天同房受孕几率最高。研究表明，排卵前2天同房受孕率约25-28%，排卵日当天约8-10%。"},
            {"q": "排卵有哪些身体信号？", "a": "常见排卵信号包括：宫颈黏液变清变稀（类似蛋清）、基础体温升高0.3-0.5°C、轻度下腹痛（排卵痛）、乳房胀痛、性欲增强等。"},
        ],
        "en_faq": [
            {"q": "How to calculate ovulation?", "a": "For a 28-day cycle, ovulation typically occurs 14 days before the next period. This tool calculates your ovulation day and fertile window based on your cycle length and last period date."},
            {"q": "What is the fertile window?", "a": "The fertile window is the period when conception is most likely, typically 5 days before ovulation plus ovulation day itself, totaling about 6 days. Sperm can survive 3-5 days, and the egg survives 12-24 hours."},
            {"q": "How accurate is this calculator?", "a": "This tool uses standard ovulation calculation methods and is fairly accurate for women with regular cycles. However, actual ovulation may vary due to stress, illness, or medication."},
            {"q": "What if my cycle is irregular?", "a": "For irregular cycles, use the average length of your last 3-6 cycles. For severely irregular cycles, consult a gynecologist."},
            {"q": "When is the best time to conceive?", "a": "The highest conception rates occur 1-2 days before ovulation (~25-28%), compared to ovulation day (~8-10%)."},
            {"q": "What are physical signs of ovulation?", "a": "Common signs include: clear, stretchy cervical mucus (egg-white consistency), slight rise in basal body temperature (0.3-0.5°C), mild lower abdominal pain (mittelschmerz), breast tenderness, and increased libido."},
        ],
    },
    "epf-calculator": {
        "zh_name": "EPF雇员公积金计算器",
        "en_name": "EPF (Employee Provident Fund) Calculator",
        "zh_desc": "免费在线EPF雇员公积金计算器，快速计算马来西亚/印度EPF缴款、利息和退休储蓄总额。支持自定义利率、缴款比例和年限。纯前端计算，数据安全。",
        "en_desc": "Free online EPF (Employee Provident Fund) calculator. Calculate EPF contributions, interest, and retirement savings for Malaysia/India. Customizable interest rate, contribution rate, and tenure. 100% client-side.",
        "zh_keywords": "EPF计算器,雇员公积金,公积金计算器,退休储蓄,EPF利息",
        "en_keywords": "EPF calculator,employee provident fund,provident fund calculator,retirement savings,EPF interest",
        "category": "金融",
        "en_category": "Finance",
        "faq": [
            {"q": "EPF是什么？", "a": "EPF（雇员公积金）是马来西亚和印度等国的强制性退休储蓄计划。雇主和雇员每月各缴纳一定比例的工资到公积金账户，账户累积资金可获得年利息，退休时可一次性提取。"},
            {"q": "EPF缴款比例是多少？", "a": "以马来西亚为例：雇员缴纳11%（可选择降低至特定比例），雇主缴纳12-13%（根据工资水平）。印度EPF：雇员缴纳12%基本工资，雇主缴纳12%（其中3.67%进入EPF，8.33%进入EPS）。"},
            {"q": "EPF利息如何计算？", "a": "EPF利息按年复利计算，每年由公积金局宣布利率。利息按月计算但按年计入账户。本工具支持设置不同的年利率来模拟不同场景。"},
            {"q": "什么时候可以提取EPF？", "a": "通常退休年龄（55-60岁，视国家而定）可全额提取。部分提取可用于购房、教育、医疗等特定目的。不同国家政策有差异。"},
            {"q": "如何最大化EPF收益？", "a": "1）尽早开始缴纳；2）考虑自愿额外缴款（超出强制部分）；3）利用复利效应长期持有；4）关注每年宣布的利率变化。"},
        ],
        "en_faq": [
            {"q": "What is EPF?", "a": "EPF (Employee Provident Fund) is a mandatory retirement savings scheme in Malaysia, India, and other countries. Both employer and employee contribute monthly, and the accumulated fund earns annual interest."},
            {"q": "What are EPF contribution rates?", "a": "Malaysia: Employee 11% (can be reduced), Employer 12-13% (varies by salary). India: Employee 12% of basic salary, Employer 12% (3.67% to EPF, 8.33% to EPS)."},
            {"q": "How is EPF interest calculated?", "a": "EPF interest is compounded annually at a rate declared yearly by the EPF board. Interest is calculated monthly but credited annually. This tool lets you simulate different rates."},
            {"q": "When can I withdraw EPF?", "a": "Full withdrawal at retirement age (55-60, depending on country). Partial withdrawals allowed for housing, education, medical, etc. Policies vary by country."},
            {"q": "How to maximize EPF returns?", "a": "1) Start early; 2) Consider voluntary additional contributions; 3) Leverage compound interest over the long term; 4) Monitor annual declared interest rates."},
        ],
    },
    "fixed-deposit-calculator": {
        "zh_name": "定期存款利息计算器",
        "en_name": "Fixed Deposit (FD) Interest Calculator",
        "zh_desc": "免费在线定期存款利息计算器，计算FD/RD到期本息总额，支持单利/复利模式、不同计息周期（月/季/年）。快速比较不同银行利率和期限的收益。纯前端计算。",
        "en_desc": "Free online Fixed Deposit (FD) interest calculator. Calculate maturity amount with simple/compound interest modes and various compounding frequencies (monthly/quarterly/yearly). Compare returns across rates and tenures. 100% client-side.",
        "zh_keywords": "定期存款计算器,FD计算器,存款利息,定期存款,复利计算器",
        "en_keywords": "fixed deposit calculator,FD calculator,deposit interest,term deposit,compound interest calculator",
        "category": "金融",
        "en_category": "Finance",
        "faq": [
            {"q": "定期存款利息怎么算？", "a": "定期存款利息通常按复利计算，公式为：到期本息 = 本金 × (1 + 年利率/计息次数)^(计息次数×年限)。部分银行也使用单利计算。本工具同时支持单利和复利两种模式。"},
            {"q": "单利和复利有什么区别？", "a": "单利只对本金计息，复利对本金和已产生利息一起计息（利滚利）。长期来看，复利的收益显著高于单利。例如：1万元存5年、年利率5%，单利到期12500元，复利到期12763元。"},
            {"q": "计息周期对收益有影响吗？", "a": "有。在复利模式下，计息越频繁（如按月 vs 按年），最终收益越高。例如同样利率5%，按月复利比按年复利多约0.12%的实际年化收益。"},
            {"q": "提前支取会怎样？", "a": "提前支取通常会损失部分利息，银行会按活期利率或降低后的利率计算。部分银行收取罚金。本工具计算正常到期情况，不包含提前支取场景。"},
            {"q": "如何选择最佳定期存款？", "a": "1）比较不同银行的利率；2）考虑计息频率（按月>按季>按年）；3）关注是否有复利；4）大额存款通常可获得更高利率（优惠利率）；5）注意存款保险上限。"},
        ],
        "en_faq": [
            {"q": "How is FD interest calculated?", "a": "FD interest is typically compounded: Maturity = Principal × (1 + Rate/N)^(N×Years), where N = compounding frequency. Some banks use simple interest. This tool supports both modes."},
            {"q": "Simple vs compound interest?", "a": "Simple interest only earns on the principal. Compound interest earns on principal + accumulated interest. Over time, compounding yields significantly more."},
            {"q": "Does compounding frequency matter?", "a": "Yes. With the same annual rate, more frequent compounding (monthly vs yearly) yields higher returns. Monthly compounding adds ~0.12% effective annual yield over yearly."},
            {"q": "What happens on premature withdrawal?", "a": "Premature withdrawal typically results in interest penalty — banks may apply savings rate or reduced rate. Some charge penalties. This tool calculates normal maturity only."},
            {"q": "How to choose the best FD?", "a": "1) Compare rates across banks; 2) Prefer monthly compounding over quarterly/yearly; 3) Verify compound interest is used; 4) Large deposits may qualify for preferential rates; 5) Note deposit insurance limits."},
        ],
    },
    "esop-calculator": {
        "zh_name": "ESOP员工股权激励计算器",
        "en_name": "ESOP (Employee Stock Option) Calculator",
        "zh_desc": "免费在线ESOP员工股权激励计算器，计算期权行权收益、税后净值和不同退出场景下的股权价值。支持多轮行权和分批归属。纯前端计算，数据安全。",
        "en_desc": "Free online ESOP (Employee Stock Option Plan) calculator. Calculate exercise profit, post-tax gains, and equity value under different exit scenarios. Supports multi-tranche exercise and vesting schedules. 100% client-side.",
        "zh_keywords": "ESOP计算器,股权激励,期权计算,行权收益,员工股权",
        "en_keywords": "ESOP calculator,employee stock options,equity calculator,option exercise,stock option value",
        "category": "金融",
        "en_category": "Finance",
        "faq": [
            {"q": "ESOP是什么？", "a": "ESOP（员工股权激励计划）是公司授予员工的股票期权，允许员工在未来以约定价格（行权价）购买公司股票。如果公司估值上涨，员工可以通过行权并出售获得收益。"},
            {"q": "行权收益怎么算？", "a": "行权收益 = (当前股价 - 行权价) × 期权数量 - 行权成本。行权后还需缴纳个人所得税（通常按工资薪金所得计税，税率取决于收入档次）。本工具自动计算税前和税后收益。"},
            {"q": "归属期是什么？", "a": "归属期（vesting）是指员工需要等待才能获得期权的时间。常见方案是4年归属、1年悬崖期（cliff）：满1年获得25%，之后每月归属剩余部分。本工具支持自定义归属方案。"},
            {"q": "行权后什么时候可以卖出？", "a": "取决于公司政策：上市公司通常行权后可立即卖出（注意禁售期）；未上市公司需要等IPO、并购或其他流动性事件才能变现。本工具可模拟不同退出场景。"},
            {"q": "ESOP有哪些税务考虑？", "a": "行权时：行权收益通常按工资薪金纳税。卖出时：卖出价与行权日市价的差额按资本利得纳税。不同国家税务政策差异较大，建议咨询税务顾问。"},
        ],
        "en_faq": [
            {"q": "What is ESOP?", "a": "ESOP (Employee Stock Option Plan) grants employees the right to buy company shares at a preset price (strike price). If the company value increases, employees profit by exercising and selling."},
            {"q": "How is exercise profit calculated?", "a": "Exercise profit = (Current price - Strike price) × Number of options - Exercise cost. After exercise, income tax applies (typically at ordinary income rates). This tool computes pre-tax and post-tax gains."},
            {"q": "What is a vesting schedule?", "a": "Vesting determines when options become exercisable. Common: 4-year vesting with 1-year cliff — 25% after year 1, remainder monthly. This tool supports custom schedules."},
            {"q": "When can I sell after exercise?", "a": "Public companies: usually immediately (mind lockup periods). Private companies: must wait for IPO, acquisition, or other liquidity events. This tool simulates different exit scenarios."},
            {"q": "What are ESOP tax considerations?", "a": "At exercise: spread typically taxed as ordinary income. At sale: difference from exercise-day price taxed as capital gains. Tax rules vary significantly by country — consult a tax advisor."},
        ],
    },
    "cap-table-calculator": {
        "zh_name": "股权结构表计算器",
        "en_name": "Cap Table Calculator",
        "zh_desc": "免费在线股权结构表（Cap Table）计算器，模拟多轮融资后的股权稀释，计算创始人和投资者的持股比例变化。支持SAFE/可转债转换、期权池预留。纯前端计算，数据安全。",
        "en_desc": "Free online Cap Table calculator. Simulate equity dilution across multiple funding rounds. Calculate founder and investor ownership changes. Supports SAFE/convertible note conversion and option pool reserve. 100% client-side.",
        "zh_keywords": "股权结构表,Cap Table,融资稀释,股权计算,创始人股权",
        "en_keywords": "cap table calculator,equity dilution,funding rounds,founder equity,ownership calculator",
        "category": "金融",
        "en_category": "Finance",
        "faq": [
            {"q": "Cap Table是什么？", "a": "Cap Table（股权结构表）是记录公司股权分配的表格，列出所有股东及其持股数量、比例和股权类型。是融资、并购和上市决策的核心参考文件。"},
            {"q": "融资稀释怎么算？", "a": "新融资轮后，原有股东持股比例 = 原有持股比例 × (1 - 新投资人持股比例)。例如：创始人持有80%，新投资人获得20%，则创始人稀释为80% × 80% = 64%。本工具自动计算每轮稀释效果。"},
            {"q": "什么是期权池？", "a": "期权池（Option Pool）是公司预留用于员工股权激励的股份，通常在融资前设立。期权池的设立也会稀释现有股东。常见的期权池规模为10-20%。"},
            {"q": "SAFE和可转债如何影响股权？", "a": "SAFE（Simple Agreement for Future Equity）和可转债是延迟定价的融资工具。转换时按约定折扣或估值上限计算转换价格。本工具支持设置折扣率和估值上限来模拟转换后的股权结构。"},
            {"q": "如何避免过度稀释？", "a": "1）合理估值融资；2）控制每轮出让比例（建议10-25%）；3）提前规划期权池；4）考虑使用SAFE/可转债延迟定价；5）通过业绩增长提高估值，降低后续稀释。"},
        ],
        "en_faq": [
            {"q": "What is a Cap Table?", "a": "A Cap Table (capitalization table) records company equity ownership — listing all shareholders, their shares, percentages, and equity types. It's central to funding, M&A, and IPO decisions."},
            {"q": "How is dilution calculated?", "a": "After a new round: Old ownership = Previous % × (1 - New investor %). E.g., founder at 80%, new investor takes 20%, founder dilutes to 80% × 80% = 64%. This tool auto-calculates per-round dilution."},
            {"q": "What is an option pool?", "a": "An option pool is shares reserved for employee equity grants, typically created before funding rounds. It dilutes existing shareholders. Common sizes: 10-20%."},
            {"q": "How do SAFEs and convertible notes affect equity?", "a": "SAFEs and convertible notes are deferred-pricing instruments. They convert at a discount or valuation cap. This tool supports discount rates and caps to simulate post-conversion ownership."},
            {"q": "How to avoid excessive dilution?", "a": "1) Raise at fair valuations; 2) Limit per-round dilution to 10-25%; 3) Plan option pools ahead; 4) Use SAFEs/notes to defer pricing; 5) Grow to higher valuations before raising."},
        ],
    },
}

def gen_tool_html(name, info, lang="zh"):
    """生成工具HTML"""
    is_zh = lang == "zh"
    base = f"/{name}/" if is_zh else f"/en/{name}/"
    alt_lang = "en" if is_zh else "zh"
    alt_base = f"/en/{name}/" if is_zh else f"/{name}/"
    site_url = "https://free-toolbase.com"
    
    tool_title = info["zh_name"] if is_zh else info["en_name"]
    tool_desc = info["zh_desc"] if is_zh else info["en_desc"]
    keywords = info["zh_keywords"] if is_zh else info["en_keywords"]
    category = info["category"] if is_zh else info["en_category"]
    faq_list = info["faq"] if is_zh else info["en_faq"]
    
    lang_attr = "zh-CN" if is_zh else "en"
    lang_switch_zh = f'<a href="{site_url}/{name}/" class="{"active" if is_zh else ""}">中文</a>'
    lang_switch_en = f'<a href="{site_url}/en/{name}/" class="{"" if is_zh else "active"}">EN</a>'
    
    faq_json = ",\n    ".join([
        f'''{{
      "@type": "Question",
      "name": "{f['q']}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{f['a']}"
      }}
    }}''' for f in faq_list
    ])
    
    breadcrumb_name = tool_title
    home_name = "首页" if is_zh else "Home"
    tools_name = "工具" if is_zh else "Tools"
    home_url = site_url + "/" if is_zh else site_url + "/en/"
    tools_url = site_url + "/#tools" if is_zh else site_url + "/en/#tools"
    
    # 根据工具类型生成具体的HTML内容
    tool_body = generate_tool_body(name, info, is_zh)
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{tool_desc}">
<meta name="keywords" content="{keywords}">
<title>{tool_title} - Free ToolBase</title>
<link rel="canonical" href="{site_url}{base}">
<meta property="og:title" content="{tool_title} - Free ToolBase">
<meta property="og:description" content="{tool_desc}">
<meta property="og:url" content="{site_url}{base}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{'zh' if is_zh else 'en'}" href="{site_url}{base}">
<link rel="alternate" hreflang="{'en' if is_zh else 'zh'}" href="{site_url}{alt_base}">
<link rel="alternate" hreflang="x-default" href="{site_url}/en/{name}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{tool_title}", "description": "{tool_desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_json}
  ]
}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "{'如何使用' if is_zh else 'How to use'} {tool_title}", "description": "{'使用说明' if is_zh else 'Step-by-step guide'}", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{tool_title}"}}, "step": [{{"@type": "HowToStep", "position": 1, "name": "{'输入数据' if is_zh else 'Enter data'}", "text": "{'在输入框中输入需要计算的数值' if is_zh else 'Enter your values in the input fields'}"}}, {{"@type": "HowToStep", "position": 2, "name": "{'选择选项' if is_zh else 'Select options'}", "text": "{'根据需要选择计算模式或参数' if is_zh else 'Choose calculation mode and parameters'}"}}, {{"@type": "HowToStep", "position": 3, "name": "{'点击计算' if is_zh else 'Calculate'}", "text": "{'点击计算按钮获取结果' if is_zh else 'Click calculate to see results'}"}}, {{"@type": "HowToStep", "position": 4, "name": "{'查看结果' if is_zh else 'View results'}", "text": "{'查看计算结果，支持一键复制' if is_zh else 'View results with one-click copy'}"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "{home_name}", "item": "{home_url}"}}, {{"@type": "ListItem", "position": 2, "name": "{tools_name}", "item": "{tools_url}"}}, {{"@type": "ListItem", "position": 3, "name": "{tool_title}", "item": "{site_url}{base}"}}]}}</script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}.header h1{{font-size:1.5rem;color:#f1c40f}}.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:24px;margin-bottom:24px}}@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}}}.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}.form-group{{margin-bottom:14px}}.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}.form-row{{display:flex;gap:12px;flex-wrap:wrap}}.form-row .form-group{{flex:1;min-width:140px}}.btn{{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;font-weight:500;cursor:pointer;transition:all .2s;color:#fff}}.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0ea5e9)}}.btn-primary:hover{{background:linear-gradient(135deg,#0891b2,#0284c7);transform:translateY(-1px)}}.btn-secondary{{background:rgba(148,163,184,.15);color:#94a3b8}}.btn-secondary:hover{{background:rgba(148,163,184,.25)}}.btn-sm{{padding:6px 12px;font-size:.8rem}}.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}.result-card{{background:#0f172a;border-radius:10px;padding:16px;margin-bottom:12px;border:1px solid rgba(148,163,184,.1)}}.result-card .label{{font-size:.8rem;color:#64748b;margin-bottom:4px}}.result-card .value{{font-size:1.5rem;font-weight:700;color:#22d3ee}}.result-card .range{{font-size:.75rem;color:#64748b;margin-top:2px}}.info-tip{{background:rgba(6,182,212,.08);border-left:3px solid #06b6d4;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:16px;font-size:.85rem;color:#94a3b8}}.sidebar .section{{position:sticky;top:24px}}.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;z-index:9999;box-shadow:0 8px 32px rgba(0,0,0,.4);opacity:0;transition:opacity .3s;pointer-events:none;border:1px solid rgba(148,163,184,.2)}}.toast.show{{opacity:1}}footer{{text-align:center;color:#64748b;font-size:.8rem;padding:32px 16px;border-top:1px solid rgba(148,163,184,.1);margin-top:24px}}footer a{{color:#64748b}}table{{width:100%;border-collapse:collapse;margin-top:12px;font-size:.85rem}}th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid rgba(148,163,184,.1)}}th{{color:#64748b;font-weight:500;font-size:.8rem}}td{{color:#e2e8f0}}.highlight{{color:#22d3ee;font-weight:600}}</style>
</head>
<body>
<div class="container">
<header class="header">
<h1>{tool_title}</h1>
<div class="lang-switch">{lang_switch_zh}{lang_switch_en}</div>
</header>
<nav class="nav-back"><a href="{site_url}/{'en/' if not is_zh else ''}">← {'Back to Home' if not is_zh else '返回首页'}</a> | <a href="{site_url}/{'en/' if not is_zh else ''}#tools">{'All Tools' if not is_zh else '全部工具'}</a></nav>
<div class="hero">
<div class="badge">{category}</div>
<p>{tool_desc}</p>
</div>
{tool_body}
<footer><p>© 2025 Free ToolBase · {'All calculations are performed locally in your browser. No data is uploaded to any server.' if not is_zh else '所有计算均在浏览器本地完成，数据不会上传至任何服务器。'}</p></footer>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
function copyText(text){{if(navigator.clipboard){{navigator.clipboard.writeText(text).then(function(){{showToast('{'Copied!' if not is_zh else '已复制！'}');}});}}else{{var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);showToast('{'Copied!' if not is_zh else '已复制！'}');}}}}
</script>
</body>
</html>'''
    return html


def generate_tool_body(name, info, is_zh):
    """生成工具特定的body内容"""
    if name == "fertility-calculator":
        return generate_fertility_body(is_zh)
    elif name == "epf-calculator":
        return generate_epf_body(is_zh)
    elif name == "fixed-deposit-calculator":
        return generate_fd_body(is_zh)
    elif name == "esop-calculator":
        return generate_esop_body(is_zh)
    elif name == "cap-table-calculator":
        return generate_captable_body(is_zh)
    return ""

def generate_fertility_body(is_zh):
    L = lambda zh, en: zh if is_zh else en
    return f'''<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>{L('📅 输入信息', '📅 Enter Information')}</h2>
<div class="form-row">
<div class="form-group"><label>{L('末次月经日期', 'Last Period Date')}</label><input type="date" id="lmpDate"></div>
<div class="form-group"><label>{L('月经周期（天）', 'Cycle Length (days)')}</label><input type="number" id="cycleLen" value="28" min="20" max="45"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('经期持续（天）', 'Period Duration (days)')}</label><input type="number" id="periodLen" value="5" min="2" max="10"></div>
<div class="form-group"><label>{L('黄体期（天）', 'Luteal Phase (days)')}</label><input type="number" id="lutealPhase" value="14" min="10" max="16"><span style="font-size:.75rem;color:#64748b">{L('（默认14天）', '(default 14)')}</span></div>
</div>
<div class="btn-group"><button class="btn btn-primary" onclick="calculate()">{L('🔍 计算排卵期', '🔍 Calculate')}</button><button class="btn btn-secondary" onclick="resetForm()">{L('🔄 重置', '🔄 Reset')}</button></div>
</div>
<div class="section" id="resultSection" style="display:none">
<h2>{L('📊 计算结果', '📊 Results')}</h2>
<div class="form-row">
<div class="result-card" style="flex:1"><div class="label">{L('预计排卵日', 'Predicted Ovulation')}</div><div class="value" id="ovDay">-</div><div class="range" id="cycleDay"></div></div>
<div class="result-card" style="flex:1"><div class="label">{L('易孕期开始', 'Fertile Window Starts')}</div><div class="value" id="fwStart">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('易孕期结束', 'Fertile Window Ends')}</div><div class="value" id="fwEnd">-</div></div>
</div>
<div class="form-row" style="margin-top:12px">
<div class="result-card" style="flex:1"><div class="label">{L('下次月经', 'Next Period')}</div><div class="value" id="nextPeriod">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('预产期（如受孕）', 'Due Date (if conceived)')}</div><div class="value" id="dueDate">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('最佳同房日', 'Best Days')}</div><div class="value" id="bestDays" style="font-size:1rem">-</div></div>
</div>
<div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="copyResults()">{L('📋 复制结果', '📋 Copy Results')}</button></div>
</div>
<div class="section">
<h2>{L('🗓️ 周期日历', '🗓️ Cycle Calendar')}</h2>
<div id="calendar" style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;font-size:.8rem;text-align:center"></div>
<div style="display:flex;gap:16px;margin-top:12px;font-size:.75rem;flex-wrap:wrap">
<span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;border-radius:3px;background:#ef4444;display:inline-block"></span>{L('经期', 'Period')}</span>
<span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;border-radius:3px;background:#22c55e;display:inline-block"></span>{L('易孕期', 'Fertile')}</span>
<span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;border-radius:3px;background:#f59e0b;display:inline-block"></span>{L('排卵日', 'Ovulation')}</span>
</div>
</div>
</div>
<aside class="sidebar">
<div class="section">
<h2>{L('💡 排卵知识', '💡 Ovulation Facts')}</h2>
<div class="info-tip">{L('排卵通常发生在下次月经前14天。精子可在体内存活3-5天，卵子可存活12-24小时。最佳受孕时间是排卵前1-2天。', 'Ovulation typically occurs 14 days before next period. Sperm survive 3-5 days, egg survives 12-24 hours. Best conception time: 1-2 days before ovulation.')}</div>
<div class="info-tip" style="margin-top:8px">{L('排卵信号：宫颈黏液变清变稀、基础体温升高0.3-0.5°C、轻度下腹痛、乳房胀痛。', 'Signs: clear stretchy mucus, BBT rise 0.3-0.5°C, mild cramping, breast tenderness.')}</div>
</div>
</aside>
</div>
<script>
function calcDate(d, offset){{ var r=new Date(d);r.setDate(r.getDate()+offset);return r;}}
function fmt(d){{ return d.toISOString().split('T')[0];}}
function calculate(){{
var lmp=new Date(document.getElementById('lmpDate').value+'T00:00:00');
var cycle=parseInt(document.getElementById('cycleLen').value)||28;
var luteal=parseInt(document.getElementById('lutealPhase').value)||14;
if(isNaN(lmp.getTime())){{showToast('{L("请选择末次月经日期", "Please select last period date")}');return;}}
var ovDay=calcDate(lmp,cycle-luteal);
var fwStart=calcDate(ovDay,-5);
var fwEnd=calcDate(ovDay,1);
var nextPeriod=calcDate(lmp,cycle);
var dueDate=calcDate(lmp,280);
var bestDay1=calcDate(ovDay,-2);
var bestDay2=calcDate(ovDay,-1);
document.getElementById('ovDay').textContent=fmt(ovDay);
document.getElementById('cycleDay').textContent='{L("周期第", "Cycle Day")} '+(cycle-luteal)+'{L("天", "")}';
document.getElementById('fwStart').textContent=fmt(fwStart);
document.getElementById('fwEnd').textContent=fmt(fwEnd);
document.getElementById('nextPeriod').textContent=fmt(nextPeriod);
document.getElementById('dueDate').textContent=fmt(dueDate);
document.getElementById('bestDays').textContent=fmt(bestDay1)+' ~ '+fmt(bestDay2);
document.getElementById('resultSection').style.display='block';
renderCalendar(lmp,cycle,luteal,parseInt(document.getElementById('periodLen').value)||5);
}}
function renderCalendar(lmp,cycle,luteal,periodLen){{
var cal=document.getElementById('calendar');
var start=new Date(lmp);start.setDate(start.getDate()-start.getDay());
var html='<div style="color:#64748b;font-weight:500">{"Sun" if not is_zh else "日"}</div><div style="color:#64748b;font-weight:500">{"Mon" if not is_zh else "一"}</div><div style="color:#64748b;font-weight:500">{"Tue" if not is_zh else "二"}</div><div style="color:#64748b;font-weight:500">{"Wed" if not is_zh else "三"}</div><div style="color:#64748b;font-weight:500">{"Thu" if not is_zh else "四"}</div><div style="color:#64748b;font-weight:500">{"Fri" if not is_zh else "五"}</div><div style="color:#64748b;font-weight:500">{"Sat" if not is_zh else "六"}</div>';
var ovDay=new Date(lmp);ovDay.setDate(ovDay.getDate()+cycle-luteal);
var periodEnd=new Date(lmp);periodEnd.setDate(periodEnd.getDate()+periodLen-1);
var fwStartD=new Date(ovDay);fwStartD.setDate(fwStartD.getDate()-5);
var nextPeriodD=new Date(lmp);nextPeriodD.setDate(nextPeriodD.getDate()+cycle);
for(var i=0;i<42;i++){{
var d=new Date(start);d.setDate(d.getDate()+i);
var cls='';var label=d.getDate();
var t=d.getTime();
if(t>=lmp.getTime()&&t<=periodEnd.getTime())cls='background:#ef4444;color:#fff';
else if(t>=fwStartD.getTime()&&t<=ovDay.getTime())cls='background:rgba(34,197,94,.2);color:#22c55e';
if(t===ovDay.getTime())cls='background:#f59e0b;color:#000;font-weight:700';
if(t>=nextPeriodD.getTime()&&t<new Date(nextPeriodD).setDate(nextPeriodD.getDate()+periodLen))cls='background:rgba(239,68,68,.3);color:#ef4444';
html+='<div style="padding:6px 2px;border-radius:4px;'+cls+'">'+label+'</div>';
}}
cal.innerHTML=html;
}}
function resetForm(){{document.getElementById('lmpDate').value='';document.getElementById('cycleLen').value='28';document.getElementById('periodLen').value='5';document.getElementById('lutealPhase').value='14';document.getElementById('resultSection').style.display='none';document.getElementById('calendar').innerHTML='';}}
function copyResults(){{var r=document.getElementById('resultSection');var txt='';r.querySelectorAll('.result-card').forEach(function(c){{var l=c.querySelector('.label');var v=c.querySelector('.value');if(l&&v)txt+=l.textContent+': '+v.textContent+'\\n';}});copyText(txt);}}
</script>'''

def generate_epf_body(is_zh):
    L = lambda zh, en: zh if is_zh else en
    return f'''<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>{L('💰 输入参数', '💰 Input Parameters')}</h2>
<div class="form-row">
<div class="form-group"><label>{L('月薪', 'Monthly Salary')} ({L('元', '$')})</label><input type="number" id="salary" value="5000" min="0"></div>
<div class="form-group"><label>{L('当前EPF余额', 'Current EPF Balance')} ({L('元', '$')})</label><input type="number" id="currentBalance" value="0" min="0"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('雇员缴款比例 (%)', 'Employee Contribution (%)')}</label><input type="number" id="eeRate" value="11" min="0" max="100" step="0.1"></div>
<div class="form-group"><label>{L('雇主缴款比例 (%)', 'Employer Contribution (%)')}</label><input type="number" id="erRate" value="12" min="0" max="100" step="0.1"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('年利率 (%)', 'Annual Interest Rate (%)')}</label><input type="number" id="interestRate" value="5.5" min="0" max="20" step="0.1"></div>
<div class="form-group"><label>{L('剩余工作年限', 'Years Until Retirement')}</label><input type="number" id="years" value="30" min="1" max="60"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('预计年薪增长 (%)', 'Annual Salary Growth (%)')}</label><input type="number" id="salaryGrowth" value="3" min="0" max="20" step="0.1"></div>
<div class="form-group"><label>{L('额外自愿缴款/月', 'Extra Voluntary Contribution/Mo')} ({L('元', '$')})</label><input type="number" id="extraContribution" value="0" min="0"></div>
</div>
<div class="btn-group"><button class="btn btn-primary" onclick="calculate()">{L('🔍 计算', '🔍 Calculate')}</button><button class="btn btn-secondary" onclick="resetForm()">{L('🔄 重置', '🔄 Reset')}</button></div>
</div>
<div class="section" id="resultSection" style="display:none">
<h2>{L('📊 计算结果', '📊 Results')}</h2>
<div class="form-row">
<div class="result-card" style="flex:1"><div class="label">{L('退休时EPF总额', 'Total EPF at Retirement')}</div><div class="value" id="totalEPF">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('总缴款额', 'Total Contributions')}</div><div class="value" id="totalContrib" style="font-size:1.2rem">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('总利息收入', 'Total Interest Earned')}</div><div class="value" id="totalInterest" style="font-size:1.2rem">-</div></div>
</div>
<div class="info-tip" style="margin-top:12px">{L('退休后每月可提取（假设分20年领取）：', 'Monthly withdrawal over 20 years post-retirement:')} <strong id="monthlyWithdrawal" style="color:#22d3ee">-</strong></div>
<div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="copyResults()">{L('📋 复制结果', '📋 Copy Results')}</button></div>
</div>
<div class="section">
<h2>{L('📈 逐年增长表', '📈 Year-by-Year Growth')}</h2>
<div style="max-height:300px;overflow-y:auto"><table id="yearTable"><thead><tr><th>{L('年份', 'Year')}</th><th>{L('年薪', 'Annual Salary')}</th><th>{L('年缴款', 'Annual Contribution')}</th><th>{L('年终余额', 'Year-End Balance')}</th></tr></thead><tbody></tbody></table></div>
</div>
</div>
<aside class="sidebar">
<div class="section">
<h2>{L('💡 EPF知识', '💡 EPF Facts')}</h2>
<div class="info-tip">{L('EPF（雇员公积金）是强制退休储蓄计划。雇员和雇主每月缴款，账户享有利息。马来西亚2024年EPF利率约5.5%。', 'EPF is a mandatory retirement savings scheme. Both employee and employer contribute monthly with guaranteed interest. Malaysia EPF rate ~5.5% for 2024.')}</div>
<div class="info-tip" style="margin-top:8px">{L('复利效应：早期缴款比晚期缴款价值高得多。30岁开始vs 40岁开始，最终余额可能相差一倍以上。', 'Compound effect: early contributions are far more valuable. Starting at 30 vs 40 can more than double your final balance.')}</div>
</div>
</aside>
</div>
<script>
function fmtNum(n){{return n.toLocaleString('{"en-US" if not is_zh else "en-US"}',{{minimumFractionDigits:2,maximumFractionDigits:2}});}}
function calculate(){{
var salary=parseFloat(document.getElementById('salary').value)||0;
var balance=parseFloat(document.getElementById('currentBalance').value)||0;
var eeRate=parseFloat(document.getElementById('eeRate').value)/100||0;
var erRate=parseFloat(document.getElementById('erRate').value)/100||0;
var intRate=parseFloat(document.getElementById('interestRate').value)/100||0;
var years=parseInt(document.getElementById('years').value)||0;
var growth=parseFloat(document.getElementById('salaryGrowth').value)/100||0;
var extra=parseFloat(document.getElementById('extraContribution').value)||0;
if(salary<=0||years<=0){{showToast('{L("请输入有效参数", "Please enter valid parameters")}');return;}}
var total=balance;var totalContrib=0;var rows='';
var monthlyRate=intRate/12;
for(var y=1;y<=years;y++){{
var yrSalary=salary*12*Math.pow(1+growth,y-1);
var yrContrib=yrSalary*(eeRate+erRate)+extra*12;
totalContrib+=yrContrib;
total=(total+yrContrib)*(1+intRate);
rows+='<tr><td>'+y+'</td><td>'+fmtNum(yrSalary)+'</td><td>'+fmtNum(yrContrib)+'</td><td>'+fmtNum(total)+'</td></tr>';
}}
document.getElementById('totalEPF').textContent=fmtNum(total);
document.getElementById('totalContrib').textContent=fmtNum(totalContrib);
document.getElementById('totalInterest').textContent=fmtNum(total-totalContrib-balance);
document.getElementById('monthlyWithdrawal').textContent=fmtNum(total/240);
document.getElementById('yearTable').querySelector('tbody').innerHTML=rows;
document.getElementById('resultSection').style.display='block';
}}
function resetForm(){{document.getElementById('salary').value='5000';document.getElementById('currentBalance').value='0';document.getElementById('eeRate').value='11';document.getElementById('erRate').value='12';document.getElementById('interestRate').value='5.5';document.getElementById('years').value='30';document.getElementById('salaryGrowth').value='3';document.getElementById('extraContribution').value='0';document.getElementById('resultSection').style.display='none';document.getElementById('yearTable').querySelector('tbody').innerHTML='';}}
function copyResults(){{var r=document.getElementById('resultSection');var txt='';r.querySelectorAll('.result-card').forEach(function(c){{var l=c.querySelector('.label');var v=c.querySelector('.value');if(l&&v)txt+=l.textContent+': '+v.textContent+'\\n';}});copyText(txt);}}
</script>'''

def generate_fd_body(is_zh):
    L = lambda zh, en: zh if is_zh else en
    return f'''<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>{L('💰 输入参数', '💰 Input Parameters')}</h2>
<div class="form-row">
<div class="form-group"><label>{L('本金', 'Principal')} ({L('元', '$')})</label><input type="number" id="principal" value="10000" min="1"></div>
<div class="form-group"><label>{L('年利率 (%)', 'Annual Interest Rate (%)')}</label><input type="number" id="rate" value="5.0" min="0" max="30" step="0.01"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('存款期限（年）', 'Tenure (years)')}</label><input type="number" id="tenure" value="5" min="0.1" max="50" step="0.1"></div>
<div class="form-group"><label>{L('计息方式', 'Interest Mode')}</label><select id="mode"><option value="compound">{L('复利', 'Compound')}</option><option value="simple">{L('单利', 'Simple')}</option></select></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('计息频率', 'Compounding Frequency')}</label><select id="frequency"><option value="12">{L('按月', 'Monthly')}</option><option value="4">{L('按季', 'Quarterly')}</option><option value="2">{L('按半年', 'Semi-Annually')}</option><option value="1">{L('按年', 'Annually')}</option></select></div>
<div class="form-group"><label>{L('税率 (%)', 'Tax Rate (%)')} <span style="font-size:.75rem;color:#64748b">{L('(可选)', '(optional)')}</span></label><input type="number" id="taxRate" value="0" min="0" max="50"></div>
</div>
<div class="btn-group"><button class="btn btn-primary" onclick="calculate()">{L('🔍 计算', '🔍 Calculate')}</button><button class="btn btn-secondary" onclick="resetForm()">{L('🔄 重置', '🔄 Reset')}</button></div>
</div>
<div class="section" id="resultSection" style="display:none">
<h2>{L('📊 计算结果', '📊 Results')}</h2>
<div class="form-row">
<div class="result-card" style="flex:1"><div class="label">{L('到期本息总额', 'Maturity Amount')}</div><div class="value" id="maturityAmount">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('利息收入', 'Interest Earned')}</div><div class="value" id="interestEarned" style="font-size:1.2rem">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('税后净收益', 'Post-Tax Gain')}</div><div class="value" id="postTax" style="font-size:1.2rem">-</div></div>
</div>
<div class="form-row" style="margin-top:12px">
<div class="result-card" style="flex:1"><div class="label">{L('实际年化收益率', 'Effective Annual Yield')}</div><div class="value" id="effectiveYield" style="font-size:1.2rem">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('总回报率', 'Total Return')}</div><div class="value" id="totalReturn" style="font-size:1.2rem">-</div></div>
</div>
<div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="copyResults()">{L('📋 复制结果', '📋 Copy Results')}</button></div>
</div>
<div class="section">
<h2>{L('📈 逐年明细', '📈 Year-by-Year Detail')}</h2>
<div style="max-height:300px;overflow-y:auto"><table id="yearTable"><thead><tr><th>{L('年份', 'Year')}</th><th>{L('年初本金', 'Opening Balance')}</th><th>{L('年利息', 'Year Interest')}</th><th>{L('年末余额', 'Closing Balance')}</th></tr></thead><tbody></tbody></table></div>
</div>
</div>
<aside class="sidebar">
<div class="section">
<h2>{L('💡 存款技巧', '💡 Deposit Tips')}</h2>
<div class="info-tip">{L('复利效应：按月复利比按年复利多约0.1-0.2%的实际年化收益。计息越频繁，收益越高。', 'Compound effect: monthly compounding yields ~0.1-0.2% more effective annual return than annual. More frequent = more gains.')}</div>
<div class="info-tip" style="margin-top:8px">{L('梯次存款策略：将大额存款分成多笔不同期限，既保持流动性又享受高利率。例如：将10万分成1年/2年/3年/4年/5年各2万。', 'Ladder strategy: split large deposits into multiple tenures for liquidity + high rates. E.g., split 100k into 1/2/3/4/5-year deposits of 20k each.')}</div>
</div>
</aside>
</div>
<script>
function fmtNum(n){{return n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}});}}
function fmtPct(n){{return n.toFixed(2)+'%';}}
function calculate(){{
var p=parseFloat(document.getElementById('principal').value)||0;
var r=parseFloat(document.getElementById('rate').value)/100||0;
var t=parseFloat(document.getElementById('tenure').value)||0;
var mode=document.getElementById('mode').value;
var freq=parseInt(document.getElementById('frequency').value)||1;
var tax=parseFloat(document.getElementById('taxRate').value)/100||0;
if(p<=0||t<=0){{showToast('{L("请输入有效参数", "Please enter valid parameters")}');return;}}
var maturity,interest,rows='',balance=p;
if(mode==='simple'){{
interest=p*r*t;
maturity=p+interest;
for(var y=1;y<=Math.ceil(t);y++){{
var yrInt=p*r;
rows+='<tr><td>'+y+'</td><td>'+fmtNum(p)+'</td><td>'+fmtNum(yrInt)+'</td><td>'+fmtNum(p+yrInt*y)+'</td></tr>';
}}
}}else{{
maturity=p*Math.pow(1+r/freq,freq*t);
interest=maturity-p;
for(var y=1;y<=Math.ceil(t);y++){{
var yrEnd=p*Math.pow(1+r/freq,freq*y);
var yrInt=yrEnd-balance;
rows+='<tr><td>'+y+'</td><td>'+fmtNum(balance)+'</td><td>'+fmtNum(yrInt)+'</td><td>'+fmtNum(yrEnd)+'</td></tr>';
balance=yrEnd;
}}
}}
var postTax=interest*(1-tax);
var effYield=(Math.pow(maturity/p,1/t)-1)*100;
var totalReturn=((maturity-p)/p)*100;
document.getElementById('maturityAmount').textContent=fmtNum(maturity);
document.getElementById('interestEarned').textContent=fmtNum(interest);
document.getElementById('postTax').textContent=fmtNum(postTax);
document.getElementById('effectiveYield').textContent=fmtPct(effYield);
document.getElementById('totalReturn').textContent=fmtPct(totalReturn);
document.getElementById('yearTable').querySelector('tbody').innerHTML=rows;
document.getElementById('resultSection').style.display='block';
}}
function resetForm(){{document.getElementById('principal').value='10000';document.getElementById('rate').value='5.0';document.getElementById('tenure').value='5';document.getElementById('mode').value='compound';document.getElementById('frequency').value='12';document.getElementById('taxRate').value='0';document.getElementById('resultSection').style.display='none';document.getElementById('yearTable').querySelector('tbody').innerHTML='';}}
function copyResults(){{var r=document.getElementById('resultSection');var txt='';r.querySelectorAll('.result-card').forEach(function(c){{var l=c.querySelector('.label');var v=c.querySelector('.value');if(l&&v)txt+=l.textContent+': '+v.textContent+'\\n';}});copyText(txt);}}
</script>'''

def generate_esop_body(is_zh):
    L = lambda zh, en: zh if is_zh else en
    return f'''<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>{L('📋 输入参数', '📋 Input Parameters')}</h2>
<div class="form-row">
<div class="form-group"><label>{L('期权数量', 'Number of Options')}</label><input type="number" id="numOptions" value="10000" min="1"></div>
<div class="form-group"><label>{L('行权价', 'Strike Price')} ({L('元/股', '$/share')})</label><input type="number" id="strikePrice" value="1.00" min="0" step="0.01"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('当前公允股价', 'Current FMV per Share')} ({L('元', '$')})</label><input type="number" id="currentPrice" value="10.00" min="0" step="0.01"></div>
<div class="form-group"><label>{L('预计退出股价', 'Expected Exit Price')} ({L('元', '$')})</label><input type="number" id="exitPrice" value="50.00" min="0" step="0.01"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('已归属比例 (%)', 'Vested (%)')}</label><input type="number" id="vestedPct" value="100" min="0" max="100"></div>
<div class="form-group"><label>{L('行权税率 (%)', 'Exercise Tax Rate (%)')}</label><input type="number" id="taxRate" value="30" min="0" max="60"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('资本利得税率 (%)', 'Capital Gains Tax (%)')}</label><input type="number" id="cgTaxRate" value="20" min="0" max="60"></div>
<div class="form-group"><label>{L('行权成本', 'Exercise Cost')} ({L('元', '$')})</label><input type="number" id="exerciseCost" value="0" min="0"></div>
</div>
<div class="btn-group"><button class="btn btn-primary" onclick="calculate()">{L('🔍 计算', '🔍 Calculate')}</button><button class="btn btn-secondary" onclick="resetForm()">{L('🔄 重置', '🔄 Reset')}</button></div>
</div>
<div class="section" id="resultSection" style="display:none">
<h2>{L('📊 计算结果', '📊 Results')}</h2>
<div class="form-row">
<div class="result-card" style="flex:1"><div class="label">{L('当前行权收益（税前）', 'Pre-Tax Exercise Profit')}</div><div class="value" id="preTaxProfit">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('当前行权净收益（税后）', 'Post-Tax Exercise Profit')}</div><div class="value" id="postTaxProfit">-</div></div>
</div>
<div class="form-row" style="margin-top:12px">
<div class="result-card" style="flex:1"><div class="label">{L('退出总收益（税前）', 'Pre-Tax Exit Profit')}</div><div class="value" id="exitPreTax">-</div></div>
<div class="result-card" style="flex:1"><div class="label">{L('退出净收益（税后）', 'Post-Tax Exit Net')}</div><div class="value" id="exitPostTax">-</div></div>
</div>
<div class="info-tip" style="margin-top:12px">{L('行权总成本（行权价+费用）：', 'Total exercise cost (strike + fees): ')} <strong id="totalExerciseCost" style="color:#22d3ee">-</strong></div>
<div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="copyResults()">{L('📋 复制结果', '📋 Copy Results')}</button></div>
</div>
</div>
<aside class="sidebar">
<div class="section">
<h2>{L('💡 ESOP须知', '💡 ESOP Tips')}</h2>
<div class="info-tip">{L('行权价是你购买股票的价格，公允股价是公司当前估值对应的股价。行权收益 = (公允股价 - 行权价) × 期权数量。', 'Strike = price you pay. FMV = current fair value. Exercise profit = (FMV - strike) × options.')}</div>
<div class="info-tip" style="margin-top:8px">{L('税务注意：行权时差价通常按工资薪金纳税，卖出时按资本利得纳税。不同国家差异大，建议咨询税务顾问。', 'Tax note: Exercise spread usually taxed as ordinary income. Sale gains taxed as capital gains. Rules vary — consult a tax advisor.')}</div>
</div>
</aside>
</div>
<script>
function fmtNum(n){{return n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}});}}
function calculate(){{
var num=parseFloat(document.getElementById('numOptions').value)||0;
var strike=parseFloat(document.getElementById('strikePrice').value)||0;
var current=parseFloat(document.getElementById('currentPrice').value)||0;
var exit=parseFloat(document.getElementById('exitPrice').value)||0;
var vpct=parseFloat(document.getElementById('vestedPct').value)/100||0;
var tax=parseFloat(document.getElementById('taxRate').value)/100||0;
var cgTax=parseFloat(document.getElementById('cgTaxRate').value)/100||0;
var excost=parseFloat(document.getElementById('exerciseCost').value)||0;
if(num<=0||current<=0){{showToast('{L("请输入有效参数", "Please enter valid parameters")}');return;}}
var vested=num*vpct;
var totalStrikeCost=vested*strike+excost;
var preTaxProfit=vested*(current-strike)-excost;
var postTaxProfit=preTaxProfit*(1-tax);
var exitPreTax=vested*(exit-strike)-excost;
var exitPostTax=(exitPreTax - vested*(exit-current)*cgTax);
document.getElementById('preTaxProfit').textContent=fmtNum(preTaxProfit);
document.getElementById('postTaxProfit').textContent=fmtNum(postTaxProfit);
document.getElementById('exitPreTax').textContent=fmtNum(exitPreTax);
document.getElementById('exitPostTax').textContent=fmtNum(exitPostTax);
document.getElementById('totalExerciseCost').textContent=fmtNum(totalStrikeCost);
document.getElementById('resultSection').style.display='block';
}}
function resetForm(){{document.getElementById('numOptions').value='10000';document.getElementById('strikePrice').value='1.00';document.getElementById('currentPrice').value='10.00';document.getElementById('exitPrice').value='50.00';document.getElementById('vestedPct').value='100';document.getElementById('taxRate').value='30';document.getElementById('cgTaxRate').value='20';document.getElementById('exerciseCost').value='0';document.getElementById('resultSection').style.display='none';}}
function copyResults(){{var r=document.getElementById('resultSection');var txt='';r.querySelectorAll('.result-card').forEach(function(c){{var l=c.querySelector('.label');var v=c.querySelector('.value');if(l&&v)txt+=l.textContent+': '+v.textContent+'\\n';}});copyText(txt);}}
</script>'''

def generate_captable_body(is_zh):
    L = lambda zh, en: zh if is_zh else en
    return f'''<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>{L('🏢 公司基本信息', '🏢 Company Basics')}</h2>
<div class="form-row">
<div class="form-group"><label>{L('总股数', 'Total Shares')}</label><input type="number" id="totalShares" value="10000000" min="1"></div>
<div class="form-group"><label>{L('创始人持股 (%)', 'Founder Ownership (%)')}</label><input type="number" id="founderPct" value="80" min="0" max="100"></div>
</div>
<div class="form-row">
<div class="form-group"><label>{L('期权池 (%)', 'Option Pool (%)')}</label><input type="number" id="optionPool" value="10" min="0" max="50"></div>
<div class="form-group"><label>{L('其他股东 (%)', 'Others (%)')}</label><input type="number" id="othersPct" value="10" min="0" max="100"></div>
</div>
</div>
<div class="section">
<h2>{L('💰 融资轮次', '💰 Funding Rounds')}</h2>
<div id="rounds">
<div class="form-row" style="margin-bottom:8px">
<div class="form-group" style="flex:1"><label>{L('轮次名称', 'Round Name')}</label><input type="text" class="roundName" value="{L('种子轮', 'Seed')}" style="font-size:.85rem"></div>
<div class="form-group" style="flex:1"><label>{L('投资金额', 'Investment')} ({L('万', 'K')})</label><input type="number" class="roundAmount" value="500" min="0" style="font-size:.85rem"></div>
<div class="form-group" style="flex:1"><label>{L('投前估值', 'Pre-Money')} ({L('万', 'K')})</label><input type="number" class="roundPreMoney" value="4000" min="0" style="font-size:.85rem"></div>
</div>
<div class="form-row" style="margin-bottom:8px">
<div class="form-group" style="flex:1"><label>{L('轮次名称', 'Round Name')}</label><input type="text" class="roundName" value="{L('A轮', 'Series A')}" style="font-size:.85rem"></div>
<div class="form-group" style="flex:1"><label>{L('投资金额', 'Investment')} ({L('万', 'K')})</label><input type="number" class="roundAmount" value="2000" min="0" style="font-size:.85rem"></div>
<div class="form-group" style="flex:1"><label>{L('投前估值', 'Pre-Money')} ({L('万', 'K')})</label><input type="number" class="roundPreMoney" value="15000" min="0" style="font-size:.85rem"></div>
</div>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="calculate()">{L('🔍 计算稀释', '🔍 Calculate Dilution')}</button>
<button class="btn btn-secondary" onclick="addRound()">{L('➕ 添加轮次', '➕ Add Round')}</button>
<button class="btn btn-secondary" onclick="resetForm()">{L('🔄 重置', '🔄 Reset')}</button>
</div>
</div>
<div class="section" id="resultSection" style="display:none">
<h2>{L('📊 稀释结果', '📊 Dilution Results')}</h2>
<table id="capTable"><thead><tr><th>{L('股东', 'Shareholder')}</th><th>{L('初始', 'Initial')}</th><th id="roundHeaders"></th><th>{L('最终', 'Final')}</th></tr></thead><tbody></tbody></table>
<div class="info-tip" style="margin-top:12px">{L('每轮融资后，原有股东按比例被稀释。新投资人获得投后估值对应的股份 = 投资金额 / 投后估值。', 'After each round, existing shareholders are diluted proportionally. New investors get post-money ownership = Investment / Post-money valuation.')}</div>
<div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="copyResults()">{L('📋 复制结果', '📋 Copy Results')}</button></div>
</div>
</div>
<aside class="sidebar">
<div class="section">
<h2>{L('💡 股权知识', '💡 Equity Tips')}</h2>
<div class="info-tip">{L('投后估值 = 投前估值 + 投资金额。新投资人持股 = 投资金额 / 投后估值。', 'Post-money = Pre-money + Investment. New investor % = Investment / Post-money.')}</div>
<div class="info-tip" style="margin-top:8px">{L('每轮融资建议出让10-25%，过多稀释会影响创始人控制权和积极性。期权池通常在融资前设立，避免只让现有股东承担稀释。', 'Target 10-25% dilution per round. Too much dilution hurts founder control. Set option pool before funding to share dilution with new investors.')}</div>
</div>
</aside>
</div>
<script>
function fmtPct(n){{return n.toFixed(2)+'%';}}
function calculate(){{
var totalShares=parseFloat(document.getElementById('totalShares').value)||0;
var founderPct=parseFloat(document.getElementById('founderPct').value)/100||0;
var optionPool=parseFloat(document.getElementById('optionPool').value)/100||0;
var othersPct=parseFloat(document.getElementById('othersPct').value)/100||0;
if(totalShares<=0){{showToast('{L("请输入总股数", "Please enter total shares")}');return;}}
var names=document.querySelectorAll('.roundName');
var amounts=document.querySelectorAll('.roundAmount');
var preMoneys=document.querySelectorAll('.roundPreMoney');
var rows=[{{name:'{L("创始人", "Founders")}',pct:founderPct}},{{name:'{L("期权池", "Option Pool")}',pct:optionPool}},{{name:'{L("其他", "Others")}',pct:othersPct}}];
var roundData=[];
for(var i=0;i<names.length;i++){{
var amt=parseFloat(amounts[i].value)||0;
var pre=parseFloat(preMoneys[i].value)||0;
if(amt>0&&pre>0)roundData.push({{name:names[i].value||('Round '+(i+1)),amount:amt,preMoney:pre}});
}}
if(roundData.length===0){{showToast('{L("请至少填写一个有效轮次", "Please fill at least one valid round")}');return;}}
var headerHtml='';
var currentPcts=rows.map(function(r){{return r.pct;}});
var investorPcts=[];
roundData.forEach(function(rd,idx){{
var postMoney=rd.preMoney+rd.amount;
var invPct=rd.amount/postMoney;
investorPcts.push(invPct);
headerHtml+='<th>'+rd.name+'</th>';
for(var j=0;j<currentPcts.length;j++)currentPcts[j]*=(1-invPct);
currentPcts.splice(1,0,invPct);
}});
document.getElementById('roundHeaders').innerHTML=headerHtml;
var bodyHtml='';
var allRows=rows.slice();
roundData.forEach(function(rd,idx){{allRows.splice(1+idx,0,{{name:rd.name,pct:0}});}});
var displayPcts=[];
allRows.forEach(function(r,i){{displayPcts.push(founderPct*(i===0?1:0));}});
// rebuild display
var finalPcts=[];
var tmp=[founderPct,optionPool,othersPct];
roundData.forEach(function(rd,idx){{
var postMoney=rd.preMoney+rd.amount;
var invPct=rd.amount/postMoney;
tmp.splice(1+idx,0,invPct);
for(var j=0;j<tmp.length;j++)if(j!==1+idx)tmp[j]*=(1-invPct);
}});
allRows.forEach(function(r,i){{
var pct=i<tmp.length?tmp[i]:0;
bodyHtml+='<tr><td>'+r.name+'</td><td>'+fmtPct(i<3?[founderPct,optionPool,othersPct][i]:0)+'</td>';
var cur=[founderPct,optionPool,othersPct];
roundData.forEach(function(rd,idx){{
var postMoney=rd.preMoney+rd.amount;
var invPct=rd.amount/postMoney;
cur.splice(1+idx,0,invPct);
for(var j=0;j<cur.length;j++)if(j!==1+idx)cur[j]*=(1-invPct);
var val=i<cur.length?cur[i]:0;
bodyHtml+='<td>'+fmtPct(val)+'</td>';
}});
bodyHtml+='<td style="color:#22d3ee;font-weight:600">'+fmtPct(pct)+'</td></tr>';
}});
document.getElementById('capTable').querySelector('tbody').innerHTML=bodyHtml;
document.getElementById('resultSection').style.display='block';
}}
function addRound(){{
var div=document.getElementById('rounds');
var html='<div class="form-row" style="margin-bottom:8px"><div class="form-group" style="flex:1"><label>{L("轮次名称", "Round Name")}</label><input type="text" class="roundName" value="{L("B轮", "Series B")}" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投资金额", "Investment")} ({L("万", "K")})</label><input type="number" class="roundAmount" value="5000" min="0" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投前估值", "Pre-Money")} ({L("万", "K")})</label><input type="number" class="roundPreMoney" value="40000" min="0" style="font-size:.85rem"></div></div>';
div.insertAdjacentHTML('beforeend',html);
}}
function resetForm(){{document.getElementById('totalShares').value='10000000';document.getElementById('founderPct').value='80';document.getElementById('optionPool').value='10';document.getElementById('othersPct').value='10';document.getElementById('rounds').innerHTML='<div class="form-row" style="margin-bottom:8px"><div class="form-group" style="flex:1"><label>{L("轮次名称", "Round Name")}</label><input type="text" class="roundName" value="{L("种子轮", "Seed")}" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投资金额", "Investment")} ({L("万", "K")})</label><input type="number" class="roundAmount" value="500" min="0" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投前估值", "Pre-Money")} ({L("万", "K")})</label><input type="number" class="roundPreMoney" value="4000" min="0" style="font-size:.85rem"></div></div><div class="form-row" style="margin-bottom:8px"><div class="form-group" style="flex:1"><label>{L("轮次名称", "Round Name")}</label><input type="text" class="roundName" value="{L("A轮", "Series A")}" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投资金额", "Investment")} ({L("万", "K")})</label><input type="number" class="roundAmount" value="2000" min="0" style="font-size:.85rem"></div><div class="form-group" style="flex:1"><label>{L("投前估值", "Pre-Money")} ({L("万", "K")})</label><input type="number" class="roundPreMoney" value="15000" min="0" style="font-size:.85rem"></div></div>';document.getElementById('resultSection').style.display='none';}}
function copyResults(){{var t=document.getElementById('capTable');var txt='';t.querySelectorAll('tr').forEach(function(tr){{var cells=tr.querySelectorAll('th,td');var row=[];cells.forEach(function(c){{row.push(c.textContent);}});txt+=row.join('\\t')+'\\n';}});copyText(txt);}}
</script>'''


# 主流程
for name, info in TOOLS.items():
    # 中文版
    os.makedirs(f"/home/chison/tools-site/{name}", exist_ok=True)
    zh_html = gen_tool_html(name, info, "zh")
    with open(f"/home/chison/tools-site/{name}/index.html", "w") as f:
        f.write(zh_html)
    print(f"✅ {name}/index.html (zh)")
    
    # 英文版
    os.makedirs(f"/home/chison/tools-site/en/{name}", exist_ok=True)
    en_html = gen_tool_html(name, info, "en")
    with open(f"/home/chison/tools-site/en/{name}/index.html", "w") as f:
        f.write(en_html)
    print(f"✅ en/{name}/index.html (en)")

print("\n✅ 全部5个工具生成完毕！")