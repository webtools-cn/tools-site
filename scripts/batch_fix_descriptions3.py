#!/usr/bin/env python3
"""Batch fix descriptions - round 3: target 135-160 chars for Chinese."""
import re
from pathlib import Path

fixes = [
    ("voltage-drop-calculator/index.html",
     "免费在线电压降计算器，快速计算直流和交流电路的电压降和百分比。输入导线长度、截面积和负载电流，自动计算电压降并评估是否符合NEC/IEC标准。帮助电工和工程师选择合适的导线规格，确保电路安全运行。纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("work-hours-calculator/index.html",
     "免费在线工时计算器，精确计算每日工作时长、加班时间和休息扣除。支持多次打卡记录，自动扣除午休时间，一键导出CSV报表方便归档。适合上班族记录考勤、自由职业者统计计费工时和HR管理人员核算薪资。纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("rich-text-editor/index.html",
     "免费在线富文本编辑器，可视化编辑文字内容，支持实时预览HTML源码和下载HTML文件。提供加粗、斜体、列表、表格、链接插入等完整编辑工具栏，操作直观方便。适合撰写文档、编辑邮件和快速排版，所有编辑内容在浏览器本地完成，无需注册完全免费。"),
    
    ("image-mirror/index.html",
     "免费在线图片镜像翻转工具，支持水平翻转和垂直翻转两种模式。支持JPG、PNG、WebP、GIF等常见图片格式，纯前端Canvas处理图片不上传服务器，保护隐私安全。适合设计师调整构图、社交媒体运营制作创意图片，无需注册完全免费。"),
    
    ("fuel-efficiency/index.html",
     "免费在线油耗计算器，支持L/100km、MPG、km/L等多种单位实时切换。输入加油量和行驶里程即可精准计算百公里油耗，帮助车主管理日常用车成本和对比不同车型燃油经济性。纯前端处理数据不上传服务器，无需注册完全免费使用。"),
    
    ("headline-generator/index.html",
     "免费在线标题生成器，为博客文章和新媒体内容一键生成高点击率爆款标题。提供列表型、疑问型、指南型等多种标题模板和SEO关键词优化建议，帮助内容创作者和新媒体运营人员提升内容曝光率和点击率。纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("net-worth-calculator/index.html",
     "免费在线净资产计算器，净资产=总资产减去总负债，是衡量个人或家庭财务健康的核心指标。输入现金存款、投资理财、房产车辆等资产和贷款债务明细，快速计算净资产总额。帮助做好家庭财务规划和资产追踪，纯前端处理数据安全有保障，无需注册完全免费。"),
    
    ("ingredient-substitute-finder/index.html",
     "免费在线食材替代查询器，提供100+常见烹饪食材的紧急替代方案。黄油、鸡蛋、牛奶、面粉、奶油、泡打粉等食材的完美替代品一键查询，解决烘焙和烹饪时缺少食材的燃眉之急。每个替代方案附带使用比例说明，纯前端处理无需注册，厨房必备实用工具。"),
    
    ("circle-calculator/index.html",
     "免费在线圆形计算器，输入半径或直径自动计算圆的面积、周长、直径和半径。显示π公式和分步计算过程，支持厘米/米/英寸多单位实时切换。适合学生学习几何知识、工程师进行图纸计算和日常尺寸换算，纯前端运算即开即用，无需注册完全免费。"),
    
    ("forex-pip-calculator/index.html",
     "免费在线外汇点值计算器，支持EUR/USD、GBP/JPY等所有主流货币对及交叉盘交易品种。帮助外汇交易者精确计算每点价值，科学进行仓位管理和风险控制。输入交易手数和货币对即可得出精确点值，纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("percentage-difference-calculator/index.html",
     "免费在线百分比差异计算器，计算两个数值之间的百分比差异、绝对差异和相对差异三项指标。适合统计数据分析、实验误差评估和双数据源对比等多种场景使用。输入两个数值即可自动计算，纯客户端本地运算数据不上传服务器，无需注册即可免费使用。"),
    
    ("directory-tree-generator/index.html",
     "免费在线目录树生成器，上传文件夹或手动输入路径，一键生成ASCII目录树结构图。支持自定义缩进深度、过滤规则和Markdown代码块输出，适合项目README文档编写和技术文档目录展示。支持Unicode/ASCII/简洁三种连接线风格，纯前端处理无需注册，文件不上传服务器。"),
    
    ("word-density-analyzer/index.html",
     "免费在线词频密度分析器，统计文本中每个词语的出现频率和密度百分比，自动计算TF-IDF权重。支持中英文分词、停用词过滤和词云可视化展示。SEO优化师分析关键词分布、内容创作者检查文章质量的必备工具，纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("keyword-density-analyzer/index.html",
     "免费在线关键词密度分析器，分析文章中每个词的出现频率和密度百分比。支持排除停用词、按频率排序和词频统计可视化。帮助SEO优化师优化关键词分布避免堆砌被搜索引擎降权，内容创作者检查文章质量。纯前端处理数据不上传服务器，无需注册完全免费。"),
    
    ("image-batch-resizer/index.html",
     "免费在线批量图片调整大小工具，支持拖放上传多张图片，一键按微信/Instagram/Twitter/YouTube等社交媒体预设尺寸或自定义尺寸批量调整。支持裁剪和留白两种缩放模式，可统一输出格式和质量。纯前端处理图片不上传服务器保护隐私，无需注册完全免费。"),
]

root = Path('.')
for rel_path, new_desc in fixes:
    filepath = root / rel_path
    if not filepath.exists():
        print(f"MISSING: {rel_path}")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    pattern = r'(<meta\s+name=[\"\']description[\"\']\s+)content=\"[^\"]*\"'
    match = re.search(pattern, content)
    if not match:
        print(f"NO MATCH: {rel_path}")
        continue
    
    new_meta = match.group(1) + f'content="{new_desc}"'
    content = re.sub(pattern, new_meta.replace('\\', '\\\\'), content)
    filepath.write_text(content, encoding='utf-8')
    
    # Verify
    new_content = filepath.read_text(encoding='utf-8')
    m = re.search(r'<meta\s+name=[\"\']description[\"\']\s+content=\"([^\"]+)\"', new_content)
    new_len = len(m.group(1)) if m else 0
    status = "OK" if 130 <= new_len <= 160 else ("SHORT" if new_len < 130 else "LONG")
    print(f"{status:5s} | {new_len:3d} chars | {rel_path}")

print("\nDone!")