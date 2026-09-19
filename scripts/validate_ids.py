#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🔴 全站 ID 铁律闸门 v2 —— 每次改动页面/新工具/提交前必须跑。

用户铁律（最高优先级，逐字）：
  「不管是开发新任务还是做调整，必须保障谷歌搜索、谷歌分析后台的 ID、
    必应搜索后台 ID、广告 ID —— 这三个必须保持准确，并且全站覆盖。
    第二点，sitemap 要完全正确，不能错误。」

四组 ID（每页 <head> 内必须齐全，一个都不能丢、不能错）:
  1 GA 加载器    https://www.googletagmanager.com/gtag/js?id=G-QVBQNJ3L5E
  2 GA config    gtag('config','G-QVBQNJ3L5E')
  3 Adsterra     https://pl31040516.profitableratecpmnetwork.com/28/e9/94/....js
  4 Bing 验证    <meta name="msvalidate.01" content="19B854C82A618C376CC972901EF717E5">

根目录验证文件:
  googlefd1a7b2848e1c305.html
  内容 = google-site-verification: googlefd1a7b2848e1c305.html
  robots.txt 不得屏蔽它

用法:
  python3 scripts/validate_ids.py                 # 全站扫描
  python3 scripts/validate_ids.py <slug> [...]    # 只查指定页
  python3 scripts/validate_ids.py --diff          # 只查 git 本次改动的页
  python3 scripts/validate_ids.py --fix           # 自动补缺失的 Bing 验证标签（唯一可自动补的项）

实现要点（血泪教训）:
  正则里**绝对不要写引号字符**（单/双引号经 shell + 文件多层转义后必然出错，
  会静默匹配失败 → 全站假阳性）。一律先 str.find 定位标记，再对切片跑纯 ASCII 正则。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GA = "G-9W1157EBQV"   # 用户唯一正确 GA 属性（2026-09-16 曾被误迁移，已回滚）
ADSTERRA_HOST = "pl31040516.profitableratecpmnetwork"
BING_ID = "19B854C82A618C376CC972901EF717E5"
GOOGLE_FILE = "googlefd1a7b2848e1c305.html"
GOOGLE_FILE_BODY = "google-site-verification: " + GOOGLE_FILE

# 零容忍：任何页面出现即判 FAIL（含"正确 ID 的打错版"）
FORBIDDEN = [
    "G-QVBQNJ3L5E",                       # 废弃 GA（2026-09-16 误迁移产物，永久封禁）
    "G-4BZ4DM6QDM", "G-PZN7F2ESMS", "G-1RHEM5P4NK", "G-7WLERB1KHP",
    "G-XXXXXXXXXX",                       # 占位符
    "19B854C82C618C376CC972901EF717E5",   # Bing 打错版（第10位 C 应为 A）
]
RE_FORBIDDEN_CA_PUB = re.compile(r"ca-pub-[0-9]+")  # 任何 AdSense ID 一律禁止

BING_TAG = '<meta name="msvalidate.01" content="%s">' % BING_ID
RE_ID = re.compile(r"[A-Z]{1,2}-[A-Z0-9]{6,}")


def head_of(html):
    i = html.find("</head>")
    return html[:i] if i > 0 else html


def _id_after(text, marker, window=60):
    j = text.find(marker)
    if j < 0:
        return None
    m = RE_ID.search(text[j + len(marker): j + len(marker) + window])
    return m.group(0) if m else None


def check_page(path, do_fix=False):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    head = head_of(raw)
    probs = []

    loader = _id_after(head, "gtag/js?id=")
    if loader is None:
        probs.append("1 缺 GA 加载器")
    elif loader != GA:
        probs.append("1 GA 加载器 ID 错误 -> %s" % loader)

    cfg = None
    for mk in ("gtag('config'", 'gtag("config"'):
        cfg = _id_after(head, mk)
        if cfg:
            break
    if cfg is None:
        probs.append("2 缺 GA config")
    elif cfg != GA:
        probs.append("2 GA config ID 错误 -> %s" % cfg)

    if ADSTERRA_HOST not in head:
        probs.append("3 缺 Adsterra 广告脚本")

    if BING_ID not in head:
        if do_fix:
            j = raw.find("</head>")
            if j > 0:
                raw = raw[:j] + "  " + BING_TAG + "\n" + raw[j:]
                open(path, "w", encoding="utf-8").write(raw)
                head = head_of(raw)
        if BING_ID not in head:
            probs.append("4 缺 Bing 站长验证 msvalidate.01")

    for b in FORBIDDEN:
        if b in head:
            probs.append("!! 禁用 ID 残留 -> %s" % b)
    m = RE_FORBIDDEN_CA_PUB.search(head)
    if m:
        probs.append("!! 禁用 AdSense ID 残留 -> %s" % m.group(0))
    return probs


def check_root_files():
    probs = []
    fp = os.path.join(ROOT, GOOGLE_FILE)
    if not os.path.exists(fp):
        probs.append("缺 Google 验证文件 %s" % GOOGLE_FILE)
    else:
        body = open(fp, encoding="utf-8", errors="ignore").read().strip()
        if GOOGLE_FILE_BODY not in body:
            probs.append("Google 验证文件内容不对: %r" % body[:80])
    robots = os.path.join(ROOT, "robots.txt")
    if os.path.exists(robots):
        r = open(robots, encoding="utf-8", errors="ignore").read()
        # 只认"整行就是 Disallow: /"（真全站屏蔽）；不能拿子串判定，
        # 否则 Disallow: /quality-reports/ 会被误判 → 假阳性
        blocks_all = any(
            ln.strip().rstrip("/").strip() == "Disallow:"
            for ln in r.splitlines()
        )
        if blocks_all and GOOGLE_FILE not in r:
            probs.append("robots.txt 整站屏蔽（Disallow: /），Google 验证文件会取不到")
    return probs


def collect_targets(args):
    if "--diff" in sys.argv:
        changed = subprocess.run(["git", "diff", "--name-only", "HEAD"],
                                 cwd=ROOT, capture_output=True, text=True).stdout.split()
        return [os.path.join(ROOT, f) for f in changed if f.endswith("index.html")]
    if args:
        out = []
        for a in args:
            p = os.path.join(ROOT, a.strip("/"), "index.html")
            if os.path.exists(p):
                out.append(p)
            else:
                print("warning: not found %s" % a)
        return out
    out = []
    for r, d, fs in os.walk(ROOT):
        parts = r.split(os.sep)
        if ".git" in parts or "node_modules" in parts:
            continue
        if "index.html" in fs:
            out.append(os.path.join(r, "index.html"))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_fix = "--fix" in sys.argv
    targets = collect_targets(args)

    bad = []
    for p in targets:
        probs = check_page(p, do_fix=do_fix)
        if probs:
            bad.append((os.path.relpath(p, ROOT), probs))
    root_probs = check_root_files()

    exit_code = 0
    if bad:
        exit_code = 1
        print("FAIL %d/%d 页 ID 不合格:" % (len(bad), len(targets)))
        for rel, probs in bad[:40]:
            print("   " + rel)
            for x in probs:
                print("      - " + x)
        if len(bad) > 40:
            print("   ... 共 %d 页不合格（上面只列前 40）" % len(bad))
    if root_probs:
        exit_code = 1
        print("FAIL 根目录验证文件:")
        for x in root_probs:
            print("   - " + x)
    if exit_code == 0:
        print("PASS ID 铁律通过: %d 页全部 OK (GA=1 GAconfig=1 Adsterra=1 Bing=1, 零禁用ID)" % len(targets))
        print("PASS 根目录: %s 存在且内容正确, robots.txt 未屏蔽" % GOOGLE_FILE)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
