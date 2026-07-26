#!/usr/bin/env python3
"""批量生成5个新工具页面：cpm-calculator, hydration-calculator, commission-calculator, paycheck-deduction, ctr-calculator"""
import os, sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

TOOLS = {
    "cpm-calculator": {
        "zh": {
            "title": "CPM计算器 - 广告千次展示成本计算 | Free ToolBase",
            "desc": "免费在线CPM计算器，输入广告总花费和展示次数，自动计算CPM（千次展示成本）。支持CPM反推预算、展示次数计算。数字营销和广告投放必备工具。纯前端本地运算，无需注册。",
            "h1": "📊 CPM广告成本计算器",
            "hero": "免费在线CPM计算器，输入广告花费和展示次数，自动计算千次展示成本。支持CPM反推预算和展示次数，数字营销必备。",
            "faq": [
                ("什么是CPM？", "CPM（Cost Per Mille）即千次展示成本，是数字广告中最常用的计价方式之一。它表示广告每展示1000次需要支付的费用。CPM = (广告总花费 / 展示次数) × 1000。"),
                ("如何计算CPM？", "CPM = (广告总花费 / 展示次数) × 1000。例如：花费500美元获得10万次展示，CPM = 500/100000 × 1000 = 5美元。即每千次展示花费5美元。"),
                ("CPM和CPC有什么区别？", "CPM按展示付费（每千次展示），CPC（Cost Per Click）按点击付费。CPM适合品牌曝光类广告，CPC适合效果类广告。CPM通常比CPC便宜，但点击率不可控。"),
                ("什么水平的CPM算好？", "CPM因行业、地区、受众定向而异。一般展示广告CPM在2-10美元正常，视频广告CPM在15-25美元。精准定向的受众CPM更高。"),
            ],
            "howto": ["输入广告花费", "输入展示次数", "点击计算", "查看CPM结果"],
            "labels": ["广告总花费", "展示次数"],
            "inputs": [{"id": "cost", "type": "number", "step": "0.01", "min": "0", "placeholder": "如 500", "default": "500"},
                      {"id": "impressions", "type": "number", "step": "1", "min": "1", "placeholder": "如 100000", "default": "100000"}],
            "results": [{"id": "rCPM", "label": "CPM（千次展示成本）", "highlight": True},
                       {"id": "rCPC_est", "label": "预估CPC（按0.1%点击率）", "highlight": False}],
            "calc_js": """function calc(){var c=parseFloat(document.getElementById('cost').value)||0;var imp=parseFloat(document.getElementById('impressions').value)||0;if(c<=0||imp<=0){clearResults();return}var cpm=c/imp*1000;document.getElementById('rCPM').textContent='$'+cpm.toFixed(2);document.getElementById('rCPC_est').textContent='$'+(cpm/1000).toFixed(4);}""",
        },
        "en": {
            "title": "CPM Calculator - Cost Per Mille Advertising Calculator | Free ToolBase",
            "desc": "Free online CPM calculator. Calculate cost per thousand impressions from ad spend and impressions. Also supports CPM-based budget and impression estimation. Essential tool for digital marketing and ad campaigns.",
            "h1": "📊 CPM Calculator",
            "hero": "Free online CPM calculator. Enter ad spend and impressions to calculate cost per thousand impressions. Supports CPM-based budget and impression estimation.",
            "faq": [
                ("What is CPM?", "CPM (Cost Per Mille) is the cost per thousand impressions, one of the most common pricing models in digital advertising. CPM = (Total Ad Spend / Impressions) × 1000."),
                ("How to calculate CPM?", "CPM = (Total Ad Spend / Impressions) × 1000. Example: $500 spent for 100,000 impressions → CPM = 500/100000 × 1000 = $5 per thousand impressions."),
                ("What's the difference between CPM and CPC?", "CPM charges per thousand impressions, CPC (Cost Per Click) charges per click. CPM is better for brand awareness campaigns, CPC for performance campaigns. CPM is usually cheaper but CTR is not guaranteed."),
                ("What is a good CPM?", "CPM varies by industry, region, and targeting. Display ads typically $2-10, video ads $15-25. Highly targeted audiences have higher CPM."),
            ],
            "labels": ["Ad Spend", "Impressions"],
        },
    },
    "hydration-calculator": {
        "zh": {
            "title": "每日饮水计算器 - 喝水量计算 | Free ToolBase",
            "desc": "免费在线每日饮水计算器，根据体重、运动量和气候计算每日推荐饮水量。支持毫升/盎司单位切换，科学喝水健康管理必备工具。纯前端本地运算，无需注册。",
            "h1": "💧 每日饮水计算器",
            "hero": "免费在线每日饮水计算器，根据体重、运动量和气温计算科学饮水量。支持毫升和盎司切换，健康生活好帮手。",
            "faq": [
                ("每天应该喝多少水？", "一般成年人每日推荐饮水量约为体重(kg) × 30-40毫升。例如：70kg的人每天需2100-2800ml水。运动量大或天气炎热时需增加500-1000ml。"),
                ("如何计算每日饮水量？", "基础饮水量 = 体重(kg) × 35ml。运动加成：轻度运动+500ml，中度运动+750ml，高强度运动+1000ml。高温环境额外+300-500ml。"),
                ("喝水过多会有问题吗？", "是的，过量饮水可能导致水中毒（低钠血症）。每小时肾脏最多处理约800-1000ml水。建议少量多次饮用，不要一次性大量灌水。"),
                ("茶、咖啡算饮水量吗？", "茶和咖啡可以计入总饮水量，但咖啡因有利尿作用，建议不超过每日总饮水量的50%。纯水仍是最好的补水来源。"),
            ],
            "howto": ["输入体重", "选择运动量", "选择气温条件", "查看推荐饮水量"],
            "labels": ["体重", "运动量", "气温条件"],
            "inputs": [{"id": "weight", "type": "number", "step": "0.1", "min": "30", "placeholder": "如 70", "default": "70"},
                      {"id": "activity", "type": "select", "options": [("sedentary","久坐不动"),("light","轻度运动"),("moderate","中度运动"),("heavy","高强度运动")]},
                      {"id": "climate", "type": "select", "options": [("normal","常温"),("hot","炎热")]}],
            "results": [{"id": "rWater", "label": "每日推荐饮水量", "highlight": True},
                       {"id": "rCups", "label": "约合杯数（250ml/杯）", "highlight": False}],
            "calc_js": """function calc(){var w=parseFloat(document.getElementById('weight').value)||70;var act=document.getElementById('activity').value;var cl=document.getElementById('climate').value;var base=w*35;if(act==='light')base+=500;else if(act==='moderate')base+=750;else if(act==='heavy')base+=1000;if(cl==='hot')base+=400;document.getElementById('rWater').textContent=Math.round(base)+' 毫升 (ml)';document.getElementById('rCups').textContent=(base/250).toFixed(1)+' 杯';}""",
        },
        "en": {
            "title": "Daily Water Intake Calculator - Hydration Calculator | Free ToolBase",
            "desc": "Free online daily water intake calculator. Calculate recommended daily water intake based on weight, activity level, and climate. Supports ml/oz unit switching. Essential health management tool.",
            "h1": "💧 Daily Water Intake Calculator",
            "hero": "Free online daily water intake calculator. Calculate science-based hydration needs based on weight, activity level, and temperature. Supports ml and oz switching.",
            "faq": [
                ("How much water should I drink daily?", "Adults should drink approximately 30-40ml per kg of body weight. Example: 70kg person needs 2100-2800ml daily. Add 500-1000ml for exercise or hot weather."),
                ("How to calculate daily water intake?", "Base intake = weight(kg) × 35ml. Activity bonus: light +500ml, moderate +750ml, intense +1000ml. Hot climate adds 300-500ml."),
                ("Can you drink too much water?", "Yes, excessive water intake can cause hyponatremia (water intoxication). Kidneys process 800-1000ml per hour max. Drink small amounts throughout the day."),
                ("Do tea and coffee count?", "Tea and coffee can count toward water intake, but caffeine is a diuretic. Limit to 50% of daily intake. Pure water remains the best hydration source."),
            ],
            "labels": ["Weight", "Activity Level", "Climate"],
        },
    },
    "commission-calculator": {
        "zh": {
            "title": "佣金计算器 - 销售佣金提成计算 | Free ToolBase",
            "desc": "免费在线佣金计算器，支持按比例提成和阶梯式提成两种模式。输入销售额和提成比例，自动计算佣金收入。支持固定底薪+提成计算，销售人员和自由职业者必备。",
            "h1": "💰 佣金提成计算器",
            "hero": "免费在线佣金计算器，支持固定比例和阶梯式提成两种模式。输入销售额自动计算佣金，支持底薪+提成综合计算。",
            "faq": [
                ("佣金怎么计算？", "佣金 = 销售额 × 提成比例。例如：销售额10万元，提成5%，佣金 = 100,000 × 5% = 5,000元。有些公司采用阶梯式提成，不同销售额区间适用不同比例。"),
                ("什么是阶梯式提成？", "阶梯式提成是根据销售额分段计算佣金。例如：0-5万提3%，5-10万提5%，10万以上提8%。销售额12万时佣金 = 5万×3% + 5万×5% + 2万×8%。"),
                ("底薪+提成怎么算总收入？", "总收入 = 固定底薪 + 佣金。例如：底薪5000元 + 佣金3000元 = 月收入8000元。注意佣金可能需要扣除个人所得税。"),
                ("佣金收入需要交税吗？", "在中国，佣金收入属于劳务报酬所得，需缴纳个人所得税。起征点为800元，超过部分按20%税率预扣。年度汇算时可合并综合所得计算。"),
            ],
            "howto": ["选择提成模式", "输入销售额", "输入提成比例", "查看佣金金额"],
            "labels": ["提成模式", "销售额", "提成比例(%)", "固定底薪（可选）"],
            "inputs": [{"id": "mode", "type": "select", "options": [("flat","固定比例"),("tiered","阶梯式")]},
                      {"id": "sales", "type": "number", "step": "0.01", "min": "0", "placeholder": "如 50000", "default": "50000"},
                      {"id": "rate", "type": "number", "step": "0.1", "min": "0", "placeholder": "如 5", "default": "5"},
                      {"id": "base", "type": "number", "step": "0.01", "min": "0", "placeholder": "如 5000（可选）", "default": "0"}],
            "results": [{"id": "rCommission", "label": "佣金金额", "highlight": True},
                       {"id": "rTotal", "label": "总收入（底薪+佣金）", "highlight": False}],
            "calc_js": """function calc(){var mode=document.getElementById('mode').value;var sales=parseFloat(document.getElementById('sales').value)||0;var rate=parseFloat(document.getElementById('rate').value)||0;var base=parseFloat(document.getElementById('base').value)||0;var comm=0;if(mode==='flat'){comm=sales*rate/100;}else{var tiers=[{limit:50000,rate:rate*0.6},{limit:100000,rate:rate},{limit:Infinity,rate:rate*1.6}];var remaining=sales;for(var i=0;i<tiers.length&&remaining>0;i++){var tierAmt=Math.min(remaining,i===0?tiers[i].limit:(tiers[i].limit-tiers[i-1].limit));comm+=tierAmt*tiers[i].rate/100;remaining-=tierAmt;}}document.getElementById('rCommission').textContent='¥'+comm.toFixed(2);document.getElementById('rTotal').textContent='¥'+(comm+base).toFixed(2);}""",
        },
        "en": {
            "title": "Commission Calculator - Sales Commission & Tiered Commission | Free ToolBase",
            "desc": "Free online commission calculator. Supports flat-rate and tiered commission models. Enter sales amount and commission rate to calculate commission income. Supports base salary + commission calculation.",
            "h1": "💰 Commission Calculator",
            "hero": "Free online commission calculator. Supports flat-rate and tiered commission models. Enter sales amount to auto-calculate commission with base salary support.",
            "faq": [
                ("How to calculate commission?", "Commission = Sales × Commission Rate. Example: $100,000 sales at 5% = $5,000 commission. Some companies use tiered rates where different sales ranges have different rates."),
                ("What is tiered commission?", "Tiered commission calculates commission by sales brackets. Example: 0-50k at 3%, 50-100k at 5%, 100k+ at 8%. On $120k sales: 50k×3% + 50k×5% + 20k×8%."),
                ("How to calculate base + commission?", "Total Income = Base Salary + Commission. Example: $5,000 base + $3,000 commission = $8,000 monthly. Note: commission may be subject to income tax."),
                ("Is commission income taxable?", "Yes, commission income is taxable in most countries. In the US, commission is treated as ordinary income. Consult a tax professional for your specific situation."),
            ],
            "labels": ["Commission Mode", "Sales Amount", "Commission Rate (%)", "Base Salary (optional)"],
        },
    },
    "paycheck-deduction": {
        "zh": {
            "title": "工资扣除计算器 - 税后实发工资计算 | Free ToolBase",
            "desc": "免费在线工资扣除计算器，计算五险一金和个人所得税扣除后的实发工资。支持中国大陆社保公积金比例自定义，打工人必备薪资计算工具。纯前端本地运算。",
            "h1": "💳 工资扣除计算器",
            "hero": "免费在线工资扣除计算器，输入税前月薪自动计算五险一金和个税扣除，快速得出实发到手工资。",
            "faq": [
                ("五险一金包括哪些？", "五险：养老保险（个人8%）、医疗保险（个人2%）、失业保险（个人0.5%）、工伤保险（个人0%）、生育保险（个人0%）。一金：住房公积金（个人5%-12%）。各地比例略有差异。"),
                ("个人所得税怎么算？", "应纳税所得额 = 税前工资 - 五险一金 - 5000元（起征点）。税率从3%到45%分7级累进。例如：月薪2万，五险一金约4000，应纳税所得额11000，个税约390元。"),
                ("什么是社保缴费基数？", "社保缴费基数有上下限：一般为当地平均工资的60%-300%。工资低于下限按下限缴，高于上限按上限缴。本计算器使用简化比例计算。"),
                ("税后实发工资怎么算？", "实发工资 = 税前工资 - 五险一金 - 个人所得税。例如：税前20000，五险一金4000，个税390，实发 = 20000-4000-390 = 15610元。"),
            ],
            "howto": ["输入税前月薪", "调整五险一金比例", "点击计算", "查看实发工资"],
            "labels": ["税前月薪", "公积金比例(%)", "社保比例(%)"],
            "inputs": [{"id": "salary", "type": "number", "step": "0.01", "min": "0", "placeholder": "如 20000", "default": "20000"},
                      {"id": "housing", "type": "number", "step": "1", "min": "5", "max": "12", "placeholder": "5-12", "default": "7"},
                      {"id": "social", "type": "number", "step": "0.1", "min": "0", "placeholder": "默认10.5%", "default": "10.5"}],
            "results": [{"id": "rInsurance", "label": "五险一金扣除", "highlight": False},
                       {"id": "rTax", "label": "个人所得税", "highlight": False},
                       {"id": "rNet", "label": "实发到手工资", "highlight": True}],
            "calc_js": """function calc(){var s=parseFloat(document.getElementById('salary').value)||0;var h=parseFloat(document.getElementById('housing').value)||7;var ss=parseFloat(document.getElementById('social').value)||10.5;var insurance=s*(h+ss)/100;var taxable=Math.max(0,s-insurance-5000);var tax=0;var brackets=[[36000,0.03],[144000,0.1],[300000,0.2],[420000,0.25],[660000,0.3],[960000,0.35],[Infinity,0.45]];var remaining=taxable;var prev=0;for(var i=0;i<brackets.length&&remaining>0;i++){var bracket=Math.min(remaining,brackets[i][0]-prev);tax+=bracket*brackets[i][1];remaining-=bracket;prev=brackets[i][0];}document.getElementById('rInsurance').textContent='¥'+insurance.toFixed(2);document.getElementById('rTax').textContent='¥'+tax.toFixed(2);document.getElementById('rNet').textContent='¥'+(s-insurance-tax).toFixed(2);}""",
        },
        "en": {
            "title": "Paycheck Deduction Calculator - Net Pay After Tax | Free ToolBase",
            "desc": "Free online paycheck deduction calculator. Calculate take-home pay after social insurance, housing fund, and income tax deductions. Customizable deduction rates for accurate net pay estimation.",
            "h1": "💳 Paycheck Deduction Calculator",
            "hero": "Free online paycheck deduction calculator. Enter gross monthly salary to auto-calculate social insurance, housing fund, and tax deductions for net take-home pay.",
            "faq": [
                ("What are common paycheck deductions?", "Common deductions include: social security tax (6.2% in US), Medicare tax (1.45%), federal/state income tax, health insurance premiums, and 401(k) contributions. Rates vary by country."),
                ("How is income tax calculated?", "Taxable income = Gross pay - Pre-tax deductions. Tax rates are progressive: higher income = higher rate. US federal rates range from 10% to 37% across 7 brackets."),
                ("What is social security tax?", "Social security tax funds retirement and disability benefits. In the US, employees pay 6.2% on wages up to the annual cap. Employers match this amount."),
                ("How to calculate net pay?", "Net Pay = Gross Pay - All Deductions. Example: $5,000 gross, $310 social security, $72.50 Medicare, $500 federal tax = $4,117.50 net pay."),
            ],
            "labels": ["Gross Monthly Salary", "Retirement/401(k) (%)", "Other Deductions (%)"],
        },
    },
    "ctr-calculator": {
        "zh": {
            "title": "CTR计算器 - 广告点击率计算 | Free ToolBase",
            "desc": "免费在线CTR（点击率）计算器，输入点击次数和展示次数，自动计算广告点击率。支持CPC反推、转化率联动计算。数字营销和广告投放必备工具。纯前端本地运算。",
            "h1": "🎯 CTR点击率计算器",
            "hero": "免费在线CTR计算器，输入点击次数和展示次数，自动计算广告点击率。支持CPC和转化率联动计算，数字营销必备。",
            "faq": [
                ("什么是CTR？", "CTR（Click-Through Rate）即点击率，是广告点击次数除以展示次数的百分比。CTR = (点击次数 / 展示次数) × 100%。它衡量广告吸引力的核心指标。"),
                ("什么样的CTR算好？", "CTR因行业和广告类型差异很大。搜索广告平均CTR约2-3%，展示广告约0.1-0.5%，社交媒体广告约0.5-1.5%。高于行业平均50%即可视为优秀。"),
                ("CTR和CPC有什么关系？", "CPC = CPM / (CTR × 10)。例如：CPM为10美元，CTR为0.5%，则CPC = 10/(0.5×10) = 2美元。提高CTR可以降低CPC，提升广告效率。"),
                ("如何提高CTR？", "提高CTR的方法：优化广告文案（使用数字、紧迫感）、精准受众定向、A/B测试不同创意、使用高质量图片/视频、优化号召性用语（CTA）。"),
            ],
            "howto": ["输入点击次数", "输入展示次数", "点击计算", "查看CTR结果"],
            "labels": ["点击次数", "展示次数", "CPM（可选，用于反推CPC）"],
            "inputs": [{"id": "clicks", "type": "number", "step": "1", "min": "0", "placeholder": "如 150", "default": "150"},
                      {"id": "impressions", "type": "number", "step": "1", "min": "1", "placeholder": "如 50000", "default": "50000"},
                      {"id": "cpm", "type": "number", "step": "0.01", "min": "0", "placeholder": "如 10（可选）", "default": "0"}],
            "results": [{"id": "rCTR", "label": "CTR（点击率）", "highlight": True},
                       {"id": "rCPC", "label": "CPC（每次点击成本）", "highlight": False}],
            "calc_js": """function calc(){var cl=parseFloat(document.getElementById('clicks').value)||0;var imp=parseFloat(document.getElementById('impressions').value)||0;var cpm=parseFloat(document.getElementById('cpm').value)||0;if(cl<0||imp<=0){clearResults();return}var ctr=cl/imp*100;document.getElementById('rCTR').textContent=ctr.toFixed(4)+'%';if(cpm>0){document.getElementById('rCPC').textContent='$'+(cpm/(ctr*10)).toFixed(2);}else{document.getElementById('rCPC').textContent='输入CPM后计算';}}""",
        },
        "en": {
            "title": "CTR Calculator - Click-Through Rate Calculator | Free ToolBase",
            "desc": "Free online CTR (Click-Through Rate) calculator. Enter clicks and impressions to calculate click-through rate. Supports CPC estimation from CPM. Essential digital marketing tool.",
            "h1": "🎯 CTR Calculator",
            "hero": "Free online CTR calculator. Enter clicks and impressions to calculate click-through rate. Supports CPC estimation from CPM for digital marketing campaigns.",
            "faq": [
                ("What is CTR?", "CTR (Click-Through Rate) is the percentage of impressions that result in clicks. CTR = (Clicks / Impressions) × 100%. It measures ad engagement and relevance."),
                ("What is a good CTR?", "CTR varies by industry and ad type. Search ads average 2-3%, display ads 0.1-0.5%, social media 0.5-1.5%. 50% above industry average is considered excellent."),
                ("What's the relationship between CTR and CPC?", "CPC = CPM / (CTR × 10). Example: $10 CPM with 0.5% CTR = $2 CPC. Higher CTR lowers CPC and improves ad efficiency."),
                ("How to improve CTR?", "Improve CTR by: optimizing ad copy (use numbers, urgency), precise audience targeting, A/B testing creatives, using high-quality images/video, and optimizing CTAs."),
            ],
            "labels": ["Clicks", "Impressions", "CPM (optional for CPC)"],
        },
    },
}

SHARED_CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:900px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.nav-back a:hover{color:#94a3b8}
.hero{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.hero p{color:#94a3b8;font-size:.9rem}
.badge{display:inline-block;margin-top:8px;padding:2px 10px;border-radius:4px;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.75rem}
.input-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.input-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.input-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:flex-end}
.input-group{flex:1;min-width:140px}
.input-group label{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}
.input-group input,.input-group select{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem}
.input-group input:focus,.input-group select:focus{outline:none;border-color:rgba(6,182,212,.5)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.result-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}
.result-section.show{display:block}
.result-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:16px}
.result-card{background:#0f172a;border-radius:8px;padding:16px;text-align:center}
.result-card .label{font-size:.75rem;color:#64748b;margin-bottom:4px}
.result-card .value{font-size:1.3rem;color:#f1f5f9;font-weight:600}
.result-card .unit{font-size:.75rem;color:#64748b;margin-top:2px}
.result-card.highlight .value{color:#22d3ee}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section h3{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}
.info-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.info-section ul{margin-left:20px;color:#94a3b8;font-size:.9rem}
.info-section li{margin-bottom:6px}
.faq-item{margin-bottom:16px}
.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}
.faq-item p{color:#94a3b8;font-size:.9rem;line-height:1.7}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}
.copy-btn{display:inline-flex;align-items:center;gap:4px;padding:6px 12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.25);border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s;margin-left:8px;vertical-align:top}
.copy-btn:hover{background:rgba(6,182,212,.25)}
.copy-btn.copied{background:rgba(34,197,94,.15);color:#22c55e;border-color:rgba(34,197,94,.3)}
@media(max-width:600px){.input-row{flex-direction:column;gap:8px}.input-group{min-width:100%}.result-grid{grid-template-columns:1fr}}
@media(max-width:640px){h1{font-size:1.2rem;word-break:break-word}.header{flex-direction:column;gap:8px}}'''

SHARED_META = '''<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'''

SHARED_JS = '''function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function clearResults(){var cards=document.querySelectorAll('.result-card .value');for(var i=0;i<cards.length;i++){cards[i].textContent='--';}}

(function(){
  var processed=new Set();
  function addCopyBtns(){
    var results=document.querySelectorAll('.result-section,.result-grid');
    results.forEach(function(el){
      if(processed.has(el)) return;
      if(el.querySelector('.copy-btn')) return;
      var btn=document.createElement('button');
      btn.className='copy-btn';
      btn.innerHTML='📋 复制';
      btn.title='复制结果';
      btn.onclick=function(e){
        e.stopPropagation();
        var text='';
        var cards=el.querySelectorAll('.result-card');
        for(var i=0;i<cards.length;i++){
          var label=cards[i].querySelector('.label');
          var value=cards[i].querySelector('.value');
          if(label&&value) text+=label.textContent+': '+value.textContent+'\\n';
        }
        navigator.clipboard.writeText(text.trim()).then(function(){
          btn.innerHTML='✅ 已复制';btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='📋 复制';btn.classList.remove('copied');},2000);
        }).catch(function(){
          var ta=document.createElement('textarea');ta.value=text.trim();ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);
          btn.innerHTML='✅ 已复制';btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='📋 复制';btn.classList.remove('copied');},2000);
        });
      };
      el.appendChild(btn);
      processed.add(el);
    });
  }
  addCopyBtns();
  document.addEventListener('click',function(){setTimeout(addCopyBtns,100);});
  if(window.MutationObserver){var obs=new MutationObserver(function(){addCopyBtns();});obs.observe(document.body,{childList:true,subtree:true});}
})();'''

def make_faq_html(faq_items):
    html = ''
    for q, a in faq_items:
        html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>\n'
    return html

def make_howto_html(steps):
    items = ''.join(f'<li style="margin-bottom:16px"><strong>{s}</strong><br><span style="color:#94a3b8;font-size:.9rem">完成此步骤</span></li>\n' for s in steps)
    return f'<h2>使用教程</h2><ol style="padding-left:20px;margin-top:12px">{items}</ol>'

def make_inputs_html(inputs):
    html = ''
    for inp in inputs:
        if inp['type'] == 'select':
            opts = ''.join(f'<option value="{v}">{l}</option>' for v, l in inp['options'])
            html += f'<div class="input-group"><label>{inp["label"]}</label><select id="{inp["id"]}" onchange="calc()">{opts}</select></div>\n'
        else:
            attrs = f'type="{inp["type"]}" step="{inp.get("step","any")}" min="{inp.get("min","0")}"'
            if inp.get('max'): attrs += f' max="{inp["max"]}"'
            html += f'<div class="input-group"><label>{inp["label"]}</label><input id="{inp["id"]}" {attrs} placeholder="{inp["placeholder"]}" value="{inp["default"]}" oninput="calc()"></div>\n'
    return html

def make_results_html(results):
    html = ''
    for r in results:
        cls = 'result-card highlight' if r.get('highlight') else 'result-card'
        html += f'<div class="{cls}"><div class="label">{r["label"]}</div><div class="value" id="{r["id"]}">--</div></div>\n'
    return html

def generate(lang, tool_id, data):
    is_cn = (lang == 'zh')
    lang_code = 'zh-CN' if is_cn else 'en'
    dir_prefix = '' if is_cn else '../'
    en_prefix = '' if is_cn else 'en/'
    cn_url = f'https://free-toolbase.com/{tool_id}/'
    en_url = f'https://free-toolbase.com/en/{tool_id}/'
    canonical = cn_url if is_cn else en_url
    alt_zh = cn_url
    alt_en = en_url
    xdefault = en_url

    title = data['title']
    desc = data['desc']
    h1 = data['h1']
    hero = data['hero']
    labels = data.get('labels', [])
    inputs = data.get('inputs', [])
    results = data.get('results', [])
    calc_js = data.get('calc_js', '')
    faq = data.get('faq', [])
    howto = data.get('howto', ['输入数据', '点击计算', '查看结果'])
    # Auto-add label from labels list if missing
    for i, inp in enumerate(inputs):
        if 'label' not in inp and i < len(labels):
            inp['label'] = labels[i]

    schema_name = h1.split(' ', 1)[1] if ' ' in h1 else h1
    schema_name_en = h1

    inputs_html = make_inputs_html(inputs)
    results_html = make_results_html(results)
    faq_html = make_faq_html(faq)
    howto_html = make_howto_html(howto)

    # Breadcrumb name
    bc_name = h1.split(' ', 1)[1] if ' ' in h1 else h1

    # 构建Schema FAQ
    faq_schema_items = []
    for q, a in faq:
        faq_schema_items.append(f'{{"@type": "Question", "name": "{q}", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}}}')

    faq_json = ','.join(faq_schema_items)
    howto_steps = ','.join(f'{{"@type": "HowToStep", "position": {i+1}, "name": "{s}", "text": "完成{s}步骤"}}' for i, s in enumerate(howto))

    if is_cn:
        lang_switch = f'<a href="index.html" class="active">中文</a><a href="../en/{tool_id}/" class="">EN</a>'
    else:
        lang_switch = f'<a href="../../{tool_id}/" class="">中文</a><a href="index.html" class="active">EN</a>'

    content = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{','.join(labels)},在线工具,免费">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="{alt_zh}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{xdefault}">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{schema_name}", "description": "{desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_json}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{h1}", "description": "如何使用{h1}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{h1}"}}, "step": [{howto_steps}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "首页", "item": "https://free-toolbase.com/"}}, {{"@type": "ListItem", "position": 2, "name": "工具", "item": "https://free-toolbase.com/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{bc_name}", "item": "{canonical}"}}]}}</script>
{SHARED_META}
<style>
{SHARED_CSS}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{h1}</h1><div class="lang-switch">{lang_switch}</div></div>
<p class="nav-back"><a href="{dir_prefix}index.html">首页</a> &rsaquo; <a href="{dir_prefix}index.html#tools">工具</a> &rsaquo; {bc_name}</p>
<div class="hero"><p>{hero}</p><span class="badge">零依赖·可离线使用</span></div>

<div class="input-section" id="input">
  <h2>{'计算输入' if is_cn else 'Calculator Input'}</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{'输入以下数值，自动实时计算' if is_cn else 'Enter values below for real-time calculation'}</p>
  <div class="input-row">
    {inputs_html}
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="clearResults();document.querySelectorAll('input').forEach(function(el){{el.value=el.defaultValue;}});calc()">{'🔄 重置' if is_cn else '🔄 Reset'}</button>
  </div>
</div>

<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{'计算结果' if is_cn else 'Results'}</h2>
  <div class="result-grid" id="resultGrid">
    {results_html}
  </div>
</div>

<div class="info-section">
  {howto_html}
</div>

<div class="info-section">
  <h2>{'常见问题 FAQ' if is_cn else 'Frequently Asked Questions'}</h2>
  {faq_html}
</div>
</div>

<div>
<!-- AdSense -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="{dir_prefix}index.html">{'首页' if is_cn else 'Home'}</a>
<a href="{dir_prefix}index.html">{'全部工具' if is_cn else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if is_cn else 'Contact'}</a>
<a href="{dir_prefix}privacy/">{'隐私政策' if is_cn else 'Privacy'}</a>
<a href="{dir_prefix}terms/">{'服务条款' if is_cn else 'Terms'}</a>
<a href="{dir_prefix}about/">{'关于我们' if is_cn else 'About'}</a>
<a href="{en_prefix}{tool_id}/">EN</a>
</footer>
<p>{bc_name} | {'无需注册 · 数据绝不上传服务器' if is_cn else 'No Registration · Data Never Leaves Your Device'}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{'问题反馈' if is_cn else 'Feedback'}: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
{SHARED_JS}
{calc_js}
calc();
</script>
</body>
</html>'''
    return content


import os

for tool_id, data in TOOLS.items():
    # CN version
    cn_dir = os.path.join(BASE, tool_id)
    os.makedirs(cn_dir, exist_ok=True)
    cn_path = os.path.join(cn_dir, 'index.html')
    cn_html = generate('zh', tool_id, data['zh'])
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f'✅ Created {cn_path}')

    # EN version
    en_dir = os.path.join(BASE, 'en', tool_id)
    os.makedirs(en_dir, exist_ok=True)
    en_path = os.path.join(en_dir, 'index.html')
    en_data = data['en'].copy()
    # Merge shared fields from zh that en doesn't have
    for k in ['inputs', 'results', 'calc_js', 'howto']:
        if k not in en_data:
            en_data[k] = data['zh'][k]
    if 'faq' not in en_data:
        en_data['faq'] = data['zh']['faq']
    if 'labels' not in en_data:
        en_data['labels'] = data['zh']['labels']
    en_html = generate('en', tool_id, en_data)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✅ Created {en_path}')

print('\n🎉 All 5 tools generated!')