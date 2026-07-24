#!/usr/bin/env python3
"""快速创建3个补充工具"""
import os, json

BASE = "/home/chison/tools-site"

GA_HEAD = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>"""

CSS = """*{box-sizing:border-box;margin:0;padding:0}
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
.hero{margin-bottom:20px;padding:16px;background:#1e293b;border-radius:12px;border:1px solid rgba(148,163,184,.1)}
.hero p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.75rem;padding:4px 10px;border-radius:20px}
.card{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.card h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}
label{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}
input,textarea,select{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit;margin-bottom:12px}
input:focus,textarea:focus,select:focus{outline:none;border-color:rgba(6,182,212,.5)}
.row{display:flex;gap:12px;flex-wrap:wrap}
.row .field{flex:1;min-width:140px}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}
.btn-success:hover{background:rgba(34,197,94,.25)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.result-box{background:#0f172a;border-radius:8px;padding:16px;margin:8px 0;border:1px solid rgba(6,182,212,.3);overflow-x:auto;min-height:60px;font-family:monospace;font-size:.9rem;white-space:pre-wrap;word-break:break-all}
.stats{color:#64748b;font-size:.8rem;margin-top:4px}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section p,.info-section li{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.info-section ul{padding-left:20px;margin-bottom:12px}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.footer a:hover{color:#94a3b8}
#toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}
#toast.show{opacity:1}
@media(max-width:600px){.row{flex-direction:column}h1{font-size:1.2rem;word-break:break-word}.header{flex-direction:column;gap:8px}}</style>"""

def make_schema_zh(name, desc, slug):
    return json.dumps([{"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"description":desc,"applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},{"@context":"https://schema.org","@type":"HowTo","name":f"如何使用{name}","description":f"如何使用{name}的详细步骤指南","totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":[{"@type":"HowToStep","position":1,"name":"输入内容","text":"在输入框中输入或粘贴需要处理的内容"},{"@type":"HowToStep","position":2,"name":"设置参数","text":"根据需要调整工具参数和选项"},{"@type":"HowToStep","position":3,"name":"执行操作","text":"点击处理按钮开始执行"},{"@type":"HowToStep","position":4,"name":"获取结果","text":"查看处理结果并一键复制"}]},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"},{"@type":"ListItem","position":3,"name":name,"item":f"https://free-toolbase.com/{slug}/"}]}],ensure_ascii=False)

def make_schema_en(name, desc, slug):
    return json.dumps([{"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"description":desc,"applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},{"@context":"https://schema.org","@type":"HowTo","name":f"How to Use {name}","description":f"Step-by-step guide for using {name}","totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":[{"@type":"HowToStep","position":1,"name":"Input","text":"Enter or paste your content into the input field"},{"@type":"HowToStep","position":2,"name":"Configure","text":"Adjust tool settings and options as needed"},{"@type":"HowToStep","position":3,"name":"Process","text":"Click the process button to execute"},{"@type":"HowToStep","position":4,"name":"Get Results","text":"View the output and copy with one click"}]},{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"},{"@type":"ListItem","position":3,"name":name,"item":f"https://free-toolbase.com/en/{slug}/"}]}],ensure_ascii=False)

def make_meta_zh(title, desc, slug, og_title):
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{title},工具,在线工具,免费">
<title>{og_title} | Free | 无需注册</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{og_title} | Free | 无需注册">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">"""

def make_meta_en(title, desc, slug, og_title):
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{title},tools,online tool,free">
<title>{og_title} | Free | No Sign-Up</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{og_title} | Free | No Sign-Up">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">"""

tools = [
    {
        "slug": "complaint-letter",
        "name_zh": "投诉信生成器",
        "name_en": "Complaint Letter Generator",
        "desc_zh": "免费在线投诉信生成工具，快速生成专业投诉信件。支持多种场景（产品投诉、服务投诉、账单争议等），填写信息即可生成正式投诉信，支持复制和下载。",
        "desc_en": "Free online complaint letter generator - quickly create professional complaint letters. Supports multiple scenarios (product, service, billing disputes). Fill in details and generate a formal complaint letter. Copy and download supported.",
        "icon_zh": "📝", "icon_en": "📝",
        "html_zh": """<div class="card"><h2>📋 投诉信息</h2><div class="row"><div class="field"><label>投诉类型</label><select id="type"><option value="product">产品投诉</option><option value="service">服务投诉</option><option value="billing">账单争议</option><option value="delivery">物流投诉</option><option value="quality">质量问题</option><option value="refund">退款要求</option></select></div><div class="field"><label>收信方</label><input type="text" id="recipient" value="客服部门" placeholder="公司名/部门"></div></div><div class="row"><div class="field"><label>您的姓名</label><input type="text" id="senderName" value="张三" placeholder="您的姓名"></div><div class="field"><label>订单/产品编号</label><input type="text" id="orderId" placeholder="可选"></div></div><label>投诉内容描述</label><textarea id="description" placeholder="详细描述您遇到的问题..." rows="4">我在贵公司购买的商品存在质量问题，产品与描述不符，且无法正常使用。我已尝试联系客服但未得到满意解决。</textarea><div class="btn-row"><button class="btn btn-primary" onclick="generate()">✍️ 生成投诉信</button><button class="btn btn-success" id="copyBtn" style="display:none" onclick="copyLetter()">📋 复制信件</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📄 生成的投诉信</h2><div class="result-box" id="letterOutput"></div></div>
<script>function generate(){const type=document.getElementById('type').value;const recipient=document.getElementById('recipient').value||'客服部门';const sender=document.getElementById('senderName').value||'尊敬的客户';const orderId=document.getElementById('orderId').value;const desc=document.getElementById('description').value||'[请填写具体问题]';const date=new Date().toLocaleDateString('zh-CN',{year:'numeric',month:'long',day:'numeric'});const typeLabels={product:'产品投诉',service:'服务投诉',billing:'账单争议',delivery:'物流投诉',quality:'质量问题',refund:'退款要求'};let letter=`${date}

致：${recipient}

主题：关于${typeLabels[type]}的正式投诉

尊敬的${recipient}负责人：

您好！

我是一名贵公司的客户，现就以下问题提出正式投诉：

${orderId?`相关订单/产品编号：${orderId}\n`:''}投诉事项：${desc}

基于以上情况，我提出以下诉求：
1. 请贵公司对上述问题进行调查并给予合理解释；
2. 根据消费者权益保护相关法规，我要求${type==='refund'?'全额退款':'予以妥善处理，包括但不限于退换货、赔偿损失等措施'}；
3. 请在收到本函后7个工作日内给予书面回复。

如贵公司未能在合理期限内妥善处理，我将保留向消费者协会投诉及采取法律途径维权的权利。

期待您的及时回复。

此致
敬礼

${sender}
联系电话：[请填写]
电子邮箱：[请填写]
${date}`;
document.getElementById('letterOutput').textContent=letter;
document.getElementById('resultCard').style.display='block';
document.getElementById('copyBtn').style.display='inline-block';
toast('投诉信已生成');}
async function copyLetter(){const t=document.getElementById('letterOutput').textContent;await navigator.clipboard.writeText(t);toast('已复制到剪贴板');}</script>""",
        "html_en": """<div class="card"><h2>📋 Complaint Details</h2><div class="row"><div class="field"><label>Complaint Type</label><select id="type"><option value="product">Product Issue</option><option value="service">Service Issue</option><option value="billing">Billing Dispute</option><option value="delivery">Delivery Issue</option><option value="quality">Quality Issue</option><option value="refund">Refund Request</option></select></div><div class="field"><label>Recipient</label><input type="text" id="recipient" value="Customer Service" placeholder="Company/Department"></div></div><div class="row"><div class="field"><label>Your Name</label><input type="text" id="senderName" value="John Doe" placeholder="Your name"></div><div class="field"><label>Order/Product ID</label><input type="text" id="orderId" placeholder="Optional"></div></div><label>Description</label><textarea id="description" placeholder="Describe your issue in detail..." rows="4">The product I purchased from your company has quality issues. It does not match the description and cannot be used properly. I have tried contacting support but have not received a satisfactory resolution.</textarea><div class="btn-row"><button class="btn btn-primary" onclick="generate()">✍️ Generate Letter</button><button class="btn btn-success" id="copyBtn" style="display:none" onclick="copyLetter()">📋 Copy</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📄 Generated Letter</h2><div class="result-box" id="letterOutput"></div></div>
<script>function generate(){const type=document.getElementById('type').value;const recipient=document.getElementById('recipient').value||'Customer Service';const sender=document.getElementById('senderName').value||'Valued Customer';const orderId=document.getElementById('orderId').value;const desc=document.getElementById('description').value||'[Please describe your issue]';const date=new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});const typeLabels={product:'Product Issue',service:'Service Issue',billing:'Billing Dispute',delivery:'Delivery Issue',quality:'Quality Issue',refund:'Refund Request'};let letter=`${date}

To: ${recipient}

Subject: Formal Complaint Regarding ${typeLabels[type]}

Dear ${recipient},

I am writing to formally file a complaint regarding the following matter:

${orderId?`Reference Number: ${orderId}\n`:''}Issue Description: ${desc}

Based on the above, I request the following:
1. An investigation into this matter with a reasonable explanation;
2. ${type==='refund'?'A full refund':'Appropriate resolution, including but not limited to replacement, repair, or compensation'};
3. A written response within 7 business days of receiving this letter.

If this matter is not resolved within a reasonable timeframe, I will escalate to consumer protection agencies and pursue legal remedies as appropriate.

I look forward to your prompt response.

Sincerely,

${sender}
Phone: [Please fill in]
Email: [Please fill in]
${date}`;
document.getElementById('letterOutput').textContent=letter;
document.getElementById('resultCard').style.display='block';
document.getElementById('copyBtn').style.display='inline-block';
toast('Letter generated successfully');}
async function copyLetter(){const t=document.getElementById('letterOutput').textContent;await navigator.clipboard.writeText(t);toast('Copied to clipboard');}</script>""",
    },
    {
        "slug": "investment-return",
        "name_zh": "投资回报计算器",
        "name_en": "Investment Return Calculator",
        "desc_zh": "免费在线投资回报计算器，计算复利投资收益。支持定期定额投资、一次性投资，考虑年化收益率和通货膨胀率，可视化展示投资增长曲线。",
        "desc_en": "Free online investment return calculator - compute compound interest returns. Supports regular investments and lump sum, considers annual return rate and inflation. Visualize investment growth curve.",
        "icon_zh": "📈", "icon_en": "📈",
        "html_zh": """<div class="card"><h2>📊 投资参数</h2><div class="row"><div class="field"><label>初始投资 (元)</label><input type="number" id="initial" value="10000" min="0" step="1000"></div><div class="field"><label>每月追加 (元)</label><input type="number" id="monthly" value="1000" min="0" step="100"></div></div><div class="row"><div class="field"><label>年化收益率 (%)</label><input type="number" id="returnRate" value="8" min="0" step="0.1"></div><div class="field"><label>通货膨胀率 (%)</label><input type="number" id="inflation" value="3" min="0" step="0.1"></div><div class="field"><label>投资年限</label><input type="number" id="years" value="20" min="1" max="50" step="1"></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calc()">📊 计算</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📊 投资回报分析</h2><div id="summaryGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px"></div><canvas id="chart" style="width:100%;height:300px;background:#0f172a;border-radius:8px"></canvas></div>
<script>function formatMoney(n){return n.toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');}function calc(){const P=parseFloat(document.getElementById('initial').value)||0;const M=parseFloat(document.getElementById('monthly').value)||0;const r=parseFloat(document.getElementById('returnRate').value)/100/12;const inf=parseFloat(document.getElementById('inflation').value)/100;const yrs=parseInt(document.getElementById('years').value);const n=yrs*12;if(n<=0){toast('请输入有效参数');return;}let total=P;let invested=P;for(let i=0;i<n;i++){total=total*(1+r)+M;invested+=M;}const realReturn=total/(Math.pow(1+inf,yrs));document.getElementById('summaryGrid').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">总投资额</div><div style="color:#e2e8f0;font-size:1.5rem;font-weight:bold">¥${formatMoney(invested)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">最终资产</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">¥${formatMoney(total)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">投资收益</div><div style="color:#4ade80;font-size:1.5rem;font-weight:bold">¥${formatMoney(total-invested)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">实际购买力</div><div style="color:#f59e0b;font-size:1.5rem;font-weight:bold">¥${formatMoney(realReturn)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">年化回报率</div><div style="color:#a78bfa;font-size:1.5rem;font-weight:bold">${(Math.pow(total/invested,1/yrs)*100-100).toFixed(2)}%</div></div>`;const canvas=document.getElementById('chart');const ctx=canvas.getContext('2d');canvas.width=canvas.parentElement.clientWidth;canvas.height=300;const w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);let values=[];let val=P;for(let i=0;i<=n;i++){values.push(val);val=val*(1+r)+M;}const maxVal=Math.max(...values);const padX=50,padY=30;ctx.strokeStyle='rgba(148,163,184,.2)';ctx.lineWidth=1;for(let i=0;i<=4;i++){const y=padY+(h-padY*2)*i/4;ctx.beginPath();ctx.moveTo(padX,y);ctx.lineTo(w-padX,y);ctx.stroke();ctx.fillStyle='#64748b';ctx.font='10px sans-serif';ctx.fillText('¥'+formatMoney(maxVal*(4-i)/4),5,y+3);}ctx.strokeStyle='#22d3ee';ctx.lineWidth=2;ctx.beginPath();for(let i=0;i<values.length;i++){const x=padX+(w-padX*2)*i/(values.length-1);const y=padY+(h-padY*2)*(1-values[i]/maxVal);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();ctx.fillStyle='#22d3ee';const lastX=padX+(w-padX*2);const lastY=padY+(h-padY*2)*(1-values[values.length-1]/maxVal);ctx.beginPath();ctx.arc(lastX,lastY,5,0,Math.PI*2);ctx.fill();document.getElementById('resultCard').style.display='block';toast('计算完成');}</script>""",
        "html_en": """<div class="card"><h2>📊 Investment Parameters</h2><div class="row"><div class="field"><label>Initial Investment ($)</label><input type="number" id="initial" value="10000" min="0" step="1000"></div><div class="field"><label>Monthly Addition ($)</label><input type="number" id="monthly" value="500" min="0" step="100"></div></div><div class="row"><div class="field"><label>Annual Return (%)</label><input type="number" id="returnRate" value="8" min="0" step="0.1"></div><div class="field"><label>Inflation Rate (%)</label><input type="number" id="inflation" value="3" min="0" step="0.1"></div><div class="field"><label>Investment Period (years)</label><input type="number" id="years" value="20" min="1" max="50" step="1"></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calc()">📊 Calculate</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📊 Return Analysis</h2><div id="summaryGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px"></div><canvas id="chart" style="width:100%;height:300px;background:#0f172a;border-radius:8px"></canvas></div>
<script>function formatMoney(n){return n.toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');}function calc(){const P=parseFloat(document.getElementById('initial').value)||0;const M=parseFloat(document.getElementById('monthly').value)||0;const r=parseFloat(document.getElementById('returnRate').value)/100/12;const inf=parseFloat(document.getElementById('inflation').value)/100;const yrs=parseInt(document.getElementById('years').value);const n=yrs*12;if(n<=0){toast('Please enter valid parameters');return;}let total=P;let invested=P;for(let i=0;i<n;i++){total=total*(1+r)+M;invested+=M;}const realReturn=total/(Math.pow(1+inf,yrs));document.getElementById('summaryGrid').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Total Invested</div><div style="color:#e2e8f0;font-size:1.5rem;font-weight:bold">$${formatMoney(invested)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Final Value</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">$${formatMoney(total)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Total Return</div><div style="color:#4ade80;font-size:1.5rem;font-weight:bold">$${formatMoney(total-invested)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Real Purchasing Power</div><div style="color:#f59e0b;font-size:1.5rem;font-weight:bold">$${formatMoney(realReturn)}</div></div>`;const canvas=document.getElementById('chart');const ctx=canvas.getContext('2d');canvas.width=canvas.parentElement.clientWidth;canvas.height=300;const w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);let values=[];let val=P;for(let i=0;i<=n;i++){values.push(val);val=val*(1+r)+M;}const maxVal=Math.max(...values);const padX=50,padY=30;ctx.strokeStyle='rgba(148,163,184,.2)';ctx.lineWidth=1;for(let i=0;i<=4;i++){const y=padY+(h-padY*2)*i/4;ctx.beginPath();ctx.moveTo(padX,y);ctx.lineTo(w-padX,y);ctx.stroke();ctx.fillStyle='#64748b';ctx.font='10px sans-serif';ctx.fillText('$'+formatMoney(maxVal*(4-i)/4),5,y+3);}ctx.strokeStyle='#22d3ee';ctx.lineWidth=2;ctx.beginPath();for(let i=0;i<values.length;i++){const x=padX+(w-padX*2)*i/(values.length-1);const y=padY+(h-padY*2)*(1-values[i]/maxVal);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();ctx.fillStyle='#22d3ee';const lastX=padX+(w-padX*2);const lastY=padY+(h-padY*2)*(1-values[values.length-1]/maxVal);ctx.beginPath();ctx.arc(lastX,lastY,5,0,Math.PI*2);ctx.fill();document.getElementById('resultCard').style.display='block';toast('Calculation complete');}</script>""",
    },
    {
        "slug": "animation-generator",
        "name_zh": "CSS动画生成器",
        "name_en": "CSS Animation Generator",
        "desc_zh": "免费在线CSS动画生成器，可视化创建CSS关键帧动画。支持淡入淡出、弹跳、旋转、滑动等多种动画效果，实时预览并一键复制CSS代码，适合前端开发者快速生成动画样式。",
        "desc_en": "Free online CSS animation generator - visually create CSS keyframe animations. Supports fade, bounce, rotate, slide and more effects. Live preview and one-click CSS copy. Perfect for frontend developers.",
        "icon_zh": "✨", "icon_en": "✨",
        "html_zh": """<div class="card"><h2>🎬 动画预览</h2><div style="text-align:center;padding:40px 0"><div id="animBox" style="width:80px;height:80px;background:linear-gradient(135deg,#06b6d4,#a78bfa);border-radius:12px;margin:0 auto;transition:none"></div></div></div><div class="card"><h2>⚙️ 动画设置</h2><div class="row"><div class="field"><label>动画类型</label><select id="animType" onchange="updateAnim()"><option value="bounce">弹跳</option><option value="fadeIn">淡入</option><option value="fadeOut">淡出</option><option value="rotate">旋转</option><option value="slideRight">右滑入</option><option value="slideLeft">左滑入</option><option value="slideUp">上滑入</option><option value="pulse">脉冲</option><option value="shake">抖动</option><option value="flip">翻转</option></select></div><div class="field"><label>持续时间 (秒)</label><input type="number" id="duration" value="1" min="0.1" max="10" step="0.1" onchange="updateAnim()"></div><div class="field"><label>重复次数</label><select id="iteration" onchange="updateAnim()"><option value="infinite">无限循环</option><option value="1">1次</option><option value="2">2次</option><option value="3">3次</option><option value="5">5次</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="applyAnim()">▶️ 播放预览</button><button class="btn btn-success" onclick="copyCSS()">📋 复制CSS代码</button></div></div><div class="card" id="codeCard" style="display:none"><h2>📄 生成的CSS</h2><div class="result-box" id="cssOutput"></div></div>
<script>const keyframes={bounce:'@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}',fadeIn:'@keyframes fadeIn{0%{opacity:0}100%{opacity:1}}',fadeOut:'@keyframes fadeOut{0%{opacity:1}100%{opacity:0}}',rotate:'@keyframes rotate{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}',slideRight:'@keyframes slideRight{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}',slideLeft:'@keyframes slideLeft{0%{transform:translateX(100px);opacity:0}100%{transform:translateX(0);opacity:1}}',slideUp:'@keyframes slideUp{0%{transform:translateY(50px);opacity:0}100%{transform:translateY(0);opacity:1}}',pulse:'@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}',shake:'@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}',flip:'@keyframes flip{0%{transform:perspective(400px) rotateY(0)}100%{transform:perspective(400px) rotateY(360deg)}}'};function updateAnim(){const box=document.getElementById('animBox');box.style.animation='none';box.offsetHeight;}function applyAnim(){const type=document.getElementById('animType').value;const dur=document.getElementById('duration').value;const iter=document.getElementById('iteration').value;const box=document.getElementById('animBox');const style=document.createElement('style');style.id='animStyle';const old=document.getElementById('animStyle');if(old)old.remove();style.textContent=keyframes[type];document.head.appendChild(style);box.style.animation=`${type} ${dur}s ease-in-out ${iter}`;const cssCode=`/* CSS Animation: ${type} */\\n${keyframes[type]}\\n\\n.element {\\n  animation: ${type} ${dur}s ease-in-out ${iter};\\n}`;document.getElementById('cssOutput').textContent=cssCode;document.getElementById('codeCard').style.display='block';}async function copyCSS(){const t=document.getElementById('cssOutput').textContent;await navigator.clipboard.writeText(t);toast('CSS已复制到剪贴板');}</script>""",
        "html_en": """<div class="card"><h2>🎬 Preview</h2><div style="text-align:center;padding:40px 0"><div id="animBox" style="width:80px;height:80px;background:linear-gradient(135deg,#06b6d4,#a78bfa);border-radius:12px;margin:0 auto;transition:none"></div></div></div><div class="card"><h2>⚙️ Settings</h2><div class="row"><div class="field"><label>Animation Type</label><select id="animType" onchange="updateAnim()"><option value="bounce">Bounce</option><option value="fadeIn">Fade In</option><option value="fadeOut">Fade Out</option><option value="rotate">Rotate</option><option value="slideRight">Slide Right</option><option value="slideLeft">Slide Left</option><option value="slideUp">Slide Up</option><option value="pulse">Pulse</option><option value="shake">Shake</option><option value="flip">Flip</option></select></div><div class="field"><label>Duration (seconds)</label><input type="number" id="duration" value="1" min="0.1" max="10" step="0.1" onchange="updateAnim()"></div><div class="field"><label>Iterations</label><select id="iteration" onchange="updateAnim()"><option value="infinite">Infinite</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="5">5</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="applyAnim()">▶️ Play</button><button class="btn btn-success" onclick="copyCSS()">📋 Copy CSS</button></div></div><div class="card" id="codeCard" style="display:none"><h2>📄 Generated CSS</h2><div class="result-box" id="cssOutput"></div></div>
<script>const keyframes={bounce:'@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}',fadeIn:'@keyframes fadeIn{0%{opacity:0}100%{opacity:1}}',fadeOut:'@keyframes fadeOut{0%{opacity:1}100%{opacity:0}}',rotate:'@keyframes rotate{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}',slideRight:'@keyframes slideRight{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}',slideLeft:'@keyframes slideLeft{0%{transform:translateX(100px);opacity:0}100%{transform:translateX(0);opacity:1}}',slideUp:'@keyframes slideUp{0%{transform:translateY(50px);opacity:0}100%{transform:translateY(0);opacity:1}}',pulse:'@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}',shake:'@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}',flip:'@keyframes flip{0%{transform:perspective(400px) rotateY(0)}100%{transform:perspective(400px) rotateY(360deg)}}'};function updateAnim(){const box=document.getElementById('animBox');box.style.animation='none';box.offsetHeight;}function applyAnim(){const type=document.getElementById('animType').value;const dur=document.getElementById('duration').value;const iter=document.getElementById('iteration').value;const box=document.getElementById('animBox');const style=document.createElement('style');style.id='animStyle';const old=document.getElementById('animStyle');if(old)old.remove();style.textContent=keyframes[type];document.head.appendChild(style);box.style.animation=`${type} ${dur}s ease-in-out ${iter}`;const cssCode=`/* CSS Animation: ${type} */\\n${keyframes[type]}\\n\\n.element {\\n  animation: ${type} ${dur}s ease-in-out ${iter};\\n}`;document.getElementById('cssOutput').textContent=cssCode;document.getElementById('codeCard').style.display='block';}async function copyCSS(){const t=document.getElementById('cssOutput').textContent;await navigator.clipboard.writeText(t);toast('CSS copied to clipboard');}</script>""",
    },
]

for t in tools:
    slug = t['slug']
    zh_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, 'en', slug)
    os.makedirs(zh_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    meta_zh = make_meta_zh(t['name_zh'], t['desc_zh'], slug, t['name_zh'])
    schema_zh = make_schema_zh(t['name_zh'], t['desc_zh'], slug)
    info_zh = f"""<div class="info-section"><h2>关于{t['name_zh']}</h2><p>{t['desc_zh']}</p></div>"""
    
    html_zh = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
{GA_HEAD}
{meta_zh}
<script type="application/ld+json">{schema_zh}</script>
<style>
{CSS}
</head>
<body>
<div class="container">
<div class="header"><h1>{t['icon_zh']} {t['name_zh']}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {t['name_zh']}</p>
<div class="hero"><p>{t['desc_zh']} | 无需注册 · 数据绝不上传服务器</p><span class="badge">零依赖·可离线使用</span></div>
{t['html_zh']}
{info_zh}
<div class="footer"><p>© 2025 Free ToolBase · <a href="../index.html">首页</a> · <a href="../en/{slug}/">English</a></p></div>
</div>
<div id="toast"></div>
<script>function toast(m){{const e=document.getElementById('toast');e.textContent=m;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),2000);}}</script>
</body>
</html>"""
    
    meta_en = make_meta_en(t['name_en'], t['desc_en'], slug, t['name_en'])
    schema_en = make_schema_en(t['name_en'], t['desc_en'], slug)
    info_en = f"""<div class="info-section"><h2>About {t['name_en']}</h2><p>{t['desc_en']}</p></div>"""
    
    html_en = f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA_HEAD}
{meta_en}
<script type="application/ld+json">{schema_en}</script>
<style>
{CSS}
</head>
<body>
<div class="container">
<div class="header"><h1>{t['icon_en']} {t['name_en']}</h1><div class="lang-switch"><a href="../../{slug}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {t['name_en']}</p>
<div class="hero"><p>{t['desc_en']} | No sign-up · Data never leaves your device</p><span class="badge">Zero-dependency · Works offline</span></div>
{t['html_en']}
{info_en}
<div class="footer"><p>© 2025 Free ToolBase · <a href="../index.html">Home</a> · <a href="../../{slug}/">中文</a></p></div>
</div>
<div id="toast"></div>
<script>function toast(m){{const e=document.getElementById('toast');e.textContent=m;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),2000);}}</script>
</body>
</html>"""
    
    with open(os.path.join(zh_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_zh)
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_en)
    print(f"  ✓ {slug}")

print(f"\n完成！共生成 {len(tools)} 个工具")