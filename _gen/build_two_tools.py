#!/usr/bin/env python3
"""Build 2 new tools using template v3"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# Tool 1: Word Counter / 字数统计器
# ============================================================

tool_js_word_counter = r'''
function updateCount() {
  var text = document.getElementById('wc-input').value;
  var chars = text.length;
  var charsNoSpace = text.replace(/\s/g, '').length;
  var words = text.trim() ? text.trim().split(/\s+/).length : 0;
  var sentences = text ? (text.match(/[.!?。！？]+/g) || []).length : 0;
  if (text && !/[.!?。！？]$/.test(text.trim())) sentences = Math.max(1, sentences);
  var paragraphs = text ? text.split(/\n\s*\n/).filter(function(p){return p.trim()}).length : 0;
  var lines = text ? text.split('\n').length : 0;
  var readingTime = Math.max(1, Math.ceil(words / 200));
  var speakingTime = Math.max(1, Math.ceil(words / 150));
  document.getElementById('wc-chars').textContent = chars.toLocaleString();
  document.getElementById('wc-chars-nospace').textContent = charsNoSpace.toLocaleString();
  document.getElementById('wc-words').textContent = words.toLocaleString();
  document.getElementById('wc-sentences').textContent = sentences.toLocaleString();
  document.getElementById('wc-paragraphs').textContent = paragraphs.toLocaleString();
  document.getElementById('wc-lines').textContent = lines.toLocaleString();
  document.getElementById('wc-reading').textContent = readingTime + ' min';
  document.getElementById('wc-speaking').textContent = speakingTime + ' min';
}
function clearText() {
  document.getElementById('wc-input').value = '';
  updateCount();
}
function pasteText() {
  navigator.clipboard.readText().then(function(t) {
    document.getElementById('wc-input').value = t;
    updateCount();
    showToast('Text pasted');
  }).catch(function(){showToast('Paste failed');});
}
'''

tool_html_cn_wc = '''
<div class="word-counter">
  <div class="form-group">
    <label>输入或粘贴文本</label>
    <textarea id="wc-input" style="width:100%;min-height:200px;padding:12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;outline:none;resize:vertical" oninput="updateCount()" placeholder="在此输入或粘贴文本..."></textarea>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn btn-primary" onclick="pasteText()">📋 粘贴</button>
    <button class="btn btn-danger" onclick="clearText()">🗑️ 清空</button>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px">
    <div class="stat-card"><div class="num" id="wc-chars">0</div><div class="lbl">字符数</div></div>
    <div class="stat-card"><div class="num" id="wc-chars-nospace">0</div><div class="lbl">不含空格</div></div>
    <div class="stat-card"><div class="num" id="wc-words">0</div><div class="lbl">单词数</div></div>
    <div class="stat-card"><div class="num" id="wc-sentences">0</div><div class="lbl">句子数</div></div>
    <div class="stat-card"><div class="num" id="wc-paragraphs">0</div><div class="lbl">段落数</div></div>
    <div class="stat-card"><div class="num" id="wc-lines">0</div><div class="lbl">行数</div></div>
    <div class="stat-card"><div class="num" id="wc-reading">0 min</div><div class="lbl">阅读时间</div></div>
    <div class="stat-card"><div class="num" id="wc-speaking">0 min</div><div class="lbl">朗读时间</div></div>
  </div>
</div>
<style>
.stat-card{background:#0f172a;border-radius:10px;padding:14px 10px;text-align:center;border:1px solid rgba(148,163,184,.1)}.stat-card .num{font-size:1.3rem;font-weight:700;color:#f1c40f;margin-bottom:4px}.stat-card .lbl{font-size:.75rem;color:#64748b}
.btn{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee}.btn-primary:hover{background:rgba(6,182,212,.35)}
.btn-danger{background:rgba(239,68,68,.15);color:#f87171}.btn-danger:hover{background:rgba(239,68,68,.3)}
</style>
'''

tool_html_en_wc = '''
<div class="word-counter">
  <div class="form-group">
    <label>Enter or paste text</label>
    <textarea id="wc-input" style="width:100%;min-height:200px;padding:12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;outline:none;resize:vertical" oninput="updateCount()" placeholder="Type or paste text here..."></textarea>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn btn-primary" onclick="pasteText()">📋 Paste</button>
    <button class="btn btn-danger" onclick="clearText()">🗑️ Clear</button>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px">
    <div class="stat-card"><div class="num" id="wc-chars">0</div><div class="lbl">Characters</div></div>
    <div class="stat-card"><div class="num" id="wc-chars-nospace">0</div><div class="lbl">No Spaces</div></div>
    <div class="stat-card"><div class="num" id="wc-words">0</div><div class="lbl">Words</div></div>
    <div class="stat-card"><div class="num" id="wc-sentences">0</div><div class="lbl">Sentences</div></div>
    <div class="stat-card"><div class="num" id="wc-paragraphs">0</div><div class="lbl">Paragraphs</div></div>
    <div class="stat-card"><div class="num" id="wc-lines">0</div><div class="lbl">Lines</div></div>
    <div class="stat-card"><div class="num" id="wc-reading">0 min</div><div class="lbl">Reading Time</div></div>
    <div class="stat-card"><div class="num" id="wc-speaking">0 min</div><div class="lbl">Speaking Time</div></div>
  </div>
</div>
<style>
.stat-card{background:#0f172a;border-radius:10px;padding:14px 10px;text-align:center;border:1px solid rgba(148,163,184,.1)}.stat-card .num{font-size:1.3rem;font-weight:700;color:#f1c40f;margin-bottom:4px}.stat-card .lbl{font-size:.75rem;color:#64748b}
.btn{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee}.btn-primary:hover{background:rgba(6,182,212,.35)}
.btn-danger{background:rgba(239,68,68,.15);color:#f87171}.btn-danger:hover{background:rgba(239,68,68,.3)}
</style>
'''

# ============================================================
# Tool 2: Password Strength Checker / 密码强度检测器
# ============================================================

tool_js_password = r'''
function checkStrength() {
  var pwd = document.getElementById('pwd-input').value;
  var score = 0;
  var checks = {};
  checks.length = pwd.length >= 8;
  checks.upper = /[A-Z]/.test(pwd);
  checks.lower = /[a-z]/.test(pwd);
  checks.digit = /\d/.test(pwd);
  checks.symbol = /[^A-Za-z0-9]/.test(pwd);
  
  var passed = 0;
  for (var k in checks) { if (checks[k]) passed++; }
  
  // Calculate score
  if (pwd.length >= 8) score += 25;
  if (pwd.length >= 12) score += 10;
  if (pwd.length >= 16) score += 5;
  if (checks.upper) score += 15;
  if (checks.lower) score += 15;
  if (checks.digit) score += 15;
  if (checks.symbol) score += 15;
  if (pwd.length >= 20) score += 5;
  score = Math.min(100, score);
  
  // Update checks display
  document.getElementById('check-length').className = 'check-item ' + (checks.length ? 'pass' : 'fail');
  document.getElementById('check-upper').className = 'check-item ' + (checks.upper ? 'pass' : 'fail');
  document.getElementById('check-lower').className = 'check-item ' + (checks.lower ? 'pass' : 'fail');
  document.getElementById('check-digit').className = 'check-item ' + (checks.digit ? 'pass' : 'fail');
  document.getElementById('check-symbol').className = 'check-item ' + (checks.symbol ? 'pass' : 'fail');
  
  // Update bar
  var bar = document.getElementById('strength-bar');
  var label = document.getElementById('strength-label');
  var scoreEl = document.getElementById('strength-score');
  bar.style.width = score + '%';
  scoreEl.textContent = score + '/100';
  
  if (score < 20) { bar.style.background = '#ef4444'; label.textContent = 'Very Weak'; label.style.color = '#ef4444'; }
  else if (score < 40) { bar.style.background = '#f97316'; label.textContent = 'Weak'; label.style.color = '#f97316'; }
  else if (score < 60) { bar.style.background = '#eab308'; label.textContent = 'Fair'; label.style.color = '#eab308'; }
  else if (score < 80) { bar.style.background = '#22c55e'; label.textContent = 'Strong'; label.style.color = '#22c55e'; }
  else { bar.style.background = '#06b6d4'; label.textContent = 'Very Strong'; label.style.color = '#06b6d4'; }
  
  if (!pwd) {
    bar.style.width = '0%';
    label.textContent = 'Enter a password';
    label.style.color = '#64748b';
    scoreEl.textContent = '';
  }
}
function togglePwdVisibility() {
  var input = document.getElementById('pwd-input');
  var btn = document.getElementById('pwd-toggle');
  if (input.type === 'password') { input.type = 'text'; btn.textContent = '🙈 Hide'; }
  else { input.type = 'password'; btn.textContent = '👁️ Show'; }
}
function genPassword() {
  var charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';
  var pwd = '';
  for (var i = 0; i < 16; i++) {
    pwd += charset.charAt(Math.floor(Math.random() * charset.length));
  }
  document.getElementById('pwd-input').value = pwd;
  checkStrength();
}
'''

tool_html_cn_pwd = '''
<div class="pwd-checker">
  <div class="form-group">
    <label>输入密码</label>
    <div style="display:flex;gap:8px">
      <input type="password" id="pwd-input" style="flex:1;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:1rem;outline:none" oninput="checkStrength()" placeholder="输入密码..." autocomplete="new-password">
      <button class="btn" id="pwd-toggle" onclick="togglePwdVisibility()" style="padding:8px 12px;background:#1e293b;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#94a3b8;cursor:pointer">👁️ Show</button>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn btn-primary" onclick="genPassword()">🎲 生成强密码</button>
    <button class="btn btn-danger" onclick="document.getElementById('pwd-input').value='';checkStrength()">🗑️ 清除</button>
  </div>
  <div style="background:#0f172a;border-radius:10px;padding:16px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <span style="font-size:1.1rem;font-weight:700" id="strength-label">Enter a password</span>
      <span style="color:#64748b;font-size:.85rem" id="strength-score"></span>
    </div>
    <div style="height:10px;background:#1e293b;border-radius:5px;overflow:hidden">
      <div id="strength-bar" style="height:100%;width:0%;border-radius:5px;transition:all .3s"></div>
    </div>
  </div>
  <div style="background:#0f172a;border-radius:10px;padding:16px;border:1px solid rgba(148,163,184,.1)">
    <div style="font-size:.85rem;color:#94a3b8;margin-bottom:8px">密码要求：</div>
    <div id="check-length" class="check-item fail">❌ 至少8个字符</div>
    <div id="check-upper" class="check-item fail">❌ 包含大写字母 (A-Z)</div>
    <div id="check-lower" class="check-item fail">❌ 包含小写字母 (a-z)</div>
    <div id="check-digit" class="check-item fail">❌ 包含数字 (0-9)</div>
    <div id="check-symbol" class="check-item fail">❌ 包含特殊字符 (!@#$%等)</div>
  </div>
</div>
<style>
.check-item{padding:6px 10px;margin:4px 0;border-radius:6px;font-size:.85rem;transition:all .2s}
.check-item.pass{color:#22c55e;background:rgba(34,197,94,.1)}
.check-item.fail{color:#ef4444;background:rgba(239,68,68,.1)}
.btn{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee}.btn-primary:hover{background:rgba(6,182,212,.35)}
.btn-danger{background:rgba(239,68,68,.15);color:#f87171}.btn-danger:hover{background:rgba(239,68,68,.3)}
</style>
'''

tool_html_en_pwd = '''
<div class="pwd-checker">
  <div class="form-group">
    <label>Enter password</label>
    <div style="display:flex;gap:8px">
      <input type="password" id="pwd-input" style="flex:1;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:1rem;outline:none" oninput="checkStrength()" placeholder="Enter password..." autocomplete="new-password">
      <button class="btn" id="pwd-toggle" onclick="togglePwdVisibility()" style="padding:8px 12px;background:#1e293b;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#94a3b8;cursor:pointer">👁️ Show</button>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn btn-primary" onclick="genPassword()">🎲 Generate Strong</button>
    <button class="btn btn-danger" onclick="document.getElementById('pwd-input').value='';checkStrength()">🗑️ Clear</button>
  </div>
  <div style="background:#0f172a;border-radius:10px;padding:16px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <span style="font-size:1.1rem;font-weight:700" id="strength-label">Enter a password</span>
      <span style="color:#64748b;font-size:.85rem" id="strength-score"></span>
    </div>
    <div style="height:10px;background:#1e293b;border-radius:5px;overflow:hidden">
      <div id="strength-bar" style="height:100%;width:0%;border-radius:5px;transition:all .3s"></div>
    </div>
  </div>
  <div style="background:#0f172a;border-radius:10px;padding:16px;border:1px solid rgba(148,163,184,.1)">
    <div style="font-size:.85rem;color:#94a3b8;margin-bottom:8px">Requirements:</div>
    <div id="check-length" class="check-item fail">❌ At least 8 characters</div>
    <div id="check-upper" class="check-item fail">❌ Uppercase (A-Z)</div>
    <div id="check-lower" class="check-item fail">❌ Lowercase (a-z)</div>
    <div id="check-digit" class="check-item fail">❌ Number (0-9)</div>
    <div id="check-symbol" class="check-item fail">❌ Special char (!@#$% etc.)</div>
  </div>
</div>
<style>
.check-item{padding:6px 10px;margin:4px 0;border-radius:6px;font-size:.85rem;transition:all .2s}
.check-item.pass{color:#22c55e;background:rgba(34,197,94,.1)}
.check-item.fail{color:#ef4444;background:rgba(239,68,68,.1)}
.btn{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee}.btn-primary:hover{background:rgba(6,182,212,.35)}
.btn-danger{background:rgba(239,68,68,.15);color:#f87171}.btn-danger:hover{background:rgba(239,68,68,.3)}
</style>
'''

# Build Tool 1: Word Counter
cn_path1, en_path1 = builder.build_bilingual(
    slug='word-counter',
    title_cn='字数统计器',
    title_en='Word Counter',
    desc_cn='免费在线字数统计工具，实时统计字符数、单词数、句子数、段落数、行数，计算阅读时间和朗读时间。纯前端本地处理，文本不上传服务器，保护隐私。',
    desc_en='Free online word counter. Count characters, words, sentences, paragraphs, lines, reading time and speaking time in real-time. 100% client-side, no data uploads.',
    icon='📝',
    cat_cn='文本工具',
    cat_en='Text Tools',
    cat_anchor='text-tools',
    tool_html_cn=tool_html_cn_wc,
    tool_html_en=tool_html_en_wc,
    tool_js=tool_js_word_counter,
    faqs_cn=[
        ('字数统计器怎么用？', '直接在输入框中输入或粘贴文本，所有统计数据会实时更新。也可以使用"粘贴"按钮从剪贴板导入文本。'),
        ('统计哪些指标？', '字符数（含空格和不含空格）、单词数、句子数、段落数、行数，还自动计算阅读时间（按200词/分钟）和朗读时间（按150词/分钟）。'),
        ('支持中文吗？', '完全支持中文。中文文本的字符数和段落数统计准确，句子数按句号、问号、感叹号等中文标点分割。'),
        ('数据安全吗？', '所有处理在浏览器本地完成，文本不上传服务器。关闭页面后数据自动清除。'),
        ('有文本长度限制吗？', '没有限制。浏览器内存允许即可，一般支持数万字的文本统计。'),
    ],
    faqs_en=[
        ('How to use the Word Counter?', 'Simply type or paste text into the input box. All statistics update in real-time. Use the "Paste" button to import text from clipboard.'),
        ('What metrics are counted?', 'Characters (with and without spaces), words, sentences, paragraphs, lines, reading time (at 200 words/min), and speaking time (at 150 words/min).'),
        ('Does it support Chinese?', 'Yes, fully supports Chinese text. Character counts and paragraph detection work correctly with Chinese punctuation.'),
        ('Is my data safe?', 'All processing is done in your browser. No text is uploaded to any server.'),
        ('Is there a text length limit?', 'No limit. As long as your browser can handle it.'),
    ],
    seo_cn='<h2>字数统计器 - 在线文本字数统计工具</h2><p>字数统计器是一款免费在线工具，帮助作家、编辑、学生和内容创作者快速统计文本字数。实时显示字符数（含空格和不含空格）、单词数、句子数、段落数和行数，还自动估算阅读时间和朗读时间。无论是写作文、投稿、SEO内容优化还是社交媒体文案，都能快速获取统计数据。</p><h3>核心功能</h3><ul><li>实时统计：输入文本立即更新统计数据</li><li>多维统计：字符数、单词数、句子数、段落数、行数一应俱全</li><li>阅读时间：自动估算阅读和朗读时间</li><li>剪贴板粘贴：一键从剪贴板导入文本</li><li>隐私安全：纯前端处理，数据不上传服务器</li></ul>',
    seo_en='<h2>Word Counter - Free Online Character & Word Count Tool</h2><p>This free online word counter helps writers, editors, students, and content creators quickly count text statistics. Real-time display of characters (with and without spaces), words, sentences, paragraphs, and lines, plus estimated reading and speaking time.</p><h3>Key Features</h3><ul><li>Real-time counting: instant updates as you type</li><li>Multi-metric: characters, words, sentences, paragraphs, lines</li><li>Reading time: auto-calculated reading and speaking estimates</li><li>Clipboard paste: one-click import from clipboard</li><li>Privacy first: all processing in your browser</li></ul>',
)
print(f'✅ Tool 1: {cn_path1} / {en_path1}')

# Build Tool 2: Password Strength Checker
cn_path2, en_path2 = builder.build_bilingual(
    slug='password-strength-checker',
    title_cn='密码强度检测器',
    title_en='Password Strength Checker',
    desc_cn='免费在线密码强度检测工具，实时检测密码强度并给出评分。检查长度、大小写字母、数字和特殊字符，提供可视化的强度条和安全建议。纯前端本地处理。',
    desc_en='Free online password strength checker. Real-time password strength analysis with scoring. Checks length, uppercase, lowercase, digits, and symbols with visual strength bar. 100% client-side.',
    icon='🔒',
    cat_cn='安全工具',
    cat_en='Security Tools',
    cat_anchor='security-tools',
    tool_html_cn=tool_html_cn_pwd,
    tool_html_en=tool_html_en_pwd,
    tool_js=tool_js_password,
    faqs_cn=[
        ('密码强度检测器怎么用？', '在输入框中输入密码，系统会实时分析密码强度并给出评分。使用"生成强密码"按钮可以一键生成16位随机强密码。'),
        ('评分标准是什么？', '满分为100分。评分基于密码长度（8字符以上开始计分）、包含大写字母、小写字母、数字和特殊字符的组合情况。分数越高密码越强。'),
        ('密码会被上传或保存吗？', '不会。所有分析在浏览器本地完成，密码不上传服务器。你可以放心使用。'),
        ('什么是强密码？', '强密码通常包含12个以上字符，混合大小写字母、数字和特殊字符，不含常见单词或个人信息。建议密码强度达到"Strong"（强）或"Very Strong"（非常强）等级。'),
        ('密码生成器安全吗？', '安全。密码生成在浏览器本地运行，使用浏览器的随机数生成器，生成的密码不会离开你的设备。'),
    ],
    faqs_en=[
        ('How to use the Password Strength Checker?', 'Type a password in the input box and the strength is analyzed in real-time. Click "Generate Strong" to create a random 16-character strong password.'),
        ('What is the scoring criteria?', 'Score out of 100. Based on length (starts counting at 8+ chars), uppercase, lowercase, digits, and special characters. Higher score = stronger password.'),
        ('Is my password uploaded or saved?', 'No. All analysis is done locally in your browser. Your password never leaves your device.'),
        ('What makes a strong password?', 'A strong password has 12+ characters, mixes uppercase, lowercase, digits, and symbols, and contains no common words or personal info.'),
        ('Is the password generator secure?', 'Yes. It runs entirely in your browser using the built-in cryptographically secure random number generator.'),
    ],
    seo_cn='<h2>密码强度检测器 - 在线密码安全评估工具</h2><p>密码强度检测器是一款免费的在线安全工具，帮助用户评估密码强度并提升账户安全性。实时分析密码长度、字符组合情况，给出0-100的量化评分和可视化强度条。还内置了强密码生成器，一键生成16位随机密码。纯前端处理，密码不上传服务器，确保你的密码隐私安全。</p><h3>核心功能</h3><ul><li>实时检测：输入密码即刻分析强度</li><li>量化评分：0-100分评分系统</li><li>可视化条：直观显示密码强度等级</li><li>密码生成：一键生成16位随机强密码</li><li>五项检测：长度、大写、小写、数字、特殊字符</li></ul>',
    seo_en='<h2>Password Strength Checker - Online Password Security Tool</h2><p>This free online password strength checker helps you evaluate password security and improve account protection. Real-time analysis of password length and character composition, with a 0-100 score and visual strength bar. Built-in strong password generator creates 16-character random passwords. 100% client-side for maximum privacy.</p><h3>Key Features</h3><ul><li>Real-time checking: instant strength analysis</li><li>Quantified scoring: 0-100 point system</li><li>Visual bar: clear strength level display</li><li>Password generator: one-click strong password creation</li><li>Five checks: length, upper, lower, digit, symbol</li></ul>',
)
print(f'✅ Tool 2: {cn_path2} / {en_path2}')

print('\n🎉 All tools built successfully!')
