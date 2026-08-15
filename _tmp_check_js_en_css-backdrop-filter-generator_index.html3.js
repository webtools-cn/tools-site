
function toggleFeedback(){const p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}
function submitFeedback(){
const type=document.getElementById('feedback-type').value;
const typeLabel={feedback:'💡 Feature Request',bug:'🐛 Bug Report',other:'💬 Other'}[type];
const title=encodeURIComponent(typeLabel+' - '+window.location.pathname);
const body=encodeURIComponent('**Page**: '+window.location.href+'\n**Type**: '+typeLabel+'\n\n'+text);
window.open('https://github.com/webtools-cn/tools-site/issues/new?title='+title+'&body='+body,'_blank');
document.getElementById('feedback-success').style.display='block';
}
