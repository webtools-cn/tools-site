#!/usr/bin/env python3
"""优化工具页面meta description到140-160字符 - 第二轮（更长的描述）"""

import re, os

# 新描述 - 确保每个在140-160字符之间（中文按字符计）
NEW_DESCRIPTIONS = {
    "chord-generator": "免费在线和弦生成器，选择根音（C-B）和10种和弦类型（大三/小三/七和弦/挂留/增减），实时显示音符组成并高亮钢琴键盘对应琴键，支持音频试听和琶音播放。适合音乐学习者、作曲编曲爱好者快速查阅和弦构成与听感。无需注册，纯前端Web Audio API实现，可离线使用。",
    
    "sudoku-solver": "免费在线数独求解器，在9x9棋盘输入已知数字一键求解完整数独谜题。支持自动求解（回溯算法）、逐步提示、答案正确性验证和随机生成新题目，游戏难度可调。适合数独爱好者消遣娱乐、小学生数学逻辑思维训练和初学者学习解题技巧。纯前端实现无需注册可离线使用。",
    
    "pomodoro-tracker": "免费在线番茄钟计时器，基于番茄工作法实现25分钟专注工作+5分钟短休息循环，支持自定义工作/短休息/长休息时长。自动切换阶段并统计完成番茄数，暂停跳过重置齐全，圆形倒计时可视化显示进度。适合学生备考、程序员深度工作和自由职业者时间管理。无需注册纯前端实现。",
    
    "multiplication-table-generator": "免费在线乘法表生成器，自定义1-20范围快速生成可打印乘法表。支持完整表格、下三角九九表格式和单行三种显示模式，自动高亮对角线平方数（1×1、2×2等），一键打印输出纸质练习页。适合小学生数学启蒙、家长课后辅导和课堂教学演示。无需注册纯前端实现。",
    
    "scientific-notation-converter": "免费在线科学计数法转换器，输入如1.5e6或3.2×10⁻⁵等科学计数法格式，一键转为普通数字或反向转换。支持数学格式、e表示法和工程格式三向互转，可自定义小数点精度。适合初高中物理化学计算、程序员处理大数和科研工作者数据格式化。无需注册浏览器本地处理隐私安全。",
    
    "compliment-generator": "免费在线夸夸生成器，一键随机生成或按分类筛选真诚赞美语句。涵盖性格魅力、外表气质、才华能力、鼓励加油、友情陪伴和浪漫情话六大分类共100+条人工精选夸赞语句，支持一键复制分享。适合朋友生日祝福、同事工作鼓励、伴侣甜蜜互动和社交媒体发帖。无需注册纯前端处理。",
    
    "apy-calculator": "免费在线APY年化收益率计算器，输入名义年利率和复利频次（日/周/月/季/半年/年），自动计算实际年化收益率APY和最终本息总额。附带逐年本金利息增长明细表，直观对比不同复利方式收益差异。适合银行理财产品对比、长期储蓄规划和投资回报率评估。无需注册数据不上传服务器。",
    
    "fibonacci": "免费在线斐波那契数列生成器，输入项数（1-100）一键生成完整斐波那契数列：0,1,1,2,3,5,8,13... 支持逗号/空格/换行三种分隔方式和连续或间隔显示模式，实时计算相邻项比值逼近黄金比例1.618。适合数学教学演示、算法编程练习题和自然规律探索。无需注册纯前端计算。",
    
    "image-brightness": "免费在线图片亮度调节工具，拖拽或上传图片后拖动滑块实时调整亮度（-100%至+100%），同时支持对比度和饱和度同步调节，即时预览效果并一键下载处理后的JPG/PNG图片。适合照片曝光不足快速补光、电商商品图调亮和社交媒体图片美化。纯浏览器端处理保护隐私图片不上传服务器。",
    
    "high-yield-savings-calculator": "免费在线高收益储蓄计算器，输入初始本金、年利率、每月定存金额和存款年限，自动计算复利增长下的最终储蓄总额、累计利息收入和本金增长趋势。支持年/月两种存款周期，直观图表展示本息增长曲线。适合个人财务规划、储蓄目标设定和不同银行产品收益对比。无需注册数据不上传服务器。",
    
    "color-gradient-extractor": "免费在线图片渐变色提取工具，上传任意图片自动使用K-means聚类分析识别主要颜色并生成渐变配色方案。提取5-10种主色，自动生成线性渐变CSS代码和HEX/RGB调色板。适合UI/UX设计师提取品牌色、前端开发者渐变参考和海报设计灵感获取。无需注册纯浏览器端处理图片不上传服务器。",
    
    "salary-comparison-calculator": "免费在线薪资对比计算器，输入两份工作的年薪、奖金、401K/公积金匹配比例和生活成本城市指数，对比计算税后净收入、实际购买力等效薪资和综合福利价值。支持中美两地税收模式切换和不同城市生活成本调整。适合求职offer决策、异地跳槽评估和职业发展规划。无需注册数据不上传服务器。",
    
    "html-entity-codec": '免费在线HTML实体编解码工具，一键将特殊字符（<>&"\'©®™€等）编码为HTML实体（&lt; &amp; &quot;）或解码回原始字符。支持HTML5全部命名实体和十进制/十六进制数字实体，内置200+常用实体速查表。适合前端开发者处理用户输入防XSS注入、HTML模板转义和邮件编码。无需注册纯前端处理。',
    
    "website-speed-test": "免费在线网站速度检测工具，输入任意URL一键分析页面性能：总大小、JS/CSS/图片/字体等各类资源数量和大小分布、域名数和预估加载时间。基于纯前端检测无需后端服务，提供页面结构分析和针对性优化建议。适合网站开发者SEO性能审计、站长优化加载速度和前端性能调优。无需安装直接使用。",
    
    "spaced-repetition-scheduler": "免费在线间隔重复调度器，基于经典SM-2算法科学规划记忆复习时间。输入学习科目名称和首次掌握程度评分（0-5分），自动计算下次复习最佳日期、复习间隔天数和遗忘概率。支持多科目并行管理和复习历史追踪，可视化展示遗忘曲线。适合语言学习背单词、考试备考和知识长期记忆巩固。无需注册纯前端计算。",
    
    "subnet-mask-calc": "免费在线子网掩码计算器，输入IP地址和CIDR前缀（如192.168.1.0/24）或子网掩码，一键计算网络地址、广播地址、可用IP范围、首个/末个可用IP和最大主机数量。支持IPv4全范围（/0至/32），结果含二进制/十进制双格式展示。适合网络工程师IP规划、CCNA/CCNP备考和IT运维日常管理。无需注册。",
    
    "military-time-converter": "免费在线军事时间格式转换工具，快速在24小时制和12小时制（AM/PM）之间互转。输入14:30即时转为2:30 PM，支持双向实时转换、显示当前系统时间和时区信息，批量输入多个时间一次性转换。适合国际航班时刻查阅、跨国远程会议时间协调和军事/医疗/物流等24小时制专业领域。无需注册一键复制。",
}

# 验证长度
for k, v in NEW_DESCRIPTIONS.items():
    l = len(v)
    status = "OK" if 140 <= l <= 160 else f"NEED FIX ({l})"
    print(f"[{status}] {k}: {l} chars")

# 修改文件
for dirname, new_desc in NEW_DESCRIPTIONS.items():
    path = os.path.join(dirname, "index.html")
    if not os.path.exists(path):
        print(f"SKIP (not found): {dirname}")
        continue
    
    content = open(path).read()
    
    # 跳过重定向页面
    if 'meta http-equiv="refresh"' in content:
        print(f"SKIP (redirect): {dirname}")
        continue
    
    changes = 0
    
    # 1. meta description
    old_meta = re.search(r'<meta name="description" content="([^"]+)"', content)
    if old_meta:
        old_full = old_meta.group(0)
        new_full = f'<meta name="description" content="{new_desc}"'
        if old_full != new_full:
            content = content.replace(old_full, new_full, 1)
            changes += 1
    
    # 2. og:description - 用截断版（保持简洁）
    if '<meta property="og:description" content="' in content:
        old_og = re.search(r'<meta property="og:description" content="([^"]+)"', content)
        if old_og:
            old_og_full = old_og.group(0)
            og_desc = new_desc[:200] if len(new_desc) > 200 else new_desc
            new_og_full = f'<meta property="og:description" content="{og_desc}"'
            if old_og_full != new_og_full:
                content = content.replace(old_og_full, new_og_full, 1)
                changes += 1
    
    # 3. Schema description
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
        print(f"  UPDATED ({changes} changes): {dirname}")
    else:
        print(f"  NO CHANGE: {dirname}")

print("\n=== ALL DONE ===")
