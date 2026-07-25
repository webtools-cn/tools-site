#!/usr/bin/env python3
"""批量生成工具页面"""
import os

tools = {
    "domain-typo-generator": {
        "cn_name": "域名拼写错误生成器",
        "en_name": "Domain Typo Generator",
        "cn_desc": "免费在线域名拼写错误生成器，模拟常见输入错误（漏字、多字、错位、替换等），用于域名安全检查和typosquatting分析。",
        "en_desc": "Free online domain typo generator. Simulates common typing errors (omissions, insertions, transpositions, substitutions) for domain security checks and typosquatting analysis.",
        "cn_kw": "域名拼写错误,域名错字生成,typosquatting,域名安全,域名变体,输入错误模拟,域名拼写检查",
        "en_kw": "domain typo generator, typosquatting, domain misspelling, domain security, typo domain",
        "category": "developer"
    },
    "subnet-mask-calc": {
        "cn_name": "子网掩码计算器",
        "en_name": "Subnet Mask Calculator",
        "cn_desc": "免费在线子网掩码计算器，支持CIDR与子网掩码互转，计算网络地址、广播地址、可用IP范围和主机数量。",
        "en_desc": "Free online subnet mask calculator. CIDR to subnet mask conversion, network/broadcast address, usable IP range and host count calculation.",
        "cn_kw": "子网掩码计算器,子网计算,CIDR计算,IP地址计算,网络地址,广播地址,子网划分",
        "en_kw": "subnet calculator, CIDR calculator, subnet mask, IP calculator, network address, broadcast address",
        "category": "developer"
    },
    "api-rate-limiter-calc": {
        "cn_name": "API速率限制计算器",
        "en_name": "API Rate Limiter Calculator",
        "cn_desc": "免费在线API速率限制计算器，计算令牌桶/滑动窗口等策略下的请求配额、恢复时间和突发容量。",
        "en_desc": "Free online API rate limiter calculator. Calculate request quotas, recovery time and burst capacity under token bucket/sliding window strategies.",
        "cn_kw": "API限流,速率限制,令牌桶,滑动窗口,请求配额,API节流,速率控制",
        "en_kw": "API rate limiter, token bucket, sliding window, request quota, rate limiting, API throttling",
        "category": "developer"
    },
    "css-specificity-calc": {
        "cn_name": "CSS优先级计算器",
        "en_name": "CSS Specificity Calculator",
        "cn_desc": "免费在线CSS选择器优先级计算器，输入CSS选择器自动计算specificity值，支持ID/类/元素/伪类/属性选择器。",
        "en_desc": "Free online CSS specificity calculator. Enter any CSS selector and get its specificity value instantly. Supports ID, class, element, pseudo-class and attribute selectors.",
        "cn_kw": "CSS优先级,CSS特异性,specificity计算,CSS选择器权重,样式优先级,前端开发工具",
        "en_kw": "CSS specificity, CSS selector weight, specificity calculator, CSS priority, frontend tool",
        "category": "developer"
    },
    "rss-to-json": {
        "cn_name": "RSS转JSON转换器",
        "en_name": "RSS to JSON Converter",
        "cn_desc": "免费在线RSS/Atom Feed转JSON工具，将XML格式的RSS订阅源解析为结构化JSON数据，支持URL和粘贴输入。",
        "en_desc": "Free online RSS/Atom Feed to JSON converter. Parse XML RSS feeds into structured JSON data. Supports URL and paste input.",
        "cn_kw": "RSS转JSON,RSS解析,Atom转JSON,Feed转换,XML转JSON,订阅源解析",
        "en_kw": "RSS to JSON, RSS parser, Atom to JSON, feed converter, XML to JSON, feed parser",
        "category": "developer"
    },
    "sql-diff": {
        "cn_name": "SQL差异对比工具",
        "en_name": "SQL Diff Tool",
        "cn_desc": "免费在线SQL语句差异对比工具，支持CREATE TABLE、INSERT等SQL语句的逐行差异对比，数据库迁移和版本控制必备。",
        "en_desc": "Free online SQL diff tool. Line-by-line comparison of SQL statements including CREATE TABLE and INSERT. Essential for database migrations and version control.",
        "cn_kw": "SQL对比,SQL差异,SQL Diff,数据库迁移,SQL版本对比,SQL变更检测,SQL语句对比",
        "en_kw": "SQL diff, SQL compare, database migration, SQL change detection, SQL comparison tool",
        "category": "developer"
    },
    "fake-identity-generator": {
        "cn_name": "假身份信息生成器",
        "en_name": "Fake Identity Generator",
        "cn_desc": "免费在线假身份信息生成器，批量生成逼真的姓名、地址、电话、邮箱等测试数据，支持多国格式，适用于开发测试。",
        "en_desc": "Free online fake identity generator. Generate realistic names, addresses, phone numbers, emails and more in batch. Supports multiple country formats for development testing.",
        "cn_kw": "假身份生成器,测试数据生成,假姓名,假地址,假电话,假邮箱,开发测试数据,faker",
        "en_kw": "fake identity generator, test data, fake name, fake address, fake phone, fake email, faker",
        "category": "developer"
    },
    "cicd-pipeline-generator": {
        "cn_name": "CI/CD流水线生成器",
        "en_name": "CI/CD Pipeline Generator",
        "cn_desc": "免费在线CI/CD流水线配置生成器，支持GitHub Actions、GitLab CI、Jenkins等平台，可视化配置构建/测试/部署阶段。",
        "en_desc": "Free online CI/CD pipeline config generator. Supports GitHub Actions, GitLab CI, Jenkins and more. Visually configure build/test/deploy stages.",
        "cn_kw": "CI/CD生成器,流水线配置,CI/CD配置,GitHub Actions生成,GitLab CI生成,Jenkins配置,DevOps工具",
        "en_kw": "CI/CD generator, pipeline config, GitHub Actions generator, GitLab CI generator, Jenkins config, DevOps tool",
        "category": "developer"
    },
    "html-color-picker": {
        "cn_name": "HTML颜色选择器",
        "en_name": "HTML Color Picker",
        "cn_desc": "免费在线HTML颜色选择器和调色板，支持HEX/RGB/HSL/HSV格式互转，实时预览，拾取屏幕颜色，前端开发必备。",
        "en_desc": "Free online HTML color picker and palette. Supports HEX/RGB/HSL/HSV format conversion with live preview. Pick colors from screen. Essential for frontend development.",
        "cn_kw": "颜色选择器,HTML颜色,HEX转RGB,RGB转HSL,调色板,取色器,前端颜色工具",
        "en_kw": "color picker, HTML color, HEX to RGB, RGB to HSL, color palette, eyedropper, frontend color tool",
        "category": "developer"
    }
}

# HTML模板生成函数
def cn_template(name, info):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{info['cn_desc']}">
<meta name="keywords" content="{info['cn_kw']}">
<title>{info['cn_name']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{name}/">
<meta property="og:title" content="{info['cn_name']} - Free ToolBase">
<meta property="og:description" content="{info['cn_desc']}">
<meta property="og:url" content="https://free-toolbase.com/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{info['cn_name']}","description":"{info['cn_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"CNY"}}}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.input-group{{margin-bottom:16px}}
.input-group label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:6px}}
.input-group input,.input-group select,.input-group textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:monospace}}
.input-group input:focus,.input-group select:focus,.input-group textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.input-group textarea{{min-height:150px;resize:vertical}}
.row{{display:flex;gap:12px;align-items:end}}
.row .input-group{{flex:1}}
.result{{background:#1e293b;border-radius:12px;padding:20px;border:1px solid rgba(148,163,184,.1);margin-top:16px;display:none}}
.result h3{{font-size:1rem;color:#f1f5f9;margin-bottom:12px}}
.result-content{{font-family:monospace;font-size:.85rem;color:#e2e8f0;white-space:pre-wrap;word-break:break-all;max-height:400px;overflow-y:auto}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-top:24px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section code{{background:rgba(6,182,212,.1);color:#22d3ee;padding:2px 6px;border-radius:3px;font-size:.85rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}.row{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
  <nav class="nav-back"><a href="/">← 返回首页</a></nav>
  <div class="header">
    <h1>{info['cn_name']}</h1>
    <div class="lang-switch"><a href="/{name}/" class="active">中文</a><a href="/en/{name}/">EN</a></div>
  </div>

  <div class="input-group">
    <label for="toolInput">输入内容</label>
    <textarea id="toolInput" placeholder="请在此输入..."></textarea>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">立即处理</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制结果</button>
  </div>

  <div class="result" id="resultPanel">
    <h3>处理结果</h3>
    <div class="result-content" id="resultContent"></div>
  </div>

  <div class="info-section">
    <h2>关于此工具</h2>
    <p>{info['cn_desc']}</p>
    <p>所有数据处理都在浏览器本地完成，不会上传到任何服务器。你可以放心处理敏感数据。</p>
  </div>

  <footer class="footer">
    <a href="/">返回首页</a> | <a href="/en/{name}/">English Version</a>
    <p style="margin-top:8px">© 2026 Free ToolBase. 数据不上传，完全浏览器本地处理。</p>
  </footer>
</div>
<div id="toast" class="toast"></div>
<script>
const $=id=>document.getElementById(id);
const toast=msg=>{{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}};
// PLACEHOLDER: tool logic here
$('btnProcess').addEventListener('click',()=>{{
  const input=$('toolInput').value.trim();
  if(!input){{toast('请输入内容');return;}}
  // TOOL_SPECIFIC_LOGIC
  $('resultPanel').style.display='block';
}});
$('btnClear').addEventListener('click',()=>{{$('toolInput').value='';$('resultPanel').style.display='none';}});
$('btnCopy').addEventListener('click',()=>{{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制到剪贴板')).catch(()=>toast('复制失败'));}});
</script>
</body>
</html>'''

def en_template(name, info):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{info['en_desc']}">
<meta name="keywords" content="{info['en_kw']}">
<title>{info['en_name']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{name}/">
<meta property="og:title" content="{info['en_name']} - Free ToolBase">
<meta property="og:description" content="{info['en_desc']}">
<meta property="og:url" content="https://free-toolbase.com/en/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{info['en_name']}","description":"{info['en_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.input-group{{margin-bottom:16px}}
.input-group label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:6px}}
.input-group input,.input-group select,.input-group textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:monospace}}
.input-group input:focus,.input-group select:focus,.input-group textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.input-group textarea{{min-height:150px;resize:vertical}}
.row{{display:flex;gap:12px;align-items:end}}
.row .input-group{{flex:1}}
.result{{background:#1e293b;border-radius:12px;padding:20px;border:1px solid rgba(148,163,184,.1);margin-top:16px;display:none}}
.result h3{{font-size:1rem;color:#f1f5f9;margin-bottom:12px}}
.result-content{{font-family:monospace;font-size:.85rem;color:#e2e8f0;white-space:pre-wrap;word-break:break-all;max-height:400px;overflow-y:auto}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-top:24px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section code{{background:rgba(6,182,212,.1);color:#22d3ee;padding:2px 6px;border-radius:3px;font-size:.85rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}.row{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
  <nav class="nav-back"><a href="/en/">← Back to Home</a></nav>
  <div class="header">
    <h1>{info['en_name']}</h1>
    <div class="lang-switch"><a href="/{name}/">中文</a><a href="/en/{name}/" class="active">EN</a></div>
  </div>

  <div class="input-group">
    <label for="toolInput">Input</label>
    <textarea id="toolInput" placeholder="Enter your content here..."></textarea>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Process</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy Result</button>
  </div>

  <div class="result" id="resultPanel">
    <h3>Result</h3>
    <div class="result-content" id="resultContent"></div>
  </div>

  <div class="info-section">
    <h2>About This Tool</h2>
    <p>{info['en_desc']}</p>
    <p>All processing is done locally in your browser. No data is uploaded to any server.</p>
  </div>

  <footer class="footer">
    <a href="/en/">Back to Home</a> | <a href="/{name}/">中文版</a>
    <p style="margin-top:8px">© 2026 Free ToolBase. All processing is local — no data uploaded.</p>
  </footer>
</div>
<div id="toast" class="toast"></div>
<script>
const $=id=>document.getElementById(id);
const toast=msg=>{{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}};
// PLACEHOLDER: tool logic here
$('btnProcess').addEventListener('click',()=>{{
  const input=$('toolInput').value.trim();
  if(!input){{toast('Please enter content');return;}}
  // TOOL_SPECIFIC_LOGIC
  $('resultPanel').style.display='block';
}});
$('btnClear').addEventListener('click',()=>{{$('toolInput').value='';$('resultPanel').style.display='none';}});
$('btnCopy').addEventListener('click',()=>{{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));}});
</script>
</body>
</html>'''

# 写入骨架文件
for name, info in tools.items():
    cn_path = f'{name}/index.html'
    en_path = f'en/{name}/index.html'
    
    cn_content = cn_template(name, info)
    en_content = en_template(name, info)
    
    with open(cn_path, 'w') as f:
        f.write(cn_content)
    with open(en_path, 'w') as f:
        f.write(en_content)
    print(f'Created: {cn_path}, {en_path}')

print(f'\nDone! Created {len(tools)*2} files.')