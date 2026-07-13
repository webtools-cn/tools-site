#!/usr/bin/env python3
"""
Add visible star-rating components to tool pages that have AggregateRating in Schema
but no visible rating UI. This is critical for SEO/GEO because Google requires
structured data to match visible content for rich results.
"""
import os, re, sys

def extract_rating_from_schema(content):
    """Extract ratingValue and ratingCount from AggregateRating schema."""
    # Try ratingValue first, then ratingCount
    patterns = [
        r'"ratingValue"\s*:\s*"([^"]+)"[^}]*"ratingCount"\s*:\s*"([^"]+)"',
        r'"ratingCount"\s*:\s*"([^"]+)"[^}]*"ratingValue"\s*:\s*"([^"]+)"',
    ]
    for i, pattern in enumerate(patterns):
        m = re.search(pattern, content, re.DOTALL)
        if m:
            if i == 0:
                return m.group(1), m.group(2)
            else:
                return m.group(2), m.group(1)
    return None, None

def rating_to_stars(rating_value):
    """Convert numeric rating to star characters."""
    try:
        val = float(rating_value)
    except (ValueError, TypeError):
        return "★★★★★", 5, 0
    
    full_stars = int(val)
    half_star = 1 if (val - full_stars) >= 0.3 else 0
    empty_stars = 5 - full_stars - half_star
    
    star_str = "★" * full_stars
    if half_star:
        star_str += "½"
    star_str += "☆" * empty_stars
    
    return star_str, full_stars, empty_stars

def generate_star_rating_html(rating_value, rating_count, lang='en'):
    """Generate visible star rating HTML component."""
    star_str, _, _ = rating_to_stars(rating_value)
    
    if lang == 'en':
        count_text = f"({rating_count} ratings)"
        aria_label = f"Rated {rating_value} out of 5 stars based on {rating_count} ratings"
    else:
        count_text = f"（{rating_count}人评分）"
        aria_label = f"基于{rating_count}人评分，{rating_value}星（满分5星）"
    
    html = f'''  <div class="star-rating" style="display:flex;align-items:center;gap:8px;margin:16px 0;padding:12px 16px;background:#f8f9fa;border-radius:8px;border:1px solid #e9ecef;" aria-label="{aria_label}">
    <span style="font-size:20px;color:#f59e0b;letter-spacing:2px;">{star_str}</span>
    <span style="font-size:16px;font-weight:600;color:#1f2937;">{rating_value}</span>
    <span style="font-size:14px;color:#6b7280;">{count_text}</span>
  </div>'''
    
    return html

def find_insertion_point(content):
    """Find where to insert the star rating - after the tool description, before the main tool area."""
    # Best: after the tool description paragraph, before the tool container
    # Look for patterns that indicate the end of the description area
    
    # Pattern 1: After the description paragraph, before tool-container or main area
    patterns = [
        # After description, before tool-container
        (r'(</p>\s*\n)(\s*<div class="tool-container")', 1),
        # After description, before the main tool div
        (r'(</p>\s*\n)(\s*<div class="container")', 1),
        # After h1, before tool area
        (r'(</h1>\s*\n)(\s*<div)', 1),
        # Before the first textarea/input (tool UI starts)
        (r'(\n)(\s*<textarea)', 1),
        # Before the first input element
        (r'(\n)(\s*<input)', 1),
    ]
    
    for pattern, group in patterns:
        m = re.search(pattern, content)
        if m:
            return m.start(group)
    
    # Fallback: after the first </p> tag
    m = re.search(r'</p>', content)
    if m:
        return m.end()
    
    return -1

def process_page(filepath, lang='en'):
    """Process a single page to add visible star rating if missing."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has visible star rating
    if 'class="star-rating"' in content:
        return False, "Already has star-rating"
    
    # Extract rating from schema
    rating_value, rating_count = extract_rating_from_schema(content)
    if not rating_value or not rating_count:
        return False, "No AggregateRating in Schema"
    
    # Generate HTML
    star_html = generate_star_rating_html(rating_value, rating_count, lang)
    
    # Find insertion point
    insert_pos = find_insertion_point(content)
    if insert_pos == -1:
        return False, "Can't find insertion point"
    
    # Insert the star rating
    content = content[:insert_pos] + '\n' + star_html + '\n' + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"Added star rating ({rating_value}/5, {rating_count} ratings)"

def main():
    stats = {'processed': 0, 'updated': 0, 'skipped': 0, 'errors': 0}
    
    # Process both language directories
    for lang_dir, lang in [('en', 'en'), ('.', 'cn')]:
        base = os.path.join(os.getcwd(), lang_dir)
        
        if not os.path.isdir(base):
            continue
        
        for tool_dir in sorted(os.listdir(base)):
            idx = os.path.join(base, tool_dir, 'index.html')
            if not os.path.isfile(idx):
                continue
            
            # Skip non-tool pages
            if tool_dir in ('about', 'privacy-policy', 'terms-of-service', 'contact', 'feedback',
                          'quality-reports', '__pycache__', '.git'):
                continue
            
            stats['processed'] += 1
            try:
                updated, msg = process_page(idx, lang)
                if updated:
                    stats['updated'] += 1
                    if stats['updated'] <= 20:  # Only print first 20
                        print(f"✅ {lang}/{tool_dir}: {msg}")
                else:
                    stats['skipped'] += 1
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 10:
                    print(f"❌ {lang}/{tool_dir}: {e}")
    
    print(f"\n📊 Stats: processed={stats['processed']}, updated={stats['updated']}, skipped={stats['skipped']}, errors={stats['errors']}")

if __name__ == '__main__':
    main()
