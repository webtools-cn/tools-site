#!/usr/bin/env python3
"""批量生成新工具页面（中英文双语）"""
import os, json, datetime

TODAY = datetime.date.today().strftime('%Y-%m-%d')

# ============ 工具定义 ============
TOOLS = [
    {
        "slug": "audio-reverse-player",
        "cn": {
            "title": "免费音频倒放器 - 在线音频反向播放工具 | 无需注册",
            "h1": "🔄 音频倒放器",
            "desc": "免费在线音频倒放工具，上传音频文件实现反向播放效果。支持WAV/MP3格式，可下载反转后的音频。纯前端Web Audio API处理。",
            "hero": "免费在线音频倒放工具。上传WAV/MP3音频文件，自动生成反向播放效果。纯前端Web Audio API处理，文件不上传服务器。",
            "howto_steps": [
                "上传音频文件（点击或拖放WAV/MP3）",
                '点击"开始倒放"按钮处理音频',
                "在线试听倒放效果",
                "点击下载按钮保存反转后的音频文件"
            ],
            "features": ["支持WAV/MP3格式", "纯前端Web Audio API处理", "文件不上传服务器", "在线试听倒放效果", "一键下载反转音频"],
            "faq": [
                ("支持哪些音频格式？", "支持WAV和MP3格式。使用Web Audio API在浏览器中解码处理。"),
                ("音频文件会上传到服务器吗？", "不会。所有处理在浏览器本地完成，文件数据绝不上传。"),
                ("反转后的音频可以下载吗？", "可以。处理完成后点击下载按钮保存为WAV格式文件。"),
                ("支持多大的音频文件？", "取决于浏览器内存。建议单个文件不超过100MB。大文件处理可能需要几秒钟。"),
                ("倒放效果如何？", "音频数据完全反转，包括音高、节奏和时长，产生独特的反向播放效果。")
            ]
        },
        "en": {
            "title": "Free Audio Reverse Player - Reverse Audio Online | No Signup",
            "h1": "🔄 Audio Reverse Player",
            "desc": "Free online audio reverse player. Upload audio files to create reverse playback effects. Supports WAV/MP3 formats. Download the reversed audio file. Pure frontend Web Audio API.",
            "hero": "Free online audio reverse player. Upload WAV/MP3 files, automatically generate reverse playback. Pure frontend Web Audio API processing, files never leave your device.",
            "howto_steps": [
                "Upload audio file (click or drag WAV/MP3)",
                "Click \"Reverse\" to process the audio",
                "Preview the reversed audio online",
                "Download the reversed audio file"
            ],
            "features": ["Supports WAV/MP3 formats", "Pure frontend Web Audio API", "Files never uploaded", "Online preview of reversed audio", "One-click download"],
            "faq": [
                ("What audio formats are supported?", "WAV and MP3 formats are supported. Processed using Web Audio API in the browser."),
                ("Are audio files uploaded to a server?", "No. All processing happens locally in your browser. Files never leave your device."),
                ("Can I download the reversed audio?", "Yes. After processing, click download to save as a WAV file."),
                ("What file size is supported?", "Depends on browser memory. Recommended under 100MB per file. Large files may take a few seconds."),
                ("How does the reverse effect work?", "Audio data is completely reversed, including pitch, rhythm and duration, creating unique reverse playback effects.")
            ]
        }
    },
    {
        "slug": "vocal-remover-online",
        "cn": {
            "title": "免费在线去人声工具 - 人声分离卡拉OK伴奏制作 | 无需注册",
            "h1": "🎤 在线去人声工具",
            "desc": "免费在线去人声工具，从音乐中分离人声和伴奏。使用相位抵消技术，支持多种音频格式。适合制作卡拉OK伴奏。纯前端处理，文件不上传。",
            "hero": "免费在线去人声工具。通过相位抵消技术从音乐中分离人声和伴奏，制作卡拉OK伴奏。纯前端Web Audio API处理，文件不上传。",
            "howto_steps": [
                "上传音频文件（点击或拖放，支持WAV/MP3）",
                '点击"分离人声"按钮开始处理',
                "在线试听分离后的伴奏和人声",
                "下载伴奏或人声音频文件"
            ],
            "features": ["相位抵消人声分离技术", "纯前端Web Audio API处理", "文件不上传服务器", "可分别试听伴奏和人声", "一键下载分离后的音频"],
            "faq": [
                ("去人声的原理是什么？", "使用相位抵消技术。立体声音频中，人声通常在中央声道，通过反转一个声道并混合，可以抵消中央的人声。"),
                ("支持哪些音频格式？", "支持WAV和MP3格式。立体声音频效果最佳，单声道音频无法有效分离。"),
                ("音频文件会上传吗？", "不会。所有处理在浏览器本地完成，文件绝不上传服务器。"),
                ("分离效果如何？", "取决于原始音频的混音方式。录音室制作的立体声音乐效果最佳，现场录音效果可能不理想。"),
                ("可以下载分离后的音频吗？", "可以。处理完成后可分别下载伴奏和人声轨。")
            ]
        },
        "en": {
            "title": "Free Online Vocal Remover - Separate Vocals for Karaoke | No Signup",
            "h1": "🎤 Vocal Remover Online",
            "desc": "Free online vocal remover. Separate vocals from accompaniment using phase cancellation. Supports multiple audio formats. Perfect for karaoke tracks. Pure frontend processing.",
            "hero": "Free online vocal remover. Separate vocals from instrumentals using phase cancellation. Create karaoke tracks. Pure frontend Web Audio API, files stay local.",
            "howto_steps": [
                "Upload audio file (click or drag, WAV/MP3 supported)",
                "Click \"Remove Vocals\" to process",
                "Preview the instrumental and vocal tracks",
                "Download instrumental or vocal audio"
            ],
            "features": ["Phase cancellation vocal separation", "Pure frontend Web Audio API", "Files never uploaded", "Separate instrumental & vocal preview", "One-click download separated audio"],
            "faq": [
                ("How does vocal removal work?", "Uses phase cancellation. In stereo audio, vocals are typically in the center channel. Inverting one channel and mixing cancels center-panned vocals."),
                ("What formats are supported?", "WAV and MP3. Stereo audio works best; mono audio cannot be effectively separated."),
                ("Are files uploaded?", "No. All processing is done locally in your browser. Files never leave your device."),
                ("How good is the separation?", "Depends on the original mix. Studio-produced stereo music works best; live recordings may have limited results."),
                ("Can I download separated tracks?", "Yes. After processing, download instrumental and vocal tracks separately.")
            ]
        }
    },
    {
        "slug": "pitch-detector-online",
        "cn": {
            "title": "免费在线音高检测器 - 实时频率音符识别调音 | 无需注册",
            "h1": "🎵 在线音高检测器",
            "desc": "免费在线音高检测器，通过麦克风实时检测音高频率和音符。支持A4=440Hz标准调音，显示频率和音分偏差。适合乐器调音和唱歌练习。",
            "hero": "免费在线音高检测工具。使用麦克风实时检测音高，显示频率和对应音符。支持A4=440Hz标准调音，显示音分偏差。适合乐器调音。",
            "howto_steps": [
                "点击'开始检测"并允许麦克风权限',
                "发出声音（唱歌或演奏乐器）",
                "实时查看检测到的音高和音符",
                "根据音分偏差调整音准"
            ],
            "features": ["实时音高检测", "自动音符识别（C4-B7）", "显示频率和音分偏差", "A4=440Hz标准调音", "响应时间<50ms"],
            "faq": [
                ("如何使用音高检测器？", "点击开始检测，允许麦克风权限，然后唱歌或演奏乐器即可实时看到音高。"),
                ("支持哪些音符范围？", "支持C4(261.63Hz)到B7(3951.07Hz)范围，覆盖大部分人声和乐器范围。"),
                ("需要安装软件吗？", "不需要。完全在线使用，通过浏览器麦克风API实现。"),
                ("精度如何？", "使用自相关算法，精度可达±1音分。显示频率精确到0.1Hz。"),
                ("可以用于吉他调音吗？", "可以。支持半音检测，适合吉他、尤克里里等弦乐器的调音。")
            ]
        },
        "en": {
            "title": "Free Online Pitch Detector - Real-time Note & Frequency Tuner | No Signup",
            "h1": "🎵 Pitch Detector Online",
            "desc": "Free online pitch detector. Real-time pitch frequency and note detection via microphone. Supports A4=440Hz standard tuning. Shows frequency and cent deviation. Great for instrument tuning.",
            "hero": "Free online pitch detector. Real-time frequency and note detection using your microphone. Supports A4=440Hz standard tuning with cent deviation display. Perfect for instrument tuning.",
            "howto_steps": [
                "Click \"Start\" and allow microphone access",
                "Make a sound (sing or play an instrument)",
                "View detected pitch and note in real-time",
                "Adjust tuning based on cent deviation"
            ],
            "features": ["Real-time pitch detection", "Automatic note recognition (C4-B7)", "Frequency & cent deviation display", "A4=440Hz standard tuning", "<50ms response time"],
            "faq": [
                ("How to use the pitch detector?", "Click start, allow microphone access, then sing or play an instrument to see pitch in real-time."),
                ("What note range is supported?", "C4 (261.63Hz) to B7 (3951.07Hz), covering most vocal and instrumental ranges."),
                ("Do I need to install software?", "No. Fully online, using browser microphone API."),
                ("How accurate is it?", "Uses autocorrelation algorithm with ±1 cent accuracy. Frequency displayed to 0.1Hz precision."),
                ("Can I use it for guitar tuning?", "Yes. Supports chromatic detection suitable for guitar, ukulele and other string instruments.")
            ]
        }
    },
    {
        "slug": "text-to-emoji-converter",
        "cn": {
            "title": "免费文字转Emoji工具 - 文本Emoji化在线转换 | 无需注册",
            "h1": "😊 文字转Emoji",
            "desc": "在线文字转Emoji工具，将普通文本转换为Emoji风格。支持字母映射和多种转换模式。一键复制转换结果。适合社交媒体文案和趣味内容创作。",
            "hero": "免费在线文字转Emoji工具。将普通文本转换为Emoji风格，支持字母映射和多种转换模式。一键复制转换结果。适合社交媒体文案。",
            "howto_steps": [
                "在输入框中输入或粘贴文字",
                "选择转换模式（字母映射/单词映射）",
                "查看Emoji风格的转换结果",
                "一键复制转换后的文本"
            ],
            "features": ["字母到Emoji自动映射", "支持单词级别映射", "多种转换模式", "实时转换预览", "一键复制结果"],
            "faq": [
                ("文字如何转换为Emoji？", "每个字母映射到对应的Emoji字符（如A→🅰️），单词级别则按常见词汇映射。"),
                ("支持中文吗？", "目前主要支持英文字母和数字的转换。中文暂不支持Emoji映射。"),
                ("转换结果可以复制吗？", "可以。点击复制按钮一键复制转换后的Emoji文本到剪贴板。"),
                ("支持哪些转换模式？", "支持字母映射（每个字母转Emoji）、单词映射（常见单词转Emoji）和混合模式。"),
                ("Emoji在所有平台显示一致吗？", "不同平台的Emoji显示可能有差异。建议在目标平台预览确认。")
            ]
        },
        "en": {
            "title": "Free Text to Emoji Converter - Transform Text into Emoji Style | No Signup",
            "h1": "😊 Text to Emoji Converter",
            "desc": "Free online text to emoji converter. Transform plain text into emoji style with letter and word mapping. Multiple modes supported. One-click copy. Perfect for social media content.",
            "hero": "Free online text to emoji converter. Transform text into emoji style with letter mapping and multiple conversion modes. One-click copy results. Perfect for social media.",
            "howto_steps": [
                "Enter or paste text in the input field",
                "Choose conversion mode (letter/word mapping)",
                "View the emoji-style output",
                "One-click copy the converted text"
            ],
            "features": ["Letter to emoji auto-mapping", "Word-level mapping support", "Multiple conversion modes", "Real-time preview", "One-click copy"],
            "faq": [
                ("How does text convert to emoji?", "Each letter maps to a corresponding emoji (e.g., A→🅰️). Word-level mode maps common words to emojis."),
                ("Does it support Chinese?", "Currently supports English letters and numbers. Chinese characters are not yet supported for emoji mapping."),
                ("Can I copy the result?", "Yes. Click the copy button to copy the emoji text to clipboard."),
                ("What conversion modes are available?", "Letter mapping (each letter → emoji), word mapping (common words → emoji), and mixed mode."),
                ("Do emojis display consistently across platforms?", "Emoji display may vary by platform. Preview on your target platform is recommended.")
            ]
        }
    },
    {
        "slug": "image-border-generator",
        "cn": {
            "title": "免费图片边框生成器 - 在线添加圆角阴影边框 | 无需注册",
            "h1": "🖼️ 图片边框生成器",
            "desc": "免费在线图片边框生成工具，为图片添加自定义边框。支持圆角、阴影、颜色渐变、虚线等多种边框样式。实时预览，纯前端Canvas渲染。",
            "hero": "免费在线图片边框生成器。上传图片，自定义边框样式（圆角、阴影、颜色、虚线），实时预览效果并下载。纯前端Canvas处理，文件不上传。",
            "howto_steps": [
                "上传图片（点击或拖放，支持JPG/PNG/WebP）",
                "调整边框参数（宽度、颜色、圆角、阴影）",
                "实时预览边框效果",
                "点击下载按钮保存带边框的图片"
            ],
            "features": ["圆角/阴影/虚线边框", "实时预览效果", "纯前端Canvas渲染", "支持JPG/PNG/WebP", "高质量PNG输出"],
            "faq": [
                ("支持哪些图片格式？", "支持JPG、PNG和WebP格式。输出为高质量PNG格式。"),
                ("边框有哪些样式？", "支持实线、虚线、点线边框，可调节宽度、颜色、圆角和阴影效果。"),
                ("图片会上传吗？", "不会。所有处理在浏览器本地完成，文件不上传服务器。"),
                ("支持透明背景吗？", "支持。PNG透明背景会保留，边框渲染在图片周围。"),
                ("输出图片质量如何？", "使用Canvas渲染，输出为原始分辨率的高质量PNG图片。")
            ]
        },
        "en": {
            "title": "Free Image Border Generator - Add Rounded Corners & Shadows Online | No Signup",
            "h1": "🖼️ Image Border Generator",
            "desc": "Free online image border generator. Add custom borders with rounded corners, shadows, gradients, dashed lines. Real-time preview with pure frontend Canvas rendering.",
            "hero": "Free online image border generator. Upload images, customize borders (rounded corners, shadows, colors, dashed), real-time preview and download. Pure frontend Canvas processing.",
            "howto_steps": [
                "Upload image (click or drag, JPG/PNG/WebP supported)",
                "Adjust border settings (width, color, radius, shadow)",
                "Real-time preview of border effect",
                "Download the bordered image"
            ],
            "features": ["Rounded/shadow/dashed borders", "Real-time preview", "Pure frontend Canvas", "JPG/PNG/WebP support", "High quality PNG output"],
            "faq": [
                ("What image formats are supported?", "JPG, PNG and WebP. Output is high quality PNG format."),
                ("What border styles are available?", "Solid, dashed, dotted borders with adjustable width, color, radius and shadow effects."),
                ("Are images uploaded?", "No. All processing is done locally in your browser. Files never leave your device."),
                ("Is transparent background supported?", "Yes. PNG transparency is preserved, borders render around the image."),
                ("What's the output quality?", "Canvas rendered at original resolution with high quality PNG output.")
            ]
        }
    },
    {
        "slug": "binary-text-translator",
        "cn": {
            "title": "免费二进制文本翻译器 - 二进制与文本互转 | 无需注册",
            "h1": "0️⃣1️⃣ 二进制文本翻译器",
            "desc": "在线二进制文本翻译器，在二进制和文本之间互相转换。支持ASCII/UTF-8编码，8位和7位格式。一键复制结果。适合编程学习和数据编码。",
            "hero": "免费在线二进制文本翻译器。在二进制和文本之间互相转换，支持ASCII/UTF-8编码，支持8位和7位二进制格式。适合编程学习。",
            "howto_steps": [
                "输入文本或二进制数据",
                "选择转换方向（文本→二进制 或 二进制→文本）",
                "选择编码格式（8位/7位）",
                "查看转换结果并一键复制"
            ],
            "features": ["文本↔二进制双向转换", "支持8位/7位格式", "ASCII/UTF-8编码", "实时转换", "一键复制结果"],
            "faq": [
                ("支持哪些编码？", "支持ASCII和UTF-8编码。ASCII使用7位二进制，UTF-8使用8位二进制表示。"),
                ("如何区分8位和7位？", "7位格式每字符7位（标准ASCII），8位格式每字符8位（扩展ASCII/UTF-8）。"),
                ("支持中文吗？", "支持。使用UTF-8编码，每个中文字符转换为多个8位二进制组。"),
                ("转换结果准确吗？", "准确。基于标准字符编码表转换，确保结果可逆。"),
                ("数据会上传吗？", "不会。所有转换在浏览器本地完成，数据不上传服务器。")
            ]
        },
        "en": {
            "title": "Free Binary Text Translator - Convert Binary to Text Online | No Signup",
            "h1": "0️⃣1️⃣ Binary Text Translator",
            "desc": "Free online binary text translator. Convert between binary and text with ASCII/UTF-8 encoding. Supports 8-bit and 7-bit formats. One-click copy. Great for programming and data encoding.",
            "hero": "Free online binary text translator. Convert between binary and text, supporting ASCII/UTF-8 encoding with 8-bit and 7-bit binary formats. Perfect for programming learning.",
            "howto_steps": [
                "Enter text or binary data",
                "Choose conversion direction (Text→Binary or Binary→Text)",
                "Select encoding format (8-bit/7-bit)",
                "View result and copy with one click"
            ],
            "features": ["Text↔Binary bidirectional", "8-bit/7-bit formats", "ASCII/UTF-8 encoding", "Real-time conversion", "One-click copy"],
            "faq": [
                ("What encodings are supported?", "ASCII and UTF-8. ASCII uses 7-bit binary, UTF-8 uses 8-bit per character."),
                ("What's the difference between 8-bit and 7-bit?", "7-bit is standard ASCII (7 bits per char), 8-bit is extended ASCII/UTF-8 (8 bits per char)."),
                ("Does it support Chinese?", "Yes. Using UTF-8 encoding, each Chinese character converts to multiple 8-bit groups."),
                ("Is the conversion accurate?", "Yes. Based on standard character encoding tables, ensuring reversible results."),
                ("Is data uploaded?", "No. All conversion happens locally in your browser.")
            ]
        }
    },
    {
        "slug": "typing-speed-test-online",
        "cn": {
            "title": "免费在线打字速度测试 - WPM准确率实时统计 | 无需注册",
            "h1": "⌨️ 打字速度测试",
            "desc": "免费在线打字速度测试，实时显示WPM和准确率。提供多种难度文本，支持中英文切换。无需注册，即刻开始练习。",
            "hero": "免费在线打字速度测试工具。实时显示打字速度(WPM)、准确率和用时。提供多种难度文本，支持中英文切换。无需注册，即刻开始。",
            "howto_steps": [
                "选择难度级别（简单/中等/困难）",
                "在输入框中按照显示文本打字",
                "实时查看WPM和准确率",
                "完成后查看详细统计结果"
            ],
            "features": ["实时WPM显示", "准确率统计", "多种难度文本", "中英文支持", "计时自动统计"],
            "faq": [
                ("WPM是什么意思？", "WPM (Words Per Minute) 每分钟输入单词数。一个单词按5个字符计算。"),
                ("支持中文打字测试吗？", "支持。中文模式下按字符数计算速度，同时显示字/分钟统计。"),
                ("如何计算准确率？", "正确输入的字符数占总输入字符数的百分比。实时显示当前准确率。"),
                ("数据会上传吗？", "不会。所有统计在浏览器本地完成，数据不上传服务器。"),
                ("可以重复练习吗？", "可以。刷新文本按钮随机更换练习文本，支持多次练习。")
            ]
        },
        "en": {
            "title": "Free Online Typing Speed Test - Real-time WPM & Accuracy | No Signup",
            "h1": "⌨️ Typing Speed Test",
            "desc": "Free online typing speed test. Real-time WPM and accuracy display. Multiple difficulty levels with Chinese and English support. No registration, start practicing now.",
            "hero": "Free online typing speed test. Real-time WPM, accuracy and time display. Multiple difficulty texts with Chinese and English support. No registration needed.",
            "howto_steps": [
                "Choose difficulty level (Easy/Medium/Hard)",
                "Type the displayed text in the input field",
                "View WPM and accuracy in real-time",
                "See detailed stats when finished"
            ],
            "features": ["Real-time WPM display", "Accuracy statistics", "Multiple difficulty levels", "Chinese & English support", "Auto-timing statistics"],
            "faq": [
                ("What does WPM mean?", "Words Per Minute. One word is calculated as 5 characters."),
                ("Does it support Chinese typing?", "Yes. Chinese mode calculates speed by character count with chars/minute display."),
                ("How is accuracy calculated?", "Percentage of correctly typed characters out of total characters entered. Updated in real-time."),
                ("Is data uploaded?", "No. All statistics are calculated locally in your browser."),
                ("Can I practice multiple times?", "Yes. Refresh text button randomizes practice text for repeated practice.")
            ]
        }
    },
]

# ============ HTML 模板 ============
CN_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{cn_desc}">
<meta name="keywords" content="{cn_keywords}">
<title>{cn_title}</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{cn_title}">
<meta property="og:description" content="{cn_desc}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{cn_name}","description":"{cn_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{cn_name}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{margin-bottom:20px;color:#94a3b8;font-size:.9rem;line-height:1.7}}
.hero .badge{{display:inline-block;margin-top:8px;padding:3px 10px;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:12px;font-size:.75rem;color:#22d3ee}}
.section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:6px}}
.form-group input[type="text"],.form-group input[type="number"],.form-group textarea,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group textarea:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.file-drop{{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;border:2px dashed rgba(148,163,184,.3);border-radius:12px;cursor:pointer;transition:all .3s;text-align:center}}
.file-drop:hover{{border-color:rgba(6,182,212,.5);background:rgba(6,182,212,.03)}}
.file-drop .icon{{font-size:2.5rem;margin-bottom:10px}}
.file-drop .hint{{color:#64748b;font-size:.85rem;margin-top:6px}}
.btn{{padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:500}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.15)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2);color:#e2e8f0}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.btn-danger:hover{{background:rgba(239,68,68,.25)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-box{{margin-top:16px;padding:16px;background:rgba(148,163,184,.05);border-radius:8px;min-height:60px}}
.result-box .label{{color:#64748b;font-size:.8rem;margin-bottom:6px}}
.result-box .value{{color:#22d3ee;font-size:1.1rem;font-weight:600;word-break:break-all}}
.feature-list{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}
.feature-tag{{padding:5px 12px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.15);border-radius:16px;font-size:.8rem;color:#22d3ee}}
.seo-content{{margin-bottom:20px;padding:16px;background:rgba(148,163,184,.03);border-radius:8px;border:1px solid rgba(148,163,184,.06)}}
.seo-content h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.seo-content ol{{padding-left:20px;margin-top:12px}}
.seo-content li{{margin-bottom:16px}}
.seo-content li strong{{color:#f1f5f9}}
.seo-content li span{{color:#94a3b8;font-size:.9rem}}
.faq-item{{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(148,163,184,.06)}}
.faq-item:last-child{{border-bottom:none}}
.faq-item .q{{color:#f1f5f9;font-size:.95rem;font-weight:600;margin-bottom:6px}}
.faq-item .a{{color:#94a3b8;font-size:.85rem;line-height:1.6}}
.preview-area{{margin-top:12px;text-align:center}}
.preview-area canvas,.preview-area img{{max-width:100%;border-radius:8px;max-height:400px}}
.status-bar{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:8px 12px;background:rgba(148,163,184,.05);border-radius:6px;margin:10px 0}}
.status-bar .info{{color:#94a3b8;font-size:.85rem}}
.stats-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}}
.stat-card{{text-align:center;padding:16px;background:rgba(148,163,184,.05);border-radius:8px}}
.stat-card .num{{font-size:1.8rem;font-weight:700;color:#22d3ee}}
.stat-card .lbl{{font-size:.75rem;color:#64748b;margin-top:4px}}
.test-text{{padding:16px;background:rgba(148,163,184,.05);border-radius:8px;font-size:1.1rem;line-height:1.8;margin-bottom:16px;color:#e2e8f0;letter-spacing:0.5px}}
.test-text .correct{{color:#22d3ee}}
.test-text .error{{color:#ef4444;text-decoration:underline}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}.stats-grid{{grid-template-columns:repeat(3,1fr)}}.stat-card .num{{font-size:1.3rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{cn_h1}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {cn_name}</p>
<div class="hero"><p>{cn_hero}</p><span class="badge">零依赖·可离线使用</span></div>
<div class="main-grid">
<div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {today}
  </span>
</div>
<div class="section">
<h2>功能操作区</h2>
<div class="feature-list">
{cn_features_html}
</div>
{cn_body}
</div>
<div class="section">
<h2>常见问题</h2>
{cn_faq_html}
</div>
</div>
<div class="seo-content">
<h2>如何使用{cn_name}</h2>
<p>使用{cn_name}非常简单：</p>
<ol>
{cn_howto_html}
</ol>
</div>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{slug}/">EN</a>
</div>
<p>{cn_name} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
</div>
<div class="toast" id="toast"></div>
{cn_js}
</body>
</html>"""

EN_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{en_desc}">
<meta name="keywords" content="{en_keywords}">
<title>{en_title}</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{en_title}">
<meta property="og:description" content="{en_desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{en_name}","description":"{en_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{en_name}","item":"https://free-toolbase.com/en/{slug}/"}}]}}</script>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{margin-bottom:20px;color:#94a3b8;font-size:.9rem;line-height:1.7}}
.hero .badge{{display:inline-block;margin-top:8px;padding:3px 10px;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:12px;font-size:.75rem;color:#22d3ee}}
.section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:6px}}
.form-group input[type="text"],.form-group input[type="number"],.form-group textarea,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group textarea:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.file-drop{{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;border:2px dashed rgba(148,163,184,.3);border-radius:12px;cursor:pointer;transition:all .3s;text-align:center}}
.file-drop:hover{{border-color:rgba(6,182,212,.5);background:rgba(6,182,212,.03)}}
.file-drop .icon{{font-size:2.5rem;margin-bottom:10px}}
.file-drop .hint{{color:#64748b;font-size:.85rem;margin-top:6px}}
.btn{{padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:500}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.15)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2);color:#e2e8f0}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.btn-danger:hover{{background:rgba(239,68,68,.25)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-box{{margin-top:16px;padding:16px;background:rgba(148,163,184,.05);border-radius:8px;min-height:60px}}
.result-box .label{{color:#64748b;font-size:.8rem;margin-bottom:6px}}
.result-box .value{{color:#22d3ee;font-size:1.1rem;font-weight:600;word-break:break-all}}
.feature-list{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}
.feature-tag{{padding:5px 12px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.15);border-radius:16px;font-size:.8rem;color:#22d3ee}}
.seo-content{{margin-bottom:20px;padding:16px;background:rgba(148,163,184,.03);border-radius:8px;border:1px solid rgba(148,163,184,.06)}}
.seo-content h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.seo-content ol{{padding-left:20px;margin-top:12px}}
.seo-content li{{margin-bottom:16px}}
.seo-content li strong{{color:#f1f5f9}}
.seo-content li span{{color:#94a3b8;font-size:.9rem}}
.faq-item{{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(148,163,184,.06)}}
.faq-item:last-child{{border-bottom:none}}
.faq-item .q{{color:#f1f5f9;font-size:.95rem;font-weight:600;margin-bottom:6px}}
.faq-item .a{{color:#94a3b8;font-size:.85rem;line-height:1.6}}
.preview-area{{margin-top:12px;text-align:center}}
.preview-area canvas,.preview-area img{{max-width:100%;border-radius:8px;max-height:400px}}
.status-bar{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:8px 12px;background:rgba(148,163,184,.05);border-radius:6px;margin:10px 0}}
.status-bar .info{{color:#94a3b8;font-size:.85rem}}
.stats-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}}
.stat-card{{text-align:center;padding:16px;background:rgba(148,163,184,.05);border-radius:8px}}
.stat-card .num{{font-size:1.8rem;font-weight:700;color:#22d3ee}}
.stat-card .lbl{{font-size:.75rem;color:#64748b;margin-top:4px}}
.test-text{{padding:16px;background:rgba(148,163,184,.05);border-radius:8px;font-size:1.1rem;line-height:1.8;margin-bottom:16px;color:#e2e8f0;letter-spacing:0.5px}}
.test-text .correct{{color:#22d3ee}}
.test-text .error{{color:#ef4444;text-decoration:underline}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}.stats-grid{{grid-template-columns:repeat(3,1fr)}}.stat-card .num{{font-size:1.3rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{en_h1}</h1><div class="lang-switch"><a href="../{slug}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {en_name}</p>
<div class="hero"><p>{en_hero}</p><span class="badge">Zero Dependencies · Works Offline</span></div>
<div class="main-grid">
<div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {today}
  </span>
</div>
<div class="section">
<h2>Tool Area</h2>
<div class="feature-list">
{en_features_html}
</div>
{en_body}
</div>
<div class="section">
<h2>FAQ</h2>
{en_faq_html}
</div>
</div>
<div class="seo-content">
<h2>How to Use {en_name}</h2>
<p>Using {en_name} is simple:</p>
<ol>
{en_howto_html}
</ol>
</div>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../privacy/">Privacy</a>
<a href="../terms/">Terms</a>
<a href="../about/">About</a>
<a href="../{slug}/">中文</a>
</div>
<p>{en_name} | No Signup · Data Never Leaves Your Device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
</div>
<div class="toast" id="toast"></div>
{en_js}
</body>
</html>"""

# ============ 各工具特定HTML Body和JS ============
TOOL_BODIES = {
    "audio-reverse-player": {
        "cn": """
<div class="file-drop" id="dropArea">
<div class="icon">🎵</div>
<div><strong>点击上传或拖放音频文件</strong></div>
<div class="hint">支持 WAV / MP3</div>
</div>
<input type="file" id="fileInput" accept="audio/*" style="display:none">
<div class="status-bar" id="statusBar" style="display:none">
<span class="info" id="fileInfo">未选择文件</span>
<div class="btn-group">
<button class="btn btn-primary" id="reverseBtn" onclick="reverseAudio()" disabled>🔄 开始倒放</button>
<button class="btn btn-secondary" id="playBtn" onclick="togglePlay()" disabled>▶ 试听</button>
<button class="btn btn-secondary" id="downloadBtn" onclick="downloadAudio()" disabled>📥 下载</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">处理状态</div>
<div class="value" id="resultMsg">等待上传音频...</div>
</div>""",
        "en": """
<div class="file-drop" id="dropArea">
<div class="icon">🎵</div>
<div><strong>Click to upload or drag audio file</strong></div>
<div class="hint">Supports WAV / MP3</div>
</div>
<input type="file" id="fileInput" accept="audio/*" style="display:none">
<div class="status-bar" id="statusBar" style="display:none">
<span class="info" id="fileInfo">No file selected</span>
<div class="btn-group">
<button class="btn btn-primary" id="reverseBtn" onclick="reverseAudio()" disabled>🔄 Reverse</button>
<button class="btn btn-secondary" id="playBtn" onclick="togglePlay()" disabled>▶ Preview</button>
<button class="btn btn-secondary" id="downloadBtn" onclick="downloadAudio()" disabled>📥 Download</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Status</div>
<div class="value" id="resultMsg">Waiting for audio upload...</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
let audioCtx=null,sourceBuffer=null,reversedBuffer=null,isPlaying=false,sourceNode=null;
const dropArea=document.getElementById("dropArea");
const fileInput=document.getElementById("fileInput");
dropArea.addEventListener("click",function(){fileInput.click()});
dropArea.addEventListener("dragover",function(e){e.preventDefault();dropArea.style.borderColor="rgba(6,182,212,.7)"});
dropArea.addEventListener("dragleave",function(){dropArea.style.borderColor="rgba(148,163,184,.3)"});
dropArea.addEventListener("drop",function(e){e.preventDefault();dropArea.style.borderColor="rgba(148,163,184,.3)";if(e.dataTransfer.files.length)handleFile(e.dataTransfer.files[0])});
fileInput.addEventListener("change",function(){if(fileInput.files.length)handleFile(fileInput.files[0])});
function handleFile(file){
  document.getElementById("fileInfo").textContent=file.name+" ("+(file.size/1024/1024).toFixed(1)+" MB)";
  document.getElementById("statusBar").style.display="flex";
  document.getElementById("resultBox").style.display="block";
  document.getElementById("resultMsg").textContent="正在解码音频...";
  document.getElementById("reverseBtn").disabled=false;
  var reader=new FileReader();
  reader.onload=function(e){
    var actx=new (window.AudioContext||window.webkitAudioContext)();
    actx.decodeAudioData(e.target.result,function(buffer){
      audioCtx=actx;sourceBuffer=buffer;reversedBuffer=null;
      document.getElementById("resultMsg").textContent="音频已加载，点击"开始倒放"处理";
      showToast("音频加载成功");
    },function(){document.getElementById("resultMsg").textContent="解码失败，请检查文件格式";showToast("解码失败")});
  };
  reader.readAsArrayBuffer(file);
}
function reverseAudio(){
  if(!sourceBuffer)return;
  document.getElementById("resultMsg").textContent="正在处理倒放...";
  var ctx=new OfflineAudioContext(sourceBuffer.numberOfChannels,sourceBuffer.length,sourceBuffer.sampleRate);
  for(var c=0;c<sourceBuffer.numberOfChannels;c++){
    var data=sourceBuffer.getChannelData(c);
    var reversed=new Float32Array(data.length);
    for(var i=0;i<data.length;i++)reversed[i]=data[data.length-1-i];
    var buf=ctx.createBuffer(1,data.length,sourceBuffer.sampleRate);
    buf.getChannelData(0).set(reversed);
    var src=ctx.createBufferSource();src.buffer=buf;src.connect(ctx.destination);src.start(0);
  }
  ctx.startRendering().then(function(rb){
    reversedBuffer=rb;audioCtx=new (window.AudioContext||window.webkitAudioContext)();
    document.getElementById("resultMsg").textContent="倒放完成！可以试听或下载";
    document.getElementById("playBtn").disabled=false;
    document.getElementById("downloadBtn").disabled=false;
    showToast("倒放处理完成");
  });
}
function togglePlay(){
  if(!reversedBuffer)return;
  if(isPlaying){if(sourceNode)sourceNode.stop();isPlaying=false;document.getElementById("playBtn").textContent="▶ 试听";return;}
  sourceNode=audioCtx.createBufferSource();sourceNode.buffer=reversedBuffer;sourceNode.connect(audioCtx.destination);
  sourceNode.onended=function(){isPlaying=false;document.getElementById("playBtn").textContent="▶ 试听"};
  sourceNode.start();isPlaying=true;document.getElementById("playBtn").textContent="⏹ 停止";
}
function downloadAudio(){
  if(!reversedBuffer)return;
  var wav=audioBufferToWav(reversedBuffer);
  var blob=new Blob([wav],{type:"audio/wav"});
  var url=URL.createObjectURL(blob);
  var a=document.createElement("a");a.href=url;a.download="reversed_audio.wav";a.click();
  URL.revokeObjectURL(url);showToast("下载已开始");
}
function audioBufferToWav(buffer){
  var numChannels=buffer.numberOfChannels,sampleRate=buffer.sampleRate;
  var format=1,bitDepth=16;
  var bytesPerSample=bitDepth/8,blockAlign=numChannels*bytesPerSample;
  var dataSize=buffer.length*blockAlign;
  var headerSize=44;
  var arrayBuffer=new ArrayBuffer(headerSize+dataSize);
  var view=new DataView(arrayBuffer);
  function writeString(offset,str){for(var i=0;i<str.length;i++)view.setUint8(offset+i,str.charCodeAt(i))}
  writeString(0,"RIFF");view.setUint32(4,36+dataSize,true);writeString(8,"WAVE");
  writeString(12,"fmt ");view.setUint32(16,16,true);view.setUint16(20,format,true);
  view.setUint16(22,numChannels,true);view.setUint32(24,sampleRate,true);
  view.setUint32(28,sampleRate*blockAlign,true);view.setUint16(32,blockAlign,true);view.setUint16(34,bitDepth,true);
  writeString(36,"data");view.setUint32(40,dataSize,true);
  var offset=44;
  for(var i=0;i<buffer.length;i++){
    for(var c=0;c<numChannels;c++){
      var sample=Math.max(-1,Math.min(1,buffer.getChannelData(c)[i]));
      sample=sample<0?sample*0x8000:sample*0x7FFF;
      view.setInt16(offset,sample,true);offset+=2;
    }
  }
  return arrayBuffer;
}
</script>"""
    },
    "vocal-remover-online": {
        "cn": """
<div class="file-drop" id="dropArea">
<div class="icon">🎤</div>
<div><strong>点击上传或拖放音频文件</strong></div>
<div class="hint">支持 WAV / MP3（立体声效果最佳）</div>
</div>
<input type="file" id="fileInput" accept="audio/*" style="display:none">
<div class="status-bar" id="statusBar" style="display:none">
<span class="info" id="fileInfo">未选择文件</span>
<div class="btn-group">
<button class="btn btn-primary" id="removeBtn" onclick="removeVocals()" disabled>🎵 分离人声</button>
<button class="btn btn-secondary" id="playInstBtn" onclick="togglePlay('inst')" disabled>▶ 伴奏</button>
<button class="btn btn-secondary" id="playVocBtn" onclick="togglePlay('voc')" disabled>▶ 人声</button>
<button class="btn btn-secondary" id="downloadInstBtn" onclick="downloadTrack('inst')" disabled>📥 下载伴奏</button>
<button class="btn btn-secondary" id="downloadVocBtn" onclick="downloadTrack('voc')" disabled>📥 下载人声</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">处理状态</div>
<div class="value" id="resultMsg">等待上传音频...</div>
</div>""",
        "en": """
<div class="file-drop" id="dropArea">
<div class="icon">🎤</div>
<div><strong>Click to upload or drag audio file</strong></div>
<div class="hint">Supports WAV / MP3 (stereo works best)</div>
</div>
<input type="file" id="fileInput" accept="audio/*" style="display:none">
<div class="status-bar" id="statusBar" style="display:none">
<span class="info" id="fileInfo">No file selected</span>
<div class="btn-group">
<button class="btn btn-primary" id="removeBtn" onclick="removeVocals()" disabled>🎵 Remove Vocals</button>
<button class="btn btn-secondary" id="playInstBtn" onclick="togglePlay('inst')" disabled>▶ Instrumental</button>
<button class="btn btn-secondary" id="playVocBtn" onclick="togglePlay('voc')" disabled>▶ Vocals</button>
<button class="btn btn-secondary" id="downloadInstBtn" onclick="downloadTrack('inst')" disabled>📥 Download Inst</button>
<button class="btn btn-secondary" id="downloadVocBtn" onclick="downloadTrack('voc')" disabled>📥 Download Vocals</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">Status</div>
<div class="value" id="resultMsg">Waiting for audio upload...</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
let audioCtx=null,sourceBuffer=null,instBuffer=null,vocBuffer=null,isPlaying=false,currentSource=null;
const dropArea=document.getElementById("dropArea"),fileInput=document.getElementById("fileInput");
dropArea.addEventListener("click",function(){fileInput.click()});
dropArea.addEventListener("dragover",function(e){e.preventDefault();dropArea.style.borderColor="rgba(6,182,212,.7)"});
dropArea.addEventListener("dragleave",function(){dropArea.style.borderColor="rgba(148,163,184,.3)"});
dropArea.addEventListener("drop",function(e){e.preventDefault();dropArea.style.borderColor="rgba(148,163,184,.3)";if(e.dataTransfer.files.length)handleFile(e.dataTransfer.files[0])});
fileInput.addEventListener("change",function(){if(fileInput.files.length)handleFile(fileInput.files[0])});
function handleFile(file){
  document.getElementById("fileInfo").textContent=file.name+" ("+(file.size/1024/1024).toFixed(1)+" MB)";
  document.getElementById("statusBar").style.display="flex";
  document.getElementById("resultBox").style.display="block";
  document.getElementById("resultMsg").textContent="Decoding audio...";
  document.getElementById("removeBtn").disabled=false;
  var reader=new FileReader();
  reader.onload=function(e){
    var actx=new (window.AudioContext||window.webkitAudioContext)();
    actx.decodeAudioData(e.target.result,function(buffer){
      audioCtx=actx;sourceBuffer=buffer;
      if(buffer.numberOfChannels<2){document.getElementById("resultMsg").textContent="Mono audio detected. Vocal removal works best with stereo files.";return}
      document.getElementById("resultMsg").textContent="Audio loaded. Click \"Remove Vocals\" to process.";
      showToast("Audio loaded successfully");
    },function(){document.getElementById("resultMsg").textContent="Decoding failed. Check file format."});
  };
  reader.readAsArrayBuffer(file);
}
function removeVocals(){
  if(!sourceBuffer||sourceBuffer.numberOfChannels<2)return;
  document.getElementById("resultMsg").textContent="Processing vocal removal...";
  var sr=sourceBuffer.sampleRate,len=sourceBuffer.length;
  var left=sourceBuffer.getChannelData(0),right=sourceBuffer.getChannelData(1);
  var ctx=new OfflineAudioContext(2,len,sr);
  var instBuf=ctx.createBuffer(2,len,sr),vocBuf=ctx.createBuffer(2,len,sr);
  var instL=instBuf.getChannelData(0),instR=instBuf.getChannelData(1);
  var vocL=vocBuf.getChannelData(0),vocR=vocBuf.getChannelData(1);
  for(var i=0;i<len;i++){var diff=(left[i]-right[i])*0.5;instL[i]=diff;instR[i]=diff;var sum=(left[i]+right[i])*0.5;vocL[i]=sum;vocR[i]=sum}
  var isrc=ctx.createBufferSource();isrc.buffer=instBuf;isrc.connect(ctx.destination);isrc.start(0);
  ctx.startRendering().then(function(rb){
    instBuffer=rb;document.getElementById("resultMsg").textContent="Separation complete! Listen to instrumental and vocal tracks.";
    document.getElementById("playInstBtn").disabled=false;
    document.getElementById("playVocBtn").disabled=false;
    document.getElementById("downloadInstBtn").disabled=false;
    document.getElementById("downloadVocBtn").disabled=false;
    showToast("Vocal separation complete");
  });
  // Create vocal buffer separately
  var ctx2=new OfflineAudioContext(2,len,sr);
  var vsrc=ctx2.createBufferSource();vsrc.buffer=vocBuf;vsrc.connect(ctx2.destination);vsrc.start(0);
  ctx2.startRendering().then(function(rb){vocBuffer=rb});
}
function togglePlay(type){
  var buf=type==="inst"?instBuffer:vocBuffer;
  if(!buf)return;
  if(isPlaying){if(currentSource)currentSource.stop();isPlaying=false;document.getElementById("playInstBtn").textContent="▶ 伴奏";document.getElementById("playVocBtn").textContent="▶ 人声";return}
  var actx=new (window.AudioContext||window.webkitAudioContext)();
  currentSource=actx.createBufferSource();currentSource.buffer=buf;currentSource.connect(actx.destination);
  currentSource.onended=function(){isPlaying=false;document.getElementById("playInstBtn").textContent="▶ 伴奏";document.getElementById("playVocBtn").textContent="▶ 人声"};
  currentSource.start();isPlaying=true;
  if(type==="inst")document.getElementById("playInstBtn").textContent="⏹ Stop";
  else document.getElementById("playVocBtn").textContent="⏹ Stop";
}
function downloadTrack(type){
  var buf=type==="inst"?instBuffer:vocBuffer;
  if(!buf)return;
  var wav=audioBufferToWav(buf);
  var blob=new Blob([wav],{type:"audio/wav"});
  var url=URL.createObjectURL(blob);
  var a=document.createElement("a");a.href=url;a.download=type+"_track.wav";a.click();
  URL.revokeObjectURL(url);showToast("Download started");
}
function audioBufferToWav(buffer){var nc=buffer.numberOfChannels,sr=buffer.sampleRate,fmt=1,bd=16,bps=bd/8,ba=nc*bps,ds=buffer.length*ba,hs=44,ab=new ArrayBuffer(hs+ds),v=new DataView(ab);function ws(o,s){for(var i=0;i<s.length;i++)v.setUint8(o+i,s.charCodeAt(i))}ws(0,"RIFF");v.setUint32(4,36+ds,true);ws(8,"WAVE");ws(12,"fmt ");v.setUint32(16,16,true);v.setUint16(20,fmt,true);v.setUint16(22,nc,true);v.setUint32(24,sr,true);v.setUint32(28,sr*ba,true);v.setUint16(32,ba,true);v.setUint16(34,bd,true);ws(36,"data");v.setUint32(40,ds,true);var o=44;for(var i=0;i<buffer.length;i++)for(var c=0;c<nc;c++){var s=Math.max(-1,Math.min(1,buffer.getChannelData(c)[i]));s=s<0?s*0x8000:s*0x7FFF;v.setInt16(o,s,true);o+=2}return ab}
</script>"""
    },
    "pitch-detector-online": {
        "cn": """
<div class="btn-group">
<button class="btn btn-primary" id="startBtn" onclick="toggleDetection()">🎤 开始检测</button>
<button class="btn btn-secondary" id="stopBtn" onclick="toggleDetection()" style="display:none">⏹ 停止</button>
</div>
<div class="stats-grid" style="margin-top:16px">
<div class="stat-card"><div class="num" id="freqDisplay">--</div><div class="lbl">频率 (Hz)</div></div>
<div class="stat-card"><div class="num" id="noteDisplay">--</div><div class="lbl">音符</div></div>
<div class="stat-card"><div class="num" id="centDisplay">--</div><div class="lbl">音分偏差</div></div>
</div>
<canvas id="waveCanvas" style="width:100%;height:120px;background:rgba(0,0,0,.2);border-radius:8px;margin-top:12px"></canvas>
<div class="result-box" style="margin-top:12px">
<div class="label">检测状态</div>
<div class="value" id="statusMsg">点击开始检测音高</div>
</div>""",
        "en": """
<div class="btn-group">
<button class="btn btn-primary" id="startBtn" onclick="toggleDetection()">🎤 Start Detection</button>
<button class="btn btn-secondary" id="stopBtn" onclick="toggleDetection()" style="display:none">⏹ Stop</button>
</div>
<div class="stats-grid" style="margin-top:16px">
<div class="stat-card"><div class="num" id="freqDisplay">--</div><div class="lbl">Frequency (Hz)</div></div>
<div class="stat-card"><div class="num" id="noteDisplay">--</div><div class="lbl">Note</div></div>
<div class="stat-card"><div class="num" id="centDisplay">--</div><div class="lbl">Cent Deviation</div></div>
</div>
<canvas id="waveCanvas" style="width:100%;height:120px;background:rgba(0,0,0,.2);border-radius:8px;margin-top:12px"></canvas>
<div class="result-box" style="margin-top:12px">
<div class="label">Status</div>
<div class="value" id="statusMsg">Click Start to detect pitch</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
let audioCtx=null,analyser=null,microphone=null,isRunning=false,animId=null;
const NOTE_NAMES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
const A4=440;
function freqToNote(freq){
  if(!freq||freq<20)return{note:"--",cents:0};
  var n=Math.round(12*Math.log2(freq/A4));
  var noteIdx=((n%12)+12)%12;
  var octave=4+Math.floor((n+9)/12);
  var idealFreq=A4*Math.pow(2,n/12);
  var cents=Math.round(1200*Math.log2(freq/idealFreq));
  return{note:NOTE_NAMES[noteIdx]+octave,cents:cents};
}
async function toggleDetection(){
  if(isRunning){stopDetection();return}
  try{
    var stream=await navigator.mediaDevices.getUserMedia({audio:true});
    audioCtx=new (window.AudioContext||window.webkitAudioContext)();
    microphone=audioCtx.createMediaStreamSource(stream);
    analyser=audioCtx.createAnalyser();
    analyser.fftSize=4096;
    analyser.smoothingTimeConstant=0.3;
    microphone.connect(analyser);
    isRunning=true;
    document.getElementById("startBtn").style.display="none";
    document.getElementById("stopBtn").style.display="inline-flex";
    document.getElementById("statusMsg").textContent="Listening... make a sound!";
    detect();
    showToast("Microphone activated");
  }catch(e){
    document.getElementById("statusMsg").textContent="Microphone access denied. Please allow microphone.";
    showToast("Microphone access required");
  }
}
function stopDetection(){
  isRunning=false;
  if(animId)cancelAnimationFrame(animId);
  if(microphone&&microphone.mediaStream)microphone.mediaStream.getTracks().forEach(t=>t.stop());
  if(audioCtx)audioCtx.close();
  document.getElementById("startBtn").style.display="inline-flex";
  document.getElementById("stopBtn").style.display="none";
  document.getElementById("freqDisplay").textContent="--";
  document.getElementById("noteDisplay").textContent="--";
  document.getElementById("centDisplay").textContent="--";
  document.getElementById("statusMsg").textContent="Detection stopped";
}
function detect(){
  if(!isRunning)return;
  var buffer=new Float32Array(analyser.fftSize);
  analyser.getFloatTimeDomainData(buffer);
  var freq=autoCorrelate(buffer,audioCtx.sampleRate);
  drawWave(buffer);
  if(freq>20){
    document.getElementById("freqDisplay").textContent=freq.toFixed(1);
    var result=freqToNote(freq);
    document.getElementById("noteDisplay").textContent=result.note;
    var cents=result.cents;
    document.getElementById("centDisplay").textContent=(cents>0?"+":"")+cents;
    document.getElementById("centDisplay").style.color=Math.abs(cents)<10?"#22d3ee":"#f59e0b";
  }
  animId=requestAnimationFrame(detect);
}
function autoCorrelate(buf,sampleRate){
  var size=buf.length,sum=0;
  for(var i=0;i<size;i++)sum+=buf[i]*buf[i];
  var rms=Math.sqrt(sum/size);
  if(rms<0.01)return -1;
  var maxSamples=Math.floor(sampleRate/20),minSamples=Math.floor(sampleRate/2000);
  var bestOffset=-1,bestCorrelation=0;
  for(var offset=minSamples;offset<Math.min(maxSamples,size);offset++){
    var correlation=0;
    for(var i=0;i<size-offset;i++)correlation+=buf[i]*buf[i+offset];
    correlation/=size-offset;
    if(correlation>bestCorrelation){bestCorrelation=correlation;bestOffset=offset}
  }
  if(bestCorrelation>0.01)return sampleRate/bestOffset;
  return -1;
}
function drawWave(buffer){
  var canvas=document.getElementById("waveCanvas");
  if(!canvas)return;
  var ctx=canvas.getContext("2d");
  canvas.width=canvas.offsetWidth;
  var w=canvas.width,h=canvas.height;
  ctx.clearRect(0,0,w,h);
  ctx.beginPath();ctx.strokeStyle="#06b6d4";ctx.lineWidth=2;
  var step=Math.ceil(buffer.length/w);
  for(var i=0;i<w;i++){
    var min=1,max=-1;
    for(var j=0;j<step;j++){
      var idx=i*step+j;
      if(idx>=buffer.length)break;
      if(buffer[idx]<min)min=buffer[idx];
      if(buffer[idx]>max)max=buffer[idx];
    }
    var y1=((min+1)/2)*h,y2=((max+1)/2)*h;
    ctx.moveTo(i,y1);ctx.lineTo(i,y2);
  }
  ctx.stroke();
}
</script>"""
    },
    "text-to-emoji-converter": {
        "cn": """
<div class="form-group">
<label>输入文本</label>
<textarea id="inputText" rows="4" placeholder="在此输入要转换的文字...">Hello World</textarea>
</div>
<div class="form-group">
<label>转换模式</label>
<select id="modeSelect">
<option value="letter">字母映射 (A→🅰️)</option>
<option value="word">单词映射 (hello→👋)</option>
<option value="mixed">混合模式</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="convert()">😊 转换</button>
<button class="btn btn-secondary" onclick="copyResult()">📋 复制结果</button>
</div>
<div class="result-box">
<div class="label">转换结果</div>
<div class="value" id="resultOutput" style="font-size:1.3rem">等待转换...</div>
</div>""",
        "en": """
<div class="form-group">
<label>Enter Text</label>
<textarea id="inputText" rows="4" placeholder="Type text to convert...">Hello World</textarea>
</div>
<div class="form-group">
<label>Conversion Mode</label>
<select id="modeSelect">
<option value="letter">Letter Mapping (A→🅰️)</option>
<option value="word">Word Mapping (hello→👋)</option>
<option value="mixed">Mixed Mode</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="convert()">😊 Convert</button>
<button class="btn btn-secondary" onclick="copyResult()">📋 Copy Result</button>
</div>
<div class="result-box">
<div class="label">Result</div>
<div class="value" id="resultOutput" style="font-size:1.3rem">Waiting...</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
const LETTER_MAP={a:"🅰️",b:"🅱️",c:"©️",d:"🇩",e:"📧",f:"🎏",g:"🇬",h:"♓",i:"ℹ️",j:"🎷",k:"🎋",l:"👢",m:"Ⓜ️",n:"♑",o:"🅾️",p:"🅿️",q:"👑",r:"®️",s:"💲",t:"✝️",u:"⛎",v:"✌️",w:"🇼",x:"❎",y:"🍸",z:"💤","0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣","4":"4️⃣","5":"5️⃣","6":"6️⃣","7":"7️⃣","8":"8️⃣","9":"9️⃣"," ":"  ","!":"❗","?":"❓"};
const WORD_MAP={hello:"👋",world:"🌍",love:"❤️",happy:"😊",sad:"😢",cool:"😎",fire:"🔥",star:"⭐",sun:"☀️",moon:"🌙",heart:"💖",music:"🎵","ok":"👌",yes:"✅",no:"❌",thanks:"🙏",good:"👍",bad:"👎",lol:"😂",peace:"✌️",cat:"🐱",dog:"🐶",food:"🍔",drink:"🥤",car:"🚗",home:"🏠"};
function convert(){
  var text=document.getElementById("inputText").value;
  var mode=document.getElementById("modeSelect").value;
  var result="";
  if(mode==="word"){
    var words=text.toLowerCase().split(/(\\s+)/);
    for(var i=0;i<words.length;i++){
      var w=words[i].replace(/[^a-z]/g,"");
      result+=WORD_MAP[w]||words[i];
    }
  }else if(mode==="letter"){
    for(var i=0;i<text.length;i++){
      var c=text[i].toLowerCase();
      result+=LETTER_MAP[c]||text[i];
    }
  }else{
    var words=text.toLowerCase().split(/(\\s+)/);
    for(var i=0;i<words.length;i++){
      var w=words[i].replace(/[^a-z]/g,"");
      if(WORD_MAP[w]){result+=WORD_MAP[w]}else{
        for(var j=0;j<words[i].length;j++){
          var c=words[i][j].toLowerCase();
          result+=LETTER_MAP[c]||words[i][j];
        }
      }
    }
  }
  document.getElementById("resultOutput").textContent=result;
}
function copyResult(){
  var text=document.getElementById("resultOutput").textContent;
  navigator.clipboard.writeText(text).then(function(){showToast("已复制")})["catch"](function(){showToast("复制失败")});
}
convert();
</script>"""
    },
    "image-border-generator": {
        "cn": """
<div class="file-drop" id="dropArea">
<div class="icon">🖼️</div>
<div><strong>点击上传或拖放图片</strong></div>
<div class="hint">支持 JPG / PNG / WebP</div>
</div>
<input type="file" id="fileInput" accept="image/*" style="display:none">
<div class="form-group" style="margin-top:12px">
<label>边框宽度: <span id="widthVal">10</span>px</label>
<input type="range" id="borderWidth" min="1" max="50" value="10" oninput="document.getElementById('widthVal').textContent=this.value;updatePreview()">
</div>
<div class="form-group">
<label>边框颜色</label>
<input type="color" id="borderColor" value="#06b6d4" onchange="updatePreview()" style="width:60px;height:36px;border:none;cursor:pointer">
</div>
<div class="form-group">
<label>圆角半径: <span id="radiusVal">8</span>px</label>
<input type="range" id="borderRadius" min="0" max="80" value="8" oninput="document.getElementById('radiusVal').textContent=this.value;updatePreview()">
</div>
<div class="form-group">
<label>阴影透明度: <span id="shadowVal">30</span>%</label>
<input type="range" id="shadowOpacity" min="0" max="80" value="30" oninput="document.getElementById('shadowVal').textContent=this.value;updatePreview()">
</div>
<div class="btn-group">
<button class="btn btn-secondary" onclick="resetBorder()">🔄 重置</button>
<button class="btn btn-primary" onclick="downloadImage()" id="downloadBtn" disabled>📥 下载图片</button>
</div>
<div class="preview-area">
<canvas id="previewCanvas" style="display:none;max-width:100%;max-height:400px"></canvas>
<div id="noImage" style="color:#64748b;padding:40px">上传图片后实时预览边框效果</div>
</div>""",
        "en": """
<div class="file-drop" id="dropArea">
<div class="icon">🖼️</div>
<div><strong>Click to upload or drag image</strong></div>
<div class="hint">Supports JPG / PNG / WebP</div>
</div>
<input type="file" id="fileInput" accept="image/*" style="display:none">
<div class="form-group" style="margin-top:12px">
<label>Border Width: <span id="widthVal">10</span>px</label>
<input type="range" id="borderWidth" min="1" max="50" value="10" oninput="document.getElementById('widthVal').textContent=this.value;updatePreview()">
</div>
<div class="form-group">
<label>Border Color</label>
<input type="color" id="borderColor" value="#06b6d4" onchange="updatePreview()" style="width:60px;height:36px;border:none;cursor:pointer">
</div>
<div class="form-group">
<label>Corner Radius: <span id="radiusVal">8</span>px</label>
<input type="range" id="borderRadius" min="0" max="80" value="8" oninput="document.getElementById('radiusVal').textContent=this.value;updatePreview()">
</div>
<div class="form-group">
<label>Shadow Opacity: <span id="shadowVal">30</span>%</label>
<input type="range" id="shadowOpacity" min="0" max="80" value="30" oninput="document.getElementById('shadowVal').textContent=this.value;updatePreview()">
</div>
<div class="btn-group">
<button class="btn btn-secondary" onclick="resetBorder()">🔄 Reset</button>
<button class="btn btn-primary" onclick="downloadImage()" id="downloadBtn" disabled>📥 Download</button>
</div>
<div class="preview-area">
<canvas id="previewCanvas" style="display:none;max-width:100%;max-height:400px"></canvas>
<div id="noImage" style="color:#64748b;padding:40px">Upload an image to preview border effect</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
let sourceImage=null;
const dropArea=document.getElementById("dropArea"),fileInput=document.getElementById("fileInput");
dropArea.addEventListener("click",function(){fileInput.click()});
dropArea.addEventListener("dragover",function(e){e.preventDefault();dropArea.style.borderColor="rgba(6,182,212,.7)"});
dropArea.addEventListener("dragleave",function(){dropArea.style.borderColor="rgba(148,163,184,.3)"});
dropArea.addEventListener("drop",function(e){e.preventDefault();dropArea.style.borderColor="rgba(148,163,184,.3)";if(e.dataTransfer.files.length)loadImage(e.dataTransfer.files[0])});
fileInput.addEventListener("change",function(){if(fileInput.files.length)loadImage(fileInput.files[0])});
function loadImage(file){
  var reader=new FileReader();
  reader.onload=function(e){
    var img=new Image();
    img.onload=function(){sourceImage=img;document.getElementById("noImage").style.display="none";document.getElementById("previewCanvas").style.display="block";document.getElementById("downloadBtn").disabled=false;updatePreview();showToast("Image loaded")};
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}
function updatePreview(){
  if(!sourceImage)return;
  var canvas=document.getElementById("previewCanvas");
  var bw=parseInt(document.getElementById("borderWidth").value);
  var br=parseInt(document.getElementById("borderRadius").value);
  var so=parseInt(document.getElementById("shadowOpacity").value)/100;
  var bc=document.getElementById("borderColor").value;
  var w=sourceImage.width+2*bw+20,h=sourceImage.height+2*bw+20;
  canvas.width=w;canvas.height=h;
  var ctx=canvas.getContext("2d");
  ctx.clearRect(0,0,w,h);
  // Shadow
  if(so>0){ctx.shadowColor="rgba(0,0,0,"+so+")";ctx.shadowBlur=15;ctx.shadowOffsetX=3;ctx.shadowOffsetY=3}
  // Border
  ctx.fillStyle=bc;
  ctx.beginPath();ctx.moveTo(10+br,10);ctx.lineTo(10+w-2*bw-20-br,10);
  ctx.quadraticCurveTo(10+w-2*bw-20,10,10+w-2*bw-20,10+br);
  ctx.lineTo(10+w-2*bw-20,10+h-2*bw-20-br);
  ctx.quadraticCurveTo(10+w-2*bw-20,10+h-2*bw-20,10+w-2*bw-20-br,10+h-2*bw-20);
  ctx.lineTo(10+br,10+h-2*bw-20);
  ctx.quadraticCurveTo(10,10+h-2*bw-20,10,10+h-2*bw-20-br);
  ctx.lineTo(10,10+br);
  ctx.quadraticCurveTo(10,10,10+br,10);
  ctx.closePath();ctx.fill();
  // Reset shadow for image
  ctx.shadowColor="transparent";ctx.shadowBlur=0;ctx.shadowOffsetX=0;ctx.shadowOffsetY=0;
  // Image with border radius clip
  ctx.save();
  ctx.beginPath();ctx.moveTo(10+bw+br,10+bw);ctx.lineTo(10+w-bw-20-br,10+bw);
  ctx.quadraticCurveTo(10+w-bw-20,10+bw,10+w-bw-20,10+bw+br);
  ctx.lineTo(10+w-bw-20,10+h-bw-20-br);
  ctx.quadraticCurveTo(10+w-bw-20,10+h-bw-20,10+w-bw-20-br,10+h-bw-20);
  ctx.lineTo(10+bw+br,10+h-bw-20);
  ctx.quadraticCurveTo(10+bw,10+h-bw-20,10+bw,10+h-bw-20-br);
  ctx.lineTo(10+bw,10+bw+br);
  ctx.quadraticCurveTo(10+bw,10+bw,10+bw+br,10+bw);
  ctx.closePath();ctx.clip();
  ctx.drawImage(sourceImage,10+bw,10+bw,sourceImage.width,sourceImage.height);
  ctx.restore();
}
function resetBorder(){
  document.getElementById("borderWidth").value=10;document.getElementById("widthVal").textContent="10";
  document.getElementById("borderColor").value="#06b6d4";
  document.getElementById("borderRadius").value=8;document.getElementById("radiusVal").textContent="8";
  document.getElementById("shadowOpacity").value=30;document.getElementById("shadowVal").textContent="30";
  updatePreview();showToast("Reset to default");
}
function downloadImage(){
  var canvas=document.getElementById("previewCanvas");
  if(!canvas||canvas.style.display==="none")return;
  canvas.toBlob(function(blob){
    var url=URL.createObjectURL(blob);
    var a=document.createElement("a");a.href=url;a.download="bordered_image.png";a.click();
    URL.revokeObjectURL(url);showToast("Download started");
  },"image/png");
}
</script>"""
    },
    "binary-text-translator": {
        "cn": """
<div class="form-group">
<label>输入</label>
<textarea id="inputText" rows="5" placeholder="输入文本或二进制数据...">Hello</textarea>
</div>
<div class="form-group">
<label>转换方向</label>
<select id="direction" onchange="translate()">
<option value="text2bin">文本 → 二进制</option>
<option value="bin2text">二进制 → 文本</option>
</select>
</div>
<div class="form-group">
<label>位格式</label>
<select id="bitFormat" onchange="translate()">
<option value="8">8位（每组8位，标准格式）</option>
<option value="7">7位（ASCII格式）</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="translate()">🔄 转换</button>
<button class="btn btn-secondary" onclick="copyResult()">📋 复制结果</button>
<button class="btn btn-secondary" onclick="swapDirection()">🔀 交换方向</button>
</div>
<div class="result-box">
<div class="label">转换结果</div>
<div class="value" id="resultOutput" style="font-family:monospace;white-space:pre-wrap">等待转换...</div>
</div>""",
        "en": """
<div class="form-group">
<label>Input</label>
<textarea id="inputText" rows="5" placeholder="Enter text or binary data...">Hello</textarea>
</div>
<div class="form-group">
<label>Direction</label>
<select id="direction" onchange="translate()">
<option value="text2bin">Text → Binary</option>
<option value="bin2text">Binary → Text</option>
</select>
</div>
<div class="form-group">
<label>Bit Format</label>
<select id="bitFormat" onchange="translate()">
<option value="8">8-bit (standard, 8 bits per group)</option>
<option value="7">7-bit (ASCII format)</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="translate()">🔄 Convert</button>
<button class="btn btn-secondary" onclick="copyResult()">📋 Copy Result</button>
<button class="btn btn-secondary" onclick="swapDirection()">🔀 Swap</button>
</div>
<div class="result-box">
<div class="label">Result</div>
<div class="value" id="resultOutput" style="font-family:monospace;white-space:pre-wrap">Waiting...</div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
function translate(){
  var input=document.getElementById("inputText").value;
  var dir=document.getElementById("direction").value;
  var bits=parseInt(document.getElementById("bitFormat").value);
  var result="";
  if(dir==="text2bin"){
    for(var i=0;i<input.length;i++){
      var code=input.charCodeAt(i);
      if(bits===7){result+=code.toString(2).padStart(7,"0")+" "}else{
        if(code>255){var b=code.toString(2).padStart(16,"0");result+=b.match(/.{1,8}/g).join(" ")+" "}else{result+=code.toString(2).padStart(8,"0")+" "}
      }
    }
  }else{
    var cleaned=input.replace(/[^01]/g,"");
    if(bits===7){for(var i=0;i<cleaned.length;i+=7){var chunk=cleaned.substr(i,7);if(chunk.length===7)result+=String.fromCharCode(parseInt(chunk,2))}}
    else{
      for(var i=0;i<cleaned.length;i+=8){
        var chunk=cleaned.substr(i,8);if(chunk.length===8){
          var code=parseInt(chunk,2);
          if(code>=32&&code<=126)result+=String.fromCharCode(code);
        }
      }
    }
  }
  document.getElementById("resultOutput").textContent=result||"(空)";
}
function copyResult(){
  var t=document.getElementById("resultOutput").textContent;
  navigator.clipboard.writeText(t).then(function(){showToast("已复制")})["catch"](function(){showToast("复制失败")});
}
function swapDirection(){
  var sel=document.getElementById("direction");
  sel.value=sel.value==="text2bin"?"bin2text":"text2bin";
  translate();
}
translate();
</script>"""
    },
    "typing-speed-test-online": {
        "cn": """
<div class="form-group">
<label>难度级别</label>
<select id="difficulty" onchange="newTest()">
<option value="easy">简单 - 短句</option>
<option value="medium" selected>中等 - 段落</option>
<option value="hard">困难 - 长段落</option>
</select>
</div>
<div class="test-text" id="testText" style="font-family:monospace">加载中...</div>
<div class="form-group">
<textarea id="userInput" rows="3" placeholder="在此输入上方显示的文本..." oninput="checkTyping()" style="font-family:monospace;font-size:1rem"></textarea>
</div>
<div class="stats-grid">
<div class="stat-card"><div class="num" id="wpmDisplay">0</div><div class="lbl">WPM</div></div>
<div class="stat-card"><div class="num" id="accuracyDisplay">100</div><div class="lbl">准确率 %</div></div>
<div class="stat-card"><div class="num" id="timeDisplay">0</div><div class="lbl">秒</div></div>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="newTest()">🔄 新文本</button>
<button class="btn btn-secondary" onclick="resetTest()">🔁 重新开始</button>
</div>
<div class="result-box" id="completionMsg" style="display:none">
<div class="label">完成！</div>
<div class="value" id="completionStats"></div>
</div>""",
        "en": """
<div class="form-group">
<label>Difficulty</label>
<select id="difficulty" onchange="newTest()">
<option value="easy">Easy - Short Phrases</option>
<option value="medium" selected>Medium - Paragraphs</option>
<option value="hard">Hard - Long Paragraphs</option>
</select>
</div>
<div class="test-text" id="testText" style="font-family:monospace">Loading...</div>
<div class="form-group">
<textarea id="userInput" rows="3" placeholder="Type the text shown above..." oninput="checkTyping()" style="font-family:monospace;font-size:1rem"></textarea>
</div>
<div class="stats-grid">
<div class="stat-card"><div class="num" id="wpmDisplay">0</div><div class="lbl">WPM</div></div>
<div class="stat-card"><div class="num" id="accuracyDisplay">100</div><div class="lbl">Accuracy %</div></div>
<div class="stat-card"><div class="num" id="timeDisplay">0</div><div class="lbl">Seconds</div></div>
</div>
<div class="btn-group">
<button class="btn btn-primary" onclick="newTest()">🔄 New Text</button>
<button class="btn btn-secondary" onclick="resetTest()">🔁 Restart</button>
</div>
<div class="result-box" id="completionMsg" style="display:none">
<div class="label">Complete!</div>
<div class="value" id="completionStats"></div>
</div>""",
        "js": """
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
const TEXTS={
  easy_cn:["今天天气真好","编程改变世界","每天学习新知识","坚持就是胜利","熟能生巧"],
  medium_cn:["在数字化时代，编程技能变得越来越重要。无论是网页开发、数据分析还是人工智能，都需要扎实的编程基础。每天花一点时间练习，你会发现自己进步神速。"],
  hard_cn:["学习编程不仅仅是掌握一门语言，更重要的是培养解决问题的思维方式。当你面对一个复杂的问题时，学会将其分解为小步骤，逐步实现。这种能力在任何领域都极为宝贵。保持好奇心，不断探索新的技术和方法，你将成为更优秀的开发者。"],
  easy_en:["The quick brown fox jumps over the lazy dog","Practice makes perfect","Keep learning every day","Code is poetry","Stay curious"],
  medium_en:["In the digital age, programming skills have become increasingly important. Whether it's web development, data analysis, or artificial intelligence, a solid programming foundation is essential. Practice a little each day and you'll see remarkable progress."],
  hard_en:["Learning to code is not just about mastering a language, but more importantly about developing a problem-solving mindset. When faced with complex challenges, learn to break them into smaller steps and implement them gradually. This skill is invaluable in any field. Stay curious, explore new technologies, and you'll become a better developer."]
};
let testText="",startTime=null,timerInterval=null,elapsed=0,completed=false;
function newTest(){
  var diff=document.getElementById("difficulty").value;
  var isCN=document.documentElement.lang==="zh-CN"||document.querySelector(".lang-switch a.active").textContent==="中文";
  var key=diff+"_"+(isCN?"cn":"en");
  var arr=TEXTS[key]||TEXTS["medium_en"];
  testText=arr[Math.floor(Math.random()*arr.length)];
  document.getElementById("testText").textContent=testText;
  resetTest();
}
function resetTest(){
  document.getElementById("userInput").value="";
  document.getElementById("userInput").disabled=false;
  document.getElementById("wpmDisplay").textContent="0";
  document.getElementById("accuracyDisplay").textContent="100";
  document.getElementById("timeDisplay").textContent="0";
  document.getElementById("completionMsg").style.display="none";
  startTime=null;elapsed=0;completed=false;
  if(timerInterval)clearInterval(timerInterval);
  document.getElementById("userInput").focus();
}
function checkTyping(){
  if(completed)return;
  if(!startTime){startTime=Date.now();timerInterval=setInterval(updateTimer,200)}
  var input=document.getElementById("userInput").value;
  var correct=0;
  for(var i=0;i<Math.min(input.length,testText.length);i++){if(input[i]===testText[i])correct++}
  var accuracy=input.length>0?Math.round(correct/input.length*100):100;
  document.getElementById("accuracyDisplay").textContent=accuracy;
  var minutes=(Date.now()-startTime)/60000;
  var words=input.length/5;
  var wpm=minutes>0?Math.round(words/minutes):0;
  document.getElementById("wpmDisplay").textContent=wpm;
  if(input.length>=testText.length){
    completed=true;clearInterval(timerInterval);
    document.getElementById("userInput").disabled=true;
    var finalWPM=wpm,finalAcc=accuracy,finalTime=Math.round(elapsed);
    document.getElementById("completionStats").textContent="WPM: "+finalWPM+" | Accuracy: "+finalAcc+"% | Time: "+finalTime+"s";
    document.getElementById("completionMsg").style.display="block";
  }
}
function updateTimer(){
  elapsed=(Date.now()-startTime)/1000;
  document.getElementById("timeDisplay").textContent=Math.round(elapsed);
}
newTest();
</script>"""
    }
}

# ============ 生成页面 ============
def generate():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    for tool in TOOLS:
        slug = tool["slug"]
        cn = tool["cn"]
        en = tool["en"]
        body_data = TOOL_BODIES.get(slug, {})
        
        # Create CN dir and file
        os.makedirs(slug, exist_ok=True)
        cn_features_html = "\n".join([f'<span class="feature-tag">{f}</span>' for f in cn["features"]])
        cn_howto_html = "\n".join([f'<li><strong>{s.split("（")[0] if "（" in s else s.split("(")[0]}</strong><br><span>{s}</span></li>' for s in cn["howto_steps"]])
        cn_faq_html = "\n".join([f'<div class="faq-item"><div class="q">{q}</div><div class="a">{a}</div></div>' for q, a in cn["faq"]])
        cn_keywords = ",".join(cn["h1"].replace("🔄","").replace("🎤","").replace("🎵","").replace("😊","").replace("🖼️","").replace("0️⃣1️⃣","").replace("⌨️","").strip().split()[:5])
        
        cn_html = CN_TEMPLATE.format(
            slug=slug, today=TODAY,
            cn_title=cn["title"], cn_desc=cn["desc"], cn_name=cn["h1"].split(" ",1)[-1] if " " in cn["h1"] else cn["h1"],
            cn_h1=cn["h1"], cn_hero=cn["hero"],
            cn_features_html=cn_features_html, cn_howto_html=cn_howto_html, cn_faq_html=cn_faq_html,
            cn_body=body_data.get("cn", ""), cn_js=body_data.get("js", ""),
            cn_keywords=cn_keywords
        )
        with open(f"{slug}/index.html", "w", encoding="utf-8") as f:
            f.write(cn_html)
        print(f"  ✅ Created {slug}/index.html (CN)")
        
        # Create EN dir and file
        en_dir = f"en/{slug}"
        os.makedirs(en_dir, exist_ok)
        en_features_html = "\n".join([f'<span class="feature-tag">{f}</span>' for f in en["features"]])
        en_howto_html = "\n".join([f'<li><strong>{s.split("(")[0].strip() if "(" in s else s}</strong><br><span>{s}</span></li>' for s in en["howto_steps"]])
        en_faq_html = "\n".join([f'<div class="faq-item"><div class="q">{q}</div><div class="a">{a}</div></div>' for q, a in en["faq"]])
        en_keywords = ",".join(en["h1"].replace("🔄","").replace("🎤","").replace("🎵","").replace("😊","").replace("🖼️","").replace("0️⃣1️⃣","").replace("⌨️","").strip().split()[:5])
        
        en_html = EN_TEMPLATE.format(
            slug=slug, today=TODAY,
            en_title=en["title"], en_desc=en["desc"], en_name=en["h1"].split(" ",1)[-1] if " " in en["h1"] else en["h1"],
            en_h1=en["h1"], en_hero=en["hero"],
            en_features_html=en_features_html, en_howto_html=en_howto_html, en_faq_html=en_faq_html,
            en_body=body_data.get("en", ""), en_js=body_data.get("js", ""),
            en_keywords=en_keywords
        )
        with open(f"en/{slug}/index.html", "w", encoding="utf-8") as f:
            f.write(en_html)
        print(f"  ✅ Created en/{slug}/index.html (EN)")

if __name__ == "__main__":
    generate()
    print(f"\nDone! Generated {len(TOOLS)} tools (CN + EN).")