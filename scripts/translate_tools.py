#!/usr/bin/env python3
"""Translate tool pages CN->EN by replacing Chinese text"""
import os, re

TRANSLATIONS = {
    # Common headers/footers
    '首页': 'Home',
    '全部工具': 'All Tools',
    '联系我们': 'Contact',
    '隐私政策': 'Privacy',
    '服务条款': 'Terms',
    '关于我们': 'About',
    '工具': 'Tools',
    '中文': '中文',
    'EN': 'EN',
    '无需注册 · 数据绝不上传服务器': 'No Sign-up · Data Never Leaves Your Device',
    '零依赖·可离线使用': 'Zero Dependencies · Works Offline',
    '问题反馈:': 'Feedback:',
    '使用教程': 'How to Use',
    '常见问题 FAQ': 'FAQ',
    '计算结果': 'Results',
}

TOOLS_TRANSLATIONS = {
    'ping-tool': {
        '在线Ping工具': 'Online Ping Tool',
        '网络延迟与连通性测试': 'Network Latency & Connectivity Test',
        '免费在线Ping工具，输入域名或IP地址即可检测服务器连通性。支持自定义发包次数和超时时间，实时显示延迟和丢包率。无需安装任何软件，浏览器直接使用。': 'Free online Ping tool. Enter a domain or IP address to test server connectivity. Supports custom packet count and timeout, real-time latency and packet loss display. No installation required.',
        '免费在线Ping工具，输入域名或IP地址即可检测服务器连通性。支持自定义发包次数和超时时间，实时显示延迟和丢包率。': 'Free online Ping tool. Enter a domain or IP address to test server connectivity. Supports custom packet count and timeout.',
        'Ping 测试': 'Ping Test',
        '输入目标域名或IP地址，点击开始测试网络连通性': 'Enter target domain or IP, click to test connectivity',
        '目标地址（域名或IP）': 'Target (Domain or IP)',
        '发包次数': 'Packet Count',
        '超时时间': 'Timeout',
        '开始Ping': 'Start Ping',
        '停止': 'Stop',
        '重置': 'Reset',
        '测试结果': 'Test Results',
        '常用IP/域名速查': 'Common IP/Domain Reference',
        '名称': 'Name',
        '地址': 'Address',
        '说明': 'Description',
        '全球最常用的公共DNS': 'Most popular public DNS worldwide',
        '以隐私保护著称的DNS': 'Privacy-focused DNS',
        '国内常用公共DNS': 'Common public DNS in China',
        '测试国内网络连通性': 'Test domestic network connectivity',
        '在输入框中填写目标域名或IP地址（如': 'Enter target domain or IP (e.g. ',
        '）。': ').',
        '选择发包次数（默认4次）和超时时间（默认2000ms）。': 'Select packet count (default 4) and timeout (default 2000ms).',
        '点击「开始Ping」按钮，实时查看每次发包的延迟时间。': 'Click "Start Ping" to see real-time latency for each packet.',
        '测试完成后自动显示统计结果：最小/最大/平均延迟、丢包率。': 'After completion, statistics are shown: min/max/average latency, packet loss rate.',
        '点击「停止」可中途终止测试，「重置」清空所有结果。': 'Click "Stop" to abort, "Reset" to clear all results.',
        'Ping是什么？有什么用？': 'What is Ping and what is it used for?',
        'Ping是网络诊断工具，用于测试本机与目标服务器之间的连通性。它通过发送ICMP回显请求并等待响应，测量往返时间（延迟）和丢包率。常用于：检测网站是否可达、判断网络故障、评估服务器响应速度。': 'Ping is a network diagnostic tool that tests connectivity between your device and a target server. It sends ICMP echo requests and measures round-trip time (latency) and packet loss. Common uses: checking website availability, diagnosing network issues, evaluating server response.',
        '为什么Ping值很高？': 'Why is my ping so high?',
        '延迟高可能原因：物理距离远（如访问海外服务器）、网络拥堵、目标服务器负载高、ISP路由问题。国内访问海外通常在150-300ms属正常范围，国内互访一般<50ms。': 'High latency causes: physical distance (e.g., overseas servers), network congestion, server load, ISP routing issues. Domestic to overseas: 150-300ms is normal; domestic to domestic: typically <50ms.',
        '丢包率100%怎么办？': 'What if packet loss is 100%?',
        '可能原因：目标服务器禁用了ICMP协议（如某些云服务商默认关闭）、防火墙拦截、域名解析失败、网络彻底断开。建议先检查域名拼写是否正确，或用浏览器访问确认网站是否可达。': 'Possible causes: target server disabled ICMP (common on cloud platforms), firewall blocking, DNS failure, complete network outage. Check domain spelling first, or verify via browser.',
        '在线Ping和命令行Ping有什么区别？': 'What\'s the difference between online and command-line Ping?',
        '命令行Ping直接从你的电脑发送ICMP包，在线Ping从工具站服务器发送。在线Ping适合在没有命令行环境（如手机）或需要从不同地理位置测试时使用。注意：本工具通过Web Worker模拟Ping行为，适合快速连通性检查。': 'Command-line Ping sends ICMP from your device; online Ping sends from our server. Useful when you lack terminal access (e.g., mobile) or need geo-diverse testing. Note: this tool simulates Ping via image loading for quick connectivity checks.',
        '在线Ping工具 | 无需注册 · 数据绝不上传服务器': 'Online Ping Tool | No Sign-up · Data Never Leaves Your Device',
        '请输入目标地址': 'Please enter a target address',
        '请输入有效的域名或IP地址': 'Please enter a valid domain or IP address',
        '来自目标地址的回复': 'Reply from target',
        '请求超时': 'Request timed out',
        '发送': 'Sent',
        '接收': 'Received',
        '丢包率': 'Loss',
        '平均延迟': 'Avg Latency',
        '最小延迟': 'Min',
        '最大延迟': 'Max',
        '个包': 'pkts',
        'Ping统计': 'Ping Statistics',
        '丢失': 'Lost',
        '最短': 'Min',
        '最长': 'Max',
        '平均': 'Avg',
    },
    'percentage-change': {
        '百分比变化计算器': 'Percentage Change Calculator',
        '增长率/降幅在线计算': 'Growth Rate / Decline Calculator',
        '免费在线百分比变化计算器，输入原值和新值，自动计算增长/减少的百分比变化。支持正负增长、反向计算，数据分析和财务报表必备工具。': 'Free online percentage change calculator. Enter original and new values to compute percentage change automatically. Supports positive/negative growth and reverse calculation.',
        '免费在线百分比变化计算器，输入原值和新值，自动计算增长或减少的百分比。支持正负增长和反向计算。': 'Free online percentage change calculator. Enter original and new values to compute percentage change. Supports positive/negative growth.',
        '计算百分比变化': 'Calculate Percentage Change',
        '输入原始值和新值，计算两者之间的百分比变化': 'Enter original and new values to calculate percentage change',
        '原始值': 'Original Value',
        '新值': 'New Value',
        '交换': 'Swap',
        '🗑 重置': '🗑 Reset',
        '常见百分比变化示例': 'Common Percentage Change Examples',
        '场景': 'Scenario',
        '原值': 'Original',
        '变化': 'Change',
        '股价上涨': 'Stock Up',
        '降价促销': 'Price Drop',
        '收入翻倍': 'Revenue Doubled',
        '减半': 'Halved',
        '在「原始值」输入框中输入变化前的数值。': 'Enter the original value in the "Original Value" field.',
        '在「新值」输入框中输入变化后的数值。': 'Enter the new value in the "New Value" field.',
        '结果自动实时计算，显示百分比变化、变化量和变化方向。': 'Results update in real-time showing percentage change, absolute change, and direction.',
        '点击「交换」可快速交换原值和新值，方便双向计算。': 'Click "Swap" to quickly exchange values for reverse calculation.',
        '百分比变化怎么算？': 'How is percentage change calculated?',
        '公式：': 'Formula: ',
        '。结果为正表示增长，为负表示减少。注意原值不能为0（因为除数为0）。': '. Positive means increase, negative means decrease. Note: original value cannot be 0 (division by zero).',
        '原值为0怎么办？': 'What if original value is 0?',
        '当原值为0时，无法计算百分比变化（数学上无意义）。本工具会显示"无定义"。如果新值>0，可理解为"从无到有"的增长；实际分析时通常用绝对变化量代替。': 'When the original value is 0, percentage change is undefined. This tool displays "Undefined". If new value > 0, think of it as "from nothing" growth; use absolute change for analysis.',
        '从负数到正数怎么算？': 'How to calculate from negative to positive?',
        '例如从-50到50，变化量=100，原值绝对值=50，百分比变化=100/50×100%=+200%。本计算器使用绝对值作为分母，正确处理正负号场景。适用于盈亏分析、温度变化等场景。': 'E.g., from -50 to 50: change=100, |original|=50, percentage=100/50×100%=+200%. This calculator uses absolute value as denominator, correctly handling sign scenarios. Ideal for P&L analysis, temperature changes, etc.',
        '增长率和百分比变化一样吗？': 'Are growth rate and percentage change the same?',
        '是的，百分比变化通常也称为增长率（增长时）或下降率/降幅（减少时）。在Excel中对应公式': 'Yes, percentage change is also called growth rate (when increasing) or decline rate (when decreasing). In Excel: ',
        '。金融分析中有时用对数收益率替代，但日常场景百分比变化已足够。': '. Finance sometimes uses logarithmic returns, but percentage change suffices for everyday use.',
        '百分比变化': 'Percentage Change',
        '变化量': 'Absolute Change',
        '增长': 'Increase',
        '减少': 'Decrease',
        '无变化': 'No Change',
        '正数表示增长': 'Positive = increase',
        '负数表示减少': 'Negative = decrease',
        '无定义': 'Undefined',
        '当原值为0时，百分比变化无定义': 'Percentage change is undefined when original value is 0',
    },
    'loan-calc': {
        '贷款计算器': 'Loan Calculator',
        '等额本息/等额本金还款计算': 'Equal Installment / Equal Principal Calculator',
        '免费在线贷款计算器，输入贷款金额、年利率和贷款期限，自动计算每月还款额、总利息和还款计划表。支持等额本息和等额本金两种方式，个人贷款购车贷款必备。': 'Free online loan calculator. Enter loan amount, annual rate, and term to calculate monthly payment, total interest, and amortization schedule. Supports equal installment and equal principal methods.',
        '免费在线贷款计算器，输入贷款金额、年利率和贷款期限，自动计算每月还款额、总利息和还款计划表。支持等额本息和等额本金两种方式。': 'Free online loan calculator. Enter loan amount, annual rate, and term to get monthly payment, total interest, and schedule.',
        '贷款参数': 'Loan Parameters',
        '填写贷款金额、年利率和期限，选择还款方式': 'Enter loan amount, annual rate, and term; select repayment method',
        '贷款金额': 'Loan Amount',
        '年利率': 'Annual Rate',
        '贷款期限 (年)': 'Loan Term (Years)',
        '还款方式': 'Repayment Method',
        '等额本息': 'Equal Installment',
        '等额本金': 'Equal Principal',
        '计算': 'Calculate',
        '🔄 重置': '🔄 Reset',
        '还款概览': 'Payment Overview',
        '还款计划表（前12期）': 'Amortization Schedule (First 12 Periods)',
        '期数': 'Period',
        '月还款': 'Monthly',
        '本金': 'Principal',
        '利息': 'Interest',
        '剩余本金': 'Balance',
        '* 仅显示前12期，完整计划可按月推算': '* Shows first 12 periods only; full schedule can be extrapolated',
        '等额本息 vs 等额本金': 'Equal Installment vs Equal Principal',
        '对比项': 'Item',
        '每月还款额': 'Monthly Payment',
        '固定不变': 'Fixed',
        '逐月递减': 'Decreasing',
        '总利息': 'Total Interest',
        '较多': 'Higher',
        '较少': 'Lower',
        '前期压力': 'Initial Burden',
        '较小': 'Lower',
        '较大': 'Higher',
        '适合人群': 'Best For',
        '收入稳定者': 'Stable income earners',
        '前期资金充裕者': 'Those with ample initial funds',
        '输入贷款金额（如100000元）。': 'Enter loan amount (e.g., 100000).',
        '输入年利率（如商业贷款基准利率4.9%）。': 'Enter annual rate (e.g., 4.9%).',
        '选择贷款期限（如30年）。': 'Select loan term (e.g., 30 years).',
        '选择还款方式：等额本息或等额本金。': 'Select repayment method: Equal Installment or Equal Principal.',
        '点击计算，查看每月还款额、总利息和还款计划表。': 'Click Calculate to view monthly payment, total interest, and schedule.',
        '等额本息和等额本金哪个更划算？': 'Which is better: Equal Installment or Equal Principal?',
        '等额本金总利息更少，但前期还款压力大；等额本息月供稳定，适合收入稳定人群。以100万贷款30年4.9%为例，等额本金比等额本息少付约17万利息。': 'Equal Principal has lower total interest but higher initial payments; Equal Installment has stable monthly payments. For a 1M loan over 30 years at 4.9%, Equal Principal saves ~170K in interest.',
        '提前还款划算吗？': 'Is early repayment worth it?',
        '等额本息前期利息占比高，越早提前还款越省利息。等额本金利息逐月递减，后期提前还款节省有限。建议在贷款前1/3期限提前还款收益最大。': 'For Equal Installment, early repayment saves more since interest is front-loaded. For Equal Principal, savings diminish over time. Best to repay early within the first 1/3 of the term.',
        '月利率怎么算？': 'How is monthly rate calculated?',
        '月利率 = 年利率 ÷ 12。例如年利率4.9%，月利率约为0.4083%。本计算器内部自动转换。': 'Monthly rate = Annual rate ÷ 12. E.g., 4.9% annual → ~0.4083% monthly. This calculator handles conversion automatically.',
        '月还款额': 'Monthly Payment',
        '总还款额': 'Total Payment',
        '利息占比': 'Interest Ratio',
        '元/月': '/mo',
        '元': '',
        '首月还款': 'First Month',
        '末月还款': 'Last Month',
    },
    'mortgage-calc': {
        '房贷计算器': 'Mortgage Calculator',
        '购房按揭月供在线计算': 'Home Loan Monthly Payment Calculator',
        '免费在线房贷计算器，输入房价、首付比例和贷款年限，自动计算月供、总利息和还款总额。支持等额本息和等额本金两种方式，购房预算规划必备工具。': 'Free online mortgage calculator. Enter home price, down payment percentage, and loan term to calculate monthly payment, total interest, and total cost. Supports equal installment and equal principal methods.',
        '免费在线房贷计算器，输入房价、首付比例和贷款年限，自动计算月供、总利息和还款计划。支持等额本息和等额本金两种方式。': 'Free online mortgage calculator. Enter home price, down payment, and loan term to get monthly payment, total interest, and schedule.',
        '购房参数': 'Mortgage Parameters',
        '填写房屋总价、首付比例、贷款年限和利率': 'Enter home price, down payment percentage, loan term, and rate',
        '房屋总价 (万元)': 'Home Price (10K)',
        '首付比例': 'Down Payment',
        '贷款年限 (年)': 'Loan Term (Years)',
        '自定义利率 (覆盖上方选择)': 'Custom Rate (overrides above)',
        '公积金': 'Provident Fund',
        'LPR基准': 'LPR Base',
        '商业贷款': 'Commercial Loan',
        '旧基准': 'Old Base',
        '自定义': 'Custom',
        '购房方案概览': 'Mortgage Overview',
        '资金构成': 'Payment Breakdown',
        '首付': 'Down Payment',
        '贷款': 'Loan',
        '各城市首付比例参考': 'Down Payment Reference by City',
        '城市': 'City',
        '首套房首付': 'First Home DP',
        '二套房首付': 'Second Home DP',
        '北京': 'Beijing',
        '上海': 'Shanghai',
        '广州': 'Guangzhou',
        '深圳': 'Shenzhen',
        '其他城市': 'Other Cities',
        '输入房屋总价（万元）。': 'Enter home price (in 10K).',
        '选择或输入首付比例（如30%）。': 'Select or enter down payment percentage (e.g., 30%).',
        '选择贷款年限（10-30年）和利率类型。': 'Select loan term (10-30 years) and rate type.',
        '如需自定义利率，在自定义输入框中填写（覆盖下拉框选择）。': 'For custom rate, enter in the custom field (overrides dropdown).',
        '选择还款方式，点击计算查看月供和总利息。': 'Select repayment method, click Calculate to view results.',
        '公积金贷款和商业贷款利率差多少？': 'How much difference between provident fund and commercial loan rates?',
        '公积金贷款利率通常比商业贷款低1-2个百分点。以100万贷款30年为例，公积金3.25%月供约4352元，商业4.2%月供约4890元，每月差额约538元，30年总利息差额约19万。': 'Provident fund rates are typically 1-2% lower than commercial. For 1M over 30 years: PF 3.25% = ~4,352/mo vs commercial 4.2% = ~4,890/mo, saving ~538/mo and ~190K total interest.',
        '首付多付还是少付好？': 'Should I pay more or less down payment?',
        '取决于资金机会成本。如果投资收益率>贷款利率，少付首付更划算；反之多付。当前LPR约3.95%，如果有稳定投资渠道年化>4%，建议少付首付。': 'Depends on opportunity cost. If investment return > loan rate, pay less down payment. Current LPR ~3.95%; if you can earn >4%, consider smaller down payment.',
        'LPR是什么？': 'What is LPR?',
        'LPR（贷款市场报价利率）是商业银行对其最优质客户执行的贷款利率。目前5年期以上LPR为3.95%（2024年），房贷利率通常在此基础上加减点。LPR每月20日更新一次。': 'LPR (Loan Prime Rate) is the rate banks offer their best customers. Current 5-year LPR is 3.95% (2024). Mortgage rates add/subtract points from LPR. LPR updates on the 20th of each month.',
        '月供': 'Monthly Payment',
        '贷款总额': 'Loan Amount',
        '首月月供': 'First Payment',
        '末月月供': 'Last Payment',
    },
    'loading-spinner': {
        'CSS加载动画生成器': 'CSS Loading Spinner Generator',
        'Loading Spinner在线生成': 'Loading Spinner Online Generator',
        '免费在线CSS加载动画生成器，可视化选择30+种loading动画，实时预览效果并一键复制HTML+CSS代码。支持旋转、脉冲、弹跳、波纹等多种样式，前端开发必备工具。': 'Free online CSS loading spinner generator. Visually choose from 30+ animations, preview in real-time, and copy HTML+CSS code with one click. Supports spinner, pulse, bounce, wave, and more.',
        '免费在线CSS加载动画生成器，可视化选择30+种loading动画，实时预览效果并一键复制HTML+CSS代码。支持旋转、脉冲、弹跳、波纹等多种样式。': 'Free online CSS loading spinner generator. Choose from 30+ animations, preview and copy HTML+CSS instantly.',
        '动画样式选择': 'Animation Style Selection',
        '自定义参数': 'Custom Parameters',
        '动画大小': 'Size',
        '动画速度': 'Speed',
        '颜色': 'Color',
        '自定义颜色': 'Custom Color',
        '🎲 随机': '🎲 Random',
        '生成的代码': 'Generated Code',
        '代码格式': 'Code Format',
        'HTML + CSS': 'HTML + CSS',
        '仅 CSS': 'CSS Only',
        '📋 复制': '📋 Copy',
        '动画类型说明': 'Animation Types',
        '类型': 'Type',
        '特点': 'Features',
        '适用场景': 'Use Case',
        '旋转 (Spinner)': 'Spinner',
        '最经典的loading样式': 'Classic loading style',
        '通用数据加载': 'General data loading',
        '脉冲 (Pulse)': 'Pulse',
        '缩放闪烁效果': 'Zoom + blink effect',
        '按钮提交状态': 'Button submit state',
        '弹跳 (Bounce)': 'Bounce',
        '上下弹跳': 'Vertical bounce',
        '聊天消息加载': 'Chat message loading',
        '波纹 (Wave)': 'Wave',
        '柱状伸缩': 'Bar stretching',
        '音频/播放器': 'Audio/player',
        '如何使用生成的代码？': 'How to use the generated code?',
        '点击复制按钮后，将HTML部分粘贴到你的页面中，CSS部分放在': 'After copying, paste the HTML into your page and the CSS into a ',
        '标签或样式文件中即可。动画使用纯CSS实现，无需JavaScript。': ' tag or stylesheet. Animations are pure CSS, no JavaScript needed.',
        '动画性能如何？': 'How is animation performance?',
        '所有动画仅使用': 'All animations use only ',
        '和': ' and ',
        '属性，不会触发layout/paint，完全GPU加速。在移动端也能流畅运行60fps。': ' properties, avoiding layout/paint triggers. Fully GPU-accelerated, smooth 60fps on mobile.',
        '可以修改颜色和大小吗？': 'Can I customize colors and size?',
        '当然！本工具提供了颜色选择器和尺寸滑块。复制代码后你也可以手动修改CSS中的颜色值和尺寸，完全灵活自定义。': 'Absolutely! This tool provides color picker and size slider. After copying, you can also manually edit CSS values for full flexibility.',
        '代码已复制到剪贴板！': 'Code copied to clipboard!',
        '复制失败，请手动选择': 'Copy failed, please select manually',
        '旋转圆环': 'Ring Spinner',
        '三点旋转': 'Three Dots',
        '脉冲圆': 'Pulse Circle',
        '波纹条': 'Wave Bars',
        '进度条': 'Progress Bar',
        '双圆环': 'Dual Ring',
        '旋转方块': 'Rotating Square',
        '淡入淡出': 'Fade In/Out',
        '时钟旋转': 'Clock Spin',
        '跳跃点': 'Jumping Dots',
    },
}

def translate_file(src, dst, tool_name):
    """Read src, apply translations, write to dst"""
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply common translations
    for cn, en in TRANSLATIONS.items():
        content = content.replace(cn, en)
    
    # Apply tool-specific translations
    if tool_name in TOOLS_TRANSLATIONS:
        for cn, en in TOOLS_TRANSLATIONS[tool_name].items():
            content = content.replace(cn, en)
    
    # Fix lang attributes
    content = content.replace('lang="zh-CN"', 'lang="en"')
    
    # Fix hreflang links
    content = content.replace('hreflang="zh"', 'hreflang="en"')
    content = content.replace('hreflang="en" href="https://free-toolbase.com/', 'hreflang="en" href="https://free-toolbase.com/en/')
    # Fix canonical
    content = content.replace('<link rel="canonical" href="https://free-toolbase.com/', '<link rel="canonical" href="https://free-toolbase.com/en/')
    # Fix og:url
    content = content.replace('content="https://free-toolbase.com/', 'content="https://free-toolbase.com/en/')
    
    # Fix lang switch: EN active, CN inactive
    content = content.replace('href="index.html" class="active">中文</a><a href="../en/', 'href="../../')
    # This needs more careful handling - fix manually
    content = re.sub(r'href="index\.html" class="active">中文</a><a href="\.\./en/([^"]+)/" class="">EN</a>',
                     r'href="../../\1/" class="">中文</a><a href="index.html" class="active">EN</a>', content)
    
    # Fix nav links (../ -> ../../)
    content = content.replace('href="../index.html"', 'href="../../index.html"')
    content = content.replace('href="../privacy/"', 'href="../../privacy/"')
    content = content.replace('href="../terms/"', 'href="../../terms/"')
    content = content.replace('href="../about/"', 'href="../../about/"')
    content = content.replace('href="../en/', 'href="../')
    content = content.replace('"../en/', '"../../en/')
    
    # Fix og:image paths
    content = content.replace('content="https://free-toolbase.com/og-image.svg"', 'content="https://free-toolbase.com/og-image.svg"')
    
    # Fix Footer EN link
    content = content.replace('<a href="../en/', '<a href="../')
    
    # Fix breadcrumb: 首页 -> Home
    content = content.replace('>首页</a>', '>Home</a>')
    content = content.replace('>工具</a>', '>Tools</a>')
    
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {tool_name} EN")

tools = ['ping-tool', 'percentage-change', 'loan-calc', 'mortgage-calc', 'loading-spinner']
for t in tools:
    src = f'/home/chison/tools-site/{t}/index.html'
    dst = f'/home/chison/tools-site/en/{t}/index.html'
    translate_file(src, dst, t)
print("Done!")