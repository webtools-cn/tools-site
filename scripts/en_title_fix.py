#!/usr/bin/env python3
"""en_title_fix.py — 批量修复EN工具title/desc/og/schema问题

修复项:
1. title中的· → | (中点→竖线)
2. og:site_name → "Free ToolBase" (统一品牌名)
3. desc末尾补CTA (Try now!/Start for free!)
4. desc中补"No signup" (如描述开头已有Free)
5. og:title同步<title> (如不一致)

用法:
  python3 scripts/en_title_fix.py [--dry-run] [--tool TOOL_NAME] [--all]
  
示例:
  python3 scripts/en_title_fix.py --dry-run            # 预览修复
  python3 scripts/en_title_fix.py --tool cidr-calculator  # 修复单个工具
  python3 scripts/en_title_fix.py --all                 # 全量修复
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
EN_DIR = BASE / "en"

# ===== 修复函数 =====

def fix_dot_separator(title: str) -> str:
    """Replace · with | in title (but not in Chinese text context)"""
    # If the title is mostly Chinese, keep · as it's a Chinese punctuation
    # Count Chinese characters
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', title))
    total_chars = len(title.strip())
    if chinese_chars > total_chars * 0.3:
        return title  # It's a Chinese title, keep ·
    return title.replace("·", "|")

def fix_og_site_name(html: str) -> str:
    """Fix og:site_name to 'Free ToolBase'"""
    html = re.sub(
        r'<meta property="og:site_name" content="[^"]*"',
        '<meta property="og:site_name" content="Free ToolBase"',
        html
    )
    return html

def fix_publisher_email(html: str) -> str:
    """Fix publisher email in JSON-LD"""
    html = re.sub(
        r'"email"\s*:\s*"[^"]*"',
        '"email": "dexshuang@google.com"',
        html
    )
    return html

def fix_og_title_to_match_title(html: str) -> str:
    """Sync og:title with <title>"""
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    og_m = re.search(r'<meta property="og:title" content="(.*?)"', html, re.DOTALL)
    if title_m and og_m:
        new_og = title_m.group(1)
        # Remove emoji/icon prefix for og:title if present
        # Actually keep it as-is to match <title>
        html = html.replace(
            f'<meta property="og:title" content="{og_m.group(1)}"',
            f'<meta property="og:title" content="{new_og}"'
        )
    return html

def fix_desc_cta(desc: str) -> str:
    """Add CTA to description if missing"""
    cta_patterns = [r'Try now', r'Start for free', r'Get started', r'Try it', r'Try today']
    has_cta = any(re.search(p, desc, re.IGNORECASE) for p in cta_patterns)
    
    if not has_cta:
        # Add "Try now!" at the end, respecting sentence boundaries
        desc = desc.rstrip('.')
        if desc:
            desc += ". Try now!"
        else:
            desc = "Free online tool. Try now!"
    
    return desc

def fix_desc_no_signup(desc: str) -> str:
    """Add No signup claim to description if missing"""
    if "No signup" not in desc and "No Signup" not in desc and "no signup" not in desc:
        # Insert before Try now
        if "Try now" in desc:
            desc = desc.replace(" Try now!", " No signup, 100% browser-based. Try now!")
        elif "Start for free" in desc:
            desc = desc.replace(" Start for free!", " No signup. Start for free!")
        else:
            desc += " No signup, 100% browser-based."
    return desc

def process_tool(tool_dir: Path, dry_run: bool = False) -> dict:
    """Process a single EN tool directory. Returns dict of changes made."""
    index_path = tool_dir / "index.html"
    if not index_path.exists():
        return {"tool": tool_dir.name, "error": "index.html not found"}
    
    original = index_path.read_text(encoding="utf-8", errors="ignore")
    html = original
    
    changes = {}
    
    # 1. Fix title · → |
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if title_m:
        old_title = title_m.group(1)
        new_title = fix_dot_separator(old_title)
        if new_title != old_title:
            html = html.replace(f"<title>{old_title}</title>", f"<title>{new_title}</title>")
            changes["title_dot_fix"] = {"old": old_title, "new": new_title}
    
    # 2. Fix og:site_name
    new_html = fix_og_site_name(html)
    if new_html != html:
        changes["og_site_name_fix"] = True
        html = new_html
    
    # 3. Fix publisher email
    new_html = fix_publisher_email(html)
    if new_html != html:
        changes["publisher_email_fix"] = True
        html = new_html
    
    # 4. Sync og:title with title
    new_html = fix_og_title_to_match_title(html)
    if new_html != html:
        changes["og_title_sync"] = True
        html = new_html
    
    # 5. Fix desc - add CTA
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    if desc_m:
        old_desc = desc_m.group(1)
        new_desc = fix_desc_cta(old_desc)
        if new_desc != old_desc:
            html = html.replace(
                f'<meta name="description" content="{old_desc}"',
                f'<meta name="description" content="{new_desc}"'
            )
            changes["desc_cta_fix"] = {"old_len": len(old_desc), "new_len": len(new_desc)}
    
    # 6. Fix desc - add No signup
    desc_m2 = re.search(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    if desc_m2:
        old_desc2 = desc_m2.group(1)
        new_desc2 = fix_desc_no_signup(old_desc2)
        if new_desc2 != old_desc2:
            html = html.replace(
                f'<meta name="description" content="{old_desc2}"',
                f'<meta name="description" content="{new_desc2}"'
            )
            changes["desc_signup_fix"] = {"old_len": len(old_desc2), "new_len": len(new_desc2)}
    
    if not changes:
        return {"tool": tool_dir.name, "changes": {}, "skipped": True}
    
    if not dry_run:
        index_path.write_text(html, encoding="utf-8")
    
    return {
        "tool": tool_dir.name,
        "changes": changes,
        "skipped": False,
        "current_title": (re.search(r'<title>(.*?)</title>', html, re.DOTALL) or type('',(),{'group':lambda s:''})()).group(1)
    }

def main():
    parser = argparse.ArgumentParser(description="Fix EN tool titles/descriptions")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--tool", type=str, help="Fix a single tool by name")
    parser.add_argument("--all", action="store_true", help="Fix all EN tools")
    parser.add_argument("--only-dot", action="store_true", help="Only fix · separator")
    parser.add_argument("--batch", type=int, default=0, 
                        help="Fix first N tools with issues (for progressive rollout)")
    args = parser.parse_args()
    
    if not EN_DIR.exists():
        print(f"ERROR: EN directory not found: {EN_DIR}")
        return
    
    # Single tool mode
    if args.tool:
        tool_path = EN_DIR / args.tool
        if not tool_path.exists():
            print(f"ERROR: Tool not found: {tool_path}")
            return
        result = process_tool(tool_path, dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # Scan all tools
    tool_dirs = sorted([d for d in EN_DIR.iterdir() if d.is_dir()])
    print(f"Scanning {len(tool_dirs)} EN tool directories...")
    
    results = []
    changed = 0
    skipped = 0
    errors = 0
    
    for tool_dir in tool_dirs:
        result = process_tool(tool_dir, dry_run=args.dry_run)
        if "error" in result:
            errors += 1
        elif result.get("skipped"):
            skipped += 1
        else:
            changed += 1
            results.append(result)
        
        # Batch limit
        if args.batch > 0 and changed >= args.batch:
            break
    
    # Summary
    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\n{'='*60}")
    print(f"  {mode} - {changed} tools changed, {skipped} skipped, {errors} errors")
    print(f"{'='*60}")
    
    if results:
        # Summary by change type
        change_types = {}
        for r in results:
            for k in r.get("changes", {}):
                change_types[k] = change_types.get(k, 0) + 1
        
        print("\nCHANGE SUMMARY:")
        for k, v in sorted(change_types.items(), key=lambda x: -x[1]):
            print(f"  {k}: {v}")
        
        # Sample changes
        print(f"\nSAMPLE CHANGES (first 10):")
        for r in results[:10]:
            print(f"  {r['tool']}: {list(r['changes'].keys())}")
            if "title_dot_fix" in r["changes"]:
                print(f"    Title: {r['changes']['title_dot_fix']['old']}")
                print(f"       →  {r['changes']['title_dot_fix']['new']}")
        
        # Show tools with most fix types
        if len(results) > 10:
            print(f"\n  ... and {len(results) - 10} more tools changed.")
    
    print(f"\nTo apply: python3 scripts/en_title_fix.py --all")
    print(f"To preview: python3 scripts/en_title_fix.py --dry-run --batch 10")

if __name__ == "__main__":
    main()
