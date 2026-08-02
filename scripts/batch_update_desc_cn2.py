#!/usr/bin/env python3
"""Fix descriptions that are still <100 chars after first pass."""
import re, os

# These are the ones that need more content
updates = [
    # chi-square-calculator: 96→~145
    ("chi-square-calculator",
     '<meta name="description" content="免费在线卡方检验计算器，输入观察值与期望值，一键计算卡方统计量、自由度和P值。支持2×2和R×C列联表分析，适用于学术研究、数据科学和统计分析。纯前端计算，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线卡方检验计算器，输入观察值与期望值，一键计算卡方统计量、自由度和P值。支持2×2和R×C列联表分析，适用于学术研究、数据科学、AB测试和统计分析。可进行独立性检验和拟合优度检验，纯前端计算，数据不上传服务器，无需注册完全免费。">'),

    # food-calorie-calculator: 99→~145
    ("food-calorie-calculator",
     '<meta name="description" content="免费在线食物热量计算器，覆盖主食、肉类、蔬果、零食、饮品等12大类数百种常见食物。点击即可添加并自动累计全天总热量，适合减脂健身、糖尿病饮食控制和日常营养管理。纯前端即开即用，数据安全不上传服务器。">',
     '<meta name="description" content="免费在线食物热量计算器，覆盖主食、肉类、蔬果、零食、饮品等12大类数百种常见食物。点击即可添加并自动累计全天总热量，适合减脂健身、糖尿病饮食控制和日常营养管理。支持中英文食物名称搜索，纯前端即开即用，数据安全不上传服务器。">'),

    # fractal-explorer: 96→~145
    ("fractal-explorer",
     '<meta name="description" content="免费在线分形探索器，实时渲染曼德勃罗集和茱莉亚集，支持无限缩放和拖拽探索分形细节。自定义迭代深度和颜色主题，生成惊艳的分形艺术作品。纯前端Canvas渲染，数据不上传服务器，无需注册完全免费。">',
     '<meta name="description" content="免费在线分形探索器，实时渲染曼德勃罗集和茱莉亚集，支持无限缩放和拖拽探索分形细节。自定义迭代深度、颜色主题和渲染精度，生成惊艳的分形艺术作品。适合数学可视化教学和数字艺术创作，纯前端Canvas渲染，数据不上传服务器，无需注册完全免费。">'),

    # days-between-dates: 96→~145
    ("days-between-dates",
     '<meta name="description" content="免费在线日期计算器，快速计算两个日期之间相差天数，或N天前后的具体日期。支持自然日和工作日模式切换，适用于项目排期、合同到期提醒、宝宝年龄计算和节日倒计时。纯浏览器本地运行，无需注册完全免费。">',
     '<meta name="description" content="免费在线日期计算器，快速计算两个日期之间相差天数，或N天前后的具体日期。支持自然日和工作日模式灵活切换，可自定义排除周末和节假日。适用于项目排期、合同到期提醒、宝宝年龄计算和节日倒计时。纯浏览器本地运行，无需注册完全免费。">'),

    # gcf-calculator: 95→~145
    ("gcf-calculator",
     '<meta name="description" content="免费在线最大公因数(GCF)和最小公倍数(LCM)计算器，支持逗号分隔批量输入多个数值，欧几里得算法精确计算。适用于数学学习、分数化简和算法教学。所有计算在浏览器本地执行，无需注册完全免费。">',
     '<meta name="description" content="免费在线最大公因数(GCF)和最小公倍数(LCM)计算器，支持逗号分隔批量输入多个数值，基于欧几里得算法精确计算。同时显示质因数分解结果和计算步骤。适用于数学学习、分数化简和算法教学。所有计算在浏览器本地执行，无需注册完全免费。">'),

    # decimal-to-fraction: 90→~145
    ("decimal-to-fraction",
     '<meta name="description" content="免费在线小数转分数计算器，将任意小数精确转换为最简分数形式。支持有限小数和无限循环小数转换、带分数显示和大数精度计算。适合学生数学学习、教师备课和工程师数值处理，无需注册即开即用。">',
     '<meta name="description" content="免费在线小数转分数计算器，将任意小数精确转换为最简分数形式。支持有限小数和无限循环小数转换、带分数显示和大数高精度计算。输入如0.375即得3/8，输入0.333循环即得1/3。适合学生数学学习、教师备课和工程师数值处理，无需注册即开即用。">'),

    # commission-calculator: 93→~145
    ("commission-calculator",
     '<meta name="description" content="免费在线佣金计算器，支持按比例提成和阶梯式提成两种模式。输入销售额和提成比例，自动计算佣金收入，可选加固定底薪。销售人员和自由职业者核算收入的必备工具，纯前端本地计算，无需注册完全免费。">',
     '<meta name="description" content="免费在线佣金计算器，支持按比例提成和阶梯式提成两种模式。输入销售额和提成比例，自动计算佣金收入，可选加固定底薪计算总收入。适合销售人员和自由职业者核算提成收入、房产中介计算佣金和电商运营分析利润。纯前端本地计算，无需注册完全免费。">'),

    # confidence-interval-calculator: 96→~145
    ("confidence-interval-calculator",
     '<meta name="description" content="免费在线置信区间计算器，输入样本均值、标准差和样本量，快速计算95%和99%置信区间。适用于AB测试数据分析、学术研究和统计推断。通过z分布或t分布精确计算，纯前端本地运行，无需注册完全免费。">',
     '<meta name="description" content="免费在线置信区间计算器，输入样本均值、标准差和样本量，快速计算95%和99%置信区间。支持z分布和t分布两种计算方法，适用于AB测试数据分析、学术论文研究和统计推断。实时显示区间上下限和标准误差，纯前端本地运行，无需注册完全免费。">'),

    # name-generator: 97→~145
    ("name-generator",
     '<meta name="description" content="免费在线名字生成器，支持生成中文名、英文名、奇幻角色名和笔名等多种类型。可指定性别风格和批量生成数量。适合小说角色命名、游戏ID创建、测试数据生成和取笔名灵感，纯前端本地生成，无需注册完全免费。">',
     '<meta name="description" content="免费在线名字生成器，支持生成中文名、英文名、日文名、奇幻角色名和笔名等多种类型。可指定性别风格和批量生成数量（1-50个）。适合小说角色命名、游戏ID创建、测试数据生成和取笔名寻找灵感，纯前端本地生成，无需注册完全免费。">'),

    # unit-price-comparison: 99→~145
    ("unit-price-comparison",
     '<meta name="description" content="免费在线单价对比计算器，输入不同商品的规格和价格，自动计算每单位（元/克、元/毫升）的真实成本。帮助消费者在超市购物时做出最优选择，避免大包装陷阱。支持多商品同时对比，纯前端计算，无需注册完全免费。">',
     '<meta name="description" content="免费在线单价对比计算器，输入不同商品的规格和价格，自动计算每单位（元/克、元/毫升）的真实成本。帮助消费者在超市购物时识别最优选择，避免大包装不一定便宜的陷阱。支持多商品同时对比，纯前端计算，无需注册完全免费。">'),

    # screenshot-tool: 93→~145
    ("screenshot-tool",
     '<meta name="description" content="免费在线网页截图工具，输入URL即可截取网页全屏或指定区域截图，导出PNG高清图片。适用于网页设计验收、竞品分析和内容存档。支持自定义视口尺寸模拟不同设备。纯前端处理，无需注册完全免费。">',
     '<meta name="description" content="免费在线网页截图工具，输入URL即可截取网页全屏或指定区域截图，一键导出PNG高清图片。支持自定义视口尺寸模拟手机、平板和桌面设备。适用于网页设计验收、竞品分析和内容存档。纯前端处理，无需注册完全免费。">'),
]

count = 0
for slug, old, new in updates:
    path = f"{slug}/index.html"
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}")
        continue
    
    with open(path) as f:
        content = f.read()
    
    if old not in content:
        print(f"SKIP (old not found): {path}")
        continue
    
    new_content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(new_content)
    
    # Verify
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', new_content)
    if m:
        print(f"OK: {path} ({len(m.group(1))} chars)")
    count += 1

print(f"\nTotal re-updated: {count}")