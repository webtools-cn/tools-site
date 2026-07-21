#!/usr/bin/env python3
"""使用模板v3创建 timestamp-to-date 工具"""
import sys
sys.path.insert(0, '/home/chison/tools-site/_gen')
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

TOOL_HTML_CN = '''
<div class="form-group"><label>Unix 时间戳（秒或毫秒）</label><input type="text" id="tsInput" placeholder="例如: 1710691200 或 1710691200000" oninput="convertTs()"></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>当前时区时间</label><input type="text" id="localResult" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>UTC 时间</label><input type="text" id="utcResult" readonly placeholder="--"></div></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>ISO 8601</label><input type="text" id="isoResult" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>RFC 2822</label><input type="text" id="rfcResult" readonly placeholder="--"></div></div>
<div class="form-group"><label>相对时间</label><input type="text" id="relativeResult" readonly placeholder="--"></div>
<hr style="border-color:rgba(148,163,184,.1);margin:20px 0">
<div class="form-group"><label>日期时间 → 时间戳</label><input type="datetime-local" id="dateInput" onchange="convertDate()"></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>Unix 秒</label><input type="text" id="tsSeconds" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>Unix 毫秒</label><input type="text" id="tsMillis" readonly placeholder="--"></div></div>
<div class="form-group"><label>当前时间戳</label><input type="text" id="nowTs" readonly><button class="btn btn-primary" style="margin-top:8px;width:100%" onclick="copyNowTs()">📋 复制当前时间戳</button></div>
'''

TOOL_HTML_EN = '''
<div class="form-group"><label>Unix Timestamp (seconds or milliseconds)</label><input type="text" id="tsInput" placeholder="e.g. 1710691200 or 1710691200000" oninput="convertTs()"></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>Local Time</label><input type="text" id="localResult" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>UTC Time</label><input type="text" id="utcResult" readonly placeholder="--"></div></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>ISO 8601</label><input type="text" id="isoResult" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>RFC 2822</label><input type="text" id="rfcResult" readonly placeholder="--"></div></div>
<div class="form-group"><label>Relative Time</label><input type="text" id="relativeResult" readonly placeholder="--"></div>
<hr style="border-color:rgba(148,163,184,.1);margin:20px 0">
<div class="form-group"><label>Date/Time → Timestamp</label><input type="datetime-local" id="dateInput" onchange="convertDate()"></div>
<div class="form-row"><div class="form-group" style="flex:1"><label>Unix Seconds</label><input type="text" id="tsSeconds" readonly placeholder="--"></div><div class="form-group" style="flex:1"><label>Unix Milliseconds</label><input type="text" id="tsMillis" readonly placeholder="--"></div></div>
<div class="form-group"><label>Current Timestamp</label><input type="text" id="nowTs" readonly><button class="btn btn-primary" style="margin-top:8px;width:100%" onclick="copyNowTs()">📋 Copy Current Timestamp</button></div>
'''

TOOL_JS = '''
function fmtDate(d){var y=d.getFullYear();var m=String(d.getMonth()+1).padStart(2,'0');var day=String(d.getDate()).padStart(2,'0');var h=String(d.getHours()).padStart(2,'0');var min=String(d.getMinutes()).padStart(2,'0');var s=String(d.getSeconds()).padStart(2,'0');return y+'-'+m+'-'+day+' '+h+':'+min+':'+s}
function fmtUTC(d){return d.getUTCFullYear()+'-'+String(d.getUTCMonth()+1).padStart(2,'0')+'-'+String(d.getUTCDate()).padStart(2,'0')+' '+String(d.getUTCHours()).padStart(2,'0')+':'+String(d.getUTCMinutes()).padStart(2,'0')+':'+String(d.getUTCSeconds()).padStart(2,'0')}
function relativeTime(d){var now=Date.now();var diff=now-d.getTime();var abs=Math.abs(diff);var sec=Math.floor(abs/1000);var min=Math.floor(sec/60);var hr=Math.floor(min/60);var day=Math.floor(hr/24);var mo=Math.floor(day/30);var yr=Math.floor(day/365);var prefix=diff>0?'前':'后';if(yr>=1)return yr+'年'+prefix;if(mo>=1)return mo+'个月'+prefix;if(day>=1)return day+'天'+prefix;if(hr>=1)return hr+'小时'+prefix;if(min>=1)return min+'分钟'+prefix;return sec+'秒'+prefix}
function relativeTimeEn(d){var now=Date.now();var diff=now-d.getTime();var abs=Math.abs(diff);var sec=Math.floor(abs/1000);var min=Math.floor(sec/60);var hr=Math.floor(min/60);var day=Math.floor(hr/24);var mo=Math.floor(day/30);var yr=Math.floor(day/365);var suffix=diff>0?' ago':' from now';if(yr>=1)return yr+' year'+(yr>1?'s':'')+suffix;if(mo>=1)return mo+' month'+(mo>1?'s':'')+suffix;if(day>=1)return day+' day'+(day>1?'s':'')+suffix;if(hr>=1)return hr+' hour'+(hr>1?'s':'')+suffix;if(min>=1)return min+' minute'+(min>1?'s':'')+suffix;return sec+' second'+(sec>1?'s':'')+suffix}
function isCN(){return document.documentElement.lang==='zh-CN'}
function convertTs(){var v=document.getElementById('tsInput').value.trim();if(!v){clearAll();return}var ts=parseInt(v,10);if(isNaN(ts)||ts<=0){clearAll();return}if(ts>9999999999999)ts=Math.floor(ts/1000);if(ts<10000000000)ts=ts*1000;var d=new Date(ts);if(isNaN(d.getTime())){clearAll();return}document.getElementById('localResult').value=fmtDate(d);document.getElementById('utcResult').value=fmtUTC(d);document.getElementById('isoResult').value=d.toISOString();document.getElementById('rfcResult').value=d.toUTCString();document.getElementById('relativeResult').value=isCN()?relativeTime(d):relativeTimeEn(d)}
function clearAll(){var ids=['localResult','utcResult','isoResult','rfcResult','relativeResult'];for(var i=0;i<ids.length;i++)document.getElementById(ids[i]).value='--'}
function convertDate(){var v=document.getElementById('dateInput').value;if(!v){document.getElementById('tsSeconds').value='--';document.getElementById('tsMillis').value='--';return}var d=new Date(v);var sec=Math.floor(d.getTime()/1000);document.getElementById('tsSeconds').value=sec;document.getElementById('tsMillis').value=d.getTime()}
function updateNow(){var now=Date.now();document.getElementById('nowTs').value=Math.floor(now/1000)+' (秒) / '+now+' (毫秒)'}
function copyNowTs(){var ts=String(Math.floor(Date.now()/1000));navigator.clipboard.writeText(ts).then(function(){showToast(isCN()?'已复制: '+ts:'Copied: '+ts)})['catch'](function(){showToast(isCN()?'复制失败':'Copy failed')})}
updateNow();setInterval(updateNow,1000);
'''

cn_path, en_path = builder.build_bilingual(
    slug='timestamp-to-date',
    title_cn='Unix时间戳转换器',
    title_en='Unix Timestamp Converter',
    desc_cn='在线Unix时间戳转换工具，支持时间戳转日期、日期转时间戳。支持秒和毫秒，自动识别。显示本地时间、UTC时间、ISO 8601、RFC 2822等多种格式。纯前端计算，数据不上传服务器。',
    desc_en='Free online Unix timestamp converter. Convert timestamps to dates and vice versa. Supports seconds and milliseconds with auto-detection. Displays local time, UTC, ISO 8601, RFC 2822 formats. Pure frontend, no server uploads.',
    icon='⏱️',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=TOOL_HTML_CN,
    tool_html_en=TOOL_HTML_EN,
    tool_js=TOOL_JS,
    faqs_cn=[
        ('什么是Unix时间戳？', 'Unix时间戳是从1970年1月1日00:00:00 UTC开始经过的秒数（或毫秒数），不含闰秒。它是计算机系统中广泛使用的时间表示方式。'),
        ('如何区分秒和毫秒？', '本工具自动识别：10位数字为秒，13位数字为毫秒。当前Unix秒约为17亿，毫秒约为1.7万亿。'),
        ('支持哪些时间格式？', '支持本地时间、UTC时间、ISO 8601（如2024-03-18T00:00:00.000Z）、RFC 2822（如Mon, 18 Mar 2024 00:00:00 GMT）、相对时间等格式。'),
        ('数据会上传到服务器吗？', '不会。所有时间转换计算均在浏览器本地完成，数据不会上传到任何服务器，保护您的隐私安全。'),
        ('日期转时间戳的时区是什么？', '使用日期时间选择器选择的时间为您的本地时区时间，转换后的时间戳为UTC Unix时间戳。'),
    ],
    faqs_en=[
        ('What is a Unix timestamp?', 'A Unix timestamp is the number of seconds (or milliseconds) that have elapsed since January 1, 1970 00:00:00 UTC, excluding leap seconds. It is widely used in computer systems.'),
        ('How to distinguish seconds from milliseconds?', 'This tool auto-detects: 10-digit numbers are seconds, 13-digit numbers are milliseconds. Current Unix seconds are around 1.7 billion.'),
        ('What time formats are supported?', 'Local time, UTC, ISO 8601 (e.g. 2024-03-18T00:00:00.000Z), RFC 2822 (e.g. Mon, 18 Mar 2024 00:00:00 GMT), relative time, and more.'),
        ('Is my data uploaded to a server?', 'No. All timestamp conversions are performed locally in your browser. No data is ever uploaded to any server.'),
        ('What timezone is used for date-to-timestamp conversion?', 'The datetime-local picker uses your local timezone. The resulting timestamp is a UTC Unix timestamp.'),
    ],
    seo_cn='<h2>Unix时间戳转换器 - 秒/毫秒互转</h2><p>Unix时间戳是计算机科学中最常用的时间表示方式，定义为从1970年1月1日00:00:00 UTC至今的秒数。本工具提供快速准确的Unix时间戳与人类可读日期之间的相互转换，支持秒级和毫秒级时间戳自动识别。</p><h3>为什么需要时间戳转换？</h3><p>在API开发、数据库查询、日志分析等场景中，Unix时间戳无处不在。开发者经常需要将时间戳转换为可读格式进行调试，或将日期转换为时间戳用于编程。</p><h3>功能特点</h3><ul><li>自动识别10位秒级和13位毫秒级时间戳</li><li>同时显示本地时间、UTC时间、ISO 8601和RFC 2822格式</li><li>支持日期时间选择器反向转换为Unix时间戳</li><li>实时显示当前Unix时间戳</li><li>纯前端计算，数据绝不上传服务器</li></ul>',
    seo_en='<h2>Unix Timestamp Converter - Seconds/Milliseconds</h2><p>The Unix timestamp is the most widely used time representation in computer science, defined as the number of seconds since January 1, 1970 00:00:00 UTC. This tool provides fast and accurate conversion between Unix timestamps and human-readable dates, with automatic detection of second and millisecond precision.</p><h3>Why use a timestamp converter?</h3><p>In API development, database queries, log analysis, and more, Unix timestamps are everywhere. Developers frequently need to convert timestamps to readable formats for debugging, or convert dates to timestamps for programming.</p><h3>Features</h3><ul><li>Auto-detects 10-digit seconds and 13-digit milliseconds</li><li>Displays local time, UTC, ISO 8601, and RFC 2822 formats simultaneously</li><li>Supports reverse conversion from datetime picker to Unix timestamp</li><li>Real-time current Unix timestamp display</li><li>Pure frontend computation, no server uploads</li></ul>',
)

print(f"✅ 中文: {cn_path}")
print(f"✅ 英文: {en_path}")