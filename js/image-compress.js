// image-compress.js - 图片压缩工具
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

  // Show quality settings
  var s=document.getElementById("settings");
  s.innerHTML='<div class="form-row"><label>压缩质量：</label><input type="range" id="quality" min="1" max="100" value="80" oninput="document.getElementById(\'qualityVal\').textContent=this.value+\'%\'"><span id="qualityVal">80%</span></div>'+
    '<div class="form-row"><label>输出格式：</label><select id="outputFmt"><option value="original">保持原格式</option><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>';
  s.style.display="block";
})();

function handleFiles(files){
  if(!files||files.length===0)return;
  var quality=parseInt(document.getElementById("quality").value)/100;
  var outputFmt=document.getElementById("outputFmt").value;
  var results=document.getElementById("results");
  for(var i=0;i<files.length;i++){
    (function(file){
      if(!file.type.match(/image\/(jpe?g|png|webp)/)){showToast(file.name+" 格式不支持，请选择JPG/PNG/WebP");return}
      if(file.size>50*1024*1024){showToast(file.name+" 文件过大(>50MB)");return}
      var reader=new FileReader();
      reader.onload=function(e){
        var img=new Image();
        img.onload=function(){
          var canvas=document.createElement("canvas");
          canvas.width=img.width;canvas.height=img.height;
          var ctx=canvas.getContext("2d");ctx.drawImage(img,0,0);
          var mimeType=outputFmt==="original"?file.type:outputFmt;
          canvas.toBlob(function(blob){
            var url=URL.createObjectURL(blob);
            var origSize=(file.size/1024).toFixed(1)+" KB";
            var newSize=(blob.size/1024).toFixed(1)+" KB";
            var saved=((1-blob.size/file.size)*100).toFixed(0);
            if(parseInt(saved)<0)saved="0";
            var idx=convertedFiles.length;
            var ext=mimeType.split("/")[1]||"png";
            convertedFiles.push({name:file.name.replace(/\.[^.]+$/,"")+"_compressed."+ext,blob:blob,url:url});
            var item=document.createElement("div");
            item.className="result-item";
            item.innerHTML='<img src="'+url+'" alt="preview"><div class="info"><div class="name">'+convertedFiles[idx].name+'</div><div class="size">原始: '+origSize+' → 压缩后: '+newSize+' (节省 '+saved+'%)</div></div><button class="btn btn-primary" onclick="downloadOne('+idx+')">📥 下载</button>';
            results.appendChild(item);
            if(convertedFiles.length>0)document.getElementById("batchActions").style.display="block";
          },mimeType,quality);
        };
        img.src=e.target.result;
      };
      reader.readAsDataURL(file);
    })(files[i]);
  }
  fi.value="";
  s.style.display="block";
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
