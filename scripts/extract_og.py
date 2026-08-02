#!/usr/bin/env python3
"""Extract og:description from truncated pages to use as reference."""
import re
from pathlib import Path

pages = [
    "cv-maker/index.html",
    "time-ago-calculator/index.html",
    "freelancer-rate-calculator/index.html",
    "email-signature-generator/index.html",
    "invoice-template/index.html",
    "cholesterol-ratio-calculator/index.html",
    "business-days-calculator/index.html",
    "fuel-economy-calculator/index.html",
    "muscle-recovery-calculator/index.html",
    "terms-of-service-generator/index.html",
    "stock-options-calculator/index.html",
    "step-goal-calculator/index.html",
    "value-comparison-calculator/index.html",
    "random-sentence-generator/index.html",
    "currency-weight-calculator/index.html",
]

for p in pages:
    fp = Path(p)
    if not fp.exists():
        print(f"MISSING: {p}")
        continue
    content = fp.read_text(encoding='utf-8')
    m = re.search(r'<meta\s+property=[\"\']og:description[\"\']\s+content=\"([^\"]+)\"', content)
    og = m.group(1) if m else 'NO OG'
    # also get h1
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1m.group(1)) if h1m else 'NO H1'
    print(f"--- {p} ---")
    print(f"OG: {og}")
    print(f"H1: {h1}")
    print()