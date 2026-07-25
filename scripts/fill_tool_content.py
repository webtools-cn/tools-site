#!/usr/bin/env python3
"""补充剩余7个工具的交互内容和JS"""
import os

# ===== rental-agreement-generator =====
RENTAL_CN = '''<div class="input-section" id="input">
  <h2>租赁协议信息</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">填写租赁相关信息，自动生成标准租赁协议（仅供参考）</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">租赁类型</p>
  <div class="template-select" id="typeSelect">
    <span class="template-opt active" data-type="house">房屋租赁</span>
    <span class="template-opt" data-type="equipment">设备租赁</span>
    <span class="template-opt" data-type="vehicle">车辆租赁</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>出租方（甲方）</label><input type="text" id="lessor" placeholder="姓名/公司名" value="张三"></div>
    <div class="input-group"><label>承租方（乙方）</label><input type="text" id="lessee" placeholder="姓名/公司名" value="李四"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>租赁物描述</label><input type="text" id="property" placeholder="如：XX市XX路XX号XX室" value="XX市XX路XX号XX室"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>月租金（元）</label><input type="number" id="rent" placeholder="3000" value="3000" min="0" step="0.01"></div>
    <div class="input-group"><label>押金（元）</label><input type="number" id="deposit" placeholder="3000" value="3000" min="0" step="0.01"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>租赁开始日期</label><input type="date" id="startDate" value="2026-08-01"></div>
    <div class="input-group"><label>租赁结束日期</label><input type="date" id="endDate" value="2027-07-31"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 重置</button>
    <button class="btn btn-primary" id="genBtn">📋 生成协议</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">协议预览</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 复制</button>
  </div>
</div>'''

RENTAL_EN = '''<div class="input-section" id="input">
  <h2>Rental Agreement Details</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Fill in rental details to generate a standard agreement (for reference only)</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Rental Type</p>
  <div class="template-select" id="typeSelect">
    <span class="template-opt active" data-type="house">House Rental</span>
    <span class="template-opt" data-type="equipment">Equipment Rental</span>
    <span class="template-opt" data-type="vehicle">Vehicle Rental</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Lessor (Party A)</label><input type="text" id="lessor" placeholder="Name/Company" value="John Smith"></div>
    <div class="input-group"><label>Lessee (Party B)</label><input type="text" id="lessee" placeholder="Name/Company" value="Jane Doe"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>Property Description</label><input type="text" id="property" placeholder="e.g., 123 Main St, Apt 4" value="123 Main St, Apt 4"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Monthly Rent ($)</label><input type="number" id="rent" placeholder="1000" value="1000" min="0" step="0.01"></div>
    <div class="input-group"><label>Deposit ($)</label><input type="number" id="deposit" placeholder="1000" value="1000" min="0" step="0.01"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Start Date</label><input type="date" id="startDate" value="2026-08-01"></div>
    <div class="input-group"><label>End Date</label><input type="date" id="endDate" value="2027-07-31"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
    <button class="btn btn-primary" id="genBtn">📋 Generate</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Agreement Preview</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 Copy</button>
  </div>
</div>'''

RENTAL_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var rtype="house";
var typeNames={house:{cn:"房屋租赁协议",en:"House Rental Agreement"},equipment:{cn:"设备租赁协议",en:"Equipment Rental Agreement"},vehicle:{cn:"车辆租赁协议",en:"Vehicle Rental Agreement"}};
function generate(){
  var lo=document.getElementById("lessor").value.trim()||"___";
  var le=document.getElementById("lessee").value.trim()||"___";
  var pr=document.getElementById("property").value.trim()||"___";
  var rt=parseFloat(document.getElementById("rent").value)||0;
  var dp=parseFloat(document.getElementById("deposit").value)||0;
  var sd=document.getElementById("startDate").value||"___";
  var ed=document.getElementById("endDate").value||"___";
  var isEN=document.documentElement.lang==="en";
  var tn=typeNames[rtype][isEN?"en":"cn"];
  var html='<div style="max-width:650px;margin:0 auto;text-align:left;line-height:2">';
  html+='<h2 style="text-align:center;margin-bottom:20px">'+tn+'</h2>';
  html+='<p>'+(isEN?'This Agreement is made on ':'本协议于 ')+new Date().toLocaleDateString()+(isEN?' between:':' 由以下双方签订：')+'</p>';
  html+='<p><strong>'+(isEN?'Party A (Lessor): ':'甲方（出租方）：')+'</strong>'+lo+'</p>';
  html+='<p><strong>'+(isEN?'Party B (Lessee): ':'乙方（承租方）：')+'</strong>'+le+'</p>';
  html+='<p><strong>'+(isEN?'1. Property: ':'1. 租赁物：')+'</strong>'+pr+'</p>';
  html+='<p><strong>'+(isEN?'2. Lease Term: ':'2. 租赁期限：')+'</strong>'+sd+(isEN?' to ':' 至 ')+ed+'</p>';
  html+='<p><strong>'+(isEN?'3. Rent: ':'3. 租金：')+'</strong>'+(isEN?'$':'¥')+rt.toFixed(2)+(isEN?' per month':'/月')+'</p>';
  html+='<p><strong>'+(isEN?'4. Deposit: ':'4. 押金：')+'</strong>'+(isEN?'$':'¥')+dp.toFixed(2)+'</p>';
  html+='<p>'+(isEN?'5. The lessee shall pay rent on time and maintain the property in good condition.':'5. 承租方应按时支付租金并保持租赁物完好。')+'</p>';
  html+='<p>'+(isEN?'6. This agreement is for reference only and does not constitute legal advice.':'6. 本协议仅供参考，不构成法律建议。')+'</p>';
  html+='<br><p>'+(isEN?'Lessor Signature: ___________':'甲方签字：___________')+'</p>';
  html+='<p>'+(isEN?'Lessee Signature: ___________':'乙方签字：___________')+'</p>';
  html+='<p>'+(isEN?'Date: ___________':'日期：___________')+'</p>';
  html+='</div>';
  document.getElementById("preview").innerHTML=html;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"Agreement generated!":"协议已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){var isEN=document.documentElement.lang==="en";document.getElementById("lessor").value=isEN?"John Smith":"张三";document.getElementById("lessee").value=isEN?"Jane Doe":"李四";document.getElementById("property").value=isEN?"123 Main St, Apt 4":"XX市XX路XX号XX室";document.getElementById("rent").value=isEN?"1000":"3000";document.getElementById("deposit").value=isEN?"1000":"3000";document.getElementById("startDate").value="2026-08-01";document.getElementById("endDate").value="2027-07-31";generate();showToast(isEN?"Reset!":"已重置！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("preview").innerText).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
document.getElementById("typeSelect").addEventListener("click",function(e){if(e.target.classList.contains("template-opt")){document.querySelectorAll("#typeSelect .template-opt").forEach(function(el){el.classList.remove("active")});e.target.classList.add("active");rtype=e.target.dataset.type;generate()}});
generate();
</script>'''

# ===== nda-generator =====
NDA_CN = '''<div class="input-section" id="input">
  <h2>保密协议信息</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">填写双方信息和保密条款，自动生成标准NDA（仅供参考）</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">NDA类型</p>
  <div class="template-select" id="typeSelect">
    <span class="template-opt active" data-type="oneway">单向NDA</span>
    <span class="template-opt" data-type="mutual">双向NDA</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>披露方</label><input type="text" id="discloser" placeholder="公司名称" value="ABC科技有限公司"></div>
    <div class="input-group"><label>接收方</label><input type="text" id="receiver" placeholder="公司名称" value="XYZ咨询公司"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>保密内容描述</label><textarea id="scope" style="min-height:80px">包括但不限于商业计划、技术方案、客户数据、财务信息、产品设计等非公开信息。</textarea></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>保密期限（年）</label><input type="number" id="term" value="3" min="1" max="99"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 重置</button>
    <button class="btn btn-primary" id="genBtn">🔒 生成NDA</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">NDA预览</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 复制</button>
  </div>
</div>'''

NDA_EN = '''<div class="input-section" id="input">
  <h2>NDA Details</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Fill in party details and confidentiality terms to generate a standard NDA (for reference only)</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">NDA Type</p>
  <div class="template-select" id="typeSelect">
    <span class="template-opt active" data-type="oneway">One-Way NDA</span>
    <span class="template-opt" data-type="mutual">Mutual NDA</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Disclosing Party</label><input type="text" id="discloser" placeholder="Company name" value="ABC Tech Inc."></div>
    <div class="input-group"><label>Receiving Party</label><input type="text" id="receiver" placeholder="Company name" value="XYZ Consulting LLC"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>Confidential Information Description</label><textarea id="scope" style="min-height:80px">Including but not limited to business plans, technical solutions, customer data, financial information, product designs and other non-public information.</textarea></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Confidentiality Term (Years)</label><input type="number" id="term" value="3" min="1" max="99"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
    <button class="btn btn-primary" id="genBtn">🔒 Generate NDA</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">NDA Preview</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 Copy</button>
  </div>
</div>'''

NDA_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var ndaType="oneway";
function generate(){
  var d=document.getElementById("discloser").value.trim()||"___";
  var r=document.getElementById("receiver").value.trim()||"___";
  var s=document.getElementById("scope").value.trim()||"___";
  var tr=parseInt(document.getElementById("term").value)||3;
  var isEN=document.documentElement.lang==="en";
  var ttl=isEN?(ndaType==="mutual"?"MUTUAL NON-DISCLOSURE AGREEMENT":"NON-DISCLOSURE AGREEMENT"):(ndaType==="mutual"?"双向保密协议":"单向保密协议");
  var html='<div style="max-width:650px;margin:0 auto;text-align:left;line-height:2">';
  html+='<h2 style="text-align:center;margin-bottom:20px">'+ttl+'</h2>';
  html+='<p>'+(isEN?'This NDA is entered into on ':'本保密协议于 ')+new Date().toLocaleDateString()+(isEN?' by and between:':' 由以下双方签订：')+'</p>';
  html+='<p><strong>'+(isEN?'Disclosing Party: ':'披露方：')+'</strong>'+d+'</p>';
  html+='<p><strong>'+(isEN?'Receiving Party: ':'接收方：')+'</strong>'+r+'</p>';
  html+='<p><strong>'+(isEN?'1. Confidential Information: ':'1. 保密信息：')+'</strong>'+s+'</p>';
  html+='<p><strong>'+(isEN?'2. Obligations: ':'2. 保密义务：')+'</strong>'+(isEN?'The Receiving Party shall maintain confidentiality and not disclose to third parties.':'接收方应严格保密，不得向任何第三方披露。')+'</p>';
  html+='<p><strong>'+(isEN?'3. Term: ':'3. 保密期限：')+'</strong>'+tr+(isEN?' years from the date of this Agreement.':' 年，自本协议签署之日起计算。')+'</p>';
  if(ndaType==="mutual") html+='<p>'+(isEN?'4. Both parties are bound by the same confidentiality obligations.':'4. 双方均受同等保密义务约束。')+'</p>';
  html+='<p>'+(isEN?'5. This NDA is for reference only and does not constitute legal advice.':'5. 本协议仅供参考，不构成法律建议。')+'</p>';
  html+='<br><p>'+(isEN?'Disclosing Party: ___________':'披露方签字：___________')+'</p>';
  html+='<p>'+(isEN?'Receiving Party: ___________':'接收方签字：___________')+'</p>';
  html+='<p>'+(isEN?'Date: ___________':'日期：___________')+'</p>';
  html+='</div>';
  document.getElementById("preview").innerHTML=html;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"NDA generated!":"NDA已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){var isEN=document.documentElement.lang==="en";document.getElementById("discloser").value=isEN?"ABC Tech Inc.":"ABC科技有限公司";document.getElementById("receiver").value=isEN?"XYZ Consulting LLC":"XYZ咨询公司";document.getElementById("scope").value=isEN?"Including but not limited to business plans, technical solutions, customer data, financial information, product designs and other non-public information.":"包括但不限于商业计划、技术方案、客户数据、财务信息、产品设计等非公开信息。";document.getElementById("term").value="3";generate();showToast(isEN?"Reset!":"已重置！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("preview").innerText).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
document.getElementById("typeSelect").addEventListener("click",function(e){if(e.target.classList.contains("template-opt")){document.querySelectorAll("#typeSelect .template-opt").forEach(function(el){el.classList.remove("active")});e.target.classList.add("active");ndaType=e.target.dataset.type;generate()}});
generate();
</script>'''

# ===== cookie-consent-banner =====
COOKIE_CN = '''<div class="input-section" id="input">
  <h2>横幅设置</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">自定义Cookie同意横幅的外观和文字</p>
  <div class="input-row">
    <div class="input-group"><label>横幅文字</label><input type="text" id="text" value="本网站使用Cookie来改善您的体验。继续使用即表示您同意我们的Cookie政策。"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>接受按钮文字</label><input type="text" id="acceptText" value="接受"></div>
    <div class="input-group"><label>拒绝按钮文字</label><input type="text" id="rejectText" value="拒绝"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>位置</label><select id="position"><option value="bottom" selected>底部</option><option value="top">顶部</option></select></div>
    <div class="input-group"><label>主题</label><select id="theme"><option value="dark" selected>深色</option><option value="light">浅色</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 重置</button>
    <button class="btn btn-primary" id="genBtn">🍪 生成代码</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">横幅预览</h2>
  <div id="bannerPreview" style="margin-bottom:16px"></div>
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">生成代码</h2>
  <div class="code-box" id="codeBox"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 复制代码</button>
  </div>
</div>'''

COOKIE_EN = '''<div class="input-section" id="input">
  <h2>Banner Settings</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Customize the appearance and text of your cookie consent banner</p>
  <div class="input-row">
    <div class="input-group"><label>Banner Text</label><input type="text" id="text" value="This website uses cookies to improve your experience. By continuing, you agree to our Cookie Policy."></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Accept Button Text</label><input type="text" id="acceptText" value="Accept"></div>
    <div class="input-group"><label>Reject Button Text</label><input type="text" id="rejectText" value="Reject"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Position</label><select id="position"><option value="bottom" selected>Bottom</option><option value="top">Top</option></select></div>
    <div class="input-group"><label>Theme</label><select id="theme"><option value="dark" selected>Dark</option><option value="light">Light</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
    <button class="btn btn-primary" id="genBtn">🍪 Generate Code</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Banner Preview</h2>
  <div id="bannerPreview" style="margin-bottom:16px"></div>
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Generated Code</h2>
  <div class="code-box" id="codeBox"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">📋 Copy Code</button>
  </div>
</div>'''

COOKIE_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function generate(){
  var text=document.getElementById("text").value.trim()||"";
  var acc=document.getElementById("acceptText").value.trim()||"Accept";
  var rej=document.getElementById("rejectText").value.trim()||"Reject";
  var pos=document.getElementById("position").value;
  var th=document.getElementById("theme").value;
  var isDark=th==="dark";
  var bg=isDark?"#1e293b":"#ffffff";
  var cl=isDark?"#e2e8f0":"#1e293b";
  var btnBg=isDark?"rgba(6,182,212,.2)":"#06b6d4";
  var btnCl=isDark?"#22d3ee":"#ffffff";
  var rejBg=isDark?"rgba(148,163,184,.1)":"#e2e8f0";
  var rejCl=isDark?"#94a3b8":"#475569";
  var topOrBottom=pos==="top"?"top:0":"bottom:0";
  // Preview
  document.getElementById("bannerPreview").innerHTML='<div style="position:relative;min-height:80px;background:#0f172a;border-radius:8px;overflow:hidden"><div style="position:absolute;'+topOrBottom+';left:0;right:0;background:'+bg+';color:'+cl+';padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.85rem"><span style="flex:1;min-width:200px">'+text+'</span><div style="display:flex;gap:8px"><button style="padding:6px 16px;border-radius:6px;border:1px solid '+rejCl+';background:'+rejBg+';color:'+rejCl+';cursor:pointer">'+rej+'</button><button style="padding:6px 16px;border-radius:6px;border:none;background:'+btnBg+';color:'+btnCl+';cursor:pointer">'+acc+'</button></div></div></div>';
  // Code
  var code='<!-- Cookie Consent Banner -->\\n<style>\\n.cookie-banner{position:fixed;'+topOrBottom+';left:0;right:0;background:'+bg+';color:'+cl+';padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.85rem;z-index:9999;box-shadow:0 -2px 10px rgba(0,0,0,.1)}\\n.cookie-banner .cookie-text{flex:1;min-width:200px}\\n.cookie-banner .cookie-btns{display:flex;gap:8px}\\n.cookie-btn-accept{padding:6px 16px;border-radius:6px;border:none;background:'+btnBg+';color:'+btnCl+';cursor:pointer}\\n.cookie-btn-reject{padding:6px 16px;border-radius:6px;border:1px solid '+rejCl+';background:'+rejBg+';color:'+rejCl+';cursor:pointer}\\n</style>\\n<div class="cookie-banner" id="cookieBanner">\\n  <span class="cookie-text">'+text+'</span>\\n  <div class="cookie-btns">\\n    <button class="cookie-btn-reject" onclick="document.getElementById(\'cookieBanner\').style.display=\'none\'">'+rej+'</button>\\n    <button class="cookie-btn-accept" onclick="document.getElementById(\'cookieBanner\').style.display=\'none\'">'+acc+'</button>\\n  </div>\\n</div>';
  document.getElementById("codeBox").textContent=code;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"Code generated!":"代码已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){var isEN=document.documentElement.lang==="en";document.getElementById("text").value=isEN?"This website uses cookies to improve your experience. By continuing, you agree to our Cookie Policy.":"本网站使用Cookie来改善您的体验。继续使用即表示您同意我们的Cookie政策。";document.getElementById("acceptText").value=isEN?"Accept":"接受";document.getElementById("rejectText").value=isEN?"Reject":"拒绝";document.getElementById("position").value="bottom";document.getElementById("theme").value="dark";generate();showToast(isEN?"Reset!":"已重置！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("codeBox").textContent).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
// Live update
["text","acceptText","rejectText","position","theme"].forEach(function(id){document.getElementById(id).addEventListener("input",generate);document.getElementById(id).addEventListener("change",generate)});
generate();
</script>'''

# ===== reverse-text =====
REVERSE_CN = '''<div class="input-section" id="input">
  <h2>文本翻转</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">选择翻转模式，输入文本实时查看翻转结果</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">翻转模式</p>
  <div class="template-select" id="modeSelect">
    <span class="template-opt active" data-mode="full">整段翻转</span>
    <span class="template-opt" data-mode="word">逐词翻转</span>
    <span class="template-opt" data-mode="line">逐行翻转</span>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:1"><label>输入文本</label><textarea id="inputText" style="min-height:180px" placeholder="在此粘贴文本...">Hello World
你好世界</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 清空</button>
    <button class="btn btn-primary" id="copyBtn">📋 复制结果</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">翻转结果</h2>
  <div class="code-box" id="output" style="min-height:180px"></div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="charCount">0</div><div class="lbl">字符数</div></div>
  </div>
</div>'''

REVERSE_EN = '''<div class="input-section" id="input">
  <h2>Reverse Text</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Choose a reversal mode and see results in real-time</p>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Reversal Mode</p>
  <div class="template-select" id="modeSelect">
    <span class="template-opt active" data-mode="full">Full Reversal</span>
    <span class="template-opt" data-mode="word">Word-by-Word</span>
    <span class="template-opt" data-mode="line">Line-by-Line</span>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:1"><label>Input Text</label><textarea id="inputText" style="min-height:180px" placeholder="Paste text here...">Hello World
你好世界</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Clear</button>
    <button class="btn btn-primary" id="copyBtn">📋 Copy Result</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Reversed Result</h2>
  <div class="code-box" id="output" style="min-height:180px"></div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="charCount">0</div><div class="lbl">Characters</div></div>
  </div>
</div>'''

REVERSE_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var mode="full";
function reverse(){
  var text=document.getElementById("inputText").value;
  var result="";
  if(mode==="full"){result=text.split("").reverse().join("")}
  else if(mode==="word"){result=text.split(/(\\s+)/).map(function(w){if(/\\s/.test(w))return w;return w.split("").reverse().join("")}).join("")}
  else if(mode==="line"){result=text.split("\\n").map(function(l){return l.split("").reverse().join("")}).join("\\n")}
  document.getElementById("output").textContent=result;
  document.getElementById("charCount").textContent=result.length;
}
document.getElementById("inputText").addEventListener("input",reverse);
document.getElementById("modeSelect").addEventListener("click",function(e){if(e.target.classList.contains("template-opt")){document.querySelectorAll("#modeSelect .template-opt").forEach(function(el){el.classList.remove("active")});e.target.classList.add("active");mode=e.target.dataset.mode;reverse()}});
document.getElementById("resetBtn").addEventListener("click",function(){document.getElementById("inputText").value="";reverse();showToast(document.documentElement.lang==="en"?"Cleared!":"已清空！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("output").textContent).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
reverse();
</script>'''

# ===== remove-duplicates =====
DEDUP_CN = '''<div class="input-section" id="input">
  <h2>文本去重</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">粘贴文本，按行去重，选择选项后点击去重</p>
  <div class="input-row" style="margin-bottom:8px">
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="keepFirst" checked> 保留首次出现</label>
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="ignoreBlank"> 忽略空行</label>
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="caseSensitive"> 区分大小写</label>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    <div class="input-group" style="flex:1"><label>输入文本</label><textarea id="inputText" style="min-height:180px" placeholder="每行一个条目...">苹果
香蕉
苹果
橘子
香蕉
葡萄</textarea></div>
    <div class="input-group" style="flex:1"><label>去重结果</label><textarea id="outputText" style="min-height:180px;background:#0f172a;color:#e2e8f0" readonly></textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 清空</button>
    <button class="btn btn-primary" id="copyBtn">📋 复制结果</button>
  </div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="beforeCount">0</div><div class="lbl">去重前行数</div></div>
    <div class="stat-item"><div class="num" id="afterCount">0</div><div class="lbl">去重后行数</div></div>
    <div class="stat-item"><div class="num" id="removedCount">0</div><div class="lbl">移除重复行</div></div>
  </div>
</div>'''

DEDUP_EN = '''<div class="input-section" id="input">
  <h2>Remove Duplicates</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Paste text, deduplicate by line with customizable options</p>
  <div class="input-row" style="margin-bottom:8px">
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="keepFirst" checked> Keep first occurrence</label>
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="ignoreBlank"> Ignore blank lines</label>
    <label style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:.85rem;cursor:pointer"><input type="checkbox" id="caseSensitive"> Case sensitive</label>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    <div class="input-group" style="flex:1"><label>Input Text</label><textarea id="inputText" style="min-height:180px" placeholder="One entry per line...">apple
banana
apple
orange
banana
grape</textarea></div>
    <div class="input-group" style="flex:1"><label>Deduplicated Result</label><textarea id="outputText" style="min-height:180px;background:#0f172a;color:#e2e8f0" readonly></textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Clear</button>
    <button class="btn btn-primary" id="copyBtn">📋 Copy Result</button>
  </div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="beforeCount">0</div><div class="lbl">Lines Before</div></div>
    <div class="stat-item"><div class="num" id="afterCount">0</div><div class="lbl">Lines After</div></div>
    <div class="stat-item"><div class="num" id="removedCount">0</div><div class="lbl">Removed</div></div>
  </div>
</div>'''

DEDUP_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function dedup(){
  var text=document.getElementById("inputText").value;
  var keepFirst=document.getElementById("keepFirst").checked;
  var ignoreBlank=document.getElementById("ignoreBlank").checked;
  var caseSensitive=document.getElementById("caseSensitive").checked;
  var lines=text.split("\\n");
  var beforeCount=lines.length;
  if(ignoreBlank) lines=lines.filter(function(l){return l.trim()!==""});
  var seen={},result=[];
  if(keepFirst){for(var i=0;i<lines.length;i++){var key=caseSensitive?lines[i]:lines[i].toLowerCase();if(!seen[key]){seen[key]=true;result.push(lines[i])}}}
  else{for(var i=lines.length-1;i>=0;i--){var key2=caseSensitive?lines[i]:lines[i].toLowerCase();if(!seen[key2]){seen[key2]=true;result.unshift(lines[i])}}}
  document.getElementById("outputText").value=result.join("\\n");
  document.getElementById("beforeCount").textContent=beforeCount;
  document.getElementById("afterCount").textContent=result.length;
  document.getElementById("removedCount").textContent=beforeCount-result.length;
}
document.getElementById("inputText").addEventListener("input",dedup);
["keepFirst","ignoreBlank","caseSensitive"].forEach(function(id){document.getElementById(id).addEventListener("change",dedup)});
document.getElementById("resetBtn").addEventListener("click",function(){document.getElementById("inputText").value="";dedup();showToast(document.documentElement.lang==="en"?"Cleared!":"已清空！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("outputText").value).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
dedup();
</script>'''

# ===== text-stats =====
STATS_CN = '''<div class="input-section" id="input">
  <h2>文本统计</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">输入文本，实时显示各项统计指标</p>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>输入文本</label><textarea id="inputText" style="min-height:200px" placeholder="在此粘贴或输入文本...">Hello World 你好世界！
这是第二行文本。
This is the third line.</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 清空</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">统计结果</h2>
  <div class="stat-row">
    <div class="stat-item"><div class="num" id="charTotal">0</div><div class="lbl">总字符数</div></div>
    <div class="stat-item"><div class="num" id="charNoSpace">0</div><div class="lbl">字符数(无空格)</div></div>
    <div class="stat-item"><div class="num" id="wordCount">0</div><div class="lbl">英文单词数</div></div>
    <div class="stat-item"><div class="num" id="cnCharCount">0</div><div class="lbl">中文字数</div></div>
  </div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="lineCount">0</div><div class="lbl">行数</div></div>
    <div class="stat-item"><div class="num" id="paraCount">0</div><div class="lbl">段落数</div></div>
    <div class="stat-item"><div class="num" id="punctCount">0</div><div class="lbl">标点符号数</div></div>
    <div class="stat-item"><div class="num" id="digitCount">0</div><div class="lbl">数字字符数</div></div>
  </div>
</div>'''

STATS_EN = '''<div class="input-section" id="input">
  <h2>Text Statistics</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Enter text to see real-time statistics</p>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>Input Text</label><textarea id="inputText" style="min-height:200px" placeholder="Paste or type text here...">Hello World 你好世界！
This is the second line.
This is the third line.</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Clear</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Statistics</h2>
  <div class="stat-row">
    <div class="stat-item"><div class="num" id="charTotal">0</div><div class="lbl">Total Characters</div></div>
    <div class="stat-item"><div class="num" id="charNoSpace">0</div><div class="lbl">Chars (no spaces)</div></div>
    <div class="stat-item"><div class="num" id="wordCount">0</div><div class="lbl">English Words</div></div>
    <div class="stat-item"><div class="num" id="cnCharCount">0</div><div class="lbl">Chinese Characters</div></div>
  </div>
  <div class="stat-row" style="margin-top:12px">
    <div class="stat-item"><div class="num" id="lineCount">0</div><div class="lbl">Lines</div></div>
    <div class="stat-item"><div class="num" id="paraCount">0</div><div class="lbl">Paragraphs</div></div>
    <div class="stat-item"><div class="num" id="punctCount">0</div><div class="lbl">Punctuation</div></div>
    <div class="stat-item"><div class="num" id="digitCount">0</div><div class="lbl">Digits</div></div>
  </div>
</div>'''

STATS_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function stats(){
  var text=document.getElementById("inputText").value;
  document.getElementById("charTotal").textContent=text.length;
  document.getElementById("charNoSpace").textContent=text.replace(/\\s/g,"").length;
  document.getElementById("wordCount").textContent=(text.match(/[a-zA-Z]+/g)||[]).length;
  document.getElementById("cnCharCount").textContent=(text.match(/[\\u4e00-\\u9fff\\u3400-\\u4dbf]/g)||[]).length;
  document.getElementById("lineCount").textContent=text.split("\\n").length;
  document.getElementById("paraCount").textContent=(text.split(/\\n\\s*\\n/).filter(function(p){return p.trim()}).length)||0;
  document.getElementById("punctCount").textContent=(text.match(/[.,!?;:'"()\\[\\]{{}}\\-—…《》「」、。，！？；：""''（）【】]/g)||[]).length;
  document.getElementById("digitCount").textContent=(text.match(/\\d/g)||[]).length;
}
document.getElementById("inputText").addEventListener("input",stats);
document.getElementById("resetBtn").addEventListener("click",function(){document.getElementById("inputText").value="";stats();showToast(document.documentElement.lang==="en"?"Cleared!":"已清空！")});
stats();
</script>'''

# ===== data-unit-converter =====
DATA_CN = '''<div class="input-section" id="input">
  <h2>数据单位转换</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">输入数值并选择单位，自动计算所有单位的对应值（二进制标准：1KB=1024B）</p>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>数值</label><input type="number" id="value" placeholder="输入数值" value="1" min="0" step="any"></div>
    <div class="input-group"><label>单位</label><select id="unit"><option value="bit">Bit</option><option value="byte" selected>Byte (B)</option><option value="kb">KB</option><option value="mb">MB</option><option value="gb">GB</option><option value="tb">TB</option><option value="pb">PB</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 重置</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">换算结果</h2>
  <div class="result-grid" id="resultGrid"></div>
</div>'''

DATA_EN = '''<div class="input-section" id="input">
  <h2>Data Unit Converter</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Enter a value and select unit. All conversions are calculated automatically (binary standard: 1KB=1024B)</p>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>Value</label><input type="number" id="value" placeholder="Enter value" value="1" min="0" step="any"></div>
    <div class="input-group"><label>Unit</label><select id="unit"><option value="bit">Bit</option><option value="byte" selected>Byte (B)</option><option value="kb">KB</option><option value="mb">MB</option><option value="gb">GB</option><option value="tb">TB</option><option value="pb">PB</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">Conversion Results</h2>
  <div class="result-grid" id="resultGrid"></div>
</div>'''

DATA_JS = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var units=["bit","byte","kb","mb","gb","tb","pb"];
var unitNames={bit:"Bit",byte:"Byte (B)",kb:"KB",mb:"MB",gb:"GB",tb:"TB",pb:"PB"};
var unitNamesCN={bit:"Bit (比特)",byte:"Byte (字节)",kb:"KB (千字节)",mb:"MB (兆字节)",gb:"GB (吉字节)",tb:"TB (太字节)",pb:"PB (拍字节)"};
var toByte={bit:1/8,byte:1,kb:1024,mb:1048576,gb:1073741824,tb:1099511627776,pb:1125899906842624};
function formatNum(n){if(n===0)return "0";if(Math.abs(n)<1e-15)return "0";if(Math.abs(n)>=1e15||(Math.abs(n)<0.01&&n!==0))return n.toExponential(4);return parseFloat(n.toPrecision(12)).toString()}
function convert(){
  var v=parseFloat(document.getElementById("value").value)||0;
  var u=document.getElementById("unit").value;
  var bytes=v*toByte[u];
  var isEN=document.documentElement.lang==="en";
  var names=isEN?unitNames:unitNamesCN;
  var grid=document.getElementById("resultGrid");
  var html="";
  for(var i=0;i<units.length;i++){var converted=bytes/toByte[units[i]];var hl=units[i]===u;html+='<div class="result-card'+(hl?' highlight':'')+'"><div class="label">'+names[units[i]]+'</div><div class="value">'+formatNum(converted)+'</div></div>'}
  grid.innerHTML=html;
}
document.getElementById("value").addEventListener("input",convert);
document.getElementById("unit").addEventListener("change",convert);
document.getElementById("resetBtn").addEventListener("click",function(){document.getElementById("value").value="1";document.getElementById("unit").value="byte";convert();showToast(document.documentElement.lang==="en"?"Reset!":"已重置！")});
convert();
</script>'''

# Map tool dir -> (CN content, EN content, JS)
TOOL_PARTS = {
    'rental-agreement-generator': (RENTAL_CN, RENTAL_EN, RENTAL_JS),
    'nda-generator': (NDA_CN, NDA_EN, NDA_JS),
    'cookie-consent-banner': (COOKIE_CN, COOKIE_EN, COOKIE_JS),
    'reverse-text': (REVERSE_CN, REVERSE_EN, REVERSE_JS),
    'remove-duplicates': (DEDUP_CN, DEDUP_EN, DEDUP_JS),
    'text-stats': (STATS_CN, STATS_EN, STATS_JS),
    'data-unit-converter': (DATA_CN, DATA_EN, DATA_JS),
}

for d, (cn_content, en_content, js) in TOOL_PARTS.items():
    # Update CN page
    with open(f'{d}/index.html', 'r', encoding='utf-8') as f:
        cn_html = f.read()
    cn_html = cn_html.replace('<!-- CONTENT_PLACEHOLDER_CN -->', cn_content)
    cn_html = cn_html.replace('<!-- JS_PLACEHOLDER_CN -->', js)
    with open(f'{d}/index.html', 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    # Update EN page
    with open(f'en/{d}/index.html', 'r', encoding='utf-8') as f:
        en_html = f.read()
    en_html = en_html.replace('<!-- CONTENT_PLACEHOLDER_EN -->', en_content)
    en_html = en_html.replace('<!-- JS_PLACEHOLDER_EN -->', js)
    with open(f'en/{d}/index.html', 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print(f'✅ Updated {d} (CN + EN)')

print('\nAll 7 tools updated with content and JS!')