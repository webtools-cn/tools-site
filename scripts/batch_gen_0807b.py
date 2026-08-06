#!/usr/bin/env python3
"""Batch generate 5 new tools - 2026-08-07 run"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_tool import gen_tool

TOOLS = [
    # 1. Circle Area Calculator
    {
        'slug': 'circle-area-calculator',
        'cn_name': '圆面积计算器',
        'en_name': 'Circle Area Calculator',
        'cn_desc': '快速计算圆的面积和周长，输入半径即可得到精确结果。支持多种单位换算。',
        'en_desc': 'Calculate circle area and circumference instantly. Enter radius to get precise results with formulas shown.',
        'inputs_cn': [
            ('半径', '输入半径数值'),
            ('单位', '', 'select:厘米,米,英寸,英尺'),
        ],
        'inputs_en': [
            ('Radius', 'Enter radius value'),
            ('Unit', '', 'select:cm,m,inches,feet'),
        ],
        'calc_js': '''
var pi=Math.PI;
var area=pi*a*a;
var circum=2*pi*a;
var isCM=v2el&&v2el.value==='厘米'?'cm':v2el&&v2el.value==='米'?'m':v2el&&v2el.value==='英寸'?'in':'ft';
document.getElementById('rv').textContent=area.toFixed(2)+' '+isCM+'²';
document.getElementById('rd').textContent='周长: '+circum.toFixed(2)+' '+isCM;
document.getElementById('result').style.display='block';
'''
    },
    # 2. Horsepower to kW Converter
    {
        'slug': 'horsepower-to-kw',
        'cn_name': '马力千瓦转换器',
        'en_name': 'Horsepower to kW Converter',
        'cn_desc': '快速转换马力和千瓦，支持机械马力、公制马力和电马力三种标准。',
        'en_desc': 'Convert between horsepower and kilowatts instantly. Supports mechanical, metric, and electrical HP standards.',
        'inputs_cn': [
            ('数值', '输入数值'),
            ('输入单位', '', 'select:机械马力(hp),公制马力(PS),千瓦(kW)'),
            ('输出单位', '', 'select:千瓦(kW),机械马力(hp),公制马力(PS)'),
        ],
        'inputs_en': [
            ('Value', 'Enter value'),
            ('Input Unit', '', 'select:Mechanical HP, Metric PS, Kilowatt (kW)'),
            ('Output Unit', '', 'select:Kilowatt (kW), Mechanical HP, Metric PS'),
        ],
        'calc_js': '''
var toKW=0;
var inp=v2el.value;
if(inp.indexOf('Mechanical')>=0||inp.indexOf('机械')>=0)toKW=a*0.7457;
else if(inp.indexOf('Metric')>=0||inp.indexOf('公制')>=0)toKW=a*0.7355;
else toKW=a;
var kw=toKW;
var out=v3el? v3el.value: '';
if(out.indexOf('Mechanical')>=0||out.indexOf('机械')>=0)kw=toKW/0.7457;
else if(out.indexOf('Metric')>=0||out.indexOf('公制')>=0)kw=toKW/0.7355;
document.getElementById('rv').textContent=kw.toFixed(2);
document.getElementById('rd').textContent=(a.toFixed(2)+' '+inp.split('(')[0].trim()+' = '+kw.toFixed(2)+' '+out.split('(')[0].trim());
document.getElementById('result').style.display='block';
'''
    },
    # 3. Cube Root Calculator
    {
        'slug': 'cube-root-calculator',
        'cn_name': '立方根计算器',
        'en_name': 'Cube Root Calculator',
        'cn_desc': '快速计算任意数字的立方根，支持正负数，并展示计算过程和验证结果。',
        'en_desc': 'Calculate cube root of any number instantly. Supports negative numbers and shows verification.',
        'inputs_cn': [
            ('数值', '输入任意数字'),
        ],
        'inputs_en': [
            ('Number', 'Enter any number'),
        ],
        'calc_js': '''
var cr=Math.cbrt(a);
document.getElementById('rv').textContent='³√'+a+' = '+cr.toFixed(6);
var verify=cr*cr*cr;
document.getElementById('rd').textContent='验证: '+cr.toFixed(4)+' × '+cr.toFixed(4)+' × '+cr.toFixed(4)+' = '+verify.toFixed(4);
document.getElementById('result').style.display='block';
'''
    },
    # 4. Heat Index Calculator
    {
        'slug': 'heat-index-calc',
        'cn_name': '体感温度计算器',
        'en_name': 'Heat Index Calculator',
        'cn_desc': '根据温度和湿度计算体感温度（热指数），了解实际炎热程度，预防中暑。',
        'en_desc': 'Calculate heat index (feels-like temperature) from temperature and humidity. Understand real heat stress levels.',
        'inputs_cn': [
            ('温度 (°C)', '输入温度'),
            ('相对湿度 (%)', '输入湿度百分比'),
        ],
        'inputs_en': [
            ('Temperature (°C)', 'Enter temperature'),
            ('Relative Humidity (%)', 'Enter humidity percentage'),
        ],
        'calc_js': '''
var T=a;
var RH=b;
var HI=0;
if(T<27){
  HI=T;
}else{
  var Tf=T*9/5+32;
  var HI_f=-42.379+2.04901523*Tf+10.14333127*RH-0.22475541*Tf*RH-0.00683783*Tf*Tf-0.05481717*RH*RH+0.00122874*Tf*Tf*RH+0.00085282*Tf*RH*RH-0.00000199*Tf*Tf*RH*RH;
  HI=(HI_f-32)*5/9;
}
document.getElementById('rv').textContent=HI.toFixed(1)+' °C';
if(HI<27)document.getElementById('rd').textContent='体感舒适';
else if(HI<32)document.getElementById('rd').textContent='注意防暑';
else if(HI<41)document.getElementById('rd').textContent='⚠ 极度炎热，避免户外活动';
else document.getElementById('rd').textContent='🚨 危险！可能中暑';
document.getElementById('result').style.display='block';
'''
    },
    # 5. Sinking Fund Calculator
    {
        'slug': 'sinking-fund-calculator',
        'cn_name': '偿债基金计算器',
        'en_name': 'Sinking Fund Calculator',
        'cn_desc': '计算偿债基金定期存款金额，帮助规划未来一次性大额支出，轻松达成储蓄目标。',
        'en_desc': 'Calculate periodic sinking fund deposits for a future lump sum. Plan ahead for large expenses effortlessly.',
        'inputs_cn': [
            ('目标金额 (元)', '输入目标金额'),
            ('年限', '输入年数'),
            ('年利率 (%)', '输入年利率'),
        ],
        'inputs_en': [
            ('Target Amount ($)', 'Enter target amount'),
            ('Years', 'Enter number of years'),
            ('Annual Rate (%)', 'Enter annual interest rate'),
        ],
        'calc_js': '''
var FV=a;
var n=b;
var r=c/100;
var periods=n*12;
var rate=r/12;
var payment=0;
if(rate>0){
  payment=FV*rate/(Math.pow(1+rate,periods)-1);
}else{
  payment=FV/periods;
}
var total=payment*periods;
document.getElementById('rv').textContent='¥'+payment.toFixed(2)+'/月';
document.getElementById('rd').textContent=periods+'个月共存入 ¥'+total.toFixed(2)+'，利息 ¥'+(FV-total).toFixed(2);
document.getElementById('result').style.display='block';
'''
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n✅ 生成了 {len(TOOLS)} 个工具')
