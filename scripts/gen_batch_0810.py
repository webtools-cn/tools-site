#!/usr/bin/env python3
"""批量生成8个新计算器工具"""
import sys
sys.path.insert(0, '/home/chison/tools-site/scripts')
from gen_tool import gen_tool

TOOLS = [
    {
        'slug': 'equity-loan-calculator',
        'cn_name': '股权贷款计算器',
        'en_name': 'Equity Loan Calculator',
        'cn_desc': '计算股权抵押贷款月供、总利息和还款总额，支持等额本息和等额本金两种方式。',
        'en_desc': 'Calculate equity loan monthly payments, total interest, and total repayment. Supports equal installments and equal principal methods.',
        'inputs_cn': [
            ('贷款金额（元）', '例如：100000'),
            ('年利率（%）', '例如：4.5'),
            ('贷款期限（年）', '例如：10'),
            ('还款方式', '等额本息', 'select:等额本息,等额本金'),
        ],
        'inputs_en': [
            ('Loan Amount ($)', 'e.g. 100000'),
            ('Annual Interest Rate (%)', 'e.g. 4.5'),
            ('Loan Term (Years)', 'e.g. 10'),
            ('Payment Method', 'Equal Installments', 'select:Equal Installments,Equal Principal'),
        ],
        'calc_js': 'var p=a, r=b/100/12, n=c*12, method=v4; var monthly, total, interest; if(method=="Equal Installments"||method=="等额本息"){ var x=Math.pow(1+r,n); monthly=(p*r*x)/(x-1); total=monthly*n; } else { var mp=p/n; monthly=mp+p*r; var sum=0; for(var i=0;i<n;i++) sum+=mp+(p-mp*i)*r; monthly=sum/n; total=sum; } interest=total-p; var out="月供 ¥"+monthly.toFixed(2)+" | 总利息 ¥"+interest.toFixed(2)+" | 总还款 ¥"+total.toFixed(2); document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'freight-cost-calculator',
        'cn_name': '货运成本计算器',
        'en_name': 'Freight Cost Calculator',
        'cn_desc': '根据货物重量、运输距离和单价计算货运总成本，支持多种运输方式选择。',
        'en_desc': 'Calculate total freight cost based on cargo weight, distance, and unit price. Supports multiple transport modes.',
        'inputs_cn': [
            ('货物重量（kg）', '例如：500'),
            ('运输距离（km）', '例如：200'),
            ('每公里单价（元/km）', '例如：3.5'),
            ('运输方式', '公路运输', 'select:公路运输,铁路运输,航空运输,海运'),
        ],
        'inputs_en': [
            ('Cargo Weight (kg)', 'e.g. 500'),
            ('Distance (km)', 'e.g. 200'),
            ('Rate per km ($)', 'e.g. 3.5'),
            ('Transport Mode', 'Road', 'select:Road,Rail,Air,Sea'),
        ],
        'calc_js': 'var weight=a, dist=b, rate=c, mode=v4; var multiplier={"公路运输":1,"Road":1,"铁路运输":0.7,"Rail":0.7,"航空运输":2.5,"Air":2.5,"海运":0.4,"Sea":0.4}; var m=multiplier[mode]||1; var cost=weight*dist*rate*m/100; var out="总运费 ¥"+cost.toFixed(2)+" | 运输方式倍率 "+m; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'pet-calorie-calculator',
        'cn_name': '宠物卡路里计算器',
        'en_name': 'Pet Calorie Calculator',
        'cn_desc': '根据宠物体重和活动水平计算每日所需卡路里，帮助科学喂养猫咪和狗狗。',
        'en_desc': 'Calculate daily calorie needs based on pet weight and activity level. Helps feed cats and dogs scientifically.',
        'inputs_cn': [
            ('宠物类型', '狗', 'select:狗,猫'),
            ('体重（kg）', '例如：10'),
            ('活动水平', '正常', 'select:低,正常,高'),
        ],
        'inputs_en': [
            ('Pet Type', 'Dog', 'select:Dog,Cat'),
            ('Weight (kg)', 'e.g. 10'),
            ('Activity Level', 'Normal', 'select:Low,Normal,High'),
        ],
        'calc_js': 'var type=v1, weight=a, activity=v3; var rer, factor; if(type=="狗"||type=="Dog"){ rer=70*Math.pow(weight,0.75); } else { rer=70*Math.pow(weight,0.67); } if(activity=="低"||activity=="Low"){ factor=1.2; } else if(activity=="高"||activity=="High"){ factor=1.8; } else { factor=1.4; } var cal=rer*factor; var out="每日需 "+Math.round(cal)+" 千卡 | RER "+Math.round(rer)+" 千卡"; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'event-capacity-calculator',
        'cn_name': '活动场地容量计算器',
        'en_name': 'Event Capacity Calculator',
        'cn_desc': '根据场地面积和活动类型计算最大容纳人数，支持站立、剧场和宴会三种布局。',
        'en_desc': 'Calculate max capacity based on venue area and event type. Supports standing, theater, and banquet layouts.',
        'inputs_cn': [
            ('场地面积（m²）', '例如：200'),
            ('布局类型', '剧场式', 'select:站立式,剧场式,宴会式'),
        ],
        'inputs_en': [
            ('Venue Area (m²)', 'e.g. 200'),
            ('Layout Type', 'Theater', 'select:Standing,Theater,Banquet'),
        ],
        'calc_js': 'var area=a, layout=v2; var perPerson={"站立式":0.5,"Standing":0.5,"剧场式":1.2,"Theater":1.2,"宴会式":2.5,"Banquet":2.5}; var pp=perPerson[layout]||1.2; var cap=Math.floor(area/pp); var out="最大容纳 "+cap+" 人 | 人均 "+pp+" m²"; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'tree-age-calculator',
        'cn_name': '树龄计算器',
        'en_name': 'Tree Age Calculator',
        'cn_desc': '通过测量树木胸径和生长因子估算树龄，支持多种常见树种。',
        'en_desc': 'Estimate tree age by measuring DBH and growth factor. Supports multiple common tree species.',
        'inputs_cn': [
            ('胸径（cm）', '例如：30'),
            ('树种', '橡树', 'select:橡树,松树,枫树,榆树,白蜡树'),
        ],
        'inputs_en': [
            ('DBH (cm)', 'e.g. 30'),
            ('Species', 'Oak', 'select:Oak,Pine,Maple,Elm,Ash'),
        ],
        'calc_js': 'var dbh=a, species=v2; var gf={"橡树":5,"Oak":5,"松树":4.5,"Pine":4.5,"枫树":4,"Maple":4,"榆树":4,"Elm":4,"白蜡树":4,"Ash":4}; var g=gf[species]||4.5; var age=Math.round(dbh/g*2.54); var out="估算树龄 "+age+" 年 | 生长因子 "+g; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'voice-over-cost-calculator',
        'cn_name': '配音费用计算器',
        'en_name': 'Voice Over Cost Calculator',
        'cn_desc': '根据配音时长、语言和类型估算配音项目费用，适用于广告、视频和播客。',
        'en_desc': 'Estimate voice-over project cost based on duration, language, and type. For ads, videos, and podcasts.',
        'inputs_cn': [
            ('脚本字数', '例如：500'),
            ('语速（字/分钟）', '例如：200', 'text:'),
            ('配音类型', '商业广告', 'select:商业广告,企业旁白,电子学习,播客'),
        ],
        'inputs_en': [
            ('Word Count', 'e.g. 500'),
            ('Speaking Rate (wpm)', 'e.g. 150', 'text:'),
            ('VO Type', 'Commercial', 'select:Commercial,Corporate,ELearning,Podcast'),
        ],
        'calc_js': 'var words=a, rate=parseFloat(b)||150, type=v3; var minutes=words/rate; var ratePerMin={"商业广告":300,"Commercial":300,"企业旁白":200,"Corporate":200,"电子学习":150,"ELearning":150,"播客":100,"Podcast":100}; var rpm=ratePerMin[type]||200; var cost=minutes*rpm; var out="预估费用 ¥"+cost.toFixed(0)+" | 时长 "+minutes.toFixed(1)+"分钟 | 费率 ¥"+rpm+"/分钟"; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'lawn-seed-calculator',
        'cn_name': '草坪种子计算器',
        'en_name': 'Lawn Seed Calculator',
        'cn_desc': '计算播种草坪所需种子量，支持新播和补播两种场景，按面积精确计算。',
        'en_desc': 'Calculate seed needed for lawn seeding. Supports new lawn and overseeding with area-based precision.',
        'inputs_cn': [
            ('草坪面积（m²）', '例如：50'),
            ('播种类型', '新播种', 'select:新播种,补播'),
        ],
        'inputs_en': [
            ('Lawn Area (m²)', 'e.g. 50'),
            ('Seeding Type', 'New Lawn', 'select:New Lawn,Overseeding'),
        ],
        'calc_js': 'var area=a, type=v2; var ratePerM2={"新播种":35,"New Lawn":35,"补播":18,"Overseeding":18}; var rate=ratePerM2[type]||35; var seed=area*rate; var out="需要 "+seed.toFixed(0)+" 克种子 | 播种率 "+rate+" g/m²"; document.getElementById("result").innerHTML=out;',
    },
    {
        'slug': 'candle-burn-time-calculator',
        'cn_name': '蜡烛燃烧时间计算器',
        'en_name': 'Candle Burn Time Calculator',
        'cn_desc': '根据蜡烛重量和蜡类型估算燃烧总时长，帮助选择合适尺寸的蜡烛。',
        'en_desc': 'Estimate total burn time based on candle weight and wax type. Helps choose the right candle size.',
        'inputs_cn': [
            ('蜡烛重量（g）', '例如：200'),
            ('蜡类型', '大豆蜡', 'select:大豆蜡,蜂蜡,石蜡,椰子蜡'),
        ],
        'inputs_en': [
            ('Candle Weight (g)', 'e.g. 200'),
            ('Wax Type', 'Soy Wax', 'select:Soy Wax,Beeswax,Paraffin,Coconut Wax'),
        ],
        'calc_js': 'var weight=a, wax=v2; var burnRate={"大豆蜡":7,"Soy Wax":7,"蜂蜡":5.5,"Beeswax":5.5,"石蜡":8,"Paraffin":8,"椰子蜡":6.5,"Coconut Wax":6.5}; var rate=burnRate[wax]||7; var hours=weight/rate; var out="预计燃烧 "+hours.toFixed(1)+" 小时 | 燃烧率 "+rate+" g/小时"; document.getElementById("result").innerHTML=out;',
    },
]

print(f'开始批量生成 {len(TOOLS)} 个工具...\n')
for i, t in enumerate(TOOLS):
    print(f'[{i+1}/{len(TOOLS)}] ', end='')
    gen_tool(**t)

print(f'\n✅ 完成！共生成 {len(TOOLS)} 个工具')
