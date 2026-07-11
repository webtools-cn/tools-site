// ico-converter.js - ICO图标转换器
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
  s.innerHTML='<div class="form-row"><label>图标尺寸：</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="16" checked onchange="updateSizes()"> 16x16</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="32" checked onchange="updateSizes()"> 32x32</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="48" checked onchange="updateSizes()"> 48x48</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="64" onchange="updateSizes()"> 64x64</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="128" onchange="updateSizes()"> 128x128</label>'+
    '<label style="display:inline-flex;align-items:center;gap:4px;margin-right:8px"><input type="checkbox" value="256" onchange="updateSizes()"> 256x256</label>'+
    '</div>'+
    '<div class="form-row"><span id="sizeHint" style="color:#64748b;font-size:.8rem">已选: 16, 32, 48</span></div>';
  s.style.display="block";
})();

function updateSizes(){
  var checks=document.querySelectorAll('#settings input[type="checkbox"]:checked');
  var sizes=Array.from(checks).map(function(c){return parseInt(c.value)});
  document.getElementById("sizeHint").textContent="已选: "+sizes.join(", ");
  if(sizes.length===0){document.getElementById("sizeHint").textContent="请至少选择一个尺寸";}
}

function getSelectedSizes(){
  var checks=document.querySelectorAll('#settings input[type="checkbox"]:checked');
  return Array.from(checks).map(function(c){return parseInt(c.value)});
}

function handleFiles(files){
  if(!files||files.length===0)return;
  for(var i=0;i<files.length;i++){
    (function(file){
      if(!file.type.match(/image\/(jpe?g|png|webp)/)){showToast(file.name+" 格式不支持");return}
      if(file.size>20*1024*1024){showToast(file.name+" 文件过大");return}
      var reader=new FileReader();
      reader.onload=function(e){
        var img=new Image();
        img.onload=function(){
          var sizes=getSelectedSizes();
          if(sizes.length===0){showToast("请至少选择一个尺寸");return}
          createICO(img,sizes,file.name);
        };
        img.src=e.target.result;
      };
      reader.readAsDataURL(file);
    })(files[i]);
  }
  document.getElementById("fileInput").value="";
}

function createICO(img,sizes,fileName){
  // Generate ICO file (multi-size)
  var icoData=[];

  // ICO header: 6 bytes
  var header=new ArrayBuffer(6);
  var dv=new DataView(header);
  dv.setUint16(0,0,true); // Reserved
  dv.setUint16(2,1,true); // Type: ICO
  dv.setUint16(4,sizes.length,true); // Count
  icoData.push(new Uint8Array(header));

  var imageDataArr=[];
  var offset=6+sizes.length*16; // header + directory entries

  sizes.forEach(function(size){
    var canvas=document.createElement("canvas");
    canvas.width=size;canvas.height=size;
    var ctx=canvas.getContext("2d");
    // Clear with transparent
    ctx.clearRect(0,0,size,size);
    ctx.drawImage(img,0,0,size,size);

    // Get PNG data (modern ICO uses PNG for >256 colors)
    var pngDataUrl=canvas.toDataURL("image/png");
    // Decode base64
    var base64=pngDataUrl.split(",")[1];
    var raw=atob(base64);
    var pngBytes=new Uint8Array(raw.length);
    for(var i=0;i<raw.length;i++){pngBytes[i]=raw.charCodeAt(i);}

    // Directory entry: 16 bytes
    var dir=new ArrayBuffer(16);
    var dd=new DataView(dir);
    dd.setUint8(0,size>=256?0:size); // Width (0 means 256)
    dd.setUint8(1,size>=256?0:size); // Height
    dd.setUint8(2,0); // Color palette
    dd.setUint8(3,0); // Reserved
    dd.setUint16(4,1,true); // Color planes
    dd.setUint16(6,32,true); // Bits per pixel
    dd.setUint32(8,pngBytes.length,true); // Image size
    dd.setUint32(12,offset,true); // Image offset
    icoData.push(new Uint8Array(dir));

    imageDataArr.push({bytes:pngBytes,dv:dd});
    offset+=pngBytes.length;
  });

  // Build final ICO
  var totalLen=offset;
  var ico=new Uint8Array(totalLen);
  var pos=0;
  icoData.forEach(function(chunk){ico.set(chunk,pos);pos+=chunk.length});
  imageDataArr.forEach(function(item){ico.set(item.bytes,item.dv.getUint32(12,true))});

  var blob=new Blob([ico],{type:"image/x-icon"});
  var url=URL.createObjectURL(blob);
  var idx=convertedFiles.length;
  var icoName=fileName.replace(/\.[^.]+$/,"")+".ico";
  convertedFiles.push({name:icoName,blob:blob,url:url});

  var results=document.getElementById("results");
  var item=document.createElement("div");
  item.className="result-item";
  item.innerHTML='<div style="font-size:2rem">🖼️</div><div class="info"><div class="name">'+icoName+'</div><div class="size">尺寸: '+sizes.map(function(s){return s+"x"+s}).join(", ")+'</div></div><button class="btn btn-primary" onclick="downloadOne('+idx+')">📥 下载ICO</button>';
  results.appendChild(item);
  if(convertedFiles.length>0)document.getElementById("batchActions").style.display="block";
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