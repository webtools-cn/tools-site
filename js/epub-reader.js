// epub-reader.js - EPUB在线阅读器
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000);}

var currentBook=null;
var currentChapter=0;
var chapters=[];
var bookTitle="";

(function(){
  var uz=document.getElementById("uploadZone");
  var fi=document.getElementById("fileInput");
  uz.addEventListener("click",function(){fi.click()});
  uz.addEventListener("dragover",function(e){e.preventDefault();uz.classList.add("dragover")});
  uz.addEventListener("dragleave",function(){uz.classList.remove("dragover")});
  uz.addEventListener("drop",function(e){e.preventDefault();uz.classList.remove("dragover");handleFile(e.dataTransfer.files[0])});
  fi.addEventListener("change",function(){handleFile(this.files[0])});

  var s=document.getElementById("settings");
  s.innerHTML='<div class="form-row"><label>字体大小：</label><input type="range" id="fontSize" min="12" max="28" value="16" onchange="updateReaderStyle()"><span id="fontSizeVal">16px</span>'+
    '<label>主题：</label><select id="theme" onchange="updateReaderStyle()"><option value="light">浅色</option><option value="dark" selected>深色</option><option value="sepia">护眼</option></select></div>';
  s.style.display="block";

  // Save progress on scroll
  window.addEventListener("beforeunload",saveProgress);
})();

function handleFile(file){
  if(!file){return}
  if(!file.name.toLowerCase().endsWith(".epub")){showToast("请选择EPUB格式文件");return}
  if(file.size>100*1024*1024){showToast("文件过大，最大100MB");return}

  showToast("正在加载EPUB...");
  var reader=new FileReader();
  reader.onload=function(e){
    loadEpub(e.target.result,file.name);
  };
  reader.readAsArrayBuffer(file);
  document.getElementById("fileInput").value="";
}

function loadEpub(data,fileName){
  if(typeof JSZip==="undefined"){
    var script=document.createElement("script");
    script.src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
    script.onload=function(){parseEpub(data,fileName)};
    document.head.appendChild(script);
  }else{
    parseEpub(data,fileName);
  }
}

function parseEpub(data,fileName){
  JSZip.loadAsync(data).then(function(zip){
    // Find container.xml
    var containerFile=zip.file("META-INF/container.xml");
    if(!containerFile){showToast("无效的EPUB文件");return}
    return containerFile.async("string").then(function(containerXml){
      var parser=new DOMParser();
      var doc=parser.parseFromString(containerXml,"text/xml");
      var rootfile=doc.querySelector("rootfile");
      if(!rootfile){showToast("无法解析EPUB结构");return}
      var opfPath=rootfile.getAttribute("full-path");

      // Fix path - sometimes it's relative to the epub root
      return zip.file(opfPath).async("string").then(function(opfXml){
        var opfDoc=parser.parseFromString(opfXml,"text/xml");
        var titleEl=opfDoc.querySelector("title");
        bookTitle=titleEl?titleEl.textContent:fileName.replace(".epub","");

        // Get manifest items
        var manifest=opfDoc.querySelectorAll("item");
        var spine=opfDoc.querySelectorAll("itemref");
        var idToHref={};
        manifest.forEach(function(item){
          idToHref[item.getAttribute("id")]=item.getAttribute("href");
        });

        // Get base path
        var basePath=opfPath.substring(0,opfPath.lastIndexOf("/")+1);

        chapters=[];
        var chapterLoads=[];
        spine.forEach(function(ref,i){
          var id=ref.getAttribute("idref");
          var href=idToHref[id];
          if(href){
            var fullPath=basePath+href;
            chapters.push({id:id,href:fullPath,title:"Chapter "+(i+1),index:i});
            chapterLoads.push(
              zip.file(fullPath).async("string").then(function(html){
                chapters[i].html=html;
              }).catch(function(){
                chapters[i].html="<p>无法加载此章节</p>";
              })
            );
          }
        });

        return Promise.all(chapterLoads).then(function(){
          renderReader();
        });
      });
    });
  }).catch(function(e){
    console.error(e);
    showToast("EPUB解析失败: "+e.message);
  });
}

function renderReader(){
  var uz=document.getElementById("uploadZone");
  var results=document.getElementById("results");
  uz.style.display="none";
  document.getElementById("settings").style.display="block";

  // Build TOC
  var tocHtml='<div style="display:flex;gap:16px;flex-wrap:wrap"><div id="toc" style="flex:0 0 200px;max-height:70vh;overflow-y:auto;background:#0f172a;border-radius:8px;padding:12px;font-size:.85rem">';
  tocHtml+='<h3 style="color:#22d3ee;margin-bottom:8px">📑 目录</h3>';
  chapters.forEach(function(ch,i){
    tocHtml+='<div style="padding:6px 8px;cursor:pointer;color:#94a3b8;border-radius:4px;margin-bottom:2px" onmouseover="this.style.background=\'rgba(6,182,212,.1)\'" onmouseout="this.style.background=\'transparent\'" onclick="goToChapter('+i+')">'+(i+1)+'. '+ch.title+'</div>';
  });
  tocHtml+='</div>';
  tocHtml+='<div id="readerContent" style="flex:1;min-width:300px;padding:20px;background:#0f172a;border-radius:8px;max-height:70vh;overflow-y:auto;line-height:1.8" onscroll="saveProgress()"></div></div>';
  results.innerHTML=tocHtml;

  // Restore progress
  var saved=localStorage.getItem("epub_progress_"+bookTitle);
  if(saved){
    var progress=JSON.parse(saved);
    currentChapter=progress.chapter||0;
    document.getElementById("fontSize").value=progress.fontSize||16;
    document.getElementById("theme").value=progress.theme||"dark";
    document.getElementById("fontSizeVal").textContent=(progress.fontSize||16)+"px";
  }
  updateReaderStyle();
  goToChapter(currentChapter);
}

function goToChapter(idx){
  if(idx<0||idx>=chapters.length)return;
  currentChapter=idx;
  var content=document.getElementById("readerContent");
  if(!content)return;
  var ch=chapters[idx];

  // Parse and clean HTML
  var parser=new DOMParser();
  var doc=parser.parseFromString(ch.html||"","text/html");
  // Remove scripts and styles
  doc.querySelectorAll("script,style,link").forEach(function(el){el.remove()});
  var bodyContent=doc.body?doc.body.innerHTML:ch.html||"";

  content.innerHTML='<h2 style="color:#f1f5f9;margin-bottom:16px">'+ch.title+'</h2>'+bodyContent;
  content.scrollTop=0;

  // Highlight current in TOC
  var tocItems=document.querySelectorAll("#toc div");
  tocItems.forEach(function(item,i){item.style.color=i===idx?"#22d3ee":"#94a3b8"});
}

function updateReaderStyle(){
  var content=document.getElementById("readerContent");
  if(!content)return;
  var fontSize=document.getElementById("fontSize").value;
  var theme=document.getElementById("theme").value;
  document.getElementById("fontSizeVal").textContent=fontSize+"px";
  content.style.fontSize=fontSize+"px";

  var themes={
    light:{bg:"#f8fafc",color:"#0f172a"},
    dark:{bg:"#0f172a",color:"#e2e8f0"},
    sepia:{bg:"#f4ecd8",color:"#5b4636"}
  };
  var t=themes[theme]||themes.dark;
  content.style.background=t.bg;
  content.style.color=t.color;

  saveProgress();
}

function saveProgress(){
  if(!bookTitle)return;
  var content=document.getElementById("readerContent");
  var fontSize=document.getElementById("fontSize");
  var theme=document.getElementById("theme");
  var progress={
    chapter:currentChapter,
    scrollTop:content?content.scrollTop:0,
    fontSize:fontSize?parseInt(fontSize.value):16,
    theme:theme?theme.value:"dark",
    time:Date.now()
  };
  localStorage.setItem("epub_progress_"+bookTitle,JSON.stringify(progress));
}

// Empty stubs for unused functions
function downloadAll(){showToast("EPUB阅读器无需下载功能");}
function clearResults(){
  localStorage.removeItem("epub_progress_"+bookTitle);
  currentBook=null;chapters=[];bookTitle="";
  document.getElementById("results").innerHTML="";
  document.getElementById("uploadZone").style.display="block";
  document.getElementById("settings").style.display="none";
}