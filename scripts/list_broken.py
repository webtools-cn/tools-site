#!/usr/bin/env python3
"""对broken工具重新生成核心内容，然后用模板重新组装"""
import subprocess, re, os, json

BROKEN_REMAINING = [
    "ai-fine-tuning-cost-calculator","dns-record-comparator","dockerfile-formatter",
    "dockerfile-linter","fancy-text-generator","flexbox-layout-generator",
    "handwriting-generator","html-entity-converter","html-meta-refresh-generator",
    "html-table-of-contents","html-table-to-json","html-tag-stripper",
    "html-wysiwyg-editor","http-cache-header-generator",
    "markdown-link-checker","markdown-previewer","markdown-to-pdf-converter",
    "maze-generator","md5-generator","meta-tag-generator","morse-code",
    "name-generator","pdf-to-html",
    "privacy-policy-generator","properties-to-yaml","quiz-generator","receipt-generator",
    "regex-cheatsheet","shopping-list-generator",
    "sitemap-validator","sql-migration-generator","sql-to-csv","sql-to-kysely",
    "sql-to-prisma","svg-to-data-uri","terms-generator",
    "text-normalizer","text-palindrome-checker","text-to-braille","typing-test",
    "vite-config-generator","word-search-generator","workout-generator","yaml-to-json"
]

print(f"Remaining broken tools: {len(BROKEN_REMAINING)}")
for i, t in enumerate(BROKEN_REMAINING, 1):
    print(f"{i}. {t}")

# Read each tool to extract metadata
for tool in BROKEN_REMAINING[:3]:  # Just show first 3 as example
    path = f'{tool}/index.html'
    if not os.path.exists(path):
        print(f"{tool}: NO FILE")
        continue
    with open(path) as f:
        c = f.read()
    # Extract title
    m = re.search(r'<title>(.*?)</title>', c)
    title = m.group(1) if m else 'N/A'
    # Extract description
    m = re.search(r'<meta name="description" content="([^"]*)"', c)
    desc = m.group(1)[:80] if m else 'N/A'
    print(f"\n{tool}:")
    print(f"  Title: {title}")
    print(f"  Desc: {desc}")
