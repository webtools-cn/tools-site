#!/usr/bin/env python3
"""Nuclear option: regex replace every Chinese character sequence in EN pages with empty or English placeholder."""
import os, re

EN_DIR = '/home/chison/tools-site/en'

TOOLS = {
    'symptom-checker': [
        # HowTo description
        ('"description":"选择身体部位，Select Symptoms，查看可能的健康信息"', '"description":"Select body part, check symptoms, view health information"'),
        # HowTo step text  
        ('"text":"浏览与您症状相关的Common健康信息"', '"text":"Browse common health information related to your symptoms"'),
        # info section
        ('<p>选择您关心的身体部位。</p>', '<p>Select the body part you\'re concerned about.</p>'),
        ('<p>勾选您感受到的具体症状。</p>', '<p>Check the specific symptoms you\'re experiencing.</p>'),
        ('<p>所有数据在本地处理，不上传服务器，保护您的隐私。</p>', '<p>All data processed locally, not uploaded to any server, protecting your privacy.</p>'),
        ('<p>点击"View Reference Info"获取健康知识科普。</p>', '<p>Click "View Reference Info" for health knowledge.</p>'),
    ],
    'pill-reminder': [
        # HowTo
        ('"description":"添加药品名称、剂量和时间，生成每日服药时间表"', '"description":"Add medication name, dosage and times, generate daily schedule"'),
        ('确定清空所有药品记录？', 'Clear all medication records?'),
        # Info
        ('<p>设置每日服药时间（可添加多个时间点）。</p>', '<p>Set daily medication times (multiple time points supported).</p>'),
        ('<p>点击添加，药品会自动保存到浏览器本地存储。</p>', '<p>Click add, medications are auto-saved to browser local storage.</p>'),
        ('<p>如需桌面通知，点击"Enable Desktop Notifications"并授权。</p>', '<p>For desktop notifications, click "Enable Desktop Notifications" and grant permission.</p>'),
        ('<p>输入药品名称和每次剂量。</p>', '<p>Enter medication name and dosage per dose.</p>'),
    ],
    'vaccination-schedule': [
        # HowTo
        ('"description":"选择年龄/月龄和国家标准，查看对应的疫苗接种计划"', '"description":"Select age/months and standard, view vaccination schedule"'),
        ('"text":"选择中国或美国CDC推荐标准"', '"text":"Select China or US CDC recommended standard"'),
        ('"text":"输入儿童当前月龄或年龄"', '"text":"Enter child age in months or years"'),
        ('"text":"查看该年龄应接种的疫苗列表和即将接种的疫苗"', '"text":"View vaccines due and upcoming for this age"'),
        # FAQ
        ('可以自定义年龄段查看吗？', 'Can I filter by age range?'),
        ('请咨询医生确认', 'Consult your doctor'),
        ('已复制到剪贴板', 'Copied to clipboard'),
    ],
    'grocery-list': [
        # HowTo
        ('"description":"添加购物项、设置分类、Set Categories"', '"description":"Add items, set categories, check off completed"'),
        ('"description":"添加购物项、设置分类、勾选已完成"', '"description":"Add items, set categories, check off completed"'),
        ('"text":"输入物品名称、数量和分类，点击添加"', '"text":"Enter item name, quantity and category, click add"'),
        ('"text":"勾选已购物品，按分类筛选查看"', '"text":"Check off purchased items, filter by category"'),
        ('"text":"One-click clear checked or export"', '"text":"One-click clear checked items or export list"'),
        ('已复制到剪贴板', 'Copied to clipboard'),
        # Info
        ('<p>输入物品名称和数量，选择分类后点击添加。</p>', '<p>Enter item name and quantity, select category, click add.</p>'),
        ('<p>使用分类筛选按钮快速查看某一品类。</p>', '<p>Use category filter buttons to quickly view a specific category.</p>'),
        ('<p>勾选已购物品，完成后可一键清除已完成项。</p>', '<p>Check off purchased items, clear done items with one click.</p>'),
        ('<p>数据自动保存到浏览器，关闭页面不会丢失。</p>', '<p>Data auto-saves to browser, won\'t be lost when you close the page.</p>'),
        ('确定清空全部购物清单？', 'Clear entire grocery list?'),
    ],
}

for tool, replacements in TOOLS.items():
    filepath = os.path.join(EN_DIR, tool, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    cn = re.findall(r'[\u4e00-\u9fff]+', content)
    print(f'{tool}: {count} replacements, {len(cn)} Chinese remaining')