#!/usr/bin/env python3
"""生成10个新工具 - 使用 .format() 避免 f-string backslash 限制"""
import os, json

BASE = "/home/chison/tools-site"

# ===== 模板 =====
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com{tool_url}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{desc}">
  <link rel="canonical" href="https://free-toolbase.com{tool_url}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{name}",
    "description": "{desc}",
    "applicationCategory": "WebApplication",
    "operatingSystem": "All",
    "url": "https://free-toolbase.com{tool_url}",
    "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
  }}
  </script>
  <style>
  :root {{
    --primary: #4F46E5;
    --primary-dark: #4338CA;
    --bg: #f8fafc;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --shadow: 0 1px 3px rgba(0,0,0,.1);
    --radius: 12px;
  }}
  *,*::before,*::after {{box-sizing:border-box;margin:0;padding:0}}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }}
  header {{
    background: var(--card-bg);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }}
  header .logo {{
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
  }}
  header nav {{display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
  header nav a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-size: .9rem;
    transition: color .2s;
  }}
  header nav a:hover {{color:var(--primary)}}
  .lang-switch {{
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: .85rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all .2s;
  }}
  .lang-switch:hover {{border-color:var(--primary);color:var(--primary)}}
  main {{
    flex: 1;
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 20px;
    width: 100%;
  }}
  h1 {{
    font-size: 1.8rem;
    margin-bottom: 8px;
    color: var(--text);
  }}
  .subtitle {{
    color: var(--text-secondary);
    margin-bottom: 28px;
    font-size: .95rem;
  }}
  .tool-area {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow);
  }}
  .tool-area label {{
    display: block;
    font-weight: 600;
    margin-bottom: 6px;
    font-size: .9rem;
    color: var(--text);
  }}
  .tool-area input[type="text"],
  .tool-area input[type="number"],
  .tool-area textarea,
  .tool-area select {{
    width: 100%;
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: .95rem;
    font-family: inherit;
    margin-bottom: 16px;
    transition: border-color .2s;
    background: #fff;
  }}
  .tool-area input:focus,
  .tool-area textarea:focus,
  .tool-area select:focus {{
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(79,70,229,.1);
  }}
  .tool-area textarea {{min-height:120px;resize:vertical}}
  .tool-area .row {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .tool-area .row > * {{flex:1;min-width:150px}}
  .btn {{
    display: inline-block;
    padding: 10px 24px;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: .95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all .2s;
  }}
  .btn:hover {{background:var(--primary-dark);transform:translateY(-1px)}}
  .btn:active {{transform:translateY(0)}}
  .btn-secondary {{
    background: #fff;
    color: var(--primary);
    border: 1px solid var(--primary);
  }}
  .btn-secondary:hover {{background:rgba(79,70,229,.05)}}
  .output {{
    margin-top: 20px;
    padding: 16px;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: .95rem;
    white-space: pre-wrap;
    word-break: break-word;
    min-height: 48px;
    color: var(--text);
    border: 1px solid var(--border);
  }}
  .output:empty {{display:none}}
  .result-item {{
    padding: 12px;
    margin-bottom: 8px;
    background: #fff;
    border-radius: 6px;
    border: 1px solid var(--border);
  }}
  footer {{
    text-align: center;
    padding: 24px;
    color: var(--text-secondary);
    font-size: .85rem;
    border-top: 1px solid var(--border);
    background: var(--card-bg);
  }}
  footer a {{color:var(--primary);text-decoration:none}}
  .toast {{
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    background: #1e293b;
    color: #fff;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: .9rem;
    z-index: 1000;
    opacity: 0;
    transition: opacity .3s;
    pointer-events: none;
  }}
  .toast.show {{opacity:1}}
  @media (max-width: 600px) {{
    main {{padding:16px 12px}}
    h1 {{font-size:1.4rem}}
    .tool-area {{padding:16px}}
  }}
  </style>
</head>
<body>
  <header>
    <a href="{home_url}" class="logo">{site_name}</a>
    <nav>
      <a href="{home_url}">{home_label}</a>
      <a href="{other_lang_url}" class="lang-switch">{lang_switch_label}</a>
    </nav>
  </header>
  <main>
    <h1>{name}</h1>
    <p class="subtitle">{short}</p>
    <div class="tool-area">
{tool_body}
    </div>
  </main>
  <footer>
    <p>&copy; 2024 <a href="{home_url}">Free ToolBase</a> | {footer_text}</p>
  </footer>
  <div class="toast" id="toast"></div>
  <script>
  function showToast(msg) {{
    var t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(function(){{t.classList.remove('show')}}, 2000);
  }}
  function copyText(text) {{
    if (navigator.clipboard) {{
      navigator.clipboard.writeText(text).then(function(){{showToast('{copied}')}});
    }} else {{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('{copied}');
    }}
  }}
  </script>
</body>
</html>"""

def gen_page(tool, lang, tool_body):
    """生成完整页面"""
    is_cn = lang == "cn"
    slug = tool["slug"]
    name = tool["cn_name"] if is_cn else tool["en_name"]
    desc = tool["cn_desc"] if is_cn else tool["en_desc"]
    short = tool["cn_short"] if is_cn else tool["en_short"]
    keywords = tool["cn_kw"] if is_cn else tool["en_kw"]
    
    return PAGE_TEMPLATE.format(
        lang_attr="zh-CN" if is_cn else "en",
        title="{} - {}".format(name, "在线小工具矩阵" if is_cn else "Free ToolBase"),
        name=name, desc=desc, short=short, keywords=keywords,
        og_title="{} - {}".format(name, "Free ToolBase" if not is_cn else "在线小工具矩阵"),
        tool_url="/" + slug + "/" if not is_cn else "/" + slug + "/",
        home_url="/" if is_cn else "/en/",
        site_name="在线小工具矩阵" if is_cn else "Free ToolBase",
        home_label="首页" if is_cn else "Home",
        other_lang_url="/en/" + slug + "/" if is_cn else "/" + slug + "/",
        lang_switch_label="EN" if is_cn else "中文",
        footer_text="所有工具均在浏览器本地运行" if is_cn else "All tools run locally in your browser",
        copied="已复制！" if is_cn else "Copied!",
        tool_body=tool_body
    )

# ===== 各工具 body 生成函数 =====

def body_meme_text(is_cn):
    top_lbl = "上方文字" if is_cn else "Top Text"
    top_ph = "（例：没有人可以）" if is_cn else "(e.g. ONE DOES NOT SIMPLY)"
    btm_lbl = "下方文字" if is_cn else "Bottom Text"
    btm_ph = "（例：走进魔多）" if is_cn else "(e.g. WALK INTO MORDOR)"
    fs_lbl = "字号" if is_cn else "Font Size"
    col_lbl = "颜色" if is_cn else "Color"
    ol_lbl = "描边" if is_cn else "Outline"
    gen_btn = "生成梗图" if is_cn else "Generate Meme"
    dl_btn = "下载" if is_cn else "Download"
    placeholder_text = "输入文字生成梗图" if is_cn else "Enter text above to generate"
    dl_toast = "已下载！" if is_cn else "Downloaded!"
    
    return """      <label for="topText">{top_lbl}</label>
      <input type="text" id="topText" placeholder="{top_ph}" maxlength="60">
      <label for="bottomText">{btm_lbl}</label>
      <input type="text" id="bottomText" placeholder="{btm_ph}" maxlength="60">
      <div class="row">
        <div><label for="fontSize">{fs_lbl}</label><input type="number" id="fontSize" value="32" min="16" max="80"></div>
        <div><label for="fontColor">{col_lbl}</label><input type="color" id="fontColor" value="#ffffff"></div>
        <div><label for="strokeColor">{ol_lbl}</label><input type="color" id="strokeColor" value="#000000"></div>
      </div>
      <button class="btn" id="generateBtn">{gen_btn}</button>
      <button class="btn btn-secondary" id="downloadBtn" style="margin-left:8px">{dl_btn}</button>
      <div style="margin-top:20px;text-align:center;background:#000;border-radius:8px;padding:20px;min-height:200px;display:flex;align-items:center;justify-content:center" id="memeCanvas">
        <canvas id="canvas" style="max-width:100%"></canvas>
      </div>
      <script>
      var canvas = document.getElementById('canvas');
      var ctx = canvas.getContext('2d');
      canvas.width = 600;
      canvas.height = 400;
      function drawMeme() {{
        var top = document.getElementById('topText').value.toUpperCase();
        var bottom = document.getElementById('bottomText').value.toUpperCase();
        var fontSize = parseInt(document.getElementById('fontSize').value);
        var fontColor = document.getElementById('fontColor').value;
        var strokeColor = document.getElementById('strokeColor').value;
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = 'bold ' + fontSize + 'px Impact, Arial Black, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = fontColor;
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = fontSize / 8;
        if (top) {{ ctx.strokeText(top, canvas.width/2, fontSize + 10); ctx.fillText(top, canvas.width/2, fontSize + 10); }}
        if (bottom) {{ ctx.strokeText(bottom, canvas.width/2, canvas.height - 20); ctx.fillText(bottom, canvas.width/2, canvas.height - 20); }}
        if (!top && !bottom) {{ ctx.fillStyle = '#666'; ctx.font = '20px sans-serif'; ctx.fillText('{placeholder_text}', canvas.width/2, canvas.height/2); }}
      }}
      document.getElementById('generateBtn').addEventListener('click', drawMeme);
      document.getElementById('downloadBtn').addEventListener('click', function() {{
        var link = document.createElement('a');
        link.download = 'meme.png';
        link.href = canvas.toDataURL();
        link.click();
        showToast('{dl_toast}');
      }});
      drawMeme();
      </script>""".format(top_lbl=top_lbl, top_ph=top_ph, btm_lbl=btm_lbl, btm_ph=btm_ph,
                       fs_lbl=fs_lbl, col_lbl=col_lbl, ol_lbl=ol_lbl,
                       gen_btn=gen_btn, dl_btn=dl_btn,
                       placeholder_text=placeholder_text, dl_toast=dl_toast)


def body_image_resize_bulk(is_cn):
    sel_lbl = "选择图片" if is_cn else "Select Images"
    mode_lbl = "缩放模式" if is_cn else "Mode"
    val_lbl = "数值" if is_cn else "Value"
    pct = "百分比缩放" if is_cn else "Percentage"
    fw = "固定宽度" if is_cn else "Fixed Width"
    fh = "固定高度" if is_cn else "Fixed Height"
    mx = "最大边限制" if is_cn else "Max Dimension"
    rz_all = "全部缩放" if is_cn else "Resize All"
    dl_all = "下载全部" if is_cn else "Download All"
    sel_first = "请先选择图片" if is_cn else "Please select images first"
    resized = " 张图片已缩放" if is_cn else " images resized"
    rz_first = "请先缩放图片" if is_cn else "Resize images first"
    downloaded = " 张已下载" if is_cn else " downloaded"
    
    return """      <label for="imageInput">{sel_lbl}</label>
      <input type="file" id="imageInput" accept="image/*" multiple>
      <div class="row">
        <div><label for="resizeMode">{mode_lbl}</label>
          <select id="resizeMode">
            <option value="percent">{pct}</option>
            <option value="width">{fw}</option>
            <option value="height">{fh}</option>
            <option value="max">{mx}</option>
          </select>
        </div>
        <div><label for="resizeValue">{val_lbl}</label><input type="number" id="resizeValue" value="50" min="1"></div>
      </div>
      <div class="row">
        <button class="btn" id="resizeBtn">{rz_all}</button>
        <button class="btn btn-secondary" id="downloadAllBtn">{dl_all}</button>
      </div>
      <div id="previewArea" style="margin-top:16px;display:flex;flex-wrap:wrap;gap:12px"></div>
      <script>
      var resizedImages = [];
      document.getElementById('resizeBtn').addEventListener('click', function() {{
        var files = document.getElementById('imageInput').files;
        if (!files.length) {{ showToast('{sel_first}'); return; }}
        var mode = document.getElementById('resizeMode').value;
        var val = parseFloat(document.getElementById('resizeValue').value);
        resizedImages = [];
        var preview = document.getElementById('previewArea');
        preview.innerHTML = '';
        var count = 0;
        Array.from(files).forEach(function(file, i) {{
          var reader = new FileReader();
          reader.onload = function(e) {{
            var img = new Image();
            img.onload = function() {{
              var c = document.createElement('canvas');
              var w = img.width, h = img.height;
              if (mode === 'percent') {{ w *= val/100; h *= val/100; }}
              else if (mode === 'width') {{ h = h * (val/w); w = val; }}
              else if (mode === 'height') {{ w = w * (val/h); h = val; }}
              else if (mode === 'max') {{
                if (w > h) {{ if (w > val) {{ h = h*(val/w); w = val; }} }}
                else {{ if (h > val) {{ w = w*(val/h); h = val; }} }}
              }}
              c.width = Math.round(w); c.height = Math.round(h);
              var ctx2 = c.getContext('2d');
              ctx2.drawImage(img, 0, 0, c.width, c.height);
              resizedImages.push({{name:file.name, canvas:c}});
              var wrapper = document.createElement('div');
              wrapper.style.cssText = 'text-align:center;width:140px';
              var thumb = document.createElement('canvas');
              thumb.width = 120;
              thumb.height = 120 * (c.height/c.width) || 120;
              var tctx = thumb.getContext('2d');
              tctx.drawImage(c, 0, 0, thumb.width, thumb.height);
              wrapper.appendChild(thumb);
              var label = document.createElement('div');
              label.textContent = Math.round(c.width) + 'x' + Math.round(c.height);
              label.style.cssText = 'font-size:.75rem;margin-top:4px;color:#666';
              wrapper.appendChild(label);
              preview.appendChild(wrapper);
              count++;
              if (count === files.length) showToast(count + '{resized}');
            }};
            img.src = e.target.result;
          }};
          reader.readAsDataURL(file);
        }});
      }});
      document.getElementById('downloadAllBtn').addEventListener('click', function() {{
        if (!resizedImages.length) {{ showToast('{rz_first}'); return; }}
        resizedImages.forEach(function(item) {{
          var link = document.createElement('a');
          link.download = 'resized_' + item.name;
          link.href = item.canvas.toDataURL('image/png');
          link.click();
        }});
        showToast(resizedImages.length + '{downloaded}');
      }});
      </script>""".format(sel_lbl=sel_lbl, mode_lbl=mode_lbl, val_lbl=val_lbl,
                       pct=pct, fw=fw, fh=fh, mx=mx,
                       rz_all=rz_all, dl_all=dl_all,
                       sel_first=sel_first, resized=resized,
                       rz_first=rz_first, downloaded=downloaded)


def body_csv_to_html(is_cn):
    paste = "粘贴CSV数据" if is_cn else "Paste CSV Data"
    ph = "姓名,年龄,城市\\n张三,30,北京\\n李四,25,上海" if is_cn else "name,age,city\\nAlice,30,NYC\\nBob,25,LA"
    hdr = "首行为表头" if is_cn else "First row as header"
    cls_lbl = "表格CSS类" if is_cn else "Table Class"
    conv = "转换" if is_cn else "Convert"
    copy_btn = "复制HTML" if is_cn else "Copy HTML"
    html_out = "HTML代码" if is_cn else "HTML Code"
    prev = "表格预览" if is_cn else "Preview"
    paste_req = "请粘贴CSV数据" if is_cn else "Please paste CSV data"
    inv = "CSV格式无效" if is_cn else "Invalid CSV"
    done = "转换完成！" if is_cn else "Converted!"
    conv_first = "请先转换" if is_cn else "Convert first"
    
    return """      <label for="csvInput">{paste}</label>
      <textarea id="csvInput" placeholder="{ph}"></textarea>
      <div class="row">
        <div><label><input type="checkbox" id="firstRowHeader" checked> {hdr}</label></div>
        <div><label for="tableClass">{cls_lbl}</label><input type="text" id="tableClass" placeholder="表格样式"></div>
      </div>
      <div class="row">
        <button class="btn" id="convertBtn">{conv}</button>
        <button class="btn btn-secondary" id="copyBtn">{copy_btn}</button>
      </div>
      <label style="margin-top:16px">{html_out}</label>
      <textarea id="htmlOutput" readonly style="font-family:monospace;font-size:.85rem"></textarea>
      <label style="margin-top:12px">{prev}</label>
      <div id="tablePreview" class="output" style="overflow-x:auto"></div>
      <script>
      function parseCSV(text) {{
        var rows = [], lines = text.trim().split(/\\n/);
        lines.forEach(function(line) {{
          var cols = [], inQuote = false, col = '';
          for (var i = 0; i < line.length; i++) {{
            var ch = line[i];
            if (ch === '"') {{ inQuote = !inQuote; }}
            else if (ch === ',' && !inQuote) {{ cols.push(col.trim()); col = ''; }}
            else {{ col += ch; }}
          }}
          cols.push(col.trim()); rows.push(cols);
        }});
        return rows;
      }}
      function escapeHtml(str) {{ return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }}
      document.getElementById('convertBtn').addEventListener('click', function() {{
        var csv = document.getElementById('csvInput').value;
        if (!csv.trim()) {{ showToast('{paste_req}'); return; }}
        var rows = parseCSV(csv);
        if (!rows.length) {{ showToast('{inv}'); return; }}
        var useHeader = document.getElementById('firstRowHeader').checked;
        var cls = document.getElementById('tableClass').value || '';
        var html = '<table' + (cls ? ' class="' + cls.replace(/"/g,'') + '"' : '') + '>\\n';
        var startRow = 0;
        if (useHeader && rows.length > 0) {{
          html += '  <thead>\\n    <tr>\\n';
          rows[0].forEach(function(cell) {{ html += '      <th>' + escapeHtml(cell) + '</th>\\n'; }});
          html += '    </tr>\\n  </thead>\\n  <tbody>\\n';
          startRow = 1;
        }} else {{ html += '  <tbody>\\n'; }}
        for (var i = startRow; i < rows.length; i++) {{
          html += '    <tr>\\n';
          rows[i].forEach(function(cell) {{ html += '      <td>' + escapeHtml(cell) + '</td>\\n'; }});
          html += '    </tr>\\n';
        }}
        html += '  </tbody>\\n</table>';
        document.getElementById('htmlOutput').value = html;
        document.getElementById('tablePreview').innerHTML = html;
        showToast('{done}');
      }});
      document.getElementById('copyBtn').addEventListener('click', function() {{
        var html = document.getElementById('htmlOutput').value;
        if (!html) {{ showToast('{conv_first}'); return; }}
        copyText(html);
      }});
      </script>""".format(paste=paste, ph=ph, hdr=hdr, cls_lbl=cls_lbl,
                       conv=conv, copy_btn=copy_btn, html_out=html_out, prev=prev,
                       paste_req=paste_req, inv=inv, done=done, conv_first=conv_first)


def body_smart_rename(is_cn):
    paste_lbl = "粘贴文件名（每行一个）" if is_cn else "Paste File Names (one per line)"
    ph = "照片1.jpg\\n照片2.jpg\\n照片3.jpg" if is_cn else "photo1.jpg\\nphoto2.jpg\\nphoto3.jpg"
    op_lbl = "操作" if is_cn else "Operation"
    add_pre = "添加前缀" if is_cn else "Add Prefix"
    add_suf = "添加后缀" if is_cn else "Add Suffix"
    rep_txt = "替换文字" if is_cn else "Replace Text"
    upper = "转大写" if is_cn else "To UPPERCASE"
    lower = "转小写" if is_cn else "To lowercase"
    add_num = "添加序号" if is_cn else "Add Numbering"
    prefix_label = "前缀" if is_cn else "Prefix"
    suffix_label = "后缀" if is_cn else "Suffix"
    find_label = "查找" if is_cn else "Find"
    replace_label = "替换为" if is_cn else "Replace With"
    start_num_label = "起始序号" if is_cn else "Start Number"
    preview_btn = "预览重命名" if is_cn else "Preview Rename"
    copy_res = "复制结果" if is_cn else "Copy Results"
    enter_names = "请输入文件名" if is_cn else "Enter file names"
    rename_first = "请先重命名" if is_cn else "Rename first"
    
    return """      <label for="fileNames">{paste_lbl}</label>
      <textarea id="fileNames" placeholder="{ph}"></textarea>
      <div class="row">
        <div><label for="operation">{op_lbl}</label>
          <select id="operation">
            <option value="prefix">{add_pre}</option>
            <option value="suffix">{add_suf}</option>
            <option value="replace">{rep_txt}</option>
            <option value="uppercase">{upper}</option>
            <option value="lowercase">{lower}</option>
            <option value="number">{add_num}</option>
          </select>
        </div>
        <div><label for="opValue" id="opLabel">{prefix_label}</label><input type="text" id="opValue" placeholder="IMG_"></div>
        <div><label for="opValue2" id="opLabel2" style="display:none">{replace_label}</label><input type="text" id="opValue2" placeholder="" style="display:none"></div>
      </div>
      <button class="btn" id="renameBtn">{preview_btn}</button>
      <button class="btn btn-secondary" id="copyNamesBtn" style="margin-left:8px">{copy_res}</button>
      <div id="renameResult" class="output"></div>
      <script>
      var prefixLabel = '{prefix_label}', suffixLabel = '{suffix_label}', findLabel = '{find_label}';
      var replaceLabel = '{replace_label}', startNumLabel = '{start_num_label}';
      document.getElementById('operation').addEventListener('change', function() {{
        var op = this.value;
        var label = document.getElementById('opLabel');
        var v1 = document.getElementById('opValue');
        var l2 = document.getElementById('opLabel2');
        var v2 = document.getElementById('opValue2');
        if (op === 'prefix') {{ label.textContent = prefixLabel; v1.style.display=''; l2.style.display='none'; v2.style.display='none'; }}
        else if (op === 'suffix') {{ label.textContent = suffixLabel; v1.style.display=''; l2.style.display='none'; v2.style.display='none'; }}
        else if (op === 'replace') {{ label.textContent = findLabel; v1.style.display=''; l2.style.display=''; v2.style.display=''; }}
        else if (op === 'number') {{ label.textContent = startNumLabel; v1.style.display=''; v1.type='number'; v1.value='1'; l2.style.display='none'; v2.style.display='none'; }}
        else {{ v1.style.display='none'; l2.style.display='none'; v2.style.display='none'; }}
        if (op !== 'number') v1.type = 'text';
        if (op !== 'replace') {{ l2.style.display='none'; v2.style.display='none'; }}
      }});
      function escapeHtml2(s) {{ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
      document.getElementById('renameBtn').addEventListener('click', function() {{
        var names = document.getElementById('fileNames').value.split('\\n').filter(function(n){{return n.trim()}});
        if (!names.length) {{ showToast('{enter_names}'); return; }}
        var op = document.getElementById('operation').value;
        var val = document.getElementById('opValue').value;
        var val2 = document.getElementById('opValue2').value;
        var result = [];
        names.forEach(function(name, i) {{
          var trimmed = name.trim();
          var ext = '';
          var dotIdx = trimmed.lastIndexOf('.');
          var base = trimmed;
          if (dotIdx > 0 && dotIdx < trimmed.length - 1) {{ ext = trimmed.substring(dotIdx); base = trimmed.substring(0, dotIdx); }}
          if (op === 'prefix') base = val + base;
          else if (op === 'suffix') base = base + val;
          else if (op === 'replace') base = base.split(val).join(val2);
          else if (op === 'uppercase') base = base.toUpperCase();
          else if (op === 'lowercase') base = base.toLowerCase();
          else if (op === 'number') base = base + '_' + (parseInt(val) + i);
          result.push(base + ext);
        }});
        var out = document.getElementById('renameResult');
        out.innerHTML = result.map(function(r){{return '<div class="result-item">' + escapeHtml2(r) + '</div>'}}).join('');
      }});
      document.getElementById('copyNamesBtn').addEventListener('click', function() {{
        var items = document.querySelectorAll('#renameResult .result-item');
        if (!items.length) {{ showToast('{rename_first}'); return; }}
        var text = Array.from(items).map(function(el){{return el.textContent}}).join('\\n');
        copyText(text);
      }});
      </script>""".format(
        paste_lbl=paste_lbl, ph=ph, op_lbl=op_lbl,
        add_pre=add_pre, add_suf=add_suf, rep_txt=rep_txt,
        upper=upper, lower=lower, add_num=add_num,
        prefix_label=prefix_label, suffix_label=suffix_label,
        find_label=find_label, replace_label=replace_label, start_num_label=start_num_label,
        preview_btn=preview_btn, copy_res=copy_res,
        enter_names=enter_names, rename_first=rename_first
    )


def body_daily_horoscope(is_cn):
    sel_zodiac = "选择星座" if is_cn else "Select Zodiac Sign"
    get_btn = "查看今日运势" if is_cn else "Get Today Horoscope"
    aries = "白羊座 (3/21-4/19)" if is_cn else "Aries (Mar 21 - Apr 19)"
    taurus = "金牛座 (4/20-5/20)" if is_cn else "Taurus (Apr 20 - May 20)"
    gemini = "双子座 (5/21-6/20)" if is_cn else "Gemini (May 21 - Jun 20)"
    cancer = "巨蟹座 (6/21-7/22)" if is_cn else "Cancer (Jun 21 - Jul 22)"
    leo = "狮子座 (7/23-8/22)" if is_cn else "Leo (Jul 23 - Aug 22)"
    virgo = "处女座 (8/23-9/22)" if is_cn else "Virgo (Aug 23 - Sep 22)"
    libra = "天秤座 (9/23-10/22)" if is_cn else "Libra (Sep 23 - Oct 22)"
    scorpio = "天蝎座 (10/23-11/21)" if is_cn else "Scorpio (Oct 23 - Nov 21)"
    sag = "射手座 (11/22-12/21)" if is_cn else "Sagittarius (Nov 22 - Dec 21)"
    cap = "摩羯座 (12/22-1/19)" if is_cn else "Capricorn (Dec 22 - Jan 19)"
    aqua = "水瓶座 (1/20-2/18)" if is_cn else "Aquarius (Jan 20 - Feb 18)"
    pisces = "双鱼座 (2/19-3/20)" if is_cn else "Pisces (Feb 19 - Mar 20)"
    
    horoscope_js = 'cn' if is_cn else 'en'
    
    return """      <label for="zodiacSelect">{sel_zodiac}</label>
      <select id="zodiacSelect">
        <option value="aries">{aries}</option><option value="taurus">{taurus}</option>
        <option value="gemini">{gemini}</option><option value="cancer">{cancer}</option>
        <option value="leo">{leo}</option><option value="virgo">{virgo}</option>
        <option value="libra">{libra}</option><option value="scorpio">{scorpio}</option>
        <option value="sagittarius">{sag}</option><option value="capricorn">{cap}</option>
        <option value="aquarius">{aqua}</option><option value="pisces">{pisces}</option>
      </select>
      <button class="btn" id="getHoroscope">{get_btn}</button>
      <div id="horoscopeResult" class="output"></div>
      <script>
      var horoscopes = {{
        en: {{
          aries: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 Passionate energy today', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 Stay focused on priorities', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 High energy levels', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Avoid impulse spending', color:'Red', number:9}},
          taurus: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 Steady and reliable', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 Good for long-term planning', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Watch your diet', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 Stable finances', color:'Green', number:6}},
          gemini: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 Exciting conversations', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 Multitasking required', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Mental rest needed', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Small gains likely', color:'Yellow', number:3}},
          cancer: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 Emotional connections', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 Trust your intuition', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 Self-care day', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Save for rainy day', color:'Silver', number:2}},
          leo: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 Center of attention', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 Leadership opportunity', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 Stay active', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 Generous but wise', color:'Gold', number:1}},
          virgo: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 Practical approach', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 Detail-oriented success', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 Good habits pay off', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Budget review needed', color:'Navy', number:5}},
          libra: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 Harmony and balance', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 Collaborative projects', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 Balanced lifestyle', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Fair deals coming', color:'Pink', number:7}},
          scorpio: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 Deep connections', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 Strategic moves', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Release tension', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 Smart investments', color:'Black', number:8}},
          sagittarius: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 Adventure calls', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 Big picture thinking', health:'\\u2605\\u2605\\u2605\\u2605\\u2605 Peak fitness', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Travel expenses', color:'Purple', number:4}},
          capricorn: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 Slow and steady', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 Ambitious goals', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Posture check', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 Financial growth', color:'Brown', number:10}},
          aquarius: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 Unique connections', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 Innovation wins', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Try new exercise', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Unexpected income', color:'Blue', number:11}},
          pisces: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 Romantic vibes', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 Creative projects', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 Stay grounded', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 Artistic investments', color:'Sea Green', number:12}}
        }},
        cn: {{
          aries: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 今日桃花运势旺盛', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 保持专注，勿分心', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 精力充沛', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 避免冲动消费', color:'红色', number:9}},
          taurus: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 稳定踏实的感情', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 适合长远规划', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 注意饮食', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 财务状况稳定', color:'绿色', number:6}},
          gemini: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 有趣的交流时光', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 需要多任务处理', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 需要精神休息', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 有小额收益', color:'黄色', number:3}},
          cancer: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 情感连接加深', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 相信直觉', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 自我关爱日', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 未雨绸缪', color:'银色', number:2}},
          leo: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 成为全场焦点', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 领导力机会', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 保持运动', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 慷慨但明智', color:'金色', number:1}},
          virgo: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 务实的态度', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 细节决定成功', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 好习惯有回报', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 需要预算审查', color:'藏青', number:5}},
          libra: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 和谐与平衡', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 合作项目顺利', health:'\\u2605\\u2605\\u2605\\u2605\\u2606 平衡的生活方式', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 公平交易来临', color:'粉色', number:7}},
          scorpio: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 深度连接', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 策略性行动', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 释放压力', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 明智投资', color:'黑色', number:8}},
          sagittarius: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 冒险在召唤', career:'\\u2605\\u2605\\u2605\\u2605\\u2606 大局思维', health:'\\u2605\\u2605\\u2605\\u2605\\u2605 体能巅峰', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 旅行开销', color:'紫色', number:4}},
          capricorn: {{love:'\\u2605\\u2605\\u2605\\u2606\\u2606 稳扎稳打', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 雄心勃勃', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 注意坐姿', wealth:'\\u2605\\u2605\\u2605\\u2605\\u2606 财务增长', color:'棕色', number:10}},
          aquarius: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2606 独特的连接', career:'\\u2605\\u2605\\u2605\\u2605\\u2605 创新制胜', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 尝试新运动', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 意外收入', color:'蓝色', number:11}},
          pisces: {{love:'\\u2605\\u2605\\u2605\\u2605\\u2605 浪漫气息', career:'\\u2605\\u2605\\u2605\\u2606\\u2606 创意项目', health:'\\u2605\\u2605\\u2605\\u2606\\u2606 脚踏实地', wealth:'\\u2605\\u2605\\u2605\\u2606\\u2606 艺术投资', color:'海绿', number:12}}
        }}
      }};
      document.getElementById('getHoroscope').addEventListener('click', function() {{
        var sign = document.getElementById('zodiacSelect').value;
        var lang = '{horoscope_js}';
        var h = horoscopes[lang][sign];
        var labels = {{en: {{love:'Love', career:'Career', health:'Health', wealth:'Wealth', color:'Lucky Color', number:'Lucky Number'}}, cn: {{love:'爱情', career:'事业', health:'健康', wealth:'财运', color:'幸运色', number:'幸运数字'}}}};
        var lb = labels[lang];
        var todayTitle = lang === 'en' ? "Today's Horoscope" : '今日运势';
        var html = '<div style="background:#fff;padding:20px;border-radius:8px;border:1px solid #e2e8f0"><h2 style="margin-bottom:16px">' + todayTitle + '</h2>';
        html += '<div style="margin-bottom:8px"><strong>' + lb.love + ':</strong> ' + h.love + '</div>';
        html += '<div style="margin-bottom:8px"><strong>' + lb.career + ':</strong> ' + h.career + '</div>';
        html += '<div style="margin-bottom:8px"><strong>' + lb.health + ':</strong> ' + h.health + '</div>';
        html += '<div style="margin-bottom:8px"><strong>' + lb.wealth + ':</strong> ' + h.wealth + '</div>';
        html += '<div style="margin-bottom:8px"><strong>' + lb.color + ':</strong> <span style="display:inline-block;width:20px;height:20px;border-radius:50%;vertical-align:middle;background:' + h.color.toLowerCase().replace(' ','') + ';border:1px solid #ccc"></span> ' + h.color + '</div>';
        html += '<div><strong>' + lb.number + ':</strong> ' + h.number + '</div></div>';
        document.getElementById('horoscopeResult').innerHTML = html;
      }});
      </script>""".format(sel_zodiac=sel_zodiac, get_btn=get_btn, aries=aries, taurus=taurus,
                       gemini=gemini, cancer=cancer, leo=leo, virgo=virgo,
                       libra=libra, scorpio=scorpio, sag=sag, cap=cap,
                       aqua=aqua, pisces=pisces, horoscope_js=horoscope_js)


def body_blood_type(is_cn):
    your = "您的血型" if is_cn else "Your Blood Type"
    view = "查看信息" if is_cn else "View Info"
    info_title = "血型信息" if is_cn else "Blood Type Info"
    donate_to = "可输血给" if is_cn else "Can Donate To"
    receive_from = "可接受输血" if is_cn else "Can Receive From"
    personality = "性格特征" if is_cn else "Personality"
    global_dist = "全球分布" if is_cn else "Global Distribution"
    univ_donor = "万能献血者" if is_cn else "universal donor"
    all_types = "All types" if not is_cn else "所有类型"
    
    return """      <label for="aboSelect">{your}</label>
      <select id="aboSelect">
        <option value="A+">A+</option><option value="A-">A-</option>
        <option value="B+">B+</option><option value="B-">B-</option>
        <option value="AB+">AB+</option><option value="AB-">AB-</option>
        <option value="O+">O+</option><option value="O-">O-</option>
      </select>
      <button class="btn" id="getInfo">{view}</button>
      <div id="bloodResult" class="output"></div>
      <script>
      var allTypesLabel = '{all_types}';
      var bloodData = {{
        'A+': {{donate:['A+','AB+'], receive:['A+','A-','O+','O-'], personality:'{a_personality}', global:'27%'}},
        'A-': {{donate:['A+','A-','AB+','AB-'], receive:['A-','O-'], personality:'{a_minus_personality}', global:'7%'}},
        'B+': {{donate:['B+','AB+'], receive:['B+','B-','O+','O-'], personality:'{b_personality}', global:'22%'}},
        'B-': {{donate:['B+','B-','AB+','AB-'], receive:['B-','O-'], personality:'{b_minus_personality}', global:'2%'}},
        'AB+': {{donate:['AB+'], receive:[allTypesLabel], personality:'{ab_personality}', global:'5%'}},
        'AB-': {{donate:['AB+','AB-'], receive:['A-','B-','AB-','O-'], personality:'{ab_minus_personality}', global:'1%'}},
        'O+': {{donate:['O+','A+','B+','AB+'], receive:['O+','O-'], personality:'{o_personality}', global:'39%'}},
        'O-': {{donate:[allTypesLabel], receive:['O-'], personality:'{o_minus_personality}', global:'6%'}}
      }};
      document.getElementById('getInfo').addEventListener('click', function() {{
        var type = document.getElementById('aboSelect').value;
        var d = bloodData[type];
        var html = '<div style="background:#fff;padding:20px;border-radius:8px;border:1px solid #e2e8f0"><h3>' + type + ' {info_title}</h3>';
        html += '<p><strong>{donate_to}:</strong> ' + d.donate.join(', ') + '</p>';
        html += '<p><strong>{receive_from}:</strong> ' + d.receive.join(', ') + '</p>';
        html += '<p><strong>{personality}:</strong> ' + d.personality + '</p>';
        html += '<p><strong>{global_dist}:</strong> ' + d.global + '</p></div>';
        document.getElementById('bloodResult').innerHTML = html;
      }});
      </script>""".format(
        your=your, view=view, info_title=info_title,
        donate_to=donate_to, receive_from=receive_from,
        personality=personality, global_dist=global_dist, all_types=all_types,
        a_personality="勤奋、负责、细心" if is_cn else "Diligent, responsible, careful",
        a_minus_personality="冷静、耐心、有条理" if is_cn else "Calm, patient, organized",
        b_personality="有创意、热情、灵活" if is_cn else "Creative, passionate, flexible",
        b_minus_personality="独立、目标导向" if is_cn else "Independent, goal-oriented",
        ab_personality="理性、适应力强、善于交际" if is_cn else "Rational, adaptable, diplomatic",
        ab_minus_personality="神秘、善于分析" if is_cn else "Mysterious, analytical",
        o_personality="自信、领导力强、善于社交" if is_cn else "Confident, leadership, sociable",
        o_minus_personality="大胆、坚定、" + ("万能献血者" if is_cn else "universal donor"),
    )


# 剩余工具实现（body_measurement, fake_news_detector, unit_price_comparison, daily_joke）
# 由于篇幅限制，把这些实现简化为直接嵌入

def body_body_measurement(is_cn):
    h_lbl = "身高 (厘米)" if is_cn else "Height (cm)"
    w_lbl = "体重 (公斤)" if is_cn else "Weight (kg)"
    waist_lbl = "腰围 (厘米)" if is_cn else "Waist (cm)"
    hip_lbl = "臀围 (厘米)" if is_cn else "Hip (cm)"
    gender_lbl = "性别" if is_cn else "Gender"
    male = "男" if is_cn else "Male"
    female = "女" if is_cn else "Female"
    age_lbl = "年龄" if is_cn else "Age"
    calc_all = "全部计算" if is_cn else "Calculate All"
    enter_hw = "请输入身高和体重" if is_cn else "Enter height and weight"
    under = "偏瘦" if is_cn else "Underweight"
    normal = "正常" if is_cn else "Normal"
    over = "超重" if is_cn else "Overweight"
    obese = "肥胖" if is_cn else "Obese"
    high_risk = "高风险" if is_cn else "High Risk"
    normal_risk = "正常" if is_cn else "Normal"
    ideal_w = "理想体重" if is_cn else "Ideal Weight"
    whr_lbl = "腰臀比" if is_cn else "Waist-Hip Ratio"
    bsa_lbl = "体表面积" if is_cn else "Body Surface Area"
    bmr_lbl = "基础代谢率 BMR" if is_cn else "BMR (Basal Metabolic Rate)"
    per_day = "天" if is_cn else "day"
    
    return """      <div class="row">
        <div><label for="height">{h_lbl}</label><input type="number" id="height" placeholder="170" min="50" max="250" step="0.1"></div>
        <div><label for="weight">{w_lbl}</label><input type="number" id="weight" placeholder="65" min="20" max="300" step="0.1"></div>
      </div>
      <div class="row">
        <div><label for="waist">{waist_lbl}</label><input type="number" id="waist" placeholder="80" min="30" max="200" step="0.1"></div>
        <div><label for="hip">{hip_lbl}</label><input type="number" id="hip" placeholder="95" min="30" max="200" step="0.1"></div>
      </div>
      <div class="row">
        <div><label for="gender">{gender_lbl}</label>
          <select id="gender"><option value="male">{male}</option><option value="female">{female}</option></select>
        </div>
        <div><label for="age">{age_lbl}</label><input type="number" id="age" placeholder="25" min="1" max="120"></div>
      </div>
      <button class="btn" id="calcBtn">{calc_all}</button>
      <div id="bodyResult" class="output"></div>
      <script>
      document.getElementById('calcBtn').addEventListener('click', function() {{
        var h = parseFloat(document.getElementById('height').value);
        var w = parseFloat(document.getElementById('weight').value);
        var waist = parseFloat(document.getElementById('waist').value);
        var hip = parseFloat(document.getElementById('hip').value);
        var gender = document.getElementById('gender').value;
        var age = parseInt(document.getElementById('age').value);
        if (!h || !w) {{ showToast('{enter_hw}'); return; }}
        var bmi = w / ((h/100) * (h/100));
        var bmiCat = bmi < 18.5 ? '{under}' : bmi < 24 ? '{normal}' : bmi < 28 ? '{over}' : '{obese}';
        var idealW = gender === 'male' ? (h - 100) * 0.9 : (h - 100) * 0.85;
        var whr = waist && hip ? waist / hip : null;
        var whrRisk = '';
        if (whr) {{ whrRisk = (gender === 'male' ? (whr > 0.9 ? '{high_risk}' : '{normal_risk}') : (whr > 0.85 ? '{high_risk}' : '{normal_risk}')); }}
        var bsa = Math.sqrt((h * w) / 3600);
        var bmr = gender === 'male' ? (10 * w + 6.25 * h - 5 * age + 5) : (10 * w + 6.25 * h - 5 * age - 161);
        var html = '<div style="background:#fff;padding:20px;border-radius:8px;border:1px solid #e2e8f0">';
        html += '<div class="result-item"><strong>BMI:</strong> ' + bmi.toFixed(1) + ' (' + bmiCat + ')</div>';
        html += '<div class="result-item"><strong>{ideal_w}:</strong> ' + idealW.toFixed(1) + ' kg</div>';
        if (whr) html += '<div class="result-item"><strong>{whr_lbl}:</strong> ' + whr.toFixed(2) + ' (' + whrRisk + ')</div>';
        html += '<div class="result-item"><strong>{bsa_lbl}:</strong> ' + bsa.toFixed(2) + ' m\\u00b2</div>';
        html += '<div class="result-item"><strong>{bmr_lbl}:</strong> ' + Math.round(bmr) + ' kcal/{per_day}</div>';
        html += '</div>';
        document.getElementById('bodyResult').innerHTML = html;
      }});
      </script>""".format(h_lbl=h_lbl, w_lbl=w_lbl, waist_lbl=waist_lbl, hip_lbl=hip_lbl,
                       gender_lbl=gender_lbl, male=male, female=female, age_lbl=age_lbl,
                       calc_all=calc_all, enter_hw=enter_hw, under=under, normal=normal,
                       over=over, obese=obese, high_risk=high_risk, normal_risk=normal_risk,
                       ideal_w=ideal_w, whr_lbl=whr_lbl, bsa_lbl=bsa_lbl, bmr_lbl=bmr_lbl, per_day=per_day)


def body_fake_news(is_cn):
    title_lbl = "文章标题" if is_cn else "Article Title"
    title_ph = "输入新闻标题..." if is_cn else "Enter the news headline..."
    content_lbl = "文章内容" if is_cn else "Article Content"
    content_ph = "粘贴文章正文进行分析..." if is_cn else "Paste the article text to analyze..."
    analyze_btn = "开始分析" if is_cn else "Analyze"
    enter_text = "请输入要分析的文本" if is_cn else "Enter text to analyze"
    result_title = "分析结果" if is_cn else "Analysis Result"
    high_risk = "高风险" if is_cn else "HIGH RISK"
    med_risk = "中等风险" if is_cn else "MEDIUM RISK"
    low_risk = "低风险" if is_cn else "LOW RISK"
    risk_score = "风险分数" if is_cn else "Risk Score"
    sens_words = "发现夸张用词" if is_cn else "Sensational Words Found"
    emo_words = "情感操纵词汇" if is_cn else "Emotional Manipulation"
    none = "无" if is_cn else "None"
    word_count = "字数" if is_cn else "Word Count"
    caps_ratio = "大写比例" if is_cn else "Capitalization Ratio"
    excl = "感叹号" if is_cn else "Exclamation Marks"
    disclaimer = "⚠️ 本工具检测语言特征模式，不能替代事实核查。请始终以权威来源核实。" if is_cn else "⚠️ This tool detects linguistic patterns, not factual accuracy. Always verify with trusted sources."
    
    return """      <label for="articleTitle">{title_lbl}</label>
      <input type="text" id="articleTitle" placeholder="{title_ph}">
      <label for="articleContent">{content_lbl}</label>
      <textarea id="articleContent" placeholder="{content_ph}"></textarea>
      <button class="btn" id="analyzeBtn">{analyze_btn}</button>
      <div id="detectorResult" class="output"></div>
      <script>
      var sensationalWords = {{en: ['shocking','unbelievable','you won\\'t believe','doctors hate','what happens next','secret they don\\'t want you to know','miracle','cure','conspiracy','wake up','they are hiding','this changes everything','mind-blowing','jaw-dropping','bombshell'], cn: ['震惊','难以置信','你绝对想不到','医生都不会告诉你','惊天秘密','内幕','奇迹','灵丹妙药','阴谋','觉醒','他们在隐瞒','颠覆认知','惊人发现','触目惊心','劲爆']}};
      var emotionalWords = {{en: ['outrage','disgusting','horrifying','terrifying','devastating','heartbreaking','infuriating','panic','fear','hate'], cn: ['愤怒','恶心','恐怖','毁灭性','令人心碎','令人发指','恐慌','恐惧','憎恨','痛心']}};
      document.getElementById('analyzeBtn').addEventListener('click', function() {{
        var title = document.getElementById('articleTitle').value;
        var content = document.getElementById('articleContent').value;
        var text = (title + ' ' + content).toLowerCase();
        if (!text.trim()) {{ showToast('{enter_text}'); return; }}
        var lang = '{lang_js}';
        var sw = sensationalWords[lang];
        var ew = emotionalWords[lang];
        var sensationalCount = 0, emotionalCount = 0, foundSens = [], foundEmo = [];
        sw.forEach(function(w) {{ var re = new RegExp(w.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'), 'gi'); var matches = text.match(re); if (matches) {{ sensationalCount += matches.length; foundSens.push(w); }} }});
        ew.forEach(function(w) {{ var re = new RegExp(w.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'), 'gi'); var matches = text.match(re); if (matches) {{ emotionalCount += matches.length; foundEmo.push(w); }} }});
        var wordCount = text.split(/\\s+/).filter(Boolean).length;
        var capsRatio = (text.match(/[A-Z]/g) || []).length / Math.max(text.length, 1);
        var exclCount = (text.match(/!/g) || []).length;
        var questionCount = (text.match(/\\?/g) || []).length;
        var riskScore = 0;
        if (sensationalCount > 2) riskScore += 30; else if (sensationalCount > 0) riskScore += 15;
        if (emotionalCount > 3) riskScore += 25; else if (emotionalCount > 0) riskScore += 10;
        if (capsRatio > 0.3) riskScore += 15;
        if (exclCount > 3) riskScore += 10;
        if (questionCount > 5) riskScore += 10;
        var level = riskScore >= 60 ? '{high_risk} \\ud83d\\udd34' : riskScore >= 30 ? '{med_risk} \\ud83d\\udfe1' : '{low_risk} \\ud83d\\udfe2';
        var html = '<div style="background:#fff;padding:20px;border-radius:8px;border:1px solid #e2e8f0"><h3>{result_title}: ' + level + '</h3>';
        html += '<p><strong>{risk_score}:</strong> ' + riskScore + '/100</p>';
        html += '<p><strong>{sens_words}:</strong> ' + (foundSens.length ? [...new Set(foundSens)].join(', ') : '{none}') + '</p>';
        html += '<p><strong>{emo_words}:</strong> ' + (foundEmo.length ? [...new Set(foundEmo)].join(', ') : '{none}') + '</p>';
        html += '<p><strong>{word_count}:</strong> ' + wordCount + '</p>';
        html += '<p><strong>{caps_ratio}:</strong> ' + (capsRatio*100).toFixed(1) + '%</p>';
        html += '<p><strong>{excl}:</strong> ' + exclCount + '</p>';
        html += '<p style="margin-top:12px;color:#64748b;font-size:.85rem">{disclaimer}</p></div>';
        document.getElementById('detectorResult').innerHTML = html;
      }});
      </script>""".format(
        title_lbl=title_lbl, title_ph=title_ph, content_lbl=content_lbl, content_ph=content_ph,
        analyze_btn=analyze_btn, enter_text=enter_text, result_title=result_title,
        high_risk=high_risk, med_risk=med_risk, low_risk=low_risk,
        risk_score=risk_score, sens_words=sens_words, emo_words=emo_words,
        none=none, word_count=word_count, caps_ratio=caps_ratio, excl=excl,
        disclaimer=disclaimer, lang_js="cn" if is_cn else "en"
    )


def body_unit_price(is_cn):
    item1 = "商品 1" if is_cn else "Item 1"
    item2 = "商品 2" if is_cn else "Item 2"
    price_lbl = "价格" if is_cn else "Price"
    amount_lbl = "数量" if is_cn else "Amount"
    unit_lbl = "单位" if is_cn else "Unit"
    g = "克" if is_cn else "g"
    ml = "毫升" if is_cn else "ml"
    pcs = "个" if is_cn else "pcs"
    m = "米" if is_cn else "m"
    L = "升" if is_cn else "L"
    compare_btn = "对比" if is_cn else "Compare"
    fill_all = "请填写所有字段" if is_cn else "Fill all fields"
    unit_price = "单价" if is_cn else "Unit Price"
    yuan_per = "元/" if is_cn else "yuan/"
    cheaper = "更划算！" if is_cn else " is cheaper!"
    saving = "每单位节省" if is_cn else "saving"
    you_save = "节省约 " if is_cn else "You save "
    
    return """      <label>{item1}</label>
      <div class="row">
        <div><label for="price1">{price_lbl} ({yuan_per})</label><input type="number" id="price1" placeholder="15.9" step="0.01"></div>
        <div><label for="amount1">{amount_lbl}</label><input type="number" id="amount1" placeholder="500" step="0.1"></div>
        <div><label for="unit1">{unit_lbl}</label>
          <select id="unit1"><option value="g">{g}</option><option value="ml">{ml}</option><option value="pcs">{pcs}</option><option value="m">{m}</option><option value="L">{L}</option></select>
        </div>
      </div>
      <label style="margin-top:16px">{item2}</label>
      <div class="row">
        <div><label for="price2">{price_lbl} ({yuan_per})</label><input type="number" id="price2" placeholder="25.9" step="0.01"></div>
        <div><label for="amount2">{amount_lbl}</label><input type="number" id="amount2" placeholder="1000" step="0.1"></div>
        <div><label for="unit2">{unit_lbl}</label>
          <select id="unit2"><option value="g">{g}</option><option value="ml">{ml}</option><option value="pcs">{pcs}</option><option value="m">{m}</option><option value="L">{L}</option></select>
        </div>
      </div>
      <button class="btn" id="compareBtn" style="margin-top:16px">{compare_btn}</button>
      <div id="compareResult" class="output"></div>
      <script>
      document.getElementById('compareBtn').addEventListener('click', function() {{
        var p1 = parseFloat(document.getElementById('price1').value);
        var a1 = parseFloat(document.getElementById('amount1').value);
        var u1 = document.getElementById('unit1').value;
        var p2 = parseFloat(document.getElementById('price2').value);
        var a2 = parseFloat(document.getElementById('amount2').value);
        var u2 = document.getElementById('unit2').value;
        if (!p1 || !a1 || !p2 || !a2) {{ showToast('{fill_all}'); return; }}
        var up1 = p1 / a1;
        var up2 = p2 / a2;
        var cheaperIdx = up1 < up2 ? 1 : 2;
        var savings = Math.abs(up1 - up2);
        var html = '<div style="background:#fff;padding:20px;border-radius:8px;border:1px solid #e2e8f0">';
        html += '<div class="result-item"><strong>{item1} {unit_price}:</strong> ' + up1.toFixed(4) + ' {yuan_per}' + u1 + '</div>';
        html += '<div class="result-item"><strong>{item2} {unit_price}:</strong> ' + up2.toFixed(4) + ' {yuan_per}' + u2 + '</div>';
        html += '<div class="result-item" style="background:#ecfdf5;border:1px solid #a7f3d0"><strong>\\u2705 ' + ('Item ' if lang==='en' else '商品') + cheaperIdx + '{cheaper}</strong> {saving} ' + savings.toFixed(4) + ' {yuan_per}' + u1 + '</div>';
        var pctSave = (savings / Math.max(up1, up2) * 100);
        html += '<p style="margin-top:8px;color:#64748b">{you_save}' + pctSave.toFixed(1) + '%</p></div>';
        document.getElementById('compareResult').innerHTML = html;
      }});
      var lang = '{lang_js}';
      </script>""".format(
        item1=item1, item2=item2, price_lbl=price_lbl, amount_lbl=amount_lbl,
        unit_lbl=unit_lbl, g=g, ml=ml, pcs=pcs, m=m, L=L,
        compare_btn=compare_btn, fill_all=fill_all, unit_price=unit_price,
        yuan_per=yuan_per, cheaper=cheaper, saving=saving, you_save=you_save,
        lang_js="en" if not is_cn else "cn"
    )


def body_daily_joke(is_cn):
    get_btn = "随机获取笑话" if is_cn else "Get Random Joke"
    copy_btn = "复制" if is_cn else "Copy"
    
    jokes_en = json.dumps([
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What's orange and sounds like a parrot? A carrot!",
        "How does a penguin build its house? Igloos it together!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a sleeping bull? A bulldozer!",
        "I used to play piano by ear, but now I use my hands.",
        "What did the left eye say to the right eye? Between you and me, something smells.",
        "Why was the math book sad? It had too many problems.",
        "What's a skeleton's favorite instrument? The trom-bone!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "I'm on a seafood diet. I see food and I eat it.",
        "What do you call a fish with no eyes? Fsh.",
        "Why did the cookie go to the doctor? Because it was feeling crumbly.",
        "I told my computer I needed a break, now it won't stop sending me vacation ads."
    ], ensure_ascii=False)
    
    jokes_cn = json.dumps([
        "为什么程序员总是搞混圣诞节和万圣节？因为 Oct 31 == Dec 25！",
        "小明：老师，我昨天看到一个成语叫「愚公移山」，为什么不是「愚公移山」呢？老师：那是愚公，不是愚公。",
        "面试官：「你有什么特长？」我：「我特别能熬夜。」面试官：「还有呢？」我：「我特别能吃。」",
        "为什么数学书总是很忧郁？因为它有太多问题。",
        "世界上什么东西最硬？女朋友的「我没事」。",
        "程序员最讨厌的数字是什么？1024。因为1024=1K，然后他就失去了工作。",
        "为什么蜗牛看起来不太高兴？因为它背上的房子贷款利率太高了。",
        "问：如何让程序员发疯？答：给他一个没有错误信息的bug。",
        "我今天去了图书馆，问管理员：「有关于偏执症的书吗？」管理员小声说：「在你身后。」",
        "两个饺子结婚了，洞房花烛夜，新郎发现新娘是肉馅的，崩溃大哭：「你不是说你是素的吗？」",
        "医生：「你的检查结果出来了，很不幸，你只有6个月的时间了。」病人：「医生，那我现在应该做什么？」医生：「我建议你嫁给一个税务师。」病人：「这样能治好我的病吗？」医生：「不能，但会让那6个月感觉像永远。」",
        "老板：「你明天不用来上班了。」我：「为什么？」老板：「你昨天在会议上睡着了。」我：「这不能怪我，是你在讲PPT的时候催眠效果太好了。」",
        "我减肥的方法很简单：每天照镜子，然后对自己说「你不胖」，然后就真的…还是胖。",
        "为什么程序员不喜欢户外活动？因为阳光太亮了，没法看清黑色主题的屏幕。",
        "问：什么样的水不能喝？答：薪水。",
        "我今天买了一个充电宝，很大很重，结果发现里面全是电池。我在想，如果我把电池都拿出来，那它是不是就变成了一个……空壳？",
        "老板：「你不是说你会Python吗？」我：「对啊，我会写print('Hello World')」老板：「就这？」我：「我还会写input()让程序停下来。」",
        "今天去相亲，对方问我：「你有什么爱好？」我说：「我喜欢安静。」对方：「那正好，我也不爱说话。」然后我们就安静地坐了一个小时，最后她说：「我们不太合适。」",
        "小明问爸爸：「为什么我们要给奶奶过生日，她却总说不用不用？」爸爸：「等你长大了就懂了。比如我给你买生日礼物的时候，你也会说不用不用。」小明：「那不一样！我说不用是真的不用！」",
        "面试官：「你期望的薪资是多少？」我：「五万。」面试官：「一个月？」我：「不，一年。」面试官：「……」我：「怎么了？太高了吗？」面试官：「不是，你走吧，我们公司配不上你。」"
    ], ensure_ascii=False)
    
    jokes_data = jokes_cn if is_cn else jokes_en
    
    return """      <button class="btn" id="getJoke">{get_btn}</button>
      <button class="btn btn-secondary" id="copyJoke" style="margin-left:8px">{copy_btn}</button>
      <div id="jokeDisplay" class="output" style="font-size:1.1rem;line-height:1.8"></div>
      <script>
      var jokes = {jokes};
      function getJoke() {{
        var joke = jokes[Math.floor(Math.random() * jokes.length)];
        document.getElementById('jokeDisplay').textContent = joke;
        return joke;
      }}
      document.getElementById('getJoke').addEventListener('click', getJoke);
      document.getElementById('copyJoke').addEventListener('click', function() {{
        var joke = document.getElementById('jokeDisplay').textContent;
        if (!joke) joke = getJoke();
        copyText(joke);
      }});
      getJoke();
      </script>""".format(get_btn=get_btn, copy_btn=copy_btn, jokes=jokes_data)


# ===== 主流程 =====
body_funcs = {
    "meme-text-generator": body_meme_text,
    "image-resize-bulk": body_image_resize_bulk,
    "csv-to-html": body_csv_to_html,
    "smart-rename": body_smart_rename,
    "daily-horoscope": body_daily_horoscope,
    "blood-type": body_blood_type,
    "body-measurement": body_body_measurement,
    "fake-news-detector": body_fake_news,
    "unit-price-comparison": body_unit_price,
    "daily-joke": body_daily_joke,
}

tools = [
    {"slug":"meme-text-generator","cn_name":"梗图文字生成器","en_name":"Meme Text Generator","cn_desc":"在线梗图文字生成器，经典Impact字体，可调整文字位置、大小和颜色","en_desc":"Free online meme text generator with classic Impact font. Adjust text position, size, and color","cn_short":"经典梗图文字生成，支持上下双行文字，自定义字体颜色和大小","en_short":"Classic meme text generator with top/bottom text, custom color & size","category":"fun-tools","cn_kw":"梗图,文字生成,表情包,meme,Impact字体","en_kw":"meme,text generator,meme maker,Impact font,funny image"},
    {"slug":"image-resize-bulk","cn_name":"批量图片缩放","en_name":"Bulk Image Resizer","cn_desc":"在线批量图片缩放工具，支持多图同时处理，可设定目标宽度/高度，纯前端处理","en_desc":"Free online bulk image resizer. Resize multiple images at once, set target width/height, 100% client-side","cn_short":"批量调整图片尺寸，支持百分比/固定像素缩放，纯前端不泄露隐私","en_short":"Resize multiple images at once, percentage or pixel scaling, private & client-side","category":"image-tools","cn_kw":"图片缩放,批量,resize,压缩,图片处理","en_kw":"image resize,bulk,compress,image processing"},
    {"slug":"csv-to-html","cn_name":"CSV转HTML表格","en_name":"CSV to HTML Table","cn_desc":"在线CSV转HTML表格工具，粘贴CSV数据一键生成HTML表格代码，支持自定义样式","en_desc":"Free online CSV to HTML table converter. Paste CSV data and generate HTML table code instantly","cn_short":"CSV数据一键转HTML表格代码，支持表头识别和自定义样式","en_short":"Convert CSV data to HTML table code, header detection & custom styles","category":"dev-tools","cn_kw":"CSV,HTML,表格,转换,代码生成","en_kw":"CSV,HTML,table,convert,code generator"},
    {"slug":"smart-rename","cn_name":"智能重命名工具","en_name":"Smart Rename Tool","cn_desc":"在线智能重命名工具，批量添加前缀/后缀、替换文本、大小写转换、序号格式化","en_desc":"Free online smart rename tool. Batch add prefix/suffix, replace text, case conversion, number formatting","cn_short":"批量智能重命名：前缀后缀、替换文本、大小写转换、数字序号","en_short":"Batch smart rename: prefix/suffix, text replace, case convert, numbering","category":"utility-tools","cn_kw":"重命名,批量,文件名,前缀,后缀,序号","en_kw":"rename,batch,filename,prefix,suffix,numbering"},
    {"slug":"daily-horoscope","cn_name":"每日星座运势","en_name":"Daily Horoscope","cn_desc":"在线每日星座运势查询，12星座今日运势、幸运色、幸运数字、爱情事业健康运程","en_desc":"Free daily horoscope for all 12 zodiac signs. Today fortune, lucky color, lucky number, love career health","cn_short":"12星座每日运势查询：爱情、事业、健康、财运、幸运色、幸运数字","en_short":"12 zodiac daily horoscope: love, career, health, wealth, lucky color & number","category":"fun-tools","cn_kw":"星座,运势,horoscope,占星,每日运势","en_kw":"horoscope,zodiac,daily,astrology,fortune"},
    {"slug":"blood-type","cn_name":"血型信息查询","en_name":"Blood Type Info","cn_desc":"在线血型信息查询工具，ABO/Rh血型系统，血型遗传规律、输血兼容性、性格特征","en_desc":"Free blood type information tool. ABO/Rh systems, inheritance patterns, transfusion compatibility, personality traits","cn_short":"ABO/Rh血型查询：遗传规律、输血兼容、性格特征、全球分布","en_short":"ABO/Rh blood type: inheritance, compatibility, personality, global distribution","category":"health-tools","cn_kw":"血型,ABO,Rh,输血,遗传,性格","en_kw":"blood type,ABO,Rh,transfusion,inheritance,personality"},
    {"slug":"body-measurement","cn_name":"身体测量计算器","en_name":"Body Measurement Calculator","cn_desc":"在线身体测量工具，BMI计算、腰臀比、理想体重、体表面积、基础代谢率BMR","en_desc":"Free body measurement calculator. BMI, waist-hip ratio, ideal weight, body surface area, BMR","cn_short":"BMI、腰臀比、理想体重、体表面积、基础代谢率一站式计算","en_short":"BMI, waist-hip ratio, ideal weight, BSA, BMR all-in-one calculator","category":"health-tools","cn_kw":"BMI,身体测量,腰臀比,理想体重,代谢率","en_kw":"BMI,body measurement,waist-hip ratio,ideal weight,BMR"},
    {"slug":"fake-news-detector","cn_name":"假新闻特征检测","en_name":"Fake News Detector","cn_desc":"在线假新闻特征检测工具，分析文章标题和内容，检测夸张用词、情感操纵、来源可疑等特征","en_desc":"Free fake news detection tool. Analyze headlines & content for sensationalism, emotional manipulation, suspicious sources","cn_short":"检测文章假新闻特征：夸张用词、情感操纵、信息缺失、来源分析","en_short":"Detect fake news traits: sensationalism, emotional manipulation, source analysis","category":"utility-tools","cn_kw":"假新闻,事实核查,检测,媒体素养","en_kw":"fake news,fact check,detection,media literacy"},
    {"slug":"unit-price-comparison","cn_name":"单价对比计算器","en_name":"Unit Price Comparator","cn_desc":"在线单价对比工具，比较不同包装商品的单位价格（元/克、元/毫升等），助你做出最优购物决策","en_desc":"Free unit price comparison tool. Compare price per unit across different package sizes for smart shopping","cn_short":"超市比价神器：不同规格商品单位价格对比，一眼看出哪个最划算","en_short":"Shopping comparison: unit price across sizes, instantly see the best deal","category":"finance-tools","cn_kw":"单价,比价,超市,购物,省钱","en_kw":"unit price,comparison,shopping,save money"},
    {"slug":"daily-joke","cn_name":"每日笑话","en_name":"Daily Joke","cn_desc":"在线每日笑话生成器，收录大量中英文笑话，分类浏览，一键复制分享，每天笑一笑","en_desc":"Free daily joke generator with a large collection of jokes. Browse by category, one-click copy & share","cn_short":"每日精选笑话：冷笑话、段子、幽默故事，一键复制分享给朋友","en_short":"Daily curated jokes: puns, one-liners, funny stories, copy & share","category":"fun-tools","cn_kw":"笑话,段子,幽默,每日,搞笑","en_kw":"joke,daily,funny,humor,pun"},
]

count = 0
for tool in tools:
    slug = tool["slug"]
    body_func = body_funcs[slug]
    
    # CN
    cn_body = body_func(is_cn=True)
    cn_page = gen_page(tool, "cn", cn_body)
    cn_path = os.path.join(BASE, slug, "index.html")
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn_page)
    print(f"✅ CN: {slug}/index.html")
    
    # EN
    en_body = body_func(is_cn=False)
    en_page = gen_page(tool, "en", en_body)
    en_path = os.path.join(BASE, "en", slug, "index.html")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_page)
    print(f"✅ EN: en/{slug}/index.html")
    count += 1

print(f"\\n🎉 完成！生成 {count} 个工具（20个页面）")
