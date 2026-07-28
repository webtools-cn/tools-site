#!/usr/bin/env python3
"""Fix remaining Chinese in EN pages - schema FAQ and info sections."""
import os, re

EN_DIR = '/home/chison/tools-site/en'

PATCHES = {
    'symptom-checker': [
        # FAQ schema
        ('这个工具能代替医生诊断吗？', 'Can this tool replace a doctor\'s diagnosis?'),
        ('不能。本工具仅根据症状关键词匹配常见健康信息，用于知识科普和自我了解，不能替代专业医疗诊断。如有健康问题，请及时就医。',
         'No. This tool only matches symptom keywords to common health information for educational purposes. It cannot replace professional medical diagnosis. If you have health concerns, please see a doctor promptly.'),
        ('不会。所有症状查询在浏览器本地完成，您的健康和症状数据不会上传到任何服务器。可断网使用。',
         'No. All symptom queries are processed locally in the browser. Your health and symptom data is never uploaded to any server. Works offline.'),
        ('选择您关心的身体部位（如头部、胸部、腹部等），然后勾选您感受到的症状。工具会列出与该部位和症状相关的常见健康信息供参考。',
         'Select the body part you\'re concerned about (e.g., head, chest, abdomen), then check the symptoms you\'re experiencing. The tool lists common health information related to that body part and symptoms.'),
        # HowTo
        ('选择部位', 'Select Body Part'),
        ('从身体部位列表中选择您关心的区域', 'Choose the area you\'re concerned about from the body part list'),
        ('勾选症状', 'Select Symptoms'),
        ('勾选您感受到的具体症状', 'Check the specific symptoms you\'re experiencing'),
        ('浏览与您症状相关的常见健康信息', 'Browse common health information related to your symptoms'),
        # Info section
        ('选择您关心的身体部位。', 'Select the body part you\'re concerned about.'),
        ('勾选您感受到的具体症状。', 'Check the specific symptoms you\'re experiencing.'),
        ('点击"查看参考信息"获取健康知识科普。', 'Click "View Reference Info" for health knowledge.'),
        ('所有数据在本地处理，不上传服务器，保护您的隐私。', 'All data processed locally, not uploaded to any server, protecting your privacy.'),
    ],
    'pill-reminder': [
        ('这个工具的提醒会响铃吗？', 'Does this tool ring an alarm?'),
        ('本工具生成服药时间表供您参考。浏览器页面打开时可在设定的时间触发桌面通知提醒（需允许通知权限）。建议同时使用手机闹钟作为双重保障。',
         'This tool generates a medication schedule for your reference. When the browser page is open, it can trigger desktop notifications at set times (notification permission required). We recommend also using a phone alarm for double assurance.'),
        ('可以。点击"添加药品"按钮可以添加多种药品，每种药品可设置独立的服药时间和剂量。所有药品将在时间表中统一展示。',
         'Yes. Click the "Add Medication" button to add multiple medications, each with independent times and dosages. All medications are displayed together in the schedule.'),
        ('药品列表会自动保存到浏览器本地存储(LocalStorage)，下次打开页面会自动恢复。数据不上传服务器，保护您的隐私。',
         'The medication list is automatically saved to browser local storage and will restore when you reopen the page. No data is uploaded to any server, protecting your privacy.'),
        ('添加药品名称、剂量和时间，生成每日服药时间表', 'Add medication name, dosage and times, generate daily medication schedule'),
        ('添加药品', 'Add Medication'),
        ('输入药品名称、每次剂量和每日服药时间', 'Enter medication name, dosage per dose, and daily times'),
        ('启用通知', 'Enable Notifications'),
        ('如需桌面提醒，点击"启用提醒"授权通知权限', 'For desktop notifications, click "Enable Notifications" and grant permission'),
        ('输入药品名称和每次剂量。', 'Enter medication name and dosage per dose.'),
        ('设置每日服药时间（可添加多个时间点）。', 'Set daily medication times (multiple time points supported).'),
        ('点击添加，药品会自动保存到浏览器本地存储。', 'Click add, medications are auto-saved to browser local storage.'),
        ('如需桌面通知，点击"启用桌面提醒"并授权。', 'For desktop notifications, click "Enable Desktop Notifications" and grant permission.'),
    ],
    'vaccination-schedule': [
        ('中国和美国的疫苗计划有什么不同？', 'What\'s the difference between Chinese and US vaccine schedules?'),
        ('两国基本疫苗种类相似，但具体接种月龄和剂次有所不同。例如中国接种卡介苗(BCG)预防结核病，而美国不常规接种BCG。本工具同时展示两国推荐计划供参考。',
         'Both countries have similar basic vaccine types, but specific ages and doses differ. For example, China administers BCG for tuberculosis prevention while the US does not routinely give BCG. This tool shows both schedules for reference.'),
        ('中国数据参考国家卫健委《国家免疫规划疫苗儿童免疫程序》，美国数据参考CDC推荐儿童免疫计划。具体接种请以当地疾控中心和医生建议为准。',
         'China data references the NHC National Immunization Program schedule. US data references CDC recommended child immunization schedule. Follow your local CDC and doctor\'s advice for actual vaccination.'),
        ('可以。选择儿童当前年龄或月龄，工具会高亮显示该年龄段应该接种和即将接种的疫苗，方便家长对照检查。',
         'Yes. Select the child\'s current age or months, and the tool highlights vaccines due or upcoming for that age range, making it easy for parents to check.'),
        ('选择年龄/月龄和国家标准，查看对应的疫苗接种计划', 'Select age/months and national standard, view the corresponding vaccination schedule'),
        ('选择国家', 'Select Country'),
        ('选择中国或美国CDC推荐标准', 'Choose China or US CDC recommended standard'),
        ('设置年龄', 'Set Age'),
        ('输入儿童当前月龄或年龄', 'Enter child\'s current age in months or years'),
        ('查看计划', 'View Schedule'),
        ('查看该年龄应接种的疫苗列表和即将接种的疫苗', 'View the list of vaccines due and upcoming at this age'),
    ],
    'grocery-list': [
        ('购物清单数据会保存吗？', 'Will grocery list data be saved?'),
        ('会。数据自动保存到浏览器本地存储，下次打开页面会自动恢复。清除浏览器缓存可能导致数据丢失，建议重要清单导出备份。',
         'Yes. Data is automatically saved to browser local storage and will restore when you reopen the page. Clearing browser cache may cause data loss; export important lists as backup.'),
        ('可以。点击"添加分类"按钮即可创建新的购物分类，如调味品、零食、日用品等，完全自由定制。',
         'Yes. Click "Add Category" button to create new shopping categories like condiments, snacks, household items, etc. Fully customizable.'),
        ('可以。使用浏览器的打印功能(Ctrl+P)即可打印当前清单。建议在打印前点击"复制清单"先备份，或勾选已购项后只打印未购项。',
         'Yes. Use browser print function (Ctrl+P) to print the current list. We recommend copying the list first as backup, or checking off purchased items to print only pending ones.'),
        ('添加购物项、设置分类、勾选已完成', 'Add items, set categories, check off completed'),
        ('添加物品', 'Add Items'),
        ('输入物品名称、数量和分类，点击添加', 'Enter item name, quantity and category, then click add'),
        ('勾选已购物品，按分类筛选查看', 'Check off purchased items, filter by category'),
        ('一键清除已勾选项或导出清单', 'One-click clear checked items or export list'),
        ('输入物品名称和数量，选择分类后点击添加。', 'Enter item name and quantity, select category, then click add.'),
        ('使用分类筛选按钮快速查看某一品类。', 'Use category filter buttons to quickly view a specific category.'),
        ('勾选已购物品，完成后可一键清除已完成项。', 'Check off purchased items. Clear done items with one click.'),
        ('数据自动保存到浏览器，关闭页面不会丢失。', 'Data auto-saves to browser. Won\'t be lost when you close the page.'),
    ],
}

for tool, replacements in PATCHES.items():
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
    print(f'{tool}: {count}/{len(replacements)} additional replacements')