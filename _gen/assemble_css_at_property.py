#!/usr/bin/env python3
"""Assemble css-at-property-generator CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "css-at-property-generator"
JS = open(os.path.expanduser("~/tools-site/_gen/js/css_at_property.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("CSS @property是什么？", "@property是CSS Houdini的一部分，允许开发者注册自定义CSS属性，定义其语法类型、初始值和继承行为。注册后的自定义属性可以被CSS动画和过渡使用。"),
    ("为什么需要@property？", "普通的CSS自定义属性（var）无法被动画化，浏览器不知道其值类型。通过@property注册后，浏览器理解属性的数据类型，就能对其应用动画和过渡效果。"),
    ("支持哪些语法类型？", "支持<length>、<number>、<percentage>、<length-percentage>、<color>、<image>、<url>、<integer>、<angle>、<time>、<resolution>、<transform-function>、<custom-ident>等类型。"),
    ("浏览器兼容性如何？", "Chrome 85+、Edge 85+、Safari 15.4+支持。Firefox正在实现中。建议使用@supports检测或提供降级方案。"),
    ("可以注册多个自定义属性吗？", "可以。每个@property规则注册一个自定义属性，你可以在样式表中注册任意数量的自定义属性。"),
    ("inherits属性有什么作用？", "inherits控制自定义属性是否继承父元素的值。设为true时子元素继承父元素的属性值，设为false则使用初始值。"),
]

cn_title = "CSS @property生成器 - 自定义属性动画代码·纯前端"
cn_desc = "免费在线CSS @property生成器。一键生成CSS自定义属性注册代码和动画关键帧，支持渐变角度动画、颜色过渡等高级效果。纯前端本地处理，代码不上传服务器。"
cn_kw = "CSS @property,CSS自定义属性,CSS动画,Houdini,@property生成器,CSS渐变动画,自定义属性动画"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "CSS @property生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>🎨 CSS @property生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线CSS @property生成器。一键生成自定义属性注册代码和动画关键帧，让渐变、颜色等原本无法动画的CSS属性实现平滑过渡。纯前端本地处理。</p>
<div class="options-area">
<div class="option-row">
<label>属性名: <input type="text" id="propertyName" value="--gradient-angle" style="width:180px"></label>
</div>
<div class="option-row">
<label>语法: <select id="syntax">
<option value="<angle>">&lt;angle&gt;</option>
<option value="<length>">&lt;length&gt;</option>
<option value="<number>">&lt;number&gt;</option>
<option value="<percentage>">&lt;percentage&gt;</option>
<option value="<color>">&lt;color&gt;</option>
<option value="<length-percentage>">&lt;length-percentage&gt;</option>
<option value="<integer>">&lt;integer&gt;</option>
<option value="<time>">&lt;time&gt;</option>
</select></label>
<label>初始值: <input type="text" id="initialValue" value="0deg" style="width:100px"></label>
<label>继承: <select id="inherits"><option value="false">否</option><option value="true">是</option></select></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">动画设置（可选）</div>
<div class="option-row">
<label>起值: <input type="text" id="animValue1" value="0deg" style="width:80px"></label>
<label>终值: <input type="text" id="animValue2" value="360deg" style="width:80px"></label>
<label>时长: <input type="number" id="animDuration" value="3" style="width:60px">s</label>
<label>缓动: <select id="animTiming">
<option value="linear">linear</option>
<option value="ease">ease</option>
<option value="ease-in-out">ease-in-out</option>
<option value="ease-in">ease-in</option>
<option value="ease-out">ease-out</option>
</select></label>
<label>次数: <select id="animIteration">
<option value="infinite">无限</option>
<option value="1">1次</option>
<option value="2">2次</option>
<option value="3">3次</option>
</select></label>
</div>
</div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的CSS代码</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">预览效果</label>
<div id="preview" style="min-height:200px;display:flex;align-items:center;justify-content:center"></div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成@property</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制代码</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载CSS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>CSS @property生成器能做什么？</h2>
<p>CSS @property生成器是一款免费在线工具，帮助前端开发者快速生成CSS自定义属性注册代码和动画关键帧。通过@property注册自定义属性，可以让原本无法动画化的CSS值类型（如渐变角度）实现平滑过渡效果。纯前端处理，代码不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>自定义属性注册</strong>：生成符合规范的@property规则，定义语法类型、初始值和继承行为</li>
<li><strong>动画关键帧</strong>：自动生成@keyframes动画，配合@property实现高级CSS动画</li>
<li><strong>实时预览</strong>：渐变角度动画支持实时预览效果</li>
<li><strong>多语法类型</strong>：支持angle、length、number、color、percentage等所有CSS值类型</li>
<li><strong>一键导出</strong>：复制或下载生成的CSS代码，直接用于项目</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>设置属性名</strong>：输入自定义属性名（如--gradient-angle）</li>
<li><strong>选择语法类型</strong>：根据属性值选择对应的CSS语法类型</li>
<li><strong>设置初始值</strong>：输入属性的默认值</li>
<li><strong>配置动画</strong>：可选设置动画起止值、时长、缓动函数</li>
<li><strong>生成代码</strong>：点击生成按钮，复制代码到项目中</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：渐变角度动画</h3>
<p>通过注册--gradient-angle为&lt;angle&gt;类型，实现渐变背景角度的平滑旋转动画，无需JavaScript。</p>
<h3>场景2：颜色类型自定义属性</h3>
<p>将自定义颜色属性注册为&lt;color&gt;类型，使主题色切换拥有平滑过渡效果。</p>
<h3>场景3：复杂布局动画</h3>
<p>将长度、百分比等自定义属性注册后用于布局动画，实现更灵活的响应式过渡。</p>
<h2>扩展知识</h2>
<p>CSS Houdini是W3C的一组API，让开发者可以扩展CSS的能力。@property属于CSS Properties and Values API，是最先被浏览器广泛支持的Houdini特性。它解决了CSS自定义属性无法被动画化的根本问题。结合@property和CSS动画，可以实现以前只能用JavaScript实现的高级动画效果，性能更优、代码更简洁。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "CSS @property生成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What is CSS @property?", "@property is part of CSS Houdini that allows developers to register custom CSS properties with defined syntax types, initial values, and inheritance behavior. Registered properties can be animated and transitioned by CSS."),
    ("Why do I need @property?", "Regular CSS custom properties (var) cannot be animated because browsers don't know their value types. By registering with @property, browsers understand the data type and can apply animations and transitions."),
    ("What syntax types are supported?", "Supports <length>, <number>, <percentage>, <length-percentage>, <color>, <image>, <url>, <integer>, <angle>, <time>, <resolution>, <transform-function>, <custom-ident>, and more."),
    ("What about browser compatibility?", "Chrome 85+, Edge 85+, Safari 15.4+ support @property. Firefox is implementing it. Use @supports detection or provide fallbacks."),
    ("Can I register multiple custom properties?", "Yes. Each @property rule registers one custom property. You can register any number of custom properties in your stylesheet."),
    ("What does the inherits property do?", "The inherits property controls whether the custom property inherits from parent elements. Set to true for inheritance, false to use the initial value."),
]

en_title = "CSS @property Generator - Custom Property Animation Code · Pure Frontend"
en_desc = "Free online CSS @property generator. Generate custom property registration code and animation keyframes instantly. Supports gradient angle animation, color transitions and more. Pure frontend, no server upload."
en_kw = "CSS @property,CSS custom property,CSS animation,Houdini,@property generator,CSS gradient animation,custom property animation"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "CSS @property Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>🎨 CSS @property Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online CSS @property generator. Generate custom property registration code and animation keyframes instantly. Enable smooth transitions for gradients, colors and other CSS values that were previously un-animatable. Pure frontend.</p>
<div class="options-area">
<div class="option-row">
<label>Property Name: <input type="text" id="propertyName" value="--gradient-angle" style="width:180px"></label>
</div>
<div class="option-row">
<label>Syntax: <select id="syntax">
<option value="<angle>">&lt;angle&gt;</option>
<option value="<length>">&lt;length&gt;</option>
<option value="<number>">&lt;number&gt;</option>
<option value="<percentage>">&lt;percentage&gt;</option>
<option value="<color>">&lt;color&gt;</option>
<option value="<length-percentage>">&lt;length-percentage&gt;</option>
<option value="<integer>">&lt;integer&gt;</option>
<option value="<time>">&lt;time&gt;</option>
</select></label>
<label>Initial: <input type="text" id="initialValue" value="0deg" style="width:100px"></label>
<label>Inherits: <select id="inherits"><option value="false">No</option><option value="true">Yes</option></select></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">Animation Settings (optional)</div>
<div class="option-row">
<label>From: <input type="text" id="animValue1" value="0deg" style="width:80px"></label>
<label>To: <input type="text" id="animValue2" value="360deg" style="width:80px"></label>
<label>Duration: <input type="number" id="animDuration" value="3" style="width:60px">s</label>
<label>Easing: <select id="animTiming">
<option value="linear">linear</option>
<option value="ease">ease</option>
<option value="ease-in-out">ease-in-out</option>
<option value="ease-in">ease-in</option>
<option value="ease-out">ease-out</option>
</select></label>
<label>Iteration: <select id="animIteration">
<option value="infinite">Infinite</option>
<option value="1">1x</option>
<option value="2">2x</option>
<option value="3">3x</option>
</select></label>
</div>
</div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated CSS Code</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Preview</label>
<div id="preview" style="min-height:200px;display:flex;align-items:center;justify-content:center"></div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate @property</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Code</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download CSS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the CSS @property Generator Do?</h2>
<p>The CSS @property Generator is a free online tool that helps frontend developers quickly generate CSS custom property registration code and animation keyframes. By registering custom properties with @property, you can animate CSS value types that were previously impossible to transition, like gradient angles. Pure frontend, no uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Custom Property Registration</strong>: Generate standards-compliant @property rules with syntax, initial value, and inheritance</li>
<li><strong>Animation Keyframes</strong>: Auto-generate @keyframes for advanced CSS animations with @property</li>
<li><strong>Live Preview</strong>: Gradient angle animations preview in real-time</li>
<li><strong>Multiple Syntax Types</strong>: Supports angle, length, number, color, percentage, and all CSS value types</li>
<li><strong>One-Click Export</strong>: Copy or download generated CSS code for your project</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Set property name</strong>: Enter custom property name (e.g. --gradient-angle)</li>
<li><strong>Choose syntax type</strong>: Select the CSS value type for your property</li>
<li><strong>Set initial value</strong>: Enter the default value for the property</li>
<li><strong>Configure animation</strong>: Optionally set animation start/end values, duration, easing</li>
<li><strong>Generate code</strong>: Click generate and copy the code to your project</li>
</ol>
<h2>Use Cases</h2>
<h3>Gradient Angle Animation</h3>
<p>Register --gradient-angle as &lt;angle&gt; to create smooth rotating gradient backgrounds without JavaScript.</p>
<h3>Color Custom Properties</h3>
<p>Register color properties as &lt;color&gt; type for smooth theme color transitions.</p>
<h3>Complex Layout Animation</h3>
<p>Register length/percentage properties for more flexible responsive transitions.</p>
<h2>Technical Background</h2>
<p>CSS Houdini is a set of W3C APIs that let developers extend CSS capabilities. @property belongs to the CSS Properties and Values API, the most widely supported Houdini feature. It solves the fundamental problem of CSS custom properties not being animatable. Combined with CSS animations, @property enables advanced effects that previously required JavaScript, with better performance and cleaner code.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "CSS @property Generator")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
