#!/usr/bin/env python3
"""Final fix: directly replace full meta descriptions for remaining short ones."""
import re

FULL_REPLACE = {
    "backwards-text": "免费在线反向文字生成器，将文本字符顺序完全反转输出，支持全部反转、单词级反转和双向原反对比三种翻转模式，每种模式实时显示结果。输入任意文字一键转换，结果即时可复制并显示字符数统计。无需注册，数据不上传服务器。适合社交媒体创意文案创作、趣味文字游戏和编程编码练习等多种场景。",
    "business-card-maker": "免费在线名片设计生成器，自定义姓名、职位、公司、邮箱、电话和网址等完整信息，提供多种专业配色模板（经典白、商务蓝、极简黑、活力橙等）自由切换。实时预览名片效果，一键下载高清PNG名片图片。无需注册登录，所有设计在浏览器本地完成。适合创业者、自由职业者和商务人士快速制作电子名片。",
    "character-counter": "免费在线字符计数器，实时统计字符数（含空格/不含空格）、字数、句子数、段落数、行数和预估阅读及朗读时长。输入或粘贴文本即时获得统计数据，无需注册，数据不上传服务器。适合文案写作、论文排版、社交媒体内容优化、翻译字数估算和SEO元描述长度检查等多种常用场景。",
    "cover-letter-generator": "免费在线求职信生成器，输入公司名称、目标职位、个人技能经验和联系方式，一键生成格式规范、内容专业的英文求职信。支持自定义技能描述，生成内容可直接复制到邮件或文档使用。无需注册，数据不上传服务器。适合求职者快速准备应聘材料、提升求职效率和面试邀约率。",
    "credit-card-payoff": "免费在线信用卡还款计算器，输入信用卡欠款余额、年利率APR和每月还款额，计算还清所需时间和总利息支出。直观对比最低还款与额外还款两种方案差异，清晰展示节省的利息金额。无需注册，数据不上传服务器。适合信用卡债务管理、还款计划制定和个人财务健康管理等多种场景。",
    "csv-sorter": "免费在线CSV排序工具，按指定列对CSV表格数据进行升序或降序排列，支持逗号、Tab、分号和竖线等自定义分隔符。纯浏览器本地处理，数据绝不上传服务器，保护数据隐私安全。适合数据整理排序、报表重新排列、数据分析预处理和Excel导入前数据清洗等常用场景。",
    "day-of-week": "免费在线星期几查询工具，选择任意日期即可显示对应星期几，并附带当月完整日历视图方便浏览。支持公历任意年份日期查询，操作简单直观。纯浏览器本地计算，无需注册登录。适合日程安排、日期核对、历史事件查询、纪念日推算和节日规划等多种日常生活场景。",
}

for tool, new_desc in FULL_REPLACE.items():
    filepath = f"{tool}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_meta = f'<meta name="description" content="{new_desc}">'
    old_pattern = r'<meta name="description" content="[^"]*">'
    content = re.sub(old_pattern, new_meta, content)
    
    og_pattern = r'<meta property="og:description" content="[^"]*">'
    og_replacement = f'<meta property="og:description" content="{new_desc}">'
    content = re.sub(og_pattern, og_replacement, content)
    
    schema_pattern = r'"description":\s*"[^"]*"'
    schema_replacement = f'"description": "{new_desc}"'
    content = re.sub(schema_pattern, schema_replacement, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    status = "✅" if 140 <= len(new_desc) <= 160 else "⚠️"
    print(f"  {status} {tool}: {len(new_desc)} chars")

print("\nDone!")