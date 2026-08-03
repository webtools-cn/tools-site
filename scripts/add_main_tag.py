#!/usr/bin/env python3
"""
为工具页面添加 <main> 语义化标签。
策略：找到 body 后第一个 <div class="container"> 改为 <main class="container">，
找到其对应的闭合 </div> 改为 </main>。

也处理首页和其他特殊页面。
"""
import re
import sys
import os

def find_matching_close(lines, start_idx):
    """从 start_idx 开始，找到 div 的匹配闭合标签"""
    balance = 0
    for i in range(start_idx, len(lines)):
        line = lines[i]
        # Count opening divs (but not self-closing or in JS strings)
        opens = len(re.findall(r'<div[\s>]', line))
        closes = len(re.findall(r'</div>', line))
        balance += opens - closes
        if balance == 0 and i > start_idx:
            return i
    return None

def fix_main_tag(filepath, dry_run=False):
    """为文件添加 main 标签"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if already has <main> tag
    if re.search(r'<main[\s>]', content):
        return False, "Already has <main>"
    
    lines = content.split('\n')
    
    # Pattern 1: <div class="container"> right after <body>
    container_idx = None
    for i, line in enumerate(lines):
        if '<body' in line:
            # Search next few lines for container
            for j in range(i+1, min(i+5, len(lines))):
                if '<div class="container">' in lines[j] or '<div class="container" ' in lines[j]:
                    container_idx = j
                    break
            break
    
    if container_idx is None:
        # Try pattern: first <div class="container"> in body
        in_body = False
        for i, line in enumerate(lines):
            if '<body' in line:
                in_body = True
            if in_body and ('<div class="container">' in line or '<div class="container" ' in line):
                container_idx = i
                break
    
    if container_idx is None:
        return False, "No container div found"
    
    # Find matching close
    close_idx = find_matching_close(lines, container_idx)
    if close_idx is None:
        return False, "Could not find matching close tag"
    
    # Replace opening tag
    old_open = lines[container_idx]
    if '<div class="container">' in old_open:
        new_open = old_open.replace('<div class="container">', '<main class="container">')
    elif '<div class="container" ' in old_open:
        new_open = old_open.replace('<div class="container"', '<main class="container"', 1)
    else:
        return False, "Unexpected container format"
    
    # Replace closing tag - need to be precise
    old_close = lines[close_idx]
    # The closing div should be the last </div> on that line that matches our container
    # Simple case: line is just </div>
    if old_close.strip() == '</div>':
        new_close = old_close.replace('</div>', '</main>')
    else:
        # Line has other content - replace the specific </div> that closes container
        # Find the position of the closing </div> by counting backwards
        # For safety, replace the last </div> on the line
        idx = old_close.rfind('</div>')
        new_close = old_close[:idx] + '</main>' + old_close[idx+6:]
    
    if dry_run:
        print(f"  Would change line {container_idx+1}: {old_open.strip()[:80]}")
        print(f"    -> {new_open.strip()[:80]}")
        print(f"  Would change line {close_idx+1}: {old_close.strip()[:80]}")
        print(f"    -> {new_close.strip()[:80]}")
        return True, "Dry run OK"
    
    lines[container_idx] = new_open
    lines[close_idx] = new_close
    
    new_content = '\n'.join(lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True, f"Fixed: line {container_idx+1} and {close_idx+1}"

def main():
    # Priority: failing URLs first
    failing_urls = [
        "tax-calculator", "checksum-calculator", "business-days-calculator",
        "mac-address-lookup", "vin-decoder", "unicode-lookup", "token-estimator",
        "sql-explainer", "reaction-test", "gpa-calculator", "compound-interest-calculator",
        "running-pace-calculator", "metronome-online", "speed-test", "wifi-password-generator",
        "en/backwards-text", "en/website-status-checker",
    ]
    
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print("=== DRY RUN MODE ===\n")
        for url in failing_urls[:3]:  # Test first 3
            fpath = f"{url}/index.html"
            if os.path.exists(fpath):
                print(f"\n{fpath}:")
                fix_main_tag(fpath, dry_run=True)
        # Also test homepage
        print(f"\nindex.html (homepage):")
        fix_main_tag("index.html", dry_run=True)
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--failing-only':
        print("=== Fixing failing URLs ===\n")
        fixed = 0
        failed = 0
        for url in failing_urls:
            fpath = f"{url}/index.html"
            if os.path.exists(fpath):
                ok, msg = fix_main_tag(fpath)
                if ok:
                    print(f"✅ {fpath}: {msg}")
                    fixed += 1
                else:
                    print(f"❌ {fpath}: {msg}")
                    failed += 1
        
        # Also fix homepage
        ok, msg = fix_main_tag("index.html")
        if ok:
            print(f"✅ index.html: {msg}")
            fixed += 1
        else:
            print(f"❌ index.html: {msg}")
            failed += 1
        
        # Fix EN homepage too
        ok, msg = fix_main_tag("en/index.html")
        if ok:
            print(f"✅ en/index.html: {msg}")
            fixed += 1
        else:
            print(f"❌ en/index.html: {msg}")
            failed += 1
        
        print(f"\n=== Summary: {fixed} fixed, {failed} failed ===")
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        print("=== Fixing ALL pages ===\n")
        fixed = 0
        failed = 0
        skipped = 0
        
        # Find all index.html files
        for root, dirs, files in os.walk('.'):
            if '.git' in root:
                continue
            for fname in files:
                if fname == 'index.html':
                    fpath = os.path.join(root, fname)
                    ok, msg = fix_main_tag(fpath)
                    if ok:
                        fixed += 1
                    elif 'Already has' in msg:
                        skipped += 1
                    else:
                        failed += 1
                        if failed <= 10:
                            print(f"❌ {fpath}: {msg}")
        
        print(f"\n=== Summary: {fixed} fixed, {skipped} skipped, {failed} failed ===")

if __name__ == '__main__':
    main()
