#!/usr/bin/env python3
"""批量生成4个新工具的CN+EN页面"""
import os, json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 4个工具定义
TOOLS = [
    {
        "slug": "holiday-savings-calculator",
        "icon": "🎄",
        "category_cn": "金融计算器",
        "category_en": "Finance Calculators",
        "name_cn": "节日储蓄计算器",
        "name_en": "Holiday Savings Calculator",
        "desc_cn": "在线规划节日开支储蓄计划，计算每月需存金额，轻松应对圣诞、春节等节日消费。纯前端计算，数据不上传服务器。",
        "desc_en": "Plan your holiday spending savings online, calculate monthly savings needed for Christmas, New Year and other holidays. Pure frontend, no data upload.",
        "keywords_cn": "节日储蓄,圣诞储蓄,春节储蓄,储蓄计划,节日预算,在线工具,免费",
        "keywords_en": "holiday savings,Christmas savings,savings plan,holiday budget,online tool,free",
        "inputs": [
            {"id": "totalBudget", "label_cn": "节日预算总额 (元)", "label_en": "Total Holiday Budget ($)", "type": "number", "default": "5000", "step": "100"},
            {"id": "monthsLeft", "label_cn": "距离节日还有几个月", "label_en": "Months until holiday", "type": "number", "default": "6", "min": "1", "max": "24"},
            {"id": "currentSavings", "label_cn": "当前已存金额 (元)", "label_en": "Current Savings ($)", "type": "number", "default": "1000", "step": "100"},
        ],
        "calc_logic": """
  var totalBudget=parseFloat(el('totalBudget').value)||0;
  var monthsLeft=parseFloat(el('monthsLeft').value)||1;
  var currentSavings=parseFloat(el('currentSavings').value)||0;
  var remaining=totalBudget-currentSavings;
  var monthly=remaining/monthsLeft;
  var weekly=monthly/4.345;
  var daily=monthly/30.44;
  var pctAchieved=(currentSavings/totalBudget)*100;
"""
    },
    {
        "slug": "pet-cost-calculator",
        "icon": "🐾",
        "category_cn": "生活计算器",
        "category_en": "Lifestyle Calculators",
        "name_cn": "宠物养育成本计算器",
        "name_en": "Pet Cost Calculator",
        "desc_cn": "估算养宠物的年度和终身花费，包括食物、医疗、美容等开支，帮您做好养宠预算规划。纯前端计算，数据不上传服务器。",
        "desc_en": "Estimate annual and lifetime pet ownership costs including food, vet care, grooming, etc. Plan your pet budget wisely. Pure frontend, no data upload.",
        "keywords_cn": "宠物成本,养宠物花费,狗开销,猫开销,宠物预算,在线工具,免费",
        "keywords_en": "pet cost,dog cost,cat cost,pet budget,pet ownership cost,online tool,free",
        "inputs": [
            {"id": "petType", "label_cn": "宠物类型", "label_en": "Pet Type", "type": "select", "options": [{"v":"dog","cn":"🐕 狗","en":"🐕 Dog"},{"v":"cat","cn":"🐈 猫","en":"🐈 Cat"},{"v":"rabbit","cn":"🐰 兔子","en":"🐰 Rabbit"},{"v":"hamster","cn":"🐹 仓鼠","en":"🐹 Hamster"}], "default": "dog"},
            {"id": "petSize", "label_cn": "体型大小", "label_en": "Size", "type": "select", "options": [{"v":"small","cn":"小型","en":"Small"},{"v":"medium","cn":"中型","en":"Medium"},{"v":"large","cn":"大型","en":"Large"}], "default": "medium"},
            {"id": "years", "label_cn": "预期寿命 (年)", "label_en": "Expected Lifespan (years)", "type": "number", "default": "12", "min": "1", "max": "30"},
            {"id": "foodMonthly", "label_cn": "每月食物花费 (元)", "label_en": "Monthly Food Cost ($)", "type": "number", "default": "200", "step": "10"},
            {"id": "vetYearly", "label_cn": "每年医疗花费 (元)", "label_en": "Annual Vet Cost ($)", "type": "number", "default": "1500", "step": "50"},
            {"id": "groomMonthly", "label_cn": "每月美容护理 (元)", "label_en": "Monthly Grooming ($)", "type": "number", "default": "100", "step": "10"},
            {"id": "otherMonthly", "label_cn": "每月其他花费 (元)", "label_en": "Monthly Other ($)", "type": "number", "default": "80", "step": "10"},
            {"id": "adoptionFee", "label_cn": "领养/购买费用 (元)", "label_en": "Adoption/Purchase Fee ($)", "type": "number", "default": "500", "step": "50", "note_cn": "一次性费用", "note_en": "One-time fee"},
        ],
        "calc_logic": """
  var years=parseFloat(el('years').value)||12;
  var foodMonthly=parseFloat(el('foodMonthly').value)||0;
  var vetYearly=parseFloat(el('vetYearly').value)||0;
  var groomMonthly=parseFloat(el('groomMonthly').value)||0;
  var otherMonthly=parseFloat(el('otherMonthly').value)||0;
  var adoptionFee=parseFloat(el('adoptionFee').value)||0;
  var monthlyTotal=foodMonthly+groomMonthly+otherMonthly;
  var yearlyTotal=monthlyTotal*12+vetYearly;
  var lifetimeTotal=yearlyTotal*years+adoptionFee;
"""
    },
    {
        "slug": "gardening-cost-calculator",
        "icon": "🌱",
        "category_cn": "生活计算器",
        "category_en": "Lifestyle Calculators",
        "name_cn": "家庭园艺成本计算器",
        "name_en": "Gardening Cost Calculator",
        "desc_cn": "规划家庭园艺预算，计算种子、肥料、工具和水费等开支，估算种植蔬菜/花卉的成本与收益。纯前端计算。",
        "desc_en": "Plan your home gardening budget, calculate costs for seeds, fertilizer, tools and water bills. Estimate ROI of growing vegetables and flowers. Pure frontend.",
        "keywords_cn": "园艺成本,种菜成本,花园花费,园艺预算,种植,在线工具,免费",
        "keywords_en": "gardening cost,growing vegetables cost,garden budget,planting,online tool,free",
        "inputs": [
            {"id": "gardenArea", "label_cn": "种植面积 (平方米)", "label_en": "Garden Area (sq ft)", "type": "number", "default": "20", "step": "1"},
            {"id": "months", "label_cn": "种植周期 (月)", "label_en": "Growing Season (months)", "type": "number", "default": "6", "min": "1", "max": "12"},
            {"id": "seedsCost", "label_cn": "种子/幼苗费用 (元)", "label_en": "Seeds/Seedlings Cost ($)", "type": "number", "default": "200"},
            {"id": "soilCost", "label_cn": "土壤肥料费用 (元)", "label_en": "Soil & Fertilizer ($)", "type": "number", "default": "300"},
            {"id": "toolCost", "label_cn": "工具费用 (元)", "label_en": "Tools Cost ($)", "type": "number", "default": "400", "note_cn": "一次性投入", "note_en": "One-time"},
            {"id": "waterMonthly", "label_cn": "每月水费增加 (元)", "label_en": "Monthly Water Cost ($)", "type": "number", "default": "50"},
            {"id": "harvestValue", "label_cn": "预期收获价值 (元)", "label_en": "Expected Harvest Value ($)", "type": "number", "default": "800", "note_cn": "蔬菜花卉总价值", "note_en": "Total produce value"},
        ],
        "calc_logic": """
  var months=parseFloat(el('months').value)||6;
  var seedsCost=parseFloat(el('seedsCost').value)||0;
  var soilCost=parseFloat(el('soilCost').value)||0;
  var toolCost=parseFloat(el('toolCost').value)||0;
  var waterMonthly=parseFloat(el('waterMonthly').value)||0;
  var harvestValue=parseFloat(el('harvestValue').value)||0;
  var monthlyCost=seedsCost/months+soilCost/months+waterMonthly;
  var totalCost=seedsCost+soilCost+toolCost+waterMonthly*months;
  var netValue=harvestValue-totalCost;
  var roi=(totalCost>0?((harvestValue/totalCost)-1)*100:0);
"""
    },
    {
        "slug": "side-hustle-calculator",
        "icon": "💼",
        "category_cn": "金融计算器",
        "category_en": "Finance Calculators",
        "name_cn": "副业收入计算器",
        "name_en": "Side Hustle Calculator",
        "desc_cn": "估算副业收入与时薪，对比不同副业方案的收益，帮您找到最优兼职方向。纯前端计算，数据不上传服务器。",
        "desc_en": "Estimate side hustle income and hourly rate, compare different side gig options to find the best part-time path. Pure frontend, no data upload.",
        "keywords_cn": "副业收入,时薪计算,兼职,副业规划,在线工具,免费",
        "keywords_en": "side hustle,side gig,hourly rate,part time income,freelance,online tool,free",
        "inputs": [
            {"id": "hoursPerWeek", "label_cn": "每周投入时间 (小时)", "label_en": "Hours per week", "type": "number", "default": "10", "min": "1", "max": "80"},
            {"id": "hourlyRate", "label_cn": "预期时薪 (元)", "label_en": "Expected Hourly Rate ($)", "type": "number", "default": "80", "step": "5"},
            {"id": "weeksPerYear", "label_cn": "每年工作周数", "label_en": "Working weeks per year", "type": "number", "default": "48", "min": "1", "max": "52"},
            {"id": "expensePerMonth", "label_cn": "每月副业开销 (元)", "label_en": "Monthly Expenses ($)", "type": "number", "default": "200"},
            {"id": "taxRate", "label_cn": "税率 (%)", "label_en": "Tax Rate (%)", "type": "number", "default": "20", "min": "0", "max": "60", "note_cn": "副业收入通常需缴税", "note_en": "Side income usually taxable"},
        ],
        "calc_logic": """
  var hoursPerWeek=parseFloat(el('hoursPerWeek').value)||0;
  var hourlyRate=parseFloat(el('hourlyRate').value)||0;
  var weeksPerYear=parseFloat(el('weeksPerYear').value)||48;
  var expensePerMonth=parseFloat(el('expensePerMonth').value)||0;
  var taxRate=parseFloat(el('taxRate').value)||0;
  var monthlyGross=hoursPerWeek*4.345*hourlyRate;
  var yearlyGross=hoursPerWeek*weeksPerYear*hourlyRate;
  var yearlyExpense=expensePerMonth*12;
  var yearlyNet=yearlyGross-yearlyExpense;
  var yearlyAfterTax=yearlyNet*(1-taxRate/100);
  var monthlyNet=yearlyNet/12;
"""
    },
]

# ---------- HTML模板 (CN) ----------
def gen_cn(t):
    ic = t["icon"]
    inputs_html = ""
    dynamic_fields_js = ""
    for inp in t["inputs"]:
        if inp["type"] == "select":
            opts_html = ""
            for o in inp["options"]:
                sel = ' selected' if o["v"] == inp.get("default", "") else ''
                opts_html += f'<option value="{o["v"]}"{sel}>{o["cn"]}</option>'
            note = inp.get("note_cn", "")
            note_html = f'<span style="color:#64748b;font-size:.75rem;margin-left:8px">{note}</span>' if note else ""
            inputs_html += f'<div class="form-group"><label>{inp["label_cn"]}{note_html}</label><select id="{inp["id"]}">{opts_html}</select></div>'
        else:
            note = inp.get("note_cn", "")
            note_html = f' <span style="color:#64748b;font-size:.75rem">({note})</span>' if note else ""
            min_attr = f' min="{inp["min"]}"' if "min" in inp else ""
            max_attr = f' max="{inp["max"]}"' if "max" in inp else ""
            step_attr = f' step="{inp["step"]}"' if "step" in inp else ' step="1"'
            inputs_html += f'<div class="form-group"><label>{inp["label_cn"]}{note_html}</label><input type="number" id="{inp["id"]}" value="{inp["default"]}"{min_attr}{max_attr}{step_attr}></div>'

    # Build result display fields dynamically from calc_logic
    result_display = ""
    if "totalBudget" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">剩余需存金额</span><span class="result-value" id="resRemaining">-</span></div>'+
    '<div class="result-item"><span class="result-label">每月需存</span><span class="result-value" id="resMonthly">-</span></div>'+
    '<div class="result-item"><span class="result-label">每周需存</span><span class="result-value" id="resWeekly">-</span></div>'+
    '<div class="result-item"><span class="result-label">每日需存</span><span class="result-value" id="resDaily">-</span></div>'+
    '<div class="result-item"><span class="result-label">当前进度</span><span class="result-value" id="resProgress">-</span></div>';"""
        set_values = """
  el('resRemaining').textContent=fmtCur1(remaining);
  el('resMonthly').textContent=fmtCur1(monthly);
  el('resWeekly').textContent=fmtCur1(weekly);
  el('resDaily').textContent=fmtCur1(daily);
  el('resProgress').textContent=fmtPct(pctAchieved);"""
    elif "adoptionFee" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">每月总花费</span><span class="result-value" id="resMonthly">-</span></div>'+
    '<div class="result-item"><span class="result-label">每年总花费</span><span class="result-value" id="resYearly">-</span></div>'+
    '<div class="result-item"><span class="result-label">一生总花费</span><span class="result-value" id="resLifetime">-</span></div>'+
    '<div class="result-item"><span class="result-label">一次性费用</span><span class="result-value" id="resOneTime">-</span></div>';"""
        set_values = """
  el('resMonthly').textContent=fmtCur1(monthlyTotal);
  el('resYearly').textContent=fmtCur1(yearlyTotal);
  el('resLifetime').textContent=fmtCur1(lifetimeTotal);
  el('resOneTime').textContent=fmtCur1(adoptionFee);"""
    elif "harvestValue" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">总投入</span><span class="result-value" id="resTotalCost">-</span></div>'+
    '<div class="result-item"><span class="result-label">预期收获</span><span class="result-value" id="resHarvest">-</span></div>'+
    '<div class="result-item"><span class="result-label">净收益</span><span class="result-value" id="resNet">-</span></div>'+
    '<div class="result-item"><span class="result-label">投资回报率</span><span class="result-value" id="resROI">-</span></div>'+
    '<div class="result-item"><span class="result-label">月均成本</span><span class="result-value" id="resMonthlyCost">-</span></div>';"""
        set_values = """
  el('resTotalCost').textContent=fmtCur1(totalCost);
  el('resHarvest').textContent=fmtCur1(harvestValue);
  el('resNet').textContent=fmtCur1(netValue);
  el('resROI').textContent=fmtPct(roi);
  el('resMonthlyCost').textContent=fmtCur1(monthlyCost);"""
    else:  # side-hustle
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">月收入 (税前)</span><span class="result-value" id="resMonthlyGross">-</span></div>'+
    '<div class="result-item"><span class="result-label">年收入 (税前)</span><span class="result-value" id="resYearlyGross">-</span></div>'+
    '<div class="result-item"><span class="result-label">年净收入 (税后)</span><span class="result-value highlight" id="resYearlyNet">-</span></div>'+
    '<div class="result-item"><span class="result-label">实际时薪 (税后)</span><span class="result-value" id="resEffectiveRate">-</span></div>'+
    '<div class="result-item"><span class="result-label">年度总工时</span><span class="result-value" id="resTotalHours">-</span></div>';"""
        set_values = """
  el('resMonthlyGross').textContent=fmtCur1(monthlyGross);
  el('resYearlyGross').textContent=fmtCur1(yearlyGross);
  el('resYearlyNet').textContent=fmtCur1(yearlyAfterTax);
  el('resEffectiveRate').textContent=fmtCur1(yearlyAfterTax/(hoursPerWeek*weeksPerYear));
  el('resTotalHours').textContent=(hoursPerWeek*weeksPerYear)+' 小时';"""

    related_tools = '[' + ','.join([
        '{"icon":"🧮","name":"复利计算器","url":"compound-interest-calculator/"}',
        '{"icon":"💰","name":"储蓄目标计算器","url":"savings-goal-calculator/"}',
        '{"icon":"📊","name":"预算规划器","url":"budget-planner/"}',
        '{"icon":"📈","name":"投资回报计算器","url":"roi-calculator-simple/"}'
    ]) + ']'

    # FAQ
    if "totalBudget" in t["calc_logic"]:
        faq = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"为什么要提前规划节日储蓄？","acceptedAnswer":{"@type":"Answer","text":"节日消费往往集中在年底（圣诞、元旦、春节），提前按月储蓄可以避免年底一次性大额支出的压力。本计算器帮您分摊到每月，让节日消费更从容。"}},{"@type":"Question","name":"应该提前多长时间开始储蓄？","acceptedAnswer":{"@type":"Answer","text":"建议提前6-12个月开始规划。越早开始，每月需要存的金额越少。本工具可以帮您计算不同时间跨度的月存金额，找到最舒适的储蓄节奏。"}},{"@type":"Question","name":"节日预算应该包含哪些开支？","acceptedAnswer":{"@type":"Answer","text":"节日预算通常包括：礼物、聚餐、旅行、装饰品、新衣服等。建议先列出所有预期开支，再用本计算器倒推每月储蓄金额。"}}]}</script>"""
        howto_steps = '[{"@type":"HowToStep","position":1,"name":"输入预算总额","text":"输入您计划的节日总开支"},{"@type":"HowToStep","position":2,"name":"设置时间","text":"设置距离节日还有几个月"},{"@type":"HowToStep","position":3,"name":"输入已存金额","text":"输入当前已储蓄的金额"},{"@type":"HowToStep","position":4,"name":"查看储蓄计划","text":"查看每月、每周、每日需要储蓄的金额"}]'
        explain_html = """<div class="info-section"><h2>📖 使用教程</h2>
<p>本节日储蓄计算器帮您规划节日消费预算，按时间分摊储蓄任务：</p>
<h3>第一步：设定节日预算总额</h3><p>盘点您预期的所有节日支出（礼物、聚餐、旅行、装饰等），填入预算总额。</p>
<h3>第二步：设置剩余时间</h3><p>输入距离节日还有多少个月。越早规划，每月需要存的金额越少。</p>
<h3>第三步：输入已有储蓄</h3><p>如果已经存了一部分钱，填入当前余额，系统会帮您计算剩余缺口。</p>
<h3>第四步：查看储蓄计划</h3><p>计算器会显示剩余缺口对应的月/周/日储蓄金额，帮您制定可行的储蓄节奏。</p></div>
<div class="info-section"><h2>💡 储蓄小贴士</h2><ul><li><strong>自动转账：</strong>设置每月自动从工资账户转入储蓄账户，避免忘记。</li><li><strong>52周挑战：</strong>从第一周存1元开始，每周递增，年底可存1378元。</li><li><strong>购物清单：</strong>提前列出礼物清单，趁打折季购买可以省30%-50%。</li><li><strong>DIY礼物：</strong>手工制作的礼物更有心意，且成本更低。</li></ul></div>"""
    elif "adoptionFee" in t["calc_logic"]:
        faq = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"养一只狗一年要花多少钱？","acceptedAnswer":{"@type":"Answer","text":"根据美国ASPCA数据，养一只中型犬年均花费约$1,400-$4,300（含食物$250-$700、医疗$500-$1,500、美容$200-$500等）。本计算器可帮您按实际情况估算。"}},{"@type":"Question","name":"猫比狗省钱吗？","acceptedAnswer":{"@type":"Answer","text":"通常是的。猫的食物消耗较少，一般不需要专业美容，年均花费约$800-$2,000，比狗低30%-50%。具体取决于品种、健康状况和生活方式。"}},{"@type":"Question","name":"领养和购买宠物哪个更划算？","acceptedAnswer":{"@type":"Answer","text":"领养通常只需支付$50-$200的领养费（已包含首轮疫苗和绝育），而购买纯种犬猫可能需要$500-$3,000+。领养不仅省钱，还能给流浪动物一个家。"}}]}</script>"""
        howto_steps = '[{"@type":"HowToStep","position":1,"name":"选择宠物类型","text":"选择您想养的宠物类型（狗/猫/兔子/仓鼠）"},{"@type":"HowToStep","position":2,"name":"设置体型和寿命","text":"设置宠物体型和预期寿命"},{"@type":"HowToStep","position":3,"name":"填写各项花费","text":"填写每月食物、医疗、美容等预估花费"},{"@type":"HowToStep","position":4,"name":"查看总花费","text":"查看年度和终身养宠总花费"}]'
        explain_html = """<div class="info-section"><h2>📖 使用教程</h2>
<p>本宠物养育成本计算器帮您全面估算养宠物的各项花费：</p>
<h3>第一步：选择宠物类型</h3><p>猫、狗、兔子、仓鼠等不同类型的宠物花费差异很大。</p>
<h3>第二步：设置体型和寿命</h3><p>大型犬的食物、医疗费用通常比小型犬高50%以上。</p>
<h3>第三步：填写各项花费</h3><p>包括食物、医疗、美容、其他（玩具/零食/保险等）和一次性领养费用。</p>
<h3>第四步：查看总花费</h3><p>计算器会显示每月、每年和一生总花费，帮您评估是否做好养宠准备。</p></div>
<div class="info-section"><h2>💡 省钱养宠建议</h2><ul><li><strong>领养代替购买：</strong>庇护所领养费用远低于购买，且已包含基础医疗。</li><li><strong>批量购买食物：</strong>大包装宠物食品通常单价更低，保存得当可省20%-30%。</li><li><strong>宠物保险：</strong>每月$30-$50的保费可避免意外大额医疗支出。</li><li><strong>DIY美容：</strong>学习基础剪毛、洗澡可以节省大量美容费用。</li></ul></div>"""
    elif "harvestValue" in t["calc_logic"]:
        faq = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"自己种菜能省多少钱？","acceptedAnswer":{"@type":"Answer","text":"根据美国园艺协会数据，一个20平米的菜园每年可产出价值$500-$1,200的蔬菜。扣除成本后净收益约$300-$800。西红柿、生菜、豆角是回报率最高的蔬菜。"}},{"@type":"Question","name":"新手园艺需要哪些基础投入？","acceptedAnswer":{"@type":"Answer","text":"基础投入包括：铲子（¥30）、锄头（¥50）、浇水壶（¥20）、手套（¥15）等工具约¥100-300，以及种子和肥料约¥100。本计算器已包含这些一次性投入。"}},{"@type":"Question","name":"哪些蔬菜最容易种、回报最高？","acceptedAnswer":{"@type":"Answer","text":"初学者推荐：生菜（30天收获）、小番茄（60天）、辣椒（70天）、豆角（50天）、黄瓜（60天）。这些病虫害少、产量高，非常适合新手入门。"}}]}</script>"""
        howto_steps = '[{"@type":"HowToStep","position":1,"name":"输入种植面积","text":"输入您的种植面积（平方米）"},{"@type":"HowToStep","position":2,"name":"设置种植周期","text":"设置种植季节的月份数"},{"@type":"HowToStep","position":3,"name":"填写各项成本","text":"填写种子、土壤肥料、工具、水费等成本"},{"@type":"HowToStep","position":4,"name":"设置预期收获","text":"填写预期收获的蔬菜/花卉总价值"},{"@type":"HowToStep","position":5,"name":"查看投入产出比","text":"查看总成本、净收益和投资回报率"}]'
        explain_html = """<div class="info-section"><h2>📖 使用教程</h2>
<p>本家庭园艺成本计算器帮您分析种菜的投入产出比：</p>
<h3>第一步：输入种植面积</h3><p>以平方米为单位，一般阳台种植3-5平米，院子种植10-30平米。</p>
<h3>第二步：设置种植周期</h3><p>一般春夏季种植周期为4-8个月，可根据当地气候调整。</p>
<h3>第三步：填写各项成本</h3><p>包括种子/幼苗、土壤肥料、工具（一次性）和每月水费增加。</p>
<h3>第四步：设置预期收获</h3><p>估算整个季节能收获的蔬菜/花卉总价值，可用菜市场零售价参考。</p>
<h3>第五步：查看分析</h3><p>系统会显示总投入、净收益和ROI，帮您判断是否值得投入。</p></div>
<div class="info-section"><h2>💡 高回报蔬菜推荐</h2><ul><li><strong>小番茄（樱桃番茄）：</strong>3株可收20-30斤，超市价¥15/斤，回报率可达300%+</li><li><strong>生菜/沙拉菜：</strong>30天速生，可多次收割，几乎没有虫害</li><li><strong>香草类：</strong>罗勒、薄荷、香菜等超市按小包装卖很贵，自己种成本极低</li><li><strong>豆角：</strong>产量高、管理简单，是单位面积产量最高的蔬菜之一</li></ul></div>"""
    else:  # side-hustle
        faq = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"做副业需要交税吗？","acceptedAnswer":{"@type":"Answer","text":"是的，副业收入通常需要缴纳个人所得税。中国综合所得适用3%-45%累进税率，美国self-employment需缴纳15.3%自雇税+联邦/州所得税。本计算器默认20%税率，您可根据实际情况调整。"}},{"@type":"Question","name":"哪些副业时薪最高？","acceptedAnswer":{"@type":"Answer","text":"高时薪副业包括：软件开发（$50-150/小时）、设计（$30-100/小时）、翻译（$20-60/小时）、线上教学（$15-50/小时）。使用本计算器可以对比不同时薪方案的年度收入差异。"}},{"@type":"Question","name":"每周花多少时间做副业合适？","acceptedAnswer":{"@type":"Answer","text":"建议每周5-15小时，不影响主业和休息。以时薪$50、每周10小时为例，年收入约$24,000。本计算器可以帮您找到最佳投入产出平衡点。"}}]}</script>"""
        howto_steps = '[{"@type":"HowToStep","position":1,"name":"输入每周时间","text":"输入您计划每周投入副业的小时数"},{"@type":"HowToStep","position":2,"name":"设置预期时薪","text":"设置您期望的时薪收入"},{"@type":"HowToStep","position":3,"name":"输入开销和税率","text":"填写副业相关开销和适用税率"},{"@type":"HowToStep","position":4,"name":"查看收入预估","text":"查看月收入、年收入、税后净收入和实际时薪"}]'
        explain_html = """<div class="info-section"><h2>📖 使用教程</h2>
<p>本副业收入计算器帮您估算兼职/副业的潜在收入：</p>
<h3>第一步：输入每周时间</h3><p>合理评估您每周能稳定投入副业的时间，建议5-15小时。</p>
<h3>第二步：设置预期时薪</h3><p>根据您的技能水平和市场需求设定预期时薪。技术类通常$30-80/小时。</p>
<h3>第三步：填写开销和税率</h3><p>副业可能有平台佣金、设备、交通等开销。税率根据所在国家和收入水平调整。</p>
<h3>第四步：查看收入预估</h3><p>计算器展示月收入、年收入、税后净收入，以及扣除各种开销后的实际时薪。</p></div>
<div class="info-section"><h2>💡 高时薪副业推荐</h2><ul><li><strong>自由职业开发：</strong>Upwork/Fiverr承接编程项目，时薪$30-$150</li><li><strong>在线辅导/教学：</strong>英语、数学、编程等科目，时薪$15-$50</li><li><strong>内容创作：</strong>写作、视频剪辑、平面设计，时薪$20-$80</li><li><strong>本地服务：</strong>遛狗、家教、摄影，可自由定价</li></ul></div>"""

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['desc_cn']}">
<meta name="keywords" content="{t['keywords_cn']}">
<title>免费在线{t['name_cn']} | 无需注册</title>
<link rel="canonical" href="https://free-toolbase.com/{t['slug']}/">
<meta property="og:title" content="免费在线{t['name_cn']} | 无需注册">
<meta property="og:description" content="{t['desc_cn']}">
<meta property="og:url" content="https://free-toolbase.com/{t['slug']}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{t['slug']}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{t['slug']}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{t['slug']}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"在线{t['name_cn']}","description":"{t['desc_cn']}","applicationCategory":"UtilityApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
{faq}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{t['name_cn']}","description":"使用{t['name_cn']}的步骤指南","totalTime":"PT3M","tool":{{"@type":"HowToTool","name":"{t['name_cn']}"}},"step":{howto_steps}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"在线{t['name_cn']}","item":"https://free-toolbase.com/{t['slug']}/"}}]}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1c40f}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.form-group{{margin-bottom:12px}}
.form-group label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.result-section{{background:#0f172a;border-radius:8px;padding:16px;border:1px solid rgba(6,182,212,.3);margin-top:16px;display:none}}
.result-section .result-title{{font-size:1rem;color:#f1c40f;margin-bottom:8px}}
.result-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.08);flex-wrap:wrap}}
.result-item:last-child{{border-bottom:none}}
.result-label{{color:#94a3b8;font-size:.9rem}}
.result-value{{color:#22d3ee;font-size:.95rem;font-weight:600}}.result-value.highlight{{color:#f1c40f;font-size:1.1rem}}
.btn-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:500}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.35)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{list-style:none;padding-left:0}}
.info-section ul li{{color:#94a3b8;font-size:.9rem;margin-bottom:6px;padding-left:20px;position:relative}}
.info-section ul li::before{{content:"•";position:absolute;left:6px;color:#22d3ee}}
.related-tools{{margin-top:24px}}
.related-tools h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
.related-item{{background:#1e293b;border-radius:8px;padding:12px;border:1px solid rgba(148,163,184,.1);transition:all .2s}}
.related-item:hover{{border-color:rgba(6,182,212,.3)}}
.related-item a{{color:#e2e8f0;font-size:.9rem}}
.related-item a:hover{{color:#22d3ee}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto 20px;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}
@media(max-width:640px){{.header h1{{font-size:1.2rem}}.section{{padding:14px}}.related-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{ic} {t['name_cn']}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{t['slug']}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {t['name_cn']}</p>
<div class="hero"><p>{t['desc_cn']} | 无需注册 · 数据绝不上传服务器</p><span class="badge">零依赖·可离线使用</span></div>

<div class="section">
<h2>🔢 输入参数</h2>
{inputs_html}
<div class="btn-row">
<button class="btn btn-primary" id="calcBtn">🧮 开始计算</button>
<button class="btn btn-secondary" id="clearBtn">🔄 重置</button>
</div>
<div class="result-section" id="resultSection">
<div class="result-title">📊 计算结果</div>
<div id="resultContent"></div>
<div class="btn-row" style="margin-top:12px"><button class="btn btn-secondary" id="copyBtn">📋 复制结果</button></div>
</div>
</div>

<div class="related-tools"><h2>🔗 相关工具</h2><div class="related-grid" id="relatedGrid"></div></div>

{explain_html}

<div class="ad-slot">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>
</div>

<footer class="footer">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{t['slug']}/">EN</a>
</div>
<p>在线{t['name_cn']} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
</div>

<div class="toast" id="toast"></div>

<script>
(function(){{
var el=function(id){{return document.getElementById(id);}};
var toastTimer=null;
function showToast(msg){{var t=el('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){{t.classList.remove('show');}},2500);}}
function fmtCur1(n){{return '¥'+n.toLocaleString('zh-CN',{{minimumFractionDigits:2,maximumFractionDigits:2}});}}
function fmtPct(n){{return n.toFixed(2)+'%';}}

function calculate(){{
{t['calc_logic']}
{result_display}
{set_values}
  el('resultSection').style.display='block';
}}

el('calcBtn').addEventListener('click',calculate);
el('clearBtn').addEventListener('click',function(){{location.reload();}});
el('copyBtn').addEventListener('click',function(){{
  var results=document.querySelectorAll('#resultContent .result-item');
  var text='{t['name_cn']} - 计算结果\\n';
  results.forEach(function(r){{text+=r.querySelector('.result-label').textContent+': '+r.querySelector('.result-value').textContent+'\\n';}});
  navigator.clipboard.writeText(text).then(function(){{showToast('结果已复制到剪贴板');}}).catch(function(){{showToast('复制失败，请手动复制');}});
}});

var relatedTools={related_tools};
var rg=el('relatedGrid');
relatedTools.forEach(function(rt){{var d=document.createElement('div');d.className='related-item';d.innerHTML='<a href="../'+rt.url+'">'+rt.icon+' '+rt.name+'</a>';rg.appendChild(d);}});

calculate();
}})();
</script>
</body>
</html>'''
    return html


# ---------- HTML模板 (EN) ----------
def gen_en(t):
    ic = t["icon"]
    inputs_html = ""
    for inp in t["inputs"]:
        if inp["type"] == "select":
            opts_html = ""
            for o in inp["options"]:
                sel = ' selected' if o["v"] == inp.get("default", "") else ''
                opts_html += f'<option value="{o["v"]}"{sel}>{o["en"]}</option>'
            note = inp.get("note_en", "")
            note_html = f'<span style="color:#64748b;font-size:.75rem;margin-left:8px">{note}</span>' if note else ""
            inputs_html += f'<div class="form-group"><label>{inp["label_en"]}{note_html}</label><select id="{inp["id"]}">{opts_html}</select></div>'
        else:
            note = inp.get("note_en", "")
            note_html = f' <span style="color:#64748b;font-size:.75rem">({note})</span>' if note else ""
            min_attr = f' min="{inp["min"]}"' if "min" in inp else ""
            max_attr = f' max="{inp["max"]}"' if "max" in inp else ""
            step_attr = f' step="{inp["step"]}"' if "step" in inp else ' step="1"'
            inputs_html += f'<div class="form-group"><label>{inp["label_en"]}{note_html}</label><input type="number" id="{inp["id"]}" value="{inp["default"]}"{min_attr}{max_attr}{step_attr}></div>'

    # Results display - same logic
    if "totalBudget" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">Remaining to Save</span><span class="result-value" id="resRemaining">-</span></div>'+
    '<div class="result-item"><span class="result-label">Monthly Savings Needed</span><span class="result-value" id="resMonthly">-</span></div>'+
    '<div class="result-item"><span class="result-label">Weekly Savings Needed</span><span class="result-value" id="resWeekly">-</span></div>'+
    '<div class="result-item"><span class="result-label">Daily Savings Needed</span><span class="result-value" id="resDaily">-</span></div>'+
    '<div class="result-item"><span class="result-label">Progress</span><span class="result-value" id="resProgress">-</span></div>';"""
        set_values = """
  el('resRemaining').textContent=fmtCur(remaining);
  el('resMonthly').textContent=fmtCur(monthly);
  el('resWeekly').textContent=fmtCur(weekly);
  el('resDaily').textContent=fmtCur(daily);
  el('resProgress').textContent=fmtPct(pctAchieved);"""
    elif "adoptionFee" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">Monthly Total</span><span class="result-value" id="resMonthly">-</span></div>'+
    '<div class="result-item"><span class="result-label">Annual Total</span><span class="result-value" id="resYearly">-</span></div>'+
    '<div class="result-item"><span class="result-label">Lifetime Total</span><span class="result-value" id="resLifetime">-</span></div>'+
    '<div class="result-item"><span class="result-label">One-Time Fee</span><span class="result-value" id="resOneTime">-</span></div>';"""
        set_values = """
  el('resMonthly').textContent=fmtCur(monthlyTotal);
  el('resYearly').textContent=fmtCur(yearlyTotal);
  el('resLifetime').textContent=fmtCur(lifetimeTotal);
  el('resOneTime').textContent=fmtCur(adoptionFee);"""
    elif "harvestValue" in t["calc_logic"]:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">Total Cost</span><span class="result-value" id="resTotalCost">-</span></div>'+
    '<div class="result-item"><span class="result-label">Expected Harvest Value</span><span class="result-value" id="resHarvest">-</span></div>'+
    '<div class="result-item"><span class="result-label">Net Return</span><span class="result-value" id="resNet">-</span></div>'+
    '<div class="result-item"><span class="result-label">ROI</span><span class="result-value" id="resROI">-</span></div>'+
    '<div class="result-item"><span class="result-label">Monthly Cost</span><span class="result-value" id="resMonthlyCost">-</span></div>';"""
        set_values = """
  el('resTotalCost').textContent=fmtCur(totalCost);
  el('resHarvest').textContent=fmtCur(harvestValue);
  el('resNet').textContent=fmtCur(netValue);
  el('resROI').textContent=fmtPct(roi);
  el('resMonthlyCost').textContent=fmtCur(monthlyCost);"""
    else:
        result_display = """
  el('resultContent').innerHTML=
    '<div class="result-item"><span class="result-label">Monthly Income (Gross)</span><span class="result-value" id="resMonthlyGross">-</span></div>'+
    '<div class="result-item"><span class="result-label">Annual Income (Gross)</span><span class="result-value" id="resYearlyGross">-</span></div>'+
    '<div class="result-item"><span class="result-label">Annual Net Income (After Tax)</span><span class="result-value highlight" id="resYearlyNet">-</span></div>'+
    '<div class="result-item"><span class="result-label">Effective Hourly Rate (After Tax)</span><span class="result-value" id="resEffectiveRate">-</span></div>'+
    '<div class="result-item"><span class="result-label">Annual Total Hours</span><span class="result-value" id="resTotalHours">-</span></div>';"""
        set_values = """
  el('resMonthlyGross').textContent=fmtCur(monthlyGross);
  el('resYearlyGross').textContent=fmtCur(yearlyGross);
  el('resYearlyNet').textContent=fmtCur(yearlyAfterTax);
  el('resEffectiveRate').textContent=fmtCur(yearlyAfterTax/(hoursPerWeek*weeksPerYear));
  el('resTotalHours').textContent=(hoursPerWeek*weeksPerYear)+' hours';"""

    related_tools = '[' + ','.join([
        '{"icon":"🧮","name":"Compound Interest Calculator","url":"compound-interest-calculator/"}',
        '{"icon":"💰","name":"Savings Goal Calculator","url":"savings-goal-calculator/"}',
        '{"icon":"📊","name":"Budget Planner","url":"budget-planner/"}',
        '{"icon":"📈","name":"ROI Calculator","url":"roi-calculator-simple/"}'
    ]) + ']'

    # FAQ EN
    if "totalBudget" in t["calc_logic"]:
        faq_en = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Why plan holiday savings in advance?","acceptedAnswer":{"@type":"Answer","text":"Holiday spending is concentrated at year-end (Christmas, New Year). Saving monthly in advance avoids the stress of a large one-time expense. This calculator helps spread the cost evenly across months."}},{"@type":"Question","name":"How far in advance should I start saving?","acceptedAnswer":{"@type":"Answer","text":"Start 6-12 months before the holiday. The earlier you start, the less you need to save each month. This tool helps you find the most comfortable saving pace."}},{"@type":"Question","name":"What should a holiday budget include?","acceptedAnswer":{"@type":"Answer","text":"A typical holiday budget includes: gifts, dining out, travel, decorations, new clothes, etc. List all expected expenses first, then use this calculator to determine monthly savings needed."}}]}</script>"""
        explain_en = """<div class="info-section"><h2>📖 How to Use</h2>
<p>This holiday savings calculator helps you plan and spread out holiday spending:</p>
<h3>Step 1: Set Total Budget</h3><p>Add up all expected holiday expenses (gifts, meals, travel, decorations, etc.).</p>
<h3>Step 2: Set Time Remaining</h3><p>Enter how many months until the holiday. The earlier you start, the less per month.</p>
<h3>Step 3: Enter Current Savings</h3><p>If you've already saved some money, enter the current balance to calculate the remaining gap.</p>
<h3>Step 4: View Your Plan</h3><p>The calculator shows how much to save monthly, weekly, and daily to reach your goal.</p></div>
<div class="info-section"><h2>💡 Saving Tips</h2><ul><li><strong>Auto-transfer:</strong> Set up monthly automatic transfers to a dedicated savings account.</li><li><strong>52-week challenge:</strong> Save $1 week 1, $2 week 2, etc. - you'll have $1,378 by year-end!</li><li><strong>Shop sales:</strong> Make a gift list early and buy during sales to save 30-50%.</li><li><strong>DIY gifts:</strong> Handmade gifts are more personal and cost less.</li></ul></div>"""
    elif "adoptionFee" in t["calc_logic"]:
        faq_en = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does a dog cost per year?","acceptedAnswer":{"@type":"Answer","text":"According to ASPCA, a medium-sized dog costs approximately $1,400-$4,300 annually (food $250-$700, vet care $500-$1,500, grooming $200-$500). Use this calculator to estimate based on your specific situation."}},{"@type":"Question","name":"Are cats cheaper than dogs?","acceptedAnswer":{"@type":"Answer","text":"Generally yes. Cats eat less, rarely need professional grooming, and annual costs run about $800-$2,000, 30-50% less than dogs. It depends on breed, health, and lifestyle."}},{"@type":"Question","name":"Is adopting cheaper than buying a pet?","acceptedAnswer":{"@type":"Answer","text":"Adoption typically costs $50-$200 (includes initial vaccines and spay/neuter), while buying a purebred can cost $500-$3,000+. Adoption saves money and gives a shelter animal a home."}}]}</script>"""
        explain_en = """<div class="info-section"><h2>📖 How to Use</h2>
<p>This pet cost calculator helps you estimate the full cost of pet ownership:</p>
<h3>Step 1: Select Pet Type</h3><p>Dogs, cats, rabbits, and hamsters have very different cost profiles.</p>
<h3>Step 2: Set Size and Lifespan</h3><p>Large dogs typically cost 50%+ more for food and vet care than small dogs.</p>
<h3>Step 3: Enter Cost Details</h3><p>Include food, vet care, grooming, other expenses (toys/treats/insurance) and one-time adoption/purchase fee.</p>
<h3>Step 4: View Total Costs</h3><p>See monthly, annual and lifetime totals to evaluate if you're financially ready for a pet.</p></div>
<div class="info-section"><h2>💡 Money-Saving Tips</h2><ul><li><strong>Adopt, don't shop:</strong> Shelter fees are much lower and include basic medical care.</li><li><strong>Buy food in bulk:</strong> Large bags of pet food cost less per pound and can save 20-30%.</li><li><strong>Pet insurance:</strong> $30-$50/month can prevent massive unexpected vet bills.</li><li><strong>DIY grooming:</strong> Learning basic grooming skills saves hundreds per year.</li></ul></div>"""
    elif "harvestValue" in t["calc_logic"]:
        faq_en = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much can I save by growing my own vegetables?","acceptedAnswer":{"@type":"Answer","text":"According to the National Gardening Association, a 200 sq ft garden can yield $500-$1,200 worth of produce annually. After costs, net savings are $300-$800. Tomatoes, lettuce, and beans offer the best ROI."}},{"@type":"Question","name":"What basic supplies do I need to start gardening?","acceptedAnswer":{"@type":"Answer","text":"Basic supplies include: trowel ($10), hoe ($15), watering can ($8), gloves ($5) - about $30-$80 for tools, plus $20-$50 for seeds and fertilizer. This calculator accounts for these one-time costs."}},{"@type":"Question","name":"Which vegetables are easiest and most profitable to grow?","acceptedAnswer":{"@type":"Answer","text":"Best for beginners: lettuce (30 days), cherry tomatoes (60 days), peppers (70 days), beans (50 days), cucumbers (60 days). These have few pest problems and high yields, perfect for new gardeners."}}]}</script>"""
        explain_en = """<div class="info-section"><h2>📖 How to Use</h2>
<p>This gardening cost calculator analyzes the ROI of growing your own food:</p>
<h3>Step 1: Enter Garden Size</h3><p>In square feet. Balcony gardens are typically 30-50 sq ft, yard gardens 100-300 sq ft.</p>
<h3>Step 2: Set Growing Season</h3><p>Typically 4-8 months for spring/summer. Adjust based on your climate.</p>
<h3>Step 3: Enter All Costs</h3><p>Seeds/seedlings, soil & fertilizer, tools (one-time), and monthly water cost increase.</p>
<h3>Step 4: Set Expected Harvest Value</h3><p>Estimate the retail value of vegetables/flowers you'll harvest this season.</p>
<h3>Step 5: View ROI Analysis</h3><p>See total cost, net return, and ROI percentage to decide if it's worth the investment.</p></div>
<div class="info-section"><h2>💡 High-ROI Vegetables</h2><ul><li><strong>Cherry Tomatoes:</strong> 3 plants yield 20-30 lbs, grocery price $3-5/lb, ROI can exceed 300%</li><li><strong>Salad Greens:</strong> Fast 30-day harvest, cut-and-come-again, virtually pest-free</li><li><strong>Herbs:</strong> Basil, mint, cilantro cost $3-5 per tiny pack at stores - grow for pennies</li><li><strong>Beans:</strong> High yield, easy maintenance, among the most productive per square foot</li></ul></div>"""
    else:
        faq_en = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need to pay taxes on side hustle income?","acceptedAnswer":{"@type":"Answer","text":"Yes, side hustle income is generally taxable. In the US, self-employment income is subject to 15.3% self-employment tax plus federal/state income tax. This calculator defaults to 20% tax rate but you can adjust it."}},{"@type":"Question","name":"Which side hustles pay the highest hourly rate?","acceptedAnswer":{"@type":"Answer","text":"Top-paying side hustles include: software development ($50-150/hr), design ($30-100/hr), translation ($20-60/hr), online tutoring ($15-50/hr). Use this calculator to compare annual earnings across different rates."}},{"@type":"Question","name":"How many hours per week should I dedicate to a side hustle?","acceptedAnswer":{"@type":"Answer","text":"5-15 hours per week is recommended to not interfere with your main job and rest. At $50/hr for 10 hours/week, annual income would be approximately $24,000. Find your optimal balance with this calculator."}}]}</script>"""
        explain_en = """<div class="info-section"><h2>📖 How to Use</h2>
<p>This side hustle calculator helps estimate your potential part-time income:</p>
<h3>Step 1: Enter Weekly Hours</h3><p>Realistically assess how many hours you can consistently dedicate. 5-15 hours is typical.</p>
<h3>Step 2: Set Expected Hourly Rate</h3><p>Based on your skills and market demand. Technical roles typically command $30-80/hr.</p>
<h3>Step 3: Enter Expenses and Tax Rate</h3><p>Account for platform fees, equipment, transportation, etc. Adjust tax rate based on your location and income level.</p>
<h3>Step 4: View Income Estimates</h3><p>See monthly, annual gross income, after-tax net income, and effective hourly rate after all deductions.</p></div>
<div class="info-section"><h2>💡 High-Paying Side Hustles</h2><ul><li><strong>Freelance Development:</strong> Upwork/Fiverr programming projects at $30-$150/hr</li><li><strong>Online Tutoring:</strong> English, math, coding subjects at $15-$50/hr</li><li><strong>Content Creation:</strong> Writing, video editing, graphic design at $20-$80/hr</li><li><strong>Local Services:</strong> Dog walking, tutoring, photography - set your own rates</li></ul></div>"""

    related_en_tools = '[' + ','.join([
        '{"icon":"🧮","name":"Compound Interest Calculator","url":"compound-interest-calculator/"}',
        '{"icon":"💰","name":"Savings Goal Calculator","url":"savings-goal-calculator/"}',
        '{"icon":"📊","name":"Budget Planner","url":"budget-planner/"}',
        '{"icon":"📈","name":"ROI Calculator","url":"roi-calculator-simple/"}'
    ]) + ']'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['desc_en']}">
<meta name="keywords" content="{t['keywords_en']}">
<title>Free Online {t['name_en']} | No Registration</title>
<link rel="canonical" href="https://free-toolbase.com/en/{t['slug']}/">
<meta property="og:title" content="Free Online {t['name_en']} | No Registration">
<meta property="og:description" content="{t['desc_en']}">
<meta property="og:url" content="https://free-toolbase.com/en/{t['slug']}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{t['slug']}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{t['slug']}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{t['slug']}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Online {t['name_en']}","description":"{t['desc_en']}","applicationCategory":"UtilityApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
{faq_en}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"How to Use {t['name_en']}","description":"Step-by-step guide for using the {t['name_en']}","totalTime":"PT3M","tool":{{"@type":"HowToTool","name":"{t['name_en']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"Enter Your Details","text":"Fill in the required parameters based on your situation"}},{{"@type":"HowToStep","position":2,"name":"Click Calculate","text":"Click the calculate button to see your results"}},{{"@type":"HowToStep","position":3,"name":"Review Results","text":"Review the detailed breakdown of your results"}},{{"@type":"HowToStep","position":4,"name":"Copy or Reset","text":"Copy results to clipboard or reset to try different scenarios"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['name_en']}","item":"https://free-toolbase.com/en/{t['slug']}/"}}]}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1c40f}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.form-group{{margin-bottom:12px}}
.form-group label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.result-section{{background:#0f172a;border-radius:8px;padding:16px;border:1px solid rgba(6,182,212,.3);margin-top:16px;display:none}}
.result-section .result-title{{font-size:1rem;color:#f1c40f;margin-bottom:8px}}
.result-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.08);flex-wrap:wrap}}
.result-item:last-child{{border-bottom:none}}
.result-label{{color:#94a3b8;font-size:.9rem}}
.result-value{{color:#22d3ee;font-size:.95rem;font-weight:600}}.result-value.highlight{{color:#f1c40f;font-size:1.1rem}}
.btn-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:500}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.35)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{list-style:none;padding-left:0}}
.info-section ul li{{color:#94a3b8;font-size:.9rem;margin-bottom:6px;padding-left:20px;position:relative}}
.info-section ul li::before{{content:"•";position:absolute;left:6px;color:#22d3ee}}
.related-tools{{margin-top:24px}}
.related-tools h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
.related-item{{background:#1e293b;border-radius:8px;padding:12px;border:1px solid rgba(148,163,184,.1);transition:all .2s}}
.related-item:hover{{border-color:rgba(6,182,212,.3)}}
.related-item a{{color:#e2e8f0;font-size:.9rem}}
.related-item a:hover{{color:#22d3ee}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto 20px;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}
@media(max-width:640px){{.header h1{{font-size:1.2rem}}.section{{padding:14px}}.related-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{ic} {t['name_en']}</h1><div class="lang-switch"><a href="../../{t['slug']}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {t['name_en']}</p>
<div class="hero"><p>{t['desc_en']} | No registration · Data never leaves your device</p><span class="badge">Zero dependencies · Works offline</span></div>

<div class="section">
<h2>🔢 Input Parameters</h2>
{inputs_html}
<div class="btn-row">
<button class="btn btn-primary" id="calcBtn">🧮 Calculate</button>
<button class="btn btn-secondary" id="clearBtn">🔄 Reset</button>
</div>
<div class="result-section" id="resultSection">
<div class="result-title">📊 Results</div>
<div id="resultContent"></div>
<div class="btn-row" style="margin-top:12px"><button class="btn btn-secondary" id="copyBtn">📋 Copy Results</button></div>
</div>
</div>

<div class="related-tools"><h2>🔗 Related Tools</h2><div class="related-grid" id="relatedGrid"></div></div>

{explain_en}

<div class="ad-slot">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>
</div>

<footer class="footer">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../privacy/">Privacy</a>
<a href="../terms/">Terms</a>
<a href="../about/">About</a>
<a href="../../{t['slug']}/">中文</a>
</div>
<p>{t['name_en']} | No registration · Data never leaves your device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
</div>

<div class="toast" id="toast"></div>

<script>
(function(){{
var el=function(id){{return document.getElementById(id);}};
var toastTimer=null;
function showToast(msg){{var t=el('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){{t.classList.remove('show');}},2500);}}
function fmtCur(n){{return '$'+n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}});}}
function fmtPct(n){{return n.toFixed(2)+'%';}}

function calculate(){{
{t['calc_logic']}
{result_display}
{set_values}
  el('resultSection').style.display='block';
}}

el('calcBtn').addEventListener('click',calculate);
el('clearBtn').addEventListener('click',function(){{location.reload();}});
el('copyBtn').addEventListener('click',function(){{
  var results=document.querySelectorAll('#resultContent .result-item');
  var text='{t['name_en']} - Results\\n';
  results.forEach(function(r){{text+=r.querySelector('.result-label').textContent+': '+r.querySelector('.result-value').textContent+'\\n';}});
  navigator.clipboard.writeText(text).then(function(){{showToast('Results copied to clipboard');}}).catch(function(){{showToast('Copy failed, please copy manually');}});
}});

var relatedTools={related_en_tools};
var rg=el('relatedGrid');
relatedTools.forEach(function(rt){{var d=document.createElement('div');d.className='related-item';d.innerHTML='<a href="../'+rt.url+'">'+rt.icon+' '+rt.name+'</a>';rg.appendChild(d);}});

calculate();
}})();
</script>
</body>
</html>'''
    return html


if __name__ == '__main__':
    for t in TOOLS:
        slug = t['slug']
        cn_dir = os.path.join(SITE, slug)
        en_dir = os.path.join(SITE, 'en', slug)
        os.makedirs(cn_dir, exist_ok=True)
        os.makedirs(en_dir, exist_ok=True)
        
        cn_path = os.path.join(cn_dir, 'index.html')
        en_path = os.path.join(en_dir, 'index.html')
        
        with open(cn_path, 'w', encoding='utf-8') as f:
            f.write(gen_cn(t))
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(gen_en(t))
        
        print(f"✅ Created {slug} (CN + EN)")
    print("Done!")
