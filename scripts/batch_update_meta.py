#!/usr/bin/env python3
"""Batch update meta descriptions for tool pages."""
import re, glob, os

# Map tool dir -> (old_meta_fragment, new_meta_description)
# old_meta_fragment should be unique enough to find+replace
UPDATES = {
    "auto-loan-calculator": {
        "old": '<meta name="description" content="免费在线汽车贷款计算器。计算月供、总利息、总还款，生成还款明细表，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线汽车贷款计算器，根据车价、首付、年利率和贷款期限，快速计算每月月供、总利息和总还款额。生成详细按月还款明细表，支持等额本息计算方式。无需注册，数据不上传服务器。">'
    },
    "avif-to-jpg": {
        "old": '<meta name="description" content="免费在线Avif To Jpg工具 | 无需注册册，保护隐私，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线AVIF转JPG格式转换工具，将AVIF图片快速转换为通用的JPG格式，无需上传文件到服务器，保护隐私。支持批量转换和高质量输出，一键下载转换结果。适合需要兼容性图片格式的场景。">'
    },
    "backwards-text": {
        "old": '<meta name="description" content="免费在线反向文字生成器。将文字顺序完全反转，支持多种模式，一键复制，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线反向文字生成器，将文本字符顺序完全反转，支持全部反转、单词反转和双向对比三种模式。一键复制结果，无需注册。适合社交媒体创意文案、文字游戏和编码练习场景。">'
    },
    "batch-rename": {
        "old": '<meta name="description" content="在线批量重命名工具，支持前缀/后缀/替换/序号等多种重命名规则，生成重命名脚本，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线批量重命名工具，支持添加前缀后缀、查找替换、序号重命名和删除字符等规则。实时预览重命名结果，生成可执行的Shell/PowerShell脚本。无需注册，数据不上传服务器。">'
    },
    "bmp-to-png": {
        "old": '<meta name="description" content="免费在线Bmp To Png工具 | 无需注册册，保护隐私，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线BMP转PNG图片格式转换工具，将BMP位图快速转为PNG格式，压缩文件体积同时保持画质。纯浏览器本地处理，无需上传文件，保护隐私安全。适合网站素材优化和图片格式统一场景。">'
    },
    "business-card-maker": {
        "old": '<meta name="description" content="免费在线名片设计生成器，自定义姓名、职位、联系方式，支持多种配色模板，一键下载PNG图片，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线名片设计生成器，自定义姓名、职位、公司、邮箱、电话和网址，支持多种专业配色模板。实时预览效果，一键下载高清PNG名片图片。无需注册，所有设计在浏览器本地完成。">'
    },
    "camera-recorder": {
        "old": '<meta name="description" content="免费在线摄像头录像工具，使用浏览器摄像头录制视频并下载。无需注册，视频不上传服务器，隐私安全，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线摄像头录像工具，使用浏览器摄像头直接录制视频，支持多摄像头切换、分辨率选择和镜像翻转。视频不上传服务器，录制完成后直接下载到本地。适合快速录屏、视频留言和在线教学场景。">'
    },
    "character-counter": {
        "old": '<meta name="description" content="免费在线字符计数器，实时统计字符数、字数、句子数、段落数、行数和阅读时间。无需注册，隐私安全，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线字符计数器，实时统计字符数（含/不含空格）、字数、句子数、段落数、行数和预估阅读时长。无需注册，数据不上传服务器。适合文案写作、论文排版和社交媒体内容优化场景。">'
    },
    "compound-interest": {
        "old": '<meta name="description" content="在线复利计算器，计算投资复利增长，支持年复利/月复利/日复利，可视化收益曲线，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线复利计算器，计算投资复利增长和最终收益，支持年复利、月复利、日复利三种计算频率。输入本金、每月定投、年化收益率和投资年限，一键计算复利终值。适合理财规划和投资回报预测。">'
    },
    "cookie-analyzer": {
        "old": '<meta name="description" content="查看和管理当前网站的Cookie，支持查看名称、值、域名、路径、过期时间等详细信息，保护您的隐私，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线Cookie分析器，查看和管理当前网站的所有Cookie信息，包括名称、值、域名、路径和过期时间等详细属性。支持一键清除Cookie，保护浏览隐私。适合Web开发调试和隐私安全检查场景。">'
    },
    "cover-letter-generator": {
        "old": '<meta name="description" content="免费在线求职信生成器，输入公司、职位和个人信息，一键生成专业求职信。无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线求职信生成器，输入公司名称、职位、个人技能和联系方式，一键生成格式规范的专业求职信。支持自定义技能经验描述，生成内容可直接复制使用。无需注册，数据不上传服务器。">'
    },
    "credit-card-payoff": {
        "old": '<meta name="description" content="免费在线信用卡还款计算器。计算还款时间、利息总额，比较不同还款方案，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线信用卡还款计算器，输入信用卡余额、年利率和每月还款额，计算还清时间和总利息支出。对比最低还款与额外还款方案差异，帮助制定最优还款计划。无需注册，数据不上传服务器。">'
    },
    "csv-merger": {
        "old": '<meta name="description" content="免费在线Csv Merger工具 | 无需注册册，保护隐私，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线CSV文件合并工具，将多个CSV表格文件按行合并为一个文件，支持自定义分隔符和表头处理。纯浏览器本地处理，无需上传数据到服务器，保护数据隐私。适合数据汇总和报表整合场景。">'
    },
    "csv-sorter": {
        "old": '<meta name="description" content="免费在线Csv Sorter工具 | 无需注册册，保护隐私，无需注册，数据不上传服务器，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线CSV排序工具，按指定列对CSV表格数据进行升序或降序排列，支持自定义分隔符。纯浏览器本地处理，数据不上传服务器。适合数据整理、报表排序和数据分析预处理场景。">'
    },
    "csv-transpose": {
        "old": '<meta name="description" content="免费在线CSV转置工具。将CSV数据的行列互换，支持自定义分隔符和表头处理。无需注册，数据不上传。">',
        "new": '<meta name="description" content="免费在线CSV转置工具，将表格数据的行和列互换，支持逗号、Tab、分号、竖线等分隔符和表头处理选项。输入CSV数据一键转置，结果可复制或下载。适合数据透视分析和格式转换场景。">'
    },
    "date-add": {
        "old": '<meta name="description" content="免费在线日期加减计算器，在指定日期上加减天数、周数、月数或年数，快速得出新日期和星期，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线日期加减计算器，在任意日期上增减天数、周数、月数或年数，快速计算新日期和星期几。提供明天、7天后、30天后等快捷预设，支持负值减日。适合项目排期、合同到期和倒计时计算场景。">'
    },
    "day-of-week-calculator": {
        "old": '<meta name="description" content="免费在线星期几计算器，查询任意日期是星期几，支持中文/英文显示。纯前端计算，无需注册，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线星期几计算器，选择任意日期快速查询对应星期几，支持中英文双语显示。基于蔡勒公式算法，可处理公历1582年后的任意日期。纯前端计算，无需注册。适合日期查询和历史研究场景。">'
    },
    "day-of-week": {
        "old": '<meta name="description" content="免费在线星期几计算器，输入任意日期快速查询是星期几，支持公历任意年份，显示农历信息，免费在线工具，无需注册，浏览器本地处理。">',
        "new": '<meta name="description" content="免费在线星期几查询工具，选择任意日期即可显示对应星期几，附带当月日历视图。支持公历任意年份查询，操作简单直观。纯浏览器本地计算，无需注册。适合日程安排、日期核对和历史事件查询场景。">'
    },
    "device-info": {
        "old": '<meta name="description" content="免费在线设备信息查看器，一键查看浏览器、操作系统、CPU、内存、网络、电池等详细信息。无需注册。">',
        "new": '<meta name="description" content="免费在线设备信息查看器，一键查看浏览器型号版本、操作系统、CPU核心数、内存大小、网络类型、电池状态、语言和时区等详细设备参数。无需注册，所有信息仅在本地显示。适合技术支持排查和开发调试场景。">'
    },
}

def update_file(tool_dir, old_str, new_str):
    filepath = f"{tool_dir}/index.html"
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if old_str not in content:
        print(f"  WARN: old string not found in {filepath}")
        # Try finding a similar pattern
        idx = content.find('<meta name="description"')
        if idx >= 0:
            snippet = content[idx:idx+200]
            print(f"  Found meta: {snippet[:150]}")
        return False
    
    # Replace meta description
    content = content.replace(old_str, new_str)
    
    # Also update og:description - extract from new meta
    new_meta_match = re.search(r'content="([^"]+)"', new_str)
    if new_meta_match:
        new_desc = new_meta_match.group(1)
        # Replace og:description with matching content
        og_pattern = r'<meta property="og:description" content="[^"]*">'
        og_replacement = f'<meta property="og:description" content="{new_desc}">'
        content = re.sub(og_pattern, og_replacement, content)
        
        # Replace Schema.org description
        schema_pattern = r'"description":\s*"[^"]*"'
        schema_replacement = f'"description": "{new_desc}"'
        content = re.sub(schema_pattern, schema_replacement, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    # Verify new length
    final_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    if final_match:
        print(f"  OK: new desc length = {len(final_match.group(1))}")
    
    return True

count = 0
for tool, update in UPDATES.items():
    print(f"Processing {tool}...")
    if update_file(tool, update["old"], update["new"]):
        count += 1

print(f"\nTotal updated: {count}/{len(UPDATES)}")