#!/usr/bin/env python3
"""批量修改meta description，目标140-160字符。短的重写，已OK的保留"""
import re

DESCRIPTIONS = {
    "2048-game": "免费在线玩经典2048数字合成益智游戏，使用键盘上下左右方向键或手机触屏滑动移动方块，相同数字方块碰撞后合并升级，不断挑战直到合成2048方块甚至4096更高分数。支持无限撤销操作、实时最高分记录和移动端触屏完美适配，纯前端实现无需下载安装打开即玩，无需注册完全免费。",

    "ai-copywriting-generator": "免费在线AI智能营销文案生成器，一键创作高质量营销文案、广告宣传语、产品详情描述和社交媒体推文内容。支持多种文案风格和语气灵活切换，完美适配小红书、微信公众号、抖音和Twitter等主流平台格式要求。营销人员、电商运营和自媒体创作者的必备高效写作利器，纯前端处理无需注册。",

    "ai-model-compare": "免费在线AI大模型技术参数对比工具，横向比较GPT-4o、Claude、Gemini和Llama等主流语言模型的参数量、上下文窗口长度、推理速度和模型架构等核心技术规格指标。支持多模型并排对比和差异高亮显示，数据来源公开文档持续更新，AI研究者和开发者进行模型选型决策的权威参考，无需注册。",

    "ai-prompt-generator": "免费在线AI提示词工程生成器，为ChatGPT、Midjourney、DALL-E、Stable Diffusion等主流AI模型一键生成结构化高质量提示词模板。涵盖角色扮演对话、代码生成、文案写作、图片创作等多场景应用，支持参数化构建和实时预览效果。无需注册完全免费，帮助用户快速掌握提示词工程技巧。",

    "ai-text-humanizer": "免费在线AI文本人性化润色工具，将ChatGPT、Claude等AI生成内容智能转化为自然流畅的人类表达风格。支持同义词智能替换、句式结构重组和语气风格精细调整，有效消除机械感和模板化痕迹。适用于学术降AI检测率、商务邮件润色和自媒体内容创作场景，纯前端本地处理保护隐私无需注册完全免费。",

    "airbnb-income-calculator": "免费在线Airbnb短租民宿收入计算器，输入每晚房价、预计月度入住率和运营成本，自动精准计算月收入、年收入和投资回报率ROI。支持淡旺季价格调整、清洁费和管理费核算，帮助房东科学评估短租房产收益潜力。纯前端本地计算，数据不上传服务器，无需注册完全免费。",

    "api-changelog-generator": "免费在线API变更日志自动生成器，根据API端点变更内容快速生成规范化的开发者changelog文档。支持语义化版本号管理、Markdown格式化输出和变更类型分类（新增功能接口、修改参数、废弃旧API、Bug修复）。开发团队维护API文档和发布说明的必备效率工具，纯前端无需注册。",

    "api-key-generator": "免费在线API密钥安全生成器，一键生成高强度的随机API密钥和访问令牌字符串。支持自定义密钥长度（8至128位）、前缀标识和字符集组合（大小写字母+数字+特殊符号），可批量生成多个密钥并一键复制导出。纯前端浏览器本地运行，密钥绝不经过网络传输，无需注册完全免费。",

    "api-rate-limit-calculator": "免费在线API速率限制策略计算器，精确计算请求配额、限流时间窗口、最大并发连接数和每秒查询率QPS等核心参数。支持令牌桶、漏桶、固定窗口计数器和滑动窗口日志四种主流限流算法的实时对比分析。帮助后端开发者设计合理API限流策略，纯前端无需注册。",

    "api-status-dashboard": "免费在线API端点状态实时监控仪表盘，同时检测多个API接口的可用性、响应延迟时间和HTTP状态码。支持定时自动检测（可设30秒、1分钟或5分钟间隔）、历史记录追踪和可用性百分比统计，可视化图表直观展示响应趋势变化。纯前端运行保护隐私数据，无需注册。",

    "api-tester": "免费在线API接口测试调试工具，支持GET、POST、PUT、DELETE等全部HTTP方法。可自定义请求Headers、Body内容（JSON/XML/Form）和查询参数，实时查看响应状态码、响应头和返回数据，支持JSON格式化预览。适合前后端联调和API开发调试，纯前端无需注册完全免费。",

    "apri-calculator": "免费在线APRI无创肝纤维化评分计算器，基于AST转氨酶和血小板计数的比值指数快速评估肝纤维化和肝硬化风险程度。适用于慢性丙型肝炎和NAFLD非酒精性脂肪肝患者的初步筛查。采用国际公认的AST-Platelet Ratio Index标准公式，纯前端本地计算无需注册。",

    "area-chart-maker": "免费在线面积图生成器，可视化展示多组数据的趋势变化和数量对比。支持堆叠面积图和重叠面积图两种模式灵活切换，渐变色彩填充增强数据视觉表现力。Canvas纯前端高性能渲染，一键导出高清PNG图片用于报告和演示。数据全程不上传服务器，无需注册完全免费。",

    "area-converter": "免费在线面积单位换算转换器，支持平方米、平方千米、公顷、亩、平方英尺、平方英寸、平方码、英亩等30余种国内外面积单位之间的实时相互转换。输入任意数值即刻显示所有单位的精确换算结果。适用于房产测量、土地规划和建筑工程计算场景，纯前端无需注册。",

    "aria-label-generator": "免费在线ARIA无障碍标签代码生成器，快速生成符合WCAG 2.1国际无障碍标准的ARIA属性代码。支持role角色定义、aria-label标签、aria-describedby描述关联等50余种ARIA属性配置，实时预览生成的HTML代码。前端开发者为网站提升无障碍可访问性的必备工具，无需注册。",

    "ascii-art": "免费在线ASCII字符画艺术生成器，将文字和图片智能转换为精美ASCII字符画作品。支持多种经典字体样式选择、自定义字符集密度和亮度精细调节，输出效果细腻生动富有艺术感。适用于终端欢迎界面设计、代码注释装饰和复古风格创意设计场景，一键复制分享无需注册。",

    "ascii-code-converter": "免费在线ASCII码编码转换工具，实现文本字符与ASCII十进制、十六进制、八进制和二进制编码的实时双向互转。支持大小写字母模式切换、批量文本转换和一键复制全部转换结果。程序员编码调试、计算机网络学习和字符编码教学的实用必备工具，纯前端本地处理无需注册完全免费。",

    "ascii-table": "免费在线ASCII码表完整查询参考工具，展示全部128个标准ASCII字符及其十进制、十六进制、八进制和二进制编码对照。支持控制字符与可打印字符分类筛选查看，一键点击复制任意字符编码。程序员日常开发和计算机基础学习的快速编码查询手册，纯前端零依赖无需注册。",

    "ascvd-risk-calculator": "免费在线ASCVD动脉粥样硬化性心血管疾病10年风险评估计算器，严格基于2013 ACC/AHA国际权威指南推荐公式。输入年龄、性别、总胆固醇、HDL胆固醇、收缩压、是否吸烟和是否糖尿病等指标，自动计算10年ASCVD风险百分比。辅助临床决策，纯前端本地计算无需注册。",

    "asset-depreciation-calculator": "免费在线固定资产折旧计算器，支持直线法、双倍余额递减法和年数总和法三种主流折旧方法。输入资产原值、预计残值和使用年限，自动生成每年折旧额、累计折旧和期末账面净值的完整折旧明细表。会计和财务人员固定资产管理与税务筹划的实用工具，无需注册完全免费。",
}

def fix_page(dirname, new_desc):
    path = f"{dirname}/index.html"
    with open(path, 'r') as f:
        content = f.read()
    
    old_meta_re = r'<meta name="description" content="[^"]*"'
    old_meta = re.search(old_meta_re, content)
    if not old_meta:
        print(f"  SKIP {dirname}: no meta description found")
        return False
    
    new_meta = f'<meta name="description" content="{new_desc}"'
    content = content.replace(old_meta.group(0), new_meta)
    
    old_og_re = r'<meta property="og:description" content="[^"]*"'
    old_og = re.search(old_og_re, content)
    if old_og:
        new_og = f'<meta property="og:description" content="{new_desc}"'
        content = content.replace(old_og.group(0), new_og)
    
    schema_re = r'"description":\s*"[^"]*"'
    schemas = list(re.finditer(schema_re, content))
    if schemas:
        new_schema_desc = f'"description": "{new_desc}"'
        content = content[:schemas[0].start()] + new_schema_desc + content[schemas[0].end():]
    
    with open(path, 'w') as f:
        f.write(content)
    return True

if __name__ == '__main__':
    all_ok = True
    count = 0
    for dirname in sorted(DESCRIPTIONS.keys()):
        desc = DESCRIPTIONS[dirname]
        desc_len = len(desc)
        in_range = 140 <= desc_len <= 160
        if not in_range:
            all_ok = False
        ok = fix_page(dirname, desc)
        status = f"{desc_len} chars {'✓' if in_range else '⚠'}"
        if ok:
            count += 1
        print(f"  {dirname}: {status}")
    
    print(f"\nFixed {count} pages. All in range: {all_ok}")