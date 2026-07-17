#!/usr/bin/env python3
"""Assemble web-audio-synthesizer CN+EN pages."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools-site/_gen"))
from base import *

SLUG = "web-audio-synthesizer"
JS = open(os.path.expanduser("~/tools-site/_gen/js/web_audio_synth.js"), encoding="utf-8").read()

# ===== CN =====
cn_faqs = [
    ("什么是Web Audio API？", "Web Audio API是浏览器提供的音频处理接口，支持音频生成、处理和分析。可以创建振荡器、滤波器、增益节点等，构建复杂的音频处理图。所有处理在浏览器本地完成。"),
    ("支持哪些波形类型？", "支持4种基本波形：sine（正弦波，纯净音色）、square（方波，8-bit风格）、sawtooth（锯齿波，明亮音色）、triangle（三角波，柔和音色）。不同波形产生不同的音色特征。"),
    ("ADSR包络是什么？", "ADSR是声音的包络参数：Attack（起音时间）、Decay（衰减时间）、Sustain（持续电平）、Release（释放时间）。控制声音从开始到结束的音量变化曲线。"),
    ("滤波器有什么作用？", "滤波器改变声音的频率成分。lowpass滤除高频使声音变暗，highpass滤除低频使声音变亮，bandpass只保留特定频段。配合Q值调节共振强度。"),
    ("可以导出音频文件吗？", "当前版本生成Web Audio API代码，可在浏览器中实时播放。导出WAV文件需要使用MediaRecorder API录制AudioContext输出，本工具暂不支持。"),
    ("和弦功能如何使用？", "点击'播放和弦'按钮，工具会基于当前频率生成大三和弦（根音+大三度+纯五度）。可以调整基频来改变和弦的音高。"),
]

cn_title = "Web音频合成器 - 在线Oscillator+滤波器+ADSR·纯前端"
cn_desc = "免费在线Web音频合成器。支持4种波形、滤波器、ADSR包络控制，实时波形可视化，一键生成Web Audio API代码。纯前端本地处理，无需安装。"
cn_kw = "Web Audio,音频合成器,在线合成器,振荡器,ADSR,滤波器,波形生成,Web Audio API"

cn_html = head_start(cn_title, cn_desc, cn_kw,
    f"https://free-toolbase.com/{SLUG}/", cn_title, cn_desc,
    f"https://free-toolbase.com/{SLUG}/", "Web音频合成器", cn_desc,
    make_faq_json(cn_faqs), "zh", SLUG)

cn_html += """
<div class="tool-section">
<h2>🎵 Web音频合成器 <span class="badge">零依赖·可离线</span></h2>
<p>免费在线Web音频合成器。支持4种波形、滤波器、ADSR包络控制，实时波形可视化，一键生成Web Audio API代码。纯前端本地处理。</p>
<div class="options-area">
<div class="option-row">
<label>波形: <select id="waveform">
<option value="sine">正弦波 (Sine)</option>
<option value="square">方波 (Square)</option>
<option value="sawtooth">锯齿波 (Sawtooth)</option>
<option value="triangle">三角波 (Triangle)</option>
</select></label>
<label>频率: <input type="number" id="frequency" value="440" min="20" max="20000" style="width:80px">Hz</label>
<label>微调: <input type="number" id="detune" value="0" style="width:60px">cents</label>
<label>音量: <input type="number" id="gain" value="0.5" min="0" max="1" step="0.1" style="width:60px"></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">滤波器</div>
<div class="option-row">
<label>类型: <select id="filterType">
<option value="lowpass">低通 (Lowpass)</option>
<option value="highpass">高通 (Highpass)</option>
<option value="bandpass">带通 (Bandpass)</option>
<option value="notch">陷波 (Notch)</option>
</select></label>
<label>截止频率: <input type="number" id="filterFreq" value="2000" style="width:80px">Hz</label>
<label>Q值: <input type="number" id="filterQ" value="1" min="0.1" step="0.1" style="width:60px"></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">ADSR包络</div>
<div class="option-row">
<label>Attack: <input type="number" id="attack" value="0.05" step="0.01" style="width:60px">s</label>
<label>Decay: <input type="number" id="decay" value="0.1" step="0.01" style="width:60px">s</label>
<label>Sustain: <input type="number" id="sustain" value="0.7" min="0" max="1" step="0.1" style="width:60px"></label>
<label>Release: <input type="number" id="release" value="0.3" step="0.01" style="width:60px">s</label>
</div>
</div>
<canvas id="waveCanvas" width="560" height="120" style="width:100%;max-width:560px;border-radius:8px;border:1px solid rgba(148,163,184,.1);margin-bottom:12px"></canvas>
<div class="result-output" id="output" style="min-height:160px">等待播放...</div>
<div class="result-actions">
<button class="btn btn-primary" onclick="playNote()">🎵 播放音符</button>
<button class="btn btn-primary" onclick="playChord()">🎹 播放和弦</button>
<button class="btn btn-secondary" onclick="stopAll()">⏹️ 停止</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 加载示例</button>
<button class="btn btn-success" onclick="copyText('output')">📄 复制代码</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 下载JS</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">快捷键: Ctrl+Enter 播放 | Ctrl+Shift+C 复制</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>Web音频合成器能做什么？</h2>
<p>Web音频合成器是一款免费在线工具，基于Web Audio API实现浏览器端音频合成。支持4种波形、滤波器、ADSR包络控制，实时波形可视化，一键生成可复用的Web Audio代码。纯前端处理。</p>
<h2>核心功能</h2>
<ul>
<li><strong>4种波形</strong>：正弦波、方波、锯齿波、三角波，覆盖常见音色需求</li>
<li><strong>滤波器</strong>：低通、高通、带通、陷波4种滤波器，可调截止频率和Q值</li>
<li><strong>ADSR包络</strong>：完整的Attack-Decay-Sustain-Release包络控制</li>
<li><strong>和弦播放</strong>：一键生成大三和弦，支持自定义基频</li>
<li><strong>波形可视化</strong>：实时显示音频波形，直观感受参数变化</li>
<li><strong>代码生成</strong>：一键导出Web Audio API代码，可直接在项目中使用</li>
</ul>
<h2>使用教程</h2>
<ol>
<li><strong>选择波形</strong>：根据需要的音色选择波形类型</li>
<li><strong>设置频率</strong>：调整音高（440Hz=A4音）</li>
<li><strong>配置滤波器</strong>：选择滤波器类型和参数</li>
<li><strong>调整ADSR</strong>：设置声音的起音、衰减、持续和释放</li>
<li><strong>播放试听</strong>：点击播放音符或和弦试听效果</li>
<li><strong>导出代码</strong>：复制生成的Web Audio代码到项目</li>
</ol>
<h2>应用场景</h2>
<h3>场景1：Web音频开发学习</h3>
<p>直观理解Web Audio API的振荡器、滤波器、包络等概念，实时调参试听效果。</p>
<h3>场景2：游戏音效原型</h3>
<p>快速设计游戏音效参数，生成代码直接集成到Web游戏中。</p>
<h3>场景3：音乐应用开发</h3>
<p>作为Web音乐应用的基础合成器模块，生成可复用的音频代码。</p>
<h2>扩展知识</h2>
<p>Web Audio API是现代浏览器提供的强大音频处理框架。AudioContext是核心对象，各种AudioNode（OscillatorNode、BiquadFilterNode、GainNode等）通过connect()方法连接成处理图。ADSR包络源自模拟合成器，是声音设计的核心概念。Web Audio API还支持ConvolverNode（混响）、DelayNode（延迟）、DynamicsCompressorNode（压缩）等高级效果。</p>
</div>
"""
cn_html += faq_html(cn_faqs, "zh")
cn_html += footer("zh", SLUG, "Web音频合成器")
cn_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(cn_html)
print(f"Written: {SLUG}/index.html ({len(cn_html)} bytes)")

# ===== EN =====
en_faqs = [
    ("What is the Web Audio API?", "The Web Audio API is a browser audio processing interface that supports audio generation, processing, and analysis. You can create oscillators, filters, gain nodes, and build complex audio processing graphs. All processing happens locally in the browser."),
    ("What waveform types are supported?", "4 basic waveforms: sine (pure tone), square (8-bit style), sawtooth (bright tone), and triangle (soft tone). Different waveforms produce different timbral characteristics."),
    ("What is ADSR envelope?", "ADSR stands for Attack (onset time), Decay (fall time), Sustain (hold level), and Release (fade time). It controls the volume curve of a sound from start to end."),
    ("What does the filter do?", "Filters change the frequency content of sound. Lowpass removes highs for a darker sound, highpass removes lows for brightness, bandpass keeps only a specific frequency range. Q controls resonance intensity."),
    ("Can I export audio files?", "The current version generates Web Audio API code for real-time browser playback. Exporting WAV files requires MediaRecorder API to record AudioContext output, which this tool doesn't support yet."),
    ("How does the chord feature work?", "Click 'Play Chord' to generate a major triad (root + major third + perfect fifth) based on the current frequency. Adjust the base frequency to change the chord pitch."),
]

en_title = "Web Audio Synthesizer - Online Oscillator+Filter+ADSR · Pure Frontend"
en_desc = "Free online Web Audio synthesizer. 4 waveforms, filter, ADSR envelope control, real-time waveform visualization, one-click Web Audio API code generation. Pure frontend, no installation needed."
en_kw = "Web Audio,audio synthesizer,online synthesizer,oscillator,ADSR,filter,waveform generator,Web Audio API"

en_html = head_start(en_title, en_desc, en_kw,
    f"https://free-toolbase.com/en/{SLUG}/", en_title, en_desc,
    f"https://free-toolbase.com/en/{SLUG}/", "Web Audio Synthesizer", en_desc,
    make_faq_json(en_faqs), "en", SLUG)

en_html += """
<div class="tool-section">
<h2>🎵 Web Audio Synthesizer <span class="badge">Zero Dependencies · Offline</span></h2>
<p>Free online Web Audio synthesizer. 4 waveforms, filter, ADSR envelope control, real-time waveform visualization, one-click code generation. Pure frontend.</p>
<div class="options-area">
<div class="option-row">
<label>Waveform: <select id="waveform">
<option value="sine">Sine</option>
<option value="square">Square</option>
<option value="sawtooth">Sawtooth</option>
<option value="triangle">Triangle</option>
</select></label>
<label>Frequency: <input type="number" id="frequency" value="440" min="20" max="20000" style="width:80px">Hz</label>
<label>Detune: <input type="number" id="detune" value="0" style="width:60px">cents</label>
<label>Volume: <input type="number" id="gain" value="0.5" min="0" max="1" step="0.1" style="width:60px"></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">Filter</div>
<div class="option-row">
<label>Type: <select id="filterType">
<option value="lowpass">Lowpass</option>
<option value="highpass">Highpass</option>
<option value="bandpass">Bandpass</option>
<option value="notch">Notch</option>
</select></label>
<label>Cutoff: <input type="number" id="filterFreq" value="2000" style="width:80px">Hz</label>
<label>Q: <input type="number" id="filterQ" value="1" min="0.1" step="0.1" style="width:60px"></label>
</div>
<div class="option-row" style="color:#94a3b8;font-size:.85rem">ADSR Envelope</div>
<div class="option-row">
<label>Attack: <input type="number" id="attack" value="0.05" step="0.01" style="width:60px">s</label>
<label>Decay: <input type="number" id="decay" value="0.1" step="0.01" style="width:60px">s</label>
<label>Sustain: <input type="number" id="sustain" value="0.7" min="0" max="1" step="0.1" style="width:60px"></label>
<label>Release: <input type="number" id="release" value="0.3" step="0.01" style="width:60px">s</label>
</div>
</div>
<canvas id="waveCanvas" width="560" height="120" style="width:100%;max-width:560px;border-radius:8px;border:1px solid rgba(148,163,184,.1);margin-bottom:12px"></canvas>
<div class="result-output" id="output" style="min-height:160px">Waiting...</div>
<div class="result-actions">
<button class="btn btn-primary" onclick="playNote()">🎵 Play Note</button>
<button class="btn btn-primary" onclick="playChord()">🎹 Play Chord</button>
<button class="btn btn-secondary" onclick="stopAll()">⏹️ Stop</button>
<button class="btn btn-secondary" onclick="loadExample()">📋 Load Example</button>
<button class="btn btn-success" onclick="copyText('output')">📄 Copy Code</button>
<button class="btn btn-secondary" onclick="downloadOutput()">💾 Download JS</button>
</div>
<div style="margin-top:8px;color:#64748b;font-size:.75rem">Shortcuts: Ctrl+Enter Play | Ctrl+Shift+C Copy</div>
</div>

<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>

<div class="tool-section seo-content">
<h2>What Can the Web Audio Synthesizer Do?</h2>
<p>The Web Audio Synthesizer is a free online tool built on the Web Audio API for browser-based audio synthesis. 4 waveforms, filter, ADSR envelope, real-time waveform visualization, and one-click code generation. Pure frontend.</p>
<h2>Core Features</h2>
<ul>
<li><strong>4 Waveforms</strong>: Sine, square, sawtooth, and triangle covering common timbre needs</li>
<li><strong>Filters</strong>: Lowpass, highpass, bandpass, and notch with adjustable cutoff and Q</li>
<li><strong>ADSR Envelope</strong>: Full Attack-Decay-Sustain-Release control</li>
<li><strong>Chord Playback</strong>: One-click major triad generation with custom base frequency</li>
<li><strong>Waveform Visualization</strong>: Real-time audio waveform display</li>
<li><strong>Code Generation</strong>: Export Web Audio API code for direct project integration</li>
</ul>
<h2>How to Use</h2>
<ol>
<li><strong>Choose waveform</strong>: Select based on desired timbre</li>
<li><strong>Set frequency</strong>: Adjust pitch (440Hz = A4)</li>
<li><strong>Configure filter</strong>: Select filter type and parameters</li>
<li><strong>Adjust ADSR</strong>: Set attack, decay, sustain, and release</li>
<li><strong>Play and listen</strong>: Click Play Note or Play Chord to hear the result</li>
<li><strong>Export code</strong>: Copy generated Web Audio code to your project</li>
</ol>
<h2>Use Cases</h2>
<h3>Web Audio Learning</h3>
<p>Visually understand Web Audio API concepts — oscillators, filters, envelopes — with real-time parameter adjustment.</p>
<h3>Game Sound Effects</h3>
<p>Quickly design game sound effect parameters and generate code for direct integration into web games.</p>
<h3>Music App Development</h3>
<p>Use as a base synthesizer module for web music applications with reusable audio code.</p>
<h2>Technical Background</h2>
<p>The Web Audio API is a powerful audio processing framework in modern browsers. AudioContext is the core object; various AudioNodes (OscillatorNode, BiquadFilterNode, GainNode, etc.) connect via connect() to form processing graphs. ADSR envelopes originate from analog synthesizers and are a core sound design concept. The API also supports ConvolverNode (reverb), DelayNode (delay), and DynamicsCompressorNode (compression) for advanced effects.</p>
</div>
"""
en_html += faq_html(en_faqs, "en")
en_html += footer("en", SLUG, "Web Audio Synthesizer")
en_html += "<script>\n" + JS + "\n</script>\n</body></html>"

with open(os.path.join(BASE, "en", SLUG, "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)
print(f"Written: en/{SLUG}/index.html ({len(en_html)} bytes)")
