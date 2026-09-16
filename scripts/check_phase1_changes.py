#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase1 独立校验脚本 (不依赖修改脚本).

用法: python3 scripts/check_phase1_changes.py
基线: git tag backup-before-phase1-20260916

校验内容:
  1. 每页 GA加载器 / GA config / Adsterra 数量 == 1/1/1
  2. canonical / JSON-LD / h1文本 / script数量 / h1数量 与基线一致
  3. 归一化对比: 屏蔽 title/description/og:title/og:description 及
     </h1>..</main> 正文区间后, 其余字节必须与基线完全相同
     -> 证明改动 100% 落在允许字段, 且正文区间内未新增 script
  4. 内联 JS node --check
"""
import os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "backup-before-phase1-20260916"
PAGES = [
    "business-days-calculator/index.html",
    "business-day-calculator/index.html",
    "tax-refund-calculator/index.html",
    "checksum-calculator/index.html",
    "pow-captcha/index.html",
    "timesheet-calculator/index.html",
]

GA_LOADER = r'googletagmanager\.com/gtag/js\?id=G-QVBQNJ3L5E'
GA_CONFIG = r"gtag\('config','G-QVBQNJ3L5E'\)"
ADSTERRA = r'pl31040516\.profitableratecpmnetwork'

errors = []
warnings = []


def sh(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def baseline(path):
    r = sh(["git", "show", TAG + ":" + path])
    if r.returncode != 0:
        errors.append("%s: 无法从 %s 读取基线 (%s)" % (path, TAG, r.stderr.strip()))
        return None
    return r.stdout


def current(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def count(pattern, s):
    return len(re.findall(pattern, s))


def extract_h1(s):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return m.group(1) if m else None


def extract_canonical(s):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', s)
    return m.group(1) if m else None


def extract_jsonld(s):
    return re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S)


def body_region(s):
    """</h1> 之后到 </main> 之前的正文内容"""
    i = s.find('</h1>')
    j = s.find('</main>')
    if i < 0 or j < 0:
        return None
    return s[i + 5:j]


def normalize(s):
    """屏蔽 4 个允许字段 + 正文区间"""
    s = re.sub(r'<title>.*?</title>', '<title>@@TITLE@@</title>', s, flags=re.S)
    s = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', r'\1@@DESC@@\2', s, flags=re.I)
    s = re.sub(r'(<meta\s+content=")[^"]*("\s+name="description")', r'\1@@DESC@@\2', s, flags=re.I)
    s = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', r'\1@@OGT@@\2', s, flags=re.I)
    s = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', r'\1@@OGD@@\2', s, flags=re.I)
    i = s.find('</h1>')
    j = s.find('</main>')
    assert i >= 0 and j >= 0
    s = s[:i + 5] + '@@BODY@@' + s[j:]
    return s


def check_js(path, s):
    scripts = re.findall(r'<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>(.*?)</script>', s, re.S)
    node = shutil.which("node")
    if not node:
        warnings.append("%s: 未找到 node, 跳过 JS 语法检查" % path)
        return
    for idx, code in enumerate(scripts):
        if not code.strip():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
            tmpname = tmp.name
        try:
            r = subprocess.run([node, "--check", tmpname], capture_output=True, text=True)
            if r.returncode != 0:
                errors.append("%s: 内联 script#%d JS 语法错误: %s" % (path, idx, r.stderr.strip().splitlines()[:1]))
            else:
                print("   [js] %s inline script#%d node --check OK" % (path, idx))
        finally:
            os.unlink(tmpname)


def main():
    for path in PAGES:
        print("=" * 60)
        print("CHECK", path)
        base = baseline(path)
        cur = current(path)
        if base is None:
            continue

        # 1. 三要素
        for label, pat in [("GA loader", GA_LOADER), ("GA config", GA_CONFIG), ("Adsterra", ADSTERRA)]:
            nb, nc = count(pat, base), count(pat, cur)
            if nc != 1:
                errors.append("%s: %s 数量=%d (应为 1)" % (path, label, nc))
            if nc != nb:
                errors.append("%s: %s 数量变化 %d -> %d" % (path, label, nb, nc))
            print("   %-10s base=%d current=%d %s" % (label, nb, nc, "OK" if nc == nb == 1 else "FAIL"))

        # 2. 结构
        for label, fn in [("canonical", extract_canonical), ("h1-text", extract_h1)]:
            b, c = fn(base), fn(cur)
            if b != c:
                errors.append("%s: %s 变化\n   base=%r\n   cur =%r" % (path, label, b, c))
            print("   %-10s %s %s" % (label, "OK" if b == c else "FAIL", "" if b == c else "%r -> %r" % (b, c)))

        for label, pat in [("script-tag", r'<script'), ("h1-tag", r'<h1'), ("canonical-tag", r'rel="canonical"')]:
            nb, nc = count(pat, base), count(pat, cur)
            if nb != nc:
                errors.append("%s: %s 数量变化 %d -> %d" % (path, label, nb, nc))
            print("   %-10s base=%d current=%d %s" % (label, nb, nc, "OK" if nb == nc else "FAIL"))

        jb, jc = extract_jsonld(base), extract_jsonld(cur)
        if jb != jc:
            errors.append("%s: JSON-LD 内容变化 (%d 块 -> %d 块)" % (path, len(jb), len(jc)))
        print("   %-10s base=%d current=%d %s" % ("jsonld", len(jb), len(jc), "OK" if jb == jc else "FAIL"))

        # 3. 正文区间内不得新增 script
        body = body_region(cur)
        if body is None:
            errors.append("%s: 找不到 </h1> 或 </main>" % path)
        elif "<script" in body:
            errors.append("%s: 正文区间内新增了 <script>" % path)

        # 4. 归一化对比 (证明改动仅在允许字段)
        nb, nc = normalize(base), normalize(cur)
        if nb != nc:
            errors.append("%s: 归一化对比不一致 -> 存在允许字段之外的改动" % path)
            # 定位首个差异
            for k in range(min(len(nb), len(nc))):
                if nb[k] != nc[k]:
                    errors.append("   首个差异位置 %d:\n   base: %r\n   cur : %r" % (k, nb[max(0, k - 60):k + 60], nc[max(0, k - 60):k + 60]))
                    break
        print("   %-10s %s" % ("normalized", "OK (仅允许字段被改动)" if nb == nc else "FAIL"))

        # 5. JS 语法
        check_js(path, cur)

    print("=" * 60)
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  ! " + w)
    if errors:
        print("RESULT: FAIL (%d errors)" % len(errors))
        for e in errors:
            print("  x " + e)
        sys.exit(1)
    print("RESULT: PASS — 全部 6 页通过 (三要素 1/1/1, 结构一致, 改动均在允许字段, JS 语法 OK)")


if __name__ == "__main__":
    main()
