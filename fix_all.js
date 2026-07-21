const fs = require('fs');
const acorn = require('/home/chison/.hermes/hermes-agent/node_modules/acorn');

function fixFile(tool) {
  const path = tool + '/index.html';
  let html = fs.readFileSync(path, 'utf8');
  const original = html;
  
  // Extract all non-JSON-LD script blocks and check for errors
  const regex = /<script([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  let scripts = [];
  while ((m = regex.exec(html)) !== null) {
    const attrs = m[1];
    const content = m[2];
    if (attrs.includes('application/ld+json') || !content.trim() || attrs.includes('src=')) continue;
    scripts.push({ start: m.index, end: m.index + m[0].length, content, attrs });
  }
  
  for (const s of scripts) {
    try {
      acorn.parse(s.content, {ecmaVersion: 2020, sourceType: 'module'});
    } catch(e) {
      console.log(tool + ': ' + e.message);
    }
  }
  
  if (html !== original) {
    fs.writeFileSync(path, html);
    return true;
  }
  return false;
}

// Fix html-tag-stripper specifically
let html = fs.readFileSync('html-tag-stripper/index.html', 'utf8');
// The broken line has mixed escaping. Let me find and replace it properly.
const lines = html.split('\n');
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("s.addEventListener('click',function(){i.value='<article>")) {
    // Replace with correct version - use backtick string to avoid escaping issues
    lines[i] = "s.addEventListener('click',function(){i.value='<article>\\n  <h1>Hello World</h1>\\n  <p>This is a <strong>sample</strong> article with <em>various</em> HTML tags.</p>\\n  <ul>\\n    <li>First item with <a href=\"#\">a link</a></li>\\n    <li>Second item</li>\\n    <li>Third <span style=\"color:red\">colored</span> item</li>\\n  </ul>\\n</article>'});";
    break;
  }
}
html = lines.join('\n');
fs.writeFileSync('html-tag-stripper/index.html', html);
console.log('Fixed html-tag-stripper');
