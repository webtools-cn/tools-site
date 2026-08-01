#!/usr/bin/env python3
"""为meta description过短的非迁移页面写精准的description"""
import os, re

# 工具名 -> 精准描述 映射
descriptions = {
    'json-formatter-example': '免费在线JSON格式化示例工具，提供JSON格式化、校验、压缩功能，含常见JSON格式示例代码和模板，一键格式化美化JSON数据。适合开发者API调试和数据分析，无需注册，数据不上传服务器。',
    
    'mac-address-lookup': '免费在线MAC地址厂商查询工具，输入MAC地址即可查询设备制造商和网卡厂商信息。基于IEEE OUI数据库，支持快速识别网络设备品牌，IT运维和网络安全排查必备，无需注册。',
    
    'regex-to-nfa': '免费在线正则表达式转NFA可视化工具，将正则表达式转换为NFA非确定有限状态自动机状态转换图。基于Thompson构造算法，Canvas交互绘图，适合编译原理学习和正则引擎理解。',
    
    'svg-filter': '免费在线SVG滤镜效果生成器，实时预览模糊、阴影、颜色矩阵等CSS/SVG滤镜效果。可视化调整参数，一键复制SVG滤镜代码和CSS filter代码，前端开发和SVG设计必备工具。',
    
    'swot-analysis': '免费在线SWOT分析工具，快速创建专业SWOT分析矩阵。优势、劣势、机会、威胁四维度分析，支持导出PNG图片和PDF文档，商业策划和项目评估必备，无需注册。',
    
    'px-to-rem-converter': '免费在线PX转REM/EM转换器，支持自定义基础字体大小，实时转换px到rem/em/pt单位。响应式网页设计必备工具，帮助前端开发者统一管理字体和间距单位，纯前端本地运算。',
    
    'rent-affordability-calculator': '免费在线租金可负担性计算器，根据月收入和支出自动计算可承担的租金范围。遵循30%租金收入比规则，帮助你理性租房和控制住房开支。纯前端本地运算，数据安全不上传。',
    
    'muscle-recovery-calculator': '免费在线肌肉恢复时间计算器，根据训练强度、年龄和睡眠质量估算肌肉群恢复所需时间。帮助健身爱好者科学安排训练计划，避免过度训练和肌肉损伤。纯前端计算，数据不上传服务器。',
    
    'coast-fire-calculator': '免费在线Coast FIRE计算器，计算何时可以停止储蓄让复利自然增长到FIRE目标。无需再存一分钱，只需等待时间让你达到财务独立提前退休。纯前端本地计算，数据不上传服务器。',
    
    'json-to-csharp': '免费在线JSON转C#类生成器，从JSON数据自动生成对应的C#类定义代码。支持嵌套对象、数组、自定义类名和命名空间，.NET开发者API对接和数据建模的必备效率工具。',
    
    'statistical-power-calculator': '免费在线统计功效计算器，计算A/B测试和假设检验的统计功效Power。支持输入样本量、效应量和显著性水平，帮助实验设计者评估检验灵敏度，纯前端计算数据不上传。',
    
    'mac-address-generator': '免费在线MAC地址生成器，支持随机生成MAC地址和批量生成，可选择指定OUI厂商前缀。支持验证MAC格式和多种格式转换，网络测试和设备模拟的实用工具，无需注册。',
    
    'text-to-yaml': '免费在线文本转YAML转换器，支持JSON和key=value格式转换为YAML，自动处理缩进、引号和特殊字符。适用于配置文件生成、Docker Compose编写和数据序列化，纯前端安全处理。',
    
    'value-comparison-calculator': '免费在线性价比比较计算器，输入不同产品的价格和规格自动计算每单位价格。支持多种商品类型对比，找出最划算的选择。超市购物比价和电商选品决策的实用工具，纯前端运算。',
    
    'fertility-calculator': '免费在线排卵期与受孕计算器，基于月经周期预测排卵日和易孕期。支持日历视图和受孕窗口期显示，帮助备孕女性精准把握最佳受孕时机。纯前端本地计算，数据安全不上传服务器。',
    
    'character-unicode-finder': '免费在线Unicode字符查询工具，输入任意字符即可查看其Unicode码点、UTF-8/UTF-16/UTF-32编码和HTML实体表示。开发者字符编码调试和多语言文本处理的实用查询工具。',
    
    'food-calorie': '免费在线食物热量查询工具，查询常见食物的卡路里和营养成分数据。包含200+常见食物数据库，支持搜索和分类浏览，帮助控制饮食热量摄入。健康饮食和体重管理必备，无需注册。',
}

base_dir = '/home/chison/tools-site'
count_fixed = 0

for tool_name, new_desc in descriptions.items():
    path = os.path.join(base_dir, tool_name, 'index.html')
    if not os.path.exists(path):
        print(f'✗ {tool_name}: file not found')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '已迁移' in content:
        print(f'  {tool_name}: migrated, skip')
        continue
    
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    if not m:
        print(f'✗ {tool_name}: no meta description found')
        continue
    
    old_desc = m.group(1)
    if old_desc == new_desc:
        print(f'  {tool_name}: already same')
        continue
    
    # Also update Schema description
    schema_pattern = r'"description":"([^"]*)"'
    m2 = re.search(schema_pattern, content)
    
    content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    
    if m2:
        old_schema = m2.group(1)
        # Keep schema description concise
        new_schema = f'免费在线{tool_name.replace("-", " ")}工具。纯前端处理，无需注册。'
        if new_schema != old_schema:
            content = content.replace(
                f'"description":"{old_schema}"',
                f'"description":"{new_schema}"'
            )
    
    # Also update OG description
    og_pattern = r'<meta property="og:description" content="([^"]*)"'
    m3 = re.search(og_pattern, content)
    if m3:
        old_og = m3.group(1)
        if old_og != new_desc:
            content = content.replace(
                f'<meta property="og:description" content="{old_og}"',
                f'<meta property="og:description" content="{new_desc}"'
            )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    count_fixed += 1
    print(f'✓ {tool_name}: {len(old_desc)}→{len(new_desc)} chars')

print(f'\nTotal fixed: {count_fixed} pages')
