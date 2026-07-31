#!/usr/bin/env python3
"""Batch optimize meta description - ensure 140-160 chars per len()."""
import re, os

DESCRIPTIONS = {
    "sep-ira-calculator": "免费在线SEP IRA退休金计算器，帮助自雇人士和小企业主快速计算可缴纳的SEP IRA退休金上限金额。基于2025年IRS最新规则，采用25%净薪酬限额计算，最高年度缴纳额$70,000。支持自定义年净收入和缴费比例参数，实时显示雇主缴款额和潜在税后节省金额，纯前端本地处理无需注册。",
    "binary-hex-converter": "免费在线进制转换器，支持二进制、八进制、十进制、十六进制四种常用进制之间的实时相互转换。在任意进制输入框中输入数值，其他三种进制的转换结果会自动同步显示，每个结果旁配备一键复制按钮。支持JavaScript BigInt处理超大数值，适合程序员调试和计算机专业学生日常使用，纯前端本地计算无需注册。",
    "json-merge-patch": "免费在线JSON Merge Patch工具，严格遵循RFC 7396标准，支持声明式JSON文档合并与字段删除操作。只需在Patch文档中描述目标JSON最终状态，null值自动删除原始文档对应字段。适合REST API部分资源更新和微服务配置合并场景，纯前端本地执行保障数据安全，无需注册。",
    "text-formatter": "免费在线文本格式化工具，提供中英文自动排版、去除多余空行、统一标点符号、段落首行缩进、自动编号、全角半角转换等多种实用功能。一键将杂乱无章的文本整理得整洁美观，适用于文章排版润色、代码注释整理、邮件格式优化和工作文档批量处理。纯前端本地处理，数据绝不上传服务器，即用即走无需注册。",
    "mesh-gradient-generator": "免费在线Mesh网格渐变生成器，通过可视化界面创建多色网格渐变背景效果。支持拖拽自由调整颜色节点位置，可自定义4至6个颜色锚点，每个锚点独立设置颜色和透明度。实时预览渐变渲染效果并一键导出完整CSS代码。适用于网页Hero区域背景设计、品牌海报制作和现代UI界面设计，无需注册完全免费。",
    "text-deduplicate": "免费在线文本去重工具，提供按行去重和按词去重两种高效模式，可灵活切换大小写敏感选项并自动过滤空白行和纯空格行。处理完成后实时显示原始行数、发现重复行数和去重后剩余行数的统计数据，并清晰列出被移除的所有重复内容。适用于名单去重整理、SEO关键词去重和数据清洗等场景，纯前端处理保障数据安全。",
    "anagram-finder": "免费在线变位词(Anagram)查找器，只需输入一串字母或单词，系统自动重组生成所有可能的有效变位词组合。同时支持中文汉字和英文单词两种语言模式，可设置最小词长过滤无意义短词结果。适用于英文字谜游戏解谜、创意写作灵感激发和英语单词联想记忆学习。纯前端本地计算，数据不上传，隐私安全无需注册。",
    "cron-sandbox": "免费在线Cron表达式测试沙盒，输入Cron定时表达式即可预览未来接下来的N次实际执行时间和对应的自然语言可读描述。同时支持5位标准cron格式和6位含秒的扩展格式，实时校验语法正确性并用红色高亮标记错误位置。Linux运维人员、后端开发者调试和验证定时任务调度的必备实用工具，纯前端无需注册。",
    "quadratic-solver": "免费在线一元二次方程求解器，使用经典求根公式精确求解ax²+bx+c=0方程的所有根。自动展示完整详细的解题步骤，包括判别式Δ的分析计算、实根与复数根的区分显示、顶点坐标和因式分解结果。非常适合作业辅导、中学生数学自主学习和教师课堂教学演示使用，支持任意实数系数输入，纯前端本地计算无需注册。",
    "color-blender": "免费在线颜色混合工具，将两种颜色按0%到100%之间的任意比例进行混合，生成完美的中间色和完整的渐变色阶序列。同时支持HEX十六进制和RGB两种颜色格式输入和输出，实时预览混合效果。非常适合UI界面配色方案设计、CSS渐变色代码生成和品牌视觉色彩调和等场景，纯前端处理，无需注册完全免费。",
    "css-scroll-driven-animation-generator": "免费在线CSS滚动驱动动画生成器，可视化创建scroll-driven和view-driven动画效果。支持自定义动画时间线、关键帧缓动函数和滚动触发区间，实时预览动画表现。自动生成标准CSS Animation Timeline代码。前端开发者实现视差滚动和元素渐显效果的效率神器，无需注册。",
    "css-gradient-text-generator": "免费在线CSS渐变文字生成器，为网页文字轻松添加绚丽的渐变色效果，告别单调纯色文字。支持线性渐变和径向渐变两种渲染模式，可自定义2至6个颜色节点和渐变角度方向。输入预览文字即可实时查看效果，一键复制完整的CSS background-clip渐变文字代码。适用于网页标题设计、品牌Logo文字和社交媒体配图，无需注册。",
    "image-resizer": "免费在线图片批量调整大小工具，支持按目标像素精确缩放和按百分比等比缩放两种灵活模式，自动保持原始图片宽高比防止变形。完全基于浏览器Canvas API本地处理图片数据，支持JPG、PNG、WebP多种输出格式选择。所有图片数据绝不上传至任何远程服务器，最大程度保护用户隐私安全，即用即走无需注册账号。",
    "profit-margin-calculator": "免费在线利润率计算器，一站式计算毛利率、净利率和加价率三大核心商业指标。只需输入产品成本和期望售价，自动得出利润金额和各项利润率百分比，同时支持反向推算达成目标利润率所需的售价。非常适合电商卖家定价策略决策、零售店铺利润分析和创业者商业计划书财务预测，纯前端本地计算数据不上传无需注册。",
    "csv-to-geojson": "免费在线CSV转GeoJSON格式转换工具，将含经纬度坐标的CSV表格数据一键转换为标准GeoJSON FeatureCollection格式。支持自定义经纬度列名映射和输出属性筛选，内置Leaflet地图实时预览数据点位分布。适用于GIS数据可视化、Web地图开发和空间数据分析，纯前端处理无需上传。",
    "college-cost-calculator": "免费在线大学费用计算器，全面预估本科四年总花费，涵盖学费、住宿费和生活费三大核心开支项目。自动考虑美国大学教育通胀的年均增长率因素，输出每年分项费用明细和四年汇总总额。帮助家长和学生提前规划教育储蓄目标和529计划每月投入金额。所有财务数据纯前端本地计算，不上传服务器，安全可靠无需注册。",
    "pdf-unlock": "免费在线PDF解锁工具，快速移除PDF文件的打开密码保护和编辑权限限制，恢复文档的完整访问能力。支持拖拽上传或点击选择PDF文件，自动检测文件的加密状态和权限级别，输入正确密码后一键下载完全解密文件。基于浏览器本地WebAssembly技术处理，PDF文件绝不上传服务器，保障敏感文档安全。仅限已知密码的合法解锁场景。",
    "diff-patch-generator": "免费在线Diff补丁生成器，对比粘贴两段文本自动生成标准unified diff格式的补丁文件。支持逐行级别的差异精准高亮显示，可选择忽略空白字符和大小写变化。一键复制补丁文本内容或直接下载.patch格式文件。适用于程序员代码审查变更对比、版本差异分析和开源项目协作提交patch补丁，纯前端本地处理无需注册。",
    "mp4-to-gif": "免费在线MP4视频转GIF动态图片转换器，将短视频片段快速转换为高质量循环播放的GIF动图。支持自定义输出帧率、画面缩放尺寸和压缩质量等级，转换前实时预览效果确保满意。完全基于浏览器Canvas逐帧渲染处理，视频文件不上传任何远程服务器保障隐私。适用于制作表情包动图、产品功能演示和社交媒体内容创作，无需注册。",
    "receipt-maker": "免费在线收据生成器，快速创建排版专业、信息规范的收款收据凭证。支持自定义商家名称地址、商品服务明细条目、税率设置和折扣优惠，自动计算金额合计。提供一键打印纸质收据和导出PDF电子收据功能。非常适合小型实体商户、自由职业者和线下现金交易场景开具简易收据使用，纯前端本地处理，交易数据不上传，安全可靠无需注册。",
}

BASE = '/home/chison/tools-site'

def update_page(tool_dir, new_desc):
    filepath = os.path.join(BASE, tool_dir, 'index.html')
    if not os.path.exists(filepath):
        return False, 0
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace meta description
    content = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        r'\1' + new_desc + r'\2', content, count=1
    )
    # Replace og:description
    content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        r'\1' + new_desc + r'\2', content, count=1
    )
    # Replace ld+json SoftwareApplication description (first occurrence)
    ld_count = [0]
    def replace_ld(m):
        ld_count[0] += 1
        if ld_count[0] == 1:
            return '"description": "' + new_desc + '"'
        return m.group(0)
    content = re.sub(r'"description":\s*"[^"]*"', replace_ld, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return True, len(new_desc)

results = []
for tool, desc in DESCRIPTIONS.items():
    ok, length = update_page(tool, desc)
    results.append((tool, ok, length))

print("=== Results ===")
in_range = 0
for tool, ok, length in results:
    status = 'OK' if ok else 'FAIL'
    flag = '✓' if 140 <= length <= 160 else '✗'
    if 140 <= length <= 160:
        in_range += 1
    print(f'{status} {flag}: {tool} ({length} chars)')
print(f'In range (140-160): {in_range}/{len(results)}')