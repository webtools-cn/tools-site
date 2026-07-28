#!/usr/bin/env python3
"""批量创建5个新工具：keto-calculator, dog-age, pet-calorie, deck-cost, hvac-size"""
import sys
sys.path.insert(0, '/home/chison/tools-site/_gen')
from tool_template_v3 import ToolPageBuilder
import os

BASE = '/home/chison/tools-site'

builder = ToolPageBuilder()

# ============================================================
# 工具1: keto-calculator - 生酮饮食宏量计算器
# ============================================================
keto_html_cn = '''
<div class="form-row"><div class="form-group"><label>体重 (kg)</label><input type="number" id="weight" placeholder="70" value="70" min="30" max="300"></div><div class="form-group"><label>身高 (cm)</label><input type="number" id="height" placeholder="170" value="170" min="100" max="250"></div></div>
<div class="form-row"><div class="form-group"><label>年龄</label><input type="number" id="age" placeholder="30" value="30" min="1" max="120"></div><div class="form-group"><label>性别</label><select id="gender"><option value="male">男</option><option value="female">女</option></select></div></div>
<div class="form-row"><div class="form-group"><label>活动水平</label><select id="activity"><option value="1.2">久坐（几乎不运动）</option><option value="1.375">轻度（每周1-3天）</option><option value="1.55" selected>中度（每周3-5天）</option><option value="1.725">重度（每周6-7天）</option><option value="1.9">运动员（每天高强度）</option></select></div><div class="form-group"><label>碳水比例 (g)</label><input type="number" id="carbs" placeholder="20" value="20" min="5" max="100"></div></div>
<button class="btn-primary" onclick="calcKeto()">计算生酮宏量</button>
<div id="result" class="result-section" style="display:none;margin-top:20px">
<div class="result-grid" id="resultGrid"></div>
<div style="background:#0f172a;border-radius:10px;padding:20px;margin-top:16px;border:1px solid rgba(148,163,184,.1)">
<h3 style="color:#f1c40f;margin-bottom:12px">每日餐食建议 (3餐)</h3><div id="mealPlan" style="color:#94a3b8;font-size:.9rem;line-height:1.8"></div>
</div>
</div>
'''

keto_html_en = keto_html_cn.replace('体重 (kg)', 'Weight (kg)').replace('身高 (cm)', 'Height (cm)').replace('年龄', 'Age').replace('性别', 'Gender').replace('男', 'Male').replace('女', 'Female').replace('活动水平', 'Activity Level').replace('久坐（几乎不运动）', 'Sedentary (little/no exercise)').replace('轻度（每周1-3天）', 'Light (1-3 days/week)').replace('中度（每周3-5天）', 'Moderate (3-5 days/week)').replace('重度（每周6-7天）', 'Heavy (6-7 days/week)').replace('运动员（每天高强度）', 'Athlete (intense daily)').replace('碳水比例 (g)', 'Carb Limit (g)').replace('计算生酮宏量', 'Calculate Keto Macros').replace('每日餐食建议 (3餐)', 'Daily Meal Plan (3 meals)')

keto_js = '''
function calcKeto(){var w=parseFloat(document.getElementById("weight").value)||70;var h=parseFloat(document.getElementById("height").value)||170;var a=parseFloat(document.getElementById("age").value)||30;var g=document.getElementById("gender").value;var act=parseFloat(document.getElementById("activity").value);var c=parseFloat(document.getElementById("carbs").value)||20;
var bmr=g==="male"?10*w+6.25*h-5*a+5:10*w+6.25*h-5*a-161;
var tdee=bmr*act;
var protein=w*1.8;
var carbCal=c*4;
var fatCal=tdee*0.25;
var fatGram=Math.round(fatCal/9);
var proteinCal=protein*4;
var totalCal=proteinCal+carbCal+fatCal;
var remaining=tdee-totalCal;
var extraFat=Math.round(Math.max(0,remaining)/9);
fatGram+=extraFat;
var finalCal=proteinCal+carbCal+(fatGram*9);
var carbs=Math.round(c);
protein=Math.round(protein);
var grid=document.getElementById("resultGrid");
grid.innerHTML='<div class="result-item"><div class="value">'+Math.round(finalCal)+'</div><div class="label">总热量 (kcal)</div></div>'+'<div class="result-item"><div class="value">'+protein+'g</div><div class="label">蛋白质</div></div>'+'<div class="result-item"><div class="value">'+carbs+'g</div><div class="label">碳水</div></div>'+'<div class="result-item"><div class="value">'+fatGram+'g</div><div class="label">脂肪</div></div>'+'<div class="result-item"><div class="value">'+Math.round(protein*4)+'</div><div class="label">蛋白质热量</div></div>'+'<div class="result-item"><div class="value">'+Math.round(fatGram*9)+'</div><div class="label">脂肪热量</div></div>';
var perMealProtein=Math.round(protein/3);var perMealFat=Math.round(fatGram/3);
document.getElementById("mealPlan").innerHTML='早餐: 蛋白质 ~'+perMealProtein+'g | 脂肪 ~'+perMealFat+'g | 碳水 <'+Math.round(carbs/3)+'g<br>午餐: 蛋白质 ~'+perMealProtein+'g | 脂肪 ~'+perMealFat+'g | 碳水 <'+Math.round(carbs/3)+'g<br>晚餐: 蛋白质 ~'+perMealProtein+'g | 脂肪 ~'+perMealFat+'g | 碳水 <'+Math.round(carbs/3)+'g';
document.getElementById("result").style.display="block";}
'''

keto_faqs_cn = [
    ("什么是生酮饮食？", "生酮饮食是一种高脂肪、适量蛋白质、极低碳水化合物的饮食方式，迫使身体进入酮症状态，以脂肪为主要能量来源。"),
    ("每天应该摄入多少碳水？", "标准的生酮饮食每日碳水摄入通常限制在20-50克。网络碳水（总碳水减去纤维和糖醇）是更精确的计量方式。"),
    ("蛋白质摄入太多会退出酮症吗？", "过量蛋白质可能通过糖异生转化为葡萄糖，建议每公斤体重1.5-2.2克蛋白质，根据活动水平调整。"),
    ("这个计算器适合所有人吗？", "本计算器提供一般性参考，具体饮食计划请咨询专业营养师或医生，特别是有肾脏疾病、肝病或糖尿病的用户。"),
]
keto_faqs_en = [
    ("What is the Keto Diet?", "The ketogenic diet is a high-fat, moderate-protein, very low-carbohydrate eating pattern that forces the body into ketosis, using fat as its primary energy source."),
    ("How many carbs should I eat daily?", "Standard keto typically limits daily carb intake to 20-50 grams. Net carbs (total carbs minus fiber and sugar alcohols) are a more precise metric."),
    ("Does too much protein kick me out of ketosis?", "Excess protein may convert to glucose via gluconeogenesis. Recommended intake is 1.5-2.2g per kg of body weight, adjusted for activity level."),
    ("Is this calculator suitable for everyone?", "This calculator provides general reference. Consult a dietitian or doctor before starting keto, especially if you have kidney disease, liver conditions, or diabetes."),
]

# ============================================================
# 工具2: dog-age - 狗狗年龄计算器
# ============================================================
dog_age_html_cn = '''
<div class="form-row"><div class="form-group"><label>狗狗品种</label><select id="breedSize"><option value="small">小型犬 (＜10kg)</option><option value="medium" selected>中型犬 (10-25kg)</option><option value="large">大型犬 (25-45kg)</option><option value="giant">巨型犬 (＞45kg)</option></select></div><div class="form-group"><label>狗狗实际年龄 (年)</label><input type="number" id="dogAge" placeholder="3" value="3" min="0" max="30" step="0.5"></div></div>
<button class="btn-primary" onclick="calcDogAge()">计算人类等效年龄</button>
<div id="result" class="result-section" style="display:none;margin-top:20px">
<div class="result-grid" id="resultGrid"></div>
<div style="background:#0f172a;border-radius:10px;padding:20px;margin-top:16px;border:1px solid rgba(148,163,184,.1)">
<h3 style="color:#f1c40f;margin-bottom:12px">生命阶段</h3><p id="lifeStage" style="color:#94a3b8;font-size:1rem"></p>
</div>
<div style="background:#0f172a;border-radius:10px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.1);color:#94a3b8;font-size:.85rem">
<strong>科普：</strong>狗狗1岁≠人类7岁。前两年发育快，之后品种体型影响衰老速度。小型犬寿命更长、衰老更慢。</div>
</div>
'''

dog_age_html_en = dog_age_html_cn.replace('狗狗品种', 'Breed Size').replace('小型犬 (＜10kg)', 'Small (＜10kg / ＜22lb)').replace('中型犬 (10-25kg)', 'Medium (10-25kg / 22-55lb)').replace('大型犬 (25-45kg)', 'Large (25-45kg / 55-99lb)').replace('巨型犬 (＞45kg)', 'Giant (＞45kg / ＞99lb)').replace('狗狗实际年龄 (年)', 'Dog\'s Actual Age (years)').replace('计算人类等效年龄', 'Calculate Human Age Equivalent').replace('生命阶段', 'Life Stage').replace('科普：', 'Fact: ').replace('狗狗1岁≠人类7岁。前两年发育快，之后品种体型影响衰老速度。小型犬寿命更长、衰老更慢。', 'A dog\'s 1 year ≠ 7 human years. The first two years see rapid development; thereafter breed size affects aging speed. Smaller dogs live longer and age slower.')

dog_age_js = '''
function calcDogAge(){var age=parseFloat(document.getElementById("dogAge").value)||3;var size=document.getElementById("breedSize").value;
var humanAge,stage;
if(size==="small"){if(age<=1)humanAge=15*age;else if(age<=2)humanAge=15+9*(age-1);else humanAge=24+(age-2)*4;if(age<1)stage="幼犬期 (Puppy)";else if(age<2)stage="青少年期 (Adolescent)";else if(age<8)stage="成年期 (Adult)";else if(age<15)stage="老年期 (Senior)";else stage="高龄期 (Geriatric)";}
else if(size==="medium"){if(age<=1)humanAge=15*age;else if(age<=2)humanAge=15+9*(age-1);else humanAge=24+(age-2)*5;if(age<1)stage="幼犬期 (Puppy)";else if(age<2)stage="青少年期 (Adolescent)";else if(age<7)stage="成年期 (Adult)";else if(age<12)stage="老年期 (Senior)";else stage="高龄期 (Geriatric)";}
else if(size==="large"){if(age<=1)humanAge=15*age;else if(age<=2)humanAge=15+9*(age-1);else humanAge=24+(age-2)*6;if(age<1)stage="幼犬期 (Puppy)";else if(age<2)stage="青少年期 (Adolescent)";else if(age<6)stage="成年期 (Adult)";else if(age<10)stage="老年期 (Senior)";else stage="高龄期 (Geriatric)";}
else{if(age<=1)humanAge=12*age;else if(age<=2)humanAge=12+10*(age-1);else humanAge=22+(age-2)*7;if(age<1)stage="幼犬期 (Puppy)";else if(age<2)stage="青少年期 (Adolescent)";else if(age<5)stage="成年期 (Adult)";else if(age<8)stage="老年期 (Senior)";else stage="高龄期 (Geriatric)";}
humanAge=Math.round(humanAge);
document.getElementById("resultGrid").innerHTML='<div class="result-item"><div class="value">'+humanAge+'</div><div class="label">人类等效年龄 (岁)</div></div>'+'<div class="result-item"><div class="value">'+age+'</div><div class="label">狗狗实际年龄 (年)</div></div>'+'<div class="result-item"><div class="value">'+(Math.round(humanAge/age*10)/10)+'x</div><div class="label">衰老倍数</div></div>';
document.getElementById("lifeStage").textContent=stage;
document.getElementById("result").style.display="block";}
'''

dog_age_faqs_cn = [
    ("「狗1岁=人7岁」这个说法对吗？", "不准确。狗狗第一年相当于人类约15岁，第二年约24岁，之后每年因品种体型不同而差异很大，小型犬约+4岁/年，巨型犬约+7岁/年。"),
    ("不同品种的狗寿命差别有多大？", "小型犬（如吉娃娃）可活15-20年，大型犬（如金毛）约10-12年，巨型犬（如大丹犬）约7-10年。体型越大，新陈代谢越快，衰老也越快。"),
    ("如何判断狗狗进入老年期？", "小型犬约8-11岁、中型犬7-10岁、大型犬5-8岁、巨型犬5-6岁进入老年期。常见的迹象包括白毛增多、活动减少、听力视力下降。"),
]
dog_age_faqs_en = [
    ("Is '1 dog year = 7 human years' correct?", "No. A dog's first year equals ~15 human years, second year ~24, then varies greatly by breed size: small dogs +4 human years/year, giant dogs +7 human years/year."),
    ("How much does lifespan vary by breed?", "Small breeds (e.g. Chihuahua) can live 15-20 years, large breeds (e.g. Golden Retriever) ~10-12 years, giant breeds (e.g. Great Dane) ~7-10 years. Larger body size accelerates metabolism and aging."),
    ("How do I know my dog is entering senior years?", "Small dogs enter senior around 8-11, medium 7-10, large 5-8, and giant 5-6. Signs include graying fur, reduced activity, and declining vision/hearing."),
]

# ============================================================
# 工具3: pet-calorie - 宠物热量需求计算器
# ============================================================
pet_cal_html_cn = '''
<div class="form-row"><div class="form-group"><label>宠物类型</label><select id="petType" onchange="updatePetUI()"><option value="dog">狗狗 🐕</option><option value="cat">猫咪 🐱</option></select></div><div class="form-group"><label>体重 (kg)</label><input type="number" id="weight" placeholder="5" value="5" min="0.5" max="100" step="0.1"></div></div>
<div class="form-row"><div class="form-group"><label id="breedLabel">体型</label><select id="bodyCondition"><option value="underweight">偏瘦</option><option value="ideal" selected>理想体重</option><option value="overweight">偏胖</option></select></div><div class="form-group"><label>绝育状态</label><select id="neutered"><option value="yes" selected>已绝育</option><option value="no">未绝育</option></select></div></div>
<div class="form-row"><div class="form-group"><label>活动水平</label><select id="activity"><option value="low">低（宅家不动）</option><option value="moderate" selected>中等（日常散步）</option><option value="high">高（大量运动/工作犬）</option></select></div><div class="form-group"><label>生命阶段</label><select id="lifeStage"><option value="adult" selected>成年 (1-7岁)</option><option value="puppy">幼年 (＜1岁)</option><option value="senior">老年 (＞7岁)</option></select></div></div>
<button class="btn-primary" onclick="calcPetCal()">计算每日热量需求</button>
<div id="result" class="result-section" style="display:none;margin-top:20px">
<div class="result-grid" id="resultGrid"></div>
<div style="background:#0f172a;border-radius:10px;padding:20px;margin-top:16px;border:1px solid rgba(148,163,184,.1)">
<h3 style="color:#f1c40f;margin-bottom:12px">喂食建议</h3><div id="feedingAdvice" style="color:#94a3b8;font-size:.9rem;line-height:1.8"></div>
</div>
</div>
'''

pet_cal_html_en = pet_cal_html_cn.replace('宠物类型', 'Pet Type').replace('狗狗 🐕', 'Dog 🐕').replace('猫咪 🐱', 'Cat 🐱').replace('体重 (kg)', 'Weight (kg)').replace('体型', 'Body Condition').replace('偏瘦', 'Underweight').replace('理想体重', 'Ideal').replace('偏胖', 'Overweight').replace('绝育状态', 'Neutered/Spayed').replace('已绝育', 'Neutered').replace('未绝育', 'Intact').replace('活动水平', 'Activity Level').replace('低（宅家不动）', 'Low (couch potato)').replace('中等（日常散步）', 'Moderate (daily walks)').replace('高（大量运动/工作犬）', 'High (intense exercise/working)').replace('生命阶段', 'Life Stage').replace('成年 (1-7岁)', 'Adult (1-7 years)').replace('幼年 (＜1岁)', 'Puppy/Kitten (＜1 year)').replace('老年 (＞7岁)', 'Senior (＞7 years)').replace('计算每日热量需求', 'Calculate Daily Calorie Needs').replace('喂食建议', 'Feeding Advice')

pet_cal_js = '''
function updatePetUI(){var t=document.getElementById("petType").value;document.getElementById("breedLabel").textContent=t==="dog"?"体型":"体型";}
function calcPetCal(){var t=document.getElementById("petType").value;var w=parseFloat(document.getElementById("weight").value)||5;var bc=document.getElementById("bodyCondition").value;var ne=document.getElementById("neutered").value;var act=document.getElementById("activity").value;var ls=document.getElementById("lifeStage").value;
var rer=70*Math.pow(w,0.75);
var factor=1.0;
if(ne==="yes")factor*=0.8;else factor*=1.0;
if(bc==="underweight")factor*=1.2;else if(bc==="overweight")factor*=0.8;
if(t==="dog"){if(act==="low")factor*=1.0;else if(act==="moderate")factor*=1.4;else factor*=1.8;}
else{if(act==="low")factor*=0.8;else if(act==="moderate")factor*=1.0;else factor*=1.2;}
if(ls==="puppy")factor*=1.8;else if(ls==="senior")factor*=0.85;
var dailyCal=Math.round(rer*factor);
var lowCal=Math.round(dailyCal*0.9);var highCal=Math.round(dailyCal*1.1);
var cupsPerDay=t==="dog"?Math.round(dailyCal/350*10)/10:Math.round(dailyCal/300*10)/10;
document.getElementById("resultGrid").innerHTML='<div class="result-item"><div class="value">'+dailyCal+'</div><div class="label">每日热量 (kcal)</div></div>'+'<div class="result-item"><div class="value">'+lowCal+'-'+highCal+'</div><div class="label">推荐范围 (kcal)</div></div>'+'<div class="result-item"><div class="value">'+cupsPerDay+'</div><div class="label">≈ 干粮杯数/天</div></div>'+'<div class="result-item"><div class="value">'+Math.round(dailyCal*7)+'</div><div class="label">每周总热量 (kcal)</div></div>';
var advice=t==="dog"?"建议分2-3餐喂食，干粮约350kcal/杯。实际喂养量请参考狗粮包装说明，并根据体重变化调整。":"建议分2-4餐喂食，干粮约300kcal/杯。猫咪天性少食多餐，可用自动喂食器控制分量。";
document.getElementById("feedingAdvice").textContent=advice;
document.getElementById("result").style.display="block";}
'''

pet_cal_faqs_cn = [
    ("如何计算宠物的每日热量需求？", "使用RER公式（静息能量需求）：RER = 70 × 体重(kg)^0.75，然后乘以活动水平、生命阶段和绝育状态等系数得出每日需求热量(DER)。"),
    ("干粮和湿粮怎么换算？", "干粮约300-400 kcal/杯，湿粮（罐头）约80-120 kcal/100g。本计算器提供干粮估算，湿粮喂养请按包装热量标注换算。"),
    ("宠物肥胖怎么减肥？", "先计算理想体重的热量需求（而非当前体重），按80%喂食。每周减重不超过体重的1-2%。严重肥胖请咨询兽医制定专业减重计划。"),
]
pet_cal_faqs_en = [
    ("How do I calculate daily calorie needs for my pet?", "Use the RER formula (Resting Energy Requirement): RER = 70 × weight(kg)^0.75, then multiply by activity level, life stage, and neuter status factors to get Daily Energy Requirement (DER)."),
    ("How do I convert between dry and wet food?", "Dry food is ~300-400 kcal/cup; wet food (canned) is ~80-120 kcal/100g. This calculator estimates dry food portions — use packaging calorie information for wet food conversion."),
    ("How can I help my overweight pet lose weight?", "Calculate calorie needs based on ideal weight (not current weight), feed at 80%. Weekly weight loss should not exceed 1-2% of body weight. Consult a vet for severe obesity cases."),
]

# ============================================================
# 工具4: deck-cost - 露台建造成本估算器
# ============================================================
deck_cost_html_cn = '''
<div class="form-row"><div class="form-group"><label>露台面积 (平方米)</label><input type="number" id="area" placeholder="20" value="20" min="5" max="500"></div><div class="form-group"><label>材料类型</label><select id="material"><option value="pressure-treated">防腐木 (最经济)</option><option value="cedar" selected>雪松/红木 (中档)</option><option value="composite">复合板材 (高档)</option><option value="pvc">PVC塑料 (顶级)</option></select></div></div>
<div class="form-row"><div class="form-group"><label>露台高度</label><select id="height"><option value="low">地面层 (＜0.6m)</option><option value="mid" selected>低架 (0.6-1.8m)</option><option value="high">高架 (＞1.8m)</option></select></div><div class="form-group"><label>是否含楼梯</label><select id="stairs"><option value="no" selected>否</option><option value="yes">是</option></select></div></div>
<button class="btn-primary" onclick="calcDeckCost()">估算建造成本</button>
<div id="result" class="result-section" style="display:none;margin-top:20px">
<div class="result-grid" id="resultGrid"></div>
<div style="background:#0f172a;border-radius:10px;padding:20px;margin-top:16px;border:1px solid rgba(148,163,184,.1);color:#94a3b8;font-size:.85rem" id="breakdown"></div>
</div>
'''

deck_cost_html_en = deck_cost_html_cn.replace('露台面积 (平方米)', 'Deck Area (m²)').replace('材料类型', 'Material').replace('防腐木 (最经济)', 'Pressure-Treated (Budget)').replace('雪松/红木 (中档)', 'Cedar/Redwood (Mid-Range)').replace('复合板材 (高档)', 'Composite (Premium)').replace('PVC塑料 (顶级)', 'PVC (Luxury)').replace('露台高度', 'Deck Height').replace('地面层 (＜0.6m)', 'Ground Level (＜2ft)').replace('低架 (0.6-1.8m)', 'Low Rise (2-6ft)').replace('高架 (＞1.8m)', 'High Rise (＞6ft)').replace('是否含楼梯', 'Include Stairs?').replace('是', 'Yes').replace('估算建造成本', 'Estimate Deck Cost')

deck_cost_js = '''
function calcDeckCost(){var area=parseFloat(document.getElementById("area").value)||20;var mat=document.getElementById("material").value;var h=document.getElementById("height").value;var stairs=document.getElementById("stairs").value;
var matCost={};matCost["pressure-treated"]=25;matCost["cedar"]=45;matCost["composite"]=70;matCost["pvc"]=90;
var hFactor={};hFactor["low"]=1.0;hFactor["mid"]=1.3;hFactor["high"]=1.6;
var matTotal=area*matCost[mat];
var laborFactor=mat==="composite"||mat==="pvc"?1.4:1.0;
var laborTotal=area*30*laborFactor*hFactor[h];
var frameTotal=area*15*hFactor[h];
var stairCost=stairs==="yes"?2500:0;
var subTotal=matTotal+laborTotal+frameTotal+stairCost;
var permitFee=subTotal*0.05;
var grandTotal=Math.round(subTotal+permitFee);
var usdTotal=Math.round(grandTotal/7.2);
var matName={"pressure-treated":"防腐木","cedar":"雪松/红木","composite":"复合板材","pvc":"PVC塑料"};
document.getElementById("resultGrid").innerHTML='<div class="result-item"><div class="value">¥'+grandTotal.toLocaleString()+'</div><div class="label">估算总成本</div></div>'+'<div class="result-item"><div class="value">$'+usdTotal.toLocaleString()+'</div><div class="label">≈ 美元估算</div></div>'+'<div class="result-item"><div class="value">¥'+Math.round(grandTotal/area).toLocaleString()+'/m²</div><div class="label">每平米成本</div></div>'+'<div class="result-item"><div class="value">'+area+' m²</div><div class="label">总面积</div></div>';
document.getElementById("breakdown").innerHTML='<strong>成本明细：</strong><br>材料费 ('+matName[mat]+'): ¥'+Math.round(matTotal).toLocaleString()+'<br>人工费: ¥'+Math.round(laborTotal).toLocaleString()+'<br>框架结构: ¥'+Math.round(frameTotal).toLocaleString()+''+(stairs==="yes"?'<br>楼梯: ¥2,500':'')+'<br>许可证及其他 (5%): ¥'+Math.round(permitFee).toLocaleString()+'<br><small>注：此为估算值，实际成本因地区、施工复杂度而异。建议获取3份以上报价。</small>';
document.getElementById("result").style.display="block";}
'''

deck_cost_faqs_cn = [
    ("建造露台每平米成本多少？", "防腐木约¥250-400/m²，雪松/红木约¥500-800/m²，复合板材约¥800-1,200/m²，PVC约¥1,200-1,800/m²。含材料和人工，价格因地区差异较大。"),
    ("哪种材料性价比最高？", "防腐木初期成本最低但需每年刷漆维护（约¥300/年）；复合板材初期成本高但几乎免维护，长期性价比更高。雪松/红木是平衡选择。"),
    ("建露台需要许可证吗？", "大多数地区高度超过一定标准（通常0.6m）或面积超过一定范围（通常10m²）需要建筑许可证。请咨询当地住建部门确认。"),
]
deck_cost_faqs_en = [
    ("How much does building a deck cost per m²?", "Pressure-treated: ~$35-55/m², Cedar/Redwood: ~$70-110/m², Composite: ~$110-165/m², PVC: ~$165-250/m². Includes materials and labor; prices vary significantly by region."),
    ("Which material offers the best value?", "Pressure-treated has lowest upfront cost but requires annual maintenance. Composite costs more initially but is nearly maintenance-free, offering better long-term value. Cedar is a balanced choice."),
    ("Do I need a permit to build a deck?", "Most jurisdictions require permits for decks above certain heights (usually 2ft/0.6m) or areas. Check with your local building department before starting."),
]

# ============================================================
# 工具5: hvac-size - 空调/暖气容量计算器
# ============================================================
hvac_html_cn = '''
<div class="form-row"><div class="form-group"><label>房屋面积 (平方米)</label><input type="number" id="area" placeholder="100" value="100" min="10" max="1000"></div><div class="form-group"><label>层高 (米)</label><input type="number" id="ceiling" placeholder="2.8" value="2.8" min="2.2" max="6" step="0.1"></div></div>
<div class="form-row"><div class="form-group"><label>气候区域</label><select id="climate"><option value="cold">寒冷 (东北/北方)</option><option value="moderate" selected>温和 (中部)</option><option value="hot">炎热 (华南/南方)</option></select></div><div class="form-group"><label>房屋保温</label><select id="insulation"><option value="poor">差（老房子/无保温）</option><option value="average" selected>一般（普通住宅）</option><option value="good">好（节能建筑/新装修）</option></select></div></div>
<div class="form-row"><div class="form-group"><label>窗户朝向</label><select id="windows"><option value="low">少/北向</option><option value="average" selected>正常</option><option value="high">多/南向大窗</option></select></div><div class="form-group"><label>居住人数</label><input type="number" id="people" placeholder="3" value="3" min="1" max="20"></div></div>
<button class="btn-primary" onclick="calcHVAC()">计算推荐容量</button>
<div id="result" class="result-section" style="display:none;margin-top:20px">
<div class="result-grid" id="resultGrid"></div>
<div style="background:#0f172a;border-radius:10px;padding:20px;margin-top:16px;border:1px solid rgba(148,163,184,.1)">
<h3 style="color:#f1c40f;margin-bottom:12px">常见机型参考</h3><div id="modelRef" style="color:#94a3b8;font-size:.9rem;line-height:1.8"></div>
</div>
</div>
'''

hvac_html_en = hvac_html_cn.replace('房屋面积 (平方米)', 'Floor Area (m²)').replace('层高 (米)', 'Ceiling Height (m)').replace('气候区域', 'Climate Zone').replace('寒冷 (东北/北方)', 'Cold (Northern)').replace('温和 (中部)', 'Moderate (Central)').replace('炎热 (华南/南方)', 'Hot (Southern)').replace('房屋保温', 'Insulation Level').replace('差（老房子/无保温）', 'Poor (old/no insulation)').replace('一般（普通住宅）', 'Average (standard)').replace('好（节能建筑/新装修）', 'Good (energy-efficient)').replace('窗户朝向', 'Window Exposure').replace('少/北向', 'Few/North-facing').replace('多/南向大窗', 'Many/South-facing').replace('居住人数', 'Occupants').replace('计算推荐容量', 'Calculate Recommended Capacity').replace('常见机型参考', 'Common Unit Reference')

hvac_js = '''
function calcHVAC(){var area=parseFloat(document.getElementById("area").value)||100;var ceil=parseFloat(document.getElementById("ceiling").value)||2.8;var climate=document.getElementById("climate").value;var insul=document.getElementById("insulation").value;var win=document.getElementById("windows").value;var people=parseInt(document.getElementById("people").value)||3;
var volume=area*ceil;
var baseBTU=volume*35;
var cFactor={};cFactor["cold"]=1.15;cFactor["moderate"]=1.0;cFactor["hot"]=0.9;
var iFactor={};iFactor["poor"]=1.3;iFactor["average"]=1.0;iFactor["good"]=0.85;
var wFactor={};wFactor["low"]=0.9;wFactor["average"]=1.0;wFactor["high"]=1.15;
var coolingBTU=Math.round(baseBTU*cFactor[climate]*iFactor[insul]*wFactor[win]+people*600);
var heatingBTU=Math.round(coolingBTU*1.1);
var coolingKW=Math.round(coolingBTU/3412*10)/10;
var coolingTon=Math.round(coolingBTU/12000*10)/10;
var coolingHP=Math.round(coolingBTU/9000*10)/10;
document.getElementById("resultGrid").innerHTML='<div class="result-item"><div class="value">'+coolingBTU.toLocaleString()+'</div><div class="label">制冷量 (BTU/h)</div></div>'+'<div class="result-item"><div class="value">'+heatingBTU.toLocaleString()+'</div><div class="label">制热量 (BTU/h)</div></div>'+'<div class="result-item"><div class="value">'+coolingKW+'</div><div class="label">制冷量 (kW)</div></div>'+'<div class="result-item"><div class="value">'+coolingTon+'</div><div class="label">制冷吨数 (Ton)</div></div>'+'<div class="result-item"><div class="value">'+coolingHP+'</div><div class="label">≈ 匹数 (HP)</div></div>'+'<div class="result-item"><div class="value">'+volume.toLocaleString()+'</div><div class="label">空间体积 (m³)</div></div>';
var ref='';
if(coolingBTU<=9000)ref='1匹空调 (约2500W/9000BTU)，适用10-15m²小房间';
else if(coolingBTU<=12000)ref='1.5匹空调 (约3500W/12000BTU)，适用15-25m²卧室';
else if(coolingBTU<=18000)ref='2匹空调 (约5000W/18000BTU)，适用25-40m²客厅';
else if(coolingBTU<=24000)ref='3匹空调 (约7000W/24000BTU)，适用40-60m²大开间';
else if(coolingBTU<=36000)ref='5匹商用空调 (约10500W/36000BTU)，适用60-100m²商铺';
else ref='建议中央空调或多台分体机组合，咨询专业暖通公司设计';
document.getElementById("modelRef").textContent='推荐机型: '+ref;
document.getElementById("result").style.display="block";}
'''

hvac_faqs_cn = [
    ("空调匹数怎么选？", "匹数是对制冷量的通俗说法，1匹≈2500W/9000BTU。选择时考虑房间面积、朝向、层高、保温等因素。本计算器提供科学估算，建议再咨询专业暖通工程师。"),
    ("制冷量和制热量为什么不同？", "一般情况下制热需求比制冷约高10-20%，因为冬季室内外温差更大。如用热泵，低温环境下制热效率会下降，寒冷地区建议选择低温热泵机型。"),
    ("买大了或买小了有什么问题？", "容量过大：频繁启停、湿度控制差、耗电高；容量过小：持续运行仍达不到温度、压缩机过劳、寿命缩短。正确选型可节能20-30%。"),
]
hvac_faqs_en = [
    ("How do I choose the right AC capacity?", "Capacity is commonly measured in BTU/h or Tons. Selection depends on room area, ceiling height, insulation, window exposure, and climate. This calculator provides a scientific estimate; consult a professional HVAC engineer for final sizing."),
    ("Why are cooling and heating capacities different?", "Heating typically requires 10-20% more capacity than cooling due to larger indoor-outdoor temperature differences in winter. Heat pump efficiency drops in cold weather — consider low-temperature heat pump models in cold regions."),
    ("What happens if I choose the wrong size?", "Oversized: frequent cycling, poor humidity control, high energy bills. Undersized: runs continuously without reaching temperature, compressor overwork, shorter lifespan. Correct sizing can save 20-30% energy."),
]

# ============================================================
# 构建所有工具
# ============================================================

tools = [
    {
        'slug': 'keto-calculator',
        'title_cn': '生酮饮食宏量计算器',
        'title_en': 'Keto Diet Macro Calculator',
        'desc_cn': '免费在线生酮饮食宏量营养素计算器，根据体重身高年龄自动计算每日蛋白质、脂肪、碳水摄入量，含BMR/TDEE计算，3餐餐食建议。',
        'desc_en': 'Free online Keto Diet Macro Calculator. Calculates daily protein, fat, and carb intake based on weight, height, and age. Includes BMR/TDEE calculation and 3-meal plan suggestions.',
        'icon': '🥩',
        'cat_cn': '健康计算器',
        'cat_en': 'Health Calculators',
        'cat_anchor': 'health-calculators',
        'tool_html_cn': keto_html_cn,
        'tool_html_en': keto_html_en,
        'tool_js': keto_js,
        'faqs_cn': keto_faqs_cn,
        'faqs_en': keto_faqs_en,
    },
    {
        'slug': 'dog-age',
        'title_cn': '狗狗年龄计算器',
        'title_en': 'Dog Age to Human Years Calculator',
        'desc_cn': '免费在线狗狗年龄换算人类年龄计算器，按品种体型（小型/中型/大型/巨型犬）科学换算，含生命阶段判断和衰老倍数分析。',
        'desc_en': 'Free Dog Age to Human Years Calculator. Scientifically converts dog age by breed size (small/medium/large/giant). Includes life stage assessment and aging ratio analysis.',
        'icon': '🐕',
        'cat_cn': '生活计算器',
        'cat_en': 'Life Calculators',
        'cat_anchor': 'life-calculators',
        'tool_html_cn': dog_age_html_cn,
        'tool_html_en': dog_age_html_en,
        'tool_js': dog_age_js,
        'faqs_cn': dog_age_faqs_cn,
        'faqs_en': dog_age_faqs_en,
    },
    {
        'slug': 'pet-calorie',
        'title_cn': '宠物热量需求计算器',
        'title_en': 'Pet Calorie Needs Calculator',
        'desc_cn': '免费在线宠物每日热量计算器，支持狗狗和猫咪，根据体重、体型、绝育状态和活动水平自动计算RER/DER，含喂食量建议。',
        'desc_en': 'Free Pet Daily Calorie Calculator for dogs and cats. Automatically calculates RER/DER based on weight, body condition, neuter status, and activity level. Includes feeding quantity suggestions.',
        'icon': '🐾',
        'cat_cn': '生活计算器',
        'cat_en': 'Life Calculators',
        'cat_anchor': 'life-calculators',
        'tool_html_cn': pet_cal_html_cn,
        'tool_html_en': pet_cal_html_en,
        'tool_js': pet_cal_js,
        'faqs_cn': pet_cal_faqs_cn,
        'faqs_en': pet_cal_faqs_en,
    },
    {
        'slug': 'deck-cost',
        'title_cn': '露台建造成本计算器',
        'title_en': 'Deck Building Cost Estimator',
        'desc_cn': '免费在线露台建造成本估算器，按面积、材料（防腐木/雪松/复合/PVC）、高度和楼梯选项自动计算材料费+人工费+许可证总成本。',
        'desc_en': 'Free Deck Building Cost Estimator. Automatically calculates material, labor, and permit costs based on area, material type (pressure-treated/cedar/composite/PVC), height, and stair options.',
        'icon': '🏗️',
        'cat_cn': '建筑计算器',
        'cat_en': 'Construction Calculators',
        'cat_anchor': 'construction-calculators',
        'tool_html_cn': deck_cost_html_cn,
        'tool_html_en': deck_cost_html_en,
        'tool_js': deck_cost_js,
        'faqs_cn': deck_cost_faqs_cn,
        'faqs_en': deck_cost_faqs_en,
    },
    {
        'slug': 'hvac-size',
        'title_cn': '空调容量计算器',
        'title_en': 'HVAC Sizing Calculator',
        'desc_cn': '免费在线空调/暖气容量计算器，按房屋面积、层高、气候、保温和窗户朝向自动计算BTU/kW/匹数/吨数，含机型推荐。',
        'desc_en': 'Free HVAC Sizing Calculator. Calculates BTU/kW/HP/Ton based on floor area, ceiling height, climate zone, insulation, and window exposure. Includes unit type recommendations.',
        'icon': '❄️',
        'cat_cn': '建筑计算器',
        'cat_en': 'Construction Calculators',
        'cat_anchor': 'construction-calculators',
        'tool_html_cn': hvac_html_cn,
        'tool_html_en': hvac_html_en,
        'tool_js': hvac_js,
        'faqs_cn': hvac_faqs_cn,
        'faqs_en': hvac_faqs_en,
    },
]

for tool in tools:
    slug = tool['slug']
    print(f"Building: {slug}...")
    try:
        cn_path, en_path = builder.build_bilingual(**tool)
        print(f"  CN: {cn_path}")
        print(f"  EN: {en_path}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone! 5 tools created.")
