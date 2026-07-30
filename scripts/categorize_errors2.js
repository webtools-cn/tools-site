const fs = require('fs');
const path = require('path');

const dirs = fs.readdirSync('.').filter(d => {
  const f = path.join('.', d, 'index.html');
  return fs.existsSync(f) && 
    !['about','blog','contact','privacy','terms','css','data','en','scripts','tests','quality','quality-reports','.git','.gsc-data'].includes(d);
});

const errorCounts = {};
const allErrors = [];

dirs.forEach(dir => {
  const filePath = path.join(dir, 'index.html');
  const content = fs.readFileSync(filePath, 'utf8');
  const scripts = content.match(/<script>([\s\S]*?)<\/script>/g);
  if(!scripts) return;
  
  for(let i = 2; i < scripts.length; i++) {
    const js = scripts[i].replace(/<script>|<\/script>/g, '');
    try {
      new Function(js);
    } catch(e) {
      const msg = e.message;
      errorCounts[msg] = (errorCounts[msg]||0) + 1;
      allErrors.push({dir, scriptIdx: i, error: msg});
    }
  }
});

// 按频次排序
const sorted = Object.entries(errorCounts).sort((a,b) => b[1]-a[1]);
console.log('=== All Error Types by Count ===');
sorted.forEach(([msg, cnt]) => {
  console.log(cnt + ': ' + msg);
});

// 输出总览
console.log('\nTotal pages with errors:', new Set(allErrors.map(e=>e.dir)).size);
console.log('Total error instances:', allErrors.length);
console.log('Unique error types:', sorted.length);