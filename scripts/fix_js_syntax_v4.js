#!/usr/bin/env node
/**
 * Fix broken feedback/showToast scripts and other injection errors - Round 4.
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;
let checkedCount = 0;

function fixJSSyntax(html) {
  const scriptRegex = /(<script(?:\s[^>]*)?>)([\s\S]*?)(<\/script>)/gi;
  
  return html.replace(scriptRegex, function(match, openTag, code, closeTag) {
    if (openTag.includes('application/ld+json')) return match;
    if (openTag.match(/\ssrc=/i)) return match;
    if (!code.trim()) return match;
    
    let fixed = code;
    let modified = false;
    
    // Pattern: {{type:'application/json'}} → {type:'application/json'}
    fixed = fixed.replace(/\{\{type:/g, function() {
      modified = true;
      return '{type:';
    });
    fixed = fixed.replace(/\}\}/g, function(m, offset, str) {
      // Only replace }} that follows a {type: pattern context
      // Check if this is likely the Blob options closing
      if (offset > 0 && str[offset-1] !== '{') {
        modified = true;
        return '}';
      }
      return m;
    });
    
    // Pattern: '+text); → '+document.getElementById('feedback-text').value);
    fixed = fixed.replace(/'\\n\\n'\+text\);/g, function() {
      modified = true;
      return "'\\n\\n'+document.getElementById('feedback-text').value);";
    });
    fixed = fixed.replace(/\+text\)\;/g, function() {
      modified = true;
      return "+document.getElementById('feedback-text').value);";
    });
    
    // Pattern: 'loading' { → 'loading') {
    fixed = fixed.replace(/'loading'\s*\{/g, function() {
      modified = true;
      return "'loading') {";
    });
    
    // Pattern: initRating; } → initRating); }
    fixed = fixed.replace(/initRating;\s*\}/g, function() {
      modified = true;
      return "initRating); }";
    });
    
    // Pattern: )} → )})  (missing closing paren in showToast)
    // showToast("复制失败")}} → showToast("复制失败")})}
    fixed = fixed.replace(/showToast\("复制失败"\)\}\}/g, function() {
      modified = true;
      return 'showToast("复制失败")})}';
    });
    
    // Pattern: ,3000} → ,3000)}
    fixed = fixed.replace(/,3000\}/g, function() {
      modified = true;
      return ',3000)}';
    });
    
    // Pattern: ,2000;} → ,2000);}  
    fixed = fixed.replace(/,2000;\}/g, function() {
      modified = true;
      return ',2000);}';
    });
    
    // Pattern: ,2000) } → ,2000)} 
    // Already handled above
    
    // Pattern: .reason.message===){ → .reason.message===""){
    fixed = fixed.replace(/\.reason\.message===\)/g, function() {
      modified = true;
      return '.reason.message===""';
    });
    
    // Pattern: )})  at end (extra paren in IIFE)  
    // convert();})();\n})();\n → convert();})();\n
    fixed = fixed.replace(/convert\(\);\}\)\(\);\n\}\)\(\);\n/g, function() {
      modified = true;
      return 'convert();})();\n';
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
  
  if (fixedErrorCount >= origErrorCount) return;
  
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
