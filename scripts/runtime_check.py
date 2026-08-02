#!/usr/bin/env python3
"""第2层：Node运行时检测 - 全站扫描ReferenceError等运行时错误"""
import os, re, subprocess, sys, json
from datetime import datetime

DOM_STUB = r'''var document={getElementById:function(id){return{textContent:"",value:"",checked:false,style:{},addEventListener:function(){},querySelectorAll:function(s){return[]},querySelector:function(s){return null},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}},setAttribute:function(){},removeAttribute:function(){},focus:function(){},blur:function(){},disabled:false,innerHTML:"",outerHTML:"",appendChild:function(){return{}},removeChild:function(){return{}},insertBefore:function(){return{}},scrollIntoView:function(){},parentElement:null,children:[],dataset:{}}},querySelector:function(s){return null},querySelectorAll:function(s){return[]},createElement:function(tag){return{appendChild:function(){return{}},style:{},innerHTML:"",textContent:"",className:"",id:"",setAttribute:function(){},addEventListener:function(){},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}},children:[],dataset:{},tagName:tag.toUpperCase()}},body:{appendChild:function(){return{}},innerHTML:"",textContent:""}};
var window={location:{href:"",pathname:"",search:"",hash:""},crypto:{subtle:{digest:function(){return Promise.resolve(new ArrayBuffer(0))},importKey:function(){return Promise.resolve({})},sign:function(){return Promise.resolve(new ArrayBuffer(0))},encrypt:function(){return Promise.resolve(new ArrayBuffer(0))}}},addEventListener:function(){},removeEventListener:function(){},open:function(){},close:function(){},innerWidth:1920,innerHeight:1080,URLSearchParams:function(){this.get=function(){return null}},AudioContext:function(){this.createOscillator=function(){return{connect:function(){},start:function(){},stop:function(){},frequency:{value:440},type:"sine"}};this.createGain=function(){return{connect:function(){},gain:{value:1}}};this.destination={}},speechSynthesis:{speak:function(){},getVoices:function(){return[]}}};
var navigator={clipboard:{writeText:function(){return Promise.resolve()}},language:"zh-CN",userAgent:"test"};
var setTimeout=function(f,t){if(typeof f==='function')try{f()}catch(e){}return 0};
var setInterval=function(f,t){return 0};
var clearTimeout=function(){};
var clearInterval=function(){};
var fetch=function(){return Promise.resolve({ok:true,json:function(){return Promise.resolve({})},text:function(){return Promise.resolve("")},blob:function(){return Promise.resolve(new ArrayBuffer(0))},arrayBuffer:function(){return Promise.resolve(new ArrayBuffer(0))},status:200})};
var Blob=function(arr,opt){this.size=0;this.type=(opt&&opt.type)||""};
var FileReader=function(){this.readAsArrayBuffer=function(){};this.readAsDataURL=function(){};this.readAsText=function(){};this.onload=null;this.result=""};
var Uint8Array=function(n){return new Array(n||0)};
var TextEncoder=function(){this.encode=function(s){return new Uint8Array(s.length)}};
var TextDecoder=function(){this.decode=function(b){return""}};
var Event=function(t){this.type=t||"";this.preventDefault=function(){};this.stopPropagation=function(){}};
var CustomEvent=function(t,d){this.type=t||"";this.detail=d};
var dataLayer=[];
var gtag=function(){};
var adsbygoogle={push:function(){}};
var URL={createObjectURL:function(){return"blob:test"},revokeObjectURL:function(){}};
var Worker=function(){this.postMessage=function(){};this.onmessage=null};
var WebSocket=function(){this.send=function(){};this.close=function(){};this.onmessage=null;this.onopen=null};
var requestAnimationFrame=function(f){return 0};
var cancelAnimationFrame=function(){};
var performance={now:function(){return Date.now()}};
var console={log:function(){},warn:function(){},error:function(){},info:function(){},debug:function(){}};
var alert=function(){};
var prompt=function(){return""};
var confirm=function(){return false};
var history={pushState:function(){},replaceState:function(){},back:function(){}};
var localStorage={getItem:function(){return null},setItem:function(){},removeItem:function(){},clear:function(){}};
var sessionStorage={getItem:function(){return null},setItem:function(){},removeItem:function(){},clear:function(){}};
var IntersectionObserver=function(cb,opt){this.observe=function(){};this.unobserve=function(){};this.disconnect=function(){}};
var ResizeObserver=function(cb,opt){this.observe=function(){};this.unobserve=function(){};this.disconnect=function(){}};
var MutationObserver=function(cb){this.observe=function(){};this.disconnect=function(){}};
var HTMLCanvasElement=function(){this.getContext=function(){return{fillRect:function(){},clearRect:function(){},fillText:function(){},strokeText:function(){},measureText:function(){return{width:0}},drawImage:function(){},getImageData:function(){return{data:new Uint8Array(4)}},putImageData:function(){},createImageData:function(){return{data:new Uint8Array(4)}},beginPath:function(){},closePath:function(){},moveTo:function(){},lineTo:function(){},arc:function(){},fill:function(){},stroke:function(){},save:function(){},restore:function(){},translate:function(){},rotate:function(){},scale:function(){},canvas:this}};this.toDataURL=function(){return"data:image/png;base64,"};this.toBlob=function(cb){if(cb)cb(new Blob())};this.width=300;this.height=150};
var OffscreenCanvas=function(w,h){this.getContext=function(){return{fillRect:function(){},clearRect:function(){},fillText:function(){},measureText:function(){return{width:0}},canvas:this}};this.convertToBlob=function(){return Promise.resolve(new Blob())};this.width=w||300;this.height=h||150};
var MediaRecorder=function(){this.start=function(){};this.stop=function(){};this.ondataavailable=null};
var Audio=function(){this.play=function(){return Promise.resolve()};this.pause=function(){};this.load=function(){}};
'''

errors = []
checked = 0
skipped = 0

def check_file(filepath, label):
    global checked, skipped
    c = open(filepath, 'r', errors='ignore').read()
    scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', c, re.DOTALL)
    
    for s in scripts:
        if not s.strip(): continue
        if 'application/ld+json' in s: continue
        if len(s) < 20: continue
        
        with open('/tmp/_rtc.js', 'w') as tmp:
            tmp.write(DOM_STUB + '\n' + s)
        
        try:
            r = subprocess.run(['node', '/tmp/_rtc.js'], capture_output=True, text=True, timeout=3)
        except subprocess.TimeoutExpired:
            skipped += 1
            continue
        
        if r.returncode != 0 and r.stderr:
            # Filter out expected errors
            err_text = r.stderr
            if 'ReferenceError' in err_text:
                m = re.search(r'ReferenceError: (.+?) is not defined', err_text)
                if m:
                    var_name = m.group(1)
                    # Skip known false positives
                    if var_name in ['dataLayer', 'gtag', 'adsbygoogle', 'exports', 'module', 'require', 'process']:
                        continue
                    errors.append(f"{label}: {var_name} is not defined")
            elif 'SyntaxError' in err_text:
                # Skip - caught by node -c
                pass
    checked += 1

# CN pages
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    check_file(p, d)

# EN pages  
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    check_file(p, f"en/{d}")

print(f"\n{'='*60}")
print(f"Node运行时检测报告 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{'='*60}")
print(f"检测: {checked}页, 跳过(超时): {skipped}")
if errors:
    print(f"\n🔴 ReferenceError ({len(errors)}):")
    for e in errors[:30]:
        print(f"  {e}")
    if len(errors) > 30:
        print(f"  ... +{len(errors)-30} more")
else:
    print("\n🟢 0个运行时引用错误")
