const fs = require('fs');
const path = require('path');

const dirs = fs.readdirSync('.').filter(d => {
  const f = path.join('.', d, 'index.html');
  return fs.existsSync(f) && 
    !['about','blog','contact','privacy','terms','css','data','en','scripts','tests','quality','quality-reports','.git','.gsc-data'].includes(d);
});

const errorTypes = {};

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
      const key = e.message.slice(0, 60);
      if(!errorTypes[key]) errorTypes[key] = [];
      if(errorTypes[key].length < 5) errorTypes[key].push(dir);
    }
  }
});

// 按频次排序
const sorted = Object.entries(errorTypes).sort((a,b) => b[1].length - a[1].length);
console.log('=== Syntax Error Categories ===');
sorted.forEach(([msg, dirs]) => {
  console.log(`\n${dirs.length} pages: "${msg}"`);
  console.log('  Examples: ' + dirs.join(', '));
});