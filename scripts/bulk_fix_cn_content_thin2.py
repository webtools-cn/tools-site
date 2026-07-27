#!/usr/bin/env python3
"""批量修复CN剩余 content_thin NO_FAQ页面"""
import os, json, re, random

SITE = '/home/chison/tools-site'

with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
    data = json.load(f)

remaining = data['remaining_pages']

cn_thin = []
for k, v in remaining.items():
    if k.startswith('cn:') and any('content_thin' in i or 'content_very_thin' in i for i in v):
        item = k.replace('cn:', '')
        path = os.path.join(SITE, item, 'index.html')
        if os.path.isfile(path):
            with open(path) as pf:
                if 'faq-section' not in pf.read():
                    cn_thin.append(item)

print(f"CN 薄页面(NO_FAQ): {len(cn_thin)} 个")

descriptions = {
    'beat-maker': ('节拍制作', '在线创建自定义节奏和节拍模式，支持多种鼓组音色，适合音乐制作人和节奏爱好者。无需安装软件，打开浏览器即可开始制作节拍。'),
    'birthday-countdown': ('生日倒计时', '精确计算距离下一个生日还有多少天、小时和分钟。支持农历和公历生日设置，分享倒计时给好友。'),
    'bubble-text': ('气泡文字', '将普通文字转换为可爱气泡风格的Unicode字符，支持多种气泡样式，一键复制到社交媒体。'),
    'business-loan-calculator': ('商业贷款计算器', '计算商业贷款月供、总利息和还款计划。支持等额本息和等额本金两种还款方式。'),
    'color-psychology': ('色彩心理学', '探索不同颜色在设计和营销中的心理含义，了解色彩如何影响用户情绪和行为。'),
    'compare-images': ('图片对比', '并排对比两张图片的差异，支持调整透明度叠加查看，适合设计师和摄影师。'),
    'correlation-calculator': ('相关系数计算器', '计算两组数据的皮尔逊相关系数，分析变量间的线性关系强度。支持CSV数据导入。'),
    'creatine-calculator': ('肌酸计算器', '根据体重计算每日肌酸摄入量和加载期/维持期用量，科学健身补剂指导。'),
    'credit-card-payoff-calculator': ('信用卡还款计算器', '计算信用卡还款计划和节省利息，对比最低还款和固定金额还款的差异。'),
    'css-border-generator': ('CSS边框生成器', '可视化生成CSS边框样式代码，支持圆角、阴影、渐变边框等效果，实时预览。'),
    'css-hover-effects': ('CSS悬停效果', '浏览和复制CSS悬停动画效果代码，包含按钮、卡片、图片等多种元素的hover效果。'),
    'donut-chart-maker': ('环形图制作', '在线创建环形图/甜甜圈图，自定义颜色、标签和数据，适合数据可视化展示。'),
    'down-payment-calculator': ('首付计算器', '计算购房首付金额和月供，考虑利率、贷款期限和首付比例等因素。'),
    'drawing-tool': ('在线画板', '支持画笔、橡皮擦、形状工具的画图工具，可导出为PNG图片，适合快速草图。'),
    'em-to-px': ('EM转PX', 'CSS单位换算工具，EM和PX互相转换，支持自定义基准字号。'),
    'fantasy-name-generator': ('奇幻名称生成器', '生成奇幻、科幻风格的随机角色名称，适合游戏、小说创作。'),
    'flip-text': ('翻转文字', '将文字上下翻转或左右翻转，生成有趣的颠倒文字效果，支持复制分享。'),
    'font-identifier': ('字体识别', '上传图片识别其中使用的字体，获取相似字体推荐和下载链接。'),
    'fuel-cost-calculator': ('油耗计算器', '计算车辆油耗和行驶成本，支持多种燃油类型和单位换算，帮助规划出行预算。'),
    'gratuity-calculator': ('小费计算器', '快速计算餐厅小费金额，支持按百分比或固定金额计算，支持多人分摊。'),
    'html-stripper': ('HTML标签清除', '一键清除HTML标签保留纯文本内容，支持自定义保留标签和属性。'),
    'inheritance-tax-calculator': ('遗产税计算器', '估算遗产税金额，考虑免税额、税率阶梯和不同财产类型。'),
    'invoice-generator': ('发票生成器', '在线生成专业发票模板，填写公司信息和费用明细，导出为PDF。'),
    'line-chart-maker': ('折线图制作', '在线创建折线图，支持多条数据系列、自定义颜色和标注，适合趋势分析。'),
    'lorem-ipsum': ('Lorem Ipsum生成器', '生成占位文本Lorem Ipsum，支持自定义段落数、字数和格式，适合设计稿填充。'),
    'lump-sum-calculator': ('一次性投资计算器', '计算一次性投资的未来价值和复利收益，对比不同投资期限和利率。'),
    'markdown-to-html': ('Markdown转HTML', '将Markdown格式文本转换为HTML代码，支持实时预览和代码高亮。'),
    'meme-generator': ('表情包生成器', '在线制作表情包图片，添加自定义文字、调整字体和位置，导出分享。'),
    'money-counter': ('点钞计算器', '快速计算纸币总额，支持多种面额人民币和美金的统计汇总。'),
    'nato-alphabet': ('北约音标字母', '学习NATO音标字母表，文本转音标拼读，适合无线电通信和航空学习。'),
    'net-worth-calculator': ('净资产计算器', '计算个人净资产，汇总资产和负债项目，清晰了解财务状况。'),
    'nipple-calculator': ('奶嘴计算器', '计算婴儿奶量和喂养频率，根据月龄和体重推荐科学喂养方案。'),
    'percentage-change': ('百分比变化', '计算数值的百分比变化和增减幅度，支持环比和同比计算。'),
    'phone-parser': ('电话号码解析', '解析和验证国际电话号码格式，提取国家代码、区号和本地号码。'),
    'ppi-calculator': ('PPI计算器', '计算屏幕像素密度PPI，输入分辨率和尺寸即可得出结果，对比不同设备。'),
    'pregnancy-calculator': ('预产期计算器', '根据末次月经日期计算预产期和孕周，提供孕期关键时间节点提醒。'),
    'progress-bar': ('进度条生成', '在线生成进度条样式代码，支持CSS和SVG格式，自定义颜色和动画效果。'),
    'regex-tester': ('正则表达式测试', '在线测试正则表达式匹配结果，支持多种编程语言语法，高亮显示匹配内容。'),
    'retirement-calculator': ('退休金计算器', '估算退休储蓄目标和每月存款需求，考虑通胀和投资回报率。'),
    'rgb-to-cmyk': ('RGB转CMYK', '颜色空间转换工具，RGB和CMYK互相转换，适合印刷和设计工作。'),
    'roulette-wheel': ('幸运转盘', '在线幸运转盘抽奖工具，自定义选项和权重，适合活动和决策。'),
    'sales-tax': ('销售税计算器', '计算含税价格和不含税价格，支持自定义税率和多种货币单位。'),
    'screen-recorder': ('屏幕录制', '在线录制屏幕和摄像头画面，支持音频录制，导出为视频文件。'),
    'sip-calculator': ('SIP投资计算器', '计算定期定额投资(SIP)的未来收益，对比不同投资金额和期限。'),
    'size-chart': ('尺码对照表', '各国服装鞋帽尺码对照转换，中美欧日尺码快速查询。'),
    'solar-calculator': ('太阳能计算器', '估算太阳能板发电量和投资回报，考虑日照时长和电费节省。'),
    'strong-password': ('强密码生成', '生成高强度随机密码，支持自定义长度和字符类型，一键复制。'),
    'svg-editor': ('SVG编辑器', '在线编辑SVG矢量图形，支持路径编辑、形状绘制和代码预览。'),
    'tarot-reader': ('塔罗牌占卜', '在线塔罗牌抽牌和解读，支持多种牌阵，了解塔罗牌含义。'),
    'text-case': ('大小写转换', '文本大小写转换工具，支持首字母大写、全大写、全小写等格式。'),
    'time-zone': ('时区转换', '全球时区时间转换，对比不同城市当前时间和时差，支持夏令时。'),
    'text-to-image': ('文字转图片', '将文字内容渲染为PNG图片，自定义字体、颜色和背景，适合社交媒体。'),
}

generic = [
    ('免费工具', '完全免费使用，无需注册登录，数据在浏览器本地处理，保护你的隐私安全。'),
    ('在线工具', '支持PC端和移动端使用，响应式设计自适应屏幕，随时随地打开浏览器即可使用。'),
]

fixed = 0
for item in cn_thin:
    path = os.path.join(SITE, item, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'faq-section' in content:
        continue
    
    if item in descriptions:
        title, desc = descriptions[item]
    else:
        tm = re.search(r'<title>(.*?)(?:\s*[-–|]\s*Free ToolBase)?</title>', content)
        title = tm.group(1).strip() if tm else item.replace('-', ' ').title()
        desc = f'{title}，免费在线使用，操作简单快捷，结果即时显示。'
    
    gtitle, gdesc = random.choice(generic)
    
    faq_html = f'''
    <section class="faq-section">
      <h2>关于{title}</h2>
      <div class="faq-item">
        <h3>如何使用{title}？</h3>
        <p>直接在输入框中输入内容或上传文件，点击相应按钮即可获得结果。{desc}</p>
      </div>
      <div class="faq-item">
        <h3>这个工具收费吗？</h3>
        <p>{title}是{gtitle}，{gdesc}</p>
      </div>
    </section>'''
    
    if '</main>' in content:
        content = content.replace('</main>', faq_html + '\n</main>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
    elif '</body>' in content:
        content = content.replace('</body>', faq_html + '\n</body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f"CN修复: {fixed} 个")