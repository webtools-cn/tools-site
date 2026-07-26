#!/usr/bin/env python3
"""Create EN versions of the 3 new tools"""
import os

SITE = '/home/chison/tools-site'

tool_en_templates = {
    'lifestyle-spending-calculator': {
        'icon': '💳',
        'title': 'Lifestyle Spending Calculator',
        'desc': 'Free online Lifestyle Spending Calculator to track and categorize daily expenses. Supports 50/30/20 budgeting rule with automatic spending breakdown and savings recommendations.',
        'keywords': 'lifestyle spending calculator,expense tracker,budgeting,50/30/20 budget,spending analysis',
        'fields': [
            ('monthlyIncome', 'Monthly Income ($)', '5000', 'Monthly after-tax income'),
            ('housing', 'Housing ($)', '1500', 'Rent/mortgage'),
            ('food', 'Food ($)', '600', 'Monthly food total'),
            ('transport', 'Transport ($)', '300', 'Gas/transit/rides'),
            ('entertainment', 'Entertainment ($)', '400', 'Fun/subscriptions/travel'),
            ('savings', 'Savings & Investment ($)', '500', 'Savings/investment'),
        ],
        'results': [
            ('totalSpending', 'Total Spending', 'Sum of all categories'),
            ('spendingRate', 'Spending Rate', 'Spending / Income × 100%'),
            ('disposable', 'Disposable Balance', 'Income - Spending'),
            ('needsRatio', 'Needs Ratio', 'Housing + Food + Transport %'),
            ('wantsRatio', 'Wants Ratio', 'Entertainment etc. %'),
            ('savingsRatio', 'Savings Rate', 'Savings / Income × 100%'),
        ],
        'faq': [
            ('What is the 50/30/20 budgeting rule?','The 50/30/20 rule divides after-tax income: 50% for needs (housing/food/transport), 30% for wants (entertainment/travel), 20% for savings and investment. This calculator analyzes your spending against this rule.'),
            ('What is a reasonable savings rate?','Generally 20% savings rate is recommended. Younger people can get away with 10-15%; those near retirement should target 30-50%. FIRE movement followers often maintain 50%+ savings rates.'),
            ('How to reduce needs spending ratio?','Consider moving to lower-rent areas, getting roommates, eating out less, using public transit. Needs are hardest to cut — long-term planning beats short-term saving.'),
        ],
        'js': """
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
""",
        'reset': "document.getElementById('monthlyIncome').value='5000';document.getElementById('housing').value='1500';document.getElementById('food').value='600';document.getElementById('transport').value='300';document.getElementById('entertainment').value='400';document.getElementById('savings').value='500';document.getElementById('resultsSection').style.display='none';",
    },
    'vitamin-deficiency-checker': {
        'icon': '💊',
        'title': 'Vitamin Deficiency Checker',
        'desc': 'Free online vitamin deficiency symptom checker. Select symptoms to get possible vitamin deficiency suggestions. For informational purposes only; not a substitute for professional medical diagnosis.',
        'keywords': 'vitamin deficiency,symptom checker,nutritional deficiency,vitamin test,health check',
        'fields': [
            ('symptom1', 'Fatigue/Weakness', '', ''),
            ('symptom2', 'Dry/Peeling Skin', '', ''),
            ('symptom3', 'Mouth Ulcers', '', ''),
            ('symptom4', 'Hair Loss/Thinning', '', ''),
            ('symptom5', 'Blurry Vision/Night Blindness', '', ''),
            ('symptom6', 'Muscle Cramps/Spasms', '', ''),
        ],
        'results': [
            ('primaryResult', 'Primary Possible Deficiency', ''),
            ('secondaryResult', 'Secondary Possible Deficiency', ''),
            ('recommendation', 'Dietary Recommendation', ''),
        ],
        'faq': [
            ('Can this tool replace medical diagnosis?','No. This tool is for health knowledge only and does not constitute medical advice. Consult a doctor and get blood tests for health concerns.'),
            ('How to confirm a vitamin deficiency?','The only accurate method is blood testing. Common tests include Vitamin D, B12, ferritin, folate. This tool provides possible directions based on symptoms only.'),
        ],
        'js': """
var symptomMap = {
    'symptom1': {v: ['Vitamin B12', 'Iron (Anemia)'], f: ['Red meat/liver/eggs', 'Red meat/spinach/legumes']},
    'symptom2': {v: ['Vitamin A', 'Vitamin E', 'Essential Fatty Acids'], f: ['Carrots/sweet potatoes/spinach', 'Nuts/seeds/vegetable oils', 'Deep sea fish/flaxseed']},
    'symptom3': {v: ['Vitamin B2', 'Vitamin B12', 'Folate'], f: ['Dairy/eggs/leafy greens', 'Red meat/liver/eggs', 'Leafy greens/legumes/citrus']},
    'symptom4': {v: ['Iron', 'Zinc', 'Biotin'], f: ['Red meat/spinach/legumes', 'Oysters/beef/pumpkin seeds', 'Eggs/nuts/sweet potatoes']},
    'symptom5': {v: ['Vitamin A'], f: ['Carrots/sweet potatoes/spinach/liver']},
    'symptom6': {v: ['Magnesium', 'Potassium', 'Calcium'], f: ['Nuts/dark chocolate/leafy greens', 'Bananas/potatoes/avocado', 'Dairy/tofu/small fish']},
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
        document.getElementById('primaryResult').textContent = 'Please select symptoms';
        document.getElementById('secondaryResult').textContent = '-';
        document.getElementById('recommendation').textContent = 'Check at least one symptom';
        document.getElementById('resultsSection').style.display = 'block';
        return;
    }
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
    document.getElementById('secondaryResult').textContent = sorted[1] || 'None';
    document.getElementById('recommendation').textContent = uniqueFoods.slice(0,3).join(' / ') || 'Consult a doctor';
    document.getElementById('resultsSection').style.display = 'block';
}
""",
        'reset': "for (var i=1;i<=6;i++){document.getElementById('symptom'+i).checked=false;}document.getElementById('resultsSection').style.display='none';",
    },
    'medication-dosage-calculator': {
        'icon': '⚕️',
        'title': 'Medication Dosage Calculator',
        'desc': 'Free online medication dosage calculator to calculate weight-based recommended dosage for common medications. Supports pediatric and adult modes. For reference only; always follow medical advice.',
        'keywords': 'medication dosage calculator,weight-based dosing,pediatric dosage,adult dosage,drug dose calculation',
        'fields': [
            ('weight', 'Weight (kg)', '70', 'Patient weight in kilograms'),
        ],
        'results': [
            ('singleDose', 'Single Dose', ''),
            ('dailyDose', 'Daily Total Dose', ''),
            ('maxDailyDose', 'Max Safe Daily Dose', ''),
        ],
        'faq': [
            ('Can this replace medical advice?','Absolutely not. This tool provides reference information only. Always follow your doctor\'s prescription or the medication label.'),
            ('How is pediatric dosage calculated?','Pediatric dosage is typically weight-based (mg/kg), some by body surface area. This calculator provides weight-based estimates. Always verify age restrictions on the medication label.'),
        ],
        'js': """
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
    var factor = mode === 'child' ? 0.75 : 1;
    var singleLow = Math.round(weight * d.singleMin * factor);
    var singleHigh = Math.round(weight * d.singleMax * factor);
    var daily = Math.round(weight * d.dailyMax * factor);
    document.getElementById('singleDose').textContent = singleLow + ' - ' + singleHigh + ' mg';
    document.getElementById('dailyDose').textContent = daily + ' mg';
    document.getElementById('maxDailyDose').textContent = daily + ' mg/day (Do not exceed)';
    document.getElementById('resultsSection').style.display = 'block';
}
""",
        'reset': "document.getElementById('weight').value='70';document.getElementById('mode').value='adult';document.getElementById('drugType').value='acetaminophen';document.getElementById('resultsSection').style.display='none';",
    },
}

for slug, t in tool_en_templates.items():
    en_dir = os.path.join(SITE, 'en', slug)
    os.makedirs(en_dir, exist_ok=True)
    
    fields_html = ''
    for f in t['fields']:
        fid, label, default, hint = f[0], f[1], f[2], f[3]
        if 'symptom' in fid:
            fields_html += f'''<div class="input-group">
<label><input type="checkbox" id="{fid}" style="width:auto;margin-right:8px;">{label}</label>
</div>
'''
        elif fid == 'weight':
            fields_html += f'''<div class="input-group">
<label for="{fid}">{label}</label>
<input type="number" id="{fid}" value="{default}" min="0" step="1">
<div class="hint">{hint}</div>
</div>
'''
        else:
            fields_html += f'''<div class="input-group">
<label for="{fid}">{label}</label>
<input type="number" id="{fid}" value="{default}" min="0" step="1">
<div class="hint">{hint}</div>
</div>
'''
    
    # Add mode + drugType selects for medication
    if slug == 'medication-dosage-calculator':
        fields_html += '''<div class="input-group">
<label for="mode">Mode</label>
<select id="mode"><option value="adult">Adult</option><option value="child">Pediatric</option></select>
<div class="hint">Select adult or pediatric mode</div>
</div>
<div class="input-group">
<label for="drugType">Medication</label>
<select id="drugType"><option value="acetaminophen">Acetaminophen (10-15mg/kg)</option><option value="ibuprofen">Ibuprofen (5-10mg/kg)</option><option value="amoxicillin">Amoxicillin (20-50mg/kg/day)</option></select>
<div class="hint">Select common medication</div>
</div>'''
    
    results_html = ''
    for r in t['results']:
        rid, rlabel, rsub = r[0], r[1], r[2]
        if r == t['results'][0]:
            results_html += f'''<div class="result-card highlight">
<div class="label">{rlabel}</div>
<div class="value" id="{rid}">-</div>
<div class="sub">{rsub}</div>
</div>
'''
        else:
            results_html += f'''<div class="result-card">
<div class="label">{rlabel}</div>
<div class="value" id="{rid}">-</div>
<div class="sub">{rsub}</div>
</div>
'''
    
    faq_html = ''
    for q, a in t['faq']:
        faq_html += f'''<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>
'''
    
    en_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['desc']}">
<meta name="keywords" content="{t['keywords']}">
<title>{t['title']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{t['title']} - Free ToolBase">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{t['title']}","description":"{t['desc']}","applicationCategory":"FinanceApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"How to Use {t['title']}","description":"Step-by-step usage guide","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{t['title']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"Enter Data","text":"Enter your parameters"}},{{"@type":"HowToStep","position":2,"name":"Select Options","text":"Choose mode or options as needed"}},{{"@type":"HowToStep","position":3,"name":"Calculate","text":"Click the calculate button to see results"}},{{"@type":"HowToStep","position":4,"name":"View Results","text":"Review detailed calculation results"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['title']}","item":"https://free-toolbase.com/en/{slug}/"}}]}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{t['icon']} {t['title']}</h1><div class="lang-switch"><a href="index.html">ZH</a><a href="../en/{slug}/" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {t['title']}</p>
<div class="hero"><p>{t['desc']} | No Signup · Data Never Leaves Your Device</p><span class="badge">Zero Dependencies · Works Offline</span></div>
<div class="calculator-section" id="calcSection">
    <h2>🔢 Input Parameters</h2>
    <div class="input-grid" id="inputGrid">
{fields_html}
    </div>
    <div class="btn-row">
        <button class="btn btn-primary" onclick="calculate()">🧮 Calculate</button>
        <button class="btn btn-secondary" onclick="resetAll()">🔄 Reset</button>
    </div>
</div>
<div class="calculator-section" id="resultsSection" style="display:none">
    <h2>📊 Results</h2>
    <div class="results-grid" id="resultsGrid">
{results_html}
    </div>
</div>
<div class="info-section">
    <h2>📖 How to Use</h2>
    <p>{t['desc']}</p>
</div>
<div class="info-section">
    <h2>❓ FAQ</h2>
{faq_html}
</div>
<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins></div>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px"><a href="../index.html">Home</a><a href="../index.html">All Tools</a><a href="mailto:dexshuang@google.com">Contact</a><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a><a href="../about/">About</a><a href="../en/{slug}/">EN</a></div>
<p>{t['title']} | No Signup · Data Never Leaves Your Device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#06b6d4;text-decoration:none}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}.header h1{{font-size:1.6rem;color:#f1f5f9}}.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}.hero{{margin-bottom:16px}}.hero p{{color:#94a3b8;font-size:.95rem}}.badge{{display:inline-block;margin-top:8px;padding:4px 12px;background:rgba(34,211,238,.1);color:#22d3ee;border-radius:20px;font-size:.8rem;border:1px solid rgba(34,211,238,.2)}}.input-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}@media(max-width:640px){{.input-grid{{grid-template-columns:1fr}}}}.input-group{{background:#1e293b;border-radius:12px;padding:16px;border:1px solid rgba(148,163,184,.1)}}.input-group label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:8px}}.input-group input,.input-group select{{width:100%;padding:10px 12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;transition:border-color .2s}}.input-group input:focus,.input-group select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}.input-group .hint{{font-size:.8rem;color:#64748b;margin-top:4px}}.calculator-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.calculator-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}.btn{{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}}.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}.btn-primary:hover{{background:rgba(6,182,212,.3)}}.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}.btn-secondary:hover{{background:rgba(148,163,184,.2)}}.results-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}}@media(max-width:640px){{.results-grid{{grid-template-columns:1fr}}}}.result-card{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:10px;padding:16px;text-align:center}}.result-card .label{{font-size:.85rem;color:#94a3b8;margin-bottom:4px}}.result-card .value{{font-size:1.4rem;color:#22d3ee;font-weight:600}}.result-card .sub{{font-size:.8rem;color:#64748b;margin-top:4px}}.result-card.highlight{{border-color:rgba(34,211,238,.3);background:rgba(34,211,238,.05)}}.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}.faq-item{{margin-bottom:16px}}.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}.faq-item p{{color:#94a3b8;font-size:.9rem}}.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}.toast.show{{opacity:1}}.ad-slot{{margin:0 auto 24px;text-align:center;max-width:960px;min-height:90px}}</style>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("Copied")}})["catch"](function(){{showToast("Copy failed")}})}}
{t['js']}
function resetAll() {{ {t['reset']} }}
</script>
</body>
</html>'''
    
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f"  Created EN: en/{slug}/index.html")

print("Done creating EN pages!")