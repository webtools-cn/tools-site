#!/usr/bin/env python3
"""修复 day-trading-calculator 的 low_interact 问题：添加交互表单"""
import os, re

SITE = '/home/chison/tools-site'

# CN版修复
cn_path = os.path.join(SITE, 'day-trading-calculator', 'index.html')
with open(cn_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 替换空的 #toolContent
old_tool = '<div id="toolContent"></div>'
new_tool = '''<div id="toolContent">
<div class="section"><h2>📊 交易信息</h2>
<div class="form-row"><div class="form-group"><label>交易类型</label><select id="tradeType"><option value="stock">股票</option><option value="crypto">加密货币</option><option value="forex">外汇</option></select></div>
<div class="form-group"><label>方向</label><select id="direction"><option value="long">做多</option><option value="short">做空</option></select></div></div>
<div class="form-row"><div class="form-group"><label>入场价格 ($)</label><input type="number" id="entryPrice" placeholder="如 150.00" step="any"></div>
<div class="form-group"><label>出场价格 ($)</label><input type="number" id="exitPrice" placeholder="如 155.00" step="any"></div></div>
<div class="form-row"><div class="form-group"><label>交易数量</label><input type="number" id="quantity" placeholder="如 100" step="any"></div>
<div class="form-group"><label>手续费 (%)</label><input type="number" id="fee" placeholder="如 0.1" step="any" value="0.1"></div></div>
<div class="btn-row"><button class="btn btn-primary" onclick="calculate()">📊 计算盈亏</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button></div></div>
<div class="section" id="resultSection" style="display:none"><h2>📋 计算结果</h2>
<div class="result-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div class="result-card"><div class="result-label">总投入</div><div class="result-value" id="totalCost">-</div></div>
<div class="result-card"><div class="result-label">总收入</div><div class="result-value" id="totalRevenue">-</div></div>
<div class="result-card"><div class="result-label">手续费</div><div class="result-value" id="totalFee">-</div></div>
<div class="result-card highlight"><div class="result-label">净盈亏</div><div class="result-value" id="netPnL">-</div></div>
<div class="result-card"><div class="result-label">盈亏比</div><div class="result-value" id="pnlRatio">-</div></div>
<div class="result-card"><div class="result-label">收益率</div><div class="result-value" id="returnRate">-</div></div></div>
<div class="btn-row" style="margin-top:12px"><button class="btn btn-secondary" onclick="copyResults()">📋 复制结果</button></div></div></div>'''

c = c.replace(old_tool, new_tool)

# 替换JS部分，添加实际逻辑
old_js = '''(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer=null;
function showToast(msg){var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity='0';},2000);}
function copyResults(){
  var labels=document.querySelectorAll('.result-label');
  var text=[];
  labels.forEach(function(label){
    var valEl=label.nextElementSibling;
    if(valEl&&valEl.classList.contains('result-value')){
      text.push(label.textContent+': '+valEl.textContent);
    }
  });
  var details=document.querySelectorAll('.detail-row');
  details.forEach(function(row){
    var lbl=row.querySelector('.detail-label');
    var val=row.querySelector('.detail-value');
    if(lbl&&val)text.push(lbl.textContent+': '+val.textContent);
  });
  if(text.length>0){navigator.clipboard.writeText(text.join('\\n')).then(function(){showToast('结果已复制 📋');});}
  else{showToast('没有可复制的结果');}
}

var TOOL_SLUG='day-trading-calculator';
var LANG='zh-CN';

})();'''

new_js = '''(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer=null;
function showToast(msg){var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity='0';},2000);}

window.calculate=function(){
  var entry=parseFloat(el('entryPrice').value);
  var exit=parseFloat(el('exitPrice').value);
  var qty=parseFloat(el('quantity').value);
  var feePct=parseFloat(el('fee').value)||0;
  var direction=el('direction').value;
  if(isNaN(entry)||isNaN(exit)||isNaN(qty)){showToast('请填写所有必填字段');return;}
  var totalCost=entry*qty;
  var totalRevenue=exit*qty;
  var fee=totalCost*(feePct/100)+totalRevenue*(feePct/100);
  var pnl;
  if(direction==='long'){pnl=(exit-entry)*qty-fee;}
  else{pnl=(entry-exit)*qty-fee;}
  var pnlRatio=Math.abs(pnl)/totalCost*100;
  var returnRate=pnl/totalCost*100;
  el('totalCost').textContent='$'+totalCost.toFixed(2);
  el('totalRevenue').textContent='$'+totalRevenue.toFixed(2);
  el('totalFee').textContent='$'+fee.toFixed(2);
  el('netPnL').textContent='$'+pnl.toFixed(2);
  el('pnlRatio').textContent=pnlRatio.toFixed(2)+'%';
  el('returnRate').textContent=returnRate.toFixed(2)+'%';
  el('resultSection').style.display='block';
  if(pnl>=0){el('netPnL').style.color='#10b981';}
  else{el('netPnL').style.color='#ef4444';}
};

window.clearAll=function(){
  el('entryPrice').value='';el('exitPrice').value='';el('quantity').value='';el('fee').value='0.1';
  el('resultSection').style.display='none';
};

window.copyResults=function(){
  var labels=document.querySelectorAll('#resultSection .result-label');
  var text=[];
  labels.forEach(function(label){
    var valEl=label.nextElementSibling;
    if(valEl&&valEl.classList.contains('result-value')){
      text.push(label.textContent+': '+valEl.textContent);
    }
  });
  if(text.length>0){navigator.clipboard.writeText(text.join('\\n')).then(function(){showToast('结果已复制 📋');});}
  else{showToast('没有可复制的结果');}
};

var TOOL_SLUG='day-trading-calculator';
var LANG='zh-CN';

})();'''

c = c.replace(old_js, new_js)

# 修复related-tools空div（之前batch脚本创建了空的）
c = c.replace('<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 相关工具推荐</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"></div></section>',
              '<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 相关工具推荐</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"><a href="/stock-average-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📉 股票均价计算器</a><a href="/compound-interest-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📈 复利计算器</a><a href="/profit-margin-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📊 利润率计算器</a></div></section>')

with open(cn_path, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ CN day-trading-calculator 修复完成")


# EN版修复
en_path = os.path.join(SITE, 'en', 'day-trading-calculator', 'index.html')
with open(en_path, 'r', encoding='utf-8') as f:
    c_en = f.read()

new_tool_en = '''<div id="toolContent">
<div class="section"><h2>📊 Trade Details</h2>
<div class="form-row"><div class="form-group"><label>Asset Type</label><select id="tradeType"><option value="stock">Stock</option><option value="crypto">Crypto</option><option value="forex">Forex</option></select></div>
<div class="form-group"><label>Direction</label><select id="direction"><option value="long">Long</option><option value="short">Short</option></select></div></div>
<div class="form-row"><div class="form-group"><label>Entry Price ($)</label><input type="number" id="entryPrice" placeholder="e.g. 150.00" step="any"></div>
<div class="form-group"><label>Exit Price ($)</label><input type="number" id="exitPrice" placeholder="e.g. 155.00" step="any"></div></div>
<div class="form-row"><div class="form-group"><label>Quantity</label><input type="number" id="quantity" placeholder="e.g. 100" step="any"></div>
<div class="form-group"><label>Fee (%)</label><input type="number" id="fee" placeholder="e.g. 0.1" step="any" value="0.1"></div></div>
<div class="btn-row"><button class="btn btn-primary" onclick="calculate()">📊 Calculate P&L</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button></div></div>
<div class="section" id="resultSection" style="display:none"><h2>📋 Results</h2>
<div class="result-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div class="result-card"><div class="result-label">Total Cost</div><div class="result-value" id="totalCost">-</div></div>
<div class="result-card"><div class="result-label">Total Revenue</div><div class="result-value" id="totalRevenue">-</div></div>
<div class="result-card"><div class="result-label">Fees</div><div class="result-value" id="totalFee">-</div></div>
<div class="result-card highlight"><div class="result-label">Net P&L</div><div class="result-value" id="netPnL">-</div></div>
<div class="result-card"><div class="result-label">P&L Ratio</div><div class="result-value" id="pnlRatio">-</div></div>
<div class="result-card"><div class="result-label">Return Rate</div><div class="result-value" id="returnRate">-</div></div></div>
<div class="btn-row" style="margin-top:12px"><button class="btn btn-secondary" onclick="copyResults()">📋 Copy Results</button></div></div></div>'''

c_en = c_en.replace('<div id="toolContent"></div>', new_tool_en)

new_js_en = '''(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer=null;
function showToast(msg){var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity='0';},2000);}

window.calculate=function(){
  var entry=parseFloat(el('entryPrice').value);
  var exit=parseFloat(el('exitPrice').value);
  var qty=parseFloat(el('quantity').value);
  var feePct=parseFloat(el('fee').value)||0;
  var direction=el('direction').value;
  if(isNaN(entry)||isNaN(exit)||isNaN(qty)){showToast('Please fill all required fields');return;}
  var totalCost=entry*qty;
  var totalRevenue=exit*qty;
  var fee=totalCost*(feePct/100)+totalRevenue*(feePct/100);
  var pnl;
  if(direction==='long'){pnl=(exit-entry)*qty-fee;}
  else{pnl=(entry-exit)*qty-fee;}
  var pnlRatio=Math.abs(pnl)/totalCost*100;
  var returnRate=pnl/totalCost*100;
  el('totalCost').textContent='$'+totalCost.toFixed(2);
  el('totalRevenue').textContent='$'+totalRevenue.toFixed(2);
  el('totalFee').textContent='$'+fee.toFixed(2);
  el('netPnL').textContent='$'+pnl.toFixed(2);
  el('pnlRatio').textContent=pnlRatio.toFixed(2)+'%';
  el('returnRate').textContent=returnRate.toFixed(2)+'%';
  el('resultSection').style.display='block';
  if(pnl>=0){el('netPnL').style.color='#10b981';}
  else{el('netPnL').style.color='#ef4444';}
};

window.clearAll=function(){
  el('entryPrice').value='';el('exitPrice').value='';el('quantity').value='';el('fee').value='0.1';
  el('resultSection').style.display='none';
};

window.copyResults=function(){
  var labels=document.querySelectorAll('#resultSection .result-label');
  var text=[];
  labels.forEach(function(label){
    var valEl=label.nextElementSibling;
    if(valEl&&valEl.classList.contains('result-value')){
      text.push(label.textContent+': '+valEl.textContent);
    }
  });
  if(text.length>0){navigator.clipboard.writeText(text.join('\\n')).then(function(){showToast('Results copied 📋');});}
  else{showToast('Nothing to copy');}
};

var TOOL_SLUG='day-trading-calculator';
var LANG='en';

})();'''

c_en = c_en.replace(old_js.replace('zh-CN','en').replace('数据不上传','data is processed locally').replace('结果已复制','Results copied'), new_js_en)

# Fix related-tools empty div in EN
c_en = c_en.replace('<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 Related Tools</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"></div></section>',
              '<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 Related Tools</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"><a href="/en/stock-average-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📉 Stock Average Calculator</a><a href="/en/compound-interest-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📈 Compound Interest Calculator</a><a href="/en/profit-margin-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📊 Profit Margin Calculator</a></div></section>')

# 修复EN版JS（因为替换模式变了，要精准匹配）
# 直接替换整个script块
import re as re_module
# 找到script块
script_match = re_module.search(r'<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', c_en, re_module.DOTALL)
if script_match:
    c_en = c_en[:script_match.start()] + '<script>\n' + new_js_en + '\n</script>' + c_en[script_match.end():]

with open(en_path, 'w', encoding='utf-8') as f:
    f.write(c_en)
print("✅ EN day-trading-calculator 修复完成")