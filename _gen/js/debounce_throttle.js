function loadExample(){
document.getElementById('funcName').value='handleSearch';
document.getElementById('delay').value='300';
document.getElementById('funcBody').value='console.log("Searching for:", query);';
document.getElementById('mode').value='debounce';
document.getElementById('leading').checked=false;
document.getElementById('trailing').checked=true;
document.getElementById('maxWait').value='';
execute();
}
function clearInput(){
document.getElementById('funcName').value='';
document.getElementById('delay').value='300';
document.getElementById('funcBody').value='';
document.getElementById('mode').value='debounce';
document.getElementById('leading').checked=false;
document.getElementById('trailing').checked=true;
document.getElementById('maxWait').value='';
document.getElementById('output').textContent='等待生成...';
}
function execute(){
var name=document.getElementById('funcName').value.trim()||'myFunction';
var delay=document.getElementById('delay').value.trim()||'300';
var body=document.getElementById('funcBody').value.trim()||'// your code here';
var mode=document.getElementById('mode').value;
var leading=document.getElementById('leading').checked;
var trailing=document.getElementById('trailing').checked;
var maxWait=document.getElementById('maxWait').value.trim();
var code='';
if(mode==='debounce'){
code='function debounce(fn, delay, options = {}) {\n';
code+='  const { leading = false, trailing = true } = options;\n';
code+='  let timer = null;\n';
code+='  let lastCallTime = 0;\n';
code+='  let lastArgs = null;\n';
code+='\n';
code+='  return function(...args) {\n';
code+='    const now = Date.now();\n';
code+='    lastArgs = args;\n';
code+='\n';
code+='    if (leading && !timer) {\n';
code+='      fn.apply(this, args);\n';
code+='      lastCallTime = now;\n';
code+='    }\n';
code+='\n';
code+='    clearTimeout(timer);\n';
code+='    timer = setTimeout(() => {\n';
code+='      if (trailing && (!leading || now - lastCallTime >= delay)) {\n';
code+='        fn.apply(this, lastArgs);\n';
code+='      }\n';
code+='      timer = null;\n';
code+='    }, delay);\n';
code+='  };\n';
code+='}\n';
code+='\n';
code+='// Usage:\n';
code+='const '+name+' = debounce(function(query) {\n';
code+='  '+body+'\n';
code+='}, '+delay;
if(leading||!trailing){
code+=', { leading: '+leading+', trailing: '+trailing+' }';
}
code+=');\n';
code+='\n';
code+='// Call: '+name+'(searchQuery);\n';
code+='// Waits '+delay+'ms of inactivity before executing\n';
}else{
code='function throttle(fn, delay, options = {}) {\n';
code+='  const { leading = true, trailing = false } = options;\n';
code+='  let timer = null;\n';
code+='  let lastArgs = null;\n';
code+='  let lastThis = null;\n';
var maxWaitLine=maxWait?'  const maxWait = options.maxWait || delay;\n':'';
code+=maxWaitLine;
code+='\n';
code+='  return function(...args) {\n';
code+='    if (!timer) {\n';
code+='      if (leading) {\n';
code+='        fn.apply(this, args);\n';
code+='      } else {\n';
code+='        lastArgs = args;\n';
code+='        lastThis = this;\n';
code+='      }\n';
code+='\n';
code+='      timer = setTimeout(() => {\n';
code+='        if (trailing && lastArgs) {\n';
code+='          fn.apply(lastThis, lastArgs);\n';
code+='        }\n';
code+='        timer = null;\n';
code+='        lastArgs = null;\n';
code+='        lastThis = null;\n';
code+='      }, delay);\n';
code+='    } else {\n';
code+='      lastArgs = args;\n';
code+='      lastThis = this;\n';
code+='    }\n';
code+='  };\n';
code+='}\n';
code+='\n';
code+='// Usage:\n';
code+='const '+name+' = throttle(function(event) {\n';
code+='  '+body+'\n';
code+='}, '+delay;
if(!leading||trailing||maxWait){
var opts=[];
if(!leading)opts.push('leading: false');
if(trailing)opts.push('trailing: true');
if(maxWait)opts.push('maxWait: '+maxWait);
if(opts.length)code+=', { '+opts.join(', ')+' }';
}
code+=');\n';
code+='\n';
code+='// Call: '+name+'(scrollEvent);\n';
code+='// Executes at most once every '+delay+'ms\n';
}
document.getElementById('output').textContent=code;
saveHistory('debounceThrottleHistory',name);
showToast(mode==='debounce'?'防抖函数生成完成':'节流函数生成完成');
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
downloadText(name+'-utils.js',text);
}
