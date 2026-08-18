
(function(){
var el=function(id){return document.getElementById(id);};
var toastTimer;
var timerInterval;

function showToast(msg){
var t=el('toast');
t.textContent=msg;t.classList.add('show');
clearTimeout(toastTimer);
toastTimer=setTimeout(function(){t.classList.remove('show');},2000);
}

function loadState(){
try{
var s=JSON.parse(localStorage.getItem('sobriety_tracker'));
if(s&&s.startDate){
el('habitName').value=s.habitName||'';
el('startDate').value=s.startDate;
el('setupSection').style.display='none';
el('trackerSection').style.display='block';
el('resetBtn').style.display='inline-block';
el('startBtn').style.display='none';
el('habitTitle').textContent=(s.habitName||'Habit')+' - Days Sober';
updateCounter();
}
}catch(e){}
}

function updateCounter(){
try{
var s=JSON.parse(localStorage.getItem('sobriety_tracker'));
if(!s||!s.startDate)return;
var start=new Date(s.startDate+'T00:00:00');
var now=new Date();
var diffMs=now-start;
if(diffMs<0){diffMs=0;}
var totalDays=Math.floor(diffMs/(1000*60*60*24));
var totalHours=Math.floor(diffMs/(1000*60*60));
var totalMinutes=Math.floor(diffMs/(1000*60));
el('daysCount').textContent=totalDays;
el('timeDetail').textContent='That\'s '+totalHours+' hours / '+totalMinutes+' minutes';

var milestones=[1,7,30,90,180,365,500,1000];
var html='';
milestones.forEach(function(m){
var cls=totalDays>=m?'achieved':'';
html+='<div class="milestone '+cls+'"><div class="milestone-days">'+m+'</div>days</div>';
});
el('milestones').innerHTML=html;
}catch(e){}
}

el('startBtn').addEventListener('click',function(){
var name=el('habitName').value.trim()||'Sobriety';
var date=el('startDate').value;
if(!date){showToast('Please select a start date');return;}
var state={habitName:name,startDate:date};
localStorage.setItem('sobriety_tracker',JSON.stringify(state));
el('setupSection').style.display='none';
el('trackerSection').style.display='block';
el('resetBtn').style.display='inline-block';
el('startBtn').style.display='none';
el('habitTitle').textContent=name+' - Days Sober';
updateCounter();
showToast('Tracking started! You got this 💪');
});

el('resetBtn').addEventListener('click',function(){
if(confirm('Are you sure you want to start over? Your current progress will be lost.')){
localStorage.removeItem('sobriety_tracker');
el('setupSection').style.display='block';
el('trackerSection').style.display='none';
el('resetBtn').style.display='none';
el('startBtn').style.display='inline-block';
el('habitName').value='';
el('startDate').value='';
clearInterval(timerInterval);
showToast('Reset complete');
}
});

el('copyBtn').addEventListener('click',function(){
var days=el('daysCount').textContent;
var name=el('habitTitle').textContent.replace(' - Days Sober','');
var text='🎯 '+name+': '+days+' days sober!\n— via Free ToolBase Sobriety Tracker';
if(navigator.clipboard){
navigator.clipboard.writeText(text).then(function(){showToast('Copied to clipboard');});
}else{
var ta=document.createElement('textarea');
ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
document.body.appendChild(ta);ta.select();
document.execCommand('copy');document.body.removeChild(ta);
showToast('Copied to clipboard');
}
});

loadState();
timerInterval=setInterval(updateCounter,60000);
})();
