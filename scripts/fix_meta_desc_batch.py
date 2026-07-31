#!/usr/bin/env python3
"""Batch fix meta descriptions for SEO optimization"""
import os, re, sys

# Each entry: (file, old_desc_snippet, new_desc)
# old_desc_snippet is a unique substring to match
PATCHES = [
    # --- 57-char group ---
    ("body-mass-index/index.html",
     '免费在线BMI（身体质量指数）计算器。输入身高和体重，自动计算BMI值和健康类别。支持公制/英制单位。纯前端处理。',
     '免费在线BMI身体质量指数计算器，输入身高体重自动计算BMI值和健康类别（偏瘦/正常/超重/肥胖），支持公制与英制单位切换。科学评估体重状况，无需注册完全免费。'),

    ("c-formatter/index.html",
     '免费在线C/C++代码格式化工具，自动调整缩进、规范空格、对齐大括号、移除多余空行。纯前端处理，代码不上传服务器。',
     '免费在线C/C++代码格式化工具，自动调整缩进对齐大括号、规范空格、移除多余空行，支持一键压缩。浏览器本地处理代码安全不上传，程序员和嵌入式开发者必备。'),

    ("chronotype-quiz/index.html",
     '通过科学的睡眠类型测试，发现你是熊、狮子、狼还是海豚型睡眠者。了解你的生物钟节律，优化你的作息时间，提高睡眠质量。',
     '免费在线睡眠类型测试（Chronotype Quiz），通过科学问卷发现你是熊、狮子、狼还是海豚型睡眠者。了解生物钟节律，优化作息安排，提升睡眠质量和白天精力。'),

    ("country-flag-finder/index.html",
     '免费在线国家旗帜查找器，支持按国家名称搜索、按大洲筛选，查看各国国旗、首都、货币、人口等信息。无需注册，无需注册。',
     '免费在线国家旗帜查找器，支持按国家名称搜索、按大洲筛选，查看各国国旗、首都、货币、人口和官方语言。地理学习和国际商务参考必备，无需注册。'),

    ("css-calc-builder/index.html",
     '免费在线CSS calc()表达式构建器，可视化构建calc计算公式，支持加减乘除、混合单位、实时预览。无需注册。',
     '免费在线CSS calc()表达式构建器，可视化构建calc计算公式，支持加减乘除和vh/vw/em/rem/%混合单位运算，实时预览计算结果。前端布局利器无需注册。'),

    ("date-time-calculator/index.html",
     '免费在线日期时间计算器，计算两个日期之间的天数差、日期加减、时间差计算、工作日计算。支持日期转时间戳，纯前端计算。',
     '免费在线日期时间计算器，计算两个日期之间的天数差、时间差和N天前后的日期，支持工作日/自然日两种模式。项目排期、纪念日倒计时和工龄计算的实用工具。'),

    ("dividend-growth-calculator/index.html",
     '免费在线股息增长计算器，计算股息增长率、未来股息金额、股息翻倍年限。支持当前股息、增长率、持有年限参数，无需注册。',
     '免费在线股息增长计算器，输入当前股息和年均增长率，自动计算未来股息金额、股息翻倍年限和累计分红收入。股息投资策略评估利器，股票投资者必备。'),

    ("emojify/index.html",
     '免费在线文字转Emoji工具，将普通文字转换为表情符号。支持字母、数字、符号到emoji的一键转换，让文字更有趣。',
     '免费在线文字转Emoji工具（Emojify），将字母、数字和符号一键转换为对应的表情符号。支持复制到社交媒体和聊天软件，让文字更生动有趣，无需注册。'),

    ("expense-ratio-calculator/index.html",
     '免费在线基金费率计算器。计算基金管理费、托管费等长期持有成本，比较不同基金费率对收益的影响，免费在线工具，无需注册',
     '免费在线基金费率计算器，计算基金管理费、托管费等长期持有成本对最终收益的侵蚀效应。输入投资额、年化收益率和费率，直观对比不同基金费率对复利收益的影响。'),

    ("favicon-extractor/index.html",
     '免费在线Favicon提取工具，输入网址即可提取网站favicon图标，支持多种尺寸下载。无需注册，不上传服务器。',
     '免费在线网站Favicon提取工具，输入任意网址自动提取网站图标，支持16×16至256×256多种尺寸下载。网页设计师和前端开发获取网站图标资源的便捷工具。'),

    ("file-encryption/index.html",
     '免费在线文件加密工具，使用AES-256-GCM算法加密任意文件，支持密码保护和文件下载。无需注册，不上传服务器。',
     '免费在线文件加密工具，使用AES-256-GCM军事级加密算法保护任意类型文件，设置密码即可加密和解密。浏览器本地处理文件不上传，敏感文档安全加密必备。'),

    ("grocery-list/index.html",
     '免费在线购物清单工具，按分类管理蔬菜、水果、肉类等购物项，支持勾选已完成和分类筛选。纯前端存储，数据不上传服务器。',
     '免费在线购物清单工具，按蔬菜、水果、肉类、乳制品等分类管理采购项，支持勾选已购和分类筛选。数据纯前端本地存储，日常超市采购和家庭备货清单好帮手。'),

    ("growth-stock-calculator/index.html",
     '免费在线成长股估值计算器。通过PEG、PS、PB等指标评估成长股的合理估值，帮助投资者判断高成长公司是否值得投资。',
     '免费在线成长股估值计算器，通过PEG市盈增长比、PS市销率和PB市净率多维度评估高成长公司的合理估值区间。帮助股票投资者判断成长股是否被高估或低估。'),

    ("handwriting-generator/index.html",
     '免费在线手写体文字生成器，多种手写风格字体一键生成。可调颜色背景墨迹，纯前端即用即走，无需注册，数据不上传服务器。',
     '免费在线手写体文字生成器，提供多种逼真手写风格字体一键生成。可调节文字颜色、背景和墨迹效果，适合社交媒体配图、贺卡设计和个性化签名，无需注册。'),

    ("house-affordability-calculator/index.html",
     '免费在线买房能力计算器，根据年收入、首付比例、贷款利率自动计算你能买得起多少钱的房子和月供金额，帮你规划购房预算。',
     '免费在线买房能力计算器，根据年收入、首付比例和贷款利率自动计算可负担房屋总价和月供金额。支持28/36负债比率规则，帮助首次购房者科学规划购房预算。'),

    ("html-to-pug/index.html",
     '免费在线HTML转Pug(Jade)模板转换器。将HTML代码一键转换为Pug语法，纯前端处理，数据不上传服务器。',
     '免费在线HTML转Pug(Jade)模板转换器，将HTML代码一键转换为简洁的Pug缩进语法。支持属性转换和嵌套结构保留，Node.js前端开发者的效率工具。'),

    ("hvac-size/index.html",
     '免费在线空调/暖气容量计算器，按房屋面积、层高、气候、保温和窗户朝向自动计算BTU/kW/匹数/吨数，含机型推荐。',
     '免费在线空调暖气容量计算器，按房屋面积、层高、气候区域、保温等级和窗户朝向自动计算所需BTU/kW/匹数，含分体式和中央空调机型推荐。装修和暖通选型必备。'),

    ("intrinsic-value-calculator/index.html",
     '免费在线内在价值计算器，基于DCF折现现金流模型，输入自由现金流、增长率和折现率计算股票内在价值。纯前端本地计算。',
     '免费在线股票内在价值计算器，基于巴菲特推崇的DCF折现现金流模型，输入自由现金流、增长率和折现率计算公司内在价值。价值投资者评估股票是否被低估的决策工具。'),

    ("kpi-calculator/index.html",
     '免费在线KPI计算器，快速计算关键绩效指标完成率和达成率，支持同比环比分析、目标对比、趋势预测。商业分析必备工具。',
     '免费在线KPI计算器，快速计算关键绩效指标完成率和达成率，支持同比环比增长率分析、目标达成对比和增长趋势预测。销售团队业绩追踪和运营数据分析必备。'),

    ("kubernetes-yaml-validator/index.html",
     '在线验证Kubernetes YAML配置文件，检查Deployment/Service/Pod等资源格式是否正确',
     '免费在线Kubernetes YAML验证器，检查Deployment、Service、Pod等K8s资源清单的格式正确性和字段合法性。DevOps工程师部署前校验配置文件的必备工具。'),

    ("lifestyle-spending-calculator/index.html",
     '免费在线生活支出计算器，帮助追踪和分类您的日常消费。支持50/30/20预算规则，自动计算各项支出占比和储蓄建议。',
     '免费在线生活支出计算器，追踪和分类日常消费，支持50/30/20预算法则自动计算需求/想要/储蓄占比。个人理财规划和消费习惯改善的实用工具，无需注册。'),

    ("marginal-tax-calculator/index.html",
     '边际税率计算器，计算在不同收入水平下新增收入的纳税比例。帮助理解税率阶梯效应，优化收入规划，免费在线工具，无需注册',
     '免费在线边际税率计算器，计算不同收入水平下新增收入的实际纳税比例。帮助理解税率阶梯效应，优化年终奖和副业收入规划，个税筹划和薪资谈判必备工具。'),

    ("pdf/index.html",
     '免费在线PDF工具集 — 合并、压缩、转换、拆分、提取文字、编辑PDF。纯浏览器处理，文件不上传服务器，无需注册。',
     '免费在线PDF工具集，提供PDF合并、压缩、转换格式、拆分页面、提取文字、编辑元数据和加密解锁等46+实用功能。浏览器本地处理文件安全不上传，办公必备。'),

    ("pig-latin/index.html",
     '免费在线Pig Latin翻译器，将英文文本转换为Pig Latin语言或反向翻译，支持多种规则，纯前端本地运行。',
     '免费在线Pig Latin翻译器，将英文文本一键转换为Pig Latin密语或反向解码回英文。支持标准规则和多种变体，语言游戏爱好者和英语教学趣味工具。'),

    ("pink-noise-generator/index.html",
     '免费在线粉红噪音发生器，帮助专注工作、放松睡眠。可调音量，纯前端生成无需注册，支持后台播放，免费在线工具，无需注册',
     '免费在线粉红噪音发生器，产生自然均衡的粉红噪声帮助深度专注、放松入睡和屏蔽环境噪音。可调节音量，支持后台播放，白噪音替代方案无需注册。'),

    ("random-text-generator/index.html",
     '免费在线随机文本生成器，支持随机汉字、英文单词、句子、段落生成。可自定义长度和数量，适用于测试数据生成和占位文本。',
     '免费在线随机文本生成器，一键生成随机中文汉字、英文单词、句子和段落。可自定义字符长度和生成数量，适用于UI占位文本填充和数据库测试数据生成。'),

    ("real-return-calculator/index.html",
     '免费在线实际回报率计算器。扣除通货膨胀后计算投资的真实购买力增长，了解你的钱真正增值了多少，免费在线工具，无需注册',
     '免费在线实际回报率计算器，扣除通货膨胀后精确计算投资的真实购买力增长。输入名义收益率和通胀率，直观看到财富是否真正增值，长期投资规划必备工具。'),

    ("regex-debugger/index.html",
     '免费在线正则表达式调试器，实时高亮匹配结果，支持捕获组可视化、匹配详情、常用正则模板。纯前端本地运行，数据不上传。',
     '免费在线正则表达式调试器，输入正则和测试文本实时高亮匹配结果，支持捕获组可视化、匹配详情和常用正则模板。程序员编写调试正则的效率利器无需注册。'),

    ("responsive-tester/index.html",
     '免费在线响应式设计测试工具。输入网址即可在手机、平板、笔记本、桌面等不同设备尺寸下预览网页效果。前端开发必备工具。',
     '免费在线响应式设计测试工具，输入网址即可模拟iPhone、iPad和各种桌面分辨率预览网页效果。前端开发者调试移动端适配和断点布局的必备工具。'),

    ("roman-numerals-converter/index.html",
     '免费在线罗马数字转换器，支持十进制与罗马数字互相转换，支持1-3999范围，即时双向转换，一键复制结果，无需注册。',
     '免费在线罗马数字转换器，支持十进制阿拉伯数字与罗马数字双向互转（1-3999范围），输入即时转换一键复制。数学学习和历史文献阅读的实用工具。'),
]

print(f"Total patches: {len(PATCHES)}")

for filepath, old_snippet, new_desc in PATCHES:
    fullpath = os.path.join('/home/chison/tools-site', filepath)
    try:
        with open(fullpath, 'r') as f:
            content = f.read()
        
        if old_snippet not in content:
            print(f"SKIP {filepath}: old snippet not found")
            continue
        
        # Find the exact meta description tag and replace it
        pattern = re.compile(r'<meta name="description" content="' + re.escape(old_snippet) + r'">')
        if not pattern.search(content):
            print(f"SKIP {filepath}: pattern not matched exactly")
            continue
        
        new_content = pattern.sub(
            f'<meta name="description" content="{new_desc}">',
            content
        )
        
        with open(fullpath, 'w') as f:
            f.write(new_content)
        
        print(f"OK {filepath}: {len(old_snippet)}c -> {len(new_desc)}c")
    except Exception as e:
        print(f"ERR {filepath}: {e}")

print("DONE")