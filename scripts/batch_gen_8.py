#!/usr/bin/env python3
"""Batch generate 8 tools — uses gen_tool() with correct tuple-list format"""
import sys
sys.path.insert(0, '/home/chison/tools-site/scripts')
from gen_tool import gen_tool

tools = [
    {
        'slug': 'roi-calculator',
        'cn_name': 'ROI投资回报率计算器',
        'en_name': 'ROI Calculator',
        'cn_desc': '计算投资回报率(ROI)，输入投资成本和收益即可快速得到百分比回报率和净利润',
        'en_desc': 'Calculate Return on Investment (ROI) — enter your investment cost and gain to get the percentage return and net profit instantly',
        'inputs_cn': [('投资金额(元)', '如 10000'), ('收益金额(元)', '如 15000')],
        'inputs_en': [('Investment Amount ($)', 'e.g. 10000'), ('Gain Amount ($)', 'e.g. 15000')],
        'calc_js': 'if(a<=0){document.getElementById("rv").innerHTML="投资金额必须大于0";document.getElementById("result").style.display="block";return}var roi=((b-a)/a)*100;var profit=b-a;document.getElementById("rv").innerHTML="ROI: <b>"+roi.toFixed(2)+"%</b><br>"+(profit>=0?"净利润":"净亏损")+": <b>"+(profit>=0?"+":"")+profit.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'break-even-calculator',
        'cn_name': '盈亏平衡点计算器',
        'en_name': 'Break-Even Point Calculator',
        'cn_desc': '计算盈亏平衡点，输入固定成本、变动成本和单价即可得到回本所需销量和销售额',
        'en_desc': 'Calculate the break-even point — enter fixed costs, variable costs, and unit price to find the units and revenue needed to break even',
        'inputs_cn': [('固定成本(元)', '如 50000'), ('单位变动成本(元)', '如 30'), ('销售单价(元)', '如 80')],
        'inputs_en': [('Fixed Costs ($)', 'e.g. 50000'), ('Variable Cost/Unit ($)', 'e.g. 30'), ('Selling Price/Unit ($)', 'e.g. 80')],
        'calc_js': 'var c=parseFloat(document.getElementById("v3").value);if(a<=c){document.getElementById("rv").innerHTML="单价必须大于变动成本";document.getElementById("result").style.display="block";return}var bep=a/(b-c);var rev=bep*b;document.getElementById("rv").innerHTML="保本销量: <b>"+Math.ceil(bep)+" 件</b><br>保本销售额: <b>"+rev.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'markup-calculator',
        'cn_name': '加价率计算器',
        'en_name': 'Markup Calculator',
        'cn_desc': '根据成本和目标售价计算加价率和毛利率，帮助定价决策',
        'en_desc': 'Calculate markup percentage and gross margin from cost and selling price to guide your pricing strategy',
        'inputs_cn': [('成本价(元)', '如 60'), ('售价(元)', '如 100')],
        'inputs_en': [('Cost Price ($)', 'e.g. 60'), ('Selling Price ($)', 'e.g. 100')],
        'calc_js': 'if(a<=0){document.getElementById("rv").innerHTML="成本不能为0";document.getElementById("result").style.display="block";return}var markup=((b-a)/a)*100;var margin=((b-a)/b)*100;var profit=b-a;document.getElementById("rv").innerHTML="加价率: <b>"+markup.toFixed(2)+"%</b><br>毛利率: <b>"+margin.toFixed(2)+"%</b><br>利润: <b>"+profit.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'commission-calculator',
        'cn_name': '佣金计算器',
        'en_name': 'Commission Calculator',
        'cn_desc': '计算销售佣金，按百分比提成快速得出应得佣金和实际到手金额',
        'en_desc': 'Calculate sales commission by percentage rate — quickly see your earned commission and net take-home amount',
        'inputs_cn': [('销售额(元)', '如 200000'), ('佣金率(%)', '如 5')],
        'inputs_en': [('Sales Amount ($)', 'e.g. 200000'), ('Commission Rate (%)', 'e.g. 5')],
        'calc_js': 'var comm=a*b/100;document.getElementById("rv").innerHTML="佣金金额: <b>"+comm.toFixed(2)+"</b><br>实际到手: <b>"+(a-comm).toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'pace-calculator',
        'cn_name': '跑步配速计算器',
        'en_name': 'Running Pace Calculator',
        'cn_desc': '根据跑步距离和时间计算配速和速度，适合马拉松训练和日常跑步分析',
        'en_desc': 'Calculate running pace and speed from distance and time — perfect for marathon training and daily run analysis',
        'inputs_cn': [('距离(公里)', '如 5'), ('时间(分钟)', '如 25')],
        'inputs_en': [('Distance (km)', 'e.g. 5'), ('Time (minutes)', 'e.g. 25')],
        'calc_js': 'if(a<=0||b<=0){document.getElementById("rv").innerHTML="请输入有效值";document.getElementById("result").style.display="block";return}var pace=b/a;var pmin=Math.floor(pace);var psec=Math.round((pace-pmin)*60);var speed=a/(b/60);document.getElementById("rv").innerHTML="平均配速: <b>"+pmin+"分"+psec+"秒/公里</b><br>平均速度: <b>"+speed.toFixed(2)+" km/h</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'calorie-burn-calculator',
        'cn_name': '运动消耗卡路里计算器',
        'en_name': 'Calorie Burn Calculator',
        'cn_desc': '根据运动类型、体重和时间估算卡路里消耗，支持跑步、游泳、骑行等常见运动',
        'en_desc': 'Estimate calories burned based on activity type, weight, and duration — supports running, swimming, cycling, and more',
        'inputs_cn': [('体重(公斤)', '如 70'), ('时间(分钟)', '如 30'), ('运动MET值', '跑步8.0/游泳7.0/骑行7.5/跳绳10.0')],
        'inputs_en': [('Weight (kg)', 'e.g. 70'), ('Duration (min)', 'e.g. 30'), ('MET Value', 'Run 8.0/Swim 7.0/Cycle 7.5/JumpRope 10.0')],
        'calc_js': 'var c=parseFloat(document.getElementById("v3").value);var cal=c*a*b/60;document.getElementById("rv").innerHTML="消耗卡路里: <b>"+Math.round(cal)+" kcal</b><br>≈ 脂肪: <b>"+(cal/7700*1000).toFixed(1)+" 克</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'gpa-calculator',
        'cn_name': 'GPA成绩计算器',
        'en_name': 'GPA Calculator',
        'cn_desc': '快速计算GPA绩点，支持4.0评分体系，输入课程分数和学分即可得出结果',
        'en_desc': 'Calculate your GPA quickly on a 4.0 scale — just enter your course grades and credits to get your GPA',
        'inputs_cn': [('课程A成绩(百分制)', '如 85'), ('课程A学分', '如 3')],
        'inputs_en': [('Course A Grade (%)', 'e.g. 85'), ('Course A Credits', 'e.g. 3')],
        'calc_js': 'var g1=a;var c1=b;var g2=parseFloat(document.getElementById("v3")?document.getElementById("v3").value:0);var c2=0;var gp=function(g){if(g>=90)return 4.0;if(g>=85)return 3.7;if(g>=82)return 3.3;if(g>=78)return 3.0;if(g>=75)return 2.7;if(g>=72)return 2.3;if(g>=68)return 2.0;if(g>=64)return 1.7;if(g>=60)return 1.0;return 0};var tp=gp(g1)*c1;if(!isNaN(g2))tp+=gp(g2)*(document.getElementById("v4")?parseFloat(document.getElementById("v4").value):0);var tc=c1;if(!isNaN(g2))tc+=parseFloat(document.getElementById("v4")?document.getElementById("v4").value:0);var gpa=tp/tc;document.getElementById("rv").innerHTML="GPA (4.0制): <b>"+gpa.toFixed(2)+"</b><br>等级: <b>"+(gpa>=3.7?"优秀":gpa>=3.0?"良好":gpa>=2.0?"中等":"需努力")+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'final-grade-calculator',
        'cn_name': '期末考试目标分计算器',
        'en_name': 'Final Grade Calculator',
        'cn_desc': '计算期末考试需要考多少分才能达到目标总成绩，帮助制定复习策略',
        'en_desc': 'Calculate what score you need on your final exam to reach your target overall grade — plan your study strategy',
        'inputs_cn': [('当前成绩(%)', '如 85'), ('目标总成绩(%)', '如 90'), ('期末权重(%)', '如 40')],
        'inputs_en': [('Current Grade (%)', 'e.g. 85'), ('Target Grade (%)', 'e.g. 90'), ('Final Exam Weight (%)', 'e.g. 40')],
        'calc_js': 'var c=parseFloat(document.getElementById("v3").value);if(c<=0||c>100){document.getElementById("rv").innerHTML="权重需在1-100之间";document.getElementById("result").style.display="block";return}var need=(b-a*(1-c/100))/(c/100);var msg=need>100?"目标无法达成!":need<=0?"即使不考也能达标!":"需得 <b>"+need.toFixed(1)+"%</b>";document.getElementById("rv").innerHTML=msg+"<br>目标总成绩: <b>"+b+"%</b><br>"+(need<=100&&need>0?"安全余量: <b>"+(100-need).toFixed(1)+"%</b>":"");document.getElementById("result").style.display="block"',
    },
]

for i, t in enumerate(tools):
    print(f"[{i+1}/8] Generating {t['slug']}...")
    gen_tool(**t)

print(f"\n✅ 成功生成 {len(tools)} 个工具")
