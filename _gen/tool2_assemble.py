#!/usr/bin/env python3
"""Assemble json-to-java CN+EN pages from template parts."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "json-to-java"
JS_CODE = open(os.path.expanduser("~/tools-site/_gen/js/json_to_java.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("JSON转Java类支持哪些类型映射？", "支持String、Integer/int、Long/long、Double/double、Boolean/boolean、BigDecimal、List<T>、Map<String,Object>等。日期格式自动识别为String或Date类型，空值字段使用Object或包装类型。"),
    ("支持Gson和Jackson注解吗？", "支持。可选择生成@SerializedName（Gson）或@JsonProperty（Jackson）注解，也可以选择不生成注解。字段名风格支持camelCase和保持原始JSON键名。"),
    ("嵌套JSON对象如何处理？", "嵌套对象自动生成独立的内部类（static inner class）或独立类文件。数组自动映射为List<T>泛型类型，元素类型根据数组内容自动推断。"),
    ("生成的Java代码可以直接编译吗？", "可以。生成的代码遵循标准Java语法，包含完整的类定义、字段声明和getter/setter方法（可选）。复制到项目中添加必要的import即可编译。"),
    ("数据安全如何保障？", "完全安全。所有JSON解析和代码生成均在浏览器本地执行，你的数据绝不会上传到任何服务器。关闭页面后数据自动清除。"),
    ("支持Lombok注解吗？", "支持。可选择添加@Data、@Getter、@Setter、@Builder等Lombok注解，减少样板代码。需要项目中引入Lombok依赖。"),
]

cn_title = "JSON转Java类生成器 - 在线生成Java POJO·自动类型推断·纯前端"
cn_desc = "免费在线JSON转Java类代码生成器。一键将JSON数据转换为Java POJO类代码，支持嵌套对象、List泛型、Gson/Jackson注解。纯前端本地处理，数据不上传服务器。"
cn_kw = "JSON转Java,Java类生成,POJO生成,JSON转POJO,Gson注解,Jackson注解,在线Java工具"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "JSON转Java类生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>☕ JSON转Java类生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线JSON转Java类代码生成器。一键将JSON数据转换为Java POJO类代码，支持嵌套对象、List泛型、Gson/Jackson注解。纯前端本地处理，数据不上传服务器。</p>
<div class="options-area">
<div class="option-row">
<label>类名: <input type="text" id="className" value="MyData" style="width:120px"></label>
<label>注解: <select id="annotation"><option value="none">无注解</option><option value="gson">Gson @SerializedName</option><option value="jackson" selected>Jackson @JsonProperty</option><option value="lombok">Lombok @Data</option></select></label>
<label>包名: <input type="text" id="packageName" value="com.example" style="width:150px"></label>
<label><input type="checkbox" id="useWrapper" checked> 包装类型</label>
<label><input type="checkbox" id="genGetterSetter" checked> Getter/Setter</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON输入</label>
<textarea id="input" placeholder='{"name":"张三","age":25,"email":"test@example.com","isVip":true}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的Java类</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成Java类</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载Java</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>JSON转Java类生成器能做什么？</h2>
<p>JSON转Java类生成器是一款免费的在线工具，帮助Java开发者快速将JSON数据转换为Java POJO类代码。无需手动编写实体类，粘贴JSON即可自动生成完整类定义，支持Gson/Jackson/Lombok注解，大幅提升开发效率。纯前端处理，数据绝不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>智能类型推断</strong>：自动将JSON值类型映射为Java类型，字符串→String，整数→Integer，浮点数→Double，布尔→Boolean</li>
<li><strong>嵌套对象支持</strong>：嵌套JSON自动生成静态内部类，多层嵌套递归处理</li>
<li><strong>数组/List映射</strong>：JSON数组自动转换为List&lt;T&gt;泛型，元素类型自动推断</li>
<li><strong>注解生成</strong>：支持Gson @SerializedName、Jackson @JsonProperty、Lombok @Data注解</li>
<li><strong>Getter/Setter生成</strong>：可选生成完整的getter/setter方法，或使用Lombok简化</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>输入JSON数据</strong>：在左侧文本框粘贴JSON对象或数组</li>
<li><strong>配置选项</strong>：设置类名、包名、注解类型、是否使用包装类型</li>
<li><strong>点击生成</strong>：点击"生成Java类"按钮，右侧立即显示代码</li>
<li><strong>复制代码</strong>：复制生成的Java类到项目中的对应包下</li>
<li><strong>添加依赖</strong>：根据选择的注解类型，确保项目引入Gson/Jackson/Lombok依赖</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：API接口对接</h3>
<p>对接第三方API时，根据返回的JSON数据快速生成Java实体类，省去手动编写的繁琐工作，配合Retrofit/OkHttp立即开始开发。</p>
<h3>场景2：JSON数据建模</h3>
<p>需要将JSON配置文件映射为Java对象时，一键生成类定义，确保字段名和类型完全匹配。</p>
<h3>场景3：数据迁移</h3>
<p>从NoSQL数据库导出JSON数据后，需要转为Java对象存入关系型数据库，本工具快速生成对应的实体类。</p>
<h2>扩展知识</h2>
<p>Java POJO（Plain Old Java Object）是最常见的Java数据载体模式。Gson和Jackson是最流行的两个JSON序列化库：Gson轻量简洁，Jackson功能强大。Lombok通过编译期注解处理，自动生成getter/setter/constructor等样板代码，显著减少代码量。使用@SerializedName或@JsonProperty注解可以在JSON键名与Java字段名不一致时进行映射。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "JSON转Java类生成器")
cn_html += "<script>\n" + JS_CODE + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What type mappings does JSON to Java support?", "Supports String, Integer/int, Long/long, Double/double, Boolean/boolean, BigDecimal, List<T>, Map<String,Object>. Date formats auto-detected as String or Date. Null fields use Object or wrapper types."),
    ("Does it support Gson and Jackson annotations?", "Yes. Choose @SerializedName (Gson), @JsonProperty (Jackson), or no annotations. Field naming supports camelCase or original JSON key names."),
    ("How are nested JSON objects handled?", "Nested objects auto-generate static inner classes. Arrays map to List<T> with element types inferred from array content."),
    ("Can the generated Java code compile directly?", "Yes. Generated code follows standard Java syntax with complete class definitions, field declarations, and optional getter/setter methods. Add necessary imports and it compiles."),
    ("Is my data secure?", "Completely secure. All JSON parsing and code generation runs locally in your browser. Your data never leaves your device and is cleared when you close the page."),
    ("Does it support Lombok annotations?", "Yes. Choose @Data, @Getter, @Setter, @Builder annotations to reduce boilerplate. Requires Lombok dependency in your project."),
]

en_title = "JSON to Java Class Generator - POJO Code · Auto Type Inference · Pure Frontend"
en_desc = "Free online JSON to Java class code generator. Convert JSON data to Java POJO classes instantly. Supports nested objects, List generics, Gson/Jackson annotations. Pure frontend, no server upload."
en_kw = "JSON to Java,Java class generator,POJO generator,JSON to POJO,Gson annotation,Jackson annotation,online Java tool"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "JSON to Java Class Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>☕ JSON to Java Class Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online JSON to Java class code generator. Convert JSON data to Java POJO classes instantly. Supports nested objects, List generics, Gson/Jackson annotations. Pure frontend, no server upload.</p>
<div class="options-area">
<div class="option-row">
<label>Class: <input type="text" id="className" value="MyData" style="width:120px"></label>
<label>Annotations: <select id="annotation"><option value="none">None</option><option value="gson">Gson @SerializedName</option><option value="jackson" selected>Jackson @JsonProperty</option><option value="lombok">Lombok @Data</option></select></label>
<label>Package: <input type="text" id="packageName" value="com.example" style="width:150px"></label>
<label><input type="checkbox" id="useWrapper" checked> Wrapper Types</label>
<label><input type="checkbox" id="genGetterSetter" checked> Getter/Setter</label>
</div></div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">JSON Input</label>
<textarea id="input" placeholder='{"name":"John","age":25,"email":"test@example.com","isVip":true}'></textarea>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated Java Class</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate Java Class</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Result</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download Java</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the JSON to Java Generator Do?</h2>
<p>The JSON to Java Class Generator is a free online tool that helps Java developers quickly convert JSON data into Java POJO class code. No need to manually write entity classes — paste JSON and auto-generate complete class definitions with Gson/Jackson/Lombok annotation support. Pure frontend, no data uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Smart Type Inference</strong>: Auto-maps JSON value types to Java types — string→String, integer→Integer, float→Double, boolean→Boolean</li>
<li><strong>Nested Object Support</strong>: Nested JSON auto-generates static inner classes with recursive multi-level handling</li>
<li><strong>Array/List Mapping</strong>: JSON arrays auto-convert to List&lt;T&gt; generics with element type inference</li>
<li><strong>Annotation Generation</strong>: Supports Gson @SerializedName, Jackson @JsonProperty, Lombok @Data</li>
<li><strong>Getter/Setter Generation</strong>: Optional full getter/setter methods or Lombok shorthand</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Paste JSON data</strong> in the left text area</li>
<li><strong>Configure options</strong>: class name, package, annotation type, wrapper types</li>
<li><strong>Click Generate</strong>: Java class code appears immediately on the right</li>
<li><strong>Copy code</strong> to your project's corresponding package</li>
<li><strong>Add dependencies</strong>: Ensure Gson/Jackson/Lombok is in your project</li>
</ol>
<h2>Use Cases</h2>
<h3>API Integration</h3>
<p>When integrating third-party APIs, quickly generate Java entity classes from JSON responses. Skip manual class writing and start coding with Retrofit/OkHttp immediately.</p>
<h3>JSON Data Modeling</h3>
<p>Map JSON config files to Java objects with one-click class generation, ensuring field names and types match perfectly.</p>
<h3>Data Migration</h3>
<p>Convert NoSQL JSON exports to Java objects for relational database storage. Generate entity classes in seconds.</p>
<h2>Technical Background</h2>
<p>Java POJO (Plain Old Java Object) is the most common Java data carrier pattern. Gson and Jackson are the two most popular JSON serialization libraries: Gson is lightweight, Jackson is feature-rich. Lombok uses compile-time annotation processing to auto-generate boilerplate code (getters, setters, constructors), significantly reducing code volume. @SerializedName or @JsonProperty annotations map JSON keys to Java fields when names differ.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "JSON to Java Class Generator")
en_html += "<script>\n" + JS_CODE + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
