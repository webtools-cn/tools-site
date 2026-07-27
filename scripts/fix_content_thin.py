#!/usr/bin/env python3
"""修复 content_thin: 给薄页面添加如何使用FAQ段落"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THIN_PAGES = [
    'chart-maker', 'donut-chart-maker', 'dotenv-validator', 'env-file-generator',
    'heic-to-jpg', 'html-editor', 'html-minifier', 'json-to-tsv', 'pdf-merge',
    'pdf-split', 'rot13-converter', 'screenshot-to-pdf', 'social-share-generator',
    'structured-data-validator', 'tsv-to-csv', 'coin-flipper', 'favicon-downloader',
    'heic-to-jpg', 'structured-data-validator'
]

FAQ_DATA = {
    'chart-maker': {
        'title': 'Chart Maker',
        'how': 'Select chart type (bar, line, pie, doughnut), enter your data as comma-separated values or labels and numbers, then click generate. Easily customize colors and download the chart as PNG.',
        'free': 'Chart Maker is completely free and runs locally in your browser. No sign-up, no uploads, no data collection.',
        'features': 'Supports bar charts, line charts, pie charts, and doughnut charts. Customizable colors, instant preview, and one-click download.'
    },
    'donut-chart-maker': {
        'title': 'Donut Chart Maker',
        'how': 'Enter labels and values for each segment, choose colors, and click generate. The donut chart renders instantly and can be downloaded as a PNG image.',
        'free': 'Donut Chart Maker is completely free and processes all data locally in your browser. No data is sent to any server.',
        'features': 'Custom segment colors, interactive hover tooltips, PNG export, responsive design.'
    },
    'dotenv-validator': {
        'title': '.env File Validator',
        'how': 'Paste your .env file content into the editor panel. The validator checks syntax, detects duplicate keys, validates value formats, and flags potential security issues.',
        'free': 'Entirely free and runs locally — your environment variables never leave your browser.',
        'features': 'Syntax validation, duplicate key detection, value format checking, real-time feedback.'
    },
    'env-file-generator': {
        'title': '.env File Generator',
        'how': 'Select your tech stack (Node.js, Python, Docker, etc.), fill in the key-value pairs, and click generate. The tool creates a properly formatted .env file ready for download.',
        'free': 'Free and private — all generation happens in your browser. No server processing or data collection.',
        'features': 'Multiple framework templates, custom key-value editing, one-click download, comment support.'
    },
    'heic-to-jpg': {
        'title': 'HEIC to JPG Converter',
        'how': 'Drag and drop or select HEIC/HEIF images, adjust quality if desired, and click convert. All conversion happens locally in your browser for maximum privacy.',
        'free': 'Completely free with no file size limits. Files are processed locally — never uploaded to any server.',
        'features': 'Batch conversion, adjustable quality, preserves metadata, instant download.'
    },
    'html-editor': {
        'title': 'HTML Editor',
        'how': 'Type or paste HTML in the editor panel, and see the live preview update instantly. Use the formatting tools and code completion for faster editing.',
        'free': 'Free online HTML editor with no registration. All code stays in your browser.',
        'features': 'Live preview, syntax highlighting, auto-completion, mobile responsive.'
    },
    'html-minifier': {
        'title': 'HTML Minifier',
        'how': 'Paste your HTML code into the editor. The minifier removes whitespace, comments, and optional tags to reduce file size while preserving functionality.',
        'free': '100% free with no limits. Minification runs locally — your code never leaves the browser.',
        'features': 'Whitespace removal, comment stripping, optional tag removal, size comparison display.'
    },
    'json-to-tsv': {
        'title': 'JSON to TSV Converter',
        'how': 'Paste your JSON array of objects into the editor. The converter flattens nested structures and outputs tab-separated values ready for spreadsheet import.',
        'free': 'Free online converter — all processing is done in your browser. No data is uploaded or stored.',
        'features': 'Nested object flattening, custom delimiter support, copy-to-clipboard, download as .tsv.'
    },
    'pdf-merge': {
        'title': 'PDF Merger',
        'how': 'Select multiple PDF files, arrange them in the desired order by dragging, and click merge. The combined PDF downloads automatically.',
        'free': 'Free PDF merging with no page limits. All files are processed locally in your browser for privacy.',
        'features': 'Drag-and-drop reordering, unlimited files, local processing, instant download.'
    },
    'pdf-split': {
        'title': 'PDF Splitter',
        'how': 'Upload a PDF, select the page ranges you want to extract, and click split. Each range becomes a separate PDF file.',
        'free': 'Free PDF splitting tool. All processing happens in your browser — your documents are never uploaded.',
        'features': 'Custom page ranges, multiple splits at once, local processing, instant download.'
    },
    'rot13-converter': {
        'title': 'ROT13 Converter',
        'how': 'Type or paste text into the input field. ROT13 shifts each letter by 13 positions — applying it twice returns the original text. Click convert to encode or decode.',
        'free': 'Free ROT13 tool with no registration. All text processing stays in your browser.',
        'features': 'Bidirectional encode/decode, instant conversion, copy-to-clipboard, supports all Latin letters.'
    },
    'screenshot-to-pdf': {
        'title': 'Screenshot to PDF Converter',
        'how': 'Upload screenshot images (PNG, JPG, WebP), arrange their order, and click convert. The tool creates a PDF with each screenshot on its own page.',
        'free': 'Free and private — all file processing happens locally in your browser. No uploads to any server.',
        'features': 'Multiple image formats supported, page ordering, adjustable page size, instant download.'
    },
    'social-share-generator': {
        'title': 'Social Share Link Generator',
        'how': 'Enter your URL and optional text, then click generate. Get ready-to-use sharing links for Facebook, Twitter/X, LinkedIn, WhatsApp, and more.',
        'free': 'Free social share link generator. No data is collected or stored.',
        'features': 'Multiple platform support, URL encoding, custom text, one-click copy for each platform.'
    },
    'structured-data-validator': {
        'title': 'Structured Data Validator',
        'how': 'Paste your JSON-LD, Microdata, or RDFa markup into the editor. The validator checks syntax, schema.org compliance, and provides fix suggestions.',
        'free': 'Free structured data validation tool. All processing is done locally in your browser.',
        'features': 'JSON-LD/Microdata/RDFa support, schema.org validation, error highlighting, fix suggestions.'
    },
    'tsv-to-csv': {
        'title': 'TSV to CSV Converter',
        'how': 'Paste your TSV (tab-separated values) data into the editor. The converter transforms tabs to commas and handles quoted fields for proper CSV output.',
        'free': 'Free online converter. All processing is done in your browser — no data is uploaded.',
        'features': 'Quoted field handling, custom delimiter options, copy-to-clipboard, download as .csv.'
    },
    'coin-flipper': {
        'title': 'Coin Flipper',
        'how': 'Click the flip button to randomly generate heads or tails. Use for decision making, game starters, or settling friendly debates.',
        'free': 'Free virtual coin flipper — no coins needed! Runs entirely in your browser.',
        'features': 'Random fair flip, heads/tails animation, flip counter, sound effects option.'
    },
    'favicon-downloader': {
        'title': 'Favicon Downloader',
        'how': 'Enter any website URL and click fetch. The tool retrieves the favicon in all available sizes and formats for download.',
        'free': 'Free favicon downloader. Fetches favicons directly — no intermediary storage.',
        'features': 'Auto-detect favicon URL, multiple sizes, PNG/ICO/SVG support, one-click download.'
    }
}

def fix_content_thin(path, tool_name):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    data = FAQ_DATA.get(tool_name)
    if not data:
        return None
    
    # Only add if missing FAQ section
    if '<section class="faq' in content or 'class="faq' in content:
        # Already has FAQ, check if content was expanded
        if 'how-to' in content.lower() or 'How to use' in content:
            return None
    
    faq = f'''
  <section class="card" style="margin-top:24px">
    <h2 style="font-size:20px;margin-bottom:16px">About {data['title']}</h2>
    <div class="faq-item" style="margin-bottom:12px">
      <h3 style="font-size:15px">How to use {data['title']}?</h3>
      <p style="color:var(--sub);font-size:14px;line-height:1.8">{data['how']}</p>
    </div>
    <div class="faq-item" style="margin-bottom:12px">
      <h3 style="font-size:15px">Is this tool free?</h3>
      <p style="color:var(--sub);font-size:14px;line-height:1.8">{data['free']}</p>
    </div>
    <div class="faq-item">
      <h3 style="font-size:15px">What features are included?</h3>
      <p style="color:var(--sub);font-size:14px;line-height:1.8">{data['features']}</p>
    </div>
  </section>'''
    
    content = content.replace('</main>', faq + '\n</main>', 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return '+FAQ section'

def main():
    pages = {
        'cn:chart-maker': 'chart-maker', 'cn:donut-chart-maker': 'donut-chart-maker',
        'cn:dotenv-validator': 'dotenv-validator', 'cn:env-file-generator': 'env-file-generator',
        'cn:heic-to-jpg': 'heic-to-jpg', 'cn:html-editor': 'html-editor',
        'cn:html-minifier': 'html-minifier', 'cn:json-to-tsv': 'json-to-tsv',
        'cn:pdf-merge': 'pdf-merge', 'cn:pdf-split': 'pdf-split',
        'cn:rot13-converter': 'rot13-converter', 'cn:screenshot-to-pdf': 'screenshot-to-pdf',
        'cn:social-share-generator': 'social-share-generator',
        'cn:structured-data-validator': 'structured-data-validator',
        'cn:tsv-to-csv': 'tsv-to-csv',
        'en:coin-flipper': 'coin-flipper', 'en:favicon-downloader': 'favicon-downloader',
        'en:heic-to-jpg': 'heic-to-jpg',
        'en:structured-data-validator': 'structured-data-validator',
    }
    
    for key, tool in pages.items():
        lang = key.split(':')[0]
        if lang == 'cn':
            path = os.path.join(SITE, tool, 'index.html')
        else:
            path = os.path.join(SITE, 'en', tool, 'index.html')
        
        if not os.path.exists(path):
            continue
        
        result = fix_content_thin(path, tool)
        if result:
            print(f'✅ {key}: {result}')
        else:
            print(f'⏭️ {key}: already has FAQ')

if __name__ == '__main__':
    main()
