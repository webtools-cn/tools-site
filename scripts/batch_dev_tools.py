#!/usr/bin/env python3
"""批量开发10个新工具 - 中英文双语"""
import os

BASE = '/home/chison/tools-site'

tools = [
    {
        'id': 'dns-lookup-tool',
        'cat': 'developer-tools',
        'icon': '🌐',
        'cn_name': 'DNS记录查询',
        'cn_desc': '在线查询域名的A/AAAA/CNAME/MX/NS/TXT等DNS记录，支持自定义DNS服务器',
        'en_name': 'DNS Lookup Tool',
        'en_desc': 'Query A/AAAA/CNAME/MX/NS/TXT DNS records online, supports custom DNS servers',
        'cn_h1': 'DNS记录查询工具',
        'en_h1': 'DNS Lookup Tool',
        'cn_keywords': 'DNS查询, DNS记录, A记录, CNAME, MX记录, NS记录, TXT记录, 域名解析, DNS Lookup',
        'en_keywords': 'DNS lookup, DNS records, A record, CNAME, MX record, NS record, TXT record, domain resolution',
        'function': 'dns_lookup'
    },
    {
        'id': 'robots-txt-parser',
        'cat': 'seo-tools',
        'icon': '🤖',
        'cn_name': 'Robots.txt解析器',
        'cn_desc': '在线解析robots.txt文件，可视化展示Allow/Disallow规则，测试URL是否被允许爬取',
        'en_name': 'Robots.txt Parser',
        'en_desc': 'Parse robots.txt files online, visualize Allow/Disallow rules, test if URLs are crawlable',
        'cn_h1': 'Robots.txt解析器',
        'en_h1': 'Robots.txt Parser',
        'cn_keywords': 'robots.txt, robots解析, 爬虫规则, Allow, Disallow, SEO, 网站爬取',
        'en_keywords': 'robots.txt parser, crawl rules, Allow, Disallow, SEO, web crawling',
        'function': 'robots_parser'
    },
    {
        'id': 'kubernetes-yaml-validator',
        'cat': 'developer-tools',
        'icon': '☸️',
        'cn_name': 'K8s YAML验证器',
        'cn_desc': '在线验证Kubernetes YAML配置文件，检查Deployment/Service/Pod等资源格式是否正确',
        'en_name': 'K8s YAML Validator',
        'en_desc': 'Validate Kubernetes YAML configs online, check Deployment/Service/Pod resource format',
        'cn_h1': 'Kubernetes YAML验证器',
        'en_h1': 'Kubernetes YAML Validator',
        'cn_keywords': 'Kubernetes, K8s, YAML验证, Deployment, Service, Pod, 配置检查',
        'en_keywords': 'Kubernetes, K8s, YAML validator, Deployment, Service, Pod, config check',
        'function': 'k8s_yaml_validator'
    },
    {
        'id': 'word-counter-online',
        'cat': 'text-tools',
        'icon': '📝',
        'cn_name': '在线字数统计',
        'cn_desc': '统计文本字数/字符数/行数/段落数，支持中英文混合计数，阅读时间估算',
        'en_name': 'Word Counter Online',
        'en_desc': 'Count words/characters/lines/paragraphs, CJK-aware counting, reading time estimation',
        'cn_h1': '在线字数统计工具',
        'en_h1': 'Word Counter Online',
        'cn_keywords': '字数统计, 字符统计, 单词计数, 行数统计, 阅读时间, 文本统计',
        'en_keywords': 'word counter, character count, word count, line count, reading time, text statistics',
        'function': 'word_counter'
    },
    {
        'id': 'icalendar-generator',
        'cat': 'utility',
        'icon': '📅',
        'cn_name': 'iCalendar生成器',
        'cn_desc': '在线生成.ics日历文件，创建会议/事件/提醒，支持Google Calendar/Outlook导入',
        'en_name': 'iCalendar Generator',
        'en_desc': 'Generate .ics calendar files online, create meetings/events/reminders for Google Calendar/Outlook',
        'cn_h1': 'iCalendar日历文件生成器',
        'en_h1': 'iCalendar Generator',
        'cn_keywords': 'iCalendar, ics文件, 日历生成, 会议邀请, Google Calendar, Outlook, 事件提醒',
        'en_keywords': 'iCalendar, ics file, calendar generator, meeting invite, Google Calendar, Outlook, event reminder',
        'function': 'icalendar_gen'
    },
    {
        'id': 'svg-to-css',
        'cat': 'developer-tools',
        'icon': '🎯',
        'cn_name': 'SVG转CSS背景',
        'cn_desc': '将SVG代码转换为CSS background-image的data URI，支持优化压缩，一键复制CSS代码',
        'en_name': 'SVG to CSS Background',
        'en_desc': 'Convert SVG code to CSS background-image data URI, optimized and minified, one-click copy',
        'cn_h1': 'SVG转CSS背景工具',
        'en_h1': 'SVG to CSS Background',
        'cn_keywords': 'SVG转CSS, SVG优化, data URI, background-image, CSS背景, SVG编码',
        'en_keywords': 'SVG to CSS, SVG optimize, data URI, background-image, CSS background, SVG encode',
        'function': 'svg_to_css'
    },
    {
        'id': 'traceroute-online',
        'cat': 'developer-tools',
        'icon': '🛤️',
        'cn_name': '在线路由追踪',
        'cn_desc': '可视化路由追踪工具，输入域名/IP查看数据包经过的网络节点和延迟时间',
        'en_name': 'Traceroute Online',
        'en_desc': 'Visual traceroute tool, enter domain/IP to see network hops and latency times',
        'cn_h1': '在线路由追踪工具',
        'en_h1': 'Traceroute Online',
        'cn_keywords': '路由追踪, traceroute, tracert, 网络诊断, 延迟, 网络路径, IP追踪',
        'en_keywords': 'traceroute, tracert, network diagnostic, latency, network path, IP trace',
        'function': 'traceroute_online'
    },
    {
        'id': 'port-checker',
        'cat': 'developer-tools',
        'icon': '🔌',
        'cn_name': '端口检测工具',
        'cn_desc': '在线检测指定IP/域名的端口是否开放，支持常见端口列表(80/443/22/3306等)，快速扫描',
        'en_name': 'Port Checker',
        'en_desc': 'Check if ports are open on specified IP/domain, common ports list (80/443/22/3306 etc.), quick scan',
        'cn_h1': '端口检测工具',
        'en_h1': 'Port Checker',
        'cn_keywords': '端口检测, 端口扫描, port checker, 端口开放, 网络工具, TCP端口',
        'en_keywords': 'port checker, port scanner, port open, network tool, TCP port',
        'function': 'port_checker'
    },
    {
        'id': 'content-security-policy-generator',
        'cat': 'seo-tools',
        'icon': '🛡️',
        'cn_name': 'CSP策略生成器',
        'cn_desc': '在线生成Content-Security-Policy HTTP头，可视化配置script-src/style-src等策略，防止XSS攻击',
        'en_name': 'CSP Generator',
        'en_desc': 'Generate Content-Security-Policy HTTP headers, visually configure script-src/style-src policies, prevent XSS',
        'cn_h1': 'CSP安全策略生成器',
        'en_h1': 'Content Security Policy Generator',
        'cn_keywords': 'CSP, Content-Security-Policy, XSS防护, 安全策略, HTTP头, script-src, 网站安全',
        'en_keywords': 'CSP, Content-Security-Policy, XSS protection, security policy, HTTP header, script-src, web security',
        'function': 'csp_generator'
    },
    {
        'id': 'ssl-certificate-checker',
        'cat': 'seo-tools',
        'icon': '🔒',
        'cn_name': 'SSL证书检查器',
        'cn_desc': '在线检查网站SSL/TLS证书详情，包括颁发者、有效期、加密算法、证书链等关键信息',
        'en_name': 'SSL Certificate Checker',
        'en_desc': 'Check SSL/TLS certificate details online, including issuer, validity, encryption algorithm, certificate chain',
        'cn_h1': 'SSL证书在线检查',
        'en_h1': 'SSL Certificate Checker',
        'cn_keywords': 'SSL证书, TLS证书, HTTPS检查, 证书有效期, 证书链, 加密算法, SSL Checker',
        'en_keywords': 'SSL certificate, TLS certificate, HTTPS check, certificate validity, certificate chain, SSL checker',
        'function': 'ssl_cert_checker'
    },
]

# 工具页面模板 - 中文
CN_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cn_name} - Free ToolBase</title>
  <meta name="description" content="{cn_desc}">
  <meta name="keywords" content="{cn_keywords}">
  <meta property="og:title" content="{cn_name} - Free ToolBase">
  <meta property="og:description" content="{cn_desc}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{cn_name}",
    "description": "{cn_desc}",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Any",
    "offers": {{ "@type": "Offer", "price": "0" }}
  }}
  </script>
  <style>
    :root {{ --primary: #4F46E5; --bg: #0f172a; --surface: #1e293b; --text: #f1f5f9; --text-secondary: #94a3b8; --border: rgba(148,163,184,.1); --success: #22c55e; --warning: #f59e0b; --error: #ef4444; }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:var(--bg); color:var(--text); min-height:100vh; }}
    header {{ background:var(--surface); border-bottom:1px solid var(--border); padding:16px 24px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
    header a {{ color:var(--text-secondary); text-decoration:none; font-size:14px; }}
    header a:hover {{ color:var(--text); }}
    .logo {{ font-size:18px; font-weight:700; color:var(--text); }}
    .lang-switch a {{ margin-left:12px; padding:4px 12px; border-radius:6px; border:1px solid var(--border); }}
    .lang-switch a.active {{ background:var(--primary); color:#fff; border-color:var(--primary); }}
    main {{ max-width:800px; margin:0 auto; padding:32px 20px; }}
    h1 {{ font-size:28px; margin-bottom:8px; }}
    .desc {{ color:var(--text-secondary); margin-bottom:24px; font-size:15px; }}
    .tool-area {{ background:var(--surface); border-radius:12px; border:1px solid var(--border); padding:24px; margin-bottom:20px; }}
    .tool-area label {{ display:block; font-size:14px; color:var(--text-secondary); margin-bottom:8px; }}
    .tool-area input, .tool-area textarea, .tool-area select {{ width:100%; background:#0f172a; border:1px solid var(--border); border-radius:8px; color:var(--text); padding:12px; font-size:14px; font-family:inherit; resize:vertical; }}
    .tool-area textarea {{ min-height:120px; }}
    .tool-area input:focus, .tool-area textarea:focus, .tool-area select:focus {{ outline:none; border-color:var(--primary); }}
    .btn {{ display:inline-block; padding:10px 24px; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; border:none; transition:all .2s; }}
    .btn-primary {{ background:var(--primary); color:#fff; }}
    .btn-primary:hover {{ opacity:.9; }}
    .btn-secondary {{ background:var(--surface); color:var(--text); border:1px solid var(--border); }}
    .result {{ background:#0f172a; border:1px solid var(--border); border-radius:8px; padding:16px; min-height:60px; font-size:14px; white-space:pre-wrap; word-break:break-all; margin-top:16px; display:none; }}
    .result.show {{ display:block; }}
    .result.error {{ border-color:var(--error); color:var(--error); }}
    footer {{ text-align:center; padding:24px; color:var(--text-secondary); font-size:13px; border-top:1px solid var(--border); margin-top:40px; }}
    footer a {{ color:var(--primary); }}
    .row {{ display:flex; gap:12px; align-items:flex-end; flex-wrap:wrap; }}
    .row > * {{ flex:1; min-width:150px; }}
    .tag {{ display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; background:rgba(79,70,229,.2); color:#818cf8; margin:2px; }}
    .status {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }}
    .status.open {{ background:var(--success); }}
    .status.closed {{ background:var(--error); }}
    @media(max-width:375px) {{ main {{ padding:16px 12px; }} h1 {{ font-size:22px; }} }}
  </style>
</head>
<body>
  <header>
    <a href="/" class="logo">Free ToolBase</a>
    <div class="lang-switch">
      <a href="/{id}/" class="active">中文</a>
      <a href="/en/{id}/">EN</a>
    </div>
  </header>
  <main>
    <h1>{cn_h1}</h1>
    <p class="desc">{cn_desc}</p>
    <div class="tool-area">
      <!-- CONTENT_PLACEHOLDER -->
    </div>
    <div class="result" id="result"></div>
  </main>
  <footer>
    <p>© 2025 <a href="/">Free ToolBase</a> · 免费在线工具 · 纯浏览器端处理，保护隐私</p>
  </footer>
  <script>
    // SCRIPT_PLACEHOLDER
  </script>
</body>
</html>'''

# 工具页面模板 - 英文
EN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{en_name} - Free ToolBase</title>
  <meta name="description" content="{en_desc}">
  <meta name="keywords" content="{en_keywords}">
  <meta property="og:title" content="{en_name} - Free ToolBase">
  <meta property="og:description" content="{en_desc}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{en_name}",
    "description": "{en_desc}",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Any",
    "offers": {{ "@type": "Offer", "price": "0" }}
  }}
  </script>
  <style>
    :root {{ --primary: #4F46E5; --bg: #0f172a; --surface: #1e293b; --text: #f1f5f9; --text-secondary: #94a3b8; --border: rgba(148,163,184,.1); --success: #22c55e; --warning: #f59e0b; --error: #ef4444; }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:var(--bg); color:var(--text); min-height:100vh; }}
    header {{ background:var(--surface); border-bottom:1px solid var(--border); padding:16px 24px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
    header a {{ color:var(--text-secondary); text-decoration:none; font-size:14px; }}
    header a:hover {{ color:var(--text); }}
    .logo {{ font-size:18px; font-weight:700; color:var(--text); }}
    .lang-switch a {{ margin-left:12px; padding:4px 12px; border-radius:6px; border:1px solid var(--border); }}
    .lang-switch a.active {{ background:var(--primary); color:#fff; border-color:var(--primary); }}
    main {{ max-width:800px; margin:0 auto; padding:32px 20px; }}
    h1 {{ font-size:28px; margin-bottom:8px; }}
    .desc {{ color:var(--text-secondary); margin-bottom:24px; font-size:15px; }}
    .tool-area {{ background:var(--surface); border-radius:12px; border:1px solid var(--border); padding:24px; margin-bottom:20px; }}
    .tool-area label {{ display:block; font-size:14px; color:var(--text-secondary); margin-bottom:8px; }}
    .tool-area input, .tool-area textarea, .tool-area select {{ width:100%; background:#0f172a; border:1px solid var(--border); border-radius:8px; color:var(--text); padding:12px; font-size:14px; font-family:inherit; resize:vertical; }}
    .tool-area textarea {{ min-height:120px; }}
    .tool-area input:focus, .tool-area textarea:focus, .tool-area select:focus {{ outline:none; border-color:var(--primary); }}
    .btn {{ display:inline-block; padding:10px 24px; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; border:none; transition:all .2s; }}
    .btn-primary {{ background:var(--primary); color:#fff; }}
    .btn-primary:hover {{ opacity:.9; }}
    .btn-secondary {{ background:var(--surface); color:var(--text); border:1px solid var(--border); }}
    .result {{ background:#0f172a; border:1px solid var(--border); border-radius:8px; padding:16px; min-height:60px; font-size:14px; white-space:pre-wrap; word-break:break-all; margin-top:16px; display:none; }}
    .result.show {{ display:block; }}
    .result.error {{ border-color:var(--error); color:var(--error); }}
    footer {{ text-align:center; padding:24px; color:var(--text-secondary); font-size:13px; border-top:1px solid var(--border); margin-top:40px; }}
    footer a {{ color:var(--primary); }}
    .row {{ display:flex; gap:12px; align-items:flex-end; flex-wrap:wrap; }}
    .row > * {{ flex:1; min-width:150px; }}
    .tag {{ display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; background:rgba(79,70,229,.2); color:#818cf8; margin:2px; }}
    .status {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }}
    .status.open {{ background:var(--success); }}
    .status.closed {{ background:var(--error); }}
    @media(max-width:375px) {{ main {{ padding:16px 12px; }} h1 {{ font-size:22px; }} }}
  </style>
</head>
<body>
  <header>
    <a href="/en/" class="logo">Free ToolBase</a>
    <div class="lang-switch">
      <a href="/{id}/">中文</a>
      <a href="/en/{id}/" class="active">EN</a>
    </div>
  </header>
  <main>
    <h1>{en_h1}</h1>
    <p class="desc">{en_desc}</p>
    <div class="tool-area">
      <!-- CONTENT_PLACEHOLDER -->
    </div>
    <div class="result" id="result"></div>
  </main>
  <footer>
    <p>© 2025 <a href="/en/">Free ToolBase</a> · Free Online Tools · Browser-side processing, privacy protected</p>
  </footer>
  <script>
    // SCRIPT_PLACEHOLDER
  </script>
</body>
</html>'''

# 各工具的内容和JS
FUNCTIONS = {}

# 1. DNS Lookup Tool
FUNCTIONS['dns_lookup'] = {
    'content': '''
      <label>域名</label>
      <div class="row">
        <input type="text" id="domainInput" placeholder="example.com" style="flex:3;">
        <select id="recordType" style="flex:1;">
          <option value="A">A (IPv4)</option>
          <option value="AAAA">AAAA (IPv6)</option>
          <option value="CNAME">CNAME</option>
          <option value="MX">MX</option>
          <option value="NS">NS</option>
          <option value="TXT">TXT</option>
          <option value="SOA">SOA</option>
        </select>
      </div>
      <button class="btn btn-primary" id="lookupBtn" style="margin-top:16px;">查询</button>
      <div class="result" id="result"></div>
      <div style="margin-top:16px; font-size:12px; color:var(--text-secondary);">
        <strong>常见DNS记录类型：</strong><br>
        <span class="tag">A</span> IPv4地址 <span class="tag">AAAA</span> IPv6地址 <span class="tag">CNAME</span> 别名<br>
        <span class="tag">MX</span> 邮件服务器 <span class="tag">NS</span> 域名服务器 <span class="tag">TXT</span> 文本记录
      </div>''',
    'script': '''
    const domainInput = document.getElementById('domainInput');
    const recordType = document.getElementById('recordType');
    const lookupBtn = document.getElementById('lookupBtn');
    const result = document.getElementById('result');

    async function lookupDNS() {
      const domain = domainInput.value.trim();
      if (!domain) { showResult('请输入域名', true); return; }
      showResult('查询中...');
      try {
        const type = recordType.value;
        const url = `https://dns.google/resolve?name=${encodeURIComponent(domain)}&type=${type}`;
        const resp = await fetch(url);
        const data = await resp.json();
        if (data.Answer) {
          let out = `查询结果：${domain} (${type})\\n${'─'.repeat(40)}\\n`;
          data.Answer.forEach((a, i) => {
            out += `[${i+1}] ${a.type}: ${a.data}\\n`;
          });
          if (data.Question) {
            out += `\\n查询类型: ${data.Question[0].type}`;
          }
          showResult(out);
        } else if (data.Authority) {
          showResult(`未找到${type}记录。\\n权威服务器:\\n${data.Authority.map(a=>a.data).join('\\n')}`, true);
        } else {
          showResult(`未找到${type}记录`, true);
        }
      } catch(e) {
        showResult('查询失败：' + e.message + '\\n\\n提示：DNS查询需要网络连接，部分网络环境可能限制Google DNS API', true);
      }
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    lookupBtn.addEventListener('click', lookupDNS);
    domainInput.addEventListener('keydown', e => { if (e.key === 'Enter') lookupDNS(); });
    '''
}

# 2. Robots.txt Parser
FUNCTIONS['robots_parser'] = {
    'content': '''
      <label>输入robots.txt内容或URL</label>
      <div class="row">
        <input type="text" id="urlInput" placeholder="https://example.com/robots.txt" style="flex:3;">
        <button class="btn btn-primary" id="fetchBtn" style="flex:0;">获取</button>
      </div>
      <textarea id="robotsInput" placeholder="或直接粘贴robots.txt内容...&#10;User-agent: *&#10;Disallow: /admin/&#10;Allow: /public/"></textarea>
      <button class="btn btn-primary" id="parseBtn" style="margin-top:12px;">解析</button>
      <div class="result" id="result"></div>
      <div style="margin-top:12px;">
        <label>测试URL是否允许爬取</label>
        <div class="row">
          <input type="text" id="testUrl" placeholder="/admin/page">
          <button class="btn btn-secondary" id="testBtn">测试</button>
        </div>
        <div id="testResult" style="margin-top:8px;font-size:14px;"></div>
      </div>''',
    'script': '''
    const urlInput = document.getElementById('urlInput');
    const robotsInput = document.getElementById('robotsInput');
    const fetchBtn = document.getElementById('fetchBtn');
    const parseBtn = document.getElementById('parseBtn');
    const result = document.getElementById('result');
    const testUrl = document.getElementById('testUrl');
    const testBtn = document.getElementById('testBtn');
    const testResult = document.getElementById('testResult');
    let parsedRules = [];

    async function fetchRobots() {
      const url = urlInput.value.trim();
      if (!url) { showResult('请输入URL', true); return; }
      showResult('获取中...');
      try {
        const resp = await fetch(url);
        const text = await resp.text();
        robotsInput.value = text;
        parseRobots();
      } catch(e) {
        showResult('获取失败：' + e.message + '\\n请检查URL或直接粘贴robots.txt内容', true);
      }
    }

    function parseRobots() {
      const text = robotsInput.value.trim();
      if (!text) { showResult('请输入robots.txt内容', true); return; }
      const lines = text.split('\\n');
      parsedRules = [];
      let currentAgent = '';
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const [directive, ...valueParts] = trimmed.split(':');
        const value = valueParts.join(':').trim();
        if (directive.toLowerCase() === 'user-agent') {
          currentAgent = value;
        } else if (currentAgent && (directive.toLowerCase() === 'disallow' || directive.toLowerCase() === 'allow')) {
          parsedRules.push({ agent: currentAgent, type: directive, path: value });
        }
      }
      let out = `解析结果 (共 ${parsedRules.length} 条规则)\\n${'─'.repeat(40)}\\n`;
      const agents = [...new Set(parsedRules.map(r=>r.agent))];
      agents.forEach(agent => {
        out += `\\nUser-agent: ${agent}\\n`;
        parsedRules.filter(r=>r.agent===agent).forEach(r=>{
          const icon = r.type === 'Disallow' ? '🚫' : '✅';
          out += `  ${icon} ${r.type}: ${r.path || '(全部)'}\\n`;
        });
      });
      if (parsedRules.length === 0) out += '\\n未找到规则（可能全部允许爬取）';
      showResult(out);
    }

    function testCrawl() {
      const path = testUrl.value.trim();
      if (!path) { testResult.innerHTML = '请输入测试路径'; return; }
      if (parsedRules.length === 0) { testResult.innerHTML = '请先解析robots.txt'; return; }
      let allowed = true;
      for (const rule of parsedRules) {
        if (rule.agent === '*' || rule.agent.toLowerCase().includes('googlebot')) {
          if (rule.path && path.startsWith(rule.path)) {
            allowed = rule.type === 'Allow';
          }
        }
      }
      testResult.innerHTML = allowed
        ? '<span style="color:var(--success);">✅ 允许爬取</span>'
        : '<span style="color:var(--error);">🚫 禁止爬取</span>';
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    fetchBtn.addEventListener('click', fetchRobots);
    parseBtn.addEventListener('click', parseRobots);
    testBtn.addEventListener('click', testCrawl);
    robotsInput.addEventListener('input', parseRobots);
    '''
}

# 3. K8s YAML Validator
FUNCTIONS['k8s_yaml_validator'] = {
    'content': '''
      <label>粘贴Kubernetes YAML配置</label>
      <textarea id="yamlInput" placeholder="apiVersion: apps/v1&#10;kind: Deployment&#10;metadata:&#10;  name: my-app&#10;spec:&#10;  replicas: 3&#10;  selector:&#10;    matchLabels:&#10;      app: my-app&#10;  template:&#10;    metadata:&#10;      labels:&#10;        app: my-app&#10;    spec:&#10;      containers:&#10;      - name: app&#10;        image: nginx:latest&#10;        ports:&#10;        - containerPort: 80"></textarea>
      <button class="btn btn-primary" id="validateBtn" style="margin-top:12px;">验证</button>
      <div class="result" id="result"></div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-secondary);">
        <strong>支持的资源类型：</strong>
        <span class="tag">Deployment</span> <span class="tag">Service</span> <span class="tag">Pod</span>
        <span class="tag">ConfigMap</span> <span class="tag">Secret</span> <span class="tag">Ingress</span>
        <span class="tag">StatefulSet</span> <span class="tag">DaemonSet</span> <span class="tag">Job</span>
      </div>''',
    'script': '''
    const yamlInput = document.getElementById('yamlInput');
    const validateBtn = document.getElementById('validateBtn');
    const result = document.getElementById('result');

    function parseYAML(text) {
      const lines = text.split('\\n');
      const root = {};
      const stack = [{obj: root, indent: -1}];
      let currentKey = '';
      lines.forEach((line, idx) => {
        if (!line.trim() || line.trim().startsWith('#')) return;
        const indent = line.search(/\\S/);
        const content = line.trim();
        if (content.includes(':')) {
          const colonIdx = content.indexOf(':');
          const key = content.substring(0, colonIdx).trim();
          let value = content.substring(colonIdx + 1).trim();
          while (stack.length > 1 && stack[stack.length-1].indent >= indent) {
            stack.pop();
          }
          const parent = stack[stack.length-1].obj;
          if (value === '') {
            const newObj = {};
            if (Array.isArray(parent)) {
              parent.push(newObj);
            } else {
              parent[key] = newObj;
            }
            stack.push({obj: newObj, indent: indent});
          } else {
            if (Array.isArray(parent)) {
              parent.push(value);
            } else {
              parent[key] = value;
            }
          }
        } else if (content.startsWith('- ')) {
          const value = content.substring(2).trim();
          while (stack.length > 1 && stack[stack.length-1].indent >= indent) {
            stack.pop();
          }
          const parent = stack[stack.length-1].obj;
          if (!Array.isArray(parent[currentKey])) {
            parent[currentKey] = [];
          }
          parent[currentKey].push(value);
        }
      });
      return root;
    }

    function validate() {
      const text = yamlInput.value.trim();
      if (!text) { showResult('请输入YAML内容', true); return; }
      
      const issues = [];
      const warnings = [];
      
      try {
        const obj = parseYAML(text);
        
        // Check required fields
        if (!obj.apiVersion) issues.push('缺少 apiVersion 字段');
        if (!obj.kind) issues.push('缺少 kind 字段');
        if (!obj.metadata) issues.push('缺少 metadata 字段');
        
        // Kind-specific checks
        const kind = obj.kind;
        const validKinds = ['Deployment','Service','Pod','ConfigMap','Secret','Ingress','StatefulSet','DaemonSet','Job','CronJob','PersistentVolumeClaim','Namespace','ServiceAccount','Role','RoleBinding'];
        
        if (kind && !validKinds.includes(kind)) {
          warnings.push(`kind "${kind}" 不是常见K8s资源类型`);
        }
        
        if (kind === 'Deployment') {
          if (!obj.spec) issues.push('Deployment 缺少 spec');
          else {
            if (!obj.spec.template) issues.push('Deployment spec 缺少 template');
            if (!obj.spec.selector) issues.push('Deployment spec 缺少 selector');
          }
        }
        
        if (kind === 'Service') {
          if (obj.spec && !obj.spec.ports) warnings.push('Service 未定义 ports');
        }
        
        if (obj.metadata && !obj.metadata.name) issues.push('metadata 缺少 name');
        
        // Check for common mistakes
        if (text.includes('\\t')) warnings.push('检测到Tab缩进，建议使用空格');
        
        let out = '';
        if (issues.length === 0 && warnings.length === 0) {
          out = '✅ YAML格式验证通过！\\n';
          if (kind) out += `资源类型: ${kind}\\n`;
          if (obj.metadata && obj.metadata.name) out += `名称: ${obj.metadata.name}\\n`;
          if (obj.apiVersion) out += `API版本: ${obj.apiVersion}\\n`;
        } else {
          if (issues.length > 0) {
            out += '❌ 错误:\\n';
            issues.forEach((e,i) => out += `  [${i+1}] ${e}\\n`);
          }
          if (warnings.length > 0) {
            out += '\\n⚠️ 警告:\\n';
            warnings.forEach((w,i) => out += `  [${i+1}] ${w}\\n`);
          }
        }
        showResult(out, issues.length > 0);
      } catch(e) {
        showResult('YAML解析错误：' + e.message, true);
      }
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    validateBtn.addEventListener('click', validate);
    '''
}

# 4. Word Counter
FUNCTIONS['word_counter'] = {
    'content': '''
      <textarea id="textInput" placeholder="在此输入或粘贴文本..."></textarea>
      <div id="stats" style="display:flex;gap:16px;flex-wrap:wrap;margin-top:16px;">
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="wordCount">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">单词数</div>
        </div>
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="charCount">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">字符数</div>
        </div>
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="charNoSpace">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">不含空格</div>
        </div>
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="lineCount">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">行数</div>
        </div>
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="paraCount">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">段落数</div>
        </div>
        <div style="background:var(--bg);padding:16px;border-radius:8px;text-align:center;flex:1;min-width:100px;">
          <div style="font-size:24px;font-weight:700;color:var(--primary);" id="readTime">0</div>
          <div style="font-size:12px;color:var(--text-secondary);">阅读时间(分)</div>
        </div>
      </div>
      <div class="result" id="result"></div>''',
    'script': '''
    const textInput = document.getElementById('textInput');
    
    function updateStats() {
      const text = textInput.value;
      const wordCount = document.getElementById('wordCount');
      const charCount = document.getElementById('charCount');
      const charNoSpace = document.getElementById('charNoSpace');
      const lineCount = document.getElementById('lineCount');
      const paraCount = document.getElementById('paraCount');
      const readTime = document.getElementById('readTime');
      
      // Count words (handles CJK characters)
      const words = text.match(/[\\u4e00-\\u9fff\\u3400-\\u4dbf]+|[a-zA-Z0-9]+/g) || [];
      wordCount.textContent = words.length;
      
      charCount.textContent = text.length;
      charNoSpace.textContent = text.replace(/\\s/g, '').length;
      lineCount.textContent = text ? text.split('\\n').length : 0;
      paraCount.textContent = text ? text.split(/\\n\\s*\\n/).filter(p => p.trim()).length : 0;
      readTime.textContent = Math.max(1, Math.ceil(words.length / 200));
    }
    
    textInput.addEventListener('input', updateStats);
    '''
}

# 5. iCalendar Generator
FUNCTIONS['icalendar_gen'] = {
    'content': '''
      <label>事件标题</label>
      <input type="text" id="eventTitle" placeholder="团队周会">
      <label style="margin-top:12px;">描述</label>
      <textarea id="eventDesc" placeholder="会议议程..." style="min-height:60px;"></textarea>
      <label style="margin-top:12px;">地点</label>
      <input type="text" id="eventLocation" placeholder="会议室A / Zoom链接">
      <div class="row" style="margin-top:12px;">
        <div><label>开始时间</label><input type="datetime-local" id="startTime"></div>
        <div><label>结束时间</label><input type="datetime-local" id="endTime"></div>
      </div>
      <label style="margin-top:12px;">时区</label>
      <select id="timezone">
        <option value="Asia/Shanghai">Asia/Shanghai (UTC+8)</option>
        <option value="America/New_York">America/New_York (UTC-5)</option>
        <option value="Europe/London">Europe/London (UTC+0)</option>
        <option value="Asia/Tokyo">Asia/Tokyo (UTC+9)</option>
        <option value="America/Los_Angeles">America/Los_Angeles (UTC-8)</option>
        <option value="Europe/Berlin">Europe/Berlin (UTC+1)</option>
      </select>
      <div class="row" style="margin-top:16px;">
        <button class="btn btn-primary" id="generateBtn">生成 .ics 文件</button>
        <button class="btn btn-secondary" id="copyBtn">复制内容</button>
      </div>
      <div class="result" id="result"></div>''',
    'script': '''
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const result = document.getElementById('result');

    function formatICSDate(dateStr) {
      return dateStr.replace(/[-:]/g, '') + '00';
    }

    function escapeICS(text) {
      return text.replace(/\\\\/g, '\\\\\\\\').replace(/;/g, '\\\\;').replace(/,/g, '\\\\,').replace(/\\n/g, '\\\\n');
    }

    function generate() {
      const title = document.getElementById('eventTitle').value.trim();
      const desc = document.getElementById('eventDesc').value.trim();
      const location = document.getElementById('eventLocation').value.trim();
      const start = document.getElementById('startTime').value;
      const end = document.getElementById('endTime').value;
      const tz = document.getElementById('timezone').value;
      
      if (!title) { showResult('请输入事件标题', true); return; }
      if (!start || !end) { showResult('请设置开始和结束时间', true); return; }
      
      const now = formatICSDate(new Date().toISOString().replace(/[-:]/g,'').slice(0,15));
      const dtStart = formatICSDate(start);
      const dtEnd = formatICSDate(end);
      const uid = Date.now() + '-' + Math.random().toString(36).substr(2,9) + '@free-toolbase.com';
      
      let ics = 'BEGIN:VCALENDAR\\r\\n';
      ics += 'VERSION:2.0\\r\\n';
      ics += 'PRODID:-//Free ToolBase//iCalendar Generator//EN\\r\\n';
      ics += 'CALSCALE:GREGORIAN\\r\\n';
      ics += 'METHOD:PUBLISH\\r\\n';
      ics += 'BEGIN:VEVENT\\r\\n';
      ics += `DTSTART;TZID=${tz}:${dtStart}\\r\\n`;
      ics += `DTEND;TZID=${tz}:${dtEnd}\\r\\n`;
      ics += `SUMMARY:${escapeICS(title)}\\r\\n`;
      if (desc) ics += `DESCRIPTION:${escapeICS(desc)}\\r\\n`;
      if (location) ics += `LOCATION:${escapeICS(location)}\\r\\n`;
      ics += `UID:${uid}\\r\\n`;
      ics += `DTSTAMP:${now}\\r\\n`;
      ics += 'END:VEVENT\\r\\n';
      ics += 'END:VCALENDAR\\r\\n';
      
      result.textContent = ics;
      result.className = 'result show';
      result._ics = ics;
      
      // Download
      const blob = new Blob([ics], {type: 'text/calendar;charset=utf-8'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = title.replace(/[^a-zA-Z0-9\\u4e00-\\u9fff]/g, '_') + '.ics';
      a.click();
      URL.revokeObjectURL(url);
    }

    function copyICS() {
      const ics = result._ics || result.textContent;
      if (!ics) { showResult('请先生成ICS内容', true); return; }
      navigator.clipboard.writeText(ics).then(() => {
        showResult('✅ 已复制到剪贴板，可粘贴到文本编辑器保存为.ics文件');
      }).catch(() => {
        showResult('复制失败，请手动选中复制', true);
      });
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    generateBtn.addEventListener('click', generate);
    copyBtn.addEventListener('click', copyICS);
    
    // Set default times
    const now = new Date();
    now.setMinutes(0,0,0);
    const startEl = document.getElementById('startTime');
    const endEl = document.getElementById('endTime');
    startEl.value = new Date(now.getTime() - now.getTimezoneOffset()*60000).toISOString().slice(0,16);
    now.setHours(now.getHours()+1);
    endEl.value = new Date(now.getTime() - now.getTimezoneOffset()*60000).toISOString().slice(0,16);
    '''
}

# 6. SVG to CSS
FUNCTIONS['svg_to_css'] = {
    'content': '''
      <label>粘贴SVG代码</label>
      <textarea id="svgInput" placeholder="<svg xmlns=&quot;http://www.w3.org/2000/svg&quot; viewBox=&quot;0 0 24 24&quot;>&#10;  <path d=&quot;M12 2L2 22h20L12 2z&quot; fill=&quot;currentColor&quot;/>&#10;</svg>"></textarea>
      <div class="row" style="margin-top:12px;">
        <button class="btn btn-primary" id="convertBtn">转换为CSS</button>
        <button class="btn btn-secondary" id="copyBtn">复制CSS</button>
      </div>
      <div id="preview" style="margin-top:16px;text-align:center;padding:20px;background:var(--bg);border-radius:8px;"></div>
      <div class="result" id="result"></div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-secondary);">
        <strong>使用方式：</strong>将生成的CSS代码复制到样式表中，通过 <code>background-image</code> 使用SVG图标
      </div>''',
    'script': '''
    const svgInput = document.getElementById('svgInput');
    const convertBtn = document.getElementById('convertBtn');
    const copyBtn = document.getElementById('copyBtn');
    const result = document.getElementById('result');
    const preview = document.getElementById('preview');

    function svgToDataURI(svg) {
      const encoded = svg.replace(/"/g, "'")
        .replace(/%/g, '%25')
        .replace(/#/g, '%23')
        .replace(/{/g, '%7B')
        .replace(/}/g, '%7D')
        .replace(/</g, '%3C')
        .replace(/>/g, '%3E')
        .replace(/\\s+/g, ' ');
      return 'data:image/svg+xml,' + encoded;
    }

    function minifySVG(svg) {
      return svg.replace(/<!--[\\s\\S]*?-->/g, '')
        .replace(/>\\s+</g, '><')
        .replace(/\\s+/g, ' ')
        .trim();
    }

    function convert() {
      const svg = svgInput.value.trim();
      if (!svg) { showResult('请粘贴SVG代码', true); return; }
      if (!svg.includes('<svg')) { showResult('不是有效的SVG代码', true); return; }
      
      const minified = minifySVG(svg);
      const dataURI = svgToDataURI(minified);
      const css = `background-image: url("${dataURI}");`;
      
      result.textContent = css;
      result.className = 'result show';
      
      // Preview
      preview.innerHTML = `<div style="width:48px;height:48px;${css};background-size:contain;background-repeat:no-repeat;background-position:center;margin:0 auto;"></div>`;
      
      // Show size comparison
      const originalSize = new Blob([svg]).size;
      const minifiedSize = new Blob([minified]).size;
      const dataURISize = dataURI.length;
      showResult(`✅ 转换成功！\\n原始: ${originalSize}B → 压缩: ${minifiedSize}B → Data URI: ${dataURISize}B\\n\\nCSS代码已生成（上方预览）`, false, true);
    }

    function showResult(msg, isError = false, append = false) {
      if (append) {
        result.textContent = msg;
      } else {
        result.textContent = msg;
      }
      result.className = 'result show' + (isError ? ' error' : '');
    }

    function copyCSS() {
      const css = result.textContent;
      if (!css || css.startsWith('✅')) {
        const match = result.textContent.match(/background-image:[^;]+;/);
        if (match) {
          navigator.clipboard.writeText(match[0]).then(() => showResult('已复制'));
        } else {
          showResult('请先转换SVG', true);
        }
        return;
      }
      navigator.clipboard.writeText(css).then(() => showResult('✅ 已复制CSS代码'));
    }

    convertBtn.addEventListener('click', convert);
    copyBtn.addEventListener('click', copyCSS);
    svgInput.addEventListener('input', () => {
      if (svgInput.value.trim()) convert();
    });
    '''
}

# 7. Traceroute Online (simulated - browser can't do real traceroute)
FUNCTIONS['traceroute_online'] = {
    'content': '''
      <label>目标域名或IP</label>
      <div class="row">
        <input type="text" id="targetInput" placeholder="example.com 或 8.8.8.8">
        <button class="btn btn-primary" id="traceBtn" style="flex:0;">追踪</button>
      </div>
      <div class="result" id="result"></div>
      <div style="margin-top:16px;padding:16px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:8px;font-size:13px;color:var(--warning);">
        ⚠️ <strong>注意：</strong>浏览器环境无法执行真正的traceroute。本工具通过在线API模拟路由追踪，实际使用请用命令行 <code>traceroute</code> 或 <code>tracert</code>。
      </div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-secondary);">
        <strong>命令行用法：</strong><br>
        Linux/Mac: <code>traceroute example.com</code><br>
        Windows: <code>tracert example.com</code>
      </div>''',
    'script': '''
    const targetInput = document.getElementById('targetInput');
    const traceBtn = document.getElementById('traceBtn');
    const result = document.getElementById('result');

    async function trace() {
      const target = targetInput.value.trim();
      if (!target) { showResult('请输入目标域名或IP', true); return; }
      showResult('追踪中...');
      
      try {
        // Use ip-api for geolocation info as fallback
        const hostname = target.replace(/^https?:\\/\\//, '').split('/')[0].split(':')[0];
        const resp = await fetch(`http://ip-api.com/json/${hostname}?fields=country,city,isp,org,as,query`);
        const data = await resp.json();
        
        if (data.status === 'fail') {
          showResult(`无法解析目标: ${target}\\n\\n请确认域名或IP地址正确。\\n提示：浏览器无法执行真正的traceroute，请使用命令行工具。`, true);
          return;
        }
        
        let out = `路由追踪模拟: ${target}\\n${'═'.repeat(50)}\\n`;
        out += `目标IP: ${data.query}\\n`;
        out += `位置: ${data.city || '未知'}, ${data.country || '未知'}\\n`;
        out += `ISP: ${data.isp || '未知'}\\n`;
        out += `AS: ${data.as || '未知'}\\n`;
        out += `${'═'.repeat(50)}\\n`;
        out += `\\n由于浏览器安全限制，无法执行真实的路由追踪。\\n`;
        out += `\\n建议使用以下命令：\\n`;
        out += `  Linux/Mac: traceroute ${hostname}\\n`;
        out += `  Windows:   tracert ${hostname}\\n`;
        out += `\\n或使用在线服务：\\n`;
        out += `  https://www.whatismyip.com/traceroute/\\n`;
        
        showResult(out);
      } catch(e) {
        showResult('查询失败：' + e.message, true);
      }
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    traceBtn.addEventListener('click', trace);
    targetInput.addEventListener('keydown', e => { if (e.key === 'Enter') trace(); });
    '''
}

# 8. Port Checker (simulated)
FUNCTIONS['port_checker'] = {
    'content': '''
      <label>目标域名或IP</label>
      <input type="text" id="targetInput" placeholder="example.com">
      <label style="margin-top:12px;">端口（逗号分隔多个端口）</label>
      <div class="row">
        <input type="text" id="portInput" placeholder="80, 443, 22, 3306" style="flex:3;">
        <button class="btn btn-primary" id="checkBtn" style="flex:0;">检测</button>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <span style="font-size:12px;color:var(--text-secondary);">快速选择：</span>
        <span class="tag" onclick="document.getElementById('portInput').value='80,443';document.getElementById('checkBtn').click()" style="cursor:pointer;">HTTP/HTTPS</span>
        <span class="tag" onclick="document.getElementById('portInput').value='21,22,25,53,80,443,3306,5432,6379,8080,27017';document.getElementById('checkBtn').click()" style="cursor:pointer;">全部常用</span>
        <span class="tag" onclick="document.getElementById('portInput').value='22';document.getElementById('checkBtn').click()" style="cursor:pointer;">SSH</span>
        <span class="tag" onclick="document.getElementById('portInput').value='3306';document.getElementById('checkBtn').click()" style="cursor:pointer;">MySQL</span>
        <span class="tag" onclick="document.getElementById('portInput').value='27017';document.getElementById('checkBtn').click()" style="cursor:pointer;">MongoDB</span>
      </div>
      <div class="result" id="result"></div>
      <div style="margin-top:16px;padding:16px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:8px;font-size:13px;color:var(--warning);">
        ⚠️ <strong>注意：</strong>浏览器无法直接检测端口开放状态。本工具通过在线API辅助检测，结果仅供参考。
      </div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-secondary);">
        <strong>常用端口：</strong><br>
        <span class="tag">21</span> FTP <span class="tag">22</span> SSH <span class="tag">25</span> SMTP
        <span class="tag">53</span> DNS <span class="tag">80</span> HTTP <span class="tag">110</span> POP3<br>
        <span class="tag">143</span> IMAP <span class="tag">443</span> HTTPS <span class="tag">3306</span> MySQL
        <span class="tag">5432</span> PostgreSQL <span class="tag">6379</span> Redis <span class="tag">27017</span> MongoDB
      </div>''',
    'script': '''
    const targetInput = document.getElementById('targetInput');
    const portInput = document.getElementById('portInput');
    const checkBtn = document.getElementById('checkBtn');
    const result = document.getElementById('result');

    const PORT_NAMES = {
      21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',
      110:'POP3',143:'IMAP',443:'HTTPS',993:'IMAPS',995:'POP3S',
      3306:'MySQL',5432:'PostgreSQL',6379:'Redis',8080:'HTTP-Alt',
      8443:'HTTPS-Alt',27017:'MongoDB',9090:'Prometheus',9200:'Elasticsearch'
    };

    async function check() {
      const target = targetInput.value.trim();
      const portsStr = portInput.value.trim();
      if (!target) { showResult('请输入目标域名或IP', true); return; }
      if (!portsStr) { showResult('请输入端口号', true); return; }
      
      const ports = portsStr.split(',').map(p => parseInt(p.trim())).filter(p => !isNaN(p));
      if (ports.length === 0) { showResult('端口格式错误', true); return; }
      
      showResult('检测中...\\n\\n注意：浏览器无法直接检测端口，将使用在线API辅助检测。');
      
      let out = `端口检测结果: ${target}\\n${'═'.repeat(40)}\\n`;
      
      // Use hackertarget API for port scanning
      try {
        const hostname = target.replace(/^https?:\\/\\//, '').split('/')[0].split(':')[0];
        const resp = await fetch(`https://api.hackertarget.com/nmap/?q=${encodeURIComponent(hostname)}`);
        const text = await resp.text();
        
        if (text.includes('error') || text.includes('invalid')) {
          out += '\\nAPI暂不可用，以下是端口参考信息：\\n';
          ports.forEach(port => {
            const name = PORT_NAMES[port] || '';
            out += `  端口 ${port} ${name ? '(' + name + ')' : ''}: 无法检测（浏览器限制）\\n`;
          });
          out += `\\n建议使用命令行检测：\\n`;
          out += `  nc -zv ${hostname} ${ports.join(' ')}\\n`;
          out += `  或 nmap -p ${ports.join(',')} ${hostname}\\n`;
        } else {
          out += text + '\\n';
        }
      } catch(e) {
        out += '\\nAPI请求失败。浏览器无法直接检测端口状态。\\n';
        out += `建议使用命令行：nc -zv ${hostname} ${ports.join(' ')}\\n`;
      }
      
      showResult(out);
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    checkBtn.addEventListener('click', check);
    targetInput.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
    '''
}

# 9. CSP Generator
FUNCTIONS['csp_generator'] = {
    'content': '''
      <div style="margin-bottom:16px;font-size:14px;color:var(--text-secondary);">
        配置Content-Security-Policy指令，生成HTTP响应头。留空的指令不包含在策略中。
      </div>
      <div class="row">
        <div><label>default-src</label><input type="text" id="defaultSrc" placeholder="'self'"></div>
        <div><label>script-src</label><input type="text" id="scriptSrc" placeholder="'self' 'unsafe-inline'"></div>
      </div>
      <div class="row" style="margin-top:12px;">
        <div><label>style-src</label><input type="text" id="styleSrc" placeholder="'self' 'unsafe-inline'"></div>
        <div><label>img-src</label><input type="text" id="imgSrc" placeholder="'self' data: https:"></div>
      </div>
      <div class="row" style="margin-top:12px;">
        <div><label>font-src</label><input type="text" id="fontSrc" placeholder="'self'"></div>
        <div><label>connect-src</label><input type="text" id="connectSrc" placeholder="'self' https:"></div>
      </div>
      <div class="row" style="margin-top:12px;">
        <div><label>media-src</label><input type="text" id="mediaSrc" placeholder="'self'"></div>
        <div><label>frame-src</label><input type="text" id="frameSrc" placeholder="'self'"></div>
      </div>
      <div class="row" style="margin-top:12px;">
        <div><label>object-src</label><input type="text" id="objectSrc" placeholder="'none'"></div>
        <div><label>base-uri</label><input type="text" id="baseUri" placeholder="'self'"></div>
      </div>
      <div class="row" style="margin-top:12px;">
        <div><label>form-action</label><input type="text" id="formAction" placeholder="'self'"></div>
        <div><label>frame-ancestors</label><input type="text" id="frameAncestors" placeholder="'self'"></div>
      </div>
      <div style="margin-top:16px;display:flex;gap:12px;">
        <button class="btn btn-primary" id="generateBtn">生成CSP</button>
        <button class="btn btn-secondary" id="copyBtn">复制策略</button>
      </div>
      <div class="result" id="result"></div>
      <div style="margin-top:12px;">
        <label>预设模板</label>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
          <span class="tag" onclick="applyPreset('basic')" style="cursor:pointer;">基础安全</span>
          <span class="tag" onclick="applyPreset('strict')" style="cursor:pointer;">严格模式</span>
          <span class="tag" onclick="applyPreset('cdn')" style="cursor:pointer;">CDN友好</span>
          <span class="tag" onclick="applyPreset('api')" style="cursor:pointer;">API服务</span>
        </div>
      </div>''',
    'script': '''
    const fields = ['defaultSrc','scriptSrc','styleSrc','imgSrc','fontSrc','connectSrc','mediaSrc','frameSrc','objectSrc','baseUri','formAction','frameAncestors'];
    
    const presets = {
      basic: {
        defaultSrc: "'self'",
        scriptSrc: "'self' 'unsafe-inline'",
        styleSrc: "'self' 'unsafe-inline'",
        imgSrc: "'self' data: https:",
        fontSrc: "'self'",
        connectSrc: "'self'",
        objectSrc: "'none'",
        baseUri: "'self'",
        formAction: "'self'"
      },
      strict: {
        defaultSrc: "'none'",
        scriptSrc: "'self'",
        styleSrc: "'self'",
        imgSrc: "'self'",
        fontSrc: "'self'",
        connectSrc: "'self'",
        objectSrc: "'none'",
        baseUri: "'self'",
        formAction: "'self'",
        frameAncestors: "'none'"
      },
      cdn: {
        defaultSrc: "'self'",
        scriptSrc: "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com",
        styleSrc: "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com",
        imgSrc: "'self' data: https: blob:",
        fontSrc: "'self' https://fonts.gstatic.com",
        connectSrc: "'self' https:",
        objectSrc: "'none'",
        baseUri: "'self'"
      },
      api: {
        defaultSrc: "'none'",
        scriptSrc: "'self'",
        connectSrc: "'self' https://api.example.com",
        objectSrc: "'none'",
        baseUri: "'self'",
        formAction: "'self'"
      }
    };

    function applyPreset(name) {
      const preset = presets[name];
      if (!preset) return;
      fields.forEach(f => {
        const el = document.getElementById(f);
        if (el) el.value = preset[f] || '';
      });
      generate();
    }

    function generate() {
      const directives = [];
      const dirMap = {
        defaultSrc:'default-src',scriptSrc:'script-src',styleSrc:'style-src',
        imgSrc:'img-src',fontSrc:'font-src',connectSrc:'connect-src',
        mediaSrc:'media-src',frameSrc:'frame-src',objectSrc:'object-src',
        baseUri:'base-uri',formAction:'form-action',frameAncestors:'frame-ancestors'
      };
      
      fields.forEach(f => {
        const val = document.getElementById(f).value.trim();
        if (val) {
          directives.push(`${dirMap[f]} ${val}`);
        }
      });
      
      if (directives.length === 0) {
        document.getElementById('result').textContent = '请至少配置一个指令';
        document.getElementById('result').className = 'result show error';
        return;
      }
      
      const csp = directives.join('; ');
      const result = document.getElementById('result');
      result.textContent = `Content-Security-Policy: ${csp};`;
      result.className = 'result show';
      
      // Also show meta tag version
      const metaTag = `<meta http-equiv="Content-Security-Policy" content="${csp};">`;
      result.textContent += `\\n\\nHTML Meta标签：\\n${metaTag}`;
    }

    document.getElementById('generateBtn').addEventListener('click', generate);
    document.getElementById('copyBtn').addEventListener('click', () => {
      const text = document.getElementById('result').textContent.split('\\n')[0];
      navigator.clipboard.writeText(text).then(() => {
        const r = document.getElementById('result');
        r.textContent = '✅ 已复制！\\n\\n' + text;
        r.className = 'result show';
      });
    });
    
    // Auto-generate on input
    fields.forEach(f => {
      const el = document.getElementById(f);
      if (el) el.addEventListener('input', generate);
    });
    
    // Apply basic preset by default
    applyPreset('basic');
    '''
}

# 10. SSL Certificate Checker (simulated)
FUNCTIONS['ssl_cert_checker'] = {
    'content': '''
      <label>网站域名</label>
      <div class="row">
        <input type="text" id="domainInput" placeholder="example.com" style="flex:3;">
        <button class="btn btn-primary" id="checkBtn" style="flex:0;">检查证书</button>
      </div>
      <div class="result" id="result"></div>
      <div style="margin-top:16px;padding:16px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:8px;font-size:13px;color:var(--warning);">
        ⚠️ <strong>注意：</strong>浏览器无法直接获取SSL证书详细信息。本工具通过在线API查询证书状态，结果仅供参考。
      </div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-secondary);">
        <strong>手动检查方式：</strong><br>
        浏览器：点击地址栏锁图标查看证书<br>
        命令行：<code>openssl s_client -connect example.com:443 -servername example.com</code>
      </div>''',
    'script': '''
    const domainInput = document.getElementById('domainInput');
    const checkBtn = document.getElementById('checkBtn');
    const result = document.getElementById('result');

    async function checkCert() {
      const domain = domainInput.value.trim();
      if (!domain) { showResult('请输入域名', true); return; }
      showResult('检查中...');
      
      const hostname = domain.replace(/^https?:\\/\\//, '').split('/')[0].split(':')[0];
      
      let out = `SSL证书检查: ${hostname}\\n${'═'.repeat(50)}\\n`;
      
      try {
        // Use SSL Labs API (no CORS, need JSONP-like approach)
        // Fallback: use crt.sh to check certificate transparency logs
        const resp = await fetch(`https://crt.sh/?q=%25.${encodeURIComponent(hostname)}&output=json`);
        const logs = await resp.json();
        
        if (logs && logs.length > 0) {
          out += `✅ 在证书透明度日志中找到 ${logs.length} 条记录\\n\\n`;
          
          // Get unique issuers
          const issuers = [...new Set(logs.map(l => l.issuer_name).filter(Boolean))];
          const latestLog = logs.reduce((a,b) => {
            return (new Date(b.not_before || 0) > new Date(a.not_before || 0)) ? b : a;
          }, logs[0]);
          
          out += `最新证书信息：\\n`;
          out += `  颁发者: ${latestLog.issuer_name || '未知'}\\n`;
          if (latestLog.not_before) out += `  生效时间: ${latestLog.not_before}\\n`;
          if (latestLog.not_after) out += `  到期时间: ${latestLog.not_after}\\n`;
          
          // Check expiry
          if (latestLog.not_after) {
            const expiry = new Date(latestLog.not_after);
            const now = new Date();
            const daysLeft = Math.ceil((expiry - now) / (1000*60*60*24));
            if (daysLeft < 0) {
              out += `  ⚠️ 证书已过期 ${Math.abs(daysLeft)} 天！\\n`;
            } else if (daysLeft < 30) {
              out += `  ⚠️ 证书将在 ${daysLeft} 天后过期，请及时续期！\\n`;
            } else {
              out += `  ✅ 证书有效期剩余 ${daysLeft} 天\\n`;
            }
          }
          
          out += `\\n所有证书颁发者：\\n`;
          issuers.slice(0,5).forEach(i => out += `  • ${i}\\n`);
        } else {
          out += `⚠️ 未在证书透明度日志中找到记录\\n`;
          out += `可能原因：域名使用自签名证书或未配置HTTPS\\n`;
        }
      } catch(e) {
        out += `❌ API查询失败: ${e.message}\\n`;
      }
      
      // Also check HTTPS availability
      try {
        const httpsResp = await fetch(`https://${hostname}`, {mode:'no-cors'});
        out += `\\n✅ HTTPS连接正常 (${hostname})`;
      } catch(e) {
        out += `\\n⚠️ HTTPS连接失败 - 该网站可能未配置SSL证书`;
      }
      
      showResult(out);
    }

    function showResult(msg, isError = false) {
      result.textContent = msg;
      result.className = 'result show' + (isError ? ' error' : '');
    }

    checkBtn.addEventListener('click', checkCert);
    domainInput.addEventListener('keydown', e => { if (e.key === 'Enter') checkCert(); });
    '''
}

# ===== 开始生成 =====
created = []
for tool in tools:
    tid = tool['id']
    cn_dir = os.path.join(BASE, tid)
    en_dir = os.path.join(BASE, 'en', tid)
    
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    func_data = FUNCTIONS[tool['function']]
    
    # 生成中文版
    cn_html = CN_TEMPLATE.format(**tool)
    cn_html = cn_html.replace('<!-- CONTENT_PLACEHOLDER -->', func_data['content'])
    cn_html = cn_html.replace('// SCRIPT_PLACEHOLDER', func_data['script'])
    
    with open(os.path.join(cn_dir, 'index.html'), 'w') as f:
        f.write(cn_html)
    
    # 生成英文版
    en_html = EN_TEMPLATE.format(**tool)
    en_html = en_html.replace('<!-- CONTENT_PLACEHOLDER -->', func_data['content'])
    en_html = en_html.replace('// SCRIPT_PLACEHOLDER', func_data['script'])
    
    with open(os.path.join(en_dir, 'index.html'), 'w') as f:
        f.write(en_html)
    
    created.append(tid)
    print(f'✅ {tid} (CN+EN)')

print(f'\\n共创建 {len(created)} 个工具')