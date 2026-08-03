#!/usr/bin/env node
/**
 * Fix common JS syntax errors in HTML files that cause Google Failing URLs.
 * 
 * Common patterns:
 * 1. (function(){ // comment var x = ... → comment eats code on same line
 * 2. })(;) → should be })();
 * 3. ,3000)} at start of script (broken showToast fragments)
 * 4. }(</script> → should be })();</script>
 * 5. window.addEventListener('load',function(){...}; → missing )
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;
let checkedCount = 0;
let stillBroken = 0;

function fixJSSyntax(html) {
  // Extract all <script> blocks (not JSON-LD, not external)
  const scriptRegex = /(<script(?:\s[^>]*)?>)([\s\S]*?)(<\/script>)/gi;
  
  return html.replace(scriptRegex, function(match, openTag, code, closeTag) {
    // Skip JSON-LD and external scripts
    if (openTag.includes('application/ld+json')) return match;
    if (openTag.match(/\ssrc=/i)) return match;
    if (!code.trim()) return match;
    
    let fixed = code;
    let modified = false;
    
    // Fix 1: (function(){ // comment var x → (function(){ var x
    // The comment eats the rest of the line including code
    fixed = fixed.replace(/\(function\(\)\{\s*\/\/\s*resultAddCopy\s+var\s/g, function(m) {
      modified = true;
      return '(function(){ var ';
    });
    
    // Fix 2: })(;) → })();
    if (fixed.includes('})(;)')) {
      fixed = fixed.replace(/\}\)\(;\)/g, function() {
        modified = true;
        return '})();';
      });
    }
    
    // Fix 3: }(</script> → })();\n</script>  (IIFE not properly closed)
    // Already handled in specific files
    
    // Fix 4: ,3000)} at start of script → proper showToast function
    if (fixed.match(/^\s*,3000\)\}/)) {
      fixed = fixed.replace(/^\s*,3000\)\}/, 'function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},3000)}');
      modified = true;
    }
    
    // Fix 5: window.addEventListener('load',function(){...};  (missing closing paren)
    fixed = fixed.replace(/window\.addEventListener\('load',function\(\)\{([^}]+)\};/, function(m, body) {
      modified = true;
      return "window.addEventListener('load',function(){" + body + "});";
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
  
  if (fixed === html) return; // No changes
  
  // Verify the fix actually resolves JS errors
  const scripts = fixed.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
  let origErrorCount = 0;
  let fixedErrorCount = 0;
  
  // Check original for errors
  const origScripts = html.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
  origScripts.forEach((s, i) => {
    if (s.includes('application/ld+json')) return;
    if (s.match(/<script\s+[^>]*src=/i)) return;
    const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
    if (!code.trim()) return;
    try { new Function(code); } catch(e) { origErrorCount++; }
  });
  
  if (origErrorCount === 0) return; // Was already fine
  
  // Check fixed version
  scripts.forEach((s, i) => {
    if (s.includes('application/ld+json')) return;
    if (s.match(/<script\s+[^>]*src=/i)) return;
    const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
    if (!code.trim()) return;
    try { new Function(code); } catch(e) { fixedErrorCount++; }
  });
  
  // Only write if we reduced errors (don't require zero errors)
  if (fixedErrorCount >= origErrorCount) {
    stillBroken++;
    return; // Fix didn't help
  }
  
  // Write the fix
  fs.writeFileSync(filepath, fixed, 'utf8');
  fixedCount++;
  console.log('FIXED: ' + filepath + ' (' + origErrorCount + ' → ' + fixedErrorCount + ' errors)');
}

// Process all HTML files
function processDir(dir, isEn) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir);
  for (const entry of entries) {
    if (entry.startsWith('.')) continue;
    if (entry === 'node_modules' || entry === 'scripts' || entry === 'quality' || 
        entry === 'css' || entry === 'js' || entry === '.gsc-data') continue;
    const fullpath = path.join(dir, entry);
    if (fs.statSync(fullpath).isDirectory()) {
      const htmlFile = path.join(fullpath, 'index.html');
      if (fs.existsSync(htmlFile)) {
        checkFile(htmlFile);
      }
    }
  }
}

// Check homepage
checkFile('index.html');
checkFile('en/index.html');

// Process all tool directories
processDir('.', false);
processDir('en', true);

console.log('\n=== Summary ===');
console.log('Checked: ' + checkedCount + ' files');
console.log('Fixed: ' + fixedCount + ' files');
console.log('Still broken: ' + stillBroken + ' files');
