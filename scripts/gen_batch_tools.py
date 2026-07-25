#!/usr/bin/env python3
"""批量生成5个新工具（中英文双语）"""
import os

BASE = '/home/chison/tools-site'

# Google Analytics + AdSense + error suppression 通用头部
COMMON_HEAD_START = '''<!DOCTYPE html>
<html lang="__LANG__">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

COMMON_HEAD_END = '''<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.ad-slot{{background:rgba(148,163,184,.06);border:1px dashed rgba(148,163,184,.15);border-radius:8px;padding:12px;text-align:center;color:#475569;font-size:.8rem;margin-bottom:16px;min-height:60px;display:flex;align-items:center;justify-content:center}}
.tool-section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.tool-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.content-section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.content-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.content-section h3{{font-size:1rem;color:#e2e8f0;margin:16px 0 8px}}
.content-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:10px;text-align:justify}}
.content-section ul{{padding-left:20px;color:#94a3b8;font-size:.9rem}}
.content-section li{{margin-bottom:6px}}
.faq-item{{margin-bottom:16px}}
.faq-item .q{{font-weight:500;color:#e2e8f0;margin-bottom:6px;font-size:.9rem}}
.faq-item .a{{color:#94a3b8;font-size:.85rem;padding-left:12px;border-left:2px solid rgba(6,182,212,.3)}}
.footer{{margin-top:32px;padding:24px 0;border-top:1px solid rgba(148,163,184,.1);text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);padding:10px 24px;background:#1e293b;color:#e2e8f0;border-radius:8px;font-size:.85rem;z-index:1000;opacity:0;transition:opacity .3s;border:1px solid rgba(148,163,184,.2);pointer-events:none}}
.toast.show{{opacity:1}}
label{{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
input,select,textarea{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.9rem;outline:none;width:100%}}
input:focus,select:focus,textarea:focus{{border-color:rgba(6,182,212,.5)}}
button{{padding:8px 16px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-box{{padding:16px;background:#0f172a;border:1px solid rgba(6,182,212,.3);border-radius:8px;margin-top:16px}}
.result-box .label{{font-size:.75rem;color:#64748b}}
.result-box .value{{font-size:1.2rem;font-family:monospace;color:#22d3ee;font-weight:600;margin-top:4px;word-break:break-all}}
@media(max-width:600px){{.header h1{{font-size:1.2rem}}}}
.hero{{margin-bottom:16px;padding:12px 16px;background:rgba(148,163,184,.06);border-radius:8px;border:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}}
.hero .badge{{font-size:.75rem;padding:2px 10px;border-radius:12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);white-space:nowrap}}
.input-group{{margin-bottom:12px}}
.input-row{{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}}
.input-row .input-group{{flex:1;min-width:120px;margin-bottom:0}}
.output-area{{min-height:60px;padding:12px;background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;color:#e2e8f0;font-size:.9rem;margin-top:8px;white-space:pre-wrap;word-break:break-all}}
</style>
</head>
<body>
<div class="container">
'''

COMMON_FOOTER_START = '''
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: 2026-07-25
  </span>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="__HP__index.html">__HP__首页</a>
<a href="__HP__index.html#tools">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="__HP__privacy/">隐私政策</a>
<a href="__HP__terms/">服务条款</a>
<a href="__HP__about/">关于我们</a>
</footer>
<p>__TOOLNAME__ | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
</script>
</body>
</html>'''

# ==================== 工具1: cron-to-text ====================
def build_cron_to_text(lang, slug, tool_name, desc_text, en_slug_path, home_prefix):
    cn_active = 'active' if lang == 'zh-CN' else ''
    en_active = 'active' if lang == 'en' else ''
    is_cn = lang == 'zh-CN'
    
    title = f'{tool_name} - Free ToolBase'
    desc = desc_text
    kw = tool_name
    canon = f'https://free-toolbase.com/{slug}/'
    
    # Schema
    schema_name = tool_name
    
    head = COMMON_HEAD_START.replace('__LANG__', lang)
    head += f'<meta name="description" content="{desc}">\n'
    head += f'<meta name="keywords" content="{kw},在线工具,免费工具">\n'
    head += f'<title>{title}</title>\n'
    head += f'<link rel="canonical" href="{canon}">\n'
    head += f'<meta property="og:title" content="{title}">\n'
    head += f'<meta property="og:description" content="{desc}">\n'
    head += f'<meta property="og:url" content="{canon}">\n'
    head += f'<meta property="og:type" content="website">\n'
    head += f'<meta property="og:site_name" content="Free ToolBase">\n'
    head += f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{schema_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>\n'
    head += COMMON_HEAD_END
    
    # Header
    lang_sw = f'<div class="lang-switch"><a href="index.html" class="{cn_active}">中文</a><a href="{en_slug_path}" class="{en_active}">EN</a></div>'
    nav = f'<p class="nav-back"><a href="{home_prefix}index.html">{home_prefix}首页</a> &rsaquo; {tool_name}</p>'
    
    if is_cn:
        hero_text = f'{desc} | 无需注册 · 数据绝不上传服务器'
        hero_badge = '零依赖·可离线使用'
    else:
        hero_text = f'{desc_text} | No registration · Data never leaves your browser'
        hero_badge = 'Zero dependencies · Works offline'
    
    body = f'<div class="header"><h1>{tool_name}</h1>{lang_sw}</div>\n'
    body += nav + '\n'
    body += f'<div class="hero"><p>{hero_text}</p><span class="badge">{hero_badge}</span></div>\n'
    
    # Tool section
    if is_cn:
        body += '''<div class="tool-section">
<h2>⏰ Cron表达式解读</h2>
<div class="input-group">
<label>Cron表达式</label>
<div style="display:flex;gap:8px">
<input type="text" id="cronInput" placeholder="例如: */5 * * * * 或 0 9 * * 1-5" value="0 9 * * 1-5" style="flex:1;font-family:monospace">
<button class="btn-primary" id="parseBtn">解读</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">解读结果</div>
<div class="value" id="cronDesc" style="font-size:1rem"></div>
<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(148,163,184,.1)">
<div class="label">各字段含义</div>
<div id="fieldDetail" style="color:#94a3b8;font-size:.85rem;margin-top:4px;line-height:1.8"></div>
</div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
<div style="margin-top:12px">
<label style="font-size:.8rem;color:#64748b">常用示例</label>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px">'''
        examples = [
            ('* * * * *', '每分钟'),
            ('*/5 * * * *', '每5分钟'),
            ('0 * * * *', '每小时整点'),
            ('0 9 * * 1-5', '工作日9点'),
            ('0 0 * * *', '每天午夜'),
            ('0 0 1 * *', '每月1日'),
            ('0 2 * * 0', '周日凌晨2点'),
            ('30 4 * * 6', '周六4:30'),
        ]
        for expr, label in examples:
            body += f'<button class="btn-secondary example-btn" data-cron="{expr}" style="font-size:.75rem;padding:4px 10px">{label}</button>\n'
        body += '</div></div></div>\n'
    else:
        body += '''<div class="tool-section">
<h2>⏰ Cron Expression Parser</h2>
<div class="input-group">
<label>Cron Expression</label>
<div style="display:flex;gap:8px">
<input type="text" id="cronInput" placeholder="e.g. */5 * * * * or 0 9 * * 1-5" value="0 9 * * 1-5" style="flex:1;font-family:monospace">
<button class="btn-primary" id="parseBtn">Parse</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Parsed Result</div>
<div class="value" id="cronDesc" style="font-size:1rem"></div>
<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(148,163,184,.1)">
<div class="label">Field Details</div>
<div id="fieldDetail" style="color:#94a3b8;font-size:.85rem;margin-top:4px;line-height:1.8"></div>
</div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
<div style="margin-top:12px">
<label style="font-size:.8rem;color:#64748b">Common Examples</label>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px">'''
        examples = [
            ('* * * * *', 'Every minute'),
            ('*/5 * * * *', 'Every 5 min'),
            ('0 * * * *', 'Every hour'),
            ('0 9 * * 1-5', 'Weekdays 9AM'),
            ('0 0 * * *', 'Midnight'),
            ('0 0 1 * *', '1st of month'),
            ('0 2 * * 0', 'Sun 2AM'),
            ('30 4 * * 6', 'Sat 4:30AM'),
        ]
        for expr, label in examples:
            body += f'<button class="btn-secondary example-btn" data-cron="{expr}" style="font-size:.75rem;padding:4px 10px">{label}</button>\n'
        body += '</div></div></div>\n'
    
    # Content sections
    if is_cn:
        body += '''<div class="content-section">
<h2>📖 Cron表达式格式</h2>
<p>Cron表达式由5个字段组成，用空格分隔：<code>分钟 小时 日 月 星期</code></p>
<ul>
<li><strong>分钟</strong>：0-59</li>
<li><strong>小时</strong>：0-23</li>
<li><strong>日</strong>：1-31</li>
<li><strong>月</strong>：1-12</li>
<li><strong>星期</strong>：0-7（0和7都表示周日）</li>
</ul>
<p>特殊字符：<code>*</code>（任意）、<code>,</code>（列表）、<code>-</code>（范围）、<code>/</code>（步进）</p>
</div>
<div class="content-section">
<h2>💼 应用场景</h2>
<p>Cron表达式广泛应用于：Linux服务器定时备份、自动发送邮件报告、定期清理日志文件、定时抓取数据、计划性系统维护等场景。</p>
</div>'''
    else:
        body += '''<div class="content-section">
<h2>📖 Cron Expression Format</h2>
<p>A cron expression consists of 5 fields separated by spaces: <code>minute hour day month weekday</code></p>
<ul>
<li><strong>Minute</strong>: 0-59</li>
<li><strong>Hour</strong>: 0-23</li>
<li><strong>Day</strong>: 1-31</li>
<li><strong>Month</strong>: 1-12</li>
<li><strong>Weekday</strong>: 0-7 (0 and 7 both represent Sunday)</li>
</ul>
<p>Special characters: <code>*</code> (any), <code>,</code> (list), <code>-</code> (range), <code>/</code> (step)</p>
</div>
<div class="content-section">
<h2>💼 Use Cases</h2>
<p>Cron expressions are widely used for: Linux server scheduled backups, automated email reports, log rotation, data scraping, and system maintenance tasks.</p>
</div>'''
    
    # JS
    js = '''
<script>
var fieldNames = {zh:['分钟','小时','日','月','星期'],en:['Minute','Hour','Day','Month','Weekday']};
var weekNames = {zh:['周日','周一','周二','周三','周四','周五','周六','周日'],en:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']};
var monthNames = {zh:['','一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],en:['','January','February','March','April','May','June','July','August','September','October','November','December']};

function describeField(val, type, lang){
  var isEn = lang === 'en';
  if(val === '*') return isEn ? 'every' : '每';
  var parts = val.split(',');
  var descs = [];
  for(var i=0;i<parts.length;i++){
    var p = parts[i];
    if(p.includes('/')){
      var sp = p.split('/');
      var base = sp[0] === '*' ? (isEn ? 'every' : '每') : sp[0];
      descs.push((isEn ? 'every ' : '每') + sp[1] + ' ' + (type==='minute'?(isEn?'min':'分'):type==='hour'?(isEn?'hr':'时'):''));
    } else if(p.includes('-')){
      var rp = p.split('-');
      descs.push(rp[0] + '-' + rp[1]);
    } else {
      descs.push(p);
    }
  }
  return descs.join(',');
}

function parseCron(expr){
  var isEn = document.documentElement.lang === 'en';
  var fields = expr.trim().split(/\\s+/);
  if(fields.length !== 5){
    document.getElementById('errorBox').style.display = 'block';
    document.getElementById('errorBox').textContent = isEn ? 'Invalid cron expression: need 5 fields' : '无效的Cron表达式：需要5个字段';
    document.getElementById('resultBox').style.display = 'none';
    return;
  }
  document.getElementById('errorBox').style.display = 'none';
  document.getElementById('resultBox').style.display = 'block';
  
  var minute = fields[0], hour = fields[1], day = fields[2], month = fields[3], week = fields[4];
  var fn = fieldNames[isEn?'en':'zh'];
  
  // Build description
  var desc = '';
  if(minute === '*' && hour === '*' && day === '*' && month === '*' && week === '*'){
    desc = isEn ? 'Every minute' : '每分钟';
  } else if(hour === '*' && day === '*' && month === '*' && week === '*'){
    if(minute.includes('*/')){
      var m = minute.split('/')[1];
      desc = (isEn ? 'Every ' + m + ' minutes' : '每' + m + '分钟');
    } else {
      desc = (isEn ? 'At minute ' + minute + ' of every hour' : '每小时的第' + minute + '分钟');
    }
  } else if(day === '*' && month === '*' && week === '*'){
    var hDesc = hour === '*' ? (isEn ? 'every hour' : '每小时') : (isEn ? 'at ' + hour + ':00' : hour + '点');
    var mDesc = minute === '0' ? '' : (isEn ? ':' + minute : ':' + minute + '分');
    desc = hDesc + mDesc;
    if(day === '*' && month === '*' && week === '*') desc += (isEn ? ' every day' : ' 每天');
  } else if(day !== '*' && month === '*'){
    desc = (isEn ? 'At ' + hour + ':' + (minute==='0'?'00':minute) + ' on day ' + day + ' of every month' : '每月' + day + '日 ' + hour + ':' + (minute==='0'?'00':minute));
  } else if(week !== '*'){
    var wDesc = week.replace(/0/g,'7');
    if(wDesc === '1-5') wDesc = isEn ? 'weekdays' : '工作日';
    else if(wDesc === '6,7') wDesc = isEn ? 'weekends' : '周末';
    else wDesc = (isEn ? 'day ' : '星期') + wDesc;
    desc = (isEn ? 'At ' + hour + ':' + (minute==='0'?'00':minute) + ' on ' + wDesc : '每' + wDesc + ' ' + hour + ':' + (minute==='0'?'00':minute));
  } else {
    desc = expr;
  }
  
  document.getElementById('cronDesc').textContent = desc;
  
  // Field details
  var detail = '';
  var vals = [minute, hour, day, month, week];
  var types = ['minute','hour','day','month','week'];
  for(var i=0;i<5;i++){
    detail += '<strong>' + fn[i] + '</strong>: ' + vals[i] + ' — ' + describeField(vals[i], types[i], isEn ? 'en' : 'zh') + '<br>';
  }
  document.getElementById('fieldDetail').innerHTML = detail;
}

document.getElementById('parseBtn').addEventListener('click', function(){
  parseCron(document.getElementById('cronInput').value);
});

document.querySelectorAll('.example-btn').forEach(function(btn){
  btn.addEventListener('click', function(){
    document.getElementById('cronInput').value = this.dataset.cron;
    parseCron(this.dataset.cron);
  });
});

// Parse on load
parseCron('0 9 * * 1-5');
</script>
'''
    
    footer = COMMON_FOOTER_START.replace('__HP__', home_prefix).replace('__TOOLNAME__', tool_name)
    return head + body + js + footer

# ==================== 工具2: roman-numerals ====================
def build_roman_numerals(lang, slug, tool_name, desc_text, en_slug_path, home_prefix):
    cn_active = 'active' if lang == 'zh-CN' else ''
    en_active = 'active' if lang == 'en' else ''
    is_cn = lang == 'zh-CN'
    
    title = f'{tool_name} - Free ToolBase'
    desc = desc_text
    canon = f'https://free-toolbase.com/{slug}/'
    
    head = COMMON_HEAD_START.replace('__LANG__', lang)
    head += f'<meta name="description" content="{desc}">\n'
    head += f'<meta name="keywords" content="{tool_name},在线工具,免费工具">\n'
    head += f'<title>{title}</title>\n'
    head += f'<link rel="canonical" href="{canon}">\n'
    head += f'<meta property="og:title" content="{title}">\n'
    head += f'<meta property="og:description" content="{desc}">\n'
    head += f'<meta property="og:url" content="{canon}">\n'
    head += f'<meta property="og:type" content="website">\n'
    head += f'<meta property="og:site_name" content="Free ToolBase">\n'
    head += f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>\n'
    head += COMMON_HEAD_END
    
    lang_sw = f'<div class="lang-switch"><a href="index.html" class="{cn_active}">中文</a><a href="{en_slug_path}" class="{en_active}">EN</a></div>'
    nav = f'<p class="nav-back"><a href="{home_prefix}index.html">{home_prefix}首页</a> &rsaquo; {tool_name}</p>'
    
    if is_cn:
        hero_text = f'{desc} | 无需注册 · 数据绝不上传服务器'
        hero_badge = '零依赖·可离线使用'
    else:
        hero_text = f'{desc_text} | No registration · Data never leaves your browser'
        hero_badge = 'Zero dependencies · Works offline'
    
    body = f'<div class="header"><h1>{tool_name}</h1>{lang_sw}</div>\n'
    body += nav + '\n'
    body += f'<div class="hero"><p>{hero_text}</p><span class="badge">{hero_badge}</span></div>\n'
    
    if is_cn:
        body += '''<div class="tool-section">
<h2>🔢 罗马数字转换器</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div>
<div class="input-group">
<label>阿拉伯数字 → 罗马数字</label>
<div style="display:flex;gap:8px">
<input type="number" id="arabicInput" placeholder="输入数字 (1-3999)" min="1" max="3999" value="2024">
<button class="btn-primary" id="toRomanBtn">转换</button>
</div>
</div>
</div>
<div>
<div class="input-group">
<label>罗马数字 → 阿拉伯数字</label>
<div style="display:flex;gap:8px">
<input type="text" id="romanInput" placeholder="输入罗马数字" value="MMXXIV" style="text-transform:uppercase">
<button class="btn-primary" id="toArabicBtn">转换</button>
</div>
</div>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label" id="resultLabel"></div>
<div class="value" id="resultValue"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    else:
        body += '''<div class="tool-section">
<h2>🔢 Roman Numerals Converter</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div>
<div class="input-group">
<label>Arabic → Roman</label>
<div style="display:flex;gap:8px">
<input type="number" id="arabicInput" placeholder="Enter number (1-3999)" min="1" max="3999" value="2024">
<button class="btn-primary" id="toRomanBtn">Convert</button>
</div>
</div>
</div>
<div>
<div class="input-group">
<label>Roman → Arabic</label>
<div style="display:flex;gap:8px">
<input type="text" id="romanInput" placeholder="Enter Roman numeral" value="MMXXIV" style="text-transform:uppercase">
<button class="btn-primary" id="toArabicBtn">Convert</button>
</div>
</div>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label" id="resultLabel"></div>
<div class="value" id="resultValue"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    
    if is_cn:
        body += '''<div class="content-section">
<h2>📖 罗马数字对照表</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:4px;font-family:monospace;font-size:.85rem">
<span>I = 1</span><span>V = 5</span><span>X = 10</span><span>L = 50</span>
<span>C = 100</span><span>D = 500</span><span>M = 1000</span>
<span>IV = 4</span><span>IX = 9</span><span>XL = 40</span><span>XC = 90</span>
<span>CD = 400</span><span>CM = 900</span>
</div>
</div>'''
    else:
        body += '''<div class="content-section">
<h2>📖 Roman Numeral Chart</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:4px;font-family:monospace;font-size:.85rem">
<span>I = 1</span><span>V = 5</span><span>X = 10</span><span>L = 50</span>
<span>C = 100</span><span>D = 500</span><span>M = 1000</span>
<span>IV = 4</span><span>IX = 9</span><span>XL = 40</span><span>XC = 90</span>
<span>CD = 400</span><span>CM = 900</span>
</div>
</div>'''
    
    js = '''
<script>
var romanMap = [
  [1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],
  [100,'C'],[90,'XC'],[50,'L'],[40,'XL'],
  [10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']
];

function toRoman(num){
  if(num < 1 || num > 3999 || !Number.isInteger(num)) return null;
  var result = '';
  for(var i=0;i<romanMap.length;i++){
    while(num >= romanMap[i][0]){
      result += romanMap[i][1];
      num -= romanMap[i][0];
    }
  }
  return result;
}

function toArabic(roman){
  var r = roman.toUpperCase().trim();
  if(!/^[IVXLCDM]+$/.test(r)) return null;
  var map = {I:1,V:5,X:10,L:50,C:100,D:500,M:1000};
  var total = 0;
  for(var i=0;i<r.length;i++){
    var cur = map[r[i]];
    var next = map[r[i+1]] || 0;
    if(cur < next) total -= cur;
    else total += cur;
  }
  if(total < 1 || total > 3999) return null;
  if(toRoman(total) !== r) return null;
  return total;
}

function showResult(label, value){
  document.getElementById('errorBox').style.display = 'none';
  document.getElementById('resultBox').style.display = 'block';
  document.getElementById('resultLabel').textContent = label;
  document.getElementById('resultValue').textContent = value;
}

function showError(msg){
  document.getElementById('resultBox').style.display = 'none';
  document.getElementById('errorBox').style.display = 'block';
  document.getElementById('errorBox').textContent = msg;
}

var isEn = document.documentElement.lang === 'en';

document.getElementById('toRomanBtn').addEventListener('click', function(){
  var val = parseInt(document.getElementById('arabicInput').value);
  if(isNaN(val) || val < 1 || val > 3999){
    showError(isEn ? 'Please enter a number between 1 and 3999' : '请输入1-3999之间的数字');
    return;
  }
  var r = toRoman(val);
  showResult(isEn ? 'Roman numeral' : '罗马数字', r);
});

document.getElementById('toArabicBtn').addEventListener('click', function(){
  var val = document.getElementById('romanInput').value.trim();
  if(!val){
    showError(isEn ? 'Please enter a Roman numeral' : '请输入罗马数字');
    return;
  }
  var a = toArabic(val);
  if(a === null){
    showError(isEn ? 'Invalid Roman numeral' : '无效的罗马数字');
    return;
  }
  showResult(isEn ? 'Arabic number' : '阿拉伯数字', a);
});

// On load
showResult(isEn ? 'Roman numeral' : '罗马数字', toRoman(2024));
</script>
'''
    
    footer = COMMON_FOOTER_START.replace('__HP__', home_prefix).replace('__TOOLNAME__', tool_name)
    return head + body + js + footer

# ==================== 工具3: expense-splitter ====================
def build_expense_splitter(lang, slug, tool_name, desc_text, en_slug_path, home_prefix):
    cn_active = 'active' if lang == 'zh-CN' else ''
    en_active = 'active' if lang == 'en' else ''
    is_cn = lang == 'zh-CN'
    
    title = f'{tool_name} - Free ToolBase'
    desc = desc_text
    canon = f'https://free-toolbase.com/{slug}/'
    
    head = COMMON_HEAD_START.replace('__LANG__', lang)
    head += f'<meta name="description" content="{desc}">\n'
    head += f'<meta name="keywords" content="{tool_name},在线工具,免费工具">\n'
    head += f'<title>{title}</title>\n'
    head += f'<link rel="canonical" href="{canon}">\n'
    head += f'<meta property="og:title" content="{title}">\n'
    head += f'<meta property="og:description" content="{desc}">\n'
    head += f'<meta property="og:url" content="{canon}">\n'
    head += f'<meta property="og:type" content="website">\n'
    head += f'<meta property="og:site_name" content="Free ToolBase">\n'
    head += f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>\n'
    head += COMMON_HEAD_END
    
    lang_sw = f'<div class="lang-switch"><a href="index.html" class="{cn_active}">中文</a><a href="{en_slug_path}" class="{en_active}">EN</a></div>'
    nav = f'<p class="nav-back"><a href="{home_prefix}index.html">{home_prefix}首页</a> &rsaquo; {tool_name}</p>'
    
    if is_cn:
        hero_text = f'{desc} | 无需注册 · 数据绝不上传服务器'
        hero_badge = '零依赖·可离线使用'
    else:
        hero_text = f'{desc_text} | No registration · Data never leaves your browser'
        hero_badge = 'Zero dependencies · Works offline'
    
    body = f'<div class="header"><h1>{tool_name}</h1>{lang_sw}</div>\n'
    body += nav + '\n'
    body += f'<div class="hero"><p>{hero_text}</p><span class="badge">{hero_badge}</span></div>\n'
    
    if is_cn:
        body += '''<div class="tool-section">
<h2>💰 账单分摊计算器</h2>
<div class="input-group">
<label>总金额</label>
<input type="number" id="totalAmount" placeholder="输入总金额" value="500" step="0.01" min="0">
</div>
<div class="input-group">
<label>分摊人数</label>
<input type="number" id="peopleCount" placeholder="输入人数" value="4" min="1" max="100">
</div>
<div class="input-group">
<label>分摊方式</label>
<select id="splitMode">
<option value="equal">平均分摊</option>
<option value="ratio">按比例分摊（用逗号分隔，如: 1,2,1,1）</option>
<option value="custom">自定义金额（用逗号分隔，如: 120,150,130,100）</option>
</select>
</div>
<div class="input-group" id="ratioGroup" style="display:none">
<label>比例（逗号分隔）</label>
<input type="text" id="ratioInput" placeholder="例如: 1,2,1,1">
</div>
<div class="input-group" id="customGroup" style="display:none">
<label>自定义金额（逗号分隔）</label>
<input type="text" id="customInput" placeholder="例如: 120,150,130,100">
</div>
<button class="btn-primary" id="calcBtn" style="width:100%">计算分摊</button>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">分摊结果</div>
<div id="splitResults" style="margin-top:8px"></div>
<div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8">
<span id="totalCheck"></span>
</div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    else:
        body += '''<div class="tool-section">
<h2>💰 Expense Splitter</h2>
<div class="input-group">
<label>Total Amount</label>
<input type="number" id="totalAmount" placeholder="Enter total amount" value="500" step="0.01" min="0">
</div>
<div class="input-group">
<label>Number of People</label>
<input type="number" id="peopleCount" placeholder="Number of people" value="4" min="1" max="100">
</div>
<div class="input-group">
<label>Split Method</label>
<select id="splitMode">
<option value="equal">Equal Split</option>
<option value="ratio">By Ratio (comma-separated, e.g. 1,2,1,1)</option>
<option value="custom">Custom Amounts (comma-separated, e.g. 120,150,130,100)</option>
</select>
</div>
<div class="input-group" id="ratioGroup" style="display:none">
<label>Ratios (comma-separated)</label>
<input type="text" id="ratioInput" placeholder="e.g. 1,2,1,1">
</div>
<div class="input-group" id="customGroup" style="display:none">
<label>Custom Amounts (comma-separated)</label>
<input type="text" id="customInput" placeholder="e.g. 120,150,130,100">
</div>
<button class="btn-primary" id="calcBtn" style="width:100%">Calculate</button>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Split Results</div>
<div id="splitResults" style="margin-top:8px"></div>
<div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8">
<span id="totalCheck"></span>
</div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    
    if is_cn:
        body += '''<div class="content-section">
<h2>💼 使用场景</h2>
<p>适用于：朋友聚餐AA制、旅行费用分摊、合租账单分配、团建活动费用等。支持平均分摊、按比例分配和自定义金额三种模式。</p>
</div>'''
    else:
        body += '''<div class="content-section">
<h2>💼 Use Cases</h2>
<p>Perfect for: splitting restaurant bills, travel expenses, shared rent, group activities. Supports equal split, ratio-based split, and custom amount split.</p>
</div>'''
    
    js = '''
<script>
var isEn = document.documentElement.lang === 'en';

document.getElementById('splitMode').addEventListener('change', function(){
  var mode = this.value;
  document.getElementById('ratioGroup').style.display = mode === 'ratio' ? 'block' : 'none';
  document.getElementById('customGroup').style.display = mode === 'custom' ? 'block' : 'none';
});

function showError(msg){
  document.getElementById('resultBox').style.display = 'none';
  document.getElementById('errorBox').style.display = 'block';
  document.getElementById('errorBox').textContent = msg;
}

document.getElementById('calcBtn').addEventListener('click', function(){
  document.getElementById('errorBox').style.display = 'none';
  var total = parseFloat(document.getElementById('totalAmount').value);
  var count = parseInt(document.getElementById('peopleCount').value);
  var mode = document.getElementById('splitMode').value;
  
  if(isNaN(total) || total <= 0){
    showError(isEn ? 'Please enter a valid total amount' : '请输入有效的总金额');
    return;
  }
  if(isNaN(count) || count < 1){
    showError(isEn ? 'Please enter a valid number of people' : '请输入有效的人数');
    return;
  }
  
  var amounts = [];
  
  if(mode === 'equal'){
    var perPerson = Math.round(total / count * 100) / 100;
    var sum = 0;
    for(var i=0;i<count-1;i++){
      amounts.push(perPerson);
      sum += perPerson;
    }
    amounts.push(Math.round((total - sum) * 100) / 100);
  } else if(mode === 'ratio'){
    var ratioStr = document.getElementById('ratioInput').value.trim();
    if(!ratioStr){
      showError(isEn ? 'Please enter ratios' : '请输入比例');
      return;
    }
    var ratios = ratioStr.split(',').map(Number);
    if(ratios.length !== count){
      showError(isEn ? 'Number of ratios must match number of people' : '比例数量必须等于人数');
      return;
    }
    var ratioSum = ratios.reduce(function(a,b){return a+b;},0);
    var distributed = 0;
    for(var i=0;i<count-1;i++){
      var amt = Math.round(total * ratios[i] / ratioSum * 100) / 100;
      amounts.push(amt);
      distributed += amt;
    }
    amounts.push(Math.round((total - distributed) * 100) / 100);
  } else {
    var customStr = document.getElementById('customInput').value.trim();
    if(!customStr){
      showError(isEn ? 'Please enter custom amounts' : '请输入自定义金额');
      return;
    }
    amounts = customStr.split(',').map(Number);
    if(amounts.length !== count){
      showError(isEn ? 'Number of amounts must match number of people' : '金额数量必须等于人数');
      return;
    }
    var customSum = amounts.reduce(function(a,b){return a+b;},0);
    if(Math.abs(customSum - total) > 0.02){
      showError(isEn ? 'Custom amounts sum (' + customSum + ') does not match total (' + total + ')' : '自定义金额总和(' + customSum + ')与总金额(' + total + ')不匹配');
      return;
    }
  }
  
  document.getElementById('resultBox').style.display = 'block';
  var html = '';
  var sumCheck = 0;
  for(var i=0;i<amounts.length;i++){
    html += '<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.05)"><span>' + (isEn ? 'Person ' : '第') + (i+1) + (isEn ? '' : '人') + '</span><span style="font-family:monospace;color:#22d3ee">$' + amounts[i].toFixed(2) + '</span></div>';
    sumCheck += amounts[i];
  }
  document.getElementById('splitResults').innerHTML = html;
  document.getElementById('totalCheck').textContent = (isEn ? 'Total: $' : '合计: $') + sumCheck.toFixed(2);
});
</script>
'''
    
    footer = COMMON_FOOTER_START.replace('__HP__', home_prefix).replace('__TOOLNAME__', tool_name)
    return head + body + js + footer

# ==================== 工具4: one-rep-max ====================
def build_one_rep_max(lang, slug, tool_name, desc_text, en_slug_path, home_prefix):
    cn_active = 'active' if lang == 'zh-CN' else ''
    en_active = 'active' if lang == 'en' else ''
    is_cn = lang == 'zh-CN'
    
    title = f'{tool_name} - Free ToolBase'
    desc = desc_text
    canon = f'https://free-toolbase.com/{slug}/'
    
    head = COMMON_HEAD_START.replace('__LANG__', lang)
    head += f'<meta name="description" content="{desc}">\n'
    head += f'<meta name="keywords" content="{tool_name},在线工具,免费工具">\n'
    head += f'<title>{title}</title>\n'
    head += f'<link rel="canonical" href="{canon}">\n'
    head += f'<meta property="og:title" content="{title}">\n'
    head += f'<meta property="og:description" content="{desc}">\n'
    head += f'<meta property="og:url" content="{canon}">\n'
    head += f'<meta property="og:type" content="website">\n'
    head += f'<meta property="og:site_name" content="Free ToolBase">\n'
    head += f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>\n'
    head += COMMON_HEAD_END
    
    lang_sw = f'<div class="lang-switch"><a href="index.html" class="{cn_active}">中文</a><a href="{en_slug_path}" class="{en_active}">EN</a></div>'
    nav = f'<p class="nav-back"><a href="{home_prefix}index.html">{home_prefix}首页</a> &rsaquo; {tool_name}</p>'
    
    if is_cn:
        hero_text = f'{desc} | 无需注册 · 数据绝不上传服务器'
        hero_badge = '零依赖·可离线使用'
    else:
        hero_text = f'{desc_text} | No registration · Data never leaves your browser'
        hero_badge = 'Zero dependencies · Works offline'
    
    body = f'<div class="header"><h1>{tool_name}</h1>{lang_sw}</div>\n'
    body += nav + '\n'
    body += f'<div class="hero"><p>{hero_text}</p><span class="badge">{hero_badge}</span></div>\n'
    
    if is_cn:
        body += '''<div class="tool-section">
<h2>💪 1RM力量计算器</h2>
<div class="input-group">
<label>举起的重量 (kg/lb)</label>
<input type="number" id="weight" placeholder="输入重量" value="100" step="0.5" min="0">
</div>
<div class="input-group">
<label>重复次数</label>
<input type="number" id="reps" placeholder="输入次数" value="5" min="1" max="30">
</div>
<div class="input-group">
<label>单位</label>
<select id="unit">
<option value="kg">kg (公斤)</option>
<option value="lb">lb (磅)</option>
</select>
</div>
<button class="btn-primary" id="calcBtn" style="width:100%">计算1RM</button>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">估算结果</div>
<div id="rmResults" style="margin-top:8px"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    else:
        body += '''<div class="tool-section">
<h2>💪 1RM Calculator</h2>
<div class="input-group">
<label>Weight Lifted (kg/lb)</label>
<input type="number" id="weight" placeholder="Enter weight" value="100" step="0.5" min="0">
</div>
<div class="input-group">
<label>Repetitions</label>
<input type="number" id="reps" placeholder="Enter reps" value="5" min="1" max="30">
</div>
<div class="input-group">
<label>Unit</label>
<select id="unit">
<option value="kg">kg</option>
<option value="lb">lb</option>
</select>
</div>
<button class="btn-primary" id="calcBtn" style="width:100%">Calculate 1RM</button>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Estimated 1RM</div>
<div id="rmResults" style="margin-top:8px"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    
    if is_cn:
        body += '''<div class="content-section">
<h2>📖 计算公式</h2>
<p>本工具使用以下公式估算1RM：</p>
<ul>
<li><strong>Epley公式</strong>：1RM = 重量 × (1 + 次数/30)</li>
<li><strong>Brzycki公式</strong>：1RM = 重量 × 36 / (37 - 次数)</li>
<li><strong>Lander公式</strong>：1RM = 100 × 重量 / (101.3 - 2.67123 × 次数)</li>
<li><strong>平均1RM</strong>：以上三种公式的平均值</li>
</ul>
</div>'''
    else:
        body += '''<div class="content-section">
<h2>📖 Formulas Used</h2>
<p>This calculator uses the following formulas:</p>
<ul>
<li><strong>Epley</strong>: 1RM = Weight × (1 + Reps/30)</li>
<li><strong>Brzycki</strong>: 1RM = Weight × 36 / (37 - Reps)</li>
<li><strong>Lander</strong>: 1RM = 100 × Weight / (101.3 - 2.67123 × Reps)</li>
<li><strong>Average</strong>: Average of the three formulas above</li>
</ul>
</div>'''
    
    js = '''
<script>
var isEn = document.documentElement.lang === 'en';

function showError(msg){
  document.getElementById('resultBox').style.display = 'none';
  document.getElementById('errorBox').style.display = 'block';
  document.getElementById('errorBox').textContent = msg;
}

document.getElementById('calcBtn').addEventListener('click', function(){
  document.getElementById('errorBox').style.display = 'none';
  var weight = parseFloat(document.getElementById('weight').value);
  var reps = parseInt(document.getElementById('reps').value);
  var unit = document.getElementById('unit').value;
  
  if(isNaN(weight) || weight <= 0){
    showError(isEn ? 'Please enter a valid weight' : '请输入有效的重量');
    return;
  }
  if(isNaN(reps) || reps < 1 || reps > 30){
    showError(isEn ? 'Please enter reps between 1-30' : '请输入1-30之间的次数');
    return;
  }
  
  var epley = weight * (1 + reps / 30);
  var brzycki = weight * 36 / (37 - reps);
  var lander = 100 * weight / (101.3 - 2.67123 * reps);
  var avg = (epley + brzycki + lander) / 3;
  
  var u = unit === 'kg' ? 'kg' : 'lb';
  var round = function(v){ return Math.round(v * 10) / 10; };
  
  document.getElementById('resultBox').style.display = 'block';
  document.getElementById('rmResults').innerHTML = 
    '<div style="margin-bottom:8px;font-size:1.3rem;color:#22d3ee;font-weight:600">' + (isEn ? 'Average 1RM' : '平均1RM') + ': ' + round(avg) + ' ' + u + '</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.85rem;color:#94a3b8">' +
    '<div>Epley: <span style="color:#e2e8f0">' + round(epley) + ' ' + u + '</span></div>' +
    '<div>Brzycki: <span style="color:#e2e8f0">' + round(brzycki) + ' ' + u + '</span></div>' +
    '<div>Lander: <span style="color:#e2e8f0">' + round(lander) + ' ' + u + '</span></div>' +
    '</div>';
});
</script>
'''
    
    footer = COMMON_FOOTER_START.replace('__HP__', home_prefix).replace('__TOOLNAME__', tool_name)
    return head + body + js + footer

# ==================== 工具5: unicode-decode ====================
def build_unicode_decode(lang, slug, tool_name, desc_text, en_slug_path, home_prefix):
    cn_active = 'active' if lang == 'zh-CN' else ''
    en_active = 'active' if lang == 'en' else ''
    is_cn = lang == 'zh-CN'
    
    title = f'{tool_name} - Free ToolBase'
    desc = desc_text
    canon = f'https://free-toolbase.com/{slug}/'
    
    head = COMMON_HEAD_START.replace('__LANG__', lang)
    head += f'<meta name="description" content="{desc}">\n'
    head += f'<meta name="keywords" content="{tool_name},在线工具,免费工具">\n'
    head += f'<title>{title}</title>\n'
    head += f'<link rel="canonical" href="{canon}">\n'
    head += f'<meta property="og:title" content="{title}">\n'
    head += f'<meta property="og:description" content="{desc}">\n'
    head += f'<meta property="og:url" content="{canon}">\n'
    head += f'<meta property="og:type" content="website">\n'
    head += f'<meta property="og:site_name" content="Free ToolBase">\n'
    head += f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">\n'
    head += f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>\n'
    head += COMMON_HEAD_END
    
    lang_sw = f'<div class="lang-switch"><a href="index.html" class="{cn_active}">中文</a><a href="{en_slug_path}" class="{en_active}">EN</a></div>'
    nav = f'<p class="nav-back"><a href="{home_prefix}index.html">{home_prefix}首页</a> &rsaquo; {tool_name}</p>'
    
    if is_cn:
        hero_text = f'{desc} | 无需注册 · 数据绝不上传服务器'
        hero_badge = '零依赖·可离线使用'
    else:
        hero_text = f'{desc_text} | No registration · Data never leaves your browser'
        hero_badge = 'Zero dependencies · Works offline'
    
    body = f'<div class="header"><h1>{tool_name}</h1>{lang_sw}</div>\n'
    body += nav + '\n'
    body += f'<div class="hero"><p>{hero_text}</p><span class="badge">{hero_badge}</span></div>\n'
    
    if is_cn:
        body += '''<div class="tool-section">
<h2>🔤 Unicode编码解码</h2>
<div class="input-group">
<label>输入文本（支持 \\\\uXXXX、&#XXXX;、U+XXXX 格式）</label>
<textarea id="inputText" rows="4" placeholder="输入Unicode编码文本...">\\\\u4f60\\\\u597d \\\\u4e16\\\\u754c</textarea>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
<button class="btn-primary" id="decodeBtn">解码 (Unicode → 文字)</button>
<button class="btn-secondary" id="encodeBtn">编码 (文字 → Unicode)</button>
<button class="btn-secondary" id="copyBtn">📋 复制结果</button>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">结果</div>
<div class="value" id="outputText" style="font-size:1.1rem"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    else:
        body += '''<div class="tool-section">
<h2>🔤 Unicode Encoder/Decoder</h2>
<div class="input-group">
<label>Input text (supports \\\\uXXXX, &#XXXX;, U+XXXX formats)</label>
<textarea id="inputText" rows="4" placeholder="Enter Unicode text...">\\\\u4f60\\\\u597d \\\\u4e16\\\\u754c</textarea>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
<button class="btn-primary" id="decodeBtn">Decode (Unicode → Text)</button>
<button class="btn-secondary" id="encodeBtn">Encode (Text → Unicode)</button>
<button class="btn-secondary" id="copyBtn">📋 Copy Result</button>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Result</div>
<div class="value" id="outputText" style="font-size:1.1rem"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>'''
    
    if is_cn:
        body += '''<div class="content-section">
<h2>📖 支持格式</h2>
<p>本工具支持以下Unicode编码格式的互转：</p>
<ul>
<li><code>\\\\uXXXX</code> — JavaScript/JSON格式（如 \\\\u4f60）</li>
<li><code>&#XXXX;</code> — HTML实体格式（如 &#20320;）</li>
<li><code>U+XXXX</code> — Unicode标准格式（如 U+4F60）</li>
<li>以上格式混合文本自动识别解码</li>
</ul>
</div>'''
    else:
        body += '''<div class="content-section">
<h2>📖 Supported Formats</h2>
<p>This tool supports conversion between the following Unicode formats:</p>
<ul>
<li><code>\\\\uXXXX</code> — JavaScript/JSON format (e.g. \\\\u4f60)</li>
<li><code>&#XXXX;</code> — HTML entity format (e.g. &#20320;)</li>
<li><code>U+XXXX</code> — Unicode standard format (e.g. U+4F60)</li>
<li>Mixed format text is auto-detected and decoded</li>
</ul>
</div>'''
    
    js = '''
<script>
var isEn = document.documentElement.lang === 'en';

function decodeUnicode(text){
  // Handle \\uXXXX
  text = text.replace(/\\\\u([0-9a-fA-F]{4})/g, function(m, g){
    return String.fromCharCode(parseInt(g, 16));
  });
  // Handle U+XXXX
  text = text.replace(/U\\+([0-9a-fA-F]{4,6})/g, function(m, g){
    var cp = parseInt(g, 16);
    if(cp > 0xFFFF){
      cp -= 0x10000;
      return String.fromCharCode(0xD800 + (cp >> 10), 0xDC00 + (cp & 0x3FF));
    }
    return String.fromCharCode(cp);
  });
  // Handle &#XXXX; and &#xXXXX;
  text = text.replace(/&#x?([0-9a-fA-F]+);/g, function(m, g){
    return String.fromCharCode(parseInt(g, m.indexOf('x') > -1 ? 16 : 10));
  });
  return text;
}

function encodeUnicode(text){
  return text.split('').map(function(c){
    var code = c.charCodeAt(0);
    if(code > 127) return '\\\\u' + code.toString(16).padStart(4, '0');
    return c;
  }).join('');
}

function showResult(text){
  document.getElementById('errorBox').style.display = 'none';
  document.getElementById('resultBox').style.display = 'block';
  document.getElementById('outputText').textContent = text;
}

document.getElementById('decodeBtn').addEventListener('click', function(){
  var input = document.getElementById('inputText').value;
  if(!input.trim()){
    document.getElementById('errorBox').style.display = 'block';
    document.getElementById('errorBox').textContent = isEn ? 'Please enter text to decode' : '请输入要解码的文本';
    return;
  }
  showResult(decodeUnicode(input));
});

document.getElementById('encodeBtn').addEventListener('click', function(){
  var input = document.getElementById('inputText').value;
  if(!input.trim()){
    document.getElementById('errorBox').style.display = 'block';
    document.getElementById('errorBox').textContent = isEn ? 'Please enter text to encode' : '请输入要编码的文本';
    return;
  }
  showResult(encodeUnicode(input));
});

document.getElementById('copyBtn').addEventListener('click', function(){
  var text = document.getElementById('outputText').textContent;
  if(!text) return;
  navigator.clipboard.writeText(text).then(function(){
    showToast(isEn ? 'Copied!' : '已复制');
  }).catch(function(){
    showToast(isEn ? 'Copy failed' : '复制失败');
  });
});

// Decode on load
showResult(decodeUnicode('\\\\u4f60\\\\u597d \\\\u4e16\\\\u754c'));
</script>
'''
    
    footer = COMMON_FOOTER_START.replace('__HP__', home_prefix).replace('__TOOLNAME__', tool_name)
    return head + body + js + footer

# ==================== 构建所有工具 ====================
tools = [
    {
        'slug': 'cron-to-text',
        'cn_name': '⏰ Cron表达式解读',
        'en_name': '⏰ Cron Expression Parser',
        'cn_desc': '将Cron表达式翻译为人类可读的自然语言描述，帮助理解和验证定时任务配置。支持标准5字段Cron格式。',
        'en_desc': 'Translate cron expressions into human-readable natural language. Supports standard 5-field cron format.',
        'builder': build_cron_to_text,
    },
    {
        'slug': 'roman-numerals',
        'cn_name': '🔢 罗马数字转换',
        'en_name': '🔢 Roman Numerals Converter',
        'cn_desc': '在线罗马数字与阿拉伯数字互转，支持1-3999范围转换。双向转换，实时验证。',
        'en_desc': 'Convert between Roman numerals and Arabic numbers online. Supports 1-3999 range with bidirectional conversion.',
        'builder': build_roman_numerals,
    },
    {
        'slug': 'expense-splitter',
        'cn_name': '💰 账单分摊计算器',
        'en_name': '💰 Expense Splitter',
        'cn_desc': '多人聚餐/旅行账单公平分摊，支持平均分摊、按比例分配和自定义金额三种模式。',
        'en_desc': 'Fairly split bills for group dining and travel. Supports equal split, ratio-based, and custom amount modes.',
        'builder': build_expense_splitter,
    },
    {
        'slug': 'one-rep-max',
        'cn_name': '💪 1RM力量计算器',
        'en_name': '💪 One Rep Max Calculator',
        'cn_desc': '根据举起的重量和重复次数估算最大重复次数(1RM)，使用Epley/Brzycki/Lander三种公式。',
        'en_desc': 'Estimate your one-rep max from weight and reps using Epley, Brzycki, and Lander formulas.',
        'builder': build_one_rep_max,
    },
    {
        'slug': 'unicode-decode',
        'cn_name': '🔤 Unicode编码解码',
        'en_name': '🔤 Unicode Decoder',
        'cn_desc': '在线Unicode/UTF-8编码解码工具，支持\\\\uXXXX、&#XXXX;、U+XXXX多种格式互转。',
        'en_desc': 'Online Unicode encoder/decoder supporting \\\\uXXXX, &#XXXX;, and U+XXXX format conversion.',
        'builder': build_unicode_decode,
    },
]

for tool in tools:
    slug = tool['slug']
    
    # CN version
    cn_path = os.path.join(BASE, slug, 'index.html')
    os.makedirs(os.path.join(BASE, slug), exist_ok=True)
    cn_html = tool['builder']('zh-CN', slug, tool['cn_name'], tool['cn_desc'], f'../en/{slug}/', '../')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f'✅ CN: {slug}/index.html')
    
    # EN version
    en_path = os.path.join(BASE, 'en', slug, 'index.html')
    os.makedirs(os.path.join(BASE, 'en', slug), exist_ok=True)
    en_html = tool['builder']('en', slug, tool['en_name'], tool['en_desc'], f'../../{slug}/', '../../')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✅ EN: en/{slug}/index.html')

print('\n🎉 All 5 tools (10 pages) generated!')