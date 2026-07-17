#!/usr/bin/env python3
"""Assemble debounce-throttle-generator CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "debounce-throttle-generator"
JS = open(os.path.expanduser("~/tools-site/_gen/js/debounce_throttle.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("防抖(debounce)和节流(throttle)有什么区别？", "防抖：在连续触发后等待一段时间才执行，如果期间再次触发则重新计时。适合搜索输入、窗口resize。节流：在指定时间间隔内最多执行一次，不管触发多少次。适合滚动事件、鼠标移动。"),
    ("leading和trailing选项是什么？", "leading：是否在等待期开始时立即执行一次。trailing：是否在等待期结束后执行最后一次。默认防抖trailing=true，节流leading=true。"),
    ("maxWait参数有什么用？", "maxWait是节流函数的选项，设置最大等待时间。即使持续触发，超过maxWait也会强制执行一次，防止函数长时间不被调用。类似lodash的throttle实现。"),
    ("生成的代码可以直接使用吗？", "可以。生成的代码是纯JavaScript，无任何依赖，可直接复制到项目中使用。支持ES5+语法，兼容所有现代浏览器。"),
    ("什么场景用防抖？", "搜索框输入联想、表单验证、窗口resize处理、按钮防重复点击、自动保存等场景。核心是'等用户停止操作后再执行'。"),
    ("什么场景用节流？", "滚动事件处理、鼠标移动追踪、拖拽更新、游戏循环、API轮询等场景。核心是'固定频率执行，不超频'。"),
]

cn_title = "防抖节流函数生成器 - Debounce/Throttle代码·纯前端"
cn_desc = "免费在线防抖节流函数生成器。一键生成JavaScript debounce和throttle函数代码，支持leading/trailing选项和maxWait配置。纯前端本地处理，代码不上传服务器。"
cn_kw = "防抖,节流,debounce,throttle,JavaScript防抖,JS节流,函数防抖,函数节流,前端性能优化"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "防抖节流函数生成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>⚡ 防抖节流函数生成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线防抖节流函数生成器。一键生成JavaScript debounce和throttle函数代码，支持leading/trailing选项和maxWait配置。纯前端本地处理。</p>
<div class="options-area">
<div class="option-row">
<label>模式: <select id="mode"><option value="debounce">防抖 (Debounce)</option><option value="throttle">节流 (Throttle)</option></select></label>
<label>函数名: <input type="text" id="funcName" value="handleSearch" style="width:140px"></label>
<label>延迟: <input type="number" id="delay" value="300" style="width:80px">ms</label>
</div>
<div class="option-row">
<label><input type="checkbox" id="leading"> leading (首次立即执行)</label>
<label><input type="checkbox" id="trailing" checked> trailing (末次延迟执行)</label>
<label>maxWait: <input type="text" id="maxWait" placeholder="可选" style="width:80px">ms</label>
</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">函数体（可选）</label>
<textarea id="funcBody" rows="3" placeholder='console.log("Searching for:", query);' style="min-height:60px"></textarea>
</div>
<div class="result-output" id="output" style="min-height:200px">等待生成...</div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ 生成函数</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制代码</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载JS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 生成 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>防抖节流函数生成器能做什么？</h2>
<p>防抖节流函数生成器是一款免费在线工具，帮助前端开发者快速生成JavaScript debounce和throttle函数代码。无需手写复杂的定时器逻辑，配置参数即可生成生产级代码。纯前端处理，代码不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>防抖/节流双模式</strong>：一键切换debounce和throttle，生成对应实现</li>
<li><strong>leading/trailing选项</strong>：控制首次和末次执行行为，满足不同场景需求</li>
<li><strong>maxWait支持</strong>：节流模式支持最大等待时间，防止长时间不执行</li>
<li><strong>自定义函数体</strong>：可输入实际业务逻辑，生成即用代码</li>
<li><strong>零依赖</strong>：生成代码无任何外部依赖，ES5+兼容</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>选择模式</strong>：根据需求选择防抖或节流</li>
<li><strong>设置参数</strong>：输入函数名、延迟时间、选项</li>
<li><strong>输入函数体</strong>：可选输入实际业务代码</li>
<li><strong>生成代码</strong>：点击生成按钮，复制代码到项目</li>
<li><strong>调用函数</strong>：用生成的包装函数替代原始调用</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：搜索输入防抖</h3>
<p>用户输入搜索词时，等待停止输入300ms后再发送API请求，避免每次按键都请求。</p>
<h3>场景2：滚动事件节流</h3>
<p>监听scroll事件时，每16ms最多执行一次，保证60fps流畅度。</p>
<h3>场景3：窗口resize防抖</h3>
<p>窗口大小变化时，等用户停止调整后再重新计算布局，避免频繁重排。</p>
<h2>扩展知识</h2>
<p>防抖和节流是前端性能优化的两大核心手段。Lodash的_.debounce和_.throttle是最流行的实现，但引入整个lodash会增加包体积。本工具生成的代码是零依赖的独立实现，功能完整且体积小。requestAnimationFrame也可用于视觉更新的节流，但不适合通用场景。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "防抖节流函数生成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What's the difference between debounce and throttle?", "Debounce: waits for a pause in triggering before executing. If triggered again during the wait, the timer resets. Best for search input, window resize. Throttle: executes at most once per time interval regardless of how many times triggered. Best for scroll events, mouse move."),
    ("What are leading and trailing options?", "Leading: whether to execute immediately at the start of the wait period. Trailing: whether to execute the last call after the wait period. Default debounce has trailing=true, throttle has leading=true."),
    ("What is maxWait for?", "maxWait is a throttle option that sets the maximum wait time. Even with continuous triggers, the function will execute at least once after maxWait, preventing long periods without execution. Similar to lodash's throttle implementation."),
    ("Can I use the generated code directly?", "Yes. The generated code is pure JavaScript with zero dependencies. Copy it directly into your project. Supports ES5+ syntax and all modern browsers."),
    ("When should I use debounce?", "Search input autocomplete, form validation, window resize handling, preventing double-clicks, auto-save. The key idea is 'wait until the user stops, then execute'."),
    ("When should I use throttle?", "Scroll event handling, mouse move tracking, drag updates, game loops, API polling. The key idea is 'execute at a fixed rate, never exceed'."),
]

en_title = "Debounce/Throttle Generator - JavaScript Function Code · Pure Frontend"
en_desc = "Free online debounce/throttle function generator. Generate JavaScript debounce and throttle code instantly with leading/trailing options and maxWait support. Pure frontend, no server upload."
en_kw = "debounce,throttle,JavaScript debounce,JS throttle,function debounce,function throttle,frontend performance"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "Debounce/Throttle Generator", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>⚡ Debounce/Throttle Generator <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online debounce/throttle function generator. Generate JavaScript debounce and throttle code instantly with leading/trailing options and maxWait support. Pure frontend.</p>
<div class="options-area">
<div class="option-row">
<label>Mode: <select id="mode"><option value="debounce">Debounce</option><option value="throttle">Throttle</option></select></label>
<label>Function: <input type="text" id="funcName" value="handleSearch" style="width:140px"></label>
<label>Delay: <input type="number" id="delay" value="300" style="width:80px">ms</label>
</div>
<div class="option-row">
<label><input type="checkbox" id="leading"> leading (execute on first call)</label>
<label><input type="checkbox" id="trailing" checked> trailing (execute after delay)</label>
<label>maxWait: <input type="text" id="maxWait" placeholder="optional" style="width:80px">ms</label>
</div>
</div>
<div class="input-area">
<label style="color:#94a3b8;font-size:.85rem">Function Body (optional)</label>
<textarea id="funcBody" rows="3" placeholder='console.log("Searching for:", query);' style="min-height:60px"></textarea>
</div>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">⚡ Generate Function</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Code</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download JS</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Generate | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the Debounce/Throttle Generator Do?</h2>
<p>The Debounce/Throttle Generator is a free online tool that helps frontend developers quickly generate JavaScript debounce and throttle function code. No need to write complex timer logic — configure parameters and get production-ready code. Pure frontend, no uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Debounce/Throttle Dual Mode</strong>: Switch between debounce and throttle with one click</li>
<li><strong>Leading/Trailing Options</strong>: Control first and last execution behavior for different scenarios</li>
<li><strong>maxWait Support</strong>: Throttle mode supports maximum wait time to prevent long execution gaps</li>
<li><strong>Custom Function Body</strong>: Input your actual business logic for ready-to-use code</li>
<li><strong>Zero Dependencies</strong>: Generated code has no external dependencies, ES5+ compatible</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Choose mode</strong>: Select debounce or throttle based on your needs</li>
<li><strong>Set parameters</strong>: Enter function name, delay, and options</li>
<li><strong>Input function body</strong>: Optionally enter your business logic</li>
<li><strong>Generate code</strong>: Click generate and copy the code to your project</li>
<li><strong>Call the function</strong>: Replace direct calls with the generated wrapper</li>
</ol>
<h2>Use Cases</h2>
<h3>Search Input Debounce</h3>
<p>Wait 300ms after the user stops typing before sending API requests, avoiding requests on every keystroke.</p>
<h3>Scroll Event Throttle</h3>
<p>Execute scroll handlers at most once every 16ms for smooth 60fps performance.</p>
<h3>Window Resize Debounce</h3>
<p>Wait for the user to stop resizing before recalculating layout, avoiding frequent reflows.</p>
<h2>Technical Background</h2>
<p>Debounce and throttle are two core frontend performance optimization techniques. Lodash's _.debounce and _.throttle are the most popular implementations, but importing all of lodash increases bundle size. This tool generates zero-dependency standalone implementations that are feature-complete and lightweight. requestAnimationFrame can also be used for visual update throttling but isn't suitable for general-purpose scenarios.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "Debounce/Throttle Generator")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
