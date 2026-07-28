#!/usr/bin/env python3
"""批量修复no_related_tools和content_thin/very_thin"""
import os, re, json

SITE = '/home/chison/tools-site'

# 相关工具映射：根据工具名推荐3个相关工具
RELATED_MAP = {
    'expense-split-calculator': ['budget-planner', 'tip-calculator', 'discount-calculator'],
    'macro-calculator-advanced': ['bmi-calculator', 'calorie-calculator', 'muscle-gain-calculator'],
    'muscle-gain-calculator': ['bmi-calculator', 'macro-calculator-advanced', 'calorie-calculator'],
    'roi-calculator-rental': ['mortgage-calculator', 'compound-interest-calculator', 'loan-calculator'],
    'stock-screener-simple': ['stock-average-calculator', 'compound-interest-calculator', 'apy-to-apr-calculator'],
    'day-trading-calculator': ['stock-average-calculator', 'compound-interest-calculator', 'profit-margin-calculator'],
    'co-worker-salary-calculator': ['salary-calculator', 'paycheck-deductions', 'overtime-calculator'],
    'fifo-lifo-calculator': ['gross-profit-calculator', 'profit-margin-calculator', 'inventory-tracker'],
    'fitness-plan-generator': ['bmi-calculator', 'calorie-calculator', 'macro-calculator-advanced'],
    'gross-profit-calculator': ['profit-margin-calculator', 'fifo-lifo-calculator', 'revenue-calculator'],
}

# CN工具名→emoji+中文名
CN_NAMES = {
    'expense-split-calculator': ('💰', '费用分摊计算器'),
    'macro-calculator-advanced': ('🍽️', '高级宏量营养素计算器'),
    'muscle-gain-calculator': ('💪', '增肌计算器'),
    'roi-calculator-rental': ('🏠', '出租ROI计算器'),
    'stock-screener-simple': ('📊', '简易选股器'),
    'day-trading-calculator': ('📈', '日内交易计算器'),
    'co-worker-salary-calculator': ('👥', '同事薪资计算器'),
    'fifo-lifo-calculator': ('📦', 'FIFO/LIFO库存计算器'),
    'fitness-plan-generator': ('🏋️', '健身计划生成器'),
    'gross-profit-calculator': ('💵', '毛利润计算器'),
    'budget-planner': ('📋', '预算规划器'),
    'tip-calculator': ('💸', '小费计算器'),
    'discount-calculator': ('🏷️', '折扣计算器'),
    'bmi-calculator': ('⚖️', 'BMI计算器'),
    'calorie-calculator': ('🔥', '卡路里计算器'),
    'mortgage-calculator': ('🏡', '房贷计算器'),
    'compound-interest-calculator': ('📈', '复利计算器'),
    'loan-calculator': ('💳', '贷款计算器'),
    'stock-average-calculator': ('📉', '股票均价计算器'),
    'apy-to-apr-calculator': ('🔄', 'APY/APR转换器'),
    'profit-margin-calculator': ('📊', '利润率计算器'),
    'salary-calculator': ('💼', '薪资计算器'),
    'paycheck-deductions': ('📋', '工资扣款计算器'),
    'overtime-calculator': ('⏰', '加班工资计算器'),
    'inventory-tracker': ('📋', '库存追踪器'),
    'revenue-calculator': ('💰', '收入计算器'),
}

EN_NAMES = {
    'expense-split-calculator': 'Expense Split Calculator',
    'macro-calculator-advanced': 'Advanced Macro Calculator',
    'muscle-gain-calculator': 'Muscle Gain Calculator',
    'roi-calculator-rental': 'Rental ROI Calculator',
    'stock-screener-simple': 'Simple Stock Screener',
    'day-trading-calculator': 'Day Trading Calculator',
    'co-worker-salary-calculator': 'Co-worker Salary Calculator',
    'fifo-lifo-calculator': 'FIFO/LIFO Calculator',
    'fitness-plan-generator': 'Fitness Plan Generator',
    'gross-profit-calculator': 'Gross Profit Calculator',
    'budget-planner': 'Budget Planner',
    'tip-calculator': 'Tip Calculator',
    'discount-calculator': 'Discount Calculator',
    'bmi-calculator': 'BMI Calculator',
    'calorie-calculator': 'Calorie Calculator',
    'mortgage-calculator': 'Mortgage Calculator',
    'compound-interest-calculator': 'Compound Interest Calculator',
    'loan-calculator': 'Loan Calculator',
    'stock-average-calculator': 'Stock Average Calculator',
    'apy-to-apr-calculator': 'APY to APR Converter',
    'profit-margin-calculator': 'Profit Margin Calculator',
    'salary-calculator': 'Salary Calculator',
    'paycheck-deductions': 'Paycheck Deductions',
    'overtime-calculator': 'Overtime Calculator',
    'inventory-tracker': 'Inventory Tracker',
    'revenue-calculator': 'Revenue Calculator',
}

def get_related_html(lang, tool_name):
    """生成相关工具推荐的HTML"""
    related = RELATED_MAP.get(tool_name, [])
    if not related:
        return ''
    
    if lang == 'cn':
        title = '🔗 相关工具推荐'
        items = []
        for r in related:
            emoji, name = CN_NAMES.get(r, ('🔧', r.replace('-', ' ').title()))
            items.append(f'<a href="/{r}/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">{emoji} {name}</a>')
    else:
        title = '🔗 Related Tools'
        items = []
        for r in related:
            name = EN_NAMES.get(r, r.replace('-', ' ').title())
            emoji = CN_NAMES.get(r, ('🔧', ''))[0] if r in CN_NAMES else '🔧'
            items.append(f'<a href="/en/{r}/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">{emoji} {name}</a>')
    
    html = f'\n<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">{title}</h2><div style="display:flex;flex-wrap:wrap;gap:4px;">{"".join(items)}</div></section>\n'
    return html

def get_content_block(lang, tool_name):
    """为content_thin/very_thin生成补充内容"""
    blocks = {
        'expense-split-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">📝 费用分摊常见场景</h3><ul><li><strong>聚餐AA制</strong>：输入总金额和人数，自动计算每人应付</li><li><strong>旅行费用</strong>：按住宿天数、交通方式等按比例分摊</li><li><strong>合租水电</strong>：按面积或人数分摊水电燃气费用</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">📝 Common Use Cases</h3><ul><li><strong>Dining Split</strong>: Enter total bill and number of people</li><li><strong>Travel Expenses</strong>: Split by days stayed or transport mode</li><li><strong>Shared Utilities</strong>: Divide bills by room size or headcount</li></ul></div>'
        },
        'day-trading-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">⚠️ 交易提示</h3><p>日内交易风险极高。本计算器仅帮助估算盈亏，不构成投资建议。请根据自身风险承受能力谨慎决策。</p></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">⚠️ Trading Disclaimer</h3><p>Day trading carries high risk. This calculator estimates P&L only and does not constitute investment advice.</p></div>'
        },
        'fifo-lifo-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#eff6ff;border-left:4px solid #3b82f6;border-radius:4px;"><h3 style="margin-top:0;">📚 FIFO vs LIFO 说明</h3><ul><li><strong>FIFO（先进先出）</strong>：先入库的存货先出库，通胀期利润偏高</li><li><strong>LIFO（后进先出）</strong>：后入库的存货先出库，通胀期利润偏低</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#eff6ff;border-left:4px solid #3b82f6;border-radius:4px;"><h3 style="margin-top:0;">📚 FIFO vs LIFO Explained</h3><ul><li><strong>FIFO</strong>: Oldest inventory sold first, higher profit during inflation</li><li><strong>LIFO</strong>: Newest inventory sold first, lower profit during inflation</li></ul></div>'
        },
        'fitness-plan-generator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#fdf2f8;border-left:4px solid #ec4899;border-radius:4px;"><h3 style="margin-top:0;">💡 使用建议</h3><p>制定计划前请先评估自身体能水平。建议配合BMI计算器和卡路里计算器使用，制定更科学的健身方案。</p></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#fdf2f8;border-left:4px solid #ec4899;border-radius:4px;"><h3 style="margin-top:0;">💡 Usage Tips</h3><p>Assess your fitness level before planning. Pair with BMI Calculator and Calorie Calculator for a more scientific approach.</p></div>'
        },
        'gross-profit-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">📊 毛利率分析</h3><ul><li>毛利率 = (收入 - 成本) / 收入 × 100%</li><li>毛利率 > 40% 通常被视为良好</li><li>不同行业毛利率标准不同，请参考同行业平均水平</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">📊 Gross Margin Analysis</h3><ul><li>Gross Margin = (Revenue - COGS) / Revenue × 100%</li><li>Margin > 40% is generally considered healthy</li><li>Standards vary by industry — compare with peers</li></ul></div>'
        },
        'co-worker-salary-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">📋 薪资对比注意事项</h3><ul><li>同级别不同经验年限薪资差异可达30-50%</li><li>地区差异显著，一线城市通常比二三线高20-40%</li><li>除月薪外，还应考虑年终奖、股票期权、福利等总包</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">📋 Salary Comparison Notes</h3><ul><li>Same level, different experience: 30-50% variance</li><li>Location matters: tier-1 cities typically 20-40% higher</li><li>Consider total comp: bonus, stock, benefits beyond base salary</li></ul></div>'
        },
        'macro-calculator-advanced': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#eff6ff;border-left:4px solid #3b82f6;border-radius:4px;"><h3 style="margin-top:0;">🥗 宏量营养素基础</h3><ul><li><strong>蛋白质</strong>：1g = 4千卡，建议1.6-2.2g/kg体重</li><li><strong>碳水</strong>：1g = 4千卡，占总热量45-65%</li><li><strong>脂肪</strong>：1g = 9千卡，占总热量20-35%</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#eff6ff;border-left:4px solid #3b82f6;border-radius:4px;"><h3 style="margin-top:0;">🥗 Macro Basics</h3><ul><li><strong>Protein</strong>: 1g = 4 kcal, 1.6-2.2g/kg recommended</li><li><strong>Carbs</strong>: 1g = 4 kcal, 45-65% of total calories</li><li><strong>Fat</strong>: 1g = 9 kcal, 20-35% of total calories</li></ul></div>'
        },
        'muscle-gain-calculator': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#fdf2f8;border-left:4px solid #ec4899;border-radius:4px;"><h3 style="margin-top:0;">💪 增肌三要素</h3><ul><li><strong>热量盈余</strong>：每日摄入 > 消耗，建议+300-500千卡</li><li><strong>渐进超负荷</strong>：逐步增加训练重量/次数</li><li><strong>充足睡眠</strong>：每天7-9小时，肌肉在休息时生长</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#fdf2f8;border-left:4px solid #ec4899;border-radius:4px;"><h3 style="margin-top:0;">💪 Muscle Gain Essentials</h3><ul><li><strong>Calorie Surplus</strong>: Eat 300-500 kcal above maintenance</li><li><strong>Progressive Overload</strong>: Gradually increase weight/reps</li><li><strong>Sleep</strong>: 7-9 hours — muscles grow during rest</li></ul></div>'
        },
        'roi-calculator-rental': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">🏠 出租回报率参考</h3><ul><li>年租金回报率 = 年租金收入 / 房产总价 × 100%</li><li>国内一线城市住宅租金回报率约1-2%</li><li>商业地产回报率通常高于住宅，约4-8%</li></ul></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#f0fdf4;border-left:4px solid #22c55e;border-radius:4px;"><h3 style="margin-top:0;">🏠 Rental ROI Reference</h3><ul><li>Annual ROI = Annual Rent / Property Price × 100%</li><li>Residential ROI in major cities: typically 1-3%</li><li>Commercial properties usually yield 4-8%</li></ul></div>'
        },
        'stock-screener-simple': {
            'cn': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">⚠️ 免责声明</h3><p>本筛选器仅提供基础数据参考，不构成投资建议。股票投资有风险，入市需谨慎。请结合基本面和技术面综合判断。</p></div>',
            'en': '<div style="margin:2rem 0;padding:1rem;background:#fef3c7;border-left:4px solid #f59e0b;border-radius:4px;"><h3 style="margin-top:0;">⚠️ Disclaimer</h3><p>This screener provides reference data only, not investment advice. All investments carry risk. Combine fundamental and technical analysis for decisions.</p></div>'
        },
    }
    
    data = blocks.get(tool_name, {})
    return data.get(lang, '')


def fix_page(path, lang, tool_name, issues):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    fixed = []
    
    # 1. 添加相关工具推荐
    if 'no_related_tools' in issues and 'related-tools' not in c:
        related_html = get_related_html(lang, tool_name)
        if related_html:
            # 插在</footer>前面
            footer_pos = c.rfind('<footer')
            if footer_pos > 0:
                c = c[:footer_pos] + related_html + c[footer_pos:]
                fixed.append('no_related_tools')
            elif '</body>' in c:
                body_pos = c.find('</body>')
                c = c[:body_pos] + related_html + c[body_pos:]
                fixed.append('no_related_tools')
    
    # 2. 添加内容块
    if ('content_thin' in issues or 'content_very_thin' in issues):
        content_html = get_content_block(lang, tool_name)
        if content_html and content_html not in c:
            # 插在related-tools后面或main结尾
            if 'related-tools' in c:
                related_end = c.find('</section>', c.find('related-tools'))
                if related_end > 0:
                    c = c[:related_end + len('</section>')] + '\n' + content_html + c[related_end + len('</section>'):]
                    fixed.append('content_block')
            elif '<footer' in c:
                footer_pos = c.find('<footer')
                c = c[:footer_pos] + content_html + '\n' + c[footer_pos:]
                fixed.append('content_block')
    
    # 3. low_interact: day-trading-calculator需要加交互
    if 'low_interact' in issues and tool_name == 'day-trading-calculator':
        # 检查是否有足够交互元素
        btns = len(re.findall(r'<button', c))
        inputs = len(re.findall(r'<input|<textarea|<select', c))
        if btns + inputs < 3:
            # 在现有按钮后添加清空按钮
            if '<button' in c and 'clearBtn' not in c and '清空' not in c and 'Clear' not in c:
                if lang == 'cn':
                    clear_btn = '<button onclick="clearAll()" style="margin-left:8px;padding:10px 20px;background:#e5e7eb;border:none;border-radius:6px;cursor:pointer;color:#374151;">🗑️ 清空</button>'
                    clear_js = '\nfunction clearAll(){document.querySelectorAll("input").forEach(i=>i.value="");document.querySelectorAll(".result").forEach(r=>r.textContent="");}\n'
                else:
                    clear_btn = '<button onclick="clearAll()" style="margin-left:8px;padding:10px 20px;background:#e5e7eb;border:none;border-radius:6px;cursor:pointer;color:#374151;">🗑️ Clear</button>'
                    clear_js = '\nfunction clearAll(){document.querySelectorAll("input").forEach(i=>i.value="");document.querySelectorAll(".result").forEach(r=>r.textContent="");}\n'
                
                # 找最后一个button并插入清空按钮
                last_btn = c.rfind('</button>')
                if last_btn > 0:
                    c = c[:last_btn + len('</button>')] + clear_btn + c[last_btn + len('</button>'):]
                    # 在</script>前加clearAll函数
                    script_end = c.rfind('</script>')
                    if script_end > 0:
                        c = c[:script_end] + clear_js + c[script_end:]
                    fixed.append('low_interact')
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
    
    return fixed

# 处理所有残留页面
pages = [
    ('cn', 'co-worker-salary-calculator', ['content_thin']),
    ('cn', 'day-trading-calculator', ['low_interact', 'content_very_thin']),
    ('cn', 'expense-split-calculator', ['content_very_thin', 'no_related_tools']),
    ('cn', 'fifo-lifo-calculator', ['content_thin']),
    ('cn', 'fitness-plan-generator', ['content_thin']),
    ('cn', 'gross-profit-calculator', ['content_thin']),
    ('cn', 'macro-calculator-advanced', ['content_thin', 'no_related_tools']),
    ('cn', 'muscle-gain-calculator', ['content_very_thin', 'no_related_tools']),
    ('cn', 'roi-calculator-rental', ['content_very_thin', 'no_related_tools']),
    ('cn', 'stock-screener-simple', ['content_very_thin', 'no_related_tools']),
    ('en', 'day-trading-calculator', ['low_interact']),
    ('en', 'expense-split-calculator', ['content_thin', 'no_related_tools']),
    ('en', 'macro-calculator-advanced', ['no_related_tools']),
    ('en', 'muscle-gain-calculator', ['no_related_tools']),
    ('en', 'roi-calculator-rental', ['no_related_tools']),
    ('en', 'stock-screener-simple', ['no_related_tools']),
]

total_fixed = 0
for lang, tool, issues in pages:
    if lang == 'en':
        path = os.path.join(SITE, 'en', tool, 'index.html')
    else:
        path = os.path.join(SITE, tool, 'index.html')
    
    if not os.path.isfile(path):
        print(f"⚠️  {lang}:{tool} 不存在")
        continue
    
    fixed = fix_page(path, lang, tool, issues)
    if fixed:
        print(f"✅ {lang}:{tool} 修复 {fixed}")
        total_fixed += len(fixed)
    else:
        print(f"⏭️  {lang}:{tool} 无法修复（{issues}）")

print(f"\n总计修复: {total_fixed} 个问题")