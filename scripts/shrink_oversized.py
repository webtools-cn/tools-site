#!/usr/bin/env python3
"""Aggressively shrink oversized meta descriptions to 140-155 chars."""
import os, re

# Map: path -> (old_prefix_for_finding, new_compact_description)
FIXES = {
    "en/pdf-crop-page/index.html": (
        "Free online PDF page cropping tool. Upload a PDF and crop pages by specifying margins",
        "Free PDF page cropper. Upload a PDF and crop pages by setting margins — remove whitespace, trim borders, resize. All browser-based, no file upload to servers."
    ),
    "en/json-flattener/index.html": (
        "Free online JSON flattener. Convert nested JSON into flat key-value pairs using dot notation. Ideal for CSV export, database imports, and data analysis",
        "Free JSON flattener. Convert nested JSON to flat key-value pairs with dot notation for CSV export, database imports, and data analysis. Paste and get results instantly."
    ),
    "en/csp-generator/index.html": (
        "Free CSP generator — build secure Content Security Policy headers visually. Configure script-src, style-src, img-src and more. Generate ready-to-use HTTP headers for your website.",
        "Free CSP generator. Build Content Security Policy headers visually — configure script-src, style-src, img-src and more. Generate ready-to-use HTTP headers for your website."
    ),
    "en/calorie-tracker/index.html": (
        "Free online calorie tracker for daily food logging. Search foods, track calories, macros, and nutrients. Set daily goals",
        "Free calorie tracker for daily food logging. Search foods, track calories, macros, and nutrients. Set daily goals and monitor progress — all data stored locally."
    ),
    "en/vigenere-cipher/index.html": (
        "Free Vigenère Cipher encoder and decoder. Encrypt or decrypt messages using the classic polyalphabetic substitution cipher. Enter text and secret key",
        "Free Vigenère cipher encoder and decoder. Encrypt or decrypt messages with the classic polyalphabetic cipher. Enter text and secret key — all in your browser."
    ),
    "en/daily-planner/index.html": (
        "Free online daily planner to organize your day. Schedule tasks by hour, set priorities, add notes, and track progress. All data stays in your browser",
        "Free daily planner to organize your day. Schedule tasks by hour, set priorities, add notes, and track progress. All data stored in your browser — no signup required."
    ),
    "en/case-converter/index.html": (
        "Free online case converter. Transform text between uppercase, lowercase, title case, camelCase, snake_case and kebab-case. Paste and convert instantly",
        "Free case converter. Transform text between uppercase, lowercase, title case, camelCase, snake_case and kebab-case. Paste and convert instantly — no signup needed."
    ),
    "en/shuffle-lines/index.html": (
        "Free online line shuffler. Randomize text line order instantly — useful for raffle draws, test questions, playlist shuffling, and data sampling. Paste and get shuffled output.",
        "Free line shuffler. Randomize text line order instantly — ideal for raffle draws, test questions, playlist shuffling, and data sampling. Paste and get shuffled output."
    ),
    "en/regex-explainer/index.html": (
        "Free online regex explainer. Paste a regular expression and get a plain-English breakdown of each component. Understand what your regex matches with syntax highlighting and match testing.",
        "Free regex explainer. Paste a regex and get a plain-English breakdown of each component. Understand what it matches with syntax highlighting and live match testing."
    ),
    "en/sql-to-kysely/index.html": (
        "Free SQL to Kysely converter. Transform SQL statements into type-safe Kysely TypeScript code. Supports SELECT, INSERT, UPDATE, DELETE",
        "Free SQL to Kysely converter. Transform SQL into type-safe Kysely TypeScript. Supports SELECT, INSERT, UPDATE, DELETE — paste SQL and get Kysely code instantly, no signup."
    ),
    "en/video-cropper/index.html": (
        "Free online video cropper. Trim and crop videos in your browser — set start/end times, adjust aspect ratio, download instantly. No upload to server, fully client-side.",
        "Free video cropper. Trim and crop videos in your browser — set start/end times, adjust aspect ratio, download instantly. Client-side processing, no upload to server."
    ),
    "en/interval-timer/index.html": (
        "Free interval timer for HIIT, Tabata, circuit training, and study sessions. Set work/rest intervals, rounds, audio alerts. Works on mobile and desktop",
        "Free interval timer for HIIT, Tabata, circuit training, and study sessions. Set work/rest intervals and rounds with audio alerts. Works on mobile and desktop — no app install."
    ),
    "en/html-beautifier/index.html": (
        "Free online HTML beautifier and formatter. Paste minified HTML and get clean, indented code instantly. Customize indent size, wrap attributes",
        "Free HTML beautifier. Paste minified HTML and get clean, indented code instantly. Customize indent size, wrap attributes — no signup needed."
    ),
    "en/mole-calculator/index.html": (
        "Free online mole calculator for chemistry. Convert between mass, moles, and molar mass. Calculate molarity, dilution, molecular weight. Essential for students and lab professionals.",
        "Free mole calculator for chemistry. Convert between mass, moles, and molar mass. Calculate molarity, dilution factor, molecular weight. Essential for students and lab professionals."
    ),
    "en/yaml-validator/index.html": (
        "Free online YAML validator and formatter. Check syntax, fix indentation, validate structure, and beautify YAML output. Paste code and get instant feedback",
        "Free YAML validator and formatter. Check syntax, fix indentation, validate structure, and beautify YAML output. Paste and get instant feedback — no signup required."
    ),
    "en/json-comparer/index.html": (
        "Free online JSON diff tool. Compare two JSON objects side by side, highlight added, removed, and changed fields. Perfect for API response comparison, config diffing, and debugging.",
        "Free JSON diff tool. Compare two JSON objects side by side — highlight added, removed, and changed fields. Perfect for API response comparison, config diffing, and debugging."
    ),
    "en/xml-validator/index.html": (
        "Free online XML validator. Paste XML to check syntax errors, mismatched tags, and structural issues. Get line-by-line error reports instantly",
        "Free XML validator. Paste XML to check syntax errors, mismatched tags, and structural issues. Get line-by-line error reports instantly — no uploads or signup needed."
    ),
    "en/emoji-to-image/index.html": (
        "Free online emoji to image converter. Turn emoji into downloadable PNG images. Choose size, background color, export format. Perfect for social media, presentations, and design.",
        "Free emoji to image converter. Turn emoji into downloadable PNG images. Choose size, background, export format. Perfect for social media, presentations, and design — no signup needed."
    ),
    "en/online-clock/index.html": (
        "Free online clock with analog and digital displays. View current time in full-screen mode with dark theme support. Perfect for presentations, time tracking, and focus sessions.",
        "Free online clock with analog and digital displays. View current time in full-screen mode with dark theme. Perfect for presentations, time tracking, and focus sessions — no signup."
    ),
    "en/svg-to-base64/index.html": (
        "Free SVG to Base64 converter. Paste SVG code and get a Base64 data URI for embedding in HTML, CSS, or Markdown. Instant conversion with copy-to-clipboard",
        "Free SVG to Base64 converter. Paste SVG code and get a Base64 data URI for embedding in HTML, CSS, or Markdown. Instant conversion with copy-to-clipboard — no uploads."
    ),
    "en/vision-test/index.html": (
        "Free online vision test using standard Snellen chart. Check visual acuity at home — read letters of decreasing size to estimate your eyesight. Not a substitute for professional eye exams.",
        "Free vision test using Snellen chart. Check visual acuity at home — read letters of decreasing size to estimate eyesight. Not a substitute for professional eye exams. No signup needed."
    ),
    "en/phone-validator/index.html": (
        "Free online phone number validator. Check if a phone number is valid, identify country and carrier, format to international standards. Supports 200+ countries",
        "Free phone number validator. Check validity, identify country and carrier, format to international standards. Supports 200+ countries — no signup required."
    ),
    "en/screenshot-tool/index.html": (
        "Free online screenshot tool. Capture webpage screenshots by URL — full page or visible area. Download as PNG. No browser extension or install needed",
        "Free screenshot tool. Capture webpage screenshots by URL — full page or visible area. Download as PNG. No browser extension or install needed — works in your browser."
    ),
    "en/url-builder/index.html": (
        "Free online URL builder. Construct and encode URLs with query parameters. Add key-value pairs, encode special chars, generate clean URLs for web development and API testing.",
        "Free URL builder. Construct and encode URLs with query parameters. Add key-value pairs, encode special chars, generate clean URLs for web dev and API testing — no signup."
    ),
    "en/pantone-to-hex/index.html": (
        "Free Pantone to HEX converter. Look up Pantone color codes and convert to HEX, RGB, and CMYK values. Perfect for designers bridging print and digital color workflows.",
        "Free Pantone to HEX converter. Look up Pantone codes and convert to HEX, RGB, and CMYK. Perfect for designers bridging print and digital color workflows — no signup needed."
    ),
    "en/line-sorter/index.html": (
        "Free online line sorter. Sort text lines A-Z, Z-A, by length, or randomly. Paste your list and get instant sorted results",
        "Free line sorter. Sort text lines A-Z, Z-A, by length, or randomly. Paste your list and get instant sorted results — no signup needed."
    ),
    "en/yaml-merger/index.html": (
        "Free online YAML merger. Combine multiple YAML files with deep merge support. Handle conflicts, merge arrays or objects. No signup",
        "Free YAML merger. Combine multiple YAML files with deep merge support. Handle conflicts, merge arrays and objects. Paste, merge, download instantly — no signup."
    ),
}

base = '/home/chison/tools-site'
for path, (old_prefix, new_desc) in FIXES.items():
    full = os.path.join(base, path)
    with open(full) as f:
        content = f.read()
    
    # Find the actual description line
    m = re.search(r'(<meta\s+name=["\']description["\']\s+content=")([^"]+)(")', content)
    if not m:
        print(f"NO META DESC: {path}")
        continue
    
    prefix = m.group(1)
    old_desc = m.group(2)
    suffix = m.group(3)
    
    if old_prefix in old_desc:
        new_line = prefix + new_desc + suffix
        content = content.replace(prefix + old_desc + suffix, new_line)
        with open(full, 'w') as f:
            f.write(content)
        print(f"OK [{len(new_desc)}] {path}")
    else:
        print(f"PREFIX NOT IN DESC: {path}")
        print(f"  looking: {old_prefix[:60]}")
        print(f"  actual:  {old_desc[:80]}")
