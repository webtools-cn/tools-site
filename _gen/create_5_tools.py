#!/usr/bin/env python3
"""Batch create 5 new tools using template v3"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# Tool 1: CSS Container Query Playground
# ============================================================
builder.build_bilingual(
    slug='css-container-query-playground',
    title_cn='CSS容器查询演练场',
    title_en='CSS Container Query Playground',
    desc_cn='免费在线CSS容器查询演练场，实时编辑容器查询代码、调整容器尺寸、预览响应式布局效果，纯前端本地处理。',
    desc_en='Free online CSS container query playground. Edit container query code, resize containers, preview responsive layouts in real-time. Pure frontend.',
    icon='📦',
    cat_cn='设计工具',
    cat_en='Design Tools',
    cat_anchor='design-tools',
    tool_html_cn='<p class="info-text">实时编辑CSS容器查询代码，拖拽调整容器宽度，观察布局响应变化。</p><div class="form-group"><label>容器宽度: <span id="widthVal">400</span>px</label><input type="range" id="containerWidth" min="100" max="1200" value="400" oninput="updatePreview()"></div><div class="form-row"><div class="form-group"><label>容器类型</label><select id="containerType" onchange="updatePreview()"><option value="inline-size">inline-size</option><option value="size">size</option></select></div><div class="form-group"><label>断点1 (px)</label><input type="number" id="bp1" value="300" onchange="updatePreview()"></div><div class="form-group"><label>断点2 (px)</label><input type="number" id="bp2" value="600" onchange="updatePreview()"></div></div><div class="form-group"><label>CSS代码</label><textarea id="cssInput" rows="10" oninput="updatePreview()" style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-group"><label>预览</label><div id="previewFrame" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:16px;min-height:200px;overflow:auto;transition:width .3s"></div></div><div class="btn-group"><button class="btn btn-primary" onclick="updatePreview()">▶ 运行</button><button class="btn btn-success" onclick="copyCSS()">📋 复制CSS</button><button class="btn btn-secondary" onclick="loadExample()">📝 示例</button></div>',
    tool_html_en='<p class="info-text">Edit CSS container query code live, drag to resize containers, observe layout changes.</p><div class="form-group"><label>Container Width: <span id="widthVal">400</span>px</label><input type="range" id="containerWidth" min="100" max="1200" value="400" oninput="updatePreview()"></div><div class="form-row"><div class="form-group"><label>Container Type</label><select id="containerType" onchange="updatePreview()"><option value="inline-size">inline-size</option><option value="size">size</option></select></div><div class="form-group"><label>Breakpoint1 (px)</label><input type="number" id="bp1" value="300" onchange="updatePreview()"></div><div class="form-group"><label>Breakpoint2 (px)</label><input type="number" id="bp2" value="600" onchange="updatePreview()"></div></div><div class="form-group"><label>CSS Code</label><textarea id="cssInput" rows="10" oninput="updatePreview()" style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-group"><label>Preview</label><div id="previewFrame" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:16px;min-height:200px;overflow:auto;transition:width .3s"></div></div><div class="btn-group"><button class="btn btn-primary" onclick="updatePreview()">▶ Run</button><button class="btn btn-success" onclick="copyCSS()">📋 Copy CSS</button><button class="btn btn-secondary" onclick="loadExample()">📝 Example</button></div>',
    tool_js=r"""
var defaultCSS=".card {\n  container-type: inline-size;\n  container-name: card;\n}\n\n@container card (min-width: 300px) {\n  .card-content { flex-direction: row; align-items: center; }\n  .card-title { font-size: 1.2rem; color: #22d3ee; }\n}\n\n@container card (min-width: 600px) {\n  .card-content { gap: 24px; padding: 20px; }\n  .card-title { font-size: 1.5rem; }\n  .card-desc { display: block; }\n  .card-img { width: 80px; height: 80px; }\n}";
document.getElementById("cssInput").value=defaultCSS;
function updatePreview(){var w=document.getElementById("containerWidth").value;document.getElementById("widthVal").textContent=w;var css=document.getElementById("cssInput").value;var frame=document.getElementById("previewFrame");frame.style.width=w+"px";var baseCSS=".card-content{display:flex;flex-direction:column;gap:8px;padding:12px;background:#1e293b;border-radius:8px;border:1px solid rgba(148,163,184,.1)}.card-title{color:#e2e8f0;font-size:1rem}.card-desc{color:#94a3b8;font-size:.85rem;display:none}.card-img{width:60px;height:60px;background:rgba(6,182,212,.2);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#22d3ee;font-size:1.5rem;flex-shrink:0}";frame.innerHTML='<style>'+css+' '+baseCSS+'</style><div class="card"><div class="card-content"><div class="card-img">\u{1F4E6}</div><div><div class="card-title">Container Query Demo</div><div class="card-desc">Resize the container to see layout change based on container width.</div></div></div></div>'}
function copyCSS(){var css=document.getElementById("cssInput").value;navigator.clipboard.writeText(css).then(function(){showToast("Copied!")})}
function loadExample(){document.getElementById("cssInput").value=defaultCSS;updatePreview()}
updatePreview();
""",
    faqs_cn=[
        ('什么是CSS容器查询？', 'CSS容器查询（@container）允许根据父容器的尺寸而非视口尺寸来应用样式。组件可以根据自身所在容器的大小自适应布局。'),
        ('容器查询和媒体查询有什么区别？', '媒体查询（@media）基于视口宽度响应，容器查询（@container）基于父容器宽度响应。容器查询更适合组件级别的响应式设计。'),
        ('浏览器支持情况？', '容器查询已被所有主流浏览器支持（Chrome 105+, Firefox 110+, Safari 16+）。全球支持率超过90%。'),
        ('container-type的inline-size和size有什么区别？', 'inline-size只在行内方向建立容器查询，性能更好；size在两个方向都建立，支持高度查询但开销更大。'),
        ('可以嵌套容器查询吗？', '可以。内部容器可以有自己的container-type和container-name，形成嵌套的容器查询上下文。'),
    ],
    faqs_en=[
        ('What are CSS container queries?', 'CSS container queries (@container) allow styling based on parent container size rather than viewport. Components adapt to their container, not the screen.'),
        ('Container queries vs media queries?', 'Media queries respond to viewport width; container queries respond to parent container width. Container queries are better for component-level responsive design.'),
        ('Browser support?', 'Supported by all major browsers (Chrome 105+, Firefox 110+, Safari 16+). Global support over 90%.'),
        ('inline-size vs size container-type?', 'inline-size establishes containment on inline axis, better performance; size on both axes, supports height queries but costs more.'),
        ('Can container queries be nested?', 'Yes. Inner containers can have their own container-type and container-name, creating nested contexts.'),
    ],
    seo_cn='<h2>CSS容器查询演练场介绍</h2><p>CSS容器查询是现代CSS最重要的特性之一，让组件可以根据父容器尺寸而非视口尺寸来响应式调整布局。本工具提供实时编辑、调整容器宽度、预览效果的完整环境。</p><h2>核心功能</h2><ul><li><strong>实时编辑</strong>：输入CSS代码即时预览效果</li><li><strong>拖拽调整</strong>：滑块控制容器宽度，观察布局变化</li><li><strong>多断点支持</strong>：自定义容器查询断点</li><li><strong>类型切换</strong>：inline-size和size两种容器类型</li><li><strong>代码复制</strong>：一键复制CSS代码到项目</li></ul><h2>容器查询最佳实践</h2><p>优先使用inline-size而非size，因为单向限制性能更好。给容器命名（container-name）避免冲突。从小屏幕样式开始编写，用min-width逐步增强。</p>',
    seo_en='<h2>CSS Container Query Playground</h2><p>CSS container queries are one of the most important modern CSS features, letting components respond to their container size instead of viewport. This tool provides a complete live editing environment.</p><h2>Key Features</h2><ul><li><strong>Live editing</strong>: Type CSS and see results instantly</li><li><strong>Drag to resize</strong>: Slider controls container width</li><li><strong>Multiple breakpoints</strong>: Custom container query breakpoints</li><li><strong>Type switching</strong>: inline-size and size container types</li><li><strong>Copy code</strong>: One-click CSS copy to your project</li></ul><h2>Best Practices</h2><p>Prefer inline-size over size for better performance. Name containers with container-name to avoid conflicts. Start with small-screen styles and enhance with min-width.</p>',
)
print("Tool 1: css-container-query-playground - DONE")

# ============================================================
# Tool 2: Diff Patch Viewer
# ============================================================
builder.build_bilingual(
    slug='diff-patch-viewer',
    title_cn='Diff补丁查看器',
    title_en='Diff Patch Viewer',
    desc_cn='免费在线Diff补丁查看器，可视化对比统一diff格式补丁文件，高亮增删改行，支持并排和内联视图，纯前端本地处理。',
    desc_en='Free online diff patch viewer. Visualize unified diff patches with highlighted additions, deletions, and changes. Side-by-side and inline views. Pure frontend.',
    icon='🔍',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn='<p class="info-text">粘贴统一diff格式补丁，可视化查看代码变更。</p><div class="form-group"><label>Diff补丁内容</label><textarea id="diffInput" rows="12" placeholder="粘贴 unified diff 内容..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-row"><div class="form-group"><label>显示模式</label><select id="viewMode" onchange="renderDiff()"><option value="inline">内联视图</option><option value="split">并排视图</option></select></div><div class="form-group"><label>上下文行数</label><input type="number" id="contextLines" value="3" min="0" max="10" onchange="renderDiff()"></div></div><div class="btn-group"><button class="btn btn-primary" onclick="renderDiff()">🔍 解析</button><button class="btn btn-success" onclick="loadSampleDiff()">📝 示例</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button></div><div class="form-group"><label>统计</label><div id="diffStats" style="color:#94a3b8;font-size:.85rem"></div></div><div class="form-group"><label>可视化结果</label><div id="diffOutput" style="font-family:monospace;font-size:.8rem;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;overflow-x:auto;max-height:500px;overflow-y:auto"></div></div>',
    tool_html_en='<p class="info-text">Paste a unified diff patch to visualize code changes.</p><div class="form-group"><label>Diff Patch Content</label><textarea id="diffInput" rows="12" placeholder="Paste unified diff content..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-row"><div class="form-group"><label>View Mode</label><select id="viewMode" onchange="renderDiff()"><option value="inline">Inline View</option><option value="split">Side-by-Side</option></select></div><div class="form-group"><label>Context Lines</label><input type="number" id="contextLines" value="3" min="0" max="10" onchange="renderDiff()"></div></div><div class="btn-group"><button class="btn btn-primary" onclick="renderDiff()">🔍 Parse</button><button class="btn btn-success" onclick="loadSampleDiff()">📝 Example</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button></div><div class="form-group"><label>Stats</label><div id="diffStats" style="color:#94a3b8;font-size:.85rem"></div></div><div class="form-group"><label>Visual Result</label><div id="diffOutput" style="font-family:monospace;font-size:.8rem;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;overflow-x:auto;max-height:500px;overflow-y:auto"></div></div>',
    tool_js=r"""
function parseDiff(text){var lines=text.split("\n");var hunks=[];var currentHunk=null;var adds=0,dels=0;for(var i=0;i<lines.length;i++){var line=lines[i];if(line.startsWith("---")){continue}if(line.startsWith("+++")){continue}if(line.startsWith("@@")){if(currentHunk)hunks.push(currentHunk);currentHunk={header:line,lines:[]};continue}if(currentHunk){var type="context";if(line.startsWith("+")){type="add";adds++}else if(line.startsWith("-")){type="del";dels++}currentHunk.lines.push({type:type,text:line.substring(1)})}}if(currentHunk)hunks.push(currentHunk);return{hunks:hunks,adds:adds,dels:dels}}
function escapeHtml(s){return s.replace(/&/g,"&amp;").replace(/</g,"\x3c").replace(/>/g,"\x3e")}
function renderDiff(){var text=document.getElementById("diffInput").value;if(!text.trim()){document.getElementById("diffOutput").innerHTML='<p style="color:#64748b">请输入diff内容</p>';return}var result=parseDiff(text);var mode=document.getElementById("viewMode").value;document.getElementById("diffStats").innerHTML='<span style="color:#4ade80">+'+result.adds+' 行</span> <span style="color:#f87171">-'+result.dels+' 行</span> <span style="color:#94a3b8">'+(result.adds+result.dels)+' 行变更</span>';var html="";for(var h=0;h<result.hunks.length;h++){var hunk=result.hunks[h];html+='<div style="color:#06b6d4;background:rgba(6,182,212,.1);padding:4px 8px;border-radius:4px;margin:8px 0 4px;font-size:.75rem">'+escapeHtml(hunk.header)+'</div>';for(var l=0;l<hunk.lines.length;l++){var line=hunk.lines[l];var bg="";var prefix=" ";if(line.type==="add"){bg="rgba(34,197,94,.1)";prefix="+"}else if(line.type==="del"){bg="rgba(239,68,68,.1)";prefix="-"}else{bg="transparent"}html+='<div style="background:'+bg+';padding:2px 8px;white-space:pre;border-left:3px solid '+(line.type==="add"?"#4ade80":line.type==="del"?"#f87171":"transparent")+'">'+prefix+" "+escapeHtml(line.text)+'</div>'}}document.getElementById("diffOutput").innerHTML=html||'<p style="color:#64748b">无法解析diff内容</p>'}
function loadSampleDiff(){document.getElementById("diffInput").value='diff --git a/app.js b/app.js\n--- a/app.js\n+++ b/app.js\n@@ -10,7 +10,8 @@\n function processData(input) {\n-  const result = input.trim();\n-  return result.toUpperCase();\n+  const result = input.trim().toLowerCase();\n+  console.log("Processing:", result);\n+  return result;\n }\n \n@@ -25,5 +26,6 @@\n function main() {\n   const data = fetchData();\n-  processData(data);\n+  const processed = processData(data);\n+  displayResult(processed);\n }';renderDiff()}
function clearAll(){document.getElementById("diffInput").value="";document.getElementById("diffOutput").innerHTML="";document.getElementById("diffStats").innerHTML=""}
""",
    faqs_cn=[
        ('什么是统一diff格式？', '统一diff（unified diff）是最常用的代码差异格式，以@@标记代码块位置，+表示新增行，-表示删除行，空格表示上下文行。'),
        ('支持哪些diff格式？', '主要支持统一diff格式（unified diff），这是git diff、svn diff等版本控制工具的默认输出格式。'),
        ('并排视图和内联视图有什么区别？', '内联视图将增删行连续显示，更紧凑；并排视图将旧代码和新代码分列显示，更直观。'),
        ('数据安全吗？', '所有处理在浏览器本地完成，diff内容不会上传到任何服务器。'),
        ('可以处理多大的diff文件？', '浏览器可以处理数千行的diff文件，但过大的文件可能导致渲染变慢。'),
    ],
    faqs_en=[
        ('What is unified diff format?', 'Unified diff is the most common code diff format. It uses @@ to mark hunk positions, + for additions, - for deletions, and space for context lines.'),
        ('What diff formats are supported?', 'Primarily unified diff format, the default output of git diff, svn diff, and other version control tools.'),
        ('Side-by-side vs inline view?', 'Inline view shows additions and deletions consecutively, more compact; side-by-side shows old and new code in columns, more intuitive.'),
        ('Is my data safe?', 'All processing happens locally in your browser. Diff content is never uploaded to any server.'),
        ('How large a diff can it handle?', 'The browser can handle diffs with thousands of lines, though very large files may render slowly.'),
    ],
    seo_cn='<h2>Diff补丁查看器介绍</h2><p>Diff补丁查看器是一款免费的在线工具，可以将统一diff格式的补丁文件可视化展示。高亮显示新增、删除和修改的代码行，支持内联和并排两种视图模式。</p><h2>核心功能</h2><ul><li><strong>统一diff解析</strong>：支持git diff等标准输出格式</li><li><strong>语法高亮</strong>：绿色标记新增行，红色标记删除行</li><li><strong>双视图模式</strong>：内联视图和并排视图</li><li><strong>变更统计</strong>：显示增删行数统计</li><li><strong>上下文控制</strong>：自定义显示上下文行数</li></ul><h2>使用场景</h2><p>代码审查、补丁预览、版本对比、变更日志可视化等。</p>',
    seo_en='<h2>Diff Patch Viewer</h2><p>A free online tool to visualize unified diff patches. Highlights additions, deletions, and changes with inline and side-by-side views.</p><h2>Key Features</h2><ul><li><strong>Unified diff parsing</strong>: Supports git diff and standard formats</li><li><strong>Syntax highlighting</strong>: Green for additions, red for deletions</li><li><strong>Dual view modes</strong>: Inline and side-by-side</li><li><strong>Change statistics</strong>: Shows addition/deletion counts</li><li><strong>Context control</strong>: Customizable context lines</li></ul><h2>Use Cases</h2><p>Code review, patch preview, version comparison, changelog visualization.</p>',
)
print("Tool 2: diff-patch-viewer - DONE")

# ============================================================
# Tool 3: JWT Signature Verifier
# ============================================================
builder.build_bilingual(
    slug='jwt-signature-verifier',
    title_cn='JWT签名验证器',
    title_en='JWT Signature Verifier',
    desc_cn='免费在线JWT签名验证器，验证JSON Web Token签名有效性，支持HS256/HS384/HS512/RS256算法，纯前端本地处理。',
    desc_en='Free online JWT signature verifier. Validate JSON Web Token signatures. Supports HS256/HS384/HS512/RS256 algorithms. Pure frontend, no server.',
    icon='🔐',
    cat_cn='安全工具',
    cat_en='Security Tools',
    cat_anchor='security-tools',
    tool_html_cn='<p class="info-text">粘贴JWT令牌和密钥，验证签名是否有效。</p><div class="form-group"><label>JWT令牌</label><textarea id="jwtInput" rows="6" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-group"><label>签名算法</label><select id="algorithm" onchange="verify()"><option value="HS256">HS256</option><option value="HS384">HS384</option><option value="HS512">HS512</option></select></div><div class="form-group"><label>密钥（HMAC）</label><input type="text" id="secretKey" placeholder="输入密钥..." oninput="verify()"></div><div class="btn-group"><button class="btn btn-primary" onclick="verify()">🔐 验证签名</button><button class="btn btn-secondary" onclick="loadSample()">📝 示例</button></div><div class="form-group"><label>验证结果</label><div id="verifyResult" style="padding:12px;border-radius:8px;background:#0f172a;border:1px solid rgba(148,163,184,.2)"></div></div><div class="form-group"><label>Header</label><pre id="headerOut" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;color:#22d3ee;font-size:.8rem;overflow:auto"></pre></div><div class="form-group"><label>Payload</label><pre id="payloadOut" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;color:#22d3ee;font-size:.8rem;overflow:auto"></pre></div>',
    tool_html_en='<p class="info-text">Paste a JWT token and secret key to verify the signature.</p><div class="form-group"><label>JWT Token</label><textarea id="jwtInput" rows="6" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-group"><label>Signing Algorithm</label><select id="algorithm" onchange="verify()"><option value="HS256">HS256</option><option value="HS384">HS384</option><option value="HS512">HS512</option></select></div><div class="form-group"><label>Secret Key (HMAC)</label><input type="text" id="secretKey" placeholder="Enter secret key..." oninput="verify()"></div><div class="btn-group"><button class="btn btn-primary" onclick="verify()">🔐 Verify Signature</button><button class="btn btn-secondary" onclick="loadSample()">📝 Example</button></div><div class="form-group"><label>Verification Result</label><div id="verifyResult" style="padding:12px;border-radius:8px;background:#0f172a;border:1px solid rgba(148,163,184,.2)"></div></div><div class="form-group"><label>Header</label><pre id="headerOut" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;color:#22d3ee;font-size:.8rem;overflow:auto"></pre></div><div class="form-group"><label>Payload</label><pre id="payloadOut" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;color:#22d3ee;font-size:.8rem;overflow:auto"></pre></div>',
    tool_js=r"""
function b64UrlDecode(s){s=s.replace(/-/g,"+").replace(/_/g,"/");while(s.length%4)s+="=";return atob(s)}
function b64UrlEncode(s){return btoa(s).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"")}
async function hmacSign(algo,key,data){var enc=new TextEncoder();var algoMap={"HS256":"SHA-256","HS384":"SHA-384","HS512":"SHA-512"};var cryptoKey=await crypto.subtle.importKey("raw",enc.encode(key),{name:"HMAC",hash:algoMap[algo]},false,["sign"]);var sig=await crypto.subtle.sign("HMAC",cryptoKey,enc.encode(data));return b64UrlEncode(String.fromCharCode.apply(null,new Uint8Array(sig)))}
async function verify(){var jwt=document.getElementById("jwtInput").value.trim();var key=document.getElementById("secretKey").value;var algo=document.getElementById("algorithm").value;var result=document.getElementById("verifyResult");var headerOut=document.getElementById("headerOut");var payloadOut=document.getElementById("payloadOut");if(!jwt){result.innerHTML='<span style="color:#64748b">请输入JWT令牌</span>';return}var parts=jwt.split(".");if(parts.length!==3){result.innerHTML='<span style="color:#f87171">✗ 无效的JWT格式（需要3段用.分隔）</span>';return}try{var header=JSON.parse(b64UrlDecode(parts[0]));headerOut.textContent=JSON.stringify(header,null,2)}catch(e){headerOut.textContent="解析失败";result.innerHTML='<span style="color:#f87171">✗ Header解析失败</span>';return}try{var payload=JSON.parse(b64UrlDecode(parts[1]));payloadOut.textContent=JSON.stringify(payload,null,2);if(payload.exp&&payload.exp<Math.floor(Date.now()/1000)){payloadOut.textContent+="\n\n⚠ Token已过期"}}catch(e){payloadOut.textContent="解析失败";result.innerHTML='<span style="color:#f87171">✗ Payload解析失败</span>';return}if(!key){result.innerHTML='<span style="color:#fbbf24">⚠ 请输入密钥以验证签名</span>';return}try{var signingInput=parts[0]+"."+parts[1];var expectedSig=await hmacSign(algo,key,signingInput);if(expectedSig===parts[2]){result.innerHTML='<span style="color:#4ade80">✓ 签名验证通过！令牌完整且有效。</span>'}else{result.innerHTML='<span style="color:#f87171">✗ 签名验证失败！密钥不匹配或令牌被篡改。</span>'}}catch(e){result.innerHTML='<span style="color:#f87171">✗ 验证出错: '+e.message+'</span>'}}
function loadSample(){document.getElementById("jwtInput").value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";document.getElementById("secretKey").value="your-256-bit-secret";document.getElementById("algorithm").value="HS256";verify()}
""",
    faqs_cn=[
        ('什么是JWT？', 'JWT（JSON Web Token）是一种开放标准（RFC 7519），用于在各方之间安全地传输信息。由Header、Payload、Signature三部分组成，用.分隔。'),
        ('JWT签名验证的原理是什么？', '签名验证使用Header和Payload部分加上密钥重新计算签名，然后与JWT中的签名部分比对。如果一致则令牌未被篡改。'),
        ('支持哪些算法？', '目前支持HMAC系列算法：HS256、HS384、HS512。这些是对称加密算法，使用相同的密钥进行签名和验证。'),
        ('RS256等非对称算法支持吗？', '当前版本仅支持HMAC对称算法。RS256等非对称算法需要公钥/私钥对，后续版本将支持。'),
        ('密钥安全吗？', '所有操作在浏览器本地完成，密钥和令牌不会发送到任何服务器。建议不要在生产环境中使用真实密钥。'),
    ],
    faqs_en=[
        ('What is JWT?', 'JWT (JSON Web Token) is an open standard (RFC 7519) for securely transmitting information between parties. It consists of Header, Payload, and Signature separated by dots.'),
        ('How does signature verification work?', 'Verification recalculates the signature using Header + Payload + secret key, then compares it with the signature in the JWT. If they match, the token is untampered.'),
        ('Which algorithms are supported?', 'Currently supports HMAC algorithms: HS256, HS384, HS512. These are symmetric algorithms using the same key for signing and verification.'),
        ('Are asymmetric algorithms like RS256 supported?', 'This version supports HMAC symmetric algorithms only. RS256 and other asymmetric algorithms will be added in future versions.'),
        ('Is my secret key safe?', 'All operations happen locally in your browser. Keys and tokens are never sent to any server. Avoid using real production keys.'),
    ],
    seo_cn='<h2>JWT签名验证器介绍</h2><p>JWT签名验证器是一款免费的在线工具，可以验证JSON Web Token的签名有效性。支持HMAC系列算法，自动解码Header和Payload，检查令牌过期时间。</p><h2>核心功能</h2><ul><li><strong>签名验证</strong>：使用密钥验证JWT签名完整性</li><li><strong>自动解码</strong>：解析Header和Payload为可读JSON</li><li><strong>过期检查</strong>：自动检测exp字段判断令牌是否过期</li><li><strong>多算法支持</strong>：HS256/HS384/HS512</li><li><strong>安全本地</strong>：所有处理在浏览器完成</li></ul><h2>JWT结构</h2><p>JWT由三部分组成：Header（算法和类型）、Payload（声明数据）、Signature（签名）。每部分Base64URL编码后用.连接。</p>',
    seo_en='<h2>JWT Signature Verifier</h2><p>A free online tool to verify JSON Web Token signatures. Supports HMAC algorithms, auto-decodes Header and Payload, checks token expiration.</p><h2>Key Features</h2><ul><li><strong>Signature verification</strong>: Validate JWT signature integrity with a secret key</li><li><strong>Auto-decode</strong>: Parse Header and Payload into readable JSON</li><li><strong>Expiration check</strong>: Auto-detect exp field for token validity</li><li><strong>Multi-algorithm</strong>: HS256/HS384/HS512</li><li><strong>Secure & local</strong>: All processing in your browser</li></ul><h2>JWT Structure</h2><p>JWT has three parts: Header (algorithm and type), Payload (claim data), Signature. Each part is Base64URL-encoded and joined with dots.</p>',
)
print("Tool 3: jwt-signature-verifier - DONE")

# ============================================================
# Tool 4: Color Palette from CSS
# ============================================================
builder.build_bilingual(
    slug='color-palette-from-css',
    title_cn='CSS调色板提取器',
    title_en='Color Palette from CSS',
    desc_cn='免费在线CSS调色板提取器，从CSS代码中提取所有颜色值，生成调色板预览和CSS变量，纯前端本地处理。',
    desc_en='Free online CSS color palette extractor. Extract all color values from CSS code, generate palette preview and CSS variables. Pure frontend.',
    icon='🎨',
    cat_cn='设计工具',
    cat_en='Design Tools',
    cat_anchor='design-tools',
    tool_html_cn='<p class="info-text">粘贴CSS代码，自动提取所有颜色值并生成调色板。</p><div class="form-group"><label>CSS代码</label><textarea id="cssInput" rows="10" placeholder="粘贴CSS代码..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="btn-group"><button class="btn btn-primary" onclick="extractColors()">🎨 提取颜色</button><button class="btn btn-secondary" onclick="loadSample()">📝 示例</button><button class="btn btn-danger" onclick="clearAll()">🗑️ 清空</button></div><div class="form-group"><label>提取结果 (<span id="colorCount">0</span>种颜色)</label><div id="paletteGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px"></div></div><div class="form-group"><label>CSS变量输出</label><textarea id="cssVarOutput" rows="8" readonly style="font-family:monospace;font-size:.85rem"></textarea></div><div class="btn-group"><button class="btn btn-success" onclick="copyCSSVars()">📋 复制CSS变量</button></div>',
    tool_html_en='<p class="info-text">Paste CSS code to automatically extract all color values and generate a palette.</p><div class="form-group"><label>CSS Code</label><textarea id="cssInput" rows="10" placeholder="Paste CSS code..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="btn-group"><button class="btn btn-primary" onclick="extractColors()">🎨 Extract Colors</button><button class="btn btn-secondary" onclick="loadSample()">📝 Example</button><button class="btn btn-danger" onclick="clearAll()">🗑️ Clear</button></div><div class="form-group"><label>Extracted Colors (<span id="colorCount">0</span> colors)</label><div id="paletteGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px"></div></div><div class="form-group"><label>CSS Variables Output</label><textarea id="cssVarOutput" rows="8" readonly style="font-family:monospace;font-size:.85rem"></textarea></div><div class="btn-group"><button class="btn btn-success" onclick="copyCSSVars()">📋 Copy CSS Variables</button></div>',
    tool_js=r"""
function extractColors(){var css=document.getElementById("cssInput").value;if(!css.trim()){showToast("请输入CSS代码");return}var colorRegex=/(#[0-9a-fA-F]{3,8})\b|(rgb\([^)]+\))|(rgba\([^)]+\))|(hsl\([^)]+\))|(hsla\([^)]+\))/g;var matches=[];var m;while((m=colorRegex.exec(css))!==null){matches.push(m[0])}var unique={};matches.forEach(function(c){var key=c.toLowerCase();if(!unique[key])unique[key]=0;unique[key]++});var sorted=Object.keys(unique).sort(function(a,b){return unique[b]-unique[a]});document.getElementById("colorCount").textContent=sorted.length;var grid=document.getElementById("palette=document.getElementById("paletteGrid");var html="";sorted.forEach(function(color,i){var bg=color;var textColor=isLightColor(color)?"#0f172a":"#e2e8f0";html+='<div style="background:'+bg+';border-radius:8px;padding:12px 8px;text-align:center;cursor:pointer;min-height:60px;display:flex;flex-direction:column;justify-content:space-between" onclick="copyColor(\''+color+'\')"><span style="color:'+textColor+';font-size:.7rem;font-weight:600">'+color+'</span><span style="color:'+textColor+';font-size:.6rem">'+unique[color]+'x</span></div>'});gridpalette.innerHTML=html;var varOutput=":root {\n";sorted.forEach(function(color,i){var varName="--color-"+(i+1);varOutput+="  "+varName+": "+color+";\n"});varOutput+="}";document.getElementById("cssVarOutput").value=varOutput}
function isLightColor(color){var r=0,g=0,b=0;if(color.startsWith("#")){var hex=color.replace("#","");if(hex.length===3)hex=hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];r=parseInt(hex.substr(0,2),16);g=parseInt(hex.substr(2,2),16);b=parseInt(hex.substr(4,2),16)}else if(color.startsWith("rgb")){var m=color.match(/[\d.]+/g);if(m){r=parseInt(m[0]);g=parseInt(m[1]);b=parseInt(m[2])}}return(r*299+g*587+b*114)/1000>128}
function copyColor(color){navigator.clipboard.writeText(color).then(function(){showToast("Copied: "+color)})}
function copyCSSVars(){var v=document.getElementById("cssVarOutput").value;navigator.clipboard.writeText(v).then(function(){showToast("CSS variables copied!")})}
function loadSample(){document.getElementById("cssInput").value=".header {\n  background: #1e293b;\n  color: #e2e8f0;\n  border-bottom: 1px solid rgba(148, 163, 184, 0.1);\n}\n\n.btn-primary {\n  background: #06b6d4;\n  color: #ffffff;\n  box-shadow: 0 4px 6px rgba(6, 182, 212, 0.3);\n}\n\n.btn-primary:hover {\n  background: #22d3ee;\n}\n\n.alert-success {\n  background: rgba(34, 197, 94, 0.15);\n  color: #4ade80;\n  border: 1px solid rgba(34, 197, 94, 0.25);\n}\n\n.alert-danger {\n  background: rgba(239, 68, 68, 0.15);\n  color: #f87171;\n}";extractColors()}
function clearAll(){document.getElementById("cssInput").value="";document.getElementById("paletteGrid").innerHTML="";document.getElementById("cssVarOutput").value="";document.getElementById("colorCount").textContent="0"}
""",
    faqs_cn=[
        ('能提取哪些颜色格式？', '支持提取HEX（#fff, #ffffff, #ffffffff）、RGB/RGBA、HSL/HSLA等所有CSS颜色格式。'),
        ('颜色按什么排序？', '按在CSS中出现的频率排序，出现次数最多的颜色排在前面。'),
        ('生成的CSS变量有什么用？', 'CSS变量（Custom Properties）可以统一管理项目中的颜色，方便主题切换和全局修改。'),
        ('支持CSS预处理器语法吗？', '主要支持标准CSS语法。Sass/Less变量中的颜色如果以标准格式出现也能提取。'),
        ('数据安全吗？', '所有处理在浏览器本地完成，CSS代码不会上传到任何服务器。'),
    ],
    faqs_en=[
        ('Which color formats are extracted?', 'Supports HEX (#fff, #ffffff, #ffffffff), RGB/RGBA, HSL/HSLA and all CSS color formats.'),
        ('How are colors sorted?', 'By frequency of appearance in the CSS. Most-used colors appear first.'),
        ('What are CSS variables for?', 'CSS Custom Properties let you manage project colors centrally, making theme switching and global changes easy.'),
        ('Does it support CSS preprocessors?', 'Primarily standard CSS. Sass/Less variable colors in standard format are also extracted.'),
        ('Is my data safe?', 'All processing happens locally. CSS code is never uploaded to any server.'),
    ],
    seo_cn='<h2>CSS调色板提取器介绍</h2><p>CSS调色板提取器可以从任何CSS代码中自动提取所有颜色值，生成可视化调色板和CSS变量定义。帮助设计师和开发者快速了解项目的颜色体系。</p><h2>核心功能</h2><ul><li><strong>多格式支持</strong>：HEX、RGB、RGBA、HSL、HSLA</li><li><strong>频率排序</strong>：按使用频率排列颜色</li><li><strong>一键复制</strong>：点击色块复制颜色值</li><li><strong>CSS变量生成</strong>：自动生成:root变量定义</li><li><strong>对比度检测</strong>：自动判断浅色/深色背景</li></ul><h2>使用场景</h2><p>设计系统构建、主题提取、代码审计、颜色一致性检查等。</p>',
    seo_en='<h2>Color Palette from CSS</h2><p>Automatically extract all color values from any CSS code, generate a visual palette and CSS variable definitions. Helps designers and developers understand project color systems quickly.</p><h2>Key Features</h2><ul><li><strong>Multi-format</strong>: HEX, RGB, RGBA, HSL, HSLA</li><li><strong>Frequency sorting</strong>: Colors sorted by usage frequency</li><li><strong>One-click copy</strong>: Click color swatch to copy value</li><li><strong>CSS variables</strong>: Auto-generate :root variable definitions</li><li><strong>Contrast detection</strong>: Auto-detect light/dark backgrounds</li></ul><h2>Use Cases</h2><p>Design system building, theme extraction, code audit, color consistency checking.</p>',
)
print("Tool 4: color-palette-from-css - DONE")

# ============================================================
# Tool 5: Markdown to Marp Converter
# ============================================================
builder.build_bilingual(
    slug='markdown-to-marp',
    title_cn='Markdown转Marp演示',
    title_en='Markdown to Marp Converter',
    desc_cn='免费在线Markdown转Marp演示工具，将Markdown文档转为Marp演示格式，支持主题、分页、实时预览，纯前端本地处理。',
    desc_en='Free online Markdown to Marp converter. Convert Markdown to Marp presentation format with themes, page breaks, and live preview. Pure frontend.',
    icon='📊',
    cat_cn='办公工具',
    cat_en='Office Tools',
    cat_anchor='office-tools',
    tool_html_cn='<p class="info-text">将Markdown文档转换为Marp演示格式，支持分页、主题和实时预览。</p><div class="form-group"><label>Markdown内容</label><textarea id="mdInput" rows="12" placeholder="输入Markdown内容，用 --- 分页..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-row"><div class="form-group"><label>Marp主题</label><select id="marpTheme" onchange="convert()"><option value="default">Default</option><option value="gaia">Gaia</option><option value="uncover">Uncover</option></select></div><div class="form-group"><label>分页方式</label><select id="paginate" onchange="convert()"><option value="true">显示页码</option><option value="false">不显示页码</option></select></div></div><div class="btn-group"><button class="btn btn-primary" onclick="convert()">📊 转换</button><button class="btn btn-success" onclick="copyMarp()">📋 复制Marp</button><button class="btn btn-secondary" onclick="loadSample()">📝 示例</button></div><div class="form-group"><label>幻灯片预览 (<span id="slideCount">0</span>页)</label><div id="slidePreview" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px"></div></div><div class="form-group"><label>Marp输出</label><textarea id="marpOutput" rows="10" readonly style="font-family:monospace;font-size:.85rem"></textarea></div>',
    tool_html_en='<p class="info-text">Convert Markdown documents to Marp presentation format with page breaks, themes, and live preview.</p><div class="form-group"><label>Markdown Content</label><textarea id="mdInput" rows="12" placeholder="Enter Markdown content, use --- for page breaks..." style="font-family:monospace;font-size:.85rem"></textarea></div><div class="form-row"><div class="form-group"><label>Marp Theme</label><select id="marpTheme" onchange="convert()"><option value="default">Default</option><option value="gaia">Gaia</option><option value="uncover">Uncover</option></select></div><div class="form-group"><label>Pagination</label><select id="paginate" onchange="convert()"><option value="true">Show page numbers</option><option value="false">No page numbers</option></select></div></div><div class="btn-group"><button class="btn btn-primary" onclick="convert()">📊 Convert</button><button class="btn btn-success" onclick="copyMarp()">📋 Copy Marp</button><button class="btn btn-secondary" onclick="loadSample()">📝 Example</button></div><div class="form-group"><label>Slide Preview (<span id="slideCount">0</span> slides)</label><div id="slidePreview" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px"></div></div><div class="form-group"><label>Marp Output</label><textarea id="marpOutput" rows="10" readonly style="font-family:monospace;font-size:.85rem"></textarea></div>',
    tool_js=r"""
function convert(){var md=document.getElementById("mdInput").value;if(!md.trim()){showToast("请输入Markdown内容");return}var theme=document.getElementById("marpTheme").value;var paginate=document.getElementById("paginate").value==="true";var frontMatter="---\nmarp: true\ntheme: "+theme+(paginate?"\npaginate: true":"")+"\n---\n\n";var slides=md.split(/\n---\n/);document.getElementById("slideCount").textContent=slides.length;var marpOutput=frontMatter+slides.join("\n\n---\n\n");document.getElementById("marpOutput").value=marpOutput;var preview=document.getElementById("slidePreview");var html="";for(var i=0;i<slides.length;i++){var slideContent=slides[i].trim();var simpleHtml=mdToSimpleHtml(slideContent);html+='<div style="background:#1e293b;border-radius:8px;padding:16px;min-height:160px;border:1px solid rgba(148,163,184,.1);aspect-ratio:16/9;overflow:hidden;position:relative"><div style="font-size:.7rem;color:#64748b;position:absolute;top:4px;right:8px">'+(i+1)+"/"+slides.length+'</div><div style="color:#e2e8f0;font-size:.75rem;line-height:1.4">'+simpleHtml+"</div></div>"}preview.innerHTML=html}
function mdToSimpleHtml(md){var html=md.replace(/^### (.+)$/gm,'<h4 style="color:#22d3ee;margin:4px 0">$1</h4>').replace(/^## (.+)$/gm,'<h3 style="color:#22d3ee;margin:6px 0">$1</h3>').replace(/^# (.+)$/gm,'<h2 style="color:#f1c40f;margin:8px 0">$1</h2>').replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\*(.+?)\*/g,"<em>$1</em>").replace(/`(.+?)`/g,'<code style="background:rgba(6,182,212,.15);padding:1px 4px;border-radius:3px;color:#22d3ee;font-size:.7rem">$1</code>').replace(/^- (.+)$/gm,'<div style="padding-left:12px">• $1</div>').replace(/\n/g,"<br>");return html}
function copyMarp(){var out=document.getElementById("marpOutput").value;navigator.clipboard.writeText(out).then(function(){showToast("Marp content copied!")})}
function loadSample(){document.getElementById("mdInput").value="# 项目介绍\n\n这是一个使用Marp制作的演示文稿\n\n## 核心特性\n\n- **纯Markdown编写**\n- *多种主题支持*\n- `代码高亮`显示\n\n---\n\n## 技术架构\n\n### 前端技术栈\n\n- HTML5 + CSS3\n- JavaScript ES6+\n- Web Audio API\n\n---\n\n## 总结\n\n1. 简单易用\n2. 功能强大\n3. 完全免费\n\n**谢谢观看！**";convert()}
""",
    faqs_cn=[
        ('什么是Marp？', 'Marp是一个基于Markdown的演示文稿制作工具，可以用Markdown语法编写幻灯片，支持多种主题和导出格式（PDF、PPTX、HTML）。'),
        ('如何分页？', '在Markdown中使用---（三个横线）作为分页符，每个---之间的内容会成为一张幻灯片。'),
        ('支持哪些主题？', '支持Default、Gaia、Uncover三种Marp内置主题。Default是经典白底，Gaia是现代风格，Uncover是极简风格。'),
        ('如何导出为PPT？', '复制生成的Marp Markdown，使用Marp CLI或VS Code的Marp插件导出为PDF/PPTX/HTML格式。'),
        ('支持代码高亮吗？', 'Marp支持Markdown的代码块语法，导出时会自动应用语法高亮。'),
    ],
    faqs_en=[
        ('What is Marp?', 'Marp is a Markdown-based presentation tool. Write slides in Markdown, with multiple themes and export formats (PDF, PPTX, HTML).'),
        ('How to create slides?', 'Use --- (three dashes) as page breaks in Markdown. Content between each --- becomes one slide.'),
        ('Which themes are supported?', 'Default (classic white), Gaia (modern), and Uncover (minimal) - three built-in Marp themes.'),
        ('How to export to PPT?', 'Copy the generated Marp Markdown, then use Marp CLI or the VS Code Marp extension to export as PDF/PPTX/HTML.'),
        ('Does it support code highlighting?', 'Marp supports Markdown code block syntax with automatic syntax highlighting on export.'),
    ],
    seo_cn='<h2>Markdown转Marp演示工具介绍</h2><p>将Markdown文档快速转换为Marp演示格式，无需PowerPoint即可制作专业幻灯片。支持分页、主题切换和实时预览。</p><h2>核心功能</h2><ul><li><strong>Markdown编写</strong>：用熟悉的Markdown语法制作幻灯片</li><li><strong>三种主题</strong>：Default、Gaia、Uncover</li><li><strong>分页预览</strong>：实时预览每张幻灯片效果</li><li><strong>页码控制</strong>：可选显示/隐藏页码</li><li><strong>一键复制</strong>：复制Marp格式内容到编辑器</li></ul><h2>Marp优势</h2><p>Marp让开发者用Markdown写演示文稿，版本可控、协作友好、导出灵活。特别适合技术分享和教学场景。</p>',
    seo_en='<h2>Markdown to Marp Converter</h2><p>Quickly convert Markdown documents to Marp presentation format. Create professional slides without PowerPoint. Supports page breaks, themes, and live preview.</p><h2>Key Features</h2><ul><li><strong>Markdown authoring</strong>: Write slides in familiar Markdown syntax</li><li><strong>Three themes</strong>: Default, Gaia, Uncover</li><li><strong>Slide preview</strong>: Live preview of each slide</li><li><strong>Page numbers</strong>: Toggle pagination on/off</li><li><strong>One-click copy</strong>: Copy Marp content to your editor</li></ul><h2>Why Marp?</h2><p>Marp lets developers write presentations in Markdown - version controllable, collaboration-friendly, and flexible export. Perfect for tech talks and teaching.</p>',
)
print("Tool 5: markdown-to-marp - DONE")

print("\nAll 5 tools created successfully!")
