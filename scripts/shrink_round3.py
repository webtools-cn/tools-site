#!/usr/bin/env python3
"""Round 3: Aggressive shrink to under 160 chars."""
import os, re

FIXES = {
    "en/vision-test/index.html": (
        "Free vision test using Snellen chart. Check visual acuity at home — read letters of decreasing size to estimate eyesight. Not a substitute for professional eye exams. No signup needed.",
        "Free vision test using Snellen chart. Check visual acuity at home — read decreasing letters to estimate eyesight. Not a substitute for professional eye exams."
    ),
    "en/emoji-to-image/index.html": (
        "Free emoji to image converter. Turn emoji into downloadable PNG images. Choose size, background, export format. Perfect for social media, presentations, and design — no signup needed.",
        "Free emoji to image converter. Turn emoji into downloadable PNG images. Choose size, background, export format. Perfect for social media, presentations, and design projects."
    ),
    "en/mole-calculator/index.html": (
        "Free mole calculator for chemistry. Convert between mass, moles, and molar mass. Calculate molarity, dilution factor, molecular weight. Essential for students and lab professionals.",
        "Free mole calculator for chemistry. Convert mass, moles, and molar mass. Calculate molarity, dilution factor, molecular weight. Essential for students and lab professionals."
    ),
    "en/online-clock/index.html": (
        "Free online clock with analog and digital displays. View current time in full-screen mode with dark theme. Perfect for presentations, time tracking, and focus sessions — no signup.",
        "Free online clock with analog and digital displays. View current time in full-screen with dark theme. Perfect for presentations, time tracking, and focus sessions."
    ),
    "en/interval-timer/index.html": (
        "Free interval timer for HIIT, Tabata, circuit training, and study sessions. Set work/rest intervals and rounds with audio alerts. Works on mobile and desktop — no app install.",
        "Free interval timer for HIIT, Tabata, and study sessions. Set work/rest intervals and rounds with audio alerts. Works on mobile and desktop — no app install needed."
    ),
    "en/json-comparer/index.html": (
        "Free JSON diff tool. Compare two JSON objects side by side — highlight added, removed, and changed fields. Perfect for API response comparison, config diffing, and debugging.",
        "Free JSON diff tool. Compare JSON objects side by side — highlight added, removed, and changed fields. Ideal for API response comparison, config diffing, and debugging."
    ),
    "en/csp-generator/index.html": (
        "Free CSP generator. Build Content Security Policy headers visually — configure script-src, style-src, img-src and more. Generate ready-to-use HTTP headers for your website.",
        "Free CSP generator. Build Content Security Policy headers visually — configure script-src, style-src, img-src and more. Generate ready-to-use HTTP headers."
    ),
    "en/pantone-to-hex/index.html": (
        "Free Pantone to HEX converter. Look up Pantone codes and convert to HEX, RGB, and CMYK. Perfect for designers bridging print and digital color workflows — no signup needed.",
        "Free Pantone to HEX converter. Look up Pantone codes and convert to HEX, RGB, and CMYK. Perfect for designers bridging print and digital color workflows."
    ),
    "en/sql-to-kysely/index.html": (
        "Free SQL to Kysely converter. Transform SQL into type-safe Kysely TypeScript. Supports SELECT, INSERT, UPDATE, DELETE — paste SQL and get Kysely code instantly, no signup.",
        "Free SQL to Kysely converter. Transform SQL into type-safe TypeScript. Supports SELECT, INSERT, UPDATE, DELETE — paste and get Kysely code instantly."
    ),
    "en/url-builder/index.html": (
        "Free URL builder. Construct and encode URLs with query parameters. Add key-value pairs, encode special chars, generate clean URLs for web dev and API testing — no signup.",
        "Free URL builder. Construct and encode URLs with query parameters. Add key-value pairs, encode special chars, generate clean URLs for web dev and API testing."
    ),
    "en/json-flattener/index.html": (
        "Free JSON flattener. Convert nested JSON to flat key-value pairs with dot notation for CSV export, database imports, and data analysis. Paste and get results instantly.",
        "Free JSON flattener. Convert nested JSON to flat key-value pairs with dot notation for CSV export, database imports, and data analysis."
    ),
    "en/svg-to-base64/index.html": (
        "Free SVG to Base64 converter. Paste SVG code and get a Base64 data URI for embedding in HTML, CSS, or Markdown. Instant conversion with copy-to-clipboard — no uploads.",
        "Free SVG to Base64 converter. Paste SVG code and get a Base64 data URI for embedding in HTML, CSS, or Markdown. Instant with copy-to-clipboard."
    ),
    "en/shuffle-lines/index.html": (
        "Free line shuffler. Randomize text line order instantly — ideal for raffle draws, test questions, playlist shuffling, and data sampling. Paste and get shuffled output.",
        "Free line shuffler. Randomize text line order instantly — ideal for raffle draws, test questions, playlist shuffling, and data sampling."
    ),
    "en/screenshot-tool/index.html": (
        "Free screenshot tool. Capture webpage screenshots by URL — full page or visible area. Download as PNG. No browser extension or install needed — works in your browser.",
        "Free screenshot tool. Capture webpage screenshots by URL — full page or visible area. Download as PNG. No extension or install needed."
    ),
    "en/xml-validator/index.html": (
        "Free XML validator. Paste XML to check syntax errors, mismatched tags, and structural issues. Get line-by-line error reports instantly — no uploads or signup needed.",
        "Free XML validator. Paste XML to check syntax errors, mismatched tags, and structural issues. Get line-by-line error reports instantly."
    ),
    "en/daily-planner/index.html": (
        "Free daily planner to organize your day. Schedule tasks by hour, set priorities, add notes, and track progress. All data stored in your browser — no signup required.",
        "Free daily planner to organize your day. Schedule tasks by hour, set priorities, add notes, and track progress. All data stored in your browser."
    ),
    "en/video-cropper/index.html": (
        "Free video cropper. Trim and crop videos in your browser — set start/end times, adjust aspect ratio, download instantly. Client-side processing, no upload to server.",
        "Free video cropper. Trim and crop videos in your browser — set start/end times, adjust aspect ratio, download instantly. Client-side, no upload."
    ),
    "en/yaml-validator/index.html": (
        "Free YAML validator and formatter. Check syntax, fix indentation, validate structure, and beautify YAML output. Paste and get instant feedback — no signup required.",
        "Free YAML validator and formatter. Check syntax, fix indentation, validate structure, and beautify YAML output. Paste and get instant feedback."
    ),
    "en/regex-explainer/index.html": (
        "Free regex explainer. Paste a regex and get a plain-English breakdown of each component. Understand what it matches with syntax highlighting and live match testing.",
        "Free regex explainer. Paste a regex and get a plain-English breakdown of each component with syntax highlighting and live match testing."
    ),
    "en/case-converter/index.html": (
        "Free case converter. Transform text between uppercase, lowercase, title case, camelCase, snake_case and kebab-case. Paste and convert instantly — no signup needed.",
        "Free case converter. Transform text between uppercase, lowercase, title case, camelCase, snake_case and kebab-case. Paste and convert instantly."
    ),
    "en/calorie-tracker/index.html": (
        "Free calorie tracker for daily food logging. Search foods, track calories, macros, and nutrients. Set daily goals and monitor progress — all data stored locally.",
        "Free calorie tracker for daily food logging. Search foods, track calories, macros, and nutrients. Set daily goals — data stored locally in your browser."
    ),
}

base = '/home/chison/tools-site'
fixed = 0
for path, (old_desc, new_desc) in FIXES.items():
    full = os.path.join(base, path)
    with open(full) as f:
        content = f.read()
    
    old_line = f'<meta name="description" content="{old_desc}"'
    new_line = f'<meta name="description" content="{new_desc}"'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(full, 'w') as f:
            f.write(content)
        status = "OK" if len(new_desc) <= 160 else f"STILL {len(new_desc)}"
        print(f"[{status}] [{len(new_desc)}] {path}")
        fixed += 1
    else:
        print(f"NOT FOUND: {path}")
        m = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]+)"', content)
        if m:
            print(f"  actual ({len(m.group(1))}): {m.group(1)[:80]}...")

print(f"\nFixed: {fixed}/{len(FIXES)}")
PYEOF