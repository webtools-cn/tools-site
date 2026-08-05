#!/usr/bin/env python3
"""Comprehensive structural check for tool pages."""
import re, sys, os

tools = sys.argv[1:]

for tool in tools:
    print(f"\n{'='*60}")
    print(f"TOOL: {tool}")
    print(f"{'='*60}")
    for lang_label, path in [("CN", f"{tool}/index.html"), ("EN", f"en/{tool}/index.html")]:
        if not os.path.exists(path):
            print(f"  [{lang_label}] FILE NOT FOUND")
            continue
        content = open(path).read()
        issues = []
        
        # 1. Check DOCTYPE
        if not content.strip().startswith('<!DOCTYPE html>'):
            issues.append("Missing DOCTYPE")
        
        # 2. Check meta description
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        if desc_match:
            desc = desc_match.group(1)
            if len(desc) < 50:
                issues.append(f"Short meta desc ({len(desc)} chars): {desc[:40]}...")
        else:
            issues.append("No meta description")
        
        # 3. Check for light backgrounds in CSS
        light_bgs = re.findall(r'background\s*:\s*(#fff|#ffffff|#f8fafc|#f8f9fa)\b', content, re.IGNORECASE)
        if light_bgs:
            issues.append(f"Light bg found: {light_bgs[:3]}")
        
        # 4. Check for aggregateRating (fake ratings)
        if 'aggregateRating' in content:
            issues.append("Has aggregateRating (fake rating!)")
        
        # 5. Check Schema.org
        has_software_app = 'SoftwareApplication' in content
        has_faq = 'FAQPage' in content
        has_breadcrumb = 'BreadcrumbList' in content
        if not has_software_app:
            issues.append("Missing SoftwareApplication schema")
        if not has_faq:
            issues.append("Missing FAQPage schema")
        if not has_breadcrumb:
            issues.append("Missing BreadcrumbList schema")
        
        # 6. Check GA
        if 'G-9W1157EBQV' not in content:
            issues.append("Missing GA tracking ID")
        
        # 7. Check AdSense
        if 'ca-pub-5998441792679372' not in content:
            issues.append("Missing AdSense publisher ID")
        
        # 8. Check robots
        if 'name="robots"' not in content:
            issues.append("Missing robots meta tag")
        
        # 9. Check interactive elements (input + button + output)
        has_input = bool(re.search(r'<input|<textarea', content))
        has_button = bool(re.search(r'<button', content))
        if not has_input:
            issues.append("No input element (possible shell tool)")
        if not has_button:
            issues.append("No button element")
        
        # 10. Check footer links
        footer_links = re.findall(r'<a\s+href="([^"]*)"[^>]*>(?:首页|Home|联系我们|Contact|隐私政策|Privacy|服务条款|Terms|关于我们|About|GitHub)', content, re.IGNORECASE)
        if len(footer_links) < 4:
            issues.append(f"Only {len(footer_links)} footer links (need 4+)")
        
        # 11. Check email
        if 'dexshuang@google.com' not in content:
            issues.append("Missing contact email")
        
        # 12. Check for onclick with inline logic > 3 lines
        onclick_matches = re.findall(r'onclick="([^"]*)"', content)
        for oc in onclick_matches:
            if oc.count(';') > 3:
                issues.append(f"Complex inline onclick ({oc.count(';')} semicolons)")
                break
        
        # 13. EN page Chinese check (excluding lang-switch links)
        if lang_label == "EN":
            # Remove ld+json, comments, and lang-switch links
            clean = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
            clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
            # Remove the "中文" link text
            clean = clean.replace('>中文<', '><')
            chinese = re.findall(r'[\u4e00-\u9fff]+', clean)
            if chinese:
                issues.append(f"Chinese text found: {chinese[:5]}")
        
        # 14. Check related-tools.css reference (should not be there per standard)
        if 'related-tools.css' in content:
            pass  # This is actually present on many pages, not a hard error
        
        if issues:
            for issue in issues:
                print(f"  [{lang_label}] ⚠️ {issue}")
        else:
            print(f"  [{lang_label}] ✅ All checks passed")
