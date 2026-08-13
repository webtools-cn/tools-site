
const toast = s => {const e = document.getElementById('toast'); e.textContent = s; e.classList.add('show'); setTimeout(() => e.classList.remove('show'), 2000); };
const copy = s => { navigator.clipboard.writeText(s).then(() => toast('Copied!')).catch(() => toast('Copy failed')); };

let selectedFile = null;

const dz = document.getElementById('dropZone');
const fi = document.getElementById('fileInput');

dz.addEventListener('click', () => fi.click());
dz.addEventListener('dragover', e => { e.preventDefault(); dz.style.borderColor = '#22d3ee'; });
dz.addEventListener('dragleave', () => { dz.style.borderColor = 'rgba(148,163,184,.1)'; });
dz.addEventListener('drop', e => { e.preventDefault(); dz.style.borderColor = 'rgba(148,163,184,.1)'; if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]); });
fi.addEventListener('change', () => {if (fi.files.length > 0) handleFile(fi.files[0]); });

function handleFile(f) {
    selectedFile = f;
    document.getElementById('fileName').textContent = f.name + ' (' + (f.size / 1024).toFixed(1) + ' KB)';
}

async function calcHash(algo) {if (!selectedFile) return '';
    const buf = await selectedFile.arrayBuffer();
    const hashBuf = await crypto.subtle.digest(algo, buf);
    return Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

document.getElementById('calcBtn').addEventListener('click', async () => {if (!selectedFile) {toast('Please select a file first'); return; }
    document.getElementById('calcBtn').disabled = true;
    document.getElementById('calcBtn').textContent = 'Calculating...';
    const checks = document.querySelectorAll('#algoGroup input:checked');
    if (checks.length === 0) {toast('Please select at least one algorithm'); document.getElementById('calcBtn').disabled = false; document.getElementById('calcBtn').textContent = 'Calculate'; return; }
    let resultHtml = '';
    const algoMap = { 'MD5': 'MD5', 'SHA-1': 'SHA-1', 'SHA-256': 'SHA-256', 'SHA-512': 'SHA-512' };
    for (const cb of checks) {const name = cb.value;
        try {const hash = await calcHash(name);
            resultHtml += `<div style="margin-bottom:8px"><strong>${name}:</strong> <code style="background:#0f172a;padding:2px 6px;border-radius:4px;word-break:break-all;font-size:.85rem">${hash}</code></div>`;
        } catch(e) {
            resultHtml += `<div style="color:#ef4444">${name}: Calculation failed</div>`;
        }
    }
    document.getElementById('resultValue').innerHTML = resultHtml + '<div style="margin-top:8px;font-size:.8rem;color:var(--text-light);cursor:pointer" onclick="navigator.clipboard.writeText(document.getElementById(\'resultValue\').innerText).then(()=>document.getElementById(\'toast\').classList.add(\'show\'),setTimeout(()=>document.getElementById(\'toast\').classList.remove(\'show\'),2000))">ClickCopyAllResult</div>';
    document.getElementById('result').classList.add('show');
    document.getElementById('calcBtn').disabled = false;
    document.getElementById('calcBtn').textContent = 'Calculate';
});

document.getElementById('resetBtn').addEventListener('click', () => {
    selectedFile = null;
    fi.value = '';
    document.getElementById('fileName').textContent = '';
    document.getElementById('result').classList.remove('show');
});

    
function ftDrawChart(){
  var cv = document.getElementById('ftChart');
  if(!cv) return;
  var ctx = cv.getContext('2d');
  var nums = [];
  function pushNum(t){
    if(!t) return;
    var m = String(t).match(/[\d,]+(?:\.\d+)?/g);
    if(m){for(var i=0;i<m.length;i++){var v=parseFloat(m[i].replace(/,/g,''));if(v>0&&v<1e14)nums.push(v)}
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
  btn.textContent=langEN?'📋 Copy Result':'📋 Copy result';
  btn.style.cssText='margin-top:12px;display:block';
  btn.onclick=function(){
    var txt=(res.innerText||res.textContent||'').replace(/\s+/g,' ').trim();
    function toast(m){
      var t=document.getElementById('toast');
      if(t){t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
    }
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){toast(langEN?'Copied!':'Copied')}).catch(function(){ftFallbackCopy(txt);toast(langEN?'Copied!':'Copied')});
    }else{ftFallbackCopy(txt);toast(langEN?'Copied!':'Copied')}
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
