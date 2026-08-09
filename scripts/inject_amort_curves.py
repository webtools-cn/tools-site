#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量给贷款类工具注入还款曲线 (剩余本金 vs 累计利息)
2026-08-09 三个同步: 任务② 贷款类曲线扩展
- 有 schedule 数组工具: ftDrawAmortSched(schedule, balKey) — 逐月数据最准
- 无 schedule 工具: ftDrawAmort(principal, mr, n, monthly) — 标准摊销曲线
- CN/EN 单位自适应 (万/亿 vs K/M/B), 通过 lang 属性判断
"""
import re, os, sys

BASE = '/home/chison/tools-site'

# ---------- 通用曲线函数 (注入到每个页面 <script> 内) ----------
AMORT_FN = r"""
function ftAmortIsCn(){var l=(document.documentElement.getAttribute('lang')||'').toLowerCase();return l.indexOf('zh')===0||l.indexOf('cn')===0}
function ftAmortFmtY(v,isCn){
  if(isCn)return v>=1e8?(v/1e8).toFixed(1)+'亿':v>=1e4?(v/1e4).toFixed(1)+'万':v.toFixed(0);
  return v>=1e9?(v/1e9).toFixed(1)+'B':v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(1)+'K':v.toFixed(0);
}
function ftDrawAmortSched(schedule,balKey){
  var cv=document.getElementById('ftAmortChart');
  if(!cv||!schedule||!schedule.length)return;
  var isCn=ftAmortIsCn();
  var series=[],cumInt=0;
  for(var i=0;i<schedule.length;i++){
    var s=schedule[i];
    cumInt+=(s.interest||0);
    if((i+1)%12===0||i===schedule.length-1){
      series.push({y:(i+1)/12,rem:Math.max(0,s[balKey]!==undefined?s[balKey]:s.remaining||s.balance||0),paidInt:cumInt});
    }
  }
  if(!series.length)return;
  var ctx=cv.getContext('2d');
  var W=cv.width,H=cv.height,padL=64,padR=14,padT=18,padB=26;
  ctx.clearRect(0,0,W,H);
  var maxV=0;
  for(var k=0;k<series.length;k++){maxV=Math.max(maxV,series[k].rem,series[k].paidInt)}
  if(maxV<=0)return;
  ctx.font='10px sans-serif';ctx.textAlign='right';
  for(var g=0;g<=4;g++){
    var y=padT+(H-padT-padB)*g/4,val=maxV*(4-g)/4;
    ctx.strokeStyle='rgba(148,163,184,.12)';ctx.beginPath();ctx.moveTo(padL,y);ctx.lineTo(W-padR,y);ctx.stroke();
    ctx.fillStyle='#94a3b8';ctx.fillText(ftAmortFmtY(val,isCn),padL-6,y+3);
  }
  function plotLine(getVal,color){
    ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();
    for(var i=0;i<series.length;i++){
      var x=padL+(W-padL-padR)*series[i].y/series[series.length-1].y;
      var y=padT+(H-padT-padB)*(1-series[i][getVal]/maxV);
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
  }
  plotLine('rem','#06b6d4');
  plotLine('paidInt','#10b981');
  ctx.fillStyle='#94a3b8';ctx.textAlign='center';
  ctx.fillText('0',padL,H-8);
  ctx.fillText(series[series.length-1].y.toFixed(0)+' '+(isCn?'年':'yr'),W-padR,H-8);
}
function ftDrawAmort(principal,mr,n,monthly){
  var cv=document.getElementById('ftAmortChart');
  if(!cv)return;
  var isCn=ftAmortIsCn();
  var rem=principal,paidInt=0,series=[];
  for(var i=1;i<=n;i++){
    var intPart=rem*mr,prinPart=monthly-intPart;
    rem-=prinPart;paidInt+=intPart;
    if(i%12===0||i===n){
      series.push({y:i/12,rem:Math.max(0,rem),paidInt:paidInt});
    }
  }
  if(!series.length)return;
  var ctx=cv.getContext('2d');
  var W=cv.width,H=cv.height,padL=64,padR=14,padT=18,padB=26;
  ctx.clearRect(0,0,W,H);
  var maxV=0;
  for(var k=0;k<series.length;k++){maxV=Math.max(maxV,series[k].rem,series[k].paidInt)}
  if(maxV<=0)return;
  ctx.font='10px sans-serif';ctx.textAlign='right';
  for(var g=0;g<=4;g++){
    var y=padT+(H-padT-padB)*g/4,val=maxV*(4-g)/4;
    ctx.strokeStyle='rgba(148,163,184,.12)';ctx.beginPath();ctx.moveTo(padL,y);ctx.lineTo(W-padR,y);ctx.stroke();
    ctx.fillStyle='#94a3b8';ctx.fillText(ftAmortFmtY(val,isCn),padL-6,y+3);
  }
  function plotLine(getVal,color){
    ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();
    for(var i=0;i<series.length;i++){
      var x=padL+(W-padL-padR)*series[i].y/series[series.length-1].y;
      var y=padT+(H-padT-padB)*(1-series[i][getVal]/maxV);
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
  }
  plotLine('rem','#06b6d4');
  plotLine('paidInt','#10b981');
  ctx.fillStyle='#94a3b8';ctx.textAlign='center';
  ctx.fillText('0',padL,H-8);
  ctx.fillText(series[series.length-1].y.toFixed(0)+' '+(isCn?'年':'yr'),W-padR,H-8);
}
"""

# canvas HTML (静态)
CANVAS_HTML = ('<canvas id="ftAmortChart" width="640" height="220" '
               'style="width:100%;height:220px;background:#0f172a;border:1px solid rgba(148,163,184,.1);'
               'border-radius:10px;margin-top:12px"></canvas>')

# ---------- 工具配置: (文件, 模式, 参数) ----------
# 模式: 'sched' → 调用 ftDrawAmortSched(schedule,'xxx'); 'std' → ftDrawAmort(p,mr,n,monthly)
TOOLS = [
    # auto-loan: 界面JS模板生成, canvas需注入模板字符串
    {
        'cn': 'auto-loan-calculator/index.html',
        'en': 'en/auto-loan-calculator/index.html',
        'mode': 'std',
        'call': 'ftDrawAmort(loan,mr,term,pmt);',
        'call_anchor': "document.getElementById('resultSection').classList.add('show');",
        'canvas_mode': 'template',  # 注入到 app.innerHTML 模板中 amortTable 后
        'canvas_anchor': '\\x3Ctbody id="amortTable">\\x3C/tbody>\\x3C/table>\\x3C/div>\\x3C/div>',
    },
    # car-loan: 静态HTML, schedule 有 remaining 字段
    {
        'cn': 'car-loan-calculator/index.html',
        'en': 'en/car-loan-calculator/index.html',
        'mode': 'sched',
        'bal_key': 'remaining',
        'call': 'ftDrawAmortSched(schedule,\'remaining\');',
        'call_anchor': "if(schedule.length>48){tbody.innerHTML+=",
        'call_insert': 'line_end',  # 整行结束后插入(避免插到表达式中间)
        'canvas_mode': 'before',
        'canvas_anchor': '<div class="schedule-scroll"',
    },
    # personal-loan: 静态HTML, schedule 有 remaining
    {
        'cn': 'personal-loan-calculator/index.html',
        'en': 'en/personal-loan-calculator/index.html',
        'mode': 'sched',
        'bal_key': 'remaining',
        'call': 'ftDrawAmortSched(schedule,\'remaining\');',
        'call_anchor': "if(schedule.length>48){tbody.innerHTML+=",
        'call_insert': 'line_end',  # 整行结束后插入(避免插到表达式中间)
        'canvas_mode': 'before',
        'canvas_anchor': '<div class="schedule-scroll"',
    },
    # home-loan: 静态HTML, 无 schedule → std (用平均emi近似, emi类型精确)
    {
        'cn': 'home-loan-calculator/index.html',
        'en': 'en/home-loan-calculator/index.html',
        'mode': 'std',
        'call': 'ftDrawAmort(principal,mr,months,emi);',
        'call_anchor': "document.getElementById('result-section').style.display='block';",
        'canvas_mode': 'after',
        'canvas_anchor': '<div class="result-grid" id="result-grid"></div>',
    },
    # loan-amortization: schedule 有 balance 字段 (注意bal_key=balance)
    {
        'cn': 'loan-amortization/index.html',
        'en': 'en/loan-amortization/index.html',
        'mode': 'sched',
        'bal_key': 'balance',
        'call': 'ftDrawAmortSched(schedule,\'balance\');',
        'call_anchor': "document.getElementById('resultCard').style.display='block';",
        'canvas_mode': 'before',
        'canvas_anchor': '<div style="max-height:400px;overflow-y:auto"><table',
    },
    # mortgage: calcMortgage, 无 schedule 数组 → std
    {
        'cn': 'mortgage-calculator/index.html',
        'en': 'en/mortgage-calculator/index.html',
        'mode': 'std',
        'call': 'ftDrawAmort(principal,monthlyRate,numPayments,monthly);',
        'call_anchor': "if(mcAmortVisible){buildMCAmort(principal,monthlyRate,numPayments,method,isCn);}",
        'canvas_mode': 'after',
        'canvas_anchor': '<div class="code-output" id="mcAmortTable"',
    },
]

def inject(path, cfg):
    if not os.path.exists(path):
        print(f'  ❌ 不存在: {path}')
        return False
    with open(path, encoding='utf-8') as f:
        html = f.read()
    orig = html

    # 1. 防重复
    if 'id="ftAmortChart"' in html:
        print(f'  ⏭️ 已有曲线: {path}')
        return True

    # 2. canvas 注入
    if cfg['canvas_mode'] == 'template':
        anchor = cfg['canvas_anchor']
        if anchor not in html:
            print(f'  ❌ canvas模板anchor未找到: {path}')
            return False
        # 模板内转义 < > 为 \x3C \x3E
        canvas_esc = CANVAS_HTML.replace('<', '\\x3C').replace('>', '\\x3E')
        html = html.replace(anchor, anchor[:-len('\\x3C/div>\\x3C/div>')] + canvas_esc + '\\x3C/div>\\x3C/div>', 1)
    elif cfg['canvas_mode'] == 'before':
        anchor = cfg['canvas_anchor']
        if anchor not in html:
            print(f'  ❌ canvas-before anchor未找到: {path}')
            return False
        html = html.replace(anchor, CANVAS_HTML + '\n' + anchor, 1)
    elif cfg['canvas_mode'] == 'after':
        anchor = cfg['canvas_anchor']
        if anchor not in html:
            print(f'  ❌ canvas-after anchor未找到: {path}')
            return False
        # 找到anchor的闭合标签: 简单策略 — 在anchor所在行的第一个 > 后插入
        pos = html.index(anchor)
        close = html.index('>', pos)
        html = html[:close+1] + '\n' + CANVAS_HTML + html[close+1:]

    # 3. 调用注入 (在 anchor 后, 支持 line_end 模式)
    call_anchor = cfg['call_anchor']
    if call_anchor not in html:
        print(f'  ❌ call anchor未找到: {path}')
        return False
    pos = html.index(call_anchor)
    end = pos + len(call_anchor)
    if cfg.get('call_insert') == 'line_end':
        # 找到该行行尾(下一个\n), 在整行结束后插入 — 避免插到 if(...){ 表达式中间
        le = html.find('\n', end)
        if le == -1:
            le = len(html)
        html = html[:le] + '\n  ' + cfg['call'] + html[le:]
    else:
        html = html[:end] + '\n  ' + cfg['call'] + html[end:]

    # 4. 函数注入: 只注入到包含 calc/calculate 函数的主 JS 块 (最后一个script块)
    #    按script块逐个分析, 找含 'function calc' 或 'function calculate' 或 'window.calculate' 的块
    blocks = list(re.finditer(r'<script[^>]*>([\s\S]*?)</script>', html))
    target_block = None
    for b in blocks:
        code = b.group(1)
        if ('function calc' in code or 'function calculate' in code
                or 'function calcMortgage' in code or 'window.calculate' in code):
            target_block = b
            break
    if not target_block:
        print(f'  ❌ 找不到主JS块: {path}')
        return False
    # 在该块内部最开头注入 (函数声明提升, 位置无关, 避免嵌套花括号匹配问题)
    code = target_block.group(1)
    new_code = AMORT_FN + '\n' + code
    html = html[:target_block.start(1)] + new_code + html[target_block.end(1):]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ {path} ({len(orig)}→{len(html)} chars)')
    return True

def main():
    ok = 0
    for cfg in TOOLS:
        for lang in ('cn', 'en'):
            print(f'== {lang.upper()} {cfg[lang]}')
            if inject(os.path.join(BASE, cfg[lang]), cfg):
                ok += 1
    print(f'\n完成: {ok}/{len(TOOLS)*2} 文件')

if __name__ == '__main__':
    main()
