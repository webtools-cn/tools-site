#!/usr/bin/env python3
"""为批量创建的10个工具页面注入实际JS功能代码"""
import re

BASE = "/home/chison/tools-site"

# 各工具的JS功能代码（注入在 </script> 之前，即 copyText之后）
APP_CODES = {
    "file-compare": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>📄 文本对比</h2><div class="row"><div class="field"><label>原始文本</label><textarea id="textA" rows="6" placeholder="粘贴原始文本..."></textarea></div><div class="field"><label>对比文本</label><textarea id="textB" rows="6" placeholder="粘贴对比文本..."></textarea></div></div><div class="btn-row"><button class="btn btn-primary" id="compareBtn">🔍 开始对比</button><button class="btn btn-secondary" id="clearBtn">清空</button><button class="btn btn-secondary" id="swapBtn">🔄 交换</button></div></div><div class="result-section" id="resultSection"><h2>📊 对比结果</h2><div id="diffStats" style="color:#94a3b8;font-size:.85rem;margin-bottom:12px"></div><div id="diffResult" class="result-box" style="font-family:monospace;font-size:.85rem;max-height:500px;overflow-y:auto"></div><div class="btn-row"><button class="btn btn-success" id="copyDiff">📋 复制结果</button></div></div>';
function computeDiff(){
  var a=document.getElementById('textA').value.split('\\n');
  var b=document.getElementById('textB').value.split('\\n');
  var maxLen=Math.max(a.length,b.length);
  var result='',added=0,removed=0,unchanged=0;
  for(var i=0;i<maxLen;i++){
    var la=a[i]||'',lb=b[i]||'';
    if(la===lb){result+='  '+la+'\\n';unchanged++;}
    else if(!la){result+='+ '+lb+'\\n';added++;}
    else if(!lb){result+='- '+la+'\\n';removed++;}
    else{result+='- '+la+'\\n+ '+lb+'\\n';removed++;added++;}
  }
  document.getElementById('diffResult').textContent=result;
  document.getElementById('diffStats').innerHTML='行数: <span style="color:#4ade80">不变 '+unchanged+'</span> | <span style="color:#f87171">删除 '+removed+'</span> | <span style="color:#22d3ee">新增 '+added+'</span>';
  document.getElementById('resultSection').classList.add('show');
}
document.getElementById('compareBtn').addEventListener('click',computeDiff);
document.getElementById('clearBtn').addEventListener('click',function(){
  document.getElementById('textA').value='';document.getElementById('textB').value='';
  document.getElementById('resultSection').classList.remove('show');
});
document.getElementById('swapBtn').addEventListener('click',function(){
  var ta=document.getElementById('textA').value;
  document.getElementById('textA').value=document.getElementById('textB').value;
  document.getElementById('textB').value=ta;
});
document.getElementById('copyDiff').addEventListener('click',function(){copyText(document.getElementById('diffResult'))});
})();
''',

    "image-compare": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🖼️ 上传图片</h2><div class="row"><div class="field"><label>图片A (基准)</label><input type="file" id="imgFileA" accept="image/*"></div><div class="field"><label>图片B (对比)</label><input type="file" id="imgFileB" accept="image/*"></div></div><div class="btn-row"><button class="btn btn-primary" id="compareBtn">🔍 对比</button><button class="btn btn-secondary" id="resetBtn">重置</button></div></div><div class="result-section" id="resultSection"><h2>📊 对比视图</h2><div style="margin-bottom:8px"><label style="display:inline;margin-right:12px"><input type="radio" name="mode" value="slider" checked> 滑动对比</label><label style="display:inline;margin-right:12px"><input type="radio" name="mode" value="side"> 并排对比</label><label style="display:inline"><input type="radio" name="mode" value="overlay"> 叠层对比</label></div><div id="viewArea" style="min-height:300px"></div></div>';
var imgA=null,imgB=null;
function loadImage(file,cb){
  var reader=new FileReader();
  reader.onload=function(e){var img=new Image();img.onload=function(){cb(img)};img.src=e.target.result;};
  reader.readAsDataURL(file);
}
function renderView(mode){
  var area=document.getElementById('viewArea');
  if(!imgA||!imgB){area.innerHTML='<p style="color:#94a3b8;text-align:center;padding:60px">请先上传两张图片</p>';return;}
  if(mode==='side'){
    area.innerHTML='<div class="row"><div style="flex:1"><img src="'+imgA.src+'" style="width:100%;display:block;border-radius:8px"><p style="text-align:center;color:#94a3b8;font-size:.8rem;margin-top:4px">图片A</p></div><div style="flex:1"><img src="'+imgB.src+'" style="width:100%;display:block;border-radius:8px"><p style="text-align:center;color:#94a3b8;font-size:.8rem;margin-top:4px">图片B</p></div></div>';
  }else if(mode==='overlay'){
    area.innerHTML='<div style="position:relative;display:inline-block;width:100%"><img src="'+imgA.src+'" style="width:100%;display:block;border-radius:8px"><img src="'+imgB.src+'" style="position:absolute;top:0;left:0;width:100%;opacity:0.5;border-radius:8px"><p style="text-align:center;color:#94a3b8;font-size:.8rem;margin-top:4px">B(半透明)覆盖在A上</p></div>';
  }else{
    area.innerHTML='<div class="slider-container" id="slider"><img src="'+imgA.src+'" alt="Image A"><div class="slider-overlay" id="sliderOverlay"><img src="'+imgB.src+'" alt="Image B"></div><div class="slider-handle" id="sliderHandle">⇔</div></div>';
    setTimeout(function(){
      var slider=document.getElementById('slider'),overlay=document.getElementById('sliderOverlay'),handle=document.getElementById('sliderHandle');
      if(!slider)return;
      var dragging=false;
      function move(e){
        var rect=slider.getBoundingClientRect();
        var x=(e.clientX||e.touches[0].clientX)-rect.left;
        var pct=Math.max(0,Math.min(100,(x/rect.width)*100));
        overlay.style.width=pct+'%';
        handle.style.left=pct+'%';
      }
      handle.addEventListener('mousedown',function(e){dragging=true;e.preventDefault();});
      handle.addEventListener('touchstart',function(e){dragging=true;});
      document.addEventListener('mousemove',function(e){if(dragging)move(e);});
      document.addEventListener('touchmove',function(e){if(dragging)move(e);});
      document.addEventListener('mouseup',function(){dragging=false;});
      document.addEventListener('touchend',function(){dragging=false;});
    },100);
  }
}
document.getElementById('imgFileA').addEventListener('change',function(e){
  if(e.target.files[0])loadImage(e.target.files[0],function(img){imgA=img;renderView(document.querySelector('input[name="mode"]:checked').value);document.getElementById('resultSection').classList.add('show');});
});
document.getElementById('imgFileB').addEventListener('change',function(e){
  if(e.target.files[0])loadImage(e.target.files[0],function(img){imgB=img;renderView(document.querySelector('input[name="mode"]:checked').value);document.getElementById('resultSection').classList.add('show');});
});
document.getElementById('resetBtn').addEventListener('click',function(){
  imgA=null;imgB=null;document.getElementById('imgFileA').value='';document.getElementById('imgFileB').value='';
  document.getElementById('resultSection').classList.remove('show');
});
document.querySelectorAll('input[name="mode"]').forEach(function(el){el.addEventListener('change',function(){renderView(this.value)});});
})();
''',

    "base32-encode": '''
(function(){
var app=document.getElementById('app');
var ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
app.innerHTML='<div class="input-section"><h2>📝 输入文本</h2><textarea id="inputText" rows="4" placeholder="输入要编码的文本...">Hello World!</textarea><div class="btn-row"><button class="btn btn-primary" id="encodeBtn">🔢 Base32编码</button><button class="btn btn-secondary" id="clearBtn">清空</button></div></div><div class="result-section show" id="resultSection"><h2>✅ Base32编码结果</h2><div id="encodeResult" class="result-box" style="font-family:monospace;font-size:.85rem;word-break:break-all;user-select:all"></div><div style="margin-top:8px;color:#64748b;font-size:.8rem" id="meta"></div><div class="btn-row"><button class="btn btn-success" id="copyBtn">📋 复制结果</button></div></div>';
function base32Encode(input){
  var bits='',result='';
  for(var i=0;i<input.length;i++){var b=input.charCodeAt(i);bits+=('00000000'+b.toString(2)).slice(-8);}
  for(var i=0;i<bits.length;i+=5){
    var chunk=bits.substring(i,i+5);
    while(chunk.length<5)chunk+='0';
    result+=ALPHABET[parseInt(chunk,2)];
  }
  var padding=8-(result.length%8);
  if(padding>0&&padding<8)result+='='.repeat(padding);
  return result;
}
function compute(){
  var text=document.getElementById('inputText').value;
  if(!text){document.getElementById('encodeResult').textContent='请输入文本';return;}
  var encoded=base32Encode(text);
  document.getElementById('encodeResult').textContent=encoded;
  document.getElementById('meta').textContent='输入: '+text.length+' 字符 | 输出: '+encoded.length+' 字符';
}
document.getElementById('encodeBtn').addEventListener('click',compute);
document.getElementById('inputText').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('inputText').value='';document.getElementById('encodeResult').textContent='';document.getElementById('meta').textContent='';});
document.getElementById('copyBtn').addEventListener('click',function(){copyText(document.getElementById('encodeResult'))});
compute();
})();
''',

    "base32-decode": '''
(function(){
var app=document.getElementById('app');
var ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
app.innerHTML='<div class="input-section"><h2>📝 Base32文本</h2><textarea id="inputText" rows="4" placeholder="输入Base32编码文本...">JBSWY3DPEB3W64TMMQ======</textarea><div class="btn-row"><button class="btn btn-primary" id="decodeBtn">🔢 Base32解码</button><button class="btn btn-secondary" id="clearBtn">清空</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 解码结果</h2><div id="decodeResult" class="result-box" style="font-family:monospace;font-size:.85rem;word-break:break-all;user-select:all"></div><div style="margin-top:8px;color:#64748b;font-size:.8rem" id="meta"></div><div class="btn-row"><button class="btn btn-success" id="copyBtn">📋 复制结果</button></div></div>';
function base32Decode(input){
  input=input.toUpperCase().replace(/[^A-Z2-7=]/g,'');
  var bits='',result='';
  for(var i=0;i<input.length;i++){
    var c=input[i];
    if(c==='=')continue;
    var idx=ALPHABET.indexOf(c);
    if(idx===-1)continue;
    bits+=('00000'+idx.toString(2)).slice(-5);
  }
  for(var i=0;i<bits.length;i+=8){
    var chunk=bits.substring(i,i+8);
    if(chunk.length<8)break;
    result+=String.fromCharCode(parseInt(chunk,2));
  }
  return result;
}
function compute(){
  var text=document.getElementById('inputText').value;
  if(!text){document.getElementById('decodeResult').textContent='请输入Base32文本';return;}
  try{
    var decoded=base32Decode(text);
    document.getElementById('decodeResult').textContent=decoded;
    document.getElementById('meta').textContent='输入: '+text.length+' 字符 | 输出: '+decoded.length+' 字符';
  }catch(e){
    document.getElementById('decodeResult').textContent='解码失败: '+e.message;
  }
}
document.getElementById('decodeBtn').addEventListener('click',compute);
document.getElementById('inputText').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('inputText').value='';document.getElementById('decodeResult').textContent='';document.getElementById('meta').textContent='';});
document.getElementById('copyBtn').addEventListener('click',function(){copyText(document.getElementById('decodeResult'))});
compute();
})();
''',

    "unicode-analyzer": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🔤 输入字符</h2><input type="text" id="charInput" placeholder="输入任意字符或粘贴文本..." value="中" maxlength="100"><div class="btn-row"><button class="btn btn-primary" id="analyzeBtn">🔍 分析</button><button class="btn btn-secondary" id="clearBtn">清空</button></div></div><div class="result-section show" id="resultSection"><h2>📊 分析结果</h2><div id="analysisResult"></div></div>';
function analyzeChar(c){
  var code=c.charCodeAt(0);
  var hex='U+'+code.toString(16).toUpperCase().padStart(4,'0');
  var utf8='';var bytes=[];
  if(code<128){bytes=[code];}
  else if(code<2048){bytes=[192|(code>>6),128|(code&63)];}
  else if(code<65536){bytes=[224|(code>>12),128|((code>>6)&63),128|(code&63)];}
  else{var hi=55296+((code-65536)>>10);var lo=56320+((code-65536)&1023);bytes=[240|(hi>>18),128|((hi>>12)&63),128|((hi>>6)&63),128|(hi&63),240|(lo>>18),128|((lo>>12)&63),128|((lo>>6)&63),128|(lo&63)];}
  var utf8hex=bytes.map(function(b){return b.toString(16).toUpperCase().padStart(2,'0')}).join(' ');
  var utf16=code.toString(16).toUpperCase().padStart(4,'0');
  var htmlEntity='&#'+code+';';
  var htmlHex='&#x'+code.toString(16).toUpperCase()+';';
  var name='';
  try{name=require&&require('fs')?c:c;}catch(e){}
  var category='';var script='';
  if(code>=0x4E00&&code<=0x9FFF){script='CJK统一表意文字';category='汉字';}
  else if(code>=0x3040&&code<=0x309F){script='平假名';category='日语';}
  else if(code>=0x30A0&&code<=0x30FF){script='片假名';category='日语';}
  else if(code>=0xAC00&&code<=0xD7AF){script='韩文音节';category='韩语';}
  else if(code>=0x0600&&code<=0x06FF){script='阿拉伯文';category='阿拉伯语';}
  else if(code>=0x0400&&code<=0x04FF){script='西里尔文';category='斯拉夫语';}
  else if(code>=0x0370&&code<=0x03FF){script='希腊文';category='希腊语';}
  else if(code>=0x0000&&code<=0x007F){script='基本拉丁文';category='ASCII';}
  else if(code>=0x0080&&code<=0x00FF){script='拉丁文补充';category='扩展拉丁文';}
  else if(code>=0x2000&&code<=0x206F){script='常用标点';category='标点符号';}
  else if(code>=0x1F300&&code<=0x1F9FF){script='Emoji';category='表情符号';}
  else{script='其他';category='其他';}
  return'<div class="result-box" style="font-size:3rem;text-align:center">'+c+'</div><table class="data" style="width:100%;margin-top:8px"><tr><th>属性</th><th>值</th></tr><tr><td>Unicode码点</td><td style="font-family:monospace">'+hex+'</td></tr><tr><td>十进制</td><td style="font-family:monospace">'+code+'</td></tr><tr><td>UTF-8编码</td><td style="font-family:monospace">'+utf8hex+' ('+bytes.length+' 字节)</td></tr><tr><td>UTF-16编码</td><td style="font-family:monospace">'+utf16+'</td></tr><tr><td>HTML实体(十进制)</td><td style="font-family:monospace">'+htmlEntity+'</td></tr><tr><td>HTML实体(十六进制)</td><td style="font-family:monospace">'+htmlHex+'</td></tr><tr><td>字符分类</td><td>'+category+'</td></tr><tr><td>Unicode区块</td><td>'+script+'</td></tr></table>';
}
function compute(){
  var text=document.getElementById('charInput').value;
  if(!text){document.getElementById('analysisResult').innerHTML='<p style="color:#94a3b8">请输入字符</p>';return;}
  var html='';
  for(var i=0;i<Math.min(text.length,5);i++){
    html+='<div style="margin-bottom:16px">'+analyzeChar(text[i])+'</div>';
  }
  if(text.length>5)html+='<p style="color:#64748b;font-size:.8rem">（仅显示前5个字符的分析结果）</p>';
  document.getElementById('analysisResult').innerHTML=html;
}
document.getElementById('analyzeBtn').addEventListener('click',compute);
document.getElementById('charInput').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('charInput').value='';document.getElementById('analysisResult').innerHTML='';});
compute();
})();
''',

    "utf8-converter": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>📝 输入文本</h2><textarea id="inputText" rows="3" placeholder="输入文本...">Hello 世界</textarea><div class="btn-row"><button class="btn btn-primary" id="toUtf8Btn">➡️ 文本→UTF-8字节</button><button class="btn btn-primary" id="toTextBtn">⬅️ UTF-8字节→文本</button><button class="btn btn-secondary" id="clearBtn">清空</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 结果</h2><div id="convertResult" class="result-box" style="font-family:monospace;font-size:.85rem;word-break:break-all;user-select:all"></div><div style="margin-top:8px;color:#64748b;font-size:.8rem" id="meta"></div><div class="btn-row"><button class="btn btn-success" id="copyBtn">📋 复制结果</button></div></div>';
function textToUtf8Hex(text){
  var bytes=[];for(var i=0;i<text.length;i++){var code=text.charCodeAt(i);if(code<128){bytes.push(code);}else if(code<2048){bytes.push(192|(code>>6));bytes.push(128|(code&63));}else if(code<55296||code>=57344){bytes.push(224|(code>>12));bytes.push(128|((code>>6)&63));bytes.push(128|(code&63));}else{i++;var lo=text.charCodeAt(i);var cp=((code-55296)<<10)+(lo-56320)+65536;bytes.push(240|(cp>>18));bytes.push(128|((cp>>12)&63));bytes.push(128|((cp>>6)&63));bytes.push(128|(cp&63));}}
  return bytes.map(function(b){return b.toString(16).toUpperCase().padStart(2,'0')}).join(' ');
}
function hexToText(hex){
  hex=hex.replace(/\\s/g,'').replace(/0x/gi,'');
  var bytes=[];for(var i=0;i<hex.length;i+=2){bytes.push(parseInt(hex.substring(i,i+2),16));}
  var text='',i=0;
  while(i<bytes.length){
    var b=bytes[i];
    if(b<128){text+=String.fromCharCode(b);i+=1;}
    else if(b<224){text+=String.fromCharCode(((b&31)<<6)|(bytes[i+1]&63));i+=2;}
    else if(b<240){text+=String.fromCharCode(((b&15)<<12)|((bytes[i+1]&63)<<6)|(bytes[i+2]&63));i+=3;}
    else{var cp=((b&7)<<18)|((bytes[i+1]&63)<<12)|((bytes[i+2]&63)<<6)|(bytes[i+3]&63);cp-=65536;text+=String.fromCharCode(55296+(cp>>10))+String.fromCharCode(56320+(cp&1023));i+=4;}
  }
  return text;
}
document.getElementById('toUtf8Btn').addEventListener('click',function(){
  var text=document.getElementById('inputText').value;
  var hex=textToUtf8Hex(text);
  document.getElementById('convertResult').textContent=hex;
  document.getElementById('meta').textContent='文本: '+text.length+' 字符 → UTF-8字节';
});
document.getElementById('toTextBtn').addEventListener('click',function(){
  var hex=document.getElementById('inputText').value;
  try{var text=hexToText(hex);document.getElementById('convertResult').textContent=text;document.getElementById('meta').textContent='UTF-8字节 → 文本: '+text.length+' 字符';}
  catch(e){document.getElementById('convertResult').textContent='转换失败，请确认输入是有效的UTF-8十六进制字节';document.getElementById('meta').textContent='';}
});
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('inputText').value='';document.getElementById('convertResult').textContent='';document.getElementById('meta').textContent='';});
document.getElementById('copyBtn').addEventListener('click',function(){copyText(document.getElementById('convertResult'))});
document.getElementById('toUtf8Btn').click();
})();
''',

    "password-strength": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🔐 输入密码</h2><input type="text" id="pwdInput" placeholder="输入要检测的密码..." value="MyP@ssw0rd!2024"><div class="btn-row"><button class="btn btn-primary" id="checkBtn">🔍 检测强度</button><button class="btn btn-secondary" id="clearBtn">清空</button><button class="btn btn-secondary" id="genBtn">🎲 随机生成</button></div></div><div class="result-section show" id="resultSection"><h2>📊 检测结果</h2><div style="margin-bottom:12px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px"><span style="font-weight:600" id="strengthLabel">-</span><span style="font-size:.85rem;color:#94a3b8" id="scoreText"></span></div><div class="strength-bar"><div class="strength-fill" id="strengthFill" style="width:0%"></div></div></div><div class="checks" id="checkItems"></div><div style="margin-top:12px;color:#94a3b8;font-size:.85rem" id="crackTime"></div></div>';
var COMMON=['password','123456','12345678','qwerty','abc123','monkey','1234567','letmein','trustno1','dragon','baseball','iloveyou','master','sunshine','ashley','bailey','shadow','123123','654321','superman','qazwsx','michael','football','password1','welcome','admin','1234','passw0rd','p@ssword','password123'];
function checkStrength(pwd){
  var score=0;var checks=[];
  var len=pwd.length;
  checks.push({text:'长度≥8',pass:len>=8});if(len>=8)score++;
  checks.push({text:'长度≥12',pass:len>=12});if(len>=12)score++;
  checks.push({text:'长度≥16',pass:len>=16});if(len>=16)score++;
  var hasUpper=/[A-Z]/.test(pwd);checks.push({text:'包含大写字母',pass:hasUpper});if(hasUpper)score++;
  var hasLower=/[a-z]/.test(pwd);checks.push({text:'包含小写字母',pass:hasLower});if(hasLower)score++;
  var hasDigit=/\\d/.test(pwd);checks.push({text:'包含数字',pass:hasDigit});if(hasDigit)score++;
  var hasSpecial=/[^A-Za-z0-9]/.test(pwd);checks.push({text:'包含特殊字符',pass:hasSpecial});if(hasSpecial)score++;
  var hasMultiType=[hasUpper,hasLower,hasDigit,hasSpecial].filter(Boolean).length>=3;
  checks.push({text:'≥3种字符类型',pass:hasMultiType});if(hasMultiType)score++;
  var isCommon=COMMON.includes(pwd.toLowerCase());checks.push({text:'非常见密码',pass:!isCommon});if(!isCommon)score++;
  var noRepeat=!/(.)\\1{2,}/.test(pwd);checks.push({text:'无连续重复',pass:noRepeat});if(noRepeat)score++;
  var noSeq=!/(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)/i.test(pwd);
  checks.push({text:'无键盘序列',pass:noSeq});if(noSeq)score++;
  var lvl='',cls='';var time='';
  if(score<=3){lvl='弱';cls='strength-0';time='秒级可破解'}
  else if(score<=5){lvl='中等';cls='strength-1';time='数分钟可破解'}
  else if(score<=7){lvl='强';cls='strength-2';time='数天可破解'}
  else if(score<=9){lvl='很强';cls='strength-3';time='数年可破解'}
  else{lvl='极强';cls='strength-4';time='数百年才能破解'}
  return{score:score,max:11,lvl:lvl,cls:cls,checks:checks,time:time};
}
function compute(){
  var pwd=document.getElementById('pwdInput').value;
  if(!pwd){document.getElementById('strengthLabel').textContent='请输入密码';return;}
  var r=checkStrength(pwd);
  document.getElementById('strengthLabel').textContent='强度等级: '+r.lvl;
  document.getElementById('scoreText').textContent=r.score+'/'+r.max+' 分';
  var fill=document.getElementById('strengthFill');
  fill.style.width=(r.score/r.max*100)+'%';
  fill.className='strength-fill '+r.cls;
  document.getElementById('crackTime').textContent='预计破解时间: '+r.time;
  var items='';
  r.checks.forEach(function(c){items+='<div class="check-item"><span class="'+(c.pass?'check-pass':'check-fail')+'">'+(c.pass?'✅':'❌')+'</span> '+c.text+'</div>';});
  document.getElementById('checkItems').innerHTML=items;
}
function genPwd(){
  var chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';
  var pwd='';for(var i=0;i<16;i++){pwd+=chars[Math.floor(Math.random()*chars.length)];}
  document.getElementById('pwdInput').value=pwd;compute();
}
document.getElementById('checkBtn').addEventListener('click',compute);
document.getElementById('pwdInput').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('pwdInput').value='';document.getElementById('strengthLabel').textContent='-';document.getElementById('strengthFill').style.width='0%';});
document.getElementById('genBtn').addEventListener('click',genPwd);
compute();
})();
''',

    "sha1-hash": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🔐 输入文本</h2><textarea id="inputText" rows="4" placeholder="输入要哈希的文本...">Hello World!</textarea><div class="btn-row"><button class="btn btn-primary" id="hashBtn">🔐 生成SHA-1</button><button class="btn btn-secondary" id="clearBtn">清空</button></div></div><div class="result-section show" id="resultSection"><h2>✅ SHA-1哈希</h2><div id="hashResult" class="result-box" style="font-family:monospace;font-size:.85rem;word-break:break-all;user-select:all"></div><div style="margin-top:8px;color:#64748b;font-size:.8rem" id="hashMeta"></div><div class="btn-row"><button class="btn btn-success" id="copyHash">📋 复制哈希</button></div></div>';
function sha1(input){
  function r(n,c){return(n<<c)|(n>>>(32-c));}
  var words=[];var bitLen=input.length*8;
  for(var i=0;i<input.length;i++){var code=input.charCodeAt(i);if(code<128){words.push(code);}else if(code<2048){words.push(192|(code>>6));words.push(128|(code&63));}else if(code<55296||code>=57344){words.push(224|(code>>12));words.push(128|((code>>6)&63));words.push(128|(code&63));}else{i++;var lo=input.charCodeAt(i);var cp=((code-55296)<<10)+(lo-56320)+65536;words.push(240|(cp>>18));words.push(128|((cp>>12)&63));words.push(128|((cp>>6)&63));words.push(128|(cp&63));}}
  var bitCount=words.length*8;words.push(128);while((words.length*8)%512!==448)words.push(0);
  words.push(0);words.push(0);words.push(0);words.push(0);words.push(bitCount>>>24);words.push((bitCount>>16)&255);words.push((bitCount>>8)&255);words.push(bitCount&255);
  var h0=0x67452301,h1=0xEFCDAB89,h2=0x98BADCFE,h3=0x10325476,h4=0xC3D2E1F0;
  for(var i=0;i<words.length;i+=64){
    var w=[];for(var t=0;t<16;t++){w[t]=(words[i+t*4]<<24)|(words[i+t*4+1]<<16)|(words[i+t*4+2]<<8)|words[i+t*4+3];}
    for(var t=16;t<80;t++){w[t]=r(w[t-3]^w[t-8]^w[t-14]^w[t-16],1);}
    var a=h0,b=h1,c=h2,d=h3,e=h4;
    for(var t=0;t<80;t++){
      var f,k;
      if(t<20){f=(b&c)|((~b)&d);k=0x5A827999;}
      else if(t<40){f=b^c^d;k=0x6ED9EBA1;}
      else if(t<60){f=(b&c)|(b&d)|(c&d);k=0x8F1BBCDC;}
      else{f=b^c^d;k=0xCA62C1D6;}
      var temp=(r(a,5)+f+e+k+w[t])&0xffffffff;e=d;d=c;c=r(b,30);b=a;a=temp;
    }
    h0=(h0+a)&0xffffffff;h1=(h1+b)&0xffffffff;h2=(h2+c)&0xffffffff;h3=(h3+d)&0xffffffff;h4=(h4+e)&0xffffffff;
  }
  return[h0,h1,h2,h3,h4].map(function(v){return('0000000'+v.toString(16)).slice(-8)}).join('');
}
function compute(){
  var text=document.getElementById('inputText').value;
  if(!text){document.getElementById('hashResult').textContent='请输入文本';return;}
  var hash=sha1(text);
  document.getElementById('hashResult').textContent=hash;
  document.getElementById('hashMeta').textContent='输入: '+text.length+' 字符 | 输出: '+hash.length+' hex字符 (160 bits)';
}
document.getElementById('hashBtn').addEventListener('click',compute);
document.getElementById('inputText').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('inputText').value='';document.getElementById('hashResult').textContent='';document.getElementById('hashMeta').textContent='';});
document.getElementById('copyHash').addEventListener('click',function(){copyText(document.getElementById('hashResult'))});
compute();
})();
''',

    "semver-checker": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🏷️ 输入版本号</h2><div class="row"><div class="field"><label>版本A</label><input type="text" id="verA" placeholder="例如: 2.1.0" value="1.2.3"></div><div class="field"><label>版本B</label><input type="text" id="verB" placeholder="例如: 2.0.0" value="2.0.0"></div></div><div class="btn-row"><button class="btn btn-primary" id="compareBtn">🔍 比较</button><button class="btn btn-secondary" id="clearBtn">清空</button><button class="btn btn-secondary" id="swapBtn">🔄 交换</button></div></div><div class="result-section show" id="resultSection"><h2>📊 比较结果</h2><div id="compareResult" style="text-align:center;font-size:1.2rem;padding:16px"></div><div class="result-box" style="font-family:monospace;font-size:.85rem"><table class="data" style="width:100%"><tr><th></th><th>主版本</th><th>次版本</th><th>补丁</th><th>预发布</th><th>构建元数据</th></tr><tr id="rowA"></tr><tr id="rowB"></tr></table></div><div style="margin-top:8px;color:#94a3b8;font-size:.85rem" id="validation"></div></div>';
var SEMVER=/^v?(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$/;
function parse(ver){
  var m=ver.match(SEMVER);
  if(!m)return null;
  return{major:parseInt(m[1]),minor:parseInt(m[2]),patch:parseInt(m[3]),prerelease:m[4]||'',build:m[5]||''};
}
function comparePre(a,b){
  if(!a&&!b)return 0;if(!a)return 1;if(!b)return -1;
  var pa=a.split('.'),pb=b.split('.');
  for(var i=0;i<Math.max(pa.length,pb.length);i++){
    var ia=pa[i]||'',ib=pb[i]||'';
    var na=parseInt(ia),nb=parseInt(ib);
    var aNum=!isNaN(ia)&&String(na)===ia;
    var bNum=!isNaN(ib)&&String(nb)===ib;
    if(aNum&&bNum){if(na!==nb)return na<nb?-1:1;}
    else if(aNum)return -1;
    else if(bNum)return 1;
    else{if(ia<ib)return -1;if(ia>ib)return 1;}
  }
  return 0;
}
function compare(a,b){
  if(a.major!==b.major)return a.major<b.major?-1:1;
  if(a.minor!==b.minor)return a.minor<b.minor?-1:1;
  if(a.patch!==b.patch)return a.patch<b.patch?-1:1;
  return comparePre(a.prerelease,b.prerelease);
}
function formatCell(v){return v===undefined?'-':v;}
function compute(){
  var va=document.getElementById('verA').value;
  var vb=document.getElementById('verB').value;
  var pa=parse(va),pb=parse(vb);
  var vMsg='';
  if(!pa)vMsg+='<span style="color:#f87171">❌ 版本A格式无效</span> ';
  else vMsg+='<span style="color:#4ade80">✅ 版本A有效</span> ';
  if(!pb)vMsg+='<span style="color:#f87171">❌ 版本B格式无效</span> ';
  else vMsg+='<span style="color:#4ade80">✅ 版本B有效</span> ';
  document.getElementById('validation').innerHTML=vMsg;
  if(!pa||!pb){document.getElementById('compareResult').innerHTML='';return;}
  var rowA='<td style="color:#22d3ee">版本A ('+va+')</td><td>'+pa.major+'</td><td>'+pa.minor+'</td><td>'+pa.patch+'</td><td>'+formatCell(pa.prerelease)+'</td><td>'+formatCell(pa.build)+'</td>';
  var rowB='<td style="color:#f87171">版本B ('+vb+')</td><td>'+pb.major+'</td><td>'+pb.minor+'</td><td>'+pb.patch+'</td><td>'+formatCell(pb.prerelease)+'</td><td>'+formatCell(pb.build)+'</td>';
  document.getElementById('rowA').innerHTML=rowA;
  document.getElementById('rowB').innerHTML=rowB;
  var cmp=compare(pa,pb);
  var result='';
  if(cmp<0)result='<span style="color:#22d3ee">'+va+'</span> < <span style="color:#f87171">'+vb+'</span><br><span style="font-size:.9rem;color:#94a3b8">版本B更新</span>';
  else if(cmp>0)result='<span style="color:#22d3ee">'+va+'</span> > <span style="color:#f87171">'+vb+'</span><br><span style="font-size:.9rem;color:#94a3b8">版本A更新</span>';
  else result='<span style="color:#22d3ee">'+va+'</span> = <span style="color:#f87171">'+vb+'</span><br><span style="font-size:.9rem;color:#94a3b8">版本相同</span>';
  document.getElementById('compareResult').innerHTML=result;
}
document.getElementById('compareBtn').addEventListener('click',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('verA').value='';document.getElementById('verB').value='';});
document.getElementById('swapBtn').addEventListener('click',function(){var t=document.getElementById('verA').value;document.getElementById('verA').value=document.getElementById('verB').value;document.getElementById('verB').value=t;compute();});
document.getElementById('verA').addEventListener('input',compute);
document.getElementById('verB').addEventListener('input',compute);
compute();
})();
''',

    "query-string-parser": '''
(function(){
var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>🔗 输入URL或查询字符串</h2><textarea id="inputUrl" rows="3" placeholder="输入URL或查询字符串...">https://example.com/search?q=hello+world&page=1&sort=desc&tags=js,css</textarea><div class="btn-row"><button class="btn btn-primary" id="parseBtn">🔍 解析</button><button class="btn btn-secondary" id="clearBtn">清空</button><button class="btn btn-secondary" id="buildBtn">🔄 从参数构建</button></div></div><div class="result-section show" id="resultSection"><h2>📊 解析结果</h2><div id="parseResult"></div><div class="btn-row"><button class="btn btn-success" id="copyJson">📋 复制JSON</button><button class="btn btn-success" id="copyQuery">📋 复制查询字符串</button></div></div>';
function parseQueryString(str){
  str=str.trim();
  var idx=str.indexOf('?');
  if(idx>=0)str=str.substring(idx+1);
  var baseUrl=str.indexOf('?')>=0?str.substring(0,str.indexOf('?')):'';
  var params={};
  if(!str)return{base:baseUrl,params:params};
  str.split('&').forEach(function(pair){
    var eq=pair.indexOf('=');
    var key,val;
    if(eq>=0){key=decodeURIComponent(pair.substring(0,eq));val=decodeURIComponent(pair.substring(eq+1));}
    else{key=decodeURIComponent(pair);val='';}
    if(params[key]!==undefined){
      if(!Array.isArray(params[key]))params[key]=[params[key]];
      params[key].push(val);
    }else{params[key]=val;}
  });
  return{base:baseUrl,params:params};
}
function compute(){
  var input=document.getElementById('inputUrl').value;
  var result=parseQueryString(input);
  var params=result.params;
  var keys=Object.keys(params);
  if(keys.length===0){document.getElementById('parseResult').innerHTML='<p style="color:#94a3b8;text-align:center;padding:20px">未找到查询参数</p>';return;}
  var html='<table class="data" style="width:100%"><tr><th>#</th><th>参数名</th><th>值</th><th>类型</th></tr>';
  keys.forEach(function(key,i){
    var val=params[key];
    var type=Array.isArray(val)?'array('+val.length+')':typeof val;
    var display=Array.isArray(val)?val.join(', '):String(val);
    html+='<tr><td>'+(i+1)+'</td><td style="font-family:monospace;color:#22d3ee">'+key+'</td><td style="font-family:monospace;word-break:break-all">'+display+'</td><td style="color:#94a3b8">'+type+'</td></tr>';
  });
  html+='</table><p style="color:#64748b;font-size:.8rem;margin-top:8px">共 '+keys.length+' 个参数</p>';
  document.getElementById('parseResult').innerHTML=html;
  // store for copy
  document.getElementById('parseResult').dataset.json=JSON.stringify(params,null,2);
  document.getElementById('parseResult').dataset.query=keys.map(function(k){var v=params[k];if(Array.isArray(v))return v.map(function(x){return encodeURIComponent(k)+'='+encodeURIComponent(x)}).join('&');return encodeURIComponent(k)+'='+encodeURIComponent(v);}).join('&');
}
document.getElementById('parseBtn').addEventListener('click',compute);
document.getElementById('inputUrl').addEventListener('input',compute);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('inputUrl').value='';document.getElementById('parseResult').innerHTML='';});
document.getElementById('copyJson').addEventListener('click',function(){
  var json=document.getElementById('parseResult').dataset.json;
  if(json)navigator.clipboard.writeText(json).then(function(){showToast('JSON已复制 ✓')});
});
document.getElementById('copyQuery').addEventListener('click',function(){
  var q=document.getElementById('parseResult').dataset.query;
  if(q)navigator.clipboard.writeText(q).then(function(){showToast('查询字符串已复制 ✓')});
});
compute();
})();
'''
}

# 注入JS代码
for tool_dir, js_code in APP_CODES.items():
    for lang, path in [("CN", f"{BASE}/{tool_dir}/index.html"), ("EN", f"{BASE}/en/{tool_dir}/index.html")]:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在 showToast 和 copyText 定义之后插入 app 代码
        # 找到最后一个 </script> 之前的位置
        marker = '["catch"](function(){showToast("'
        if marker in content:
            # 找到这个函数结束后的位置
            pos = content.index(marker)
            # 找到这行结尾的 })\n 位置
            end_pos = content.index('\n', pos)
            # 再往后找 })(); 闭合
            search_from = end_pos
            while search_from < len(content):
                if '})();' in content[search_from:search_from+10]:
                    insert_pos = content.index('})();', search_from) + 5
                    break
                search_from += 1
            else:
                # fallback: 找到 </script> 之前
                insert_pos = content.rindex('</script>')
            
            new_content = content[:insert_pos] + '\n' + js_code + '\n' + content[insert_pos:]
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected JS: {path}")
        else:
            print(f"WARNING: marker not found in {path}")

print("\n✅ JS injection complete")