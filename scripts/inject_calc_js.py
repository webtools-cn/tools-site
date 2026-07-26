#!/usr/bin/env python3
"""Add real calculator JS logic to the 5 new tools"""
import os, re

SITE = "/home/chison/tools-site"

TOOL_JS = {
    "cd-calculator": {
        "inputs": [
            {"id": "principal", "label_cn": "存入本金 ($)", "label_en": "Principal ($)", "type": "number", "default": "10000", "min": "1", "hint_cn": "您存入CD的初始金额", "hint_en": "Initial deposit amount"},
            {"id": "annualRate", "label_cn": "年利率 (%)", "label_en": "Annual Rate (%)", "type": "number", "default": "4.5", "min": "0.01", "step": "0.01", "hint_cn": "CD约定的年化利率", "hint_en": "CD annual interest rate"},
            {"id": "termMonths", "label_cn": "存期 (月)", "label_en": "Term (months)", "type": "number", "default": "12", "min": "1", "max": "60", "hint_cn": "CD存款期限", "hint_en": "CD term length"},
            {"id": "compoundFreq", "label_cn": "复利频率", "label_en": "Compounding", "type": "select", "options_cn": [("1","年复利"),("4","季复利"),("12","月复利"),("365","日复利")], "options_en": [("1","Annual"),("4","Quarterly"),("12","Monthly"),("365","Daily")]},
            {"id": "earlyWithdrawMonth", "label_cn": "提前支取月份 (0=到期)", "label_en": "Early withdrawal month (0=maturity)", "type": "number", "default": "0", "min": "0", "hint_cn": "如果提前支取，输入支取月份；0表示持有到期", "hint_en": "If withdrawing early, enter month; 0 for full term"},
        ],
        "results": [
            {"id": "maturityValue", "label_cn": "到期价值", "label_en": "Maturity Value", "sub_cn": "含本金和利息", "sub_en": "Principal + Interest"},
            {"id": "totalInterest", "label_cn": "总利息收益", "label_en": "Total Interest", "sub_cn": "复利产生的收益", "sub_en": "Interest earned"},
            {"id": "penaltyAmount", "label_cn": "提前支取罚息", "label_en": "Early Withdrawal Penalty", "sub_cn": "罚息金额", "sub_en": "Penalty amount"},
        ],
        "calc_js": """
function calculate() {
    var p = parseFloat(document.getElementById('principal').value) || 0;
    var r = parseFloat(document.getElementById('annualRate').value) || 0;
    var t = parseInt(document.getElementById('termMonths').value) || 0;
    var n = parseInt(document.getElementById('compoundFreq').value) || 1;
    var ew = parseInt(document.getElementById('earlyWithdrawMonth').value) || 0;
    
    r = r / 100;
    var years = t / 12;
    var periods = n * years;
    var ratePerPeriod = r / n;
    var maturity = p * Math.pow(1 + ratePerPeriod, periods);
    var interest = maturity - p;
    
    var penalty = 0;
    if (ew > 0 && ew < t) {
        var earlyYears = ew / 12;
        var earlyPeriods = n * earlyYears;
        var earlyValue = p * Math.pow(1 + ratePerPeriod, earlyPeriods);
        var penaltyDays = Math.min(180, t * 30);
        penalty = (earlyValue - p) * (penaltyDays / (t * 30));
        if (penalty > interest) penalty = interest;
    }
    
    var netValue = maturity - penalty;
    document.getElementById('maturityValue').textContent = '$' + netValue.toFixed(2);
    document.getElementById('totalInterest').textContent = '$' + interest.toFixed(2);
    document.getElementById('penaltyAmount').textContent = penalty > 0 ? '$' + penalty.toFixed(2) : '$0.00';
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('principal').value = '10000';
    document.getElementById('annualRate').value = '4.5';
    document.getElementById('termMonths').value = '12';
    document.getElementById('compoundFreq').value = '1';
    document.getElementById('earlyWithdrawMonth').value = '0';
    document.getElementById('resultsSection').style.display = 'none';
}
"""
    },
    "restaurant-tip-calculator": {
        "inputs": [
            {"id": "billAmount", "label_cn": "账单金额 ($)", "label_en": "Bill Amount ($)", "type": "number", "default": "50", "min": "0.01", "step": "0.01", "hint_cn": "不含小费的账单总金额", "hint_en": "Total bill before tip"},
            {"id": "tipPercent", "label_cn": "小费比例 (%)", "label_en": "Tip Percentage (%)", "type": "number", "default": "18", "min": "0", "max": "50", "step": "0.5", "hint_cn": "通常15-20%", "hint_en": "Typically 15-20%"},
            {"id": "numPeople", "label_cn": "用餐人数", "label_en": "Number of People", "type": "number", "default": "2", "min": "1", "max": "100", "hint_cn": "AA制分账人数", "hint_en": "Split among this many people"},
            {"id": "taxRate", "label_cn": "税率 (%)", "label_en": "Tax Rate (%)", "type": "number", "default": "8", "min": "0", "max": "30", "step": "0.5", "hint_cn": "当地消费税税率（可选）", "hint_en": "Local sales tax rate (optional)"},
        ],
        "results": [
            {"id": "tipAmount", "label_cn": "小费金额", "label_en": "Tip Amount", "sub_cn": "建议小费", "sub_en": "Suggested tip"},
            {"id": "totalWithTip", "label_cn": "总计(含小费)", "label_en": "Total with Tip", "sub_cn": "账单+小费", "sub_en": "Bill + Tip"},
            {"id": "perPerson", "label_cn": "每人应付", "label_en": "Per Person", "sub_cn": "AA制分账", "sub_en": "Split equally"},
        ],
        "calc_js": """
function calculate() {
    var bill = parseFloat(document.getElementById('billAmount').value) || 0;
    var tipPct = parseFloat(document.getElementById('tipPercent').value) || 0;
    var people = parseInt(document.getElementById('numPeople').value) || 1;
    var taxRate = parseFloat(document.getElementById('taxRate').value) || 0;
    
    var taxAmount = bill * (taxRate / 100);
    var tip = (bill + taxAmount) * (tipPct / 100);
    var total = bill + taxAmount + tip;
    var perPerson = total / people;
    
    document.getElementById('tipAmount').textContent = '$' + tip.toFixed(2);
    document.getElementById('totalWithTip').textContent = '$' + total.toFixed(2);
    document.getElementById('perPerson').textContent = '$' + perPerson.toFixed(2);
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('billAmount').value = '50';
    document.getElementById('tipPercent').value = '18';
    document.getElementById('numPeople').value = '2';
    document.getElementById('taxRate').value = '8';
    document.getElementById('resultsSection').style.display = 'none';
}
"""
    },
    "bmi-children-calculator": {
        "inputs": [
            {"id": "age", "label_cn": "年龄 (岁)", "label_en": "Age (years)", "type": "number", "default": "10", "min": "2", "max": "19", "step": "0.5", "hint_cn": "2-19岁", "hint_en": "2-19 years"},
            {"id": "gender", "label_cn": "性别", "label_en": "Gender", "type": "select", "options_cn": [("male","男"),("female","女")], "options_en": [("male","Male"),("female","Female")]},
            {"id": "heightCm", "label_cn": "身高 (cm)", "label_en": "Height (cm)", "type": "number", "default": "140", "min": "50", "max": "250", "hint_cn": "孩子当前身高", "hint_en": "Current height"},
            {"id": "weightKg", "label_cn": "体重 (kg)", "label_en": "Weight (kg)", "type": "number", "default": "35", "min": "10", "max": "200", "step": "0.1", "hint_cn": "孩子当前体重", "hint_en": "Current weight"},
        ],
        "results": [
            {"id": "bmiValue", "label_cn": "BMI值", "label_en": "BMI", "sub_cn": "身体质量指数", "sub_en": "Body Mass Index"},
            {"id": "percentile", "label_cn": "BMI百分位", "label_en": "BMI Percentile", "sub_cn": "同龄儿童中的位置", "sub_en": "Among peers"},
            {"id": "category", "label_cn": "体重类别", "label_en": "Weight Category", "sub_cn": "CDC分类", "sub_en": "CDC classification"},
        ],
        "calc_js": """
// CDC LMS parameters (simplified lookup)
var cdcLms = {
    male: {
        2:[16.5,1.0,0.08],3:[15.9,1.0,0.08],4:[15.5,1.0,0.09],5:[15.3,1.0,0.09],
        6:[15.4,1.0,0.10],7:[15.6,1.0,0.10],8:[16.0,1.0,0.11],9:[16.4,1.0,0.11],
        10:[16.9,1.0,0.12],11:[17.5,1.0,0.13],12:[18.2,1.0,0.14],13:[18.9,1.0,0.15],
        14:[19.7,1.0,0.16],15:[20.5,1.0,0.17],16:[21.3,1.0,0.18],17:[22.0,1.0,0.18],
        18:[22.6,1.0,0.18],19:[23.1,1.0,0.19]
    },
    female: {
        2:[16.2,1.0,0.08],3:[15.7,1.0,0.08],4:[15.3,1.0,0.09],5:[15.1,1.0,0.09],
        6:[15.2,1.0,0.10],7:[15.5,1.0,0.10],8:[15.9,1.0,0.11],9:[16.5,1.0,0.11],
        10:[17.1,1.0,0.12],11:[17.8,1.0,0.13],12:[18.5,1.0,0.14],13:[19.2,1.0,0.15],
        14:[19.8,1.0,0.16],15:[20.3,1.0,0.16],16:[20.7,1.0,0.17],17:[21.0,1.0,0.17],
        18:[21.2,1.0,0.17],19:[21.4,1.0,0.17]
    }
};

function calculate() {
    var age = parseFloat(document.getElementById('age').value);
    var gender = document.getElementById('gender').value;
    var h = parseFloat(document.getElementById('heightCm').value) / 100;
    var w = parseFloat(document.getElementById('weightKg').value);
    
    var bmi = w / (h * h);
    document.getElementById('bmiValue').textContent = bmi.toFixed(1);
    
    var ageKey = Math.round(age);
    if (ageKey < 2) ageKey = 2;
    if (ageKey > 19) ageKey = 19;
    var params = cdcLms[gender][ageKey];
    if (!params) { params = [22,1,0.15]; }
    
    var L = params[0], M = params[1], S = params[2];
    var z = Math.pow(bmi / M, L) - 1;
    z = z / (L * S);
    if (L < 0.001) { z = Math.log(bmi / M) / S; }
    
    // Approximate percentile from z-score
    var pct = Math.round(normalCDF(z) * 100);
    if (pct < 1) pct = 1;
    if (pct > 99) pct = 99;
    document.getElementById('percentile').textContent = pct + '%';
    
    var cat;
    if (pct < 5) cat = '偏瘦 (Underweight)';
    else if (pct < 85) cat = '正常 (Healthy)';
    else if (pct < 95) cat = '超重 (Overweight)';
    else cat = '肥胖 (Obese)';
    document.getElementById('category').textContent = cat;
    document.getElementById('resultsSection').style.display = 'block';
}

function normalCDF(x) {
    var t = 1 / (1 + 0.2316419 * Math.abs(x));
    var d = 0.3989423 * Math.exp(-x * x / 2);
    var p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    return x > 0 ? 1 - p : p;
}

function resetAll() {
    document.getElementById('age').value = '10';
    document.getElementById('gender').value = 'male';
    document.getElementById('heightCm').value = '140';
    document.getElementById('weightKg').value = '35';
    document.getElementById('resultsSection').style.display = 'none';
}
"""
    },
    "metabolic-age-calculator": {
        "inputs": [
            {"id": "age", "label_cn": "实际年龄", "label_en": "Actual Age", "type": "number", "default": "30", "min": "18", "max": "100", "hint_cn": "您的实际年龄", "hint_en": "Your actual age"},
            {"id": "gender", "label_cn": "性别", "label_en": "Gender", "type": "select", "options_cn": [("male","男"),("female","女")], "options_en": [("male","Male"),("female","Female")]},
            {"id": "weightKg", "label_cn": "体重 (kg)", "label_en": "Weight (kg)", "type": "number", "default": "70", "min": "30", "max": "300", "step": "0.1", "hint_cn": "当前体重", "hint_en": "Current weight"},
            {"id": "heightCm", "label_cn": "身高 (cm)", "label_en": "Height (cm)", "type": "number", "default": "170", "min": "100", "max": "250", "hint_cn": "当前身高", "hint_en": "Current height"},
            {"id": "bodyFat", "label_cn": "体脂率 (%) (可选)", "label_en": "Body Fat (%) (optional)", "type": "number", "default": "", "min": "3", "max": "60", "step": "0.1", "hint_cn": "如果知道体脂率可输入，更准确", "hint_en": "Enter if known for more accuracy"},
        ],
        "results": [
            {"id": "bmrValue", "label_cn": "您的基础代谢率", "label_en": "Your BMR", "sub_cn": "大卡/天", "sub_en": "cal/day"},
            {"id": "avgBmr", "label_cn": "同龄平均BMR", "label_en": "Average BMR", "sub_cn": "同龄同性别均值", "sub_en": "Peer average"},
            {"id": "metabolicAge", "label_cn": "代谢年龄", "label_en": "Metabolic Age", "sub_cn": "身体代谢年龄", "sub_en": "Body's metabolic age"},
        ],
        "calc_js": """
function calculate() {
    var age = parseInt(document.getElementById('age').value) || 30;
    var gender = document.getElementById('gender').value;
    var w = parseFloat(document.getElementById('weightKg').value) || 70;
    var h = parseFloat(document.getElementById('heightCm').value) || 170;
    var bf = parseFloat(document.getElementById('bodyFat').value) || 0;
    
    // Mifflin-St Jeor
    var bmr;
    if (gender === 'male') {
        bmr = 10 * w + 6.25 * h - 5 * age + 5;
    } else {
        bmr = 10 * w + 6.25 * h - 5 * age - 161;
    }
    
    // Adjust for body fat if provided
    if (bf > 0) {
        var leanMass = w * (1 - bf / 100);
        var fatMass = w * (bf / 100);
        bmr = leanMass * 21.6 + fatMass * 4.3 + 370;
    }
    
    document.getElementById('bmrValue').textContent = Math.round(bmr) + ' cal/day';
    
    // Average BMR for age group (simplified)
    var avgBmr;
    if (gender === 'male') {
        avgBmr = 2000 - (age - 20) * 8;
    } else {
        avgBmr = 1650 - (age - 20) * 6;
    }
    document.getElementById('avgBmr').textContent = Math.round(avgBmr) + ' cal/day';
    
    // Calculate metabolic age
    var diff = bmr - avgBmr;
    var metaAge = age - Math.round(diff / 10);
    if (metaAge < 18) metaAge = 18;
    if (metaAge > 90) metaAge = 90;
    document.getElementById('metabolicAge').textContent = metaAge + ' 岁';
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('age').value = '30';
    document.getElementById('gender').value = 'male';
    document.getElementById('weightKg').value = '70';
    document.getElementById('heightCm').value = '170';
    document.getElementById('bodyFat').value = '';
    document.getElementById('resultsSection').style.display = 'none';
}
"""
    },
    "wilks-score-calculator": {
        "inputs": [
            {"id": "bodyWeight", "label_cn": "体重 (kg)", "label_en": "Body Weight (kg)", "type": "number", "default": "80", "min": "30", "max": "300", "step": "0.1", "hint_cn": "当前体重", "hint_en": "Current body weight"},
            {"id": "gender", "label_cn": "性别", "label_en": "Gender", "type": "select", "options_cn": [("male","男"),("female","女")], "options_en": [("male","Male"),("female","Female")]},
            {"id": "squat", "label_cn": "深蹲 (kg)", "label_en": "Squat (kg)", "type": "number", "default": "140", "min": "0", "max": "500", "step": "0.5", "hint_cn": "深蹲最大重量(1RM)", "hint_en": "Squat 1RM"},
            {"id": "bench", "label_cn": "卧推 (kg)", "label_en": "Bench Press (kg)", "type": "number", "default": "100", "min": "0", "max": "400", "step": "0.5", "hint_cn": "卧推最大重量(1RM)", "hint_en": "Bench press 1RM"},
            {"id": "deadlift", "label_cn": "硬拉 (kg)", "label_en": "Deadlift (kg)", "type": "number", "default": "180", "min": "0", "max": "500", "step": "0.5", "hint_cn": "硬拉最大重量(1RM)", "hint_en": "Deadlift 1RM"},
        ],
        "results": [
            {"id": "total", "label_cn": "三项总成绩", "label_en": "Total", "sub_cn": "深蹲+卧推+硬拉", "sub_en": "Squat+Bench+Deadlift"},
            {"id": "wilksScore", "label_cn": "Wilks分数", "label_en": "Wilks Score", "sub_cn": "相对力量评分", "sub_en": "Relative strength score"},
            {"id": "level", "label_cn": "水平等级", "label_en": "Level", "sub_cn": "力量等级评估", "sub_en": "Strength level"},
        ],
        "calc_js": """
// Wilks 2020 coefficients
var wilksCoeffsMale = [-216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-6, -1.291e-8];
var wilksCoeffsFemale = [594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-5, -9.054e-8];

function wilks(bw, gender) {
    var coeffs = gender === 'male' ? wilksCoeffsMale : wilksCoeffsFemale;
    var x = bw;
    var denom = coeffs[0] + coeffs[1]*x + coeffs[2]*x*x + coeffs[3]*x*x*x + coeffs[4]*x*x*x*x + coeffs[5]*x*x*x*x*x;
    return 500 / denom;
}

function calculate() {
    var bw = parseFloat(document.getElementById('bodyWeight').value) || 80;
    var gender = document.getElementById('gender').value;
    var squat = parseFloat(document.getElementById('squat').value) || 0;
    var bench = parseFloat(document.getElementById('bench').value) || 0;
    var deadlift = parseFloat(document.getElementById('deadlift').value) || 0;
    
    var total = squat + bench + deadlift;
    var score = total * wilks(bw, gender);
    
    document.getElementById('total').textContent = total.toFixed(1) + ' kg';
    document.getElementById('wilksScore').textContent = score.toFixed(2);
    
    var level;
    if (score < 250) level = '初学者 (Beginner)';
    else if (score < 300) level = '入门 (Novice)';
    else if (score < 350) level = '中级 (Intermediate)';
    else if (score < 400) level = '进阶 (Advanced)';
    else if (score < 450) level = '精英 (Elite)';
    else level = '世界级 (World Class)';
    document.getElementById('level').textContent = level;
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('bodyWeight').value = '80';
    document.getElementById('gender').value = 'male';
    document.getElementById('squat').value = '140';
    document.getElementById('bench').value = '100';
    document.getElementById('deadlift').value = '180';
    document.getElementById('resultsSection').style.display = 'none';
}
"""
    },
}

def build_input_html(tool_data, is_cn):
    html = ""
    for inp in tool_data["inputs"]:
        label = inp[f"label_{'cn' if is_cn else 'en'}"]
        hint = inp.get(f"hint_{'cn' if is_cn else 'en'}", "")
        inp_id = inp["id"]
        
        if inp["type"] == "select":
            options = inp[f"options_{'cn' if is_cn else 'en'}"]
            opt_html = "".join([f'<option value="{v}">{label_text}</option>' for v, label_text in options])
            html += f'''<div class="input-group">
<label for="{inp_id}">{label}</label>
<select id="{inp_id}">{opt_html}</select>
<div class="hint">{hint}</div>
</div>
'''
        else:
            default = inp.get("default", "")
            min_val = inp.get("min", "")
            max_val = inp.get("max", "")
            step = inp.get("step", "")
            attrs = f'id="{inp_id}" value="{default}"'
            if min_val: attrs += f' min="{min_val}"'
            if max_val: attrs += f' max="{max_val}"'
            if step: attrs += f' step="{step}"'
            html += f'''<div class="input-group">
<label for="{inp_id}">{label}</label>
<input type="{inp['type']}" {attrs}>
<div class="hint">{hint}</div>
</div>
'''
    return html

def build_results_html(tool_data, is_cn):
    html = ""
    for r in tool_data["results"]:
        label = r[f"label_{'cn' if is_cn else 'en'}"]
        sub = r.get(f"sub_{'cn' if is_cn else 'en'}", "")
        # first result gets highlight
        is_first = (r == tool_data["results"][0])
        cls = ' highlight' if is_first else ''
        html += f'''<div class="result-card{cls}">
<div class="label">{label}</div>
<div class="value" id="{r['id']}">-</div>
<div class="sub">{sub}</div>
</div>
'''
    return html

def inject_js(filepath, tool_slug, is_cn):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tool_data = TOOL_JS[tool_slug]
    
    # Replace input grid placeholder
    input_html = build_input_html(tool_data, is_cn)
    content = content.replace('<div class="input-grid" id="inputGrid"></div>', 
                              f'<div class="input-grid" id="inputGrid">\n{input_html}</div>')
    
    # Replace results grid placeholder
    results_html = build_results_html(tool_data, is_cn)
    content = content.replace('<div class="results-grid" id="resultsGrid"></div>',
                              f'<div class="results-grid" id="resultsGrid">\n{results_html}</div>')
    
    # Replace empty calculate/reset functions with real logic
    old_funcs = """function calculate(){}
function resetAll(){}"""
    new_funcs = tool_data["calc_js"].strip()
    content = content.replace(old_funcs, new_funcs)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Injected JS: {filepath}")

# Inject JS into all 10 pages
for tool_slug in TOOL_JS:
    cn_path = os.path.join(SITE, tool_slug, "index.html")
    en_path = os.path.join(SITE, "en", tool_slug, "index.html")
    inject_js(cn_path, tool_slug, True)
    inject_js(en_path, tool_slug, False)

print("\n🎉 All 5 tools now have real calculator logic!")