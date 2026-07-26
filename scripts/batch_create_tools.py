#!/usr/bin/env python3
"""批量创建新工具页面"""
import os, json

TOOLS = [
    {
        "slug": "capm-calculator",
        "icon_cn": "📈", "icon_en": "📈",
        "name_cn": "CAPM资本资产定价计算器",
        "name_en": "CAPM Calculator",
        "desc_cn": "使用资本资产定价模型计算期望收益率。输入无风险利率、市场收益率和贝塔系数，一键得出资产合理回报。",
        "desc_en": "Calculate expected return using the Capital Asset Pricing Model. Input risk-free rate, market return and beta to get fair asset return.",
        "keywords_cn": "CAPM计算器,资本资产定价模型,期望收益率,贝塔系数,无风险利率,市场溢价,投资估值,金融计算器",
        "keywords_en": "CAPM calculator,Capital Asset Pricing Model,expected return,beta,risk-free rate,market premium,investment valuation,financial calculator",
        "category": "finance-tools",
        "inputs": [
            {"id": "riskFreeRate", "label_cn": "无风险利率 (%)", "label_en": "Risk-Free Rate (%)", "default": "4.0", "type": "number", "step": "0.01"},
            {"id": "marketReturn", "label_cn": "市场期望收益率 (%)", "label_en": "Expected Market Return (%)", "default": "10.0", "type": "number", "step": "0.01"},
            {"id": "beta", "label_cn": "贝塔系数 (β)", "label_en": "Beta (β)", "default": "1.2", "type": "number", "step": "0.01"}
        ],
        "calc": """
    const rf = parseFloat(riskFreeRate.value) || 0;
    const rm = parseFloat(marketReturn.value) || 0;
    const b = parseFloat(beta.value) || 0;
    const capm = rf + b * (rm - rf);
    const marketPremium = rm - rf;
    document.getElementById('expectedReturn').textContent = capm.toFixed(2) + '%';
    document.getElementById('marketPremium').textContent = (marketPremium >= 0 ? '+' : '') + marketPremium.toFixed(2) + '%';
    document.getElementById('riskPremium').textContent = (b * marketPremium >= 0 ? '+' : '') + (b * marketPremium).toFixed(2) + '%';
"""
    },
    {
        "slug": "sharpe-ratio",
        "icon_cn": "📊", "icon_en": "📊",
        "name_cn": "夏普比率计算器",
        "name_en": "Sharpe Ratio Calculator",
        "desc_cn": "计算投资组合的夏普比率，衡量风险调整后的收益。输入组合收益率、无风险利率和标准差，评估投资效率。",
        "desc_en": "Calculate the Sharpe Ratio of your investment portfolio to measure risk-adjusted returns. Input portfolio return, risk-free rate and standard deviation.",
        "keywords_cn": "夏普比率,风险调整收益,投资组合,标准差,夏普指数,金融计算器,投资效率",
        "keywords_en": "Sharpe ratio,risk-adjusted return,portfolio,standard deviation,Sharpe index,financial calculator,investment efficiency",
        "category": "finance-tools",
        "inputs": [
            {"id": "portfolioReturn", "label_cn": "投资组合年化收益率 (%)", "label_en": "Portfolio Annual Return (%)", "default": "12.0", "type": "number", "step": "0.01"},
            {"id": "riskFreeRate", "label_cn": "无风险利率 (%)", "label_en": "Risk-Free Rate (%)", "default": "4.0", "type": "number", "step": "0.01"},
            {"id": "stdDev", "label_cn": "年化标准差 (%)", "label_en": "Annual Std Deviation (%)", "default": "15.0", "type": "number", "step": "0.01"}
        ],
        "calc": """
    const rp = parseFloat(portfolioReturn.value) || 0;
    const rf = parseFloat(riskFreeRate.value) || 0;
    const sd = parseFloat(stdDev.value) || 0;
    if (sd === 0) { document.getElementById('sharpe').textContent = 'N/A（标准差为0）'; document.getElementById('excessReturn').textContent = '0.00%'; return; }
    const excess = rp - rf;
    const sharpe = excess / sd;
    document.getElementById('sharpe').textContent = sharpe.toFixed(4);
    document.getElementById('excessReturn').textContent = (excess >= 0 ? '+' : '') + excess.toFixed(2) + '%';
    let rating = sharpe < 0 ? '❌ 负值（低于无风险收益）' : sharpe < 0.5 ? '⚠️ 较差' : sharpe < 1.0 ? '📊 一般' : sharpe < 2.0 ? '✅ 良好' : sharpe < 3.0 ? '🌟 优秀' : '🏆 卓越';
    document.getElementById('rating').textContent = rating;
"""
    },
    {
        "slug": "beta-calculator",
        "icon_cn": "📉", "icon_en": "📉",
        "name_cn": "贝塔系数计算器",
        "name_en": "Beta Calculator",
        "desc_cn": "计算股票/资产的贝塔系数，衡量系统性风险。输入资产收益率和市场收益率序列，自动计算β值和R²。",
        "desc_en": "Calculate Beta coefficient for stocks/assets to measure systematic risk. Input asset and market return series to compute β and R².",
        "keywords_cn": "贝塔系数,系统风险,股票波动率,CAPM,回归分析,金融计算器,β系数",
        "keywords_en": "Beta coefficient,systematic risk,stock volatility,CAPM,regression,financial calculator,beta",
        "category": "finance-tools",
        "inputs": [
            {"id": "assetReturns", "label_cn": "资产月收益率 (% 每行一个)", "label_en": "Asset Monthly Returns (% one per line)", "default": "5.2\n-2.1\n3.8\n-1.5\n4.0\n0.5\n-3.2\n6.1\n2.3\n-0.8\n1.9\n4.5", "type": "textarea"},
            {"id": "marketReturns", "label_cn": "市场月收益率 (% 每行一个)", "label_en": "Market Monthly Returns (% one per line)", "default": "3.0\n-1.2\n2.5\n-0.8\n2.8\n0.3\n-2.0\n4.5\n1.5\n-0.5\n1.2\n3.8", "type": "textarea"}
        ],
        "calc": """
    const assetRaw = assetReturns.value.trim().split(/[\\n,]+/).map(v => parseFloat(v)).filter(v => !isNaN(v));
    const marketRaw = marketReturns.value.trim().split(/[\\n,]+/).map(v => parseFloat(v)).filter(v => !isNaN(v));
    const n = Math.min(assetRaw.length, marketRaw.length);
    if (n < 2) { document.getElementById('beta').textContent = '需要至少2组数据'; return; }
    const asset = assetRaw.slice(0, n);
    const market = marketRaw.slice(0, n);
    const meanA = asset.reduce((a,b) => a+b, 0) / n;
    const meanM = market.reduce((a,b) => a+b, 0) / n;
    let cov = 0, varM = 0, varA = 0;
    for (let i = 0; i < n; i++) {
        cov += (asset[i] - meanA) * (market[i] - meanM);
        varM += (market[i] - meanM) ** 2;
        varA += (asset[i] - meanA) ** 2;
    }
    const betaVal = varM === 0 ? 0 : cov / varM;
    const r2 = (varA * varM === 0) ? 0 : (cov ** 2) / (varA * varM);
    document.getElementById('beta').textContent = betaVal.toFixed(4);
    document.getElementById('r2').textContent = (r2 * 100).toFixed(1) + '%';
    document.getElementById('correlation').textContent = Math.sqrt(Math.max(0, r2)).toFixed(4);
    let interp = betaVal < 0 ? '🔄 负相关（对冲特性）' : betaVal < 0.5 ? '🛡️ 低风险（防御型）' : betaVal < 1.0 ? '📊 低于市场波动' : betaVal === 1.0 ? '⚖️ 与市场同步' : betaVal < 1.5 ? '📈 略高于市场' : betaVal < 2.0 ? '🔥 高波动' : '🚀 极高波动';
    document.getElementById('interpretation').textContent = interp;
    document.getElementById('dataPoints').textContent = n;
"""
    },
    {
        "slug": "dividend-calculator",
        "icon_cn": "💸", "icon_en": "💸",
        "name_cn": "股息收益计算器",
        "name_en": "Dividend Yield Calculator",
        "desc_cn": "计算股票股息收益率和年化分红收入。输入股价、每股股息和持股数量，一键评估股息投资回报。",
        "desc_en": "Calculate dividend yield and annual dividend income. Input stock price, dividend per share and shares held to evaluate dividend returns.",
        "keywords_cn": "股息计算器,股息率,分红收益,股票分红,每股股息,投资回报,金融计算器",
        "keywords_en": "dividend calculator,dividend yield,stock dividend,income investing,per share dividend,investment return,financial calculator",
        "category": "finance-tools",
        "inputs": [
            {"id": "stockPrice", "label_cn": "当前股价 (元)", "label_en": "Current Stock Price ($)", "default": "100.00", "type": "number", "step": "0.01"},
            {"id": "dividendPerShare", "label_cn": "每股年度股息 (元)", "label_en": "Annual Dividend Per Share ($)", "default": "3.50", "type": "number", "step": "0.01"},
            {"id": "shares", "label_cn": "持股数量", "label_en": "Number of Shares", "default": "1000", "type": "number", "step": "1"}
        ],
        "calc": """
    const price = parseFloat(stockPrice.value) || 0;
    const dps = parseFloat(dividendPerShare.value) || 0;
    const qty = parseFloat(shares.value) || 0;
    if (price <= 0) { document.getElementById('yield').textContent = 'N/A'; return; }
    const yieldVal = (dps / price) * 100;
    const annualIncome = dps * qty;
    const monthlyIncome = annualIncome / 12;
    document.getElementById('yield').textContent = yieldVal.toFixed(2) + '%';
    document.getElementById('annualIncome').textContent = formatMoney(annualIncome);
    document.getElementById('monthlyIncome').textContent = formatMoney(monthlyIncome);
    document.getElementById('totalInvestment').textContent = formatMoney(price * qty);
    document.getElementById('payoutRatio').textContent = price > 0 ? (dps / price * 100).toFixed(2) + '%' : 'N/A';
"""
    },
    {
        "slug": "debt-payoff-calculator",
        "icon_cn": "💳", "icon_en": "💳",
        "name_cn": "债务清偿计算器",
        "name_en": "Debt Payoff Calculator",
        "desc_cn": "制定债务清偿计划，计算还清时间和总利息。输入债务本金、年利率和每月还款额，对比不同还款策略。",
        "desc_en": "Create a debt payoff plan. Input principal, APR and monthly payment to calculate payoff time and total interest. Compare strategies.",
        "keywords_cn": "债务清偿,还债计划,信用卡还款,贷款还清,利息计算,债务管理,金融计算器",
        "keywords_en": "debt payoff,repayment plan,credit card payoff,loan repayment,interest calculator,debt management,financial calculator",
        "category": "finance-tools",
        "inputs": [
            {"id": "principal", "label_cn": "债务本金 (元)", "label_en": "Principal ($)", "default": "50000", "type": "number", "step": "100"},
            {"id": "annualRate", "label_cn": "年利率 (%)", "label_en": "APR (%)", "default": "18.0", "type": "number", "step": "0.01"},
            {"id": "monthlyPayment", "label_cn": "每月还款额 (元)", "label_en": "Monthly Payment ($)", "default": "2000", "type": "number", "step": "100"}
        ],
        "calc": """
    const p = parseFloat(principal.value) || 0;
    const r = parseFloat(annualRate.value) || 0;
    const m = parseFloat(monthlyPayment.value) || 0;
    if (p <= 0 || r <= 0 || m <= 0) { document.getElementById('payoffMonths').textContent = '请输入有效数值'; return; }
    const monthlyRate = r / 100 / 12;
    if (m <= p * monthlyRate) { document.getElementById('payoffMonths').textContent = '⚠️ 月供不足以覆盖利息，债务将永远无法还清！'; document.getElementById('totalInterest').textContent = '∞'; return; }
    let balance = p, months = 0, totalInt = 0;
    while (balance > 0 && months < 1200) {
        const interest = balance * monthlyRate;
        totalInt += interest;
        const principalPayment = Math.min(m - interest, balance);
        balance -= principalPayment;
        months++;
    }
    const years = Math.floor(months / 12);
    const remainingMonths = months % 12;
    document.getElementById('payoffMonths').textContent = months + ' 个月 (' + years + '年' + (remainingMonths > 0 ? remainingMonths + '个月' : '') + ')';
    document.getElementById('totalInterest').textContent = formatMoney(totalInt);
    document.getElementById('totalPayment').textContent = formatMoney(p + totalInt);
    document.getElementById('interestRatio').textContent = (totalInt / (p + totalInt) * 100).toFixed(1) + '%';
    // 对比：如果每月多还10%
    let bal2 = p, m2 = 0, int2 = 0;
    const mp2 = m * 1.1;
    while (bal2 > 0 && m2 < 1200) {
        const interest2 = bal2 * monthlyRate;
        int2 += interest2;
        bal2 -= Math.min(mp2 - interest2, bal2);
        m2++;
    }
    document.getElementById('fastPayoff').textContent = m2 + ' 个月（节省 ' + formatMoney(totalInt - int2) + '）';
"""
    }
]

# HTML模板
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#f8fafc;color:#1e293b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#4F46E5;text-decoration:none}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.6rem}.lang-switch{display:flex;gap:4px;background:#fff;border-radius:8px;padding:4px;border:1px solid #e2e8f0}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#64748b}.lang-switch a.active{background:#EEF2FF;color:#4F46E5;font-weight:600}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.nav-back a:hover{color:#4F46E5}.hero{background:linear-gradient(135deg,#EEF2FF 0%,#E0E7FF 100%);border-radius:12px;padding:20px 24px;margin-bottom:20px;font-size:.95rem;color:#3730A3;line-height:1.7}.hero .badge{display:inline-block;background:#4F46E5;color:#fff;padding:3px 10px;border-radius:20px;font-size:.75rem;margin-top:8px}.panel{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.1)}.panel-title{font-size:1.1rem;margin-bottom:14px;font-weight:600}.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}.btn-primary{background:#4F46E5;color:#fff}.btn-primary:hover{opacity:.9;transform:translateY(-1px)}.btn-secondary{background:#fff;color:#1e293b;border:1px solid #e2e8f0}.btn-secondary:hover{background:#f8fafc}.btn-large{padding:12px 32px;font-size:1.1rem;font-weight:600}.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}input,select,textarea{padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;background:#fff;color:#1e293b;font-size:.9rem;width:100%}input:focus,select:focus,textarea:focus{outline:none;border-color:#4F46E5;box-shadow:0 0 0 3px rgba(79,70,229,.1)}.input-group{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:8px}.input-group label{display:block;font-size:.85rem;color:#64748b;margin-bottom:4px}.result-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:16px}.result-item{background:#f8fafc;border-radius:8px;padding:16px;text-align:center;border:1px solid #e2e8f0}.result-item .val{font-size:1.6rem;font-weight:700;color:#4F46E5}.result-item .lbl{font-size:.8rem;color:#64748b;margin-top:4px}.result-main{text-align:center;padding:24px;background:linear-gradient(135deg,#EEF2FF,#E0E7FF);border-radius:12px;margin-bottom:16px}.result-main .val{font-size:2.4rem;font-weight:800;color:#3730A3}.result-main .lbl{font-size:.9rem;color:#6366f1;margin-top:4px}.copy-btn{display:inline-flex;align-items:center;gap:4px;padding:6px 12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.25);border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s;margin-left:8px;vertical-align:top}.copy-btn:hover{background:rgba(6,182,212,.25)}.copy-btn.copied{background:rgba(34,197,94,.15);color:#22c55e;border-color:rgba(34,197,94,.3)}footer{text-align:center;padding:24px 0;color:#94a3b8;font-size:.85rem;margin-top:20px}footer a{color:#94a3b8}.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 24px;border-radius:20px;font-size:.9rem;opacity:0;transition:opacity .3s;z-index:9999;pointer-events:none}.toast.show{opacity:1}@media(max-width:600px){.header h1{font-size:1.3rem}.container{padding:16px 12px}.result-main .val{font-size:1.8rem}}"""


def generate_tool(tool, lang, lang_attr):
    """生成工具页面HTML"""
    name = tool[f'name_{lang}']
    desc = tool[f'desc_{lang}']
    keywords = tool[f'keywords_{lang}']
    icon = tool[f'icon_{lang}']
    slug = tool['slug']
    
    # 输入HTML
    inputs_html = ''
    for inp in tool['inputs']:
        label = inp[f'label_{lang}']
        if inp['type'] == 'textarea':
            inputs_html += f'''    <div><label>{label}</label><textarea id="{inp['id']}" rows="6" style="resize:vertical;font-family:monospace">{inp['default']}</textarea></div>\n'''
        else:
            step = inp.get('step', '1')
            inputs_html += f'''    <div><label>{label}</label><input type="number" id="{inp['id']}" value="{inp['default']}" step="{step}"></div>\n'''
    
    # 结果HTML根据工具不同
    result_html = {
        'capm-calculator': {
            'cn': '''  <div class="result-main"><div class="lbl">期望收益率 (CAPM)</div><div class="val" id="expectedReturn">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="marketPremium">—</div><div class="lbl">市场风险溢价</div></div>
    <div class="result-item"><div class="val" id="riskPremium">—</div><div class="lbl">资产风险溢价</div></div>
  </div>''',
            'en': '''  <div class="result-main"><div class="lbl">Expected Return (CAPM)</div><div class="val" id="expectedReturn">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="marketPremium">—</div><div class="lbl">Market Risk Premium</div></div>
    <div class="result-item"><div class="val" id="riskPremium">—</div><div class="lbl">Asset Risk Premium</div></div>
  </div>'''
        },
        'sharpe-ratio': {
            'cn': '''  <div class="result-main"><div class="lbl">夏普比率</div><div class="val" id="sharpe">—</div><div style="margin-top:8px;font-size:1.2rem" id="rating"></div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="excessReturn">—</div><div class="lbl">超额收益率</div></div>
  </div>''',
            'en': '''  <div class="result-main"><div class="lbl">Sharpe Ratio</div><div class="val" id="sharpe">—</div><div style="margin-top:8px;font-size:1.2rem" id="rating"></div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="excessReturn">—</div><div class="lbl">Excess Return</div></div>
  </div>'''
        },
        'beta-calculator': {
            'cn': '''  <div class="result-main"><div class="lbl">贝塔系数 (β)</div><div class="val" id="beta">—</div><div style="margin-top:8px;font-size:1rem;color:#6366f1" id="interpretation"></div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="r2">—</div><div class="lbl">R² 拟合度</div></div>
    <div class="result-item"><div class="val" id="correlation">—</div><div class="lbl">相关系数</div></div>
    <div class="result-item"><div class="val" id="dataPoints">—</div><div class="lbl">数据点数</div></div>
  </div>''',
            'en': '''  <div class="result-main"><div class="lbl">Beta Coefficient (β)</div><div class="val" id="beta">—</div><div style="margin-top:8px;font-size:1rem;color:#6366f1" id="interpretation"></div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="r2">—</div><div class="lbl">R² (Goodness of Fit)</div></div>
    <div class="result-item"><div class="val" id="correlation">—</div><div class="lbl">Correlation</div></div>
    <div class="result-item"><div class="val" id="dataPoints">—</div><div class="lbl">Data Points</div></div>
  </div>'''
        },
        'dividend-calculator': {
            'cn': '''  <div class="result-main"><div class="lbl">股息收益率</div><div class="val" id="yield">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="annualIncome">—</div><div class="lbl">年度分红收入</div></div>
    <div class="result-item"><div class="val" id="monthlyIncome">—</div><div class="lbl">月均分红收入</div></div>
    <div class="result-item"><div class="val" id="totalInvestment">—</div><div class="lbl">总投资金额</div></div>
    <div class="result-item"><div class="val" id="payoutRatio">—</div><div class="lbl">派息率</div></div>
  </div>''',
            'en': '''  <div class="result-main"><div class="lbl">Dividend Yield</div><div class="val" id="yield">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="annualIncome">—</div><div class="lbl">Annual Dividend Income</div></div>
    <div class="result-item"><div class="val" id="monthlyIncome">—</div><div class="lbl">Monthly Dividend Income</div></div>
    <div class="result-item"><div class="val" id="totalInvestment">—</div><div class="lbl">Total Investment</div></div>
    <div class="result-item"><div class="val" id="payoutRatio">—</div><div class="lbl">Payout Ratio</div></div>
  </div>'''
        },
        'debt-payoff-calculator': {
            'cn': '''  <div class="result-main"><div class="lbl">预计还清时间</div><div class="val" id="payoffMonths">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="totalInterest">—</div><div class="lbl">总利息</div></div>
    <div class="result-item"><div class="val" id="totalPayment">—</div><div class="lbl">总还款额</div></div>
    <div class="result-item"><div class="val" id="interestRatio">—</div><div class="lbl">利息占比</div></div>
  </div>
  <div class="panel" style="margin-top:12px;background:#F0FDF4;border-color:#BBF7D0">
    <div class="panel-title">💡 加速还款建议</div>
    <p style="font-size:.9rem">如果每月多还10%，可在 <strong id="fastPayoff">—</strong> 内还清。</p>
  </div>''',
            'en': '''  <div class="result-main"><div class="lbl">Estimated Payoff Time</div><div class="val" id="payoffMonths">—</div></div>
  <div class="result-grid">
    <div class="result-item"><div class="val" id="totalInterest">—</div><div class="lbl">Total Interest</div></div>
    <div class="result-item"><div class="val" id="totalPayment">—</div><div class="lbl">Total Payment</div></div>
    <div class="result-item"><div class="val" id="interestRatio">—</div><div class="lbl">Interest Ratio</div></div>
  </div>
  <div class="panel" style="margin-top:12px;background:#F0FDF4;border-color:#BBF7D0">
    <div class="panel-title">💡 Accelerated Payoff</div>
    <p style="font-size:.9rem">If you pay 10% more monthly, you can be debt-free in <strong id="fastPayoff">—</strong>.</p>
  </div>'''
        }
    }[slug][lang]

    # FAQ
    faq_cn = {
        'capm-calculator': [{"q":"什么是CAPM？","a":"CAPM（Capital Asset Pricing Model，资本资产定价模型）是金融学中用于计算资产期望收益率的经典模型。公式为：E(Ri) = Rf + β × (Rm - Rf)，其中Rf为无风险利率，β为贝塔系数，(Rm-Rf)为市场风险溢价。"},{"q":"贝塔系数β代表什么？","a":"β衡量资产相对于市场的波动性。β=1表示与市场同步波动；β>1表示波动大于市场（进攻型）；β<1表示波动小于市场（防御型）；β<0表示与市场反向波动。"},{"q":"无风险利率应该用多少？","a":"通常使用10年期国债收益率作为无风险利率的代理变量。不同国家不同时期数值不同，常见范围在2%-5%之间。"}],
        'sharpe-ratio': [{"q":"夏普比率多高算好？","a":"一般认为：<0为负（低于无风险收益），0-0.5较差，0.5-1.0一般，1.0-2.0良好，2.0-3.0优秀，>3.0卓越。但不同市场环境下标准不同。"},{"q":"夏普比率和索提诺比率的区别？","a":"夏普比率用标准差衡量总风险（上行+下行），索提诺比率只用下行标准差。对于偏态分布的投资组合，索提诺比率更能反映真实风险。"},{"q":"年化标准差怎么算？","a":"年化标准差 = 月收益率标准差 × √12。如果只有日收益率，则×√252。"}],
        'beta-calculator': [{"q":"贝塔系数怎么计算？","a":"β = Cov(Ri, Rm) / Var(Rm)，即资产收益率与市场收益率的协方差除以市场收益率的方差。本质上是OLS回归的斜率系数。"},{"q":"多少数据点足够计算β？","a":"一般建议至少36-60个月的月度收益率数据。数据太少则统计意义不足，R²偏低。"},{"q":"β=0是什么意思？","a":"β=0表示资产收益率与市场无关，理论上期望收益等于无风险利率。现实中很少有资产β严格为0。"}],
        'dividend-calculator': [{"q":"股息率多少算好？","a":"不同行业差异很大：公用事业/REITs通常3%-6%，科技股通常0%-1.5%，消费必需品2%-3%。高股息率（>8%）可能意味着股价大跌或股息不可持续。"},{"q":"派息率和股息率有什么区别？","a":"股息率=每股股息/股价，反映投资回报率；派息率=每股股息/EPS，反映公司将多少利润用于分红。"},{"q":"中国A股股息率一般多少？","a":"上证50成分股平均股息率约2.5%-3.5%，银行股可达4%-6%。港股通标的股息率普遍更高。"}],
        'debt-payoff-calculator': [{"q":"雪球法和雪崩法哪个更好？","a":"雪球法（先还最小余额）心理激励效果好；雪崩法（先还最高利率）数学上最优，总利息最少。本计算器展示的是固定月供策略。"},{"q":"为什么月供不足覆盖利息？","a":"当月还款额≤本金×月利率时，还款只够支付利息，本金永远不会减少。这就是信用卡最低还款陷阱——按最低还款还可能需要几十年才能还清。"},{"q":"提前还款划算吗？","a":"如果债务利率>投资收益率，提前还款更划算。信用卡（18%+）应优先还清；房贷（3%-5%）可考虑投资。"}]
    }[slug]
    
    faq_en = {
        'capm-calculator': [{"q":"What is CAPM?","a":"CAPM (Capital Asset Pricing Model) calculates expected return: E(Ri) = Rf + β × (Rm - Rf). Rf is risk-free rate, β is beta, and (Rm-Rf) is market risk premium. It's widely used in finance for asset pricing and portfolio management."},{"q":"What does Beta (β) mean?","a":"Beta measures volatility relative to the market. β=1 means moving with market; β>1 means more volatile (aggressive); β<1 means less volatile (defensive); β<0 means inverse movement."},{"q":"What risk-free rate should I use?","a":"Typically the 10-year government bond yield is used as a proxy. Values vary by country and period, commonly 2%-5%."}],
        'sharpe-ratio': [{"q":"What is a good Sharpe Ratio?","a":"Generally: <0 is poor (below risk-free), 0-0.5 suboptimal, 0.5-1.0 acceptable, 1.0-2.0 good, 2.0-3.0 excellent, >3.0 outstanding. Context matters by market environment."},{"q":"Sharpe vs Sortino Ratio?","a":"Sharpe uses total standard deviation (up+down), Sortino only uses downside deviation. For skewed distributions, Sortino better reflects true risk."},{"q":"How to annualize standard deviation?","a":"Annual σ = monthly σ × √12. For daily returns, multiply by √252."}],
        'beta-calculator': [{"q":"How is Beta calculated?","a":"β = Cov(Ri, Rm) / Var(Rm), the slope coefficient from OLS regression of asset returns on market returns."},{"q":"How many data points needed?","a":"Generally 36-60 months of monthly returns are recommended. Too few points lack statistical significance with low R²."},{"q":"What does β=0 mean?","a":"β=0 means the asset's returns are uncorrelated with the market. In theory, expected return equals the risk-free rate."}],
        'dividend-calculator': [{"q":"What is a good dividend yield?","a":"Varies by sector: Utilities/REITs 3-6%, Tech 0-1.5%, Consumer Staples 2-3%. Yields >8% may signal unsustainable dividends or falling stock price."},{"q":"Dividend Yield vs Payout Ratio?","a":"Dividend Yield = DPS/Price (investor return). Payout Ratio = DPS/EPS (how much profit is distributed)."},{"q":"Are dividends taxed?","a":"Yes, in most countries. US qualified dividends taxed at 0-20% capital gains rate. Tax treatment varies by jurisdiction."}],
        'debt-payoff-calculator': [{"q":"Snowball vs Avalanche method?","a":"Snowball (smallest balance first) provides psychological wins; Avalanche (highest APR first) is mathematically optimal. This calculator shows fixed monthly payment strategy."},{"q":"Why does minimum payment barely reduce debt?","a":"When payment ≤ principal × monthly rate, you only cover interest. This is the credit card minimum payment trap — it can take decades to pay off."},{"q":"Should I pay off debt or invest?","a":"Compare rates: if debt APR > expected investment return, prioritize payoff. Credit cards (18%+) should be paid first; mortgages (3-5%) may allow concurrent investing."}]
    }[slug]
    
    faq = faq_cn if lang == 'cn' else faq_en
    faq_json = json.dumps(faq, ensure_ascii=False)
    
    # Hreflang
    hreflang_zh = f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">\n<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">\n<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">'
    
    # 面包屑
    home_text = 'Home' if lang == 'en' else '首页'
    tools_text = 'Tools' if lang == 'en' else '工具'
    breadcrumb = [
        {"name": home_text, "item": "https://free-toolbase.com/" if lang == 'cn' else "https://free-toolbase.com/en/"},
        {"name": tools_text, "item": "https://free-toolbase.com/#tools" if lang == 'cn' else "https://free-toolbase.com/en/#tools"},
        {"name": name, "item": f"https://free-toolbase.com/{'en/' if lang == 'en' else ''}{slug}/"}
    ]
    
    # formatMoney
    money_func = "function formatMoney(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}" if lang == 'en' else "function formatMoney(n){return'¥'+n.toLocaleString('zh-CN',{minimumFractionDigits:2,maximumFractionDigits:2});}"
    
    page_url = f"https://free-toolbase.com/{'en/' if lang == 'en' else ''}{slug}/"
    cn_url = f"https://free-toolbase.com/{slug}/"
    en_url = f"https://free-toolbase.com/en/{slug}/"
    
    calc_script = tool['calc']
    # 替换formatMoney调用为locale版本
    if lang == 'en':
        calc_script = calc_script
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{name} | Free ToolBase</title>
<link rel="canonical" href="{page_url}">
<meta property="og:title" content="{name} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
{hreflang_zh}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"FinanceApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">""" + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in faq]}, ensure_ascii=False) + """</script>
<script type="application/ld+json">""" + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":b["name"],"item":b["item"]} for i,b in enumerate(breadcrumb)]}, ensure_ascii=False) + """</script>
<style>{CSS}</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {name}</h1><div class="lang-switch"><a href="{cn_url}"{' class="active"' if lang == 'cn' else ''}>中文</a><a href="{en_url}"{' class="active"' if lang == 'en' else ''}>EN</a></div></div>
<p class="nav-back"><a href="{'../index.html' if lang == 'cn' else '../'}">{"首页" if lang == "cn" else "Home"}</a> &rsaquo; <a href="{'../#tools' if lang == 'cn' else '../#tools'}">{"工具" if lang == "cn" else "Tools"}</a> &rsaquo; {name}</p>
<div class="hero"><p>{desc} <span class="badge">{'💰 无需注册 · 纯前端计算' if lang == 'cn' else '💰 No signup · Client-side only'}</span></p></div>

<div class="panel">
  <div class="panel-title">{'📋 输入参数' if lang == 'cn' else '📋 Input Parameters'}</div>
  <div class="input-group">
{inputs_html}  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="calcBtn">{'📊 计算' if lang == 'cn' else '📊 Calculate'}</button>
    <button class="btn btn-secondary" id="resetBtn">{'🔄 重置' if lang == 'cn' else '🔄 Reset'}</button>
  </div>
</div>

<div class="panel" id="resultPanel">
  <div class="panel-title">{'📈 计算结果' if lang == 'cn' else '📈 Results'}</div>
{result_html}
</div>

<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer><p>© 2025 Free ToolBase · {'纯前端计算，数据不上传服务器' if lang == 'cn' else 'Client-side only, no data uploaded'} · <a href="{'../' if lang == 'cn' else '../'}">{'首页' if lang == 'cn' else 'Home'}</a></p></footer>
<div class="toast" id="toast"></div>
</div>

<script>
function showToast(msg) {{
  const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2000);
}}
{money_func}
{calc_script}

// 元素引用
const calcBtn=document.getElementById('calcBtn'),resetBtn=document.getElementById('resetBtn');

calcBtn.addEventListener('click',calc);
resetBtn.addEventListener('click',function(){{location.reload();}});
calc();
</script>

<script>
(function(){{
  var processed=new Set();
  function addCopyBtns(){{
    var results=document.querySelectorAll('[id*="result"],[id*="Result"],[class*="result"]');
    results.forEach(function(el){{
      if(processed.has(el))return;
      if(el.querySelector('.copy-btn'))return;
      if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.tagName==='SELECT')return;
      if(el.children.length===0&&el.textContent.trim().length<5)return;
      var btn=document.createElement('button');
      btn.className='copy-btn';
      btn.innerHTML='📋 {"复制" if lang == "cn" else "Copy"}';
      btn.title='{"复制结果" if lang == "cn" else "Copy result"}';
      btn.onclick=function(e){{
        e.stopPropagation();
        var text=el.textContent||el.value||'';
        navigator.clipboard.writeText(text.trim()).then(function(){{
          btn.innerHTML='✅ {"已复制" if lang == "cn" else "Copied"}';
          btn.classList.add('copied');
          setTimeout(function(){{btn.innerHTML='📋 {"复制" if lang == "cn" else "Copy"}';btn.classList.remove('copied');}},2000);
        }}).catch(function(){{
          var ta=document.createElement('textarea');ta.value=text.trim();
          ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);
          btn.innerHTML='✅ {"已复制" if lang == "cn" else "Copied"}';
          btn.classList.add('copied');
          setTimeout(function(){{btn.innerHTML='📋 {"复制" if lang == "cn" else "Copy"}';btn.classList.remove('copied');}},2000);
        }});
      }};
      el.appendChild(btn);
      processed.add(el);
    }});
  }}
  addCopyBtns();
  document.addEventListener('click',function(){{setTimeout(addCopyBtns,100);}});
  if(window.MutationObserver){{
    var obs=new MutationObserver(function(){{addCopyBtns();}});
    obs.observe(document.body,{{childList:true,subtree:true}});
  }}
}})();
</script>

</body>
</html>'''
    return html


# 生成所有文件
base = '/home/chison/tools-site'

for tool in TOOLS:
    slug = tool['slug']
    
    # 中文版
    os.makedirs(f'{base}/{slug}', exist_ok=True)
    cn_html = generate_tool(tool, 'cn', 'zh-CN')
    with open(f'{base}/{slug}/index.html', 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f'✅ Created {slug}/index.html')
    
    # 英文版
    os.makedirs(f'{base}/en/{slug}', exist_ok=True)
    en_html = generate_tool(tool, 'en', 'en')
    with open(f'{base}/en/{slug}/index.html', 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✅ Created en/{slug}/index.html')

print(f'\n🎉 Done! Generated {len(TOOLS)} tools (10 files)')