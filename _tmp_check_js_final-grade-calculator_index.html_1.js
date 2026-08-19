
function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)||isNaN(b)||(v3el&&isNaN(c))){show('请输入有效数值');return}
  if(c<=0||c>100){show("权重需在1-100之间");return}var need=(b-a*(1-c/100))/(c/100);var msg=need>100?"目标无法达成!":"需得 <b>"+need.toFixed(1)+"%</b>";document.getElementById("rv").innerHTML=msg+"<br>目标总成绩: <b>"+b+"%</b>"+(need<=100&&need>0?"<br>安全余量: <b>"+(100-need).toFixed(1)+"%</b>":"");document.getElementById("result").style.display="block"
}
function show(m){var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2500)}

function fillExample(){
  var vals = [["v1", "85"], ["v2", "90"], ["v3", "40"]];
  for(var i=0;i<vals.length;i++){
    var el = document.getElementById(vals[i][0]);
    if(el){el.value = vals[i][1];}
  }
  calc();
  var t=document.getElementById('toast');
  if(t){t.textContent='已填入示例并计算';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
}

function ftDrawChart(){
  var cv = document.getElementById('ftChart');
  if(!cv) return;
  var ctx = cv.getContext('2d');
  var nums = [];
  function pushNum(t){
    if(!t) return;
    var m = String(t).match(/[\d,]+(?:\.\d+)?/g);
    if(m){for(var i=0;i<m.length;i++){var v=parseFloat(m[i].replace(/,/g,''));if(v>0&&v<1e14)nums.push(v)}}
  }
  var scope = document.getElementById('result') || document;
  pushNum(scope.textContent);
  if(nums.length < 2) return;
  nums = Array.from(new Set(nums)).sort(function(a,b){return b-a}).slice(0,6);
  var W=cv.width,H=cv.height,padL=70,padR=10,padT=14,padB=26;
  ctx.clearRect(0,0,W,H);
  var maxV=Math.max.apply(null,nums);
  ctx.fillStyle='#94a3b8';ctx.font='10px sans-serif';ctx.textAlign='right';
  for(var g=0;g<=4;g++){
    var y=padT+(H-padT-padB)*g/4, val=maxV*(4-g)/4;
    ctx.strokeStyle='rgba(148,163,184,.12)';ctx.beginPath();ctx.moveTo(padL,y);ctx.lineTo(W-padR,y);ctx.stroke();
    var lab=val>=1e8?(val/1e8).toFixed(1)+'亿':val>=1e4?(val/1e4).toFixed(1)+'万':val.toFixed(0);
    ctx.fillText(lab,padL-6,y+3);
  }
  var bw=(W-padL-padR)/nums.length*0.55;
  var colors=['#06b6d4','#10b981','#8b5cf6','#f59e0b','#ef4444','#64748b'];
  ctx.textAlign='center';
  for(var i=0;i<nums.length;i++){
    var bh=(H-padT-padB)*nums[i]/maxV;
    var x=padL+(W-padL-padR)*(i+0.5)/nums.length;
    var y=padT+(H-padT-padB)-bh;
    ctx.fillStyle=colors[i%colors.length];
    ctx.fillRect(x-bw/2,y,bw,bh);
    ctx.fillStyle='#e2e8f0';ctx.fillText(ftFmt(nums[i]),x,y-4);
  }
}
function ftFmt(n){
  if(n>=1e8)return (n/1e8).toFixed(1)+'亿';
  if(n>=1e4)return (n/1e4).toFixed(1)+'万';
  return n.toFixed(0);
}
document.addEventListener('click',function(e){
  if(e.target&&e.target.closest&&e.target.closest('button')){setTimeout(ftDrawChart,180)}
});


document.addEventListener('click',function(e){
  if(e.target&&e.target.closest&&e.target.closest('button')){
    setTimeout(ftEnsureCopy,250);
  }
});
function ftEnsureCopy(){
  var res=document.getElementById('result');
  if(!res||res.offsetParent===null)return;
  if(res.querySelector('.ft-copy-btn'))return;
  var langEN=/^en/i.test((document.documentElement.getAttribute('lang')||'zh'));
  var btn=document.createElement('button');
  btn.className='btn btn-secondary ft-copy-btn';
  btn.textContent=langEN?'📋 Copy Result':'📋 复制结果';
  btn.style.cssText='margin-top:12px;display:block';
  btn.onclick=function(){
    var txt=(res.innerText||res.textContent||'').replace(/\s+/g,' ').trim();
    function toast(m){
      var t=document.getElementById('toast');
      if(t){t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
    }
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){toast(langEN?'Copied!':'已复制')}).catch(function(){ftFallbackCopy(txt);toast(langEN?'Copied!':'已复制')});
    }else{ftFallbackCopy(txt);toast(langEN?'Copied!':'已复制')}
  };
  res.appendChild(btn);
}
function ftFallbackCopy(txt){
  var ta=document.createElement('textarea');
  ta.value=txt;ta.style.position='fixed';ta.style.opacity='0';
  document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy')}catch(err){}
  document.body.removeChild(ta);
}

