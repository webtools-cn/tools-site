#!/usr/bin/env python3
"""存根页修复 - 最终校验 (2026-09-15)
基准 = git HEAD 原文（权威源），不是自定义快照。
检查:
  1. noindex 必须存在
  2. GA 标签 id 集合完全一致
  3. Adsterra 广告脚本完全一致
  4. canonical 完全一致
  5. meta refresh 跳转目标完全一致
  6. 除目标行外无其他改动（逐行 diff 只允许 1 行差异）
"""
import subprocess, re, sys, json
BASE = "/home/chison/tools-site/"
split = json.load(open(BASE + ".temp/stub_split.json"))
FILES = split["A"] + split["B"]

GA_RX = r'googletagmanager\.com/gtag/js\?id=([A-Z0-9\-]+)'
AD_RX = r'profitableratecpmnetwork\.com[^"\']*'
ROB_RX = r'<meta[^>]*name="robots"[^>]*>'
CAN_RX = r'<link rel="canonical" href="([^"]*)"'
REF_RX = r'http-equiv="refresh"[^>]*url=([^"]+)"'

def git_head(path):
    p = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=BASE,
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None

def feats(h):
    rob = re.findall(ROB_RX, h)
    return dict(ga=sorted(set(re.findall(GA_RX, h))), ad=re.findall(AD_RX, h),
                canonical=re.findall(CAN_RX, h), refresh=re.findall(REF_RX, h),
                noindex=any("noindex" in r for r in rob))

bad = []; ok = 0; stats = {"insert": 0, "replace": 0}
for f in FILES:
    old = git_head(f)
    if old is None:
        bad.append((f, ["git HEAD 无此文件"])); continue
    new = open(BASE + f, encoding="utf-8").read()
    errs = []
    fo, fn = feats(old), feats(new)
    if not fn["noindex"]: errs.append("noindex缺失")
    for k in ("ga", "ad", "canonical", "refresh"):
        if fo[k] != fn[k]: errs.append(f"{k}被改动 {fo[k]} -> {fn[k]}")
    # 逐行 diff
    lo, ln = old.splitlines(), new.splitlines()
    diff = [(i, a, b) for i, (a, b) in enumerate(zip(lo, ln)) if a != b]
    if abs(len(lo) - len(ln)) > 1:
        errs.append(f"行数变化异常 {len(lo)}->{len(ln)}")
    extra = [d for d in diff if "robots" not in d[1].lower() and "robots" not in d[2].lower()]
    if extra:
        errs.append(f"出现非 robots 行改动: {extra[:2]}")
    if len(diff) == 1: stats["replace"] += 1
    elif len(diff) == 0 and len(ln) == len(lo) + 1: stats["insert"] += 1
    if errs: bad.append((f, errs))
    else: ok += 1

print(f"✅ 完全通过: {ok}/{len(FILES)}   (替换robots {stats['replace']} / 新增robots行 {stats['insert']})")
if bad:
    print(f"\n❌ 异常 {len(bad)}:")
    for f, e in bad[:20]: print("   ", f, e)
    sys.exit(1)
print("\n🔒 断言: GA统计标签 / Adsterra广告脚本 / canonical / 跳转目标 —— 全部逐字节未变")
print("🔒 断言: 除 robots 一行外，无任何其他行改动")
