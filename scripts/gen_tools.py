#!/usr/bin/env python3
"""批量生成5个新工具的中英文HTML页面"""
import os, json, hashlib

# ============================================================
# TOOL DEFINITIONS
# ============================================================
TOOLS = []

# --- 1. rgb-to-hsl ---
TOOLS.append({
    "slug": "rgb-to-hsl",
    "cn": {
        "title": "RGB转HSL颜色转换器 - Free ToolBase",
        "desc": "免费在线RGB转HSL颜色转换器，支持实时颜色预览和一键复制。输入RGB值自动转换为HSL格式，无需注册，数据不上传服务器。",
        "kw": "RGB转HSL转换器,颜色转换,在线工具,免费",
        "h1": "🎨 RGB转HSL颜色转换器",
        "hero": "免费在线RGB转HSL颜色转换器，实时颜色预览和一键复制。 | 无需注册 · 数据绝不上传服务器",
        "schema_name": "RGB转HSL颜色转换器",
        "breadcrumb": "RGB转HSL颜色转换器",
        "usage_title": "使用说明",
        "usage": """<p>在RGB输入框中输入红(R)、绿(G)、蓝(B)的值（0-255），点击转换按钮自动计算对应的HSL值（色相H: 0-360, 饱和度S: 0-100%, 亮度L: 0-100%）。</p><p>支持颜色选择器可视化选色。一键复制HEX、RGB和HSL值。纯前端本地计算，数据绝不上传服务器。</p>""",
        "footer": "RGB转HSL颜色转换器 | 无需注册 · 数据绝不上传服务器",
        "canonical": "/rgb-to-hsl/",
        "en_alt": "/en/rgb-to-hsl/",
    },
    "en": {
        "title": "RGB to HSL Color Converter - Free ToolBase",
        "desc": "Free online RGB to HSL color converter with real-time preview and one-click copy. Enter RGB values to convert to HSL format instantly. No registration required.",
        "kw": "RGB to HSL converter,color converter,online tool,free",
        "h1": "🎨 RGB to HSL Color Converter",
        "hero": "Free online RGB to HSL color converter. Convert RGB values to HSL instantly. Real-time color preview. | No registration · All processing done locally",
        "schema_name": "RGB to HSL Color Converter",
        "breadcrumb": "RGB to HSL Color Converter",
        "usage_title": "How to Use",
        "usage": """<p>Enter Red (R), Green (G), and Blue (B) values (0-255) and click Convert to see HSL values (Hue: 0-360, Saturation: 0-100%, Lightness: 0-100%).</p><p>Use the color picker for visual selection. One-click copy of HEX, RGB, and HSL values. All processing done locally in your browser.</p>""",
        "footer": "RGB to HSL Color Converter | No registration · All processing done locally",
        "canonical": "/en/rgb-to-hsl/",
        "en_alt": "/en/rgb-to-hsl/",
    },
    "html_body_cn": """<div class="input-section"><h2>🔴🟢🔵 RGB Input</h2><div class="row"><div class="field"><label>Red (R) 0-255</label><input type="number" id="rIn" min="0" max="255" value="255" placeholder="255"></div><div class="field"><label>Green (G) 0-255</label><input type="number" id="gIn" min="0" max="255" value="107" placeholder="107"></div><div class="field"><label>Blue (B) 0-255</label><input type="number" id="bIn" min="0" max="255" value="107" placeholder="107"></div></div><div class="field"><label>Or pick a color: <input type="color" id="colorPicker" value="#ff6b6b"></label></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 转换 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 转换结果 Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>HEX:</strong> <span id="hexResult">#ff6b6b</span></div><div><strong>RGB:</strong> <span id="rgbResult">rgb(255,107,107)</span></div><div><strong>HSL:</strong> <span id="hslResult">hsl(0, 100%, 71%)</span></div><div><strong>细分:</strong> H=<span id="hVal">0</span>° S=<span id="sVal">100</span>% L=<span id="lVal">71</span>%</div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 复制 HEX</button><button class="btn btn-success" id="copyRgb">📋 复制 RGB</button><button class="btn btn-success" id="copyHsl">📋 复制 HSL</button></div></div>""",
    "html_body_en": """<div class="input-section"><h2>🔴🟢🔵 RGB Input</h2><div class="row"><div class="field"><label>Red (R) 0-255</label><input type="number" id="rIn" min="0" max="255" value="255" placeholder="255"></div><div class="field"><label>Green (G) 0-255</label><input type="number" id="gIn" min="0" max="255" value="107" placeholder="107"></div><div class="field"><label>Blue (B) 0-255</label><input type="number" id="bIn" min="0" max="255" value="107" placeholder="107"></div></div><div class="field"><label>Or pick a color: <input type="color" id="colorPicker" value="#ff6b6b"></label></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>HEX:</strong> <span id="hexResult">#ff6b6b</span></div><div><strong>RGB:</strong> <span id="rgbResult">rgb(255,107,107)</span></div><div><strong>HSL:</strong> <span id="hslResult">hsl(0, 100%, 71%)</span></div><div><strong>Breakdown:</strong> H=<span id="hVal">0</span>° S=<span id="sVal">100</span>% L=<span id="lVal">71</span>%</div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 Copy HEX</button><button class="btn btn-success" id="copyRgb">📋 Copy RGB</button><button class="btn btn-success" id="copyHsl">📋 Copy HSL</button></div></div>""",
    "js": """
function rgbToHsl(r,g,b){r/=255;g/=255;b/=255;var max=Math.max(r,g,b),min=Math.min(r,g,b);var h,s,l=(max+min)/2;if(max===min){h=s=0;}else{var d=max-min;s=l>0.5?d/(2-max-min):d/(max+min);switch(max){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;case b:h=(r-g)/d+4;break;}h/=6;}return{h:Math.round(h*360),s:Math.round(s*100),l:Math.round(l*100)};}
function hslToRgb(h,s,l){h/=360;s/=100;l/=100;var r,g,b;if(s===0){r=g=b=l;}else{var hue2rgb=function(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;};var q=l<0.5?l*(1+s):l+s-l*s;var p=2*l-q;r=hue2rgb(p,q,h+1/3);g=hue2rgb(p,q,h);b=hue2rgb(p,q,h-1/3);}return{r:Math.round(r*255),g:Math.round(g*255),b:Math.round(b*255)};}
function convert(){var r=_pI('rIn'),g=_pI('gIn'),b=_pI('bIn');var hsl=rgbToHsl(r,g,b);document.getElementById('hslResult').textContent='hsl('+hsl.h+', '+hsl.s+'%, '+hsl.l+'%)';document.getElementById('hVal').textContent=hsl.h;document.getElementById('sVal').textContent=hsl.s;document.getElementById('lVal').textContent=hsl.l;var hex='#'+[r,g,b].map(function(x){var hx=Math.round(x).toString(16);return hx.length===1?'0'+hx:hx;}).join('');document.getElementById('hexResult').textContent=hex;document.getElementById('rgbResult').textContent='rgb('+r+', '+g+', '+b+')';document.getElementById('previewBox').style.backgroundColor='rgb('+r+','+g+','+b+')';window._lastColor={hex:hex,rgb:'rgb('+r+', '+g+', '+b+')',hsl:'hsl('+hsl.h+', '+hsl.s+'%, '+hsl.l+'%)'};}
function _pI(id){var v=parseInt(document.getElementById(id).value,10);return isNaN(v)?0:Math.max(0,Math.min(255,v));}
""",
})

# --- 2. hsv-to-rgb ---
TOOLS.append({
    "slug": "hsv-to-rgb",
    "cn": {
        "title": "HSV转RGB颜色转换器 - Free ToolBase",
        "desc": "免费在线HSV转RGB颜色转换器，输入HSV值（色相、饱和度、明度）自动转换为RGB和HEX格式。支持实时颜色预览，无需注册，数据不上传服务器。",
        "kw": "HSV转RGB转换器,颜色转换,在线工具,免费",
        "h1": "🎨 HSV转RGB颜色转换器",
        "hero": "免费在线HSV转RGB颜色转换器，实时颜色预览和一键复制。 | 无需注册 · 数据绝不上传服务器",
        "schema_name": "HSV转RGB颜色转换器",
        "breadcrumb": "HSV转RGB颜色转换器",
        "usage_title": "使用说明",
        "usage": """<p>输入HSV值：H(色相0-360°)、S(饱和度0-100%)、V(明度0-100%)，系统自动转换为RGB和HEX格式。</p><p>纯前端计算，实时颜色预览。支持一键复制RGB和HEX值。数据绝不上传服务器。</p>""",
        "footer": "HSV转RGB颜色转换器 | 无需注册 · 数据绝不上传服务器",
        "canonical": "/hsv-to-rgb/",
        "en_alt": "/en/hsv-to-rgb/",
    },
    "en": {
        "title": "HSV to RGB Color Converter - Free ToolBase",
        "desc": "Free online HSV to RGB color converter. Enter HSV values (Hue, Saturation, Value) to convert to RGB and HEX formats instantly. Real-time color preview, no registration required.",
        "kw": "HSV to RGB converter,color converter,online tool,free",
        "h1": "🎨 HSV to RGB Color Converter",
        "hero": "Free online HSV to RGB color converter. Convert HSV values to RGB and HEX instantly. Real-time color preview. | No registration · All processing done locally",
        "schema_name": "HSV to RGB Color Converter",
        "breadcrumb": "HSV to RGB Color Converter",
        "usage_title": "How to Use",
        "usage": """<p>Enter HSV values: H (Hue 0-360°), S (Saturation 0-100%), V (Value 0-100%) to convert to RGB and HEX formats.</p><p>All computation done locally in your browser. Real-time color preview with one-click copy of RGB and HEX values.</p>""",
        "footer": "HSV to RGB Color Converter | No registration · All processing done locally",
        "canonical": "/en/hsv-to-rgb/",
        "en_alt": "/en/hsv-to-rgb/",
    },
    "html_body_cn": """<div class="input-section"><h2>🎨 HSV Input</h2><div class="row"><div class="field"><label>色相 Hue (H) 0-360°</label><input type="number" id="hIn" min="0" max="360" value="0" placeholder="0"></div><div class="field"><label>饱和度 Saturation (S) 0-100%</label><input type="number" id="sIn" min="0" max="100" value="80" placeholder="80"></div><div class="field"><label>明度 Value (V) 0-100%</label><input type="number" id="vIn" min="0" max="100" value="100" placeholder="100"></div></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 转换 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 转换结果 Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>RGB:</strong> <span id="rgbResult">rgb(51, 0, 255)</span></div><div><strong>HEX:</strong> <span id="hexResult">#3300ff</span></div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 复制 HEX</button><button class="btn btn-success" id="copyRgb">📋 复制 RGB</button></div></div>""",
    "html_body_en": """<div class="input-section"><h2>🎨 HSV Input</h2><div class="row"><div class="field"><label>Hue (H) 0-360°</label><input type="number" id="hIn" min="0" max="360" value="0" placeholder="0"></div><div class="field"><label>Saturation (S) 0-100%</label><input type="number" id="sIn" min="0" max="100" value="80" placeholder="80"></div><div class="field"><label>Value (V) 0-100%</label><input type="number" id="vIn" min="0" max="100" value="100" placeholder="100"></div></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>RGB:</strong> <span id="rgbResult">rgb(51, 0, 255)</span></div><div><strong>HEX:</strong> <span id="hexResult">#3300ff</span></div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 Copy HEX</button><button class="btn btn-success" id="copyRgb">📋 Copy RGB</button></div></div>""",
    "js": """
function hsvToRgb(h,s,v){h/=360;s/=100;v/=100;var r,g,b;var i=Math.floor(h*6);var f=h*6-i;var p=v*(1-s);var q=v*(1-f*s);var t=v*(1-(1-f)*s);switch(i%6){case 0:r=v;g=t;b=p;break;case 1:r=q;g=v;b=p;break;case 2:r=p;g=v;b=t;break;case 3:r=p;g=q;b=v;break;case 4:r=t;g=p;b=v;break;case 5:r=v;g=p;b=q;break;}return{r:Math.round(r*255),g:Math.round(g*255),b:Math.round(b*255)};}
function convert(){var h=_pF('hIn',0,360),s=_pF('sIn',0,100),v=_pF('vIn',0,100);var rgb=hsvToRgb(h,s,v);var hex='#'+[rgb.r,rgb.g,rgb.b].map(function(x){var hx=Math.round(x).toString(16);return hx.length===1?'0'+hx:hx;}).join('');document.getElementById('rgbResult').textContent='rgb('+rgb.r+', '+rgb.g+', '+rgb.b+')';document.getElementById('hexResult').textContent=hex;document.getElementById('previewBox').style.backgroundColor='rgb('+rgb.r+','+rgb.g+','+rgb.b+')';window._lastColor={hex:hex,rgb:'rgb('+rgb.r+', '+rgb.g+', '+rgb.b+')'};}
function _pF(id,min,max){var v=parseFloat(document.getElementById(id).value);if(isNaN(v))return 0;return Math.max(min,Math.min(max,v));}
""",
})

# --- 3. rgb-to-hsv ---
TOOLS.append({
    "slug": "rgb-to-hsv",
    "cn": {
        "title": "RGB转HSV颜色转换器 - Free ToolBase",
        "desc": "免费在线RGB转HSV颜色转换器，输入RGB值自动转换为HSV格式。支持实时颜色预览和一键复制，无需注册，数据不上传服务器。",
        "kw": "RGB转HSV转换器,颜色转换,在线工具,免费",
        "h1": "🎯 RGB转HSV颜色转换器",
        "hero": "免费在线RGB转HSV颜色转换器，实时颜色预览和一键复制。 | 无需注册 · 数据绝不上传服务器",
        "schema_name": "RGB转HSV颜色转换器",
        "breadcrumb": "RGB转HSV颜色转换器",
        "usage_title": "使用说明",
        "usage": """<p>输入红(R)、绿(G)、蓝(B)值（0-255），系统自动计算并显示对应的HSV值（H:0-360°, S:0-100%, V:0-100%）。</p><p>支持颜色选择器可视化选色，一键复制HEX、RGB和HSV值。纯前端本地计算。</p>""",
        "footer": "RGB转HSV颜色转换器 | 无需注册 · 数据绝不上传服务器",
        "canonical": "/rgb-to-hsv/",
        "en_alt": "/en/rgb-to-hsv/",
    },
    "en": {
        "title": "RGB to HSV Color Converter - Free ToolBase",
        "desc": "Free online RGB to HSV color converter. Enter RGB values to convert to HSV format instantly. Real-time color preview with one-click copy, no registration required.",
        "kw": "RGB to HSV converter,color converter,online tool,free",
        "h1": "🎯 RGB to HSV Color Converter",
        "hero": "Free online RGB to HSV color converter. Convert RGB values to HSV format instantly. | No registration · All processing done locally",
        "schema_name": "RGB to HSV Color Converter",
        "breadcrumb": "RGB to HSV Color Converter",
        "usage_title": "How to Use",
        "usage": """<p>Enter Red (R), Green (G), and Blue (B) values (0-255) to automatically convert to HSV format (Hue: 0-360°, Saturation: 0-100%, Value: 0-100%).</p><p>Supports color picker for visual selection, one-click copy of HEX, RGB, and HSV values. All processing done locally.</p>""",
        "footer": "RGB to HSV Color Converter | No registration · All processing done locally",
        "canonical": "/en/rgb-to-hsv/",
        "en_alt": "/en/rgb-to-hsv/",
    },
    "html_body_cn": """<div class="input-section"><h2>🔴🟢🔵 RGB Input</h2><div class="row"><div class="field"><label>Red (R) 0-255</label><input type="number" id="rIn" min="0" max="255" value="51" placeholder="51"></div><div class="field"><label>Green (G) 0-255</label><input type="number" id="gIn" min="0" max="255" value="204" placeholder="204"></div><div class="field"><label>Blue (B) 0-255</label><input type="number" id="bIn" min="0" max="255" value="255" placeholder="255"></div></div><div class="field"><label>或使用颜色选择器: <input type="color" id="colorPicker" value="#33ccff"></label></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 转换 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 转换结果 Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>HEX:</strong> <span id="hexResult">#33ccff</span></div><div><strong>RGB:</strong> <span id="rgbResult">rgb(51,204,255)</span></div><div><strong>HSV:</strong> <span id="hsvResult">hsv(195, 80%, 100%)</span></div><div><strong>细分:</strong> H=<span id="hVal">195</span>° S=<span id="sVal">80</span>% V=<span id="vVal">100</span>%</div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 复制 HEX</button><button class="btn btn-success" id="copyRgb">📋 复制 RGB</button><button class="btn btn-success" id="copyHsv">📋 复制 HSV</button></div></div>""",
    "html_body_en": """<div class="input-section"><h2>🔴🟢🔵 RGB Input</h2><div class="row"><div class="field"><label>Red (R) 0-255</label><input type="number" id="rIn" min="0" max="255" value="51" placeholder="51"></div><div class="field"><label>Green (G) 0-255</label><input type="number" id="gIn" min="0" max="255" value="204" placeholder="204"></div><div class="field"><label>Blue (B) 0-255</label><input type="number" id="bIn" min="0" max="255" value="255" placeholder="255"></div></div><div class="field"><label>Or pick a color: <input type="color" id="colorPicker" value="#33ccff"></label></div><div class="btn-row"><button class="btn btn-primary" id="convBtn">🔄 Convert</button></div></div><div class="result-section show" id="resultSection"><h2>✅ Conversion Results</h2><div id="previewBox" style="width:100%;height:80px;border-radius:12px;margin-bottom:12px;border:2px solid rgba(148,163,184,.2)"></div><div class="result-box" id="convResults"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><strong>HEX:</strong> <span id="hexResult">#33ccff</span></div><div><strong>RGB:</strong> <span id="rgbResult">rgb(51,204,255)</span></div><div><strong>HSV:</strong> <span id="hsvResult">hsv(195, 80%, 100%)</span></div><div><strong>Breakdown:</strong> H=<span id="hVal">195</span>° S=<span id="sVal">80</span>% V=<span id="vVal">100</span>%</div></div></div><div class="btn-row"><button class="btn btn-success" id="copyHex">📋 Copy HEX</button><button class="btn btn-success" id="copyRgb">📋 Copy RGB</button><button class="btn btn-success" id="copyHsv">📋 Copy HSV</button></div></div>""",
    "js": """
function rgbToHsv(r,g,b){r/=255;g/=255;b/=255;var max=Math.max(r,g,b),min=Math.min(r,g,b);var h,s,v=max;var d=max-min;s=max===0?0:d/max;if(max===min){h=0;}else{switch(max){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;case b:h=(r-g)/d+4;break;}h/=6;}return{h:Math.round(h*360),s:Math.round(s*100),v:Math.round(v*100)};}
function convert(){var r=_pI('rIn'),g=_pI('gIn'),b=_pI('bIn');var hsv=rgbToHsv(r,g,b);document.getElementById('hsvResult').textContent='hsv('+hsv.h+', '+hsv.s+'%, '+hsv.v+'%)';document.getElementById('hVal').textContent=hsv.h;document.getElementById('sVal').textContent=hsv.s;document.getElementById('vVal').textContent=hsv.v;var hex='#'+[r,g,b].map(function(x){var hx=Math.round(x).toString(16);return hx.length===1?'0'+hx:hx;}).join('');document.getElementById('hexResult').textContent=hex;document.getElementById('rgbResult').textContent='rgb('+r+', '+g+', '+b+')';document.getElementById('previewBox').style.backgroundColor='rgb('+r+','+g+','+b+')';window._lastColor={hex:hex,rgb:'rgb('+r+', '+g+', '+b+')',hsv:'hsv('+hsv.h+', '+hsv.s+'%, '+hsv.v+'%)'};}
function _pI(id){var v=parseInt(document.getElementById(id).value,10);return isNaN(v)?0:Math.max(0,Math.min(255,v));}
""",
})

# --- 4. sql-minifier ---
TOOLS.append({
    "slug": "sql-minifier",
    "cn": {
        "title": "SQL压缩/美化工具 - Free ToolBase",
        "desc": "免费在线SQL压缩和格式化工具，支持SQL压缩（移除多余空格和注释）和美化（自动缩进）。兼容MySQL、PostgreSQL、SQLite等，无需注册，数据不上传服务器。",
        "kw": "SQL压缩,SQL格式化,SQL美化,在线工具,免费",
        "h1": "🗜️ SQL压缩/美化工具",
        "hero": "免费SQL压缩和格式化工具，支持压缩和美化两种模式。 | 无需注册 · 数据绝不上传服务器",
        "schema_name": "SQL压缩美化工具",
        "breadcrumb": "SQL压缩美化工具",
        "usage_title": "使用说明",
        "usage": """<p>粘贴SQL语句到输入框，选择压缩或美化模式后点击处理。</p><p><strong>压缩模式</strong>：移除所有多余空格、换行和注释（-- 和 /* */），生成最紧凑的SQL。<strong>美化模式</strong>：自动缩进和格式化关键词，使SQL结构清晰可读。纯前端处理。</p>""",
        "footer": "SQL压缩/美化工具 | 无需注册 · 数据绝不上传服务器",
        "canonical": "/sql-minifier/",
        "en_alt": "/en/sql-minifier/",
    },
    "en": {
        "title": "SQL Minifier & Formatter - Free ToolBase",
        "desc": "Free online SQL minifier and formatter. Compress SQL by removing extra whitespace and comments, or beautify SQL with automatic indentation. Supports MySQL, PostgreSQL, SQLite, and more.",
        "kw": "SQL minifier,SQL formatter,SQL beautifier,online tool,free",
        "h1": "🗜️ SQL Minifier & Formatter",
        "hero": "Free SQL minifier and formatter. Compress or beautify your SQL queries. | No registration · All processing done locally",
        "schema_name": "SQL Minifier & Formatter",
        "breadcrumb": "SQL Minifier & Formatter",
        "usage_title": "How to Use",
        "usage": """<p>Paste your SQL into the input box, choose Minify or Beautify mode, and click Process.</p><p><strong>Minify</strong>: Removes all extra whitespace, newlines, and comments (-- and /* */) for the most compact SQL. <strong>Beautify</strong>: Auto-indents and formats keywords for readability. All processing done locally.</p>""",
        "footer": "SQL Minifier & Formatter | No registration · All processing done locally",
        "canonical": "/en/sql-minifier/",
        "en_alt": "/en/sql-minifier/",
    },
    "html_body_cn": """<div class="input-section"><h2>📝 SQL 输入</h2><textarea id="sqlInput" placeholder="在此粘贴SQL语句..." style="min-height:180px">SELECT id, name, email
FROM users
WHERE status = 'active' AND created_at > '2024-01-01'
ORDER BY name ASC;</textarea><div class="options"><label><input type="radio" name="mode" value="minify" checked> 🗜️ 压缩 Minify</label><label><input type="radio" name="mode" value="beautify"> ✨ 美化 Beautify</label></div><div class="btn-row"><button class="btn btn-primary" id="procBtn">🔄 处理 Process</button><button class="btn btn-secondary" id="clearBtn">🗑 清空 Clear</button></div></div><div class="result-section show" id="resultSection"><h2>✅ 结果 Output <span style="font-weight:normal;font-size:.85rem;color:#64748b">(<span id="charCount">0</span> 字符)</span></h2><textarea id="sqlOutput" readonly style="min-height:180px;font-family:monospace"></textarea><div class="btn-row"><button class="btn btn-success" id="copyBtn">📋 复制结果</button></div></div>""",
    "html_body_en": """<div class="input-section"><h2>📝 SQL Input</h2><textarea id="sqlInput" placeholder="Paste your SQL here..." style="min-height:180px">SELECT id, name, email
FROM users
WHERE status = 'active' AND created_at > '2024-01-01'
ORDER BY name ASC;</textarea><div class="options"><label><input type="radio" name="mode" value="minify" checked> 🗜️ Minify</label><label><input type="radio" name="mode" value="beautify"> ✨ Beautify</label></div><div class="btn-row"><button class="btn btn-primary" id="procBtn">🔄 Process</button><button class="btn btn-secondary" id="clearBtn">🗑 Clear</button></div></div><div class="result-section show" id="resultSection"><h2>✅ Output <span style="font-weight:normal;font-size:.85rem;color:#64748b">(<span id="charCount">0</span> chars)</span></h2><textarea id="sqlOutput" readonly style="min-height:180px;font-family:monospace"></textarea><div class="btn-row"><button class="btn btn-success" id="copyBtn">📋 Copy Result</button></div></div>""",
    "js": """
function minifySql(sql){return sql.replace(/--.*$/gm,'').replace(/\\/\\*[\\s\\S]*?\\*\\//g,'').replace(/\\s+/g,' ').trim();}
function beautifySql(sql){var keywords=['SELECT','FROM','WHERE','AND','OR','INNER JOIN','LEFT JOIN','RIGHT JOIN','OUTER JOIN','ON','ORDER BY','GROUP BY','HAVING','LIMIT','OFFSET','INSERT INTO','VALUES','UPDATE','SET','DELETE FROM','CREATE TABLE','ALTER TABLE','DROP TABLE','UNION','UNION ALL','AS','CASE','WHEN','THEN','ELSE','END','IN','NOT IN','EXISTS','BETWEEN','LIKE','IS NULL','IS NOT NULL','COUNT','SUM','AVG','MAX','MIN','DISTINCT','CROSS JOIN','FULL JOIN','ASC','DESC','NULL','NOT NULL','PRIMARY KEY','FOREIGN KEY','REFERENCES','DEFAULT','UNIQUE','INDEX','IF','BEGIN','COMMIT','ROLLBACK'];var s=sql.replace(/\\b(\\w+)\\b/g,function(m){var u=m.toUpperCase();return keywords.includes(u)?u:m;});s=s.replace(/(\\b(SELECT|FROM|WHERE|ORDER BY|GROUP BY|HAVING|SET|VALUES|ON|AND|OR|UNION|UNION ALL|LEFT JOIN|RIGHT JOIN|INNER JOIN|OUTER JOIN|CROSS JOIN|FULL JOIN|INSERT INTO|DELETE FROM|CREATE TABLE|ALTER TABLE|DROP TABLE|LIMIT|OFFSET|CASE|WHEN|ELSE|END|BEGIN|COMMIT|ROLLBACK)\\b)/gi,'\\n$1');s=s.replace(/\\(\\s*/g,'(\\n  ').replace(/\\s*\\)/g,'\\n)').replace(/,\\s*/g,',\\n  ');s=s.replace(/\\n\\s*\\n/g,'\\n').trim();var lines=s.split('\\n'),result=[],indent=0;for(var i=0;i<lines.length;i++){var line=lines[i].trim();if(!line)continue;if(/^\\)/.test(line)||/^END\\b/.test(line)||/^ELSE\\b/.test(line))indent=Math.max(0,indent-1);result.push('  '.repeat(indent)+line);if(/\\($/.test(line)&&!/\\)/.test(line)||/^CASE\\b/.test(line)||/^(SELECT|INSERT INTO|CREATE TABLE|BEGIN)\\b/.test(line)&&!/\\)/.test(line))indent++;}return result.join('\\n');}
function process(){var sql=document.getElementById('sqlInput').value;var mode=document.querySelector('input[name=mode]:checked').value;var result=mode==='minify'?minifySql(sql):beautifySql(sql);document.getElementById('sqlOutput').value=result;document.getElementById('charCount').textContent=result.length;}
""",
})

# --- 5. percent-change ---
TOOLS.append({
    "slug": "percent-change",
    "cn": {
        "title": "百分比变化计算器 - Free ToolBase",
        "desc": "免费在线百分比变化计算器，计算两个数值之间的百分比增减。支持增长率和下降率计算、反向推算新值。适合财务分析、销售增长、股票涨跌等场景。",
        "kw": "百分比变化计算器,增长率计算,下降率计算,在线工具,免费",
        "h1": "📊 百分比变化计算器",
        "hero": "免费在线百分比变化计算器，计算增长率和下降率。 | 无需注册 · 数据绝不上传服务器",
        "schema_name": "百分比变化计算器",
        "breadcrumb": "百分比变化计算器",
        "usage_title": "使用说明",
        "usage": """<p>输入原始值和新值，自动计算百分比变化。</p><p>公式: (新值 - 原始值) / |原始值| × 100%。正数表示增长📈，负数表示下降📉。也支持反向计算：从原始值和百分比变化推算新值。纯前端计算。</p>""",
        "footer": "百分比变化计算器 | 无需注册 · 数据绝不上传服务器",
        "canonical": "/percent-change/",
        "en_alt": "/en/percent-change/",
    },
    "en": {
        "title": "Percentage Change Calculator - Free ToolBase",
        "desc": "Free online percentage change calculator. Calculate the percentage increase or decrease between two values. Supports reverse calculation from original value and percentage. Perfect for finance, sales, stocks.",
        "kw": "percentage change calculator,growth rate calculator,decrease rate calculator,online tool,free",
        "h1": "📊 Percentage Change Calculator",
        "hero": "Free online percentage change calculator. Calculate increase and decrease rates. | No registration · All processing done locally",
        "schema_name": "Percentage Change Calculator",
        "breadcrumb": "Percentage Change Calculator",
        "usage_title": "How to Use",
        "usage": """<p>Enter the original value and new value to automatically calculate the percentage change.</p><p>Formula: (New - Original) / |Original| × 100%. Positive = increase 📈, negative = decrease 📉. Also supports reverse calculation: from original value and percentage change to new value. All computation done locally.</p>""",
        "footer": "Percentage Change Calculator | No registration · All processing done locally",
        "canonical": "/en/percent-change/",
        "en_alt": "/en/percent-change/",
    },
    "html_body_cn": """<div class="input-section"><h2>📊 计算百分比变化</h2><div class="row"><div class="field"><label>原始值</label><input type="number" id="origVal" step="any" value="100" placeholder="例如 100"></div><div class="field"><label>新值</label><input type="number" id="newVal" step="any" value="125" placeholder="例如 125"></div></div><div class="btn-row"><button class="btn btn-primary" id="calcBtn">🔄 计算 Calculate</button></div><div class="result-box" style="margin-top:12px"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;text-align:center"><div><div style="color:#94a3b8;font-size:.8rem">百分比变化</div><div style="font-size:1.4rem;font-weight:700" id="changePct">+25.00%</div></div><div><div style="color:#94a3b8;font-size:.8rem">绝对变化</div><div style="font-size:1.4rem;font-weight:700" id="absDiff">+25.00</div></div><div><div style="color:#94a3b8;font-size:.8rem">趋势</div><div style="font-size:1.4rem;font-weight:700;color:#4ade80" id="trend">📈 增长</div></div></div></div></div><div class="input-section"><h2>🔄 反向计算：从百分比推算新值</h2><div class="row"><div class="field"><label>原始值</label><input type="number" id="origVal2" step="any" value="200" placeholder="例如 200"></div><div class="field"><label>百分比变化 (%)</label><input type="number" id="pctInput" step="any" value="15" placeholder="例如 15 表示 +15%"></div></div><div class="btn-row"><button class="btn btn-secondary" id="revBtn">🔄 计算新值</button></div><div class="result-box" style="margin-top:12px"><div style="text-align:center"><div style="color:#94a3b8;font-size:.8rem">结果值</div><div style="font-size:1.4rem;font-weight:700" id="reverseResult">230.0000</div></div></div></div>""",
    "html_body_en": """<div class="input-section"><h2>📊 Calculate Percentage Change</h2><div class="row"><div class="field"><label>Original Value</label><input type="number" id="origVal" step="any" value="100" placeholder="e.g. 100"></div><div class="field"><label>New Value</label><input type="number" id="newVal" step="any" value="125" placeholder="e.g. 125"></div></div><div class="btn-row"><button class="btn btn-primary" id="calcBtn">🔄 Calculate</button></div><div class="result-box" style="margin-top:12px"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;text-align:center"><div><div style="color:#94a3b8;font-size:.8rem">Percentage Change</div><div style="font-size:1.4rem;font-weight:700" id="changePct">+25.00%</div></div><div><div style="color:#94a3b8;font-size:.8rem">Absolute Change</div><div style="font-size:1.4rem;font-weight:700" id="absDiff">+25.00</div></div><div><div style="color:#94a3b8;font-size:.8rem">Trend</div><div style="font-size:1.4rem;font-weight:700;color:#4ade80" id="trend">📈 Increase</div></div></div></div></div><div class="input-section"><h2>🔄 Reverse: From % Change to New Value</h2><div class="row"><div class="field"><label>Original Value</label><input type="number" id="origVal2" step="any" value="200" placeholder="e.g. 200"></div><div class="field"><label>Percentage Change (%)</label><input type="number" id="pctInput" step="any" value="15" placeholder="e.g. 15 for +15%"></div></div><div class="btn-row"><button class="btn btn-secondary" id="revBtn">🔄 Calculate New Value</button></div><div class="result-box" style="margin-top:12px"><div style="text-align:center"><div style="color:#94a3b8;font-size:.8rem">Resulting Value</div><div style="font-size:1.4rem;font-weight:700" id="reverseResult">230.0000</div></div></div></div>""",
    "js": """
function calcChange(){var orig=_pF2('origVal'),newV=_pF2('newVal');if(orig===null||newV===null)return;var diff=newV-orig;var pct=orig!==0?(diff/Math.abs(orig)*100):0;document.getElementById('changePct').textContent=pct>=0?'+'+pct.toFixed(2)+'%':pct.toFixed(2)+'%';document.getElementById('absDiff').textContent=diff>=0?'+'+diff.toFixed(4):diff.toFixed(4);if(pct>0){document.getElementById('trend').textContent='📈 增长 Increase';document.getElementById('trend').style.color='#4ade80';}else if(pct<0){document.getElementById('trend').textContent='📉 下降 Decrease';document.getElementById('trend').style.color='#f87171';}else{document.getElementById('trend').textContent='➡ 无变化 No change';document.getElementById('trend').style.color='#94a3b8';}}
function calcReverse(){var orig=_pF2('origVal2'),pct=_pF2('pctInput');if(orig===null||pct===null)return;var result=orig*(1+pct/100);document.getElementById('reverseResult').textContent=result.toFixed(4);}
function _pF2(id){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?null:v;}
""",
})

# ============================================================
# HTML GENERATION
# ============================================================

BASE_DIR = "/home/chison/tools-site"

CSS_BLOCK = """*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:900px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.input-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.input-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
select{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}
select:focus{outline:none;border-color:rgba(6,182,212,.5)}
label{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}
input[type=text],input[type=number]{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}
input:focus{outline:none;border-color:rgba(6,182,212,.5)}
input[type=color]{width:48px;height:40px;padding:2px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;cursor:pointer;margin-bottom:12px}
textarea{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit;resize:vertical;min-height:100px;margin-bottom:12px}
textarea:focus{outline:none;border-color:rgba(6,182,212,.5)}
.options{display:flex;gap:12px;align-items:center;margin:12px 0;flex-wrap:wrap}
.options label{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#94a3b8;cursor:pointer;margin-bottom:0}
.options input[type=checkbox],.options input[type=radio]{accent-color:#06b6d4}
.row{display:flex;gap:12px;flex-wrap:wrap}
.row .field{flex:1;min-width:140px}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}
.btn-success:hover{background:rgba(34,197,94,.25)}
.result-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}
.result-section.show{display:block}
.result-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.result-box{background:#0f172a;border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(148,163,184,.08);overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;font-size:.85rem}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.table-wrap{overflow-x:auto;margin:8px 0}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}
.toast.show{opacity:1}
@media(max-width:600px){.row{flex-direction:column}.header h1{font-size:1.2rem}}
"""

GA_SCRIPT = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>"""

COMMON_JS = """function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2000)}
function copyText(id){var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){showToast("已复制")})["catch"](function(){showToast("复制失败")})}
"""

def generate_page(tool, lang):
    """Generate HTML for one language version"""
    t = tool[lang]
    slug = tool["slug"]
    
    # Language-specific values
    if lang == "cn":
        html_lang = "zh-CN"
        en_path = f"/en/{slug}/"
        lang_switch_cn = "中文"
        lang_switch_en = "EN"
        cn_active = "active"
        en_active = ""
        home_path = "../index.html"
        tools_path = "../index.html#tools"
        home_label = "首页"
        tools_label = "工具"
        contact_label = "联系我们"
        privacy_label = "隐私政策"
        terms_label = "服务条款"
        about_label = "关于我们"
        all_tools_label = "全部工具"
        faq_title = "常见问题"
        copy_hex = "复制 HEX"
        copy_rgb = "复制 RGB"
        copy_hsl = "复制 HSL"
        copy_hsv = "复制 HSV"
        copy_result = "复制结果"
        en_link = f"../en/{slug}/"
        en_label = "EN"
    else:
        html_lang = "en"
        en_path = f"/en/{slug}/"
        lang_switch_cn = "中文"
        lang_switch_en = "EN"
        cn_active = ""
        en_active = "active"
        home_path = "../../index.html"
        tools_path = "../../index.html#tools"
        home_label = "Home"
        tools_label = "Tools"
        contact_label = "Contact"
        privacy_label = "Privacy"
        terms_label = "Terms"
        about_label = "About"
        all_tools_label = "All Tools"
        faq_title = "FAQ"
        copy_hex = "Copy HEX"
        copy_rgb = "Copy RGB"
        copy_hsl = "Copy HSL"
        copy_hsv = "Copy HSV"
        copy_result = "Copy Result"
        en_link = "index.html"
        en_label = "EN"
    
    body_html = tool[f"html_body_{lang}"]
    
    # Determine copy buttons based on tool
    js_code = tool["js"]
    event_bindings_extra = ""
    
    # Per-tool event bindings
    if slug == "rgb-to-hsl":
        event_bindings_extra = """
document.getElementById('convBtn').addEventListener('click',convert);
document.getElementById('colorPicker').addEventListener('input',function(){var hex=this.value;var r=parseInt(hex.substr(1,2),16);var g=parseInt(hex.substr(3,2),16);var b=parseInt(hex.substr(5,2),16);document.getElementById('rIn').value=r;document.getElementById('gIn').value=g;document.getElementById('bIn').value=b;convert();});
['rIn','gIn','bIn'].forEach(function(id){document.getElementById(id).addEventListener('input',convert);});
document.getElementById('copyHex').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.hex).then(function(){showToast('HEX copied!')})});
document.getElementById('copyRgb').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.rgb).then(function(){showToast('RGB copied!')})});
document.getElementById('copyHsl').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.hsl).then(function(){showToast('HSL copied!')})});
convert();"""
    elif slug == "hsv-to-rgb":
        event_bindings_extra = """
document.getElementById('convBtn').addEventListener('click',convert);
['hIn','sIn','vIn'].forEach(function(id){document.getElementById(id).addEventListener('input',convert);});
document.getElementById('copyHex').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.hex).then(function(){showToast('HEX copied!')})});
document.getElementById('copyRgb').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.rgb).then(function(){showToast('RGB copied!')})});
convert();"""
    elif slug == "rgb-to-hsv":
        event_bindings_extra = """
document.getElementById('convBtn').addEventListener('click',convert);
document.getElementById('colorPicker').addEventListener('input',function(){var hex=this.value;var r=parseInt(hex.substr(1,2),16);var g=parseInt(hex.substr(3,2),16);var b=parseInt(hex.substr(5,2),16);document.getElementById('rIn').value=r;document.getElementById('gIn').value=g;document.getElementById('bIn').value=b;convert();});
['rIn','gIn','bIn'].forEach(function(id){document.getElementById(id).addEventListener('input',convert);});
document.getElementById('copyHex').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.hex).then(function(){showToast('HEX copied!')})});
document.getElementById('copyRgb').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.rgb).then(function(){showToast('RGB copied!')})});
document.getElementById('copyHsv').addEventListener('click',function(){if(window._lastColor)navigator.clipboard.writeText(window._lastColor.hsv).then(function(){showToast('HSV copied!')})});
convert();"""
    elif slug == "sql-minifier":
        event_bindings_extra = """
document.getElementById('procBtn').addEventListener('click',process);
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('sqlInput').value='';document.getElementById('sqlOutput').value='';document.getElementById('charCount').textContent='0';});
document.getElementById('copyBtn').addEventListener('click',function(){var v=document.getElementById('sqlOutput').value;if(v)navigator.clipboard.writeText(v).then(function(){showToast('Copied!')})});
process();"""
    elif slug == "percent-change":
        event_bindings_extra = """
document.getElementById('calcBtn').addEventListener('click',calcChange);
document.getElementById('revBtn').addEventListener('click',calcReverse);
['origVal','newVal'].forEach(function(id){document.getElementById(id).addEventListener('input',calcChange);});
['origVal2','pctInput'].forEach(function(id){document.getElementById(id).addEventListener('input',calcReverse);});
calcChange();calcReverse();"""
    
    # Schema.org breadcrumb
    if lang == "cn":
        bc_name1, bc_url1 = "首页", "https://free-toolbase.com/"
        bc_name2, bc_url2 = "工具", "https://free-toolbase.com/#tools"
    else:
        bc_name1, bc_url1 = "Home", "https://free-toolbase.com/en/"
        bc_name2, bc_url2 = "Tools", "https://free-toolbase.com/en/#tools"
    
    bc_name3 = t["breadcrumb"]
    bc_url3 = f"https://free-toolbase.com{t['canonical']}"
    
    page = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
{GA_SCRIPT}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['desc']}">
<meta name="keywords" content="{t['kw']}">
<title>{t['title']}</title>
<link rel="canonical" href="https://free-toolbase.com{t['canonical']}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="https://free-toolbase.com{t['canonical']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">""" + json.dumps({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": t["schema_name"],
    "description": t["desc"],
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Web",
    "publisher": {"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"},
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
}, ensure_ascii=False) + """</script>
<script type="application/ld+json">""" + json.dumps({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": bc_name1, "item": bc_url1},
        {"@type": "ListItem", "position": 2, "name": bc_name2, "item": bc_url2},
        {"@type": "ListItem", "position": 3, "name": bc_name3, "item": bc_url3}
    ]
}, ensure_ascii=False) + """</script>
<style>
""" + CSS_BLOCK + """
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>""" + t["h1"] + """</h1><div class="lang-switch"><a href=""""" + (f'"{en_link}"' if lang == "en" else f'"index.html"') + """" class=\"""" + cn_active + """\">中文</a><a href=\"""" + (f'"{en_link}"' if lang == "en" else f'"../en/{slug}/"') + """" class=\"""" + en_active + """\">EN</a></div></div>
<p class="nav-back"><a href=\"""" + home_path + """\">""" + home_label + """</a> &rsaquo; <a href=\"""" + tools_path + """\">""" + tools_label + """</a> &rsaquo; """ + t["breadcrumb"] + """</p>
<div style="text-align:center;margin-bottom:16px;font-size:0.95rem;color:#94a3b8">""" + t["hero"] + """ <span style="display:inline-block;padding:2px 12px;border-radius:12px;background:rgba(6,182,212,.1);color:#22d3ee;font-size:.8rem;margin-left:8px">零依赖·可离线使用</span></div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: 2026-07-25
  </span>
</div>
""" + body_html + """
<div class="info-section" id="usage">
  <h2>""" + t["usage_title"] + """</h2>
  <div id="usageContent">""" + t["usage"] + """</div>
</div>
</div>
<div class="footer container">
<div style="margin-bottom:12px">
<a href=\"""" + home_path + """\">""" + home_label + """</a>
<a href=\"""" + tools_path + """\">""" + all_tools_label + """</a>
<a href="mailto:dexshuang@google.com">""" + contact_label + """</a>
<a href="../privacy/">""" + privacy_label + """</a>
<a href="../terms/">""" + terms_label + """</a>
<a href="../about/">""" + about_label + """</a>
<a href=\"""" + en_path + """\">EN</a>
</div>
<p>""" + t["footer"] + """</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
""" + COMMON_JS + """
""" + js_code + """
(function(){
""" + event_bindings_extra + """
})();
</script>
</body>
</html>"""
    return page


# Generate all files
for tool in TOOLS:
    slug = tool["slug"]
    
    os.makedirs(os.path.join(BASE_DIR, slug), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "en", slug), exist_ok=True)
    
    cn_page = generate_page(tool, "cn")
    en_page = generate_page(tool, "en")
    
    with open(os.path.join(BASE_DIR, slug, "index.html"), "w", encoding="utf-8") as f:
        f.write(cn_page)
    
    with open(os.path.join(BASE_DIR, "en", slug, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_page)
    
    print(f"✅ Generated {slug} (CN + EN)")

print(f"\nDone! Generated {len(TOOLS)} tools × 2 languages = {len(TOOLS)*2} pages")
