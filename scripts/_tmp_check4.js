const fs = require('fs');
const f = 'paint-coverage-calculator/index.html';
const h = fs.readFileSync(f, 'utf8');
const matches = h.match(/<script>([\s\S]*?)<\/script>/g);
const code = matches[1].replace(/<\/?script[^>]*>/g, '');
// Write to temp file for node -c
fs.writeFileSync('/tmp/_tmp_paint.js', code);
console.log('Written ' + code.length + ' bytes');
