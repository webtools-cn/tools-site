#!/usr/bin/env python3
"""批量验证修复后的工具"""
import subprocess

tools = [
    # Illegal return
    'avif-to-jpg','bandwidth-calculator','banner-generator','base32-encode-decode',
    'csv-to-markdown-table','csv-transposer','dev','hex-calculator',
    'json-to-elixir','json-to-protobuf','jwt-parser','markdown-slides',
    'markdown-to-pdf-converter','mock-data-generator','network','pattern-generator',
    'pdf-add-image','pdf-ocr','roman-to-decimal','rust-formatter',
    'semantic-version-parser','sql-query-builder',
    # container
    'ai-sentence-rewriter','audio-normalize','audio-volume-adjuster',
    'bitwise-calculator','cagr-calculator','cidr-calculator',
    'data-url-converter','decimal-to-roman','email-security-checker',
    'excel-to-pdf','favicon-downloader','hex-encoder-decoder',
    'hsl-to-rgb','ico-converter','image-resize','jpg-to-webp',
    'json-merge-patch','json-to-table','log-viewer','md5-hash',
]

passed = []
failed = []

for tool in tools:
    result = subprocess.run(
        ['node', 'tests/puppeteer_test.js', '--level', 'L0', '--tool', tool],
        capture_output=True, text=True, timeout=60,
        cwd='/home/chison/tools-site'
    )
    if '100.0%' in result.stdout:
        passed.append(tool)
        print(f'✅ {tool}')
    else:
        for line in result.stdout.split('\n'):
            if '❌' in line:
                print(f'❌ {tool}: {line.strip()[:80]}')
                break
        else:
            print(f'❌ {tool}: unknown')
        failed.append(tool)

print(f'\n通过: {len(passed)}/{len(tools)}, 失败: {len(failed)}')
print(f'通过率: {len(passed)/len(tools)*100:.1f}%')