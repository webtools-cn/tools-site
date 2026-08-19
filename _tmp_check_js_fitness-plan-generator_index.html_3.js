
(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer=null;
function showToast(msg){var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.style.opacity='0';},2000);}
window.copyResults = copyResults; function copyResults(){
  var labels=document.querySelectorAll('.result-label');
  var text=[];
  labels.forEach(function(label){
    var valEl=label.nextElementSibling;
    if(valEl&&valEl.classList.contains('result-value')){
      text.push(label.textContent+': '+valEl.textContent);
    }
  });
  var details=document.querySelectorAll('.detail-row');
  details.forEach(function(row){
    var lbl=row.querySelector('.detail-label');
    var val=row.querySelector('.detail-value');
    if(lbl&&val)text.push(lbl.textContent+': '+val.textContent);
  });
  if(text.length>0){navigator.clipboard.writeText(text.join('\n')).then(function(){showToast('结果已复制 📋');});}
  else{showToast('没有可复制的结果');}
}

var TOOL_SLUG='fitness-plan-generator';
var LANG='zh-CN';

})();
