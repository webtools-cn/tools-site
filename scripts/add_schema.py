#!/usr/bin/env python3
"""给缺失Schema的工具页添加SoftwareApplication"""
import re

FILES_DATA = [
    ('fica-tax-calculator', 'FICA Tax Calculator', 'FICA Tax Calculator'),
    ('en/fica-tax-calculator', 'FICA Tax Calculator', 'FICA Tax Calculator'),
    ('freelancer-rate-calculator', 'Freelancer Rate Calculator', 'Freelancer Rate Calculator'),
    ('en/freelancer-rate-calculator', 'Freelancer Rate Calculator', 'Freelancer Rate Calculator'),
    ('hydration-tracker', 'Hydration Tracker', 'Hydration Tracker'),
    ('en/hydration-tracker', 'Hydration Tracker', 'Hydration Tracker'),
]

schema_tpl = '<script type="application/ld+json">\n  {{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"HealthApplication","operatingSystem":"All","url":"https://free-toolbase.com/{path}/","offers":{{"@type":"Offer","price":"0"}}}}\n  </script>'

for path, name, desc in FILES_DATA:
    f = path + '/index.html'
    with open(f) as fh:
        content = fh.read()
    
    if 'SoftwareApplication' in content:
        continue
    
    # 在 AdSense 脚本后插入
    schema = schema_tpl.format(name=name, desc=desc, path=path)
    # 尝试多种marker
    markers = ['crossorigin="anonymous"></script>', 'crossorigin="anonymous">\n']
    for marker in markers:
        if marker in content:
            content = content.replace(marker, marker + '\n' + schema)
            break
    else:
        # fallback: 在</head>之前插入
        content = content.replace('</head>', schema + '\n</head>')
    
    with open(f, 'w') as fh:
        fh.write(content)
    print(f'{f}: done')

print('Done')