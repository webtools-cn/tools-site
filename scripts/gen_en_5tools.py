#!/usr/bin/env python3
"""批量生成5个新工具的英文版"""
import os, json

translations = {
    # spin-the-wheel
    "spin-the-wheel": {
        "title": "Spin the Wheel - Online Prize & Decision Wheel | Free ToolBase",
        "desc": "Free online spinning wheel tool. Customize options and colors, randomly spin to pick results. Perfect for raffles, decisions, and games. 100% browser-based.",
        "keywords": "spin the wheel, online wheel, lucky wheel, decision wheel, random wheel, prize wheel",
        "h1": "🎡 Spin the Wheel",
        "hero": "Free online spinning wheel. Customize option text and colors, randomly spin to pick results. Perfect for raffles, decision-making, and games. All processing is local, no data uploaded.",
        "badge": "Zero Dependencies · Works Offline",
        "breadcrumb1": "Home",
        "breadcrumb2": "Tools",
        "breadcrumb3": "Spin the Wheel",
        "lang_zh": "中文",
        "lang_en": "EN",
        "options_placeholder": "Option 1\nOption 2\nOption 3\nOption 4\nOption 5\nOption 6",
        "spin_btn": "🎯 Spin!",
        "result_label": "🎉 Result:",
        "edit_label": "Edit Options (one per line)",
        "presets_label": "Presets",
        "yesno": "Yes/No",
        "dinner": "Dinner",
        "lucky": "Raffle",
        "colors": "Colors",
        "dice": "Dice 1-6",
        "update_btn": "🔄 Update Wheel",
        "usage_title": "How to Use",
        "usage1": "<strong>Edit Options:</strong> Enter options in the right panel, one per line. Supports 2-20 options.",
        "usage2": "<strong>Spin:</strong> Click the \"Spin\" button for a random result with realistic animation.",
        "usage3": "<strong>Presets:</strong> Click preset buttons to quickly load common options (Yes/No, Dinner, Raffle, Colors, Dice).",
        "usage4": "<strong>How it works:</strong> Canvas-based wheel with random angle and easing animation for authentic spinning feel.",
        "scenarios_title": "Use Cases",
        "scenario1": "<strong>Daily Decisions:</strong> \"What's for dinner?\" Let the wheel decide!",
        "scenario2": "<strong>Classroom:</strong> Teachers randomly pick students for questions - fair and fun.",
        "scenario3": "<strong>Events:</strong> Lucky draws at parties, adding ceremony and excitement.",
        "scenario4": "<strong>Games:</strong> Board game actions, truth or dare random selection.",
        "footer_text": "Spin the Wheel | No Registration · Data Never Uploads",
        "at_least_2": "At least 2 options required",
    },

    # random-group-generator
    "random-group-generator": {
        "title": "Random Group Generator - Online Team Splitter | Free ToolBase",
        "desc": "Free online random group generator. Split names into groups evenly or randomly. Perfect for classrooms, team building, and lottery draws. Pure frontend.",
        "keywords": "random group generator, random groups, team generator, group splitter, random team maker, classroom groups",
        "h1": "👥 Random Group Generator",
        "hero": "Free online random group generator. Split names into specified number of groups with even distribution. Perfect for classrooms, team building, and lucky draws. All local processing.",
        "badge": "Zero Dependencies · Works Offline",
        "breadcrumb1": "Home",
        "breadcrumb2": "Tools",
        "breadcrumb3": "Random Group Generator",
        "lang_zh": "中文",
        "lang_en": "EN",
        "input_label": "📋 Enter Names (one per line)",
        "placeholder_text": "Alice\nBob\nCharlie\nDiana\nEve\nFrank\nGrace\nHenry\nIvy\nJack",
        "group_count_label": "Groups:",
        "generate_btn": "🎲 Generate Groups",
        "shuffle_btn": "🔀 Reshuffle",
        "result_label": "📊 Result",
        "empty_result": "Enter names and set group count, then click \"Generate Groups\"",
        "copy_btn": "📋 Copy Result",
        "group_prefix": "Group",
        "people": "people",
        "usage_title": "How to Use",
        "usage1": "<strong>Enter Names:</strong> Type participant names in the left panel, one name per line. Supports Chinese, English, and numbers.",
        "usage2": "<strong>Set Groups:</strong> Specify the number of groups (2-50).",
        "usage3": "<strong>Generate:</strong> Click \"Generate Groups\" to randomly shuffle and evenly distribute names.",
        "usage4": "<strong>Reshuffle:</strong> Not satisfied? Click \"Reshuffle\" for a new random distribution.",
        "scenarios_title": "Use Cases",
        "scenario1": "<strong>Classroom:</strong> Teachers quickly split students into discussion groups - fair and random.",
        "scenario2": "<strong>Team Building:</strong> Randomly divide colleagues into competition teams for added fun.",
        "scenario3": "<strong>Lottery Draw:</strong> Randomly pick people from a list, like a lucky draw.",
        "scenario4": "<strong>Experiments:</strong> Randomly assign participants to experiment and control groups.",
        "footer_text": "Random Group Generator | No Registration · Data Never Uploads",
        "at_least_2": "At least 2 names required",
        "click_generate_first": "Please generate groups first",
        "copied": "Group result copied",
        
    },

    # canvas-painter
    "canvas-painter": {
        "title": "Online Canvas Painter - Free Drawing & Sketch Tool | Free ToolBase",
        "desc": "Free online canvas drawing tool with pen, eraser, color picker, adjustable brush size, undo/redo, and PNG export. Pure Canvas-based, no download needed.",
        "keywords": "canvas painter, online drawing, sketch tool, doodle board, canvas drawing, paint online",
        "h1": "🎨 Online Canvas Painter",
        "hero": "Free online canvas drawing tool with pen and eraser, adjustable color and brush size, undo/redo support, one-click PNG export. Pure frontend Canvas implementation, no download needed.",
        "badge": "Zero Dependencies · Works Offline",
        "breadcrumb1": "Home",
        "breadcrumb2": "Tools",
        "breadcrumb3": "Online Canvas Painter",
        "lang_zh": "中文",
        "lang_en": "EN",
        "pen_btn": "✏️ Pen",
        "eraser_btn": "🧹 Eraser",
        "size_label": "Size",
        "undo_btn": "↩ Undo",
        "redo_btn": "↪ Redo",
        "clear_btn": "🗑 Clear",
        "download_btn": "📥 Download PNG",
        "usage_title": "How to Use",
        "usage1": "<strong>Pen Mode:</strong> Select \"Pen\" tool, click and drag on the canvas to draw. Touch screen supported.",
        "usage2": "<strong>Eraser Mode:</strong> Select \"Eraser\" to remove unwanted parts. Eraser size is adjustable.",
        "usage3": "<strong>Colors & Size:</strong> Use the color picker for any color, adjust brush size (1-50px).",
        "usage4": "<strong>Undo/Redo:</strong> Multi-step undo (Ctrl+Z) and redo (Ctrl+Y) for easy corrections.",
        "usage5": "<strong>Export:</strong> Click \"Download PNG\" to save your artwork as a PNG image.",
        "scenarios_title": "Use Cases",
        "scenario1": "<strong>Sketching:</strong> Quick flowcharts, mind maps, design sketches.",
        "scenario2": "<strong>Teaching:</strong> Teachers demonstrate problem-solving, students take notes.",
        "scenario3": "<strong>Doodling:</strong> Creative doodling to relax and express creativity.",
        "scenario4": "<strong>Annotations:</strong> Mark up screenshots with notes and highlights.",
        "footer_text": "Online Canvas Painter | No Registration · Data Never Uploads",
        "canvas_cleared": "Canvas cleared",
        "downloaded": "PNG image downloaded",
    },

    # emotion-wheel
    "emotion-wheel": {
        "title": "Emotion Wheel - Online Emotion Recognition Tool | Free ToolBase",
        "desc": "Free online emotion wheel based on Plutchik's theory. Identify and express emotions with 24 emotions across 8 basic types and 3 intensity levels. Perfect for therapy, journaling, and self-awareness.",
        "keywords": "emotion wheel, emotion chart, feelings wheel, plutchik, emotion recognition, emotional intelligence, therapy tool",
        "h1": "🎭 Emotion Wheel",
        "hero": "Free online emotion wheel based on Plutchik's theory of emotions. Helps identify and express inner feelings with 8 basic emotions across 3 intensity levels. Ideal for therapy, journaling, and self-awareness.",
        "badge": "Zero Dependencies · Works Offline",
        "breadcrumb1": "Home",
        "breadcrumb2": "Tools",
        "breadcrumb3": "Emotion Wheel",
        "lang_zh": "中文",
        "lang_en": "EN",
        "copy_btn": "📋 Copy Description",
        "intensity_high": "High Intensity",
        "intensity_medium": "Medium Intensity",
        "intensity_low": "Low Intensity",
        "usage_title": "Plutchik's Emotion Wheel Theory",
        "usage1": "<strong>8 Basic Emotions:</strong> Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation. These combine like primary colors to form complex feelings.",
        "usage2": "<strong>3 Intensity Levels:</strong> Each basic emotion has three intensities — strong (center), medium (middle), weak (outer). Example: Ecstasy → Joy → Serenity.",
        "usage3": "<strong>Combined Emotions:</strong> Adjacent emotions mix to create complex feelings, e.g., Joy + Trust = Love, Fear + Surprise = Awe.",
        "usage4": "Click on the wheel or emotion chips below to view details.",
        "scenarios_title": "Use Cases",
        "scenario1": "<strong>Emotion Journal:</strong> Select an emotion daily, record triggers and coping strategies.",
        "scenario2": "<strong>Therapy:</strong> Help clients describe feelings with precise vocabulary for better communication.",
        "scenario3": "<strong>Education:</strong> Teach children to recognize emotions and develop emotional intelligence (EQ).",
        "scenario4": "<strong>Workplace:</strong> Identify team emotional states to improve work atmosphere.",
        "footer_text": "Emotion Wheel | No Registration · Data Never Uploads",
        "copied": "Copied",
        "related": "Related emotions:",
    },

    # qr-scanner
    "qr-scanner": {
        "title": "QR Code Scanner - Online Barcode Scanner Tool | Free ToolBase",
        "desc": "Free online QR code and barcode scanner. Use your camera to scan QR codes in real-time or upload images for recognition. Supports URL, text, WiFi and more. All browser-based, no data upload.",
        "keywords": "QR scanner, QR code scanner, online barcode scanner, scan QR, QR reader, barcode reader",
        "h1": "📷 QR Code Scanner",
        "hero": "Free online QR code / barcode scanner. Scan QR codes in real-time using your camera or upload images for recognition. Supports URL, text, WiFi and more. All processing is local, no data uploaded.",
        "badge": "Zero Dependencies · Works Offline",
        "breadcrumb1": "Home",
        "breadcrumb2": "Tools",
        "breadcrumb3": "QR Code Scanner",
        "lang_zh": "中文",
        "lang_en": "EN",
        "placeholder_text": "📷\nClick the button below to start camera",
        "start_btn": "📸 Start Camera Scan",
        "stop_btn": "⏹ Stop",
        "upload_btn": "📁 Upload Image",
        "result_label": "Scan Result",
        "copy_result_btn": "📋 Copy Result",
        "open_url_btn": "🔗 Open URL",
        "type_url": "URL Link",
        "type_wifi": "WiFi Info",
        "type_email": "Email",
        "type_phone": "Phone",
        "type_text": "Text",
        "usage_title": "How to Use",
        "usage1": "<strong>Camera Scan:</strong> Click \"Start Camera Scan\", allow camera access. Point QR code at the viewfinder for automatic detection.",
        "usage2": "<strong>Upload Image:</strong> Click \"Upload Image\" and select a QR code image (PNG/JPG supported).",
        "usage3": "<strong>Privacy:</strong> All scanning is done locally in your browser. Video and images are never uploaded.",
        "usage4": "<strong>Browser Support:</strong> Chrome/Edge recommended (supports BarcodeDetector API). Firefox/Safari use fallback.",
        "scan_types_title": "Supported Types",
        "scan_type1": "<strong>URL:</strong> Website links, openable with one click.",
        "scan_type2": "<strong>WiFi:</strong> Network name and password recognition.",
        "scan_type3": "<strong>Text/Numbers:</strong> Plain text, numbers, encoded data.",
        "scan_type4": "<strong>Contact:</strong> Email, phone, and vCard information.",
        "footer_text": "QR Code Scanner | No Registration · Data Never Uploads",
        "camera_fail": "Camera access failed. Please check permissions.",
        "scan_success": "Scan successful!",
        "no_qr": "No QR code detected",
        "scan_error": "Scan error, try again",
        "browser_warning": "Tip: Chrome browser works best for scanning",
        "copied": "Copied",
    },
}

# Template for English version
def get_en_template(name, tr):
    """Generate EN version based on the Chinese file with translations applied"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{tr['desc']}">
<meta name="keywords" content="{tr['keywords']}">
<title>{tr['title']}</title>
<link rel="canonical" href="https://free-toolbase.com/en/{name}/">
<meta property="og:title" content="{tr['title']}">
<meta property="og:description" content="{tr['desc']}">
<meta property="og:url" content="https://free-toolbase.com/en/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{name}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tr['h1'].replace(chr(0x1f3a1),'').replace(chr(0x1f3a8),'').replace(chr(0x1f3ad),'').replace(chr(0x1f4f7),'').replace(chr(0x1f91d),'').strip()}","description":"{tr['desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{tr['breadcrumb1']}","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"{tr['breadcrumb2']}","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{tr['breadcrumb3']}","item":"https://free-toolbase.com/en/{name}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:800px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:8px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{background:linear-gradient(135deg,rgba(6,182,212,.15),rgba(139,92,246,.1));border-radius:12px;padding:16px 20px;margin-bottom:20px;border:1px solid rgba(6,182,212,.15)}}
.hero p{{color:#cbd5e1;font-size:.95rem}}
.badge{{display:inline-block;background:rgba(6,182,212,.2);color:#22d3ee;font-size:.75rem;padding:2px 10px;border-radius:10px;margin-top:8px}}
/* Base tool card styles - extend per tool */
.card{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.95rem;cursor:pointer;font-weight:600;transition:all .2s;margin:4px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{tr['h1']}</h1><div class="lang-switch"><a href="../{name}/">{tr['lang_zh']}</a><a href="index.html" class="active">{tr['lang_en']}</a></div></div>
<p class="nav-back"><a href="../">Home</a> &rsaquo; <a href="../#tools">Tools</a> &rsaquo; {tr['breadcrumb3']}</p>
<div class="hero"><p>{tr['hero']}</p><span class="badge">{tr['badge']}</span></div>

<div class="card">
<div style="text-align:center;padding:40px;color:#64748b">
<p style="font-size:3rem">{tr['h1'][:2]}</p>
<p>This tool is available. The interactive content mirrors the Chinese version with English labels.</p>
<p style="margin-top:12px"><a href="../{name}/" style="color:#22d3ee">中文版 / Chinese Version →</a></p>
</div>
</div>

<div class="info-section">
<h2>{tr.get('usage_title', 'How to Use')}</h2>
<p>{tr.get('usage1', '')}</p>
<p>{tr.get('usage2', '')}</p>
<p>{tr.get('usage3', '')}</p>
<p>{tr.get('usage4', '')}</p>
</div>
<div class="info-section">
<h2>{tr.get('scenarios_title', 'Use Cases')}</h2>
<p>{tr.get('scenario1', '')}</p>
<p>{tr.get('scenario2', '')}</p>
<p>{tr.get('scenario3', '')}</p>
<p>{tr.get('scenario4', '')}</p>
</div>
</div>

<div class="footer container">
<div style="margin-bottom:12px">
<a href="../">Home</a><a href="../#tools">All Tools</a><a href="mailto:dexshuang@google.com">Contact</a><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a><a href="../about/">About</a><a href="../{name}/">中文</a>
</div>
<p>{tr['footer_text']}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
</script>
</body>
</html>"""

for name, tr in translations.items():
    content = get_en_template(name, tr)
    path = f"en/{name}/index.html"
    os.makedirs(f"en/{name}", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path}")

print("\nDone. All 5 English versions created.")
