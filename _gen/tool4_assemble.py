#!/usr/bin/env python3
"""Assemble json-to-ruby CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "json-to-ruby"
JS = open(os.path.expanduser("~/tools-site/_gen/js/json_to_ruby.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("JSON转Ruby支持哪些类型映射？", "支持String、Integer、Float、Boolean、Array、Hash、NilClass等Ruby原生类型。嵌套对象映射为Hash或独立类，数组映射为Array。"),
    ("支持Struct和Class两种模式吗？", "支持。可选择生成Ruby Struct（轻量数据容器）或完整Class定义（含initialize、to_json、from_json方法）。Struct适合简单数据，Class适合复杂逻辑。"),
    ("生成的Ruby代码可以直接运行吗？", "可以。生成的代码遵循Ruby标准语法，包含必要的require语句。复制到.rb文件中即可运行，无需额外依赖（除json库外）。"),
    ("字段名如何转换？", "JSON的camelCase或snake_case字段名自动转换为Ruby惯用的snake_case风格，符合Ruby命名规范。"),
    ("数据安全吗？", "完全安全。所有处理在浏览器本地执行，JSON数据不会上传到任何服务器。"),
    ("支持from_json反序列化吗？", "支持。Class模式自动生成self.from_json类方法，可从JSON字符串直接创建对象实例。Struct模式可直接使用JSON.parse。"),
]

cn_title = "JSON转Ruby类生成器 - 在线生成Ruby Class/Struct·纯前端"
cn_desc = "免费在线JSON转Ruby类代码生成器。一键将JSON数据转换为Ruby Class或Struct代码，支持snake_case命名、to_json/from_json方法。纯前端本地处理，数据不上传服务器。"
cn_kw = "JSON转Ruby,Ruby类生成,Ruby Struct生成,JSON转Ruby Class,在线Ruby工具,Ruby代码生成"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "JSON转Ruby类生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>💎 JSON转Ruby类生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线JSON转Ruby类代码生成器。一键将JSON数据转换为Ruby Class或Struct代码，支持snake_case命名、to_json/from_json方法。纯前端本地处理，数据不上传服务器。</p>
<div class="options-area">
<div class="option-row">
<label>类名: <input type="text" id="className" value="MyData" style="width:120px"></label>
<label>类型: <select id="classType"><option value="class" selected>Class</option><option value="struct">Struct</option></select></label>
<label><input type="checkbox" id="useAttr" checked> attr_accessor</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON输入</label>
<textarea id="input" placeholder='{"name":"张三","age":25,"isVip":true}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的Ruby代码</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成Ruby类</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载RB</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>JSON转Ruby类生成器能做什么？</h2>
<p>JSON转Ruby类生成器是一款免费的在线工具，帮助Ruby开发者快速将JSON数据转换为Ruby Class或Struct代码。无需手动编写类定义和序列化方法，粘贴JSON即可自动生成完整代码，支持snake_case命名规范。纯前端处理，数据绝不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>Class/Struct双模式</strong>：选择生成完整Class（含initialize、to_json、from_json）或轻量Struct</li>
<li><strong>snake_case命名</strong>：自动将JSON字段名转换为Ruby惯用的snake_case风格</li>
<li><strong>序列化方法</strong>：Class模式自动生成to_h、to_json和self.from_json方法</li>
<li><strong>attr_accessor</strong>：可选生成属性访问器，支持读写对象字段</li>
<li><strong>关键字参数初始化</strong>：Struct模式使用keyword_init，Class模式使用关键字参数</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>输入JSON数据</strong>：在左侧文本框粘贴JSON对象</li>
<li><strong>配置选项</strong>：设置类名、选择Class或Struct模式</li>
<li><strong>点击生成</strong>：点击"生成Ruby类"按钮，右侧立即显示代码</li>
<li><strong>复制代码</strong>：复制生成的Ruby代码到项目中</li>
<li><strong>添加依赖</strong>：Class模式需要require 'json'</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：API响应建模</h3>
<p>对接REST API时，根据JSON响应快速生成Ruby类，配合to_json/from_json实现自动序列化。</p>
<h3>场景2：配置文件解析</h3>
<p>将JSON配置映射为Ruby Struct，类型安全地访问配置项。</p>
<h3>场景3：Rails模型原型</h3>
<p>快速生成Ruby类原型，后续可迁移为ActiveRecord模型。</p>
<h2>扩展知识</h2>
<p>Ruby Struct是轻量级数据容器，适合简单值对象。Class适合需要自定义逻辑的复杂对象。Ruby社区推荐snake_case命名，JSON的camelCase字段应转换为snake_case。Rails的jbuilder和active_model_serializers提供了更强大的JSON序列化方案。Dry-struct是Struct的类型安全替代品，支持类型检查和验证。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "JSON转Ruby类生成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What type mappings does JSON to Ruby support?", "Supports String, Integer, Float, Boolean, Array, Hash, NilClass and other Ruby native types. Nested objects map to Hash or independent classes, arrays to Array."),
    ("Does it support both Struct and Class modes?", "Yes. Choose Ruby Struct (lightweight data container) or full Class definition (with initialize, to_json, from_json methods). Struct for simple data, Class for complex logic."),
    ("Can the generated Ruby code run directly?", "Yes. Generated code follows standard Ruby syntax with necessary require statements. Copy to a .rb file and run — no extra dependencies needed (except the json library."),
    ("How are field names converted?", "JSON camelCase or snake_case field names are automatically converted to Ruby's conventional snake_case style."),
    ("Is my data secure?", "Completely secure. All processing runs locally in your browser. JSON data never leaves your device."),
    ("Does it support from_json deserialization?", "Yes. Class mode auto-generates self.from_json class method for creating instances from JSON strings. Struct mode can use JSON.parse directly."),
]

en_title = "JSON to Ruby Class Generator - Ruby Class/Struct Code · Pure Frontend"
en_desc = "Free online JSON to Ruby class code generator. Convert JSON data to Ruby Class or Struct code instantly. Supports snake_case naming, to_json/from_json methods. Pure frontend, no server upload."
en_kw = "JSON to Ruby,Ruby class generator,Ruby Struct generator,JSON to Ruby Class,online Ruby tool,Ruby code generator"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "JSON to Ruby Class Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>💎 JSON to Ruby Class Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online JSON to Ruby class code generator. Convert JSON data to Ruby Class or Struct code instantly. Supports snake_case naming, to_json/from_json methods. Pure frontend, no server upload.</p>
<div class="options-area">
<div class="option-row">
<label>Class Name: <input type="text" id="className" value="MyData" style="width:120px"></label>
<label>Type: <select id="classType"><option value="class" selected>Class</option><option value="struct">Struct</option></select></label>
<label><input type="checkbox" id="useAttr" checked> attr_accessor</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON Input</label>
<textarea id="input" placeholder='{"name":"John","age":25,"isVip":true}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated Ruby Code</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate Ruby Class</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Result</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download RB</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the JSON to Ruby Generator Do?</h2>
<p>The JSON to Ruby Class Generator is a free online tool that helps Ruby developers quickly convert JSON data into Ruby Class or Struct code. No need to manually write class definitions and serialization methods — paste JSON and auto-generate complete code with snake_case naming. Pure frontend, no data uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Class/Struct Dual Mode</strong>: Choose full Class (with initialize, to_json, from_json) or lightweight Struct</li>
<li><strong>snake_case Naming</strong>: Auto-converts JSON field names to Ruby's conventional snake_case style</li>
<li><strong>Serialization Methods</strong>: Class mode auto-generates to_h, to_json, and self.from_json methods</li>
<li><strong>attr_accessor</strong>: Optional attribute accessors for reading/writing object fields</li>
<li><strong>Keyword Arguments</strong>: Struct uses keyword_init, Class uses keyword arguments for initialization</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Paste JSON data</strong> in the left text area</li>
<li><strong>Configure options</strong>: class name, Class or Struct mode</li>
<li><strong>Click Generate</strong>: Ruby code appears immediately on the right</li>
<li><strong>Copy code</strong> to your Ruby project</li>
<li><strong>Add dependency</strong>: Class mode requires 'json' library</li>
</ol>
<h2>Use Cases</h2>
<h3>API Response Modeling</h3>
<p>Generate Ruby classes from JSON API responses with to_json/from_json for automatic serialization.</p>
<h3>Config File Parsing</h3>
<p>Map JSON configs to Ruby Structs for type-safe config access.</p>
<h3>Rails Model Prototyping</h3>
<p>Quickly generate Ruby class prototypes that can later migrate to ActiveRecord models.</p>
<h2>Technical Background</h2>
<p>Ruby Struct is a lightweight data container ideal for simple value objects. Class is better for objects requiring custom logic. The Ruby community recommends snake_case naming; JSON camelCase fields should be converted. Rails offers jbuilder and active_model_serializers for more powerful JSON serialization. Dry-struct is a type-safe alternative to Struct with type checking and validation.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "JSON to Ruby Class Generator")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
