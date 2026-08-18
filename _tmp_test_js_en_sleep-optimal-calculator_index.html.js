
(function(){
  var modeSwitch=document.getElementById('modeSwitch'),timeInput=document.getElementById('timeInput'),
      timeLabel=document.getElementById('timeLabel'),resultsEl=document.getElementById('results'),
      toast=document.getElementById('toast'),currentMode='wakeup';
  function showToast(msg){toast.textContent=msg;toast.classList.add('show');setTimeout(function(){toast.classList.remove('show')},2000)}
  function formatTime(h,m){return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')}
  function addMinutes(h,m,add){var total=h*60+m+add;return {h:Math.floor(((total%1440)+1440)%1440/60),m:((total%1440)+1440)%1440%60}}
  function calculate(){
    var p=timeInput.value.split(':'),h=parseInt(p[0]),m=parseInt(p[1]),opts=[];
    if(currentMode==='wakeup'){
      for(var i=6;i>=3;i--){var bt=addMinutes(h,m,-i*90-15);opts.push({rank:i,time:formatTime(bt.h,bt.m),info:i+' cycles ('+(i*1.5).toFixed(1)+'h)',best:i==5,label:i==5?'⭐ Best':''})}
      document.getElementById('resultTitle').textContent='🛏️ To wake up at '+timeInput.value+', go to bed at:';
    }else{
      for(var i=4;i<=6;i++){var wt=addMinutes(h,m,i*90+15);opts.push({rank:i,time:formatTime(wt.h,wt.m),info:i+' cycles ('+(i*1.5).toFixed(1)+'h)',best:i==5,label:i==5?'⭐ Best':''})}
      document.getElementById('resultTitle').textContent='⏰ If you sleep at '+timeInput.value+', wake up at:';
    }
    document.getElementById('sleepOptions').innerHTML=opts.map(function(o,i){return '<div class="sleep-option'+(o.best?' best':'')+'"><span class="rank">#'+(i+1)+'</span><span class="time">'+o.time+'</span><span class="info">'+o.info+'</span>'+(o.label?'<span class="badge-rec">'+o.label+'</span>':'')+'</div>'}).join('');
    resultsEl.style.display='block';resultsEl.scrollIntoView({behavior:'smooth'});
  }
  modeSwitch.addEventListener('click',function(e){
    if(e.target.tagName==='BUTTON'){
      var mode=e.target.dataset.mode;if(mode===currentMode)return;currentMode=mode;
      modeSwitch.querySelectorAll('button').forEach(function(b){b.classList.toggle('active',b.dataset.mode===mode)});
      timeLabel.textContent=mode==='wakeup'?'Wake-up time:':'Bedtime:';
      timeInput.value=mode==='wakeup'?'07:00':'23:00';
      if(resultsEl.style.display!=='none') calculate();
    }
  });
  document.getElementById('calcBtn').addEventListener('click',calculate);
  document.getElementById('nowBtn').addEventListener('click',function(){timeInput.value=formatTime(new Date().getHours(),new Date().getMinutes());showToast('Set to current time');calculate()});
  document.getElementById('copyBtn').addEventListener('click',function(){
    var lines=['Sleep Cycle Results:'];
    document.querySelectorAll('.sleep-option').forEach(function(e){lines.push(e.querySelector('.time').textContent+' - '+e.querySelector('.info').textContent+(e.classList.contains('best')?' ⭐':''))});
    navigator.clipboard.writeText(lines.join('\n')).then(function(){showToast('Copied')});
  });
  document.getElementById('shareBtn').addEventListener('click',function(){if(navigator.share)navigator.share({title:'Sleep Calculator',text:'My optimal sleep times',url:window.location.href});else showToast('Link copied')});
})();
