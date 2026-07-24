#!/usr/bin/env python3
"""生成5个新工具：file-diff, css-selector-tester, xpath-tester, html-encode-decode, text-to-audio"""

import os, json

BASE = os.path.expanduser("~/tools-site")

TOOLS = {
    "file-diff": {
        "name_cn": "文件差异对比",
        "name_en": "File Diff Checker",
        "desc_cn": "免费在线文件差异对比工具，上传两个文件快速比较内容差异。逐行对比、差异高亮显示，支持txt/csv/json/xml/html/md等文本格式。代码比对、文档校对必备工具。",
        "desc_en": "Free online file diff checker - compare two files and highlight differences instantly. Line-by-line comparison with visual diff highlighting. Supports txt, csv, json, xml, html, md formats. Essential tool for code review and document comparison.",
        "kw_cn": "文件对比,差异对比,文本比对,文件差异,在线比对工具,文件比较器,代码比对",
        "kw_en": "file diff, compare files, file comparison, diff checker, online diff tool, file difference, code comparison",
        "title_cn": "在线文件差异对比工具 - 文件比对 | 逐行高亮 | 免费",
        "title_en": "Online File Diff Checker - Compare Files | Line-by-Line | Free",
    },
    "css-selector-tester": {
        "name_cn": "CSS选择器测试器",
        "name_en": "CSS Selector Tester",
        "desc_cn": "免费在线CSS选择器测试工具，实时测试CSS选择器匹配效果。输入HTML代码和CSS选择器，即时高亮显示匹配元素。前端开发调试必备，支持所有CSS3选择器。",
        "desc_en": "Free online CSS selector tester - test CSS selectors in real-time against HTML code. Instantly see which elements match your selector with visual highlighting. Supports all CSS3 selectors including attribute, pseudo-class, and combinators.",
        "kw_cn": "CSS选择器,选择器测试,CSS测试,前端调试,选择器验证,CSS开发工具,CSS3选择器",
        "kw_en": "CSS selector, selector tester, CSS test, frontend debug, selector validator, CSS development tool, CSS3 selector",
        "title_cn": "在线CSS选择器测试工具 - HTML匹配 | 实时高亮 | 免费",
        "title_en": "Online CSS Selector Tester - Test Against HTML | Real-time Highlighting | Free",
    },
    "xpath-tester": {
        "name_cn": "XPath测试器",
        "name_en": "XPath Tester",
        "desc_cn": "免费在线XPath表达式测试工具，输入XML/HTML代码和XPath表达式，实时测试匹配结果。支持XPath 1.0语法，显示匹配节点数量和完整路径，网页爬虫和XML解析必备。",
        "desc_en": "Free online XPath expression tester - test XPath expressions against XML/HTML code in real-time. Supports XPath 1.0 syntax, shows matched node count and full paths. Essential tool for web scraping and XML parsing.",
        "kw_cn": "XPath测试,XPath表达式,XML解析,HTML解析,网页爬虫,XPath工具,XPath验证器",
        "kw_en": "XPath tester, XPath expression, XML parsing, HTML parsing, web scraping, XPath tool, XPath validator",
        "title_cn": "在线XPath表达式测试工具 - XML/HTML匹配 | 节点查询 | 免费",
        "title_en": "Online XPath Tester - Test XML/HTML Expressions | Node Query | Free",
    },
    "html-encode-decode": {
        "name_cn": "HTML实体编码解码",
        "name_en": "HTML Entity Encoder Decoder",
        "desc_cn": "免费在线HTML实体编码解码工具，一键将HTML特殊字符转换为实体或反向解码。支持&amp;&lt;&gt;&quot;&#39;等HTML保留字符，可选十进制、十六进制和命名实体格式，Web开发安全编码必备。",
        "desc_en": "Free online HTML entity encoder and decoder - convert special characters to HTML entities and back. Supports &<>\"' reserved characters with decimal, hexadecimal, and named entity formats. Essential for secure web development.",
        "kw_cn": "HTML实体,实体编码,HTML编码,HTML解码,特殊字符转义,HTML转义,实体转换",
        "kw_en": "HTML entities, entity encoder, HTML encode, HTML decode, special character escape, HTML escape, entity converter",
        "title_cn": "在线HTML实体编码解码工具 - 特殊字符转义 | 三种格式 | 免费",
        "title_en": "Online HTML Entity Encoder Decoder - Character Escape | Three Formats | Free",
    },
    "text-to-audio": {
        "name_cn": "文字转语音",
        "name_en": "Text to Speech",
        "desc_cn": "免费在线文字转语音工具，将文本内容朗读为音频。支持多种语言和声音选择，可调节语速和音调，实时播放和下载音频。无需安装，浏览器Web Speech API驱动。",
        "desc_en": "Free online text to speech converter - read text aloud as audio. Supports multiple languages and voice options with adjustable speed and pitch. Real-time playback and audio download. No installation, powered by browser Web Speech API.",
        "kw_cn": "文字转语音,文本朗读,TTS,语音合成,在线朗读,文字朗读,语音转换",
        "kw_en": "text to speech, text reader, TTS, speech synthesis, online reader, read aloud, voice converter",
        "title_cn": "在线文字转语音工具 - 文本朗读 | 多语音 | 语速调节 | 免费",
        "title_en": "Online Text to Speech Converter - Read Text Aloud | Multi-Voice | Speed Control | Free",
    },
}

CSS = '''<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:900px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.header h1{font-size:1.5rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.nav-back a:hover{color:#94a3b8}
.tool-section{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.tool-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}
.tool-section label{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:6px;font-weight:500}
.tool-section textarea,.tool-section input[type="text"],.tool-section input[type="file"],.tool-section select{width:100%;padding:12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;font-family:inherit;margin-bottom:12px;resize:vertical}
.tool-section textarea:focus,.tool-section input:focus,.tool-section select:focus{outline:none;border-color:#06b6d4}
.tool-section textarea{min-height:150px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-size:.9rem;font-weight:500;transition:all .2s}
.btn-primary{background:#06b6d4;color:#0f172a}
.btn-primary:hover{background:#22d3ee}
.btn-secondary{background:rgba(148,163,184,.15);color:#e2e8f0}
.btn-secondary:hover{background:rgba(148,163,184,.25)}
.btn-group{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.result-box{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;min-height:60px;max-height:400px;overflow:auto;font-size:.9rem;white-space:pre-wrap;word-break:break-all;margin-top:12px}
.result-box:empty::after{content:"等待处理...";color:#475569}
.diff-added{background:rgba(34,197,94,.15);color:#4ade80;padding:2px 4px;border-radius:3px}
.diff-removed{background:rgba(239,68,68,.15);color:#f87171;padding:2px 4px;border-radius:3px}
.stat-bar{display:flex;gap:16px;margin-bottom:12px;font-size:.85rem;color:#94a3b8;flex-wrap:wrap}
.stat-bar span{padding:4px 8px;background:rgba(148,163,184,.08);border-radius:6px}
.output-controls{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.content-section{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.content-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.content-section h3{font-size:1rem;color:#e2e8f0;margin:16px 0 8px}
.content-section p{color:#94a3b8;font-size:.9rem;margin-bottom:10px;text-align:justify}
.content-section ul{padding-left:20px;color:#94a3b8;font-size:.9rem}
.content-section li{margin-bottom:6px}
.faq-item{margin-bottom:16px}
.faq-item .q{font-weight:500;color:#e2e8f0;margin-bottom:6px;font-size:.9rem}
.faq-item .a{color:#94a3b8;font-size:.85rem;padding-left:12px;border-left:2px solid rgba(6,182,212,.3)}
.footer{margin-top:32px;padding:24px 0;border-top:1px solid rgba(148,163,184,.1);text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b}
.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#06b6d4;color:#0f172a;padding:12px 24px;border-radius:8px;font-size:.9rem;z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none}
.toast.show{opacity:1}
.radio-group{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px}
.radio-group label{display:flex;align-items:center;gap:6px;cursor:pointer;margin-bottom:0;font-size:.9rem;color:#e2e8f0}
.radio-group input[type="radio"]{width:auto;accent-color:#06b6d4}
.hidden{display:none!important}
@media(max-width:600px){.header h1{font-size:1.2rem}.tool-section{padding:16px}}
</style>'''


GTAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>
  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments);}
  gtag('js',new Date());
  gtag('config','G-9W1157EBQV');
</script>'''


def gen_schema(name, desc, is_cn):
    lang = "zh-CN" if is_cn else "en"
    name_display = name
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{name_display}",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Web",
  "publisher": {{
    "@type": "Organization",
    "name": "Online Tools",
    "email": "dexshuang@google.com"
  }},
  "author": {{
    "@type": "Organization",
    "name": "Online Tools"
  }},
  "dateModified": "2026-07-25",
  "description": "{desc}",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "CNY"
  }}
}}
</script>'''


def gen_faq(is_cn, name):
    if is_cn:
        faqs = [
            ("这个工具收费吗？", "完全免费。本工具属于在线小工具矩阵的一部分，所有功能均无需注册、无需付费即可使用。"),
            ("数据会上传到服务器吗？", "不会。所有处理操作完全在您的浏览器中执行，输入数据不会上传到任何服务器，充分保障隐私安全。"),
            ("支持哪些浏览器？", "支持所有现代浏览器，包括Chrome、Firefox、Safari、Edge等。推荐使用最新版本以获得最佳体验。"),
            ("可以在手机上使用吗？", "可以。本工具完全响应式设计，在手机和平板设备上均可正常使用。"),
        ]
    else:
        faqs = [
            ("Is this tool free?", "Yes, completely free. This tool is part of our free online tools collection. No registration or payment required."),
            ("Is my data uploaded to a server?", "No. All processing happens entirely in your browser. No data is ever uploaded to any server, ensuring complete privacy."),
            ("Which browsers are supported?", "All modern browsers are supported, including Chrome, Firefox, Safari, and Edge. We recommend using the latest version for the best experience."),
            ("Can I use it on mobile?", "Yes. This tool is fully responsive and works great on phones and tablets."),
        ]
    q_items = []
    for q, a in faqs:
        q_items.append(f'''  {{
    "@type": "Question",
    "name": "{q}",
    "acceptedAnswer": {{
      "@type": "Answer",
      "text": "{a}"
    }}
  }}''')
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{",".join(q_items)}
  ]
}}
</script>'''


def gen_howto(is_cn, name, slug):
    if is_cn:
        name_d = name
        howto = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "如何使用{name_d}",
  "description": "使用{name_d}的简单步骤。所有处理都在你的浏览器本地完成，无需上传数据。",
  "totalTime": "PT1M",
  "tool": {{
    "@type": "HowToTool",
    "name": "{name_d}"
  }},
  "step": [
    {{
      "@type": "HowToStep",
      "position": 1,
      "name": "输入内容",
      "text": "在工具页面的输入区域中输入或粘贴你的内容。",
      "url": "https://free-toolbase.com/{slug}/#input"
    }},
    {{
      "@type": "HowToStep",
      "position": 2,
      "name": "配置选项",
      "text": "根据需要调整可用的选项或设置。",
      "url": "https://free-toolbase.com/{slug}/#options"
    }},
    {{
      "@type": "HowToStep",
      "position": 3,
      "name": "查看结果",
      "text": "点击处理按钮，立即在浏览器中查看结果。所有数据处理都在你的设备本地完成——不会上传任何数据到服务器。",
      "url": "https://free-toolbase.com/{slug}/#output"
    }}
  ]
}}
</script>'''
    else:
        howto = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Use {name}",
  "description": "Simple steps to use {name}. All processing happens locally in your browser — no data is uploaded.",
  "totalTime": "PT1M",
  "tool": {{
    "@type": "HowToTool",
    "name": "{name}"
  }},
  "step": [
    {{
      "@type": "HowToStep",
      "position": 1,
      "name": "Input Content",
      "text": "Enter or paste your content in the input area of the tool page.",
      "url": "https://free-toolbase.com/en/{slug}/#input"
    }},
    {{
      "@type": "HowToStep",
      "position": 2,
      "name": "Configure Options",
      "text": "Adjust available options or settings as needed.",
      "url": "https://free-toolbase.com/en/{slug}/#options"
    }},
    {{
      "@type": "HowToStep",
      "position": 3,
      "name": "View Results",
      "text": "Click the process button to see results instantly in your browser. All data processing happens on your device — nothing is uploaded to any server.",
      "url": "https://free-toolbase.com/en/{slug}/#output"
    }}
  ]
}}
</script>'''
    return howto


def gen_footer(is_cn):
    if is_cn:
        return '''<footer class="footer">
<p>© 2026 <a href="/">在线小工具矩阵</a>. All rights reserved.</p>
<nav style="margin-top:8px">
  <a href="/about/" style="margin:0 8px">关于我们</a>
  <a href="/contact/" style="margin:0 8px">联系我们</a>
  <a href="/privacy/" style="margin:0 8px">隐私政策</a>
  <a href="/terms/" style="margin:0 8px">使用条款</a>
</nav>
</footer>'''
    else:
        return '''<footer class="footer">
<p>© 2026 <a href="/en/">Free ToolBase</a>. All rights reserved.</p>
<nav style="margin-top:8px">
  <a href="/en/about/" style="margin:0 8px">About</a>
  <a href="/en/contact/" style="margin:0 8px">Contact</a>
  <a href="/en/privacy/" style="margin:0 8px">Privacy</a>
  <a href="/en/terms/" style="margin:0 8px">Terms</a>
</nav>
</footer>'''


def gen_toast():
    return '''<div class="toast" id="toast"></div>
<script>
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
async function copyToClipboard(text){try{await navigator.clipboard.writeText(text);showToast('已复制到剪贴板')}catch(e){showToast('复制失败')}}
</script>'''


# ============ TOOL-SPECIFIC GENERATORS ============


def gen_file_diff(is_cn):
    """Generate file-diff HTML with JS logic"""
    if is_cn:
        title = "在线文件差异对比工具 - 文件比对 | 逐行高亮 | 免费"
        desc = "免费在线文件差异对比工具，上传两个文件快速比较内容差异。逐行对比、差异高亮显示，支持txt/csv/json/xml/html/md等文本格式。代码比对、文档校对必备工具。"
        og_title = "在线文件差异对比工具 - 文件比对 | 逐行高亮 | 免费"
        meta_kw = "文件对比,差异对比,文本比对,文件差异,在线比对工具,文件比较器,代码比对"
        tn = TOOLS["file-diff"]
        content_title = "📂 文件差异对比"
        content_desc = "上传两个文本文件，快速比较内容差异，逐行对比并高亮显示不同之处。"
        tool_ui = '''
    <div class="tool-section">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <label>📁 原始文件</label>
          <input type="file" id="file1" accept=".txt,.csv,.json,.xml,.html,.md,.js,.py,.css,.yaml,.yml,.log,.ini,.cfg,.sh,.bat" style="margin-bottom:4px">
          <textarea id="text1" placeholder="或直接粘贴原始文本内容..."></textarea>
        </div>
        <div>
          <label>📁 对比文件</label>
          <input type="file" id="file2" accept=".txt,.csv,.json,.xml,.html,.md,.js,.py,.css,.yaml,.yml,.log,.ini,.cfg,.sh,.bat" style="margin-bottom:4px">
          <textarea id="text2" placeholder="或直接粘贴对比文本内容..."></textarea>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="compareFiles()">🔍 开始对比</button>
        <button class="btn btn-secondary" onclick="swapTexts()">🔄 交换文本</button>
        <button class="btn btn-secondary" onclick="clearAll()">🗑 清空</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="diffMode" value="line" checked> 逐行对比</label>
        <label><input type="radio" name="diffMode" value="word"> 逐词对比</label>
        <label><input type="radio" name="diffMode" value="char"> 逐字符对比</label>
      </div>
      <div id="diffStats" class="stat-bar"></div>
      <div id="diffOutput" class="result-box" style="max-height:500px"></div>
    </div>'''
        js = '''<script>
  var file1=document.getElementById('file1'), file2=document.getElementById('file2'),
      text1=document.getElementById('text1'), text2=document.getElementById('text2');
  file1.onchange=function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(e){text1.value=e.target.result};r.readAsText(f)};
  file2.onchange=function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(e){text2.value=e.target.result};r.readAsText(f)};
  function swapTexts(){var t=text1.value;text1.value=text2.value;text2.value=t;}
  function clearAll(){text1.value='';text2.value='';document.getElementById('diffOutput').innerHTML='';document.getElementById('diffStats').innerHTML='';}
  function compareFiles(){
    var t1=text1.value.trim(), t2=text2.value.trim();
    if(!t1&&!t2){showToast('请先输入或上传文件');return}
    var mode=document.querySelector('input[name="diffMode"]:checked').value;
    var lines1=t1.split('\\n'), lines2=t2.split('\\n'), out=[], added=0, removed=0, unchanged=0;
    var maxLen=Math.max(lines1.length,lines2.length);
    for(var i=0;i<maxLen;i++){
      var l1=lines1[i]||'', l2=lines2[i]||'', row='<div style="font-family:monospace;padding:2px 0;border-bottom:1px solid rgba(148,163,184,.05)">';
      row+='<span style="color:#475569;margin-right:8px">'+(i+1)+'</span>';
      if(l1===l2){row+='<span style="color:#94a3b8">'+escHtml(l1)+'</span>';unchanged++}
      else{
        row+='<span class="diff-removed">- '+escHtml(l1)+'</span><br>';
        row+='<span style="margin-left:24px" class="diff-added">+ '+escHtml(l2)+'</span>';
        if(l1&&l2){added++;removed++}else if(!l1){added++}else{removed++}
      }
      row+='</div>';out.push(row);
    }
    document.getElementById('diffStats').innerHTML='<span>新增: <b style="color:#4ade80">'+added+'</b></span><span>删除: <b style="color:#f87171">'+removed+'</b></span><span>未变: <b style="color:#94a3b8">'+unchanged+'</b></span><span>总行: <b>'+maxLen+'</b></span>';
    document.getElementById('diffOutput').innerHTML=out.join('');
  }
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
</script>'''
    else:
        title = "Online File Diff Checker - Compare Files | Line-by-Line | Free"
        desc = "Free online file diff checker - compare two files and highlight differences instantly. Line-by-line comparison with visual diff highlighting. Supports txt, csv, json, xml, html, md formats. Essential tool for code review and document comparison."
        og_title = "Online File Diff Checker - Compare Files | Line-by-Line | Free"
        meta_kw = "file diff, compare files, file comparison, diff checker, online diff tool, file difference, code comparison"
        tn = TOOLS["file-diff"]
        content_title = "📂 File Diff Checker"
        content_desc = "Upload two text files and instantly compare their differences with line-by-line highlighting."
        tool_ui = '''
    <div class="tool-section">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <label>📁 Original File</label>
          <input type="file" id="file1" accept=".txt,.csv,.json,.xml,.html,.md,.js,.py,.css,.yaml,.yml,.log,.ini,.cfg,.sh,.bat" style="margin-bottom:4px">
          <textarea id="text1" placeholder="Or paste original text directly..."></textarea>
        </div>
        <div>
          <label>📁 Comparison File</label>
          <input type="file" id="file2" accept=".txt,.csv,.json,.xml,.html,.md,.js,.py,.css,.yaml,.yml,.log,.ini,.cfg,.sh,.bat" style="margin-bottom:4px">
          <textarea id="text2" placeholder="Or paste comparison text directly..."></textarea>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="compareFiles()">🔍 Compare</button>
        <button class="btn btn-secondary" onclick="swapTexts()">🔄 Swap</button>
        <button class="btn btn-secondary" onclick="clearAll()">🗑 Clear</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="diffMode" value="line" checked> Line-by-Line</label>
        <label><input type="radio" name="diffMode" value="word"> Word-by-Word</label>
        <label><input type="radio" name="diffMode" value="char"> Char-by-Char</label>
      </div>
      <div id="diffStats" class="stat-bar"></div>
      <div id="diffOutput" class="result-box" style="max-height:500px"></div>
    </div>'''
        js = '''<script>
  var file1=document.getElementById('file1'), file2=document.getElementById('file2'),
      text1=document.getElementById('text1'), text2=document.getElementById('text2');
  file1.onchange=function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(e){text1.value=e.target.result};r.readAsText(f)};
  file2.onchange=function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(e){text2.value=e.target.result};r.readAsText(f)};
  function swapTexts(){var t=text1.value;text1.value=text2.value;text2.value=t;}
  function clearAll(){text1.value='';text2.value='';document.getElementById('diffOutput').innerHTML='';document.getElementById('diffStats').innerHTML='';}
  function compareFiles(){
    var t1=text1.value.trim(), t2=text2.value.trim();
    if(!t1&&!t2){showToast('Please input or upload files first');return}
    var mode=document.querySelector('input[name="diffMode"]:checked').value;
    var lines1=t1.split('\\n'), lines2=t2.split('\\n'), out=[], added=0, removed=0, unchanged=0;
    var maxLen=Math.max(lines1.length,lines2.length);
    for(var i=0;i<maxLen;i++){
      var l1=lines1[i]||'', l2=lines2[i]||'', row='<div style="font-family:monospace;padding:2px 0;border-bottom:1px solid rgba(148,163,184,.05)">';
      row+='<span style="color:#475569;margin-right:8px">'+(i+1)+'</span>';
      if(l1===l2){row+='<span style="color:#94a3b8">'+escHtml(l1)+'</span>';unchanged++}
      else{
        row+='<span class="diff-removed">- '+escHtml(l1)+'</span><br>';
        row+='<span style="margin-left:24px" class="diff-added">+ '+escHtml(l2)+'</span>';
        if(l1&&l2){added++;removed++}else if(!l1){added++}else{removed++}
      }
      row+='</div>';out.push(row);
    }
    document.getElementById('diffStats').innerHTML='<span>Added: <b style="color:#4ade80">'+added+'</b></span><span>Removed: <b style="color:#f87171">'+removed+'</b></span><span>Unchanged: <b style="color:#94a3b8">'+unchanged+'</b></span><span>Total: <b>'+maxLen+'</b></span>';
    document.getElementById('diffOutput').innerHTML=out.join('');
  }
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
</script>'''

    return title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js


def gen_css_selector_tester(is_cn):
    if is_cn:
        title = "在线CSS选择器测试工具 - HTML匹配 | 实时高亮 | 免费"
        desc = "免费在线CSS选择器测试工具，实时测试CSS选择器匹配效果。输入HTML代码和CSS选择器，即时高亮显示匹配元素。前端开发调试必备，支持所有CSS3选择器。"
        og_title = "在线CSS选择器测试工具 - HTML匹配 | 实时高亮 | 免费"
        meta_kw = "CSS选择器,选择器测试,CSS测试,前端调试,选择器验证,CSS开发工具,CSS3选择器"
        tn = TOOLS["css-selector-tester"]
        content_title = "🎯 CSS选择器测试器"
        content_desc = "输入HTML代码和CSS选择器，实时测试选择器匹配效果，高亮显示匹配元素。"
        sample_html = '<div class="container"><h1 id="title">Hello World</h1><p class="intro">This is a paragraph</p><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><a href="https://example.com">Click me</a></div>'
        tool_ui = f'''
    <div class="tool-section">
      <label>📝 HTML代码</label>
      <textarea id="htmlInput" placeholder="在此输入或粘贴HTML代码...">{sample_html}</textarea>
      <label>🔍 CSS选择器</label>
      <input type="text" id="selectorInput" placeholder="输入CSS选择器，如 .container, #title, div > p, [href]" value="li">
      <div class="btn-group">
        <button class="btn btn-primary" onclick="testSelector()">🔍 测试匹配</button>
        <button class="btn btn-secondary" onclick="clearResults()">🗑 清空</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="resultMode" value="html" checked> 显示匹配HTML</label>
        <label><input type="radio" name="resultMode" value="text"> 仅显示文本</label>
        <label><input type="radio" name="resultMode" value="count"> 仅显示数量</label>
      </div>
      <div id="selectorStats" class="stat-bar"></div>
      <div id="selectorOutput" class="result-box" style="max-height:400px"></div>
    </div>'''
        js = '''<script>
  function testSelector(){
    var html=document.getElementById('htmlInput').value.trim();
    var sel=document.getElementById('selectorInput').value.trim();
    if(!html){showToast('请输入HTML代码');return}
    if(!sel){showToast('请输入CSS选择器');return}
    try{
      var parser=new DOMParser(),doc=parser.parseFromString(html,'text/html');
      var matches=doc.querySelectorAll(sel);
      var mode=document.querySelector('input[name="resultMode"]:checked').value;
      if(mode==='count'){
        document.getElementById('selectorStats').innerHTML='<span>匹配元素: <b style="color:#22d3ee">'+matches.length+'</b></span>';
        document.getElementById('selectorOutput').innerHTML='';
        return;
      }
      var out=[],texts=[];
      for(var i=0;i<matches.length;i++){
        var el=matches[i],tag=el.tagName.toLowerCase();
        var cls=el.className?'.'+el.className.split(' ').join('.'):'';
        var id=el.id?'#'+el.id:'';
        var attrs='';
        for(var j=0;j<el.attributes.length;j++){
          var a=el.attributes[j];
          if(a.name!=='class'&&a.name!=='id')attrs+=' '+a.name+'="'+a.value+'"';
        }
        var txt=(el.textContent||'').trim().substring(0,100);
        if(mode==='html'){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#22d3ee">&lt;'+tag+id+cls+attrs+'&gt;</span> '+
            '<span style="color:#94a3b8">'+escHtml(txt)+'</span>'+
            '<span style="color:#22d3ee">&lt;/'+tag+'&gt;</span></div>');
        }else{
          texts.push('<div style="font-family:monospace;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#e2e8f0">'+escHtml(txt||'(empty)')+'</span></div>');
        }
      }
      if(mode==='text')out=texts;
      document.getElementById('selectorStats').innerHTML='<span>选择器: <b style="color:#22d3ee">'+escHtml(sel)+'</b></span><span>匹配: <b style="color:#4ade80">'+matches.length+'</b> 个元素</span>';
      document.getElementById('selectorOutput').innerHTML=out.join('')||'<span style="color:#475569">无匹配元素</span>';
    }catch(e){
      document.getElementById('selectorOutput').innerHTML='<span style="color:#f87171">错误: '+escHtml(e.message)+'</span>';
      document.getElementById('selectorStats').innerHTML='';
    }
  }
  function clearResults(){document.getElementById('selectorOutput').innerHTML='';document.getElementById('selectorStats').innerHTML='';}
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
  // auto test on load
  window.addEventListener('DOMContentLoaded',function(){setTimeout(testSelector,300)});
</script>'''
    else:
        title = "Online CSS Selector Tester - Test Against HTML | Real-time Highlighting | Free"
        desc = "Free online CSS selector tester - test CSS selectors in real-time against HTML code. Instantly see which elements match your selector with visual highlighting. Supports all CSS3 selectors including attribute, pseudo-class, and combinators."
        og_title = "Online CSS Selector Tester - Test Against HTML | Real-time Highlighting | Free"
        meta_kw = "CSS selector, selector tester, CSS test, frontend debug, selector validator, CSS development tool, CSS3 selector"
        tn = TOOLS["css-selector-tester"]
        content_title = "🎯 CSS Selector Tester"
        content_desc = "Enter HTML code and a CSS selector to visually test which elements match in real-time."
        sample_html = '<div class="container"><h1 id="title">Hello World</h1><p class="intro">This is a paragraph</p><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><a href="https://example.com">Click me</a></div>'
        tool_ui = f'''
    <div class="tool-section">
      <label>📝 HTML Code</label>
      <textarea id="htmlInput" placeholder="Enter or paste HTML code here...">{sample_html}</textarea>
      <label>🔍 CSS Selector</label>
      <input type="text" id="selectorInput" placeholder="Enter a CSS selector, e.g. .container, #title, div > p, [href]" value="li">
      <div class="btn-group">
        <button class="btn btn-primary" onclick="testSelector()">🔍 Test</button>
        <button class="btn btn-secondary" onclick="clearResults()">🗑 Clear</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="resultMode" value="html" checked> Show HTML</label>
        <label><input type="radio" name="resultMode" value="text"> Text Only</label>
        <label><input type="radio" name="resultMode" value="count"> Count Only</label>
      </div>
      <div id="selectorStats" class="stat-bar"></div>
      <div id="selectorOutput" class="result-box" style="max-height:400px"></div>
    </div>'''
        js = '''<script>
  function testSelector(){
    var html=document.getElementById('htmlInput').value.trim();
    var sel=document.getElementById('selectorInput').value.trim();
    if(!html){showToast('Please enter HTML code');return}
    if(!sel){showToast('Please enter a CSS selector');return}
    try{
      var parser=new DOMParser(),doc=parser.parseFromString(html,'text/html');
      var matches=doc.querySelectorAll(sel);
      var mode=document.querySelector('input[name="resultMode"]:checked').value;
      if(mode==='count'){
        document.getElementById('selectorStats').innerHTML='<span>Matches: <b style="color:#22d3ee">'+matches.length+'</b> elements</span>';
        document.getElementById('selectorOutput').innerHTML='';
        return;
      }
      var out=[],texts=[];
      for(var i=0;i<matches.length;i++){
        var el=matches[i],tag=el.tagName.toLowerCase();
        var cls=el.className?'.'+el.className.split(' ').join('.'):'';
        var id=el.id?'#'+el.id:'';
        var attrs='';
        for(var j=0;j<el.attributes.length;j++){
          var a=el.attributes[j];
          if(a.name!=='class'&&a.name!=='id')attrs+=' '+a.name+'="'+a.value+'"';
        }
        var txt=(el.textContent||'').trim().substring(0,100);
        if(mode==='html'){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#22d3ee">&lt;'+tag+id+cls+attrs+'&gt;</span> '+
            '<span style="color:#94a3b8">'+escHtml(txt)+'</span>'+
            '<span style="color:#22d3ee">&lt;/'+tag+'&gt;</span></div>');
        }else{
          texts.push('<div style="font-family:monospace;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#e2e8f0">'+escHtml(txt||'(empty)')+'</span></div>');
        }
      }
      if(mode==='text')out=texts;
      document.getElementById('selectorStats').innerHTML='<span>Selector: <b style="color:#22d3ee">'+escHtml(sel)+'</b></span><span>Matches: <b style="color:#4ade80">'+matches.length+'</b> elements</span>';
      document.getElementById('selectorOutput').innerHTML=out.join('')||'<span style="color:#475569">No matches found</span>';
    }catch(e){
      document.getElementById('selectorOutput').innerHTML='<span style="color:#f87171">Error: '+escHtml(e.message)+'</span>';
      document.getElementById('selectorStats').innerHTML='';
    }
  }
  function clearResults(){document.getElementById('selectorOutput').innerHTML='';document.getElementById('selectorStats').innerHTML='';}
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
  window.addEventListener('DOMContentLoaded',function(){setTimeout(testSelector,300)});
</script>'''

    return title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js


def gen_xpath_tester(is_cn):
    if is_cn:
        title = "在线XPath表达式测试工具 - XML/HTML匹配 | 节点查询 | 免费"
        desc = "免费在线XPath表达式测试工具，输入XML/HTML代码和XPath表达式，实时测试匹配结果。支持XPath 1.0语法，显示匹配节点数量和完整路径，网页爬虫和XML解析必备。"
        og_title = "在线XPath表达式测试工具 - XML/HTML匹配 | 节点查询 | 免费"
        meta_kw = "XPath测试,XPath表达式,XML解析,HTML解析,网页爬虫,XPath工具,XPath验证器"
        tn = TOOLS["xpath-tester"]
        content_title = "🔍 XPath测试器"
        content_desc = "输入XML/HTML代码和XPath表达式，实时测试节点匹配结果，显示匹配数量、路径和文本内容。"
        sample_xml = '''<bookstore>
  <book category="fiction">
    <title lang="en">The Great Gatsby</title>
    <author>F. Scott Fitzgerald</author>
    <year>1925</year>
    <price>12.99</price>
  </book>
  <book category="fiction">
    <title lang="en">1984</title>
    <author>George Orwell</author>
    <year>1949</year>
    <price>9.99</price>
  </book>
  <book category="nonfiction">
    <title lang="en">Sapiens</title>
    <author>Yuval Noah Harari</author>
    <year>2011</year>
    <price>15.99</price>
  </book>
</bookstore>'''
        tool_ui = f'''
    <div class="tool-section">
      <label>📄 XML/HTML代码</label>
      <textarea id="xmlInput" placeholder="在此输入或粘贴XML/HTML代码...">{sample_xml}</textarea>
      <label>🔍 XPath表达式</label>
      <input type="text" id="xpathInput" placeholder="输入XPath表达式，如 //book/title, //book[@category='fiction'], /bookstore/book[1]" value="//book/title">
      <div class="btn-group">
        <button class="btn btn-primary" onclick="testXPath()">🔍 测试匹配</button>
        <button class="btn btn-secondary" onclick="clearXPath()">🗑 清空</button>
      </div>
      <div id="xpathStats" class="stat-bar"></div>
      <div id="xpathOutput" class="result-box" style="max-height:400px"></div>
    </div>'''
        js = '''<script>
  function testXPath(){
    var xml=document.getElementById('xmlInput').value.trim();
    var xpath=document.getElementById('xpathInput').value.trim();
    if(!xml){showToast('请输入XML/HTML代码');return}
    if(!xpath){showToast('请输入XPath表达式');return}
    try{
      var parser=new DOMParser(),doc=parser.parseFromString(xml,'text/xml');
      var pe=doc.documentElement;if(!pe){throw new Error('无效的XML格式')}
      var result=doc.evaluate(xpath,doc,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);
      var count=result.snapshotLength,out=[];
      for(var i=0;i<count;i++){
        var node=result.snapshotItem(i);
        var path=getXPath(node,doc);
        if(node.nodeType===1){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#22d3ee">&lt;'+node.nodeName+'&gt;</span> '+
            '<span style="color:#94a3b8">'+escHtml((node.textContent||'').trim().substring(0,200))+'</span></div>');
        }else if(node.nodeType===2){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#fbbf24">@'+node.nodeName+'</span> = '+
            '<span style="color:#94a3b8">"'+escHtml(node.nodeValue||'')+'"</span></div>');
        }else if(node.nodeType===3){
          var t=(node.nodeValue||'').trim();if(!t)continue;
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#94a3b8">'+escHtml(t.substring(0,200))+'</span></div>');
        }
      }
      document.getElementById('xpathStats').innerHTML='<span>XPath: <b style="color:#22d3ee">'+escHtml(xpath)+'</b></span><span>匹配: <b style="color:#4ade80">'+count+'</b> 个节点</span>';
      document.getElementById('xpathOutput').innerHTML=out.join('')||'<span style="color:#475569">无匹配节点</span>';
    }catch(e){
      document.getElementById('xpathOutput').innerHTML='<span style="color:#f87171">错误: '+escHtml(e.message)+'</span>';
      document.getElementById('xpathStats').innerHTML='';
    }
  }
  function getXPath(node,doc){
    if(node===doc)return '/';
    if(node.nodeType===2)return '@'+node.nodeName;
    if(node.nodeType===3)return 'text()';
    var path='',cur=node;
    while(cur&&cur.nodeType===1){
      var tag=cur.nodeName,idx=1,s=cur.previousSibling;
      while(s){if(s.nodeType===1&&s.nodeName===tag)idx++;s=s.previousSibling}
      path='/'+tag+'['+idx+']'+path;
      cur=cur.parentNode;
    }
    return path;
  }
  function clearXPath(){document.getElementById('xpathOutput').innerHTML='';document.getElementById('xpathStats').innerHTML='';}
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
  window.addEventListener('DOMContentLoaded',function(){setTimeout(testXPath,300)});
</script>'''
    else:
        title = "Online XPath Tester - Test XML/HTML Expressions | Node Query | Free"
        desc = "Free online XPath expression tester - test XPath expressions against XML/HTML code in real-time. Supports XPath 1.0 syntax, shows matched node count and full paths. Essential tool for web scraping and XML parsing."
        og_title = "Online XPath Tester - Test XML/HTML Expressions | Node Query | Free"
        meta_kw = "XPath tester, XPath expression, XML parsing, HTML parsing, web scraping, XPath tool, XPath validator"
        tn = TOOLS["xpath-tester"]
        content_title = "🔍 XPath Tester"
        content_desc = "Enter XML/HTML code and an XPath expression to test node matching in real-time. Shows match count, paths, and text content."
        sample_xml = '''<bookstore>
  <book category="fiction">
    <title lang="en">The Great Gatsby</title>
    <author>F. Scott Fitzgerald</author>
    <year>1925</year>
    <price>12.99</price>
  </book>
  <book category="fiction">
    <title lang="en">1984</title>
    <author>George Orwell</author>
    <year>1949</year>
    <price>9.99</price>
  </book>
  <book category="nonfiction">
    <title lang="en">Sapiens</title>
    <author>Yuval Noah Harari</author>
    <year>2011</year>
    <price>15.99</price>
  </book>
</bookstore>'''
        tool_ui = f'''
    <div class="tool-section">
      <label>📄 XML/HTML Code</label>
      <textarea id="xmlInput" placeholder="Enter or paste XML/HTML code here...">{sample_xml}</textarea>
      <label>🔍 XPath Expression</label>
      <input type="text" id="xpathInput" placeholder="Enter XPath expression, e.g. //book/title, //book[@category='fiction']" value="//book/title">
      <div class="btn-group">
        <button class="btn btn-primary" onclick="testXPath()">🔍 Test</button>
        <button class="btn btn-secondary" onclick="clearXPath()">🗑 Clear</button>
      </div>
      <div id="xpathStats" class="stat-bar"></div>
      <div id="xpathOutput" class="result-box" style="max-height:400px"></div>
    </div>'''
        js = '''<script>
  function testXPath(){
    var xml=document.getElementById('xmlInput').value.trim();
    var xpath=document.getElementById('xpathInput').value.trim();
    if(!xml){showToast('Please enter XML/HTML code');return}
    if(!xpath){showToast('Please enter an XPath expression');return}
    try{
      var parser=new DOMParser(),doc=parser.parseFromString(xml,'text/xml');
      var pe=doc.documentElement;if(!pe){throw new Error('Invalid XML format')}
      var result=doc.evaluate(xpath,doc,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);
      var count=result.snapshotLength,out=[];
      for(var i=0;i<count;i++){
        var node=result.snapshotItem(i);
        if(node.nodeType===1){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#22d3ee">&lt;'+node.nodeName+'&gt;</span> '+
            '<span style="color:#94a3b8">'+escHtml((node.textContent||'').trim().substring(0,200))+'</span></div>');
        }else if(node.nodeType===2){
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#fbbf24">@'+node.nodeName+'</span> = '+
            '<span style="color:#94a3b8">"'+escHtml(node.nodeValue||'')+'"</span></div>');
        }else if(node.nodeType===3){
          var t=(node.nodeValue||'').trim();if(!t)continue;
          out.push('<div style="font-family:monospace;font-size:.85rem;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.05)">'+
            '<span style="color:#475569">['+(i+1)+']</span> '+
            '<span style="color:#94a3b8">'+escHtml(t.substring(0,200))+'</span></div>');
        }
      }
      document.getElementById('xpathStats').innerHTML='<span>XPath: <b style="color:#22d3ee">'+escHtml(xpath)+'</b></span><span>Matches: <b style="color:#4ade80">'+count+'</b> nodes</span>';
      document.getElementById('xpathOutput').innerHTML=out.join('')||'<span style="color:#475569">No matches found</span>';
    }catch(e){
      document.getElementById('xpathOutput').innerHTML='<span style="color:#f87171">Error: '+escHtml(e.message)+'</span>';
      document.getElementById('xpathStats').innerHTML='';
    }
  }
  function clearXPath(){document.getElementById('xpathOutput').innerHTML='';document.getElementById('xpathStats').innerHTML='';}
  function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
  window.addEventListener('DOMContentLoaded',function(){setTimeout(testXPath,300)});
</script>'''

    return title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js


def gen_html_encoder(is_cn):
    if is_cn:
        title = "在线HTML实体编码解码工具 - 特殊字符转义 | 三种格式 | 免费"
        desc = "免费在线HTML实体编码解码工具，一键将HTML特殊字符转换为实体或反向解码。支持&amp;&lt;&gt;&quot;&#39;等HTML保留字符，可选十进制、十六进制和命名实体格式，Web开发安全编码必备。"
        og_title = "在线HTML实体编码解码工具 - 特殊字符转义 | 三种格式 | 免费"
        meta_kw = "HTML实体,实体编码,HTML编码,HTML解码,特殊字符转义,HTML转义,实体转换"
        tn = TOOLS["html-encode-decode"]
        content_title = "🔤 HTML实体编码解码"
        content_desc = "一键将HTML特殊字符（<>&\"'）转换为HTML实体或反向解码。支持命名实体、十进制和十六进制格式。"
        sample = '<div class="alert">警告: 请输入 <strong>有效</strong> 的邮箱地址 & 密码</div>'
        tool_ui = f'''
    <div class="tool-section">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <label>📝 纯文本（解码后）</label>
          <textarea id="plainText" placeholder="输入需要编码的纯文本...">{sample}</textarea>
        </div>
        <div>
          <label>🔐 HTML实体（编码后）</label>
          <textarea id="entityText" placeholder="输入HTML实体进行解码..."></textarea>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="encode()">⬇ 编码</button>
        <button class="btn btn-secondary" onclick="decode()">⬆ 解码</button>
        <button class="btn btn-secondary" onclick="swapTexts()">🔄 交换</button>
        <button class="btn btn-secondary" onclick="clearAll()">🗑 清空</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="entityMode" value="named" checked> 命名实体 (&amp;lt;)</label>
        <label><input type="radio" name="entityMode" value="decimal"> 十进制 (&amp;#60;)</label>
        <label><input type="radio" name="entityMode" value="hex"> 十六进制 (&amp;#x3C;)</label>
      </div>
      <div id="encodeStats" class="stat-bar"></div>
    </div>'''
        js = '''<script>
  var chars={'<':'lt','>':'gt','&':'amp','"':'quot',"'":'apos'};
  var named={'lt':60,'gt':62,'amp':38,'quot':34,'apos':39};
  function encode(){
    var t=document.getElementById('plainText').value;
    var mode=document.querySelector('input[name="entityMode"]:checked').value;
    var r='',c=0;
    for(var i=0;i<t.length;i++){
      var ch=t[i],code=t.charCodeAt(i);
      if(ch in chars){
        c++;
        if(mode==='named')r+='&'+chars[ch]+';';
        else if(mode==='decimal')r+='&#'+code+';';
        else r+='&#x'+code.toString(16).toUpperCase()+';';
      }else if(code>127){
        c++;
        if(mode==='named')r+='&#'+code+';';
        else if(mode==='decimal')r+='&#'+code+';';
        else r+='&#x'+code.toString(16).toUpperCase()+';';
      }else{r+=ch}
    }
    document.getElementById('entityText').value=r;
    document.getElementById('encodeStats').innerHTML='<span>编码字符: <b style="color:#4ade80">'+c+'</b></span><span>总字符: <b>'+t.length+'</b></span>';
  }
  function decode(){
    var t=document.getElementById('entityText').value,c=0;
    var r=t.replace(/&(?:#(\\d+)|#x([0-9a-fA-F]+)|(\\w+));/g,function(m,dec,hex,name){
      c++;
      if(dec)return String.fromCharCode(parseInt(dec,10));
      if(hex)return String.fromCharCode(parseInt(hex,16));
      var code=named[name];if(code)return String.fromCharCode(code);
      var h={'amp':38,'lt':60,'gt':62,'quot':34,'apos':39,'nbsp':160};
      if(name in h)return String.fromCharCode(h[name]);
      return m;
    });
    document.getElementById('plainText').value=r;
    document.getElementById('encodeStats').innerHTML='<span>解码实体: <b style="color:#4ade80">'+c+'</b></span><span>总字符: <b>'+r.length+'</b></span>';
  }
  function swapTexts(){var a=document.getElementById('plainText').value;document.getElementById('plainText').value=document.getElementById('entityText').value;document.getElementById('entityText').value=a}
  function clearAll(){document.getElementById('plainText').value='';document.getElementById('entityText').value='';document.getElementById('encodeStats').innerHTML=''}
</script>'''
    else:
        title = "Online HTML Entity Encoder Decoder - Character Escape | Three Formats | Free"
        desc = "Free online HTML entity encoder and decoder - convert special characters to HTML entities and back. Supports &<>\"' reserved characters with decimal, hexadecimal, and named entity formats. Essential for secure web development."
        og_title = "Online HTML Entity Encoder Decoder - Character Escape | Three Formats | Free"
        meta_kw = "HTML entities, entity encoder, HTML encode, HTML decode, special character escape, HTML escape, entity converter"
        tn = TOOLS["html-encode-decode"]
        content_title = "🔤 HTML Entity Encoder / Decoder"
        content_desc = "Convert special characters (<>&\"') to HTML entities and back. Supports named, decimal, and hex formats."
        sample = '<div class="alert">Warning: Enter a <strong>valid</strong> email & password</div>'
        tool_ui = f'''
    <div class="tool-section">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <label>📝 Plain Text (Decoded)</label>
          <textarea id="plainText" placeholder="Enter text to encode...">{sample}</textarea>
        </div>
        <div>
          <label>🔐 HTML Entities (Encoded)</label>
          <textarea id="entityText" placeholder="Enter HTML entities to decode..."></textarea>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="encode()">⬇ Encode</button>
        <button class="btn btn-secondary" onclick="decode()">⬆ Decode</button>
        <button class="btn btn-secondary" onclick="swapTexts()">🔄 Swap</button>
        <button class="btn btn-secondary" onclick="clearAll()">🗑 Clear</button>
      </div>
      <div class="radio-group">
        <label><input type="radio" name="entityMode" value="named" checked> Named (&amp;lt;)</label>
        <label><input type="radio" name="entityMode" value="decimal"> Decimal (&amp;#60;)</label>
        <label><input type="radio" name="entityMode" value="hex"> Hex (&amp;#x3C;)</label>
      </div>
      <div id="encodeStats" class="stat-bar"></div>
    </div>'''
        js = '''<script>
  var chars={'<':'lt','>':'gt','&':'amp','"':'quot',"'":'apos'};
  var named={'lt':60,'gt':62,'amp':38,'quot':34,'apos':39};
  function encode(){
    var t=document.getElementById('plainText').value;
    var mode=document.querySelector('input[name="entityMode"]:checked').value;
    var r='',c=0;
    for(var i=0;i<t.length;i++){
      var ch=t[i],code=t.charCodeAt(i);
      if(ch in chars){
        c++;
        if(mode==='named')r+='&'+chars[ch]+';';
        else if(mode==='decimal')r+='&#'+code+';';
        else r+='&#x'+code.toString(16).toUpperCase()+';';
      }else if(code>127){
        c++;
        if(mode==='named')r+='&#'+code+';';
        else if(mode==='decimal')r+='&#'+code+';';
        else r+='&#x'+code.toString(16).toUpperCase()+';';
      }else{r+=ch}
    }
    document.getElementById('entityText').value=r;
    document.getElementById('encodeStats').innerHTML='<span>Encoded: <b style="color:#4ade80">'+c+'</b></span><span>Total: <b>'+t.length+'</b></span>';
  }
  function decode(){
    var t=document.getElementById('entityText').value,c=0;
    var r=t.replace(/&(?:#(\\d+)|#x([0-9a-fA-F]+)|(\\w+));/g,function(m,dec,hex,name){
      c++;
      if(dec)return String.fromCharCode(parseInt(dec,10));
      if(hex)return String.fromCharCode(parseInt(hex,16));
      var code=named[name];if(code)return String.fromCharCode(code);
      var h={'amp':38,'lt':60,'gt':62,'quot':34,'apos':39,'nbsp':160};
      if(name in h)return String.fromCharCode(h[name]);
      return m;
    });
    document.getElementById('plainText').value=r;
    document.getElementById('encodeStats').innerHTML='<span>Decoded: <b style="color:#4ade80">'+c+'</b></span><span>Total: <b>'+r.length+'</b></span>';
  }
  function swapTexts(){var a=document.getElementById('plainText').value;document.getElementById('plainText').value=document.getElementById('entityText').value;document.getElementById('entityText').value=a}
  function clearAll(){document.getElementById('plainText').value='';document.getElementById('entityText').value='';document.getElementById('encodeStats').innerHTML=''}
</script>'''
    return title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js


def gen_text_to_audio(is_cn):
    if is_cn:
        title = "在线文字转语音工具 - 文本朗读 | 多语音 | 语速调节 | 免费"
        desc = "免费在线文字转语音工具，将文本内容朗读为音频。支持多种语言和声音选择，可调节语速和音调，支持暂停/恢复/停止控制。无需安装，浏览器Web Speech API驱动。"
        og_title = "在线文字转语音工具 - 文本朗读 | 多语音 | 语速调节 | 免费"
        meta_kw = "文字转语音,文本朗读,TTS,语音合成,在线朗读,文字朗读,语音转换,Web Speech"
        tn = TOOLS["text-to-audio"]
        content_title = "🔊 文字转语音"
        content_desc = "将文本转换为语音朗读，支持多种语言和声音，可调节语速、音调，暂停恢复。"
        sample = "欢迎使用在线文字转语音工具。这是一个免费的浏览器端文本朗读工具，无需安装任何软件。"
        tool_ui = f'''
    <div class="tool-section">
      <label>📝 输入文本</label>
      <textarea id="ttsText" placeholder="在此输入要朗读的文本..." style="min-height:120px">{sample}</textarea>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px">
        <div>
          <label>🌐 语言/声音</label>
          <select id="voiceSelect"></select>
        </div>
        <div>
          <label>⏩ 语速 (0.5-3)</label>
          <input type="range" id="rateSlider" min="0.5" max="3" step="0.1" value="1" oninput="document.getElementById('rateVal').textContent=this.value">
          <span id="rateVal" style="color:#94a3b8;font-size:.8rem">1</span>
        </div>
        <div>
          <label>🎵 音调 (0.5-2)</label>
          <input type="range" id="pitchSlider" min="0.5" max="2" step="0.1" value="1" oninput="document.getElementById('pitchVal').textContent=this.value">
          <span id="pitchVal" style="color:#94a3b8;font-size:.8rem">1</span>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="speak()">▶ 朗读</button>
        <button class="btn btn-secondary" onclick="pauseResume()">⏯ 暂停/恢复</button>
        <button class="btn btn-secondary" onclick="stopSpeaking()">⏹ 停止</button>
      </div>
      <div id="ttsStatus" class="stat-bar" style="margin-top:8px"></div>
    </div>'''
        js = '''<script>
  var synth=window.speechSynthesis,utterance=null,voices=[],isPaused=false;
  function loadVoices(){
    voices=synth.getVoices();
    var sel=document.getElementById('voiceSelect'),html='';
    var filtered=voices.filter(function(v){return v.lang.startsWith('zh')||v.lang.startsWith('en')});
    if(!filtered.length)filtered=voices;
    for(var i=0;i<filtered.length;i++){
      html+='<option value="'+i+'">'+filtered[i].name+' ('+filtered[i].lang+')</option>';
    }
    sel.innerHTML=html||'<option>无可用声音</option>';
    if(filtered.length){
      var def=filtered.findIndex(function(v){return v.default})||0;
      sel.selectedIndex=def;
    }
  }
  loadVoices();
  if(synth.onvoiceschanged!==undefined)synth.onvoiceschanged=loadVoices;
  function speak(){
    var text=document.getElementById('ttsText').value.trim();
    if(!text){showToast('请输入要朗读的文本');return}
    stopSpeaking();
    utterance=new SpeechSynthesisUtterance(text);
    var vi=parseInt(document.getElementById('voiceSelect').value);
    var filtered=voices.filter(function(v){return v.lang.startsWith('zh')||v.lang.startsWith('en')});
    if(!filtered.length)filtered=voices;
    if(filtered[vi])utterance.voice=filtered[vi];
    utterance.rate=parseFloat(document.getElementById('rateSlider').value);
    utterance.pitch=parseFloat(document.getElementById('pitchSlider').value);
    utterance.onstart=function(){document.getElementById('ttsStatus').innerHTML='<span style="color:#4ade80">▶ 正在朗读...</span>';isPaused=false}
    utterance.onend=function(){document.getElementById('ttsStatus').innerHTML='<span style="color:#94a3b8">✓ 朗读完成</span>';isPaused=false}
    utterance.onerror=function(e){document.getElementById('ttsStatus').innerHTML='<span style="color:#f87171">✗ 朗读出错</span>'}
    synth.speak(utterance);
  }
  function pauseResume(){
    if(synth.speaking&&!isPaused){synth.pause();isPaused=true;document.getElementById('ttsStatus').innerHTML='<span style="color:#fbbf24">⏸ 已暂停</span>'}
    else if(synth.paused){synth.resume();isPaused=false;document.getElementById('ttsStatus').innerHTML='<span style="color:#4ade80">▶ 继续朗读...</span>'}
  }
  function stopSpeaking(){synth.cancel();isPaused=false;document.getElementById('ttsStatus').innerHTML='<span style="color:#94a3b8">⏹ 已停止</span>'}
</script>'''
    else:
        title = "Online Text to Speech Converter - Read Text Aloud | Multi-Voice | Speed Control | Free"
        desc = "Free online text to speech converter - read text aloud as audio. Supports multiple languages and voice options with adjustable speed and pitch. Pause/resume/stop controls. No installation, powered by browser Web Speech API."
        og_title = "Online Text to Speech Converter - Read Text Aloud | Multi-Voice | Speed Control | Free"
        meta_kw = "text to speech, text reader, TTS, speech synthesis, online reader, read aloud, voice converter, Web Speech"
        tn = TOOLS["text-to-audio"]
        content_title = "🔊 Text to Speech"
        content_desc = "Convert text to spoken audio with multiple language and voice options. Adjustable speed, pitch, pause/resume support."
        sample = "Welcome to the online text to speech converter. This is a free browser-based text reading tool that requires no software installation."
        tool_ui = f'''
    <div class="tool-section">
      <label>📝 Input Text</label>
      <textarea id="ttsText" placeholder="Enter text to read aloud..." style="min-height:120px">{sample}</textarea>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px">
        <div>
          <label>🌐 Language / Voice</label>
          <select id="voiceSelect"></select>
        </div>
        <div>
          <label>⏩ Speed (0.5-3)</label>
          <input type="range" id="rateSlider" min="0.5" max="3" step="0.1" value="1" oninput="document.getElementById('rateVal').textContent=this.value">
          <span id="rateVal" style="color:#94a3b8;font-size:.8rem">1</span>
        </div>
        <div>
          <label>🎵 Pitch (0.5-2)</label>
          <input type="range" id="pitchSlider" min="0.5" max="2" step="0.1" value="1" oninput="document.getElementById('pitchVal').textContent=this.value">
          <span id="pitchVal" style="color:#94a3b8;font-size:.8rem">1</span>
        </div>
      </div>
      <div class="btn-group">
        <button class="btn btn-primary" onclick="speak()">▶ Speak</button>
        <button class="btn btn-secondary" onclick="pauseResume()">⏯ Pause/Resume</button>
        <button class="btn btn-secondary" onclick="stopSpeaking()">⏹ Stop</button>
      </div>
      <div id="ttsStatus" class="stat-bar" style="margin-top:8px"></div>
    </div>'''
        js = '''<script>
  var synth=window.speechSynthesis,utterance=null,voices=[],isPaused=false;
  function loadVoices(){
    voices=synth.getVoices();
    var sel=document.getElementById('voiceSelect'),html='';
    var filtered=voices.filter(function(v){return v.lang.startsWith('zh')||v.lang.startsWith('en')});
    if(!filtered.length)filtered=voices;
    for(var i=0;i<filtered.length;i++){
      html+='<option value="'+i+'">'+filtered[i].name+' ('+filtered[i].lang+')</option>';
    }
    sel.innerHTML=html||'<option>No voices available</option>';
    if(filtered.length){
      var def=filtered.findIndex(function(v){return v.default})||0;
      sel.selectedIndex=def;
    }
  }
  loadVoices();
  if(synth.onvoiceschanged!==undefined)synth.onvoiceschanged=loadVoices;
  function speak(){
    var text=document.getElementById('ttsText').value.trim();
    if(!text){showToast('Please enter text to read');return}
    stopSpeaking();
    utterance=new SpeechSynthesisUtterance(text);
    var vi=parseInt(document.getElementById('voiceSelect').value);
    var filtered=voices.filter(function(v){return v.lang.startsWith('zh')||v.lang.startsWith('en')});
    if(!filtered.length)filtered=voices;
    if(filtered[vi])utterance.voice=filtered[vi];
    utterance.rate=parseFloat(document.getElementById('rateSlider').value);
    utterance.pitch=parseFloat(document.getElementById('pitchSlider').value);
    utterance.onstart=function(){document.getElementById('ttsStatus').innerHTML='<span style="color:#4ade80">▶ Speaking...</span>';isPaused=false}
    utterance.onend=function(){document.getElementById('ttsStatus').innerHTML='<span style="color:#94a3b8">✓ Finished</span>';isPaused=false}
    utterance.onerror=function(e){document.getElementById('ttsStatus').innerHTML='<span style="color:#f87171">✗ Error</span>'}
    synth.speak(utterance);
  }
  function pauseResume(){
    if(synth.speaking&&!isPaused){synth.pause();isPaused=true;document.getElementById('ttsStatus').innerHTML='<span style="color:#fbbf24">⏸ Paused</span>'}
    else if(synth.paused){synth.resume();isPaused=false;document.getElementById('ttsStatus').innerHTML='<span style="color:#4ade80">▶ Resumed...</span>'}
  }
  function stopSpeaking(){synth.cancel();isPaused=false;document.getElementById('ttsStatus').innerHTML='<span style="color:#94a3b8">⏹ Stopped</span>'}
</script>'''
    return title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js


# ============ BUILD ALL PAGES ============

def build_page(slug, is_cn):
    """generate full HTML for a tool"""
    if slug == "file-diff":
        title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js = gen_file_diff(is_cn)
    elif slug == "css-selector-tester":
        title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js = gen_css_selector_tester(is_cn)
    elif slug == "xpath-tester":
        title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js = gen_xpath_tester(is_cn)
    elif slug == "html-encode-decode":
        title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js = gen_html_encoder(is_cn)
    elif slug == "text-to-audio":
        title, desc, og_title, meta_kw, tn, content_title, content_desc, tool_ui, js = gen_text_to_audio(is_cn)

    canonical = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
    og_url = canonical
    lang = 'lang="zh-CN"' if is_cn else 'lang="en"'
    lang_switch_cn = '<a href="/en/' + slug + '/">EN</a>'
    lang_switch_en = '<a href="/' + slug + '/">中文</a>'
    nav_back_text = '← 返回首页' if is_cn else '← Back to Home'
    nav_back_url = '/' if is_cn else '/en/'

    schema = gen_schema(tn['name_en'], desc, is_cn)
    faq = gen_faq(is_cn, tn['name_en'])
    howto = gen_howto(is_cn, tn['name_en'], slug)
    footer_html = gen_footer(is_cn)

    name_display = tn['name_cn'] if is_cn else tn['name_en']
    breadcrumb_name = tn['name_cn'] if is_cn else tn['name_en']

    page = f'''<!DOCTYPE html>
<html {lang}>
<head>
{GTAG}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{meta_kw}">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{"在线小工具矩阵" if is_cn else "Free ToolBase"}">
{schema}
{faq}
{howto}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "{"首页" if is_cn else "Home"}",
      "item": "https://free-toolbase.com{"/" if is_cn else "/en/"}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{breadcrumb_name}",
      "item": "{canonical}"
    }}
  ]
}}
</script>
{CSS}
</head>
<body>
<div class="container">
  <div class="nav-back"><a href="{nav_back_url}">{nav_back_text}</a></div>
  <header class="header">
    <h1>{name_display}</h1>
    <div class="lang-switch">
      {'<a class="active" href="' + canonical + '">中文</a>' + lang_switch_en if is_cn else lang_switch_cn + '<a class="active" href="' + canonical + '">EN</a>'}
    </div>
  </header>
{tool_ui}
  <div class="content-section">
    <h2>{"关于此工具" if is_cn else "About This Tool"}</h2>
    <p>{content_desc}</p>
  </div>
  <div class="content-section">
    <h2>{"常见问题" if is_cn else "FAQ"}</h2>
    {''.join('<div class="faq-item"><div class="q">'+(q if is_cn else q_en)+'</div><div class="a">'+(a if is_cn else a_en)+'</div></div>' for q,a,q_en,a_en in [
      ("这个工具收费吗？", "完全免费。本工具属于在线小工具矩阵的一部分，所有功能均无需注册、无需付费即可使用。", "Is this tool free?", "Yes, completely free. This tool is part of our free online tools collection. No registration or payment required."),
      ("数据会上传到服务器吗？", "不会。所有处理操作完全在您的浏览器中执行，输入数据不会上传到任何服务器，充分保障隐私安全。", "Is my data uploaded to a server?", "No. All processing happens entirely in your browser. No data is uploaded to any server, ensuring complete privacy."),
      ("支持哪些浏览器？", "支持所有现代浏览器，包括Chrome、Firefox、Safari、Edge等。推荐使用最新版本。", "Which browsers are supported?", "All modern browsers are supported, including Chrome, Firefox, Safari, and Edge. Use the latest version for best experience."),
      ("可以在手机上使用吗？", "可以。本工具完全响应式设计，在手机和平板设备上均可正常使用。", "Can I use it on mobile?", "Yes. This tool is fully responsive and works great on phones and tablets."),
    ])}
  </div>
{footer_html}
</div>
{gen_toast()}
{js}
</body>
</html>'''

    # fix breadcrumb emoji
    page = page.replace('name_display', name_display)
    return page


# ============ MAIN ============

def main():
    slugs = ["file-diff", "css-selector-tester", "xpath-tester", "html-encode-decode", "text-to-audio"]
    for slug in slugs:
        # CN version
        cn_dir = os.path.join(BASE, slug)
        os.makedirs(cn_dir, exist_ok=True)
        cn_html = build_page(slug, is_cn=True)
        cn_path = os.path.join(cn_dir, "index.html")
        with open(cn_path, "w", encoding="utf-8") as f:
            f.write(cn_html)
        print(f"Created: {cn_path}")

        # EN version
        en_dir = os.path.join(BASE, "en", slug)
        os.makedirs(en_dir, exist_ok=True)
        en_html = build_page(slug, is_cn=False)
        en_path = os.path.join(en_dir, "index.html")
        with open(en_path, "w", encoding="utf-8") as f:
            f.write(en_html)
        print(f"Created: {en_path}")

    print(f"\nDone: {len(slugs)} tools x2 = {len(slugs)*2} pages created")


if __name__ == "__main__":
    main()
