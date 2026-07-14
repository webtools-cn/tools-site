/* ===================================================================
 * Hash 哈希生成器 - Chrome 扩展 popup 逻辑
 * 复用工具站 free-toolbase.com/hash-generator/ 的核心算法
 * 纯前端，零依赖，数据完全本地处理
 * =================================================================== */
(function () {
'use strict';

/* ==================== MD5 (纯JS实现) ==================== */
var md5 = (function(){
  function safeAdd(x,y){var lsw=(x&0xFFFF)+(y&0xFFFF);var msw=(x>>16)+(y>>16)+(lsw>>16);return(msw<<16)|(lsw&0xFFFF)}
  function bitRol(num,cnt){return(num<<cnt)|(num>>>(32-cnt))}
  function cmn(q,a,b,x,s,t){return safeAdd(bitRol(safeAdd(safeAdd(a,q),safeAdd(x,t)),s),b)}
  function ff(a,b,c,d,x,s,t){return cmn((b&c)|((~b)&d),a,b,x,s,t)}
  function gg(a,b,c,d,x,s,t){return cmn((b&d)|(c&(~d)),a,b,x,s,t)}
  function hh(a,b,c,d,x,s,t){return cmn(b^c^d,a,b,x,s,t)}
  function ii(a,b,c,d,x,s,t){return cmn(c^(b|(~d)),a,b,x,s,t)}
  function coreMD5(x,len){
    x[len>>5]|=0x80<<(len%32);
    x[(((len+64)>>>9)<<4)+14]=len;
    var a=1732584193,b=-271733879,c=-1732584194,d=271733878;
    for(var i=0;i<x.length;i+=16){
      var olda=a,oldb=b,oldc=c,oldd=d;
      a=ff(a,b,c,d,x[i+0],7,-680876936);d=ff(d,a,b,c,x[i+1],12,-389564586);c=ff(c,d,a,b,x[i+2],17,606105819);b=ff(b,c,d,a,x[i+3],22,-1044525330);
      a=ff(a,b,c,d,x[i+4],7,-176418897);d=ff(d,a,b,c,x[i+5],12,1200080426);c=ff(c,d,a,b,x[i+6],17,-1473231341);b=ff(b,c,d,a,x[i+7],22,-45705983);
      a=ff(a,b,c,d,x[i+8],7,1770035416);d=ff(d,a,b,c,x[i+9],12,-1958414417);c=ff(c,d,a,b,x[i+10],17,-42063);b=ff(b,c,d,a,x[i+11],22,-1990404162);
      a=ff(a,b,c,d,x[i+12],7,1804603682);d=ff(d,a,b,c,x[i+13],12,-40341101);c=ff(c,d,a,b,x[i+14],17,-1502002290);b=ff(b,c,d,a,x[i+15],22,1236535329);
      a=gg(a,b,c,d,x[i+1],5,-165796510);d=gg(d,a,b,c,x[i+6],9,-1069501632);c=gg(c,d,a,b,x[i+11],14,643717713);b=gg(b,c,d,a,x[i+0],20,-373897302);
      a=gg(a,b,c,d,x[i+5],5,-701558691);d=gg(d,a,b,c,x[i+10],9,38016083);c=gg(c,d,a,b,x[i+15],14,-660478335);b=gg(b,c,d,a,x[i+4],20,-405537848);
      a=gg(a,b,c,d,x[i+9],5,568446438);d=gg(d,a,b,c,x[i+14],9,-1019803690);c=gg(c,d,a,b,x[i+3],14,-187363961);b=gg(b,c,d,a,x[i+8],20,1163531501);
      a=gg(a,b,c,d,x[i+13],5,-1444681467);d=gg(d,a,b,c,x[i+2],9,-51403784);c=gg(c,d,a,b,x[i+7],14,1735328473);b=gg(b,c,d,a,x[i+12],20,-1926607734);
      a=hh(a,b,c,d,x[i+5],4,-378558);d=hh(d,a,b,c,x[i+8],11,-2022574463);c=hh(c,d,a,b,x[i+11],16,1839030562);b=hh(b,c,d,a,x[i+14],23,-35309556);
      a=hh(a,b,c,d,x[i+1],4,-1530992060);d=hh(d,a,b,c,x[i+4],11,1272893353);c=hh(c,d,a,b,x[i+7],16,-155497632);b=hh(b,c,d,a,x[i+10],23,-1094730640);
      a=hh(a,b,c,d,x[i+13],4,681279174);d=hh(d,a,b,c,x[i+0],11,-358537222);c=hh(c,d,a,b,x[i+3],16,-722521979);b=hh(b,c,d,a,x[i+6],23,76029189);
      a=hh(a,b,c,d,x[i+9],4,-640364487);d=hh(d,a,b,c,x[i+12],11,-421815835);c=hh(c,d,a,b,x[i+15],16,530742520);b=hh(b,c,d,a,x[i+2],23,-995338651);
      a=ii(a,b,c,d,x[i+0],6,-198630844);d=ii(d,a,b,c,x[i+7],10,112689814);c=ii(c,d,a,b,x[i+14],15,-1416354905);b=ii(b,c,d,a,x[i+5],21,-57434055);
      a=ii(a,b,c,d,x[i+12],6,1700485571);d=ii(d,a,b,c,x[i+3],10,-1894986606);c=ii(c,d,a,b,x[i+10],15,-1051523);b=ii(b,c,d,a,x[i+1],21,-2054922799);
      a=ii(a,b,c,d,x[i+8],6,1873313359);d=ii(d,a,b,c,x[i+15],10,-30611744);c=ii(c,d,a,b,x[i+6],15,-1565486053);b=ii(b,c,d,a,x[i+13],21,1309151649);
      a=ii(a,b,c,d,x[i+4],6,-145523070);d=ii(d,a,b,c,x[i+11],10,-1120210379);c=ii(c,d,a,b,x[i+2],15,718787259);b=ii(b,c,d,a,x[i+9],21,-343485551);
      a=safeAdd(a,olda);b=safeAdd(b,oldb);c=safeAdd(c,oldc);d=safeAdd(d,oldd);
    }
    return[a,b,c,d];
  }
  function binl2hex(binarray){
    var hexTab='0123456789abcdef';var str='';
    for(var i=0;i<binarray.length*4;i++){
      str+=hexTab.charAt((binarray[i>>2]>>((i%4)*8+4))&0xF)+hexTab.charAt((binarray[i>>2]>>((i%4)*8))&0xF);
    }
    return str;
  }
  function bytesToWords(bytes){
    var words=[];var i=0;
    for(;i+3<bytes.length;i+=4){
      words[i>>2]=bytes[i]|(bytes[i+1]<<8)|(bytes[i+2]<<16)|(bytes[i+3]<<24);
    }
    if(i<bytes.length){
      var w=0;
      for(var j=0;i+j<bytes.length;j++){w|=bytes[i+j]<<(j*8)}
      words[i>>2]=w;
    }
    return words;
  }
  return function(data){
    var words=bytesToWords(data);
    var result=coreMD5(words,data.length*8);
    return binl2hex(result);
  };
})();

/* ==================== SHA-1 (纯JS实现) ==================== */
var sha1 = (function(){
  function rotateLeft(n,s){return(n<<s)|(n>>>(32-s))}
  function toHexStr(n){
    var s='',v;
    for(var i=7;i>=0;i--){v=(n>>>(i*4))&0x0f;s+=v.toString(16)}
    return s;
  }
  return function(data){
    var len=data.length;
    var bitLen=len*8;
    var paddedLen=len+1+8;
    var padZeros=(64-(paddedLen%64))%64;
    paddedLen+=padZeros;
    var padded=new Uint8Array(paddedLen);
    padded.set(data);
    padded[len]=0x80;
    var dv=new DataView(padded.buffer);
    dv.setUint32(paddedLen-8,Math.floor(bitLen/0x100000000),false);
    dv.setUint32(paddedLen-4,bitLen>>>0,false);
    var H0=0x67452301,H1=0xEFCDAB89,H2=0x98BADCFE,H3=0x10325476,H4=0xC3D2E1F0;
    for(var i=0;i<paddedLen;i+=64){
      var w=new Array(80);
      for(var j=0;j<16;j++){w[j]=dv.getUint32(i+j*4,false)}
      for(var j=16;j<80;j++){w[j]=rotateLeft(w[j-3]^w[j-8]^w[j-14]^w[j-16],1)}
      var a=H0,b=H1,c=H2,d=H3,e=H4,f,k,temp;
      for(var j=0;j<80;j++){
        if(j<20){f=(b&c)|((~b)&d);k=0x5A827999}
        else if(j<40){f=b^c^d;k=0x6ED9EBA1}
        else if(j<60){f=(b&c)|(b&d)|(c&d);k=0x8F1BBCDC}
        else{f=b^c^d;k=0xCA62C1D6}
        temp=(rotateLeft(a,5)+f+e+k+w[j])|0;
        e=d;d=c;c=rotateLeft(b,30);b=a;a=temp;
      }
      H0=(H0+a)|0;H1=(H1+b)|0;H2=(H2+c)|0;H3=(H3+d)|0;H4=(H4+e)|0;
    }
    return toHexStr(H0)+toHexStr(H1)+toHexStr(H2)+toHexStr(H3)+toHexStr(H4);
  };
})();

/* ==================== 辅助函数 ==================== */
function bufferToHex(buffer){
  var bytes=buffer instanceof Uint8Array?buffer:new Uint8Array(buffer);
  var hex='';
  for(var i=0;i<bytes.length;i++){hex+=(bytes[i]<16?'0':'')+bytes[i].toString(16)}
  return hex;
}

function hexToBytes(hex){
  var bytes=new Uint8Array(hex.length/2);
  for(var i=0;i<hex.length;i+=2){bytes[i/2]=parseInt(hex.substr(i,2),16)}
  return bytes;
}

function formatSize(bytes){
  if(bytes<1024)return bytes+' B';
  if(bytes<1048576)return(bytes/1024).toFixed(2)+' KB';
  if(bytes<1073741824)return(bytes/1048576).toFixed(2)+' MB';
  return(bytes/1073741824).toFixed(2)+' GB';
}

function fmtHash(hash, upper){
  return upper?hash.toUpperCase():hash;
}

var hasSubtleCrypto=(typeof crypto!=='undefined'&&crypto.subtle&&typeof crypto.subtle.digest==='function');

var hashFns={
  md5:function(data){return md5(data)},
  sha1:function(data){return sha1(data)},
  sha256:function(data){return crypto.subtle.digest('SHA-256',data).then(bufferToHex)},
  sha384:function(data){return crypto.subtle.digest('SHA-384',data).then(bufferToHex)},
  sha512:function(data){return crypto.subtle.digest('SHA-512',data).then(bufferToHex)}
};

var blockSizes={md5:64,sha1:64,sha256:64,sha384:128,sha512:128};

/* HMAC 计算 */
async function computeHMAC(hashFn,keyBytes,msgBytes,blockSize){
  var keyData;
  if(keyBytes.length>blockSize){
    keyData=hexToBytes(await hashFn(keyBytes));
  }else{
    keyData=keyBytes;
  }
  var paddedKey=new Uint8Array(blockSize);
  paddedKey.set(keyData);
  var ipad=new Uint8Array(blockSize);
  var opad=new Uint8Array(blockSize);
  for(var i=0;i<blockSize;i++){ipad[i]=paddedKey[i]^0x36;opad[i]=paddedKey[i]^0x5C}
  var innerInput=new Uint8Array(blockSize+msgBytes.length);
  innerInput.set(ipad);
  innerInput.set(msgBytes,blockSize);
  var innerHash=hexToBytes(await hashFn(innerInput));
  var outerInput=new Uint8Array(blockSize+innerHash.length);
  outerInput.set(opad);
  outerInput.set(innerHash,blockSize);
  return await hashFn(outerInput);
}

/* ==================== UI 状态 ==================== */
var toastEl=document.getElementById('toast');
var textResults={};
var fileResults={};
var hmacResults={};

function showToast(msg){
  toastEl.textContent=msg;
  toastEl.classList.add('show');
  setTimeout(function(){toastEl.classList.remove('show')},2000);
}

function flashBtn(btn,text,ok){
  var orig=btn.textContent;
  btn.textContent=text;
  setTimeout(function(){btn.textContent=orig},1500);
}

/* ==================== Tab 切换 ==================== */
var tabBtns=document.querySelectorAll('.tab-btn');
var tabPanels=document.querySelectorAll('.tab-panel');

tabBtns.forEach(function(btn){
  btn.addEventListener('click',function(){
    var target=this.dataset.tab;
    tabBtns.forEach(function(b){b.classList.remove('active')});
    tabPanels.forEach(function(p){p.classList.remove('active')});
    this.classList.add('active');
    document.getElementById('tab-'+target).classList.add('active');
  });
});

/* ==================== 文本哈希 ==================== */
var textInput=document.getElementById('textInput');
var textCount=document.getElementById('textCount');
var uppercaseText=document.getElementById('uppercaseText');
var liveCompute=document.getElementById('liveCompute');
var textTimer=null;

function updateTextCount(){
  var len=textInput.value.length;
  textCount.textContent=len+' 字符';
}

function setTextResult(algo,hash){
  textResults[algo]=hash;
  var el=document.getElementById('res_text_'+algo);
  if(el)el.textContent=fmtHash(hash,uppercaseText.checked);
}

function clearTextResults(){
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){
    textResults[a]='';
    var el=document.getElementById('res_text_'+a);
    if(el)el.textContent='—';
  });
}

function computeTextHashes(){
  var text=textInput.value;
  if(!text){clearTextResults();return}
  var bytes=new TextEncoder().encode(text);
  setTextResult('md5',md5(bytes));
  setTextResult('sha1',sha1(bytes));
  if(hasSubtleCrypto){
    ['sha256','sha384','sha512'].forEach(function(a){
      crypto.subtle.digest(a.toUpperCase(),bytes).then(function(buf){
        setTextResult(a,bufferToHex(buf));
      });
    });
  }else{
    ['sha256','sha384','sha512'].forEach(function(a){setTextResult(a,'需要安全上下文');});
  }
}

function updateTextUppercase(){
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){
    var el=document.getElementById('res_text_'+a);
    if(el&&textResults[a])el.textContent=fmtHash(textResults[a],uppercaseText.checked);
  });
}

document.getElementById('btnComputeText').addEventListener('click',function(){computeTextHashes();});
document.getElementById('btnClearText').addEventListener('click',function(){textInput.value='';clearTextResults();updateTextCount();});

textInput.addEventListener('input',function(){
  updateTextCount();
  if(liveCompute.checked){
    clearTimeout(textTimer);
    textTimer=setTimeout(computeTextHashes,200);
  }
});

uppercaseText.addEventListener('change',updateTextUppercase);

/* ==================== 文件哈希 ==================== */
var dropZone=document.getElementById('dropZone');
var fileInput=document.getElementById('fileInput');
var fileInfo=document.getElementById('fileInfo');

function setFileResult(algo,hash){
  fileResults[algo]=hash;
  var el=document.getElementById('res_file_'+algo);
  if(el)el.textContent=fmtHash(hash,uppercaseText.checked);
}

dropZone.addEventListener('click',function(){fileInput.click()});
dropZone.addEventListener('dragover',function(e){e.preventDefault();dropZone.classList.add('dragover');});
dropZone.addEventListener('dragleave',function(){dropZone.classList.remove('dragover');});
dropZone.addEventListener('drop',function(e){
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if(e.dataTransfer.files.length>0)handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change',function(e){if(e.target.files.length>0)handleFile(e.target.files[0]);});

async function handleFile(file){
  fileInfo.style.display='block';
  fileInfo.textContent='📄 '+file.name+' · '+formatSize(file.size);
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){setFileResult(a,'计算中...');});
  try{
    var buffer=await file.arrayBuffer();
    var bytes=new Uint8Array(buffer);
    setFileResult('md5',md5(bytes));
    setFileResult('sha1',sha1(bytes));
    if(hasSubtleCrypto){
      ['sha256','sha384','sha512'].forEach(function(a){
        crypto.subtle.digest(a.toUpperCase(),bytes).then(function(buf){
          setFileResult(a,bufferToHex(buf));
        });
      });
    }else{
      ['sha256','sha384','sha512'].forEach(function(a){setFileResult(a,'需要安全上下文');});
    }
  }catch(e){
    showToast('文件处理错误: '+e.message);
    ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){setFileResult(a,'计算失败');});
  }
}

/* ==================== HMAC ==================== */
var hmacKey=document.getElementById('hmacKey');
var hmacMsg=document.getElementById('hmacMsg');
var uppercaseHmac=document.getElementById('uppercaseHmac');

function setHmacResult(algo,hash){
  hmacResults[algo]=hash;
  var el=document.getElementById('res_hmac_'+algo);
  if(el)el.textContent=fmtHash(hash,uppercaseHmac.checked);
}

function clearHmacResults(){
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){
    hmacResults[a]='';
    var el=document.getElementById('res_hmac_'+a);
    if(el)el.textContent='—';
  });
}

function computeHMACs(){
  var key=hmacKey.value;
  var msg=hmacMsg.value;
  if(!msg){clearHmacResults();return}
  var keyBytes=new TextEncoder().encode(key);
  var msgBytes=new TextEncoder().encode(msg);
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(algo){
    if(!hasSubtleCrypto&&!['md5','sha1'].includes(algo)){
      setHmacResult(algo,'需要安全上下文');
      return;
    }
    computeHMAC(hashFns[algo],keyBytes,msgBytes,blockSizes[algo]).then(function(h){
      setHmacResult(algo,h);
    });
  });
}

function updateHmacUppercase(){
  ['md5','sha1','sha256','sha384','sha512'].forEach(function(a){
    var el=document.getElementById('res_hmac_'+a);
    if(el&&hmacResults[a])el.textContent=fmtHash(hmacResults[a],uppercaseHmac.checked);
  });
}

document.getElementById('btnComputeHmac').addEventListener('click',computeHMACs);
document.getElementById('btnClearHmac').addEventListener('click',function(){hmacKey.value='';hmacMsg.value='';clearHmacResults();});
uppercaseHmac.addEventListener('change',updateHmacUppercase);

/* ==================== 复制功能 ==================== */
function doCopy(text){
  if(navigator.clipboard){
    navigator.clipboard.writeText(text).then(function(){showToast('已复制到剪贴板');});
  }else{
    var ta=document.createElement('textarea');
    ta.value=text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('已复制到剪贴板');
  }
}

document.querySelectorAll('.hash-copy').forEach(function(btn){
  btn.addEventListener('click',function(){
    var targetId=this.dataset.target;
    var el=document.getElementById(targetId);
    if(!el||!el.textContent||el.textContent==='—'||el.textContent==='计算中...'||el.textContent==='计算失败'||el.textContent.indexOf('需要')===0){
      showToast('没有结果可复制');return;
    }
    doCopy(el.textContent);
  });
});

document.getElementById('btnCopyAll').addEventListener('click',function(){
  var activePanel=document.querySelector('.tab-panel.active');
  var items=activePanel.querySelectorAll('.hash-item');
  var lines=[];
  items.forEach(function(item){
    var name=item.querySelector('.hash-name').textContent;
    var val=item.querySelector('.hash-val').textContent;
    if(val&&val!=='—'&&val!=='计算中...'&&val!=='计算失败'&&val.indexOf('需要')!==0){
      lines.push(name+': '+val);
    }
  });
  if(lines.length===0){showToast('没有结果可复制');return;}
  doCopy(lines.join('\n'));
});

/* ==================== 底部链接 ==================== */
document.getElementById('siteLink').addEventListener('click',function(e){
  if(typeof chrome!=='undefined'&&chrome.tabs&&chrome.tabs.create){
    e.preventDefault();
    chrome.tabs.create({url:this.href});
  }
});

/* ==================== 初始化 ==================== */
updateTextCount();
})();
