#!/usr/bin/env python3
"""批量生成8个计算器工具"""
import json, os, sys
sys.path.insert(0, '/home/chison/tools-site/scripts')
from gen_tool import gen_tool

TOOLS = [
    {
        'slug': 'apr-calculator',
        'cn_name': '年化利率计算器',
        'en_name': 'APR Calculator',
        'cn_desc': '根据贷款费用和利率计算实际年化利率(APR)，包含所有费用的真实借款成本',
        'en_desc': 'Calculate the true Annual Percentage Rate including all loan fees and costs',
        'inputs_cn': [('贷款金额(元)', '如: 100000'), ('年利率(%)', '如: 5.0'), ('手续费(%)', '如: 1.0')],
        'inputs_en': [('Loan Amount ($)', 'e.g. 100000'), ('Nominal Rate (%)', 'e.g. 5.0'), ('Origination Fee (%)', 'e.g. 1.0')],
        'calc_js': 'var fee=a*c/100;var net=a-fee;var mr=b/100/12;var n=12;var mp=mr===0?net/n:net*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1);var apr=((mp*12-net)/net*100);document.getElementById("rv").innerHTML="实际年化: <b>"+apr.toFixed(2)+"%</b><br>净到手: <b>"+net.toFixed(0)+" 元</b><br>手续费: <b>"+fee.toFixed(0)+" 元</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'tip-calculator',
        'cn_name': '小费计算器',
        'en_name': 'Tip Calculator',
        'cn_desc': '快速计算餐厅小费和AA制分摊，支持自定义小费比例',
        'en_desc': 'Quickly calculate restaurant tips and split the bill evenly among diners',
        'inputs_cn': [('账单金额(元)', '如: 380'), ('小费比例(%)', '如: 15'), ('分摊人数', '如: 4')],
        'inputs_en': [('Bill Amount ($)', 'e.g. 85'), ('Tip Percentage (%)', 'e.g. 18'), ('Split Among', 'e.g. 3')],
        'calc_js': 'var tip=a*b/100;var total=a+tip;var per=c>0?total/c:total;document.getElementById("rv").innerHTML="小费: <b>"+tip.toFixed(2)+"</b><br>总金额: <b>"+total.toFixed(2)+"</b><br>人均: <b>"+per.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'discount-calculator',
        'cn_name': '折扣计算器',
        'en_name': 'Discount Calculator',
        'cn_desc': '计算打折后的实际价格和节省金额，支持满减和百分比折扣',
        'en_desc': 'Calculate final price after discounts and how much you will save',
        'inputs_cn': [('原价(元)', '如: 299'), ('折扣(%)', '如: 20'), ('额外满减(元)', '如: 10')],
        'inputs_en': [('Original Price ($)', 'e.g. 85'), ('Discount (%)', 'e.g. 25'), ('Extra Off ($)', 'e.g. 5')],
        'calc_js': 'var disc=a*b/100;var final=a-disc-c;var saved=disc+c;document.getElementById("rv").innerHTML="折后价: <b>"+Math.max(0,final).toFixed(2)+" 元</b><br>节省: <b>"+saved.toFixed(2)+" 元</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'commission-calculator',
        'cn_name': '佣金计算器',
        'en_name': 'Commission Calculator',
        'cn_desc': '计算销售佣金收入，支持阶梯费率和基础工资',
        'en_desc': 'Calculate sales commission income with tiered rates and base salary',
        'inputs_cn': [('销售额(元)', '如: 50000'), ('佣金比例(%)', '如: 5'), ('基础工资(元)', '如: 3000')],
        'inputs_en': [('Sales Amount ($)', 'e.g. 50000'), ('Commission Rate (%)', 'e.g. 5'), ('Base Salary ($)', 'e.g. 3000')],
        'calc_js': 'var comm=a*b/100;var total=comm+c;document.getElementById("rv").innerHTML="佣金: <b>"+comm.toFixed(2)+" 元</b><br>总收入: <b>"+total.toFixed(2)+" 元</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'fuel-cost-calculator',
        'cn_name': '油费计算器',
        'en_name': 'Fuel Cost Calculator',
        'cn_desc': '根据里程、油耗和油价计算出行油费，支持往返计算',
        'en_desc': 'Calculate trip fuel costs based on distance, fuel efficiency and price',
        'inputs_cn': [('单程距离(km)', '如: 200'), ('百公里油耗(L)', '如: 8'), ('油价(元/L)', '如: 7.5')],
        'inputs_en': [('Distance (km)', 'e.g. 300'), ('Fuel Consumption (L/100km)', 'e.g. 8'), ('Fuel Price ($/L)', 'e.g. 1.5')],
        'calc_js': 'var fuel=a/100*b;var cost=fuel*c;document.getElementById("rv").innerHTML="单程油耗: <b>"+fuel.toFixed(1)+" L</b><br>单程费用: <b>"+cost.toFixed(2)+" 元</b><br>往返费用: <b>"+(cost*2).toFixed(2)+" 元</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'electricity-cost-calculator',
        'cn_name': '电费计算器',
        'en_name': 'Electricity Cost Calculator',
        'cn_desc': '根据电器功率和使用时长计算每日和每月电费',
        'en_desc': 'Calculate daily and monthly electricity costs based on appliance power and usage',
        'inputs_cn': [('功率(瓦)', '如: 1500'), ('每日使用(小时)', '如: 5'), ('电价(元/度)', '如: 0.6')],
        'inputs_en': [('Power (Watts)', 'e.g. 1500'), ('Daily Usage (Hours)', 'e.g. 5'), ('Rate ($/kWh)', 'e.g. 0.12')],
        'calc_js': 'var kwh=a*b/1000;var daily=kwh*c;var monthly=daily*30;var yearly=daily*365;document.getElementById("rv").innerHTML="每日电费: <b>"+daily.toFixed(2)+" 元</b><br>每月电费: <b>"+monthly.toFixed(2)+" 元</b><br>每年电费: <b>"+yearly.toFixed(2)+" 元</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'body-fat-calculator',
        'cn_name': '体脂率计算器',
        'en_name': 'Body Fat Calculator',
        'cn_desc': '根据身高体重和腰围估算体脂率，基于美国海军方法',
        'en_desc': 'Estimate body fat percentage using the U.S. Navy method based on height, weight and measurements',
        'inputs_cn': [('身高(cm)', '如: 170'), ('体重(kg)', '如: 70'), ('腰围(cm)', '如: 80')],
        'inputs_en': [('Height (cm)', 'e.g. 170'), ('Weight (kg)', 'e.g. 70'), ('Waist (cm)', 'e.g. 80')],
        'calc_js': 'var bf=(495/(1.0324-0.19077*Math.log10(c-(a*0.3937)*0.382)+0.15456*Math.log10(a))-450);document.getElementById("rv").innerHTML="估算体脂率: <b>"+bf.toFixed(1)+"%</b><br>体脂重量: <b>"+(b*bf/100).toFixed(1)+" kg</b><br>瘦体重: <b>"+(b*(1-bf/100)).toFixed(1)+" kg</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'calorie-calculator',
        'cn_name': '每日热量计算器',
        'en_name': 'Daily Calorie Calculator',
        'cn_desc': '根据身高体重和活动水平计算每日基础代谢和总热量需求',
        'en_desc': 'Calculate daily BMR and total calorie needs based on your stats and activity level',
        'inputs_cn': [('体重(kg)', '如: 70'), ('身高(cm)', '如: 170'), ('年龄', '如: 30')],
        'inputs_en': [('Weight (kg)', 'e.g. 70'), ('Height (cm)', 'e.g. 170'), ('Age', 'e.g. 30')],
        'calc_js': 'var bmr=10*a+6.25*b-5*c+5;var tdee_sedentary=bmr*1.2;var tdee_moderate=bmr*1.55;var tdee_active=bmr*1.9;document.getElementById("rv").innerHTML="基础代谢: <b>"+bmr.toFixed(0)+" kcal</b><br>久坐: <b>"+tdee_sedentary.toFixed(0)+"</b> | 中等: <b>"+tdee_moderate.toFixed(0)+"</b><br>高强度: <b>"+tdee_active.toFixed(0)+" kcal</b>";document.getElementById("result").style.display="block"',
    },
]

print(f"准备生成 {len(TOOLS)} 个工具...")
for i, t in enumerate(TOOLS):
    try:
        gen_tool(**t)
        print(f"  [{i+1}/{len(TOOLS)}] ✅ {t['slug']}")
    except Exception as e:
        print(f"  [{i+1}/{len(TOOLS)}] ❌ {t['slug']}: {e}")

print(f"\n✅ 完成！生成了 {len(TOOLS)} 个工具")
