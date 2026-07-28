#!/usr/bin/env python3
"""快速生成英文版工具页面：替换中文文本为英文"""
import sys, os, re

TRANSLATIONS = {
    # meeting-agenda-generator
    'smart-goal-generator': {
        'SMART目标生成器': 'SMART Goal Generator',
        '按SMART原则（具体、可衡量、可实现、相关、有时限）制定清晰目标。一键生成目标陈述，复制导出。': 'Create clear goals using the SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound). One-click goal statement generation, copy and export.',
        '首页': 'Home', '工具': 'Tools',
        '在线SMART目标生成器': 'SMART Goal Generator',
        '免费在线SMART目标生成器，按SMART原则（具体、可衡量、可实现、相关、有时限）制定清晰目标。一键生成目标陈述，复制导出。纯前端处理，数据不上传。': 'Free online SMART goal generator. Create clear goals using the SMART framework. One-click goal statement generation, copy and export. Pure frontend, no data upload.',
        '按SMART原则制定清晰目标。纯前端处理，数据不上传。': 'Create clear goals using the SMART framework. Pure frontend, no data upload.',
        '数据绝不上传服务器': 'Data never leaves your device',
        '无需注册 · 数据绝不上传服务器': 'No registration · Data never leaves your device',
        'SMART目标,smart goal,目标设定,目标管理,在线工具,免费': 'SMART goal,goal generator,goal setting,online tool,free',
        '零依赖·可离线使用': 'Zero dependencies · Works offline',
        '免费在线SMART目标生成器 - SMART Goal Generator | 无需注册': 'Free SMART Goal Generator - No Registration Required',
        '已保存的目标': 'Saved Goals',
        '制定SMART目标': 'Create SMART Goal',
        '具体的（Specific）— 你要达成什么？': 'Specific — What to achieve?',
        '如：将网站月访问量从5万提升到10万': 'e.g. Increase monthly website traffic from 50K to 100K',
        '可衡量的（Measurable）— 如何衡量成功？': 'Measurable — How to measure success?',
        '如：Google Analytics月度UV达到10万': 'e.g. Google Analytics monthly UV reaches 100K',
        '可实现的（Achievable）— 资源是否支持？': 'Achievable — Resources available?',
        '如：通过SEO优化+内容营销+社交媒体推广': 'e.g. Via SEO + content marketing + social media',
        '相关的（Relevant）— 为何重要？': 'Relevant — Why does it matter?',
        '如：增加品牌曝光，提升产品转化率': 'e.g. Increase brand exposure, boost conversion rate',
        '有时限的（Time-bound）— 何时完成？': 'Time-bound — When to complete?',
        '如：2025年3月31日前': 'e.g. By March 31, 2025',
        '生成目标陈述': 'Generate Statement',
        '保存目标': 'Save Goal',
        '复制目标': 'Copy',
        '清空': 'Clear',
        '目标陈述': 'Goal Statement: ',
        '已保存的目标': 'Saved Goals',
        '尚未保存目标': 'No saved goals yet',
        '目标已删除': 'Goal deleted',
        '目标已保存 💾': 'Goal saved 💾',
        '已清空': 'Cleared',
        '已复制到剪贴板 📋': 'Copied to clipboard 📋',
        '请先填写并生成目标': 'Please fill in and generate first',
        '请至少填写具体目标': 'Please fill in at least the specific goal',
        '确定清空所有内容吗？': 'Clear all content?',
        'SMART目标生成器是一款免费的在线工具，无需安装任何软件即可直接在浏览器中使用。该工具完全在本地运行，您的数据不会上传到服务器，保障隐私安全。使用SMART目标生成器可以帮助您制定清晰、可执行的目标，提高目标达成率。本工具采用纯前端技术实现，打开即用，无需注册账号或下载插件。SMART原则是目标管理领域的黄金标准，被全球500强企业广泛采用。所有处理均在浏览器本地完成，响应速度快且安全可靠。': 'The SMART Goal Generator is a free online tool that requires no installation. It runs entirely in your browser and your data never leaves your device. Use it to create clear, actionable goals. Open and use instantly — no registration or downloads required.',
        '相关工具推荐': 'Related Tools',
        '行动计划生成器': 'Action Plan Generator',
        '会议议程生成器': 'Meeting Agenda Generator',
        '隐私政策': 'Privacy Policy',
    }
}

def translate_file(src, dst, tool_name):
    trans = TRANSLATIONS.get(tool_name, {})
    with open(src, 'r') as f:
        content = f.read()

    # Replace zh-CN with en
    content = content.replace('lang="zh-CN"', 'lang="en"')
    content = content.replace('lang="zh"', 'lang="en"')

    # Replace canonical
    content = re.sub(r'https://free-toolbase\.com/', 'https://free-toolbase.com/en/', content)

    # Fix hreflang - keep href pointing to en version
    # Fix lang-switch links
    content = content.replace('href="index.html" class="active">中文</a><a href="../en/', 'href="../../'+tool_name+'/">中文</a><a href="index.html" class="active">EN</a>')
    content = content.replace('href="index.html" class="active">中文</a><a href="../../en/', 'href="../../'+tool_name+'/">中文</a><a href="index.html" class="active">EN</a>')

    # Fix nav-back links
    content = content.replace('href="../index.html">首页</a> › <a href="../index.html#tools">工具</a>', 'href="../index.html">Home</a> › <a href="../index.html#tools">Tools</a>')
    content = content.replace('href="../../index.html">首页</a> › <a href="../../index.html#tools">工具</a>', 'href="../index.html">Home</a> › <a href="../index.html#tools">Tools</a>')

    # Apply text translations
    for zh, en in trans.items():
        content = content.replace(zh, en)

    # Fix STORAGE_KEY to add -en suffix
    content = content.replace("STORAGE_KEY='", "STORAGE_KEY='"+tool_name+"-en-")

    # Fix placeholders
    content = content.replace('如：', 'e.g. ')
    content = content.replace('如: ', 'e.g. ')

    # Fix remaining Chinese UI text
    content = re.sub(r'placeholder="如：([^"]*)"', r'placeholder="e.g. \1"', content)

    # Fix related tools links to /en/
    content = content.replace('href="/action-plan/', 'href="/en/action-plan/')
    content = content.replace('href="/meeting-agenda-generator/', 'href="/en/meeting-agenda-generator/')
    content = content.replace('href="/meeting-notes/', 'href="/en/meeting-notes/')
    content = content.replace('href="/smart-goal-generator/', 'href="/en/smart-goal-generator/')
    content = content.replace('href="/subscription-revenue-calculator/', 'href="/en/subscription-revenue-calculator/')
    content = content.replace('href="/project-estimate-calculator/', 'href="/en/project-estimate-calculator/')
    content = content.replace('href="/profit-per-unit-calculator/', 'href="/en/profit-per-unit-calculator/')
    content = content.replace('href="/profit-margin-calculator/', 'href="/en/profit-margin-calculator/')
    content = content.replace('href="/break-even-calculator/', 'href="/en/break-even-calculator/')
    content = content.replace('href="/commission-calculator/', 'href="/en/commission-calculator/')
    content = content.replace('href="/burn-rate-calculator/', 'href="/en/burn-rate-calculator/')
    content = content.replace('href="/runway-calculator/', 'href="/en/runway-calculator/')
    content = content.replace('href="/revenue-calculator/', 'href="/en/revenue-calculator/')
    content = content.replace('href="/swot-analysis/', 'href="/en/swot-analysis/')
    content = content.replace('href="/business-plan-generator/', 'href="/en/business-plan-generator/')

    # Fix href="/" to href="/en/"
    content = re.sub(r'href="/"(?!en)', 'href="/en/"', content)
    content = re.sub(r'href="/privacy"', 'href="/en/privacy"', content)

    with open(dst, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    base = '/home/chison/tools-site'
    tools = ['smart-goal-generator', 'subscription-revenue-calculator', 'project-estimate-calculator', 'profit-per-unit-calculator', 'pitch-deck-outline']

    for tool in tools:
        src = f'{base}/{tool}/index.html'
        dst = f'{base}/en/{tool}/index.html'
        translate_file(src, dst, tool)
        print(f'✅ {tool} EN done')
