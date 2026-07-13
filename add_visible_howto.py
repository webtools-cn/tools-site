#!/usr/bin/env python3
"""
Add visible HowTo steps to tool pages that have HowTo in Schema but no visible steps.
Google requires structured data to match visible content for rich results.
This is critical for HowTo rich snippets in search results.
"""
import os, re, sys

def extract_howto_from_schema(content):
    """Extract HowTo steps from Schema.org JSON-LD."""
    steps = []
    
    # Find HowTo schema - use .*? instead of [^}]*? because there are nested objects
    m = re.search(r'"@type"\s*:\s*"HowTo".*?"step"\s*:\s*\[(.*?)\]', content, re.DOTALL)
    if not m:
        return steps
    
    step_content = m.group(1)
    
    # Extract step name and text
    # Pattern for each step - position may come before name
    step_pattern = r'"@type"\s*:\s*"HowToStep"\s*,\s*"position"\s*:\s*\d+\s*,\s*"name"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"text"\s*:\s*"((?:[^"\\]|\\.)*)"'
    matches = re.findall(step_pattern, step_content, re.DOTALL)
    
    # Also try without position
    if not matches:
        step_pattern = r'"@type"\s*:\s*"HowToStep"\s*,\s*"name"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"text"\s*:\s*"((?:[^"\\]|\\.)*)"'
        matches = re.findall(step_pattern, step_content, re.DOTALL)
    
    for name, text in matches:
        name = name.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', ' ')
        text = text.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', ' ')
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        steps.append((name, text))
    
    return steps

def has_visible_howto(content):
    """Check if page already has visible HowTo steps section."""
    indicators = ['class="howto-steps"', 'class="how-to-steps"', 'class="usage-steps"']
    return any(ind in content for ind in indicators)

def generate_howto_html(steps, lang='en'):
    """Generate visible HowTo steps HTML."""
    if not steps:
        return ""
    
    if lang == 'en':
        header = "📋 How to Use"
    else:
        header = "📋 使用步骤"
    
    html_parts = [
        f'  <div class="howto-steps" style="margin:16px 0;padding:16px 20px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;">',
        f'    <h2 style="font-size:1.1rem;font-weight:600;margin:0 0 12px 0;color:#1e293b;">{header}</h2>',
        f'    <ol style="margin:0;padding-left:24px;">',
    ]
    
    for i, (name, text) in enumerate(steps, 1):
        name_esc = name.replace('<', '&lt;').replace('>', '&gt;')
        html_parts.append(f'      <li style="margin-bottom:8px;line-height:1.6;"><strong>{name_esc}</strong> — {text}</li>')
    
    html_parts.append(f'    </ol>')
    html_parts.append(f'  </div>')
    
    return '\n'.join(html_parts)

def find_insertion_point(content):
    """Find where to insert HowTo steps - after trust signals, before tool container."""
    # After trust-signals
    m = re.search(r'(<div class="trust-signals".*?</div>)\s*\n', content, re.DOTALL)
    if m:
        return m.end()
    
    # After star-rating
    m = re.search(r'(<div class="star-rating".*?</div>)\s*\n', content, re.DOTALL)
    if m:
        return m.end()
    
    # After description paragraph
    m = re.search(r'</p>\s*\n(\s*<div class="tool-container")', content)
    if m:
        return m.start(1)
    
    # Before tool container
    m = re.search(r'(<div class="tool-container")', content)
    if m:
        return m.start(1)
    
    return -1

def process_page(filepath, lang='en'):
    """Process a single page to add visible HowTo steps."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if has_visible_howto(content):
        return False, "Already has visible HowTo"
    
    steps = extract_howto_from_schema(content)
    if not steps:
        return False, "No HowTo in Schema"
    
    html = generate_howto_html(steps, lang)
    insert_pos = find_insertion_point(content)
    
    if insert_pos == -1:
        return False, "Can't find insertion point"
    
    content = content[:insert_pos] + html + '\n' + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"Added {len(steps)} visible HowTo steps"

def main():
    stats = {'processed': 0, 'updated': 0, 'skipped': 0, 'errors': 0}
    
    for lang_dir, lang in [('en', 'en'), ('.', 'cn')]:
        base = os.path.join(os.getcwd(), lang_dir)
        
        if not os.path.isdir(base):
            continue
        
        for tool_dir in sorted(os.listdir(base)):
            idx = os.path.join(base, tool_dir, 'index.html')
            if not os.path.isfile(idx):
                continue
            
            if tool_dir in ('about', 'privacy-policy', 'terms-of-service', 'contact', 'feedback',
                          'quality-reports', '__pycache__', '.git'):
                continue
            
            stats['processed'] += 1
            try:
                updated, msg = process_page(idx, lang)
                if updated:
                    stats['updated'] += 1
                    if stats['updated'] <= 10:
                        print(f"✅ {lang}/{tool_dir}: {msg}")
                else:
                    stats['skipped'] += 1
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 5:
                    print(f"❌ {lang}/{tool_dir}: {e}")
    
    print(f"\n📊 Stats: processed={stats['processed']}, updated={stats['updated']}, skipped={stats['skipped']}, errors={stats['errors']}")

if __name__ == '__main__':
    main()
