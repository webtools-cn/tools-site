#!/usr/bin/env python3
"""优化短描述的页面 - 第三轮，确保全部在140-160"""

import re, os

# 只包含需要加长的
NEW_DESCRIPTIONS = {
    "chord-generator": "免费在线和弦生成器，选择根音从C到B搭配10种和弦类型（大三/小三/大七/小七/属七/挂四/挂二/加九/减三/增三），实时显示音符组成并高亮钢琴键盘对应琴键位置，支持音频试听和琶音播放两种模式。适合音乐学习者、作曲编曲爱好者快速查阅和弦结构与听感。无需注册纯前端Web Audio API实现可离线使用。",
    
    "sudoku-solver": "免费在线数独求解器，在9x9标准棋盘手动输入已知数字，一键自动求解完整数独谜题。支持回溯算法深度求解、逐步提示不直接给答案、答案正确性验证和随机生成不同难度新题目。适合数独爱好者休闲消遣、小学生数学逻辑思维训练和初学者系统学习数独解题技巧。纯前端实现无需注册可离线使用。",
    
    "pomodoro-tracker": "免费在线番茄钟计时器，基于经典番茄工作法实现25分钟专注工作+5分钟短休息的循环模式。支持自定义工作时长（1-60分钟）、短休息和长休息时间，自动切换阶段并统计完成番茄数。具有暂停、跳过、重置功能，圆形倒计时可视化显示剩余时间。适合学生备考、程序员深度工作和自由职业者时间管理。无需注册纯前端实现。",
    
    "multiplication-table-generator": "免费在线乘法表生成器，自定义1-20范围内的起始和结束数字，一键生成可打印的完整乘法表。支持完整表格、下三角九九表格式和单行三种显示模式，自动高亮对角线平方数（1×1=1、2×2=4…），附带打印功能输出纸质练习页。适合小学生数学启蒙背诵、家长课后辅导和课堂教学演示。无需注册纯前端实现。",
    
    "scientific-notation-converter": "免费在线科学计数法转换器，输入如1.5e6或3.2×10⁻⁵等格式，一键在科学计数法与普通数字之间互相转换。支持数学格式（a×10ⁿ）、编程e表示法和工程格式（指数为3的倍数）三种表示形式，可自定义小数精度位数。适合初高中物理化学计算、程序员处理大数据精度和科研工作者数据格式化。无需注册浏览器本地处理保护隐私。",
    
    "compliment-generator": "免费在线夸夸生成器，一键随机生成或按分类精准筛选真诚走心的赞美语句。涵盖性格魅力、外表气质、才华能力、鼓励加油、友情陪伴和浪漫情话六大分类共100+条人工精选夸赞语句，每条配有独立复制按钮方便分享。适合朋友生日送祝福、同事工作加油打气、伴侣日常甜蜜互动和社交媒体发帖互动。无需注册纯前端处理。",
    
    "apy-calculator": "免费在线APY年化收益率计算器，输入初始本金、名义年利率和复利频次（每日/每周/每月/每季度/每半年/每年），自动计算实际年化收益率APY和到期本息总额。附带逐年度本金与利息增长明细表格，直观对比不同复利方式下的收益差异。适合银行理财产品对比、长期储蓄规划评估和投资回报率快速计算。无需注册数据不上传服务器。",
    
    "image-brightness": "免费在线图片亮度调节工具，拖拽或点击上传JPG/PNG图片后，拖动滑块实时调整亮度（-100%至+100%），同时支持对比度和饱和度同步微调。即时预览调节效果，满意后一键下载处理后的高清图片。适合照片曝光不足快速补光修正、电商商品图亮度优化和社交媒体自拍图片美化。纯浏览器端处理保护隐私图片不上传服务器。",
    
    "high-yield-savings-calculator": "免费在线高收益储蓄计算器，输入初始本金、年化利率、每月定存金额和存款年限（1-30年），自动计算复利增长下的到期储蓄总额、累计利息收入以及本金增长趋势明细。支持年存和月存两种存款周期，折线图直观展示本息增长曲线。适合个人财务规划、储蓄目标达成设定和不同银行高收益储蓄产品对比评估。无需注册数据不上传服务器。",
    
    "salary-comparison-calculator": "免费在线薪资对比计算器，同时输入两份工作的年薪、年终奖金比例、401K/公积金匹配比例和目标城市生活成本指数，对比分析税后净收入差异、实际购买力等效薪资和综合福利价值。支持中美两地税收模式切换，考虑不同城市房租生活成本调整。适合求职offer理性决策、异地跳槽收入评估和长期职业发展规划。无需注册数据不上传服务器。",
}

# 验证长度
for k, v in NEW_DESCRIPTIONS.items():
    l = len(v)
    status = "OK" if 140 <= l <= 160 else f"NEED FIX ({l})"
    print(f"[{status}] {k}: {l} chars")

print()

# 修改
for dirname, new_desc in NEW_DESCRIPTIONS.items():
    path = os.path.join(dirname, "index.html")
    content = open(path).read()
    changes = 0
    
    # meta description
    old_meta = re.search(r'<meta name="description" content="([^"]+)"', content)
    if old_meta:
        old_full = old_meta.group(0)
        new_full = f'<meta name="description" content="{new_desc}"'
        if old_full != new_full:
            content = content.replace(old_full, new_full, 1)
            changes += 1
    
    # og:description
    if '<meta property="og:description" content="' in content:
        old_og = re.search(r'<meta property="og:description" content="([^"]+)"', content)
        if old_og:
            old_og_full = old_og.group(0)
            og_desc = new_desc[:200] if len(new_desc) > 200 else new_desc
            new_og_full = f'<meta property="og:description" content="{og_desc}"'
            if old_og_full != new_og_full:
                content = content.replace(old_og_full, new_og_full, 1)
                changes += 1
    
    # Schema
    old_schema = re.search(r'"@type"\s*:\s*"SoftwareApplication".*?"description"\s*:\s*"([^"]+)"', content, re.DOTALL)
    if old_schema:
        old_schema_full = old_schema.group(0)
        old_sd = old_schema.group(1)
        schema_desc = new_desc[:150] if len(new_desc) > 150 else new_desc
        new_schema_full = old_schema_full.replace(f'"description":"{old_sd}"', f'"description":"{schema_desc}"')
        if old_schema_full != new_schema_full:
            content = content.replace(old_schema_full, new_schema_full, 1)
            changes += 1
    
    if changes > 0:
        open(path, 'w').write(content)
        print(f"  UPDATED ({changes}): {dirname}")
    else:
        print(f"  NO CHANGE: {dirname}")

print("\n=== DONE ===")
