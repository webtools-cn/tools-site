#!/usr/bin/env python3
"""生成5个新工具的中英文页面"""
import os

BASE = os.path.expanduser("~/tools-site")
TODAY = "2026-07-12"

tools = {
    "webp-converter": {
        "icon": "🖼️",
        "cat": "image",
        "cat_name_cn": "图片工具",
        "cat_name_en": "Image Tools",
        "cn": {
            "title": "WebP格式转换器",
            "h1": "🖼️ WebP格式转换器",
            "desc": "免费在线WebP格式转换器，支持WebP与PNG、JPEG、GIF互转。拖放上传，批量转换，纯前端Canvas处理，图片不上传服务器。支持质量调节和透明度保留。",
            "keywords": "WebP转换,WebP转PNG,PNG转WebP,JPEG转WebP,在线WebP转换器,图片格式转换,WebP转JPEG",
            "software_name": "WebP格式转换器",
            "category": "MultimediaApplication",
            "faq": [
                {"q": "什么是WebP格式？", "a": "WebP是Google开发的现代图片格式，同时支持有损和无损压缩。相比JPEG和PNG，WebP文件通常小25-35%，同时保持相似的画质。绝大多数现代浏览器都支持WebP格式。"},
                {"q": "转换后图片质量会下降吗？", "a": "支持质量调节（1-100）。当质量为100时，转换几乎无损。建议WebP质量设为80-90，文件大小可减少30%以上同时肉眼难以分辨差异。如果转换回PNG/JPEG，请使用最高质量以保持原始品质。"},
                {"q": "支持批量转换吗？", "a": "支持！一次可拖放或选择多个图片文件（最多20个），工具会自动批量处理。每个转换完成后可单独下载，也可以一键打包下载全部结果。"},
                {"q": "转换后能保留透明度吗？", "a": "可以。WebP和PNG都支持透明度（Alpha通道）。当PNG带透明区域转WebP时，透明度会自动保留。JPEG格式不支持透明度，转JPEG时透明区域将变为白色。"},
            ],
            "howto_steps": [
                {"pos": 1, "name": "上传图片", "text": "拖放或点击上传WebP/PNG/JPEG/GIF图片。", "url": "#upload"},
                {"pos": 2, "name": "选择目标格式", "text": "选择要转换成的目标格式（WebP/PNG/JPEG/GIF）。", "url": "#format"},
                {"pos": 3, "name": "下载结果", "text": "点击下载按钮保存转换后的图片。", "url": "#download"},
            ],
            "totalTime": "PT1M",
            "breadcrumb": [("首页", "/"), ("图片工具", "/#image-tools"), ("WebP格式转换器", "/webp-converter/")],
        },
        "en": {
            "title": "WebP Converter - Free Online Image Format Converter",
            "h1": "🖼️ WebP Converter",
            "desc": "Free online WebP converter - convert between WebP, PNG, JPEG, and GIF. Drag & drop, batch conversion, pure client-side Canvas processing. No uploads, your images stay private.",
            "keywords": "WebP converter, WebP to PNG, PNG to WebP, JPEG to WebP, online WebP converter, image format converter, WebP to JPEG, free WebP converter",
            "software_name": "WebP Converter",
            "category": "MultimediaApplication",
            "faq": [
                {"q": "What is WebP format?", "a": "WebP is a modern image format developed by Google, supporting both lossy and lossless compression. Compared to JPEG and PNG, WebP files are typically 25-35% smaller while maintaining similar visual quality. Most modern browsers support WebP natively."},
                {"q": "Will image quality degrade after conversion?", "a": "You can adjust quality (1-100). At quality 100, conversion is nearly lossless. For WebP output, quality 80-90 is recommended — file size reduces by 30%+ with barely noticeable differences. When converting back to PNG/JPEG, use maximum quality to preserve original fidelity."},
                {"q": "Does it support batch conversion?", "a": "Yes! You can drag and drop or select multiple image files (up to 20) at once. The tool processes them in batch automatically. Download each result individually or as a zip package."},
                {"q": "Does it preserve transparency?", "a": "Yes. WebP and PNG both support transparency (alpha channel). When converting PNG with transparency to WebP, the alpha channel is automatically preserved. JPEG does not support transparency — transparent areas become white when converting to JPEG."},
            ],
            "howto_steps": [
                {"pos": 1, "name": "Upload Image", "text": "Drag & drop or click to upload WebP/PNG/JPEG/GIF images.", "url": "#upload"},
                {"pos": 2, "name": "Select Target Format", "text": "Choose the target format (WebP/PNG/JPEG/GIF).", "url": "#format"},
                {"pos": 3, "name": "Download Result", "text": "Click download to save the converted image.", "url": "#download"},
            ],
            "totalTime": "PT1M",
            "breadcrumb": [("Home", "/en/"), ("Image Tools", "/en/#image-tools"), ("WebP Converter", "/en/webp-converter/")],
        },
    },
    "ascii-art": {
        "icon": "🎨",
        "cat": "creative",
        "cat_name_cn": "创意工具",
        "cat_name_en": "Creative Tools",
        "cn": {
            "title": "ASCII艺术生成器",
            "h1": "🎨 ASCII艺术生成器",
            "desc": "免费在线ASCII艺术生成器，将文字、图片转换为ASCII字符画。支持多种字体样式、自定义字符集、亮度调节。纯前端本地处理，数据不上传服务器。一键复制分享。",
            "keywords": "ASCII艺术,ASCII Art,字符画,文字转ASCII,图片转ASCII,在线ASCII生成器,ASCII文字效果",
            "software_name": "ASCII艺术生成器",
            "category": "DesignApplication",
            "faq": [
                {"q": "什么是ASCII艺术？", "a": "ASCII艺术是用ASCII字符（字母、数字、符号）排列组成的图像或图案。最早起源于打字机时代，现在常用于终端界面、签名档、代码注释、社交媒体等场景，具有独特的复古美感。"},
                {"q": "如何生成更好的ASCII艺术？", "a": "文字模式：选择不同的字体样式和字符集可以获得不同效果。图片模式：调整亮度阈值和分辨率可以控制细节程度。推荐使用对比度较高的图片，简单的Logo和图标效果最好。"},
                {"q": "支持哪些字符集？", "a": "提供多种预设字符集：标准ASCII（@%#*+=-:. ）、方块字符（█▓▒░）、详细字符集（$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ）以及自定义字符集选项。"},
                {"q": "生成结果可以商用吗？", "a": "可以。您使用本工具生成的ASCII艺术作品完全归您所有，可以自由用于个人和商业项目。本工具纯前端处理，不会存储您的任何数据。"},
            ],
            "howto_steps": [
                {"pos": 1, "name": "输入内容", "text": "输入文字或上传图片。文字模式直接输入文本，图片模式拖放或选择图片。", "url": "#input"},
                {"pos": 2, "name": "调整参数", "text": "选择字体样式、字符集、亮度阈值等参数，实时预览效果。", "url": "#settings"},
                {"pos": 3, "name": "复制结果", "text": "点击复制按钮一键复制ASCII艺术，或下载为文本文件。", "url": "#copy"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("首页", "/"), ("创意工具", "/#creative-tools"), ("ASCII艺术生成器", "/ascii-art/")],
        },
        "en": {
            "title": "ASCII Art Generator - Free Online Text & Image to ASCII Converter",
            "h1": "🎨 ASCII Art Generator",
            "desc": "Free online ASCII art generator — convert text and images to ASCII character art. Multiple font styles, custom character sets, brightness adjustment. Pure client-side processing, no data uploads. One-click copy & share.",
            "keywords": "ASCII art, ASCII art generator, text to ASCII, image to ASCII, online ASCII generator, character art, ASCII text effect, free ASCII converter",
            "software_name": "ASCII Art Generator",
            "category": "DesignApplication",
            "faq": [
                {"q": "What is ASCII art?", "a": "ASCII art is imagery created using ASCII characters (letters, numbers, symbols) arranged in patterns. Originating from typewriter era, it's now commonly used in terminals, email signatures, code comments, and social media for its unique retro aesthetic."},
                {"q": "How do I generate better ASCII art?", "a": "Text mode: try different font styles and character sets for varied effects. Image mode: adjust brightness threshold and resolution to control detail level. High-contrast images work best; simple logos and icons produce the clearest results."},
                {"q": "What character sets are supported?", "a": "Several presets are available: Standard ASCII (@%#*+=-:. ), Block characters (█▓▒░), Detailed set ($@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ), plus a custom character set option."},
                {"q": "Can I use the generated art commercially?", "a": "Yes. Any ASCII artwork you generate with this tool is entirely yours to use freely for personal and commercial projects. This tool processes everything client-side — we never store your data."},
            ],
            "howto_steps": [
                {"pos": 1, "name": "Enter Content", "text": "Type text or upload an image. Text mode: type directly. Image mode: drag & drop or select an image.", "url": "#input"},
                {"pos": 2, "name": "Adjust Settings", "text": "Choose font style, character set, brightness threshold — preview updates in real-time.", "url": "#settings"},
                {"pos": 3, "name": "Copy Result", "text": "Click copy to grab your ASCII art, or download as a text file.", "url": "#copy"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("Home", "/en/"), ("Creative Tools", "/en/#creative-tools"), ("ASCII Art Generator", "/en/ascii-art/")],
        },
    },
    "csv-diff": {
        "icon": "📊",
        "cat": "dev",
        "cat_name_cn": "开发工具",
        "cat_name_en": "Developer Tools",
        "cn": {
            "title": "CSV差异对比器",
            "h1": "📊 CSV差异对比器",
            "desc": "免费在线CSV差异对比工具，快速比较两个CSV文件的行级差异。支持新增、删除、修改标记，列对齐显示，忽略空白和大小写选项。纯前端本地处理，数据不上传服务器。",
            "keywords": "CSV对比,CSV diff,CSV差异,在线CSV比较,CSV文件对比,表格对比,数据差异检测",
            "software_name": "CSV差异对比器",
            "category": "DeveloperApplication",
            "faq": [
                {"q": "支持多大的CSV文件？", "a": "纯前端处理，建议文件大小不超过10MB或10万行。对于超大文件，浏览器可能会变慢。工具会在处理前显示行数预览，您可以根据需要选择只对比前N行。"},
                {"q": "对比结果如何解读？", "a": "结果分为三种类型：<strong>新增行</strong>（绿色标记，仅在文件B中存在）、<strong>删除行</strong>（红色标记，仅在文件A中存在）、<strong>修改行</strong>（黄色标记，同一位置内容不同）。支持按类型筛选查看。"},
                {"q": "支持哪些CSV格式？", "a": "支持逗号、分号、Tab制表符等常见分隔符，自动检测。支持带引号字段、换行符转义等标准CSV特性。UTF-8和GBK编码自动识别。"},
                {"q": "可以导出对比结果吗？", "a": "可以。支持导出为HTML格式的差异报告（保留颜色标记），也可以单独导出新增行、删除行或修改行为CSV文件。方便存档和分享对比结果。"},
            ],
            "howto_steps": [
                {"pos": 1, "name": "上传文件", "text": "粘贴或上传原始CSV（A）和新CSV（B）文件。", "url": "#upload"},
                {"pos": 2, "name": "设置选项", "text": "选择分隔符、编码、是否忽略空白和大小写等选项。", "url": "#options"},
                {"pos": 3, "name": "查看差异", "text": "对比结果按新增/删除/修改分类显示，可筛选和导出。", "url": "#result"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("首页", "/"), ("开发工具", "/#dev-tools"), ("CSV差异对比器", "/csv-diff/")],
        },
        "en": {
            "title": "CSV Diff Checker - Free Online CSV Comparison Tool",
            "h1": "📊 CSV Diff Checker",
            "desc": "Free online CSV diff tool — quickly compare two CSV files row by row. Highlights additions, deletions, and modifications with column alignment. Ignore whitespace and case options. Pure client-side, no uploads.",
            "keywords": "CSV diff, CSV comparison, CSV compare, online CSV diff, CSV file comparison, spreadsheet diff, data diff checker, free CSV diff tool",
            "software_name": "CSV Diff Checker",
            "category": "DeveloperApplication",
            "faq": [
                {"q": "What CSV file size is supported?", "a": "Since processing is client-side, we recommend files under 10MB or 100K rows. For very large files, the browser may slow down. The tool shows a row count preview before processing — you can limit comparison to the first N rows if needed."},
                {"q": "How to read the comparison results?", "a": "Results are categorized into three types: <strong>Added rows</strong> (green, only in file B), <strong>Removed rows</strong> (red, only in file A), <strong>Modified rows</strong> (yellow, same position but different content). Filter by type to focus on specific changes."},
                {"q": "What CSV formats are supported?", "a": "Comma, semicolon, tab, and other common delimiters are supported with auto-detection. Quoted fields, escaped newlines, and standard CSV features work correctly. UTF-8 and Latin-1 encodings are auto-detected."},
                {"q": "Can I export the comparison results?", "a": "Yes. Export as an HTML diff report (preserving color highlights), or export added/removed/modified rows individually as CSV files. Great for archiving and sharing comparison results."},
            ],
            "howto_steps": [
                {"pos": 1, "name": "Upload Files", "text": "Paste or upload the original CSV (A) and the new CSV (B).", "url": "#upload"},
                {"pos": 2, "name": "Configure Options", "text": "Set delimiter, encoding, and choose whether to ignore whitespace or case.", "url": "#options"},
                {"pos": 3, "name": "View Differences", "text": "Results display categorized as added/removed/modified — filter and export as needed.", "url": "#result"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("Home", "/en/"), ("Developer Tools", "/en/#dev-tools"), ("CSV Diff Checker", "/en/csv-diff/")],
        },
    },
    "gif-to-mp4": {
        "icon": "🎬",
        "cat": "video",
        "cat_name_cn": "视频工具",
        "cat_name_en": "Video Tools",
        "cn": {
            "title": "GIF转MP4转换器",
            "h1": "🎬 GIF转MP4转换器",
            "desc": "免费在线GIF转MP4转换器，将GIF动图转换为MP4视频格式。支持调整帧率、质量和尺寸，文件体积可减少90%以上。纯前端FFmpeg.wasm处理，数据不上传服务器。",
            "keywords": "GIF转MP4,GIF to MP4,在线GIF转换,GIF压缩,动图转视频,GIF转换器,免费GIF转MP4",
            "software_name": "GIF转MP4转换器",
            "category": "MultimediaApplication",
            "faq": [
                {"q": "为什么要把GIF转成MP4？", "a": "MP4视频格式比GIF高效得多。一个10MB的GIF转成MP4后通常只有1-2MB，体积减少80-90%。MP4支持更流畅的帧率、更好的色彩（1600万色 vs GIF的256色），而且几乎所有平台都原生支持MP4播放。"},
                {"q": "转换后的MP4能循环播放吗？", "a": "能。生成的MP4默认包含循环播放元数据。在网页中可以使用HTML5 video标签的loop属性，在社交媒体上传后也会自动循环播放，完美替代GIF的循环效果。"},
                {"q": "转换过程会丢失画质吗？", "a": "可以选择输出质量。高质量模式（CRF 18）几乎无损，文件稍大；默认模式（CRF 23）画质良好且文件较小。相比GIF的256色调色板限制，MP4的1600万色可以呈现更丰富的色彩。"},
                {"q": "支持哪些GIF特性？", "a": "支持透明GIF（透明度转为黑色背景）、多帧GIF、不同帧率的GIF。超大GIF（>50MB）建议先在本地压缩再转换。纯前端FFmpeg.wasm处理，首次加载可能需要几秒下载WASM文件。"},
            ],
            "howto_steps": [
                {"pos": 1, "name": "上传GIF", "text": "拖放或点击上传GIF动图文件（支持最大50MB）。", "url": "#upload"},
                {"pos": 2, "name": "设置参数", "text": "调整输出帧率、视频质量和尺寸（可选）。", "url": "#settings"},
                {"pos": 3, "name": "下载MP4", "text": "点击转换并下载生成的MP4视频文件。", "url": "#download"},
            ],
            "totalTime": "PT2M",
            "breadcrumb": [("首页", "/"), ("视频工具", "/#video-tools"), ("GIF转MP4转换器", "/gif-to-mp4/")],
        },
        "en": {
            "title": "GIF to MP4 Converter - Free Online GIF to Video Converter",
            "h1": "🎬 GIF to MP4 Converter",
            "desc": "Free online GIF to MP4 converter — turn animated GIFs into MP4 videos. Adjustable frame rate, quality, and dimensions. File size reduced by up to 90%. Pure client-side FFmpeg.wasm, no uploads.",
            "keywords": "GIF to MP4, GIF to video, online GIF converter, GIF compressor, animated GIF to MP4, GIF converter, free GIF to MP4 converter",
            "software_name": "GIF to MP4 Converter",
            "category": "MultimediaApplication",
            "faq": [
                {"q": "Why convert GIF to MP4?", "a": "MP4 video format is far more efficient than GIF. A 10MB GIF typically becomes just 1-2MB as MP4 — an 80-90% size reduction. MP4 supports smoother frame rates, better colors (16 million vs GIF's 256), and virtually all platforms support MP4 playback natively."},
                {"q": "Will the MP4 loop like the original GIF?", "a": "Yes. The generated MP4 includes loop metadata by default. Use the HTML5 video tag's loop attribute on web pages, and it will auto-loop on social media uploads too — a perfect GIF replacement."},
                {"q": "Does conversion lose quality?", "a": "You can choose output quality. High quality mode (CRF 18) is nearly lossless with slightly larger files; default mode (CRF 23) offers good quality with smaller files. Compared to GIF's 256-color palette, MP4's 16 million colors can render richer visuals."},
                {"q": "What GIF features are supported?", "a": "Transparent GIFs (transparency becomes black background), multi-frame GIFs, and variable frame rates are all supported. For very large GIFs (>50MB), consider compressing locally first. FFmpeg.wasm runs client-side — first load may take a few seconds to download the WASM binary."},
            ],
            "howto_steps": [
                {"pos": 1, "name": "Upload GIF", "text": "Drag & drop or click to upload your animated GIF (up to 50MB).", "url": "#upload"},
                {"pos": 2, "name": "Configure Settings", "text": "Adjust output frame rate, video quality, and dimensions (optional).", "url": "#settings"},
                {"pos": 3, "name": "Download MP4", "text": "Click convert and download the resulting MP4 video file.", "url": "#download"},
            ],
            "totalTime": "PT2M",
            "breadcrumb": [("Home", "/en/"), ("Video Tools", "/en/#video-tools"), ("GIF to MP4 Converter", "/en/gif-to-mp4/")],
        },
    },
    "latex-editor": {
        "icon": "📝",
        "cat": "dev",
        "cat_name_cn": "开发工具",
        "cat_name_en": "Developer Tools",
        "cn": {
            "title": "LaTeX在线编辑器",
            "h1": "📝 LaTeX在线编辑器",
            "desc": "免费在线LaTeX编辑器，实时预览数学公式和文档。支持常用数学符号、矩阵、分数、积分等模板，一键插入。纯前端MathJax渲染，数据不上传服务器。适合学术论文、作业、笔记。",
            "keywords": "LaTeX编辑器,在线LaTeX,数学公式编辑器,LaTeX公式,在线公式编辑,LaTeX预览,免费LaTeX编辑器",
            "software_name": "LaTeX在线编辑器",
            "category": "DeveloperApplication",
            "faq": [
                {"q": "LaTeX是什么？", "a": "LaTeX是一种专业的排版系统，广泛用于学术论文、数学公式、科学文档的编写。它使用标记语言描述文档结构和公式，能生成高质量的PDF输出。本工具专注LaTeX数学公式的实时编辑和预览。"},
                {"q": "支持哪些LaTeX命令？", "a": "支持MathJax兼容的LaTeX命令，包括：上下标、分数、根号、求和积分、矩阵、希腊字母、三角函数、括号、箭头、化学式等。内置模板面板提供常用公式的快速插入。"},
                {"q": "可以导出公式吗？", "a": "可以。支持复制LaTeX源码、导出为SVG矢量图（可嵌入Word/PPT）、导出为PNG图片。SVG格式可无限放大不失真，适合论文插图。"},
                {"q": "需要安装什么吗？", "a": "完全不需要！本工具是纯网页应用，打开浏览器即可使用。不需要安装LaTeX发行版（如TeX Live、MiKTeX），也不需要任何插件。所有渲染通过MathJax在浏览器中完成。"},
            ],
            "howto_steps": [
                {"pos": 1, "name": "编写公式", "text": "在编辑区输入LaTeX代码，或点击模板面板快速插入常用公式。", "url": "#editor"},
                {"pos": 2, "name": "实时预览", "text": "右侧面板实时渲染LaTeX公式，即时查看效果。", "url": "#preview"},
                {"pos": 3, "name": "导出使用", "text": "复制LaTeX源码或导出为SVG/PNG图片，用于论文、博客或演示。", "url": "#export"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("首页", "/"), ("开发工具", "/#dev-tools"), ("LaTeX在线编辑器", "/latex-editor/")],
        },
        "en": {
            "title": "LaTeX Editor - Free Online LaTeX Formula Editor & Preview",
            "h1": "📝 LaTeX Online Editor",
            "desc": "Free online LaTeX editor with real-time math formula preview. Common math symbols, matrices, fractions, integrals — one-click insertion. Pure client-side MathJax rendering, no uploads. Perfect for academic papers, homework, and notes.",
            "keywords": "LaTeX editor, online LaTeX, math formula editor, LaTeX formula, online equation editor, LaTeX preview, free LaTeX editor",
            "software_name": "LaTeX Online Editor",
            "category": "DeveloperApplication",
            "faq": [
                {"q": "What is LaTeX?", "a": "LaTeX is a professional typesetting system widely used for academic papers, mathematical formulas, and scientific documents. It uses markup language to describe document structure and formulas, producing high-quality PDF output. This tool focuses on real-time LaTeX math formula editing and preview."},
                {"q": "What LaTeX commands are supported?", "a": "MathJax-compatible LaTeX commands are supported, including: superscripts/subscripts, fractions, roots, sums/integrals, matrices, Greek letters, trigonometric functions, brackets, arrows, chemical formulas, and more. The template panel provides quick insertion of common formulas."},
                {"q": "Can I export formulas?", "a": "Yes. Copy LaTeX source code, export as SVG vector graphics (embeddable in Word/PPT), or export as PNG images. SVG format scales infinitely without quality loss — ideal for paper illustrations."},
                {"q": "Do I need to install anything?", "a": "Not at all! This is a pure web application — just open your browser. No LaTeX distribution (TeX Live, MiKTeX) or plugins required. All rendering is done client-side via MathJax."},
            ],
            "howto_steps": [
                {"pos": 1, "name": "Write Formula", "text": "Type LaTeX code in the editor, or click template buttons to quickly insert common formulas.", "url": "#editor"},
                {"pos": 2, "name": "Live Preview", "text": "The right panel renders LaTeX formulas in real-time — see results instantly.", "url": "#preview"},
                {"pos": 3, "name": "Export & Use", "text": "Copy LaTeX source or export as SVG/PNG images for papers, blogs, or presentations.", "url": "#export"},
            ],
            "totalTime": "PT30S",
            "breadcrumb": [("Home", "/en/"), ("Developer Tools", "/en/#dev-tools"), ("LaTeX Online Editor", "/en/latex-editor/")],
        },
    },
}


def build_page(tool_id, lang, info, tool_data):
    """构建完整的HTML页面"""
    is_cn = lang == "cn"
    lang_attr = "zh-CN" if is_cn else "en"
    site_name = "在线小工具矩阵" if is_cn else "Online Tools Matrix"
    base_path = "" if is_cn else "en/"
    home_path = "../../" if not is_cn else "../../"
    en_path_prefix = "../../en/" if is_cn else ""
    other_lang_path = f"../../en/{tool_id}/" if is_cn else f"../../{tool_id}/"
    other_lang_label = "English" if is_cn else "中文"
    og_image = "og-image.svg" if is_cn else "en/og-image.svg"
    
    # Canonical URL
    if is_cn:
        canonical = f"https://webtools-cn.github.io/tools-site/{tool_id}/"
    else:
        canonical = f"https://webtools-cn.github.io/tools-site/en/{tool_id}/"
    
    # Schema data
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": fa["q"], "acceptedAnswer": {"@type": "Answer", "text": fa["a"]}}
            for fa in info["faq"]
        ]
    }
    
    howto_schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": info["howto_steps"][0]["name"] if is_cn else f"How to Use the {info['software_name']}",
        "description": f"使用{info['software_name']}的简单步骤。" if is_cn else f"Simple steps to use the {info['software_name']}.",
        "totalTime": info["totalTime"],
        "tool": {"@type": "HowToTool", "name": info["software_name"]},
        "step": [
            {
                "@type": "HowToStep", "position": s["pos"], "name": s["name"],
                "text": s["text"], "url": f"https://webtools-cn.github.io/tools-site/{base_path}{tool_id}/{s['url']}"
            }
            for s in info["howto_steps"]
        ]
    }
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b[0],
             "item": f"https://webtools-cn.github.io/tools-site{b[1]}"}
            for i, b in enumerate(info["breadcrumb"])
        ]
    }
    
    software_schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": info["software_name"],
        "applicationCategory": info["category"],
        "operatingSystem": "Web",
        "publisher": {"@type": "Organization", "name": "Online Tools"},
        "dateModified": TODAY,
        "description": info["desc"][:150],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CNY"}
    }
    
    import json
    faq_json = json.dumps(faq_schema, ensure_ascii=False, indent=2)
    howto_json = json.dumps(howto_schema, ensure_ascii=False, indent=2)
    bread_json = json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)
    sw_json = json.dumps(software_schema, ensure_ascii=False, indent=2)
    
    # FAQ HTML
    faq_html = ""
    for fa in info["faq"]:
        faq_html += f'''    <div class="faq-item">
      <h3>{fa["q"]}</h3>
      <p>{fa["a"]}</p>
    </div>
'''
    
    page = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-9W1157EBQV');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{info['desc']}">
<meta name="keywords" content="{info['keywords']}">
<title>{info['title']}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{info['title']}">
<meta property="og:description" content="{info['desc'][:150]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://webtools-cn.github.io/tools-site/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{'免费在线工具 - 无需注册' if is_cn else 'Free Online Tools - No Signup Required'}">
<meta name="twitter:description" content="{'1200+免费在线工具。纯前端，不上传服务器，保护隐私。' if is_cn else '1200+ free online tools. Client-side only, no uploads, privacy protected.'}">
<meta name="twitter:image" content="https://webtools-cn.github.io/tools-site/{og_image}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<script type="application/ld+json">
{sw_json}
</script>
<script type="application/ld+json">
{faq_json}
</script>
<script type="application/ld+json">
{howto_json}
</script>
<script type="application/ld+json">
{bread_json}
</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
textarea,.text-input{{width:100%;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;color:#e2e8f0;font-family:monospace;font-size:.9rem;resize:vertical;min-height:120px}}
textarea:focus,.text-input:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.upload-zone{{border:2px dashed rgba(148,163,184,.3);border-radius:12px;padding:40px;text-align:center;transition:border-color .3s;cursor:pointer;margin:12px 0}}
.upload-zone:hover,.upload-zone.dragover{{border-color:rgba(6,182,212,.5);background:rgba(6,182,212,.05)}}
.upload-zone svg{{width:48px;height:48px;margin-bottom:12px;opacity:.5}}
.upload-zone p{{color:#94a3b8;font-size:.9rem}}
.form-row{{display:flex;gap:16px;flex-wrap:wrap;margin:12px 0;align-items:center}}
.form-row label{{font-size:.9rem;color:#94a3b8;min-width:80px}}
.form-row input,.form-row select{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:6px 10px;color:#e2e8f0;font-size:.85rem}}
.form-row input[type=range]{{accent-color:#06b6d4;flex:1;max-width:200px}}
.form-row input[type=number]{{width:80px}}
.form-row span{{font-size:.8rem;color:#22d3ee;min-width:30px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-primary:disabled{{opacity:.4;cursor:not-allowed}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-danger{{background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.3)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-content{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:12px;font-family:monospace;font-size:.85rem;color:#94a3b8;max-height:400px;overflow:auto;white-space:pre-wrap;word-break:break-all}}
.empty-state{{text-align:center;padding:40px 20px;color:#64748b}}
.template-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;margin:12px 0}}
.template-btn{{background:rgba(148,163,184,.1);border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#94a3b8;font-size:.8rem;cursor:pointer;text-align:center;transition:all .2s}}
.template-btn:hover{{background:rgba(6,182,212,.15);border-color:rgba(6,182,212,.3);color:#22d3ee}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem}}
.preview-box{{min-height:60px;background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:16px;margin-top:12px;text-align:center}}
.preview-box img,.preview-box video{{max-width:100%;max-height:300px;border-radius:4px}}
.diff-added{{background:rgba(34,197,94,.15);color:#4ade80;padding:2px 6px;border-radius:3px}}
.diff-removed{{background:rgba(239,68,68,.15);color:#f87171;padding:2px 6px;border-radius:3px}}
.diff-modified{{background:rgba(234,179,8,.15);color:#facc15;padding:2px 6px;border-radius:3px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1}}
#fileInput{{display:none}}
@media(max-width:600px){{.header{{flex-direction:column;align-items:flex-start}}.preview-row{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{info['h1']}</h1>
    <div class="lang-switch">
      <a href="#" class="active">{'中文' if is_cn else 'English'}</a>
      <a href="{other_lang_path}">{other_lang_label}</a>
    </div>
  </div>
  
  <div class="nav-back"><a href="{home_path}">{'← 返回首页' if is_cn else '← Back to Home'}</a> / {tool_data['cat_name_cn'] if is_cn else tool_data['cat_name_en']} / {info['software_name']}</div>

  <!-- PLACEHOLDER: Tool-specific HTML + JS will be injected here -->
  <div id="tool-placeholder" style="background:#1e293b;border-radius:12px;padding:40px;text-align:center;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)">
    <p style="color:#64748b">{'🔧 工具加载中...' if is_cn else '🔧 Tool loading...'}</p>
  </div>

  <div class="info-section">
    <h2>{'📖 常见问题' if is_cn else '📖 Frequently Asked Questions'}</h2>
{faq_html}  </div>

  <div class="footer">
    <a href="{home_path}">{'首页' if is_cn else 'Home'}</a> | 
    <a href="{home_path}#{tool_data['cat']}-tools">{tool_data['cat_name_cn'] if is_cn else tool_data['cat_name_en']}</a> |
    <a href="{other_lang_path}">{other_lang_label}</a>
    <p style="margin-top:8px">{'© 2026 WebTools. 所有工具免费使用，数据不上传服务器。' if is_cn else '© 2026 WebTools. All tools are free. No data is uploaded to any server.'}</p>
  </div>
  <div class="toast" id="toast"></div>
</div>
</body>
</html>'''
    return page


# 生成所有页面
for tool_id, tool_data in tools.items():
    for lang in ["cn", "en"]:
        info = tool_data[lang]
        page = build_page(tool_id, lang, info, tool_data)
        
        if lang == "cn":
            path = os.path.join(BASE, tool_id, "index.html")
        else:
            path = os.path.join(BASE, "en", tool_id, "index.html")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Created: {path}")

print("\nAll 10 pages generated successfully!")