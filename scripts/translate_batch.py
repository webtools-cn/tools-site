#!/usr/bin/env python3
"""批量翻译工具页面为英文版"""
import re, os

SITE = '/home/chison/tools-site'

tools = [
    'stock-screener-simple',
    'roi-calculator-rental',
    'macro-calculator-advanced',
    'muscle-gain-calculator',
    'expense-split-calculator',
]

translations = {
    # stock-screener-simple
    '股票筛选器 - Free ToolBase': 'Stock Screener - Free ToolBase',
    '免费股票筛选工具，按市盈率、市值、股息率等指标筛选美股，快速找到符合投资策略的股票，无需注册。': 'Free stock screening tool. Filter US stocks by P/E ratio, market cap, dividend yield, and more. Find stocks matching your investment strategy. No signup required.',
    '免费股票筛选工具，按市盈率、市值、股息率等指标筛选美股，快速找到符合投资策略的股票。': 'Free stock screening tool. Filter US stocks by P/E ratio, market cap, dividend yield, and more.',
    '按财务指标筛选美股，快速找到符合投资策略的股票': 'Filter US stocks by financial metrics and find investments matching your strategy',
    '筛选条件': 'Filter Criteria',
    '行业': 'Sector',
    '全部行业': 'All Sectors',
    '科技': 'Technology',
    '金融': 'Financial',
    '医疗健康': 'Healthcare',
    '消费周期': 'Consumer Cyclical',
    '通信': 'Communication',
    '能源': 'Energy',
    '工业': 'Industrial',
    '消费防御': 'Consumer Defensive',
    '房地产': 'Real Estate',
    '公用事业': 'Utilities',
    '基础材料': 'Basic Materials',
    '最大PE比率': 'Max P/E Ratio',
    '最小市值(亿$)': 'Min Market Cap (B$)',
    '最小股息率(%)': 'Min Dividend Yield (%)',
    '最大市净率(PB)': 'Max P/B Ratio',
    '排序方式': 'Sort By',
    '市值 ↓': 'Market Cap ↓',
    'PE比率 ↑': 'P/E Ratio ↑',
    '股息率 ↓': 'Dividend Yield ↓',
    '营收增长 ↓': 'Revenue Growth ↓',
    '🔍 筛选股票': '🔍 Screen Stocks',
    '↺ 重置条件': '↺ Reset',
    '📋 复制结果': '📋 Copy Results',
    '筛选结果': 'Screening Results',
    '代码': 'Ticker',
    '公司名称': 'Company',
    '市值(亿$)': 'Market Cap (B$)',
    '股息率': 'Dividend',
    '营收增长': 'Rev Growth',
    '没有匹配的股票，请放宽筛选条件': 'No matching stocks found. Please relax your filter criteria.',
    '免责声明：股票数据仅供参考，不构成投资建议。数据可能存在延迟。': 'Disclaimer: Stock data is for reference only and does not constitute investment advice. Data may be delayed.',
    '找到': 'Found',
    '只股票': ' stocks',
    '没有结果可复制': 'No results to copy',
    '已复制': 'Copied',
    '条结果': ' results',
    '复制失败': 'Copy failed',
    '股票筛选器': 'Stock Screener',
    '苹果': 'Apple',
    '微软': 'Microsoft',
    '谷歌': 'Google',
    '亚马逊': 'Amazon',
    '英伟达': 'NVIDIA',
    '特斯拉': 'Tesla',
    '伯克希尔': 'Berkshire Hathaway',
    '摩根大通': 'JPMorgan Chase',
    '强生': 'Johnson & Johnson',
    '沃尔玛': 'Walmart',
    '宝洁': 'Procter & Gamble',
    '埃克森美孚': 'Exxon Mobil',
    '联合健康': 'UnitedHealth',
    '家得宝': 'Home Depot',
    '万事达': 'Mastercard',
    '美国银行': 'Bank of America',
    '雪佛龙': 'Chevron',
    '可口可乐': 'Coca-Cola',
    '百事可乐': 'PepsiCo',
    '艾伯维': 'AbbVie',
    '默克': 'Merck',
    '好市多': 'Costco',
    '奈飞': 'Netflix',
    '甲骨文': 'Oracle',
    '英特尔': 'Intel',
    '思科': 'Cisco',
    '迪士尼': 'Disney',
    '富国银行': 'Wells Fargo',
    '赛默飞': 'Thermo Fisher',
    '耐克': 'Nike',
    '卡特彼勒': 'Caterpillar',
    '通用电气': 'GE',
    '波音': 'Boeing',
    'AT&T': 'AT&T',
    'Verizon': 'Verizon',
    '辉瑞': 'Pfizer',
    '杜克能源': 'Duke Energy',
    '南方公司': 'Southern Company',
    '新纪元能源': 'NextEra Energy',
    '安博': 'Prologis',
    '美国铁塔': 'American Tower',
    '自由港': 'Freeport-McMoRan',
    '纽蒙特矿业': 'Newmont',
    '林德': 'Linde',
    'Meta': 'Meta',
    'Visa': 'Visa',
    'Adobe': 'Adobe',
    'Salesforce': 'Salesforce',
    'AMD': 'AMD',

    # roi-calculator-rental
    '租金回报率计算器 - Free ToolBase': 'Rental ROI Calculator - Free ToolBase',
    '免费租金回报率(ROI)计算器，计算房产投资的年回报率、现金回报率、资本化率，助您做出明智的房地产投资决策。': 'Free rental property ROI calculator. Calculate annual return, cash-on-cash return, and cap rate for real estate investments. Make informed property decisions.',
    '免费租金回报率(ROI)计算器，计算房产投资的年回报率、现金回报率、资本化率。': 'Free rental property ROI calculator. Calculate annual return, cash-on-cash return, and cap rate.',
    '计算房产投资的年回报率、现金回报率与资本化率': 'Calculate annual ROI, cash-on-cash return and cap rate for property investments',
    '📋 输入房产信息': '📋 Property Details',
    '购房总价': 'Purchase Price',
    '元（含税费）': ' (incl. taxes & fees)',
    '首付比例': 'Down Payment',
    '月租金收入': 'Monthly Rent',
    '元/月': '/mo',
    '贷款利率': 'Loan Interest Rate',
    '% 年利率': '% APR',
    '贷款期限': 'Loan Term',
    '月物业费+维护费': 'Monthly Expenses',
    '年房产税率': 'Annual Property Tax',
    '% 房价': '% of price',
    '预计年增值率': 'Est. Appreciation',
    '💰 计算回报率': '💰 Calculate ROI',
    '↺ 重置': '↺ Reset',
    '📊 回报率分析': '📊 ROI Analysis',
    '现金回报率': 'Cash on Cash',
    '资本化率': 'Cap Rate',
    '总回报率': 'Total ROI',
    '含增值': 'incl. appreciation',
    '年净现金流': 'Annual Cash Flow',
    '正现金流': 'Positive',
    '负现金流': 'Negative',
    '月供：': 'Monthly Payment: ',
    '/月（等额本息，': '/mo (fixed payment, ',
    '年）': 'yr)',
    '年租金收入：': 'Annual Rent: ',
    '年运营支出：': 'Annual Expenses: ',
    '年房贷总额：': 'Annual Mortgage: ',
    '现金投入（首付）：': 'Cash Invested (Down): ',
    '年增值收益：': 'Annual Appreciation: ',
    '✅ 优质投资：现金回报率超过6%，现金流良好': '✅ Strong Investment: Cash-on-cash over 6%, good cash flow',
    '⚠️ 一般投资：现金回报率3-6%，需关注增值潜力': '⚠️ Moderate Investment: Cash-on-cash 3-6%, watch appreciation',
    '⚡ 低回报：现金回报率低于3%，依赖增值收益': '⚡ Low Return: Cash-on-cash under 3%, relies on appreciation',
    '❌ 负现金流：每月需额外贴钱，风险较高': '❌ Negative Cash Flow: Monthly out-of-pocket, higher risk',
    '请先计算': 'Please calculate first',
    '已复制结果': 'Results copied',
    '免责声明：计算结果仅供参考，不构成投资建议。': 'Disclaimer: Calculations are for reference only and do not constitute investment advice.',
    '租金回报率计算器': 'Rental ROI Calculator',
    '请输入购房总价': 'Please enter purchase price',
    '请输入月租金': 'Please enter monthly rent',
    '请输入有效的首付比例(0-100)': 'Please enter a valid down payment (0-100)',
    '请输入贷款利率': 'Please enter loan interest rate',
    '请输入贷款期限': 'Please enter loan term',
    '请输入月支出': 'Please enter monthly expenses',
    '请输入房产税率': 'Please enter property tax rate',
    '请输入增值率': 'Please enter appreciation rate',
}

def translate_cn_to_en(cn_content, tool_name):
    """简单字符串替换翻译"""
    en = cn_content
    
    # 基础标签替换
    en = en.replace('lang="zh-CN"', 'lang="en"')
    
    # 按字典替换
    for cn, eng in translations.items():
        en = en.replace(cn, eng)
    
    # 修复URL
    en = en.replace(f'href="../favicon.svg"', f'href="../../favicon.svg"')
    en = en.replace(f'href="/"', f'href="/en/"')
    en = en.replace(f'href="/privacy"', f'href="/en/privacy"')
    
    # 修复canonical和hreflang
    en = en.replace(f'https://free-toolbase.com/{tool_name}/', f'https://free-toolbase.com/en/{tool_name}/')
    
    # 修复og:url
    en = re.sub(r'content="https://free-toolbase\.com/' + tool_name + r'/', 
                f'content="https://free-toolbase.com/en/{tool_name}/', en)
    
    # 修复hreflang - zh指向CN, en指向EN
    en = en.replace(f'href="https://free-toolbase.com/{tool_name}/"', f'href="https://free-toolbase.com/en/{tool_name}/"')
    # 需要有一个zh的hreflang指向CN
    if 'hreflang="zh"' not in en:
        en = en.replace('hreflang="x-default"', f'hreflang="zh" href="https://free-toolbase.com/{tool_name}/"')
        # 重新添加x-default指向EN
        en = en.replace('</head>', f'\n<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{tool_name}/">\n</head>')
    
    # 修复BreadcrumbList
    en = en.replace('"name":"首页"', '"name":"Home"')
    en = en.replace('"name":"工具"', '"name":"Tools"')
    en = en.replace('"item":"https://free-toolbase.com/"', '"item":"https://free-toolbase.com/en/"')
    en = en.replace('"item":"https://free-toolbase.com/#tools"', '"item":"https://free-toolbase.com/en/#tools"')
    
    # 修复footer链接
    en = en.replace('>首页<', '>Home<')
    en = en.replace('>隐私政策<', '>Privacy<')
    
    # 修复返回首页链接
    en = en.replace('← 返回首页', '← Back to Home')
    
    # 修复一些常见的中文残留
    en = en.replace('→ 返回首页', '→ Back to Home')
    
    # 修复name字段
    en = re.sub(r'"name":"股票筛选器"', '"name":"Stock Screener"', en)
    en = re.sub(r'"name":"租金回报率计算器"', '"name":"Rental ROI Calculator"', en)
    en = re.sub(r'"name":"高级宏量营养素计算器"', '"name":"Advanced Macro Calculator"', en)
    en = re.sub(r'"name":"增肌计算器"', '"name":"Muscle Gain Calculator"', en)
    en = re.sub(r'"name":"费用分摊计算器"', '"name":"Expense Split Calculator"', en)
    
    return en

for tool in tools:
    cn_path = os.path.join(SITE, tool, 'index.html')
    en_path = os.path.join(SITE, 'en', tool, 'index.html')
    
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_content = f.read()
    
    en_content = translate_cn_to_en(cn_content, tool)
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_content)
    
    print(f'Created: en/{tool}/index.html')

print('Done!')