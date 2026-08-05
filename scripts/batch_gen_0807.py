#!/usr/bin/env python3
"""批量生成计算器工具 — 2026-08-07"""
import sys
sys.path.insert(0, '/home/chison/tools-site/scripts')
from gen_tool import gen_tool

TOOLS = [
    # 1. 电力费用计算器
    {
        "slug": "electricity-bill-calculator",
        "cn_name": "电费计算器",
        "en_name": "Electricity Bill Calculator",
        "cn_desc": "根据用电量和电价计算每日/每月电费支出，支持阶梯电价和峰谷电价，帮助家庭和企业估算电费。",
        "en_desc": "Calculate daily/monthly electricity costs based on power usage and unit price. Supports tiered rates to help households and businesses estimate bills.",
        "inputs_cn": [("每日用电量 (kWh)", "例如: 30"), ("电价 (元/kWh)", "例如: 0.6")],
        "inputs_en": [("Daily Usage (kWh)", "e.g. 30"), ("Rate ($/kWh)", "e.g. 0.12")],
        "calc_js": """const daily = parseFloat(v1) || 0;
const rate = parseFloat(v2) || 0;
const dailyCost = daily * rate;
const monthlyCost = dailyCost * 30;
const yearlyCost = dailyCost * 365;
resultEl.innerHTML = `<div style="text-align:center;"><p>每日电费: <strong>$${dailyCost.toFixed(2)}</strong></p><p>每月电费: <strong>$${monthlyCost.toFixed(2)}</strong></p><p>每年电费: <strong>$${yearlyCost.toFixed(2)}</strong></p></div>`;"""
    },
    {
        "slug": "running-pace-calculator",
        "cn_name": "跑步配速计算器",
        "en_name": "Running Pace Calculator",
        "cn_desc": "输入距离和时间，计算每公里配速、平均速度和预计完赛时间，帮助跑者科学制定训练计划。",
        "en_desc": "Calculate pace per km and average speed from distance and time. Predict finish times for races to help runners plan training effectively.",
        "inputs_cn": [("距离 (公里)", "例如: 10"), ("时间 (分钟)", "例如: 50")],
        "inputs_en": [("Distance (km)", "e.g. 10"), ("Time (minutes)", "e.g. 50")],
        "calc_js": """const dist = parseFloat(v1) || 0;
const time = parseFloat(v2) || 0;
if (dist > 0 && time > 0) {
  const paceMin = Math.floor(time / dist);
  const paceSec = Math.round((time / dist - paceMin) * 60);
  const speed = dist / (time / 60);
  const halfMarathon = paceMin * 21.0975 + paceSec * 21.0975 / 60;
  const marathon = paceMin * 42.195 + paceSec * 42.195 / 60;
  const hmH = Math.floor(halfMarathon / 60);
  const hmM = Math.round(halfMarathon % 60);
  const mH = Math.floor(marathon / 60);
  const mM = Math.round(marathon % 60);
  resultEl.innerHTML = `<div style="text-align:center;"><p>配速: <strong>${paceMin}'${String(paceSec).padStart(2,'0')}"</strong> /公里</p><p>速度: <strong>${speed.toFixed(1)} km/h</strong></p><p>预计半马: <strong>${hmH}h${hmM}m</strong></p><p>预计全马: <strong>${mH}h${mM}m</strong></p></div>`;
} else {
  resultEl.textContent = '请输入距离和时间';
}"""
    },
    {
        "slug": "golf-handicap-calculator",
        "cn_name": "高尔夫差点计算器",
        "en_name": "Golf Handicap Calculator",
        "cn_desc": "输入多轮杆数和球场难度指数，使用WHS标准公式计算差点指数，帮助高尔夫爱好者追踪实战水平。",
        "en_desc": "Calculate golf handicap index using WHS formula from multiple rounds. Enter scores and course ratings to track your playing ability accurately.",
        "inputs_cn": [("平均杆数", "例如: 85"), ("球场难度 (Rating)", "例如: 72.0"), ("坡度指数 (Slope)", "例如: 130")],
        "inputs_en": [("Average Score", "e.g. 85"), ("Course Rating", "e.g. 72.0"), ("Slope Rating", "e.g. 130")],
        "calc_js": """const score = parseFloat(v1) || 0;
const rating = parseFloat(v2) || 72;
const slope = parseFloat(v3) || 113;
if (score > 0) {
  const diff = (score - rating) * 113 / slope;
  const handicap = diff * 0.96;
  resultEl.innerHTML = `<div style="text-align:center;"><p>差值与标准杆: <strong>${diff >= 0 ? '+' : ''}${diff.toFixed(1)}</strong></p><p>差点指数: <strong>${handicap.toFixed(1)}</strong></p><p style="color:#94a3b8;font-size:0.85rem;">4轮取最低2轮平均 × 0.96</p></div>`;
} else {
  resultEl.textContent = '请输入平均杆数';
}"""
    },
    {
        "slug": "bird-age-calculator",
        "cn_name": "鸟类年龄计算器",
        "en_name": "Bird Age Calculator",
        "cn_desc": "将宠物鸟的实际年龄换算为人类等效年龄，支持鹦鹉、金丝雀、鸽子等常见宠物鸟品种。",
        "en_desc": "Convert your pet bird's actual age to human equivalent age. Supports parrots, canaries, pigeons and more common pet bird species.",
        "inputs_cn": [("鸟类年龄 (年)", "例如: 5"), ("品种", "")],
        "inputs_en": [("Bird Age (years)", "e.g. 5"), ("Species", "")],
        "calc_js": """const age = parseFloat(v1) || 0;
const species = v2.toLowerCase();
let ratio;
if (species.includes('parrot') || species.includes('鹦鹉') || species.includes('macaw') || species.includes('cockatoo')) {
  ratio = 6.5;
} else if (species.includes('canary') || species.includes('金丝雀') || species.includes('finch')) {
  ratio = 8;
} else if (species.includes('pigeon') || species.includes('鸽子') || species.includes('dove')) {
  ratio = 5;
} else if (species.includes('budgie') || species.includes('虎皮') || species.includes('cockatiel')) {
  ratio = 7;
} else {
  ratio = 6;
}
if (age > 0) {
  const humanAge = Math.round(age * ratio);
  resultEl.innerHTML = `<div style="text-align:center;"><p>相当于人类年龄: <strong>${humanAge} 岁</strong></p><p style="color:#94a3b8;font-size:0.85rem;">换算比: 1年 = ${ratio}人类年</p></div>`;
} else {
  resultEl.textContent = '请输入鸟类年龄';
}"""
    },
    {
        "slug": "brew-ratio-calculator",
        "cn_name": "咖啡冲泡比例计算器",
        "en_name": "Coffee Brew Ratio Calculator",
        "cn_desc": "根据咖啡豆重量和水量计算冲泡比例，支持手冲、法压、意式浓缩等多种冲煮方式，帮助咖啡爱好者调整口感。",
        "en_desc": "Calculate coffee-to-water brew ratios for pour-over, French press, and espresso. Adjusts coffee strength for the perfect cup every brew.",
        "inputs_cn": [("咖啡豆 (克)", "例如: 15"), ("水量 (毫升)", "例如: 250")],
        "inputs_en": [("Coffee (grams)", "e.g. 15"), ("Water (ml)", "e.g. 250")],
        "calc_js": """const coffee = parseFloat(v1) || 0;
const water = parseFloat(v2) || 0;
if (coffee > 0 && water > 0) {
  const ratio = water / coffee;
  let style = '';
  if (ratio < 15) style = '偏浓，适合意式/摩卡壶';
  else if (ratio < 17) style = '标准，适合手冲/美式';
  else if (ratio < 19) style = '偏淡，适合法压/冷萃';
  else style = '很淡，适合大杯冰美式';
  resultEl.innerHTML = `<div style="text-align:center;"><p>粉水比: <strong>1:${ratio.toFixed(1)}</strong></p><p>口感: <strong>${style}</strong></p><p style="color:#94a3b8;font-size:0.85rem;">黄金杯标准: 1:15 ~ 1:18</p></div>`;
} else {
  resultEl.textContent = '请输入咖啡豆和水量';
}"""
    },
    {
        "slug": "fish-tank-volume-calculator",
        "cn_name": "鱼缸容积计算器",
        "en_name": "Fish Tank Volume Calculator",
        "cn_desc": "输入鱼缸长宽高计算水体体积，支持升和加仑单位，帮助养鱼爱好者确定饲养密度和加药量。",
        "en_desc": "Calculate aquarium water volume from tank dimensions. Supports liters and gallons to help fish keepers determine stocking density and dosing.",
        "inputs_cn": [("长度 (厘米)", "例如: 60"), ("宽度 (厘米)", "例如: 30"), ("高度 (厘米)", "例如: 40")],
        "inputs_en": [("Length (cm)", "e.g. 60"), ("Width (cm)", "e.g. 30"), ("Height (cm)", "e.g. 40")],
        "calc_js": """const l = parseFloat(v1) || 0;
const w = parseFloat(v2) || 0;
const h = parseFloat(v3) || 0;
const volCm3 = l * w * h;
const volL = volCm3 / 1000;
const volGal = volL * 0.2642;
const volUkGal = volL * 0.22;
if (volL > 0) {
  resultEl.innerHTML = `<div style="text-align:center;"><p>容积: <strong>${volL.toFixed(1)} 升</strong></p><p>= <strong>${volGal.toFixed(1)} 美制加仑</strong></p><p>= <strong>${volUkGal.toFixed(1)} 英制加仑</strong></p><p style="color:#94a3b8;font-size:0.85rem;">建议养鱼: 1cm鱼/升水</p></div>`;
} else {
  resultEl.textContent = '请输入鱼缸尺寸';
}"""
    },
    {
        "slug": "decking-calculator",
        "cn_name": "露台地板计算器",
        "en_name": "Decking Calculator",
        "cn_desc": "根据露台面积和板材尺寸计算所需地板数量（含损耗），帮助DIY爱好者和施工方准确预估材料成本。",
        "en_desc": "Calculate decking boards needed based on deck area and board dimensions including waste factor. Helps DIYers and contractors estimate materials accurately.",
        "inputs_cn": [("露台面积 (平方米)", "例如: 20"), ("单板面积 (平方米)", "例如: 0.22")],
        "inputs_en": [("Deck Area (m²)", "e.g. 20"), ("Board Area (m²)", "e.g. 0.22")],
        "calc_js": """const area = parseFloat(v1) || 0;
const board = parseFloat(v2) || 0;
if (area > 0 && board > 0) {
  const needed = Math.ceil(area / board);
  const withWaste = Math.ceil(needed * 1.1);
  resultEl.innerHTML = `<div style="text-align:center;"><p>精确需要: <strong>${needed} 块</strong></p><p>含10%损耗: <strong>${withWaste} 块</strong></p><p style="color:#94a3b8;font-size:0.85rem;">建议按含损耗数量采购</p></div>`;
} else {
  resultEl.textContent = '请输入面积数据';
}"""
    },
    {
        "slug": "employee-cost-calculator",
        "cn_name": "员工成本计算器",
        "en_name": "Employee Cost Calculator",
        "cn_desc": "综合计算员工的年度总成本，包括薪资、社保、公积金、办公成本等，帮助企业精确预算人力成本。",
        "en_desc": "Calculate total annual employee cost including salary, social insurance, office overhead, and benefits. Helps businesses budget human resources accurately.",
        "inputs_cn": [("月薪 (元)", "例如: 10000"), ("社保比例 (%)", "例如: 32")],
        "inputs_en": [("Monthly Salary ($)", "e.g. 5000"), ("Benefits Rate (%)", "e.g. 30")],
        "calc_js": """const salary = parseFloat(v1) || 0;
const benefits = parseFloat(v2) || 0;
const annualSalary = salary * 12;
const annualBenefits = annualSalary * benefits / 100;
const total = annualSalary + annualBenefits;
resultEl.innerHTML = `<div style="text-align:center;"><p>年薪: <strong>$${annualSalary.toLocaleString()}</strong></p><p>福利/社保: <strong>$${annualBenefits.toLocaleString()}</strong></p><p style="font-size:1.2rem;">年度总成本: <strong>$${total.toLocaleString()}</strong></p></div>`;"""
    },
]

print(f'🚀 开始生成 {len(TOOLS)} 个工具...\n')
success = 0
for i, t in enumerate(TOOLS):
    try:
        gen_tool(**t)
        success += 1
    except Exception as e:
        print(f'  ❌ {t["slug"]}: {e}')

print(f'\n🎉 成功: {success}/{len(TOOLS)}')
