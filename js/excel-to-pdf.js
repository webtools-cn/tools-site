// excel-to-pdf.js - Excel转PDF工具
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
  s.innerHTML='<div class="form-row"><label>纸张大小：</label><select id="paperSize"><option value="a4">A4</option><option value="letter">Letter</option><option value="legal">Legal</option></select>'+
    '<label>方向：</label><select id="orientation"><option value="portrait">纵向</option><option value="landscape">横向</option></select></div>';
  s.style.display="block";
})();

// Dynamic load jsPDF
function loadScript(src,cb){
  var s=document.createElement("script");s.src=src;s.onload=cb;document.head.appendChild(s);
}

function handleFiles(files){
  if(!files||files.length===0)return;
  for(var i=0;i<files.length;i++){
    (function(file){
      var ext=file.name.split(".").pop().toLowerCase();
      if(!["xls","xlsx"].includes(ext)){showToast(file.name+" 不是Excel文件，请选择XLS/XLSX");return}
      if(file.size>20*1024*1024){showToast(file.name+" 文件过大(>20MB)");return}
      var reader=new FileReader();
      reader.onload=function(e){
        var data=new Uint8Array(e.target.result);
        // Load SheetJS + jsPDF
        if(typeof XLSX==="undefined"){
          loadScript("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",function(){
            processExcel(data,file.name);
          });
        }else{
          processExcel(data,file.name);
        }
      };
      reader.readAsArrayBuffer(file);
    })(files[i]);
  }
  document.getElementById("fileInput").value="";
}

function processExcel(data,fileName){
  var wb=XLSX.read(data,{type:"array"});
  var sheetName=wb.SheetNames[0];
  var ws=wb.Sheets[sheetName];
  var html=XLSX.utils.sheet_to_html(ws,{id:"xlsTable"});

  // Create a hidden div to render
  var div=document.createElement("div");
  div.innerHTML=html;
  div.style.position="absolute";div.style.left="-9999px";
  document.body.appendChild(div);

  if(typeof window.jspdf==="undefined"){
    loadScript("https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",function(){
      doConvert(div,fileName);
    });
  }else{
    doConvert(div,fileName);
  }
}

function doConvert(div,fileName){
  var orientation=document.getElementById("orientation").value;
  var paperSize=document.getElementById("paperSize").value;
  var {jsPDF}=window.jspdf;
  var doc=new jsPDF(orientation,"mm",paperSize);

  doc.html(div,{
    callback:function(pdf){
      var pdfBlob=pdf.output("blob");
      var url=URL.createObjectURL(pdfBlob);
      var idx=convertedFiles.length;
      var pdfName=fileName.replace(/\.(xlsx?)$/i,"")+".pdf";
      convertedFiles.push({name:pdfName,blob:pdfBlob,url:url});
      var results=document.getElementById("results");
      var item=document.createElement("div");
      item.className="result-item";
      item.innerHTML='<div style="font-size:2rem">📄</div><div class="info"><div class="name">'+pdfName+'</div><div class="size">转换完成</div></div><button class="btn btn-primary" onclick="downloadOne('+idx+')">📥 下载PDF</button>';
      results.appendChild(item);
      if(convertedFiles.length>0)document.getElementById("batchActions").style.display="block";
      document.body.removeChild(div);
    },
    margin:[10,10,10,10],
    autoPaging:"text",
    width:doc.internal.pageSize.getWidth()-20
  });
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