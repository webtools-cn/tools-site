#!/usr/bin/env python3
"""Assemble js-benchmark CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "js-benchmark"
JS = open(os.path.expanduser("~/tools-site/_gen/js/js_benchmark.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("什么是JavaScript性能基准测试？", "JavaScript性能基准测试是通过多次运行代码片段并测量执行时间来比较不同实现性能的方法。帮助开发者选择更高效的代码写法，优化应用性能。"),
    ("测试结果准确吗？", "本工具运行5轮测试取平均值，包含预热阶段消除JIT编译影响。但浏览器环境受CPU负载、内存状态等因素影响，建议多次测试取稳定结果。"),
    ("为什么需要预热？", "现代JavaScript引擎使用JIT编译，首次执行代码时会进行编译优化，速度较慢。预热让引擎完成优化后再计时，确保测试的是优化后的性能。"),
    ("可以测试异步代码吗？", "当前版本仅支持同步代码测试。异步代码（Promise、setTimeout）的执行时间无法通过简单的循环测量，需要专门的异步基准测试工具。"),
    ("iterations参数是什么？", "iterations是每轮测试中代码执行的次数。次数越多，单次执行的平均误差越小，但总测试时间越长。建议100-10000之间。"),
    ("如何解读测试结果？", "关注平均耗时和吞吐量(ops/sec)。对比两段代码时，速度倍数(Speedup)是最直观的指标。注意各轮结果的一致性，波动大说明受系统干扰。"),
]

cn_title = "JS性能基准测试 - JavaScript Benchmark对比·纯前端"
cn_desc = "免费在线JavaScript性能基准测试工具。对比两段JS代码的执行速度，可视化展示测试结果，支持自定义迭代次数和预热。纯前端本地处理，代码不上传服务器。"
cn_kw = "JS性能测试,JavaScript基准测试,JS Benchmark,代码性能对比,JavaScript性能优化,前端性能测试"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "JS性能基准测试", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>📊 JS性能基准测试 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线JavaScript性能基准测试工具。对比两段JS代码的执行速度，可视化展示测试结果，帮助选择更高效的代码实现。纯前端本地处理。</p>
<div class="grid-2">
<div class="input-area">
<label style="color:#06b6d4;font-size:.85rem;font-weight:600">代码 A</label>
<textarea id="codeA" rows="6" placeholder='// 代码A: Array.map\nconst result = Array.from({length: 10000}, (_, i) => i).map(x => x * 2);'></textarea>
</div>
<div class="input-area">
<label style="color:#a855f7;font-size:.85rem;font-weight:600">代码 B（可选对比）</label>
<textarea id="codeB" rows="6" placeholder='// 代码B: For loop\nconst arr = Array.from({length: 10000}, (_, i) => i);\nconst result = [];\nfor (let i = 0; i < arr.length; i++) {\n  result.push(arr[i] * 2);\n}'></textarea>
</div>
</div>
<div class="options-area">
<div class="option-row">
<label>迭代次数: <input type="number" id="iterations" value="1000" style="width:100px"></label>
<label>预热轮数: <input type="number" id="warmup" value="10" style="width:80px"></label>
</div>
</div>
<div class="result-output" id="output" style="min-height:200px">等待测试...</div>
<div id="chartArea" style="margin:12px 0"></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">🚀 开始测试</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制结果</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ 清空</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 测试 | Ctrl+Shift+C 复制 | Ctrl+Shift+X 清空</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>JS性能基准测试能做什么？</h2>
<p>JS性能基准测试是一款免费在线工具，帮助开发者对比不同JavaScript代码实现的执行速度。通过多次迭代和预热消除JIT编译影响，提供准确的性能数据和可视化图表。纯前端处理，代码不上传。</p>
<h2>核心功能</h2>
<ul>
<li><strong>双代码对比</strong>：同时测试两段代码，直观对比性能差异</li>
<li><strong>多轮测试</strong>：5轮测试取平均值，减少随机误差</li>
<li><strong>JIT预热</strong>：预热阶段消除首次编译影响，测试优化后性能</li>
<li><strong>可视化图表</strong>：柱状图展示各轮耗时，一目了然</li>
<li><strong>吞吐量计算</strong>：自动计算ops/sec，量化代码性能</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>输入代码</strong>：在代码A和B区域输入要对比的JS代码</li>
<li><strong>设置参数</strong>：调整迭代次数和预热轮数</li>
<li><strong>运行测试</strong>：点击开始测试，等待结果</li>
<li><strong>分析结果</strong>：查看平均耗时、吞吐量和速度倍数</li>
<li><strong>优化代码</strong>：根据结果选择更高效的实现</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：数组方法对比</h3>
<p>对比Array.map vs for循环、Array.filter vs Array.reduce等不同数组操作的性能。</p>
<h3>场景2：字符串操作优化</h3>
<p>对比字符串拼接的不同方式：+运算符、模板字符串、Array.join等。</p>
<h3>场景3：DOM操作优化</h3>
<p>对比innerHTML vs createElement、querySelector vs getElementById等DOM操作的性能。</p>
<h2>扩展知识</h2>
<p>JavaScript引擎（V8、SpiderMonkey、JavaScriptCore）都使用JIT编译优化代码。首次执行时解释运行，热点代码会被编译为机器码。因此基准测试需要预热来消除编译开销。V8的TurboFan优化编译器会根据类型反馈进行内联和逃逸分析，相同逻辑不同写法可能产生显著性能差异。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "JS性能基准测试")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What is JavaScript performance benchmarking?", "JavaScript performance benchmarking compares the execution speed of different code implementations by running them multiple times and measuring elapsed time. It helps developers choose more efficient code patterns and optimize application performance."),
    ("Are the test results accurate?", "This tool runs 5 rounds of tests with averaged results and includes a warmup phase to eliminate JIT compilation effects. However, browser performance varies with CPU load and memory state, so run multiple tests for stable results."),
    ("Why is warmup needed?", "Modern JavaScript engines use JIT compilation. First-time code execution includes compilation overhead and is slower. Warmup lets the engine complete optimization before timing begins, ensuring we measure optimized performance."),
    ("Can I test async code?", "The current version only supports synchronous code testing. Async code (Promise, setTimeout) execution time can't be measured through simple loops and requires specialized async benchmarking tools."),
    ("What is the iterations parameter?", "Iterations is the number of times the code runs per test round. More iterations reduce per-execution error but increase total test time. Recommended range: 100-10000."),
    ("How to interpret results?", "Focus on average time and throughput (ops/sec). When comparing two code snippets, the Speedup factor is the most intuitive metric. Check consistency across rounds — high variance indicates system interference."),
]

en_title = "JS Performance Benchmark - JavaScript Code Comparison · Pure Frontend"
en_desc = "Free online JavaScript performance benchmark tool. Compare execution speed of two JS code snippets with visual charts, custom iterations and warmup. Pure frontend, no server upload."
en_kw = "JS benchmark,JavaScript benchmark,JS performance test,code performance comparison,JavaScript optimization,frontend performance"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "JS Performance Benchmark", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>📊 JS Performance Benchmark <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online JavaScript performance benchmark tool. Compare execution speed of two JS code snippets with visual charts and accurate measurements. Pure frontend.</p>
<div class="grid-2">
<div class="input-area">
<label style="color:#06b6d4;font-size:.85rem;font-weight:600">Code A</label>
<textarea id="codeA" rows="6" placeholder='// Code A: Array.map\nconst result = Array.from({length: 10000}, (_, i) => i).map(x => x * 2);'></textarea>
</div>
<div class="input-area">
<label style="color:#a855f7;font-size:.85rem;font-weight:600">Code B (optional comparison)</label>
<textarea id="codeB" rows="6" placeholder='// Code B: For loop\nconst arr = Array.from({length: 10000}, (_, i) => i);\nconst result = [];\nfor (let i = 0; i < arr.length; i++) {\n  result.push(arr[i] * 2);\n}'></textarea>
</div>
</div>
<div class="options-area">
<div class="option-row">
<label>Iterations: <input type="number" id="iterations" value="1000" style="width:100px"></label>
<label>Warmup: <input type="number" id="warmup" value="10" style="width:80px"></label>
</div>
</div>
<div class="result-output" id="output" style="min-height:200px">Waiting...</div>
<div id="chartArea" style="margin:12px 0"></div>
<div class="result-actions">
<button class="btn btn-primary" onclick="execute()">🚀 Run Benchmark</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Results</button>
<button class="btn btn-secondary" onclick="clearInput()">🗑️ Clear</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Run | Ctrl+Shift+C Copy | Ctrl+Shift+X Clear</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the JS Performance Benchmark Do?</h2>
<p>The JS Performance Benchmark is a free online tool that helps developers compare the execution speed of different JavaScript implementations. Multiple iterations and warmup eliminate JIT compilation effects for accurate results with visual charts. Pure frontend, no uploads.</p>
<h2>Core Features</h2>
<ul>
<li><strong>Dual Code Comparison</strong>: Test two code snippets side by side with intuitive performance comparison</li>
<li><strong>Multiple Rounds</strong>: 5 rounds of tests with averaged results to reduce random error</li>
<li><strong>JIT Warmup</strong>: Warmup phase eliminates first-time compilation overhead</li>
<li><strong>Visual Charts</strong>: Bar charts show per-round timing at a glance</li>
<li><strong>Throughput Calculation</strong>: Auto-calculates ops/sec to quantify code performance</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Enter code</strong>: Input JS code in Code A and B areas</li>
<li><strong>Set parameters</strong>: Adjust iterations and warmup rounds</li>
<li><strong>Run test</strong>: Click Run Benchmark and wait for results</li>
<li><strong>Analyze results</strong>: Check average time, throughput, and speedup factor</li>
<li><strong>Optimize code</strong>: Choose the more efficient implementation based on results</li>
</ol>
<h2>Use Cases</h2>
<h3>Array Method Comparison</h3>
<p>Compare Array.map vs for loop, Array.filter vs Array.reduce, and other array operations.</p>
<h3>String Operation Optimization</h3>
<p>Compare string concatenation methods: + operator, template literals, Array.join.</p>
<h3>DOM Operation Optimization</h3>
<p>Compare innerHTML vs createElement, querySelector vs getElementById performance.</p>
<h2>Technical Background</h2>
<p>JavaScript engines (V8, SpiderMonkey, JavaScriptCore) all use JIT compilation to optimize code. First execution is interpreted; hot code gets compiled to machine code. Benchmarks need warmup to eliminate compilation overhead. V8's TurboFan optimizer performs inlining and escape analysis based on type feedback, so identical logic with different patterns can produce significantly different performance.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "JS Performance Benchmark")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
