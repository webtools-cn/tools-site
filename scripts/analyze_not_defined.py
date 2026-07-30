#!/usr/bin/env python3
"""分析并修复 'xxx is not defined' 错误
策略：对于每个失败工具，找到报错的函数名，
如果onclick引用的函数确实没定义，就创建一个最小的函数stub暴露到window。
"""

import json, re, os, sys

BASE = '/home/chison/tools-site'

with open(f'{BASE}/quality-reports/puppeteer-L0.json') as f:
    data = json.load(f)

# 提取 "is not defined" 的函数名
fnf = []
for t in data['failures']:
    m = re.search(r'(\w+) is not defined \(event handler\)', t['reason'])
    if m:
        fnf.append((t['tool'], m.group(1)))

print(f"共 {len(fnf)} 个 'not defined' 错误")
for tool, fn in fnf[:30]:
    print(f"  {tool}: {fn}")
