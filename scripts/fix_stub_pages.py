#!/usr/bin/env python3
"""修复 368 个跳转/存根页 (2026-09-15)
1. 加 noindex,follow  (原来 0 个有)
2. canonical 指向真实目标 (原来 365/368 指向自己)
3. 移除广告脚本 (原来 368/368 空壳页都在投放广告 —— 广告网络违规风险)
4. 保留 meta refresh 供真人跳转
用法: python3 fix_stub_pages.py [--dry N]
"""
import os, re, sys, json
from urllib.parse import urljoin

BASE = "/home/chison/tools-site/"
LIST = BASE + ".temp/stub_pages.json"
ORIGIN = "https://free-toolbase.com/"

stubs = json.load(open(LIST))
dry = None
if len(sys.argv) > 2 and sys.argv[1] == "--dry":
    dry = int(sys.argv[2])

def public_url(relfile):
    """相对路径 -> 线上 URL"""
    d = os.path.dirname(relfile)
    return ORIGIN + (d + "/" if d else "")

def transform(relfile):
    p = BASE + relfile
    h = open(p, encoding="utf-8").read()
    before = h
    orig_url = public_url(relfile)

    # --- 1. 解析跳转目标(绝对URL) ---
    m = re.search(r'http-equiv="refresh"\s+content="0;url=([^"]+)"', h)
    target = urljoin(orig_url, m.group(1)) if m else orig_url
    if target.rstrip("/") == orig_url.rstrip("/"):
        target = ""   # 自己没有跳转目标 -> 不写 canonical

    # --- 2. noindex ---
    if re.search(r'<meta\s+name="robots"[^>]*>', h):
        h = re.sub(r'<meta\s+name="robots"[^>]*>',
                   '<meta name="robots" content="noindex, follow">', h, count=1)
    else:
        h = h.replace('<meta charset="UTF-8">',
                      '<meta charset="UTF-8">\n<meta name="robots" content="noindex, follow">', 1)

    # --- 3. canonical 指向真实目标 ---
    if target:
        h = re.sub(r'<link rel="canonical" href="[^"]*">',
                   '<link rel="canonical" href="%s">' % target, h, count=1)
        h = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
                   r'\g<1>%s\g<2>' % target, h, count=1)

    # --- 4. 移除广告脚本(空壳页不得投放) ---
    h = re.sub(r'[ \t]*<script[^>]*profitableratecpmnetwork[^>]*></script>\s*\n?', '', h)

    if h != before:
        open(p, "w", encoding="utf-8").write(h)
    return orig_url, target, (h != before)

if dry:
    for s in stubs[:dry]:
        o, t, c = transform(s["file"])
        print(f"--- {s['file']}\n    原URL : {o}\n    新canonical: {t}\n    已修改: {c}\n")
    print(open(BASE + stubs[0]["file"], encoding="utf-8").read()[:1400])
else:
    changed = 0
    for s in stubs:
        try:
            _, _, c = transform(s["file"])
            changed += 1 if c else 0
        except Exception as e:
            print("ERR", s["file"], e)
    print(f"已修改 {changed}/{len(stubs)} 个存根页")
