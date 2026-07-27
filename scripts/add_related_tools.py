#!/usr/bin/env python3
"""Add related-tools section to newly generated tool pages"""
import os

BASE = "/home/chison/tools-site"
NEW_SLUGS = [
    "spaced-repetition-scheduler",
    "pomodoro-tracker",
    "pronunciation-guide",
    "vocabulary-builder",
    "multiplication-table-generator",
]

CN_RELATED = '''
<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 相关工具推荐</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"><a href="/age-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🎂 在线年龄计算器</a><a href="/body-shape-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📐 体型计算器</a><a href="/sleep-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">😴 睡眠周期计算器</a></div></section>
'''

EN_RELATED = '''
<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">🔗 Related Tools</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"><a href="/en/age-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">🎂 Age Calculator</a><a href="/en/body-shape-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">📐 Body Shape Calculator</a><a href="/en/sleep-calculator/" style="display:inline-block;padding:6px 12px;margin:4px;background:var(--bg,#f0f0f0);border-radius:6px;text-decoration:none;color:var(--primary,#4F46E5);font-size:14px;">😴 Sleep Cycle Calculator</a></div></section>
'''

INSERT_BEFORE_CN = '<div class="footer">'
INSERT_BEFORE_EN = '<div class="footer">'

for slug in NEW_SLUGS:
    # CN
    cn_path = os.path.join(BASE, slug, "index.html")
    with open(cn_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(INSERT_BEFORE_CN, CN_RELATED.strip() + "\n" + INSERT_BEFORE_CN, 1)
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ CN: {slug}")

    # EN
    en_path = os.path.join(BASE, "en", slug, "index.html")
    with open(en_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(INSERT_BEFORE_EN, EN_RELATED.strip() + "\n" + INSERT_BEFORE_EN, 1)
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ EN: {slug}")

print("\n🎉 Related tools added to all 10 pages")