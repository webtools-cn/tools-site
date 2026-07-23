#!/usr/bin/env python3
"""Build 2 new tools: reading-time + checklist-generator using template v3"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# Tool 1: reading-time (阅读时间估算)
# ============================================================
reading_time_html_cn = '''
<div class="form-group">
  <label>📝 输入文本</label>
  <textarea id="inputText" rows="8" placeholder="粘贴或输入需要估算阅读时间的文本..."></textarea>
</div>
<div class="form-row" style="display:flex;gap:12px;flex-wrap:wrap">
  <div class="form-group" style="flex:1;min-width:120px">
    <label>阅读速度</label>
    <select id="speed">
      <option value="200">慢速 (200词/分钟)</option>
      <option value="250" selected>正常 (250词/分钟)</option>
      <option value="300">快速 (300词/分钟)</option>
      <option value="400">精读 (400词/分钟)</option>
    </select>
  </div>
  <div class="form-group" style="flex:1;min-width:120px">
    <label>语言</label>
    <select id="lang">
      <option value="zh" selected>中文</option>
      <option value="en">英文</option>
    </select>
  </div>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="calcReadingTime()">⏱ 计算阅读时间</button>
  <button class="btn btn-secondary" onclick="clearAll()">🗑 清空</button>
</div>
<div id="resultArea" style="display:none">
  <div class="result-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:16px">
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">📖 阅读时间</div>
      <div id="readingTime" style="font-size:1.8rem;font-weight:700;color:#22d3ee">--</div>
    </div>
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">📊 总字数</div>
      <div id="totalWords" style="font-size:1.8rem;font-weight:700;color:#f1c40f">--</div>
    </div>
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">🔤 总字符</div>
      <div id="totalChars" style="font-size:1.8rem;font-weight:700;color:#4ade80">--</div>
    </div>
  </div>
  <div style="margin-top:12px;padding:16px;background:#0f172a;border-radius:10px;text-align:center">
    <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">⏰ 详细阅读时间</div>
    <div id="detailedTime" style="color:#94a3b8;font-size:.95rem"></div>
  </div>
</div>
'''

reading_time_html_en = '''
<div class="form-group">
  <label>📝 Input Text</label>
  <textarea id="inputText" rows="8" placeholder="Paste or type the text to estimate reading time..."></textarea>
</div>
<div class="form-row" style="display:flex;gap:12px;flex-wrap:wrap">
  <div class="form-group" style="flex:1;min-width:120px">
    <label>Reading Speed</label>
    <select id="speed">
      <option value="200">Slow (200 wpm)</option>
      <option value="250" selected>Normal (250 wpm)</option>
      <option value="300">Fast (300 wpm)</option>
      <option value="400">Speed Read (400 wpm)</option>
    </select>
  </div>
  <div class="form-group" style="flex:1;min-width:120px">
    <label>Language</label>
    <select id="lang">
      <option value="zh">Chinese</option>
      <option value="en" selected>English</option>
    </select>
  </div>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="calcReadingTime()">⏱ Calculate</button>
  <button class="btn btn-secondary" onclick="clearAll()">🗑 Clear</button>
</div>
<div id="resultArea" style="display:none">
  <div class="result-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:16px">
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">📖 Reading Time</div>
      <div id="readingTime" style="font-size:1.8rem;font-weight:700;color:#22d3ee">--</div>
    </div>
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">📊 Words</div>
      <div id="totalWords" style="font-size:1.8rem;font-weight:700;color:#f1c40f">--</div>
    </div>
    <div class="info-item" style="padding:16px;background:#0f172a;border-radius:10px;text-align:center">
      <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">🔤 Characters</div>
      <div id="totalChars" style="font-size:1.8rem;font-weight:700;color:#4ade80">--</div>
    </div>
  </div>
  <div style="margin-top:12px;padding:16px;background:#0f172a;border-radius:10px;text-align:center">
    <div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">⏰ Detailed</div>
    <div id="detailedTime" style="color:#94a3b8;font-size:.95rem"></div>
  </div>
</div>
'''

reading_time_js = '''
function calcReadingTime(){
  var text=document.getElementById("inputText").value;
  if(!text.trim()){showToast("请输入文本");return}
  var speed=parseInt(document.getElementById("speed").value);
  var lang=document.getElementById("lang").value;
  var totalChars=text.length;
  var totalWords;
  if(lang==="zh"){
    var clean=text.replace(/\\s+/g,"");
    var chineseChars=clean.match(/[\\u4e00-\\u9fff]/g);
    var chineseCount=chineseChars?chineseChars.length:0;
    var englishWords=text.replace(/[\\u4e00-\\u9fff]/g," ").trim().split(/\\s+/).filter(function(w){return w.length>0}).length;
    totalWords=chineseCount+englishWords;
    var zhMinutes=chineseCount/300;
    var enMinutes=englishWords/(speed/1.5);
    var totalMinutes=zhMinutes+enMinutes;
    var displayedMinutes=chineseCount/300+englishWords/speed;
    displayedMinutes=Math.max(totalMinutes,displayedMinutes);
    displayResult(displayedMinutes,totalWords,totalChars,lang,chineseCount,englishWords);
  }else{
    totalWords=text.trim().split(/\\s+/).filter(function(w){return w.length>0}).length;
    var minutes=totalWords/speed;
    displayResult(minutes,totalWords,totalChars,lang,totalWords,0);
  }
}
function displayResult(minutes,words,chars,lang,enWords,zhChars){
  var hrs=Math.floor(minutes/60);
  var mins=Math.round(minutes%60);
  var secs=Math.round((minutes-Math.floor(minutes))*60);
  var timeStr="";
  if(hrs>0)timeStr+=hrs+"小时"+(lang==="en"?"h ":"");
  if(mins>0||hrs>0)timeStr+=mins+"分钟"+(lang==="en"?"min ":"");
  timeStr+=secs+"秒"+(lang==="en"?"sec":"");
  if(lang==="en"){
    var display="";
    if(hrs>0)display+=hrs+"h ";
    if(mins>0||hrs>0)display+=mins+"min ";
    display+=secs+"sec";
    document.getElementById("readingTime").textContent=display;
  }else{
    document.getElementById("readingTime").textContent=timeStr;
  }
  document.getElementById("totalWords").textContent=words.toLocaleString();
  document.getElementById("totalChars").textContent=chars.toLocaleString();
  var detail="";
  if(lang==="zh"){
    detail="中文: "+zhChars+" 字 · 英文: "+enWords+" 词 · ";
    detail+="速度: "+document.getElementById("speed").options[document.getElementById("speed").selectedIndex].text;
  }else{
    detail=enWords+" words · ";
    detail+="Speed: "+document.getElementById("speed").options[document.getElementById("speed").selectedIndex].text;
  }
  document.getElementById("detailedTime").textContent=detail;
  document.getElementById("resultArea").style.display="block";
}
function clearAll(){
  document.getElementById("inputText").value="";
  document.getElementById("resultArea").style.display="none";
}
'''

faqs_cn_rt = [
    ('阅读时间如何计算？', '中文按300字/分钟估算，英文根据你选择的速度（默认250词/分钟）计算。中英文混排时分别计算后相加。'),
    ('为什么中文和英文阅读速度不同？', '中文信息密度高，阅读速度通常按字/分钟计算。英文按词/分钟计算。工具会自动识别并分别处理。'),
    ('数据安全吗？', '所有文本仅在浏览器本地处理，不会上传到任何服务器，请放心使用。'),
    ('支持哪些语言？', '主要支持中文和英文。其他语言按英文方式统计单词数。'),
]
faqs_en_rt = [
    ('How is reading time calculated?', 'Chinese text is estimated at 300 chars/min, English at your selected speed (default 250 wpm). Mixed text calculates each part separately.'),
    ('Why different speeds for Chinese and English?', 'Chinese has higher information density per character, so it uses chars/min. English uses words/min. The tool auto-detects and processes accordingly.'),
    ('Is my data safe?', 'All text is processed locally in your browser. Nothing is uploaded to any server.'),
    ('What languages are supported?', 'Primarily Chinese and English. Other languages are counted as words like English.'),
]

seo_cn_rt = '<h2>阅读时间估算工具</h2><p>阅读时间估算是内容创作者、博主和写作者的必备工具。通过输入文本内容，快速估算读者需要花费的阅读时间，帮助你优化文章长度和内容结构。</p><h3>为什么需要估算阅读时间？</h3><p>研究表明，显示阅读时间可以提高用户参与度。读者更倾向于点击标有阅读时间的文章，因为他们知道自己需要投入多少时间。</p><h3>如何使用</h3><p>只需粘贴文本，选择阅读速度（慢速200/正常250/快速300词每分钟），点击计算即可。支持中英文混排，自动识别语言类型。</p>'
seo_en_rt = '<h2>Reading Time Calculator</h2><p>A reading time estimator helps content creators, bloggers, and writers estimate how long it takes readers to consume their content. Optimize your article length and structure based on reading time data.</p><h3>Why Estimate Reading Time?</h3><p>Studies show that displaying estimated reading time increases user engagement. Readers are more likely to click on articles that show reading time because they know the time commitment upfront.</p><h3>How to Use</h3><p>Simply paste your text, select reading speed (Slow 200/Normal 250/Fast 300 wpm), and click Calculate. Supports mixed Chinese and English text with auto-detection.</p>'

# ============================================================
# Tool 2: checklist-generator (清单生成器)
# ============================================================
checklist_html_cn = '''
<div class="form-group">
  <label>📋 输入清单项目（每行一项）</label>
  <textarea id="checklistInput" rows="8" placeholder="输入清单项目，每行一项&#10;例如：&#10;购买食材&#10;完成报告&#10;回复邮件&#10;打电话给客户"></textarea>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="generateChecklist()">✅ 生成清单</button>
  <button class="btn btn-success" onclick="resetAll()">🔄 全部重置</button>
  <button class="btn btn-secondary" onclick="exportList()">📤 导出结果</button>
</div>
<div id="checklistResult" style="display:none;margin-top:16px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
    <div>
      <span style="color:#64748b;font-size:.85rem">进度: </span>
      <span id="progressText" style="color:#22d3ee;font-weight:600;font-size:.95rem">0/0</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <div style="background:#0f172a;border-radius:20px;height:8px;width:200px;overflow:hidden;border:1px solid rgba(148,163,184,.1)">
        <div id="progressBar" style="height:100%;width:0%;background:linear-gradient(90deg,#22d3ee,#4ade80);border-radius:20px;transition:width .3s"></div>
      </div>
      <span id="progressPct" style="color:#94a3b8;font-size:.8rem;min-width:40px">0%</span>
    </div>
  </div>
  <div id="checklistItems"></div>
  <div style="margin-top:12px;text-align:center">
    <span style="color:#64748b;font-size:.8rem">✅ 已完成: <span id="doneCount" style="color:#4ade80;font-weight:600">0</span></span>
    <span style="color:#475569;margin:0 8px">|</span>
    <span style="color:#64748b;font-size:.8rem">⏳ 待完成: <span id="pendingCount" style="color:#f1c40f;font-weight:600">0</span></span>
  </div>
</div>
'''

checklist_html_en = '''
<div class="form-group">
  <label>📋 Enter Checklist Items (one per line)</label>
  <textarea id="checklistInput" rows="8" placeholder="Enter checklist items, one per line&#10;Example:&#10;Buy groceries&#10;Complete report&#10;Reply to emails&#10;Call client"></textarea>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="generateChecklist()">✅ Generate</button>
  <button class="btn btn-success" onclick="resetAll()">🔄 Reset All</button>
  <button class="btn btn-secondary" onclick="exportList()">📤 Export</button>
</div>
<div id="checklistResult" style="display:none;margin-top:16px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
    <div>
      <span style="color:#64748b;font-size:.85rem">Progress: </span>
      <span id="progressText" style="color:#22d3ee;font-weight:600;font-size:.95rem">0/0</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <div style="background:#0f172a;border-radius:20px;height:8px;width:200px;overflow:hidden;border:1px solid rgba(148,163,184,.1)">
        <div id="progressBar" style="height:100%;width:0%;background:linear-gradient(90deg,#22d3ee,#4ade80);border-radius:20px;transition:width .3s"></div>
      </div>
      <span id="progressPct" style="color:#94a3b8;font-size:.8rem;min-width:40px">0%</span>
    </div>
  </div>
  <div id="checklistItems"></div>
  <div style="margin-top:12px;text-align:center">
    <span style="color:#64748b;font-size:.8rem">✅ Done: <span id="doneCount" style="color:#4ade80;font-weight:600">0</span></span>
    <span style="color:#475569;margin:0 8px">|</span>
    <span style="color:#64748b;font-size:.8rem">⏳ Pending: <span id="pendingCount" style="color:#f1c40f;font-weight:600">0</span></span>
  </div>
</div>
'''

checklist_js = '''
var checkItems=[];
function generateChecklist(){
  var input=document.getElementById("checklistInput").value;
  var lines=input.split("\\n").filter(function(l){return l.trim().length>0});
  if(lines.length===0){showToast("请输入至少一项");return}
  checkItems=lines.map(function(l,i){return{id:i,text:l.trim(),done:false}});
  renderChecklist();
  document.getElementById("checklistResult").style.display="block";
  updateProgress();
}
function renderChecklist(){
  var container=document.getElementById("checklistItems");
  var html="";
  for(var i=0;i<checkItems.length;i++){
    var item=checkItems[i];
    html+='<div class="checklist-item" style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:#0f172a;border-radius:8px;margin-bottom:8px;border:1px solid '+(item.done?'rgba(34,197,94,.2)':'rgba(148,163,184,.1)')+'">';
    html+='<input type="checkbox" id="cb_'+item.id+'" '+(item.done?'checked':'')+' onchange="toggleItem('+item.id+')" style="width:18px;height:18px;accent-color:#22d3ee;cursor:pointer">';
    html+='<label for="cb_'+item.id+'" style="flex:1;color:'+(item.done?'#4ade80':'#e2e8f0')+';text-decoration:'+(item.done?'line-through':'none')+';cursor:pointer;font-size:.95rem">'+escapeHtml(item.text)+'</label>';
    html+='<button class="copy-btn" onclick="removeItem('+item.id+')" title="删除" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:1.1rem;padding:4px">✕</button>';
    html+='</div>';
  }
  container.innerHTML=html;
  updateProgress();
}
function toggleItem(id){
  for(var i=0;i<checkItems.length;i++){
    if(checkItems[i].id===id){checkItems[i].done=!checkItems[i].done;break}
  }
  renderChecklist();
}
function removeItem(id){
  checkItems=checkItems.filter(function(item){return item.id!==id});
  if(checkItems.length===0){
    document.getElementById("checklistResult").style.display="none";
  }else{
    renderChecklist();
  }
}
function resetAll(){
  for(var i=0;i<checkItems.length;i++)checkItems[i].done=false;
  renderChecklist();
}
function updateProgress(){
  var total=checkItems.length;
  var done=0;
  for(var i=0;i<checkItems.length;i++){if(checkItems[i].done)done++}
  var pct=total>0?Math.round(done/total*100):0;
  document.getElementById("progressText").textContent=done+"/"+total;
  document.getElementById("progressBar").style.width=pct+"%";
  document.getElementById("progressPct").textContent=pct+"%";
  document.getElementById("doneCount").textContent=done;
  document.getElementById("pendingCount").textContent=total-done;
}
function exportList(){
  if(checkItems.length===0){showToast("没有清单可导出");return}
  var lines=[];
  for(var i=0;i<checkItems.length;i++){
    var item=checkItems[i];
    lines.push((item.done?"[x]":"[ ]")+" "+item.text);
  }
  var text=lines.join("\\n");
  navigator.clipboard.writeText(text).then(function(){showToast("已导出到剪贴板")})["catch"](function(){showToast("导出失败")});
}
function escapeHtml(str){
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
'''

faqs_cn_cl = [
    ('清单可以保存吗？', '目前为纯前端工具，数据保存在浏览器内存中。关闭页面后数据会丢失，建议导出保存。'),
    ('如何导出清单？', '点击"导出结果"按钮，清单将以Markdown格式复制到剪贴板（[x]已完成 / [ ]待完成）。'),
    ('最多支持多少项？', '没有数量限制，但建议每项简短明了，便于查看和管理。'),
    ('数据安全吗？', '所有数据仅在浏览器本地处理，不会上传到任何服务器。'),
]
faqs_en_cl = [
    ('Can I save my checklist?', 'This is a pure frontend tool. Data is stored in browser memory and will be lost on page close. Export to save.'),
    ('How to export?', 'Click "Export" to copy the checklist in Markdown format ([x] done / [ ] pending) to clipboard.'),
    ('Maximum items?', 'No limit, but keeping items short and clear is recommended for better readability.'),
    ('Is my data safe?', 'All data is processed locally in your browser. Nothing is uploaded to any server.'),
]

seo_cn_cl = '<h2>在线清单生成器</h2><p>免费在线清单工具，帮助你快速创建待办事项清单、购物清单、任务清单等。支持勾选标记完成状态、实时进度追踪、一键导出Markdown格式。</p><h3>适用场景</h3><ul><li>日常待办事项管理</li><li>购物清单</li><li>旅行打包清单</li><li>工作任务分解</li><li>学习计划检查</li></ul><h3>使用方法</h3><p>每行输入一项，点击生成即可创建交互式清单。点击复选框标记完成，实时进度条直观显示完成比例。支持删除单项和导出结果。</p>'
seo_en_cl = '<h2>Online Checklist Generator</h2><p>Create interactive checklists instantly. Perfect for todo lists, shopping lists, task management, travel packing, and work planning. Features real-time progress tracking and Markdown export.</p><h3>Use Cases</h3><ul><li>Daily task management</li><li>Shopping lists</li><li>Travel packing checklists</li><li>Work task breakdown</li><li>Study plan tracking</li></ul><h3>How to Use</h3><p>Enter one item per line, click Generate to create an interactive checklist. Check items to mark them done, view real-time progress bar, delete individual items, or export results.</p>'

# ============================================================
# Build both tools
# ============================================================
print("=" * 50)
print("Building Tool 1: reading-time")
print("=" * 50)

cn1, en1 = builder.build_bilingual(
    slug='reading-time',
    title_cn='⏱ 阅读时间估算',
    title_en='⏱ Reading Time Calculator',
    desc_cn='免费在线阅读时间估算工具。输入文本，快速估算阅读所需时间。支持中英文混排，多种阅读速度可选。',
    desc_en='Free online reading time calculator. Estimate how long it takes to read any text. Supports Chinese & English with adjustable reading speed.',
    icon='⏱',
    cat_cn='写作与内容',
    cat_en='Writing & Content',
    cat_anchor='writing-content',
    tool_html_cn=reading_time_html_cn,
    tool_html_en=reading_time_html_en,
    tool_js=reading_time_js,
    faqs_cn=faqs_cn_rt,
    faqs_en=faqs_en_rt,
    seo_cn=seo_cn_rt,
    seo_en=seo_en_rt,
)
print(f"  CN: {cn1}")
print(f"  EN: {en1}")

print()
print("=" * 50)
print("Building Tool 2: checklist-generator")
print("=" * 50)

cn2, en2 = builder.build_bilingual(
    slug='checklist-generator',
    title_cn='✅ 清单生成器',
    title_en='✅ Checklist Generator',
    desc_cn='免费在线交互式清单生成器。快速创建待办清单、购物清单、任务清单，支持进度追踪和一键导出。',
    desc_en='Free online interactive checklist generator. Create todo lists, shopping lists, task checklists with progress tracking and one-click export.',
    icon='✅',
    cat_cn='生产力工具',
    cat_en='Productivity',
    cat_anchor='productivity',
    tool_html_cn=checklist_html_cn,
    tool_html_en=checklist_html_en,
    tool_js=checklist_js,
    faqs_cn=faqs_cn_cl,
    faqs_en=faqs_en_cl,
    seo_cn=seo_cn_cl,
    seo_en=seo_en_cl,
)
print(f"  CN: {cn2}")
print(f"  EN: {en2}")

print()
print("=" * 50)
print("SUCCESS: Both tools built!")
print("=" * 50)
