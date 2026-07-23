#!/usr/bin/env python3
"""Add visual FAQ blocks to EN tool pages that have FAQPage schema but no visual faq-item."""

import json
import re
import os

TOOLS_TO_FIX = [
    "apy-calculator",
    "auto-loan-calculator",
    "average-calculator",
    "bubble-text-generator",
]

BASE = os.path.dirname(os.path.abspath(__file__)) + "/.."

def extract_faq_from_schema(html_content):
    """Extract QA pairs from FAQPage JSON-LD schema."""
    # Find all script tags with ld+json
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    for m in matches:
        try:
            data = json.loads(m.strip())
            if isinstance(data, dict) and data.get("@type") == "FAQPage":
                qa_pairs = []
                for entity in data.get("mainEntity", []):
                    q = entity.get("name", "")
                    a = entity.get("acceptedAnswer", {}).get("text", "")
                    if q and a:
                        qa_pairs.append((q, a))
                return qa_pairs
        except (json.JSONDecodeError, KeyError):
            continue
    return []

def build_faq_html(qa_pairs):
    """Build visual FAQ HTML block."""
    items = []
    for q, a in qa_pairs:
        items.append(f'    <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    items_str = "\n".join(items)
    return f'''  <div class="info-section">
    <h2>Frequently Asked Questions</h2>
{items_str}
  </div>
'''

def has_faq_css(html_content):
    """Check if faq-item CSS exists."""
    return ".faq-item" in html_content

def add_faq_css(html_content):
    """Add faq-item CSS if missing."""
    css = """.faq-item{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}
.faq-item:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.faq-item h3{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}
.faq-item p{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}"""
    
    # Find existing .info-section p CSS and append after it
    pattern = r'(\.info-section\s+p\{[^}]+\})'
    match = re.search(pattern, html_content)
    if match:
        return html_content[:match.end()] + "\n" + css + html_content[match.end():]
    return html_content

def insert_faq_block(html_content, faq_html):
    """Insert FAQ block before footer."""
    # Try to find footer div
    footer_pattern = r'(\n<div class="footer")'
    match = re.search(footer_pattern, html_content)
    if match:
        pos = match.start()
        return html_content[:pos] + faq_html + html_content[pos:]
    
    # Try </main>
    main_pattern = r'(</main>)'
    match = re.search(main_pattern, html_content)
    if match:
        pos = match.start()
        return html_content[:pos] + faq_html + html_content[pos:]
    
    return html_content

def process_tool(tool_name):
    """Process a single tool's EN page."""
    en_path = os.path.join(BASE, "en", tool_name, "index.html")
    
    if not os.path.exists(en_path):
        print(f"  SKIP: {en_path} not found")
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if already has visual FAQ
    if "faq-item" in html:
        print(f"  SKIP: {tool_name} EN already has faq-item")
        return False
    
    # Extract QA from schema
    qa_pairs = extract_faq_from_schema(html)
    if not qa_pairs:
        print(f"  SKIP: {tool_name} EN no FAQPage schema found")
        return False
    
    print(f"  Found {len(qa_pairs)} QA pairs in schema for {tool_name}")
    
    # Build FAQ HTML
    faq_html = build_faq_html(qa_pairs)
    
    # Add CSS if missing
    if not has_faq_css(html):
        html = add_faq_css(html)
        print(f"  Added faq-item CSS")
    
    # Insert FAQ block
    html = insert_faq_block(html, faq_html)
    print(f"  Inserted FAQ visual block")
    
    # Write back
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  DONE: {tool_name} EN")
    return True

def main():
    print("=== Adding visual FAQ blocks to EN pages ===\n")
    fixed = 0
    for tool in TOOLS_TO_FIX:
        print(f"[{tool}]")
        if process_tool(tool):
            fixed += 1
    print(f"\nTotal fixed: {fixed}/{len(TOOLS_TO_FIX)}")

if __name__ == "__main__":
    main()
