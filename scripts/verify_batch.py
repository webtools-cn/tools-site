#!/usr/bin/env python3
"""逐个验证修复后的工具"""
import subprocess
import sys

tools = [
    'avif-to-jpg','bandwidth-calculator','banner-generator','base32-encode-decode',
    'csv-to-markdown-table','csv-transposer','dev','hex-calculator',
    'json-to-elixir','json-to-protobuf','jwt-parser','markdown-slides',
    'markdown-to-pdf-converter','mock-data-generator','network','pattern-generator',
    'pdf-add-image','pdf-ocr','roman-to-decimal','rust-formatter',
    'semantic-version-parser','sql-query-builder'
]

passed = []
failed = []

for tool in tools:
    result = subprocess.run(
        ['node', 'tests/puppeteer_test.js', '--level', 'L0', '--tool', tool],
        capture_output=True, text=True, timeout=60,
        cwd='/home/chison/tools-site'
    )
    if '100.0%' in result.stdout or '1/1 通过' in result.stdout:
        passed.append(tool)
        print(f'✅ {tool}')
    else:
        # 提取失败原因
        for line in result.stdout.split('\n'):
            if '❌' in line:
                print(f'❌ {tool}: {line.strip()}')
                break
        else:
            print(f'❌ {tool}: {result.stdout[:100]}')
        failed.append(tool)

print(f'\n通过: {len(passed)}/{len(tools)}, 失败: {len(failed)}')
if failed:
    print(f'失败列表: {failed}')