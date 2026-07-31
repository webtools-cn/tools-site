#!/usr/bin/env python3
"""Bulk fix meta descriptions for 26 short pages"""
import re
import os

BASE = '/home/chison/tools-site'

# Each entry: (file_path, new_meta_description, new_og_description)
FIXES = [
    # ===== 26 short pages =====
    ('./image-sharpener/index.html',
     '免费在线图片锐化工具，一键将模糊照片变清晰。支持调整锐化强度（1-100级），实时预览锐化效果，支持JPG/PNG/WebP格式。采用Canvas卷积算法本地处理，图片绝不上传服务器保护隐私。适合修复拍摄抖动模糊、提升图片细节层次，无需注册即用。',
     '免费在线图片锐化工具，一键将模糊照片变清晰，支持调整锐化强度，实时预览效果，纯前端处理，图片不上传服务器。'),

    ('./website-screenshot/index.html',
     '免费在线网站SEO信息查看器，输入URL一键获取网站元数据：标题、描述、关键词、Open Graph标签、Favicon图标和Twitter Card信息。适合SEO优化人员检测页面标签完整性、开发者检查meta配置，纯前端抓取无需注册安装。',
     '免费在线网站信息查看器，输入URL获取网站标题、描述、关键词、OG标签、favicon等SEO元信息，纯前端抓取无需注册。'),

    ('./lottery-picker/index.html',
     '免费在线随机抽签器/抽奖工具，输入名单或选项即可随机抽取一个或多个结果，支持去重抽取、滚动动画效果和结果导出。适用于年会抽奖活动、课堂随机点名、团建分组决策和游戏队友分配，纯前端运行无需注册。',
     '在线随机抽签工具，输入名单随机抽取，支持去重抽取、滚动动画和多结果抽取，适用于抽奖、分组、决策、年会活动。'),

    ('./whitespace-remover/index.html',
     '免费在线空白字符去除工具，一键清理文本中多余空格、制表符、换行符、零宽字符和全角空格。支持仅删首尾/全部删除/压缩多余空格三种模式，适合代码格式化、数据清洗和文本排版，纯前端处理数据不上传服务器。',
     '免费在线去除空白字符工具，一键清理多余空格、制表符、换行符、零宽字符等，支持多种去除模式，纯前端本地运行。'),

    ('./gig-economy-tax-calculator/index.html',
     '免费在线零工经济/自由职业税务计算器，输入年收入自动计算自雇税（Social Security + Medicare）、联邦所得税和季度预估税额。考虑QBI扣除、业务支出抵扣和标准扣除额，帮助Uber司机和自由职业者规划税务。纯前端计算。',
     '零工经济自由职业税务计算器，自动计算自雇税和联邦所得税，考虑业务扣除和季度预估税，帮您合理规划税务，纯前端计算。'),

    ('./kelvin-to-celsius/index.html',
     '免费在线温度单位换算器，快速将开尔文(K)转换为摄氏度(℃)和华氏度(℉)，支持三种温度单位之间的任意双向换算。实时输入即出结果，附带绝对零度、水的沸点等科学参考值。适合物理化学学习和实验室数据处理，纯前端本地运算。',
     '免费在线温度单位换算器，快速在开尔文(K)、摄氏度(℃)和华氏度(℉)之间双向换算，实时输入即出结果，纯前端本地计算。'),

    ('./health-age-calculator/index.html',
     '免费在线健康年龄计算器，综合评估年龄、BMI体重指数、血压水平、运动频率、吸烟饮酒习惯和睡眠质量等因素，估算您的生理健康年龄。比身份证年龄更真实反映身体状态，帮助及早发现健康风险，纯前端计算数据不上传。',
     '免费健康年龄计算器，综合年龄、BMI、血压、运动习惯和生活方式因素估算生理年龄，比实际年龄更能反映真实健康状况，纯前端计算。'),

    ('./canonical-url-checker/index.html',
     '免费在线Canonical URL检查器，检测任意网页的规范链接标签设置是否正确。输入URL即可查看canonical指向、HTTP头中的Link canonical和重复内容风险，帮助网站管理员排查SEO规范化问题，提升搜索排名，纯前端检测无需注册。',
     '在线Canonical URL检查器，检测网页规范链接设置是否正确，发现重复内容问题，优化SEO排名，免费在线工具无需注册。'),

    ('./paper-size-converter/index.html',
     '免费在线纸张尺寸转换器，查询A系列、B系列、C系列国际标准纸张尺寸，支持毫米/英寸/像素三种单位自由切换。设计师打印排版、印刷品设计、名片制作和展板规划的必备参考工具，支持常用预设尺寸一键查看，纯前端离线可用。',
     '免费在线纸张尺寸转换器，查询A/B/C系列国际标准纸张尺寸，支持mm/英寸/像素转换，打印设计和印刷排版必备工具，纯前端可用。'),

    ('./legal-fee-calculator/index.html',
     '免费在线律师费计算器，快速估算法律咨询、诉讼代理、合同审查和知识产权等法律服务费用。支持按小时费率、固定费用和风险代理三种计费模式，内置常见案件类型费率参考。帮助当事人在委托律师前合理预估维权成本，无需注册。',
     '免费在线律师费计算器，估算法律咨询、诉讼代理和合同审查等法律服务费用，支持按小时/固定/风险代理三种计费模式，无需注册。'),

    ('./json-path-extractor/index.html',
     '免费在线JSON路径提取器，使用JSONPath表达式从复杂JSON数据中精准提取目标字段。支持嵌套对象、数组过滤、通配符匹配和实时结果预览，帮助开发者调试API响应数据和ETL转换。路径语法自动补全，纯前端处理数据不上传。',
     '免费在线JSON路径提取器，支持JSONPath表达式查询复杂JSON数据，实时预览提取结果，路径语法高亮，帮助开发者调试API，数据不上传。'),

    ('./tax-estimator/index.html',
     '免费在线个税估算器，快速计算中国个人所得税，支持月薪/年薪/年终奖多种收入类型的税款估算。涵盖五险一金扣除、专项附加扣除（子女教育/房贷利息等）和最新累进税率表，帮助打工人合理规划税后收入，纯前端计算。',
     '免费在线个税估算器，计算个人所得税支持月薪/年终奖/年薪，含五险一金扣除和专项附加扣除，纯前端计算数据安全。'),

    ('./css-scope-generator/index.html',
     '免费在线CSS @scope规则生成器，可视化创建CSS作用域样式，精确控制样式生效范围。支持设置作用域根选择器和边界限制，实时预览嵌套作用域效果，一键生成标准CSS @scope代码。帮助前端开发者避免样式冲突，提升组件化开发效率。',
     '免费在线CSS @scope生成器，可视化创建CSS作用域规则，支持作用域选择器和嵌套样式，实时预览效果，帮助避免样式冲突。'),

    ('./font-pairing-generator/index.html',
     '免费在线字体搭配生成器，智能推荐Google Fonts中文字体/标题与正文的最佳配对组合。输入字体名称即可预览搭配效果并生成CSS @import代码，支持中英文混排字体、衬线与无衬线对比选择。帮助设计师和前端开发者快速决策字体方案。',
     '免费在线字体搭配生成器，智能推荐标题与正文字体最佳配对组合，预览搭配效果并生成CSS代码，帮助设计决策。'),

    ('./pdf-text-extractor/index.html',
     '免费在线PDF文字提取工具，上传PDF即可逐页提取文字内容，支持复制到剪贴板或下载为TXT纯文本文件。所有处理在浏览器本地完成，PDF文件不上传任何服务器，保护合同、论文等敏感文档隐私安全。无需注册，拖拽即用。',
     '免费在线PDF文字提取工具，上传PDF逐页提取文字内容，支持复制和下载TXT文件，纯前端本地处理保护文档隐私。'),

    ('./video-trimmer/index.html',
     '免费在线视频剪切修剪工具，在浏览器中拖动时间轴截取视频片段，无需上传服务器。支持MP4/WebM/MOV等主流格式，自定义起止时间精准裁剪，实时预览修剪效果。适合短视频制作、社交媒体素材精简和录播课剪辑，纯前端处理。',
     '免费在线视频修剪工具，浏览器中拖动时间轴截取视频片段，支持主流格式，自定义起止时间精准裁剪，纯前端处理不上传。'),

    ('./vocabulary-builder/index.html',
     '免费在线英语词汇量测试工具，通过科学随机抽样方法快速估算您的英语词汇量。覆盖基础到高阶多个难度级别，测试后可查看详细分析报告：词汇量范围、等级评估和学习建议。适合英语自学者摸底水平和备考雅思/托福前评估，无需注册。',
     '免费在线英语词汇量测试，通过随机抽样科学估算英语词汇量，支持多难度级别，提供详细分析报告和学习建议。'),

    ('./opportunity-cost-calculator/index.html',
     '免费在线机会成本计算器，对比不同投资或消费选择之间的潜在收益差异。输入各方案的预期回报率、投资年限和初始金额，自动计算放弃的收益总额。考虑通胀率、税率和风险因素，帮助做出更明智的财务决策，纯前端计算。',
     '免费在线机会成本计算器，对比不同投资选择的潜在收益差异，考虑通胀、税率和风险因素，帮助做更明智的财务决策。'),

    ('./katex-editor/index.html',
     '免费在线KaTeX数学公式编辑器，左侧输入LaTeX语法右侧实时渲染预览数学公式。支持分数、根号、积分、矩阵、求和符号等常用数学表达式，一键复制渲染后的公式代码插入网页或文档。适合学生编写数学作业和教师制作课件，无需注册。',
     '免费在线KaTeX编辑器，实时预览LaTeX数学公式渲染效果，支持分数/根号/积分/矩阵等表达式，一键复制公式代码。'),

    ('./decision-maker/index.html',
     '免费在线决策助手工具集，包含抛硬币、随机数生成、YES/NO决策、抽签转盘和选项摇号等多种随机工具。聚会选择困难症的救星，也适合课堂互动、游戏分组和日常小决策。操作简单即开即用，纯前端运行无需注册。',
     '免费在线决策工具集，包含抛硬币、随机抽签、转盘摇号和YES/NO决策等多种随机选择工具，帮助快速做决定。'),

    ('./webgpu-info/index.html',
     '免费在线WebGPU信息检测器，一键查看浏览器对WebGPU API的支持状态、GPU适配器型号、显存大小和设备性能限制。帮助开发者判断用户设备是否支持GPU加速计算和渲染，评估WebGPU应用兼容性，无需注册安装。',
     '免费在线WebGPU信息检测器，检测浏览器WebGPU支持状态、GPU适配器型号和设备性能限制，开发者必备工具。'),

    ('./estimate-calculator/index.html',
     '免费在线项目工时与成本估算计算器，输入任务列表和预估工时，自动计算项目总工时和总成本。支持按小时/按天两种计费模式，可设置不同费率。适合自由职业者报价、项目经理排期和客户预算沟通，数据不上传服务器。',
     '免费在线项目估算计算器，输入任务和工时自动计算总工时和成本，支持按小时/天计费，适合自由职业者和项目经理。'),

    ('./gift-tax-calculator/index.html',
     '免费在线赠与税计算器，根据赠与财产金额、年度免税额和超额累进税率自动计算应缴赠与税额。支持夫妻合并赠与和终身免税额抵扣，帮助家庭进行财产传承规划和赠与策略优化，纯前端本地计算数据不上传。',
     '免费在线赠与税计算器，根据赠与金额和免税额自动计算应缴赠与税，帮助财产传承与赠与规划，纯前端计算。'),

    ('./webgpu-benchmark/index.html',
     '免费在线WebGPU性能基准测试工具，测试浏览器GPU的计算着色器处理能力、渲染管线吞吐量和内存带宽。生成综合性能评分方便跨设备对比，帮助开发者评估WebGPU应用的运行性能预期。纯前端运行无需下载安装。',
     '免费在线WebGPU性能基准测试，测试GPU计算着色器、渲染管线和内存带宽性能，生成综合评分，开发者评估工具。'),

    ('./letter-frequency-analyzer/index.html',
     '免费在线字母频率分析器，统计文本中每个英文字母的出现次数和百分比。支持柱状图可视化展示频率分布，适用于密码学学习、古典密码破解分析、语言特征研究和文本数据探索。纯前端处理数据不上传，无需注册。',
     '免费在线字母频率分析器，统计文本中每个字母的出现次数和百分比，支持柱状图可视化，适合密码分析和语言学习。'),

    ('./html-form-builder/index.html',
     '免费在线HTML表单构建器，拖拽式创建网页表单，支持文本输入、下拉选择、单选/多选、文件上传和日期选择等多种字段类型。实时预览表单效果，一键导出标准HTML代码。适合前端开发者和产品经理快速搭建原型表单，无需注册。',
     '免费在线HTML表单构建器，拖拽式创建网页表单，支持文本/选择/文件上传等多种字段，实时预览并一键导出HTML代码。'),
]

def apply_fix(filepath, new_desc, new_og_desc):
    full_path = os.path.join(BASE, filepath)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace meta description
    old_desc_pattern = r'<meta name="description" content="[^"]*">'
    new_desc_tag = f'<meta name="description" content="{new_desc}">'
    content = re.sub(old_desc_pattern, new_desc_tag, content, count=1)
    
    # Replace og:description if exists
    old_og_pattern = r'<meta property="og:description" content="[^"]*">'
    new_og_tag = f'<meta property="og:description" content="{new_og_desc}">'
    if re.search(old_og_pattern, content):
        content = re.sub(old_og_pattern, new_og_tag, content, count=1)
    
    # Also fix og:description in ld+json if present
    # (leave it as is for now, it's less critical)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(new_desc)

for filepath, new_desc, new_og_desc in FIXES:
    try:
        length = apply_fix(filepath, new_desc, new_og_desc)
        print(f'OK [{length}c] {filepath}')
    except Exception as e:
        print(f'FAIL {filepath}: {e}')

print('\nDone!')
