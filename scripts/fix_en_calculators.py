#!/usr/bin/env python3
"""Fix 8 EN calculator pages: translate all Chinese, replace placeholders, fix calc output."""

import re

# Tool configurations: EN translations
TOOLS = {
    'apr-calculator': {
        'name': 'APR Calculator',
        'title': 'APR Calculator — Free ToolBase',
        'desc': 'Calculate the true Annual Percentage Rate (APR) of a loan including fees and interest. Know your real borrowing cost.',
        'subtitle': 'Calculate the true Annual Percentage Rate (APR) of a loan including fees and interest.',
        'seo_h2': 'About APR Calculator',
        'seo_intro': 'The APR Calculator is a free online tool that computes the true Annual Percentage Rate (APR) of a loan, factoring in both the nominal interest rate and any origination fees. APR gives you the real cost of borrowing, making it easy to compare different loan offers. Works on mobile and desktop — all calculations run locally in your browser, so your data never leaves your device.',
        'steps': [
            'Enter the loan amount you plan to borrow',
            'Enter the nominal annual interest rate and any origination fee percentage',
            'Click "Calculate" to see the true APR',
        ],
        'calc_output': '"Effective APR: <b>"+apr.toFixed(2)+"%</b><br>Net Loan Amount: <b>"+net.toFixed(0)+"</b><br>Origination Fee: <b>"+fee.toFixed(0)+"</b>"',
        'faq': [
            ('What is APR and why is it different from the interest rate?', 'APR (Annual Percentage Rate) includes both the interest rate and any additional fees, giving you the true annual cost of borrowing. The nominal interest rate only reflects the interest charged, not fees.'),
            ('How is APR calculated?', 'APR is calculated by amortizing the loan (after deducting fees) at the nominal monthly rate, then expressing the total annual cost as a percentage of the net amount received.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up, no download — just open and use. All calculations happen in your browser.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'tip-calculator': {
        'name': 'Tip Calculator',
        'title': 'Tip Calculator — Free ToolBase',
        'desc': 'Quickly calculate tips and split the bill among friends. Supports custom tip percentages and group splitting.',
        'subtitle': 'Quickly calculate tips and split the bill among friends.',
        'seo_h2': 'About Tip Calculator',
        'seo_intro': 'The Tip Calculator is a free online tool that helps you calculate tips at restaurants and split the total among your group. Simply enter the bill amount, choose a tip percentage, and specify how many people are splitting — the calculator does the rest. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter the total bill amount',
            'Set the tip percentage you want to leave',
            'Enter how many people are splitting the bill, then click "Calculate"',
        ],
        'calc_output': '"Tip: <b>"+tip.toFixed(2)+"</b><br>Total: <b>"+total.toFixed(2)+"</b><br>Per Person: <b>"+per.toFixed(2)+"</b>"',
        'faq': [
            ('What is a standard tip percentage?', 'In the US, 15-20% is standard for good service. 18% is a common default. In many other countries, tipping customs vary — adjust accordingly.'),
            ('How is the per-person amount calculated?', 'The per-person amount is the total (bill + tip) divided by the number of people splitting. If you enter 0 for people, the full total is shown.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed — just open and use.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'discount-calculator': {
        'name': 'Discount Calculator',
        'title': 'Discount Calculator — Free ToolBase',
        'desc': 'Calculate the final price after discounts and how much you save. Supports percentage discounts and additional fixed-amount off.',
        'subtitle': 'Calculate the final price after discounts and how much you save.',
        'seo_h2': 'About Discount Calculator',
        'seo_intro': 'The Discount Calculator is a free online tool that computes the final price after applying a percentage discount and any additional fixed-amount reduction. Perfect for shopping sales, comparing deals, and knowing exactly how much you save. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter the original price of the item',
            'Enter the discount percentage (e.g. 25 for 25% off)',
            'Add any extra fixed-amount off, then click "Calculate"',
        ],
        'calc_output': '"Final Price: <b>"+Math.max(0,final).toFixed(2)+"</b><br>You Save: <b>"+saved.toFixed(2)+"</b>"',
        'faq': [
            ('How is the final price calculated?', 'The final price equals the original price minus the percentage discount, minus any additional fixed-amount off. The result is never negative.'),
            ('Can I use this for stacked discounts?', 'This calculator supports one percentage discount plus one fixed-amount reduction. For multiple percentage discounts, calculate them one at a time.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'commission-calculator': {
        'name': 'Commission Calculator',
        'title': 'Commission Calculator — Free ToolBase',
        'desc': 'Calculate sales commission earnings based on sales amount, commission rate, and base salary.',
        'subtitle': 'Calculate sales commission earnings based on sales amount, commission rate, and base salary.',
        'seo_h2': 'About Commission Calculator',
        'seo_intro': 'The Commission Calculator is a free online tool that computes your commission earnings from sales. Enter your sales amount, commission rate, and base salary to see your total income. Perfect for sales professionals, real estate agents, and anyone working on commission-based pay. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter your total sales amount',
            'Enter your commission rate as a percentage',
            'Enter your base salary, then click "Calculate"',
        ],
        'calc_output': '"Commission: <b>"+comm.toFixed(2)+"</b><br>Total Income: <b>"+total.toFixed(2)+"</b>"',
        'faq': [
            ('How is commission calculated?', 'Commission equals the sales amount multiplied by the commission rate (as a percentage). Total income adds your base salary to the commission.'),
            ('Can I use this for tiered commission rates?', 'This calculator uses a single flat commission rate. For tiered rates, calculate each tier separately and add the results.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'fuel-cost-calculator': {
        'name': 'Fuel Cost Calculator',
        'title': 'Fuel Cost Calculator — Free ToolBase',
        'desc': 'Calculate trip fuel costs based on distance, fuel consumption, and fuel price. Supports round-trip calculation.',
        'subtitle': 'Calculate trip fuel costs based on distance, fuel consumption, and fuel price.',
        'seo_h2': 'About Fuel Cost Calculator',
        'seo_intro': 'The Fuel Cost Calculator is a free online tool that estimates how much a trip will cost in fuel. Enter the one-way distance, your vehicle\'s fuel consumption (L/100km), and the fuel price per liter to see the one-way and round-trip costs. Perfect for road trip planning and budgeting. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter the one-way distance of your trip in kilometers',
            'Enter your vehicle\'s fuel consumption (L/100km)',
            'Enter the fuel price per liter, then click "Calculate"',
        ],
        'calc_output': '"One-way Fuel: <b>"+fuel.toFixed(1)+" L</b><br>One-way Cost: <b>"+cost.toFixed(2)+"</b><br>Round-trip Cost: <b>"+(cost*2).toFixed(2)+"</b>"',
        'faq': [
            ('How is fuel cost calculated?', 'Fuel used equals distance divided by 100, multiplied by the consumption rate (L/100km). Cost equals fuel used multiplied by the price per liter.'),
            ('Does this support round-trip calculation?', 'Yes, the calculator shows both one-way and round-trip costs. The round-trip is simply double the one-way cost.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'electricity-cost-calculator': {
        'name': 'Electricity Cost Calculator',
        'title': 'Electricity Cost Calculator — Free ToolBase',
        'desc': 'Calculate daily, monthly, and yearly electricity costs based on appliance power, usage hours, and electricity rate.',
        'subtitle': 'Calculate daily, monthly, and yearly electricity costs for any appliance.',
        'seo_h2': 'About Electricity Cost Calculator',
        'seo_intro': 'The Electricity Cost Calculator is a free online tool that estimates how much an appliance costs to run. Enter the power rating in watts, daily usage hours, and your electricity rate per kWh to see daily, monthly, and yearly costs. Perfect for managing energy expenses. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter the appliance power rating in watts',
            'Enter the daily usage hours',
            'Enter your electricity rate per kWh, then click "Calculate"',
        ],
        'calc_output': '"Daily Cost: <b>"+daily.toFixed(2)+"</b><br>Monthly Cost: <b>"+monthly.toFixed(2)+"</b><br>Yearly Cost: <b>"+yearly.toFixed(2)+"</b>"',
        'faq': [
            ('How is electricity cost calculated?', 'Daily energy used (kWh) equals watts times hours divided by 1000. Daily cost equals kWh times the rate. Monthly = daily × 30, yearly = daily × 365.'),
            ('Why use 30 days for monthly?', 'For simplicity, the calculator uses 30 days per month. For precise billing cycles, multiply the daily cost by your actual billing days.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'body-fat-calculator': {
        'name': 'Body Fat Calculator',
        'title': 'Body Fat Calculator — Free ToolBase',
        'desc': 'Estimate your body fat percentage using the U.S. Navy method based on height, weight, and waist measurements.',
        'subtitle': 'Estimate your body fat percentage using the U.S. Navy method.',
        'seo_h2': 'About Body Fat Calculator',
        'seo_intro': 'The Body Fat Calculator is a free online tool that estimates your body fat percentage using the U.S. Navy method. By entering your height, weight, and waist circumference, you can get an approximation of your body fat percentage, fat mass, and lean body mass. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter your height in centimeters',
            'Enter your weight in kilograms',
            'Enter your waist circumference in cm, then click "Calculate"',
        ],
        'calc_output': '"Estimated Body Fat: <b>"+bf.toFixed(1)+"%</b><br>Fat Mass: <b>"+(b*bf/100).toFixed(1)+" kg</b><br>Lean Mass: <b>"+(b*(1-bf/100)).toFixed(1)+" kg</b>"',
        'faq': [
            ('What is the U.S. Navy method?', 'The U.S. Navy method estimates body fat using circumference measurements. This simplified version uses height and waist circumference for a quick approximation.'),
            ('How accurate is this calculator?', 'This calculator provides an estimate based on a formula. For precise body composition analysis, consult a healthcare professional or use methods like DEXA scans.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
            ('Is my data safe?', 'Absolutely. All calculations run locally in your browser. No data is uploaded to any server.'),
        ],
    },
    'calorie-calculator': {
        'name': 'Daily Calorie Calculator',
        'title': 'Daily Calorie Calculator — Free ToolBase',
        'desc': 'Calculate your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on weight, height, and age.',
        'subtitle': 'Calculate your BMR and daily calorie needs based on your body metrics.',
        'seo_h2': 'About Daily Calorie Calculator',
        'seo_intro': 'The Daily Calorie Calculator is a free online tool that estimates your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) at different activity levels. Using the Mifflin-St Jeor equation, it calculates how many calories you need to maintain your weight based on your weight, height, and age. Works on mobile and desktop, all calculations run locally in your browser.',
        'steps': [
            'Enter your weight in kilograms',
            'Enter your height in centimeters',
            'Enter your age, then click "Calculate"',
        ],
        'calc_output': '"BMR: <b>"+bmr.toFixed(0)+" kcal</b><br>Sedentary: <b>"+tdee_sedentary.toFixed(0)+"</b> | Moderate: <b>"+tdee_moderate.toFixed(0)+"</b><br>Very Active: <b>"+tdee_active.toFixed(0)+" kcal</b>"',
        'faq': [
            ('What is BMR?', 'BMR (Basal Metabolic Rate) is the number of calories your body burns at rest to maintain basic functions like breathing and circulation.'),
            ('What is TDEE?', 'TDEE (Total Daily Energy Expenditure) is your BMR multiplied by an activity factor. Sedentary = 1.2, Moderate = 1.55, Very Active = 1.9.'),
            ('Which formula is used?', 'This calculator uses the Mifflin-St Jeor equation, one of the most widely recommended formulas for estimating BMR.'),
            ('Is this calculator free?', 'Yes, completely free. No sign-up or download needed.'),
        ],
    },
}

def build_faq_html(faq_items):
    html = '<div class="faq">\n'
    for q, a in faq_items:
        html += f'<h3>{q}</h3>\n<p>{a}</p>\n'
    html += '</div>'
    return html

def build_faq_json(faq_items):
    items = []
    for q, a in faq_items:
        items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    return '[' + ','.join(items) + ']'

def build_en_page(tool, config):
    # Read current EN page to preserve form HTML and calc logic structure
    html = open(f'en/{tool}/index.html').read()
    
    # Extract form labels and placeholders (already in English)
    form_match = re.search(r'<div class="card">(.*?)</div>\s*<div class="result"', html, re.DOTALL)
    form_html = form_match.group(1) if form_match else ''
    
    # Extract the calc function's variable computation (before the innerHTML assignment)
    # We need to replace the Chinese output text with English
    script_match = re.search(r'function calc\(\)\{(.*?)\}function show', html, re.DOTALL)
    calc_body = script_match.group(1) if script_match else ''
    
    # Replace the Chinese innerHTML with English version
    # The pattern is: document.getElementById("rv").innerHTML="Chinese text..."
    calc_body_fixed = re.sub(
        r'document\.getElementById\("rv"\)\.innerHTML=.*?;document\.getElementById\("result"\)',
        f'document.getElementById("rv").innerHTML={config["calc_output"]};document.getElementById("result")',
        calc_body
    )
    
    faq_html = build_faq_html(config['faq'])
    faq_json = build_faq_json(config['faq'])
    
    steps_html = '\n'.join(f'  <li>{s}</li>' for s in config['steps'])
    
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="robots" content="index, follow">
<title>{config['title']}</title>
<meta name="description" content="{config['desc']}">
<meta property="og:title" content="{config['title']}">
<meta property="og:description" content="{config['desc']}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<link rel="canonical" href="https://free-toolbase.com/en/{tool}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{tool}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{tool}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{config['name']}","applicationCategory":"UtilityApplication","operatingSystem":"Web Browser","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{faq_json}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"{config['name']}"}}]}}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-9W1157EBQV')</script>
<style>
:root {{
  --bg: #0f172a;
  --card-bg: #1e293b;
  --text: #e2e8f0;
  --text-secondary: #94a3b8;
  --primary: #06b6d4;
  --primary-hover: #22d3ee;
  --border: rgba(148,163,184,.1);
  --danger: #ef4444;
  --success: #10b981;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; }}
header {{ background: var(--card-bg); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }}
header a {{ color: var(--primary); text-decoration: none; font-weight: 600; font-size: 18px; }}
.lang-switch a {{ padding: 6px 12px; border-radius: 6px; font-size: .85rem; color: var(--text-secondary); border: 1px solid var(--border); }}
.lang-switch a:hover {{ color: var(--primary); border-color: var(--primary); }}
main {{ flex: 1; max-width: 720px; margin: 0 auto; padding: 32px 20px 48px; width: 100%; }}
h1 {{ font-size: 28px; margin-bottom: 8px; text-align: center; }}
.subtitle {{ text-align: center; color: var(--text-secondary); margin-bottom: 28px; }}
.card {{ background: var(--card-bg); border-radius: 12px; padding: 24px; border: 1px solid var(--border); margin-bottom: 20px; }}
.form-group {{ margin-bottom: 16px; }}
.form-group label {{ display: block; font-weight: 600; margin-bottom: 6px; font-size: 14px; color: var(--text-secondary); }}
.form-group input, .form-group select {{ width: 100%; padding: 12px; border: 2px solid var(--border); border-radius: 8px; font-size: 16px; background: var(--bg); color: var(--text); transition: border-color .2s; }}
.form-group input:focus, .form-group select:focus {{ outline: none; border-color: var(--primary); }}
.btn {{ width: 100%; padding: 14px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: 600; background: var(--primary); color: #fff; transition: opacity .2s; }}
.btn:hover {{ opacity: .9; }}
.result {{ background: var(--bg); border-radius: 8px; padding: 20px; margin-top: 20px; border: 1px solid rgba(6,182,212,.2); display: none; }}
.result .val {{ font-size: 36px; font-weight: 700; color: var(--primary); }}
.result .detail {{ color: var(--text-secondary); font-size: .9rem; margin-top: 4px; }}
.seo-section {{ margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); }}
.seo-section h2 {{ font-size: 1.3rem; margin-bottom: 16px; color: var(--text); }}
.seo-section p, .seo-section li {{ color: var(--text-secondary); line-height: 1.7; font-size: .95rem; margin-bottom: 8px; }}
.seo-section ul {{ padding-left: 20px; margin-bottom: 20px; }}
.faq {{ margin-top: 24px; }}
.faq h3 {{ font-size: 1.1rem; color: var(--primary); margin-bottom: 8px; }}
.faq p {{ color: var(--text-secondary); margin-bottom: 16px; }}
.toast {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(100px); background: var(--card-bg); color: #fff; padding: 12px 24px; border-radius: 8px; font-size: 14px; z-index: 9999; opacity: 0; transition: all .3s; pointer-events: none; border: 1px solid var(--border); }}
.toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
footer {{ text-align: center; padding: 24px; color: var(--text-secondary); font-size: 13px; border-top: 1px solid var(--border); margin-top: auto; }}
footer a {{ color: var(--primary); text-decoration: none; }}
footer a:hover {{ text-decoration: underline; }}
@media(max-width:600px) {{ main {{ padding: 20px 12px; }} h1 {{ font-size: 22px; }} .result .val {{ font-size: 28px; }} }}
</style>
</head>
<body>
<header><a href="/">🧰 Free ToolBase</a><div class="lang-switch"><a href="/{tool}/">中文</a></div></header>
<main>
<h1>{config['name']}</h1>
<p class="subtitle">{config['subtitle']}</p>
<div class="card">
{form_html}
<button class="btn" onclick="calc()">🧮 Calculate</button>
</div>
<div class="result" id="result"><div class="val" id="rv">—</div><div class="detail" id="rd"></div></div>

<div class="seo-section">
<h2>{config['seo_h2']}</h2>
<p>{config['seo_intro']}</p>
<h3>How to Use</h3>
<ol>
{steps_html}
</ol>
</div>
{faq_html}
</main>
<footer>
  <div class="footer" style="display:flex;justify-content:center;flex-wrap:wrap;gap:16px;margin-bottom:8px;">
    <a href="../index.html">Home</a>
    <a href="mailto:dexshuang@google.com">Contact Us</a>
    <a href="../privacy/">Privacy Policy</a>
    <a href="../terms/">Terms of Service</a>
    <a href="../about/">About Us</a>
  </div>
  <div>© 2026 Free ToolBase — All calculations run locally in your browser. No data uploaded.</div>
</footer>
<div class="toast" id="toast"></div>
<script>
function calc(){{
{calc_body_fixed}
}}
function show(m){{var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2500)}}
</script>
</body>
</html>
'''
    return page

# Generate all 8 EN pages
for tool, config in TOOLS.items():
    page = build_en_page(tool, config)
    path = f'en/{tool}/index.html'
    with open(path, 'w') as f:
        f.write(page)
    print(f"✅ {tool} EN written ({len(page)} bytes)")

print("\nAll 8 EN pages rewritten!")
