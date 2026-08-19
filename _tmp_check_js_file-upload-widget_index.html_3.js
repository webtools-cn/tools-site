
document.getElementById('dropZone').addEventListener('click',function(){document.getElementById('fileInput').click();});
function handleDrop(e){e.preventDefault();e.target.style.borderColor='var(--border)';e.target.style.background='transparent';handleFiles(e.dataTransfer.files);}
var files=[];
window.handleFiles = handleFiles; function handleFiles(fileList){
var allowed=document.getElementById('allowedTypes').value.toLowerCase().split(',').map(function(s){return s.trim();}).filter(Boolean);
for(var i=0;i<fileList.length;i++){
var f=fileList[i];
if(allowed.length>0){var ext='.'+f.name.split('.').pop().toLowerCase();if(allowed.indexOf(ext)===-1){showToast("跳过不支持的文件: "+f.name);continue;}}
files.push(f);
}
renderFileList();
}
function renderFileList(){
var html='';var totalSize=0;
files.forEach(function(f,i){
totalSize+=f.size;
var size=f.size<1024?f.size+' B':f.size<1048576?(f.size/1024).toFixed(1)+' KB':(f.size/1048576).toFixed(1)+' MB';
var isImg=/\.(jpg|jpeg|png|gif|webp|svg)$/i.test(f.name);
html+='<div class="result-item" style="background:#0f172a;border:1px solid var(--border);border-radius:8px;padding:12px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:10px">';
html+='<div style="display:flex;align-items:center;gap:10px;flex:1;min-width:0"><span style="font-size:1.5rem">'+(isImg?'🖼️':'📄')+'</span>';
html+='<div style="min-width:0"><div style="color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+f.name+'</div>';
html+='<div style="color:var(--text-secondary);font-size:.8rem">'+size+' | '+f.type+'</div></div></div>';
html+='<button class="btn-secondary" style="padding:4px 10px;font-size:.8rem" onclick="removeFile('+i+')">✕</button>';
html+='</div>';
});
if(files.length>0){var ts=totalSize<1024?totalSize+' B':totalSize<1048576?(totalSize/1024).toFixed(1)+' KB':(totalSize/1048576).toFixed(1)+' MB';html+='<div style="color:var(--text-secondary);font-size:.85rem;margin-top:8px">共 '+files.length+' 个文件，'+ts+'</div>';}
document.getElementById('fileList').innerHTML=html||('<div class="output-area" style="color:var(--text-secondary)">暂无文件</div>');
}
function removeFile(i){files.splice(i,1);renderFileList();}
function clearFiles(){files=[];renderFileList();document.getElementById('fileInput').value='';showToast("已清空");}

/* Thin-tool enhancement v1 (fillExample + ftChart + ftEnsureCopy) */
(function(){
  var langEN=/^en/i.test((document.documentElement.getAttribute('lang')||'zh'));
  var isZh=!langEN;
  function toast(msg){var t=document.getElementById('toast')||document.getElementById('copy-toast');if(!t)return;t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2200);}
  function fallbackCopy(text){var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');toast(isZh?'已复制':'Copied');}catch(e){toast(isZh?'复制失败':'Copy failed');}document.body.removeChild(ta);}
  window.ftEnsureCopy=function(){
    var res=document.getElementById('result')||document.getElementById('output')||document.getElementById('result-text');
    if(!res||res.offsetParent===null)return;
    if(res.querySelector('.ft-copy-btn'))return;
    var btn=document.createElement('button');
    btn.className='btn btn-secondary ft-copy-btn';
    btn.textContent=isZh?'📋 复制结果':'📋 Copy Result';
    btn.style.cssText='margin-top:10px;width:100%';
    btn.onclick=function(){
      var txt=(res.innerText||res.textContent||'').trim();
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt).then(function(){toast(isZh?'已复制':'Copied');})['catch'](function(){fallbackCopy(txt);});
      }else{fallbackCopy(txt);}
    };
    res.appendChild(btn);
  };
  function pushNum(t,arr){var m=t.match(/[\d][\d,]*(?:\.[\d]+)?/g);if(!m)return;m.forEach(function(x){var n=parseFloat(x.replace(/,/g,''));if(!isNaN(n)&&n>0)arr.push(n);});}
  window.ftDrawChart=function(){
    var existing=document.getElementById('ftChart');
    if(existing&&existing.parentNode){existing.parentNode.removeChild(existing);}
    var res=document.getElementById('result')||document.getElementById('output');
    if(!res||res.offsetParent===null)return;
    var nums=[];pushNum(res.textContent,nums);
    if(nums.length<2)return;
    var wrap=res.parentNode;
    if(!wrap)return;
    var cv=document.createElement('canvas');
    cv.id='ftChart';cv.style.cssText='width:100%;max-width:480px;margin-top:14px;background:#1e293b;border-radius:10px';
    wrap.appendChild(cv);
    var ctx=cv.getContext('2d');
    var W=cv.width=480,H=cv.height=200;
    ctx.fillStyle='#1e293b';ctx.fillRect(0,0,W,H);
    var max=Math.max.apply(null,nums);
    var barW=Math.max(14,W/nums.length-10);
    var colors=['#06b6d4','#10b981','#f59e0b','#8b5cf6','#ef4444','#22d3ee'];
    nums.slice(0,12).forEach(function(n,i){
      var bh=Math.max(4,(n/max)*(H-40));
      ctx.fillStyle=colors[i%colors.length];
      ctx.fillRect(i*(barW+10)+10,H-30-bh,barW,bh);
      ctx.fillStyle='#94a3b8';ctx.font='11px sans-serif';
      var label=n>=1e6?(n/1e6).toFixed(1)+'M':n>=1e4?(n/1e4).toFixed(1)+'w':n.toFixed(n%1===0?0:1);
      ctx.fillText(label,i*(barW+10)+10,H-18);
    });
    ctx.strokeStyle='rgba(148,163,184,.2)';ctx.beginPath();ctx.moveTo(10,H-30);ctx.lineTo(W-10,H-30);ctx.stroke();
  };
  window.ftFillExample=function(){
    var pairs=[];
    var phs=document.querySelectorAll('input[placeholder]');
    phs.forEach(function(inp){
      var m=(inp.getAttribute('placeholder')||'').match(/([\d]+(?:\.\d+)?)/);
      if(m&&m[1]){pairs.push([inp.id||inp.name,m[1]]);}
    });
    if(!pairs.length)return;
    pairs.forEach(function(pair){
      var el=document.getElementById(pair[0]);
      if(el){el.value=pair[1];el.dispatchEvent(new Event('input',{bubbles:true}));}
    });
    toast(isZh?'已填入示例':'Example filled');
    var btn=document.querySelector('button[onclick]')||document.querySelector('.btn-primary');
    if(btn){try{if(btn.onclick)btn.onclick();}catch(e){}}
  };
  document.addEventListener('click',function(e){
    if(e.target&&e.target.closest&&e.target.closest('button')){
      setTimeout(function(){ftEnsureCopy();ftDrawChart();},280);
    }
  });
  /* 示例按钮 */
  var phs2=document.querySelectorAll('input[placeholder]');
  var hasNumPh=Array.prototype.some.call(phs2,function(i){return /[\d]/.test(i.getAttribute('placeholder')||'');});
  if(hasNumPh&&!document.getElementById('ftFillBtn')){
    var calcBtn=document.querySelector('button[onclick]')||document.querySelector('.btn-primary');
    if(calcBtn){
      var fb=document.createElement('button');
      fb.id='ftFillBtn';
      fb.className='btn btn-secondary';
      fb.textContent=isZh?'🎲 填入示例':'🎲 Try example';
      fb.style.cssText='margin-left:8px';
      fb.onclick=function(){ftFillExample();};
      calcBtn.parentNode.insertBefore(fb,calcBtn.nextSibling);
    }
  }
})();
