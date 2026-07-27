#!/usr/bin/env python3
"""
批量修复 quality_loop.py 未能自动修复的残留问题:
- no_adsense: 插入AdSense代码到</head>前
- no_related_tools: 插入相关工具推荐区到</footer>或</body>前
- no_copy_btn: 添加复制按钮
- content_thin / content_very_thin: 添加说明段落
- title_long: 缩短title
"""
import os, re, json

SITE = '/home/chison/tools-site'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>\n'
AD_SLOT_HTML = '<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="9876543210" data-ad-format="auto" data-full-width-responsive="true"></ins></div>\n'

# 页面信息: {page_key: [issues]}
PAGES = {
    'cn:bmi-percentile-calculator': ['no_adsense', 'content_very_thin'],
    'cn:bmr-calculator-harris-benedict': ['no_adsense', 'content_thin'],
    'cn:calorie-burned-calculator': ['no_adsense', 'content_thin'],
    'cn:cholesterol-units-converter': ['no_adsense', 'content_thin'],
    'cn:currency-converter-with-rates': ['no_copy_btn', 'no_related_tools'],
    'cn:discount-calculator-percentage': ['no_related_tools'],
    'cn:raise-calculator': ['no_copy_btn', 'content_thin', 'no_related_tools'],
    'cn:roi-calculator-investment': ['no_adsense', 'content_very_thin'],
    'cn:tip-calculator-percentage': ['no_related_tools'],
    'cn:travel-budget-calculator': ['no_copy_btn', 'content_thin', 'no_related_tools'],
    'en:bmi-percentile-calculator': ['no_adsense'],
    'en:bmr-calculator-harris-benedict': ['no_adsense'],
    'en:calorie-burned-calculator': ['no_adsense'],
    'en:cholesterol-units-converter': ['no_adsense'],
    'en:currency-converter-with-rates': ['title_long', 'no_copy_btn', 'no_related_tools'],
    'en:discount-calculator-percentage': ['title_long', 'no_related_tools'],
    'en:raise-calculator': ['no_copy_btn', 'no_related_tools'],
    'en:roi-calculator-investment': ['no_adsense'],
    'en:tip-calculator-percentage': ['no_related_tools'],
    'en:travel-budget-calculator': ['no_copy_btn', 'no_related_tools'],
}

# 相关工具推荐区模板 (CN)
RELATED_TOOLS_CN = '''<div class="section related-tools">
  <h2>🔧 相关工具</h2>
  <div class="tool-links" style="display:flex;flex-wrap:wrap;gap:8px">{links}</div>
</div>
'''

# 相关工具推荐区模板 (EN)
RELATED_TOOLS_EN = '''<div class="section related-tools">
  <h2>🔧 Related Tools</h2>
  <div class="tool-links" style="display:flex;flex-wrap:wrap;gap:8px">{links}</div>
</div>
'''

# 工具名到推荐工具的映射（由工具自身决定）
TOOL_RELATED = {
    'bmi-percentile-calculator': ['bmi-calculator', 'macro-calculator', 'calorie-calculator', 'bmr-calculator-harris-benedict'],
    'bmr-calculator-harris-benedict': ['calorie-calculator', 'bmi-calculator', 'macro-calculator', 'bmi-percentile-calculator'],
    'calorie-burned-calculator': ['calorie-calculator', 'bmr-calculator-harris-benedict', 'macro-calculator', 'bmi-calculator'],
    'cholesterol-units-converter': ['unit-converter', 'blood-sugar-converter', 'blood-pressure-tracker', 'medical-calculator'],
    'currency-converter-with-rates': ['discount-calculator-percentage', 'tip-calculator-percentage', 'roi-calculator-investment', 'travel-budget-calculator'],
    'discount-calculator-percentage': ['tip-calculator-percentage', 'currency-converter-with-rates', 'raise-calculator', 'travel-budget-calculator'],
    'raise-calculator': ['discount-calculator-percentage', 'tip-calculator-percentage', 'roi-calculator-investment', 'currency-converter-with-rates'],
    'roi-calculator-investment': ['compound-interest-calculator', '401k-calculator', 'currency-converter-with-rates', 'raise-calculator'],
    'tip-calculator-percentage': ['discount-calculator-percentage', 'currency-converter-with-rates', 'travel-budget-calculator', 'raise-calculator'],
    'travel-budget-calculator': ['currency-converter-with-rates', 'tip-calculator-percentage', 'discount-calculator-percentage', 'travel-planner'],
}


def get_tool_names():
    """获取所有存在的工具目录名"""
    tools = set()
    SKIP = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git',
            'about','contact','terms','privacy','node_modules'}
    for d in os.listdir(SITE):
        if d in SKIP or d.startswith('.'): continue
        p = os.path.join(SITE, d, 'index.html')
        if os.path.isfile(p): tools.add(d)
    return tools


def build_related_links(tool_name, lang, all_tools):
    """构建相关工具链接HTML"""
    related = TOOL_RELATED.get(tool_name, [])
    # 过滤不存在的工具
    valid = [t for t in related if t in all_tools][:4]
    if not valid:
        return ''
    
    links = []
    for t in valid:
        # 尝试从EN页面获取英文名
        en_path = os.path.join(SITE, 'en', t, 'index.html')
        name = t.replace('-', ' ').title()
        if os.path.isfile(en_path):
            with open(en_path, 'r', encoding='utf-8', errors='ignore') as f:
                enc = f.read()
            tm = re.search(r'<title>([^<]+)</title>', enc)
            if tm:
                en_title = tm.group(1).split(' - ')[0].split(' | ')[0].strip()
                if lang == 'en':
                    name = en_title
        
        if lang == 'cn':
            url = f'/{t}/'
            cn_path = os.path.join(SITE, t, 'index.html')
            if os.path.isfile(cn_path):
                with open(cn_path, 'r', encoding='utf-8', errors='ignore') as f:
                    cnc = f.read()
                tm = re.search(r'<title>([^<]+)</title>', cnc)
                if tm:
                    name = tm.group(1).split(' - ')[0].split(' | ')[0].strip()
        else:
            url = f'/en/{t}/'
        
        links.append(f'<a href="{url}" style="background:var(--bg);padding:6px 14px;border-radius:8px;color:var(--accent);font-size:.85rem;border:1px solid var(--border)">{name}</a>')
    
    return '\n    '.join(links)


def fix_no_adsense(c, path):
    """插入AdSense脚本到</head>前"""
    if 'adsbygoogle' in c:
        return c, True  # already has
    
    if '</head>' in c:
        # 在GTM script后面、</head>前插入
        c = c.replace('</head>', ADSENSE_SCRIPT + '</head>')
        # 在<body>后第一个主容器内插入ad-slot
        # 在 <div class="container"> 或第一个section后
    return c, True


def fix_no_ad_slot(c):
    """在页面中插入广告位（如果还没有）"""
    if 'ad-slot' in c:
        return c, True
    
    # 在 <main> 或第一个 .section 前插入
    # 找到合适的插入点
    insert_after = None
    for pattern in [
        r'(<div class="header"[^>]*>.*?</div>\s*</div>)',  # header结束
        r'(<div class="nav-back"[^>]*>.*?</div>)',  # nav-back后
    ]:
        m = re.search(pattern, c, re.DOTALL)
        if m:
            insert_after = m.end()
            break
    
    if insert_after:
        c = c[:insert_after] + '\n' + AD_SLOT_HTML + c[insert_after:]
        return c, True
    
    return c, False


def fix_no_copy_btn(c, lang):
    """添加复制按钮"""
    if 'copyBtn' in c or 'copy-btn' in c:
        return c, True
    
    # 查找按钮行区域，在重置按钮后添加复制按钮
    # 模式1: <button class="btn btn-secondary" id="resetBtn"
    reset_m = re.search(r'(<button[^>]*id="resetBtn"[^>]*>.*?</button>)', c)
    if reset_m:
        copy_btn = '<button class="btn btn-secondary" id="copyBtn">📋 复制结果</button>' if lang == 'cn' else '<button class="btn btn-secondary" id="copyBtn">📋 Copy Results</button>'
        # 插入到resetBtn后面
        insert_pos = reset_m.end()
        c = c[:insert_pos] + '\n    ' + copy_btn + c[insert_pos:]
        
        # 添加复制JS逻辑
        copy_js = '''
    // Copy functionality
    const copyBtn = document.getElementById('copyBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const resultEl = document.querySelector('.result-section, #result, [class*="result"]');
        if (resultEl) {
          const text = resultEl.innerText || resultEl.textContent;
          navigator.clipboard.writeText(text).then(() => {
            const orig = copyBtn.textContent;
            copyBtn.textContent = '{}';
            setTimeout(() => copyBtn.textContent = orig, 2000);
          }).catch(() => {});
        }
      });
    }'''.format('✅ 已复制!' if lang == 'cn' else '✅ Copied!')
        
        # 找到</script>位置插入（在最后一个</script>标签前）
        script_end = c.rfind('</script>')
        if script_end > 0:
            c = c[:script_end] + copy_js + '\n  ' + c[script_end:]
        else:
            # 在</body>前插入
            c = c.replace('</body>', '<script>' + copy_js + '\n</script>\n</body>')
        
        return c, True
    
    return c, False


def fix_no_related_tools(c, tool_name, lang, all_tools):
    """插入相关工具推荐区"""
    if 'related-tools' in c or '相关工具' in c or 'Related Tools' in c:
        return c, True
    
    links_html = build_related_links(tool_name, lang, all_tools)
    if not links_html:
        return c, False
    
    if lang == 'cn':
        related_html = RELATED_TOOLS_CN.format(links=links_html)
    else:
        related_html = RELATED_TOOLS_EN.format(links=links_html)
    
    # 插入到</footer>前或最后一个section后
    if '</footer>' in c:
        c = c.replace('</footer>', related_html + '\n</footer>')
    elif '<footer' in c:
        # 在footer前插入
        fm = re.search(r'<footer[^>]*>', c)
        if fm:
            c = c[:fm.start()] + related_html + '\n' + c[fm.start():]
    else:
        # 在</body>前插入
        c = c.replace('</body>', related_html + '\n</body>')
    
    return c, True


def fix_content_thin(c, tool_name, lang, level='thin'):
    """为内容薄的页面添加更多说明"""
    clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    
    # 如果已经有足够内容，不再添加
    if level == 'very_thin' and text_len >= 300:
        return c, True
    if level == 'thin' and text_len >= 500:
        return c, True
    
    # 生成描述文字
    descriptions = {
        'bmi-percentile-calculator': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于儿童BMI百分位</h2>
    <p style="color:var(--muted);line-height:1.8">BMI（身体质量指数）百分位是评估儿童生长发育的重要指标。CDC（美国疾病控制与预防中心）生长曲线通过对全国儿童数据的统计分析，将BMI值转化为百分位数。百分位50代表中位数，85-95为超重，≥95为肥胖。儿童BMI随年龄变化，因此必须结合年龄和性别评估，不能简单套用成人标准。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具基于CDC 2000年生长参考数据，支持2-20岁儿童和青少年。Z-score表示偏离中位数的标准差数，比百分位更适用于极端值评估。我们的计算器完全在浏览器本地运行，无需上传任何数据，保护儿童隐私。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About BMI Percentiles</h2>
    <p style="color:var(--muted);line-height:1.8">BMI (Body Mass Index) percentile is a key indicator for assessing child growth and development. The CDC growth charts convert BMI values into percentiles based on statistical analysis of national child data. The 50th percentile represents the median, 85-95 indicates overweight, and ≥95 indicates obesity. Children's BMI changes with age, so it must be evaluated with age and gender, not simply using adult standards.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool is based on CDC 2000 growth reference data, supporting children and adolescents aged 2-20. Z-score represents standard deviations from the median, more suitable for extreme value assessment than percentiles. Our calculator runs entirely locally in your browser — no data is ever uploaded, protecting children's privacy.</p>
  </div>
''',
        },
        'bmr-calculator-harris-benedict': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于BMR与哈里斯-本尼迪克特公式</h2>
    <p style="color:var(--muted);line-height:1.8">基础代谢率（BMR）是身体在完全静止状态下维持生命所需的最低能量。哈里斯-本尼迪克特公式是最经典的BMR计算方法之一，于1919年发表，经过多次修订。公式基于体重、身高、年龄和性别四个参数，在临床营养、运动科学和体重管理领域广泛应用。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">使用本工具可以快速估算每日基础能量消耗，并结合活动系数计算总能量需求。这对于制定健康饮食计划和体重管理目标具有重要参考价值。所有计算均在本地浏览器完成，确保您的隐私安全。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About BMR & Harris-Benedict</h2>
    <p style="color:var(--muted);line-height:1.8">Basal Metabolic Rate (BMR) is the minimum energy required to sustain life at complete rest. The Harris-Benedict equation is one of the most classic BMR calculation methods, published in 1919 and revised multiple times. Based on weight, height, age, and gender, it is widely used in clinical nutrition, sports science, and weight management.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">Use this tool to quickly estimate daily basal energy expenditure and calculate total energy needs with activity factors. This is valuable for creating healthy diet plans and weight management goals. All calculations run locally in your browser, ensuring your privacy.</p>
  </div>
''',
        },
        'calorie-burned-calculator': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于卡路里消耗</h2>
    <p style="color:var(--muted);line-height:1.8">卡路里消耗计算基于MET（代谢当量）系统，1 MET代表静息代谢率。不同活动有不同的MET值：步行约3-5 MET，慢跑约7-8 MET，跑步约8-12 MET，高强度运动可达15 MET以上。消耗的卡路里 = MET × 体重(kg) × 时间(小时)。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具内置了数十种常见活动的MET值，只需输入您的体重和运动时间即可估算卡路里消耗。这对于制定运动计划和体重管理非常有帮助。所有数据在本地处理，无需注册。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About Calorie Burn</h2>
    <p style="color:var(--muted);line-height:1.8">Calorie burn calculation is based on the MET (Metabolic Equivalent of Task) system, where 1 MET represents resting metabolic rate. Different activities have different MET values: walking ~3-5 MET, jogging ~7-8 MET, running ~8-12 MET, and high-intensity exercise can reach 15+ MET. Calories burned = MET × weight(kg) × time(hours).</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool includes MET values for dozens of common activities. Simply enter your weight and exercise duration to estimate calorie burn. It's very helpful for exercise planning and weight management. All data is processed locally — no signup required.</p>
  </div>
''',
        },
        'cholesterol-units-converter': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于胆固醇单位换算</h2>
    <p style="color:var(--muted);line-height:1.8">胆固醇检测结果有两种常用单位：mmol/L（毫摩尔/升）和 mg/dL（毫克/分升）。不同国家和实验室使用的单位可能不同，中国常用mmol/L，美国常用mg/dL。总胆固醇换算系数为38.67，即 mg/dL = mmol/L × 38.67。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具支持总胆固醇、LDL（低密度脂蛋白）、HDL（高密度脂蛋白）和甘油三酯的单位换算，帮助您跨标准理解检验报告。所有计算在浏览器本地完成，不会上传您的健康数据。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About Cholesterol Unit Conversion</h2>
    <p style="color:var(--muted);line-height:1.8">Cholesterol test results use two common units: mmol/L (millimoles per liter) and mg/dL (milligrams per deciliter). Different countries and labs may use different units — mmol/L is common in many countries while mg/dL is standard in the US. The total cholesterol conversion factor is 38.67, i.e., mg/dL = mmol/L × 38.67.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool supports conversion for total cholesterol, LDL, HDL, and triglycerides, helping you interpret lab reports across standards. All calculations run locally in your browser — your health data is never uploaded.</p>
  </div>
''',
        },
        'raise-calculator': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于涨薪计算</h2>
    <p style="color:var(--muted);line-height:1.8">涨薪计算器帮助您量化工资增长的实际影响。无论是百分比涨幅还是固定金额调整，了解税后实际收入变化对财务规划至关重要。美国平均年涨薪幅度约3-5%，但技术、医疗等高需求行业可能更高。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具支持多种计算模式：按百分比、按金额、按周期（年薪/月薪/时薪）。自动对比涨薪前后的差异，帮助您评估offer和规划预算。所有数据在本地处理，保障隐私安全。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About Raise Calculation</h2>
    <p style="color:var(--muted);line-height:1.8">The raise calculator helps quantify the real impact of salary increases. Whether it's a percentage raise or a fixed amount adjustment, understanding your actual take-home change is crucial for financial planning. The average annual raise in the US is about 3-5%, though high-demand fields like tech and healthcare may see higher rates.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool supports multiple calculation modes: by percentage, by amount, and by pay period (annual/monthly/hourly). Automatically compares before and after differences to help you evaluate offers and plan budgets. All data is processed locally for privacy.</p>
  </div>
''',
        },
        'roi-calculator-investment': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于投资回报率(ROI)</h2>
    <p style="color:var(--muted);line-height:1.8">ROI（投资回报率）是衡量投资效率的核心指标，计算公式为：ROI =（收益 - 成本）/ 成本 × 100%。它帮助投资者比较不同投资机会的收益效率。年化ROI考虑了时间因素，更能反映长期投资表现。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具支持多种计算模式：简单ROI、年化ROI和净现值分析。输入初始投资、期末价值和持有期即可获得完整的投资回报分析。所有计算在本地完成，无需上传财务数据。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About ROI (Return on Investment)</h2>
    <p style="color:var(--muted);line-height:1.8">ROI (Return on Investment) is a core metric for measuring investment efficiency. The formula is: ROI = (Gain - Cost) / Cost × 100%. It helps investors compare the return efficiency of different opportunities. Annualized ROI factors in time, better reflecting long-term investment performance.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool supports multiple calculation modes: simple ROI, annualized ROI, and net present value analysis. Enter initial investment, end value, and holding period for a complete return analysis. All calculations run locally — no financial data is ever uploaded.</p>
  </div>
''',
        },
        'travel-budget-calculator': {
            'cn': '''<div class="section" style="margin-top:16px">
    <h2>📖 关于旅行预算规划</h2>
    <p style="color:var(--muted);line-height:1.8">合理的旅行预算是愉快旅行的基础。主要开支类别包括交通（机票/火车/租车）、住宿、餐饮、景点门票、购物和应急储备。国际旅行还需考虑签证费、旅行保险和汇率波动。</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">本工具帮助您分门别类规划旅行开支，自动汇总并提供预算建议。内置常见旅行类型模板（背包客/经济/舒适/奢华），快速估算总费用。所有计算在本地完成，保障隐私。</p>
  </div>
''',
            'en': '''<div class="section" style="margin-top:16px">
    <h2>📖 About Travel Budget Planning</h2>
    <p style="color:var(--muted);line-height:1.8">A well-planned travel budget is the foundation of an enjoyable trip. Major expense categories include transportation (flights/trains/rental cars), accommodation, dining, attractions, shopping, and emergency reserves. International travel should also account for visa fees, travel insurance, and exchange rate fluctuations.</p>
    <p style="color:var(--muted);line-height:1.8;margin-top:12px">This tool helps you plan travel expenses by category, automatically summarize totals, and provides budgeting suggestions. Built-in common travel style templates (backpacker/budget/comfort/luxury) let you quickly estimate total costs. All calculations run locally for privacy.</p>
  </div>
''',
        },
    }
    
    desc = descriptions.get(tool_name, {}).get(lang)
    if not desc:
        return c, False
    
    # 插入到</footer>前或最后一个section后或</body>前
    if '</footer>' in c:
        c = c.replace('</footer>', desc + '\n</footer>')
    elif '<footer' in c:
        fm = re.search(r'<footer[^>]*>', c)
        if fm:
            c = c[:fm.start()] + desc + '\n' + c[fm.start():]
    else:
        c = c.replace('</body>', desc + '\n</body>')
    
    return c, True


def fix_title_long(c, lang):
    """缩短过长的title"""
    tm = re.search(r'<title>([^<]+)</title>', c)
    if not tm:
        return c, False
    t = tm.group(1)
    if len(t) <= 60:
        return c, True
    
    # 尝试缩短
    nt = t.replace('Free Online ', '').replace('Online ', '').replace('Free ', '')
    if ' - Free ToolBase' in nt:
        core = nt.replace(' - Free ToolBase', '')
        mx = 60 - len(' - Free ToolBase')
        if len(core) > mx:
            core = core[:mx-1] + '…'
        nt = core + ' - Free ToolBase'
    
    if nt != t and len(nt) <= 60:
        c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
        return c, True
    
    return c, False


def main():
    all_tools = get_tool_names()
    fixed_count = 0
    results = []
    
    for page_key, issues in PAGES.items():
        lang, tool = page_key.split(':', 1)
        
        if lang == 'cn':
            path = os.path.join(SITE, tool, 'index.html')
        else:
            path = os.path.join(SITE, 'en', tool, 'index.html')
        
        if not os.path.isfile(path):
            print(f"[SKIP] {page_key}: file not found")
            continue
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            original = f.read()
        
        c = original
        page_fixed = []
        
        for issue in issues:
            if issue == 'no_adsense':
                c, ok = fix_no_adsense(c, path)
                if ok:
                    c, ok2 = fix_no_ad_slot(c)
                    
                    # 检查ad-slot没有被错误插入到head中
                    head_end = c.find('</head>')
                    ad_pos = c.find('ad-slot')
                    if ad_pos > 0 and ad_pos < head_end:
                        # 移除head中的ad-slot
                        ad_match = re.search(r'<div class="ad-slot">.*?</div>', c[:head_end], re.DOTALL)
                        if ad_match:
                            c = c[:ad_match.start()] + c[ad_match.end():]
                            # 重新插入到正确位置
                            c, _ = fix_no_ad_slot(c)
                    
                    page_fixed.append(issue)
                else:
                    print(f"[FAIL] {page_key}: {issue}")
            
            elif issue == 'no_copy_btn':
                c, ok = fix_no_copy_btn(c, lang)
                if ok: page_fixed.append(issue)
                else: print(f"[FAIL] {page_key}: {issue}")
            
            elif issue == 'no_related_tools':
                c, ok = fix_no_related_tools(c, tool, lang, all_tools)
                if ok: page_fixed.append(issue)
                else: print(f"[FAIL] {page_key}: {issue}")
            
            elif issue in ('content_thin', 'content_very_thin'):
                c, ok = fix_content_thin(c, tool, lang, issue)
                if ok: page_fixed.append(issue)
                else: print(f"[FAIL] {page_key}: {issue}")
            
            elif issue == 'title_long':
                c, ok = fix_title_long(c, lang)
                if ok: page_fixed.append(issue)
                else: print(f"[FAIL] {page_key}: {issue}")
        
        if page_fixed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            fixed_count += len(page_fixed)
            print(f"[FIXED] {page_key}: {page_fixed}")
            results.append(f"  {page_key}: {page_fixed}")
    
    print(f"\n---\nTotal: fixed {fixed_count} issues across {len(results)} pages")
    return fixed_count


if __name__ == '__main__':
    main()
