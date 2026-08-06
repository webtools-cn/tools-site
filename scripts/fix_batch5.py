#!/usr/bin/env python3
"""Fix P0+P1 issues in 9 new calculator tools (CN+EN = 18 files)"""

import re

tools_config = {
    'composting-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let bw=parseFloat(v[0]),br=parseFloat(v[1])||60,gw=parseFloat(v[2]),gr=parseFloat(v[3])||15; let totalC=(bw*br+gw*gr); let totalN=(bw+gw); let ratio=totalC/totalN; let ideal=ratio>=25&&ratio<=35; return `总碳氮比: ${ratio.toFixed(0)}:1 | ${ideal?'✅ 理想范围(25-35:1)':'⚠️ 建议调整配比'}`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let bw=v1,br=v2||60,gw=v3,gr=v4||15; let totalC=(bw*br+gw*gr); let totalN=(bw+gw); let ratio=totalC/totalN; let ideal=ratio>=25&&ratio<=35; var r=`总碳氮比: ${ratio.toFixed(0)}:1 | ${ideal?'✅ 理想范围(25-35:1)':'⚠️ 建议调整配比'}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let bw=parseFloat(v[0]),br=parseFloat(v[1])||60,gw=parseFloat(v[2]),gr=parseFloat(v[3])||15; let totalC=(bw*br+gw*gr); let totalN=(bw+gw); let ratio=totalC/totalN; let ideal=ratio>=25&&ratio<=35; return `总碳氮比: ${ratio.toFixed(0)}:1 | ${ideal?'✅ 理想范围(25-35:1)':'⚠️ 建议调整配比'}`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let bw=v1,br=v2||60,gw=v3,gr=v4||15; let totalC=(bw*br+gw*gr); let totalN=(bw+gw); let ratio=totalC/totalN; let ideal=ratio>=25&&ratio<=35; var r=`C:N Ratio: ${ratio.toFixed(0)}:1 | ${ideal?'✅ Ideal range (25-35:1)':'⚠️ Adjust the ratio'}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入棕色材料重量(kg)和C:N比', '输入绿色材料重量(kg)和C:N比', '点击"计算"按钮查看碳氮比结果'],
        'en_steps': ['Enter brown material weight and C:N ratio', 'Enter green material weight and C:N ratio', 'Click "Calculate" to see the C:N ratio result'],
    },
    'food-cost-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let totalCost=parseFloat(v[0]),servings=parseInt(v[1]),price=parseFloat(v[2]); let perCost=totalCost/servings; let margin=price-perCost; let marginRate=margin/price*100; return `每份成本: $${perCost.toFixed(2)} | 毛利润: $${margin.toFixed(2)} | 毛利率: ${marginRate.toFixed(1)}%`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let totalCost=v1,servings=parseInt(v2),price=v3; let perCost=totalCost/servings; let margin=price-perCost; let marginRate=margin/price*100; var r=`每份成本: $${perCost.toFixed(2)} | 毛利润: $${margin.toFixed(2)} | 毛利率: ${marginRate.toFixed(1)}%`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let totalCost=parseFloat(v[0]),servings=parseInt(v[1]),price=parseFloat(v[2]); let perCost=totalCost/servings; let margin=price-perCost; let marginRate=margin/price*100; return `每份成本: $${perCost.toFixed(2)} | 毛利润: $${margin.toFixed(2)} | 毛利率: ${marginRate.toFixed(1)}%`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let totalCost=v1,servings=parseInt(v2),price=v3; let perCost=totalCost/servings; let margin=price-perCost; let marginRate=margin/price*100; var r=`Cost/Serving: $${perCost.toFixed(2)} | Margin: $${margin.toFixed(2)} | Margin Rate: ${marginRate.toFixed(1)}%`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入食材总成本和份数', '输入每份售价', '点击"计算"按钮查看成本和利润'],
        'en_steps': ['Enter total ingredient cost and number of servings', 'Enter selling price per serving', 'Click "Calculate" to see cost and profit'],
    },
    'language-difficulty-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let hours={'ZH→EN':2200,'EN→ZH':2200,'EN→JA':2200,'ZH→JA':2200,'EN→KO':2200,'EN→AR':2200,'EN→FR':750,'EN→ES':600,'EN→DE':900,'EN→IT':750,'ZH→KO':2200,'EN→PT':750}; let key=v[0].substr(0,2)+'→'+v[1].substr(0,2); let needed=hours[key]||900; let weekly=parseFloat(v[2])||10; let weeks=needed/weekly; let months=weeks/4.3; return `预估学时: ${needed}h | 按${weekly}h/周: ${months.toFixed(1)}个月 | 难度: ${needed<=600?'⭐ 容易':needed<=900?'⭐⭐ 中等':'⭐⭐⭐ 困难'}`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let hours={'ZH→EN':2200,'EN→ZH':2200,'EN→JA':2200,'ZH→JA':2200,'EN→KO':2200,'EN→AR':2200,'EN→FR':750,'EN→ES':600,'EN→DE':900,'EN→IT':750,'ZH→KO':2200,'EN→PT':750}; let key=String(v1).substr(0,2)+'→'+String(v2).substr(0,2); let needed=hours[key]||900; let weekly=v3||10; let weeks=needed/weekly; let months=weeks/4.3; var r=`预估学时: ${needed}h | 按${weekly}h/周: ${months.toFixed(1)}个月 | 难度: ${needed<=600?'⭐ 容易':needed<=900?'⭐⭐ 中等':'⭐⭐⭐ 困难'}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let hours={'ZH→EN':2200,'EN→ZH':2200,'EN→JA':2200,'ZH→JA':2200,'EN→KO':2200,'EN→AR':2200,'EN→FR':750,'EN→ES':600,'EN→DE':900,'EN→IT':750,'ZH→KO':2200,'EN→PT':750}; let key=v[0].substr(0,2)+'→'+v[1].substr(0,2); let needed=hours[key]||900; let weekly=parseFloat(v[2])||10; let weeks=needed/weekly; let months=weeks/4.3; return `预估学时: ${needed}h | 按${weekly}h/周: ${months.toFixed(1)}个月 | 难度: ${needed<=600?'⭐ 容易':needed<=900?'⭐⭐ 中等':'⭐⭐⭐ 困难'}`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let hours={'ZH→EN':2200,'EN→ZH':2200,'EN→JA':2200,'ZH→JA':2200,'EN→KO':2200,'EN→AR':2200,'EN→FR':750,'EN→ES':600,'EN→DE':900,'EN→IT':750,'ZH→KO':2200,'EN→PT':750}; let key=String(v1).substr(0,2)+'→'+String(v2).substr(0,2); let needed=hours[key]||900; let weekly=v3||10; let weeks=needed/weekly; let months=weeks/4.3; var r=`Est. Hours: ${needed}h | At ${weekly}h/week: ${months.toFixed(1)} months | Difficulty: ${needed<=600?'⭐ Easy':needed<=900?'⭐⭐ Medium':'⭐⭐⭐ Hard'}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入母语和目标语言（如EN、ZH、JA）', '输入每周学习时长', '点击"计算"按钮查看预估学时和难度'],
        'en_steps': ['Enter your native and target language (e.g. EN, ZH, JA)', 'Enter weekly study hours', 'Click "Calculate" to see estimated hours and difficulty'],
    },
    'octave-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let freq=parseFloat(v[0])||440,octave=parseInt(v[1])||0,note=v[2]; let resultFreq=freq*Math.pow(2,octave); let low=(resultFreq/1.059463).toFixed(2); let high=(resultFreq*1.059463).toFixed(2); return `频率: ${resultFreq.toFixed(2)} Hz | 半音步进: ${low}→${resultFreq.toFixed(2)}→${high} Hz`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let freq=v1||440,octave=parseInt(v2)||0,note=v3; let resultFreq=freq*Math.pow(2,octave); let low=(resultFreq/1.059463).toFixed(2); let high=(resultFreq*1.059463).toFixed(2); var r=`频率: ${resultFreq.toFixed(2)} Hz | 半音步进: ${low}→${resultFreq.toFixed(2)}→${high} Hz`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let freq=parseFloat(v[0])||440,octave=parseInt(v[1])||0,note=v[2]; let resultFreq=freq*Math.pow(2,octave); let low=(resultFreq/1.059463).toFixed(2); let high=(resultFreq*1.059463).toFixed(2); return `频率: ${resultFreq.toFixed(2)} Hz | 半音步进: ${low}→${resultFreq.toFixed(2)}→${high} Hz`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let freq=v1||440,octave=parseInt(v2)||0,note=v3; let resultFreq=freq*Math.pow(2,octave); let low=(resultFreq/1.059463).toFixed(2); let high=(resultFreq*1.059463).toFixed(2); var r=`Frequency: ${resultFreq.toFixed(2)} Hz | Semitone steps: ${low}→${resultFreq.toFixed(2)}→${high} Hz`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入基准频率(Hz)，默认440Hz', '输入八度偏移量（正=升高，负=降低）', '点击"计算"按钮查看频率结果'],
        'en_steps': ['Enter base frequency (Hz), default 440Hz', 'Enter octave offset (positive=higher, negative=lower)', 'Click "Calculate" to see the frequency result'],
    },
    'pomodoro-planner': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let total=parseFloat(v[0]),pom=parseFloat(v[1])||25,shortB=parseFloat(v[2])||5,longEvery=parseInt(v[3])||4; let rounds=Math.ceil(total/(pom+shortB)); let totalTime=rounds*pom+(rounds-1)*shortB+Math.floor((rounds-1)/longEvery)*(15-shortB); let effectiveHours=Math.floor(totalTime/60); let effectiveMins=totalTime%60; return `${rounds}个番茄钟 | 总耗时: ${effectiveHours}h${effectiveMins}m | 专注时间: ${rounds*pom}min`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let total=v1,pom=v2||25,shortB=v3||5,longEvery=parseInt(v4)||4; let rounds=Math.ceil(total/(pom+shortB)); let totalTime=rounds*pom+(rounds-1)*shortB+Math.floor((rounds-1)/longEvery)*(15-shortB); let effectiveHours=Math.floor(totalTime/60); let effectiveMins=totalTime%60; var r=`${rounds}个番茄钟 | 总耗时: ${effectiveHours}h${effectiveMins}m | 专注时间: ${rounds*pom}min`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let total=parseFloat(v[0]),pom=parseFloat(v[1])||25,shortB=parseFloat(v[2])||5,longEvery=parseInt(v[3])||4; let rounds=Math.ceil(total/(pom+shortB)); let totalTime=rounds*pom+(rounds-1)*shortB+Math.floor((rounds-1)/longEvery)*(15-shortB); let effectiveHours=Math.floor(totalTime/60); let effectiveMins=totalTime%60; return `${rounds}个番茄钟 | 总耗时: ${effectiveHours}h${effectiveMins}m | 专注时间: ${rounds*pom}min`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let total=v1,pom=v2||25,shortB=v3||5,longEvery=parseInt(v4)||4; let rounds=Math.ceil(total/(pom+shortB)); let totalTime=rounds*pom+(rounds-1)*shortB+Math.floor((rounds-1)/longEvery)*(15-shortB); let effectiveHours=Math.floor(totalTime/60); let effectiveMins=totalTime%60; var r=`${rounds} Pomodoros | Total: ${effectiveHours}h${effectiveMins}m | Focus: ${rounds*pom}min`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入任务总时长(分钟)', '设置番茄钟和休息时间', '点击"计算"按钮查看番茄钟规划'],
        'en_steps': ['Enter total task duration (minutes)', 'Set pomodoro and break durations', 'Click "Calculate" to see your pomodoro plan'],
    },
    'retirement-score-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let age=parseInt(v[0]),retireAge=parseInt(v[1]),savings=parseFloat(v[2]),expense=parseFloat(v[3]),ret=parseFloat(v[4])/100; let yearsLeft=retireAge-age; let need=expense*25; let projected=savings*Math.pow(1+ret,yearsLeft); let score=Math.min(100,Math.round(projected/need*100)); let gap=Math.max(0,need-projected); return `评分: ${score}/100 | 退休金预测: $${(projected/1000).toFixed(0)}K | 目标: $${(need/1000).toFixed(0)}K${gap>0?' | 缺口: $'+(gap/1000).toFixed(0)+'K':''}`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let age=parseInt(v1),retireAge=parseInt(v2),savings=v3,expense=v4,ret=v5/100; let yearsLeft=retireAge-age; let need=expense*25; let projected=savings*Math.pow(1+ret,yearsLeft); let score=Math.min(100,Math.round(projected/need*100)); let gap=Math.max(0,need-projected); var r=`评分: ${score}/100 | 退休金预测: $${(projected/1000).toFixed(0)}K | 目标: $${(need/1000).toFixed(0)}K${gap>0?' | 缺口: $'+(gap/1000).toFixed(0)+'K':''}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let age=parseInt(v[0]),retireAge=parseInt(v[1]),savings=parseFloat(v[2]),expense=parseFloat(v[3]),ret=parseFloat(v[4])/100; let yearsLeft=retireAge-age; let need=expense*25; let projected=savings*Math.pow(1+ret,yearsLeft); let score=Math.min(100,Math.round(projected/need*100)); let gap=Math.max(0,need-projected); return `评分: ${score}/100 | 退休金预测: $${(projected/1000).toFixed(0)}K | 目标: $${(need/1000).toFixed(0)}K${gap>0?' | 缺口: $'+(gap/1000).toFixed(0)+'K':''}`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let age=parseInt(v1),retireAge=parseInt(v2),savings=v3,expense=v4,ret=v5/100; let yearsLeft=retireAge-age; let need=expense*25; let projected=savings*Math.pow(1+ret,yearsLeft); let score=Math.min(100,Math.round(projected/need*100)); let gap=Math.max(0,need-projected); var r=`Score: ${score}/100 | Projected: $${(projected/1000).toFixed(0)}K | Target: $${(need/1000).toFixed(0)}K${gap>0?' | Gap: $'+(gap/1000).toFixed(0)+'K':''}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入当前年龄和计划退休年龄', '输入当前储蓄、月支出和预期收益率', '点击"计算"按钮查看退休准备评分'],
        'en_steps': ['Enter current age and planned retirement age', 'Enter savings, monthly expenses and expected return rate', 'Click "Calculate" to see your retirement readiness score'],
    },
    'spring-rate-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let force=parseFloat(v[0]),disp=parseFloat(v[1]),coils=parseFloat(v[2])||0; let rate=force/disp; let result=`刚度: ${rate.toFixed(2)} N/mm`; if(coils>0) result+=` | 单圈等效: ${(rate*coils).toFixed(2)} N/mm`; return result;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let force=v1,disp=v2,coils=v3||0; let rate=force/disp; var result=`刚度: ${rate.toFixed(2)} N/mm`; if(coils>0) result+=` | 单圈等效: ${(rate*coils).toFixed(2)} N/mm`; document.getElementById('rv').textContent=result; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let force=parseFloat(v[0]),disp=parseFloat(v[1]),coils=parseFloat(v[2])||0; let rate=force/disp; let result=`刚度: ${rate.toFixed(2)} N/mm`; if(coils>0) result+=` | 单圈等效: ${(rate*coils).toFixed(2)} N/mm`; return result;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let force=v1,disp=v2,coils=v3||0; let rate=force/disp; var result=`Stiffness: ${rate.toFixed(2)} N/mm`; if(coils>0) result+=` | Per-coil: ${(rate*coils).toFixed(2)} N/mm`; document.getElementById('rv').textContent=result; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入弹簧受力(N)和变形量(mm)', '可选：输入线圈数', '点击"计算"按钮查看弹簧刚度'],
        'en_steps': ['Enter spring force (N) and displacement (mm)', 'Optional: enter number of coils', 'Click "Calculate" to see spring rate'],
    },
    'subnet-calculator-v6': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let prefix=parseInt(v[0])||64,net=parseInt(v[1])||64; let subnets=Math.pow(2,net-prefix); let hosts=Math.pow(2,128-net); let hostStr=hosts>=1e24?`${(hosts/1e24).toFixed(0)}Y`:(hosts>=1e18?`${(hosts/1e18).toFixed(0)}E`:hosts.toExponential(0)); return `子网数: ${subnets>=1e6?subnets.toExponential(0):subnets.toFixed(0)}个 | 每子网地址: ${hostStr} | /${net}`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let prefix=parseInt(v1)||64,net=parseInt(v2)||64; let subnets=Math.pow(2,net-prefix); let hosts=Math.pow(2,128-net); let hostStr=hosts>=1e24?`${(hosts/1e24).toFixed(0)}Y`:(hosts>=1e18?`${(hosts/1e18).toFixed(0)}E`:hosts.toExponential(0)); var r=`子网数: ${subnets>=1e6?subnets.toExponential(0):subnets.toFixed(0)}个 | 每子网地址: ${hostStr} | /${net}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let prefix=parseInt(v[0])||64,net=parseInt(v[1])||64; let subnets=Math.pow(2,net-prefix); let hosts=Math.pow(2,128-net); let hostStr=hosts>=1e24?`${(hosts/1e24).toFixed(0)}Y`:(hosts>=1e18?`${(hosts/1e18).toFixed(0)}E`:hosts.toExponential(0)); return `子网数: ${subnets>=1e6?subnets.toExponential(0):subnets.toFixed(0)}个 | 每子网地址: ${hostStr} | /${net}`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let prefix=parseInt(v1)||64,net=parseInt(v2)||64; let subnets=Math.pow(2,net-prefix); let hosts=Math.pow(2,128-net); let hostStr=hosts>=1e24?`${(hosts/1e24).toFixed(0)}Y`:(hosts>=1e18?`${(hosts/1e18).toFixed(0)}E`:hosts.toExponential(0)); var r=`Subnets: ${subnets>=1e6?subnets.toExponential(0):subnets.toFixed(0)} | Hosts/subnet: ${hostStr} | /${net}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入IPv6前缀长度(如64)', '输入子网前缀长度(如72)', '点击"计算"按钮查看子网数和地址数'],
        'en_steps': ['Enter IPv6 prefix length (e.g. 64)', 'Enter subnet prefix length (e.g. 72)', 'Click "Calculate" to see subnet count and host count'],
    },
    'water-footprint-calculator': {
        'cn_calc': "var v1=a,v2=b,v3=c,v4=d;let shower=parseFloat(v[0])*9.5,toilet=parseInt(v[1])*6,laundry=parseFloat(v[2])*70/7,dish=parseFloat(v[3])*15; let daily=shower+toilet+laundry+dish; let tip=daily>150?'💧 建议缩短淋浴2分钟可节水约19L/天':'✅ 用水量在合理范围内'; return `日均耗水: ${daily.toFixed(0)}L | 月均: ${(daily*30/1000).toFixed(1)}m³ | ${tip}`;",
        'cn_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let shower=v1*9.5,toilet=parseInt(v2)*6,laundry=v3*70/7,dish=v4*15; let daily=shower+toilet+laundry+dish; let tip=daily>150?'💧 建议缩短淋浴2分钟可节水约19L/天':'✅ 用水量在合理范围内'; var r=`日均耗水: ${daily.toFixed(0)}L | 月均: ${(daily*30/1000).toFixed(1)}m³ | ${tip}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'en_calc': "var v1=a,v2=b,v3=c,v4=d;let shower=parseFloat(v[0])*9.5,toilet=parseInt(v[1])*6,laundry=parseFloat(v[2])*70/7,dish=parseFloat(v[3])*15; let daily=shower+toilet+laundry+dish; let tip=daily>150?'💧 建议缩短淋浴2分钟可节水约19L/天':'✅ 用水量在合理范围内'; return `日均耗水: ${daily.toFixed(0)}L | 月均: ${(daily*30/1000).toFixed(1)}m³ | ${tip}`;",
        'en_calc_fix': "var v1=a,v2=b,v3=c,v4=d;let shower=v1*9.5,toilet=parseInt(v2)*6,laundry=v3*70/7,dish=v4*15; let daily=shower+toilet+laundry+dish; let tip=daily>150?'💧 Shorten showers by 2 min to save ~19L/day':'✅ Water usage is within reasonable range'; var r=`Daily: ${daily.toFixed(0)}L | Monthly: ${(daily*30/1000).toFixed(1)}m³ | ${tip}`; document.getElementById('rv').textContent=r; document.getElementById('result').style.display='block'; return;",
        'cn_steps': ['输入淋浴分钟数和冲厕次数', '输入洗衣次数和洗碗次数', '点击"计算"按钮查看水足迹'],
        'en_steps': ['Enter shower minutes and toilet flushes', 'Enter laundry and dishwashing counts', 'Click "Calculate" to see your water footprint'],
    },
}

import os

base = '/home/chison/tools-site'

for tool, cfg in tools_config.items():
    # Fix CN
    cn_path = os.path.join(base, tool, 'index.html')
    with open(cn_path, 'r') as f:
        cn_content = f.read()
    
    # Fix calc function
    cn_content = cn_content.replace(cfg['cn_calc'], cfg['cn_calc_fix'])
    
    # Fix placeholder steps (CN)
    steps_cn = cfg['cn_steps']
    cn_content = cn_content.replace('<li>输入第一个参数</li>', f'<li>{steps_cn[0]}</li>')
    cn_content = cn_content.replace('<li>输入第二个参数</li>', f'<li>{steps_cn[1]}</li>')
    cn_content = cn_content.replace('<li>点击"计算"按钮查看结果</li>', f'<li>{steps_cn[2]}</li>')
    
    with open(cn_path, 'w') as f:
        f.write(cn_content)
    print(f"{tool} CN: FIXED")
    
    # Fix EN
    en_path = os.path.join(base, 'en', tool, 'index.html')
    with open(en_path, 'r') as f:
        en_content = f.read()
    
    # Fix calc function
    en_content = en_content.replace(cfg['en_calc'], cfg['en_calc_fix'])
    
    # Fix placeholder steps (EN)
    steps_en = cfg['en_steps']
    en_content = en_content.replace('<li>Enter the first parameter</li>', f'<li>{steps_en[0]}</li>')
    en_content = en_content.replace('<li>Enter the second parameter</li>', f'<li>{steps_en[1]}</li>')
    en_content = en_content.replace('<li>Click "Calculate" to see the result</li>', f'<li>{steps_en[2]}</li>')
    # Also try without quotes
    en_content = en_content.replace('<li>Enter the first parameter</li>', f'<li>{steps_en[0]}</li>')
    en_content = en_content.replace('<li>Enter the second parameter</li>', f'<li>{steps_en[1]}</li>')
    
    # Fix footer (EN) - Chinese to English
    en_content = en_content.replace('>联系我们<', '>Contact Us<')
    en_content = en_content.replace('>隐私政策<', '>Privacy Policy<')
    en_content = en_content.replace('>服务条款<', '>Terms of Service<')
    en_content = en_content.replace('>关于我们<', '>About Us<')
    en_content = en_content.replace('>首页<', '>Home<')
    # Fix copyright text
    en_content = en_content.replace('所有计算在浏览器本地完成，数据不上传服务器', 'All calculations run locally in your browser, data never leaves your device')
    
    with open(en_path, 'w') as f:
        f.write(en_content)
    print(f"{tool} EN: FIXED")

print("\nDone! All 18 files fixed.")
