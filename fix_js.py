#!/usr/bin/env python3
"""Fix JS syntax errors in tool index.html files by analyzing the extracted JS."""

import subprocess
import sys
import os
import re

os.chdir('/home/chison/tools-site')

TOOLS = [
    "pdf-page-extractor", "pdf-to-excel", "pdf-to-html", "pdf-to-jpg", "pdf-to-ppt",
    "piano-keyboard", "pie-chart-maker", "privacy-policy-generator", "properties-to-yaml",
    "quiz-generator", "radar-chart-maker", "random-password-generator", "receipt-generator",
    "regex-character-class-generator", "regex-cheatsheet", "rot13-converter",
    "scatter-plot-maker", "schema-generator", "seo-meta-generator", "shopping-list-generator",
    "sitemap-validator", "snake-game", "social-share-link-generator", "spectrum-analyzer",
    "sql-migration-generator", "sql-to-csv", "sql-to-json", "sql-to-kysely", "sql-to-prisma",
    "svg-color-changer", "svg-to-data-uri", "swot-analysis-generator", "tdee-calculator",
    "terms-generator", "text-diff-checker", "text-normalizer", "text-palindrome-checker",
    "text-readability-analyzer", "text-sentiment-analyzer", "text-to-braille", "tic-tac-toe",
    "tsv-to-csv", "unique-id-generator", "username-generator", "video-compress",
    "vite-config-generator", "whois-lookup", "word-search-generator", "word-to-pdf",
    "workout-generator", "yes-no-generator"
]

def check_js(tool):
    """Extract JS and check syntax, return (ok, error_message)."""
    js_path = f"/tmp/{tool}.js"
    html_path = f"{tool}/index.html"
    subprocess.run(["python3", "scripts/extract_js.py", html_path, "-o", js_path], 
                   capture_output=True)
    # Actually the script prints to stdout
    with open(js_path, 'w') as f:
        result = subprocess.run(["python3", "scripts/extract_js.py", html_path], 
                              capture_output=True, text=True)
        f.write(result.stdout)
    
    result = subprocess.run(["node", "-c", js_path], capture_output=True, text=True)
    if result.returncode == 0:
        return True, ""
    return False, result.stderr.strip()

# First pass: identify all broken tools
broken = []
ok_tools = []
for tool in TOOLS:
    ok, err = check_js(tool)
    if ok:
        ok_tools.append(tool)
    else:
        broken.append((tool, err))
        print(f"ERR: {tool}")

print(f"\n{len(ok_tools)} OK, {len(broken)} broken")
for tool, err in broken:
    print(f"\n=== {tool} ===")
    print(err)
