#!/usr/bin/env python3
"""Batch generate meta description fixes using og:description as reference."""
import re, os
from pathlib import Path

# Map of filepath -> old_description_snippet -> new_description
# Using og:description as reference since it's usually complete
fixes = []

# Next batch: more truncated pages with their og:descriptions
pages = [
    ("voltage-drop-calculator/index.html", 
     'content="/交流电路的电压降和百分比，帮助电工和工程师选择合适的导线规格，符合NEC/IEC标准。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"',
     '免费在线电压降计算器，快速计算直流和交流电路的电压降和百分比。帮助电工和工程师选择合适的导线规格，符合NEC/IEC标准，纯前端处理无需注册。'),
    
    ("work-hours-calculator/index.html",
     'content="免费在线工时计算器，精确计算工作时长、加班时间、休息扣除。支持多次打卡记录，自动扣除午休时间，一键导出CSV。适合上班族、自由职业者、HR使用。"',
     '免费在线工时计算器，精确计算工作时长、加班时间和休息扣除。支持多次打卡记录，自动扣除午休时间，一键导出CSV。适合上班族、自由职业者和HR使用，纯前端处理无需注册。'),
    
    ("rich-text-editor/index.html",
     'content="HTML源码或下载HTML文件，工具栏按钮齐全操作直观。所有编辑内容在浏览器本地完成，无需注册下载即可免费使用。纯前端本地处理，数据安全有保障。"',
     '免费在线富文本编辑器，可视化编辑文字内容，支持实时预览HTML源码和下载HTML文件。工具栏齐全操作直观，所有编辑内容在浏览器本地完成，无需注册完全免费。'),
    
    ("image-mirror/index.html",
     'content="JPG、PNG、WebP、GIF等格式，纯前端Canvas处理，图片不上传服务器，保护隐私。纯前端本地处理，数据不上传服务器，无需注册完全免费。"',
     '免费在线图片镜像翻转工具，支持水平翻转和垂直翻转。支持JPG、PNG、WebP、GIF等格式，纯前端Canvas处理，图片不上传服务器保护隐私，无需注册完全免费。'),
    
    ("fuel-efficiency/index.html",
     'content="L/100km、MPG、km/L），输入加油量和行驶里程即可计算，适合车主管理用车成本。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"',
     '免费在线油耗计算器，支持L/100km、MPG、km/L等多种单位。输入加油量和行驶里程即可计算油耗，适合车主管理用车成本，纯前端处理无需注册。'),
    
    ("headline-generator/index.html",
     'content="SEO关键词优化建议。提升内容曝光率和点击率，助力内容创作者和新媒体运营人员高效产出爆款标题。纯前端本地处理，数据不上传服务器，无需注册完全免费。"',
     '免费在线标题生成器，为博客文章和新媒体内容生成高点击率标题。提供多种标题模板和SEO关键词优化建议，助力内容创作者高效产出爆款标题，纯前端处理无需注册。'),
    
    ("net-worth-calculator/index.html",
     'content="= 总资产 - 总负债，是衡量财务健康的核心指标。净资产计算器在线支持实时预览，操作简单快捷。纯前端本地处理，数据不上传服务器，无需注册完全免费。"',
     '免费在线净资产计算器，净资产=总资产-总负债，是衡量财务健康的核心指标。快速计算个人或家庭净资产，操作简单快捷，纯前端处理无需注册。'),
    
    ("ingredient-substitute-finder/index.html",
     'content="100+常见食材的替代方案。黄油、鸡蛋、牛奶、面粉等食材的完美替代品，支持黄油替代、牛奶替代。纯前端本地处理，数据不上传服务器，无需注册完全免费。"',
     '免费在线食材替代查询器，提供100+常见食材的替代方案。黄油、鸡蛋、牛奶、面粉等食材的完美替代品一键查询，适合烘焙和烹饪时的紧急替代，纯前端处理无需注册。'),
    
    ("circle-calculator/index.html",
     'content="π公式和分步计算过程，适合学生学习几何、工程设计图纸计算和日常尺寸换算，纯前端运算即开即用，完全免费无需注册下载。纯前端本地处理，数据安全有保障。"',
     '免费在线圆形计算器，输入半径或直径自动计算圆的面积、周长、直径和半径。显示π公式和分步计算过程，适合学生学习几何和工程计算，纯前端运算无需注册。'),
    
    ("forex-pip-calculator/index.html",
     'content="EUR/USD、GBP/JPY等所有主流货币对及交叉盘，适合外汇交易者进行仓位管理和风险控制。纯前端本地处理，数据不上传服务器，无需注册完全免费。"',
     '免费在线外汇点值计算器，支持EUR/USD、GBP/JPY等所有主流货币对及交叉盘。帮助外汇交易者精确计算每点价值，进行仓位管理和风险控制，纯前端处理无需注册。'),
]

root = Path('.')

for rel_path, old_snippet, new_desc in pages:
    filepath = root / rel_path
    if not filepath.exists():
        print(f"MISSING: {rel_path}")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    # Find the exact meta description line
    pattern = r'(<meta\s+name=["\']description["\']\s+)content="[^"]*"'
    match = re.search(pattern, content)
    if not match:
        print(f"NO MATCH: {rel_path}")
        continue
    
    old_meta = match.group(0)
    new_meta = match.group(1) + f'content="{new_desc}"'
    
    content = content.replace(old_meta, new_meta)
    filepath.write_text(content, encoding='utf-8')
    
    # Verify
    new_content = filepath.read_text(encoding='utf-8')
    m = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]*)"', new_content)
    new_len = len(m.group(1)) if m else 0
    print(f"FIXED: {rel_path} ({new_len} chars)")

print("\nDone!")