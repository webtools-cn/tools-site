#!/usr/bin/env node
// 智能JS修复器 - 用acorn解析定位错误，自动修复
const acorn = require('acorn');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKIP = new Set(['_gen','__pycache__','en','libs','js','css','scripts','tools',
  '.git','data','about','blog','privacy-policy','terms-of-service','category',
  'calc','design','dev','fun','health','image','math','media','network',
  'office','pdf','security','seo','text','utility']);

function extractJs(html) {
  const scripts = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
  const jsParts = [];
  for (const s of scripts) {
    const inner = s.replace(/<\/?script>/g, '').trim();
    if (!inner) continue;
    if (inner.startsWith('{') && (inner.includes('@context') || inner.includes('"@type"'))) continue;
    jsParts.push(inner);
  }
  return jsParts.join('\n');
}

function checkJs(js) {
  try {
    execSync('node -c -', { input: js, timeout: 5000, stdio: ['pipe','pipe','pipe'] });
    return { ok: true };
  } catch(e) {
    return { ok: false, error: e.stderr.toString() };
  }
}

function fixJs(js) {
  let fixed = js;
  
  // 1. Fix HTML closing tags in strings: </tag> → <\/tag>
  fixed = fixed.replace(/<\/(style|script|div|table|html|head|body|a|p|tr|td|th|ul|ol|li|span|IfModule|FilesMatch|VirtualHost|Directory|Location|Proxy|form|input|select|option|button|h[1-6]|header|footer|nav|section|article|main|aside|label|textarea|strong|em|b|i|pre|code|blockquote|img|br|hr|noscript|template|svg|path|g|rect|circle|line|polyline|polygon|text|tspan|defs|clipPath|filter|linearGradient|radialGradient|stop|use|symbol|mask|pattern|image|foreignObject|animate|animateTransform|animateMotion|set|mpath)>/g, '<\\/$1>');
  
  // 2. Fix HTML entities
  fixed = fixed.replace(/&nbsp;/g, ' ');
  fixed = fixed.replace(/&amp;/g, '&');
  fixed = fixed.replace(/&lt;/g, '<');
  fixed = fixed.replace(/&gt;/g, '>');
  fixed = fixed.replace(/&quot;/g, '\\"');
  
  // 3. Fix Python ternary: "X" if cond else "Y" → (cond?"X":"Y")
  fixed = fixed.replace(/"([^"]+)"\s+if\s+(\w+)\s+else\s+"([^"]+)"/g, '($2?"$1":"$3")');
  fixed = fixed.replace(/'([^']+)'\s+if\s+(\w+)\s+else\s+'([^']+)'/g, "($2?'$1':'$3')");
  
  // 4. Fix duplicate const/let declarations
  for (const kw of ['const', 'let', 'var']) {
    const re = new RegExp(kw + '\\s+(\\w+)\\s*=', 'g');
    const seen = new Set();
    let m;
    while ((m = re.exec(fixed)) !== null) {
      const name = m[1];
      if (seen.has(name)) {
        fixed = fixed.substring(0, m.index) + name + ' =' + fixed.substring(m.index + m[0].length);
        re.lastIndex = m.index + name.length + 2;
      }
      seen.add(name);
    }
  }
  
  // 5. Fix unquoted object properties with spaces/Chinese
  fixed = fixed.replace(/\{([A-Z][a-z]+\s[A-Za-z\u4e00-\u9fff\u0080-\uffff]+):/g, '{"$1":');
  
  // 6. Fix broken regex: /[!\"#$%&\'()*+,\\-./:;<=>?@[\\]^_`{|}~]/g
  fixed = fixed.replace(/\/\[!\\?"#\$%&'?\(\)\*\+,\\\\-\.\/:;<=>\?@\[\\\\\]\^_`\{\\|\}~\]\/g?/g, 
    '/[!"#$%&\'()*+,\\\\-./:;<=>?@[\\\\]^_`{|}~]/g');
  
  // 7. Fix </ in template literals that break HTML parsing  
  // Already handled by #1
  
  // 8. Fix 'double declining' as object key
  fixed = fixed.replace(/double declining:/g, '"double declining":');
  
  // 9. Fix catch without parens: catch{ → catch(e){
  fixed = fixed.replace(/catch\s*\{/g, 'catch(e){');
  
  // 10. Fix if(ternary); → ternary;
  fixed = fixed.replace(/if\s*\(\s*(\w+)\s*\?\s*/g, '$1 ? ');
  
  // 11. Fix broken ternary: ==='sqlite'?'sqlite':'sqlite' → ==='sqlite'?'sqlite':'sqlite'
  // This is valid but wrong logic - skip
  
  // 12. Fix < in JS that's not in strings (comparison operators)
  // Already handled by \x3C replacement in prior commit
  
  // 13. Fix unclosed strings at end of line
  // Too risky to auto-fix
  
  return fixed;
}

// Main
const baseDir = '/home/chison/tools-site';
const dirs = fs.readdirSync(baseDir).filter(d => {
  if (SKIP.has(d) || d.startsWith('.')) return false;
  return fs.existsSync(path.join(baseDir, d, 'index.html'));
});

let ok = 0, broken = 0, fixed = 0;
const stillBroken = [];

for (const d of dirs) {
  const f = path.join(baseDir, d, 'index.html');
  const html = fs.readFileSync(f, 'utf8');
  const js = extractJs(html);
  if (!js) continue;
  
  const r = checkJs(js);
  if (r.ok) { ok++; continue; }
  
  broken++;
  
  // Try fixing
  const fixedJs = fixJs(js);
  if (fixedJs === js) {
    stillBroken.push(d);
    continue;
  }
  
  // Apply fix to HTML
  let newHtml = html;
  const scripts = html.match(/<script>[\s\S]*?<\/script>/g) || [];
  for (const s of scripts) {
    const inner = s.replace(/<\/?script>/g, '').trim();
    if (!inner) continue;
    if (inner.startsWith('{') && (inner.includes('@context') || inner.includes('"@type"'))) continue;
    const fixedInner = fixJs(inner);
    if (fixedInner !== inner) {
      newHtml = newHtml.replace(s, '<script>' + fixedInner + '</script>');
    }
  }
  
  if (newHtml !== html) {
    fs.writeFileSync(f, newHtml);
    const newJs = extractJs(newHtml);
    const r2 = checkJs(newJs);
    if (r2.ok) {
      fixed++;
      console.log(`✅ ${d}`);
    } else {
      fs.writeFileSync(f, html); // revert
      stillBroken.push(d);
    }
  } else {
    stillBroken.push(d);
  }
}

console.log(`\nOK: ${ok}, Fixed: ${fixed}, Still broken: ${stillBroken.length}`);
if (stillBroken.length > 0) {
  console.log('Still broken:');
  for (const t of stillBroken) console.log(`  ❌ ${t}`);
}
