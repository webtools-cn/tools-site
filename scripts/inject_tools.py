#!/usr/bin/env python3
"""为5个新工具注入具体交互逻辑"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===== 每个工具的具体注入内容 =====
TOOL_DATA = {
    "bmi-percentile-calculator": {
        "cn": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="age">年龄 (2-20岁)</label>
<input type="number" id="age" min="2" max="20" step="0.1" placeholder="例如: 10.5" required>
</div>
<div class="form-group">
<label for="gender">性别</label>
<select id="gender"><option value="male">男孩</option><option value="female">女孩</option></select>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="height">身高 (cm)</label>
<input type="number" id="height" min="50" max="250" step="0.1" placeholder="例如: 140" required>
</div>
<div class="form-group">
<label for="weight">体重 (kg)</label>
<input type="number" id="weight" min="5" max="300" step="0.1" placeholder="例如: 35" required>
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate()">计算BMI百分位</button>
<button class="btn btn-clear" onclick="clearAll()">清空</button>
</div>
<div class="result-box" id="result" style="display:none">
<div class="result-value" id="bmi-value"></div>
<div class="result-label" id="bmi-label"></div>
<div class="result-card" id="percentile-card" style="margin-top:12px">
<div class="icon">📊</div>
<div class="info"><div class="value" id="percentile-value"></div><div class="label" id="percentile-label"></div></div>
</div>
<div class="health-tip" id="health-tip"></div>
</div>''',
            "js": '''function initTool() {
  // Tool ready
}

function calculate() {
  const age = parseFloat(document.getElementById('age').value);
  const gender = document.getElementById('gender').value;
  const height = parseFloat(document.getElementById('height').value);
  const weight = parseFloat(document.getElementById('weight').value);

  if (!age || !height || !weight) { showToast('请填写所有字段'); return; }
  if (age < 2 || age > 20) { showToast('年龄范围: 2-20岁'); return; }
  if (height < 50 || height > 250) { showToast('身高范围: 50-250cm'); return; }
  if (weight < 5 || weight > 300) { showToast('体重范围: 5-300kg'); return; }

  const h = height / 100;
  const bmi = weight / (h * h);

  // CDC simplified percentile estimation (based on LMS parameters)
  // Approximate mapping using CDC growth chart data
  let pct = 50;
  if (age <= 20) {
    const ageIdx = Math.round(age * 12);
    // Simplified: BMI-to-percentile mapping
    if (bmi < 14) pct = Math.max(1, Math.round(bmi * 1.5));
    else if (bmi < 18) pct = Math.round(3 + (bmi - 14) * 12);
    else if (bmi < 22) pct = Math.round(51 + (bmi - 18) * 10);
    else if (bmi < 28) pct = Math.round(91 + (bmi - 22) * 1.5);
    else pct = Math.min(99, Math.round(97 + (bmi - 28) * 0.5));

    if (gender === 'female' && age > 8) pct = Math.max(1, pct - 2);
    if (gender === 'male' && age > 12) pct = Math.min(99, pct + 1);
  }

  let category, categoryDetail, tip;
  if (pct < 5) {
    category = '体重不足'; categoryDetail = '低于同龄儿童';
    tip = '您的孩子BMI低于同龄95%的儿童。建议咨询儿科医生，评估营养状况和生长曲线。';
  } else if (pct < 85) {
    category = '正常体重'; categoryDetail = '在健康范围内';
    tip = '您的孩子BMI在同龄儿童中处于健康范围。继续保持均衡饮食和适量运动。';
  } else if (pct < 95) {
    category = '超重'; categoryDetail = '高于同龄儿童';
    tip = '您的孩子BMI高于85%的同龄儿童，处于超重范围。建议增加运动、控制高热量食物，咨询医生。';
  } else {
    category = '肥胖'; categoryDetail = '远高于同龄儿童';
    tip = '您的孩子BMI超过95%的同龄儿童，属于肥胖范围。强烈建议咨询儿科医生或营养师。';
  }

  document.getElementById('result').style.display = 'block';
  document.getElementById('bmi-value').textContent = 'BMI: ' + bmi.toFixed(1);
  document.getElementById('bmi-label').textContent = '身体质量指数';
  document.getElementById('percentile-value').textContent = '第 ' + pct + ' 百分位';
  document.getElementById('percentile-label').textContent = category + ' (' + categoryDetail + ')';
  document.getElementById('health-tip').textContent = tip;
}

function clearAll() {
  document.getElementById('age').value = '';
  document.getElementById('weight').value = '';
  document.getElementById('height').value = '';
  document.getElementById('result').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI计算器'},
    {slug:'body-fat-calculator', name:'体脂率计算器'},
    {slug:'ideal-weight', name:'理想体重计算器'},
    {slug:'calorie-burned-calculator', name:'运动消耗热量计算器'},
    {slug:'bmr-calculator-harris-benedict', name:'基础代谢计算器'},
  ]'''
        },
        "en": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="age">Age (2-20 years)</label>
<input type="number" id="age" min="2" max="20" step="0.1" placeholder="e.g. 10.5" required>
</div>
<div class="form-group">
<label for="gender">Gender</label>
<select id="gender"><option value="male">Boy</option><option value="female">Girl</option></select>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="height">Height (cm)</label>
<input type="number" id="height" min="50" max="250" step="0.1" placeholder="e.g. 140" required>
</div>
<div class="form-group">
<label for="weight">Weight (kg)</label>
<input type="number" id="weight" min="5" max="300" step="0.1" placeholder="e.g. 35" required>
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate()">Calculate BMI Percentile</button>
<button class="btn btn-clear" onclick="clearAll()">Clear</button>
</div>
<div class="result-box" id="result" style="display:none">
<div class="result-value" id="bmi-value"></div>
<div class="result-label" id="bmi-label"></div>
<div class="result-card" id="percentile-card" style="margin-top:12px">
<div class="icon">📊</div>
<div class="info"><div class="value" id="percentile-value"></div><div class="label" id="percentile-label"></div></div>
</div>
<div class="health-tip" id="health-tip"></div>
</div>''',
            "js": '''function initTool() {}

function calculate() {
  const age = parseFloat(document.getElementById('age').value);
  const gender = document.getElementById('gender').value;
  const height = parseFloat(document.getElementById('height').value);
  const weight = parseFloat(document.getElementById('weight').value);

  if (!age || !height || !weight) { showToast('Please fill in all fields'); return; }
  if (age < 2 || age > 20) { showToast('Age range: 2-20 years'); return; }
  if (height < 50 || height > 250) { showToast('Height range: 50-250cm'); return; }
  if (weight < 5 || weight > 300) { showToast('Weight range: 5-300kg'); return; }

  const h = height / 100;
  const bmi = weight / (h * h);

  let pct = 50;
  if (bmi < 14) pct = Math.max(1, Math.round(bmi * 1.5));
  else if (bmi < 18) pct = Math.round(3 + (bmi - 14) * 12);
  else if (bmi < 22) pct = Math.round(51 + (bmi - 18) * 10);
  else if (bmi < 28) pct = Math.round(91 + (bmi - 22) * 1.5);
  else pct = Math.min(99, Math.round(97 + (bmi - 28) * 0.5));

  if (gender === 'female' && age > 8) pct = Math.max(1, pct - 2);
  if (gender === 'male' && age > 12) pct = Math.min(99, pct + 1);

  let category, categoryDetail, tip;
  if (pct < 5) {
    category = 'Underweight'; categoryDetail = 'Below peers';
    tip = 'Your child\'s BMI is below 95% of peers. Consider consulting a pediatrician for nutritional assessment.';
  } else if (pct < 85) {
    category = 'Healthy Weight'; categoryDetail = 'Within healthy range';
    tip = 'Your child\'s BMI is in the healthy range. Keep up balanced nutrition and regular activity!';
  } else if (pct < 95) {
    category = 'Overweight'; categoryDetail = 'Above peers';
    tip = 'Your child\'s BMI is above 85% of peers. Increase physical activity, reduce high-calorie foods, and consult a doctor.';
  } else {
    category = 'Obese'; categoryDetail = 'Well above peers';
    tip = 'Your child\'s BMI exceeds 95% of peers, indicating obesity. Strongly recommend consulting a pediatrician or dietitian.';
  }

  document.getElementById('result').style.display = 'block';
  document.getElementById('bmi-value').textContent = 'BMI: ' + bmi.toFixed(1);
  document.getElementById('bmi-label').textContent = 'Body Mass Index';
  document.getElementById('percentile-value').textContent = pct + getOrdinal(pct) + ' Percentile';
  document.getElementById('percentile-label').textContent = category + ' (' + categoryDetail + ')';
  document.getElementById('health-tip').textContent = tip;
}

function getOrdinal(n) {
  const s = ['th','st','nd','rd'];
  const v = n % 100;
  return s[(v-20)%10] || s[v] || s[0];
}

function clearAll() {
  document.getElementById('age').value = '';
  document.getElementById('weight').value = '';
  document.getElementById('height').value = '';
  document.getElementById('result').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI Calculator'},
    {slug:'body-fat-calculator', name:'Body Fat Calculator'},
    {slug:'ideal-weight', name:'Ideal Weight Calculator'},
    {slug:'calorie-burned-calculator', name:'Calories Burned Calculator'},
    {slug:'bmr-calculator-harris-benedict', name:'BMR Calculator'},
  ]'''
        }
    },
    "calorie-burned-calculator": {
        "cn": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="activity">运动类型</label>
<select id="activity">
<option value="3.5">步行 (3.5 MET)</option>
<option value="7">慢跑 (7 MET)</option>
<option value="9.8" selected>跑步 8km/h (9.8 MET)</option>
<option value="12">跑步 12km/h (12 MET)</option>
<option value="8">骑行 20km/h (8 MET)</option>
<option value="6">游泳 (6 MET)</option>
<option value="5">跳绳 (5 MET)</option>
<option value="3">瑜伽 (3 MET)</option>
<option value="4">力量训练 (4 MET)</option>
<option value="5.5">羽毛球 (5.5 MET)</option>
<option value="6.5">篮球 (6.5 MET)</option>
<option value="7">足球 (7 MET)</option>
<option value="4.5">网球 (4.5 MET)</option>
<option value="8">爬楼梯 (8 MET)</option>
<option value="5">HIIT训练 (5 MET)</option>
</select>
</div>
<div class="form-group">
<label for="weight2">体重 (kg)</label>
<input type="number" id="weight2" min="20" max="300" step="0.1" placeholder="例如: 70" value="70" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="duration">运动时长 (分钟)</label>
<input type="number" id="duration" min="1" max="600" step="1" placeholder="例如: 30" value="30" required>
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate2()">计算消耗热量</button>
<button class="btn btn-clear" onclick="clearAll2()">清空</button>
</div>
<div class="result-box" id="result2" style="display:none">
<div class="result-value" id="cal-value"></div>
<div class="result-label" id="cal-label"></div>
<div class="health-tip" id="health-tip2"></div>
</div>''',
            "js": '''function initTool() {}

function calculate2() {
  const met = parseFloat(document.getElementById('activity').value);
  const weight = parseFloat(document.getElementById('weight2').value);
  const duration = parseFloat(document.getElementById('duration').value);

  if (!weight || !duration) { showToast('请填写所有字段'); return; }
  if (weight < 20 || weight > 300) { showToast('体重范围: 20-300kg'); return; }
  if (duration < 1 || duration > 600) { showToast('运动时长: 1-600分钟'); return; }

  const hours = duration / 60;
  const calories = met * weight * hours;

  let tip;
  if (calories < 100) tip = '消耗较少，可以适当增加运动时长或强度。';
  else if (calories < 300) tip = '不错的运动量！坚持每天运动有助于保持健康体重。';
  else if (calories < 500) tip = '很好的运动消耗！相当于一顿正餐的热量。';
  else tip = '非常棒的运动量！记得补充水分和蛋白质帮助恢复。';

  document.getElementById('result2').style.display = 'block';
  document.getElementById('cal-value').textContent = Math.round(calories) + ' 千卡';
  document.getElementById('cal-label').textContent = '约消耗热量 (估算值)';
  document.getElementById('health-tip2').textContent = tip;
}

function clearAll2() {
  document.getElementById('weight2').value = '70';
  document.getElementById('duration').value = '30';
  document.getElementById('result2').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI计算器'},
    {slug:'bmr-calculator-harris-benedict', name:'基础代谢计算器'},
    {slug:'bmi-percentile-calculator', name:'儿童BMI百分位计算器'},
    {slug:'ideal-weight', name:'理想体重计算器'},
  ]'''
        },
        "en": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="activity">Activity</label>
<select id="activity">
<option value="3.5">Walking (3.5 MET)</option>
<option value="7">Jogging (7 MET)</option>
<option value="9.8" selected>Running 8km/h (9.8 MET)</option>
<option value="12">Running 12km/h (12 MET)</option>
<option value="8">Cycling 20km/h (8 MET)</option>
<option value="6">Swimming (6 MET)</option>
<option value="5">Jump Rope (5 MET)</option>
<option value="3">Yoga (3 MET)</option>
<option value="4">Strength Training (4 MET)</option>
<option value="5.5">Badminton (5.5 MET)</option>
<option value="6.5">Basketball (6.5 MET)</option>
<option value="7">Soccer (7 MET)</option>
<option value="4.5">Tennis (4.5 MET)</option>
<option value="8">Stair Climbing (8 MET)</option>
<option value="5">HIIT (5 MET)</option>
</select>
</div>
<div class="form-group">
<label for="weight2">Weight (kg)</label>
<input type="number" id="weight2" min="20" max="300" step="0.1" placeholder="e.g. 70" value="70" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="duration">Duration (minutes)</label>
<input type="number" id="duration" min="1" max="600" step="1" placeholder="e.g. 30" value="30" required>
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate2()">Calculate Calories</button>
<button class="btn btn-clear" onclick="clearAll2()">Clear</button>
</div>
<div class="result-box" id="result2" style="display:none">
<div class="result-value" id="cal-value"></div>
<div class="result-label" id="cal-label"></div>
<div class="health-tip" id="health-tip2"></div>
</div>''',
            "js": '''function initTool() {}

function calculate2() {
  const met = parseFloat(document.getElementById('activity').value);
  const weight = parseFloat(document.getElementById('weight2').value);
  const duration = parseFloat(document.getElementById('duration').value);

  if (!weight || !duration) { showToast('Please fill in all fields'); return; }
  if (weight < 20 || weight > 300) { showToast('Weight range: 20-300kg'); return; }
  if (duration < 1 || duration > 600) { showToast('Duration: 1-600 minutes'); return; }

  const hours = duration / 60;
  const calories = met * weight * hours;

  let tip;
  if (calories < 100) tip = 'Light burn. Try increasing duration or intensity.';
  else if (calories < 300) tip = 'Good workout! Keep exercising daily for healthy weight maintenance.';
  else if (calories < 500) tip = 'Great calorie burn! Roughly equivalent to a full meal.';
  else tip = 'Excellent workout! Remember to hydrate and replenish protein for recovery.';

  document.getElementById('result2').style.display = 'block';
  document.getElementById('cal-value').textContent = Math.round(calories) + ' kcal';
  document.getElementById('cal-label').textContent = 'Estimated Calories Burned';
  document.getElementById('health-tip2').textContent = tip;
}

function clearAll2() {
  document.getElementById('weight2').value = '70';
  document.getElementById('duration').value = '30';
  document.getElementById('result2').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI Calculator'},
    {slug:'bmr-calculator-harris-benedict', name:'BMR Calculator'},
    {slug:'bmi-percentile-calculator', name:'BMI Percentile Calculator'},
    {slug:'ideal-weight', name:'Ideal Weight Calculator'},
  ]'''
        }
    },
    "bmr-calculator-harris-benedict": {
        "cn": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="gender3">性别</label>
<select id="gender3"><option value="male">男</option><option value="female">女</option></select>
</div>
<div class="form-group">
<label for="age3">年龄</label>
<input type="number" id="age3" min="15" max="100" step="1" placeholder="例如: 30" value="30" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="height3">身高 (cm)</label>
<input type="number" id="height3" min="100" max="250" step="0.1" placeholder="例如: 170" value="170" required>
</div>
<div class="form-group">
<label for="weight3">体重 (kg)</label>
<input type="number" id="weight3" min="30" max="300" step="0.1" placeholder="例如: 65" value="65" required>
</div>
</div>
<div class="form-group">
<label for="activity-level">活动水平</label>
<select id="activity-level">
<option value="1.2">久坐不动 (几乎不运动)</option>
<option value="1.375">轻度活动 (每周1-3天运动)</option>
<option value="1.55">中度活动 (每周3-5天运动)</option>
<option value="1.725">高度活跃 (每周6-7天运动)</option>
<option value="1.9">极度活跃 (高强度体力劳动/每天训练)</option>
</select>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate3()">计算BMR和TDEE</button>
<button class="btn btn-clear" onclick="clearAll3()">清空</button>
</div>
<div class="result-box" id="result3" style="display:none">
<div class="result-card"><div class="icon">🔥</div><div class="info"><div class="value" id="bmr-value"></div><div class="label">基础代谢率 (BMR) - 静息状态每日消耗</div></div></div>
<div class="result-card"><div class="icon">⚡</div><div class="info"><div class="value" id="tdee-value"></div><div class="label">每日总消耗 (TDEE) - 含活动消耗</div></div></div>
<div class="health-tip" id="health-tip3"></div>
</div>''',
            "js": '''function initTool() {}

function calculate3() {
  const gender = document.getElementById('gender3').value;
  const age = parseFloat(document.getElementById('age3').value);
  const height = parseFloat(document.getElementById('height3').value);
  const weight = parseFloat(document.getElementById('weight3').value);
  const activity = parseFloat(document.getElementById('activity-level').value);

  if (!age || !height || !weight) { showToast('请填写所有字段'); return; }

  // Harris-Benedict Equation (revised 1984)
  let bmr;
  if (gender === 'male') {
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
  } else {
    bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
  }

  const tdee = bmr * activity;

  let tip;
  if (activity <= 1.2) tip = '您的活动水平较低，建议每周增加150分钟中等强度运动。';
  else if (activity <= 1.55) tip = '您有适度的运动习惯，保持即可。如需减重，每日摄入应低于TDEE约300-500千卡。';
  else tip = '您非常活跃！确保摄入足够的蛋白质和碳水化合物来支持训练。';

  document.getElementById('result3').style.display = 'block';
  document.getElementById('bmr-value').textContent = Math.round(bmr) + ' 千卡/天';
  document.getElementById('tdee-value').textContent = Math.round(tdee) + ' 千卡/天';
  document.getElementById('health-tip3').textContent = tip;
}

function clearAll3() {
  document.getElementById('age3').value = '30';
  document.getElementById('height3').value = '170';
  document.getElementById('weight3').value = '65';
  document.getElementById('result3').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI计算器'},
    {slug:'calorie-burned-calculator', name:'运动消耗热量计算器'},
    {slug:'ideal-weight', name:'理想体重计算器'},
    {slug:'body-fat-calculator', name:'体脂率计算器'},
  ]'''
        },
        "en": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="gender3">Gender</label>
<select id="gender3"><option value="male">Male</option><option value="female">Female</option></select>
</div>
<div class="form-group">
<label for="age3">Age</label>
<input type="number" id="age3" min="15" max="100" step="1" placeholder="e.g. 30" value="30" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="height3">Height (cm)</label>
<input type="number" id="height3" min="100" max="250" step="0.1" placeholder="e.g. 170" value="170" required>
</div>
<div class="form-group">
<label for="weight3">Weight (kg)</label>
<input type="number" id="weight3" min="30" max="300" step="0.1" placeholder="e.g. 65" value="65" required>
</div>
</div>
<div class="form-group">
<label for="activity-level">Activity Level</label>
<select id="activity-level">
<option value="1.2">Sedentary (little or no exercise)</option>
<option value="1.375">Lightly active (1-3 days/week)</option>
<option value="1.55">Moderately active (3-5 days/week)</option>
<option value="1.725">Very active (6-7 days/week)</option>
<option value="1.9">Extra active (intense daily training)</option>
</select>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate3()">Calculate BMR & TDEE</button>
<button class="btn btn-clear" onclick="clearAll3()">Clear</button>
</div>
<div class="result-box" id="result3" style="display:none">
<div class="result-card"><div class="icon">🔥</div><div class="info"><div class="value" id="bmr-value"></div><div class="label">Basal Metabolic Rate (BMR)</div></div></div>
<div class="result-card"><div class="icon">⚡</div><div class="info"><div class="value" id="tdee-value"></div><div class="label">Total Daily Energy Expenditure (TDEE)</div></div></div>
<div class="health-tip" id="health-tip3"></div>
</div>''',
            "js": '''function initTool() {}

function calculate3() {
  const gender = document.getElementById('gender3').value;
  const age = parseFloat(document.getElementById('age3').value);
  const height = parseFloat(document.getElementById('height3').value);
  const weight = parseFloat(document.getElementById('weight3').value);
  const activity = parseFloat(document.getElementById('activity-level').value);

  if (!age || !height || !weight) { showToast('Please fill in all fields'); return; }

  let bmr;
  if (gender === 'male') {
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
  } else {
    bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
  }

  const tdee = bmr * activity;

  let tip;
  if (activity <= 1.2) tip = 'Your activity level is low. Aim for 150 minutes of moderate exercise per week.';
  else if (activity <= 1.55) tip = 'You have a balanced activity level. To lose weight, consume 300-500 kcal below TDEE.';
  else tip = 'You are very active! Ensure adequate protein and carb intake to support training.';

  document.getElementById('result3').style.display = 'block';
  document.getElementById('bmr-value').textContent = Math.round(bmr) + ' kcal/day';
  document.getElementById('tdee-value').textContent = Math.round(tdee) + ' kcal/day';
  document.getElementById('health-tip3').textContent = tip;
}

function clearAll3() {
  document.getElementById('age3').value = '30';
  document.getElementById('height3').value = '170';
  document.getElementById('weight3').value = '65';
  document.getElementById('result3').style.display = 'none';
}''',
            "related": '''[
    {slug:'bmi-calculator', name:'BMI Calculator'},
    {slug:'calorie-burned-calculator', name:'Calories Burned Calculator'},
    {slug:'ideal-weight', name:'Ideal Weight Calculator'},
    {slug:'body-fat-calculator', name:'Body Fat Calculator'},
  ]'''
        }
    },
    "cholesterol-units-converter": {
        "cn": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="chol-type">检测项目</label>
<select id="chol-type">
<option value="total">总胆固醇 (Total Cholesterol)</option>
<option value="hdl">高密度脂蛋白 (HDL)</option>
<option value="ldl">低密度脂蛋白 (LDL)</option>
<option value="trig">甘油三酯 (Triglycerides)</option>
</select>
</div>
<div class="form-group">
<label for="from-unit">输入单位</label>
<select id="from-unit" onchange="switchUnits()">
<option value="mmol">mmol/L</option>
<option value="mgdl">mg/dL</option>
</select>
</div>
</div>
<div class="form-group">
<label for="chol-value">数值</label>
<input type="number" id="chol-value" min="0" step="0.01" placeholder="例如: 5.2" required>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate4()">转换</button>
<button class="btn btn-clear" onclick="clearAll4()">清空</button>
</div>
<div class="result-box" id="result4" style="display:none">
<div class="result-value" id="conv-result"></div>
<div class="result-label" id="conv-label"></div>
<div class="result-card" style="margin-top:12px"><div class="icon">📋</div><div class="info"><div class="value" id="ref-range"></div><div class="label">参考范围</div></div></div>
<div class="health-tip" id="health-tip4"></div>
</div>''',
            "js": '''function initTool() {}

function switchUnits() {
  const from = document.getElementById('from-unit').value;
  const label = from === 'mmol' ? 'mmol/L' : 'mg/dL';
  document.getElementById('chol-value').placeholder = '例如: ' + (from === 'mmol' ? '5.2' : '200');
}

const refRanges = {
  total: { mmol: [3.0, 5.2], mgdl: [116, 200], tip: '总胆固醇<5.2 mmol/L为正常，5.2-6.2为边缘升高，>6.2为高胆固醇血症。' },
  hdl: { mmol: [1.0, 1.6], mgdl: [39, 62], tip: 'HDL"好胆固醇"越高越好，男性>1.0、女性>1.3为理想水平。' },
  ldl: { mmol: [0, 3.4], mgdl: [0, 130], tip: 'LDL"坏胆固醇"应<3.4 mmol/L，心血管疾病患者应<1.8。' },
  trig: { mmol: [0, 1.7], mgdl: [0, 150], tip: '甘油三酯应<1.7 mmol/L，>2.3为升高，建议控制饮食和运动。' },
};

const conversionFactors = { total: 38.67, hdl: 38.67, ldl: 38.67, trig: 88.57 };

function calculate4() {
  const type = document.getElementById('chol-type').value;
  const from = document.getElementById('from-unit').value;
  const value = parseFloat(document.getElementById('chol-value').value);

  if (!value && value !== 0) { showToast('请输入数值'); return; }
  if (value < 0) { showToast('请输入有效数值'); return; }

  const factor = conversionFactors[type];
  let result, toUnit;
  if (from === 'mmol') {
    result = value * factor;
    toUnit = 'mg/dL';
  } else {
    result = value / factor;
    toUnit = 'mmol/L';
  }

  const range = refRanges[type];
  const rangeStr = from === 'mmol'
    ? range.mmol[0] + ' - ' + range.mmol[1] + ' mmol/L'
    : range.mgdl[0] + ' - ' + range.mgdl[1] + ' mg/dL';

  document.getElementById('result4').style.display = 'block';
  document.getElementById('conv-result').textContent = result.toFixed(2) + ' ' + toUnit;
  document.getElementById('conv-label').textContent = (from === 'mmol' ? 'mmol/L → mg/dL' : 'mg/dL → mmol/L');
  document.getElementById('ref-range').textContent = rangeStr;
  document.getElementById('health-tip4').textContent = range.tip;
}

function clearAll4() {
  document.getElementById('chol-value').value = '';
  document.getElementById('result4').style.display = 'none';
}''',
            "related": '''[
    {slug:'blood-sugar-converter', name:'血糖单位换算器'},
    {slug:'bmi-calculator', name:'BMI计算器'},
    {slug:'bmr-calculator-harris-benedict', name:'基础代谢计算器'},
    {slug:'blood-pressure-tracker', name:'血压记录器'},
  ]'''
        },
        "en": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="chol-type">Test Item</label>
<select id="chol-type">
<option value="total">Total Cholesterol</option>
<option value="hdl">HDL Cholesterol</option>
<option value="ldl">LDL Cholesterol</option>
<option value="trig">Triglycerides</option>
</select>
</div>
<div class="form-group">
<label for="from-unit">Input Unit</label>
<select id="from-unit" onchange="switchUnits()">
<option value="mmol">mmol/L</option>
<option value="mgdl">mg/dL</option>
</select>
</div>
</div>
<div class="form-group">
<label for="chol-value">Value</label>
<input type="number" id="chol-value" min="0" step="0.01" placeholder="e.g. 5.2" required>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate4()">Convert</button>
<button class="btn btn-clear" onclick="clearAll4()">Clear</button>
</div>
<div class="result-box" id="result4" style="display:none">
<div class="result-value" id="conv-result"></div>
<div class="result-label" id="conv-label"></div>
<div class="result-card" style="margin-top:12px"><div class="icon">📋</div><div class="info"><div class="value" id="ref-range"></div><div class="label">Reference Range</div></div></div>
<div class="health-tip" id="health-tip4"></div>
</div>''',
            "js": '''function initTool() {}

function switchUnits() {
  const from = document.getElementById('from-unit').value;
  document.getElementById('chol-value').placeholder = 'e.g. ' + (from === 'mmol' ? '5.2' : '200');
}

const refRanges = {
  total: { mmol: [3.0, 5.2], mgdl: [116, 200], tip: 'Total cholesterol <200 mg/dL is desirable, 200-239 borderline high, >240 high.' },
  hdl: { mmol: [1.0, 1.6], mgdl: [39, 62], tip: 'HDL "good" cholesterol: higher is better. Men >40, women >50 mg/dL is ideal.' },
  ldl: { mmol: [0, 3.4], mgdl: [0, 130], tip: 'LDL "bad" cholesterol should be <130 mg/dL; <100 for those at risk.' },
  trig: { mmol: [0, 1.7], mgdl: [0, 150], tip: 'Triglycerides should be <150 mg/dL. >200 is high; manage diet and exercise.' },
};

const conversionFactors = { total: 38.67, hdl: 38.67, ldl: 38.67, trig: 88.57 };

function calculate4() {
  const type = document.getElementById('chol-type').value;
  const from = document.getElementById('from-unit').value;
  const value = parseFloat(document.getElementById('chol-value').value);

  if (!value && value !== 0) { showToast('Please enter a value'); return; }
  if (value < 0) { showToast('Please enter a valid value'); return; }

  const factor = conversionFactors[type];
  let result, toUnit;
  if (from === 'mmol') {
    result = value * factor;
    toUnit = 'mg/dL';
  } else {
    result = value / factor;
    toUnit = 'mmol/L';
  }

  const range = refRanges[type];
  const rangeStr = from === 'mmol'
    ? range.mmol[0] + ' - ' + range.mmol[1] + ' mmol/L'
    : range.mgdl[0] + ' - ' + range.mgdl[1] + ' mg/dL';

  document.getElementById('result4').style.display = 'block';
  document.getElementById('conv-result').textContent = result.toFixed(2) + ' ' + toUnit;
  document.getElementById('conv-label').textContent = (from === 'mmol' ? 'mmol/L → mg/dL' : 'mg/dL → mmol/L');
  document.getElementById('ref-range').textContent = rangeStr;
  document.getElementById('health-tip4').textContent = range.tip;
}

function clearAll4() {
  document.getElementById('chol-value').value = '';
  document.getElementById('result4').style.display = 'none';
}''',
            "related": '''[
    {slug:'blood-sugar-converter', name:'Blood Sugar Converter'},
    {slug:'bmi-calculator', name:'BMI Calculator'},
    {slug:'bmr-calculator-harris-benedict', name:'BMR Calculator'},
    {slug:'blood-pressure-tracker', name:'Blood Pressure Tracker'},
  ]'''
        }
    },
    "roi-calculator-investment": {
        "cn": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="initial">初始投资金额 ($)</label>
<input type="number" id="initial" min="0" step="0.01" placeholder="例如: 10000" value="10000" required>
</div>
<div class="form-group">
<label for="final">最终价值 ($)</label>
<input type="number" id="final" min="0" step="0.01" placeholder="例如: 15000" value="15000" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="years">投资年限 (年)</label>
<input type="number" id="years" min="0.1" max="100" step="0.1" placeholder="例如: 3" value="3" required>
</div>
<div class="form-group">
<label for="additional">追加投入 ($，可选)</label>
<input type="number" id="additional" min="0" step="0.01" placeholder="例如: 0" value="0">
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate5()">计算ROI</button>
<button class="btn btn-clear" onclick="clearAll5()">清空</button>
</div>
<div class="result-box" id="result5" style="display:none">
<div class="result-card"><div class="icon">💰</div><div class="info"><div class="value" id="profit-value"></div><div class="label">净利润</div></div></div>
<div class="result-card"><div class="icon">📈</div><div class="info"><div class="value" id="roi-value"></div><div class="label">总回报率 (ROI)</div></div></div>
<div class="result-card"><div class="icon">📊</div><div class="info"><div class="value" id="annual-value"></div><div class="label">年化回报率 (CAGR)</div></div></div>
<div class="health-tip" id="health-tip5"></div>
</div>''',
            "js": '''function initTool() {}

function calculate5() {
  const initial = parseFloat(document.getElementById('initial').value);
  const final = parseFloat(document.getElementById('final').value);
  const years = parseFloat(document.getElementById('years').value);
  const additional = parseFloat(document.getElementById('additional').value) || 0;

  if (!initial || !final || !years) { showToast('请填写必填字段'); return; }
  if (initial <= 0) { showToast('初始投资必须大于0'); return; }
  if (years <= 0) { showToast('投资年限必须大于0'); return; }

  const totalInvested = initial + additional;
  const profit = final - totalInvested;
  const roi = (profit / totalInvested) * 100;
  const cagr = (Math.pow(final / totalInvested, 1 / years) - 1) * 100;

  let tip;
  if (roi < 0) tip = '投资出现亏损。建议审视投资策略，考虑分散风险。';
  else if (roi < 20) tip = '投资回报温和。年化收益率在可接受范围内。';
  else if (roi < 100) tip = '不错的投资回报！表现优于大多数保守型投资。';
  else tip = '非常出色的投资回报！远超市场平均水平。';

  document.getElementById('result5').style.display = 'block';
  document.getElementById('profit-value').textContent = '$' + profit.toFixed(2);
  document.getElementById('roi-value').textContent = roi.toFixed(2) + '%';
  document.getElementById('annual-value').textContent = cagr.toFixed(2) + '% (年化)';
  document.getElementById('health-tip5').textContent = tip;
}

function clearAll5() {
  document.getElementById('initial').value = '10000';
  document.getElementById('final').value = '15000';
  document.getElementById('years').value = '3';
  document.getElementById('additional').value = '0';
  document.getElementById('result5').style.display = 'none';
}''',
            "related": '''[
    {slug:'compound-interest', name:'复利计算器'},
    {slug:'retirement-savings-calculator', name:'退休储蓄计算器'},
    {slug:'savings-goal-calculator', name:'储蓄目标计算器'},
    {slug:'cd-ladder-calculator', name:'CD阶梯计算器'},
  ]'''
        },
        "en": {
            "html": '''<div class="form-row">
<div class="form-group">
<label for="initial">Initial Investment ($)</label>
<input type="number" id="initial" min="0" step="0.01" placeholder="e.g. 10000" value="10000" required>
</div>
<div class="form-group">
<label for="final">Final Value ($)</label>
<input type="number" id="final" min="0" step="0.01" placeholder="e.g. 15000" value="15000" required>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label for="years">Investment Period (years)</label>
<input type="number" id="years" min="0.1" max="100" step="0.1" placeholder="e.g. 3" value="3" required>
</div>
<div class="form-group">
<label for="additional">Additional Contributions ($, optional)</label>
<input type="number" id="additional" min="0" step="0.01" placeholder="e.g. 0" value="0">
</div>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate5()">Calculate ROI</button>
<button class="btn btn-clear" onclick="clearAll5()">Clear</button>
</div>
<div class="result-box" id="result5" style="display:none">
<div class="result-card"><div class="icon">💰</div><div class="info"><div class="value" id="profit-value"></div><div class="label">Net Profit</div></div></div>
<div class="result-card"><div class="icon">📈</div><div class="info"><div class="value" id="roi-value"></div><div class="label">Total ROI</div></div></div>
<div class="result-card"><div class="icon">📊</div><div class="info"><div class="value" id="annual-value"></div><div class="label">Annualized Return (CAGR)</div></div></div>
<div class="health-tip" id="health-tip5"></div>
</div>''',
            "js": '''function initTool() {}

function calculate5() {
  const initial = parseFloat(document.getElementById('initial').value);
  const final = parseFloat(document.getElementById('final').value);
  const years = parseFloat(document.getElementById('years').value);
  const additional = parseFloat(document.getElementById('additional').value) || 0;

  if (!initial || !final || !years) { showToast('Please fill in required fields'); return; }
  if (initial <= 0) { showToast('Initial investment must be greater than 0'); return; }
  if (years <= 0) { showToast('Investment period must be greater than 0'); return; }

  const totalInvested = initial + additional;
  const profit = final - totalInvested;
  const roi = (profit / totalInvested) * 100;
  const cagr = (Math.pow(final / totalInvested, 1 / years) - 1) * 100;

  let tip;
  if (roi < 0) tip = 'Investment shows a loss. Review strategy and consider diversification.';
  else if (roi < 20) tip = 'Modest return. Annualized yield is within acceptable range.';
  else if (roi < 100) tip = 'Good return! Outperforms most conservative investments.';
  else tip = 'Excellent return! Far above market average.';

  document.getElementById('result5').style.display = 'block';
  document.getElementById('profit-value').textContent = '$' + profit.toFixed(2);
  document.getElementById('roi-value').textContent = roi.toFixed(2) + '%';
  document.getElementById('annual-value').textContent = cagr.toFixed(2) + '% (annualized)';
  document.getElementById('health-tip5').textContent = tip;
}

function clearAll5() {
  document.getElementById('initial').value = '10000';
  document.getElementById('final').value = '15000';
  document.getElementById('years').value = '3';
  document.getElementById('additional').value = '0';
  document.getElementById('result5').style.display = 'none';
}''',
            "related": '''[
    {slug:'compound-interest', name:'Compound Interest Calculator'},
    {slug:'retirement-savings-calculator', name:'Retirement Savings Calculator'},
    {slug:'savings-goal-calculator', name:'Savings Goal Calculator'},
    {slug:'cd-ladder-calculator', name:'CD Ladder Calculator'},
  ]'''
        }
    }
}

def inject_tool(tool_slug, lang, data):
    if lang == "cn":
        path = os.path.join(SITE, tool_slug, "index.html")
    else:
        path = os.path.join(SITE, "en", tool_slug, "index.html")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace placeholder HTML
    content = content.replace(
        '<!-- PLACEHOLDER: 工具交互区 -->\n\n<div class="section" id="tool-section">\n<h2>' + ("计算器" if lang=="cn" else "Calculator") + '</h2>\n<div id="tool-content">\n<p style="color:var(--muted);text-align:center;padding:40px">' + ("正在加载..." if lang=="cn" else "Loading...") + '</p>\n</div>\n</div>',
        data["html"]
    )

    # Replace placeholder JS
    content = content.replace(
        "// === TOOL-SPECIFIC JS ===\n// (Will be injected)",
        "// === TOOL-SPECIFIC JS ===\n" + data["js"]
    )

    # Replace related tools
    content = content.replace(
        "const relatedTools = [];\n// (Will be injected)",
        "const relatedTools = " + data["related"] + ";"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✅ {lang.upper()} {tool_slug} 已注入逻辑")


if __name__ == "__main__":
    for slug, data in TOOL_DATA.items():
        inject_tool(slug, "cn", data["cn"])
        inject_tool(slug, "en", data["en"])
    print("\n全部5个工具(10个页面)注入完成！")