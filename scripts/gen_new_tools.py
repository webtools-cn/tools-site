#!/usr/bin/env python3
"""批量生成4个新工具：graham-number, intrinsic-value, cost-basis, athletic-performance"""
import os

BASE = "/home/chison/tools-site"

tools = {
    "graham-number-calculator": {
        "cn": {
            "title": "免费在线格雷厄姆数字计算器",
            "short": "格雷厄姆数字计算器",
            "desc": "免费在线格雷厄姆数字（Graham Number）计算器，基于本杰明·格雷厄姆的价值投资公式，输入EPS和BVPS计算股票公允价值上限。纯前端本地计算。",
            "faq_title": "什么是格雷厄姆数字？",
            "faq_answer": "格雷厄姆数字（Graham Number）由本杰明·格雷厄姆提出，用于估算股票公允价值的上限。公式：<code>√(22.5 × EPS × BVPS)</code>，其中22.5 = 15倍PE × 1.5倍PB。若股价低于格雷厄姆数字，可能被低估。",
            "hero_desc": "免费在线格雷厄姆数字（Graham Number）计算器，基于本杰明·格雷厄姆的价值投资公式，输入EPS和BVPS计算股票公允价值上限。纯前端本地计算。",
            "calc_label": "输入每股收益 EPS和每股账面价值 BVPS，计算格雷厄姆数字",
            "input1_label": "每股收益 EPS：",
            "input1_id": "eps",
            "input1_val": "5.50",
            "input2_label": "每股账面价值 BVPS：",
            "input2_id": "bvps",
            "input2_val": "45.00",
            "result_label": "格雷厄姆数字",
            "formula": "√(22.5 × EPS × BVPS) = √(22.5 × 5.50 × 45.00)",
            "calc_js": """
var eps=parseFloat(document.getElementById('eps').value)||0;
var bvps=parseFloat(document.getElementById('bvps').value)||0;
var graham=Math.sqrt(22.5*eps*bvps);
var pe15=15*eps;
var pb15=1.5*bvps;
document.getElementById('val1').textContent='$'+graham.toFixed(2);
document.getElementById('val2').textContent='$'+pe15.toFixed(2);
document.getElementById('val3').textContent='$'+pb15.toFixed(2);
var margin=((graham-parseFloat(document.getElementById('price').value||'0'))/graham*100);
document.getElementById('val4').textContent=margin.toFixed(1)+'%';
""",
            "extra_input": '<div class="form-row"><label>当前股价：</label><input type="number" id="price" value="65.00" step="any"></div>',
            "extra_labels": {"label2": "15×PE=EPS×15", "label3": "1.5×PB=BVPS×1.5", "label4": "安全边际"},
            "info_html": '<h3>🎯 格雷厄姆数字公式</h3><p><code>Graham Number = √(22.5 × EPS × BVPS)</code></p><p>本杰明·格雷厄姆在《聪明的投资者》中提出：防御型投资者买入价格不应超过每股收益的15倍和每股净资产的1.5倍。22.5 = 15 × 1.5。</p><h3>📊 使用说明</h3><p>输入公司的每股收益(EPS)和每股账面价值(BVPS)，计算器会输出格雷厄姆数字。如果股价低于计算结果，股票可能具备安全边际。</p>'
        },
        "en": {
            "title": "Free Online Graham Number Calculator",
            "short": "Graham Number Calculator",
            "desc": "Free online Graham Number Calculator based on Benjamin Graham's value investing formula. Input EPS and BVPS to calculate the fair value ceiling. Pure frontend computation.",
            "faq_title": "What is the Graham Number?",
            "faq_answer": "The Graham Number, developed by Benjamin Graham, estimates the fair value ceiling of a stock. Formula: <code>√(22.5 × EPS × BVPS)</code>, where 22.5 = 15× P/E × 1.5× P/B. If the stock price is below the Graham Number, it may be undervalued.",
            "hero_desc": "Free online Graham Number Calculator based on Benjamin Graham's value investing formula. Input EPS and BVPS to calculate the fair value ceiling. Pure frontend computation.",
            "calc_label": "Enter EPS and BVPS to calculate the Graham Number",
            "input1_label": "Earnings Per Share EPS:",
            "input1_val": "5.50",
            "input2_label": "Book Value Per Share BVPS:",
            "input2_val": "45.00",
            "result_label": "Graham Number",
            "formula": "√(22.5 × EPS × BVPS) = √(22.5 × 5.50 × 45.00)",
            "extra_input": '<div class="form-row"><label>Current Stock Price:</label><input type="number" id="price" value="65.00" step="any"></div>',
            "extra_labels": {"label2": "15×P/E=EPS×15", "label3": "1.5×P/B=BVPS×1.5", "label4": "Margin of Safety"},
            "info_html": '<h3>🎯 Graham Number Formula</h3><p><code>Graham Number = √(22.5 × EPS × BVPS)</code></p><p>Benjamin Graham proposed in "The Intelligent Investor" that defensive investors should pay no more than 15× earnings and 1.5× book value. 22.5 = 15 × 1.5.</p><h3>📊 How to Use</h3><p>Enter the company\'s EPS and BVPS. The calculator outputs the Graham Number. If the stock price is below the result, the stock may have a margin of safety.</p>'
        }
    },
    "intrinsic-value-calculator": {
        "cn": {
            "title": "免费在线内在价值计算器",
            "short": "内在价值计算器",
            "desc": "免费在线内在价值计算器，基于DCF折现现金流模型，输入自由现金流、增长率和折现率计算股票内在价值。纯前端本地计算。",
            "faq_title": "什么是内在价值？",
            "faq_answer": "内在价值是资产基于其基本面分析的公允价值。DCF模型通过将未来现金流折现回当前来计算。公式：<code>内在价值 = FCF × (1+g) / (r-g)</code>，其中FCF=自由现金流，g=永续增长率，r=折现率。",
            "hero_desc": "免费在线内在价值计算器，基于DCF折现现金流模型，输入自由现金流、增长率和折现率计算股票内在价值。纯前端本地计算。",
            "calc_label": "基于DCF折现现金流模型计算股票内在价值",
            "input1_label": "自由现金流 FCF：",
            "input1_id": "fcf",
            "input1_val": "100",
            "input2_label": "永续增长率 g (%)：",
            "input2_id": "growth",
            "input2_val": "3",
            "result_label": "内在价值",
            "formula": "FCF×(1+g)/(r-g)",
            "calc_js": """
var fcf=parseFloat(document.getElementById('fcf').value)||0;
var growth=parseFloat(document.getElementById('growth').value)||0;
var discount=parseFloat(document.getElementById('discount').value)||0;
var terminalGrowth=parseFloat(document.getElementById('terminalGrowth').value)||0;
var years=parseInt(document.getElementById('years').value)||5;
var g=growth/100,r=discount/100,tg=terminalGrowth/100;
var pvCashFlows=0;
var cf=fcf;
for(var i=1;i<=years;i++){
cf=cf*(1+g);
pvCashFlows+=cf/Math.pow(1+r,i);
}
var terminalValue=cf*(1+tg)/(r-tg);
var pvTerminal=terminalValue/Math.pow(1+r,years);
var intrinsic=(pvCashFlows+pvTerminal);
var perShare=intrinsic/(parseFloat(document.getElementById('shares').value)||1);
document.getElementById('val1').textContent='$'+intrinsic.toFixed(2)+'M';
document.getElementById('val2').textContent='$'+perShare.toFixed(2);
document.getElementById('val3').textContent='$'+pvCashFlows.toFixed(2)+'M';
document.getElementById('val4').textContent='$'+pvTerminal.toFixed(2)+'M';
""",
            "extra_input": '<div class="form-row"><label>折现率 r (%)：</label><input type="number" id="discount" value="10" step="any"></div><div class="form-row"><label>终值增长率 (%)：</label><input type="number" id="terminalGrowth" value="2" step="any"></div><div class="form-row"><label>预测年数：</label><input type="number" id="years" value="10" min="1" max="20" step="1"></div><div class="form-row"><label>总股数 (百万)：</label><input type="number" id="shares" value="100" step="any"></div>',
            "extra_labels": {"label2": "每股内在价值", "label3": "预测期现金流现值", "label4": "终值现值"},
            "info_html": '<h3>🎯 DCF内在价值公式</h3><p><code>内在价值 = Σ(FCF_t/(1+r)^t) + 终值/(1+r)^n</code></p><p>DCF（折现现金流）是最经典的企业估值方法，通过将未来所有现金流折现来评估企业价值。沃伦·巴菲特和查理·芒格都推崇此方法。</p>'
        },
        "en": {
            "title": "Free Online Intrinsic Value Calculator",
            "short": "Intrinsic Value Calculator",
            "desc": "Free online Intrinsic Value Calculator based on DCF (Discounted Cash Flow) model. Input free cash flow, growth rate, and discount rate. Pure frontend computation.",
            "faq_title": "What is Intrinsic Value?",
            "faq_answer": "Intrinsic value is the fair value of an asset based on fundamental analysis. The DCF model calculates it by discounting future cash flows to present. Formula: <code>Intrinsic Value = FCF × (1+g) / (r-g)</code>, where FCF=Free Cash Flow, g=perpetual growth, r=discount rate.",
            "hero_desc": "Free online Intrinsic Value Calculator based on DCF (Discounted Cash Flow) model. Input free cash flow, growth rate, and discount rate. Pure frontend computation.",
            "calc_label": "Calculate intrinsic value using the DCF model",
            "input1_label": "Free Cash Flow FCF:",
            "input1_val": "100",
            "input2_label": "Growth Rate g (%):",
            "input2_val": "3",
            "result_label": "Intrinsic Value",
            "formula": "FCF×(1+g)/(r-g)",
            "extra_input": '<div class="form-row"><label>Discount Rate r (%):</label><input type="number" id="discount" value="10" step="any"></div><div class="form-row"><label>Terminal Growth (%):</label><input type="number" id="terminalGrowth" value="2" step="any"></div><div class="form-row"><label>Forecast Years:</label><input type="number" id="years" value="10" min="1" max="20" step="1"></div><div class="form-row"><label>Shares (Millions):</label><input type="number" id="shares" value="100" step="any"></div>',
            "extra_labels": {"label2": "Per Share Value", "label3": "PV of Cash Flows", "label4": "PV of Terminal Value"},
            "info_html": '<h3>🎯 DCF Intrinsic Value Formula</h3><p><code>Intrinsic Value = Σ(FCF_t/(1+r)^t) + Terminal Value/(1+r)^n</code></p><p>DCF (Discounted Cash Flow) is the most classic business valuation method, assessing value by discounting all future cash flows. Used by Warren Buffett and Charlie Munger.</p>'
        }
    },
    "cost-basis-calculator": {
        "cn": {
            "title": "免费在线成本基础计算器",
            "short": "成本基础计算器",
            "desc": "免费在线成本基础计算器，计算股票投资的平均成本基础，支持多次买入、分红再投资和股票拆分调整。纯前端本地计算。",
            "faq_title": "什么是成本基础？",
            "faq_answer": "成本基础（Cost Basis）是投资者为计算资本利得税而确定资产原始价值的方法。公式：<code>成本基础 = 总投入金额 + 再投资分红 - 已回收资金</code>。准确计算成本基础对税务报告至关重要。",
            "hero_desc": "免费在线成本基础计算器，计算股票投资的平均成本基础，支持多次买入、分红再投资和股票拆分调整。纯前端本地计算。",
            "calc_label": "输入多次买入记录，计算加权平均成本基础",
            "input1_label": "买入批次：",
            "input1_id": "entries",
            "input1_val": "",
            "input2_label": "股票拆分比例（如2:1填2）：",
            "input2_id": "splitRatio",
            "input2_val": "1",
            "result_label": "加权平均成本",
            "formula": "总投入 ÷ 总股数",
            "calc_js": """
var splitRatio=parseFloat(document.getElementById('splitRatio').value)||1;
var entries=document.getElementById('entries').value.trim();
var totalCost=0,totalShares=0;
if(entries){
var lines=entries.split('\\n');
for(var i=0;i<lines.length;i++){
var parts=lines[i].split(/[,\\t ]+/);
if(parts.length>=2){
var shares=parseFloat(parts[0])||0;
var price=parseFloat(parts[1])||0;
totalShares+=shares;
totalCost+=shares*price;
}
}
}
totalShares*=splitRatio;
var avgCost=totalShares>0?totalCost/totalShares:0;
document.getElementById('val1').textContent='$'+avgCost.toFixed(2);
document.getElementById('val2').textContent=totalShares.toFixed(2);
document.getElementById('val3').textContent='$'+totalCost.toFixed(2);
var currentPrice=parseFloat(document.getElementById('currentPrice').value)||0;
if(currentPrice>0){
var gain=(currentPrice-avgCost)*totalShares;
var gainPct=avgCost>0?((currentPrice/avgCost)-1)*100:0;
document.getElementById('val4').textContent=(gain>=0?'+':'')+'$'+gain.toFixed(2)+' ('+gainPct.toFixed(2)+'%)';
}
""",
            "extra_input": '<div class="form-row"><label>当前股价：</label><input type="number" id="currentPrice" value="150" step="any"></div>',
            "extra_labels": {"label2": "调整后总股数", "label3": "总投入成本", "label4": "未实现盈亏"},
            "info_html": '<h3>📊 使用说明</h3><p>每行输入一笔买入记录，格式：<code>股数 价格</code>（空格或逗号分隔）。例如：</p><p><code>100 50<br>200 55<br>150 52</code></p><p>如有股票拆分，输入拆分比例（如2:1填2）。系统会自动计算加权平均成本和未实现盈亏。</p>'
        },
        "en": {
            "title": "Free Online Cost Basis Calculator",
            "short": "Cost Basis Calculator",
            "desc": "Free online Cost Basis Calculator for stock investments. Supports multiple purchases, dividend reinvestment, and stock split adjustments. Pure frontend computation.",
            "faq_title": "What is Cost Basis?",
            "faq_answer": "Cost Basis is the original value of an asset used to calculate capital gains tax. Formula: <code>Cost Basis = Total Invested + Reinvested Dividends - Return of Capital</code>. Accurate cost basis calculation is crucial for tax reporting.",
            "hero_desc": "Free online Cost Basis Calculator for stock investments. Supports multiple purchases, dividend reinvestment, and stock split adjustments. Pure frontend computation.",
            "calc_label": "Enter multiple purchase lots to calculate weighted average cost basis",
            "input1_label": "Purchase Lots:",
            "input1_val": "",
            "input2_label": "Split Ratio (e.g., 2 for 2:1):",
            "input2_val": "1",
            "result_label": "Weighted Avg Cost",
            "formula": "Total Cost ÷ Total Shares",
            "extra_input": '<div class="form-row"><label>Current Price:</label><input type="number" id="currentPrice" value="150" step="any"></div>',
            "extra_labels": {"label2": "Adjusted Shares", "label3": "Total Cost", "label4": "Unrealized G/L"},
            "info_html": '<h3>📊 How to Use</h3><p>Enter one purchase per line in format: <code>shares price</code> (space or comma separated). Example:</p><p><code>100 50<br>200 55<br>150 52</code></p><p>For stock splits, enter the split ratio (e.g., 2 for 2:1). The calculator computes weighted average cost and unrealized gain/loss.</p>'
        }
    },
    "athletic-performance-calculator": {
        "cn": {
            "title": "免费在线运动表现计算器",
            "short": "运动表现计算器",
            "desc": "免费在线运动表现计算器，计算VO₂max估算值、力量水平评级、BMI、体脂率和基础代谢率。输入年龄、体重和运动数据，获取综合体能评估。",
            "faq_title": "如何估算VO₂max？",
            "faq_answer": "VO₂max（最大摄氧量）是衡量心肺耐力的黄金标准。可用Rockport步行测试估算：<code>VO₂max = 132.853 - 0.0769×体重 - 0.3877×年龄 + 6.315×性别 - 3.2649×时间 - 0.1565×心率</code>。",
            "hero_desc": "免费在线运动表现计算器，计算VO₂max估算值、力量水平评级、BMI、体脂率和基础代谢率。输入年龄、体重和运动数据，获取综合体能评估。",
            "calc_label": "输入身体数据和运动表现，获取综合体能评估",
            "input1_label": "年龄：",
            "input1_id": "age",
            "input1_val": "30",
            "input2_label": "体重 (kg)：",
            "input2_id": "weight",
            "input2_val": "75",
            "result_label": "综合评分",
            "formula": "多指标综合评估",
            "calc_js": """
var age=parseInt(document.getElementById('age').value)||30;
var weight=parseFloat(document.getElementById('weight').value)||75;
var height=parseFloat(document.getElementById('height').value)||175;
var gender=document.getElementById('gender').value;
var bench=parseFloat(document.getElementById('bench').value)||0;
var squat=parseFloat(document.getElementById('squat').value)||0;
var deadlift=parseFloat(document.getElementById('deadlift').value)||0;
var run5k=parseFloat(document.getElementById('run5k').value)||0;
// BMI
var bmi=weight/Math.pow(height/100,2);
// Estimated body fat (US Navy method simplified)
var bfEst=(gender==='male')?(86.01*Math.log10(weight/Math.pow(height/100,2))-70.041+age*0.1):(163.205*Math.log10(weight/Math.pow(height/100,2))-97.684+age*0.1);
if(bfEst<3)bfEst=3;if(bfEst>55)bfEst=55;
// BMR (Mifflin-St Jeor)
var bmr=(gender==='male')?(10*weight+6.25*height-5*age+5):(10*weight+6.25*height-5*age-161);
// Strength score
var total=bench+squat+deadlift;
var wilks=total*500/((-216.0475144+16.2606339*weight-0.002388645*weight*weight-0.00113732*weight*weight*weight+7.01863e-6*weight*weight*weight*weight-1.291e-8*weight*weight*weight*weight*weight)||1);
var strengthLevel=total>0?(total/weight).toFixed(1)+'x':'-';
document.getElementById('val1').textContent=bmi.toFixed(1)+' (BMI)';
document.getElementById('val2').textContent=bfEst.toFixed(1)+'%';
document.getElementById('val3').textContent=bmr.toFixed(0)+' kcal';
document.getElementById('val4').textContent=wilks.toFixed(1)+' Wilks';
""",
            "extra_input": '<div class="form-row"><label>身高 (cm)：</label><input type="number" id="height" value="175" step="any"></div><div class="form-row"><label>性别：</label><select id="gender"><option value="male">男</option><option value="female">女</option></select></div><div class="form-row"><label>卧推 (kg)：</label><input type="number" id="bench" value="80" step="any"></div><div class="form-row"><label>深蹲 (kg)：</label><input type="number" id="squat" value="120" step="any"></div><div class="form-row"><label>硬拉 (kg)：</label><input type="number" id="deadlift" value="150" step="any"></div>',
            "extra_labels": {"label2": "估算体脂率", "label3": "基础代谢率", "label4": "力量评分"},
            "info_html": '<h3>🏋️ 综合运动表现评估</h3><p>本计算器基于多维度数据评估你的体能：</p><p><strong>BMI：</strong>体重(kg)/身高²(m)，评估体重状态。</p><p><strong>体脂率：</strong>基于海军方法估算。</p><p><strong>BMR：</strong>Mifflin-St Jeor公式计算基础代谢率。</p><p><strong>Wilks系数：</strong>力量举标准评分，消除体重差异。</p>'
        },
        "en": {
            "title": "Free Online Athletic Performance Calculator",
            "short": "Athletic Performance Calculator",
            "desc": "Free online Athletic Performance Calculator. Estimate VO₂max, strength level, BMI, body fat percentage, and BMR. Enter age, weight, and performance data for a comprehensive fitness assessment.",
            "faq_title": "How is athletic performance assessed?",
            "faq_answer": "Athletic performance is assessed through multiple dimensions: BMI (weight status), estimated body fat percentage (Navy method), BMR (Mifflin-St Jeor equation), and Wilks coefficient (standardized strength scoring that eliminates body weight differences).",
            "hero_desc": "Free online Athletic Performance Calculator. Estimate VO₂max, strength level, BMI, body fat percentage, and BMR. Enter age, weight, and performance data for a comprehensive fitness assessment.",
            "calc_label": "Enter body data and performance metrics for a comprehensive fitness assessment",
            "input1_label": "Age:",
            "input1_val": "30",
            "input2_label": "Weight (kg):",
            "input2_val": "75",
            "result_label": "Overall Score",
            "formula": "Multi-metric composite assessment",
            "extra_input": '<div class="form-row"><label>Height (cm):</label><input type="number" id="height" value="175" step="any"></div><div class="form-row"><label>Gender:</label><select id="gender"><option value="male">Male</option><option value="female">Female</option></select></div><div class="form-row"><label>Bench Press (kg):</label><input type="number" id="bench" value="80" step="any"></div><div class="form-row"><label>Squat (kg):</label><input type="number" id="squat" value="120" step="any"></div><div class="form-row"><label>Deadlift (kg):</label><input type="number" id="deadlift" value="150" step="any"></div>',
            "extra_labels": {"label2": "Est. Body Fat", "label3": "BMR", "label4": "Strength Score"},
            "info_html": '<h3>🏋️ Comprehensive Athletic Assessment</h3><p>This calculator evaluates your fitness across multiple dimensions:</p><p><strong>BMI:</strong> Weight(kg)/Height²(m) — assesses weight status.</p><p><strong>Body Fat %:</strong> Estimated using the Navy method.</p><p><strong>BMR:</strong> Mifflin-St Jeor equation for basal metabolic rate.</p><p><strong>Wilks Coefficient:</strong> Standardized powerlifting score that eliminates body weight differences.</p>'
        }
    }
}

def generate_tool(name, cfg, lang, is_cn=True):
    """Generate a tool HTML file"""
    c = cfg[lang]
    _dir = f"{BASE}/{name}" if is_cn else f"{BASE}/en/{name}"
    os.makedirs(_dir, exist_ok=True)
    
    lcode = "zh-CN" if is_cn else "en"
    hreflang_self = "zh" if is_cn else "en"
    hreflang_other = "en" if is_cn else "zh"
    canonical = f"https://free-toolbase.com/{name}/" if is_cn else f"https://free-toolbase.com/en/{name}/"
    alt_zh = f"https://free-toolbase.com/{name}/" if is_cn else f"https://free-toolbase.com/{name}/"
    alt_en = f"https://free-toolbase.com/en/{name}/" if is_cn else f"https://free-toolbase.com/en/{name}/"
    
    nav_home = "首页" if is_cn else "Home"
    nav_tools = "工具" if is_cn else "Tools"
    nav_back_href = "../index.html" if is_cn else "../index.html"
    lang_switch = f'<a href="index.html" class="active">中文</a><a href="../en/{name}/" class="">EN</a>' if is_cn else f'<a href="../{name}/" class="">中文</a><a href="index.html" class="active">EN</a>'
    breadcrumb_home = "首页" if is_cn else "Home"
    
    extra_input = c.get("extra_input", "")
    extra_labels = c.get("extra_labels", {})
    info_html = c.get("info_html", "")
    
    faqs = [
        (c["faq_title"], c["faq_answer"]),
        (f'{c["short"]}有什么使用限制吗？' if is_cn else f'Are there usage limits?',
         f'{c["short"]}是免费在线工具，没有使用次数限制。' if is_cn else f'The {c["short"]} is free with no usage limits.'),
        (f'{c["short"]}支持手机端使用吗？' if is_cn else f'Does it work on mobile?',
         f'支持。{c["short"]}采用响应式设计，可以在手机、平板和电脑上正常使用。' if is_cn else f'Yes, it uses responsive design and works on phones, tablets, and desktops.'),
        (f'数据安全吗？' if is_cn else 'Is my data secure?',
         f'安全。所有计算在浏览器中完成，数据不上传服务器。' if is_cn else 'All calculations happen in your browser — no data is uploaded to any server.'),
    ]
    faq_json = []
    for q, a in faqs:
        faq_json.append('{"@type": "Question", "name": "' + q.replace('"','\\"') + '", "acceptedAnswer": {"@type": "Answer", "text": "' + a.replace('"','\\"').replace('\n',' ') + '"}}')
    
    faq_html = ""
    for q, a in faqs:
        faq_html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>\n'
    
    # Build FAQ JSON
    faq_ld = '[' + ','.join(faq_json) + ']'
    
    # Extra result cards
    extra_cards = ""
    default_labels = {"label2": "指标2", "label3": "指标3", "label4": "指标4"}
    for k in ["label2", "label3", "label4"]:
        lbl = extra_labels.get(k, default_labels[k])
        vid = "val" + k[-1]
        extra_cards += f'<div class="card"><div class="label">{lbl}</div><div class="value" id="{vid}">--</div></div>\n'
    
    # Build copy function
    extra_copy = ""
    for k in ["label1", "label2", "label3", "label4"]:
        vid = "val" + k[-1]
        if k == "label1":
            extra_copy += f'var l1=document.getElementById("label1").textContent;var v1=document.getElementById("val1").textContent;if(v1!=="--")r.push(l1+": "+v1);\n'
        else:
            lbl = extra_labels.get(k, default_labels[k])
            extra_copy += f'var v{vid[-1]}=document.getElementById("{vid}").textContent;if(v{vid[-1]}!=="--")r.push("{lbl}: "+v{vid[-1]});\n'
    
    html = f'''<!DOCTYPE html>
<html lang="{lcode}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{c['desc']}">
<meta name="keywords" content="{c['title']},工具,在线工具,免费">
<title>{c['title']} | 无需注册</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{c['title']} | 无需注册">
<meta property="og:description" content="{c['desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{hreflang_self}" href="{canonical}">
<link rel="alternate" hreflang="{hreflang_other}" href="{alt_en if is_cn else alt_zh}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{c['title']}", "description": "{c['desc']}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": {faq_ld}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{c['title']}", "description": "如何使用{c['title']}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{c['title']}"}}, "step": [{{"@type": "HowToStep", "position": 1, "name": "输入数据", "text": "在输入框中输入需要计算的数值"}}, {{"@type": "HowToStep", "position": 2, "name": "选择选项", "text": "根据需要选择计算模式或参数"}}, {{"@type": "HowToStep", "position": 3, "name": "点击计算", "text": "点击计算按钮获取结果"}}, {{"@type": "HowToStep", "position": 4, "name": "查看结果", "text": "查看计算结果，支持一键复制"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "{breadcrumb_home}", "item": "{'https://free-toolbase.com/' if is_cn else 'https://free-toolbase.com/en/'}"}}, {{"@type": "ListItem", "position": 2, "name": "{nav_tools}", "item": "{'https://free-toolbase.com/#tools' if is_cn else 'https://free-toolbase.com/en/#tools'}"}}, {{"@type": "ListItem", "position": 3, "name": "{c['title']}", "item": "{canonical}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,{"PingFang SC","Microsoft YaHei" if is_cn else ""}sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.hero{{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);font-size:.9rem;color:#94a3b8}}
.hero .badge{{display:inline-block;margin-top:8px;background:rgba(6,182,212,.1);color:#22d3ee;padding:4px 10px;border-radius:4px;font-size:.75rem}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-row{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;align-items:center}}
.form-row label{{font-size:.9rem;color:#94a3b8;min-width:100px}}
.form-row input,.form-row select,.form-row textarea{{background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;font-size:.9rem;width:200px}}
.form-row textarea{{width:100%;min-height:100px;resize:vertical;font-family:monospace}}
.form-row input:focus,.form-row select:focus,.form-row textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-card{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
.card{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:16px;text-align:center}}
.card .label{{font-size:.8rem;color:#64748b;margin-bottom:4px}}
.card .value{{font-size:1.4rem;font-weight:700;color:#22d3ee}}
.card .sub{{font-size:.75rem;color:#64748b;margin-top:4px}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section code{{background:rgba(6,182,212,.1);color:#22d3ee;padding:2px 6px;border-radius:3px;font-size:.85rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.faq-section{{margin-top:24px}}
.faq-section h2{{margin-bottom:16px}}
.faq-item{{margin-bottom:12px;padding:14px 16px;border-radius:8px;background:#1e293b;border:1px solid rgba(148,163,184,.08);transition:border-color .2s}}
.faq-item:hover{{border-color:rgba(6,182,212,.2)}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px;cursor:pointer;display:flex;align-items:center;gap:8px}}
.faq-item h3::before{{content:'Q';display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.7rem;font-weight:700;flex-shrink:0}}
.faq-item p{{color:#94a3b8;font-size:.88rem;line-height:1.6;padding-left:30px}}
@media(max-width:600px){{.form-row{{flex-direction:column;align-items:flex-start}}.form-row label{{min-width:auto}}.form-row input,.form-row select,.form-row textarea{{width:100%}}.header{{flex-direction:column;gap:8px}}.header h1{{font-size:1.2rem}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>📊 {c['title']}</h1><div class="lang-switch">{lang_switch}</div></div>
<p class="nav-back"><a href="{nav_back_href}">{nav_home}</a> &rsaquo; <a href="{nav_back_href}#tools">{nav_tools}</a> &rsaquo; {c['title']}</p>
<div class="hero"><p>{c['hero_desc']} | {'无需注册 · 数据绝不上传服务器' if is_cn else 'No signup · Data never leaves your device'}</p><span class="badge">{'零依赖·可离线使用' if is_cn else 'Zero dependencies · Works offline'}</span></div>

<div class="input-section">
<h2>📊 {'输入数据' if is_cn else 'Input Data'}</h2>
<div class="form-row"><label>{c['input1_label']}</label><input type="{('number' if 'entries' not in c['input1_id'] else 'text')}" id="{c['input1_id']}" value="{c['input1_val']}" step="any"{(' placeholder="100 50\\n200 55\\n150 52"' if 'entries' in c['input1_id'] else '')}></div>
<div class="form-row"><label>{c['input2_label']}</label><input type="number" id="{c['input2_id']}" value="{c['input2_val']}" step="any"></div>
{extra_input}
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate()">🔍 {'计算' if is_cn else 'Calculate'}</button>
<button class="btn btn-secondary" onclick="resetAll()">🔄 {'重置' if is_cn else 'Reset'}</button>
<button class="btn btn-secondary" onclick="copyResults()">📋 {'复制结果' if is_cn else 'Copy Results'}</button>
</div>
</div>

<div class="result-section" id="resultSection">
<h2>📈 {'计算结果' if is_cn else 'Results'}</h2>
<div class="result-card">
<div class="card"><div class="label" id="label1">{c['result_label']}</div><div class="value" id="val1">--</div></div>
{extra_cards}
</div>
</div>

<div class="info-section">
<h2>📖 {'公式说明' if is_cn else 'Formula Guide'}</h2>
{info_html}
</div>

<div class="faq-section info-section">
<h2>❓ {'常见问题' if is_cn else 'FAQ'}</h2>
{faq_html}
</div>

<div class="footer">
<p>&copy; 2026 Free ToolBase. {'完全免费 · 无需注册 · 纯前端计算' if is_cn else '100% Free · No Signup · Client-Side Only'}</p>
<p><a href="{'../about/' if is_cn else '../about/'}">{'关于' if is_cn else 'About'}</a> <a href="{'../contact/' if is_cn else '../contact/'}">{'联系' if is_cn else 'Contact'}</a> <a href="{'../privacy/' if is_cn else '../privacy/'}">{'隐私' if is_cn else 'Privacy'}</a> <a href="{'../terms/' if is_cn else '../terms/'}">{'条款' if is_cn else 'Terms'}</a></p>
</div>
</div>
<div class="toast" id="toast"></div>

<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
function copyResults(){{var r=[];{extra_copy}if(r.length===0){{showToast("{'请先计算' if is_cn else 'Please calculate first'}");return}}navigator.clipboard.writeText(r.join('\\n')).then(function(){{showToast("{'已复制到剪贴板' if is_cn else 'Copied to clipboard'}")}}).catch(function(){{showToast("{'复制失败' if is_cn else 'Copy failed'}")}})}}
function calculate(){{{c['calc_js']}}}
function resetAll(){{var defaults={{}};defaults["{c['input1_id']}"]="{c['input1_val'] if 'entries' not in c['input1_id'] else ''}";defaults["{c['input2_id']}"]="{c['input2_val']}";for(var k in defaults){{var el=document.getElementById(k);if(el)el.value=defaults[k]}};document.getElementById('val1').textContent='--';document.getElementById('val2').textContent='--';document.getElementById('val3').textContent='--';document.getElementById('val4').textContent='--';}}
calculate();
</script>
</body>
</html>'''
    
    filepath = os.path.join(_dir, "index.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ {filepath}")

# Generate all tools
for name, cfg in tools.items():
    print(f"\n🔨 {name}:")
    generate_tool(name, cfg, "cn", is_cn=True)
    generate_tool(name, cfg, "en", is_cn=False)

print("\n✅ All 4 tools generated!")
