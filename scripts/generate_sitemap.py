#!/usr/bin/env python3
"""Generate complete sitemap.xml for free-toolbase.com"""

import os
from pathlib import Path
from datetime import datetime

SITE_DIR = Path("/home/chison/tools-site")
OUTPUT_FILE = SITE_DIR / "sitemap.xml"
BASE_URL = "https://free-toolbase.com"

def get_all_pages():
    """Get all index.html files and convert to URLs"""
    pages = []
    
    # CN pages (root level)
    for tool_dir in sorted(SITE_DIR.iterdir()):
        if tool_dir.is_dir() and tool_dir.name not in ['en', 'scripts', 'quality', '.git', '.github', '.gsc-data', 'css', 'js']:
            index_file = tool_dir / "index.html"
            if index_file.exists():
                slug = tool_dir.name
                pages.append({
                    'url': f"{BASE_URL}/{slug}/",
                    'lastmod': datetime.fromtimestamp(index_file.stat().st_mtime).strftime('%Y-%m-%d'),
                    'priority': '0.8'
                })
    
    # EN pages
    en_dir = SITE_DIR / "en"
    if en_dir.exists():
        for tool_dir in sorted(en_dir.iterdir()):
            if tool_dir.is_dir() and tool_dir.name not in ['scripts', 'quality', '.git']:
                index_file = tool_dir / "index.html"
                if index_file.exists():
                    slug = tool_dir.name
                    pages.append({
                        'url': f"{BASE_URL}/en/{slug}/",
                        'lastmod': datetime.fromtimestamp(index_file.stat().st_mtime).strftime('%Y-%m-%d'),
                        'priority': '0.8'
                    })
    
    return pages

def generate_sitemap(pages):
    """Generate sitemap XML"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Homepage CN
    xml += f'''<url>
  <loc>{BASE_URL}/</loc>
  <lastmod>{today}</lastmod>
  <changefreq>weekly</changefreq>
  <priority>1.0</priority>
</url>
'''
    
    # Homepage EN
    xml += f'''<url>
  <loc>{BASE_URL}/en/</loc>
  <lastmod>{today}</lastmod>
  <changefreq>weekly</changefreq>
  <priority>1.0</priority>
</url>
'''
    
    # Tool pages
    for page in pages:
        xml += f'''<url>
  <loc>{page['url']}</loc>
  <lastmod>{page['lastmod']}</lastmod>
  <changefreq>monthly</changefreq>
  <priority>{page['priority']}</priority>
</url>
'''
    
    xml += '</urlset>'
    return xml

def main():
    print("Scanning pages...")
    pages = get_all_pages()
    
    cn_count = sum(1 for p in pages if '/en/' not in p['url'])
    en_count = sum(1 for p in pages if '/en/' in p['url'])
    
    print(f"Found {len(pages)} pages ({cn_count} CN + {en_count} EN)")
    
    print("Generating sitemap...")
    sitemap = generate_sitemap(pages)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    
    print(f"Saved to {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
