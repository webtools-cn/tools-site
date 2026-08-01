#!/usr/bin/env python3
"""Round 2: Fix remaining CN tool pages (<70 chars) + all EN tool pages."""
import os, re

# Round 2 CN fixes (68-69 chars)
cn_fixes = {
    'code-playground': '免费在线代码沙盒，支持HTML、CSS、JavaScript三语言实时编辑预览，所见即所得。无需注册登录，代码完全在浏览器本地运行不联网。适合前端学习者练习、快速原型开发和代码片段调试，打开即用。',
    'css-border-generator': '免费在线CSS边框生成器，可视化实时预览border-radius圆角、渐变边框、虚线点线实线等多种边框样式，拖拽滑块调节参数，一键复制生成的CSS代码。前端开发者UI组件样式设计和网页边框美化必备工具，纯前端无需注册。',
    'css-easing-generator': '免费在线CSS Cubic-Bezier缓动函数生成器，可视化拖拽贝塞尔曲线控制点编辑动画缓动效果，实时预览元素动画表现。内置ease、ease-in-out等经典预设曲线，一键复制cubic-bezier() CSS代码。前端动效设计必备，无需注册。',
    'currency-converter-with-rates': '免费在线多币种汇率转换计算器，支持50+种全球主流货币实时参考汇率换算，支持双向金额换算。出国旅行、跨境海淘购物和外贸报价场景必备工具。纯前端本地计算，数据不上传服务器，无需注册完全免费。',
    'env-editor': '免费在线.env环境变量文件编辑器，支持语法高亮显示、变量键值对管理、多环境配置隔离和一键导入导出。可为开发/测试/生产环境快速生成.env配置文件。适合全栈开发者管理项目环境变量，纯前端处理数据不上传。',
    'epub-reader': '免费在线EPUB电子书阅读器，在浏览器中直接打开和阅读EPUB格式电子书。支持章节目录导航、字体大小调节、夜间主题切换和阅读进度自动保存。无需安装任何软件或插件，纯前端处理，电子书文件绝不上传服务器保护隐私。',
    'extra-payment-calculator': '免费在线额外还款节省计算器，计算在房贷/车贷月供基础上额外多还本金所能节省的总利息金额和缩短的还款期限。支持按月、按年和一次性三种额外还款方式对比。适合提前还贷决策和债务优化规划，无需注册。',
    'gpa-calculator': '免费在线GPA绩点计算器，支持标准4.0制、5.0制和百分制转GPA三种计算模式。输入课程学分和成绩即可自动算出加权平均绩点。适合大学生申请出国留学、奖学金评选和学业成绩追踪。纯本地计算，无需注册。',
    'html-color-names': '免费在线HTML标准颜色名称查询工具，收录W3C规范的147种标准颜色名称。搜索或浏览即可查看颜色名称对应的HEX十六进制值和实时颜色预览。前端开发者CSS配色和网页设计选色必备参考工具，无需注册。',
    'keycode-info': '免费在线键盘按键代码查询工具，按下任意键盘按键即可显示该键的keyCode键码、key字符、code物理键位和which兼容值。支持全部标准键盘按键含修饰键Ctrl/Alt/Shift。JavaScript键盘事件编程必备工具，无需注册。',
    'leetspeak': '免费在线1337语Leet Speak转换器，将普通英文文本一键转换为经典黑客风格Leet语。支持基础级字符替换和高级终极多种转换模式。适合网络安全爱好者、CTF竞赛选手和游戏昵称创意生成。纯前端本地处理，无需注册。',
    'markdown-previewer': '免费在线Markdown实时预览编辑器，左栏编辑右侧同步实时渲染。支持全部标准Markdown语法含表格、代码高亮和数学公式，可导出HTML和Markdown文件。适合技术写作、README文档编辑和博客文章排版。纯前端无需注册。',
    'never-have-i-ever': '免费在线真心话大冒险「我没做过」派对游戏，内置200+精选趣味问题随机出题。适合朋友聚会、团建破冰和酒桌游戏，大胆坦诚拉近彼此距离。纯前端本地运行，数据不上传服务器，无需注册完全免费。',
    'noise-generator': '免费在线白噪声生成器，支持白噪声White Noise、粉红噪声Pink Noise和棕色噪声Brown Noise等多种类型。可调节频率和音量，利用Web Audio API纯前端生成高音质噪声。适合助眠入眠、办公专注、婴儿安抚和冥想练习使用。无需注册。',
    'pdf-merge': '免费在线PDF合并工具，将多个PDF文件按自定义顺序合并为一个完整PDF文档。支持拖拽上传、页面顺序自由调整和一键下载合并结果。适合合同归档、发票整理和报告汇总。纯浏览器端处理，PDF文件不上传服务器保障安全，无需注册。',
    'percent-change-calculator': '免费在线百分比变化计算器，快速计算两个数值之间的百分比增长或下降变化率。输入初始值和最终值自动输出变化百分比、绝对变化幅度。适合电商销售额增长分析、KPI指标追踪和投资收益回报率计算。纯前端本地计算，无需注册。',
    'percentage-difference-calculator': '免费在线百分比差异计算器，计算两个数值之间的百分比差异。输入值1和值2，自动输出百分比差异、绝对差异和相对差异三项指标。适合统计数据分析、实验误差评估和双数据源对比。纯客户端本地计算，数据不上传，无需注册。',
    'pet-age-calculator': '免费在线宠物年龄换算计算器，将猫咪和狗狗的实际年龄精准换算为人类等效年龄。基于最新兽医学研究考虑不同品种和体型的衰老速度差异。帮助宠物主人科学了解爱宠所处的生命阶段和对应的健康护理需求，无需注册。',
    'random-wheel': '免费在线幸运转盘随机抽取工具，支持自定义选项列表内容和扇形颜色，点击转盘即可旋转随机选出结果。适合活动抽奖、课堂互动点名、团建游戏惩罚和日常选择困难决策。纯前端本地运行，数据不上传服务器，无需注册。',
    'regex-fuzzer': '免费在线正则表达式模糊测试器，自动生成随机匹配和不匹配字符串来测试正则表达式的正确性和健壮性。支持边界情况测试、ReDoS拒绝服务漏洞检测和批量测试用例生成。前端开发者和QA测试正则表达式质量利器，纯前端无需注册。',
    'retirement-expense-planner': '免费在线退休生活支出规划计算器，全面估算退休后月度年度开支、医疗护理费用和通货膨胀影响。输入当前生活支出和预期通胀率，精准计算退休储蓄目标金额。帮助中年人士制定科学的退休财务规划，纯前端本地计算无需注册。',
    'special-characters': '免费在线特殊字符符号速查表，收录2000+Unicode特殊符号包括数学符号、货币符号、箭头、标点符号和制表符等分类。支持关键词搜索和一键复制到剪贴板。适合社交媒体文案、编程注释和文档排版场景，无需注册。',
    'srt-editor': '免费在线SRT字幕编辑器，支持创建字幕、编辑现有字幕、调整字幕时间轴偏移和合并拆分双语字幕。适合视频创作者制作字幕、翻译字幕和校对字幕时间轴。纯浏览器本地处理，字幕文件绝不上传服务器，安全可靠无需注册。',
    'statistics-calculator': '免费在线统计分析计算器，一键计算均值、中位数、方差、标准差和相关系数等常用统计指标。支持数据批量导入和计算结果导出。适合大学统计课程作业、科学实验数据分析和市场调研数据处理。纯前端本地运行无需注册。',
    'student-loan-calculator': '免费在线学生贷款还款计算器，计算每月还款额、总利息支出和还款总时长。支持固定还款和渐进还款等多种还款方案对比分析。适合大学毕业生和留学回国人员规划学生贷款偿还策略，纯前端计算无需注册。',
    'symbol-explorer': '免费在线Unicode符号浏览器，收录2000+特殊符号包括箭头→、数学符号∞、货币符号€、表情符号和制表符┌等。支持关键词搜索和分类浏览，一键复制符号。适合程序员、设计师和文案编辑日常使用，纯前端无需注册。',
    'team-generator': '免费在线随机分组工具，将人员名单列表随机分配到指定数量的小组中。支持自定义组数和每组人数上限，一键打乱重新随机分组。适合公司团建活动分组、课堂教学分组和体育比赛抽签场景，纯前端本地运行无需注册。',
    'text-reverse': '免费在线文本反转翻转工具，支持按字符反转倒序、单词反转、逐行反转和全文倒序排列四种模式。一键翻转文本排列顺序，轻松处理各种文本反转需求。适合文字游戏创意、编码解码趣味和文本排版处理，无需注册。',
    'text-to-handwriting': '免费在线文字转手写体工具，将输入文本转换为逼真的手写笔记图片效果。支持多种手写字体风格、纸张背景样式和墨水颜色调节，可导出高清PNG图片。适合学生作业笔记还原和社交媒体手写晒图，纯前端无需注册。',
    'user-agent': '免费在线User Agent解析器，输入任意浏览器UA字符串即可解析出浏览器名称版本、操作系统、设备类型和渲染引擎等详细信息。前端开发者调试浏览器兼容性和UA模拟测试必备工具。纯前端本地解析，数据不上传无需注册。',
    'webcam-recorder': '免费在线摄像头视频录制工具，利用浏览器WebRTC API调用电脑或手机摄像头直接录制视频。支持前置/后置摄像头切换，录制完成后自动下载WebM格式视频文件。无需安装任何软件插件，打开浏览器即用，视频不上传保障隐私。',
}

# Round 2 EN fixes 
en_fixes = {
    'en/jensen-alpha-calculator': 'Free online Jensen\'s Alpha calculator to evaluate portfolio excess returns above market benchmarks. Input actual return, risk-free rate, market return and beta to measure fund manager performance. Essential for investment analysis, portfolio attribution and finance education. Pure client-side, no registration required.',
    'en/ohms-law-calculator': 'Free online Ohm\'s Law calculator to compute voltage, current, resistance and power in electrical circuits. Simply enter any two known values to solve for the remaining two using Ohm\'s Law V=IR and Power Law P=VI formulas. Essential for electronics students, Arduino makers and circuit design. Browser local, no upload.',
    'en/conways-game-of-life': 'Free online Conway\'s Game of Life cellular automaton simulator. Watch fascinating patterns emerge from simple mathematical rules — gliders, oscillators and spaceships evolve in real time. Customize the grid, seed patterns and control simulation speed. Great for computer science education and mathematical exploration. No registration, pure browser.',
    'en/pet-food-calculator': 'Free online pet food calculator to determine daily feeding amounts for dogs and cats based on weight, activity level and calorie requirements. Enter your pet\'s details to get personalized daily food portion recommendations. Helps prevent pet obesity and ensure balanced nutrition. Pure client-side, no registration.',
    'en/tip-calculator-by-country': 'Free online international tip calculator with tipping customs for 50+ countries worldwide. Calculate appropriate tips based on local norms — from US 15-20% to Japan\'s no-tipping culture. Split bills among multiple people. Perfect for international travelers and global business diners. No registration required.',
    'en/voice-to-text': 'Free online voice-to-text speech recognition tool using browser\'s built-in Web Speech API. Click and speak to convert your spoken words into written text in real time. Supports multiple languages and continuous dictation mode. Perfect for quick note-taking, drafting emails and accessibility needs. No data leaves your browser.',
    'en/cat-age-calculator': 'Cat Age Calculator — accurately convert your cat\'s real age to human equivalent years. Our calculator uses veterinary science-based formulas accounting for rapid feline development in the first two years versus gradual aging afterward. Understand your cat\'s life stage and health needs. No registration required, 100% browser-based.',
    'en/college-savings-calculator': 'Free College Savings Calculator to plan your child\'s education fund with inflation-adjusted projections. Estimate four-year total costs including tuition, housing and living expenses. Calculate monthly savings needed to reach your 529 plan or education savings goal. Essential for parents planning college funding strategy.',
    'en/child-height-predictor': 'Online child height predictor to estimate your child\'s future adult height using the mid-parental height formula. Enter parent heights and child\'s current age, gender and height for science-based height prediction. Helpful for pediatric growth monitoring and sports talent scouting. Pure browser, no data upload.',
    'en/gratitude-journal': 'Free online gratitude journal to practice daily positive thinking and mindfulness. Write three things you\'re grateful for each day, track your happiness streaks and reflect on positive moments. Backed by positive psychology research on well-being improvement. All entries stored locally in your browser for complete privacy.',
    'en/cat-calorie-calculator': 'Free online cat calorie calculator to determine your cat\'s ideal daily calorie intake for weight management. Calculate your cat\'s Resting Energy Requirement (RER) based on weight, life stage and body condition score. Supports weight loss, maintenance and growth plans. Veterinary nutrition science-based, pure browser.',
    'en/chronotype-quiz': 'Free chronotype quiz to discover your natural sleep-wake biological rhythm. Answer science-based questions about your energy levels, productivity peaks and sleep preferences to determine if you\'re a Morning Lark, Night Owl, Hummingbird or Bear chronotype. Optimize your daily schedule around your natural body clock.',
    'en/dog-calorie-calculator': 'Free online dog calorie calculator to determine your dog\'s daily calorie needs based on weight, breed, age and activity level. Calculate Resting Energy Requirement (RER) and Daily Energy Requirement (DER) for puppies, adult and senior dogs. Supports weight management and healthy feeding plans. Pure browser.',
    'en/burn-rate-calculator': 'Free online startup Burn Rate Calculator to analyze your company\'s cash burn and runway. Calculate your startup\'s gross burn rate, net burn rate and how many months of cash runway remain before fundraising is needed. Essential for startup founders, CFO planning and investor updates. Pure client-side, no registration.',
    'en/password-pwned-checker': 'Free online password breach checker that uses k-anonymity to securely verify if your passwords have been exposed in known data breaches. Your password never leaves your browser — only a partial hash prefix is sent to the HaveIBeenPwned API. Stay safe online without compromising your passwords.',
    'en/graham-number-calculator': 'Free online Graham Number Calculator based on Benjamin Graham\'s value investing formula. Input Earnings Per Share (EPS) and Book Value Per Share to calculate the maximum price a defensive investor should pay for a stock. Essential tool for value investors and fundamental stock analysis. No registration needed.',
    'en/car-depreciation-calculator': 'Free online car depreciation calculator to estimate your vehicle\'s resale value over time. Model future depreciation using industry-standard curves accounting for make, model, age, mileage and condition. Compare new vs used car value retention rates. Essential for car buyers planning total ownership costs.',
    'en/business-valuation-calculator': 'Free online business valuation calculator to estimate your company\'s worth using multiple methods. Calculate business value using revenue multiples, EBITDA multiples, discounted cash flow and asset-based approaches. Essential for entrepreneurs planning exit strategies, fundraising and M&A discussions. No registration.',
    'en/link-preview': 'Free online link preview tool to check how any URL appears when shared on social media. Enter a URL to preview the webpage title, description, image thumbnail and Open Graph meta tags. Test how your content looks on Facebook, Twitter, LinkedIn before publishing. Pure browser, no registration needed.',
    'en/nps-calculator': 'Free online NPS (National Pension System) Calculator for India. Estimate your retirement corpus from NPS contributions and projected returns. Calculate monthly pension amounts, lump-sum withdrawal options and tax benefits under Section 80CCD. Essential for Indian employees planning retirement through the NPS scheme.',
}

# Apply CN fixes
cn_count = 0
for slug, new_desc in cn_fixes.items():
    path = f'./{slug}/index.html'
    if not os.path.exists(path):
        print(f'  SKIP CN: {path} not found')
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    m = re.search(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])', content)
    if not m:
        print(f'  SKIP CN: {path} no desc')
        continue
    old_desc = m.group(2)
    old_len = len(old_desc)
    new_content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    if new_content == content:
        new_content = content.replace(
            f"<meta name='description' content='{old_desc}'",
            f"<meta name='description' content='{new_desc}'"
        )
    if new_content == content:
        print(f'  FAIL CN: {slug} replace did not match')
        continue
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    print(f'  OK CN: {slug} [{old_len}→{len(new_desc)}]')
    cn_count += 1

# Apply EN fixes
en_count = 0
for slug, new_desc in en_fixes.items():
    path = f'./{slug}/index.html'
    if not os.path.exists(path):
        print(f'  SKIP EN: {path} not found')
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    m = re.search(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])', content)
    if not m:
        print(f'  SKIP EN: {path} no desc')
        continue
    old_desc = m.group(2)
    old_len = len(old_desc)
    new_content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    if new_content == content:
        new_content = content.replace(
            f"<meta name='description' content='{old_desc}'",
            f"<meta name='description' content='{new_desc}'"
        )
    if new_content == content:
        print(f'  FAIL EN: {slug} replace did not match')
        continue
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    print(f'  OK EN: {slug} [{old_len}→{len(new_desc)}]')
    en_count += 1

print(f'\nTotal CN fixed: {cn_count}')
print(f'Total EN fixed: {en_count}')
print(f'Combined total: {cn_count + en_count}')
