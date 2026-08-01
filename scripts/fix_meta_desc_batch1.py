#!/usr/bin/env python3
"""Generate and apply precise meta descriptions for 30 EN tool pages."""
import re, os

# Map: relative_path -> (old_desc_prefix, new_description)
# old_desc_prefix must be unique enough to find the line
FIXES = {
    "en/yaml-lint/index.html": (
        'Free yaml lint. Free online YAML lint tool. Real-time.... No registration required.',
        'Free online YAML validator and linter. Paste your YAML to check syntax errors, fix indentation issues, and validate structure instantly in your browser — no uploads or signup needed.'
    ),
    "en/line-sorter/index.html": (
        'Free line sort. Free online line sorter tool for sort.... No registration required.',
        'Free online line sorter tool. Sort text lines alphabetically (A-Z or Z-A), by length, randomly, or reverse order. Paste your list and get instant sorted results in your browser.'
    ),
    "en/url-builder/index.html": (
        'Free url builder. Free online URL Builder & Query Strin.... No registration required.',
        'Free online URL builder to construct and encode URLs with query parameters. Add key-value pairs, encode special characters, and generate clean URLs for web development and API testing.'
    ),
    "en/yaml-merger/index.html": (
        'Free yaml merger. Free online YAML merger tool. Deep me.... No registration required.',
        'Free online YAML merger. Combine multiple YAML files with deep merge support, handle conflicts, and merge arrays or objects. No signup — paste, merge, and download instantly.'
    ),
    "en/vision-test/index.html": (
        'Free vision test. Free online vision test with standard.... No registration required.',
        'Free online vision test using standard Snellen chart. Check your visual acuity at home — read letters of decreasing size to estimate your eyesight. Not a substitute for professional eye exams.'
    ),
    "en/csv-to-excel/index.html": (
        'Free csv to excel. Free online CSV to Excel (XLSX) conve.... No registration required.',
        'Free online CSV to Excel (XLSX) converter. Upload your CSV file and download a formatted Excel spreadsheet instantly. Supports delimiter detection, UTF-8 encoding, and large files — no signup required.'
    ),
    "en/online-clock/index.html": (
        'Free online clock. Free online clock with analog and dig.... No registration required.',
        'Free online clock with analog and digital displays. View current time in your timezone with a full-screen mode, dark theme support, and second hand — perfect for presentations and time tracking.'
    ),
    "en/xml-validator/index.html": (
        'Free xml validator. Free online XML validator. Validate X.... No registration required.',
        'Free online XML validator. Paste your XML to check for syntax errors, mismatched tags, and structural issues. Get line-by-line error reports with instant validation — no uploads or signup needed.'
    ),
    "en/sql-to-kysely/index.html": (
        'Free sql to kysely. Free online SQL to Kysely converter. .... No registration required.',
        'Free online SQL to Kysely query builder converter. Transform raw SQL statements into type-safe Kysely TypeScript code. Supports SELECT, INSERT, UPDATE, DELETE — paste SQL and get Kysely code instantly.'
    ),
    "en/daily-planner/index.html": (
        'Free daily planner. Free online daily planner tool to hel.... No registration required.',
        'Free online daily planner to organize your day. Schedule tasks by hour, set priorities, add notes, and track progress. Simple drag-and-drop interface — all data stays in your browser, no signup required.'
    ),
    "en/svg-to-base64/index.html": (
        'Free svg to base64. Free online Svg To Base64 tool. Pure .... No registration required.',
        'Free online SVG to Base64 converter. Paste your SVG code and get a Base64 data URI for embedding images in HTML, CSS, or Markdown. Instant conversion with copy-to-clipboard — no uploads needed.'
    ),
    "en/video-cropper/index.html": (
        'Free video cropper. Free online video cropper. Crop video.... No registration required.',
        'Free online video cropper. Trim and crop videos directly in your browser — select start/end times, adjust aspect ratio, and download the cropped clip. No upload to server, fully client-side processing.'
    ),
    "en/csp-generator/index.html": (
        'Free csp generator. Free online Content Security Policy (.... No registration required.',
        'Free online Content Security Policy (CSP) generator. Build secure CSP headers for your website — configure script-src, style-src, img-src, and more with a visual builder. Generate ready-to-use HTTP headers.'
    ),
    "en/shuffle-lines/index.html": (
        'Free shuffle lines. Free online line shuffler tool. Rando.... No registration required.',
        'Free online line shuffler. Randomize the order of text lines instantly — useful for raffle draws, test question randomization, playlist shuffling, and data sampling. Paste lines and get shuffled output.'
    ),
    "en/interval-timer/index.html": (
        'Free interval timer. Free online interval timer for HIIT, .... No registration required.',
        'Free online interval timer for HIIT workouts, Tabata, circuit training, and study sessions. Set work/rest intervals, rounds, and get audio alerts. Works on mobile and desktop — no app install needed.'
    ),
    "en/yaml-validator/index.html": (
        'Free yaml validator. Free online YAML validator and format.... No registration required.',
        'Free online YAML validator and formatter. Check YAML syntax, fix indentation, validate against schemas, and beautify your YAML output. Paste your code and get instant feedback — no signup required.'
    ),
    "en/emoji-to-image/index.html": (
        'Free emoji to image. Free online Emoji to image converter..... No registration required.',
        'Free online emoji to image converter. Turn any emoji into a downloadable PNG image. Choose size, background color, and export format. Perfect for social media, presentations, and design projects.'
    ),
    "en/json-flattener/index.html": (
        'Free json flattener. Free online JSON flattener. Convert n.... No registration required.',
        'Free online JSON flattener. Convert nested JSON objects into flat key-value pairs using dot notation. Ideal for CSV export, database imports, and data analysis. Paste JSON and get flattened output instantly.'
    ),
    "en/pdf-crop-page/index.html": (
        'Free pdf crop pages. Free online PDF page cropping tool. P.... No registration required.',
        'Free online PDF page cropping tool. Upload a PDF and crop individual pages by specifying margins — remove whitespace, trim borders, and resize pages. All processing happens in your browser, no file upload to servers.'
    ),
    "en/json-comparer/index.html": (
        'Free json diff tool. Free online JSON diff tool. Compare t.... No registration required.',
        'Free online JSON diff tool. Compare two JSON objects side by side and highlight differences — added, removed, and changed fields. Perfect for API response comparison, config diffing, and debugging.'
    ),
    "en/case-converter/index.html": (
        'Free case converter. Free online case converter tool. Conv.... No registration required.',
        'Free online case converter. Transform text between uppercase, lowercase, title case, sentence case, camelCase, PascalCase, snake_case, and kebab-case. Paste text and convert instantly — no signup needed.'
    ),
    "en/pantone-to-hex/index.html": (
        'Free pantone to hex. Free online Pantone To Hex tool. Pure.... No registration required.',
        'Free online Pantone to HEX color converter. Look up Pantone color codes and convert them to HEX, RGB, and CMYK values. Perfect for designers bridging print and digital color workflows.'
    ),
    "en/phone-validator/index.html": (
        'Free phone validator. Free online phone number validator. V.... No registration required.',
        'Free online phone number validator. Check if a phone number is valid, identify the country and carrier, and format it to international standards. Supports 200+ countries — no signup required.'
    ),
    "en/vigenere-cipher/index.html": (
        'Free vigenere cipher. Free online Vigenere Cipher encryptio.... No registration required.',
        'Free online Vigenère Cipher encoder and decoder. Encrypt or decrypt messages using the classic polyalphabetic substitution cipher. Enter your text and secret key — all processing happens in your browser.'
    ),
    "en/html-beautifier/index.html": (
        'Free html beautifier. Free online HTML beautifier and forma.... No registration required.',
        'Free online HTML beautifier and formatter. Paste minified or messy HTML and get clean, indented, readable code instantly. Customize indent size, wrap attributes, and sort classes — no signup needed.'
    ),
    "en/calorie-tracker/index.html": (
        'Free calorie tracker. Free online calorie tracker for daily.... No registration required.',
        'Free online calorie tracker for daily food logging. Search foods, track calories, macros, and nutrients. Set daily goals and monitor progress — all data stored locally in your browser, no account required.'
    ),
    "en/mole-calculator/index.html": (
        'Free mole calculator. Free online mole calculator. Convert .... No registration required.',
        'Free online mole calculator for chemistry. Convert between mass, moles, and molar mass. Calculate molarity, dilution factors, and molecular weight. Essential tool for students and lab professionals.'
    ),
    "en/screenshot-tool/index.html": (
        'Free screenshot tool. Free online screenshot tool. Capture .... No registration required.',
        'Free online screenshot tool. Capture webpage screenshots by URL — full page or visible area. Download as PNG. No browser extension or software install needed, works directly in your browser.'
    ),
    "en/regex-explainer/index.html": (
        'Free regex explainer. Free online regex explainer — breaks .... No registration required.',
        'Free online regex explainer. Paste any regular expression and get a plain-English breakdown of each component. Understand what your regex matches, with color-coded syntax highlighting and match testing.'
    ),
    "en/regex-generator/index.html": (
        'Free regex generator. Free online regex generator. Instantl.... No registration required.',
        'Free online regex generator. Describe what you want to match in plain English and get the corresponding regular expression. Supports email, URL, phone, date patterns and custom requirements — no signup needed.'
    ),
}

base_dir = '/home/chison/tools-site'
fixed = 0

for path, (old_prefix, new_desc) in FIXES.items():
    full_path = os.path.join(base_dir, path)
    if not os.path.exists(full_path):
        print(f"MISSING: {full_path}")
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the description
    # The description is in: <meta name="description" content="OLD">
    old_full = f'<meta name="description" content="{old_prefix}"'
    new_full = f'<meta name="description" content="{new_desc}"'
    
    if old_full in content:
        content = content.replace(old_full, new_full)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK [{len(new_desc)}] {path}")
        fixed += 1
    else:
        # Try with escaped quotes
        print(f"NOT FOUND (exact): {path}")
        # Find the actual line
        for line in content.split('\n'):
            if 'name="description"' in line:
                print(f"  Actual: {line.strip()[:120]}...")
                break

print(f"\nFixed: {fixed}/{len(FIXES)}")