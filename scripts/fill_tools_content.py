#!/usr/bin/env python3
"""填充工具2-10的实际功能代码"""
import os

BASE = '/home/chison/tools-site'

TOOL_CONTENTS = {
    'terms-of-service-generator': {
        'zh': '''
<div class="input-section">
<h2>📋 填写信息</h2>
<div class="form-group"><label>网站/应用名称</label><input type="text" id="siteName" placeholder="例如：我的网站"></div>
<div class="form-group"><label>网站URL</label><input type="text" id="siteUrl" placeholder="https://example.com"></div>
<div class="form-group"><label>联系邮箱</label><input type="text" id="contactEmail" placeholder="admin@example.com"></div>
<div class="form-group"><label>业务类型</label><select id="bizType"><option value="website">网站</option><option value="app">移动应用</option><option value="saas">SaaS平台</option><option value="ecommerce">电商</option><option value="community">社区论坛</option></select></div>
<div class="form-group"><label>公司/个人名称</label><input type="text" id="companyName" placeholder="公司或个人名称"></div>
<div class="form-group"><label>所在地区</label><select id="region"><option value="cn">中国大陆</option><option value="us">美国</option><option value="eu">欧盟</option><option value="global">全球通用</option></select></div>
<div class="btn-row"><button class="btn btn-primary" id="generateBtn">📄 生成服务条款</button><button class="btn btn-secondary" id="copyBtn">📋 复制全文</button></div>
</div>
<div class="result-section" id="resultSection">
<h2>📝 生成的服务条款</h2>
<div style="background:#0f172a;border-radius:8px;padding:20px;max-height:500px;overflow-y:auto;font-size:.9rem;color:#e2e8f0;white-space:pre-wrap;border:1px solid rgba(148,163,184,.1)" id="tosOutput"></div>
</div>
<script>
document.getElementById('generateBtn').addEventListener('click',function(){
  var sn=document.getElementById('siteName').value.trim()||'本网站';
  var su=document.getElementById('siteUrl').value.trim()||'[网站URL]';
  var ce=document.getElementById('contactEmail').value.trim()||'[联系邮箱]';
  var bt=document.getElementById('bizType').value;
  var cn=document.getElementById('companyName').value.trim()||sn;
  var rg=document.getElementById('region').value;
  var date=new Date().toISOString().split('T')[0];
  var types={website:'网站',app:'移动应用程序',saas:'SaaS平台',ecommerce:'电子商务平台',community:'社区论坛'};
  var tos='# '+sn+' 服务条款\\n\\n最后更新日期：'+date+'\\n\\n';
  tos+='## 1. 接受条款\\n通过访问和使用'+sn+'（以下简称"本'+types[bt]+'"），即表示您同意遵守本服务条款。如果您不同意这些条款，请勿使用本服务。\\n\\n';
  tos+='## 2. 服务描述\\n'+sn+'提供在线工具服务，包括但不限于各类计算器、生成器和转换工具。我们保留随时修改或终止服务的权利，恕不另行通知。\\n\\n';
  tos+='## 3. 用户责任\\n用户在使用本服务时，不得：\\n- 违反任何适用法律法规\\n- 上传恶意代码或病毒\\n- 干扰或破坏本服务的正常运行\\n- 侵犯他人知识产权\\n- 进行任何形式的滥用行为\\n\\n';
  tos+='## 4. 知识产权\\n本服务的所有内容、设计和代码均受知识产权法保护。未经'+cn+'明确书面许可，不得复制、修改或分发本服务的任何部分。\\n\\n';
  tos+='## 5. 免责声明\\n本服务按"现状"提供，不作任何明示或暗示的保证。'+cn+'不对服务的可用性、准确性或可靠性作任何保证。使用本服务的风险由用户自行承担。\\n\\n';
  tos+='## 6. 责任限制\\n在法律允许的最大范围内，'+cn+'不对因使用或无法使用本服务而产生的任何直接、间接、附带、特殊或后果性损害承担责任。\\n\\n';
  tos+='## 7. 第三方链接\\n本服务可能包含指向第三方网站的链接。'+cn+'不对任何第三方网站的内容或隐私政策负责。\\n\\n';
  tos+='## 8. 隐私\\n'+cn+'尊重您的隐私。请参阅我们的隐私政策了解详细信息。我们不会收集个人身份信息，除非您主动提供。\\n\\n';
  tos+='## 9. 终止\\n'+cn+'保留在不事先通知的情况下，以任何理由终止或暂停任何用户访问本服务的权利。\\n\\n';
  tos+='## 10. 条款修改\\n'+cn+'保留随时修改本服务条款的权利。修改后的条款一经发布即生效。建议定期查看本页面。\\n\\n';
  tos+='## 11. 适用法律\\n';
  if(rg==='cn')tos+='本条款受中华人民共和国法律管辖，并依其解释。任何争议应提交有管辖权的人民法院解决。';
  else if(rg==='us')tos+='本条款受美国法律管辖，并依其解释。任何争议应提交有管辖权的联邦法院解决。';
  else if(rg==='eu')tos+='本条款受欧盟相关法律管辖。任何争议应首先尝试通过调解解决。';
  else tos+='本条款的解释和适用应遵循国际商业惯例。任何争议应首先通过友好协商解决。';
  tos+='\\n\\n## 12. 联系我们\\n如有任何问题，请通过以下方式联系我们：\\n- 邮箱：'+ce+'\\n- 网站：'+su;
  document.getElementById('tosOutput').textContent=tos;
  document.getElementById('resultSection').classList.add('show');
  showToast('服务条款已生成');
});
document.getElementById('copyBtn').addEventListener('click',function(){
  var text=document.getElementById('tosOutput').textContent;
  if(!text.trim()){showToast('请先生成条款');return;}
  navigator.clipboard.writeText(text).then(function(){showToast('已复制到剪贴板')}).catch(function(){showToast('复制失败，请手动复制')});
});
</script>
''',
        'en': '''
<div class="input-section">
<h2>📋 Fill Information</h2>
<div class="form-group"><label>Website/App Name</label><input type="text" id="siteName" placeholder="e.g. My Website"></div>
<div class="form-group"><label>Website URL</label><input type="text" id="siteUrl" placeholder="https://example.com"></div>
<div class="form-group"><label>Contact Email</label><input type="text" id="contactEmail" placeholder="admin@example.com"></div>
<div class="form-group"><label>Business Type</label><select id="bizType"><option value="website">Website</option><option value="app">Mobile App</option><option value="saas">SaaS Platform</option><option value="ecommerce">E-Commerce</option><option value="community">Community Forum</option></select></div>
<div class="form-group"><label>Company/Individual Name</label><input type="text" id="companyName" placeholder="Company or individual name"></div>
<div class="form-group"><label>Region</label><select id="region"><option value="us">United States</option><option value="eu">European Union</option><option value="global">Global</option><option value="cn">China</option></select></div>
<div class="btn-row"><button class="btn btn-primary" id="generateBtn">📄 Generate Terms</button><button class="btn btn-secondary" id="copyBtn">📋 Copy Text</button></div>
</div>
<div class="result-section" id="resultSection">
<h2>📝 Generated Terms of Service</h2>
<div style="background:#0f172a;border-radius:8px;padding:20px;max-height:500px;overflow-y:auto;font-size:.9rem;color:#e2e8f0;white-space:pre-wrap;border:1px solid rgba(148,163,184,.1)" id="tosOutput"></div>
</div>
<script>
document.getElementById('generateBtn').addEventListener('click',function(){
  var sn=document.getElementById('siteName').value.trim()||'this website';
  var su=document.getElementById('siteUrl').value.trim()||'[Website URL]';
  var ce=document.getElementById('contactEmail').value.trim()||'[Contact Email]';
  var bt=document.getElementById('bizType').value;
  var cn=document.getElementById('companyName').value.trim()||sn;
  var rg=document.getElementById('region').value;
  var date=new Date().toISOString().split('T')[0];
  var types={website:'Website',app:'Mobile Application',saas:'SaaS Platform',ecommerce:'E-Commerce Platform',community:'Community Forum'};
  var tos='# '+sn+' Terms of Service\\n\\nLast Updated: '+date+'\\n\\n';
  tos+='## 1. Acceptance of Terms\\nBy accessing and using '+sn+' (the "'+types[bt]+'"), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Service.\\n\\n';
  tos+='## 2. Description of Service\\n'+sn+' provides online tool services, including but not limited to various calculators, generators, and conversion tools. We reserve the right to modify or discontinue the Service at any time without notice.\\n\\n';
  tos+='## 3. User Responsibilities\\nUsers shall not:\\n- Violate any applicable laws or regulations\\n- Upload malicious code or viruses\\n- Interfere with or disrupt the Service\\n- Infringe upon intellectual property rights\\n- Engage in any form of abuse\\n\\n';
  tos+='## 4. Intellectual Property\\nAll content, design, and code of the Service are protected by intellectual property laws. Reproduction, modification, or distribution without express written permission from '+cn+' is prohibited.\\n\\n';
  tos+='## 5. Disclaimer\\nThe Service is provided "as is" without any warranties, express or implied. '+cn+' makes no warranties regarding availability, accuracy, or reliability. Use the Service at your own risk.\\n\\n';
  tos+='## 6. Limitation of Liability\\nTo the maximum extent permitted by law, '+cn+' shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use or inability to use the Service.\\n\\n';
  tos+='## 7. Third-Party Links\\nThe Service may contain links to third-party websites. '+cn+' is not responsible for the content or privacy practices of any third-party sites.\\n\\n';
  tos+='## 8. Privacy\\n'+cn+' respects your privacy. Please refer to our Privacy Policy for details. We do not collect personally identifiable information unless voluntarily provided.\\n\\n';
  tos+='## 9. Termination\\n'+cn+' reserves the right to terminate or suspend access to the Service for any reason, without prior notice.\\n\\n';
  tos+='## 10. Modifications to Terms\\n'+cn+' reserves the right to modify these Terms at any time. Modified terms become effective upon posting. We recommend checking this page periodically.\\n\\n';
  tos+='## 11. Governing Law\\n';
  if(rg==='us')tos+='These Terms shall be governed by and construed in accordance with the laws of the United States.';
  else if(rg==='eu')tos+='These Terms shall be governed by applicable EU laws. Disputes shall first be attempted through mediation.';
  else if(rg==='cn')tos+='These Terms shall be governed by the laws of China. Any disputes shall be submitted to the competent people\'s court.';
  else tos+='These Terms shall be interpreted in accordance with international commercial practices. Disputes shall first be resolved through friendly negotiation.';
  tos+='\\n\\n## 12. Contact Us\\nFor any questions, please contact us:\\n- Email: '+ce+'\\n- Website: '+su;
  document.getElementById('tosOutput').textContent=tos;
  document.getElementById('resultSection').classList.add('show');
  showToast('Terms generated');
});
document.getElementById('copyBtn').addEventListener('click',function(){
  var text=document.getElementById('tosOutput').textContent;
  if(!text.trim()){showToast('Please generate terms first');return;}
  navigator.clipboard.writeText(text).then(function(){showToast('Copied to clipboard')}).catch(function(){showToast('Copy failed, please copy manually')});
});
</script>
'''
    },
    'recipe-analyzer': {
        'zh': '''
<div class="input-section">
<h2>🍳 添加食材</h2>
<div class="form-row">
<div class="form-group"><label>食材名称</label><input type="text" id="ingredientName" placeholder="如：鸡胸肉、米饭"></div>
<div class="form-group"><label>用量(克)</label><input type="number" id="ingredientAmount" placeholder="100" min="1" value="100"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" id="addBtn">➕ 添加食材</button><button class="btn btn-secondary" id="clearBtn">🔄 清空</button></div>
</div>
<div class="input-section">
<h2>📋 食材清单</h2>
<div id="ingredientList" style="max-height:300px;overflow-y:auto"><p style="color:#64748b;text-align:center;padding:20px">暂无食材，请添加</p></div>
</div>
<div class="result-section" id="resultSection">
<h2>📊 营养分析</h2>
<div class="result-grid">
<div class="result-card"><div class="label">总热量</div><div class="value" id="totalCal">0 kcal</div></div>
<div class="result-card"><div class="label">蛋白质</div><div class="value" style="color:#4ade80" id="totalProtein">0 g</div></div>
<div class="result-card"><div class="label">脂肪</div><div class="value" style="color:#fbbf24" id="totalFat">0 g</div></div>
<div class="result-card"><div class="label">碳水</div><div class="value" style="color:#f87171" id="totalCarbs">0 g</div></div>
<div class="result-card"><div class="label">纤维</div><div class="value" id="totalFiber">0 g</div></div>
<div class="result-card"><div class="label">钠</div><div class="value" id="totalSodium">0 mg</div></div>
</div>
</div>
<script>
var db={rice:{name:'米饭',cal:116,protein:2.6,fat:0.3,carbs:25.9,fiber:0.3,sodium:2},
chicken_breast:{name:'鸡胸肉',cal:133,protein:31,fat:3.6,carbs:0,fiber:0,sodium:74},
egg:{name:'鸡蛋',cal:155,protein:13,fat:11,carbs:1.1,fiber:0,sodium:140},
broccoli:{name:'西兰花',cal:34,protein:2.8,fat:0.4,carbs:7,fiber:2.6,sodium:33},
tofu:{name:'豆腐',cal:76,protein:8,fat:4.8,carbs:1.9,fiber:0.3,sodium:7},
salmon:{name:'三文鱼',cal:208,protein:20,fat:13,carbs:0,fiber:0,sodium:59},
milk:{name:'牛奶',cal:61,protein:3.2,fat:3.3,carbs:4.8,fiber:0,sodium:44},
banana:{name:'香蕉',cal:89,protein:1.1,fat:0.3,carbs:23,fiber:2.6,sodium:1},
apple:{name:'苹果',cal:52,protein:0.3,fat:0.2,carbs:14,fiber:2.4,sodium:1},
pasta:{name:'意面',cal:131,protein:5,fat:1.1,carbs:25,fiber:1.8,sodium:1},
beef:{name:'牛肉',cal:250,protein:26,fat:15,carbs:0,fiber:0,sodium:63},
shrimp:{name:'虾仁',cal:99,protein:24,fat:0.3,carbs:0.2,fiber:0,sodium:111},
potato:{name:'土豆',cal:77,protein:2,fat:0.1,carbs:17,fiber:2.2,sodium:6},
spinach:{name:'菠菜',cal:23,protein:2.9,fat:0.4,carbs:3.6,fiber:2.2,sodium:79},
avocado:{name:'牛油果',cal:160,protein:2,fat:15,carbs:9,fiber:6.7,sodium:7},
carrot:{name:'胡萝卜',cal:41,protein:0.9,fat:0.2,carbs:10,fiber:2.8,sodium:69},
bread:{name:'全麦面包',cal:247,protein:13,fat:3.4,carbs:41,fiber:7,sodium:400},
yogurt:{name:'酸奶',cal:61,protein:3.5,fat:3.3,carbs:4.7,fiber:0,sodium:46},
oil:{name:'食用油',cal:884,protein:0,fat:100,carbs:0,fiber:0,sodium:0},
sugar:{name:'白砂糖',cal:387,protein:0,fat:0,carbs:100,fiber:0,sodium:1}};
var items=[];
function findFood(n){n=n.toLowerCase();for(var k in db){if(db[k].name===n||k===n.replace(/\\s/g,'_'))return k;}for(var k in db){if(k.indexOf(n)!==-1||db[k].name.indexOf(n)!==-1)return k;}return null;}
function updateTotals(){
  var cal=0,pro=0,fat=0,carb=0,fib=0,sod=0;
  items.forEach(function(it){var f=db[it.key];cal+=f.cal*it.amt/100;pro+=f.protein*it.amt/100;fat+=f.fat*it.amt/100;carb+=f.carbs*it.amt/100;fib+=f.fiber*it.amt/100;sod+=f.sodium*it.amt/100;});
  document.getElementById('totalCal').textContent=Math.round(cal)+' kcal';
  document.getElementById('totalProtein').textContent=pro.toFixed(1)+' g';
  document.getElementById('totalFat').textContent=fat.toFixed(1)+' g';
  document.getElementById('totalCarbs').textContent=carb.toFixed(1)+' g';
  document.getElementById('totalFiber').textContent=fib.toFixed(1)+' g';
  document.getElementById('totalSodium').textContent=Math.round(sod)+' mg';
}
function renderList(){
  var list=document.getElementById('ingredientList');
  var rs=document.getElementById('resultSection');
  if(items.length===0){list.innerHTML='<p style="color:#64748b;text-align:center;padding:20px">暂无食材，请添加</p>';rs.classList.remove('show');return;}
  var h='<table style="width:100%;border-collapse:collapse"><thead><tr style="border-bottom:1px solid rgba(148,163,184,.2)"><th style="padding:8px;text-align:left;color:#94a3b8;font-size:.85rem">食材</th><th style="padding:8px;text-align:right;color:#94a3b8;font-size:.85rem">用量</th><th style="padding:8px;text-align:right;color:#94a3b8;font-size:.85rem">热量</th><th></th></tr></thead><tbody>';
  items.forEach(function(it,i){
    var f=db[it.key];
    h+='<tr style="border-bottom:1px solid rgba(148,163,184,.05)"><td style="padding:8px">'+f.name+'</td><td style="padding:8px;text-align:right">'+it.amt+'g</td><td style="padding:8px;text-align:right;color:#22d3ee">'+Math.round(f.cal*it.amt/100)+' kcal</td><td style="padding:8px;text-align:center"><button class="btn btn-danger" style="padding:2px 8px;font-size:.75rem" onclick="removeItem('+i+')">✕</button></td></tr>';
  });
  h+='</tbody></table>';
  list.innerHTML=h;
  updateTotals();
  rs.classList.add('show');
}
document.getElementById('addBtn').addEventListener('click',function(){
  var n=document.getElementById('ingredientName').value.trim();
  var a=parseFloat(document.getElementById('ingredientAmount').value);
  if(!n||isNaN(a)||a<=0){showToast('请输入有效食材和用量');return;}
  var key=findFood(n);
  if(!key){showToast('未找到该食材，数据库持续更新中');return;}
  items.push({key:key,amt:a});
  document.getElementById('ingredientName').value='';
  document.getElementById('ingredientAmount').value='100';
  renderList();
});
document.getElementById('clearBtn').addEventListener('click',function(){items=[];renderList();showToast('已清空');});
function removeItem(i){items.splice(i,1);renderList();}
</script>
''',
        'en': '''
<div class="input-section">
<h2>🍳 Add Ingredient</h2>
<div class="form-row">
<div class="form-group"><label>Ingredient Name</label><input type="text" id="ingredientName" placeholder="e.g. chicken breast, rice"></div>
<div class="form-group"><label>Amount (g)</label><input type="number" id="ingredientAmount" placeholder="100" min="1" value="100"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" id="addBtn">➕ Add Ingredient</button><button class="btn btn-secondary" id="clearBtn">🔄 Clear All</button></div>
</div>
<div class="input-section">
<h2>📋 Ingredient List</h2>
<div id="ingredientList" style="max-height:300px;overflow-y:auto"><p style="color:#64748b;text-align:center;padding:20px">No ingredients yet, add some</p></div>
</div>
<div class="result-section" id="resultSection">
<h2>📊 Nutrition Analysis</h2>
<div class="result-grid">
<div class="result-card"><div class="label">Total Calories</div><div class="value" id="totalCal">0 kcal</div></div>
<div class="result-card"><div class="label">Protein</div><div class="value" style="color:#4ade80" id="totalProtein">0 g</div></div>
<div class="result-card"><div class="label">Fat</div><div class="value" style="color:#fbbf24" id="totalFat">0 g</div></div>
<div class="result-card"><div class="label">Carbs</div><div class="value" style="color:#f87171" id="totalCarbs">0 g</div></div>
<div class="result-card"><div class="label">Fiber</div><div class="value" id="totalFiber">0 g</div></div>
<div class="result-card"><div class="label">Sodium</div><div class="value" id="totalSodium">0 mg</div></div>
</div>
</div>
<script>
var db={rice:{name:'Rice',cal:116,protein:2.6,fat:0.3,carbs:25.9,fiber:0.3,sodium:2},
chicken_breast:{name:'Chicken Breast',cal:133,protein:31,fat:3.6,carbs:0,fiber:0,sodium:74},
egg:{name:'Egg',cal:155,protein:13,fat:11,carbs:1.1,fiber:0,sodium:140},
broccoli:{name:'Broccoli',cal:34,protein:2.8,fat:0.4,carbs:7,fiber:2.6,sodium:33},
tofu:{name:'Tofu',cal:76,protein:8,fat:4.8,carbs:1.9,fiber:0.3,sodium:7},
salmon:{name:'Salmon',cal:208,protein:20,fat:13,carbs:0,fiber:0,sodium:59},
milk:{name:'Milk',cal:61,protein:3.2,fat:3.3,carbs:4.8,fiber:0,sodium:44},
banana:{name:'Banana',cal:89,protein:1.1,fat:0.3,carbs:23,fiber:2.6,sodium:1},
apple:{name:'Apple',cal:52,protein:0.3,fat:0.2,carbs:14,fiber:2.4,sodium:1},
pasta:{name:'Pasta',cal:131,protein:5,fat:1.1,carbs:25,fiber:1.8,sodium:1},
beef:{name:'Beef',cal:250,protein:26,fat:15,carbs:0,fiber:0,sodium:63},
shrimp:{name:'Shrimp',cal:99,protein:24,fat:0.3,carbs:0.2,fiber:0,sodium:111},
potato:{name:'Potato',cal:77,protein:2,fat:0.1,carbs:17,fiber:2.2,sodium:6},
spinach:{name:'Spinach',cal:23,protein:2.9,fat:0.4,carbs:3.6,fiber:2.2,sodium:79},
avocado:{name:'Avocado',cal:160,protein:2,fat:15,carbs:9,fiber:6.7,sodium:7},
carrot:{name:'Carrot',cal:41,protein:0.9,fat:0.2,carbs:10,fiber:2.8,sodium:69},
bread:{name:'Whole Wheat Bread',cal:247,protein:13,fat:3.4,carbs:41,fiber:7,sodium:400},
yogurt:{name:'Yogurt',cal:61,protein:3.5,fat:3.3,carbs:4.7,fiber:0,sodium:46},
oil:{name:'Cooking Oil',cal:884,protein:0,fat:100,carbs:0,fiber:0,sodium:0},
sugar:{name:'Sugar',cal:387,protein:0,fat:0,carbs:100,fiber:0,sodium:1}};
var items=[];
function findFood(n){n=n.toLowerCase();for(var k in db){if(db[k].name.toLowerCase()===n||k===n.replace(/\\s/g,'_'))return k;}for(var k in db){if(k.indexOf(n)!==-1||db[k].name.toLowerCase().indexOf(n)!==-1)return k;}return null;}
function updateTotals(){
  var cal=0,pro=0,fat=0,carb=0,fib=0,sod=0;
  items.forEach(function(it){var f=db[it.key];cal+=f.cal*it.amt/100;pro+=f.protein*it.amt/100;fat+=f.fat*it.amt/100;carb+=f.carbs*it.amt/100;fib+=f.fiber*it.amt/100;sod+=f.sodium*it.amt/100;});
  document.getElementById('totalCal').textContent=Math.round(cal)+' kcal';
  document.getElementById('totalProtein').textContent=pro.toFixed(1)+' g';
  document.getElementById('totalFat').textContent=fat.toFixed(1)+' g';
  document.getElementById('totalCarbs').textContent=carb.toFixed(1)+' g';
  document.getElementById('totalFiber').textContent=fib.toFixed(1)+' g';
  document.getElementById('totalSodium').textContent=Math.round(sod)+' mg';
}
function renderList(){
  var list=document.getElementById('ingredientList');
  var rs=document.getElementById('resultSection');
  if(items.length===0){list.innerHTML='<p style="color:#64748b;text-align:center;padding:20px">No ingredients yet, add some</p>';rs.classList.remove('show');return;}
  var h='<table style="width:100%;border-collapse:collapse"><thead><tr style="border-bottom:1px solid rgba(148,163,184,.2)"><th style="padding:8px;text-align:left;color:#94a3b8;font-size:.85rem">Ingredient</th><th style="padding:8px;text-align:right;color:#94a3b8;font-size:.85rem">Amount</th><th style="padding:8px;text-align:right;color:#94a3b8;font-size:.85rem">Calories</th><th></th></tr></thead><tbody>';
  items.forEach(function(it,i){
    var f=db[it.key];
    h+='<tr style="border-bottom:1px solid rgba(148,163,184,.05)"><td style="padding:8px">'+f.name+'</td><td style="padding:8px;text-align:right">'+it.amt+'g</td><td style="padding:8px;text-align:right;color:#22d3ee">'+Math.round(f.cal*it.amt/100)+' kcal</td><td style="padding:8px;text-align:center"><button class="btn btn-danger" style="padding:2px 8px;font-size:.75rem" onclick="removeItem('+i+')">✕</button></td></tr>';
  });
  h+='</tbody></table>';
  list.innerHTML=h;
  updateTotals();
  rs.classList.add('show');
}
document.getElementById('addBtn').addEventListener('click',function(){
  var n=document.getElementById('ingredientName').value.trim();
  var a=parseFloat(document.getElementById('ingredientAmount').value);
  if(!n||isNaN(a)||a<=0){showToast('Please enter valid ingredient name and amount');return;}
  var key=findFood(n);
  if(!key){showToast('Ingredient not found, database is being updated');return;}
  items.push({key:key,amt:a});
  document.getElementById('ingredientName').value='';
  document.getElementById('ingredientAmount').value='100';
  renderList();
});
document.getElementById('clearBtn').addEventListener('click',function(){items=[];renderList();showToast('Cleared');});
function removeItem(i){items.splice(i,1);renderList();}
</script>
'''
    },
    'nutrition-analyzer': {
        'zh': '''
<div class="input-section">
<h2>🔍 查询食物营养</h2>
<div class="form-row">
<div class="form-group" style="flex:2"><label>搜索食物</label><input type="text" id="foodSearch" placeholder="输入食物名称搜索..."></div>
<div class="form-group" style="flex:1"><label>份量(克)</label><input type="number" id="servingSize" value="100" min="1"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" id="searchBtn">🔍 查询</button></div>
<div class="form-group" style="margin-top:12px"><label>快速选择</label><select id="quickSelect"><option value="">-- 选择常见食物 --</option><option value="rice">米饭 Rice</option><option value="chicken_breast">鸡胸肉 Chicken Breast</option><option value="egg">鸡蛋 Egg</option><option value="broccoli">西兰花 Broccoli</option><option value="tofu">豆腐 Tofu</option><option value="salmon">三文鱼 Salmon</option><option value="milk">牛奶 Milk</option><option value="banana">香蕉 Banana</option><option value="apple">苹果 Apple</option><option value="pasta">意面 Pasta</option><option value="beef">牛肉 Beef</option><option value="shrimp">虾仁 Shrimp</option><option value="potato">土豆 Potato</option><option value="spinach">菠菜 Spinach</option><option value="avocado">牛油果 Avocado</option><option value="carrot">胡萝卜 Carrot</option><option value="bread">全麦面包 Whole Wheat Bread</option><option value="yogurt">酸奶 Yogurt</option><option value="oil">食用油 Cooking Oil</option><option value="sugar">白砂糖 Sugar</option></select></div>
</div>
<div class="result-section" id="resultSection">
<h2>📊 <span id="resultName"></span> - 每<span id="resultServing">100</span>g营养成分</h2>
<div class="result-grid">
<div class="result-card"><div class="label">热量 Calories</div><div class="value" id="calVal">-</div><div class="sub">kcal</div></div>
<div class="result-card"><div class="label">蛋白质 Protein</div><div class="value" style="color:#4ade80" id="proVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">脂肪 Fat</div><div class="value" style="color:#fbbf24" id="fatVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">碳水 Carbs</div><div class="value" style="color:#f87171" id="carbVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">纤维 Fiber</div><div class="value" id="fibVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">钠 Sodium</div><div class="value" id="sodVal">-</div><div class="sub">mg</div></div>
</div>
</div>
<script>
var db={rice:{name:'米饭',cal:116,protein:2.6,fat:0.3,carbs:25.9,fiber:0.3,sodium:2},
chicken_breast:{name:'鸡胸肉',cal:133,protein:31,fat:3.6,carbs:0,fiber:0,sodium:74},
egg:{name:'鸡蛋',cal:155,protein:13,fat:11,carbs:1.1,fiber:0,sodium:140},
broccoli:{name:'西兰花',cal:34,protein:2.8,fat:0.4,carbs:7,fiber:2.6,sodium:33},
tofu:{name:'豆腐',cal:76,protein:8,fat:4.8,carbs:1.9,fiber:0.3,sodium:7},
salmon:{name:'三文鱼',cal:208,protein:20,fat:13,carbs:0,fiber:0,sodium:59},
milk:{name:'牛奶',cal:61,protein:3.2,fat:3.3,carbs:4.8,fiber:0,sodium:44},
banana:{name:'香蕉',cal:89,protein:1.1,fat:0.3,carbs:23,fiber:2.6,sodium:1},
apple:{name:'苹果',cal:52,protein:0.3,fat:0.2,carbs:14,fiber:2.4,sodium:1},
pasta:{name:'意面',cal:131,protein:5,fat:1.1,carbs:25,fiber:1.8,sodium:1},
beef:{name:'牛肉',cal:250,protein:26,fat:15,carbs:0,fiber:0,sodium:63},
shrimp:{name:'虾仁',cal:99,protein:24,fat:0.3,carbs:0.2,fiber:0,sodium:111},
potato:{name:'土豆',cal:77,protein:2,fat:0.1,carbs:17,fiber:2.2,sodium:6},
spinach:{name:'菠菜',cal:23,protein:2.9,fat:0.4,carbs:3.6,fiber:2.2,sodium:79},
avocado:{name:'牛油果',cal:160,protein:2,fat:15,carbs:9,fiber:6.7,sodium:7},
carrot:{name:'胡萝卜',cal:41,protein:0.9,fat:0.2,carbs:10,fiber:2.8,sodium:69},
bread:{name:'全麦面包',cal:247,protein:13,fat:3.4,carbs:41,fiber:7,sodium:400},
yogurt:{name:'酸奶',cal:61,protein:3.5,fat:3.3,carbs:4.7,fiber:0,sodium:46},
oil:{name:'食用油',cal:884,protein:0,fat:100,carbs:0,fiber:0,sodium:0},
sugar:{name:'白砂糖',cal:387,protein:0,fat:0,carbs:100,fiber:0,sodium:1}};
function findFood(n){n=n.toLowerCase();for(var k in db){if(k===n||db[k].name===n)return k;}for(var k in db){if(k.indexOf(n)!==-1||db[k].name.indexOf(n)!==-1)return k;}return null;}
function showResult(key){
  var f=db[key];
  var s=parseFloat(document.getElementById('servingSize').value)||100;
  var m=s/100;
  document.getElementById('resultName').textContent=f.name;
  document.getElementById('resultServing').textContent=s;
  document.getElementById('calVal').textContent=Math.round(f.cal*m)+' kcal';
  document.getElementById('proVal').textContent=(f.protein*m).toFixed(1)+' g';
  document.getElementById('fatVal').textContent=(f.fat*m).toFixed(1)+' g';
  document.getElementById('carbVal').textContent=(f.carbs*m).toFixed(1)+' g';
  document.getElementById('fibVal').textContent=(f.fiber*m).toFixed(1)+' g';
  document.getElementById('sodVal').textContent=Math.round(f.sodium*m)+' mg';
  document.getElementById('resultSection').classList.add('show');
}
document.getElementById('searchBtn').addEventListener('click',function(){
  var q=document.getElementById('foodSearch').value.trim();
  if(!q){showToast('请输入食物名称');return;}
  var key=findFood(q);
  if(!key){showToast('未找到该食物');return;}
  showResult(key);
});
document.getElementById('quickSelect').addEventListener('change',function(){
  var v=this.value;
  if(!v)return;
  showResult(v);
});
</script>
''',
        'en': '''
<div class="input-section">
<h2>🔍 Search Food Nutrition</h2>
<div class="form-row">
<div class="form-group" style="flex:2"><label>Search Food</label><input type="text" id="foodSearch" placeholder="Enter food name to search..."></div>
<div class="form-group" style="flex:1"><label>Serving (g)</label><input type="number" id="servingSize" value="100" min="1"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" id="searchBtn">🔍 Search</button></div>
<div class="form-group" style="margin-top:12px"><label>Quick Select</label><select id="quickSelect"><option value="">-- Select common food --</option><option value="rice">Rice</option><option value="chicken_breast">Chicken Breast</option><option value="egg">Egg</option><option value="broccoli">Broccoli</option><option value="tofu">Tofu</option><option value="salmon">Salmon</option><option value="milk">Milk</option><option value="banana">Banana</option><option value="apple">Apple</option><option value="pasta">Pasta</option><option value="beef">Beef</option><option value="shrimp">Shrimp</option><option value="potato">Potato</option><option value="spinach">Spinach</option><option value="avocado">Avocado</option><option value="carrot">Carrot</option><option value="bread">Whole Wheat Bread</option><option value="yogurt">Yogurt</option><option value="oil">Cooking Oil</option><option value="sugar">Sugar</option></select></div>
</div>
<div class="result-section" id="resultSection">
<h2>📊 <span id="resultName"></span> - Per <span id="resultServing">100</span>g</h2>
<div class="result-grid">
<div class="result-card"><div class="label">Calories</div><div class="value" id="calVal">-</div><div class="sub">kcal</div></div>
<div class="result-card"><div class="label">Protein</div><div class="value" style="color:#4ade80" id="proVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">Fat</div><div class="value" style="color:#fbbf24" id="fatVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">Carbs</div><div class="value" style="color:#f87171" id="carbVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">Fiber</div><div class="value" id="fibVal">-</div><div class="sub">g</div></div>
<div class="result-card"><div class="label">Sodium</div><div class="value" id="sodVal">-</div><div class="sub">mg</div></div>
</div>
</div>
<script>
var db={rice:{name:'Rice',cal:116,protein:2.6,fat:0.3,carbs:25.9,fiber:0.3,sodium:2},
chicken_breast:{name:'Chicken Breast',cal:133,protein:31,fat:3.6,carbs:0,fiber:0,sodium:74},
egg:{name:'Egg',cal:155,protein:13,fat:11,carbs:1.1,fiber:0,sodium:140},
broccoli:{name:'Broccoli',cal:34,protein:2.8,fat:0.4,carbs:7,fiber:2.6,sodium:33},
tofu:{name:'Tofu',cal:76,protein:8,fat:4.8,carbs:1.9,fiber:0.3,sodium:7},
salmon:{name:'Salmon',cal:208,protein:20,fat:13,carbs:0,fiber:0,sodium:59},
milk:{name:'Milk',cal:61,protein:3.2,fat:3.3,carbs:4.8,fiber:0,sodium:44},
banana:{name:'Banana',cal:89,protein:1.1,fat:0.3,carbs:23,fiber:2.6,sodium:1},
apple:{name:'Apple',cal:52,protein:0.3,fat:0.2,carbs:14,fiber:2.4,sodium:1},
pasta:{name:'Pasta',cal:131,protein:5,fat:1.1,carbs:25,fiber:1.8,sodium:1},
beef:{name:'Beef',cal:250,protein:26,fat:15,carbs:0,fiber:0,sodium:63},
shrimp:{name:'Shrimp',cal:99,protein:24,fat:0.3,carbs:0.2,fiber:0,sodium:111},
potato:{name:'Potato',cal:77,protein:2,fat:0.1,carbs:17,fiber:2.2,sodium:6},
spinach:{name:'Spinach',cal:23,protein:2.9,fat:0.4,carbs:3.6,fiber:2.2,sodium:79},
avocado:{name:'Avocado',cal:160,protein:2,fat:15,carbs:9,fiber:6.7,sodium:7},
carrot:{name:'Carrot',cal:41,protein:0.9,fat:0.2,carbs:10,fiber:2.8,sodium:69},
bread:{name:'Whole Wheat Bread',cal:247,protein:13,fat:3.4,carbs:41,fiber:7,sodium:400},
yogurt:{name:'Yogurt',cal:61,protein:3.5,fat:3.3,carbs:4.7,fiber:0,sodium:46},
oil:{name:'Cooking Oil',cal:884,protein:0,fat:100,carbs:0,fiber:0,sodium:0},
sugar:{name:'Sugar',cal:387,protein:0,fat:0,carbs:100,fiber:0,sodium:1}};
function findFood(n){n=n.toLowerCase();for(var k in db){if(k===n||db[k].name.toLowerCase()===n)return k;}for(var k in db){if(k.indexOf(n)!==-1||db[k].name.toLowerCase().indexOf(n)!==-1)return k;}return null;}
function showResult(key){
  var f=db[key];
  var s=parseFloat(document.getElementById('servingSize').value)||100;
  var m=s/100;
  document.getElementById('resultName').textContent=f.name;
  document.getElementById('resultServing').textContent=s;
  document.getElementById('calVal').textContent=Math.round(f.cal*m)+' kcal';
  document.getElementById('proVal').textContent=(f.protein*m).toFixed(1)+' g';
  document.getElementById('fatVal').textContent=(f.fat*m).toFixed(1)+' g';
  document.getElementById('carbVal').textContent=(f.carbs*m).toFixed(1)+' g';
  document.getElementById('fibVal').textContent=(f.fiber*m).toFixed(1)+' g';
  document.getElementById('sodVal').textContent=Math.round(f.sodium*m)+' mg';
  document.getElementById('resultSection').classList.add('show');
}
document.getElementById('searchBtn').addEventListener('click',function(){
  var q=document.getElementById('foodSearch').value.trim();
  if(!q){showToast('Please enter a food name');return;}
  var key=findFood(q);
  if(!key){showToast('Food not found');return;}
  showResult(key);
});
document.getElementById('quickSelect').addEventListener('change',function(){
  var v=this.value;
  if(!v)return;
  showResult(v);
});
</script>
'''
    },
    'gradient-extractor': {
        'zh': '''
<div class="input-section">
<h2>📷 上传图片提取渐变色</h2>
<div class="form-group"><input type="file" id="imageInput" accept="image/*"></div>
<div class="form-row">
<div class="form-group"><label>渐变类型</label><select id="gradientType"><option value="linear">线性渐变 Linear</option><option value="radial">径向渐变 Radial</option></select></div>
<div class="form-group"><label>渐变角度</label><select id="gradientAngle"><option value="to right">→ 从左到右</option><option value="to bottom">↓ 从上到下</option><option value="to bottom right">↘ 左上到右下</option><option value="to bottom left">↙ 右上到左下</option><option value="45deg">45°</option><option value="135deg">135°</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-success" id="copyCssBtn">📋 复制CSS代码</button></div>
</div>
<div class="input-section">
<h2>🎨 提取结果</h2>
<div class="preview-area" id="gradientPreview" style="min-height:120px;border-radius:8px"></div>
<div class="result-section show" style="margin-top:12px">
<div style="background:#0f172a;border-radius:8px;padding:12px;font-family:monospace;font-size:.9rem;color:#22d3ee;word-break:break-all" id="cssOutput">上传图片后自动提取</div>
</div>
<div class="preview-area" id="placeholderPreview"><p style="color:#64748b">请上传一张图片</p></div>
<canvas id="workCanvas" style="display:none"></canvas>
</div>
<script>
var canvas=document.getElementById('workCanvas'),ctx=canvas.getContext('2d');
var currentCss='';
document.getElementById('imageInput').addEventListener('change',function(e){
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){var img=new Image();img.onload=function(){extractColors(img);};img.src=ev.target.result;};
  reader.readAsDataURL(file);
});
function extractColors(img){
  canvas.width=Math.min(img.width,400);
  canvas.height=Math.min(img.height,400);
  var scale=Math.min(canvas.width/img.width,canvas.height/img.height);
  canvas.width=img.width*scale;canvas.height=img.height*scale;
  ctx.drawImage(img,0,0,canvas.width,canvas.height);
  var data=ctx.getImageData(0,0,canvas.width,canvas.height).data;
  var r=0,g=0,b=0,n=0;
  for(var i=0;i<data.length;i+=4){r+=data[i];g+=data[i+1];b+=data[i+2];n++;}
  var avgR=Math.round(r/n),avgG=Math.round(g/n),avgB=Math.round(b/n);
  // Sample colors from different regions
  var topR=0,topG=0,topB=0,tn=0,botR=0,botG=0,botB=0,bn=0;
  for(var i=0;i<data.length;i+=4){
    var y=Math.floor(i/4/canvas.width);
    if(y<canvas.height/3){topR+=data[i];topG+=data[i+1];topB+=data[i+2];tn++;}
    else if(y>canvas.height*2/3){botR+=data[i];botG+=data[i+1];botB+=data[i+2];bn++;}
  }
  var c1={r:Math.round(topR/tn),g:Math.round(topG/tn),b:Math.round(topB/tn)};
  var c2={r:Math.round(botR/bn),g:Math.round(botG/bn),b:Math.round(botB/bn)};
  var type=document.getElementById('gradientType').value;
  var angle=document.getElementById('gradientAngle').value;
  var css;
  if(type==='linear')css='background: linear-gradient('+angle+', rgb('+c1.r+','+c1.g+','+c1.b+'), rgb('+c2.r+','+c2.g+','+c2.b+'));';
  else css='background: radial-gradient(circle, rgb('+c1.r+','+c1.g+','+c1.b+'), rgb('+c2.r+','+c2.g+','+c2.b+'));';
  currentCss=css;
  document.getElementById('cssOutput').textContent=css;
  document.getElementById('gradientPreview').style.background=css.replace('background: ','');
  document.getElementById('placeholderPreview').style.display='none';
  showToast('渐变色已提取');
}
document.getElementById('gradientType').addEventListener('change',function(){if(currentCss)showToast('已切换类型，可重新上传或复制当前CSS');});
document.getElementById('copyCssBtn').addEventListener('click',function(){
  if(!currentCss){showToast('请先上传图片');return;}
  navigator.clipboard.writeText(currentCss).then(function(){showToast('CSS已复制')}).catch(function(){showToast('复制失败，请手动复制')});
});
</script>
''',
        'en': '''
<div class="input-section">
<h2>📷 Upload Image to Extract Gradient</h2>
<div class="form-group"><input type="file" id="imageInput" accept="image/*"></div>
<div class="form-row">
<div class="form-group"><label>Gradient Type</label><select id="gradientType"><option value="linear">Linear</option><option value="radial">Radial</option></select></div>
<div class="form-group"><label>Angle</label><select id="gradientAngle"><option value="to right">→ Left to Right</option><option value="to bottom">↓ Top to Bottom</option><option value="to bottom right">↘ Top-Left to Bottom-Right</option><option value="to bottom left">↙ Top-Right to Bottom-Left</option><option value="45deg">45°</option><option value="135deg">135°</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-success" id="copyCssBtn">📋 Copy CSS</button></div>
</div>
<div class="input-section">
<h2>🎨 Extracted Gradient</h2>
<div class="preview-area" id="gradientPreview" style="min-height:120px;border-radius:8px"></div>
<div class="result-section show" style="margin-top:12px">
<div style="background:#0f172a;border-radius:8px;padding:12px;font-family:monospace;font-size:.9rem;color:#22d3ee;word-break:break-all" id="cssOutput">Upload an image to extract colors</div>
</div>
<div class="preview-area" id="placeholderPreview"><p style="color:#64748b">Please upload an image</p></div>
<canvas id="workCanvas" style="display:none"></canvas>
</div>
<script>
var canvas=document.getElementById('workCanvas'),ctx=canvas.getContext('2d');
var currentCss='';
document.getElementById('imageInput').addEventListener('change',function(e){
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){var img=new Image();img.onload=function(){extractColors(img);};img.src=ev.target.result;};
  reader.readAsDataURL(file);
});
function extractColors(img){
  canvas.width=Math.min(img.width,400);
  canvas.height=Math.min(img.height,400);
  var scale=Math.min(canvas.width/img.width,canvas.height/img.height);
  canvas.width=img.width*scale;canvas.height=img.height*scale;
  ctx.drawImage(img,0,0,canvas.width,canvas.height);
  var data=ctx.getImageData(0,0,canvas.width,canvas.height).data;
  var topR=0,topG=0,topB=0,tn=0,botR=0,botG=0,botB=0,bn=0;
  for(var i=0;i<data.length;i+=4){
    var y=Math.floor(i/4/canvas.width);
    if(y<canvas.height/3){topR+=data[i];topG+=data[i+1];topB+=data[i+2];tn++;}
    else if(y>canvas.height*2/3){botR+=data[i];botG+=data[i+1];botB+=data[i+2];bn++;}
  }
  var c1={r:Math.round(topR/tn),g:Math.round(topG/tn),b:Math.round(topB/tn)};
  var c2={r:Math.round(botR/bn),g:Math.round(botG/bn),b:Math.round(botB/bn)};
  var type=document.getElementById('gradientType').value;
  var angle=document.getElementById('gradientAngle').value;
  var css;
  if(type==='linear')css='background: linear-gradient('+angle+', rgb('+c1.r+','+c1.g+','+c1.b+'), rgb('+c2.r+','+c2.g+','+c2.b+'));';
  else css='background: radial-gradient(circle, rgb('+c1.r+','+c1.g+','+c1.b+'), rgb('+c2.r+','+c2.g+','+c2.b+'));';
  currentCss=css;
  document.getElementById('cssOutput').textContent=css;
  document.getElementById('gradientPreview').style.background=css.replace('background: ','');
  document.getElementById('placeholderPreview').style.display='none';
  showToast('Gradient extracted');
}
document.getElementById('copyCssBtn').addEventListener('click',function(){
  if(!currentCss){showToast('Please upload an image first');return;}
  navigator.clipboard.writeText(currentCss).then(function(){showToast('CSS copied')}).catch(function(){showToast('Copy failed')});
});
</script>
'''
    }
}

PLACEHOLDER = '<!-- TOOL-SPECIFIC CONTENT PLACEHOLDER -->'

def apply():
    for slug, variants in TOOL_CONTENTS.items():
        for lang in ['zh', 'en']:
            if lang == 'zh':
                path = os.path.join(BASE, slug, 'index.html')
            else:
                path = os.path.join(BASE, 'en', slug, 'index.html')
            with open(path, 'r') as f:
                content = f.read()
            if PLACEHOLDER not in content:
                print(f'SKIP {path}: no placeholder')
                continue
            content = content.replace(PLACEHOLDER, variants[lang])
            with open(path, 'w') as f:
                f.write(content)
            print(f'OK {path}')

if __name__ == '__main__':
    apply()