#!/usr/bin/env node
/**
 * Fix common JS syntax errors in HTML files - Round 3.
 * More patterns from batch injection scripts.
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;
let checkedCount = 0;
let stillBroken = 0;

function fixJSSyntax(html) {
  const scriptRegex = /(<script(?:\s[^>]*)?>)([\s\S]*?)(<\/script>)/gi;
  
  return html.replace(scriptRegex, function(match, openTag, code, closeTag) {
    if (openTag.includes('application/ld+json')) return match;
    if (openTag.match(/\ssrc=/i)) return match;
    if (!code.trim()) return match;
    
    let fixed = code;
    let modified = false;
    
    // Pattern: addEventListener('DOMContentLoaded', initRating; → addEventListener('DOMContentLoaded', initRating);
    fixed = fixed.replace(/document\.addEventListener\('DOMContentLoaded',\s*(\w+);/g, function(m, fn) {
      modified = true;
      return "document.addEventListener('DOMContentLoaded', " + fn + ");";
    });
    
    // Pattern: initRating; } → initRating); }
    fixed = fixed.replace(/document\.addEventListener\('DOMContentLoaded',\s*(\w+)\s*;\s*\}/g, function(m, fn) {
      modified = true;
      return "document.addEventListener('DOMContentLoaded', " + fn + "); }";
    });
    
    // Pattern: else {  } → else { initRating(); }
    // Skip - complex, need context
    
    // Pattern: ,2000;} → ,2000);}
    fixed = fixed.replace(/,2000;\}/g, function() {
      modified = true;
      return ',2000);}';
    });
    
    // Pattern: },3000} → },3000)}
    fixed = fixed.replace(/\},3000\}/g, function() {
      modified = true;
      return '},3000)}';
    });
    
    // Pattern: },2200} → },2200)}
    fixed = fixed.replace(/\},2200\}/g, function() {
      modified = true;
      return '},2200)}';
    });
    
    // Pattern: )}} → )}) (missing closing paren in showToast)
    fixed = fixed.replace(/\[\"catch\"\]\(function\(\)\{showToast\(\"复制失败\"\)\}\}/g, function() {
      modified = true;
      return '["catch"](function(){showToast("复制失败")})}';
    });
    
    // Pattern: message===){ → message===""){ 
    fixed = fixed.replace(/\.reason\.message===\)\{/g, function() {
      modified = true;
      return '.reason.message===""){';
    });
    
    // Pattern: .label.width + 40; → .label.width + 40);
    fixed = fixed.replace(/\.label\.width\s*\+\s*40;/g, function() {
      modified = true;
      return '.label.width + 40);';
    });
    
    // Pattern: )})  at end → )}) (IIFE close with extra)
    // Skip complex ones
    
    // Pattern: })} at end → })()
    if (fixed.match(/\}\)\}\s*$/)) {
      fixed = fixed.replace(/\}\)\}\s*$/, function() {
        modified = true;
        return '})();';
      });
    }
    
    // Pattern: .catch(function() { s.innerHTML = ''; });\n})();\n  → just remove extra )();
    // This is related tools script - seems fine actually
    
    // Pattern: event.target.classList.add('active');\n} → event.target.classList.add('active');\n}
    // This is valid syntax, the error is elsewhere
    
    if (modified) {
      return openTag + fixed + closeTag;
    }
    return match;
  });
}

function checkFile(filepath) {
  if (!fs.existsSync(filepath)) return;
  checkedCount++;
  
  const html = fs.readFileSync(filepath, 'utf8');
  const fixed = fixJSSyntax(html);
  
  if (fixed === html) return;
  
  const scripts = fixed.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
  let origErrorCount = 0;
  let fixedErrorCount = 0;
  
  const origScripts = html.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
  origScripts.forEach((s) => {
    if (s.includes('application/ld+json')) return;
    if (s.match(/<script\s+[^>]*src=/i)) return;
    const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
    if (!code.trim()) return;
    try { new Function(code); } catch(e) { origErrorCount++; }
  });
  
  if (origErrorCount === 0) return;
  
  scripts.forEach((s) => {
    if (s.includes('application/ld+json')) return;
    if (s.match(/<script\s+[^>]*src=/i)) return;
    const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
    if (!code.trim()) return;
    try { new Function(code); } catch(e) { fixedErrorCount++; }
  });
  
  if (fixedErrorCount >= origErrorCount) {
    stillBroken++;
    return;
  }
  
  fs.writeFileSync(filepath, fixed, 'utf8');
  fixedCount++;
  console.log('FIXED: ' + filepath + ' (' + origErrorCount + ' → ' + fixedErrorCount + ' errors)');
}

function processDir(dir) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir);
  for (const entry of entries) {
    if (entry.startsWith('.')) continue;
    if (entry === 'node_modules' || entry === 'scripts' || entry === 'quality' || 
        entry === 'css' || entry === 'js' || entry === '.gsc-data') continue;
    const fullpath = path.join(dir, entry);
    if (fs.statSync(fullpath).isDirectory()) {
      const htmlFile = path.join(fullpath, 'index.html');
      if (fs.existsSync(htmlFile)) checkFile(htmlFile);
    }
  }
}

checkFile('index.html');
checkFile('en/index.html');
processDir('.');
processDir('en');

console.log('\n=== Summary ===');
console.log('Checked: ' + checkedCount + ' files');
console.log('Fixed: ' + fixedCount + ' files');
console.log('Still broken: ' + stillBroken + ' files');
