import os, re, sys

failing = [
    ("", "index.html"),
    ("tax-calculator", "tax-calculator/index.html"),
    ("checksum-calculator", "checksum-calculator/index.html"),
    ("business-days-calculator", "business-days-calculator/index.html"),
    ("mac-address-lookup", "mac-address-lookup/index.html"),
    ("vin-decoder", "vin-decoder/index.html"),
    ("unicode-lookup", "unicode-lookup/index.html"),
    ("token-estimator", "token-estimator/index.html"),
    ("sql-explainer", "sql-explainer/index.html"),
    ("reaction-test", "reaction-test/index.html"),
    ("gpa-calculator", "gpa-calculator/index.html"),
    ("compound-interest-calculator", "compound-interest-calculator/index.html"),
    ("running-pace-calculator", "running-pace-calculator/index.html"),
    ("metronome-online", "metronome-online/index.html"),
    ("speed-test", "speed-test/index.html"),
    ("wifi-password-generator", "wifi-password-generator/index.html"),
    ("en/backwards-text", "en/backwards-text/index.html"),
    ("en/website-status-checker", "en/website-status-checker/index.html"),
]

for slug, path in failing:
    if not os.path.exists(path):
        print(f'MISSING: {path}')
        continue
    with open(path) as fh:
        content = fh.read()
    
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    meta_len = len(m.group(1)) if m else 0
    
    rm = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    robots = rm.group(1) if rm else 'MISSING'
    
    bgm = re.search(r'body\{[^}]*background:\s*([#\w]+)', content)
    bg = bgm.group(1) if bgm else 'unknown'
    
    print(f'{slug or "HOME":35s} meta:{meta_len:3d} robots:{robots:12s} bg:{bg}')
    if meta_len < 120:
        print(f'  SHORT META: {m.group(1)[:120]}')
