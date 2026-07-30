#!/usr/bin/env python3
"""修复 meta description 中的 REPEAT_LOOP 问题 - 第二轮：扩展描述至140-160字符"""
import re, os

FIXES = {
    '401k-contribution': '免费在线401k退休供款计算器，输入年薪和供款比例，自动计算雇主匹配金额和年度总供款上限。支持传统401k和Roth 401k对比，帮你充分利用税收优惠实现退休储蓄最大化。',
    'bic-validator': '免费在线BIC/SWIFT代码验证器，快速检查银行识别代码格式是否有效。输入8位或11位BIC代码，自动识别银行名称、国家和分行信息。全球银行代码一键校验，无需注册。',
    'body-measurement': '免费在线身体测量计算器，综合评估BMI指数、腰臀比、理想体重、体表面积和BMR基础代谢率五大健康指标。输入身高、体重、腰围等数据，即时获取科学评估和健康建议。',
    'bold-text-generator': '免费在线粗体文字生成器，将普通文字转换为Unicode粗体、斜体、花体等9种装饰风格。适合社交媒体昵称、朋友圈文案和创意设计。输入文字即时转换，一键复制即用即走。',
    'bubble-text': '免费在线泡泡文字生成器，将普通文字转换为圆圈包围的装饰性文字，每字拥有独立泡泡风格边框。适合社交媒体个性签名和创意文字设计，一键复制泡泡风格文字。',
    'business-loan-calculator': '免费在线企业经营贷款计算器，支持等额本息和等额本金两种还款方式。输入贷款金额、利率和期限，自动计算月供、总利息和还款明细表。助力中小企业融资决策和现金流规划。',
    'chess-timer': '免费在线国际象棋计时器，支持自定义倒计时时间和每步加秒。双人轮流计时模式，到时自动声音提示。适合棋类比赛、日常对弈和训练使用。无需下载安装，即开即用。',
    'college-fund': '免费在线大学基金储蓄计算器，输入孩子当前年龄和预期大学费用，自动计算每月需存金额。支持529教育基金储蓄模拟，可视化展示复利增长效果，帮你提前规划子女大学教育费用。',
    'cooking-measurement': '免费在线烹饪计量换算器，支持杯、汤匙、茶匙、毫升、克、盎司等常用烘焙和烹饪单位快速换算。附带常用食材密度数据，精准换算面粉、糖、油等用量。厨房必备实用工具。',
    'cron-validator': '免费在线Cron表达式验证器，测试和解析定时任务表达式。支持5位和6位Cron格式，可视化显示未来10次执行时间。支持秒级cron和Quartz扩展。运维和开发者必备定时任务测试工具。',
    'css-ribbon-generator': '免费在线CSS角标生成器，可视化创建网页装饰角标样式。支持自定义文字内容、背景颜色、位置（左上/右上）和旋转角度。实时预览效果，一键复制纯CSS代码，无需图片。',
    'daily-horoscope': '免费在线每日星座运势查询，12星座今日运势、幸运色、幸运数字、爱情事业健康运程一应俱全。每日更新星座解读内容，纯前端本地运行无需注册，轻松了解今日星运指南。',
    'daily-joke': '免费在线每日笑话生成器，收录大量中英文笑话、段子和冷笑话。支持按分类浏览（程序员、动物、生活等），一键复制分享给朋友。纯前端本地运行无需注册，每天给你会心一笑。',
    'education-loan-calculator': '免费在线教育贷款计算器，支持等额本息和等额本金两种还款方式。包含在校期间宽限期利息计算，自动生成月供明细和总利息对比表。帮你科学规划助学贷款还款方案减轻毕业后压力。',
    'em-to-px': '免费在线EM转PX转换器，输入EM值和基准字号自动计算对应的像素值。支持EM→PX和PX→EM双向实时换算，前端开发响应式设计必备。无需注册，数据不上传服务器。',
    'expense-splitter': '免费在线账单分摊计算器，轻松和朋友分摊聚餐、旅行、合租等共同费用。支持平均分摊、按比例分配和自定义金额三种模式。输入总金额和参与人数，一键复制分摊明细结果。',
    'fitness-pace': '免费在线运动配速计算器，计算跑步、骑行和游泳的配速、速度和完成时间。支持公制和英制单位自由切换，附带卡路里消耗估算。运动训练和马拉松备赛的好帮手工具。',
    'flip-text': '免费在线文字翻转器，支持水平镜像翻转、上下倒置翻转和反向翻转三种模式。一键将文字变换为翻转效果，适合创意设计和趣味社交。无需注册，纯前端本地处理。',
    'gratuity-calculator': '免费在线离职金计算器，根据工龄年限和最后工资自动计算应得遣散费。支持各国劳动法规公式自定义调整，帮助你了解离职时应获得的法定经济补偿金额和退休金福利。',
    'gross-margin-calculator': '免费在线毛利率计算器，输入售价和成本自动计算毛利率和加价率。支持正向计算（已知成本求售价）和反向推导（已知售价求成本）。电商卖家、零售业和企业财务分析必备工具。',
}

count = 0
for d, new_desc in FIXES.items():
    path = f'{d}/index.html'
    if not os.path.exists(path):
        print(f'SKIP {d}: file not found')
        continue
    
    content = open(path, 'r').read()
    
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
    
    # 替换 schema description
    content = re.sub(
        r'"description"\s*:\s*"[^"]*"',
        f'"description": "{new_desc}"',
        content
    )
    
    open(path, 'w').write(content)
    count += 1
    print(f'FIXED {d}: {len(new_desc)} chars')

print(f'\nTotal fixed: {count}')