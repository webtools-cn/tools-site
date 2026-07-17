#!/usr/bin/env python3
"""Assemble css-houdini-paint-generator CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "css-houdini-paint-generator"
JS = open(os.path.expanduser("~/tools-site/_gen/js/css_houdini_paint.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("什么是CSS Houdini Paint Worklet？", "Paint Worklet是CSS Houdini的一部分，允许开发者用JavaScript编写自定义绘制逻辑，然后通过CSS的paint()函数作为背景、边框等使用。相当于用JS扩展CSS的绘制能力。"),
    ("浏览器兼容性如何？", "Chrome 65+、Edge 79+支持Paint Worklet。Safari正在实现中。Firefox尚未支持。建议使用@supports检测或提供CSS降级方案。"),
    ("如何注册Paint Worklet？", "在主线程JS中调用CSS.paintWorklet.addModule('paint-file.js')加载Worklet文件。Worklet文件中用registerPaint()注册画笔类，CSS中用background: paint(paint-name)使用。"),
    ("Paint Worklet和Canvas有什么区别？", "Canvas是命令式绘制，需要手动管理。Paint Worklet是声明式的，通过CSS属性驱动，浏览器自动调用paint()方法。Worklet在独立线程运行，不影响主线程性能。"),
    ("支持哪些图案类型？", "本工具支持棋盘格、圆点、斜条纹、交叉线、波浪等5种基础图案。每种图案可自定义颜色和尺寸，生成的代码可作为基础进一步修改。"),
    ("Paint Worklet能访问DOM吗？", "不能。Paint Worklet运行在独立的Worklet全局作用域中，无法访问DOM、window等API。只能使用Canvas 2D API进行绘制，这是为了保证性能和安全性。"),
]

cn_title = "CSS Houdini Paint生成器 - 自定义绘制Worklet代码·纯前端"
cn_desc = "免费在线CSS Houdini Paint Worklet生成器。一键生成自定义CSS绘制代码，支持棋盘格、圆点、条纹等5种图案，实时预览效果。纯前端本地处理，代码不上传服务器。"
cn_kw = "CSS Houdini,Paint Worklet,CSS自定义绘制,CSS画笔,CSS图案生成,Houdini Paint,自定义背景图案"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "CSS Houdini Paint生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>🎨 CSS Houdini Paint生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线CSS Houdini Paint Worklet生成器。一键生成自定义CSS绘制代码，支持5种图案类型，实时Canvas预览。纯前端本地处理。</p>
<div class="options-area">
<div class="option-row">
<label>图案类型: <select id="paintType">
<option value="checkerboard">棋盘格</option>
<option value="dots">圆点</option>
<option value="stripes">斜条纹</option>
<option value="crosshatch">交叉线</option>
<option value="waves">波浪</option>
</select></label>
<label>颜色1: <input type="color" id="color1" value="#06b6d4" style="width:50px;height:30px"></label>
<label>颜色2: <input type="color" id="color2" value="#1e293b" style="width:50px;height:30px"></label>
<label>尺寸: <input type="number" id="size" value="20" style="width:60px">px</label>
</div>
</div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">生成的Paint Worklet代码</label>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">预览效果</label>
<div id="preview" style="min-height:200px;display:flex;align-items:center;justify-content:center"></div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成Worklet</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制代码</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载JS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>CSS Houdini Paint生成器能做什么？</h2>
<p>CSS Houdini Paint生成器是一款免费在线工具，帮助前端开发者快速生成CSS Paint Worklet代码。通过JavaScript自定义绘制逻辑，扩展CSS的背景和边框绘制能力。支持5种基础图案，实时Canvas预览。纯前端处理。</p>
<h2>核心功能</h2>
<ul>
<li><strong>5种图案类型</strong>：棋盘格、圆点、斜条纹、交叉线、波浪</li>
<li><strong>自定义配色</strong>：双色选择器，自由搭配前景和背景色</li>
<li><strong>尺寸控制</strong>：调整图案单元大小，适配不同场景</li>
<li><strong>实时预览</strong>：Canvas即时渲染预览效果</li>
<li><strong>完整代码</strong>：生成包含注册和CSS用法的完整代码</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>选择图案</strong>：从5种基础图案中选择</li>
<li><strong>设置颜色</strong>：选择前景色和背景色</li>
<li><strong>调整尺寸</strong>：设置图案单元的像素大小</li>
<li><strong>生成代码</strong>：点击生成，复制Worklet代码</li>
<li><strong>集成项目</strong>：将Worklet文件部署到服务器，CSS中用paint()引用</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：自定义背景图案</h3>
<p>用Paint Worklet替代重复的background-image，实现无限平铺的自定义图案背景。</p>
<h3>场景2：动态边框效果</h3>
<p>配合CSS自定义属性，实现响应式的动态边框绘制效果。</p>
<h3>场景3：性能优化</h3>
<p>Paint Worklet在独立线程运行，不阻塞主线程，适合需要频繁重绘的场景。</p>
<h2>扩展知识</h2>
<p>CSS Houdini是W3C的一组底层API，让开发者可以扩展CSS引擎的能力。Paint Worklet是最成熟的Houdini API之一。与Canvas不同，Paint Worklet是声明式的——浏览器在需要时自动调用paint()方法，无需手动管理绘制时机。Worklet运行在独立的渲染线程，不会阻塞主线程，天然适合性能敏感的绘制场景。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "CSS Houdini Paint生成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What is CSS Houdini Paint Worklet?", "Paint Worklet is part of CSS Houdini that allows developers to write custom drawing logic in JavaScript, then use it via CSS paint() function for backgrounds, borders, etc. It extends CSS drawing capabilities with JS."),
    ("What about browser compatibility?", "Chrome 65+ and Edge 79+ support Paint Worklet. Safari is implementing it. Firefox doesn't support it yet. Use @supports detection or provide CSS fallbacks."),
    ("How do I register a Paint Worklet?", "Call CSS.paintWorklet.addModule('paint-file.js') in your main JS to load the Worklet. In the Worklet file, use registerPaint() to register the painter class. In CSS, use background: paint(paint-name)."),
    ("How is Paint Worklet different from Canvas?", "Canvas is imperative — you manually manage drawing. Paint Worklet is declarative — driven by CSS properties, the browser automatically calls paint(). Worklet runs in a separate thread without blocking the main thread."),
    ("What pattern types are supported?", "This tool supports 5 base patterns: checkerboard, dots, diagonal stripes, crosshatch, and waves. Each pattern allows custom colors and sizes. Generated code can be further modified."),
    ("Can Paint Worklet access the DOM?", "No. Paint Worklet runs in an isolated Worklet global scope and cannot access DOM, window, or other APIs. It can only use Canvas 2D API for drawing, ensuring performance and security."),
]

en_title = "CSS Houdini Paint Generator - Custom Paint Worklet Code · Pure Frontend"
en_desc = "Free online CSS Houdini Paint Worklet generator. Generate custom CSS drawing code instantly with  with 5 pattern types and live Canvas preview. Pure frontend, no server upload."
en_kw = "CSS Houdini,Paint Worklet,CSS custom painting,CSS paint,CSS pattern generator,Houdini Paint,custom background pattern"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "CSS Houdini Paint Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>🎨 CSS Houdini Paint Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online CSS Houdini Paint Worklet generator. Generate custom CSS drawing code with 5 pattern types and live Canvas preview. Pure frontend.</p>
<div class="options-area">
<div class="option-row">
<label>Pattern: <select id="paintType">
<option value="checkerboard">Checkerboard</option>
<option value="dots">Dots</option>
<option value="stripes">Diagonal Stripes</option>
<option value="crosshatch">Crosshatch</option>
<option value="waves">Waves</option>
</select></label>
<label>Color 1: <input type="color" id="color1" value="#06b6d4" style="width:50px;height:30px"></label>
<label>Color 2: <input type="color" id="color2" value="#1e293b" style="width:50px;height:30px"></label>
<label>Size: <input type="number" id="size" value="20" style="width:60px">px</label>
</div>
</div>
<div class="grid-2">
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Generated Paint Worklet Code</label>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Preview</label>
<div id="preview" style="min-height:200px;display:flex;align-items:center;justify-content:center"></div>
</div></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate Worklet</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Code</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download JS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the CSS Houdini Paint Generator Do?</h2>
<p>The CSS Houdini Paint Generator is a free online tool that helps frontend developers quickly generate CSS Paint Worklet code. Extend CSS background and border drawing capabilities with custom JavaScript logic. 5 base patterns with live Canvas preview. Pure frontend.</p>
<h2>Core Features</h2>
<ul>
<li><strong>5 Pattern Types</strong>: Checkerboard, dots, diagonal stripes, crosshatch, and waves</li>
<li><strong>Custom Colors</strong>: Dual color picker for foreground and background</li>
<li><strong>Size Control</strong>: Adjust pattern unit size for different use cases</li>
<li><strong>Live Preview</strong>: Instant Canvas rendering preview</li>
<li><strong>Complete Code</strong>: Generates full code including registration and CSS usage</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Choose pattern</strong>: Select from 5 base patterns</li>
<li><strong>Set colors</strong>: Pick foreground and background colors</li>
<li><strong>Adjust size</strong>: Set pattern unit pixel size</li>
<li><strong>Generate code</strong>: Click generate and copy the Worklet code</li>
<li><strong>Integrate</strong>: Deploy Worklet file to server, reference with paint() in CSS</li>
</ol>
<h2>Use Cases</h2>
<h3>Custom Background Patterns</h3>
<p>Replace repeating background-image with Paint Worklet for infinite tiling custom pattern backgrounds.</p>
<h3>Dynamic Border Effects</h3>
<p>Combine with CSS custom properties for responsive dynamic border drawing effects.</p>
<h3>Performance Optimization</h3>
<p>Paint Worklet runs in a separate thread without blocking the main thread, ideal for frequently redrawn elements.</p>
<h2>Technical Background</h2>
<p>CSS Houdini is a set of W3C low-level APIs that let developers extend the CSS engine. Paint Worklet is one of the most mature Houdini APIs. Unlike Canvas, Paint Worklet is declarative — the browser automatically calls paint() when needed. Worklet runs in an isolated render thread, never blocking the main thread, making it naturally suited for performance-sensitive drawing scenarios.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "CSS Houdini Paint Generator")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
