#!/usr/bin/env python3
"""
工具可行性检查 v1.0
开发前必须运行，检查：
1. 纯前端能不能做（CORS/浏览器限制）
2. 是否与现有工具重复
"""
import os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git',
        'about','contact','terms','privacy','node_modules'}

IMPOSSIBLE_PATTERNS = {
    'port-scanner': '浏览器无法扫描端口',
    'traceroute': '浏览器无法traceroute',
    'whois': '需WHOIS API',
    'dns-lookup': '需DNS API',
    'dns-propagation': '需DNS API',
    'dns-record': '需DNS API',
    'backlink-check': '需SEO API',
    'domain-authority': '需SEO API',
    'domain-availability': '需WHOIS API',
    'ssl-check': '需服务端验证证书',
    'ssl-expiry': '需服务端验证',
    'uptime-check': '需服务端持续监控',
    'website-status': '需CORS代理',
    'server-status': '需CORS代理',
    'broken-link': '需逐个fetch→CORS',
    'speed-test': '需服务端测速(但click/typing/reading/network-speed纯前端可做)',
    'redirect-trace': '需CORS代理',
    'redirect-check': '需CORS代理',
    'security-header': '需CORS代理',
    'docx-to-pdf': '需后端转换',
    'xlsx-to-pdf': '需后端转换',
    'word-to-pdf': '需后端转换',
    'html-to-docx': '需后端',
    'ebook-convert': '需后端',
    'video-convert': '需后端/FFmpeg',
    'audio-convert': '需后端/FFmpeg',
    'image-denoise': '需大计算/AI',
    'image-upscale': '需AI模型',
    'image-to-cartoon': '需AI模型',
    'background-remov': '需AI模型',
    'image-remove-bg': '需AI模型',
    'image-oil-paint': '需复杂算法',
}

# 精确白名单：名字含不可行关键词但纯前端完全可行
FEASIBLE_WHITELIST = {
    'click-speed-test', 'typing-speed-test', 'reading-speed-test',
    'network-speed-test', 'download-speed-test', 'upload-speed-test',
}

def check_feasibility(tool_name):
    if tool_name in FEASIBLE_WHITELIST:
        return True, 'OK'
    for pattern, reason in IMPOSSIBLE_PATTERNS.items():
        if pattern in tool_name:
            return False, reason
    return True, 'OK'

def check_duplicate(tool_name):
    tools = []
    for d in sorted(os.listdir(SITE)):
        if d in SKIP or d.startswith('.'): continue
        if os.path.isfile(os.path.join(SITE, d, 'index.html')):
            tools.append(d)
    parts = tool_name.split('-')
    skip_words = {'online','free','tool','generator','calculator','converter','checker','maker','builder'}
    core_parts = [p for p in parts if len(p) > 2 and p not in skip_words]
    duplicates = []
    # 要求2+核心词重叠，或单核心词完全包含
    for existing in tools:
        if existing == tool_name:
            duplicates.append((existing, '完全同名'))
            continue
        ep = existing.split('-')
        ecore = [p for p in ep if len(p)>2 and p not in skip_words]
        common = set(core_parts) & set(ecore)
        if len(common) >= 2 or (len(core_parts)==1 and core_parts[0] in ep):
            duplicates.append((existing, f'关键词重叠: {common}'))
    return duplicates

def scan_existing_impossible():
    results = []
    for d in sorted(os.listdir(SITE)):
        if d in SKIP or d.startswith('.'): continue
        path = os.path.join(SITE, d, 'index.html')
        if not os.path.isfile(path): continue
        feasible, reason = check_feasibility(d)
        if not feasible:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
            has_noindex = 'noindex' in c
            results.append({'tool': d, 'reason': reason, 'noindex': has_noindex})
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
        feasible, reason = check_feasibility(name)
        dups = check_duplicate(name)
        print(f"工具名: {name}")
        print(f"可行性: {'✅ 可行' if feasible else '❌ 不可行 - ' + reason}")
        if dups:
            print(f"重复检查: ❌ 发现{len(dups)}个相似工具")
            for d, r in dups[:5]:
                print(f"  → {d} ({r})")
        else:
            print(f"重复检查: ✅ 无重复")
        if not feasible or dups:
            print(f"\n🚫 建议不要开发此工具！")
            sys.exit(1)
        else:
            print(f"\n✅ 可以开发")
            sys.exit(0)
    else:
        results = scan_existing_impossible()
        no_noindex = [r for r in results if not r['noindex']]
        print(f"不可行工具: {len(results)}个")
        print(f"  已noindex: {len(results)-len(no_noindex)}个")
        print(f"  未noindex: {len(no_noindex)}个")
        for r in no_noindex:
            print(f"  ❌ {r['tool']}: {r['reason']}")
