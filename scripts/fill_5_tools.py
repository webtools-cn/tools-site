#!/usr/bin/env python3
"""为5个工具填充实际的输入字段和计算逻辑"""
import os

SITE = '/home/chison/tools-site'

# 每个工具的输入HTML + 计算JS (CN + EN)
TOOL_DEFS = {
    'interest-rate-calculator': {
        'cn_inputs': '<div class="form-row"><div class="form-group"><label>输入类型</label><select id="rateType"><option value="annual">年利率 (%)</option><option value="monthly">月利率 (%)</option><option value="daily">日利率 (%)</option></select></div><div class="form-group"><label>利率值</label><input type="number" id="rateValue" placeholder="例如 5" step="any"></div></div><div class="form-group"><label>复利频率</label><select id="compoundFreq"><option value="1">每年</option><option value="2">每半年</option><option value="4">每季度</option><option value="12" selected>每月</option><option value="365">每日</option></select></div>',
        'en_inputs': '<div class="form-row"><div class="form-group"><label>Rate Type</label><select id="rateType"><option value="annual">Annual Rate (%)</option><option value="monthly">Monthly Rate (%)</option><option value="daily">Daily Rate (%)</option></select></div><div class="form-group"><label>Rate Value</label><input type="number" id="rateValue" placeholder="e.g. 5" step="any"></div></div><div class="form-group"><label>Compounding Frequency</label><select id="compoundFreq"><option value="1">Annually</option><option value="2">Semi-annually</option><option value="4">Quarterly</option><option value="12" selected>Monthly</option><option value="365">Daily</option></select></div>',
        'cn_js': '''function calculate(){
var r=parseFloat(document.getElementById('rateValue').value);
if(isNaN(r)){showToast('请输入有效利率值');return}
var type=document.getElementById('rateType').value;
var n=parseInt(document.getElementById('compoundFreq').value);
var annual, monthly, daily, ear;
if(type==='annual'){annual=r/100;monthly=Math.pow(1+annual,1/12)-1;daily=Math.pow(1+annual,1/365)-1}
else if(type==='monthly'){monthly=r/100;annual=Math.pow(1+monthly,12)-1;daily=Math.pow(1+monthly,1/30.4167)-1}
else{daily=r/100;annual=Math.pow(1+daily,365)-1;monthly=Math.pow(1+daily,30.4167)-1}
ear=Math.pow(1+annual/n,n)-1;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">年利率 (名义)</div><div class="value highlight">'+(annual*100).toFixed(4)+'%</div></div>'+
'<div class="result-item"><div class="label">月利率</div><div class="value">'+(monthly*100).toFixed(4)+'%</div></div>'+
'<div class="result-item"><div class="label">日利率</div><div class="value">'+(daily*100).toFixed(6)+'%</div></div>'+
'<div class="result-item"><div class="label">有效年利率 (EAR)</div><div class="value">'+(ear*100).toFixed(4)+'%</div></div>';
document.getElementById('results').style.display='block';
}''',
        'en_js': '''function calculate(){
var r=parseFloat(document.getElementById('rateValue').value);
if(isNaN(r)){showToast('Please enter a valid rate');return}
var type=document.getElementById('rateType').value;
var n=parseInt(document.getElementById('compoundFreq').value);
var annual, monthly, daily, ear;
if(type==='annual'){annual=r/100;monthly=Math.pow(1+annual,1/12)-1;daily=Math.pow(1+annual,1/365)-1}
else if(type==='monthly'){monthly=r/100;annual=Math.pow(1+monthly,12)-1;daily=Math.pow(1+monthly,1/30.4167)-1}
else{daily=r/100;annual=Math.pow(1+daily,365)-1;monthly=Math.pow(1+daily,30.4167)-1}
ear=Math.pow(1+annual/n,n)-1;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">Annual Rate (Nominal)</div><div class="value highlight">'+(annual*100).toFixed(4)+'%</div></div>'+
'<div class="result-item"><div class="label">Monthly Rate</div><div class="value">'+(monthly*100).toFixed(4)+'%</div></div>'+
'<div class="result-item"><div class="label">Daily Rate</div><div class="value">'+(daily*100).toFixed(6)+'%</div></div>'+
'<div class="result-item"><div class="label">Effective Annual Rate (EAR)</div><div class="value">'+(ear*100).toFixed(4)+'%</div></div>';
document.getElementById('results').style.display='block';
}''',
    },
    'dca-calculator': {
        'cn_inputs': '<div class="form-row"><div class="form-group"><label>初始投入 (元)</label><input type="number" id="initial" value="10000" step="any"></div><div class="form-group"><label>每次定投金额 (元)</label><input type="number" id="periodic" value="1000" step="any"></div></div><div class="form-row"><div class="form-group"><label>预期年化收益率 (%)</label><input type="number" id="rate" value="8" step="any"></div><div class="form-group"><label>定投频率</label><select id="frequency"><option value="12" selected>每月</option><option value="4">每季度</option><option value="52">每周</option><option value="1">每年</option></select></div></div><div class="form-row"><div class="form-group"><label>投资年限</label><input type="number" id="years" value="10" step="any"></div><div class="form-group"><label>对比：一次性投入 (元)</label><input type="number" id="lumpsum" value="0" step="any"></div></div>',
        'en_inputs': '<div class="form-row"><div class="form-group"><label>Initial Investment ($)</label><input type="number" id="initial" value="10000" step="any"></div><div class="form-group"><label>Periodic Contribution ($)</label><input type="number" id="periodic" value="1000" step="any"></div></div><div class="form-row"><div class="form-group"><label>Expected Annual Return (%)</label><input type="number" id="rate" value="8" step="any"></div><div class="form-group"><label>Contribution Frequency</label><select id="frequency"><option value="12" selected>Monthly</option><option value="4">Quarterly</option><option value="52">Weekly</option><option value="1">Annually</option></select></div></div><div class="form-row"><div class="form-group"><label>Investment Period (Years)</label><input type="number" id="years" value="10" step="any"></div><div class="form-group"><label>Compare: Lump Sum ($)</label><input type="number" id="lumpsum" value="0" step="any"></div></div>',
        'cn_js': '''function calculate(){
var init=parseFloat(document.getElementById('initial').value)||0;
var per=parseFloat(document.getElementById('periodic').value)||0;
var rate=parseFloat(document.getElementById('rate').value)/100||0;
var freq=parseInt(document.getElementById('frequency').value);
var yrs=parseFloat(document.getElementById('years').value)||0;
var ls=parseFloat(document.getElementById('lumpsum').value)||0;
if(yrs<=0){showToast('请输入有效投资年限');return}
var periods=yrs*freq;
var rPer=rate/freq;
// DCA total
var dcaTotal=init*Math.pow(1+rPer,periods);
if(rPer>0){dcaTotal+=per*((Math.pow(1+rPer,periods)-1)/rPer)*(1+rPer)}
else{dcaTotal+=per*periods}
var dcaInvested=init+per*periods;
// Lump sum
var lsTotal=ls>0?ls*Math.pow(1+rate,yrs):0;
var lsInvested=ls>0?ls:0;
// If no lump sum provided, calculate equivalent lump sum
var eqLs=ls>0?ls:(init+per*periods);
var eqLsTotal=eqLs*Math.pow(1+rate,yrs);
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">定投总投入</div><div class="value">¥'+dcaInvested.toLocaleString('zh-CN',{maximumFractionDigits:2})+'</div></div>'+
'<div class="result-item"><div class="label">定投最终价值</div><div class="value highlight">¥'+dcaTotal.toLocaleString('zh-CN',{maximumFractionDigits:2})+'</div></div>'+
'<div class="result-item"><div class="label">定投总收益</div><div class="value">¥'+(dcaTotal-dcaInvested).toLocaleString('zh-CN',{maximumFractionDigits:2})+' ('+((dcaTotal/dcaInvested-1)*100).toFixed(2)+'%)</div></div>'+
(ls>0?'<div class="result-item"><div class="label">一次性投入总投入</div><div class="value">¥'+lsInvested.toLocaleString('zh-CN',{maximumFractionDigits:2})+'</div></div>':'')+
(ls>0?'<div class="result-item"><div class="label">一次性投入最终价值</div><div class="value">¥'+lsTotal.toLocaleString('zh-CN',{maximumFractionDigits:2})+'</div></div>':'')+
(ls>0?'<div class="result-item"><div class="label">策略差异</div><div class="value highlight">¥'+(dcaTotal-lsTotal).toLocaleString('zh-CN',{maximumFractionDigits:2})+' ('+(dcaTotal>lsTotal?'定投胜出':'一次性胜出')+')</div></div>':'')+
'<div class="result-item"><div class="label">等额一次性投入最终价值</div><div class="value">¥'+eqLsTotal.toLocaleString('zh-CN',{maximumFractionDigits:2})+'</div></div>';
document.getElementById('results').style.display='block';
}''',
        'en_js': '''function calculate(){
var init=parseFloat(document.getElementById('initial').value)||0;
var per=parseFloat(document.getElementById('periodic').value)||0;
var rate=parseFloat(document.getElementById('rate').value)/100||0;
var freq=parseInt(document.getElementById('frequency').value);
var yrs=parseFloat(document.getElementById('years').value)||0;
var ls=parseFloat(document.getElementById('lumpsum').value)||0;
if(yrs<=0){showToast('Please enter a valid investment period');return}
var periods=yrs*freq;
var rPer=rate/freq;
var dcaTotal=init*Math.pow(1+rPer,periods);
if(rPer>0){dcaTotal+=per*((Math.pow(1+rPer,periods)-1)/rPer)*(1+rPer)}
else{dcaTotal+=per*periods}
var dcaInvested=init+per*periods;
var lsTotal=ls>0?ls*Math.pow(1+rate,yrs):0;
var lsInvested=ls>0?ls:0;
var eqLs=ls>0?ls:(init+per*periods);
var eqLsTotal=eqLs*Math.pow(1+rate,yrs);
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">Total Invested (DCA)</div><div class="value">$'+dcaInvested.toLocaleString('en-US',{maximumFractionDigits:2})+'</div></div>'+
'<div class="result-item"><div class="label">Final Value (DCA)</div><div class="value highlight">$'+dcaTotal.toLocaleString('en-US',{maximumFractionDigits:2})+'</div></div>'+
'<div class="result-item"><div class="label">Total Return (DCA)</div><div class="value">$'+(dcaTotal-dcaInvested).toLocaleString('en-US',{maximumFractionDigits:2})+' ('+((dcaTotal/dcaInvested-1)*100).toFixed(2)+'%)</div></div>'+
(ls>0?'<div class="result-item"><div class="label">Total Invested (Lump Sum)</div><div class="value">$'+lsInvested.toLocaleString('en-US',{maximumFractionDigits:2})+'</div></div>':'')+
(ls>0?'<div class="result-item"><div class="label">Final Value (Lump Sum)</div><div class="value">$'+lsTotal.toLocaleString('en-US',{maximumFractionDigits:2})+'</div></div>':'')+
(ls>0?'<div class="result-item"><div class="label">Strategy Difference</div><div class="value highlight">$'+(dcaTotal-lsTotal).toLocaleString('en-US',{maximumFractionDigits:2})+' ('+(dcaTotal>lsTotal?'DCA wins':'Lump Sum wins')+')</div></div>':'')+
'<div class="result-item"><div class="label">Equivalent Lump Sum Final Value</div><div class="value">$'+eqLsTotal.toLocaleString('en-US',{maximumFractionDigits:2})+'</div></div>';
document.getElementById('results').style.display='block';
}''',
    },
    'fuel-economy-calculator': {
        'cn_inputs': '<div class="form-row"><div class="form-group"><label>行驶距离</label><input type="number" id="distance" placeholder="例如 500" step="any"></div><div class="form-group"><label>距离单位</label><select id="distUnit"><option value="km">公里 (km)</option><option value="mi">英里 (mi)</option></select></div></div><div class="form-row"><div class="form-group"><label>油耗</label><input type="number" id="fuelUsed" placeholder="例如 40" step="any"></div><div class="form-group"><label>油耗单位</label><select id="fuelUnit"><option value="L">升 (L)</option><option value="gal">加仑 (gal)</option></select></div></div><div class="form-row"><div class="form-group"><label>油价 (元/升)</label><input type="number" id="fuelPrice" placeholder="例如 7.5" step="any" value="7.5"></div><div class="form-group"><label>年行驶里程 (公里)</label><input type="number" id="annualKm" placeholder="例如 15000" step="any" value="15000"></div></div>',
        'en_inputs': '<div class="form-row"><div class="form-group"><label>Distance</label><input type="number" id="distance" placeholder="e.g. 300" step="any"></div><div class="form-group"><label>Distance Unit</label><select id="distUnit"><option value="km">Kilometers (km)</option><option value="mi">Miles (mi)</option></select></div></div><div class="form-row"><div class="form-group"><label>Fuel Used</label><input type="number" id="fuelUsed" placeholder="e.g. 25" step="any"></div><div class="form-group"><label>Fuel Unit</label><select id="fuelUnit"><option value="L">Liters (L)</option><option value="gal">Gallons (gal)</option></select></div></div><div class="form-row"><div class="form-group"><label>Fuel Price ($/L)</label><input type="number" id="fuelPrice" placeholder="e.g. 1.0" step="any" value="1.0"></div><div class="form-group"><label>Annual Distance (km)</label><input type="number" id="annualKm" placeholder="e.g. 15000" step="any" value="15000"></div></div>',
        'cn_js': '''function calculate(){
var d=parseFloat(document.getElementById('distance').value);
var f=parseFloat(document.getElementById('fuelUsed').value);
var price=parseFloat(document.getElementById('fuelPrice').value)||0;
var annual=parseFloat(document.getElementById('annualKm').value)||0;
var du=document.getElementById('distUnit').value;
var fu=document.getElementById('fuelUnit').value;
if(!d||!f||d<=0||f<=0){showToast('请输入有效距离和油耗');return}
// Convert to metric
var km=du==='mi'?d*1.60934:d;
var liters=fu==='gal'?f*3.78541:f;
var l100km=(liters/km*100);
var mpg=235.215/l100km;
var costPerKm=price*liters/km;
var annualCost=annual>0?costPerKm*annual:0;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">百公里油耗</div><div class="value highlight">'+l100km.toFixed(2)+' L/100km</div></div>'+
'<div class="result-item"><div class="label">MPG (英里/加仑)</div><div class="value">'+mpg.toFixed(2)+' MPG</div></div>'+
'<div class="result-item"><div class="label">每公里油耗</div><div class="value">'+(liters/km).toFixed(4)+' 升</div></div>'+
'<div class="result-item"><div class="label">每公里油费</div><div class="value">¥'+costPerKm.toFixed(4)+'</div></div>'+
(annual>0?'<div class="result-item"><div class="label">年燃油成本 (预估)</div><div class="value highlight">¥'+annualCost.toFixed(2)+' ('+annual.toLocaleString()+'公里)</div></div>':'');
document.getElementById('results').style.display='block';
}''',
        'en_js': '''function calculate(){
var d=parseFloat(document.getElementById('distance').value);
var f=parseFloat(document.getElementById('fuelUsed').value);
var price=parseFloat(document.getElementById('fuelPrice').value)||0;
var annual=parseFloat(document.getElementById('annualKm').value)||0;
var du=document.getElementById('distUnit').value;
var fu=document.getElementById('fuelUnit').value;
if(!d||!f||d<=0||f<=0){showToast('Please enter valid distance and fuel');return}
var km=du==='mi'?d*1.60934:d;
var liters=fu==='gal'?f*3.78541:f;
var l100km=(liters/km*100);
var mpg=235.215/l100km;
var costPerKm=price*liters/km;
var annualCost=annual>0?costPerKm*annual:0;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">Fuel Consumption</div><div class="value highlight">'+l100km.toFixed(2)+' L/100km</div></div>'+
'<div class="result-item"><div class="label">MPG</div><div class="value">'+mpg.toFixed(2)+' MPG</div></div>'+
'<div class="result-item"><div class="label">Fuel per km</div><div class="value">'+(liters/km).toFixed(4)+' L</div></div>'+
'<div class="result-item"><div class="label">Cost per km</div><div class="value">$'+costPerKm.toFixed(4)+'</div></div>'+
(annual>0?'<div class="result-item"><div class="label">Annual Fuel Cost (Est.)</div><div class="value highlight">$'+annualCost.toFixed(2)+' ('+annual.toLocaleString()+' km)</div></div>':'');
document.getElementById('results').style.display='block';
}''',
    },
    'tdde-calculator': {
        'cn_inputs': '<div class="form-row"><div class="form-group"><label>性别</label><select id="gender"><option value="male">男</option><option value="female">女</option></select></div><div class="form-group"><label>年龄</label><input type="number" id="age" value="30" step="any" min="15" max="100"></div></div><div class="form-row"><div class="form-group"><label>身高 (cm)</label><input type="number" id="height" value="170" step="any"></div><div class="form-group"><label>体重 (kg)</label><input type="number" id="weight" value="70" step="any"></div></div><div class="form-group"><label>活动水平</label><select id="activity"><option value="1.2">久坐（几乎不运动）</option><option value="1.375" selected>轻度活动（1-3天/周）</option><option value="1.55">中度活动（3-5天/周）</option><option value="1.725">高度活跃（6-7天/周）</option><option value="1.9">极度活跃（运动员）</option></select></div>',
        'en_inputs': '<div class="form-row"><div class="form-group"><label>Gender</label><select id="gender"><option value="male">Male</option><option value="female">Female</option></select></div><div class="form-group"><label>Age</label><input type="number" id="age" value="30" step="any" min="15" max="100"></div></div><div class="form-row"><div class="form-group"><label>Height (cm)</label><input type="number" id="height" value="170" step="any"></div><div class="form-group"><label>Weight (kg)</label><input type="number" id="weight" value="70" step="any"></div></div><div class="form-group"><label>Activity Level</label><select id="activity"><option value="1.2">Sedentary (little/no exercise)</option><option value="1.375" selected>Light (1-3 days/week)</option><option value="1.55">Moderate (3-5 days/week)</option><option value="1.725">Very Active (6-7 days/week)</option><option value="1.9">Extra Active (athlete)</option></select></div>',
        'cn_js': '''function calculate(){
var gender=document.getElementById('gender').value;
var age=parseFloat(document.getElementById('age').value);
var h=parseFloat(document.getElementById('height').value);
var w=parseFloat(document.getElementById('weight').value);
var act=parseFloat(document.getElementById('activity').value);
if(!age||!h||!w){showToast('请填写所有字段');return}
var bmr;
if(gender==='male'){bmr=10*w+6.25*h-5*age+5}
else{bmr=10*w+6.25*h-5*age-161}
var tdee=bmr*act;
var lose05=tdee-500;
var lose025=tdee-250;
var gain05=tdee+500;
var gain025=tdee+250;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">基础代谢 (BMR)</div><div class="value">'+Math.round(bmr)+' 大卡/天</div></div>'+
'<div class="result-item"><div class="label">每日总消耗 (TDEE)</div><div class="value highlight">'+Math.round(tdee)+' 大卡/天</div></div>'+
'<div class="result-item"><div class="label">减重 (~0.5kg/周)</div><div class="value">'+Math.round(lose05)+' 大卡/天</div></div>'+
'<div class="result-item"><div class="label">温和减重 (~0.25kg/周)</div><div class="value">'+Math.round(lose025)+' 大卡/天</div></div>'+
'<div class="result-item"><div class="label">增重 (~0.5kg/周)</div><div class="value">'+Math.round(gain05)+' 大卡/天</div></div>'+
'<div class="result-item"><div class="label">温和增重 (~0.25kg/周)</div><div class="value">'+Math.round(gain025)+' 大卡/天</div></div>';
document.getElementById('results').style.display='block';
}''',
        'en_js': '''function calculate(){
var gender=document.getElementById('gender').value;
var age=parseFloat(document.getElementById('age').value);
var h=parseFloat(document.getElementById('height').value);
var w=parseFloat(document.getElementById('weight').value);
var act=parseFloat(document.getElementById('activity').value);
if(!age||!h||!w){showToast('Please fill in all fields');return}
var bmr;
if(gender==='male'){bmr=10*w+6.25*h-5*age+5}
else{bmr=10*w+6.25*h-5*age-161}
var tdee=bmr*act;
var lose05=tdee-500;
var lose025=tdee-250;
var gain05=tdee+500;
var gain025=tdee+250;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">BMR (Basal Metabolic Rate)</div><div class="value">'+Math.round(bmr)+' kcal/day</div></div>'+
'<div class="result-item"><div class="label">TDEE (Total Daily Energy Expenditure)</div><div class="value highlight">'+Math.round(tdee)+' kcal/day</div></div>'+
'<div class="result-item"><div class="label">Weight Loss (~0.5 kg/week)</div><div class="value">'+Math.round(lose05)+' kcal/day</div></div>'+
'<div class="result-item"><div class="label">Mild Weight Loss (~0.25 kg/week)</div><div class="value">'+Math.round(lose025)+' kcal/day</div></div>'+
'<div class="result-item"><div class="label">Weight Gain (~0.5 kg/week)</div><div class="value">'+Math.round(gain05)+' kcal/day</div></div>'+
'<div class="result-item"><div class="label">Mild Weight Gain (~0.25 kg/week)</div><div class="value">'+Math.round(gain025)+' kcal/day</div></div>';
document.getElementById('results').style.display='block';
}''',
    },
    'rental-property-calculator': {
        'cn_inputs': '<div class="form-row"><div class="form-group"><label>房产总价 (万元)</label><input type="number" id="price" placeholder="例如 200" step="any"></div><div class="form-group"><label>首付比例 (%)</label><input type="number" id="downPct" value="30" step="any"></div></div><div class="form-row"><div class="form-group"><label>月租金 (元)</label><input type="number" id="monthlyRent" placeholder="例如 5000" step="any"></div><div class="form-group"><label>房贷利率 (%)</label><input type="number" id="mortgageRate" value="4.2" step="any"></div></div><div class="form-row"><div class="form-group"><label>贷款年限</label><input type="number" id="loanYears" value="30" step="any"></div><div class="form-group"><label>月物业费 (元)</label><input type="number" id="hoa" value="200" step="any"></div></div><div class="form-row"><div class="form-group"><label>年维修费 (元)</label><input type="number" id="maintenance" value="0" step="any"></div><div class="form-group"><label>空置率 (%)</label><input type="number" id="vacancy" value="5" step="any"></div></div>',
        'en_inputs': '<div class="form-row"><div class="form-group"><label>Property Price ($)</label><input type="number" id="price" placeholder="e.g. 300000" step="any"></div><div class="form-group"><label>Down Payment (%)</label><input type="number" id="downPct" value="20" step="any"></div></div><div class="form-row"><div class="form-group"><label>Monthly Rent ($)</label><input type="number" id="monthlyRent" placeholder="e.g. 2000" step="any"></div><div class="form-group"><label>Mortgage Rate (%)</label><input type="number" id="mortgageRate" value="6.5" step="any"></div></div><div class="form-row"><div class="form-group"><label>Loan Term (Years)</label><input type="number" id="loanYears" value="30" step="any"></div><div class="form-group"><label>Monthly HOA ($)</label><input type="number" id="hoa" value="100" step="any"></div></div><div class="form-row"><div class="form-group"><label>Annual Maintenance ($)</label><input type="number" id="maintenance" value="0" step="any"></div><div class="form-group"><label>Vacancy Rate (%)</label><input type="number" id="vacancy" value="5" step="any"></div></div>',
        'cn_js': '''function calculate(){
var price=parseFloat(document.getElementById('price').value)*10000;
var downPct=parseFloat(document.getElementById('downPct').value)/100;
var rent=parseFloat(document.getElementById('monthlyRent').value);
var mr=parseFloat(document.getElementById('mortgageRate').value)/100/12;
var yrs=parseFloat(document.getElementById('loanYears').value);
var hoa=parseFloat(document.getElementById('hoa').value)||0;
var maint=parseFloat(document.getElementById('maintenance').value)||0;
var vacancy=parseFloat(document.getElementById('vacancy').value)/100||0;
if(!price||!rent||price<=0||rent<=0){showToast('请填写房产总价和月租金');return}
var down=price*downPct;
var loan=price-down;
var n=yrs*12;
var monthlyPayment=0;
if(mr>0){monthlyPayment=loan*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1)}
else{monthlyPayment=loan/n}
var annualRent=rent*12*(1-vacancy);
var annualCost=monthlyPayment*12+hoa*12+maint;
var annualCashFlow=annualRent-annualCost;
var monthlyCashFlow=annualCashFlow/12;
var rentalYield=annualRent/price*100;
var cashOnCash=annualCashFlow/down*100;
var totalROI=(annualCashFlow+(price*0.03))/down*100
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">首付金额</div><div class="value">¥'+down.toLocaleString('zh-CN',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">月供</div><div class="value">¥'+monthlyPayment.toLocaleString('zh-CN',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">年租金收入 (扣除空置)</div><div class="value">¥'+annualRent.toLocaleString('zh-CN',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">年总支出</div><div class="value">¥'+annualCost.toLocaleString('zh-CN',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">月现金流</div><div class="value highlight">¥'+monthlyCashFlow.toLocaleString('zh-CN',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">租金收益率</div><div class="value">'+rentalYield.toFixed(2)+'%</div></div>'+
'<div class="result-item"><div class="label">现金回报率</div><div class="value highlight">'+cashOnCash.toFixed(2)+'%</div></div>';
document.getElementById('results').style.display='block';
}''',
        'en_js': '''function calculate(){
var price=parseFloat(document.getElementById('price').value);
var downPct=parseFloat(document.getElementById('downPct').value)/100;
var rent=parseFloat(document.getElementById('monthlyRent').value);
var mr=parseFloat(document.getElementById('mortgageRate').value)/100/12;
var yrs=parseFloat(document.getElementById('loanYears').value);
var hoa=parseFloat(document.getElementById('hoa').value)||0;
var maint=parseFloat(document.getElementById('maintenance').value)||0;
var vacancy=parseFloat(document.getElementById('vacancy').value)/100||0;
if(!price||!rent||price<=0||rent<=0){showToast('Please fill in property price and monthly rent');return}
var down=price*downPct;
var loan=price-down;
var n=yrs*12;
var monthlyPayment=0;
if(mr>0){monthlyPayment=loan*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1)}
else{monthlyPayment=loan/n}
var annualRent=rent*12*(1-vacancy);
var annualCost=monthlyPayment*12+hoa*12+maint;
var annualCashFlow=annualRent-annualCost;
var monthlyCashFlow=annualCashFlow/12;
var rentalYield=annualRent/price*100;
var cashOnCash=annualCashFlow/down*100;
document.getElementById('resultGrid').innerHTML=
'<div class="result-item"><div class="label">Down Payment</div><div class="value">$'+down.toLocaleString('en-US',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">Monthly Mortgage</div><div class="value">$'+monthlyPayment.toLocaleString('en-US',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">Annual Rent (after vacancy)</div><div class="value">$'+annualRent.toLocaleString('en-US',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">Annual Expenses</div><div class="value">$'+annualCost.toLocaleString('en-US',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">Monthly Cash Flow</div><div class="value highlight">$'+monthlyCashFlow.toLocaleString('en-US',{maximumFractionDigits:0})+'</div></div>'+
'<div class="result-item"><div class="label">Rental Yield</div><div class="value">'+rentalYield.toFixed(2)+'%</div></div>'+
'<div class="result-item"><div class="label">Cash-on-Cash Return</div><div class="value highlight">'+cashOnCash.toFixed(2)+'%</div></div>';
document.getElementById('results').style.display='block';
}''',
    },
}

def fill_tool(slug, defn):
    for lang, lang_dir in [('cn', os.path.join(SITE, slug)), ('en', os.path.join(SITE, 'en', slug))]:
        path = os.path.join(lang_dir, 'index.html')
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 替换空的inputs
        html = html.replace('<div id="inputs"></div>', '<div id="inputs">' + defn[f'{lang}_inputs'] + '</div>')
        
        # 替换脚本中的calculate占位（脚本里没有calculate函数，需要插入在clearAll后面）
        js_code = defn[f'{lang}_js']
        # 在clearAll函数的}后面插入
        html = html.replace(
            "function clearAll(){",
            js_code + "\nfunction clearAll(){"
        )
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {slug}/{lang}: filled")

if __name__ == '__main__':
    for slug, defn in TOOL_DEFS.items():
        fill_tool(slug, defn)
    print("\nDone!")