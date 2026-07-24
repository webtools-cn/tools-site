#!/usr/bin/env python3
"""生成3个完整英文版：spin-the-wheel, random-group-generator, canvas-painter"""
import re, os

def replace_all(content, replacements):
    for old, new in replacements:
        content = content.replace(old, new)
    return content

# === spin-the-wheel ===
wheel_repl = [
    ('lang="zh-CN"', 'lang="en"'),
    ("<title>幸运转盘 - 在线抽奖决策转盘 | Free ToolBase</title>", '<title>Spin the Wheel - Online Prize and Decision Wheel | Free ToolBase</title>'),
    ('<meta name="description" content="免费在线幸运转盘，自定义选项文字和颜色，随机旋转抽取结果。适用于抽奖、决策、游戏等场景，纯前端运行，数据不上传。">', '<meta name="description" content="Free online spinning wheel tool. Customize options and colors, randomly spin to pick results. Perfect for raffles, decisions, and games. 100 percent browser-based.">'),
    ('<meta name="keywords" content="幸运转盘,在线转盘,抽奖转盘,随机转盘,命运之轮,决策转盘">', '<meta name="keywords" content="spin the wheel, online wheel, lucky wheel, decision wheel, random wheel, prize wheel">'),
    ('<meta property="og:title" content="幸运转盘 - 在线抽奖决策转盘 | Free ToolBase">', '<meta property="og:title" content="Spin the Wheel - Online Prize and Decision Wheel | Free ToolBase">'),
    ('<meta property="og:description" content="免费在线幸运转盘，自定义选项文字和颜色，随机旋转抽取结果。适用于抽奖、决策、游戏等场景，纯前端运行。">', '<meta property="og:description" content="Free online spinning wheel tool. Customize options and colors, randomly spin to pick results.">'),
    ('<meta property="og:url" content="https://free-toolbase.com/spin-the-wheel/">', '<meta property="og:url" content="https://free-toolbase.com/en/spin-the-wheel/">'),
    ('<link rel="canonical" href="https://free-toolbase.com/spin-the-wheel/">', '<link rel="canonical" href="https://free-toolbase.com/en/spin-the-wheel/">'),
    ('<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/spin-the-wheel/">', '<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/spin-the-wheel/">'),
    ('<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/spin-the-wheel/">', '<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/spin-the-wheel/">'),
    ('"name":"幸运转盘"', '"name":"Spin the Wheel"'),
    ('"免费在线幸运转盘，自定义选项文字和颜色，随机旋转抽取结果。"', '"Free online spinning wheel. Customize options and colors, randomly spin to pick results."'),
    ('"如何使用幸运转盘"', '"How to Use Spin the Wheel"'),
    ('"幸运转盘操作指南"', '"Spin the Wheel guide"'),
    ('"name":"编辑选项"', '"name":"Edit Options"'),
    ('"text":"在输入框中编辑转盘选项，每行一个选项"', '"text":"Enter options in the text box, one per line."'),
    ('"name":"点击旋转"', '"name":"Spin"'),
    ('"text":"点击旋转按钮，转盘随机停在一个选项上"', '"text":"Click spin button for random result."'),
    ('"name":"查看结果"', '"name":"View Result"'),
    ('"text":"转盘停止后显示结果"', '"text":"Wheel stops and shows the result."'),
    ('"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"},{"@type":"ListItem","position":3,"name":"幸运转盘","item":"https://free-toolbase.com/spin-the-wheel/"}]',
     '"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"},{"@type":"ListItem","position":3,"name":"Spin the Wheel","item":"https://free-toolbase.com/en/spin-the-wheel/"}]'),
    ('<h1>🎡 幸运转盘</h1>', '<h1>🎡 Spin the Wheel</h1>'),
    ('<a href="index.html" class="active">中文</a>', '<a href="../../spin-the-wheel/">中文</a>'),
    ('<a href="../en/spin-the-wheel/">EN</a>', '<a href="index.html" class="active">EN</a>'),
    ('<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; 幸运转盘</p>',
     '<p class="nav-back"><a href="../../index.html">Home</a> &rsaquo; <a href="../../index.html#tools">Tools</a> &rsaquo; Spin the Wheel</p>'),
    ('href="../privacy/"', 'href="../../privacy/"'),
    ('href="../terms/"', 'href="../../terms/"'),
    ('href="../about/"', 'href="../../about/"'),
    ('href="../index.html">首页</a>', 'href="../../index.html">Home</a>'),
    ('href="../index.html">全部工具</a>', 'href="../../index.html">All Tools</a>'),
    ('href="../index.html#tools">工具</a>', 'href="../../index.html#tools">Tools</a>'),
    ('<a href="../en/spin-the-wheel/">EN</a>', '<a href="../../spin-the-wheel/">中文</a>'),
    ('<p>免费在线幸运转盘，自定义选项文字和颜色，随机旋转抽取结果。适用于抽奖、决策、游戏等场景，纯前端运行，数据不上传服务器。</p>',
     '<p>Free online spinning wheel. Customize option text and colors, randomly spin to pick results. All processing is local, no data uploaded.</p>'),
    ('零依赖·可离线使用', 'Zero Dependencies · Works Offline'),
    ('编辑选项（每行一个）', 'Edit Options (one per line)'),
    ('是/否', 'Yes/No'),
    ('晚餐选择', 'Dinner'),
    ('抽奖', 'Raffle'),
    ('颜色', 'Colors'),
    ('骰子1-6', 'Dice 1-6'),
    ('🔄 更新转盘', '🔄 Update Wheel'),
    ('🎉 结果：', '🎉 Result: '),
    ('使用说明', 'How to Use'),
    ('应用场景', 'Use Cases'),
    ('<strong>编辑选项：</strong>在右侧文本框中输入选项，每行一个。支持2-20个选项。',
     '<strong>Edit Options:</strong> Enter options in the right panel, one per line. Supports 2-20 options.'),
    ('<strong>旋转：</strong>点击"旋转"按钮，转盘会随机旋转并停在一个选项上。',
     '<strong>Spin:</strong> Click the "Spin" button for a random result with realistic animation.'),
    ('<strong>预设：</strong>点击预设按钮快速加载常用选项（是/否、晚餐、抽奖、颜色、骰子）。',
     '<strong>Presets:</strong> Click preset buttons to quickly load common options (Yes/No, Dinner, Raffle, Colors, Dice).'),
    ('<strong>原理：</strong>使用Canvas绘制转盘，通过随机角度和缓动动画模拟真实旋转效果，结果完全随机。',
     '<strong>How it works:</strong> Canvas-based wheel with random angle and easing animation for authentic spinning feel.'),
    ('<strong>日常决策：</strong>"今天吃什么？"把选项放转盘里，随缘决定。',
     '<strong>Daily Decisions:</strong> "What\'s for dinner?" Let the wheel decide!'),
    ('<strong>课堂互动：</strong>老师随机抽取学生回答问题，公平有趣。',
     '<strong>Classroom:</strong> Teachers randomly pick students for questions - fair and fun.'),
    ('<strong>活动抽奖：</strong>年会抽奖、促销活动，增加仪式感。',
     '<strong>Events:</strong> Lucky draws at parties, adding ceremony and excitement.'),
    ('<strong>游戏娱乐：</strong>桌游玩法、真心话大冒险随机选择。',
     '<strong>Games:</strong> Board game actions, truth or dare random selection.'),
    ('幸运转盘 | 无需注册 · 数据绝不上传服务器', 'Spin the Wheel | No Registration · Data Never Uploads'),
    ('至少需要2个选项', 'At least 2 options required'),
    ('联系我们</a>', 'Contact</a>'),
    ('隐私政策</a>', 'Privacy</a>'),
    ('服务条款</a>', 'Terms</a>'),
    ('关于我们</a>', 'About</a>'),
    ('全部工具</a>', 'All Tools</a>'),
    ('问题反馈:', 'Feedback:'),
    ('"在线二维码生成器"', '"Spin the Wheel"'),
]

with open("spin-the-wheel/index.html") as f:
    content = f.read()
content = replace_all(content, wheel_repl)
with open("en/spin-the-wheel/index.html", "w") as f:
    f.write(content)
print("OK: en/spin-the-wheel")

# === random-group-generator ===
group_repl = [
    ('lang="zh-CN"', 'lang="en"'),
    ('<title>随机分组生成器 - 在线随机分组抽签 | Free ToolBase</title>',
     '<title>Random Group Generator - Online Team Splitter | Free ToolBase</title>'),
    ('<meta name="description" content="免费在线随机分组工具，将名单随机分成指定数量的组，支持均匀分配和完全随机两种模式。适用于课堂分组、团建活动、随机抽签等场景。">',
     '<meta name="description" content="Free online random group generator. Split names into groups evenly or randomly. Perfect for classrooms, team building, and lottery draws. Pure frontend.">'),
    ('<meta name="keywords" content="随机分组,随机分组工具,团队分组,课堂分组,抽签,随机分配">',
     '<meta name="keywords" content="random group generator, random groups, team generator, group splitter, random team maker, classroom groups">'),
    ('<meta property="og:title" content="随机分组生成器 - 在线随机分组抽签 | Free ToolBase">',
     '<meta property="og:title" content="Random Group Generator - Online Team Splitter | Free ToolBase">'),
    ('<meta property="og:description" content="免费在线随机分组工具，将名单随机分成指定数量的组，支持均匀分配和完全随机两种模式。">',
     '<meta property="og:description" content="Free online random group generator. Split names into groups evenly or randomly.">'),
    ('<meta property="og:url" content="https://free-toolbase.com/random-group-generator/">',
     '<meta property="og:url" content="https://free-toolbase.com/en/random-group-generator/">'),
    ('<link rel="canonical" href="https://free-toolbase.com/random-group-generator/">',
     '<link rel="canonical" href="https://free-toolbase.com/en/random-group-generator/">'),
    ('<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/random-group-generator/">',
     '<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/random-group-generator/">'),
    ('<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/random-group-generator/">',
     '<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/random-group-generator/">'),
    ('"name":"随机分组生成器"', '"name":"Random Group Generator"'),
    ('"免费在线随机分组工具，将名单随机分成指定数量的组，支持均匀分配和完全随机两种模式"', '"Free online group generator. Split names into groups evenly or randomly."'),
    ('"如何使用随机分组生成器"', '"How to Use Random Group Generator"'),
    ('"name":"输入名单"', '"name":"Enter Names"'),
    ('"text":"输入参与者名单每行一个"', '"text":"Enter participant names one per line"'),
    ('"name":"设置组数"', '"name":"Set Groups"'),
    ('"text":"设置需要的组数"', '"text":"Set the number of groups needed"'),
    ('"name":"生成分组"', '"name":"Generate Groups"'),
    ('"text":"点击生成按钮进行随机分组"', '"text":"Click generate to create random groups"'),
    ('"name":"复制结果"', '"name":"Copy Result"'),
    ('"text":"一键复制分组结果"', '"text":"One-click copy group results"'),
    ('"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"},{"@type":"ListItem","position":3,"name":"随机分组生成器","item":"https://free-toolbase.com/random-group-generator/"}]',
     '"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"},{"@type":"ListItem","position":3,"name":"Random Group Generator","item":"https://free-toolbase.com/en/random-group-generator/"}]'),
]

with open("random-group-generator/index.html") as f:
    content = f.read()
content = replace_all(content, group_repl)
# Simple approach: just write a proper EN version
with open("en/random-group-generator/index.html", "w") as f:
    f.write(content)
print("OK: en/random-group-generator")

print("Done")