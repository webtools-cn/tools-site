#!/usr/bin/env python3
"""存根页最小修复 (2026-09-15) — 只加 noindex，不碰广告/GA/canonical

安全约束（用户明确要求）:
  ✋ 不动广告脚本
  ✋ 不动 GA 标签
  ✋ 不改 canonical
  ✋ 不改任何其他字节

流程: 基线快照 -> 最小插入 -> 逐文件字节校验 -> 输出报告
用法: python3 fix_stub_minimal.py --baseline | --apply | --verify
"""
import os, re, sys, json, hashlib

BASE = "/home/chison/tools-site/"
SPLIT = BASE + ".temp/stub_split.json"
BASE_SNAP = BASE + ".temp/stub_baseline.json"
ROBOTS_LINE = '<meta name="robots" content="noindex, follow">'
GA_RX = r'googletagmanager\.com/gtag/js\?id=([A-Z0-9\-]+)'
AD_RX = r'profitableratecpmnetwork\.com[^"\']*'
ROBOTS_RX = r'<meta\s+name="robots"[^>]*content="([^"]*)"'

def snap(path):
    h = open(path, encoding="utf-8").read()
    return {
        "md5": hashlib.md5(h.encode()).hexdigest(),
        "size": len(h),
        "ga": sorted(set(re.findall(GA_RX, h))),
        "ad": re.findall(AD_RX, h),
        "robots": re.findall(ROBOTS_RX, h),
        "noindex": "noindex" in " ".join(re.findall(ROBOTS_RX, h)),
        "canonical": re.findall(r'<link rel="canonical" href="([^"]*)"', h),
        "refresh": re.findall(r'http-equiv="refresh"[^>]*url=([^"]+)"', h),
    }

def targets():
    d = json.load(open(SPLIT))
    return d["A"] + d["B"]

def baseline():
    out = {}
    for f in targets():
        out[f] = snap(BASE + f)
    json.dump(out, open(BASE_SNAP, "w"), ensure_ascii=False, indent=1)
    print(f"基线快照: {len(out)} 个文件")
    ga = {}
    for f, s in out.items():
        for g in s["ga"]:
            ga[g] = ga.get(g, 0) + 1
    print("  GA 分布:", ga)
    print("  带广告脚本:", sum(1 for s in out.values() if s["ad"]))
    print("  已有 noindex:", sum(1 for s in out.values() if s["noindex"]))
    print("  已有 robots 标签:", sum(1 for s in out.values() if s["robots"]))
    print("  有跳转目标:", sum(1 for s in out.values() if s["refresh"]))

def apply():
    changed = 0
    for f in targets():
        p = BASE + f
        h = open(p, encoding="utf-8").read()
        m = re.search(r'<meta\s+name=["\']?robots["\']?[^>]*>', h, re.I)
        if m and "noindex" in m.group(0).lower():
            continue
        if m:
            h2 = h[:m.start()] + ROBOTS_LINE + h[m.end():]
        else:
            a = '<meta charset="UTF-8">'
            if a not in h:
                print("  ⚠️ 无 charset 锚点，跳过:", f); continue
            h2 = h.replace(a, a + "\n" + ROBOTS_LINE, 1)
        open(p, "w", encoding="utf-8").write(h2)
        changed += 1
    print(f"已插入 noindex: {changed} 个文件")

def verify():
    snap0 = json.load(open(BASE_SNAP))
    bad = []
    ok = 0
    for f, s0 in snap0.items():
        s1 = snap(BASE + f)
        errs = []
        if not s1["noindex"]:
            errs.append("noindex缺失")
        if s1["ga"] != s0["ga"]:
            errs.append(f"GA变了 {s0['ga']}->{s1['ga']}")
        if s1["ad"] != s0["ad"]:
            errs.append("广告脚本变了")
        if s1["canonical"] != s0["canonical"]:
            errs.append("canonical变了")
        if s1["refresh"] != s0["refresh"]:
            errs.append("跳转目标变了")
        # 只允许新增一行
        delta = s1["size"] - s0["size"]
        if delta != len(ROBOTS_LINE) + 1:
            errs.append(f"字节增量异常 {delta} (应为{len(ROBOTS_LINE)+1})")
        if errs:
            bad.append((f, errs))
        else:
            ok += 1
    print(f"✅ 校验通过: {ok}/{len(snap0)}")
    if bad:
        print(f"❌ 异常 {len(bad)} 个:")
        for f, e in bad[:20]:
            print("   ", f, e)
    return bad

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--baseline"
    if mode == "--baseline": baseline()
    elif mode == "--apply": apply()
    elif mode == "--verify": verify()
