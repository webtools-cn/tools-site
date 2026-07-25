#!/usr/bin/env python3
"""将工具逻辑注入到骨架文件中。一次处理所有剩余8个工具的中英文版。"""
import re, os

BASE = '/home/chison/tools-site'

# 定义每个工具的 HTML UI 和 JS 逻辑
tools = {}

# === 2. subnet-mask-calc ===
tools['subnet-mask-calc'] = {
    'cn': {
        'html': '''  <div class="input-group">
    <label for="toolInput">输入IP/CIDR (如 192.168.1.0/24)</label>
    <input type="text" id="toolInput" placeholder="192.168.1.0/24">
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">计算子网</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ipToInt(ip){return ip.split('.').reduce((s,o)=>s*256+parseInt(o),0)>>>0;}
function intToIp(n){return [(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255].join('.');}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  const match=input.match(/^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})\\/(\\d{1,2})$/);
  if(!match){toast('格式错误，请使用 IP/CIDR 格式');return;}
  const ip=match[1],cidr=parseInt(match[2]);
  if(cidr<0||cidr>32){toast('CIDR范围: 0-32');return;}
  const ipInt=ipToInt(ip);
  const mask=~(0xFFFFFFFF>>>cidr)>>>0;
  const net=ipInt&mask;
  const bcast=net|~mask>>>0;
  const first=cidr<31?net+1:net;
  const last=cidr<31?bcast-1:bcast;
  const hosts=cidr<31?(1<<(32-cidr))-2:cidr===31?2:1;
  const lines=[
    `IP地址:     ${ip}`,
    `子网掩码:   ${intToIp(mask)}  (/${cidr})`,
    `网络地址:   ${intToIp(net)}`,
    `广播地址:   ${intToIp(bcast)}`,
    `可用范围:   ${intToIp(first)} ~ ${intToIp(last)}`,
    `可用主机数: ${hosts.toLocaleString()}`,
    `总IP数:     ${(hosts+2).toLocaleString()}`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="input-group">
    <label for="toolInput">Enter IP/CIDR (e.g. 192.168.1.0/24)</label>
    <input type="text" id="toolInput" placeholder="192.168.1.0/24">
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Calculate</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ipToInt(ip){return ip.split('.').reduce((s,o)=>s*256+parseInt(o),0)>>>0;}
function intToIp(n){return [(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255].join('.');}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  const match=input.match(/^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})\\/(\\d{1,2})$/);
  if(!match){toast('Invalid format. Use IP/CIDR');return;}
  const ip=match[1],cidr=parseInt(match[2]);
  if(cidr<0||cidr>32){toast('CIDR range: 0-32');return;}
  const ipInt=ipToInt(ip);
  const mask=~(0xFFFFFFFF>>>cidr)>>>0;
  const net=ipInt&mask;
  const bcast=net|~mask>>>0;
  const first=cidr<31?net+1:net;
  const last=cidr<31?bcast-1:bcast;
  const hosts=cidr<31?(1<<(32-cidr))-2:cidr===31?2:1;
  const lines=[
    `IP Address:    ${ip}`,
    `Subnet Mask:   ${intToIp(mask)}  (/${cidr})`,
    `Network:       ${intToIp(net)}`,
    `Broadcast:     ${intToIp(bcast)}`,
    `Usable Range:  ${intToIp(first)} ~ ${intToIp(last)}`,
    `Usable Hosts:  ${hosts.toLocaleString()}`,
    `Total IPs:     ${(hosts+2).toLocaleString()}`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 3. api-rate-limiter-calc ===
tools['api-rate-limiter-calc'] = {
    'cn': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="rateLimit">速率限制 (请求数)</label>
      <input type="number" id="rateLimit" placeholder="100" value="100" min="1">
    </div>
    <div class="input-group">
      <label for="rateWindow">时间窗口 (秒)</label>
      <input type="number" id="rateWindow" placeholder="60" value="60" min="1">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">计算配额</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function calc(){
  const limit=parseInt($('rateLimit').value)||100;
  const win=parseInt($('rateWindow').value)||60;
  if(limit<1||win<1){toast('请输入有效数值');return;}
  const rps=limit/win;
  const lines=[
    `=== 速率限制分析 ===`,
    `配置: ${limit} 请求 / ${win} 秒`,
    `平均速率: ${rps.toFixed(2)} 请求/秒`,
    ``,
    `--- 固定窗口 ---`,
    `每10秒:   ${Math.floor(rps*10)} 请求`,
    `每分钟:   ${Math.floor(rps*60)} 请求`,
    `每小时:   ${Math.floor(rps*3600).toLocaleString()} 请求`,
    ``,
    `--- 令牌桶策略 ---`,
    `填充速率: ${rps.toFixed(2)} 令牌/秒`,
    `桶容量(推荐): ${limit} 令牌`,
    `恢复1令牌: ${Math.ceil(1/rps*1000)}ms`,
    `恢复全桶: ${win}s`,
    ``,
    `--- 滑动窗口 ---`,
    `窗口:      ${win}s`,
    `最大突发:  ${limit} 请求`,
    `均匀间隔:  ${Math.ceil(win/limit*1000)}ms`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
}

$('btnProcess').addEventListener('click',calc);
$('btnClear').addEventListener('click',()=>{$('rateLimit').value='100';$('rateWindow').value='60';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});
calc();'''
    },
    'en': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="rateLimit">Rate Limit (requests)</label>
      <input type="number" id="rateLimit" placeholder="100" value="100" min="1">
    </div>
    <div class="input-group">
      <label for="rateWindow">Time Window (seconds)</label>
      <input type="number" id="rateWindow" placeholder="60" value="60" min="1">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Calculate</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function calc(){
  const limit=parseInt($('rateLimit').value)||100;
  const win=parseInt($('rateWindow').value)||60;
  if(limit<1||win<1){toast('Please enter valid numbers');return;}
  const rps=limit/win;
  const lines=[
    `=== Rate Limiter Analysis ===`,
    `Config: ${limit} requests / ${win}s`,
    `Avg Rate: ${rps.toFixed(2)} req/s`,
    ``,
    `--- Fixed Window ---`,
    `Per 10s:   ${Math.floor(rps*10)} req`,
    `Per min:   ${Math.floor(rps*60)} req`,
    `Per hour:  ${Math.floor(rps*3600).toLocaleString()} req`,
    ``,
    `--- Token Bucket ---`,
    `Fill rate: ${rps.toFixed(2)} tokens/s`,
    `Bucket (rec): ${limit} tokens`,
    `Refill 1:  ${Math.ceil(1/rps*1000)}ms`,
    `Refill all: ${win}s`,
    ``,
    `--- Sliding Window ---`,
    `Window:     ${win}s`,
    `Max burst:  ${limit} req`,
    `Even:       ${Math.ceil(win/limit*1000)}ms`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
}

$('btnProcess').addEventListener('click',calc);
$('btnClear').addEventListener('click',()=>{$('rateLimit').value='100';$('rateWindow').value='60';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});
calc();'''
    }
}

# === 4. css-specificity-calc ===
tools['css-specificity-calc'] = {
    'cn': {
        'html': '''  <div class="input-group">
    <label for="toolInput">输入CSS选择器</label>
    <input type="text" id="toolInput" placeholder="如 #header .nav > ul li a:hover">
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">计算优先级</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function calcSpecificity(selector){
  const s=selector.trim();
  let ids=(s.match(/#[\\w-]+/g)||[]).length;
  let classes=(s.match(/\\.[\\w-]+/g)||[]).length;
  let attrs=(s.match(/\\[[^\\]]+\\]/g)||[]).length;
  let pseudos=(s.match(/:[\\w-]+(?=\\s|\\(|$)/g)||[]).length;
  let elements=(s.match(/(?:^|[\\s>+~,])([a-zA-Z][\\w-]*)(?![\\w-]*[\\]\\)])(?![\\w-]*\\()/g)||[]).filter(e=>!/^(?:not|has|is|where)$/i.test(e.replace(/[^a-zA-Z]/g,''))).length;
  if(!ids&&!classes&&!attrs&&!pseudos&&!elements){
    elements=(s.match(/\\b[a-zA-Z][\\w-]*\\b/g)||[]).filter(e=>!/^(?:not|has|is|where|nth-child|nth-of-type|first-child|last-child)$/i.test(e)).length;
  }
  return {ids,classes:classes+attrs+pseudos,elements};
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('请输入CSS选择器');return;}
  const spec=calcSpecificity(input);
  const score=`${spec.ids},${spec.classes},${spec.elements}`;
  const lines=[
    `选择器: ${input}`,
    `优先级 (ID,Class,Element): (${score})`,
    ``,
    `ID选择器:     ${spec.ids}`,
    `类/属性/伪类: ${spec.classes}`,
    `元素/伪元素:  ${spec.elements}`,
    ``,
    `权重值: ${spec.ids*10000+spec.classes*100+spec.elements}`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="input-group">
    <label for="toolInput">Enter CSS Selector</label>
    <input type="text" id="toolInput" placeholder="e.g. #header .nav > ul li a:hover">
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Calculate Specificity</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function calcSpecificity(selector){
  const s=selector.trim();
  let ids=(s.match(/#[\\w-]+/g)||[]).length;
  let classes=(s.match(/\\.[\\w-]+/g)||[]).length;
  let attrs=(s.match(/\\[[^\\]]+\\]/g)||[]).length;
  let pseudos=(s.match(/:[\\w-]+(?=\\s|\\(|$)/g)||[]).length;
  let elements=(s.match(/(?:^|[\\s>+~,])([a-zA-Z][\\w-]*)(?![\\w-]*[\\]\\)])(?![\\w-]*\\()/g)||[]).filter(e=>!/^(?:not|has|is|where)$/i.test(e.replace(/[^a-zA-Z]/g,''))).length;
  if(!ids&&!classes&&!attrs&&!pseudos&&!elements){
    elements=(s.match(/\\b[a-zA-Z][\\w-]*\\b/g)||[]).filter(e=>!/^(?:not|has|is|where|nth-child|nth-of-type|first-child|last-child)$/i.test(e)).length;
  }
  return {ids,classes:classes+attrs+pseudos,elements};
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('Please enter a CSS selector');return;}
  const spec=calcSpecificity(input);
  const score=`${spec.ids},${spec.classes},${spec.elements}`;
  const lines=[
    `Selector: ${input}`,
    `Specificity (ID,Class,Element): (${score})`,
    ``,
    `ID selectors:      ${spec.ids}`,
    `Class/Attr/Pseudo: ${spec.classes}`,
    `Element/Pseudo-el: ${spec.elements}`,
    ``,
    `Weight: ${spec.ids*10000+spec.classes*100+spec.elements}`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 5. rss-to-json ===
tools['rss-to-json'] = {
    'cn': {
        'html': '''  <div class="input-group">
    <label for="toolInput">粘贴RSS/Atom XML内容</label>
    <textarea id="toolInput" placeholder="在此粘贴RSS或Atom Feed的XML内容..."></textarea>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">转换为JSON</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制JSON</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function xmlToJson(xml){
  try{
    const parser=new DOMParser();
    const doc=parser.parseFromString(xml,'text/xml');
    if(doc.querySelector('parsererror'))throw new Error('XML解析错误');
    function parse(node){
      if(node.nodeType===3)return node.nodeValue.trim()||null;
      if(node.nodeType!==1)return null;
      const obj={};
      const children=Array.from(node.childNodes);
      const textChildren=children.filter(c=>c.nodeType===3).map(c=>c.nodeValue.trim()).filter(Boolean);
      const elChildren=children.filter(c=>c.nodeType===1);

      if(elChildren.length===0&&textChildren.length===1){
        return textChildren[0];
      }

      const groups={};
      for(const el of elChildren){
        const name=el.nodeName;
        const val=parse(el);
        if(!groups[name])groups[name]=[];
        groups[name].push(val);
      }
      for(const [k,v] of Object.entries(groups)){
        obj[k]=v.length===1?v[0]:v;
      }
      if(textChildren.length>0&&Object.keys(obj).length===0){
        return textChildren.join(' ');
      }
      if(textChildren.length>0){
        obj['#text']=textChildren.join(' ');
      }
      return Object.keys(obj).length===0&&textChildren.length>0?textChildren.join(' '):obj;
    }
    return JSON.stringify(parse(doc.documentElement),null,2);
  }catch(e){
    return 'Error: '+e.message;
  }
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('请粘贴RSS/Atom XML内容');return;}
  const json=xmlToJson(input);
  $('resultContent').textContent=json;
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="input-group">
    <label for="toolInput">Paste RSS/Atom XML</label>
    <textarea id="toolInput" placeholder="Paste your RSS or Atom Feed XML here..."></textarea>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Convert to JSON</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy JSON</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function xmlToJson(xml){
  try{
    const parser=new DOMParser();
    const doc=parser.parseFromString(xml,'text/xml');
    if(doc.querySelector('parsererror'))throw new Error('XML parse error');
    function parse(node){
      if(node.nodeType===3)return node.nodeValue.trim()||null;
      if(node.nodeType!==1)return null;
      const obj={};
      const children=Array.from(node.childNodes);
      const textChildren=children.filter(c=>c.nodeType===3).map(c=>c.nodeValue.trim()).filter(Boolean);
      const elChildren=children.filter(c=>c.nodeType===1);

      if(elChildren.length===0&&textChildren.length===1){
        return textChildren[0];
      }

      const groups={};
      for(const el of elChildren){
        const name=el.nodeName;
        const val=parse(el);
        if(!groups[name])groups[name]=[];
        groups[name].push(val);
      }
      for(const [k,v] of Object.entries(groups)){
        obj[k]=v.length===1?v[0]:v;
      }
      if(textChildren.length>0&&Object.keys(obj).length===0){
        return textChildren.join(' ');
      }
      if(textChildren.length>0){
        obj['#text']=textChildren.join(' ');
      }
      return Object.keys(obj).length===0&&textChildren.length>0?textChildren.join(' '):obj;
    }
    return JSON.stringify(parse(doc.documentElement),null,2);
  }catch(e){
    return 'Error: '+e.message;
  }
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('Please paste RSS/Atom XML');return;}
  const json=xmlToJson(input);
  $('resultContent').textContent=json;
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 6. sql-diff ===
tools['sql-diff'] = {
    'cn': {
        'html': '''  <div class="input-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div class="input-group">
      <label for="toolInput">SQL版本 A</label>
      <textarea id="toolInput" placeholder="粘贴SQL版本A..."></textarea>
    </div>
    <div class="input-group">
      <label for="sqlB">SQL版本 B</label>
      <textarea id="sqlB" placeholder="粘贴SQL版本B..."></textarea>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">对比差异</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

$('btnProcess').addEventListener('click',()=>{
  const a=$('toolInput').value.split('\\n');
  const b=$('sqlB').value.split('\\n');
  if(!a.join('').trim()&&!b.join('').trim()){toast('请粘贴SQL内容');return;}

  const maxLen=Math.max(a.length,b.length);
  const result=[];
  for(let i=0;i<maxLen;i++){
    const la=a[i]||'',lb=b[i]||'';
    if(la===lb)result.push(`  ${i+1}: ${la}`);
    else{
      if(la)result.push(`- ${i+1}: ${la}`);
      if(lb)result.push(`+ ${i+1}: ${lb}`);
    }
  }
  const added=b.length-a.length;
  const removed=a.length-b.length;
  const changed=result.filter(l=>l.startsWith('-')||l.startsWith('+')).length;
  const summary=`=== 差异统计 ===\\n新增行: ${added>0?added:0} | 删除行: ${removed>0?removed:0} | 变更行: ${changed}\\n\\n`;
  $('resultContent').textContent=summary+result.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('sqlB').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="input-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div class="input-group">
      <label for="toolInput">SQL Version A</label>
      <textarea id="toolInput" placeholder="Paste SQL version A..."></textarea>
    </div>
    <div class="input-group">
      <label for="sqlB">SQL Version B</label>
      <textarea id="sqlB" placeholder="Paste SQL version B..."></textarea>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Compare Diff</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

$('btnProcess').addEventListener('click',()=>{
  const a=$('toolInput').value.split('\\n');
  const b=$('sqlB').value.split('\\n');
  if(!a.join('').trim()&&!b.join('').trim()){toast('Please paste SQL content');return;}

  const maxLen=Math.max(a.length,b.length);
  const result=[];
  for(let i=0;i<maxLen;i++){
    const la=a[i]||'',lb=b[i]||'';
    if(la===lb)result.push(`  ${i+1}: ${la}`);
    else{
      if(la)result.push(`- ${i+1}: ${la}`);
      if(lb)result.push(`+ ${i+1}: ${lb}`);
    }
  }
  const added=b.length-a.length;
  const removed=a.length-b.length;
  const changed=result.filter(l=>l.startsWith('-')||l.startsWith('+')).length;
  const summary=`=== Diff Summary ===\\nAdded: ${added>0?added:0} | Removed: ${removed>0?removed:0} | Changed: ${changed}\\n\\n`;
  $('resultContent').textContent=summary+result.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('sqlB').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 7. fake-identity-generator ===
tools['fake-identity-generator'] = {
    'cn': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="toolInput">生成数量</label>
      <input type="number" id="toolInput" value="5" min="1" max="100">
    </div>
    <div class="input-group">
      <label for="locale">国家/地区</label>
      <select id="locale"><option value="zh">中国</option><option value="en">美国</option><option value="uk">英国</option><option value="jp">日本</option></select>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">生成假身份</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制结果</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

const DATA={
  zh:{first:'张李王赵刘陈杨黄周吴徐孙马胡朱郭何罗高林',last:'伟芳娜秀英敏静丽强磊洋勇艳杰军涛明超平刚华飞龙斌',
    streets:'中山路解放路人民路建设路文化路和平路长安街南京路北京路',cities:'北京上海广州深圳杭州成都武汉南京重庆西安',tlds:'@qq.com,@163.com,@126.com'},
  en:{first:'JamesJohnRobertMichaelWilliamDavidRichardJosephThomasCharlesMaryPatriciaJenniferLindaElizabethBarbaraSusanJessicaSarah',
    last:'SmithJohnsonWilliamsBrownJonesGarciaMillerDavisRodriguezMartinezHernandezLopezGonzalezWilsonAnderson',
    streets:'MainOakElmMaplePineCedarParkWashingtonLakeHill',cities:'NewYorkLosAngelesChicagoHoustonPhoenixPhiladelphiaSanAntonioSanDiegoDallas',
    tlds:'@gmail.com,@yahoo.com,@outlook.com,@hotmail.com'},
  uk:{first:'JamesJohnRobertMichaelWilliamDavidRichardJosephThomasCharlesMaryPatriciaJenniferLindaElizabethBarbaraSusanJessicaSarah',
    last:'SmithJonesWilliamsTaylorBrownDaviesEvansWilsonThomasRobertsJohnsonWalkerWrightRobinson',
    streets:'HighStreetStationRoadChurchLaneChurchStreetLondonRoadGreenLaneMillLane',cities:'LondonManchesterBirminghamLeedsLiverpoolGlasgowEdinburghBristolSheffield',
    tlds:'@gmail.com,@yahoo.co.uk,@outlook.com,@hotmail.co.uk'},
  jp:{first:'佐藤鈴木高橋田中伊藤渡辺山本中村小林加藤吉田山崎山口松本井上木村林斎藤清水',last:'一郎二郎三郎太郎花子美咲愛子優子',
    streets:'中央通り駅前通り銀座通り本町通り大通り',cities:'東京大阪横浜名古屋札幌神戸京都福岡川崎',
    tlds:'@gmail.com,@yahoo.co.jp,@docomo.ne.jp,@ezweb.ne.jp'}
};

function rand(arr){return arr[Math.floor(Math.random()*arr.length)];}
function randNum(min,max){return Math.floor(Math.random()*(max-min+1))+min;}

$('btnProcess').addEventListener('click',()=>{
  const count=parseInt($('toolInput').value)||5;
  const locale=$('locale').value;
  const d=DATA[locale]||DATA.en;
  const results=[];
  const firstArr=[...d.first.match(/.{1,2}/g)||[]];
  const lastArr=[...d.last.match(/.{1,2}/g)||[]];
  const streetArr=d.streets.split(/[、,]/);
  const cityArr=d.cities.split(/[、,]/);
  const tldArr=d.tlds.split(',');

  for(let i=0;i<Math.min(count,100);i++){
    const firstName=rand(firstArr);
    const lastName=rand(lastArr);
    const street=rand(streetArr);
    const city=rand(cityArr);
    const tld=rand(tldArr);
    const email=(firstName+lastName+randNum(0,999)).toLowerCase()+tld;
    const phone=`1${randNum(3,9)}${String(randNum(0,99999999)).padStart(8,'0')}`;

    results.push([
      `=== 身份 #${i+1} ===`,
      `姓名: ${firstName}${lastName}`,
      `性别: ${Math.random()>0.5?'男':'女'}`,
      `年龄: ${randNum(18,65)}`,
      `电话: ${phone}`,
      `邮箱: ${email}`,
      `地址: ${city}市${street}${randNum(1,500)}号`,
      `邮编: ${String(randNum(100000,999999))}`,
      `公司: ${rand(cityArr)}科技有限公司`,
    ].join('\\n'));
  }
  $('resultContent').textContent=results.join('\\n\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='5';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="toolInput">Count</label>
      <input type="number" id="toolInput" value="5" min="1" max="100">
    </div>
    <div class="input-group">
      <label for="locale">Region</label>
      <select id="locale"><option value="zh">China</option><option value="en">USA</option><option value="uk">UK</option><option value="jp">Japan</option></select>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Generate</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

const DATA={
  zh:{first:'张李王赵刘陈杨黄周吴徐孙马胡朱郭何罗高林',last:'伟芳娜秀英敏静丽强磊洋勇艳杰军涛明超平刚华飞龙斌',
    streets:'Zhongshan,Jiefang,Renmin,Jianshe,Wenhua,Heping,Changan,Nanjing,Beijing',cities:'Beijing,Shanghai,Guangzhou,Shenzhen,Hangzhou,Chengdu,Wuhan,Nanjing,Chongqing,Xian',tlds:'@qq.com,@163.com,@126.com'},
  en:{first:'JamesJohnRobertMichaelWilliamDavidRichardJosephThomasCharlesMaryPatriciaJenniferLindaElizabethBarbaraSusanJessicaSarah',
    last:'SmithJohnsonWilliamsBrownJonesGarciaMillerDavisRodriguezMartinezHernandezLopezGonzalezWilsonAnderson',
    streets:'Main,Oak,Elm,Maple,Pine,Cedar,Park,Washington,Lake,Hill',cities:'NewYork,LosAngeles,Chicago,Houston,Phoenix,Philadelphia,SanAntonio,SanDiego,Dallas',
    tlds:'@gmail.com,@yahoo.com,@outlook.com,@hotmail.com'},
  uk:{first:'JamesJohnRobertMichaelWilliamDavidRichardJosephThomasCharlesMaryPatriciaJenniferLindaElizabethBarbaraSusanJessicaSarah',
    last:'SmithJonesWilliamsTaylorBrownDaviesEvansWilsonThomasRobertsJohnsonWalkerWrightRobinson',
    streets:'HighStreet,StationRoad,ChurchLane,ChurchStreet,LondonRoad,GreenLane,MillLane',cities:'London,Manchester,Birmingham,Leeds,Liverpool,Glasgow,Edinburgh,Bristol,Sheffield',
    tlds:'@gmail.com,@yahoo.co.uk,@outlook.com,@hotmail.co.uk'},
  jp:{first:'SatoSuzukiTakahashiTanakaItoWatanabeYamamotoNakamuraKobayashiKatoYoshidaYamazakiYamaguchiMatsumotoInoueKimuraHayashiSaitoShimizu',last:'IchiroJiroSaburoTaroHanakoMisakiAikoYuko',
    streets:'Chuo-dori,Ekimae-dori,Ginza-dori,Hommachi-dori,Odori',cities:'Tokyo,Osaka,Yokohama,Nagoya,Sapporo,Kobe,Kyoto,Fukuoka,Kawasaki',
    tlds:'@gmail.com,@yahoo.co.jp,@docomo.ne.jp,@ezweb.ne.jp'}
};

function rand(arr){return arr[Math.floor(Math.random()*arr.length)];}
function randNum(min,max){return Math.floor(Math.random()*(max-min+1))+min;}

$('btnProcess').addEventListener('click',()=>{
  const count=parseInt($('toolInput').value)||5;
  const locale=$('locale').value;
  const d=DATA[locale]||DATA.en;
  const results=[];
  const firstArr=[...d.first.match(/.{1,2}/g)||[]];
  const lastArr=[...d.last.match(/.{1,2}/g)||[]];
  const streetArr=d.streets.split(',');
  const cityArr=d.cities.split(',');
  const tldArr=d.tlds.split(',');

  for(let i=0;i<Math.min(count,100);i++){
    const firstName=rand(firstArr);
    const lastName=rand(lastArr);
    const street=rand(streetArr);
    const city=rand(cityArr);
    const tld=rand(tldArr);
    const email=(firstName+lastName+randNum(0,999)).toLowerCase()+tld;
    const phone=`+1${randNum(200,999)}${String(randNum(0,9999999)).padStart(7,'0')}`;

    results.push([
      `=== Identity #${i+1} ===`,
      `Name: ${firstName} ${lastName}`,
      `Gender: ${Math.random()>0.5?'Male':'Female'}`,
      `Age: ${randNum(18,65)}`,
      `Phone: ${phone}`,
      `Email: ${email}`,
      `Address: ${randNum(100,9999)} ${rand(streetArr)} St, ${rand(cityArr)}`,
      `ZIP: ${String(randNum(10000,99999))}`,
      `Company: ${rand(cityArr)} Technologies`,
    ].join('\\n'));
  }
  $('resultContent').textContent=results.join('\\n\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='5';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 8. cicd-pipeline-generator ===
tools['cicd-pipeline-generator'] = {
    'cn': {
        'html': '''  <div class="input-group">
    <label for="pipelineType">CI/CD 平台</label>
    <select id="pipelineType"><option value="github">GitHub Actions</option><option value="gitlab">GitLab CI</option><option value="jenkins">Jenkins</option></select>
  </div>
  <div class="input-group">
    <label for="toolInput">项目名称</label>
    <input type="text" id="toolInput" placeholder="my-app">
  </div>
  <div class="input-group">
    <label>触发条件</label>
    <div class="btn-row" style="margin-top:4px">
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkPush" checked> Push</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkPR" checked> Pull Request</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkSched"> 定时</label>
    </div>
  </div>
  <div class="input-group">
    <label>流水线阶段</label>
    <div class="btn-row" style="margin-top:4px">
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkLint" checked> 代码检查</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkTest" checked> 测试</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkBuild" checked> 构建</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkDeploy"> 部署</label>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">生成配置</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制配置</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ghActions(name,push,pr,sched,lint,test,build,deploy){
  const lines=['name: CI Pipeline','','on:'];
  if(push)lines.push('  push:','    branches: [ main, develop ]');
  if(pr)lines.push('  pull_request:','    branches: [ main ]');
  if(sched)lines.push('  schedule:','    - cron: "0 8 * * 1-5"');
  lines.push('','jobs:','  pipeline:','    runs-on: ubuntu-latest','    steps:','      - uses: actions/checkout@v4');
  if(lint)lines.push('      - name: Lint','        run: npm run lint');
  if(test)lines.push('      - name: Test','        run: npm test');
  if(build)lines.push('      - name: Build','        run: npm run build');
  if(deploy)lines.push('      - name: Deploy','        run: |','          echo "Deploying..."');
  return lines.join('\\n');
}

function gitlabCI(name,push,pr,sched,lint,test,build,deploy){
  const lines=['stages:'];
  const stages=[];
  if(lint)stages.push('lint');
  if(test)stages.push('test');
  if(build)stages.push('build');
  if(deploy)stages.push('deploy');
  if(stages.length===0)stages.push('build');
  lines.push('  - '+stages.join('\\n  - '));
  lines.push('','variables:','  PROJECT: '+name);
  if(lint){lines.push('','lint:','  stage: lint','  script:','    - npm run lint');}
  if(test){lines.push('','test:','  stage: test','  script:','    - npm test');}
  if(build){lines.push('','build:','  stage: build','  script:','    - npm run build','  artifacts:','    paths:','      - dist/');}
  if(deploy){lines.push('','deploy:','  stage: deploy','  script:','    - echo "Deploying..."','  only:','    - main');}
  return lines.join('\\n');
}

$('btnProcess').addEventListener('click',()=>{
  const name=$('toolInput').value.trim()||'my-app';
  const type=$('pipelineType').value;
  const push=$('chkPush').checked,pr=$('chkPR').checked,sched=$('chkSched').checked;
  const lint=$('chkLint').checked,test=$('chkTest').checked,build=$('chkBuild').checked,deploy=$('chkDeploy').checked;
  let yaml='';
  if(type==='github')yaml=ghActions(name,push,pr,sched,lint,test,build,deploy);
  else if(type==='gitlab')yaml=gitlabCI(name,push,pr,sched,lint,test,build,deploy);
  else yaml='# Jenkinsfile\\npipeline {\\n  agent any\\n  stages {\\n'+((lint?'    stage("Lint") { steps { sh "npm run lint" } }\\n':''))+((test?'    stage("Test") { steps { sh "npm test" } }\\n':''))+((build?'    stage("Build") { steps { sh "npm run build" } }\\n':''))+((deploy?'    stage("Deploy") { steps { sh "deploy.sh" } }\\n':''))+'  }\\n}';
  $('resultContent').textContent=yaml;
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="input-group">
    <label for="pipelineType">CI/CD Platform</label>
    <select id="pipelineType"><option value="github">GitHub Actions</option><option value="gitlab">GitLab CI</option><option value="jenkins">Jenkins</option></select>
  </div>
  <div class="input-group">
    <label for="toolInput">Project Name</label>
    <input type="text" id="toolInput" placeholder="my-app">
  </div>
  <div class="input-group">
    <label>Triggers</label>
    <div class="btn-row" style="margin-top:4px">
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkPush" checked> Push</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkPR" checked> Pull Request</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkSched"> Scheduled</label>
    </div>
  </div>
  <div class="input-group">
    <label>Stages</label>
    <div class="btn-row" style="margin-top:4px">
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkLint" checked> Lint</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkTest" checked> Test</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkBuild" checked> Build</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkDeploy"> Deploy</label>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Generate Config</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy Config</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ghActions(name,push,pr,sched,lint,test,build,deploy){
  const lines=['name: CI Pipeline','','on:'];
  if(push)lines.push('  push:','    branches: [ main, develop ]');
  if(pr)lines.push('  pull_request:','    branches: [ main ]');
  if(sched)lines.push('  schedule:','    - cron: "0 8 * * 1-5"');
  lines.push('','jobs:','  pipeline:','    runs-on: ubuntu-latest','    steps:','      - uses: actions/checkout@v4');
  if(lint)lines.push('      - name: Lint','        run: npm run lint');
  if(test)lines.push('      - name: Test','        run: npm test');
  if(build)lines.push('      - name: Build','        run: npm run build');
  if(deploy)lines.push('      - name: Deploy','        run: |','          echo "Deploying..."');
  return lines.join('\\n');
}

function gitlabCI(name,push,pr,sched,lint,test,build,deploy){
  const lines=['stages:'];
  const stages=[];
  if(lint)stages.push('lint');
  if(test)stages.push('test');
  if(build)stages.push('build');
  if(deploy)stages.push('deploy');
  if(stages.length===0)stages.push('build');
  lines.push('  - '+stages.join('\\n  - '));
  lines.push('','variables:','  PROJECT: '+name);
  if(lint){lines.push('','lint:','  stage: lint','  script:','    - npm run lint');}
  if(test){lines.push('','test:','  stage: test','  script:','    - npm test');}
  if(build){lines.push('','build:','  stage: build','  script:','    - npm run build','  artifacts:','    paths:','      - dist/');}
  if(deploy){lines.push('','deploy:','  stage: deploy','  script:','    - echo "Deploying..."','  only:','    - main');}
  return lines.join('\\n');
}

$('btnProcess').addEventListener('click',()=>{
  const name=$('toolInput').value.trim()||'my-app';
  const type=$('pipelineType').value;
  const push=$('chkPush').checked,pr=$('chkPR').checked,sched=$('chkSched').checked;
  const lint=$('chkLint').checked,test=$('chkTest').checked,build=$('chkBuild').checked,deploy=$('chkDeploy').checked;
  let yaml='';
  if(type==='github')yaml=ghActions(name,push,pr,sched,lint,test,build,deploy);
  else if(type==='gitlab')yaml=gitlabCI(name,push,pr,sched,lint,test,build,deploy);
  else yaml='# Jenkinsfile\\npipeline {\\n  agent any\\n  stages {\\n'+((lint?'    stage("Lint") { steps { sh "npm run lint" } }\\n':''))+((test?'    stage("Test") { steps { sh "npm test" } }\\n':''))+((build?'    stage("Build") { steps { sh "npm run build" } }\\n':''))+((deploy?'    stage("Deploy") { steps { sh "deploy.sh" } }\\n':''))+'  }\\n}';
  $('resultContent').textContent=yaml;
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# === 9. html-color-picker ===
tools['html-color-picker'] = {
    'cn': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="toolInput">颜色值 (HEX/RGB/HSL)</label>
      <input type="text" id="toolInput" placeholder="#4F46E5 或 rgb(79,70,229) 或 hsl(240,80%,59%)">
    </div>
    <div class="input-group" style="flex:0 0 auto">
      <label for="colorPreview">&nbsp;</label>
      <div id="colorPreview" style="width:48px;height:48px;border-radius:8px;border:2px solid rgba(148,163,184,.2);background:#4F46E5"></div>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">解析颜色</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制结果</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function parseColor(input){
  let r,g,b;
  const hex=input.match(/^#?([a-f0-9]{3}|[a-f0-9]{6})$/i);
  if(hex){
    let h=hex[1];
    if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    r=parseInt(h.slice(0,2),16);
    g=parseInt(h.slice(2,4),16);
    b=parseInt(h.slice(4,6),16);
    return {r,g,b};
  }
  const rgb=input.match(/rgba?\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/);
  if(rgb)return {r:+rgb[1],g:+rgb[2],b:+rgb[3]};
  const hsl=input.match(/hsla?\\(\\s*(\\d+)\\s*,\\s*(\\d+)%?\\s*,\\s*(\\d+)%?/);
  if(hsl){
    const h=+hsl[1]/360,s=+hsl[2]/100,l=+hsl[3]/100;
    if(s===0){r=g=b=Math.round(l*255);}
    else{
      const hue2rgb=(p,q,t)=>{if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;};
      const q=l<0.5?l*(1+s):l+s-l*s;
      const p=2*l-q;
      r=Math.round(hue2rgb(p,q,h+1/3)*255);
      g=Math.round(hue2rgb(p,q,h)*255);
      b=Math.round(hue2rgb(p,q,h-1/3)*255);
    }
    return {r,g,b};
  }
  return null;
}

function rgbToHsl(r,g,b){
  r/=255;g/=255;b/=255;
  const max=Math.max(r,g,b),min=Math.min(r,g,b);
  let h=0,s=0,l=(max+min)/2;
  if(max!==min){
    const d=max-min;
    s=l>0.5?d/(2-max-min):d/(max+min);
    switch(max){
      case r:h=(g-b)/d+(g<b?6:0);break;
      case g:h=(b-r)/d+2;break;
      case b:h=(r-g)/d+4;break;
    }
    h/=6;
  }
  return {h:Math.round(h*360),s:Math.round(s*100),l:Math.round(l*100)};
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('请输入颜色值');return;}
  const color=parseColor(input);
  if(!color){toast('无法解析颜色，请使用HEX/RGB/HSL格式');return;}
  const {r,g,b}=color;
  const hex='#'+[r,g,b].map(c=>c.toString(16).padStart(2,'0')).join('').toUpperCase();
  const hsl=rgbToHsl(r,g,b);
  $('colorPreview').style.background=hex;
  const lines=[
    `HEX: ${hex}`,
    `RGB: rgb(${r}, ${g}, ${b})`,
    `HSL: hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`,
    ``,
    `CSS: ${hex}`,
    `亮度: ${Math.round((0.299*r+0.587*g+0.114*b)/2.55)}%`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';$('colorPreview').style.background='#4F46E5';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''
    },
    'en': {
        'html': '''  <div class="row">
    <div class="input-group">
      <label for="toolInput">Color Value (HEX/RGB/HSL)</label>
      <input type="text" id="toolInput" placeholder="#4F46E5 or rgb(79,70,229) or hsl(240,80%,59%)">
    </div>
    <div class="input-group" style="flex:0 0 auto">
      <label for="colorPreview">&nbsp;</label>
      <div id="colorPreview" style="width:48px;height:48px;border-radius:8px;border:2px solid rgba(148,163,184,.2);background:#4F46E5"></div>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Parse Color</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy</button>
  </div>''',
        'js': '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function parseColor(input){
  let r,g,b;
  const hex=input.match(/^#?([a-f0-9]{3}|[a-f0-9]{6})$/i);
  if(hex){
    let h=hex[1];
    if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    r=parseInt(h.slice(0,2),16);
    g=parseInt(h.slice(2,4),16);
    b=parseInt(h.slice(4,6),16);
    return {r,g,b};
  }
  const rgb=input.match(/rgba?\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/);
  if(rgb)return {r:+rgb[1],g:+rgb[2],b:+rgb[3]};
  const hsl=input.match(/hsla?\\(\\s*(\\d+)\\s*,\\s*(\\d+)%?\\s*,\\s*(\\d+)%?/);
  if(hsl){
    const h=+hsl[1]/360,s=+hsl[2]/100,l=+hsl[3]/100;
    if(s===0){r=g=b=Math.round(l*255);}
    else{
      const hue2rgb=(p,q,t)=>{if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;};
      const q=l<0.5?l*(1+s):l+s-l*s;
      const p=2*l-q;
      r=Math.round(hue2rgb(p,q,h+1/3)*255);
      g=Math.round(hue2rgb(p,q,h)*255);
      b=Math.round(hue2rgb(p,q,h-1/3)*255);
    }
    return {r,g,b};
  }
  return null;
}

function rgbToHsl(r,g,b){
  r/=255;g/=255;b/=255;
  const max=Math.max(r,g,b),min=Math.min(r,g,b);
  let h=0,s=0,l=(max+min)/2;
  if(max!==min){
    const d=max-min;
    s=l>0.5?d/(2-max-min):d/(max+min);
    switch(max){
      case r:h=(g-b)/d+(g<b?6:0);break;
      case g:h=(b-r)/d+2;break;
      case b:h=(r-g)/d+4;break;
    }
    h/=6;
  }
  return {h:Math.round(h*360),s:Math.round(s*100),l:Math.round(l*100)};
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('Please enter a color value');return;}
  const color=parseColor(input);
  if(!color){toast('Cannot parse color. Use HEX/RGB/HSL format');return;}
  const {r,g,b}=color;
  const hex='#'+[r,g,b].map(c=>c.toString(16).padStart(2,'0')).join('').toUpperCase();
  const hsl=rgbToHsl(r,g,b);
  $('colorPreview').style.background=hex;
  const lines=[
    `HEX: ${hex}`,
    `RGB: rgb(${r}, ${g}, ${b})`,
    `HSL: hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`,
    ``,
    `CSS: ${hex}`,
    `Luminance: ${Math.round((0.299*r+0.587*g+0.114*b)/2.55)}%`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';$('colorPreview').style.background='#4F46E5';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''
    }
}

# ==================== 执行替换 ====================

DEFAULT_CN_HTML = '''  <div class="input-group">
    <label for="toolInput">输入内容</label>
    <textarea id="toolInput" placeholder="请在此输入..."></textarea>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">立即处理</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
    <button class="btn btn-secondary" id="btnCopy">复制结果</button>
  </div>'''

DEFAULT_EN_HTML = '''  <div class="input-group">
    <label for="toolInput">Input</label>
    <textarea id="toolInput" placeholder="Enter your content here..."></textarea>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Process</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy Result</button>
  </div>'''

DEFAULT_CN_JS = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};
// PLACEHOLDER: tool logic here
$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('请输入内容');return;}
  // TOOL_SPECIFIC_LOGIC
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制到剪贴板')).catch(()=>toast('复制失败'));});'''

DEFAULT_EN_JS = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};
// PLACEHOLDER: tool logic here
$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  if(!input){toast('Please enter content');return;}
  // TOOL_SPECIFIC_LOGIC
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''

for name, data in tools.items():
    for lang in ['cn', 'en']:
        prefix = '' if lang == 'cn' else 'en/'
        filepath = os.path.join(BASE, f'{prefix}{name}/index.html')
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace HTML
        old_html = DEFAULT_CN_HTML if lang == 'cn' else DEFAULT_EN_HTML
        new_html = data[lang]['html']
        if old_html in content:
            content = content.replace(old_html, new_html)
        else:
            print(f'WARN: HTML pattern not found in {filepath}')
        
        # Replace JS
        old_js = DEFAULT_CN_JS if lang == 'cn' else DEFAULT_EN_JS
        new_js = data[lang]['js']
        if old_js in content:
            content = content.replace(old_js, new_js)
        else:
            print(f'WARN: JS pattern not found in {filepath}')
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'OK: {filepath}')

print('\nAll tools injected!')