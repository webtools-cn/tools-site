#!/usr/bin/env node
/**
 * Fix broken related-tools scripts where HTML was injected into JS string literals.
 * Also fix other remaining JS syntax errors.
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;

function fixRelatedToolsScript(code) {
  // The pattern is: JS string literal gets interrupted by injected HTML
  // Original: var h = '<div class="related-tools-inner">...' + (en ? '...' : '...') + '...</div>';
  // Broken: HTML tags appear inside the string concatenation
  
  // Strategy: Find the related-tools script and replace with a clean version
  if (!code.includes('related-tools-section')) return code;
  
  // Check if it has syntax errors
  try { new Function(code); return code; } catch(e) {}
  
  // Replace the entire related-tools IIFE with a clean version
  const cleanRelatedTools = `(function() {
  'use strict';
  var s = document.getElementById('related-tools-section');
  if (!s) return;
  var p = window.location.pathname;
  var en = p.indexOf('/en/') !== -1;
  p = p.replace(/\\/en\\//g, '/');
  var slug = p.split('/').filter(Boolean).pop() || '';
  if (!slug) { s.innerHTML = ''; return; }
  var depth = en ? '../../' : '../';
  var u = depth + 'related-tools.json';
  fetch(u).then(function(r) {
    if (!r.ok) throw new Error('not found');
    return r.json();
  }).then(function(d) {
    var data = en ? d.en : d.cn;
    var t = data[slug];
    if (!t || !t.related || !t.related.length) { s.innerHTML = ''; return; }
    var h = '\\x3Cdiv class="related-tools-inner">\\x3Ch3 class="related-tools-title">'
      + (en ? 'You May Also Like' : '相关工具推荐')
      + '\\x3C/h3>\\x3Cdiv class="related-tools-grid">';
    t.related.forEach(function(r) {
      var link = en ? '../../en/' + r.slug + '/' : '../' + r.slug + '/';
      h += '\\x3Ca href="' + link + '" class="related-tool-card">'
        + '\\x3Cspan class="related-tool-icon">' + (r.icon || '🔧') + '\\x3C/span>'
        + '\\x3Cspan class="related-tool-name">' + r.name + '\\x3C/span>\\x3C/a>';
    });
    h += '\\x3C/div>\\x3C/div>';
    s.innerHTML = h;
  }).catch(function() { s.innerHTML = ''; });
})();`;
  
  // Find and replace the related-tools IIFE
  // Pattern: (function() { 'use strict'; var s = document.getElementById('related-tools-section' ... })();
  const relatedToolsRegex = /\(function\(\)\s*\{\s*'use strict';\s*var\s+s\s*=\s*document\.getElementById\('related-tools-section'[\s\S]*?\}\)\(\);?/;
  
  let fixed = code.replace(relatedToolsRegex, cleanRelatedTools);
  
  if (fixed !== code) return fixed;
  
  return code;
}

function fixFile(filepath) {
  if (!fs.existsSync(filepath)) return;
  const html = fs.readFileSync(filepath, 'utf8');
  const scriptRegex = /(<script(?:\s[^>]*)?>)([\s\S]*?)(<\/script>)/gi;
  
  let modified = false;
  let newHtml = html.replace(scriptRegex, function(match, openTag, code, closeTag) {
    if (openTag.includes('application/ld+json')) return match;
    if (openTag.match(/\ssrc=/i)) return match;
    if (!code.trim()) return match;
    
    // Check if has error
    try { new Function(code); return match; } catch(e) {}
    
    let fixed = code;
    
    // Fix related-tools script
    if (code.includes('related-tools-section')) {
      fixed = fixRelatedToolsScript(code);
    }
    
    // Fix: ,2000;} → ,2000);} (showToast missing paren)
    if (fixed.includes(',2000;}')) {
      fixed = fixed.replace(/,2000;\}/g, ',2000);}');
    }
    
    // Fix: ,3000} → ,3000)} (showToast missing paren)
    if (fixed.includes(',3000}')) {
      fixed = fixed.replace(/,3000\}/g, ',3000)}');
    }
    
    // Fix: ,2200} → ,2200)}
    if (fixed.includes(',2200}')) {
      fixed = fixed.replace(/,2200\}/g, ',2200)}');
    }
    
    // Fix: ,2500} → ,2500)}
    if (fixed.includes(',2500}')) {
      fixed = fixed.replace(/,2500\}/g, ',2500)}');
    }
    
    // Fix: ,2000; } → ,2000); }
    if (fixed.includes(',2000; }')) {
      fixed = fixed.replace(/,2000;\s*\}/g, ',2000); }');
    }
    
    // Fix: message===){ → message===""){
    if (fixed.includes('===)')) {
      fixed = fixed.replace(/\.reason\.message===\)/g, '.reason.message===""');
    }
    
    // Fix: .label.width + 40; → .label.width + 40);
    if (fixed.includes('.width + 40;')) {
      fixed = fixed.replace(/\.width\s*\+\s*40;/g, '.width + 40);');
    }
    
    // Fix: showToast("复制失败")}} → showToast("复制失败")})}
    if (fixed.includes('复制失败")}}')) {
      fixed = fixed.replace(/showToast\("复制失败"\)\}\}/g, 'showToast("复制失败")})}');
    }
    
    // Fix: })} at end → })() (IIFE close)
    if (fixed.match(/\}\)\}\s*$/)) {
      fixed = fixed.replace(/\}\)\}\s*$/, '})();');
    }
    
    // Fix: ;}) → ;) (extra paren)
    if (fixed.match(/;\}\)\s*$/)) {
      // Check if this is an IIFE that's not properly closed
      // Skip - might break valid code
    }
    
    if (fixed !== code) {
      // Verify fix
      try {
        new Function(fixed);
        modified = true;
        return openTag + fixed + closeTag;
      } catch(e) {
        // Check if at least reduced errors
        return match;
      }
    }
    
    return match;
  });
  
  if (modified) {
    fs.writeFileSync(filepath, newHtml, 'utf8');
    fixedCount++;
    console.log('FIXED: ' + filepath);
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

console.log('\nTotal fixed: ' + fixedCount);
