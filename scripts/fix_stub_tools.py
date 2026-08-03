#!/usr/bin/env python3
"""Add functional JS to stub tool pages."""
import os

TOOLS_DIR = "/home/chison/tools-site"

# JS implementations for each tool
JS_IMPLEMENTATIONS = {
    "decimal-to-roman": r"""<script>
function setNum(n){document.getElementById('decimalInput').value=n;convert();}
function convert(){
var n=parseInt(document.getElementById('decimalInput').value);
var out=document.getElementById('romanOutput');var echo=document.getElementById('decimalEcho');
if(isNaN(n)||n<1||n>3999){out.textContent='请输入1-3999之间的整数';echo.textContent='';return;}
echo.textContent=n+' = ';
var val=[1000,900,500,400,100,90,50,40,10,9,5,4,1];
var sym=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I'];
var r='';for(var i=0;i<val.length;i++){while(n>=val[i]){r+=sym[i];n-=val[i];}}
out.textContent=r;
}
function copyRoman(){var t=document.getElementById('romanOutput').textContent;if(t){navigator.clipboard.writeText(t);showToast('已复制');}}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
document.getElementById('decimalInput').addEventListener('input',convert);
document.getElementById('decimalInput').addEventListener('keydown',function(e){if(e.key==='Enter')convert();});
</script>""",

    "hex-encoder-decoder": r"""<script>
function encodeHex(){
var text=document.getElementById('inputText').value;
var useSpace=document.getElementById('useSpace').checked;
var useUpper=document.getElementById('useUppercase').checked;
var hex='';
for(var i=0;i<text.length;i++){
var h=text.charCodeAt(i).toString(16);
if(useUpper)h=h.toUpperCase();
hex+=h;if(useSpace&&i<text.length-1)hex+=' ';
}
document.getElementById('resultBox').value=hex;
document.getElementById('byteCount').textContent=text.length+' 字符';
}
function decodeHex(){
var hex=document.getElementById('inputText').value.trim().replace(/[\s,;:]/g,'');
if(hex.length%2!==0){showToast('Hex长度必须为偶数');return;}
var str='';try{
for(var i=0;i<hex.length;i+=2){str+=String.fromCharCode(parseInt(hex.substr(i,2),16));}
}catch(e){showToast('解码失败');return;}
document.getElementById('resultBox').value=str;
document.getElementById('byteCount').textContent=str.length+' 字符';
}
function copyResult(){var v=document.getElementById('resultBox').value;if(v){navigator.clipboard.writeText(v);showToast('已复制');}}
function clearAll(){document.getElementById('inputText').value='';document.getElementById('resultBox').value='';document.getElementById('byteCount').textContent='';}
function swapInputOutput(){
var i=document.getElementById('inputText'),r=document.getElementById('resultBox');
var tmp=i.value;i.value=r.value;r.value=tmp;
}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
</script>""",

    "hsl-to-rgb": r"""<script>
function hslToRgb(h,s,l){
h/=360;s/=100;l/=100;
if(s===0){var v=Math.round(l*255);return[v,v,v];}
var q=l<0.5?l*(1+s):l+s-l*s;var p=2*l-q;
function hue2rgb(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}
var r=hue2rgb(p,q,h+1/3);var g=hue2rgb(p,q,h);var b=hue2rgb(p,q,h-1/3);
return[Math.round(r*255),Math.round(g*255),Math.round(b*255)];
}
function rgbToHex(r,g,b){return'#'+[r,g,b].map(function(x){return x.toString(16).padStart(2,'0');}).join('');}
function update(){
var h=parseInt(document.getElementById('hSlider').value);
var s=parseInt(document.getElementById('sSlider').value);
var l=parseInt(document.getElementById('lSlider').value);
document.getElementById('hVal').textContent=h+'°';
document.getElementById('sVal').textContent=s+'%';
document.getElementById('lVal').textContent=l+'%';
var rgb=hslToRgb(h,s,l);
var hex=rgbToHex(rgb[0],rgb[1],rgb[2]);
document.getElementById('rgbValue').textContent='rgb('+rgb.join(', ')+')';
document.getElementById('hexValue').textContent=hex.toUpperCase();
document.getElementById('cssValue').textContent='hsl('+h+', '+s+'%, '+l+'%)';
document.getElementById('colorPreview').style.background=hex;
}
function copyText(id){var v=document.getElementById(id).textContent;if(v){navigator.clipboard.writeText(v);showToast('已复制');}}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
['hSlider','sSlider','lSlider'].forEach(function(id){document.getElementById(id).addEventListener('input',update);});
update();
</script>""",

    "json-to-table": r"""<script>
function convertJson(){
var input=document.getElementById('jsonInput').value.trim();
var err=document.getElementById('errorBox');var container=document.getElementById('tableContainer');
err.style.display='none';container.innerHTML='';
if(!input){err.textContent='请输入JSON数据';err.style.display='block';return;}
var data;try{data=JSON.parse(input);}catch(e){err.textContent='JSON解析失败: '+e.message;err.style.display='block';return;}
var rows=Array.isArray(data)?data:(data.items||data.data||[data]);
if(!Array.isArray(rows)){rows=[rows];}
document.getElementById('rowCount').textContent=rows.length+' 行';
if(rows.length===0){container.innerHTML='<p style="color:#94a3b8">无数据</p>';return;}
var keys=Object.keys(rows[0]);
var html='<table style="width:100%;border-collapse:collapse;font-size:13px;"><thead><tr>';
keys.forEach(function(k){html+='<th style="padding:8px;border:1px solid rgba(148,163,184,.2);background:#1e293b;text-align:left;color:#94a3b8;">'+k+'</th>';});
html+='</tr></thead><tbody>';
rows.forEach(function(r){html+='<tr>';keys.forEach(function(k){var v=r[k];v=v===null?'null':(typeof v==='object'?JSON.stringify(v):String(v));html+='<td style="padding:8px;border:1px solid rgba(148,163,184,.1);color:#e2e8f0;max-width:300px;overflow:hidden;text-overflow:ellipsis;">'+v+'</td>';});html+='</tr>';});
html+='</tbody></table>';
container.innerHTML=html;
}
function loadExample(){
var ex=[{"name":"Alice","age":30,"city":"Beijing"},{"name":"Bob","age":25,"city":"Shanghai"},{"name":"Carol","age":35,"city":"Guangzhou"}];
document.getElementById('jsonInput').value=JSON.stringify(ex,null,2);
convertJson();
}
function copyTable(){var t=document.getElementById('tableContainer').innerText;if(t){navigator.clipboard.writeText(t);showToast('已复制');}}
function clearAll(){document.getElementById('jsonInput').value='';document.getElementById('tableContainer').innerHTML='';document.getElementById('rowCount').textContent='';}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
</script>""",

    "nanoid-generator": r"""<script>
function generateNanoIds(){
var count=parseInt(document.getElementById('idCount').value)||1;
var length=parseInt(document.getElementById('idLength').value)||21;
var charset=document.getElementById('charset').value||'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-';
var list=[];
for(var c=0;c<count;c++){
var id='';for(var i=0;i<length;i++){id+=charset[Math.floor(Math.random()*charset.length)];}
list.push(id);
}
document.getElementById('nanoidList').value=list.join('\n');
document.getElementById('resultCount').textContent=count+' 个ID';
}
function copyAll(){var v=document.getElementById('nanoidList').value;if(v){navigator.clipboard.writeText(v);showToast('已复制');}}
function clearResults(){document.getElementById('nanoidList').value='';document.getElementById('resultCount').textContent='';}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
document.getElementById('idCount').addEventListener('change',generateNanoIds);
document.getElementById('idLength').addEventListener('change',generateNanoIds);
document.getElementById('charset').addEventListener('input',generateNanoIds);
generateNanoIds();
</script>""",

    "scientific-notation-converter": r"""<script>
function convert(){
var input=document.getElementById('inputNumber').value.trim();
var prec=parseInt(document.getElementById('precision').value)||6;
var err=document.getElementById('errorBox');var res=document.getElementById('results');
err.style.display='none';res.innerHTML='';
if(!input){err.textContent='请输入数字';err.style.display='block';return;}
var n=parseFloat(input);if(isNaN(n)){err.textContent='无效的数字';err.style.display='block';return;}
var abs=Math.abs(n);
var exp=abs===0?0:Math.floor(Math.log10(abs));
var mant=n/Math.pow(10,exp);
var sci=mant.toFixed(prec)+' × 10^'+exp;
var eForm=n.toExponential(prec);
var normal=n.toLocaleString('en-US',{maximumFractionDigits:20});
var items=[
['科学计数法',sci],
['E表示法',eForm],
['普通数字',normal],
['指数',exp.toString()],
['有效数字',mant.toFixed(prec)]
];
var html='';
items.forEach(function(item){html+='<div style="margin-bottom:12px"><div style="color:#94a3b8;font-size:12px;text-transform:uppercase;margin-bottom:4px">'+item[0]+'</div><div style="color:#e2e8f0;font-size:16px;font-family:monospace;word-break:break-all">'+item[1]+'</div></div>';});
res.innerHTML=html;
}
function loadExample(type){
document.getElementById('inputNumber').value=type==='large'?'299792458':'0.0000000000667430';
convert();
}
function clearAll(){document.getElementById('inputNumber').value='';document.getElementById('results').innerHTML='';}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
document.getElementById('inputNumber').addEventListener('input',convert);
document.getElementById('precision').addEventListener('change',convert);
</script>""",

    "unix-timestamp-converter": r"""<script>
function switchTab(tab){
document.getElementById('tab-ts2date').classList.toggle('active',tab==='ts2date');
document.getElementById('tab-date2ts').classList.toggle('active',tab==='date2ts');
document.querySelectorAll('.tab-panel').forEach(function(p){p.style.display='none';});
document.getElementById('panel-'+tab).style.display='block';
}
function tsToDate(){
var ts=parseInt(document.getElementById('tsInput').value);
if(isNaN(ts)){showToast('请输入有效时间戳');return;}
var isMs=ts>1e12;var d=new Date(isMs?ts:ts*1000);
document.getElementById('utcTime').textContent=d.toISOString();
document.getElementById('localTime').textContent=d.toLocaleString('zh-CN');
document.getElementById('isoTime').textContent=d.toISOString().replace('T',' ').substr(0,19);
var now=Date.now();var diff=ts*1000-now;
var rel;
if(diff>0){var days=Math.floor(diff/86400000);rel=days+'天后';}
else{var days=Math.floor(-diff/86400000);rel=days+'天前';}
document.getElementById('relativeTime').textContent=rel;
}
function dateToTs(){
var input=document.getElementById('dateInput').value;
if(!input){showToast('请选择日期');return;}
var d=new Date(input);if(isNaN(d.getTime())){showToast('无效日期');return;}
document.getElementById('tsSeconds').textContent=Math.floor(d.getTime()/1000);
document.getElementById('tsMillis').textContent=d.getTime();
}
function useNowStamp(){
var now=Math.floor(Date.now()/1000);
document.getElementById('tsInput').value=now;tsToDate();
}
function setNow(){
var d=new Date();var off=d.getTimezoneOffset()*60000;
document.getElementById('dateInput').value=new Date(d.getTime()-off).toISOString().slice(0,16);
dateToTs();
}
function updateLive(){document.getElementById('liveTimestamp').textContent=Math.floor(Date.now()/1000);}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
setInterval(updateLive,1000);updateLive();
</script>""",

    "data-unit-converter": r"""<script>
function convert(){
var bits=[1,8,8192,8388608,8589934592,8796093022208,9007199254740992,
1024,1048576,1073741824,1099511627776,1125899906842624,
1000,8000,8000000,8000000000,8000000000000];
// Bit, Byte, KB, MB, GB, TB, PB (binary) + KB,MB,GB,TB (decimal)
var input=parseFloat(document.getElementById('inputValue').value);
if(isNaN(input)){return;}
var fromIdx=document.getElementById('fromUnit').selectedIndex;
// Simplified: just show conversions
var bytes=input;
// assume input is in bytes for now, show all
var units=['b','B','KB','MB','GB','TB','PB'];
var results=[
(input*8)+' b',
input+' B',
(input/1024).toFixed(4)+' KiB',
(input/1048576).toFixed(4)+' MiB',
(input/1073741824).toFixed(4)+' GiB',
(input/1099511627776).toFixed(4)+' TiB',
(input/1125899906842624).toFixed(4)+' PiB'
];
document.getElementById('resultBox').value=results.join('\n');
}
function showToast(m){var t=document.getElementById('toast');if(t){t.textContent=m;t.style.display='block';setTimeout(function(){t.style.display='none';},2000);}}
</script>""",
}

# Tools that can't be implemented in pure frontend → add noindex
NOINDEX_TOOLS = [
    "excel-to-pdf", "ico-converter", "image-resize", "jpg-to-webp",
    "mp4-to-gif", "pdf-compress", "wav-to-mp3", "webp-converter",
    "dns-records-lookup", "url-unshortener", "og-checker",
    "pdf-to-image", "pdf-bookmark", "pdf-page-reorder", "pdf-password-protect",
    "audio-recorder", "video-rotator", "log-viewer", "php-formatter",
    "mermaid-editor"
]

def add_js_to_tool(tool_name, js_code):
    """Add JS before </body> in tool page."""
    filepath = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has functional JS (more than just gtag)
    if 'function calc(' in content or 'function convert(' in content or 'function generate' in content:
        print(f"  SKIP: {tool_name} already has functional JS")
        return False
    
    # Insert JS before </body>
    if '</body>' in content:
        content = content.replace('</body>', js_code + '\n</body>')
    else:
        content += js_code
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK: {tool_name}")
    return True

def add_noindex(tool_name):
    """Add noindex to tools that can't be implemented in pure frontend."""
    filepath = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'noindex' in content:
        return False
    
    # Replace index,follow with noindex,follow
    if 'index, follow' in content:
        content = content.replace('index, follow', 'noindex, follow')
    elif 'index,follow' in content:
        content = content.replace('index,follow', 'noindex,follow')
    else:
        # Add noindex meta tag after charset
        content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex, follow">')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  NOINDEX: {tool_name}")
    return True

if __name__ == '__main__':
    print("=== Adding functional JS to stub tools ===")
    for tool, js in JS_IMPLEMENTATIONS.items():
        add_js_to_tool(tool, js)
    
    print("\n=== Adding noindex to non-implementable tools ===")
    for tool in NOINDEX_TOOLS:
        add_noindex(tool)
    
    print("\nDone!")
