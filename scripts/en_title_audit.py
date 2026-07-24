#!/usr/bin/env python3
"""en_title_audit.py — 扫描所有EN工具title/desc，报告格式问题

检测项目:
1. · 中点分隔符 → 应使用 |
2. Free/No Signup 不在前置 → 应前置
3. desc 缺 CTA (Try now!/Start for free!)
4. title 长度 > 60 字符(截断风险)
5. desc 长度 > 155 字符(截断风险)
6. og:title 与 <title> 不一致
7. publisher.email 非标准
8. og:site_name 不是 "Free ToolBase"
"""

import os
import re
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
EN_DIR = BASE / "en"

def get_title_desc(html: str) -> dict:
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    og_title_m = re.search(r'<meta property="og:title" content="(.*?)"', html, re.DOTALL)
    og_site_m = re.search(r'<meta property="og:site_name" content="(.*?)"', html, re.DOTALL)
    pub_m = re.search(r'"publisher"\s*:\s*\{[^}]*"email"\s*:\s*"([^"]*)"', html, re.DOTALL)
    
    return {
        "title": title_m.group(1) if title_m else "",
        "desc": desc_m.group(1) if desc_m else "",
        "og_title": og_title_m.group(1) if og_title_m else "",
        "og_site_name": og_site_m.group(1) if og_site_m else "",
        "publisher_email": pub_m.group(1) if pub_m else "",
    }

def check_title(title: str) -> list:
    issues = []
    if not title:
        return ["[MISSING] <title> is empty/missing"]
    
    # 1. · 分隔符检查
    if "·" in title:
        issues.append(f"[·_SEP] uses · separator (should use |): \"{title}\"")
    
    # 2. Free前置检查
    if not re.search(r'^Free\s', title):
        issues.append(f"[FREE_POS] title doesn't start with 'Free': \"{title}\"")
    
    # 3. No Signup检查
    # Accept: | No Signup, - No Signup, · No Signup, simply "No Signup" at end
    if not re.search(r'No Signup', title) and not re.search(r'No Download', title) and not re.search(r'Free$', title):
        # Some titles have "Free" at end or "Pure Frontend" instead
        if not title.strip().endswith("Free") and "No Signup" not in title:
            issues.append(f"[CTA_MISS] title missing 'No Signup'/'Free' suffix: \"{title}\"")
    
    # 4. 长度检查
    if len(title) > 60:
        issues.append(f"[TITLE_LEN] title length {len(title)} > 60: \"{title}\"")
    
    # 5. · as separator (not Chinese text)
    # Separate from #1 - this is about when · is used as a separator between concepts
    # (already covered in #1)
    
    return issues

def check_desc(desc: str) -> list:
    issues = []
    if not desc:
        return ["[MISSING] <meta description> is empty/missing"]
    
    # 1. CTA检查
    cta_patterns = [r'Try now', r'Start for free', r'Get started', r'Try it', r'Try today']
    has_cta = any(re.search(p, desc, re.IGNORECASE) for p in cta_patterns)
    if not has_cta:
        issues.append(f"[DESC_CTA] desc missing CTA (Try now! / Start for free!): \"{desc[:80]}...\"")
    
    # 2. 长度检查
    if len(desc) > 155:
        issues.append(f"[DESC_LEN] desc length {len(desc)} > 155: \"{desc[:80]}...\"")
    
    # 3. No Signup检查
    if "No Signup" not in desc and "No signup" not in desc:
        issues.append(f"[DESC_SIGNUP] desc missing 'No signup': \"{desc[:80]}...\"")
    
    return issues

def check_og(title: str, og_title: str, tool_name: str) -> list:
    issues = []
    if og_title and title and og_title != title:
        issues.append(f"[OG_MISMATCH] og:title differs from <title>\n  title:    \"{title}\"\n  og:title:  \"{og_title}\"")
    return issues

def check_publisher(pub_email: str) -> list:
    issues = []
    if pub_email and pub_email != "dexshuang@google.com":
        issues.append(f"[PUB_EMAIL] publisher.email is \"{pub_email}\" (should be dexshuang@google.com)")
    return issues

def check_og_site(og_site: str) -> list:
    issues = []
    if og_site and og_site != "Free ToolBase":
        issues.append(f"[OG_SITE] og:site_name is \"{og_site}\" (should be 'Free ToolBase')")
    return issues

def audit_tool(tool_path: Path) -> dict:
    """Audit a single EN tool directory."""
    index_path = tool_path / "index.html"
    if not index_path.exists():
        return {"path": str(tool_path), "error": "index.html not found"}
    
    html = index_path.read_text(encoding="utf-8", errors="ignore")
    info = get_title_desc(html)
    
    issues = []
    issues.extend(check_title(info["title"]))
    issues.extend(check_desc(info["desc"]))
    issues.extend(check_og(info["title"], info["og_title"], tool_path.name))
    issues.extend(check_publisher(info["publisher_email"]))
    issues.extend(check_og_site(info["og_site_name"]))
    
    return {
        "path": str(tool_path),
        "tool_name": tool_path.name,
        "title": info["title"],
        "desc": info["desc"][:100] + "..." if len(info["desc"]) > 100 else info["desc"],
        "issues": issues,
        "issue_count": len(issues)
    }

def main():
    if not EN_DIR.exists():
        print(f"ERROR: EN directory not found: {EN_DIR}")
        return
    
    tool_dirs = sorted([d for d in EN_DIR.iterdir() if d.is_dir()])
    print(f"Scanning {len(tool_dirs)} EN tool directories...\n")
    
    all_results = []
    total_issues = 0
    issue_summary = {}
    
    for tool_dir in tool_dirs:
        result = audit_tool(tool_dir)
        all_results.append(result)
        if "error" in result:
            continue
        total_issues += result["issue_count"]
        
        for issue in result["issues"]:
            cat = issue.split("]")[0] + "]" if "]" in issue else "OTHER"
            issue_summary[cat] = issue_summary.get(cat, 0) + 1
    
    # Sort by issue count descending
    all_results.sort(key=lambda r: r.get("issue_count", 0), reverse=True)
    
    # Print summary
    print(f"{'='*60}")
    print(f"AUDIT SUMMARY: {total_issues} total issues across {len(tool_dirs)} tools")
    print(f"{'='*60}")
    print()
    
    print("ISSUES BY CATEGORY:")
    for cat, count in sorted(issue_summary.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print()
    
    # Print tools with most issues
    print("TOP 20 TOOLS BY ISSUE COUNT:")
    print(f"{'Issues':>6}  {'Tool Name':<35}")
    print("-" * 45)
    for r in all_results[:20]:
        if r.get("issue_count", 0) > 0:
            print(f"{r['issue_count']:>6}  {r['tool_name']:<35}")
    print()
    
    # Detailed report for each tool with issues
    print("DETAILED ISSUE REPORT:")
    for r in all_results:
        if r.get("issues") and r.get("issue_count", 0) > 0:
            print(f"\n--- {r['tool_name']} ({r['issue_count']} issues) ---")
            for issue in r["issues"]:
                print(f"  {issue}")
    
    # Save JSON report
    report = {
        "total_tools": len(tool_dirs),
        "total_issues": total_issues,
        "tools_with_issues": sum(1 for r in all_results if r["issue_count"] > 0),
        "issue_summary": issue_summary,
        "results": [{k: v for k, v in r.items() if k != "issues"} for r in all_results],
        "detailed_results": all_results
    }
    
    report_path = BASE / "quality" / "en_title_audit_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFull report saved to: {report_path}")
    
    # Print tools with · separator for easy batch fixing
    dot_sep_tools = [r for r in all_results if r.get("issues") and any("·_SEP" in i for i in r["issues"])]
    if dot_sep_tools:
        print(f"\n{'='*60}")
        print(f"TOOLS WITH · SEPARATOR ({len(dot_sep_tools)} total):")
        for r in dot_sep_tools:
            print(f"  {r['tool_name']}: \"{r['title']}\"")
        print(f"\nFix command template:")
        print(f"  grep -rl '<title>.*·.*</title>' en/ | while read f; do ... done")

if __name__ == "__main__":
    main()
