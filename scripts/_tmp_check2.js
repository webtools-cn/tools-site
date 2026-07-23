const fs = require('fs');
const files = [
  'paint-coverage-calculator/index.html',
  'en/paint-coverage-calculator/index.html'
];

files.forEach(f => {
  const h = fs.readFileSync(f, 'utf8');
  const matches = h.match(/<script>([\s\S]*?)<\/script>/g);
  console.log('=== ' + f + ' ===');
  if (matches) {
    matches.forEach((s, i) => {
      const code = s.replace(/<\/?script[^>]*>/g, '');
      if (code.trim()) {
        console.log('  Block ' + i + ' (first 80 chars): ' + code.trim().substring(0, 80).replace(/\n/g, ' '));
      }
    });
  }
});
