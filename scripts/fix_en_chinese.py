#!/usr/bin/env python3
"""英化 EN 页面中的中文 - 集中修复4个页面"""
import os, re

SITE = '/home/chison/tools-site'

# 中文→英文映射 (可见文本和Schema)
REPLACE_MAP = {
    # ===== project-estimate-calculator =====
    'en/project-estimate-calculator/index.html': [
        # h1
        ('<h1>📐 项目估算计算器</h1>', '<h1>📐 Project Estimate Calculator</h1>'),
        # nav-back
        ('Tools</a> › 项目估算计算器', 'Tools</a> › Project Estimate Calculator'),
        # hero
        ('<p>免费在线项目估算计算器，快速估算项目时间、成本和人力资源。支持任务分解、三种估算方法。纯前端处理，数据不上传。 | No registration', '<p>Free online project estimate calculator. Quickly estimate project time, cost and resources. Supports task breakdown and three estimation methods. Pure frontend, no data upload. | No registration'),
        # section h2
        ('<h2>⚙️ 项目设置</h2>', '<h2>⚙️ Project Settings</h2>'),
        ('<h2>📝 任务列表</h2>', '<h2>📝 Task List</h2>'),
        ('<h2>📊 估算结果</h2>', '<h2>📊 Estimation Results</h2>'),
        # labels
        ('<label>日费率 ($)</label>', '<label>Daily Rate ($)</label>'),
        ('<label>团队人数</label>', '<label>Team Size</label>'),
        ('<label>任务名称</label>', '<label>Task Name</label>'),
        # placeholder
        ('placeholder="如：前端页面开发"', 'placeholder="e.g.: Frontend Development"'),
        # button
        ('＋ 添加任务', '＋ Add Task'),
        ('🗑️ 清空', '🗑️ Clear'),
        ('📋 加载示例', '📋 Load Example'),
        # result labels
        ('>⏱ PERT加权总时间<', '>⏱ PERT Weighted Total<'),
        ('>💰 预估总成本<', '>💰 Estimated Total Cost<'),
        ('>📅 预计工期(团队)<', '>📅 Duration (Team)<'),
        ('>🕐 乐观总时间<', '>🕐 Optimistic Total<'),
        # result values
        ('0天', '0 days'),
        # JS strings
        ("'需求分析与设计'", "'Requirements & Design'"),
        ("'前端页面开发'", "'Frontend Development'"),
        ("'后端API开发'", "'Backend API Development'"),
        ("'测试与修复'", "'Testing & Bug Fixes'"),
        ("'部署上线'", "'Deployment'"),
        ("toFixed(1)+'天'", "toFixed(1)+' days'"),
        ("teamDays+'天'", "teamDays+' days'"),
        ("'天</span>", "' days</span>"),
        ("opt:'", "opt:'"),  # keep
        ("' ✕ 删除'", "' ✕ Delete'"),
        ("'任务已删除'", "'Task deleted'"),
        ("'请输入任务名称'", "'Please enter task name'"),
        ("'时间应满足：乐观≤最可能≤悲观'", "'Time must satisfy: Opt ≤ Most Likely ≤ Pess'"),
        ("'任务已添加 ✅'", "'Task added ✅'"),
        ("'已清空'", "'Cleared'"),
        ("'已加载示例 ✅'", "'Example loaded ✅'"),
        ("'确定清空所有任务吗？'", "'Clear all tasks?'"),
        # 点击
        ("点击「加载示例」或添加任务", "Click \"Load Example\" or add tasks"),
        # Schema names
        ('"name":"项目估算计算器"', '"name":"Project Estimate Calculator"'),
        ('"name":"如何进行项目估算"', '"name":"How to Estimate a Project"'),
        ('"name":"项目估算计算器"', '"name":"Project Estimate Calculator"'),
        ('"name":"添加任务"', '"name":"Add Tasks"'),
        ('"name":"设置费率"', '"name":"Set Rate"'),
        ('"name":"查看结果"', '"name":"View Results"'),
        ('"描述":', '"description":'),
        # Schema text
        ('"text":"逐项添加项目任务及其三种估算时间"', '"text":"Add project tasks one by one with three estimates each"'),
        ('"text":"输入团队日费率或时费率"', '"text":"Enter team daily or hourly rate"'),
        ('"text":"自动计算PERT加权时间和总成本"', '"text":"Auto-calculate PERT weighted time and total cost"'),
        ('"description":"免费在线项目估算计算器，快速估算项目时间、成本和人力资源。支持任务分解、三种估算方法，PERT加权计算。纯前端处理，数据不上传。"',
         '"description":"Free online project estimate calculator. Quickly estimate project time, cost and resources. Supports task breakdown, three estimation methods, PERT weighted calculation. Pure frontend, no data upload."'),
        ('"description":"使用项目估算计算器的步骤指南"',
         '"description":"Step-by-step guide to using the project estimate calculator"'),
        # FAQ
        ('"name":"什么是PERT估算？"', '"name":"What is PERT estimation?"'),
        ('"text":"PERT（Program Evaluation and Review Technique）是一种三点估算方法：期望时间 = (乐观+4×最可能+悲观)/6。它能更准确地反映项目的不确定性。"',
         '"text":"PERT (Program Evaluation and Review Technique) is a three-point estimation method: Expected Time = (Optimistic + 4×Most Likely + Pessimistic)/6. It better reflects project uncertainty."'),
        ('"name":"数据会保存吗？"', '"name":"Is my data saved?"'),
        ('"text":"数据保存在浏览器本地存储（localStorage），再次打开页面会自动恢复。不会上传到任何服务器。"',
         '"text":"Data is saved in browser localStorage and auto-restores on revisit. Nothing is uploaded to any server."'),
        # Breadcrumb
        ('"name":"项目估算计算器","item":"https://free-toolbase.com/en/project-estimate-calculator/"',
         '"name":"Project Estimate Calculator","item":"https://free-toolbase.com/en/project-estimate-calculator/"'),
        # seo-content
        ('<p>项目估算计算器是一款免费的在线工具，帮助项目经理和团队快速估算项目时间和成本。采用PERT三点估算法，比单一估算更准确。支持任务分解、团队规模调整、日费率设置。该工具完全在本地运行，数据不上传。所有处理均在浏览器本地完成，响应速度快且安全可靠。</p>',
         '<p>The Project Estimate Calculator is a free online tool that helps project managers and teams quickly estimate project time and cost. It uses the PERT three-point estimation method, which is more accurate than single-point estimates. Supports task breakdown, team size adjustment, and daily rate settings. The tool runs entirely locally, with no data uploads. All processing happens in the browser, ensuring fast response and data security.</p>'),
        # related tools
        ('📋 行动计划生成器', '📋 Action Plan Generator'),
        ('💰 订阅收入计算器', '💰 Subscription Revenue Calculator'),
    ],
}

for fp, replacements in REPLACE_MAP.items():
    path = os.path.join(SITE, fp)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            fixed += 1
        else:
            print(f'  [!] Not found in {fp}: {old[:60]}...')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✅ {fp}: {fixed}/{len(replacements)} replacements')

# Also fix remaining '天' in the file specifically
path = os.path.join(SITE, 'en/project-estimate-calculator/index.html')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining 天 in JS that wasn't caught
import re
# Fix 0天 values: only in JS result strings
content = content.replace("'0天'", "'0 days'")
content = re.sub(r"toFixed\(\d\)\+'天'", lambda m: m.group().replace("'天'", "' days'"), content)
content = content.replace("+'天'", "+' days'")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Final day→days cleanup done')
