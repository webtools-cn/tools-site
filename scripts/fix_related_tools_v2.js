#!/usr/bin/env node
/**
 * Fix related-tools scripts that have HTML before the script tag,
 * and missing IIFE wrapper.
 */

const fs = require('fs');
const path = require('path');

let fixedCount = 0;

const CLEAN_RELATED_TOOLS = `(function() {
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

function fixFile(filepath) {
  if (!fs.existsSync(filepath)) return;
  const html = fs.readFileSync(filepath, 'utf8');
  const scriptRegex = /(<script(?:\s[^>]*)?>)([\s\S]*?)(<\/script>)/gi;
  
  let modified = false;
  let newHtml = html.replace(scriptRegex, function(match, openTag, code, closeTag) {
    if (openTag.includes('application/ld+json')) return match;
    if (openTag.match(/\ssrc=/i)) return match;
    if (!code.trim()) return match;
    
    // Check for syntax errors
    try { new Function(code); return match; } catch(e) {}
    
    let fixed = code;
    
    // Fix 1: If code starts with HTML (like <div ...>), remove the HTML part
    // and fix the JS
    if (fixed.match(/^\s*<div/) || fixed.match(/^\s*<section/)) {
      // Remove HTML tags from the beginning
      fixed = fixed.replace(/^[\s\S]*?(?=\n\s*['"]use strict|n\s*var\s+s\s*=)/, '');
    }
    
    // Fix 2: If code has 'use strict' without IIFE wrapper, add wrapper
    if (fixed.includes("'use strict';") && !fixed.includes('(function()')) {
      // Check if this is a related-tools script
      if (fixed.includes('related-tools-section')) {
        // Replace entire content with clean version
        fixed = CLEAN_RELATED_TOOLS;
      }
    }
    
    // Fix 3: If code has 'showToast' function followed by related-tools code
    // without proper IIFE, fix it
    if (fixed.includes('related-tools-section') && fixed.includes('showToast')) {
      // Split: keep showToast, replace related-tools part
      const showToastMatch = fixed.match(/^(function showToast[\s\S]*?}\n)/);
      if (showToastMatch) {
        fixed = showToastMatch[1] + '\n' + CLEAN_RELATED_TOOLS;
      } else {
        // Just replace with clean version
        fixed = CLEAN_RELATED_TOOLS;
      }
    }
    
    // Fix 4: Missing IIFE wrapper - code has 'var s = document.getElementById' at top level
    if (fixed.includes("var s = document.getElementById('related-tools-section'") && 
        !fixed.includes('(function()')) {
      fixed = CLEAN_RELATED_TOOLS;
    }
    
    if (fixed !== code) {
      try {
        new Function(fixed);
        modified = true;
        return openTag + fixed + closeTag;
      } catch(e) {
        // Still has errors, but might be better
        // Check if related-tools is the main content
        if (fixed.includes('related-tools-section')) {
          // Just use clean version
          fixed = CLEAN_RELATED_TOOLS;
          try {
            new Function(fixed);
            modified = true;
            return openTag + fixed + closeTag;
          } catch(e2) {}
        }
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
