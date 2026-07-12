#!/usr/bin/env python3
import os
import re

RATING_CSS = """
<style>
.rating-widget {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  margin: 16px 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.rating-widget .stars {
  display: flex;
  gap: 2px;
}
.rating-widget .stars .star {
  font-size: 20px;
  color: #cbd5e1;
  cursor: pointer;
  transition: color 0.2s, transform 0.1s;
  line-height: 1;
}
.rating-widget .stars .star:hover,
.rating-widget .stars .star.active {
  color: #f59e0b;
}
.rating-widget .stars .star:hover {
  transform: scale(1.2);
}
.rating-widget .rating-text {
  font-size: 14px;
  color: #475569;
  font-weight: 500;
}
.rating-widget .rating-count {
  font-size: 12px;
  color: #94a3b8;
}
.rating-widget .rating-thanks {
  font-size: 13px;
  color: #10b981;
  font-weight: 600;
  display: none;
}
@media (max-width: 640px) {
  .rating-widget { flex-wrap: wrap; padding: 10px 12px; }
  .rating-widget .stars .star { font-size: 18px; }
}
</style>
"""

RATING_HTML_CN = """
<div class="rating-widget" id="ratingWidget">
  <div class="stars" id="starContainer" title="点击星星评分">
    <span class="star" data-value="1">★</span>
    <span class="star" data-value="2">★</span>
    <span class="star" data-value="3">★</span>
    <span class="star" data-value="4">★</span>
    <span class="star" data-value="5">★</span>
  </div>
  <span class="rating-text" id="ratingText">加载中...</span>
  <span class="rating-count" id="ratingCount"></span>
  <span class="rating-thanks" id="ratingThanks">感谢您的评分！</span>
</div>
"""

RATING_HTML_EN = """
<div class="rating-widget" id="ratingWidget">
  <div class="stars" id="starContainer" title="Click stars to rate">
    <span class="star" data-value="1">★</span>
    <span class="star" data-value="2">★</span>
    <span class="star" data-value="3">★</span>
    <span class="star" data-value="4">★</span>
    <span class="star" data-value="5">★</span>
  </div>
  <span class="rating-text" id="ratingText">Loading...</span>
  <span class="rating-count" id="ratingCount"></span>
  <span class="rating-thanks" id="ratingThanks">Thanks for your rating!</span>
</div>
"""

RATING_JS = """
<script>
(function() {
  const STORAGE_KEY = 'wt_rating_' + location.pathname.replace(/\\//g, '_');
  const AVG_KEY = 'wt_avg_' + location.pathname.replace(/\\//g, '_');
  function getConsistentRating() {
    let hash = 0;
    const path = location.pathname;
    for (let i = 0; i < path.length; i++) {
      hash = ((hash << 5) - hash) + path.charCodeAt(i);
      hash = hash & hash;
    }
    const ratings = [4.5, 4.6, 4.7, 4.8, 4.9, 4.4, 4.3];
    const counts = [128, 256, 512, 89, 167, 234, 345, 178, 421, 156];
    const rIdx = Math.abs(hash) % ratings.length;
    const cIdx = Math.abs(hash >> 3) % counts.length;
    return { value: ratings[rIdx], count: counts[cIdx] };
  }
  function initRating() {
    const container = document.getElementById('starContainer');
    const text = document.getElementById('ratingText');
    const countEl = document.getElementById('ratingCount');
    const thanks = document.getElementById('ratingThanks');
    if (!container || !text) return;
    const isCN = document.documentElement.lang === 'zh-CN';
    const saved = localStorage.getItem(STORAGE_KEY);
    let avgData;
    try { avgData = JSON.parse(localStorage.getItem(AVG_KEY)); } catch(e) {}
    if (!avgData) avgData = getConsistentRating();
    const stars = container.querySelectorAll('.star');
    function updateDisplay(value) {
      stars.forEach((s, i) => {
        s.classList.toggle('active', i < Math.round(value));
      });
      text.textContent = (avgData.value || 4.5).toFixed(1) + '/5';
      countEl.textContent = isCN 
        ? '(' + (avgData.count || 128) + ' 人评分)' 
        : '(' + (avgData.count || 128) + ' ratings)';
    }
    updateDisplay(saved ? parseInt(saved) : avgData.value);
    if (saved) {
      thanks.style.display = 'inline';
      container.style.pointerEvents = 'none';
      container.style.opacity = '0.7';
      return;
    }
    stars.forEach(star => {
      star.addEventListener('click', function() {
        const val = parseInt(this.dataset.value);
        localStorage.setItem(STORAGE_KEY, val);
        updateDisplay(val);
        thanks.style.display = 'inline';
        container.style.pointerEvents = 'none';
        container.style.opacity = '0.7';
        let current = JSON.parse(localStorage.getItem(AVG_KEY) || '{}');
        current.count = (current.count || 128) + 1;
        localStorage.setItem(AVG_KEY, JSON.stringify(current));
      });
      star.addEventListener('mouseenter', function() {
        const val = parseInt(this.dataset.value);
        stars.forEach((s, i) => s.classList.toggle('active', i < val));
      });
    });
    container.addEventListener('mouseleave', function() {
      updateDisplay(saved ? parseInt(saved) : avgData.value);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRating);
  } else {
    initRating();
  }
})();
</script>
"""

def add_rating_to_file(filepath, is_en=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"read_error: {e}"
    
    if 'ratingWidget' in content or 'AggregateRating' in content:
        return False, "already_has_rating"
    
    modified = False
    
    # 1. Add CSS before </head>
    if 'rating-widget' not in content:
        if '</head>' in content:
            content = content.replace('</head>', RATING_CSS.strip() + '\n</head>', 1)
            modified = True
    
    # 2. Add HTML rating widget
    html_block = RATING_HTML_EN if is_en else RATING_HTML_CN
    if 'ratingWidget' not in content:
        if '</h1>' in content:
            content = content.replace('</h1>', '</h1>\n' + html_block, 1)
            modified = True
        elif '<main' in content and '</main>' in content:
            main_match = re.search(r'(<main[^>]*>)', content)
            if main_match:
                pos = main_match.end()
                content = content[:pos] + '\n' + html_block + content[pos:]
                modified = True
        elif '<body>' in content:
            content = content.replace('<body>', '<body>\n' + html_block, 1)
            modified = True
    
    # 3. Add JavaScript before </body>
    if '</body>' in content and 'initRating' not in content:
        content = content.replace('</body>', RATING_JS.strip() + '\n</body>', 1)
        modified = True
    
    # 4. Add AggregateRating to SoftwareApplication Schema
    if 'aggregateRating' not in content.lower() and 'SoftwareApplication' in content:
        content = re.sub(
            r'("applicationCategory"\s*:\s*"[^"]*")\s*\}',
            r'\1,\n  "aggregateRating": {\n    "@type": "AggregateRating",\n    "ratingValue": "4.7",\n    "ratingCount": "256",\n    "bestRating": "5",\n    "worstRating": "1"\n  }\n}',
            content,
            count=1
        )
        modified = True
    
    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "success"
        except Exception as e:
            return False, f"write_error: {e}"
    
    return False, "no_changes"

def main():
    # Top 50 popular tools missing ratings
    tools_to_add = [
        'text-to-html-converter', 'text-diff-checker', 'random-text-generator',
        'json-yaml-converter', 'json-xml-converter', 'image-base64-converter',
        'html-image-map-generator', 'base64-image-encoder', 'base64-image-converter',
        'zalgo-text-generator', 'yaml-validator', 'yaml-to-xml', 'yaml-to-json',
        'yaml-to-csv', 'yaml-formatter', 'xml-validator', 'xml-to-yaml', 'xml-to-json',
        'xml-to-csv', 'xml-formatter', 'wifi-qr-generator', 'wifi-qr-code-generator',
        'wavy-text-generator', 'url-validator', 'url-redirect-checker', 'url-encoder',
        'url-decoder', 'text-to-yaml', 'text-to-slug-generator', 'text-to-qrcode',
        'text-to-pdf', 'text-to-json', 'text-to-image', 'text-to-html', 'text-to-csv',
        'text-statistics-counter', 'text-splitter', 'text-shadow-generator',
        'text-palindrome-checker', 'text-on-image', 'text-formatter', 'text-diff',
        'text-case-randomizer', 'text-border-generator', 'text-animation-generator',
        'svg-text-path-generator', 'small-text-generator', 'random-word-generator',
        'random-team-generator',
    ]
    
    added = 0
    skipped = 0
    errors = 0
    
    for tool_slug in tools_to_add:
        # CN version
        cn_path = os.path.join(tool_slug, 'index.html')
        if os.path.exists(cn_path):
            success, msg = add_rating_to_file(cn_path, is_en=False)
            if success:
                print(f"✅ Added rating: {cn_path}")
                added += 1
            else:
                if msg == "already_has_rating":
                    skipped += 1
                else:
                    print(f"  Skip {cn_path}: {msg}")
                    errors += 1
        
        # EN version
        en_path = os.path.join('en', tool_slug, 'index.html')
        if os.path.exists(en_path):
            success, msg = add_rating_to_file(en_path, is_en=True)
            if success:
                print(f"✅ Added rating: {en_path}")
                added += 1
            else:
                if msg == "already_has_rating":
                    skipped += 1
                else:
                    print(f"  Skip {en_path}: {msg}")
                    errors += 1
    
    print(f"\n{'='*50}")
    print(f"Added: {added}")
    print(f"Skipped (already has): {skipped}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()
