
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
function copyText(id){var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){showToast("Copied to clipboard")})["catch"](function(){showToast("Copy failed")})}
function downloadText(filename,text){var b=new Blob([text],{type:'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=filename;a.click();URL.revokeObjectURL(a.href)}
document.addEventListener('keydown',function(e){if(e.ctrlKey&&e.key==='Enter'){execute();e.preventDefault()}if(e.ctrlKey&&e.shiftKey&&e.key==='C'){copyText('output');e.preventDefault()}if(e.ctrlKey&&e.shiftKey&&e.key==='X'){clearInput();e.preventDefault()}});
function saveHistory(key,val){var h=JSON.parse(localStorage.getItem(key)||'[]');h=h.filter(function(x){return x!==val});h.unshift(val);if(h.length>5)h=h.slice(0,5);localStorage.setItem(key,JSON.stringify(h))}
function loadHistory(key){return JSON.parse(localStorage.getItem(key)||'[]')}
