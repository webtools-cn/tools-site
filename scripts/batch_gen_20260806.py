#!/usr/bin/env python3
"""批量生成8个工具"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_tool import gen_tool

TOOLS = [
    {
        "slug": "pressure-calculator",
        "cn_name": "压力换算器",
        "en_name": "Pressure Converter",
        "cn_desc": "在线压力单位换算器，支持帕斯卡(Pa)、千帕(kPa)、巴(bar)、大气压(atm)、毫米汞柱(mmHg)、磅力/平方英寸(psi)等常用压力单位互转。",
        "en_desc": "Free online pressure unit converter. Convert between Pa, kPa, bar, atm, mmHg, psi and more common pressure units instantly.",
        "inputs_cn": [
            ("数值", "输入压力值"),
            ("从单位", "选择原始单位", "select:帕斯卡(Pa),千帕(kPa),巴(bar),大气压(atm),毫米汞柱(mmHg),磅/平方英寸(psi),兆帕(MPa)"),
            ("到单位", "选择目标单位", "select:帕斯卡(Pa),千帕(kPa),巴(bar),大气压(atm),毫米汞柱(mmHg),磅/平方英寸(psi),兆帕(MPa)"),
        ],
        "inputs_en": [
            ("Value", "Enter pressure value"),
            ("From Unit", "Select source unit", "select:Pascal(Pa),Kilopascal(kPa),Bar(bar),Atmosphere(atm),mmHg(mmHg),PSI(psi),Megapascal(MPa)"),
            ("To Unit", "Select target unit", "select:Pascal(Pa),Kilopascal(kPa),Bar(bar),Atmosphere(atm),mmHg(mmHg),PSI(psi),Megapascal(MPa)"),
        ],
        "calc_js": """var pa=1,kpa=.001,bar=1e-5,atm=9.8692e-6,mmhg=.0075006,psi=.00014504,mpa=1e-6;
var factors={Pa:[1,.001,1e-5,9.8692e-6,.0075006,.00014504,1e-6],kPa:[1000,1,.01,.0098692,7.5006,.14504,.001],bar:[100000,100,1,.98692,750.06,14.504,.1],atm:[101325,101.325,1.01325,1,760,14.696,.101325],mmHg:[133.322,.133322,.00133322,.00131579,1,.0193368,.000133322],PSI:[6894.76,6.89476,.0689476,.068046,51.7149,1,.00689476],MPa:[1000000,1000,10,9.8692,7500.62,145.038,1]};
var keys=['Pa','kPa','bar','atm','mmHg','PSI','MPa'];
var fromKey=keys[document.getElementById('v2').selectedIndex];
var toIdx=document.getElementById('v3').selectedIndex;
var ff=factors[fromKey];if(!ff)ff=factors.Pa;
var result=a*ff[toIdx];
document.getElementById('rv').textContent=result.toFixed(6);
document.getElementById('rd').textContent=a+' '+fromKey+' = '+result.toFixed(6)+' '+keys[toIdx];
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "energy-calculator",
        "cn_name": "能量换算器",
        "en_name": "Energy Converter",
        "cn_desc": "在线能量单位换算器，支持焦耳(J)、千焦(kJ)、卡路里(cal)、千卡(kcal)、瓦时(Wh)、千瓦时(kWh)、电子伏特(eV)等常用能量单位互转。",
        "en_desc": "Free online energy unit converter. Convert between Joule, kJ, calorie, kcal, watt-hour, kWh, electron-volt and more energy units instantly.",
        "inputs_cn": [
            ("数值", "输入能量值"),
            ("从单位", "选择原始单位", "select:焦耳(J),千焦(kJ),卡路里(cal),千卡(kcal),瓦时(Wh),千瓦时(kWh),电子伏特(eV)"),
            ("到单位", "选择目标单位", "select:焦耳(J),千焦(kJ),卡路里(cal),千卡(kcal),瓦时(Wh),千瓦时(kWh),电子伏特(eV)"),
        ],
        "inputs_en": [
            ("Value", "Enter energy value"),
            ("From Unit", "Select source unit", "select:Joule(J),Kilojoule(kJ),Calorie(cal),Kilocalorie(kcal),Watt-hour(Wh),Kilowatt-hour(kWh),Electron-volt(eV)"),
            ("To Unit", "Select target unit", "select:Joule(J),Kilojoule(kJ),Calorie(cal),Kilocalorie(kcal),Watt-hour(Wh),Kilowatt-hour(kWh),Electron-volt(eV)"),
        ],
        "calc_js": """var keys=['J','kJ','cal','kcal','Wh','kWh','eV'];
var fromKey=keys[document.getElementById('v2').selectedIndex];
var toKey=keys[document.getElementById('v3').selectedIndex];
var toJ={J:1,kJ:1000,cal:4.184,kcal:4184,Wh:3600,kWh:3600000,eV:1.602176634e-19};
var fromJ={J:1,kJ:.001,cal:.239005736,kcal:.000239005736,Wh:.0002777778,kWh:2.777778e-7,eV:6.241509e18};
var joules=a*toJ[fromKey];
var result=joules*fromJ[toKey];
document.getElementById('rv').textContent=result<.0001?result.toExponential(4):result.toFixed(6);
document.getElementById('rd').textContent=a+' '+fromKey+' = '+result.toFixed(6)+' '+toKey;
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "caffeine-intake-calculator",
        "cn_name": "咖啡因摄入计算器",
        "en_name": "Caffeine Intake Calculator",
        "cn_desc": "在线咖啡因摄入计算器，根据饮品类型和杯数计算每日咖啡因摄入总量，对比安全上限(400mg/天)，帮助管理咖啡因摄入。",
        "en_desc": "Free caffeine intake calculator. Calculate your daily caffeine total based on drink type and cups, compare against 400mg daily safety limit for healthy adults.",
        "inputs_cn": [
            ("饮品类型", "选择饮品类型", "select:浓缩咖啡(63mg),美式咖啡(95mg),拿铁(75mg),速溶咖啡(63mg),绿茶(28mg),红茶(47mg),可乐(34mg),能量饮料(80mg),红牛(80mg),抹茶(70mg),乌龙茶(37mg),热可可(5mg)"),
            ("杯数", "杯数"),
            ("体重(kg)", "体重(可选)"),
        ],
        "inputs_en": [
            ("Drink Type", "Select drink type", "select:Espresso(63mg),Brewed Coffee(95mg),Latte(75mg),Instant Coffee(63mg),Green Tea(28mg),Black Tea(47mg),Cola(34mg),Energy Drink(80mg),Red Bull(80mg),Matcha(70mg),Oolong Tea(37mg),Hot Chocolate(5mg)"),
            ("Cups", "Number of cups"),
            ("Body Weight(kg)", "Weight (optional)"),
        ],
        "calc_js": """var mgMap={espresso:63,brewed:95,latte:75,instant:63,greentea:28,blacktea:47,cola:34,energydrink:80,redbull:80,matcha:70,oolong:37,hotchocolate:5};
var v2el=document.getElementById('v1');
var opts=v2el.options[v2el.selectedIndex].text.toLowerCase().replace(/[^a-z]/g,'');
var total=a*b;
var limit=400;
var safe=total<=limit?'Safe (<=400mg/day)':'Exceeds daily limit (400mg)';
var pct=((total/limit)*100).toFixed(0);
var perKg=c>0?(total/c).toFixed(2):null;
document.getElementById('rv').textContent=total.toFixed(0)+' mg';
var detail=safe+' | '+pct+'% of limit';
if(perKg)detail+=' | '+perKg+' mg/kg';
document.getElementById('rd').textContent=detail;
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "fuel-efficiency-calculator",
        "cn_name": "油耗计算器",
        "en_name": "Fuel Efficiency Calculator",
        "cn_desc": "在线油耗计算器，计算百公里油耗(L/100km)、每公里油费、每升行驶里程。支持公里和英里单位切换。",
        "en_desc": "Free fuel efficiency calculator. Calculate L/100km, cost per km, km per liter. Supports metric and imperial units for cars, trucks and motorcycles.",
        "inputs_cn": [
            ("行驶里程(km)", "输入行驶里程"),
            ("消耗燃油(L)", "输入消耗燃油量"),
            ("油价(元/L)", "输入单价(可选)"),
        ],
        "inputs_en": [
            ("Distance(km)", "Enter distance traveled"),
            ("Fuel Used(L)", "Enter fuel consumed"),
            ("Fuel Price(per L)", "Enter price (optional)"),
        ],
        "calc_js": """if(a<=0||b<=0){show('Please enter valid numbers');return}
var per100km=((b/a)*100).toFixed(2);
var kmPerL=(a/b).toFixed(2);
var costPerKm=c>0?((c*b)/a).toFixed(2):null;
document.getElementById('rv').textContent=per100km+' L/100km';
var detail=kmPerL+' km/L | '+per100km+' L per 100km';
if(costPerKm)detail+=' | '+costPerKm+' per km';
document.getElementById('rd').textContent=detail;
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "percent-error-calculator",
        "cn_name": "百分比误差计算器",
        "en_name": "Percent Error Calculator",
        "cn_desc": "在线百分比误差计算器，计算实验值与理论值的百分比误差。常用于科学实验、质量控制和数据分析场景。",
        "en_desc": "Free percent error calculator. Calculate the percent error between experimental and theoretical values. Ideal for science labs, QC, and data analysis.",
        "inputs_cn": [
            ("实验值", "输入实验测量值"),
            ("理论值", "输入理论/参考值"),
        ],
        "inputs_en": [
            ("Experimental Value", "Enter experimental value"),
            ("Theoretical Value", "Enter theoretical value"),
        ],
        "calc_js": """if(b===0){show('Theoretical value cannot be zero');return}
var err=Math.abs((a-b)/b)*100;
document.getElementById('rv').textContent=err.toFixed(4)+'%';
document.getElementById('rd').textContent='Experimental: '+a+' | Theoretical: '+b+' | Abs error: '+Math.abs(a-b).toFixed(4);
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "recurring-cost-calculator",
        "cn_name": "订阅费用计算器",
        "en_name": "Recurring Cost Calculator",
        "cn_desc": "在线订阅费用计算器，计算各类订阅服务的月度、年度总支出，清晰展示Netflix、Spotify等所有订阅的合计费用。",
        "en_desc": "Free recurring cost calculator. Sum up monthly, quarterly, and yearly subscription costs in one view. See your total annual spending at a glance.",
        "inputs_cn": [
            ("月订阅额(元/月)", "月付总额"),
            ("季订阅额(元/季)", "季付总额"),
            ("年订阅额(元/年)", "年付总额"),
        ],
        "inputs_en": [
            ("Monthly(per month)", "Monthly total"),
            ("Quarterly(per quarter)", "Quarterly total"),
            ("Yearly(per year)", "Yearly total"),
        ],
        "calc_js": """var monthly=a+(c>0?c/12:0)+(b>0?b/3:0);
var yearly=monthly*12;
document.getElementById('rv').textContent=monthly.toFixed(0)+'/month';
document.getElementById('rd').textContent='Avg monthly: '+monthly.toFixed(0)+' | Quarterly: '+(b||0)+' | Yearly: '+(c||0)+' | Annual total: '+yearly.toFixed(0);
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "baking-ratio-calculator",
        "cn_name": "烘焙比例计算器",
        "en_name": "Baking Ratio Calculator",
        "cn_desc": "在线烘焙比例计算器，基于面粉量自动计算水、酵母、盐等配料用量，支持贝果、法棍、恰巴塔等常见水合比例。",
        "en_desc": "Free baking ratio calculator. Calculate water, yeast, and salt based on flour weight. Supports bagel, baguette, ciabatta hydration ratios and custom.",
        "inputs_cn": [
            ("面粉(g)", "输入面粉重量"),
            ("水合比例", "选择水合比", "select:贝果 60%,披萨 65%,吐司 68%,法棍 72%,恰巴塔 80%,自定义"),
            ("自定义比例(%)", "输入自定义水合比例"),
        ],
        "inputs_en": [
            ("Flour(g)", "Enter flour weight"),
            ("Hydration", "Select hydration", "select:Bagel 60%,Pizza 65%,Toast 68%,Baguette 72%,Ciabatta 80%,Custom"),
            ("Custom(%)", "Enter custom hydration"),
        ],
        "calc_js": """var preset=[60,65,68,72,80];
var hydrate=preset[document.getElementById('v2').selectedIndex]||65;
if(document.getElementById('v2').selectedIndex===5&&c>0)hydrate=c;
var water=(a*hydrate/100).toFixed(0);
var yeast=(a*.01).toFixed(1);
var salt=(a*.02).toFixed(1);
document.getElementById('rv').textContent=water+'g water + '+a+'g flour';
document.getElementById('rd').textContent='Water '+water+'g | Yeast(1%) '+yeast+'g | Salt(2%) '+salt+'g | Hydration '+hydrate+'%';
document.getElementById('result').style.display='block'""",
    },
    {
        "slug": "heating-cost-calculator",
        "cn_name": "取暖费用计算器",
        "en_name": "Heating Cost Calculator",
        "cn_desc": "在线取暖费用计算器，根据取暖器功率、使用时长和电价计算每日、每月费用，帮你选择最经济的取暖方案。",
        "en_desc": "Free heating cost calculator. Estimate daily and monthly heating costs based on heater wattage, usage hours, and electricity price per kWh.",
        "inputs_cn": [
            ("取暖器功率(W)", "输入功率瓦数"),
            ("每日使用(h)", "每日使用小时数"),
            ("电价(元/kWh)", "每度电价格"),
        ],
        "inputs_en": [
            ("Heater Power(W)", "Enter wattage"),
            ("Daily Usage(h)", "Hours per day"),
            ("Electricity Price(per kWh)", "Price per kWh"),
        ],
        "calc_js": """var kwhPerDay=(a*b)/1000;
var costDay=kwhPerDay*c;
var costMonth=costDay*30;
var costSeason=costDay*120;
document.getElementById('rv').textContent=costDay.toFixed(2)+'/day';
document.getElementById('rd').textContent=kwhPerDay.toFixed(2)+' kWh/day | Month: '+costMonth.toFixed(0)+' | Winter(4mo): '+costSeason.toFixed(0);
document.getElementById('result').style.display='block'""",
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\nTotal: {len(TOOLS)} tools generated')
