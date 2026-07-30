const fs = require('fs');
const path = require('path');

// 全站扫描：检测JS语法错误 + 函数未定义
const dirs = fs.readdirSync('.').filter(d => {
  const f = path.join('.', d, 'index.html');
  return fs.existsSync(f) && 
    !['about','blog','contact','privacy','terms','css','data','en','scripts','tests','quality','quality-reports','.git','.gsc-data'].includes(d);
});

let syntaxErrors = [], missingFns = [];

dirs.forEach(dir => {
  const filePath = path.join(dir, 'index.html');
  const content = fs.readFileSync(filePath, 'utf8');
  const scripts = content.match(/<script>([\s\S]*?)<\/script>/g);
  if(!scripts) return;
  
  // 跳过第0、1个script（GA和error handler）
  for(let i = 2; i < scripts.length; i++) {
    const js = scripts[i].replace(/<script>|<\/script>/g, '');
    try {
      new Function(js);
    } catch(e) {
      syntaxErrors.push({dir, scriptIdx: i, error: e.message});
    }
  }
  
  // 检查onclick调用的函数是否定义
  const onclickFns = [...content.matchAll(/on(?:click|change|submit|input|keypress|mousedown)=\s*"([^(]+)\(/g)]
    .map(m => m[1].trim());
  const uniqueFns = [...new Set(onclickFns)];
  uniqueFns.forEach(fn => {
    if(['event','this','gtag'].includes(fn)) return;
    // 转义特殊正则字符
    const escFn = fn.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const defPattern = new RegExp('function\\s+' + escFn + '\\s*\\(|' + escFn + '\\s*=\\s*function|window\\.' + escFn + '\\s*=');
    if(!defPattern.test(content)) {
      missingFns.push({dir, fn});
    }
  });
});

console.log('=== Syntax Errors: ' + syntaxErrors.length + ' ===');
syntaxErrors.forEach(e => console.log('  ' + e.dir + ' (script#' + e.scriptIdx + '): ' + e.error));

console.log('\n=== Missing Functions: ' + missingFns.length + ' ===');
missingFns.slice(0, 50).forEach(e => console.log('  ' + e.dir + ': ' + e.fn));

// 统计fn出现频次（top函数名）
const fnFreq = {};
missingFns.forEach(e => { fnFreq[e.fn] = (fnFreq[e.fn]||0) + 1; });
console.log('\n=== Top Missing Functions (by frequency) ===');
Object.entries(fnFreq).sort((a,b) => b[1]-a[1]).slice(0,20).forEach(([fn, cnt]) => {
  console.log('  ' + fn + ': ' + cnt + ' pages');
});
