#!/usr/bin/env node
/**
 * Remove broken rating injection scripts that cause JS syntax errors.
 * These scripts were injected by a batch script but have corrupted syntax.
 * Pattern: contains 'initRating' and 'catch(e)' without 'try'
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;
let checkedCount = 0;

function isBrokenRatingScript(code) {
  // Check if this is a broken rating script
  if (!code.includes('initRating') && !code.includes('AVG_KEY')) return false;
  
  // Check if it has syntax errors
  try {
    new Function(code);
    return false; // Valid syntax, don't remove
  } catch(e) {
    return true; // Has syntax errors, should remove
  }
}

function fixFile(filepath) {
  if (!fs.existsSync(filepath)) return;
  checkedCount++;
  
  const html = fs.readFileSync(filepath, 'utf8');
  const scriptRegex = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi;
  
  let modified = false;
  let newHtml = html.replace(scriptRegex, function(match, code) {
    // Skip JSON-LD and external scripts
    if (match.includes('application/ld+json')) return match;
    if (match.match(/<script\s+[^>]*src=/i)) return match;
    if (!code.trim()) return match;
    
    if (isBrokenRatingScript(code)) {
      modified = true;
      return ''; // Remove the broken script
    }
    
    return match;
  });
  
  if (modified) {
    // Verify we didn't break anything else
    const origScripts = html.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
    let origErrors = 0;
    origScripts.forEach((s) => {
      if (s.includes('application/ld+json')) return;
      if (s.match(/<script\s+[^>]*src=/i)) return;
      const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
      if (!code.trim()) return;
      try { new Function(code); } catch(e) { origErrors++; }
    });
    
    const newScripts = newHtml.match(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi) || [];
    let newErrors = 0;
    newScripts.forEach((s) => {
      if (s.includes('application/ld+json')) return;
      if (s.match(/<script\s+[^>]*src=/i)) return;
      const code = s.replace(/<script(?:\s[^>]*)?>/, '').replace(/<\/script>/, '');
      if (!code.trim()) return;
      try { new Function(code); } catch(e) { newErrors++; }
    });
    
    if (newErrors < origErrors) {
      fs.writeFileSync(filepath, newHtml, 'utf8');
      fixedCount++;
      console.log('FIXED: ' + filepath + ' (' + origErrors + ' → ' + newErrors + ' errors)');
    }
  }
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
      if (fs.existsSync(htmlFile)) fixFile(htmlFile);
    }
  }
}

fixFile('index.html');
fixFile('en/index.html');
processDir('.');
processDir('en');

console.log('\n=== Summary ===');
console.log('Checked: ' + checkedCount + ' files');
console.log('Fixed: ' + fixedCount + ' files');
