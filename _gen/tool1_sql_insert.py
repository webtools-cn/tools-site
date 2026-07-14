#!/usr/bin/env python3
"""Generate sql-insert-generator pages (CN + EN)."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "sql-insert-generator"
DATE = "2026-07-14"

# ===== CN PAGE =====
cn_title = "SQL INSERT语句生成器 - 在线生成INSERT·批量数据·纯前端"
cn_desc = "免费在线SQL INSERT语句生成器。从表结构或CSV数据一键生成INSERT INTO语句，支持批量生成、自定义表名、字段映射。纯前端本地处理，数据不上传服务器。"
cn_kw = "SQL INSERT生成器,INSERT语句生成,SQL数据生成,批量INSERT,SQL工具,数据库工具"
cn_schema_name = "SQL INSERT语句生成器"
cn_schema_desc = cn_desc

cn_faqs = [
    ("SQL INSERT语句生成器支持哪些数据库？", "生成标准SQL INSERT语法，兼容MySQL、PostgreSQL、SQLite、SQL Server、Oracle等主流数据库。可选择是否包含反引号、方括号等数据库特定引用符号。"),
    ("如何批量生成INSERT语句？", "在输入框中粘贴多行数据（CSV格式或自定义分隔符），工具会自动为每行数据生成一条INSERT语句。支持自定义批量大小和事务包装。"),
    ("生成的INSERT语句可以直接在数据库执行吗？", "可以。生成的SQL语句遵循标准语法，可直接复制到数据库客户端执行。建议先在测试环境验证，确认字段映射和数据类型正确。"),
    ("数据会发送到服务器吗？", "不会。所有数据处理均在浏览器本地完成，你的表结构和数据绝不会上传到任何服务器。即使断网也能正常使用。"),
    ("支持哪些输入格式？", "支持CSV、TSV、自定义分隔符文本、手动输入字段名和数据。也可从JSON数组自动转换。支持拖拽文件导入。"),
    ("如何处理特殊字符和SQL注入？", "工具自动对单引号、反斜杠等特殊字符进行转义处理，防止SQL注入。数值类型不添加引号，字符串类型自动加引号。"),
]

faq_json_cn = make_faq_json(cn_faqs)

cn_content = f"""{head_start(cn_title, cn_desc, cn_kw, f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc, f"https://free-toolbase.com/{SLUG}/", cn_schema_name, cn_schema_desc, faq_json_cn, "zh", SLUG)}

<div class="tool-section">
<h2>🔧 SQL INSERT语句生成器 <span class="badge">零依赖·可离线</span></h2>
<p>{cn_desc}</p>
<div class="options-area">
<div class="option-row">
<label>表名: <input type="text" id="tableName" value="users" style="width:150px"></label>
<label>分隔符: <select id="delimiter"><option value=",">逗号(,)</option><option value="&#9;">制表符(Tab)</option><option value="|">竖线(|)</option><option value=";">分号(;)</option></select></label>
<label><input type="checkbox" id="useBacktick" checked> 反引号</label>
<label><input type="checkbox" id="wrapTransaction"> 事务包装</label>
<label><input type="checkbox" id="includeDrop"> 添加DROP TABLE</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">字段名（第一行）+ 数据行</label>
<textarea id="input" placeholder="id,name,email,age&#10;1,张三,zhang@example.com,25&#10;2,李四,li@example.com,30"></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的SQL</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成INSERT</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载SQL</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>SQL INSERT语句生成器能做什么？</h2>
<p>SQL INSERT语句生成器是一款免费的在线工具，帮助开发者和数据库管理员快速生成标准SQL INSERT语句。无需手动编写繁琐的INSERT语法，只需粘贴数据即可批量生成，大幅提升数据库初始化和数据迁移效率。纯前端处理，数据绝不上传服务器。</p>

<h2>核心功能</h2>
<ul>
<li><strong>批量INSERT生成</strong>：从CSV/TSV数据一键生成多条INSERT语句，支持自定义分隔符</li>
<li><strong>智能类型识别</strong>：自动识别数值、字符串、日期等类型，数值不加引号，字符串自动转义</li>
<li><strong>自定义表名和字段</strong>：灵活指定目标表名，首行自动识别为字段名</li>
<li><strong>事务包装</strong>：可选BEGIN/COMMIT事务包装，保证批量插入的原子性</li>
<li><strong>特殊字符转义</strong>：自动处理单引号、反斜杠等SQL特殊字符，防止注入</li>
</ul>

<h2>使用教程</h2>
<ol>
<li><strong>输入字段名</strong>：在文本框第一行输入字段名（逗号分隔），如 id,name,email,age</li>
<li><strong>输入数据行</strong>：从第二行开始，每行一条记录，字段间用相同分隔符分隔</li>
<li><strong>配置选项</strong>：设置表名、分隔符类型、是否使用反引号等</li>
<li><strong>点击生成</strong>：点击"生成INSERT"按钮，右侧立即显示SQL语句</li>
<li><strong>复制或下载</strong>：复制生成的SQL到剪贴板，或下载为.sql文件</li>
</ol>

<h2>应用场景</h2>
<h3>场景1：数据库初始化</h3>
<p>开发新项目时，需要快速创建测试数据。使用本工具从CSV数据批量生成INSERT语句，一键初始化数据库，省去手动编写每条INSERT的繁琐工作。</p>
<h3>场景2：数据迁移</h3>
<p>从Excel或CSV导出数据后，需要导入到数据库。本工具将CSV数据直接转换为INSERT语句，无需导入向导，粘贴即用。</p>
<h3>场景3：测试数据生成</h3>
<p>测试人员需要构造大量测试数据。使用本工具快速生成INSERT语句，配合事务包装确保数据一致性。</p>
<h3>场景4：教学演示</h3>
<p>数据库课程教学中，教师可以快速生成示例INSERT语句，让学生直观理解SQL语法结构。</p>

<h2>扩展知识</h2>
<p>SQL INSERT语句是数据库操作中最基本的DML语句之一。标准语法为 INSERT INTO table_name (column1, column2) VALUES (value1, value2)。批量INSERT（多行VALUES）比逐条INSERT性能更高，因为减少了网络往返和事务开销。MySQL支持INSERT INTO ... VALUES (...),(...),(...) 多行语法，单次可插入数千行。对于大规模数据导入，建议使用LOAD DATA INFILE（MySQL）或COPY命令（PostgreSQL）获得最佳性能。</p>
</div>

{faq_html(cn_faqs, "zh")}
{footer("zh", SLUG, "SQL INSERT语句生成器")}
<script>
function loadExample(){{
document.getElementById('input').value='id,name,email,age,created_at\\n1,张三,zhang@example.com,25,2024-01-15\\n2,李四,li@example.com,30,2024-02-20\\n3,王五,wang@example.com\\'s,28,2024-03-10\\n4,赵六,zhao@example.com,35,2024-04-05';
execute();
}}
function clearInput(){{document.getElementById('input').value='';document.getElementById('output').textContent='等待生成...'}}
function escapeSql(s){{return s.replace(/'/g,"''")}}
function isNumeric(v){{return v!==''&&!isNaN(v)&&isFinite(v)}}
function execute(){{
var raw=document.getElementById('input').value.trim();
if(!raw){{showToast('请输入数据');return}}
var tableName=document.getElementById('tableName').value||'table1';
var delim=document.getElementById('delimiter').value;
var useBacktick=document.getElementById('useBacktick').checked;
var wrapTx=document.getElementById('wrapTransaction').checked;
var includeDrop=document.getElementById('includeDrop').checked;
var lines=raw.split('\\n');
if(lines.length<2){{showToast('至少需要字段名行和一行数据');return}}
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
showToast('生成完成，共'+(lines.length-1)+'条INSERT');
}}
function downloadOutput(){{
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){{showToast('请先生成SQL');return}}
downloadText('insert_statements.sql',text);
}}
window.addEventListener('load',function(){{loadExample()}});
</script>
</body></html>"""

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_content)
print(f"Written: {SLUG}/index.html ({len(cn_content)} bytes)")
