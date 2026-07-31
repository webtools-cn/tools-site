#!/usr/bin/env python3
"""批量为meta description太短的CN页面生成并替换SEO描述（目标140-160字符）"""
import re

UPDATES = {
    "yaml-path-finder": (
        "免费在线YAML路径查找器，输入YAML配置文档和路径表达式快速定位并提取嵌套数据。支持点号语法访问嵌套键、方括号语法访问数组元素和通配符匹配多个节点，一键列出文档中所有数据路径并导出结果。所有解析在浏览器本地完成，无需注册下载，保障配置文件数据安全不泄露。",
    ),
    "youtube-timestamp-link": (
        "免费在线YouTube视频时间戳链接生成器，输入YouTube视频URL和指定的时间点，自动生成带时间戳参数的直达分享链接。支持时分秒精确输入和总秒数两种模式，点击链接直接跳转到视频指定位置。适合分享教程重点、会议录像关键节点或精彩片段，无需注册，一键复制链接即可使用。",
    ),
    "word-counter-online": (
        "免费在线字数统计工具，实时精确统计输入文本的字数、字符数（含和不含空格）、英文单词数、行数和段落数。全面支持中英文及混合文本计数，提供基于不同阅读速度的阅读时间估算。所有统计计算在浏览器本地完成，文本不上传服务器。适合写作、翻译校对、SEO内容优化和社交媒体文案编辑场景。",
    ),
    "wrap-text": (
        "免费在线文本换行格式化工具，按指定列宽自动将长文本拆分为多行显示。提供硬换行精确断行、软换行保持单词完整和单词边界换行三种模式，灵活适应不同需求。支持自定义添加行号和每行缩进空格数，方便嵌套引用和代码对齐。适用于电子邮件正文78列标准格式化、代码注释对齐和纯文本文档排版，无需注册即用。",
    ),
    "essay-outline-generator": (
        "免费在线论文大纲生成器，为学术论文、研究文章和课程作业快速创建I-II-III级结构化层级大纲。支持议论文、分析性论文、研究论文、对比论文和因果分析论文等多种类型，一键生成包含引言、主体段落和结论的完整写作框架。纯前端运行无需注册下载，适合学生和研究人员高效规划论文结构和逻辑脉络。",
    ),
    "macro-calculator-advanced": (
        "免费在线高级宏量营养素计算器，根据您的体重、身高、年龄、日常运动量和健身目标精确计算每日所需蛋白质、碳水化合物和脂肪的克数目标。支持增肌、减脂、维持体重和低碳高蛋白等多种饮食模式，提供科学的每餐营养分配建议。所有计算在浏览器本地完成，无需注册，适合健身爱好者和营养规划者日常使用。",
    ),
    "sass-to-css": (
        "免费在线Sass/SCSS转CSS实时编译工具，全面支持.scss和.sass两种语法格式，输入Sass代码即可即时编译为标准CSS输出。提供expanded展开和compressed压缩两种输出风格，自动检测并显示编译错误的行号和详细提示方便排查。所有代码在浏览器本地处理，绝不上传到任何服务器，保障您的样式代码绝对安全。无需注册。",
    ),
    "dividend-yield-calculator": (
        "免费在线股息率计算器，输入股票当前市场价和每股年度派息金额，实时自动计算股息率、股息支付率和年化分红收益。支持同时添加多只股票进行横向对比分析，帮助价值投资者快速评估股票的分红投资回报率。所有计算在浏览器本地完成，数据不上传服务器，无需注册即可免费使用，适合股票投资者日常研究。",
    ),
    "time-tracker": (
        "免费在线工作时间追踪器，支持创建多个项目并独立计时管理，提供开始、暂停、继续和标记完成等完整操作。可按自定义标签分类筛选工时记录，自动汇总每日和每周的工作时长统计数据。支持将时间记录导出为CSV格式详细报告方便报销或分析。所有数据保存在浏览器本地存储中，纯前端运行完全无需注册账号。",
    ),
    "credit-utilization-calculator": (
        "免费在线信用卡使用率计算器，输入每张信用卡的信用额度和当前欠款余额，自动计算单卡和总体信用利用率及对信用评分的潜在影响等级。支持管理多张信用卡同时对比分析，实时显示使用率健康度评估和建议。帮助合理规划信用卡使用策略，所有计算在浏览器本地完成，数据不上传服务器无需注册。适合信用管理。",
    ),
    "google-font-previewer": (
        "免费在线Google Fonts字体预览和对比工具，实时浏览和预览Google Fonts开源字体库中上千款精选网页字体。支持输入自定义预览文本内容，自由调节字体大小、字重粗细和字体颜色样式。一键复制字体CSS引入代码，方便快速集成到网页项目中。适合网页设计师、前端开发者和UI设计师进行字体选型、搭配测试和排版方案对比。",
    ),
    "localstorage-viewer": (
        "免费在线LocalStorage浏览器和管理工具，实时读取并清晰展示当前网站在浏览器中的所有localStorage存储键值对数据。支持按关键字快速搜索和过滤存储条目，可直接在线编辑修改任意键的值并实时生效。提供批量删除选中条目和一键导出完整JSON格式备份功能。前端开发调试和排查存储问题的必备利器，无需安装任何浏览器扩展。",
    ),
    "decimal-to-percent": (
        "免费在线小数与百分比双向实时转换计算器，输入任意小数数值自动即时显示对应的百分比结果，反之输入百分比数值也能自动换算回小数形式。支持高精度多位小数精确换算，转换结果即时显示无需点击按钮。适用于数学作业辅导、数据报表百分比分析、成绩评分换算、打折促销计算和财务报表比率分析等各种日常计算场景，无需注册完全免费。",
    ),
    "email-generator": (
        "免费在线测试邮箱地址生成器，一键快速生成随机且逼真的测试用电子邮箱地址。支持自定义邮箱域名的前缀后缀设置，可批量一次性生成多个不同的测试邮箱地址满足批量测试需求。所有邮箱在浏览器端纯本地生成，绝不存储和记录任何生成的邮箱数据。适合软件开发和QA工程师进行注册流程验证、自动化测试和邮件系统调试等场景。",
    ),
    "lifetime-earnings-calculator": (
        "免费在线终身总收入计算器，输入当前年薪水平、已工作年限、预期退休年龄和预估年薪增长率，科学估算整个职业生涯的总收入金额。计算模型综合考虑薪资复利增长效应和长期通货膨胀影响因素，提供更真实的总收入预估。帮助进行长期职业规划、退休财务准备和人生重要财务决策。纯前端计算保障个人财务数据安全，无需注册。",
    ),
    "calories-burned-calculator": (
        "免费在线运动卡路里消耗计算器，基于MET代谢当量科学标准估算100多种日常运动和健身项目的热量消耗。涵盖跑步、游泳、骑行、跳绳、力量训练、瑜伽和各种球类运动等常见项目。只需输入个人体重和运动持续时长即可即时计算卡路里消耗数值。支持同时添加多种运动累计总消耗热量，纯前端计算无需注册，适合健身减重规划。",
    ),
    "css-validator": (
        "免费在线CSS代码验证和语法错误检测工具，实时检查CSS代码中的语法错误、缺失的大括号花括号、无效的属性值和存在浏览器兼容性问题的过时前缀。精确显示每个错误的类型、所在行号和具体修复建议。全面支持CSS3最新特性验证包括Grid、Flexbox和自定义属性等。所有代码在浏览器本地完成检测，绝不上传服务器保障代码安全隐私。",
    ),
    "image-blur-tool": (
        "免费在线图片模糊处理工具，支持高斯模糊算法和像素化马赛克两种专业模糊效果。可通过滑块实时调节模糊强度参数并即时预览画面效果，处理完成后一键下载保存处理后的图片。所有图像处理运算在浏览器本地完成，无需将图片上传到任何服务器。适合制作网页背景虚化图、遮挡图片中隐私敏感信息和创建像素化艺术效果等场景，无需注册。",
    ),
    "markdown-link-checker": (
        "免费在线Markdown链接有效性检查工具，自动智能提取Markdown文档中所有超链接URL和锚点引用，然后逐一验证每个链接的HTTP响应状态码来检测死链和失效链接。支持检测重复出现的链接、无效锚点跳转和相对路径引用。清晰显示每个链接的检查状态和响应码。适合技术文档维护、开源项目README质量检查和博客文章发布前的链接完整性审核验证。",
    ),
    "css-grid-inspector": (
        "免费在线CSS Grid布局可视化交互构建工具，通过直观的图形界面设置网格容器的列数、行数、列间距和行间距等核心参数。实时预览网格布局的视觉效果并自动生成对应的完整CSS Grid代码。支持调整网格项目的对齐方式和跨行列设置。无需手动记忆和编写复杂的Grid语法，特别适合CSS初学者学习Grid布局原理和有经验的前端开发者快速原型设计验证。",
    ),
}

for slug, (new_meta,) in UPDATES.items():
    print(f"{slug}: {len(new_meta)} chars")

def update_file(filepath, slug):
    new_meta, = UPDATES[slug]
    with open(filepath, 'r') as f:
        content = f.read()
    
    made_change = False
    for _ in range(2):  # Two passes for different patterns
        # Pattern 1: <meta name="description" content="OLD"/>
        pattern_meta = re.compile(
            r'(<meta\s+name="description"\s+content=")([^"]*)(")',
            re.IGNORECASE
        )
        m = pattern_meta.search(content)
        if m:
            content = content[:m.start(2)] + new_meta + content[m.end(2):]
            made_change = True
        
        # Pattern 2: <meta property="og:description" content="OLD"/>
        pattern_og = re.compile(
            r'(<meta\s+property="og:description"\s+content=")([^"]*)(")',
            re.IGNORECASE
        )
        m = pattern_og.search(content)
        if m:
            content = content[:m.start(2)] + new_meta + content[m.end(2):]
            made_change = True
        
        # Pattern 3: Schema.org description
        pattern_schema = re.compile(
            r'("description"\s*:\s*")([^"]*)(")',
            re.IGNORECASE
        )
        m = pattern_schema.search(content)
        if m:
            content = content[:m.start(2)] + new_meta + content[m.end(2):]
            made_change = True
    
    if made_change:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✓ {slug}: {len(new_meta)} chars")
    return made_change

if __name__ == "__main__":
    count = 0
    for slug in UPDATES:
        filepath = f"{slug}/index.html"
        try:
            if update_file(filepath, slug):
                count += 1
        except FileNotFoundError:
            print(f"  ✗ {slug}: file not found")
    print(f"\nUpdated {count} files.")