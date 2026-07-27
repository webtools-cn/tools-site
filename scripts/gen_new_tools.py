#!/usr/bin/env python3
"""批量生成5个新工具：max-drawdown, treynor-ratio, information-ratio, kidney-function, iron-deficiency"""
import os

BASE = '/home/chison/tools-site'
DOMAIN = 'https://free-toolbase.com'

tools = [
    {
        'slug': 'max-drawdown-calculator',
        'name_cn': '最大回撤计算器',
        'name_en': 'Max Drawdown Calculator',
        'desc_cn': '免费在线最大回撤计算器，计算投资组合或资产的最大回撤率和回撤金额。支持多期数据输入，自动分析最大回撤周期，无需注册，数据不上传服务器。',
        'desc_en': 'Free online Max Drawdown Calculator. Calculate maximum drawdown rate and amount for portfolios or assets. Multi-period data input, automatic max drawdown analysis. No registration required.',
        'keywords': '最大回撤,回撤率,投资风险,max-drawdown-calculator,工具,在线工具,免费',
        'faq_cn': [
            ('什么是最大回撤？', '最大回撤(Max Drawdown) = (峰值 - 谷值) / 峰值 × 100%。它衡量投资期间从最高点到最低点的最大亏损幅度。'),
            ('最大回撤如何计算？', '遍历所有时间点：对每个峰值，找到后续最低点，计算回撤率，取最大值。例如净值从100跌到70，回撤率为30%。'),
            ('最大回撤的意义是什么？', '最大回撤反映投资的最大潜在亏损，是衡量风险的核心指标。回撤越大，风险越高。通常与夏普比率配合使用。'),
            ('如何降低最大回撤？', '分散投资、设置止损、资产配置再平衡、对冲策略等。最大回撤是历史数据，不代表未来表现。'),
        ],
        'faq_en': [
            ('What is Max Drawdown?', 'Max Drawdown = (Peak - Trough) / Peak × 100%. It measures the largest peak-to-trough decline during an investment period.'),
            ('How is Max Drawdown calculated?', 'For each peak, find the subsequent lowest point, calculate drawdown rate, take the maximum. E.g. NAV drops from 100 to 70, drawdown is 30%.'),
            ('What does Max Drawdown tell us?', 'It reflects the maximum potential loss of an investment and is a core risk metric. Higher drawdown means higher risk. Often used with Sharpe Ratio.'),
            ('How to reduce Max Drawdown?', 'Diversify investments, set stop-loss orders, rebalance asset allocation, use hedging strategies. Past drawdown does not guarantee future results.'),
        ],
        'inputs': [
            ('navValues', '净值数据（每行一个）', 'NAV Values (one per line)', 'textarea', '100\n95\n90\n88\n92\n85\n80\n78\n75\n70\n72\n68\n65\n62\n60'),
        ],
        'calc_formula': '遍历净值数组：对每个i，找j>i的最小值，回撤=(nav[i]-nav[j])/nav[i]，取最大',
        'calc_js': """function calc(){
  var raw = document.getElementById('navValues').value.trim();
  if(!raw){showToast('请输入净值数据');return}
  var lines = raw.split(/[\\n,;\\s]+/).filter(function(x){return x!==''});
  var navs = [];
  for(var i=0;i<lines.length;i++){
    var v=parseFloat(lines[i]);
    if(!isNaN(v)&&v>0) navs.push(v);
  }
  if(navs.length<2){showToast('至少需要2个净值数据');return}
  var maxDD=0, peakIdx=0, troughIdx=0;
  for(var i=0;i<navs.length;i++){
    for(var j=i+1;j<navs.length;j++){
      var dd=(navs[i]-navs[j])/navs[i];
      if(dd>maxDD){maxDD=dd;peakIdx=i;troughIdx=j;}
    }
  }
  var peakVal=navs[peakIdx], troughVal=navs[troughIdx];
  document.getElementById('rDrawdown').textContent=(maxDD*100).toFixed(2)+'%';
  document.getElementById('rLoss').textContent='$'+(peakVal-troughVal).toFixed(2);
  document.getElementById('rPeak').textContent='$'+peakVal.toFixed(2)+' (#'+(peakIdx+1)+')';
  document.getElementById('rTrough').textContent='$'+troughVal.toFixed(2)+' (#'+(troughIdx+1)+')';
  document.getElementById('rPeriod').textContent=(troughIdx-peakIdx+1)+' 期';
  document.getElementById('rRecovery').textContent=troughIdx<navs.length-1?((navs[navs.length-1]-troughVal)/troughVal*100).toFixed(2)+'%':'未恢复';
}""",
    },
    {
        'slug': 'treynor-ratio-calculator',
        'name_cn': '特雷诺比率计算器',
        'name_en': 'Treynor Ratio Calculator',
        'desc_cn': '免费在线特雷诺比率计算器，衡量投资组合每单位系统性风险的超额回报。输入组合收益率、无风险利率和Beta值即可计算，无需注册，数据不上传服务器。',
        'desc_en': 'Free online Treynor Ratio Calculator. Measure excess return per unit of systematic risk. Input portfolio return, risk-free rate, and Beta to calculate. No registration required.',
        'keywords': '特雷诺比率,treynor,风险调整收益,投资分析,treynor-ratio-calculator,工具,在线工具,免费',
        'faq_cn': [
            ('什么是特雷诺比率？', '特雷诺比率 = (组合收益率 - 无风险利率) / Beta。衡量每单位系统性风险获得的超额回报。'),
            ('特雷诺比率和夏普比率的区别？', '夏普比率用标准差（总风险），特雷诺比率用Beta（系统性风险）。特雷诺适合评估已充分分散的投资组合。'),
            ('特雷诺比率多高算好？', '越高越好。正值表示跑赢无风险收益，越高表示风险调整后表现越好。可与基准指数比较。'),
            ('Beta值如何获取？', 'Beta衡量资产相对市场的波动性。Beta>1波动大于市场，Beta<1波动小于市场。可从金融数据平台获取。'),
        ],
        'faq_en': [
            ('What is Treynor Ratio?', 'Treynor Ratio = (Portfolio Return - Risk-Free Rate) / Beta. Measures excess return per unit of systematic risk.'),
            ('Treynor vs Sharpe Ratio?', 'Sharpe uses standard deviation (total risk), Treynor uses Beta (systematic risk). Treynor is better for well-diversified portfolios.'),
            ('What is a good Treynor Ratio?', 'Higher is better. Positive means outperforming risk-free rate. Compare against benchmark index.'),
            ('How to get Beta value?', 'Beta measures volatility relative to the market. Beta>1 = more volatile, Beta<1 = less volatile. Available from financial data platforms.'),
        ],
        'inputs': [
            ('portfolioReturn', '组合年化收益率(%)', 'Portfolio Annual Return (%)', 'number', '12'),
            ('riskFreeRate', '无风险利率(%)', 'Risk-Free Rate (%)', 'number', '3'),
            ('beta', 'Beta值', 'Beta', 'number', '1.2'),
        ],
        'calc_formula': '特雷诺比率 = (portfolioReturn - riskFreeRate) / beta',
        'calc_js': """function calc(){
  var rp=parseFloat(document.getElementById('portfolioReturn').value);
  var rf=parseFloat(document.getElementById('riskFreeRate').value);
  var beta=parseFloat(document.getElementById('beta').value);
  if(isNaN(rp)||isNaN(rf)||isNaN(beta)){showToast('请填写所有字段');return}
  if(beta<=0){showToast('Beta必须大于0');return}
  var treynor=(rp-rf)/beta;
  document.getElementById('rTreynor').textContent=treynor.toFixed(4);
  document.getElementById('rExcess').textContent=(rp-rf).toFixed(2)+'%';
  var rating=treynor>2?'优秀':treynor>1?'良好':treynor>0.5?'一般':treynor>0?'较差':'很差';
  document.getElementById('rRating').textContent=rating;
}""",
    },
    {
        'slug': 'information-ratio-calculator',
        'name_cn': '信息比率计算器',
        'name_en': 'Information Ratio Calculator',
        'desc_cn': '免费在线信息比率计算器，衡量投资组合相对基准的超额回报稳定性。输入组合收益、基准收益和跟踪误差即可计算，无需注册，数据不上传服务器。',
        'desc_en': 'Free online Information Ratio Calculator. Measure consistency of excess return vs benchmark. Input portfolio return, benchmark return, and tracking error. No registration required.',
        'keywords': '信息比率,information ratio,投资分析,跟踪误差,information-ratio-calculator,工具,在线工具,免费',
        'faq_cn': [
            ('什么是信息比率？', '信息比率 = (组合收益率 - 基准收益率) / 跟踪误差。衡量每单位主动风险获得的超额回报。'),
            ('信息比率多高算好？', '0.5以上为良好，0.75以上为优秀，1.0以上为卓越。正数表示持续跑赢基准。'),
            ('跟踪误差是什么？', '跟踪误差是组合收益率与基准收益率差异的标准差，衡量主动管理的风险程度。'),
            ('信息比率和夏普比率的区别？', '信息比率关注相对基准的超额回报，夏普比率关注绝对回报。信息比率更适合评估主动管理能力。'),
        ],
        'faq_en': [
            ('What is Information Ratio?', 'Information Ratio = (Portfolio Return - Benchmark Return) / Tracking Error. Measures excess return per unit of active risk.'),
            ('What is a good Information Ratio?', 'Above 0.5 is good, 0.75+ excellent, 1.0+ outstanding. Positive means consistently beating the benchmark.'),
            ('What is Tracking Error?', 'Tracking error is the standard deviation of return differences vs benchmark. Measures active management risk.'),
            ('IR vs Sharpe Ratio?', 'IR focuses on excess return vs benchmark, Sharpe on absolute return. IR better evaluates active management skill.'),
        ],
        'inputs': [
            ('portfolioReturn', '组合年化收益率(%)', 'Portfolio Annual Return (%)', 'number', '15'),
            ('benchmarkReturn', '基准年化收益率(%)', 'Benchmark Annual Return (%)', 'number', '10'),
            ('trackingError', '跟踪误差(%)', 'Tracking Error (%)', 'number', '6'),
        ],
        'calc_formula': '信息比率 = (portfolioReturn - benchmarkReturn) / trackingError',
        'calc_js': """function calc(){
  var rp=parseFloat(document.getElementById('portfolioReturn').value);
  var rb=parseFloat(document.getElementById('benchmarkReturn').value);
  var te=parseFloat(document.getElementById('trackingError').value);
  if(isNaN(rp)||isNaN(rb)||isNaN(te)){showToast('请填写所有字段');return}
  if(te<=0){showToast('跟踪误差必须大于0');return}
  var ir=(rp-rb)/te;
  document.getElementById('rIR').textContent=ir.toFixed(4);
  document.getElementById('rExcess').textContent=(rp-rb).toFixed(2)+'%';
  var rating=ir>1?'卓越':ir>0.75?'优秀':ir>0.5?'良好':ir>0?'一般':'跑输基准';
  document.getElementById('rRating').textContent=rating;
}""",
    },
    {
        'slug': 'kidney-function-calculator',
        'name_cn': '肾功能计算器 (eGFR)',
        'name_en': 'Kidney Function Calculator (eGFR)',
        'desc_cn': '免费在线肾功能计算器，使用CKD-EPI公式估算肾小球滤过率(eGFR)。输入肌酐、年龄、性别即可计算肾功能分期，无需注册，数据不上传服务器。',
        'desc_en': 'Free online Kidney Function Calculator using CKD-EPI formula to estimate eGFR. Input creatinine, age, gender. No registration required, data stays local.',
        'keywords': '肾功能,eGFR,肾小球滤过率,CKD-EPI,肌酐,kidney-function-calculator,工具,在线工具,免费',
        'faq_cn': [
            ('什么是eGFR？', 'eGFR(估算肾小球滤过率)是衡量肾脏过滤血液能力的指标。正常值≥90 mL/min/1.73m²。'),
            ('CKD分期如何划分？', 'G1:≥90正常，G2:60-89轻度下降，G3a:45-59轻中度，G3b:30-44中重度，G4:15-29重度，G5:<15肾衰竭。'),
            ('肌酐是什么？', '肌酐是肌肉代谢废物，由肾脏过滤排出。血肌酐升高通常提示肾功能下降。'),
            ('本计算器的准确性？', '使用CKD-EPI 2021公式，适用于成人。仅作参考，不能替代医学诊断。请咨询医生。'),
        ],
        'faq_en': [
            ('What is eGFR?', 'eGFR (estimated Glomerular Filtration Rate) measures kidney filtering capacity. Normal is ≥90 mL/min/1.73m².'),
            ('What are CKD stages?', 'G1:≥90 normal, G2:60-89 mild, G3a:45-59 mild-moderate, G3b:30-44 moderate-severe, G4:15-29 severe, G5:<15 kidney failure.'),
            ('What is creatinine?', 'Creatinine is a muscle waste product filtered by kidneys. Elevated blood creatinine often indicates reduced kidney function.'),
            ('How accurate is this calculator?', 'Uses CKD-EPI 2021 formula for adults. Reference only, not medical diagnosis. Consult a doctor.'),
        ],
        'inputs': [
            ('creatinine', '血肌酐 (mg/dL)', 'Serum Creatinine (mg/dL)', 'number', '1.0'),
            ('age', '年龄', 'Age', 'number', '45'),
            ('gender', '性别', 'Gender', 'select', 'male,female'),
        ],
        'calc_formula': 'CKD-EPI 2021: eGFR = 142 × (Scr/κ)^α × 0.9938^age × 1.012(if female)，κ=0.7(female)/0.9(male)，α=-0.241(female)/-0.302(male)',
        'calc_js': """function calc(){
  var scr=parseFloat(document.getElementById('creatinine').value);
  var age=parseFloat(document.getElementById('age').value);
  var gender=document.getElementById('gender').value;
  if(isNaN(scr)||isNaN(age)){showToast('请填写所有字段');return}
  if(scr<=0||age<=0||age>120){showToast('请输入有效数值');return}
  var kappa=gender==='female'?0.7:0.9;
  var alpha=gender==='female'?-0.241:-0.302;
  var factor=gender==='female'?1.012:1;
  var egfr=142*Math.pow(Math.min(scr/kappa,1),alpha)*Math.pow(Math.max(scr/kappa,1),-1.200)*Math.pow(0.9938,age)*factor;
  egfr=Math.round(egfr);
  document.getElementById('rEGFR').textContent=egfr+' mL/min/1.73m²';
  var stage,stageDesc;
  if(egfr>=90){stage='G1';stageDesc='正常或高滤过';}
  else if(egfr>=60){stage='G2';stageDesc='轻度下降';}
  else if(egfr>=45){stage='G3a';stageDesc='轻中度下降';}
  else if(egfr>=30){stage='G3b';stageDesc='中重度下降';}
  else if(egfr>=15){stage='G4';stageDesc='重度下降';}
  else{stage='G5';stageDesc='肾衰竭';}
  document.getElementById('rStage').textContent=stage;
  document.getElementById('rDesc').textContent=stageDesc;
  document.getElementById('rDisclaimer').style.display='block';
}""",
    },
    {
        'slug': 'iron-deficiency-calculator',
        'name_cn': '缺铁性贫血评估计算器',
        'name_en': 'Iron Deficiency Anemia Calculator',
        'desc_cn': '免费在线缺铁性贫血评估计算器，基于血红蛋白、铁蛋白等指标评估缺铁风险。帮助识别缺铁性贫血的可能性和严重程度，无需注册，数据不上传服务器。',
        'desc_en': 'Free online Iron Deficiency Anemia Calculator. Assess iron deficiency risk based on hemoglobin, ferritin, and other markers. No registration required, data stays local.',
        'keywords': '缺铁性贫血,铁蛋白,血红蛋白,iron-deficiency-calculator,工具,在线工具,免费,贫血评估',
        'faq_cn': [
            ('缺铁性贫血的常见症状？', '疲劳乏力、面色苍白、头晕、心悸、注意力不集中、异食癖等。严重时影响免疫功能。'),
            ('血红蛋白正常值是多少？', '成年男性:13.5-17.5 g/dL，成年女性:12.0-15.5 g/dL。低于正常值提示贫血。'),
            ('铁蛋白的作用？', '铁蛋白反映体内铁储备。低铁蛋白(<30 ng/mL)提示铁缺乏，即使血红蛋白正常也可能是潜伏性缺铁。'),
            ('如何改善缺铁？', '增加红肉、动物肝脏、菠菜等富铁食物摄入，搭配维生素C促进吸收。严重时需遵医嘱补铁。'),
        ],
        'faq_en': [
            ('What are symptoms of iron deficiency?', 'Fatigue, pale skin, dizziness, palpitations, poor concentration, pica. Severe cases affect immune function.'),
            ('What is normal hemoglobin?', 'Adult male: 13.5-17.5 g/dL, adult female: 12.0-15.5 g/dL. Below normal indicates anemia.'),
            ('What does ferritin indicate?', 'Ferritin reflects iron stores. Low ferritin (<30 ng/mL) suggests iron deficiency even with normal hemoglobin.'),
            ('How to improve iron levels?', 'Eat iron-rich foods (red meat, liver, spinach), pair with vitamin C. Severe cases need medical iron supplementation.'),
        ],
        'inputs': [
            ('hemoglobin', '血红蛋白 (g/dL)', 'Hemoglobin (g/dL)', 'number', '11.5'),
            ('ferritin', '铁蛋白 (ng/mL)', 'Ferritin (ng/mL)', 'number', '20'),
            ('gender2', '性别', 'Gender', 'select', 'female,male'),
        ],
        'calc_formula': '综合评估：Hb低于阈值+铁蛋白低=缺铁性贫血高风险',
        'calc_js': """function calc(){
  var hb=parseFloat(document.getElementById('hemoglobin').value);
  var ferritin=parseFloat(document.getElementById('ferritin').value);
  var gender=document.getElementById('gender2').value;
  if(isNaN(hb)||isNaN(ferritin)){showToast('请填写所有字段');return}
  if(hb<=0||ferritin<=0){showToast('请输入有效数值');return}
  var hbLow=gender==='female'?12.0:13.5;
  var hbNormal=gender==='female'?15.5:17.5;
  var anemia=(hb<hbLow)?(hb<8?'重度贫血':hb<10?'中度贫血':'轻度贫血'):'无贫血';
  var ironStatus=ferritin<15?'严重缺铁':ferritin<30?'铁缺乏':ferritin<50?'铁储备偏低':ferritin<100?'铁储备充足':'铁储备过高';
  var risk='';
  if(hb<hbLow&&ferritin<30) risk='高风险：缺铁性贫血可能性大，建议就医';
  else if(hb<hbLow&&ferritin>=30) risk='中风险：贫血但铁储备正常，可能是其他原因';
  else if(hb>=hbLow&&ferritin<30) risk='中风险：潜伏性缺铁，血红蛋白尚正常但铁储备不足';
  else risk='低风险：血红蛋白和铁储备均正常';
  document.getElementById('rHb').textContent=hb+' g/dL ('+anemia+')';
  document.getElementById('rFerritin').textContent=ferritin+' ng/mL ('+ironStatus+')';
  document.getElementById('rRisk').textContent=risk;
  document.getElementById('rDisclaimer').style.display='block';
}""",
    },
]


def gen_tool(t, lang='cn'):
    is_cn = lang == 'cn'
    slug = t['slug']
    name = t['name_cn'] if is_cn else t['name_en']
    desc = t['desc_cn'] if is_cn else t['desc_en']
    faq = t['faq_cn'] if is_cn else t['faq_en']
    keywords = t['keywords']

    dir_path = os.path.join(BASE, slug) if is_cn else os.path.join(BASE, 'en', slug)
    os.makedirs(dir_path, exist_ok=True)

    lang_code = 'zh-CN' if is_cn else 'en'
    alt_lang = 'zh' if is_cn else 'en'
    alt_href = f'{DOMAIN}/{slug}/' if is_cn else f'{DOMAIN}/en/{slug}/'
    other_href = f'{DOMAIN}/en/{slug}/' if is_cn else f'{DOMAIN}/{slug}/'

    # Inputs HTML
    inputs_html = ''
    for inp in t['inputs']:
        inp_id = inp[0]
        inp_label = inp[1] if is_cn else inp[2]
        inp_type = inp[3]
        if inp_type == 'textarea':
            default_val = inp[4]
            inputs_html += f'''<div class="form-group"><label>{inp_label}</label><textarea id="{inp_id}" rows="8" style="width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;font-family:monospace;resize:vertical">{default_val}</textarea></div>\n'''
        elif inp_type == 'select':
            opts = inp[4].split(',')
            opts_html = ''.join([f'<option value="{o}">{o.capitalize()}</option>' for o in opts])
            inputs_html += f'''<div class="form-group"><label>{inp_label}</label><select id="{inp_id}" style="width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none">{opts_html}</select></div>\n'''
        else:
            default_val = inp[4]
            step = '0.01' if '.' in str(default_val) else '1'
            inputs_html += f'''<div class="form-group"><label>{inp_label}</label><input type="number" id="{inp_id}" step="{step}" min="0" value="{default_val}"></div>\n'''

    # FAQ HTML
    faq_html = ''
    for q, a in faq:
        faq_html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>\n'

    # Result fields based on calc_js
    result_ids = set()
    import re
    for m in re.finditer(r"getElementById\('(r\w+)'\)", t['calc_js']):
        result_ids.add(m.group(1))

    result_grid = ''
    for rid in sorted(result_ids):
        label_map = {
            'rDrawdown': ('最大回撤率', 'Max Drawdown'),
            'rLoss': ('回撤金额', 'Drawdown Amount'),
            'rPeak': ('峰值', 'Peak'),
            'rTrough': ('谷值', 'Trough'),
            'rPeriod': ('回撤周期', 'Drawdown Period'),
            'rRecovery': ('恢复幅度', 'Recovery'),
            'rTreynor': ('特雷诺比率', 'Treynor Ratio'),
            'rExcess': ('超额收益', 'Excess Return'),
            'rRating': ('评级', 'Rating'),
            'rIR': ('信息比率', 'Information Ratio'),
            'rEGFR': ('估算eGFR', 'Estimated eGFR'),
            'rStage': ('CKD分期', 'CKD Stage'),
            'rDesc': ('肾功能状态', 'Kidney Status'),
            'rHb': ('血红蛋白', 'Hemoglobin'),
            'rFerritin': ('铁蛋白', 'Ferritin'),
            'rRisk': ('风险评估', 'Risk Assessment'),
        }
        label = label_map.get(rid, (rid, rid))
        label_text = label[0] if is_cn else label[1]
        highlight = ' highlight' if rid in ('rDrawdown','rTreynor','rIR','rEGFR','rRisk') else ''
        result_grid += f'<div class="result-item"><div class="label">{label_text}</div><div class="value{highlight}" id="{rid}">&mdash;</div></div>\n'

    # Disclaimer for medical tools
    disclaimer = ''
    if 'rDisclaimer' in result_ids:
        disclaimer = '<div id="rDisclaimer" style="display:none;margin-top:12px;padding:10px 14px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:8px;font-size:.8rem;color:#fbbf24;text-align:center">⚠️ ' + ('此计算器仅作参考，不能替代医学诊断。如有健康问题请咨询医生。' if is_cn else '⚠️ This calculator is for reference only. Not a substitute for medical diagnosis. Consult a doctor.') + '</div>\n'

    home_label = '首页' if is_cn else 'Home'
    tools_label = '工具' if is_cn else 'Tools'
    lang_link = f'<a href="index.html" class="active">{alt_lang.upper() if is_cn else "中文" if alt_lang=="zh" else alt_lang.upper()}</a><a href="../{slug}/">{"EN" if is_cn else "中文"}</a>' if is_cn else f'<a href="../en/{slug}/" class="active">EN</a><a href="../../{slug}/">中文</a>'
    nav_home = '../index.html' if is_cn else '../../index.html'

    html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{name} - Free ToolBase</title>
<link rel="canonical" href="{DOMAIN}/{slug}/">
<meta property="og:title" content="{name} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">
<link rel="alternate" hreflang="{'en' if is_cn else 'zh'}" href="{other_href}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{','.join(['{"@type":"Question","name":"'+q+'","acceptedAnswer":{"@type":"Answer","text":"'+a+'"}}' for q,a in faq])}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{name}","description":"如何使用{name}的详细步骤指南","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入参数","text":"输入相关参数数据。"}},{{"@type":"HowToStep","position":2,"name":"点击计算","text":"点击计算按钮，系统自动分析并显示结果。"}},{{"@type":"HowToStep","position":3,"name":"查看结果","text":"查看计算结果，支持一键复制。"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_label}","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"{tools_label}","item":"{DOMAIN}/#tools"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"{DOMAIN}/{slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4)}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.result-item{{background:#0a0f1e;border-radius:8px;padding:14px}}
.result-item .label{{color:#94a3b8;font-size:.8rem}}
.result-item .value{{font-size:1.2rem;font-weight:700;color:#22d3ee;margin-top:4px}}
.result-item .value.highlight{{color:#fbbf24;font-size:1.5rem}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-item h3{{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}}
.faq-item p{{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}}
.footer{{text-align:center;color:#64748b;font-size:.85rem;margin-top:32px;padding-top:20px;border-top:1px solid rgba(148,163,184,.08)}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}}}
</style>
<meta property="og:image" content="{DOMAIN}/og-image.svg">
<meta name="twitter:image" content="{DOMAIN}/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{'📉 ' if 'max-drawdown' in slug else '📊 ' if 'ratio' in slug else '🩺 '}{name}</h1><div class="lang-switch">{lang_link}</div></div>
<p class="nav-back"><a href="{nav_home}">{home_label}</a> &rsaquo; <a href="{nav_home}#tools">{tools_label}</a> &rsaquo; {name}</p>
<div class="section">
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{desc}</p>
{inputs_html}
<div class="btn-group"><button class="btn btn-primary" onclick="calc()">{'计算' if is_cn else 'Calculate'}</button><button class="btn btn-secondary" onclick="clearAll()">{'清空' if is_cn else 'Clear'}</button></div>
<div class="result-grid" style="margin-top:16px">
{result_grid}</div>
{disclaimer}
<div class="btn-group"><button class="btn btn-secondary" onclick="copyAll()">📋 {'复制结果' if is_cn else 'Copy Results'}</button></div>
</div>
<div class="section"><h2>{'常见问题' if is_cn else 'FAQ'}</h2>
{faq_html}</div>
</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container"><div style="margin-bottom:12px"><a href="{nav_home}">{home_label}</a><a href="{nav_home}#tools">{tools_label}</a><a href="mailto:dexshuang@google.com">{'联系我们' if is_cn else 'Contact'}</a><a href="{nav_home}privacy/">{'隐私政策' if is_cn else 'Privacy'}</a><a href="{nav_home}terms/">{'服务条款' if is_cn else 'Terms'}</a><a href="{nav_home}about/">{'关于我们' if is_cn else 'About'}</a></div>
<p>{name} | {'无需注册 · 数据绝不上传服务器' if is_cn else 'No registration · Data stays on your device'}</p><p style="margin-top:8px;color:#475569;font-size:.8rem">{'问题反馈' if is_cn else 'Feedback'}: dexshuang@google.com</p></footer>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
{t['calc_js']}
function clearAll(){{location.reload()}}
function copyAll(){{var items=document.querySelectorAll('.result-item .value');var lines=[];items.forEach(function(el){{var lbl=el.parentElement.querySelector('.label');if(lbl&&el.textContent!=='—')lines.push(lbl.textContent+': '+el.textContent)}});if(lines.length===0){{showToast("{'没有结果可复制' if is_cn else 'No results to copy'}");return}}navigator.clipboard.writeText(lines.join("\\n")).then(function(){{showToast("{'已复制' if is_cn else 'Copied'}")}}).catch(function(){{showToast("{'复制失败' if is_cn else 'Copy failed'}")}})}}
</script>
</body>
</html>'''

    filepath = os.path.join(dir_path, 'index.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Created: {filepath}')
    return True


for t in tools:
    gen_tool(t, 'cn')
    gen_tool(t, 'en')

print('\nDone! 5 tools x 2 langs = 10 files')