#!/usr/bin/env python3
"""Final aggressive fix: replace ALL remaining Chinese in EN pages."""
import os, re

EN_DIR = '/home/chison/tools-site/en'

REPLACEMENTS = [
    # symptom-checker FAQ
    ('"如何使用这个症状自查工具？"', '"How to Use This Symptom Checker?"'),
    ('"选择您关心的身体部位（如头部、胸部、腹部等），然后勾选您感受到的症状。工具会列出与该部位和症状相关的常见健康信息供参考。"',
     '"Select a body part (e.g. head, chest, abdomen), then check the symptoms you feel. The tool lists common health information for reference."'),
    ('"数据会上传到服务器吗？"', '"Is data uploaded to the server?"'),
    ('"不会。所有症状查询在浏览器本地完成，您的健康和症状数据不会上传到任何服务器。可断网使用。"',
     '"No. All symptom queries happen locally in the browser. Your health and symptom data is never uploaded to any server. Works offline."'),
    ('"可以。选择儿童当前年龄或月龄，工具会高亮显示该年龄段应该接种和即将接种的疫苗，方便家长对照检查。"',
     '"Yes. Select the child\'s current age in months, and the tool highlights vaccines due or upcoming for that range."'),
    # Knowledge base text
    ('感冒引起的咳嗽，通常伴流涕、咽痛，1-2周自愈。', 'Cough from common cold, usually with runny nose and sore throat, self-resolves in 1-2 weeks.'),
    ('丛集性', 'Cluster'),
    ('小时', 'hours'),
    ('吸烟是主因', 'smoking is main cause'),
    ('单侧剧烈疼痛，集中在眼周，发作时间短但频率高。', 'Severe unilateral pain around the eye, short attacks but high frequency.'),
    ('心理因素导致胸部紧绷感，深呼吸可缓解。', 'Psychological factor causing chest tightness, relieved by deep breathing.'),
    ('胸骨后压迫感，活动时加重，休息缓解。需及时就医。', 'Substernal pressure, worsens with activity, relieved by rest. Seek medical attention.'),
    ('感觉心跳过快、过慢或不规则搏动。咖啡因、压力可诱发。', 'Sensation of fast, slow or irregular heartbeat. Caffeine and stress can trigger.'),
    ('伴随心慌、出汗、呼吸急促。心理因素引发。', 'Accompanied by palpitations, sweating, rapid breathing. Triggered by psychological factors.'),
    ('上腹部不适、胀气，与饮食有关。', 'Upper abdominal discomfort, bloating, related to diet.'),
    ('伴腹泻、恶心、呕吐，多为病毒或细菌感染。', 'With diarrhea, nausea, vomiting. Usually viral or bacterial.'),
    ('右下腹持续性疼痛，按压痛明显，常伴发热。需急诊。', 'Persistent right lower abdominal pain with tenderness, often with fever. Requires emergency.'),
    ('肠道气体过多，与饮食、肠道菌群相关。', 'Excess intestinal gas, related to diet and gut flora.'),
    ('反复腹胀、腹痛伴排便习惯改变。', 'Recurrent bloating and pain with changes in bowel habits.'),
    ('关节退行性变，晨僵<30分钟，活动后改善。', 'Degenerative joint changes, morning stiffness <30 min, improves with activity.'),
    ('对称性多关节肿痛，晨僵>1小时。自身免疫疾病。', 'Symmetrical polyarthritis with swelling, morning stiffness >1 hour. Autoimmune.'),
    ('大脚趾等关节突发剧痛、红肿热痛，与高尿酸相关。', 'Sudden severe pain, redness, swelling in joints like big toe. Related to high uric acid.'),
    ('运动后24-72小时肌肉酸痛，正常生理反应。', 'Muscle soreness 24-72 hours post-exercise. Normal physiological response.'),
    ('全身广泛疼痛、疲劳、睡眠障碍。', 'Widespread pain, fatigue, and sleep disturbance.'),
    ('皮肤干燥、红斑、瘙痒，常有渗出。', 'Dry skin, erythema, itching, often with exudation.'),
    ('红色风团，瘙痒，大小不等，可自行消退再复发。', 'Red wheals, itching, variable size. Can resolve and recur spontaneously.'),
    ('用药后出现皮疹，需停药就医。', 'Rash after medication, requires discontinuation and medical attention.'),
    ('接触过敏原后干咳，伴打喷嚏、鼻痒。', 'Dry cough after allergen exposure, with sneezing and nasal itching.'),
    ('每年咳嗽>3个月，连续>2年。', 'Cough >3 months/year for >2 consecutive years.'),
    # Body parts
    ('腹部', 'Abdomen'),
    ('胸部', 'Chest'),
    ('皮肤', 'Skin'),
    ('四肢', 'Limbs'),
    ('呼吸系统', 'Respiratory'),
    # pill-reminder
    ('"可以设置多种药品吗？"', '"Can I set multiple medications?"'),
    ('"可以。点击\\"添加药品\\"按钮可以添加多种药品，每种药品可设置独立的服药时间和剂量。所有药品将在时间表中统一展示。"',
     '"Yes. Click Add Medication to add multiple meds, each with independent times and dosages. All appear in the schedule."'),
    ('"数据会保存吗？"', '"Will data be saved?"'),
    ('"药品列表会自动保存到浏览器本地存储(LocalStorage)，下次打开页面会自动恢复。数据不上传服务器，保护您的隐私。"',
     '"Medication list auto-saves to browser LocalStorage and restores on next visit. No data is uploaded, protecting your privacy."'),
    ('"这个工具的提醒会响铃吗？"', '"Does this tool ring an alarm?"'),
    ('"本工具生成服药时间表供您参考。浏览器页面打开时可在设定的时间触发桌面通知提醒（需允许通知权限）。建议同时使用手机闹钟作为双重保障。"',
     '"This tool generates a medication schedule. When the page is open, it can trigger desktop notifications at set times (permission required). Use a phone alarm as backup."'),
    # vaccination-schedule
    ('"中国和美国的疫苗计划有什么不同？"', '"What\'s different between Chinese and US vaccine schedules?"'),
    ('"两国基本疫苗种类相似，但具体接种月龄和剂次有所不同。例如中国接种卡介苗(BCG)预防结核病，而美国不常规接种BCG。本工具同时展示两国推荐计划供参考。"',
     '"Both countries have similar vaccine types, but ages and doses differ. For example, China administers BCG for TB prevention while the US doesn\'t. This tool shows both for reference."'),
    ('"数据来源是什么？"', '"What are the data sources?"'),
    ('"中国数据参考国家卫健委《国家免疫规划疫苗儿童免疫程序》，美国数据参考CDC推荐儿童免疫计划。具体接种请以当地疾控中心和医生建议为准。"',
     '"China data references the NHC National Immunization Program. US data references CDC recommendations. Follow your local CDC and doctor for actual vaccination."'),
    ('"可以。选择儿童当前年龄或月龄，工具会高亮显示。"', '"Yes. Select child age and the tool highlights relevant vaccines."'),
    # grocery-list
    ('"购物清单数据会保存吗？"', '"Will grocery list data be saved?"'),
    ('"会。数据自动保存到浏览器本地存储，下次打开页面会自动恢复。清除浏览器缓存可能导致数据丢失，建议重要清单导出备份。"',
     '"Yes. Data auto-saves to browser local storage and restores on next visit. Clearing cache may cause data loss; export important lists as backup."'),
    ('"可以添加自定义分类吗？"', '"Can I add custom categories?"'),
    ('"可以。点击\\"添加分类\\"按钮即可创建新的购物分类，如调味品、零食、日用品等，完全自由定制。"',
     '"Yes. Click Add Category to create new categories like condiments, snacks, household items. Fully customizable."'),
    ('"可以打印购物清单吗？"', '"Can I print the grocery list?"'),
    ('"可以。使用浏览器的打印功能(Ctrl+P)即可打印当前清单。建议在打印前点击\\"复制清单\\"先备份，或勾选已购项后只打印未购项。"',
     '"Yes. Use browser print (Ctrl+P) to print the current list. We recommend copying first as backup, or checking off purchased items first."'),
    # Common footer etc
    ('首页', 'Home'),
    ('隐私政策', 'Privacy'),
    ('使用条款', 'Terms'),
]

for tool in ['symptom-checker','pill-reminder','vaccination-schedule','grocery-list']:
    filepath = os.path.join(EN_DIR, tool, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Check remaining
    cn = set(re.findall(r'[\u4e00-\u9fff]+', content))
    print(f'{tool}: {count} replacements, {len(cn)} Chinese remaining: {list(cn)[:10]}')