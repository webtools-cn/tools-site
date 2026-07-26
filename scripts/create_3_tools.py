#!/usr/bin/env python3
"""Create 3 new tools: lifestyle-spending-calculator, vitamin-deficiency-checker, medication-dosage-calculator"""
import os

SITE = '/home/chison/tools-site'

tool_cn_templates = {
    'lifestyle-spending-calculator': {
        'icon': '💳',
        'title_cn': '生活支出计算器',
        'title_en': 'Lifestyle Spending Calculator',
        'desc_cn': '免费在线生活支出计算器，帮助追踪和分类您的日常消费。支持50/30/20预算规则，自动计算各项支出占比和储蓄建议。',
        'desc_en': 'Free online Lifestyle Spending Calculator to track and categorize daily expenses. Supports 50/30/20 budgeting rule with automatic spending breakdown and savings recommendations.',
        'keywords_cn': '生活支出计算器,消费追踪,预算管理,50/30/20预算,支出分析',
        'keywords_en': 'lifestyle spending calculator,expense tracker,budgeting,50/30/20 budget,spending analysis',
        'fields': [
            ('monthlyIncome', '月收入 ($)', 'Monthly Income ($)', '5000', '月税后收入', 'Monthly after-tax income'),
            ('housing', '住房支出 ($)', 'Housing ($)', '1500', '房租/房贷', 'Rent/mortgage'),
            ('food', '餐饮支出 ($)', 'Food ($)', '600', '每月餐饮总支出', 'Monthly food total'),
            ('transport', '交通出行 ($)', 'Transport ($)', '300', '油费/公交/打车', 'Gas/transit/rides'),
            ('entertainment', '休闲娱乐 ($)', 'Entertainment ($)', '400', '娱乐/订阅/旅行', 'Fun/subscriptions/travel'),
            ('savings', '储蓄投资 ($)', 'Savings & Investment ($)', '500', '存款/理财/投资', 'Savings/investment'),
        ],
        'results': [
            ('totalSpending', '总支出', 'Total Spending', '所有类别支出总和', 'Sum of all categories'),
            ('spendingRate', '支出率', 'Spending Rate', '总支出/收入×100%', 'Spending / Income × 100%'),
            ('disposable', '可支配余额', 'Disposable Balance', '收入-总支出', 'Income - Spending'),
            ('needsRatio', '必要支出占比', 'Needs Ratio', '住房+餐饮+交通占比', 'Housing + Food + Transport %'),
            ('wantsRatio', '非必要支出占比', 'Wants Ratio', '娱乐等消费占比', 'Entertainment etc. %'),
            ('savingsRatio', '储蓄率', 'Savings Rate', '储蓄/收入×100%', 'Savings / Income × 100%'),
        ],
        'faq_cn': [
            ('50/30/20预算规则是什么？','50/30/20规则将税后收入分为三部分：50%用于必要支出(住房/餐饮/交通)、30%用于非必要支出(娱乐/旅行)、20%用于储蓄和投资。此计算器自动分析您的支出是否符合此规则。'),
            ('合理的储蓄率是多少？','一般建议储蓄率至少20%。年轻人可以更低(10-15%)，接近退休应更高(30-50%)。FIRE运动追随者通常保持50%+储蓄率。'),
            ('如何降低必要支出占比？','考虑搬家到租金更低地区、合租、减少外食、使用公共交通。必要支出是最难削减的，长期规划比短期节省更有效。'),
        ],
        'faq_en': [
            ('What is the 50/30/20 budgeting rule?','The 50/30/20 rule divides after-tax income: 50% for needs (housing/food/transport), 30% for wants (entertainment/travel), 20% for savings and investment. This calculator analyzes your spending against this rule.'),
            ('What is a reasonable savings rate?','Generally 20% savings rate is recommended. Younger people can get away with 10-15%; those near retirement should target 30-50%. FIRE movement followers often maintain 50%+ savings rates.'),
            ('How to reduce needs spending ratio?','Consider moving to lower-rent areas, getting roommates, eating out less, using public transit. Needs are hardest to cut — long-term planning beats short-term saving.'),
        ],
    },
    'vitamin-deficiency-checker': {
        'icon': '💊',
        'title_cn': '维生素缺乏检测工具',
        'title_en': 'Vitamin Deficiency Checker',
        'desc_cn': '免费的维生素缺乏症状自查工具。选择症状快速获得可能的维生素缺乏建议。仅供信息参考，不替代专业医学诊断。',
        'desc_en': 'Free online vitamin deficiency symptom checker. Select symptoms to get possible vitamin deficiency suggestions. For informational purposes only; not a substitute for professional medical diagnosis.',
        'keywords_cn': '维生素缺乏,症状自查,营养缺乏,维生素检测,健康自查',
        'keywords_en': 'vitamin deficiency,symptom checker,nutritional deficiency,vitamin test,health check',
        'fields': [
            ('symptom1', '疲劳/无力', 'Fatigue/Weakness', '', ''),
            ('symptom2', '皮肤干燥/脱皮', 'Dry/Peeling Skin', '', ''),
            ('symptom3', '口腔溃疡', 'Mouth Ulcers', '', ''),
            ('symptom4', '脱发/头发稀疏', 'Hair Loss/Thinning', '', ''),
            ('symptom5', '视力模糊/夜盲', 'Blurry Vision/Night Blindness', '', ''),
            ('symptom6', '肌肉抽筋/痉挛', 'Muscle Cramps/Spasms', '', ''),
        ],
        'results': [
            ('primaryResult', '主要可能缺乏', 'Primary Possible Deficiency', '', ''),
            ('secondaryResult', '次要可能缺乏', 'Secondary Possible Deficiency', '', ''),
            ('recommendation', '饮食建议', 'Dietary Recommendation', '', ''),
        ],
        'faq_cn': [
            ('这个工具能替代医学诊断吗？','不能。此工具仅供健康知识普及，不构成医学建议。如有健康问题请咨询医生并进行血液检测。'),
            ('如何确认是否缺乏某种维生素？','唯一准确的方法是血液检测。常见检测包括维生素D、B12、铁蛋白、叶酸等。此工具仅基于症状提供可能方向。'),
        ],
        'faq_en': [
            ('Can this tool replace medical diagnosis?','No. This tool is for health knowledge only and does not constitute medical advice. Consult a doctor and get blood tests for health concerns.'),
            ('How to confirm a vitamin deficiency?','The only accurate method is blood testing. Common tests include Vitamin D, B12, ferritin, folate. This tool provides possible directions based on symptoms only.'),
        ],
    },
    'medication-dosage-calculator': {
        'icon': '⚕️',
        'title_cn': '药物剂量计算器',
        'title_en': 'Medication Dosage Calculator',
        'desc_cn': '免费在线药物剂量计算器，按体重计算常用药物的推荐剂量。支持儿童和成人模式。仅供参考，实际用药请遵医嘱。',
        'desc_en': 'Free online medication dosage calculator to calculate weight-based recommended dosage for common medications. Supports pediatric and adult modes. For reference only; always follow medical advice.',
        'keywords_cn': '药物剂量计算,按体重给药,儿童用药剂量,成人用药剂量,药品剂量计算',
        'keywords_en': 'medication dosage calculator,weight-based dosing,pediatric dosage,adult dosage,drug dose calculation',
        'fields': [
            ('weight', '体重 (kg)', 'Weight (kg)', '70', '患者体重公斤数', 'Patient weight in kilograms'),
            ('mode', '', '', '', ''),
            ('drugType', '', '', '', ''),
        ],
        'results': [
            ('singleDose', '单次剂量', 'Single Dose', '', ''),
            ('dailyDose', '每日总剂量', 'Daily Total Dose', '', ''),
            ('maxDailyDose', '每日最大安全剂量', 'Max Safe Daily Dose', '', ''),
        ],
        'faq_cn': [
            ('此计算结果可以替代医嘱吗？','绝对不行。此工具仅提供参考信息。实际用药剂量须严格遵从医生处方或药品说明书。'),
            ('儿童剂量如何计算？','儿童剂量通常按体重(kg)计算，部分药物按体表面积。此计算器提供基于体重的估算。务必确认药品说明书的年龄限制。'),
        ],
        'faq_en': [
            ('Can this replace medical advice?','Absolutely not. This tool provides reference information only. Always follow your doctor\'s prescription or the medication label.'),
            ('How is pediatric dosage calculated?','Pediatric dosage is typically weight-based (mg/kg), some by body surface area. This calculator provides weight-based estimates. Always verify age restrictions on the medication label.'),
        ],
    },
}

# Create CN pages
for slug, t in tool_cn_templates.items():
    cn_dir = os.path.join(SITE, slug)
    en_dir = os.path.join(SITE, 'en', slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    icon = t['icon']
    title_cn = t['title_cn']
    fields = t['fields']
    results = t['results']
    faq_cn = t['faq_cn']
    
    # Build CN page
    fields_html = ''
    for f in fields:
        fid, label, _, default, hint = f[0], f[1], f[2], f[3], f[4]
        if fid == 'symptom1' or fid == 'symptom2':
            # Checkbox fields
            fields_html += f'''<div class="input-group">
<label><input type="checkbox" id="{fid}" style="width:auto;margin-right:8px;">{label}</label>
<div class="hint">{hint}</div>
</div>
'''
        elif fid == 'mode':
            fields_html += f'''<div class="input-group">
<label for="mode">计算模式</label>
<select id="mode"><option value="adult">成人</option><option value="child">儿童</option></select>
<div class="hint">选择成人或儿童模式</div>
</div>
'''
        elif fid == 'drugType':
            fields_html += f'''<div class="input-group">
<label for="drugType">药物类型</label>
<select id="drugType"><option value="acetaminophen">对乙酰氨基酚 (10-15mg/kg)</option><option value="ibuprofen">布洛芬 (5-10mg/kg)</option><option value="amoxicillin">阿莫西林 (20-50mg/kg/天)</option></select>
<div class="hint">选择常用药物</div>
</div>
'''
        else:
            fields_html += f'''<div class="input-group">
<label for="{fid}">{label}</label>
<input type="number" id="{fid}" value="{default}" min="0" step="1">
<div class="hint">{hint}</div>
</div>
'''
    
    results_html = ''
    for r in results:
        rlabel_en, rlabel_cn = r[0], r[1]
        rsub_en, rsub_cn = r[3], r[3]
        if r == results[0]:
            results_html += f'''<div class="result-card highlight">
<div class="label">{rlabel_cn}</div>
<div class="value" id="{rlabel_en}">-</div>
<div class="sub">{rsub_cn}</div>
</div>
'''
        else:
            results_html += f'''<div class="result-card">
<div class="label">{rlabel_cn}</div>
<div class="value" id="{rlabel_en}">-</div>
<div class="sub">{rsub_cn}</div>
</div>
'''
    
    faq_html = ''
    for i, (q, a) in enumerate(faq_cn):
        faq_html += f'''<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>
'''
    
    # Custom JS per tool
    if slug == 'lifestyle-spending-calculator':
        js = """
function calculate() {
    var income = parseFloat(document.getElementById('monthlyIncome').value) || 0;
    var housing = parseFloat(document.getElementById('housing').value) || 0;
    var food = parseFloat(document.getElementById('food').value) || 0;
    var transport = parseFloat(document.getElementById('transport').value) || 0;
    var entertainment = parseFloat(document.getElementById('entertainment').value) || 0;
    var savings = parseFloat(document.getElementById('savings').value) || 0;
    var totalSpending = housing + food + transport + entertainment + savings;
    var disposable = income - totalSpending;
    var spendingRate = income > 0 ? (totalSpending / income) * 100 : 0;
    var needsRatio = income > 0 ? ((housing + food + transport) / income) * 100 : 0;
    var wantsRatio = income > 0 ? (entertainment / income) * 100 : 0;
    var savingsRatio = income > 0 ? (savings / income) * 100 : 0;
    document.getElementById('totalSpending').textContent = '$' + totalSpending.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('spendingRate').textContent = spendingRate.toFixed(1) + '%';
    document.getElementById('disposable').textContent = '$' + disposable.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('needsRatio').textContent = needsRatio.toFixed(1) + '%';
    document.getElementById('wantsRatio').textContent = wantsRatio.toFixed(1) + '%';
    document.getElementById('savingsRatio').textContent = savingsRatio.toFixed(1) + '%';
    document.getElementById('resultsSection').style.display = 'block';
}
"""
    elif slug == 'vitamin-deficiency-checker':
        js = """
var symptomMap = {
    'symptom1': {v: ['维生素B12', '铁(贫血)'], f: ['红肉/肝脏/蛋类', '红肉/菠菜/豆类']},
    'symptom2': {v: ['维生素A', '维生素E', '必需脂肪酸'], f: ['胡萝卜/红薯/菠菜', '坚果/种子/植物油', '深海鱼/亚麻籽']},
    'symptom3': {v: ['维生素B2', '维生素B12', '叶酸'], f: ['奶制品/蛋类/绿叶蔬菜', '红肉/肝脏/蛋类', '绿叶蔬菜/豆类/柑橘']},
    'symptom4': {v: ['铁', '锌', '生物素'], f: ['红肉/菠菜/豆类', '牡蛎/牛肉/南瓜籽', '蛋类/坚果/红薯']},
    'symptom5': {v: ['维生素A'], f: ['胡萝卜/红薯/菠菜/肝脏']},
    'symptom6': {v: ['镁', '钾', '钙'], f: ['坚果/黑巧克力/绿叶蔬菜', '香蕉/土豆/牛油果', '奶制品/豆腐/小鱼干']},
};
function calculate() {
    var selected = [];
    var foods = [];
    for (var i = 1; i <= 6; i++) {
        if (document.getElementById('symptom' + i).checked) {
            var s = symptomMap['symptom' + i];
            selected = selected.concat(s.v);
            foods = foods.concat(s.f);
        }
    }
    if (selected.length === 0) {
        document.getElementById('primaryResult').textContent = '请选择症状';
        document.getElementById('secondaryResult').textContent = '-';
        document.getElementById('recommendation').textContent = '请至少勾选一个症状';
        document.getElementById('resultsSection').style.display = 'block';
        return;
    }
    // Count frequencies
    var count = {};
    for (var j = 0; j < selected.length; j++) {
        count[selected[j]] = (count[selected[j]] || 0) + 1;
    }
    var sorted = Object.keys(count).sort(function(a,b){return count[b]-count[a];});
    var uniqueFoods = [];
    for (var k = 0; k < foods.length; k++) {
        if (uniqueFoods.indexOf(foods[k]) === -1) uniqueFoods.push(foods[k]);
    }
    document.getElementById('primaryResult').textContent = sorted[0] || '-';
    document.getElementById('secondaryResult').textContent = sorted[1] || '无';
    document.getElementById('recommendation').textContent = uniqueFoods.slice(0,3).join(' / ') || '请咨询医生';
    document.getElementById('resultsSection').style.display = 'block';
}
"""
    elif slug == 'medication-dosage-calculator':
        js = """
var drugData = {
    'acetaminophen': {singleMin: 10, singleMax: 15, dailyMax: 75, unit: 'mg/kg'},
    'ibuprofen': {singleMin: 5, singleMax: 10, dailyMax: 40, unit: 'mg/kg'},
    'amoxicillin': {singleMin: 20, singleMax: 50, dailyMax: 90, unit: 'mg/kg/day'},
};
function calculate() {
    var weight = parseFloat(document.getElementById('weight').value) || 0;
    var mode = document.getElementById('mode').value;
    var drug = document.getElementById('drugType').value;
    var d = drugData[drug];
    // Child mode: lower end of range
    var factor = mode === 'child' ? 0.75 : 1;
    var singleLow = Math.round(weight * d.singleMin * factor);
    var singleHigh = Math.round(weight * d.singleMax * factor);
    var daily = Math.round(weight * d.dailyMax * factor);
    document.getElementById('singleDose').textContent = singleLow + ' - ' + singleHigh + ' mg';
    document.getElementById('dailyDose').textContent = daily + ' mg';
    document.getElementById('maxDailyDose').textContent = daily + ' mg/天 (请勿超过)';
    document.getElementById('resultsSection').style.display = 'block';
}
"""
    
    reset_js = ""
    if slug == 'vitamin-deficiency-checker':
        reset_js = "for (var i=1;i<=6;i++){document.getElementById('symptom'+i).checked=false;}document.getElementById('resultsSection').style.display='none';"
    elif slug == 'medication-dosage-calculator':
        reset_js = "document.getElementById('weight').value='70';document.getElementById('mode').value='adult';document.getElementById('drugType').value='acetaminophen';document.getElementById('resultsSection').style.display='none';"
    else:
        reset_js = "document.getElementById('monthlyIncome').value='5000';document.getElementById('housing').value='1500';document.getElementById('food').value='600';document.getElementById('transport').value='300';document.getElementById('entertainment').value='400';document.getElementById('savings').value='500';document.getElementById('resultsSection').style.display='none';"
    
    cn_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['desc_cn']}">
<meta name="keywords" content="{t['keywords_cn']}">
<title>{title_cn} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{title_cn} - Free ToolBase">
<meta property="og:description" content="{t['desc_cn']}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title_cn}","description":"{t['desc_cn']}","applicationCategory":"FinanceApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用 {title_cn}","description":"使用步骤指南","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{title_cn}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入数据","text":"输入相关参数"}},{{"@type":"HowToStep","position":2,"name":"选择选项","text":"根据需要选择模式或参数"}},{{"@type":"HowToStep","position":3,"name":"计算","text":"点击计算按钮查看结果"}},{{"@type":"HowToStep","position":4,"name":"查看结果","text":"查看详细计算结果"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{title_cn}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {title_cn}</h1><div class="lang-switch"><a href="index.html" class="active">ZH</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {title_cn}</p>
<div class="hero"><p>{t['desc_cn']} | 无需注册 · 数据不离设备</p><span class="badge">零依赖 · 离线可用</span></div>
<div class="calculator-section" id="calcSection">
    <h2>🔢 输入参数</h2>
    <div class="input-grid" id="inputGrid">
{fields_html}
    </div>
    <div class="btn-row">
        <button class="btn btn-primary" onclick="calculate()">🧮 计算</button>
        <button class="btn btn-secondary" onclick="resetAll()">🔄 重置</button>
    </div>
</div>
<div class="calculator-section" id="resultsSection" style="display:none">
    <h2>📊 计算结果</h2>
    <div class="results-grid" id="resultsGrid">
{results_html}
    </div>
</div>
<div class="info-section">
    <h2>📖 使用说明</h2>
    <p>{t['desc_cn']}</p>
</div>
<div class="info-section">
    <h2>❓ 常见问题</h2>
{faq_html}
</div>
<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins></div>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px"><a href="../index.html">首页</a><a href="../index.html">全部工具</a><a href="mailto:dexshuang@google.com">联系</a><a href="../privacy/">隐私</a><a href="../terms/">条款</a><a href="../about/">关于</a><a href="../en/{slug}/">EN</a></div>
<p>{title_cn} | 无需注册 · 数据不离设备</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">反馈: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#06b6d4;text-decoration:none}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}.header h1{{font-size:1.6rem;color:#f1f5f9}}.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}.hero{{margin-bottom:16px}}.hero p{{color:#94a3b8;font-size:.95rem}}.badge{{display:inline-block;margin-top:8px;padding:4px 12px;background:rgba(34,211,238,.1);color:#22d3ee;border-radius:20px;font-size:.8rem;border:1px solid rgba(34,211,238,.2)}}.input-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}@media(max-width:640px){{.input-grid{{grid-template-columns:1fr}}}}.input-group{{background:#1e293b;border-radius:12px;padding:16px;border:1px solid rgba(148,163,184,.1)}}.input-group label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:8px}}.input-group input,.input-group select{{width:100%;padding:10px 12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;transition:border-color .2s}}.input-group input:focus,.input-group select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}.input-group .hint{{font-size:.8rem;color:#64748b;margin-top:4px}}.calculator-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.calculator-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}.btn{{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}}.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}.btn-primary:hover{{background:rgba(6,182,212,.3)}}.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}.btn-secondary:hover{{background:rgba(148,163,184,.2)}}.results-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}}@media(max-width:640px){{.results-grid{{grid-template-columns:1fr}}}}.result-card{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:10px;padding:16px;text-align:center}}.result-card .label{{font-size:.85rem;color:#94a3b8;margin-bottom:4px}}.result-card .value{{font-size:1.4rem;color:#22d3ee;font-weight:600}}.result-card .sub{{font-size:.8rem;color:#64748b;margin-top:4px}}.result-card.highlight{{border-color:rgba(34,211,238,.3);background:rgba(34,211,238,.05)}}.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}.faq-item{{margin-bottom:16px}}.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}.faq-item p{{color:#94a3b8;font-size:.9rem}}.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}.toast.show{{opacity:1}}.ad-slot{{margin:0 auto 24px;text-align:center;max-width:960px;min-height:90px}}</style>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("已复制")}})["catch"](function(){{showToast("复制失败")}})}}
{js}
function resetAll() {{ {reset_js} }}
</script>
</body>
</html>'''
    
    with open(os.path.join(cn_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f"  Created CN: {slug}/index.html")

print("Done creating CN pages!")
