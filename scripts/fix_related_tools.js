#!/usr/bin/env node
/**
 * Replace all broken related-tools scripts with a clean version.
 * These scripts have HTML injected into JS string literals.
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
    
    // Check if this script contains related-tools-section
    if (!code.includes('related-tools-section')) return match;
    
    // Check if it has syntax errors
    try { new Function(code); return match; } catch(e) {}
    
    // Has errors and contains related-tools-section
    // Replace the related-tools IIFE portion
    // Find the start of the related-tools code
    const patterns = [
      // Pattern: (function() { ... related-tools-section ... })();
      /\(function\(\)\s*\{[\s\S]*?related-tools-section[\s\S]*?\}\)\(\);?/,
      // Pattern: var s = document.getElementById('related-tools-section' ... until end
      /var\s+s\s*=\s*document\.getElementById\('related-tools-section'[\s\S]*$/,
      // Pattern: (function(){ ... related-tools-section ... })  (no semicolon)
    ];
    
    let fixed = code;
    for (const pattern of patterns) {
      const newFixed = fixed.replace(pattern, CLEAN_RELATED_TOOLS);
      if (newFixed !== fixed) {
        fixed = newFixed;
        break;
      }
    }
    
    // If pattern didn't match, try replacing the whole script block
    // (only if it's primarily a related-tools script)
    if (fixed === code) {
      // Check if the script is mostly related-tools code
      if (code.length < 3000 && code.includes('related-tools-section') && code.includes('fetch')) {
        fixed = CLEAN_RELATED_TOOLS;
      }
    }
    
    if (fixed !== code) {
      try {
        new Function(fixed);
        modified = true;
        return openTag + fixed + closeTag;
      } catch(e) {
        // Still broken, but let's try writing it anyway if it's better
        // Count errors
        let oldErr = 0, newErr = 0;
        try { new Function(code); } catch(e2) { oldErr = 1; }
        try { new Function(fixed); } catch(e2) { newErr = 1; }
        if (newErr < oldErr) {
          modified = true;
          return openTag + fixed + closeTag;
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
