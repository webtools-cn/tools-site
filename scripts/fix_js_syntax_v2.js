#!/usr/bin/env node
/**
 * Fix common JS syntax errors in HTML files - Round 2.
 * Focuses on patterns introduced by batch injection scripts.
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
    
    // Pattern 1: (function(){ // resultAddCopy var → (function(){ var
    fixed = fixed.replace(/\(function\(\)\{\s*\/\/\s*resultAddCopy\s+var\s/g, function(m) {
      modified = true;
      return '(function(){ var ';
    });
    
    // Pattern 2: })(;) → })();
    fixed = fixed.replace(/\}\)\(;\)/g, function() {
      modified = true;
      return '})();';
    });
    
    // Pattern 3: }(; → })();
    fixed = fixed.replace(/\}\(\;\)/g, function() {
      modified = true;
      return '})();';
    });
    
    // Pattern 4: ,3000)} at start → proper showToast
    if (fixed.match(/^\s*,3000\)\}/)) {
      fixed = fixed.replace(/^\s*,3000\)\}/, 'function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},3000)}');
      modified = true;
    }
    
    // Pattern 5: window.addEventListener('load',function(){...};  (missing closing paren)
    fixed = fixed.replace(/window\.addEventListener\('load',function\(\)\{([^}]+)\};/, function(m, body) {
      modified = true;
      return "window.addEventListener('load',function(){" + body + "});";
    });
    
    // Pattern 6: toggle('open'; → toggle('open');
    fixed = fixed.replace(/\.toggle\('open';/g, function() {
      modified = true;
      return ".toggle('open');";
    });
    
    // Pattern 7: toggleFaq(el{ → toggleFaq(el){
    fixed = fixed.replace(/toggleFaq\(el\{/g, function() {
      modified = true;
      return "toggleFaq(el){";
    });
    
    // Pattern 8: aagGenerate; → aagGenerate);  (missing closing paren in addEventListener)
    fixed = fixed.replace(/document\.addEventListener\('DOMContentLoaded',\s*(\w+);/g, function(m, fn) {
      modified = true;
      return "document.addEventListener('DOMContentLoaded', " + fn + ");";
    });
    
    // Pattern 9: link.click(; → link.click();
    fixed = fixed.replace(/\.click\(\;/g, function() {
      modified = true;
      return ".click();";
    });
    
    // Pattern 10: initRating; → initRating);
    fixed = fixed.replace(/document\.addEventListener\('DOMContentLoaded',\s*(\w+);/g, function(m, fn) {
      modified = true;
      return "document.addEventListener('DOMContentLoaded', " + fn + ");";
    });
    
    // Pattern 11: else }(; → else {}();
    fixed = fixed.replace(/else\s*\}\(\;\)/g, function() {
      modified = true;
      return "else {}();";
    });
    
    // Pattern 12: else {  } → else { initRating(); }  (for rating script)
    // Actually this is complex, skip for now
    
    // Pattern 13: lookup();) → lookup();})  (missing closing for IIFE or function)
    // Skip complex ones
    
    // Pattern 14: catch(e){} without try — rating script
    // (function(){const AVG_KEY=...catch(e){}const stars=...
    // Need to add try{ before the code that has catch
    if (fixed.includes("catch(e){}const stars=") && !fixed.includes("try{")) {
      fixed = fixed.replace(/catch\(e\)\{\}const stars=/g, function() {
        modified = true;
        return "try{var saved=JSON.parse(localStorage.getItem(AVG_KEY)||'null')}catch(e){}var saved=null;const stars=";
      });
    }
    
    // Pattern 15: )) → ) at end of IIFE (extra paren)
    // clearCanonical: ...innerHTML='';}))  → innerHTML='';})
    fixed = fixed.replace(/innerHTML='';\}\)\)/g, function() {
      modified = true;
      return "innerHTML='';})";
    });
    
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
