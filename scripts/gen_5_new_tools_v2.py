#!/usr/bin/env python3
"""批量生成5个新工具: CN+EN 共10页"""
import os, json, re

SITE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SITE)  # scripts/.. → tools-site

OG_IMAGE = 'https://free-toolbase.com/og-image.svg'
CN_URL = 'https://free-toolbase.com/'
EN_URL = 'https://free-toolbase.com/en/'

FOOTER_CN = '<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem"><a href="/" style="color:#64748b;margin:0 8px">首页</a> <a href="/privacy" style="color:#64748b;margin:0 8px">隐私政策</a></footer>'
FOOTER_EN = '<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem"><a href="/en/" style="color:#64748b;margin:0 8px">Home</a> <a href="/en/privacy" style="color:#64748b;margin:0 8px">Privacy</a></footer>'

TOOLS = [
    {
        "slug": "medical-cost-estimator",
        "icon": "🏥",
        "cat_cn": "健康计算器",
        "cat_en": "Health Calculators",
        "name_cn": "医疗费用估算器",
        "name_en": "Medical Cost Estimator",
        "desc_cn": "预估各类医疗服务费用，包括门诊、住院、手术、药品等开支，帮助做好医疗预算规划。纯前端计算，数据绝不上传。",
        "desc_en": "Estimate various medical service costs including outpatient, inpatient, surgery, and medication expenses. Plan your healthcare budget. Pure frontend, no data upload.",
        "kw_cn": "医疗费用,看病花费,住院费,手术费,医疗预算,在线工具",
        "kw_en": "medical cost,healthcare cost,hospital bill,surgery cost,medical budget,online tool",
        "inputs": [
            {"id":"serviceType","label_cn":"医疗服务类型","label_en":"Service Type","type":"select","options":[{"v":"outpatient","cn":"门诊","en":"Outpatient"},{"v":"inpatient","cn":"住院","en":"Inpatient"},{"v":"surgery","cn":"手术","en":"Surgery"},{"v":"dental","cn":"牙科","en":"Dental"},{"v":"vision","cn":"眼科","en":"Vision"}],"default":"outpatient"},
            {"id":"visitCount","label_cn":"预计就诊/天数","label_en":"Expected Visits/Days","type":"number","default":"3","min":"1"},
            {"id":"costPerVisit","label_cn":"每次/天费用(元)","label_en":"Cost per Visit/Day ($)","type":"number","default":"500","step":"50"},
            {"id":"medication","label_cn":"药费(元)","label_en":"Medication Cost ($)","type":"number","default":"300","step":"50"},
            {"id":"insuranceCoverage","label_cn":"医保报销比例(%)","label_en":"Insurance Coverage (%)","type":"number","default":"70","min":"0","max":"100"},
        ],
        "calc": """var visits=parseFloat(el('visitCount').value)||0;
var costPer=parseFloat(el('costPerVisit').value)||0;
var med=parseFloat(el('medication').value)||0;
var coverage=parseFloat(el('insuranceCoverage').value)||0;
var totalBefore=visits*costPer+med;
var covered=totalBefore*coverage/100;
var outOfPocket=totalBefore-covered;""",
        "results": [
            {"id":"resTotalBefore","label_cn":"总费用(报销前)","label_en":"Total Cost (Before Insurance)","fmt":"money"},
            {"id":"resCovered","label_cn":"医保报销金额","label_en":"Insurance Covered","fmt":"money"},
            {"id":"resOutOfPocket","label_cn":"自付金额","label_en":"Out-of-Pocket","fmt":"money"},
        ],
    },
    {
        "slug": "pet-insurance-calculator",
        "icon": "🐾",
        "cat_cn": "金融计算器",
        "cat_en": "Finance Calculators",
        "name_cn": "宠物保险费用计算器",
        "name_en": "Pet Insurance Cost Calculator",
        "desc_cn": "计算宠物保险的年费和潜在赔付，对比不同保险方案的成本效益，为爱宠选择最优保障。纯前端计算，数据不上传。",
        "desc_en": "Calculate pet insurance annual premiums and potential reimbursements, compare cost-effectiveness of different plans. Pure frontend, no data upload.",
        "kw_cn": "宠物保险,宠物医保,狗保险,猫保险,宠物医疗险,在线工具",
        "kw_en": "pet insurance,dog insurance,cat insurance,pet health plan,online tool",
        "inputs": [
            {"id":"petType","label_cn":"宠物类型","label_en":"Pet Type","type":"select","options":[{"v":"dog","cn":"🐕 狗","en":"🐕 Dog"},{"v":"cat","cn":"🐈 猫","en":"🐈 Cat"},{"v":"other","cn":"🐹 其他","en":"🐹 Other"}],"default":"dog"},
            {"id":"petAge","label_cn":"宠物年龄(岁)","label_en":"Pet Age (years)","type":"number","default":"3","min":"0","max":"20"},
            {"id":"monthlyPremium","label_cn":"月保费(元)","label_en":"Monthly Premium ($)","type":"number","default":"80","step":"10"},
            {"id":"deductible","label_cn":"年免赔额(元)","label_en":"Annual Deductible ($)","type":"number","default":"500","step":"50"},
            {"id":"reimbursement","label_cn":"报销比例(%)","label_en":"Reimbursement Rate (%)","type":"number","default":"80","min":"10","max":"100"},
            {"id":"annualLimit","label_cn":"年度赔付上限(元)","label_en":"Annual Limit ($)","type":"number","default":"10000","step":"500"},
            {"id":"expectedVetBill","label_cn":"预计年兽医费用(元)","label_en":"Expected Annual Vet Bill ($)","type":"number","default":"2000","step":"100"},
        ],
        "calc": """var premium=parseFloat(el('monthlyPremium').value)||0;
var deduct=parseFloat(el('deductible').value)||0;
var reimb=parseFloat(el('reimbursement').value)||0;
var limit=parseFloat(el('annualLimit').value)||0;
var vetBill=parseFloat(el('expectedVetBill').value)||0;
var annualPremium=premium*12;
var eligible=Math.max(0,vetBill-deduct);
var reimbursed=Math.min(eligible*reimb/100,limit);
var netCost=annualPremium+deduct+(vetBill-reimbursed);
var saved=Math.max(0,vetBill-netCost);""",
        "results": [
            {"id":"resAnnualPremium","label_cn":"年保费","label_en":"Annual Premium","fmt":"money"},
            {"id":"resReimbursed","label_cn":"预计赔付","label_en":"Estimated Reimbursement","fmt":"money"},
            {"id":"resNetCost","label_cn":"净支出(保费+自付)","label_en":"Net Cost (Premium+Out-of-Pocket)","fmt":"money"},
            {"id":"resSaved","label_cn":"相比不投保节省","label_en":"Saved vs No Insurance","fmt":"money"},
        ],
    },
    {
        "slug": "long-term-care-calculator",
        "icon": "👴",
        "cat_cn": "金融计算器",
        "cat_en": "Finance Calculators",
        "name_cn": "长期护理费用计算器",
        "name_en": "Long-Term Care Cost Calculator",
        "desc_cn": "估算养老和长期护理费用，包括居家护理、辅助生活和养老院开支，提前规划退休后的护理保障。纯前端计算。",
        "desc_en": "Estimate long-term care and retirement care costs including in-home care, assisted living, and nursing home expenses. Plan ahead. Pure frontend.",
        "kw_cn": "长期护理,养老费用,养老院,居家护理,退休规划,在线工具",
        "kw_en": "long-term care,retirement care,nursing home,in-home care,retirement planning,online tool",
        "inputs": [
            {"id":"careType","label_cn":"护理类型","label_en":"Care Type","type":"select","options":[{"v":"home","cn":"🏠 居家护理","en":"🏠 In-Home Care"},{"v":"assisted","cn":"🏢 辅助生活","en":"🏢 Assisted Living"},{"v":"nursing","cn":"🏥 养老院","en":"🏥 Nursing Home"}],"default":"home"},
            {"id":"currentAge","label_cn":"当前年龄","label_en":"Current Age","type":"number","default":"60","min":"40","max":"90"},
            {"id":"careStartAge","label_cn":"预计需要护理年龄","label_en":"Expected Care Start Age","type":"number","default":"75","min":"50","max":"95"},
            {"id":"careYears","label_cn":"预计护理年数","label_en":"Expected Care Years","type":"number","default":"10","min":"1","max":"30"},
            {"id":"monthlyCost","label_cn":"当前月护理费用(元)","label_en":"Current Monthly Care Cost ($)","type":"number","default":"5000","step":"500"},
            {"id":"inflation","label_cn":"年通胀率(%)","label_en":"Annual Inflation (%)","type":"number","default":"3","min":"0","max":"10","step":"0.5"},
        ],
        "calc": """var age=parseFloat(el('currentAge').value)||60;
var startAge=parseFloat(el('careStartAge').value)||75;
var years=parseFloat(el('careYears').value)||10;
var monthly=parseFloat(el('monthlyCost').value)||5000;
var infl=parseFloat(el('inflation').value)||3;
var waitYears=Math.max(0,startAge-age);
var futureMonthly=monthly*Math.pow(1+infl/100,waitYears);
var totalCost=0;
for(var y=0;y<years;y++){
  totalCost+=futureMonthly*12*Math.pow(1+infl/100,y);
}""",
        "results": [
            {"id":"resWaitYears","label_cn":"距离需护理还有","label_en":"Years Until Care Needed","fmt":"years"},
            {"id":"resFutureMonthly","label_cn":"届时月护理费","label_en":"Future Monthly Cost","fmt":"money"},
            {"id":"resTotalCost","label_cn":"总护理费用","label_en":"Total Care Cost","fmt":"money"},
        ],
    },
    {
        "slug": "gig-economy-tax-calculator",
        "icon": "🧾",
        "cat_cn": "金融计算器",
        "cat_en": "Finance Calculators",
        "name_cn": "零工经济税务计算器",
        "name_en": "Gig Economy Tax Calculator",
        "desc_cn": "计算自由职业和零工收入的应缴税款，考虑自雇税、业务扣除和季度预估税，帮您合理规划税务。纯前端计算。",
        "desc_en": "Calculate taxes for freelance and gig income, accounting for self-employment tax, business deductions, and quarterly estimates. Pure frontend.",
        "kw_cn": "零工税,自由职业税,自雇税,1099税,季度税,在线工具",
        "kw_en": "gig tax,freelance tax,self-employment tax,1099 tax,quarterly tax,online tool",
        "inputs": [
            {"id":"gigIncome","label_cn":"零工总收入(元)","label_en":"Total Gig Income ($)","type":"number","default":"50000","step":"1000"},
            {"id":"businessExpenses","label_cn":"业务扣除(元)","label_en":"Business Expenses ($)","type":"number","default":"10000","step":"500"},
            {"id":"otherIncome","label_cn":"其他收入(元)","label_en":"Other Income ($)","type":"number","default":"0","step":"500"},
            {"id":"taxRate","label_cn":"边际税率(%)","label_en":"Marginal Tax Rate (%)","type":"number","default":"22","min":"0","max":"50"},
            {"id":"seTaxRate","label_cn":"自雇税率(%)","label_en":"Self-Employment Tax Rate (%)","type":"number","default":"15.3","min":"0","max":"30","step":"0.1"},
        ],
        "calc": """var income=parseFloat(el('gigIncome').value)||0;
var expenses=parseFloat(el('businessExpenses').value)||0;
var other=parseFloat(el('otherIncome').value)||0;
var taxRate=parseFloat(el('taxRate').value)||0;
var seRate=parseFloat(el('seTaxRate').value)||0;
var netIncome=income-expenses;
var seTax=netIncome*0.9235*seRate/100;
var taxable=netIncome*0.9235+other;
var incomeTax=taxable*taxRate/100;
var totalTax=seTax+incomeTax;
var quarterly=totalTax/4;
var effectiveRate=totalTax/netIncome*100;""",
        "results": [
            {"id":"resNetIncome","label_cn":"净收入","label_en":"Net Income","fmt":"money"},
            {"id":"resSeTax","label_cn":"自雇税","label_en":"Self-Employment Tax","fmt":"money"},
            {"id":"resIncomeTax","label_cn":"所得税","label_en":"Income Tax","fmt":"money"},
            {"id":"resTotalTax","label_cn":"总税款","label_en":"Total Tax","fmt":"money"},
            {"id":"resQuarterly","label_cn":"季度预估税","label_en":"Quarterly Estimate","fmt":"money"},
            {"id":"resEffectiveRate","label_cn":"有效税率","label_en":"Effective Rate","fmt":"pct"},
        ],
    },
    {
        "slug": "agency-pricing-calculator",
        "icon": "💼",
        "cat_cn": "商业计算器",
        "cat_en": "Business Calculators",
        "name_cn": "代理服务定价计算器",
        "name_en": "Agency Pricing Calculator",
        "desc_cn": "计算代理服务的合理定价，考虑人力成本、管理费用和利润率，帮助代理公司科学报价。纯前端计算。",
        "desc_en": "Calculate reasonable pricing for agency services, considering labor costs, overhead, and profit margin. Price your services scientifically. Pure frontend.",
        "kw_cn": "代理定价,服务报价,广告公司定价,咨询费率,自由职业定价,在线工具",
        "kw_en": "agency pricing,service pricing,consulting rate,freelance rate,online tool",
        "inputs": [
            {"id":"teamSize","label_cn":"团队人数","label_en":"Team Size","type":"number","default":"5","min":"1","max":"100"},
            {"id":"avgSalary","label_cn":"平均年薪(元)","label_en":"Average Annual Salary ($)","type":"number","default":"80000","step":"5000"},
            {"id":"overhead","label_cn":"运营管理费用(月,元)","label_en":"Monthly Overhead ($)","type":"number","default":"15000","step":"1000"},
            {"id":"targetMargin","label_cn":"目标利润率(%)","label_en":"Target Profit Margin (%)","type":"number","default":"25","min":"0","max":"80"},
            {"id":"billableHours","label_cn":"每人每月可计费小时","label_en":"Billable Hours/Month/Person","type":"number","default":"120","min":"20","max":"200"},
            {"id":"nonBillable","label_cn":"不可计费时间占比(%)","label_en":"Non-Billable Time (%)","type":"number","default":"30","min":"0","max":"60"},
        ],
        "calc": """var team=parseFloat(el('teamSize').value)||1;
var salary=parseFloat(el('avgSalary').value)||0;
var overhead=parseFloat(el('overhead').value)||0;
var margin=parseFloat(el('targetMargin').value)||0;
var billableHrs=parseFloat(el('billableHours').value)||120;
var nonBill=parseFloat(el('nonBillable').value)||0;
var annualSalary=team*salary;
var annualOverhead=overhead*12;
var totalCost=annualSalary+annualOverhead;
var totalBillable=team*billableHrs*12;
var effectiveBillable=totalBillable*(1-nonBill/100);
var hourlyCost=totalCost/effectiveBillable;
var hourlyRate=hourlyCost/(1-margin/100);
var monthlyRevenue=hourlyRate*totalBillable/12;""",
        "results": [
            {"id":"resTotalCost","label_cn":"年度总成本","label_en":"Annual Total Cost","fmt":"money"},
            {"id":"resHourlyCost","label_cn":"每小时实际成本","label_en":"Actual Hourly Cost","fmt":"money"},
            {"id":"resHourlyRate","label_cn":"建议每小时报价","label_en":"Recommended Hourly Rate","fmt":"money"},
            {"id":"resMonthlyRevenue","label_cn":"预期月收入","label_en":"Expected Monthly Revenue","fmt":"money"},
        ],
    },
]

def gen_html(tool, lang):
    """lang: 'cn' or 'en'"""
    slug = tool['slug']
    icon = tool['icon']
    name = tool['name_cn'] if lang == 'cn' else tool['name_en']
    desc = tool['desc_cn'] if lang == 'cn' else tool['desc_en']
    cat = tool['cat_cn'] if lang == 'cn' else tool['cat_en']
    kw = tool['kw_cn'] if lang == 'cn' else tool['kw_en']
    lang_attr = 'zh-CN' if lang == 'cn' else 'en'
    base = '/' if lang == 'cn' else '/en/'
    prefix = '' if lang == 'cn' else '../'
    
    # Build inputs HTML
    inputs_html = ''
    calc_fields = []
    for inp in tool['inputs']:
        lid = inp['id']
        label = inp['label_cn'] if lang == 'cn' else inp['label_en']
        if inp['type'] == 'select':
            opts = ''
            for o in inp['options']:
                sel = ' selected' if o['v'] == inp.get('default', '') else ''
                txt = o['cn'] if lang == 'cn' else o['en']
                opts += f'<option value="{o["v"]}"{sel}>{txt}</option>'
            inputs_html += f'<div class="form-group"><label for="{lid}">{label}</label><select id="{lid}">{opts}</select></div>\n'
            calc_fields.append(f"/* {lid}=el('{lid}').value */")
        else:
            dv = inp.get('default', '')
            mn = f' min="{inp["min"]}"' if 'min' in inp else ''
            mx = f' max="{inp["max"]}"' if 'max' in inp else ''
            st = f' step="{inp["step"]}"' if 'step' in inp else ' step="1"'
            inputs_html += f'<div class="form-group"><label for="{lid}">{label}</label><input type="number" id="{lid}" value="{dv}"{mn}{mx}{st}></div>\n'
    
    # Build results HTML
    results_html = ''
    set_vals = ''
    for i, r in enumerate(tool['results']):
        rid = r['id']
        rlabel = r['label_cn'] if lang == 'cn' else r['label_en']
        results_html += f'<div class="result-item"><span class="result-label">{rlabel}</span><span class="result-value" id="{rid}">-</span></div>\n'
    
    # Currency format
    currency = '¥' if lang == 'cn' else '$'
    decimal_sep = ''
    
    # Build the set values JS
    set_vals_lines = []
    for r in tool['results']:
        rid = r['id']
        fmt = r.get('fmt', 'money')
        var_name = 'res' + rid[3:]  # resTotalCost -> TotalCost (but we use lowercase)
        # Actually use the camelCase from calc
        if fmt == 'money':
            set_vals_lines.append(f"  el('{rid}').textContent='{currency}'+(Math.round({rid[3:]}*100)/100).toLocaleString();")
        elif fmt == 'pct':
            set_vals_lines.append(f"  el('{rid}').textContent=(Math.round({rid[3:]}*10)/10).toFixed(1)+'%';")
        elif fmt == 'years':
            set_vals_lines.append(f"  el('{rid}').textContent=Math.round({rid[3:]})+('{ '年' if lang == 'cn' else ' years'}');")
        else:
            set_vals_lines.append(f"  el('{rid}').textContent=Math.round({rid[3:]}*100)/100;")
    
    cn_url = f'https://free-toolbase.com/{slug}/'
    en_url = f'https://free-toolbase.com/en/{slug}/'
    page_url = cn_url if lang == 'cn' else en_url
    
    # Related tools - simple
    related = [t for t in TOOLS if t['slug'] != slug][:4]
    if lang == 'cn':
        related_html = ''.join(f'<a href="/{r["slug"]}/" style="display:inline-block;padding:6px 12px;margin:4px;background:#0f172a;border-radius:6px;text-decoration:none;color:#22d3ee;font-size:14px;">{r["icon"]} {r["name_cn"]}</a>' for r in related)
        related_title = '🔗 相关工具推荐'
    else:
        related_html = ''.join(f'<a href="/en/{r["slug"]}/" style="display:inline-block;padding:6px 12px;margin:4px;background:#0f172a;border-radius:6px;text-decoration:none;color:#22d3ee;font-size:14px;">{r["icon"]} {r["name_en"]}</a>' for r in related)
        related_title = '🔗 Related Tools'
    
    # Breadcrumb
    if lang == 'cn':
        bc = json.dumps({
            "@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[
                {"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},
                {"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"},
                {"@type":"ListItem","position":3,"name":name}
            ]
        }, ensure_ascii=False)
        home_label = '首页'
    else:
        bc = json.dumps({
            "@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"},
                {"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"},
                {"@type":"ListItem","position":3,"name":name}
            ]
        }, ensure_ascii=False)
        home_label = 'Home'
    
    sa = json.dumps({
        "@context":"https://schema.org","@type":"SoftwareApplication",
        "name":name,"description":desc[:150],"applicationCategory":"UtilitiesApplication",
        "operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}
    }, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - Free ToolBase</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="zh" href="{cn_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{cn_url}">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{desc[:150]}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{sa}
</script>
<script type="application/ld+json">
{bc}
</script>
<style>
:root{{--primary:#4F46E5;--bg:#f8fafc;--card-bg:#ffffff;--text:#1e293b;--text-secondary:#64748b;--border:rgba(148,163,184,.2);--shadow:0 1px 3px rgba(0,0,0,.06);--radius:12px;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}}
.container{{max-width:720px;margin:0 auto;padding:0 20px}}
header{{background:var(--card-bg);border-bottom:1px solid var(--border);padding:16px 0;margin-bottom:32px}}
header .container{{display:flex;justify-content:space-between;align-items:center}}
header a{{color:var(--primary);text-decoration:none;font-weight:600;font-size:1.1rem}}
header nav a{{margin-left:20px;font-size:.9rem;color:var(--text-secondary)}}
h1{{font-size:1.6rem;margin-bottom:8px;color:var(--text)}}
.subtitle{{color:var(--text-secondary);font-size:.95rem;margin-bottom:24px}}
.form-group{{margin-bottom:16px}}
.form-group label{{display:block;font-size:.9rem;font-weight:600;color:var(--text);margin-bottom:6px}}
.form-group input,.form-group select{{width:100%;padding:10px 14px;border:1px solid var(--border);border-radius:8px;font-size:1rem;background:var(--card-bg);color:var(--text);transition:border-color .2s}}
.form-group input:focus,.form-group select:focus{{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}}
.btn-row{{display:flex;gap:10px;margin:20px 0;flex-wrap:wrap}}
.btn{{padding:10px 20px;border:none;border-radius:8px;font-size:.95rem;font-weight:600;cursor:pointer;transition:all .2s}}
.btn-primary{{background:var(--primary);color:#fff}}
.btn-primary:hover{{opacity:.9;transform:translateY(-1px)}}
.btn-secondary{{background:#e2e8f0;color:var(--text)}}
.btn-secondary:hover{{background:#cbd5e1}}
.result-panel{{background:var(--card-bg);border-radius:var(--radius);padding:24px;margin-top:24px;box-shadow:var(--shadow);border:1px solid var(--border);display:none}}
.result-panel h2{{font-size:1.1rem;margin-bottom:16px;color:var(--text)}}
.result-item{{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border)}}
.result-item:last-child{{border-bottom:none}}
.result-label{{font-size:.9rem;color:var(--text-secondary)}}
.result-value{{font-size:1.2rem;font-weight:700;color:var(--primary)}}
.info-box{{background:rgba(79,70,229,.05);border:1px solid rgba(79,70,229,.15);border-radius:8px;padding:16px;margin-top:24px;font-size:.9rem;color:var(--text-secondary)}}
footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
footer a{{color:#64748b;margin:0 8px}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 24px;border-radius:20px;font-size:.9rem;opacity:0;pointer-events:none;transition:opacity .3s;z-index:9999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.container{{padding:0 12px}}.btn{{padding:8px 14px;font-size:.85rem}}.result-panel{{padding:16px}}}}
</style>
</head>
<body>
<header>
<div class="container">
<a href="{base}">{icon} Free ToolBase</a>
<nav>
<a href="{base}">{home_label}</a>
</nav>
</div>
</header>
<main class="container">
<h1>{icon} {name}</h1>
<p class="subtitle">{desc}</p>

<div class="form-panel">
{inputs_html}
</div>

<div class="btn-row">
<button class="btn btn-primary" onclick="calculate()">🖩 {'计算' if lang == 'cn' else 'Calculate'}</button>
<button class="btn btn-secondary" onclick="clearAll()">🗑️ {'清空' if lang == 'cn' else 'Clear'}</button>
</div>

<div class="result-panel" id="resultPanel">
<h2>{'📊 计算结果' if lang == 'cn' else '📊 Results'}</h2>
<div id="resultContent">
{results_html}
</div>
<button class="btn btn-secondary" style="margin-top:16px" onclick="copyResults()">📋 {'复制结果' if lang == 'cn' else 'Copy Results'}</button>
</div>

<div class="info-box">
{'<strong>💡 说明：</strong>本工具为纯前端计算，所有数据仅在您的浏览器中处理，不会上传到任何服务器。' if lang == 'cn' else '<strong>💡 Note:</strong> This tool runs entirely in your browser. No data is ever uploaded to any server.'}
</div>

<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">{related_title}</h2>
<div style="display:flex;flex-wrap:wrap;gap:4px;">{related_html}</div>
</section>

</main>
{FOOTER_CN if lang == 'cn' else FOOTER_EN}
<div class="toast" id="toast"></div>
<script>
function el(id){{return document.getElementById(id);}}
function showToast(msg){{var t=el('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}

function calculate(){{
{tool['calc']}

el('resultPanel').style.display='block';
{chr(10).join(set_vals_lines)}
}}

function clearAll(){{
{'el(\"resultPanel\").style.display=\"none\";' if lang == 'cn' else 'el("resultPanel").style.display="none";'}
var inputs=document.querySelectorAll('input[type=number]');
inputs.forEach(function(i){{i.value=i.defaultValue;}});
var selects=document.querySelectorAll('select');
selects.forEach(function(s){{s.selectedIndex=0;}});
}}

function copyResults(){{
var text='';
var items=document.querySelectorAll('.result-item');
items.forEach(function(item){{
text+=item.querySelector('.result-label').textContent+': '+item.querySelector('.result-value').textContent+'\\n';
}});
if(text)navigator.clipboard.writeText(text).then(function(){{showToast('{'已复制到剪贴板' if lang == 'cn' else 'Copied to clipboard'}');}});
}}
</script>
</body>
</html>'''
    return html

# Create directories and write files
created = []
for tool in TOOLS:
    slug = tool['slug']
    
    # CN
    cn_dir = os.path.join(SITE, slug)
    os.makedirs(cn_dir, exist_ok=True)
    cn_html = gen_html(tool, 'cn')
    cn_path = os.path.join(cn_dir, 'index.html')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    created.append(f'cn:{slug}')
    
    # EN
    en_dir = os.path.join(SITE, 'en', slug)
    os.makedirs(en_dir, exist_ok=True)
    en_html = gen_html(tool, 'en')
    en_path = os.path.join(en_dir, 'index.html')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    created.append(f'en:{slug}')

print(f'✅ Created {len(created)} pages:')
for c in created:
    print(f'  {c}')
