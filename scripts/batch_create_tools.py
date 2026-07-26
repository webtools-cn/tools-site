#!/usr/bin/env python3
"""批量创建5个新工具: body-shape-calculator, muscle-recovery-calculator, stretching-timer, grip-strength-calculator, sleep-quality-assessor"""
import os, json

BASE = "/home/chison/tools-site"

TOOLS = [
    {
        "slug": "body-shape-calculator",
        "name_zh": "体型计算器",
        "name_en": "Body Shape Calculator",
        "desc_zh": "免费在线体型计算器，通过肩围、腰围、臀围等数据判断您的体型类型（倒三角、矩形、苹果型、梨型、沙漏型），并提供穿搭建议。纯前端本地计算，数据不上传。",
        "desc_en": "Free online body shape calculator — determine your body type (inverted triangle, rectangle, apple, pear, hourglass) using shoulder, waist, and hip measurements. Get personalized styling tips. 100% client-side, no data uploaded.",
        "icon": "📐",
        "category": "health",
        "inputs": [
            {"id": "gender", "label_zh": "性别", "label_en": "Gender", "type": "select", "options": [["male","男性"],["female","女性"]]},
            {"id": "shoulder", "label_zh": "肩围 (cm)", "label_en": "Shoulder (cm)", "type": "number", "min": 60, "max": 180, "step": 0.1},
            {"id": "bust", "label_zh": "胸围 (cm)", "label_en": "Bust (cm)", "type": "number", "min": 50, "max": 180, "step": 0.1},
            {"id": "waist", "label_zh": "腰围 (cm)", "label_en": "Waist (cm)", "type": "number", "min": 40, "max": 160, "step": 0.1},
            {"id": "hip", "label_zh": "臀围 (cm)", "label_en": "Hip (cm)", "type": "number", "min": 50, "max": 180, "step": 0.1}
        ],
        "faq_zh": [
            {"q":"什么是体型分类？","a":"体型分类是根据身体各部位围度比例来划分的，主要类型包括：倒三角（肩宽臀窄）、矩形（肩腰臀接近）、苹果型（腰围较大）、梨型（臀宽肩窄）、沙漏型（肩臀接近且腰细）。"},
            {"q":"如何准确测量身体围度？","a":"测量肩围时皮尺绕过肩膀最宽处；胸围在胸部最丰满处水平测量；腰围在肚脐上方最细处；臀围在臀部最宽处。保持皮尺水平且不过紧。"},
            {"q":"体型会影响穿搭吗？","a":"是的。了解自己的体型可以帮助选择更适合的服装款式。例如倒三角体型适合V领和A字裙，梨型适合强调上身的款式，沙漏型适合收腰设计。"}
        ],
        "faq_en": [
            {"q":"What are the body shape types?","a":"The main body shape types are: Inverted Triangle (broad shoulders, narrow hips), Rectangle (similar shoulder/waist/hip), Apple (larger waist), Pear (wider hips, narrower shoulders), and Hourglass (balanced shoulders/hips with defined waist)."},
            {"q":"How to measure body circumferences accurately?","a":"Measure shoulder at the widest point, bust at the fullest part, waist at the narrowest point above the navel, and hips at the widest point. Keep the tape level and not too tight."},
            {"q":"Does body shape affect clothing choices?","a":"Yes! Knowing your body shape helps choose flattering styles. Inverted triangles suit V-necks and A-line skirts, pears benefit from emphasizing the upper body, and hourglass shapes look great in waist-defining designs."}
        ],
        "calculate_js": """
const g = document.getElementById('gender').value;
const s = parseFloat(document.getElementById('shoulder').value);
const b = parseFloat(document.getElementById('bust').value);
const w = parseFloat(document.getElementById('waist').value);
const h = parseFloat(document.getElementById('hip').value);
if (!s || !b || !w || !h) { showToast('请填写所有字段'); return; }

let type_zh, type_en, desc_zh, desc_en;
const swr = s / h; // shoulder-to-hip ratio
const whr = w / h; // waist-to-hip ratio

if (swr > 1.05 && whr < 0.85) {
  type_zh = '倒三角型'; type_en = 'Inverted Triangle';
  desc_zh = '肩部较宽，臀部较窄。建议选择V领、A字裙来平衡上下身比例。';
  desc_en = 'Broad shoulders, narrower hips. V-necks and A-line skirts help balance proportions.';
} else if (swr > 1.05 && whr >= 0.85) {
  type_zh = '矩形'; type_en = 'Rectangle';
  desc_zh = '肩、腰、臀比例接近。建议用腰带和层次感穿搭来创造曲线。';
  desc_en = 'Similar shoulder, waist, and hip measurements. Use belts and layers to create curves.';
} else if (swr <= 1.05 && whr >= 0.9) {
  type_zh = '苹果型'; type_en = 'Apple';
  desc_zh = '腰围相对较大。建议选择帝国腰线和V领设计来拉长身形。';
  desc_en = 'Relatively larger waist. Empire waistlines and V-necks help elongate the silhouette.';
} else if (swr <= 0.95 && whr < 0.8) {
  type_zh = '梨型'; type_en = 'Pear';
  desc_zh = '臀部较宽，肩部较窄。建议强调上身，选择亮色上衣和深色下装。';
  desc_en = 'Wider hips, narrower shoulders. Emphasize upper body with bright tops and dark bottoms.';
} else {
  type_zh = '沙漏型'; type_en = 'Hourglass';
  desc_zh = '肩臀比例接近，腰部纤细。适合收腰设计，突出曲线美。';
  desc_en = 'Balanced shoulders and hips with defined waist. Waist-defining styles highlight your natural curves.';
}

document.getElementById('resType').textContent = type_zh;
document.getElementById('resDesc').textContent = desc_zh;
document.getElementById('resRatio').textContent = '肩臀比: ' + swr.toFixed(2) + ' | 腰臀比: ' + whr.toFixed(2);
document.getElementById('resultSection').style.display = 'block';
"""
    },
    {
        "slug": "muscle-recovery-calculator",
        "name_zh": "肌肉恢复时间计算器",
        "name_en": "Muscle Recovery Calculator",
        "desc_zh": "免费在线肌肉恢复时间计算器，根据训练强度、年龄和睡眠质量估算肌肉群恢复所需时间。帮助科学安排训练计划，避免过度训练。纯前端计算。",
        "desc_en": "Free online muscle recovery time calculator — estimate recovery time for muscle groups based on workout intensity, age, and sleep quality. Plan your training scientifically and avoid overtraining. 100% client-side.",
        "icon": "💪",
        "category": "health",
        "inputs": [
            {"id": "age", "label_zh": "年龄", "label_en": "Age", "type": "number", "min": 14, "max": 80, "step": 1},
            {"id": "intensity", "label_zh": "训练强度", "label_en": "Intensity", "type": "select", "options": [["light","轻度 (Light)"],["moderate","中度 (Moderate)"],["heavy","重度 (Heavy)"],["max","极限 (Max)"]]},
            {"id": "sleep", "label_zh": "睡眠质量", "label_en": "Sleep Quality", "type": "select", "options": [["poor","差 (<6h)"],["fair","一般 (6-7h)"],["good","良好 (7-8h)"],["excellent","优秀 (>8h)"]]},
            {"id": "experience", "label_zh": "训练经验", "label_en": "Experience", "type": "select", "options": [["beginner","初学者"],["intermediate","中级"],["advanced","高级"]]}
        ],
        "faq_zh": [
            {"q":"肌肉需要多长时间恢复？","a":"恢复时间取决于多个因素。轻度训练通常需要24小时，中度训练48小时，高强度训练可能需要72小时以上。年龄、睡眠和营养都会影响恢复速度。"},
            {"q":"如何判断肌肉是否完全恢复？","a":"主要指标包括：肌肉酸痛消失、力量恢复到正常水平、关节活动度正常。如果连续训练后表现下降，说明需要更多恢复时间。"},
            {"q":"可以每天训练同一肌群吗？","a":"不建议。同一肌群至少需要48小时恢复。建议采用分化训练（如推/拉/腿），让不同肌群轮流休息。"}
        ],
        "faq_en": [
            {"q":"How long do muscles need to recover?","a":"Recovery time varies. Light workouts need ~24h, moderate ~48h, and intense sessions may need 72h+. Age, sleep, and nutrition all affect recovery speed."},
            {"q":"How to know if muscles are fully recovered?","a":"Key indicators: soreness gone, strength back to normal, full range of motion. If performance declines across sessions, you need more recovery."},
            {"q":"Can I train the same muscle group daily?","a":"Not recommended. Same muscle groups need at least 48h recovery. Use split routines (push/pull/legs) to rotate muscle groups."}
        ],
        "calculate_js": """
const age = parseInt(document.getElementById('age').value);
const intensity = document.getElementById('intensity').value;
const sleep = document.getElementById('sleep').value;
const exp = document.getElementById('experience').value;

let baseHours = {light: 24, moderate: 48, heavy: 72, max: 96}[intensity];
const ageMod = age > 40 ? 1.3 : age > 30 ? 1.15 : 1.0;
const sleepMod = {poor: 1.4, fair: 1.2, good: 1.0, excellent: 0.85}[sleep];
const expMod = {beginner: 1.2, intermediate: 1.0, advanced: 0.85}[exp];

const totalHours = Math.round(baseHours * ageMod * sleepMod * expMod);
const days = Math.ceil(totalHours / 24);
const nextTrain = new Date();
nextTrain.setHours(nextTrain.getHours() + totalHours);

const advice = totalHours <= 24 ? '轻度训练，明天可继续' : 
               totalHours <= 48 ? '建议休息1-2天' :
               totalHours <= 72 ? '建议休息2-3天，可训练其他肌群' : '高强度训练，充分休息3-4天';

document.getElementById('resHours').textContent = totalHours + ' 小时';
document.getElementById('resDays').textContent = days + ' 天';
document.getElementById('resAdvice').textContent = advice;
document.getElementById('resNext').textContent = '建议下次训练: ' + nextTrain.toLocaleString('zh-CN', {month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'});
document.getElementById('resultSection').style.display = 'block';
"""
    },
    {
        "slug": "stretching-timer",
        "name_zh": "拉伸计时器",
        "name_en": "Stretching Timer",
        "desc_zh": "免费在线拉伸计时器，预设全身拉伸动作及时长，语音提示切换动作。包含颈部、肩部、背部、腿部等10+拉伸动作，适合运动前后使用。纯前端，无需安装。",
        "desc_en": "Free online stretching timer with preset full-body stretches and voice prompts. Includes 10+ stretches for neck, shoulders, back, legs. Perfect for pre/post workout. Pure frontend, no installation needed.",
        "icon": "🧘",
        "category": "health",
        "inputs": [
            {"id": "routine", "label_zh": "拉伸方案", "label_en": "Routine", "type": "select", "options": [["full","全身拉伸 (10min)"],["upper","上半身 (5min)"],["lower","下半身 (5min)"],["neck","颈部肩部 (3min)"],["custom","自定义时长"]]},
            {"id": "customDuration", "label_zh": "每个动作时长(秒)", "label_en": "Duration per stretch (sec)", "type": "number", "min": 10, "max": 120, "step": 5}
        ],
        "faq_zh": [
            {"q":"拉伸应该持续多长时间？","a":"每个拉伸动作建议保持15-30秒，整个拉伸流程5-15分钟。运动前动态拉伸，运动后静态拉伸效果最佳。"},
            {"q":"拉伸能预防运动损伤吗？","a":"是的。定期拉伸可以增加关节活动度、改善肌肉弹性、促进血液循环，有效降低拉伤和扭伤风险。"},
            {"q":"什么时候拉伸最好？","a":"运动前做动态拉伸热身，运动后做静态拉伸放松。避免在冷肌肉状态下做高强度静态拉伸。"}
        ],
        "faq_en": [
            {"q":"How long should stretching last?","a":"Hold each stretch 15-30 seconds, total routine 5-15 minutes. Dynamic stretching before exercise, static stretching after for best results."},
            {"q":"Can stretching prevent injuries?","a":"Yes. Regular stretching improves joint range of motion, muscle elasticity, and blood circulation, reducing strain and sprain risks."},
            {"q":"When is the best time to stretch?","a":"Dynamic stretches before workout as warm-up, static stretches after as cool-down. Avoid intense static stretching on cold muscles."}
        ],
        "calculate_js": """
const routine = document.getElementById('routine').value;
let stretches;
if (routine === 'full') {
  stretches = [
    {name:'颈部侧倾', dur:30}, {name:'肩部绕环', dur:30}, {name:'手臂拉伸', dur:30},
    {name:'体侧拉伸', dur:30}, {name:'脊柱扭转', dur:30}, {name:'猫牛式', dur:30},
    {name:'髋屈肌拉伸', dur:30}, {name:'腘绳肌拉伸', dur:30}, {name:'股四头肌拉伸', dur:30},
    {name:'小腿拉伸', dur:30}
  ];
} else if (routine === 'upper') {
  stretches = [
    {name:'颈部侧倾', dur:30}, {name:'肩部绕环', dur:30}, {name:'手臂拉伸', dur:30},
    {name:'体侧拉伸', dur:30}, {name:'脊柱扭转', dur:30}
  ];
} else if (routine === 'lower') {
  stretches = [
    {name:'髋屈肌拉伸', dur:30}, {name:'腘绳肌拉伸', dur:30}, {name:'股四头肌拉伸', dur:30},
    {name:'小腿拉伸', dur:30}, {name:'蝴蝶拉伸', dur:30}
  ];
} else if (routine === 'neck') {
  stretches = [
    {name:'颈部侧倾', dur:30}, {name:'颈部旋转', dur:30}, {name:'肩部耸肩', dur:30}
  ];
} else {
  const cd = parseInt(document.getElementById('customDuration').value) || 30;
  stretches = [
    {name:'颈部拉伸', dur:cd}, {name:'肩部拉伸', dur:cd}, {name:'背部拉伸', dur:cd},
    {name:'腿部拉伸', dur:cd}, {name:'全身拉伸', dur:cd}
  ];
}

const totalSec = stretches.reduce((s,st) => s + st.dur, 0);
document.getElementById('resTotal').textContent = totalSec + ' 秒 (' + Math.floor(totalSec/60) + '分' + (totalSec%60) + '秒)';
document.getElementById('resCount').textContent = stretches.length + ' 个动作';

let html = '';
stretches.forEach((st,i) => {
  html += '<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.08)"><span>' + (i+1) + '. ' + st.name + '</span><span style="color:#22d3ee">' + st.dur + 's</span></div>';
});
document.getElementById('resList').innerHTML = html;
document.getElementById('resultSection').style.display = 'block';
"""
    },
    {
        "slug": "grip-strength-calculator",
        "name_zh": "握力等级计算器",
        "name_en": "Grip Strength Calculator",
        "desc_zh": "免费在线握力等级计算器，输入握力值和性别年龄，评估您的握力水平（优秀/良好/一般/需改善）。握力是整体健康的重要指标。纯前端本地计算。",
        "desc_en": "Free online grip strength calculator — evaluate your grip strength level (excellent/good/fair/needs improvement) based on grip force, gender, and age. Grip strength is a key health indicator. 100% client-side.",
        "icon": "🤝",
        "category": "health",
        "inputs": [
            {"id": "gender", "label_zh": "性别", "label_en": "Gender", "type": "select", "options": [["male","男性"],["female","女性"]]},
            {"id": "age", "label_zh": "年龄", "label_en": "Age", "type": "number", "min": 10, "max": 90, "step": 1},
            {"id": "grip", "label_zh": "握力 (kg)", "label_en": "Grip Strength (kg)", "type": "number", "min": 5, "max": 100, "step": 0.1},
            {"id": "hand", "label_zh": "惯用手", "label_en": "Dominant Hand", "type": "select", "options": [["right","右手"],["left","左手"]]}
        ],
        "faq_zh": [
            {"q":"握力为什么重要？","a":"握力是整体肌肉力量和健康状况的重要指标。研究表明握力与心血管健康、长寿和日常功能能力密切相关。低握力可能预示更高的健康风险。"},
            {"q":"正常握力是多少？","a":"成年男性平均握力约45-55kg，女性约25-35kg。握力在30-40岁达到峰值，之后逐年下降。定期测量可追踪健康变化。"},
            {"q":"如何提高握力？","a":"可通过握力器训练、农夫行走、引体向上、哑铃训练等提高。建议每周2-3次，每次3-5组，每组保持10-15秒。"}
        ],
        "faq_en": [
            {"q":"Why is grip strength important?","a":"Grip strength is a key indicator of overall muscle strength and health. Research links it to cardiovascular health, longevity, and daily function. Low grip strength may signal higher health risks."},
            {"q":"What is a normal grip strength?","a":"Adult males average ~45-55kg, females ~25-35kg. Grip strength peaks around age 30-40 then gradually declines. Regular measurement helps track health changes."},
            {"q":"How to improve grip strength?","a":"Use grip trainers, farmer's walks, pull-ups, and dumbbell training. Aim for 2-3 sessions/week, 3-5 sets, holding 10-15 seconds each."}
        ],
        "calculate_js": """
const gender = document.getElementById('gender').value;
const age = parseInt(document.getElementById('age').value);
const grip = parseFloat(document.getElementById('grip').value);
if (!grip) { showToast('请输入握力值'); return; }

// Reference: ACSM norms (approximate)
let levels;
if (gender === 'male') {
  if (age < 30) levels = {excellent: 55, good: 48, fair: 40};
  else if (age < 40) levels = {excellent: 52, good: 45, fair: 38};
  else if (age < 50) levels = {excellent: 48, good: 42, fair: 35};
  else if (age < 60) levels = {excellent: 44, good: 38, fair: 32};
  else levels = {excellent: 38, good: 33, fair: 28};
} else {
  if (age < 30) levels = {excellent: 35, good: 30, fair: 25};
  else if (age < 40) levels = {excellent: 33, good: 28, fair: 23};
  else if (age < 50) levels = {excellent: 30, good: 25, fair: 20};
  else if (age < 60) levels = {excellent: 27, good: 22, fair: 18};
  else levels = {excellent: 23, good: 19, fair: 15};
}

let level, color, desc;
if (grip >= levels.excellent) { level = '优秀 ⭐'; color = '#22c55e'; desc = '握力处于优秀水平，肌肉力量出色！'; }
else if (grip >= levels.good) { level = '良好 👍'; color = '#06b6d4'; desc = '握力良好，保持训练可进一步提升。'; }
else if (grip >= levels.fair) { level = '一般'; color = '#eab308'; desc = '握力一般，建议增加力量训练。'; }
else { level = '需改善 �'; color = '#ef4444'; desc = '握力偏低，建议咨询医生并开始力量训练。'; }

document.getElementById('resLevel').textContent = level;
document.getElementById('resLevel').style.color = color;
document.getElementById('resDesc').textContent = desc;
document.getElementById('resPercentile').textContent = '参考标准: ' + levels.excellent + 'kg(优秀) / ' + levels.good + 'kg(良好) / ' + levels.fair + 'kg(一般)';
document.getElementById('resultSection').style.display = 'block';
"""
    },
    {
        "slug": "sleep-quality-assessor",
        "name_zh": "睡眠质量评估器",
        "name_en": "Sleep Quality Assessor",
        "desc_zh": "免费在线睡眠质量评估工具，基于PSQI匹兹堡睡眠质量指数，通过7个维度评估您的睡眠质量。输入入睡时间、睡眠时长、醒来次数等数据，获得0-21分综合评分。纯前端计算。",
        "desc_en": "Free online sleep quality assessment tool based on the Pittsburgh Sleep Quality Index (PSQI). Evaluate your sleep across 7 dimensions — sleep latency, duration, disturbances, and more. Get a 0-21 composite score. 100% client-side.",
        "icon": "😴",
        "category": "health",
        "inputs": [
            {"id": "bedtime", "label_zh": "通常几点上床?", "label_en": "Bedtime", "type": "time"},
            {"id": "latency", "label_zh": "入睡需要多久?", "label_en": "Time to fall asleep", "type": "select", "options": [["0","≤15分钟"],["1","16-30分钟"],["2","31-60分钟"],["3",">60分钟"]]},
            {"id": "wakeup", "label_zh": "通常几点起床?", "label_en": "Wake-up time", "type": "time"},
            {"id": "hours", "label_zh": "实际睡眠时长", "label_en": "Actual sleep hours", "type": "select", "options": [["0",">7小时"],["1","6-7小时"],["2","5-6小时"],["3","<5小时"]]},
            {"id": "disturbances", "label_zh": "夜间醒来次数?", "label_en": "Night disturbances", "type": "select", "options": [["0","0次"],["1","1次"],["2","2次"],["3","≥3次"]]},
            {"id": "quality", "label_zh": "主观睡眠质量", "label_en": "Subjective quality", "type": "select", "options": [["0","很好"],["1","较好"],["2","较差"],["3","很差"]]},
            {"id": "medication", "label_zh": "是否使用助眠药物?", "label_en": "Sleep medication", "type": "select", "options": [["0","从不"],["1","<1次/周"],["2","1-2次/周"],["3","≥3次/周"]]},
            {"id": "daytime", "label_zh": "白天是否困倦?", "label_en": "Daytime drowsiness", "type": "select", "options": [["0","从不"],["1","偶尔"],["2","经常"],["3","严重影响"]]}
        ],
        "faq_zh": [
            {"q":"什么是PSQI睡眠质量指数？","a":"匹兹堡睡眠质量指数(PSQI)是国际公认的睡眠评估工具，通过7个维度评估近1个月的睡眠质量。总分0-21分，≤5分为良好，>5分建议改善。"},
            {"q":"如何提高睡眠质量？","a":"保持规律作息、睡前1小时远离屏幕、保持卧室凉爽黑暗、避免咖啡因和酒精、白天适度运动。如果长期失眠建议咨询医生。"},
            {"q":"成年人需要多少睡眠？","a":"大多数成年人需要7-9小时。但个体差异大，关键是醒来后感觉精神充沛。长期<6小时或>10小时都可能增加健康风险。"}
        ],
        "faq_en": [
            {"q":"What is the PSQI sleep quality index?","a":"The Pittsburgh Sleep Quality Index (PSQI) is a globally recognized sleep assessment using 7 dimensions. Total score 0-21; ≤5 is good, >5 suggests improvement needed."},
            {"q":"How to improve sleep quality?","a":"Maintain regular schedule, avoid screens 1h before bed, keep bedroom cool and dark, avoid caffeine/alcohol, exercise moderately. Consult a doctor for chronic insomnia."},
            {"q":"How much sleep do adults need?","a":"Most adults need 7-9 hours. Individual variation is large — the key is waking up refreshed. Consistently <6h or >10h may increase health risks."}
        ],
        "calculate_js": """
const scores = ['latency','hours','disturbances','quality','medication','daytime'];
let total = 0;
scores.forEach(id => { total += parseInt(document.getElementById(id).value); });

let level, color, advice;
if (total <= 5) { level = '良好 😊'; color = '#22c55e'; advice = '睡眠质量良好，请继续保持规律作息。'; }
else if (total <= 10) { level = '一般 😐'; color = '#eab308'; advice = '睡眠质量有待改善，建议优化睡眠环境和作息。'; }
else { level = '较差 😟'; color = '#ef4444'; advice = '睡眠质量较差，建议咨询医生或睡眠专家。'; }

document.getElementById('resScore').textContent = total + ' / 21';
document.getElementById('resLevel').textContent = level;
document.getElementById('resLevel').style.color = color;
document.getElementById('resAdvice').textContent = advice;
document.getElementById('resultSection').style.display = 'block';
"""
    }
]

print(f"准备创建 {len(TOOLS)} 个工具")
for t in TOOLS:
    print(f"  - {t['slug']}: {t['name_zh']}")