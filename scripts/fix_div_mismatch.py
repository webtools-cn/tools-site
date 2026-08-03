#!/usr/bin/env python3
"""
批量修复HTML div标签不匹配问题 (v2)。
策略：
- diff > 0 (opens > closes): 在</body>前添加缺少的</div> — 安全
- diff < 0 (closes > opens): 找到多余的</div>并移除 — 需要更小心

⚠️ 只修复diff绝对值<=3的文件
"""
import re
import os
import glob
import sys

def fix_div_mismatch(filepath, dry_run=False):
    """修复单个文件的div不匹配"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # More precise div counting - exclude self-closing and template literals
    opens = len(re.findall(r'<div[^>]*>', content))
    closes = len(re.findall(r'</div>', content))
    diff = opens - closes
    
    if diff == 0:
        return None  # Already balanced
    
    if abs(diff) > 3:
        return f'SKIP (diff={diff} too large, needs manual fix)'
    
    if diff > 0:
        # Need to add diff </div> before </body> — safe
        # Use rfind to only replace the LAST </body> (avoid JS strings containing </body>)
        close_divs = '\n' + '</div>\n' * diff
        body_idx = content.rfind('</body>')
        if body_idx == -1:
            return 'SKIP (no </body> found)'
        new_content = content[:body_idx] + close_divs + content[body_idx:]
    else:
        # diff < 0: too many </div>
        # Strategy: find standalone </div> lines near the end (before </body>) and remove them
        abs_diff = abs(diff)
        
        body_close_idx = content.rfind('</body>')
        if body_close_idx == -1:
            return 'SKIP (no </body> found)'
        
        before_body = content[:body_close_idx]
        after_body = content[body_close_idx:]
        
        # Split into lines and work backwards
        lines = before_body.split('\n')
        removed = 0
        new_lines = []
        
        for line in reversed(lines):
            if removed >= abs_diff:
                new_lines.append(line)
                continue
            
            stripped = line.strip()
            # Only remove standalone </div> lines (nothing else on the line)
            if stripped == '</div>':
                removed += 1
                continue  # Skip this line entirely
            # Also handle </div> at end of line with only whitespace before
            elif re.match(r'^\s*</div>\s*$', line):
                removed += 1
                continue
            else:
                new_lines.append(line)
        
        new_lines.reverse()
        new_content = '\n'.join(new_lines) + after_body
    
    # Verify the fix worked
    new_opens = len(re.findall(r'<div[^>]*>', new_content))
    new_closes = len(re.findall(r'</div>', new_content))
    new_diff = new_opens - new_closes
    
    if new_diff != 0:
        return f'FAILED (was {diff}, now {new_diff})'
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return f'FIXED (was {opens}/{closes}, now {new_opens}/{new_closes})'


def main():
    dry_run = '--dry-run' in sys.argv
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    results = {'fixed': 0, 'skipped': 0, 'failed': 0, 'already_ok': 0}
    failed_files = []
    skipped_files = []
    
    for path in sorted(glob.glob(os.path.join(base_dir, '**/index.html'), recursive=True)):
        if 'node_modules' in path or '.git' in path:
            continue
        
        rel_path = os.path.relpath(path, base_dir)
        result = fix_div_mismatch(path, dry_run=dry_run)
        
        if result is None:
            results['already_ok'] += 1
        elif result.startswith('FIXED'):
            results['fixed'] += 1
            if not dry_run:
                print(f'✅ {rel_path}: {result}')
        elif result.startswith('SKIP'):
            results['skipped'] += 1
            if 'too large' in result:
                skipped_files.append((rel_path, result))
        elif result.startswith('FAILED'):
            results['failed'] += 1
            failed_files.append((rel_path, result))
    
    print(f'\n=== Summary ===')
    print(f'Already OK: {results["already_ok"]}')
    print(f'Fixed: {results["fixed"]}')
    print(f'Skipped (diff > 3): {results["skipped"]}')
    print(f'Failed: {results["failed"]}')
    
    if failed_files:
        print(f'\nFailed files ({len(failed_files)}):')
        for path, reason in failed_files:
            print(f'  {path}: {reason}')
    
    if skipped_files:
        print(f'\nSkipped files ({len(skipped_files)}):')
        for path, reason in skipped_files:
            print(f'  {path}: {reason}')


if __name__ == '__main__':
    main()
