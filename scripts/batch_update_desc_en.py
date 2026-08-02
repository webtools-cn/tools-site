#!/usr/bin/env python3
"""Batch update meta descriptions for EN tool pages (mirror of CN updates)."""
import re, os, sys

updates = [
    # 1. chi-square-calculator EN
    ("en/chi-square-calculator",
     '<meta name="description" content="P值。支持2x2和R×C列联表分析。适用于统计分析、学术研究和数据科学。纯前端计算。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online Chi-Square Test calculator. Enter observed and expected values to compute chi-square statistic, degrees of freedom, and P-value instantly. Supports 2×2 and R×C contingency table analysis for academic research, data science, and statistical hypothesis testing. Pure frontend, no registration required.">'),

    # 2. food-calorie-calculator EN
    ("en/food-calorie-calculator",
     '<meta name="description" content="12大分类，点击即添加自动累计全天总热量。适合减脂健身、糖尿病饮食控制和日常营养管理，无需注册即开即用。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="Free online food calorie calculator with 12 categories covering hundreds of common foods. Click to add items and auto-sum daily total calories. Ideal for weight loss, fitness tracking, diabetes diet management, and daily nutrition planning. Pure frontend processing, no registration required.">'),

    # 3. fractal-explorer EN
    ("en/fractal-explorer",
     '<meta name="description" content="Canvas渲染，支持拖拽选择、滚轮缩放。🔮 分形探索器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online fractal explorer — render stunning Mandelbrot and Julia sets in real time. Zoom infinitely, pan, and explore fractal details with custom iteration depth and color themes. Pure frontend Canvas rendering, no data upload, no registration required.">'),

    # 4. color-contrast EN
    ("en/color-contrast",
     '<meta name="description" content="AA/AAA级合规。支持HEX/RGB/HSL输入，实时预览。前端无障碍检测必备。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="Free online WCAG color contrast checker — enter foreground and background colors to calculate contrast ratio and determine AA/AAA compliance. Supports HEX, RGB, and HSL input with real-time text readability preview. An essential accessibility tool for frontend developers, no registration required.">'),

    # 5. days-between-dates EN
    ("en/days-between-dates",
     '<meta name="description" content="N天前后的具体日期，可切换自然日和工作日模式。适用于项目管理排期、合同到期日提醒、宝宝年龄计算和节日倒计时。纯浏览器本地运行，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="Free online date calculator — quickly calculate days between two dates or find a date N days from now. Switch between calendar days and business days mode. Perfect for project planning, contract deadlines, baby age tracking, and countdown timers. Pure browser-based, no registration required.">'),

    # 6. gcf-calculator EN
    ("en/gcf-calculator",
     '<meta name="description" content="(GCF)和最小公倍数(LCM)。支持逗号分隔批量输入。所有计算在浏览器本地执行。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="Free online GCF and LCM calculator — compute Greatest Common Factor and Least Common Multiple for multiple numbers at once. Supports comma-separated batch input with Euclidean algorithm precision. Perfect for math learning, fraction simplification, and algorithm teaching. Pure browser computation, no registration required.">'),

    # 7. decimal-to-fraction EN
    ("en/decimal-to-fraction",
     '<meta name="description" content="0.333.转为1/3）、带分数显示、大数计算。无需注册，适合学生、教师、工程师。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="Free online decimal to fraction converter — convert any decimal to its simplest fraction form. Supports terminating and repeating decimals, mixed number display, and high-precision computation. Ideal for students, teachers, and engineers. Pure frontend processing, no registration required.">'),

    # 8. loan-calc EN
    ("en/loan-calc",
     '<meta name="description" content="1-30年），生成逐月详细还款计划表。购房贷款和消费贷款的决策参考工具。纯前端本地计算，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="Free online loan calculator with equal installment and equal principal repayment methods. Enter loan amount, interest rate, and term to generate monthly payments, total interest, and a detailed amortization schedule. Perfect for mortgage and personal loan planning. Pure frontend computation, no registration required.">'),

    # 9. commission-calculator EN
    ("en/commission-calculator",
     '<meta name="description" content="+提成计算，销售人员和自由职业者必备，支持输入销售额完成此步骤、输入提成比例完成此步骤。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online commission calculator — supports percentage-based and tiered commission models. Enter sales amount and commission rate to compute earnings instantly, with optional base salary. Essential tool for sales professionals and freelancers. Pure frontend computation, no registration required.">'),

    # 10. confidence-interval-calculator EN
    ("en/confidence-interval-calculator",
     '<meta name="description" content="95%置信区间的含义是：如果重复抽样100次，大约95次计算出的区间会包含真实总体均值。纯前端本地处理，数据不上传服务器，无需注册免费使用。">',
     '<meta name="description" content="Free online confidence interval calculator — enter sample mean, standard deviation, and sample size to compute 95% and 99% confidence intervals. Ideal for A/B testing analysis, academic research, and statistical inference using z-distribution or t-distribution. Pure frontend, no registration required.">'),

    # 11. download-time-calculator EN
    ("en/download-time-calculator",
     '<meta name="description" content="B/KB/MB/GB/TB和bps/Kbps/Mbps/Gbps单位换算，纯前端零上传。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online download time calculator — enter file size and network bandwidth to estimate download duration. Supports B to TB file sizes and bps to Gbps bandwidth with automatic unit conversion. Useful for game downloads, video transfers, and file delivery estimation. Pure frontend, no registration required.">'),

    # 12. equity-dilution-calc EN
    ("en/equity-dilution-calc",
     '<meta name="description" content="ESOP期权池、可转债转换等多种稀释场景。📊 股权稀释计算器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online equity dilution calculator — simulate ownership changes across multiple funding rounds. Supports ESOP pool allocation, convertible notes, and new investor scenarios. Essential cap table management tool for startup founders. Pure frontend computation, no data upload, no registration required.">'),

    # 13. expense-ratio-calculator EN
    ("en/expense-ratio-calculator",
     '<meta name="description" content="0.1%与2%费率在10年20年后的收益差距。指数基金与主动基金对比评估的理财必备工具。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online fund expense ratio calculator — compare the long-term impact of different management fees on investment returns. See how a 0.1% low-cost index fund outperforms a 2% actively managed fund over 10-20 years. Essential decision tool for index fund investors. Pure frontend, no registration required.">'),

    # 14. username-generator EN
    ("en/username-generator",
     '<meta name="description" content="/符号后缀、前缀修饰。生成结果可直接复制，适合游戏ID、社交媒体账号、论坛昵称等场景。纯前端本地处理，数据不上传服务器，无需注册免费使用。">',
     '<meta name="description" content="Free online username generator — create cool, cute, professional, and funny usernames with customizable prefixes, suffixes, and symbol combinations. Bulk generate and one-click copy. Perfect for gaming IDs, social media handles, forum nicknames, and test data. Pure frontend, no registration required.">'),

    # 15. name-generator EN
    ("en/name-generator",
     '<meta name="description" content="1-50个）。适合小说角色命名、游戏ID创建、测试数据生成和笔名取名灵感。纯前端本地生成，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="Free online name generator — generate Chinese, English, fantasy character names, and pen names with customizable gender styles and batch quantity. Ideal for novel character naming, game ID creation, test data generation, and pen name inspiration. Pure frontend, no registration required.">'),

    # 16. business-card-maker EN
    ("en/business-card-maker",
     '<meta name="description" content="PNG名片图片。无需注册登录，所有设计在浏览器本地完成。适合创业者、自由职业者和商务人士快速制作电子名片。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="Free online business card maker — customize name, title, company, phone, and email with template styles and color schemes. Real-time preview and export as high-res PNG. Perfect for entrepreneurs, freelancers, and professionals creating digital business cards. Pure browser design, no registration, data stays local.">'),

    # 17. signature-maker EN
    ("en/signature-maker",
     '<meta name="description" content="PNG。无需注册，适合电子合同、PDF签署、电子邮件签名等场景，支持撤销操作、高清导出。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online signature maker — draw or handwrite your signature on canvas and export as transparent PNG. Supports multiple brush sizes and colors with undo/redo. Perfect for electronic contracts, PDF signing, and email signatures. Pure frontend Canvas processing, no registration, data never uploaded.">'),

    # 18. placeholder-image EN
    ("en/placeholder-image",
     '<meta name="description" content="免费在线占位图生成器工具，快速高效地完成占位图生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online placeholder image generator — customize dimensions, background color, and text to create placeholder images for web design and prototyping. Supports common size presets and custom dimensions with PNG/SVG download. Essential tool for frontend developers and UI designers, no registration required.">'),

    # 19. progress-bar EN
    ("en/progress-bar",
     '<meta name="description" content="免费在线进度条生成器工具，快速高效地完成进度条生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online progress bar generator — visually customize colors, size, border radius, and animation effects with real-time preview. Generates ready-to-use CSS/HTML code. Supports percentage and segmented progress display for web loading animations, form progress, and data visualization. Pure frontend, no registration required.">'),

    # 20. coupon-generator EN
    ("en/coupon-generator",
     '<meta name="description" content="免费在线优惠码生成器工具，快速高效地完成优惠码生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online coupon code generator — batch generate random coupon codes for e-commerce promotions, marketing campaigns, and membership rewards. Customize prefix, length, character type (numeric/alphanumeric/mixed), and quantity with one-click export. Essential for e-commerce and marketing professionals, no registration required.">'),

    # 21. word-cloud-generator EN
    ("en/word-cloud-generator",
     '<meta name="description" content="PNG图片。纯前端本地Canvas处理，数据不上传服务器，支持演示报告、简历技能展示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online word cloud generator — paste text to auto-count word frequency and create visual word clouds. Customize color themes, fonts, and layout direction with stop word filtering. Perfect for presentations, data analysis, and resume skill tags. Pure frontend Canvas rendering, no registration required.">'),

    # 22. graph-plotter EN
    ("en/graph-plotter",
     '<meta name="description" content="PNG。支持sin/cos/tan/exp/log/多项式等常见函数。无需注册。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="Free online function graph plotter — enter math expressions to plot curves instantly. Supports sin, cos, tan, exp, log, polynomials and more. Overlay multiple curves, zoom and pan interactively. Ideal for math teaching, function analysis, and learning visualization. Export as PNG, no registration required.">'),

    # 23. file-diff EN
    ("en/file-diff",
     '<meta name="description" content="txt/csv/json/xml/html/md等文本格式。代码比对、文档校对必备工具。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online file diff tool — paste or upload two text files to compare differences with line-by-line highlighting. Supports txt, csv, json, xml, html, md and more formats. Perfect for code review, document version comparison, and config change tracking. Pure frontend processing, no registration required.">'),

    # 24. unit-price-comparison EN
    ("en/unit-price-comparison",
     '<meta name="description" content="/克、元/毫升等），助你做出最优购物决策。单价对比计算器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online unit price comparison calculator — enter product specs and prices to calculate real cost per unit (per gram, per ml). Compare multiple products simultaneously to make the best shopping decisions and avoid bulk-packaging traps. Pure frontend computation, no registration required.">'),

    # 25. internet-speed-test EN
    ("en/internet-speed-test",
     '<meta name="description" content="免费在线网速测试工具，测试Ping延迟、下载速度和上传速度。无需安装，一键测速，实时显示网络性能。纯浏览器端测试，数据不上传服务器保护隐私。">',
     '<meta name="description" content="Free online internet speed test — one-click check of ping latency, download speed, and upload speed. No software installation needed, real-time network performance metrics with connection quality assessment. Perfect for broadband testing, mobile network checks, and troubleshooting. Pure browser test, privacy protected.">'),

    # 26. screenshot-tool EN
    ("en/screenshot-tool",
     '<meta name="description" content="F12打开控制台，粘贴截图代码来截取该页面。📸 在线网页截图支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online webpage screenshot tool — enter a URL to capture full-page or selected-area screenshots and export as high-res PNG. Customize viewport dimensions to simulate different devices. Perfect for web design review, competitor analysis, and content archiving. Pure frontend, no registration required.">'),

    # 27. webcam-test EN
    ("en/webcam-test",
     '<meta name="description" content="/对比度检测。无需注册，不上传服务器，保护隐私安全，支持查看实时视频画面、查看检测结果。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online webcam test — check if your camera works properly with one click. Displays real-time video feed with resolution, frame rate, and color detection. Perfect for pre-meeting camera debugging, online interview prep, and streaming equipment checks. Pure browser detection, video never uploaded, privacy safe.">'),

    # 28. color-blind-simulator EN
    ("en/color-blind-simulator",
     '<meta name="description" content="(Deuteranopia) - 最常见、蓝黄色盲 (Tritanopia) - 罕见。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="Free online color blindness simulator — upload an image to view it through protanopia, deuteranopia, tritanopia, and achromatopsia lenses. Supports multiple CVD simulation types. Essential accessibility testing tool for UI designers. Pure frontend processing, images never uploaded, no registration required.">'),

    # 29. solar-roi-calculator EN
    ("en/solar-roi-calculator",
     '<meta name="description" content="ROI投资回报率、回本周期和25年总发电收益与累计电费节省金额。自动考虑联邦税收抵免政策(ITC)和电价年涨幅，帮房主评估光伏发电经济可行性。纯浏览器本地计算，数据不上传，无需注册完全免费。">',
     '<meta name="description" content="Free online solar ROI calculator — estimate payback period, 25-year total energy revenue, and cumulative electricity savings for your solar installation. Automatically factors in tax credits and annual electricity rate increases. Helps homeowners evaluate photovoltaic economic feasibility. Pure browser computation, no registration required.">'),
]

count = 0
for slug, old, new in updates:
    path = f"{slug}/index.html"
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}")
        continue
    
    with open(path) as f:
        content = f.read()
    
    if old not in content:
        print(f"SKIP (old not found): {path}")
        # Try finding the actual line
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
        if m:
            print(f"  Actual desc ({len(m.group(1))} chars): {m.group(1)[:100]}...")
        continue
    
    new_content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(new_content)
    
    print(f"OK: {path} ({len(old)} → {len(new)} chars)")
    count += 1

print(f"\nTotal EN updated: {count}")