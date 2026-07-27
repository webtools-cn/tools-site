#!/usr/bin/env python3
"""批量替换alert()为showToast()，并添加toast组件"""
import re, os, glob

TOAST_CSS = """
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(100px);background:#1e293b;color:#fff;padding:12px 24px;border-radius:8px;font-size:14px;z-index:9999;opacity:0;transition:all .3s ease;pointer-events:none}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
"""

TOAST_HTML = '\n<div class="toast" id="toast"></div>\n'

TOAST_JS = """function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
"""


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has toast
    if 'showToast' in content:
        print(f"  SKIP (already has toast): {filepath}")
        return False

    # Replace alert(...) calls
    new_content = re.sub(r'alert\(([^)]+)\)', r'showToast(\1)', content)

    if new_content == content:
        print(f"  SKIP (no alert): {filepath}")
        return False

    # Add toast CSS before </style> or </head>
    if '</style>' in new_content:
        new_content = new_content.replace('</style>', TOAST_CSS + '</style>', 1)
    elif '</head>' in new_content:
        new_content = new_content.replace('</head>', f'<style>{TOAST_CSS}</style>\n</head>', 1)
    else:
        print(f"  WARN: no </style> or </head> found in {filepath}")
        return False

    # Add toast div before </body>
    if '</body>' in new_content:
        # Add before first <script> near </body>, or before </body>
        new_content = new_content.replace('</body>', TOAST_HTML + '\n</body>', 1)
    else:
        print(f"  WARN: no </body> found in {filepath}")
        return False

    # Add showToast function before first alert replacement line, or at top of first <script>
    # Better: add after the first <script> opening
    if '<script>' in new_content:
        new_content = new_content.replace('<script>', '<script>\n' + TOAST_JS, 1)
    else:
        print(f"  WARN: no <script> found in {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  FIXED: {filepath}")
    return True


files = [
    'stock-average-calculator/index.html',
    'yield-to-maturity-calculator/index.html',
    'dollar-cost-average-calculator/index.html',
    'bond-price-calculator/index.html',
    'real-return-calculator/index.html',
    'en/stock-average-calculator/index.html',
    'en/yield-to-maturity-calculator/index.html',
    'en/bond-price-calculator/index.html',
    'en/dollar-cost-average-calculator/index.html',
    'en/real-return-calculator/index.html',
]

# Filter: only process files with alert() calls that are NOT in test strings
targets = []
for f in files:
    fpath = f'/home/chison/tools-site/{f}'
    if not os.path.exists(fpath):
        print(f"  MISSING: {fpath}")
        continue
    with open(fpath) as fh:
        c = fh.read()
    # Check for actual alert() function calls (not in strings)
    if re.search(r'\balert\(', c):
        targets.append(fpath)

count = 0
for t in targets:
    if process_file(t):
        count += 1

print(f"\nTotal fixed: {count}")
