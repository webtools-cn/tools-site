const fs = require('fs');
const files = [
  'gravel-calculator/index.html',
  'en/gravel-calculator/index.html',
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
      if (code.trim() && !code.includes('dataLayer') && !code.includes('adsbygoogle') && !code.includes('gtag')) {
        try {
          new Function(code);
          console.log('  Block ' + i + ': OK');
        } catch(e) {
          console.log('  Block ' + i + ': ERROR - ' + e.message);
        }
      }
    });
  }
});
