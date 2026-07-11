// image-resize.js - 图片尺寸调整工具
var convertedFiles=[];
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000);}

(function(){
  var uz=document.getElementById("uploadZone");
  var fi=document.getElementById("fileInput");
  uz.addEventListener("click",function(){fi.click()});
  uz.addEventListener("dragover",function(e){e.preventDefault();uz.classList.add("dragover")});
  uz.addEventListener("dragleave",function(){uz.classList.remove("dragover")});
  uz.addEventListener("drop",function(e){e.preventDefault();uz.classList.remove("dragover");handleFiles(e.dataTransfer.files)});
  fi.addEventListener("change",function(){handleFiles(this.files)});

  var s=document.getElementById("settings");
  s.innerHTML='<div class="form-row"><label>调整模式：</label><select id="resizeMode" onchange="toggleResizeMode()"><option value="pixels">按像素</option><option value="percent">按百分比</option><option value="preset">预设尺寸</option></select></div>'+
    '<div id="pixelInputs"><div class="form-row"><label>宽度(px)：</label><input type="number" id="targetWidth" value="800" min="1" max="8192" onchange="updatePreview()">'+
    '<label>高度(px)：</label><input type="number" id="targetHeight" value="600" min="1" max="8192" onchange="updatePreview()">'+
    '<label style="display:inline-flex;align-items:center;gap:4px"><input type="checkbox" id="keepRatio" checked onchange="updatePreview()"> 保持比例</label></div></div>'+
    '<div id="percentInputs" style="display:none"><div class="form-row"><label>缩放比例：</label><input type="range" id="percentSlider" min="10" max="300" value="50" oninput="document.getElementById(\'percentVal\').textContent=this.value+\'%\'"><span id="percentVal">50%</span></div></div>'+
    '<div id="presetInputs" style="display:none"><div class="form-row"><label>预设：</label><select id="preset" onchange="applyPreset()">'+
    '<option value="">自定义...</option><option value="1920,1080">全高清 1920x1080</option><option value="1280,720">HD 1280x720</option><option value="800,600">SVGA 800x600</option><option value="500,500">Instagram 方形 500x500</option><option value="1080,1080">Instagram 高清 1080x1080</option><option value="1200,630">社交媒体分享图 1200x630</option><option value="300,250">广告横幅 300x250</option><option value="1200,628">Facebook链接图 1200x628</option></select></div></div>'+
    '<div class="form-row"><label>输出格式：</label><select id="outputFmt"><option value="original">保持原格式</option><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>';
  s.style.display="block";
})();

function toggleResizeMode(){
  var mode=document.getElementById("resizeMode").value;
  document.getElementById("pixelInputs").style.display=mode==="pixels"?"block":"none";
  document.getElementById("percentInputs").style.display=mode==="percent"?"block":"none";
  document.getElementById("presetInputs").style.display=mode==="preset"?"block":"none";
}

function applyPreset(){
  var val=document.getElementById("preset").value;
  if(val){
    var parts=val.split(",");
    document.getElementById("targetWidth").value=parts[0];
    document.getElementById("targetHeight").value=parts[1];
  }
}

function handleFiles(files){
  if(!files||files.length===0)return;
  for(var i=0;i<files.length;i++){
    (function(file){
      if(!file.type.match(/image\/(jpe?g|png|webp)/)){showToast(file.name+" 格式不支持，请选择PNG/JPG/WebP");return}
      if(file.size>50*1024*1024){showToast(file.name+" 文件过大(>50MB)");return}
      var reader=new FileReader();
      reader.onload=function(e){
        var img=new Image();
        img.onload=function(){
          resizeImage(img,file);
        };
        img.src=e.target.result;
      };
      reader.readAsDataURL(file);
    })(files[i]);
  }
  document.getElementById("fileInput").value="";
}

function resizeImage(img,file){
  var mode=document.getElementById("resizeMode").value;
  var newW,newH;
  var keepRatio=document.getElementById("keepRatio").checked;

  if(mode==="percent"){
    var pct=parseInt(document.getElementById("percentSlider").value)/100;
    newW=Math.round(img.width*pct);
    newH=Math.round(img.height*pct);
  }else if(mode==="preset"){
    newW=parseInt(document.getElementById("targetWidth").value);
    newH=parseInt(document.getElementById("targetHeight").value);
  }else{
    newW=parseInt(document.getElementById("targetWidth").value);
    newH=parseInt(document.getElementById("targetHeight").value);
  }

  if(keepRatio&&mode!=="preset"){
    var ratio=img.width/img.height;
    if(newW/newH>ratio){newW=Math.round(newH*ratio)}
    else{newH=Math.round(newW/ratio)}
  }

  newW=Math.max(1,Math.min(8192,newW||img.width));
  newH=Math.max(1,Math.min(8192,newH||img.height));

  var canvas=document.createElement("canvas");
  canvas.width=newW;canvas.height=newH;
  var ctx=canvas.getContext("2d");
  ctx.imageSmoothingEnabled=true;
  ctx.imageSmoothingQuality="high";
  ctx.drawImage(img,0,0,newW,newH);

  var outputFmt=document.getElementById("outputFmt").value;
  var mimeType=outputFmt==="original"?file.type:outputFmt;
  canvas.toBlob(function(blob){
    var url=URL.createObjectURL(blob);
    var idx=convertedFiles.length;
    var ext=mimeType.split("/")[1]||"png";
    var newName=file.name.replace(/\.[^.]+$/,"")+"_"+newW+"x"+newH+"."+ext;
    convertedFiles.push({name:newName,blob:blob,url:url});
    var origSize=img.width+"x"+img.height;
    var newSize=newW+"x"+newH;
    var results=document.getElementById("results");
    var item=document.createElement("div");
    item.className="result-item";
    item.innerHTML='<img src="'+url+'" alt="preview"><div class="info"><div class="name">'+newName+'</div><div class="size">原始: '+origSize+' → 调整后: '+newSize+'</div></div><button class="btn btn-primary" onclick="downloadOne('+idx+')">📥 下载</button>';
    results.appendChild(item);
    if(convertedFiles.length>0)document.getElementById("batchActions").style.display="block";
  },mimeType,0.92);
}

function downloadOne(idx){
  var f=convertedFiles[idx];
  var a=document.createElement("a");a.href=f.url;a.download=f.name;a.click();
}
function downloadAll(){
  for(var i=0;i<convertedFiles.length;i++){
    setTimeout(function(idx){var f=convertedFiles[idx];var a=document.createElement("a");a.href=f.url;a.download=f.name;a.click()},i*200,i);
  }
  showToast("正在批量下载 "+convertedFiles.length+" 个文件...");
}
function clearResults(){
  convertedFiles.forEach(function(f){URL.revokeObjectURL(f.url)});
  convertedFiles=[];document.getElementById("results").innerHTML="";document.getElementById("batchActions").style.display="none";
}