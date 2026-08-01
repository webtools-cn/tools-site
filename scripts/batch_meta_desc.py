#!/usr/bin/env python3
"""Batch extend meta descriptions for CN tool pages."""
import os, re, sys

updates = {
    "email-verifier": """免费在线邮箱地址验证工具，实时检测邮箱格式是否正确、域名是否存在MX记录、是否为一次性临时邮箱。支持批量验证多个邮箱地址，帮助清理邮件列表中无效邮箱、降低邮件退信率。纯前端验证，邮箱地址不上传服务器保护数据隐私。""",
    "file-upload-compress": """免费在线文件压缩工具，支持拖拽上传图片、PDF和文档进行无损压缩。智能选择最优压缩算法，大幅减小文件体积同时保持质量，实时预览压缩前后大小对比。所有文件在浏览器本地处理绝不上传，适合网站优化和邮件附件压缩场景。""",
    "html-editor": """免费在线HTML代码编辑器，左侧编写HTML/CSS/JS代码右侧即时渲染预览效果。支持语法高亮、自动缩进、代码格式化、一键下载HTML文件。前端开发学习、网页原型设计和代码调试的在线IDE工具，纯浏览器运行代码不上传服务器保护隐私。""",
    "karnaugh-map-solver": """免费在线卡诺图化简求解器，支持2-6变量的逻辑表达式化简。输入最小项或直接在卡诺图上点击格子，自动生成最简与或式和或与式并显示质蕴含项。数字电路设计和计算机组成原理课程学习的必备辅助工具，纯前端计算无需注册。""",
    "online-stopwatch": """免费在线秒表计时器，高精度毫秒级计时，支持分段计时(Lap)和计次功能。可记录无限次分段时间并导出数据。适合体育训练计时、演讲限时练习、实验计时和烹饪计时等场景。界面简洁大字体显示，支持后台运行保持计时，无需安装App。""",
    "pdf-page-deleter": """免费在线PDF页面删除工具，上传PDF文件后预览所有页面缩略图，点击即可选择删除指定页面。支持多选批量删除，删除后即时预览效果并下载新PDF。完全浏览器端使用pdf-lib引擎处理，PDF文件绝不上传服务器保护文档隐私。""",
    "placeholder-text-generator": """免费在线占位文本生成器(Lorem Ipsum)，一键生成中文乱数假文和英文Lorem Ipsum占位文本。支持自定义段落数、句子数和字数，可生成HTML格式带标签的占位内容。UI设计师和前端开发做原型页面时快速填充占位文字的实用工具。""",
    "post-office-calculator": """免费在线邮局存款计算器，计算印度邮局定期存款(RD/TD/MIS/PPF/SCSS)的到期本息金额和利息收入。支持各种邮局储蓄方案利率对比，帮助印度居民规划邮局理财投资。纯前端计算无需注册，数据不上传服务器。""",
    "pythagorean-calculator": """免费在线勾股定理计算器，输入直角三角形任意两条边的长度，自动计算第三条边。同时计算三角形面积、周长和内角角度，显示完整计算步骤和公式推导。中学数学学习、建筑测量和木工DIY中快速验证直角三角形的实用在线计算工具。""",
    "query-string-parser": """免费在线URL查询字符串解析工具，将URL中的查询参数一键解析为键值对表格。支持URL编码自动解码、参数编辑和重新生成查询字符串。前端开发者调试API接口参数和SEO分析URL结构的必备在线小工具，纯浏览器运行无需注册。""",
    "quick-ratio": """免费在线速动比率(酸性测试比率)计算器，输入企业流动资产、存货和流动负债，一键计算速动比率评估企业短期偿债能力。速动比率大于1说明企业不依赖存货即可偿还短期债务。财务分析师和投资者评估公司流动性风险的核心在线指标工具。""",
    "resolution-calculator": """免费在线屏幕分辨率计算器，输入屏幕宽度和高度自动计算纵横比、总像素数(MP)和PPI像素密度。内置iPhone/iPad/安卓/4K显示器等常见设备分辨率预设。UI设计师和前端开发者确定屏幕适配方案及计算设备像素比的实用在线工具。""",
    "rule-of-72-calculator": """免费在线72法则计算器，根据年化收益率快速估算投资本金翻倍所需的年数（72÷年利率）。同时支持反向计算：已知目标翻倍年限推算所需年化收益率。理财入门者快速评估复利投资增长潜力的简便工具，纯前端计算无需注册。""",
    "smart-rename": """免费在线智能文件重命名工具，支持按查找替换、添加前缀后缀、插入递增序号和正则表达式四种模式批量重命名。实时预览重命名前后对比效果，一键复制重命名命令。摄影师批量整理照片和开发者重命名代码文件的高效在线工具，纯前端处理数据安全。""",
    "url-extractor": """免费在线URL链接提取器，从文本、HTML代码或网页源码中批量提取所有http/https链接。支持去重、按域名过滤和导出为文本列表。SEO外链分析、网页爬虫开发和竞品链接收集的实用在线工具，纯浏览器运行数据不上传。""",
    "category/health": """免费在线健康计算器工具集，包含BMI体重指数计算器、每日饮水摄入量计算器、排卵期计算器、儿童身高预测、宠物热量计算器、睡眠负债计算器等多种健康管理在线工具。科学管理个人和家庭健康，全部免费无需注册纯前端运行。""",
    "category/text": """免费在线文本处理工具集，包含英文大小写转换、文本去重、文本统计分析、关键词提取、文本排序、文本前后缀添加、智能引号转换等多种文本编辑处理工具。写作者、程序员和SEO内容优化必备的免费文本工具合集。""",
    "color-picker-hex": """免费在线取色器/颜色选择器工具，支持色盘取色、HEX十六进制颜色码输入和RGB/HSL颜色空间转换。点击即可复制颜色值，保存最近使用的颜色历史记录。UI设计师、前端开发者和平面设计师快速选取网页配色的必备在线取色工具。""",
    "countdown": """免费在线倒计时器，设置目标日期和时间后实时显示剩余天数、小时、分钟和秒数。支持自定义倒计时标题和背景颜色，可同时创建多个倒计时。适合活动倒计时、考试倒计时、项目截止日和节日倒计时的全屏大字体显示在线工具。""",
    "css-clip-path-generator": """免费在线CSS Clip-Path裁剪路径生成器，可视化拖拽调整圆形、椭圆、多边形、内凹等裁剪形状的顶点坐标。实时预览裁剪效果，一键复制clip-path CSS代码。前端开发者制作异形图片裁剪、不规则布局和创意动效的CSS可视化编辑在线工具。""",
    "data-uri-to-image": """免费在线Data URI转图片工具，将Base64编码的Data URI字符串还原为PNG/JPG/GIF图片并下载。同时支持反向：图片转Data URI编码。前端开发者处理内联图片、邮件HTML中的图片嵌入和CSS背景图Base64优化的实用在线转换工具。""",
    "domain-name-generator": """免费在线域名创意生成器，输入关键词后自动组合前后缀生成大量可用域名创意。支持.com/.net/.io/.ai等多种顶级域名后缀，筛选短域名和易记域名。创业者寻找品牌域名、独立开发者选择项目域名的域名头脑风暴在线工具。""",
    "dummy-xml-generator": """免费在线模拟XML测试数据生成器，快速生成带自定义标签结构和嵌套层级的XML示例数据。支持自定义根节点、子节点、属性值和重复数量，一键复制XML代码。开发者在API测试和XML解析调试时快速生成测试XML数据的在线工具。""",
    "file-hash-checker": """免费在线文件哈希值校验工具，计算文件的MD5、SHA-1、SHA-256、SHA-512等哈希值。拖拽上传文件即可获得多种哈希算法结果，用于校验文件完整性、验证下载文件未被篡改。软件下载安全验证和数字取证分析场景的在线必备工具。""",
    "fraction-calculator": """免费在线分数计算器，支持分数加减乘除四则运算、约分化简、分数转小数和带分数与假分数互转。显示详细计算步骤和通分过程。小学生分数运算练习、中学数学作业辅导和家长检查数学题的实用在线工具，纯前端计算无需注册。""",
    "gear-ratio-calculator": """免费在线齿轮比计算器，输入输入和输出齿轮的齿数或转速，自动计算齿轮传动比、输出转速和扭矩变化。支持多级齿轮传动系统串行计算。机械工程学生、DIY创客和自行车变速系统调试中的齿轮参数在线计算工具。""",
    "holiday-countdown": """免费在线节假日倒计时器，实时显示距离元旦、春节、清明、端午、中秋、国庆、圣诞节等中外节假日的剩余天数。支持添加自定义纪念日和生日倒计时提醒。规划假期出行和活动安排的节日提醒工具，纯浏览器运行无需注册。""",
    "html-encoder": """免费在线HTML实体编码解码工具，将HTML特殊字符（尖括号、引号、和号等）转换为对应的HTML实体编码（&lt; &gt; &amp; 等）。支持批量编码解码操作，防止XSS跨站脚本攻击。前端开发者在网页中安全嵌入用户内容的HTML转义处理在线工具。""",
    "html-previewer": """免费在线HTML代码实时预览工具，粘贴HTML代码即可即时渲染查看网页效果。支持独立窗口预览和响应式设备模拟功能。前端开发者快速测试HTML片段、调试页面样式和验证HTML代码效果的在线实时预览工具，纯浏览器运行代码不上传。""",
    "html-table-to-json": """免费在线HTML表格转JSON转换器，粘贴HTML table代码或直接粘贴网页表格内容，自动解析为结构化JSON数组格式。支持识别表头行作为JSON键名。前端开发和数据抓取场景中将网页表格数据快速转为JSON结构化数据的在线转换工具。""",
}

count = 0
for tool, new_desc in updates.items():
    fpath = os.path.join(os.path.dirname(__file__), '..', tool, 'index.html')
    if not os.path.exists(fpath):
        print(f"SKIP: {fpath}")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    m = re.search(r'(<meta\s+name="description"\s+content=")([^"]*)(")', content)
    if not m:
        continue

    old_desc = m.group(2)
    old_len = len(old_desc)

    # Replace meta description
    old_meta = f'<meta name="description" content="{old_desc}"'
    new_meta = f'<meta name="description" content="{new_desc}"'
    content = content.replace(old_meta, new_meta, 1)

    # Update og:description if matches
    old_og = f'<meta property="og:description" content="{old_desc}"'
    new_og = f'<meta property="og:description" content="{new_desc}"'
    if old_og in content:
        content = content.replace(old_og, new_og, 1)

    # Update Schema description if matches
    schema_old = f'"description": "{old_desc}"'
    schema_new = f'"description": "{new_desc}"'
    if schema_old in content:
        content = content.replace(schema_old, schema_new, 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    new_len = len(new_desc)
    print(f"OK: {tool} | {old_len} -> {new_len} chars")
    count += 1

print(f"\nTotal: {count} pages updated")
