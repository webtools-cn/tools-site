const fs = require('fs');
const path = process.argv[2];
const html = fs.readFileSync(path, 'utf8');
// Find all script blocks that aren't ld+json
const re = /<script(?!.*type="application\/ld\+json")[^>]*>([\s\S]*?)<\/script>/gi;
let errors = 0;
let match;
while ((match = re.exec(html)) !== null) {
  try {
    new Function(match[1]);
  } catch(e) {
    console.log('JS_ERR:', e.message.substring(0, 80));
    errors++;
  }
}
if (errors === 0) console.log('OK');
