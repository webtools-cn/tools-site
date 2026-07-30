#!/usr/bin/env python3
"""修复剩余所有包含 REPEAT_LOOP 的位置：meta, og, twitter, schema, tool-description"""
import re, os

# 每个页面的新描述
FIXES = {
    'body-measurement': '免费在线身体测量计算器，综合评估BMI指数、腰臀比、理想体重、体表面积和BMR基础代谢率五大健康指标。输入身高、体重、腰围等数据，即时获取科学评估和健康建议。',
    'bubble-text': '免费在线泡泡文字生成器，将普通文字转换为圆圈包围的装饰性文字，每字拥有独立泡泡风格边框。适合社交媒体个性签名和创意文字设计，一键复制泡泡风格文字。',
    'business-loan-calculator': '免费在线企业经营贷款计算器，支持等额本息和等额本金两种还款方式。输入贷款金额、利率和期限，自动计算月供、总利息和还款明细表。助力中小企业融资决策和现金流规划。',
    'daily-horoscope': '免费在线每日星座运势查询，12星座今日运势、幸运色、幸运数字、爱情事业健康运程一应俱全。每日更新星座解读内容，纯前端本地运行无需注册，轻松了解今日星运指南。',
    'daily-joke': '免费在线每日笑话生成器，收录大量中英文笑话、段子和冷笑话。支持按分类浏览（程序员、动物、生活等），一键复制分享给朋友。纯前端本地运行无需注册，每天给你会心一笑。',
    'education-loan-calculator': '免费在线教育贷款计算器，支持等额本息和等额本金两种还款方式。包含在校期间宽限期利息计算，自动生成月供明细和总利息对比表。帮你科学规划助学贷款还款方案减轻毕业后压力。',
    'em-to-px': '免费在线EM转PX转换器，输入EM值和基准字号自动计算对应的像素值。支持EM→PX和PX→EM双向实时换算，前端开发响应式设计必备。无需注册，数据不上传服务器。',
    'expense-splitter': '免费在线账单分摊计算器，轻松和朋友分摊聚餐、旅行、合租等共同费用。支持平均分摊、按比例分配和自定义金额三种模式。输入总金额和参与人数，一键复制分摊明细结果。',
    'flip-text': '免费在线文字翻转器，支持水平镜像翻转、上下倒置翻转和反向翻转三种模式。一键将文字变换为翻转效果，适合创意设计和趣味社交。无需注册，纯前端本地处理。',
    'gratuity-calculator': '免费在线离职金计算器，根据工龄年限和最后工资自动计算应得遣散费。支持各国劳动法规公式自定义调整，帮助你了解离职时应获得的法定经济补偿金额和退休金福利。',
    'home-loan-calculator': '免费在线住房贷款计算器，支持等额本息和等额本金两种还款方式。输入房价、首付、利率和贷款年限，自动计算月供、总利息和还款明细表。帮你对比不同贷款方案做出最优选择。',
    'hra-calculator': '免费在线HRA房屋租金补贴计算器，输入基本工资和城市类型自动计算免税租金补贴额度。支持地铁城市和非地铁城市不同费率，帮你合理规划薪资结构最大化节税效果。',
    'image-resize-bulk': '免费在线图片批量调整大小工具，支持同时处理多张图片。可自定义宽高、保持比例或固定尺寸，纯浏览器端处理无需上传服务器。一键批量缩放并打包下载，保护隐私安全。',
    'internal-rate-of-return': '免费在线内部收益率(IRR)计算器，输入现金流序列自动计算投资项目的内部收益率。支持不规则现金流输入，帮你评估项目投资回报水平做出明智投资决策。纯前端计算。',
    'lumpsum-vs-sip-calculator': '免费在线一次性投资vs定投对比计算器，输入本金、月投金额、预期收益率和投资年限，自动计算两种策略的最终收益差异。帮你选择最适合的投资方式实现财富增值。',
    'market-cap-calculator': '免费在线市值计算器，输入股价和流通股数自动计算公司总市值。支持多种货币单位，帮投资者快速评估上市公司规模。无需注册，纯前端本地计算。',
    'meal-planner': '免费在线餐食计划生成器，根据热量目标、饮食偏好和餐次数量自动生成一周膳食计划。支持增肌、减脂和均衡三种模式，帮你科学规划每日饮食营养搭配。',
    'meme-text-generator': '免费在线梗图文字生成器，快速生成网络热梗风格的文字图片。支持多种字体样式和颜色，一键下载或分享到社交平台。无需注册，纯前端处理。',
    'pixel-to-em': '免费在线PX转EM转换器，输入像素值和基准字号自动计算对应的EM值。支持PX→EM和EM→PX双向实时换算，前端开发和响应式设计必备工具。无需注册。',
    'post-office-calculator': '免费在线邮政储蓄收益计算器，支持定期存款、小额储蓄和月收入计划等多种产品。计算复利收益和到期本息合计，帮你对比不同存款方案的最终回报。',
    'python-formatter': '免费在线Python代码格式化工具，自动调整缩进、规范空格、对齐括号、移除多余空行。支持PEP 8规范检查，纯前端处理代码不上传服务器，开发者日常必备工具。',
    'roas-calculator': '免费在线广告支出回报率(ROAS)计算器，输入广告花费和广告收入自动计算ROAS。支持ROAS与ROI对比分析，帮电商和营销人员评估广告投放效果优化预算分配。',
    'roman-numerals': '免费在线罗马数字转换器，支持数字转罗马数字和罗马数字转数字双向转换。支持1-3999范围，一键复制结果。无需注册，即用即走。',
    'smart-rename': '免费在线智能文件重命名工具，支持查找替换、添加前缀后缀、插入序号和正则表达式批量重命名。实时预览重命名效果，无需注册数据不上传服务器。',
    'yes-no': '免费在线决策工具，提供魔法8球、命运转盘和抛硬币三种随机决策方式。帮你快速做选择，告别纠结和选择困难症。纯前端本地运行无需注册，仅供娱乐。',
}

count = 0
for d, new_desc in FIXES.items():
    path = f'{d}/index.html'
    if not os.path.exists(path):
        print(f'SKIP {d}: file not found')
        continue
    
    content = open(path, 'r').read()
    original = content
    
    # 替换 meta description
    content = re.sub(
        r'<meta name="description" content="[^"]+"',
        f'<meta name="description" content="{new_desc}"',
        content
    )
    
    # 替换 og:description
    content = re.sub(
        r'<meta property="og:description" content="[^"]+"',
        f'<meta property="og:description" content="{new_desc}"',
        content
    )
    
    # 替换 twitter:description（如果存在）
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]+"',
        f'<meta name="twitter:description" content="{new_desc}"',
        content
    )
    
    # 替换 schema description
    content = re.sub(
        r'"description"\s*:\s*"[^"]*"',
        f'"description": "{new_desc}"',
        content
    )
    
    # 替换 .tool-description 中的重复部分（用re.sub替换整个p标签内容）
    content = re.sub(
        r'<p class="tool-description"[^>]*>.*?</p>',
        f'<p class="tool-description" style="color:#6b7280;font-size:0.95rem;line-height:1.6;margin:0.5rem 0 1rem;">{new_desc}</p>',
        content
    )
    
    if content != original:
        open(path, 'w').write(content)
        count += 1
        print(f'FIXED {d}: {len(new_desc)} chars')
    else:
        print(f'UNCHANGED {d}')

print(f'\nTotal fixed: {count}')