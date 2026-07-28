#!/usr/bin/env python3
"""修复 content_thin/very_thin：把误放在<script>标签内的HTML内容移出来"""
import re, os

FILES = [
    # CN content_very_thin
    'child-height-predictor/index.html',
    'hourly-wage-calculator/index.html',
    'payback-period-calculator/index.html',
    'pregnancy-weight-calculator/index.html',
    'strength-level-calculator/index.html',
    # CN content_thin
    'api-doc-generator/index.html',
    'html-beautify/index.html',
    'receipt-generator/index.html',
    'tag-cloud/index.html',
    # EN content_thin
    'en/child-height-predictor/index.html',
    'en/markdown-to-pdf-converter/index.html',
    'en/payback-period-calculator/index.html',
    'en/pregnancy-weight-calculator/index.html',
    'en/strength-level-calculator/index.html',
]

fixed = 0
for f in FILES:
    path = os.path.join('/home/chison/tools-site', f)
    if not os.path.exists(path):
        print(f'SKIP (not found): {f}')
        continue
    
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Pattern: <script>\n\n<SEO-or-footer-HTML>\n<footer>...</footer>\n<script>...real JS
    # Fix: remove the empty script wrapper around HTML content
    # The pattern is: </main>\n\n<script>\n\n<div/section...>...</footer>\n<script>
    
    original = content
    
    # Fix 1: close empty <script> before SEO content and move SEO HTML out
    # Pattern: <script>\n\n<div class="seo-content"... or <section class="related-tools"...
    content = re.sub(
        r'(</main>\s*)\n<script>\n\n(<div class="seo-content".*?</div>)\n(<section class="related-tools".*?</section>)\n(<footer>.*?</footer>)\n<script>',
        r'\1\n\2\n\3\n\4\n<script>',
        content,
        flags=re.DOTALL
    )
    
    # Fix 1b: pattern without seo-content (just related-tools)
    content = re.sub(
        r'(</main>\s*)\n<script>\n\n(<section class="related-tools".*?</section>)\n(<footer>.*?</footer>)\n<script>',
        r'\1\n\2\n\3\n<script>',
        content,
        flags=re.DOTALL
    )
    
    # Fix 1c: just footer inside script
    content = re.sub(
        r'(</main>\s*)\n<script>\n\n(<footer>.*?</footer>)\n<script>',
        r'\1\n\2\n<script>',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'FIXED: {f}')
        fixed += 1
    else:
        print(f'NO CHANGE: {f}')

print(f'\nTotal fixed: {fixed}')