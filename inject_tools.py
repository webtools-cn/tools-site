#!/usr/bin/env python3
"""给5个工具的10个页面注入实际工具代码，替换#tool-placeholder"""
import os, re

BASE = os.path.expanduser("~/tools-site")

# 各工具的placehoder替换代码
tool_implementations = {
    "webp-converter": {
        "cn": '''  <div class="input-section">
    <h2>📤 上传图片</h2>
    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
      <p>拖放图片到此处，或点击上传（支持批量，最多20张）</p>
      <p style="color:#64748b;font-size:.8rem">支持 WebP、PNG、JPEG、GIF 格式</p>
    </div>
    <input type="file" id="fileInput" accept="image/webp,image/png,image/jpeg,image/gif" multiple onchange="handleFiles(this.files)">
    
    <div class="form-row">
      <label>目标格式：</label>
      <select id="targetFormat" onchange="convertAll()">
        <option value="image/webp">WebP</option>
        <option value="image/png">PNG</option>
        <option value="image/jpeg">JPEG</option>
        <option value="image/gif">GIF</option>
      </select>
      <label>质量：</label>
      <input type="range" id="quality" min="10" max="100" value="85" oninput="document.getElementById('qVal').textContent=this.value;convertAll()">
      <span id="qVal">85</span>
    </div>
    
    <div id="fileList" style="margin-top:12px;display:flex;flex-wrap:wrap;gap:8px"></div>
    <div class="btn-row">
      <button class="btn btn-primary" onclick="downloadAll()" id="dlAllBtn" disabled>💾 下载全部</button>
      <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清除</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 转换结果</h2>
    <div id="results" class="empty-state">上传图片后这里显示转换结果</div>
  </div>''',
        "en": '''  <div class="input-section">
    <h2>📤 Upload Images</h2>
    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
      <p>Drag & drop images here, or click to upload (batch, up to 20)</p>
      <p style="color:#64748b;font-size:.8rem">Supports WebP, PNG, JPEG, GIF formats</p>
    </div>
    <input type="file" id="fileInput" accept="image/webp,image/png,image/jpeg,image/gif" multiple onchange="handleFiles(this.files)">
    
    <div class="form-row">
      <label>Target Format:</label>
      <select id="targetFormat" onchange="convertAll()">
        <option value="image/webp">WebP</option>
        <option value="image/png">PNG</option>
        <option value="image/jpeg">JPEG</option>
        <option value="image/gif">GIF</option>
      </select>
      <label>Quality:</label>
      <input type="range" id="quality" min="10" max="100" value="85" oninput="document.getElementById('qVal').textContent=this.value;convertAll()">
      <span id="qVal">85</span>
    </div>
    
    <div id="fileList" style="margin-top:12px;display:flex;flex-wrap:wrap;gap:8px"></div>
    <div class="btn-row">
      <button class="btn btn-primary" onclick="downloadAll()" id="dlAllBtn" disabled>💾 Download All</button>
      <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 Conversion Results</h2>
    <div id="results" class="empty-state">Upload images to see conversion results here</div>
  </div>''',
        "js": '''const uploadZone = document.getElementById('uploadZone');
['dragover','dragenter'].forEach(e=>{uploadZone.addEventListener(e,ev=>{ev.preventDefault();uploadZone.classList.add('dragover')})});
['dragleave','drop'].forEach(e=>{uploadZone.addEventListener(e,ev=>{ev.preventDefault();uploadZone.classList.remove('dragover')})});
uploadZone.addEventListener('drop',e=>{const files=e.dataTransfer.files;if(files.length)handleFiles(files)});

let imageFiles=[], convertedBlobs=[];

function handleFiles(files){
  imageFiles=Array.from(files).filter(f=>f.type.startsWith('image/')).slice(0,20);
  if(!imageFiles.length){showToast('⚠️ 请选择图片文件');return}
  const list=document.getElementById('fileList');
  list.innerHTML=imageFiles.map((f,i)=>`<div style="background:#0f172a;border-radius:8px;padding:8px 12px;font-size:.8rem;color:#94a3b8;display:flex;align-items:center;gap:8px">📄 ${f.name} <span style="color:#64748b">(${(f.size/1024).toFixed(1)}KB)</span> <span onclick="removeFile(${i})" style="cursor:pointer;color:#f87171;margin-left:auto">✕</span></div>`).join('');
  list.innerHTML+=`<div style="color:#64748b;font-size:.8rem;padding:8px">共 ${imageFiles.length} 个文件</div>`;
  convertAll();
}

function removeFile(i){imageFiles.splice(i,1);handleFiles(imageFiles.length?imageFiles:[]);convertAll()}

function convertAll(){
  const fmt=document.getElementById('targetFormat').value;
  const q=parseInt(document.getElementById('quality').value)/100;
  const results=document.getElementById('results');
  if(!imageFiles.length){results.innerHTML='<div class="empty-state">请先上传图片</div>';document.getElementById('dlAllBtn').disabled=true;return}
  
  results.innerHTML='<div style="color:#22d3ee;text-align:center;padding:20px">⏳ 转换中...</div>';
  convertedBlobs=[];
  let done=0;
  
  imageFiles.forEach((f,i)=>{
    const reader=new FileReader();
    reader.onload=function(e){
      const img=new Image();
      img.onload=function(){
        const canvas=document.createElement('canvas');
        canvas.width=img.width;canvas.height=img.height;
        const ctx=canvas.getContext('2d');
        ctx.drawImage(img,0,0);
        canvas.toBlob(blob=>{
          const ext=fmt.split('/')[1];
          const name=f.name.replace(/\\.[^.]+$/,'.'+ext);
          convertedBlobs[i]={blob,name,origName:f.name,origSize:f.size,newSize:blob.size};
          done++;
          if(done===imageFiles.length)showResults();
        },fmt,q);
      };
      img.src=e.target.result;
    };
    reader.readAsDataURL(f);
  });
}

function showResults(){
  const results=document.getElementById('results');
  let html='';
  convertedBlobs.forEach((r,i)=>{
    const reduction=((1-r.newSize/r.origSize)*100).toFixed(0);
    const color=reduction>0?'#4ade80':(reduction<0?'#f87171':'#94a3b8');
    html+=`<div style="display:flex;align-items:center;gap:12px;padding:12px;background:#0f172a;border-radius:8px;margin-bottom:8px">
      <span>📄</span>
      <div style="flex:1"><div style="font-size:.85rem;color:#e2e8f0">${r.name}</div>
      <div style="font-size:.75rem;color:#64748b">${(r.origSize/1024).toFixed(1)}KB → ${(r.newSize/1024).toFixed(1)}KB <span style="color:${color}">${reduction>0?'↓':'↑'}${Math.abs(reduction)}%</span></div></div>
      <button class="btn btn-primary" style="font-size:.75rem;padding:6px 12px" onclick="downloadOne(${i})">⬇ 下载</button>
    </div>`;
  });
  results.innerHTML=html||'<div class="empty-state">无结果</div>';
  document.getElementById('dlAllBtn').disabled=!convertedBlobs.length;
}

function downloadOne(i){
  const r=convertedBlobs[i];
  const url=URL.createObjectURL(r.blob);
  const a=document.createElement('a');a.href=url;a.download=r.name;a.click();
  URL.revokeObjectURL(url);showToast('✅ 已下载');
}

function downloadAll(){
  convertedBlobs.forEach((r,i)=>setTimeout(()=>downloadOne(i),i*300));
  showToast('✅ 开始下载全部');
}

function clearAll(){imageFiles=[];convertedBlobs=[];document.getElementById('fileList').innerHTML='';document.getElementById('results').innerHTML='<div class="empty-state">已清除</div>';document.getElementById('dlAllBtn').disabled=true;document.getElementById('fileInput').value=''}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}'''
    },
    "ascii-art": {
        "cn": '''  <div class="input-section">
    <h2>📝 输入内容</h2>
    <div class="form-row">
      <label>模式：</label>
      <select id="mode" onchange="switchMode()">
        <option value="text">文字转ASCII</option>
        <option value="image">图片转ASCII</option>
      </select>
    </div>
    
    <div id="textMode">
      <textarea id="textInput" placeholder="输入要转换的文字..." oninput="generateTextArt()">Hello</textarea>
      <div class="form-row">
        <label>字体：</label>
        <select id="fontStyle" onchange="generateTextArt()">
          <option value="standard">标准</option>
          <option value="block">方块</option>
          <option value="lean">细体</option>
          <option value="bubble">气泡</option>
          <option value="script">手写</option>
          <option value="squared">正方形</option>
        </select>
      </div>
    </div>
    
    <div id="imageMode" style="display:none">
      <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
        <p>拖放图片到此处，或点击上传</p>
      </div>
      <input type="file" id="fileInput" accept="image/*" onchange="handleImage(this.files[0])">
      <div class="form-row">
        <label>宽度：</label>
        <input type="range" id="imgWidth" min="40" max="120" value="80" oninput="document.getElementById('wVal').textContent=this.value;generateImageArt()">
        <span id="wVal">80</span>
      </div>
    </div>
    
    <div class="form-row">
      <label>字符集：</label>
      <select id="charSet" onchange="onCharSetChange()">
        <option value="standard">标准 (@%#*+=-:. )</option>
        <option value="blocks">方块 (█▓▒░)</option>
        <option value="detailed">详细 (复杂字符)</option>
        <option value="custom">自定义</option>
      </select>
    </div>
    <div class="form-row" id="customCharRow" style="display:none">
      <label>自定义：</label>
      <input type="text" id="customChars" value="@%#*+=-:. " style="flex:1" oninput="onCustomChange()">
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="copyResult()">📋 复制ASCII艺术</button>
      <button class="btn btn-secondary" onclick="downloadTxt()">💾 下载文本</button>
    </div>
  </div>

  <div class="result-section">
    <h2>🎨 ASCII艺术预览</h2>
    <div id="asciiPreview" class="result-content" style="font-size:6px;line-height:1;letter-spacing:0;min-height:100px">等待输入...</div>
  </div>''',
        "en": '''  <div class="input-section">
    <h2>📝 Input Content</h2>
    <div class="form-row">
      <label>Mode:</label>
      <select id="mode" onchange="switchMode()">
        <option value="text">Text to ASCII</option>
        <option value="image">Image to ASCII</option>
      </select>
    </div>
    
    <div id="textMode">
      <textarea id="textInput" placeholder="Enter text to convert..." oninput="generateTextArt()">Hello</textarea>
      <div class="form-row">
        <label>Font:</label>
        <select id="fontStyle" onchange="generateTextArt()">
          <option value="standard">Standard</option>
          <option value="block">Block</option>
          <option value="lean">Lean</option>
          <option value="bubble">Bubble</option>
          <option value="script">Script</option>
          <option value="squared">Squared</option>
        </select>
      </div>
    </div>
    
    <div id="imageMode" style="display:none">
      <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
        <p>Drag & drop an image here, or click to upload</p>
      </div>
      <input type="file" id="fileInput" accept="image/*" onchange="handleImage(this.files[0])">
      <div class="form-row">
        <label>Width:</label>
        <input type="range" id="imgWidth" min="40" max="120" value="80" oninput="document.getElementById('wVal').textContent=this.value;generateImageArt()">
        <span id="wVal">80</span>
      </div>
    </div>
    
    <div class="form-row">
      <label>Char Set:</label>
      <select id="charSet" onchange="onCharSetChange()">
        <option value="standard">Standard (@%#*+=-:. )</option>
        <option value="blocks">Blocks (█▓▒░)</option>
        <option value="detailed">Detailed</option>
        <option value="custom">Custom</option>
      </select>
    </div>
    <div class="form-row" id="customCharRow" style="display:none">
      <label>Custom:</label>
      <input type="text" id="customChars" value="@%#*+=-:. " style="flex:1" oninput="onCustomChange()">
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="copyResult()">📋 Copy ASCII Art</button>
      <button class="btn btn-secondary" onclick="downloadTxt()">💾 Download Text</button>
    </div>
  </div>

  <div class="result-section">
    <h2>🎨 ASCII Art Preview</h2>
    <div id="asciiPreview" class="result-content" style="font-size:6px;line-height:1;letter-spacing:0;min-height:100px">Waiting for input...</div>
  </div>''',
        "js": '''const fontDefs={
  standard:{A:'  A  \\n A A \\nAAAAA\\nA   A\\nA   A',B:'BBBB \\nB   B\\nBBBB \\nB   B\\nBBBB ',C:' CCCC\\nC    \\nC    \\nC    \\n CCCC',H:'H   H\\nH   H\\nHHHHH\\nH   H\\nH   H',E:'EEEEE\\nE    \\nEEEEE\\nE    \\nEEEEE',L:'L    \\nL    \\nL    \\nL    \\nLLLLL',O:' OOO \\nO   O\\nO   O\\nO   O\\n OOO '},
  block:{A:'▗▄▄▄▖\\n▐▛▀▜▌\\n▐▌ ▐▌\\n▐▙▄▟▌\\n▐▌ ▐▌',B:'▗▄▄▄▖\\n▐▛▀▜▌\\n▐▙▄▟▌\\n▐▛▀▜▌\\n▐▙▄▟▌',H:'▐▌ ▐▌\\n▐▌ ▐▌\\n▐▙▄▟▌\\n▐▌ ▐▌\\n▐▌ ▐▌'},
  lean:{A:' /\\\\ \\n/__\\\\\\n|  |\\n|  |\\n|  |',B:'|--\\\\\\n|--/\\n|---\\\\\\n|--/\\n|--/',H:'|  |\\n|  |\\n|--|\\n|  |\\n|  |'},
  bubble:{A:' ╭╮ \\n│██│\\n╰╯╭╯\\n╭╮│ \\n╰╯╰╯',B:'╭╮╮ \\n├╯│ \\n├╮╯ \\n├╯│ \\n╰╯╯ '},
  script:{A:'  𝒶  \\n 𝒶 𝒶 \\n𝒶𝒶𝒶𝒶𝒶\\n𝒶   𝒶\\n𝒶   𝒶',B:'𝒷𝒷𝒷 \\n𝒷   𝒷\\n𝒷𝒷𝒷 \\n𝒷   𝒷\\n𝒷𝒷𝒷 '},
  squared:{A:'┏━━━┓\\n┃▀▄▀┃\\n┃ █ ┃\\n┃▄▀▄┃\\n┃   ┃',B:'┏━━━┓\\n┃▀▄▀┃\\n┃▄▀▄┃\\n┃▀▄▀┃\\n┗━━━┛'}
};

const charSets={
  standard:'@%#*+=-:. ',
  blocks:'█▓▒░ ',
  detailed:'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\\\|()1{}[]?-_+~<>i!lI;:,"^`\\'. '
};
let currentChars=charSets.standard;

function getFontChar(c,style){return(fontDefs[style]||fontDefs.standard)[c.toUpperCase()]||c}
function generateTextArt(){
  const text=document.getElementById('textInput').value||'Hello';
  const style=document.getElementById('fontStyle').value;
  const lines=Array(5).fill('');
  for(const ch of text){
    const fc=getFontChar(ch,style).split('\\n');
    for(let i=0;i<5;i++)lines[i]+=(fc[i]||' '.repeat(fc[0]?.length||3))+' ';
  }
  document.getElementById('asciiPreview').textContent=lines.join('\\n');
}
let imageData=null;
function handleImage(file){
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    const img=new Image();
    img.onload=function(){imageData=img;generateImageArt()};
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}
function generateImageArt(){
  if(!imageData)return;
  const w=parseInt(document.getElementById('imgWidth').value);
  const h=Math.round(imageData.height*w/imageData.width/2);
  const canvas=document.createElement('canvas');
  canvas.width=w;canvas.height=h;
  const ctx=canvas.getContext('2d');
  ctx.drawImage(imageData,0,0,w,h);
  const data=ctx.getImageData(0,0,w,h).data;
  let result='';
  for(let y=0;y<h;y++){
    for(let x=0;x<w;x++){
      const i=(y*w+x)*4;
      const gray=(data[i]*0.299+data[i+1]*0.587+data[i+2]*0.114);
      const idx=Math.floor(gray/255*(currentChars.length-1));
      result+=currentChars[currentChars.length-1-idx]||' ';
    }
    result+='\\n';
  }
  document.getElementById('asciiPreview').textContent=result;
}
function switchMode(){
  const mode=document.getElementById('mode').value;
  document.getElementById('textMode').style.display=mode==='text'?'block':'none';
  document.getElementById('imageMode').style.display=mode==='image'?'block':'none';
  if(mode==='text')generateTextArt();else generateImageArt();
}
function onCharSetChange(){
  const v=document.getElementById('charSet').value;
  document.getElementById('customCharRow').style.display=v==='custom'?'flex':'none';
  currentChars=v==='custom'?(document.getElementById('customChars').value||'@%#'):charSets[v];
  if(document.getElementById('mode').value==='image')generateImageArt();else generateTextArt();
}
function onCustomChange(){currentChars=document.getElementById('customChars').value;generateImageArt()}
function copyResult(){
  const text=document.getElementById('asciiPreview').textContent;
  navigator.clipboard.writeText(text).then(()=>showToast('✅ 已复制'));
}
function downloadTxt(){
  const text=document.getElementById('asciiPreview').textContent;
  const blob=new Blob([text],{type:'text/plain'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ascii-art.txt';a.click();
}
const uz=document.getElementById('uploadZone');if(uz){['dragover','dragenter'].forEach(e=>{uz.addEventListener(e,ev=>{ev.preventDefault();uz.classList.add('dragover')})});['dragleave','drop'].forEach(e=>{uz.addEventListener(e,ev=>{ev.preventDefault();uz.classList.remove('dragover')})});uz.addEventListener('drop',e=>{const f=e.dataTransfer.files[0];if(f)handleImage(f)})}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}
generateTextArt();'''
    },
    "csv-diff": {
        "cn": '''  <div class="input-section">
    <h2>📊 上传CSV文件</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">文件A（原始）</h3>
        <textarea id="csvA" placeholder="粘贴CSV内容或拖放文件..." style="min-height:150px"></textarea>
        <input type="file" id="fileA" accept=".csv,.tsv,.txt" onchange="loadFile(this,'csvA')" style="margin-top:8px;color:#94a3b8;font-size:.8rem">
      </div>
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">文件B（新版）</h3>
        <textarea id="csvB" placeholder="粘贴CSV内容或拖放文件..." style="min-height:150px"></textarea>
        <input type="file" id="fileB" accept=".csv,.tsv,.txt" onchange="loadFile(this,'csvB')" style="margin-top:8px;color:#94a3b8;font-size:.8rem">
      </div>
    </div>
    
    <div class="form-row">
      <label>分隔符：</label>
      <select id="delimiter">
        <option value="auto">自动检测</option>
        <option value=",">逗号 (,)</option>
        <option value=";">分号 (;)</option>
        <option value="\\t">Tab</option>
      </select>
      <label><input type="checkbox" id="ignoreCase"> 忽略大小写</label>
      <label><input type="checkbox" id="ignoreWS"> 忽略空白</label>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="compare()">🔍 对比</button>
      <button class="btn btn-secondary" onclick="loadSample()">📋 加载示例</button>
      <button class="btn btn-secondary" onclick="clearCSV()">🗑️ 清除</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 对比结果 <span id="diffStats" style="font-size:.85rem;color:#94a3b8"></span></h2>
    <div class="form-row">
      <label>筛选：</label>
      <select id="filterType" onchange="applyFilter()">
        <option value="all">全部</option>
        <option value="added">新增</option>
        <option value="removed">删除</option>
        <option value="modified">修改</option>
      </select>
    </div>
    <div id="diffResult" class="result-content" style="max-height:500px">上传两个CSV文件后点击对比</div>
    <div class="btn-row" style="margin-top:12px">
      <button class="btn btn-primary" onclick="exportHTML()" id="exportBtn" disabled>📄 导出HTML报告</button>
    </div>
  </div>''',
        "en": '''  <div class="input-section">
    <h2>📊 Upload CSV Files</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">File A (Original)</h3>
        <textarea id="csvA" placeholder="Paste CSV content or drop a file..." style="min-height:150px"></textarea>
        <input type="file" id="fileA" accept=".csv,.tsv,.txt" onchange="loadFile(this,'csvA')" style="margin-top:8px;color:#94a3b8;font-size:.8rem">
      </div>
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">File B (New)</h3>
        <textarea id="csvB" placeholder="Paste CSV content or drop a file..." style="min-height:150px"></textarea>
        <input type="file" id="fileB" accept=".csv,.tsv,.txt" onchange="loadFile(this,'csvB')" style="margin-top:8px;color:#94a3b8;font-size:.8rem">
      </div>
    </div>
    
    <div class="form-row">
      <label>Delimiter:</label>
      <select id="delimiter">
        <option value="auto">Auto-detect</option>
        <option value=",">Comma (,)</option>
        <option value=";">Semicolon (;)</option>
        <option value="\\t">Tab</option>
      </select>
      <label><input type="checkbox" id="ignoreCase"> Ignore Case</label>
      <label><input type="checkbox" id="ignoreWS"> Ignore Whitespace</label>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="compare()">🔍 Compare</button>
      <button class="btn btn-secondary" onclick="loadSample()">📋 Load Sample</button>
      <button class="btn btn-secondary" onclick="clearCSV()">🗑️ Clear</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 Comparison Results <span id="diffStats" style="font-size:.85rem;color:#94a3b8"></span></h2>
    <div class="form-row">
      <label>Filter:</label>
      <select id="filterType" onchange="applyFilter()">
        <option value="all">All</option>
        <option value="added">Added</option>
        <option value="removed">Removed</option>
        <option value="modified">Modified</option>
      </select>
    </div>
    <div id="diffResult" class="result-content" style="max-height:500px">Upload two CSV files then click Compare</div>
    <div class="btn-row" style="margin-top:12px">
      <button class="btn btn-primary" onclick="exportHTML()" id="exportBtn" disabled>📄 Export HTML Report</button>
    </div>
  </div>''',
        "js": '''function loadFile(input,targetId){
  const file=input.files[0];if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){document.getElementById(targetId).value=e.target.result};
  reader.readAsText(file);
}
function detectDelim(text){
  const firstLine=text.split('\\n')[0]||'';
  const counts={',':(firstLine.match(/,/g)||[]).length,';':(firstLine.match(/;/g)||[]).length,'\\t':(firstLine.match(/\\t/g)||[]).length};
  const best=Object.entries(counts).sort((a,b)=>b[1]-a[1])[0];
  return best[1]>0?best[0]:',';
}
function parseCSV(text,delim,ignoreCase,ignoreWS){
  if(delim==='auto')delim=detectDelim(text);
  const lines=text.trim().split(/\\r?\\n/).filter(l=>l.trim());
  return lines.map(l=>{
    let row=[];let current='';let inQuote=false;
    for(let i=0;i<l.length;i++){
      const ch=l[i];
      if(ch==='"'){inQuote=!inQuote}
      else if((ch===delim||(delim==='\\t'&&ch==='\\t'))&&!inQuote){row.push(current);current=''}
      else current+=ch;
    }
    row.push(current);
    if(ignoreWS)row=row.map(c=>c.trim());
    if(ignoreCase)row=row.map(c=>c.toLowerCase());
    return row;
  });
}
function rowsEqual(a,b){return a.length===b.length&&a.every((v,i)=>v===b[i])}

let diffData=null;
function compare(){
  const a=document.getElementById('csvA').value.trim();
  const b=document.getElementById('csvB').value.trim();
  if(!a||!b){showToast('⚠️ 请填写两个CSV内容');return}
  
  const delim=document.getElementById('delimiter').value;
  const ic=document.getElementById('ignoreCase').checked;
  const iw=document.getElementById('ignoreWS').checked;
  
  const rowsA=parseCSV(a,delim,ic,iw);
  const rowsB=parseCSV(b,delim,ic,iw);
  
  diffData={added:[],removed:[],modified:[],all:[]};
  
  const aSet=new Set(rowsA.map(r=>r.join('|')));
  const bSet=new Set(rowsB.map(r=>r.join('|')));
  
  // Find removed (in A but not B)
  rowsA.forEach((row,i)=>{
    const key=row.join('|');
    if(!bSet.has(key)){
      // Check if it's modified (same position but different)
      if(i<rowsB.length&&!rowsEqual(row,rowsB[i])){
        diffData.modified.push({type:'modified',oldRow:row,newRow:rowsB[i],idx:i});
        diffData.all.push({type:'modified',oldRow:row,newRow:rowsB[i],idx:i});
      }else{
        diffData.removed.push({type:'removed',row,idx:i});
        diffData.all.push({type:'removed',row,idx:i});
      }
    }
  });
  
  // Find added (in B but not A)
  rowsB.forEach((row,i)=>{
    const key=row.join('|');
    if(!aSet.has(key)&&!diffData.modified.some(m=>rowsEqual(m.newRow,row))){
      diffData.added.push({type:'added',row,idx:i});
      diffData.all.push({type:'added',row,idx:i});
    }
  });
  
  // Add matching rows
  const maxLen=Math.max(rowsA.length,rowsB.length);
  for(let i=0;i<maxLen;i++){
    if(i<rowsA.length&&i<rowsB.length&&rowsEqual(rowsA[i],rowsB[i])){
      diffData.all.push({type:'same',row:rowsA[i],idx:i});
    }
  }
  
  document.getElementById('diffStats').textContent=` | 新增:${diffData.added.length} 删除:${diffData.removed.length} 修改:${diffData.modified.length}`;
  document.getElementById('exportBtn').disabled=false;
  applyFilter();
}

function applyFilter(){
  if(!diffData){return}
  const filter=document.getElementById('filterType').value;
  let items=filter==='all'?diffData.all:diffData[filter];
  const result=document.getElementById('diffResult');
  
  let html='';
  items.forEach(item=>{
    if(item.type==='added'){
      html+=`<div style="padding:4px 8px;margin:2px 0;border-radius:4px" class="diff-added">+ ${item.row.join(', ')}</div>`;
    }else if(item.type==='removed'){
      html+=`<div style="padding:4px 8px;margin:2px 0;border-radius:4px" class="diff-removed">- ${item.row.join(', ')}</div>`;
    }else if(item.type==='modified'){
      html+=`<div style="padding:4px 8px;margin:2px 0;border-radius:4px" class="diff-modified">~ ${item.oldRow.join(', ')} → ${item.newRow.join(', ')}</div>`;
    }else{
      html+=`<div style="padding:4px 8px;margin:2px 0;color:#64748b">  ${item.row.join(', ')}</div>`;
    }
  });
  result.innerHTML=html||'<div style="color:#64748b;padding:8px">无匹配结果</div>';
}

function loadSample(){
  document.getElementById('csvA').value='Name,Age,City\\nAlice,30,New York\\nBob,25,Boston\\nCharlie,35,Chicago\\nDiana,28,Denver';
  document.getElementById('csvB').value='Name,Age,City\\nAlice,30,New York\\nBob,26,Boston\\nCharlie,35,Seattle\\nEve,22,Portland';
  showToast('✅ 示例已加载');
}

function clearCSV(){
  document.getElementById('csvA').value='';
  document.getElementById('csvB').value='';
  document.getElementById('diffResult').innerHTML='已清除';
  document.getElementById('diffStats').textContent='';
  document.getElementById('exportBtn').disabled=true;
  diffData=null;
}

function exportHTML(){
  if(!diffData)return;
  const filter=document.getElementById('filterType').value;
  let items=filter==='all'?diffData.all:diffData[filter];
  let html='<html><head><meta charset="UTF-8"><style>body{font-family:monospace;background:#0f172a;color:#e2e8f0;padding:20px}.a{background:rgba(34,197,94,.15);color:#4ade80}.r{background:rgba(239,68,68,.15);color:#f87171}.m{background:rgba(234,179,8,.15);color:#facc15}</style></head><body><h1>CSV Diff Report</h1>';
  items.forEach(item=>{
    if(item.type==='added')html+=`<div class="a">+ ${item.row.join(', ')}</div>`;
    else if(item.type==='removed')html+=`<div class="r">- ${item.row.join(', ')}</div>`;
    else if(item.type==='modified')html+=`<div class="m">~ ${item.oldRow.join(', ')} → ${item.newRow.join(', ')}</div>`;
  });
  html+='</body></html>';
  const blob=new Blob([html],{type:'text/html'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='csv-diff-report.html';a.click();
  showToast('✅ 报告已下载');
}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}'''
    },
    "gif-to-mp4": {
        "cn": '''  <div class="input-section">
    <h2>📤 上传GIF</h2>
    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
      <p>拖放GIF动图到此处，或点击上传</p>
      <p style="color:#64748b;font-size:.8rem">最大50MB，支持透明GIF</p>
    </div>
    <input type="file" id="fileInput" accept="image/gif" onchange="handleGIF(this.files[0])">
    
    <div id="gifInfo" style="display:none;margin-top:12px">
      <div class="form-row">
        <label>帧率：</label>
        <input type="range" id="fps" min="5" max="30" value="15" oninput="document.getElementById('fpsVal').textContent=this.value">
        <span id="fpsVal">15</span>
      </div>
      <div class="form-row">
        <label>质量：</label>
        <select id="quality">
          <option value="0.9">高 (文件较大)</option>
          <option value="0.7" selected>中 (推荐)</option>
          <option value="0.5">低 (文件较小)</option>
        </select>
      </div>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="convertToMP4()" id="convertBtn" disabled>🎬 转换为MP4</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 转换结果</h2>
    <div id="gifPreview" class="preview-box">
      <p style="color:#64748b">GIF预览</p>
      <img id="gifImg" style="display:none;max-width:100%;max-height:300px">
    </div>
    <div id="mp4Result" style="display:none;margin-top:12px">
      <div class="preview-box">
        <p style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">MP4预览</p>
        <video id="mp4Video" controls loop autoplay muted style="max-width:100%;max-height:300px;border-radius:4px"></video>
      </div>
      <div class="btn-row" style="margin-top:12px">
        <button class="btn btn-primary" onclick="downloadMP4()">💾 下载MP4</button>
      </div>
      <div id="sizeCompare" style="margin-top:8px;font-size:.85rem;color:#94a3b8"></div>
    </div>
  </div>''',
        "en": '''  <div class="input-section">
    <h2>📤 Upload GIF</h2>
    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-7l5-5 5 5m-5-5v12" stroke-width="2"/></svg>
      <p>Drag & drop an animated GIF here, or click to upload</p>
      <p style="color:#64748b;font-size:.8rem">Max 50MB, supports transparent GIF</p>
    </div>
    <input type="file" id="fileInput" accept="image/gif" onchange="handleGIF(this.files[0])">
    
    <div id="gifInfo" style="display:none;margin-top:12px">
      <div class="form-row">
        <label>Frame Rate:</label>
        <input type="range" id="fps" min="5" max="30" value="15" oninput="document.getElementById('fpsVal').textContent=this.value">
        <span id="fpsVal">15</span>
      </div>
      <div class="form-row">
        <label>Quality:</label>
        <select id="quality">
          <option value="0.9">High (larger file)</option>
          <option value="0.7" selected>Medium (recommended)</option>
          <option value="0.5">Low (smaller file)</option>
        </select>
      </div>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="convertToMP4()" id="convertBtn" disabled>🎬 Convert to MP4</button>
    </div>
  </div>

  <div class="result-section">
    <h2>📋 Conversion Result</h2>
    <div id="gifPreview" class="preview-box">
      <p style="color:#64748b">GIF Preview</p>
      <img id="gifImg" style="display:none;max-width:100%;max-height:300px">
    </div>
    <div id="mp4Result" style="display:none;margin-top:12px">
      <div class="preview-box">
        <p style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">MP4 Preview</p>
        <video id="mp4Video" controls loop autoplay muted style="max-width:100%;max-height:300px;border-radius:4px"></video>
      </div>
      <div class="btn-row" style="margin-top:12px">
        <button class="btn btn-primary" onclick="downloadMP4()">💾 Download MP4</button>
      </div>
      <div id="sizeCompare" style="margin-top:8px;font-size:.85rem;color:#94a3b8"></div>
    </div>
  </div>''',
        "js": '''let gifFile=null,mp4Blob=null;
const uz=document.getElementById('uploadZone');
if(uz){
  ['dragover','dragenter'].forEach(e=>{uz.addEventListener(e,ev=>{ev.preventDefault();uz.classList.add('dragover')})});
  ['dragleave','drop'].forEach(e=>{uz.addEventListener(e,ev=>{ev.preventDefault();uz.classList.remove('dragover')})});
  uz.addEventListener('drop',e=>{const f=e.dataTransfer.files[0];if(f)handleGIF(f)});
}

function handleGIF(file){
  if(!file||!file.type.includes('gif')){showToast('⚠️ 请选择GIF文件');return}
  if(file.size>50*1024*1024){showToast('⚠️ 文件不能超过50MB');return}
  gifFile=file;
  
  const reader=new FileReader();
  reader.onload=function(e){
    document.getElementById('gifImg').src=e.target.result;
    document.getElementById('gifImg').style.display='block';
  };
  reader.readAsDataURL(file);
  
  document.getElementById('gifInfo').style.display='block';
  document.getElementById('convertBtn').disabled=false;
  document.getElementById('mp4Result').style.display='none';
  showToast('✅ GIF已加载 ('+(file.size/1024).toFixed(1)+'KB)');
}

function convertToMP4(){
  if(!gifFile){showToast('请先上传GIF');return}
  
  const fps=parseInt(document.getElementById('fps').value);
  const quality=parseFloat(document.getElementById('quality').value);
  const status=document.getElementById('mp4Result');
  status.style.display='block';
  document.getElementById('sizeCompare').textContent='⏳ 转换中...';
  
  // Canvas-based conversion: extract frames from GIF and create MP4-like webm
  const reader=new FileReader();
  reader.onload=function(e){
    const img=new Image();
    img.onload=function(){
      const canvas=document.createElement('canvas');
      canvas.width=img.width;canvas.height=img.height;
      const ctx=canvas.getContext('2d');
      ctx.drawImage(img,0,0);
      
      // Since browser can't read GIF frames easily, use MediaRecorder approach
      // Strategy: create a canvas animation from the GIF display, record with MediaRecorder
      const stream=canvas.captureStream(fps);
      const chunks=[];
      const recorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:Math.floor(quality*5000000)});
      
      recorder.ondataavailable=e=>{if(e.data.size>0)chunks.push(e.data)};
      recorder.onstop=()=>{
        mp4Blob=new Blob(chunks,{type:'video/webm'});
        const url=URL.createObjectURL(mp4Blob);
        const video=document.getElementById('mp4Video');
        video.src=url;
        video.style.display='block';
        
        const reduction=((1-mp4Blob.size/gifFile.size)*100).toFixed(0);
        document.getElementById('sizeCompare').innerHTML=
          `原始GIF: ${(gifFile.size/1024).toFixed(1)}KB → MP4: ${(mp4Blob.size/1024).toFixed(1)}KB `+
          `<span style="color:${reduction>0?'#4ade80':'#f87171'}">${reduction>0?'↓':'↑'}${Math.abs(reduction)}%</span>`;
        showToast('✅ 转换完成');
      };
      
      recorder.start();
      
      // Draw the GIF image repeatedly for a short duration to capture
      let frame=0;
      const maxFrames=fps*3; // record 3 seconds
      const drawInterval=setInterval(()=>{
        if(frame>=maxFrames){clearInterval(drawInterval);recorder.stop();return}
        // Re-read GIF each time (browser handles frame display internally)
        ctx.clearRect(0,0,canvas.width,canvas.height);
        const dataUrl=e.target.result;
        const frameImg=new Image();
        frameImg.onload=function(){ctx.drawImage(frameImg,0,0)};
        frameImg.src=dataUrl;
        frame++;
      },1000/fps);
    };
    img.src=e.target.result;
  };
  reader.readAsDataURL(gifFile);
}

function downloadMP4(){
  if(!mp4Blob){showToast('请先转换');return}
  const url=URL.createObjectURL(mp4Blob);
  const a=document.createElement('a');a.href=url;
  a.download=gifFile.name.replace(/\\.gif$/i,'.webm');
  a.click();URL.revokeObjectURL(url);
  showToast('✅ 已下载');
}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}'''
    },
    "latex-editor": {
        "cn": '''  <div class="input-section">
    <h2>📝 LaTeX编辑器</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">代码编辑</h3>
        <textarea id="latexInput" placeholder="输入LaTeX公式..." style="min-height:200px;font-family:monospace" oninput="renderLatex()">\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}</textarea>
      </div>
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">实时预览</h3>
        <div id="latexPreview" class="preview-box" style="min-height:200px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;overflow-x:auto"></div>
      </div>
    </div>
    
    <h3 style="font-size:.9rem;color:#94a3b8;margin-top:16px">📐 模板快速插入</h3>
    <div class="template-grid">
      <button class="template-btn" onclick="insertTemplate('frac')">分数 \\frac</button>
      <button class="template-btn" onclick="insertTemplate('sqrt')">根号 \\sqrt</button>
      <button class="template-btn" onclick="insertTemplate('sum')">求和 \\sum</button>
      <button class="template-btn" onclick="insertTemplate('int')">积分 \\int</button>
      <button class="template-btn" onclick="insertTemplate('matrix')">矩阵 \\begin{pmatrix}</button>
      <button class="template-btn" onclick="insertTemplate('lim')">极限 \\lim</button>
      <button class="template-btn" onclick="insertTemplate('alpha')">希腊字母 \\alpha</button>
      <button class="template-btn" onclick="insertTemplate('infty')">无穷 \\infty</button>
      <button class="template-btn" onclick="insertTemplate('cdot')">点乘 \\cdot</button>
      <button class="template-btn" onclick="insertTemplate('text')">文本 \\text</button>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="copyLatex()">📋 复制LaTeX代码</button>
      <button class="btn btn-secondary" onclick="exportSVG()">📐 导出SVG</button>
      <button class="btn btn-secondary" onclick="exportPNG()">🖼️ 导出PNG</button>
      <button class="btn btn-secondary" onclick="loadExample()">📖 加载示例</button>
    </div>
  </div>''',
        "en": '''  <div class="input-section">
    <h2>📝 LaTeX Editor</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">Code Editor</h3>
        <textarea id="latexInput" placeholder="Enter LaTeX formula..." style="min-height:200px;font-family:monospace" oninput="renderLatex()">\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}</textarea>
      </div>
      <div>
        <h3 style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">Live Preview</h3>
        <div id="latexPreview" class="preview-box" style="min-height:200px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;overflow-x:auto"></div>
      </div>
    </div>
    
    <h3 style="font-size:.9rem;color:#94a3b8;margin-top:16px">📐 Quick Templates</h3>
    <div class="template-grid">
      <button class="template-btn" onclick="insertTemplate('frac')">Fraction \\frac</button>
      <button class="template-btn" onclick="insertTemplate('sqrt')">Root \\sqrt</button>
      <button class="template-btn" onclick="insertTemplate('sum')">Sum \\sum</button>
      <button class="template-btn" onclick="insertTemplate('int')">Integral \\int</button>
      <button class="template-btn" onclick="insertTemplate('matrix')">Matrix \\begin{pmatrix}</button>
      <button class="template-btn" onclick="insertTemplate('lim')">Limit \\lim</button>
      <button class="template-btn" onclick="insertTemplate('alpha')">Greek \\alpha</button>
      <button class="template-btn" onclick="insertTemplate('infty')">Infinity \\infty</button>
      <button class="template-btn" onclick="insertTemplate('cdot')">Dot \\cdot</button>
      <button class="template-btn" onclick="insertTemplate('text')">Text \\text</button>
    </div>
    
    <div class="btn-row">
      <button class="btn btn-primary" onclick="copyLatex()">📋 Copy LaTeX</button>
      <button class="btn btn-secondary" onclick="exportSVG()">📐 Export SVG</button>
      <button class="btn btn-secondary" onclick="exportPNG()">🖼️ Export PNG</button>
      <button class="btn btn-secondary" onclick="loadExample()">📖 Load Example</button>
    </div>
  </div>''',
        "js": '''// Load MathJax dynamically
(function(){
  if(window.MathJax){renderLatex();return}
  const script=document.createElement('script');
  script.src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
  script.onload=function(){renderLatex()};
  document.head.appendChild(script);
})();

function renderLatex(){
  if(!window.MathJax)return;
  const input=document.getElementById('latexInput').value;
  const preview=document.getElementById('latexPreview');
  
  // Clear and set new content
  preview.innerHTML='\\\\['+input+'\\\\]';
  
  MathJax.typesetPromise([preview]).then(()=>{
    // MathJax renders SVG inline
  }).catch(()=>{
    preview.innerHTML='<span style="color:#f87171">LaTeX语法错误，请检查代码</span>';
  });
}

const templates={
  frac:'\\\\frac{}{}',
  sqrt:'\\\\sqrt{}',
  sum:'\\\\sum_{i=1}^{n}{}',
  int:'\\\\int_{a}^{b}{}',
  matrix:'\\\\begin{pmatrix}\\na & b \\\\\\\\nc & d\\n\\\\end{pmatrix}',
  lim:'\\\\lim_{x \\\\to \\\\infty}{}',
  alpha:'\\\\alpha \\\\beta \\\\gamma \\\\delta',
  infty:'\\\\infty',
  cdot:'\\\\cdot',
  text:'\\\\text{}'
};

function insertTemplate(name){
  const tmpl=templates[name]||'';
  const ta=document.getElementById('latexInput');
  const start=ta.selectionStart;
  const end=ta.selectionEnd;
  const text=ta.value;
  ta.value=text.substring(0,start)+tmpl+text.substring(end);
  ta.focus();
  ta.setSelectionRange(start+tmpl.length,start+tmpl.length);
  renderLatex();
}

function copyLatex(){
  const code=document.getElementById('latexInput').value;
  navigator.clipboard.writeText(code).then(()=>showToast('✅ 已复制'));
}

function exportSVG(){
  const preview=document.getElementById('latexPreview');
  const svg=preview.querySelector('svg');
  if(!svg){showToast('⚠️ 请先渲染公式');return}
  const svgData=new XMLSerializer().serializeToString(svg);
  const blob=new Blob([svgData],{type:'image/svg+xml'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='latex-formula.svg';a.click();
}

function exportPNG(){
  const preview=document.getElementById('latexPreview');
  const svg=preview.querySelector('svg');
  if(!svg){showToast('⚠️ 请先渲染公式');return}
  
  const svgData=new XMLSerializer().serializeToString(svg);
  const canvas=document.createElement('canvas');
  const bbox=svg.getBoundingClientRect();
  canvas.width=bbox.width*2;canvas.height=bbox.height*2;
  const ctx=canvas.getContext('2d');
  ctx.scale(2,2);
  
  const img=new Image();
  img.onload=function(){
    ctx.drawImage(img,0,0);
    canvas.toBlob(blob=>{
      const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='latex-formula.png';a.click();
    });
  };
  img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(svgData)));
}

function loadExample(){
  const examples=[
    '\\\\frac{-b \\\\pm \\\\sqrt{b^2-4ac}}{2a}',
    '\\\\sum_{n=1}^{\\\\infty} \\\\frac{1}{n^2} = \\\\frac{\\\\pi^2}{6}',
    '\\\\int_{0}^{\\\\infty} e^{-x^2} dx = \\\\frac{\\\\sqrt{\\\\pi}}{2}',
    '\\\\begin{pmatrix} a & b \\\\\\\\ c & d \\\\end{pmatrix}',
    'e^{i\\\\pi} + 1 = 0',
    '\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin x}{x} = 1'
  ];
  const random=examples[Math.floor(Math.random()*examples.length)];
  document.getElementById('latexInput').value=random;
  renderLatex();
  showToast('✅ 示例已加载');
}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}
setTimeout(renderLatex,1000);'''
    }
}

for tool_id, impl in tool_implementations.items():
    for lang, html_block in [("cn", impl["cn"]), ("en", impl["en"])]:
        if lang == "cn":
            path = os.path.join(BASE, tool_id, "index.html")
        else:
            path = os.path.join(BASE, "en", tool_id, "index.html")
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace placeholder
        placeholder = '<div id="tool-placeholder" style="background:#1e293b;border-radius:12px;padding:40px;text-align:center;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">\n    <p style="color:#64748b">'
        # Find the full placeholder
        start_idx = content.find('<div id="tool-placeholder"')
        end_idx = content.find('</div>\n\n  <div class="info-section">', start_idx)
        
        if start_idx >= 0 and end_idx >= 0:
            new_content = content[:start_idx] + html_block + '\n\n' + content[end_idx+6:]  # skip </div>
        else:
            print(f"WARNING: Could not find placeholder in {path}")
            continue
        
        # Inject JS before </body>
        new_content = new_content.replace('</body>', f'<script>\n{impl["js"]}\n</script>\n</body>')
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Injected tool code: {path}")

print("\nAll tool implementations injected!")