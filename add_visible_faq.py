#!/usr/bin/env python3
"""
Add visible FAQ sections to tool pages that have FAQPage Schema but no visible FAQ HTML.
Extracts Q&A from Schema JSON and renders as visible HTML content.
This is critical for GEO (AI search engines need to SEE the FAQ content).
"""
import os, re, json, sys

TOOLS_DIR = os.path.expanduser('~/tools-site')
FAQ_CSS_LIGHT = """.faq-section{margin-top:30px;padding:24px;border-radius:12px;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.04)}
.faq-section h2{font-size:1.3em;margin-bottom:16px;color:#1a1a2e}
.faq-item{background:#f8f9fa;border-radius:10px;padding:16px 20px;margin-bottom:10px;border:1px solid #e9ecef;transition:border-color .2s}
.faq-item:hover{border-color:rgba(6,182,212,.2)}
.faq-item h3{font-size:1em;margin-bottom:6px;color:#333;cursor:pointer;display:flex;align-items:center;gap:8px}
.faq-item h3::before{content:'Q';display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.7rem;font-weight:700;flex-shrink:0}
.faq-item p{color:#666;font-size:.9em;line-height:1.6;padding-left:30px}"""

FAQ_CSS_DARK = """.faq-section{margin-top:32px;padding:24px;border-radius:12px;background:rgba(15,23,42,.6);border:1px solid rgba(148,163,184,.08)}
.faq-section h2{font-size:1.25rem;color:#f1f5f9;margin-bottom:16px}
.faq-item{margin-bottom:12px;padding:14px 16px;border-radius:8px;background:#1e293b;border:1px solid rgba(148,163,184,.08);transition:border-color .2s}
.faq-item:hover{border-color:rgba(6,182,212,.2)}
.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px;cursor:pointer;display:flex;align-items:center;gap:8px}
.faq-item h3::before{content:'Q';display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.7rem;font-weight:700;flex-shrink:0}
.faq-item p{color:#94a3b8;font-size:.88rem;line-height:1.6;padding-left:30px}"""

def is_dark_theme(html):
    """Detect if page uses dark theme"""
    dark_indicators = ['background:#0f172a', 'background:#1e293b', 'background:rgba(15,23,42',
                       'background:#111827', 'background:#0a0a0a', 'color:#f1f5f9',
                       'color:#e2e8f0', 'color:#94a3b8']
    light_indicators = ['background:#f5f7fa', 'background:#fff', 'color:#333',
                        'color:#666', 'color:#1a1a2e']
    dark_count = sum(1 for i in dark_indicators if i in html[:3000])
    light_count = sum(1 for i in light_indicators if i in html[:3000])
    return dark_count > light_count

def extract_faq_from_schema(html):
    """Extract FAQ Q&A from FAQPage Schema JSON"""
    # Find all ld+json blocks
    schema_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for block in schema_blocks:
        try:
            data = json.loads(block)
            if data.get('@type') == 'FAQPage':
                entities = data.get('mainEntity', [])
                faqs = []
                for entity in entities:
                    q = entity.get('name', '')
                    a = entity.get('acceptedAnswer', {}).get('text', '')
                    if q and a:
                        faqs.append((q, a))
                if faqs:
                    return faqs
        except json.JSONDecodeError:
            continue
    return []

def build_faq_html(faqs, is_en=False):
    """Build visible FAQ HTML section"""
    heading = "Frequently Asked Questions (FAQ)" if is_en else "常见问题 (FAQ)"
    items = []
    for q, a in faqs:
        # Handle list-type answers
        if isinstance(a, list):
            a = ' '.join(str(x) for x in a)
        a = str(a)
        # Clean up answer text - convert numbered lists to proper HTML
        a_clean = a.replace('\n', '<br>')
        # Convert patterns like "1）" to proper formatting
        a_clean = re.sub(r'(\d+）)', r'<strong>\1</strong>', a_clean)
        # Convert patterns like "1) " to proper formatting
        a_clean = re.sub(r'(\d+\)\s)', r'<br><strong>\1</strong>', a_clean)
        items.append(f'    <div class="faq-item">\n      <h3>{q}</h3>\n      <p>{a_clean}</p>\n    </div>')
    
    return f'  <div class="faq-section">\n    <h2>{heading}</h2>\n' + '\n'.join(items) + '\n  </div>'

def process_file(filepath):
    """Process a single HTML file to add visible FAQ"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already has visible FAQ
    if 'faq-section' in html:
        return 'already_has_faq'
    
    # Extract FAQ from Schema
    faqs = extract_faq_from_schema(html)
    if not faqs:
        return 'no_schema_faq'
    
    # Determine language
    is_en = '/en/' in filepath or 'lang="en"' in html[:200]
    
    # Determine theme
    dark = is_dark_theme(html)
    css = FAQ_CSS_DARK if dark else FAQ_CSS_LIGHT
    
    # Build FAQ HTML
    faq_html = build_faq_html(faqs, is_en)
    
    # Insert CSS before </head>
    head_close = html.find('</head>')
    if head_close == -1:
        return 'no_head_tag'
    
    # Check if there's already a <style> block we can append to
    # Insert CSS as a new style block before </head>
    css_block = f'<style>{css}</style>\n'
    html = html[:head_close] + css_block + html[head_close:]
    
    # Insert FAQ HTML before </body>, or at end of file if no </body>
    body_close = html.rfind('</body>')
    if body_close == -1:
        # No </body> tag - append at end of file
        html = html.rstrip() + '\n' + faq_html + '\n</body>\n</html>'
    else:
        html = html[:body_close] + '\n' + faq_html + '\n' + html[body_close:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return f'added_{len(faqs)}_faqs'

def main():
    stats = {'added': 0, 'already_has': 0, 'no_schema': 0, 'error': 0, 'total_faqs': 0}
    
    # Find all index.html files
    for root, dirs, files in os.walk(TOOLS_DIR):
        # Skip .git and other non-tool dirs
        if '.git' in root:
            continue
        for f in files:
            if f != 'index.html':
                continue
            filepath = os.path.join(root, f)
            result = process_file(filepath)
            
            if result == 'already_has_faq':
                stats['already_has'] += 1
            elif result == 'no_schema_faq':
                stats['no_schema'] += 1
            elif result.startswith('added_'):
                num = int(result.split('_')[1])
                stats['added'] += 1
                stats['total_faqs'] += num
            else:
                stats['error'] += 1
    
    print(f"=== FAQ Visibility Report ===")
    print(f"Added visible FAQ: {stats['added']} pages ({stats['total_faqs']} Q&A items)")
    print(f"Already had FAQ: {stats['already_has']} pages")
    print(f"No Schema FAQ: {stats['no_schema']} pages")
    print(f"Errors: {stats['error']} pages")

if __name__ == '__main__':
    main()
