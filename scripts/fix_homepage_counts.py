#!/usr/bin/env python3
"""首页静态数字校准 + 显示bug修复 (2026-09-15)
静态HTML = 无JS环境 + 爬虫看到的索引内容，必须与真实数据一致。
真实数据(tools-data-cn/en.json): 总 3475 | calc 2982 / design 145 / text 79
                                office 62 / pdf 60 / creative 35 / gen 32
                                sports 21 / conv 18 / seo 21 / color 7
用法: python3 fix_homepage_counts.py [--apply]
"""
import sys

BASE = "/home/chison/tools-site/"

EDITS = [
    # ---------- 总数 CN ----------
    ("index.html", "3690+", "3475+", 8),
    ("index.html", "3690个", "3475个", 1),
    ("index.html", ">3690</span>", ">3475</span>", 1),
    ("index.html", "3353+工具", "3475+工具", 1),
    # ---------- 总数 EN ----------
    ("en/index.html", "3690+", "3475+", 6),
    ("en/index.html", ">3690</span>", ">3475</span>", 1),
    ("en/index.html", "3400+", "3475+", 1),
    # ---------- CN 静态分类数 -> 真实值 ----------
    ("index.html", ">3147 个工具", ">2982 个工具", 1),
    ("index.html", ">159 个工具", ">145 个工具", 1),
    ("index.html", ">107 个工具", ">79 个工具", 1),
    ("index.html", ">63 个工具", ">62 个工具", 1),
    ("index.html", ">22 个工具", ">21 个工具", 1),
    ("index.html", ">12 个工具", ">7 个工具", 1),
    # ---------- CN 显示bug: 原始key当名称 ----------
    ("index.html", '<span class="cat-icon">conv-tools</span><span class="cat-name">conv-tools</span>',
     '<span class="cat-icon">\U0001F504</span><span class="cat-name">\U0001F504 转换工具</span>', 1),
    ("index.html", '<span class="cat-icon">color-tools</span><span class="cat-name">color-tools</span>',
     '<span class="cat-icon">\U0001F3A8</span><span class="cat-name">\U0001F3A8 颜色工具</span>', 1),
    # ---------- EN 静态分类数 -> 真实值 ----------
    ("en/index.html", ">3328 tools", ">2982 tools", 1),
    ("en/index.html", ">138 tools", ">145 tools", 1),
    ("en/index.html", ">109 tools", ">79 tools", 1),
    ("en/index.html", ">44 tools", ">7 tools", 1),
    ("en/index.html", ">40 tools", ">62 tools", 1),
    ("en/index.html", ">20 tools", ">60 tools", 1),
    ("en/index.html", ">15 tools", ">35 tools", 1),
]

# 需要按"分类块"定位的计数替换: 数字在块内，全局不唯一
BLOCK_EDITS = [
    ("index.html", "gen-tools", "35", "32"),
    ("index.html", "sports-tools", "23", "21"),
    ("index.html", "conv-tools", "23", "18"),
]


def fix_block(h, cat, old_num, new_num):
    """定位含 setCategory('<cat>') 的 cat-header 块，替换其中唯一的计数数字"""
    key = "setCategory('" + cat + "')"
    i = h.find(key)
    if i < 0:
        return h, 0
    j = h.rfind("cat-header", 0, i)
    seg = h[j:i]
    needle = ">" + old_num + " 个工具"
    if seg.count(needle) != 1:
        return h, 0
    seg2 = seg.replace(needle, ">" + new_num + " 个工具")
    return h[:j] + seg2 + h[i:], 1


def main(apply=False):
    total = 0
    files = sorted({f for f, *_ in EDITS} | {f for f, *_ in BLOCK_EDITS})
    for f in files:
        p = BASE + f
        h = open(p, encoding="utf-8").read()
        orig = h
        for ff, old, new, expect in EDITS:
            if ff != f:
                continue
            n = h.count(old)
            if n != expect:
                print(f"  ❌ {f}: 期望 {expect} 实际 {n} -> {old[:45]!r}")
                continue
            h = h.replace(old, new)
            total += n
        for ff, cat, o, nn in BLOCK_EDITS:
            if ff != f:
                continue
            h, n = fix_block(h, cat, o, nn)
            if n != 1:
                print(f"  ❌ {f}: 块定位失败 {cat} {o}->{nn}")
                continue
            total += n
        if apply and h != orig:
            open(p, "w", encoding="utf-8").write(h)
            print(f"  ✅ 已写入 {f}: {len(h)-len(orig):+d} 字节")
        elif not apply:
            print(f"  · {f}: 预演, 变更 {len(h)-len(orig):+d} 字节")
    print(f"替换总数: {total}" + ("" if apply else "  (预演)"))


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
