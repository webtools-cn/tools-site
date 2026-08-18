
function showToast(msg){
  var t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(function(){t.classList.remove('show');},1500);
}

function smartQuotes(text, mode){
  if(mode==='auto'){
    var hasCJK=/[\u4e00-\u9fff]/.test(text);
    mode=hasCJK?'cn':'en';
  }
  var result=text;
  if(mode==='cn'){
    var dqOpen=true;
    result=result.replace(/"/g,function(){var r=dqOpen?'\u201c':'\u201d';dqOpen=!dqOpen;return r;});
    var sqOpen=true;
    result=result.replace(/'/g,function(){var r=sqOpen?'\u2018':'\u2019';sqOpen=!sqOpen;return r;});
    result=result.replace(/<</g,'\u300a').replace(/>>/g,'\u300b');
  }else{
    var dqOpen=true;
    result=result.replace(/"/g,function(){var r=dqOpen?'\u201c':'\u201d';dqOpen=!dqOpen;return r;});
    var sqOpen=true;
    result=result.replace(/'/g,function(){var r=sqOpen?'\u2018':'\u2019';sqOpen=!sqOpen;return r;});
  }
  return result;
}

function revertQuotes(text){
  return text.replace(/[\u201c\u201d]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u300a]/g,'<<').replace(/[\u300b]/g,'>>');
}

document.getElementById('convertBtn').addEventListener('click',function(){
  var input=document.getElementById('inputText').value;
  var mode=document.querySelector('input[name="mode"]:checked').value;
  var result=smartQuotes(input,mode);
  document.getElementById('outputBox').textContent=result;
  showToast('Converted!');
});

document.getElementById('revertBtn').addEventListener('click',function(){
  var input=document.getElementById('inputText').value;
  var result=revertQuotes(input);
  document.getElementById('outputBox').textContent=result;
  showToast('Reverted to straight quotes');
});

document.getElementById('copyBtn').addEventListener('click',function(){
  var text=document.getElementById('outputBox').textContent;
  if(!text){showToast('Nothing to copy');return;}
  navigator.clipboard.writeText(text).then(function(){showToast('Copied to clipboard');});
});

document.getElementById('clearBtn').addEventListener('click',function(){
  document.getElementById('inputText').value='';
  document.getElementById('outputBox').textContent='';
});

document.getElementById('inputText').addEventListener('input',function(){
  var mode=document.querySelector('input[name="mode"]:checked').value;
  var result=smartQuotes(this.value,mode);
  document.getElementById('outputBox').textContent=result;
});
