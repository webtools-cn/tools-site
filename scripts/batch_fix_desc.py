#!/usr/bin/env python3
"""
Batch fix meta descriptions for CN tool pages with <70 chars.
Strategy: extend existing desc to 100-160 chars by appending standard suffixes.
For each file: read existing desc, append "无需注册完全免费" or context-aware suffix.
"""
import os, re

# Tools and their new descriptions (hand-crafted, context-aware)
# Format: {slug: new_description}

fixes = {
    'smart-quotes-converter': '免费在线智能引号转换器，一键将直引号转为弯引号，完美支持中文全角引号「」和英文半角引号""。适合博客写作、学术论文排版和专业排版场景，纯前端本地处理，数据不上传，无需注册完全免费。',
    
    'iban-validator': '免费在线IBAN国际银行账户号码验证工具，验证IBAN格式正确性并执行MOD-97校验和验证，自动识别所属国家代码和银行分行信息。支持欧洲及全球80+国家IBAN格式，跨境汇款、国际支付必备，纯前端本地处理保障数据安全，无需注册完全免费。',
    
    'insulin-dosage-calculator': '免费在线胰岛素剂量计算器，根据碳水化合物摄入量和当前血糖水平精准计算胰岛素注射用量。支持基础胰岛素和餐时胰岛素两种模式，可自定义胰岛素敏感因子和碳水系数，帮助1型及2型糖尿病患者科学管理血糖。纯前端本地计算，数据不上传，无需注册。',
    
    'keyboard-event-tester': '免费在线键盘事件测试工具，实时显示按键的key、keyCode、code和which值及修饰键状态，记录完整键盘事件日志。前端开发者调试快捷键、键盘交互和游戏控制的必备利器。纯前端本地运行，数据不上传服务器，无需注册完全免费。',
    
    'mirror-text': '免费在线镜像文字生成器，一键将文字进行左右翻转镜像处理，生成有趣的倒影文字效果。支持即时预览和一键复制，适合社交媒体创意文案、Logo设计和艺术字体创作。纯前端浏览器本地处理，数据不上传服务器，无需注册完全免费。',
    
    'nutrition-analyzer': '免费在线食物营养成分查询分析工具，搜索常见食物查看详细营养数据，包括热量卡路里、蛋白质、脂肪、碳水化合物、维生素和矿物质含量。适合减脂健身人群、营养师和饮食管理者查询食物营养信息。数据来源于权威营养数据库，纯前端查询无需注册。',
    
    'password-strength': '免费在线密码强度检测工具，从密码长度、字符类型组合和复杂度三个维度分析密码安全性，评估破解需时并检测123456、password等常见弱密码模式。提供密码改进建议帮你创建强密码。纯浏览器本地分析，密码不上传服务器，无需注册。',
    
    'pdf-to-jpg': '免费在线PDF转JPG图片工具，将PDF文档页面转换为高质量JPG图片，支持自定义选择页面范围、输出图片质量调节和批量导出独立JPG文件。适合提取PDF中的图表、合同扫描件和设计稿。纯浏览器本地处理，PDF文件不出电脑，安全可靠无需注册。',
    
    'percentage-difference': '免费在线百分比差异计算器，以两数值平均值为基准对称计算百分比差异率，自动输出绝对差异和相对差异。适用于统计数据分析、科学实验误差计算和财务数据同比环比对比。纯前端本地计算，数据不上传服务器，无需注册完全免费。',
    
    'personality-test': '免费在线人格类型测试工具，基于经典心理学理论设计，从性格特征、思维方式和行为偏好等维度全面分析你的个人特质。适合自我认知探索、职业倾向评估和团队协作角色分析。纯前端本地运行，测试数据不上传服务器，无需注册完全免费。',
    
    'proportion-calculator': '免费在线比例计算器，快速求解比例方程A:B=C:D，输入任意三个值即可算出第四项。支持比例缩放、分数化简和比例转换功能，附带详细分步解题过程。适合数学学习辅导、工程设计配比和日常比例换算。纯前端计算，数据不上传，无需注册。',
    
    'quadratic-formula-calculator': '免费在线一元二次方程计算器，输入系数a、b、c即可快速求解ax²+bx+c=0的所有根。自动展示判别式Δ分析、实根与虚根区分及详细解题步骤。适合中学生数学作业辅导、教师课堂教学演示和工程数学计算。纯客户端本地计算，无需注册完全免费。',
    
    'rag-pipeline-builder': '免费在线RAG检索增强生成管道构建器，可视化为大语言模型设计RAG工作流。支持文档分块策略配置、嵌入模型选择、向量数据库配置和检索参数调优，一键导出完整配置文件。适合AI工程师搭建LLM知识库问答系统，纯前端无需注册。',
    
    'sleep-calculator': '免费在线睡眠周期计算器，基于90分钟睡眠周期科学原理，精准计算最佳入睡时间和自然醒起床时间。支持就寝模式和起床模式双向推算，帮你规划高质量睡眠，醒来精力充沛。适合失眠改善、倒班工作者和跨时区旅行调整时差使用，无需注册。',
    
    'sleep-cycle-calculator': '免费在线睡眠周期科学计算器，基于90分钟REM-NREM睡眠周期理论，帮助你找到最佳入睡时间或起床时间。输入起床时间自动推算入睡窗口，避免在深睡阶段被闹钟吵醒。改善睡眠质量、告别早起疲惫感，纯前端运行无需注册。',
    
    'sleep-optimal-calculator': '免费在线最佳睡眠时间计算器，基于睡眠周期科学精准计算最佳入睡和起床时间窗口。支持REM快速眼动和深度睡眠阶段分析，帮你错过深睡时段实现自然醒。适合睡眠质量改善、倒时差调整和科学作息规划，无需注册完全免费。',
    
    'sudoku': '免费在线数独谜题生成器，自动生成简单、中等、困难三种难度级别数独，支持候选数标记、即时验证和智能提示功能。可一键打印纸质版数独，适合数独爱好者日常脑力训练、逻辑推理能力提升和儿童数学思维培养。纯前端本地生成，无需注册。',
    
    'swift-code-validator': '免费在线SWIFT/BIC银行代码验证查询工具，验证国际银行识别代码格式正确性，解析银行名称、所属国家和分行信息。内置8000+全球银行SWIFT代码数据库，支持跨境汇款前验证收款银行信息。纯前端本地查询，数据不上传，无需注册完全免费。',
    
    'synonym-finder': '免费在线英语同义词和反义词查找器，内置丰富本地词库，输入任意英文单词即可快速查找海量同义词与反义词，支持词性分类筛选。适合英语写作润色、雅思托福词汇扩展和学术论文用词多样化。纯浏览器本地处理，查阅隐私安全，无需注册。',
    
    'tailwind-generator': '免费在线Tailwind CSS可视化代码生成器，所见即所得配置Flexbox布局、Grid网格、间距、颜色、排版等实用样式，实时预览渲染效果，一键复制生成的Tailwind CSS类名代码。前端开发者快速搭建页面原型和UI组件的效率工具。纯前端无需注册。',
    
    'text-deduplicator': '免费在线文本去重工具，支持按行去重和整体去重两种高效模式，可选择保留或移除重复项。一键粘贴文本秒级去重，实时统计原始行数、重复行数和去重后剩余行数。适合名单去重整理、SEO关键词去重和数据清洗，纯前端处理保障数据安全。',
    
    'text-entity-extractor': '免费在线文本实体信息提取工具，一键从大段文本中批量提取URL链接、邮箱地址、手机号码、IP地址、身份证号和日期时间等结构化信息。适合数据采集挖掘、信息脱敏处理和文本解析。纯浏览器本地处理，数据不上传服务器，无需注册。',
    
    'text-to-qrcode': '免费在线二维码生成器，一键将文本、网址、WiFi网络配置、联系方式名片等信息生成高清QR二维码。支持嵌入自定义Logo图标、颜色样式自定义、多种尺寸导出和批量生成。适合产品包装、活动海报和共享WiFi密码，纯前端处理。',
    
    'timezone-converter': '免费在线全球时区转换器，支持400+国际时区快速换算，输入日期时间选择来源和目标时区即可即时显示转换结果。适合跨国远程会议安排、国际航班起降时间换算和海外客户沟通。纯浏览器本地计算，无需注册完全免费。',
    
    'truth-table-generator': '免费在线逻辑表达式真值表生成器，支持AND、OR、NOT、XOR、IMPLIES等常用逻辑运算符。输入逻辑表达式即可生成完整真值表，直观展示布尔函数所有输入组合与输出结果。适合数字电路学习、离散数学作业和编程逻辑验证，无需注册。',
    
    'unicode-inspector': '免费在线Unicode字符检查器，输入任意字符即可查看Unicode码位值、字符名称、UTF-8/UTF-16/UTF-32编码、HTML实体表示和所属字符分类等详细信息。适合软件国际化开发、网页编码调试和特殊符号查询。纯前端本地运行，无需注册。',
    
    'vaccination-schedule': '免费在线疫苗接种时间表查询工具，按年龄段清晰展示中国国家免疫规划和美国CDC推荐的儿童及成人疫苗接种计划。帮助家长科学安排宝宝疫苗接种时间不错过关键免疫窗口期。纯前端查询，数据不上传服务器，无需注册完全免费。',
    
    'vcf-generator': '免费在线VCF电子名片生成器，创建符合vCard 3.0标准的联系人文件。支持填写姓名、电话、邮箱、地址、公司职位和头像等完整字段，一键下载VCF文件直接导入手机通讯录。适合商务社交、展会联系和名片数字化管理，无需注册。',
    
    'viewport-tester': '免费在线响应式视口测试器，输入任意网址即可在手机、平板、桌面等不同设备屏幕分辨率下模拟预览网页显示效果。支持自定义分辨率尺寸和缩放比例调节，前端开发者响应式设计调试和移动端适配测试必备工具，无需注册。',
    
    'year-progress': '免费在线年度进度追踪工具，可视化显示今年已过去的时间百分比和精确到秒的年度倒计时。一目了然查看本年剩余天数、周数和月数。适合年度目标追踪、项目里程碑时间管理和个人复盘激励，无需注册，打开即用。',
}

# Now apply these fixes
count = 0
for slug, new_desc in fixes.items():
    path = f'./{slug}/index.html'
    if not os.path.exists(path):
        print(f'  SKIP: {path} not found')
        continue
    
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find the old description
    old_m = re.search(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])', content)
    if not old_m:
        print(f'  SKIP: {path} no desc found')
        continue
    
    old_desc = old_m.group(2)
    old_len = len(old_desc)
    new_len = len(new_desc)
    
    # Replace
    new_content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    # Also try with single quotes
    if new_content == content:
        new_content = content.replace(
            f"<meta name='description' content='{old_desc}'",
            f"<meta name='description' content='{new_desc}'"
        )
    
    if new_content == content:
        print(f'  FAIL: {path} replace did not match')
        continue
    
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    
    print(f'  OK: {slug} [{old_len}→{new_len}]')
    count += 1

print(f'\nTotal fixed: {count}')
