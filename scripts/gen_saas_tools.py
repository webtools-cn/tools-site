#!/usr/bin/env python3
"""批量生成5个SaaS/商业计算器工具 (CN+EN)"""
import os, json

SITE = '/home/chison/tools-site'

TOOLS = [
    {
        'slug': 'saas-mrr-calculator',
        'title_cn': 'SaaS MRR计算器 - 月度经常性收入在线计算',
        'title_en': 'SaaS MRR Calculator - Monthly Recurring Revenue | Free ToolBase',
        'desc_cn': '在线SaaS MRR计算器，计算月度经常性收入(MRR)和年度经常性收入(ARR)。支持新客户MRR、扩展MRR、流失MRR等指标。免费在线工具。',
        'desc_en': 'Free SaaS MRR calculator to compute Monthly Recurring Revenue and Annual Recurring Revenue. Calculate new, expansion, contraction, and churn MRR. Free online tool.',
        'h1_cn': '📊 SaaS MRR计算器',
        'h1_en': '📊 SaaS MRR Calculator',
        'keywords_cn': 'SaaS MRR计算器,月度经常性收入,ARR计算,MRR计算,SaaS指标,在线工具',
        'keywords_en': 'SaaS MRR calculator, monthly recurring revenue, ARR calculator, SaaS metrics, online tool',
        'category': 'business',
        'emoji': '📊'
    },
    {
        'slug': 'startup-runway-calculator',
        'title_cn': '创业跑道计算器 - 现金流可持续时间在线计算',
        'title_en': 'Startup Runway Calculator - Cash Burn Rate | Free ToolBase',
        'desc_cn': '创业跑道计算器，根据现金余额和月均消耗率计算公司可持续运营月数。帮助创业者做好现金流规划。免费在线工具。',
        'desc_en': 'Startup runway calculator: compute how many months your startup can operate based on cash balance and monthly burn rate. Free online tool for founders.',
        'h1_cn': '🚀 创业跑道计算器',
        'h1_en': '🚀 Startup Runway Calculator',
        'keywords_cn': '创业跑道计算器,现金流,烧钱率,startup runway,burn rate,在线工具',
        'keywords_en': 'startup runway calculator, cash flow, burn rate, startup finance, online tool',
        'category': 'business',
        'emoji': '🚀'
    },
    {
        'slug': 'lead-conversion-rate-calculator',
        'title_cn': '线索转化率计算器 - 营销转化率在线分析',
        'title_en': 'Lead Conversion Rate Calculator - Marketing Funnel | Free ToolBase',
        'desc_cn': '线索转化率计算器，计算营销漏斗各阶段转化率。支持从访问到线索、从线索到成交等多级转化分析。免费在线工具。',
        'desc_en': 'Lead conversion rate calculator: analyze marketing funnel conversion rates. Calculate visitor-to-lead, lead-to-customer, and overall conversion metrics. Free online tool.',
        'h1_cn': '📈 线索转化率计算器',
        'h1_en': '📈 Lead Conversion Rate Calculator',
        'keywords_cn': '转化率计算器,线索转化,营销漏斗,conversion rate,在线工具',
        'keywords_en': 'conversion rate calculator, lead conversion, marketing funnel, online tool',
        'category': 'business',
        'emoji': '📈'
    },
    {
        'slug': 'revenue-churn-calculator',
        'title_cn': '收入流失率计算器 - SaaS客户流失分析',
        'title_en': 'Revenue Churn Calculator - SaaS Churn Analysis | Free ToolBase',
        'desc_cn': '收入流失率计算器，计算月度/年度收入流失率。支持客户流失率和收入流失率对比分析，帮助SaaS企业监控业务健康度。免费在线工具。',
        'desc_en': 'Revenue churn calculator: compute monthly and annual revenue churn rates. Compare customer churn vs revenue churn to monitor SaaS business health. Free online tool.',
        'h1_cn': '📉 收入流失率计算器',
        'h1_en': '📉 Revenue Churn Calculator',
        'keywords_cn': '收入流失率,SaaS流失率,churn rate,客户流失,在线工具',
        'keywords_en': 'revenue churn, SaaS churn rate, customer churn, online tool',
        'category': 'business',
        'emoji': '📉'
    },
    {
        'slug': 'viral-coefficient-calculator',
        'title_cn': '病毒系数计算器 - 产品增长指标分析',
        'title_en': 'Viral Coefficient Calculator - Growth Metrics | Free ToolBase',
        'desc_cn': '病毒系数计算器，计算产品病毒传播效率。通过邀请发送量和转化率评估病毒系数K值，预测用户增长潜力。免费在线工具。',
        'desc_en': 'Viral coefficient calculator: measure product virality with K-factor. Input invites sent and conversion rate to predict organic user growth. Free online tool.',
        'h1_cn': '🦠 病毒系数计算器',
        'h1_en': '🦠 Viral Coefficient Calculator',
        'keywords_cn': '病毒系数,K因子,病毒传播,增长指标,viral coefficient,在线工具',
        'keywords_en': 'viral coefficient, K-factor, viral growth, growth metrics, online tool',
        'category': 'business',
        'emoji': '🦠'
    }
]

def generate_tool(tool, lang):
    slug = tool['slug']
    if lang == 'cn':
        title = tool['title_cn']
        desc = tool['desc_cn']
        h1 = tool['h1_cn']
        keywords = tool['keywords_cn']
        lang_tag = 'zh-CN'
        canonical = f'https://free-toolbase.com/{slug}/'
        hreflang_en = f'https://free-toolbase.com/en/{slug}/'
        og_title = f'{tool["title_cn"].split(" - ")[0]} - Free ToolBase'
    else:
        title = tool['title_en']
        desc = tool['desc_en']
        h1 = tool['h1_en']
        keywords = tool['keywords_en']
        lang_tag = 'en'
        canonical = f'https://free-toolbase.com/en/{slug}/'
        hreflang_en = canonical
        og_title = title
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_tag}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="{hreflang_en}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Free ToolBase">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{tool['h1_cn'].split(' - ')[0] if lang == 'en' else tool['h1_cn']}",
    "description": "{desc}",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {{
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    }}
  }}
  </script>
  <style>
    :root {{
      --primary: #4F46E5;
      --primary-hover: #4338CA;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-secondary: #64748b;
      --border: #e2e8f0;
      --success: #10b981;
      --danger: #ef4444;
      --radius: 12px;
      --shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem 1rem;
      flex: 1;
      width: 100%;
    }}
    header {{
      text-align: center;
      padding: 1.5rem 0;
      border-bottom: 1px solid var(--border);
      margin-bottom: 2rem;
    }}
    header a {{
      text-decoration: none;
      color: var(--primary);
      font-weight: 700;
      font-size: 1.25rem;
    }}
    header nav {{
      display: flex;
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }}
    header nav a {{
      color: var(--text-secondary);
      font-size: 0.9rem;
    }}
    h1 {{
      font-size: 1.75rem;
      margin-bottom: 1.5rem;
      color: var(--text);
    }}
    .card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
      margin-bottom: 1.5rem;
    }}
    .input-group {{
      margin-bottom: 1rem;
    }}
    .input-group label {{
      display: block;
      font-weight: 600;
      margin-bottom: 0.35rem;
      color: var(--text-secondary);
      font-size: 0.9rem;
    }}
    .input-group input, .input-group select {{
      width: 100%;
      padding: 0.6rem 0.8rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 1rem;
      transition: border-color 0.2s;
    }}
    .input-group input:focus, .input-group select:focus {{
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
    }}
    .btn {{
      display: inline-block;
      padding: 0.65rem 1.5rem;
      background: var(--primary);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
      margin-right: 0.5rem;
    }}
    .btn:hover {{ background: var(--primary-hover); }}
    .btn-secondary {{
      background: var(--border);
      color: var(--text);
    }}
    .btn-secondary:hover {{ background: #cbd5e1; }}
    .result {{
      margin-top: 1rem;
      padding: 1rem;
      background: #f0fdf4;
      border-radius: 8px;
      border: 1px solid #bbf7d0;
      display: none;
    }}
    .result.show {{ display: block; }}
    .result-item {{
      display: flex;
      justify-content: space-between;
      padding: 0.4rem 0;
      border-bottom: 1px solid #dcfce7;
    }}
    .result-item:last-child {{ border-bottom: none; }}
    .result-value {{
      font-weight: 700;
      color: var(--primary);
    }}
    footer {{
      text-align: center;
      padding: 1.5rem;
      color: var(--text-secondary);
      font-size: 0.85rem;
      border-top: 1px solid var(--border);
      margin-top: auto;
    }}
    .toast {{
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      background: #1e293b;
      color: #fff;
      padding: 0.75rem 1.25rem;
      border-radius: 8px;
      font-size: 0.9rem;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.3s;
      z-index: 1000;
      pointer-events: none;
    }}
    .toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}
    @media (max-width: 480px) {{
      .container {{ padding: 1rem 0.75rem; }}
      h1 {{ font-size: 1.4rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <a href="{canonical.split(slug)[0] if lang == 'en' else '/'}">Free ToolBase</a>
    <nav>
      <a href="{canonical.split(slug)[0] if lang == 'en' else '/'}">{'Home' if lang == 'en' else '首页'}</a>
      <a href="{canonical.split(slug)[0] + '/en/' + slug + '/' if lang == 'cn' else '/' + slug + '/'}">{'中文' if lang == 'cn' else 'EN'}</a>
    </nav>
  </header>
  <main class="container">
    <h1>{h1}</h1>
    <div class="card" id="calc-card">
      {generate_inputs(tool)}
      <button class="btn" onclick="calculate()">{'计算' if lang == 'cn' else 'Calculate'}</button>
      <button class="btn btn-secondary" onclick="clearAll()">{'清空' if lang == 'cn' else 'Clear'}</button>
      <div class="result" id="result"></div>
    </div>
    {generate_related(tool)}
  </main>
  <footer>
    <p>&copy; 2025 Free ToolBase. All rights reserved.</p>
  </footer>
  <div class="toast" id="toast"></div>
  <script>
    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }}
    function copyResult(text) {{
      navigator.clipboard.writeText(text).then(() => showToast('{'已复制！' if lang == 'cn' else 'Copied!'}'));
    }}
    {generate_js(tool)}
  </script>
</body>
</html>'''
    return html

def generate_inputs(tool):
    slug = tool['slug']
    if slug == 'saas-mrr-calculator':
        return '''      <div class="input-group">
        <label for="new-mrr">New Customer MRR ($)</label>
        <input type="number" id="new-mrr" placeholder="e.g. 10000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="expansion-mrr">Expansion MRR ($)</label>
        <input type="number" id="expansion-mrr" placeholder="e.g. 2000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="contraction-mrr">Contraction MRR ($)</label>
        <input type="number" id="contraction-mrr" placeholder="e.g. 500" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="churn-mrr">Churned MRR ($)</label>
        <input type="number" id="churn-mrr" placeholder="e.g. 1000" step="0.01" min="0">
      </div>'''
    elif slug == 'startup-runway-calculator':
        return '''      <div class="input-group">
        <label for="cash">Cash Balance ($)</label>
        <input type="number" id="cash" placeholder="e.g. 100000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="burn-rate">Monthly Burn Rate ($)</label>
        <input type="number" id="burn-rate" placeholder="e.g. 15000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="revenue">Monthly Revenue ($)</label>
        <input type="number" id="revenue" placeholder="e.g. 5000" step="0.01" min="0">
      </div>'''
    elif slug == 'lead-conversion-rate-calculator':
        return '''      <div class="input-group">
        <label for="visitors">Total Visitors</label>
        <input type="number" id="visitors" placeholder="e.g. 10000" min="0">
      </div>
      <div class="input-group">
        <label for="leads">Leads Generated</label>
        <input type="number" id="leads" placeholder="e.g. 500" min="0">
      </div>
      <div class="input-group">
        <label for="customers">Customers Acquired</label>
        <input type="number" id="customers" placeholder="e.g. 50" min="0">
      </div>'''
    elif slug == 'revenue-churn-calculator':
        return '''      <div class="input-group">
        <label for="start-mrr">MRR at Start ($)</label>
        <input type="number" id="start-mrr" placeholder="e.g. 50000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="end-mrr">MRR at End ($)</label>
        <input type="number" id="end-mrr" placeholder="e.g. 45000" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="new-mrr-churn">New MRR Added ($)</label>
        <input type="number" id="new-mrr-churn" placeholder="e.g. 3000" step="0.01" min="0">
      </div>'''
    elif slug == 'viral-coefficient-calculator':
        return '''      <div class="input-group">
        <label for="invites">Invites Sent per User</label>
        <input type="number" id="invites" placeholder="e.g. 5" step="0.01" min="0">
      </div>
      <div class="input-group">
        <label for="conversion-rate-viral">Conversion Rate (%)</label>
        <input type="number" id="conversion-rate-viral" placeholder="e.g. 20" step="0.01" min="0" max="100">
      </div>'''

def generate_related(tool):
    """生成相关工具推荐"""
    slug = tool['slug']
    related = {
        'saas-mrr-calculator': [('revenue-churn-calculator', 'Revenue Churn'), ('startup-runway-calculator', 'Startup Runway'), ('lead-conversion-rate-calculator', 'Lead Conversion')],
        'startup-runway-calculator': [('saas-mrr-calculator', 'SaaS MRR'), ('revenue-churn-calculator', 'Revenue Churn'), ('burn-rate-calculator', 'Burn Rate')],
        'lead-conversion-rate-calculator': [('viral-coefficient-calculator', 'Viral Coefficient'), ('saas-mrr-calculator', 'SaaS MRR'), ('startup-runway-calculator', 'Startup Runway')],
        'revenue-churn-calculator': [('saas-mrr-calculator', 'SaaS MRR'), ('startup-runway-calculator', 'Startup Runway'), ('lead-conversion-rate-calculator', 'Lead Conversion')],
        'viral-coefficient-calculator': [('lead-conversion-rate-calculator', 'Lead Conversion'), ('saas-mrr-calculator', 'SaaS MRR'), ('startup-runway-calculator', 'Startup Runway')],
    }
    items = related.get(slug, [])
    links = ''.join([f'<a href="/en/{s}/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">{n}</a>' for s, n in items])
    return f'<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 Related Tools</h2><div style="display:flex;flex-wrap:wrap;gap:4px;">{links}</div></section>'

def generate_js(tool):
    slug = tool['slug']
    if slug == 'saas-mrr-calculator':
        return '''
    function calculate() {
      const n = parseFloat(document.getElementById('new-mrr').value) || 0;
      const e = parseFloat(document.getElementById('expansion-mrr').value) || 0;
      const c = parseFloat(document.getElementById('contraction-mrr').value) || 0;
      const ch = parseFloat(document.getElementById('churn-mrr').value) || 0;
      if (n+e+c+ch === 0) { showToast('Please enter at least one value'); return; }
      const netNew = n + e - c - ch;
      const total = n + e;
      const churnRate = total > 0 ? (ch / total * 100).toFixed(1) : '0.0';
      document.getElementById('result').innerHTML = `
        <div class="result-item"><span>Net New MRR</span><span class="result-value">$${netNew.toLocaleString('en-US', {minimumFractionDigits:2})}</span></div>
        <div class="result-item"><span>Total MRR</span><span class="result-value">$${(n+e).toLocaleString('en-US', {minimumFractionDigits:2})}</span></div>
        <div class="result-item"><span>MRR Churn Rate</span><span class="result-value">${churnRate}%</span></div>
        <div class="result-item"><span>Annual Run Rate (ARR)</span><span class="result-value">$${(netNew*12).toLocaleString('en-US', {minimumFractionDigits:2})}</span></div>
      `;
      document.getElementById('result').classList.add('show');
    }
    function clearAll() {
      ['new-mrr','expansion-mrr','contraction-mrr','churn-mrr'].forEach(id => document.getElementById(id).value='');
      document.getElementById('result').classList.remove('show');
    }'''
    elif slug == 'startup-runway-calculator':
        return '''
    function calculate() {
      const cash = parseFloat(document.getElementById('cash').value) || 0;
      const burn = parseFloat(document.getElementById('burn-rate').value) || 0;
      const rev = parseFloat(document.getElementById('revenue').value) || 0;
      if (cash <= 0 || burn <= 0) { showToast('Please enter cash balance and burn rate'); return; }
      const netBurn = burn - rev;
      const months = netBurn > 0 ? (cash / netBurn).toFixed(1) : (rev >= burn ? '∞' : '0');
      document.getElementById('result').innerHTML = `
        <div class="result-item"><span>Net Monthly Burn</span><span class="result-value">$${netBurn.toLocaleString('en-US', {minimumFractionDigits:2})}</span></div>
        <div class="result-item"><span>Runway</span><span class="result-value">${months} months</span></div>
      `;
      document.getElementById('result').classList.add('show');
    }
    function clearAll() {
      ['cash','burn-rate','revenue'].forEach(id => document.getElementById(id).value='');
      document.getElementById('result').classList.remove('show');
    }'''
    elif slug == 'lead-conversion-rate-calculator':
        return '''
    function calculate() {
      const v = parseFloat(document.getElementById('visitors').value) || 0;
      const l = parseFloat(document.getElementById('leads').value) || 0;
      const c = parseFloat(document.getElementById('customers').value) || 0;
      if (v <= 0) { showToast('Please enter number of visitors'); return; }
      const vtl = v > 0 ? (l/v*100).toFixed(2) : '0.00';
      const ltc = l > 0 ? (c/l*100).toFixed(2) : '0.00';
      const overall = v > 0 ? (c/v*100).toFixed(2) : '0.00';
      document.getElementById('result').innerHTML = `
        <div class="result-item"><span>Visitor → Lead</span><span class="result-value">${vtl}%</span></div>
        <div class="result-item"><span>Lead → Customer</span><span class="result-value">${ltc}%</span></div>
        <div class="result-item"><span>Overall Conversion</span><span class="result-value">${overall}%</span></div>
      `;
      document.getElementById('result').classList.add('show');
    }
    function clearAll() {
      ['visitors','leads','customers'].forEach(id => document.getElementById(id).value='');
      document.getElementById('result').classList.remove('show');
    }'''
    elif slug == 'revenue-churn-calculator':
        return '''
    function calculate() {
      const start = parseFloat(document.getElementById('start-mrr').value) || 0;
      const end = parseFloat(document.getElementById('end-mrr').value) || 0;
      const add = parseFloat(document.getElementById('new-mrr-churn').value) || 0;
      if (start <= 0) { showToast('Please enter starting MRR'); return; }
      const gross = start - end + add;
      const rate = start > 0 ? (gross/start*100).toFixed(2) : '0.00';
      document.getElementById('result').innerHTML = `
        <div class="result-item"><span>Gross MRR Churn</span><span class="result-value">$${gross.toLocaleString('en-US', {minimumFractionDigits:2})}</span></div>
        <div class="result-item"><span>Net Revenue Retention</span><span class="result-value">${(100-parseFloat(rate)).toFixed(1)}%</span></div>
        <div class="result-item"><span>Churn Rate</span><span class="result-value">${rate}%</span></div>
      `;
      document.getElementById('result').classList.add('show');
    }
    function clearAll() {
      ['start-mrr','end-mrr','new-mrr-churn'].forEach(id => document.getElementById(id).value='');
      document.getElementById('result').classList.remove('show');
    }'''
    elif slug == 'viral-coefficient-calculator':
        return '''
    function calculate() {
      const inv = parseFloat(document.getElementById('invites').value) || 0;
      const conv = parseFloat(document.getElementById('conversion-rate-viral').value) || 0;
      if (inv <= 0) { showToast('Please enter invites per user'); return; }
      const k = (inv * conv / 100).toFixed(2);
      let interpretation = k > 1 ? 'Viral! Each user brings >1 new user' : k > 0.5 ? 'Moderate growth potential' : 'Low viral growth';
      document.getElementById('result').innerHTML = `
        <div class="result-item"><span>Viral Coefficient (K)</span><span class="result-value">${k}</span></div>
        <div class="result-item"><span>Interpretation</span><span class="result-value">${interpretation}</span></div>
        <div class="result-item"><span>Growth Cycle Users</span><span class="result-value">${Math.round(inv*conv/100)} per user</span></div>
      `;
      document.getElementById('result').classList.add('show');
    }
    function clearAll() {
      ['invites','conversion-rate-viral'].forEach(id => document.getElementById(id).value='');
      document.getElementById('result').classList.remove('show');
    }'''

# 生成所有工具
for tool in TOOLS:
    for lang in ['cn', 'en']:
        slug = tool['slug']
        dir_path = os.path.join(SITE, slug if lang == 'cn' else f'en/{slug}')
        os.makedirs(dir_path, exist_ok=True)
        html = generate_tool(tool, lang)
        with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Generated: {dir_path}/index.html')

print('\\nAll 10 tool pages (5 CN + 5 EN) generated successfully!')