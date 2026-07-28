#!/usr/bin/env python3
"""Translate new tool pages from CN to EN by replacing key Chinese strings."""
import sys, os, re

TOOLS_DIR = '/home/chison/tools-site'
NEW_TOOLS = [
    'option-price-calculator',
    'symptom-checker',
    'pill-reminder',
    'vaccination-schedule',
    'grocery-list',
]

# Translation map: (chinese_string, english_string)
TR = [
    # --- Common / boilerplate ---
    ('lang="zh-CN"', 'lang="en"'),
    ('lang="zh"', 'lang="en"'),
    ('<title>免费在线', '<title>Free Online '),
    (' | Free ToolBase</title>', ' | Free ToolBase</title>'),
    ('免费在线期权定价计算器 - Black-Scholes模型 | Free ToolBase', 'Free Online Option Price Calculator - Black-Scholes Model | Free ToolBase'),
    ('免费在线症状自查工具 - 健康参考 | Free ToolBase', 'Free Online Symptom Checker - Health Reference | Free ToolBase'),
    ('免费在线服药提醒工具 - 用药时间表管理 | Free ToolBase', 'Free Online Pill Reminder - Medication Schedule Manager | Free ToolBase'),
    ('免费在线疫苗接种时间表 - 儿童免疫计划 | Free ToolBase', 'Free Online Vaccination Schedule - Child Immunization Plan | Free ToolBase'),
    ('免费在线购物清单工具 - 智能分类管理 | Free ToolBase', 'Free Online Grocery List - Smart Category Manager | Free ToolBase'),

    ('首页', 'Home'),
    ('工具', 'Tools'),
    ('<a href="../index.html"', '<a href="../../index.html"'),
    ('<a href="/"', '<a href="../../"'),
    ('href="index.html" class="active">中文</a><a href="../en/', 'href="index.html" class="">中文</a><a href="../en/'),
    ('<a href="../en/', '<a href="../'),

    ('中文', '中文'),
    ('EN', 'EN'),

    # --- og / meta ---
    ('content="https://free-toolbase.com/', 'content="https://free-toolbase.com/en/'),
    ('href="https://free-toolbase.com/', 'href="https://free-toolbase.com/en/'),
    ('"item":"https://free-toolbase.com/"', '"item":"https://free-toolbase.com/en/"'),
    ('"item":"https://free-toolbase.com/#tools"', '"item":"https://free-toolbase.com/en/#tools"'),

    # --- Footer ---
    ('<a href="/">首页</a>', '<a href="../../">Home</a>'),
    ('<a href="/privacy">隐私政策</a>', '<a href="../../privacy">Privacy</a>'),
    ('<a href="/terms">使用条款</a>', '<a href="../../terms">Terms</a>'),

    # --- lang switch fix ---
    ('<a href="index.html" class="active">中文</a>', '<a href="../../option-price-calculator/">中文</a>'),
    ('<a href="index.html" class="">中文</a>', '<a href="../../option-price-calculator/">中文</a>'),

    # We need per-tool specific translations, will handle inline
]

def translate_file(src_path, dst_path, tool_name):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Basic boilerplate replacements
    content = content.replace('lang="zh-CN"', 'lang="en"')

    # Canonical / og URLs: replace CN URL with EN URL
    content = re.sub(r'(https://free-toolbase\.com)/(?!en/)', r'\1/en/', content)

    # Fix hreflang
    content = content.replace('<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/en/', '<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/')
    # Wait, the hreflang mapping:
    # CN: zh -> /tool/, en -> /en/tool/, x-default -> /en/tool/
    # EN: zh -> /tool/, en -> /en/tool/, x-default -> /en/tool/
    # So EN version is same as CN actually... they both point to same URLs
    # Let's just keep as-is, hreflang URLs should be absolute and same for both pages
    # Actually the pattern: CN page says zh=CN, en=EN. EN page should say zh=CN, en=EN too.

    # Description translations
    content = content.replace(
        '免费在线期权定价计算器，支持Black-Scholes模型计算欧式看涨/看跌期权理论价格。纯前端计算，数据不上传服务器。帮助投资者评估期权价值。',
        'Free online option price calculator using Black-Scholes model for European call/put option theoretical pricing. Pure frontend calculation, no server upload. Help investors evaluate option value.'
    )
    content = content.replace(
        '免费在线症状自查工具，通过选择身体部位和症状，帮助您了解可能的健康问题。纯前端查询，数据不上传服务器。仅供参考，不能替代医生诊断。',
        'Free online symptom checker. Select body parts and symptoms to learn about possible health conditions. Pure frontend, no data upload. For reference only, not a substitute for medical diagnosis.'
    )
    content = content.replace(
        '免费在线服药提醒工具，设置药品名称、剂量和提醒时间，生成服药时间表。纯前端工具，数据不上传服务器。帮助您按时服药，管理用药计划。',
        'Free online pill reminder tool. Set medication name, dosage and reminder times, generate a medication schedule. Pure frontend, no data upload. Help you take medications on time.'
    )
    content = content.replace(
        '免费在线疫苗接种时间表工具，按年龄段展示中国和美国CDC推荐的疫苗接种计划。纯前端查询，数据不上传服务器。帮助家长科学安排儿童疫苗接种。',
        'Free online vaccination schedule tool. Display recommended vaccination schedules by age based on China NIP and US CDC. Pure frontend query, no data upload. Help parents plan children vaccinations.'
    )
    content = content.replace(
        '免费在线购物清单工具，按分类管理蔬菜、水果、肉类等购物项，支持勾选已完成和分类筛选。纯前端存储，数据不上传服务器。',
        'Free online grocery list tool. Manage shopping items by category (vegetables, fruits, meat etc.), with check-off and category filtering. Pure frontend storage, no data upload.'
    )

    # Keywords
    for cn_kw, en_kw in [
        ('期权定价计算器,Black-Scholes,看涨期权,看跌期权,期权计算,在线工具,免费',
         'option price calculator,Black-Scholes,call option,put option,option pricing,online tool,free'),
        ('症状自查,健康自查,症状查询,身体检查,在线工具,免费',
         'symptom checker,health checker,symptom lookup,body check,online tool,free'),
        ('服药提醒,用药提醒,药品管理,吃药提醒,健康管理,在线工具,免费',
         'pill reminder,medication reminder,drug management,medicine reminder,health management,online tool,free'),
        ('疫苗接种时间表,儿童疫苗,预防接种,免疫计划,疫苗日历,在线工具,免费',
         'vaccination schedule,child vaccine,immunization,immunization plan,vaccine calendar,online tool,free'),
        ('购物清单,买菜清单,超市清单,购物列表,grocery list,在线工具,免费',
         'grocery list,shopping list,supermarket list,shopping checklist,grocery,online tool,free'),
    ]:
        if cn_kw in content:
            content = content.replace(cn_kw, en_kw)

    # og:title
    for cn_title, en_title in [
        ('免费在线期权定价计算器 - Black-Scholes模型 | Free ToolBase',
         'Free Online Option Price Calculator - Black-Scholes Model | Free ToolBase'),
        ('免费在线症状自查工具 - 健康参考 | Free ToolBase',
         'Free Online Symptom Checker - Health Reference | Free ToolBase'),
        ('免费在线服药提醒工具 - 用药时间表管理 | Free ToolBase',
         'Free Online Pill Reminder - Medication Schedule Manager | Free ToolBase'),
        ('免费在线疫苗接种时间表 - 儿童免疫计划 | Free ToolBase',
         'Free Online Vaccination Schedule - Child Immunization Plan | Free ToolBase'),
        ('免费在线购物清单工具 - 智能分类管理 | Free ToolBase',
         'Free Online Grocery List - Smart Category Manager | Free ToolBase'),
    ]:
        if cn_title in content:
            content = content.replace(cn_title, en_title)

    # title tag
    for cn_title, en_title in [
        ('<title>免费在线期权定价计算器 - Black-Scholes模型 | Free ToolBase</title>',
         '<title>Free Online Option Price Calculator - Black-Scholes Model | Free ToolBase</title>'),
        ('<title>免费在线症状自查工具 - 健康参考 | Free ToolBase</title>',
         '<title>Free Online Symptom Checker - Health Reference | Free ToolBase</title>'),
        ('<title>免费在线服药提醒工具 - 用药时间表管理 | Free ToolBase</title>',
         '<title>Free Online Pill Reminder - Medication Schedule Manager | Free ToolBase</title>'),
        ('<title>免费在线疫苗接种时间表 - 儿童免疫计划 | Free ToolBase</title>',
         '<title>Free Online Vaccination Schedule - Child Immunization Plan | Free ToolBase</title>'),
        ('<title>免费在线购物清单工具 - 智能分类管理 | Free ToolBase</title>',
         '<title>Free Online Grocery List - Smart Category Manager | Free ToolBase</title>'),
    ]:
        if cn_title in content:
            content = content.replace(cn_title, en_title)

    # og:description
    for cn_desc, en_desc in [
        ('免费在线期权定价计算器，支持Black-Scholes模型计算欧式看涨/看跌期权理论价格。纯前端计算，数据不上传服务器。',
         'Free online option price calculator using Black-Scholes model for European call/put option pricing. Pure frontend, no data upload.'),
        ('免费在线症状自查工具，通过选择身体部位和症状，帮助您了解可能的健康问题。纯前端查询，数据不上传服务器。',
         'Free online symptom checker. Select body parts and symptoms to learn about possible health conditions. Pure frontend, no data upload.'),
        ('免费在线服药提醒工具，设置药品名称、剂量和提醒时间，生成服药时间表。纯前端工具，数据不上传服务器。',
         'Free online pill reminder tool. Set medication name, dosage and reminder times, generate a schedule. Pure frontend, no data upload.'),
        ('免费在线疫苗接种时间表工具，按年龄段展示中国和美国CDC推荐的疫苗接种计划。纯前端查询，数据不上传服务器。',
         'Free online vaccination schedule tool. Display vaccination plans by age based on China NIP and US CDC. Pure frontend, no data upload.'),
        ('免费在线购物清单工具，按分类管理蔬菜、水果、肉类等购物项，支持勾选已完成和分类筛选。纯前端存储，数据不上传服务器。',
         'Free online grocery list tool. Manage items by category with check-off and filtering. Pure frontend storage, no data upload.'),
    ]:
        if cn_desc in content:
            content = content.replace(cn_desc, en_desc)

    # Schema.org SoftwareApplication names
    for cn_name, en_name in [
        ('期权定价计算器', 'Option Price Calculator'),
        ('症状自查工具', 'Symptom Checker'),
        ('服药提醒工具', 'Pill Reminder'),
        ('疫苗接种时间表', 'Vaccination Schedule'),
        ('购物清单工具', 'Grocery List'),
    ]:
        if cn_name in content:
            content = content.replace('"name":"' + cn_name + '"', '"name":"' + en_name + '"')

    # applicationCategory
    content = content.replace('FinanceApplication', 'FinanceApplication')
    content = content.replace('HealthApplication', 'HealthApplication')
    content = content.replace('LifestyleApplication', 'LifestyleApplication')

    # SoftwareApplication descriptions in schema
    for cn_desc, en_desc in [
        ('免费在线期权定价计算器，支持Black-Scholes模型计算欧式看涨/看跌期权理论价格。纯前端计算，数据不上传服务器。',
         'Free online option price calculator using Black-Scholes model for European call/put option theoretical pricing. Pure frontend calculation, no data upload.'),
        ('免费在线症状自查工具，通过选择身体部位和症状，帮助您了解可能的健康问题。纯前端查询，数据不上传服务器。',
         'Free online symptom checker. Select body parts and symptoms to learn about possible health conditions. Pure frontend, no data upload.'),
        ('免费在线服药提醒工具，设置药品名称、剂量和提醒时间，生成服药时间表。纯前端工具，数据不上传服务器。',
         'Free online pill reminder tool. Set medication name, dosage and reminder times. Pure frontend, no data upload.'),
        ('免费在线疫苗接种时间表工具，按年龄段展示中国和美国CDC推荐的疫苗接种计划。纯前端查询，数据不上传服务器。',
         'Free online vaccination schedule tool. Display plans by age based on China NIP and US CDC. Pure frontend, no data upload.'),
        ('免费在线购物清单工具，按分类管理蔬菜、水果、肉类等购物项，支持勾选已完成和分类筛选。纯前端存储，数据不上传服务器。',
         'Free online grocery list tool. Manage items by category with check-off and filtering. Pure frontend storage, no data upload.'),
    ]:
        if cn_desc in content:
            content = content.replace(cn_desc, en_desc)

    # Breadcrumb names
    for cn_name, en_name in [
        ('"name":"首页"', '"name":"Home"'),
        ('"name":"工具"', '"name":"Tools"'),
        ('"name":"期权定价计算器"', '"name":"Option Price Calculator"'),
        ('"name":"症状自查工具"', '"name":"Symptom Checker"'),
        ('"name":"服药提醒工具"', '"name":"Pill Reminder"'),
        ('"name":"疫苗接种时间表"', '"name":"Vaccination Schedule"'),
        ('"name":"购物清单工具"', '"name":"Grocery List"'),
    ]:
        content = content.replace(cn_name, en_name)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    # Now fix all the visible Chinese text in the HTML body...
    # This is complex, let's do per-tool manual patch after
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created {dst_path}')

for tool in NEW_TOOLS:
    src = os.path.join(TOOLS_DIR, tool, 'index.html')
    dst = os.path.join(TOOLS_DIR, 'en', tool, 'index.html')
    translate_file(src, dst, tool)
