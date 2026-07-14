#!/usr/bin/env python3
"""Assemble json-to-cpp CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "json-to-cpp"
JS = open(os.path.expanduser("~/tools-site/_gen/js/json_to_cpp.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("JSON转C++支持哪些类型映射？", "支持std::string、int、double、bool、std::vector<T>、嵌套struct等。空值映射为std::variant或std::any，数组映射为std::vector，嵌套对象映射为嵌套struct。"),
    ("支持nlohmann/json库吗？", "支持。可选择生成NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE宏，方便与nlohmann/json库配合使用进行JSON序列化和反序列化。"),
    ("嵌套JSON如何处理？", "嵌套对象自动生成独立的struct定义，数组中的对象也会递归生成对应struct。支持多层嵌套。"),
    ("生成的C++代码可以直接编译吗？", "可以。生成的代码遵循C++11/14标准语法，包含必要的头文件引用。复制到项目中确保编译器支持C++11以上即可编译。"),
    ("数据安全吗？", "完全安全。所有处理在浏览器本地执行，JSON数据不会上传到任何服务器。"),
    ("支持C++20特性吗？", "目前生成C++11/14兼容代码。未来可添加std::optional、std::variant、Concepts等C++17/20特性支持。"),
]

cn_title = "JSON转C++结构体生成器 - 在线生成C++ Struct·nlohmann/json·纯前端"
cn_desc = "免费在线JSON转C++结构体代码生成器。一键将JSON数据转换为C++ struct代码，支持嵌套对象、std::vector、nlohmann/json宏。纯前端本地处理，数据不上传服务器。"
cn_kw = "JSON转C++,C++结构体生成,JSON转struct,C++代码生成,nlohmann json,在线C++工具"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "JSON转C++结构体生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>⚡ JSON转C++结构体生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线JSON转C++结构体代码生成器。一键将JSON数据转换为C++ struct代码，支持嵌套对象、std::vector、nlohmann/json宏。纯前端本地处理，数据不上传服务器。</p>
<div class="options-area">
<div class="option-row">
<label>结构体名: <input type="text" id="structName" value="MyData" style="width:120px"></label>
<label><input type="checkbox" id="useNlohmann" checked> nlohmann/json宏</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON输入</label>
<textarea id="input" placeholder='{"name":"Alice","age":30,"score":95.5}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的C++代码</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成C++结构体</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载HPP</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>JSON转C++结构体生成器能做什么？</h2>
<p>JSON转C++结构体生成器是一款免费的在线工具，帮助C++开发者快速将JSON数据转换为C++ struct定义代码。无需手动编写结构体和序列化逻辑，粘贴JSON即可自动生成完整代码，支持nlohmann/json库集成，大幅提升开发效率。纯前端处理，数据绝不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>智能类型推断</strong>：自动将JSON值类型映射为C++类型，字符串→std::string，整数→int，浮点数→double，布尔→bool</li>
<li><strong>嵌套struct支持</strong>：嵌套JSON对象自动生成独立struct定义，多层递归处理</li>
<li><strong>std::vector映射</strong>：JSON数组自动转换为std::vector&lt;T&gt;，元素类型自动推断</li>
<li><strong>nlohmann/json集成</strong>：可选生成NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE宏，一键实现序列化</li>
<li><strong>头文件自动引用</strong>：自动添加&lt;string&gt;、&lt;vector&gt;、nlohmann/json.hpp等必要头文件</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>输入JSON数据</strong>：在左侧文本框粘贴JSON对象</li>
<li><strong>配置选项</strong>：设置结构体名、是否启用nlohmann/json宏</li>
<li><strong>点击生成</strong>：点击"生成C++结构体"按钮，右侧立即显示代码</li>
<li><strong>复制代码</strong>：复制生成的C++代码到项目头文件中</li>
<li><strong>添加依赖</strong>：如使用nlohmann/json，确保项目中包含该库</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：REST API客户端开发</h3>
<p>对接REST API时，根据JSON响应快速生成C++结构体，配合nlohmann/json库实现自动序列化/反序列化。</p>
<h3>场景2：配置文件解析</h3>
<p>将JSON配置文件映射为C++结构体，类型安全地访问配置项，避免手动解析错误。</p>
<h3>场景3：游戏数据建模</h3>
<p>游戏开发中，从JSON数据文件快速生成C++数据结构，用于角色、道具、关卡等数据定义。</p>
<h2>扩展知识</h2>
<p>C++ struct是最常用的数据聚合方式。nlohmann/json是C++最流行的JSON库，通过NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE宏可以一行代码实现struct与JSON的互转。C++17引入了std::optional和std::variant，可以更优雅地处理JSON中的可选字段和多类型字段。对于高性能场景，可考虑使用simdjson等零拷贝JSON解析器。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "JSON转C++结构体生成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What type mappings does JSON to C++ support?", "Supports std::string, int, double, bool, std::vector<T>, nested structs. Null values map to std::variant or std::any, arrays to std::vector, nested objects to nested structs."),
    ("Does it support nlohmann/json library?", "Yes. Optionally generate NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE macro for seamless JSON serialization/deserialization with nlohmann/json."),
    ("How are nested JSON objects handled?", "Nested objects auto-generate independent struct definitions. Objects in arrays are also recursively generated. Supports multi-level nesting."),
    ("Can the generated C++ code compile directly?", "Yes. Generated code follows C++11/14 standard syntax with necessary header includes. Copy to your project and ensure C++11+ compiler support."),
    ("Is my data secure?", "Completely secure. All processing runs locally in your browser. JSON data never leaves your device."),
    ("Does it support C++20 features?", "Currently generates C++11/14 compatible code. Future updates may add std::optional, std::variant, Concepts, and other C++17/20 features."),
]

en_title = "JSON to C++ Struct Generator - Online C++ Code · nlohmann/json · Pure Frontend"
en_desc = "Free online JSON to C++ struct code generator. Convert JSON data to C++ struct definitions instantly. Supports nested objects, std::vector, nlohmann/json macros. Pure frontend, no server upload."
en_kw = "JSON to C++,C++ struct generator,JSON to struct,C++ code generator,nlohmann json,online C++json,online C++ tool"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "JSON to C++ Struct Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>⚡ JSON to C++ Struct Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online JSON to C++ struct code generator. Convert JSON data to C++ struct definitions instantly. Supports nested objects, std::vector, nlohmann/json macros. Pure frontend, no server upload.</p>
<div class="options-area">
<div class="option-row">
<label>Struct Name: <input type="text" id="structName" value="MyData" style="width:120px"></label>
<label><input type="checkbox" id="useNlohmann" checked> nlohmann/json macro</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON Input</label>
<textarea id="input" placeholder='{"name":"Alice","age":30,"score":95.5}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated C++ Code</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate C++ Struct</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Result</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download HPP</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the JSON to C++ Generator Do?</h2>
<p>The JSON to C++ Struct Generator is a free online tool that helps C++ developers quickly convert JSON data into C++ struct definitions. No need to manually write structs and serialization logic — paste JSON and auto-generate complete code with nlohmann/json integration. Pure frontend, no data uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Smart Type Inference</strong>: Auto-maps JSON types to C++ — string→std::string, integer→int, float→double, boolean→bool</li>
<li><strong>Nested Struct Support</strong>: Nested JSON objects auto-generate independent struct definitions with recursive handling</li>
<li><strong>std::vector Mapping</strong>: JSON arrays auto-convert to std::vector&lt;T&gt; with element type inference</li>
<li><strong>nlohmann/json Integration</strong>: Optional NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE macro for one-line serialization</li>
<li><strong>Auto Header Includes</strong>: Automatically adds &lt;string&gt;, &lt;vector&gt;, nlohmann/json.hpp as needed</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Paste JSON data</strong> in the left text area</li>
<li><strong>Configure options</strong>: struct name, nlohmann/json macro toggle</li>
<li><strong>Click Generate</strong>: C++ code appears immediately on the right</li>
<li><strong>Copy code</strong> to your project header file</li>
<li><strong>Add dependency</strong>: Include nlohmann/json library if using macros</li>
</ol>
<h2>Use Cases</h2>
<h3>REST API Client Development</h3>
<p>Generate C++ structs from JSON API responses, paired with nlohmann/json for automatic serialization/deserialization.</p>
<h3>Config File Parsing</h3>
<p>Map JSON config files to C++ structs for type-safe config access, eliminating manual parsing errors.</p>
<h3>Game Data Modeling</h3>
<p>Quickly generate C++ data structures from JSON data files for characters, items, levels, and more.</p>
<h2>Technical Background</h2>
<p>C++ structs are the most common data aggregation mechanism. nlohmann/json is the most popular C++ JSON library, enabling struct-to-JSON conversion with a single NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE macro. C++17 introduced std::optional and std::variant for elegantly handling optional and multi-type JSON fields. For high-performance scenarios, consider simdjson for zero-copy JSON parsing.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "JSON to C++ Struct Generator")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
