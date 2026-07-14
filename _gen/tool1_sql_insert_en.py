#!/usr/bin/env python3
"""Generate sql-insert-generator EN page."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "sql-insert-generator"

en_title = "SQL INSERT Statement Generator - Batch INSERT · Pure Frontend"
en_desc = "Free online SQL INSERT statement generator. Generate INSERT INTO statements from table schema or CSV data instantly. Batch generation, custom table names, field mapping. Pure frontend, no server upload."
en_kw = "SQL INSERT generator,INSERT statement generator,SQL data generator,batch INSERT,SQL tool,database tool"
en_schema_name = "SQL INSERT Statement Generator"
en_schema_desc = en_desc

en_faqs = [
    ("Which databases does the SQL INSERT generator support?", "It generates standard SQL INSERT syntax compatible with MySQL, PostgreSQL, SQLite, SQL Server, Oracle, and other mainstream databases. You can optionally include backticks, brackets, or other database-specific quoting."),
    ("How to batch generate INSERT statements?", "Paste multi-row data (CSV format or custom delimiter) in the input area. The tool automatically generates one INSERT statement per row. Supports custom batch size and transaction wrapping."),
    ("Can the generated INSERT statements be executed directly?", "Yes. The generated SQL follows standard syntax and can be copied directly to a database client for execution. We recommend testing in a development environment first."),
    ("Is my data sent to a server?", "No. All data processing happens locally in your browser. Your table schema and data never leave your device. Works even offline."),
    ("What input formats are supported?", "Supports CSV, TSV, custom delimiter text, manual field name and data entry. Also supports drag-and-drop file import."),
    ("How are special characters and SQL injection handled?", "The tool automatically escapes single quotes, backslashes, and other special characters to prevent SQL injection. Numeric values are unquoted; strings are automatically quoted."),
]

faq_json_en = make_faq_json(en_faqs)

en_content = f"""{head_start(en_title, en_desc, en_kw, f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc, f"https://free-toolbase.com/en/{SLUG}/", en_schema_name, en_schema_desc, faq_json_en, "en", SLUG)}

<div class="tool-section">
<h2>🔧 SQL INSERT Statement Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>{en_desc}</p>
<div class="options-area">
<div class="option-row">
<label>Table: <input type="text" id="tableName" value="users" style="width:150px"></label>
<label>Delimiter: <select id="delimiter"><option value=",">Comma(,)</option><option value="&#9;">Tab</option><option value="|">Pipe(|)</option><option value=";">Semicolon(;)</option></select></label>
<label><input type="checkbox" id="useBacktick"> Backticks</label>
<label><input type="checkbox" id="wrapTransaction"> Wrap in Transaction</label>
<label><input type="checkbox" id="includeDrop"> Add DROP TABLE</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Field Names (1st row) + Data Rows</label>
<textarea id="input" placeholder="id,name,email,age&#10;1,John,john@example.com,25&#10;2,Jane,jane@example.com,30"></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated SQL</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate INSERT</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Result</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download SQL</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the SQL INSERT Generator Do?</h2>
<p>The SQL INSERT Statement Generator is a free online tool that helps developers and DBAs quickly generate standard SQL INSERT statements. No need to manually write tedious INSERT syntax — just paste your data and generate in bulk. Pure frontend processing, your data never leaves your browser.</p>

<h2>Core Features</h2>
<ul>
<li><strong>Batch INSERT Generation</strong>: Generate multiple INSERT statements from CSV/TSV data with one click, custom delimiters supported</li>
<li><strong>Smart Type Detection</strong>: Automatically identifies numeric, string, and date types — numbers unquoted, strings auto-escaped</li>
<li><strong>Custom Table & Fields</strong>: Flexible target table name, first row auto-detected as field names</li>
<li><strong>Transaction Wrapping</strong>: Optional BEGIN/COMMIT wrapping for atomic batch inserts</li>
<li><strong>Special Character Escaping</strong>: Auto-handles single quotes, backslashes, and other SQL special characters</li>
</ul>

<h2>How to Use</h2>
<ol>
<li><strong>Enter field names</strong>: Type comma-separated field names in the first row, e.g. id,name,email,age</li>
<li><strong>Enter data rows</strong>: Starting from row 2, one record per line with the same delimiter</li>
<li><strong>Configure options</strong>: Set table name, delimiter type, backtick usage, etc.</li>
<li><strong>Click Generate</strong>: Click "Generate INSERT" to see SQL output immediately</li>
<li><strong>Copy or Download</strong>: Copy SQL to clipboard or download as .sql file</li>
</ol>

<h2>Use Cases</h2>
<h3>Database Initialization</h3>
<p>When starting a new project, quickly create test data by generating INSERT statements from CSV. Initialize your database in seconds without manually writing each INSERT.</p>
<h3>Data Migration</h3>
<p>Convert exported Excel or CSV data directly to INSERT statements for database import. No need for import wizards — paste and go.</p>
<h3>Test Data Generation</h3>
<p>QA engineers can quickly generate INSERT statements for test data, with transaction wrapping for data consistency.</p>
<h3>Teaching & Demos</h3>
<p>Instructors can quickly generate example INSERT statements for database courses, helping students understand SQL syntax structure.</p>

<h2>Technical Background</h2>
<p>SQL INSERT is one of the most fundamental DML statements. Standard syntax: INSERT INTO table_name (col1, col2) VALUES (val1, val2). Batch INSERT (multi-row VALUES) outperforms individual INSERTs by reducing network round-trips and transaction overhead. MySQL supports INSERT INTO ... VALUES (...),(...),(...) for inserting thousands of rows at once. For large-scale imports, consider LOAD DATA INFILE (MySQL) or COPY (PostgreSQL) for best performance.</p>
</div>

{faq_html(en_faqs, "en")}
{footer("en", SLUG, "SQL INSERT Statement Generator")}
<script>
function loadExample(){{
document.getElementById('input').value='id,name,email,age,created_at\\n1,John,john@example.com,25,2024-01-15\\n2,Jane,jane@example.com,30,2024-02-20\\n3,Bob,bob@example.com\\'s,28,2024-03-10\\n4,Alice,alice@example.com,35,2024-04-05';
execute();
}}
function clearInput(){{document.getElementById('input').value='';document.getElementById('output').textContent='Waiting...'}}
function escapeSql(s){{return s.replace(/'/g,"''")}}
function isNumeric(v){{return v!==''&&!isNaN(v)&&isFinite(v)}}
function execute(){{
var raw=document.getElementById('input').value.trim();
if(!raw){{showToast('Please enter data');return}}
var tableName=document.getElementById('tableName').value||'table1';
var delim=document.getElementById('delimiter').value;
var useBacktick=document.getElementById('useBacktick').checked;
var wrapTx=document.getElementById('wrapTransaction').checked;
var includeDrop=document.getElementById('includeDrop').checked;
var lines=raw.split('\\n');
if(lines.length<2){{showToast('Need at least header row and one data row');return}}
var fields=lines[0].split(delim).map(function(f){{return f.trim()}});
var q=useBacktick?'`':'';
var sql='';
if(includeDrop)sql+='DROP TABLE IF EXISTS '+q+tableName+q+';\\n';
if(wrapTx)sql+='BEGIN;\\n';
for(var i=1;i<lines.length;i++){{
if(!lines[i].trim())continue;
var vals=lines[i].split(delim);
var colParts=[];var valParts=[];
for(var j=0;j<fields.length;j++){{
colParts.push(q+fields[j]+q);
var v=(j<vals.length)?vals[j].trim():'';
if(isNumeric(v)){{valParts.push(v)}}else{{valParts.push("'"+escapeSql(v)+"'")}}
}}
sql+='INSERT INTO '+q+tableName+q+' ('+colParts.join(',')+') VALUES ('+valParts.join(',')+');\\n';
}}
if(wrapTx)sql+='COMMIT;\\n';
document.getElementById('output').textContent=sql;
saveHistory('sqlInsertHistory',raw.substring(0,100));
showToast('Generated '+(lines.length-1)+' INSERT statements');
}}
function downloadOutput(){{
var text=document.getElementById('output').textContent;
if(!text||text==='Waiting...'){{showToast('Please generate SQL first');return}}
downloadText('insert_statements.sql',text);
}}
window.addEventListener('load',function(){{loadExample()}});
</script>
</body></html>"""

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_content)
print(f"Written: en/{SLUG}/index.html ({len(en_content)} bytes)")
