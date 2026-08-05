#!/usr/bin/env python3
"""L1 static check for tool pages - extracts JS from HTML and validates."""
import re
import sys
import subprocess
import tempfile
import os

def extract_js(html):
    """Extract all <script> content (non-src, non-ld+json) from HTML."""
    # Match <script> without src attribute and without type="application/ld+json"
    pattern = r'<script(?![^>]*\bsrc=)(?![^>]*\btype\s*=\s*["\']application/ld\+json)[^>]*>(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL)
    return '\n'.join(matches)

def check_js_syntax(html, filepath):
    """Extract JS and run node -c."""
    js = extract_js(html)
    if not js.strip():
        return "NO_JS"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js)
        tmpname = f.name
    try:
        result = subprocess.run(['node', '-c', tmpname], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return "OK"
        else:
            # Return first 3 lines of error
            return "ERROR: " + result.stderr.strip().split('\n')[0][:120]
    except Exception as e:
        return f"EXCEPTION: {e}"
    finally:
        os.unlink(tmpname)

def check_theme(html):
    """Check dark theme compliance."""
    issues = []
    
    # Check :root variables OR inline values
    root_match = re.search(r':root\s*\{([^}]+)\}', html, re.DOTALL)
    if root_match:
        root = root_match.group(1)
        # Check --bg
        bg = re.search(r'--bg\s*:\s*([^;]+)', root)
        if bg and '#0f172a' not in bg.group(1).lower():
            issues.append(f"--bg is '{bg.group(1).strip()}' (expected #0f172a)")
        elif not bg:
            issues.append("--bg not found in :root")
            
        # Check --card-bg
        card_bg = re.search(r'--card-bg\s*:\s*([^;]+)', root)
        if card_bg and '#1e293b' not in card_bg.group(1).lower():
            issues.append(f"--card-bg is '{card_bg.group(1).strip()}' (expected #1e293b)")
        elif not card_bg:
            issues.append("--card-bg not found in :root")
    else:
        # No :root - check inline values for dark theme
        if '#0f172a' not in html:
            issues.append("No #0f172a background color found anywhere")
        if '#1e293b' not in html:
            issues.append("No #1e293b card background found anywhere")
    
    # Check for light backgrounds used as actual backgrounds (background: or background-color:)
    light_bgs = re.findall(r'background(?:-color)?\s*:\s*(#fff|#ffffff|#f8fafc|#f8f9fa|#fdf2f8|#faf8f5)\b', html, re.IGNORECASE)
    if light_bgs:
        issues.append(f"Light background(s) used: {set(light_bgs)}")
    
    # Check for dark text colors used as color:
    dark_text = re.findall(r'(?<!background-)(?<!background)color\s*:\s*(#333|#666)\b', html, re.IGNORECASE)
    if dark_text:
        issues.append(f"Dark text color(s) used: {set(dark_text)}")
    
    return issues if issues else ["OK"]

def check_meta(html):
    """Check meta description length and presence."""
    issues = []
    desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if not desc:
        issues.append("No meta description")
    else:
        d = desc.group(1)
        if len(d) < 50:
            issues.append(f"Meta description too short ({len(d)} chars): {d[:50]}...")
        elif len(d) > 160:
            issues.append(f"Meta description too long ({len(d)} chars)")
    
    # Check title
    title = re.search(r'<title>([^<]+)</title>', html)
    if not title:
        issues.append("No <title> tag")
    
    return issues if issues else ["OK"]

def check_schema(html):
    """Check for Schema.org markup."""
    issues = []
    if 'application/ld+json' not in html:
        issues.append("No JSON-LD schema")
    else:
        if 'SoftwareApplication' not in html and 'WebApplication' not in html:
            issues.append("No SoftwareApplication/WebApplication schema")
        if 'FAQPage' not in html:
            issues.append("No FAQPage schema")
        if 'BreadcrumbList' not in html:
            issues.append("No BreadcrumbList schema")
    return issues if issues else ["OK"]

def check_en_chinese(html):
    """For EN pages, check if Chinese characters are present."""
    chinese = re.findall(r'[\u4e00-\u9fff]+', html)
    if chinese:
        # Filter out comments
        # Count unique Chinese strings
        unique = set(chinese)
        return [f"Chinese text found: {list(unique)[:5]}"]
    return ["OK"]

def check_ga_adsense(html):
    """Check GA and AdSense."""
    issues = []
    if 'google-analytics' not in html and 'gtag' not in html and 'GA_MEASUREMENT' not in html.upper() and 'googletagmanager' not in html:
        issues.append("No Google Analytics")
    if 'adsbygoogle' not in html and 'adsense' not in html.lower():
        issues.append("No AdSense")
    return issues if issues else ["OK"]

def main():
    tools = sys.argv[1:]
    for tool_path in tools:
        lang = "CN" if '/en/' not in tool_path else "EN"
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                html = f.read()
        except Exception as e:
            print(f"❌ {tool_path}: READ ERROR: {e}")
            continue
        
        print(f"\n{'='*60}")
        print(f"📄 {tool_path} ({lang})")
        print(f"{'='*60}")
        
        # JS syntax
        js_result = check_js_syntax(html, tool_path)
        print(f"  JS语法: {js_result}")
        
        # Theme
        theme_issues = check_theme(html)
        print(f"  主题: {', '.join(theme_issues)}")
        
        # Meta
        meta_issues = check_meta(html)
        print(f"  Meta: {', '.join(meta_issues)}")
        
        # Schema
        schema_issues = check_schema(html)
        print(f"  Schema: {', '.join(schema_issues)}")
        
        # GA/AdSense
        ga_issues = check_ga_adsense(html)
        print(f"  GA/AdSense: {', '.join(ga_issues)}")
        
        # EN Chinese
        if lang == "EN":
            en_issues = check_en_chinese(html)
            print(f"  EN中文残留: {', '.join(en_issues)}")
        
        # Count interactive elements (input, button, output divs)
        inputs = len(re.findall(r'<(?:input|textarea|select)\b', html, re.IGNORECASE))
        buttons = len(re.findall(r'<button\b', html, re.IGNORECASE))
        print(f"  交互元素: {inputs} inputs, {buttons} buttons")

if __name__ == '__main__':
    main()
