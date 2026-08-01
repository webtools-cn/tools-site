#!/usr/bin/env python3
"""Fix remaining short/empty English descriptions - handles multiline and edge cases."""
import os
import re
import glob

BASE = '/home/chison/tools-site'

# Tool-specific descriptions for missing/broken pages
TOOL_DESCRIPTIONS = {
    'binary-to-hex': 'Convert binary to hexadecimal instantly with our free online converter. Real-time conversion, supports space-separated input. No registration required.',
    'character-frequency-analyzer': 'Analyze character frequency in any text online for free. Count letters, digits, and special characters. Perfect for cryptography and text analysis.',
    'color-name-to-hex': 'Convert color names to hex codes and vice versa. Free online color name converter with 140+ named colors. Perfect for web designers and developers.',
    'cron-validator': 'Validate cron expressions online for free. Check syntax and see next scheduled run times. Essential for developers and system administrators.',
    'csv-sql-query': 'Run SQL queries on CSV data online for free. Query your spreadsheet data with standard SQL syntax. No database setup required.',
    'csv-statistics': 'Calculate statistics from CSV data online for free. Mean, median, mode, standard deviation, and more. Analyze your data instantly.',
    'data': 'Free online data conversion tools — JSON, CSV, YAML, XML, and more. Convert, format, and validate your data formats in seconds.',
    'dns-propagation-checker': 'Check DNS propagation status worldwide. Free online tool to verify DNS changes across multiple global locations. Monitor your domain updates.',
    'env-generator': 'Generate environment configuration files online for free. Create .env files with variables, defaults, and documentation. Perfect for project setup.',
    'git-cheatsheet': 'Quick reference for Git commands and workflows. Free online Git cheat sheet with common commands, branching strategies, and troubleshooting tips.',
    'ini-editor': 'Edit INI configuration files online for free. Visual section and key-value editor with syntax validation. Perfect for config file management.',
    'ip-range-calculator': 'Calculate IP address ranges, subnets, and CIDR notation. Free online IP range calculator for network administrators and DevOps engineers.',
    'json-to-typescript': 'Free online JSON to TypeScript interface generator. Convert JSON data to type-safe TypeScript interfaces instantly. Save development time.',
    'loading-spinner-generator': 'Create CSS loading spinner animations online for free. Choose from 20+ spinner styles with customizable colors and sizes. Copy clean CSS code.',
    'manifest-generator': 'Generate web app manifest.json files online for free. Configure PWA settings, icons, and theme colors. Visual manifest builder.',
    'media': 'Free online media tools — image converters, compressors, editors, and more. Process your images, audio, and video files in the browser.',
    'mock-data-generator': 'Generate realistic mock data for testing and development. Free online mock data generator with customizable schemas. Create users, orders, and more.',
    'morse-to-text': 'Free online Morse code to text decoder. Convert dots and dashes back to readable text. Quick, accurate, and works entirely in your browser.',
    'octal-decimal-converter': 'Convert between octal and decimal numbers instantly. Free online octal to decimal converter with step-by-step conversion. Learn number systems.',
    'office': 'Free online office productivity tools — PDF editors, document converters, calculators, and more. Boost your workflow with browser-based utilities.',
    'palette-extractor': 'Extract color palettes from images online for free. Upload any image to get dominant colors and hex codes. Perfect for designers and branding.',
    'pdf-merge': 'Merge multiple PDF files into one document online for free. Combine PDFs in any order with drag-and-drop simplicity. No signup required.',
    'pdf-split': 'Split PDF files into separate pages online for free. Extract specific pages or split by page ranges. Fast browser-based PDF splitting.',
    'readability-score': 'Check text readability scores online for free. Flesch-Kincaid, Gunning Fog, and SMOG indices. Ensure your content is at the right reading level.',
    'savings-goal-calculator': 'Plan your savings goals with our free online calculator. Calculate monthly contributions needed to reach your target. Visual savings tracker.',
    'srt-editor': 'Edit SRT subtitle files online for free. Adjust timing, fix sync issues, and modify text. Perfect for video content creators.',
    'svg-to-jsx': 'Free online SVG to JSX/React component converter. Transform SVG markup into React-ready JSX components instantly. No signup needed.',
    'toml-to-yaml': 'Convert TOML configuration files to YAML format. Free online TOML to YAML converter with instant results. Perfect for config migration.',
    'uuid-generator': 'Generate UUID v4 identifiers online for free. Create unique universal IDs for databases, APIs, and distributed systems. Instant generation.',
    'whois-lookup': 'Free online WHOIS domain lookup tool. Check domain registration details, expiration dates, and registrar information instantly.',
    'xml-to-csv-converter': 'Free online XML to CSV converter. Transform XML data into spreadsheet-ready CSV format. Perfect for data analysis and Excel import.',
}

def fix_single_file(filepath):
    dirname = os.path.basename(os.path.dirname(filepath))
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Get new description
    new_desc = TOOL_DESCRIPTIONS.get(dirname)
    if not new_desc:
        # Use title as fallback
        m = re.search(r'<title>(.*?)(?:\s*[-–—|]\s*Free ToolBase)?</title>', content, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
            new_desc = f"Free online {title.lower()} tool. Fast, secure, and no registration required. Works entirely in your browser."
        else:
            return False
    
    # Handle multiline meta description - replace from <meta name="description" to next >
    # Match meta description that may span multiple lines
    new_content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"',
        f'<meta name="description" content="{new_desc}"',
        content,
        flags=re.DOTALL
    )
    
    if new_content == content:
        # Try multiline match
        new_content = re.sub(
            r'<meta\s+name="description"\s+content=".*?"',
            f'<meta name="description" content="{new_desc}"',
            content,
            flags=re.DOTALL
        )
    
    # Also fix OG and twitter descriptions
    new_content = re.sub(
        r'<meta\s+property="og:description"\s+content=".*?"',
        f'<meta property="og:description" content="{new_desc}"',
        new_content,
        flags=re.DOTALL
    )
    new_content = re.sub(
        r'<meta\s+name="twitter:description"\s+content=".*?"',
        f'<meta name="twitter:description" content="{new_desc}"',
        new_content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    return True

def main():
    files = glob.glob(os.path.join(BASE, 'en/*/index.html'))
    fixed = 0
    for f in sorted(files):
        if fix_single_file(f):
            fixed += 1
    
    print(f"Processed: {fixed}/{len(files)}")

if __name__ == '__main__':
    main()