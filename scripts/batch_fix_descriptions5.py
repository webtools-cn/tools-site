#!/usr/bin/env python3
"""Batch fix descriptions batch 3 - 15 more pages with 130-160 char target."""
import re
from pathlib import Path

fixes = [
    ("cv-maker/index.html",
     "免费在线简历制作工具，填写个人信息、工作经历和教育背景即可快速生成专业简历。支持三种精美模板，一键导出PDF格式直接投递。求职者准备应聘材料和更新个人履历的实用工具，所有数据本地处理不上传服务器，无需注册完全免费。"),

    ("time-ago-calculator/index.html",
     "免费在线时间差计算器，计算两个日期之间相差多少天/小时/分钟，也支持计算某个日期距今多久。输入日期区间自动计算精确差值，适合项目工期管理、倒计时和纪念日计算等场景。纯前端处理数据不上传服务器，无需注册即可免费使用。"),

    ("freelancer-rate-calculator/index.html",
     "免费在线自由职业者费率计算器，帮你确定合理的时薪或日薪。考虑税费、保险、休假和运营成本等因素，从期望年收入反推实际费率。自由职业者接单定价和薪资谈判的必备工具，纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("email-signature-generator/index.html",
     "免费在线邮件签名生成器，支持自定义姓名、职位、公司、联系方式、社交链接和品牌颜色。一键生成HTML邮件签名，兼容Gmail、Outlook等主流邮件客户端。提升商务邮件专业度和品牌形象，纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("invoice-template/index.html",
     "免费在线发票模板生成器，快速创建专业发票文档。自定义公司信息、客户信息、项目明细和金额，一键导出PDF或直接打印。自由职业者和小微企业开具发票的必备工具，纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("cholesterol-ratio-calculator/index.html",
     "免费在线胆固醇比率计算器，计算总胆固醇/HDL、LDL/HDL和甘油三酯/HDL比率，科学评估心血管疾病风险。支持mg/dL和mmol/L两种单位切换。总胆固醇/HDL理想值<3.5，LDL/HDL<2.5，纯前端处理无需注册完全免费。"),

    ("business-days-calculator/index.html",
     "免费在线工作日计算器，快速计算两个日期之间的工作日天数，自动排除周末和法定节假日。支持添加或减去N个工作日、自定义节假日设定。适合项目管理排期、合同截止日期计算和人力资源考勤统计，纯前端处理无需注册完全免费。"),

    ("fuel-economy-calculator/index.html",
     "免费在线油耗计算器，计算百公里油耗、每公里油费和年燃油成本。支持L/100km、MPG、km/L等多种单位切换，可对比不同车型的燃油经济性。帮助车主管理日常用车成本，纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("muscle-recovery-calculator/index.html",
     "免费在线肌肉恢复时间计算器，根据训练强度、年龄和睡眠质量科学估算肌肉群恢复所需时间。帮助健身爱好者合理安排下次训练日期，避免过度训练导致肌肉损伤。支持初级/中级/高级三种训练水平，纯前端处理无需注册完全免费。"),

    ("terms-of-service-generator/index.html",
     "免费在线服务条款生成器，选择网站或App类型填写基本信息，一键生成专业的服务条款和使用协议文档。适用于网站、App、SaaS等在线业务场景，帮助创业者和小企业快速建立法律合规基础。纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("stock-options-calculator/index.html",
     "免费在线股票期权收益计算器，计算看涨期权和看跌期权的盈亏平衡点、最大利润、最大亏损和回报率。输入行权价、权利金和合约数，可视化不同到期价格下的盈亏情况。帮助投资者评估期权策略，纯前端处理无需注册完全免费。"),

    ("step-goal-calculator/index.html",
     "免费在线每日步数目标计算器，根据年龄、体重和运动目标科学计算每日推荐步数。支持久坐、轻度、中度和高强度四种活动水平，帮助制定个性化步行计划。科学设定走路目标轻松达成健康生活，纯前端处理无需注册完全免费。"),

    ("value-comparison-calculator/index.html",
     "免费在线性价比比较计算器，输入不同产品的价格和规格自动计算每单位价格，找出最划算的选择。支持多种商品类型对比，无论是超市购物比价还是大宗采购决策都能帮你做出明智选择。纯前端运算数据不上传服务器，无需注册完全免费。"),

    ("random-sentence-generator/index.html",
     "免费在线随机句子生成器，一键生成英文句子。支持调整句子长度（短/中/长），按句型筛选（陈述句/疑问句/感叹句）。适合英语教学、写作练习、Lorem Ipsum替代和创意启发等场景。纯前端处理数据不上传服务器，无需注册完全免费。"),

    ("currency-weight-calculator/index.html",
     "免费在线货币重量计算器，根据面额和张数或枚数计算纸币和硬币的总重量和总价值。支持人民币、美元、欧元、日元、英镑等多种货币。适合银行柜台、出纳和现金管理场景使用，纯前端处理数据不上传服务器，无需注册完全免费。"),
]

root = Path('.')
for rel_path, new_desc in fixes:
    filepath = root / rel_path
    if not filepath.exists():
        print(f"MISSING: {rel_path}")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    pattern = r'(<meta\s+name=[\"\']description[\"\']\s+)content=\"[^\"]*\"'
    content = re.sub(pattern, lambda m: m.group(1) + f'content="{new_desc}"', content)
    filepath.write_text(content, encoding='utf-8')
    
    # Verify
    new_content = filepath.read_text(encoding='utf-8')
    m = re.search(r'<meta\s+name=[\"\']description[\"\']\s+content=\"([^\"]+)\"', new_content)
    new_len = len(m.group(1)) if m else 0
    status = "OK" if 130 <= new_len <= 160 else ("SHORT" if new_len < 130 else "LONG")
    print(f"{status:5s} | {new_len:3d} chars | {rel_path}")

print("\nDone!")