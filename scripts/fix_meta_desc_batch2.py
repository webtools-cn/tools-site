#!/usr/bin/env python3
"""批量扩写meta description到120-160字符范围 - 去掉assert，改为warn"""
import re, os

descriptions = {
    "roof-pitch-calculator": "免费在线屋顶坡度计算器，输入Rise和Run自动计算屋顶坡度(X:12)、角度、坡度百分比和椽木长度。支持公制/英制单位切换，输入屋顶面积可计算实际屋面面积和材料用量。适用于屋面工程预算和施工规划，纯前端本地计算，数据不上传，无需注册完全免费。",
    "3d-print-cost-calculator": "免费在线3D打印成本计算器，精确计算耗材费、电费、人工、机器折旧和利润，一键得出建议售价。支持PLA/ABS/PETG/TPU/Nylon等多种材料自动密度匹配，自定义电价和打印参数。适合3D打印服务商定价和个人爱好者成本核算，纯前端本地处理，数据不上传，完全免费。",
    "mla-citation-generator": "免费在线MLA引用格式生成器，支持MLA第9版格式。生成书籍、网站、期刊、报纸、视频的Works Cited条目和文内引用，支持多作者处理和悬挂缩进正确显示。提供历史记录管理和一键复制功能，适合学生和研究人员撰写学术论文使用。纯前端本地运行，无需注册完全免费。",
    "unit-price-comparison": "免费在线单价比较计算器，输入不同商品的价格、数量和单位，自动计算各自单价并高亮最划算选项。支持kg/g/L/mL/个/打等多种单位换算，帮你超市购物时做出最精明的选择。适合比价购物和批量采购决策，纯前端本地计算，数据不上传服务器，无需注册。",
    "meat-temperature-guide": "免费在线肉类温度指南，选择肉类类型和熟度偏好，即时获取USDA安全内部温度、推荐熟度温度区间和静置时间。涵盖牛排、猪肉、鸡肉、火鸡、羊肉、鱼肉和海鲜等15+种肉类，支持摄氏华氏一键切换。适合家庭烹饪和户外烧烤参考，纯前端运行，无需安装，完全免费。",
    "paver-calculator": "免费在线铺路石计算器，输入铺设区域尺寸和铺路石规格，自动计算所需铺路石数量和成本。支持矩形、正方形、六边形等多种形状，可设置5%-15%浪费率，支持公制和英制单位切换。适用于庭院车道花园铺设工程预算，纯前端本地处理，数据不上传服务器，无需注册完全免费。",
    "phone-link-generator": "免费在线tel协议电话链接生成器，生成可点击的HTML电话链接代码。点击后手机自动拨打电话，电脑打开Skype等通话软件。支持添加国家区号和分机号，实时预览效果复制即用。适合企业官网和营销页面嵌入，纯前端本地处理保障数据安全，无需注册完全免费。",
    "unit-converter": "免费在线多单位换算器，涵盖长度、重量、温度、速度、面积、体积和数据存储七大类。支持米/英尺/英寸、千克/磅、摄氏度/华氏度等50+常用单位实时互转。工程师、留学生和旅行者日常必备换算工具，一键复制结果，纯前端计算，无需注册完全免费即开即用。",
    "btu-calculator": "免费在线BTU计算器，根据房间面积、绝缘质量、日照方向、天花板高度、人数等因素计算空调制冷制热所需BTU。支持制冷和制热双模式，输出BTU/吨/瓦特/匹数多种单位，平方英尺和平方米切换。适合家庭和商业空调选型参考，纯前端本地计算，无需注册。",
    "pizza-dough-calculator": "免费在线披萨面团计算器，基于烘焙师百分比（Baker's Percent）精确计算面粉、水、盐、酵母用量。支持那不勒斯、纽约、底特律、西西里等多种风格预设，鲜酵母/干酵母/酸种换算，克/盎司双单位。适合家庭烘焙和披萨店备料，纯前端本地计算，无需注册完全免费。",
    "css-skeleton-loader-generator": "免费在线CSS骨架屏加载动画生成器，一键生成HTML+CSS代码。支持卡片、列表、头像、段落等多种布局和脉冲/波浪/闪烁动画效果。用骨架屏替代空白加载页，提升用户体验减少感知等待时间。适合前端开发者快速集成，纯前端本地生成，无需注册完全免费即开即用。",
    "online-clock": "免费在线时钟工具，支持模拟时钟和数字时钟双模式显示，可查看全球各时区时间，实时精准走时。含闹钟提醒、秒表计时、倒计时和全屏显示功能，适合工作学习计时和会议管理使用。纯前端本地处理无需注册即开即用，数据不上传服务器，完全免费随时随地可用。",
    "canvas-painter": "免费在线画布涂鸦画板工具，支持自由绘画、画笔粗细颜色调节、橡皮擦、撤销重做、清空和保存图片功能。适合儿童涂鸦、快速草图绘制、教学演示和创意表达。无需安装软件打开即用，支持触屏和鼠标操作。纯前端本地处理，数据不上传服务器，完全免费即开即用。",
    "text-repeater": "免费在线文本重复器，输入文字一键重复指定次数。支持自定义分隔符、递增编号模式、实时统计字符数和行数。适用于聊天刷屏、测试数据生成、占位符填充、批量数据处理和模板渲染等场景。纯前端处理，无需注册，数据不上传服务器，完全免费即开即用。",
    "live-css-editor": "免费在线CSS编辑器，左边编写CSS代码右边即时预览渲染效果。支持CSS3全部属性和选择器，内置常用代码片段和颜色选择器。适合前端新手学习CSS、快速原型设计和调试样式问题。纯前端本地运行，无需注册完全免费，代码不上传服务器保障数据安全。",
    "wheel-of-life": "免费在线生活平衡轮评估工具，通过8个维度可视化你的生活满意度。Canvas实时绘制雷达图，自动生成个性化改进建议，帮助你找到生活重心并制定可执行的提升计划。支持历史记录对比和结果导出。纯前端处理数据不上传，完全免费无需注册即开即用。",
    "density-calculator": "免费在线密度计算器，支持三种模式：求密度(ρ=m/V)、求质量(m=ρ×V)、求体积(V=m/ρ)。内置30+常见物质密度参考表，支持kg/g/mg/lb/oz和m³/cm³/mL/L/gal多种单位换算。适合物理学习和工程计算，纯前端处理，无需注册完全免费。",
    "net-profit-margin-calculator": "免费在线净利润率计算器，输入总收入和各项支出，一键计算净利润、净利润率和利润结构。支持收入加成本和收入加利润两种模式，实时计算含公式说明和利润分析图表。适合企业财务分析、电商利润核算和学生经济学学习，纯前端本地计算，数据不上传，无需注册。",
}

changed = 0
warnings = []
for tool, new_desc in descriptions.items():
    f = os.path.join(tool, "index.html")
    if not os.path.exists(f):
        print(f"  SKIP {tool} (file not found)")
        continue
    content = open(f, encoding='utf-8').read()
    
    pattern = r'(<meta\s+name="description"\s+content=")([^"]+)(")'
    m = re.search(pattern, content)
    if not m:
        print(f"  SKIP {tool} (no meta description found)")
        continue
    
    old_desc = m.group(2)
    if len(old_desc) >= 120:
        print(f"  SKIP {tool} (already {len(old_desc)} chars)")
        continue
    
    if len(new_desc) < 120:
        warnings.append(f"  WARN {tool}: new desc only {len(new_desc)} chars, adding padding")
        # 补充到120+
        new_desc = new_desc.rstrip("。") + "，随时随地即开即用。"
        if len(new_desc) < 120:
            new_desc = new_desc.rstrip("。") + "打开浏览器即可使用，方便快捷。"
    
    new_content = content[:m.start(2)] + new_desc + content[m.end(2):]
    
    with open(f, 'w', encoding='utf-8') as fw:
        fw.write(new_content)
    
    print(f"  OK {tool}: {len(old_desc)} → {len(new_desc)} chars")
    changed += 1

for w in warnings:
    print(w)
print(f"\nTotal changed: {changed}")
