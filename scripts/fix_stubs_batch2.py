#!/usr/bin/env python3
"""Fix stub functions in multiple tool pages - Batch 1"""
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_function(content, func_name, new_impl):
    """Replace a stub function with a real implementation"""
    # Match: function funcName() { ... coming soon ... }
    pattern = rf'function {re.escape(func_name)}\s*\([^)]*\)\s*\{{[^}}]*coming soon[^}}]*\}}'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_impl + content[match.end():]
        return content, True
    # Also try without "coming soon" - just replace the function
    pattern2 = rf'function {re.escape(func_name)}\s*\([^)]*\)\s*\{{'
    match2 = re.search(pattern2, content)
    if match2:
        # Find the closing brace
        brace_count = 0
        start = match2.start()
        i = match2.end() - 1
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    content = content[:start] + new_impl + content[i+1:]
                    return content, True
            i += 1
    return content, False

def fix_csv_transpose(content):
    """Fix csv-transpose: transposeCSV, clearCT, copyCTResult, downloadCT"""
    new_transpose = """function transposeCSV() {
  var input=document.getElementById('ctInput').value;
  if(!input.trim()){showToast('请输入CSV数据');return;}
  var delim=document.getElementById('ctDelim').value;
  var hasHeader=document.getElementById('ctHeader').checked;
  var lines=input.split('\\n').filter(function(l){return l.trim()!==''});
  if(lines.length===0){showToast('无有效数据');return;}
  var rows=lines.map(function(l){return l.split(delim)});
  var maxCols=Math.max.apply(null,rows.map(function(r){return r.length}));
  rows.forEach(function(r){while(r.length<maxCols)r.push('')});
  var transposed=[];
  for(var c=0;c<maxCols;c++){
    var newRow=[];
    for(var r=0;r<rows.length;r++){newRow.push(rows[r][c]||'')}
    transposed.push(newRow.join(delim));
  }
  var result=transposed.join('\\n');
  document.getElementById('ctResult').style.display='block';
  document.getElementById('ctOutput').textContent=result;
  showToast('转置完成: '+rows.length+'行x'+maxCols+'列 → '+maxCols+'行x'+rows.length+'列');
}"""
    content,_=replace_function(content,'transposeCSV',new_transpose)
    
    new_clear = """function clearCT() {
  document.getElementById('ctInput').value='';
  document.getElementById('ctResult').style.display='none';
  showToast('已清空');
}"""
    content,_=replace_function(content,'clearCT',new_clear)
    
    new_copy = """function copyCTResult() {
  var t=document.getElementById('ctOutput').textContent;
  navigator.clipboard.writeText(t).then(function(){showToast('已复制')}).catch(function(){showToast('复制失败')});
}"""
    content,_=replace_function(content,'copyCTResult',new_copy)
    
    new_download = """function downloadCT() {
  var t=document.getElementById('ctOutput').textContent;
  var blob=new Blob([t],{type:'text/csv'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='transposed.csv';a.click();
  URL.revokeObjectURL(a.href);showToast('已下载');
}"""
    content,_=replace_function(content,'downloadCT',new_download)
    return content

def fix_csv_splitter(content):
    """Fix csv-splitter: splitCSV, clearCS"""
    new_split = """function splitCSV() {
  var input=document.getElementById('csInput').value;
  if(!input.trim()){showToast('请输入CSV数据');return;}
  var delim=document.getElementById('csDelim').value;
  var splitBy=document.getElementById('csSplitBy').value;
  var num=parseInt(document.getElementById('csNum').value)||100;
  var keepHeader=document.getElementById('csHeader').checked;
  var lines=input.split('\\n');
  var header=keepHeader?lines[0]:null;
  var dataLines=keepHeader?lines.slice(1):lines;
  var chunks=[];
  if(splitBy==='rows'){
    for(var i=0;i<dataLines.length;i+=num){
      chunks.push(dataLines.slice(i,i+num));
    }
  }else{
    var perFile=Math.ceil(dataLines.length/num);
    for(var i=0;i<num;i++){
      chunks.push(dataLines.slice(i*perFile,(i+1)*perFile));
    }
  }
  var grid=document.getElementById('csGrid');
  var filesDiv=document.getElementById('csFiles');
  grid.innerHTML='';filesDiv.innerHTML='';
  var stats=document.createElement('div');stats.className='stat-row';
  stats.innerHTML='<span class="stat-label">总行数</span><span class="stat-value">'+dataLines.length+'</span>';
  grid.appendChild(stats);
  stats=document.createElement('div');stats.className='stat-row';
  stats.innerHTML='<span class="stat-label">分割文件数</span><span class="stat-value">'+chunks.length+'</span>';
  grid.appendChild(stats);
  chunks.forEach(function(chunk,idx){
    var content=header?header+'\\n'+chunk.join('\\n'):chunk.join('\\n');
    var blob=new Blob([content],{type:'text/csv'});
    var url=URL.createObjectURL(blob);
    var btn=document.createElement('button');
    btn.className='btn btn-success';btn.style.cssText='margin:4px';
    btn.textContent='下载文件 '+(idx+1)+' ('+chunk.length+'行)';
    btn.onclick=function(){var u=url;var b=btn;return function(){b.href=u;b.download='split_'+(idx+1)+'.csv';var a=document.createElement('a');a.href=u;a.download='split_'+(idx+1)+'.csv';a.click()}}();
    filesDiv.appendChild(btn);
  });
  document.getElementById('csResult').style.display='block';
  showToast('已分割为'+chunks.length+'个文件');
}"""
    content,_=replace_function(content,'splitCSV',new_split)
    
    new_clear = """function clearCS() {
  document.getElementById('csInput').value='';
  document.getElementById('csResult').style.display='none';
  showToast('已清空');
}"""
    content,_=replace_function(content,'clearCS',new_clear)
    return content

def fix_csv_diff(content):
    """Fix csv-diff: compare, applyFilter, clearCSV, loadFile, loadSample, exportHTML"""
    # Need to add a global var for diff data
    new_js = """var diffData=[];
function compare() {
  var a=document.getElementById('csvA').value;
  var b=document.getElementById('csvB').value;
  if(!a.trim()||!b.trim()){showToast('请输入两个CSV文件内容');return;}
  var delimEl=document.getElementById('delimiter');
  var delim=delimEl.value;
  if(delim==='auto'){delim=a.indexOf('\\t')>-1?'\\t':a.indexOf(';')>-1?';':','}
  var ignoreCase=document.getElementById('ignoreCase').checked;
  var ignoreWS=document.getElementById('ignoreWS').checked;
  var linesA=a.split('\\n').filter(function(l){return l.trim()!==''});
  var linesB=b.split('\\n').filter(function(l){return l.trim()!==''});
  function norm(s){s=ignoreCase?s.toLowerCase():s;s=ignoreWS?s.replace(/\\s+/g,' ').trim():s;return s}
  diffData=[];
  var maxLen=Math.max(linesA.length,linesB.length);
  for(var i=0;i<maxLen;i++){
    var rowA=i<linesA.length?linesA[i]:'';
    var rowB=i<linesB.length?linesB[i]:'';
    if(!rowA&&rowB){diffData.push({type:'added',line:i+1,a:'',b:rowB})}
    else if(rowA&&!rowB){diffData.push({type:'removed',line:i+1,a:rowA,b:''})}
    else if(norm(rowA)!==norm(rowB)){diffData.push({type:'modified',line:i+1,a:rowA,b:rowB})}
  }
  document.getElementById('diffStats').textContent='共'+diffData.length+'处差异';
  document.getElementById('exportBtn').disabled=false;
  applyFilter();
  showToast('对比完成: '+diffData.length+'处差异');
}

function applyFilter() {
  var filter=document.getElementById('filterType').value;
  var result=document.getElementById('diffResult');
  var filtered=filter==='all'?diffData:diffData.filter(function(d){return d.type===filter});
  if(filtered.length===0){result.innerHTML='<div style="text-align:center;color:#64748b;padding:20px">没有差异</div>';return}
  var html='';
  filtered.forEach(function(d){
    var cls=d.type==='added'?'diff-added':d.type==='removed'?'diff-removed':'diff-modified';
    var label=d.type==='added'?'新增':d.type==='removed'?'删除':'修改';
    html+='<div style="margin:4px 0"><span class="'+cls+'">['+label+' 第'+d.line+'行]</span> ';
    if(d.type==='added'){html+=d.b}
    else if(d.type==='removed'){html+=d.a}
    else{html+='<br>A: '+d.a+'<br>B: '+d.b}
    html+='</div>';
  });
  result.innerHTML=html;
}

function clearCSV() {
  document.getElementById('csvA').value='';
  document.getElementById('csvB').value='';
  document.getElementById('diffResult').innerHTML='上传两个CSV文件后点击对比';
  document.getElementById('diffStats').textContent='';
  document.getElementById('exportBtn').disabled=true;
  diffData=[];
  showToast('已清除');
}

function loadFile(input,targetId) {
  var file=input.files[0];
  if(!file)return;
  var reader=new FileReader();
  reader.onload=function(e){document.getElementById(targetId).value=e.target.result;showToast('文件已加载')};
  reader.readAsText(file);
}

function loadSample() {
  document.getElementById('csvA').value='id,name,score\\n1,Alice,85\\n2,Bob,90\\n3,Carol,78';
  document.getElementById('csvB').value='id,name,score\\n1,Alice,85\\n2,Bob,95\\n4,Dave,92\\n3,Carol,78';
  showToast('示例已加载');
}

function exportHTML() {
  if(diffData.length===0){showToast('没有差异可导出');return}
  var html='<!DOCTYPE html><html><head><meta charset="UTF-8"><title>CSV Diff Report</title>';
  html+='<style>body{font-family:monospace;padding:20px}.added{color:green}.removed{color:red}.modified{color:orange}</style>';
  html+='</head><body><h1>CSV差异对比报告</h1><p>共'+diffData.length+'处差异</p>';
  diffData.forEach(function(d){
    var cls=d.type==='added'?'added':d.type==='removed'?'removed':'modified';
    html+='<p class="'+cls+'">['+d.type+' 第'+d.line+'行] '+d.a+' → '+d.b+'</p>';
  });
  html+='</body></html>';
  var blob=new Blob([html],{type:'text/html'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='diff_report.html';a.click();
  URL.revokeObjectURL(a.href);showToast('报告已导出');
}"""
    # Replace all stub functions
    for func in ['applyFilter','compare','exportHTML','loadFile','loadSample','clearCSV']:
        pattern = rf'function {re.escape(func)}\s*\([^)]*\)\s*\{{[^}}]*\}}'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    # Insert new JS before the closing script tag
    content = content.replace('</script>', new_js + '\n</script>')
    return content

def fix_sleep_calculator(content):
    """Fix sleep-calculator: calcBedtime, calcWakeTime + add switchMode"""
    new_js = """var currentMode='bedtime';
function switchMode(mode){
  currentMode=mode;
  document.querySelectorAll('.mode-btn').forEach(function(b){b.classList.remove('active')});
  document.querySelector('[data-mode="'+mode+'"]').classList.add('active');
  document.getElementById('panel-bedtime').style.display=mode==='bedtime'?'block':'none';
  document.getElementById('panel-waketime').style.display=mode==='waketime'?'block':'none';
}

function calcBedtime() {
  var wakeTime=document.getElementById('wakeTime').value;
  if(!wakeTime){showToast('请选择起床时间');return;}
  var fallAsleep=parseInt(document.getElementById('fallAsleepTime').value);
  var cycleSelect=document.querySelector('#bedtimeCycles input:checked');
  var cycles=cycleSelect?parseInt(cycleSelect.value):5;
  var parts=wakeTime.split(':');
  var wake=new Date();
  wake.setHours(parseInt(parts[0]),parseInt(parts[1]),0,0);
  var results=document.getElementById('bedtimeResults');
  results.innerHTML='';
  var cycleMin=90;
  for(var c=6;c>=4;c--){
    var totalMin=c*cycleMin+fallAsleep;
    var bedTime=new Date(wake.getTime()-totalMin*60000);
    var h=bedTime.getHours().toString().padStart(2,'0');
    var m=bedTime.getMinutes().toString().padStart(2,'0');
    var isBest=c===cycles;
    var card=document.createElement('div');
    card.className='result-card'+(isBest?' best':'');
    card.innerHTML='<div class="time">'+h+':'+m+'</div><div class="label">'+c+'个周期 ('+(c*1.5)+'小时)</div>'+(isBest?'<div class="cycle-note">推荐</div>':'');
    results.appendChild(card);
  }
  showToast('已计算最佳入睡时间');
}

function calcWakeTime() {
  var bedTimeVal=document.getElementById('bedTime').value;
  if(!bedTimeVal){showToast('请选择入睡时间');return;}
  var fallAsleep=parseInt(document.getElementById('fallAsleepTime2').value);
  var cycleSelect=document.querySelector('#waketimeCycles input:checked');
  var cycles=cycleSelect?parseInt(cycleSelect.value):5;
  var parts=bedTimeVal.split(':');
  var bed=new Date();
  bed.setHours(parseInt(parts[0]),parseInt(parts[1]),0,0);
  bed.setMinutes(bed.getMinutes()+fallAsleep);
  var results=document.getElementById('waketimeResults');
  results.innerHTML='';
  var cycleMin=90;
  for(var c=4;c<=6;c++){
    var totalMin=c*cycleMin;
    var wakeTime=new Date(bed.getTime()+totalMin*60000);
    var h=wakeTime.getHours().toString().padStart(2,'0');
    var m=wakeTime.getMinutes().toString().padStart(2,'0');
    var isBest=c===cycles;
    var card=document.createElement('div');
    card.className='result-card'+(isBest?' best':'');
    card.innerHTML='<div class="time">'+h+':'+m+'</div><div class="label">'+c+'个周期 ('+(c*1.5)+'小时)</div>'+(isBest?'<div class="cycle-note">推荐</div>':'');
    results.appendChild(card);
  }
  showToast('已计算最佳起床时间');
}

// Init cycle selectors
function initCycles(){
  ['bedtimeCycles','waketimeCycles'].forEach(function(id){
    var container=document.getElementById(id);
    if(!container)return;
    for(var c=3;c<=6;c++){
      var label=document.createElement('label');
      var checked=c===5?'checked':'';
      label.innerHTML='<input type="radio" name="'+id+'" value="'+c+'" '+checked+'><span><span class="num">'+c+'</span>个周期</span>';
      container.appendChild(label);
    }
  });
}
initCycles();"""
    # Remove old stubs
    for func in ['calcBedtime','calcWakeTime']:
        pattern = rf'function {re.escape(func)}\s*\([^)]*\)\s*\{{[^}}]*\}}'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    content = content.replace('</script>', new_js + '\n</script>')
    return content

def fix_color_harmony(content):
    """Fix color-harmony: updateHarmony, randomHarmony, copyHarmony"""
    new_js = """function hexToHsl(hex){
  hex=hex.replace('#','');
  var r=parseInt(hex.substr(0,2),16)/255;
  var g=parseInt(hex.substr(2,2),16)/255;
  var b=parseInt(hex.substr(4,2),16)/255;
  var max=Math.max(r,g,b),min=Math.min(r,g,b);
  var h,s,l=(max+min)/2;
  if(max===min){h=s=0}
  else{var d=max-min;s=l>0.5?d/(2-max-min):d/(max+min);
    switch(max){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;case b:h=(r-g)/d+4;break}
    h/=6;
  }
  return[h*360,s*100,l*100];
}

function hslToHex(h,s,l){
  h/=360;s/=100;l/=100;
  var r,g,b;
  if(s===0){r=g=b=l}
  else{
    var hue2rgb=function(p,q,t){
      if(t<0)t+=1;if(t>1)t-=1;
      if(t<1/6)return p+(q-p)*6*t;
      if(t<1/2)return q;
      if(t<2/3)return p+(q-p)*(2/3-t)*6;
      return p;
    };
    var q=l<0.5?l*(1+s):l+s-l*s;
    var p=2*l-q;
    r=hue2rgb(p,q,h+1/3);
    g=hue2rgb(p,q,h);
    b=hue2rgb(p,q,h-1/3);
  }
  var toHex=function(x){var v=Math.round(x*255).toString(16);return v.length===1?'0'+v:v};
  return'#'+toHex(r)+toHex(g)+toHex(b);
}

function updateHarmony(){
  var baseHex=document.getElementById('harmBaseColor').value;
  var rule=document.getElementById('harmRule').value;
  var sat=parseInt(document.getElementById('harmSaturation').value);
  var lit=parseInt(document.getElementById('harmLightness').value);
  var hsl=hexToHsl(baseHex);
  var h=hsl[0];
  var colors=[];
  switch(rule){
    case'complementary':colors=[h,h+180];break;
    case'analogous':colors=[h-30,h,h+30];break;
    case'triadic':colors=[h,h+120,h+240];break;
    case'tetradic':colors=[h,h+90,h+180,h+270];break;
    case'monochromatic':colors=[h,h,h,h];lit=[lit-20,lit,lit+15,lit+30];break;
    case'split-complementary':colors=[h,h+150,h+210];break;
  }
  var container=document.getElementById('harmColors');
  container.innerHTML='';
  var hexList=[];
  colors.forEach(function(c,i){
    var hh=((c%360)+360)%360;
    var ll=rule==='monochromatic'?(lit?lit[i]:lit):lit;
    var hex=hslToHex(hh,sat,ll);
    hexList.push(hex);
    var wrap=document.createElement('div');
    wrap.className='color-swatch-wrap';
    wrap.innerHTML='<div class="color-swatch" style="background:'+hex+'" onclick="navigator.clipboard.writeText(\''+hex+'\').then(function(){showToast(\\''+hex+'已复制\\')})"></div><div class="color-swatch-label">'+hex.toUpperCase()+'</div>';
    container.appendChild(wrap);
  });
  document.getElementById('harmOutput').value=hexList.join('\\n');
}

function randomHarmony(){
  var h=Math.floor(Math.random()*360);
  var s=50+Math.floor(Math.random()*50);
  var l=40+Math.floor(Math.random()*30);
  var hex=hslToHex(h,s,l);
  document.getElementById('harmBaseColor').value=hex;
  updateHarmony();
  showToast('随机配色已生成');
}

function copyHarmony(){
  var t=document.getElementById('harmOutput').value;
  navigator.clipboard.writeText(t).then(function(){showToast('颜色代码已复制')}).catch(function(){showToast('复制失败')});
}

updateHarmony();"""
    for func in ['copyHarmony','randomHarmony','updateHarmony']:
        pattern = rf'function {re.escape(func)}\s*\([^)]*\)\s*\{{[^}}]*\}}'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    content = content.replace('</script>', new_js + '\n</script>')
    return content

def fix_palette_generator(content):
    """Fix palette-generator: updateFromHex, updateFromPicker, randomColor, copyAllColors"""
    new_js = """var paletteMode='complementary';
function hexToHsl(hex){
  hex=hex.replace('#','');
  if(hex.length!==6)return[0,0,0];
  var r=parseInt(hex.substr(0,2),16)/255;
  var g=parseInt(hex.substr(2,2),16)/255;
  var b=parseInt(hex.substr(4,2),16)/255;
  var max=Math.max(r,g,b),min=Math.min(r,g,b);
  var h,s,l=(max+min)/2;
  if(max===min){h=s=0}
  else{var d=max-min;s=l>0.5?d/(2-max-min):d/(max+min);
    switch(max){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;case b:h=(r-g)/d+4;break}
    h/=6;
  }
  return[h*360,s*100,l*100];
}

function hslToHex(h,s,l){
  h=((h%360)+360)%360;s=Math.max(0,Math.min(100,s));l=Math.max(0,Math.min(100,l));
  h/=360;s/=100;l/=100;
  var r,g,b;
  if(s===0){r=g=b=l}
  else{
    var hue2rgb=function(p,q,t){
      if(t<0)t+=1;if(t>1)t-=1;
      if(t<1/6)return p+(q-p)*6*t;
      if(t<1/2)return q;
      if(t<2/3)return p+(q-p)*(2/3-t)*6;
      return p;
    };
    var q=l<0.5?l*(1+s):l+s-l*s;
    var p=2*l-q;
    r=hue2rgb(p,q,h+1/3);g=hue2rgb(p,q,h);b=hue2rgb(p,q,h-1/3);
  }
  var toHex=function(x){var v=Math.round(x*255).toString(16);return v.length===1?'0'+v:v};
  return'#'+toHex(r)+toHex(g)+toHex(b);
}

function generatePalette(hex,mode){
  var hsl=hexToHsl(hex);
  var h=hsl[0],s=Math.max(40,hsl[1]),l=hsl[2];
  var colors=[];
  switch(mode){
    case'complementary':colors=[{h:h,s:s,l:l},{h:h+180,s:s,l:l}];break;
    case'analogous':colors=[{h:h-30,s:s,l:l},{h:h,s:s,l:l},{h:h+30,s:s,l:l}];break;
    case'triadic':colors=[{h:h,s:s,l:l},{h:h+120,s:s,l:l},{h:h+240,s:s,l:l}];break;
    case'split-complementary':colors=[{h:h,s:s,l:l},{h:h+150,s:s,l:l},{h:h+210,s:s,l:l}];break;
    case'tetradic':colors=[{h:h,s:s,l:l},{h:h+90,s:s,l:l},{h:h+180,s:s,l:l},{h:h+270,s:s,l:l}];break;
    case'monochromatic':colors=[{h:h,s:s,l:30},{h:h,s:s,l:50},{h:h,s:s,l:70},{h:h,s:s,l:90}];break;
  }
  return colors.map(function(c){return hslToHex(c.h,c.s,c.l)});
}

function renderPalette(colors){
  var grid=document.getElementById('paletteGrid');
  grid.innerHTML='';
  colors.forEach(function(hex){
    var card=document.createElement('div');
    card.className='color-card';
    card.onclick=function(){navigator.clipboard.writeText(hex).then(function(){showToast(hex+' 已复制')})};
    var r=parseInt(hex.substr(1,2),16),g=parseInt(hex.substr(3,2),16),b=parseInt(hex.substr(5,2),16);
    card.innerHTML='<div class="color-preview" style="background:'+hex+'"></div><div class="color-info"><div class="color-hex">'+hex.toUpperCase()+'</div><div class="color-rgb">rgb('+r+', '+g+', '+b+')</div></div>';
    grid.appendChild(card);
  });
}

function updateFromPicker(){
  var hex=document.getElementById('baseColor').value;
  document.getElementById('hexInput').value=hex;
  var colors=generatePalette(hex,paletteMode);
  renderPalette(colors);
}

function updateFromHex(){
  var hex=document.getElementById('hexInput').value;
  if(!/^#[0-9A-Fa-f]{6}$/.test(hex)){showToast('请输入有效的HEX颜色');return;}
  document.getElementById('baseColor').value=hex;
  var colors=generatePalette(hex,paletteMode);
  renderPalette(colors);
}

function randomColor(){
  var h=Math.floor(Math.random()*360);
  var s=50+Math.floor(Math.random()*50);
  var l=40+Math.floor(Math.random()*30);
  var hex=hslToHex(h,s,l);
  document.getElementById('baseColor').value=hex;
  document.getElementById('hexInput').value=hex;
  var colors=generatePalette(hex,paletteMode);
  renderPalette(colors);
  showToast('随机颜色已生成');
}

function copyAllColors(){
  var cards=document.querySelectorAll('.color-hex');
  var hexList=Array.from(cards).map(function(c){return c.textContent});
  navigator.clipboard.writeText(hexList.join(', ')).then(function(){showToast('全部颜色已复制')}).catch(function(){showToast('复制失败')});
}

// Mode buttons
document.querySelectorAll('.mode-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    document.querySelectorAll('.mode-btn').forEach(function(b){b.classList.remove('active')});
    btn.classList.add('active');
    paletteMode=btn.dataset.mode;
    updateFromPicker();
  });
});

// Initial render
updateFromPicker();"""
    for func in ['copyAllColors','randomColor','updateFromHex','updateFromPicker']:
        pattern = rf'function {re.escape(func)}\s*\([^)]*\)\s*\{{[^}}]*\}}'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    content = content.replace('</script>', new_js + '\n</script>')
    return content

# Main
tools_to_fix = {
    'csv-transpose/index.html': fix_csv_transpose,
    'csv-splitter/index.html': fix_csv_splitter,
    'csv-diff/index.html': fix_csv_diff,
    'sleep-calculator/index.html': fix_sleep_calculator,
    'color-harmony/index.html': fix_color_harmony,
    'palette-generator/index.html': fix_palette_generator,
}

fixed = 0
for rel_path, fixer in tools_to_fix.items():
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print(f"SKIP: {rel_path} not found")
        continue
    content = read_file(path)
    new_content = fixer(content)
    if new_content != content:
        write_file(path, new_content)
        fixed += 1
        print(f"FIXED: {rel_path}")
    else:
        print(f"NO CHANGE: {rel_path}")

print(f"\nTotal fixed: {fixed}")
