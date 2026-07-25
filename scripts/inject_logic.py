#!/usr/bin/env python3
"""注入每个工具的实际JS逻辑和HTML UI"""
import os

# ==================== 1. domain-typo-generator EN ====================
en_domain_typo_html = '''  <div class="input-group">
    <label for="toolInput">Enter Domain (no protocol, e.g. example.com)</label>
    <input type="text" id="toolInput" placeholder="example.com">
  </div>

  <div class="input-group">
    <label>Error Types</label>
    <div class="btn-row" style="margin-top:4px" id="errorTypes">
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkOmit" checked> Omission</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkInsert" checked> Insertion</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkSwap" checked> Transposition</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkReplace" checked> Replacement</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkDot" checked> Missing/Extra Dot</label>
      <label style="color:#94a3b8;font-size:.85rem"><input type="checkbox" id="chkTld" checked> TLD Variants</label>
    </div>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">Generate Typos</button>
    <button class="btn btn-secondary" id="btnClear">Clear</button>
    <button class="btn btn-secondary" id="btnCopy">Copy Results</button>
  </div>'''

en_domain_typo_js = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

const NEARBY={'a':'qwsz','b':'vghn','c':'xdfv','d':'serfcx','e':'wsdr','f':'drtgc','g':'tgfhvb','h':'yugjbn','i':'uojk','j':'hknmui','k':'jm,loij','l':'k;.,opk','m':'njkl','n':'bhjm','o':'iklp','p':'0ol-;','q':'12wa','r':'45tfde','s':'awedxza','t':'56ygrf','u':'78yhji','v':'cfgb','w':'23qase','x':'zsdc','y':'67tghu','z':'asx','0':'9op-','1':'2qw','2':'13wqe','3':'24ewr','4':'35rte','5':'46tyr','6':'57yut','7':'68uig','8':'79ioh','9':'80opj'};
const TLD_VARIANTS=['.com','.net','.org','.co','.io','.dev','.app','.ai','.biz','.info','.xyz','.cn','.us','.eu','.uk'];

function getTLD(domain){
  const parts=domain.split('.');
  if(parts.length<2)return {name:domain,tld:''};
  return {name:parts.slice(0,-1).join('.'),tld:'.'+parts[parts.length-1]};
}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim().toLowerCase();
  if(!input){toast('Please enter a domain');return;}
  const {name,tld}=getTLD(input);
  if(!tld){toast('Please enter a full domain with TLD');return;}
  if(name.length<2){toast('Domain too short to generate typos');return;}
  const result=new Set();

  if($('chkOmit').checked){
    for(let i=0;i<name.length;i++)result.add(name.slice(0,i)+name.slice(i+1)+tld);
  }
  if($('chkInsert').checked){
    for(let i=0;i<=name.length;i++){
      for(const c of 'abcdefghijklmnopqrstuvwxyz'){
        result.add(name.slice(0,i)+c+name.slice(i)+tld);
      }
    }
  }
  if($('chkSwap').checked){
    for(let i=0;i<name.length-1;i++){
      const arr=name.split('');
      [arr[i],arr[i+1]]=[arr[i+1],arr[i]];
      result.add(arr.join('')+tld);
    }
  }
  if($('chkReplace').checked){
    for(let i=0;i<name.length;i++){
      const nearby=NEARBY[name[i]]||'';
      for(const c of nearby){
        result.add(name.slice(0,i)+c+name.slice(i+1)+tld);
      }
    }
  }
  if($('chkDot').checked){
    const parts=name.split('.');
    if(parts.length===1){
      for(let i=1;i<name.length;i++)result.add(name.slice(0,i)+'.'+name.slice(i)+tld);
    }
    result.add(name.replace(/\\./g,'')+tld);
  }
  if($('chkTld').checked){
    for(const vtld of TLD_VARIANTS){
      if(vtld!==tld)result.add(name+vtld);
    }
  }
  result.delete(input);
  const arr=[...result].sort();
  if(arr.length===0){toast('No typos generated');return;}
  $('resultContent').textContent=arr.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''

# ==================== 2. subnet-mask-calc ====================
subnet_html = '''  <div class="input-group">
    <label for="toolInput">输入IP/CIDR (如 192.168.1.0/24)</label>
    <input type="text" id="toolInput" placeholder="192.168.1.0/24">
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" id="btnProcess">计算子网</button>
    <button class="btn btn-secondary" id="btnClear">清除</button>
  </div>'''

subnet_js_cn = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ipToInt(ip){return ip.split('.').reduce((s,o)=>s*256+parseInt(o),0)>>>0;}
function intToIp(n){return [(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255].join('.');}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  const match=input.match(/^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})\\/(\\d{1,2})$/);
  if(!match){toast('格式错误，请使用 IP/CIDR 格式，如 192.168.1.0/24');return;}
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
    `IP类型:     ${cidr===32?'单主机':cidr===31?'点对点(CIDR<31?hosts>65536?'超大型网络':'常规子网':'')}`
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});'''

subnet_js_en = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

function ipToInt(ip){return ip.split('.').reduce((s,o)=>s*256+parseInt(o),0)>>>0;}
function intToIp(n){return [(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255].join('.');}

$('btnProcess').addEventListener('click',()=>{
  const input=$('toolInput').value.trim();
  const match=input.match(/^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})\\/(\\d{1,2})$/);
  if(!match){toast('Invalid format. Use IP/CIDR, e.g. 192.168.1.0/24');return;}
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
    `Type:          ${cidr===32?'Single Host':cidr===31?'Point-to-Point':'Subnet'}`
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('toolInput').value='';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});'''

# ==================== 3. api-rate-limiter-calc ====================
apirate_html = '''  <div class="row">
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
  </div>'''

apirate_js_cn = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

$('btnProcess').addEventListener('click',()=>{
  const limit=parseInt($('rateLimit').value)||100;
  const window=parseInt($('rateWindow').value)||60;
  if(limit<1||window<1){toast('请输入有效数值');return;}
  const rps=limit/window;
  const per10s=Math.floor(rps*10);
  const perMin=Math.floor(rps*60);
  const perHour=Math.floor(rps*3600);
  const lines=[
    `=== 速率限制分析 ===`,
    ``,
    `配置: ${limit} 请求 / ${window} 秒`,
    `平均速率: ${rps.toFixed(2)} 请求/秒`,
    ``,
    `--- 固定窗口策略 ---`,
    `每10秒配额:   ${per10s} 请求`,
    `每分钟配额:   ${perMin} 请求`,
    `每小时配额:   ${perHour.toLocaleString()} 请求`,
    ``,
    `--- 令牌桶策略 ---`,
    `填充速率:     ${rps.toFixed(2)} 令牌/秒`,
    `桶容量(推荐): ${limit} 令牌`,
    `恢复1个令牌:  ${Math.ceil(1/rps*1000)}ms`,
    `恢复全桶:     ${window}秒`,
    ``,
    `--- 滑动窗口策略 ---`,
    `窗口大小:     ${window}秒`,
    `最大突发:     ${limit} 请求（窗口内）`,
    `建议间隔:     ${Math.ceil(window/limit*1000)}ms 均匀分布`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('rateLimit').value='100';$('rateWindow').value='60';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('已复制')).catch(()=>toast('复制失败'));});
$('btnProcess').click();'''

apirate_js_en = '''const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)};

$('btnProcess').addEventListener('click',()=>{
  const limit=parseInt($('rateLimit').value)||100;
  const window=parseInt($('rateWindow').value)||60;
  if(limit<1||window<1){toast('Please enter valid numbers');return;}
  const rps=limit/window;
  const per10s=Math.floor(rps*10);
  const perMin=Math.floor(rps*60);
  const perHour=Math.floor(rps*3600);
  const lines=[
    `=== Rate Limiter Analysis ===`,
    ``,
    `Config: ${limit} requests / ${window}s`,
    `Avg Rate: ${rps.toFixed(2)} req/s`,
    ``,
    `--- Fixed Window ---`,
    `Per 10s:   ${per10s} requests`,
    `Per min:   ${perMin} requests`,
    `Per hour:  ${perHour.toLocaleString()} requests`,
    ``,
    `--- Token Bucket ---`,
    `Fill rate:     ${rps.toFixed(2)} tokens/s`,
    `Bucket (rec): ${limit} tokens`,
    `Refill 1 token: ${Math.ceil(1/rps*1000)}ms`,
    `Refill all:     ${window}s`,
    ``,
    `--- Sliding Window ---`,
    `Window:        ${window}s`,
    `Max burst:     ${limit} requests`,
    `Even spacing:  ${Math.ceil(window/limit*1000)}ms`,
  ];
  $('resultContent').textContent=lines.join('\\n');
  $('resultPanel').style.display='block';
});
$('btnClear').addEventListener('click',()=>{$('rateLimit').value='100';$('rateWindow').value='60';$('resultPanel').style.display='none';});
$('btnCopy').addEventListener('click',()=>{const r=$('resultContent').textContent;if(!r)return;navigator.clipboard.writeText(r).then(()=>toast('Copied!')).catch(()=>toast('Copy failed'));});
$('btnProcess').click();'''

print("Functions defined. Now will write files via patch...")
print("OK - all logic defs ready")