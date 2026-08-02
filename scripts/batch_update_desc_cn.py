#!/usr/bin/env python3
"""Batch update meta descriptions for 30 CN tool pages."""
import re, os, sys

# Each entry: (slug, old_desc_substring, new_desc)
# old_desc_substring is used to locate the line to replace
updates = [
    # 1. chi-square-calculator (68 chars → ~150)
    ("chi-square-calculator",
     '<meta name="description" content="P值。支持2x2和R×C列联表分析。适用于统计分析、学术研究和数据科学。纯前端计算。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线卡方检验计算器，输入观察值与期望值，一键计算卡方统计量、自由度和P值。支持2×2和R×C列联表分析，适用于学术研究、数据科学和统计分析。纯前端计算，数据不上传服务器，无需注册完全免费。">'),

    # 2. food-calorie-calculator (68 chars → ~150)
    ("food-calorie-calculator",
     '<meta name="description" content="12大分类，点击即添加自动累计全天总热量。适合减脂健身、糖尿病饮食控制和日常营养管理，无需注册即开即用。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="免费在线食物热量计算器，覆盖主食、肉类、蔬果、零食、饮品等12大类数百种常见食物。点击即可添加并自动累计全天总热量，适合减脂健身、糖尿病饮食控制和日常营养管理。纯前端即开即用，数据安全不上传服务器。">'),

    # 3. fractal-explorer (68 chars → ~150)
    ("fractal-explorer",
     '<meta name="description" content="Canvas渲染，支持拖拽选择、滚轮缩放。🔮 分形探索器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线分形探索器，实时渲染曼德勃罗集和茱莉亚集，支持无限缩放和拖拽探索分形细节。自定义迭代深度和颜色主题，生成惊艳的分形艺术作品。纯前端Canvas渲染，数据不上传服务器，无需注册完全免费。">'),

    # 4. color-contrast (69 chars → ~150)
    ("color-contrast",
     '<meta name="description" content="AA/AAA级合规。支持HEX/RGB/HSL输入，实时预览。前端无障碍检测必备。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="免费在线WCAG颜色对比度检查器，输入前景色和背景色自动计算对比度比值并判断AA/AAA级合规。支持HEX/RGB/HSL格式输入，实时预览文字在不同颜色下的可读性。前端开发者无障碍设计必备工具，无需注册。">'),

    # 5. days-between-dates (88 chars → ~150)
    ("days-between-dates",
     '<meta name="description" content="N天前后的具体日期，可切换自然日和工作日模式。适用于项目管理排期、合同到期日提醒、宝宝年龄计算和节日倒计时。纯浏览器本地运行，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="免费在线日期计算器，快速计算两个日期之间相差天数，或N天前后的具体日期。支持自然日和工作日模式切换，适用于项目排期、合同到期提醒、宝宝年龄计算和节日倒计时。纯浏览器本地运行，无需注册完全免费。">'),

    # 6. gcf-calculator (69 chars → ~150)
    ("gcf-calculator",
     '<meta name="description" content="(GCF)和最小公倍数(LCM)。支持逗号分隔批量输入。所有计算在浏览器本地执行。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="免费在线最大公因数(GCF)和最小公倍数(LCM)计算器，支持逗号分隔批量输入多个数值，欧几里得算法精确计算。适用于数学学习、分数化简和算法教学。所有计算在浏览器本地执行，无需注册完全免费。">'),

    # 7. decimal-to-fraction (69 chars → ~150)
    ("decimal-to-fraction",
     '<meta name="description" content="0.333.转为1/3）、带分数显示、大数计算。无需注册，适合学生、教师、工程师。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="免费在线小数转分数计算器，将任意小数精确转换为最简分数形式。支持有限小数和无限循环小数转换、带分数显示和大数精度计算。适合学生数学学习、教师备课和工程师数值处理，无需注册即开即用。">'),

    # 8. loan-calc (69 chars → ~150)
    ("loan-calc",
     '<meta name="description" content="1-30年），生成逐月详细还款计划表。购房贷款和消费贷款的决策参考工具。纯前端本地计算，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="免费在线贷款计算器，支持等额本息和等额本金两种还款方式。输入贷款金额、年利率和期限，自动生成每月还款额、总利息和逐月还款计划表。购房贷款和消费贷款的理想决策参考工具，纯前端本地计算，无需注册完全免费。">'),

    # 9. commission-calculator (70 chars → ~150)
    ("commission-calculator",
     '<meta name="description" content="+提成计算，销售人员和自由职业者必备，支持输入销售额完成此步骤、输入提成比例完成此步骤。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线佣金计算器，支持按比例提成和阶梯式提成两种模式。输入销售额和提成比例，自动计算佣金收入，可选加固定底薪。销售人员和自由职业者核算收入的必备工具，纯前端本地计算，无需注册完全免费。">'),

    # 10. confidence-interval-calculator (70 chars → ~150)
    ("confidence-interval-calculator",
     '<meta name="description" content="95%置信区间的含义是：如果重复抽样100次，大约95次计算出的区间会包含真实总体均值。纯前端本地处理，数据不上传服务器，无需注册免费使用。">',
     '<meta name="description" content="免费在线置信区间计算器，输入样本均值、标准差和样本量，快速计算95%和99%置信区间。适用于AB测试数据分析、学术研究和统计推断。通过z分布或t分布精确计算，纯前端本地运行，无需注册完全免费。">'),

    # 11. download-time-calculator (70 chars → ~150)
    ("download-time-calculator",
     '<meta name="description" content="B/KB/MB/GB/TB和bps/Kbps/Mbps/Gbps单位换算，纯前端零上传。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线下载时间计算器，输入文件大小和网络带宽，即时估算下载所需时间。支持B至TB文件大小和bps至Gbps带宽单位的自动换算。适用于游戏下载、视频传输和文件传输场景预估，纯前端零上传，无需注册完全免费。">'),

    # 12. equity-dilution-calc (70 chars → ~150)
    ("equity-dilution-calc",
     '<meta name="description" content="ESOP期权池、可转债转换等多种稀释场景。📊 股权稀释计算器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线股权稀释计算器，帮助创业者模拟多轮融资后的股权比例变化。支持ESOP期权池预留、可转债转换和新增投资者等多种稀释场景。创业团队Cap Table管理的必备工具，纯前端计算，数据不上传服务器，无需注册完全免费。">'),

    # 13. expense-ratio-calculator (70 chars → ~150)
    ("expense-ratio-calculator",
     '<meta name="description" content="0.1%与2%费率在10年20年后的收益差距。指数基金与主动基金对比评估的理财必备工具。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线基金费率计算器，直观对比不同基金管理费率对长期投资回报的影响。输入投资金额和年限，对比0.1%低费率指数基金与2%高费率主动基金在10年、20年后的收益差距。指数基金投资者的理财决策必备工具，纯前端计算。">'),

    # 14. random-password → 路径是 password-generator (69 chars → ~150)
    ("password-generator",
     '<meta name="description" content="+数字+符号），实时评估密码强度，一键复制。随机密码生成器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线随机密码生成器，使用密码学安全随机数生成高强度密码。自定义长度（8-128位）和字符类型（大小写字母+数字+特殊符号），实时评估密码强度并一键复制。保护账户安全的必备工具，纯浏览器端生成，密码不上传服务器。">'),

    # 15. username-generator (69 chars → ~150)
    ("username-generator",
     '<meta name="description" content="/符号后缀、前缀修饰。生成结果可直接复制，适合游戏ID、社交媒体账号、论坛昵称等场景。纯前端本地处理，数据不上传服务器，无需注册免费使用。">',
     '<meta name="description" content="免费在线用户名生成器，随机生成炫酷、可爱、专业、搞笑等多种风格的用户名。支持自定义前缀后缀修饰和数字/符号组合。适合游戏ID、社交媒体账号、论坛昵称和测试数据等场景，批量生成一键复制。纯前端本地处理，无需注册完全免费。">'),

    # 16. name-generator (70 chars → ~150)
    ("name-generator",
     '<meta name="description" content="1-50个）。适合小说角色命名、游戏ID创建、测试数据生成和笔名取名灵感。纯前端本地生成，无需注册完全免费。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="免费在线名字生成器，支持生成中文名、英文名、奇幻角色名和笔名等多种类型。可指定性别风格和批量生成数量。适合小说角色命名、游戏ID创建、测试数据生成和取笔名灵感，纯前端本地生成，无需注册完全免费。">'),

    # 17. business-card-maker (69 chars → ~150)
    ("business-card-maker",
     '<meta name="description" content="PNG名片图片。无需注册登录，所有设计在浏览器本地完成。适合创业者、自由职业者和商务人士快速制作电子名片。纯前端本地处理，数据安全有保障。">',
     '<meta name="description" content="免费在线名片生成器，自定义姓名、职位、公司、电话和邮箱信息，选择模板样式和配色方案，实时预览并导出高清PNG名片。适合创业者、自由职业者和商务人士快速制作电子名片。纯浏览器端设计，无需注册，数据安全不上传。">'),

    # 18. signature-maker (70 chars → ~150)
    ("signature-maker",
     '<meta name="description" content="PNG。无需注册，适合电子合同、PDF签署、电子邮件签名等场景，支持撤销操作、高清导出。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线签名制作工具，在画布上手写或绘制个性化签名，导出高清PNG透明背景图片。支持多种笔触粗细和颜色，可撤销重画。适合电子合同签署、PDF签名和电子邮件签名等场景。纯前端Canvas处理，无需注册，数据不上传服务器。">'),

    # 19. placeholder-image (69 chars → ~150)
    ("placeholder-image",
     '<meta name="description" content="免费在线占位图生成器工具，快速高效地完成占位图生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线占位图生成器，自定义图片尺寸、背景颜色和文字内容，即时生成占位图片用于网页设计和原型开发。支持常见尺寸预设和自定义宽高，一键下载PNG/SVG格式。前端开发者和UI设计师的必备工具，无需注册完全免费。">'),

    # 20. progress-bar (69 chars → ~150)
    ("progress-bar",
     '<meta name="description" content="免费在线进度条生成器工具，快速高效地完成进度条生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线进度条生成器，可视化自定义进度条的颜色、尺寸、圆角和动画效果，实时预览并生成CSS/HTML代码。支持百分比和分段进度显示，适用于网页加载动画、表单进度和数据可视化场景。纯前端处理，无需注册完全免费。">'),

    # 21. coupon-generator (69 chars → ~150)
    ("coupon-generator",
     '<meta name="description" content="免费在线优惠码生成器工具，快速高效地完成优惠码生成器操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线优惠码生成器，批量生成随机优惠码用于电商促销、营销活动和会员福利。自定义前缀、长度、字符类型（数字/字母/混合）和生成数量，一键导出。电商运营和市场营销人员的必备工具，纯前端生成，无需注册完全免费。">'),

    # 22. word-cloud-generator (69 chars → ~150)
    ("word-cloud-generator",
     '<meta name="description" content="PNG图片。纯前端本地Canvas处理，数据不上传服务器，支持演示报告、简历技能展示。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线词云生成器，输入文本自动统计词频并生成可视化词云图。支持自定义颜色主题、字体样式和布局方向，可排除常见停用词。适用于演示报告、数据分析展示和简历技能标签，纯前端Canvas渲染，无需注册完全免费。">'),

    # 23. graph-plotter (68 chars → ~150)
    ("graph-plotter",
     '<meta name="description" content="PNG。支持sin/cos/tan/exp/log/多项式等常见函数。无需注册。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。">',
     '<meta name="description" content="免费在线函数图表绘制器，输入数学表达式即时绘制函数曲线。支持sin/cos/tan/exp/log/多项式等常见函数，可叠加多条曲线对比，支持缩放和平移交互。适合数学教学、函数分析和学习可视化，导出PNG图片，无需注册完全免费。">'),

    # 24. file-diff (70 chars → ~150)
    ("file-diff",
     '<meta name="description" content="txt/csv/json/xml/html/md等文本格式。代码比对、文档校对必备工具。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线文件差异对比工具，粘贴或上传两个文本文件，逐行高亮显示差异内容。支持txt/csv/json/xml/html/md等文本格式，适用于代码对比审查、文档版本校对和配置文件变更检查。纯前端本地处理，数据不上传服务器，无需注册完全免费。">'),

    # 25. unit-price-comparison (68 chars → ~150)
    ("unit-price-comparison",
     '<meta name="description" content="/克、元/毫升等），助你做出最优购物决策。单价对比计算器支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线单价对比计算器，输入不同商品的规格和价格，自动计算每单位（元/克、元/毫升）的真实成本。帮助消费者在超市购物时做出最优选择，避免大包装陷阱。支持多商品同时对比，纯前端计算，无需注册完全免费。">'),

    # 26. internet-speed-test (70 chars → ~150)
    ("internet-speed-test",
     '<meta name="description" content="免费在线网速测试工具，测试Ping延迟、下载速度和上传速度。无需安装，一键测速，实时显示网络性能。纯浏览器端测试，数据不上传服务器保护隐私。">',
     '<meta name="description" content="免费在线网速测试工具，一键检测Ping延迟、下载速度和上传速度。无需安装任何软件，实时显示网络性能指标和连接质量评估。适用于宽带测速、移动网络检测和故障排查，纯浏览器端测试，数据不上传服务器，保护隐私安全。">'),

    # 27. screenshot-tool (70 chars → ~150)
    ("screenshot-tool",
     '<meta name="description" content="F12打开控制台，粘贴截图代码来截取该页面。📸 在线网页截图支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线网页截图工具，输入URL即可截取网页全屏或指定区域截图，导出PNG高清图片。适用于网页设计验收、竞品分析和内容存档。支持自定义视口尺寸模拟不同设备。纯前端处理，无需注册完全免费。">'),

    # 28. webcam-test (70 chars → ~150)
    ("webcam-test",
     '<meta name="description" content="/对比度检测。无需注册，不上传服务器，保护隐私安全，支持查看实时视频画面、查看检测结果。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线摄像头测试工具，一键检测摄像头是否正常工作。实时显示视频画面，支持分辨率、帧率和色彩检测。适用于视频会议前摄像头调试、在线面试准备和直播设备检查。纯浏览器端检测，视频流不上传服务器，保护隐私安全。">'),

    # 29. color-blind-simulator (70 chars → ~150)
    ("color-blind-simulator",
     '<meta name="description" content="(Deuteranopia) - 最常见、蓝黄色盲 (Tritanopia) - 罕见。纯前端本地处理，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线色盲模拟器，上传图片即可从红绿色盲、蓝黄色盲和全色盲视角查看图片效果。支持绿色弱视和红色弱视等多种色觉障碍类型模拟。UI设计师无障碍设计验证的必备工具，纯前端处理，图片不上传服务器，无需注册完全免费。">'),

    # 30. solar-roi-calculator (95 chars → ~150)
    ("solar-roi-calculator",
     '<meta name="description" content="ROI投资回报率、回本周期和25年总发电收益与累计电费节省金额。自动考虑联邦税收抵免政策(ITC)和电价年涨幅，帮房主评估光伏发电经济可行性。纯浏览器本地计算，数据不上传，无需注册完全免费。">',
     '<meta name="description" content="免费在线太阳能投资回报率计算器，输入安装成本和当地日照参数，计算光伏系统回本周期、25年总发电收益和累计电费节省。自动考虑税收抵免政策和电价年涨幅，帮助房主评估屋顶光伏的经济可行性。纯浏览器本地计算，数据不上传，无需注册完全免费。">'),
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
        continue
    
    new_content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(new_content)
    
    print(f"OK: {path} ({len(old)} → {len(new)} chars)")
    count += 1

print(f"\nTotal updated: {count}")
