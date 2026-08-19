#!/usr/bin/env python3
"""
Add visible trust signals to tool pages.
These are critical for GEO (AI search engines look for authority signals)
and SEO (builds user trust, reduces bounce rate).
Signals: client-side processing, no signup, 100% free, instant results.
"""
import os, re, sys

def has_trust_signals(content):
    """Check if page already has trust signal component."""
    # Only check for actual trust signal UI components, not text mentions
    indicators = ['class="trust-signals"', 'class="trust-badges"', 'class="trust-badge"']
    return any(ind in content for ind in indicators)

def generate_trust_signals_html(lang='en'):
    """Generate trust signal badges HTML."""
    if lang == 'en':
        html = '''  <div class="trust-signals" style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin:12px 0;padding:8px 0;">
    <span style="background:#ecfdf5;color:#065f46;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">🔒 Client-side — Your data never leaves your browser</span>
    <span style="background:#eff6ff;color:#1e40af;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">✅ 100% Free — No signup, no limits</span>
    <span style="background:#fefce8;color:#854d0e;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">⚡ Instant — No server processing</span>
  </div>'''
    else:
        html = '''  <div class="trust-signals" style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin:12px 0;padding:8px 0;">
    <span style="background:#ecfdf5;color:#065f46;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">🔒 数据不上传 — 一切在浏览器中处理</span>
    <span style="background:#eff6ff;color:#1e40af;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">✅ 100%免费 — 无需注册，无使用限制</span>
    <span style="background:#fefce8;color:#854d0e;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:500;">⚡ 即时处理 — 无需等待服务器</span>
  </div>'''
    return html

def find_insertion_point(content):
    """Find where to insert trust signals - after star rating or after description."""
    # After star-rating component
    m = re.search(r'</div>\s*\n(\s*<div class="tool-container")', content)
    if m:
        return m.start(1)
    
    # After star-rating
    m = re.search(r'(<div class="star-rating".*?</div>)\s*\n', content, re.DOTALL)
    if m:
        return m.end()
    
    # After the description paragraph
    m = re.search(r'</p>\s*\n(\s*<div)', content)
    if m:
        return m.start(1)
    
    # After h1
    m = re.search(r'</h1>\s*\n(\s*<div)', content)
    if m:
        return m.start(1)
    
    return -1

def process_page(filepath, lang='en'):
    """Process a single page to add trust signals."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if has_trust_signals(content):
        return False, "Already has trust signals"
    
    html = generate_trust_signals_html(lang)
    insert_pos = find_insertion_point(content)
    
    if insert_pos == -1:
        return False, "Can't find insertion point"
    
    content = content[:insert_pos] + html + '\n' + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, "Added trust signals"

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
