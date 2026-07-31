const fs = require("fs");
let html = fs.readFileSync("ai-response-parser/index.html", "utf-8");

// Fix line 225
html = html.replace(
  /content\.innerHTML=results\.json\.map\(\(j,i=>`[^`]*`\.join\('';/,
  'content.innerHTML=results.json.map((j,i)=>`<div class="result-item"><div class="result-label">JSON #${i+1} ${j.valid?"✅ 有效":"❌ 无效: "+j.error}</div><div class="result-content">${escapeHtml(j.formatted)}</div><button class="copy-btn" onclick="copyText(\'${escapeForAttr(j.formatted)}\')">📋 复制</button></div>`).join("");'
);

// Fix line 226
html = html.replace("}else if(id==='code'{", "}else if(id==='code'){");

// Fix line 227
html = html.replace(
  /content\.innerHTML=results\.code\.map\(\(c,i=>`[^`]*`\.join\('';/,
  'content.innerHTML=results.code.map((c,i)=>`<div class="result-item"><div class="result-label">代码 #${i+1} [${c.lang}]</div><div class="result-content">${escapeHtml(c.content)}</div><button class="copy-btn" onclick="copyText(\'${escapeForAttr(c.content)}\')">📋 复制</button></div>`).join("");'
);

// Fix remaining
html = html.replace("}else if(id==='list'{", "}else if(id==='list'){");
html = html.replace("}else if(id==='url'{", "}else if(id==='url'){");
html = html.replace("}else if(id==='table'{", "}else if(id==='table'){");

// Fix list join
html = html.replace(
  "results.list.map(l=>`${l.type==='task'?(l.checked?'☑':'☐':'•'} ${l.text}`.join('\\n'+'</div></div>';",
  "results.list.map(l=>`${l.type==='task'?(l.checked?'☑':'☐'):'•'} ${l.text}`).join('\\n')+'</div></div>';"
);

// Fix url join
html = html.replace(
  "results.url.join('\\n'+'</div></div>';",
  "results.url.join('\\n')+'</div></div>';"
);

// Fix table map
html = html.replace(
  "content.innerHTML=results.table.map((t,i=>`<div class=\"result-item\"><div class=\"result-label\">表格 #${i+1}</div><div class=\"result-content\">${t.headers.join(' | ')}\\n${'---|'.repeat(t.headers.length}\\n${t.rows.map(r=>r.join(' | '.join('\\n'}</div></div>`.join('';",
  "content.innerHTML=results.table.map((t,i)=>`<div class=\"result-item\"><div class=\"result-label\">表格 #${i+1}</div><div class=\"result-content\">${t.headers.join(' | ')}\\n${'---|'.repeat(t.headers.length)}\\n${t.rows.map(r=>r.join(' | ')).join('\\n')}</div></div>`).join('');"
);

fs.writeFileSync("ai-response-parser/index.html", html);
console.log("Done");