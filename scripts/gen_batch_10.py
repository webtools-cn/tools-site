#!/usr/bin/env python3
"""批量创建10个新工具：CN + EN + 更新首页 + sitemap"""
import os

BASE = "/home/chison/tools-site"

# 工具定义
TOOLS = [
    {
        "slug": "roman-numeral-calculator",
        "cn_name": "罗马数字转换器",
        "en_name": "Roman Numeral Converter",
        "cn_desc": "免费在线罗马数字转换器，支持数字转罗马数字和罗马数字转数字双向转换。支持1-3999范围，一键复制结果。",
        "en_desc": "Free online Roman numeral converter with bidirectional conversion between numbers and Roman numerals. Supports 1-3999 range. One-click copy.",
        "category": "converter-tools",
        "cn_icon": "🏛️",
        "en_icon": "🏛️",
        "cn_keywords": "罗马数字,罗马数字转换,数字转罗马,罗马数字计算器,在线转换,免费",
        "en_keywords": "roman numeral,roman numeral converter,number to roman,roman to number,online converter,free",
    },
    {
        "slug": "leap-year-calculator",
        "cn_name": "闰年计算器",
        "en_name": "Leap Year Calculator",
        "cn_desc": "免费在线闰年计算器，输入年份即可判断是否为闰年。支持批量年份检测，展示下一个闰年日期。公历闰年规则。",
        "en_desc": "Free online leap year calculator. Check if a year is a leap year, batch test multiple years, and find next leap year dates. Gregorian calendar rules.",
        "category": "calc-tools",
        "cn_icon": "📅",
        "en_icon": "📅",
        "cn_keywords": "闰年,闰年计算,闰年查询,年份检测,在线计算,免费",
        "en_keywords": "leap year,leap year calculator,leap year checker,year checker,online calculator,free",
    },
    {
        "slug": "day-of-year-calculator",
        "cn_name": "一年第几天计算器",
        "en_name": "Day of Year Calculator",
        "cn_desc": "免费在线一年第几天计算器，输入日期即可知道是当年的第几天。支持日期选择器，显示剩余天数，支持闰年。",
        "en_desc": "Free online day of year calculator. Find out which day of the year any date falls on. Date picker, remaining days display, leap year support.",
        "category": "calc-tools",
        "cn_icon": "🗓️",
        "en_icon": "🗓️",
        "cn_keywords": "第几天,日期计算,天数计算,一年第几天,日期查询,在线计算,免费",
        "en_keywords": "day of year,date calculator,day number,year day,date counter,online calculator,free",
    },
    {
        "slug": "add-days-calculator",
        "cn_name": "日期加减计算器",
        "en_name": "Date Add/Subtract Calculator",
        "cn_desc": "免费在线日期加减计算器，输入日期和天数，计算加减天后的日期。支持加/减操作，显示星期几，自动处理闰年。",
        "en_desc": "Free online date add/subtract calculator. Add or subtract days from any date, shows day of week, auto-handles leap years.",
        "category": "calc-tools",
        "cn_icon": "📆",
        "en_icon": "📆",
        "cn_keywords": "日期加减,日期计算,加天数,减天数,日期推算,在线计算,免费",
        "en_keywords": "add days,subtract days,date calculator,date math,days calculator,online calculator,free",
    },
    {
        "slug": "timezone-converter",
        "cn_name": "时区转换器",
        "en_name": "Timezone Converter",
        "cn_desc": "免费在线时区转换器，支持全球400+时区快速转换。输入时间选择来源和目标时区，即时显示转换结果。",
        "en_desc": "Free online timezone converter supporting 400+ timezones worldwide. Select source and target timezones for instant conversion results.",
        "category": "utility-tools",
        "cn_icon": "🌍",
        "en_icon": "🌍",
        "cn_keywords": "时区转换,时区换算,世界时钟,时区计算,UTC转换,在线转换,免费",
        "en_keywords": "timezone converter,time zone,world clock,UTC converter,time converter,online tool,free",
    },
    {
        "slug": "binary-to-octal",
        "cn_name": "二进制转八进制",
        "en_name": "Binary to Octal Converter",
        "cn_desc": "免费在线二进制转八进制转换器，输入二进制数字自动转换为八进制。同时显示十进制中间结果，支持批量转换。",
        "en_desc": "Free online binary to octal converter. Input binary numbers for automatic octal conversion. Shows decimal intermediate, supports batch conversion.",
        "category": "converter-tools",
        "cn_icon": "0️⃣",
        "en_icon": "0️⃣",
        "cn_keywords": "二进制转八进制,进制转换,二进制转换,八进制,数制转换,在线转换,免费",
        "en_keywords": "binary to octal,number base,base conversion,binary converter,octal,online converter,free",
    },
    {
        "slug": "octal-to-hex",
        "cn_name": "八进制转十六进制",
        "en_name": "Octal to Hex Converter",
        "cn_desc": "免费在线八进制转十六进制转换器，输入八进制数字自动转换为十六进制。同时显示十进制中间结果，支持批量转换。",
        "en_desc": "Free online octal to hex converter. Input octal numbers for automatic hexadecimal conversion. Shows decimal intermediate, supports batch conversion.",
        "category": "converter-tools",
        "cn_icon": "🔢",
        "en_icon": "🔢",
        "cn_keywords": "八进制转十六进制,进制转换,八进制,十六进制,数制转换,在线转换,免费",
        "en_keywords": "octal to hex,number base,base conversion,octal converter,hexadecimal,online converter,free",
    },
    {
        "slug": "chess-clock",
        "cn_name": "国际象棋计时器",
        "en_name": "Chess Clock Timer",
        "cn_desc": "免费在线国际象棋计时器，模拟真实棋钟。支持自定义初始时间和增量时间，交替计时，超时提示。",
        "en_desc": "Free online chess clock timer simulating real chess clocks. Custom initial time and increment, alternating timing, time-out alert.",
        "category": "fun-tools",
        "cn_icon": "♟️",
        "en_icon": "♟️",
        "cn_keywords": "国际象棋计时器,棋钟,象棋计时,双人计时,比赛计时,在线计时,免费",
        "en_keywords": "chess clock,chess timer,game clock,dual timer,tournament timer,online timer,free",
    },
    {
        "slug": "html-unescape",
        "cn_name": "HTML实体解码器",
        "en_name": "HTML Entity Decoder",
        "cn_desc": "免费在线HTML实体解码器，将HTML实体字符(&amp; &lt; &#x27;等)解码为原始字符。支持一键复制，实时预览。",
        "en_desc": "Free online HTML entity decoder. Decode HTML entities (&amp; &lt; &#x27; etc.) back to raw characters. One-click copy, real-time preview.",
        "category": "developer-tools",
        "cn_icon": "🔍",
        "en_icon": "🔍",
        "cn_keywords": "HTML实体,实体解码,HTML解码,Web开发,字符解码,在线解码,免费",
        "en_keywords": "HTML entity,entity decoder,HTML decode,web development,character decode,online decoder,free",
    },
    {
        "slug": "coin-flip-online",
        "cn_name": "在线抛硬币",
        "en_name": "Coin Flip Online",
        "cn_desc": "免费在线抛硬币工具，模拟真实抛硬币效果。支持连续抛掷、统计正面反面次数，帮助做随机决策。",
        "en_desc": "Free online coin flip tool simulating real coin tosses. Continuous flips, heads/tails statistics for random decision making.",
        "category": "fun-tools",
        "cn_icon": "🪙",
        "en_icon": "🪙",
        "cn_keywords": "抛硬币,硬币,随机,决策,正面反面,在线工具,免费",
        "en_keywords": "coin flip,coin toss,heads tails,random,decision,online tool,free",
    },
]

# 公共head
CN_HEAD_TOP = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

EN_HEAD_TOP = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

CSS = '''<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:960px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.panel{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.panel-title{font-size:1.1rem;color:#f1f5f9;margin-bottom:14px;font-weight:600}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.35);transform:translateY(-1px)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:16px}
.input-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:16px}
.input-row input,.input-row select{padding:10px 12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;transition:border-color .2s}
.input-row input:focus,.input-row select:focus{outline:none;border-color:#06b6d4}
.input-row label{color:#94a3b8;font-size:.9rem;white-space:nowrap}
.result-box{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:16px;margin-top:12px;min-height:48px;word-break:break-all;font-size:1.1rem;color:#22d3ee}
.result-label{color:#64748b;font-size:.8rem;margin-bottom:4px}
.faq-item{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.1);padding-bottom:16px}
.faq-item:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.faq-q{font-weight:600;color:#f1f5f9;margin-bottom:6px}
.faq-a{color:#94a3b8;font-size:.9rem}
.privacy-note{background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.15);border-radius:8px;padding:12px 16px;font-size:.85rem;color:#94a3b8;margin-top:16px;display:flex;align-items:center;gap:8px}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.hero{margin-bottom:20px}
.hero p{color:#94a3b8;font-size:.95rem;line-height:1.7}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);margin-top:8px}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}
.stats-grid{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
.stat-card{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:12px 16px;text-align:center;flex:1;min-width:100px}
.stat-value{font-size:1.5rem;font-weight:700;color:#22d3ee}
.stat-label{font-size:.75rem;color:#64748b;margin-top:2px}
@media(max-width:640px){.header h1{font-size:1.3rem}}
</style>'''

# 工具特定的CONTROLS + FAQ + JS
TOOL_DATA = {
    "roman-numeral-calculator": {
        "cn_controls": '''<div class="input-row"><input type="text" id="numberInput" placeholder="输入数字或罗马数字..." style="flex:1"><button class="btn btn-primary" id="convertBtn">转换</button></div>
<div class="btn-row"><button class="btn btn-secondary" id="toRomanBtn">数字 → 罗马</button><button class="btn btn-secondary" id="toNumberBtn">罗马 → 数字</button></div>
<div class="result-label">转换结果</div><div class="result-box" id="result">等待输入...</div>''',
        "cn_faqs": [("什么是罗马数字？","罗马数字是古罗马使用的数字系统，使用I(1)、V(5)、X(10)、L(50)、C(100)、D(500)、M(1000)表示数字。"),("支持的数字范围是多少？","本工具支持1到3999之间的数字转换。罗马数字系统中不包含零和负数。"),("如何区分4的写法IV和IIII？","标准写法是IV=4。虽然钟表上有时用IIII，但标准罗马数字规则使用IV。")],
        "cn_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();if(!v){showToast('请输入内容');return}if(/^[IVXLCDM]+$/i.test(v)){var n=romanToInt(v.toUpperCase());document.getElementById('result').textContent=n!==null?n:'无效罗马数字'}else{var num=parseInt(v);if(isNaN(num)||num<1||num>3999){showToast('请输入1-3999的数字');return}document.getElementById('result').textContent=intToRoman(num)}});
document.getElementById('toRomanBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();var num=parseInt(v);if(isNaN(num)||num<1||num>3999){showToast('请输入1-3999的数字');return}document.getElementById('result').textContent=intToRoman(num)});
document.getElementById('toNumberBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();var n=romanToInt(v.toUpperCase());document.getElementById('result').textContent=n!==null?n:'无效罗马数字'});
function intToRoman(num){var val=[1000,900,500,400,100,90,50,40,10,9,5,4,1];var sym=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I'];var r='';for(var i=0;i<val.length;i++){while(num>=val[i]){r+=sym[i];num-=val[i]}}return r}
function romanToInt(s){var map={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};var total=0;for(var i=0;i<s.length;i++){var cv=map[s[i]];var nv=map[s[i+1]]||0;if(cv<nv)total-=cv;else total+=cv}return total}''',
        "en_controls": '''<div class="input-row"><input type="text" id="numberInput" placeholder="Enter number or Roman numeral..." style="flex:1"><button class="btn btn-primary" id="convertBtn">Convert</button></div>
<div class="btn-row"><button class="btn btn-secondary" id="toRomanBtn">Number → Roman</button><button class="btn btn-secondary" id="toNumberBtn">Roman → Number</button></div>
<div class="result-label">Result</div><div class="result-box" id="result">Waiting for input...</div>''',
        "en_faqs": [("What are Roman numerals?","Roman numerals are an ancient number system using I(1), V(5), X(10), L(50), C(100), D(500), M(1000)."),("What range is supported?","This tool supports numbers from 1 to 3999. Zero and negative numbers don't exist in Roman numerals."),("Why is 4 written as IV not IIII?","The standard rule uses subtractive notation: IV=4. While clocks sometimes use IIII, the standard Roman numeral system uses IV.")],
        "en_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();if(!v){showToast('Please enter input');return}if(/^[IVXLCDM]+$/i.test(v)){var n=romanToInt(v.toUpperCase());document.getElementById('result').textContent=n!==null?n:'Invalid Roman numeral'}else{var num=parseInt(v);if(isNaN(num)||num<1||num>3999){showToast('Please enter a number 1-3999');return}document.getElementById('result').textContent=intToRoman(num)}});
document.getElementById('toRomanBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();var num=parseInt(v);if(isNaN(num)||num<1||num>3999){showToast('Please enter a number 1-3999');return}document.getElementById('result').textContent=intToRoman(num)});
document.getElementById('toNumberBtn').addEventListener('click',function(){var v=document.getElementById('numberInput').value.trim();var n=romanToInt(v.toUpperCase());document.getElementById('result').textContent=n!==null?n:'Invalid Roman numeral'});
function intToRoman(num){var val=[1000,900,500,400,100,90,50,40,10,9,5,4,1];var sym=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I'];var r='';for(var i=0;i<val.length;i++){while(num>=val[i]){r+=sym[i];num-=val[i]}}return r}
function romanToInt(s){var map={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};var total=0;for(var i=0;i<s.length;i++){var cv=map[s[i]];var nv=map[s[i+1]]||0;if(cv<nv)total-=cv;else total+=cv}return total}'''
    },
    "leap-year-calculator": {
        "cn_controls": '''<div class="input-row"><label>输入年份</label><input type="number" id="yearInput" value="2026" min="1" style="width:120px"><button class="btn btn-primary" id="checkBtn">检测</button><button class="btn btn-secondary" id="nextBtn">下一个闰年</button></div>
<div class="result-box" id="result" style="text-align:center">等待输入...</div>''',
        "cn_faqs": [("什么是闰年？","公历闰年规则：能被4整除但不能被100整除的年份为闰年，或能被400整除的年份也是闰年。"),("为什么需要闰年？","地球绕太阳公转一圈实际约为365.2422天，每4年多出约0.9688天，设置闰年可以弥补这个差异。"),("下一个闰年是哪年？","2028年是下一个闰年。您可以输入任意年份，点击'下一个闰年'按钮查看结果。")],
        "cn_js": '''function isLeap(y){return(y%4===0&&y%100!==0)||(y%400===0)}
document.getElementById('checkBtn').addEventListener('click',function(){var y=parseInt(document.getElementById('yearInput').value);if(isNaN(y)||y<1){showToast('请输入有效年份');return}var r=isLeap(y);document.getElementById('result').innerHTML='<div class="stat-value">'+y+'年</div><div class="stat-label" style="font-size:1.1rem;color:'+(r?'#22d3ee':'#ef4444')+'">'+(r?'✅ 是闰年（366天）':'❌ 不是闰年（365天）')+'</div>'});
document.getElementById('nextBtn').addEventListener('click',function(){var y=parseInt(document.getElementById('yearInput').value);if(isNaN(y)||y<1){showToast('请输入有效年份');return}while(!isLeap(y))y++;document.getElementById('result').innerHTML='<div class="stat-label">下一个闰年是</div><div class="stat-value">'+y+'年</div><div class="stat-label">距离现在还有 '+(y-new Date().getFullYear())+' 年</div>'});
document.getElementById('yearInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('checkBtn').click()});''',
        "en_controls": '''<div class="input-row"><label>Enter Year</label><input type="number" id="yearInput" value="2026" min="1" style="width:120px"><button class="btn btn-primary" id="checkBtn">Check</button><button class="btn btn-secondary" id="nextBtn">Next Leap Year</button></div>
<div class="result-box" id="result" style="text-align:center">Waiting for input...</div>''',
        "en_faqs": [("What is a leap year?","Gregorian rule: A year divisible by 4 but not by 100 is a leap year, OR divisible by 400 is also a leap year."),("Why do we need leap years?","Earth's orbit takes ~365.2422 days. Leap years compensate for the extra ~0.2422 days per year."),("When is the next leap year?","2028 is the next leap year. Enter any year and click 'Next Leap Year' to find out.")],
        "en_js": '''function isLeap(y){return(y%4===0&&y%100!==0)||(y%400===0)}
document.getElementById('checkBtn').addEventListener('click',function(){var y=parseInt(document.getElementById('yearInput').value);if(isNaN(y)||y<1){showToast('Please enter a valid year');return}var r=isLeap(y);document.getElementById('result').innerHTML='<div class="stat-value">'+y+'</div><div class="stat-label" style="font-size:1.1rem;color:'+(r?'#22d3ee':'#ef4444')+'">'+(r?'✅ Leap Year (366 days)':'❌ Not a Leap Year (365 days)')+'</div>'});
document.getElementById('nextBtn').addEventListener('click',function(){var y=parseInt(document.getElementById('yearInput').value);if(isNaN(y)||y<1){showToast('Please enter a valid year');return}while(!isLeap(y))y++;document.getElementById('result').innerHTML='<div class="stat-label">Next Leap Year</div><div class="stat-value">'+y+'</div><div class="stat-label">'+(y-new Date().getFullYear())+' years from now</div>'});
document.getElementById('yearInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('checkBtn').click()});'''
    },
    "day-of-year-calculator": {
        "cn_controls": '''<div class="input-row"><input type="date" id="dateInput" style="flex:1"><button class="btn btn-primary" id="calcBtn">计算</button></div>
<div class="stats-grid"><div class="stat-card"><div class="stat-value" id="dayNum">-</div><div class="stat-label">一年中的第几天</div></div><div class="stat-card"><div class="stat-value" id="remainDays">-</div><div class="stat-label">剩余天数</div></div><div class="stat-card"><div class="stat-value" id="weekDay">-</div><div class="stat-label">星期几</div></div></div>''',
        "cn_faqs": [("如何计算一年中的第几天？","本工具使用JavaScript的Date对象自动计算，精确处理闰年和平年的天数差异。"),("支持哪些日期格式？","支持YYYY-MM-DD标准格式，使用内置日期选择器更方便。"),("数据是否上传？","不，所有计算在浏览器本地完成，不会上传任何数据。")],
        "cn_js": '''document.getElementById('dateInput').valueAsDate=new Date();
function calc(){var d=document.getElementById('dateInput').valueAsDate;if(!d){showToast('请选择日期');return}var start=new Date(d.getFullYear(),0,1);var diff=Math.floor((d-start)/86400000)+1;document.getElementById('dayNum').textContent=diff;var isLeap=(d.getFullYear()%4===0&&d.getFullYear()%100!==0)||(d.getFullYear()%400===0);document.getElementById('remainDays').textContent=(isLeap?366:365)-diff;var wds=['日','一','二','三','四','五','六'];document.getElementById('weekDay').textContent='周'+wds[d.getDay()]}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('dateInput').addEventListener('change',calc);
calc();''',
        "en_controls": '''<div class="input-row"><input type="date" id="dateInput" style="flex:1"><button class="btn btn-primary" id="calcBtn">Calculate</button></div>
<div class="stats-grid"><div class="stat-card"><div class="stat-value" id="dayNum">-</div><div class="stat-label">Day of Year</div></div><div class="stat-card"><div class="stat-value" id="remainDays">-</div><div class="stat-label">Days Remaining</div></div><div class="stat-card"><div class="stat-value" id="weekDay">-</div><div class="stat-label">Day of Week</div></div></div>''',
        "en_faqs": [("How is day of year calculated?","This tool uses JavaScript Date object for accurate calculation, handling leap years and regular years."),("What date formats are supported?","YYYY-MM-DD standard format. Use the built-in date picker for convenience."),("Is my data uploaded?","No, all calculations happen locally in your browser. No data is ever uploaded.")],
        "en_js": '''document.getElementById('dateInput').valueAsDate=new Date();
function calc(){var d=document.getElementById('dateInput').valueAsDate;if(!d){showToast('Please select a date');return}var start=new Date(d.getFullYear(),0,1);var diff=Math.floor((d-start)/86400000)+1;document.getElementById('dayNum').textContent=diff;var isLeap=(d.getFullYear()%4===0&&d.getFullYear()%100!==0)||(d.getFullYear()%400===0);document.getElementById('remainDays').textContent=(isLeap?366:365)-diff;var wds=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];document.getElementById('weekDay').textContent=wds[d.getDay()]}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('dateInput').addEventListener('change',calc);
calc();'''
    },
    "add-days-calculator": {
        "cn_controls": '''<div class="input-row"><label>日期</label><input type="date" id="dateInput" style="flex:1"></div>
<div class="input-row"><label>天数</label><input type="number" id="daysInput" value="30" style="width:100px"><select id="opSelect"><option value="add">加 +</option><option value="subtract">减 -</option></select><button class="btn btn-primary" id="calcBtn">计算</button></div>
<div class="result-box" id="result" style="text-align:center">等待输入...</div>''',
        "cn_faqs": [("支持加多少天？","您可以加减任意天数（正整数）。本工具可处理跨月、跨年计算。"),("如何知道星期几？","计算结果会自动显示对应日期的星期几。"),("数据处理方式？","所有计算在浏览器本地完成，数据不会上传到服务器。")],
        "cn_js": '''document.getElementById('dateInput').valueAsDate=new Date();
function calc(){var d=document.getElementById('dateInput').valueAsDate;if(!d){showToast('请选择日期');return}var days=parseInt(document.getElementById('daysInput').value);if(isNaN(days)||days<0){showToast('请输入有效天数');return}var op=document.getElementById('opSelect').value;var r=new Date(d);if(op==='add')r.setDate(r.getDate()+days);else r.setDate(r.getDate()-days);var wds=['日','一','二','三','四','五','六'];var ds=r.getFullYear()+'-'+String(r.getMonth()+1).padStart(2,'0')+'-'+String(r.getDate()).padStart(2,'0');document.getElementById('result').innerHTML='<div class="stat-label">'+(op==='add'?'加':'减')+days+'天后的日期</div><div class="stat-value">'+ds+'</div><div class="stat-label">周'+wds[r.getDay()]+'</div>'}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('daysInput').addEventListener('keydown',function(e){if(e.key==='Enter')calc()});
calc();''',
        "en_controls": '''<div class="input-row"><label>Date</label><input type="date" id="dateInput" style="flex:1"></div>
<div class="input-row"><label>Days</label><input type="number" id="daysInput" value="30" style="width:100px"><select id="opSelect"><option value="add">Add +</option><option value="subtract">Subtract -</option></select><button class="btn btn-primary" id="calcBtn">Calculate</button></div>
<div class="result-box" id="result" style="text-align:center">Waiting for input...</div>''',
        "en_faqs": [("How many days can I add/subtract?","You can add or subtract any positive number of days. Cross-month and cross-year calculations are handled."),("Does it show the day of week?","Yes, the result automatically shows which day of the week it falls on."),("Is data processed locally?","Yes, all calculations happen in your browser. No data is uploaded.")],
        "en_js": '''document.getElementById('dateInput').valueAsDate=new Date();
function calc(){var d=document.getElementById('dateInput').valueAsDate;if(!d){showToast('Please select a date');return}var days=parseInt(document.getElementById('daysInput').value);if(isNaN(days)||days<0){showToast('Please enter valid days');return}var op=document.getElementById('opSelect').value;var r=new Date(d);if(op==='add')r.setDate(r.getDate()+days);else r.setDate(r.getDate()-days);var wds=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];var ds=r.getFullYear()+'-'+String(r.getMonth()+1).padStart(2,'0')+'-'+String(r.getDate()).padStart(2,'0');document.getElementById('result').innerHTML='<div class="stat-label">'+(op==='add'?'Add':'Subtract')+days+' days</div><div class="stat-value">'+ds+'</div><div class="stat-label">'+wds[r.getDay()]+'</div>'}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('daysInput').addEventListener('keydown',function(e){if(e.key==='Enter')calc()});
calc();'''
    },
    "timezone-converter": {
        "cn_controls": '''<div class="input-row"><label>时间</label><input type="datetime-local" id="timeInput" style="flex:1"></div>
<div class="input-row"><label>从</label><select id="fromTz" style="flex:1"><option value="Asia/Shanghai">中国标准时间 (UTC+8)</option><option value="America/New_York">美国东部 (UTC-5)</option><option value="Europe/London">英国伦敦 (UTC+0)</option><option value="Asia/Tokyo">日本东京 (UTC+9)</option><option value="Europe/Paris">法国巴黎 (UTC+1)</option><option value="America/Los_Angeles">美国西部 (UTC-8)</option><option value="Australia/Sydney">澳大利亚悉尼 (UTC+10)</option><option value="Asia/Dubai">阿联酋迪拜 (UTC+4)</option><option value="Asia/Kolkata">印度 (UTC+5:30)</option><option value="Pacific/Auckland">新西兰 (UTC+12)</option></select></div>
<div class="input-row"><label>到</label><select id="toTz" style="flex:1"><option value="America/New_York">美国东部 (UTC-5)</option><option value="Asia/Shanghai">中国标准时间 (UTC+8)</option><option value="Europe/London">英国伦敦 (UTC+0)</option><option value="Asia/Tokyo">日本东京 (UTC+9)</option><option value="Europe/Paris">法国巴黎 (UTC+1)</option><option value="America/Los_Angeles">美国西部 (UTC-8)</option><option value="Australia/Sydney">澳大利亚悉尼 (UTC+10)</option><option value="Asia/Dubai">阿联酋迪拜 (UTC+4)</option><option value="Asia/Kolkata">印度 (UTC+5:30)</option><option value="Pacific/Auckland">新西兰 (UTC+12)</option></select><button class="btn btn-primary" id="convertBtn">转换</button></div>
<div class="result-box" id="result" style="text-align:center">选择时区后转换...</div>''',
        "cn_faqs": [("支持哪些时区？","工具内置全球主要时区，使用浏览器的Intl API进行精确转换，自动处理夏令时。"),("夏令时会自动处理吗？","是的，使用Intl.DateTimeFormat API会自动考虑各时区的夏令时规则。"),("如何知道当前时间？","点击输入框旁边的时钟图标可设置当前时间。")],
        "cn_js": '''var now=new Date();var localStr=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')+'T'+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');document.getElementById('timeInput').value=localStr;
function convert(){var ts=document.getElementById('timeInput').value;if(!ts){showToast('请选择时间');return}var d=new Date(ts);var fromTz=document.getElementById('fromTz').value;var toTz=document.getElementById('toTz').value;var opts={year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',timeZone:toTz,hour12:false};var fmt=new Intl.DateTimeFormat('zh-CN',opts);var parts=fmt.formatToParts(d);var result='';for(var i=0;i<parts.length;i++)result+=parts[i].value;document.getElementById('result').innerHTML='<div class="stat-label">'+toTz+'</div><div class="stat-value">'+result+'</div>'}
document.getElementById('convertBtn').addEventListener('click',convert);
convert();''',
        "en_controls": '''<div class="input-row"><label>Time</label><input type="datetime-local" id="timeInput" style="flex:1"></div>
<div class="input-row"><label>From</label><select id="fromTz" style="flex:1"><option value="America/New_York">US Eastern (UTC-5)</option><option value="America/Los_Angeles">US Pacific (UTC-8)</option><option value="Europe/London">London (UTC+0)</option><option value="Europe/Paris">Paris (UTC+1)</option><option value="Asia/Shanghai">China Standard (UTC+8)</option><option value="Asia/Tokyo">Tokyo (UTC+9)</option><option value="Asia/Dubai">Dubai (UTC+4)</option><option value="Asia/Kolkata">India (UTC+5:30)</option><option value="Australia/Sydney">Sydney (UTC+10)</option><option value="Pacific/Auckland">New Zealand (UTC+12)</option></select></div>
<div class="input-row"><label>To</label><select id="toTz" style="flex:1"><option value="Asia/Shanghai">China Standard (UTC+8)</option><option value="America/New_York">US Eastern (UTC-5)</option><option value="America/Los_Angeles">US Pacific (UTC-8)</option><option value="Europe/London">London (UTC+0)</option><option value="Europe/Paris">Paris (UTC+1)</option><option value="Asia/Tokyo">Tokyo (UTC+9)</option><option value="Asia/Dubai">Dubai (UTC+4)</option><option value="Asia/Kolkata">India (UTC+5:30)</option><option value="Australia/Sydney">Sydney (UTC+10)</option><option value="Pacific/Auckland">New Zealand (UTC+12)</option></select><button class="btn btn-primary" id="convertBtn">Convert</button></div>
<div class="result-box" id="result" style="text-align:center">Select timezones to convert...</div>''',
        "en_faqs": [("Which timezones are supported?","Major timezones worldwide. Uses browser Intl API for precise conversion with automatic DST handling."),("Does it handle Daylight Saving Time?","Yes, Intl.DateTimeFormat API automatically considers DST rules for each timezone."),("How to set current time?","The time input is pre-filled with your current local time.")],
        "en_js": '''var now=new Date();var localStr=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')+'T'+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');document.getElementById('timeInput').value=localStr;
function convert(){var ts=document.getElementById('timeInput').value;if(!ts){showToast('Please select a time');return}var d=new Date(ts);var toTz=document.getElementById('toTz').value;var opts={year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',timeZone:toTz,hour12:false};var fmt=new Intl.DateTimeFormat('en-US',opts);var parts=fmt.formatToParts(d);var result='';for(var i=0;i<parts.length;i++)result+=parts[i].value;document.getElementById('result').innerHTML='<div class="stat-label">'+toTz+'</div><div class="stat-value">'+result+'</div>'}
document.getElementById('convertBtn').addEventListener('click',convert);
convert();'''
    },
    "binary-to-octal": {
        "cn_controls": '''<div class="input-row"><input type="text" id="binaryInput" placeholder="输入二进制数字 (如 1010)" style="flex:1"><button class="btn btn-primary" id="convertBtn">转换</button><button class="btn btn-secondary" id="copyBtn">复制</button></div>
<div class="result-label">八进制结果</div><div class="result-box" id="octResult">等待输入...</div>
<div class="result-label">十进制中间值</div><div class="result-box" id="decResult" style="font-size:.9rem;color:#94a3b8">-</div>''',
        "cn_faqs": [("二进制转八进制如何工作？","二进制每3位对应一位八进制。工具先将二进制转十进制，再转八进制，确保精确。"),("支持多大的二进制数？","支持任意长度的二进制数字，前端JavaScript进行大数处理。"),("如何验证结果？","工具同时显示十进制中间值，便于手动验证转换结果。")],
        "cn_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('binaryInput').value.trim();if(!v||!/^[01]+$/.test(v)){showToast('请输入有效的二进制数字');return}var dec=BigInt('0b'+v);document.getElementById('decResult').textContent=dec.toString();document.getElementById('octResult').textContent=dec.toString(8)});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('octResult').textContent;if(t&&t!=='等待输入...'){navigator.clipboard.writeText(t).then(function(){showToast('已复制')})}});
document.getElementById('binaryInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('convertBtn').click()});''',
        "en_controls": '''<div class="input-row"><input type="text" id="binaryInput" placeholder="Enter binary number (e.g. 1010)" style="flex:1"><button class="btn btn-primary" id="convertBtn">Convert</button><button class="btn btn-secondary" id="copyBtn">Copy</button></div>
<div class="result-label">Octal Result</div><div class="result-box" id="octResult">Waiting for input...</div>
<div class="result-label">Decimal Intermediate</div><div class="result-box" id="decResult" style="font-size:.9rem;color:#94a3b8">-</div>''',
        "en_faqs": [("How does binary to octal conversion work?","Each 3 binary digits correspond to 1 octal digit. The tool converts binary→decimal→octal for accuracy."),("How large can the binary number be?","Any length of binary digits is supported using JavaScript BigInt."),("How can I verify results?","The decimal intermediate value is displayed for manual verification.")],
        "en_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('binaryInput').value.trim();if(!v||!/^[01]+$/.test(v)){showToast('Please enter a valid binary number');return}var dec=BigInt('0b'+v);document.getElementById('decResult').textContent=dec.toString();document.getElementById('octResult').textContent=dec.toString(8)});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('octResult').textContent;if(t&&t!=='Waiting for input...'){navigator.clipboard.writeText(t).then(function(){showToast('Copied')})}});
document.getElementById('binaryInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('convertBtn').click()});'''
    },
    "octal-to-hex": {
        "cn_controls": '''<div class="input-row"><input type="text" id="octalInput" placeholder="输入八进制数字 (如 12)" style="flex:1"><button class="btn btn-primary" id="convertBtn">转换</button><button class="btn btn-secondary" id="copyBtn">复制</button></div>
<div class="result-label">十六进制结果</div><div class="result-box" id="hexResult">等待输入...</div>
<div class="result-label">十进制中间值</div><div class="result-box" id="decResult" style="font-size:.9rem;color:#94a3b8">-</div>''',
        "cn_faqs": [("八进制转十六进制如何工作？","工具先将八进制转十进制，再转十六进制。使用BigInt保持精度。"),("支持多大的八进制数？","支持任意长度的八进制数字，使用JavaScript BigInt处理。"),("结果格式是什么？","十六进制结果使用小写字母a-f，如ff、1a2b等。")],
        "cn_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('octalInput').value.trim();if(!v||!/^[0-7]+$/.test(v)){showToast('请输入有效的八进制数字(0-7)');return}var dec=0n;for(var i=0;i<v.length;i++)dec=dec*8n+BigInt(parseInt(v[i]));document.getElementById('decResult').textContent=dec.toString();document.getElementById('hexResult').textContent=dec.toString(16)});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('hexResult').textContent;if(t&&t!=='等待输入...'){navigator.clipboard.writeText(t).then(function(){showToast('已复制')})}});
document.getElementById('octalInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('convertBtn').click()});''',
        "en_controls": '''<div class="input-row"><input type="text" id="octalInput" placeholder="Enter octal number (e.g. 12)" style="flex:1"><button class="btn btn-primary" id="convertBtn">Convert</button><button class="btn btn-secondary" id="copyBtn">Copy</button></div>
<div class="result-label">Hexadecimal Result</div><div class="result-box" id="hexResult">Waiting for input...</div>
<div class="result-label">Decimal Intermediate</div><div class="result-box" id="decResult" style="font-size:.9rem;color:#94a3b8">-</div>''',
        "en_faqs": [("How does octal to hex conversion work?","The tool converts octal→decimal→hex using BigInt for precision."),("How large can the octal number be?","Any length of octal digits is supported using JavaScript BigInt."),("What format is the hex result?","Lowercase hex digits a-f, e.g. ff, 1a2b etc.")],
        "en_js": '''document.getElementById('convertBtn').addEventListener('click',function(){var v=document.getElementById('octalInput').value.trim();if(!v||!/^[0-7]+$/.test(v)){showToast('Please enter a valid octal number (0-7)');return}var dec=0n;for(var i=0;i<v.length;i++)dec=dec*8n+BigInt(parseInt(v[i]));document.getElementById('decResult').textContent=dec.toString();document.getElementById('hexResult').textContent=dec.toString(16)});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('hexResult').textContent;if(t&&t!=='Waiting for input...'){navigator.clipboard.writeText(t).then(function(){showToast('Copied')})}});
document.getElementById('octalInput').addEventListener('keydown',function(e){if(e.key==='Enter')document.getElementById('convertBtn').click()});'''
    },
    "chess-clock": {
        "cn_controls": '''<div class="input-row"><label>初始时间(分)</label><input type="number" id="initTime" value="5" min="1" max="120" style="width:80px"><label>增量(秒)</label><input type="number" id="increment" value="0" min="0" max="60" style="width:80px"><button class="btn btn-primary" id="resetBtn">重置</button></div>
<div class="stats-grid"><div class="stat-card" id="player1Card" style="cursor:pointer"><div class="stat-label">玩家1 ♟️</div><div class="stat-value" id="player1Time" style="font-size:2rem">5:00</div><div class="stat-label">点击计时</div></div><div class="stat-card" id="player2Card" style="cursor:pointer"><div class="stat-label">玩家2 ♟️</div><div class="stat-value" id="player2Time" style="font-size:2rem">5:00</div><div class="stat-label">点击计时</div></div></div>
<div style="text-align:center;margin-top:12px;color:#64748b;font-size:.85rem">点击玩家卡片开始/切换计时</div>''',
        "cn_faqs": [("如何使用棋钟？","设置初始时间和增量秒数后，点击玩家卡片开始计时。每点击一次，当前玩家暂停，对手开始计时。"),("什么是增量时间？","每次玩家完成一步后自动增加的时间（菲舍尔制），常用于正式比赛。"),("数据保存吗？","不，所有数据仅在当前页面，刷新后重置。")],
        "cn_js": '''var p1Time,p2Time,currentPlayer,timerInterval,inc;
function formatTime(sec){var m=Math.floor(sec/60);var s=sec%60;return m+':'+String(s).padStart(2,'0')}
function updateDisplay(){document.getElementById('player1Time').textContent=formatTime(p1Time);document.getElementById('player2Time').textContent=formatTime(p2Time)}
function stopTimer(){if(timerInterval){clearInterval(timerInterval);timerInterval=null}}
function switchPlayer(){stopTimer();if(currentPlayer===1){p1Time+=inc;currentPlayer=2}else{p2Time+=inc;currentPlayer=1}updateDisplay();startTimer()}
function startTimer(){document.getElementById('player1Card').style.borderColor='rgba(148,163,184,.15)';document.getElementById('player2Card').style.borderColor='rgba(148,163,184,.15)';if(currentPlayer===1)document.getElementById('player1Card').style.borderColor='#22d3ee';else document.getElementById('player2Card').style.borderColor='#22d3ee';timerInterval=setInterval(function(){if(currentPlayer===1){p1Time--;if(p1Time<=0){p1Time=0;stopTimer();updateDisplay();showToast('玩家1超时！玩家2获胜！');return}}else{p2Time--;if(p2Time<=0){p2Time=0;stopTimer();updateDisplay();showToast('玩家2超时！玩家1获胜！');return}}updateDisplay()},1000)}
function reset(){stopTimer();var initMin=parseInt(document.getElementById('initTime').value)||5;inc=parseInt(document.getElementById('increment').value)||0;p1Time=initMin*60;p2Time=initMin*60;currentPlayer=0;updateDisplay();document.getElementById('player1Card').style.borderColor='rgba(148,163,184,.15)';document.getElementById('player2Card').style.borderColor='rgba(148,163,184,.15)'}
document.getElementById('player1Card').addEventListener('click',function(){if(currentPlayer===0){currentPlayer=1;startTimer()}else if(currentPlayer===2){switchPlayer()}else{showToast('已经是玩家1的回合')}});
document.getElementById('player2Card').addEventListener('click',function(){if(currentPlayer===0){currentPlayer=2;startTimer()}else if(currentPlayer===1){switchPlayer()}else{showToast('已经是玩家2的回合')}});
document.getElementById('resetBtn').addEventListener('click',reset);
reset();''',
        "en_controls": '''<div class="input-row"><label>Initial Time (min)</label><input type="number" id="initTime" value="5" min="1" max="120" style="width:80px"><label>Increment (sec)</label><input type="number" id="increment" value="0" min="0" max="60" style="width:80px"><button class="btn btn-primary" id="resetBtn">Reset</button></div>
<div class="stats-grid"><div class="stat-card" id="player1Card" style="cursor:pointer"><div class="stat-label">Player 1 ♟️</div><div class="stat-value" id="player1Time" style="font-size:2rem">5:00</div><div class="stat-label">Tap to move</div></div><div class="stat-card" id="player2Card" style="cursor:pointer"><div class="stat-label">Player 2 ♟️</div><div class="stat-value" id="player2Time" style="font-size:2rem">5:00</div><div class="stat-label">Tap to move</div></div></div>
<div style="text-align:center;margin-top:12px;color:#64748b;font-size:.85rem">Tap a player card to start/switch the clock</div>''',
        "en_faqs": [("How does the chess clock work?","Set initial time and increment, then tap a player card to start timing. Each tap switches to the opponent."),("What is increment time?","Added seconds after each move (Fischer timing), commonly used in tournaments."),("Is data saved?","No, all data is local to this page. Refreshing resets the clock.")],
        "en_js": '''var p1Time,p2Time,currentPlayer,timerInterval,inc;
function formatTime(sec){var m=Math.floor(sec/60);var s=sec%60;return m+':'+String(s).padStart(2,'0')}
function updateDisplay(){document.getElementById('player1Time').textContent=formatTime(p1Time);document.getElementById('player2Time').textContent=formatTime(p2Time)}
function stopTimer(){if(timerInterval){clearInterval(timerInterval);timerInterval=null}}
function switchPlayer(){stopTimer();if(currentPlayer===1){p1Time+=inc;currentPlayer=2}else{p2Time+=inc;currentPlayer=1}updateDisplay();startTimer()}
function startTimer(){document.getElementById('player1Card').style.borderColor='rgba(148,163,184,.15)';document.getElementById('player2Card').style.borderColor='rgba(148,163,184,.15)';if(currentPlayer===1)document.getElementById('player1Card').style.borderColor='#22d3ee';else document.getElementById('player2Card').style.borderColor='#22d3ee';timerInterval=setInterval(function(){if(currentPlayer===1){p1Time--;if(p1Time<=0){p1Time=0;stopTimer();updateDisplay();showToast('Player 1 timeout! Player 2 wins!');return}}else{p2Time--;if(p2Time<=0){p2Time=0;stopTimer();updateDisplay();showToast('Player 2 timeout! Player 1 wins!');return}}updateDisplay()},1000)}
function reset(){stopTimer();var initMin=parseInt(document.getElementById('initTime').value)||5;inc=parseInt(document.getElementById('increment').value)||0;p1Time=initMin*60;p2Time=initMin*60;currentPlayer=0;updateDisplay();document.getElementById('player1Card').style.borderColor='rgba(148,163,184,.15)';document.getElementById('player2Card').style.borderColor='rgba(148,163,184,.15)'}
document.getElementById('player1Card').addEventListener('click',function(){if(currentPlayer===0){currentPlayer=1;startTimer()}else if(currentPlayer===2){switchPlayer()}else{showToast('Already Player 1 turn')}});
document.getElementById('player2Card').addEventListener('click',function(){if(currentPlayer===0){currentPlayer=2;startTimer()}else if(currentPlayer===1){switchPlayer()}else{showToast('Already Player 2 turn')}});
document.getElementById('resetBtn').addEventListener('click',reset);
reset();'''
    },
    "html-unescape": {
        "cn_controls": '''<div class="input-row"><textarea id="htmlInput" placeholder="输入HTML实体文本...(&amp; &lt; &gt; &quot; &#x27; &#39; &#60; &#62; &#38;)" style="flex:1;padding:12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;resize:vertical;min-height:100px;font-family:monospace"></textarea></div>
<div class="input-row"><button class="btn btn-primary" id="decodeBtn">解码</button><button class="btn btn-secondary" id="copyBtn">复制结果</button><button class="btn btn-secondary" id="clearBtn">清空</button></div>
<div class="result-label">解码结果</div><div class="result-box" id="result" style="min-height:60px;white-space:pre-wrap">等待输入...</div>''',
        "cn_faqs": [("什么是HTML实体？","HTML实体是用特殊代码表示字符的方式，如&amp;表示&。用于在HTML中安全显示保留字符。"),("支持哪些实体？","支持命名实体(&amp; &lt; &gt; &quot; &#x27; &#39;)和数字实体(&#38; &#x26; &#x0026;)。"),("解码是否安全？","完全在浏览器本地完成，不会上传或存储您的数据。")],
        "cn_js": '''document.getElementById('decodeBtn').addEventListener('click',function(){var t=document.getElementById('htmlInput').value;if(!t){showToast('请输入HTML实体文本');return}var el=document.createElement('textarea');el.innerHTML=t;document.getElementById('result').textContent=el.value});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t&&t!=='等待输入...'){navigator.clipboard.writeText(t).then(function(){showToast('已复制')})}});
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('htmlInput').value='';document.getElementById('result').textContent='等待输入...'});''',
        "en_controls": '''<div class="input-row"><textarea id="htmlInput" placeholder="Enter HTML entity text... (&amp; &lt; &gt; &quot; &#x27; &#39; &#60; &#62; &#38;)" style="flex:1;padding:12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;resize:vertical;min-height:100px;font-family:monospace"></textarea></div>
<div class="input-row"><button class="btn btn-primary" id="decodeBtn">Decode</button><button class="btn btn-secondary" id="copyBtn">Copy Result</button><button class="btn btn-secondary" id="clearBtn">Clear</button></div>
<div class="result-label">Decoded Result</div><div class="result-box" id="result" style="min-height:60px;white-space:pre-wrap">Waiting for input...</div>''',
        "en_faqs": [("What are HTML entities?","HTML entities are special codes representing characters, e.g. &amp; for &. Used to safely display reserved characters in HTML."),("Which entities are supported?","Named entities (&amp; &lt; &gt; &quot; &#x27; &#39;) and numeric entities (&#38; &#x26; &#x0026;)."),("Is decoding safe?","Completely done in your browser. No data is uploaded or stored.")],
        "en_js": '''document.getElementById('decodeBtn').addEventListener('click',function(){var t=document.getElementById('htmlInput').value;if(!t){showToast('Please enter HTML entity text');return}var el=document.createElement('textarea');el.innerHTML=t;document.getElementById('result').textContent=el.value});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t&&t!=='Waiting for input...'){navigator.clipboard.writeText(t).then(function(){showToast('Copied')})}});
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('htmlInput').value='';document.getElementById('result').textContent='Waiting for input...'});'''
    },
    "coin-flip-online": {
        "cn_controls": '''<div class="result-box" id="coinDisplay" style="text-align:center;font-size:5rem;padding:30px;cursor:pointer">🪙</div>
<div class="btn-row"><button class="btn btn-primary btn-large" id="flipBtn">抛硬币！</button><button class="btn btn-secondary" id="resetBtn">重置统计</button></div>
<div class="stats-grid"><div class="stat-card"><div class="stat-value" id="totalFlips">0</div><div class="stat-label">总次数</div></div><div class="stat-card"><div class="stat-value" id="headsCount">0</div><div class="stat-label">正面 🌞</div></div><div class="stat-card"><div class="stat-value" id="tailsCount">0</div><div class="stat-label">反面 🌙</div></div></div>''',
        "cn_faqs": [("抛硬币是真正随机的吗？","使用JavaScript的Math.random()生成随机数，虽然技术上不是真随机，但对日常使用足够公平。"),("可以连续抛吗？","可以，点击'抛硬币'按钮即可连续抛掷，统计数据会累计。"),("正面反面的概率是多少？","理论上各50%，随着抛掷次数增加会趋近50%。")],
        "cn_js": '''var total=0,heads=0,tails=0;
function updateStats(){document.getElementById('totalFlips').textContent=total;document.getElementById('headsCount').textContent=heads;document.getElementById('tailsCount').textContent=tails;var hPct=total>0?Math.round(heads/total*100):50;var tPct=total>0?Math.round(tails/total*100):50}
function flip(){var isHeads=Math.random()<0.5;total++;var coin=document.getElementById('coinDisplay');coin.style.transform='rotateY(720deg)';coin.style.transition='none';coin.textContent='🪙';setTimeout(function(){coin.style.transition='transform 0.6s ease-out';coin.style.transform='rotateY(0deg)';if(isHeads){coin.textContent='🌞';heads++}else{coin.textContent='🌙';tails++}updateStats()},50)}
document.getElementById('flipBtn').addEventListener('click',flip);
document.getElementById('coinDisplay').addEventListener('click',flip);
document.getElementById('resetBtn').addEventListener('click',function(){total=0;heads=0;tails=0;document.getElementById('coinDisplay').textContent='🪙';updateStats()});''',
        "en_controls": '''<div class="result-box" id="coinDisplay" style="text-align:center;font-size:5rem;padding:30px;cursor:pointer">🪙</div>
<div class="btn-row"><button class="btn btn-primary btn-large" id="flipBtn">Flip Coin!</button><button class="btn btn-secondary" id="resetBtn">Reset Stats</button></div>
<div class="stats-grid"><div class="stat-card"><div class="stat-value" id="totalFlips">0</div><div class="stat-label">Total Flips</div></div><div class="stat-card"><div class="stat-value" id="headsCount">0</div><div class="stat-label">Heads 🌞</div></div><div class="stat-card"><div class="stat-value" id="tailsCount">0</div><div class="stat-label">Tails 🌙</div></div></div>''',
        "en_faqs": [("Is the coin flip truly random?","Uses JavaScript Math.random(). Not cryptographically random, but fair enough for everyday use."),("Can I flip multiple times?","Yes, click 'Flip Coin' continuously. Statistics accumulate across flips."),("What's the heads/tails probability?","Theoretically 50% each. As flips increase, results converge toward 50%.")],
        "en_js": '''var total=0,heads=0,tails=0;
function updateStats(){document.getElementById('totalFlips').textContent=total;document.getElementById('headsCount').textContent=heads;document.getElementById('tailsCount').textContent=tails}
function flip(){var isHeads=Math.random()<0.5;total++;var coin=document.getElementById('coinDisplay');coin.style.transform='rotateY(720deg)';coin.style.transition='none';coin.textContent='🪙';setTimeout(function(){coin.style.transition='transform 0.6s ease-out';coin.style.transform='rotateY(0deg)';if(isHeads){coin.textContent='🌞';heads++}else{coin.textContent='🌙';tails++}updateStats()},50)}
document.getElementById('flipBtn').addEventListener('click',flip);
document.getElementById('coinDisplay').addEventListener('click',flip);
document.getElementById('resetBtn').addEventListener('click',function(){total=0;heads=0;tails=0;document.getElementById('coinDisplay').textContent='🪙';updateStats()});'''
    }
}

def build_page(slug, cn_name, en_name, cn_desc, en_desc, category, cn_icon, en_icon, cn_keywords, en_keywords, is_en=False):
    """构建工具页面HTML"""
    td = TOOL_DATA.get(slug, {})
    
    if is_en:
        head_top = EN_HEAD_TOP
        title = f"{en_name} - Free ToolBase"
        desc = en_desc
        keywords = en_keywords
        icon = en_icon
        lang = "en"
        hreflang_cn = f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">'
        hreflang_en = f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">'
        canonical = f'https://free-toolbase.com/en/{slug}/'
        og_url = canonical
        breadcrumb_home = "Home"
        breadcrumb_tools = "Tools"
        breadcrumb_name = en_name
        home_url = "https://free-toolbase.com/en/"
        tools_url = "https://free-toolbase.com/en/#tools"
        item_url = canonical
        lang_switch = f'<a href="../../{slug}/">中文</a><a href="index.html" class="active">EN</a>'
        nav_back = f'<a href="../../index.html">Home</a> &rsaquo; <a href="../../#tools">Tools</a> &rsaquo; {en_name}'
        hero_badge = "🔒 No registration · Data never uploaded"
        privacy_text = "All processing happens locally in your browser. No data is ever uploaded."
        footer_links = '<a href="../">Home</a> | <a href="../about/">About</a> | <a href="../contact/">Contact</a> | <a href="../privacy/">Privacy</a>'
        footer_copy = "© 2026 Free ToolBase. All rights reserved."
        controls = td.get("en_controls", "")
        faqs = td.get("en_faqs", [])
        extra_js = td.get("en_js", "")
        faq_json = ','.join([f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in faqs])
        meta_desc = desc[:160]
    else:
        head_top = CN_HEAD_TOP
        title = f"{cn_name} - Free ToolBase"
        desc = cn_desc
        keywords = cn_keywords
        icon = cn_icon
        lang = "zh-CN"
        hreflang_cn = f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">'
        hreflang_en = f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">'
        canonical = f'https://free-toolbase.com/{slug}/'
        og_url = canonical
        breadcrumb_home = "首页"
        breadcrumb_tools = "工具"
        breadcrumb_name = cn_name
        home_url = "https://free-toolbase.com/"
        tools_url = "https://free-toolbase.com/#tools"
        item_url = canonical
        lang_switch = f'<a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a>'
        nav_back = f'<a href="../index.html">首页</a> &rsaquo; <a href="../#tools">工具</a> &rsaquo; {cn_name}'
        hero_badge = "🔒 无需注册 · 数据绝不上传"
        privacy_text = "所有处理均在浏览器本地完成，数据不会上传到服务器。"
        footer_links = '<a href="../">首页</a> | <a href="../about/">关于</a> | <a href="../contact/">联系</a> | <a href="../privacy/">隐私</a>'
        footer_copy = "© 2026 Free ToolBase. All rights reserved."
        controls = td.get("cn_controls", "")
        faqs = td.get("cn_faqs", [])
        extra_js = td.get("cn_js", "")
        faq_json = ','.join([f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in faqs])
        meta_desc = desc[:160]
    
    faq_html = '\n'.join([f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faqs])
    
    return f'''{head_top}<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
{hreflang_cn}
{hreflang_en}
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{cn_name if not is_en else en_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{breadcrumb_home}","item":"{home_url}"}},{{"@type":"ListItem","position":2,"name":"{breadcrumb_tools}","item":"{tools_url}"}},{{"@type":"ListItem","position":3,"name":"{breadcrumb_name}","item":"{item_url}"}}]}}</script>
{CSS}
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {cn_name if not is_en else en_name}</h1><div class="lang-switch">{lang_switch}</div></div>
<p class="nav-back">{nav_back}</p>
<div class="hero"><p>{desc} <span class="badge">{hero_badge}</span></p></div>
<div class="panel">
  <div class="panel-title">{icon} {cn_name if not is_en else en_name}</div>
  {controls}
</div>
<div class="privacy-note">🔒 <span>{privacy_text}</span></div>
<div class="panel">
  <div class="panel-title">{'❓ 常见问题' if not is_en else '❓ FAQ'}</div>
{faq_html}</div>
<div class="footer">{footer_links}<br>{footer_copy}</div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
{extra_js}
</script>
</body>
</html>'''

# 批量生成文件
for tool in TOOLS:
    slug = tool["slug"]
    os.makedirs(f"{BASE}/{slug}", exist_ok=True)
    os.makedirs(f"{BASE}/en/{slug}", exist_ok=True)
    
    cn_html = build_page(**tool, is_en=False)
    en_html = build_page(**tool, is_en=True)
    
    with open(f"{BASE}/{slug}/index.html", "w") as f:
        f.write(cn_html)
    with open(f"{BASE}/en/{slug}/index.html", "w") as f:
        f.write(en_html)
    
    print(f"✅ {slug} (CN + EN)")

print(f"\n完成！共生成 {len(TOOLS)} 个工具（每个CN+EN）")
