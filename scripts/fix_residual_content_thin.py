#!/usr/bin/env python3
"""修复10个content_thin/very_thin残留 - 在body中添加丰富文字区域"""
import json, re, os

BASE = '/home/chison/tools-site'
with open(f'{BASE}/quality/quality_loop_result.json') as f:
    result = json.load(f)

pages = result['remaining_pages']

# 每个工具的内容增强文本
content_map = {
    'cn:401k-contribution': '''
<div class="section" id="infoSection">
<h2>🏦 关于401k退休储蓄</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是401k计划？</b> 401k是美国最主流的退休储蓄计划，由雇主提供，员工可从税前工资中直接供款。2024年个人供款上限为$23,000（50岁以上可追加$7,500）。</p>
<p><b>雇主匹配（Employer Match）：</b> 多数雇主会按比例匹配员工供款，常见方案为50%匹配前6%工资。这是"免费的钱"，强烈建议至少供满匹配上限。</p>
<p><b>传统 vs ROTH：</b> 传统401k用税前收入供款，提取时交税；ROTH 401k用税后收入供款，提取时免税。选择哪种取决于您当前税率与预期退休税率的比较。</p>
<p><b>复利的力量：</b> 早开始是关键。30岁开始每月存$500，按7%年化收益，60岁时可达$61万+。晚10年开始将减少近一半。</p>
<p><b>建议策略：</b> ①至少供满雇主匹配部分；②每年提高供款比例1-2%；③利用年度加薪增加供款；④不要提前支取以避免罚款。</p>
</div>
</div>''',

    'cn:529-contribution-calculator': '''
<div class="section" id="infoSection">
<h2>🎓 关于529教育储蓄计划</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是529计划？</b> 529计划是美国州政府提供的教育储蓄工具，投资收益和合格教育支取均免税。可用于大学学费、K-12学费、学生贷款还款等。</p>
<p><b>税收优势：</b> 存入529计划的资金在账户内增长免税，用于合格教育费用支取也免税。许多州还为供款提供州税抵免。</p>
<p><b>教育成本趋势：</b> 过去20年美国大学学费年均增长约5-7%，远超通胀。一个今天出生的孩子，18年后四年公立大学费用预计约$150,000，私立大学超过$350,000。</p>
<p><b>供款建议：</b> 越早开始越好。即使是每月小额供款，通过复利效应也能积累可观余额。可以考虑用生日、节日红包增加供款。</p>
<p><b>注意事项：</b> 非教育用途支取需缴纳所得税和10%罚款。如果孩子获得奖学金，可取回等额资金免罚款。</p>
</div>
</div>''',

    'cn:college-fund': '''
<div class="section" id="infoSection">
<h2>🎓 大学储蓄规划指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>大学费用构成：</b> 包括学费、住宿费、书本费、生活费等。四年制公立大学州内学生年均总费用约$25,000-35,000，私立大学约$55,000-80,000。</p>
<p><b>储蓄工具选择：</b> 529计划（教育储蓄专用，双免税）、Coverdell ESA（年供款上限$2,000）、UGMA/UTMA托管账户、ROTH IRA（可用于教育支出免罚）等。</p>
<p><b>目标设定：</b> 一般建议储蓄目标为预期总费用的50-70%，其余通过奖学金、助学金、学生贷款和勤工俭学补充。不要试图100%覆盖——适度贷款也有教育意义。</p>
<p><b>时间规划：</b> 如果孩子现在N岁，距大学还有(18-N)年。例如现在8岁，有10年时间。每月存$300，按6%年化，10年后约$49,000。</p>
<p><b>奖学金策略：</b> 除了储蓄，鼓励孩子参与体育、艺术、社区服务等活动提升奖学金竞争力。每年有数十亿美元奖学金无人申请。</p>
</div>
</div>''',

    'cn:cooking-measurement': '''
<div class="section" id="infoSection">
<h2>🍳 烹饪计量换算完全指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>为什么烹饪换算很重要？</b> 不同国家使用不同的计量系统——美国用杯和盎司，欧洲和亚洲用克和毫升。错误的换算可能导致烘焙失败或菜肴味道失衡，尤其是对精度敏感的烘焙。</p>
<p><b>体积 vs 重量：</b> 专业厨师和烘焙师更推荐使用重量（克）而非体积（杯），因为重量不受食材压实程度、湿度影响。1杯筛过的面粉和1杯压紧的面粉可能相差30%！</p>
<p><b>常见换算速查：</b> 1杯=16汤匙=48茶匙≈240毫升 | 1汤匙=3茶匙≈15毫升 | 1盎司≈28.35克 | 1磅≈453.6克 | 1升≈4.23杯</p>
<p><b>食材密度差异：</b> 1杯不同食材的重量差异巨大：面粉≈120g，糖≈200g，黄油≈227g，蜂蜜≈340g。这就是为什么精确换算必须考虑食材类型。</p>
<p><b>温度换算：</b> 华氏转摄氏：°C=(°F-32)×5/9。常见温度：325°F≈163°C（慢烤），350°F≈177°C（常规烘焙），400°F≈204°C（高温烤制）。</p>
</div>
</div>''',

    'cn:credit-score-estimator': '''
<div class="section" id="infoSection">
<h2>📊 信用评分完全指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是信用评分？</b> 信用评分是衡量个人信用风险的数字化指标，范围通常300-850。FICO评分是最常用的模型，被90%以上的贷款机构使用。好分数意味着更低的贷款利率和更高的获批率。</p>
<p><b>评分构成：</b> 还款历史（35%）- 最重要，一次逾期可降100+分；信用使用率（30%）- 建议保持<30%；信用历史长度（15%）- 越长越好；新信用查询（10%）- 短期内多次申请会降分；信用类型（10%）- 多样化更佳。</p>
<p><b>各分数段解读：</b> 800+ 卓越 - 获得最优利率；740-799 非常好 - 高于平均水平；670-739 良好 - 多数贷款人可接受；580-669 一般 - 可能被视为次级借款人；<580 较差 - 贷款困难。</p>
<p><b>提升建议：</b> ①按时还款是最高优先级；②降低信用卡使用率到30%以下；③不要关闭旧信用卡（信用历史越长越好）；④避免短期内开多张新卡。</p>
<p><b>免费查询：</b> 每年可通过AnnualCreditReport.com免费获取三大征信机构报告。许多银行和信用卡App也提供免费分数查看。</p>
</div>
</div>''',

    'cn:currency-exchange-fee-calculator': '''
<div class="section" id="infoSection">
<h2>💱 货币兑换费用完全指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>兑换费用构成：</b> 国际交易通常包含三部分费用：银行/信用卡公司外汇手续费（通常1-3%）、中间市场汇率差价（银行加价0.5-2%）、以及可能的固定手续费。总费用可能高达交易金额的3-5%。</p>
<p><b>省钱策略：</b> ①使用免外汇手续费的信用卡（如Chase Sapphire、Capital One等）；②避免在机场和酒店兑换（汇率最差）；③使用Wise/Revolut等专业汇款服务而非传统银行电汇；④大额兑换时比较多家报价。</p>
<p><b>银行卡对比：</b> Visa/Mastercard通常加价0-1%，Amex较高约2-3%。Debit卡境外取款可能额外收取$2-5固定费用。出发前务必确认卡片的外汇政策。</p>
<p><b>旅游换汇建议：</b> 抵达后在当地ATM取现通常汇率最好（但注意ATM手续费）。携带少量现金应急即可，大额消费优先刷卡。</p>
<p><b>隐藏费用警示：</b> 动态货币转换（DCC）— 境外商户提供"以您的货币结算"时通常使用极差汇率，应始终选择以当地货币结算。</p>
</div>
</div>''',

    'cn:fitness-pace': '''
<div class="section" id="infoSection">
<h2>🏃 运动配速完全指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是配速？</b> 配速（Pace）是衡量跑步/步行速度的指标，通常表示为每公里所需时间（如5:30/km = 每公里5分30秒）。马拉松选手常用配速来规划比赛策略。</p>
<p><b>配速基准：</b> 步行：10-12分钟/公里；慢跑：6-8分钟/公里；跑步：4-6分钟/公里；专业马拉松选手：约3分钟/公里。普通人5公里完成时间约25-35分钟。</p>
<p><b>配速与距离关系：</b> 同一跑者，短距离配速通常快于长距离。5公里配速比半马配速快约10-15%，比全马配速快约15-25%。训练时应有针对性地练习不同距离的配速。</p>
<p><b>训练建议：</b> 80/20法则—80%的训练应为轻松配速（能正常交谈），20%为高强度训练。每周总跑量增加不超过10%以避免受伤。间歇训练可有效提升最大摄氧量和配速。</p>
<p><b>比赛策略：</b> 不要起跑太快！前半程保持略低于目标配速，后半程逐渐加速（负分段策略）。补给站不要停下，边走边喝。后半程心理因素比体力更重要。</p>
</div>
</div>''',

    'cn:internal-rate-of-return': '''
<div class="section" id="infoSection">
<h2>📈 内部收益率（IRR）投资指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是IRR？</b> 内部收益率（Internal Rate of Return）是使项目净现值为零的折现率，是衡量投资吸引力的核心指标。IRR越高，投资回报越丰厚。与ROI不同，IRR考虑了资金的时间价值。</p>
<p><b>IRR vs ROI：</b> 同样是100%回报，2年获得的年化IRR约41%，而10年获得仅约7%。IRR让不同时间跨度的投资可以进行公平比较。</p>
<p><b>应用场景：</b> ①评估私募股权/风险投资项目；②比较不同不动产投资回报；③计算企业资本预算项目的可行性；④分析保险/年金产品的实际收益；⑤对比不同债券的到期收益率。</p>
<p><b>决策基准：</b> 一般要求IRR > 资金成本（WACC）。个人投资者通常期望IRR > 8-12%。高IRR项目通常伴随高风险。巴菲特的长期年化回报约20%，可作为顶级标杆。</p>
<p><b>局限性：</b> IRR假设期间现金流按IRR再投资，可能高估实际收益。对于非常规现金流（正负交替），可能存在多个IRR。建议结合NPV和MIRR综合判断。</p>
</div>
</div>''',

    'cn:stock-options-calculator': '''
<div class="section" id="infoSection">
<h2>📊 股票期权投资指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>什么是股票期权？</b> 股票期权是赋予持有者在特定时间以特定价格买入（Call）或卖出（Put）股票的权利。期权是强大的工具，可用于投机、对冲风险或生成额外收入，但风险较高。</p>
<p><b>期权类型：</b> 看涨期权（Call）- 押注股价上涨；看跌期权（Put）- 押注股价下跌或保护持股。买方风险有限（最多损失权利金），卖方理论上风险无限。</p>
<p><b>关键要素：</b> 行权价（Strike Price）- 可买卖的目标价格；到期日（Expiration）- 期权失效日期；权利金（Premium）- 购买期权的成本；内在价值与时间价值决定了期权总价。</p>
<p><b>常见策略：</b> 覆盖性看涨（Covered Call）- 持有股票同时卖出Call，赚取额外收入；保护性看跌（Protective Put）- 为持股买保险；现金担保看跌（Cash-Secured Put）- 想低价买入时使用。</p>
<p><b>⚠️ 风险警示：</b> 期权交易可能导致本金全部损失。卖方策略风险极高。初学者应从模拟交易开始。本计算器仅用于教育目的，不构成投资建议。</p>
</div>
</div>''',

    'cn:subscription-auditor': '''
<div class="section" id="infoSection">
<h2>💰 订阅管理完全指南</h2>
<div style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
<p><b>订阅疲劳症（Subscription Fatigue）：</b> 美国成年人平均每月订阅支出$219+，涵盖流媒体、软件、健身、送餐、云存储等。一项调查显示84%的人低估了自己的订阅总支出至少$50/月。</p>
<p><b>常见浪费陷阱：</b> ①免费试用忘记取消—78%的人至少有一次被"免费试用"收费的经历；②重复订阅—同时拥有Netflix/Hulu/HBO/Disney+但实际只用其中1-2个；③闲置的健身房会员—年费$500+却每月只去2次；④多份云存储—Google Drive + Dropbox + iCloud同时付费。</p>
<p><b>审计策略：</b> ①每季度检查银行/信用卡账单中的定期扣款；②检查App Store/Google Play中的活跃订阅；③登录PayPal查看自动付款列表；④使用本工具记录和可视化所有订阅。</p>
<p><b>省钱方案：</b> 家庭共享计划每年可省$200+；年付通常比月付便宜15-25%；轮流订阅流媒体（一个月Netflix，下个月HBO）；检查是否有学生/军人的折扣资格。</p>
<p><b>订阅投资视角：</b> 如果每月削减$50订阅支出并投资于年化7%的指数基金，30年后将积累超过$60,000。小额支出累积效应不容小觑。</p>
</div>
</div>''',
}

fixed = 0
for page_key, issues in pages.items():
    lang, slug = page_key.split(':', 1)
    
    if lang == 'cn':
        filepath = f'{BASE}/{slug}/index.html'
    else:
        filepath = f'{BASE}/en/{slug}/index.html'
    
    if not os.path.exists(filepath):
        print(f"  SKIP: file not found: {filepath}")
        continue
    
    if page_key not in content_map:
        print(f"  SKIP: no content for {page_key}")
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if infoSection already exists
    if 'id="infoSection"' in content:
        print(f"  SKIP: infoSection already exists: {page_key}")
        continue
    
    # Insert before the footer div (last </div> before </body>)
    insert_html = content_map[page_key]
    
    # Find the footer section and insert before it
    # Pattern: the last <div class="footer">...</div> or <footer...> before </body>
    footer_match = re.search(r'(<footer[^>]*>|</div>\s*</div>\s*<div id="toast")', content)
    if footer_match:
        insert_pos = footer_match.start()
        new_content = content[:insert_pos] + insert_html + '\n' + content[insert_pos:]
    else:
        # Fallback: insert before </body>
        new_content = content.replace('</body>', insert_html + '\n</body>', 1)
    
    with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)
    
    print(f"  FIXED: {page_key}")
    fixed += 1

print(f"\nTotal fixed: {fixed}/10")
