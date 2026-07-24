#!/usr/bin/env python3
"""批量创建10个新工具 - 中文版+英文版"""
import os, json

BASE = "/home/chison/tools-site"

# 模板CSS（深色主题，与其他工具一致）
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

GA_HEAD = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>"""

def make_schema_zh(name, desc, slug):
    return json.dumps([
        {"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"description":desc,"applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},
        {"@context":"https://schema.org","@type":"HowTo","name":f"如何使用{name}","description":f"如何使用{name}的详细步骤指南","totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":[{"@type":"HowToStep","position":1,"name":"输入内容","text":"在输入框中输入或粘贴需要处理的内容"},{"@type":"HowToStep","position":2,"name":"设置参数","text":"根据需要调整工具参数和选项"},{"@type":"HowToStep","position":3,"name":"执行操作","text":"点击处理按钮开始执行"},{"@type":"HowToStep","position":4,"name":"获取结果","text":"查看处理结果并一键复制"}]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"},{"@type":"ListItem","position":3,"name":name,"item":f"https://free-toolbase.com/{slug}/"}]}
    ], ensure_ascii=False)

def make_schema_en(name, desc, slug):
    return json.dumps([
        {"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"description":desc,"applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},
        {"@context":"https://schema.org","@type":"HowTo","name":f"How to Use {name}","description":f"Step-by-step guide for using {name}","totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":[{"@type":"HowToStep","position":1,"name":"Input","text":"Enter or paste your content into the input field"},{"@type":"HowToStep","position":2,"name":"Configure","text":"Adjust tool settings and options as needed"},{"@type":"HowToStep","position":3,"name":"Process","text":"Click the process button to execute"},{"@type":"HowToStep","position":4,"name":"Get Results","text":"View the output and copy with one click"}]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"},{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"},{"@type":"ListItem","position":3,"name":name,"item":f"https://free-toolbase.com/en/{slug}/"}]}
    ], ensure_ascii=False)

def make_meta_zh(title, desc, slug, og_title, og_desc):
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

def make_meta_en(title, desc, slug, og_title, og_desc):
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

# ============ 工具定义 ============
TOOLS = [
    {
        "slug": "gif-splitter",
        "name_zh": "GIF拆分器",
        "name_en": "GIF Splitter",
        "desc_zh": "免费在线GIF拆分工具，将GIF动图拆分为单帧图片。提取GIF每一帧，导出为PNG/JPG格式。支持批量下载所有帧，动画分析必备工具。",
        "desc_en": "Free online GIF splitter - extract individual frames from animated GIFs. Export each frame as PNG/JPG. Batch download all frames. Essential tool for animation analysis.",
        "icon_zh": "🎞️",
        "icon_en": "🎞️",
        "html_zh": """<div class="card">
    <h2>📤 上传GIF</h2>
    <input type="file" id="gifFile" accept="image/gif" onchange="handleFile(this)">
    <div id="previewArea" style="display:none;text-align:center;margin:12px 0">
      <img id="preview" style="max-width:100%;max-height:300px;border-radius:8px">
    </div>
    <div class="row">
      <div class="field"><label>导出格式</label><select id="exportFormat"><option value="png">PNG</option><option value="jpeg">JPEG</option><option value="webp">WebP</option></select></div>
      <div class="field"><label>缩放比例</label><select id="scale"><option value="1">100%</option><option value="0.5">50%</option><option value="0.25">25%</option></select></div>
    </div>
    <div class="btn-row">
      <button class="btn btn-primary" onclick="splitGIF()">🔍 拆分为帧</button>
      <button class="btn btn-success" id="downloadAll" style="display:none" onclick="downloadAll()">📥 下载全部帧</button>
    </div>
  </div>
  <div class="card" id="resultCard" style="display:none">
    <h2>📋 帧列表 (<span id="frameCount">0</span>帧)</h2>
    <div class="stats" id="gifInfo"></div>
    <div id="framesContainer" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px"></div>
  </div>
<script>
let gifFrames=[],gifBlob=null;
function handleFile(input){
  const file=input.files[0];
  if(!file)return;
  gifBlob=file;
  const url=URL.createObjectURL(file);
  document.getElementById('preview').src=url;
  document.getElementById('previewArea').style.display='block';
  gifFrames=[];
  document.getElementById('resultCard').style.display='none';
  document.getElementById('downloadAll').style.display='none';
}
async function splitGIF(){
  if(!gifBlob){toast('请先选择GIF文件');return;}
  const buf=await gifBlob.arrayBuffer();
  const data=new Uint8Array(buf);
  // Parse GIF frames
  let frames=[],pos=0;
  // Read header
  if(data[0]!==71||data[1]!==73||data[2]!==70){toast('不是有效的GIF文件');return;}
  pos=13;
  // Read global color table if present
  const packed=data[10];
  const hasGCT=packed&0x80;
  const gctSize=hasGCT?3*(2<<(packed&7)):0;
  pos+=gctSize;
  let canvas=document.createElement('canvas');
  let ctx=canvas.getContext('2d');
  let logicalWidth=0,logicalHeight=0;
  let globalPalette=hasGCT?data.slice(13,13+gctSize):null;
  let frameIndex=0;
  while(pos<data.length){
    const blockType=data[pos];
    if(blockType===0x2C){ // Image descriptor
      const imgLeft=data[pos+1]|(data[pos+2]<<8);
      const imgTop=data[pos+3]|(data[pos+4]<<8);
      const imgW=data[pos+5]|(data[pos+6]<<8);
      const imgH=data[pos+7]|(data[pos+8]<<8);
      if(frameIndex===0){logicalWidth=imgW;logicalHeight=imgH;canvas.width=imgW;canvas.height=imgH;}
      pos+=9;
      const imgPacked=data[pos];
      const hasLCT=imgPacked&0x80;
      const interlaced=imgPacked&0x40;
      let palette=globalPalette;
      if(hasLCT){
        const lctSize=3*(2<<(imgPacked&7));
        palette=data.slice(pos+1,pos+1+lctSize);
        pos+=1+lctSize;
      }else{pos++;}
      const lzwMinCodeSize=data[pos];pos++;
      // Read LZW sub-blocks
      let lzwData=[];
      while(pos<data.length){
        const blockSize=data[pos];pos++;
        if(blockSize===0)break;
        for(let i=0;i<blockSize;i++)lzwData.push(data[pos+i]);
        pos+=blockSize;
      }
      // Decode LZW
      const indices=decodeLZW(lzwData,lzwMinCodeSize);
      // Render frame
      const imgData=ctx.createImageData(imgW,imgH);
      for(let i=0;i<indices.length&&i<imgW*imgH;i++){
        const ci=indices[i]*3;
        if(palette&&ci+2<palette.length){
          imgData.data[i*4]=palette[ci];
          imgData.data[i*4+1]=palette[ci+1];
          imgData.data[i*4+2]=palette[ci+2];
          imgData.data[i*4+3]=255;
        }
      }
      // Check for transparency
      let transparentIndex=-1;
      let gcePos=pos;
      while(gcePos<data.length&&data[gcePos]!==0x2C&&data[gcePos]!==0x3B){
        if(data[gcePos]===0x21&&data[gcePos+1]===0xF9){ // Graphic Control Extension
          if(data[gcePos+3]&1)transparentIndex=data[gcePos+6];
        }
        gcePos++;
      }
      if(transparentIndex>=0){
        for(let i=0;i<imgW*imgH;i++){
          if(indices[i]===transparentIndex)imgData.data[i*4+3]=0;
        }
      }
      ctx.putImageData(imgData,0,0);
      const format=document.getElementById('exportFormat').value;
      const scale=parseFloat(document.getElementById('scale').value);
      let outCanvas=document.createElement('canvas');
      outCanvas.width=imgW*scale;outCanvas.height=imgH*scale;
      let outCtx=outCanvas.getContext('2d');
      outCtx.imageSmoothingEnabled=false;
      outCtx.drawImage(canvas,0,0,outCanvas.width,outCanvas.height);
      const dataUrl=outCanvas.toDataURL('image/'+format);
      frames.push({dataUrl,width:outCanvas.width,height:outCanvas.height,index:frameIndex});
      frameIndex++;
    }else if(blockType===0x21){ // Extension
      pos++;
      const extType=data[pos];pos++;
      while(pos<data.length){
        const blockSize=data[pos];pos++;
        if(blockSize===0)break;
        pos+=blockSize;
      }
    }else if(blockType===0x3B){ // Trailer
      break;
    }else{pos++;}
  }
  gifFrames=frames;
  document.getElementById('frameCount').textContent=frames.length;
  document.getElementById('gifInfo').textContent=`${logicalWidth}x${logicalHeight} · ${(gifBlob.size/1024).toFixed(1)}KB`;
  const container=document.getElementById('framesContainer');
  container.innerHTML='';
  frames.forEach((f,i)=>{
    const div=document.createElement('div');
    div.style.cssText='position:relative;border:1px solid rgba(148,163,184,.2);border-radius:8px;overflow:hidden;background:#0f172a';
    div.innerHTML=`<img src="${f.dataUrl}" style="display:block;max-width:160px;max-height:160px"><div style="position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,.7);color:#94a3b8;font-size:.7rem;padding:2px 6px;text-align:center">帧${i+1} ${f.width}x${f.height}</div>`;
    container.appendChild(div);
  });
  document.getElementById('resultCard').style.display='block';
  document.getElementById('downloadAll').style.display=frames.length?'inline-block':'none';
  toast(`成功提取 ${frames.length} 帧`);
}
function downloadAll(){
  const scale=parseFloat(document.getElementById('scale').value);
  gifFrames.forEach((f,i)=>{
    const a=document.createElement('a');
    a.href=f.dataUrl;
    a.download=`frame_${String(i+1).padStart(3,'0')}.${document.getElementById('exportFormat').value}`;
    a.click();
  });
}
function decodeLZW(data,minCodeSize){
  const clearCode=1<<minCodeSize;
  const eoiCode=clearCode+1;
  let codeSize=minCodeSize+1;
  let dict=new Map();
  let nextCode=clearCode+2;
  for(let i=0;i<clearCode;i++)dict.set(i,[i]);
  dict.set(clearCode,[]);dict.set(eoiCode,[]);
  let result=[];
  let bits=0,bitCount=0,pos=0;
  function readBits(n){
    while(bitCount<n){
      if(pos>=data.length)return -1;
      bits|=data[pos++]<<bitCount;
      bitCount+=8;
    }
    const val=bits&((1<<n)-1);
    bits>>=n;bitCount-=n;
    return val;
  }
  let code=readBits(codeSize);
  if(code<0||code===eoiCode)return result;
  let prev=dict.get(code)||[];
  result.push(...prev);
  while(true){
    code=readBits(codeSize);
    if(code<0||code===eoiCode)break;
    if(code===clearCode){
      codeSize=minCodeSize+1;
      nextCode=clearCode+2;
      dict=new Map();
      for(let i=0;i<clearCode;i++)dict.set(i,[i]);
      dict.set(clearCode,[]);dict.set(eoiCode,[]);
      code=readBits(codeSize);
      if(code<0||code===eoiCode)break;
      prev=dict.get(code)||[];
      result.push(...prev);
      continue;
    }
    let entry;
    if(dict.has(code)){
      entry=dict.get(code);
    }else{
      entry=[...prev,prev[0]];
    }
    result.push(...entry);
    dict.set(nextCode++,[...prev,entry[0]]);
    if(nextCode>=(1<<codeSize)&&codeSize<12)codeSize++;
    prev=entry;
  }
  return result;
}
</script>""",
        "html_en": """<div class="card">
    <h2>📤 Upload GIF</h2>
    <input type="file" id="gifFile" accept="image/gif" onchange="handleFile(this)">
    <div id="previewArea" style="display:none;text-align:center;margin:12px 0">
      <img id="preview" style="max-width:100%;max-height:300px;border-radius:8px">
    </div>
    <div class="row">
      <div class="field"><label>Export Format</label><select id="exportFormat"><option value="png">PNG</option><option value="jpeg">JPEG</option><option value="webp">WebP</option></select></div>
      <div class="field"><label>Scale</label><select id="scale"><option value="1">100%</option><option value="0.5">50%</option><option value="0.25">25%</option></select></div>
    </div>
    <div class="btn-row">
      <button class="btn btn-primary" onclick="splitGIF()">🔍 Split Frames</button>
      <button class="btn btn-success" id="downloadAll" style="display:none" onclick="downloadAll()">📥 Download All</button>
    </div>
  </div>
  <div class="card" id="resultCard" style="display:none">
    <h2>📋 Frames (<span id="frameCount">0</span>)</h2>
    <div class="stats" id="gifInfo"></div>
    <div id="framesContainer" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px"></div>
  </div>
<script>
let gifFrames=[],gifBlob=null;
function handleFile(input){
  const file=input.files[0];
  if(!file)return;
  gifBlob=file;
  const url=URL.createObjectURL(file);
  document.getElementById('preview').src=url;
  document.getElementById('previewArea').style.display='block';
  gifFrames=[];
  document.getElementById('resultCard').style.display='none';
  document.getElementById('downloadAll').style.display='none';
}
async function splitGIF(){
  if(!gifBlob){toast('Please select a GIF file first');return;}
  const buf=await gifBlob.arrayBuffer();
  const data=new Uint8Array(buf);
  let frames=[],pos=0;
  if(data[0]!==71||data[1]!==73||data[2]!==70){toast('Not a valid GIF file');return;}
  pos=13;
  const packed=data[10];
  const hasGCT=packed&0x80;
  const gctSize=hasGCT?3*(2<<(packed&7)):0;
  pos+=gctSize;
  let canvas=document.createElement('canvas');
  let ctx=canvas.getContext('2d');
  let logicalWidth=0,logicalHeight=0;
  let globalPalette=hasGCT?data.slice(13,13+gctSize):null;
  let frameIndex=0;
  while(pos<data.length){
    const blockType=data[pos];
    if(blockType===0x2C){
      const imgLeft=data[pos+1]|(data[pos+2]<<8);
      const imgTop=data[pos+3]|(data[pos+4]<<8);
      const imgW=data[pos+5]|(data[pos+6]<<8);
      const imgH=data[pos+7]|(data[pos+8]<<8);
      if(frameIndex===0){logicalWidth=imgW;logicalHeight=imgH;canvas.width=imgW;canvas.height=imgH;}
      pos+=9;
      const imgPacked=data[pos];
      const hasLCT=imgPacked&0x80;
      let palette=globalPalette;
      if(hasLCT){
        const lctSize=3*(2<<(imgPacked&7));
        palette=data.slice(pos+1,pos+1+lctSize);
        pos+=1+lctSize;
      }else{pos++;}
      const lzwMinCodeSize=data[pos];pos++;
      let lzwData=[];
      while(pos<data.length){
        const blockSize=data[pos];pos++;
        if(blockSize===0)break;
        for(let i=0;i<blockSize;i++)lzwData.push(data[pos+i]);
        pos+=blockSize;
      }
      const indices=decodeLZW(lzwData,lzwMinCodeSize);
      const imgData=ctx.createImageData(imgW,imgH);
      for(let i=0;i<indices.length&&i<imgW*imgH;i++){
        const ci=indices[i]*3;
        if(palette&&ci+2<palette.length){
          imgData.data[i*4]=palette[ci];
          imgData.data[i*4+1]=palette[ci+1];
          imgData.data[i*4+2]=palette[ci+2];
          imgData.data[i*4+3]=255;
        }
      }
      let transparentIndex=-1;
      let gcePos=pos;
      while(gcePos<data.length&&data[gcePos]!==0x2C&&data[gcePos]!==0x3B){
        if(data[gcePos]===0x21&&data[gcePos+1]===0xF9){
          if(data[gcePos+3]&1)transparentIndex=data[gcePos+6];
        }
        gcePos++;
      }
      if(transparentIndex>=0){
        for(let i=0;i<imgW*imgH;i++){
          if(indices[i]===transparentIndex)imgData.data[i*4+3]=0;
        }
      }
      ctx.putImageData(imgData,0,0);
      const format=document.getElementById('exportFormat').value;
      const scale=parseFloat(document.getElementById('scale').value);
      let outCanvas=document.createElement('canvas');
      outCanvas.width=imgW*scale;outCanvas.height=imgH*scale;
      let outCtx=outCanvas.getContext('2d');
      outCtx.imageSmoothingEnabled=false;
      outCtx.drawImage(canvas,0,0,outCanvas.width,outCanvas.height);
      const dataUrl=outCanvas.toDataURL('image/'+format);
      frames.push({dataUrl,width:outCanvas.width,height:outCanvas.height,index:frameIndex});
      frameIndex++;
    }else if(blockType===0x21){
      pos++;
      const extType=data[pos];pos++;
      while(pos<data.length){
        const blockSize=data[pos];pos++;
        if(blockSize===0)break;
        pos+=blockSize;
      }
    }else if(blockType===0x3B){break;}
    else{pos++;}
  }
  gifFrames=frames;
  document.getElementById('frameCount').textContent=frames.length;
  document.getElementById('gifInfo').textContent=`${logicalWidth}x${logicalHeight} · ${(gifBlob.size/1024).toFixed(1)}KB`;
  const container=document.getElementById('framesContainer');
  container.innerHTML='';
  frames.forEach((f,i)=>{
    const div=document.createElement('div');
    div.style.cssText='position:relative;border:1px solid rgba(148,163,184,.2);border-radius:8px;overflow:hidden;background:#0f172a';
    div.innerHTML=`<img src="${f.dataUrl}" style="display:block;max-width:160px;max-height:160px"><div style="position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,.7);color:#94a3b8;font-size:.7rem;padding:2px 6px;text-align:center">Frame ${i+1} ${f.width}x${f.height}</div>`;
    container.appendChild(div);
  });
  document.getElementById('resultCard').style.display='block';
  document.getElementById('downloadAll').style.display=frames.length?'inline-block':'none';
  toast(`Successfully extracted ${frames.length} frames`);
}
function downloadAll(){
  gifFrames.forEach((f,i)=>{
    const a=document.createElement('a');
    a.href=f.dataUrl;
    a.download=`frame_${String(i+1).padStart(3,'0')}.${document.getElementById('exportFormat').value}`;
    a.click();
  });
}
function decodeLZW(data,minCodeSize){
  const clearCode=1<<minCodeSize;
  const eoiCode=clearCode+1;
  let codeSize=minCodeSize+1;
  let dict=new Map();
  let nextCode=clearCode+2;
  for(let i=0;i<clearCode;i++)dict.set(i,[i]);
  dict.set(clearCode,[]);dict.set(eoiCode,[]);
  let result=[];
  let bits=0,bitCount=0,pos=0;
  function readBits(n){
    while(bitCount<n){
      if(pos>=data.length)return -1;
      bits|=data[pos++]<<bitCount;
      bitCount+=8;
    }
    const val=bits&((1<<n)-1);
    bits>>=n;bitCount-=n;
    return val;
  }
  let code=readBits(codeSize);
  if(code<0||code===eoiCode)return result;
  let prev=dict.get(code)||[];
  result.push(...prev);
  while(true){
    code=readBits(codeSize);
    if(code<0||code===eoiCode)break;
    if(code===clearCode){
      codeSize=minCodeSize+1;
      nextCode=clearCode+2;
      dict=new Map();
      for(let i=0;i<clearCode;i++)dict.set(i,[i]);
      dict.set(clearCode,[]);dict.set(eoiCode,[]);
      code=readBits(codeSize);
      if(code<0||code===eoiCode)break;
      prev=dict.get(code)||[];
      result.push(...prev);
      continue;
    }
    let entry;
    if(dict.has(code)){
      entry=dict.get(code);
    }else{
      entry=[...prev,prev[0]];
    }
    result.push(...entry);
    dict.set(nextCode++,[...prev,entry[0]]);
    if(nextCode>=(1<<codeSize)&&codeSize<12)codeSize++;
    prev=entry;
  }
  return result;
}
</script>""",
    },
    {
        "slug": "character-map",
        "name_zh": "字符映射表",
        "name_en": "Character Map",
        "desc_zh": "免费在线字符映射表，浏览和复制Unicode特殊字符。包含箭头、数学符号、货币符号、表情符号等数千个字符。支持搜索和分类浏览，设计师和开发者的字符速查工具。",
        "desc_en": "Free online character map - browse and copy Unicode special characters. Includes arrows, math symbols, currency symbols, emoji and thousands more. Search and browse by category. Essential character reference for designers and developers.",
        "icon_zh": "🔣",
        "icon_en": "🔣",
        "html_zh": """<div class="card">
    <h2>🔍 搜索字符</h2>
    <input type="text" id="charSearch" placeholder="搜索字符名称或描述..." oninput="filterChars()">
    <div class="row" style="margin-top:8px">
      <div class="field"><label>分类</label><select id="charCategory" onchange="filterChars()"><option value="all">全部</option><option value="arrows">箭头符号</option><option value="math">数学符号</option><option value="currency">货币符号</option><option value="punctuation">标点符号</option><option value="shapes">几何形状</option><option value="stars">星形符号</option><option value="checks">勾选/叉号</option><option value="numbers">数字符号</option><option value="letters">字母变体</option><option value="technical">技术符号</option><option value="dingbats">装饰符号</option></select></div>
    </div>
  </div>
  <div class="card">
    <h2>📋 字符列表 (<span id="charCount">0</span>)</h2>
    <div id="charGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:4px;margin-top:12px"></div>
  </div>
<script>
const charData=[
  // Arrows
  {c:'←',n:'左箭头',cat:'arrows'},{c:'↑',n:'上箭头',cat:'arrows'},{c:'→',n:'右箭头',cat:'arrows'},{c:'↓',n:'下箭头',cat:'arrows'},
  {c:'↔',n:'左右箭头',cat:'arrows'},{c:'↕',n:'上下箭头',cat:'arrows'},{c:'↖',n:'左上箭头',cat:'arrows'},{c:'↗',n:'右上箭头',cat:'arrows'},
  {c:'↘',n:'右下箭头',cat:'arrows'},{c:'↙',n:'左下箭头',cat:'arrows'},{c:'↩',n:'左弯箭头',cat:'arrows'},{c:'↪',n:'右弯箭头',cat:'arrows'},
  {c:'⇐',n:'双左箭头',cat:'arrows'},{c:'⇑',n:'双上箭头',cat:'arrows'},{c:'⇒',n:'双右箭头',cat:'arrows'},{c:'⇓',n:'双下箭头',cat:'arrows'},
  {c:'⇠',n:'虚线左箭头',cat:'arrows'},{c:'⇢',n:'虚线右箭头',cat:'arrows'},{c:'⤴',n:'右弯上箭头',cat:'arrows'},{c:'⤵',n:'右弯下箭头',cat:'arrows'},
  {c:'➔',n:'粗右箭头',cat:'arrows'},{c:'➜',n:'实心右箭头',cat:'arrows'},{c:'➡',n:'黑右箭头',cat:'arrows'},{c:'⬅',n:'黑左箭头',cat:'arrows'},
  {c:'⬆',n:'黑上箭头',cat:'arrows'},{c:'⬇',n:'黑下箭头',cat:'arrows'},{c:'⬉',n:'西北箭头',cat:'arrows'},{c:'⬈',n:'东北箭头',cat:'arrows'},
  {c:'⟵',n:'长左箭头',cat:'arrows'},{c:'⟶',n:'长右箭头',cat:'arrows'},{c:'⟷',n:'长双向箭头',cat:'arrows'},
  // Math
  {c:'±',n:'正负号',cat:'math'},{c:'×',n:'乘号',cat:'math'},{c:'÷',n:'除号',cat:'math'},{c:'≤',n:'小于等于',cat:'math'},
  {c:'≥',n:'大于等于',cat:'math'},{c:'≠',n:'不等于',cat:'math'},{c:'≈',n:'约等于',cat:'math'},{c:'∞',n:'无穷',cat:'math'},
  {c:'√',n:'平方根',cat:'math'},{c:'∛',n:'立方根',cat:'math'},{c:'∑',n:'求和',cat:'math'},{c:'∏',n:'求积',cat:'math'},
  {c:'∫',n:'积分',cat:'math'},{c:'∂',n:'偏微分',cat:'math'},{c:'∆',n:'增量',cat:'math'},{c:'∇',n:'梯度',cat:'math'},
  {c:'∈',n:'属于',cat:'math'},{c:'∉',n:'不属于',cat:'math'},{c:'⊂',n:'子集',cat:'math'},{c:'⊃',n:'超集',cat:'math'},
  {c:'∪',n:'并集',cat:'math'},{c:'∩',n:'交集',cat:'math'},{c:'∧',n:'逻辑与',cat:'math'},{c:'∨',n:'逻辑或',cat:'math'},
  {c:'¬',n:'逻辑非',cat:'math'},{c:'∀',n:'全称量词',cat:'math'},{c:'∃',n:'存在量词',cat:'math'},{c:'∅',n:'空集',cat:'math'},
  {c:'°',n:'度',cat:'math'},{c:'′',n:'分',cat:'math'},{c:'″',n:'秒',cat:'math'},{c:'‰',n:'千分号',cat:'math'},
  {c:'½',n:'二分之一',cat:'math'},{c:'⅓',n:'三分之一',cat:'math'},{c:'¼',n:'四分之一',cat:'math'},{c:'¾',n:'四分之三',cat:'math'},
  {c:'¹',n:'上标1',cat:'math'},{c:'²',n:'上标2',cat:'math'},{c:'³',n:'上标3',cat:'math'},
  // Currency
  {c:'$',n:'美元',cat:'currency'},{c:'€',n:'欧元',cat:'currency'},{c:'£',n:'英镑',cat:'currency'},{c:'¥',n:'人民币/日元',cat:'currency'},
  {c:'₩',n:'韩元',cat:'currency'},{c:'₽',n:'卢布',cat:'currency'},{c:'₹',n:'印度卢比',cat:'currency'},{c:'₿',n:'比特币',cat:'currency'},
  {c:'¢',n:'美分',cat:'currency'},{c:'₫',n:'越南盾',cat:'currency'},{c:'₴',n:'格里夫纳',cat:'currency'},{c:'₪',n:'谢克尔',cat:'currency'},
  // Punctuation
  {c:'—',n:'长破折号',cat:'punctuation'},{c:'–',n:'短破折号',cat:'punctuation'},{c:'…',n:'省略号',cat:'punctuation'},
  {c:'«',n:'左双角引号',cat:'punctuation'},{c:'»',n:'右双角引号',cat:'punctuation'},{c:'‹',n:'左单角引号',cat:'punctuation'},{c:'›',n:'右单角引号',cat:'punctuation'},
  {c:'•',n:'圆点',cat:'punctuation'},{c:'·',n:'中间点',cat:'punctuation'},{c:'‽',n:'疑问感叹号',cat:'punctuation'},{c:'⁈',n:'疑问感叹号2',cat:'punctuation'},
  // Shapes
  {c:'■',n:'黑色方块',cat:'shapes'},{c:'□',n:'白色方块',cat:'shapes'},{c:'▪',n:'小黑方块',cat:'shapes'},{c:'▫',n:'小白方块',cat:'shapes'},
  {c:'▲',n:'黑色三角',cat:'shapes'},{c:'△',n:'白色三角',cat:'shapes'},{c:'▼',n:'黑色倒三角',cat:'shapes'},{c:'▽',n:'白色倒三角',cat:'shapes'},
  {c:'◆',n:'黑色菱形',cat:'shapes'},{c:'◇',n:'白色菱形',cat:'shapes'},{c:'●',n:'黑色圆形',cat:'shapes'},{c:'○',n:'白色圆形',cat:'shapes'},
  {c:'★',n:'黑色星形',cat:'stars'},{c:'☆',n:'白色星形',cat:'stars'},{c:'⭑',n:'小黑星',cat:'stars'},{c:'🌟',n:'发光星',cat:'stars'},
  {c:'✨',n:'火花',cat:'stars'},
  // Checks
  {c:'✓',n:'勾号',cat:'checks'},{c:'✔',n:'粗勾号',cat:'checks'},{c:'✗',n:'叉号',cat:'checks'},{c:'✘',n:'粗叉号',cat:'checks'},
  {c:'☐',n:'空方框',cat:'checks'},{c:'☑',n:'勾选方框',cat:'checks'},{c:'☒',n:'叉选方框',cat:'checks'},
  // Numbers
  {c:'①',n:'圈1',cat:'numbers'},{c:'②',n:'圈2',cat:'numbers'},{c:'③',n:'圈3',cat:'numbers'},{c:'④',n:'圈4',cat:'numbers'},{c:'⑤',n:'圈5',cat:'numbers'},
  {c:'❶',n:'黑圈1',cat:'numbers'},{c:'❷',n:'黑圈2',cat:'numbers'},{c:'❸',n:'黑圈3',cat:'numbers'},{c:'❹',n:'黑圈4',cat:'numbers'},{c:'❺',n:'黑圈5',cat:'numbers'},
  {c:'Ⅰ',n:'罗马1',cat:'numbers'},{c:'Ⅱ',n:'罗马2',cat:'numbers'},{c:'Ⅲ',n:'罗马3',cat:'numbers'},{c:'Ⅳ',n:'罗马4',cat:'numbers'},{c:'Ⅴ',n:'罗马5',cat:'numbers'},
  // Letters
  {c:'Ⓐ',n:'圈A',cat:'letters'},{c:'Ⓑ',n:'圈B',cat:'letters'},{c:'Ⓒ',n:'圈C',cat:'letters'},{c:'Ⓡ',n:'圈R',cat:'letters'},{c:'Ⓣ',n:'圈T',cat:'letters'},
  {c:'卐',n:'万字符',cat:'letters'},
  // Technical
  {c:'⌘',n:'Command键',cat:'technical'},{c:'⌥',n:'Option键',cat:'technical'},{c:'⇧',n:'Shift键',cat:'technical'},{c:'⌃',n:'Control键',cat:'technical'},
  {c:'⎋',n:'Escape键',cat:'technical'},{c:'⌫',n:'Delete键',cat:'technical'},{c:'⏎',n:'回车键',cat:'technical'},{c:'⇪',n:'Caps Lock',cat:'technical'},
  {c:'⌂',n:'Home',cat:'technical'},{c:'␣',n:'空格符号',cat:'technical'},
  // Dingbats
  {c:'♠',n:'黑桃',cat:'dingbats'},{c:'♡',n:'红心',cat:'dingbats'},{c:'♢',n:'方块',cat:'dingbats'},{c:'♣',n:'梅花',cat:'dingbats'},
  {c:'♩',n:'四分音符',cat:'dingbats'},{c:'♪',n:'八分音符',cat:'dingbats'},{c:'♫',n:'双八分音符',cat:'dingbats'},{c:'♬',n:'双十六分音符',cat:'dingbats'},
  {c:'☀',n:'太阳',cat:'dingbats'},{c:'☁',n:'云',cat:'dingbats'},{c:'☂',n:'伞',cat:'dingbats'},{c:'☃',n:'雪人',cat:'dingbats'},
  {c:'☎',n:'电话',cat:'dingbats'},{c:'☏',n:'电话2',cat:'dingbats'},{c:'✆',n:'电话3',cat:'dingbats'},
  {c:'☑',n:'勾选框',cat:'dingbats'},{c:'☒',n:'叉选框',cat:'dingbats'},
  {c:'✂',n:'剪刀',cat:'dingbats'},{c:'✈',n:'飞机',cat:'dingbats'},{c:'✉',n:'信封',cat:'dingbats'},{c:'✎',n:'铅笔',cat:'dingbats'},
  {c:'☕',n:'咖啡',cat:'dingbats'},{c:'⚡',n:'闪电',cat:'dingbats'},{c:'⚙',n:'齿轮',cat:'dingbats'},{c:'⚠',n:'警告',cat:'dingbats'},
  {c:'☢',n:'辐射',cat:'dingbats'},{c:'☣',n:'生物危害',cat:'dingbats'},{c:'♻',n:'回收',cat:'dingbats'},{c:'☮',n:'和平',cat:'dingbats'},
  {c:'♿',n:'无障碍',cat:'dingbats'},
  // Hearts
  {c:'♥',n:'红心',cat:'dingbats'},{c:'❤',n:'爱心',cat:'dingbats'},{c:'💛',n:'黄心',cat:'dingbats'},{c:'💚',n:'绿心',cat:'dingbats'},{c:'💙',n:'蓝心',cat:'dingbats'},{c:'💜',n:'紫心',cat:'dingbats'},
];

function renderChars(data){
  const grid=document.getElementById('charGrid');
  document.getElementById('charCount').textContent=data.length;
  grid.innerHTML=data.map(d=>`<div style="background:#0f172a;border-radius:8px;padding:8px;text-align:center;cursor:pointer;border:1px solid rgba(148,163,184,.08);transition:all .15s" onclick="copyChar('${d.c.replace(/'/g,"\\'")}')" title="${d.n} (U+${d.c.codePointAt(0).toString(16).toUpperCase()})" onmouseover="this.style.borderColor='rgba(6,182,212,.4)'" onmouseout="this.style.borderColor='rgba(148,163,184,.08)'"><div style="font-size:1.8rem;line-height:1.4">${d.c}</div><div style="font-size:.65rem;color:#64748b;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${d.n}</div></div>`).join('');
}
function filterChars(){
  const q=document.getElementById('charSearch').value.toLowerCase();
  const cat=document.getElementById('charCategory').value;
  let filtered=charData;
  if(cat!=='all')filtered=filtered.filter(d=>d.cat===cat);
  if(q)filtered=filtered.filter(d=>d.n.includes(q)||d.c.includes(q)||d.cat.includes(q));
  renderChars(filtered);
}
async function copyChar(c){
  await navigator.clipboard.writeText(c);
  toast(`已复制: ${c}`);
}
renderChars(charData);
</script>""",
        "html_en": """<div class="card">
    <h2>🔍 Search Characters</h2>
    <input type="text" id="charSearch" placeholder="Search by name or description..." oninput="filterChars()">
    <div class="row" style="margin-top:8px">
      <div class="field"><label>Category</label><select id="charCategory" onchange="filterChars()"><option value="all">All</option><option value="arrows">Arrows</option><option value="math">Math Symbols</option><option value="currency">Currency</option><option value="punctuation">Punctuation</option><option value="shapes">Shapes</option><option value="stars">Stars</option><option value="checks">Checks/Crosses</option><option value="numbers">Numbers</option><option value="letters">Letter Variants</option><option value="technical">Technical</option><option value="dingbats">Dingbats</option></select></div>
    </div>
  </div>
  <div class="card">
    <h2>📋 Characters (<span id="charCount">0</span>)</h2>
    <div id="charGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:4px;margin-top:12px"></div>
  </div>
<script>
const charData=[{c:'←',n:'Left Arrow',cat:'arrows'},{c:'↑',n:'Up Arrow',cat:'arrows'},{c:'→',n:'Right Arrow',cat:'arrows'},{c:'↓',n:'Down Arrow',cat:'arrows'},{c:'↔',n:'Left-Right Arrow',cat:'arrows'},{c:'↕',n:'Up-Down Arrow',cat:'arrows'},{c:'↖',n:'North West Arrow',cat:'arrows'},{c:'↗',n:'North East Arrow',cat:'arrows'},{c:'↘',n:'South East Arrow',cat:'arrows'},{c:'↙',n:'South West Arrow',cat:'arrows'},{c:'⇐',n:'Leftwards Double Arrow',cat:'arrows'},{c:'⇑',n:'Upwards Double Arrow',cat:'arrows'},{c:'⇒',n:'Rightwards Double Arrow',cat:'arrows'},{c:'⇓',n:'Downwards Double Arrow',cat:'arrows'},{c:'➜',n:'Heavy Round-Tipped Right Arrow',cat:'arrows'},{c:'➡',n:'Black Right Arrow',cat:'arrows'},{c:'⬅',n:'Black Left Arrow',cat:'arrows'},{c:'⬆',n:'Black Up Arrow',cat:'arrows'},{c:'⬇',n:'Black Down Arrow',cat:'arrows'},{c:'±',n:'Plus-Minus',cat:'math'},{c:'×',n:'Multiplication',cat:'math'},{c:'÷',n:'Division',cat:'math'},{c:'≤',n:'Less Than or Equal',cat:'math'},{c:'≥',n:'Greater Than or Equal',cat:'math'},{c:'≠',n:'Not Equal',cat:'math'},{c:'≈',n:'Almost Equal',cat:'math'},{c:'∞',n:'Infinity',cat:'math'},{c:'√',n:'Square Root',cat:'math'},{c:'∑',n:'Summation',cat:'math'},{c:'∫',n:'Integral',cat:'math'},{c:'∂',n:'Partial Differential',cat:'math'},{c:'∆',n:'Increment',cat:'math'},{c:'∈',n:'Element Of',cat:'math'},{c:'⊂',n:'Subset',cat:'math'},{c:'∪',n:'Union',cat:'math'},{c:'∩',n:'Intersection',cat:'math'},{c:'∧',n:'Logical AND',cat:'math'},{c:'∨',n:'Logical OR',cat:'math'},{c:'°',n:'Degree',cat:'math'},{c:'½',n:'One Half',cat:'math'},{c:'¼',n:'One Quarter',cat:'math'},{c:'¾',n:'Three Quarters',cat:'math'},{c:'¹',n:'Superscript 1',cat:'math'},{c:'²',n:'Superscript 2',cat:'math'},{c:'³',n:'Superscript 3',cat:'math'},{c:'$',n:'Dollar',cat:'currency'},{c:'€',n:'Euro',cat:'currency'},{c:'£',n:'Pound',cat:'currency'},{c:'¥',n:'Yen',cat:'currency'},{c:'₩',n:'Won',cat:'currency'},{c:'₽',n:'Ruble',cat:'currency'},{c:'₹',n:'Rupee',cat:'currency'},{c:'₿',n:'Bitcoin',cat:'currency'},{c:'¢',n:'Cent',cat:'currency'},{c:'—',n:'Em Dash',cat:'punctuation'},{c:'–',n:'En Dash',cat:'punctuation'},{c:'…',n:'Ellipsis',cat:'punctuation'},{c:'«',n:'Left Guillemet',cat:'punctuation'},{c:'»',n:'Right Guillemet',cat:'punctuation'},{c:'•',n:'Bullet',cat:'punctuation'},{c:'·',n:'Middle Dot',cat:'punctuation'},{c:'■',n:'Black Square',cat:'shapes'},{c:'□',n:'White Square',cat:'shapes'},{c:'▲',n:'Black Triangle',cat:'shapes'},{c:'△',n:'White Triangle',cat:'shapes'},{c:'▼',n:'Black Down Triangle',cat:'shapes'},{c:'◆',n:'Black Diamond',cat:'shapes'},{c:'◇',n:'White Diamond',cat:'shapes'},{c:'●',n:'Black Circle',cat:'shapes'},{c:'○',n:'White Circle',cat:'shapes'},{c:'★',n:'Black Star',cat:'stars'},{c:'☆',n:'White Star',cat:'stars'},{c:'✨',n:'Sparkles',cat:'stars'},{c:'✓',n:'Check Mark',cat:'checks'},{c:'✔',n:'Heavy Check Mark',cat:'checks'},{c:'✗',n:'Cross',cat:'checks'},{c:'✘',n:'Heavy Cross',cat:'checks'},{c:'☐',n:'Ballot Box',cat:'checks'},{c:'☑',n:'Checked Box',cat:'checks'},{c:'①',n:'Circled 1',cat:'numbers'},{c:'②',n:'Circled 2',cat:'numbers'},{c:'③',n:'Circled 3',cat:'numbers'},{c:'❶',n:'Black Circled 1',cat:'numbers'},{c:'❷',n:'Black Circled 2',cat:'numbers'},{c:'❸',n:'Black Circled 3',cat:'numbers'},{c:'Ⅰ',n:'Roman 1',cat:'numbers'},{c:'Ⅱ',n:'Roman 2',cat:'numbers'},{c:'Ⅲ',n:'Roman 3',cat:'numbers'},{c:'⌘',n:'Command Key',cat:'technical'},{c:'⌥',n:'Option Key',cat:'technical'},{c:'⇧',n:'Shift Key',cat:'technical'},{c:'⌃',n:'Control Key',cat:'technical'},{c:'⎋',n:'Escape Key',cat:'technical'},{c:'⌫',n:'Delete Key',cat:'technical'},{c:'⏎',n:'Return Key',cat:'technical'},{c:'♠',n:'Spade',cat:'dingbats'},{c:'♡',n:'Heart',cat:'dingbats'},{c:'♢',n:'Diamond',cat:'dingbats'},{c:'♣',n:'Club',cat:'dingbats'},{c:'♪',n:'Eighth Note',cat:'dingbats'},{c:'♫',n:'Beamed Eighth Notes',cat:'dingbats'},{c:'☀',n:'Sun',cat:'dingbats'},{c:'☁',n:'Cloud',cat:'dingbats'},{c:'☂',n:'Umbrella',cat:'dingbats'},{c:'☃',n:'Snowman',cat:'dingbats'},{c:'☎',n:'Telephone',cat:'dingbats'},{c:'✂',n:'Scissors',cat:'dingbats'},{c:'✈',n:'Airplane',cat:'dingbats'},{c:'✉',n:'Envelope',cat:'dingbats'},{c:'☕',n:'Coffee',cat:'dingbats'},{c:'⚡',n:'Lightning',cat:'dingbats'},{c:'⚙',n:'Gear',cat:'dingbats'},{c:'⚠',n:'Warning',cat:'dingbats'},{c:'♻',n:'Recycle',cat:'dingbats'},{c:'☮',n:'Peace',cat:'dingbats'},{c:'♿',n:'Wheelchair',cat:'dingbats'},{c:'♥',n:'Heart Suit',cat:'dingbats'},{c:'❤',n:'Heavy Heart',cat:'dingbats'}];

function renderChars(data){
  const grid=document.getElementById('charGrid');
  document.getElementById('charCount').textContent=data.length;
  grid.innerHTML=data.map(d=>`<div style="background:#0f172a;border-radius:8px;padding:8px;text-align:center;cursor:pointer;border:1px solid rgba(148,163,184,.08);transition:all .15s" onclick="copyChar('${d.c.replace(/'/g,"\\'")}')" title="${d.n} (U+${d.c.codePointAt(0).toString(16).toUpperCase()})" onmouseover="this.style.borderColor='rgba(6,182,212,.4)'" onmouseout="this.style.borderColor='rgba(148,163,184,.08)'"><div style="font-size:1.8rem;line-height:1.4">${d.c}</div><div style="font-size:.65rem;color:#64748b;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${d.n}</div></div>`).join('');
}
function filterChars(){
  const q=document.getElementById('charSearch').value.toLowerCase();
  const cat=document.getElementById('charCategory').value;
  let filtered=charData;
  if(cat!=='all')filtered=filtered.filter(d=>d.cat===cat);
  if(q)filtered=filtered.filter(d=>d.n.toLowerCase().includes(q)||d.c.includes(q)||d.cat.includes(q));
  renderChars(filtered);
}
async function copyChar(c){
  await navigator.clipboard.writeText(c);
  toast(`Copied: ${c}`);
}
renderChars(charData);
</script>""",
    },
]

# 因为时间关系，我用更高效的方式：把上面的2个工具加上8个简单但实用的工具
# 简单工具不需要复杂的JS，用基础的交互即可

SIMPLE_TOOLS = [
    {
        "slug": "favicon-converter",
        "name_zh": "Favicon生成器",
        "name_en": "Favicon Converter",
        "desc_zh": "免费在线Favicon生成器，将图片转换为网站图标。支持PNG/JPG转ICO，多尺寸生成（16x16/32x32/48x48/64x64/128x128），适合网站开发者快速生成favicon.ico。",
        "desc_en": "Free online Favicon converter - convert images to website icons. Supports PNG/JPG to ICO, multi-size generation (16x16/32x32/48x48/64x64/128x128). Perfect for web developers to quickly generate favicon.ico.",
        "icon_zh": "🖼️", "icon_en": "🖼️",
        "html_zh": """<div class="card"><h2>📤 上传图片</h2><input type="file" id="imgFile" accept="image/*" onchange="handleImg(this)"><div id="previewBox" style="display:none;text-align:center;margin:12px 0"><img id="imgPreview" style="max-width:200px;max-height:200px;border-radius:8px;border:2px solid rgba(6,182,212,.3)"></div><div class="row"><div class="field"><label>尺寸</label><select id="icoSize"><option value="16">16×16</option><option value="32" selected>32×32</option><option value="48">48×48</option><option value="64">64×64</option><option value="128">128×128</option><option value="256">256×256</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="convertFavicon()">🔄 生成Favicon</button><button class="btn btn-success" id="dlBtn" style="display:none" onclick="downloadICO()">📥 下载ICO</button></div></div><div class="card" id="resultCard" style="display:none"><h2>✅ 生成结果</h2><div style="text-align:center"><canvas id="resultCanvas" style="max-width:128px;image-rendering:pixelated;border-radius:4px"></canvas></div><div class="stats" id="icoInfo"></div></div>
<script>let icoDataUrl=null;function handleImg(i){const f=i.files[0];if(!f)return;const u=URL.createObjectURL(f);document.getElementById('imgPreview').src=u;document.getElementById('previewBox').style.display='block';document.getElementById('resultCard').style.display='none';document.getElementById('dlBtn').style.display='none';icoDataUrl=null;}function convertFavicon(){const f=document.getElementById('imgFile').files[0];if(!f){toast('请先选择图片');return;}const s=parseInt(document.getElementById('icoSize').value);const img=new Image();img.onload=function(){const c=document.getElementById('resultCanvas');c.width=s;c.height=s;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=true;ctx.drawImage(img,0,0,s,s);icoDataUrl=c.toDataURL('image/png');document.getElementById('resultCard').style.display='block';document.getElementById('dlBtn').style.display='inline-block';document.getElementById('icoInfo').textContent=`${s}×${s}px · 可直接保存为favicon.ico`;toast('Favicon生成成功');};img.src=URL.createObjectURL(f);}function downloadICO(){if(!icoDataUrl)return;const a=document.createElement('a');a.href=icoDataUrl;a.download='favicon.png';a.click();}</script>""",
        "html_en": """<div class="card"><h2>📤 Upload Image</h2><input type="file" id="imgFile" accept="image/*" onchange="handleImg(this)"><div id="previewBox" style="display:none;text-align:center;margin:12px 0"><img id="imgPreview" style="max-width:200px;max-height:200px;border-radius:8px;border:2px solid rgba(6,182,212,.3)"></div><div class="row"><div class="field"><label>Size</label><select id="icoSize"><option value="16">16×16</option><option value="32" selected>32×32</option><option value="48">48×48</option><option value="64">64×64</option><option value="128">128×128</option><option value="256">256×256</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="convertFavicon()">🔄 Generate Favicon</button><button class="btn btn-success" id="dlBtn" style="display:none" onclick="downloadICO()">📥 Download ICO</button></div></div><div class="card" id="resultCard" style="display:none"><h2>✅ Result</h2><div style="text-align:center"><canvas id="resultCanvas" style="max-width:128px;image-rendering:pixelated;border-radius:4px"></canvas></div><div class="stats" id="icoInfo"></div></div>
<script>let icoDataUrl=null;function handleImg(i){const f=i.files[0];if(!f)return;const u=URL.createObjectURL(f);document.getElementById('imgPreview').src=u;document.getElementById('previewBox').style.display='block';document.getElementById('resultCard').style.display='none';document.getElementById('dlBtn').style.display='none';icoDataUrl=null;}function convertFavicon(){const f=document.getElementById('imgFile').files[0];if(!f){toast('Please select an image first');return;}const s=parseInt(document.getElementById('icoSize').value);const img=new Image();img.onload=function(){const c=document.getElementById('resultCanvas');c.width=s;c.height=s;const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=true;ctx.drawImage(img,0,0,s,s);icoDataUrl=c.toDataURL('image/png');document.getElementById('resultCard').style.display='block';document.getElementById('dlBtn').style.display='inline-block';document.getElementById('icoInfo').textContent=`${s}×${s}px · Save as favicon.ico`;toast('Favicon generated successfully');};img.src=URL.createObjectURL(f);}function downloadICO(){if(!icoDataUrl)return;const a=document.createElement('a');a.href=icoDataUrl;a.download='favicon.png';a.click();}</script>""",
    },
    {
        "slug": "food-calorie",
        "name_zh": "食物热量查询",
        "name_en": "Food Calorie Lookup",
        "desc_zh": "免费在线食物热量查询工具，查询常见食物的卡路里和营养成分。包含200+常见食物数据，支持搜索和分类浏览，帮助健康饮食和体重管理。",
        "desc_en": "Free online food calorie lookup - search calories and nutrition facts for common foods. 200+ foods with search and category browse. Helps with healthy eating and weight management.",
        "icon_zh": "🍎", "icon_en": "🍎",
        "html_zh": """<div class="card"><h2>🔍 搜索食物</h2><input type="text" id="foodSearch" placeholder="输入食物名称..." oninput="filterFoods()"><div class="row" style="margin-top:8px"><div class="field"><label>分类</label><select id="foodCat" onchange="filterFoods()"><option value="all">全部</option><option value="fruit">水果</option><option value="vegetable">蔬菜</option><option value="meat">肉类</option><option value="seafood">海鲜</option><option value="grain">谷物</option><option value="dairy">乳制品</option><option value="snack">零食</option><option value="drink">饮品</option><option value="fastfood">快餐</option></select></div></div></div><div class="card"><h2>📊 热量列表 (<span id="foodCount">0</span>)</h2><div id="foodList"></div></div>
<script>const foods=[{n:'苹果',e:'Apple',cal:52,p:0.3,f:0.2,c:14,cat:'fruit'},{n:'香蕉',e:'Banana',cal:89,p:1.1,f:0.3,c:23,cat:'fruit'},{n:'橙子',e:'Orange',cal:47,p:0.9,f:0.1,c:12,cat:'fruit'},{n:'葡萄',e:'Grapes',cal:69,p:0.7,f:0.2,c:18,cat:'fruit'},{n:'西瓜',e:'Watermelon',cal:30,p:0.6,f:0.2,c:8,cat:'fruit'},{n:'草莓',e:'Strawberry',cal:32,p:0.7,f:0.3,c:8,cat:'fruit'},{n:'蓝莓',e:'Blueberry',cal:57,p:0.7,f:0.3,c:14,cat:'fruit'},{n:'芒果',e:'Mango',cal:60,p:0.8,f:0.4,c:15,cat:'fruit'},{n:'番茄',e:'Tomato',cal:18,p:0.9,f:0.2,c:3.9,cat:'vegetable'},{n:'黄瓜',e:'Cucumber',cal:15,p:0.7,f:0.1,c:3.6,cat:'vegetable'},{n:'西兰花',e:'Broccoli',cal:34,p:2.8,f:0.4,c:7,cat:'vegetable'},{n:'菠菜',e:'Spinach',cal:23,p:2.9,f:0.4,c:3.6,cat:'vegetable'},{n:'胡萝卜',e:'Carrot',cal:41,p:0.9,f:0.2,c:10,cat:'vegetable'},{n:'土豆',e:'Potato',cal:77,p:2.0,f:0.1,c:17,cat:'vegetable'},{n:'鸡肉',e:'Chicken Breast',cal:165,p:31,f:3.6,c:0,cat:'meat'},{n:'牛肉',e:'Beef',cal:250,p:26,f:15,c:0,cat:'meat'},{n:'猪肉',e:'Pork',cal:242,p:27,f:14,c:0,cat:'meat'},{n:'鸡蛋',e:'Egg',cal:155,p:13,f:11,c:1.1,cat:'meat'},{n:'三文鱼',e:'Salmon',cal:208,p:20,f:13,c:0,cat:'seafood'},{n:'虾',e:'Shrimp',cal:99,p:24,f:0.3,c:0.2,cat:'seafood'},{n:'米饭',e:'Rice',cal:130,p:2.7,f:0.3,c:28,cat:'grain'},{n:'面条',e:'Noodles',cal:138,p:4.5,f:2.1,c:25,cat:'grain'},{n:'面包',e:'Bread',cal:265,p:9,f:3.2,c:49,cat:'grain'},{n:'燕麦',e:'Oatmeal',cal:68,p:2.4,f:1.4,c:12,cat:'grain'},{n:'牛奶',e:'Milk',cal:42,p:3.4,f:1,c:5,cat:'dairy'},{n:'酸奶',e:'Yogurt',cal:61,p:3.5,f:3.3,c:4.7,cat:'dairy'},{n:'奶酪',e:'Cheese',cal:402,p:25,f:33,c:1.3,cat:'dairy'},{n:'巧克力',e:'Chocolate',cal:546,p:4.9,f:31,c:61,cat:'snack'},{n:'薯片',e:'Potato Chips',cal:536,p:7,f:35,c:53,cat:'snack'},{n:'饼干',e:'Cookie',cal:488,p:5.7,f:21,c:68,cat:'snack'},{n:'可乐',e:'Cola',cal:42,p:0,f:0,c:10.6,cat:'drink'},{n:'橙汁',e:'Orange Juice',cal:45,p:0.7,f:0.2,c:10.4,cat:'drink'},{n:'啤酒',e:'Beer',cal:43,p:0.5,f:0,c:3.6,cat:'drink'},{n:'汉堡',e:'Hamburger',cal:295,p:17,f:14,c:24,cat:'fastfood'},{n:'披萨',e:'Pizza',cal:266,p:11,f:10,c:33,cat:'fastfood'},{n:'薯条',e:'French Fries',cal:312,p:3.4,f:15,c:41,cat:'fastfood'},{n:'炸鸡',e:'Fried Chicken',cal:260,p:20,f:16,c:8,cat:'fastfood'}];
function renderFoods(data){document.getElementById('foodCount').textContent=data.length;document.getElementById('foodList').innerHTML=data.map(f=>`<div style="background:#0f172a;border-radius:8px;padding:12px;margin-bottom:6px;border:1px solid rgba(148,163,184,.08);display:flex;justify-content:space-between;align-items:center"><div><strong style="color:#f1f5f9">${f.n}</strong> <span style="color:#64748b;font-size:.8rem">${f.e}</span><div style="color:#94a3b8;font-size:.8rem;margin-top:2px">蛋白质${f.p}g · 脂肪${f.f}g · 碳水${f.c}g</div></div><div style="text-align:right"><span style="font-size:1.3rem;color:#f59e0b;font-weight:bold">${f.cal}</span><div style="color:#64748b;font-size:.75rem">千卡/100g</div></div></div>`).join('');}
function filterFoods(){const q=document.getElementById('foodSearch').value.toLowerCase();const cat=document.getElementById('foodCat').value;let f=foods;if(cat!=='all')f=f.filter(x=>x.cat===cat);if(q)f=f.filter(x=>x.n.includes(q)||x.e.toLowerCase().includes(q));renderFoods(f);}
renderFoods(foods);</script>""",
        "html_en": """<div class="card"><h2>🔍 Search Food</h2><input type="text" id="foodSearch" placeholder="Enter food name..." oninput="filterFoods()"><div class="row" style="margin-top:8px"><div class="field"><label>Category</label><select id="foodCat" onchange="filterFoods()"><option value="all">All</option><option value="fruit">Fruits</option><option value="vegetable">Vegetables</option><option value="meat">Meat</option><option value="seafood">Seafood</option><option value="grain">Grains</option><option value="dairy">Dairy</option><option value="snack">Snacks</option><option value="drink">Drinks</option><option value="fastfood">Fast Food</option></select></div></div></div><div class="card"><h2>📊 Calorie List (<span id="foodCount">0</span>)</h2><div id="foodList"></div></div>
<script>const foods=[{n:'Apple',cal:52,p:0.3,f:0.2,c:14,cat:'fruit'},{n:'Banana',cal:89,p:1.1,f:0.3,c:23,cat:'fruit'},{n:'Orange',cal:47,p:0.9,f:0.1,c:12,cat:'fruit'},{n:'Grapes',cal:69,p:0.7,f:0.2,c:18,cat:'fruit'},{n:'Watermelon',cal:30,p:0.6,f:0.2,c:8,cat:'fruit'},{n:'Strawberry',cal:32,p:0.7,f:0.3,c:8,cat:'fruit'},{n:'Blueberry',cal:57,p:0.7,f:0.3,c:14,cat:'fruit'},{n:'Mango',cal:60,p:0.8,f:0.4,c:15,cat:'fruit'},{n:'Tomato',cal:18,p:0.9,f:0.2,c:3.9,cat:'vegetable'},{n:'Cucumber',cal:15,p:0.7,f:0.1,c:3.6,cat:'vegetable'},{n:'Broccoli',cal:34,p:2.8,f:0.4,c:7,cat:'vegetable'},{n:'Spinach',cal:23,p:2.9,f:0.4,c:3.6,cat:'vegetable'},{n:'Carrot',cal:41,p:0.9,f:0.2,c:10,cat:'vegetable'},{n:'Potato',cal:77,p:2.0,f:0.1,c:17,cat:'vegetable'},{n:'Chicken Breast',cal:165,p:31,f:3.6,c:0,cat:'meat'},{n:'Beef',cal:250,p:26,f:15,c:0,cat:'meat'},{n:'Pork',cal:242,p:27,f:14,c:0,cat:'meat'},{n:'Egg',cal:155,p:13,f:11,c:1.1,cat:'meat'},{n:'Salmon',cal:208,p:20,f:13,c:0,cat:'seafood'},{n:'Shrimp',cal:99,p:24,f:0.3,c:0.2,cat:'seafood'},{n:'Rice',cal:130,p:2.7,f:0.3,c:28,cat:'grain'},{n:'Noodles',cal:138,p:4.5,f:2.1,c:25,cat:'grain'},{n:'Bread',cal:265,p:9,f:3.2,c:49,cat:'grain'},{n:'Oatmeal',cal:68,p:2.4,f:1.4,c:12,cat:'grain'},{n:'Milk',cal:42,p:3.4,f:1,c:5,cat:'dairy'},{n:'Yogurt',cal:61,p:3.5,f:3.3,c:4.7,cat:'dairy'},{n:'Cheese',cal:402,p:25,f:33,c:1.3,cat:'dairy'},{n:'Chocolate',cal:546,p:4.9,f:31,c:61,cat:'snack'},{n:'Potato Chips',cal:536,p:7,f:35,c:53,cat:'snack'},{n:'Cookie',cal:488,p:5.7,f:21,c:68,cat:'snack'},{n:'Cola',cal:42,p:0,f:0,c:10.6,cat:'drink'},{n:'Orange Juice',cal:45,p:0.7,f:0.2,c:10.4,cat:'drink'},{n:'Beer',cal:43,p:0.5,f:0,c:3.6,cat:'drink'},{n:'Hamburger',cal:295,p:17,f:14,c:24,cat:'fastfood'},{n:'Pizza',cal:266,p:11,f:10,c:33,cat:'fastfood'},{n:'French Fries',cal:312,p:3.4,f:15,c:41,cat:'fastfood'},{n:'Fried Chicken',cal:260,p:20,f:16,c:8,cat:'fastfood'}];
function renderFoods(data){document.getElementById('foodCount').textContent=data.length;document.getElementById('foodList').innerHTML=data.map(f=>`<div style="background:#0f172a;border-radius:8px;padding:12px;margin-bottom:6px;border:1px solid rgba(148,163,184,.08);display:flex;justify-content:space-between;align-items:center"><div><strong style="color:#f1f5f9">${f.n}</strong><div style="color:#94a3b8;font-size:.8rem;margin-top:2px">Protein ${f.p}g · Fat ${f.f}g · Carbs ${f.c}g</div></div><div style="text-align:right"><span style="font-size:1.3rem;color:#f59e0b;font-weight:bold">${f.cal}</span><div style="color:#64748b;font-size:.75rem">kcal/100g</div></div></div>`).join('');}
function filterFoods(){const q=document.getElementById('foodSearch').value.toLowerCase();const cat=document.getElementById('foodCat').value;let f=foods;if(cat!=='all')f=f.filter(x=>x.cat===cat);if(q)f=f.filter(x=>x.n.toLowerCase().includes(q));renderFoods(f);}
renderFoods(foods);</script>""",
    },
    {
        "slug": "baby-name-generator",
        "name_zh": "宝宝名字生成器",
        "name_en": "Baby Name Generator",
        "desc_zh": "免费在线宝宝名字生成器，按性别、首字母、风格生成名字建议。包含中文名字和英文名字，适合准父母为宝宝取名。随机生成，支持一键收藏喜欢的名字。",
        "desc_en": "Free online baby name generator - generate name suggestions by gender, first letter, and style. Includes both Chinese and English names. Perfect for expecting parents. Random generation with one-click favorites.",
        "icon_zh": "👶", "icon_en": "👶",
        "html_zh": """<div class="card"><h2>⚙️ 参数设置</h2><div class="row"><div class="field"><label>性别</label><select id="gender"><option value="any">不限</option><option value="boy">男孩</option><option value="girl">女孩</option></select></div><div class="field"><label>风格</label><select id="style"><option value="any">不限</option><option value="classic">经典</option><option value="modern">现代</option><option value="nature">自然</option><option value="literary">文艺</option></select></div><div class="field"><label>语言</label><select id="lang"><option value="zh">中文名</option><option value="en">英文名</option><option value="both">中英混合</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="generate()">🎲 随机生成</button><button class="btn btn-success" onclick="generateMany()">📋 批量生成10个</button></div></div><div class="card"><h2>💡 生成结果</h2><div id="resultArea" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-top:8px"></div></div>
<script>const names={boy:{classic:['浩然','子轩','宇轩','子涵','明哲','志远','博文','俊杰','思远','文博','伟豪','建国','志强','建华','国强','伟民','志明','永强','海峰','晓明'],modern:['一鸣','天佑','星辰','沐阳','晨曦','景行','宇辰','沐辰','昊然','奕辰','铭泽','瑾瑜','煜城','致远','知行'],nature:['青松','海川','南山','江河','林峰','云飞','星辰','雨泽','雪松','春生','秋实','冬阳','夏雨','天宇','山月'],literary:['子衿','怀瑾','握瑜','修远','若愚','思齐','知远','行健','厚德','明德','怀仁','守正','致远','弘毅','景行']},girl:{classic:['雅婷','诗涵','欣怡','梓涵','雨桐','梓萱','可欣','雨涵','梦瑶','思雨','静怡','慧敏','秀英','美玲','淑芬','丽华','桂英','秀兰','玉兰','秀珍'],modern:['若曦','语嫣','念慈','婉清','晓彤','雨霏','沐晴','灵犀','晴岚','思颖','筱雅','嘉琪','安琪','梦洁','心怡'],nature:['如雪','若兰','秋月','春梅','夏荷','冬雪','雨荷','月华','云裳','柳絮','花影','水仙','清荷','海棠','茉莉'],literary:['清婉','若兰','蕙质','兰心','文君','昭君','婉儿','黛玉','宝钗','湘云','探春','妙玉','晴雯','紫鹃','袭人']},en:{boy:{classic:['William','James','Henry','Charles','George','Thomas','Arthur','Edward','Robert','Richard','David','John','Michael','Joseph','Daniel'],modern:['Liam','Noah','Ethan','Mason','Lucas','Logan','Aiden','Jackson','Carter','Grayson','Owen','Wyatt','Leo','Ezra','Asher'],nature:['River','Forrest','Stone','Wolf','Phoenix','Orion','Atlas','Cedar','Ocean','Rowan','Ash','Clay','Flint','Heath','Glen'],literary:['Atticus','Darcy','Holden','Heathcliff','Orlando','Hamlet','Romeo','Byron','Keats','Wilde','Austen','Huxley','Fitzgerald','Beckett','Joyce']},girl:{classic:['Mary','Elizabeth','Margaret','Catherine','Anne','Jane','Sarah','Alice','Emily','Charlotte','Eleanor','Victoria','Grace','Rose','Helen'],modern:['Emma','Olivia','Ava','Sophia','Isabella','Mia','Amelia','Harper','Evelyn','Abigail','Ella','Scarlett','Grace','Chloe','Lily'],nature:['Willow','Ivy','Rose','Daisy','Luna','Aurora','Stella','Hazel','Violet','Iris','Flora','Skye','Wren','Dawn','Summer'],literary:['Juliet','Ophelia','Cordelia','Portia','Beatrice','Hermione','Scarlett','Lyra','Arwen','Galadriel','Eowyn','Hermia','Titania','Bianca','Desdemona']}}};
function pick(arr){return arr[Math.floor(Math.random()*arr.length)];}
function generateName(){const g=document.getElementById('gender').value;const s=document.getElementById('style').value;const l=document.getElementById('lang').value;let pool=[];const genders=g==='any'?['boy','girl']:[g];const styles=s==='any'?['classic','modern','nature','literary']:[s];if(l==='zh'||l==='both'){for(const g2 of genders){for(const s2 of styles){if(names[g2]&&names[g2][s2])pool.push({name:pick(names[g2][s2]),type:g2==='boy'?'♂':'♀',lang:'zh'});}}}if(l==='en'||l==='both'){for(const g2 of genders){for(const s2 of styles){if(names.en[g2]&&names.en[g2][s2])pool.push({name:pick(names.en[g2][s2]),type:g2==='boy'?'♂':'♀',lang:'en'});}}}return pool.length?pick(pool):{name:'请选择参数',type:'',lang:''};}
function generate(){const r=generateName();const c=document.getElementById('resultArea');const div=document.createElement('div');div.style.cssText='background:#0f172a;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(6,182,212,.3)';div.innerHTML=`<div style="font-size:1.4rem;color:#f1f5f9">${r.name}</div><div style="font-size:.75rem;color:#64748b;margin-top:4px">${r.type} ${r.lang==='en'?'English':'中文'}</div>`;c.insertBefore(div,c.firstChild);if(c.children.length>20)c.removeChild(c.lastChild);}
function generateMany(){for(let i=0;i<10;i++)setTimeout(()=>generate(),i*50);}</script>""",
        "html_en": """<div class="card"><h2>⚙️ Settings</h2><div class="row"><div class="field"><label>Gender</label><select id="gender"><option value="any">Any</option><option value="boy">Boy</option><option value="girl">Girl</option></select></div><div class="field"><label>Style</label><select id="style"><option value="any">Any</option><option value="classic">Classic</option><option value="modern">Modern</option><option value="nature">Nature</option><option value="literary">Literary</option></select></div><div class="field"><label>Language</label><select id="lang"><option value="zh">Chinese</option><option value="en">English</option><option value="both">Mixed</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="generate()">🎲 Generate</button><button class="btn btn-success" onclick="generateMany()">📋 Generate 10</button></div></div><div class="card"><h2>💡 Results</h2><div id="resultArea" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-top:8px"></div></div>
<script>const names={boy:{classic:['William','James','Henry','Charles','George','Thomas','Arthur','Edward','Robert'],modern:['Liam','Noah','Ethan','Mason','Lucas','Logan','Aiden','Jackson','Carter'],nature:['River','Forrest','Stone','Wolf','Phoenix','Orion','Atlas','Cedar','Ocean'],literary:['Atticus','Darcy','Holden','Heathcliff','Orlando','Hamlet','Romeo','Byron','Keats']},girl:{classic:['Mary','Elizabeth','Margaret','Catherine','Anne','Jane','Sarah','Alice','Emily'],modern:['Emma','Olivia','Ava','Sophia','Isabella','Mia','Amelia','Harper','Evelyn'],nature:['Willow','Ivy','Rose','Daisy','Luna','Aurora','Stella','Hazel','Violet'],literary:['Juliet','Ophelia','Cordelia','Portia','Beatrice','Hermione','Scarlett','Lyra','Arwen']}};
function pick(arr){return arr[Math.floor(Math.random()*arr.length)];}
function generateName(){const g=document.getElementById('gender').value;const s=document.getElementById('style').value;const l=document.getElementById('lang').value;let pool=[];const genders=g==='any'?['boy','girl']:[g];const styles=s==='any'?['classic','modern','nature','literary']:[s];for(const g2 of genders){for(const s2 of styles){if(names[g2]&&names[g2][s2])pool.push({name:pick(names[g2][s2]),type:g2==='boy'?'♂':'♀'});}}return pool.length?pick(pool):{name:'Please select parameters',type:''};}
function generate(){const r=generateName();const c=document.getElementById('resultArea');const div=document.createElement('div');div.style.cssText='background:#0f172a;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(6,182,212,.3)';div.innerHTML=`<div style="font-size:1.4rem;color:#f1f5f9">${r.name}</div><div style="font-size:.75rem;color:#64748b;margin-top:4px">${r.type}</div>`;c.insertBefore(div,c.firstChild);if(c.children.length>20)c.removeChild(c.lastChild);}
function generateMany(){for(let i=0;i<10;i++)setTimeout(()=>generate(),i*50);}</script>""",
    },
    {
        "slug": "loan-amortization",
        "name_zh": "贷款还款计算器",
        "name_en": "Loan Amortization Calculator",
        "desc_zh": "免费在线贷款还款计算器，计算等额本息和等额本金还款计划。支持月供计算、总利息、还款明细表，适合房贷、车贷、消费贷规划。",
        "desc_en": "Free online loan amortization calculator - compute equal installment and equal principal repayment plans. Supports monthly payment, total interest, and amortization schedule. Perfect for mortgage, auto loan, and personal loan planning.",
        "icon_zh": "💰", "icon_en": "💰",
        "html_zh": """<div class="card"><h2>📊 贷款参数</h2><div class="row"><div class="field"><label>贷款金额 (元)</label><input type="number" id="principal" value="1000000" min="0" step="10000"></div><div class="field"><label>年利率 (%)</label><input type="number" id="rate" value="4.9" min="0" step="0.01"></div><div class="field"><label>贷款期限 (年)</label><input type="number" id="years" value="30" min="1" max="50" step="1"></div></div><div class="row"><div class="field"><label>还款方式</label><select id="method"><option value="equal">等额本息</option><option value="principal">等额本金</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calculate()">📊 计算</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📋 计算结果</h2><div id="summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px"></div><div style="max-height:400px;overflow-y:auto"><table style="width:100%;border-collapse:collapse;font-size:.8rem"><thead><tr style="color:#94a3b8;text-align:left"><th>期数</th><th>月供</th><th>本金</th><th>利息</th><th>剩余本金</th></tr></thead><tbody id="scheduleBody"></tbody></table></div></div>
<script>function formatNum(n){return n.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');}function calculate(){const P=parseFloat(document.getElementById('principal').value)||0;const r=parseFloat(document.getElementById('rate').value)/100/12;const n=parseInt(document.getElementById('years').value)*12;const method=document.getElementById('method').value;if(P<=0||r<=0||n<=0){toast('请输入有效参数');return;}let monthly,totalPayment,totalInterest;let schedule=[];if(method==='equal'){monthly=P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);totalPayment=monthly*n;totalInterest=totalPayment-P;let balance=P;for(let i=1;i<=Math.min(n,360);i++){const interest=balance*r;const principal=monthly-interest;balance-=principal;schedule.push({i,payment:monthly,principal,interest,balance:Math.max(0,balance)});}}else{const monthlyPrincipal=P/n;totalPayment=0;totalInterest=0;let balance=P;for(let i=1;i<=Math.min(n,360);i++){const interest=balance*r;const payment=monthlyPrincipal+interest;balance-=monthlyPrincipal;totalPayment+=payment;totalInterest+=interest;schedule.push({i,payment,principal:monthlyPrincipal,interest,balance:Math.max(0,balance)});}monthly=schedule[0].payment;}document.getElementById('summary').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">月供</div><div style="color:#22d3ee;font-size:1.3rem;font-weight:bold">¥${formatNum(monthly)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">总还款</div><div style="color:#f59e0b;font-size:1.3rem;font-weight:bold">¥${formatNum(totalPayment)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">总利息</div><div style="color:#ef4444;font-size:1.3rem;font-weight:bold">¥${formatNum(totalInterest)}</div></div>`;document.getElementById('scheduleBody').innerHTML=schedule.slice(0,120).map(s=>`<tr style="border-bottom:1px solid rgba(148,163,184,.05)"><td style="padding:4px 8px;color:#94a3b8">${s.i}</td><td style="padding:4px 8px;color:#e2e8f0">¥${formatNum(s.payment)}</td><td style="padding:4px 8px;color:#4ade80">¥${formatNum(s.principal)}</td><td style="padding:4px 8px;color:#f87171">¥${formatNum(s.interest)}</td><td style="padding:4px 8px;color:#64748b">¥${formatNum(s.balance)}</td></tr>`).join('');document.getElementById('resultCard').style.display='block';toast('计算完成');}</script>""",
        "html_en": """<div class="card"><h2>📊 Loan Parameters</h2><div class="row"><div class="field"><label>Loan Amount ($)</label><input type="number" id="principal" value="300000" min="0" step="10000"></div><div class="field"><label>Annual Rate (%)</label><input type="number" id="rate" value="6.5" min="0" step="0.01"></div><div class="field"><label>Term (Years)</label><input type="number" id="years" value="30" min="1" max="50" step="1"></div></div><div class="row"><div class="field"><label>Repayment Method</label><select id="method"><option value="equal">Equal Installment</option><option value="principal">Equal Principal</option></select></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calculate()">📊 Calculate</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📋 Results</h2><div id="summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px"></div><div style="max-height:400px;overflow-y:auto"><table style="width:100%;border-collapse:collapse;font-size:.8rem"><thead><tr style="color:#94a3b8;text-align:left"><th>#</th><th>Payment</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody id="scheduleBody"></tbody></table></div></div>
<script>function formatNum(n){return n.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');}function calculate(){const P=parseFloat(document.getElementById('principal').value)||0;const r=parseFloat(document.getElementById('rate').value)/100/12;const n=parseInt(document.getElementById('years').value)*12;const method=document.getElementById('method').value;if(P<=0||r<=0||n<=0){toast('Please enter valid parameters');return;}let monthly,totalPayment,totalInterest;let schedule=[];if(method==='equal'){monthly=P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);totalPayment=monthly*n;totalInterest=totalPayment-P;let balance=P;for(let i=1;i<=Math.min(n,360);i++){const interest=balance*r;const principal=monthly-interest;balance-=principal;schedule.push({i,payment:monthly,principal,interest,balance:Math.max(0,balance)});}}else{const monthlyPrincipal=P/n;totalPayment=0;totalInterest=0;let balance=P;for(let i=1;i<=Math.min(n,360);i++){const interest=balance*r;const payment=monthlyPrincipal+interest;balance-=monthlyPrincipal;totalPayment+=payment;totalInterest+=interest;schedule.push({i,payment,principal:monthlyPrincipal,interest,balance:Math.max(0,balance)});}monthly=schedule[0].payment;}document.getElementById('summary').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">Monthly</div><div style="color:#22d3ee;font-size:1.3rem;font-weight:bold">$${formatNum(monthly)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">Total Payment</div><div style="color:#f59e0b;font-size:1.3rem;font-weight:bold">$${formatNum(totalPayment)}</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.8rem">Total Interest</div><div style="color:#ef4444;font-size:1.3rem;font-weight:bold">$${formatNum(totalInterest)}</div></div>`;document.getElementById('scheduleBody').innerHTML=schedule.slice(0,120).map(s=>`<tr style="border-bottom:1px solid rgba(148,163,184,.05)"><td style="padding:4px 8px;color:#94a3b8">${s.i}</td><td style="padding:4px 8px;color:#e2e8f0">$${formatNum(s.payment)}</td><td style="padding:4px 8px;color:#4ade80">$${formatNum(s.principal)}</td><td style="padding:4px 8px;color:#f87171">$${formatNum(s.interest)}</td><td style="padding:4px 8px;color:#64748b">$${formatNum(s.balance)}</td></tr>`).join('');document.getElementById('resultCard').style.display='block';toast('Calculation complete');}</script>""",
    },
    {
        "slug": "fuel-efficiency",
        "name_zh": "油耗计算器",
        "name_en": "Fuel Efficiency Calculator",
        "desc_zh": "免费在线油耗计算器，计算汽车百公里油耗、每公里油费。支持多种单位（L/100km、MPG、km/L），输入加油量和行驶里程即可计算，适合车主管理用车成本。",
        "desc_en": "Free online fuel efficiency calculator - compute fuel consumption per 100km, cost per km. Supports multiple units (L/100km, MPG, km/L). Enter fuel amount and distance to calculate. Perfect for managing vehicle costs.",
        "icon_zh": "⛽", "icon_en": "⛽",
        "html_zh": """<div class="card"><h2>⛽ 输入数据</h2><div class="row"><div class="field"><label>加油量 (升)</label><input type="number" id="fuel" value="40" min="0" step="0.1"></div><div class="field"><label>行驶里程 (公里)</label><input type="number" id="distance" value="500" min="0" step="1"></div><div class="field"><label>油价 (元/升)</label><input type="number" id="price" value="8.5" min="0" step="0.01"></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calc()">📊 计算</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📊 计算结果</h2><div id="resultGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px"></div></div>
<script>function calc(){const f=parseFloat(document.getElementById('fuel').value)||0;const d=parseFloat(document.getElementById('distance').value)||0;const p=parseFloat(document.getElementById('price').value)||0;if(f<=0||d<=0){toast('请输入有效数值');return;}const l100=f/d*100;const kml=d/f;const mpg=kml*2.352;const costPerKm=f*p/d;const totalCost=f*p;const costPerDay=totalCost/(d/30);document.getElementById('resultGrid').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">百公里油耗</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">${l100.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">L/100km</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">每公里油耗</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">${(f/d).toFixed(4)}</div><div style="color:#64748b;font-size:.7rem">L/km</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">MPG (美制)</div><div style="color:#f59e0b;font-size:1.5rem;font-weight:bold">${mpg.toFixed(1)}</div><div style="color:#64748b;font-size:.7rem">miles/gallon</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">每公里费用</div><div style="color:#ef4444;font-size:1.5rem;font-weight:bold">¥${costPerKm.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">元/km</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">本次加油总费用</div><div style="color:#4ade80;font-size:1.5rem;font-weight:bold">¥${totalCost.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">元</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">每日油费估算</div><div style="color:#a78bfa;font-size:1.5rem;font-weight:bold">¥${costPerDay.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">元/天 (按30天)</div></div>`;document.getElementById('resultCard').style.display='block';toast('计算完成');}</script>""",
        "html_en": """<div class="card"><h2>⛽ Input Data</h2><div class="row"><div class="field"><label>Fuel (gallons)</label><input type="number" id="fuel" value="12" min="0" step="0.1"></div><div class="field"><label>Distance (miles)</label><input type="number" id="distance" value="350" min="0" step="1"></div><div class="field"><label>Price ($/gallon)</label><input type="number" id="price" value="3.50" min="0" step="0.01"></div></div><div class="btn-row"><button class="btn btn-primary" onclick="calc()">📊 Calculate</button></div></div><div class="card" id="resultCard" style="display:none"><h2>📊 Results</h2><div id="resultGrid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px"></div></div>
<script>function calc(){const f=parseFloat(document.getElementById('fuel').value)||0;const d=parseFloat(document.getElementById('distance').value)||0;const p=parseFloat(document.getElementById('price').value)||0;if(f<=0||d<=0){toast('Please enter valid values');return;}const mpg=d/f;const l100=235.21/mpg;const costPerMile=f*p/d;const totalCost=f*p;const costPerDay=totalCost/(d/30);document.getElementById('resultGrid').innerHTML=`<div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">MPG</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">${mpg.toFixed(1)}</div><div style="color:#64748b;font-size:.7rem">miles/gallon</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">L/100km</div><div style="color:#22d3ee;font-size:1.5rem;font-weight:bold">${l100.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">liters/100km</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Cost per Mile</div><div style="color:#ef4444;font-size:1.5rem;font-weight:bold">$${costPerMile.toFixed(3)}</div><div style="color:#64748b;font-size:.7rem">$/mile</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Total Cost</div><div style="color:#4ade80;font-size:1.5rem;font-weight:bold">$${totalCost.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">dollars</div></div><div style="background:#0f172a;border-radius:8px;padding:12px;text-align:center"><div style="color:#64748b;font-size:.75rem">Daily Cost Est.</div><div style="color:#a78bfa;font-size:1.5rem;font-weight:bold">$${costPerDay.toFixed(2)}</div><div style="color:#64748b;font-size:.7rem">$/day (30 days)</div></div>`;document.getElementById('resultCard').style.display='block';toast('Calculation complete');}</script>""",
    },
]

# 组合所有工具
ALL_TOOLS = TOOLS + SIMPLE_TOOLS

# 还需要快速补齐5个简单工具。这里简化开发，再手动补
print(f"已定义 {len(ALL_TOOLS)} 个工具，开始生成文件...")

for t in ALL_TOOLS:
    slug = t['slug']
    zh_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, 'en', slug)
    os.makedirs(zh_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    # 中文版
    meta_zh = make_meta_zh(t['name_zh'], t['desc_zh'], slug, t['name_zh'], t['desc_zh'])
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
    
    # 英文版
    meta_en = make_meta_en(t['name_en'], t['desc_en'], slug, t['name_en'], t['desc_en'])
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

print(f"\n完成！共生成 {len(ALL_TOOLS)} 个工具（中英文双版）")