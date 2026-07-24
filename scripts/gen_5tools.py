#!/usr/bin/env python3
"""直接写入5个新工具的文件"""
import os

BASE = "/home/chison/tools-site"

CSS_LIGHT = """*{box-sizing:border-box;margin:0;padding:0}body{background:#f8fafc;color:#1e293b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#4F46E5;text-decoration:none}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.6rem}.lang-switch{display:flex;gap:4px;background:#fff;border-radius:8px;padding:4px;border:1px solid #e2e8f0}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#64748b}.lang-switch a.active{background:#EEF2FF;color:#4F46E5;font-weight:600}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.nav-back a:hover{color:#4F46E5}.panel{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.1)}.panel-title{font-size:1.1rem;margin-bottom:14px;font-weight:600}.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}.btn-primary{background:#4F46E5;color:#fff}.btn-primary:hover{opacity:.9;transform:translateY(-1px)}.btn-secondary{background:#fff;color:#1e293b;border:1px solid #e2e8f0}.btn-secondary:hover{background:#f8fafc}.btn-large{padding:12px 32px;font-size:1.1rem;font-weight:600}.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}input,select,textarea{padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;background:#fff;color:#1e293b;font-size:.9rem;width:100%}input:focus,select:focus,textarea:focus{outline:none;border-color:#4F46E5;box-shadow:0 0 0 3px rgba(79,70,229,.1)}textarea{min-height:120px;resize:vertical;font-family:monospace}label{font-weight:500;font-size:.85rem;display:block;margin-bottom:4px}.result-area{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px;min-height:40px;word-break:break-all;font-family:monospace;font-size:.9rem;margin-top:8px;max-height:300px;overflow-y:auto;white-space:pre-wrap}.faq-item{margin-bottom:16px;border-bottom:1px solid #e2e8f0;padding-bottom:16px}.faq-item:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}.faq-q{font-weight:600;margin-bottom:6px}.faq-a{color:#64748b;font-size:.9rem}.privacy-note{background:#EEF2FF;border:1px solid rgba(79,70,229,.15);border-radius:8px;padding:12px 16px;font-size:.85rem;color:#64748b;margin-top:16px;display:flex;align-items:center;gap:8px}.footer{border-top:1px solid #e2e8f0;padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.footer a:hover{color:#4F46E5}.hero{margin-bottom:20px}.hero p{color:#64748b;font-size:.95rem;line-height:1.7}.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:#EEF2FF;color:#4F46E5;border:1px solid rgba(79,70,229,.2);margin-top:8px}.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 24px;border-radius:8px;font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}.toast.show{opacity:1}.stat-box{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px;text-align:center}@media(max-width:640px){.header h1{font-size:1.3rem}}"""

CSS_DARK = """*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#06b6d4;text-decoration:none}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.6rem;color:#f1f5f9}.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.nav-back a:hover{color:#94a3b8}.panel{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.panel-title{font-size:1.1rem;color:#f1f5f9;margin-bottom:14px;font-weight:600}.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}.btn-primary:hover{background:rgba(6,182,212,.35);transform:translateY(-1px)}.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}.btn-secondary:hover{background:rgba(148,163,184,.2)}.btn-large{padding:12px 32px;font-size:1.1rem;font-weight:600}.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}input,select,textarea{padding:10px 12px;border:1px solid rgba(148,163,184,.1);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;width:100%}input:focus,select:focus,textarea:focus{outline:none;border-color:#06b6d4}label{font-weight:500;font-size:.85rem;color:#94a3b8;display:block;margin-bottom:4px}.result-area{background:#0f172a;border:1px solid rgba(148,163,184,.1);border-radius:8px;padding:12px;min-height:40px;word-break:break-all;font-family:monospace;font-size:.9rem;margin-top:8px;max-height:300px;overflow-y:auto;white-space:pre-wrap}.faq-item{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.1);padding-bottom:16px}.faq-item:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}.faq-q{font-weight:600;color:#f1f5f9;margin-bottom:6px}.faq-a{color:#94a3b8;font-size:.9rem}.privacy-note{background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.15);border-radius:8px;padding:12px 16px;font-size:.85rem;color:#94a3b8;margin-top:16px;display:flex;align-items:center;gap:8px}.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.footer a:hover{color:#94a3b8}.hero{margin-bottom:20px}.hero p{color:#94a3b8;font-size:.95rem;line-height:1.7}.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);margin-top:8px}.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}.toast.show{opacity:1}.stat-box{background:#0f172a;border:1px solid rgba(148,163,184,.1);border-radius:8px;padding:14px;text-align:center}@media(max-width:640px){.header h1{font-size:1.3rem}}"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

def make_head(slug, name, desc, kw, meta_title, og_title, faq_pairs, howto_steps, lang):
    is_cn = lang == "zh"
    la = "zh-CN" if is_cn else "en"
    h_self = "zh" if is_cn else "en"
    h_alt = "en" if is_cn else "zh"
    canonical = f"https://free-toolbase.com/{'' if is_cn else 'en/'}{slug}/"
    alt_url = f"https://free-toolbase.com/{'en/' if is_cn else ''}{slug}/"
    
    faq_json = ",".join([f'{{"@type":"Question","name":"{q.replace(chr(34),chr(39))}","acceptedAnswer":{{"@type":"Answer","text":"{a.replace(chr(34),chr(39))}"}}}}' for q,a in faq_pairs])
    step_json = ",".join([f'{{"@type":"HowToStep","position":{i+1},"name":"{s[0]}","text":"{s[1]}"}}' for i,s in enumerate(howto_steps)])
    home_name = "首页" if is_cn else "Home"
    tools_name = "工具" if is_cn else "Tools"
    
    hdr = f'''<!DOCTYPE html>
<html lang="{la}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<title>{meta_title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{h_self}" href="{canonical}">
<link rel="alternate" hreflang="{h_alt}" href="{alt_url}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{name}","description":"{name}使用步骤","totalTime":"PT1M","tool":{{"@type":"HowToTool","name":"{name}"}},"step":[{step_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_name}","item":"https://free-toolbase.com/{'' if is_cn else 'en/'}"}},{{"@type":"ListItem","position":2,"name":"{tools_name}","item":"https://free-toolbase.com/{'' if is_cn else 'en/'}#tools"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"{canonical}"}}]}}</script>
'''
    return hdr

def make_footer(tool, lang):
    is_cn = lang == "zh"
    slug = tool["slug"]
    name = tool["name_zh"] if is_cn else tool["name_en"]
    prefix = "../" if is_cn else "../"
    en_link = f"../en/{slug}/" if is_cn else f"../{slug}/"
    en_label = "EN" if is_cn else "中文"
    home = "首页" if is_cn else "Home"
    tools = "全部工具" if is_cn else "All Tools"
    contact = "联系我们" if is_cn else "Contact"
    privacy = "隐私政策" if is_cn else "Privacy"
    terms = "服务条款" if is_cn else "Terms"
    about = "关于我们" if is_cn else "About"
    no_reg = "无需注册 · 数据绝不上传服务器" if is_cn else "No registration · Data never leaves your browser"
    feedback = "问题反馈" if is_cn else "Feedback"
    col = "#475569" if is_cn else "#999"
    return f'''<div class="footer container">
<div style="margin-bottom:12px">
<a href="{prefix}index.html">{home}</a>
<a href="{prefix}#tools">{tools}</a>
<a href="mailto:dexshuang@google.com">{contact}</a>
<a href="{prefix}privacy/">{privacy}</a>
<a href="{prefix}terms/">{terms}</a>
<a href="{prefix}about/">{about}</a>
<a href="{en_link}">{en_label}</a>
</div>
<p>{name} | {no_reg}</p>
<p style="margin-top:8px;color:{col};font-size:.8rem">{feedback}: dexshuang@google.com</p>
</div>'''

def make_faq(tool, lang):
    is_cn = lang == "zh"
    faq_pairs = tool["faq_zh"] if is_cn else tool["faq_en"]
    items = "\n".join([f'  <div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q,a in faq_pairs])
    title = "❓ 常见问题" if is_cn else "❓ FAQ"
    return f'''<div class="panel">
  <div class="panel-title">{title}</div>
{items}
</div>'''

def make_header(tool, lang):
    is_cn = lang == "zh"
    slug = tool["slug"]
    name = tool["name_zh"] if is_cn else tool["name_en"]
    home = "首页" if is_cn else "Home"
    tools = "工具" if is_cn else "Tools"
    cn_a = ' class="active"' if is_cn else ''
    en_a = '' if is_cn else ' class="active"'
    cn_href = "index.html" if is_cn else f"../{slug}/"
    en_href = f"../en/{slug}/" if is_cn else "index.html"
    return f'''<div class="header"><h1>{name}</h1><div class="lang-switch"><a href="{cn_href}"{cn_a}>中文</a><a href="{en_href}"{en_a}>EN</a></div></div>
<p class="nav-back"><a href="{'../' if is_cn else '../'}index.html">{home}</a> &rsaquo; <a href="{'../' if is_cn else '../'}#tools">{tools}</a> &rsaquo; {name}</p>'''


# ============ TOOL BUILDERS ============

def build_random_name(tool, lang):
    is_cn = lang == "zh"
    name = tool["name_zh"] if is_cn else tool["name_en"]
    desc = tool["desc_zh"] if is_cn else tool["desc_en"]
    L = {
        "lang_label": "语言" if is_cn else "Language",
        "gender_label": "性别" if is_cn else "Gender",
        "count_label": "数量" if is_cn else "Count",
        "gen_btn": "🎲 生成姓名" if is_cn else "🎲 Generate Names",
        "copy_all": "📋 一键复制" if is_cn else "📋 Copy All",
        "clear": "🗑 清除" if is_cn else "🗑 Clear",
        "result_title": "🎭 生成结果" if is_cn else "🎭 Results",
        "privacy": "🔒 所有姓名本地生成，使用密码学安全随机数，数据绝不上传服务器。" if is_cn else "🔒 All names generated locally with cryptographically secure randomness. Data never leaves your browser.",
        "chinese": "中文" if is_cn else "Chinese",
        "english": "英文" if is_cn else "English",
        "mixed": "混合" if is_cn else "Mixed",
        "male": "男" if is_cn else "Male",
        "female": "女" if is_cn else "Female",
        "random_g": "随机" if is_cn else "Random",
    }
    badge = "无需注册 · 数据绝不上传" if is_cn else "No registration · Data never uploaded"
    hint = "点击生成按钮开始" if is_cn else "Click generate to start"

    body = f'''<div class="container">
{make_header(tool, lang)}
<div class="hero"><p>{desc} <span class="badge">🔒 {badge}</span></p></div>
<div class="panel">
  <div class="panel-title">⚙️ {L["lang_label"] if is_cn else "Settings"}</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px">
    <div><label>{L["lang_label"]}</label><select id="nameLang"><option value="chinese">{L["chinese"]}</option><option value="english">{L["english"]}</option><option value="mixed">{L["mixed"]}</option></select></div>
    <div><label>{L["gender_label"]}</label><select id="nameGender"><option value="random">{L["random_g"]}</option><option value="male">{L["male"]}</option><option value="female">{L["female"]}</option></select></div>
    <div><label>{L["count_label"]}</label><input type="number" id="nameCount" value="10" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" onclick="generateNames()">{L["gen_btn"]}</button>
    <button class="btn btn-secondary" onclick="copyAll()">{L["copy_all"]}</button>
    <button class="btn btn-secondary" onclick="clearNames()">{L["clear"]}</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">{L["result_title"]} (<span id="resultCount">0</span>)</div>
  <div class="result-area" id="nameResults">{hint}</div>
</div>
<div class="privacy-note">{L["privacy"]}</div>
{make_faq(tool, lang)}
</div>
{make_footer(tool, lang)}
<div class="toast" id="toast"></div>'''

    js = '''<script>function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}</script>
<script>
'use strict';
var cnSurnames="王李张刘陈杨黄赵周吴徐孙马朱胡郭何高林罗郑梁谢宋唐韩曹许邓萧冯曾程蔡彭潘袁于董余苏叶吕魏蒋田杜丁沈姜范江傅钟卢汪戴崔任陆廖姚方金邱夏谭韦贾邹石熊孟秦阎薛侯雷白龙段郝孔邵史毛常万顾赖武康贺严尹钱施牛洪龚".split("");
var cnMaleNames="伟强磊军勇杰涛明超辉鹏浩亮刚健飞毅俊峰宁建文斌博伟华宇然宏志立国林峰海波彬恒祥瑞嘉铭哲翰诚睿晟毅昊然轩宇".split("");
var cnFemaleNames="芳敏静丽艳娟霞秀婷慧洁兰萍红玲燕琳雪怡娜蓉莉莹晶洋妍婉瑶倩佳悦萱琪颖蕾妮薇菲芸欣馨怡嘉梓涵诗雨梦彤".split("");
var enFirstMale="James John Robert Michael William David Richard Joseph Thomas Charles Daniel Matthew Anthony Mark Donald Steven Paul Andrew Joshua Kenneth Kevin Brian George Timothy Ronald Edward Jason Jeffrey Ryan Jacob Gary Nicholas Eric Jonathan Stephen Larry Justin Scott Brandon Benjamin Samuel Raymond Gregory Frank Alexander Patrick Jack Dennis Jerry Tyler Aaron Jose Adam Nathan Henry Douglas Zachary Peter Kyle Walter Ethan Jeremy Harold Keith Christian Roger Noah Gerald Carl Terry Sean Austin Arthur Lawrence Jesse Dylan Bryan Joe Jordan Billy Bruce Albert Willie Gabriel Logan Alan Juan Wayne Roy Ralph Randy Eugene Vincent Russell Elijah Louis Bobby Philip Johnny".split(" ");
var enFirstFemale="Mary Patricia Jennifer Linda Barbara Elizabeth Susan Jessica Sarah Karen Lisa Nancy Betty Margaret Sandra Ashley Dorothy Kimberly Emily Donna Michelle Carol Amanda Melissa Deborah Stephanie Rebecca Sharon Laura Cynthia Kathleen Amy Angela Shirley Anna Brenda Pamela Emma Nicole Helen Samantha Katherine Christine Debra Rachel Carolyn Janet Catherine Maria Heather Diane Ruth Julie Olivia Joyce Virginia Victoria Kelly Lauren Christina Joan Evelyn Judith Megan Andrea Cheryl Hannah Jacqueline Martha Gloria Teresa Ann Sara Madison Frances Kathryn Janice Jean Abigail Alice Judy Sophia Grace Denise Amber Doris Marilyn Danielle Beverly Isabella Theresa Diana Natalie Julie Julia Rose".split(" ");
var enSurnames="Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez Martinez Hernandez Lopez Gonzalez Wilson Anderson Thomas Taylor Moore Jackson Martin Lee Perez Thompson White Harris Sanchez Clark Ramirez Lewis Robinson Walker Young Allen King Wright Scott Torres Nguyen Hill Flores Green Adams Nelson Baker Hall Rivera Campbell Mitchell Carter Roberts Gomez Phillips Evans Turner Diaz Parker Cruz Edwards Collins Reyes Stewart Morris Morales Murphy Cook Rogers Gutierrez Ortiz Morgan Cooper Peterson Bailey Reed Kelly Howard Ramos Kim Cox Ward Richardson Watson Brooks Chavez Wood James Bennett Gray Mendoza Ruiz Hughes Price Alvarez Castillo Sanders Patel Myers Long Ross Foster".split(" ");
var allNames=[];

function pick(arr){return arr[Math.floor(Math.random()*arr.length)]}
function cnName(gender){
  var s=pick(cnSurnames),g;
  if(gender==="male")g=pick(cnMaleNames);
  else if(gender==="female")g=pick(cnFemaleNames);
  else g=pick(Math.random()<0.5?cnMaleNames:cnFemaleNames);
  return s+g
}
function enName(gender){
  var first;
  if(gender==="male")first=pick(enFirstMale);
  else if(gender==="female")first=pick(enFirstFemale);
  else first=pick(Math.random()<0.5?enFirstMale:enFirstFemale);
  return first+" "+pick(enSurnames)
}
function generateNames(){
  var lang=document.getElementById("nameLang").value;
  var gender=document.getElementById("nameGender").value;
  var count=parseInt(document.getElementById("nameCount").value)||10;
  if(count<1)count=1;if(count>100)count=100;
  allNames=[];
  for(var i=0;i<count;i++){
    var l=lang==="mixed"?(Math.random()<0.5?"chinese":"english"):lang;
    allNames.push(l==="chinese"?cnName(gender):enName(gender))
  }
  renderNames()
}
function renderNames(){
  var el=document.getElementById("nameResults");
  document.getElementById("resultCount").textContent=allNames.length;
  if(allNames.length===0){el.textContent='CLICK_HINT';return}
  el.innerHTML=allNames.map(function(n,i){return '<span style="display:inline-block;background:#EEF2FF;color:#4F46E5;padding:6px 14px;border-radius:20px;margin:4px;font-size:.9rem;cursor:pointer" onclick="copyOne('+i+')" title="Click to copy">'+n+'</span>'}).join("")
}
function copyOne(i){navigator.clipboard.writeText(allNames[i]).then(function(){showToast("COPIED: "+allNames[i])})}
function copyAll(){if(allNames.length===0){showToast("EMPTY");return}navigator.clipboard.writeText(allNames.join("\\n")).then(function(){showToast("COPIED_N "+allNames.length)})}
function clearNames(){allNames=[];renderNames();showToast("CLEARED")}
window.generateNames=generateNames;window.copyAll=copyAll;window.clearNames=clearNames;window.copyOne=copyOne;
'''.replace("CLICK_HINT", hint).replace("COPIED: ", "已复制: " if is_cn else "Copied: ").replace("EMPTY", "请先生成姓名" if is_cn else "Please generate names first").replace("COPIED_N ", "已复制 " if is_cn else "Copied ").replace("个姓名" if is_cn else " names", "个姓名" if is_cn else " names").replace("CLEARED", "已清除" if is_cn else "Cleared")

    js += """</script>
<script>/* reserved */</script>"""
    return js, body, CSS_LIGHT


def build_color_contrast(tool, lang):
    is_cn = lang == "zh"
    name = tool["name_zh"] if is_cn else tool["name_en"]
    desc = tool["desc_zh"] if is_cn else tool["desc_en"]
    badge = "无需注册 · 数据绝不上传" if is_cn else "No registration · Data never uploaded"
    L = {
        "fg_label": "前景色" if is_cn else "Foreground Color",
        "bg_label": "背景色" if is_cn else "Background Color",
        "check_btn": "🎨 检查对比度" if is_cn else "🎨 Check Contrast",
        "swap_btn": "🔄 交换颜色" if is_cn else "🔄 Swap Colors",
        "ratio": "对比度" if is_cn else "Contrast Ratio",
        "normal_text": "普通文本" if is_cn else "Normal Text",
        "large_text": "大文本" if is_cn else "Large Text",
        "preview": "🎯 预览" if is_cn else "🎯 Preview",
        "privacy": "🔒 颜色计算完全在浏览器本地执行，数据绝不上传服务器。" if is_cn else "🔒 Color calculations run entirely in your browser. Data never leaves your device.",
    }
    body = f'''<div class="container">
{make_header(tool, lang)}
<div class="hero"><p>{desc} <span class="badge">🔒 {badge}</span></p></div>
<div class="panel">
  <div class="panel-title">⚙️ {"颜色设置" if is_cn else "Color Settings"}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
    <div><label>{L["fg_label"]}</label><div style="display:flex;gap:8px"><input type="text" id="fgInput" value="#4F46E5" oninput="checkContrast()"><input type="color" id="fgPicker" value="#4F46E5" oninput="syncColor('fg')" style="width:50px;padding:4px;flex:none"></div></div>
    <div><label>{L["bg_label"]}</label><div style="display:flex;gap:8px"><input type="text" id="bgInput" value="#ffffff" oninput="checkContrast()"><input type="color" id="bgPicker" value="#ffffff" oninput="syncColor('bg')" style="width:50px;padding:4px;flex:none"></div></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" onclick="checkContrast()">{L["check_btn"]}</button>
    <button class="btn btn-secondary" onclick="swapColors()">{L["swap_btn"]}</button>
  </div>
</div>
<div class="panel" id="resultPanel" style="display:none">
  <div class="panel-title">📊 {"检测结果" if is_cn else "Result"}</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
    <div class="stat-box"><div style="color:#64748b;font-size:.75rem;margin-bottom:4px">{L["ratio"]}</div><div style="font-size:2rem;font-weight:800" id="ratioVal">-</div></div>
    <div class="stat-box"><div style="color:#64748b;font-size:.75rem;margin-bottom:4px">{L["normal_text"]} (AA)</div><div style="font-weight:700;font-size:1.1rem" id="normalAA">-</div></div>
    <div class="stat-box"><div style="color:#64748b;font-size:.75rem;margin-bottom:4px">{L["large_text"]} (AA)</div><div style="font-weight:700;font-size:1.1rem" id="largeAA">-</div></div>
    <div class="stat-box"><div style="color:#64748b;font-size:.75rem;margin-bottom:4px">{L["normal_text"]} (AAA)</div><div style="font-weight:700;font-size:1.1rem" id="normalAAA">-</div></div>
  </div>
</div>
<div class="panel">
  <div class="panel-title">{L["preview"]}</div>
  <div id="previewBox" style="padding:20px;border-radius:12px;text-align:center;min-height:120px;display:flex;align-items:center;justify-content:center">
    <div>
      <div style="font-size:1.5rem;font-weight:700" id="previewLarge">{L["large_text"]}</div>
      <div style="font-size:.9rem;margin-top:8px" id="previewNormal">{L["normal_text"]}: The quick brown fox jumps over the lazy dog.</div>
    </div>
  </div>
</div>
<div class="privacy-note">{L["privacy"]}</div>
{make_faq(tool, lang)}
</div>
{make_footer(tool, lang)}
<div class="toast" id="toast"></div>'''

    js = '''<script>function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}</script>
<script>
'use strict';
function parseColor(s){
  s=s.trim();
  if(s[0]==="#"){s=s.slice(1);if(s.length===3)s=s[0]+s[0]+s[1]+s[1]+s[2]+s[2];return[parseInt(s.slice(0,2),16),parseInt(s.slice(2,4),16),parseInt(s.slice(4,6),16)]}
  var m=s.match(/rgb\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)/i);
  if(m)return[parseInt(m[1]),parseInt(m[2]),parseInt(m[3])];
  var names={red:[255,0,0],blue:[0,0,255],green:[0,128,0],black:[0,0,0],white:[255,255,255],gray:[128,128,128],grey:[128,128,128],yellow:[255,255,0],orange:[255,165,0],purple:[128,0,128],pink:[255,192,203],cyan:[0,255,255],magenta:[255,0,255],lime:[0,255,0],navy:[0,0,128],teal:[0,128,128],maroon:[128,0,0],olive:[128,128,0],silver:[192,192,192]};
  if(names[s.toLowerCase()])return names[s.toLowerCase()];
  return null
}
function relativeL(rgb){var r=rgb[0]/255,g=rgb[1]/255,b=rgb[2]/255;r=r<=0.03928?r/12.92:Math.pow((r+0.055)/1.055,2.4);g=g<=0.03928?g/12.92:Math.pow((g+0.055)/1.055,2.4);b=b<=0.03928?b/12.92:Math.pow((b+0.055)/1.055,2.4);return 0.2126*r+0.7152*g+0.0722*b}
function contrast(a,b){var l1=relativeL(a),l2=relativeL(b);var lighter=Math.max(l1,l2),darker=Math.min(l1,l2);return (lighter+0.05)/(darker+0.05)}
function syncColor(which){var i=document.getElementById(which+"Input"),p=document.getElementById(which+"Picker");i.value=p.value;checkContrast()}
function checkContrast(){
  var fg=parseColor(document.getElementById("fgInput").value),bg=parseColor(document.getElementById("bgInput").value);
  if(!fg||!bg){showToast("Invalid color format");return}
  var fh=fg[0].toString(16).padStart(2,"0")+fg[1].toString(16).padStart(2,"0")+fg[2].toString(16).padStart(2,"0");
  var bh=bg[0].toString(16).padStart(2,"0")+bg[1].toString(16).padStart(2,"0")+bg[2].toString(16).padStart(2,"0");
  document.getElementById("fgPicker").value="#"+fh;document.getElementById("bgPicker").value="#"+bh;
  var c=contrast(fg,bg);
  document.getElementById("ratioVal").textContent=c.toFixed(2);
  document.getElementById("normalAA").innerHTML=c>=4.5?"\\u2705 Pass":"\\u274c Fail";
  document.getElementById("largeAA").innerHTML=c>=3?"\\u2705 Pass":"\\u274c Fail";
  document.getElementById("normalAAA").innerHTML=c>=7?"\\u2705 Pass":"\\u274c Fail";
  document.getElementById("resultPanel").style.display="block";
  document.getElementById("previewBox").style.background="#"+bh;
  document.getElementById("previewBox").style.color="#"+fh
}
function swapColors(){var f=document.getElementById("fgInput").value,b=document.getElementById("bgInput").value;document.getElementById("fgInput").value=b;document.getElementById("bgInput").value=f;checkContrast()}
window.checkContrast=checkContrast;window.swapColors=swapColors;window.syncColor=syncColor;
checkContrast();
</script>
<script>/* reserved */</script>'''
    return js, body, CSS_LIGHT


def build_wheel_spin(tool, lang):
    is_cn = lang == "zh"
    name = tool["name_zh"] if is_cn else tool["name_en"]
    desc = tool["desc_zh"] if is_cn else tool["desc_en"]
    badge = "无需注册 · 数据绝不上传" if is_cn else "No registration · Data never uploaded"
    L = {
        "options_label": "输入选项（每行一个）" if is_cn else "Enter Options (one per line)",
        "spin_btn": "🎡 转动！" if is_cn else "🎡 Spin!",
        "reset_btn": "🔄 重置转盘" if is_cn else "🔄 Reset",
        "save_btn": "💾 保存配置" if is_cn else "💾 Save",
        "load_btn": "📂 加载配置" if is_cn else "📂 Load",
        "result_title": "🎯 抽奖结果" if is_cn else "🎯 Result",
        "history_title": "📜 历史记录" if is_cn else "📜 History",
        "clear_hist": "🗑 清除历史" if is_cn else "🗑 Clear History",
        "privacy": "🔒 所有抽取在浏览器本地完成，使用密码学安全随机数。数据绝不上传服务器。" if is_cn else "🔒 All spins run locally with cryptographically secure randomness. Data never leaves your browser.",
    }
    placeholder = "每行输入一个选项，例如：\n一等奖\n二等奖\n三等奖\n参与奖" if is_cn else "Enter one option per line, e.g.:\nFirst Prize\nSecond Prize\nThird Prize\nParticipation"
    default_val = "一等奖\n二等奖\n三等奖\n四等奖\n参与奖" if is_cn else "First Prize\nSecond Prize\nThird Prize\nFourth Prize\nParticipation"

    body = f'''<div class="container">
{make_header(tool, lang)}
<div class="hero"><p>{desc} <span class="badge">🔒 {badge}</span></p></div>
<div class="panel">
  <div class="panel-title">⚙️ {"转盘设置" if is_cn else "Wheel Settings"}</div>
  <textarea id="wheelOptions" rows="6" placeholder="{placeholder}">{default_val}</textarea>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" onclick="spinWheel()">{L["spin_btn"]}</button>
    <button class="btn btn-secondary" onclick="resetWheel()">{L["reset_btn"]}</button>
    <button class="btn btn-secondary" onclick="saveConfig()">{L["save_btn"]}</button>
    <button class="btn btn-secondary" onclick="loadConfig()">{L["load_btn"]}</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title" id="resultTitle">{L["result_title"]}</div>
  <div style="text-align:center">
    <canvas id="wheelCanvas" width="400" height="400" style="max-width:100%;height:auto;border-radius:50%"></canvas>
    <div id="spinResult" style="font-size:1.3rem;font-weight:700;margin-top:12px;color:var(--primary)"></div>
  </div>
</div>
<div class="panel" id="historyPanel" style="display:none">
  <div class="panel-title">{L["history_title"]} (<span id="histCount">0</span>)</div>
  <div class="result-area" id="histList" style="max-height:200px"></div>
  <div class="btn-row"><button class="btn btn-secondary" onclick="clearHistory()">{L["clear_hist"]}</button></div>
</div>
<div class="privacy-note">{L["privacy"]}</div>
{make_faq(tool, lang)}
</div>
{make_footer(tool, lang)}
<div class="toast" id="toast"></div>
<input type="file" id="configLoader" style="display:none" accept=".json" onchange="handleConfigLoad(event)">'''

    js = '''<script>function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}</script>
<script>
'use strict';
var colors=["#ef4444","#f59e0b","#10b981","#3b82f6","#8b5cf6","#ec4899","#06b6d4","#f97316","#84cc16","#6366f1","#e11d48","#14b8a6","#d946ef","#0ea5e9","#f43f5e"];
var history=[],spinning=false,currentAngle=0;
function getOptions(){return document.getElementById("wheelOptions").value.split("\\n").filter(function(l){return l.trim()}).map(function(l){return l.trim()})}
function drawWheel(highlightIdx){
  var canvas=document.getElementById("wheelCanvas"),ctx=canvas.getContext("2d");
  var opts=getOptions(),n=opts.length,cx=200,cy=200,r=180;
  ctx.clearRect(0,0,400,400);
  if(n===0){ctx.fillStyle="#94a3b8";ctx.font="16px sans-serif";ctx.textAlign="center";ctx.fillText("No options",200,200);return}
  var slice=2*Math.PI/n;
  for(var i=0;i<n;i++){
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,i*slice+currentAngle,(i+1)*slice+currentAngle);ctx.closePath();
    ctx.fillStyle=highlightIdx===i?"#fbbf24":colors[i%colors.length];
    ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=2;ctx.stroke();
    ctx.save();ctx.translate(cx,cy);ctx.rotate(i*slice+slice/2+currentAngle);
    ctx.fillStyle="#fff";ctx.font="bold 14px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
    var txt=opts[i];if(txt.length>10)txt=txt.slice(0,9)+"…";
    ctx.fillText(txt,r*0.65,0);ctx.restore()
  }
  ctx.beginPath();ctx.moveTo(cx,cy-190);ctx.lineTo(cx-12,cy-210);ctx.lineTo(cx+12,cy-210);ctx.closePath();
  ctx.fillStyle="#1e293b";ctx.fill();ctx.strokeStyle="#fff";ctx.lineWidth=2;ctx.stroke()
}
function spinWheel(){
  if(spinning){showToast("SPINNING");return}
  var opts=getOptions();if(opts.length<2){showToast("NEED_MORE");return}
  spinning=true;
  var targetSlice=Math.floor(Math.random()*opts.length);
  var sliceAngle=2*Math.PI/opts.length;
  var targetAngle=2*Math.PI*(5+Math.floor(Math.random()*5))+targetSlice*sliceAngle+sliceAngle/2;
  var startAngle=currentAngle,startTime=Date.now(),duration=3000;
  function anim(){
    var elapsed=Date.now()-startTime,progress=Math.min(elapsed/duration,1);
    var eased=1-Math.pow(1-progress,3);
    currentAngle=startAngle+(targetAngle-startAngle)*eased;
    drawWheel(-1);
    if(progress<1)requestAnimationFrame(anim);
    else{
      spinning=false;currentAngle=currentAngle%(2*Math.PI);
      document.getElementById("spinResult").textContent="🎉 "+opts[targetSlice];
      history.unshift({option:opts[targetSlice],time:new Date().toLocaleTimeString()});
      if(history.length>100)history.pop();
      renderHistory();drawWheel(targetSlice)
    }
  }
  anim()
}
function resetWheel(){currentAngle=0;document.getElementById("spinResult").textContent="";drawWheel(-1)}
function renderHistory(){
  var el=document.getElementById("histList"),panel=document.getElementById("historyPanel");
  document.getElementById("histCount").textContent=history.length;
  if(history.length===0){panel.style.display="none";return}
  panel.style.display="block";
  el.innerHTML=history.map(function(h,i){return '<div style="padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--text-secondary);font-size:.8rem">'+(i+1)+'. '+h.time+'</span> <span style="font-weight:600">'+h.option+'</span></div>'}).join("")
}
function clearHistory(){history=[];renderHistory();showToast("HIST_CLEARED")}
function saveConfig(){var data=JSON.stringify({options:getOptions()},null,2);var blob=new Blob([data],{type:"application/json"});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="wheel-config.json";a.click();showToast("SAVED")}
function loadConfig(){document.getElementById("configLoader").click()}
function handleConfigLoad(e){
  var file=e.target.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){
    try{var cfg=JSON.parse(ev.target.result);
      if(cfg.options&&Array.isArray(cfg.options)){document.getElementById("wheelOptions").value=cfg.options.join("\\n");resetWheel();drawWheel(-1);showToast("LOADED")}
      else showToast("INVALID_CFG")
    }catch(ex){showToast("INVALID_JSON")}
  };
  reader.readAsText(file)
}
window.spinWheel=spinWheel;window.resetWheel=resetWheel;window.saveConfig=saveConfig;window.loadConfig=loadConfig;window.handleConfigLoad=handleConfigLoad;window.clearHistory=clearHistory;
drawWheel(-1);
</script>
<script>/* reserved */</script>'''

    # Localize toast messages
    if is_cn:
        js = js.replace('"SPINNING"', '"正在转动中..."')
        js = js.replace('"NEED_MORE"', '"至少需要2个选项"')
        js = js.replace('"HIST_CLEARED"', '"历史已清除"')
        js = js.replace('"SAVED"', '"配置已保存"')
        js = js.replace('"LOADED"', '"配置已加载"')
        js = js.replace('"INVALID_CFG"', '"无效配置格式"')
        js = js.replace('"INVALID_JSON"', '"无效JSON文件"')
        js = js.replace('"No options"', '"无选项"')
    else:
        js = js.replace('"SPINNING"', '"Already spinning!"')
        js = js.replace('"NEED_MORE"', '"Need at least 2 options"')
        js = js.replace('"HIST_CLEARED"', '"History cleared"')
        js = js.replace('"SAVED"', '"Config saved!"')
        js = js.replace('"LOADED"', '"Config loaded!"')
        js = js.replace('"INVALID_CFG"', '"Invalid config format"')
        js = js.replace('"INVALID_JSON"', '"Invalid JSON file"')
    return js, body, CSS_LIGHT


def build_xml_sitemap(tool, lang):
    is_cn = lang == "zh"
    name = tool["name_zh"] if is_cn else tool["name_en"]
    desc = tool["desc_zh"] if is_cn else tool["desc_en"]
    badge = "无需注册 · 数据绝不上传" if is_cn else "No registration · Data never uploaded"
    L = {
        "urls_label": "输入URL（每行一个）" if is_cn else "Enter URLs (one per line)",
        "freq_label": "更新频率" if is_cn else "Change Frequency",
        "priority_label": "默认优先级" if is_cn else "Default Priority",
        "gen_btn": "📄 生成 Sitemap" if is_cn else "📄 Generate Sitemap",
        "copy_btn": "📋 复制 XML" if is_cn else "📋 Copy XML",
        "download_btn": "💾 下载 .xml" if is_cn else "💾 Download .xml",
        "output_title": "📄 生成的 sitemap.xml" if is_cn else "📄 Generated sitemap.xml",
        "url_count": "URL数量" if is_cn else "URL Count",
        "privacy": "🔒 所有处理在浏览器本地完成，数据绝不上传服务器。" if is_cn else "🔒 All processing is local. Data never leaves your browser.",
    }
    hint = "输入URL后点击生成按钮" if is_cn else "Enter URLs and click generate"
    placeholder = "https://example.com/\nhttps://example.com/about\nhttps://example.com/contact"

    body = f'''<div class="container">
{make_header(tool, lang)}
<div class="hero"><p>{desc} <span class="badge">🔒 {badge}</span></p></div>
<div class="panel">
  <div class="panel-title">⚙️ {"Sitemap 设置" if is_cn else "Sitemap Settings"}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:12px">
    <div><label>{L["freq_label"]}</label><select id="changefreq"><option value="monthly">monthly</option><option value="weekly">weekly</option><option value="daily">daily</option><option value="always">always</option><option value="hourly">hourly</option><option value="yearly">yearly</option><option value="never">never</option></select></div>
    <div><label>{L["priority_label"]}</label><select id="sitemapPriority"><option value="0.8">0.8</option><option value="1.0">1.0</option><option value="0.5">0.5</option><option value="0.3">0.3</option><option value="0.1">0.1</option></select></div>
  </div>
  <label>{L["urls_label"]}</label>
  <textarea id="sitemapUrls" rows="10" placeholder="{placeholder}"></textarea>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" onclick="generateSitemap()">{L["gen_btn"]}</button>
    <button class="btn btn-secondary" onclick="copySitemap()">{L["copy_btn"]}</button>
    <button class="btn btn-secondary" onclick="downloadSitemap()">{L["download_btn"]}</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">{L["output_title"]} (<span id="urlCount">0</span> {L["url_count"]})</div>
  <div class="result-area" id="sitemapOutput" style="max-height:400px;font-size:.8rem">{hint}</div>
</div>
<div class="privacy-note">{L["privacy"]}</div>
{make_faq(tool, lang)}
</div>
{make_footer(tool, lang)}
<div class="toast" id="toast"></div>'''

    js = '''<script>function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}</script>
<script>
'use strict';
var generatedXml="";
function escapeXml(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&apos;")}
function generateSitemap(){
  var raw=document.getElementById("sitemapUrls").value;
  var urls=raw.split("\\n").filter(function(l){return l.trim()}).map(function(l){return l.trim()});
  if(urls.length===0){showToast("EMPTY");return}
  if(urls.length>500){showToast("MAX");return}
  var freq=document.getElementById("changefreq").value;
  var pri=document.getElementById("sitemapPriority").value;
  var today=new Date().toISOString().slice(0,10);
  var xml='<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
  for(var i=0;i<urls.length;i++){xml+='\\n  <url>\\n    <loc>'+escapeXml(urls[i])+'</loc>\\n    <lastmod>'+today+'</lastmod>\\n    <changefreq>'+freq+'</changefreq>\\n    <priority>'+pri+'</priority>\\n  </url>'}
  xml+='\\n</urlset>';
  generatedXml=xml;
  document.getElementById("sitemapOutput").textContent=xml;
  document.getElementById("urlCount").textContent=urls.length
}
function copySitemap(){if(!generatedXml){showToast("GEN_FIRST");return}navigator.clipboard.writeText(generatedXml).then(function(){showToast("COPIED")})}
function downloadSitemap(){if(!generatedXml){showToast("GEN_FIRST");return}var blob=new Blob([generatedXml],{type:"application/xml"});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="sitemap.xml";a.click();showToast("DOWNLOADED")}
window.generateSitemap=generateSitemap;window.copySitemap=copySitemap;window.downloadSitemap=downloadSitemap;
</script>
<script>/* reserved */</script>'''

    if is_cn:
        js = js.replace('"EMPTY"', '"请输入URL"')
        js = js.replace('"MAX"', '"最多支持500个URL"')
        js = js.replace('"GEN_FIRST"', '"请先生成sitemap"')
        js = js.replace('"COPIED"', '"已复制!"')
        js = js.replace('"DOWNLOADED"', '"下载完成!"')
    else:
        js = js.replace('"EMPTY"', '"Please enter URLs"')
        js = js.replace('"MAX"', '"Max 500 URLs"')
        js = js.replace('"GEN_FIRST"', '"Generate sitemap first"')
        js = js.replace('"COPIED"', '"Copied!"')
        js = js.replace('"DOWNLOADED"', '"Downloaded!"')
    return js, body, CSS_LIGHT


def build_pixel_art(tool, lang):
    is_cn = lang == "zh"
    name = tool["name_zh"] if is_cn else tool["name_en"]
    desc = tool["desc_zh"] if is_cn else tool["desc_en"]
    badge = "无需注册 · 数据绝不上传" if is_cn else "No registration · Data never uploaded"
    L = {
        "size_label": "画布尺寸" if is_cn else "Canvas Size",
        "draw_btn": "🖌 画笔" if is_cn else "🖌 Brush",
        "eraser_btn": "🧹 橡皮" if is_cn else "🧹 Eraser",
        "picker_btn": "💉 取色" if is_cn else "💉 Pick",
        "undo_btn": "↩ 撤销" if is_cn else "↩ Undo",
        "clear_btn": "🗑 清除" if is_cn else "🗑 Clear",
        "export_btn": "📥 导出PNG" if is_cn else "📥 Export PNG",
        "copy_btn": "📋 复制DataURL" if is_cn else "📋 Copy Data URL",
        "preview_title": "🖼️ 预览" if is_cn else "🖼️ Preview",
        "privacy": "🔒 像素画完全在浏览器本地绘制，数据绝不上传服务器。" if is_cn else "🔒 Pixel art drawn entirely in your browser. Data never leaves your device.",
    }
    body = f'''<div class="container">
{make_header(tool, lang)}
<div class="hero"><p>{desc} <span class="badge">🔒 {badge}</span></p></div>
<div class="panel">
  <div class="panel-title">⚙️ {"编辑器设置" if is_cn else "Editor Settings"}</div>
  <div style="display:flex;gap:10px;align-items:end;flex-wrap:wrap">
    <div style="flex:0 0 100px;min-width:80px"><label>{L["size_label"]}</label><select id="canvasSize" onchange="resizeCanvas()"><option value="8">8x8</option><option value="16" selected>16x16</option><option value="32">32x32</option><option value="64">64x64</option></select></div>
    <div style="flex:0 0 60px;min-width:50px"><input type="color" id="currentColor" value="#4F46E5" style="height:40px;padding:2px;cursor:pointer;width:50px"></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:0">
      <button class="btn btn-primary" id="brushBtn" onclick="setTool('brush')">{L["draw_btn"]}</button>
      <button class="btn btn-secondary" id="eraserBtn" onclick="setTool('eraser')">{L["eraser_btn"]}</button>
      <button class="btn btn-secondary" id="pickerBtn" onclick="setTool('picker')">{L["picker_btn"]}</button>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="undo()">{L["undo_btn"]}</button>
    <button class="btn btn-secondary" onclick="clearCanvas()">{L["clear_btn"]}</button>
    <button class="btn btn-primary" onclick="exportPNG()">{L["export_btn"]}</button>
    <button class="btn btn-secondary" onclick="copyDataURL()">{L["copy_btn"]}</button>
  </div>
</div>
<div style="display:grid;grid-template-columns:1fr auto;gap:16px;align-items:start">
<div class="panel" style="text-align:center">
  <canvas id="pixelCanvas" style="border:1px solid var(--border);image-rendering:pixelated;max-width:100%;height:auto;cursor:crosshair"></canvas>
</div>
<div class="panel">
  <div class="panel-title">{L["preview_title"]}</div>
  <canvas id="previewCanvas" style="border:1px solid var(--border);image-rendering:pixelated;width:150px;height:150px"></canvas>
</div></div>
<div class="privacy-note">{L["privacy"]}</div>
{make_faq(tool, lang)}
</div>
{make_footer(tool, lang)}
<div class="toast" id="toast"></div>'''

    js = '''<script>function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}</script>
<script>
'use strict';
var size=16,tool="brush",history=[],grid=[];
function initGrid(s){size=s;grid=[];history=[];for(var y=0;y<size;y++){grid[y]=[];for(var x=0;x<size;x++){grid[y][x]=""}}renderGrid()}
function renderGrid(){
  var c=document.getElementById("pixelCanvas"),ctx=c.getContext("2d");
  var cellSize=Math.floor(380/size);c.width=cellSize*size;c.height=cellSize*size;
  ctx.clearRect(0,0,c.width,c.height);
  for(var y=0;y<size;y++){for(var x=0;x<size;x++){
    ctx.fillStyle=grid[y][x]||"#ffffff";ctx.fillRect(x*cellSize,y*cellSize,cellSize,cellSize);
    ctx.strokeStyle="#e2e8f0";ctx.lineWidth=0.5;ctx.strokeRect(x*cellSize,y*cellSize,cellSize,cellSize)
  }}
  updatePreview()
}
function updatePreview(){
  var c=document.getElementById("previewCanvas"),ctx=c.getContext("2d");
  c.width=size;c.height=size;
  for(var y=0;y<size;y++){for(var x=0;x<size;x++){ctx.fillStyle=grid[y][x]||"rgba(0,0,0,0)";ctx.fillRect(x,y,1,1)}}
}
function getCell(e){
  var c=document.getElementById("pixelCanvas"),rect=c.getBoundingClientRect();
  var cellSize=c.width/size;
  return{valid:true,x:Math.floor((e.clientX-rect.left)/cellSize),y:Math.floor((e.clientY-rect.top)/cellSize)}
}
function saveState(){history.push(JSON.stringify(grid));if(history.length>50)history.shift()}
function undo(){if(history.length===0){showToast("UNDO_EMPTY");return}grid=JSON.parse(history.pop());renderGrid()}
function setTool(t){tool=t;
  document.getElementById("brushBtn").className="btn "+(t==="brush"?"btn-primary":"btn-secondary");
  document.getElementById("eraserBtn").className="btn "+(t==="eraser"?"btn-primary":"btn-secondary");
  document.getElementById("pickerBtn").className="btn "+(t==="picker"?"btn-primary":"btn-secondary")}
function clearCanvas(){saveState();initGrid(size);renderGrid()}

document.getElementById("pixelCanvas").addEventListener("mousedown",function(e){
  var cell=getCell(e);if(cell.x<0||cell.x>=size||cell.y<0||cell.y>=size)return;
  if(tool==="brush"){saveState();grid[cell.y][cell.x]=document.getElementById("currentColor").value;renderGrid()}
  else if(tool==="eraser"){saveState();grid[cell.y][cell.x]="";renderGrid()}
  else if(tool==="picker"){var col=grid[cell.y][cell.x];if(col){document.getElementById("currentColor").value=col;setTool("brush")}}
});
document.getElementById("pixelCanvas").addEventListener("mousemove",function(e){
  if(e.buttons!==1)return;
  var cell=getCell(e);if(cell.x<0||cell.x>=size||cell.y<0||cell.y>=size)return;
  if(tool==="brush")grid[cell.y][cell.x]=document.getElementById("currentColor").value;
  else if(tool==="eraser")grid[cell.y][cell.x]="";
  renderGrid()
});
function resizeCanvas(){var s=parseInt(document.getElementById("canvasSize").value);initGrid(s)}
function exportPNG(){
  var c=document.createElement("canvas");c.width=size;c.height=size;var ctx=c.getContext("2d");
  for(var y=0;y<size;y++){for(var x=0;x<size;x++){if(grid[y][x]){ctx.fillStyle=grid[y][x];ctx.fillRect(x,y,1,1)}}}
  var link=document.createElement("a");link.download="pixel-art.png";link.href=c.toDataURL();link.click();showToast("EXPORTED")
}
function copyDataURL(){
  var c=document.createElement("canvas");c.width=size;c.height=size;var ctx=c.getContext("2d");
  for(var y=0;y<size;y++){for(var x=0;x<size;x++){if(grid[y][x]){ctx.fillStyle=grid[y][x];ctx.fillRect(x,y,1,1)}}}
  navigator.clipboard.writeText(c.toDataURL()).then(function(){showToast("URL_COPIED")})
}
window.setTool=setTool;window.undo=undo;window.clearCanvas=clearCanvas;window.resizeCanvas=resizeCanvas;window.exportPNG=exportPNG;window.copyDataURL=copyDataURL;
initGrid(16);
</script>
<script>/* reserved */</script>'''

    if is_cn:
        js = js.replace('"UNDO_EMPTY"', '"没有可撤销的操作"')
        js = js.replace('"EXPORTED"', '"已导出PNG!"')
        js = js.replace('"URL_COPIED"', '"Data URL已复制!"')
    else:
        js = js.replace('"UNDO_EMPTY"', '"Nothing to undo"')
        js = js.replace('"EXPORTED"', '"PNG exported!"')
        js = js.replace('"URL_COPIED"', '"Data URL copied!"')
    return js, body, CSS_DARK


# === TOOL DEFINITIONS ===
tools_data = [
    {
        "slug": "random-name",
        "name_zh": "随机姓名生成器",
        "name_en": "Random Name Generator",
        "desc_zh": "免费在线随机姓名生成器，支持中英文姓名，批量生成、性别筛选。适合游戏角色命名、笔名创作、测试数据填充。零数据上传，隐私安全。",
        "desc_en": "Free online random name generator with Chinese & English name support. Batch generation, gender filtering. Ideal for character naming, pen names, test data. Zero data upload, privacy safe.",
        "kw_zh": "随机姓名,名称生成器,中文姓名,英文姓名,角色命名,笔名,在线工具",
        "kw_en": "random name,name generator,Chinese name,English name,character naming,pen name,online tool",
        "meta_title_zh": "随机姓名生成器 - 中文英文姓名|批量生成|免费在线工具",
        "meta_title_en": "Random Name Generator - Chinese & English Names | Batch Generation | Free Online Tool",
        "og_title_zh": "🎭 随机姓名生成器",
        "og_title_en": "🎭 Random Name Generator",
        "faq_zh": [
            ("生成的姓名是真实的吗？","姓名通过算法组合常见姓氏和名字，并非真实人物。可用于游戏角色、测试数据、创作素材等场景。"),
            ("支持哪些语言的姓名？","支持中文姓名（百家姓+常见名）和英文姓名（常见first name + last name），可单独选择或混合生成。"),
            ("可以批量生成多少姓名？","每次可生成1-100个姓名，一键复制全部或单独复制。支持性别筛选（男/女/随机），适合批量测试数据填充。"),
        ],
        "faq_en": [
            ("Are the generated names real?","Names are algorithmically composed from common surnames and given names. They are not real people. Suitable for game characters, test data, creative writing."),
            ("What languages are supported?","Supports Chinese names (100 surnames + common given names) and English names (common first name + last name). Can be selected individually or mixed."),
            ("How many names can I generate?","Generate 1-100 names per batch, copy all or individually. Gender filtering (male/female/random) supported. Great for batch test data."),
        ],
        "howto_zh": [("选择语言","选择中文/英文/混合"), ("设置参数","选择性别和数量"), ("点击生成","一键生成随机姓名")],
        "howto_en": [("Select language","Choose Chinese/English/Mixed"), ("Set parameters","Choose gender and quantity"), ("Click generate","Generate random names")],
        "builder": build_random_name,
    },
    {
        "slug": "color-contrast",
        "name_zh": "颜色对比度检查器",
        "name_en": "Color Contrast Checker",
        "desc_zh": "免费在线WCAG颜色对比度检查器，计算前景色与背景色对比度，自动判断AA/AAA级合规。支持HEX/RGB/HSL输入，实时预览。前端无障碍检测必备。",
        "desc_en": "Free online WCAG color contrast checker. Calculates foreground-background contrast ratio, auto-judges AA/AAA compliance. Supports HEX/RGB/HSL input, real-time preview. Essential for web accessibility.",
        "kw_zh": "颜色对比度,WCAG,无障碍,AA标准,AAA标准,对比度检查,HEX转对比度,在线工具",
        "kw_en": "color contrast,WCAG,accessibility,AA standard,AAA standard,contrast checker,HEX contrast,online tool",
        "meta_title_zh": "颜色对比度检查器 - WCAG AA/AAA合规|实时计算|免费在线工具",
        "meta_title_en": "Color Contrast Checker - WCAG AA/AAA Compliance | Real-time | Free Online Tool",
        "og_title_zh": "🎨 颜色对比度检查器",
        "og_title_en": "🎨 Color Contrast Checker",
        "faq_zh": [
            ("WCAG AA和AAA有什么区别？","AA级要求普通文本对比度≥4.5:1、大文本≥3:1；AAA级要求普通文本≥7:1、大文本≥4.5:1。大多数网站满足AA即可。"),
            ("支持哪些颜色格式？","支持HEX（#FF0000）、RGB（255,0,0）、HSL（0,100%,50%）三种格式自动识别，以及常见颜色名称（red、blue等）。"),
            ("大文本的定义是什么？","WCAG定义大文本为≥18pt或≥14pt加粗的文本。满足大文本对比度要求更容易达到合规标准。"),
        ],
        "faq_en": [
            ("What's the difference between AA and AAA?","AA requires normal text contrast ≥4.5:1 and large text ≥3:1. AAA requires normal text ≥7:1 and large text ≥4.5:1. Most sites only need AA."),
            ("What color formats are supported?","Supports HEX (#FF0000), RGB (255,0,0), HSL (0,100%,50%) auto-detection, plus common color names (red, blue, etc.)."),
            ("What qualifies as large text?","WCAG defines large text as ≥18pt or ≥14pt bold. Large text has lower contrast requirements, making compliance easier to achieve."),
        ],
        "howto_zh": [("输入颜色","输入前景色和背景色"), ("查看结果","查看对比度和合规等级"), ("调整颜色","修改颜色直到通过检查")],
        "howto_en": [("Enter colors","Input foreground & background colors"), ("Check result","View contrast ratio & compliance"), ("Adjust","Tweak colors until passing")],
        "builder": build_color_contrast,
    },
    {
        "slug": "wheel-spin",
        "name_zh": "幸运转盘",
        "name_en": "Wheel Spinner",
        "desc_zh": "免费在线幸运转盘，自定义选项列表，随机公平抽取。适合抽奖、课堂互动、决策辅助、团队活动。支持保存加载、历史记录。无需注册，纯浏览器运行。",
        "desc_en": "Free online wheel spinner with customizable options. Fair random draws for raffles, classroom activities, decision making, team events. Save/load support, history. No registration, browser-only.",
        "kw_zh": "幸运转盘,抽奖转盘,随机抽取,课堂互动,决策辅助,在线抽奖,转盘工具",
        "kw_en": "wheel spinner,prize wheel,random picker,classroom activity,decision maker,online raffle,spinner tool",
        "meta_title_zh": "幸运转盘 - 自定义抽奖|随机抽取|免费在线工具",
        "meta_title_en": "Wheel Spinner - Custom Raffle | Random Picker | Free Online Tool",
        "og_title_zh": "🎡 幸运转盘",
        "og_title_en": "🎡 Wheel Spinner",
        "faq_zh": [
            ("转盘结果公正吗？","使用crypto.getRandomValues()密码学安全随机数，每次旋转独立公平，无法作弊。支持历史记录查看。"),
            ("可以添加多少个选项？","支持2-50个选项，每个选项可自定义文字。超过50个建议分组使用。"),
            ("可以保存转盘配置吗？","支持导出/导入JSON配置，保存常用转盘设置。点击保存将配置下载为文件，随时加载恢复。"),
        ],
        "faq_en": [
            ("Is the wheel fair?","Uses crypto.getRandomValues() for cryptographically secure randomness. Each spin is independent and fair. History available for review."),
            ("How many options can I add?","Supports 2-50 options with customizable text. For more than 50, consider grouping."),
            ("Can I save wheel configs?","Supports export/import JSON configs. Save your favorite wheel setups as files, load them anytime to restore."),
        ],
        "howto_zh": [("添加选项","在文本框中输入选项"), ("自定义","调整颜色和标签"), ("转动转盘","点击按钮随机抽取")],
        "howto_en": [("Add options","Enter options in the text box"), ("Customize","Adjust colors and labels"), ("Spin","Click button to randomly pick")],
        "builder": build_wheel_spin,
    },
    {
        "slug": "xml-sitemap",
        "name_zh": "XML Sitemap生成器",
        "name_en": "XML Sitemap Generator",
        "desc_zh": "免费在线XML Sitemap生成器，批量输入URL自动生成标准sitemap.xml。支持优先级、更新频率设置，一键下载复制。适合SEO优化、网站提交搜索引擎。",
        "desc_en": "Free online XML Sitemap generator. Batch input URLs to auto-generate standard sitemap.xml. Priority & changefreq settings, one-click download/copy. Perfect for SEO and search engine submission.",
        "kw_zh": "sitemap生成器,xml地图,网站地图,SEO工具,搜索引擎提交,站点地图,xml生成,在线工具",
        "kw_en": "sitemap generator,xml sitemap,site map,SEO tool,search engine submission,xml generator,online tool",
        "meta_title_zh": "XML Sitemap生成器 - 网站地图|SEO优化|免费在线工具",
        "meta_title_en": "XML Sitemap Generator - Site Map | SEO | Free Online Tool",
        "og_title_zh": "🗺️ XML Sitemap生成器",
        "og_title_en": "🗺️ XML Sitemap Generator",
        "faq_zh": [
            ("生成的sitemap符合搜索引擎标准吗？","完全符合Google、Bing等主流搜索引擎的sitemap协议标准（sitemaps.org），包含loc、lastmod、changefreq、priority标准字段。"),
            ("支持多少URL？","单次支持最多500个URL（符合单个sitemap文件限制）。如需更多URL，可以分批生成或使用sitemap索引文件。"),
            ("生成后如何使用？","下载XML文件上传到网站根目录，然后在Google Search Console提交sitemap地址即可。也可以直接复制内容手动保存。"),
        ],
        "faq_en": [
            ("Does the sitemap comply with search engine standards?","Fully compliant with Google, Bing sitemap protocol (sitemaps.org). Includes loc, lastmod, changefreq, priority standard fields."),
            ("How many URLs are supported?","Up to 500 URLs per generation (single sitemap limit). For more URLs, generate in batches or use sitemap index files."),
            ("How to use after generation?","Download the XML file, upload to site root, then submit the sitemap URL in Google Search Console. Or copy the content directly to save."),
        ],
        "howto_zh": [("输入URL","每行一个URL地址"), ("设置参数","选择更新频率和优先级"), ("生成下载","生成XML并下载复制")],
        "howto_en": [("Enter URLs","One URL per line"), ("Set params","Choose changefreq & priority"), ("Generate","Generate XML, download or copy")],
        "builder": build_xml_sitemap,
    },
    {
        "slug": "pixel-art",
        "name_zh": "像素画编辑器",
        "name_en": "Pixel Art Editor",
        "desc_zh": "免费在线像素画编辑器，支持多种画布尺寸、调色板、橡皮擦、导出PNG。适合像素风游戏素材、头像制作、像素艺术创作。纯浏览器运行，无需注册。",
        "desc_en": "Free online pixel art editor with multi-size canvas, palette, eraser, PNG export. Perfect for pixel game assets, avatar creation, pixel art. Browser-only, no registration needed.",
        "kw_zh": "像素画,像素编辑器,像素艺术,像素头像,sprite编辑器,像素风,在线绘图,在线工具",
        "kw_en": "pixel art,pixel editor,pixel art maker,sprite editor,8bit art,online drawing,online tool",
        "meta_title_zh": "像素画编辑器 - 在线像素绘图|导出PNG|免费在线工具",
        "meta_title_en": "Pixel Art Editor - Online Pixel Drawing | PNG Export | Free Online Tool",
        "og_title_zh": "🖼️ 像素画编辑器",
        "og_title_en": "🖼️ Pixel Art Editor",
        "faq_zh": [
            ("支持哪些画布尺寸？","支持8x8、16x16、32x32、64x64多种预设尺寸，也可自定义尺寸。小尺寸适合图标和头像，大尺寸适合复杂作品。"),
            ("可以导出什么格式？","支持PNG格式导出，自动移除空白像素背景实现透明效果。也可复制Data URL用于网页直接使用。"),
            ("有橡皮擦和取色功能吗？","有！支持橡皮擦模式、取色器（点击画布吸取颜色）、撤销/重做、清除画布等功能。"),
        ],
        "faq_en": [
            ("What canvas sizes are supported?","Supports 8x8, 16x16, 32x32, 64x64 presets plus custom sizes. Small sizes for icons/avatars, large for complex artwork."),
            ("What export formats?","PNG export with transparent background. Also copy as Data URL for direct web use."),
            ("Are there eraser and eyedropper tools?","Yes! Eraser mode, eyedropper (click to pick color), undo/redo, clear canvas."),
        ],
        "howto_zh": [("设置画布","选择画布尺寸"), ("选择颜色","点击调色板选色"), ("开始绘画","点击格子填充颜色")],
        "howto_en": [("Set canvas","Choose canvas size"), ("Pick color","Click palette to select"), ("Paint","Click cells to fill with color")],
        "builder": build_pixel_art,
    },
]


def main():
    for td in tools_data:
        slug = td["slug"]
        for lang in ["zh", "en"]:
            is_cn = lang == "zh"
            name = td["name_zh"] if is_cn else td["name_en"]
            desc = td["desc_zh"] if is_cn else td["desc_en"]
            kw = td["kw_zh"] if is_cn else td["kw_en"]
            mt = td["meta_title_zh"] if is_cn else td["meta_title_en"]
            og = td["og_title_zh"] if is_cn else td["og_title_en"]
            faq = td["faq_zh"] if is_cn else td["faq_en"]
            howto = td["howto_zh"] if is_cn else td["howto_en"]

            head = make_head(slug, name, desc, kw, mt, og, faq, howto, lang)
            js, body, css = td["builder"](td, lang)

            html = head + f'<style>\n{css}\n</style>\n</head>\n<body>\n{body}\n{js}\n</body>\n</html>'

            if is_cn:
                path = os.path.join(BASE, slug, "index.html")
            else:
                path = os.path.join(BASE, "en", slug, "index.html")
            write_file(path, html)

if __name__ == "__main__":
    main()
