const fs = require('fs');
const f = 'paint-coverage-calculator/index.html';
const h = fs.readFileSync(f, 'utf8');
const matches = h.match(/<script>([\s\S]*?)<\/script>/g);
if (matches) {
  matches.forEach((s, i) => {
    const code = s.replace(/<\/?script[^>]*>/g, '');
    console.log('--- Block ' + i + ' (len=' + code.length + ') ---');
    console.log(code.substring(0, 200));
    console.log('...');
  });
}
