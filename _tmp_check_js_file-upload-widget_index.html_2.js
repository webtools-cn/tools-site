
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2000);}
function copyText(text){navigator.clipboard.writeText(text).then(function(){showToast('已复制到剪贴板');}).catch(function(){showToast('复制失败');});}
