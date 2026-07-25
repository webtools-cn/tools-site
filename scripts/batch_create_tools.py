#!/usr/bin/env python3
"""批量创建4个新工具的中英文版"""
import os

tools = [
    {
        "slug": "polygon-area-calculator",
        "name_cn": "多边形面积计算器",
        "name_en": "Polygon Area Calculator",
        "desc_cn": "免费在线多边形面积计算器，输入顶点坐标自动计算任意多边形面积。支持三角形、四边形、五边形、六边形，可视化图形展示。",
        "desc_en": "Free online polygon area calculator. Enter vertex coordinates to auto-calculate polygon area. Supports triangles, quadrilaterals, pentagons, hexagons with visual diagram.",
        "icon_cn": "📐",
        "icon_en": "📐",
        "cat": "math-tools",
        "primary": "#10B981",
    },
    {
        "slug": "typing-race",
        "name_cn": "打字竞速",
        "name_en": "Typing Race",
        "desc_cn": "免费在线打字竞速游戏，随机生成段落，实时显示WPM和准确率。挑战自己的打字速度极限，适合打字练习和测试。",
        "desc_en": "Free online typing race game. Random paragraphs with real-time WPM and accuracy display. Challenge your typing speed limit. Perfect for practice and testing.",
        "icon_cn": "⌨️",
        "icon_en": "⌨️",
        "cat": "utility-tools",
        "primary": "#F59E0B",
    },
    {
        "slug": "mouse-click-counter",
        "name_cn": "鼠标点击计数器",
        "name_en": "Mouse Click Counter",
        "desc_cn": "免费在线鼠标点击计数器，统计左键/右键/中键点击次数、CPS点击速度、总点击数。支持计时模式和无限模式。",
        "desc_en": "Free online mouse click counter. Track left/right/middle clicks, CPS click speed, total clicks. Supports timed mode and unlimited mode.",
        "icon_cn": "🖱️",
        "icon_en": "🖱️",
        "cat": "utility-tools",
        "primary": "#EF4444",
    },
    {
        "slug": "favicon-from-text",
        "name_cn": "文字生成Favicon",
        "name_en": "Text to Favicon",
        "desc_cn": "免费在线文字生成Favicon工具，输入文字自动生成网站图标。支持自定义字体颜色、背景色、圆角，一键下载ICO/PNG/SVG。",
        "desc_en": "Free online text to favicon generator. Input text to auto-generate website icons. Customize font color, background color, border radius. Download as ICO/PNG/SVG.",
        "icon_cn": "🖼️",
        "icon_en": "🖼️",
        "cat": "design-tools",
        "primary": "#8B5CF6",
    },
]

BASE = "/home/chison/tools-site"

for tool in tools:
    slug = tool["slug"]
    
    # CN template
    cn_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tool['name_cn']} - 免费在线工具 | Free ToolBase</title>
  <meta name="description" content="{tool['desc_cn'][:160]}">
  <meta property="og:title" content="{tool['name_cn']} - 免费在线工具">
  <meta property="og:description" content="{tool['desc_cn'][:160]}">
  <meta property="og:type" content="website">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool['name_cn']}","description":"{tool['desc_cn'][:160]}","applicationCategory":"WebApplication","operatingSystem":"Web"}}</script>
  <style>
    :root {{ --primary: {tool['primary']}; --bg: #f8fafc; --card: #fff; --text: #1e293b; --text2: #64748b; --radius: 12px; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; display: flex; flex-direction: column; }}
    header {{ background: var(--card); padding: 16px 24px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 12px; }}
    header a {{ text-decoration: none; color: var(--primary); font-weight: 700; font-size: 18px; }}
    main {{ flex: 1; max-width: 720px; margin: 0 auto; padding: 40px 20px; width: 100%; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .subtitle {{ color: var(--text2); margin-bottom: 32px; font-size: 15px; }}
    .card {{ background: var(--card); border-radius: var(--radius); padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 20px; }}
    .card h2 {{ font-size: 18px; margin-bottom: 12px; }}
    .input-group {{ display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }}
    input, textarea, select {{ padding: 10px 14px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-family: inherit; }}
    input:focus, textarea:focus, select:focus {{ border-color: var(--primary); outline: none; }}
    textarea {{ width: 100%; min-height: 120px; resize: vertical; }}
    button {{ padding: 10px 20px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }}
    .btn-primary {{ background: var(--primary); color: #fff; }}
    .btn-primary:hover {{ opacity: 0.9; }}
    .btn-secondary {{ background: #e2e8f0; color: var(--text); }}
    .result {{ margin-top: 16px; padding: 16px; background: #f1f5f9; border-radius: 8px; font-family: monospace; font-size: 14px; white-space: pre-wrap; word-break: break-all; min-height: 40px; }}
    .stat-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }}
    .stat {{ flex: 1; min-width: 100px; text-align: center; padding: 12px; background: #f1f5f9; border-radius: 8px; }}
    .stat-value {{ font-size: 28px; font-weight: 800; color: var(--primary); }}
    .stat-label {{ font-size: 12px; color: var(--text2); margin-top: 4px; }}
    canvas {{ max-width: 100%; border-radius: 8px; }}
    footer {{ text-align: center; padding: 20px; color: var(--text2); font-size: 13px; border-top: 1px solid #e2e8f0; background: var(--card); }}
    footer a {{ color: var(--primary); text-decoration: none; }}
    .toast {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1e293b; color: #fff; padding: 12px 24px; border-radius: 8px; font-size: 14px; opacity: 0; transition: opacity 0.3s; z-index: 1000; pointer-events: none; }}
    .toast.show {{ opacity: 1; }}
    @media (max-width: 480px) {{ h1 {{ font-size: 22px; }} .stat-value {{ font-size: 22px; }} }}
  </style>
</head>
<body>
<header><a href="/">⚒ Free ToolBase</a><span style="color:#94a3b8;">/</span><span>{tool['name_cn']}</span></header>
<main>
  <h1>{tool['icon_cn']} {tool['name_cn']}</h1>
  <p class="subtitle">{tool['desc_cn'][:120]}</p>
  <div class="card" id="toolArea">
    <p style="color:var(--text2);text-align:center;">正在加载工具...</p>
  </div>
</main>
<footer>&copy; 2024 <a href="/">Free ToolBase</a> · 所有工具免费使用</footer>
<div class="toast" id="toast"></div>
<script src="app.js"></script>
</body>
</html>"""

    # EN template  
    en_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tool['name_en']} - Free Online Tool | Free ToolBase</title>
  <meta name="description" content="{tool['desc_en'][:160]}">
  <meta property="og:title" content="{tool['name_en']} - Free Online Tool">
  <meta property="og:description" content="{tool['desc_en'][:160]}">
  <meta property="og:type" content="website">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool['name_en']}","description":"{tool['desc_en'][:160]}","applicationCategory":"WebApplication","operatingSystem":"Web"}}</script>
  <style>
    :root {{ --primary: {tool['primary']}; --bg: #f8fafc; --card: #fff; --text: #1e293b; --text2: #64748b; --radius: 12px; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; display: flex; flex-direction: column; }}
    header {{ background: var(--card); padding: 16px 24px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 12px; }}
    header a {{ text-decoration: none; color: var(--primary); font-weight: 700; font-size: 18px; }}
    main {{ flex: 1; max-width: 720px; margin: 0 auto; padding: 40px 20px; width: 100%; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .subtitle {{ color: var(--text2); margin-bottom: 32px; font-size: 15px; }}
    .card {{ background: var(--card); border-radius: var(--radius); padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 20px; }}
    .card h2 {{ font-size: 18px; margin-bottom: 12px; }}
    .input-group {{ display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }}
    input, textarea, select {{ padding: 10px 14px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-family: inherit; }}
    input:focus, textarea:focus, select:focus {{ border-color: var(--primary); outline: none; }}
    textarea {{ width: 100%; min-height: 120px; resize: vertical; }}
    button {{ padding: 10px 20px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }}
    .btn-primary {{ background: var(--primary); color: #fff; }}
    .btn-primary:hover {{ opacity: 0.9; }}
    .btn-secondary {{ background: #e2e8f0; color: var(--text); }}
    .result {{ margin-top: 16px; padding: 16px; background: #f1f5f9; border-radius: 8px; font-family: monospace; font-size: 14px; white-space: pre-wrap; word-break: break-all; min-height: 40px; }}
    .stat-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }}
    .stat {{ flex: 1; min-width: 100px; text-align: center; padding: 12px; background: #f1f5f9; border-radius: 8px; }}
    .stat-value {{ font-size: 28px; font-weight: 800; color: var(--primary); }}
    .stat-label {{ font-size: 12px; color: var(--text2); margin-top: 4px; }}
    canvas {{ max-width: 100%; border-radius: 8px; }}
    footer {{ text-align: center; padding: 20px; color: var(--text2); font-size: 13px; border-top: 1px solid #e2e8f0; background: var(--card); }}
    footer a {{ color: var(--primary); text-decoration: none; }}
    .toast {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1e293b; color: #fff; padding: 12px 24px; border-radius: 8px; font-size: 14px; opacity: 0; transition: opacity 0.3s; z-index: 1000; pointer-events: none; }}
    .toast.show {{ opacity: 1; }}
    @media (max-width: 480px) {{ h1 {{ font-size: 22px; }} .stat-value {{ font-size: 22px; }} }}
  </style>
</head>
<body>
<header><a href="/en/">⚒ Free ToolBase</a><span style="color:#94a3b8;">/</span><span>{tool['name_en']}</span></header>
<main>
  <h1>{tool['icon_en']} {tool['name_en']}</h1>
  <p class="subtitle">{tool['desc_en'][:120]}</p>
  <div class="card" id="toolArea">
    <p style="color:var(--text2);text-align:center;">Loading tool...</p>
  </div>
</main>
<footer>&copy; 2024 <a href="/en/">Free ToolBase</a> · All tools free to use</footer>
<div class="toast" id="toast"></div>
<script src="app.js"></script>
</body>
</html>"""

    cn_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, "en", slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    with open(os.path.join(cn_dir, "index.html"), "w") as f:
        f.write(cn_html)
    with open(os.path.join(en_dir, "index.html"), "w") as f:
        f.write(en_html)
    
    print(f"Created: {slug} (CN + EN)")

print("Done!")
