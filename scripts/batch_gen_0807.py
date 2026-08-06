#!/usr/bin/env python3
"""批量生成5个计算器工具 — 2026-08-07"""
import sys
sys.path.insert(0, '/home/chison/tools-site/scripts')
from gen_tool import gen_tool

TOOLS = [
    {
        "slug": "salary-to-hourly-calculator",
        "cn_name": "年薪转时薪计算器",
        "en_name": "Salary to Hourly Rate Calculator",
        "cn_desc": "将年薪换算为时薪，输入年薪和工作时长，自动计算每小时收入。支持周工作小时和年工作周数调整。",
        "en_desc": "Convert your annual salary to hourly rate. Enter your annual salary, weekly hours, and work weeks per year to see your effective hourly pay.",
        "inputs_cn": [
            ("年薪(元)", "例: 120000"),
            ("每周工作小时", "例: 40"),
            ("每年工作周数", "例: 48"),
        ],
        "inputs_en": [
            ("Annual Salary ($)", "e.g. 50000"),
            ("Hours per Week", "e.g. 40"),
            ("Work Weeks per Year", "e.g. 48"),
        ],
        "calc_js": "var totalHours=a*b*c; var result=totalHours>0?(a/totalHours).toFixed(2):'0'; document.getElementById('result').innerHTML='时薪: <strong>'+result+'</strong> 元/小时';",
    },
    {
        "slug": "discount-percent-calculator",
        "cn_name": "折扣百分比计算器",
        "en_name": "Discount Percentage Calculator",
        "cn_desc": "计算打折后的价格，输入原价和折扣率，一键得出折后价和节省金额。",
        "en_desc": "Calculate the final price after discount. Enter original price and discount percentage to see your savings and final price instantly.",
        "inputs_cn": [
            ("原价(元)", "例: 200"),
            ("折扣率(%)", "例: 30"),
        ],
        "inputs_en": [
            ("Original Price ($)", "e.g. 200"),
            ("Discount (%)", "e.g. 30"),
        ],
        "calc_js": "var discount=a*b/100; var finalPrice=(a-discount).toFixed(2); document.getElementById('result').innerHTML='折后价: <strong>'+finalPrice+'</strong> 元 | 节省: <strong>'+discount.toFixed(2)+'</strong> 元';",
    },
    {
        "slug": "circumference-calculator",
        "cn_name": "圆的周长计算器",
        "en_name": "Circle Circumference Calculator",
        "cn_desc": "计算圆的周长，输入半径或直径，自动使用圆周率公式计算，支持两种模式。",
        "en_desc": "Calculate the circumference of a circle. Enter radius or diameter, and get results using the pi formula automatically. Supports both modes.",
        "inputs_cn": [
            ("半径", "例: 5"),
        ],
        "inputs_en": [
            ("Radius", "e.g. 5"),
        ],
        "calc_js": "var circumference=(2*Math.PI*a).toFixed(4); var diameter=(2*a).toFixed(4); var area=(Math.PI*a*a).toFixed(4); document.getElementById('result').innerHTML='周长: <strong>'+circumference+'</strong> | 直径: <strong>'+diameter+'</strong> | 面积: <strong>'+area+'</strong>';",
    },
    {
        "slug": "grade-percentage-calculator",
        "cn_name": "成绩百分比计算器",
        "en_name": "Grade Percentage Calculator",
        "cn_desc": "计算考试得分百分比，输入得分和满分，自动换算成百分制成绩。适用于学生、教师快速评分。",
        "en_desc": "Calculate test score as a percentage. Enter earned points and total possible points to get percentage and letter grade instantly. Perfect for students and teachers.",
        "inputs_cn": [
            ("得分", "例: 85"),
            ("满分", "例: 100"),
        ],
        "inputs_en": [
            ("Points Earned", "e.g. 85"),
            ("Total Points", "e.g. 100"),
        ],
        "calc_js": "var pct=b>0?(a/b*100).toFixed(1):'0'; var grade=''; if(pct>=90)grade='A'; else if(pct>=80)grade='B'; else if(pct>=70)grade='C'; else if(pct>=60)grade='D'; else grade='F'; document.getElementById('result').innerHTML='百分比: <strong>'+pct+'%</strong> | 等级: <strong>'+grade+'</strong>';",
    },
    {
        "slug": "grocery-budget-calculator",
        "cn_name": "买菜预算计算器",
        "en_name": "Grocery Budget Calculator",
        "cn_desc": "规划家庭买菜预算，输入人数和每餐预算，自动计算周/月食品开支。",
        "en_desc": "Plan your grocery budget easily. Enter household size and per-meal budget to get weekly and monthly food cost estimates.",
        "inputs_cn": [
            ("家庭人数", "例: 3"),
            ("每人每餐预算(元)", "例: 15"),
        ],
        "inputs_en": [
            ("Household Size", "e.g. 3"),
            ("Budget per Meal ($)", "e.g. 5"),
        ],
        "calc_js": "var daily=a*b*3; var weekly=daily*7; var monthly=weekly*4; document.getElementById('result').innerHTML='每日: <strong>'+daily.toFixed(0)+'</strong> 元 | 每周: <strong>'+weekly.toFixed(0)+'</strong> 元 | 每月: <strong>'+monthly.toFixed(0)+'</strong> 元';",
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n生成了 {len(TOOLS)} 个工具')
